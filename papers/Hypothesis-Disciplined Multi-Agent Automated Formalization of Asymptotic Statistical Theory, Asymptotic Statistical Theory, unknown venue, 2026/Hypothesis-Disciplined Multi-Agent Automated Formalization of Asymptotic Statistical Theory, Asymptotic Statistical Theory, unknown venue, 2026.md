                                            Hypothesis-Disciplined Multi-Agent Automated Formalization of
                                                            Asymptotic Statistical Theory
                                                            Tingzhou Wei1 , Zeyu Zheng2 , Ethan X. Fang1 , Junwei Lu3∗
                                                                1
                                                               Department of Biostatistics & Bioinformatics, Duke University
                                                            2
                                                             Department of Mathematical Sciences, Carnegie Mellon University
                                                         3
                                                           Department of Biostatistics, Harvard T.H. Chan School of Public Health
arXiv:2606.20642v1 [cs.AI] 3 Jun 2026




                                                                                           Abstract
                                                  Asymptotic statistical theory is a challenging domain for AI-assisted formalization: its cen-
                                              tral results mix convergence statements, asymptotic expansions, functional analysis, and reg-
                                              ularity conditions that have a large gap from existing infrastructure in Lean 4 formalization.
                                              To address these challenges, we propose a hypothesis-disciplined Lean 4 formalization pipeline
                                              built from multiple agents: a manager that coordinates seven specialist roles for proof plan-
                                              ning, skeleton scaffolding, Mathlib reconnaissance, proof construction, integration, independent
                                              review, and audit. The main methodological discipline is the hypothesis-disciplined audit, im-
                                              plemented by the Auditor agent: every main-theorem hypothesis and concept-layer field must
                                              be anchored in the source mathematical prose, justified as a Lean encoding adapter, marked
                                              as source-implied, or rejected as an unsupported strengthening. Using this workflow, we build
                                              a systematic formalization of asymptotic statistical theory, especially the parametric and semi-
                                              parametric models’ asymptotic distribution and eﬀiciency results. The resulting Lean develop-
                                              ment is axiom-clean and source-faithful, with Lean-checked and human-audited proofs of core
                                              parametric and semi-parametric theorems organized so that theorem-agnostic infrastructure and
                                              statistical concept definitions are separated from theorem-specific assembly. The formalization
                                              results are available in the following GitHub repository.
                                                   a GitHub: https://github.com/junwei-lu/Lean-Asymptotic-Statistical-Theory


                                        1    Introduction
                                        Asymptotic statistical theory provides the mathematical language for large-sample inference: local
                                        experiments, likelihood expansions, contiguity, weak limits of estimators, eﬀiciency bounds, and
                                        minimax risk comparisons [30, 31, 16, 12]. Formalizing this theory is therefore not just a matter of
                                        proving a handful of named theorems; it requires a reusable library of probability infrastructure and
                                        statistical concepts such as parametric and semi-parametric models, differentiability in quadratic
                                        mean, score functions, Fisher information, kernels, and loss functionals. Yet this part of statistics
                                        has remained largely absent from machine-checked mathematics. Lean 4 and Mathlib [22, 28]
                                        provide substantial measure-theoretic foundations and classical limit theorems, and recent work
                                        has pushed agentic formalization at both the textbook-chapter scale [7] and the level of research-
                                        grade individual theorems [6], as well as Lean-side statistical learning theory [36]. To our knowledge,
                                           ∗
                                             Lu is partially supported by NSF Artificial Intelligence, Formal Methods, and Mathematical Reasoning (AIMing)
                                        program DMS-2434664. Fang is partially supported by NSF grants DMS-2346292 and DMS-2434666.


                                                                                                1
there is no existing automatic formalization pipeline for asymptotic statistical theory, especially the
parametric and semi-parametric models’ statistical eﬀiciency.
    There are several potential risks in the formalization of the asymptotic statistical theory. Prior
work formalizing non-asymptotic statistical learning theory [36] observes in its Lean formaliza-
tion that statistical proofs written in natural language often leave measurability and topological
assumptions implicit and blur almost-sure versus pointwise statements. Asymptotic statistical for-
malization inherits this ambiguity, and several of its structural features (e.g., ambiguity in asymp-
totic arguments, the regularity condition complexity, and the functional space issues) sharpen it
further. In an agentic formalization pipeline, this ambiguity turns into a concrete failure mode.
When an agent encounters a missing proof obligation it cannot discharge, it can quietly absorb
the obligation as an extra hypothesis on the main theorem’s signature or as an extra field on a
concept-layer definition. The resulting Lean formalization may still compile and be sorry-free. We
call the signature-level version of this hypothesis laundering and the concept-level version definition
drift. The latter is the former relocated to a definition: the missing proof obligation is hidden as
a concept-layer field or helper definition rather than as a theorem hypothesis. We highlight four
examples in the asymptotic statistical formalization below:
• Natural-language imprecision at the formal boundary. Source prose underspecifies
  choices Lean must commit to. “The integral on the left” may be pointwise, almost-sure, in-
  probability, or Lp ; “a measurable function” may or may not require L2 -membership of its squares.
  Each such phrase resolves to several distinct typed propositions and the agent must pick one.
• Long Mathlib dependency chains amplify drift. Statistical concepts stack deeply. For ex-
  ample, differentiability in quadratic mean sits on measurability, Lp -membership, and σ-finiteness,
  each stacking further down. A single drifted field several layers up silently propagates to every
  downstream consumer.
• Lean constructions without source anchor. Some constructions have no source-text syn-
  tactic counterpart at all: the asymptotic representation theorem requires realizing the limit
  law as the Gaussian-shift limit experiment composed with a Markov kernel; the prose gives
  only a randomized-statistic (T (X, U )) form, so the kernel object itself has nothing to transcribe
  directly.
• Multi-source variation. The standard sources [30, 31, 16, 12] each give the regularity con-
  dition with slightly different content, so a laundered hypothesis often reads to a reviewer as
  some other source’s regularity: cross-wave drift across variants stays invisible without explicit
  version-tracking.
    Our multi-agent formalization framework aims to make the source mathematical prose the audit
authority inside the multi-agent loop. We therefore develop an agent Auditor for both locations
of the same drift pattern, which maintains a structured book-reference document for each audited
theorem boundary: every main-theorem hypothesis, instance constraint, and concept-layer defi-
nition field is paired with a row classification, a verbatim source excerpt, and a citation to the
original section and page in the chosen source (van der Vaart’s Asymptotic Statistics [30] in our
case). We use hypothesis-disciplined in this broad boundary sense: the audited obligations include
theorem hypotheses, instance constraints, and definition fields. This row-level artifact is not an
after-the-fact checklist. Immediately after the agent Scaffolder fixes the opening skeleton, the agent
Auditor checks that the main signature has source-backed rows; at each wave checkpoint, after the
agent Integrator proposes a trunk state, it revisits both new rows and historical rows affected by
any changed signature or audited definition; when an agent Executor reports a genuine gap, the
agent Auditor first classifies the proposed missing assumption before the agent Manager dispatches


                                                  2
the next agent Planner or agent Executor task. The result is a hypothesis-disciplined workflow
in which laundering is made visible at the theorem boundary where it is introduced, and unsup-
ported strengthenings are removed, justified as Lean encoding adapters, or escalated before they
can propagate downstream.
    On top of this discipline we develop a systematic Lean 4 formalization of central results in
asymptotic statistical theory. The development covers parametric and semi-parametric models,
with an emphasis on asymptotic distributions, lower-bound phenomena, and eﬀiciency results for
statistical procedures. Its library is organized into reusable theorem-agnostic infrastructure, sta-
tistical concept definitions, and theorem-specific assemblies, so that later formalization work in
asymptotic statistics can reuse both the mathematical components and the proof-engineering pat-
tern. At the same time, the hypothesis-disciplined audit is text-agnostic by construction: it requires
only a chosen source text, row-level evidence, and explicit classifications of formal obligations. The
methodology therefore applies beyond the present case study to other source-faithful formalization
projects in deep mathematical domains where important assumptions are implicit, layered, or easy
to strengthen inadvertently.

1.1   Our Contributions
A Lean 4 library of asymptotic statistical theory. The library contains a shared stratum
of Mathlib-side theorem-agnostic bricks and a statistical concept stratum consisting of asymptotic-
statistics definitions together with reusable derived properties of those definitions. We present five
cornerstone theorems on both the parametric and semi-parametric sides; these serve as named entry
points for downstream formalization and are not meant to delimit the library’s reusable surface.
A multi-agent automated formalization pipeline for thin-Mathlib-coverage infrastruc-
ture. Our second contribution is an execution scaffold for domains where the formal library is
too thin for a single proof-search loop to be the right unit of work. The architecture organizes
the orchestration loop: one user-facing agent Manager assigns scoped tasks to specialist agents,
isolates their work in separate git worktrees, and admits progress only through reviewed checkpoint
merges on a buildable trunk. This design turns large formalization into a sequence of auditable
engineering transactions: reconnaissance can precede proof construction, independent review can
gate completed changes, and reusable infrastructure can be promoted out of theorem-specific files
as it is discovered. Our pipeline then provides a division of labor tailored to thin-Mathlib-coverage
formalization, where library search, proof decomposition, cross-worktree deduplication, and shared-
infrastructure growth must be managed together.
An auditor to discipline against agent-side drift. We introduce a dedicated agent Audi-
tor that makes source-faithfulness a runtime obligation rather than a post-hoc judgment. The
Auditor attaches source evidence to each theorem boundary and audited definition boundary, so
that a successful Lean build is not accepted unless its assumptions are also justified by the chosen
mathematical source or by an explicit Lean encoding need. It is invoked exactly where agent-side
drift tends to enter: after the initial scaffold fixes a theorem statement, at wave checkpoints that
change audited boundaries, and when a proof obstruction pressures the system to add a stronger
assumption. Unsupported assumptions are therefore routed back to planning, repaired in the proof
strategy, or explicitly escalated rather than silently absorbed into the formal statement.
    The rest of the paper is organized as follows. Section 2 describes the agent architecture and the
source-reference discipline. Section 3 presents the Lean library and the five highlighted cornerstones.
Appendix A reports the scale and axiom certificates and summarizes the hypothesis-audit outcomes,
and Appendix B stress-tests the audit discipline through two drift case studies. Section 4 concludes


                                                  3
the paper and discusses the future work.

1.2   Related Work
Multi-agent Lean formalization. There are several existing works on the multi-agent Lean
formalization, such as Gloeckle et al. [7], who formalize an algebraic combinatorics textbook with
thousands of agents collaborating on a shared code base via version control; Archon [6], which
orchestrates Claude Code via a dispatcher targeting research-level individual theorems; and Zhang
et al. [36], who formalize non-asymptotic statistical learning theory under supervised Claude Code
use. Our problem differs from each along the same axis: prior systems emphasize scale, throughput,
and proof closure; this work adds a hypothesis-lineage audit, pairing mechanical change-detection
with a semantic faithfulness judgment, for source-faithful textbook formalization in a thin-coverage,
assumption-heavy domain. We further use a multi-tool Mathlib retrieval layer (type-by-name
lookup, type-shape search, and natural-language search) to match a higher-coverage setting. There
are also other recent works in this space: [20] is a general agentic reasoning system for formal
mathematics, while [8] and [13] focus on human-collaborative formalization of specific theorems
rather than a systematic area of mathematical theory.
Statement faithfulness and autoformalization drift. A parallel line studies a structurally
different audit problem: the gap between proof validity and translation faithfulness when a large
language model (LLM) produces a candidate Lean statement from natural language. Kim et al. [14]
document formalization gaming; Li et al. [18] score candidate formalization by symbolic equiva-
lence and back-translation similarity; Meadows et al. [21] characterize semantic drift in physics
auto-formalization. Each operates at the natural-language and Lean statement boundary on an
LLM-generated candidate. Our novelty is a hypothesis-disciplined audit for source faithfulness dur-
ing collaborative theory development: every theorem-boundary assumption and audited definition
boundary is tied to source evidence, a Lean encoding need, or an explicit drift finding. Faithfulness
is therefore enforced as the formal library evolves, rather than approximated by back-translation,
an LLM judge, or symbolic-equivalence scoring of a single candidate. A separate ecosystem of
benchmark datasets, tactic models, and proof-search agents [33, 32, 5, 4, 24, 35, 15, 25, 19, 26, 34]
typically evaluates proof search on single problems drawn from benchmarks. These systems oper-
ate on isolated theorems with pre-supplied Mathlib-native formal statements and do not address
source-fidelity at theory-development scale.
Formalized probability and statistics. In Lean, Sonoda et al. [27] formalized Rademacher
complexity generalization bounds, followed by broader non-asymptotic statistical learning theory
in [36]. Besides using Lean, there are other works formalizing probability and statistics in other
interactive theorem provers. For example, in Rocq [29], Infotheo [2] formalized discrete probability
and information theory and Affeldt et al. [1] for non-asymptotic concentration (Markov, Chebyshev,
and Chernoff inequalities, culminating in a Bernoulli-sampling bound). In the HOL4 theorem
prover, some probability theory topics are formalized [9, 10]. Using Isabelle/HOL [23], the central
limit theorem is formalized in [3], and the Lévy–Prokhorov metric and Prokhorov’s theorem are
formalized in [11].


2     Multi-Agent Architecture
This section describes the multi-agent architecture used to turn source-faithfulness from a post hoc
review concern into a runtime discipline. The system combines a fixed agent roster, an orchestration
loop, and role-specific contracts for decomposing, executing, reviewing, merging, and auditing proof

                                                 4
       1 Opening
                        Manager                           Planner                         Scaffolder                      Auditor
                       invokes Planner                 DAG & outline                     build skeleton              maintain reference



                                                                                 reads
       2 Body                                                       Scout                           Math
                                                                         reads                     Library
                           risk tasks                                                                                         Blocked
                                                                   Shared Brick
                        return gap report                                                                                      Triage
                                                              read by any Executor as needed

                            ＞— Executor N             ＞— Executor N                ＞— Executor N             ...    ＞— Executor N

       Manager
                                 Reviewer N                                              Reviewer N          ...          Reviewer N
       dispatches                                         Reviewer N
          wave
                    large gap
                                re-plan
                                                          Auditor      main-sig or audited
                    Planner
                                                           check         def changed
                                                                                                             Integrator

            repeat until all open sub-lemmas are closed


                                                                                                                       Theorem
       3 Closure                               Manager                               Auditor
                                                                                                                     formalization
                                            invokes Auditor                          final audit                       complete


Figure 1: Multi-agent architecture and runtime flow: a theorem’s movement through the Opening,
Body, and Closure phases, with the Body expanded into one parallel execution wave dispatched by
the Manager across the specialist roles.


work. This design responds to the two failure modes: hypothesis laundering at the main-theorem
signature and definition drift at the concept layer. They share the same source: definition drift is
a proof obligation relocated from the theorem signature into a project-authored concept definition,
and is therefore governed by the same hypothesis discipline. Figure 1 summarizes the architecture
and the multi-agent orchestration flow.
    The architecture of our formalization framework has one user-facing parent agent and seven
specialist agents that work through task cards, isolated git worktrees, and disk-backed artifacts.
We first introduce the agents as follows.
• Manager: It orchestrates the theorem workflow, dispatches all specialist agents, and decides the
  next step from their returned artifacts.
• Auditor: It maintains book-reference rows for theorem boundaries and project-level definitions,
  and checks that signature or definition changes remain anchored in the source.
• Planner: It converts the source proof into an executable sub-lemma plan and revises that plan
  when a route fails or needs finer decomposition.
• Scaffolder: It emits the initial build-clean skeleton with sorry-stubbed bodies, thereby locking
  the sub-lemma signatures for later proof work.
• Scout: It performs bounded Mathlib reconnaissance for risky sub-lemmas, records whether the
  needed bricks are present, composable, or absent, and truth-verifies suspect blocked goals.


                                                                     5
State       Source           Actions
Self-reported state on return
DONE        Executor       Enters the review gate; the Reviewer returns one of the three verdicts below
PARTIAL     Executor/Scout Carries named residual sorries and enters the review gate
BLOCKED     Executor/Scout No candidate changes; does not gate the checkpoint. Triaged by cause: a
                           missing or suspect assumption goes to the Auditor; a doubted goal is
                           truth-verified by a Scout, with counter-examples sent to the Planner
CLASSIFIED Scout           Folds gap report into the revised plan
Reviewer verdict on a candidate return
GREEN      Reviewer       Mergeable: captured build green, body-only differences, baseline axioms
                          only, no style or naming blocker
YELLOW     Reviewer       Approach is sound but the proof is not yet fully closed: small residual
                          sorries return to the same Executor as a continuation, large ones to the
                         Planner for re-decomposition
RED        Reviewer       Narrowing is redone by a fresh Executor against the locked signature; a dead
                          route goes to the Planner for re-decomposition (rare safety net)

Table 1: Agent return states and the Manager’s routing. The returning agent self-identifies its
state; a DONE or PARTIAL candidate additionally receives a Reviewer verdict.

• Executor: It closes one assigned sub-lemma in an isolated worktree and returns a terminal state
  (see Table 1) with any candidate changes.
• Reviewer: It gates each Executor return by checking the candidate change set, build evidence,
  axioms usage output, and code quality before assigning a verdict.
• Integrator: It folds accepted worktrees onto the trunk at wave checkpoints, rebuilds from scratch,
  deduplicates cross-worktree differences, and promotes reusable sub-lemmas into the shared li-
  brary (Section 3).
    The detailed contracts for the four methodologically load-bearing roles (Planner, Scout, Re-
viewer, and Auditor) appear in Section 2.2.

2.1     Orchestration and Workflow
A theorem target enters the system with its source material; at opening time, the Manager dis-
patches the Planner, and the theorem leaves as a build-clean Lean theorem. Figure 1 breaks this
movement into three lifecycle phases: opening, where the Planner turns the source proof into an
executable sub-lemma plan; body, where the planned sub-lemmas are closed; and closure, where
the remaining proof debt and book-reference audit are both discharged. The body phase advances
by execution waves. In one wave, the Manager dispatches a batch of Executors in parallel; each
Executor closes one sub-lemma in its own worktree; a Reviewer gates each candidate return on the
captured build and axioms usage result; and the Integrator folds the accepted worktrees into one
merge commit at the wave checkpoint, building the merged result from scratch. Green in isolation
does not imply green after merge, since cross-worktree symbol collisions, signature drift, and the
Integrator’s own deduplication and library promotion produce an artifact no Reviewer has built.
The trunk remains buildable at each checkpoint.
Opening. At opening time, the Manager dispatches the Planner on the theorem target and
source proof. The Planner drafts the informal attack route—prose, an initial sub-lemma table,
and a chosen decomposition—and converts it into an executable plan: a sub-lemma DAG with a


                                                  6
                                            Blocked Triage
                                      Manager routes
                                        by cause

                                                      false / dead      counter
                            missing /
                                                          route         example
                             suspect
                           assumption                                             Planner
                                                        Scout
                                                       truth verify               new route
                            Auditor
                            check         refute           confirm


                                           Planner                           Planner
                                          new route                          finer DAG



                                                      ＞— Executor
                                                            new trial



Figure 2: Triage of a blocked Executor return: a missing or suspect assumption routes to the
Auditor’s drift control, while a doubted sub-lemma is truth-verified by a Scout.


per-row proof outline tying each formal sub-lemma to the corresponding source-proof step. The
Scaffolder then commits a single build-clean skeleton in which every sub-lemma body is sorry,
locking signatures for Executor body-filling. The Auditor performs its first book-reference pass on
this skeleton: it maintains the per-theorem reference rows for the main-theorem signature and flags
any assumption without a source anchor.
Body. Waves run consecutively, each chosen from the open sorries in the current scaffold. In the
baseline path, the Manager selects a batch of sub-lemmas, optionally sends the risky ones flagged
by the Planner to a Scout for Mathlib reconnaissance, and dispatches one Executor per sub-lemma.
When an Executor returns a candidate that the Reviewer marks GREEN, it is accepted, and at the
wave checkpoint the Integrator folds the wave’s accepted worktrees into one merge commit on the
trunk; whenever that checkpoint changes the main-theorem signature or an audited definition, the
Auditor runs its standing book-reference pass. Two local failures can pull a sub-lemma off this path:
the Executor cannot produce a candidate, or the Reviewer rejects the one it produced. Both route
any source-fidelity question to the Auditor, the project’s main safeguard against drift. In rare cases
a strategic re-plan resets the route altogether.
• Executor block. An Executor that cannot produce a candidate at all returns BLOCKED with a diag-
nosis and evidence; Figure 2 summarizes how the Manager then routes the blocked sub-lemma by
cause. It carries no candidate changes, so it bypasses the Reviewer and does not block the check-
point: the Integrator still folds the wave’s other accepted worktrees, while the Manager triages the
blocked sub-lemma for reassignment or replanning. A missing or suspect assumption, a hypothesis
the proof needs but the signature lacks, goes to the Auditor’s drift control. When the Executor
instead doubts the sub-lemma itself (it may be false, or the route may not reach it), a Scout truth-
verifies the goal: a refutation, or a counter-example the Executor already holds, returns it to the
Planner for a new route, while a confirmation hands a fresh Executor the supporting brick, or,
when the confirmed goal still needs breaking down, prompts the Planner to re-decompose it into a
finer DAG.


                                                       7
• Reviewer rejection. After review, a candidate return (DONE or PARTIAL) that is not GREEN receives
one of two non-merging verdicts. YELLOW means that the route is sound but named residual sorries
remain; this is the normal verdict for a PARTIAL return unless review finds a narrowing or dead
route. Small residuals then return to the same Executor, large ones go to the Planner for re-
decomposition, and the closed part still merges. RED marks a candidate that proves a narrower
or different statement than the locked signature, or whose route is dead; the Reviewer contract
(Section 2.2.4) specifies how each is routed.
• Strategic re-plan. Occasionally local repairs can no longer preserve the chosen route. In that case
a strategic re-plan, authorized by the user, makes a wholesale change of proof strategy. Triggered
by a falsification, a scope correction, or accumulated drift findings, it resets the sub-lemma DAG
and emits a fresh Scaffolder skeleton, and unlike the within-strategy repairs above it crosses back
to the user.
    Planner reruns can interleave with new wave dispatches rather than blocking them, so a re-
decomposition for one sub-lemma proceeds while others advance. These repairs all stay within the
body phase of an already-open theorem, in contrast to the strategic re-plan above.
Closure. Closure is the state in which the sorry count on the main theorem’s transitive closure
reaches zero, and the Auditor’s standing seven-check passes (Section 2.2.1); the same audit that
accompanies wave-boundary merges certifies closure when the last sorry disappears. The loop pro-
vides three structural guarantees: accepted work reaches the trunk only at wave checkpoints, where
it stays buildable; the merged trunk is rebuilt from scratch by the Integrator at each checkpoint,
while the Reviewer confirms every candidate’s axioms usage output against the accepted baseline;
and every committed change to a main-theorem signature or audited definition is checked against
the Auditor’s reference rows.

2.2     Agent Contracts
The four agents whose contracts carry the load on the methodological discipline are spelled out
in turn. The remaining roles (Scaffolder, Executor, Integrator, Manager) operate by the lifecycle
described in Section 2.1 and need no contract beyond their inventory entry.

2.2.1    Auditor Agent

The Auditor maintains the book-reference rows for main-theorem hypotheses, instance constraints,
and project-level definitions. For each audited Lean entry point it records the row classification,
source citation, and evidence, then checks whether each audited entry has been strengthened beyond
its source anchor. Its output is the row-level finding used by the Manager at wave boundaries.
Figure 3 summarizes this source-anchor classification, in which each audited row is either accepted
(directly, or by user consent when the source anchor is not clear) or removed as drift.
    The canonical audit, fired every time the main-theorem signature or an audited definition
changes, is seven checks. Each check separates a mechanical detection step, which surfaces that
something changed, from a semantic judgment step, in which the Auditor agent decides whether
the surfaced change is faithful to the source, removing an unanchored assumption by default and
reaching the user only when evidence shows it is genuinely needed. Two checks are fully mechanical
(1–2); four pair mechanical change-detection with a per-item semantic faithfulness judgment (3–6);
one is a global semantic spot check (7). The mechanical detection under checks 3–6 is a comparison
against the committed signature-pinning snapshot (Appendix C.2), which surfaces any change to
a hypothesis, the conclusion, an instance binder, or an authored definition body. See Table 2 for


                                                 8
                                        Auditor Workflow

                              Audited                    Classify
                             Boundary                   Each Item             pass &
                                                                             proceed
                    main theorem hypothesis
                    audited definition
                                                  high-confidence
                                                                         user consent
                    instance constraint
                    conclusion                                            Clear
                                                  lean-artifact
                                                                         Evidence

                           Match Source                                    default
                             Anchors              implied

                   verbatim quote + page                                     remove
                                                  potential-drift              drift
                   compare each item



Figure 3: The Hypothesis-Disciplined Auditor’s source-anchor classification: each audited main-
theorem hypothesis, instance constraint, and definition field is tied to a book-reference row, classi-
fied by its source anchor, and either accepted (directly or by user consent) or removed as drift.

      #   Check                                              Kind                    Trigger
      1   no stray sorry                                     mechanical              per build
      2   axioms usage clean                                 mechanical              per build
      3   each main-sig hypothesis matches a reference row   semantic, per-item      main-sig change
      4   conclusion equivalent to source                    semantic, per-item      main-sig change
      5   each instance constraint matches a row             semantic, per-item      main-sig change
      6   structure fields, def edges classified             semantic, per-def       def change
      7   main assumptions jointly satisfiable               semantic, global        hyp. revision

Table 2: Seven checks performed by the hypothesis-disciplined audit, including explicit accounting
for instance constraints. Mechanical checks are decided by tooling; semantic checks are the Auditor
agent’s source-faithfulness calls.

details.
    At a wave checkpoint, the Manager schedules this pass after the Integrator has produced a
candidate trunk state whose audited boundary changed: a new or rewritten main-theorem signature,
or a modified project-authored definition on the audited dependency path. The pass revisits both
rows introduced by the current wave and historical rows that may have gone stale after a refactor.
The audit tool below supplies the mechanical side of these checks.
Lifecycle role. The Auditor is invoked at the points where the theorem boundary can drift.
Immediately after the Scaffolder commits the opening skeleton, it runs the book-reference pass: it
creates or updates the reference rows for the main-theorem signature, checks that every row has
a verbatim quote and page citation, and pushes the Planner to eliminate any potential-drift
assumption carried over from the informal outline. At wave checkpoints it performs the pass
described above. When a BLOCKED report raises a missing or suspect assumption, it routes through


                                                  9
the Auditor first, which classifies the assumption before the Manager chooses the next Planner or
Executor dispatch.
Hypothesis taxonomy. Every signature argument lands in one of four tiers; the book-reference
row records the tier.
• high-confidence: appears verbatim in the book (header or proof body). Row must cite the
  book’s chapter, page, and verbatim quote.
• lean-artifact: encoding adapter required by Lean / Mathlib API (typeclass instance, joint-
  measurability witness, L2 -membership for Bochner integrability, support bookkeeping for change-
  of-measure, and similar). Each row must cite a concrete encoding correspondence (e.g. “the
  Kernel.compProd construction requires joint measurability of (θ, x) 7→ pθ (x)”); the phrase “im-
  plicit in book” is forbidden as the sole justification.
• implied: the book sentence implies the hypothesis without stating it (e.g. “has covariance
  matrix” semantically presupposes a finite second moment). Auto-accepted on a citation to the
  implying sentence.
• potential-drift: no book anchor. The Manager first treats the row as a route error and asks
  the Planner or Executor to remove the assumption or repair the statement. If a counter-example,
  or a sustained proof obstruction diagnosed by the agents, indicates that the assumption is needed
  for the proposed theorem, the row escalates to the user; accepted rows stay potential-drift
  with the evidence recorded and explicit sign-off.
Definition discipline. The same machinery applies to project-authored structure and def decla-
rations on the audited dependency path. A definition-side row is judged by the same source-anchor
test as a signature row: the field or definition edge must appear in the source definition, be implied
by it, or be justified as a Lean encoding adapter. This is not a parallel discipline: it is the place
where a hypothesis-like obligation can be relocated into a definition. If it has no such anchor, it is
definition-side potential-drift. The typical drift pattern is relocation: an extra condition used
by a proof route is encoded as a structure field or a project-authored helper def. The Auditor
records such rows in the same book-reference document and classifies them by the source anchor
that justifies the field or definition.
Audit tool. A lightweight audit-tool suite complements the Auditor’s per-item semantic checks.
Its passes mirror the mechanical side of the seven-check audit: a build-hygiene pass counts stray
sorry occurrences and reports their transitive taint; a signature-pinning pass compares the audited
theorem’s fully elaborated signature, together with the bodies of the authored definitions it depends
on, against a committed snapshot, so any change to a hypothesis, an instance argument, the conclu-
sion, or a definition body is surfaced (Appendix C.2); and a declaration-inventory pass enumerates
project-authored structures, defs, and related declarations in the audited scope. Against the
book-reference document, the tool runs a coverage check on the signature’s hypotheses: it flags any
hypothesis with no matching row, any stale row, the forbidden “implicit” / “by analogy” / “book
is informal” defenses on high-confidence rows, and any potential-drift row still present among
the theorem’s formal assumptions. This matches hypothesis names against the document’s rows,
not against [30]. A potential-drift row accepted by the user remains in the reference document
with its evidence and sign-off, so later audits can distinguish it from unresolved drift. The Auditor
agent makes the source-faithfulness, row classification, and joint-consistency judgments, reading
the candidate items and reproducible checks that the tool produces to reach its verdict. In our
development this resolved most discrepancies at the agent level, without escalation to the user.




                                                 10
2.2.2   Planner Agent

The Planner owns proof planning. At opening time, it reads the theorem target and source proof,
drafts the attack route, and turns that route into a sub-lemma DAG with a per-row proof outline.
When the source proof invokes a supporting result or proof device, the Planner records it either as
an available brick or as a local derivation target on the DAG.
    The same role handles planning repairs once the body phase is under way. A YELLOW verdict with
large residual sorries, or a BLOCKED goal that a Scout verifies as true but reachable only through a
finer breakdown, asks the Planner to refine the remaining lemma into a finer DAG while preserving
the existing GREEN sub-lemmas. A RED verdict, or a BLOCKED route falsified by a counter-example
or a Scout’s truth-verification, asks it instead to abandon the current route and draft a new one.

2.2.3   Scout Agent

A Scout is a bounded reconnaissance probe: given one sub-lemma the Planner has flagged as risky,
it spends a fixed time budget checking what Mathlib actually supplies, and returns a gap report
with cited evidence. The role exists because thin-coverage domains make coverage uncertainty
load-bearing: whether the bricks a sub-lemma needs are present, composable from existing pieces,
or absent entirely.
    During BLOCKED triage, a Scout also truth-verifies a suspect goal under the locked signature: it
either confirms the goal and names the supporting brick or reports a refutation or counter-example
that sends the route back to the Planner.
Risk classification. The Planner marks a sub-lemma risky when its closure depends on Mathlib
API of uncertain existence or shape: results named in the source proof (central limit theorems,
Prokhorov, Le Cam lemmas) whose informal name may not correspond to a discoverable Mathlib
declaration, theorem-sized targets that are unlikely to be packaged under one declaration, and
steps where the right brick exists but its hypotheses may not match the sub-lemma’s assumptions.
Sub-lemmas with no such dependency skip reconnaissance and go straight to an Executor.
Gap report. A Scout’s success state is CLASSIFIED: for each expected brick it records whether
the target is directly supported (the same objects, operation, and conclusion already in Mathlib),
composable (the ingredients exist and the remaining gap is routine adapter work), or not found (no
declaration and no suﬀicient ingredients), with the evidence cited. The report also flags adapter
gaps (a brick whose hypotheses need bridging), critiques the scaffold’s locked signature when it
does not express the intended mathematics, estimates the cost to close, and names fragments that
should be promoted to the shared library.
    When a gap is caught before Executor work begins, the CLASSIFIED report can redirect the
Planner; the same gap found inside an Executor attempt usually forces a downstream re-plan.
The report is recorded for reuse by later Scouts and Executors, but route selection stays with the
Planner.

2.2.4   Reviewer Agent

The Reviewer gates each candidate return (DONE or PARTIAL) and issues the verdict that routes it.
Its work is to compare the candidate change set against the locked scaffold, review the code for style,
and write a pull request-style change summary. The change set is what certifies that the proof closes
the assigned statement rather than a weaker one: the Scaffolder’s skeleton pins each sub-lemma
signature, a well-formed candidate changes only the body, and a body-only change that typechecks


                                                  11
proves exactly the locked statement, since Lean admits no narrower proof against a fixed signature
and fixed referenced definitions. Any narrowing therefore shows up in the change set as an edited
signature line, or—when relocated into a project-authored definition the signature references—as
an edited audited definition (the definition-drift channel of Section 2.2.1). The candidate’s axioms
usage output surfaces any residual sorry or non-baseline axiom. The verdict is one of three:
• GREEN means the change is mergeable: the captured lake build is green, the change touches
  only bodies, axioms usage on the target contains only the baseline axioms, and the code review
  finds no style or naming blocker.
• YELLOW means the approach is sound but the proof is not yet closed: named residual sorries
  remain, so small residuals return to the same Executor for continuation and larger ones go to
  the Planner for re-decomposition. A PARTIAL return lands here by construction.
• RED means the candidate proves a narrower or different statement than the locked signature,
  or that its route is dead. The Manager either reassigns the work to a fresh Executor against
  the still-standing signature or sends it to the Planner for re-decomposition, escalating to a
  strategic re-plan when local repair no longer preserves the route. RED is a rare safety net for
  a confident-but-wrong submission: most route failures surface upstream as BLOCKED, and the
  locked-signature discipline pre-empts most narrowing. It did fire in our development, catching
  a sub-lemma whose signature had drifted from its locked form.
    The book-reference row check is conditional. Ordinary sub-lemma body changes do not consult
the book-reference document; when a candidate changes the main-theorem signature or an audited
definition, the Reviewer compares only the changed main-signature hypotheses, definition fields,
and definition edges against the per-theorem book-reference document (Section 2.2.1), and a main-
signature hypothesis or definition-side field lacking a matching row blocks the merge until the
Auditor creates or updates the corresponding row.


3     Formalization Results for Asymptotic Statistical Theory
In this section, we use five cornerstone theorems and several core definitions from the resulting
Lean library to make the formalization artifact concrete. These examples show how asymptotic
statistics theory is represented in Lean through reusable statistical concept definitions and theorem-
level Lean signatures. They also identify recurring formalization challenges: implicit source-proof
assumptions, Lean representation choices, proof-body hypotheses promoted to typed inputs, and
potential drift between the source argument and the formal statement. Throughout this section we
follow van der Vaart’s Asymptotic Statistics [30] as the source text for the theorems and definitions
we formalize.

3.1   The Statistical Concept Layer
Before turning to individual cornerstones, we describe the reusable library objects that those corner-
stones share. Mathlib4 supplies measure theory and the classical CLT but not the parametric-family
machinery for asymptotic estimation, so the released library separates the reusable material by im-
port direction. The shared-library stratum contains theorem-agnostic analytic, measure-theoretic,
and probability infrastructure absent from current Mathlib. The statistical concept layer builds
on this infrastructure to define the asymptotic-statistics objects whose fields encode model, estima-
tor, and tangent-space definitions. The separation follows the Lean dependency role rather than
whether a predicate appears in a theorem statement. The cornerstone demonstrations then instan-


                                                 12
 Local Asymptotic         Asymptotic              Hájek-Le Cam                                                 Variance bound
    Normality            Representation            Convolution                                                   Σ ≽ 𝑃𝜓%! 𝜓%!"

                                                                              Semi-parametric
                                                                                Convolution
                                                                                                                Convolution
                                     Local Asymptotic                                                          decomposition
                                        Minimax
                                                                                                               L = N(0, G) ⋆ M




                          Score function &
  Parametric family                               Differentiable in                                                  Efficient influence
                               Fisher                                  Regular estimator        Tangent cone
     & density                                    quadratic mean                                                       function (EIF)
                            information




                                                                  Anderson’s
        Le Cam I & III     Bowl-shaped       Gaussian-shift                       Markov-kernel     Portmanteau         Sigmoid
                                                                    lemma
          contiguity          Loss            Experiment                           Prokhorov        (LSC bridge)       Submodel
                                                               Prékopa–Leindler


                                  Mathlib4 base: MeasureTheory, Probability, LinearAlgebra, Analysis


Figure 4: Dependency graph of the five cornerstone theorems with approximate per-cornerstone
line counts. The upper-left blue panel groups the four parametric cornerstones; the upper-right
rose panel shows the semi-parametric cornerstones. The middle band lists statistical concept-layer
definitions, the lower green band lists reusable shared-library bricks, and the gray baseline records
the Mathlib4 dependencies.


tiate these reusable components in five released entry-point theorem files, while the library also
contains many supporting theorems and reusable intermediate results.
    Figure 4 shows the reusable objects that enter the cornerstone signatures, split by this de-
pendency direction into concept-layer definitions and shared-library bricks. We expand the three
concept-layer definitions that most directly explain the surfaced assumptions below: Differentiable
Quadratic Mean, regular estimator sequence, and tangent set with its generated tangent space.
• Differentiability in quadratic mean.                            We use the quadratic-mean differentiability condition
of Chapter 7, Eq. (7.1) of [30].

 Definition 3.1. A model with densities pθ is differentiable in quadratic mean at θ if there exists
 a measurable score vector ℓθ such that
         ∫ (√             √                      √      )2
               pθ+h (x) − pθ (x) − 12 hh, ℓθ (x)i pθ (x) dµ(x) = o(khk2 )      (h → 0).

    Lean represents the chosen score vector as an explicit parameter ℓ of the structure. The structure
then has two fields: isLittleO records the displayed rate statement, and mem records that the
residual is eventually an L2 (µ) function.
 structure DifferentiableQuadraticMean
     (M : ParametricFamily 𝓧 Θ) (μ : Measure 𝓧) (θ : Θ)
     (ℓ : 𝓧 → Θ) : Prop where
   mem : ∀ᶠ h in 𝓝 (0 : Θ),
     MemLp (fun x => M.sqrtDensity (θ + h) x - M.sqrtDensity θ x




                                                                      13
                     - (1/2 : ℝ) * ⟪h, ℓ x⟫ * M.sqrtDensity θ x) 2 μ
   isLittleO :
     (fun h : Θ =>
       ∫ x, (M.sqrtDensity (θ + h) x
             - M.sqrtDensity θ x
             - (1/2 : ℝ) * ⟪h, ℓ x⟫ * M.sqrtDensity θ x) ^ 2 ∂μ)
     =o[𝓝 (0 : Θ)] (fun h : Θ => ‖h‖ ^ 2)

The Lean definition uses Mathlib’s L2 -membership predicate and asymptotic little-o notation. The
field isLittleO records the displayed rate statement. The field mem records the integrability content
presupposed by the source integral: Mathlib’s Bochner integral is defined even for non-integrable
functions, so the rate statement alone would not force the residual to be an L2 object.
• Regular estimator sequence.         We use the regular-estimator definition of Chapter 8 of [30].

 Definition 3.2. A sequence of statistics Tn is regular at θ0 for estimating ψ(θ0 ) if there exists
 a probability measure Lθ0 such that, for every h ∈ Rk ,
                       √ (                 √ )
                        n Tn − ψ(θ0 + h/ n) ⇝ Lθ0 under Pθn0 +h/√n .

 The same limit law Lθ0 is used for every h.

   Lean represents this source condition as the following structure.
 structure RegularEstimatorSequence
     (M : ParametricFamily 𝓧 (AsymptoticRepresentation.Θ k))
     (μ : Measure 𝓧)
     (θ₀ : AsymptoticRepresentation.Θ k)
     (ψ : AsymptoticRepresentation.Θ k → AsymptoticRepresentation.𝓨 d)
     (T : ∀ n, (Fin n → 𝓧) → AsymptoticRepresentation.𝓨 d) :
     Type where
   limitDist : Measure (AsymptoticRepresentation.𝓨 d)
   isProb : IsProbabilityMeasure limitDist
   tendsto : ∀ h : AsymptoticRepresentation.Θ k,
     WeakConverges
       (fun n : ℕ =>
         (AsymptoticRepresentation.productMeasure M μ
             (θ₀ + (Real.sqrt n)⁻¹ • h) n).map
           (fun x => (Real.sqrt n) •
             (T n x - ψ (θ₀ + (Real.sqrt n)⁻¹ • h))))
       limitDist
The Lean definition uses Mathlib measures together with the project’s WeakConverges predicate.
The fields limitDist and tendsto record the common weak-limit law and the convergence required
for every local perturbation h; isProb records that this limit law is a probability measure.
• Tangent set and tangent space.          We use the tangent-set discussion and closed-linear-span
construction of Chapter 25.3 of [30].

 Definition 3.3. At P , a tangent set ṖP is a collection of score functions obtained from quadratic-
 mean-differentiable submodels through P ; by Lemma 25.14, these scores lie in L20 (P ). The
 generated tangent space is the closed linear span lin ṖP of this tangent set.

    The source first names the tangent set and later uses its closed linear span to define eﬀicient
influence functions and lower-bound statements. Lean keeps these two source-level objects separate:


                                                 14
TangentSpec formalizes ṖP , recording the tangent directions together with a realizing submodel
for each direction, while tangentSpace formalizes lin ṖP .
 structure TangentSpec (P : Measure Ω) [IsProbabilityMeasure P] where
   carrier : Set ↥(L2ZeroMean P)
   submodelOf : ∀ g ∈ carrier,
     ∃ γ : AsymptoticStatistics.Core.QMDPath.QMDPath P, γ.score = g

 noncomputable def tangentSpace
     {P : Measure Ω} [IsProbabilityMeasure P] (T : TangentSpec P) :
     Submodule ℝ ↥(L2ZeroMean P) :=
   (Submodule.span ℝ T.carrier).topologicalClosure

The Lean definition uses Mathlib’s L2 space and closed-submodule operations. In TangentSpec,
carrier is the tangent set itself, while submodelOf records that each listed direction is realized
as the score of a quadratic-mean-differentiable submodel. The derived object tangentSpace then
takes the closed linear span of carrier, corresponding to lin ṖP in the source.

3.2   Local Asymptotic Normality
Local Asymptotic Normality (LAN) expresses the log-likelihood ratio of a regular parametric ex-
periment under local reparametrization as a quadratic-Gaussian-plus-remainder; it is the gateway
through which every downstream cornerstone reduces to a Gaussian-shift question.

 Theorem 3.4 ([30, Theorem 7.2]). Suppose Θ is an open subset of Rk and the model (Pθ : θ ∈
 Θ) is differentiable in quadratic mean at θ. Then Pθ ℓθ = 0 and the Fisher information matrix
 I θ = Pθ ℓ θ ℓ ⊤
                θ exists. Furthermore, for every converging sequence hn → h, as n → ∞,

                             ∏
                             n
                               pθ+hn /√n
                       log                 (Xi ) = h⊤ ∆n,θ − 12 h⊤ Iθ h + oPθ (1),
                                   pθ
                             i=1
                      ∑n
 where ∆n,θ = n−1/2    i=1 ℓθ (Xi ) is asymptotically N (0, Iθ ).

   The Lean entry point is LAN_expansion, with signature:
 theorem LAN_expansion
     {k : ℕ}
     {Ω : Type*} {mΩ : MeasurableSpace Ω} (P : Measure Ω)
     [IsProbabilityMeasure P]
     (M : ParametricFamily 𝓧 (EuclideanSpace ℝ (Fin k))) (μ : Measure 𝓧)
     [SigmaFinite μ]
     (θ₀ : EuclideanSpace ℝ (Fin k))
     (ℓ : 𝓧 → EuclideanSpace ℝ (Fin k)) (hℓ : Measurable ℓ)
     (hPDF : IsPDFOf M μ)
     (hDQM : DifferentiableQuadraticMean M μ θ₀ ℓ)
     (h : EuclideanSpace ℝ (Fin k)) (h_n : ℕ → EuclideanSpace ℝ (Fin k))
     (hconv : Filter.Tendsto h_n Filter.atTop (𝓝 h))
     (X : ℕ → Ω → 𝓧) (hX_meas : ∀ i, Measurable (X i))
     (hindep : Pairwise fun i j => ProbabilityTheory.IndepFun (X i) (X j) P)
     (hident : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) P P)
     (hlaw : Measure.map (X 0) P
               = μ.withDensity fun x => ENNReal.ofReal (M.density θ₀ x)) :
     (∀ u, ∫ x, ⟪u, ℓ x⟫ * M.density θ₀ x ∂μ = 0) ∧



                                                    15
      (∀ u, Integrable (fun x => ⟪u, ℓ x⟫^2 * M.density θ₀ x) μ) ∧
      TendstoInMeasure P
        (fun n ω =>
          (∑ i ∈ Finset.range n,
            Real.log (M.density (θ₀ + (Real.sqrt n)⁻¹ • h_n n) (X i ω)
                      / M.density θ₀ (X i ω)))
          - (Real.sqrt n)⁻¹ * ∑ i ∈ Finset.range n, ⟪h, ℓ (X i ω)⟫
          + (1/2 : ℝ) * fisherInformation M μ θ₀ ℓ h h)
        Filter.atTop (fun _ => (0 : ℝ))

     The conclusion states the three assertions of Theorem 7.2 that are uniform in the experiment:
the score identity Pθ ℓθ = 0, finiteness of the Fisher information, and the in-probability quadratic
expansion. It carries no separate openness or interior hypothesis: its parameter space is the typed
                                                                                    √
Euclidean space EuclideanSpace ℝ (Fin k), so local perturbations θ0 + hn / n are well typed
by construction, with the global normalization carried by IsPDFOf M μ. The remaining local con-
tent is the reusable DifferentiableQuadraticMean M μ θ₀ ℓ, whose residual-integrability field the
signature inherits (Section 3.1).
     The asymptotic normality ∆n,θ ⇝ N (0, Iθ ) lies outside this entry point: it does not depend
on quadratic-mean differentiability but is the classical multivariate central limit theorem for the
i.i.d. score vectors ℓθ (Xi ). We therefore present only the three differentiability-driven conclusions
in LAN_expansion, keeping the normality clause in the quoted statement above solely to reproduce
[30, Theorem 7.2] in full.

3.3   Asymptotic Representation Theorem
                                                                                                      h
The Asymptotic Representation Theorem matches every weak limit of statistics Tn satisfying Tn ⇝
            n
Lθ,h under Pθ+h/ √ with a randomized statistic in the Gaussian shift experiment.
                  n

 Theorem 3.5 ([30, Theorem 7.10]). Assume that the model is differentiable in quadratic mean
 at θ with nonsingular Fisher information matrix Iθ . Let Tn be statistics in the local experiments
    n
 (Pθ+h/ √ : h ∈ Rk ) such that Tn converges in distribution under every h. Then there exists a
         n
 randomized statistic T in the normal experiment (N (h, Iθ−1 ) : h ∈ Rk ) such that Tn converges
 in distribution to T under every h.

    Lean represents this randomized-statistic conclusion in the equivalent Markov-kernel form: a
randomized statistic based on a Gaussian observation is equivalently a probability kernel from the
Gaussian observation space to the statistic space; this is the standard randomization formulation
in Le Cam’s comparison of experiments [17, Chapter 2].
    The Lean entry point is LAN_representation; the signature is:
 theorem LAN_representation
     (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) [SigmaFinite μ]
     (θ₀ : Θ k)
     (ℓ : 𝓧 → Θ k) (hℓ : Measurable ℓ)
     (hDQM : DifferentiableQuadraticMean M μ θ₀ ℓ)
     (J : Matrix (Fin k) (Fin k) ℝ) (hJ_pd : Matrix.PosDef J)
     (hJ : ∀ u v : Θ k, fisherInformation M μ θ₀ ℓ u v =
       ⟪u, (WithLp.equiv 2 _).symm (J.mulVec ((WithLp.equiv 2 _) v))⟫)
     (T : ∀ n, (Fin n → 𝓧) → 𝓨 d) (hT_meas : ∀ n, Measurable (T n))
     (L : Θ k → Measure (𝓨 d)) [∀ h, IsProbabilityMeasure (L h)]




                                                  16
      (hT_weak : ∀ h : Θ k,
        WeakConverges
          (fun n => (productMeasure M μ (θ₀ + (Real.sqrt n)⁻¹ • h) n).map (T n))
          (L h))
      [StandardBorelSpace (𝓨 d)] [Nonempty (𝓨 d)]
      [HasOuterApproxClosed (𝓨 d)] [BorelSpace (𝓨 d)]
      (hPDF : IsPDFOf M μ) :
      ∃ κ : Kernel (Θ k) (𝓨 d), IsMarkovKernel κ ∧
        ∀ h, L h = (multivariateGaussian h J⁻¹).bind κ

    The Lean signature carries these assumptions as lean-artifact witnesses rather than addi-
tional source-side restrictions. The measurability hypotheses hℓ and hT_meas expose the typed
data needed for score representatives and statistic pushforwards, while hPDF packages the density
normalization and integrability facts needed to form the product experiments. The kernel conclu-
sion also requires descriptive-set-theoretic structure on the statistic space (StandardBorelSpace,
Nonempty, BorelSpace, and HasOuterApproxClosed), automatic for Rd but explicit in Lean. Thus
the extra rows in the signature record Lean’s measure-kernel encoding of Theorem 7.10, not stronger
statistical assumptions.

3.4   Hájek–Le Cam Convolution Theorem
The Convolution Theorem decomposes the limit law of a regular estimator as a Gaussian shift
convolved with a noise factor, and specializes to a covariance-matrix lower bound when the limit
law has finite second moment.
 Theorem 3.6 ([30, Theorem 8.8]). Assume that the experiment (Pθ : θ ∈ Θ) is differentiable
 in quadratic mean at the point θ with non-singular Fisher information matrix Iθ . Let ψ be
 differentiable at θ. Let Tn be a regular estimator sequence in the experiments (Pθn : θ ∈ Θ) with
 limit distribution Lθ . Then there exists a probability measure Mθ such that

                                    Lθ = N (0, ψ̇θ Iθ−1 ψ̇θ⊤ ) ∗ Mθ .

 In particular, if Lθ has covariance matrix Σθ , then the matrix Σθ − ψ̇θ Iθ−1 ψ̇θ⊤ is non-negative-
 definite.
    The Lean entry point chains LAN (Section 3.2) and the Asymptotic Representation Theorem
(Section 3.3) through an equivariance bridge. The decomposition theorem itself has no moment
hypothesis:
 theorem hajek_le_cam_convolution_theorem
     (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) [SigmaFinite μ]
     (θ₀ : Θ k)
     (ℓ : 𝓧 → Θ k) (hℓ : Measurable ℓ)
     (hDQM : DifferentiableQuadraticMean M μ θ₀ ℓ)
     (J : Matrix (Fin k) (Fin k) ℝ) (hJ_pd : Matrix.PosDef J)
     (hJ_fisher : ∀ u v : Θ k, fisherInformation M μ θ₀ ℓ u v =
       ⟪u, (WithLp.equiv 2 _).symm (J.mulVec ((WithLp.equiv 2 _) v))⟫)
     (ψ : Θ k → 𝓨 d) (ψDot : Θ k →L[ℝ] 𝓨 d)
     (hψ_diff : HasFDerivAt ψ ψDot θ₀)
     (ψDotMat : Matrix (Fin d) (Fin k) ℝ)
     (h_ψDot_mat : ∀ h : Θ k,
       ψDot h = (WithLp.equiv 2 _).symm (ψDotMat.mulVec ((WithLp.equiv 2 _) h)))




                                                   17
      (T : ∀ n, (Fin n → 𝓧) → 𝓨 d) (hT_meas : ∀ n, Measurable (T n))
      (hReg : RegularEstimatorSequence M μ θ₀ ψ T)
      (hPDF : IsPDFOf M μ) :
      ∃ M_θ : Measure (𝓨 d), IsProbabilityMeasure M_θ ∧
        hReg.limitDist =
          (ProbabilityTheory.multivariateGaussian (0 : 𝓨 d)
            (ψDotMat * J⁻¹ * ψDotMat.transpose)) ∗ M_θ

  The covariance lower bound is packaged as a separate Lean entry point, so the finite-second-
moment witness is paid only by callers asking for the covariance statement:
  theorem cov_psd_of_regular_estimator
      (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) [SigmaFinite μ]
      (θ₀ : Θ k) (ℓ : 𝓧 → Θ k) (hℓ : Measurable ℓ)
      (hDQM : DifferentiableQuadraticMean M μ θ₀ ℓ)
      (J : Matrix (Fin k) (Fin k) ℝ) (hJ_pd : Matrix.PosDef J)
      (hJ_fisher : ∀ u v : Θ k, fisherInformation M μ θ₀ ℓ u v =
        ⟪u, (WithLp.equiv 2 _).symm (J.mulVec ((WithLp.equiv 2 _) v))⟫)
      (ψ : Θ k → 𝓨 d) (ψDot : Θ k →L[ℝ] 𝓨 d)
      (hψ_diff : HasFDerivAt ψ ψDot θ₀)
      (ψDotMat : Matrix (Fin d) (Fin k) ℝ)
      (h_ψDot_mat : ∀ h : Θ k,
        ψDot h = (WithLp.equiv 2 _).symm (ψDotMat.mulVec ((WithLp.equiv 2 _) h)))
      (T : ∀ n, (Fin n → 𝓧) → 𝓨 d) (hT_meas : ∀ n, Measurable (T n))
      (hReg : RegularEstimatorSequence M μ θ₀ ψ T)
      (hL_memLp : MemLp (fun y : 𝓨 d => y) 2 hReg.limitDist)
      (Sigmaθ : Matrix (Fin d) (Fin d) ℝ)
      (hSigmaθ_isCov : ∀ u v : 𝓨 d,
        ∫ y, ⟪u, y⟫ * ⟪v, y⟫ ∂hReg.limitDist
          - (∫ y, ⟪u, y⟫ ∂hReg.limitDist) * (∫ y, ⟪v, y⟫ ∂hReg.limitDist)
          = ⟪u, (WithLp.equiv 2 _).symm (Sigmaθ.mulVec ((WithLp.equiv 2 _) v))⟫)
      (hPDF : IsPDFOf M μ) :
      (Sigmaθ - ψDotMat * J⁻¹ * ψDotMat.transpose).PosSemidef

    The Lean signature of the corollary carries the implied hypothesis: second-moment condition
for the covariance positive semidefiniteness (PSD) conclusion. The phrase “if Lθ has covariance
matrix Σθ ” semantically presupposes Lθ to have finite second moment: without it, Σθ is undefined
and the statement is vacuous. The source text does not list the second moment as a separate
hypothesis, but the implication is linguistic, not mathematical: “has covariance matrix” is exactly
“has finite second moment plus the entries are the L2 inner products”. Our Lean version scopes
the MemLp witness as an internal antecedent to the covariance-PSD conclusion, classified implied
because the witnessing sentence is in the source verbatim (see Section 3.7).

3.5   Local Asymptotic Minimax bound
The local asymptotic minimax (LAM) bound gives a worst-case-over-finite-perturbations lower
bound on estimator risk; it is one of the most assumption-heavy cornerstones on the parametric
side and the one whose formalization surfaces the sharpest theorem-vs-proof scope distinction.

  Theorem 3.7 ([30, Theorem 8.11]). Let the experiment (Pθ : θ ∈ Θ) be differentiable in
  quadratic mean at θ with non-singular Fisher information Iθ . Let ψ be differentiable at θ. Let
  Tn be any estimator sequence in the experiments (Pθn : θ ∈ Rk ). Then for any bowl-shaped loss



                                                18
 function ℓ,
                           ∫                                                       ∫
                                   (√                 √       )
        sup lim inf sup        ℓ        n(Tn − ψ(θ + h/ n))         n
                                                                  dPθ+h/ √
                                                                           n   ≥       ℓ dN (0, ψ̇θ Iθ−1 ψ̇θ⊤ ).
               n→∞
       I⊂Rk          h∈I
       #I<∞

    Our Lean entry point is local_asymptotic_minimax_bound. Its proof reduces the theorem
to localAsymptoticRisk_ge_target, which combines with the Gaussian-shift minimax bound for
bowl-shaped losses. The signature is:
 theorem local_asymptotic_minimax_bound
     (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) [SigmaFinite μ]
     (θ₀ : Θ k)
     (ℓ : 𝓧 → Θ k) (hℓ : Measurable ℓ)
     (hDQM : DifferentiableQuadraticMean M μ θ₀ ℓ)
     (J : Matrix (Fin k) (Fin k) ℝ) (hJ : J.PosDef)
     (hJ_fisher : ∀ u v : Θ k, fisherInformation M μ θ₀ ℓ u v
       = ⟪u, (WithLp.equiv 2 _).symm (J.mulVec ((WithLp.equiv 2 _) v))⟫)
     (ψ : Θ k → 𝓨 d) (ψDot : Θ k →L[ℝ] 𝓨 d)
     (hψ_diff : HasFDerivAt ψ ψDot θ₀)
     (ψDotMat : Matrix (Fin d) (Fin k) ℝ)
     (h_ψDot_mat : ∀ h : Θ k,
       ψDot h = (WithLp.equiv 2 _).symm (ψDotMat.mulVec ((WithLp.equiv 2 _) h)))
     (T : ∀ n, (Fin n → 𝓧) → 𝓨 d) (hT_meas : ∀ n, Measurable (T n))
     (L : 𝓨 d → ℝ≥0∞)
     (hL_bowl : BowlShaped L) (hL_lsc : LowerSemicontinuous L)
     (hTight : MeasureTheory.IsTightMeasureSet
         (Set.range (fun n : ℕ =>
           (AsymptoticRepresentation.productMeasure M μ θ₀ n).map
             (fun ω => (Real.sqrt n) • (T n ω - ψ θ₀)))))
     (hPDF : IsPDFOf M μ) :
     localAsymptoticRisk M μ θ₀ T ψ L
       ≥ ∫⁻ y, L y ∂(multivariateGaussian (0 : 𝓨 d)
                      (ψDotMat * J⁻¹ * ψDotMat.transpose))

    The proof in [30, Theorem 8.11] restricts to lower semicontinuous bowl-shaped ℓ and uniformly
tight Tn . These restrictions are not listed in the theorem header but appear verbatim in the proof
                                                                                     √
opener (“we only give the proof under the further assumptions that the sequence n(Tn − ψ(θ))
is uniformly tight under θ and that ℓ is (lower) semicontinuous”). Our Lean signature promotes
them to the typed hypotheses hL_lsc and hTight, so local_asymptotic_minimax_bound proves
exactly the restricted theorem the published proof justifies. The row-level audit classifies both as
high-confidence with source location in the proof body rather than the header.


3.6   Semi-Parametric Convolution Theorem
At the semi-parametric tier the convolution pattern reappears under the lift from a Euclidean
parameter θ ∈ Rk to an infinite-dimensional parameter indexed by a tangent space ṖP ⊂ L20 (P ).

 Theorem 3.8 ([30, Theorem 25.20]). Let the function ψ : P → Rk be differentiable at P relative
 to the tangent cone ṖP with eﬀicient influence function ψ̃P . Then the asymptotic covariance
 matrix of every regular sequence of estimators is bounded below by P ψ̃P ψ̃P⊤ . Furthermore, if
 ṖP is a convex cone, then every limit distribution L of a regular sequence of estimators can be



                                                      19
              (             )
 written L = N 0, P ψ̃P ψ̃P⊤ ∗ M for some probability distribution M .

    We present the formalized theorem in its combined vector form below (k ≥ 1); we write part (a)
for the covariance lower bound and part (b) for the convolution decomposition used by the Lean
proof. The displayed combined form packages parts (a) and (b), so it carries the finite-second-
moment witness needed for part (a); the part-specific entry point for part (b) has the same common
inputs but omits that moment witness.
  theorem semiparametric_convolution_theorem_vec
      {ψ : Measure Ω → EuclideanSpace ℝ (Fin k)}
      (hψ : PathwiseDifferentiableAt_vec P (tangentSpace T_set) ψ)
      {IF_eff : Fin k → ↥(L2ZeroMean P)}
      (hEIF : IsEfficientInfluenceFunction_vec hψ.derivative IF_eff)
      (T_n : ∀ n, (Fin n → Ω) → EuclideanSpace ℝ (Fin k))
      (hT_meas : ∀ n, Measurable (T_n n))
      (L : Measure (EuclideanSpace ℝ (Fin k))) [IsProbabilityMeasure L]
      (hReg : IsRegularEstimator_vec P T_set ψ hψ hEIF T_n L)
      (hL_memLp : MemLp (id : EuclideanSpace ℝ (Fin k) → _) 2 L) :
      let G : Matrix (Fin k) (Fin k) ℝ := Matrix.gram ℝ IF_eff
      let Sigma : Matrix (Fin k) (Fin k) ℝ := fun i j =>
        ∫ y, (y.ofLp i - ∫ z, z.ofLp i ∂L)
            * (y.ofLp j - ∫ z, z.ofLp j ∂L) ∂L
      (Sigma - G).PosSemidef ∧
      (∃ M : Measure (EuclideanSpace ℝ (Fin k)), IsProbabilityMeasure M ∧
        L = (ProbabilityTheory.multivariateGaussian
              (0 : EuclideanSpace ℝ (Fin k)) G) ∗ M)

    The tangent-space encoding separates two roles. The pathwise derivative and eﬀicient influence
functions live over tangentSpace T_set, the L2 -closed span of the user-supplied tangent set; this
is the Hilbert-space object used for projections, Gram matrices, and eﬀicient-influence-function
approximation. The regular-estimator hypothesis, however, quantifies score directions only over the
algebraic span Submodule.span ℝ T_set.carrier, matching [30, p. 366] (“for every g ∈ lin gp ”).
The released theorem formalizes the linear-space case of Theorem 25.20 in [30], which the source
proof establishes first (“Assume first that the tangent set is a linear space”), by applying the finite-
dimensional argument on algebraic-span subspaces and passing to the closed-span limit through the
eﬀicient-influence-function approximation. In the displayed vector headline, the proof works over
the closed linear span generated by T_set.carrier; this space is automatically a convex cone, so
no separate cone hypothesis appears in that vector signature. The proof reuses the LAN expansion
(Section 3.2) and the Asymptotic Representation Theorem (Section 3.3), and applies the Hájek–
Le Cam Convolution Theorem (Section 3.4) to the sigmoid-family submodels of [30, Example 25.16].
This route replaces an earlier closure through the same theorem’s Fréchet wrapper, which forced
a uniform-Hadamard remainder condition; the architectural choices behind the rewrite (including
the three drift hypotheses it eliminated) are the subject of the case study in Section B.2.

3.7   Selected Surfaced Hypotheses by Tier
The cornerstone formalizations above surface hypotheses that a reader of the source prose might not
expect to track explicitly. We classify the cornerstone-by-cornerstone instances using the scheme of
Section 2.2.1. The list below is selective: it collects the recurring or load-bearing rows used in the
main-text discussion; a reference-document fragment appears in Appendix B.3. The bullets name
the Lean object, point to the relevant source evidence when applicable, and state why the assigned


                                                  20
tier applies.
Hypotheses labeled with high-confidence.
• hL_lsc (lower semicontinuity of the loss, LAM bound): [30, Chapter 8], proof opener of Theo-
  rem 8.11 verbatim.
• hTight (uniform tightness of the recentered estimator, LAM bound): same proof opener (Sec-
  tion 3.5).
• tangentSpace (closed linear span, semi-parametric Convolution Theorem): takes the closure of
  the user-supplied span, matching [30, Chapter 25.3] verbatim; the eﬀicient influence function is
  quantified over this closed span, and the convolution-decomposition statement uses it through
  the EIF Gram matrix.
Hypotheses labeled with lean-artifact.
• Parametric DifferentiableQuadraticMean residual mem field: Bochner-integral
                                                                        ∫         representation
  choice for the parametric LAN cornerstone’s∫real-integral form (Lean’s f dµ returns 0 on non-
  integrable f , whereas the source expression f 2 dµ < ∞ presupposes integrability).
• Measurability witnesses such as hℓ and hT_meas: Lean requires them when forming integrals,
  product laws, and pushforwards from the score representatives and estimator statistics of the
  source setup (Section 3.3).
• Density-family adapter hPDF : IsPDFOf M μ: it writes pθ as a density of Pθ with respect to a
  dominating measure [30]; the Lean API packages the corresponding normalization, nonnegativity,
  and integrability facts explicitly.
Hypotheses labeled with implied.
• hL_memLp for covariance-matrix conclusions. In the Hájek–Le Cam Convolution Theorem, the
  witnessing sentence is [30, p. 115] “if Lθ has covariance matrix”; in the semi-parametric Convo-
  lution Theorem, the statement uses the phrase “asymptotic covariance matrix”. Both phrases
  semantically presuppose a finite second moment, so the Lean moment witness is scoped only to
  the covariance-PSD/covariance-Gram conclusions (Sections 3.4 and 3.6).
No hypotheses labeled with potential-drift. On the cornerstone chains this column is empty:
every hypothesis on a cornerstone main signature either matches a reference row directly or has
been reverted. The operational referent is the LAM-bound drift episode of Section B.1: its clearest
row was hL_coercive, a coercivity strengthening of the source bowl-shaped-loss assumption, but
the same audit also reverted hL_continuous, h_L_orig_avgRisk_bd, and hψ_meas. Thus the empty
potential-drift column records the post-revert theorem state; Section B.1 describes how the drift
was introduced and removed.


4   Conclusion
We have presented a systematic Lean 4 formalization of asymptotic statistical estimation theory,
covering core parametric and semi-parametric limit theorems through reusable probability infras-
tructure, statistical concept definitions, and theorem-level entry points. The accompanying multi-
agent scaffold addresses the thin-Mathlib-coverage setting of this domain, while the hypothesis-
disciplined audit makes source-faithfulness a runtime obligation rather than a consequence of com-
pilation alone. Together, the formal library and the audit methodology show how agent-assisted
formalization can scale while keeping theorem assumptions tied to the mathematical source.
    Future work has two immediate directions. On the mathematical side, the library should be


                                                21
extended toward broader asymptotic statistics, including additional limit experiments, eﬀiciency
results, and nonparametric settings. On the methodological side, the audit should be tested across
other assumption-heavy domains and agent platforms, with more automation for extracting candi-
date theorem boundaries and tracking source evidence across refactors.


References
 [1] Reynald Affeldt, Alessandro Bruni, Cyril Cohen, Pierre Roux, and Takafumi Saikawa. Formal-
     izing concentration inequalities in Rocq: infrastructure and automation. In 16th International
     Conference on Interactive Theorem Proving (ITP 2025), volume 352, pages 21:1–21:20. Schloss
     Dagstuhl–Leibniz-Zentrum für Informatik, 2025.

 [2] Reynald Affeldt, Manabu Hagiwara, Jonas Sénizergues, Jacques Garrigue, Kazuhiko Sakaguchi,
     Taku Asai, Takafumi Saikawa, Naruomi Obata, and Alessandro Bruni. Infotheo: A Rocq
     formalization of information theory and linear error-correcting codes. https://github.com/
     affeldt-aist/infotheo, 2026. Latest stable release 0.9.7.

 [3] Jeremy Avigad, Johannes Hölzl, and Luke Serafin. A formally verified proof of the central
     limit theorem. Journal of Automated Reasoning, 59(4):389–423, 2017.

 [4] Kaito Baba, Chaoran Liu, Shuhei Kurita, and Akiyoshi Sannai. Prover agent: An agent-based
     framework for formal mathematical proofs. arXiv preprint arXiv:2506.19923, 2025.

 [5] Benjamin Breen, Marco Del Tredici, Jacob McCarran, Javier Aspuru Mijares, Weichen Win-
     ston Yin, Kfir Sulimany, Jacob M Taylor, Frank HL Koppens, and Dirk Englund. AX-Prover:
     A deep reasoning agentic framework for theorem proving in mathematics and quantum physics.
     arXiv preprint arXiv:2510.12787, 2025.

 [6] Guoxiong Gao, Bin Wu, Zeming Sun, Jiedong Jiang, Wanyi He, Zichen Wang, Yutong Wang,
     Peihao Wu, and Bin Dong. Archon: Toward fully autonomous formalization of FirstProof’s
     research-level problems. https://github.com/frenzymath/Archon; announcement at https:
     //frenzymath.com/news/archon-firstproof/, March 2026.

 [7] Fabian Gloeckle, Ahmad Rammal, Charles Arnal, Remi Munos, Vivien Cabannes, Gabriel
     Synnaeve, and Amaury Hayat.     Automatic textbook formalization.  arXiv preprint
     arXiv:2604.03071, 2026.

 [8] Sidharth Hariharan, Christopher Birkbeck, Seewoo Lee, Ho Kiu Gareth Ma, Bhavik Mehta,
     Auguste Poiroux, and Maryna Viazovska. A milestone in formalization: The sphere packing
     problem in dimension 8. arXiv preprint arXiv:2604.23468, 2026.

 [9] Osman Hasan and Sofiene Tahar. Formalization of continuous probability distributions. In
     International Conference on Automated Deduction, pages 3–18. 2007.

[10] Osman Hasan and Sofiene Tahar. Formalization of the standard uniform random variable.
     Theoretical Computer Science, 382(1):71–83, 2007.

[11] Michikazu Hirata. A formalization of the Lévy-Prokhorov metric in Isabelle/HOL. In 15th
     International Conference on Interactive Theorem Proving (ITP 2024), volume 309, pages 21:1–
     21:18. Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 2024.


                                                22
[12] I. A. Ibragimov and R. Z. Has’minskii. Statistical Estimation: Asymptotic Theory, volume 16
     of Stochastic Modelling and Applied Probability. Springer, New York, 1981.

[13] Vasily Ilin. Semi-autonomous formalization of the Vlasov-Maxwell-Landau equilibrium. arXiv
     preprint arXiv:2603.15929, 2026.

[14] Kyuhee Kim, Auguste Poiroux, and Antoine Bosselut. Do LLMs game formalization? evalu-
     ating faithfulness in logical reasoning. arXiv preprint arXiv:2604.19459, 2026.

[15] Adarsh Kumarappan, Mo Tiwari, Peiyang Song, Robert Joseph George, Chaowei Xiao, and
     Anima Anandkumar. LeanAgent: Lifelong learning for formal theorem proving. In Interna-
     tional Conference on Learning Representations, volume 2025, pages 73525–73564, 2025.

[16] Lucien Le Cam. Asymptotic Methods in Statistical Decision Theory. Springer Series in Statis-
     tics. Springer, New York, 1986.

[17] Lucien Le Cam and Grace Lo Yang. Asymptotics in statistics: some basic concepts. Springer
     Science & Business Media, 2000.

[18] Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Fan Yang, Xian Zhang, and Xiaoxing Ma.
     Autoformalize mathematical statements by symbolic equivalence and semantic consistency. In
     Advances in Neural Information Processing Systems, volume 37, pages 53598–53625, 2024.

[19] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
     Geng, Jiawei Ge, Jingruo Sun, et al. Goedel-Prover-V2: Scaling formal theorem proving with
     scaffolded data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.

[20] Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang,
     Yunzhou Xie, Junqiao Zhao, Qiufeng Wang, et al. Numina-Lean-Agent: An open and general
     agentic reasoning system for formal mathematics. arXiv preprint arXiv:2601.14027, 2026.

[21] Jordan Meadows, Lan Zhang, and Andre Freitas. FormalScience: Scalable human-in-the-
     loop autoformalisation of science with agentic code generation in Lean. arXiv preprint
     arXiv:2604.23002, 2026.

[22] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In International Conference on Automated Deduction, pages 625–635. Springer,
     2021.

[23] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL: a proof assistant
     for higher-order logic. Springer, 2002.

[24] Azim Ospanov, Farzan Farnia, and Roozbeh Yousefzadeh. Apollo: Automated LLM and Lean
     collaboration for advanced formal reasoning. In Advances in Neural Information Processing
     Systems, volume 38, pages 41599–41633, 2025.

[25] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. DeepSeek-Prover-V2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025.

[26] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models
     as copilots for theorem proving in Lean. arXiv preprint arXiv:2404.12534, 2024.

                                               23
[27] Sho Sonoda, Kazumi Kasaura, Yuma Mizuno, Kei Tsukamoto, and Naoto Onda. Lean formal-
     ization of generalization error bound by Rademacher complexity and Dudley’s entropy integral.
     arXiv preprint arXiv:2503.19605, 2025.
[28] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, CPP 2020, pages 367–
     381, New York, NY, USA, 2020. Association for Computing Machinery.
[29] The Rocq Development Team. The Rocq prover, version 9.2.0. Zenodo, 2026. https://doi.
     org/10.5281/zenodo.19256047.

[30] Aad W. van der Vaart. Asymptotic Statistics. Cambridge Series in Statistical and Probabilistic
     Mathematics. Cambridge University Press, 1998.
[31] Aad W. van der Vaart and Jon A. Wellner. Weak Convergence and Empirical Processes: With
     Applications to Statistics. Springer Series in Statistics. Springer, New York, 1996.
[32] Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert:
     Recursively building formal proofs with informal reasoning. arXiv preprint arXiv:2509.22819,
     2025.
[33] Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang, Yizhen Jia, Shizhe Diao, Renjie Pi, Junjie Hu,
     and Tong Zhang. MA-LoT: Model-collaboration Lean-based long chain-of-thought reasoning
     enhances formal theorem proving. In Proceedings of the 42nd International Conference on
     Machine Learning (ICML), volume 267 of Proceedings of Machine Learning Research, pages
     63972–64004. PMLR, 2025.
[34] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan J Prenger, and Animashree Anandkumar. LeanDojo: Theorem proving with
     retrieval-augmented language models. In Advances in Neural Information Processing Systems,
     volume 36, pages 21573–21612, 2023.
[35] Lan Zhang, Marco Valentino, and André Freitas. MASA: LLM-driven multi-agent systems for
     autoformalization. In Proceedings of the 2025 Conference on Empirical Methods in Natural
     Language Processing: System Demonstrations, pages 615–624, 2025.
[36] Yuanhe Zhang, Jason D Lee, and Fanghui Liu. Statistical learning theory in Lean 4: Empirical
     processes from scratch. arXiv preprint arXiv:2602.02285, 2026.


A     Evaluation
In this appendix, together with the two case studies presented in Appendix B, we answer three
questions about the methodological contributions of Section 1.1: (i) is the closed artifact axiom-
clean at the scale claimed (Section A.2); (ii) do the row-level signature audit and the definition
audit catch failure modes that lake build, #print axioms, and subjective mathematical review let
pass (Section A.3); and (iii) do the two case studies exhibit diﬀiculties specific to faithful statistical
formalization that stress-test the audit discipline introduced in Section 2.2.1 (Appendix B). The
LAM bound isolates the failure mode at the signature layer; the semi-parametric Convolution
Theorem extends it to the definition layer. Operational metrics (commit attribution, retrieval
usage, wave terminal-state breakdown, cost concentration, and the full falsification log) are treated
as project-run artifacts rather than load-bearing evidence for the released theorem statements.

                                                   24
A.1    Platform Requirements
The framework does not require a custom agent-platform integration, but it does assume a small
set of harness primitives:

  1. Agent dispatch into an isolated execution context. In our case a git worktree on the same
     host, with the Lake package directory symlinked and the build cache copied for fast rebuilds.
  2. Durable task cards and self-identified terminal-state returns for each dispatched agent (the
     recorded wave outcomes of Table 1).
  3. Tool-mediated build verification through the platform’s shell primitive (lake build invoked
     from inside the worktree by both Executors and the gating Reviewer).

These primitives are common in current coding-agent environments, but this paper evaluates only
one implementation: every experiment used Claude Code (Opus 4.7) for both the Manager session
and all agent dispatches. We have not validated the framework end-to-end on a platform other
than Claude Code.

A.2    Scale and Axiom Certificates
The released library comprises about 80,700 lines of Lean 4 code across 151 files: roughly 240
definitional declarations and about a thousand lemmas and theorems (counted by a line-prefix scan,
so indicative rather than exact), so the definitional surface is compact relative to the proof effort
built on it. Every declaration in the released library is axiom-clean, with no sorryAx; Appendix C.1
records the per-cornerstone certificates and the exact baseline axiom set.
    The library can support further formalization in the same domain: a substantial part of it is
general-purpose probability, measure-theory, and analysis material that fills gaps in current Mathlib
and is a candidate for upstreaming, and this reusable infrastructure is distributed across the library
rather than confined to any one directory. The cornerstone entry-point theorems sit above it as
axiom-clean, named entry points.

A.3    Hypothesis Classification and Audit Outcomes
Across the five released cornerstones, the audit layer turns source-faithfulness into a row-level
property of theorem and definition boundaries. Each cornerstone’s reference document classifies
every signature hypothesis and instance binder into the four tiers of Section 2.2.1, and the load-
bearing outcome is uniform across the five released cornerstones: no cornerstone chain carries
a potential-drift row. The only implied rows are the finite-second-moment prerequisites for
covariance or variance statements. The mechanical audit script reports Mechanical checks:
PASS on all five cornerstones, and each row is tied to a source quotation, an implied mathematical
prerequisite, or a concrete Lean encoding correspondence.
   These rows make the extra structure in the Lean statements accountable. A reviewer can inspect,
argument by argument, whether a formal boundary is source-stated, source-implied, required by
the encoding, or unsupported. Appendix B gives the two case studies behind this claim: first at
the main-signature boundary of the LAM theorem, and then at the definition boundary of the
semi-parametric Convolution Theorem.




                                                 25
B     Case Studies and Supporting Evidence
B.1    Case Study: The LAM-Bound Drift Episode
The LAM bound shows the control loop at the theorem-signature boundary. An initially plausible
route produced a closed but over-strengthened statement; the audit rows exposed the unsupported
assumptions, and the Manager sent the theorem back to planning rather than accepting the stronger
boundary. The released LAM theorem is closed with no extra unsupported assumptions.
The setting. Early in LAM development the proof tried to shortcut the finite-prior LAN bridge
by moving directly to Gaussian-τ -prior average-risk objects at the sub-lemma level. That shortcut
mixed the finite-prior comparison step with the later Gaussian-shift minimax calculation, so the
intermediate hypotheses no longer had a clean anchor in the reference text. The skeleton was
build-clean (lake build succeeded), and subsequent dispatch batches chained off it.
Drift accumulation. During the body phase, proof blockers led later route revisions to pro-
pose four unsupported assumptions on candidate LAM signatures: hL_coercive, hL_continuous,
h_L_orig_avgRisk_bd, and hψ_meas. Each was introduced to discharge a blocker raised by the
mis-specified collapse, strengthening the hypothesis set rather than questioning the strategy. The
result was an axiom-clean, sorry-free chain with a strictly over-strengthened hypothesis boundary,
and hence a weaker theorem than the standard LAM statement: the constant-zero loss function is
bowl-shaped but not coercive, refuting hL_coercive as a hypothesis a faithful formalization could
carry. The other rows failed the audit by strengthening the theorem boundary or imposing a
condition outside the source theorem’s scope.
    The measurability row is a useful inversion of the usual source-text problem. Human prose
often leaves measurability obligations implicit, but here the agent-side pressure went in the opposite
direction: blocked routes promoted a global measurability assumption on the functional, hψ_meas,
to the theorem boundary even though the LAM theorem does not require it there. The audit
therefore treated hψ_meas as a route artifact, not a released assumption.
Route correction and released state. The row-level reference made the strengthened bound-
ary visible: hL_coercive strictly strengthens the “bowl-shaped” hypothesis of [30, Theorem 8.11],
hL_continuous strictly strengthens the proof opener’s lower-semicontinuity condition, hψ_meas has
no source anchor, and h_L_orig_avgRisk_bd restricts estimators beyond the source’s regularity.
All four were therefore recorded as potential-drift. Under the workflow of Section 2.1, the Man-
ager treated these rows as route errors rather than accepted hypotheses, sending the theorem back
to the Planner. The replacement proof follows the source argument more closely. In the Lean
development, the route is exposed by localAsymptoticRisk_ge_target: it first passes to a subse-
quential Gaussian-shift limit for the recentered estimator–score pair, then transfers lower bounds
from rational local parameters to all local parameters by lower semicontinuity, and finally applies
the Gaussian-shift bowl-shaped-loss lower bound.
    The released LAM statement is therefore not the strengthened intermediate theorem: its audited
boundary has no potential-drift row, and every remaining formal argument is source-stated,
source-implied, or justified by a concrete Lean encoding correspondence.
    The episode is the operational referent of the theorem-boundary claim: the workflow converted
four unsupported assumptions into a route change and finished the theorem without carrying them
in the released signature.




                                                 26
B.2    Case Study: The Semi-Parametric Convolution Theorem
The semi-parametric Convolution Theorem (Section 3.6) shows the same control loop one layer
deeper, at the definition boundary. In one development cycle, a second-moment prerequisite is
accepted as implied, three signature-side drifts are rejected as potential-drift, an attempted
relocation into authored structure fields is made visible by the definition audit, and the final proof
is recovered by a strategic rewrite rather than by adding hypotheses. The released theorem and
audited definitions have no extra unsupported assumptions: every non-verbatim input is either
classified as implied or justified as a Lean representation choice.
The implied second-moment assumption. The source theorem states part (a) as “the asymp-
totic covariance matrix of every regular sequence of estimators is bounded below by P ψ̃P ψ̃P⊤ ”; the
phrase “covariance matrix” presupposes the matrix exists as E[(X − EX)(X − EX)⊤ ], requiring
E[Xi2 ] < ∞, i.e. a finite second moment of L that the source theorem does not state separately.
    The first attempt to close part (a) blocked at the covariance lower bound. In the released Lean
route, the finite-second-moment fact is not derived from the other regularity hypotheses; it is sup-
plied explicitly because the source phrase “covariance matrix” already presupposes such a moment
condition. Without this MemLp 2 witness, the encoded covariance inequality does not express the
intended lower bound through Mathlib’s covariance and moment APIs. Re-reading against the row-
level reference identified “covariance matrix” as the source; the finite-second-moment hypothesis
was classified implied (the source phrase “covariance matrix” is the witnessing sentence). A subse-
quent split of the Lean entry points (Section 3.6) confines it to part (a); part (b)’s decomposition
is well-defined for arbitrary L.
Drift accumulation, made visible by the row-level reference. Independently of this implied-
hypothesis surfacing, the original closure of the cornerstone routed through the parametric Convolu-
tion Theorem’s Fréchet wrapper (Section 3.4), which forced uniform Hadamard. As the proof route
developed, three unsupported assumptions appeared as route pressure: a bounded-density regular-
ity condition on the tangent set (hT_dense); a uniform-Hadamard remainder bound strictly stronger
than the source’s pointwise pathwise-differentiability (hψ_Hadamard_remainder); and an externally
supplied path family with its score-equation hypothesis (γ + hγ_score), where the source proof
constructs the family inside the proof body.
    The bounded-density and uniform-Hadamard assumptions reached the main theorem signature,
while the path-family hypothesis appeared only on an intermediate candidate route. None matched
a source row, so all three were classified potential-drift. As in the LAM case, that classification
did not authorize a stronger theorem; it returned the route to planning.
Failed relocation into definitions. A later route tried to move the same conditions one
layer down, into authored structure fields. It added a hadamard_remainder field to Pathwise
DifferentiableAt and a bounded_dense field to TangentSpec, dropping the two corresponding
hypotheses from the main signature; the potential-drift column on the theorem momentarily
emptied, the build stayed green, and #print axioms stayed at the project baseline.
    The definition audit made the relocation visible. The added fields had no source anchor: the
source tangent-set definition (Chapter 25.3) carries no bounded-density regularity condition, and
the pathwise-differentiability definition ([30, p. 363]) is pointwise, not uniform-Hadamard. Both
fields were reverted, and the two hypotheses returned to the potential-drift column. A par-
allel definition-side episode on the QMDPath structure (qmd_residual_memLp added as a separate
field, then removed by restating the quadratic-mean limit in R≥0 form) is documented in Ap-
pendix B.3. Across both episodes, the system forced drift to surface either as a theorem-side
potential-drift row or as a definition-side potential-drift row, leaving no path through silent


                                                 27
definitional strengthening.
Strategic rewrite and released state. Once the audit had rejected both repairs—adding the
assumptions to the theorem signature and relocating them into authored structure fields—the orig-
inal proof route had no faithful local patch. The remaining option was an architectural rewrite.
Phase Sigmoid re-architected the proof chain around [30, Example 25.16] (construction in Sec-
tion 3.6), eliminating all three drift pressures at the source. No new structure field, no moment
strengthening on the basis scores; the post-Phase-Sigmoid potential-drift and definition-side
potential-drift columns are both empty. The definition-level encoding of IsRegularEstimator
and the algebraic-span scope decision are addressed in Appendix C.3.

B.3   Semi-Parametric Reference Rows and Drift Sequence
Table 3 reproduces representative rows from the book-reference document shipped with the semi-
parametric Convolution Theorem artifact ([30, Theorem 25.20]), focusing on rows relevant to the
convolution-decomposition part (part (b)).
    The historical rows in the table correspond to the following development sequence, expanding
the compressed summary in Section B.2: the wave-by-wave drift accumulation, the attempted
relocation into authored structure fields, and the architectural rewrite that eliminated all three.
• First drift wave: agent introduces hT_dense (a bounded-density regularity condition on the
  tangent set) to the main signature, demanded by an early character-function deriver closure step.
  Not in the tangent-set definition of [30, Chapter 25.3].
• Second drift wave: hψ_Hadamard_remainder added: a uniform-Hadamard remainder strictly
  stronger than the source’s pointwise pathwise-differentiability ([30, p. 363]).
• Third drift wave: a user-supplied path family γ together with its score-equation hypothesis
  hγ_score, where the source proof constructs the family inside the proof body rather than
  receiving it as a hypothesis. This third drift appeared only on an intermediate candidate route.
• After three waves, two unsupported hypotheses had reached the main theorem signature, and a
  third had appeared on that intermediate route; lake build was green, #print axioms stayed
  at the project baseline, and there was no sorry. The row-level reference audit flagged all three
  as non-matching any high-confidence row.
• Attempted relocation into definitions: rather than rewrite the proof, the same conditions
  are moved one layer down: a hadamard_remainder field added to PathwiseDifferentiable
  At, and a bounded_dense field added to TangentSpec. The main signature’s potential-drift
  column momentarily empties; lake build stays green, #print axioms stays at the baseline.
• Definition audit blocks the relocation: the added fields have no source anchor: [30, Chap-
  ter 25.3] defines the tangent set as a collection of score functions in L2 (P ) arising from QMD
  submodels, with no bounded-density condition, and [30, p. 363] defines pathwise differentiability
  as a pointwise statement along each submodel, with no uniform Hadamard rate. Both fields are
  reverted in a single commit; the two signature-side drift rows return to the potential-drift
  column.
• Parallel definition-side episode: a qmd_residual_memLp field is caught on the QMDPath struc-
  ture (an L2 -membership claim on the DQM residual, absent from the source’s Chapter 25.3
  eq. (25.13)). This is the semi-parametric QMDPath structure, distinct from the parametric
  DifferentiableQuadraticMean residual mem field discussed in Section 3.7: the parametric cor-
  nerstone keeps vdV’s real-integral equation (7.1), where the extra field restores the Lebesgue-
  integrability content, whereas this semi-parametric cornerstone adopts an R≥0 eLpNorm form of
  equation (25.13). Accordingly, the added field is removed by restating the quadratic-mean limit

                                                28
Row                 Ref.            Verbatim opener / justification
high-confidence
T_set               Ch. 25.3 /      “ … differentiable at P relative to the tangent cone ṖP …” Tangent
                    p. 366          cone source: [30, Chapter 25.3, p. 362].
hReg                Ch. 25.3 /      “An estimator sequence Tn is called regular at P for estimating ψ(P )
                    pp. 365–366     …” Encoded over the algebraic span Submodule.span ℝ T_set.carrier
                                    (vdV’s “g ∈ lin gp ,” p. 366).
lean-artifact
hT_meas             Ch. 25.3 /      Estimator measurability, stated verbatim in the source: “as usual, an
                    p. 365          estimator sequence Tn is a measurable function Tn (X1 , . . . , Xn ) of the
                                    observations” [30, Chapter 25.3, p. 365]. hT_meas is the explicit Lean
                                    witness of this source-stated property, used to form pushforwards and
                                    integrals.
potential-drift (historical)
hT_dense            none            [Eliminated] Bounded-density regularity on the tangent set, demanded
                                    by an early character-function step; removed by the Phase Sigmoid
                                    rewrite.
Hadamard rem.       none            [Eliminated] A uniform-Hadamard rate, strictly stronger than the
                                    source’s pointwise pathwise-differentiability ([30, p. 363]); removed by
                                    the same rewrite.
high-confidence definition-side row
IsRegular           Ch. 25.3 /      “An estimator sequence Tn is called regular at P for estimating ψ(P ) …
Estimator_vec       p. 365          for every g ∈ ṖP .” This is the source anchor for the chosen-submodel
                                    regularity pattern: one realizing submodel is selected for each score di-
                                    rection in the algebraic-span scope Submodule.span ℝ T_set.carrier
                                    used by the released theorem (vdV’s “g ∈ lin gp ”).
reverted definition-side drift (historical)
Hadamard rem.     none           [Reverted] Field added to the pathwise-differentiability structure to
                                 hide the same uniform-Hadamard requirement; the definition audit
                                 caught that [30, p. 363] is pointwise, with no uniform rate.
bounded_dense     none           [Reverted] Field added to the tangent-set definition; [30, Chapter 25.3]
                                 defines the tangent set as a collection of score functions in L2 (P ) arising
                                 from QMD submodels, with no bounded-density condition, so the field
                                 was removed.

Table 3: Abridged excerpt from the book-reference document accompanying the semi-parametric
Convolution Theorem cornerstone. The table is a selected excerpt rather than the complete audit
record. potential-drift is empty on the released artifact; all potential-drift rows shown here
are historical, kept for parallel with the development case study (Section B.2) and marked [Elimi-
nated] or [Reverted] accordingly.


  in R≥0 form and recovering the previous corollary statement as a downstream lemma rather
  than a structure field.
• Architectural rewrite (Phase Sigmoid): the proof chain is re-architected around [30, Ex-
  ample 25.16]’s sigmoid-family construction, eliminating all three drift pressures at the source.
  No new structure field, no moment strengthening on the basis scores. The audit script applied
  to the post-rewrite state confirms no signature-side and no definition-side drift.


                                                     29
B.4   Joint Lesson
The LAM case study (Section B.1) establishes the theorem-boundary layer: unsupported assump-
tions on a main signature are routed back into planning until the released theorem has none. The
semi-parametric Convolution Theorem extends this in two directions. First, when the same pressure
moves into authored structure fields, the definition audit makes the relocation visible and returns
it to the same source-anchor discipline. Second, when both signature and definition boundaries are
clean but the proof route still demands unsupported assumptions, the resolution is architectural,
not a local patch. Phase Sigmoid is the operational referent: it replaces the proof route rather than
adding another hypothesis or definition field.


C     Verification Artifacts and Lean-Side Details
This appendix collects the Lean-side details that support the domain claims of Section 3 — ax-
iom certificates, signature pinning, and the load-bearing concept definitions that the cornerstone
signatures are stated in terms of — to keep the main text focused on the conceptual contributions.

C.1   Axiom Certificates
Each of the five cornerstones (LAN expansion, Asymptotic Representation, Hájek–Le Cam Con-
volution, Local Asymptotic Minimax bound, and the semi-parametric Convolution Theorem (Sec-
tion 3.6)), including the covariance-PSD conclusion associated with Hájek–Le Cam, compiles under
the same three baseline axioms. Running #print axioms on each top-level declaration produces

[propext, Classical.choice, Quot.sound]

with no sorryAx. Thus every step on the main chain of each theorem is closed by typed Lean
terms rather than deferred proof placeholders. The released artifact contains no remaining sorry,
on-chain or off-chain.

C.2   Signature Pinning
The axiom certificate of Appendix C.1 guarantees that every cornerstone is closed by typed Lean
terms; it says nothing about what those terms claim. A build can stay green, sorry-free, and
axiom-clean while a hypothesis, an instance binder, the conclusion, or an authored definition body
silently changes meaning. The signature-pinning pass closes this gap on the mechanical side. It
records the fully elaborated signature of each cornerstone and the body of each authored definition
the cornerstones depend on as a committed snapshot, and a checker fails whenever a regenerated
snapshot differs. The mechanical layer therefore certifies two complementary facts: that each
theorem is well typed (the axiom certificate) and that no tracked signature element changes without
surfacing in a single snapshot comparison (signature pinning). Faithfulness to [30], the judgment
that each surfaced element matches the source, remains the human-and-model row audit over the
book-reference document (Section 2.2.1).
    On the type side, membership is computed rather than curated. The tracked roots are exactly
the cornerstone theorems this paper claims; printing each elaborated type pins, for free, every in-
stance binder, universe level, and quantifier the type mentions, so no instance argument is selected
by hand; the only human choice is which cornerstones to pin, already fixed by the paper’s scope.


                                                 30
A definition the type names is pinned there only by use; the body that gives it meaning is tracked
separately. The tracked bodies are the authored book-concept definitions the cornerstone signa-
tures are stated in terms of (Appendix C.3). A body is pinned because changing it relocates a
proof obligation into a definition (the definition-drift channel of Section 3.7) without touching any
hypothesis. Mathlib definitions, including multivariateGaussian, are trusted base and are not
body-tracked; the pinned toolchain guards them.
    The signature pass of the audit suite (Section 2.2.1) reconciles a signature’s explicit hypotheses
against their reference rows by name and count. Signature pinning is what extends mechanical
coverage to the instance arguments, the conclusion, and the definition bodies: these enter through
the elaborated type and the printed body rather than through the name-and-count reconciliation.
The snapshot is taken with universe levels shown but proofs and notation left folded. Full expansion
of every instance and operator is faithful but yields an unreadable artifact (on the order of 105 lines),
whereas the universe-level form is under a thousand lines and remains a human-readable review
surface; proof-term arguments are elided by proof irrelevance, so an unrelated proof edit does not
perturb the snapshot. The single channel left uncovered is an internal instance replacement that
prints identically, which the row audit covers semantically on the affected hypothesis.
    Because the toolchain is pinned, the snapshot moves only when a tracked signature changes or
the toolchain is deliberately advanced, the latter regenerated within the same change. A coupling
check rejects any commit that stages a new snapshot without staging a book-reference update
alongside it, so a signature change cannot land without surfacing to the faithfulness audit in the
same commit.

C.3    Cornerstone-Load-Bearing Definitions
The theorem signatures in Section 3 are stated in terms of authored structures and defs whose
fields carry source content not visible on the signature alone. The case studies of Section B.2 (the
relocated hadamard_remainder and bounded_dense fields, and the rejected qmd_residual_memLp
field) hinge on these field layouts: the definition audit asks whether each structure field has a
source anchor, and the verdict is over the fields, not the structure’s name. The main text already
expands the DQM, regular estimator, and tangent-set definitions (Section 3.1); we do not repeat
those definitions here. The supplementary source excerpts below are a readability-oriented selection
of load-bearing declarations needed to read the cornerstone signatures and the case-study discussion;
they are not the complete tracked set of Appendix C.2. The displayed declarations are source
excerpts under their file-level namespace and variable context.
Vector-valued pathwise differentiability (PathwiseDifferentiableAt_vec).
[30, Chapter 25.3, pp. 362–363]. A vector functional ψ : M → Rk is pathwise differentiable at P
relative to a tangent space T if there exists a continuous linear map ψ̇ : T → Rk such that for every
QMD submodel t 7→ Pt through P with score g ∈ T , the difference quotient t−1 (ψ(Pt ) − ψ(P ))
converges to ψ̇(g) as t → 0.
 structure PathwiseDifferentiableAt_vec
     (ψ : Measure Ω → EuclideanSpace ℝ (Fin k)) where
   derivative : T →L[ℝ] EuclideanSpace ℝ (Fin k)
   derivative_spec :
     ∀ (γ : QMDPath.QMDPath P),
       ∀ (h_in_T : (γ.score : ↥(L2ZeroMean P)) ∈ T),
         Filter.Tendsto
           (fun t : ℝ => t⁻¹ • (ψ (γ.curve t) - ψ P))



                                                   31
            (nhdsWithin 0 {0}ᶜ) (nhds (derivative ⟨γ.score, h_in_T⟩))

Both fields match the source definition: the source definition packs (existence of a continuous-linear
derivative) and (convergence along every QMD submodel) and we transcribe them as the two fields.
Notably absent: uniform-Hadamard control, or any explicit remainder rate. [30, Chapter 25.3]
phrases convergence pointwise in t → 0 along each fixed submodel; uniformity over submodels
and remainder rates appear later (Chapter 25.6, for specific applications) and are not part of the
definition. The rejected hadamard_remainder field of Section B.2 would have added such a rate
condition here, strictly strengthening the source’s pointwise statement.
Parametric family (ParametricFamily, IsPDFOf). [30, Chapter 7], opening pages. Carries the
per-parameter density, its measurability, and nonnegativity; the normalization and integrability are
bundled in the companion predicate IsPDFOf.
 structure ParametricFamily
     (𝓧 : Type*) [MeasurableSpace 𝓧] (Θ : Type*) where
   density : Θ → 𝓧 → ℝ
   density_meas : ∀ θ, Measurable (density θ)
   density_nonneg : ∀ θ x, 0 ≤ density θ x

 structure IsPDFOf
     {𝓧 : Type*} [MeasurableSpace 𝓧] {Θ : Type*}
     (M : ParametricFamily 𝓧 Θ) (μ : Measure 𝓧) : Prop where
   density_integral_eq_one : ∀ θ, ∫ x, M.density θ x ∂μ = 1
   density_integrable : ∀ θ, Integrable (M.density θ) μ

Score function and Fisher information (ScoreFunction, fisherInformation). [30, The-
orem 7.2], p. 94. The score is a measurable map; the L2 properties (zero mean, finite Fisher
information) are downstream consequences of DQM, not structure fields (see Section 3.1).
 structure ScoreFunction
     (M : ParametricFamily 𝓧 Θ) (θ : Θ) where
   toFun : 𝓧 → Θ
   measurable : Measurable toFun

 noncomputable def fisherInformation
     (M : ParametricFamily 𝓧 Θ) (μ : Measure 𝓧) (θ : Θ) (ℓ : 𝓧 → Θ) :
     Θ → Θ → ℝ :=
   fun u v => ∫ x, (⟪u, ℓ x⟫ * ⟪v, ℓ x⟫) * M.density θ x ∂μ

Product measure Pθn (productMeasure). [30, Chapter 7], the n-fold i.i.d. product Pθn used
throughout the parametric cornerstones. Wraps Mathlib’s Measure.pi specialized to a parametric-
family density.
 noncomputable def productMeasure
     (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) (θ : Θ k) (n : ℕ) :
     Measure (Fin n → 𝓧) :=
   Measure.pi (fun _ =>
     μ.withDensity fun x => ENNReal.ofReal (M.density θ x))

Weak convergence (WeakConverges). A predicate-form wrapper for [30]’s ⇝. Mathlib al-
ready carries weak convergence as the weak topology on ProbabilityMeasure (with the bounded-
continuous-test-function characterization as the tendsto_iff_forall_integral_tendsto theorem);
the project’s WeakConverges restates the same content as a direct predicate on raw Measure E ar-
guments, so that cornerstone signatures can pass raw measure sequences directly.



                                                 32
 def WeakConverges {E : Type*} [MeasurableSpace E] [TopologicalSpace E]
     (μ : ℕ → Measure E) (ν : Measure E) : Prop :=
   ∀ f : E →ᵇ ℝ,
     Tendsto (fun n => ∫ x, f x ∂(μ n)) atTop
       (𝓝 (∫ x, f x ∂ν))

Bowl-shaped loss (BowlShaped). [30, Chapter 8.4], p. 113. Symmetric, convex sublevel sets, plus
a measurability adapter (source-implicit, required in Lean for the integral on the LAM bound’s
LHS to be defined).
 structure BowlShaped [AddCommGroup E] [Module ℝ E] [MeasurableSpace E]
     (L : E → ℝ≥0∞) : Prop where
   measurable : Measurable L
   symm : ∀ x, L (-x) = L x
   convex_sublevel : ∀ c : ℝ≥0∞, Convex ℝ {x | L x ≤ c}

Local asymptotic L-risk (localAsymptoticRisk). [30, Theorem 8.11], p. 118, the LHS of the
LAM bound: worst-case asymptotic L-risk over local finite alternatives.
 noncomputable def localAsymptoticRisk
     (M : ParametricFamily 𝓧 (Θ k)) (μ : Measure 𝓧) (θ₀ : Θ k)
     (T : ∀ n, (Fin n → 𝓧) → 𝓨 d) (ψ : Θ k → 𝓨 d)
     (L : 𝓨 d → ℝ≥0∞) : ℝ≥0∞ :=
   ⨆ I : Finset (Θ k), Filter.liminf
     (fun n : ℕ => ⨆ h ∈ I,
       ∫⁻ ω, L ((Real.sqrt n) • (T n ω - ψ (θ₀ + (Real.sqrt n)⁻¹ • h)))
             ∂(AsymptoticRepresentation.productMeasure M μ (θ₀ + (Real.sqrt n)⁻¹ • h) n))
     Filter.atTop

QMD submodel (QMDPath). [30, Chapter 25.3, Eq. (25.13)], pp. 362–363. A quadratic-mean-
differentiable submodel through P in the dominated specialization authorized by the footnote on
p. 362; the score lives in the closed mean-zero L2 subspace L2ZeroMean P (defined below).
 structure QMDPath (P : Measure Ω) [IsProbabilityMeasure P] where
   curve : ℝ → Measure Ω
   curve_at_zero : curve 0 = P
   curve_isProbability : ∀ t, IsProbabilityMeasure (curve t)
   dominating : Measure Ω
   curve_absContinuous : ∀ t, curve t ≪ dominating
   dominating_sigmaFinite : SigmaFinite dominating
   score : ↥(L2ZeroMean P)
   qmd_limit :
     Tendsto
       (fun t : ℝ =>
         eLpNorm (fun ω : Ω =>
           Real.sqrt ((curve t).rnDeriv dominating ω).toReal
             - Real.sqrt ((curve 0).rnDeriv dominating ω).toReal
             - (t / 2) * (score : Ω → ℝ) ω
                 * Real.sqrt ((curve 0).rnDeriv dominating ω).toReal)
           2 dominating / ENNReal.ofReal |t|)
       (𝓝[≠] 0) (𝓝 (0 : ℝ≥0∞))

Zero-mean L2 subspace (L2ZeroMean). The closed submodule of Lp ℝ 2 P of mean-zero func-
tions: the kernel of the integral functional, restricted to L2 (P ). The semi-parametric tangent space
is a submodule of this object.



                                                 33
 noncomputable def L2ZeroMean (P : Measure Ω) [IsFiniteMeasure P] :
     Submodule ℝ (Lp ℝ 2 P) :=
   LinearMap.ker (integralL2 P).toLinearMap

Eﬀicient influence function, vector form (IsEfficientInfluenceFunction_vec). [30, Chap-
ter 25.3], pp. 363–365. IsEfficientInfluenceFunction_vec lifts the coordinate-wise eﬀicient-
influence-function predicate to a k-tuple. The semi-parametric Cramér–Rao bound is the k × k
Gram matrix of this tuple — [30, p. 365]’s optimal asymptotic covariance P ψ̃P ψ̃P⊤ , with entries
hIFi , IFj iL2 (P ) . The cornerstone signatures take this matrix as Mathlib’s Matrix.gram applied to
the tuple of eﬀicient influence functions, so no project-level wrapper is introduced.
 def IsEfficientInfluenceFunction_vec
     (Dψ : T →L[ℝ] EuclideanSpace ℝ (Fin k))
     (IF : Fin k → ↥(L2ZeroMean P)) : Prop :=
   ∀ i, IsEfficientInfluenceFunction P T
     (EuclideanSpace.proj i ∘L Dψ) (IF i)

Regular estimator, semi-parametric form (IsRegularEstimator_vec). [30, Chapter 25.3],
pp. 365–366; the semi-parametric analog of RegularEstimatorSequence. The source phrases reg-
ularity by selecting, for each score direction g ∈ ṖP , a submodel (“write Pt,g for a submodel”);
the Lean definition records this submodel as an existentially quantified chosenFamily with score
g, along which the rescaled, perturbed-truth–recentered estimator converges weakly to the com-
mon limit law L. The score direction is quantified over the algebraic span of T_set.carrier ([30,
p. 366], “for every g ∈ lin gp ”); the pathwise derivative hψ and the eﬀicient influence function hEIF
are quantified over the L2 -closed span tangentSpace T_set.
 def IsRegularEstimator_vec
     (P : Measure Ω) [IsProbabilityMeasure P]
     (T_set : TangentSpec P)
     {k : ℕ}
     (ψ : Measure Ω → EuclideanSpace ℝ (Fin k))
     {IF_eff : Fin k → ↥(L2ZeroMean P)}
     (hψ : PathwiseDifferentiableAt_vec P (tangentSpace T_set) ψ)
     (_hEIF : IsEfficientInfluenceFunction_vec
               (P := P) (T := tangentSpace T_set)
               hψ.derivative IF_eff)
     (T_n : ∀ n, (Fin n → Ω) → EuclideanSpace ℝ (Fin k))
     (L : Measure (EuclideanSpace ℝ (Fin k)))
     [IsProbabilityMeasure L] :
     Prop :=
   ∃ chosenFamily :
       ∀ (g : ↥(L2ZeroMean P)),
         (g : ↥(L2ZeroMean P)) ∈
           Submodule.span ℝ T_set.carrier → QMDPath P,
     (∀ (g : ↥(L2ZeroMean P))
         (hg : (g : ↥(L2ZeroMean P)) ∈
           Submodule.span ℝ T_set.carrier),
       (chosenFamily g hg).score = g) ∧
     (∀ (g : ↥(L2ZeroMean P))
         (hg : (g : ↥(L2ZeroMean P)) ∈
           Submodule.span ℝ T_set.carrier),
       WeakConverges
         (fun n : ℕ =>
           (MeasureTheory.Measure.pi



                                                 34
       (fun _ : Fin n =>
         (chosenFamily g hg).curve
           ((Real.sqrt n)⁻¹))).map
     (fun X : Fin n → Ω =>
       Real.sqrt n •
         (T_n n X
           - ψ ((chosenFamily g hg).curve
               ((Real.sqrt n)⁻¹)))))
L)




                                    35
