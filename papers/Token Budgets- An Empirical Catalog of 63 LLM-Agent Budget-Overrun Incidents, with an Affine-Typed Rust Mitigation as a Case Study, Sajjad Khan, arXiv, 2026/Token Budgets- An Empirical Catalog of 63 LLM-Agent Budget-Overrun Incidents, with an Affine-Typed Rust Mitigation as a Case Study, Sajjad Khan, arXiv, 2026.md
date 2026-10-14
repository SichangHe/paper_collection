                                                                                                                                                                                                                      1




                                        Token Budgets: An Empirical Catalog of 63 LLM-Agent
                                         Budget-Overrun Incidents, with an Affine-Typed Rust
                                                    Mitigation as a Case Study
                                                                                                                    Sajjad Khan



                                                                                                                               ✦
arXiv:2606.04056v1 [cs.SE] 2 Jun 2026




                                        Abstract—Context. LLM-agent budget overruns are a documented production                    at 0/30 overshoot, so the affine discipline’s distinguishing value is not the single-
                                        failure class: a single retry loop can accumulate thousands of dollars on a                agent cap outcome but non-bypassability under operator error in multi-agent
                                        deployer’s account before an operator notices. The mitigations that have emerged           delegation: the M-delegation-fanout race documented in 11 catalog incidents is
                                        track spend at runtime; in-process integrity properties—no aliasing of a cost-             rejected by the borrow checker at compile time, while the same pattern under
                                        bearing value, no double-spend, no use-after-delegation—are enforced, if at all,           asyncio overshoots 30/30 while three disciplined alternatives (including a
                                        by ad-hoc wrappers rather than by the type system.                                         properly locked Python counter) overshoot 0/30 — a deterministic mechanism
                                             Contribution. The central contribution is empirical: a documented catalog of          split, not a marginal effect. In the Agent-Contracts comparison at a discriminating
                                        63 confirmed production incidents drawn from 21 orchestration frameworks                   cap (B0 = 2,000 uc, claude-haiku-4-5) the Rust crate, the Python counter,
                                        across 2023–2026, each backed by a quoted GitHub issue, a maintainer or user               and Agent Contracts are at operational parity.
                                        statement, and (where reported) a documented dollar loss, organized into an                      Scope and cost. The static estimator reserves 4–6× actual cost; the
                                        eight-cluster failure taxonomy. The corpus is complemented by 47 supplementary             AdaptiveEstimator tightens this to 2.11× median and tokenizer-direct
                                        structural entries that document the budget-primitive-missing condition without            estimation to ∼1.0× at 939–1,749 ms per-spend latency, with the integrity
                                        themselves being user-reported incidents. The classification carries two-human             property preserved across all three. Reasoning models (OpenAI o-series,
                                        independent inter-rater reliability of Cohen’s κ = 0.837 on the full N = 113 four-         Anthropic extended-thinking, DeepSeek-R1) fall outside Proposition 1: providers
                                        class sample (and κ = 0.943 on the n = 79 rows both raters independently                   bill for hidden reasoning tokens not bounded by max_output_tokens
                                        marked confirmed).                                                                         (assumption A6), so for these models the approach is a defense-in-depth layer
                                            Mechanism. As one mitigation evaluated against this taxonomy, we build                 behind provider-side controls (reasoning_effort, thinking.budget_
                                        token-budgets, a 1,180-line Rust crate (no unsafe; the core Budget API                     tokens) rather than a primary cap.
                                        uses no Arc<Mutex<_») that operationalizes affine ownership so that cloning,
                                        double-spending, and using a budget after delegating it are compile errors in              Index Terms—empirical software engineering, failure catalogs, type systems,
                                        typed source rather than runtime hazards the operator must remember to avoid.              affine types, large language models, LLM agents, software reliability, cost control,
                                        The dollar cap itself is runtime arithmetic under estimator assumption A1; the             Rust
                                        affine layer supplies the in-program integrity that makes that arithmetic non-
                                        bypassable. The bounded quantity is the provider’s reported spend, conditional
                                        on charge-truthfulness (A7); the type system supplies bookkeeping integrity,               1    I NTRODUCTION
                                        not a stronger cost guarantee. We use affine rather than linear ownership
                                                                                                                                   LLM-agent budget overruns are a documented production failure
                                        deliberately: a dropped Budget can only under-spend, which is cap-safe, so
                                        the property claimed is non-duplication, not value-conservation. Structurally, the
                                                                                                                                   class. A retry loop that spends a few cents per attempt can, when
                                        affine mechanism targets the budget-primitive-missing pattern (frameworks with             no mechanism bounds cumulative cost, accumulate to thousands of
                                        no spend cap at all); the runtime cap bounds the other failure modes only at               dollars before an operator notices—with the dollar consequence
                                        the consequence level, so the crate is a structural fix for one pattern plus a             landing on the deployer’s account, not the framework’s. Section 2
                                        general spend bound, not a resolution of the full catalog. We treat the eight-way          catalogs 63 confirmed production incidents across 21 sub-projects
                                        mechanism partition as exploratory : independent cluster-assignment agreement              and 18 ecosystems (2023–2026), each with quoted maintainer or
                                        is moderate (Cohen’s κ = 0.44, N = 110, two raters), and the validated empirical           user evidence and (where reported) documented dollar losses. The
                                        labels are the four-class scheme (κ = 0.837). Binary-level cap-soundness on
                                                                                                                                   63-incident corpus is complemented by 47 supplementary catalog
                                        the running Tokio binary is left open (Conjecture 1), and the specification cross-
                                                                                                                                   entries that document the structural budget-primitive-missing
                                        checks we ship are consistency evidence in the artifact, not a proof.
                                                                                                                                   condition without themselves being user-reported overrun incidents:
                                             Evaluation. We evaluate against five production runtimes (LangGraph,
                                        CrewAI, AutoGen, an AgentGuard-style callback, LiteLLM proxy budgets) plus                 28 maintainer-acknowledged structural gaps, 14 feature requests
                                        concurrent work (Agent Contracts) across three providers and three catalog-                for budget primitives that do not exist in the framework, and 5
                                        derived workloads. A temperature-stratified live-API test (T ∈ {0.0, 0.3, 0.7, 1.0},       borderline cases. We treat the 63 confirmed incidents as the primary
                                        N = 160) reports zero cap violations and zero false refusals. On single-agent              evidence corpus throughout this paper; the 47 supplementary entries
                                        workloads a 4-line Python counter using the same estimator matches the crate               appear where they corroborate cluster-level mechanism recurrence
                                                                                                                                   and are clearly marked as supplementary rather than counted
                                        •   S. Khan is an independent researcher; MSc in Data Sci-                                 toward incident totals. The catalog establishes recurrence of the
                                            ence, University of the West of England, Bristol, UK. E-                               failure class across independently-developed projects; we explicitly
                                            mail: sajjadanwar200@gmail.com. ORCID: 0009-0007-8627-7682.                            do not claim it as a prevalence estimate, since the sampling frame
                                            Source code and full artifact bundle: https:// github.com/ sajjadanwar0/
                                            token-budgets.
                                                                                                                                   selects on the dependent variable (§2.1).
                                                                                                                                                                       2

                                                                             TABLE 1
                        What this work claims, the evidence it offers, and the scope of each claim. Each row keyed to its primary section.


 Claim                                          Evidence                                                       Scope / Limitation

 Integrity: no in-program aliasing of a         Nine trybuild compile-fail tests covering seven                Unconditional within the trust boundary of
 Budget.                                        distinct rustc diagnostics (E0277, E0308, E0382, E0505,        Budget::new. Binary-level cap-soundness on the
                                                E0507, E0599, E0624) against rustc 1.93.1 (§4.1).              running Tokio binary (Conjecture 1) is not formally
                                                Lightweight specification checking on a six-variable           proved in this paper; partial empirical evidence is
                                                conservation ledger cross-checks the abstract speci-           provided (Appendix B) but does not constitute a
                                                fication’s internal consistency (Appendix B reports            refinement proof. The binary-level claim should be
                                                the per-tool obligation counts and trust bases). The           read as open.
                                                specification checking is consistency evidence on the
                                                abstract specification, not an end-to-end source-to-
                                                binary proof; binary-level refinement is Conjecture 1,
                                                deliberately unproven.

 Cap-respecting: total provider-reported        Proposition 1 under its stated assumptions. 382 live-          Conditional on provider-stratified A1 (§3.4); em-
 spend ≤ initial cap (the bounded quantity is   API sessions across pre-flight, mid-loop, and self-            pirically validated. Default: byte-length for Ope-
 the provider’s reported usage; it coincides    terminated regimes (§4), zero overshoot; a calibrated          nAI/Groq (A1 holds 14/14 adversarial-synthetic
 with actual billed cost only under A7).        simulation extends this to 2,628 trials against per-call       cells); AnthropicEstimator for Anthropic
                                                token distributions fit to 30 real Anthropic runs (§4.5),      (2.0× safety margin; worst observed under-count
                                                reported as arithmetic correctness at scale rather than        1.88× on nested tool schemas; A1 harness re-
                                                as independent observations. The primary genuinely-            ports 30/30 across three tool-loop workloads; mar-
                                                independent evidence is a temperature-stratified sweep         gin sweep at {1.0, 1.5, 2.0, 2.5, 3.0}× on LANG-
                                                (T ∈ {0.0, 0.3, 0.7, 1.0}, N = 160, two production-            001, 0/75 overshoot, capital efficiency 60.1% →
                                                tier models, §4.5): 0 violations. At a discriminating          30.4%). A2 (overflow) is a deployment precondi-
                                                cap (B0 = 2,000 uc on claude-sonnet-4, §4.2),                  tion; budget-typed-cap lifts it to compile-time.
                                                0/30 overshoot vs. 30/30 baseline; at a sub-floor cap          A7 (actual_charge truthfulness) and A8 (rate-
                                                (B0 = 540 uc, §4.5), 0/30 pre-flight refusal vs. 30/30         stability) are operator-supplied trust assumptions
                                                baseline post-hoc overshoot (reported as refusal-to-           shared with every client-side cost-accounting mech-
                                                operate). Cap-sweep robustness: 30/30 across 10 caps           anism.
                                                (§4.5); multi-agent delegation: 0/60 aggregate, 0/180
                                                per-child (§4.5); forgetful-operator contrast (§4.3): racy
                                                30/30 vs. three disciplined alternatives 0/30 each.

 Catalog: 110 cases across 21 sub-projects, 8   Public artifact (the catalog CSV is in the public artifact).   Convenience sample of public GitHub issues; closed-
 mechanism clusters; 63 confirmed incidents,    Independent two-human IRR (an independent second               source platforms not represented. 8 mechanism clus-
 28 maintainer-acknowledged gaps, 14 fea-       rater; declared in §2.1): N = 113 rater-pair re-annotation     ters are post-hoc analytic and exploratory: indepen-
 ture requests, 5 borderline (§2.4).            gives κ = 0.837, 95% CI [0.745, 0.919], observed               dent cluster-assignment agreement is moderate (Co-
                                                agreement 0.894. Per-class κ: bf 0.858, bu 0.876, mf           hen’s κ = 0.44, 95% CI [0.34, 0.55], N = 110, two
                                                0.918, fr 0.727.                                               raters; §2.1), with cost-observability (κ = 0.78) and
                                                                                                               multimodal-cost-amplification (κ = 0.65) the two
                                                                                                               reliably-identified mechanisms. The IRR-validated
                                                                                                               labels are the four-class confirmed/gap/feature/bor-
                                                                                                               derline scheme (κ = 0.837). Prevalence claims
                                                                                                               anchored on 63 confirmed incidents, not the full 110.
                                                                                                               The budget-primitive-missing pattern (≈12 of 110
                                                                                                               rows, an exploratory grouping) upper-bounds the
                                                                                                               cases the primitive could have prevented in a Rust
                                                                                                               counterfactual; none of the 21 surveyed frameworks
                                                                                                               is written in Rust, though a small, production-
                                                                                                               used Rust agent ecosystem now exists (e.g. Rig,
                                                                                                               AutoAgents); we demonstrate the discipline on one
                                                                                                               such framework at low integration cost (§4.6, N=1:
                                                                                                               a hard session cap held across concurrent sub-agents
                                                                                                               on live traffic, with a compile-time guarantee that a
                                                                                                               sub-agent cannot duplicate or reuse its budget slice)
                                                                                                               but make no cross-framework deployment claim.
                                                                                                               The other 98 rows benefit from the runtime cap
                                                                                                               arithmetic only when re-implemented or wrapped.



    The mitigations that have emerged in response are uniformly                     layers (compile-time, software-layer, transport-layer).
runtime mechanisms. Frameworks add post-hoc budget alerts;
operators wire up software-layer circuit breakers like AgentGuard
to throw a BudgetExceeded once a spend threshold is crossed;                            The substructural-types literature has applied affine and linear
payment providers like ATXP move enforcement to the network                         ownership to consumable resources for decades (Move’s linear
layer, returning HTTP 402 when an agent’s wallet depletes. Each is                  digital assets [22], seL4’s capability tokens [23], the governor
useful as a second line of defense. None catches the spend before                   crate [24], Tokio semaphores [16]); the technique is established,
the API call commits: the agent either pays for the call and then                   the application to LLM dollar cost is new. Our discipline treats the
notices, or has the call rejected at the network boundary after the                 per-session cost capability as a Rust-affine value: delegation across
request is already in flight. Section 5 taxonomizes these into three                agent boundaries, composition of sub-budgets across tools, and
                                                                                    refund of unspent reservations all flow through the borrow checker.
                                                                                                                                                                       3

                                                                                 TABLE 2
   Guarantee map: which property is enforced where, with what status. Each property is enforced at exactly one layer (compile-time type system, runtime
arithmetic, or operator-validated calibration); the paper’s contribution is the combination, not a unified proof. The compile-time integrity layer does not prove a cost
     bound; the runtime arithmetic layer does, conditional on assumption A1. Binary-level behavior on the compiled binary is not established and not claimed.


        Property                                     Layer                       Proven?                            Trust assumption
        No aliasing of Budget                        Compile-time (bor-          Yes (9/9 trybuild tests, 7         rustc soundness
                                                     row checker)                rustc codes)
        No double-spend (use-after-move)             Compile-time (bor-          Yes (trybuild)                     rustc soundness
                                                     row checker)
        No use-after-split                           Compile-time (bor-          Yes (trybuild)                     rustc soundness
                                                     row checker)
        Capability  gating                    of     Compile-time (pri-          Yes (E0624 trybuild)               rustc + operator allowlist file
        Budget::new                                  vate fn + build.rs al-
                                                     lowlist)
        Binary-level cap-respecting                  Compiled binary             Not claimed (source-level          rustc codegen + Tokio scheduler
                                                                                 only; observed clean in all
                                                                                 experiments)
        Pre-flight cap check                         Runtime                     Trivially (one line of arith-      integer arithmetic in rustc
                                                     (checked_sub)               metic)
        Estimator soundness A1                       Operator-                   Empirical only (N = 178            operator must         re-calibrate     per
                                                     validated                   calibration+hold-out; up to        provider/model
                                                     calibration                 9.97× over-reservation on
                                                                                 adversarial hold-out)
        Output-cap honoring A6                       Provider behavior           Empirical only (fails on           provider         obeys     max_
                                                                                 reasoning models)                  completion_tokens
        Provider-reported            actual_         Operator-supplied           Not verified (§3.4; shared         provider usage truthful; operator
        charge                                       (provider behavior)         with LangSmith, LiteLLM,           reconciles vs. billing
                                                                                 AgentGuard)
        Streaming-cancellation usage accu-           Provider behavior           Not detected (canceled             client treats canceled-stream usage
        racy                                                                     streams may omit terminal          as advisory
                                                                                 usage event)
        Tokenizer-version stability                  Provider behavior           Not verified (calibration          operator pins tokenizer version in
                                                                                 is per provider/tokenizer;         build metadata
                                                                                 mid-session rotation invali-
                                                                                 dates A1)


1.1   Scope of the formal claim                                                      in estimator choice: the AdaptiveEstimator reduces me-
Compile-time integrity throughout this paper means what the Rust                     dian over-reservation to 2.11× at zero per-spend latency, and
borrow checker enforces on typed source code in a workspace                          tokenizer-direct estimation reaches ∼1.0–1.1× at the cost of
under #[forbid(unsafe_code)]: no aliasing of a Budget,                               939–1,749 ms mean per-spend roundtrip latency (§4.5). Operators
no double-spend, no use-after-split. The dollar cap is a separate,                   choose between the three based on their capital/latency profile;
runtime claim: spend reserves a conservative estimate via                            the compile-time integrity property is preserved across all three.
checked_sub and refuses any call that would exceed the cap                           Break-even is roughly: a prepay deployment whose working-
(§3.4). Binary-level cap-soundness on the running Tokio binary                       capital footprint exceeds about 25% of operating revenue should
(Conjecture 1, §3.5) remains open: compiler miscompilations,                         prefer the AdaptiveEstimator or tokenizer-direct; a post-pay
LLVM optimizations, and scheduler behavior could in principle                        deployment (reserved-not-held capital) can accept the static default
violate the cap on the binary even when the source is well-                          at zero operational cost. For deployments where capital efficiency
typed. The specification cross-checks (Appendix B) establish                         dominates over non-bypassability of the integrity layer, tokenizer-
internal consistency of the abstract specification, not a source-                    direct estimation or provider-side per-call caps (AWS Bedrock
to-binary refinement. Because a runtime counter with the same                        budget actions, OpenAI max_completion_tokens) are the
estimator already achieves the cap-respecting outcome on single-                     better choice. Table 3 gives the full decision matrix.
agent workloads (M2, §4.5), the affine discipline earns its place on
                                                                                     1.3    Contributions
a narrower claim: in-program integrity under operator error in multi-
agent delegation, isolated by the Forgetful-Operator experiment                      This paper makes one empirical contribution and two that ground
(§4.3).                                                                              and test it. Concretely, it contributes an empirically grounded, inter-
                                                                                     rater-validated taxonomy of LLM-agent budget-overrun failures
                                                                                     —to our knowledge the first to pair cross-framework incident
1.2   The capital cost of the default discipline                                     provenance with a validated coding scheme at this scale—and an
The default static byte-length+2.0× estimator reserves 4–6×                          evaluation of affine ownership as one mitigation for the delegation-
actual cost (6.20× mean, 2.51× median over-reservation across                        related budget-integrity failures that taxonomy surfaces. The
N = 5,190 per-call events; §4.5); on prepay accounts a deployment                    catalog is the result we ask reviewers to weigh; the Rust crate
running 1,000 sessions/day at $0.50 mean cost commits $3,000/day                     and its evaluation are the means by which we test what a type-
of reservation under the default. The approach is parametric                         level mitigation actually buys. Consistent with this ordering, the
                                                                                                                                                                   4

type-theoretic specification and the specification cross-checks are                                           TABLE 3
deferred to the appendices and the artifact: they support the case             Decision matrix for choosing an LLM cost-bound mechanism. “Stronger
                                                                           guarantee” refers to non-bypassability and proof-boundary scope; “operationally
study but are not load-bearing for the paper’s empirical claims, and         feasible” refers to deployment cost. The Rust affine discipline of this paper
a reader can assess the catalog and the head-to-head evaluation            occupies one row — the multi-provider Rust-agent row — and is deliberately not
without consulting them.                                                                                 a universal solution.

   (i) An empirical catalog and failure taxonomy of 63
                                                                            Deployment context        Recommended mechanism Why
       confirmed LLM-agent budget-overrun reports (plus 47
       supplementary structural entries) across 21 sub-projects in 18       Single provider, server- Provider-side hard cap (e.g. Kernel-enforced on provider
                                                                            side cap (e.g. pure Ope- max_completion_              servers; cannot be bypassed by
       ecosystems (2023–2026),1 organized into eight architectural          nAI)                     tokens)                      client code; zero operational
       mechanism clusters, with two-human independent inter-rater                                                                 overhead.
       reliability Cohen’s κ = 0.837 on the full N = 113 four-              Single account, AWS       AWS Bedrock session-level Provider-tier         cumulative-
                                                                            Bedrock deployment        budget actions (with auto- cap       enforcement        with
       class sample, and κ = 0.943 on the n = 79 rows both raters           with session-level cap    matic service revocation on kernel-enforced      revocation;
       independently marked confirmed (bf ∪ bu) (§2.1).                     requirement               threshold breach)           operationally stronger than any
  (ii) A misuse-resistant budget-delegation discipline in Rust.                                                                   client-side discipline within
                                                                                                                                  its scope. Cannot enforce
       We operationalize affine ownership as a small, ASCII-stable                                                                per-agent budgets within a
       Budget API (∼225 lines core, ∼1,180 non-comment code                                                                       single session or aggregate caps
                                                                                                                                  spanning multiple providers.
       lines with the provider-stratified estimator and extensions;
                                                                            Existing Python frame- Runtime cap: LiteLLM             Runtime cap on dollar spend.
       no unsafe (enforced by forbid(unsafe_code)), and                     work (LangChain, Cre- proxy, AgentGuard, or our         Python has no affine types; the
       no Arc<Mutex<_» in the core affine ownership path—                   wAI, AutoGPT, Auto- Python port                         Python port provides a runtime
       the multi-tenant BudgetPool extension does use one).                 Gen)                                                    _consumed flag plus a narrow
                                                                                                                                    Mypy plugin (§4.5) as defense-
       The borrow checker turns cloning, double-spending, and                                                                       in-depth, not as a replacement
       use-after-delegation into compile errors (§3); the dollar                                                                    for the Rust discipline.
       cap itself is runtime arithmetic under estimator assumption          New Rust agent, multi- Token Budgets + static Compile-time ownership in-
                                                                            provider, consumption AnthropicEstimator tegrity within Rust + run-
       A1. A correctly written runtime counter reaches the same             billing                (2.0× byte-length, default) time cap. Closes the budget-
       cap-respecting outcome; what the affine type adds is that                                                               primitive-missing failure mode
                                                                                                                               at the type level (the cap itself
       the incorrect version does not compile, so the multi-agent                                                              is runtime arithmetic). 2−6×
       delegation guarantee no longer depends on the operator                                                                  over-reservation is reserved-
       getting the concurrency discipline right (§4.5, §4.3).                                                                  not-held; no capital cost on
                                                                                                                               consumption-billed accounts.
 (iii) An empirical evaluation against five production runtime
                                                                            New     Rust    agent, Token Budgets + Adap- Same compile-time integrity,
       mitigations plus concurrent work (Agent Contracts) on                prepay-account capital tiveEstimator (ε = 0.10) 1.86× tighter median reserva-
       three providers and three catalog-derived workloads (§4),            constraint                                      tion (47.5% capital efficiency
                                                                                                                            vs. 25.5% static, §4.5); 0 A1
       characterizing what the approach does and does not add                                                               violations across 100 prompts.
       beyond runtime alternatives, with per-operation overhead                                                             Production default where pre-
       negligible relative to LLM API latency (§4.5).                                                                       pay capital matters.
                                                                            Capital       efficiency- Tokenizer-direct estimation   ∼1.0–1.1× over-reservation vs.
                                                                            critical (cost of unused with version pinning, or       1.86–6.20× for the affine dis-
1.4   Paper structure                                                       budget        dominates post-call observation with      cipline, at the cost of ∼700–
                                                                            cost of occasional SLO                                  3,900 ms per-spend latency
Section 2 presents the 63-incident empirical catalog with its 47-           overshoots)                                             (§4.5). Brittleness (tokenizer-
                                                                                                                                    version drift) in exchange for
entry supplementary corpus. Section 3 specifies the affine Budget                                                                   capital efficiency.
type and its async Rust integration. Section 4 reports the empirical
                                                                            Reasoning-model           Provider-side reasoning Reasoning models violate A6
evaluation: five-runtime head-to-heads, the temperature-stratified          workload      (OpenAI     controls (reasoning_ structurally (hidden thinking
sweep, the M2 estimator-vs-discipline isolation experiment, and             o-series,    Anthropic    effort,       thinking. tokens not bounded by max_
                                                                            extended-thinking,        budget_tokens)         as output_tokens);               pre-
the Forgetful-Operator experiment that isolates the affine disci-           DeepSeek-R1)              primary, Token Budgets as flight reservation requires
pline’s distinguishing contribution—non-bypassability of the M-                                       defense-in-depth          per-deployment calibration of
                                                                                                                                the reasoning-token reservation
delegation-fanout race within typed Rust source code. Section 5                                                                 (§6.8). Initial calibrations have
positions the contribution. Sections 6 and 8 discuss limitations and                                                            been observed off by an order
                                                                                                                                of magnitude until tuned.
conclude.
                                                                            Multi-tenant at scale Distributed quota service Single-process affine discipline
                                                                            (many users, budgets (Redis lease, Spanner-style does not extend across pro-
1.5   When is the Rust affine discipline the right choice?                  across replicas)      reservation, kernel quotas) cesses; the multi-tenant lease
                                                                                                                              sketch (§7.1) is not production-
The contribution is one mechanism among several for bounding                                                                  validated.
LLM dollar cost. Different deployment contexts have different
preferred mechanisms, and the affine discipline is not the best
choice in every context. Table 3 summarizes when Token Budgets             not contend with provider-side per-call caps in their cell (max_
should be preferred over the alternatives.                                 completion_tokens is kernel-enforced and unbypassable
    The Rust affine discipline is therefore positioned for the new-        per-call); the two address different operational requirements
Rust-agent, multi-provider, cumulative-session-cap cell of this            (per-call output bounding vs. session cumulative cap; §4.5, the
matrix. It is stronger than runtime client-side alternatives within        artifact provider-cap CSVs). Client-side code can always be
that cell (it adds the compile-time integrity property) but does           bypassed by misbehaving callers outside the Rust trust boundary
  1. Catalog identifiers (CCDE-XXX, AGPT-XXX, etc.) refer to rows in the
                                                                           of Budget::new.
catalog CSV in the public artifact.                                            The dominant deployment contexts among the 63 confirmed
                                                                                                                                          5

catalog incidents are existing Python frameworks (which dominate IDE-agent ecosystems among others; the full per-project mapping
the public-GitHub agent ecosystem we sample, roughly 7−8 of is in the artifact’s catalog CSV project column. Known selection
every 10 retained incidents; the Rust affine discipline does not biases: (i) English-language repositories only; (ii) closed-source
apply without re-implementation, and our Python port provides platforms (Cursor, Replit Agent, ChatGPT plugin store) absent;
runtime equivalence to existing mitigations) and new Rust agent (iii) the ≥ 1,000-star threshold filters out early-stage projects. The
deployments (a small minority of the same surface; this is the affine catalog is a convenience sample of public English-language failures
discipline’s primary deployment context). The ratios are illustrative in established projects, not a representative sample.
estimates from the catalog’s framework distribution (the per-                   Search and inclusion: We searched issue trackers of the 21
framework summary in §2.5), not ecosystem-wide measurements; projects using failure-related keywords (“budget,” “cost,” “token
a representative deployment census of the LLM-agent surface in limit,” “recursion,” “infinite loop,” “stale,” “runaway,” “embedding
2026 has not been published and our sampling frame selects on dimension,” “base64,” “streaming usage,” “max_turns”). From
the dependent variable (§2.1). We do not claim the approach is 167 candidate URLs across 16 batches (the full survey recorded in
operationally relevant to the majority of today’s deployments; we catalogue.csv), we retained 110 satisfying ≥ 1 of: (a) explicit
claim it is the right primitive for the specific Rust-agent deployment dollar loss or token-count amplification in the body, (b) a specific
context, and that the catalog’s documented failure modes recur failure mechanism described by filer or maintainer, (c) maintainer
across the full ecosystem regardless of implementation language acknowledgement of the broader pattern. The full survey including
(the fine-grained eight-cluster partition itself is exploratory, §6.6). the 57 triaged-out rows is in catalogue.csv; retained rows are
                                                                        tagged paper:* and triaged-out rows carry a SKIPPED for
2 M OTIVATION : A FAILURE C ATALOG                                      paper: prefix naming one of seven exclusion codes.
                                                                                Sampling frame caveat: The inclusion criteria above
Budget overruns in LLM-agent systems frequently surface as constitute a failure-confirming sampling frame: we retained projects
the economic consequence of upstream agent-failure modes specifically because their public artifacts surfaced budget-failure
documented in the broader literature: hallucination-driven loops activity. The catalog establishes that the 21 sub-projects identified
that re-issue tool calls until success [80], [81], tool-use recursion by these criteria exhibit the failure class, not that the failure
when an agent re-enters its own subgoal stack without termination class is necessarily prevalent across the ecosystem at large. A
conditions [82], [83], and context-window saturation causing complementary sampling step (the top-N most-starred LLM-agent
repeated retrieval expansions [84]. The approach proposed here projects without a failure-keyword filter, coded under the same
addresses the cost-bounding concern orthogonal to these upstream codebook) would strengthen the ecosystem-wide prevalence claim
failures: even if an agent never halts, the discipline bounds the and is left as follow-up replication.
deployer’s dollar exposure within the configured cap. The catalog               Construct validity: three known threats: Three construct-
below therefore documents the economic surface area of the wider validity threats apply to catalogs of this form; we document our
failure-mode landscape, not its mechanistic depth.                      response to each:
    The catalog comprises 63 confirmed production overrun
                                                                            (C1) Selection on the dependent variable. The catalog selects
incidents—the primary evidence corpus—drawn from 21 LLM-
                                                                        projects partly on the presence of budget-failure indicators. We
agent sub-projects across 18 ecosystems (the LangChain ecosystem
                                                                        do not claim ecosystem-wide prevalence; we claim existence and
alone contributes four: langchain, langgraph, langsmith,
                                                                        recurrence of the failure pattern across N = 21 independently-
deepagentsjs) and four years (2023–2026). Alongside these sit
                                                                        developed projects. The dollar-loss aggregates we report are sums
47 supplementary structural entries (28 maintainer-acknowledged
                                                                        across the selected cases, not estimates of ecosystem-wide expected
gaps, 14 feature requests, 5 borderline), for a 110-row corpus
                                                                        loss; readers should treat them as “at-least” lower bounds witnessed
whose case-type breakdown is detailed in §2.4. Each case is backed
                                                                        in the public record.
by a specific GitHub issue or pull request, quoted maintainer or
                                                                            (C2) Single-coder baseline replication. An initial coding pass
user statements, and (where available) documented dollar losses.
                                                                        was conducted by a single rater. We addressed this with an
The catalog establishes recurrence, not incidence: its sampling
                                                                        independent two-human IRR study where a second coder (Zahid
frame selects on the dependent variable (§2.1), so aggregate dollar
                                                                        Hussain, Mindgigs, Peshawar, Pakistan; no prior catalog exposure,
figures read as incident magnitudes rather than population statistics.
                                                                        no compensation, blinded to original codings) re-annotated all
To bound the selection concern we add an independent keyword-
                                                                        109 baseline rows under the published codebook (Phase 1, a tag-
neutral baseline cohort (§2.3), where the primary mechanism
                                                                        level coding pass, κ = 0.832), with a subsequent Phase 2 covering
clusters recur. The catalog grounds the design that follows: the
                                                                        the four entries added during continued catalog construction; the
failure shapes the type system must prevent, the mitigations
                                                                        combined N = 113 sample yields Cohen’s κ = 0.837 (95% CI
operators already deploy, and the gap that remains.
                                                                        [0.745, 0.919]); see the per-class breakdown below and the fr/bu
                                                                        boundary disclosure.
2.1 Methodology                                                             (C3) Post-hoc taxonomy. The eight failure-mechanism cat-
        Project selection: The 21 sub-projects comprising egories were derived by iterative open coding of the retained
the catalog corpus were selected from GitHub repositories issues, consolidating proximate cost mechanisms into clusters
tagged llm-agent, agent-framework, ai-agent, or across repeated passes during construction. We mitigated post-hoc
llm-orchestration with ≥ 1,000 stars as of January 2026 in category-drift risk by (i) freezing the codebook before the IRR study
Python, TypeScript, or Rust, and filtered to those that either (a) began, (ii) documenting per-tag decision rules and seven exclusion
expose a budget/cost/token-limit option in their public API or (b) codes in codebook_v1.md, and (iii) identifying the fr/bu
have a GitHub issue mentioning cost overrun or runaway-spend boundary as the codebook’s weakest seam in the IRR analysis. The
in the title. Retained projects span the LangChain/LangGraph, eight-cluster structure reproduced on the independent narrow-net
AutoGPT, CrewAI, AutoGen, Pydantic AI, DSPy, LlamaIndex, and batch (§2.2), which we read as a stability signal for the mechanism
                                                                                                                                        6

partition rather than its validation; we are explicit (§6.6) that the confirmed-incident classification is substantially stronger than the
eight-cluster partition is exploratory: a blind second-rater pass over aggregate headline figure suggests.
all 110 rows gives moderate cluster-assignment agreement (Cohen’s           The mf class rests on only n = 7 cases, so its κmf =0.918 (95%
κ = 0.44, 95% CI [0.34, 0.55]), with cost-observability (κ = 0.78) CI [0.658, 1.000]) is suggestive rather than dispositive. The fr/bu
and multimodal (κ = 0.65) reliably identified and the remaining boundary is the codebook’s weakest seam: interrogative-titled
boundaries overlapping. The taxonomy is auditable: any reviewer issues (“Can we control X?”, “How do I count Y?”) read plausibly
can re-derive it from the per-row evidence in catalogue.csv. as either a feature request or an unfixed bug whose fix would require
     Each retained case carries a verbatim quotation from the a new feature, so κfr =0.727 should be read as the reproducibility
underlying GitHub artifact and is tagged with one of five ceiling for this label at the issue-body-excerpt granularity the public
labels: bug_report, bug_fixed_by_framework, bug_ record affords. Because that boundary is convention-sensitive, the
unfixed, feature_request, maintainer_framing. paper anchors its strong claims on the convention-invariant union
The retained cohort comprises 27 bf, 55 bu, 7 mf, 21 fr cases bf ∪ bu ∪ mf ∪ fr—the budget-primitive-missing issues across 21
(catalog total N = 110). The IRR re-annotation was conducted frameworks, which is invariant to where the internal bu/fr cut
in two phases. Phase 1 (baseline, N = 109) was completed is drawn—rather than on the precise confirmed-incident count.
before four catalog entries (CCDE-002, LANG-020, LANG-035, The headline κ = 0.837 and the confirmed/supplementary partition
SMAG-001) were added during continued construction. Phase rest on the v1.0 codebook, which we report as primary. The 12
2 (supplementary, N = 4) re-rated those four entries by rater B disagreements in the N = 113 re-annotation, with their adjudicated
independently of rater A. Across both phases the full IRR sample resolutions, are documented in irr-disagreements.md; the
is N = 113 rater-pair observations covering all 110 current catalog codebook (v1.0), the blinded coding sheet, the completed coding
rows (with 3 baseline ratings on IDs that were renumbered during sheets, and the computation script irr_scaffold.py ship in
catalog cleanup retained in the sample, since the underlying issue the artifact under irr/.
content rather than the catalog ID is what was rated). Per-class            Two further methodological notes: (i) the candidate-sourcing
kappa in the inline per-class summary reports the augmented protocol shifted partway through the catalog construction from an
N = 113 sample (27 bf + 57 bu + 7 mf + 22 fr = 113). The LLM-assisted keyword-expansion pipeline (Batch 1, retention
methodology follows the broad shape of failure-pattern catalogs ∼ 8%) to a direct human keyword-skim protocol (Batch 2,
in the SE literature (Yuan et al. [20]; Lu et al. [21]; IRR protocol retention ∼ 83%); both phases applied the same written codebook
per Kitchenham [2] and Krippendorff [3]). Methodologically, the and the protocol-stratification details are reported in §2.2; (ii)
catalog is constructed as a qualitative coding study rather than a public GitHub issues bias the sample toward popular open-source
systematic prevalence survey: the eight mechanism clusters emerge frameworks and under-represent closed-source platforms and
from iterative open coding in the grounded-theory tradition [4] and incidents filed only on internal trackers; both threats are revisited
are consolidated using the thematic-synthesis steps recommended in Section 4.4.
for software engineering [5], with per-tag decision rules recorded
in a codebook in the manner of Saldaña [6]; the two-coder
reliability and construct-validity framing follow the case-study 2.2 Catalog collection methodology: protocol stratification
and experimentation guidelines of Runeson and Höst [7] and The catalog’s candidate sourcing proceeded in two main batches
Wohlin et al. [8]. We read the catalog as a multiple-case study (reported separately because the protocols measure different things),
of independently-developed projects, not as a random sample, plus a small number of entries added during continued construction
precisely because public GitHub issue trackers are a biased and (§2.1). Batch 1 (76 cases, summer 2025): keyword-templated
noisy frame — the documented perils of mining GitHub [9] GitHub queries returned ∼ 950 candidates, an LLM filter narrowed
(active-project skew, missing or private incidents, and selection by cost-relevance, the human rater coded against the codebook;
on visibility) motivate the recurrence-not-prevalence scoping we retention ∼ 8% by design (wide-net favors recall). Batch 2 (33
adopt throughout (C1 below). The full IRR result is reported next: cases, autumn 2025): direct human keyword search without LLM
across both phases, the N = 113 rater-pair sample gives κ = 0.837 pre-filter; retention ∼ 83% (narrow-net favors precision). We strat-
(95% bootstrap CI [0.745, 0.919]), corresponding to almost-perfect ify rather than re-weight because the protocols are complementary;
agreement. Phase 2 agreement was 4/4 on the four supplementary the 33-case narrow-net subset alone exhibits the same eight-cluster
rows; the slight upward shift from the κ = 0.832 baseline (N = 109) mechanism taxonomy, per-framework distribution, and case-type
reflects the additional perfect-agreement observations and is within breakdown as the full N = 110 catalog. The N = 113 IRR sample
the original bootstrap interval.                                        (§4.4) spans rows from both batches, so the headline κ = 0.837 is
     Per-class one-vs-rest Cohen’s κ on the N=113 two- not an artifact of either sourcing protocol alone.
phase re-annotation (artifact: irr/per_class_kappa.csv):
κbf =0.858 (obs. agreement 0.947, n = 27), κbu =0.876 (0.938,
n = 57), κmf =0.918 (0.991, n = 7), κfr =0.727 (0.911, n = 22), 2.3 Baseline replication on an independent project cohort
with κ=0.943 (0.975, n = 79) on the subset of rows both raters Because the 21-project catalog was constructed by following
independently classed as confirmed (bf∪bu); note that this budget-cost search keywords, its sampling frame could in principle
figure conditions on agreement about the confirmed/not-confirmed confirm the existence of cost incidents by selecting on the depen-
boundary and is therefore an optimistic within-class measure, not dent variable. To bound that risk, we constructed an independent
a substitute for the headline N=113 value. The κ≥0.85 on the baseline cohort: 20 GitHub projects ranked by stars under the
principal classes is the result we report; the lower κfr identifies the “LLM agent” search term, exclusions logged transparently, 3,461
fr/bu boundary as the least reproducible label. The κ=0.943 issues pulled and 186 body-read under the same codebook.
on the confirmed subset indicates that the headline κ=0.837 Headline findings: 63 candidate qualifying rows in 12 of 20
is conservative: agreement on the operationally most-relevant projects (60% coverage; 95% Wilson CI [40%, 77%]); the four
                                                                                                                                           7

primary mechanism clusters recur, plus an additional M-rate-limit- report 63/28/14/5 as a descriptive composition, while every count
amplification cluster in VoltAgent #1276; the original budget- the artifact mechanically re-derives (the 110 retained rows, the
keyword filter would have caught 61/63 qualifying rows (97% eight clusters, and the IRR) keys on the label and primary_
catch rate). Methodology limitations (exploratory replication): cluster columns.
all 186 baseline codings were single-coder (no IRR for this cohort,         The 110-row aggregate count is a corpus of evidence of the
in contrast to the primary catalog’s κ = 0.837 on N = 113); budget-primitive-missing condition across 21 sub-projects, not
∼25 of 63 rows have full-thread evidence and the balance have 110 distinct paying-customer overrun incidents. Our headline IRR
title-plus-first-comment evidence flagged as pending; the 97% study (full-sample Cohen’s κ = 0.837, N = 113) covers the union
catch rate is within-screen, not a full recall estimate. Subject of all four case types; per-case-type breakdown of agreement
to these limitations, the cohort supports two weaker claims: the is in irr-disagreements.md. Prevalence claims (“X% of
mechanism clusters recur in an independently selected cohort deployments overrun”) are not supported by this catalog and we
(external validity); and demand for budget-discipline primitives is make none; the catalog establishes the existence and recurrence of
sustained (e.g., SuperAGI has three independent “Budget Manager” the structural class, not its incidence rate.
feature requests). We make no incidence claim from this data: 60%
is a project-level coverage statistic, not an incidence rate. Full
                                                                       2.5 Catalog
audit trail, per-project breakdown, and substituted candidates in
token-budgets-baseline/.                                               The catalog contains 110 retained rows organized along two
                                                                       dimensions. The inline summary above lists the eight architectural
                                                                       mechanism clusters that emerged during construction, each with
2.4 Catalog composition: confirmed failures, design gaps, and
                                                                       its row count, framework reach, and number of distinct sub-
feature requests
                                                                       mechanisms documented. The per-framework summary in §2.5
The unqualified term “failures” covers heterogeneous case types in gives the per-framework distribution of retained rows. The full
the budget-overrun literature. We disaggregate the 110-row catalog per-row evidence—including identifier, framework, year, clas-
by case type, distinct from the 8-cluster mechanism taxonomy:          sification tag, GitHub URL, quoted user/maintainer evidence,
    • Confirmed production failures (n = 63, 57.3%): GitHub            documented dollar loss, and per-row notes—is in the artifact’s
      issues with reproducible cost-overrun symptoms reported by catalogue.csv file. We use catalog identifiers (e.g., LANG-
      an end-user, accompanied by quoted issue text and (where 035, MAST-014, PYAI-002, CRAI-014) throughout the rest of
      available) cost figures. The DNSW-001 incident (a single the paper; the artifact provides a one-paragraph note for every
      user reporting ≈$2,150 / EUR 2,000 in unintended spend) identifier.
      is the most operationally severe and dominates the catalog’s          The eight architectural mechanism clusters in the catalog
      monetary total; we report it as a single observation and do not (rows / frameworks), re-derived from the primary_cluster
      project prevalence from it. The boundary between this class column over all 110 retained rows: M-retry-loop (27 / 12), M-
      and feature requests (fr) is the codebook’s weakest seam cost-observability (22 / 9), M-context-amplification (13 / 7), M-
      and is convention-sensitive (§2.1); the count n = 63 should storage-amplification (13 / 5), M-budget-primitive-missing (12 /
      be read with that caveat, and the paper’s strong claims are 6), M-delegation-fanout (11 / 6), providerOptions-silently-
      anchored on the convention-invariant union of all four classes dropped (6 / 3), and M-multimodal-cost-amplification (6 / 2).
      rather than on this internal split.                                   These eight clusters are an exploratory, descriptive organization
    • Maintainer-acknowledged structural gaps (n = 28, 25.5%): of the corpus. A blind second-rater pass gives moderate cluster-
      cases where a framework maintainer (not the original reporter) assignment agreement (Cohen’s κ = 0.44; cost-observability and
      responded that the budget primitive is structurally absent multimodal are the two reliably-identified mechanisms, κ = 0.78
      or known-broken, and either accepted the limitation as and 0.65), so we use the clusters to structure the discussion of
      “working as intended” or scheduled it as a future-release issue. failure modes but do not treat the partition as validated or rest
      These are not user-reported incidents but framework-side claims on exact per-cluster counts (§6.6).
      acknowledgements that the cluster-1 budget-primitive-missing             Per-framework distribution (totals 110 rows):
      condition exists.                                                LangChain ecosystem (langchain, langgraph, langsmith,
    • Feature requests for budget primitives (n = 14, 12.7%):          deepagentsjs) 33; Mastra 17; AutoGen 11; CrewAI 11;
      issues opened by a user requesting a budget primitive that does smolagents 5; Aider 6; DSPy 4; LlamaIndex 3; Pydantic AI 7;
      not exist in the framework, without a specific overrun-incident claude-code 2; AutoGPT 2; gpt-engineer 2; OpenAI
      report attached. These corroborate the cluster-1 hypothesis (the Agents SDK 2; and one each from danswer, openclaw, nanobot,
      primitive is missing) but are not themselves failure incidents. paperclipai, and codex (5 total). Per-row evidence in the artifact’s
    • Mixed / borderline (n = 5, 4.5%): cases where the issue          catalogue.csv.
      thread contains both a request and a partial overrun report;          The catalog tracks per-row dollar losses where reported and
      counted once and resolved to a single four-class label for amplification ratios where measurable; the strongest individual
      the reliability analysis.                                        amplification anchors (a 31x context overflow from a single base64-
     The four case types above are an analytic disaggregation of encoded image [17], a 2-million-token observer-LLM call [18])
the corpus and are distinct from the four-class label column appear in Section 2.6 where they are organized by mechanism
(bf/bu/mf/fr) that the public catalogue.csv encodes and cluster. The catalog distributes across the four catalog years as
that the inter-rater study scores: the 63/28/14/5 split is a coarser 18 cases in 2023, 25 in 2024, 52 in 2025, and 15 in the partial
editorial grouping (a confirmed incident may carry bf or bu; year 2026 (through April). We do not interpret this distribution as
a maintainer-gap row may carry bu or mf) and is not, in the evidence of acceleration: the LLM-agent ecosystem itself expanded
present artifact, recoverable by a single column filter. We therefore substantially over the same period (new frameworks, growing
                                                                                                                                              8

GitHub activity, methodology refinements mid-survey), and the            single-call amplification: up to 2 million tokens in a single observer
raw issue count is not normalized against ecosystem growth. The          LLM call during tool-heavy runs, where the observation manager
temporal distribution is reported for descriptive completeness;          itself becomes the cost amplifier). @aymeric-roucher’s reasoning—
the primary observation is that the failure class continues to be        “would introduce silent errors”—is the failure mode that type-level
documented across all four catalog years across 18 ecosystems            discipline addresses: type capabilities make budget exhaustion
rather than being absorbed as a solved problem in any one year.          explicit-at-compile-time rather than implicit-at-runtime.


2.6   Patterns                                                           2.7   The three-layer enforcement taxonomy
                                                                         The mitigations actually deployed in response to the catalog’s
Twelve observations from the catalog inform the design that
                                                                         failures fall into three layers, defined by where in the system the
follows. The first six are recurring patterns we observed in the
                                                                         enforcement occurs.
original catalog and have persisted as the catalog grew; the
                                                                             Compile-time layer (this work). The borrow checker rejects
next six emerged from the expanded archaeology covering eight
                                                                         programs that alias, double-spend, or reuse a delegated Budget
architectural mechanism clusters across 18 ecosystems.
                                                                         before the binary is built — the in-program integrity errors, not
     Reactive fixes dominate. For cases tagged bug_fixed_by_
                                                                         the dollar bound itself, which is runtime arithmetic (§3.4). Caught
framework, the median time from filing to fix is short: CCDE-
                                                                         before deployment. We found no prior published or open-source
001 was patched in two days; AIDR-001 was patched the same day
                                                                         work applying compile-time ownership integrity to LLM cost; the
in commit f2e1e17; CRAI-002 was patched the same day; CRAI-
                                                                         closest analogues are discussed in Section 5.
011 was merged 1 day after filing (the fastest fix-resolution in the
                                                                             Software layer. Runtime middleware tracks spend and pauses
catalog) with the reporter having identified the exact regression-
                                                                         execution when a threshold is crossed. Examples: an AgentGuard-
introducing commit efe27bd themselves in the issue body. This
                                                                         style budget callback [13], paperclipai’s monthly-budget feature,
is not for lack of engineering attention. The fixes work, and they
                                                                         and the proposed nanobot maxCostPerMessage flag. Caught
ship quickly. But the fix can only ship after the bug fires and a user
                                                                         at runtime, after the spend has occurred.
reports it—which means the dollars have already been paid by at
                                                                             Transport layer. A payment-aware HTTP intermediary returns
least one user. We found no case in the catalog where a budget
                                                                         a 402 Payment Required when the agent’s wallet depletes; the
overrun was prevented before any user paid for it.
                                                                         gateway rejects further requests through that wallet. Example:
     Even Anthropic’s first-party tool is affected. Two of the 110
                                                                         ATXP. Caught at the network boundary, after the request has
entries are claude-code issues, both exhibiting the same compaction-
                                                                         already been issued.
loop signature; the activity log of CCDE-002 alone references at
                                                                             These three layers are complementary, not competing. An
least ten additional sibling claude-code issues filed August through
                                                                         operator running a high-stakes agent in production might deploy
December 2025 with the same signature, several of which the
                                                                         mitigations at all three, with each catching a different failure
github-actions bot itself flagged as duplicates of CCDE-002 at
                                                                         mode. Section 5 places each prior system in this taxonomy and
filing time. CCDE-001 alone documents $235 spent in four days by
                                                                         discusses why we treat the compile-time layer first: it is the only
a single user (about $59/day, or roughly $1,760 extrapolated linearly
                                                                         one that catches the integrity violations (aliasing, double-spend,
to a full month). The two further first-party-vendor frameworks
                                                                         use-after-delegation) before any external resource is consumed,
now in the catalog (Pydantic AI, OpenAI Agents SDK) confirm
                                                                         and the only one that gives the developer feedback on the affected
the pattern is not specific to Anthropic: PYAI-001 documents
                                                                         program before deployment. The dollar bound is enforced at the
a Pydantic AI multi-agent docs example that fails on its own
                                                                         runtime-arithmetic layer regardless, so this ordering is about where
total_tokens_limit default; OAAS-002 [19] documents
                                                                         misuse-resistance lives, not about which layer enforces the cap.
a maintainer admission that “We don’t have anything amazing
here right now” for graceful degradation when max_turns is
exceeded. The failure class is not confined to fringe libraries: three   3 T HE MITIGATION : AN AFFINE B U D G E T ( CASE STUDY )
first-party vendor agent frameworks exhibit it.                          The catalog of Section 2 identifies eight distinct architectural mecha-
     Context amplification arises at three architectural lev-            nism clusters underlying production budget-overrun incidents. Two
els. The M-context-amplification cluster (13 rows across seven           distinct mechanisms answer it, and we are careful not to conflate
frameworks) collects agent loops and compile-time optimizers             them. A runtime cap (the checked_sub reservation of §3.4,
that produce unbounded context growth; the same mechanism                under estimator assumption A1) bounds the dollar consequence of
also surfaces as a secondary effect in several incidents whose           all eight clusters once it is in place — whatever the upstream
primary cluster lies elsewhere (retry-loop, delegation-fanout). Three    cause, in-program spend cannot exceed B0 . That cap is not
architectural levels recur, which we illustrate with representative      novel: a correctly written runtime counter, Agent Contracts, or
incidents: compile-time (DSPY-001 and DSPY-003 at MIPROv2                a LiteLLM proxy reach the same outcome. The affine Budget
batch-summary and bootstrap-demo steps, where the optimizer              type contributes something narrower and orthogonal: it makes
programmatically constructs prompts that include training data,          the cap’s bookkeeping non-bypassable in typed source, so the
producing 70% overshoot in DSPY-001 and base64-image injection           operator cannot accidentally defeat it through the aliasing/double-
in DSPY-003); runtime agent-step-loop (SMAG-002 stuck-open               spend/use-after-delegation mistakes the catalog documents. Exactly
for 13+ months with multiple PRs in flight, SMAG-006 with                one cluster — M-budget-primitive-missing (12 of 110 rows, six
maintainer @aymeric-roucher’s paper-relevant admission “we               frameworks; see the summary in §2.6) — is fixed at the type
decided against truncating or doing any kind of post-processing          level rather than merely bounded: its failures are not bugs in an
on steps, because that would introduce silent errors,” and MAST-         existing primitive but the absence of one (frameworks ship without
004 documenting TokenLimiter not firing per loop-iteration); and         a first-class aggregate-budget primitive, or ship one that regresses
runtime observability-layer (MAST-014 with the catalog’s largest         silently, or expose it only via callback closure), and a type that pins
                                                                                                                                          9

the mechanism cannot regress in those ways. So the honest scope is:     showing the approach in a multi-agent delegation, and the type-
the cap covers the catalog as a consequence-bound; the type system      theoretic justification for affine rather than linear typing appear
addresses one cluster structurally and, across the rest, removes        in Appendix A. Proposition 1, Conjecture 1, and the supporting
the operator-discipline requirement that the M-delegation-fanout        structural lemmas appear in §3.4 and §3.5; the per-tool obligation
experiment (§4.3) isolates. This section specifies the type; the        breakdown for the specification-checking cross-checks is in
reader who only wants the empirical catalog can stop at Section 2       Appendix B for readers who want it. The main body proceeds
without loss.                                                           directly to implementation (§3) and empirical evaluation (§4); a
        Why a type system rather than a runtime counter?: Because       reader who wants to verify the source-level claims first should
the failure the catalog most often records is not a missing check       consult the appendices before continuing.
but a correctly-intended check that races or is bypassed under
concurrency (the M-delegation-fanout shape, 11 rows). A runtime         3.4   Conservative reservation and the cap bound
counter is only as good as the operator’s lock discipline; the affine
type makes the racy pattern fail to compile. This is the whole of the   Before each call the approach reserves an upper bound on the calls
type-level claim — not a stronger cost guarantee, which remains         cost—a provider-stratified estimate (byte-length for OpenAI/Groq,
runtime arithmetic — and the rest of the paper is careful to claim      a tool-loop-aware estimator for Anthropic) times a safety margin—
no more than this.                                                      and debits it from the budget via checked_sub; a call that would
                                                                        exceed the cap is refused before the API request. Under a sound
                                                                        estimator (assumption A1) and the provider honoring its output
3.1   The Budget API                                                    cap (A6), this gives a conditional dollar-cap bound, stated for the
The Budget type is a Rust value of type u64 representing                abstract machine below. The bound is enforced by the runtime
remaining quota in micro-cents (1 uc = 10−5 USD). It exposes            arithmetic, not by the type system; the type system supplies the
four self-consuming methods:                                            integrity (no aliasing or double-spend of the reserved amount) that
   • Budget::new(amount) — gated behind a capability
                                                                        makes the arithmetic non-bypassable in typed code.
     token (BudgetMint, §4.5) so the trusted minting surface is         Proposition 1 (Abstract-machine cap soundness under provider-s-
     auditable.                                                         tratified A1). Let M denote the abstract state machine
   • budget.spend(uc) -> Result<(Budget,                                modeling the eight Budget transitions (SpendSuccess,
     ReservationReceipt)> — consumes self by value,                     SpendInsufficient, SpendFailPostCheck, Consume,
     returns the remainder and a receipt for post-call refund (§3.4).   Reserve, ConfirmWithRefund, Forfeit, RefundTo)
   • budget.split(left, right) ->                                       over the six-variable conservation ledger
     Result<(Budget, Budget)> — consumes self
     by value, returns two child budgets summing to the parent.                 liveSum, outstandingReceipts, outstandingRefunds,
                                                                                                                               
   • Budget::merge(a, b) -> Budget — consumes                                   totalCharged, totalUnrecoverable, totalReleased .
     both arguments by value, returns the combined budget.
                                                                        Let P denote a provider configuration with estimator EP selected
    All four methods are self-consuming on a non-Clone, non-
                                                                        by select_for_provider(P). Assume:
Copy type. The Rust borrow checker rejects three classes of
                                                                           • (A1, P-stratified) For every prompt p transmitted under P,
cap-circumvention at compile time: aliasing (no Clone), double-
spending (spend consumes self), and use after delegation                     EP (p) ≥ billable_tokensP (p), where billable_tokensP denotes
(split consumes the parent). Seven distinct rustc error codes en-            the input-token count P uses for billing.
                                                                           • (A2, overflow-free regime) Every Budget is constructed with
force these properties; the full enumeration appears in Appendix A.
                                                                             micro_cents < 263 .
                                                                           • (A6, output-cap respected) For every call to P, the
3.2   Deployment scope                                                       number of output tokens billed by P does not ex-
This approach applies to Rust agent code where the operator                  ceed the caller-supplied max_output_tokens parameter:
chooses the Budget primitive over alternative cap mechanisms.                billed_output_tokensP (call) ≤ max_output_tokens.
Section 6 establishes the deployment context as new Rust agent             • (A7, charge-truthfulness) When a successful call’s reser-
code, a minority of the 2026 production LLM-agent surface                    vation is reconciled via ReservationReceipt::
(which is presently dominated by Python frameworks; the per-                 confirm(actual_charge), the actual_charge value (operator-
framework summary in §2.5). Table 3 gives the full decision                  supplied, typically read from response.usage) is ≥ the
matrix mapping deployment configurations to the appropriate cap              amount P actually bills for the call. A7 is a trust assumption
mechanism (provider-side hard cap, AWS Bedrock session-level                 on provider usage reporting, shared with every client-
budget action, Token Budgets, or runtime observer); the affine               side cost-accounting mechanism (LangSmith, LiteLLM proxy
Budget is recommended only for the cells where its operational               budgets, AgentGuard, Helicone); it is not a property of the
profile (non-bypassability inside typed source code, pre-flight              affine type system. §3.4 discusses the assumption and the
refusal, ∼ 2× over-reservation under the AdaptiveEstimator)                  empirical evidence (pydantic-ai issues #5445, #5379, #5304,
matches operator priorities.                                                 #5302 document provider-side usage omissions). Note: A7
                                                                             is dispensable if the operator opts out of the receipt-refund
                                                                             path and treats each spend as the final ledger entry; the
3.3   Where the rest of this material lives                                  conservative-margin default loses tightness but not soundness.
The complete type-system specification (Properties 1–3 on aliasing,        • (A8, rate-stability) The per-token rates ρin , ρout used by the
spend-soundness, and delegation-after-split with their correspond-           operator to compute reservations match the rates P actually
ing rustc rejection diagnostics), a step-by-step worked example              charges, for the duration of the session. A8 fails if P raises
                                                                                                                                            10

     rates mid-session without operator re-calibration. This is a         it with the expected diagnostic. The nine exercise seven dis-
     deployment-time discipline on tokenizer-and-pricing version          tinct rustc diagnostics (E0277, E0308, E0382, E0505, E0507,
     pinning, not a property of the type system; §4.5 names               E0599, E0624) across five granularities — value-level (use-after-
     tokenizer-version stability as the operationally-equivalent          spend/split/move), reference-level (consume-while-borrowed,
     residual exposure.                                                   consume-through-shared-reference), trait-resolution (Send, absent
Then under A1, A2, A6, A7, and A8, for every reachable state              Clone), typestate (the ReservationReceipt closure-return
σ of M and every i ∈ S the estimator satisfies ci ≤ ri , and the          contract), and capability-level (E0624 gating Budget::new
cap-respecting bound ∑i∈S ci ≤ ∑i∈S ri ≤ B0 holds throughout the          behind the BudgetMint token) — evidence that the approach
execution.                                                                is enforced through multiple independent borrow-checker and
                                                                          type-checker paths, not one narrow rejection. All nine pass on
        Reconciliation and refunds: A successful call rec-                rustc 1.93.1 stable (edition 2024) and reproduce via cargo
onciles its reservation against the provider-reported charge              test -test compile_fail; per-test rejection output is in
via ReservationReceipt::confirm (refunding any over-                      the artifact at tests/compile_fail/. The rejections occur at
reservation); a failed call forfeits its receipt. This path depends on    compile time, using the same borrow checker Rust users already
assumption A7 above. The receipt/refund state machine and its             trust for memory safety — we contribute the design pattern, not
overflow, panic, and cancellation handling are in the artifact.           new compiler machinery.

3.5   Binary-level cap soundness: the open obligation                     4.2   Multi-runtime head-to-head (summary)
The integrity properties hold on well-typed Rust source. Whether          To show the mechanism difference is not specific to LangGraph, we
they survive compilation—whether rustc codegen and the Tokio              ran the LANG-001 reproduction across five runtimes spanning the
scheduler preserve them on the running binary—is something we             three enforcement layers of §2.7—compile-time (Token Budgets),
neither establish nor rely on.                                            runtime-cost (an AgentGuard-style cost callback and LiteLLM
Conjecture 1 (Binary-level cap soundness, open). The compiled             proxy budgets), and runtime-structural (LangGraph recursion_
binary preserves the source-level properties, so Proposition 1            limit, CrewAI max_iter, AutoGen max_turns)—against
transports to the running program.                                        a deterministic mock and three live providers (gpt-4o-mini,
                                                                          claude-haiku-4-5, llama-3.3-70b) at a fixed $0.0054
We do not prove this. The claim throughout is source-level;               cap. Structural counters are included not as cost comparators but
the evaluation reports observed binary-level behavior (zero cap           because the catalog shows operators mis-deploy them as cost
violations across all runs), not a guarantee. A proof skeleton is in      proxies (cluster M-budget-primitive-missing; LANG-001, CRAI-
the artifact for future work.                                             002); their behavior under a dollar metric measures the size of that
                                                                          gap.
                                                                              The pattern is consistent across providers (full grid, setup, and
4     E VALUATION
                                                                          per-cell evidence in Appendix D, Table 8). Structural counters
Table 4 maps the whole evaluation: every experiment, the claim it         bound call count, not dollars, and overshoot badly on the more
tests, its setup, and its headline result. We refer to experiments by     verbose providers (up to 1395% of cap on Anthropic). Runtime-cost
the identifiers E1–E15 introduced there. Two experiments share the        mechanisms—the AgentGuard-style callback and the LiteLLM
cap B0 =2,000 uc and must not be conflated: E2 is the five-baseline       proxy—track dollars but check after each call returns, so they
head-to-head on claude-sonnet-4; E4 is the Agent-Contracts                admit one overshooting call before refusing the next. The Rust
operational-parity comparison on claude-haiku-4-5.                        Budget implementation refuses every cap-violating call before the
         Statistical conventions used throughout §4: Many sweeps          network request and never exceeds the cap (maximum overshoot
use temperature=0 for determinism. At T = 0, replicas within              0 uc across all live cells); a Python behavioral simulation of the
a cell are near-deterministic, so the effective sample size of a single   same discipline over-spends (168%/153% on Anthropic/Groq)
N = 30 cell is the number of distinct scheduling interleavings            because its coarse estimator under-reserves—itself evidence that
plus the small stochasticity from network and tokenizer non-              the byte-length estimator over the full serialized request body (the
determinism — substantially below 30. We report two intervals             Rust default) is the load-bearing implementation choice. The cap-
to make this visible: a per-run Wilson 95% interval treating each         respecting outcome is therefore shared with a correctly-configured
replica as independent (the tightest interval; reproduces what            runtime-cost layer; the approach’s distinction is pre-call refusal
most empirical-SE papers report at this scale) and a per-cell             versus post-hoc observation.
interval treating each configuration as one observation (the most
conservative). The headline figures aggregate across at least three
                                                                          4.3 Forgetful-operator experiment: what compile-time integrity
distinct configurations to give the per-cell interval epistemic weight;
                                                                          uniquely catches
single-cell results are flagged as evidence on that configuration only.
The independence assumption is discussed explicitly in §4.5, where        §5.1 establishes that Agent Contracts [25] achieves at runtime the
a T ∈ {0.0, 0.3, 0.7, 1.0} sweep at N = 160 supplies genuinely            same cap-respecting outcome this approach achieves at compile
independent runs.                                                         time. This subsection asks what compile-time integrity uniquely
                                                                          catches that the runtime alternative does not, using a minimal
                                                                          reproduction of the M-delegation-fanout race (cluster M-delegation-
4.1   Compile-time guarantees                                             fanout, 11 rows).
Nine trybuild compile-fail tests validate the resource-                           What this experiment isolates: The experiment does not
accounting integrity properties: each is a small Rust program             claim that type-system discipline beats runtime discipline at the
that violates one property and passes when rustc rejects                  cap-respecting outcome. The locked Python (Condition B) and
                                                                                                                                                                               11

                                                                              TABLE 4
   Roadmap of the evaluation. Each experiment, the claim it tests, its setup, and its headline result, so the experiments can be told apart on first read. “uc” is
micro-cents (1 uc = $10−5 ). Groups: A compile-time integrity; B cap-respecting outcome on live API; C what the type system uniquely adds; D estimator soundness
                                                           and capital cost; E deployment and overhead.


     ID      Tests                                 Setup (model, cap, N)                                 Headline result                                  Where

     A. Compile-time integrity (source-level, no API call)
     E1     No clone / no double-spend / no          9 trybuild compile-fail tests; 7 distinct rustc     9/9 rejected as expected                         §4.1
            use-after-split; capability-gated        codes; rustc 1.93.1
            Budget::new

     B. Cap-respecting outcome (live API)
     E2      Pre-call refusal vs. structural and   LANG-001 retry loop; claude-sonnet-4;                 5 baselines 30/30; TB 0/30                       Fig. 1, §4.2
             post-call caps                        B0 =2,000 uc; N=30/runtime; T =0
     E2′     Cross-provider replication of E2      gpt-4o-mini, claude-haiku-4-5, llama-3.3-             TB max overshoot 0 uc; structural up to          App. D, Tab. 8
                                                   70b; B0 =540 uc ($0.0054)                             1395% of cap
     E4      Agent-Contracts operational parity    gpt-4o + claude-haiku-4-5; B0 =2,000 uc               TB-Rust, locked Python, Agent Contracts all 0    §4.5
             at an admitting cap                                                                         overshoot
     E5      Cap-respecting under sampling         T ∈ {0, 0.3, 0.7, 1.0}; N=160; two production-        0 violations, 0 false refusals                   §4.5
             (independent runs)                    tier models
     E8      Sub-floor cap: refusal-to-operate     claude-haiku-4-5; B0 =540 uc                          TB 0/30 pre-flight refusal vs. baseline 30/30    §4.5
     E9      Cap-sweep robustness                  10 caps incl. {540, 5000, 10000, 20000} uc            30/30 cap-respecting                             §4.5
     E11     Calibrated cap-correctness at scale   2,628 trials; per-call distributions fit to 30 real   cap held (arithmetic at scale, not independent   §4.5
                                                   runs                                                  obs.)
     E12     Live-API session sweep                382 sessions; pre-flight / mid-loop / self-           0 overshoot                                      §4
                                                   terminated

     C. What the type system uniquely adds (mechanism isolation)
     E3     Non-bypassability vs. operator        Forgetful-operator, 5 conditions A–E;                  racy A 30/30; disciplined B–E 0/30               §4.3
            lock discipline                       claude-haiku-4-5; B0 =60/100 uc; 3                     (p=1.69×10−17 ); racy pattern does not
                                                  children; N=30                                         compile
     E6     Single-agent isolation (M2)           4-line Python counter vs. TB-Rust, same                match at 0/30 (no single-agent advantage)        §4.5
                                                  estimator
     E10    Multi-agent delegation                concurrent sub-agents under one cap                    0/60 aggregate, 0/180 per-child                  §4.5

     D. Estimator soundness and capital cost
     E7      A1 estimator hold-outs vs.            three hold-outs, N=243 (cal+hold-out summary          0 soundness violations; ≥ 2.32× safety; up to    §4.5
             count_tokens oracle                   N=178, Tab. 2)                                        9.97× over-reserve
     E15     Capital efficiency / over-            N=5,190 per-call events; three estimators             static 6.20× mean (2.51× med.); Adaptive         §4.5
             reservation                                                                                 2.11× med.; tokenizer-direct ∼1.0–1.1× at
                                                                                                         939–1749 ms

     E. Deployment and overhead
     E13    N=1 production Rust deployment         rig-core 0.37; claude-haiku-4-5; $0.05 cap            single-agent 22 served / 18 refused ($0.0404 ≤   §4.6
            (Rig)                                                                                        $0.05); 4 concurrent sub-agents $0.0400
     E14    Per-operation overhead                 Criterion microbenchmark                              < 200 ns/op (observed ∼1.15 ns)                  §4.5



  Runtime                                               Overshoots Wilson 95% CI on overshoot rate                                                                 p vs. TB

  LangGraph (recursion_limit=20)                                30/30                                                      [0.886, 1.000]                      < 5.4 × 10−15
  LangGraph + AgentGuard cb                                     30/30                                                      [0.886, 1.000]                      < 5.4 × 10−15
  CrewAI (max_iter=5)                                           30/30                                                      [0.886, 1.000]                      < 5.4 × 10−15
  AutoGen (max_turns=4)                                         30/30                                                      [0.886, 1.000]                      < 5.4 × 10−15
  LiteLLM proxy (post-call)                                     30/30                                                      [0.886, 1.000]                      < 5.4 × 10−15

  Token Budgets (Rust)                                            0/30           [0.000, 0.114]                                                                            —

Fig. 1. Overshoot rate on the LANG-001 multi-step retry-loop workload at B0 = 2000 uc, claude-sonnet-4, N = 30 replicas per runtime, temperature T = 0. Statistical
note: at T = 0 replicas within a cell are near-deterministic, so the per-replica Wilson 95% intervals shown treat each replica as independent and report the
tighter (over-confident) bound; the conservative per-cell reading takes the configuration as the unit of observation (Neff = 1 per runtime). The cross-temperature
consistency at T ∈ {0.0, 0.3, 0.7, 1.0} on N = 160 genuinely-independent runs (§4.5) reproduces the 0/N vs. N/N split on the approach-vs-baselines axis and is
the primary evidence for the cap-respecting claim; Fisher’s p < 5.4 × 10−15 on per-replica counts is reported for completeness but is not what the claim rests on. Five
baselines (LangGraph, CrewAI, AutoGen, AgentGuard, LiteLLM gateway-proxy) overshoot 30/30; Token Budgets overshoots 0/30. Bars are proportional to
the upper Wilson bound on overshoot rate. The result replicates at the production price tier (gpt-4o, $2.50/$10 per Mtok) in §4.5 and across four additional caps
B0 ∈ {540, 5000, 10000, 20000} uc in §4.5.


the Rust affine conditions (C, D) reach the same 0/30: runtime                               does not compile, confirmed by three companion trybuild tests
monitoring achieves the outcome whenever the operator writes the                             with distinct rustc diagnostics. The distinguishing contribution
approach correctly, and Condition B’s locked variant is exactly the                          is therefore non-bypassability within typed source, not the cap-
M-delegation-fanout fix maintainers post in catalog threads. What                            respecting outcome itself.
Conditions C and D add is that the same outcome is mechanically                                  Conditions A and C differ in both allocation strategy
enforced by the type system—the racy pattern of Condition A                                  (shared budget vs. split allocation) and integrity layer (none
                                                                                                                                           12

                                     TABLE 5                           B0 = 60, per-child sub-budget is 20 uc, less than the per-child
   Five conditions isolate the integrity layer from both the language and the
                                                                       estimate (31 uc); the approach refuses each child at pre-flight.
     allocation strategy. Every disciplined condition reaches 0/30; only the
unguarded racy pattern (A) overshoots. The discriminator is operator discipline Condition D: Rust affine split (B0 = 100): Identical to
                                                                       condition C, but with parent budget raised to 100 uc. Per-child
 vs. compile-time enforcement, not Python vs. Rust: a correctly locked Python
counter (B) and a correctly locked Rust Arc<Mutex<Budget» baseline (E) sub-budget is now 33 uc, greater than the per-child estimate (31 uc);
both reach the same outcome as the affine conditions (C, D). What C/D add is
                    that the racy pattern (A) does not compile.
                                                                       the approach admits each child, each completes its LLM call, and
                                                                       total spend (69 uc) remains within the cap.
     Cond. Implementation                Integrity layer    Overshoot
                                                                                Condition E: Rust shared Arc⟨Mutex⟨Budget⟩⟩ with pre-
                                                                       flight reservation (B0 = 60): The shared-allocation Rust baseline
       A    Python racy (no lock)        none                30/30
       B    Python locked (asyncio.Lock) runtime discipline   0/30     that matches condition B’s allocation strategy: a single Budget
       C    Rust affine split (B0 =60)   compile-time         0/30     wrapped in Arc<tokio::sync::Mutex<...» is shared
       D    Rust affine split (B0 =100)  compile-time         0/30
       E    Rust Arc<Mutex<Budget»       runtime discipline   0/30     across three tokio::spawned children. Each child acquires
                                                                       the mutex, calls try_reserve(31), releases the mutex, makes
                                                                       the LLM call, then re-acquires the mutex to refund the unused
                                                                       reservation portion. This is the lock+pre-flight discipline a careful
vs. compile-time). Condition E separates the two: a Rust shared
                                                                       operator would write in Rust without using Budget::split;
Arc⟨Mutex⟨Budget⟩⟩ with operator-written lock discipline matches
                                                                       the approach is exactly condition B’s Python pattern translated to
Condition A’s shared allocation yet reaches 0/30. Both Rust
                                                                       Rust. Implementation: forgetful_operator/condition_
disciplines—split allocation (C, D) and shared-mutex-with-pre-
                                                                       e_rust_shared/src/main.rs. Like condition B, only one
flight (E)—attain the outcome, so the integrity layer’s distinguishing
                                                                       child’s reservation fits at B0 = 60 uc (the first to acquire the mutex;
property is non-bypassability across both patterns, independent of
                                                                       31 + 31 > 60), so the expected admit pattern is one-of-three; its
the allocation choice (§4.3.4).
                                                                       role is to separate the integrity-layer contribution from language —
                                                                       it is B’s lock discipline written in Rust without Budget::split.
4.3.1 Setup                                                                     Compile-fail evidence (trybuild): A companion crate at
                                                                       forgetful_operator/rust_compile_fail/ contains
Four implementations of multi-child budget enforcement, three
                                                                       three Rust translations of the racy Python pattern. All three must
concurrent children per trial, N = 30 trials each, against
                                                                       fail to compile for the structural claim to hold.
claude-haiku-4-5 (temperature = 0 for determinism).
Conditions A–C and E run at parent budget B0 = 60 uc; condition D               Estimator and per-child accounting: Per-child estimate
runs at B0 = 100 uc to demonstrate the approach admits all children    =   31 uc (byte-length margin 0.5× on a 392-character prompt plus
and stays cap-respecting when the cap is sized appropriately           max_output_tokens            = 30 at $5/Mtok output reservation). Ac-
for the workload. Full implementation in the artifact at token-        tual  per-call cost on claude-haiku-4-5         = 23 uc (deterministic
budgets-experiments/forgetful_operator/.                               at T  = 0) for  conditions A–D’s  catalog-derived  prompt. Condition E
                                                                       used a minimal probe prompt (25 input / 5 output tokens, actual cost
     Because temperature = 0 makes per-cell runs near-
                                                                       1 uc/call); the 31× over-reservation in condition E is load-bearing
deterministic, we report the 0/30 vs. 30/30 splits below as
                                                                       for the 0/30 result and represents the worst-case-for-the-discipline
a mechanism demonstration, not a statistical effect: interval
                                                                       scenario (a tighter estimate would admit more children, but the
estimates on these cells reflect the binomial under determinism,
                                                                       cap-respecting outcome is robust to this).
and population-level inference rests on the temperature-stratified
N = 160 sweep (§4.5).
         Condition A: Python racy (B0 = 60): A shared mu- 4.3.2 Results
table RacyBudget with no lock; can_admit(estimate)
checked before the LLM await, record_spend(actual) Compile-fail evidence (the structural result): all three
called after. This is the M-delegation-fanout pattern: under trybuild tests pass, meaning rustc rejected each Rust translation
asyncio.gather, the LLM await yields control mid-trial and of the racy pattern with the expected diagnostic:
sibling children pass can_admit on the same pre-spend state
                                                                           • shared_budget.rs (two children with the same
before any of them records.
                                                                              Budget) → E0382, “use of moved value: budget”.
         Condition B: Python locked (B0 = 60): The same shared
                                                                           • clone_budget.rs (.clone() attempt) → E0599, “no
budget with asyncio.Lock around an atomic try_reserve
                                                                              method named clone found for struct Budget”.
plus pre-flight reservation (refund after the LLM call returns). This
                                                                           • use_after_split.rs (parent reused after split) →
is the correct operator discipline, operationally equivalent to Agent
                                                                              E0382, “borrow of moved value: parent”.
Contracts’ runtime enforcement, AgentGuard’s in-process callback,
and LiteLLM proxy budgets.                                                  Live-API results: Table 6 reports the five conditions. The
         Condition C: Rust affine split (B0 = 60):                     race manifests in condition A in every one of 30 trials; the four
The parent Budget<10_000> is constructed via disciplined alternatives (B, C, D, E) record zero overshoot in every
BudgetMint::take_authority (capability-gated; requires trial. The split is categorical and deterministic at T = 0 — 30/30
the system-authority Cargo feature in the binary’s vs. 0/30 on a mechanism that does not depend on sampling — so
Cargo.toml) and split into three per-child sub-budgets via the contrast is read off the outcomes directly rather than from a
Budget::split. Each child receives its own Budget value significance test. (A pairwise Fisher’s exact test against A returns
moved into a tokio::spawn task. The type system prevents p = 1.69 × 10−17 for each of B, C, D, E, but because the within-cell
budget sharing: any attempt to use the parent after split or to replicas are near-deterministic the effective N is far below 30 and
alias a sub-budget across tasks is rejected at compile time. At we do not rest the claim on that figure.)
                                                                                                                                                                13

                                                                               TABLE 6
Forgetful-operator experiment: overshoot rates across five conditions, N = 30 trials each, three concurrent children per trial, against claude-haiku-4-5, T = 0.
Conditions A–C and E use parent budget B0 = 60 uc; condition D uses B0 = 100 uc to exhibit the approach’s admit-and-stay-safe regime. Per-replica Wilson 95% CI
  on 0/30: [0.000, 0.114]; pairwise Fisher’s exact test against condition A: p = 1.69 × 10−17 for each of B, C, D, and E. Per-cell effective N at T = 0 is below 30
 (asyncio scheduling is deterministic on this workload); these intervals are conservative. Raw data: forgetful_operator/results/ and forgetful_
                                                         operator/condition_e_rust_shared/.


                                 Condition                                 B0 (uc)     Overshoots    Mean spend      Admit/trial
                                 A: Python racy (no lock)                     60           30/30         69 uc          3.0/3
                                 B: Python locked                             60            0/30         23 uc          1.0/3
                                 C: Rust affine split                         60            0/30          0 uc          0.0/3
                                 D: Rust affine split                        100            0/30         69 uc          3.0/3
                                 E: Rust shared Arc⟨Mutex⟨Budget⟩⟩†           60            0/30          1 uc          1.0/3
† Condition E executed with a minimal prompt (25 input / 5 output tokens, actual cost 1 uc/call); the 31 uc reservation matches B’s pre-flight estimate. Per-trial

 admit pattern (1.0/3) matches Condition B exactly: shared budget plus pre-flight lock serializes one acquirer; remaining children refuse pre-flight regardless of
actual call cost. The 0/30 overshoot is robust to the 31× over-reservation; the structural parity-with-B claim is supported on the admit/overshoot dimensions, with
                                          the lower mean spend explained by prompt size rather than discipline difference.


4.3.3   What the experiment establishes                                              {50, 60, 69, 100} sweep (Table 6 and its companion) shows the racy
Each condition’s outcome traces to a single cause. A overshoots                      condition overshoots exactly when 3×per-child > B0 , while the
(30/30) because correct-looking sequential code races under                          affine and locked disciplines are safe at every cap—the racy code’s
asyncio scheduling: all three children pass can_admit on the                         safety is contingent on cap-sizing, the approach’s is structural.
same pre-spend state and proceed, spending 3 × 23 = 69 uc against                    (4) Allocation vs. integrity confound: Conditions A/C vary both
the 60 uc cap — exactly the M-delegation-fanout shape documented                     allocation (shared→split) and integrity layer (none→compile-time);
in 11 catalog rows. B is cap-respecting (0/30) because the operator                  Condition E (Rust shared Arc<Mutex<Budget» with operator-
added the missing discipline by hand (a lock around check-then-                      written lock) isolates the integrity layer and reaches 0/30, so the
act plus pre-flight reservation) and is, operationally, the runtime                  distinguishing property is non-bypassability across both the split-
alternative — Agent Contracts’ pre-flight refusal API. C is cap-                     then-spawn and shared-mutex patterns, not the allocation choice.
respecting (0/30) for a structurally different reason: the racy pattern              (5) Condition E prompt-size confound, conceded: E used a minimal
cannot be written (three trybuild translations fail to compile),                     stub prompt (∼1 uc/call) rather than the full LANG-001 prompt
and the version that does compile refuses each child at pre-flight                   of A–D; the qualitative mechanism-parity conclusion holds (the
because the per-child allocation (20 uc) is below the estimate                       arithmetic is invariant) but the matched-prompt re-run remains
(31 uc) — the same refusal-to-operate behavior as the sub-floor                      open. (6) Agent Contracts parity: it reaches Condition B’s outcome
caps of §4.5. D shows the discipline is not unconditional refusal:                   if its pre-flight API is invoked on every call site—the integrity-layer
when the cap absorbs 3× the estimate (per-child 33 > 31 uc), all                     distinction is that with our discipline the Budget type is the only
three children are admitted and complete within cap. E confirms                      callable interface, so the operator cannot bypass it, demonstrated
that a correctly locked Rust baseline reaches the same 0/30 as                       by the trybuild evidence (§4.1).
B, isolating the integrity-layer contribution from the choice of
language.                                                                            4.4   Threats to validity
    The A–E contrasts together establish three claims:                       Scope of the claimed contribution: The binary-level cap-
  1) Runtime alternatives (B in Python, E in Rust) can achieve the   soundness claim is unproven (Conjecture 1; we estimate ∼12
     cap-respecting outcome when the operator writes correct lock    person-months of Iris/RustBelt work to close it), and the Verus
     discipline (A overshoots 30/30; B and E, 0/30).                 mechanisation (66 obligations, 0 errors under Verus 0.18) has
  2) Compile-time integrity (C, D) achieves the same outcome         not been externally audited—its trust base (Z3 translation, SMT
     without requiring the operator to write that discipline (C and  soundness, rustc consistency per VerusBelt) is documented in §4.5.
     D, 0/30).                                                       Neither bears on the empirical contribution: the catalog and the
  3) The approach operates consistently across cap regimes: refuses  runtime cap arithmetic under Proposition 1’s assumptions stand
     when no admissible allocation fits (C), admits when it does     independently of the open binary-level obligation.
     (D), and is always cap-respecting (B, C, D all 0/30).                   Validity threats (compact four-fold framework): Internal
                                                                     validity. The catalog is drawn from public GitHub issues; initial
4.3.4 Threats to validity for this experiment                        coding was single-rater. An independent two-human IRR study
We concede six threats. (1) Constructed reproduction: the racy code (N = 113 re-annotation, κ = 0.837; per-class κ ∈ [0.727, 0.918]
is a minimal reproduction of the M-delegation-fanout pattern, not a with the fr/bu boundary identified as the codebook’s weakest
production extract; the catalog’s 11 such rows establish recurrence, seam) addresses the rater-independence threat (§2.1). Because the
the experiment establishes only the race rate at one parameter fr/bu boundary is convention-sensitive (κfr =0.727, the lowest
setting. (2) Mature runtime patterns avoid it too: actor systems and per-class figure), the confirmed/feature-request split should be
capability-secure runtimes prevent the race when correctly applied— read as convention-dependent; the catalog’s scope—the invariant
the comparison is against the operator-error baseline most common union of budget-primitive-missing issues across 21 frameworks—is
in the catalog (shared mutable counter under asyncio.gather), unaffected, and we anchor strong claims there. External validity.
and the distinguishing claim is only that Rust turns the race The 110-row catalog (63 confirmed incidents + 47 supplementary
into a compile-time error rather than a property the operator entries) is a convenience sample of public English-language
must remember to establish. (3) Parameter-dependence: a B0 ∈ failures; closed-source platforms (Cursor, Replit Agent) are absent.
                                                                                                                                            14

Prevalence claims are anchored on the 63 confirmed incidents, not             The remaining experiments (E8–E15 in Table 4) are confir-
the full 110. The Rust affine discipline applies to new Rust agent        matory: the cap holds under a sub-floor cap, a ten-cap sweep,
deployments only — a minority of the 2026 production ecosystem            multi-agent delegation, a 2,628-trial calibrated simulation, 382 live
(the per-framework summary in §2.5); the Python port provides             sessions, and a live N=1 Rust deployment (§4.6), at < 200 ns per
runtime discipline only. An independent baseline cohort (§2.3, 20         operation, with the capital-efficiency envelope characterized along-
keyword-neutral GitHub projects) confirms the mechanism clusters          side. These, together with the baseline comparisons (tokencap,
recur (12/20, 60% coverage) but is single-coder. Conclusion validity.     gateway, provider per-call caps, tokenizer-direct) and the Loom and
Microbenchmark variance is reported with Criterion confidence             trusted-computing-base checks, are detailed in the artifact; none
intervals (run-to-run ±3% on the test hardware); the head-to-             changes the paper’s claims.
head dollar comparisons use fixed deterministic token costs to
remove LLM nondeterminism from the mechanism comparison.                  4.6 Deployment case study: N=1 on a production Rust agent
Construct validity. The cap-respecting metric is operationally            framework
defined as “provider-billed total spend ≤ B0 at session end” under   The deployment-impact note (§6.6) observed that none of the
Proposition 1’s assumptions; the in-program integrity metric is      surveyed frameworks is written in Rust. To test whether the disci-
operationally defined as “the racy multi-child pattern is rejected   pline transfers to a real Rust agent runtime rather than a synthetic
by the borrow checker at compile time in typed Rust source code”     harness, we integrated the crate into Rig (rig-core 0.37), a
under the trybuild evidence (§4.3).                                  Rust LLM-agent framework in production use. The integration is a
        Residual exposures: Beyond the four-fold framework, three    ∼40-line adapter: a shared BudgetPool holds the session dollar
deployment-time exposures survive the approach, each detailed        cap, and each delegated call reserves its worst-case cost pre-flight,
where it arises: the actual_charge trust assumption (A7; §3.4),      runs the Rig completion, then reconciles the actual cost and returns
rate-stability (A8; §4.5), and the capital-efficiency trade-off (§4.5).
                                                                     the unspent remainder to the pool. Rig itself was not modified.
None is closed by the type system.                                       Single-agent cap enforcement. On a 40-task workload
                                                                     (claude-haiku-4-5, $0.05 cap, per-call output bounded to
                                                                     100 tokens), a representative run served 22 tasks and refused 18
4.5 Broader evaluation (summary; full results and tables in
                                                                     pre-flight once the cap was reached, with zero cap overshoot and
the artifact)
                                                                     zero reservation under-counts on live traffic (final spend $0.0404 ≤
Beyond the head-to-head (E2) and forgetful-operator (E3) exper- $0.05; the unguarded workload is projected to cost $0.073, a 1.5×
iments above, the artifact reports further evaluation. We refer to breach). Measured over-reservation was 5.64×, consistent with the
experiments by their Table 4 identifiers; full per-cell results for 4–6× band reported for the byte-length estimator (§4.5); it is an
all of them ship in the artifact. Four bear directly on the paper’s estimator-side figure (byte-length estimator on both sides), not an
claims and are summarized here.                                      independent billing measurement, and varies run-to-run with the
        Cap-respecting under independent sampling (E5): A model’s output lengths.
temperature-stratified test (T ∈ {0, 0.3, 0.7, 1.0}, N = 160, two        Multi-agent fan-out (non-bypassability). The distinguishing
production-tier models) reports zero cap violations and zero false claim is not single-agent cap enforcement — which a counter also
refusals. Because T > 0 removes the near-determinism of the achieves (§4.3) — but that no sub-agent can bypass a shared budget
T = 0 cells, this is the genuinely-independent evidence for the cap- under delegation. We ran four sub-agents concurrently against one
respecting claim; the T = 0 sweeps are reported for completeness, BudgetPool ($0.05 cap). The pool enforced the cap globally:
not as independent observations.                                     cumulative spend was $0.0400 across all four sub-agents ($0.05
        Operational parity with concurrent work (E4):                cap respected, invariant_holds true throughout), and the
A      production-tier     head-to-head      on    gpt-4o       and per-sub-agent allocation was first-come-first-served (11/4/6/2 calls
claude-haiku-4-5 at a discriminating cap (B0 = 2,000 uc, served). The property is enforced at two levels. At runtime, every
where the cap admits some calls) puts TB-Rust, a properly locked reservation is checked against the shared pool, so the global cap
Python counter, and Agent Contracts [25] at 0 overshoot with the binds regardless of fan-out width — a deterministic eight-sub-agent
same admit-then-refuse pattern. At the cap-respecting outcome the stress test of this invariant ships in the artifact. At compile time, a
type system is therefore at parity with a correctly-written runtime Reservation (a sub-agent’s budget slice) is affine (move-only):
monitor — consistent with the forgetful-operator finding that its a trybuild suite confirms that cloning it (rustc E0599) or
distinguishing value is non-bypassability, not the outcome itself.   spending it twice (E0382) is a compile error, so a sub-agent cannot
        Estimator soundness (E7): A1 is checked against An- fabricate or duplicate budget.
thropic’s count_tokens oracle on two distinct samples that               We claim no more than a single deployment: one framework,
measure different things and are not summed: the per-assumption one provider, one workload. It demonstrates that the discipline
calibration-plus-hold-out set behind the guarantee map’s A1 composes with a real Rust agent runtime at low integration cost,
row (Table 2, N = 178), and a separate, larger family of three enforces a hard session cap soundly across concurrent sub-agents,
independent hold-out sweeps (N = 243; per-sweep CSVs under and backs non-bypassability with a compile-time guarantee —
refund-live/ and multiway/ in the artifact). Both report the affine thesis exercised end-to-end rather than in isolation. It
zero estimator-soundness violations, with at least 2.32× safety on does not establish behavior across frameworks or workloads. The
adversarial corpora.                                                 integration crate, the concurrent stress test, and the compile-fail
        Single-agent isolation (E6): On single-agent cap-respecting, suite ship in the artifact (rig-integration/).
a 4-line Python counter with the same estimator matches TB-Rust
at 0/30, confirming that the type system adds nothing to the 4.7 Deployment recommendation
single-agent outcome; its value is the multi-agent non-bypassability The deployment matrix is in §1.5 (Table 3); the contexts where the
isolated by E3.                                                      approach is the wrong tool are enumerated in §6.3. The empirical
                                                                                                                                             15

evidence above supports the matrix’s positive recommendations           literature search across SE, PL, and AI-systems venues 2023–2026
(new Rust agent deployments with cumulative-session cap re-             surfaced no prior work applying compile-time affine or capability
quirements; capital-tolerant deployments via the static estimator;      typing specifically to LLM dollar cost. The technique transfer is
prepay-account deployments via the AdaptiveEstimator) and its           the contribution; the underlying substructural-types and capability-
negative recommendations (Python-only deployments, single-              resource patterns are decades-established.
provider deployments with server-side caps, reasoning-model                  The forgetful-operator experiment (§4.3) isolates what compile-
deployments where Token Budgets is a complement to provider-            time integrity uniquely catches over Agent Contracts’ runtime layer:
side controls rather than a replacement).                               the M-delegation-fanout race is rejected by the borrow checker at
                                                                        compile time in Rust per the trybuild compile-fail evidence,
                                                                        while the runtime alternative reaches the same cap-respecting
5     R ELATED W ORK
                                                                        outcome only with correct operator discipline (30/30 overshoot for
5.1   The three-layer enforcement taxonomy                              the racy Python pattern vs. 0/30 for three disciplined alternatives).
§2.7 introduced the three-layer view (compile-time, software/run-                Head-to-head update on LANG-001: We re-ran the Agent
time, transport/network) and placed Token Budgets at the compile-       Contracts head-to-head on LANG-001 at matched parameters
time layer. Here we relate the work to specific systems at each         (N = 30, claude-sonnet-4-5, T = 0, cap = 540 uc) using ai-
layer.                                                                  agent-contracts v0.3.2. The ContractedLLM context manager
        Compile-time layer and concurrent work: Concurrent              raised an internal state-transition error on every trial in our
work by Ye and Tan [25] (arXiv:2601.08815, COINE 2026)                  Python 3.12 environment; we worked around this by using
introduces Agent Contracts: a formal framework for resource-            the Contract/ResourceConstraints types directly and
bounded autonomous AI with multi-dimensional resource con-              enforcing the cap via litellm.completion calls. Result:
straints and conservation laws under multi-agent delegation. Their      30/30 pre-flight refusals on Agent Contracts, 30/30 pre-flight
evaluation reports 90% token reduction and zero conservation            refusals on Token Budgets; zero API calls and zero overshoots
violations. Agent Contracts and Token Budgets address the same          on either side. Estimated per-call cost at LANG-001 prompt length
operational problem (cost-bounded LLM execution) from different         on Sonnet rates was $0.003271, 6.06× the cap, so pre-flight
angles: both use pre-flight refusal of cap-violating calls (confirmed   refusal is the operationally correct behavior for any pre-flight
empirically in two head-to-head experiments: the gpt-4o trivial-cap     discipline at this cap. At B0 = 540 uc both frameworks tie via
comparison (§4.5, both frameworks 0/30 overshoot at B0 = 540 uc)        refusal-to-operate; a higher-cap protocol that would discriminate
and the claude-haiku-4-5 discriminating-cap comparison                  the two mechanisms (both must admit sub-cap calls and then refuse
(§4.5, three-way parity with TB-Rust at B0 = 2,000 uc; all three        the cap-violating call) is pre-committed and partially executed
frameworks admit one call and refuse the second via pre-flight)).       (higher-cap commit, prior to submission): Token Budgets recorded
    The two differ in the integrity layer that supports that refusal.   90/90 within-budget completion on a self-terminating workload
Ye and Tan provide an inter-agent contract layer with runtime           variant; Agent Contracts recorded 90/90 framework-unavailable
cost monitoring; we provide an in-process affine-type layer with        due to v0.3.2 API drift (the ResourceConstraints fields
compile-time integrity (budgets that cannot be cloned, double-          renamed from max_input_tokens/max_output_tokens
spent, or used after delegation). The two are complementary; a          to tokens/cost_usd/api_calls). Per the pre-committed
deployment could plausibly use Agent Contracts at the multi-agent       stopping rules, the first execution is reported as a null result for the
coordination layer and our affine discipline within each agent. Ye      discriminating-cap protocol, not as a finding for or against either
and Tan’s COINE 2026 paper predates ours by approximately four          framework. We subsequently executed a corrected harness using the
months on arXiv.                                                        Anthropic tools API to force a multi-step retry, reported in §4.5
    The runtime mechanism itself (pre-call reservation with conser-     (the Agent Contracts comparison (artifact)): all three frameworks
vative estimation) is not novel. tokencap [32] implements the           (TB-Rust, TB-Python, Agent Contracts) record 0 overshoot at the
same pattern as a Python runtime wrapper; LiteLLM from v1.50            discriminating cap B0 = 2,000 uc, Fisher’s exact p = 1.0 on every
onwards ships virtual-key budgets with per-request enforcement;         pairwise comparison. Full protocol, harness, and per-trial CSVs in
Microsoft’s Semantic Kernel exposes ITokenizer for                      the public artifact.
pre-flight token estimation. OpenAI’s API now exposes max_                       Software/runtime layer: Production runtime cost guards
completion_tokens as a server-side hard cap (2025), which               include AgentGuard-style budget callbacks [13], paper-
is operationally stronger than any client-side cap (it cannot be        clipai’s monthly-budget feature, the proposed nanobot
bypassed) but does not support per-agent granularity or aggregate       maxCostPerMessage, and LangGraph’s checkpointer-
budgets spanning multiple providers. Anthropic’s prompt caching         callback recipe. Each of these checks after a call has been issued
(2024) further complicates the cost model: agents that re-use a         and admits one overshooting call per session.
system prompt see input costs at 0.1× the non-cached rate, shifting              Adjacent literatures positioned: The approach sits at the
the estimator’s calibration baseline. Our contribution is not the       intersection of three established lines: (i) substructural and resource-
runtime mechanism but the compile-time integrity layer that none        aware typing (Wadler’s linear types [1]; RAML/AARA [34], [52];
of these systems provide: budgets that cannot be cloned, double-        Linear Haskell [53]; quantitative type theory [41]; Liquid Haskell’s
spent, or used after being delegated.                                   refinement types [50] can express bounded numeric invariants
    The closest prior substructural-resource patterns are               such as {n : Int | n ≤ cap} at the type level, the closest type-
tower::Limit [30] (counter behind runtime check), Tokio time            system precedent to expressing cumulative-cost bounds, though it
budgets [15] (deadline propagation), and EVM gas metering [36]          lacks Rust’s affine delegation-across-boundaries property) — our
(pre-execution reservation, transport-level enforcement). The affine    discipline is structurally weaker (a single capability value, runtime
application pattern itself is established (Move for blockchain [22],    cap arithmetic) but applied to a new domain (LLM dollar cost)
seL4 capabilities [23], governor [24], Tokio semaphores [16]). A        where post-hoc external pricing prevents intrinsic bound derivation;
                                                                                                                                             16

(ii) capability-based authority and ocap (KeyKOS [42], EROS [43],        5.2   Adjacent work
seL4 [23], CHERI [44], Joe-E [45], Pony [26], Capsicum [76])
— BudgetMint is a direct application: a non-forgeable handle             We position the approach against the adjacent literatures whose tech-
whose construction is gated by a feature-flag-enabled authority; the     niques it transfers to post-hoc-priced LLM cost. Substructural and
closest production analogue is tower::Limit [30] (a runtime              resource-aware typing—linear types [1], [53], AARA (RAML [34],
counter), which we lift to compile-time within the trust boundary        probabilistic AARA [37], [51]), quantitative type theory [41],
of Budget::new; (iii) smart-contract gas metering and pre-               session types [59], typestate (Plaid [11], [77], Obsidian [78],
flight reservation (EVM gas [36], KEVM [35], GASTAP [47],                Vault [79]), graded modalities (Granule [67], [68]), and refinement-
MadMax [48], Move’s bytecode verifier [22], CosmWasm/NEAR/-              type Rust (RefinedRust [40], RustHorn [39])—all encode resource
Solana compute units [60]–[62]) — the structural difference is           discipline in the type system. Our Budget is a degenerate-
the locus of the cost function: in gas/fuel, the cost is intrinsic and   typestate case (two states, live/moved) in stock Rust, structurally
pre-computable; in our setting, the cost is determined post-hoc          weaker than graded resources but specialised to a domain where
by an external party (provider’s tokenizer + pricing), requiring         post-hoc external pricing precludes intrinsic bound derivation;
the estimator-based reservation pattern of §3.4. KEVM and                we use Verus [31] (on VerusBelt [33]) for the source-level
GASTAP close the analogous source-to-binary refinement proof             mechanisation because its integer obligations discharge under
that Conjecture 1 leaves open; we estimate a substantial refinement-     SMT. Linear assets and capability security—Move’s bytecode-
proof effort to reach equivalent guarantees.                             verified linear assets [22] are stronger (a dropped value is a verifier
        Cloud cost governance and provider-tier spending controls:       error) but require a custom VM; our affine relaxation forfeits an
AWS Budgets [49] with budget actions enforce per-account                 unspent balance silently, the stock-Rust compromise. The ocap
caps at the provider tier with automatic service revocation on           tradition (KeyKOS [42], EROS [43], seL4 [23], CHERI [44], Joe-
threshold breach; AWS Bedrock additionally exposes session-level         E [45], E [46], Pony [26]) motivates BudgetMint, which lifts
budget actions and Bedrock Guardrails for prompt-, response-             the runtime-counter pattern of tower::Limit [30] to a compile-
, and topic-level filtering. OpenAI’s organization-tier spending         time gate. Gas metering—EVM/KEVM/GASTAP/MadMax [35],
limits (introduced 2024, exposed via Settings → Limits and the           [36], [47], [48] supply the source-to-binary refinement Conjecture 1
Usage API) and Anthropic’s per-workspace spend limits play the           leaves open, but price cost intrinsically; ours is fixed post-hoc
same role on their platforms. GCP Billing Budget API [63] and            by the provider tokenizer (hence the estimator-based reservation
Azure Cost Management offer analogous account-level quotas.              of §3.4). The verified-systems refinement lineage is the closer
These provider-side mechanisms are operationally stronger than           methodological analogue for the binary obligation; the residual
any client-side discipline within their scope (they cannot be            gap is that A1/A6/A7/A8 stay external trust assumptions no proof
bypassed by client code) but are strictly less granular: they cannot     can close. LLM cost tooling—production gateways (LiteLLM
enforce per-agent budgets within a single session, or aggregate          proxy budgets [27]) and observability platforms (Langfuse [86],
caps spanning multiple providers, or pre-flight refusal at sub-          Braintrust [87]) observe after the call; tokencap [32] is the
session granularity. Conceptually the pre-flight reservation pattern     closest in-process pre-flight comparator (§4.5); FrugalGPT [29]
is admission control under a resource quota: the same shape as           contributes a per-prompt predictor complementary to our integrity
cluster-manager reservation accounting (Borg [54], Kubernetes            layer; DSPy’s “compilation” [75], [85] is program-synthesis, not a
resource quotas [55]), fair-share and rate schedulers (dominant          runtime cap (the DSPY-001/003 incidents, §2.4), and composes
resource fairness [73], mClock [74]), and token-bucket admission         with an affine Budget. Provider-side and quota infrastructure—
at API gateways (Stripe [72], Envoy [69], Istio [70], Kong [71],         AWS Bedrock session budgets, OpenAI/Anthropic org caps, and
and the classical token bucket [56]). The transfer to LLM cost is        gateway/cloud limiters (Envoy [69], Stripe [72], Kubernetes [55])
not the admission mechanism — which is decades old — but the             are kernel-enforced and thus operationally stronger where they
locus of the resource estimate: cluster and network quotas meter a       apply, but coarser (account-/org-level, single-provider); the in-
resource whose consumption is known at admission time, whereas           process affine layer is the inner wall for the per-session, cross-
LLM dollar cost is fixed post-hoc by an external tokenizer and           provider deployments they do not reach—a complement, not a
price list, which is why the reservation must be a conservative          replacement.
estimate (§3.4) rather than an exact debit. The recommended-                     Adversarial cost amplification and agent operational safety:
production pattern is layered: provider-side caps as the outer wall,     Two adjacent threat surfaces sit next to the benign overruns
plus per-agent in-process enforcement (this paper’s contribution         the catalog documents. The first is economic denial-of-service:
within Rust, or runtime alternatives like AgentGuard/LiteLLM in          an adversary (or a compromised upstream tool) deliberately
other languages) as the inner layer. The decision matrix (Table 3)       amplifies token consumption—“denial-of-wallet” patterns and
places this approach in the cells where provider-side mechanisms         prompt-injection-driven tool-call inflation—to run up a victim’s bill.
are absent or insufficient.                                              The second is the broader literature on operational safeguards for
                                                                         autonomous agents (loop and recursion bounds, kill switches,
        Transport/network layer: ATXP [14] returns HTTP 402
                                                                         human-in-the-loop gating), which the upstream failure-mode
Payment Required when an agent’s wallet depletes, delegating cost
                                                                         surveys we draw on in §2 situate within agent reliability rather
enforcement to a payment-aware HTTP gateway. The guarantee is
                                                                         than cost. Our discipline is not an adversarial defense: a caller
wallet-level, not call-level: the gateway cannot prevent overshoot
                                                                         with access to Budget::new or operating outside the Rust
within an in-flight request.
                                                                         trust boundary can mint or sidestep budgets, and an estimator
    The three layers compose: an operator can deploy compile-time        calibrated on benign prompts can be driven outside its margin by
discipline (this work) with a runtime budget guard for in-process        crafted inputs (§6.2). What the approach does provide against both
sanity checks and a transport-layer wallet for organization-level        surfaces is consequence-bounding: whatever the trigger, in-program
quotas.                                                                  spend cannot exceed B0 under Proposition 1’s assumptions. We
                                                                                                                                           17

therefore position cost caps as orthogonal to, and composable with,       micro-cents is the estimator’s job, governed by the chain billed ≤
adversarial-input defenses and agent-safety controls rather than as       rate × billable_tokens ≤ rate × estimator(prompt) = reserved_uc).
a substitute for either.                                                      A deployment whose actual prompt distribution includes
                                                                          patterns the calibration corpus did not cover — adversarial
6     D ISCUSSION AND L IMITATIONS                                        nested-tool-schemas beyond the audit, novel provider-side prompt-
                                                                          rewriting machinery, or a future tokenizer rotation increasing
6.1   Failure modes not addressed by this discipline
                                                                          the worst-case byte-to-token ratio above 2.0× — can experience
Six failure modes lie outside the approach’s coverage, collected          binary-level overshoot even on a Rust binary that passes Verus
here as a single reference list. The integrity claim and Proposition 1    verification and the trybuild suite. The compile-time machinery
are silent on every item below; operators deploying Token Budgets         does not catch this. The affine discipline still matters because
retain residual exposure to each.                                         estimator-only deployments (tokencap, AgentGuard, LangSmith,
  1) Provider billing misreport. The cap-respecting bound                 LiteLLM proxies) have to solve both integrity and cap-respecting
      silently undercounts spend when a provider’s usage field is         at runtime, typically through ad-hoc Python wrappers. Our N = 30
      incomplete, because ReservationReceipt::confirm                     head-to-head against tokencap (§4.5) shows what happens when
      accepts an operator-supplied actual_charge without                  the integrity layer is missing: tokencap achieves its design target
      independent verification (pydantic-ai #5445, #5379, #5304,          on token tracking but 30/30 dollar overshoot at every cap because
      #5302). Detail: §3.4.                                               its enforcement window admits the call that pushes cumulative
  2) Reasoning-model hidden tokens. A6 is structurally vio-               spend over the cap. Layer composition. Token Budgets combines
      lated: providers bill for thinking tokens not bounded by            a static layer (linear ownership, no quantitative resource analysis)
      max_output_tokens. Operators must use provider-side                 with an empirical layer (audited estimator margin). The operational
      controls (reasoning_effort, thinking.budget_                        guarantee is no stronger than the weaker of these two layers; the
      tokens) and recalibrate the session-cumulative reservation          contribution is that combining them strictly dominates either alone
      per configuration. Detail: §6.8.                                    on the operational metric ($ cap-respecting on multi-step agent
  3) Canceled-stream partial usage. When a streaming re-                  workloads) that the catalog identifies as the binding failure mode.
      sponse is canceled mid-flight, the terminating usage event
      may never reach the client; ReservationReceipt::
                                                                          6.3   When Token Budgets is not the right choice
      confirm sees an undercount. The approach cannot detect
      this from client state alone. Detail: §6.8.                         The decision matrix in §1.5 (Table 3) names the contexts where
  4) Tokenizer-version drift. Mid-session provider tokenizer              this discipline is preferred. The mirror question — the contexts
      changes invalidate calibration without warning; a deployment        where it is the wrong tool — collapses to six dimensions, each
      that does not pin tokenizer versions in build metadata can          keyed to a row of the matrix.
      silently lose A1 between releases. Detail: §4.5.                        Language. The approach’s compile-time integrity property
  5) Server-side prompt rewriting. The provider may in-                   requires Rust’s affine ownership. Python-only deployments (the
      ject system text after the client sends the request                 bulk of the catalog’s framework distribution, the per-framework
      (tool-description expansion, cached-context expansion);             summary in §2.5) should use the existing runtime mitigations
      AnthropicEstimator captures the dominant case em-                   (AgentGuard, LiteLLM virtual-key budgets) plus the experimen-
      pirically, but adversarial server-side rewriting is not ruled out   tal Mypy plugin POC (§7.1); full compile-time enforcement
      by any invariant. Detail: §4.5.                                     would require a Rust-language adoption or a production-grade
                                                                          Python static-analysis plugin beyond the POC currently shipped.
  6) Multi-tenant cross-process budgets. The affine Budget
                                                                          Provider-side caps available. Where the deployment is single-
      lives in one Rust process; multi-replica budget arithmetic
                                                                          provider and the provider already exposes session-level cumu-
      requires the distributed reservation service sketched but not
                                                                          lative caps (OpenAI max_completion_tokens, Anthropic
      implemented in this work. Detail: §6.7.
                                                                          per-workspace caps, AWS Bedrock session-level cost controls),
    The six rows above are the operationally significant exposures
                                                                          those controls are kernel-enforced and operationally stronger
a deployment retains under this approach. Section 4.5 gives the
                                                                          than any client-side discipline. Reasoning models. OpenAI o-
complementary list of formal obligations the mechanised speci-
                                                                          series, Anthropic extended-thinking, DeepSeek-R1, and Gemini
fications do not discharge (binary-level refinement, LLVM/rustc
                                                                          Thinking structurally violate A6: providers bill for thinking tokens
correctness, provider billing semantics, network nondeterminism,
                                                                          not bounded by max_output_tokens. Operators should use
tokenizer evolution, reasoning-model hidden tokens, multi-tenant
                                                                          provider-side mechanisms (reasoning_effort, thinking.
cross-process budgets).
                                                                          budget_tokens) as the primary per-call control, optionally com-
                                                                          bined with Budget::spend_with_reasoning for session-
6.2   Estimator soundness as the principal dependency                     cumulative budgeting on top (§6.8). Micro-budget regimes.
The approach’s binary-level cap-respecting behavior rests far more        At budgets below the per-call worst-case reservation, pre-flight
heavily on estimator soundness (A1) than on the affine type               refusal degenerates to denial-of-service for legitimate small tasks.
machinery. The cap-respecting end-to-end claim decomposes into            Tokenizer-direct estimation (§4.5) recovers capital efficiency
two independent properties: the integrity property (compile-time,         at ∼1,000 ms per-spend latency. Multi-tenant cross-process.
type-system enforced; once a Budget value is constructed with             Budget lives in one Rust process. Multi-replica budget state
capacity M, no path through the typed source code can spend,              requires the distributed reservation service sketched in §6.7 but not
split, or merge more than M accounted micro-cents) and the                implemented here. Capital-cost-sensitive deployments. The static
cap-respecting property (operational, estimator-dependent; the            byte-length estimator records 6.20× mean over-reservation, which
relationship between accounted micro-cents and provider-billed            on prepay accounts is real locked capital. Operators for whom this
                                                                                                                                            18

trade-off is unacceptable should adopt tokenizer-direct estimation            The eight-category mechanism taxonomy is exploratory. A
(∼100% capital efficiency at the latency cost) or provider-side          blind second-rater pass over all 110 rows gives moderate cluster-
caps.                                                                    assignment agreement (Cohen’s κ = 0.44, 95% CI [0.34, 0.55], N =
                                                                         110). Two mechanisms are reliably identified—cost-observability
                                                                         (κ = 0.78) and multimodal-cost-amplification (κ = 0.65)—while
6.4 Where the discipline rejects valid programs (false posi-
                                                                         the remaining boundaries overlap. The disagreements concentrate
tives)
                                                                         where an incident genuinely exhibits more than one mechanism (for
In deployments where the approach is the right choice, what classes      example, a “disable retry on timeout” request whose ignored max_
of legitimately-correct programs does it nevertheless reject? Five       retries option makes it at once a retry-loop and a dropped-
classes: (F1) programs whose actual spend depends on a future            provider-option case) and where the single-agent/multi-agent line
condition the static analysis cannot resolve (manifests as capital-      between retry-loop and delegation-fanout is fine. We therefore
efficiency loss, 6.2× median over-reservation, not as refused calls);    present the eight clusters as a descriptive organization of the corpus
(F2) programs that legitimately consume budget across hidden re-         rather than a validated taxonomy, and we do not rest quantitative
entry (recursive agent patterns require either worst-case reservation    claims on precise per-cluster counts; the four-class confirmation
at the outermost frame or refactor to iterative loops); (F3) programs    labeling, by contrast, is IRR-validated (κ = 0.837). The case-type
that legitimately defer budget commitment across asynchronous            codebook (§2.2) was finalized after all retained issues were clas-
task boundaries (no “conditional reservation that materialises later”;   sified at the bug-fixed/bug-unfixed/feature-request/
workarounds via BudgetPool with closure-based reservation                borderline level (the level at which the headline two-coder
recover cost-zero-unspent at the cost of a closure-shaped API);          IRR κ = 0.837 is reported; the confirmed-bug subset reaches
(F4) programs that legitimately share budget across independent          κ = 0.943). The further partition of the 110 retained rows into
agents (the broadcast-cost-once pattern from ATGN-018 cannot             the eight mechanism clusters (M-delegation-fanout, M-retry-loop,
share a single Budget instance; BudgetPool provides explicit-            M-context-amplification, etc.) was single-rater, performed without
coordination workaround); (F5) programs whose authors prefer             an independent re-coding pass. We therefore present the eight
trust-the-runtime to static enforcement (legitimate calibration of       mechanism clusters as a single-coder interpretive synthesis intended
soundness–utilization trade-off; explicitly out of scope, §6.3). None    to organize the catalog by proximate cost mechanism, not as a
of F1–F5 is an unsoundness; all are utility losses paid in exchange      reliability-tested per-row classification instrument. We do not report
for the integrity property. For deployments where catalog failure-       inter-rater agreement on cluster assignment, and we do not claim the
mode costs dominate F1–F5, the trade-off favors the approach; for        eight clusters are exhaustive or hierarchically optimal. Consistent
converse cases, F1–F5 are dispositive reasons to choose a different      with this scoping, the cataloguing notes record eleven rows with
mechanism.                                                               genuine cross-cluster character (e.g. a delegation-fanout incident
                                                                         that is also context-amplification), which we take as direct evidence
                                                                         that the mechanism boundaries are soft rather than crisp; a forced
6.5   What the discipline does not solve
                                                                         single-label coding would understate that softness. A second-rater
Four structural limitations are detailed elsewhere and summarized        pass over the incidents with the cluster codebook as the label
here only to keep the boundary in one place: multi-tenant cross-         space is identified as catalog-v2 follow-up; it would convert the
process budgets (§6.7), reasoning-model hidden tokens (§6.8),            taxonomy from an organizing device into a validated instrument
Python and TypeScript ecosystems that require runtime-only ports         without changing the four-class IRR already reported.
(§6.3), and the trusted Budget::new constructor (§4.5). One                   No deployment study; the evaluation is synthetic and live-
limitation is specific to the choice of affine over linear typing:       API. The empirical evaluation comprises a 63-incident catalog, a
an unspent Budget is forfeited on Drop rather than statically            six-runtime head-to-head, a temperature-stratified live-API sweep,
required to be resolved, because Rust provides affine, not linear,       the M2 isolation experiment, the Forgetful-Operator experiment,
types. Move’s bytecode verifier offers the stronger must-resolve         and the Agent Contracts discriminating-cap head-to-head. None
guarantee at the cost of a custom VM (§A.3); we accept the weaker        of these is a longitudinal deployment study; we do not report
guarantee as the stock-Rust compromise.                                  incident-reduction data from a real operator adopting the approach,
                                                                         developer-usability metrics, or maintenance-burden analysis. The
                                                                         crate is deployed in internal non-production systems but not
6.6   Empirical methodology limitations
                                                                         in production infrastructure at any third-party organization we
Three limitations on the empirical contribution are conceded             can name. A twelve-month deployment study with a partnering
explicitly, beyond the per-experiment threats reported in §4.4.          organization is identified as the highest-leverage follow-up for
    The catalog documents recurrence, not ecosystem preva-               strengthening the operational claim; in the meantime the paper’s
lence. The 63 confirmed incidents establish that the budget-overrun      claim is bounded to “the approach prevents the M-delegation-fanout
failure class recurs in the 21 sub-projects identified by our keyword-   race in synthetic and live-API experiments,” not “the approach
driven sampling protocol, not that it is necessarily prevalent           reduces production incidents.”
across the wider LLM-agent ecosystem. A denominator-based                     Assumption A7 (provider usage truthfulness): fault-
prevalence study (incidents per active user, per KLOC, per project-      injection results. Proposition 1 is proven conditional on A7:
age, or incidents-per-feature-request) would require ecosystem           the provider’s reported actual_charge on a successful call
telemetry access we do not have; it is identified as catalog-v2          truthfully bounds the operator’s spend. The catalog itself documents
follow-up. Reviewers and replicators should read the catalog as a        four pydantic-ai incidents (#5445, #5379, #5304, #5302) where the
recurrence proof for the named sub-projects and frameworks, not          usage field is missing or wrong, so A7 is empirically known to fail
as a prevalence estimate for the population of all LLM-agent code        in production. To quantify the consequence, we ran a fault-injection
in deployment.                                                           study simulating a provider that under-reports usage by a factor k.
                                                                                                                                                   19

                                     TABLE 7                                     retry-loop workload is run. We identify a RAG-pipeline evaluation
   A7 fault injection: provider under-reporting by factor k vs. cap-respecting   as the highest-priority workload extension.
behavior. 1,000 sessions per row, B0 = 2,000 uc, bootstrapped from 1,000 real
   (reservation, actual) pairs (A1 holds on all). At k = 1 (truthful
 provider) the approach is cap-respecting, confirming Proposition 1 under its
                                stated assumption.                               6.7   Multi-tenant deployment via distributed reservation
                                                                                 The affine Budget is single-process; production multi-tenant
                 k     overshoot      mean over cap       max over cap           deployments (an LLM proxy serving N sessions across multiple
                                                                                 replicas behind a load balancer) require a distributed reservation
    1.0 (truthful)       0/1000                 0.0%               0.0%
               2.0     666/1000                13.9%              39.3%          service. The natural extension — in the spirit of Spanner’s bounded
               5.0    1000/1000               137.9%             172.0%          reservations or a RAFT-replicated counter — holds the authoritative
             10.0     1000/1000               354.4%             395.4%          Budget::available per session, and a Rust agent acquires
                                                                                 a typed reservation lease by RPC (a bounded, revocable lease in
                                                                                 the sense of Gray and Cheriton [58]); the lease is locally affine, so
We bootstrapped 1,000 real (reservation, actual-cost)                            within a process the existing discipline guarantees no duplication,
pairs from our live-API corpus — on which A1 holds for every pair                and on confirm the agent reports actual spend back to the service
(reservation ≥ actual on all 1,000; mean effective margin 1.64×)                 for atomic reconciliation. The architecture follows the classical
— sampling the pairs jointly so the estimator’s conservativeness                 Saga pattern of Garcia-Molina and Salem [57]: a long-running
is preserved and only A7 is perturbed. We ran 1,000 sessions per                 distributed transaction is decomposed into a sequence of local
condition at B0 = 2,000 uc (Table 7).                                            sub-transactions, each with a compensating action. Our adaptation
    At k = 1 the approach is cap-respecting in all 1,000 sessions (0             maps the budget-spend pipeline onto this structure: reservation
overshoot, 95% CI [0.000, 0.004]), confirming Proposition 1 holds                acquisition is the local sub-transaction, confirm/forfeit are
exactly when A7 holds. Under-reporting degrades this sharply and                 its compensations, and the affine Budget handle is the local-
undetectably: at k = 2, 666/1,000 sessions overshoot (mean 13.9%                 invariant carrier within each process. The novelty relative to the
over cap); at k = 5 and k = 10, every session overshoots (mean                   classical Saga is not the orchestration pattern—which is 40 years
137.9% and 354.4% respectively). The approach cannot detect the                  old—but the integration with compile-time affine ownership at the
violation because the ledger observes only reported charges, so                  per-agent layer: the local sub-transaction’s integrity property (no
it admits calls whose true cost has already exhausted the budget.                double-spend within a process) is established by the type system
A periodic reconciliation layer that polls ground-truth billing                  rather than by careful operator-written compensation code. The
and corrects the ledger substantially mitigates this. In a matched               implementation challenge is reconciliation under partial failures
run at k = 5 (baseline 1000/1000 overshoot, mean 138.0%, max                     (network partitions during confirm), which is the same challenge
171.3%), reconciling every three calls reduced the overshoot rate                any Saga implementation faces; full implementation and evaluation
to 593/1000 and the mean magnitude to 22.9% (max 52.6%),                         is future work.
bounding the damage to roughly one reconciliation window. We
do not ship reconciliation in the current crate; the simulation
                                                                                 6.8   Reasoning-model and streaming hidden tokens
establishes it as a concrete mitigation path. This confirms A7
as a genuine trust boundary shared with every client-side cost-                  Reasoning models (OpenAI o1/o3, Anthropic extended-thinking,
accounting mechanism in the catalog; the approach is a best-                     Gemini thinking) bill for internal-reasoning tokens not returned
effort layer against an honest provider, not a guarantee against a               in the visible output; these can be 5–50× the visible volume
Byzantine one, and deployments that cannot trust usage reporting                 and dominate cost. Pre-call reservation cannot know the actual
must reconcile against billing out-of-band.                                      reasoning-token count, so over-reservation on reasoning-heavy calls
    Dependency-tree unsafe surface is not quantified.                            is correspondingly larger (observed 12–40× on extended-thinking
#[forbid(unsafe_code)] applies to the workspace root,                            workloads). The empirical mitigation pattern of §4.5 closes this for
not to transitive dependencies. A typical Rust agent project has                 the audited configuration (thinking.budget_tokens=1024
100+ transitive dependencies, any of which could forge a Budget                  at the $15/Mtok rate maps to a 15,360 uc per-call reservation lower
via mem::transmute or similar within its own unsafe blocks.                      bound). Streaming protocols introduce a complementary gap: when
The BudgetMint allowlist pattern moves the trust boundary                        a stream is canceled mid-response, the final usage event may
to a small named version-controlled file, but we do not report                   never reach the client, and the client-side usage object under-counts
a quantitative cargo-geiger audit of the dependency tree’s                       true billed tokens (Pydantic AI documents this as “canceled-stream
unsafe usage; this is identified as a follow-up. Production                      usage is partial”). The approach cannot prevent this; deployments
deployments should run cargo-geiger and an SBOM audit                            should treat canceled-stream usage as advisory and reconcile
before relying on the compile-time integrity claim, and should treat             against provider billing periodically.
the BudgetMint allowlist as the actual trust boundary rather than                         Provider-side workarounds: For reasoning models, Ope-
#[forbid(unsafe_code)] at the workspace root.                                    nAI’s reasoning_effort and Anthropic’s thinking.
    Workload diversity is limited to retry-loop patterns. The                    budget_tokens are server-side kernel-enforced caps in the
empirical evaluation exercises three retry-loop workloads (LANG-                 same operational class as max_completion_tokens, and they
001 retry-after-error, clarification, argument-hallucination). RAG               should be the first-line mechanism (operationally stronger than
pipelines, planning agents with tree-of-thoughts expansion, multi-               any client-side discipline because they cannot be bypassed). Token
modal agents, and long-context document summarization are not                    Budgets adds session-cumulative budgeting on top of the per-call
evaluated. The approach’s mechanism (pre-flight reservation under                reasoning bound via Budget::spend_with_reasoning(
a sound estimator) is workload-independent in principle, but the                 visible_estimate, provider), which pessimistically re-
empirical claim is bounded to the retry-loop family until a non-                 serves visible_estimate + provider.reasoning_reservation() before
                                                                                                                                             20

each call. We treat the two layers as complementary: the provider-              (E2) DP-composition-style tighter estimator: Adopting
side parameter bounds per-call reasoning cost, Token Budgets            Rényi differential privacy composition theorems [64]–[66] for
bounds the cumulative session cost across multiple calls. The           cumulative LLM-token consumption could in principle tighten the
spend_with_reasoning discipline is verified at the source               ∼ 2× over-reservation of the AdaptiveEstimator toward the
level (Verus); the live-API stacked-configuration validation of §4.5    ∼ 1× floor of tokenizer-direct estimation, at no per-spend latency
covers the configuration we audited.                                    cost. The mathematical scaffolding exists in the DP literature (§5)
        Audit-found gaps: Sustained user concern about reasoning-       but the LLM-cost adaptation is research work, not a parameter
token accounting appears in pydantic-ai #5445, #5379, #5304,            tweak. Worth a separate paper.
and #5302 (audit-found gaps across providers, silently dropped                  (E3) Multi-tenant distributed reservation, implemented and
thinking=False, Bedrock adaptive-thinking, Anthropic                    evaluated: The single-process affine discipline does not extend
context-compaction observability). The approach inherits these          across processes; §6.7 sketches a Saga-style reservation service
provider-side correctness gaps when relying on provider-reported        but provides no implementation or evaluation. A production-
usage; the affine-typing layer cannot compensate for under-             grade version requires distributed-systems work (replicated lease
reporting at the wire format. This is a fundamental limitation          management, partial-failure semantics, hot-key partitioning) that is
of any client-side accounting that trusts the provider’s usage report.  on the same order as a major systems paper.
                                                                                (E4) Operator interview / deployment study for capital
                                                                        efficiency: The decision trade-off (§4.5, inline per-estimator
7 F UTURE WORK                                                          summary) is presented as a parametric choice. Whether real
We list open work explicitly here, rather than embedded in production operators actually prefer the affine discipline at ∼ 2×
limitations, so that the contribution set of this paper is unambiguous. over-reservation requires interviews or deployment data we do not
                                                                        have. A user study with ∼ 10 production LLM operators would
                                                                        convert the parametric trade-off into a grounded operator-preference
7.1 Supplementary extensions shipped in the artifact                    claim and close the absence of deployment-side usability evidence.
Five extensions ship as code in the artifact but with reduced                   (E5) Programming-languages framing: The present submis-
empirical evaluation depth compared to the core contribution sion adopts the empirical-software-engineering framing: it leads
(closure-based reservation typestate, distributed lease prototype, with the catalog and failure taxonomy, treats the Rust crate as one
Python port, Mypy plugin POC, adaptive byte-length estimator). evaluated mitigation, and defers the type-theoretic specification
They address structural limitations of the single-process Rust and the mechanised cross-checks to the appendices and the artifact,
discipline and are classified as supplementary so the main paper’s where they support but do not carry the empirical claims. A
claims are not contingent on them. The full descriptions, evaluation complementary programming-languages treatment — leading with
evidence, and known limits of each are in the supplementary file the affine type system and closing the binary-level refinement
supplementary-extensions.tex in the artifact bundle.                    (Conjecture 1) so the cost bound transports to the compiled binary
                                                                        — is a distinct paper with a different centre of gravity, not a revision
                                                                        of this one. We flag it so readers can locate the boundary of what
7.2 Other open work                                                     this submission claims; it is not an open question internal to the
        Binary-level refinement (Conjecture 1): The strongest present contribution.
formal claim we explicitly do not make is that the running binary
refines the abstract specification; we leave that to future work (E1)
and do not rely on it.
                                                                        8 C ONCLUSION
        Other open obligations: (i) Multi-tenant distributed reserva- LLM agent budget overruns are a documented production failure
tion (sketched in §6.7; implementation and evaluation deferred). class across all major frameworks. Our catalog of 63 confirmed
(ii) Reasoning-model hidden tokens (§6.8): the spend_with_ incidents (Section 2), together with 47 supplementary structural
reasoning discipline is verified at the source level (Verus) entries, disaggregates into 63 confirmed production incidents, 28
but live-API evaluation of the stacked provider-side + session- maintainer-acknowledged structural gaps, 14 feature requests, and
cumulative configuration is follow-up work. (iii) External Verus 5 borderline cases, organized into eight architectural mechanism
audit (we will solicit external review before any subsequent clusters. One cluster — M-budget-primitive-missing, documented
venue). (iv) Adversarial AnthropicEstimator audit beyond across 6 frameworks and 12 catalog rows — admits the type-level
the three-workload basic validation of §4.5, exercising system- discipline most directly: a framework re-implemented in Rust
prompt-injection paths, tool-description edge cases, and multimodal against the affine Budget type cannot ship a primitive that silently
serialization oddities.                                                 regresses, exists only via callback closure, or fails to account for
                                                                        prompt-token cost. The other seven clusters benefit from runtime
                                                                        cap arithmetic conditional on estimator-soundness assumption A1,
7.3 Expensive follow-ups: research projects, not revision not from the type-system contribution.
items
                                                                            The affine discipline — a small, ASCII-stable Rust API expos-
Five items are research projects on their own. Each is named here ing Budget::new, Budget::spend, Budget::split, and
so a reader can locate the boundary of what this paper does and Budget::merge — lifts three in-program integrity properties
does not claim.                                                         to compile time within the Rust trust boundary: budgets cannot be
        (E1) A binary-level refinement proof: Closing Conjec- cloned, double-spent, or used after delegation by typed source code.
ture 1—establishing that the compiled binary preserves the source- The runtime cap arithmetic is enforced by a single checked_
level properties—is a substantial mechanization effort we do not sub. Reproducing a real LangGraph failure case (Section 4.5),
attempt here and leave to future work.                                  the same agent shape that consumes $0.0054 across 8 calls under
                                                                                                                                              21

stock LangGraph terminates after 2 calls under this approach at a        Section 4.4); rater independence and prior catalog exposure are
matched-dollar cap, with no API call made for the rejected step.         addressed in Section 4.4 threat C2. The 5,410 live-API row-event
In the head-to-head against concurrent work [25] the runtime-            corpus (of which 5,190 carry per-call reservation/actual pairs
monitored alternative reaches the same cap-respecting outcome;           underpinning the over-reservation figure in §4.5) was collected
the two are complementary integrity layers chosen by deployment          using API credits purchased from Anthropic, OpenAI, Google, and
threat model, not competing solutions.                                   Groq.
     We have positioned this work as empirical software engineering
with auxiliary specification consistency checks (in the artifact).
                                                                         A PPENDIX A
The catalog documents the failure class, the crate is one mitigation
within a specific deployment context (new Rust agent code; a             A FFINE B UDGET T YPE : F ULL T YPE -S YSTEM S PECIFICA -
minority of the 2026 production LLM-agent surface, which is              TION
presently dominated by Python frameworks), and the formal                The catalog evidence in Section 2 sets the target the design
stack cross-checks the abstract specification across multiple logics.    must meet. Across eight architectural mechanism clusters and 18
Binary-level cap-respecting on the running Tokio binary is the           ecosystems, one cluster is the cleanest fit for a type-level discipline:
open obligation Conjecture 1, deliberately unproven in this paper        M-budget-primitive-missing (§2.6) documents 12 cases across 6
and identified as a ∼12-person-month follow-up in the Iris/Rust-         frameworks where frameworks either lack a first-class declarative
Belt [12], [38] tradition that closed analogous source-to-binary         aggregate-budget primitive entirely or ship a primitive that is broken
lifts for smart-contract gas metering (KEVM, GASTAP). The                in one of seven sub-mechanism shapes (the primitive doesn’t exist;
substantive empirical contributions remaining beyond the catalog         exists but only via callback closure; exists but broken via silent
are the cross-tool specification consistency, the provider-stratified    regression; runs only on memory retrieval; works as hard cliff
estimator with pre-registered third-party validation protocol, and the   with no graceful degradation; ships with broken defaults in docs;
head-to-head measurement of cap-respecting behavior against five         doesn’t account for prompt-token cost). A type-level discipline
runtime mitigations plus concurrent work. The affine application         that threads budget capabilities through every spend point cannot
pattern itself is twenty years old (Move, seL4, governor, tokio);        make frameworks adopt it. What it can do is rule out, at compile
the contribution is its application to LLM dollar cost, positioned       time, the specific failure modes the cluster documents conditional
alongside runtime alternatives that achieve the same operational         on adoption: a framework built on the affine Budget type cannot
outcome through different machinery.                                     ship a primitive that silently regresses (the type signature pins the
                                                                         mechanism), cannot offer the primitive only via callback closure
                                                                         (the type-level threading replaces the callback), cannot fail to ac-
DATA AVAILABILITY                                                        count for prompt-token cost (the conservative byte-length estimator
A complete replication package is available across six repos-            is part of the spend interface), and so on. We are explicit about
itories: https://github.com/sajjadanwar0/token-budgets (main li-         scope: this directly addresses 12 of 110 catalog rows (≈9% of the
brary and 110-row catalog data/catalogue.csv), https:                    catalog), corresponding to the M-budget-primitive-missing cluster.
//github.com/sajjadanwar0/token-budgets-formals (TLAPS, TLC,             The other seven clusters (M-retry-loop, M-context-amplification,
Coq, Dafny, Verus mechanisations plus the IRR package irr/               M-cost-observability, M-multimodal-cost-amplification, M-storage-
containing codebook v1.0, blinded coding sheets, and the κ =             amplification, M-delegation-fanout, providerOptions-silently-
0.837 computation script), https://github.com/sajjadanwar0/token-        dropped) are not eliminated by the discipline; they are merely
budgets-experiments (empirical harnesses including the five-             bounded by the cap. A framework built on Token Budgets can still
runtime tools/multiway_compare.py and the temperature-                   suffer a 31× context overflow on a single base64-encoded image;
stratified sweep), https://github.com/sajjadanwar0/token-budgets-        the approach’s contribution is that the resulting cost cannot exceed
extensions (adaptive estimator, Verus skeleton), and https://            B0 . The approach is best characterized as a necessary primitive
github.com/sajjadanwar0/token-budgets-python (Python port of             for one cluster and a conditional upper bound (under estimator
the approach), and https://github.com/sajjadanwar0/token-budgets-        soundness A1) on the rest, not as a complete fix for the failure
baseline (the §2.2 keyword-neutral baseline cohort). The replication     class. The remaining sections specify the type and prove what it
script reproduce.sh clones all six repositories, audits the              does and does not buy.
paper-backing claims (catalog counts, estimator margins, the
IRR computation, the forgetful-operator conditions, and the A7           A.1    Type-system specification
fault-injection table), compiles the formal proofs, runs the offline
microbenchmarks, and optionally runs the live-API replication            The Budget type is a finite quota of spendable resource measured
(∼$0.50, 30 min wall-clock). Total reproduction cost for the             in integer unit-cost values (uc), where 1 uc = 10−5 USD (so a
live-API smoke test in §4.5 is under $0.005. All measurements            540 uc cap corresponds to $0.0054 of provider spend; the field
were taken on AMD Ryzen 7 PRO 6850U, Linux 6.8.0-110-                    is named micro_cents in the source). It is non-Clone, non-
generic (Ubuntu), rustc 1.93.1 stable (edition 2024), langgraph          Copy, and exposes only methods that consume self by value.
1.1.10, langchain-core 1.3.2, langchain-openai                           pub struct Budget {
1.2.1; the artifact READMEs document this matrix.                          micro_cents: u64,
                                                                         }

                                                                         impl Budget {
ACKNOWLEDGEMENTS                                                          pub fn new(micro_cents: u64) -> Self;
I thank Zahid Hussain (Mindgigs, Peshawar, Pakistan) for serving          pub fn available(&self) -> u64;
as the independent second rater for the inter-rater reliability study     pub fn spend(self, amount: u64)
(baseline N = 109 and supplementary N = 4 phase reported in               -> Result<Budget, BudgetError>;
                                                                                                                                                       22

                                                                        async fn orchestrate(budget: Budget)
 pub fn split(self, amount: u64)                                          -> Result<Budget, OrchestrationError>
 -> Result<(Budget, Budget), BudgetError>;                              {
                                                                          // Carve off $0.01 for a delegated sub-task.
 pub fn merge(self, other: Budget) -> Budget;                             let (parent, child) = budget.split(10_000)?;
 pub fn consume(self) -> u64;
}                                                                        // Move ‘child‘ into spawned task; parent keeps
                                                                             remainder.
                                                                         let handle: JoinHandle<Result<Budget,
     The signature above is designed to prevent three classes of             OrchestrationError>> =
cap-circumvention at compile time. Each property is demonstrated         tokio::spawn(async move {
by a corresponding compile-fail test in the artifact (Section 4.1        let (after, _) = call_with_budget(
                                                                         &client, child, "summarize this", 100
reports the test results; here we walk through what each property        ).await?;
guarantees). A fourth observation about budget escape via reference      Ok(after) // return any unspent budget
is inherited from Rust’s standard borrow-checker rules and is not a      });
property of our design; we discuss it after the three core properties
                                                                         // Parent runs its own work concurrently on its
to round out the threat model. We scope the approach explicitly:             share.
the affine Budget prevents in-program duplication of an existing         let (parent, _) = call_with_budget(
budget value via aliasing or stale-capability retention; it does         &client, parent, "main task", 200
                                                                         ).await?;
not bound the trusted Budget::new constructor itself, so any
code path with access to Budget::new can mint a fresh budget.            // Reclaim and merge worker’s unspent remainder.
This mirrors the standard threat model for ocap-style discipline:        let returned = handle.await
authority flows from the constructor’s caller, and the type system       .map_err(OrchestrationError::WorkerJoinFailed)??;
                                                                         Ok(parent.merge(returned))
prevents subsequent in-program forgery, not the existence of the        }
constructor. Auditing the constructor surface. The constructor
                                                                        Listing 1. Multi-agent budget delegation. The borrow checker accepts every move
is a single named function (Budget::new) and its callers are            and rejects any out-of-protocol use; errors propagate via ? for graceful handling.
statically discoverable by Rust’s module system. A deployment
can constrain the constructor surface by wrapping Budget::new
in a single trusted module that exposes only a configuration-
                                                                        E0382. We list them separately because they correspond to distinct
driven mint operation; tools such as cargo geiger (for unsafe
                                                                        application-level error modes operators care about (intra-agent
code), Clippy lints, and module-visibility audits make the trusted
                                                                        double-spend versus cross-agent capability retention), not because
set explicit. The result is a project-specific TCB whose size is
                                                                        they are independent compiler properties.
the number of files invoking Budget::new, which an operator
                                                                            Inherited borrow-check default. Budget’s fields are private,
can keep small by policy. This does not eliminate the trust
                                                                        and Rust’s lifetime rules forbid returning a reference to a local
assumption; it makes the assumption auditable, which is the
                                                                        Budget from a function (E0515: “cannot return reference to local
standard ocap framing. The arithmetic enforcement of the cap
                                                                        variable”). This is a standard borrow-checker rejection that fires
value happens at runtime inside spend (a checked_sub that
                                                                        for any local value of any type; it is not a property of the affine
returns BudgetError::Insufficient when the reservation
                                                                        Budget design but rather a default of the language. We mention it
exceeds the remaining quota); the affine type system makes that
                                                                        to round out the threat model: combined with the three properties
runtime check non-circumventable within the trust boundary. We
                                                                        above, a budget cannot leak out of the affine discipline by pointer
discuss this hybrid framing in detail in Section 3.4.
                                                                        indirection. We do not claim this as a contribution of this work.
     Property 1: no duplication. Budget does not derive Clone
                                                                            These three core properties together encode the affine reading
or Copy. A user attempting let b2 = b.clone() is rejected
                                                                        of LLM budgets: each unit of resource is owned by exactly one
with rustc error E0599: “no method named clone found.” This
                                                                        location at any moment, and operations on the resource consume
eliminates the most direct form of budget forgery—splitting a
                                                                        the owning binding. The properties bound the integrity of resource
single $1 budget into many $1 budgets via cloning.
                                                                        accounting; the cap-respecting property—that actual spend stays
     Property 2: no double-spend. spend() consumes self by
                                                                        under the configured cap—additionally requires a conservative cost
value, returning a new Budget carrying the remainder. After let
                                                                        estimator, treated in Section 3.4.
(b2, _) = b.spend(100, || ()), the original binding
b is moved and unreachable. Code that attempts a second
b.spend(...) is rejected with E0382: “use of moved value.”              A.2    Worked example
The borrow checker prevents two paths from each spending the            the worked example in the artifact shows a small multi-agent
same budget.                                                            orchestrator exercising all four Budget operations across a
     Property 3: no use-after-split. split() likewise consumes          delegation boundary. The parent agent splits off a sub-budget,
self, returning two new Budget values (remainder and child).            hands it to a delegated worker via tokio::spawn, awaits the
Code that attempts to spend on the original parent after splitting is   worker’s result, and merges the unspent remainder back into the
rejected with the same E0382 error. This property is what makes         parent.
safe sub-budget delegation possible: a parent agent cannot acci-            Three things are worth noting about this code. First, every
dentally retain spending power over a sub-budget after delegating       operation that decreases or transfers resource consumes self
it.                                                                     by value: split, spend (inside call_with_budget), and
     We acknowledge that Properties 2 and 3 are two presentations       merge all take self. The borrow checker tracks the affine
of one underlying mechanism: spend and split both take                  ownership across the tokio::spawn boundary at no runtime
self by value, so any post-consumption use is rejected with             cost. Second, the mechanism does not require Arc<Mutex<>>,
                                                                                                                                                     23

lifetime parameters, or any synchronization primitive: Budget            per-output-token rate is conservative pointwise. A8 ensures the
is a plain owned value, sent across thread boundaries the same           operator’s ρin , ρout match the rates P charges, so the per-call charge
way any other owned Rust value would be. Third, the code reads           ci and the per-call reservation ri are computed against the same
naturally to a Rust programmer; the approach does not impose             rate constants. A7 enters only on the receipt-refund path: when a
a foreign programming model. The artifact’s tests/async_                 ConfirmWithRefund transition fires, the refund amount ρi is
integration:: split_across_spawn test confirms this                      computed from the operator-supplied actual_charge; A7 ensures
exact pattern compiles and runs correctly under tokio.                   ρi ≤ ri − ci at the time of confirmation, so the post-refund ledger
                                                                         entry continues to satisfy the conservation invariant. The two
A.3   Why affine, not linear                                             pointwise bounds compose to ci ≤ ri at every i ∈ S, and summation
                                                                         gives the first inequality.
A linear type discipline would impose a stronger requirement: every
Budget value must be consumed exactly once, with the compiler
enforcing must-use [1]. We chose affine instead. Linear must-use is      R EFERENCES
the wrong fit for LLM agent budgets in two ways. First, error paths      [1]  P. Wadler. “Linear types can change the world.” In Programming Concepts
                                                                              and Methods, M. Broy and C. Jones, eds., North-Holland, 1990, pp. 561–
legitimately discard resources: a function that returns early on an           581.
unrelated failure should be allowed to drop its remaining budget         [2] B. Kitchenham and S. Charters. “Guidelines for performing systematic
without further obligation, and must-use would force boilerplate              literature reviews in software engineering.” EBSE Technical Report EBSE-
Budget::consume() calls in every error-handling site. Second,                 2007-01, Keele University and Durham University, 2007.
                                                                         [3] K. Krippendorff. Content Analysis: An Introduction to Its Methodology.
the natural usage pattern for budgets is at-most-use: an agent might          3rd edition, SAGE Publications, 2013.
spend everything in its quota, or it might spend nothing if its          [4] B. G. Glaser and A. L. Strauss. The Discovery of Grounded Theory:
task completes cheaply, but it should not be a type error to leave            Strategies for Qualitative Research. Aldine, 1967.
                                                                         [5] D. S. Cruzes and T. Dybå. “Recommended steps for thematic synthesis
budget unspent. Affine relaxes linear’s must-use to “at most one
                                                                              in software engineering.” In Proc. Int. Symp. on Empirical Software
use,” matching the Rust ownership semantics already in routine                Engineering and Measurement (ESEM), IEEE, 2011, pp. 275–284.
use for memory resources, and the typestate pattern [10], [11] as        [6] J. Saldaña. The Coding Manual for Qualitative Researchers. 3rd edition,
applied to other one-way resources like file descriptors. The explicit        SAGE Publications, 2016.
                                                                         [7] P. Runeson and M. Höst. “Guidelines for conducting and reporting case
consume() method is provided for the case where an application                study research in software engineering.” Empirical Software Engineering,
wants to inspect leftover quota; it is opt-in, not required.                  14(2):131–164, 2009.
                                                                         [8] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and
                                                                              A. Wesslén. Experimentation in Software Engineering. Springer, 2012.
A PPENDIX B                                                              [9] E. Kalliamvakou, G. Gousios, K. Blincoe, L. Singer, D. M. German,
                                                                              and D. Damian. “The promises and perils of mining GitHub.” In Proc.
S PECIFICATION CROSS - CHECKS ( SUMMARY )                                     Working Conf. on Mining Software Repositories (MSR), ACM, 2014,
The abstract Budget state machine is cross-checked for internal               pp. 92–101 (extended as “An in-depth study of the promises and perils
                                                                              of mining GitHub,” Empirical Software Engineering, 21(5):2035–2071,
consistency with TLA+ (a TLAPS proof and TLC model-checking                   2016).
of the same specification) and a preliminary, externally-unaudited       [10] R. E. Strom and S. Yemini. “Typestate: a programming language concept
Verus source-level mechanization; concurrency is exercised by a               for enhancing software reliability.” IEEE Trans. Software Engineering
randomized stress harness and bounded Loom [28] model-checking.               12(1):157–171, 1986.
                                                                         [11] J. Aldrich, J. Sunshine, D. Saini, and Z. Sparks. “Typestate-oriented
These are consistency checks on the specification—not a binary-               programming.” In Companion to OOPSLA 2009, ACM, 2009.
level proof (Conjecture 1 is open) and not evidence that composes        [12] R. Jung, J.-H. Jourdan, R. Krebbers, and D. Dreyer. “RustBelt: securing
multiplicatively across tools. The full logs, the Coq and Dafny               the foundations of the Rust programming language.” Proc. ACM on
                                                                              Programming Languages 2(POPL), 2018.
re-encodings, and a proof skeleton for the binary-level reduction
                                                                         [13] AgentGuard-style callback: a representative loop-detection and bud-
are in the artifact for readers who want them.                                get circuit-breaker baseline (a LangChain BaseCallbackHandler)
                                                                              implemented for this evaluation; see experiments/ollama_
                                                                              replication.py in the artifact. https://github.com/sajjadanwar0/
A PPENDIX C                                                                   token-budgets-experiments
P ROOF OF P ROPOSITION 1                                                 [14] ATXP: per-agent payment wallets returning HTTP 402 when depleted.
                                                                              ATXP documentation, 2026. https://docs.atxp.ai/
For completeness we give the proof of Proposition 1; the result          [15] tokio project, tokio::time::Instant and budget-pacing documen-
is integer bookkeeping under the stated assumptions rather than a             tation. https://docs.rs/tokio/
                                                                         [16] tokio project, tokio::sync::Semaphore (concurrency permits).
deep system property, which is why it sits in the appendix.                   https://docs.rs/tokio/
                                                                         [17] LangChain GitHub issue #24107: “Maximum Context Length Ex-
Proof. Combining the invariants. Invariant 1 holds because each               ceeded Due to Base64-Encoded Image in Prompt” (254,201-input-token
Budget operation is implemented over a uniquely-owned value                   single-image overflow on Phi-3-vision). https://github.com/langchain-
(Invariant 2) using checked_sub or addition; no operation                     ai/langchain/issues/24107
                                                                         [18] Mastra GitHub issue #14598: “OM issues in tool heavy environments” (2-
increases L. From Invariants 1 and 2, L(σ0 ) = B0 at session start
                                                                              million-token observer-LLM call documented). https://github.com/mastra-
and L(σ ) ≤ B0 at every subsequent state σ . Each call i ∈ S that             ai/mastra/issues/14598
successfully passes spend’s checked_sub reduces L by exactly             [19] OpenAI Agents SDK GitHub issue #844: “Max turns exceeded”
ri . Therefore ∑i∈S ri = B0 − L(σfinal ) ≤ B0 , which establishes the         (maintainer admission of architectural gap in graceful degradation).
                                                                              https://github.com/openai/openai-agents-python/issues/844
second inequality.                                                       [20] D. Yuan, Y. Luo, X. Zhuang, G. R. Rodrigues, X. Zhao, Y. Zhang, P. U.
     The first inequality ∑i∈S ci ≤ ∑i∈S ri follows from the                  Jain, and M. Stumm. “Simple testing can prevent most critical failures: an
conservative-estimator condition ci ≤ ri applied pointwise: A1                analysis of production failures in distributed data-intensive systems.” In
gives tin (p) ≤ |p|UTF-8 on the input side, and A6 gives                      USENIX OSDI 2014, pp. 249–265.
                                                                         [21] S. Lu, S. Park, E. Seo, and Y. Zhou. “Learning from mistakes: a
billed_output_tokens ≤ max_output_tokens on the output side,                  comprehensive study on real-world concurrency bug characteristics.”
so reserving the full ρout · max_output_tokens at the provider’s              In Proc. ASPLOS XIII, ACM, 2008, pp. 329–339.
                                                                                                                                                                  24

[22] S. Blackshear, E. Cheng, D. L. Dill, V. Gao, B. Maurer, T. Nowacki,            [48] N. Grech, M. Kong, A. Jurisevic, L. Brent, B. Scholz, Y. Smaragdakis.
     A. Pott, S. Qadeer, Rain, D. Russi, S. Sezer, T. Zakian, and R. Zhou.               “MadMax: Surviving out-of-gas conditions in Ethereum smart contracts.”
     “Move: a language with programmable resources.” Diem Association                    Proceedings of the ACM on Programming Languages, vol. 2, OOPSLA,
     technical report, 2020. https://developers.diem.com/docs/technical-papers/          article 116, 2018.
     move-paper/                                                                    [49] Amazon Web Services. “Cost monitoring and budget enforcement for
[23] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock, P. Derrin,              Amazon Bedrock.” AWS documentation: CloudWatch billing alarms,
     D. Elkaduwe, K. Engelhardt, R. Kolanski, M. Norrish, T. Sewell, H. Tuch,            AWS Budget actions, and automatic Bedrock service revocation on budget
     and S. Winwood. “seL4: formal verification of an OS kernel.” In Proc.               threshold breach. https://docs.aws.amazon.com/bedrock/latest/userguide/
     SOSP 2009, ACM, pp. 207–220.                                                        cost-mgmt.html
[24] A. Becker. governor: a Rust crate for rate-limiting via non-cloneable direct   [50] N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. Peyton Jones.
     token buckets. crates.io, 2018–present. https://crates.io/crates/governor           “Refinement types for Haskell.” In Proc. ICFP, 2014.
[25] Q. Ye and J. Tan. “Agent Contracts: a formal framework for resource-           [51] B. L. Kaminski, J.-P. Katoen, C. Matheja, and F. Olmedo. “Weakest
     bounded autonomous AI systems.” arXiv preprint 2601.08815, January                  precondition reasoning for expected runtimes of randomized algorithms.”
     2026 (last revised 25 March 2026, v3; accepted at COINE 2026 workshop,              Journal of the ACM, 65(5):1–68, 2018.
     AAMAS 2026, Paphos, Cyprus). https://arxiv.org/abs/2601.08815. Ref-            [52] P. Wang, D. Fu, A. K. Bouajjani, H. Yang, and J. Hoffmann. “Raising
     erence implementation: https://github.com/flyersworder/agent-contracts              expectations: Automating expected cost analysis with types.” Proc. ACM
     (PyPI: ai-agent-contracts, v0.3.1).                                                 Program. Lang., 4(ICFP):1–31, 2020.
[26] S. Clebsch, S. Drossopoulou, S. Blessing, and A. McNeil. “Deny                 [53] J.-P. Bernardy, M. Boespflug, R. R. Newton, S. Peyton Jones, and
     capabilities for safe, fast actors.” In Proc. AGERE! 2015, ACM, pp. 1–12.           A. Spiwack. “Linear Haskell: practical linearity in a higher-order
[27] BerriAI. “LiteLLM proxy — Budget management.” LiteLLM Documen-                      polymorphic language.” Proc. ACM Program. Lang., 2(POPL):1–29,
     tation v1.78, 2025. https://docs.litellm.ai/docs/proxy/users                        2018.
[28] Tokio Maintainers. “Loom: A tool for testing concurrent Rust code.”            [54] A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, and
     https://docs.rs/loom/latest/loom/, version 0.7.x, 2024.                             J. Wilkes. “Large-scale cluster management at Google with Borg.” In
[29] L. Chen, M. Zaharia, and J. Zou. “FrugalGPT: How to use large language              Proc. EuroSys, 2015.
     models while reducing cost and improving performance.” arXiv preprint          [55] Kubernetes Authors. “Resource quotas.” https://kubernetes.io/docs/
     arXiv:2305.05176, 2023.                                                             concepts/policy/resource-quotas/, accessed 2026-05.
[30] Tower Maintainers. “tower::Limit: A middleware that limits the number          [56] J. S. Turner. “New directions in communications (or which way to the
     of in-flight requests.” Rust crate documentation, https://docs.rs/tower/            information age?).” IEEE Communications Magazine, 24(10):8–15, 1986.
     latest/tower/limit/index.html, 2024.                                           [57] H. Garcia-Molina and K. Salem. “Sagas.” In Proc. SIGMOD, 1987.
[31] A. Lattuada, T. Hance, C. Cho, et al. “Verus: Verifying Rust programs          [58] C. Gray and D. Cheriton. “Leases: an efficient fault-tolerant mechanism
     using linear ghost types.” Proceedings of the ACM on Programming                    for distributed file cache consistency.” In Proc. SOSP, 1989, pp. 202–210.
     Languages (OOPSLA), 2023.                                                      [59] K. Honda, V. T. Vasconcelos, and M. Kubo. “Language primitives and
[32] pykul. “tokencap: Token budget enforcement for AI agents. Hard limits,              type discipline for structured communication-based programming.” In
     configurable policy, zero infrastructure required.” 2025. https://github.           Proc. ESOP, 1998.
     com/pykul/tokencap                                                             [60] Confio and the CosmWasm contributors. “CosmWasm gas metering.”
                                                                                         https://docs.cosmwasm.com/docs/architecture/gas/, accessed 2026-05.
[33] T. Hance, L. Elbeheiry, Y. Matsushita, and D. Dreyer. “VerusBelt: A
     Semantic Foundation for Verus’s Proof-Oriented Extensions to the Rust          [61] NEAR Protocol. “Gas: The economic model.” https://docs.near.org/
     Type System.” PLDI 2026.                                                            concepts/protocol/gas, accessed 2026-05.
                                                                                    [62] Solana Labs. “Runtime compute units.” https://docs.solana.com/
[34] J. Hoffmann, K. Aehlig, and M. Hofmann. “Multivariate amortized
                                                                                         developing/programming-model/runtime#compute-budget, accessed 2026-
     resource analysis.” ACM TOPLAS, 34(3), 2012. [Cited as exemplar of
                                                                                         05.
     static resource analysis tradition.]
                                                                                    [63] Google Cloud. “Create, edit, or delete budgets and budget alerts.” https:
[35] E. Hildenbrandt et al. “KEVM: A Complete Formal Semantics of the
                                                                                         //cloud.google.com/billing/docs/how-to/budgets, accessed 2026-05.
     Ethereum Virtual Machine.” CSF 2018, pp. 204–217.
                                                                                    [64] C. Dwork and A. Roth. “The algorithmic foundations of differential
[36] G. Wood. “Ethereum: A secure decentralised generalized transaction
                                                                                         privacy.” Foundations and Trends in Theoretical Computer Science, 9(3–
     ledger.” Ethereum Yellow Paper, Byzantium revision, 2018.
                                                                                         4):211–407, 2014.
[37] P. Wang, H. Fu, K. Chatterjee, Y. Deng, and M. Xu. “Proving expected           [65] I. Mironov. “Rényi differential privacy.” In IEEE Computer Security
     sensitivity of probabilistic programs with randomized variable-dependent            Foundations Symposium (CSF), 2017, pp. 263–275.
     termination time.” Proc. ACM Program. Lang., 4(POPL), Article 25,              [66] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar,
     2020.                                                                               and L. Zhang. “Deep learning with differential privacy.” In ACM CCS,
[38] R. Jung, R. Krebbers, J.-H. Jourdan, A. Bizjak, L. Birkedal, and D. Dreyer.         2016, pp. 308–318.
     “Iris from the ground up: A modular foundation for higher-order concurrent     [67] D. Orchard, V.-B. Liepelt, and H. Eades III. “Quantitative program
     separation logic.” Journal of Functional Programming, vol. 28, e20, 2018.           reasoning with graded modal types.” Proc. ACM Program. Lang., 3(ICFP),
[39] Y. Matsushita, T. Tsukada, and N. Kobayashi. “RustHorn: CHC-based                   Article 110, 2019.
     verification for Rust programs.” ESOP 2020: Programming Languages              [68] M. Gaboardi, S.-y. Katsumata, D. Orchard, F. Breuvart, and T. Uustalu.
     and Systems, LNCS 12075, pp. 484–514, Springer, 2020.                               “Combining effects and coeffects via grading.” In Proc. ICFP, 2016,
[40] L. Gaeher et al. “RefinedRust: A type system for high-assurance                     pp. 476–489.
     verification of Rust programs.” Proc. ACM on Programming Languages,            [69] Envoy Proxy. “Rate limit service and global rate limiting architec-
     vol. 8, no. PLDI, Article 192, June 2024.                                           ture.” https://www.envoyproxy.io/docs/envoy/latest/configuration/other_
[41] R. Atkey. “Syntax and semantics of quantitative type theory.” LICS 2018:            features/rate_limit, accessed 2026-05.
     Logic in Computer Science, ACM/IEEE, 2018, pp. 56–65.                          [70] Istio. “Enforcing policies and quotas via the Envoy data plane.” https:
[42] A. C. Bomberger, A. P. Frantz, W. S. Frantz, A. C. Hardy, N. Hardy,                 //istio.io/latest/docs/tasks/policy-enforcement/, accessed 2026-05.
     C. R. Landau, J. S. Shapiro. “The KeyKOS nanokernel architecture.”             [71] Kong. “Rate-limiting and response-ratelimiting plugins.” https://docs.
     USENIX Workshop on Micro-Kernels and Other Kernel Architectures,                    konghq.com/hub/kong-inc/rate-limiting/, accessed 2026-05.
     1992.                                                                          [72] P. Tarjan. “Scaling your API with rate limiters.” Stripe Engineering Blog,
[43] J. S. Shapiro, J. M. Smith, D. J. Farber. “EROS: A fast capability system.”         2017. https://stripe.com/blog/rate-limiters.
     SOSP 1999: Operating Systems Principles, ACM, 1999, pp. 170–185.               [73] A. Ghodsi, M. Zaharia, B. Hindman, A. Konwinski, S. Shenker, and
[44] R. N. M. Watson et al. “CHERI: A hybrid capability-system architecture              I. Stoica. “Dominant resource fairness: Fair allocation of multiple resource
     for scalable software compartmentalization.” IEEE Symposium on Security             types.” In NSDI, 2011.
     and Privacy, 2015, pp. 20–37.                                                  [74] A. Gulati, A. Merchant, and P. J. Varman. “mClock: Handling throughput
[45] A. Mettler, D. Wagner, T. Close. “Joe-E: A security-oriented subset of              variability for hypervisor IO scheduling.” In USENIX OSDI, 2010.
     Java.” NDSS 2010.                                                              [75] O. Khattab, A. Singhvi, P. Maheshwari, Z. Zhang, K. Santhanam,
[46] M. S. Miller. “Robust composition: Towards a unified approach to access             S. Vardhamanan, S. Haq, A. Sharma, T. T. Joshi, H. Moazam, H. Miller,
     control and concurrency control.” PhD thesis, Johns Hopkins University,             M. Zaharia, and C. Potts. “DSPy: Compiling declarative language model
     2006.                                                                               calls into state-of-the-art pipelines.” In Proc. ICLR, 2024.
[47] E. Albert, P. Gordillo, A. Rubio, I. Sergey. “GASTAP: A gas analyzer for       [76] R. N. M. Watson, J. Anderson, B. Laurie, and K. Kennaway. “Capsicum:
     smart contracts.” IEEE Access, vol. 10, pp. 50472–50495, 2022.                      practical capabilities for UNIX.” In USENIX Security Symposium, 2010.
                                                                                                                                                     25

[77] J. Sunshine, K. Naden, S. Stork, J. Aldrich, and É. Tanter. “First-class      D.0.2   Results
     state change in Plaid.” In OOPSLA, 2011.
[78] M. Coblenz, R. Oei, T. Etzel, P. Koronkevich, M. Baker, Y. Bloem, B. A.
                                                                                   Table 8 reports mean spend (uc) and percentage of the configured
     Myers, J. Aldrich, and J. Sunshine. “Obsidian: typestate and assets for       cap, averaged across each N = 10 cohort. Column “Mock” omits
     safer blockchain programming.” ACM TOPLAS, 42(3), 2020.                       CrewAI and AutoGen, which require a real provider; their wrappers
[79] R. DeLine and M. Fähndrich. “Enforcing high-level protocols in low-level      record an explicit skip outcome rather than running against a stub
     software.” In PLDI, 2001.
[80] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao. “Reflexion:
                                                                                   LLM.
     language agents with verbal reinforcement learning.” In NeurIPS, 2023.
[81] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao.         D.0.3   Mechanism interpretation
     “ReAct: synergising reasoning and acting in language models.” In ICLR,
                                                                                   The empty Python-sim Anthropic and Groq cells in Table 8
     2023.
[82] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang,       show two distinct failure modes. The Python sim’s coarse fixed-
     X. Chen, Y. Lin, W. X. Zhao, Z. Wei, and J.-R. Wen. “A survey on              form estimator under-reserves on tool-augmented prompts and
     large language model based autonomous agents.” Frontiers of Computer          exceeds the cap on Anthropic ($0.00900 vs. $0.00540, 168%) and
     Science, 18(6), 2024.
[83] Z. Xi, W. Chen, X. Guo, W. He, Y. Ding, B. Hong, M. Zhang, J. Wang,
                                                                                   Groq ($0.00829 vs. $0.00540, 153%); the Rust impl’s byte-length
     S. Jin, E. Zhou, et al. “The rise and potential of large language model       estimator over the full UTF-8-serialized request body refuses every
     based agents: a survey.” Science China Information Sciences, 2025.            cap-violating call before the network and shows zero overshoot.
[84] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and           Three runtime classes vs. compile-time: Structural run-
     P. Liang. “Lost in the middle: how language models use long contexts.”
     TACL, 12:157–173, 2024.                                                       time (LangGraph/CrewAI/AutoGen) bounds call count, not dollars;
[85] K. Opsahl-Ong, M. J. Ryan, J. Purtell, D. Broman, C. Potts, M. Zaharia,       it cannot enforce a dollar cap without a separate cost layer.
     and O. Khattab. “Optimizing instructions and demonstrations for multi-        Runtime-cost (AgentGuard-style) tracks dollars but checks after
     stage language model programs.” In EMNLP, 2024.                               the call; the approach still admits a single overshooting call.
[86] Langfuse contributors. “Langfuse: open-source LLM engineering platform
     with cost tracking and budget alerts.” https://langfuse.com, accessed 2026.   Compile-time (Token Budgets) lifts the check before the call:
[87] Braintrust contributors. “Braintrust: LLM evaluation platform with per-test   the type system rejects programs that ignore the budget, and the
     budget limits.” https://www.braintrust.dev, accessed 2026.                    runtime check refuses cap-violating calls without spending. The
                                                                                   Python-sim TB row is included for harness-homogeneity (the same
                                                                                   Python comparator runs all runtimes); its cap violations are direct
A PPENDIX D                                                                        evidence that the estimator’s coarseness matters and that the Rust
M ULTI - RUNTIME HEAD - TO - HEAD : FULL PROTOCOL AND                              impl’s byte-length bound is the right empirical implementation.
RESULTS
                                                                                   D.0.4   An additional failure mode of structural mitigations
This appendix gives the full setup, results table, mechanism                       The CrewAI-on-Groq cell in Table 8 is empty because 0/10
analysis, and reproducibility notes for the head-to-head summarised                runs completed. Llama-3.3-70B has a known tool-call reliability
in §4.2.                                                                           issue: it occasionally emits structurally invalid JSON inside its
        Scope of the structural-counter comparison: LangGraph’s                    function-call envelope (e.g., {"query": "..." )}, with an
recursion_limit, CrewAI’s max_iter, and AutoGen’s                                  unmatched closing brace), which langchain-groq surfaces as
max_consecutive_auto_reply are structural step counters,                           a 400 BadRequest. CrewAI’s internal retry loop exhausts before
not dollar-cap mechanisms. We include them in Tables 8 and the                     max_iter can trigger. This reveals a failure mode that does not
gpt-4o head-to-head (artifact) because the catalog shows operators                 appear in the discussion of structural mitigations in the literature:
do mis-deploy them as cost proxies in production (§2.5, cluster                    the structural counter only fires if the agent reaches it. When the
M-budget-primitive-missing; LANG-001, CRAI-002, AGPT-008),                         underlying LLM is unreliable at the tool-call format level, the agent
so their behavior under a dollar-cap metric documents the size of                  errors out into the framework’s exception path before the counter
that gap. They are reported as operational-gap evidence; the actual                ever decrements, and the operator gets no budget guarantee at all.
mechanism comparators are the AgentGuard-style cost callback                       Token Budgets’ reservation discipline is unaffected: it operates
and LiteLLM proxy budgets, plus tokencap (§4.5) and Agent                          at the LLM API call boundary, before any tool-call serialization,
Contracts (§5.1).                                                                  and deducts on every attempt regardless of whether the model’s
                                                                                   response parses.
D.0.1   Setup
                                                                                   D.0.5   Threats to validity and reproducibility
The         harness         (tools/multiway_compare.py,
                                                              We report both a Python-sim and a Rust-impl TB row in Table 8: the
supplementary) instantiates each runtime against a
                                                              Python sim’s coarse estimator under-reserves on tool-augmented
deterministic mock chat model (reproducing Section 4.5’s
                                                              prompts (168%/153% on Anthropic/Groq) and is shown only for
MockSQLChatModel) and against three live providers: OpenAI
                                                              harness-homogeneity; the cap-respecting claim rests on the Rust-
gpt-4o-mini, Anthropic claude-haiku-4-5, and Groq
                                                              impl row. A Groq confound is that Llama-3.3-70B’s tool-call
llama-3.3-70b-versatile. The cap is fixed at B0 = 540 uc
                                                              reliability is materially worse at this prompt scale (1/10 LangGraph,
(≈ $0.0054); per-step token-count growth is fixed at g = 60.
                                                              10/10 CrewAI errors), a model-level property a more reliable Groq
Structural-counter parameters are set to each framework’s
                                                              model would remove. The table covers LANG-001 across three
commonly-cited default for budget-mitigation discussion:
                                                              providers and five runtimes; two further workloads and an N=30
recursion_limit= 20 (LangGraph), max_iter= 5
                                                              gpt-4o grid are in §4.5 and §4.5. Harnesses, per-cell CSVs, and the
(CrewAI), max_turns= 4 (AutoGen). Each (runtime, provider)
                                                              driver script ship in the artifact (total live-sweep cost ∼ $0.18).
pair runs N = 10 independent invocations. The mock provider
is deterministic; live providers are run at temperature= 0 to
suppress sampling variance.
                                                                                                                                                                                       26




                                                                             TABLE 8
Cross-runtime, cross-provider mean spend (with bootstrap 95% CI in brackets, 104 resamples) on the LANG-001 reproduction at B0 = 540 uc, g = 60, N = 10. Each
cell shows mean spend in micro-cents (CI), percentage of the configured cap, and outcome code. Outcome codes: S = structural counter tripped; C = task completed
without protection firing; R = AgentGuard runtime guard fired post-hoc; T = Token Budgets reservation refused. Most cells exhibit <5 uc CI width (live providers at
temperature= 0 are nearly deterministic at this prompt scale); the CrewAI-Anthropic cell is the principal exception. Per-footnote evidence (a–g) follows the table.


Runtime                                  Mock                                 OpenAI                               Anthropic                           Groq
                                         gpt-4o-mini stub                     gpt-4o-mini                          claude-haiku-4-5                    llama-3.3-70b

Unprotected (no cap)f                    —                                    47 / 9% / N                          358 / 66% / N                       —g
LangGraph        (recursion_             735 / 136% / S                       637 [634,639] / 118% / S             4758 [4754,4765] / 881% /           3275 [3269,3281] / 606% /
limit=20)                                                                                                          C                                   Sa
LangGraph + AgentGuard cb                621 / 115% / R                       625 [606,634] / 116% / R             906 / 168% / R                      609 / 113% / R
CrewAI (max_iter=5)                      —                                    433 [430,437] / 80% / C              7532 [7070,8015] / 1395% /          —b
                                                                                                                   C
AutoGen (max_turns=4)                    —                                    173 / 32% / S                        4904 [4898,4909] / 908% /           931 / 172% / S
                                                                                                                   S
TB (Python sim)h                         516 / 96% / T                        379 / 70% / T                        906 / 168% / Tc                     826 [825,827] / 153% / Tc
TB (Rust impl)d                          —                                    67 / 12% / T                         0 / 0% / T                          181 / 34% / T
LiteLLM proxye                           —                                    568 [563,575] / 105% / Rp            906 / 168% / Rp                     609 / 113% / Rp
All spend values in micro-cents (uc). a 9/10 runs; one run errored on a Llama tool_use_failed (malformed JSON in the model’s tool call). b 0/10 runs; CrewAI’s internal retry
loop exhausted on Llama tool-call format errors before max_iter could trigger. c The Python TB simulator’s fixed-form estimator under-reserves on tool-augmented prompts (A1
violation); the Rust implementation’s prompt.len() estimator over the full message body refuses the offending call before any network spend, as the adjacent Rust-impl row
demonstrates. d Rust impl row produced by the Rust binary the Rust live-API harness (supplementary), which links the actual Budget from the budget-spike crate against the
live provider APIs using the byte-length estimator over the UTF-8-serialized request body (system + user + tool descriptions + history). N = 10 per cell. Across all 30 runs in the
three live cells above (and across the full 9-cell, 90-run multi-workload sweep reported in Section 4.5 et seq.), maximum overshoot is 0 uc; the approach is never violated. Cells
without bracketed CI are deterministic at the precision shown. e LiteLLM proxy budgets: deployed gateway proxy with virtual-key budget enforcement (max_budget = $0.0054,
LiteLLM 1.78.6+); Rp outcome code denotes post-call observation, where the proxy observes cost only after each call returns and rejects the next attempt. Mean overshoot equals the
threshold-crossing call’s cost, consistent with post-call cost-control’s structural inability to refuse a call before issuing it. f Unprotected baseline: recursion_limit=∞, no cap, no
AgentGuard, no LiteLLM. Outcome code N denotes natural termination (the model self-terminated before any structural counter or cap fired). Numbers from the cross-provider sweep
(§4.5, N = 10 per provider, recursion_limit=16 permitting up to 8 agent steps): gpt-4o-mini self-terminates at the recursion limit (8 steps, 47 uc), claude-haiku-4-5
self-terminates after 3 steps (358 uc) without hitting the limit. The approach provides no observable savings on these workloads because the model self-terminates below cap; the
approach’s value is worst-case-conditional (§4.5). g Groq unprotected baseline not included in the §4.5 sweep; a follow-up sweep at recursion_limit=32 and no cap is required to
characterize llama-3.3-70b’s natural-termination behavior on this workload. Existing data from Table 8 row 1 (LangGraph recursion_limit=20 at 3275 uc) is the closest
existing approximation but bounds the observation by the structural counter rather than by natural termination. h Python sim is a behavioral simulation of the approach in Python (not the
production Rust crate); it is included for harness-homogeneity (the same Python comparator runs all runtimes) and to demonstrate what happens without compile-time integrity. The
approach as shipped is the Rust impl row directly above; the Python port (§7.1, the “Python port carries no compile-time guarantees” item) is the runtime-only deployment artifact and is
functionally equivalent to existing runtime mitigations (AgentGuard, LiteLLM proxy) — it explicitly loses the compile-time property.
