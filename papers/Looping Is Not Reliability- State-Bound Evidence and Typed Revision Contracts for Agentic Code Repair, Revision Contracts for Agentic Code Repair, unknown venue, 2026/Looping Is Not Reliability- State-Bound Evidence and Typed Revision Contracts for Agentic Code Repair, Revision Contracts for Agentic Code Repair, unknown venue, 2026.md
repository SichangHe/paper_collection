                                               Looping Is Not Reliability: State-Bound Evidence and Typed
                                                      Revision Contracts for Agentic Code Repair
                                                           Xueping Gao✉                                               Jianwei Yang                                    Qiang Yang
                                                  xueping.gxp@alibaba-inc.com                               jianwei.yjw@alibaba-inc.com                       yuanzhan.yq@taobao.com
                                                    Alibaba Cloud Computing                                   Alibaba Cloud Computing                         Alibaba Cloud Computing
                                                        Hangzhou, China                                           Hangzhou, China                                 Hangzhou, China

                                         Abstract                                                                                    CODE TRAJECTORY                   NO STATE CHECK
                                                                                                                                              repair + verify               revise
                                         Generate–test–revise loops are common in coding agents, but rep-
                                                                                                                                        A WRONG                B VERIFIED             C REGRESSED
                                         etition alone provides no reliability guarantee. We study the gap
arXiv:2607.24604v2 [cs.CL] 14 Sep 2026




                                         between finding a correct patch and retaining, verifying, and sub-                           shift = 12              shift = 4               shift = 12
                                         mitting it. A sealed five-seed study over 30 HumanEval repairs
                                         produces 900 three-revision trajectories. Under forced revision,                            EVIDENCE       observe
                                         current correctness with current traces falls from 0.820 after one                                                   stale trace reused
                                         revision to 0.673 after two, although ever-correct rises to 0.847. Two                      TRACE FROM STATE A
                                         common-state studies use 2,430 branches from identical frozen pro-                          failure: shift = 12      trace A ≠ code B
                                         grams to remove post-treatment risk-set bias. In a prespecified 14B
                                                                                                                                                                       STATE-BOUND CHECK
                                         replication, stale traces harm 34/135 correct starts versus 4/135 with                                                   reject mismatch; preserve B
                                         current traces, a 22.2-point increase (task-cluster 95% CI [8.9, 37.0],
                                         exact Holm 𝑝 = 0.0337). A prospective 540-rollout policy eliminates
                                         observed correct-start harm but reduces wrong-start repair and                          Figure 1: Mechanism of stale-evidence resurrection. Repair
                                         fails its joint criterion. Repository experiments over 24 bugs and                      changes code state A (shift 12) to verified state B (shift 4),
                                         four coder stacks expose floor effects and component heterogeneity                      but an old trace bound to A is reused for the next revision
                                         without Holm-significant effects. We therefore separate admission,                      and restores shift 12. State binding rejects the A/B mismatch
                                         preservation, grounded certification, competence, and liveness. We                      before revision. Section 5.3 reports HumanEval/89.
                                         derive an evidence-bound typed loop contract and instantiate its
                                         mechanically enforceable subset in a reference implementation
                                         that binds verifier evidence to exact code states, preserves verified                   1     Introduction
                                         checkpoints, and emits auditable admission receipts. The imple-                         Coding agents increasingly operate as loops: propose code, execute
                                         mentation is an executable specification and conformance artifact,                      tests, consume feedback, revise, and stop. Iterative refinement can
                                         not evidence of improved repair competence or calibrated verifier                       improve the probability that a correct solution is produced [5, 15,
                                         dependence.                                                                             22]. This search-centric view, however, obscures a deployment
                                                                                                                                 question: after a correct patch appears, what prevents the next
                                         CCS Concepts                                                                            revision from destroying it, a stale observation from reviving an
                                         • Software and its engineering → Software testing and debug-                            old bug, or a correlated verifier from confirming the same error?
                                         ging; • Computing methodologies → Artificial intelligence.                                 We call this distinction proposal search versus completion relia-
                                                                                                                                 bility. Search asks whether any revision in a trajectory is correct.
                                         Keywords                                                                                Completion reliability asks whether the orchestrator retains a cor-
                                                                                                                                 rect state, bases revisions on evidence about that state, and stops
                                         coding agents, agent reliability, code repair, verification, stopping                   only when its accepted evidence has sufficiently low risk. The dis-
                                         policies, LLM evaluation                                                                tinction matters because an increasing ever-correct rate can coexist
                                         ACM Reference Format:                                                                   with a decreasing current or final correctness rate.
                                         Xueping Gao, Jianwei Yang, and Qiang Yang. 2026. Looping Is Not Reliability:               Prior work establishes important pieces of this problem. Intrinsic
                                         State-Bound Evidence and Typed Revision Contracts for Agentic Code                      self-correction may fail or regress without reliable external feed-
                                         Repair. In Proceedings of the 1st International Workshop on Agentic AI for              back [9, 11]; error localization and revision ability are distinct [25];
                                         Next-Generation Software Development (AgenticDev ’26), October 12–16, 2026,             and weak verifiers limit self-correction [28]. FeedbackEval mea-
                                         Munich, Germany. ACM, New York, NY, USA, 11 pages. https://doi.org/10.                  sures how feedback types affect code repair [5]. Work on evaluator
                                         1145/3843282.3844438
                                                                                                                                 self-preference and correlated model errors cautions that a second
                                                                                                                                 model is not automatically an independent judge [12, 18]. These
                                                                                                                                 findings do not yet provide a joint account of state transitions, evi-
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   dence provenance, verifier selective risk, verifier dependence, and
                                         AgenticDev ’26, Munich, Germany                                                         stopping in one code-agent protocol.
                                         © 2026 Copyright held by the owner/author(s).                                              This paper asks five research questions:
                                         ACM ISBN 979-8-4007-2985-0/2026/10
                                         https://doi.org/10.1145/3843282.3844438                                                 RQ1 Is correctness an absorbing state under repeated revision?
AgenticDev ’26, October 12–16, 2026, Munich, Germany                                                                                Gao, Yang, Yang


RQ2 From the same wrong or correct program, how do evidence                 evidence, and gate completion: first under controlled function-level
       content and state alignment change repair and continuation           states, then as a bundle in repository Git/search/edit/test loops.
       harm?                                                                   Recent process studies characterize feedback integration [1]; the
RQ3 Can verifier quality or independence be inferred from model-            “lucky pass” AgentLens identifies regression cycles [21], while a
       family diversity?                                                    production-assessed AgentLens studies verification and recovery
RQ4 Which orchestration guards directly block the observed fail-            over whole trajectories [19]. Others control hint depth while mea-
       ure classes, and what do they cost?                                  suring preservation [13], or expose action bias and visible–held-out
RQ5 How do contracts and revision allowance affect repository               gaps [7, 29]. Evidence guards, abstention, and transactional admis-
       completion?                                                          sion are established ideas [2, 3, 16]. Our narrower contribution is
   Our contributions are:                                                   a fixed-code-state intervention on evidence provenance, linked to
(1) A trajectory-level reliability decomposition that jointly               verifier risk and dependence and followed by a prospective policy
    reports correctness discovery and retention, wrong-to-correct           test.
    and correct-to-wrong transitions, verifier risk–coverage, condi-           Adjacent infrastructure enforces related but different bound-
    tional false-accept dependence, and sound completion.                   aries. In-toto records and verifies software-supply-chain steps [24],
(2) Controlled evidence studies. Forced revision shows correct-             SLSA provenance describes where, when, and how an artifact was
    ness loss; paired common-state interventions at two coder ca-           produced [23], and OPA separates general policy decisions from
    pacities estimate state-alignment contrasts from identical se-          their enforcement [17]. Our reference implementation adopts prove-
    lected states.                                                          nance and admission ideas but applies them inside an agent-repair
(3) An executable contract and reference implementation.                    transaction: verifier evidence is bound to the candidate code state
    We derive testable obligations for state-bound evidence, typed          on which it was produced, and admission preserves or recertifies
    actions, checkpoint preservation, fresh completion certification,       that state. It neither provides supply-chain attestation nor repairs
    and risk-aware stopping. A reference implementation instanti-           an inadequate oracle.
    ates the mechanically enforceable subset as an admission layer
    around existing coding agents and verifiers.
(4) Repository-agent factorials. Over 24 bugs, four coder stacks            2.3    Code Correctness and Executable Evidence
    test a contract; two Devstral factorials separate components and        HumanEval introduced execution-based functional correctness for
    depth. All use sealed adjudication and task-cluster inference.          generated programs [4]. EvalPlus expands its tests and demon-
                                                                            strates that a small visible suite can overestimate correctness [14].
2 Related Work                                                              We use disjoint visible, challenge, and hidden input sets derived
2.1 Self-Correction and Feedback-Driven Repair                              from HumanEval+, while explicitly treating challenge and hidden
                                                                            tests as construction-dependent rather than independent oracles.
Huang et al. find that intrinsic self-correction does not reliably
improve reasoning when no external signal is available [9]. Kamoi et
al.’s survey similarly identifies reliable external feedback as a central
success condition [11]. Tyen et al. show that models often fail to          2.4    Verifier Risk and Dependence
locate errors even when they can correct an error whose location            LLM evaluators may recognize and favor their own generations [18].
is supplied [25]; Zhang et al. separate refinement ability from the         More broadly, errors remain correlated across model architectures
strength of the verifier that decides when to refine [28]. In code,         and providers [12]. We therefore distinguish two quantities: selec-
FeedbackEval evaluates feedback types and reports diminishing               tive risk at a specified coverage and conditional error dependence
gains over repeated repair [5]. We do not claim the new observation         among incorrect candidates. Risk–coverage follows selective pre-
that feedback quality matters. We instead measure the bidirectional         diction, where abstention is part of evaluation rather than silently
transition process and intervene on whether evidence is attached            discarded [6]. Our contribution is to connect these quantities to
to the program state it describes.                                          agent completion decisions and to show that dependence changes
    Self-Refine and Reflexion exemplify inference-time refinement           with the acceptance operating point.
with generated feedback or memory [15, 22]. Their motivating met-
ric is typically task success. Our focus is the reliability contract
required after a proposal exists: preservation, provenance, verifica-       3     Reliability Decomposition
tion, and stopping.                                                         Consider the observed transition sketched in Figure 1. After the shift
                                                                            is repaired, the current program is correct, so 𝑌𝑡 = 1. A failure trace
2.2     Agentic Software Engineering Systems                                produced from the earlier wrong program is then supplied as if it
Repository-scale systems make orchestration concrete. SWE-agent             described the current state; the next revision restores the old defect,
shows that the agent–computer interface changes coding perfor-              yielding 𝑌𝑡 +1 = 0. This is a correct-to-wrong transition. Conversely,
mance [27]; Agentless reports that a simpler localization–repair–           changing a wrong program into a correct one is a wrong-to-correct
validation pipeline can outperform more elaborate open-source               transition. The following decomposition measures both rather than
agents on SWE-bench Lite [26]; and SWE-bench exposes long-                  treating correctness as an absorbing endpoint.
context, multi-file demands [10]. Beyond their end-task metrics,                Let 𝑌𝑡 ∈ {0, 1} denote the executable correctness of the code
we test whether loops preserve valid states, consume state-aligned          after revision 𝑡, and let 𝑒𝑡 denote the evidence supplied for the next
Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair             AgenticDev ’26, October 12–16, 2026, Munich, Germany


revision. For a fixed evidence condition 𝑒, define                                       4 Study Design
                       𝛼𝑒 = 𝑃 (𝑌𝑡 +1 = 1 | 𝑌𝑡 = 0, 𝑒),                        (1)        4.1 Tasks and Executable Adjudication
                       𝛽𝑒 = 𝑃 (𝑌𝑡 +1 = 0 | 𝑌𝑡 = 1, 𝑒).                        (2)        We select 30 Python function-repair tasks from the HumanEval por-
                                                                                         tion of FeedbackEval [5]. Initial wrong candidates are stratified by
If 𝑞𝑡 = 𝑃 (𝑌𝑡 = 1), then
                                                                                         source (existing benchmark candidate, LLM-generated candidate,
                      𝑞𝑡 +1 − 𝑞𝑡 = (1 − 𝑞𝑡 )𝛼𝑒 − 𝑞𝑡 𝛽𝑒 .                      (3)        and rule-based mutation) and frozen by hash before the confir-
                                                                                         matory runs. We do not redistribute the source benchmark data;
Repair ability alone is therefore insufficient: when the current state
                                                                                         the artifact records task identifiers, candidate indices, sources, and
is likely correct, a nonzero regression rate can make another re-
                                                                                         hashes.
vision harmful in expectation. If 𝛼𝑒 + 𝛽𝑒 > 0, continuation has
                                                                                            Correctness requires passing visible, challenge, and hidden tests.
negative expected correctness change when 𝑞𝑡 > 𝛼𝑒 /(𝛼𝑒 + 𝛽𝑒 ).
                                                                                         Challenge and hidden inputs are disjoint partitions of HumanEval+
    This transition view makes the paper’s three factors precise
                                                                                         [14]; they share the same benchmark construction process. Genera-
without pretending that all are separately identifiable. Let 𝑒 0 be
                                                                                         tion sees only visible evidence. Challenge and hidden suites remain
a matched nonactionable control. We operationalize the effective
                                                                                         sealed until all trajectory and branch matrices pass structural vali-
evidence response on wrong and correct states as
                                                                                         dation. Evaluation is cached by (suite, task, code SHA-256).
            𝑅𝑊 (𝑒) = 𝛼𝑒 − 𝛼𝑒0 ,                𝑅𝐶 (𝑒) = 𝛽𝑒0 − 𝛽𝑒 .            (4)
These contrasts combine two latent quantities: how much task-
relevant information the evidence carries and how responsively the
                                                                                         4.2     Trajectory Study
coder maps that information into an edit. A single-coder evidence                        The coder is Qwen2.5-7B-Instruct [20], sampled with temperature
intervention identifies their joint effective action, not “informative-                  0.3 and top-𝑝 0.9. Each trajectory performs three forced revisions.
ness” and “responsiveness” separately. Zero response can mean un-                        We cross 30 tasks, six evidence conditions, and five seeds, yielding
informative evidence or an unresponsive reviser; negative response                       900 trajectories and 2,700 revisions. The evidence conditions are
can mean misleading or state-misaligned evidence, overreaction, or                       current binary outcome, current execution trace, stale binary out-
both. This identification limit is important: the three-factor thesis                    come, stale trace, unavailable evidence, and a flipped-binary stress
is an interface decomposition, not a fitted multiplicative law.                          condition. Forced revision intentionally estimates what happens
   Evidence also has provenance. Write 𝑒 = (ℎ𝑠 , ℎ𝑞 , 𝑥) for source-                     when an orchestrator continues; it is not presented as the behavior
state hash, test-suite hash, and payload. The evidence is state-                         of every adaptive agent.
aligned only if ℎ𝑠 = ℎ(𝑆𝑡 ). Payload 𝑥 may contain true input/output                        Every revision is judged by native self-declaration, fresh-context
facts while the envelope is invalid for the current state. The                           Qwen2.5-7B, same-family Qwen2.5-14B, cross-family DeepSeek-
common-state study varies this alignment while holding the start-                        Coder-6.7B [8], and an executable challenge verifier. This produces
ing code fixed.                                                                          13,500 verdicts. Replaying four stopping rules for each verifier pro-
   For verifier 𝑣 with threshold chosen to attain coverage 𝑐, we                         duces 18,000 paired outcomes: verifier-only, visible gate, challenge
report                                                                                   gate, and a strict gate requiring challenge acceptance plus evidence
                                                                                         sourced from the immediately preceding state.
                      Cov𝑣 (𝑐) = 𝑃 (𝐴𝑣 = 1),                                  (5)           The three model verifiers use an order-swapped, single-token
                      Risk𝑣 (𝑐) = 𝑃 (𝑌 = 0 | 𝐴𝑣 = 1),                         (6)        A/B forced choice; the acceptance score is the mean ACCEPT prob-
where 𝐴𝑣 denotes acceptance. To avoid conflating shared prevalence                       ability under both label orders. Native thresholds are fixed at 0.5.
with shared errors, dependence is computed only among incorrect                          Retrospective coverage matching ranks scores on the frozen revi-
candidates. For verifiers 𝑖, 𝑗 we report excess joint false acceptance,                  sion distribution and accepts the top fraction; it compares verifiers
                                                                                         but does not estimate deployment calibration. A stopping replay se-
      𝐷𝑖 𝑗 (𝑐) = 𝑃 (𝐴𝑖 𝐴 𝑗 | 𝑌 = 0) − 𝑃 (𝐴𝑖 | 𝑌 = 0)𝑃 (𝐴 𝑗 | 𝑌 = 0),          (7)        lects the first revision satisfying its gate; if none does, it rejects after
and the corresponding 𝜙 coefficient. Both are operating-point con-                       revision 3. Because generation is frozen before replay, every policy
ditional: changing coverage changes which errors are accepted.                           sees the same candidates and executable outcomes. “Mean rounds”
   For an ensemble that accepts only when both verifiers accept,                         includes rejected trajectories, which consume the full three-revision
let 𝑓𝑖 = 𝑃 (𝐴𝑖 = 1 | 𝑌 = 0). Its conditional false-accept rate is                        budget.

                    𝑃 (𝐴𝑖 𝐴 𝑗 = 1 | 𝑌 = 0) = 𝑓𝑖 𝑓 𝑗 + 𝐷𝑖 𝑗 .                  (8)
Thus the familiar product-of-errors argument is valid only when                          4.3     Common-State Intervention
𝐷𝑖 𝑗 = 0. Positive dependence is an additive reliability penalty even                    Transition rates in a free-running trajectory have a post-treatment
if both marginal verifiers are individually strong; low dependence                       risk-set problem: evidence affects whether a revision reaches a cor-
is not useful when either marginal risk is poor.                                         rect state, so comparing later regressions conditions on an evidence-
    Finally, sound completion is 𝑃 (𝐴 = 1, 𝑌 = 1) over all trajectories.                 dependent event. We address this with common-state intervention.
Unlike risk alone, it exposes a policy that obtains zero observed er-                    For each task we freeze one wrong and one correct code state, se-
ror by rejecting nearly everything. We report coverage, risk, sound                      lected before assigning the new evidence branches. Twenty-seven
completion, and mean selected revision together rather than choos-                       of 30 tasks contain both states and enter this study; the estimand
ing a universal scalar utility.                                                          therefore concerns tasks with an observed repairable state.
AgenticDev ’26, October 12–16, 2026, Munich, Germany                                                                                       Gao, Yang, Yang


Table 1: Evidence interventions. Current evidence is generated from the code being revised; stale evidence is generated from a
different revision or the frozen wrong state.

                   Condition             Payload                                  Source state         Role
                   Current binary        Visible PASS/FAIL                        Current code         Minimal aligned signal
                   Current trace         Outcome, pass count, up to 3 failures    Current code         Actionable aligned signal
                   Stale binary/trace    Same formats                             Previous revision    Free-running freshness stress
                   Unavailable           UNAVAILABLE                              None                 No-evidence baseline
                   Flipped binary        Negated visible PASS/FAIL                Current code         Misleading-signal stress
                   Matched control       Neutral text, character-length matched   None                 Report-length/attention control
                   Stale wrong trace     Failure trace                            Frozen wrong code    State-misalignment intervention


             Table 2: Confirmatory study inventory.                               analysis subtracts 7B task-level effects from 14B effects and applies
                                                                                  a separate six-test Holm family; it was specified before inspecting
    Component                  Trajectory study    Common-state study             14B outcomes but is not a randomized model-family comparison.
                                                                                  Trajectory confidence intervals also resample complete task clus-
    Tasks                                    30                         27
    Seeds                                     5                          5        ters, preserving all seeds, conditions, revisions, and policies. Invalid
    Coder capacities                          1                          2        generations remain in the intention-to-treat denominator. All pro-
    Evidence conditions                       6        4 wrong / 5 correct        tocol, data-partition, trajectory, verdict, and analysis artifacts carry
    Revisions per branch                      3                          1        SHA-256 lineage hashes.
    Trajectories/branches                   900                      2,430           Generation processes can read only the visible bundle. Challenge
    Candidate revisions                   2,700                      2,430        and hidden bundles are opened only after trajectory IDs, condition
    Verifier verdicts                    13,500                         —         matrices, hashes, parser outputs, and lineage fingerprints validate
    Policy outcomes                      18,000                         —         exactly. Hidden adjudication then recomputes the complete verifier
                                                                                  and policy matrices. This ordering prevents a partial run or adaptive
                                                                                  policy choice from leaking hidden outcomes back into generation.
   From every frozen wrong state we branch current binary, cur-
rent trace, unavailable, and length-matched nonactionable evidence.               4.5    Prospective Paired Online
From every correct state we branch the same conditions plus a
                                                                                         Commit-Admission Comparison
stale trace generated from the paired wrong state. The prompt
permits returning unchanged code. Crossing 27 tasks, nine state–                  Replay can show whether a guard would intercept recorded outputs,
evidence branches, and five common-random-number seeds gives                      but not how enforcing it changes subsequent model behavior. We
1,215 single-step branches for Qwen2.5-7B. Before inspecting repli-               therefore run a sealed paired online comparison on the 27 common-
cation outcomes, we freeze an exact Qwen2.5-14B repeat with the                   state tasks: two start states, five seeds, and baseline/guarded arms
same states, evidence, prompts, sampling parameters, seeds, and ad-               yield 540 rollouts. Both arms use Qwen2.5-7B, the same typed action
judication, adding 1,215 branches. The two capacities are analyzed                prompt, visible diagnostics, challenge executions, seed schedule,
separately rather than pooled.                                                    and three-step budget. Baseline commits every parseable patch
   The frozen wrong state is the original visible-failing candidate.              and ignores challenge verdicts for admission. Guarded execution
The frozen correct state is selected mechanically as the lexico-                  binds evidence to the current state, admits a patch only after the
graphically first v0.4.3 revision passing all three suites; no failure            challenge gate, and retains a last-known-good checkpoint after
case is hand-picked. The matched control contains no task, test,                  invalid or rejected proposals. Hidden outcomes are opened only
PASS/FAIL, or numerical semantics and exactly matches the tar-                    after the complete paired matrix validates. The preregistered end-
get report in Unicode character count. It does not exactly match                  points are unsafe-completion superiority and sound-completion
tokenizer length, so prompt-token distributions remain an audited                 non-inferiority at a −5-point margin; inference uses paired task-
nuisance variable. Within each task–state–seed block, evidence                    cluster bootstrap intervals.
branches share the sampling seed; invalid or unchanged outputs
remain in the intention-to-treat denominator.                                     4.6    Repository-Agent Factorial
                                                                                  To test the contract beyond single-function repair, we freeze 24 his-
4.4     Inference and Audit                                                       torical bugs from nine Python projects, with at most three tasks per
The task, not the revision, is the independent sampling unit. Con-                project. Eligibility requires direct-parent bug/fix endpoints, stable
firmatory common-state contrasts average seeds within each task                   three-repeat signatures across the frozen suites, no ignored oracle,
and then weight tasks equally. Within each coder, we use 10,000                   and a gold production patch of at most five files and 200 changed
task-cluster bootstrap draws, 100,000 paired sign flips, and one                  lines. The primary-only manifest excludes pilot tasks, is frozen
Holm correction over six preregistered contrasts. Because five-seed               before model output, and permits no outcome-driven replacement.
task effects lie on a discrete grid, an exact dynamic-programming                 Each task has a sanitized agent mirror containing only the buggy
sign-flip sensitivity removes Monte Carlo error. A secondary paired               tree and a separate evaluator mirror containing sealed tests but
Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair           AgenticDev ’26, October 12–16, 2026, Munich, Germany


no gold source object. A hash-locked local Qwen2.5-14B snapshot                          contract obligations and was not used to generate the reported
operates through typed search, view, edit, shell, test, submit, and                      empirical results.
escalate actions in a real Git worktree, sampled at temperature 0.3,
top-𝑝 0.9, and at most 1,024 new tokens per action. We cross current
versus one-step-stale diagnostic evidence with contract OFF versus
ON and repeat every cell over three preregistered seeds, yielding                        5 Results
24×2×2×3 = 288 intention-to-treat rollouts. Each rollout is limited                      5.1 RQ1: Correctness Is Non-Absorbing
to 15 actions, three source revisions, six visible tests, and a shared
wall-clock budget.                                                                       Figure 2b separates current correctness from cumulative discovery.
   Contract ON bundles evidence–state binding, a private com-                            With current traces, 82.0% of trajectories are correct after revision
mit gate, rejection with rollback, last-known-good checkpoints,                          1. Current correctness then falls to 67.3% at revision 2 and recovers
and completion certification. Contract OFF executes and records                          only to 69.3% at revision 3. In contrast, ever-correct increases from
the same private gate but does not use its verdict to block a re-                        82.0% to 84.7% and 85.3%. At revision 3, 16.0% of trajectories have
vision. Diagnostic, gate, fail-to-pass, pass-to-pass, and full-suite                     produced a correct patch and subsequently lost it. Current binary
assets are content-hashed; generation can access only the diagnos-                       evidence has lower loss (8.0%) but still does not make correctness
tic interface. Every proposed patch, including rejected proposals, is                    absorbing.
preserved and later replayed in an evaluator-owned worktree. Be-                            The shape is evidence-specific rather than a generic depth
fore unsealing, a 24-task by four-suite baseline audit found residue                     penalty. Current-binary correctness is 0.700, 0.700, 0.720 across
only from terminal full-suite runs; the frozen evaluator orders fail-                    revisions; stale-trace correctness is 0.687, 0.713, 0.660; and unavail-
to-pass, pass-to-pass, then full, and hard-resets and cleans before                      able evidence is 0.687, 0.687, 0.707. Consequently, neither “more
each candidate. Final resolution requires all three suites to pass.                      rounds help” nor “more rounds hurt” is supported as a context-free
An orchestrator-accepted completion is either an explicit agent sub-                     rule. Loop depth changes the number of transition opportunities;
mission or, in the ON arm, a checkpoint accepted by the frozen                           the transition kernel determines their sign.
completion rule. Unsafe and sound completion are accepted-and-                              This result is deliberately scoped: it establishes non-absorption
incorrect and accepted-and-correct, respectively.                                        under the tested forced-revision protocol. It does not show that an
   The task is the inferential unit: seeds are averaged within task                      adaptive loop must regress. It shows why an adaptive loop needs a
and all 24 tasks receive equal weight. The co-primary intersection–                      preservation and stopping rule.
union decision requires the one-sided 95% upper bound on the
Contract ON-minus-OFF unsafe-completion effect to be below zero
and the lower bound on sound completion to exceed the prereg-
istered absolute −5-point margin. This margin was frozen before
                                                                                         5.2     RQ2: Evidence Helps Repair but Can Harm
outcomes; when baseline sound completion later falls below 5%, its                               Retention
non-inferiority decision is necessarily weak evidence about live-                        Table 3 and Figure 3 consolidate the assignment outcomes. For
ness. We use 200,000 task-cluster bootstrap draws; task sign flips,                      7B, current traces produce the most repairs from wrong starts
project-equal estimates, and leave-one-project-out checks are sen-                       (113/135), while stale traces produce the most harms from correct
sitivities.                                                                              starts (12/135). Trace minus control repair is +5.9 points with task-
   To probe stack generality under the 14B completion floor, we                          cluster 95% CI [−2.2, 17.0]; all six 7B contrasts have Holm-adjusted
froze three separate 288-rollout replications before their outcomes:                     𝑝 = 1.0.
Qwen2.5-Coder-32B-Instruct-AWQ, Qwen3-Coder-Next-FP8, and                                   The 14B replication changes the ordering: unavailable evidence
Devstral Small 2 24B. Each preserves the task matrix, co-primary es-                     produces the most repairs (126/135), so additional task feedback
timands, budgets, completion rule, and task-equal inference, and is                      is not monotonically useful. From correct starts, stale traces harm
analyzed separately. Model, tokenizer, adapter, and runtime changes                      34/135 branches versus 4/135 under current traces, a +22.2-point
remain bundled ecological contrasts, not identified capacity or fam-                     contrast with CI [8.9, 37.0] and exact Holm 𝑝 = 0.0337. Stale minus
ily effects. Outcome-blind runtime or adapter faults were repaired                       control is +12.6 points, CI [0.7, 25.9], but does not survive Holm
before restarting empty main roots; discarded attempts remain                            correction (𝑝 = 0.3934). Thus long-context editing pressure explains
receipted and no scientific design changed.                                              part, but not all, of the stale-current gap.
   With Devstral fixed, a 576-rollout 23 factorial randomizes state                         The stale-minus-current interaction across coders is +17.0 points
binding, proposal admission/rollback, and completion certification.                      (task-cluster 95% CI [0.7, 33.4]) but remains suggestive rather than
Task-equal main effects enter one six-test Holm family over unsafe                       confirmatory after its separate Holm correction (𝑝 = 0.3615); we
and sound completion. A separate 576-rollout equal-budget factorial                      therefore do not claim a general capacity effect. For 14B correct
crosses Contract OFF/ON with revision limits 1, 3, 5, and 8 while                        starts, stale traces change code in 81.5% of branches, versus 47.4%
holding action, test, token, and wall budgets fixed; its six-test family                 for current traces and 77.8% for control; the corresponding harms
covers depth, contract, and interaction effects. Full stack, runtime,                    are 25.2%, 3.0%, and 12.6%. Churn is therefore neither repair nor
pilot, and sensitivity specifications are in the reproduction artifact.                  semantic harm. Under both coders, character matching leaves a
   All reported experiments use the frozen research harness de-                          token-length difference (498.4 versus 451.7 mean prompt tokens
scribed above. The reference implementation was developed after-                         for stale and control), an audited nuisance rather than a complete
ward as an executable realization of the mechanically enforceable                        explanation.
AgenticDev ’26, October 12–16, 2026, Munich, Germany                                                                                                                                         Gao, Yang, Yang



                                               (a) Verifier risk-coverage                                                                   (b) Correctness is not monotone
                                                                                                                                     0.85
      Risk among accepted revisions



                                                                                                                                                                                    Current binary
                                      0.25




                                                                                                       Correct at current revision
                                                                                                                                                                                    Current trace
                                                                                                                                     0.80                                           Stale trace
                                      0.20                                                                                                                                          Unavailable

                                                                                                                                     0.75
                                      0.15

                                                                                                                                     0.70
                                      0.10
                                                                                    Qwen 7B
                                      0.05                                                                                           0.65
                                                                                    Qwen 14B
                                                                                    DeepSeek 6.7B
                                                                                                                                     0.60
                                               0.60   0.65    0.70 0.75 0.80             0.85   0.90                                          1                       2                           3
                                                              Selective coverage                                                                               Forced revisions


Figure 2: Left: retrospective selective risk at matched coverage. Cross-family diversity does not ensure verifier quality. Right:
current correctness across forced revisions is non-monotone even while cumulative ever-correct increases.

Table 3: Common-state repair and continuation harm. Each                                                                             effects. The clustering and redistribution explain why task-level,
cell is event count/135; starts and assignments are identical                                                                        not branch-level, uncertainty is essential.
across coders.

                                       Start      Evidence            7B event   14B event
                                       Wrong      Current binary      105/135     115/135
                                       Wrong      Current trace       113/135     120/135
                                       Wrong      Unavailable          97/135     126/135
                                       Wrong      Matched control     105/135     119/135                                            5.4    RQ3: Verifier Quality Is Not Independence
                                       Correct    Current binary         0/135       4/135                                           At native thresholds, Qwen-7B covers 0.757 of revisions at risk 0.095;
                                       Correct    Current trace          5/135       4/135                                           Qwen-14B covers 0.711 at risk 0.040; DeepSeek covers 0.991 at risk
                                       Correct    Unavailable            0/135      10/135                                           0.298. Coverage confounds direct comparison, so Figure 2a imposes
                                       Correct    Stale wrong trace     12/135      34/135                                           retrospective matched coverage. At 70%, risks are 0.050, 0.041, and
                                       Correct    Matched control        2/135      17/135                                           0.240, respectively. Qwen-14B minus DeepSeek is −19.9 points with
                                                                                                                                     task-bootstrap CI [−26.4, −9.5] when each bootstrap draw refits the
                                                                                                                                     cutoff. This compares the frozen distribution; deployment requires
                                                                                                                                     held-out calibration.
5.3                               Stale Evidence Resurrects Fixed Bugs                                                                  This ordering is not an artifact of choosing 70% coverage: Qwen-
Average uncertainty does not erase constructive counterexamples.                                                                     14B minus DeepSeek risk differences remain negative from 60%
For 7B, all correct-state harms occur in 4/27 tasks (Figure 4); stale                                                                through 90% coverage, ranging from −20.5 to −4.0 points, with all
traces regress HumanEval/10 and /89 in all five seeds. In /89, a stale                                                               five task-bootstrap intervals below zero. Repeated code states do
report from code using Caesar shift 12 changes the fixed shift 4 back                                                                affect the magnitude. Collapsing 2,700 revisions to 617 unique task–
to 12 in every seed. The report contains valid input/expected-output                                                                 code hashes raises 70%-coverage risks to 0.400, 0.387, and 0.472;
facts, but falsely asserts that they describe the current code.                                                                      Qwen-14B still has lower empirical AURC (0.225 versus 0.402) and
   For 14B, stale harm is broader: 34 branches across 12/27 task                                                                     8.5 points lower risk than DeepSeek. We therefore interpret 19.9
clusters. HumanEval/10 and /46 regress in 5/5 stale seeds while                                                                      points as the revision-distribution estimate, not an intrinsic model
their matched controls harm 0/5 and 1/5, respectively. Conversely,                                                                   constant.
/89 no longer regresses, and /50 and /120 fail under both stale and                                                                     Quality also does not imply independent errors. Among hidden-
control prompts. This redistribution is important: stale evidence is                                                                 incorrect revisions at 70% coverage, Qwen-7B/Qwen-14B have 𝜙 =
a reproducible failure mechanism, not a deterministic property of a                                                                  0.641 with task-cluster CI [0.096, 0.935] and excess joint false ac-
task, and responsiveness determines whether the mechanism fires.                                                                     ceptance 0.060 [0.001, 0.133]. Qwen-14B/DeepSeek have 𝜙 = 0.021
   This yields a sharper mechanism than “more information helps”:                                                                    [−0.231, 0.272] at the same coverage, but DeepSeek’s risk is much
utility depends jointly on payload, provenance, and the coder’s                                                                      higher. At 75% coverage, all three scored pairs have positive excess-
response. Candidate-source diagnostics also shift across coders and                                                                  joint intervals. Dependence is thus an operating-point property,
were not randomized, so they are descriptive rather than subgroup                                                                    not a static label attached to a pair of model families.
Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair                       AgenticDev ’26, October 12–16, 2026, Munich, Germany


                                         Qwen2.5-7B                Qwen2.5-14B                                                                                            5

                                                                                                   HumanEval/10            0           0        0         5           0
                                (a) Frozen wrong state                                                                                                                    4
                     100%                                                 93%
                                                        89%                              88%
                                         85%     84%




                                                                                                                                                                              Harm seeds
                                   78%                                            78%              HumanEval/89            0           0        0         5           0
                          80%                                                                                                                                             3
                                                                   72%
 Repair rate




                          60%                                                                     HumanEval/113            0           0        0         1           0   2


                          40%                                                                                                                                             1
                                                                                                                                    5
                                                                                                  HumanEval/137            0                    0         1           2
                                                                                                                               (5 invalid)
                          20%
                                                                                                                                                                          0
                                                                                                                        y           e        ne        le             l
                                                                                                                      ar       Tra
                                                                                                                                   c
                                                                                                                                           No       Sta           tro
                          0%                                                                                      Bin                                         Con
                                     Binary        Trace             None           Control
                                (b) Frozen correct state
                          30%
                                                                                                Figure 4: 7B correct-to-incorrect outcomes are clustered, not
                                                                            25.2%
                                                                                                uniform. HumanEval/10 and /89 show stale-evidence bug
                          25%                                                                   resurrection in 5/5 seeds; current-trace failures on /137 are
      Continuation harm




                                                                                                invalid action-schema outputs.
                          20%

                          15%                                                           12.6%
                                                                                                population risk: the conservative one-sided 95% zero-event bound
                          10%                                            8.9%
                                                                7.4%                            over 30 task clusters is 9.5%.
                                                                                                   Task-cluster uncertainty is wide enough to matter. Self-only risk
                          5%            3.0% 3.7%3.0%
                                                                                    1.5%        has a 95% interval of [0.154, 0.445], visible-gated risk [0, 0.077],
                                   0%                      0%
                          0%                                                                    and visible-gated sound completion [0.642, 0.900]. The zero-event
                                   Binary       Trace       None          Stale       Control   task bound is 1 − 0.051/30 = 0.095; treating 1,877 challenge-passing
                                                                                                revisions as independent would instead give 0.0016 and would be
                                                                                                anti-conservative for cross-task generalization. The empirical result
Figure 3: Assignment outcomes from identical frozen states.                                     supports executable gating in this domain, not a universal safety
Evidence ordering changes across coder capacities; 14B stale                                    guarantee.
evidence produces the largest continuation harm. Inference                                         Strict freshness is not free. Qwen-14B plus a current-evidence
is reported in text.                                                                            challenge has no observed false completion but covers only 38.4%,
                                                                                                loses 311 baseline sound completions, and requires 2.27 mean re-
Table 4: Verifier quality and conditional dependence. Risk is                                   visions. Reliability evaluation must expose this abstention/cost
at 70% coverage; 𝜙 is conditional on incorrect revisions.                                       trade-off.
                                                                                                   The prospective paired comparison estimates the bundled pol-
                                                                                                icy’s orchestrator-level effect. From correct starts, baseline con-
                                Verifier/pair              Risk      Conditional 𝜙
                                                                                                tinuation harms 13/135 branches and finishes correct on 122/135;
                                Qwen-7B                    0.050                  —             guarded execution has no observed harm and retains correctness
                                Qwen-14B                   0.041                  —             on 135/135. The −9.6-point harm contrast has a task-bootstrap 95%
                                DeepSeek-6.7B              0.240                  —
                                                                                                CI of [−20.7, 0.0] and sign-flip 𝑝 = 0.25, because all baseline harms
                                Qwen-7B / Qwen-14B            —              0.641              occur in only 3/27 task clusters. From wrong starts, repair falls
                                Qwen-7B / DeepSeek            —             −0.072              from 100/135 to 93/135. Across both start states, unsafe comple-
                                Qwen-14B / DeepSeek           —              0.021              tion changes from 1/270 to 0/270 (effect −0.4 points, CI [−1.1, 0.0]),
                                                                                                which is too sparse to demonstrate superiority. Sound completion
                                                                                                changes from 219/270 to 211/270 (effect −3.0 points, CI [−8.5, 1.1]),
5.5                       RQ4: Bundled Admission Changes                                        so the preregistered −5-point non-inferiority criterion is not met.
                          Retention and Repair                                                  The bundled guard therefore shifts observed errors while reducing
                                                                                                both revision plasticity and completion coverage; these data do not
Table 5 evaluates stopping and verification on the same 900 trajec-
                                                                                                identify any component’s individual effect.
tories. Self-only stopping accepts 99.8% but has 29.5% risk and 70.3%
sound completion. A visible gate prevents 248 false completions
and introduces none, reducing risk to 2.4% while increasing sound
                                                                                                5.6    RQ5: Repository Contracts Expose
completion to 77.8%. The challenge gate prevents all 265 self-only                                     Completion-Gate Dependence
false completions in this sample and attains 77.8% sound comple-                                Table 6 consolidates the four stack matrices. The original Qwen2.5-
tion at 77.8% coverage. Its zero observed errors do not imply zero                              14B study has a severe completion floor: Contract OFF produces
AgenticDev ’26, October 12–16, 2026, Munich, Germany                                                                                        Gao, Yang, Yang


                                        Co-primary repository-agent effects


          Unsafe completion                                                                                    -2.78 pp [-8.33, +0.00]




           Sound completion                                                                                    -0.69 pp [-2.08, +0.00]
                                                                           sound NI margin (-5 pp)

                                   −10.0                −7.5           −5.0           −2.5           0.0           2.5                     5.0
                                                                 Contract effect (ON minus OFF), percentage points

Figure 5: Prespecified repository-agent contract effects (ON minus OFF). Bars are task-cluster bootstrap 95% intervals over 24
task-level effects; the three seeds per cell are averaged before inference. Unsafe-completion superiority requires its one-sided
upper bound below zero; sound-completion non-inferiority requires its lower bound above −5 points. Only the latter, floor-
limited criterion is met, so the joint IUT fails.

Table 5: Stopping-policy replay over 900 fixed trajectories.                          Across the four stack matrices, accepted-completion totals are
CIs are task-clustered; paired changes are reported in text.                       only 5, 12, 6, and 4, and OFF-arm sound-completion rates are 0–
                                                                                   2.1%. Thus the tables expose the common floor directly: the contract
           Policy                       Cov.    Risk    Sound   Rounds             changes completion control but does not establish competence or
           Self only                    0.998   0.295   0.703     1.03             liveness.
           Self + visible               0.797   0.024   0.778     1.55
           Self + challenge             0.778   0.000   0.778     1.56
           Qwen-14B only                0.794   0.046   0.758     1.52             6    Evidence-Bound Typed Loop Contract
           Qwen-14B + challenge         0.769   0.000   0.769     1.55
           Challenge executable         0.788   0.000   0.788     1.52            The observed failures motivate an auditable orchestration specifica-
           Qwen-14B + fresh challenge   0.384   0.000   0.384     2.27
                                                                                  tion, not a universally validated remedy or a new prompting recipe.
                                                                                  Its four interfaces separate obligations that the negative policy and
                                                                                  factorial decisions show must be evaluated rather than assumed.
five accepted completions, whereas Contract ON produces none.
It removes all four observed unsafe completions but also the only                      State-bound evidence. Every observation is carried in an envelope
sound one; 276/288 rollouts exhaust the action budget. Figure 5 gives                           𝐸 = (ℎ𝑐𝑜𝑑𝑒 , ℎ𝑠𝑢𝑖𝑡𝑒 , 𝑒𝑥𝑒𝑐𝑢𝑡𝑖𝑜𝑛_𝑖𝑑, 𝑝𝑎𝑦𝑙𝑜𝑎𝑑).
the task-equal effects. Unsafe completion changes by −2.78 points
(task-cluster 95% CI [−8.33, 0.00]), missing strict superiority, while            The orchestrator may use 𝐸 to revise only when ℎ𝑐𝑜𝑑𝑒 equals the
sound completion changes by −0.69 points ([−2.08, 0.00]), passing                 current state hash. A mismatch triggers refresh, Keep, or Escalate;
the −5-point margin. With only one OFF-arm sound completion,                      it never directly triggers a patch.
that pass is weak liveness evidence and the joint decision is negative.             Typed revision actions. Free-form text conflates “no edit is needed”
    The 32B stack is the only replication with observed unsafe com-               with “the attempted patch was unparsable.” We use
pletion under Contract ON: six unsafe completions are concentrated
                                                                                       𝑅𝑒𝑣𝑖𝑠𝑖𝑜𝑛𝐴𝑐𝑡𝑖𝑜𝑛 = Keep | Patch(𝑐𝑜𝑑𝑒) | Escalate(𝑟𝑒𝑎𝑠𝑜𝑛).
in two tasks, and the gate false-passes incorrect proposals and
submissions. Qwen3-Coder-Next and Devstral show no observed                        Only a parsed, executable Patch may replace the current state. In
unsafe completion, but they produce only six and four accepted                     the 7B common-state study, all five current-trace harms on Hu-
completions, respectively; 282/288 and 284/288 rollouts exhaust                    manEval/137 are responses containing only STATUS: DONE without
their action budgets. These are stack-level ecological contrasts,                  code. A fail-closed parser that maps this action to Keep, rather than
not identified capacity or model-family effects. Full gate, cost, and              treating it as an invalid patch, would retain the correct checkpoint
sensitivity breakdowns remain in the artifact.                                     in these recorded branches.
    Table 7 moves the two Devstral factorials into one inferential
                                                                                      Last-known-good checkpoint. The ledger records code and ev-
summary. No component, depth, contract, or interaction effect
                                                                                   idence hashes for the last state that passed the configured gate.
survives its preregistered six-test Holm family. Certification has
                                                                                   Invalid actions never overwrite it. This makes correctness absorb-
the largest descriptive sound-completion effect, but only four tasks
                                                                                   ing with respect to parser and protocol failures even when model
support it and 𝐶 = 0 removes the checkpoint-completion path; the
                                                                                   behavior is not.
contrast therefore partly reflects endpoint mechanics rather than an
isolated semantic verification benefit. The depth factorial contains                  Risk- and dependence-aware stopping. Verifier selection uses risk
0/576 unsafe and 25/576 sound completions. Revision caps rarely                    at the intended coverage and conditional dependence, not model
bind, so its null depth result concerns this sparse-proposal process,              diversity as a proxy. Our matched-coverage estimates are retro-
not loop depth in general.                                                         spective; deployment additionally requires held-out calibration and
Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair               AgenticDev ’26, October 12–16, 2026, Munich, Germany


Table 6: Repository-agent stack matrices. Each arm has 72 rollouts and reports accepted/unsafe/sound counts; effects are
task-equal Contract ON minus OFF percentage points with task-cluster 95% CIs. Every joint IUT fails; sound non-inferiority
passes only under severe completion floors.

                      Stack                   Current/OFF Current/ON Stale/OFF Stale/ON                  Δ unsafe [95% CI]      Δ sound [95% CI]
                      Qwen2.5-14B                  3/2/1          0/0/0         2/2/0        0/0/0      −2.78 [ −8.33, 0.00] −0.69 [ −2.08, 0.00]
                      Qwen2.5-Coder-32B            2/0/2          5/3/2         1/0/1        4/3/1      +4.17 [0.00, 11.11]   0.00 [ −2.08, 2.08]
                      Qwen3-Coder-Next             0/0/0          2/0/2         0/0/0        4/0/4         0.00 [0.00, 0.00] +4.17 [0.00, 11.11]
                      Devstral Small 2 24B         0/0/0          2/0/2         0/0/0        2/0/2         0.00 [0.00, 0.00]  +2.78 [0.00, 7.64]


Table 7: Devstral factorial effects (percentage points; 𝑛 = 576 each). CIs are task-cluster 95%; 𝑝 𝐻 is Holm-adjusted within each
six-test family. B, A, and C denote state binding, admission/rollback, and completion certification.

                           Design (𝑛 = 576)         Contrast                        Δ unsafe [95% CI]; 𝑝 𝐻          Δ sound [95% CI]; 𝑝𝐻
                           23 components            B: state binding              −0.69 [ −2.08, 0.00]; 1.000      +0.69 [0.00, 1.74]; 1.000
                                                    A: admission/rollback          0.00 [0.00, 0.00]; 1.000       +0.69 [ −0.69, 2.43]; 1.000
                                                    C: certification               +0.69 [0.00, 2.08]; 1.000      +6.25 [0.69, 13.19]; 0.753
                           4 × 2 depth–contract     Cap 1 to cap 8                  0.00 [0.00, 0.00]; 1.000      −0.23 [ −1.77, 1.09]; 1.000
                                                    Contract ON minus OFF           0.00 [0.00, 0.00]; 1.000       +3.13 [0.00, 9.03]; 1.000
                                                    Depth × contract                0.00 [0.00, 0.00]; 1.000      −0.45 [ −7.63, 6.27]; 1.000


drift monitoring. A completion decision records its operating point                         At the frozen snapshot, all 35 deterministic failure-injection cases
so residual risk remains auditable.                                                      and three managed-language fixtures pass. This is conformance
                                                                                         evidence, not effectiveness, competence, verifier independence, or
6.1     Operational Semantics                                                            study validation. The public v0.1.1 release provides source, com-
                                                                                         mands, and the case catalog.
The contract turns a permissive text loop into a small state machine.
                                                                                            In deterministic replay, state binding intercepts all 12 and 34
At step 𝑡, the orchestrator stores current state 𝑆𝑡 , last-known-good
                                                                                         stale-condition harms for 7B and 14B; adding typed action reduces
state 𝐿𝑡 (possibly empty), and an append-only evidence ledger. It
                                                                                         total harm from 19 → 2 and 69 → 33. A challenge checkpoint
executes the following transaction:
                                                                                         blocks all 19 7B harms but misses two 14B hidden-test regressions.
(1) run a named suite on 𝑆𝑡 ; append evidence bound to the state
                                                                                         Because stale evidence is assigned only to correct starts, replay
    and suite;
                                                                                         diagnoses mechanisms rather than end-to-end utility.
(2) reject or refresh 𝐸𝑡 if either hash does not match the requested
    state and suite;
(3) request one typed action; Keep leaves state unchanged, Esca-                         7    Discussion
    late abstains, and only a parseable Patch creates candidate                             Controlled counterexamples. Search does not ensure retention;
    𝑆𝑡′ ;                                                                                valid reports become harmful under state mismatch; and model-
(4) evaluate 𝑆𝑡′ with the configured commit gate; on failure retain                      family diversity ensures neither low verifier risk nor independent
    𝑆𝑡 or roll back to 𝐿𝑡 , never overwrite 𝐿𝑡 ;                                         errors. Iteration cannot substitute for evidence, state management,
(5) stop only if the completion policy accepts the committed state at                    or verification.
    its declared risk–coverage operating point; otherwise continue
    within budget.                                                                          What they do not refute. Loops remain useful when expected
Two safety properties follow mechanically. First, a state-hash mis-                      repair exceeds continuation harm. We critique unconditional con-
match cannot trigger a commit. Second, parser or action-schema                           tinuation and unqualified completion, not adaptive search: depth
failure cannot erase a checkpoint. Neither property claims that                          samples transitions; orchestration determines whether value accu-
a hash-matched patch is semantically correct; that residual risk                         mulates.
belongs to the executable and learned verifiers.
                                                                                            Why the three factors are not interchangeable. Better feedback
                                                                                         cannot help an unresponsive coder; responsiveness can amplify
6.2     StateSeal Reference Implementation and
                                                                                         stale evidence; and proposal quality cannot offset correlated false
        Conformance                                                                      acceptance. Equation 8 requires both low marginal false acceptance
StateSeal wraps existing agents and project-defined verifiers. Its                       and low dependence.
admission broker recomputes state identity, verifies an isolated
proposal outside the agent process, preserves a checkpoint, and                             Safety, plasticity, liveness, and interface fit are separate. The
recertifies it before issuing a digest-bearing receipt. It records cov-                  prospective policy prevents observed regression but rejects useful
erage and delivery impact but does not learn risk or dependence.                         repairs; repository contracts similarly trade unsupported against
AgenticDev ’26, October 12–16, 2026, Munich, Germany                                                                                                              Gao, Yang, Yang


                          Table 8: Contract obligations, reference mechanisms, conformance cases, and residual risks.

    Obligation                       Reference mechanism                                Conformance evidence                  Residual risk
    State-bound evidence             Bind candidate, tree, policy, verifier, and con-   Reject replay, mutation, and wrong-   Aligned evidence may be wrong; host and verifier
                                     text identities                                    tree evidence (SB001–SB007)           remain trusted
    Independent admission            Broker alone advances verified state and is-       Self-report cannot authorize admis-   Process separation does not imply error indepen-
                                     sues decisions                                     sion (SB021, SB027)                   dence
    Checkpoint preservation          Retain and exactly restore the last verified       Regressions and malformed actions     Only oracle-covered properties are preserved
                                     candidate                                          cannot overwrite it (SB008–SB010,
                                                                                        SB014, SB016)
    Fresh certification              Re-execute checks on the selected completion       Failed recertification cannot com-    Flakiness, drift, and suite incompleteness remain
                                     state                                              plete (SB012, SB020, SB031)
    Auditable stopping               Typed outcomes, hash-linked events, digest-        False pass/rejection, abstention,     Auditability is not calibration, liveness, or attes-
                                     bearing receipt, coverage and liveness fields      and coverage collapse are explicit    tation
                                                                                        (SB028–SB035)



sparse sound completion. Neither randomized factorial is Holm-                               6, and 4 accepted completions; under this floor, the absolute −5-
significant. Admission, preservation, certification, interface fit, and                      point non-inferiority margin weakly constrains liveness. Task-equal
depth remain distinct.                                                                       inference has project-equal and leave-one-project-out checks, but
                                                                                             only nine projects support project-level generalization.
   Implications for agent evaluation. Pass@1 or best-of-𝑘 misses
state loss, incorrect acceptance, and low risk from abstention. Evalu-                          Reproducibility. Prompts, private suites, full lineage, and the nu-
ations should also report current versus ever-correct, common-state                          merical reconstruction package are retained internally. The public
transitions, coverage–risk, sound completion, cost, and conditional                          materials provide the StateSeal v0.1.1 source, commands, and case
verifier overlap. Our 24 repository bugs test mechanisms, not preva-                         catalog; licensing and evaluator privacy prevent redistribution of
lence.                                                                                       the full raw trajectories and private suites. The post-study artifact
                                                                                             tests mechanism conformance, not effectiveness, verifier adequacy
  Mechanism, policy, and calibration. State binding, transition
                                                                                             or independence, or trust in the host, runner, Git, and OS. Strict
guards, checkpoints, and recertification are mechanical. Verifier ad-
                                                                                             admission can reject useful repairs; its UI is outside the trusted
equacy, error dependence, residual risk, and safety–liveness remain
                                                                                             boundary.
empirical. The implementation makes failure modes falsifiable; it
does not improve agent or oracle competence.
                                                                                             9    Conclusion
8      Threats to Validity                                                                  Iteration supplies proposals, not reliability. The typed contract
                                                                                            separates state alignment, admission, preservation, grounded com-
   External validity. The trajectory and common-state studies use
                                                                                            pletion, competence, liveness, and interface fit; its implementation
public HumanEval tasks that may occur in model training data, and
                                                                                            enforces state binding, checkpoints, recertification, and auditable
27 tasks are selected for 7B-observed repairability. Pairing strength-
                                                                                            decisions. Verifier quality, dependence, and general reliability re-
ens assignment contrasts but not absolute-rate generalization. The
                                                                                            main empirical.
repository study covers 24 bugs from nine Python projects, four
                                                                                            Availability and disclosures. The numerical reconstruction pack-
coder stacks, and one scaffold. Stack factors vary jointly, interface
                                                                                            age is retained internally; private suites and licensed source are
friction is material, and tasks within projects may be correlated;
                                                                                            not redistributed. StateSeal v0.1.1 is at https://github.com/hellogxp/
these are mechanism tests, not random samples of agents, lan-
                                                                                            stateseal. AI-assisted code and prose were author-verified.
guages, projects, or bugs. The controlled function-level studies stop
at 14B parameters and do not establish that frontier-scale hosted
models have the same transition kernel.
   Construct validity. Challenge and hidden inputs are disjoint but
share HumanEval+ construction, and no finite repository suite is a
complete specification. One-step staleness is an intervention, not
its natural prevalence; exact-code change is not semantic churn.
Verifier family and capacity are confounded. Self acceptance is
declarative, whereas repository acceptance also includes the ON
arm’s frozen checkpoint rule.
   Internal and statistical validity. Forced revision is not a natural
adaptive policy. Common states address post-treatment risk-set bias,
but all six 7B and five of six 14B contrasts are nonsignificant after
Holm correction; no secondary cross-coder interaction survives
correction. The original repository contract identifies only a joint
effect; component randomization remains event-sparse, and the
depth caps rarely bind. The four stack matrices have only 5, 12,
Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair                 AgenticDev ’26, October 12–16, 2026, Munich, Germany


References                                                                                    Information Processing Systems, Vol. 36. Neural Information Processing Systems
 [1] Islem Bouzenia and Michael Pradel. 2025. Understanding Software Engineer-                Foundation, Inc., 46534–46594. doi:10.52202/075280-2019
     ing Agents: A Study of Thought-Action-Result Trajectories. In 40th IEEE/ACM         [16] Qianru Meng, Xiao Zhang, Zhaochun Ren, and Joost Visser. 2026. EviACT:
     International Conference on Automated Software Engineering. IEEE, 2846–2857.             An Evidence-to-Action Framework for Agentic Program Repair. arXiv preprint
     doi:10.1109/ASE63991.2025.00234                                                          arXiv:2605.27238 (2026). doi:10.48550/arXiv.2605.27238
 [2] José Pablo Cambronero, Michele Tufano, Sherry Shi, Renyao Wei, Grant Uy, Runx-      [17] Open Policy Agent Contributors. 2026. Open Policy Agent Documentation.
     iang Cheng, Chin-Jung Liu, Shiying Pan, Satish Chandra, and Patrick Rondon.              Accessed 2026-07-24. https://www.openpolicyagent.org/docs
     2026. Abstain and Validate: A Dual-LLM Policy for Reducing Noise in Agentic         [18] Arjun Panickssery, Samuel R. Bowman, and Shi Feng. 2024. LLM Evaluators
     Program Repair. In Proceedings of the IEEE/ACM 48th International Conference on          Recognize and Favor Their Own Generations. In Advances in Neural Information
     Software Engineering: Software Engineering in Practice. Association for Computing        Processing Systems, Vol. 37. Neural Information Processing Systems Foundation,
     Machinery, 118–129. doi:10.1145/3786583.3786858                                          Inc., 68772–68802. doi:10.52202/079017-2197
 [3] Edward Y. Chang, Longling Geng, and Emily J. Chang. 2026. Mnemosyne: Agentic        [19] Andrey Podivilov, Vadim Lomshakov, Sergey Savin, Matvei Startsev, Roman
     Transaction Processing for Validating and Repairing AI-Generated Workflows.              Pozharskiy, Maksim Parshin, and Sergey Nikolenko. 2026. AgentLens: Production-
     arXiv preprint arXiv:2607.00269 (2026). doi:10.48550/arXiv.2607.00269                    Assessed Trajectory Reviews for Coding Agent Evaluation. arXiv preprint
 [4] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira             arXiv:2607.06624 (2026). doi:10.48550/arXiv.2607.06624
                                                                                         [20] Qwen, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen
     Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, et al. 2021. Evaluating Large
                                                                                              Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang,
     Language Models Trained on Code. arXiv preprint arXiv:2107.03374 (2021). doi:10.
                                                                                              Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang
     48550/arXiv.2107.03374
                                                                                              Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue,
 [5] Dekun Dai, MingWei Liu, Anji Li, Jialun Cao, Yanlin Wang, Chong Wang, Xin
                                                                                              Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia,
     Peng, and Zibin Zheng. 2025. FeedbackEval: A Benchmark for Evaluating
                                                                                              Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan,
     Large Language Models in Feedback-Driven Code Repair Tasks. arXiv preprint
                                                                                              Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. 2024. Qwen2.5 Technical
     arXiv:2504.06939 (2025). doi:10.48550/arXiv.2504.06939
                                                                                              Report. arXiv preprint arXiv:2412.15115 (2024). doi:10.48550/arXiv.2412.15115
 [6] Yonatan Geifman and Ran El-Yaniv. 2019. SelectiveNet: A Deep Neural Network
                                                                                         [21] Priyam Sahoo, Gaurav Mittal, Xiaomin Li, Shengjie Ma, Benjamin Steenhoek,
     with an Integrated Reject Option. In Proceedings of the 36th International Con-
                                                                                              Pingping Lin, and Yu Hu. 2026. AgentLens: Revealing the Lucky Pass Problem
     ference on Machine Learning (Proceedings of Machine Learning Research, Vol. 97).
                                                                                              in SWE-Agent Evaluation. arXiv preprint arXiv:2605.12925 (2026). doi:10.48550/
     PMLR, 2151–2159. https://proceedings.mlr.press/v97/geifman19a.html
                                                                                              arXiv.2605.12925
 [7] Thibaud Gloaguen, Niels Mündler, Mark Niklas Mueller, Veselin Raychev, and
                                                                                         [22] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and
     Martin Vechev. 2026. Coding Agents Don’t Know When to Act. In Second Work-
                                                                                              Shunyu Yao. 2023. Reflexion: Language Agents with Verbal Reinforcement Learn-
     shop on Agents in the Wild: Safety, Security, and Beyond. https://openreview.net/
                                                                                              ing. In Advances in Neural Information Processing Systems, Vol. 36. Neural Informa-
     forum?id=CVg4Honh4Y
                                                                                              tion Processing Systems Foundation, Inc., 8634–8652. doi:10.52202/075280-0377
 [8] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang,
                                                                                         [23] Supply-chain Levels for Software Artifacts. 2026. SLSA v1.2 Provenance. Accessed
     Guanting Chen, Xiao Bi, Y. Wu, Y. K. Li, et al. 2024. DeepSeek-Coder: When
                                                                                              2026-07-24. https://slsa.dev/spec/v1.2/provenance
     the Large Language Model Meets Programming—The Rise of Code Intelligence.
                                                                                         [24] Santiago Torres-Arias, Hammad Afzali, Trishank Karthik Kuppusamy, Reza Curt-
     arXiv preprint arXiv:2401.14196 (2024). doi:10.48550/arXiv.2401.14196
                                                                                              mola, and Justin Cappos. 2019. in-toto: Providing Farm-to-Table Guarantees for
 [9] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei
                                                                                              Bits and Bytes. In 28th USENIX Security Symposium. USENIX Association, 1393–
     Yu, Xinying Song, and Denny Zhou. 2024. Large Language Models Cannot Self-
                                                                                              1410. https://www.usenix.org/conference/usenixsecurity19/presentation/torres-
     Correct Reasoning Yet. In International Conference on Learning Representations.
                                                                                              arias
     https://openreview.net/forum?id=IkmD3fKBPQ
                                                                                         [25] Gladys Tyen, Hassan Mansoor, Victor Carbune, Peter Chen, and Tony Mak. 2024.
[10] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir
                                                                                              LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error
     Press, and Karthik R. Narasimhan. 2024. SWE-bench: Can Language Models
                                                                                              Location. In Findings of the Association for Computational Linguistics: ACL 2024.
     Resolve Real-World GitHub Issues?. In International Conference on Learning Rep-
                                                                                              Association for Computational Linguistics, 13894–13908. doi:10.18653/v1/2024.
     resentations. https://openreview.net/forum?id=VTF8yNQM66
                                                                                              findings-acl.826
[11] Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, and Rui Zhang. 2024. When
                                                                                         [26] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2025. De-
     Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-
                                                                                              mystifying LLM-Based Software Engineering Agents. Proceedings of the ACM on
     Correction of LLMs. Transactions of the Association for Computational Linguistics
                                                                                              Software Engineering 2, FSE (2025), 801–824. doi:10.1145/3715754
     12 (2024), 1417–1440. doi:10.1162/tacl_a_00713
                                                                                         [27] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao,
[12] Elliot Myunghoon Kim, Avi Garg, Kenny Peng, and Nikhil Garg. 2025. Correlated
                                                                                              Karthik Narasimhan, and Ofir Press. 2024. SWE-agent: Agent-Computer Inter-
     Errors in Large Language Models. In Proceedings of the 42nd International Confer-
                                                                                              faces Enable Automated Software Engineering. In Advances in Neural Information
     ence on Machine Learning (Proceedings of Machine Learning Research, Vol. 267).
                                                                                              Processing Systems, Vol. 37. Neural Information Processing Systems Foundation,
     PMLR, 30038–30066. https://proceedings.mlr.press/v267/kim25e.html
                                                                                              Inc., 50528–50652. doi:10.52202/079017-1601
[13] Cuong Chi Le, Aashish Yadavally, Minh Le-Anh, and Tien N. Nguyen. 2026.
                                                                                         [28] Yunxiang Zhang, Muhammad Khalifa, Lajanugen Logeswaran, Jaekyeom Kim,
     Benchmarking Code Improvement with Progressive, Adaptive, and Interactive
                                                                                              Moontae Lee, Honglak Lee, and Lu Wang. 2024. Small Language Models Need
     Feedback. arXiv preprint arXiv:2607.01360 (2026). doi:10.48550/arXiv.2607.01360
                                                                                              Strong Verifiers to Self-Correct Reasoning. In Findings of the Association for
[14] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is
                                                                                              Computational Linguistics: ACL 2024. Association for Computational Linguistics,
     Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large
                                                                                              15637–15653. doi:10.18653/v1/2024.findings-acl.924
     Language Models for Code Generation. In Advances in Neural Information Pro-
                                                                                         [29] Bingchen Zhao, Dhruv Srikanth, Yuxiang Wu, and Zhengyao Jiang. 2026.
     cessing Systems, Vol. 36. Neural Information Processing Systems Foundation, Inc.,
                                                                                              SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents. arXiv
     21558–21572. doi:10.52202/075280-0943
                                                                                              preprint arXiv:2605.21384 (2026). doi:10.48550/arXiv.2605.21384
[15] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
     Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al.
     2023. Self-Refine: Iterative Refinement with Self-Feedback. In Advances in Neural   Received 2026-07-23; accepted 2026-08-20
