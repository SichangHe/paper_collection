                                            F ORALL -L EAN -AGENT for Auditable Reasoning in
                                              Formal Mathematics and Software Verification


                                                                                    Naing Oo Lwin
                                                                                      Astrio Labs
                                                                              nolan.lwin@astriolabs.com
arXiv:2610.00885v1 [cs.SE] 1 Oct 2026




                                                                                             Abstract

                                                  Coding agents increasingly automate Lean proof development, but successful
                                                  compilation alone does not establish that a candidate proves the intended statement
                                                  under acceptable assumptions. We present F ORALL -L EAN -AGENT, a frontend-
                                                  agnostic framework for auditable reasoning in formal mathematics and software
                                                  verification. The framework combines isolated workspaces, Lean tools, and fresh
                                                  review with statement comparison, axiom audits, and independent proof checking
                                                  where supported. Verification evidence and reviewer decisions are bound to the
                                                  same candidate artifact, making acceptance traceable. We evaluate the framework
                                                  on VeriSoftBench, PutnamBench, and both problems in the Lean Eval software-
                                                  verification track. On the 100-task VeriSoftBench subset, integration with F ORALL -
                                                  L EAN -AGENT raises benchmark-rule success from 93 to 100 for GPT-5.6 Sol at
                                                  low effort while reducing cost from $69 to $62. The PutnamBench evaluation
                                                  accepts all 672 problems at an average of $4.72 each. These results show that agent
                                                  harness design can improve correctness and efficiency while providing evidence
                                                  beyond aggregate solve counts.


                                        1    Introduction

                                        Lean 4 provides a formal language and trusted kernel for checking mathematical arguments and
                                        software properties [10]. General-purpose coding agents can use this infrastructure to search libraries,
                                        construct candidate proofs, and revise them in response to compiler diagnostics. Recent systems
                                        demonstrate that this approach can support competition mathematics and substantial formalization
                                        tasks without training a dedicated prover [6, 17, 21]. Their evaluation depends on the protocol
                                        connecting proof generation to verification.
                                        A successful Lean elaboration establishes correctness relative to the elaborated statement and its
                                        dependencies. It does not, by itself, establish that an agent preserved the intended statement, avoided
                                        reference solutions, or submitted the same artifact that was subsequently reviewed. These distinctions
                                        matter for agents with filesystem, shell, and network access. Evaluation also depends on the handling
                                        of resource limits and infrastructure errors. A reported failure may reflect an unavailable service or a
                                        broken scoring environment, while a reported success may depend on information excluded by the
                                        benchmark protocol.
                                        F ORALL -L EAN -AGENT addresses these concerns through a common execution and acceptance
                                        protocol for Lean proving. It separates an actor that constructs proofs from a fresh reviewer that
                                        examines each verified candidate. It restricts runtime access to permitted task context, exposes
                                        declaration statements through retrieval tools, and records the evidence used for acceptance. The
                                        framework is frontend agnostic, with an adapter interface that supports integration with additional
                                        coding agents.
                                        The principal contributions are the following.

                                        NeurIPS 2026 Workshop on AI for Verifiable Coding.
                          Sandbox

                             Coding agents                         MCP tools
           LLM                                                                                     Axiom audit
                                                               ∀ Forall-Lean-MCP                   #print axioms
          VSB 271                                             lookup · search · usages
      theorem progress
       t T :             Codex Claude Code OpenCode                                                Comparator
       HasType t T →                                          Benchmark-specific MCP
       value t ∨            Write and refine proofs            vsb_mcp, pb_mcp, ...                nanoda (Lean Eval)
       ∃ t’, Step t t’
      := by sorry                                                          compile / submit
                                        revise




                             Fresh reviewer                      Lean verifier                   Acceptance
                         Read-only; no actor transcript          Statement integrity          Verifier + reviewer agree
                           Recompile and critique                 Kernel checking                  Same SHA-256


                                                                 approve                       Accepted proof
                                                                                                    proof.lean


Figure 1. The F ORALL -L EAN -AGENT workflow. A coding agent develops a candidate in an isolated
sandbox using Lean and MCP tools. A fresh reviewer recompiles and assesses the candidate without
access to the actor’s transcript. Acceptance binds the verifier result, reviewer approval, and stored
artifact to one digest. Axiom auditing checks dependencies, and Lean Eval additionally uses an
independent comparator. The input illustrates VeriSoftBench task 271, TM.progress, with repository
context omitted.


1. An auditable execution protocol that combines isolated workspaces, persistent proof generation,
   fresh review, and acceptance tied to a specific candidate artifact.
2. An empirical comparison of coding-agent frontends and execution protocols on VeriSoftBench-
   Aristotle, with separate reporting of benchmark success, axiom compliance, and independent-
   checker coverage.
3. Applications to mathematical verification on PutnamBench and two independently checked Lean
   Eval software developments, together with an analysis of information leakage and infrastructure
   errors that can invalidate aggregate measurements.


2   Related work

Agentic proof generation. COPRA uses execution feedback to guide formal proof generation [24].
LeanDojo and Pantograph provide interfaces for premise retrieval and interaction with Lean [3, 29].
More recent approaches place these capabilities within general-purpose agent workflows. Numina-
Lean-Agent combines Claude Code with a Lean MCP server for retrieval, compilation, and auxiliary
reasoning [4, 17]. Ax-Prover separates orchestration, proving, and verification [6], while Requena
et al. [21] study iterative refinement, library search, and context management in a minimal agent.
Specialized systems additionally use learned proof search, recursive decomposition, and blueprint
construction [1, 8, 9, 16, 26]. F ORALL -L EAN -AGENT builds on iterative proof generation and review,
with an emphasis on access restrictions and the evidence required to accept a candidate.
Evaluation settings. PutnamBench contains 672 formalized competition problems in its Lean
answer-given configuration [25]. VeriSoftBench extends evaluation to 500 proof obligations from 23
repositories, where project-specific definitions and dependencies differ from the Mathlib setting [28].
Context dependence is also central to miniCTX [11], while vericoding benchmarks evaluate verified
program synthesis [7]. Lean Eval includes larger formal developments and checks submissions
against trusted challenge statements using a comparator and an independent kernel [2, 13, 14]. Recent
studies examine code agents for software verification [12, 15, 22]. Our evaluation uses a shared
acceptance design across these settings while retaining their distinct context and budget requirements.
Verification and execution control. Independent comparison of elaborated environments addresses
failure modes that compilation alone cannot exclude [13]. F ORALL -L EAN -AGENT combines verifier-
controlled continuation with fresh review, candidate digests, and runtime access logs. Context
separation between actor and reviewer is an additional diagnostic mechanism. Formal correctness
continues to depend on the verifier and its trusted environment.


                                                          2
3     Framework
3.1   Execution model

F ORALL -L EAN -AGENT coordinates proof generation, tool access, and acceptance through a task-
specific workspace. The actor is a resumable coding-agent session, and the verifier is controlled by
the framework. The framework is frontend agnostic. Its adapter interface separates frontend-specific
session management from the shared execution and acceptance protocol. Current adapters support
Claude Code, Codex, and OpenCode [5, 19, 23], and additional frontends can be integrated through
the same interface. Benchmark adapters provide the target statement, build environment, and scoring
procedure. The separation allows the same review and artifact checks to operate on Mathlib problems,
repository theorems, and multi-file developments. The actor cannot modify framework state or
acceptance records.

3.2   Workspace isolation

The workspace contains the context permitted by the evaluation protocol. For repository tasks, the
actor receives a sanitized project with proof bodies removed and the target theorem withheld from
retrieval. For PutnamBench, the environment contains the build configuration and compiled Mathlib
dependencies without the benchmark checkout that carries reference solutions. We use runtime
blindness to denote these access restrictions. This term makes no claim about the model’s training
data.
Shell-enabled configurations enforce filesystem restrictions across the process tree using an operating-
system sandbox. A local CONNECT proxy limits outbound traffic to the model provider. Tool-
restricted configurations instead validate tool names and resolve path arguments before execution.
Restrictions cover alternative checkouts, repository history, previous outputs, and frontend scratch
state. Access decisions are logged.

3.3   Lean tools and retrieval

The MCP interface separates general Lean retrieval from benchmark-specific operations. Forall-
Lean-MCP provides lookup, search, usages, and outline. Responses contain declaration
kinds, statements, and source locations without proof bodies. Benchmark-specific servers, including
vsb_mcp and pb_mcp, provide task initialization, compilation, and submission. Shell-based adapters
can invoke the build and external scorer directly while retaining the acceptance protocol.
Statement-only retrieval makes repository interfaces available without exposing completed proofs
through the retrieval channel. Its design was motivated by two exploratory evaluations in which
navigation accounted for 51 to 65% of tool calls and compilation for 10 to 20%. These exploratory
counts motivate the interface without isolating its effect on success.

3.4   Candidate review and acceptance

When a candidate passes the verifier, the framework starts a fresh reviewer session. The reviewer
receives the task statement and candidate through read-only access and cannot inspect the actor’s
transcript, previous reviews, or orchestration state. It recompiles the candidate and checks for
statement weakening, name shadowing, altered answer values, unsupported assumptions, and vacuous
or circular constructions. It then returns an explicit verdict and the candidate digest.
Acceptance requires a verifier pass and reviewer approval for the same artifact. The digest in the
submission result must match the reviewer’s compilation evidence and the proof stored on disk. A
mismatch invalidates acceptance. Rejection feedback is made available to the persistent actor for
another revision. An HMAC authenticates resumption state and binds it to the task and directory.
Invalid partial state is quarantined.

3.5   Continuation and termination

The framework determines task completion from verification evidence. If an actor turn ends without
a verifier pass, the same session resumes with the latest diagnostics and an instruction to continue.
External limits on rounds, time, spending, and continuation requests still apply.


                                                   3
The outcome record distinguishes acceptance, exhausted review budgets, resource caps, and infras-
tructure interruptions. Authentication or usage errors that occur before any inference expenditure
leave the task resumable without assigning a proof outcome. Suspected false statements are examined
separately from proof failures.

3.6     Verification and artifact audit

The layered verifier checks candidate syntax, preservation of the frozen statement, declaration
shadowing, elaboration, and kernel axioms. The syntactic screen rejects admissions, declared
axioms, disallowed imports, and mechanisms such as native_decide, @[implemented_by], and
@[extern]. Statement comparison ignores whitespace and comments. The shadowing guard rejects
new bindings that change how names in the target resolve, except declarations already present in
the trusted template. This matters because redefining IsGreatest as set membership removes its
upper-bound requirement while allowing an apparently unchanged theorem to elaborate.
The axiom audit queries #print axioms for the target. The strict policy permits propext,
Classical.choice, and Quot.sound. For VeriSoftBench, benchmark-rule success is reported
separately from strict success because repository lemmas can inherit sorryAx or native-evaluation
axioms. A candidate may satisfy the benchmark’s scoring rule while failing this stricter policy. Lean
Eval additionally requires the pinned comparator, lean4export, and the independent nanoda kernel
in a Linux environment. Independent-checker coverage on VeriSoftBench is reported with its own
denominator.
Accepted artifacts are re-verified serially against clean repositories. The audit retains the submitted
proof, verifier evidence, axiom dependencies, actor and reviewer transcripts, execution metadata, and
access logs. Text similarity to withheld reference proofs identifies candidates for manual inspection.
Similarity is a screening measure and does not by itself establish leakage or independence. For legacy
evaluations in which the final file differs from the submitted file, scoring uses the submit-time artifact
recovered from the transcript. Unrecoverable artifacts are excluded.


4     Experimental setup

Tasks and coverage. The main repository evaluation uses the 100-task VeriSoftBench-Aristotle
subset drawn from 11 repositories. The tasks cover compiler verification, type systems, circuit
libraries, probabilistic programs, and separation logic. Task 222 requires a recovered dependency
revision because its original pinned revision is no longer available upstream. The replacement targets
the same Lean version and is identified separately in the provenance record. The PutnamBench
evaluation covers 672 problems in the Lean answer-given configuration. The Lean Eval evaluation
covers both problems in its software-verification track, strong normalization for the calculus of
constructions and quantifier elimination for real closed fields.
Configurations. Table 1 lists models, effort, and the target protocol Pass@8 with r = 3, meaning
up to eight samples and three local compiler invocations per sample. Reviewer rounds are separate.
Appendices A and C document recorded budgets and prompts.
Comparisons and accounting. Within-frontend comparisons fix model and effort, but sampling,
compilation, and review budgets differ. We compare benchmark-rule success, strict correctness,
tokens, and cost without isolating component effects or assuming equal budgets. Costs include
generation, review, and retries. Cumulative scores include documented recovery and subsequent
acceptances.


5     Results

5.1     Software verification

5.1.1    VeriSoftBench
Table 1 reports benchmark success, axiom compliance, independent-checker outcomes, and cost.
The results show that model capability and execution design both affect measured performance. The


                                                    4
Table 1. Results on the 100-task VeriSoftBench-Aristotle subset. Rules denotes benchmark-rule suc-
cess, Strict excludes disallowed kernel axioms, and Indep. reports independent-checker acceptances
over judged candidates. § Numina-Lean-Agent runs its released protocol, one sample with up to ten
rounds, rather than the target protocol used for the other systems, so its total is not a like-for-like
comparison. Target protocols are requested settings. Recorded budgets differ. Token counts are in
millions. Input totals include cached tokens, shown in parentheses. Output includes reasoning tokens
where reported. Dashes indicate unreported values. ‡ Published baselines [27, 28]. Appendix A
documents validation coverage.
                                                                                                                Input tokens  Output
System                                      Model           Effort Target protocol   Rules Strict Indep.                                           Cost
                                                                                                                (cached, M) tokens (M)
Aleph Prover‡                               –            –          Unknown            94       –          –                    –             –          –
Aristotle‡                                  –            –          Unknown            69       –          –                    –             –          –
VeriSoftBench‡                              Gemini-3-Pro –          Pass@8, r=3        65       –          –                    –             –          –
Claude Code           Opus 5                                xhigh   Pass@8, r=3       100     89        –   53.8 (50.1)                  2.09      $135
F ORALL -L EAN -AGENT Opus 5                                xhigh   Pass@8, r=3       100     96    69/69   45.3 (44.0)                  1.58      $111
Claude Code           Opus 5                                low     Pass@8, r=3        99     87    62/69   62.9 (58.7)                  1.18      $101
F ORALL -L EAN -AGENT Opus 5                                low     Pass@8, r=3       100     89        – 132.9 (129.4)                  0.95      $118
Claude Code           Fable 5                               low     Pass@8, r=3        96     89    60/66   58.0 (53.8)                  1.11      $157
F ORALL -L EAN -AGENT Fable 5                               low     Pass@8, r=3       100     89    62/70 178.3 (172.6)                  1.27      $350
Numina-Lean-Agent§                          Fable 5         low     1 sample, r≤10     86       –          – 899.3 (867.8)               5.15 $2,011
Codex                 GPT-5.6 Sol                           low     Pass@8, r=3        93     82     –           68.1 (61.7)             0.95       $69
F ORALL -L EAN -AGENT GPT-5.6 Sol                           low     Pass@8, r=3       100     88 63/69           80.7 (75.4)             0.54       $62
Codex                 GPT-5.6 Sol                           xhigh   Pass@8, r=3        97     86     –           63.4 (56.6)             0.95       $68
F ORALL -L EAN -AGENT GPT-5.6 Sol                           xhigh   Pass@8, r=3       100     88 60/67          104.5 (98.1)             1.00       $85
OpenCode              GPT-5.6 Sol                           low     Pass@8, r=3        67     61 42/45           41.9 (37.1)             0.54       $45
F ORALL -L EAN -AGENT GPT-5.6 Sol                           low     Pass@8, r=3        70     65     –           26.3 (22.3)             0.25       $33


                               unaided      with F ORALL -L EAN -AGENT                                     r1        r2    r3       r4   r5       exh.

                                    100              100           100        Claude Code + F ORALL
                       100
                                                                                        Opus 5, low
  tasks solved / 100




                                                              97              Claude Code + F ORALL
                               96                                                       Fable 5, low
                       95                                                          Codex + F ORALL
                                                93                                          Sol, low
                                                                                   Codex + F ORALL
                                                                                          Sol, xhigh
                       90                                                       OpenCode + F ORALL
                                                                                            Sol, low

                             Claude Code        Codex        Codex                                     0        20        40        60    80       100
                             Fable 5, low      Sol, low     Sol, xhigh                                                    % of tasks

(a) Matched frontend, model, and effort. Blue (b) Initial recorded outcomes before recovery and retries.
bars denote F ORALL -L EAN -AGENT paired with Exh. denotes exhaustion.
the named frontend.
Figure 2. Repository proof success under alternative execution protocols and the distribution of
review rounds.


comparisons below separate complete subset evaluations from partial studies and cumulative retry
results.
Performance without task-specific tools. Unaided agents solve 93 to 100 of the 100 subset tasks
under benchmark rules. Claude Code with Opus 5 solves 100 tasks at xhigh effort and 99 at low effort.
Codex solves 93 and 97 at the corresponding effort levels. The published Aleph Prover, Aristotle, and
custom in-house Gemini-3-Pro baselines report 94, 69, and 65 tasks, respectively [27, 28]. Detailed
access conditions for Aleph are unreported. The model, context, and budget differences preclude
attributing this gap solely to the framework. At high effort, the tool-assisted and unaided Opus 5
evaluations both approach the benchmark ceiling.
Effect of the agent harness. At fixed low effort, F ORALL -L EAN -AGENT + Claude Code improves
Fable 5 from 96 to 100 solved tasks, while F ORALL -L EAN -AGENT + Codex improves GPT-5.6 Sol


                                                                              5
from 93 to 100. The F ORALL -L EAN -AGENT + Claude Code configuration with Fable 5 solves all
four tasks missed by its unaided counterpart. With Opus 5 at low effort, F ORALL -L EAN -AGENT
improves the unaided configuration from 99 to 100 solved tasks and from 87 to 89 under the strict
axiom policy, recovering task 121 after eight unaided samples fail. This configuration reaches the
same counts as unaided Opus 5 at xhigh, 100 and 89, at a lower cost of $118 against $135, while the
larger strict gain observed at xhigh, 89 to 96, does not appear at low effort. F ORALL -L EAN -AGENT
+ Codex at xhigh reaches 100 tasks across the initial evaluation and subsequent retries. Appendix A
records validation coverage.
Several model and harness configurations reach the benchmark-rule ceiling on the 100-task subset,
limiting the ability of solve counts to distinguish performance. We did not evaluate the full 500-task
VeriSoftBench benchmark and therefore cannot assess whether this saturation extends to the complete
benchmark.
Variation across frontends. With GPT-5.6 Sol at low effort, F ORALL -L EAN -AGENT + OpenCode
solves 67 tasks without retrieval and 70 with the Lean tool integration, compared with 100 for
F ORALL -L EAN -AGENT + Codex. The F ORALL -L EAN -AGENT + OpenCode no-tool transcripts
contain 1,029 reads, 300 searches with grep, and 690 patches. The tool-integrated configuration
reduces cost from $44.84 to $33.17 and solves three additional tasks. Frontend behavior and tool
integration therefore affect performance under the same nominal model and effort setting.

5.1.2    Lean Eval
The Lean Eval software-verification tasks require connected formal developments with guards against
vacuous implementations. The calculus-of-constructions task contains six obligations covering
typing, reduction, subject reduction, strong normalization, and consistency. The real-closed-field task
requires a quantifier-elimination definition and three associated theorems. Both accepted candidates
pass the benchmark’s comparator and independent-kernel checks.
For each review, the framework copies the permitted solver files into a pristine benchmark workspace
and binds the review to a digest of the complete candidate. The normalization submission contains
233 files and approximately 28.6 thousand lines of Lean. Its development includes operator assistance
with checkpoints, infrastructure recovery, and strategic guidance. The final proof covers all six
obligations without a universe bound. It is consequently reported as an assisted development, without
a standardized single-attempt cost or time claim. The real-closed-field submission contains one file
and approximately 1.5 thousand lines. Its accepted implementation has no stated degree or depth
restriction.
The cases assess larger-artifact support without providing a controlled model comparison.

5.2     Mathematical verification

We evaluate F ORALL -L EAN -AGENT on PutnamBench using Opus 5 at xhigh effort. Table 3 reports
all 672 problems accepted. The resource analysis covers every accepted problem.
662 of 672 accepted candidates pass review in the first round, with the remaining 10 accepted in a
second review round. Compilation remains iterative, with a median of 7 invocations before accepted
submission and a maximum of 56. Mean actor and reviewer costs are $3.52 and $1.20, an average of
$4.72 per accepted problem and $3,169 in total.
Scope of inference. The reported result is a single run at one model and effort setting, not a pass
rate over repeated trials, so it does not estimate variance. Acceptance requires verifier success and
reviewer approval on one digest-bound artifact; it does not certify that a proof is idiomatic or minimal.


Table 2. Lean Eval software-verification developments completed with F ORALL -L EAN -AGENT and
GPT-6 Astra. The submissions pass native compilation, fresh review, comparator validation, and
independent-kernel checks.
        Problem                        Holes        Submission          Model        Verification
        coc_strong_normalization   6 thm         233 files / 28.6k lines GPT-6 Astra Benchmark validated
        rcf_quantifier_elimination 1 def + 3 thm 1 file / 1.5k lines     GPT-6 Astra Benchmark validated



                                                       6
Matched controls are needed to separate the contributions of retrieval, review, and continuation. The
evaluation also spans two billing accounts and one harness revision, neither of which changes the
model, effort setting, or acceptance rule.

5.3             Interpreting performance and efficiency

Closed-source comparisons. Published scores from closed-source systems provide useful reference
points, but direct comparison is difficult when model details, tool access, inference budgets, or cost
accounting are unavailable. Aggregate scores alone cannot establish whether a difference arises from
model capability or the surrounding agent harness. We therefore distinguish published leaderboard
results from matched comparisons within our evaluation.
Benchmark ceilings and saturation. At the subset ceiling, strict correctness and resource con-
sumption remain informative. For example, Opus 5 at xhigh solves 100 tasks with and without
F ORALL -L EAN -AGENT, while strict successes increase from 89 to 96 and total cost falls from $135
to $111.
Cost across execution protocols. With Fable 5 at low effort, Numina-Lean-Agent solves 86 tasks for
$2,011, compared with 100 for $350 using F ORALL -L EAN -AGENT and 96 for $157 unaided. Cost
per solved task is $23.38, $3.50, and $1.64, respectively. Numina uses one sample with up to ten
rounds and uncapped compilation. These protocol differences limit attribution of the observed cost
gap to stopping behavior or any individual harness component.
Model capability and harness efficiency. Strong performance without task-specific tools demon-
strates the contribution of the underlying model. The harness determines how that capability is used
through context selection, tool access, feedback, and review. Its efficiency gains depend on the


Table 3. Comparison on the Lean answer-given version of PutnamBench. Leaderboard totals [20] use
different benchmark versions, models, budgets, and statement revisions. Reported resource statistics
for F ORALL -L EAN -AGENT cover all 672 accepted problems.
               System                                      Reported resources                             Solved    Evaluation setting
               Aleph Prover [18]                           avg $74, max $1,468                               672 closed system
               NEAR AI, DeepSeek V4a                       mean $0.17                                        672 shell agent with retries
               Humanfiab                                   avg $44.5                                         672 GPT-5.6 Sol at xhigh effort
               Goedel-Architect [9]                        8 blueprints, 4 retries per node, avg             642
                                                           $5.8
               Seed-Prover 1.5 [8]                         10 H20-days                                       581
               Hilbert [26]                                avg Pass@1840                                     462 evaluated on 660 problems
               Minimal agent [21]                          avg $12.60, 50 iterations                         365 Claude Opus 4.5
               Ax-Prover [6]                               Pass@1, ≈100 tool calls                            91
               F ORALL -L EAN -AGENT                       avg $4.72                                         672    Opus 5, xhigh
a
  https://github.com/SkidanovAlex/putnambench-deepseek
b
  https://github.com/humanfia/putnambench



                80
                                                                                              150
                60
                                                                                   problems
    problems




                                                                                              100
                40

                20                                                                            50

                 0                                                                             0
                     1    10         20      30       40             56                             0          2       4        6        8       10+
                               compilations before acceptance                                           actor cost per accepted problem (USD bins)

(a) Compilations with median 7, mean 8.9, and maxi-                             (b) Actor cost with median $2.49, mean $3.52, and
mum 56 across 672 accepted problems.                                            maximum $34.01.
Figure 3. Resource use across all 672 accepted PutnamBench problems. 662 receive approval in the
first review round and 651 require no continuation request. Median wall time is 27 minutes and the
maximum is 211 minutes.


                                                                            7
Table 4. Observed threats to evaluation validity and the corresponding controls. Access violations
can inflate success counts, while artifact drift, scorer failures, and service interruptions can produce
incorrect negative outcomes.
Threat                                    Evidence                                Control
Permission bypass allowed access to       reference similarity of 0.99 to 1.00    operating-system restrictions across the pro-
the reference repository                  and transcript path evidence            cess tree
Unrestricted network access exposed       reference similarity of 1.00 and        provider-only network proxy with refusal logs
public reference material                 recorded curl access
Filesystem search located alternative     reference similarity of 1.00 and        pattern-based restrictions covering alternative
benchmark copies                          recorded search paths                   checkouts
Stored and submitted proofs differed in   serial verification of recovered        candidate digests and single-use sample direc-
5 of 97 cases                             submit-time artifacts                   tories
Scorer dependencies were unavailable      independent rescoring of an all-        pinned interpreter and toolchain with environ-
for five valid samples                    negative task                           ment checks
Authentication errors generated 229       error returns with zero inference ex-   interruption status and resumable tasks
false failure records                     penditure



configuration. With GPT-5.6 Sol at low effort, F ORALL -L EAN -AGENT increases benchmark-rule
successes from 93 to 100 while reducing cost from $69 to $62, corresponding to $0.62 per solved
task. With Fable 5, successes increase from 96 to 100, but cost rises from $157 to $350 and strict
successes remain at 89. The results support configuration-dependent gains in efficiency, rather than a
uniform reduction in inference cost.
Axiom audit and independent checking. The axiom audit inspects the assumptions on which a
compiled theorem depends. Strict success requires compliance with the permitted axiom policy
described in Section 3.6. Independent checking additionally validates the candidate against the
benchmark statement and replays its exported proof with a separate kernel implementation. The
Indep. column reports accepted candidates over those judged by this checker, not over all 100 tasks.
These checks assess different properties, and incomplete independent-checker coverage should not be
interpreted as either success or failure on the remaining tasks.

6    Evaluation integrity
The incidents in Table 4 identify three distinct obligations for an auditable evaluation. First, informa-
tion access must be enforced beyond the agent’s prompt. A settings-based deny list was ineffective
under permission-bypass execution, and restricting one checkout left other local copies and public
network sources accessible. Similarity screening and transcript inspection exposed these violations.
A valid runtime-blind result therefore requires both effective access controls and records showing
how the candidate was produced.
The network control is load-bearing rather than precautionary. Across the 100-task Numina-
Lean-Agent evaluation, whose audit records every connection attempt, 26 of 86 audited tasks
issue a total of 425 requests to public code-hosting endpoints during solving, including
github.com, codeload.github.com and raw.githubusercontent.com. All are refused, and
api.anthropic.com is the only host ever permitted. The benchmark repositories are themselves
public, so whether any request would have retrieved reference material is not established; the control
removes the need to answer that question.
Second, acceptance must identify an immutable artifact. Reused sample directories caused the
proof on disk to differ from the proof submitted during the evaluated session. Binding submission,
compilation, and review evidence to the same digest makes such discrepancies detectable. Older
results require recovery from the submit-time transcript or exclusion when the artifact cannot be
reconstructed.
Third, infrastructure failures must remain distinguishable from proof failures. This recurs. During
the Numina evaluation, a spend limit and an expired credential each produced batches of tasks that
exhausted their round budget without a single model call, recorded as failures whose stated cause
was an unproved declaration, which is the staged stub being graded. Sixteen such records were
identified by their zero token consumption and re-measured; all five of one batch then succeeded. A
harness that aborts on a turn that spent nothing, rather than recording it, prevents these from entering


                                                               8
a result table at all. Missing scorer dependencies, expired credentials, and parser defects produced
plausible negative records without corresponding unsuccessful reasoning. Separate status categories,
environment checks, and serial artifact validation reduce this ambiguity.

7   Limitations
The evaluation is descriptive, with no repeated configurations, confidence intervals, or component
ablations. The contributions of retrieval, review, and persistence remain unresolved. Limited
disclosure by closed-source baselines restricts comparisons of capability and efficiency. Results on
the 100-task subset do not establish performance on all 500 VeriSoftBench tasks.
The reviewer shares the actor’s model family, so context separation does not establish independent
errors. Approval supplements kernel evidence. Runtime restrictions and similarity audits cannot rule
out training-data exposure. Temporal holdouts and withheld solutions would strengthen contamination
studies. The unreleased harness limits external reproduction.

Broader impacts. Automated Lean proving can reduce verification effort, but proofs of inadequate
specifications can create unwarranted confidence in unsafe systems. Statement comparison, axiom
audits, and human specification review help mitigate this risk.

8   Conclusion
F ORALL -L EAN -AGENT links proof generation and fresh review to verified artifacts through a
frontend-agnostic acceptance protocol. The evaluation demonstrates strong performance on the 100-
task VeriSoftBench subset, accepts all 672 PutnamBench problems, and supports both independently
checked Lean Eval software-verification developments. These results demonstrate applicability across
formal mathematics and software verification and the value of reporting accepted artifacts alongside
verification policies, information boundaries, and resource budgets.

Acknowledgments and Disclosure of Funding
We thank Hung Pham, Todd Schmid, Jules Jacobs, and Wojciech Różowski for their advice and
guidance. We also thank George Tsoukalas and Jocelyn Qiaochu Chen for supporting our submissions
to PutnamBench and VeriSoftBench, respectively, and for helping verify and review the results. We
are grateful to the anonymous reviewers at NeurIPS VeriCodeGen for their thoughtful feedback.
This work received no external funding. The author declares no competing interests.

References
 [1] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathïs Fédérico, Sergei Gukov, Daniel
     Halpern-Leistner, Kirsten Henningsgard, Yury Kudryashov, Alexander Meiburg, Martin
     Michelsen, Riley Patterson, Eric Rodriguez, Laura Scharff, Vikram Shanker, Vladmir Sicca,
     Hari Sowrirajan, Aidan Swope, Matyas Tamas, Vlad Tenev, Jonathan Thomm, Harold Williams,
     and Lawrence Wu. Aristotle: IMO-level automated theorem proving. arXiv preprint
     arXiv:2510.01346, 2025. doi: 10.48550/arXiv.2510.01346.

 [2] ammkrn. nanoda: An independent type checker for Lean 4 export files. https://github.
     com/ammkrn/nanoda_lib, 2024.

 [3] Leni Aniva, Chuyue Sun, Brando Miranda, Clark Barrett, and Sanmi Koyejo. Pantograph:
     A machine-to-machine interaction interface for advanced theorem proving, high level rea-
     soning, and data extraction in Lean 4. In TACAS, 2025. doi: 10.48550/arXiv.2410.16429.
     arXiv:2410.16429.

 [4] Anthropic. Model Context Protocol. https://modelcontextprotocol.io, 2024.

 [5] Anthropic. Claude Code. https://docs.anthropic.com/en/docs/claude-code, 2026.


                                                 9
 [6] Benjamin Breen, Marco Del Tredici, Jacob McCarran, Javier Aspuru Mijares, Weichen Winston
     Yin, Kfir Sulimany, Jacob M. Taylor, Frank H. L. Koppens, and Dirk Englund. Ax-Prover: A
     deep reasoning agentic framework for theorem proving in mathematics and quantum physics.
     arXiv preprint arXiv:2510.12787, 2025. doi: 10.48550/arXiv.2510.12787.

 [7] Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian
     Chiosa, Jure Kukovec, Alok Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, Miranda
     Zhao, Max Tan, and Max Tegmark. A benchmark for vericoding: Formally verified program
     synthesis. arXiv preprint arXiv:2509.22908, 2025. doi: 10.48550/arXiv.2509.22908.

 [8] Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu, Zhicheng Jiang, Allan Jie, Xiaoran
     Jin, Xing Jin, Chenggang Li, Wenlei Shi, Zhihong Wang, Mingxuan Wang, Chenrui Wei,
     Shufa Wei, Huajian Xin, Fan Yang, Weihao Gao, Zheng Yuan, Tianyang Zhan, Zeyu Zheng,
     Tianxi Zhou, and Thomas Hanwen Zhu. Seed-Prover 1.5: Mastering undergraduate-level
     theorem proving via learning from experience. arXiv preprint arXiv:2512.17260, 2025. doi:
     10.48550/arXiv.2512.17260.

 [9] Jui-Hui Chung, Ziyang Cai, Zihao Li, Qishuo Yin, Rohit Agarwal, Simon Park, Rodrigo Porto,
     Narutatsu Ri, Ziran Yang, Shange Tang, Xingyu Dang, Hongzhou Lin, Mengdi Wang, Danqi
     Chen, Chi Jin, Liam H Fowl, and Sanjeev Arora. Goedel-Architect: Streamlining formal
     theorem proving with blueprint generation and refinement. arXiv preprint arXiv:2606.06468,
     2026. doi: 10.48550/arXiv.2606.06468.

[10] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In CADE, 2021.

[11] Jiewen Hu, Thomas Zhu, and Sean Welleck. miniCTX: Neural theorem proving with (long-
     )contexts. In ICLR, 2025. doi: 10.48550/arXiv.2408.03350. arXiv:2408.03350.

[12] Shuangxiang Kan, Shuanglong Kan, and Sebastian Ertel. Harnessing code agents for automatic
     software verification. arXiv preprint arXiv:2607.06341, 2026. doi: 10.48550/arXiv.2607.06341.

[13] Lean FRO. Comparator: Trustworthy verification of Lean solutions against trusted challenge
     statements. https://github.com/leanprover/comparator, 2026.

[14] Lean FRO. Lean Eval: A comparator-based Lean benchmark and leaderboard. https://
     lean-lang.org/eval/ and https://github.com/leanprover/lean-eval, 2026.

[15] Zenan Li, Ziran Yang, Deyuan He, Haoyu Zhao, Andrew Zhao, Shange Tang, Kaiyu Yang,
     Aarti Gupta, Zhendong Su, and Chi Jin. Goedel-Code-Prover: Hierarchical proof search
     for open state-of-the-art code verification. arXiv preprint arXiv:2603.19329, 2026. doi:
     10.48550/arXiv.2603.19329.

[16] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang,
     Yihan Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu
     Yang, Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover-V2:
     Scaling formal theorem proving with scaffolded data synthesis and self-correction. arXiv
     preprint arXiv:2508.03613, 2025. doi: 10.48550/arXiv.2508.03613.

[17] Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang,
     Yunzhou Xie, Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li, and Wenda Li. Numina-Lean-
     Agent: An open and general agentic reasoning system for formal mathematics. arXiv preprint
     arXiv:2601.14027, 2026. doi: 10.48550/arXiv.2601.14027.

[18] Logical Intelligence. Aleph Prover reaches state-of-the-art across the leading formal reasoning
     benchmarks. https://logicalintelligence.com/aleph-prover-final.html, 2026.

[19] OpenAI. Codex. https://github.com/openai/codex, 2026.

[20] PutnamBench Contributors. PutnamBench leaderboard. https://trishullab.github.io/
     PutnamBench/leaderboard.html, 2026. Results metadata accessed 9 September 2026.


                                                10
[21] Borja Requena, Austin Letson, Krystian Nowakowski, Izan Beltran-Ferreiro, and Leopoldo
     Sarra. A minimal agent for automated theorem proving. In International Conference on Machine
     Learning (ICML), 2026. doi: 10.48550/arXiv.2602.24273. arXiv:2602.24273.
[22] Alessandro Sosso, Akhil Arora, and Bas Spitters. Agentic proving for program verification.
     arXiv preprint arXiv:2605.23772, 2026. doi: 10.48550/arXiv.2605.23772.
[23] SST. OpenCode: An open-source coding agent. https://github.com/sst/opencode,
     2026.
[24] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An
     in-context learning agent for formal theorem-proving. In COLM, 2024. doi: 10.48550/arXiv.
     2310.04353. arXiv:2310.04353.
[25] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating neural theorem-provers
     on the Putnam mathematical competition. In NeurIPS Datasets and Benchmarks Track, 2024.
     doi: 10.48550/arXiv.2407.11214. arXiv:2407.11214.
[26] Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert:
     Recursively building formal proofs with informal reasoning. arXiv preprint arXiv:2509.22819,
     2025. doi: 10.48550/arXiv.2509.22819.
[27] VeriSoftBench Contributors.           VeriSoftBench leaderboard. https://raw.
     githubusercontent.com/utopia-group/VeriSoftBench/main/docs/results.json,
     2026. Results metadata accessed 9 September 2026.
[28] Yutong Xin, Qiaochu Chen, Greg Durrett, and Işil Dillig. VeriSoftBench: Repository-scale
     formal verification benchmarks for Lean. arXiv preprint arXiv:2602.18307, 2026. doi: 10.
     48550/arXiv.2602.18307.
[29] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
     Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented
     language models. In NeurIPS Datasets and Benchmarks Track, 2023.




                                               11
A    Repository results and independent validation

Table 5. Repository-level results. Codex Sol low includes the final acceptance on clean. Codex Sol
xhigh shows the initial 97-task total before fresh retries, with its cumulative result in Table 1. VCV
denotes VCV-io, FR denotes lean-formal-reasoning-program, Ark denotes ArkLib, juvix denotes
juvix-lean, Leroy denotes the compiler course, Expr denotes LeanExprEvaluator, iris denotes iris-lean,
and pcf denotes pcf-lean.
        System and configuration              clean VCV FR Ark loom juvix veil Leroy Expr iris pcf Total
        Tasks                                    47   17 7   5    5     5   5      4    3    1   1 100
        Claude Code
                                                43   17   7    5    5    5    5     4    3   1   1    96
        Fable 5 low, unaided
        Claude Code
                                                46   17   7    5    5    5    5     4    3   1   1    99
        Opus 5 low, unaided
        F ORALL -L EAN -AGENT + Claude Code
                                                47   17   7    5    5    5    5     4    3   1   1   100
        Fable 5 low
        F ORALL -L EAN -AGENT + Claude Code
                                                47   17   7    5    5    5    5     4    3   1   1   100
        Opus 5 low
        F ORALL -L EAN -AGENT + Codex
                                                47   17   7    5    5    5    5     4    3   1   1   100
        Sol low
        F ORALL -L EAN -AGENT + Codex
                                                46   15   7    5    5    5    5     4    3   1   1    97
        Sol xhigh
        F ORALL -L EAN -AGENT + OpenCode
                                                28   14   3    4    4    5    5     2    0   1   1    67
        Sol low, no tools
        Numina-Lean-Agent + Claude Code
                                                45   10   5    4    3    5    5     4    3   1   1    86
        Fable 5 low


Execution budgets. Model identifiers are claude-opus-5, claude-fable-5, gpt-5.6-sol, and
gpt-6-astra. A sample starts a fresh actor session. A reviewer round uses a persistent actor and
fresh review after verifier success. A continuation resumes the actor, while a fresh retry starts a
new session. Unaided Claude Code and Codex use up to eight samples with three local compiler
invocations per sample. The Opus-xhigh MCP evaluation uses one sample with uncapped compilation.
Reviewed Claude Code configurations allow up to five rounds with uncapped compilation. Reviewed
Codex and OpenCode configurations allow up to three rounds and three local actor compilations per
task. Numina allows one sample with up to ten rounds and uncapped compilation. Figure 2b shows
initial recorded statuses, while Table 1 includes subsequent recovery and retries. These recorded
budgets do not establish that every historical timeout or continuation override is recoverable.
Kernel dependencies. The audit re-elaborates each accepted target with #print axioms. Twelve
subset tasks can inherit disallowed axioms from repository lemmas. Tasks 128, 129, 145, 149, 152,
and 153 depend on Lean.ofReduceBool or Lean.trustCompiler. Tasks 266, 268, 272, 275, 454,
and 457 can inherit sorryAx from admitted dependencies. Reference proofs show the corresponding
dependencies. Some generated proofs avoid these lemmas, so the strict count varies by configuration.
No additional agent-introduced axiom was identified in the audited candidates. Unavailable audits
remain unreported rather than being assigned a clean result.
Independent-checker procedure. The checker evaluates candidates from 72 tasks in repositories
pinned to Lean v4.24.0 or v4.24.0-rc1. These repositories are clean, veil, LeanExprEvaluator,
and VCV-io. It builds a trusted Challenge containing the target statement and a separate Solution
containing the candidate under landrun. Both environments are exported with lean4export. The
comparison requires declarations referenced by the statement to agree, inspects exported axiom de-
pendencies, and checks the solution through Lean and nanoda. The implementation uses comparator
revision 71b52ec with two compatibility patches for Lean versions earlier than v4.27.
Only solved candidates that the checker can judge enter the independent-checker denominator. One
or two candidates per configuration are excluded when module-dependent generated names prevent
comparison of otherwise matching contexts. Seven Numina candidates from the earlier 49-task
evaluation additionally require repository helpers absent from the per-task environment. Among
judged cases, no candidate is rejected on a task whose reference proof passes the same checker. The
observed rejections concern inherited repository axioms. This finding is conditional on checker
coverage and does not certify the unjudged candidates.
Supplementary probes and retries. The Opus-5-low reviewed configuration is measured over all
100 tasks. Every task is accepted, 71 in the first review round and the remainder within four, at
a total billed cost of $118.41. Its axiom audit reports 89 clean targets and 11 carrying forbidden


                                                          12
axioms, all of which the corresponding reference proofs also carry, so no axiom is agent-introduced.
F ORALL -L EAN -AGENT + Codex at xhigh effort initially accepts 96 of the 99 tasks available under
their original dependency pins. Recovered task 222 adds one acceptance, and fresh retries of tasks
140, 452, and 462 complete the cumulative set. The $85 total includes these continuations. Its
independent-checker result in Table 1 covers the original 96 accepted tasks, so its denominator differs
from the cumulative benchmark score.

Existing assets. The retained VeriSoftBench distribution uses the MIT License, and the Lean
portion of PutnamBench uses Apache License 2.0. These benchmark licenses do not replace the
licenses of their dependencies or the terms governing hosted model access. The submission does not
redistribute the benchmark repositories or model weights.
Reference similarity. Raw-text sequence similarity is computed between each accepted candidate
and its withheld reference proof. Ratios of 0.99 to 1.00 identify the confirmed access violations
discussed in Section 6. Other high-similarity cases include short proofs and conventional induction
patterns. Transcript inspection and reproduction by another model help assess these cases, but neither
establishes absence of training-data exposure. The audit is therefore used to prioritize investigation
rather than to assign an unconditional independence guarantee.

B    PutnamBench coverage and validation

Table 6. Year-ordered PutnamBench coverage. The evaluation records and accepts all 672 problems.
                Year         62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77
                In benchmark 11 9 12 12 12 12 11 11 10 10 11 9 10 11 9 10
                Accepted     11 9 12 12 12 12 11 11 10 10 11 9 10 11 9 10
                Year         78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93
                In benchmark 11 10 10 8 9 9 8 10 12 11 12 9 10 10 11 11
                Accepted     11 10 10 8 9 9 8 10 12 11 12 9 10 10 11 11
                Year         94 95 96 97 98 99 00 01 02 03 04 05 06 07 08 09
                In benchmark 11 10 10 9 10 11 10 9 8 12 10 11 10 11 11 11
                Accepted     11 10 10 9 10 11 10 9 8 12 10 11 10 11 11 11
                Year         10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
                In benchmark 12 12 11 10 11 12 11 9 12 11 9 10 12 12 11 12
                Accepted     12 12 11 10 11 12 11 9 12 11 9 10 12 12 11 12


Model and verification. The PutnamBench evaluation uses Opus 5 at xhigh effort with the answer-
given statement and Mathlib context. Acceptance requires verification and fresh review of the same
candidate. The diagnostics below cover all accepted problems in the completed evaluation.
Resource distributions. Across the 672 accepted problems, compilation count has median 7, mean
8.9, and maximum 56. Actor expenditure has median $2.49, mean $3.52, maximum $34.01, and
rounded total $2,364. Reviewer expenditure averages $1.20 and totals approximately $805, giving an
average of $4.72 per accepted problem and $3,169 overall. Wall time has median 27 minutes, 90th
percentile 68 minutes, and maximum 211 minutes. Actor turns have median 31 and maximum 169.
Acceptance required a second review round in 10 cases and a continuation request in 21.
Verifier validation. A fifteen-case test set covers permitted proofs and attempts to bypass the
verification policy. The cases include admissions, declared axioms, native evaluation, extra imports,
altered statements or answer values, and several forms of name shadowing. Positive controls include
comments containing sorry, statement reformatting, and harmless helper declarations. The tests
exposed an incorrect rejection of template-defined answer abbreviations and a missed notation-based
redefinition. After these cases were addressed, a round-trip check of 1,018 staged candidates recorded
no false rejection. This is an empirical check over the retained candidates, not a completeness
guarantee for the verifier.
Toolchain migration. The evaluation ran on Lean v4.27.0. After the benchmark moved to Lean
v4.33.1 on 22 September 2026, all 672 accepted proofs were re-verified against it. 502 compiled
unchanged. The other 170 failed only through changed tactic behavior, such as simp normal forms,
ring_nf, and instance synthesis. An agent restricted to proof bodies repaired all 170 for a total of


                                                  13
$89.90. Each repaired file was re-checked for compilation, permitted axioms, and an unchanged
statement and answer term. Resource figures above describe the original evaluation and exclude these
repairs.

C     Harness prompt templates
The following templates reproduce the task instructions supplied by the retained harness implemen-
tations. Line wrapping, dash typography, and one incidental remark are edited for presentation.
Placeholders denote the task identifier, problem name, candidate digest, or reviewer report inserted at
runtime. Task files and tool responses provide the formal statement, repository context, and compiler
diagnostics separately. These templates do not include frontend system instructions or task-specific
continuation overrides.
Table 1 reports the target protocol, token consumption, and cost of the repository evaluations.
Appendix B reports the mathematical evaluation’s resource distributions. The prompts below comple-
ment this accounting with the instructions used for proof generation, fresh review, and revision.

C.1    VeriSoftBench

The actor can initialize the task, inspect and edit its candidate, compile, and submit through the
benchmark tools. The reviewer receives read-only inspection and reviewer-specific compilation tools.
The task identifier replaces <task-id>.

    Actor

    # Solve VeriSoftBench task <task-id> as the actor

    Call ‘vsb_start‘ with task id ‘<task-id>‘. It returns the exact theorem statement and
    prepares the proof-elided ‘./tree/‘.

    If ‘./REVIEW.md‘ exists, read it before doing further proof work. It was written
    by a fresh, independent, read-only reviewer. Treat its findings as hypotheses:
    check them against Lean and address every valid blocking issue.

    Read and search ‘./tree/‘, and maintain the candidate proof body in
    ‘./proof.lean‘. The proof must begin with ‘:= by‘; never restate or weaken the
    theorem. Use ‘vsb_compile‘ for deterministic feedback. Call ‘vsb_submit‘ only
    when the candidate compiles and you believe it is complete.

    The outer runner may resume this same actor session after another independent
    review. Keep useful reasoning and failed approaches in your session, while the
    workspace carries the current candidate between rounds.

    Nothing outside this directory and no network access are permitted. Do not try
    to alter ‘REVIEW.md‘, transcripts, audit files, metadata, or result files.



    Fresh reviewer

    # Independently review VeriSoftBench task <task-id>

    You are a fresh critic. You have no solver conversation and must form your own
    judgment from the formal task and current artifact.

    1. Call ‘vsb_review_start‘ with task id ‘<task-id>‘ to obtain the exact theorem
    statement
       without changing solver state.
    2. Read ‘./proof.lean‘ and any relevant definitions or theorem statements in
       the proof-elided ‘./tree/‘.
    3. Call ‘vsb_review_compile‘ exactly once after inspection. Compiler success is
       required for approval and records evidence bound to the candidate’s hash.
    4. Check that the proof addresses the exact statement, closes every goal, and



                                                  14
  Fresh reviewer (continued)

     does not rely on a forbidden escape, hidden admission, statement mutation,
     or irrelevant generated declaration.
  5. Do not edit any file and do not call actor compile/start or submission tools.

  Return exactly one verdict line followed by concise evidence and, on rejection,
  specific next steps. Also return exactly one digest line copied from the
  successful ‘vsb_review_compile‘ result:

  ‘REVIEW_VERDICT: APPROVE‘

  or

  ‘REVIEW_VERDICT: REJECT‘

  ‘REVIEW_PROOF_SHA256: <64 lowercase hexadecimal characters>‘

  Be skeptical but evidence-driven. Never approve a candidate that did not pass
  ‘vsb_compile‘. Do not reject a kernel-checked proof merely for style.



  Actor continuation

  A fresh independent reviewer has assessed the current candidate. Read ./REVIEW.md,
  verify every finding yourself, improve ./proof.lean, compile it, and submit only when
  complete.



C.2     PutnamBench in the answer-given configuration

The actor receives the frozen theorem and its answer value through pb_start. The reviewer reads
the same task and the candidate through its own tools. The quoted instructions encourage persistence.
Their statements about unlimited resources do not replace the external stopping conditions enforced
by the runner, as described in Section 3.5.

  Actor

  Prove the theorem in ‘<problem-name>.lean‘, in this directory.

  Use the Forall tools, not the shell, for this task:

       * ‘pb_start("<problem-name>")‘ - begin, and see the task. Call it first.
       * ‘pb_compile()‘        - elaborate your file. UNLIMITED: there is no budget
                                 and no penalty. Compile after every single step.
       * ‘pb_submit()‘         - score the file with the five-layer verifier.
       * ‘forall_lean‘ search / lookup / usages - retrieval over Mathlib. Prefer it
                                 to grepping the source by hand.

  ‘pb_submit‘ IS THE ONLY THING THAT ENDS THIS TASK. Nothing else counts as
  finishing - not a clean ‘pb_compile‘, and not your own judgement that the proof
  is done. Submitting is free and unlimited: a failure returns the verifier’s
  exact words and costs you nothing.

  So: WHENEVER YOU BELIEVE THE PROOF IS COMPLETE, CALL ‘pb_submit()‘. If you
  submitted earlier while the proof was still unfinished, that submission is dead
  - you must call ‘pb_submit()‘ again now that it is finished. Never end a turn
  having compiled cleanly without submitting.

  WHAT COUNTS AS DONE. Not your judgement -- the verifier’s, via ‘pb_submit‘.
  It checks all of:

       * no ‘sorry‘, ‘admit‘, ‘native_decide‘, ‘@[implemented_by]‘, ‘@[extern]‘, and




                                                 15
Actor (continued)

    no ‘axiom‘ declaration anywhere in the file;
  * no import other than ‘import Mathlib‘;
  * the theorem statement is character-for-character the one you were given
    (whitespace and comments aside), and so is the answer value in the ‘abbrev‘ above
    it -- it was given to you,
and changing it is tampering, not solving;
  * no declaration of yours shadows a name the statement resolves through --
    defining your own ‘IsGreatest‘ beside a statement that uses Mathlib’s is a
    rejection, not a proof;
  * the file elaborates with no errors;
  * ‘#print axioms‘ for the theorem shows nothing beyond ‘propext‘,
    ‘Classical.choice‘ and ‘Quot.sound‘.

You will see the verifier’s exact output when it refuses, so work from what it
says rather than guessing.

HOW LONG YOU HAVE. There is no turn limit and no token budget. Compile as often
as you want -- there is no per-compile cost to you and no penalty for a failed
attempt. Long proofs are expected: budget for hundreds of turns on a hard
problem, and do not try to land it in one shot.

HOW TO WORK. Write a short proof sketch first, in natural language, and only
then formalise it. Turn each step of the sketch into a ‘have ... := by sorry‘
and discharge them one at a time, compiling after each, so you always know
which step is the one that is failing. Search Mathlib for the lemma you need
rather than reproving it. If you come to believe the statement is false, say so
explicitly and try to derive ‘False‘ from its hypotheses -- that is a real
finding.



Fresh reviewer

You are an independent reviewer. You did not write this proof and you cannot
edit it. You have not seen the author’s reasoning - only the statement it must
prove and the file it produced.

Call ‘pb_review_start("<problem-name>")‘ to see both, and ‘pb_review_compile()‘ to
elaborate the candidate yourself. Do not take the author’s word, or a previous
verifier PASS, for anything you can check.

Your job is to find the ways this could be wrong while still compiling:

  * Does it prove the FROZEN statement, or a weaker one? Compare the statement
    in the file against the frozen one character by character.
  * Does any declaration in the file shadow a name the statement resolves
    through? A local ‘def IsGreatest‘ beside a statement using Mathlib’s
    ‘IsGreatest‘ guts the problem while compiling cleanly.
  * Where an answer value was given, is it unchanged?
  * Does anything reach past the kernel - an axiom, ‘native_decide‘, a
    ‘@[implemented_by]‘, an extra import?
  * Are there vacuous or circular steps: a hypothesis that is never used
    because it was silently weakened, a ‘have‘ that restates the goal?

Then end your reply with exactly one line:

    VERDICT: APPROVE

if the proof is correct and complete, or

    VERDICT: REJECT

if it is not - and above that line say precisely what is wrong, specifically
enough that the author can fix it. Approving a broken proof is the worst




                                             16
  Fresh reviewer (continued)

  outcome available to you; rejecting a sound one merely costs a round.



  Actor continuation after an unaccepted turn

  You are not finished, so do not stop.

  A run ends in exactly one way: ‘pb_submit()‘ returns PASS. That has not
  happened yet. If your proof already compiles cleanly, CALL ‘pb_submit()‘
  NOW -- a clean compile is not finishing, and an earlier submission made
  while the proof was unfinished does not count.

  You have NO turn limit and NO time limit. Nothing is running out, no budget is
  being spent that you need to protect, and nobody is waiting on you. Another
  hundred turns costs nothing and is entirely fine.

  None of your work is lost -- everything you have established is still there in
  front of you. Pick it up from where you left off. If the last thing you tried
  did not work, try a different angle: a different decomposition of the goal,
  different Mathlib lemmas, a smaller intermediate lemma proved on its own, or a
  concrete small case worked by hand to sharpen the idea. If you have started to
  suspect the statement is false, chase that instead: build a counterexample and
  try to derive ‘False‘ from the hypotheses.


  Continue now, with a tool call.



  Actor continuation after reviewer rejection

  An independent reviewer examined your proof and did NOT approve it. Its full report
  follows. Treat it as the thing to fix; it has not seen your reasoning, only the
  statement and the candidate.

  <reviewer-report>

  Revise the proof and call pb_submit again. There is no turn limit.



C.3   Lean Eval

The default prompts refer to the challenge and solver-owned submission files. The reviewer receives
the digest of the submission files as <candidate-sha256>. External comparison and independent
kernel checking remain controlled by the runner. These are the base templates, with task-specific
recovery instructions supplied separately when needed.

  Actor

  You are the proof actor for the LeanEval problem <problem-name>. Read README.md,
  Challenge.lean, ChallengeDeps/, config.json, and the starter Submission.lean. Complete
  every required declaration using only the challenge, its local dependencies, published
  mathematical knowledge you already have, and Lean compiler feedback. Work only in this
  workspace. Edit only Submission.lean and Lean files under Submission/. Do not modify
  trusted files or build configuration. Do not use the network and do not search for
  existing benchmark solutions. Use lake build Submission repeatedly and leave your
  strongest complete candidate on disk. This is a persistent actor session; an
  independent fresh reviewer will assess the candidate after this round.




                                                17
Fresh reviewer

You are a fresh independent reviewer of a LeanEval candidate and have no actor
transcript. Inspect README.md, Challenge.lean, ChallengeDeps/, config.json,
Submission.lean, and Submission/**/*.lean. Independently run lake build Submission.
Check that every hole is genuinely solved, that the candidate does not rely on sorry
or unsafe shortcuts, and that it respects solver-owned file boundaries. Do not edit
any file. Do not use the network or search for existing solutions. End with exactly
two standalone lines: REVIEW_VERDICT: APPROVE or REVIEW_VERDICT: REJECT, and
REVIEW_CANDIDATE_SHA256: <candidate-sha256>



Actor continuation

A fresh independent reviewer or the external verifier rejected the current candidate.
Read REVIEW.md, verify the feedback yourself, and continue solving every required
declaration. Work only in this workspace. You may edit only Submission.lean and Lean
files under Submission/. Use lake build Submission to check your work. Do not use the
network or search for existing benchmark solutions. Leave your strongest complete
candidate on disk.




                                          18
