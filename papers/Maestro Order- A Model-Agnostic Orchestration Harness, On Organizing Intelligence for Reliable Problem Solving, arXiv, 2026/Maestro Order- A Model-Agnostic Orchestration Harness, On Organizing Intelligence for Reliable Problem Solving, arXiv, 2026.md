                                                   Maestro Order: A Model-Agnostic Orchestration Harness
                                                                                On Organizing Intelligence for Reliable Problem Solving
                                                                                                                    Hidayet Aksu
                                                                                                              hidayetaksu@gmail.com

                                         Abstract                                                                           hallucination, the confident generation of incorrect or unsupported
                                         A single forward pass of a capable model is a fast, fluent, and un-                content, and the compounding of small per-step error rates that
                                         reliable problem-solver: it is right often enough to be useful and                 makes long-running, multi-step jobs fail almost surely without
                                         wrong often enough to be dangerous; in language models, such                       correction.
                                         confident errors are known as hallucinations. We present Maestro                       This paper is the applied counterpart to a companion theory
                                         Order, a model-agnostic orchestration harness that turns unreliable                report, Odds Law [1], which shows that a small algebra of four
arXiv:2606.23983v1 [cs.CR] 22 Jun 2026




                                         solvers into reliable problem-solving systems by composing them                    combinators (sequential decomposition, parallel ensembling, ver-
                                         according to four structural primitives (decompose, ensemble, ver-                 ification gating, and recursion) generates the organizations that
                                         ify, and recurse) and a budget-aware controller that decides where                 solve problems reliably, and that reliability flows through them
                                         to spend compute. The harness treats any model as a black-box base                 by explicit laws (most importantly, a verification gate multiplies
                                         solver behind a uniform interface, layers a verifier ensemble whose                the odds of correctness by the verifier’s likelihood ratio). Here we
                                         discrimination is measured online, and allocates verification and                  turn those laws into a running system: a harness that wraps any
                                         voting to the stages with the highest marginal reliability per unit                model as a base solver and composes solvers and verifiers under a
                                         cost. We give the architecture, the message and state schema, the                  controller that spends compute where it buys the most reliability.
                                         controller algorithm, and the engineering that makes it determinis-
                                                                                                                               Why a harness, not a better model. Three properties make or-
                                         tic, observable, and fault-tolerant. We then specify an evaluation
                                                                                                                            chestration attractive and complementary to improving the base
                                         methodology (reliability at fixed cost, coverage, calibration, and
                                                                                                                            model. (i) Generate–verify asymmetry: for many tasks, checking a
                                         ablations) and report results from a faithful Monte Carlo simulation
                                                                                                                            candidate (run the tests, recompute the sum, search for a counterex-
                                         of the harness over a parameterized solver/verifier model. The sim-
                                                                                                                            ample) is far cheaper and more reliable than producing it; this is
                                         ulation reproduces the predicted laws quantitatively: verification
                                                                                                                            exactly the regime where verification gating pays off. (ii) Test-time
                                         amplifies reliability geometrically (e.g. 0.55 → 0.98 with two gates,
                                                                                                                            compute is elastic: a harness can trade more calls for more reliability
                                         → 0.999 with four), voting helps only above chance and is limited
                                                                                                                            on the instances that need it, and abstain or escalate on the rest. (iii)
                                         by shared errors, and a budget-aware controller reaches a target
                                                                                                                            Model-agnosticism: the same scaffolding improves whatever model
                                         reliability at a small fraction of the cost of voting alone by selecting
                                                                                                                            sits behind the interface, and survives model upgrades.
                                         the cheapest mechanism for each regime. We close with failure
                                         modes (verifier gaming, correlated errors, and decomposition er-                      Contributions.
                                         ror compounding) and concrete guidance: build robust checkers,
                                         diversify solvers, and let the controller put compute where the in-                     • A model-agnostic harness architecture (§4–§6) that instanti-
                                         formation is. Maestro Order is the framework layer of a two-part                          ates the four combinators as composable components (plan-
                                         program (Theory: Odds Law → Framework: Maestro Order),                                    ner, solver pool, verifier ensemble, aggregator, controller,
                                         built on the laws of the companion Odds Law report.                                       blackboard, and tool sandbox) behind a uniform solver in-
                                                                                                                                   terface.
                                         Keywords                                                                                • A budget-aware controller (§7) that allocates voting and ver-
                                                                                                                                   ification by greedy marginal log-odds per unit cost, the op-
                                         LLM orchestration, agents, verification, self-consistency, test-time
                                                                                                                                   erational form of the theory’s water-filling optimum (spend
                                         compute, reliability, ensembles, scaffolding, evaluation, hallucina-
                                                                                                                                   where the return is highest until all options return the
                                         tion mitigation, long-horizon agents
                                                                                                                                   same), with online estimation of verifier discrimination Λ.
                                         1    Introduction                                                                       • An engineering account (§11) of determinism, idempotency,
                                                                                                                                   concurrency, cost accounting, and tracing required to make
                                         Modern models answer hard questions in one shot with impressive
                                                                                                                                   reliability measurable and reproducible.
                                         fluency and uneven reliability. For deployment, where a wrong
                                                                                                                                 • An evaluation methodology and simulation study (§12–§13)
                                         answer has a cost, the relevant question is not “how good is the
                                                                                                                                   that reproduces the predicted reliability laws and quantifies
                                         model on average?” but “how do we build a system whose answers
                                                                                                                                   the cost of voting vs. verification, the diversity floor, and
                                         we can trust at a known cost?” The same question recurs across
                                                                                                                                   the value of abstention.
                                         substrates: a research group made of fallible people, a compiler
                                                                                                                                 • A catalog of failure modes and mitigations (§15): verifier
                                         made trustworthy by its test suite, a distributed job made correct
                                                                                                                                   gaming (Goodhart), correlated solver errors, and decompo-
                                         by re-execution. The answer, in every case, is organization: many
                                                                                                                                   sition error compounding.
                                         unreliable attempts, arranged so their errors are caught and out-
                                                                                                                                 • An open-source release of the harness code, simulation, and
                                         voted. Two failure patterns make this urgent for language models:
                                                                                                                                   reproduction scripts at https://github.com/hidayetaksu/
                                         ∗ Code and reproduction scripts: https://github.com/hidayetaksu/maestro-order             maestro-order.
2   Background and Related Work                                           Table 1: The four combinators and their harness realization.
                                                                          The reliability law column summarizes the companion the-
   Eliciting and aggregating reasoning. Chain-of-thought prompt-
                                                                          ory [1].
ing elicits intermediate steps [2]; self-consistency samples many
chains and takes the majority answer, the voting combinator in
practice [3]. Tree-of-thoughts searches over partial solutions with           Combinator      Harness component                Reliability law
look-ahead [4], a decomposition-plus-search organization.                     Sequential      Planner / decomposer             errors compound ( 𝜌𝑖 )
                                                                                                                                                 Î
                                                                              Parallel        Voter / aggregator               amplify if 𝑝 > 12
   Acting, checking, and refining. ReAct interleaves reasoning with
                                                                              Verify          Verifier ensemble + gate         odds × Λ per gate
tool actions [5]; Reflexion [6] and Self-Refine [7] iterate generate–         Recurse         Recursive dispatch               union bound over nodes
critique–revise loops; multi-agent debate has models cross-examine
each other [8]. These are instances of verification and refinement
with the model (or a tool) as verifier.                                                                        problem 𝑥


                                                                                                               Controller                    Blackboard
   Verifiers and process supervision. Training explicit verifiers im-                                       (budget, policy)                (state, traces)
proves math word-problem reliability [9]; process-level reward
models that check each step outperform outcome-only checks [10];
                                                                                                              Planner /
“LLM-as-judge” uses a model to score candidates [11]. Our harness                                            Decomposer
treats any such checker as a gate and measures its discrimination
Λ online.
   Tools, retrieval, and code execution. Grounding answers in re-                           Solver pool                          Verifier
                                                                                           (roles, temps)                       ensemble
trieval [12], tool use [13], and program execution / unit tests [14]
supplies robust verifiers whose false-acceptance is bounded indepen-                                         Aggregator /                   Tool sandbox
dently of how the candidate was produced, which is precisely the                       refine/escalate          Gate                        (exec, search)

property the theory shows is needed under optimization pressure.
Retrieval grounding is also a primary defense against hallucina-                                               answer / ⊥

tion [15].
   Reliable systems from unreliable parts. The organizing idea pre-       Figure 1: Harness architecture. The controller allocates a
dates models: von Neumann’s reliable automata from unreliable             compute budget across decomposition, voting, and verifica-
components [16], Condorcet’s jury theorem [17], and divide-and-           tion; the blackboard holds shared state and traces; the tool
conquer in distributed systems [18]. Our harness is a contemporary,       sandbox supplies robust verifiers (execution, tests, search).
model-agnostic realization, and our companion paper [1] supplies          Arrows show data and control flow; the refine/escalate edge
the reliability calculus it optimizes.                                    closes the verify loop.

   How this work differs. Most of the techniques above are studied
and deployed in isolation: self-consistency or a verifier or refine-      a discriminating checker exists: a single gate with Λ = 6 outper-
ment, each used as a separate technique. Our contribution is to treat     forms dozens of votes for a near-threshold solver. Third, spend at
them as instances of one algebra and to put a controller in charge of     the margin: allocate the next unit of compute to whichever stage
choosing among them per instance under an explicit budget, guided         currently offers the largest reliability gain per call. The controller
by the reliability laws. Two consequences distinguish the approach.       (§7) implements all three.
First, the harness measures verifier discrimination Λ online and
credits each mechanism only with the amplification its measured           4    Harness Architecture
quality supports, rather than fixing a pipeline in advance. Second,       Figure 1 shows the components. Everything is built on one abstrac-
by reporting reliability at a measured cost and selecting the cheapest    tion.
configuration that meets a target, it makes the cost–reliability trade-
off an explicit, tunable quantity instead of an implicit side effect of      The solver interface. A base solver exposes solve(task, ctx)
a prompt template. The aim is not a new trick but a principled way        -> {answer, score, trace, cost}. Any model, tool, or sub-
to compose the existing ones.                                             harness implements it, so components compose uniformly and the
                                                                          controller can treat a whole subtree as a single solver. score is a
3   From Algebra to Architecture                                          self-reported confidence (used only as a weak prior); trace feeds
The harness is a direct compilation of the four combinators into          the blackboard; cost is the realized call/token count.
runtime components. Table 1 gives the correspondence; the rest               The blackboard record. All components read and write a single
of the paper elaborates each row and the controller that composes         structured record, which is also the unit of tracing and replay:
them.
   Three design principles follow from the laws. First, check more           Planner / decomposer. Given a task, the planner optionally emits
than you decompose: since sequential decomposition can only lose          a typed plan: a DAG of subtasks with dependencies and a recom-
reliability, every decomposition boundary should be paired with a         bination step. Decomposition is applied only when the planner’s
verifier that restores it. Second, prefer verification to voting when     confidence in a clean split is high, since unguarded decomposition
Maestro Order: A Model-Agnostic Orchestration Harness


Solve {                                                                    never as a silent accept. This keeps the false-acceptance rate 𝛼
  task:    {id, type, input, deps[]}                                       bounded by the verifier’s genuine error rather than by infrastruc-
  budget: {max_calls, target_rel, lambda}
                                                                           ture flakiness, which is what makes the discrimination Λ = 𝛽/𝛼
  cands:   [{answer, score, trace, cost}]
  verdicts:[{verifier_id, accept, score,
                                                                           meaningful and stable. A harness that failed open would see its Λ
             est_beta, est_alpha}]                                         collapse under load exactly when reliability matters most.
  state:   {logodds, calls, coverage}
                                                                              I3: Monotone confidence. Adding work never decreases the
  result: {answer | ABSTAIN, confidence}
                                                                           system’s information about an instance: a new vote or gate can
}
                                                                           only sharpen the posterior, and the controller never discards
                                                                           evidence. This guarantees that spending more budget weakly
Figure 2: Blackboard record (simplified). The controller reads
                                                                           improves reliability (the refinement order of the theory), so the
state.logodds and per-mechanism marginal estimates to
                                                   ˆ 𝛼ˆ used to            cost–reliability curve is monotone and the controller’s greedy
decide the next action; verdicts carry the online 𝛽,                       ascent is well-defined.
compute b Λ.
                                                                              I4: Budget conservation and accountability. Every call is attributed
                                                                           to a stage and counted against the budget before it is made; the
compounds error (Table 1); each subtask boundary is annotated              controller cannot overspend, and every reported reliability number
with the verifier to apply on recombination.                               has an associated, measured cost. Reliability claims without cost
   Solver pool. A configurable set of solver roles (for example, dif-      are meaningless, so the two are always reported together.
ferent prompts, temperatures, tools, or distinct models) provides             I5: Determinism up to declared randomness. Given fixed seeds
the diversity that voting needs. The pool composition is the main          and backend versions, a solve is replayable bit-for-bit from its trace.
control on error correlation 𝛾 (§13); pools of near-identical solvers      Randomness enters only where declared (sampling temperatures,
vote poorly.                                                               vote seeds), so experiments are reproducible and regressions are
   Verifier ensemble. One or more verifiers, each a checker return-        diagnosable. These five invariants are the contract every component
ing accept/reject with a score: deterministic tools (unit tests, type-     signs; the mechanisms below are implementations that honor it.
checkers, math re-evaluation, retrieval corroboration) and model-
based critics. Each verifier’s completeness 𝛽 and false-acceptance 𝛼       6   Reliability Mechanisms
are estimated online (§7); the gate uses the calibrated log-likelihood     The harness exposes the combinators as mechanisms the controller
ratio as its acceptance score.                                             can deploy per instance.
   Aggregator / gate. Combines candidates: plurality or score-                Self-consistency voting. Sample 𝑛 diverse candidates and return
weighted voting, verified selection (return the highest-scoring            the plurality answer; reliability rises with 𝑛 when per-sample cor-
accepted candidate), or all-accept gating for amplification. Emits an      rectness exceeds 12 and errors are diverse (§13). Cheap, model-only,
answer or ⊥ (abstain) with a calibrated confidence.                        but bounded by the correlation floor.
   Blackboard and tool sandbox. A shared store holds intermediate              Verified selection and gating. Run candidates through the ver-
results, verifier verdicts, and a full execution trace for observability   ifier ensemble; either select the best accepted candidate or, for
and replay. The tool sandbox executes untrusted code and runs              amplification, require all 𝑘 gates to accept, regenerating otherwise
searches in isolation, supplying the robust verifiers the theory priv-     (Algorithm 1). Each accepted gate multiplies the odds of correctness
ileges.                                                                    by its Λ.

5    Design Rationale and System Invariants                                   Iterative refinement. On rejection, return the verifier’s critique
A reliability harness is only trustworthy if its guarantees hold           to the solver and resample, a generate–critique–revise loop. Re-
regardless of what the wrapped model does. We therefore design             finement raises the per-attempt success probability 𝑝, which com-
around a small set of invariants that the components must preserve         pounds with gating.
and that the companion theory [1] shows are sufficient for the                Debate and cross-examination. Independent solvers critique each
reliability laws to apply.                                                 other’s candidates; disagreement is a cheap signal that routes an
   I1: Confidence is calibrated log-odds. Every commitment carries a       instance toward more verification or abstention.
confidence that is, after calibration, the true log-odds of correctness.      Abstention and escalation. When the accumulated log-odds score
This single invariant makes the rest composable: gates add to it           falls below a calibrated threshold, the harness abstains or escalates
(the odds law), abstention thresholds it (Chow’s rule), and the con-       to a stronger (costlier) sub-organization: selective answering on the
troller maximizes it per unit cost. Components that cannot expose          risk–coverage frontier (§13).
a calibrated score are wrapped by a calibration map fit on held-out
data; uncalibrated raw scores are never used for decisions, only as        7   The Budget-Aware Controller
weak priors.
                                                                           The controller decides, per instance, how to spend a compute budget
  I2: Fail closed. Any ambiguity, such as a tool error, a timeout, a       𝜅 across the mechanisms. By the companion theory the reliability-
malformed candidate, or a verifier crash, is treated as a rejection,       maximizing allocation equalizes the marginal log-odds gain per
    1: input: generator 𝑔, verifiers 𝑣 1 ..𝑣 𝑘 , budget 𝑇                    Prefer ground-truth checks. The most robust verifiers reduce to ex-
    2: for 𝑡 = 1 to 𝑇 do                                                  ecuting a specification rather than judging plausibility. For code, run
    3:    𝑎 ← 𝑔.solve(𝑥)                      ⊲ sample a candidate        the candidate against unit tests, property-based tests, type-checkers,
    4:    if ∀𝑖 : 𝑣𝑖 .accept(𝑥, 𝑎) then                                   and sanitizers in the sandbox; for mathematics, re-evaluate numeri-
              return 𝑎 with odds 𝑖 Λ𝑖 applied
                                    Î
    5:                                                                    cally, check units and boundary cases, or machine-check a proof; for
    6:    end if                                                          factual claims, corroborate against retrieved sources and require ci-
    7: end for                                                            tation support. The defining property is that their false-acceptance
    8: return ⊥                         ⊲ abstain after 𝑇 rejections      rate is bounded by the specification, not by how the candidate was
                                                                          generated, so 𝛼 does not rise under optimization pressure and Λ
Algorithm 1: VerifyGate: amplify a candidate by all-accept                stays high.
gating
                                                                             Make model-based judges as robust as possible. When only a
                                                                          model can check (open-ended reasoning, style, subtle correctness),
    1: input: task 𝑥, budget 𝜅, mechanism set M
                                                                          several techniques raise and stabilize Λ: ask the judge to find a coun-
    2: 𝜎 ← single base solve; estimate log-odds ℓ
                                                                          terexample or a concrete flaw rather than to rate quality (refutation
    3: while cost(𝜎) < 𝜅 and not converged do
                                                                          is harder to game than approval); require the judge to show its
    4:          for 𝑚 ∈ M do     ⊲ vote+𝑛, add gate, refine, decompose    check (a verification chain-of-thought) and verify that; use a judge
    5:             𝑟ˆ𝑚 ← Δℓ
                         c (𝑚)/Δcost(𝑚) ⊲ est. marginal log-odds per
                                                                          that is independent of the generator (a different model, prompt,
         call                                                             or seed) to keep verifier and generator errors conditionally inde-
    6: end for                                                            pendent; and combine several judges so that a single exploitable
    7: 𝑚★ ← arg max𝑚 𝑟ˆ𝑚                                                  blind spot does not dominate. Each independent, informative judge
 8:    if 𝑟ˆ𝑚★ ≤ 𝜆 then break                               ⊲ saturated   contributes additively to the log-odds (the odds law), so a panel of
 9:    end if                                                             diverse weak judges can rival a single strong one, subject to the
10:    𝜎 ← apply(𝑚★, 𝜎); update ℓ                                         same correlation floor that limits voting.
11: end while
12: return aggregate(𝜎) or ⊥ if ℓ < 𝜏
                                                                             Measure Λ, do not assume it. The controller treats every verifier’s
                                                                          (𝛽, 𝛼) as quantities to be estimated, not declared. Wherever ground
     Algorithm 2: Controller: greedy marginal allocation                  truth eventually becomes available (a tool oracle, a downstream
                                                                          outcome, a held-out labeled stream, or human spot-checks), the
                                                                          harness updates running estimates 𝛽,   ˆ 𝛼ˆ and hence b
                                                                                                                                Λ. A verifier is
unit cost across stages; the controller approximates this by greedy       only credited with the amplification its measured discrimination
selection (Algorithm 2).                                                  supports; nominal accuracy on a benign distribution is never trusted
                                                                          on its own.
   Online estimation of verifier discrimination. The controller main-
tains running estimates of each verifier’s 𝛽 and 𝛼 from instances            Detect and resist drift. Under sustained optimization, a verifier’s
where ground truth is later revealed (tool oracles, held-out checks,      effective 𝛼 tends to rise as generators discover what it wrongly
or human spot-checks), yielding b         ˆ 𝛼ˆ and hence Δℓ
                                     Λ = 𝛽/              c = log b Λ      accepts: Goodhart’s law in action. The harness watches b  Λ over time
for the gate mechanism. Verifiers whose estimated Λ drifts toward         and, when it drifts toward 1, reduces that verifier’s weight, rotates
1 are demoted, an explicit guard against the gaming failure mode          in fresh or held-out checkers, and raises the abstention threshold for
(§15). Voting’s marginal gain is estimated from the current vote          affected instances. Disagreement among diverse verifiers is itself a
margin via a Chernoff exponent.                                           cheap early-warning signal: a sudden rise in unanimous acceptance
   Calibration. Raw model and judge scores are poorly calibrated,         with falling downstream correctness is the signature of a gamed
so the controller fits a monotone calibration map (e.g. isotonic/Platt)   gate.
from scores to empirical correctness, and uses calibrated log-odds
both as the gate score and as the abstention threshold (Chow’s               Tune the operating point. A verifier exposes a threshold trading
rule: commit only when the calibrated posterior clears a cost-based       completeness 𝛽 against false-acceptance 𝛼 (its ROC curve). For
threshold). Calibration quality is reported as expected calibration       amplification the harness prefers a high-𝛽/low-𝛼 operating point
error (ECE) in §13.                                                       even at the cost of more regenerations, because Λ, not through-
                                                                          put, governs the reachable reliability; for inexpensive screening it
                                                                          may accept lower 𝛽. The controller selects the operating point per
8        Engineering Robust Verifiers
                                                                          instance from the marginal-rate calculus.
Because verification is the high-leverage mechanism (§13) and be-
cause gameable verifiers are the dominant failure mode (§15), the
verifier ensemble deserves the most engineering attention. The            9   Decomposition and Planning in Practice
goal is high discrimination Λ = 𝛽/𝛼 that is robust: it must hold          Decomposition is the riskiest combinator: by the serial law it can
even when candidates are produced by a process optimizing for             only lose reliability unless each boundary is restored by verification.
acceptance.                                                               The planner is therefore conservative by design.
Maestro Order: A Model-Agnostic Orchestration Harness


   Decompose only when the split is clean and checkable. The planner        Table 2: A controller trace (simulation). Each gate multiplies
proposes a decomposition only when it is confident the subprob-             the odds by Λ=6 (+1.79 log-odds); reliability saturates while
lems are (i) genuinely independent or cleanly ordered, and (ii) each        cost grows linearly. The controller stops at the first row that
individually verifiable. A split into subproblems that cannot be            meets the target, or when the next gate’s marginal rate falls
checked inherits the worst of both worlds (more stages that can             below 𝜆.
fail, and no way to catch the failures), and the planner declines it
in favor of a monolithic solve plus verification. This is the opera-                 Step   Action           Δℓ      ℓ    𝑃 (corr)    calls
tional reading of the recursion master theorem: depth is affordable
                                                                                       0    base solve        —    0.20     0.550      1.0
precisely when every level is gated.                                                   1    + verify gate   1.79   1.99     0.880      3.8
   Typed plans and verified recombination. A plan is a typed DAG:                      2    + verify gate   1.79   3.78     0.978      7.4
                                                                                       3    + verify gate   1.79   5.58     0.996     11.7
each node declares its input and output types, its dependencies, and
                                                                                       4    + verify gate   1.79   7.37     0.999     17.3
the verifier to apply to its result and to the recombination. Type
compatibility is checked statically before any model call, catching                  stop: the next gate would offer Δℓ/Δcalls ≈ 0.25 < 𝜆
a class of decomposition errors for free. The recombination step is
itself a gated solver, so a correct assembly of correct parts is verified
rather than assumed.
                                                                            fix seeds per attempt so an experiment is bit-reproducible given
   Interleaving planning and acting. For tasks where the right de-
                                                                            the same backends.
composition is not knowable up front, the harness interleaves plan-
                                                                               Idempotency and caching. Solver and verifier calls are keyed by
ning with acting: solve a subproblem, observe the result and its
                                                                            (input, config) and cached, so retries and refinement loops do not
verdict on the blackboard, and let the planner revise the remain-
                                                                            double-bill and so ablations reuse work.
ing plan. This keeps decomposition adaptive while preserving the
                                                                               Concurrency. Independent candidates and verifiers run in parallel;
invariant that every committed intermediate has passed a gate, so
                                                                            the controller bounds fan-out by the remaining budget and merges
errors do not silently propagate down the tree.
                                                                            results on the blackboard.
   Budgeting across the tree. The controller allocates the global bud-         Failure handling. Tool/model errors are treated as rejections (fail
get across plan nodes by the same marginal-rate rule, spending              closed), never as silent acceptances; timeouts count toward cost
more verification on nodes whose errors are most likely to cor-             and trigger escalation or abstention rather than a guess.
rupt the final answer (those with high fan-out or on the critical              Cost accounting and observability. Every call’s token and latency
path) and less on cheap and easily checked leaves. The result is            cost is attributed to a stage, so the reliability–cost curves of §13 are
the verifier-saturated, marginal-rate-equalizing organization the           measured, not estimated, and per-stage marginal rates are visible
theory predicts, realized at the granularity of a plan.                     to the controller and to operators.
                                                                               Scheduling and backpressure. The controller issues independent
10     Anatomy of a Solve                                                   candidate and verifier calls concurrently up to a fan-out bounded
To make the controller concrete, Table 2 shows the controller’s             by the remaining budget and backend rate limits; results stream
expected progress with a weak base solver (𝑝 0 = 0.55) and a robust         onto the blackboard and the controller re-plans as each arrives.
verifier (Λ = 6, so each accepted gate adds log 6 = 1.79 to the log-        Under load it applies backpressure by lowering fan-out and raising
odds). The controller starts with one base solve, then repeatedly           the marginal-rate threshold 𝜆, gracefully degrading from a high-
adds the highest-rate mechanism (here, another verification gate),          reliability profile to a cheaper one rather than violating latency
updating the running log-odds and cost, until the calibrated log-           budgets.
odds clears the target threshold or the marginal rate drops below 𝜆.           Sandboxing and security. Tool verifiers (code execution, shell,
The reliabilities and call counts are the measured simulation values        search) run in an isolated sandbox with no access to secrets or the
of §13; the log-odds column is their logit.                                 host, because robust verification often means executing untrusted
   The trace exhibits the law operationally: the benefit per gate is        candidate code. Sandbox failures are rejections (invariant I2), and
constant in log-odds (+1.79) but the cost per gate grows (each gate         resource limits (CPU, memory, wall-clock) are enforced per call so
lowers acceptance probability, so more regenerations are needed),           a pathological candidate cannot exhaust the budget.
which is why the marginal rate falls and the controller eventually             Regression testing the harness itself. Because solves are replayable,
stops. A target of 0.97 is met at step 2 (7.4 calls) and 0.999 at step 4    a fixed suite of recorded instances doubles as a regression test: a
(17.3 calls). Voting alone from this near-threshold base would need         change to a prompt, verifier, or controller policy is evaluated by re-
several hundred calls for the same targets (Fig. 4b).                       running the suite and comparing reliability-at-cost and calibration,
                                                                            catching silent degradations before they reach production.
11     Implementation Concerns
Reliability claims are only as trustworthy as the plumbing beneath          12    Evaluation Methodology
them.                                                                       We evaluate the harness along four axes.
   Determinism and reproducibility. Each solve records model id,               Metrics. (i) Reliability at fixed cost: correctness rate on committed
decoding parameters, seed, prompt hash, and tool versions; runs             answers at a capped expected number of base calls. (ii) Coverage and
are replayable from the trace. Stochastic steps (sampling, voting)          the risk–coverage curve (and its area, AURC) for selective answering.
(iii) Calibration (ECE) of the harness confidence. (iv) Cost (expected
base calls) and latency.
    Ablations. We vary the vote count 𝑛, the number of gates 𝑘,
decomposition depth, verifier quality Λ, and solver diversity (corre-
lation 𝛾), isolating each combinator’s contribution.
    Statistical methodology. Each reported point is an average over
many i.i.d. trials with fixed seeds; we report it with a binomial con-
fidence interval and treat differences smaller than the interval as
noise. Because the harness is deterministic up to declared random-
ness (invariant I5), any reported number is reproducible from the
recorded seeds and backend versions, and ablations reuse cached
calls so that only the varied factor changes.
    Protocol for real models. The harness is designed to be evaluated
on standard suites (grade-school and competition math, code syn-          Figure 3: Controller trajectories (simulation): reliability ver-
thesis with execution-based verifiers, and open-domain QA with            sus cumulative base calls for three strategies on a weak base
retrieval corroboration) using standard metrics: pass@𝑘 accuracy,         (𝑝 0 =0.55). Verification and the hybrid strategy reach high re-
execution pass rate, and exact match, with the deterministic-replay       liability at an order of magnitude lower cost than voting;
machinery of §11.                                                         the controller follows whichever trajectory has the steepest
                                                                          current slope.
   Simulation study (this paper). To exercise the controller and vali-
date that the implementation obeys the predicted laws without con-
flating harness behavior with any particular model’s idiosyncrasies,      on a 𝑝 = 0.62 solver needs about 90 calls to pass 0.99, and a near-
we report a faithful Monte Carlo simulation of the harness over a         threshold solver barely improves at all. This is the practical form of
parameterized solver/verifier model: a generator emits a correct can-     the Θ(log 𝛿1 ) scaling, with very different constants.
didate with probability 𝑝; each verifier accepts a correct candidate
                                                                              The controller follows the steepest trajectory. Figure 3 plots re-
with probability 𝛽 and a wrong one with probability 𝛼 (Λ = 𝛽/𝛼);
                                                                          liability against cumulative cost for verify-only, vote-only, and a
correlated solver pools are produced by a Gaussian-copula latent
                                                                          hybrid that votes over three candidates before gating. Verify-only
factor with pairwise correlation 𝛾. We emphasize that the numbers
                                                                          reaches 0.999 at about 17 calls and the hybrid at about 23; vote-only
below are simulation outputs, not measurements of a deployed
                                                                          is still below 0.98 at 60 calls. The controller’s greedy policy (Algo-
model; they test the harness logic and the theory, and set expecta-
                                                                          rithm 2) is a walk up whichever trajectory is locally steepest, and
tions for the real-model protocol above. Each point uses between
                                                                          the figure shows why it would choose gates from the start here:
2 × 104 and 4 × 104 trials; repeated runs differ by Monte Carlo noise
                                                                          from 𝑝 0 = 0.55, the first gate offers about 0.64 log-odds per call,
of roughly ±0.004 in reliability and ±0.1 in expected calls, which
                                                                          while extra votes offer about 0.05 (a 3-vote lifts 0.55 only to 0.575).
explains small discrepancies between tables. Every number, figure,
                                                                          Voting becomes the better first move only when the vote margin is
and table in this paper can be regenerated exactly with the released
                                                                          large or the verifier is weak; the controller detects which regime it
code (§18).
                                                                          is in from the measured marginal rates instead of committing to a
                                                                          fixed pipeline.
13    Results
    Verification amplifies as the odds law predicts. Figure 4a over-         Diversity sets a hard ceiling on voting. Figure 4c shows major-
lays simulated gate reliability on the theoretical prediction 𝑟𝑘 =        ity reliability versus committee size for error correlations 𝛾 ∈
𝑜 0 Λ𝑘 /(1 + 𝑜 0 Λ𝑘 ) for a strong (Λ = 8) and a weak (Λ = 2) verifier,   {0, 0.05, 0.2} under the Gaussian-copula model. Independent solvers
starting from 𝑝 0 = 0.55. The simulation tracks theory to within          approach 1; at 𝛾 = 0.05 reliability plateaus near 0.85 and at 𝛾 = 0.2
Monte Carlo noise: three strong gates take the base from 0.55 to          near 0.71, no matter how many correlated members are added. The
0.998, and because 83 = 29 the weak verifier needs exactly three          plateaus match the shared-cause floor of the companion theory [1]:
times as many gates for the same odds gain. Across all gate counts        with 𝑝 = 0.6, the predicted asymptotic limits (the probability that
and both verifiers the simulated reliabilities agree with the closed-     the shared factor keeps the committee above chance) are 0.87 for
form odds law to within ±0.004 (the binomial standard error at            𝛾 = 0.05 (the 𝑛 = 255 committee is still approaching it) and 0.71 for
our trial counts), and the controller trace of Table 2 reproduces the     𝛾 = 0.2. Diversifying the solver pool (varied prompts, temperatures,
same values, evidence that the implementation faithfully realizes         models) is therefore a primary reliability decision, not a detail.
the algebra rather than merely being inspired by it. This agreement         Abstention buys reliability cheaply. Figure 4d is the risk–coverage
is the point of the simulation: it validates the harness logic and        curve from a calibrated harness score: committing only on the
isolates it from any particular model’s quirks before a real-model        most-confident 20% of instances drops the error rate from 0.45 (no
evaluation introduces them.                                               abstention) to under 0.1. Selective answering plus escalation is the
                                                                          cheapest reliability available when full coverage is not required.
   Verification dominates voting on the cost frontier. Figure 4b plots
reliability against expected base calls. A verifier with Λ = 6 reaches       The hybrid controller wins. Table 3 ablates the mechanisms from
0.98 within eight calls and 0.997 within twelve; majority voting          a weak base (𝑝 0 = 0.55, Λ = 6). Voting alone is nearly useless this
Maestro Order: A Model-Agnostic Orchestration Harness


                                                                             Table 4: Deployment profiles (simulation, 𝑝 0 =0.55, Λ=6).

                                                                                  Profile            Mechanisms              Reliability     Calls
                                                                                  Cheap              single solve                  0.55        1.0
                                                                                  Balanced           vote 5 + verify 𝑘=2           0.98       16.0
                                                                                  High-reliability   verify 𝑘=4 (+abstain)        0.999       17.3



   (a) amplification vs. theory                (b) cost–reliability        Table 5: Cost-to-target (simulation). Verification reaches each
                                                                           target with slowly growing incremental cost; the voting-only
                                                                           column is the approximate cost for a 𝑝=0.62 solver (normal
                                                                           approximation) and is roughly an order of magnitude larger.

                                                                                    Target reliability   Config   Verify calls   Voting calls
                                                                                    0.90                   𝑘=1            3.8               ∼27
                                                                                    0.97                   𝑘=2            7.4               ∼60
                                                                                    0.99                   𝑘=3           11.7               ∼90
                                                                                    0.999                  𝑘=4           17.3              ∼160
        (c) diversity floor                     (d) risk–coverage

Figure 4: Simulation results (Monte Carlo over the parameter-
ized solver/verifier model; not measurements of a deployed                 for the same target but does not change the geometric character of
model). (a) gate reliability matches the odds law; (b) verifica-           the amplification. The practical implication: because the required
tion reaches a target at far lower cost than voting; (c) error             depth is divided by log Λ, a modest improvement in the verifier
correlation caps voting gains; (d) abstention trades coverage              multiplies through the entire frontier, and often helps more than a
for reliability.                                                           large increase in vote count or a slightly better base model. This
                                                                           is the empirical form of the theory’s recommendation to invest in
                                                                           robust checkers.
Table 3: Ablation (simulation): reliability, coverage, and ex-
pected base calls for harness configurations on a weak base                   Calibration. The selective-answering results (Fig. 4d) depend on
(𝑝 0 =0.55, verifier Λ=6, 𝑇 =20). Hybrid configurations dominate           the harness confidence being calibrated: the abstention threshold is
at the high-reliability end.                                               only meaningful if a reported 0.9 confidence corresponds to a 0.9
                                                                           empirical correctness rate. After fitting the monotone calibration
           Configuration         Reliability   Coverage    Calls           map of §7, the harness confidence is well-calibrated by construction
           single shot                0.549        1.000     1.0
                                                                           in the simulation, so the risk–coverage curve is the true achievable
           vote n=5                   0.591        1.000     5.0           frontier; on real models, calibration error (ECE) would be reported
           verify k=2                 0.978        1.000     7.4           alongside it, and miscalibration would manifest as a gap between
           verify k=4                 0.999        0.999    17.4           the nominal threshold and the realized risk. Calibration is thus not
           vote5 + verify k=2         0.980        1.000    16.0           a cosmetic metric but the precondition that makes abstention and
           vote5 + verify k=4         0.999        1.000    28.8           gating trustworthy.

                                                                           13.2     Deployment profiles and cost-to-target
close to threshold (0.55 → 0.59); two gates reach 0.978 at 7.4 calls;
four gates reach 0.999. Combining a small vote with gating gives           Operators rarely tune individual mechanisms; they pick a profile
the best reliability-per-call at the high end. The controller’s job is     and a target. Table 4 distills the ablation into three profiles, and
to pick the point on this surface that meets the target at least cost:     Table 5 inverts the relationship: given a reliability target, the cheap-
here, “verify 𝑘=2” for a 0.97 target and “𝑘=4” for 0.999.                  est configuration the controller selects and its expected cost. The
                                                                           pattern is clear: each order-of-magnitude reduction in error costs
13.1     Sensitivity to verifier quality and base                          only a few more calls under verification, because cost grows with
         reliability                                                       log 𝛿1 while voting grows far faster.

The two parameters that matter most are the verifier discrimination            Summary. The harness reproduces every qualitative prediction
Λ and the base reliability 𝑝 0 , and their effects are exactly those the   of the theory and quantifies the trade-offs an operator faces: ver-
theory prescribes. The number of gates to reach a target scales as         ification is the high-leverage mechanism when a discriminating
1/log Λ, which is why the Λ = 8 curve in Figure 4a needs one third         checker exists, voting is a cheap supplement bounded by diversity,
of the gates of the Λ = 2 curve (log 8 = 3 log 2). A higher base 𝑝 0       and abstention converts confidence into reliability. The controller’s
shifts the whole cost–reliability frontier left by the additive term       marginal-rate policy reduces all of these choices to two settings: a
log 1−𝑝0 0 in the log-odds, so a stronger base solver needs fewer gates    target reliability and a budget.
     𝑝
14    Case Studies                                                          fixed pipeline is the special case the controller reduces to when
The same harness specializes to very different tasks by changing            every instance happens to have the same difficulty, which is rare in
only the solver pool and the verifier ensemble; the controller and          practice.
invariants are unchanged. We sketch three configurations to make
the mapping concrete.                                                       15    Discussion: Failure Modes and Guidance
                                                                                Verifier gaming (Goodhart). When solvers are optimized against
   Grade-school and competition mathematics. The base solver sam-           a fixed checker, the checker’s effective false-acceptance rises and its
ples chain-of-thought solutions at moderate temperature; diversity          discrimination collapses toward Λ = 1, and amplification silently
comes from multiple seeds and two prompt styles. The verifier en-           fails. (This is Goodhart’s law: a proxy measure stops tracking what
semble is deliberately robust: a deterministic arithmetic re-evaluator      it was meant to measure once it is optimized directly.) Mitigations:
recomputes the final expression, a units and sanity checker rejects         prefer robust verifiers whose soundness is independent of the gener-
out-of-range answers, and, for problems with a checkable form, sub-         ator (execution, proofs, types, corroborated retrieval); monitor each
stitutes the candidate back into the problem’s constraints. Because
                                                                                              Λ and demote drifters; rotate or ensemble diverse
                                                                            verifier’s online b
these checks reduce to executing the problem’s own definition, their
                                                                            verifiers; and hold out a ground-truth stream for recalibration.
false-acceptance is low and stable, so Λ is high and the controller
leans heavily on gating, falling back to self-consistency voting only          Correlated errors. A pool of near-identical solvers inherits shared
when no closed-form check applies. The expected behavior is the             blind spots; voting then plateaus far below 1 (Fig. 4c). Mitigation:
amplification curve of Figure 4a: a few gates take a near-threshold         engineer diversity (distinct prompts, temperatures, tools, and ideally
solver to high reliability at modest cost.                                  distinct models) and measure 𝛾 directly from disagreement rates.

    Program synthesis. Here verification is nearly ideal. The base              Decomposition error compounding. Aggressive decomposition
solver proposes a program; the verifier executes it in the sand-            multiplies per-stage error and can underperform a monolithic solve.
box against unit tests, a type-checker, and property-based fuzzing,         Mitigation: decompose only when a clean split is confident, and
with failures counting as rejections (invariant I2). Execution-based        gate every recombination boundary so each level is restored before
checking has very high discrimination: a program that passes a              it propagates; this is the recursion master theorem in practice [1].
strong test suite is very likely correct, and one that fails is certainly
                                                                               Cost and latency. Reliability is bought with calls; the controller’s
rejected. The controller’s dominant mechanism is therefore a single
                                                                            budget cap and abstention keep total cost bounded, and caching plus
high-Λ gate plus refinement: on rejection, the failing test output
                                                                            parallel fan-out keep latency manageable. The right operating point
is fed back as a critique and the solver revises. Decomposition ap-
                                                                            is application-specific and is exactly the marginal-rate threshold 𝜆.
pears naturally for multi-function tasks, with each function gated
by its own tests before integration; this is the recursion master              When not to use a harness. Orchestration is not free, and not
theorem realized as test-driven assembly. This is the regime where          every task warrants it. For tasks where the base solver is already
orchestration most clearly beats single-shot generation.                    reliable enough, where no informative verifier exists (Λ ≈ 1), or
                                                                            where latency dominates and a single fast answer is preferable to
   Open-domain question answering. Verification is hardest here
                                                                            a slow reliable one, the cheap profile (single solve) is correct and
because correctness is not mechanically checkable. The harness
                                                                            the overhead of voting and gating is waste. The controller makes
leans on grounding: a retrieval step supplies sources, the solver
                                                                            this an explicit decision: if the estimated marginal rate of every
must answer with citations, and the verifier checks that each claim
                                                                            mechanism is below 𝜆 from the start, it commits the single solve.
is supported by a retrieved passage (a corroboration check) and
                                                                            The harness adds value exactly in the regime the theory identifies:
cross-examines with an independent judge model prompted to find
                                                                            weak base solvers with discriminating, robust checkers.
unsupported assertions. No single check is decisive, so the controller
combines a modest verifier panel with self-consistency over diverse             Interaction with model improvements. A better base model raises
retrievals, and, crucially, sets a conservative abstention threshold,       𝑝 0 and shifts the whole cost–reliability curve left: the same target is
declining or escalating when corroboration is weak. The operating           reached with fewer gates and votes, and the controller spends less by
point sits on the risk–coverage frontier of Figure 4d: the system           default. Crucially, orchestration and model quality are complements,
answers confidently where sources agree and abstains where they             not substitutes: a stronger model with a robust verifier reaches
do not, which is the responsible behavior for factual tasks.                extreme reliability more cheaply than either alone. The harness
                                                                            therefore remains valuable as models improve, simply operating at
   Adaptive allocation versus fixed pipelines. A fixed pipeline, such       a cheaper point. The exception is verification quality: if generation
as “always sample five and verify twice,” spends the same budget on         improves faster than checking, the verifier becomes the limiting
every instance, over-paying on easy cases and under-serving hard            factor, which reinforces the paper’s central recommendation to
ones. The controller instead reads each instance’s running log-odds         invest there.
and stops early when the target is already met, redirecting budget
to the instances that need it. Because difficulty is heavy-tailed (most        Hallucinations and long-running jobs. Two deployment problems
instances are easy, a few are hard), this adaptivity is where much of       map directly onto the harness. The first is hallucination: a gener-
the practical cost saving comes from: the average cost is dominated         ative model’s confident production of incorrect or unsupported
by the easy majority, on which the controller commits quickly,              content [15]. This is exactly the failure that calibrated confidence
while the hard tail receives the deep verification it requires. The         targets: a hallucinated candidate either fails corroboration and test
Maestro Order: A Model-Agnostic Orchestration Harness


gates and is rejected, or fails to accumulate enough log-odds and be-    Table 6: Reproduction map: each published artifact, the sub-
comes an abstention or an escalation. Confident errors are thereby       command of reproduce.py that regenerates it, and the PCG64
converted into checked refusals. The second is the long-running,         seed.
multi-step job: because per-step error compounds, even a step that
is 99% reliable fails almost surely over hundreds of steps. Verifying          Artifact                                 Subcommand          Seed
every boundary bounds end-to-end error at logarithmic overhead
                                                                               Fig. 4(a–d), Table 3                     figures             20260607
(the recursion master theorem of the companion theory), and idem-              Table 2 (trace, stop rate)               trace               7
potent, replayable state lets such jobs checkpoint, suspend, and               Fig. 3 (trajectories)                    traj                11
resume, which is what long-horizon automation requires.                        Closed-form numbers in the text          predictions         —

   Safety. Fail-closed verification (treating errors and timeouts as
rejections), calibrated abstention, and full traceability make the
                                                                         the cost of voting alone, automatically selecting the cheapest mech-
harness conservative by construction: when it is unsure, it declines
                                                                         anism for the regime at hand. The practical message mirrors the
or escalates rather than emitting a confident guess. The full execu-
                                                                         theory: build robust checkers, diversify solvers, verify every bound-
tion trace also makes every answer auditable after the fact (which
                                                                         ary, and let the controller allocate at the margin. Reliability is not a
candidates were generated, which verifiers accepted, and why the
                                                                         property of a model; it is a property of how models are organized.
controller stopped), itself a requirement for high-stakes deploy-
ment.
                                                                         18     Artifact and Reproducibility Statement
                                                                         All experimental results in this paper are Monte Carlo simulations of
16     Limitations and Threats to Validity                               the parameterized solver/verifier model of §12; no proprietary mod-
The headline results are simulations of a parameterized model, not       els, datasets, or services are required to reproduce them. The full
measurements of a deployed system; they validate the harness logic       source code is publicly available at https://github.com/hidayetaksu/
and the reliability laws but do not, by themselves, establish absolute   maestro-order, together with pinned dependencies, reference out-
numbers on any benchmark. Real models violate the simulation’s           puts, and a README with step-by-step instructions.
clean assumptions: verifier errors are not perfectly conditionally
independent, solver correctness is instance-dependent rather than          One-command reproduction. With Python 3.10+ and the pinned
a single 𝑝, and 𝛽, 𝛼, 𝛾 vary across the input distribution. The com-     packages from requirements.txt (NumPy 2.2.6 is the version that
panion theory [1] bounds the cost of these violations (correlated        matters for bit-exact randomness),
verifiers lose effective Λ; correlated solvers can hit a floor when                              python reproduce.py all
shared causes push the committee below chance), and the harness          regenerates every artifact in two to four minutes on a single CPU
estimates the relevant quantities online, but a full real-model eval-    core, writing to ./output. Table 6 maps each artifact to its subcom-
uation under the §12 protocol is necessary to claim deployment           mand and seed. The four panels of Figure 4 and the ablation table
numbers and is the natural next step. Finally, our controller is         share one pseudo-random stream in a fixed order, so the figures
greedy; the constrained optimum it approximates can in principle         subcommand runs them together; the exact pattern of random
be solved more globally when marginal-rate estimates are reliable.       draws inside the simulation primitives is documented in the code
                                                                         and is part of the artifact.
17     Conclusion
                                                                            Verification. Reproduced outputs can be checked against the pub-
   Generalization. Although we describe the harness in terms of          lished artifacts by direct comparison: the regenerated ablation table
language models, nothing in the architecture or the controller de-       in output/ is byte-identical to the published copy in figures/, and
pends on that choice. A base solver is any process behind the solve      JSON summaries of every data series (including the measured max-
interface (a model, a heuristic, a search procedure, a tool, a human,    imum deviation between simulation and the closed-form odds law,
or another harness), and a verifier is anything that returns a cali-     0.0019 ≤ 0.004) are provided as reference outputs. Derived quanti-
brated accept/reject. The same controller would organize a pool of       ties quoted in the text (the voting cost-to-target estimates of Table 5,
human reviewers with an automated checker, or a mix of models            the diversity plateaus of §13, and the marginal rates in the trajec-
and classical algorithms, identically. This is the practical payoff of   tory analysis) are computed in closed form by the predictions
grounding the system in an algebra over abstract solvers: the har-       subcommand, with no random input. The paper itself builds from
ness is a general-purpose organizer of unreliable problem-solving,       the repository root with pdflatex and the ACM acmart class; fig-
of which the language-model case is one instance.                        ure and table sources are read from the figures/ directory that
   We presented a model-agnostic harness that organizes unreli-          the reproduction script can regenerate.
able solvers into reliable problem-solving systems by compiling
four structural combinators into runtime components and a budget-        References
aware controller that spends compute where it buys the most relia-        [1] Hidayet Aksu. 2026. Odds Law: The Decomposition Algebra—On How Intel-
bility. A faithful simulation reproduces the predicted laws: geomet-          ligence Organizes Itself to Solve Difficult Problems Reliably. arXiv:2606.15712.
ric amplification by verification, threshold-and-floor behavior of            https://arxiv.org/abs/2606.15712
                                                                          [2] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia,
voting, and the value of abstention. It also shows that a controller-         Ed Chi, Quoc Le, and Denny Zhou. 2022. Chain-of-Thought Prompting Elicits
driven organization reaches reliability targets at a small fraction of        Reasoning in Large Language Models. In Proc. NeurIPS.
[3] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang,           [10] Hunter Lightman, Vineet Kosaraju, Yura Burda, et al. 2023. Let’s Verify Step by
    Aakanksha Chowdhery, and Denny Zhou. 2023. Self-Consistency Improves Chain              Step. arXiv:2305.20050.
    of Thought Reasoning in Language Models. In Proc. ICLR.                            [11] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, et al. 2023. Judging LLM-as-a-Judge
[4] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao,        with MT-Bench and Chatbot Arena. In Proc. NeurIPS Datasets and Benchmarks.
    and Karthik Narasimhan. 2023. Tree of Thoughts: Deliberate Problem Solving         [12] Patrick Lewis, Ethan Perez, Aleksandra Piktus, et al. 2020. Retrieval-Augmented
    with Large Language Models. In Proc. NeurIPS.                                           Generation for Knowledge-Intensive NLP Tasks. In Proc. NeurIPS.
[5] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,      [13] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, et al. 2023. Toolformer: Language
    and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language                 Models Can Teach Themselves to Use Tools. In Proc. NeurIPS.
    Models. In Proc. ICLR.                                                             [14] Mark Chen, Jerry Tworek, Heewoo Jun, et al. 2021. Evaluating Large Language
[6] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik                   Models Trained on Code. arXiv:2107.03374.
    Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal           [15] Ziwei Ji, Nayeon Lee, Rita Frieske, et al. 2023. Survey of Hallucination in Natural
    Reinforcement Learning. In Proc. NeurIPS.                                               Language Generation. ACM Computing Surveys 55, 12, Article 248.
[7] Aman Madaan, Niket Tandon, Prakhar Gupta, et al. 2023. Self-Refine: Iterative      [16] John von Neumann. 1956. Probabilistic Logics and the Synthesis of Reliable
    Refinement with Self-Feedback. In Proc. NeurIPS.                                        Organisms from Unreliable Components. In Automata Studies. Princeton Univ.
[8] Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mor-               Press, 43–98.
    datch. 2023. Improving Factuality and Reasoning in Language Models through         [17] Marquis de Condorcet. 1785. Essai sur l’application de l’analyse à la probabilité
    Multiagent Debate. arXiv:2305.14325.                                                    des décisions. Paris.
[9] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, et al. 2021. Training Verifiers    [18] Jeffrey Dean and Sanjay Ghemawat. 2004. MapReduce: Simplified Data Process-
    to Solve Math Word Problems. arXiv:2110.14168.                                          ing on Large Clusters. In Proc. OSDI. USENIX, 137–150.
