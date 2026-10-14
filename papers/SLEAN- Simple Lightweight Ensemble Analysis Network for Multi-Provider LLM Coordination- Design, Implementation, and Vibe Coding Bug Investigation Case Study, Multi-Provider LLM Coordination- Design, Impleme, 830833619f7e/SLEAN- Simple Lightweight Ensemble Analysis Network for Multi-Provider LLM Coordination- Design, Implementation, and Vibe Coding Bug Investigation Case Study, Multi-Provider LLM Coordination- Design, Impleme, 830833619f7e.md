SLEAN: Simple Lightweight Ensemble Analysis Network for
Multi-Provider LLM Coordination: Design, Implementation, and
Vibe Coding Bug Investigation Case Study
Matheus J. T. Vargas*
*Affiliation: CyAura AI, matheus@cyaura.ai




ABSTRACT
We present SLEAN (Simple Lightweight Ensemble Analysis Network), a deterministic framework for coordinating multiple LLM
providers through text-based prompt orchestration. Unlike complex multi-agent systems requiring specialized infrastructure,
SLEAN operates as a simple prompt bridge between LLMs using .txt templates, requiring no deep technical knowledge for
deployment. The three-phase protocol formed by independent analysis, cross-critique, and arbitration, filters harmful AI-
generated code suggestions before production deployment, addressing how AI-assisted debugging increasingly produces
modifications that introduce unnecessary complexity, break existing functionality, or address problems. Evaluating 15 software
bugs, we analyzed 69 AI-generated fix propositions. SLEAN's filtering accepted 22 fixes (31.9%, 95% CI 20.9-42.9%) while rejecting
47 that would have been harmful if applied verbatim. The arbitration process reduced code change surface by 83-90% relative to
raw AI outputs, enforcing minimal causal edits over scope-expanding modifications. Minimal Type 2 inputs proved more efficient
than detailed Type 1 inputs, requiring 2.85 versus 3.56 propositions per accepted fix (35.1% versus 28.1% acceptance, about a 20%
efficiency gain). Agreement between AI systems showed weak correlation with fix quality: high convergence (at least 80%) occurred
in 4 of 15 cases and improved acceptance by only 2.4% points; arbitration appeared only at exactly 10% convergence in 2 of 15
cases, although low convergence alone did not necessitate arbitration. The file-driven, provider-agnostic architecture enables
deployment without specialized coding expertise, making it applicable to security auditing, code review, document verification,
and other domains requiring reliable multi-provider synthesis with end-to-end auditability.


Keywords: multi-provider LLMs, automated program repair, consensus workflows, large language models, bug investigation,
practical deployment



BACKGROUND
Large Language Models (LLMs) have shown significant                  pipelines,    maintain   deterministic    behavior     for
promise in data analysis, code generation, and automated             reproducibility, and operate reliably without specialized
program repair, yet practical deployment faces a                     deployment environments. 12–14
fundamental tension between analytical sophistication and
                                                                     We propose a middle path that leverages multiple LLM
deployment complexity.1–4 Single-model approaches suffer
                                                                     providers through structured workflows without requiring
from inherent biases and inconsistencies that can yield
                                                                     complex multi-agent infrastructure. We have named it
incomplete or incorrect answers, especially in complex
                                                                     Simple Lightweight Ensemble Analysis Network (SLEAN). We
problems.5     Meanwhile,       sophisticated  multi-agent
                                                                     aim at a minimal-overhead Python setup that runs smoothly
frameworks demonstrate impressive collaborative reasoning
                                                                     on a local machine. Our approach treats different providers
but require complex, stateful runtime environments that are
                                                                     as complementary analytical resources orchestrated through
impractical for many production pipelines as well as for
                                                                     simple, deterministic protocols. Rather than implementing
general use, for example, vibe coders.6,7
                                                                     long-lived agent processes with persistent state, we employ
Existing orchestration frameworks such as CrewAI, AutoGen,           a static orchestration model with three fixed phases:
LangGraph, Swarm, and Voyager excel at multi-agent                   independent analysis, cross-critique, and final arbitration.
collaboration through persistent agent memory, complex               Our coordination protocol follows three phases that
role negotiation, and graph-based orchestration.5,8–10               preserve independence while enabling structured synthesis.
However, these capabilities come at substantial
                                                                     In Phase 1, each provider receives the same task description
infrastructure cost and the use of single choice LLM.11
                                                                     with the same corpus and produces an independent audit
Complex problems, such as production debugging
                                                                     without seeing the output of its peer(s). Inputs may be
workflows, require solutions that integrate seamlessly with
                                                                     segmented per provider to respect context limits, but the
existing continuous integration/continuous delivery (CI/CD)
                                                                                                                                1
source material is identical. These audits are saved verbatim     condition our Phase 1 enforces by isolating providers during
as artifacts, which fixes the baseline for later review and       independent audits.26 Subsequent syntheses formalized
supports      reproducible     analysis.   Providers    never     voting, stacking, and bagging as general strategies for
communicate directly; all interaction flows through the           aggregation, which map naturally onto our deterministic
orchestrator with fixed prompts, which prevents early             arbitration in Phase 3.24,27 Random Forests further quantified
convergence and captures the provenance of every claim.           how ensemble error depends on member strength and inter-
                                                                  member correlation, reinforcing our emphasis on
Phase 2 introduces cross-critique under symmetric prompts.
                                                                  heterogeneity and controlled synthesis rather than
Each provider reads the original inputs together with its own
                                                                  unconstrained interaction.28
Phase 1 audit and the peer audit, then issues a consolidated
assessment that records points of agreement,                      In automated bug investigation and repair, recent systems
disagreements, and any proposed changes. These                    show that LLMs can localize faults without tests, suggesting
consolidations remain independent products, preserving            that code and natural-language priors can substitute for
diversity while exposing conflicts. In Phase 3 an arbitrating     traditional coverage signals in some settings. 29 Conversation-
provider consumes the original inputs, both audits, and both      driven repair illustrates how multi-turn guidance improves
consolidations and produces the definitive synthesis. The         patch quality on standard benchmarks, although it increases
final artifact lists accepted and rejected fixes with             orchestration surfaces that must be engineered and audited
justification and attribution, stores contribution percentages,   in production.30 Self-supervised repair pipelines use test-
and preserves every intermediate file in a versioned              execution feedback to reduce human labelling while
directory. This sequencing yields determinism at the              maintaining correctness, which underscores the value of
workflow level, minimizes uncontrolled coupling between           reproducible control flow and persisted artifacts when
models, and provides an auditable trail that can be               models propose many candidate changes. 31 Generation-
integrated into continuous delivery pipelines.                    centric studies in multilingual settings show that disciplined
                                                                  selection and filtering of model outputs can be an effective
As a case study, we address a practical scenario common in
                                                                  baseline, aligning with our focus on consensus formation and
software development, especially in this new vibe coding
                                                                  explicit rejection of non-causal edits.32
era: given a bug description and associated codebase,
multiple independent LLM providers analyze the issue,             Operationally, bringing learning systems into continuous
critique each other's findings, and a final provider arbitrates   delivery places a premium on transparency and auditability
the consensus fix. This workflow produces detailed analysis       of decisions, which motivates our design choice to persist
while maintaining the deployment simplicity required for          intermediate artifacts and attributions across phases. 33
production integration. It is light-weight and can easily run     Interpretable reporting frameworks advocate standardized
locally or without much cloud resources, making it practical      summaries of model behavior and limitations to support
and easily deployable.                                            downstream accountability, a practice our versioned outputs
                                                                  and contribution ledgers make concrete for bug investigation
RELATED WORK                                                      workflows. 34 Experience reports in software engineering for
There are several agent-oriented orchestrators. CrewAI            machine learning highlight the engineering frictions of
implements role-based orchestration with hierarchical task        integrating model-driven components into CI pipelines,
delegation, AutoGen provides conversational workflows with        which our configuration-driven orchestration addresses by
dynamic group interactions, and LangGraph offers graph-           fixing prompts, parameters, and file artifacts for reproducible
structured coordination patterns.8,15–17 Recent advances          runs.35
include ChatDev's virtual software teams with specialized
communication protocols,           MetaGPT's standardized         KEY DIFFERENCES OF SLEAN
operating procedures for structured coordination, and             Our contribution is a deterministic, file-driven coordination
Swarm's scalable collaboration with memory sharing.16,18,19       protocol across multiple LLM providers that yields auditable
Domain-specific systems like FixAgent implement three-level       artifacts at each phase (independent audits, cross-
coordination (Localizer, Repairer, Analyzer) while                consolidations, and arbitrated synthesis) and integrates
AGDebugger provides interactive debugging with user               cleanly with CI/CD. Unlike conversational multi-agent
steering capabilities.20,21 These systems require substantial     controllers that rely on long-lived agent state and role
infrastructure investment that limits practical adoption.22,23    negotiation, our design enforces isolation in Phase 1,
                                                                  recorded critique in Phase 2, and a single, attributable
A complementary foundation for coordinated analysis comes
                                                                  arbitration in Phase 3, aligning with ensemble-learning
from ensemble learning, which shows that diversity across
                                                                  principles for diversity and controlled aggregation while
models can reduce variance and improve reliability when
                                                                  emphasizing reproducibility and provenance for production
outputs are aggregated under a principled rule.24,25 Classic
                                                                  workflows. Table 1 shows the key SLEAN differences.
work demonstrated that combining independent learners
improves accuracy when their errors are decorrelated, a

                                                                                                                               2
Table 1. Differences between SLEAN and representative prior studies.

           AXIS                                 SLEAN                                       LITERATURE                    WHY IT MATTERS FOR PRACTICE
     EXECUTION MODEL          Deterministic orchestration of multiple            Multi-agent frameworks require         Deterministic, repeatable runs reduce
                               LLM providers through a fixed three-                  complex, stateful runtime           orchestration variance and enable
                              phase workflow: independent analysis,          environments with persistent agent           precise regression analysis during
                                cross-critique, and final arbitration.    memory, complex role negotiation, and                       CI/CD. 37–39
                               Static orchestration model with three          graph-based orchestration (CrewAI
                                 strictly ordered phases that yields       hierarchical task delegation, AutoGen
                                determinism at the workflow level.          conversational workflow, LangGraph
                                                                                  graph-structured coordination,
                                                                            ChatDev virtual software teams, and
                                                                                MetaGPT standardized operating
                                                                                        procedures. 8,15,17,18,36
     STATE & ISOLATION        Providers never communicate directly;                Multi-agent systems maintain           Early isolation reduces correlated
                                  all interaction flows through the       persistent agent state and enable direct        errors and supports decorrelated
                              orchestrator with fixed prompts. Phase       communication between agents, with           evidence before aggregation, a classic
                                1 enforces complete independence           complex messaging protocols and role             ensemble prerequisite. 11,25,26
                                 where providers do not see peer                  negotiation (CrewAI role-based
                                 outputs. Provider independence           orchestration, AutoGen dynamic group
                               enforced by orchestrator mediation.              interactions, ChatDev specialized
                                                                              communication protocols, domain-
                                                                             specific systems like FixAgent three-
                                                                                     level coordination).8,15,18,21
  AGGREGATION PRINCIPLE        Single arbitrating provider receives all           Multi-agent frameworks rely on            Controlled aggregation maps to
                               prior artifacts and produces definitive        conversational consensus or graph            voting/bagging/stacking ideas and
                                synthesis with explicit accept/reject              search without deterministic,          lowers variance when members are
                                      decisions and guidance.             attributable combination rules (Graph-        diverse while keeping a clear audit trail.
                                                                                                                                        15,25,26,40,41
                                                                            of-Thoughts collaborative reasoning,
                                                                          AutoAgents graph search, and ChatDev
                                                                                conversational consensus). 11,16,18
    PROVIDER STRATEGY          Treats providers such as OpenAI GPT                 Multi-agent systems typically           Cross-provider diversity increases
                                      and Anthropic Claude as                instantiate roles over a single model       hypothesis variety, which ensembles
                               interchangeable analytical resources          family or within one vendor runtime        leverage for reliability when errors are
                                via unified API abstraction. Exploits        (CrewAI single-model orchestration,              partially independent.25,26,36
                                  analytical diversity without role       AutoGen single-vendor focus, ChatDev
                                  negotiation or provider-specific                homogeneous teams, MetaGPT
                                           specializations.                   standardized procedures). 8,15,17,18,36
       PROVENANCE &               Preserves complete artifacts for               Multi-agent frameworks provide              Provenance supports post-hoc
        AUDITABILITY             reproducible audits. Orchestrator             inconsistent artifact reporting and         accountability and reproducibility
                               constructs fresh, zero-padded results         attribution tracking, with debugging       expectations in production ML & other
                                directory for every run. Every phase               challenges for complex agent          software engineering pipelines. 35,43,44
                               emits versioned files with attribution           interactions (human-factors work
                                 and rejection rationales persisted.        highlights debugging challenges, and
                                                                               model-reporting standards call for
                                                                                    structured summaries). 21,42
     CI/CD INTEGRATION        File-driven, configuration-based design            Multi-agent frameworks require              Pure file artifacts mesh with
                                eliminates infrastructure overhead.        specialized deployment environments          reproducible-builds ethos and supply-
                                Configuration parameters primarily                  with complex infrastructure             chain integrity practices, and
                                   defined in YAML files. Provides            dependencies and stateful services         predictable runs ease rollbacks and
                               auditable trail that can be integrated      (substantial infrastructure investment             diff-based reviews. 12,46–48
                                 into continuous delivery pipelines.             limits adoption, and operational
                                                                            frictions occur when systems depend
                                                                                    on stateful services). 13,23,45
   EXPLORATION VS. SCOPE      Cross-review explores breadth through              Multi-agent exploration through         Strict pruning limits blast-radius risk
         CONTROL              symmetric prompts; arbitration applies        conversational reasoning can expand            and review load, consistent with
                                 strict scope discipline, privileging        scope without explicit accept/reject        disciplined change-management in
                               minimal causal remedy over broader          accounting (conversational consensus                 production systems. 49–51
                                                edits.                    in ChatDev, graph search in AutoAgent,
                                                                                 role negotiation in CrewAI). 8,11,18
     LINK TO THEORY &         Explicitly aligns with ensemble-learning        Multi-agent frameworks emphasize           The design operationalizes ensemble
         EVIDENCE              principles: Phase 1 isolation enforces            collaborative reasoning and role        benefits while satisfying engineering
                                 decorrelated errors condition from                specialization without explicit         requirements for traceability and
                                classic ensemble theory; arbitration              grounding in ensemble learning                  reproducibility. 24,25
                                implements principled aggregation;         principles for diversity and controlled
                                    outcomes fully attributable.          aggregation (role-based specialization,
                                                                           conversational workflows, and virtual
                                                                                      team coordination). 8,11,18




                                                                                                                                                                     3
METHODOLOGY AND SYSTEM DESIGN                                          orchestrated three-phase analysis workflow maintains
                                                                       provider independence and enables systematic peer review
System Architecture Overview                                           and consensus formation.
SLEAN is a layered multi-provider LLM framework that                   Figure 1 illustrates the simplified architecture and the
leverages complementary model strengths under a                        controlled flow of information through five principal layers.
deterministic protocol and preserves complete artifacts for            The Input Layer manages all inbound resources, including
reproducible    audits.    Providers are      treated     as           configuration files, environment variables, bug descriptions,
interchangeable analyzers behind a unified abstraction layer,          relevant codebase folders, and prompt templates. It also
enabling substitution or integration without infrastructure            supports utility operations such as connection testing and
changes or role negotiation. The design eliminates direct              initial project setup. Inputs are prepared into a structured
provider-to-provider messaging to avoid the hidden state               form suitable for analysis before processing.
while still aggregating diverse reasoning outputs. An




                                 Figure 1. SLEAN diagram showing its different components and phases.



                                                                                                                                  4
Provider Abstraction and Coordination Framework                    token limits. Providers do not see peer outputs in this phase.
                                                                   The analyses 𝐴𝑖 are saved as structured reports and establish
The system uses four input categories at the start: Bug
                                                                   the baseline. Providers never communicate directly; all
Description (problem statement with constraints), Codebase
                                                                   routing occurs through orchestrator maintaining
(recursive folder scan with supported extensions excluding
                                                                   architectural isolation.
build/cache directories), Configuration (YAML/JSON with
environment variable substitution for ${VARNAME}                   Phase 2. Cross-Review and Consolidation.
patterns), and Prompts (phase-specific templates). The             Each provider receives the task description, the full corpus,
orchestrator creates zero-padded results directory                 its own Phase 1 report, and the peer’s Phase 1 report, and
(bug0001_results, bug0002_results) ensuring lexicographic          then produces a consolidated analysis. Prompts are
ordering, copies input files for complete provenance, and          symmetric in the sense that they distinguish own from other,
rewrites all output paths to the versioned directory.              rather than being literally identical. Given by (eq. 2),
Configuration loading initializes dotenv early, performs                      𝐶𝑖 = 𝑃𝑖 (𝑡𝑎𝑠𝑘𝑑𝑒𝑠𝑐𝑟𝑖𝑝𝑡𝑖𝑜𝑛 , 𝑐𝑜𝑟𝑝𝑢𝑠, 𝐴𝑖 , 𝐴𝑗≠𝑖 ) (eq. 2)
environment substitution within APIs section, and
instantiates providers through factory pattern behind the          where 𝐴𝑗≠𝑖 is the Phase 1 analysis from the peer provider
standardized AIClient interface. The abstract base class           where 𝑗 ≠ 𝑖. This step enables peer review that can surface
enforces explicit temperature and max_tokens parameters,           disagreements, omissions, or errors, while each 𝐶𝑖 remains
where construction fails if either is missing, and provides        the work of a single provider, which preserves analytical
uniform _make_api_request wrapper with exponential back-           diversity.
off and bounded retries, surfacing HTTP payloads for
                                                                   Phase 3. Synthesis and Arbitration.
diagnosis. OpenAIClient normalizes endpoints to ensure
exactly one /v1 segment before calling chat-completions;           An arbitrating provider receives all prior artifacts together
AnthropicClient uses x-api-key authentication with required        with the original inputs and produces the final output. Given
anthropic-version header posting to /v1/messages.                  by (eq. 3),
                                                                             𝐹 = 𝑃𝑎 (𝑡𝑎𝑠𝑘𝑑𝑒𝑠𝑐𝑟𝑖𝑝𝑡𝑖𝑜𝑛 , 𝑐𝑜𝑟𝑝𝑢𝑠, ⋃𝑛𝑖=1 𝐴𝑖 𝐶𝑖 ) (eq. 3)
Corpus ingestion performs a recursive folder scan collecting
supported extensions in stable sorted order, reads files with      where 𝑃𝑎 is the arbitrator selected in the workflow
UTF-8 decoding and recovery path for non-UTF-8 bytes, and          configuration and 𝐹 is the definitive result such as
assembles structured text with clear delimiters (# =====           recommendations, decisions, or an action plan, and we have
filename =====) enabling safe chunking. Prompt                     the collection of all analyses from multiple providers.
management validates prompts folder existence and ensures          Optional elements such as attribution or confidence follow
referenced files are non-empty, externalizing content for          the prompt template and are not enforced by program logic.
domain-agnostic template swapping.
                                                                   The sequential structure, explicit configuration that requires
Phase 1. Independent Analysis with Token Management                at least temperature and max tokens, and persisted artifacts
The orchestrator routes bug description and structured             support reproducible audits of runs. Independence in Phase
codebase to Phase 1 Analysis, which applies token                  1 reduces early coupling, and peer review in Phase 2
management before provider distribution. The token                 supports systematic error detection and broader coverage.
manager estimates tokens from character counts using               Full determinism or bias elimination is not guaranteed by
provider-specific ratios, applies provider-specific context        code and depends on model settings and prompt design.
limits with 75% safety margin for prompt scaffolding and
                                                                   Results Collection and Audit Trail
response generation. When content exceeds limits, it
segments along file boundaries using structured headers            All five outputs (Audit Report A, Audit Report B,
from corpus ingestion, truncating single oversized files at line   Consolidation A, Consolidation B, Definitive Fixes) flow into
boundaries with explicit elision markers.                          the versioned results directory alongside copied input files.
                                                                   This creates a complete audit trail enabling reproducibility
Each provider analyzes the same sources, namely a task             verification, run comparison, and systematic analysis of
description and an evidence corpus, subject to provider            provider behavior across different configurations. Error
specific token limits that can require segmenting the corpus       handling flows uniformly through provider abstraction layer
for each provider. Given by (eq. 1),                               with consistent failure surfacing regardless of underlying
           𝐴𝑖 = 𝑃𝑖 (𝑡𝑎𝑠𝑘𝑑𝑒𝑠𝑐𝑟𝑖𝑝𝑡𝑖𝑜𝑛 , 𝑐𝑜𝑟𝑝𝑢𝑠_𝑐ℎ𝑢𝑛𝑘𝑠𝑖 ) (eq. 1)     provider implementation.

where 𝑃𝑖 is provider 𝑖 under the unified client interface,         The sequential structure with explicit configuration
𝑡𝑎𝑠𝑘𝑑𝑒𝑠𝑐𝑟𝑖𝑝𝑡𝑖𝑜𝑛 is the problem statement with any                  requirements, provider isolation through orchestrated
constraints, 𝑐𝑜𝑟𝑝𝑢𝑠 is the full evidence set such as code,         routing, and comprehensive data persistence supports
documents, data, or logs, and 𝑐𝑜𝑟𝑝𝑢𝑠_𝑐ℎ𝑢𝑛𝑘𝑠𝑖 denotes the           reproducible audits while accommodating diverse provider
segments of that corpus prepared for provider 𝑖 to satisfy         capabilities within controlled execution envelope.

                                                                                                                                       5
Table 2. Bug types and general information.

 Bug ID          Domain                            Number of Files        Bug Description (chars)           Codebase (Chars)
 001             Authentication                         4                          518                            4395
 002             Algorithmic Error                      4                           84                            8332
 003             Logic Error                            4                          107                           10891
 004             Transaction Integrity                  4                         2607                           11453
 005             Data Synchronization                   5                          194                           16647
 006             Null Reference                         4                         1194                           17793
 007             Distributed Systems                    6                           64                           35211
 008             Configuration                          5                         1225                            3266
 009             Concurrency                            7                          353                            5773
 010             Regex Performance                      5                         1213                           11096
 011             Race Condition                         5                         7006                           13906
 012             Server Imbalance                       4                          760                           21109
 013             Wrong Cache and Calculations           5                           92                           26699
 014             Scheduling and Parsing                 5                          145                           13649
 015             Data Validation/Edge Case              6                          164                           40499
 Average         -                                     ~5                        ~1,048                         ~16,048




CASE STUDY METHODS                                                   public users rather than professional developers ("vibe
                                                                     coder" simulation). Stack traces, where present, consisted of
Data Sources and Collection                                          authentic terminal output copied directly from error logs
We systematically analyzed 15 software debugging                     without modification.
scenarios, each consisting of a deliberately buggy codebase
                                                                     Configurations
paired with a casual user bug report. Each scenario was
documented through structured definitive fix reports                 Experiments used a Python runner (main.py) with YAML
(definitive_fixes_001.md through definitive_fixes_015.md)            configuration managing provider assignments, model
containing AI-assisted debugging performance metrics,                specifications, and parameters. AIA was assigned to OpenAI
contribution assessments, proposed solutions, and final              (gpt-3.5-turbo, temperature=0.1, max_tokens=3000), AIB to
arbitration decisions.                                               Anthropic (claude-sonnet-4-20250514, temperature=0.1,
                                                                     max_tokens=4000), and the final arbitrator to OpenAI with
The experimental design employed autogenerated                       identical AIA settings. This created an OpenAI-Anthropic-
codebases with strategically embedded bugs to simulate               OpenAI workflow with retry logic (3 attempts, exponential
realistic debugging challenges, especially found by vibe             backoff) and API authentication via environment variables.
coders. Codebases were intentionally provided without bug
identification markers, and diagnostic information was               Pre-run validation verified API connectivity and token limits
deliberately limited to increase discovery difficulty for AI         using character-to-token ratios of 0.25, with context limits at
systems. Bug selection criteria prioritized single-run               16,000 tokens (OpenAI) and 200,000 tokens (Anthropic),
resolvable issues, while some codebases contained multiple           applying 75% safety margins before automatic chunking
bugs, non-crashing bugs were co-located to enable                    (applied only in Phase 1 for initial testing; see Future Work).
simultaneous resolution, whereas crash-inducing bugs were            The workflow consumed four inputs: bug.txt (problem
isolated as single defects to prevent multi-stage debugging          description and traces), codebase/ directory (source code),
requirements.                                                        config.yaml (environment variables), and three prompt
                                                                     templates. Three distinct prompt templates controlled each
The dataset encompasses diverse codebase complexities                workflow phase. The bug_slayer_prompt.txt directed Phase
(Table 2) and bug report verbosity levels, ranging from              1 independent analysis, requiring structured output with
minimal 64-character casual descriptions to comprehensive            executive summary, root cause analysis, prioritized fixes with
7,006-character diagnostic logs. The codebase sizes varied           exact code snippets, implementation strategy, and testing
from compact 3,266-character implementations to complex              recommendations. audit_consolidator_prompt.txt guided
40,499-character systems, enabling evaluation across                 Phase 2 cross-critique through systematic methodology:
different code comprehension and analysis demands.                   technical accuracy assessment, investigation depth
User Input Scenario Classification                                   evaluation, fix quality analysis, and evidence strength
                                                                     verification, culminating in superior synthesis with quantified
User prompts were extracted from bug report files
                                                                     contribution percentages. final_consolidator_prompt.txt
(bug_001.txt through bug_015.txt) and systematically
                                                                     enforced Phase 3 arbitration via contradiction detection,
categorized based on information completeness and
                                                                     peer review validation, and five quality gates (technically
diagnostic complexity. To simulate realistic debugging
                                                                     sound, peer validated, non-conflicting, minimal impact,
scenarios encountered by AI systems, we deliberately
employed casual, non-technical language typical of general
                                                                                                                                  6
evidence-backed) with explicit rejection criteria and                       Analysis
directness requirements.                                                    Two binary classification schemes were implemented. The
Source code was recursively scanned excluding build                         Arbitration Flag was set to TRUE when Final Arbitration ≥
directories, filtering 24 file extensions (.py, .js, .java, .cpp, .c,       50%, indicating scenarios requiring substantial extra
.h, .cs, .php, .rb, .go, .rs, .ts, .jsx, .tsx, .vue, .swift, .kt, .scala,   (arbitrator layer) intervention. The Convergence Flag was set
.r, .sql, .html, .css, .json, .xml, .yaml, .yml, .md, .txt), and            to TRUE when Convergent contribution ≥ 75%, identifying
assembled with UTF-8 encoding into structured text with file                cases where AI systems achieved high levels of agreement
boundary delimiters and metadata headers.                                   without the arbitration layer.

Each run executed a deterministic sequence: Phase 1 to 3 as                 Data extraction underwent systematic verification through
identical prompts (bug description + codebase) sent to AIA                  document-by-document audit procedures. Each contribution
and AIB independently for parallel analysis. Phase 2 enabled                percentage was cross-referenced against source document
cross-critique where each AI reviewed the peer's Phase 1                    headers using exact text matching. Fix counts were validated
output alongside original inputs. Phase 3 provided all                      by manual enumeration of all Fix #N entries and rejected
previous artifacts to the arbitrator for final synthesis.                   approach listings. Calculated fields were verified through
Each run generated versioned directories (bug0001_results,                  independent mathematical computation. Boolean flag
etc.)    containing     input     copies     and      artifacts:            assignments were confirmed through rule-based logic
audit_report_A.md (AI analysis), audit_report_B.md (AIB
                        A                                                   verification. This multi-stage validation process ensured
analysis),    consolidation_A.md       (AIA     cross-critique),            100% data integrity across all table entries. The bug fixes
consolidation_B.md         (AI B
                                     cross-critique),       and             were checked manually, applied and tested in the code,
definitive_fixes.md (arbitrator synthesis).                                 ensuring that they fixed the proposed bugs.

AI contribution percentages were extracted directly from                    The analysis maintained strict adherence to source
standardized headers in each definitive fix document. Four                  document specifications without statistical interpolation or
contribution categories were systematically recorded: (i) AIA               estimation. All percentages, counts, and derived metrics
CONTRIBUTION, representing the first AI system's individual                 were computed deterministically from explicitly stated
contribution; (ii) AIB CONTRIBUTION, representing the                       values in the definitive fix documentation. No data
second AI system's individual contribution; (iii) CONVERGENT                imputation or statistical modeling was employed, ensuring
(BOTH AGREED), representing collaborative solutions where                   direct traceability between table entries and source
both AI systems reached consensus; and (iv) FINAL                           evidence.
ARBITRATION, representing the arbitrator's intervention, or                 All source documents (definitive_fixes_001.md through
final reviewer, which in this case is also AI B.                            definitive_fixes_015.md) and extraction protocols are
We employed systematic content analysis to quantify                         available for independent verification and replication of
debugging solutions. Accepted fixes were identified by                      results at github.com/cyaura-open.
enumerating all items listed under "DEFINITIVE FIX LIST"                    All fixes were independently validated by applying each fix to
sections, with each Fix #N entry counted as one accepted                    the buggy codebase, executing the program with test inputs,
proposition. Rejected fixes were quantified by cataloguing all              and verifying resolution of the reported behavior. Rejected
items explicitly listed in "REJECTED FIXES" sections of each                fixes were reviewed to confirm they would introduce errors,
document. Total fix propositions were calculated as the sum                 break functionality, or expand scope unnecessarily.
of accepted and rejected fixes. This approach ensured
comprehensive capture of all debugging attempts while                       RESULTS
maintaining clear distinction between successful and                        We identified two distinct input categories (Table 3) based
unsuccessful solutions.                                                     on the availability of technical diagnostic information: (i)
Acceptance rates were computed using the formula:                           Technical/Diagnostic Issues (n=8, 53%), providing substantial
Acceptance Rate = (Accepted Fixes / Total Fix Propositions) ×               technical information including complete terminal error
100, with results expressed as percentages rounded to one                   output with file locations and exception types, detailed
decimal place. This metric provided a quantitative measure                  system logs, reproduction commands, or comprehensive
of debugging efficiency for each scenario.                                  execution traces, paired with casual problem descriptions;
                                                                            and (ii) Functional/Behavioral Issues (n=7, 47%), containing
Several composite metrics were calculated from primary                      informal problem statements using everyday language
data. Total AI contribution was computed as AIA + AIB,                      without technical diagnostics, describing behavioral
representing the combined two AIs without the third AI                      inconsistencies or system malfunctions through user-
arbitration. Max Contributor was determined by identifying                  observable symptoms.
the category (AIA, AIB, Convergent, or Arbitrator) with the
highest percentage contribution for each bug scenario.

                                                                                                                                        7
Table 3. Bug description by the users divided into 2 categories.

          CATEGORY                                        DEFINITION                                   BUG IDS                      N                  %
   TECHNICAL/DIAGNOSTIC            Substantial technical information including stack traces,    001, 004, 006, 008, 009,            8                  53
       ISSUES (TYPE 1)              detailed system output, reproduction commands, or                010, 011, 012
                                                comprehensive execution logs
  FUNCTIONAL/BEHAVIORAL            Informal problem statements using everyday language          002, 003, 005, 007, 013,             7                 47
      ISSUES (TYPE 2)                without technical diagnostics, describing behavioral              014, 015
                                        inconsistencies or user-observable symptoms




Figure 2. (top-left) Distribution of total, accepted, and rejected bug fix propositions. (top-right) Fix acceptance rates and efficiency by input description type.
(bottom-left) Relative AI contribution for the fixes by input type. (bottom-right) Convergence rates between AI systems by input type




Technical/Diagnostic Issues included: Bug 001: "User                                    cache system is completely broken!" [emotional, non-
registration fails with 500 error" [authentic TypeError stack                           technical language]; Bug 013: "different ways of calculating
trace]; Bug 004: "something is clearly incorrect in my system,                          customer revenue give different results" [calculation
fix it" [complete banking transaction terminal output]; Bug                             discrepancy]; Bug 014: "it is failing to scheduling there is a
006: "the code crashed" [authentic AttributeError stack                                 problem with the slots and there is a isoformat string that is
trace]; Bug 008: "code crashes" [authentic ImportError                                  invalid" [scheduling malfunction]; Bug 015: "The system is
circular import stack trace]; Bug 009: "I have a nasty bug once                         still counting stocks I sold as if I still own them, which makes
I run the below in powershell" [PowerShell load testing                                 my portfolio value calculations completely wrong" [portfolio
command]; Bug 010: "bugs when I run the below" [curl                                    calculation error].
command with full HTTP response output]; Bug 011: "my
                                                                                        SLEAN was tested across 15 software bugs spanning diverse
results seem incorrect, there is a hidden bug in my code"
                                                                                        fault domains, with system-wide performance metrics for
[extensive job scheduler execution logs]; Bug 012:
                                                                                        both bug input types presented in Figure 2. The complete
"something is odd with the load distribution of servers"
                                                                                        dataset comprised 69 individual fix propositions, of which 22
[detailed load distribution metrics and capacity analysis].
                                                                                        were accepted and 47 were rejected, yielding an overall
Functional/Behavioral Issues included: Bug 002: "my                                     acceptance rate of 31.9% (95% CI: 20.9–42.9%).
calculations seem to be incorrect. fix them." [no technical
                                                                                        We stratified the dataset by input format: Type 1 inputs
details]; Bug 003: "something is wrong with my management
                                                                                        (detailed diagnostic information, n = 8) versus Type 2 inputs
system but I am unsure what it is" [vague description]; Bug
                                                                                        (minimal colloquial descriptions, n = 7). Type 1 inputs
005: "Different ways of counting tasks in our system give
                                                                                        generated 32 total propositions with 9 acceptances, for a
different results" [behavioral inconsistency]; Bug 007: "Our
                                                                                        28.1% acceptance rate.
                                                                                                                                                    8
  Figure 3. (left) AIB dominance over AIA in contributions when fixing specific bugs. (right) Acceptance rate according to the bug input type and AIB contribution.




Type 2 inputs produced 37 propositions with 13 acceptances                              achieved exactly 25% acceptance rates. Configuration
or a 35.1% acceptance rate. Type 2 inputs demonstrated                                  defects achieved 33.3% acceptance but required arbitration.
superior efficiency, requiring 2.85 propositions per accepted                           Concurrency-related bugs (Concurrency, Regex Performance,
fix compared to 3.56 for Type 1 inputs, representing a 20%                              Race Condition) demonstrated high convergence rates (85-
improvement in resource utilization.                                                    90%) but modest acceptance rates ranging from 20% - 33.3%.

The AI systems exhibited markedly different response                                    Codebase complexity metrics showed no systematic
patterns across input types. For Type 1 inputs, AIA                                     relationship with debugging success. The number of files
contributed a mean of 22.5% of solutions while AIB                                      ranged from 4 to 7 across all bugs, while bug description
contributed 51.9%. Type 2 inputs showed even greater                                    length varied dramatically from 64 characters (Distributed
asymmetry, with AIA contributing 21.4% and AIB contributing                             Systems) to 7,006 characters (Race Condition), with no
58.6%. This produced AIB-to-AIA contribution ratios of 2.31:1                           apparent correlation to acceptance outcomes. Similarly,
for Type 1 inputs and 2.74:1 for Type 2 inputs. Convergence                             codebase size varied from 3,266 characters to 40,499
rates varied inversely, with Type 1 inputs achieving higher                             characters without systematic impact on fix acceptance
mean convergence (43.1%) compared to Type 2 inputs                                      rates.
(25.7%).
                                                                                        AI system convergence showed minimal relationship with
                       B
Across all bugs, AI demonstrated consistent dominance in                                ultimate fix acceptance (Figure 4. left), with high
solution generation (Figure 3). AIB outperformed AIA by an                              convergence (≥80%) occurring in 4 of 15 cases: Logic Error
average of 33.0%, with AIB exceeding AIA contributions in 14                            (85%), Concurrency (90%), Regex Performance (85%), and
of 15 cases (93.3%). Only bug 015 (Data Validation/Edge Case                            Race Condition (85%). These high-convergence cases
domain) showed AIA dominance, where AIA contributed 40%                                 averaged 34.1% acceptance compared to 31.7% for all other
versus AIB's 35%. The largest performance gaps occurred in                              cases, a difference of only 2.4 percentage points. However,
bugs 002 (Algorithmic Error, +60%) and 005 (Data                                        convergence did not serve as a perfect predictor of
Synchronization, +65%), while the smallest differences                                  arbitration necessity: both arbitrated cases (bugs 004:
appeared in bugs 001 (Authentication, +5%) and 004                                      Transaction Integrity and 008: Configuration) exhibited
(Transaction Integrity, +10%).                                                          convergence rates of exactly 10%, while several non-
                                                                                        Arbitrated bugs also had 10% convergence (e.g., 002, 005,
Total AI contribution (combined AIA and AIB percentages)
                                                                                        007, 012), and no bugs with convergence above 10%
averaged 77.0% across all bugs, with the arbitrator
                                                                                        required arbitration. The four high-convergence cases
contributing the remaining 23.0%. The distribution of total AI
                                                                                        involved technically well-defined domains with clear
contribution varied substantially, ranging from 40% in bugs
                                                                                        behavioral specifications, with two of these four cases
004 and 008 to 95% in bugs 005, 009, 010, and 011,
                                                                                        representing concurrency-related bugs (bugs 009 and 011),
indicating significant variation in the complexity of arbitrator
                                                                                        indicating particular AI system alignment on timing-
oversight required across different bug types.
                                                                                        dependent fault patterns. In arbitrated cases, the arbitrator
In contrast, six domains showed consistently modest                                     AI contributed 50% of the final solutions, representing
performance. Authentication, Transaction Integrity, Data                                substantial intervention.
Synchronization, Wrong Cache and Calculations, Scheduling
and Parsing, and Data Validation/Edge Case domains all

                                                                                                                                                                      9
Table 4. General table of studied bugs.

  Bug                   Domain                 Propositions       Acceptance Rate (%)      Codebase Files        AIA (%)         AIB (%)         Arbitrator (%)
   1      Authentication                            4.0                    25.0                   4               25.0            30.0                 5.0
   2      Algorithmic Error                         2.0                    50.0                   4               15.0            75.0                 0.0
   3      Logic Error                               2.0                    50.0                   4               25.0            65.0                10.0
   4      Transaction Integrity                     4.0                    25.0                   4               15.0            25.0                50.0
   5      Data Synchronization                      4.0                    25.0                   5               15.0            80.0                 5.0
   6      Null Reference                            5.0                    20.0                   4               25.0            60.0                 0.0
   7      Distributed Systems                       9.0                    55.6                   6                5.0            60.0                25.0
   8      Configuration                             3.0                    33.3                   5               15.0            25.0                50.0
   9      Concurrency                               3.0                    33.3                   7               25.0            70.0                 5.0
   10     Regex Performance                         3.0                    33.3                   5               25.0            70.0                 5.0
   11     Race Condition                            5.0                    20.0                   5               25.0            70.0                 5.0
   12     Server Imbalance                          5.0                    40.0                   4               25.0            65.0                 0.0
   13     Wrong Cache and Calculations              8.0                    25.0                   5               25.0            35.0                10.0
   14     Scheduling and Parsing                    8.0                    25.0                   5               25.0            60.0                 0.0
   15     Data Validation/Edge Case                 4.0                    25.0                   6               40.0            35.0                 5.0
   -      Average                                   4.6                    32.4                  4.9              22.0            55.3                11.7




Figure 4. (left) Acceptance rate of bug fixes, convergence between AIA and AIB, and arbitration flag at 80%. (right) Distribution of acceptance rate according to bug
input type.

The relationship between proposal quantity and acceptance                               (Distributed Systems) exemplifies this pattern, requiring 9
success revealed complex efficiency patterns strongly                                   propositions yet achieving the highest acceptance rate
influenced by input format as seen in Figure 4 (right). Type 1                          (55.6%), a pattern consistent with architectural issues
(detailed) inputs clustered consistently in moderate                                    benefiting from multiple targeted interventions, though this
efficiency ranges (3–5 propositions, 20–40% acceptance),                                dataset does not establish causality. Excluding this
suggesting that detailed diagnostic information provides                                architectural outlier, high-volume bugs (8 propositions, bugs
sufficient context to avoid major confusion while potentially                           013 and 014) achieved only 25% acceptance rates.
introducing noise that prevents highly efficient solutions. By
                                                                                        The distribution of maximum contributors revealed clear
contrast, Type 2 (minimal) inputs exhibited extreme
                                                                                        system specialization patterns: AIB served as the maximum
outcomes (25–55.6% acceptance), either achieving the
                                                                                        contributor in 7 cases, convergent agreement occurred in 5
highest efficiency (2 propositions, 50% acceptance for bugs
                                                                                        cases, the arbitrator ("Final") dominated in 2 cases, and AIA
002: Algorithmic Error and 003: Logic Error) or requiring
                                                                                        led in only 1 case. This distribution reinforces the systematic
extensive exploration (8–9 propositions). Table 4 shows all
                                                                                        advantage of AIB across diverse fault types, confirms the
the data summarized.
                                                                                        rarity of scenarios where AIA-centric approaches prove
This "input minimalism paradox" demonstrates that sparse                                superior, and demonstrates substantial AI system alignment
problem descriptions either provide sufficient clarity for                              on technically well-defined problems.
rapid AI convergence or prove so ambiguous that multiple
solution iterations become necessary (Table 5). Bug 007

                                                                                                                                                                  10
Table 5. Debugging efficiency patterns by proposal volume and input format.

         Propositions                   Bugs (Input Type)                 Mean Acceptance                Input Type Pattern                      Insight
              2                            2(T2), 3(T2)                       50.0%                          All Type 2                    Highest efficiency
              3                        8(T1), 9(T1), 10(T1)                   33.3%                          All Type 1                   Consistent moderate
              4                     1(T1), 4(T1), 5(T2), 15(T2)               25.0%                       Mixed (2T1, 2T2)                  Lower efficiency
              5                       6(T1), 11(T1), 12(T1)                   26.7%                          All Type 1                   Mixed Type 1 results
              8                           13(T2), 14(T2)                      25.0%                          All Type 2                      Low efficiency


Table 6 - Risk categories for AI-generated code fixes with operational impacts and arbitration decision patterns.

 Risk Category                 Representative Examples from Dataset              Documented Operational Risk                  Arbitration Decision Pattern
                               AIA’s fatal syntax error with threading.Lock()    Prevents code execution entirely,
                                                                                                                              Rejected as “fatal syntax error that
 Syntax Errors and             without storing the instance (Bug 009); AIA’s     leading to immediate deployment
                                                                                                                              would prevent code from running.”
 Technical Impossibilities     invalid threading syntax causing compilation      failures and compilation errors in
                                                                                                                              Basic technical correctness is required
                               errors (Bug 009)                                  production

                               AIB’s enhanced error handling where the
                               original code already had proper bounds           Wastes development resources,                Rejected as “addresses theoretical
 Fixing Nonexistent            checking (Bug 002); AIA’s queue clearing fix      introduces unnecessary code                  problem not evidenced” or “safe
 Problems                      when queue.clear() already works (Bug 007);       complexity, and obscures real issues by      function already exists and doesn’t
                               AIB’s UUID solution as overly complex for a       adding redundant layers                      need modification”
                               nonexistent collision problem (Bug 004)

                               AIB’s conversion to Decimal arithmetic
                               without evidence of floating-point errors         Increases maintenance burden,                Rejected as “unnecessary complexity,”
 Over-engineering and          (Bug 002); AIB’s arbitrary 70/30 weighting        complicates testing, and may reduce          “speculative addition not required,” or
 Unnecessary Complexity        with no proven benefit (Bug 012); multi-step      performance. Complex solutions are           “overengineered when a simple fix
                               approaches where the defect required a one-       harder to debug and validate                 suffices”
                               line fix (Bug 010)

                               AIB’s hardcoding fix that removed
                                                                                 Causes immediate service degradation,        Rejected as “breaks existing error
                               environment-aware behavior (Bug 008); AIA’s
 Breaking Existing                                                               resource exhaustion, or loss of critical     handling,” “would prevent legitimate
                               resource tracking leading to leaks (Bug 011);
 Functionality                                                                   system capabilities; disrupts                completions,” or “destroys
                               AIA’s fix that could overload smaller servers
                                                                                 established operational patterns             functionality”
                               (Bug 012)

                               AIA’s duplicate checking fix when identical
                                                                                 Consumes development effort without          Rejected as “misreading existing code,”
                               code already existed (Bug 004); AIA’s
 Misunderstanding                                                                resolving defects, reflects poor             “demonstrates misunderstanding of the
                               consolidation that misidentified the root
 Existing Code                                                                   comprehension of system logic, and           problem,” or “failed to recognize
                               cause (Bug 005); AIA’s invalid import change
                                                                                 risks introducing further errors             existing implementations”
                               (Bug 008)

                               AIA’s fixes targeting the reporting module
                               even though it was functioning correctly (Bug     Leaves actual defects unresolved,            Rejected as “addresses symptoms, not
 Addressing Symptoms           005); AIA’s rounding adjustment addressing        allowing recurrence under different          root cause,” “defensive programming
 Rather Than Root Cause        symptoms instead of cause (Bug 013); AIB’s        conditions; increases code complexity        without addressing cause,” or targeting
                               defensive programming not tied to root            while masking core issues                    “functioning modules”
                               cause (Bug 005)

                               AIA’s insertion of print statements into
                                                                                 Reduces production efficiency, violates      Rejected as “not a valid fix in
 Production Code Quality       production code (Bug 007); AIB’s runtime
                                                                                 coding standards, and risks information      production” or “creates performance
 Violations                    import that degrades performance and
                                                                                 leakage through improper logging             penalty”
                               violates clean code standards (Bug 012)

                               Security measures without concrete
                                                                                 Expands scope beyond defect                  Rejected as “speculative enhancement
 Speculative                   implementation (Bug 001); documentation-
                                                                                 resolution, delays critical fixes, and       not required,” “not necessary for
 Enhancements Beyond           focused changes instead of functional fixes
                                                                                 introduces untested or non-essential         immediate bug resolution,” or “beyond
 Scope                         (Bug 003); AIB
                                                                                 changes                                      scope”
                               ’s unnecessary code removal (Bug 010)




DISCUSSION ON RISK-BEARING SUGGESTIONS AND                                             modifications that would introduce substantial operational
                                                                                       risk in production hot-fix scenarios. Final arbitration
FILTRATION OUTCOMES
                                                                                       systematically pruned these broader edits as out-of-scope,
The consolidations consistently surfaced extensive                                     preserving only minimal causal interventions. Table 6
"improvement" suggestions that extended far beyond                                     summarizes actual categories observed across fault domains,
minimal defect resolution. Individual AI systems                                       documenting where such suggestions originated, their
demonstrated systematic bias toward comprehensive                                      documented operational risks, and arbitration disposition
refactoring, security hardening, and architectural                                     patterns.
                                                                                                                                                                    11
LIMITATIONS AND FUTURE WORK                                      CONCLUSION
Several architectural extensions could enhance SLEAN's           We presented SLEAN, a practical framework for coordinating
capabilities. Sequential processing through phases prevents      multiple LLM providers in automated bug investigation that
parallelization that could reduce execution time, particularly   achieves the analytical diversity of multi-agent systems
for independent analysis where providers could operate           without their infrastructure complexity. By treating each
concurrently. Static configuration requires provider             provider as an interchangeable analytical module within a
assignment at initialization, preventing dynamic adaptation      deterministic three-phase workflow, the framework
based on availability or performance characteristics. File       preserves independence, supports reproducible audits, and
boundary chunking may struggle with extremely large              filters harmful proposals before code integration.
individual files that exceed token limits even after
                                                                 Evaluation demonstrated that the framework effectively
partitioning.
                                                                 identifies and rejects scope-expanding modifications while
The framework's modular architecture and clear abstraction       preserving minimal causal interventions. The systematic
boundaries explicitly support future extensions. The provider    arbitration process proved essential in preventing potentially
interface can accommodate new providers with minimal             harmful AI suggestions from reaching production code,
modification, while the prompt template system enables           addressing a critical safety concern in AI-assisted
domain-specific customization. The workflow orchestration        development.
pattern supports extension with additional phases or
                                                                 The approach generalizes beyond debugging to any domain
modified coordination protocols without affecting core
                                                                 requiring synthesis from heterogeneous LLM analyses. The
functionality.
                                                                 provider-agnostic architecture and file-driven design make it
The framework's modular design supports investigation of         readily applicable to security auditing, code review,
multilayered review architectures with expanded arbitration      document verification, and risk assessment. By combining
hierarchies. Future studies should examine n-layer               operational simplicity, deterministic coordination, and
workflows incorporating diverse arbitrators, heterogeneous       explicit traceability, SLEAN offers a viable production-ready
provider combinations, and varied prompt engineering             alternative to complex multi-agent systems where reliable,
strategies. Information accumulation across layers where         explainable, and auditable analytical consensus is required.
each phase preserves and augments prior artifacts
represents a promising direction for comprehensive
analytical depth.                                                CONFLICT OF INTEREST
Additional enhancements include parallel execution for           No conflict of interest.
independent analysis phases, adaptive provider selection
based on bug characteristics or performance history,
feedback integration mechanisms learning from successful         EXTRA MATERIAL
repair sessions, and hierarchical analysis approaches for very
large codebases decomposing complex systems into                 https://github.com/cyaura-open/SLEAN
manageable components while maintaining overall
coherence.                                                       ACKNOWLEDGEMENTS
Another limitation of our experimental design is that the        Dr. Yong Je Kwon and Dr. Anany Dwivedi for reviewing this
arbitrator shares the same underlying architecture as AIA.       work.
This may introduce bias during arbitration. Future work
should employ an independent third provider for arbitration
to ensure complete architectural diversity.                      REFERENCES
Chunking is currently implemented only in Phase 1. Tested        1.      Eladawy, H., Le Goues, C. & Brun, Y. Automated Program Repair,
codebases (3,266 to 40,499 characters) passed all phases                 What Is It Good For? Not Absolutely Nothing! in Proceedings of
                                                                         the IEEE/ACM 46th International Conference on Software
without token violations, but larger repositories may require            Engineering 1–13 (ACM, New York, NY, USA, 2024).
multi-phase chunking strategies. Future work will evaluate               doi:10.1145/3597503.3639095.
SLEAN on enterprise-scale codebases, implement parallel
                                                                 2.      Zhang, Q., Fang, C., Ma, Y., Sun, W. & Chen, Z. A Survey of Learning-
execution for independent analysis phases, and explore                   based Automated Program Repair. ACM Transactions on Software
dynamic provider selection based on performance                          Engineering and Methodology 33, 1–69 (2024).
characteristics.
                                                                 3.      Xia, C. S., Wei, Y. & Zhang, L. Automated Program Repair in the Era
                                                                         of Large Pre-trained Language Models. in 2023 IEEE/ACM 45th
                                                                         International Conference on Software Engineering (ICSE) 1482–
                                                                         1494 (2023). doi:10.1109/ICSE48619.2023.00129.


                                                                                                                                          12
4.    Anany Dwivedi et al. Leveraging Large Language Models for              19.   Li, G., Al Kader Hammoud, H. A., Itani, H., Khizbullin, D. & Ghanem,
      Automated Feature Extraction and Model Training in EMG Based                 B. CAMEL: communicative agents for ‘mind’ exploration of large
      Motion Decoding. in ”, IEEE Engineering in Medicine and Biology              language model society. in Proceedings of the 37th International
      Society (EMBC) (Copenhagen, 2025).                                           Conference on Neural Information Processing Systems (Curran
                                                                                   Associates Inc., Red Hook, NY, USA, 2023).
5.    Chen, J., Saha, S. & Bansal, M. ReConcile: Round-Table Conference
      Improves Reasoning via Consensus among Diverse LLMs. in                20.   Epperson, W. et al. Interactive Debugging and Steering of Multi-
      Proceedings of the 62nd Annual Meeting of the Association for                Agent AI Systems. in Proceedings of the 2025 CHI Conference on
      Computational Linguistics (Volume 1: Long Papers) (eds. Ku, L.-W.,           Human Factors in Computing Systems 1–15 (ACM, New York, NY,
      Martins, A. & Srikumar, V.) 7066–7085 (Association for                       USA, 2025). doi:10.1145/3706598.3713581.
      Computational Linguistics,         Bangkok,    Thailand,   2024).
      doi:10.18653/v1/2024.acl-long.381.                                     21.   Yin, X. et al. ThinkRepair: Self-Directed Automated Program
                                                                                   Repair. in Proceedings of the 33rd ACM SIGSOFT International
6.    Perry, N., Srivastava, M., Kumar, D. & Boneh, D. Do Users Write              Symposium on Software Testing and Analysis 1274–1286
      More Insecure Code with AI Assistants? in Proceedings of the 2023            (Association for Computing Machinery, New York, NY, USA, 2024).
      ACM SIGSAC Conference on Computer and Communications                         doi:10.1145/3650212.3680359.
      Security 2785–2799 (ACM, New York, NY, USA, 2023).
      doi:10.1145/3576915.3623157.                                           22.   Mascardi, V., Weyns, D. & Ricci, A. Engineering Multi-Agent
                                                                                   Systems. ACM SIGSOFT Software Engineering Notes 44, 18–28
7.    Li, X., Wang, S., Zeng, S., Wu, Y. & Yang, Y. A survey on LLM-based          (2019).
      multi-agent systems: workflow, infrastructure, and challenges.
      Vicinagearth 1, 9 (2024).                                              23.   Guo, T. et al. Large Language Model Based Multi-agents: A Survey
                                                                                   of Progress and Challenges. in Proceedings of the Thirty-Third
8.    Inc., crewAI. CrewAI: Open-Source Multi-Agent Framework.                     International Joint Conference on Artificial Intelligence, IJCAI-24
      Preprint at https://github.com/crewAIInc/crewAI (2025).                      (ed. Larson, K.) 8048–8057 (International Joint Conferences on
                                                                                   Artificial         Intelligence      Organization,           2024).
9.    OpenAI. Swarm: Lightweight Agent Coordination and Handoffs.                  doi:10.24963/ijcai.2024/890.
      Preprint at https://github.com/openai/swarm (2024).
                                                                             24.   Dietterich, T. G. Ensemble Methods in Machine Learning.
10.   Wang, G. et al. Voyager: An Open-Ended Embodied Agent with                   http://www.cs.orst.edu/˜tgd.
      Large Language Models. https://arxiv.org/abs/2305.16291
      (2023).                                                                25.   Hansen, L. K. & Salamon, P. Neural network ensembles. IEEE Trans
                                                                                   Pattern Anal Mach Intell 12, 993–1001 (1990).
11.   Chen, G. et al. AutoAgents: A Framework for Automatic Agent
      Generation. in Proceedings of the Thirty-Third International Joint     26.   Breiman, L. Bagging Predictors. vol. 24 (1996).
      Conference on Artificial Intelligence, IJCAI-24 (ed. Larson, K.) 22–
      30 (International Joint Conferences on Artificial Intelligence         27.   Wolpert, D. H. Stacked generalization. Neural Networks 5, 241–
      Organization, 2024). doi:10.24963/ijcai.2024/3.                              259 (1992).

12.   Lamb, C. & Zacchiroli, S. Reproducible Builds: Increasing the          28.   Breiman, L. Random Forests. vol. 45 (2001).
      Integrity of Software Supply Chains. IEEE Softw 39, 62–70 (2022).
                                                                             29.   Yang, A. Z. H., Le Goues, C., Martins, R. & Hellendoorn, V. Large
13.   Sculley, D. et al. Hidden Technical Debt in Machine Learning                 Language Models for Test-Free Fault Localization. in Proceedings
      Systems. in Advances in Neural Information Processing Systems 28             of the IEEE/ACM 46th International Conference on Software
      (NeurIPS 2015) 2503–2511 (Curran Associates, Inc., Montreal,                 Engineering (Association for Computing Machinery, New York, NY,
      Canada, 2015).                                                               USA, 2024). doi:10.1145/3597503.3623342.

14.   Steidl, M., Felderer, M. & Ramler, R. The pipeline for the             30.   Xia, C. S. & Zhang, L. Automated Program Repair via Conversation:
      continuous development of artificial intelligence models—Current             Fixing 162 out of 337 Bugs for 0.42 Each using ChatGPT. in
      state of research and practice. Journal of Systems and Software              Proceedings of the 33rd ACM SIGSOFT International Symposium
      199, 111615 (2023).                                                          on Software Testing and Analysis 819–831 (Association for
                                                                                   Computing Machinery, New York, NY, USA, 2024).
15.   Wu, Q. et al. AutoGen: Enabling Next-Gen LLM Applications via                doi:10.1145/3650212.3680323.
      Multi-Agent Conversation. https://arxiv.org/abs/2308.08155
      (2023).                                                                31.   Ye, H., Martinez, M., Luo, X., Zhang, T. & Monperrus, M. SelfAPR:
                                                                                   Self-supervised Program Repair with Test Execution Diagnostics. in
16.   Besta, M. et al. Graph of thoughts: solving elaborate problems               Proceedings of the 37th IEEE/ACM International Conference on
      with large language models. in Proceedings of the Thirty-Eighth              Automated Software Engineering (Association for Computing
      AAAI Conference on Artificial Intelligence and Thirty-Sixth                  Machinery,        New        York,       NY,    USA,       2023).
      Conference on Innovative Applications of Artificial Intelligence and         doi:10.1145/3551349.3556926.
      Fourteenth Symposium on Educational Advances in Artificial
      Intelligence (AAAI Press, 2024). doi:10.1609/aaai.v38i16.29720.        32.   Joshi, H. et al. Repair Is Nearly Generation: Multilingual Program
                                                                                   Repair         with         LLMs.      www.aaai.org          (2023)
17.   LangChain. LangGraph: A low-level orchestration framework for                doi:https://doi.org/10.1609/aaai.v37i4.25642.
      stateful agents. Preprint at (2024).
                                                                             33.   Ribeiro, M. T., Singh, S. & Guestrin, C. ‘Why should i trust you?’
18.   Qian, C. et al. ChatDev: Communicative Agents for Software                   Explaining the predictions of any classifier. in Proceedings of the
      Development. in Proceedings of the 62nd Annual Meeting of the                ACM SIGKDD International Conference on Knowledge Discovery
      Association for Computational Linguistics (Volume 1: Long Papers)            and Data Mining vols 13-17-August-2016 1135–1144 (Association
      (eds. Ku, L.-W., Martins, A. & Srikumar, V.) 15174–15186                     for Computing Machinery, 2016).
      (Association for Computational Linguistics, Bangkok, Thailand,
      2024). doi:10.18653/v1/2024.acl-long.810.                              34.   Ohmann, P. An Assessment of Oral Exams in Introductory CS. in
                                                                                   Proceedings of the 50th ACM Technical Symposium on Computer
                                                                                   Science Education 613–619 (Association for Computing

                                                                                                                                                   13
      Machinery,     New       York,           NY,      USA,        2019).          Transparency 220–229 (ACM, New York, NY, USA, 2019).
      doi:10.1145/3287324.3287489.                                                  doi:10.1145/3287560.3287596.

35.   Mitchell, M. et al. Model Cards for Model Reporting. in                 43.   Hutchinson, B. et al. Towards Accountability for Machine Learning
      Proceedings of the Conference on Fairness, Accountability, and                Datasets: Practices from Software Engineering and Infrastructure.
      Transparency 220–229 (ACM, New York, NY, USA, 2019).                          in Proceedings of the 2021 ACM Conference on Fairness,
      doi:10.1145/3287560.3287596.                                                  Accountability, and Transparency 560–575 (ACM, New York, NY,
                                                                                    USA, 2021). doi:10.1145/3442188.3445918.
36.   Hong, S. et al. MetaGPT: Meta Programming for A Multi-Agent
      Collaborative    Framework.   http://arxiv.org/abs/2308.00352           44.   Stodden, V. & Miguez, S. Best Practices for Computational Science:
      (2024).                                                                       Software Infrastructure and Environments for Reproducible and
                                                                                    Extensible Research. J Open Res Softw 2, (2014).
37.   Ahn, D. H. et al. Overcoming extreme-scale reproducibility
      challenges through a unified, targeted, and multilevel toolset. in      45.   Mascardi, V. et al. Engineering Multi-Agent Systems. ACM SIGSOFT
      Proceedings of the 1st International Workshop on Software                     Software Engineering Notes 44, 18–28 (2019).
      Engineering for High Performance Computing in Computational
      Science and Engineering 41–44 (ACM, New York, NY, USA, 2013).           46.   Benedetti, G. et al. An Empirical Study on Reproducible Packaging
      doi:10.1145/2532352.2532357.                                                  in Open-Source Ecosystems. in 2025 IEEE/ACM 47th International
                                                                                    Conference on Software Engineering (ICSE) 1052–1063 (IEEE,
38.   Bouthillier, X., Laurent, C. & Vincent, P. Unreproducible Research            2025). doi:10.1109/ICSE55347.2025.00136.
      is Reproducible. in Proceedings of the 36th International
      Conference on Machine Learning (eds. Chaudhuri, K. &                    47.   Spinellis, D. Version control systems. IEEE Softw 22, 108–109
      Salakhutdinov, R.) vol. 97 725–734 (PMLR, 2019).                              (2005).

39.   Malka, J., Zacchiroli, S. & Zimmermann, T. Reproducibility of Build     48.   Easterbrook, S., Singer, J., Storey, M.-A. & Damian, D. Selecting
      Environments through Space and Time. in Proceedings of the 2024               Empirical Methods for Software Engineering Research. in Guide to
      ACM/IEEE 44th International Conference on Software Engineering:               Advanced Empirical Software Engineering 285–311 (Springer
      New Ideas and Emerging Results 97–101 (ACM, New York, NY,                     London, London, 2008). doi:10.1007/978-1-84800-044-5_11.
      USA, 2024). doi:10.1145/3639476.3639767.
                                                                              49.   Eick, S. G., Graves, T. L., Karr, A. F., Marron, J. S. & Mockus, A. Does
40.   Neisse, R., Steri, G. & Nai-Fovino, I. A Blockchain-based Approach            code decay? Assessing the evidence from change management
      for Data Accountability and Provenance Tracking. in Proceedings               data. IEEE Transactions on Software Engineering 27, 1–12 (2001).
      of the 12th International Conference on Availability, Reliability and
                                                                              50.   Vogel-Heuser, B., Fay, A., Schaefer, I. & Tichy, M. Evolution of
      Security 1–10 (ACM, New York, NY, USA, 2017).
                                                                                    software in automated production systems: Challenges and
      doi:10.1145/3098954.3098958.
                                                                                    research directions. Journal of Systems and Software 110, 54–84
41.   Kohan Marzagão, D., Huynh, T. D., Helal, A., Baccas, S. & Moreau,             (2015).
      L. Provenance Graph Kernel. IEEE Trans Knowl Data Eng 37, 3653–
                                                                              51.   Alami, A., Jensen, V. V. & Ernst, N. A. Accountability in Code
      3668 (2025).
                                                                                    Review: The Role of Intrinsic Drivers and the Impact of LLMs. ACM
42.   Mitchell, M. et al. Model Cards for Model Reporting. in                       Transactions on Software Engineering and Methodology
      Proceedings of the Conference on Fairness, Accountability, and                https://doi.org/10.1145/3721127 (2025) doi:10.1145/3721127.




                                                                                                                                                        14
