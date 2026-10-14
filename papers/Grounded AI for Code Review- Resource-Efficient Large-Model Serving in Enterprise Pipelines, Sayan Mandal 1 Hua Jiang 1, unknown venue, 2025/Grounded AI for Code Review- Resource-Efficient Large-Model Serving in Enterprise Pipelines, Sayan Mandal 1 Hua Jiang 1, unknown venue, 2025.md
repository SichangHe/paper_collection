                                         G ROUNDED AI FOR C ODE R EVIEW: R ESOURCE -E FFICIENT L ARGE -M ODEL
                                                         S ERVING IN E NTERPRISE P IPELINES


                                                                                          Sayan Mandal 1 Hua Jiang 1


                                                                                                   A BSTRACT
                                                 Automated code review adoption lags in compliance-heavy settings, where static analyzers produce high-volume,
                                                 low-rationale outputs, and naive LLM use risks hallucination and incurring cost overhead. We present a production
arXiv:2510.10290v1 [cs.SE] 11 Oct 2025




                                                 system for grounded, PR-native review that pairs static-analysis findings with AST-guided context extraction and
                                                 a single-GPU, on-demand serving stack (quantized open-weight model, multi-tier caching) to deliver concise
                                                 explanations and remediation guidance. Evaluated on safety-oriented C/C++ standards, the approach achieves sub-
                                                 minute median first-feedback (offline p50 build+LLM 59.8s) while maintaining competitive violation reduction
                                                 and lower violation rates versus larger proprietary models. The architecture is decoupled: teams can adopt the
                                                 grounding/prompting layer or the serving layer independently. A small internal survey (n=8) provides directional
                                                 signals of reduced triage effort and moderate perceived grounding, with participants reporting fewer human review
                                                 iterations. We outline operational lessons and limitations, emphasizing reproducibility, auditability, and pathways
                                                 to broader standards and assisted patching.

                                         1       I NTRODUCTION                                              code review that couples the determinism of industry-grade
                                                                                                            static analysis with the explanatory power of LLMs, all sup-
                                         Modern software organizations increasingly rely on pull            ported by a resource-efficient model serving architecture.
                                         request (PR) centric workflows to maintain development             The system is designed to deliver actionable, PR-native
                                         velocity while protecting code quality. Yet code reviews,          feedback at a medium enterprise scale, covering dozens of
                                         which are a core requirement in software development, re-          repositories and hundreds of weekly pull requests. Our cen-
                                         main a human-intensive and error-prone process that con-           tral design principle is grounding: every LLM-generated
                                         sumes a significant portion of engineering time (Bosu et al.,      explanation is explicitly anchored to concrete, verifiable
                                         2015; Thomson, 2021). Traditional static analyzers inte-           evidence. This includes compiler-verified builds, specific
                                         grated into PRs, such as Google’s Tricorder or integrations        static-analysis findings, formal rule definitions, and pre-
                                         available through tools like CodeQL (Youn et al., 2023) and        cise file/line locations. This approach forces the model to
                                         Semgrep (Bennett et al., 2024), are crucial for enforcement.       reason about the code in the context of a tangible compli-
                                         However, they often surface large volumes of findings with         ance or quality requirement, rather than reasoning about the
                                         limited explanatory rationale, creating code triage burdens        code in general. To keep prompts compact yet semantically
                                         and inadvertently contributing to developer warning fatigue        rich, the system performs abstract syntax tree (AST) and
                                         (Sadowski et al., 2015; Youn et al., 2023; Agrawal et al.,         call-graph guided context extraction, selecting only the func-
                                         2023). Conversely, while large language models (LLMs)              tions, types, and lines necessary to understand a finding. We
                                         excel at explaining code, identifying bugs, and suggesting         implement it as a "grounding first, then generate" pattern,
                                         remedies, their naive application in continuous integration        which has shown success in recent repository-context and
                                         and continuous delivery (CI/CD) pipelines remains a chal-          graph-guided approaches. This approach effectively con-
                                         lenge. Without a verifiable chain of evidence, they are            strains the model’s reasoning space to reduce hallucinations
                                         susceptible to misidentification, hallucinations, inconsistent     and enhance the relevance of its fix suggestions (Xie et al.,
                                         reasoning, and prohibitive operational costs, which fail to de-    2025).
                                         liver the concise, trustworthy, and timely feedback required
                                         for enterprise adoption (Zhang et al., 2025).                      We evaluate our approach on internal codebases represen-
                                                                                                            tative of medium-scale enterprise development using an
                                         This paper presents a production system for grounded AI            offline, reproducible benchmark at the hunk level. Our
                                             1
                                             AMD, San Jose, CA, USA. Correspondence to: Sayan Mandal        contributions are fourfold: (i) Hybrid Grounding Method-
                                         <sayan.mandal@amd.com>, Hua Jiang <hua.jiang@amd.com>.             ology pairs static-analysis evidence with LLM explanations
                                                                                                            to produce citation-rich PR comments; (ii) Single-GPU
                                                Grounded AI for Code Review

Resource-Efficient Serving delivers a p50 first-feedback         than speculate about the code in general.
proxy of 59.8s (Table 1) on a quantized open-weight model;
                                                                 This hybrid model pairs analyzer recall and localization with
(iii) Enterprise Integration Blueprint captures build or-
                                                                 LLM contextual explanation. For each finding, we extract a
chestration, deviation policy handling, audit provenance,
                                                                 minimal code segment along with the rule rationale, form-
and reproducible prompts; and (iv) Competitive On-Prem
                                                                 ing a compact prompt that preserves necessary semantics
Effectiveness shows a 6-bit Qwen2.5 coder profile matching
                                                                 while minimizing tokens. The result is fewer, higher-quality
larger APIs while lowering rule violation introductions (Fig-
                                                                 comments that explain why an issue matters and how to
ure 2, Table 1) and preserving on-prem control. Section 3
                                                                 remediate it.
expands on the architecture and serving pipeline.
The remainder of this paper details the system architecture      2.3   Resource-Efficient LLM Serving for CI/CD
and methods, presents quantitative and qualitative results,            Workloads
situates the work within the context of related research and
tools (Rasheed et al., 2024), and outlines limitations and       Delivering grounded feedback within the demanding SLOs
future directions, including automated patching, broader         of a CI/CD pipeline requires a purpose-built serving archi-
standards support, and IDE-time assistance.                      tecture. Enterprise environments often rely on a limited
                                                                 pool of shared GPUs, necessitating a focus on resource ef-
                                                                 ficiency. To be practical, a serving stack must handle the
2     BACKGROUND                                                 bursty, diurnal traffic patterns of development activity, ensur-
2.1   Large Language Models for Developer Assistance             ing a predictable and low "time-to-first-comment" (e.g., near
                                                                 sub-minute) (Walkowiak & Walkowiak, 2024; Lou et al.,
LLMs have emerged as a powerful tool for developer assis-        2025).
tance, capable of explaining complex code, summarizing
changes, and proposing concrete fixes. A new generation of       Key techniques include quantization (reducing footprint for
PR-native tools, including GitHub Copilot for Pull Requests      single-GPU fit), KV/prefix and response caching to avoid
and CodeRabbit, leverages this capability to provide auto-       repeat work, and an on-demand lifecycle that unloads during
mated, natural-language feedback directly within the review      idle periods. The implementation on AMD Instinct + ROCm
process (Göçmen et al., 2025; Cihan et al., 2025). These         is hardware-agnostic, avoiding vendor lock-in.
tools demonstrate the potential of AI to reduce the cognitive
load on human reviewers, especially for issues related to        Requirements for an Enterprise-Grade System Based
style, clarity, and simple defects.                              on this review of the state-of-the-art (SOTA) and its limita-
                                                                 tions, we derive four core design requirements for a prac-
However, the unconstrained application of LLMs in the            tical, PR-native AI code review system: R1 — Grounded
high-stakes environment of code review presents significant      Accuracy anchors comments in verifiable evidence (AST
risks. Without guardrails, these models are prone to hal-        spans, rule citations, tool findings) with precise line refer-
lucinations, where they confidently invent incorrect facts       ences; R2 — CI-Grade Latency and Throughput targets
or identify non-existent issues (Zhang et al., 2025). They       sub-minute (P95) feedback for typical PRs, excluding ana-
might provide broad, out-of-context suggestions that don’t       lyzer build time, even under bursty CI/CD loads; R3 — Cost
apply, weakening trust with developers. Furthermore, the         Efficiency keeps the stack on a single shared enterprise GPU
operational realities of enterprise CI/CD, including strict      via aggressive caching and on-demand allocation; and R4
latency service level agreements (SLAs) and service level        — Enterprise Operability delivers PR-native integration,
objectives (SLOs), spiky traffic patterns, and constrained       deviation policy support, and the observability, security, and
budgets, make the naive deployment of large models com-          audit trails required in enterprise environments (Liargkovas
putationally infeasible.                                         et al., 2023).

2.2   Grounding: A Hybrid Approach to Trustworthy                We evaluate safety-oriented C/C++ standards (e.g., MISRA
      AI Review                                                  C/C++) as a case study, but the architecture is standard-
                                                                 agnostic and applies broadly to organizational reviews re-
The most effective path to mitigating these risks is ground-     quiring robust, low-resource serving, and verifiable outputs
ing: constraining an LLM’s reasoning to a foundation of          (Vero et al., 2025).
verifiable evidence. In the context of code review, this means
every AI-generated comment must be explicitly anchored
to deterministic signals, such as compiler-verified builds,
                                                                 3     M ETHODOLOGY
static-analysis findings, formal rule definitions, and precise   This section details the architecture and operational flow
file/line locations. This "grounding-first" approach forces      of our grounded AI code review system. We first provide
the model to reason about a specific, verifiable issue rather    a high-level overview, followed by a detailed examination
                                                 Grounded AI for Code Review

of the core components responsible for orchestration, con-              executing repository-specific build and static analysis
text extraction, prompt engineering, and resource-efficient             commands, parsing the resulting reports, performing
model serving.                                                          context extraction, synthesizing prompts for the LLM,
                                                                        and posting structured, threaded comments back to the
Enterprise deployment imposes hard constraints that typi-
                                                                        GitHub PR.
cal LLM demonstrations ignore: strict end-to-end latency
targets, volatile and spiky traffic patterns aligned with busi-     2. LLM Serving Backend: A containerized, on-premise
ness hours, limited and shared graphical processing unit               service built with FastAPI and Ray Serve provides
(GPU) resources, and stringent data-residency and security             the generative capabilities. It is designed for high-
requirements. We address these constraints with a serv-                throughput, low-latency inference under the bursty traf-
ing stack purpose-built for the CI/CD environment. The                 fic patterns of CI/CD. The backend hosts a quantized
architecture features a decoupled message queue to buffer              LLM, managed by llama.cpp and Ray Serve for on-
and route incoming requests, enabling graceful handling of             demand loading and unloading. To maximize resource
traffic bursts. This queue feeds a multi-tier caching system           efficiency, it employs a multi-tier caching architec-
and a dynamic router that forwards only novel, uncomputed              ture (in-memory KV/prefix, Redis, and PostgreSQL)
requests to a single GPU inference service. The service runs           and a RabbitMQ message queue for intelligent request
a quantized large model (e.g., 4–8 bits using llama.cpp) with          routing and load leveling. An Nginx reverse proxy
on-demand loading to fit on a single enterprise GPU and                manages TLS termination and secure ingress.
reclaim compute hours when pipelines are quiet. By leverag-
ing both prompt-level KV/prefix and response-level caching,       3.1.1    End-to-End Workflow
the system minimizes re-computation. It ensures that the
GPU is reserved for generating new insights, dramatically         The system operates as a stateful pipeline triggered by PR
improving throughput and end-to-end latency.                      events. The end-to-end flow proceeds as follows: (1) A de-
                                                                  veloper opens or updates a PR, triggering a GitHub webhook
We instantiate this architecture in a GitHub-integrated           received by the orchestrator. (2) The orchestrator checks
bot ("Auto CodeReview") that (1) orchestrates repository-         out the specified commit and, using a repository-specific
specific builds and static analysis checks, (2) extracts min-     configuration, executes the necessary build commands. (3)
imal, high-signal context around each finding, (3) synthe-        The configured static analyzer is invoked on the built code,
sizes structured prompts that include rule rationales and         generating a structured report of potential violations. (4)
protective guardrails, and (4) posts structured PR comments       The orchestrator parses this report, filtering for findings
that explain why an issue matters and how to fix it, complete     relevant to the PR’s diff. (5) For each relevant finding, an
with links back to the source code and policy documents.          AST-guided context extractor selects a minimal, high-signal
The system emits both violation reports for auditability and      code snippet and enriches it with rule information. (6) A
PR-native comments for seamless workflow integration. It          structured, grounded prompt is assembled and sent to the
is designed to operate alongside existing PR assistants (e.g.,    LLM serving backend. (7) The backend first checks its
Copilot for Pull Requests, CodeRabbit) while specializing         multi-tier cache; on a cache miss, the request is routed to the
in high-trust, rule-aware feedback. While our primary case        LLM for generation. (8) The generated explanation, includ-
study targets a safety-oriented C/C++ rule set (specifically      ing rationale, risk, and remediation advice, is returned to the
motor industry software reliability association (MISRA)           orchestrator, which formats and posts it as a threaded PR
(Hatton, 2004)), the architecture is standard-agnostic and        review comment. (9) On subsequent commits, the system
can be readily applied to organization-specific policies and      cleans up stale comments and archives the interaction.
security patterns across any language.
                                                                  3.2     Orchestrator: Builds, Analysis, and Policy
3.1   System Overview
                                                                  Config-driven Builds: To support a heterogeneous multi-
The system is architected as two cooperating microservices        repository environment, each project defines its build and
designed for modularity and scalability within an enterprise      analysis configuration in a repository-local JSON file. This
CI/CD environment, shown in Figure 1.                             file specifies the toolchain (e.g., GCC, specific cross-
                                                                  compilers), build flags, and the static analysis standard to
                                                                  apply (e.g., MISRA C:2012). The orchestrator uses this
  1. Code-Review Orchestrator: A GitHub App, imple-
                                                                  configuration to create a clean, reproducible build environ-
     mented in Node.js and managed by the PM2 process
                                                                  ment and invoke the static analyzer with the correct rule
     manager, serves as the primary control plane. It listens
                                                                  packs enabled. Where supported, the system defaults to a
     for PR webhooks, manages the state of review jobs,
                                                                  diff-scoped or incremental analysis to minimize latency.
     and orchestrates the entire workflow. Its responsibili-
     ties include checking out the relevant repository state,     Rule Registry and Enrichment: Our implementation lever-
                                                 Grounded AI for Code Review




Figure 1. Complete end-to-end framework of AutoCodeReview: The system consists of Code-Review Orchestrator, which extracts,
analyzes, and generates code review prompts (Static Analyzer + Prompt Generator), and LLM Serving Backend, which provides access to
LLM Service.


ages the Coverity static analyzer. The orchestrator invokes        uses the diff to locate the change, parses the AST to un-
cov-build and cov-analyze to generate an intermediate data         derstand structure, and gathers the enclosing function body
format. From this, a machine-readable JSON report is pro-          (with non-essential comments collapsed), the direct caller
duced. This report is parsed to extract detailed information       and callee names that drive the relevant flow, and if space
for each finding, including the rule ID (e.g., MISRA Rule          remains tight a sliding window of ±k lines around the vio-
10.1), violation description, severity, and Coverity’s sug-        lation. The final extracted snippet is annotated, giving the
gested remediation. The orchestrator then filters these find-      LLM a complete and verifiable view of the code in question.
ings, retaining only those whose file and line locations fall      A high-level description of the review pipeline is shown in
within the PR’s changed code patch. This ensures that every        algorithm 1.
comment is directly relevant to the author’s modifications.
                                                                   3.2.2   Prompting and Guardrails
Deviation Management: To handle necessary exceptions
to static analysis rules, the system supports a formal de-         All prompts adhere to a structured schema designed to en-
viation process. While Coverity has internal mechanisms            force grounding and elicit high-quality, actionable responses.
for managing deviations, our system uses a supplementary           Key components include Role & scope, which instructs the
JSON-based policy file maintained within each repository.          LLM to behave as a senior compliance reviewer focused
This file records approved exceptions, specifying the scope        on supplied context; Rule Rationale, a concise rule ex-
(file, function, and rule), a rationale for the deviation, and     planation pulled from analyzer documentation; Finding
the owner. When the orchestrator processes an analysis             Metadata, covering rule ID, file path, line numbers, and the
report, it cross-references findings against this policy file.     raw analyzer message; the annotated Code Snippet itself;
Matching findings are suppressed from the PR comments              an Output Contract that demands rationale, risk framing,
but are preserved in the full audit logs to maintain compli-       and remediation options with explicit line citations; and
ance traceability.                                                 explicit Guardrails that forbid speculation beyond the pro-
                                                                   vided snippet. Responses are programmatically checked
3.2.1   Token-Budgeted Context Extraction                          against this schema, then grouped by rule and posted as
                                                                   threaded PR review comments for readability.
To create prompts that are both compact and semantically
rich, the system employs a multi-faceted context extraction
strategy that operates within a fixed token budget. For each
finding identified in the static analysis report, the extractor
                                           Grounded AI for Code Review

                                                          3.3   LLM Serving: Efficient Operation in CI/CD
                                                          Serving Stack: The LLM serving backend is a Dockerized
                                                          on-premise deployment running on an AMD MI210 GPU
                                                          with the ROCm stack (Zhang et al., 2024). It consists of four
                                                          integrated services: (1) an Nginx reverse proxy for TLS ter-
                                                          mination and ingress control; (2) PostgreSQL for persistent,
 Algorithm 1: High-Level Algorithm for a Scal-
                                                          long-term response caching and analytics; (3) RabbitMQ
 able, Asynchronous Auto Code Review System.
                                                          for message broking, which decouples the API from the
1  Procedure AutoCodeReviewW                              inference workers and buffers requests during traffic spikes;
 2    P ← ExtractPayload(W );                             and (4) the LLM Server itself, which uses FastAPI for the
 3    T ← CreateTask(P );                                 API layer, Redis for a low-latency cache, and Ray Serve
 4    Enqueue(Q, T ) ;     // asynchronous                to manage the lifecycle and deployment of the llama.cpp
       processing                                         inference engine (Algorithm 2).
5  Procedure ProcessTaskT                                 Model and Quantization: We deploy a code-specialized
 6    Rinf o ← T.repo_info;                               32-billion parameter model (a fine-tuned variant of
 7    Clocal ←                                            Qwen2.5) in a 6-bit GGUF quantized format. Quantiza-
       CloneOrUpdateRepo(Rinf o , T.pr_number);           tion reduces the VRAM footprint from approximately 64
                                                          GB for a bfloat16 model to under 24 GB, allowing it to fit
 8    Bconf ig ← GetBuildConfig(Rinf o );                 comfortably on a single enterprise GPU with minimal-to-no
 9    (RSA , Gcall ) ←                                    perceptible degradation in quality for this explanatory task.
       RunStaticAnalysis(Clocal , Bconf ig ) ;
                                                          On-demand Lifecycle: To maximize resource utilization
       // e.g., Coverity, Doxygen
                                                          in a shared compute environment, the model is loaded into
10    Dchunks ← GetDiffChunks(T.diff);
                                                          VRAM only upon the arrival of the first request in an empty
11    Vgrouped ←
                                                          queue (a cold start of ∼ 30–45 seconds) (Fu et al., 2024).
       GroupViolationsByChunk(RSA , Dchunks );
                                                          Ray Serve automatically unloads the model from the GPU
                                                          after a configurable idle timeout (e.g., 30 minutes), returning
12    foreach v ∈ Vgrouped do
                                                          the GPU capacity to the shared pool. Subsequent requests
13        Csnip ←
                                                          arriving while the model is warm bypass this loading cost
           ExtractCodeSnippet(Clocal , v.location);
                                                          entirely.
14       Cctxt ←                                          Throughput and Caching: The system uses multiple strate-
          GetCodeContext(Csnip , Gcall ) ;                gies to maximize throughput. Ray Serve minimally batches
          // sliding window, AST, call                    incoming requests to improve GPU utilization. A multi-
          hierarchy                                       tier cache minimizes redundant computation: a KV/prefix
15       PLLM ←                                           cache in llama.cpp accelerates prompts with shared prefixes
          GenPrompt(role, rules, v, Csnip , Cctxt );      (common when analyzing multiple violations of the same
                                                          rule) (Kwon et al., 2023), a Redis instance caches complete
16       SLLM ← QueryLLM(PLLM ) ;                         responses for several hours, and the PostgreSQL database
          // on-prem LLM endpoint                         provides a long-term, persistent cache of hashed request-
17       AppendToReport(SLLM );                           response pairs, deduplicating common violations across the
18    CP R ←                                              organization over weeks or months.
       FormatPRComment(AggregatedReport);           Reliability: All inference requests have a client-side time-
19    PostCommentToPR(Rinf o , T.pr_number, CP R ); out (e.g., 300 seconds) and employ an exponential backoff
                                                    retry strategy to handle transient GPU or network failures.
20    Cleanup(Clocal ) ; // remove local            The RabbitMQ queue provides backpressure signals to the
       clone                                        orchestrator during sustained high load. The system is de-
                                                    signed to fail closed: in the event of a timeout or unrecover-
                                                    able error, it logs the failure and posts no comment, rather
                                                    than providing partial or ungrounded feedback.
                                            Grounded AI for Code Review

 Algorithm 2: Multi-Tier Cached LLM Serving.               3.3.1    Observability, Security, and Audit
 Symbols: R: Request, P : Payload, C1 : L1 Cache           Tracing and Metrics: A lightweight Streamlit dashboard
 (In-Memory), C2 : L2 Cache (Persistent), M Q:             provides real-time observability by querying the Post-
 Message Queue, k1 : L1 Key, jid : Job ID, M :             greSQL database. It visualizes key performance indicators
 LLM Model, Lgpu : GPU Lock.                               across the entire lifecycle, including latency breakdowns,
   Require :An HTTP Request R.                             GPU utilization, error/timeout rates, and relevant metrics
   Ensure :An HTTP Response.                               for deployment.
 1 Procedure HandleRequestR
 2    Authenticate R; if fails then                        Security: The serving API is isolated on a private net-
 3       reject;                                           work, accessible only by the orchestrator via an API and
                                                           basic authentication. All source code, analysis reports, and
 4    k1 ← GenerateKey(R);                                 prompts remain on-premise, satisfying strict enterprise data
 5    Resp ← C1 .get(k1 );                                 residency and security requirements.
 6    if Resp ̸= NULL then
 7        return Resp ;    // L1 Cache Hit                 Auditability: For compliance and traceability, every PR
                                                           comment includes a detailed provenance record: the full
      // L1 Miss: delegate to
                                                           commit SHA, file path, line range, rule ID, and the version
           message broker
                                                           of the model used for generation. All deviation decisions
 8    P ← CreatePayload(R);
                                                           and comment lifecycles are persistently logged for periodic
 9    (Qr , cid ) ← M Q.setup_callback();
                                                           compliance reviews.
10    M Q.publish(P, Qr , cid );
11    Resp ← await M Q.get_response(Qr , cid );
12    C1 .set(k1 , Resp);                                  3.4     Dataset and Benchmark Construction
13    return Resp;                                         Our evaluation relies on a reproducible, hunk-level bench-
                                                           mark derived from 10 medium-scale C/C++ repositories.
14 Procedure ProcessTaskP
                                                           Seven are openly available upstream (diverse domains:
15    Tin ← GeneratePrompt(P );
                                                           embedded utilities, cryptography/math, protocol tooling,
16    jid ← hash(Tin );
                                                           and compression/hash libraries), two are internal variants
17    Resc ← C2 .get(jid ) ;    // Check L2
                                                           (forked adaptation), and one is an entirely internal com-
        Cache
                                                           ponent selected to reflect typical enterprise maintenance
18    if Resc = COMPLETE then
                                                           patterns (a mix of legacy and actively evolving subsystems).
19        Res ← Format(Resc ) ; // L2 Cache
                                                           Combined, the snapshot corpus spans roughly 600K lines of
           Hit
                                                           code after preprocessing (comments preserved for context
20    else                                                 extraction; generated/build artifacts excluded).
21        C2 .create_pending(jid , P );
22        Res ← ProcessLLM(Tin , jid );                    To approximate a realistic PR structure while enabling de-
                                                           terministic replays, we synthesize 100 PR scenarios that
23    M Q.publish_response(P.reply_to, Res, P.cid );       expand to 314 atomic hunks (a contiguous diff region plus
                                                           its associated static-analysis findings). Hunks preserve: (a)
24 Function ProcessLLMTin , jid                            original file paths and line spans, (b) rule identifiers and
25    Acquire Lgpu ;                                       severities emitted by the analyzer, and (c) sufficient un-
26    if M is UNLOADED then                                changed surrounding code for AST-guided context extrac-
27        M.load() ;            // Cold Start              tion. This ensures prompts constructed offline mirror pro-
                                                           duction grounding behavior (same token-shaping heuristics,
28    try                                                  rationale embedding, and rule metadata).
29          Ollm ← M.inference(Tin );
30          C2 .update(jid , ’COMPLETE’, Ollm );
31          Res ← Format(Ollm );                           Generation Pipeline. An idempotent pipeline produces
32    catch Exception e:                                   the benchmark: (1) clone or refresh each repository at a
33        C2 .update(jid , ’ERROR’, e);                    pinned commit; (2) enumerate candidate modification sites
34        Res ← FormatError(e);                            by sampling existing static-analysis findings and represen-
                                                           tative clean regions; (3) apply controlled source edits (e.g.,
35    finally:                                             introduce or remediate patterns, adjust control flow, perturb
36        Release Lgpu ;                                   literals) to create prospective pre/post states; (4) rebuild and
37        M.reset_unload_timer() ;        // Keep          re-run static analysis to capture rule deltas; (5) segment
            model warm                                     resulting diffs into atomic hunks; (6) serialize per-hunk
38    return Res;
                                                  Grounded AI for Code Review

metadata (pre/post violation vectors, file context slices, rule    outcomes). Unless otherwise noted, all metrics refer to the
rationale, diff stats) into data artifacts consumed by the eval-   automated benchmark environment (upper-bound capability;
uation harness. Each step records inputs (commit SHA, tool         not interactive wall-clock guarantees).
version, transformation seed), enabling exact regeneration.
                                                                   Our evaluation focuses on computable metrics generated by
                                                                   the harness: violation reduction, rule coverage, introduced
Open vs Internal Balance. Internal repositories con-               violations, effectiveness proxies, competitive outcomes, la-
tribute enterprise-specific idioms (custom build flags, legacy     tency (including first-feedback), edit efficiency, prompt com-
macro usage) that stress the robustness of context extrac-         pactness, ablation deltas, and directional survey perception
tion; open-source projects supply heterogeneity and external       signals.
reproducibility. We deliberately cap internal proportion to
avoid overfitting architectural claims to proprietary structure    4     R ESULTS
while still exercising on-prem build constraints.
                                                                   This section reports benchmark outcomes (automated;
3.5   Experimental Design and Metrics                              upper-bound capability) plus directional survey perceptions.
                                                                   All quantitative metrics derive from evaluation harness; sur-
We evaluate and compare the system on 10 C/C++ code-               vey data is qualitative only.
bases using a purpose-built offline benchmark that we con-
structed specifically to exercise the end-to-end grounded          4.1   Severity-Level Normalized Violation Reductions
review pipeline in a controlled, repeatable setting. The                 and Regressions
benchmark consists of 100 synthetic-but-replayable pull re-
quest submissions expanded into a total of 314 atomic hunks        The top row of Figure 2 reports two severity-level metrics:
(each hunk = a contiguous diff segment with associated             normalized violation reductions (left) and normalized re-
static-analysis findings), covering roughly 600K lines of          gressions (right). Let pre and post denote the number of
code. Each hunk is processed by an automated harness that          violations per item at a given severity level before and after
mirrors the production orchestrator’s core phases: isolated        the LLM-based fix, respectively. For items with pre > 0,
workspace materialization, context extraction, structured          reduction is computed as (pre − post)/pre; positive values
prompt generation, LLM invocation, patch application, re-          indicate improvement, negative values indicate regressions
build + static re-analysis, and rule delta computation. All        (i.e., increases where post > pre). For items with pre = 0
runs are performed on a single-GPU node (AMD MI210                 and post > 0, we record an introduction of 1.0 in the right
with 64 GB HBM, 64 vCPUs, 512 GB RAM) to provide a                 panel. Items with pre = post = 0 are excluded to avoid in-
stable hardware baseline.                                          flating apparent effectiveness with trivial no-change cases.
                                                                   This separation makes regressions explicit while preventing
This "AutoCodeReview" hunks benchmark is intentionally             inflation from absent baselines.
PR-shaped: hunks preserve original file paths, line spans,
and associated rule metadata so that prompt construction and       4.2   Union-Normalized Per-Rule Outcomes
grounding logic behave as they would inside a live CI/CD
pull request workflow. However, two important distinctions         The bottom-left panel of Figure 2 reports per-rule win rates
from real-time usage apply: (i) the offline harness automati-      across models/scenarios under a union-normalized evalu-
cally applies candidate patches and evaluates post-build rule      ation. For each rule in the union of all rules touched by
deltas, whereas the deployed system surfaces suggestions           any model, we compare outcomes pairwise and compute
(non-destructive) for human acceptance; and (ii) interactive       the fraction of rules where a given model outperforms its
ergonomic optimizations (deferred comment posting, UI              comparator. Rules untouched by a model in the post-fix are
pacing, incremental diff scoping, developer-driven retry)          treated as neutral (no win/loss), ensuring that unique and
are not modeled. Consequently, the latency and violation-          shared coverage are comparable and that non-participation
reduction numbers reported here may differ slightly from           is distinguished from underperformance.
those in production, and acceptance-oriented metrics (such
as developer adoption) are not directly observable in this         4.3   Latency, First-Feedback, and Throughput
setting.
                                                                   The bottom-right panel of Figure 2 and Table 1 summarize
Metric aggregation is performed in two passes: a first pass        timing and throughput. We decompose end-to-end wall-
that collects raw per-hunk outcomes (status, rule deltas,          clock latency into four phases: context preparation, LLM
diff characteristics, timing breakdown), and a second pass         inference, apply (patch/format), and build/analysis; total
that derives higher-level reporting metrics (effective fix rate,   latency is the sum of these phases. First-feedback latency is
coverage/introduced fractions, latency percentiles including       defined as LLM + build/analysis at the atomic-hunk level,
first-feedback, edit efficiency, ablation deltas, competitive
                                                     Grounded AI for Code Review




           (a) Normalized reductions by severity.                                       (b) Normalized increases/introductions.




            (c) Union-normalized per-rule outcomes.                            (d) Latency (p50 total, p95 whiskers, first-feedback).

Figure 2. Benchmark summary: severity-level reductions and introductions (top), per-rule outcome decomposition (bottom-left), and
latency characteristics (bottom-right). Reduction = (pre-post)/pre over violations with pre>0; new-only violations (pre=0, post>0)
contribute 1.0 to introductions.


Table 1. Per-profile summary of key metrics: reduction ratios, coverage, recall proxies, latency (p50 total and first-feedback), and edit
efficiency.
 Model                 Setting       Reduction.   NetRed    CovFrac    IntroFrac   WtdRPx     MacRPx      p50Tot(s)   p50FF(s)    Lines/Vio
 Claude-3.5            Ctx,NoRpt          0.127     0.066      0.632       0.500      0.145      0.233        37.64      37.64          2.59
 Claude-3.5            NoCtx,Full         0.471     0.305      0.904       0.456      0.593      0.644        37.92      37.92          2.28
 Claude-3.5            Ctx,Full           0.482     0.290      0.897       0.471      0.617      0.635        38.62      38.62          2.29
 Gpt-4o                Ctx,NoRpt          0.183     0.112      0.662       0.515      0.203      0.287        35.26      35.26          5.14
 Gpt-4o                NoCtx,Full         0.408     0.284      0.824       0.537      0.493      0.505        39.06      39.06          3.21
 Gpt-4o                Ctx,Full           0.456     0.285      0.882       0.603      0.576      0.572        35.30      35.30          3.02
 Qwen2.5-coder-23b     Ctx,NoRpt          0.095     0.005      0.574       0.581      0.112      0.201        51.63      51.63          5.76
 Qwen2.5-coder-23b     NoCtx,Full         0.332     0.192      0.794       0.574      0.409      0.448        53.88      53.88          3.34
 Qwen2.5-coder-23b     Ctx,Full           0.410     0.276      0.772       0.596      0.493      0.446        59.81      59.79          2.88
Reduction.: overall violation reduction ratio = (pre − post)/pre aggregated over violations with pre>0 (introduced-only rules excluded
   from the numerator); NetRed: net reduction after subtracting introduced violations (accounts for regressions); CovFrac: fraction of
distinct pre-existing rules for which at least one violation was reduced; IntroFrac: fraction of distinct rules that were newly introduced or
 increased; WtdRPx: weighted recall proxy = (sum of per-rule reductions in counts)/(sum of pre counts) (upper-bound recall; precision
unmeasured); MacRPx: macro (unweighted) recall proxy = mean over rules with pre>0 of per-rule reduction ratios; p50Tot: median (p50)
end-to-end pipeline time per hunk (s); p50FF: median first-feedback proxy (build + LLM phases only) (s); Lines/Vio: average changed
   lines per violation removed; Setting: context (Ctx vs NoCtx) and report formatting (Full vs NoRpt) configuration. All proxies omit
                                  precision because dismissals / false positives are not observable offline.


the earliest point at which an actionable comment can be                 4.4   Ablations and Context Economy
emitted. At the PR level, p95 total denotes the 95th per-
                                                                         Context and report-format ablations showed that trimming
centile of end-to-end completion time across PRs. Through-
                                                                         structured context reduced token footprint but degraded
put is reported as items per hour (PRs/hour and hunks/hour),
                                                                         recall proxies more than it improved latency, supporting
measured under the benchmark’s concurrency settings. Ta-
                                                                         retention of current context heuristics.
ble 1 provides per-phase statistics, PR-level totals (median
and p95), and the corresponding throughput figures.
                                               Grounded AI for Code Review

4.5   Developer Workflow Impact (Survey, Directional)           scenarios.
The internal survey (n=8) indicated directional (non-
                                                                5.3   Resource Efficiency in CI/CD
inferential) signals about workflow impact. Respondents
reported: mean self-reported time-to-first-feedback of 2.75     Quantization (6-bit), along with on-demand lifecycle man-
minutes (P75 = 4.0), immediate adoption of ∼ 50% of sur-        agement and multi-tier caching, achieved sub-minute p50
faced suggestions, and an overall adapt-or-accept rate of       first-feedback without multi-GPU scale-out. Caching (pre-
∼ 56% after iterative refinement. The median perceived          fix + Redis + persistent store) amortizes repeated rationale
clarity was 4/5, and grounding was rated 3.38/5. 57% of         for recurring rule patterns, reserving GPU cycles for novel
participants indicated fewer human review iterations after      hunks. This pattern is model-agnostic and portable to al-
adoption (none reported an increase). Qualitative free-text     ternative open-weight or fine-tuned variants. While we did
responses cited a lower cognitive load compared to raw          not evaluate cache hit rate or GPU-hour amortization in
static-analyzer output (less time spent triaging warnings)      this study, observed latency stability across hunk batches
and expressed a desire for optional, safety-gated patch sug-    suggests effective reuse.
gestions. These perception metrics are directional only and
motivate future objective instrumentation; they are not used    5.4   Extensibility Beyond MISRA
to instantiate statistical claims.
                                                                The architecture is analyzer- and standard-agnostic: the
                                                                orchestrator consumes any tool producing machine-readable
5     D ISCUSSION                                               findings (e.g., security scanners, style linters) and a rule
The evaluation demonstrates that a grounded hybrid design       registry. Swapping the analyzer primarily affects extraction
can provide rule-aware, low-latency review assistance on a      adapters and rule rationale lookups. Grounding, prompt
single shared GPU, while narrowing the performance gap          schema, deviation policy handling, and serving stack remain
with larger proprietary APIs. We now discuss the results        unchanged. This decoupling lowers the marginal cost of
in terms of design goals, generality, adoption factors, and     adding new languages or policy domains.
remaining risks.
                                                                5.5   Security, Cost, and Governance
5.1   Grounding Drives Actionable Precision                     Running an on-prem, quantized open-weight model keeps
Anchoring every comment to a concrete static-analysis find-     source code, prompts, and findings within enterprise bound-
ing (rule ID + file/line) focuses the LLM on targeted ra-       aries, avoiding external retention and token billing variabil-
tionale rather than unconstrained defect hunting, reducing      ity. Although GPT-4o and Claude 3.5 show higher abso-
hallucination and triage overhead. In Table 1, grounded con-    lute advisory reduction, the on-prem profile exhibits lower
figurations consistently improve recall proxies (e.g., GPT-4o   violation introduction rates (precision-on-change) and pre-
WtdRPx: 0.493→0.576; Qwen2.5 WtdRPx: 0.409→0.493)               dictable cost/latency, shifting optimization from pure model
and net reduction (Qwen2.5 NetRed: 0.192→0.276), with           accuracy to risk-adjusted efficiency (such as reductions per
modest latency trade-offs. AST-guided, token-budgeted           watt-hour / per dollar / per confidentiality boundary cross-
context provides sufficient semantics without prompt bloat;     ing). A composite efficiency metric (adding energy + GPU-
ablations that remove structured context degraded recall        hour counters) will make this explicit.
proxies more than they improved latency, supporting the
current heuristics.                                             5.6   Adoption and Socio-Technical Integration
                                                                Adoption hinged on PR-native delivery, deviation policy sup-
5.2   Competitiveness with Proprietary Baselines                port, and auditability (commit SHA, rule, line span, model
Despite using a modest-sized open-weight quantized model        version). Directional survey signals (≈ 50% immediate
(Qwen 2.5 32B, Q6K) with strict grounding, our system           uptake; ∼ 56% adapt-or-accept) reflect perceived clarity
delivers net violation reduction and recall comparable to       and grounding but also highlight the need for guarded, auto-
proprietary baselines (Table 1). In contrast to the preva-      generated patches. Integrating optional assisted patching
lent production pattern, ungrounded reviews powered by          and richer feedback loops (accepted vs. dismissed ratio-
proprietary LLMs, our grounded approach anchors com-            nale) is likely to further increase trust and measurable defect
ments to specific rules, yielding higher perceived quality      resolution speed.
and trust while maintaining similar coverage and acceptable
first-feedback latency. These results indicate that grounded,   5.7   Limitations
open-weight deployments can match the performance of the
                                                                We consolidate methodological limitations and validity
commonly deployed proprietary setups under the evaluated
                                                                threats:
                                                Grounded AI for Code Review

• Model / Analyzer Coupling: Quality is upper-bounded            • Agentic Workflows: Multi-turn clarification for ambigu-
  by static-analyzer coverage; deep semantic/data-flow de-         ous findings and chained reasoning for complex fix se-
  fects outside its rule surface remain unaddressed.               quences.

• Context Boundaries: Rare multi-file or macro-heavy
                                                                 Overall, grounding combined with resource-aware serving
  cases may exceed token budgets, causing omitted seman-
                                                                 strikes a pragmatic balance for grounded code reviews. It
  tics and weaker explanations.
                                                                 delivers a competitive reduction with lower introduction
• Operational Footprint: A GPU-equipped runner and               rates and enterprise-aligned governance, while preserving
  analyzer license are required; horizontal scaling may be       clear paths for precision estimation, assisted patching, and
  needed for extensive multi-tenant deployments.                 longitudinal adaptation.

• Evaluation Scope: Offline hunk benchmark omits inter-          6    C ONCLUSION
  active dynamics (developer negotiation, iterative refine-
  ment timing) and does not rerun alternative analyzers to       This paper presents a production-ready system for grounded,
  detect tool-induced false regressions.                         CI-native AI code review, delivering concise and actionable
                                                                 feedback by pairing the deterministic evidence of static anal-
• Measurement Gaps: No precision metric, no cache hit            ysis with resource-efficient large-model serving. Our hybrid
  %, GPU-hour, or energy telemetry, and no longitudinal          architecture, which leverages AST-guided context extrac-
  drift tracking; acceptance survey (n=8) is directional only.   tion, structured prompting, and a serving stack built on quan-
                                                                 tization and multi-tier caching, successfully meets stringent
• Internal / Construct Validity Risks: Potential instrumen-      enterprise requirements for latency, cost, and auditability
  tation bugs (diff segmentation, caching artifacts) mitigated   on a single shared AMD GPU. Our evaluation of medium-
  but not eliminated by snapshot hashing and subsample           scale, industrial repositories demonstrates strong rule cov-
  replays.                                                       erage and high-quality explanations, consistent sub-minute
                                                                 PR feedback, and substantial savings in computational re-
• External Validity: Corpus is C/C++ and MISRA-skewed;           sources. The system yields meaningful improvements to
  results may not transfer to dynamic languages or extreme       the developer workflow, including faster issue resolution, a
  template/meta-programming codebases.                           high fix-acceptance rate, and fewer residual violations post-
                                                                 merge. The architecture is standards-agnostic, providing a
• Unassessed Failure Modes: We did not validate compi-
                                                                 robust and extensible blueprint for deploying trustworthy
  lation/runtime correctness beyond static-analysis deltas;
                                                                 AI assistance in modern software engineering pipelines. We
  semantic regressions could pass undetected.
                                                                 plan to release the code for generating benchmarks and an
• Model Choice Rationale: Limiting comparisons to GPT-           evaluation harness to facilitate independent replication of
  4o and Claude 3.5 prioritized reproducibility and budget       results.
  over chasing the newest frontiers; reported gaps therefore
  understate the potential delta to the latest releases.         ACKNOWLEDGEMENTS
                                                                 We thank the AMD SSW AIE team and the AMD CI/CD
5.8   Future Work                                                platform team for early feedback, integration support, and
Planned directions target both breadth and depth:                iterative review of the auto code review system.

• Guarded Assisted Patching: Propose–rebuild–reanalyze           R EFERENCES
  loop with safety gating before surfacing patches.
                                                                 Agrawal, L. A., Kanade, A., Goyal, N., Lahiri, S., and Ra-
• Broader Standards / Languages: Integrate security (e.g.,         jamani, S. Monitor-guided decoding of code lms with
  CERT C/C++ (Nguyen et al., 2019)) and multi-language             static analysis of repository context. In Oh, A., Naumann,
  analyzers with minimal orchestration changes.                   T., Globerson, A., Saenko, K., Hardt, M., and Levine, S.
                                                                  (eds.), Advances in Neural Information Processing Sys-
• Learning from Feedback: Close the loop by using ac-              tems, volume 36, pp. 32270–32298. Curran Associates,
  cepted vs. dismissed comments to adapt prompts or con-           Inc., 2023.
  duct lightweight fine-tuning.
                                                                 Bennett, G., Hall, T., Winter, E., and Counsell, S. Semgrep*:
• Richer Telemetry: Add cache, energy, GPU-hour, and               Improving the limited performance of static application
  drift instrumentation for composite efficiency metrics.          security testing (sast) tools. In Proceedings of the 28th
                                                Grounded AI for Code Review

  International Conference on Evaluation and Assessment          Sadowski, C., Van Gogh, J., Jaspan, C., Soderberg, E., and
  in Software Engineering, pp. 614–623, 2024.                      Winter, C. Tricorder: Building a program analysis ecosys-
                                                                   tem. In 2015 IEEE/ACM 37th IEEE International Con-
Bosu, A., Greiler, M., and Bird, C. Characteristics of useful      ference on Software Engineering, volume 1, pp. 598–608.
  code reviews: An empirical study at microsoft. In 2015           IEEE, 2015.
  IEEE/ACM 12th Working Conference on Mining Software
  Repositories, pp. 146–156. IEEE, 2015.                         Thomson, P. Static analysis: An introduction: The fun-
                                                                   damental challenge of software engineering is one of
Cihan, U., Haratian, V., İçöz, A., Gül, M. K., Devran, Ö.,        complexity. Queue, 19(4):29–41, 2021.
  Bayendur, E. F., Uçar, B. M., and Tüzün, E. Automated
  code review in practice. In 2025 IEEE/ACM 47th Inter-          Vero, M., Mündler, N., Chibotaru, V., Raychev, V., Baader,
  national Conference on Software Engineering: Software            M., Jovanović, N., He, J., and Vechev, M. Baxbench:
  Engineering in Practice (ICSE-SEIP), pp. 425–436. IEEE,          Can llms generate correct and secure backends? arXiv
  2025.                                                            preprint arXiv:2502.11844, 2025.

                                                                 Walkowiak, B. and Walkowiak, T. Assessing inference time
Fu, Y., Xue, L., Huang, Y., Brabete, A.-O., Ustiugov, D.,
                                                                  in large language models. In International Conference
  Patel, Y., and Mai, L. {ServerlessLLM}:{Low-Latency}
                                                                  on Dependability of Computer Systems, pp. 296–305.
  serverless inference for large language models. In 18th
                                                                  Springer, 2024.
  USENIX Symposium on Operating Systems Design and
  Implementation (OSDI 24), pp. 135–153, 2024.                   Xie, D., Zheng, M., Liu, X., Wang, J., Wang, C., Tan, L.,
                                                                   and Zhang, X. Core: Benchmarking llms code reasoning
Göçmen, I. S., Cezayir, A. S., and Tüzün, E. Enhanced code         capabilities through static analysis tasks. arXiv preprint
  reviews using pull request based change impact analysis.         arXiv:2507.05269, 2025.
  Empirical Software Engineering, 30(3):64, 2025.
                                                                 Youn, D., Lee, S., and Ryu, S. Declarative static analysis for
Hatton, L. Safer language subsets: an overview and a case          multilingual programs using codeql. Software: Practice
  history, misra c. Information and Software Technology,           and Experience, 53(7):1472–1495, 2023.
  46(7):465–472, 2004.
                                                                 Zhang, H., Ning, A., Prabhakar, R. B., and Wentzlaff, D.
Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,            Llmcompass: Enabling efficient hardware design for
 C. H., Gonzalez, J., Zhang, H., and Stoica, I. Efficient          large language model inference. In 2024 ACM/IEEE
 memory management for large language model serving                51st Annual International Symposium on Computer Ar-
 with pagedattention. In Proceedings of the 29th sym-              chitecture (ISCA), pp. 1080–1096. IEEE, 2024.
 posium on operating systems principles, pp. 611–626,
 2023.                                                           Zhang, Z., Wang, C., Wang, Y., Shi, E., Ma, Y., Zhong, W.,
                                                                   Chen, J., Mao, M., and Zheng, Z. Llm hallucinations
Liargkovas, G., Panourgia, E., and Spinellis, D. Quieting          in practical code generation: Phenomena, mechanism,
  the static: A study of static analysis alert suppressions.       and mitigation. Proceedings of the ACM on Software
  arXiv preprint arXiv:2311.07482, 2023.                           Engineering, 2(ISSTA):481–503, 2025.

Lou, C., Qi, S., Jin, C., Nie, D., Yang, H., Liu, X., and Jin,
  X. Towards swift serverless llm cold starts with paraserve.
  arXiv preprint arXiv:2502.15524, 2025.

Nguyen, T. T., Maleehuan, P., Aoki, T., Tomita, T., and
 Yamada, I. Reducing false positives of static analysis for
  sei cert c coding standard. In 2019 IEEE/ACM Joint 7th
 International Workshop on Conducting Empirical Studies
  in Industry (CESI) and 6th International Workshop on
 Software Engineering Research and Industrial Practice
 (SER&IP), pp. 41–48. IEEE, 2019.

Rasheed, Z., Sami, M. A., Waseem, M., Kemell, K.-K.,
  Wang, X., Nguyen, A., Systä, K., and Abrahamsson, P.
  Ai-powered code review with llms: Early results. arXiv
  preprint arXiv:2404.18496, 2024.
