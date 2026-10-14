                                                          P3: Joint Program-and-Proof Planning
                                                               for Verified Code Generation


                                                     Zenan Li1,∗       Ziran Yang2,∗       Peiyang Song3       Zhaoyu Li4       Kaiyu Yang1
                                                          1             2
                                                              Apodex        Princeton University 3 Caltech      4
                                                                                                                    University of Toronto
                                                                                        ∗
                                                                                          Equal contribution



                                                                                            Abstract
                                                     Verified code generation asks a large language model (LLM) to generate both
                                                     an executable program and a machine-checkable proof that the program meets a
arXiv:2608.09277v1 [cs.AI] 10 Aug 2026




                                                     formal specification, promising software that is correct by construction. The de
                                                     facto workflow decouples the two halves of the problem: first synthesize a program,
                                                     then attempt to prove it correct. We observe that this sequential pipeline can be both
                                                     ineffective and inefficient in practice. A program generated without anticipating
                                                     its proof can be subtly incorrect or structurally difficult to verify, forcing the LLM
                                                     into brittle repair loops that alternate between patching the code and patching the
                                                     proof. Inspired by Dijkstra’s view that a program and its correctness argument
                                                     should be developed hand in hand, we propose P3 , an LLM-based agentic workflow
                                                     that first derives a unified program-and-proof plan from the specification, then
                                                     elaborates the implementation and proof scaffold under this shared plan. To evaluate
                                                     verified code generation in realistic settings, we further introduce Lean4Commit0, a
                                                     repository-derived, library-level benchmark built by extracting core APIs from real-
                                                     world software repositories and translating their requirements, including relational
                                                     specifications across APIs, into Lean tasks. Using four frontier LLM backends,
                                                     we evaluate P3 on Verina, AlgoVeri, and our Lean4Commit0 benchmark, where
                                                     it achieves the highest solve rate in every benchmark–model setting. Compared
                                                     with the stronger baseline, it improves solve rates by 4.6–11.2 percentage points
                                                     and reduces per-task API cost by up to roughly 40% and wall-clock time by up to
                                                     roughly 37% on the difficult subset of each benchmark. A targeted ablation further
                                                     shows gains of 3.3–8.3 points over implementation-only planning, isolating the
                                                     benefit of planning the program and proof jointly.


                                         1    Introduction
                                         Recent progress in large language models (LLMs) has pushed code generation beyond autocomplete-
                                         style snippets to full functions, files, and repository-level development through agentic workflows [1–
                                         3]. At the same time, formal systems such as Lean 4 [4] have become practical environments for
                                         writing executable programs together with machine-checkable proofs of their correctness [5, 6].
                                         The intersection of these two trends gives rise to verified code generation [7, 8]: given a formal
                                         specification, an LLM is asked to synthesize both an executable implementation and a proof that the
                                         implementation satisfies the specification. If the formal system accepts both artifacts, the generated
                                         program carries a machine-checked correctness guarantee that goes beyond finite test coverage,
                                         substantially reducing the burden of reviewing, trusting, and composing LLM-written software.
                                         Despite this promise, existing verified-code-generation pipelines often follow a sequential program-
                                         then-proof schedule: the LLM first commits to a concrete implementation, after which a separate
                                         proving stage, ranging from automated solvers to LLM-based provers, is invoked to discharge the
                                         resulting proof obligations [9–13]. When verification fails, the workflow enters a patch-and-retry

                                         Preprint.
  @ Spec σ                        Ð Program π                    ¥ Proof κ                      u Verifier
  what to build                   write the code                 prove correctness              check code + proof


 (a) Program-then-proof                                              L patch & retry

                  q Artifacts meet late at verification time; mismatches trigger coupled code/proof repair.




                                                                 Ð Program π
                                                                 elaborate code
  @ Spec σ                        ¨ Plan ρ                                                      u Verifier
  what to build                   shared sketch                                                 check code + proof
                                                                 ¥ Proof κ
 (b) P3 (Our proposed framework)                                 elaborate proof


      ¥ Artifacts agree by construction via the shared plan; consistency is designed in, not repaired afterward.


Figure 1: Our proposed framework. Top: the program-then-proof pipeline commits to an implemen-
tation before the proof’s structure is known, so the two artifacts only meet at verification time and
mismatches trigger coupled code/proof repair. Bottom: our workflow first settles a shared structural
plan, then elaborates the program and proof scaffold against the same plan, so that consistency holds
by construction rather than being recovered by post-hoc repair.

loop. This ordering creates both effectiveness and efficiency bottlenecks. First, an implementation
generated without anticipating its proof may lack the invariant or induction structure needed for a
clean correctness argument. In such cases, local repair is unlikely to recover a proof-friendly structure
that was never planned. Second, even when a verified solution is eventually found, much of the token
and time budget may be spent exploring repairs that are doomed by the initially committed program.
To address these limitations, we propose P3 , a joint program-and-proof planning framework for
verified code generation in Lean 4, ensuring that the implementation and proof are structurally
consistent before either artifact is elaborated. The underlying principle is classical. Programs and
their correctness arguments have long been viewed as co-designed artifacts: Dijkstra [14] argued
that proof structure and program structure mutually constrain each other, and therefore that the two
should be developed “hand in hand”. We adapt this principle to an agentic setting by having the
model first construct a shared high-level plan for both artifacts. This plan specifies the decomposition
that carries the computation, the intermediate assertions or invariants that connect the precondition to
the postcondition, the induction or case analysis that structures the proof, and the auxiliary lemmas
required along the way. The implementation and proof scaffold are then elaborated against this same
plan, with remaining proof leaves discharged using Lean 4’s feedback. As a result, the two artifacts
agree structurally from the start, rather than being reconciled through post-hoc repair (Figure 1).
To evaluate verified code generation beyond textbook settings, we also introduce Lean4Commit0, a
benchmark derived from real open-source software. Existing benchmarks for verified code generation
primarily consist of textbook algorithms and competitive-programming tasks, which are valuable
but often differ from the APIs and behaviors encountered in production software. Lean4Commit0 is
built from 108 real-world open-source libraries spanning four mainstream ecosystems: Python, Rust,
C/C++, and Java. For each library, we select several core APIs and encode their expected behavior
as Lean implementation placeholders and correctness theorems, including relational specifications
that connect multiple API calls. To ensure specification quality, each specification passes a three-
stage validation pipeline: a reference-satisfaction check verifies that the behavior of the original
implementation is consistent with the Lean specification; a mutation-rejection check tests whether the
specification rejects behavior-changing mutants; an LLM review flags specifications that are trivial or
irrelevant.
We evaluate P3 on Verina [7], AlgoVeri [15], and Lean4Commit0 with four frontier LLM backends,
comparing against a plain Lean-agent baseline and a program-then-proof baseline. Across all 12
(benchmark, model) cells, P3 achieves the highest solve rate, with a 4.6–11.2 percentage-point
gain over the stronger primary baseline in each setting; on difficult tasks, it also reduces per-task
cost and time by up to 40% and 37%, respectively. A targeted ablation with implementation-only


                                                             2
planning yields a further controlled comparison: joint program-and-proof planning improves solve
rate by 3.3–8.3 points. A case study on left-leaning red-black tree deletion further shows that the
program-then-proof baseline either fails after 6,344 lines under the structural-deletion commitment
or succeeds only with redundant rebuild invariants in 1,176 lines, whereas P3 compares the plans
before committing and solves the task in 1,105 lines.


2     Problem

The input to verified code generation is a formal specification σ = (P, Q) for a target function, where
P is a precondition on the function’s inputs and Q is a postcondition relating those inputs to the
outputs. Given σ, the goal is to construct two artifacts: a program π implementing the function,
and a certificate κ from which a verifier can establish that, on every input satisfying P , running
π terminates and returns an output satisfying Q. A task is solved iff a designated verifier accepts
(σ, π, κ). This setting differs from test-based code generation in that correctness must be established
for all admissible inputs rather than for a finite collection of examples. The concrete form of κ
depends on the verification backend. In SMT-based systems, such as Dafny [16], F⋆ [17], and
Verus [18], κ is a collection of program annotations whose verification conditions are discharged
by an SMT solver. In interactive theorem proving settings, such as Lean 4 [4], Rocq [19], and
Isabelle/HOL [20], κ is an explicit proof term or tactic script checked by the prover’s kernel.
Although these backends expose different certificate languages, representative LLM agents largely
follow the same sequential schedule. In Verus, systems such as AutoVerus [11], VeruSAGE [12],
and ExVerus [13] first commit to a program and then repair its annotations; Lean 4 systems such as
WybeCoder [9] and Goedel-Code-Prover [10] follow the analogous loop over tactic scripts. Across
both settings, the LLM agent first commits to an implementation, then searches for a compatible
certificate, using verifier feedback to patch the certificate and, when necessary, revise the program.
The limitation is that the implementation largely determines the shape of the certificate. A structurally
inconvenient program can force the LLM to establish auxiliary lemmas that are not directly suggested
by the specification, making certificate search unnecessarily difficult. This coupling between code
structure and proof structure is especially visible in Lean 4 benchmarks such as Verina [7] and
AlgoVeri [15], where each task provides a function signature together with pre- and postconditions,
and leaves both the implementation and proof as open placeholders.
As a running example, consider the task of computing the maximum element of a non-empty list of
integers, together with a theorem stating that the returned value belongs to the list and upper-bounds
every element. Two natural implementations are possible (see Appendix D for the full Lean source of
both versions and their proofs):

    -- (A) structural recursion                                 -- (B) accumulator fold
    def listMax : (xs : List Int) → xs ̸= [] → Int              def listMax (xs : List Int)
      | [x],     _ => x                                             (h : xs ̸= []) : Int :=
      | x::y::t, _ => max x (listMax (y::t) (by simp))            xs.foldl max xs.head!

Both implementations compute the same value, but they induce very different proof obligations.
Version (A) admits an induction that mirrors the postcondition: membership and upper-bound facts
are proved case by case, with the induction hypothesis applied directly to the tail. Version (B),
although shorter and arguably more idiomatic, is in fact substantially harder to verify against the
stated specification. A proof cannot proceed directly from the original postcondition; it must first
generalize to an accumulator invariant such as

    lemma foldl_max_gen (init : Int) (ys : List Int) :
        ys.foldl max init ∈ init :: ys ∧ ∀ z ∈ init :: ys, z ≤ ys.foldl max init

This lemma is then specialized to the non-empty input xs to recover the desired theorem. The
universal quantification over arbitrary init has no counterpart in the specification: it is an invariant
of the fold, not of the maximum itself. Thus, after committing to Version (B), the LLM agent must
either discover this stronger invariant under the fixed implementation or rewrite the program toward
Version (A), discarding any proof work already accumulated. The failure mode is therefore structural:


                                                   3
the sequential schedule commits the implementation before identifying the proof structure most
natural for the specification, often leading to wasted certificate search.


3     Methodology

Motivation. The central limitation of the program-then-proof paradigm is the potential misalignment
between program and proof construction. A program may satisfy the specification extensionally, yet
expose a structure that is difficult to verify. Conversely, optimizing only for proof simplicity can
produce implementations that are inefficient, unnatural, or fail to capture the intended algorithm. For
example, consider searching for a target in a sorted array. Binary search has the desired asymptotic
behavior, but its proof requires reasoning about intervals, index bounds, and preservation of the search
invariant across recursive calls. A linear scan is much easier to verify by induction, but it ignores the
sortedness assumption and gives a weaker algorithmic result. This tension motivates planning the
program and proof jointly, rather than generating one first and forcing the other to fit afterward.
Framework. Given a formal specification σ = (P, Q), our LLM agent, P3 , runs in two stages.
(1) Planning: P3 proposes candidate plans based on σ and selects a plan ρ containing a program
sketch aligned with a compatible proof sketch. (2) Elaboration: conditioned on ρ, P3 synthesizes the
program π and a proof scaffold that mirrors ρ (e.g., induction principles, case splits, and intermediate
lemmas). It then fills in the remaining proof details, using Lean feedback for repair. On success, Lean
certifies the proof κ of correctness for (σ, π); on failure, P3 classifies the error as elaboration-level or
plan-level and invokes the corresponding repair procedure. Within a single agent harness, planning
and elaboration run as two stages with distinct prompts and tool contexts; the main agent (running the
named backend) handles planning, and for elaboration may either continue itself or dispatch cheaper
subagents. The concrete templates are given in Appendix E.

3.1   Joint Program-and-Proof Planning

A plan ρ records four commitments that the program and proof must later realize: (i) the formal
contract and any algorithmic or asymptotic instruction; (ii) the program decomposition, including the
recursion variable, branch structure, data representation, auxiliary routines, and termination measure;
(iii) the concrete library functions and existing lemmas on which elaboration will rely; and (iv) the
proof obligations, including the bridging predicate, induction or case structure, and statements of
auxiliary lemmas. Together, these choices specify the structural shape that the program and proof
must share.
The planning agent validates the candidate plan at the sketch level. This validation is informal but
explicit: the program sketch must meet the task instructions, including any algorithmic constraints;
the proof sketch must explain why the chosen decomposition preserves the bridging predicate and
why that predicate entails Q; and any nontrivial strengthening of Q needed by the proof must be
named as an auxiliary lemma rather than left implicit. Only after this validation does the agent pass
the selected plan to elaboration.
Compact procedure.
1. Propose candidate plans from σ, each containing all four commitments above.
2. Reject a candidate if its program sketch violates the instruction, its decomposition does not
   preserve the bridging predicate, or the predicate does not entail Q.
3. Select a surviving candidate whose decomposition exposes the smallest anticipated proof burden,
   and freeze its structural commitments as ρ.
4. Elaborate (π, κ) under ρ; repair local errors in place, but return to Step 1 if elaboration requires an
   unplanned algorithm, invariant, or structural lemma.
In the running listMax example, planning exposes the structural tradeoff between Version (A) and
Version (B) before the agent commits to code. Version (A) uses structural recursion on xs (split [x]
vs. x :: y :: t) and lets the postcondition itself serve as the bridging predicate. Version (B) takes
List.foldl, which forces the bridging predicate to range over a universally quantified accumulator,
stated explicitly as the lemma foldl_max_gen. This generalized accumulator invariant is not a surface
fact about the maximum function; it is a proof obligation introduced by the choice to implement the
function with List.foldl.


                                                     4
If the fold choice is made only as code, the agent sees the invariant only after proof search fails. If the
same choice is represented in the plan, the invariant appears immediately as part of the proof sketch,
before any tactic script is written. The planner can therefore compare version (A) and version (B) at
the level of sketches: version (A) aligns the computation with the postcondition directly, whereas
version (B) commits the agent to proving and later specializing an auxiliary accumulator lemma.
This comparison is lightweight because plans differ only in their decomposition, bridging predicate,
and named auxiliary lemmas, not in full Lean terms or tactic scripts. Although listMax is our
running example, the same kind of sketch-level comparison applies to other structural choices as well,
including case splits, collection combinators, and relational specifications across multiple functions.



3.2   Plan-Guided Elaboration

Once a plan ρ is selected, elaboration turns its sketches into concrete Lean artifacts. For programs,
the agent writes an implementation whose control structure follows the decomposition fixed by ρ: the
recursive argument, case split, collection combinator, or auxiliary routine is not chosen again during
coding. For proofs, the agent writes a certificate scaffold with the same shape: the target theorem,
the auxiliary lemma statements named by the plan, and the top-level proof structure that invokes the
planned induction, case analysis, or lemma applications. At this point the program is concrete, while
the scaffold may still contain local gaps, represented as sorry, at the leaves of the planned argument.
Proof completion then becomes a local elaboration problem rather than an unconstrained proof search
problem. The agent asks Lean to elaborate the file, reads the resulting goals and errors, and fills the
remaining proof leaves or auxiliary lemmas while preserving the structure fixed by ρ. For example, if
ρ specifies structural recursion over a list, the agent closes the cases exposed by that recursion; if ρ
specifies a fold with an accumulator invariant, the agent works on the accumulator lemma and its
specialization rather than inventing a different induction principle inside the main proof.
This completion step can be implemented by proof-tree search, test-time scaling over candidate
tactics, or an agentic Lean-feedback loop. In our Lean 4 setting, LSP/MCP feedback provides
localized goals and diagnostics without rebuilding the search context from scratch. The verifier still
has the final authority: the task is solved only when Lean accepts the full pair (π, κ) against σ.



3.3   Benefits of Plan-Guided Generation

The plan turns the verifier’s binary feedback into structured guidance about where a failure lives
and what progress can be salvaged. An elaboration-level failure is one whose error localizes under
the current plan, such as a missing tactic in one branch, an unmet preservation step for the bridging
predicate, or a small implementation mismatch in π. The agent repairs the localized artifact while
keeping the rest of the plan and the other side of the pair intact. A plan-level failure is signaled when
repeated local repairs cannot close the obligations under ρ, or when Lean exposes that the bridging
predicate is too weak, for example because completion requires an algorithm, invariant, or structural
lemma that the plan did not name. In that case the agent retreats to planning, revises ρ, and only
then re-elaborates the program and certificate against the new plan. Thus the plan serves as a single,
well-defined point of retreat: when nothing under it works, the agent moves up one level rather than
thrashing between code edits and proof edits, which is the failure mode that drives the efficiency gap
of program-then-proof pipelines.
This planning-and-elaboration separation also changes the model-allocation problem. Conceptu-
ally, the high-level reasoning load is concentrated in planning, where the agent must choose the
decomposition, identify the bridging predicate, and decide which auxiliary lemmas make the code
sketch and proof sketch compatible. Once those choices are fixed, elaboration is a more constrained
implementation task: the agent is asked to realize an agreed-upon structure in Lean, not to rediscover
the structure from verifier failures. In practice, the main agent uses the named backend for planning,
and for elaboration steps that it deems constrained enough it may dispatch cheaper subagents rather
than handle them itself. This division is not part of the trusted base: Lean still checks the final artifact,
and an elaborator can only succeed by producing code and proofs accepted by the kernel.


                                                     5
4     Benchmark
Lean4Commit0 extends the single-function setting to library tasks in which several APIs are jointly
constrained by relational postconditions. Existing Lean 4 benchmarks for verified code generation,
including Verina [7], Clever [21], and AlgoVeri [15], draw most of their tasks from textbooks and
competitive programming. These tasks are typically short, self-contained, and centered on a single
function whose behavior is captured by one or two arithmetic or list invariants. Real software,
however, has a different texture: state that is shared across several APIs, ordering and consistency
properties that relate multiple operations, and edge cases that arise from actual usage rather than from
a one-line problem statement. Without benchmark coverage of these patterns, claims about verified
code generation remain hard to interpret for the kinds of code developers actually ship. To close this
gap, and inspired by Commit0 [22], we present Lean4Commit0: a benchmark that extracts Lean 4
verified-generation tasks from 108 real-world open-source libraries.

4.1   Benchmark Construction

The source libraries span four ecosystems: 65 Python, 17 Rust, 15 C/C++, and 11 Java. They cover
a wide range of domains, including cryptographic primitives, data structures, web and network
frameworks, parsers, schedulers, and game emulators. From each library we select several core
APIs, defined as the user-facing entry points to that library’s main data structures. Each selected
API is encoded as a triple of (i) a Lean function signature with body sorry, (ii) a postcondition
predicate, and (iii) a correctness theorem with proof sorry. When the intended semantics ties several
APIs together, we additionally add relational specs: theorems whose statement quantifies over the
joint behavior of two or more functions. Each library forms one task; across the 108 libraries, the
benchmark contains 511 implementation placeholders and 519 theorem placeholders.
For example, Fabric is a Python library for SSH-based deployment and remote execution;
Lean4Commit0 models core configuration logic from its API. We extract operations such as
Config.set and Config.get, where configuration entries carry precedence levels from defaults to
runtime overrides. Beyond single-API behavior, Lean4Commit0 adds relational specifications that
connect operations across calls: after setting key k to value v, a subsequent lookup of k returns some
v; and if the same key is set at a lower level and then a higher level, get returns the higher-precedence
value. These properties cannot be discharged by reasoning about set or get in isolation. The proof
must connect updates to later queries and respect the precedence ordering. The full encoded Lean
task appears in Appendix G.

4.2   Specification Quality Pipeline

Repository-grounded specifications must be adequate with respect to the intended library behavior,
but this adequacy cannot be checked directly: for real libraries, the intended behavior is distributed
across source code, tests, documentation, and usage conventions rather than given as a complete
formal oracle [23, 24]. Moreover, the available executable evidence, such as source code and tests,
lives in the original project language rather than in Lean, preventing direct Lean-level adequacy
checking. Therefore, Lean4Commit0 uses an automated filtering pipeline to detect three common
and actionable failure modes:
• Unsatisfiable: no implementation can satisfy the stated theorem obligations.
• Underconstrained: behavior-changing implementations can still satisfy the stated properties.
• Vacuous: the stated properties are trivial or irrelevant to the target API behavior.
To detect unsatisfiable specifications, we use the reference implementation and test cases from the
original project as executable evidence. For each test input, we run the reference implementation to
obtain the reference output, then check in Lean whether the resulting input-output pair satisfies the
corresponding pre/postcondition or relational specification. To detect underconstrained specifications,
we apply behavior-changing mutations to the reference implementation and run the same test inputs
again. The mutated input-output pairs should violate the specification; if they still satisfy it, the spec
is too weak to distinguish the mutant from the reference behavior. Formal counterexample generation
likewise uses symbolic mutation to construct Lean-checkable negative instances [25]; our quality gate
instead mutates executable library implementations and asks whether candidate API specifications
reject their changed behavior.


                                                    6
Table 1: Lean4Commit0 summary after the specification quality pipeline. Reference satisfaction is a
hard admissibility condition; the quality score combines mutation rejection and LLM review.

                                        Placeholders (#)               Quality metrics (%)
           Language    Libraries
                                   Code     Theorem        Total   Mutation   Review    Quality
           Python             65     314         314        628        98.7     82.5         90.6
           Rust               17      88          73        161        98.2     86.2         92.2
           C/C++              15      58          72        130        98.7     80.9         89.8
           Java               11      51          60        111        99.0     80.3         89.7
           All               108     511         519    1,030          98.6     82.7         90.7

To detect vacuous specifications, we invoke an LLM-based review with explicit rules: the specification
should not be provable by trivial tactics such as rfl or decide, should not be a tautology or duplicate
of another statement, and should depend on the functions being implemented. The LLM reviewer
finally assigns a score on a 1–5 scale based on these criteria and flags specifications that add little or
no constraint on the target API behavior.
To automate the specification quality-assurance pipeline end to end, Lean4Commit0 introduces an
LLM agent that orchestrates the components above. For example, we provide various mutation tools
for the supported source languages; the agent selects and invokes the appropriate tool for each project
to obtain behavior-changing mutants. The agent also bridges the language gap between the reference
project and Lean: since the reference projects are written in Python, Rust, C/C++, or Java while the
specifications are written in Lean, it generates language-specific shims that run the reference code,
collect inputs and outputs, and serialize them as Lean values.
We treat reference satisfaction as a hard admissibility condition: every reference input-output pair
must satisfy the corresponding Lean specification. For specifications that pass this check, we compute
an aggregate quality score from mutation rejection and LLM review. Let Mutation denote the
mutation rejection rate, i.e., the fraction of behavior-changing mutants rejected by the specification,
and let Review denote the LLM review score for vacuity and semantic relevance, normalized to a
percentage as Review(σ) = score(σ)/5 × 100%. We define
                        Quality(σ) = 0.5 · Mutation(σ) + 0.5 · Review(σ).
We iteratively refine each task and admit it only if reference satisfaction is complete and the aggregate
score is at least 80%. Table 1 summarizes the resulting benchmark scale and specification-quality
metrics after this pipeline. All 108 libraries clear this threshold; the mean score across the benchmark
is 90.7%, and ten libraries reach 100%.

5     Experiments
5.1   Experimental Setup

We evaluate whether the proposed framework improves verified code generation along two axes:
effectiveness, measured by how often the agent produces a Lean-accepted implementation and proof,
and efficiency, measured by how much repair work is needed before acceptance.
Benchmarks. We evaluate on Verina [7] (189 tasks), AlgoVeri [15] (77 tasks), as well as the
new Lean4Commit0 benchmark. Verina and AlgoVeri test single-function verified generation over
textbook-style algorithmic tasks, while Lean4Commit0 tests repository-derived, library-level task
bundles, including relational specifications across APIs. Because Verina and AlgoVeri do not
impose explicit complexity requirements, agents can sometimes satisfy the formal specification
with impractical implementations, such as exponential-time algorithms. We therefore augment each
task with a natural-language instruction specifying the expected algorithmic strategy or asymptotic
complexity, and apply the same instruction to all evaluated systems.
Baselines. We compare the proposed framework against two primary agent settings. Existing
proof-search and annotation-repair systems assume a fixed implementation, so they do not provide
a direct end-to-end orchestration baseline (Section 6). The first is a plain Lean-agent setting: the
agent receives the formal specification and Lean tools [26], but no task-specific skill or strategy
prompt. The second is a skill-based program-then-proof setting: the agent is guided to first produce an


                                                    7
Table 2: Solve rate (%) across backend models, methods, and benchmarks. A task is counted as
solved if the produced solution satisfies the instruction and passes Lean’s checker. Higher is better.

      Benchmark             Model                       P LAIN           S EQ            P3       ∆
                            Codex-GPT-5.5                 72.0           67.7           77.2    +5.2
                            Gemini-3-Pro                  59.3           60.8           72.0   +11.2
      Verina
                            Claude-Sonnet-4.6             64.0           61.9           73.0    +9.0
                            Claude-Opus-4.7               68.8           68.3           74.6    +5.8
                            Codex-GPT-5.5                 36.4           33.8           44.2    +7.8
                            Gemini-3-Pro                  33.8           31.2           39.0    +5.2
      AlgoVeri
                            Claude-Sonnet-4.6             35.1           32.5           40.3    +5.2
                            Claude-Opus-4.7               39.0           40.3           48.1    +7.8
                            Codex-GPT-5.5                 11.1           13.0           18.5    +5.5
                            Gemini-3-Pro                   9.3           11.1           15.7    +4.6
      Lean4Commit0
                            Claude-Sonnet-4.6             10.2           13.0           17.6    +4.6
                            Claude-Opus-4.7               13.9           17.6           22.2    +4.6
           Table 3: Implementation-planning ablation with Claude-Opus-4.7 (solve rate, %).

                       Benchmark        P LAIN   S EQ      P LAN -S EQ     P3      ∆
                       Verina             68.8   68.3            69.8     74.6   +4.8
                       AlgoVeri           39.0   40.3            44.8     48.1   +3.3
                       Lean4Commit0       13.9   17.6            13.9     22.2   +8.3


implementation and then generate and repair the proof [27]. Our framework instead equips the agent
with a planning skill: before elaboration, it selects a plan ρ containing a mutually consistent program
sketch and proof sketch, and then writes both artifacts under that plan. For a targeted ablation, we
additionally evaluate P LAN -S EQ, which plans implementation-side choices but is forbidden from
anticipating invariants, proof decomposition, induction strategies, or proof lemmas before running
the program-then-proof pipeline.
Settings. We instantiate each agent setting with four frontier backend configurations: Codex-GPT-5.5,
Gemini-3-Pro, Claude-Sonnet-4.6, and Claude-Opus-4.7, invoked through their native command-
line interfaces under a fixed harness. Each run is given a per-task API budget of 30.0 USD and a
wall-clock time limit of 180 minutes. All runs execute inside the same Docker image with Lean
4.28.0. To isolate the effect of the agent setting, all runs use the same task instructions, API budget,
time limit, and maximum feedback-iteration budget. Each (task, model, method) configuration is run
once, so rates aggregate over tasks but do not estimate within-task variance; the complete prompts,
harness, scripts, pinned environment, and run metadata are available at https://figshare.com/s/
2ab7020cacaffcf0d258.

5.2     Main Results

Table 2 reports solve rates, where a task counts as solved only when the produced solution both
passes the Lean checker and satisfies the algorithmic instruction. P3 attains the best solve rate on
every (benchmark, model) cell, with the absolute gain over the stronger baseline (∆) ranging from
+4.6 to +11.2 percentage points. The baselines split by benchmark type: P LAIN is competitive on
textbook-style Verina and AlgoVeri, whereas S EQ consistently beats P LAIN on repository-grounded
Lean4Commit0 by 1.8–3.7 points. The positive ∆ across all three regimes (solve rates 59–77% on
Verina, 31–48% on AlgoVeri, 9–22% on Lean4Commit0) shows that joint planning improves over
the two primary baselines regardless of benchmark difficulty.
Table 3 isolates joint planning from generic implementation planning: P3 outperforms P LAN -S EQ
by 3.3–8.3 points. P LAN -S EQ helps on Verina and AlgoVeri but hurts on Lean4Commit0, where
independently reasonable API implementations may be difficult to connect under a relational theorem
unless they are planned against their shared proof obligations.
Plan viability. Across all 189 Verina traces for P3 with Claude-Opus-4.7, 131 of 141 successes
(92.9%) retain the initial plan, while only 4 of 48 failures (8.3%) are attributed to an inadequate plan;
Appendix I reports the full breakdown and caveat that retention is only a proxy for proof-burden
prediction accuracy.


                                                   8
To compare efficiency on tasks that require non-trivial search, we restrict to the top 25% of tasks by
mean cost across the three methods (n=48 on Verina, n=20 on AlgoVeri, n=27 on Lean4Commit0).
Appendix Table 5 reports per-task cost and wall-clock time on this difficult subset. P3 is the cheapest
and fastest method on every (benchmark, model) cell, reducing cost by 3.0–39.6% and wall-clock
time by 3.1–37.2% relative to the better baseline for each metric. The largest savings appear on
Verina and AlgoVeri, while Lean4Commit0 leaves less room for time reduction because all three
methods often run close to the per-task limit. On the all-solved intersection, P3 remains broadly
comparable to the baselines, with some visible planning overhead on easier cells (Appendix L).
Trace inspection attributes much of S EQ’s cost to full-restart repair: after local repairs fail under
the committed program, the agent rewrites both artifacts. P3 checks structural consistency before
elaboration and restarts less often; Appendix K gives the breakdown.

5.3   Case Study

On AlgoVeri’s left-leaning red-black-tree deletion task, S EQ’s structural route reaches 6,344 lines
without closing, while rebuild closes in 1,176 lines only after inheriting redundant invariants. P3
compares both sketches, recognizes that rebuild reduces the value-set goal to list permutation, and
closes it in 1,105 lines and about 34 minutes.
A repository-derived counterpart is M EMCHR, a three-API relational task solved only by P3 under
the same backend and budget (Appendix H).
Scope and limitations. Evidence is restricted to Lean 4, closed-source backends, Python-skewed
core APIs, imperfect specification gates, and single runs; transfer to other verifiers, open models, and
whole systems remains open (Appendix C).

6     Related Work
Verified code generation. Proof-carrying code [28] cast safe execution as a producer-consumer
protocol with a trusted checker; LLM-driven verified code generation instead makes the LLM
the producer, shifting the difficulty from certificate checking to certificate construction. Across
SMT and ITP systems [18, 16, 17, 4, 19, 20], recent agents construct or repair certificates after the
implementation is fixed [11–13, 29–31, 9]. Proof-search systems add decomposition before local
proving [10, 32] or scale neuro-symbolic search to system-level developments [33], but still begin
after the program and obligations are fixed; theorem-proving priors [34–37] leave that schedule
unchanged. The Floyd–Hoare and refinement-synthesis traditions [38, 39, 14, 40, 41] long argued
instead that program structure and correctness argument should be developed together; our workflow
ports this discipline into LLM-driven verified code generation, with the plan playing the role of the
inductive assertion or refinement schema before either the program or the certificate is elaborated.
Explicit planning has also been shown to help LLM agents on unverified code generation [42, 43];
the new requirement in our setting is that the plan align the program decomposition with the proof
decomposition the verifier will demand.
Benchmark. Existing benchmarks are either short, problem-level verified-generation tasks [7, 21, 15,
44] or annotation reconstruction over fixed programs [45, 11, 12]. Lean4Commit0 differs on three
axes from prior verified-code-generation benchmarks (see Appendix F for a side-by-side comparison):
each task is a library-level bundle of core APIs derived from a real GitHub project rather than a single
function; specifications include relational properties across multiple APIs of the same library; and
admission is gated by a uniform automated pipeline (reference satisfaction, mutation rejection, LLM
review), so reported solve rates can be read against a known floor on spec strength.

7     Conclusion
Committing to implementation structure before proof structure induces brittle repair loops; P3 instead
fixes a shared decomposition, bridging predicate, and auxiliary lemmas before elaboration, routing
feedback to local repair or explicit replanning. Lean4Commit0 complements this workflow with
repository-derived, library-level tasks, relational API specifications, and a uniform quality pipeline,
moving verified generation toward correctness arguments planned with the code rather than recovered
after the fact.


                                                   9
References
 [1] Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming Zhang, and
     Yiling Lou. Large language model-based agents for software engineering: A survey. ACM
     Transactions on Software Engineering and Methodology, 2024.

 [2] Yihong Dong, Xue Jiang, Jiaru Qian, Tian Wang, Kechi Zhang, Zhi Jin, and Ge Li. A survey on
     code generation with llm-based agents. arXiv preprint arXiv:2508.00083, 2025.

 [3] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. A survey on large language
     models for code generation. ACM Transactions on Software Engineering and Methodology, 35
     (2):1–72, 2026.

 [4] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In International Conference on Automated Deduction, pages 625–635. Springer,
     2021.

 [5] Anne Baanen, Matthew Robert Ballard, Johan Commelin, Bryan Gin-ge Chen, Michael Roth-
     gang, and Damiano Testa. Growing mathlib: maintenance of a large scale mathematical library.
     In International Conference on Intelligent Computer Mathematics, pages 51–70. Springer, 2025.

 [6] Clark Barrett, Swarat Chaudhuri, Fabrizio Montesi, Jim Grundy, Pushmeet Kohli, Leonardo
     de Moura, Alexandre Rademaker, and Sorrachai Yingchareonthawornchai. Cslib: The lean
     computer science library. arXiv preprint arXiv:2602.04846, 2026.

 [7] Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kasriel, Kaiyu Yang, and Dawn Song. Verina:
     Benchmarking verifiable code generation. arXiv preprint arXiv:2505.23135, 2025.

 [8] Quinn Dougherty and Ronak Mehta. Proving the coding interview: A benchmark for formally
     verified code generation. In 2025 IEEE/ACM International Workshop on Large Language
     Models for Code (LLM4Code), pages 72–79. IEEE, 2025.

 [9] Fabian Gloeckle, Mantas Baksys, Darius Feher, Kunhao Zheng, Amaury Hayat, Sean B. Holden,
     Gabriel Synnaeve, and Peter O’Hearn. Wybecoder: Verified imperative code generation. arXiv
     preprint arXiv:2603.29088, 2026.

[10] Zenan Li, Ziran Yang, Deyuan He, Haoyu Zhao, Andrew Zhao, Shange Tang, Kaiyu Yang,
     Aarti Gupta, Zhendong Su, and Chi Jin. Goedel-code-prover: Hierarchical proof search for
     open state-of-the-art code verification. arXiv preprint arXiv:2603.19329, 2026.

[11] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong,
     Chris Hawblitzel, Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. Autoverus: Automated proof
     generation for rust code. Proceedings of the ACM on Programming Languages, 9(OOPSLA2):
     3454–3482, 2025.

[12] Chenyuan Yang, Natalie Neamtu, Chris Hawblitzel, Jacob R Lorch, and Shan Lu. Verusage: A
     study of agent-based verification for rust systems. arXiv preprint arXiv:2512.18436, 2025.

[13] Jun Yang, Yuechun Sun, Yi Wu, Rodrigo Caridad, Yongwei Yuan, Jianan Yao, Shan Lu,
     and Kexin Pei. Exverus: Verus proof repair via counterexample reasoning. arXiv preprint
     arXiv:2603.25810, 2026.

[14] Edsger W. Dijkstra. A Discipline of Programming. Prentice-Hall, Englewood Cliffs, NJ, 1976.

[15] Haoyu Zhao, Ziran Yang, Jiawei Li, Deyuan He, Zenan Li, Chi Jin, Venugopal V Veeravalli,
     Aarti Gupta, and Sanjeev Arora. Algoveri: An aligned benchmark for verified code generation
     on classical algorithms. arXiv preprint arXiv:2602.09464, 2026.

[16] K Rustan M Leino. Dafny: An automatic program verifier for functional correctness. In
     International conference on logic for programming artificial intelligence and reasoning, pages
     348–370. Springer, 2010.


                                                10
[17] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon
     Forest, Karthikeyan Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, et al.
     Dependent types and multi-monadic effects in F⋆ . In Proceedings of the 43rd annual ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages, pages 256–270,
     2016.
[18] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon
     Howell, Bryan Parno, and Chris Hawblitzel. Verus: Verifying rust programs using linear ghost
     types. Proceedings of the ACM on Programming Languages, 7(OOPSLA1):286–315, 2023.
[19] Yves Bertot and Pierre Castéran. Interactive Theorem Proving and Program Development:
     Coq’Art: The Calculus of Inductive Constructions. Springer, 2004.
[20] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL: A Proof Assistant
     for Higher-Order Logic, volume 2283 of Lecture Notes in Computer Science. Springer, 2002.
[21] Amitayush Thakur, Jasper Lee, George Tsoukalas, Meghana Sistla, Matthew Zhao, Stefan
     Zetzsche, Greg Durrett, Yisong Yue, and Swarat Chaudhuri. Clever: A curated benchmark for
     formally verified code generation. In The Thirty-ninth Annual Conference on Neural Information
     Processing Systems Datasets and Benchmarks Track, 2025.
[22] Wenting Zhao, Nan Jiang, Celine Lee, Justin T Chiu, Claire Cardie, Matthias Gallé, and Alexan-
     der M Rush. Commit0: Library generation from scratch. arXiv preprint arXiv:2412.01769,
     2024.
[23] Didar Zowghi and Vincenzo Gervasi. On the interplay between consistency, completeness, and
     correctness in requirements evolution. Information and Software technology, 45(14):993–1009,
     2003.
[24] Lloyd Montgomery, Davide Fucci, Abir Bouraffa, Lisa Scholz, and Walid Maalej. Empirical
     research on requirements quality: a systematic mapping study. Requirements Engineering, 27
     (2):183–209, 2022.
[25] Zenan Li, Zhaoyu Li, Kaiyu Yang, Xiaoxing Ma, and Zhendong Su. Learning to disprove: For-
     mal counterexample generation with large language models. arXiv preprint arXiv:2603.19514,
     2026.
[26] Oliver Dressler. Lean LSP MCP: Tools for agentic interaction with the Lean theorem prover, 3
     2025. URL https://github.com/oOo0oOo/lean-lsp-mcp.
[27] Cameron Freer. Lean 4 Skills: Theorem proving skill and workflow pack for AI coding agents,
     October 2025. URL https://github.com/cameronfreer/lean4-skills.
[28] George C. Necula. Proof-carrying code. In Proceedings of the 24th ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, pages 106–119, 1997.
[29] Chuanhao Yan, Fengdi Che, Xuhan Huang, Xu Xu, Xin Li, Yizhi Li, Xingwei Qu, Jingzhe Shi,
     Chenghua Lin, Yaodong Yang, Binhang Yuan, Hang Zhao, Yu Qiao, Bowen Zhou, and Jie Fu.
     Re:Form – reducing human priors in scalable formal software verification with RL in LLMs: A
     preliminary study on Dafny. arXiv preprint arXiv:2507.16331, 2025.
[30] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation
     and repair with large language models. In Proceedings of the 31st ACM Joint European
     Software Engineering Conference and Symposium on the Foundations of Software Engineering
     (ESEC/FSE), pages 1229–1241, 2023.
[31] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An
     in-context learning agent for formal theorem-proving. In International Conference on Learning
     Representations (ICLR), 2024.
[32] Ning Zhang, Nongyu Di, Zenan Li, Yuan Yao, and Xiaoxing Ma. Planning to hammer:
     Difficulty-aware decomposition for automating Rocq proofs. arXiv preprint arXiv:2606.17981,
     2026.


                                                11
[33] Baoding He, Zenan Li, Wei Sun, Yuan Yao, Taolue Chen, Xiaoxing Ma, and Zhendong Su.
     Neuro-symbolic proof generation for scaling systems software verification. In 20th USENIX
     Symposium on Operating Systems Design and Implementation (OSDI 26), pages 2533–2550,
     Seattle, WA, July 2026. USENIX Association. URL https://www.usenix.org/conference/
     osdi26/presentation/he-baoding.
[34] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer,
     Albert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language
     model for mathematics. International Conference on Learning Representations (ICLR), 2024.
[35] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda
     Li, and Xiaodan Liang. DeepSeek-Prover: Advancing theorem proving in LLMs through
     large-scale synthetic data. arXiv preprint arXiv:2405.14333, 2024.
[36] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. DeepSeek-Prover-V2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025.
[37] Thomas Hubert, Rishabh Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Erin Wieser,
     Anian Huang, Julian Schrittwieser, et al. Olympiad-level formal mathematical reasoning with
     reinforcement learning. Nature, 2025. doi: 10.1038/s41586-025-09833-y.
[38] Robert W. Floyd. Assigning meanings to programs. In J. T. Schwartz, editor, Mathematical
     Aspects of Computer Science, pages 19–32. American Mathematical Society, 1967.
[39] C. A. R. Hoare. An axiomatic basis for computer programming. Communications of the ACM,
     12(10):576–580, 1969.
[40] David Gries. The Science of Programming. Texts and Monographs in Computer Science.
     Springer, 1981.
[41] Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. Program synthesis from polymor-
     phic refinement types. In Proceedings of the 37th ACM SIGPLAN Conference on Programming
     Language Design and Implementation (PLDI), pages 522–538, 2016.
[42] Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, and
     Wenpin Jiao. Self-planning code generation with large language models. ACM Transactions on
     Software Engineering and Methodology, 2024.
[43] Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, and Ee-
     Peng Lim. Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by
     large language models. In Proceedings of the 61st Annual Meeting of the Association for
     Computational Linguistics (ACL), 2023.
[44] Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian
     Chiosa, Jure Kukovec, Alok Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, Miranda
     Zhao, Max Tan, and Max Tegmark. A benchmark for vericoding: Formally verified program
     synthesis. arXiv preprint arXiv:2509.22908, 2025.
[45] Chloe Loughridge, Qinyi Sun, Seth Ahrenbach, Federico Cassano, Chuyue Sun, Ying Sheng,
     Anish Mudide, Md Rakib Hossain Misu, Nada Amin, and Max Tegmark. DafnyBench: A
     benchmark for formal software verification. arXiv preprint arXiv:2406.08467, 2024.
[46] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In International
     conference on Tools and Algorithms for the Construction and Analysis of Systems, pages
     337–340. Springer, 2008.
[47] Haniel Barbosa, Clark Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai Mann,
     Abdalrhman Mohamed, Mudathir Mohamed, Aina Niemetz, Andres Nötzli, et al. cvc5: A
     versatile and industrial-strength smt solver. In International Conference on Tools and Algorithms
     for the Construction and Analysis of Systems, pages 415–442. Springer, 2022.



                                                 12
A    LLM Usage Disclosure
Large language models are the central object of study in this work; their use as experimental backends
(Codex-GPT-5.5, Gemini-3-Pro, Claude-Sonnet-4.6, and Claude-Opus-4.7) is fully documented in
Section 5. Beyond this experimental role, the authors used LLM-based assistants (ChatGPT and
Claude) for limited, non-substantive support during manuscript preparation, specifically polishing
English phrasing in already-drafted paragraphs, suggesting LaTeX formatting fixes, and aiding
in routine code refactoring for the evaluation harness. All research ideas, the design of P3 , the
construction of Lean4Commit0, the experimental protocol, the analysis of results, and all claims
made in this paper were conceived, verified, and written by the authors, who take full responsibility
for the final content.

B    Broader Impacts
We discuss the societal implications of P3 and Lean4Commit0 along three axes.
Intended positive impact. The work targets verified code generation, where every accepted output
ships with a machine-checked correctness proof against a formal specification. To the extent that
planning-first agent workflows raise the solve rate of such pipelines, the deployable consequence is a
higher fraction of LLM-produced software whose correctness is established by Lean’s kernel rather
than by sampled tests, which is particularly relevant for safety-critical and security-critical settings
(cryptographic primitives, parsers, configuration logic, smart-contract code). Lean4Commit0 itself
contributes a denser supply of repository-derived, library-level training and evaluation tasks for the
formal-methods community, with relational specifications across APIs that are largely absent from
prior single-function benchmarks.
Risks and misuse pathways. We do not foresee direct misuse pathways beyond the residual risks al-
ready shared with general code-generation systems, namely the acceleration of software development
in directions that may themselves be undesirable (proprietary lock-in, capability concentration, au-
tomation of work whose social distribution remains unsettled). A more specific risk is misplaced trust:
a verified artifact is correct only with respect to the shipped specification, so an under-constrained or
vacuous specification can yield code that the verifier accepts but that does not satisfy the user’s actual
intent. Lean4Commit0 mitigates this for benchmark specifications via the three-stage quality pipeline
of §4.2 (reference satisfaction, mutation rejection, LLM review), but downstream users who write
their own specifications retain full responsibility for adequacy.
Data and privacy. The benchmark surfaces only Lean specifications, reference implementations,
and tests derived from public open-source libraries already redistributed via Commit0 [22], with their
original licenses preserved; it introduces no scraping of private content, no human-subject data, and
no surveillance dimension. The released agent harness operates on this same public corpus and on
user-supplied Lean files, and does not collect or transmit user data beyond what the underlying LLM
API providers already see.

C    Limitations
We discuss the main limitations of this work along three axes.
Substrate scope. P3 and Lean4Commit0 are instantiated exclusively on Lean 4. Other verified-
programming substrates, in particular SMT-backed systems such as Dafny and Verus and dependently
typed languages such as F⋆ and Rocq, differ substantially in proof-obligation granularity, automation
profile, and the cost of failed attempts. In Verus, a shared plan would pair Rust control and data
structures with pre/postconditions, loop invariants, decreases clauses, ghost state, and SMT-facing
auxiliary lemmas; Dafny admits an analogous mapping. Local annotation or solver errors could be
repaired under the fixed plan, whereas a missing shared invariant or incompatible decomposition
would trigger replanning. This transfer is plausible but not empirically established here.
Benchmark and specification coverage. Lean4Commit0 is constructed from real GitHub libraries
surfaced through Commit0, but the extraction pipeline focuses on core APIs rather than full project
compilation, and the resulting tasks therefore underrepresent very long-horizon dependencies, com-
plex build configurations, and dynamic features that resist Lean modeling. The selected libraries


                                                   13
also reflect Commit0’s domain distribution and are skewed toward Python-origin code, which may
not generalize to systems-heavy or numerically intensive software. In addition, Lean4Commit0
specifications are constructed by our pipeline rather than fully hand-written. Each candidate is filtered
by reference satisfaction, behavior-changing mutation rejection, and LLM review, but a specification
could still be subtly under-constrained relative to a use case the reference tests do not exercise. Solve
rate is therefore a function of the specifications we ship, not of the underlying intent.
Statistical, cost, and backend considerations. Because each (task, model, method) configuration is
run once, we do not estimate within-task stochastic variance or perform formal significance testing
across all settings. The absolute costs reported are tied to the API pricing in effect at evaluation
time and should be read as relative comparisons rather than fixed budgets. Our experiments also
use four frontier closed-source LLM backends (Codex-GPT-5.5, Gemini-3-Pro, Claude-Sonnet-4.6,
Claude-Opus-4.7); it remains open whether the planning advantage transfers to open-weight models,
smaller models, or specialized fine-tuned theorem-proving models.

D     Full listMax Example
This appendix gives the complete Lean 4 source for the listMax example of §2. Both versions are
checked against the same specification Spec; the file compiles under Lean 4 with Mathlib.
Shared specification. The postcondition states that the returned value lies in the input list and
upper-bounds every element.

    def Spec (xs : List Int) (m : Int) : Prop :=
      m ∈ xs ∧ ∀ x ∈ xs, x ≤ m

Version (A): structural recursion. The induction mirrors the spec: Spec itself serves as the bridging
predicate, and each conjunct of the postcondition is discharged case by case.
    def listMaxA : (xs : List Int) → xs ̸= [] → Int
      | [a],          _ => a
      | a :: b :: rs, _ => max a (listMaxA (b :: rs) (by simp))

    theorem listMaxA_spec :
        ∀ (xs : List Int) (h : xs ̸= []), Spec xs (listMaxA xs h)
      | [a], _ => by
          refine ⟨by simp [listMaxA], ?_⟩
          intro x hx; simp at hx; subst hx; simp [listMaxA]
      | a :: b :: rs, _ => by
          have ih := listMaxA_spec (b :: rs) (by simp)
          obtain ⟨ih_mem, ih_ub⟩ := ih
          refine ⟨?_, ?_⟩
          · show listMaxA (a :: b :: rs) _ ∈ a :: b :: rs
            simp only [listMaxA]
            rcases le_total a (listMaxA (b :: rs) (by simp)) with hle | hle
            · rw [max_eq_right hle]; simp [ih_mem]
            · rw [max_eq_left hle]; simp
          · intro x hx
            simp only [listMaxA]
            rcases List.mem_cons.mp hx with rfl | hx'
            · exact le_max_left _ _
            · exact le_max_of_le_right (ih_ub x hx')

Version (B): accumulator fold. The fold cannot satisfy Spec directly. The proof must first gener-
alize over an arbitrary accumulator init, discharge the auxiliary lemma foldl_max_gen, and then
specialize init to xs.head!. The lemma is a fact about foldl, not about the maximum function.
    def listMaxB (xs : List Int) (h : xs ̸= []) : Int :=
      xs.foldl max xs.head!

    lemma foldl_max_gen :
        ∀ (init : Int) (ys : List Int), Spec (init :: ys) (ys.foldl max init)
      | init, [] => by



                                                   14
          refine ⟨by simp, ?_⟩
          intro z hz; simp at hz; subst hz; simp
      | init, y :: t => by
          have ih := foldl_max_gen (max init y) t
          obtain ⟨ih_mem, ih_ub⟩ := ih
          refine ⟨?_, ?_⟩
          · show (y :: t).foldl max init ∈ init :: y :: t
            simp only [List.foldl]
            rcases List.mem_cons.mp ih_mem with hcase | hcase
            · rw [hcase]
              rcases le_total init y with hle | hle
              · rw [max_eq_right hle]; simp
              · rw [max_eq_left hle]; simp
            · simp [hcase]
          · intro z hz
            simp only [List.foldl]
            rcases List.mem_cons.mp hz with heq | hz'
            · rw [heq]
              exact (le_max_left init y).trans
                (ih_ub _ (List.mem_cons.mpr (Or.inl rfl)))
            · rcases List.mem_cons.mp hz' with heq | hz''
              · rw [heq]
                exact (le_max_right init y).trans
                  (ih_ub _ (List.mem_cons.mpr (Or.inl rfl)))
              · exact ih_ub z (List.mem_cons.mpr (Or.inr hz''))

    theorem listMaxB_spec (xs : List Int) (h : xs ̸= []) :
        Spec xs (listMaxB xs h) := by
      match xs, h with
      | a :: rs, _ =>
          have hg := foldl_max_gen a rs
          simpa [listMaxB, List.head!, Spec] using hg


E     Prompt Templates
This appendix reproduces the methodology-defining portions of the agent skill that drives P3 ’s
planning and elaboration phases. Planning and elaboration enter the same skill at different phases of
the workflow shown below: planning halts at Phase 3 (the plan gate) and emits the plan file plus a
sketch of code and proof obligations; elaboration takes over from Phase 4 to fill the implementation
and proof bodies. For brevity we omit operational scaffolding (LSP-tool listings, subagent routing,
fallback scripts, troubleshooting, and the cross-reference index between sub-skills); these portions
are not load-bearing for the algorithmic claims of the paper. The anonymized agent harness, prompts,
benchmark, and evaluation scripts are available in the Figshare snapshot at https://figshare.com/
s/2ab7020cacaffcf0d258.
Skill description.
Lean 4 code generation & verification with a co-derivation discipline -- code and
proof sketch are derived together from a single shared reasoning trace. Use when
editing .lean files with sorry placeholders.


Core principles.
- Never modify specifications. Preconditions, postconditions, and theorem
  statements are read-only.

- Respect Instructions. A `/-! Instruction: -/` docstring or `instruction.md` is
  a hard constraint -- do not take spec-satisfying shortcuts that violate the
  stated algorithm or complexity.

- Plan commitment before writing code & proof. Code emitted in Phase 4 must
  realise the plan's `## Algorithmic idea` and `## Library support`. If you find
  yourself typing a different algorithm, that is plan failure -- revert and
  re-enter Phase 2. No silent algorithm switch at implementation time -- the
  single most common path to the spec-copy / wrong-complexity cheat.

- Standard axioms only. `propext`, `Classical.choice`, `Quot.sound`,



                                                      15
  `Lean.ofReduceBool`, `Lean.trustCompiler`. Nothing else. In particular, do not
  use `Classical.choose` on an existence proof to extract a value the
  Instruction says must be computed -- that is not an algorithm.

- Search during the plan, not during the proof. Phase 2 commits the plan to
  specific stdlib functions and mathlib lemmas (`## Library support`); Phase 4
  code and Phase 5 proof both implement those same commitments. If Phase 5 needs
  a lemma the plan didn't commit to, treat it as plan failure -> horizontal
  pivot back to Phase 2.


Workflow. The skill enforces six phases, each producing an artifact and gating on an explicit exit
check; do not advance until the check holds.
1. Understand
   - Produces: classified sorry inventory (code vs proof); spec + instruction
     restated.
   - Exit: every sorry enumerated; instruction source located or confirmed
     absent.

2. Co-derive plan
   - Produces: <file>.plan.md with the schema's required sections.
   - Exit: plan file exists on disk; all required sections present; any
     locked-algorithm instruction is restated verbatim under
     `## Restated contract`. May not edit the .lean file before this artifact.

3. Plan gate
   - Produces: external PASS-PLAN / FAIL verdict from `lean_plan_verify` (or
     the `lean-verifier-plan` subagent).
   - Exit: verdict is PASS-PLAN. On FAIL, revise the plan file and re-run the
     same gate. Self-review is not a gate.

4. Emit code sketch + proof sketch
   - Produces: code bodies written in full; proof bodies left as `sorry`.
     `decreasing_by sorry` may stay (or be omitted if Lean auto-derives).
     Plus stub statements for the main theorem and any auxiliary lemmas.
   - Exit: `lean_diagnostic_messages` reports no errors; expected `sorry`
     warnings only; signatures elaborate so the sketch parses.

5. Fill tactic details
   - Produces: all tactic-level sorries closed (proof sorries and any
     `decreasing_by sorry` -- both are tactic blocks).
   - Exit: no errors and no in-scope sorries.

6. Quality gate (final)
   - Produces: go / no-go verdict on delivery.
   - Exit: `lean-verifier-mechanical` returns PASS-MECHANICAL and
     `lean-verifier-instruction` returns PASS-INSTRUCTION; act on each
     verdict's Action: line otherwise.


Plan schema (Phase 2 artifact). The plan file at <file>.plan.md must contain the following
sections; each is the explicit commitment that Phase 4 code and Phase 5 proof are required to realise.
## Restated contract
  Verbatim restatement of the formal spec and any algorithmic / asymptotic
  instruction.

## Algorithmic idea
  The decomposition: recursion variable, case split, termination measure.

## Library support
  Specific stdlib functions and mathlib lemma names the plan commits to.
  Adding a lemma here that does not exist is a Phase-2 failure, not a Phase-5
  failure.

## Proof obligation sketch
  For the main theorem and each auxiliary lemma, the bridging predicate or
  invariant under which Phase 5 will close it.


Phase 6 – Quality gate. Two delegated checks run in sequence (stop-on-first-failure); both must pass
before delivery.
1. Mechanical gate: lean-verifier-mechanical.
   Runs sorry scan, compile check, axiom check.
   On FAIL, parent re-enters Phase 5 targeting the failing sorry / error.




                                                      16
2. Instruction compliance: lean-verifier-instruction.
   Reads the @start code ... @end code region and judges whether the
   implementation satisfies the Instruction's complexity / algorithmic intent.
   On FAIL, parent reverts and re-enters Phase 2 with a different algorithm
   or stdlib pivot, then redoes Phase 3 -> 4 -> 5 -> 6.

Do not swap the implementation in place and re-run Phase 6 -- that bypasses
the co-derivation gate and desyncs plan, code, and proof.



When stuck. Two recovery axes – vertical (refine the current plan, once or twice max) and horizontal
(discard the plan, re-enter Phase 2). Patching a doomed plan is the more common failure mode this
skill creates than rewriting one; when in doubt, pivot.

Hard caps per target (one sorry or one compile error), per Phase-5 cycle:
  - Max 6 edits OR 8 distinct tactic candidates, whichever first.
  - Max 2 attempts per (file, line, error_or_sorry_id) signature with no
    error_count decrease.

Pivot horizontally as soon as any of these fire:
  - Same signature in 2 consecutive iterations, no error_count decrease.
  - Same sub-goal failed 2 distinct tactics AND 1 invariant rewording.
  - Phase 2: 2 consecutive empty searches for the same commitment -- the
    mathlib path the plan named doesn't exist; revise ## Algorithmic idea.
  - Phase 4-5: needing a lemma not in ## Library support -- the plan didn't
    anticipate the case; re-derive ## Library support and ## Algorithmic
    idea together, not mid-proof.
  - decreasing_by keeps failing -- recursion scheme has no clean termination
    measure.
  - Type-system fight (Fin vs Nat, getElem vs getElem!) eats > 5 turns --
    data-structure choice is wrong.
  - Postcondition is a multi-conjunction (>=3 independent claims) but the
    plan has only one main lemma.

Vertical first: refine tactic -> invariant. Allowed once or twice; if still
stuck, go horizontal: discard plan + Phase-4 sketch. Re-enter Phase 2 with
a different recursion variable, fuel formulation, split lemma, or different
data structure. Not wasted work -- it is the right move when the plan can't
carry the proof.




F    Benchmark Comparison

Table 4 situates Lean4Commit0 alongside prior verified-code-generation benchmarks. Each bench-
mark is characterized along three axes:

• Substrate. The verifier the benchmark targets. ITP-based substrates (Lean 4) require explicit proof
  terms or tactic scripts, whereas SMT-based substrates (Dafny, Verus) discharge annotation bundles
  through Z3 [46] or CVC5 [47]. “Multi” indicates that the benchmark provides tasks across more
  than one substrate.
• Task. Which artifacts the model is asked to produce: spec + code + proof synthesizes all three
  from a high-level natural-language description; code + proof fixes the formal specification and
  asks the model to write the implementation together with the proof artifact; proof only fixes both
  the implementation and the specification and asks the model to fill in the verifier annotations. The
  proof artifact subsumes both ITP tactic/term proofs and SMT annotation bundles.
• Source. Where the underlying problems come from: manually curated short functions, problems
  adapted from HumanEval-style or competitive-programming sources, or real-world software
  corpora.

The existing benchmarks in this table all draw tasks from manually curated single-function problems
or annotated SMT corpora. Lean4Commit0 instead draws from real GitHub libraries via Com-
mit0 [22], forming each task as a bundle of selected core APIs and admitting relational specifications
across those APIs (§4); these structural differences are the reason a plan that fixes the program
decomposition before either the implementation or the proof is elaborated has visible leverage on this
benchmark, as documented in Table 2.


                                                      17
Table 4: Verified code generation benchmarks. Task indicates the artifact the model is asked to
produce: spec + code + proof (synthesize all three from a high-level description), code + proof
(formal specification is given; model writes the implementation and proof artifact), or proof only
(implementation and specification are given; model writes only the proof artifact). The proof artifact
subsumes both ITP tactic/term proofs and SMT annotation bundles. Existing benchmarks draw
tasks from manually curated single-function problems or annotated SMT corpora; Lean4Commit0
instead derives library-level core-API bundles from real GitHub libraries via Commit0 [22] and adds
relational specifications across APIs.

    Benchmark               Substrate Task                   Source
    Verina [7]              Lean 4     spec + code + proof   manually curated tasks
    Clever [21]             Lean 4     spec + code + proof   adapted from HumanEval
    AlgoVeri [15]           Multi      code + proof          classical algorithms (curated)
    DafnyBench [45]         Dafny      proof only            GitHub Dafny + Clover + MBPP
    AutoVerus [11]          Verus      proof only            translated from MBPP, Diffy, CloverBench
    VeruSAGE [12]           Verus      proof only            open-source Verus-verified Rust systems
    Vericoding [44]         Multi      code + proof          12,504 specs (HumanEval, APPS, etc.)
    Lean4Commit0 (ours) Lean 4         code + proof          real GitHub libraries



G    Fabric Relational Specification Example

This appendix shows the Lean 4 task excerpt used in §4 to illustrate cross-API relational specifications.
Fabric is a Python library for SSH-based deployment and remote execution; in Lean4Commit0 we
model core configuration behavior from its API. The agent must fill every sorry, including both
implementation bodies and proofs.
  def Config.set (cfg : Config) (key : String) (value : ConfigValue)
      (level : ConfigLevel) : Config := sorry

  def Config.get (cfg : Config) (key : String) : Option ConfigValue := sorry

  @[reducible]
  def Config.set_get_roundtrip_rel (cfg : Config) (k : String) (v : ConfigValue)
      (level : ConfigLevel) (result : Option ConfigValue) : Prop :=
    result = some v

  @[reducible]
  def Config.higher_level_overrides_rel (cfg : Config) (k : String)
      (v1 v2 : ConfigValue) (lo hi : ConfigLevel) : Prop :=
    lo.precedence < hi.precedence →
      ((cfg.set k v1 lo).set k v2 hi).get k = some v2

  theorem Config.set_get_roundtrip_spec (cfg : Config) (k : String)
      (v : ConfigValue) (level : ConfigLevel) :
      Config.set_get_roundtrip_rel cfg k v level ((cfg.set k v level).get k) := by
    sorry

  theorem Config.higher_level_overrides_spec (cfg : Config) (k : String)
      (v1 v2 : ConfigValue) (lo hi : ConfigLevel)
      (hlt : lo.precedence < hi.precedence) :
      Config.higher_level_overrides_rel cfg k v1 v2 lo hi := by
    sorry



H    Lean4Commit0 M EMCHR Case Study

The M EMCHR task contains three APIs—memchr, memmem, and memrchr—and four correctness
theorems, including a relational requirement that forward and reverse search agree on whether the
target byte occurs. Under Claude-Opus-4.7 and the same budget as the main experiment, neither
primary baseline solves the task. P LAIN cannot connect the available List.idxOf lemmas to the


                                                  18
Table 5: Average cost (USD) and wall-clock time (minutes) per task on the difficult subset of each
benchmark (the top 25% of tasks ranked by mean cost across P LAIN, S EQ, and P3 ). Lower is better.

                                              P LAIN                S EQ                  P3
     Benchmark       Model
                                             Cost        Time    Cost      Time       Cost     Time
                     Codex-GPT-5.5           12.7         65.5    13.3      63.8      11.3      47.6
                     Gemini-3-Pro            14.9         83.0    15.7      89.6      13.6      52.1
     Verina
                     Claude-Sonnet-4.6       19.7        132.0    19.9     149.0      11.9     103.0
                     Claude-Opus-4.7         25.0        164.5    26.6     162.2      23.0     140.5
                     Codex-GPT-5.5           11.3         91.2    13.8      72.8       9.1      48.9
                     Gemini-3-Pro            13.4        110.1    13.6      79.6       8.4      63.2
     AlgoVeri
                     Claude-Sonnet-4.6       29.4        134.3    26.2     137.1      24.2     125.9
                     Claude-Opus-4.7         26.1        158.0    21.3     116.6      15.6      95.1
                  Codex-GPT-5.5              16.5         90.6    18.1     113.4      12.6      82.7
                  Gemini-3-Pro               20.1        149.7    25.2     142.6      16.7     135.7
     Lean4Commit0
                  Claude-Sonnet-4.6          20.0        149.6    28.2     160.5      18.2     141.6
                  Claude-Opus-4.7            29.8        125.8    29.6     130.5      28.7     121.9

optional-index specification before timing out, while S EQ commits to an unbounded search and fails
the final algorithmic evaluation.
P3 instead makes the finite witness domain explicit in the shared plan and aligns the first- and
last-occurrence proofs with Nat.find and Nat.findGreatest. This makes the cross-API theorem
compositional: after extracting occurrence and bound facts from the forward-search specification, the
reverse-search specification rules out the contradictory branch. The central proof connection is:
    have hi := (memchr_spec needle haystack).1 i hmemchr
    exact ((memrchr_spec needle haystack).2
      hmemrchr i hi.1 hi.2.1).elim

The converse direction is symmetric. Lean accepts all three implementations and all four proofs
without sorry or custom axioms; the complete traces are included in the released artifact.

I    Plan Retention and Failure Analysis
We inspect all 189 Verina traces for P3 with Claude-Opus-4.7. Among 141 successful runs, 131
(92.9%) retain the initially selected plan through completion and 10 (7.1%) replace it after the original
route proves infeasible. Because a task may admit multiple valid plans, retention is an observable
proxy for plan viability rather than a direct measure of perfect proof-burden prediction.
Among the 48 failed runs, 4 (8.3%) fail because of an inadequate plan, 3 (6.3%) during program
elaboration, 15 (31.3%) during proof elaboration under an otherwise viable plan, and 26 (54.2%)
because of timeout or tool failure. Thus only 4 of 48 failures are attributed to plan inadequacy; most
arise from proof elaboration or execution limits after a viable plan has been chosen.

J     Efficiency on the Difficult Subset
Table 5 reports the cost and wall-clock comparison summarized in Section 5.2 for the top 25% of
tasks by mean cost.

K      Full-Restart Repair Frequency
Section 5.2 described a full-restart repair failure mode: after local repairs fail under the committed
program structure, the agent abandons the current derivation and rewrites both code and proof from
scratch, sometimes more than once. We measure the frequency of this failure mode by inspecting
traces and counting runs that perform such a full restart; lower is better.
Table 6 breaks down this full-restart rate by benchmark and backend. P3 attains the lowest rate on
every Verina and AlgoVeri cell, typically reducing the restart rate by a factor of two to four relative


                                                    19
Table 6: Full-restart repair rate (% of runs where local repair fails and the agent rewrites the code-
and-proof derivation from scratch). Lower is better.

           Benchmark                  Model                     P LAIN          S EQ      P3
                                      Codex-GPT-5.5               25.9          28.6     11.7
                                      Gemini-3-Pro                24.2          24.7      7.8
           Verina (n=189)
                                      Claude-Sonnet-4.6           17.4          18.5      5.3
                                      Claude-Opus-4.7             28.5          24.9      8.5
                                      Codex-GPT-5.5               33.4          34.9     11.2
                                      Gemini-3-Pro                21.3          32.2      7.0
           AlgoVeri (n=77)
                                      Claude-Sonnet-4.6           21.9          23.2      5.8
                                      Claude-Opus-4.7             24.4          33.6      9.1
                                      Codex-GPT-5.5                3.7           4.3      1.7
                                      Gemini-3-Pro                 4.1           4.9      1.6
           Lean4Commit0 (n=108)
                                      Claude-Sonnet-4.6            3.2           4.4      1.2
                                      Claude-Opus-4.7              4.3           5.2      2.2

Table 7: Average per-task cost (USD) and time (minutes) on the intersection of correctly-solved
tasks (Plain, Seq, and P3 all yield algorithmically-correct solutions). Isolates per-task efficiency from
coverage.

                                                P LAIN                   S EQ               P3
  Benchmark         Model
                                              Cost       Time       Cost        Time    Cost     Time
                    Codex-GPT-5.5              1.96       9.5        1.61        8.6    1.71       9.2
                    Gemini-3-Pro               2.24      13.5        1.71        9.3    1.62      10.7
  Verina
                    Claude-Sonnet-4.6          2.22      21.6        2.22       21.7    2.13      20.9
                    Claude-Opus-4.7            2.55      18.1        2.63       19.1    2.67      19.6
                    Codex-GPT-5.5              2.78      13.9        2.95       16.8    1.20      19.6
                    Gemini-3-Pro               2.67      20.5        4.17       18.1    1.10      19.2
  AlgoVeri
                    Claude-Sonnet-4.6          4.02      16.5        5.71       28.0    5.31      31.8
                    Claude-Opus-4.7            2.31      27.8        2.31       26.6    2.86      36.9
               Codex-GPT-5.5                   1.46      14.2        2.83       26.0    2.90      18.4
               Gemini-3-Pro                    2.28      17.0        3.71       35.3    2.71      21.4
  Lean4Commit0
               Claude-Sonnet-4.6               4.01      32.5        3.89       41.2    3.95      30.5
               Claude-Opus-4.7                 3.75      32.9        3.79       47.7    4.06      42.7


to the stronger baseline. On Lean4Commit0, all three methods are below 5% because library-level
relational specifications already pin down enough behavior to leave little room for full restarts.

L    Per-Task Efficiency on the Solved Intersection
Table 7 reports per-task cost and time on the intersection of tasks where Plain, Seq, and P3 all produce
algorithmically-correct solutions, isolating per-task efficiency from coverage differences in the main
results.




                                                   20
