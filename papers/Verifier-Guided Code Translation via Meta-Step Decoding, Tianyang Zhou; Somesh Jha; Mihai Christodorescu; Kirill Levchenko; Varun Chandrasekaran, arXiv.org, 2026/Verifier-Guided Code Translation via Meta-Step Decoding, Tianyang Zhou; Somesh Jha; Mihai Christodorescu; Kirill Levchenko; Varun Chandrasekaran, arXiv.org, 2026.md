                                               Verifier-Guided Code Translation via Meta-Step
                                                                 Decoding


                                                         Tianyang Zhou                                        Somesh Jha
                                             University of Illinois Urbana-Champaign          University of Wisconsin–Madison and Google
                                                      tz64@illinois.edu                                    jha@cs.wisc.edu
arXiv:2605.17626v1 [cs.LG] 17 May 2026




                                                         Mihai Christodorescu                            Kirill Levchenko
                                                                Google                        University of Illinois Urbana-Champaign
                                                     christodorescu@google.com                      klevchen@illinois.edu

                                                                                Varun Chandrasekaran
                                                                         University of Illinois Urbana-Champaign
                                                                                varunc@illinois.edu



                                                                                        Abstract

                                                     Test-time scaling is an important mechanism for improving large language models,
                                                     especially on tasks with deterministic verifiers. Code translation is a canonical
                                                     example: the source program constrains valid outputs, while compilers, type check-
                                                     ers, and behavioral checks provide exact pass/fail feedback. Existing approaches
                                                     typically apply these verifiers only after generation, which is inefficient because
                                                     early errors corrupt the autoregressive context and are rarely corrected later. We
                                                     introduce Decoding Time Verification (DTV), a framework that treats structural
                                                     boundaries as meta steps for verifier-guided decoding. DTV interleaves generation
                                                     with verifier calls under a state-machine controller that enforces valid prefixes,
                                                     using structural-boundary checks and structure-aware rollback to prevent error
                                                     propagation while reducing wasted tokens. We evaluate DTV on C-to-Rust and
                                                     JavaScript-to-TypeScript translation. Using Qwen3-4B as the primary generator
                                                     under matched token budgets, DTV improves pass rates from 72.3% to 82.0%
                                                     on C-to-Rust and from 33.3% to 46.0% on JavaScript-to-TypeScript relative to
                                                     matched self-refinement baselines, while using fewer tokens per case; the same
                                                     trend largely transfers to Gemma-4-E4B. In the evaluated cost-matched grid, DTV
                                                     achieves a more favorable pass-rate-cost tradeoff than post-hoc verification or
                                                     sampling-based scaling. These results show that verifier-guided decoding is an
                                                     effective use of inference-time compute for code translation.


                                         1    Introduction
                                         Large language models (LLMs) have become capable general-purpose code generators, but improving
                                         performance on difficult inputs is increasingly pursued at inference time rather than solely through
                                         larger pretraining runs. A growing line of work studies test-time scaling: allocating additional
                                         inference compute through repeated sampling, search, self-refinement, or process-level guidance to
                                         improve the performance of a frozen pretrained model [1–6].
                                         Most existing test-time scaling methods are designed for open-ended domains where correctness is
                                         difficult to verify exactly. Consequently, they guide generation using probabilistic signals derived
                                         from the model itself or learned scorers [7, 8], such as token likelihoods, preference models, or

                                         Preprint.
                     GENERATION                                         VERIFICATION                                          RECOVERY
                                                        at
                        GENERATE                     boundary                 VERIFY                     fail                  FEEDBACK
              Extend prefix to structural boundary               Render prefix, run applicable oracles               Augment generation with diagnostics
              Scope: stmt, block, func, or program                 Oracles run on rendered artifact                   Inline append or patch-based retry

                                                                                      pass
                                                                             COMMIT                                            ROLLBACK
                                                                 Checkpoint prefix as rollback target                Restore checkpoint, augment context
                                                                  Triggered when all oracles pass                     Escalate scope on repeated failure


                                                                 Finish program
                                                                           TERMINATE
                                                                        End decoding loop
                                                                                                           bailout
                                        with augmented context    Success (g = program) or bailout




Figure 1: GENERATION extends the target prefix to the next structural boundary (statement, block, function,
or program). VERIFICATION renders the prefix and runs applicable oracles, committing on pass. RECOVERY
parses diagnostics on fail, rolls back to the last checkpoint with augmented context, and escalates scope on
repeated failure. The loop terminates on program-level success or budget bailout.
intermediate reasoning heuristics. While these signals can improve reasoning quality in open-
ended settings, coding tasks impose discrete semantic and syntactic correctness constraints, making
probabilistic guidance only weakly aligned with true success: models may assign high probability to
plausible-looking yet incorrect programs, while learned reward models for code are expensive to train
and brittle across languages and libraries [9, 10]. At the same time, coding tasks expose deterministic
external verifiers unavailable in most domains. Compilers, type checkers, and behavioral tests provide
exact pass/fail feedback together with structured diagnostics, creating an opportunity for stronger
inference-time guidance. Existing approaches, however, typically use these signals only post-hoc to
filter, rerank, or repair completed samples [11–13]. This cannot influence the trajectory of generation
itself: once a verifier-detectable error enters the autoregressive prefix, later decoding proceeds under
a corrupted conditioning context, and models tend to continue the trajectory rather than recover [14].
One possible approach to overcome this limitation is to let verifier signals participate directly in the
autoregressive loop, governing which prefixes are admitted as conditioning context rather than only
which completed samples are retained. Doing so raises three coupled questions: when to invoke a
verifier, since verifiers require structurally complete artifacts rather than arbitrary token prefixes; how
to roll back when verification fails, balancing context preservation against error excision; and what to
do with diagnostics beyond retry with the same context.
We introduce Decoding Time Verification (DTV), a decoding framework that interleaves generation
from a pretrained code model with deterministic verifier calls under an explicit state-machine
controller1 . As illustrated in Figure 1, DTV generates target code up to the next structural boundary
(e.g., statement, block, or function), renders the current prefix into a verifier-consumable artifact, and
runs the applicable verifiers. If all checks pass, the prefix is committed; else, the controller rolls back
to an earlier checkpoint, updates a feedback state using verifier diagnostics, and retries generation.
Unlike prior in-loop verification systems that fix a particular combination of scope, verifier type, and
search mechanism [15–17], DTV separates the controller, verification scopes, and verifier suite as
configurable components. It combines three key mechanisms. First, structural-boundary verification
enforces a legal prefix invariant: only prefixes satisfying all applicable verifiers are admitted as
conditioning context for subsequent decoding. Second, structure-aware rollback with escalation
rolls back to the smallest scope implicated by the verifier diagnostic, escalating to larger scopes on
repeated failures rather than retrying more. Third, feedback via prompt augmentation summarizes
verifier diagnostics and injects them back into the model context so retries proceed under updated
information rather than blind resampling. Together, these mechanisms prevent verifier-detectable
errors from propagating through the autoregressive context by ensuring generation continues only
from committed verified prefixes. While we instantiate DTV on code translation, the framework
applies to any task with deterministic process-level verifiers and a structural renderer in principle,
such as code generation tasks or even open-ended generation with external knowledge validators.
We evaluate DTV on two translation settings with complementary verifier structures. C-to-Rust
combines compiler checks with differential testing against the output in the end, while JavaScript-to-
TypeScript relies on static type and lint verification for the type annotation task. Using Qwen3-4B [18]
as the primary generator under matched generation budgets, DTV with self-refinement improves
compile-pass rate from 72.3% to 82.0% on C-to-Rust and from 33.3% to 46.0% on JavaScript-to-
TypeScript, while using fewer tokens overall (§ 4.1); the same gains transfer to Gemma-4-E4B [19]
   1 Source code is available at: https://github.com/qsdrqs/dtv-translation




                                                                                  2
(Appendix K). These gains are not solely due to outer-loop scaling: even without outer-loop retry,
in-loop verification alone improves one-shot pass rate by +30.7 pp and +16.7 pp over direct decoding,
showing that DTV introduces a distinct scaling mechanism. In the cost-matched grid, DTV also
achieves a more favorable pass-rate-cost point than other test-time scaling methods, including best-
of-N and the compile-feedback-based S* baseline [20]. Ablations show that all three key design
components of DTV contribute, with in-loop recovery providing the largest benefit (§ 4.2).

2     Decoding Time Verification
As discussed in § 1, post-hoc verification applies verifier feedback only after generation is complete,
surfacing errors too late to guide decoding. We instead verify during decoding using deterministic
program verifiers (e.g., compilers, type checkers, and tests) as oracles. Verifier calls are aligned with
structural boundaries such as completed statements, blocks, or functions, where verdicts become
meaningful and rollback can target the scope at which an error was introduced. This forms an inner
loop of generation that complements traditional outer-loop strategies (e.g., self-refinement with
verifier feedback) operating only on completed programs. Outer-loop verification is recovered as a
special case by invoking oracles only at full-program scope.

2.1   Overview

Decoding Time Verification (DTV) instantiates this idea as a deterministic state-machine controller.
At each structural boundary, the controller selects from a fixed action set: G ENERATE (extend the
token prefix), V ERIFY (render the prefix and run oracles), C OMMIT (checkpoint the current prefix),
ROLLBACK (restore an earlier checkpoint), F EEDBACK (construct a retry prompt from diagnostics),
and T ERMINATE (end decoding); Figure 1 shows the overall control flow. While the framework is
task-agnostic, we focus on code translation throughout the paper because it admits an abundance of
deterministic oracles.
Translation setting. Code translation aims for the generated program to exhibit the same observable
behavior as the source. Given a source program S, a translation model M generates a target token
sequence Y = (y1 , . . . , ym ). At each step i, M defines a conditional distribution pM (yi | y<i , S),
where Y<i = (y1 , . . . , yi−1 ) is the prefix and Y≤i is its length-i extension. We treat M as a fixed
pretrained black-box generator and assume access to a suite of deterministic oracles whose verdicts
capture correctness of the translation result.
Key abstractions. We now formalize the three abstractions needed to state our algorithm:
1. Scope. Let G be a finite totally ordered set of scopes ordered by granularity, with G =
{stmt, block, func, program} in our instantiations and stmt ⪯ block ⪯ func ⪯ program
denoting nested enclosure (a statement inside a block, a block inside a function, and so on). Each
scope g ∈ G also marks a class of structural boundaries: positions in the target token sequence
at which an instance of g ends (e.g., a function’s closing brace, a statement’s semicolon). These
boundaries are the points at which oracles can be invoked, since intermediate prefixes are typically
syntactically incomplete.
2. Renderer and artifacts. Partial prefixes are typically syntactically incomplete (unclosed braces,
unfinished statements), and different oracles expect different inputs (a compilable snippet for a
compiler, an executable for a test runner). We therefore define a deterministic renderer
                                    Render : (S, Y≤i ) 7→ Ai ∈ A                                 (1)
mapping a boundary-terminated prefix to an artifact an oracle can process, where A is the artifact
space equipped with a scope map g : A → G. Render is defined only at structural boundaries:
prefixes ending at the closing token of some g ∈ G.
3. Oracle interface. Let O = {O1 , . . . , OJ } be the suite of verification oracles. Each oracle Oj has
an applicability predicate Fj : A → {0, 1} indicating whether it can be meaningfully invoked on A,
and returns a deterministic verdict and diagnostics:
                                 Oj (S, A) = (qj , dj ), qj ∈ {0, 1, ⊥},                               (2)
where 1, 0, ⊥ denote pass, fail, and not applicable respectively; qj = ⊥ iff Fj (A) = 0. In our
instantiations Fj is typically a scope threshold Fj (A) = 1[g(A) ⪰ gjmin ], but Fj may depend on
other features of A (e.g., a differential-testing oracle requires the target function to have test inputs).


                                                    3
Objective. A decoding strategy π interleaves token generation under M with oracle invocations on
intermediate artifacts, and may rollback and regenerate. Let Am := Render(S, Y≤m ) be the terminal
artifact, with terminal quality Q(S, Am ) = 1 iff all applicable evaluation oracles pass on Am . Given
a generation budget Bgen that hard-caps next-token model calls (counting tokens later discarded by
rollback), DTV targets
                                               
                            max E Q(S, Am ) s.t. Ngen (π) ≤ Bgen ,                                  (3)
                             π

where the expectation is over randomness in sampling from pM and any stochasticity in π. § 2.2
gives our concrete, deterministic instantiation of π.

2.2   Detailed Approach

We target the objective Eq. (3) through three mechanisms: (i) structural-boundary verification (§ 2.1),
which enforces the legal prefix invariant by aligning verifier calls with structural boundaries; (ii)
structure-aware rollback with escalation, which rolls back to the smallest scope implicated by the
verifier diagnostic and escalates to larger scopes on repeated failures; and (iii) feedback via prompt
augmentation, which surfaces unresolved oracle failures back to the model so subsequent generation
conditions on what went wrong. Algorithm 1 (Appendix G) describes these mechanisms as a single
loop: at each iteration the controller extends the prefix to the next structural boundary, runs applicable
oracles on the rendered artifact, and either commits (on unanimous pass) or invokes feedback-
augmented rollback at a chosen scope (on failure). Termination occurs on program-level oracle pass,
on bailout (the inner loop concedes that escalation cannot resolve the persistent diagnostics and
returns the current artifact to the outer loop), or generation budget exhaustion.
Meta steps. Between structural boundaries, DTV delegates token generation to the base sampler;
at each boundary it pauses to invoke oracles and act on their verdicts. We call each pause a meta
step (indexed k = 1, . . . , K): let bk denote the prefix length at meta step k (after any rollbacks),
Ak := Render(S, Y≤bk ) the artifact, and gk := g(Ak ) its scope. Oracles Oj with Fj (Ak ) = 1 are
applicable at meta step k. Every committed checkpoint must satisfy the legal prefix invariant: the
committed prefix can be extended into a program that passes all oracles, so that rollback targets are
always viable starting points. Enforcement is two-part: the renderer turns the current prefix into an
oracle-consumable artifact, and Algorithm 1 commits only when all oracles applicable at the current
scope pass. The controller below decides which action to take at each meta step.
Controller. The policy π is instantiated as a deterministic state-machine controller. At
each meta step k, it consumes an observation σk and emits an operation ωk that drives the
next iteration. The observation aggregates the current prefix, the latest oracle outputs ok =
{(qj , dj ) : Fj (Ak ) = 1}, the feedback state Fk , bounded retry and visit counters, and the
remaining token budget. The op ωk = (ak , ℓk , µk , βk ) chooses one of six actions ak ∈
{G ENERATE, V ERIFY, C OMMIT, ROLLBACK, F EEDBACK, T ERMINATE}, with optional fields: a
rollback scope ℓk ∈ G, a retry mode µk , and a bailout flag βk . Between meta steps, token generation
follows the base sampler unchanged, so DTV is a drop-in meta-level wrapper around any sampling
strategy (greedy, top-k, top-p). Appendix G gives precise semantics for each action.
Feedback. Rollback alone amounts to resampling from the same conditional distribution: although
sampling diversity (e.g., varying temperature) can yield retries that differ from earlier attempts,
exploring for the specific fix without diagnostic guidance is inefficient.The feedback loop therefore
has two parts.
1. Feedback state. The feedback state Fk is the controller’s working record of oracle failures not yet
resolved, with each entry holding the diagnostics needed to guide repair (error message and source
anchor). It feeds both the prompt augmentation step and the rollback/bailout policy. After observing
ok , the state is updated:
                                       Fk+1 = Update(Fk , ok ).                                    (4)
Update is a deterministic state update that adds new failures, drops failures resolved by passing
verdicts, and bounds the state’s size.
2. Prompt augmentation. We communicate Fk+1 back to the model by augmenting the condition-
ing context. Let ϕk+1 := Encode(Fk+1 ) be a textual block summarizing the active diagnostics,
and Sek+1 := Augment(S, ϕk+1 ) the augmented conditioning context. Between meta steps, Sek+1
replaces S in the conditioning context, so for any prefix Y<i the next-token distribution shifts from


                                                    4
pM (· | Y<i , S) to pM (· | Y<i , Sek+1 ). Rollback-with-feedback is therefore not blind resampling:
decoding resumes under updated feedback while S remains fixed. Two concrete retry modes (inline
continuation, patch-based repair) are described below.
Rollback, escalation, and bailout. When verification fails, the controller rolls back the prefix at the
smallest scope ℓ ∈ G capable of repairing the error. Scope selection is driven by oracle diagnostics:
for example, a localized type error may trigger statement-level rollback, while a missing function
return type may require function-level rollback. Failed retries escalate monotonically to coarser
scopes, exposing the model to a larger region of code in which to revise its generation.
To avoid unbounded retries on unfixable errors, DTV introduces two safeguards. Escalation: the
controller widens the rollback scope after repeated failures at finer scopes. For example, a Rust
mutability error whose root cause lies several statements upstream may require escalation to block
scope so the binding region itself can be regenerated (Appendix L.4). Bailout: when diagnostics
persist even after escalation, the controller terminates the inner loop and returns the current artifact
together with outstanding diagnostics to the outer loop.
In our implementation, a streaming-parser renderer maintains checkpoints over both the token prefix
and structural parsing state. After rollback, retries proceed in one of two modes: inline continuation,
which appends diagnostics as comments and resumes decoding in the same turn, or patch-based
repair, which requests a minimal patch in a new turn (Appendix I shows the prompt format and an
example exchange for each mode). Escalation follows a fixed ladder of (scope, mode) configurations,
and bailout occurs once rollback attempts exceed a threshold (Appendix H).


3     Experimental Setup

Tasks and datasets. We evaluate DTV on two complementary translation tasks:
 1. C to Rust (unsafe-to-safe systems translation): we sample 300 C programs from CodeNet [21],
    with test inputs for differential testing generated via AFL++ fuzzing with LLM-based seeding;
    we use rustc as oracle and differential testing for post-hoc behavioral equivalence.
 2. JavaScript to TypeScript (dynamic-to-static typing): we sample 150 self-bundled programs from
    TypeWeaver [22] that do not type-check as plain JavaScript, using tsc and ESLint’s type checker
    as oracles; executable tests are unavailable.
For comparisons with other baselines and cross-model analysis, we use cost-matched subsets of 200
(C to Rust) and 100 (JS to TS), drawn from the same pools. Per-task DTV instantiation, sampling
pipelines, and oracle filtering choices are in Appendix E.
Models. DTV requires direct control over decoding (boundary stops, rollback, feedback injection);
closed-weight inference APIs do not expose this control surface, so we use open-weight models
throughout. Our primary translation model is Qwen3-4B-Instruct [18]; we additionally use Gemma-
4-E4B-it [19] to test generalization across model families. DTV and the baselines share the same
model and decoding configuration in every comparison; full hyperparameters are in Appendix F.
Baselines and budget. We decompose test-time decoding strategies along two orthogonal axes. The
inner loop is either naı̈ve (the outcome-only configuration of § 2.2: complete generation in one
pass with no in-loop verification) or DTV (in-loop verification, rollback, and feedback; § 2.2). The
outer loop is either one-shot (a single attempt), self-refine (sequential regeneration with diagnostic
feedback when available), or best-of-N (BoN) (N independent attempts, returning the first oracle-
passing candidate). We evaluate five inner×outer combinations—naı̈ve/one-shot, naı̈ve/self-refine,
naı̈ve/BoN, DTV/one-shot, DTV/self-refine—plus S* [20]2 as a process-verified reference baseline
combining parallel sampling with compile-driven self-debug. All self-refine configurations share the
same per-case generation budget of 16× source tokens, counting all output tokens within a case.
Metrics. The primary metric is the post-hoc compilation pass rate (rustc for C to Rust; tsc with
strict mode disabled and ESLint zero-typedef for JS to TS). On C to Rust we additionally report
functional success rate via differential testing to verify that compile-pass gains do not mask semantic
regressions (Appendix J.5). We report the average per-case output tokens as the cost metric.

    2 Configured with independent attempts N =8, rounds R=3, and compile-error-based selection, deviating from the original

defaults [20] to fit the per-case token budget and fair comparison (clarified in Appendix E).


                                                              5
4                Results

Through our evaluation, we aim to answer the following questions:
• RQ1. Under equal per-case token budgets, does (i) DTV perform better than baselines on pass rate
  versus token cost on both tasks, and (ii) the gain transfer to different generator model families?
• RQ2. Do DTV’s key mechanisms all contribute positively to its performance?
• RQ3. (i) On which cases does DTV outperform naı̈ve, (ii) why does it do so, and (iii) how does the
  this picture hold under multi-round self-refine?

4.1                   Comparing DTV with baselines on pass rate and token efficiency

Under a fixed per-case generation budget of 16× source tokens, DTV/self-refine Pareto-dominates
naı̈ve/self-refine and lies in the upper-left region of the cost-vs-pass-rate frontier on both tasks
(cumulative pass-rate view in Figure 2b; full-set Pareto positions in Figure 6 in Appendix J.1). It
attains a pass rate of 82.0% on C to Rust and 46.0% on JS to TS, exceeding naı̈ve/self-refine by
+9.7 pp and +12.7 pp respectively.

                     naive/one-shot                 naive/self-refine          DTV/one-shot                           DTV/self-refine         naive/BoN-{1,2,4,8,16,32}                            S*/n8r3
                               C to Rust (n=200)                        JS to TS (n=100)                                       C to Rust (n=200)                                JS to TS (n=100)
                                     84.5                                                                             80




                                                                                                                                                        budget cap (k=16)




                                                                                                                                                                                                         budget cap (k=16)
                80                      76.0
                                                  75.5
                                                                                                                      60
                                                                                                      Pass rate (%)
                60
Pass rate (%)




                          45.5                    44.5                                  50.0
                40                                   N=32                               37.0                          40
                         17.0                                                  23.0      33.0                         20
                20                                                                           7.0
                         N=1                                      7.0
                 0                                                     N=1                     N=32                    0
                        103                 104                  103              104                                      0   5         10        15                       0   5       10          15
                                       Avg tokens per case (log scale)                                                                  Average k = tokens / source tokens

  (a) Per-case token cost (log scale) vs. compile pass rate, (b) Cumulative pass rate vs. per-case token budget k
  comparing against naı̈ve, best-of-N and S*
Figure 2: DTV/self-refine Pareto-dominates naı̈ve/self-refine and sits on the upper-left of the cost-
pass-rate frontier on both tasks, above the BoN-N and S* frontiers at matched per-case cost.

DTV/self-refine is also more token-efficient than naı̈ve/self-refine while attaining a higher pass rate:
on C to Rust the two configurations average k = 5.28 and k = 7.18 tokens per case respectively.
DTV/self-refine therefore lies in the upper-left region of the cost-versus-pass-rate frontier on both
tasks (Figure 6 in Appendix J.1).
Cumulative scaling of DTV vs. naı̈ve. The cumulative pass-rate curves over the per-case token
budget k (Figure 2b) reveal two structural differences. First, DTV exhibits an early-rise effect: its
step curve begins climbing at substantially smaller k than naı̈ve/self-refine on both tasks, because
in-loop verification and repair admit successful programs well before naı̈ve’s first complete sample is
generated. Second, on JS to TS, the two regimes diverge in the long-run: naı̈ve/self-refine plateaus
once additional tokens cease to yield further passes, while DTV/self-refine continues to rise. Once a
generation has settled on an under-typed structure, further refinement attempts tend not to recover
from it; in-loop type-annotation feedback, by contrast, redirects generation away from these basins.
Scaling through in-loop verification. Without any outer-loop retry, DTV/one-shot reaches 47.0%
on C to Rust and 21.3% on JS to TS at average per-case budgets of k ≈ 2.00 and k ≈ 2.77 (versus
k ≈ 1.55 and k ≈ 1.10 for naı̈ve/one-shot), exceeding naı̈ve/one-shot by +30.7 pp and +16.7 pp
(Figure 6 in Appendix J.1); the pass-rate gain more than offsets the verification overhead on both
tasks (per-pass cost in Appendix J.3). Layering self-refinement on top of DTV further raises the pass
rate, indicating that DTV composes with rather than substitutes for outer-loop test-time scaling.
This compile-pass improvement is not accompanied by a regression in behavioral correctness: on C to
Rust, DTV/self-refine attains a full-functional success rate of 8.3% compared with 9.3% for naı̈ve/self-
refine, a difference indistinguishable from zero under the paired test (Appendix J.5). DTV’s in-loop
oracle on C to Rust is rustc alone, with differential testing reserved for post-hoc evaluation, so the
controller receives no behavioral-equivalence signal during decoding; the absence of a regression
confirms that DTV does not erode behavioral correctness while optimizing compile pass.


                                                                                                      6
Cross-model robustness. The same in-loop verification mechanism transfers to a second model
family. We re-evaluate DTV/self-refine against naı̈ve/self-refine using Gemma4 as the generator on
both tasks (Appendix K). DTV exceeds naı̈ve at the budget cap on three of the four model-task pairs
and reduces normalized cost on three. The exception is C to Rust on Gemma4, where naı̈ve already
reaches 93.5% at the cap; under tight budgets (k ≤ 7), DTV/self-refine still leads naı̈ve on this cell
with a peak advantage of about +10 pp at k ≈ 4, and the curves cross near k ≈ 7 where naı̈ve’s
outer-loop retry over residual hard cases yields more marginal passes than DTV’s verify-and-rollback.

Comparing with other baselines. We additionally compare DTV/self-refine against best-of-N
(BoN, N ∈{1, 2, 4, 8, 16, 32}) and S* at matched per-case budget; DTV/self-refine remains on the
upper-left frontier against both on both tasks. On C to Rust, BoN improves from 15.5% at N =1 to
44.5% at N =32, but no N reaches DTV/self-refine’s frontier: small N (N ≤4) is cheaper yet caps
below 29.0%; large N (N ≥8) costs more yet still trails by at least +40.0 pp (Figure 2a). On JS to TS,
BoN is flat at 7.0% across all N as cost grows, suggesting that independent samples under the same
prompt reproduce the same under-typed structure.
S* reaches 75.5% on C to Rust and 33.0% on JS to TS, versus DTV/self-refine’s 84.5% and 50.0%,
while consuming roughly 4.7× DTV’s per-case tokens on C to Rust and 2× on JS to TS. DTV’s
advantage stems from verification timing: S* compiles only after each completed attempt, whereas
DTV verifies at structural boundaries within a single attempt, converting the same signal into early
localized rollback rather than full restart. The full baseline grid is in Appendix J.3.
Takeaway. DTV/self-refine Pareto-dominates naı̈ve/self-refine and lies above all baseline frontiers
on both tasks, with the gain transferring across model families.

4.2   Ablation study on DTV’s three key mechanisms


Table 1: Ablations on 100 C-to-Rust cases. All four configurations share the self-refine outer loop
and the same per-case token budget. ∆ columns report the ablation minus DTV-full.
                 Configuration           Pass rate       ∆ pp    Avg. tokens   ∆ tokens
                 DTV-full                  85.0%            –          3580          –
                 DTV-no-feedback           74.0%         -11.0         4138       +558
                 DTV-no-escalation         79.0%          -6.0         3623        +43
                 DTV-detect-and-abort      70.0%         -15.0         4417       +837


We ablate each of DTV’s three key mechanisms (§ 2.2) in turn, holding the remainder of DTV
(including the outer self-refine loop) fixed:
• DTV-no-feedback (ablates feedback via prompt augmentation): rollback without injecting diagnos-
   tics during inner generation.
• DTV-no-escalation (ablates structure-aware rollback with escalation): always roll back to statement
   scope, never widening to block or function.
• DTV-detect-and-abort (ablates structural-boundary verification): terminate the inner loop on the
   first verification failure, deferring recovery to outer self-refine.
DTV with all three mechanisms enabled (hereafter DTV-full) attains the highest pass rate among
the four configurations, and disabling any of the three reduces pass rate (Table 1). DTV-full reaches
85.0% on the first 100 C-to-Rust cases. Removing inner-loop diagnostic feedback drops pass rate to
74.0% (-11.0 pp), restricting rollback to statement scope drops it to 79.0% (-6.0 pp), and disabling
structure-aware inner recovery (detect-and-abort) drops it to 70.0% (-15.0 pp).
Within an equal per-case token budget. DTV-full converts more of the budget into passing
translations than the ablations: 3580 avg tokens per case versus 4138, 3623, and 4417 for the three
ablations. The detect-and-abort ablation in particular exhausts budget on failed inner attempts that
hit the per-case cap, which the outer self-refine loop then re-attempts: 13.5 outer rounds for detect-
and-abort versus 3.1 for DTV-full, roughly 4×. DTV-full achieves this by spending more tokens on
each successful translation than the ablations: 1694 per pass versus 1412, 1437, and 1173 (detailed in
Appendix L.1). The extra per-success tokens fund the in-loop verification and structured-recovery
work that converts otherwise-failing cases into passes.


                                                     7
                                                                                                     7




                                                                  rnaive/rDTV ( > 1 = DTV earlier)
                                                                                                     6
                                                                                                     5
                                                                                                     4
 Task          Local        Mixed        Nonlocal       ∆L-N                                         3
                                                                                                     2 mean=2.06   med=2.00
                                                                                                                         mean=1.61
 C → Rust     50.0% (12)   43.5% (168)   29.6% (27)    +20.4 pp                                                                      med=1.50
 JS → TS      29.3% (58)   11.9% (67)     0.0% (2∗ )   +29.3 pp                                      1                                          ratio = 1
                                                                                                     0
Table 2: DTV/one-shot rescue rate on naı̈ve R1-               C Rust        JS TS
                                                               (n=196)       (n=43)
failure cases by fix shape (R1→R2 diff). Cells show
rate with sample number n; color tracks rate; ∗ Figure 3: Paired round-count ratios
marks n < 5. Rescue rate decreases monotonically (rnaı̈ve /rDTV ) on the both-pass subset of
LOCAL→NONLOCAL on both tasks. Full breakdown self-refine. Markers: median (white circle),
in Table 18 in Appendix M.2.                        mean (red triangle).


Differential-testing pass rates. They follow the same ordering: DTV-full attains 10.0%, while
no-feedback, no-escalation, and detect-and-abort reach only 8.0%, 5.0%, and 8.0% respectively.
DTV-full therefore leads on behavioral correctness as well, ruling out the possibility that its pass-rate
advantage masks a behavioral regression. Paired McNemar tests on this 100-case ablation cohort are
reported in Appendix L.2.
The inner-1shot pass rate. This decomposes each mechanism’s effect between inner DTV and outer
self-refine. Removing diagnostic feedback drops inner-1shot by -23.0 pp: without an explicit signal
about what failed, the inner loop’s resampling tends to reproduce the same error pattern, deferring
recovery to outer self-refine. Disabling structured inner recovery (detect-and-abort) drops inner-1shot
by -30.0 pp—the largest first-pass effect: every inner verification failure discards in-loop state and
forces outer self-refine to retry from scratch with only post-hoc diagnostic context. Restricting
rollback to statement scope leaves inner-1shot unchanged at 44.0% but limits recovery on cases
where a diagnostic detected at one statement requires repair at an earlier committed statement (e.g.,
rustc’s “cannot assign to immutable variable” detected at a later mutation whose root cause is an
earlier let binding, which statement-scope rollback cannot reach). DTV-full’s scope escalation
does occasionally over-rollback and discard correctly-committed prefix in exchange; the net effect is
-6.0 pp final pass rate. Detailed analysis is in Appendix L.4.
Takeaway. All three of DTV’s mechanisms contribute, and removing any one reduces pass rate.
In-loop recovery contributes the largest gain compare to diagnostic feedback and scope escalation.

4.3     Deep analysis of DTV’s gain over the naı̈ve baseline

We take DTV’s gain apart through three sub-questions: (i) on which cases DTV outperforms naı̈ve,
(ii) why it does so, and (iii) whether the same picture holds under multi-round self-refine. The analysis
uses the 300 C-to-Rust and 150 JS-to-TS samples from § 4.1.
What kind of error DTV helps? To localize where DTV’s gain comes from in the one-shot regime,
we measure DTV’s rescue rate (the fraction of naı̈ve-failed cases that DTV solves) separately for each
type of fix the case requires. Lacking a ground-truth oracle for fix location, we use naı̈ve’s self-refine
behavior as a proxy: when naı̈ve’s first generation (R1) fails, its second generation (R2) attempts to
repair R1, and we take the lines R2 edits in R1 as an approximation of the necessary fix location.
We label each case’s fix shape, the relation between R2’s edited lines and R1’s flagged error lines,
as LOCAL (every edit lands on a flagged error line), NONLOCAL (none does), MIXED (partial
overlap), or UNKNOWN (R2 rewrites more than 50% of R1, excluded as uninformative); a more
rigorous variant using naı̈ve’s final passing round Rfinal in place of R2 yields the same conclusion on
a smaller set of cases (Appendix M.1). On both tasks, DTV’s rescue rate decreases monotonically as
the necessary fix moves further from the failing line, with the LOCAL-to-NONLOCAL gap reaching
20.4pp on C to Rust and 29.3pp on JS to TS (Table 2; full breakdown in Appendix M.2).
Why DTV outperforms post-hoc verification? DTV and naı̈ve differ in when they invoke verifi-
cation: DTV intervenes during generation, while naı̈ve verifies only the completed program. This
timing matters because autoregressive language models condition each token’s distribution on the


                                                           8
preceding prefix [14]: an error introduced early biases subsequent tokens toward extending the error
rather than recovering from it, so intervening early should reduce error accumulation compared
to post-hoc verification. To check whether DTV’s interventions reduce error counts, we restrict
to error codes that appear in both DTV’s inner-loop trace and naı̈ve’s one-shot loop, and on each
rescued case compute the per-case shared-code edit-concentration ratio: distinct DTV inner-loop
diagnostic emissions on the shared codes divided by distinct naı̈ve R1 emissions on the same codes
(Appendix M.4); a ratio below 1 means DTV emits fewer per-shared-code diagnostics than naı̈ve.
On JS to TS the ratio is well below 1 (median 0.50, mean 0.71, n = 26): a missing or wrong type
annotation propagates to every downstream use site, so catching it early prevents many derivative
errors. On C to Rust the ratio is near parity (median 1.00, mean 1.19, n = 57); the suppression
effect is weaker because rustc’s main error families (borrow check, lifetime, type mismatch) do not
compound across use sites the way TypeScript type errors do.
How DTV saves self-refine tokens? On cases both methods eventually pass (Figure 3), DTV’s
earlier intervention translates into fewer self-refine rounds (median paired ratio of naı̈ve’s rounds
to DTV’s: 2.00 on C to Rust, 1.50 on JS to TS), and the round savings carry through to tokens on
C to Rust (DTV uses fewer tokens on 67.9% of cases, median paired difference -208 tokens). On
JS to TS the median still favors DTV (-61 tokens), but the mean reverses (+220 tokens), driven by
a small tail of nonlocal-fix cases (e.g., typedef errors whose correct annotation depends on usage
elsewhere) where the inner loop re-emits the same diagnostic and rolls back without converging. A
detailed breakdown is in Appendix M.6.
Takeaway. DTV’s gain concentrates on cases with local fixes while weakens on nonlocal ones, where
early intervention prevents derivative errors and reduces self-refine rounds.


5   Related Work

DTV sits within test-time compute scaling, in the process-level supervision sub-family that emits
step-level signals during generation [1–3, 5, 7]; its distinguishing feature is that signals come from
deterministic verifiers rather than learned scorers or repeated sampling. Appendix D provides a
complete discussion; Figure 4 in Appendix C contrasts DTV against the two dominant prior paradigms.
We summarize the closest threads here.
Process supervision. Process reward models attach learned step-level scores and outperform outcome-
only verifiers on multi-step reasoning [4, 10, 23–26]. DTV produces step-level signals from de-
terministic oracles instead, yielding exact rather than probabilistic verdicts, removing the need for
annotation or training, and providing structured diagnostics to guide repair.
Verifier-guided generation. Outcome-only methods apply verifiers to completed programs for
filtering, ranking, or single-shot repair [6, 11–13, 20]. Recent work uses probabilistic programs of
thought reuse token-level uncertainty to obtain cheap candidate variants before post-hoc verifica-
tion [27]. In-loop methods place verifiers inside generation: line-level Python execution feedback
[15], function-level MCTS over Dafny/Coq partial programs [16], and verifier-driven tree-search
refinement on top of a self-improving training loop for Dafny-to-Verus [17]. DTV differs in three
respects: adaptive structural-boundary granularity (statement to program) rather than a fixed scope,
hard state-machine control rather than stochastic search, and multi-oracle composition (compiler,
type checker, differential tests).
Constrained decoding. Token-level recognizers (grammars, regexes, type automata) enforce hard
syntactic constraints during sampling [28–37]. They cannot invoke semantic verifiers (full type
checking, differential testing) on intermediate program scopes, since these require structurally
complete artifacts. DTV is complementary: constrained decoding can enforce syntactic invariants
while DTV adds semantic verification on top.


6   Conclusion

Standard test-time scaling for code applies deterministic verifiers (compilers, type checkers, tests)
post-hoc, after errors have compounded the whole generated code. We introduce Decoding Time
Verification (DTV), a decoding framework that interleaves generation with verifier calls, combining
with structural-boundary verification, structure-aware rollback, and feedback via prompt augmen-


                                                  9
tation. With Qwen3-4B, DTV/self-refine raises compile pass rate from 72.3% to 82.0% on C to
Rust and from 33.3% to 46.0% on JS to TS using fewer tokens per case than naı̈ve/self-refine,
Pareto-dominating naı̈ve/self-refine and sitting above the best-of-N and S* frontiers at matched cost;
gains transfer to Gemma-4-E4B on three of four pairs. Key challenges remain: scaling to larger
models, extending the approach beyond translation, and reducing the implementation effort for new
models and tasks (Appendix A). We hope DTV motivates future work on decoding-time control with
deterministic oracles.

References
 [1] Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM Test-Time Com-
     pute Optimally Can be More Effective than Scaling Parameters for Reasoning. In International
     Conference on Learning Representations, 2025.

 [2] Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi,
     Luke Zettlemoyer, Percy Liang, Emmanuel Candes, and Tatsunori Hashimoto. S1: Simple
     test-time scaling. In Proceedings of the 2025 Conference on Empirical Methods in Natural
     Language Processing, pages 20286–20332. Association for Computational Linguistics, 2025.
     doi: 10.18653/v1/2025.emnlp-main.1025.

 [3] Yixin Ji, Juntao Li, Yang Xiang, Hai Ye, Kaixin Wu, Kai Yao, Jia Xu, Linjian Mo, and Min
     Zhang. A Survey of Test-Time Compute: From Intuitive Inference to Deliberate Reasoning,
     January 2025.

 [4] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee,
     Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s Verify Step by Step. In
     International Conference on Learning Representations, 2024.

 [5] OpenAI. OpenAI o1 System Card, December 2024.

 [6] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond,
     Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy,
     Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl,
     Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson,
     Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-level
     code generation with AlphaCode. Science, 378(6624):1092–1097, December 2022. ISSN
     0036-8075, 1095-9203. doi: 10.1126/science.abq1158.

 [7] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré,
     and Azalia Mirhoseini. Large Language Monkeys: Scaling Inference Compute with Repeated
     Sampling, July 2024.

 [8] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and
     Karthik R Narasimhan. Tree of Thoughts: Deliberate Problem Solving with Large Language
     Models. In Advances in Neural Information Processing Systems, 2023.

 [9] Claudio Spiess, David Gros, Kunal Suresh Pai, Michael Pradel, Md Rafiqul Islam Rabin, Amin
     Alipour, Susmit Jha, Prem Devanbu, and Toufique Ahmed. Calibration and Correctness of
     Language Models for Code. In 2025 IEEE/ACM 47th International Conference on Software
     Engineering (ICSE), pages 540–552. IEEE, April 2025. doi: 10.1109/icse55347.2025.00040.

[10] Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng,
     Moontae Lee, Honglak Lee, and Lu Wang. Process Reward Models That Think, April 2025.

[11] Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-tau Yih, Sida Wang, and
     Xi Victoria Lin. LEVER: Learning to Verify Language-to-Code Generation with Execution. In
     International Conference on Machine Learning, 2023.

[12] Bei Chen, Fengji Zhang, A. Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu
     Chen. CodeT: Code Generation with Generated Tests. In International Conference on Learning
     Representations, July 2022.


                                                 10
[13] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teaching Large Language
     Models to Self-Debug. In International Conference on Learning Representations, 2024.
[14] Kushal Arora, Layla El Asri, Hareesh Bahuleyan, and J. Cheung. Why Exposure Bias Matters:
     An Imitation Learning Perspective of Error Accumulation in Language Generation. Findings,
     April 2022.
[15] Boaz Lavon, Shahar Katz, and Lior Wolf. Execution Guided Line-by-Line Code Generation,
     June 2025.
[16] David Brandfonbrener, Simon Henniger, Sibi Raja, Tarun Prasad, Chloe Loughridge, Federico
     Cassano, Sabrina Ruixin Hu, Jianang Yang, William E. Byrd, Robert Zinkov, and Nada Amin.
     VerMCTS: Synthesizing Multi-Step Programs using a Verifier, a Large Language Model, and
     Tree Search, May 2024.
[17] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. AlphaVerus: Bootstrapping Formally
     Verified Code Generation through Self-Improving Translation and Treefinement, December
     2024.
[18] Qwen Team. Qwen3 Technical Report, May 2025.
[19] Clement Farabet and Olivier Lacombe. Gemma 4: Byte for byte, the most capable open models,
     April 2026.
[20] Dacheng Li, Shiyi Cao, Chengkun Cao, Xiuyu Li, Shangyin Tan, Kurt Keutzer, Jiarong Xing,
     Joseph E. Gonzalez, and Ion Stoica. S*: Test Time Scaling for Code Generation. In Findings of
     the Association for Computational Linguistics: EMNLP 2025, pages 15964–15978. Association
     for Computational Linguistics, 2025. doi: 10.18653/v1/2025.findings-emnlp.865.
[21] Ruchi Puri, David S. Kung, G. Janssen, Wei Zhang, Giacomo Domeniconi, Vladmir A. Zolotov,
     Julian Dolby, Jie Chen, M. Choudhury, Lindsey Decker, Veronika Thost, Luca Buratti, Saurabh
     Pujar, and Ulrich Finkler. CodeNet: A Large-Scale AI for Code Dataset for Learning a Diversity
     of Coding Tasks. NeurIPS Datasets and Benchmarks, May 2021.
[22] Ming-Ho Yee and Arjun Guha. Do Machine Learning Models Produce TypeScript Types That
     Type Check? LIPIcs, Volume 263, ECOOP 2023, 263:37:1–37:28, 2023. ISSN 1868-8969. doi:
     10.4230/LIPIcs.ECOOP.2023.37.
[23] Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, L. Wang, Antonia
     Creswell, G. Irving, and I. Higgins. Solving math word problems with process- and outcome-
     based feedback, November 2022.
[24] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
     Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
     Schulman. Training Verifiers to Solve Math Word Problems, October 2021.
[25] Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu,
     and Zhifang Sui. Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human
     Annotations. In Proceedings of the 62nd Annual Meeting of the Association for Computa-
     tional Linguistics (Volume 1: Long Papers), pages 9426–9439. Association for Computational
     Linguistics, 2024. doi: 10.18653/v1/2024.acl-long.510.
[26] Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Harsh Lara, Yunxuan Li, Lei Shu,
     Yun Zhu, Lei Meng, Jiao Sun, and Abhinav Rastogi. Improve Mathematical Reasoning in
     Language Models by Automated Process Supervision, June 2024.
[27] Poorva Garg, Renato Lui Geh, Daniel Israel, Todd Millstein, Kyle Richardson, and Guy Van
     den Broeck. Probabilistic Programs of Thought, April 2026.
[28] Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. PICARD: Parsing Incrementally
     for Constrained Auto-Regressive Decoding from Language Models. In Proceedings of the
     2021 Conference on Empirical Methods in Natural Language Processing, pages 9895–9901.
     Association for Computational Linguistics, 2021. doi: 10.18653/v1/2021.emnlp-main.779.


                                                11
[29] Gabriel Poesia, Oleksandr Polozov, Vu Le, A. Tiwari, Gustavo Soares, Christopher Meek, and
     Sumit Gulwani. Synchromesh: Reliable code generation from pre-trained language models. In
     International Conference on Learning Representations, January 2022.
[30] Brandon T. Willard and Rémi Louf. Efficient Guided Generation for Large Language Models,
     July 2023.
[31] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. Prompting Is Programming: A Query
     Language for Large Language Models. Proceedings of the ACM on Programming Languages, 7
     (PLDI):1946–1969, June 2023. ISSN 2475-1421. doi: 10.1145/3591300.
[32] Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West. Grammar-Constrained
     Decoding for Structured NLP Tasks without Finetuning. In Proceedings of the 2023 Conference
     on Empirical Methods in Natural Language Processing, pages 10932–10952. Association for
     Computational Linguistics, 2023. doi: 10.18653/v1/2023.emnlp-main.674.
[33] Lakshya Agrawal, Aditya Kanade, Navin Goyal, Shuvendu K Lahiri, and Sriram Rajamani.
     Monitor-Guided Decoding of Code LMs with Static Analysis of Repository Context. In
     Advances in Neural Information Processing Systems, 2023.
[34] Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. Copiloting the Copilots: Fusing Large
     Language Models with Completion Engines for Automated Program Repair. In Proceedings
     of the 31st ACM Joint European Software Engineering Conference and Symposium on the
     Foundations of Software Engineering, ESEC/FSE 2023, pages 172–184, New York, NY, USA,
     November 2023. Association for Computing Machinery. ISBN 979-8-4007-0327-0. doi:
     10.1145/3611643.3616271.
[35] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song, and Martin Vechev. Type-
     Constrained Code Generation with Language Models. In Programming Language Design and
     Implementation, May 2025. doi: 10.1145/3729274.
[36] Debangshu Banerjee, Tarun Suresh, Shubham Ugare, Sasa Misailovic, and Gagandeep Singh.
     CRANE: Reasoning with constrained LLM generation. In International Conference on Machine
     Learning, February 2025.
[37] Henrijs Princis, Arindam Sharma, and Cristina David. TreeCoder: Systematic Exploration and
     Optimisation of Decoding and Constraints for LLM Code Generation, November 2025.
[38] Anh Ta, Junjie Zhu, and Shahin Shayandeh. Reinforced Agent: Inference-Time Feedback for
     Tool-Calling Agents, April 2026.
[39] Tianyang Zhou, Ziyi Zhang, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko,
     and Varun Chandrasekaran. SACTOR: LLM-Driven Correct and Idiomatic C to Rust Translation
     with Static Analysis and FFI-Based Verification, March 2025.
[40] Gavin Bierman, Martı́n Abadi, and Mads Torgersen. Understanding TypeScript. In Lecture
     Notes in Computer Science, pages 257–281. Springer Berlin Heidelberg, 2014. ISBN 978-3-
     662-44201-2 978-3-662-44202-9. doi: 10.1007/978-3-662-44202-9 11.
[41] Vincent J. Hellendoorn, Christian Bird, Earl T. Barr, and Miltiadis Allamanis. Deep learning
     type inference. In Proceedings of the 2018 26th ACM Joint Meeting on European Software
     Engineering Conference and Symposium on the Foundations of Software Engineering, pages
     152–162. ACM, October 2018. doi: 10.1145/3236024.3236051.




                                               12
                                          APPENDIX

A    Limitations

DTV rests on assumptions that bound its applicability and incurs non-trivial per-task and per-model
implementation effort, both of which we document here.

Oracle requirements. DTV requires oracles to produce local, actionable diagnostics with source-
line attribution (Section 2.2); oracles returning only a global pass/fail verdict can drive the commit
decision but cannot guide structure-aware rollback or feedback. Our in-loop oracle suite consists
only of compilation-style verifiers (rustc on C to Rust, tsc and ESLint on JS to TS); slower or
weaker-signal oracles such as cross-language differential testing (Table 3) are reserved for post-hoc
evaluation, and whether DTV’s in-loop mechanism remains effective when driven by such oracles is
not addressed empirically.

Non-local semantic errors. Structure-aware rollback is only effective when a failure can be
fixed within a bounded scope (statement, block, or function). Errors requiring global redesign—
cross-module type inconsistencies, architectural mismatches—lie outside the rollback ladder; in the
JS-to-TS experiment, three classes of tsc type-correctness errors exhibit this non-locality and are
removed from the in-loop oracle (Appendix E).

Implementation and evaluation scope. DTV requires non-trivial effort to support a new task: each
new language pair requires a partial-prefix renderer with per-construct context rules and, for each
oracle, a driver, output parser, and prefix-incompleteness filter, while supporting a new model family
requires a model-specific decoding backend encoding its chat template, and may require extending
renderer coverage and recalibrating prompting heuristics to match the new model’s target-language
idiom preferences. Our evaluation correspondingly covers a limited scope: two 4B-parameter open-
weight generators (Qwen3-4B-Instruct, Gemma-4-E4B-it) on two code translation settings (C to Rust,
JS to TS). Whether the observed gains persist on larger generators or on non-translation domains
with deterministic process-level verifiers (theorem proving, query generation, formal modeling) is
not addressed empirically.

Verifier wall-clock cost. Our evaluation matches per-case generation budgets in tokens, which
controls model-side compute but not verifier-side wall-clock cost (toolchain startup, code size,
dependency resolution). DTV’s higher oracle-invocation count relative to outcome-only baselines
therefore incurs additional wall-clock cost that the token-matched evaluation does not account for;
the token-cost-versus-pass-rate improvements reported in Section 4.1 may not translate directly to
wall-clock in deployments where verifier latency dominates.


B    Broader Impacts

DTV is a decoding-time algorithm for code translation under deterministic verifiers; it does not train
new models or release new generative capabilities. Its most direct positive impact is lowering the
cost of translating legacy code into safer target languages, for example C to Rust, where memory-
safety bugs account for a substantial fraction of reported security vulnerabilities, and JavaScript to
TypeScript, where static typing catches a class of latent defects at development time. By converting
outcome verifiers into process-level guidance, DTV also reduces the number of generation tokens
spent on rejected candidates relative to outcome-only decoding, which lowers compute and energy
cost per successful translation.
The most direct negative impact is the risk of misplaced confidence in oracle-passing translations.
DTV’s C OMMIT decision certifies only that the committed prefix passes the configured verifier suite
(compilation, type checking, and differential testing on a finite set of inputs). It does not certify
behavioral equivalence on all inputs, freedom from undefined behavior, concurrency correctness,
or fitness for any particular safety-critical use. Users who deploy DTV-translated code without
independent review, especially in security-sensitive or safety-critical settings, may be exposed to
defects outside the oracles’ coverage. We recommend treating DTV outputs as a starting point


                                                 13
              (a) OUTCOME-ONLY                                         (b) LEARNED PRM                                                (c) DTV
                                                        Line      Generated statement         PRM score        Generate L1
                                                                                                                                                                         rollback
        rustc fires only at end of trajectory                                                                                          rustc at      Diagnostic          to L0 &
                                                        L1      let count: i32 = "10";            0.87    let count: i32 = "10";

                                                                                                                                         🛠️
                                                                                                                                      boundary      line 1: expected   regenerate


                                                        L2      let total = count * 2;            0.42
                                                                                                                                                     i32, found &str
                                                                                                                                                                           🔄
                                                                                                                                                                        with hint


 L1 let count: i32 = "10";         ✖ L1 type mismatch
                                                                                                                                 Repaired program
 L2 let total = count * 2;         ✖ L2 cascade error
                                                        L3      let avg = total / 4;              0.71    L1 let count: i32 = "10".parse().unwrap();
 L3 let avg = total / 4;           ✖ L3 cascade error



                                                                                                                                                                       ✅
                                                                                                          L2 let total = count * 2;
 L4 println!("{}", avg);           ✖ L4 cascade error
                                                                                                          L3 let avg = total / 4;
                                                        L4      println!("{}", avg);              0.55
                                                                                                          L4 println!("{}", avg);


       Downstream lines generated on falsified                 May mark the wrong line → L3 with 0.71
                                                                 Scalar score only → No repair hint                   Error captured and fixed in the early stage
          assumption → cascade of errors




Figure 4: Three verification paradigms on an illustrative C-to-Rust translation. (a) Outcome-only
verifies after completion; (b) a learned PRM produces scalar ranking signals; (c) DTV verifies at
structural boundaries, rolls back, and regenerates with diagnostic feedback.


for human review and co-designing the verifier suite with the deployment risk profile (e.g., adding
fuzzing, sanitizers, or formal verification for high-assurance settings).

C      Verification Paradigms
Figure 4 situates DTV against the two paradigms that dominate prior work on verifier-guided
generation. Outcome-only verification (panel a) applies verifiers post-hoc to completed samples, so
a failing verdict discards an entire program-length sequence and the model has already extended
downstream code on top of the falsified prefix. Learned process supervision (panel b) attaches
probabilistic scores to intermediate steps, but a high score cannot certify that a partial translation can
be extended to pass the compiler, type checker, and differential tests, and training such scorers requires
verifier-, language-, and source-target-specific supervision. DTV (panel c) integrates deterministic
verifiers directly into the autoregressive loop, combining structural-boundary verification, structure-
aware rollback, and feedback re-injection. Appendix D discusses the closest prior work in each
paradigm.

D      Related Work (Extended)
This appendix expands the compressed discussion in §5 with a per-system breakdown.

Test-time compute scaling. Test-time compute scaling has emerged as a complement to parameter
scaling: extra inference compute can substitute for larger models. Existing approaches differ along
two axes: the signal source used to allocate compute (repeated independent sampling [7], compute-
optimal allocation against learned process reward models [1], deliberate search over reasoning
traces [8], and end-to-end long-reasoning systems [2, 5]; surveys catalog these strategies [3]), and
the decoding integration of those signals (outcome-only after a complete program, or process-level
inside generation). DTV is itself a test-time compute scaling method, in the process-level supervision
sub-family, with the distinguishing feature that signals come from deterministic verifiers (compilers,
type checkers, tests) integrated at structural boundaries during decoding. Probabilistic programs of
thought (PPoT) [27] are also motivated by fixed-budget inference: they reuse next-token probabilities
from completed LLM samples to draw cheap local variants before post-hoc verification, whereas
DTV changes when verifier diagnostics affect the search by committing, rolling back, and repairing
prefixes. The rest of this section compares DTV against the closest prior work in each adjacent corner:
learned process scorers, execution-guided and verifier-guided generation (post-hoc and in-loop), and
constrained decoding.

Process supervision via learned scorers. Process reward models (PRMs) train a learned scorer
on step-level annotations and outperform outcome-only verifiers on multi-step reasoning [4, 23, 24].
Recent work reduces annotation cost via automated step supervision [25, 26], while Khalifa et al. [10]
replace discriminative PRMs with chain-of-thought verifiers. Reinforced Agent [38] similarly moves
feedback before tool execution, its signal is a reviewer LLM over complete tool-call actions rather
than a deterministic verifier over rendered code artifacts. DTV produces step-level signals as well,
but obtains them from deterministic oracles rather than learned scorers. This shifts the design space


                                                                                        14
along three axes: signals are exact rather than probabilistic, enabling hard C OMMIT and ROLLBACK
actions instead of soft re-ranking; they require no annotation or training data; and they come with
structured diagnostics (error messages, failing locations) that DTV uses for repair—none of which is
naturally available from a learned PRM.

Execution-guided and verifier-guided generation. One line of work uses deterministic verifiers
(compilers, tests, formal solvers) to evaluate complete programs after generation, using the verdict for
filtering, ranking, or single-shot repair [6, 11–13, 20]. A more recent line moves the verifier inside
generation: Lavon et al. [15] run line-by-line Python execution feedback through Classifier-Free
Guidance (EG-CFG); Brandfonbrener et al. [16] use MCTS guided by partial-program verification
in Dafny and Coq (VerMCTS), with a token-budget metric (pass@T) closely related to ours; and
Aggarwal et al. [17] add verifier-driven tree-search refinement (Treefinement) for translating Dafny to
Verus (AlphaVerus). DTV differs from these in-loop methods in five respects: (i) adaptive structural-
boundary granularity spanning statement, block, function, and program, rather than a single fixed
scope (line in EG-CFG, function in VerMCTS), motivated by the fact that partial programs in static-
typed mainstream languages admit only specific oracle-consumable scopes; (ii) hard state-machine
control with explicit C OMMIT, ROLLBACK, and F EEDBACK actions, rather than soft probability
interpolation, stochastic search, or whole-program restart; (iii) multi-oracle composition (compiler
diagnostics, type checker, differential testing) rather than a single signal type; (iv) decoding-time only
with a frozen pretrained model, while AlphaVerus involves a self-improving training loop; and (v)
structured diagnostic-driven repair via the explicit F EEDBACK action and its patch-based retry mode,
which consume oracle diagnostics and failing locations to construct targeted repair prompts, rather
than passing raw execution traces as soft prompt context (EG-CFG) or discarding the failure content
beyond a scalar pass/fail signal (VerMCTS, AlphaVerus).

Constrained decoding for code. Constrained decoding enforces hard token-level constraints
derived from a recognizer (grammar, regex, finite-state machine, or type automaton) that operates
over partial token sequences, masking tokens that would violate the recognizer at each sampling
step [28–32]. Recent code-aware variants extend this in several directions: Agrawal et al. [33]
drive decoding with repository-level static analysis; Wei et al. [34] prune tokens via a completion
engine; Mündler et al. [35] introduce prefix automata over inhabitable types; and Banerjee et al.
[36] augment the grammar to preserve reasoning capacity. More recent framework work generalizes
this with pluggable search strategies and composable constraints: Princis et al. [37] unify sampling,
beam search, MCTS, SMC, and ASAp under a tree-search abstraction that admits both token-level
syntactic constraints and whole-program execution constraints (e.g., unit tests) via a product-of-
experts formulation. By construction, these methods enforce constraints either as recognizers
over partial token sequences (typically syntax or local typing) or as post-hoc filters on completed
programs; they cannot invoke semantic verifiers at intermediate program scopes during generation.
DTV is orthogonal in two respects. First, it accepts oracles as black boxes, including those that
require structurally complete artifacts and therefore cannot be expressed as token-level recognizers
(compilation against the full type and borrow checker, differential testing against the source program).
Second, it does not constrain the base sampler; verification failures are handled after the fact by
structure-aware rollback and diagnostic feedback, rather than prevented up front. The two approaches
compose: constrained decoding can enforce hard syntactic invariants while DTV adds a semantic
verification layer on top, a combination we leave to future work.
In summary, DTV sits within test-time compute scaling and process-level supervision, with three
architectural commitments that distinguish it from prior work: deterministic verifier signals (vs.
learned PRMs), adaptive structural-boundary granularity with explicit checkpoint rollback (vs. fixed-
scope or whole-program in-loop methods), and a hard state-machine controller composing multiple
oracles (vs. soft re-ranking, syntactic recognizers, or training-time verifier-feedback pipelines).

E    Task and Oracle Setup
This appendix expands the per-task descriptions, dataset construction pipelines, and oracle configura-
tions summarized in Section 3.

C to Rust. A representative unsafe-to-safe systems translation task. C programs routinely rely on
manual memory management and undefined behavior that must be resolved into explicit Rust idioms


                                                   15
(ownership, borrowing, lifetimes), making correctness verification non-trivial and the task widely
studied in the program-analysis community [39]. The Rust compiler (rustc) provides a strong static
oracle spanning syntactic and semantic analysis (types, borrows, lifetimes), and differential testing,
executing both the C source and the Rust translation on the same inputs and comparing outputs,
provides a behavioral equivalence oracle. These oracles complement each other: rustc supplies
static signals on partial programs, while differential testing supplies behavioral signals on complete
programs.

JavaScript to TypeScript. A representative dynamic-to-static typing task. The translation is
primarily about introducing sound type annotations: when an explicit annotation is missing and the
compiler’s inference cannot resolve a type, TypeScript silently falls back to implicit any, which passes
compilation but bypasses the type system and exposes the program to the type-related safety issues
that migration was meant to eliminate [40, 41]. Catching such degradation requires verifiers beyond
the compiler alone. Two verifiers are used: the TypeScript compiler (tsc) for compilation checks,
and ESLint for detecting missing type annotations. Unlike C to Rust, TypeWeaver packages do not
ship with executable test suites, so differential testing is not available; the compiler and linter serve as
the sole correctness oracles.

Component instantiation. Table 3 summarizes how the abstract DTV components (Section 2.2)
are instantiated for each task. The two tasks span complementary verification axes: unsafe-to-safe (C
to Rust) versus dynamic-to-static (JS to TS), and compiler-plus-executable-test versus compiler-plus-
linter oracle suites.

Table 3: Instantiation of DTV components for each translation task. The in-loop oracle drives DTV’s
in-generation verification, rollback, and feedback. The outer-loop oracle judges pass/fail at the end
of each generation attempt for self-refine and best-of-N . The post-hoc oracle is used only for final
evaluation.
            Component           C to Rust                        JS to TS
            Renderer            Rust syntax/semantic patching    TS legal prefix + context rules
            In-loop oracle      rustc                            tsc (weakened) + ESLint
            Outer-loop oracle   rustc                            tsc (strict off) + ESLint
            Post-hoc oracle     rustc; differential testing      tsc (strict off) + ESLint



C to Rust dataset and test-input generation. We construct the 300-sample evaluation set in three
stages, all using fixed random seeds. Stage 1: pool construction. We filter Project CodeNet [21] to C
submissions with status Accepted and retain only those whose source contains a standard-input call
(scanf, fgets, getchar, etc.), since differential testing requires programs that consume external
inputs. For each problem we select the submission with median code size as its representative,
ensuring at most one program per problem. Stage 2: stratified sampling. We stratify the per-problem
representatives by source byte size into three tiers (small <300 bytes, medium 300–1000 bytes,
large >1000 bytes) and sample proportionally across tiers with a minimum of 10 representatives per
tier, yielding 400 candidate programs. Stage 3: test-input generation. CodeNet does not provide
executable test inputs, so we generate them per candidate via a hybrid LLM-seeded AFL++ pipeline.
We first prompt GPT-5.4 for 25 stdin test inputs per program, with instructions to include boundary
values and ASCII-only content, and validate each candidate by executing the AFL-instrumented
binary; seeds that exit non-zero or exceed a 5-second timeout are discarded. The validated seeds
bootstrap AFL++ fuzzing for 90 seconds in stdin mode. The resulting AFL++ queue is minimized with
afl-cmin and further filtered through AddressSanitizer, UndefinedBehaviorSanitizer, and Valgrind
memcheck to drop inputs that trigger crashes, undefined behavior, or memory errors; surviving inputs
form the final test corpus per program. The pipeline succeeds on 306 of the 400 candidates; the
remaining 94 fail due to compilation errors, lack of valid LLM seeds after execution filtering, AFL++
producing no queue entries, or no inputs surviving the sanitizer filter. We draw 300 cases uniformly
at random from these 306 as the final evaluation set. Coverage is measured by re-executing each
surviving input against a coverage-instrumented clang build and reported via llvm-cov source-
based coverage. The resulting fuzz corpora attain mean per-sample line coverage of 93.4% (aggregate
85.1%, 11,721 of 13,781 lines) and mean per-sample branch coverage of 87.5% (aggregate 78.9%,


                                                    16
6,838 of 8,662 branches). The selected programs span 16–448 lines of code, with median 46 and
mean 68.8.

JavaScript to TypeScript dataset. We construct the 150-sample evaluation set from
TypeWeaver [22].         We start from the two subsets top1k-typed-nodeps-es6 and
top1k-untyped-nodeps-es6 and process each candidate package as follows. For each pack-
age we produce a single bundled JavaScript file via rollup (ES module format on the package’s
main entry). We discard packages whose bundled size falls outside [30, 1000] lines of code, and we
exclude packages that already pass tsc under strict mode without modification, since these provide
no translation signal. From the resulting pool we sample 150 packages uniformly at random (seed
42). The selected packages span 30–741 bundled lines of code, with median 91 and mean 149.2.

Oracle diagnostic filtering. All three in-generation verifiers (rustc, tsc, and ESLint) filter their
raw diagnostic output before it drives rollback or feedback in DTV. We distinguish two categories of
filtering.
Partial-code noise filters (all three oracles). Partial-code verification is inherently noisy: a prefix
produces diagnostics that reflect mere incompleteness (“unexpected EOF”, “expected }”) rather than
genuine translation errors. Each oracle therefore applies a lightweight noise filter. These filters are
necessary plumbing for any partial-program verification scheme rather than conceptual weakenings
of the verifiers:
• rustc (C to Rust): drops diagnostics whose source spans extend past the current prefix boundary
  or point to end-of-file artifacts introduced by partial code.
• tsc (JS to TS): applies the analogous filter on tsc’s JSON output, discarding incompleteness-only
  diagnostics.
• ESLint (JS to TS): drops diagnostics whose source position lies past the current prefix boundary,
  which can arise because our rendered artifact includes context-rule additions (e.g., a closing })
  beyond the actual generated prefix.
Semantic weakening of tsc (JS to TS only). On top of partial-code noise filtering, the in-loop tsc oracle
for JS to TS is weakened in two additional ways, which are conceptual design choices rather than
plumbing:
• Strict mode disabled: tsc is invoked with strict: false, which suppresses strictness-family
  diagnostics (including noImplicitAny).
• Type-correctness error filter: three error classes are dropped before the verdict is computed:
  TS2322 (type mismatch in assignment), TS2339 (property does not exist on type), and TS2345
  (argument type not assignable to parameter type).
These errors are common in partial translations but are typically not actionable for in-loop retry: they
often reflect missing context about external types or deliberate typing choices that become resolvable
only once the full program is available. Retaining them would cause DTV to spend retry budget on
diagnostics the model cannot productively fix. We therefore filter them during generation only; the
outer-loop and post-hoc tsc oracles preserve them and let them count against the verdict.
The post-hoc compilation pass rate reported in Section 3 uses tsc with strict mode disabled and pairs it
with the ESLint @typescript-eslint/typedef rule, which independently flags the implicit-any
hazard that strict mode’s noImplicitAny would otherwise catch. We do not enable strict mode for
tsc because ESLint’s type-annotation checks already target the key safety issue of missing type
annotations, which is enough to evaluate for the JS to TS task.
Note that rustc and ESLint do not receive analogous semantic weakening. rustc’s structural errors
(unresolved names, moved values, borrow violations) are directly actionable in-loop, and ESLint’s
configured rules are already narrowly targeted at missing type annotations.

Baseline configuration details. S* [20] is configured with N =8 parallel candidates, R=3 compile-
feedback rounds per candidate, and compile-error argmin selection (the candidate whose final round
compiles with the fewest errors is returned, breaking ties by sample order). Both choices deviate
from the original defaults (N =16, R=2, adaptive input synthesis) for two reasons. First, N =8, R=3
replaces N =16, R=2 because N =16 would exceed the per-case token cap under which DTV and
naı̈ve/BoN-32 operate; the resulting per-case generation budget of N × R = 24 (versus the paper’s


                                                   17
default of 32) aligns with the envelope shared by the other baselines. Second, compile-error argmin
selection replaces adaptive input synthesis because the original mechanism prompts an auxiliary
LLM to synthesize distinguishing test inputs and selects the candidate whose execution outputs align
with the LLM’s predicted behavior, a procedure that presupposes the availability of program-level
test inputs in the task specification, which translation tasks (C-to-Rust, JS-to-TS) do not provide.
We therefore adopt the “Public Only” selection variant reported in Table 3 of Li et al. [20], which
selects the candidate whose final round compiles with the fewest errors and breaks ties by sample
order, ensuring DTV and all baselines share an identical in-loop oracle signal (rustc for C to
Rust, tsc with ESLint zero-typedef for JS to TS). Because BoN-32 and S* are substantially more
computation-intensive than the head-to-head configurations, the BoN grid, S* comparisons, and
cross-model analysis (Appendix K) are evaluated on subsets: n = 200 for C to Rust and n = 100 for
JS to TS, drawn from the same case pools as the main evaluation.

F   Model and Decoding Hyperparameters
All experiments are run locally via the HuggingFace Transformers library. We evaluate two open-
weight instruction-tuned models:
• Qwen3-4B-Instruct (Qwen/Qwen3-4B-Instruct-2507) [18].
• Gemma-4-E4B-it (google/gemma-4-E4B-it) [19].
Both models are used as black-box generators (no fine-tuning). DTV and the naı̈ve baseline share
the same model and decoding configuration within a given experiment, so any pass-rate difference
isolates the effect of the decoding strategy rather than the underlying sampler.

Sampling. Between meta steps we use each model’s default sampler as shipped in its
generation config.json, without overriding sampling hyperparameters. Table 4 lists the specific
values for the two evaluated models. A greedy decoding mode (do sample=False) is exposed as an
ablation option but is not used in the main experiments.

Table 4: Default sampler hyperparameters shipped with each model’s generation config.json.
               Model                     do sample       temperature   top k   top p
               Qwen3-4B-Instruct-2507       true             0.7        20       0.8
               Gemma-4-E4B-it               true             1.0        64      0.95


Generation caps. Each outer decoding round is bounded by a per-round cap on newly generated
tokens (MAX NEW LENGTH: 2048 for C-to-Rust, 16384 for JS-to-TS) and a global cap on controller
iterations (MAX STEPS = 2000). The per-case generation-token budget is set to 16× the source token
count (Section 3), consumed across all generation within a case (including tokens discarded by
rollback).

Hardware. All experiments are run on a single Nvidia A100 (40GB) or GH200 (96GB) GPU. Both
4B-parameter generators are loaded in BF16.

G    Per-Action Semantics
The controller’s action set is implemented as follows.
• G ENERATE: invoke the base sampler to extend the current prefix by one or more tokens, stopping
  at a structural boundary (e.g., end of statement) or when the generation budget is exhausted.
• V ERIFY: render the current prefix into an artifact, select applicable oracles by scope, and record
  their verdicts and diagnostics into the feedback state.
• C OMMIT: mark the current prefix as a trusted checkpoint, saving the group stack state from the
  renderer for later structure-aware rollback.
• ROLLBACK: restore the prefix to a prior checkpoint at a scope ℓ ∈ G chosen by the policy;
  statement-level rollback retries the last statement, while block/function rollback truncates to the
  group start.


                                                   18
Algorithm 1 Decoding Time Verification (DTV). Given source S, oracles O, and budget Bgen , DTV
alternates boundary-aligned token generation with oracle verification. Failures trigger feedback-
augmented rollback; success terminates at program-level oracle pass.
Require: source S, oracles O, generation budget Bgen
Ensure: terminal artifact A, success flag s ∈ {SUCC, FAIL}
 1: Y ← ∅, C ← {∅}, F ← ∅ {init prefix, checkpoints, feedback state}
 2: while Ngen < Bgen do
 3:   Y ← G ENERATE(Y, Augment(S, F)) {sample to next structural boundary or EOS}
 4:   A ← Render(S, Y ); {(qj , dj )} ← V ERIFY(A, O)
 5:   if qj = 1 for all applicable j then
 6:      C ← C OMMIT(C, Y )
 7:      if g(A) = program then
 8:         return (A, SUCC)
 9:      end if
10:   else
11:      F ← U PDATE(F, {(qj , dj )})
12:      (action, ℓ) ← D ECIDE(F)
13:      if action = BAILOUT then
14:         return (A, FAIL)
15:      end if
16:      Y ← ROLLBACK(C, ℓ)
17:   end if
18: end while
19: return (Render(S, Y ), FAIL) {budget exhausted}



• F EEDBACK: construct a retry prompt from the current feedback state and ask the model to address
  the diagnostics; supports two realizations described in Section 2.2.
• T ERMINATE: end the decoding loop; triggered normally at end-of-sequence, or early in the case of
  a bailout when the same diagnostic persists across scope escalations.

H    Implementation Details
This appendix specifies the concrete data structures and policies that instantiate the DTV algorithm
of Section 2.2. Other instantiations are possible; we describe the one used in our experiments.
Scope map implementation. We implement the scope map g : A → G via a group stack maintained
by the renderer: as tokens stream in, the renderer pushes frames onto the stack at block and function
openings, and pops them at the corresponding closings. This mirrors the scope-tracking stack
standard parsers maintain when reading source code, with the difference that it operates on the partial
generation rather than on a complete file. The renderer is paired with a token-level stopping criterion
that halts the base sampler when the current prefix reaches a structural boundary (with awareness of
strings, comments, and nested delimiters), handing control back to the controller to trigger the next
meta step.
The renderer supplies the oracle-consumable artifact referenced by the legal prefix invariant (Sec-
tion 2.2): it emits only when the current prefix ends at a structural boundary and the group stack is
in a consistent state. The semantic side of the invariant (absence of oracle violations at the current
scope) is decided by V ERIFY and C OMMIT in Algorithm 1.
Checkpoints and retry ladder. Each C OMMIT checkpoints the current prefix together with the group-
stack state. On ROLLBACK, the controller re-generates from the rolled-back prefix under the aug-
mented context. Retry is parameterized by two choices: the rollback scope ℓ ∈ {stmt, block, func}
(how far back to truncate Y ) and the retry mode (Appendix I shows the prompt format and an example
exchange for each mode):
• Inline continuation: the model resumes generation from the rolled-back prefix with the diagnostic
  summary appended as an inline comment.
• Patch-based repair: instead of continuing inline, the controller closes the current assistant turn and
  asks the model in a new user turn for a minimal patch addressing the diagnostics. The patch is


                                                  19
                 Feedback A: Inline continuation                              Feedback B: Patch-based repair

    let arr: Vec<f64> = ...;        // failed; rolled back        let arr: Vec<f64> = ...;        // failed; rolled back
    /* repair feedback:                                           [User message]
       diagnostic: trait bound 'f64: FromStr'                     Failed snippet: let arr: Vec<f64> = ...;
                   not satisfied; expected 'i32'                  Diagnostic:      E0277 expected 'i32', found 'f64'
       hint: try changing 'f64' to 'i32'                          Goal:            minimal patch at scope=stmt.
    */
    let arr: Vec<i32> = ...|         // model continues           [Assistant response]
                                                                  - let arr: Vec<f64> = ...;
                                                                  + let arr: Vec<i32> = ...;



Figure 5: The two repair modes (Section 2.2) on the same rustc E0277 failure. (left) Inline
continuation: diagnostic appended as a comment, model continues in the same turn. (right) Patch-
based repair: structured user turn, model returns a diff patch in a fresh assistant turn.


    constrained to the rollback scope; outputs that violate the constraint are rejected and the controller
    advances along the retry ladder.
The controller traverses a fixed linear retry ladder R1 , R2 , . . . , RK , where each Rk = (ℓk , µk )
specifies a (scope, mode) configuration together with a maximum retry count ck . On repeated failure
at the same diagnostic anchor, the controller advances along the ladder: finer configurations are
exhausted before coarser ones (scope widens from stmt through func; within each scope, mode
escalates from inline to patch-based). Exact ordering and retry counts are given in Appendix G.
Bailout. To bound work on unfixable errors, the controller tracks the number of times each diagnostic
anchor (identified by enclosing function, primary error code, and primary error message) has triggered
a rollback. When this visit count exceeds a threshold, the ladder is abandoned: the controller issues
T ERMINATE with bailout flag βk = 1 and returns the current artifact together with the outstanding
diagnostics.


I     Feedback Prompt Formats

The two retry modes from Section 2.2 differ in how the diagnostic-augmented prompt is delivered
to the model and what the model is asked to return. Figure 5 shows the same C-to-Rust failure (a
rustc E0277 trait-bound error: the model bound Vec<f64> where the surrounding context required
Vec<i32>) handled by each mode.


J      RQ1 detailed results

This appendix complements the main-body RQ1 results (Section 4.1) with the full numerical break-
down, paired statistical tests, and the methodology underlying the BoN comparison. All reported
numbers are produced by the same statistics pipeline that generates the figures and tables in Sec-
tion 4.1.


J.1     Full-set head-to-head comparison

Figure 6 reproduces main-body Figure 2 on the full evaluation set (n = 300 for C to Rust, n = 150
for JS to TS), restricted to the four head-to-head configurations referenced in Section 4.1 (naı̈ve
vs. DTV with one-shot vs. self-refine). The cost-matched subset version, jointly comparing these
head-to-head configurations against the BoN-N and S* baselines on the n = 200 C-to-Rust and
n = 100 JS-to-TS subsets, is reported in main-body Figure 2; the head-to-head pass rates on the full
set quoted in Section 4.1 are taken directly from the data underlying this appendix figure.


J.2     Pass rate breakdown

Table 5 gives the full pass-rate and token-cost breakdown underlying the compact RQ1 summary in
Section 4.1.


                                                             20
                       naive/one-shot               naive/self-refine        DTV/one-shot                          DTV/self-refine                  naive/BoN-{1,2,4,8,16,32}                            S*/n8r3
                100             C to Rust (n=300)                   JS to TS (n=150)                                                  C to Rust (n=300)                                   JS to TS (n=150)
                                                                                                                        80




                                                                                                                                                               budget cap (k=16)




                                                                                                                                                                                                                  budget cap (k=16)
                 80                     82.0%
                                           72.3%
Pass rate (%)                                                                                                           60




                                                                                                        Pass rate (%)
                 60
                        47.0%                                                                  46.0%                    40
                 40                                                                          33.3%

                       16.3%                                                                                            20
                 20                                                            21.3%
                                                             4.7%
                  0                                                                                                      0
                      103                          104     103                         104                                   0        5        10         15                       0      5       10         15
                                          Average tokens per case (log)                                                                      Average k = tokens / source tokens

 (a) Per-case avg tokens (log scale) vs. compile pass                                                                            (b) Cumulative pass rate vs. per-case cost k.
 rate.
  Figure 6: Full-set head-to-head comparison on C to Rust (n = 300) and JS to TS (n = 150),
  restricted to the four head-to-head configurations (naı̈ve vs. DTV with one-shot vs. self-refine); the
  legend is shared with main-body Figure 2 (BoN-N and S* entries do not appear in this figure). (a)
  Cost-rate scatter: DTV/self-refine occupies the upper-left region (low cost, high pass rate) on both
  tasks. (b) Cumulative pass rate vs. per-case cost: DTV exhibits the early-rise effect on both tasks and
  a continued-rise pattern on JS to TS that distinguishes it from naı̈ve’s plateau (Section 4.1).


 Table 5: Pass rate, average tokens-per-case ratio k, and tokens-per-pass (mean with 95% bootstrap
 CI) for all five configurations on both tasks. Per-case paired token-cost statistics on the both-pass
 subset are reported separately in Appendix M.6.
                  Task                                    Configuration                        Pass                     Pass rate            Avg. k                Tokens / pass [95% CI]
                  C → Rust (n =300)                       naive/one-shot                 49/300                                  16.3%          1.55                                      360 [309,415]
                                                          naive/self-refine             217/300                                  72.3%          7.18                                   1903 [1548,2339]
                                                          DTV/one-shot                  141/300                                  47.0%          2.00                                      596 [499,714]
                                                          DTV/self-refine               246/300                                  82.0%          5.28                                   1654 [1345,1990]
                  JS → TS (n =150)                        naive/one-shot                      7/150                               4.7%          1.10                                      435 [310,567]
                                                          naive/self-refine                  50/150                              33.3%         11.48                                   1648 [1071,2497]
                                                          DTV/one-shot                       32/150                              21.3%          2.77                                      715 [547,960]
                                                          DTV/self-refine                    69/150                              46.0%         10.11                                   2103 [1470,2856]



  J.3                   Cost-matched baseline grid

 Table 6 reports the full pass-rate and per-case token-cost breakdown for the cost-matched baseline
 grid summarized in Section 4.1. The grid compares the head-to-head configurations with best-of-N
 for N ∈ {1, 2, 4, 8, 16, 32} and S* on the cost-matched subsets (n = 200 for C to Rust, n = 100 for
 JS to TS); naı̈ve/self-refine and DTV/self-refine are repeated here at the subset n for direct comparison
 against the BoN and S* columns.

  J.4                   Paired comparisons (compile pass)

 Table 7 reports the paired compile-pass comparisons used to separate DTV’s gains from case-level
 difficulty variation.

  J.5                   Functional guardrail (C to Rust)

 The pass-rate metric in the main body uses compilation as the primary criterion because compilation
 is the dense in-loop verifier signal that the DTV controller consumes. To rule out the possibility that
 DTV’s compile-rate gains are achieved at the expense of behavioral correctness (for example, by
 patching function bodies with stubs that compile but fail differential tests), we run a paired functional
 analysis on the matched outer-loop setting: naı̈ve/self-refine versus DTV/self-refine. A case is a full
 success only if the Rust translation compiles and matches the C source on all differential test inputs;
 the per-case test pass rate is the fraction of differential tests passed and is set to zero on compilation
 failure. Table 8 reports the marginal outcomes per configuration, with the conditional column giving
 full-success rate among cases that compile.


                                                                                                       21
Table 6: Pass rate, average token cost per case, tokens per successful pass, and per-case token cost
relative to DTV/self-refine for the cost-matched baseline grid on the n=200 C-to-Rust and n=100
JS-to-TS subsets. The × ratio is per-case tokens divided by DTV/self-refine’s per-case tokens on
the same task. naı̈ve/self-refine and DTV/self-refine are repeated here at the subset n for direct
comparison.
 Task                  Configuration         Pass    Pass rate    Tok/case    Tok/pass     vs DTV (tok/case)
 C → Rust (n =200)     naive/self-refine   152/200        76.0%      5266           1798              1.51×
                       DTV/self-refine     169/200        84.5%      3489           1805              1.00×
                       naive/BoN-1          31/200        15.5%       737            377              0.21×
                       naive/BoN-2          42/200        21.0%      1437            476              0.41×
                       naive/BoN-4          58/200        29.0%      2772            928              0.79×
                       naive/BoN-8          73/200        36.5%      5154           1880              1.48×
                       naive/BoN-16         84/200        42.0%      9574           2573              2.74×
                       naive/BoN-32         89/200        44.5%     17866           3445              5.12×
                       S*/n8r3             151/200        75.5%     16563          11551              4.75×
 JS → TS (n =100)      naive/self-refine    37/100        37.0%     15105          1740               1.09×
                       DTV/self-refine      50/100        50.0%     13815          2185               1.00×
                       naive/BoN-1           7/100         7.0%      1186           435               0.09×
                       naive/BoN-2           7/100         7.0%      2377           435               0.17×
                       naive/BoN-4           7/100         7.0%      4727           435               0.34×
                       naive/BoN-8           7/100         7.0%      9509           435               0.69×
                       naive/BoN-16          7/100         7.0%     18871           435               1.37×
                       naive/BoN-32          7/100         7.0%     37664           435               2.73×
                       S*/n8r3              33/100        33.0%     27388          9751               1.98×


Table 7: Paired McNemar tests on per-case compile pass for the four canonical comparisons on both
tasks. The Only-A and Only-B columns report the discordant counts. All comparisons in the main
text are paired (same case identifiers under the same dataset and budget).
 Task         Baseline (A)        DTV (B)              n     Only A    Only B       Diff (pp)   McNemar p
 C → Rust     naive/one-shot      DTV/one-shot       300          13         105       +30.7        < 0.001
              naive/self-refine   DTV/self-refine    300          21          50        +9.7        < 0.001
 JS → TS      naive/one-shot      DTV/one-shot       150           1         26        +16.7        < 0.001
              naive/self-refine   DTV/self-refine    150           7         26        +12.7          0.001


The marginal view shows DTV’s conditional full-success rate (10.2%) below naı̈ve’s (13.0%), but
this conditional comparison conditions on different sets of cases: DTV compiles 246 of 300 cases
versus naı̈ve’s 217, so DTV’s denominator includes harder cases that naı̈ve cannot compile at all.
The cleanest way to remove this selection effect is to restrict to the cases where both configurations
produce a compiling translation. On this matched compile set (Table 9, n = 195), DTV’s full-success
rate is 10.8% versus naı̈ve’s 12.3% (-1.54 pp; McNemar p = 0.549), and its average per-case
differential test rate is 29.6% versus naı̈ve’s 32.8% (-3.18 pp, 95% bootstrap CI [−7.49, +1.14]).
Neither difference reaches significance and the bootstrap CI straddles zero, so on cases where both
methods produce a compiling target, DTV’s behavioral correctness is statistically indistinguishable
from naı̈ve’s.
The full-sample paired view (Table 10) confirms this conclusion across all 300 cases. The discordant
counts are 11 (only naı̈ve) versus 8 (only DTV), giving a difference of -1.00 pp on full success
(McNemar p = 0.648); the paired test pass rate difference is -1.5 pp with a 95% bootstrap CI
of [−5.2, +2.3] pp. Together, the both-compile and full-sample paired analyses rule out a hidden
behavioral regression: DTV’s compile-rate gains are not paired with worse differential correctness.

K    Cross-model robustness
This appendix presents the cross-model robustness analysis referenced in Section 4.1. We compare
DTV/self-refine against naı̈ve/self-refine using Qwen3 and Gemma4 as generators on both translation
tasks, holding RQ1’s metric hierarchy fixed: pass rate as the headline metric, with C-to-Rust
differential testing as the functional guardrail. Across all four model-task pairs, DTV/self-refine


                                                     22
Table 8: Marginal functional outcomes for naı̈ve/self-refine and DTV/self-refine on C to Rust
(n = 300). Compile is the share of cases whose Rust translation compiles, the average test pass rate
is the per-case fraction of differential tests passed (zero on compilation failure) averaged over all n
cases, and the conditional column gives the full-success rate among the cases that compile.
                Configuration                Compile      Avg. test pass rate   Full | compile
                naı̈ve/self-refine    217/300 (72.3%)                 23.9%            13.0%
                DTV/self-refine       246/300 (82.0%)                 22.4%            10.2%



Table 9: Both-compile paired comparison on C to Rust, restricted to cases where both naı̈ve/self-refine
and DTV/self-refine produce a compiling translation (n = 195). The full-success columns report
the share of these cases that pass all differential tests; the average rate column averages the per-case
fraction of differential tests passed, with a 95% paired-bootstrap CI on the difference.
            n   naı̈ve full    DTV full      Full diff (pp)   McNemar       Avg. rate diff [95% CI]
          195       12.3%            10.8%           -1.54    p = 0.549     -3.18 pp [−7.49, +1.14]



reaches a higher pass rate than naı̈ve/self-refine across the lower portion of the budget range (Figure 7);
at the per-case budget cap of k = 16, DTV exceeds naı̈ve on three pairs (+8.5 pp, +13.0 pp, +8.0 pp)
and reduces normalized cost on three (-23.6%, -11.5%, -14.5%). The fourth pair exhibits a budget-
dependent crossover discussed below.
On Gemma4 C to Rust, the comparison is budget-dependent (Figure 7, left panel). DTV/self-refine
reaches a higher pass rate than naı̈ve/self-refine across the lower-to-mid budget range, with a peak
lead of +10.5 pp at k ≈ 4; the curves cross near k ≈ 7 and naı̈ve/self-refine continues to climb past
DTV through the cap, ending at 93.5% versus 86.0%. We attribute the erosion of DTV’s early-rise
advantage to the high baseline pass rate on this pair: with naı̈ve/self-refine already passing 93.5% of
cases at the cap, the residual hard cases provide fewer opportunities for DTV’s verify-and-rollback to
convert into marginal passes than naı̈ve’s outer-loop retry produces over the same total budget. The
per-case failure modes that drive the cap-budget gap, and whether they fall outside the scope of DTV’s
structure-aware rollback, are part of the per-case analysis in Section 4.3. Behavioral correctness on
the differential-testing guardrail is unchanged on this pair (15.00% vs 15.00% in functional pass rate;
Appendix K.3).
On JS to TS, both model families show DTV pass-rate gains at the budget cap (+13.0 pp on Qwen3,
+8.0 pp on Gemma4) at reduced normalized cost (-11.5% and -14.5% respectively). Across the four
pairs, DTV’s gains on both pass rate and per-case cost generalize across model families: on three
pairs DTV exceeds naı̈ve at the budget cap in both metrics, and across the lower portion of the budget
range DTV exceeds naı̈ve in pass rate on all four. The single cap-budget exception is concentrated on
the pair where the baseline is highest (Gemma4 C to Rust at 93.5%).


K.1   Marginal stats

Table 11 reports per-cell pass rate, average per-case k, and tokens per pass for naı̈ve/self-refine and
DTV/self-refine on both tasks. Each Gemma cell uses the corresponding RQ1 sample list (n = 200
for C to Rust, n = 100 for JS to TS); Qwen cells are restricted to the same prefixes for paired
cross-model comparison, so the matched case set within each (model, task) cell has the same case
identifiers across configurations.


K.2   Paired comparisons

Within each cell, both methods see the same case identifiers under the same per-case budget cap,
so paired McNemar tests on per-case pass directly isolate method-attributable gain from case-level
difficulty variation (Table 12). To separate per-success efficiency from marginal pass-rate composition
differences, Table 13 restricts to the subset of cases where both methods produce a passing translation
and compares average k on that matched both-pass subset.


                                                        23
Table 10: Full-sample paired comparison on full-functional success for naı̈ve/self-refine versus
DTV/self-refine across all 300 C-to-Rust cases. Only-A and Only-B count cases where exactly one
configuration achieves full success. The test rate diff is the paired difference in average test pass rate
(in percentage points) with a 95% bootstrap CI.
            Only naı̈ve                 Only DTV     Diff (pp)                        McNemar                   Test rate diff (pp) [95% CI]
                                   11           8        -1.00                           p = 0.648              -1.5 [−5.2, +2.3]

                Qwen3-4B naive/SR              Qwen3-4B DTV/SR                                       Gemma-4-E4B naive/SR        Gemma-4-E4B DTV/SR
                            100         C to Rust (n=200)                                            100         JS to TS (n=100)
                                                                               -7.5 pp
                             80                                               +8.5 pp                 80
            Pass rate (%)




                                                                                     Pass rate (%)
                             60                                                                       60                                                  +8.0 pp
                                                                                                                                                         +13.0 pp
                             40                                                                       40


                                                          budget cap (k=16)




                                                                                                                                     budget cap (k=16)
                             20                                                                       20
                              00         5      10      15              00        5                                         10      15
                                                  Average k = tokens / source tokens
Figure 7: Cross-model cumulative pass rate vs. normalized per-case cost k for naı̈ve/self-refine and
DTV/self-refine on both tasks. DTV exceeds naı̈ve across the lower budget range on all four pairs; at
the budget cap, DTV remains ahead on three pairs, while on Gemma4 C to Rust the curves cross near
k ≈ 7 and naı̈ve overtakes (behavioral correctness preserved; Appendix K.3).


K.3    Functional guardrail (C to Rust)

Mirroring RQ1’s functional guardrail (Appendix J.5), we report differential-testing outcomes on
both C-to-Rust cells to verify that DTV’s pass-rate change on each cell does not reflect a substantive
behavioral-correctness loss. Note that the Qwen functional values reported here are restricted to
the Gemma-matched 200 ids; the full-300 Qwen functional view is in RQ1 (Appendix J.5) and is
consistent in sign and magnitude with the values reported here.
On the matched 200 ids, naı̈ve/self-refine on Qwen3 produces 11.50% full-functional success and
DTV/self-refine 9.50% (-2.0 pp; McNemar p = 0.424). The marginal difference is small in absolute
terms (4 cases out of 200) and consistent with the n.s. RQ1 result on the full 300 set; we therefore do
not interpret it as a substantive behavioral-correctness loss.
On Gemma4 C to Rust, the marginal full-functional success rate is identical between naı̈ve/self-refine
and DTV/self-refine (15.00% versus 15.00%, exact tie; McNemar p = 1.000). DTV’s compiling
pool is smaller than naı̈ve’s by 15 cases (170 versus 185), but the conditional full-success rate within
DTV’s compiling pool is higher than naı̈ve’s (17.65% versus 16.22%), suggesting that the cases DTV
does compile are more likely to also pass differential tests. Aggregating both views, DTV’s pass-rate
regression on this near-saturation cell does not coincide with a behavioral-correctness regression; on
the cases DTV does compile, behavioral pass-through is in fact slightly higher than naı̈ve’s, indicating
that the lost compiles concentrate among translations whose compile-pass-but-test-fail status would
not have been detectable by the in-loop oracle alone.

L     RQ2 detailed results
This appendix complements the main-body RQ2 results (Section 4.2) with the full per-configuration
cost breakdown, paired statistical tests against the DTV-full baseline, and an outer self-refine rescue
accounting that decomposes inner-loop and outer-loop contributions to final pass rate.

L.1   Cost breakdown

Table 15 reports the full per-configuration cost breakdown underlying the compact RQ2 summary in
Section 4.2. The Tokens/pass column reports the mean tokens consumed on cases that compile-pass


                                                                                    24
Table 11: Per-cell pass rate, average per-case k, and tokens per pass for naı̈ve/self-refine and DTV/self-
refine on both tasks. k is normalized in each model’s own tokenizer; failed (including OOM and
timeout) cases are counted at k = 16.
 Cell                                   Strategy              Pass     Pass rate   Avg. k      Tokens / pass
 Qwen3-4B × C → Rust (n =200)           naive/self-refine   152/200        76.0%        6.77           1798
                                        DTV/self-refine     169/200        84.5%        5.17           1805
 Gemma-4-E4B × C → Rust (n =200)        naive/self-refine   187/200        93.5%        5.91           3327
                                        DTV/self-refine     172/200        86.0%        5.99           3024
 Qwen3-4B × JS → TS (n =100)            naive/self-refine    37/100        37.0%    10.96              1740
                                        DTV/self-refine      50/100        50.0%     9.70              2185
 Gemma-4-E4B × JS → TS (n =100)         naive/self-refine    50/100        50.0%        9.87           3515
                                        DTV/self-refine      58/100        58.0%        8.43           3692



Table 12: Paired McNemar tests on per-case pass within each cell (same case identifiers under naı̈ve
vs. DTV). Discordant counts: “Only naı̈ve” = naı̈ve passes and DTV does not; “Only DTV” = DTV
passes and naı̈ve does not.
         Cell                           n    Only naive     Only DTV        Diff (pp)     McNemar p
         Qwen3-4B × C → Rust          200              15             32        +8.5      0.019
         Gemma-4-E4B × C → Rust       200              19              4        -7.5      0.003
         Qwen3-4B × JS → TS           100               6             19       +13.0      0.015
         Gemma-4-E4B × JS → TS        100              11             19        +8.0      0.200




with a 95% bootstrap CI, mirroring the reporting convention of Appendix J.2. DTV-full’s per-success
cost (1694) is higher than each of the three ablations’ (1412, 1437, 1173); the gap reflects the
additional in-loop verification and structured-recovery work DTV-full performs on cases that succeed.
At the per-case granularity at which the budget is actually allocated, DTV-full nevertheless converts
more of the budget into passing translations (the Avg. tokens column) than two of the three ablations.


L.2     Paired ablation comparisons

Table 16 reports paired McNemar tests for each ablation against the DTV-full baseline on three
metrics. Within each row, both configurations see the same case identifiers, so the discordant counts
(Only-A: baseline-only pass; Only-B: ablation-only pass) directly attribute outcome differences to
the ablation rather than to case-level difficulty variation.
The compile-rate drops for detect-and-abort (-15.0 pp, p = 0.003) and no-feedback (-11.0 pp, p =
0.035) are paired-significant. The no-escalation drop (-6.0 pp, p = 0.263) is directionally consistent
with the other two but falls below the detectability floor at n = 100. Inner-1shot drops for detect-
and-abort (-30.0 pp) and no-feedback (-23.0 pp) are large enough to be detected at this sample size
(p < 0.001 and p < 0.001 respectively); no-escalation leaves inner-1shot unchanged (p = 1.000).
All three functional differences fall below the detectability floor and should be read alongside the
descriptive ordering reported in Section 4.2.


L.3     Outer self-refine rescue contribution

Outer self-refine compensates for inner-loop ablations by rerunning DTV with accumulated diagnostic
feedback in the prompt. Table 17 reports the rescue rate (cases recovered by outer retry as a fraction
of inner-1shot failures) for each configuration. Rescue rates fall in a 62–73% band across all four
configurations, indicating outer self-refine’s rescue capacity is roughly comparable across inner-loop
ablations. Consequently, the gap between inner-1shot and final compile rates (Table 17) reflects what
outer self-refine can compensate for rather than how the ablation interacts with the outer loop.


                                                    25
Table 13: Both-pass subset analysis: average k on the cases where both naı̈ve/self-refine and
DTV/self-refine produce a passing translation. This view isolates DTV’s per-success efficiency from
the marginal pass-rate composition difference reported in Table 11.
           Cell                            Both-pass n      naive avg. k    DTV avg. k         ∆k (%)
           Qwen3-4B × C → Rust                      137             3.54             2.95      -16.5%
           Gemma-4-E4B × C → Rust                   168             5.10             4.66       -8.7%
           Qwen3-4B × JS → TS                        31             2.54             3.39      +33.3%
           Gemma-4-E4B × JS → TS                     39             3.01             2.49      -17.2%


Table 14: Functional outcomes for naı̈ve/self-refine and DTV/self-refine on C to Rust under the
matched cross-model case set (n = 200 per model). Same metrics as RQ1’s functional guardrail
(Appendix J.5); the Qwen functional values here differ from the RQ1 appendix because RQ1 uses the
full n = 300 set while RQ2 restricts to the Gemma-matched first 200.
 Cell                      Strategy            Compile       Full success     Full | compile    McNemar p (full)
 Qwen3-4B × C → Rust       naive/self-refine   151/200    23/200 (11.50%)   23/151 (15.23%)     0.424
                           DTV/self-refine     168/200     19/200 (9.50%)   19/168 (11.31%)
 Gemma-4-E4B × C → Rust    naive/self-refine   185/200    30/200 (15.00%)   30/185 (16.22%)     1.000
                           DTV/self-refine     170/200    30/200 (15.00%)   30/170 (17.65%)



L.4     Trace walk-throughs: when escalation helps and hurts

We examine two paired cases illustrating the mechanism underlying the -6.0 pp final-pass-rate gap
between DTV-full and no-escalation. The runs use temperature sampling rather than greedy decoding,
so paired-trace differences are mechanistic rather than deterministic counterfactual.

Escalation rescues a non-local mutability error. Case s368372837 (only-A: DTV-full passes,
no-escalation fails) is a non-local error: rustc reports cannot assign twice to immutable
variable sold at a mutation site whose diagnostic help points back to an earlier let mut sold
binding committed several statements before the mutation. DTV-full attempts three statement-scope
rollbacks to the same prefix length, each producing the same diagnostic; the diagnostic-anchor visit
count then triggers escalation to block scope, which truncates the committed prefix back through the
offending binding region. Regeneration from the rolled-back prefix produces a passing verify and
commit, and the case finishes in 652 generated tokens. No-escalation on the same case is restricted
to statement scope: it cycles through statement-rollback and repair under the same diagnostic until
the per-case budget cap is reached at 3600 tokens, without ever reaching outer-loop verification.
Across the no-escalation cohort, 10 cases exhaust their budget entirely within inner-loop activity
(zero recorded outer rounds), consistent with statement-only rollback failing to make progress on
non-recoverable diagnostics.

Escalation discards a useful prefix. Case s126370263 (only-B: no-escalation passes, DTV-full
fails) shows the opposite failure mode. DTV-full repeatedly attempts patch-based repair on a local
if/else expression; after several stalls the controller escalates to function-scope rollback, which
truncates the committed prefix to length zero and forces regeneration from scratch. The regenerated
trajectory does not converge within the budget. No-escalation on the same case applies a single
statement-scope rollback to fix an unrelated macro syntax error, commits, and passes on the first outer
round.

Aggregate caveat. These two cases illustrate the canonical positive and negative interactions
between rollback scope and the regeneration trajectory, but they do not generalize mechanically to
all 20 paired identity flips. Of the 13 only-A cases, DTV-full uses non-statement rollback on 7; the
remaining 6 succeed without scope widening in DTV-full and fail under no-escalation, indicating
that escalation policy also affects generation trajectories indirectly (e.g., function-scope rollback
resets the feedback mechanism from patch-based to inline continuation, exposing the model to a
different repair-prompt format). Of the 7 only-B cases, 5 show DTV-full taking non-statement
rollback (consistent with over-aggressive scope widening discarding useful prefix); the other 2 show
no scope-widening at all, suggesting stochastic trajectory variation under temperature sampling.


                                                     26
Table 15: Per-configuration pass rate, average tokens per case, and Tokens/pass with 95% bootstrap
CI on the first 100 C-to-Rust cases. The Avg. tokens column is the per-case mean over all cases
(failures hit the budget cap); the Tokens/pass column is the mean over cases that compile-pass with a
paired bootstrap CI.
            Configuration                    Pass rate       Avg. tokens     Tokens / pass [95% CI]
            DTV-full                  85/100 (85.0%)               3580             1694 [1164,2405]
            DTV-no-feedback           74/100 (74.0%)               4138             1412 [1157,1691]
            DTV-no-escalation         79/100 (79.0%)               3623             1437 [1025,2000]
            DTV-detect-and-abort      70/100 (70.0%)               4417              1173 [937,1416]


Table 16: Paired McNemar tests on per-case compile, inner-1shot, and functional pass for each
ablation against the DTV-full baseline (n = 100 paired cases). Only-A: baseline-only pass; Only-B:
ablation-only pass. With n = 100, McNemar can reliably detect effects of approximately 10 pp or
larger; differences below this floor with non-significant p-values should be read as point estimates
rather than null effects.
 Comparison                         Metric                     Only-A      Only-B    n    Diff (pp)   McNemar p
 DTV-full vs DTV-no-feedback        Compile (HEADLINE)             17           6   100      -11.0    0.035
 DTV-full vs DTV-no-feedback        Inner-1shot                    29           6   100      -23.0    < 0.001
 DTV-full vs DTV-no-feedback        Functional (guardrail)          6           4   100       -2.0    0.754
 DTV-full vs DTV-no-escalation      Compile (HEADLINE)             13           7   100       -6.0    0.263
 DTV-full vs DTV-no-escalation      Inner-1shot                    17          17   100       +0.0    1.000
 DTV-full vs DTV-no-escalation      Functional (guardrail)          7           2   100       -5.0    0.180
 DTV-full vs DTV-detect-and-abort   Compile (HEADLINE)             19           4   100      -15.0    0.003
 DTV-full vs DTV-detect-and-abort   Inner-1shot                    34           4   100      -30.0    < 0.001
 DTV-full vs DTV-detect-and-abort   Functional (guardrail)          4           2   100       -2.0    0.688



M     RQ3 detailed results

This appendix complements the main-body RQ3 results (Section 4.3) with the fix-shape classifier
algorithm, the full fix-shape breakdown including UNKNOWN counts and the alternative Rfinal
classification, the per-error-code rescue rate, the shared-code ratio distribution underlying the on-
rescued mechanism claim, and the fix-shape transfer of the rescued cohort from one-shot to self-refine.

M.1    Fix-shape classifier algorithm

The fix-shape classifier introduced in Section 4.3 labels each naı̈ve R1-failure case by the shape of the
edit that naı̈ve’s R2 (its repair attempt) actually attempted, computed mechanically from the line-level
diff between R1 and R2. No human labels enter the classification.
For each naı̈ve case where round 1 fails, let R1 denote naı̈ve’s first-attempt code and R2 its second-
attempt code. Let E denote the set of R1 line numbers reported as errors in the diagnostic block
fed back to round 2; for C to Rust the line numbers are extracted from rustc’s primary span
markers (- -> program.rs:L:C), and for JS to TS from tsc’s and ESLint’s primary error markers
(- LL:C: error:). Let C denote the set of R1 line numbers that R2 modified, computed from
difflib.SequenceMatcher opcodes: replace and delete chunks mark every R1 line in the chunk;
insert chunks mark the R1 line immediately after the insertion point (or line 1 if the insertion is at the
top). Let nR1 denote the number of R1 lines.
The four-class label and a sub-reason for transparency are assigned by Algorithm 2, with the first
matching rule winning.
The 0.5 rewrite threshold is fixed across both tasks and across model families. UNKNOWN is
reported separately and excluded from hierarchy claims because the fix shape is not determined
by the diff alone in those sub-cases; the headline ordering in Section 4.3 (LOCAL ≥ MIXED ≥
NONLOCAL) is read from the three resolved classes.
The primary classification (mode A) uses R2 as defined above. An alternative classification (mode B)
uses Rfinal , the round of naı̈ve’s outer self-refine trace that ultimately compiled, in place of R2 , and is


                                                      27
Table 17: Outer self-refine rescue accounting: rescued cases (final compile − inner-1shot compile) as
a fraction of inner-1shot failures, for each configuration. The rescue rate band (62.5–73.2%) indicates
that outer self-refine’s rescue capacity is roughly independent of which inner mechanism is ablated.
          Configuration              Inner-1shot        Final compile   Rescued     Rescue rate
          DTV-full                44/100 (44.0%)    85/100 (85.0%)          41/56          73.2%
          DTV-no-feedback         21/100 (21.0%)    74/100 (74.0%)          53/79          67.1%
          DTV-no-escalation       44/100 (44.0%)    79/100 (79.0%)          35/56          62.5%
          DTV-detect-and-abort    14/100 (14.0%)    70/100 (70.0%)          56/86          65.1%


Algorithm 2 Fix-shape classifier (mode A). Given the modified line set C, the error line set E, and
the R1 length nR1 , label the case as LOCAL, NONLOCAL, MIXED, or UNKNOWN.
Require: nR1 , E, C
 1: if nR1 = 0 then
 2:    return UNKNOWN {EXTRACT FAIL}
 3: else if C = ∅ then
 4:    return UNKNOWN {NO OP: R2 produced no diff against R1 }
 5: else if |C|/nR1 > 0.5 then
 6:    return UNKNOWN {REWRITE: R2 rewrote the majority of R1 }
 7: else if E = ∅ then
 8:    return UNKNOWN {NO ERROR LINES: no extractable line numbers}
 9: else if C \ E = ∅ then
10:    return LOCAL {every R2 edit lands on an R1 error line}
11: else if C ∩ E = ∅ then
12:    return NONLOCAL {no R2 edit lands on an error line}
13: else
14:    return MIXED {partial overlap}
15: end if



restricted to cases where naı̈ve eventually passes; mode B is reported alongside mode A in Table 2.
The two modes agree on 88.1% of mode-B-eligible cases on C to Rust (loose: 91.2%, n=159) and
84.1% on JS to TS (loose: 95.5%, n=44); the loose agreement collapses LOCAL and MIXED into a
single ANCHORED bucket.

M.2    Fix-shape full breakdown

Table 18 reports the complete fix-shape rescue rate including the UNKNOWN bucket and the
alternative Rfinal classification (mode B), complementing the slim main-body view in Table 2. The
universe is naı̈ve R1-failure cases (rescued plus both-fail; n = 230 on C to Rust under mode A,
n = 141 on JS to TS under mode A). The UNKNOWN row sits at 57.9% on C to Rust (n = 19) and
20.0% on JS to TS (n = 5); we exclude UNKNOWN from the LOCAL ≥ MIXED ≥ NONLOCAL
hierarchy claim because its constituent sub-reasons (no-op and rewrite) describe undetermined fix
shapes rather than a coherent shape class.

Table 18: Full fix-shape rescue rate on naı̈ve R1-failure cases. Columns A use R2 as the repair anchor
(primary classification, matching the main-body Table 2); columns B use Rfinal from naı̈ve-eventually-
pass cases (alternative anchor). Cells report rescue rate (rate-eligible n); ∗ marks bins below the
underpowered threshold of 5 cases.
                 Fix-shape    C → Rust A     C → Rust B        JS → TS A     JS → TS B
                 Local        50.0% (12)     100.0% (2*)       29.3% (58)     48.0% (25)
                 Mixed        43.5% (168)    50.4% (129)       11.9% (67)     37.5% (16)
                 Nonlocal      29.6% (27)     40.0% (10)       0.0% (2*)         – (0)
                 Unknown       57.9% (19)     75.0% (16)       20.0% (5)      0.0% (2*)

The NONLOCAL bucket on JS to TS is underpowered. Mode A counts 5 NONLOCAL cases out of
141 R1-failure cases on JS to TS, with 2 cases entering the rescue-rate denominator; mode B counts


                                                   28
0 NONLOCAL cases (n = 0). Below the underpowered threshold of 5 cases, the rescue-rate point
estimate is reported with a ∗ marker in Table 2 and is not used to claim a NONLOCAL gap on JS
to TS in Section 4.3; the LOCAL versus MIXED gap on JS to TS (29.3% vs 11.9%, mode A) is
well-powered (n = 58 and n = 67 respectively) and supports the LOCAL ≥ MIXED edge of the
hierarchy on this task.

M.3     Per-error-code rescue rate

The fix-shape hierarchy in Section 4.3 categorizes cases by the shape of naı̈ve’s repair attempt; we
additionally report per-error-code rescue rate as a complementary view organized by the diagnostic
that broke naı̈ve’s R1 (Table 19). For each error code that appears on at least 5 naı̈ve R1-failure cases,
we report the number of such cases, the number where DTV/one-shot rescues, and the rescue rate. A
case enters the denominator for every distinct error code that appears on its R1 diagnostic block.


Table 19: Per-error-code rescue rate on naı̈ve R1-failure cases, top 6 codes by R1-failure prevalence
on each task. A case may enter the denominator for multiple codes when its R1 diagnostic block
reports several. Codes with fewer than 5 R1-failure cases are excluded.
 Task       Code                                                  Naive-fail n   DTV rescued   Rescue rate
 C → Rust   E0599                                                          79             43        54.4%
            E0308                                                          66             22        33.3%
            E0277                                                          61             24        39.3%
            E0425                                                          49             15        30.6%
            E0433                                                          14              4        28.6%
            E0384                                                           8              4        50.0%
 JS → TS    @typescript-eslint/typedef                                    118             23        19.5%
            @typescript-eslint/explicit-function-return-type               58              7        12.1%
            TS2339                                                         43              1         2.3%
            TS2554                                                         28              1         3.6%
            TS1192                                                         21              0         0.0%
            TS1259                                                         16              0         0.0%


On C to Rust, the highest rescue rates concentrate on borrow-check and type-mismatch families
(E0599 method resolution at 54.4%, E0384 immutable-binding violations at 50.0%) where the diag-
nostic anchors a concrete fix on the error line. The lower-rescue families (E0425 unresolved name at
30.6%, E0433 unresolved trait at 28.6%) typically require a non-local edit at an import or declaration
upstream of the error line. On JS to TS, the dominant code is @typescript-eslint/typedef
(the missing-type-annotation rule under our zero-typedef policy) at 19.5%; the lower-rescue codes
TS2339, TS2554, TS1192, TS1259 are concentrated on cases where the correct annotation depends
on cross-program usage rather than on a fact local to the variable declaration. The per-code ordering
is consistent with the fix-shape hierarchy: codes whose canonical fix is local-cause and local-fix
rescue at higher rates, and codes whose canonical fix lives upstream rescue at lower rates.

M.4     Shared-code edit-concentration ratio

Figure 8 reports the per-case distribution of the shared-code edit-concentration ratio used in the
Section 4.3 mechanism analysis on rescued cases. The universe is the subset of rescued cases where
DTV’s inner verifier fired and structure-aware rollback intervened (DTV/one-shot passes after at
least one inner-loop rollback), intersected with the shared-code subset (DTV inner-loop error codes
and naı̈ve R1 error codes have non-empty intersection). For each case in this universe, the ratio is
computed as the number of distinct DTV inner-loop diagnostic emissions on the shared codes divided
by the number of distinct naı̈ve R1 diagnostic emissions on the same codes; a ratio below 1 indicates
DTV emits fewer per-shared-code verify diagnostics than naı̈ve accumulated as R1 errors on the
same codes.
The C-to-Rust distribution is centered at parity (median 1.00, with first and third quartiles Q1 =1.00
and Q3 =1.50, mean 1.19); the JS-to-TS distribution is shifted left of parity (median 0.50, Q1 =0.23,
Q3 =1.00, mean 0.71). Both distributions sit at or below 1 at the median, supporting the Section 4.3
claim that DTV’s incremental work is concentrated on the same error codes naı̈ve’s R1 hit rather than
redirected to a different error class. The complementary both-fail comparison reinforces this view:
40.4% of C-to-Rust both-fail cases (n = 59 of 146) and 86.3% of JS-to-TS both-fail cases (n = 101


                                                   29
                                                                      Site-count ratio (B2 shared-code subset)
                                                          3


             DTV inner-loop / naive final, shared codes
                                                          2

                                                          mean=1.19
                                                          1                         med=1.00                                     ratio = 1
                                                                                                                                 (no shift)
                                                                                            mean=0.71
                                                                                                                     med=0.50

                                                          0               C Rust                          JS TS
                                                                           (n=57)                          (n=26)
Figure 8: Per-case distribution of the shared-code edit-concentration ratio on rescued cases where
DTV’s inner verifier fired and the DTV/naı̈ve code sets intersect. n = 57 on C to Rust and n = 26
on JS to TS. Ratios at or below 1 indicate DTV reaches rescue with at most as many per-shared-code
verify-and-rollback cycles as naı̈ve accumulated as R1 errors on the same codes.


of 117) have DTV’s inner-loop diagnostics intersecting naı̈ve’s R1 diagnostics, indicating that when
DTV does not pass, it is most often stuck on the same error codes that broke naı̈ve.

M.5     Paired round-of-pass statistics (self-refine)

Table 20 reports the paired round-of-pass statistics summarized in the Section 4.3 round-savings
claim. The both-pass subset includes only cases where both naı̈ve/self-refine and DTV/self-refine
reach pass on the matched case identifiers. The med ratio and mean ratio columns are over the
per-case naı̈ve rounds / DTV rounds; the e/s/l column reports the count of cases where DTV reaches
pass earlier, in the same outer round, or later than naı̈ve; ∆ is the per-case difference (naı̈ve − DTV)
in outer rounds; sign p uses the two-sided exact sign test on the discordant pairs. The right-shifted
ratio distributions (Q1 =1.00, Q3 =3.00on C to Rust; Q1 =1.00, Q3 =2.00on JS to TS) confirm the
round-savings effect is broad rather than driven by tail outliers; both sign tests reject equality and
both bootstrap CIs on the mean ratio exclude 1.0 (Table 20).


Table 20: Paired round-count statistics on the both-pass subset (matched naı̈ve/self-refine and
DTV/self-refine, same case identifiers).
 Task                                   n                     med ratio    mean ratio [95% CI]           e/s/l   ∆ mean      ∆ [95% CI]       Sign p
 C → Rust        196                                               2.00        2.06 [1.88, 2.27]    129/46/21       +1.22   [+0.94, +1.52]    < 10−19
 JS → TS          43                                               1.50        1.61 [1.38, 1.88]      24/15/4       +0.63   [+0.35, +0.93]    < 0.001



M.6     Both-pass token-cost analysis (self-refine)

The compile-pass paired analysis in Appendix J.4 establishes that DTV improves the binary outcome
(more cases compile). This subsection addresses the orthogonal question used in the Section 4.3
round-savings analysis: on the cases where both methods succeed, does DTV use more or fewer
tokens? Restricted to the both-pass subset of the matched naı̈ve/self-refine versus DTV/self-refine
comparison, Table 21 reports the per-case token-difference distribution (∆tok = DTV − naı̈ve in
tokens; negative favors DTV).


                                                                                               30
Table 21: Per-case token-difference distribution on the both-pass subsets of the matched naı̈ve/self-
refine versus DTV/self-refine comparison (∆tok = DTV tokens − naı̈ve tokens; negative favors DTV).
The DTV < / = / > naı̈ve columns report the number of cases where DTV uses fewer, equal, or more
tokens (the equal column captures cases where both methods pass on first attempt with identical token
counts). The trimmed mean drops the top 10% and bottom 10% of cases (the largest DTV-better and
DTV-worse outliers symmetrically) to expose tail-driven shifts in the arithmetic mean.
 Task        n    DTV < naive   DTV = naive   DTV > naive   Median ∆tok   Mean ∆tok   Trimmed mean
 C → Rust   196     133 (68%)        7 (4%)      56 (29%)          -208        -519            -297
 JS → TS     43      24 (56%)       5 (12%)      14 (33%)           -61        +220            -109



Both-pass medians favor DTV on both tasks. On C to Rust (n = 196), DTV uses fewer tokens
than naı̈ve on 133 of the both-pass cases (67.9%), naı̈ve uses fewer on 56 (28.6%), and the median
paired difference is -208 tokens (sign test p < 0.001). On JS to TS (n = 43), DTV is the winner on
24 cases (55.8%) versus 14 for naı̈ve (32.6%), with a median paired difference of -61 tokens (sign
test p = 0.143, underpowered at this sample size). Both medians point in the same direction: on the
typical case where both methods pass, DTV uses fewer tokens.

The mean disagrees with the median on JS to TS, driven by an asymmetric tail. On C to Rust
the arithmetic mean (-519 tokens) agrees with the median direction; on JS to TS the mean is +220
tokens, opposite of the median. Inspecting the tails explains the discrepancy. Among the JS-to-TS
both-pass cases, the top 4 (10%) where DTV uses most extra tokens contribute a cumulative +20875
tokens, while the bottom 4 where DTV saves most contribute only -7604 tokens (a 2.75× asymmetry
favoring the DTV-bad tail). After symmetrically trimming 4 cases from each tail, the mean over the
remaining 35 cases swings to -109 tokens, recovering the median direction. The C-to-Rust both-pass
distribution has the opposite tail shape: top-10% DTV-good cases cumulatively save -98903 tokens
versus top-10% DTV-bad cases costing +44106 tokens (0.45× in the opposite direction), so the
C-to-Rust mean is robust to trimming and stays negative (-297 tokens after the same symmetric
10%/10% trim).

Mechanism behind the JS-to-TS DTV-bad tail. The structure-aware rollback mechanism under-
lying this asymmetric tail is described in Section 4.3: it ties back to the same non-local fix-shape
boundary that lowers DTV’s per-case rescue rate.




                                                 31
