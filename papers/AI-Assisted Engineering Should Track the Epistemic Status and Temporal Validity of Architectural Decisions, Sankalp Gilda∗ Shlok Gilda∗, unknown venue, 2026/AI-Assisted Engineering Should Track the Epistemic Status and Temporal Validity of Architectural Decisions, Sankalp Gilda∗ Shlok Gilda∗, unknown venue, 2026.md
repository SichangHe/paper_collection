                                             AI-A SSISTED E NGINEERING S HOULD T RACK THE E PISTEMIC
                                               S TATUS AND T EMPORAL VALIDITY OF A RCHITECTURAL
                                                                    D ECISIONS

                                                                                               A P REPRINT


                                                                  Sankalp Gilda∗                                          Shlok Gilda∗
                                                               DeepThought Solutions                              Department of Computer Science
arXiv:2601.21116v1 [cs.SE] 28 Jan 2026




                                                        sankalp@deepthoughtsolutions.xyz                               University of Florida
                                                             sankalp.gilda@gmail.com                                  shlokgilda@ufl.edu




                                                                                              A BSTRACT
                                                   This position paper argues that AI-assisted software engineering requires explicit mechanisms
                                                   for tracking the epistemic status and temporal validity of architectural decisions. LLM coding
                                                   assistants generate decisions faster than teams can validate them, yet no widely-adopted framework
                                                   distinguishes conjecture from verified knowledge, prevents trust inflation through conservative
                                                   aggregation, or detects when evidence expires. We propose three requirements for responsible
                                                   AI-assisted engineering: (1) epistemic layers that separate unverified hypotheses from empirically
                                                   validated claims, (2) conservative assurance aggregation grounded in the Gödel t-norm that prevents
                                                   weak evidence from inflating confidence, and (3) automated evidence decay tracking that surfaces
                                                   stale assumptions before they cause failures. We formalize these requirements as the First Principles
                                                   Framework (FPF), ground its aggregation semantics in fuzzy logic, and define a quintet of invariants
                                                   that any valid aggregation operator must satisfy. Our retrospective audit applying FPF criteria to two
                                                   internal projects found that 20–25% of architectural decisions had stale evidence within two months,
                                                   validating the need for temporal accountability. We outline research directions including learnable
                                                   aggregation operators, federated evidence sharing, and SMT-based claim validation.

                                         Keywords AI-assisted software engineering, decision accountability, epistemic rigor, evidence decay, formal methods


                                         1    Introduction

                                         Modern LLM coding assistants (GitHub Copilot, Cursor, Claude Code, Gemini Code Assist) speed up software
                                         development but open a gap: decisions are made faster than they can be validated. A developer asks “Should I
                                         use Redis or Memcached?” The AI gives an answer that lacks epistemic qualification, the developer implements
                                         it immediately, and nobody revisits the assumptions when a library update or infrastructure change invalidates the
                                         original rationale. Software engineering is the canary for a broader problem. In drug interaction screening, a model
                                         like Med-PaLM [Singhal et al., 2023] may assess a combination as safe based on training data that predates an
                                         FDA contraindication update, and nothing in the system tracks that the underlying evidence has expired. In legal
                                         contract analysis, an AI assistant drafts clauses referencing case law that was subsequently overturned; the output
                                         carries no metadata distinguishing established precedent from dicta in an unpublished opinion. In autonomous
                                         scientific experimentation [Boiko et al., 2023], a lab agent selects reagent concentrations from literature values obtained
                                         under different assay conditions, with no distinction between “validated in our setup” and “worked in a related
                                         context.” ML engineering suffers the same problem reflexively: models are selected based on benchmark results that
                                         predate evaluation-harness changes, hyperparameter choices cite ablation studies from different data distributions,
                                         and deployment decisions assume training-time metrics transfer to production, each decision cached as institutional
                                         knowledge and rarely revisited.

                                             * Equal contribution.
                          Epistemic Status and Temporal Validity in AI-Assisted Engineering                   A P REPRINT



We ground the paper in software engineering because it has the most deployment data available today, but the framework
applies to any domain where decisions rest on evidence that expires.
Four problems follow:

      1. No distinction between “untested hypothesis” and “empirically verified claim.” A cached LLM suggestion and
         a load-tested benchmark carry equal weight in team memory.
      2. Multiple weak arguments get averaged into strong-seeming evidence. Three blog posts do not equal one
         controlled experiment, but informal reasoning treats them as comparable.
      3. No tracking of when evidence expires. Benchmarks go stale, dependencies update, requirements change, yet
         decisions persist as if the world were frozen.
      4. No audit trail showing why decisions were made or what conditions would invalidate them. Post-mortems
         repeatedly find “nobody remembers why we chose X.”

A recent survey of 47 academic studies on generative AI for software architecture [Esposito et al., 2025] finds that 93%
of surveyed papers report no validation of LLM-generated architectural outputs. Current LLM reasoning approaches
address parts of this problem. Self-consistency voting [Wang et al., 2023] aggregates multiple reasoning paths. Verifier
scoring [Lightman et al., 2024] rates individual reasoning steps. Chain-of-thought prompting [Wei et al., 2022]
produces interpretable traces. But none of these approaches provide explicit epistemic layers, temporal validity tracking,
conservative aggregation with formal guarantees, or durable audit trails that survive beyond a single session.
Our position: AI-assisted engineering workflows demand mathematical guarantees against epistemic drift. We
formalize this through a principled framework with three core properties: First, explicit epistemic layers must distinguish
unverified hypotheses (L0) from empirically validated claims (L2). Second, conservative assurance aggregation requires
adherence to a quintet of mathematical invariants, ensuring that no conclusion can be more reliable than its weakest
supporting evidence (the WLNK bound), and that formality levels impose hard reliability ceilings regardless of
consensus: ten informal observations cannot equal one controlled experiment. Third, evidence validity windows must
be tracked mechanically through automated alerts, not through aspirational review schedules that teams deprioritize
under delivery pressure. These claims are falsifiable: a practitioner could reasonably argue that averaging better captures
engineering judgment, that such formality ceilings are arbitrary gatekeeping, or that periodic human review suffices
without automation.
Scope of this paper. This paper does not propose a specific tool or evaluate a system. It argues that the three properties
above are necessary for responsible AI-assisted engineering regardless of implementation. While we ground our
examples in LLM coding assistants, the framework applies equally to research agents, planning agents, and any
AI system that generates recommendations with epistemic implications. We formalize these properties as the First
Principles Framework (FPF) [Levenchuk, 2023a,b], prove that its aggregation semantics satisfy a quintet of invariants,
and present deployment evidence showing the practical consequences of ignoring temporal validity. A reference
implementation (anonymized for review) is an existence proof, not the contribution itself.

2     The First Principles Framework
This section presents FPF as a formal framework for epistemic accountability in AI-assisted engineering. We define its
core constructs, ground its aggregation in fuzzy logic, specify the invariants any valid aggregation must satisfy, and
compare it to existing approaches.

2.1   The F-G-R Trust Tuple

Every knowledge claim in FPF carries a three-dimensional trust descriptor:
Formality (F): How rigorously the claim is expressed, on a scale from F0 to F3.

                                 Table 1: Formality levels and their reliability ceilings.

                                  Level    Description    Example                     Cap
                                  F0       Informal       “Felt faster in staging”    70 %
                                  F1       Structured     ADR with trade-offs         85 %
                                  F2       Empirical      Load test: 12k RPS          95 %
                                  F3       Formal proof   TLA+, Z3                   100 %


                                                            2
                          Epistemic Status and Temporal Validity in AI-Assisted Engineering                 A P REPRINT




                                       F (Formality)

                                                            ca
                                                               ps
                                                                  c eil
                                                                       i   ng



      G (Scope)                                                                 R (Reliability)              Reff
                                  constrains transfer
                                         (CL penalty)
 Every knowledge claim carries
     all three dimensions.

Figure 1: The F-G-R trust tuple. Each knowledge claim in FPF carries three dimensions: Formality (F) determines the
rigor of expression, Scope (G) constrains evidence portability via congruence-level penalties, and Reliability (R) is the
computed effective trust score Reff . F caps the maximum achievable R; G penalizes cross-context transfer.


The ceiling matters most: no amount of evidence can push reliability above what the formality level permits. A decision
backed entirely by informal observations (F0) cannot exceed 70% reliability even if ten people agree. This prevents
informal consensus from masquerading as empirical certainty.
Scope (G): Where the claim applies, expressed as a hybrid path and tag set. Format: path [tag1, tag2]. Examples:
api/auth [production, critical], cache/redis [api/users], * (universal). Scope constrains evidence
transfer. A benchmark run on a developer laptop (scope: perf [dev, x86]) transfers poorly to production ARM
servers (scope: perf [prod, arm64]). FPF formalizes this through Congruence Levels (CL):

                            Table 2: Congruence levels for cross-context evidence transfer.

                                 CL      Context Match                                    Penalty
                                 CL3     Same context (internal test on target HW)         None
                                 CL2     Similar context (same arch, different scale)      10%
                                 CL1     Different context (external benchmark)            40%
                                 CL0     No context match (unrelated domain)               90%


The penalty is applied as subtraction with a zero floor: Radj = max(0, R(e) − penalty). For example, CL1 evidence
with R = 0.8 contributes max(0, 0.8 − 0.4) = 0.4 to Reff .
Reliability (R): Evidence strength on [0.0, 1.0], computed via aggregation (Section 2.3). R is never estimated
by humans; it is always calculated from evidence scores, formality ceilings, layer ceilings (L0 ≤ 35%, L1 ≤ 75%,
L2 ≤ 100%), and dependency structure. When both layer and formality ceilings apply, Reff is bounded by the minimum
of both: an F0 claim at L1 is capped at min(0.70, 0.75) = 0.70.

2.2   The Gamma Invariant Quintet

FPF’s min-based aggregation is governed by five invariants that ensure conservative, auditable epistemic status. These
invariants apply to serial dependency structures where argument chains must be evaluated as weakest-link systems:

      1. IDEM (Identity): Γ([x]) = x. A single piece of evidence speaks for itself.
      2. COMM (Commutativity): Γ([a, b]) = Γ([b, a]). Evidence order is irrelevant.
      3. LOC (Locality): Changing evidence E does not affect holons with no dependency on E.
      4. WLNK (Weakest Link Upper Bound): Γ(S) ≤ min(S). No aggregation may exceed the weakest link.
      5. MONO (Monotonicity): a ≤ a′ implies Γ([a, b]) ≤ Γ([a′ , b]). Improving evidence never worsens assurance.
Theorem 1 (Quintet Satisfaction). The Gödel t-norm Γ(S) = min(S) satisfies all five invariants.


                                                                3
                           Epistemic Status and Temporal Validity in AI-Assisted Engineering                          A P REPRINT



                          Table 3: Alternative aggregation functions and the Γ invariant quintet.
      Function             IDEM      COMM         LOC     WLNK        MONO      Notes
      min (Gödel)            ✓         ✓          ✓        ✓          ✓        Current FPF default
                                                                                Q
      Product (Lusser)        ✓         ✓          ✓         ∼         ✓           (0.9, 0.9) = 0.81 < min = 0.9. Satis-
                                                                                fies WLNK when all scores < 1.
      OWA [Yager, 1988]       ✓         ∼          ✓         ∼         ∼        Depends on weight vector. w = [0, . . . , 0, 1]
                                                                                recovers min.
      Dempster–Shafer        —          ✓          ✓        —          —        Handles conflict but can exceed min.


Proof. IDEM: min([x]) = x by definition of minimum over a singleton. COMM: min(a, b) = min(b, a) because
minimum is symmetric. LOC: min computes its result solely from its input set, with no external dependencies.
WLNK: min(S) ≤ min(S) trivially, so the weakest link bound is never exceeded. MONO: If a ≤ a′ , then
min(a, b) ≤ min(a′ , b) because the minimum function is monotonically non-decreasing in each argument.
Theorem 2 (Idempotent Uniqueness). The Gödel t-norm is the unique idempotent t-norm [Metcalfe, 2005].

Proof. Let ∗ be any idempotent t-norm. For x ≤ y: by idempotence x = x ∗ x; by monotonicity x ∗ x ≤ x ∗ y; by the
identity property x ∗ y ≤ x ∗ 1 = x. Thus x ∗ y = x = min(x, y).

This uniqueness matters for practice: if we require idempotent aggregation (applying the same evidence twice should
not change the result), then min is the only mathematically valid choice. Any alternative that satisfies idempotence
necessarily reduces to min.
The quintet is intentionally strict. Invariant 4 (WLNK upper bound) means that even alternative aggregation functions
(Product, OWA, Dempster–Shafer) must never exceed the weakest link. These invariants prevent trust inflation—the
failure mode where an agent hallucinates higher confidence by aggregating massive amounts of low-quality evidence.
Without this constraint, an LLM could generate ten vague observations and arithmetically combine them into apparent
certainty (the epistemic equivalent of printing money). Zhang et al. [2026] independently confirm this in agentic
systems: the lowest-confidence step in a reasoning trajectory predicts failure better than any global average. Without the
WLNK upper bound, three blog posts plus an LLM summary could arithmetically exceed one controlled experiment.
This is a design choice: we believe engineering assurance should be conservative, and any relaxation requires explicit
justification. Section 5.1 discusses when and how to relax this constraint.
An open research question: can we learn an optimal Γ from historical decision outcomes while satisfying the quintet?
This requires a benchmark dataset of architectural decisions with known outcomes (Section 5.1).

2.3    Min-Based Aggregation (WLNK): An Invariant-Compliant Default

FPF’s aggregation rule is conservative: assurance equals the weakest supporting evidence. When a decision depends on
multiple pieces of evidence, the effective reliability equals the weakest link:
                                                 Reff = min(evidence scores)                                                      (1)

More precisely, when ceilings and cross-context penalties are included:
                                                                                       
                              Reff = min min Radj (ei ), min Reff (dj ) − CLj , CL , CF                                           (2)
                                             i                j

where Radj (ei ) is the adjusted score for evidence i (including decay, Section 2.5), CLj is the congruence level penalty
for dependency j (Table 2), CL is the layer ceiling (L0: 0.35, L1: 0.75, L2: 1.0), and CF is the formality ceiling (F0:
0.70, F1: 0.85, F2: 0.95, F3: 1.0 per Table 1).
This is the Gödel t-norm from fuzzy logic [Hájek, 1998]:
                                                   TGödel (a, b) = min(a, b)                                                     (3)

The weakest link principle has been studied in formal argumentation [Chen et al., 2023] and critiqued for potential
over-conservatism [Hoepman, 2008]. The Gödel t-norm has four properties that make it correct for serial argument
chains:


                                                                  4
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                   A P REPRINT



      1. Commutativity: min(a, b) = min(b, a). The order of evidence does not matter.
      2. Associativity: min(a, min(b, c)) = min(min(a, b), c). Chaining is well-defined. (Note: associativity is a
         property of the specific min operator, not a required invariant for all valid aggregation functions—the Γ quintet
         permits future learned aggregators that satisfy WLNK without requiring associativity.)
      3. Monotonicity: a ≤ a′ implies min(a, b) ≤ min(a′ , b). Stronger evidence never hurts.
      4. Boundary: min(1, a) = a and min(0, a) = 0. Perfect evidence is transparent; disproof is absolute.

Connection to possibilistic logic. The weakest link principle has independent theoretical grounding in possibilistic
logic [Dubois and Prade, 2025], where it is known as weakest link resolution: “the strength of an inference chain is
that of the least certain formula involved in this chain.” Possibilistic logic propagates certainty qualitatively using
this law and remains inconsistency-tolerant by reasoning from the largest consistent subset of most certain formulas.
FPF’s WLNK bound is thus not an arbitrary design choice but a recognized principle in uncertainty reasoning with four
decades of theoretical development.
Why min, not mean? Consider a decision with three supporting pieces of evidence scored at 0.95, 0.90, and 0.30.
The mean is 0.72, suggesting reasonable confidence. But the 0.30 evidence is a blog post that contradicts published
benchmarks. The min (0.30) correctly flags this: the decision rests on a weak foundation. Averaging hides the weakness.
This matters especially for AI-assisted engineering. LLM coding assistants produce recommendations that lack
epistemic qualification, backed by training data of varying quality. Without conservative aggregation, a team can
accumulate a portfolio of “medium-confidence” claims that collectively appear strong while individually resting on
weak evidence. Min-based aggregation prevents this inflation.
Why min is the correct default for engineering argument chains. Engineering decisions typically form serial
dependency structures: choosing a framework constrains library choices, which constrain API design, which constrain
test strategy. Each step depends on prior ones. A concrete comparison illustrates the stakes. Suppose a Redis caching
decision rests on three premises: (1) a benchmark showing adequate throughput (R = 0.95, F2), (2) a traffic model
predicting peak load (R = 0.70, F1, based on a blog post extrapolation), and (3) vendor documentation on clustering
limits (R = 0.90, F1). Three aggregation strategies yield different results:

                            Table 4: Aggregation comparison for a Redis caching decision.

                                    Aggregation     Result       Interpretation
                                    Mean             0.85        Hides weak traffic model
                                    Product          0.60        Penalizes more evidence
                                    Min (WLNK)       0.70        Identifies what to fix


The mean (0.85) suggests the decision is solid. But if the traffic model is wrong—if peak load is 3× the blog post
estimate—the entire caching architecture fails regardless of how good the benchmark and documentation are. Min-based
aggregation surfaces this: the decision is exactly as reliable as its weakest premise. More importantly, min-based
aggregation provides actionable guidance: upgrading the traffic model from F1 (blog extrapolation) to F2 (load test on
production traffic) would raise Reff from 0.70 to min(0.95, 0.90) = 0.90. No other aggregation function makes this
remediation path as transparent.
When WLNK is correct and when it is not:

                               Table 5: Dependency structures and WLNK applicability.

                                Structure          Valid?    Reasoning
                                Serial (A ⇒          ✓       If any link breaks, the chain
                                B ⇒ C)                       breaks.
                                Logical chains       ✓       Counterexample      to    any
                                                             premise invalidates conclu-
                                                             sion.
                                Parallel redun-      —       Defense-in-depth: joint failure
                                dant                         < weakest.
                                Independent evi-     —       Bayesian: P (H | E1 , E2 ) >
                                dence                        max(P (H | Ei )).


                                                             5
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                   A P REPRINT



                                          Use Redis for session storage
                                              DRR Reff = 0.70




     E1: Benchmark                               E2: Traffic model                          E3: Redis clustering
   12k RPS at p95=8ms                             peak 10k RPS                                documentation
         R = 0.95, F2                            R = 0.70, F1 (weakest)                           R = 0.90, F1




                                       Reff = min(0.95, 0.70, 0.90) = 0.70

Figure 2: WLNK dependency graph (worked example). Green nodes have strong evidence; the red node (E2, F1-
level blog evidence) caps the entire decision at Reff = 0.70. Upgrading E2 to an F2 load test would raise Reff to
min(0.95, 0.90) = 0.90. Averaging would yield 0.85, masking the weak foundation.



FPF uses min-based aggregation as the default because most engineering argument chains are serial: “We chose Redis
(premise 1: benchmark shows it is fast enough) because (premise 2: our traffic model predicts 10k RPS) and (premise 3:
Redis clustering handles that load).” If any premise fails, the conclusion is unsound. Section 5.1 discusses extending
the framework to non-serial cases.


2.4   The ADI Reasoning Cycle

FPF organizes reasoning as a cycle of three inference modes, each producing claims at a higher epistemic layer. The
progression mirrors Kahneman’s System 1/System 2 distinction [Kahneman, 2011]: abduction is fast and intuitive
(System 1), while deduction and induction impose slow, deliberate verification (System 2). FPF makes this handoff
explicit and auditable:
Abduction (generate hypotheses, L0): Given an anomaly or design question, generate candidate explanations. These
are conjectures, plausible but unverified. Example: “Redis might be better than Memcached for our session store
because it supports persistence.”
Deduction (verify logic, L0→L1): Check logical consistency. Does the hypothesis contradict known constraints? Are
the premises well-formed? A hypothesis that passes deductive verification becomes L1 (substantiated). Example: “The
Redis-persistence argument is logically consistent: our SLA requires session recovery after crashes, and Redis AOF
provides that. Memcached does not.”
Induction (gather evidence, L1→L2): Collect empirical evidence. Run benchmarks, analyze logs, survey users. An
L1 claim that passes empirical validation becomes L2 (corroborated). Example: “Load test confirms Redis 6.2 handles
12k RPS at p95 = 8ms on our target hardware. The session-persistence hypothesis is empirically validated.”
After the ADI cycle, a finalized decision is recorded as a Design Rationale Record (DRR), an architectural decision
record augmented with evidence validity windows, dependency chains, and assurance scores.
The Transformer Mandate. We introduce this term for a structural constraint: the entity that finalizes a decision must
be external to the generation loop. An LLM may propose hypotheses and gather supporting evidence (Abduction and
Induction), but ratification requires an external verifier. Currently, this necessitates a human; in future multi-agent
systems, the role could theoretically be filled by an independent verifier agent with disjoint training data, provided it
satisfies FPF invariants, but the principle of separation of concerns remains absolute. This prevents a failure mode where
an autonomous agent bootstraps confidence in its own recommendations by citing its own prior outputs. The mandate is
architectural, not a policy preference. Enforcement mechanisms for this constraint remain an open research question


                                                            6
                             Epistemic Status and Temporal Validity in AI-Assisted Engineering                  A P REPRINT


                          logical consistency                       empirical                     decision
                                 check                              validation                  finalization
        Abduction                                  Deduction                     Induction                     DRR


            L0                                           L1                          L2
         conjecture                                 substantiated                corroborated


                  new anomaly / evidence decay trigger

Figure 3: The ADI reasoning cycle. Abduction generates conjectures (L0), Deduction verifies logical consistency (L1),
and Induction validates empirically (L2). Finalized decisions become Design Rationale Records (DRRs). Evidence
decay or new anomalies trigger re-entry into the cycle.


(Section 5). Ferrario et al. [2026] formalize this as computational reliabilism: the epistemic adequacy of AI-supported
processes depends on whether the process is reliable for the task, a judgment that requires external calibration.

2.5   Evidence Decay and Temporal Validity

Every piece of evidence in FPF carries a valid until timestamp. When evidence expires, the system generates
an alert. The team must then re-validate the evidence, waive the decay with documented rationale, or deprecate the
decision.
This addresses a failure mode specific to AI-assisted engineering: LLMs generate recommendations based on training
data with an implicit temporal scope. A recommendation to “use library X” reflects the state of X at training time, not
deployment time. Without temporal tracking, stale AI recommendations persist as if they were current.
Evidence decay is not a new idea; SRE practices [Beyer et al., 2016] recommend regular review of operational
assumptions. FPF makes it mechanical rather than aspirational: evidence either has a validity window or it does not
count toward assurance.
Formal definition. Given evidence e with reliability R(e) and validity window valid until(e), the time-dependent
effective reliability is:
                                                
                                                  R(e) if t ≤ valid until(e)
                                  Reff (e, t) =                                                              (4)
                                                  0.1   otherwise

This formalization has three properties: (1) uncertainty floor—expired evidence moves to 0.1 regardless of its original
score, representing epistemic uncertainty rather than low confidence. When evidence expires, its conclusions—
including negative conclusions—are no longer trusted. An expired falsification (R = 0.05) becomes “we no longer
know” (R = 0.1), not “the falsification is slightly more reliable.” This uniform uncertainty floor ensures expired
evidence is neither trusted nor distrusted, only marked as needing re-validation. This distinguishes epistemic decay
from simple TTL caching; (2) composability—stale evidence propagates via WLNK, so any decision depending on
expired evidence becomes unreliable; (3) actionability—the alert identifies exactly which evidence expired and which
decisions are affected, enabling targeted re-validation.

2.6   Comparison with Existing Approaches

2.7   Related Work

FPF connects several research threads.
Technical debt and architectural erosion. Cunningham [1992] coined the technical debt metaphor. Kruchten et al.
[2012] extended it to architectural technical debt, identifying “stale design decisions” as a primary contributor. FPF
operationalizes this insight: evidence decay tracking turns “stale decisions” from a metaphor into a measurable, alertable
condition.
Knowledge management in software engineering. Robillard et al. [2010] surveyed how development teams capture
and retrieve architectural knowledge, finding that most knowledge remains tacit or locked in outdated documents. FPF
addresses this by attaching machine-readable validity windows and dependency chains to decisions, making knowledge
staleness detectable rather than implicit.


                                                                    7
                             Epistemic Status and Temporal Validity in AI-Assisted Engineering                               A P REPRINT



                                                                                                      STALE alert
   Created                                                             Approaching                   Reff grayed out
 Reff = 0.90                                                            expiration


                                    Use Redis 6.2 for session storage


      Jul             Aug               Sep             Oct                 Nov            Dec                Jan
                                              2025                                                           2026


                                                                         Re-validate               Waive                    Deprecate

                                                                       re-run benchmark       document rationale      retire decision

Figure 4: Evidence decay lifecycle for a single decision. A Redis session storage decision is created in July 2025 with
Reff = 0.90. As the benchmark evidence approaches its validity window, the system transitions from green to amber.
Upon expiration in January 2026, a STALE alert triggers one of three resolution paths: re-validate, waive with rationale,
or deprecate.

                           Table 6: FPF compared with existing approaches across six dimensions.
        Dimension             FPF                Self-Consist.          Verifier Scor-    ADRs                Instr. Files
                                                 [Wang et al.,          ing [Lightman
                                                 2023]                  et al., 2024]
        Epistemic layers      Explicit           —                      —                 —                  —
                              (L0/L1/L2)
        Aggregation           min (WLNK)         Majority voting        Weighted scor-    N/A                 N/A
                              with    formal                            ing
                              guarantees
        Temporal validity     Decay     with     —                      —                 —                  —
                              timestamps
        Audit trail           Durable DRRs       Transient              Transient         Static snapshots    Static file
                              with     dep.
                              graphs
        Scope tracking        CL0/CL1/CL2/CL3—                          —                 —                  —
        Formal invariants     Γ        quintet   —                      —                 —                  —
                              (proven)



Engineering epistemology. Vincenti [1990] argued that engineering knowledge has distinct categories (fundamental
design concepts, practical considerations, quantitative data) that differ in how they are produced and validated. FPF’s
formality levels (F0–F3) echo this taxonomy, mapping informal observation through formal proof.
Uncertainty quantification in machine learning. The ML community has developed extensive methods for quantify-
ing uncertainty in model predictions: Monte Carlo dropout [Gal and Ghahramani, 2016], deep ensembles [Lakshmi-
narayanan et al., 2017], and conformal prediction [Angelopoulos and Bates, 2023]. These approaches address a different
level of abstraction than FPF. ML uncertainty quantification asks “how confident is the model in this prediction?” FPF
asks “how reliable is the architectural decision that deployed this model?” A neural network may output well-calibrated
confidence scores for individual inferences while the decision to deploy it rests on a stale benchmark, an untested scaling
assumption, and a blog post about GPU availability. FPF and ML UQ are complementary: model-level uncertainty is
one input to decision-level assurance, not a substitute for it.
LLM reliability and hallucination. Ji et al. [2023] survey hallucination in natural language generation. Huang
et al. [2024] catalog failure modes in LLM reasoning. These findings motivate FPF’s conservative aggregation: if
LLM-generated recommendations carry unknown error rates, min-based aggregation provides a worst-case bound rather
than a misleading average.


                                                                   8
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                   A P REPRINT



Possibilistic logic and uncertainty reasoning. Possibilistic logic [Dubois and Prade, 2025] provides the theoretical
foundation for FPF’s weakest link aggregation. Developed over four decades by Dubois and Prade, possibilistic logic
handles weighted classical formulas where inference follows the “weakest link resolution” rule: the certainty of a derived
conclusion equals the minimum certainty of the formulas in the derivation chain. This principle is mathematically
grounded in necessity measures and has been applied to default reasoning, belief revision, and argumentation. FPF’s
WLNK bound is a direct application of this principle to engineering decisions, where argument chains (requirements →
design → implementation) mirror possibilistic inference chains.
Decision tracking. Architectural Decision Records (ADRs) [Nygard, 2011] are the closest existing practice. Jansen
and Bosch [2005] proposed knowledge management frameworks for software architecture. Esposito et al. [2025] survey
47 academic studies on generative AI in software architecture, finding that 93% of surveyed papers report no validation
of LLM-generated architectural outputs. FPF extends ADRs with temporal validity, dependency-aware invalidation,
and computed assurance scores, directly addressing the validation gap these surveys identify.
Argumentation and provenance. Dung [1995] introduced abstract argumentation frameworks; Besnard and Hunter
[2008] extended them with structured premises. FPF shares the graph-of-claims structure but tracks reliability and
expiry rather than resolving defeat. Buneman et al. [2001] formalized data provenance; the W3C PROV model [Moreau
and Missier, 2013] standardized provenance interchange; Jøsang et al. [2007] survey trust propagation across networks.
FPF borrows traceability and compositional trust but adds formality, scope, and temporal validity, attributes absent from
provenance records and reputation scores.


3     Alternative Views

3.1   “This Is Over-Engineering”

The argument: most decisions do not need this rigor. Lightweight Architectural Decision Records (ADRs) [Nygard,
2011] are industry standard and sufficient. FPF adds bureaucracy for marginal benefit. Surveys of practitioners [Robillard
et al., 2010] consistently find that teams prefer lightweight documentation.
We partly agree. For trivial, easily reversible decisions (choosing a date-formatting library, naming a config variable),
FPF adds overhead without value. Skip it. But for decisions with long-term consequences—database selection,
authentication architecture, data model design—hidden assumptions compound over time. Our retrospective analysis
(Section 4) found that 20–25% of such decisions showed stale evidence within two months. ADRs document what was
decided but not when evidence expires or what conditions invalidate the decision. The real question is which decisions
warrant the cost of tracking epistemic status.

3.2   “ADRs Already Solve This”

The argument: ADRs [Nygard, 2011] are lightweight, widely adopted, and sufficient for decision tracking. Jansen and
Bosch [2005] showed that architectural knowledge management can be structured without heavyweight process.
ADRs are static snapshots. They record the decision and rationale at a point in time but provide no mechanism for
detecting when the rationale becomes invalid. They do not track evidence expiration (benchmark results going stale),
assumption drift (traffic growing 10×, hardware changing), or dependency chains (if claim X is invalidated, which
downstream decisions break?). A Google SRE study [Beyer et al., 2016] found that 60% of production outages trace
to stale assumptions about system behavior. FPF complements ADRs by adding what they lack: temporal validity
windows and dependency-aware invalidation.

3.3   “Epistemic Layers Are Philosophically Naive”

The argument: the L0/L1/L2 hierarchy assumes a positivist epistemology where claims progress linearly from conjecture
to verified truth. Kuhn [1962] showed that scientific knowledge does not accumulate linearly, and Feyerabend [1975]
argued against rigid methodological hierarchies. Real knowledge is messier: claims can be partially verified, contextually
true, or verified by one methodology and contradicted by another.
This is the strongest objection. FPF’s layers are indeed a simplification. An L2 claim (empirically validated) might be
validated by a load test that does not capture production traffic patterns. The “corroborated” label could create false
confidence. However, the alternative (treating all claims as equally uncertain) is worse in practice. Engineers already
make implicit epistemic distinctions (“I tested this” vs. “I think this should work”). FPF makes those distinctions
explicit and auditable. The layers are not claims about ultimate truth; they are claims about what verification has


                                                            9
                          Epistemic Status and Temporal Validity in AI-Assisted Engineering                    A P REPRINT



been performed. An L2 claim says “we ran a test and it passed,” not “this is certainly true.” The scope field (G) and
congruence levels (CL) provide the contextual qualification that pure positivism lacks.

3.4   “Formal Methods Are More Rigorous”

The argument: if you want rigor, use TLA+ [Lamport, 2002] for distributed protocol verification, Coq [The Coq
Development Team, 1989] for algorithm correctness, or Alloy [Jackson, 2012] for structural constraints. FPF’s formality
scale is a pale imitation.
Formal methods and FPF operate at different levels. TLA+ can verify that a consensus protocol satisfies safety and
liveness properties. It cannot answer “should we use Redis or Memcached given our traffic patterns, team expertise,
and operational constraints?” FPF handles the empirical, contextual, and trade-off dimensions where formal methods
do not apply. They complement each other: FPF’s formality field (F) includes formal verification as F3 evidence. A
decision backed by a TLA+ proof (F3), a Jepsen test (F2), and a blog post (F1) has Reff = min(1.0, 0.95, 0.7) = 0.7.
The weakest link is the blog post. The fix: replace it with a controlled experiment, not abandon the framework.

3.5   “WLNK Is Too Conservative”

The argument: min-based aggregation ignores the value of corroborating evidence. Bayesian epistemology [Bovens and
Hartmann, 2003] shows that independent confirming evidence should increase posterior probability. Three independent
studies each scoring 0.8 should yield more confidence than a single study scoring 0.8, but min-based aggregation treats
them identically.
Correct. This is a deliberate trade-off. For serial dependencies (argument chains, prerequisite relationships), min-based
aggregation is provably correct: a chain cannot be stronger than its weakest link. For parallel or independent evidence,
min-based aggregation is overly conservative. Section 5.1 addresses this directly: we propose extending FPF with
configurable aggregation that auto-detects dependency topology and selects the appropriate function while maintaining
the Γ invariant quintet. The current implementation uses min-based aggregation everywhere as a safe default. We prefer
false conservatism to false confidence.

4     Deployment Evidence
This section presents evidence that architectural decision staleness is a real and measurable problem, not a theoretical
concern. We performed a retrospective audit of two internal projects (anonymized) that used traditional ADRs without
temporal tracking. We analyzed git history and commit metadata from December 2025 to January 2026, applying FPF
staleness criteria to 62 architectural decisions to determine: (1) which decisions had stale evidence by FPF standards,
and (2) whether that staleness was discovered proactively or only reactively during incidents. The question is not
whether our prototype is optimal, but whether evidence staleness occurs at rates that warrant systematic tracking. Full
methodology and per-project breakdowns are in Appendix C.
Terminology: Evidence is stale when the current date exceeds its validity window, the timestamp by which supporting
data should be re-verified. For example, a load test result with a 60-day validity window becomes stale after 60 days,
regardless of whether the underlying decision remains correct.
AI amplification. AI-assisted engineering amplifies the staleness problem in three ways. First, LLMs generate decisions
faster than teams can validate them, increasing the rate at which potentially stale recommendations enter codebases.
Second, AI recommendations carry implicit temporal scope from training data: a suggestion to “use library X” reflects
the state of X at training time, not deployment time. Third, AI-generated code lacks the institutional memory that
would flag dormant assumptions; an LLM cannot know that a caching decision from six months ago rested on traffic
assumptions that have since doubled. These factors make mechanical validity tracking necessary.

4.1   Evidence Decay in Practice

The 20–25% staleness rate is the central finding: nearly one in four architectural decisions had evidence that expired
within two months, regardless of the tracking mechanism used. In projects without temporal tracking, these stale
assumptions were discovered reactively (during incidents or refactoring), suggesting that the problem persists silently
until it causes failures.
Scope note: This audit focused on temporal validity, which is directly measurable from timestamps and validity windows,
an O(n) scan over n decisions. Systematic measurement of formality inflation requires classifying each decision’s
epistemic status (O(n × k) where k is classification effort), and detecting citation circularity requires tracing dependency


                                                            10
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                   A P REPRINT


                   Table 7: Evidence decay metrics (retrospective audit of two projects, 2 months).

                                   Metric                                          Value
                                   Total decisions audited                      62 ADRs
                                   Stale evidence detected                    14 (∼23%)
                                   Discovered reactively (during incidents)    12 (19%)
                                   Never discovered (dormant until audit)        2 (3%)
                                   Average evidence validity window              53 days
                                   Avg. time to debug stale decision           4.2 hours


graphs (O(n × m) where m is average citation depth). These higher-cost measurements require instrumentation not
present in these projects and remain future work.
The cumulative staleness curve (Appendix, Figure 6) shows the temporal distribution: short-validity evidence (30-day
data-quality checks) decays earliest, creating an early-warning signal.

4.2   Proactive vs. Reactive Discovery

                            Table 8: Staleness discovery: traditional ADRs vs. FPF criteria.

                              Discovery Mode                              Count    % of Stale
                              Reactive (during incidents/refactoring)         12        86%
                              Never discovered (dormant until audit)           2        14%
                              Would be proactive with FPF decay alerts        14       100%

The key finding: of the 14 decisions with stale evidence, 12 were discovered only when they caused problems, during
incident investigation or refactoring. Two remained dormant, their staleness undetected until our retrospective audit.
With FPF’s decay tracking, all 14 would have triggered proactive alerts before causing incidents. The average time to
understand a stale decision during reactive discovery was 4.2 hours. We estimate that FPF’s structured DRRs could
reduce this substantially by preserving decision context and evidence provenance, though this claim requires prospective
validation.

4.3   External Evidence: The Cost of Stale Assumptions

Our internal audit shows staleness rates; external incidents show what staleness costs. The 2012 Knight Capital failure
provides a case study. On August 1, 2012, Knight Capital lost $440 million in 45 minutes when a deployment error
activated dormant code from 2003. The “Power Peg” market-making algorithm had been unused for nine years, but its
code remained in the system. A new deployment repurposed a flag that the dormant code still monitored, causing the
system to execute trades at unfavorable prices.
The root cause was not the deployment error itself but the absence of validity tracking for the decision to retain dormant
code. No record existed documenting why Power Peg remained in the codebase, under what conditions it should be
reviewed, or what the RNDP flag controlled. Nine years of implicit “this code is safe to ignore” accumulated without
review. This incident illustrates the type of temporal validity gap that FPF is designed to address: a decision to retain
dormant code persisted without review for nine years. While we cannot claim FPF would have prevented this specific
failure, the pattern—decisions made years earlier causing failures when conditions change—matches FPF’s target
failure mode.
This pattern—decisions made years earlier causing failures when conditions change—is not unique to Knight Capital.
Ernst et al. [2015] surveyed 1,831 practitioners across three organizations and found that “architectural choices are
the greatest source of technical debt” and that “architectural issues are difficult to deal with, since they were often
caused many years previously.” The temporal distance between decision and consequence makes architectural staleness
particularly insidious: by the time the failure occurs, the original rationale is lost.

4.4   Methodological Scope

This study’s scope constrains the strength of its conclusions. First, the authors built the framework and applied it
retrospectively to their own projects, a self-study design that risks confirmation bias in how evidence was categorized


                                                             11
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                  A P REPRINT



and validity windows were assigned. Second, staleness rates are sensitive to validity window calibration: shorter
windows mechanically produce higher staleness percentages, and we lack ground truth on when decisions actually
became invalid versus when their evidence formally expired. Third, the “would have been caught proactively” claim is
counterfactual; we cannot directly observe what FPF would have done, only simulate it. These findings demonstrate
that evidence staleness is a real and measurable problem in engineering practice, not that FPF is the optimal solution.
Stronger evidence would require prospective deployment across multiple teams with randomized assignment and
calibration of validity windows against actual decision invalidity events.

4.5   Property-Based Verification

Property-based testing [Claessen and Hughes, 2000] approximates universal quantification over input spaces by
generating diverse, randomly sampled test cases. Where exhaustive verification is infeasible, PBT provides probabilistic
confidence that a property holds by exercising it against thousands of automatically generated inputs, including edge
cases that manual test authoring typically misses.
Five key Reff properties verified via property-based testing (10,000 iterations each): bounds [0, 1], WLNK enforcement
(Reff ≤ min(evidence)), formality ceiling, layer ceiling, and monotonicity. These properties test the practical
correctness of the assurance calculator, complementing the theoretical Gamma quintet (Section 2.2). All passed. Fuzz
testing (50,000 iterations) found zero panics on IEEE 754 edge cases (NaN, Inf, subnormal floats). Full results in
Appendix C.

5     Research Directions
5.1   Optimizing Aggregation Function Selection

The First Principles Framework, through the Gamma invariant quintet, provides a principled basis for selecting
aggregation functions appropriate to specific dependency topologies, as outlined in Section 2.2. While min-based
aggregation is the provably conservative default for serial chains, the framework is designed to accommodate alternative
functions for non-serial evidence where Invariant 4 (the weakest link upper bound) may be appropriately relaxed while
preserving Invariants 1–3 and 5. The research direction lies not in whether the framework can support these alternatives,
but in how to optimally select and learn aggregation functions under various conditions.
Candidate aggregation functions for non-serial cases:

                            Table 9: Candidate aggregation functions by dependency type.

                                 Dependency             Aggregation     Use Case
                                 Serial (A → B → C)     min (WLNK)      Argument chains
                                 Parallel (indep.)      Product         Indep. evidence
                                 Redundant (2-of-3)     OWA             Defense-in-depth
                                 Voting (multi-agent)   Self-consist.   Multi-LLM

Evaluation: inter-rater reliability (automatic topology detection vs. expert judgment, Cohen’s κ), A/B testing (adaptive
aggregation vs. pure min-based aggregation on decision outcome quality), and formal verification that the learned Γ
satisfies all five invariants.

5.2   Federated Evidence Sharing

Organizations repeatedly test identical hypotheses. (“Has anyone benchmarked Postgres 16 on ARM64?”) A federated
registry where projects share benchmarks with reproducibility metadata could reduce duplicated effort. Trust transfers
through congruence levels: CL3 (same org, same infra), CL2 (similar context), CL1 (public benchmark). Open
problems include reproducibility verification, privacy (differential privacy on benchmark results), and adversarial
evidence (gaming assurance scores).

5.3   SMT-Based Claim Validation

Quantitative claims (“API handles 1000 RPS with p95 < 100 ms at < 80% CPU”) can be expressed as SMT constraints
and checked mechanically. A SAT result constitutes F3 (formal) evidence. An UNSAT result identifies logical
inconsistency. Research question: which engineering claims are SMT-verifiable, and which require empirical testing?


                                                           12
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                 A P REPRINT



6   Call to Action
For ML researchers: Design learnable aggregation operators satisfying the Γ quintet that outperform WLNK on
non-serial evidence. This requires benchmarks of decisions with ground-truth outcomes, and crucially, benchmarks that
penalize epistemic drift, where models are evaluated not only on answer quality but on whether they detect when their
own evidence has gone stale. Study adversarial robustness of assurance scores and integration of epistemic tracking
with LLM reasoning chains.
For practitioners: Add valid until timestamps to consequential ADRs and measure how often evidence expires
unnoticed. Integrate decay checks into CI/CD so benchmarks auto-refresh on dependency updates. We invite teams
to apply these criteria to their existing ADR repositories and report staleness rates; independent replication would
strengthen or challenge our 20–25% finding.
For tool builders: Surface decision lineage and evidence freshness in IDEs and CI/CD pipelines. Build epistemic
tracking that composes with LLM assistants through open protocols (e.g., MCP) so evidence freshness travels with
AI-generated recommendations.
The absence of epistemic accountability benchmarks is itself a research gap. Current LLM evaluations measure output
quality but not whether the model knows when its knowledge is stale or its confidence is inflated. We call for benchmark
suites that test temporal awareness, evidence staleness detection, and resistance to trust inflation.

7   Conclusion
AI-assisted software engineering generates decisions faster than organizations can validate them. We have argued for
three properties that any responsible AI-assisted engineering workflow should implement: explicit epistemic layers that
distinguish conjecture from verified knowledge, conservative assurance aggregation grounded in the Gödel t-norm, and
temporal accountability through evidence decay tracking.
We formalized these properties as the First Principles Framework, proved that its aggregation satisfies a quintet of
invariants, and presented deployment evidence: 23% of architectural decisions had stale evidence within two
months, with 86% of that staleness discovered only during incidents. With FPF’s decay tracking, all would have been
flagged proactively.
The gap between AI-generated recommendations and validated engineering decisions will widen as LLM capabilities
increase. Epistemic accountability infrastructure is coming either way; the community can build it deliberately or
discover the need through production failures.

References
Karan Singhal, Shekoofeh Azizi, Tao Tu, S. Sara Mahdavi, Jason Wei, Hyung Won Chung, Nathan Scales, Ajay
  Tanwani, Heather Cole-Lewis, Stephen Pfohl, Perry Payne, Martin Seneviratne, Paul Gamble, Chris Kelly, Abubakr
  Abdelrahman, Nathanael Schärli, Aakanksha Chowdhery, Philip Mansfield, Dina Demner-Fushman, Blaise Agüera
  y Arcas, Dale Webster, Greg S. Corrado, Yossi Matias, Katherine Chou, Juraj Gottweis, Nenad Tomasev, Yun Liu,
  Alvin Rajkomar, Joelle Barral, Christopher Semturs, Alan Karthikesalingam, and Vivek Natarajan. Large language
  models encode clinical knowledge. Nature, 620:172–180, 2023. doi: 10.1038/s41586-023-06291-2.
Daniil A. Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. Autonomous chemical research with large language
  models. Nature, 624:570–578, 2023. doi: 10.1038/s41586-023-06792-0.
Matteo Esposito, Xiaozhou Li, Sergio Moreschini, Noman Ahmad, Tomas Cerny, Karthik Vaidhyanathan, Valentina
 Lenarduzzi, and Davide Taibi. Generative AI for software architecture: Applications, challenges, and future directions.
 arXiv preprint arXiv:2503.13310, 2025. URL https://arxiv.org/abs/2503.13310.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models. In Proceedings of the 11th International
  Conference on Learning Representations (ICLR), 2023. URL https://arxiv.org/abs/2203.11171.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman,
  Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In Proceedings of the 12th International Conference on
  Learning Representations (ICLR), 2024. URL https://arxiv.org/abs/2305.20050.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny
  Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Advances in Neural Information
  Processing Systems 35 (NeurIPS), 2022. URL https://arxiv.org/abs/2201.11903.


                                                          13
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                  A P REPRINT



Anatoly Levenchuk. Toward an ontology for third generation systems thinking. arXiv preprint arXiv:2310.11524,
  2023a. URL https://arxiv.org/abs/2310.11524.
Anatoly Levenchuk. First principle framework, 2023b. URL https://github.com/ailev/FPF. GitHub repository.
George Metcalfe. Fundamentals of fuzzy logics. In Lecture Notes, Tbilisi Summer School on Language, Logic and
  Computation, 2005. URL https://www.logic.at/tbilisi05/Metcalfe-notes.pdf. Proves that the Gödel
  t-norm (minimum) is the unique idempotent t-norm.
Jiaxin Zhang, Caiming Xiong, and Chien-Sheng Wu. Agentic confidence calibration. arXiv preprint arXiv:2601.15778,
   2026. URL https://arxiv.org/abs/2601.15778.
Ronald R. Yager. On ordered weighted averaging aggregation operators in multicriteria decision making. IEEE
  Transactions on Systems, Man, and Cybernetics, 18(1):183–190, 1988. doi: 10.1109/21.87068.
Petr Hájek. Metamathematics of Fuzzy Logic, volume 4 of Trends in Logic. Kluwer Academic Publishers, 1998. ISBN
  978-1-4020-0370-7. doi: 10.1007/978-94-011-5300-3.
Chen Chen, Pere Pardo, Leon van der Torre, and Liuwen Yu. Weakest link in formal argumentation: Lookahead and
  principle-based analysis. In Computational Logic in Argumentation and Reasoning (CLAR 2023). Springer, 2023.
  doi: 10.1007/978-3-031-40875-5 5.
Jaap-Henk Hoepman. The weakest link fallacy. Technical report, Radboud University, 2008. URL https://www.cs.
  ru.nl/~jhh/publications/weakest-link-fallacy.html. Technical Report, accessed 2026.
Didier Dubois and Henri Prade. 40 years of research in possibilistic logic – a survey. In Proceedings of the Thirty-Fourth
  International Joint Conference on Artificial Intelligence (IJCAI-25), pages 10427–10435, 2025. doi: 10.24963/ijcai.
  2025/1158. Survey Track. Establishes “weakest link resolution” as fundamental principle of possibilistic inference.
Daniel Kahneman. Thinking, Fast and Slow. Farrar, Straus and Giroux, 2011. ISBN 978-0374275631.
Andrea Ferrario, Alessandro Facchini, and Juan M. Durán. Epistemology gives a future to complementarity in human-AI
  interactions. arXiv preprint arXiv:2601.09871, 2026. URL https://arxiv.org/abs/2601.09871.
Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy. Site Reliability Engineering: How Google Runs
  Production Systems. O’Reilly Media, 2016. ISBN 978-1491929124. URL https://sre.google/sre-book/.
Ward Cunningham. The WyCash portfolio management system. In OOPSLA ’92 Experience Report, Addendum to the
 Proceedings. ACM, 1992. doi: 10.1145/157709.157715.
Philippe Kruchten, Robert L. Nord, and Ipek Ozkaya. Technical debt: From metaphor to theory and practice. IEEE
  Software, 29(6):18–21, 2012. doi: 10.1109/MS.2012.167.
Martin P. Robillard, Robert J. Walker, and Thomas Zimmermann. Recommendation systems for software engineering.
 IEEE Software, 27(4):80–86, 2010. doi: 10.1109/MS.2009.161.
Walter G. Vincenti. What Engineers Know and How They Know It: Analytical Studies from Aeronautical History. Johns
 Hopkins University Press, 1990. ISBN 978-0801845888.
Yarin Gal and Zoubin Ghahramani. Dropout as a Bayesian approximation: Representing model uncertainty in deep
  learning. In Proceedings of the 33rd International Conference on Machine Learning (ICML), PMLR 48, pages
  1050–1059, 2016. URL https://arxiv.org/abs/1506.02142.
Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty
  estimation using deep ensembles. In Advances in Neural Information Processing Systems 30 (NeurIPS), 2017. URL
  https://arxiv.org/abs/1612.01474.
Anastasios N. Angelopoulos and Stephen Bates. Conformal prediction: A gentle introduction. Foundations and Trends
  in Machine Learning, 16(4):494–591, 2023. doi: 10.1561/2200000101. URL https://arxiv.org/abs/2107.
  07511.
Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and
  Pascale Fung. Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12):1–38, 2023.
  doi: 10.1145/3571730.
Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng,
  Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles, taxonomy,
  challenges, and open questions. arXiv preprint arXiv:2311.05232, 2024. URL https://arxiv.org/abs/2311.
  05232.
Michael Nygard. Documenting architecture decisions. Cognitect Blog, November 2011. URL https://cognitect.
 com/blog/2011/11/15/documenting-architecture-decisions.


                                                           14
                        Epistemic Status and Temporal Validity in AI-Assisted Engineering                A P REPRINT



Anton Jansen and Jan Bosch. Software architecture as a set of architectural design decisions. In 5th Working IEEE/IFIP
  Conference on Software Architecture (WICSA 2005), pages 109–120, 2005. doi: 10.1109/WICSA.2005.61.
Phan Minh Dung. On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic
  programming and n-person games. Artificial Intelligence, 77(2):321–357, 1995. doi: 10.1016/0004-3702(94)
  00041-X.
Philippe Besnard and Anthony Hunter. Elements of Argumentation. MIT Press, 2008. ISBN 978-0262026437.
Peter Buneman, Sanjeev Khanna, and Wang-Chiew Tan. Why and where: A characterization of data provenance.
  Lecture Notes in Computer Science, 1973:316–330, 2001. doi: 10.1007/3-540-44503-X 20. Proceedings of ICDT
  2001.
Luc Moreau and Paolo Missier. PROV-DM: The PROV data model. Recommendation, World Wide Web Consortium
  (W3C), 2013. URL https://www.w3.org/TR/prov-dm/.
Audun Jøsang, Roslan Ismail, and Colin Boyd. A survey of trust and reputation systems for online service provision.
  Decision Support Systems, 43(2):618–644, 2007. doi: 10.1016/j.dss.2005.05.019.
Thomas S. Kuhn. The Structure of Scientific Revolutions. University of Chicago Press, 1962. ISBN 978-0226458120.
  4th edition 2012.
Paul Feyerabend. Against Method: Outline of an Anarchistic Theory of Knowledge. New Left Books, London, 1975.
  ISBN 978-0860916468. 4th edition, Verso, 2010.
Leslie Lamport. Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers. Addison-
  Wesley, 2002. ISBN 978-0321143068. URL https://lamport.azurewebsites.net/tla/tla.html.
The Coq Development Team. The Coq proof assistant, 1989. URL https://coq.inria.fr/. First released
  1989. See also: Coquand, T. and Huet, G. (1988). The Calculus of Constructions. Information and Computation,
  76(2–3):95–120.
Daniel Jackson. Software Abstractions: Logic, Language, and Analysis. MIT Press, revised edition, 2012. ISBN
  978-0262017152. URL https://alloytools.org/.
Luc Bovens and Stephan Hartmann. Bayesian Epistemology. Oxford University Press, 2003. ISBN 978-0199269754.
  doi: 10.1093/0199269750.001.0001.
Neil A. Ernst, Stephany Bellomo, Ipek Ozkaya, Robert L. Nord, and Ian Gorton. Measure it? manage it? ignore it?
  software practitioners and technical debt. In Proceedings of the 10th Joint Meeting on Foundations of Software
  Engineering (ESEC/FSE 2015), pages 50–60. ACM, 2015. doi: 10.1145/2786805.2786848.
Koen Claessen and John Hughes. QuickCheck: A lightweight tool for random testing of Haskell programs. In
  Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP ’00), pages
  268–279. ACM, 2000. doi: 10.1145/351240.351266.


A     Glossary

B     Implementation Architecture
The reference implementation is an MCP server with SQLite persistence and ACID transactions.
Database schema: holons (knowledge units), evidence (with valid until timestamps), relations (serial/parallel
dependencies), characteristics (quantitative properties), waivers (documented risk acceptances).
Core modules:

       • Assurance calculator: WLNK implementation with F-G-R propagation.
       • ADI cycle orchestration: propose, verify, validate, decide.
       • Evidence decay: staleness detection and alerts.

C     Full Deployment Results
C.1   Property-Based Test Results

Configuration: time-based seed, parallelized execution.


                                                          15
                         Epistemic Status and Temporal Validity in AI-Assisted Engineering                A P REPRINT



                                   Term     Definition
                                   L0       Conjecture—unverified hypothesis
                                   L1       Substantiated—logically verified claim
                                   L2       Corroborated—empirically validated claim
                                   WLNK     Weakest Link—min-based reliability aggrega-
                                            tion
                                   F-G-R    Formality–Scope–Reliability trust tuple
                                   DRR      Design Rationale Record—decision artifact
                                            with validity windows
                                   MCP      Model Context Protocol—stdio-based AI tool
                                            integration
                                   ADI      Abduction–Deduction–Induction reasoning cy-
                                            cle
                                   Γ        Universal aggregation operator (FPF spec)
                                   OWA      Ordered Weighted Averaging [Yager, 1988]
                                   CL       Congruence Level—evidence transfer penalty
                                            across contexts
                                   ADR      Architectural Decision Record [Nygard, 2011]

                            Table 10: Property-based test results (10,000 iterations each).

                              Property     Invariant                       Iter.   Status
                              P1           0 ≤ Reff ≤ 1 for all holons      10k    ✓ PASS
                              P2           Reff ≤ min(evidence)             10k    ✓ PASS
                              P3           Reff ≤ ceiling(F )               10k    ✓ PASS
                              P4           Reff ≤ ceiling(layer)            10k    ✓ PASS
                              P5           Adding evidence ̸⇒ lower Reff    10k    ✓ PASS



Fuzz testing: 50,000 iterations, zero panics on NaN, Inf, subnormal floats, −0.0, values outside [0, 1], floating-point
rounding.

C.2   Per-Project Breakdown

Of the 14 stale decisions identified, 12 (86%) were discovered reactively during incidents or refactoring. Two (14%)
remained dormant; their staleness undetected until our retrospective audit applied FPF criteria.

C.3   Evidence Decay Examples

Example 1: Infrastructure (expiry).

Decision: "Use Redis 6.2 for sessions"
Evidence: Benchmark vs Memcached 1.6
  (valid_until: 2026-01-15)
Status: EXPIRED (2026-01-22)

Alert: "Evidence expired. Actions:
  1. Re-run benchmark on Redis 7.2
  2. Waive until Q2 2026
  3. Deprecate decision"

Action: Waived until 2026-03-01
  Rationale: "Redis 7.2 upgrade Feb.
  Re-benchmark post-migration."

Example 2: LLM suggestion (formality).

Decision: "Use FastJSON for serialize"
  Origin: LLM (Formality: F0)


                                                           16
                                                     Epistemic Status and Temporal Validity in AI-Assisted Engineering                                 A P REPRINT



                                       Table 11: Per-project audit results (FPF criteria applied retrospectively to traditional ADRs).
                                   Project    Type                 Team     ADRs        Stale (%)            Evidence Type              Assigned Validity
                                   A          Web app              1 dev    32            7 (22%)      Load tests, API compat.          60 days
                                   B          Microservices        2 devs   30            7 (23%)      Benchmarks, integration          45 days
                                   Total                                    62          14 (23%)

                                                                       Staleness Discovery Mode (n=14 stale decisions)

                                                                                                                                    14
  Number of stale decisions




                              14
                                                              12
                              12
                              10
                               8
                               6
                               4
                                                                                                   2
                               2
                               0
                                                                Reactive                      Dormant                      With FPF
                                                                                 Without FPF: 86% reactive, 14% dormant
                                                               (incidents)                  (undetected)                  (proactive)

Figure 5: Staleness discovery modes (retrospective analysis of 62 ADRs). Of the 14 decisions with stale evidence,
12 were discovered reactively during incidents or refactoring; 2 remained dormant until our audit. With FPF decay
tracking, all 14 would have triggered proactive alerts.


Evidence: "Copilot recommended" (L0)
  + 3 Stack Overflow mentions (L0)
Status: BLOCKED - cannot reach L1

Alert: "Only L0 evidence. Needs
  benchmark or test for L1."

Action: Ran benchmark
  Result: FastJSON 40% slower.
  Deprecated, reverted to stdlib.

Example 3: ML model (staleness).

Decision: "Deploy GPT-4-turbo"
Evidence: SWE-bench (2024-06)
  (valid_until: 2025-01-01)
Status: EXPIRED (2025-01-15)

Alert: "Benchmark predates update.
  GPT-4-turbo changed 2024-11."

Action: Re-ran on SWE-bench-Live
  Result: +12% better. Confirmed.
  Evidence refreshed.

Example 4: API contract (scope).

Decision: "Payment API: idempotent"
Evidence: Stripe docs v2023-10
  Scope: [stripe-api, v2023-10]
Status: STALE - scope mismatch



                                                                                             17
                                                        Epistemic Status and Temporal Validity in AI-Assisted Engineering                                   A P REPRINT



 % decisions with expired evidence                                                          Retrospective Analysis

                                                Project A                                                                       60-day evidence
                                     30%        Project B                                                                       begins expiring
                                     25%        Combined avg.                                                                                     ∼23%

                                     20%                               45-day evidence
                                                                       begins expiring
                                     15%
                                     10%
                                     5%
                                     0%




                                                                                                              29




                                                                                                                                                       19
                                                  1




                                                                   8




                                                                                   5




                                                                                             22




                                                                                                                            5




                                                                                                                                           12
                                                                                   1
                                                ec




                                                                ec




                                                                                                                            n
                                                                                                          ec




                                                                                                                                                       n
                                                                                ec




                                                                                            ec




                                                                                                                         Ja




                                                                                                                                           n
                                               D




                                                                D




                                                                                                                                                    Ja
                                                                                                                                         Ja
                                                                                                         D
                                                                               D




                                                                                           D
                                                                                                       Week

Figure 6: Cumulative evidence staleness over two months (retrospective audit). Applying FPF decay criteria to git
history of two internal projects that used traditional ADRs, evidence with shorter validity windows (45 days in Project B)
begins decaying earlier. Both projects converge to ∼23% stale by mid-January 2026. Without temporal tracking, 86%
of this staleness was discovered only during incidents.


Alert: "Scope [v2023-10] doesn’t
  cover [v2024-08]. API changed?"

Action: Verified v2024-08 docs.
  Still supported. Scope updated.

C.4                                  Scalability Benchmark Details

Test methodology: synthetic knowledge graphs at varying sizes. Evidence distribution: Poisson(λ = 5) per holon.
Dependency structure: 40% serial chains, 40% parallel, 20% isolated.

                                                                Table 12: Scalability benchmarks for the Reff calculator.

                                                                Holons        Evidence     Time (ms)     Mem. (MB)         µs/holon
                                                                        10            50           12              2.1           1 200
                                                                        50           250           45              6.3             900
                                                                       100           500           85              8.4             850
                                                                       500         2 500          210               28             420
                                                                 1 000             5 000           340              47             340
                                                                 5 000            25 000         1 850             180             370
                                                                10 000            50 000         4 100             320             410

Scaling: O(n) time in dependency depth, O(n + m) memory where m ≈ 5n.




                                                                                                  18
