                                                           Self-Modifying Lean Proof Agents with
                                                          Verifier-Grounded Benchmark Coevolution
                                                         Yuqing Li                         Zeguan Wu                            Yu Gan
                                                  University of Pittsburgh           University of Pittsburgh           University of Pittsburgh
                                                    yul658@pitt.edu                     zew79@pitt.edu                    yug130@pitt.edu
                                                                                         Junyu Liu∗
                                                                                   University of Pittsburgh
                                                                                 junyuliucaltech@gmail.com
arXiv:2607.17352v1 [cs.AI] 19 Jul 2026




                                                                                              Abstract
                                                       Designing effective Lean proof agents is a central challenge in formal mathematical reasoning.
                                                   While one line of work builds stronger Lean-oriented provers, recent perspectives emphasize that
                                                   theorem-proving agents also need better workflows around Lean: how they decompose proof obli-
                                                   gations, use tools and compiler feedback, diagnose failed attempts, repair proofs, and maintain
                                                   structured proof context. Motivated by code-level self-evolving agents, we study whether such
                                                   workflows can be evolved rather than hand-designed. We present a self-evolving Lean proof agent
                                                   in which a small fixed, trusted runtime wraps a fully mutable workspace — the proof workflow,
                                                   prompts, and tools. Unlike most self-evolving agent systems, which optimize against an exter-
                                                   nally supplied, fixed benchmark, our system coevolves the agent and its benchmark. Between
                                                   generations, the highest-scoring agent — the champion — revises the active task distribution
                                                   through a mastery-throttled curriculum update, introducing harder proof obligations only after
                                                   the current level has been mastered; a single-anchor recalibration then re-runs the champion on
                                                   the updated benchmark so that scores remain comparable as difficulty rises. All evolution stays
                                                   inside a Lean-grounded verification loop: however the agent rewrites itself, a success counts
                                                   only when its behavior yields Lean-verified proofs under a trusted snapshot. Each solve attempt
                                                   must also emit a machine-readable, Lean-grounded proof context whose representation is free
                                                   to evolve but whose groundedness is enforced. We run both the coevolving trajectory and a
                                                   fixed-benchmark baseline for 15 active generations. Because coevolving raw scores are measured
                                                   under changing benchmark difficulty, we compare runs on a held-out miniF2F test split, evalu-
                                                   ating selected agents from the coevolving trajectory and the two highest-scoring agents from the
                                                   fixed-benchmark baseline. On this split, the best evaluated coevolving agent reaches a 45.1%
                                                   held-out solve rate, compared with 12.7% for the seed and 32.0% for the best fixed-benchmark
                                                   baseline agent. These results show that verifier-grounded self-evolution can improve Lean proof
                                                   workflows under a coevolving benchmark.


                                         1        Introduction
                                         Lean proof agents and the workflow bottleneck. Designing effective agentic frameworks for
                                         Lean-based theorem proving has become an increasingly central problem in formal mathematical
                                         reasoning [12, 20, 16, 15, 5]. One line of work aims to build stronger Lean-oriented provers: special-
                                         ized models, tactics, or search procedures that more directly synthesize valid Lean proofs [12, 20, 16].
                                             ∗
                                                 Corresponding author.


                                                                                                   1
                                                                               Total Task Pool
                    seed
                    agent
                                                                       Current                                tasks
                                                                                                      single-tactic lemmas
                                                     Evaluation       Bechmark
                                                      Records

                                                     Records from       easy tasks                            tasks
         G1          G1                               all agents                                            miniF2F
        agent       agent
                                    Champion agent
                                                          G1 agent          hard tasks
                                                          records
                                                                                                              tasks
                                                                                                         PutnamBench
                                                          G1 agent     Updated
                                                          records     Benchmark

                                                       Champion
                                                         agent
             G2              G2              G2
                                                        records
                                                                         Benchmark update rule
            agent           agent           agent
                                                                     When Champion agent's accuracy                    :
                                                                      replace an      task with

                                                                          an       task if accuracy
                     Difficulty normalization                             an         task if accuracy




Figure 1: Champion-driven agent–benchmark coevolution. A seed agent produces first-
generation (G1) children that stream into a shared archive as they are evaluated, so a strong
early child can already parent later siblings in the same generation; the strongest child becomes
the champion, seeds the next generation (G2), and also drives the benchmark update. Evaluation
records from all agents are collected. The benchmark is drawn from a candidate problem pool
stratified by difficulty level (L1 : single-tactic lemmas; L2 : miniF2F valid split, disjoint from the
held-out test set used only for generalization; L3 : PutnamBench). When the champion clears
the update threshold, mastered tasks are retired and replaced either laterally by new tasks from
the same level, or by harder tasks from the next level once that level has been mastered. The
updated benchmark is then used to evaluate the next generation. To keep scores comparable as the
benchmark becomes harder, the champion is re-run on the updated benchmark as a single-anchor
recalibration: equating its normalized scores, e.g. 0.39 × 1 = 0.32 × c, yields the new difficulty
coefficient c = 1.24 (illustrative values).


A complementary, workflow-centered line — exemplified by LEAP [15] and Goedel-Architect [5] —
instead emphasizes that the bottleneck is not only prover strength, but also how an agent interacts
with the Lean proof environment: how it decomposes proof obligations, invokes tools, uses compiler
feedback, diagnoses failed attempts, repairs proofs, and maintains useful proof context. Both rely
on hand-designed proof workflows built around intermediate Lean lemmas or AND/OR-style de-
composition, and report strong results (Goedel-Architect reaches 99.2% on miniF2F-test), showing
that the proof workflow itself is a major determinant of performance.
    This work follows the workflow-centered view. We do not aim to make Lean itself a stronger
verifier. Instead, Lean serves as a fixed, trusted substrate for checking correctness, while the object
of improvement is the agentic proof workflow around it. Our motivating question is therefore: if a
Lean proof agent is not given a carefully hand-designed workflow, what proof workflow can it evolve
for itself?



                                                      2
From DGM to Hyperagents. We approach this question through recent work on code-level
self-evolving agents. The Darwin Gödel Machine (DGM) [35] showed that an agent can improve by
rewriting its own code and empirically validating the resulting variants on downstream tasks. This
makes DGM a natural starting point for self-improvement, but its original setting is closely aligned
with coding: the agent modifies code, and its improvement is measured on coding benchmarks.
     Hyperagents [36] extend this line by introducing a self-referential architecture that integrates
two roles into a single editable program: a task agent, which solves the target task, and a meta
agent, which modifies both itself and the task agent. Because the meta-level modification procedure
is itself editable, the system can improve not only task-solving behavior but also the mechanism
that generates future improvements. This distinction matters for formal mathematics: it allows a
self-evolving framework to target Lean theorem proving, where the object of improvement is the
mathematical proof workflow itself rather than the agent’s general coding ability.

From self-evolving agents to coevolving benchmarks. Although coevolving environments
have been studied in open-ended systems such as POET and MCC [29, 2], many recent self-evolving
agent systems still evolve the agent while keeping the external environment fixed [35, 36, 4, 32, 10,
37]. This is especially problematic for Lean theorem proving, where benchmark difficulty deter-
mines whether evolution receives an informative selection signal. In our experiments, the seed
proof agent solves only 12.7% of the held-out miniF2F test split overall, and solves almost none of
its competition-level (AMC/AIME/IMO) problems. Evolving directly against benchmarks of this
difficulty means most evaluations end in failure and provide little selection signal. Conversely, a
benchmark easy enough to be informative quickly saturates if it never hardens.
     We therefore use a coevolving benchmark, illustrated in Figure 1. To make benchmark replace-
ment auditable, we organize the candidate problem pool into three difficulty levels. Although our
longer-term goal is to let agents propose increasingly difficult formal problems themselves, this study
takes a bounded first step: the champion updates the active benchmark under fixed rules, retiring
mastered problems and replacing them either with new problems from the same level or, once that
level has been mastered, with problems from a harder level. The benchmark can therefore begin
in a tractable regime that provides an effective evolutionary signal while avoiding the saturation of
a fixed easy benchmark. As the agent’s proof ability improves, the benchmark self-hardens, so the
proof environment evolves together with the agent rather than remaining a fixed yardstick.

Why Lean keeps the evolution grounded. The formal setting is essential: a self-rewriting
proof agent cannot be trusted to report its own mathematical success; Lean, rather than the agent,
is therefore the arbiter. A proof obligation counts as solved only when the generated proof re-verifies
under a trusted Lean snapshot, and benchmark updates are driven by these Lean-verified records
rather than by self-reports. We additionally require each attempt to emit an inspectable, Lean-
grounded proof context whose representation is free to evolve but whose groundedness is enforced.
We detail this representation-free-but-grounded contract, and the re-verification that makes solves
hard to spoof under the trusted-runtime threat model, in Section 3.2.

Contributions.

   • Self-evolving Lean proof agent. We present a code-level self-evolving Lean theorem-
     proving agent in which the proof workflow and tools are mutable, while proof success remains
     grounded in Lean verification.




                                                  3
    • Benchmark coevolution. We introduce a champion-driven, self-hardening benchmark that
      coevolves with the proof agent, using mastery-throttled updates and single-anchor recalibra-
      tion to raise difficulty while keeping scores comparable across generations.

    • Representation-free proof contexts grounded by Lean. We require each solve attempt
      to expose a machine-readable proof context whose representation may evolve, while solved
      claims remain grounded by trusted Lean verification.

Paper organization. Section 2 situates our work among self-evolving agents, LLM-based provers,
and coevolution / automatic curricula. Section 3 presents the system: the mutable workspace and
evolution interface, the verifier-grounded proof-context contract, and the coevolving-benchmark
loop with its parent selection. Section 4 reports the experimental study — capability under the self-
hardening benchmark, a fixed-vs-coevolving ablation, workflow/tool self-modification, and proof-
context quality. Section 5 discusses the main implications and concludes. The appendix collects
experimental details, the benchmark-update algorithm, a worked example, and the lineage record
of the accepted run.


2    Related Work
Our work sits at the intersection of three lines of research — self-evolving agents, LLM-based formal
theorem proving, and coevolution with automatic curricula — which we review in turn.

Self-evolving agents. Recent work on self-evolving agents studies how agents can improve by
rewriting their own code or prompts [23, 34, 7, 32, 21], by searching over agent designs and work-
flows [10, 37, 24, 33, 3], or by evolving programs against an automatic evaluator [22, 17], rather
than relying on a fixed hand-designed workflow; see [26, 8] for surveys. DGM [35] evolves an
archive of code-level agents, Hyperagents [36] distinguish a task agent from a meta agent that
modifies the improvement process itself, and related group-evolving systems study population-level
self-improvement [4, 31]. Our work transfers this line to Lean theorem proving and further allows
the benchmark to coevolve with the proof agent.

LLM agents for formal mathematical proof. Recent work couples LLMs with formal provers
through proof generation, sketching, retrieval, compiler feedback, and repair [18, 14, 30, 25], with
benchmarks such as miniF2F [38] and PutnamBench [27]. LEAP [15] and Goedel-Architect [5]
most directly demonstrate the importance of agentic proof workflows: both build a hand-designed,
static workflow around a fixed prover — LEAP maintains its proof plan as an AND-OR DAG of
intermediate Lean lemmas, while Goedel-Architect generates and iteratively refines a blueprint, a
dependency graph of definitions and lemmas — with Goedel-Architect reaching 99.2% on miniF2F-
test. Our work instead makes the proof workflow evolvable, while requiring Lean-grounded proof
context without hard-coding a single representation.

Coevolution and automatic curricula. Coevolving solvers with environments or curricula is
well established outside formal proof, including POET, MCC, PAIRED, and automatic-curriculum
methods [29, 2, 6, 19, 28, 1]. Recent LLM-agent work also explores agent–environment or agent–
benchmark coevolution [9, 4, 31, 11]. Red Queen Gödel Machine (RQGM) [13] coevolves agents
with their evaluators: it targets settings where no fixed ground-truth answer may be available, so
the evaluator and the criterion of success must themselves adapt. Formal mathematical proof, by


                                                 4
contrast, has a fixed correctness criterion and a strict requirement for proof validity, so we keep the
evaluator fixed as a trusted Lean verifier and coevolve benchmark difficulty instead. Thus, RQGM
coevolves the criterion of success, whereas our system keeps the criterion fixed and coevolves the
difficulty distribution over formally verifiable proof tasks.


3     Method
This section presents our system: a fixed, trusted runtime wrapping a mutable, evolvable workspace
(Section 3.1); a proof-context contract that keeps the self-rewriting agent inspectable and hard to
spoof (Section 3.2); and the coevolving benchmark with its parent selection (Section 3.3, Section 3.4).

3.1   Mutable workspace and evolution interface
Our system separates a fixed, trusted runtime from a mutable workspace. The trusted runtime is
responsible for all mechanisms that determine correctness and reward — Lean verification, evalua-
tion, benchmark management, and proof-context validation — and stays outside the evolutionary
search. The mutable workspace holds the agent-facing proof workflow together with the meta-level
logic that adapts it, and is the sole object of evolution: across generations, agents rewrite this
workspace through a constrained edit interface while the trusted runtime remains untouched.
    A central design choice is to separate code validity from proof success. A mutated agent first
passes through a code-level stage — basic execution and smoke tests confirming that its rewritten
workflow runs and returns the expected interface. Passing this stage admits the agent to evalu-
ation but does not by itself mark any theorem as solved: whether a proof obligation is solved is
decided solely by the trusted runtime, which re-verifies the generated proof under a trusted Lean
snapshot (Section 3.2). However the agent rewrites its workflow, tools, or proof-producing code,
the solved/unsolved verdict is determined by Lean alone, and benchmark updates are driven by
Lean-verified solve records rather than by anything the agent reports about itself. Against this
backdrop the seed agent is kept deliberately minimal — a single proof attempt that is checked once,
with no repair loop, search, or proof decomposition — so that any later repair behavior, search
strategy, or proof-context structure can be attributed to the self-evolving process rather than to a
hand-designed proof workflow.

3.2   Enforced, trustworthy proof context: free to evolve, hard to spoof
The proof-context contract has two parts. Part A specifies what each solve attempt must emit
and what minimal grounding requirements the proof context must satisfy. Part B describes the
trusted re-verification layer that prevents a mutable agent from faking solved proofs or proof-context
certificates. Together, these two parts make the agent’s proof attempts inspectable while keeping
all reported solves and benchmark records grounded in Lean-verified evidence.

Part A: the contract. Every solve attempt returns a triple {ok, proof_body, proof_context}.
The proof context records the mathematical structure of the attempt, such as claims, lemmas,
subgoals, dependencies, and how they support the final theorem. It is kept separate from the
workflow trace, which records LLM attempts, repair loops, and tool calls.
    The representation of the proof context is free: the agent may use a graph, a tree, a lemma table,
or another structure. The validator enforces only a small set of grounding requirements. First, a
root context item must exist. Second, the context must contain at least one mathematical claim,
subgoal, or lemma besides the root. Third, dependency edges, if present, must point to known

                                                  5
items. Fourth, proof-attempt and diagnostic records do not count as mathematical context. Fifth,
any item marked as solved must be backed by Lean-verified evidence. Finally, if the agent provides
optional formal fields such as a lean_statement and a proof_body, the trusted runtime can verify
that item independently and return node-level feedback. The principle is that representation is
flexible, but groundedness is mandatory.

Part B: trusted re-verification and spoofing resistance. Because the agent rewrites code
adjacent to scoring, none of its self-reports can be trusted. The trusted runtime therefore re-checks
both final proofs and proof-context certificates before they affect any score or benchmark record.
    First, the final score ignores all of the mutable code’s self-reported status; the fixed runtime inde-
pendently re-verifies the task statement together with the returned proof body under a trusted Lean
snapshot. Second, top-level Lean commands in the returned proof body are rejected, preventing
the agent from substituting an unrelated theorem. Third, certificates are sanitized: a proof-context
item is marked solved only after its associated Lean evidence passes trusted verification. Fourth,
immutable runtime files and verifier configuration are protected against tampering; any detected
modification is reverted or rejected, and recorded. Fifth, mutable entry points run in isolated worker
processes on a copied workspace, so the trusted parent does not import or execute mutable modules
directly. Sixth, real Lean proofs are required: sorry and admit are rejected.

3.3   Coevolving benchmark
The benchmark is drawn from a candidate pool stratified into difficulty levels L1 < L2 < L3
(defined in Appendix A), chosen so that the seed has substantial success on L1 but low success on
L3 . Between generations, the champion drives the benchmark update. A single difficulty coefficient
c links the two halves of the loop: it both normalizes the selection scores (Section 3.4) and records
the accumulated change in benchmark difficulty.

Benchmark update mechanism. The full procedure is given in Algorithm 1 in Appendix B. At
the end of each generation, the benchmark is updated only if the champion meets the update thresh-
old: its raw solve rate on the current benchmark must exceed γ = 0.30; otherwise the benchmark
is carried over unchanged.
    Once the threshold is met, the update proceeds. A task is eligible for retirement only if it is
solved by all agents evaluated in that generation, and the update retires at most κ such tasks.
    For each retired task at level ℓ, the replacement level is determined by the champion’s current
solve rate mℓ on level ℓ. If mℓ ≥ τ with τ = 0.70, the retired task is replaced by a task from the next
level ℓ + 1; otherwise, it is replaced laterally by a new task from the same level ℓ. Newly inserted
tasks are treated as unsolved until they are evaluated in a later generation, so mℓ is recomputed
after each replacement. This makes the update self-throttling: a level can graduate only while the
champion’s level-specific mastery remains high, and repeated replacements reduce the measured
mastery rate, preventing abrupt benchmark hardening.
    When selecting replacement tasks, the update also prefers domains where the archive has accu-
mulated more failures, so the new benchmark reflects both level difficulty and observed population
weaknesses.

Single-anchor recalibration and cross-generation comparability. Because the benchmark
hardens, raw solve rate is not comparable across generations. We restore comparability with a
single-anchor recalibration: the champion is re-evaluated on the new benchmark and the difficulty


                                                    6
coefficient is updated multiplicatively,
                                                   rt
                                 ct+1 = ct ·                ,     c0 = 1,
                                               max rt+1 , ϵ

where rt is the champion’s raw score on Bt , and the difficulty-normalized score reported for every
agent is q = r × c. By construction the champion’s normalized score is preserved across the
recalibration (it is the anchor), so an agent evaluated on a harder benchmark and one evaluated
on an easier benchmark are placed on a single scale. The per-step ratio is small (typically ≲ 1.4
for our pool sizes) but compounds across generations, so the coefficient measures how much harder
the current benchmark is than the original baseline; ϵ guards against degenerate ratios when the
champion’s re-evaluated score is very low.

3.4    Parent selection within a generation
Within a generation, parents are sampled from the archive in proportion to a DGM-style weight
that rewards capability and discounts agents that have already produced many children:
                                                                      1
                               q = r × c,        w = max(q, 0) ·           .
                                                                    1 + nc
Here q is the difficulty-normalized score, r the raw solve rate, c the difficulty coefficient (Section 3.3),
and nc the agent’s current child count; parents are drawn with replacement ∝ w. Selection uses
within-generation streaming: each accepted child is archived as soon as it is evaluated and immedi-
ately becomes eligible as a parent for later attempts in the same generation, so an early strong child
can seed its own siblings. The child count nc also includes pending, not-yet-evaluated children, so
the same factor discounts agents with outstanding offspring and damps runaway selection of a single
lineage within a generation.


4     Results
This section reports held-out capability across evolution generations, the comparison with a fixed-
benchmark baseline, and the evolution of workflow structure, mutable tools, and proof-context
quality.
    During evolution, agents are evaluated on a 76-task active benchmark stratified into difficulty
levels L1 –L3 : author-constructed single-tactic warm-up lemmas, miniF2F problems [38], and Put-
namBench problems [27]. To make results comparable across generations, we also evaluate agents
on a fixed held-out miniF2F test split of 244 problems. This test split is disjoint from the curriculum
and is never used for training. Both the coevolving run and the fixed-benchmark baseline complete
15 active generations. For the fixed-benchmark baseline, where raw scores are measured on the
same benchmark throughout, we evaluate the two highest-scoring agents on the held-out test split.
For the coevolving run, where the active benchmark changes over time, we evaluate selected agents
across the trajectory. Backend, hyperparameters, hardware, and runtime details are provided in
Appendix A.

4.1    Capability under a self-hardening benchmark
Because benchmark difficulty changes throughout evolution, we evaluate high-scoring agents on the
fixed held-out test split, which provides a stable yardstick for identifying the strongest agent. As
shown in Table 1, held-out solve rate rises from 12.7% for the seed agent to 45.1% at generation 15.

                                                     7
            Table 1: Held-out miniF2F test solve rates for evaluated coevolving agents.

              Gen 0     Gen 2    Gen 4    Gen 5       Gen 9   Gen 10   Gen 13    Gen 14     Gen 15
 Solve rate   12.7%     38.9%    29.9%    29.9%       11.9%   25.4%    40.6%      25.4%     45.1%
 Agent         seed      c12      c26      c39         c52     c86      c99        c141      c144


The solve rate does not increase monotonically, reflecting that selection optimizes active-benchmark
score rather than held-out performance. At the same time, the benchmark difficulty coefficient rises
from 1.00 to 3.17; see Table 2 in Appendix D for details.

4.2   Fixed vs. coevolving benchmark
The fixed-benchmark baseline reaches lower held-out solve rates than the coevolving run. Because
the fixed benchmark never changes, raw training scores are directly comparable; we therefore evalu-
ate the two highest-scoring fixed-benchmark agents on the held-out test split. Their held-out solve
rates are 32.0% and 26.6%. For the coevolving run, raw training scores are measured under changing
benchmark difficulty, so we evaluate 9 selected agents across the trajectory. By generation 15, the
best coevolving agent reaches a held-out solve rate of 45.1%, higher than either fixed-benchmark
agent.
    The fixed-benchmark run scores lower because its evolutionary pressure becomes weak after early
mastery. Once an agent solves a stable subset of the fixed 76 tasks, later mutations are selected
mainly for preserving or slightly improving performance on the same problems. The benchmark
does not retire mastered tasks or introduce harder ones, so later agents mostly explore local repair
and tool variants without being forced to broaden their capability. Thus, the fixed-benchmark run
keeps changing code, but mostly around the same narrow set of solutions, which limits held-out
generalization.

4.3   Workflow self-modification
The high-scoring workflow is repair-centered, not decomposition-centered. Across the accepted
lineage, selected agents mostly preserve a compact Lean-error repair loop: generate a full proof, run
Lean, use the error message and lemma-name checks, and retry with bounded feedback (Figure 2
and Table 3). This winning workflow pattern is cheap, directly tied to final solve rate, and easier
for selection to reward than a blueprint-first decomposition-based workflow.
    This does not mean that decomposition-based workflows are absent from the search. On the
contrary, the mutation traces repeatedly reason about proof blueprints, subgoals, isolated sub-lemma
verification, and deeper proof-context trees. The gap is between reasoning about these workflows
and shipping them. Several agents judge the change too large or risky and fall back to label-only
nodes, degenerate whole-theorem nodes, or conventional repair machinery: c12 writes the binder-
isolation fix that verified subnodes would need but improves instead through lemma tooling, and
c39 later defers isolated sub-lemma verification after observing that variables are unbound. This
behavior is rational under the sparse objective: if only the final Lean-checked theorem is rewarded, a
compact proof body plus compiler-feedback repair is often a better use of budget than constructing
and checking intermediate proof nodes.
    We now examine the decomposition-based workflows that actually evolved: three main branches
shown as bold nodes in the evolution tree (Appendix D, Figure 2). First, the c22 branch makes an
early attempt at a decomposition-and-prove fallback. This branch tries to add lemma indexing and


                                                  8
retrieval machinery around decomposition, but the implementation hits the mutable-process guard,
the trusted runtime’s ban on spawning subprocesses. Its descendant c23 removes the subprocess-
based machinery and simplifies the workflow, but the simplified version collapses to raw 0.132. This
branch therefore shows an early failure mode: decomposition needs extra tooling, but that tooling
can easily become too brittle or incompatible with the trusted runtime. Second, the c44 branch
evolves genuine node-level verification, but only in a shallow form. The c44/c47 lineage asks for self-
contained sub-lemmas, carries the ambient binders into each lemma statement, and verifies many
subgoals independently in Lean. This is a real improvement over post-hoc have-extraction, but
it is not yet a full decomposition-and-assembly workflow: the branch mainly certifies local helper
nodes and does not seriously address how those verified lemmas should be composed back into the
final theorem. Trace-level problems, such as c44’s null root certificate, can also invalidate otherwise
meaningful subgoal evidence. Thus c44/c47 improve proof-context structure, but remain shallow
and do not become the winning route. Third, the c26 lineage is the most important later case because
it eventually pushes decomposition into an explicit plan-prove-assemble workflow. Earlier agents
mostly use decomposition after repair, or only as proof-context structure. By contrast, the later c141,
shown in Appendix C and Listing 1, introduces a subgoal-prover workflow: it first plans auxiliary
lemmas, then tries to prove them, and finally attempts to assemble the main theorem from those
lemmas. This is the closest the run comes to a decomposition-first workflow. It fails not because
it ignores assembly, but because assembly is exactly the hard part: generated helper lemmas often
do not match the final theorem’s needed context, the interfaces between lemma planning, lemma
proving, and final assembly create extra failure points, and the longer prompts increase timeout
and truncation risk. Since selection rewards only final theorem success, this richer structure is not
protected when its final assembly fails.
     Repair itself also does not grow without bound. Proof generation runs under a bounded output
budget and a per-task wall-clock cap (Appendix A). When repeated repair accumulates long prompts
and error histories, proof-generation calls can be truncated or time out; these errors are visible to
the agent and become pressure to shorten the next workflow. The large-repair variants show this
saturation: c19 expands the loop to ten attempts but falls to raw 0.368, and c51 raises monolithic
repair to twelve attempts but scores only 0.263. Its descendant c52 keeps the repair idea but shifts
toward early native_decide, shorter prompts, bans on hallucinated lemmas, and streamlined result
construction. Thus evolution preserves verifier-feedback repair as a workflow principle, but not
unbounded repair: very large repair loops are competed away.

4.4   Mutable tools
Most evolved tools target hallucinated Lean names. Early agents add simple #check probes
and Mathlib source search, so invented Lean names can be rejected before they enter the fi-
nal proof. Later agents make the same idea more systematic: they batch name checks through
verify_lemma_list, pass verified signatures into the prompt, and keep small caches or namespace-
aware indexes so that names such as Nat.gcd_dvd_left or Nat.dvd_mul_right can be confirmed
before being used. c96 turns this into a cached lemma checker with namespace-aware search and
a verified-only fallback, while c144 feeds exact verified signatures and source-grep suggestions back
into the monolithic repair loop. These tools do not create a new high-level proving strategy by
themselves. Their main role is to make repair safer: when Lean reports an unknown identifier
or type error, the workflow can ban the bad name, suggest a verified alternative, and retry with
concrete Lean feedback.




                                                  9
4.5   Proof context
Proof contexts become inspectable but rarely grow into deep verified proof graphs. Proof-context
quality is logged but not rewarded (Section 3.4), so it should be read as a diagnostic signal rather
than a direct optimization target. Empirically, it stays roughly stable across generations even as the
final solve rate changes. The lineage record explains why: agents often preserve inspectable proof
context, but rarely turn it into verified mathematical decomposition trees (Table 3).
    The record shows that agents in early and middle generations mostly construct proof context
backward from the final Lean proof rather than planning a proof graph in advance. Agents such
as c11, c12, c25, and c26 extract have statements from the generated proof body and attach them
as lemma or subgoal nodes beneath a single main-theorem node. Their mutation traces explicitly
discuss decomposition-based workflows, subgoal verification, and per-node proof contexts, but the
executed nodes are usually not self-contained Lean theorems: they depend on binders, local hy-
potheses, and type context from the surrounding proof. When isolated for node-level verification,
these nodes often fail with unknown identifiers, type mismatches, or unsolved goals. This phase
therefore increases the number of nodes, but the realized structure is mostly a shallow support star
of the form have-* → main-theorem, not a deep proof tree or reusable DAG.
    The c44/c47 branch is the first meaningful node-level verification attempt. It partially solves the
binder-isolation problem by asking for self-contained sub-lemmas whose statements carry the ambi-
ent variables as explicit binders, and by attaching Lean lean_statement/proof_body evidence to
some proof-context nodes. Later descendants show both the promise and the limit of this direction.
c99 keeps the c47 structure and produces a subgoal_tree_with_formal_lemmas context, with some
helper nodes passing formal verification; however, these nodes remain shallow supports for one final
theorem, not a reusable multi-layer graph. c144 reaches a high solve rate, but its proof plan mainly
guides monolithic repair, and many extracted have nodes either fail isolated verification or lack the
full lean_statement/proof_body pair required for node-level checking. c145 makes the graph label
more explicit as a subgoal_dag, but its nodes are mostly open or label-only supports and the score
drops. Thus later descendants retain the winning repair-centered mechanisms—lemma checking,
bounded repair, and native_decide fast paths—while proof context stabilizes as shallow verified
or label-only supports for the main theorem rather than a deep dependency graph.


5     Discussion
This paper studies whether a Lean proof agent can improve by rewriting its own proof workflow,
tools, and proof-context representation while remaining grounded by a fixed verifier. We build such
an agent and pair it with a coevolving benchmark that hardens as the current champion masters
easier tasks. The main claim is not that the verifier changes or becomes stronger: Lean remains the
trusted judge throughout. Rather, the mutable code around Lean learns better ways to use verifier
feedback, check lemma names, repair failed proofs, and record proof structure.
    The experiments show that useful mathematical workflow structure can evolve under this fixed-
verifier setting. The lineage develops verifier-adjacent tools for preventing hallucinated Lean names,
and it eventually evolves genuine node-level verification for self-contained sub-lemmas. This sup-
ports the feasibility of node-level verification in a self-modifying proof agent: mutable agents can
invent new proof-context formats, while the fixed runtime can still audit whether claimed nodes
are actually Lean-verified. The fixed-vs-coevolving ablation also shows why benchmark hardening
matters. A fixed benchmark makes raw scores directly comparable, but it gives weaker curriculum
pressure once the agent reaches a plateau. The coevolving benchmark keeps the training signal
closer to the agent’s current frontier.

                                                  10
    After 15 generations, held-out miniF2F test solve rate rises from 12.7% for the seed agent to
45.1% for c144 at generation 15. This is a substantial improvement from code-level self-evolution
alone, but it remains well below the strongest hand-designed proof agents (Goedel-Architect reaches
99.2% on miniF2F-test, with a different backend). Our lineage audit suggests a main reason for the
gap: the winning workflow is still mostly repair-centered. High-scoring agents repeatedly generate
a complete proof, ask Lean for errors, and repair the result with bounded feedback. Decomposition-
based workflows do appear, and later agents increasingly reason about subgoals and node-level
verification, but these structures usually remain shallow and fragile when they must be assembled
back into the final theorem.
    We therefore view the current result as evidence for a direction rather than a finished proof
assistant. Longer runs, larger populations, or rewards that directly value verified decomposition
may make decomposition-based workflows a more important evolutionary route. In the present
15-generation runs, however, the agent has not yet evolved a deep, durable proof-context graph.
Looking further ahead, we see a natural path in pushing this approach into other domains where
formal, Lean-verified reasoning is essential—such as quantum computing—where machine-checked
proofs of correctness could prove especially valuable.


Acknowledgments
YL, ZW, YG and JL are supported in part by the University of Pittsburgh, School of Computing and
Information, Department of Computer Science, Pitt Cyber, Pitt Momentum fund, PQI Community
Collaboration Awards, John C. Mascaro Faculty Scholar in Sustainability, Switzerland NSF award
2000-1-243053, NSF award 2535915, Thinking Machines Lab and Cisco Research. This research
used resources of the Oak Ridge Leadership Computing Facility, which is a DOE Office of Science
User Facility supported under Contract DE-AC05-00OR22725.


A    Experimental details and hyperparameters
We report a single-run study; quantitative comparisons therefore come without variance estimates
and should be interpreted accordingly.

Backend, verifier, and hardware. A single LLM backend — DeepSeek deepseek-v4-pro over
an OpenAI-compatible API (1M-token context) — drives both the proof workflow and its self-
modification. We use this backend to keep long evolution runs affordable while retaining enough
capability for Lean proof search. Decoding is greedy (temperature 0, fixed random seed). LLM
calls use a 600s API timeout, and the backend treats max-token truncation as an error rather than
passing an incomplete proof to Lean. Each mutable proof workflow is also run in an isolated worker
with a hard wall-clock cap (set by PROOF_HYPERAGENT_WORKFLOW_TIMEOUT_S; 1200s throughout the
reported runs). Even at temperature 0 the backend shows non-negligible output instability on
boundary problems, so small differences should be interpreted cautiously. Correctness is checked
by real Lean 4 with Mathlib (v4.30.0; mock Lean is disabled in scored runs). The evolution
orchestration and all Lean compilation and verification run on a single multi-core CPU host with
the Mathlib environment staged on local storage; the model is served remotely.

Compute cost. A single 15-generation coevolution run evaluates up to three accepted children per
generation on the 76-task benchmark and performs the mutation and smoke-testing steps. Wall-
clock time scales roughly linearly with the number of generations, with held-out test evaluation

                                                11
adding separate benchmark jobs. Because the model is a remote API, this wall-clock is dominated
by Lean compilation, verification, and long proof-generation calls rather than local compute.

Benchmark and held-out test set. The agent is trained on Lean 4 tasks drawn from a candidate
pool stratified into difficulty levels: L1 consists of author-constructed single-tactic warm-up lemmas,
L2 of miniF2F problems (valid split, disjoint from the held-out test set), and L3 of PutnamBench
problems. These levels impose a deliberate evolution gradient: across the candidate pool, the seed’s
per-level solve rate falls steeply — ≈ 0.52 on L1 , ≈ 0.18 on L2 , and ≈ 0.00 on L3 — so each level
is a rung just beyond the one below. The coevolving active benchmark holds 76 tasks; at t=0 its
level mix is L1 :L2 :L3 = 27:46:3, drawn from a candidate pool of 365 tasks (52 at L1 , 57 at L2 , and
256 at L3 ). We compose this initial mix so that the seed’s overall solve rate is ≈ 0.37 (28/76) —
challenging enough to leave room for improvement while still providing an informative evolutionary
signal. Generalization is measured on the held-out miniF2F test split (244 problems), disjoint from
the valid-split curriculum and never used for selection.

Experimental hyperparameters. Both experiments run for 15 active evolution generations
after the seed, with up to three accepted children per generation, aborting after three consecutive
backend failures and allowing at most six mutation attempts per generation. Agent identifiers
are global mutation-attempt IDs across the run, including variants rejected before evaluation, so
they need not match the number of accepted children. The benchmark-update threshold is a raw
champion solve rate of γ = 0.30; the graduation threshold is τ = 0.70 and the curriculum step
σ = 1; each generation retires up to κ = 6 mastered tasks (the fixed-benchmark baseline uses κ = 0),
replaces them with domain-matched tasks, and halts replacement when no eligible task remains in
the weak domains. Recalibration uses ϵ = 0.1 in the multiplicative update ct+1 = ct ·rt / max(rt+1 , ϵ),
and time and token penalties are set to 0.


B    Benchmark-update algorithm
Algorithm 1 states the full mastery-throttled benchmark update whose core mechanisms — the
champion check, weakness-driven selection, mastery-throttled graduation, self-throttling, and single-
anchor recalibration — are described in Section 3.3.




                                                  12
Algorithm 1 Mastery-throttled benchmark update (generation t → t+1).
Require: active benchmark Bt with curriculum levels; the champion and its per-task solve results;
    candidate pool P ; update threshold γ; mastery threshold τ ; replacement budget κ; step σ
Ensure: next benchmark Bt+1 and difficulty coefficient ct+1
 1: if the champion’s raw solve rate is below γ then
 2:     return Bt unchanged                                                        ▷ champion check
 3: end if
 4: D ← domains most failed across the whole archive                        ▷ population weaknesses
 5: R ← up to κ tasks of Bt solved by all agents this generation, lowest level first
 6: for each level ℓ do
 7:     tot[ℓ], sol[ℓ] ← champion’s total / solved counts on level ℓ
 8: end for
 9: A ← ∅
10: for each retired task q at level ℓ in R do
11:     mℓ ← sol[ℓ]/tot[ℓ]                                            ▷ recomputed after every swap
12:     if mℓ ≥ τ then
13:         ℓ⋆ ← ℓ + σ                                                                     ▷ graduate
14:     else
15:         ℓ⋆ ← ℓ                                                                   ▷ lateral refresh
16:     end if
17:     a ← unused task from P at level ℓ⋆ , preferring domains D
18:     if a = nil and ℓ⋆ ̸= ℓ then
19:         a ← unused task from P at level ℓ                                    ▷ fallback to lateral
20:     end if
21:     if a = nil then
22:         skip this swap
23:     else
24:         A ← A ∪ {a}; mark q for removal
25:         tot[ℓ] ← tot[ℓ] − 1; if the champion solved q then sol[ℓ] ← sol[ℓ] − 1      ▷ self-throttle
26:         tot[ℓ⋆ ] ← tot[ℓ⋆ ] + 1                                  ▷ added task assumed unsolved
27:     end if
28: end for
29: Bt+1 ← (Bt \ R) ∪ A
30: rt+1 ← raw score of the champion re-evaluated on Bt+1                             ▷ single anchor
31: ct+1 ← ct · rt / max(rt+1 , ϵ)                                ▷ compounds with an epsilon floor
32: return Bt+1 , ct+1



C    A worked example: an evolved subgoal-prover workflow (agent
     c141)
As a worked example we show agent c141, the late-stage child whose evolved workflow makes
the most explicit attempt at a standalone subgoal-prover workflow. Its meta agent added a
subgoal_prover.py module: after quick tactics and a short monolithic repair loop, the work-
flow asks the model for a lemma plan, proves the proposed lemmas one by one, and then tries to
assemble the final theorem from those lemmas (Listing 1). This is the clearest instance in the run
of the structured, node-bearing proof context that the proof-context contract is meant to make


                                                  13
inspectable.
  def solve_task(task, policy, runtime):
      body = _try_quick_tactics(task, runtime)         # 1. fast auto-tactics
      if body is not None:
          return _record(body, "auto_tactic")

      last_solution, ok, attempts, _ = _try_monolithic(
          task, policy, runtime, start_time, tool_text, verified_lemmas)
      if ok:                                      # 2. monolithic repair first
          proof_body = last_solution
          strategy = "monolithic"
      else:
          sub = _try_subgoal(task, policy, runtime, start_time,
                             tool_text, verified_lemmas)
          if sub[0]:                              # 3. explicit subgoal workflow
              proof_body, _, proof_nodes, edges = sub
              strategy = "subgoal"
          else:
              proof_body, ok = _try_safe_mode(
                  task, policy, runtime, start_time, verified_lemmas)
              strategy = "safe_fallback" if ok else "monolithic_fallback"

Listing 1: Core control flow of c141’s evolved solve_task: quick tactics, a short monolithic repair
loop, then an explicit subgoal-prover workflow with lemma planning, lemma proofs, and final
assembly.

    The subgoal prompt is more ambitious than a have-block parser: it asks for independent lemma
statements with explicit binders, then separately proves and assembles them (Listing 2).
  "Given a theorem, break it down into auxiliary lemmas. "
  "Each lemma should be a self-contained statement with all variables explicitly "
  "quantified. Do NOT use the theorem’s context implicitly. "
  "Output up to 5 lemmas as JSON objects with keys: name, statement, explanation."

Listing 2: c141’s subgoal-planning prompt (abridged): propose self-contained helper lemmas before
proving and assembling them.

     Two evolved design choices explain why this more explicit decomposition-based workflow was
nonetheless competed away. First, decomposition still runs after the monolithic route has failed, so
it is asked to recover exactly the hardest cases. Second, the separate lemma-plan, lemma-proving,
and assembly interfaces add new places where the proof can fail: JSON parsing, non-self-contained
lemma statements, and helper lemmas that cannot be introduced into the final Lean environment, as
well as longer prompts and a higher risk of timeout. The net effect is a structurally richer workflow
whose trace is more informative, but whose solve rate remains below the repair-centered champions
(cf. the lineage record in Appendix D).


D     Evolution record of the accepted lineage
Section C showed one evolved agent in detail; here we record the accepted lineage as an evolutionary
history, with representative rows for early generations and, for active generations 10–15, all evaluated
accepted children available at writing time. The goal is to show which workflow, tool, node-level
verification, and proof-context changes were proposed, which ones actually ran, and which ones
survived selection (Figure 2 and Table 3). The main lineage-level pattern is that compact repair
mechanisms survive, while richer decomposition-based workflows appear repeatedly but are usually

                                                  14
pruned. During most of the observed run, agents discuss decomposition-based workflows and per-
node verification yet defer them: the sparse pass/fail reward (Section 3.4) assigns no gradient
to proof structure, so an agent that maximizes solve rate often skips it. The highest raw-score
agent, c12, wrote out the exact binder fix that node-level verification requires and then skipped
it, improving instead through lemma tooling; a later champion (c39) reasoned that an isolated
sub-lemma “cannot be verified” because its variables are unbound and left it “for now.”

Table 2: Difficulty coefficient of the coevolving active benchmark. The coefficient is used for cross-
generation normalization and is not a held-out solve rate.

                    Gen 0   Gen 1    Gen 2      Gen 3    Gen 4   Gen 5   Gen 6   Gen 7   Gen 8    Gen 9   Gen 10    Gen 11   Gen 12   Gen 13    Gen 14     Gen 15
Difficulty coeff.   1.00    1.00         1.11   1.18     1.27    1.40    1.44     1.59   1.76      2.07    2.47      2.75     2.75     3.17         3.17    3.17




                                                                  c100           c145


                                                                  c99

                                                                  c46
                                                   c47
                                                                  c39
                                                                                 c96             c141
                                   c44             c45
                                                                  c26
                    c3                                                           c38
                                                                                                 c144
                                   c11             c12            c25
 seed                                                                            c86
                                                                                                 c96
                                   c40             c83            c101
                    c0
                                                                                 c43             c51          c52            c82              c92           c94
                                    c8             c93            c143

                                                                                                 c137        c146
                                                   c10            c24

                                                                                 c50             c140
                                                   c48            c41

                                                                  c22            c23             c37          c42
                                                   c98

                                                                  c19



Figure 2: Evolution tree for the accepted lineage. Bold nodes mark agents with decomposition-
based workflows. Darker node colors indicate agents evolved in later generations.




                                                                                  15
Table 3: Four-dimension evolution record of the accepted lineage (single coevolving run). Intent:
proposed in the agent’s mutation trace; Outcome: shipped, evaluated, and retained or lost under
selection. Raw = solve rate on that generation’s benchmark, whose difficulty coefficient rises 1.00 →
3.17 by active generation 15, so raw scores are not directly comparable across generations. Shaded
cells mark proposed changes that were not realized, not retained, or net-negative; un-shaded done
cells in the node-level verification column (c44, c47) mark genuinely Lean-certified sub-lemmas. The
workflow columns are restricted to the control-flow choice between repair and decomposition-based
workflows; Lean-name utilities are separated under mutable tools. Trace invalid means the emitted
proof context failed the validator’s grounding checks. The seed itself is not listed; c0 is the first
accepted child. ⋆ generation champion, ⋆⋆ highest raw-score agent. Earlier rows are representative;
for active generations 10–15, all evaluated accepted children available at writing time are shown.

                       1. Workflow             2. Mutable tools            3. Node-level verif.   4. Proof-context depth
 Agent        Intent         Outcome        Intent       Outcome       Intent          Outcome    Intent         Outcome
 (raw)

 c0 (.368)    monolithic     done:          lemma-name part.:          –               –          –              – (flat, 1
              repair         simple retry   probe      inlined                                                   node)
                             loop                      #check
 c3 (.526)    error-         done:          lemma      done:           –               –          –              – (0 math
              feedback       repair stays   existence  #check +                                                  nodes)
              repair         monolithic     helper     source
                                                       search
 c8 ⋆ (.553) stronger        done:          verified   part.:          annotate /   n/i:         structured      part.: mild
             repair loop     bounded        signatures mostly          decompose    text-only    context         (2 math
                             repair, no                prompt-side     into nodes   labels (“un-                 nodes)
                             decomp.                                                verified”)
 c10 (.447)   repair         part.:        decl cache / part.:       whole          part.:       –               – (flat)
              hardening      repair policy FD guard     inlined, no  theorem as degenerate
                             regresses                  durable tool one node       (node ≡
                                                        API                         proof)
 c11 (.487)   repair +       done:         batch        done: edits  build +        n/i: 7 nodes deep            part.:
              shallow        repair first; lemma        tools.py     isolate-verify built,       subgoal tree    richest (7
              decomp.        have nodes verification                 have           binder-                      nodes) but
                             post hoc                                sub-nodes      isolation                    unverified
                                                                                    fails
 c12 ⋆⋆       compact        done:          verified    part.:       wrote binder n/i:           subgoal tree    part.: ∼5
 (.618)       repair +       repair wins;   lemma       prompt-side, fix +          skipped; 0                   nodes but
              decomp.        decomp.        catalogue   no new tool planned de- verified                         tooling
              idea           skipped                    API          composition sub-nodes                       steps, not
                                                                     verification                                math
 c19 (.368)   large repair   n/i: 10        expanded    n/i: no      whole-         part.:       –               – (flat)
              budget         attempts       lemma cache durable      theorem        degenerate
                             hurt                       advantage    node
                             stability
 c22 †        decomp.        n/i:         grep index / n/i: guard isolate-verify n/i:             LLM            n/i: skipped
 (.368)       fallback       crash-prone, lookup       blocks       each have    deferred         sub-lemma      (“large
                             not selected              subprocess; subgoal       (“too risky”)    skeleton       change”)
                                                       tool dropped                               then
                                                                                                  assemble
 c26 ⋆        repair →       done: 8        expanded    done:          per-subgoal    part.: runs subgoal tree   part.: built,
 (.566)       decomp.        repair         verified-   prefetch +     verify (first  but hangs                  often
              fallback       attempts,      lemma tools source         real           on hard                    monolithic
                             then 4                     search         attempt)       tasks, falls               fallback
                             decomp.                                                  back
 c39 ⋆        repair with    done:          lemma        done: edits   isolate-verify n/i:         richer        part.:
 (.487)       deferred       repair         #check /     tools.py      but “vars      deferred;    context       label-only
              decomp.        remains        resolve                    unbound”       have-parsed                nodes
                             main path                                                labels only

                                                                                                   Continued on next page



                                                               16
Table 3: Four-dimension evolution record of the accepted lineage (continued).

                       1. Workflow            2. Mutable tools            3. Node-level verif.      4. Proof-context depth
 Agent        Intent        Outcome        Intent       Outcome       Intent         Outcome        Intent         Outcome
 (raw)

 c41 ⋆        monolithic    done: no       lemma_       n/i: mostly   subgoal        n/i:           subgoal tree – (shallow, 1
 (.421)       repair        decomp.        exists       inlined;      nodes +        cosmetic                    claim)
                            route          / cache      tools.py      per-node       flag only
                                                        untouched     verify
 c44 ⋆        decomp.       done:          cached       done: edits   verify self-   done: 141 real decom- done:
 (.408)       workflow      sublemma-      #check       tools.py      contained      certified     position tree verified
                            first          existence                  subgoals       (root still                 shallow
                            workflow                                                 null)                       graph
 c47 ⋆        extend c44    done:          verify       done: edits   verify each    done: 150 richest tree part.: 173
 (.434)       decomp.       two-tier       searched     tools.py      subgoal        certified;    (avg 17)      verified, 958
                            decomp.        lemmas                                    rest                        label-only
                            workflow                                                 label-only
 c52 ⋆        back to       done:          complete    done: edits    (not           n/i:          –             – (flat, 2
 (.329)       monolithic    shorter        lemma index tools.py       selected)      inherited de-               nodes)
              repair        repair;                                                  composition
                            decomp.                                                  dead, 0/76
                            inactive                                                 fires
 c82 (.145)   repair c52    n/i: over-    unknown-      done:       inherited        n/i: trace    decomp.       part.: high
              decomp.       constrained;  lemma         stricter    subgoal          valid but     supports      score,
              path          11/76         rejection +   checks,     checks           low solve                   shallow
                                          short         force_short                  rate                        graph
                                          prompts
 c83 (.224)   verify-and-   done:         lemma_ +      part.:        –              –              repair         part.:
              repair loop   simple Lean exists          backend                                     context        shallow;
                            feedback      prompt        errors                                                     weaker than
                            loop          hints         remain                                                     parent
 c86 ⋆        repair        done:         lemma_ /      done: new     node           n/i: trace     shallow        part.: many
 (.382)       hardening     lemma         checker       helper,       feedback       invalid; no    supports       events, not a
                            pre-check + symbol grep     safe-lemma                   durable                       deep graph
                            bounded                     cleanup                      subgoal
                            repair; no                                               verification
                            decomp.
                            route
 c92 (.040)   very large    n/i: 20–25 signature        n/i: prompt proof-node       n/i: invalid   shallow        n/i: mostly
              repair        attempts      retrieval     bloat       checks           trace          supports       failures
              budget        collapse to                 dominates
                            3/76
 c93 ⋆        verify-and-   done:         def/abbrev    done:         –              –              repair         part.:
 (.211)       repair loop   simple Lean- index +        cached                                      context        inspectable
                            feedback      repair        Lean-name                                                  but shallow
                            loop, low     history       checks
                            score
 c94 (.066)   simplify      done: fast    source grep   part.: no     –              –              flat context   n/i: only
              after c92     monolithic    idea          recovery                                                   5/76
                            workflow,
                            still weak
 c96 (.290)   safe-mode     done:         lemma-        done:         inherited      part.:        shallow         part.: no
              repair        verified-only checker       broader       subgoal        parser fixed, supports        new deep
                            fallback      cache         namespace     parser         not                           graph
                            after c95                   search                       dominant
                            crash
 c97 ⋆        decomp.-      done: plan verified         part.: safer verify each     done:          subgoal tree part.: real
 (.303)       first         subgoals,     catalogue     prompt +     helper          node-level                  but shallow,
              workflow      prove,                      lemma        lemma           feedback;                   no break-
                            assemble;                   filtering                    compose                     through
                            fallback                                                 fragile
                            repair

                                                                                                    Continued on next page



                                                             17
Table 3: Four-dimension evolution record of the accepted lineage (continued).

                        1. Workflow         2. Mutable tools            3. Node-level verif.     4. Proof-context depth
 Agent         Intent        Outcome     Intent        Outcome      Intent        Outcome        Intent      Outcome
 (raw)

 c98 (.224)    multi-      done: more FD guard + part.: fixes       per-node      part.: self-   math        part.:
               sample      attempts + lemma          engineering,   check         contained      context     shallow,
               repair      namespace ranking         not solve                    nodes                      trace invalid
                           scan, weak                rate                         attempted
                           score
 c99 ⋆       repair +      done: c47     fake-lemma done: name      inherited     part.: not a shallow       part.:
 (.290)      inherited     branch        autocorrect map +          subgoal       new certified supports     stable but
             decomp.       keeps re-                 prompt         checks        graph                      not deeper
                           pair/subgoal              pitfalls
                           attempts
 c100 (.263) simplify c47 done: plain source         done: grep     inherited     part.: no      shallow     part.: high
             branch        retry +       signatures  exact          checks        new node       supports    context,
                           early                     declarations                 route                      lower solve
                           unknown-
                           lemma
                           rejection
 c101 (.224) repair c83    done:         cached      done:          –             n/i: 1200s     shallow     part.: no
             branch        concise retry lemma index forbidden-                   timeout        repair      structural
                           + reject bad              name list                    appears        context     gain
                           best proofs
 c137 (.171) anti-halluc. n/i: stricter static       done:          have-node     n/i: trace     shallow     n/i: low
             repair        checks lower lemma scan prompt +         extraction    invalid, no    supports    solve rate,
                           solve rate    + bad-name loop edits                    isolated                   no depth
                                         rejection                                node checks                gain
 c140 (.211) repair + lint done:         safe-lemma part.:          have-node     n/i: trace     shallow     part.:
             feedback      auto-patch list / native prompt-side     extraction    invalid        supports    inspectable
                           then LLM      guard       guard                                                   but not
                           repair, still                                                                     deeper
                           weak
 c141 (.250) repair        n/i:          lemma       part.:        subgoal-level part.:          subgoal tree n/i: many
             decomp.       decomp.       checker +   helper        verification helper                        tasks emit
             child         route         subgoal     tooling                     checks exist,                no final
                           remains       prover      integrated                  final                        proof body
                           weak                                                  assembly
                                                                                 weak
 c143 ⋆      c93 repair + done:          verified      done:       proof-        part.:          shallow     part.:
 (.276)      structured   lemma          lemma         cached name context       nodes           decomp.     modest gain
             prompt       checking       feedback      checks in   nodes         logged, not     hints       over parent
                          plus                         loop                      a certified
                          monolithic                                             graph
                          repair
 c144 ⋆      proof-plan   done: plan     lemma         done:       claimed        n/i: flag set, shallow     part.: best
 (.303)      prompt +     guides         checker       verified-   have nodes     but no         supports    score, still
             repair       monolithic     integration   lemma hints                isolated                   no deep
                          repair; best                 + stricter                 node                       DAG
                          held-out                     prompt                     verification
                          solve rate
 c145 (.211) c100         done: have-    safe-lemma done:         extract have n/i: no           proof-      part.:
             structured   extraction,    set + hallu- rejects     subgoals     node-verif.       context     richer labels,
             context      weak solve     cination     invented                                   DAG         no gain in
                          rate           filters      names early                                            solve rate
 c146 (.158) cached-      n/i: extra     lemma cache done: cache lemma /       n/i: trace        shallow     n/i:
             example      machinery      + examples wired into    error        invalid, no       supports    timeout-
             repair       lowers solve                workflow    feedback     node checks                   prone, only
                          rate                                                                               12/76


    †
        c22’s lemma index invoked subprocess, which the mutable-process guard blocks; the uncaught exception crashed
nearly every task, which is why c22 fell to the seed-level score. Its descendant c23 then removed the index and the


                                                            18
decomposition scaffolding in favor of a simpler robust loop.


References
 [1] Benjamin S. Bloom. Learning for mastery. Evaluation Comment, 1(2):1–12, 1968.

 [2] Jonathan C. Brant and Kenneth O. Stanley. Minimal criterion coevolution: A new approach to
     open-ended search. In Proceedings of the Genetic and Evolutionary Computation Conference,
     pages 67–74, 2017.

 [3] Guangyao Chen, Siwei Dong, Yu Shu, Ge Zhang, Jaward Sesay, Börje F. Karlsson, Jie Fu,
     and Yemin Shi. Autoagents: A framework for automatic agent generation. In Proceedings
     of the Thirty-Third International Joint Conference on Artificial Intelligence (IJCAI), 2024.
     arXiv:2309.17288.

 [4] Yixing Chen, Yiding Wang, Siqi Zhu, Haofei Yu, Tao Feng, Muhan Zhang, Mostofa Patwary,
     and Jiaxuan You. Multi-agent evolve: Llm self-improve through co-evolution. arXiv preprint
     arXiv:2510.23595, 2025.

 [5] Jui-Hui Chung, Ziyang Cai, Zihao Li, Qishuo Yin, Rohit Agarwal, Simon Park, Rodrigo Porto,
     Narutatsu Ri, Ziran Yang, Shange Tang, Xingyu Dang, Hongzhou Lin, Mengdi Wang, Danqi
     Chen, Chi Jin, Liam H. Fowl, and Sanjeev Arora. Goedel-architect: Streamlining formal
     theorem proving with blueprint generation and refinement. arXiv preprint arXiv:2606.06468,
     2026.

 [6] Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre Bayen, Stuart Russell, Andrew
     Critch, and Sergey Levine. Emergent complexity and zero-shot transfer via unsupervised en-
     vironment design. In Advances in Neural Information Processing Systems (NeurIPS), 2020.
     arXiv:2012.02096.

 [7] Chrisantha Fernando, Dylan Banarse, Henryk Michalewski, Simon Osindero, and Tim Rock-
     täschel. Promptbreeder: Self-referential self-improvement via prompt evolution. arXiv preprint
     arXiv:2309.16797, 2023.

 [8] Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong
     Liu, Jiahao Qiu, Xuan Qi, Yiran Wu, Hongru Wang, Han Xiao, Yuhang Zhou, Shaokun Zhang,
     Jiayi Zhang, Jinyu Xiang, Yixiong Fang, Qiwen Zhao, Dongrui Liu, Qihan Ren, Cheng Qian,
     Zhenhailong Wang, Minda Hu, Huazheng Wang, Qingyun Wu, Heng Ji, and Mengdi Wang. A
     survey of self-evolving agents: What, when, how, and where to evolve on the path to artificial
     super intelligence. Transactions on Machine Learning Research, 2026. arXiv:2507.21046.

 [9] Jiacheng Guo, Ling Yang, Peter Chen, Qixin Xiao, Yinjie Wang, Xinzhe Juan, Jiahao Qiu,
     Ke Shen, and Mengdi Wang. Genenv: Difficulty-aligned co-evolution between llm agents and
     environment simulators. arXiv preprint arXiv:2512.19682, 2025.

[10] Shengran Hu, Cong Lu, and Jeff Clune. Automated design of agentic systems. arXiv preprint
     arXiv:2408.08435, 2024.

[11] Yukun Huang, Leonardo F. R. Ribeiro, Momchil Hardalov, Bhuwan Dhingra, Markus Dreyer,
     and Venkatesh Saligrama. Deepfact: Co-evolving benchmarks and agents for deep research
     factuality. arXiv preprint arXiv:2603.05912, 2026. Accepted at ACL 2026.

                                                         19
[12] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser,
     Aja Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-
     level formal mathematical reasoning with reinforcement learning. Nature, 651:607–613, 2026.
     Published online 2025.
[13] Alex Iacob, Andrej Jovanović, William F. Shen, Daniel Burkhardt, Meghdad Kurmanji, Nurbek
     Tastan, Lorenzo Sani, Niccolò Alberto Elia Venanzi, Ambroise Odonnat, Zeyu Cao, Bill Marino,
     Xinchi Qiu, and Nicholas D. Lane. The red queen gödel machine: Co-evolving agents and their
     evaluators. arXiv preprint arXiv:2606.26294, 2026.
[14] Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik,
     Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding
     formal theorem provers with informal proofs. In International Conference on Learning Repre-
     sentations, 2023. arXiv:2210.12283.
[15] Po-Nien Kung, Linfeng Song, Dawsen Hwang, Jinsung Yoon, Chun-Liang Li, Simone Severini,
     Mirek Olšák, Edward Lockhart, Quoc V. Le, Burak Gokturk, Thang Luong, Tomas Pfister,
     and Nanyun Peng. Leap: Supercharging llms for formal mathematics with agentic frameworks.
     arXiv preprint arXiv:2606.03303, 2026.
[16] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang,
     Yihan Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu
     Yang, Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-
     v2: Scaling formal theorem proving with scaffolded data synthesis and self-correction. arXiv
     preprint arXiv:2508.03613, 2025.
[17] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang,
     Adam Zsolt Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas
     Mehrabian, M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies,
     Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. Alphaevolve: A coding agent for scien-
     tific and algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.
[18] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem prov-
     ing. arXiv preprint arXiv:2009.03393, 2020.
[19] Rémy Portelas, Cédric Colas, Lilian Weng, Katja Hofmann, and Pierre-Yves Oudeyer. Auto-
     matic curriculum learning for deep rl: A short survey. In International Joint Conference on
     Artificial Intelligence (IJCAI), 2020. arXiv:2003.04664.
[20] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang,
     Yuxuan Liu, Wenjun Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025.
[21] Maxime Robeyns, Martin Szummer, and Laurence Aitchison. A self-improving coding agent.
     arXiv preprint arXiv:2504.15228, 2025.
[22] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang,
     Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program
     search with large language models. Nature, 625:468–475, 2024.

                                               20
[23] Jürgen Schmidhuber. Gödel machines: Fully self-referential optimal universal self-improvers.
     In Ben Goertzel and Cassio Pennachin, editors, Artificial General Intelligence, Cognitive Tech-
     nologies, pages 199–226. Springer, 2007.

[24] Yu Shang, Yu Li, Keyu Zhao, Likai Ma, Jiahe Liu, Fengli Xu, and Yong Li. Agentsquare:
     Automatic llm agent search in modular design space. In International Conference on Learning
     Representations, 2025. arXiv:2410.06153.

[25] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as
     copilots for theorem proving in lean. In International Conference on Neuro-symbolic Systems
     (NeuS), 2025. arXiv:2404.12534.

[26] Zhengwei Tao, Ting-En Lin, Xiancai Chen, Hangyu Li, Yuchuan Wu, Yongbin Li, Zhi Jin, Fei
     Huang, Dacheng Tao, and Jingren Zhou. A survey on self-evolution of large language models.
     arXiv preprint arXiv:2404.14387, 2024.

[27] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers
     on the putnam mathematical competition. In Advances in Neural Information Processing
     Systems (NeurIPS) Datasets and Benchmarks, 2024. arXiv:2407.11214.

[28] Lev S. Vygotsky. Mind in Society: The Development of Higher Psychological Processes. Harvard
     University Press, 1978. Edited by Michael Cole, Vera John-Steiner, Sylvia Scribner, and Ellen
     Souberman.

[29] Rui Wang, Joel Lehman, Jeff Clune, and Kenneth O. Stanley. Paired open-ended trailblazer
     (poet): Endlessly generating increasingly complex and diverse learning environments and their
     solutions. arXiv preprint arXiv:1901.01753, 2019.

[30] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-
     augmented language models. In Advances in Neural Information Processing Systems (NeurIPS)
     Datasets and Benchmarks, 2023. arXiv:2306.15626.

[31] Ruiyi Yang, Zechen Li, Hao Xue, Imran Razzak, and Flora D. Salim. Mage: Multi-agent
     self-evolution with co-evolutionary knowledge graphs. arXiv preprint arXiv:2605.10064, 2026.

[32] Xunjian Yin, Xinyi Wang, Liangming Pan, Li Lin, Xiaojun Wan, and William Yang Wang.
     Gödel agent: A self-referential agent framework for recursively self-improvement. In Proceedings
     of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
     Papers), pages 27890–27913, Vienna, Austria, 2025. Association for Computational Linguistics.
     arXiv:2410.04444.

[33] Siyu Yuan, Kaitao Song, Jiangjie Chen, Xu Tan, Dongsheng Li, and Deqing Yang. Evoagent:
     Towards automatic multi-agent generation via evolutionary algorithms. In Annual Confer-
     ence of the Nations of the Americas Chapter of the Association for Computational Linguistics
     (NAACL), 2025. arXiv:2406.14228.

[34] Eric Zelikman, Eliana Lorch, Lester Mackey, and Adam Tauman Kalai. Self-taught opti-
     mizer (stop): Recursively self-improving code generation. In Conference on Language Modeling
     (COLM), 2024. arXiv:2310.02304.


                                                 21
[35] Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. Darwin gödel machine:
     Open-ended evolution of self-improving agents. arXiv preprint arXiv:2505.22954, 2025.

[36] Jenny Zhang, Bingchen Zhao, Wannan Yang, Jakob Foerster, Jeff Clune, Minqi Jiang, Sam
     Devlin, and Tatiana Shavrina. Hyperagents. arXiv preprint arXiv:2603.19461, 2026.

[37] Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xionghui Chen, Jiaqi Chen, Mingchen
     Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, and Chenglin
     Wu. Aflow: Automating agentic workflow generation. In International Conference on Learning
     Representations, 2025. arXiv:2410.10762.

[38] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: A cross-system benchmark for
     formal olympiad-level mathematics. In International Conference on Learning Representations,
     2022. arXiv:2109.00110.




                                              22
