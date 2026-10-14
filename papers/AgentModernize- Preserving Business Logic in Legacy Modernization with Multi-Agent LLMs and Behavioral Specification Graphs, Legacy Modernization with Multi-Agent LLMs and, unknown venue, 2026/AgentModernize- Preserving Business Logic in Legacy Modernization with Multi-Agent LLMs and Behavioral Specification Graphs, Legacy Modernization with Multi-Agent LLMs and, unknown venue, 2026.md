                                          AgentModernize: Preserving Business Logic in
                                        Legacy Modernization with Multi-Agent LLMs and
                                                Behavioral Specification Graphs
                                                                  Sheikh Nazib Ahmed                                            Marnim Galib
                                                              University of Texas at Arlington                         University of Texas at Arlington
                                                                   Arlington, TX, USA                                       Arlington, TX, USA
                                                                  sxa5256@mavs.uta.edu                                     marnim.galib@uta.edu




                                           Abstract—Legacy modernization breaks business logic more           to integrate with modern platforms, and increasingly fragile as
                                        often than most teams expect. Most tools and LLM-based                the engineers who wrote them retire [2].
                                        approaches treat modernization as syntax translation: convert
                                        COBOL to Java, swap PL/SQL for Python, ship it. Implicit                 Modernization is the standard response, but most modern-
                                        rules, edge-case handling, and cross-module constraints that keep     ization efforts destroy the thing they should preserve: behav-
arXiv:2605.17535v2 [cs.SE] 4 Aug 2026




                                        production systems running are lost, and nobody notices until         ioral semantics. Business rules in legacy systems are rarely
                                        something fails in production.                                        documented; they live in control flow patterns, conditional
                                           We present AgentModernize, a multi-agent framework that            branches, exception handlers, and configuration files [3]. A
                                        treats modernization as a behavioral preservation problem. Four
                                                                                                              line-by-line COBOL-to-Java translation can compile and run
                                        agents handle extraction, specification, code generation, and val-
                                        idation. The key intermediate artifact, a Behavioral Specification    yet silently break edge-case handling, alter validation logic,
                                        Graph (BSG), forces extracted business logic to be explicit and       or drop constraints that were never written down [4]. We saw
                                        inspectable before any code is generated.                             this firsthand in a telecom provisioning workflow where a
                                           We evaluated on LegacyModernize-8, eight synthetic scenarios       syntactically correct translation passed compilation but silently
                                        spanning telecom and banking, under a fair protocol where each        dropped a suspended-account exemption that had been in
                                        method’s tests are generated from its own API surface (3 trials,
                                        temperature 0.0). With GPT-4o-mini, AgentModernize with feed-         production for fifteen years. The system looked modern and
                                        back achieves 23.0% mean BER (non-zero on 5/8 scenarios, up to        behaved differently.
                                        53.3%), while AgentModernize without feedback reaches 23.8%.             Large Language Models can parse legacy code, reason about
                                        SP-LLM scores 12.4% (non-zero on 2/8) and CoT-LLM 4.5%                intent, and generate modern equivalents [5], [6], but prompting
                                        (2/8). No single method dominates all scenarios. The feedback
                                        loop is decisive for scenarios requiring iterative correction (S4,    one to “convert this legacy code to a modern API” is brittle.
                                        S6, S7) but can regress code in others (S2, S8). The BSG              Context windows cannot hold an entire legacy codebase; a
                                        captures 92.3% of gold-standard rules with 90.2% precision; the       single generation pass provides no way to verify behavior was
                                        bottleneck is code generation, not extraction. A cross-model study    preserved; and a monolithic prompt conflates understanding,
                                        (GPT-4o, GPT-5.3-codex) reveals the pipeline’s benefit is inversely   specification, transformation, and validation, tasks that benefit
                                        correlated with model capability: stronger models achieve higher
                                        BER with single-prompt methods than with the pipeline. For            from separation [7].
                                        regulated industries, the pipeline’s traceable artifacts (business       Our approach, AgentModernize, decomposes legacy mod-
                                        rule inventory, BSG, equivalence reports) provide an audit trail      ernization into four agent-handled phases:
                                        that no single-prompt approach can match.
                                           Index Terms—legacy modernization, multi-agent systems, large         1) A Legacy Analyzer that extracts both explicit and
                                        language models, business logic preservation, behavioral equiva-           implicit business rules, along with control flows and
                                        lence, software engineering                                                operational constraints, from legacy artifacts.
                                                                                                                2) A Specification Generator that encodes the extracted
                                                               I. I NTRODUCTION                                    logic into Behavioral Specification Graphs (BSGs), a
                                                                                                                   structured intermediate representation with precondi-
                                           Telecommunications carriers, financial institutions, and                tions, postconditions, and invariants.
                                        healthcare providers run their core operations on systems built         3) A Modernization Transformer that generates modern
                                        twenty or thirty years ago. COBOL batch jobs process billing.              service implementations from the BSG, preserving be-
                                        PL/SQL procedures enforce contract logic. Shell scripts or-                havioral contracts.
                                        chestrate provisioning workflows. These systems work, and               4) An Equivalence Validator that checks the generated
                                        the business rules encoded in them have been refined through               code against the BSG through automated test generation
                                        years of production experience, bug fixes, and regulatory                  and differential trace analysis, feeding failures back for
                                        adaptation [1]. They are also expensive to maintain, difficult             iterative correction.
   The BSG acts as a “glass box” between legacy under-                 Design/Workflow Recovery and Code Summarization.
standing and modern generation: extracted business logic is         Adjacent literatures on program comprehension have long
explicit and inspectable before any code is written. When the       addressed pieces of the modernization problem under different
Validator detects a behavioral divergence, it triggers a targeted   names. Zou and Hung [26] extract workflow structure from e-
correction loop rather than a full re-generation. As our ablation   commerce applications; the recent survey by Zhang et al. [25]
shows (Table VI), the multi-agent decomposition consistently        covers automatic source code summarization techniques that
outperforms single-prompt baselines, and the feedback loop          produce natural-language descriptions of code behavior. Our
adds value on scenarios with localized, correctable errors.         Legacy Analyzer is closest in spirit to workflow recovery, and
   We evaluate on LegacyModernize-8, a benchmark of eight           the BSG plays a role analogous to a structured code-level
synthetic scenarios covering telecom and banking modern-            summary. What separates AgentModernize from this line of
ization, measuring behavioral equivalence rate and business         work is the closed loop with a code-generation and verification
rule preservation against single-prompt and chain-of-thought        stage: recovery/summarization systems traditionally stop at the
LLM baselines. With GPT-4o-mini, AgentModernize achieves            human-readable artifact, whereas the BSG must be executable-
23.0% mean BER with feedback and 23.8% without, compared            enough for downstream synthesis and differential testing.
to 12.4% for SP-LLM and 4.5% for CoT-LLM. No method                    Comparison to Established IRs. The Knowledge Discov-
dominates all scenarios; the feedback loop helps on some and        ery Metamodel (KDM) [22] and Architecture-Driven Mod-
regresses others, a nuance prior single-pass evaluations would      ernization (ADM) standards from OMG provide formal repre-
miss.                                                               sentations of legacy system semantics. Behavioral interface
                                                                    specification languages such as JML [20] and Eiffel [21]
A. Contributions
                                                                    encode pre/post/invariants per method. BSG draws from both
  Our contributions are:                                            but differs in three respects: it is designed for LLM-mediated
  • A multi-agent framework that decomposes legacy mod-             extraction with per-rule confidence scoring and source trace-
    ernization into extraction, specification, transformation,      ability; it distinguishes explicit from implicit rules (a cat-
    and validation, with a feedback loop for iterative correc-      egorization absent from KDM/JML); and it serves as an
    tion.                                                           inspectable trust boundary between LLM extraction and LLM
  • Behavioral Specification Graphs, an intermediate repre-         generation, which had no analog in pre-LLM workflows. BSG
    sentation that captures business rules, pre/post-conditions,    adapts the graph-IR-with-contracts paradigm to LLM-driven
    data constraints, and control flow dependencies in an           modernization rather than introducing a new representation.
    inspectable, verifiable form.
  • An automated equivalence checking approach based                B. LLMs for Software Engineering
    on test oracle generation from BSG specifications, com-            LLMs have shown strong results in code generation [5], bug
    bined with differential trace analysis.                         detection [10], code review [11], and program repair [12]. The
  • An empirical evaluation on an eight-scenario benchmark          work most relevant to ours is Pan et al. [13], who found that
    (including a held-out banking scenario) with ablation           GPT-4 produces syntactically correct cross-language transla-
    and model comparison, showing that the multi-agent              tions but introduces semantic bugs in complex control flows.
    pipeline with feedback achieves the highest BER on              This is consistent with our own experiments (Section V):
    scenarios requiring iterative correction, while revealing       single-prompt baselines compiled and ran but achieved low
    that feedback can regress code in other scenarios.              BER (12.4% SP-LLM, 4.5% CoT-LLM mean) compared to
                                                                    the multi-agent pipeline.
                     II. R ELATED W ORK
                                                                       The common thread in all of these studies is that they treat
A. Legacy System Modernization                                      modernization as a single-pass task. One model, one prompt,
   Early frameworks catalogued modernization strategies rang-       one output. No intermediate representation, no verification,
ing from wrapping to full re-engineering [1] and formalized         no feedback. For a self-contained utility function, that might
the process as iterative abstraction, transformation, and re-       work. For a 280-line COBOL provisioning workflow with
finement (the horseshoe model [3]). Model-driven approaches         thirteen interacting business rules and implicit logic buried in
like MoDisco [8] formalize legacy knowledge using KDM and           exception handlers, it does not. Our results in Table III confirm
ADM standards, but constructing the models requires manual          this empirically.
effort that often rivals the cost of the modernization itself.
   Industry tools (IBM Rational Asset Analyzer, Micro Focus         C. Multi-Agent LLM Systems
Enterprise Analyzer, COBOL-to-Java transpilers) handle syn-            MetaGPT [14] partitions software development across ar-
tactic translation competently [9], but “compile-and-run” is        chitect, engineer, and tester agents. ChatDev [15] models
not behavioral equivalence. None of these tools verify that the     an entire software company through multi-agent dialogue.
translated system behaves the same as the original, and none        AgentCoder [16] pairs a code generator with an adversarial test
publish behavioral equivalence metrics we could compare             generator. Self-Refine [23] and Reflexion [24] show that LLM
against. As Section V shows, even LLM-based approaches fail         agents can improve their own outputs through self-generated
to preserve behavior without an explicit feedback mechanism.        feedback, a principle our feedback loop shares.
   All of these target greenfield development. Building new                            Legacy Artifact Bundle
code from scratch is a different problem than modernizing
existing code with undocumented business rules; none extract
implicit logic from decades-old COBOL, represent it in a
verifiable form, or confirm that generated code preserves un-                        Agent 1: Legacy Analyzer
documented behavior. AgentModernize’s BSG is task-specific
to modernization (not applicable to code review or refactoring
                                                                                       Business Rule Inventory
in general), but it is not tied to any application domain: it
captures business rules, control/data flow, and constraints in a
form that applies equally to telecom, banking, healthcare, or                         Agent 2: Spec Generator
government legacy systems, as our S8 result begins to show.
                                                                                       Behavioral Spec Graph                            trust boundary
D. Behavioral Equivalence
    Formal program equivalence (bisimulation, trace equiv-
alence, observational equivalence) provides the theoretical                             Agent 3: Transformer
grounding for our verification approach [17]. Full formal
verification is intractable for most real-world systems. Prac-                           Modernized Service                  feedback
titioners rely on lighter alternatives: differential testing [18]
compares outputs across system versions; metamorphic test-
ing [19] checks whether known input transformations produce                              Agent 4: Validator
expected output transformations.
    Our Equivalence Validator combines both ideas but gen-                               Equivalence Report
erates test oracles from the BSG specification, not from the
legacy code directly. This avoids the circularity of testing a      Fig. 1. AgentModernize Pipeline Architecture. Solid arrows show the forward
translation against itself. We do not claim formal guarantees;      pipeline; the dashed red arrow shows the feedback loop from the Validator
                                                                    to the Transformer. The BSG (dotted box) acts as a trust boundary between
Section V shows the approach catches a class of behavioral          extraction and generation.
regressions that single-pass methods miss.

        III. T HE AGENT M ODERNIZE F RAMEWORK                         • S = Source code files (e.g., COBOL programs, PL/SQL
A. Overview                                                             procedures, shell scripts)
                                                                      • C = Configuration files (e.g., JCL, parameter files, cron
   The framework takes a bundle of legacy artifacts (source
                                                                        schedules)
code, configuration files, database schemas, and any available
                                                                      • D = Database schemas (e.g., DDL statements, copybook
documentation) and produces a modernized service implemen-
                                                                        layouts, data dictionaries)
tation with a report on how faithfully the original behavior was
                                                                      • N = Natural language documentation (optional; e.g.,
preserved. Four agents handle this in sequence, each reading
                                                                        runbooks, comments, requirement documents)
from and writing to a shared pipeline state. Fig. 1 shows the
architecture.
   The pipeline is not purely feed-forward: when the Equiv-         C. Agent 1: Legacy Analyzer
alence Validator (Agent 4) detects behavioral divergences, it          The Legacy Analyzer extracts both explicit business rules
feeds specific failure information back to the Modernization        (stated directly in conditionals, guards, or comments) and im-
Transformer (Agent 3) for targeted correction. This loop runs       plicit rules (inferable from code patterns, default values, excep-
up to three iterations.                                             tion handlers, or cross-module dependencies). Each extracted
   LLM Interaction Model. All four agents use zero-shot             rule is tagged with its category (explicit or implicit)
prompting with off-the-shelf models via their public APIs. We       and a confidence score in the Business Rule Inventory. The
do not fine-tune, do not use RAG, and do not include few-shot       agent operates in three sub-phases:
in-context examples. Each agent’s prompt is a fixed instruction        Phase 1a — Structural Parsing: The agent identifies
template plus the current pipeline state. The scenarios in          program entry points, module boundaries, data flows, and ex-
Section IV-B were used during development to iterate on             ternal dependencies. For procedural legacy code, this involves
prompt templates, but no model weights are updated and              identifying PERFORM/CALL hierarchies, file I/O operations,
no scenario-specific examples are embedded in prompts at            and database interactions.
inference time.                                                        Phase 1b — Business Rule Extraction: The agent identi-
                                                                    fies conditional logic, validation rules, computation formulas,
B. Legacy Artifact Bundle                                           state transitions, and exception handling patterns. Each ex-
  The input to the framework is a Legacy Artifact Bundle            tracted rule is annotated with: a natural language description,
L = {S, C, D, N } where:                                            the source location (file, line range), input variables and output
effects, and a confidence score (high/medium/low) based on
                                                                    {
extraction clarity.                                                     "operation": "ValidateDisconnectOrder",
   Phase 1c — Constraint Discovery: The agent identifies                "source_rule": "BR-004",
implicit constraints including data type restrictions, value            "source_location": "ORDER_VALIDATION.cob:118-142",
                                                                        "preconditions": [
ranges, referential integrity rules, temporal ordering require-           "account_status in [’ACTIVE’, ’SUSPENDED’]",
ments, and business-specific invariants (e.g., “order total must          "order_type == ’DISCONNECT’"
equal sum of line items”).                                              ],
                                                                        "postconditions": [
   Output: A Business Rule Inventory (BRI), a JSON docu-                  "suspended accounts proceed for disconnect
ment containing all extracted rules, constraints, and metadata.               orders",
                                                                          "non-disconnect orders rejected for suspended"
                                                                        ],
D. Agent 2: Specification Generator                                     "invariants": ["order_total == sum(line_items)"],
                                                                        "confidence": "high"
  The Specification Generator transforms the Business Rule          }
Inventory into a Behavioral Specification Graph (BSG), the
core intermediate representation of AgentModernize.                         Listing 1. BSG Node — S1 Disconnect Order Validation
  Definition 1 (Behavioral Specification Graph). A BSG is              This node captures an implicit rule (suspended accounts are
a directed acyclic graph G = (V, E, P re, P ost, Inv) where:        normally blocked, but disconnect orders are exempted) that
  • V is a set of operation nodes, each representing a discrete     would be lost in a direct syntax translation. The BSG makes
    business operation (e.g., “validate order”, “calculate tax”).   it explicit before code generation begins.
  • E      ⊆     V × V × L is a set of labeled
                                                                    E. Agent 3: Modernization Transformer
    edges representing control flow, where L                   =
    {sequence, conditional, parallel, error} is the label              The Modernization Transformer generates a modern
    set. Data dependencies live at the node level through           service-oriented implementation from the BSG. It operates
    the inputs(v) and outputs(v) annotations below;                 under four transformation principles:
    a data dependency from u to v is implicit when                     Principle 1 — Operation-to-Endpoint Mapping: Each
    outputs(u) ∩ inputs(v) ̸= ∅. Keeping control flow on            BSG operation node maps to a discrete function or API
    edges and data flow on nodes lets downstream agents             endpoint in the modernized system.
    and human reviewers inspect each independently.                    Principle 2 — Contract Preservation: Pre/postconditions
  • P re : V → P maps each node to a set of preconditions,
                                                                    from the BSG are translated into input validation, output
    logical predicates that must hold before the operation          assertions, and error handling in the generated code.
    executes.                                                          Principle 3 — Data Model Derivation: Input/output an-
  • P ost : V → P maps each node to a set of postconditions,
                                                                    notations from BSG nodes are aggregated to derive modern
    predicates that must hold after it completes.                   data models (e.g., Pydantic models, dataclasses) with type
  • Inv : G → P is a set of global invariants that must hold
                                                                    constraints.
    throughout the workflow.                                           Principle 4 — Flow Preservation: BSG edge labels (se-
                                                                    quence, conditional, parallel, error) determine the orchestration
   Each operation node v ∈ V is further annotated with:             pattern in the modernized implementation.
inputs(v) (required input data fields with types), outputs(v)          Output: A Modernized Service Package with API endpoint
(produced output data fields with types), rules(v) (set of          implementations (Python/FastAPI), data models with valida-
business rule IDs from the BRI), and error behavior(v)              tion rules, orchestration logic preserving the BSG control
(expected behavior under error conditions).                         flow, error handling matching the BSG error behaviors, and
   Edge Label Taxonomy. The four edge labels map to                 documentation mapping each endpoint to its source BSG node.
distinct code-generation patterns: sequence is unconditional
next-step ordering (v always executes after u, generated as         F. Agent 4: Equivalence Validator
a straight-line call); conditional is a guarded transi-                The Equivalence Validator verifies that the modernized
tion where the guard is stored as a P re(v) clause (typi-           implementation matches the behavioral contract specified by
cally paired with a sibling conditional or error edge);             the BSG, using three validation types:
parallel means u and v have no data dependency and                     Type 1 — Contract Verification: For each BSG node,
can run concurrently (generated as an async/gather block);          the agent generates test cases that exercise the correspond-
error is an exception-triggered transition matched against          ing modernized endpoint, verifying that preconditions are
error behavior(u) (generated as an except/catch handler).           enforced, postconditions hold, and invariants are maintained
Every edge carries exactly one label; patterns outside this set     across multi-step workflows.
(e.g., cooperative coroutines) are out of scope for the current        Type 2 — Boundary Testing: The agent generates bound-
BSG.                                                                ary test cases based on BSG constraints (e.g., minimum/max-
   Concrete Example (S1, Order Validation). The BSG node            imum values, empty inputs, null handling, type boundaries).
below, extracted from S1’s COBOL order validation program,             Type 3 — Differential Trace Analysis: The agent con-
illustrates the representation:                                     structs end-to-end workflow traces from the BSG and executes
them against the modernized implementation, comparing ac-           scenarios are drawn from telecommunications and one from
tual outputs against expected BSG-specified outputs.                banking (S8) to test generalization beyond telecom. Each sce-
   Output: A Behavioral Equivalence Report (BER) con-               nario is a legacy artifact bundle plus a gold-standard behavioral
taining: per-node equivalence status (PASS/FAIL/PARTIAL),           specification curated by a domain expert (AI-assisted drafting,
overall behavioral equivalence rate, failed test cases with root    human-reviewed). Table I summarizes them.
cause analysis, and recommendations for remediation.
   Feedback Loop: When the BER identifies behavioral diver-                                     TABLE I
gences, the pipeline re-invokes the Modernization Transformer                  L EGACY M ODERNIZE -8 B ENCHMARK S CENARIOS
with targeted correction instructions, including the failing test
                                                                    ID    Scenario             Domain         Complexity   Rules   LOC
cases and expected behaviors. This feedback loop runs for a
configurable maximum number of iterations (default: 3).             S1    Order Validation     Orders         Medium        12     248
                                                                    S2    Billing Disputes     Billing        High          12     195
G. Orchestration and State Management                               S3    Service Activation   Provisioning   High          14     245
                                                                    S4    Circuit Inventory    Inventory      High          13     280
   The four agents are orchestrated by a directed-graph execu-      S5    Fault Escalation     Fault Mgmt     High          13     230
tion engine (LangGraph). A shared state object accumulates          S6    Contract Renewal     Contracts      High          12     210
                                                                    S7    Account Migration    Accounts       Very High     15     280
artifacts across phases:                                            S8    Bank Transactions    Banking        Very High     15     310
State = {
  legacy_bundle: LegacyArtifactBundle,
  business_rules: BusinessRuleInventory,                               Scenario Design. Each scenario contains explicitly docu-
  bsg: BehavioralSpecificationGraph,                                mented rules and at least three implicit rules inferable only
  modern_code: ModernizedServicePackage,                            from code patterns. Complexity reflects the number of condi-
  equiv_report: BehavioralEquivalenceReport,
  iteration: int,                                                   tional branches, external dependencies, and state transitions.
  status: RUNNING | COMPLETED | FAILED                              Scenarios S1–S7 cover telecom-domain challenges: multi-step
}                                                                   validation (S1), tier-based conditional logic (S2), capacity
                  Listing 2. Pipeline State Object                  management with exemptions (S3), lifecycle management with
                                                                    parent-child dependencies (S4), SLA tracking with tiered
   Each agent reads from and writes to this state, giving full      escalation (S5), stacking discount calculations (S6), and multi-
traceability from legacy artifacts to modernized output.            phase migration with rollback semantics (S7). S8 is a COBOL
                  IV. E VALUATION D ESIGN                           banking transaction processor with multi-type transactions,
                                                                    tier-based withdrawal limits, overdraft protection, transfer fees,
A. Research Questions
                                                                    fraud detection, and dormant account handling.
   We evaluate AgentModernize with respect to the following            Gold-Standard Construction. For each scenario we pro-
research questions:                                                 duced three artifacts before any pipeline run: the legacy code,
   • RQ1 (Behavioral Equivalence): To what extent does              a specification listing every business rule the scenario is
     AgentModernize preserve the behavioral semantics of            intended to encode, and a reference Python implementation
     legacy systems in modernized implementations?                  used later by the fair-evaluation test generator. The rule list
   • RQ2 (Business Rule Preservation): How effectively              was drafted by the primary annotator with LLM assistance
     does the framework extract and preserve individual busi-       (GPT-4o enumerated candidate rules from the legacy code),
     ness rules through the modernization pipeline?                 then manually reviewed, edited, and filtered. Each retained rule
   • RQ3 (Effort Reduction): How does the manual ef-                is labeled explicit or implicit. We treat rule authorship
     fort required for AgentModernize-assisted modernization        as a single-annotator ground truth (Section VII). To avoid
     compare to single-prompt LLM baselines?                        inflating preservation scores, we excluded tautological rules:
   • RQ4 (Agent Contribution): What is the individual               generic input sanitization, rules trivially implied by the target
     contribution of each agent to the overall modernization        type system, and pure field-presence assertions unless presence
     quality?                                                       is itself a business decision. A rule was retained only if a naive
   • RQ5 (BSG Quality): How accurately does the Be-                 translation could plausibly get it wrong (thresholds, exemp-
     havioral Specification Graph capture the gold-standard         tions, state-dependent branches, ordering constraints, cross-
     business rules?                                                field invariants, error-handling policies). Filtering removed 4–9
   • RQ6 (Model Sensitivity): How does modernization qual-          candidate rules per scenario, roughly one third of the LLM-
     ity vary across LLM model sizes?                               drafted set.
B. Benchmark: LegacyModernize-8
                                                                    C. Metrics
  All eight scenarios in LegacyModernize-8 are synthetic,
hand-authored to reflect realistic legacy patterns (COBOL/PL-          Both metrics are computed against a gold-standard test
SQL procedures with embedded business logic, multi-step             suite withheld from the pipeline. Test cases are not derived
workflows, and implicit rules in exception handlers and default     from the BSG. They are synthesized fresh at evaluation time
values) rather than sampled from production codebases. Seven        by GPT-4o-mini from two inputs: the gold-standard scenario
specification (human-authored, AI-assisted drafting, human-                                     TABLE II
reviewed) and the method’s own modernized code. Each                                    R EPRODUCIBILITY D ETAILS
method receives tests generated from its own API surface
                                                                     Item             Details
(endpoint names, request schemas), ensuring fair comparison:
                                                                     Repository       [anonymized for double-blind review]
a method that names its endpoint /process instead of                 Python           3.11
/validate is not penalized for a naming choice. The same             Core libraries   LangGraph, pytest, OpenAI SDK
gold-standard business rules are tested for every method; only       Models           GPT-4o-mini, GPT-4o, GPT-5.3-codex
                                                                     Temperature      0.2 (extraction), 0.0 (generation/eval)
the HTTP-level test harness differs. Assertions are executed         Trials           3 per scenario per method
deterministically by pytest, so BER depends on the test-             Random seed      N/A (temperature 0.0 for generation)
generation prompt but not on any pipeline artifact.                  Run command      python run_fair_eval_existing.py
                                                                                      --model all --trials 3
   M1 — Behavioral Equivalence Rate (BER): The percent-              Output           fair_eval_summary.json, per-scenario fold-
age of gold-standard test cases that pass against the generated                       ers
code: BER = |passing tests|/|total tests|.                           Total API cost   < $15 for full evaluation suite
   M2 — Business Rule Preservation Score (BRPS): The
percentage of gold-standard business rules correctly rep-                                          TABLE III
resented in the modernized output. A rule is preserved                  B EHAVIORAL E QUIVALENCE R ATE (%) — FAIR E VALUATION
                                                                    (GPT-4 O - MINI ). C ELLS REPORT THE MEAN OF 3 TRIALS . N ON - ZERO σ
if it appears in the BSG and the modernized code en-               VALUES : AM ON S2 (10.5), S6 (5.8), S7 (4.4); AM-N O FB ON S2 (10.5),
forces it, as verified by targeted test cases: BRP S =             S5 (48.1), S8 (3.8); C OT ON S2 (5.2), S6 (17.3); SP-LLM ON S8 (3.8).
|preserved rules|/|total rules|.                                                           A LL OTHER CELLS σ = 0.0.

D. Baselines                                                             Scenario     SP-LLM     CoT-LLM      AM (No FB)      AM
   B1 — Single-Prompt LLM (SP-LLM): A single GPT-                             S1       50.0          0.0          58.3        50.0
4o-mini prompt that receives the entire legacy artifact bundle                S2        0.0          6.1          75.8        12.1
                                                                              S3        0.0          0.0           0.0         0.0
and instructions to produce a modernized implementation. No                   S4        0.0          0.0           0.0        25.0
intermediate representation, no verification.                                 S5        0.0          0.0          27.8         0.0
   B2 — Chain-of-Thought LLM (CoT-LLM): A single                              S6        0.0         30.0           0.0        53.3
                                                                              S7        0.0          0.0           0.0        43.6
GPT-4o-mini prompt with chain-of-thought instructions: “First                 S8       48.9          0.0          28.9         0.0
analyze the business logic, then design the modern API, then                  Avg      12.4         4.5           23.9        23.0
implement it.” Still a single model call, but with structured
reasoning.
   B3 — AgentModernize (No Feedback): The full Agent-              S1 (58.3%), S2 (75.8%), S5 (27.8%), and S8 (28.9%). SP-
Modernize pipeline with the feedback loop disabled, measur-        LLM achieves 48.9% on S8, the highest single-cell BER
ing the contribution of iterative refinement.                      for any baseline, demonstrating that a well-shaped single
E. Implementation Details                                          prompt can sometimes outperform the full pipeline on specific
                                                                   scenarios. CoT-LLM scores 30.0% on S6.
   All agents use GPT-4o-mini (OpenAI) as the default LLM             The feedback loop is not universally beneficial: on S2,
backend, with GPT-4o used for the model comparison study           feedback degrades BER from 75.8% (no feedback) to 12.1%,
and GPT-5.3-codex for the frontier model study (Section V-G).      and on S8 from 28.9% to 0.0%. In these cases the Validator’s
The pipeline is orchestrated using LangGraph (Python) for          corrections introduced regressions. On S4, S6, and S7 the
stateful execution. Test cases are executed using pytest. Legacy   pattern reverses: feedback raises BER from 0.0% to 25.0%,
artifacts are written in COBOL/PL-SQL; modernized output           53.3%, and 43.6% respectively. Section VI-B analyzes when
targets Python (FastAPI). Temperature is set to 0.2 for ex-        feedback helps versus hurts. S3 remains at 0.0% across all
traction/specification agents and 0.0 for code generation. The     methods, indicating a structural complexity that no configura-
feedback loop runs for a maximum of 3 iterations. The model        tion handles.
override is implemented at the pipeline level, allowing any
OpenAI-compatible model to be substituted without architec-        B. RQ2: Business Rule Preservation
tural changes.                                                        Table IV lists each scenario’s gold-standard rule composi-
                         V. R ESULTS                               tion (total, explicit, implicit) alongside its preservation score.
                                                                      AgentModernize with feedback preserves rules in S1, S2,
A. RQ1: Behavioral Equivalence                                     S4, S6, and S7, achieving the highest BRPS on S4, S6, and
   Table III compares behavioral equivalence rates across all      S7. SP-LLM preserves 48.9% of rules on S8 (banking), the
scenarios and methods.                                             highest single-scenario preservation for any baseline. CoT-
   No single method dominates all scenarios. AgentModernize        LLM preserves 30.0% on S6 (pricing). The feedback loop adds
with feedback (AM) achieves the highest BER on S4 (25.0%),         value on scenarios where the initial code has correctable point
S6 (53.3%), and S7 (43.6%), where iterative correction fixes       errors (S4, S6, S7) but can regress preservation on S2 and S8.
localized errors. AM without feedback (AM-NoFB) leads on           Table IV shows the explicit/implicit composition per scenario.
                               TABLE IV                                                              TABLE VI
     RULE C OMPOSITION AND P RESERVATION — FAIR E VALUATION .              A BLATION S TUDY — BER (%) BY C ONFIGURATION (FAIR E VALUATION )
  E XPLICIT /I MPLICIT COLUMNS COUNT RULES IN THE GOLD STANDARD ;
 BRPS IS THE FRACTION OF GOLD - STANDARD RULES PRESERVED . E ACH             Config               SP-LLM   CoT    AM (No FB)    Full AM
     GOLD - STANDARD RULE IS EXERCISED BY EXACTLY ONE TEST, SO
NUMERICALLY BRPS EQUALS BER ON A PER - SCENARIO BASIS ; THE TWO              Avg BER               12.4     4.5       23.8         23.0
 TABLES DIFFER IN WHAT THEY MEASURE ( TEST- LEVEL VS . RULE - LEVEL          Non-zero scenarios    2/8      2/8       4/8          5/8
                     VIEW OF THE SAME EVALUATION ).


           ID       Rules    Expl.     Impl.    SP     CoT     AM
                                                                           (NoFB) and 5/8 (AM) vs. 2/8. The extraction-BSG-generation
           S1        12           7     5       50.0     0.0   50.0
           S2        12           8     4        0.0     6.1   12.1
                                                                           pipeline produces better initial code than single-prompt ap-
           S3        14           8     6        0.0     0.0    0.0        proaches even before feedback.
           S4        13           9     4        0.0     0.0   25.0           Feedback helps selectively. Adding feedback raises BER
           S5        13           8     5        0.0     0.0    0.0
           S6        12           7     5        0.0    30.0   53.3
                                                                           on S4 (0 to 25%), S6 (0 to 53.3%), and S7 (0 to 43.6%), where
           S7        15           9     6        0.0     0.0   43.6        iteration 1 code had the correct endpoint shape but localized
           S8        15           8     7       48.9     0.0    0.0        errors (a wrong constant, a missing branch). On S2 (75.8 to
                                                                           12.1%) and S8 (28.9 to 0%), feedback degrades performance:
                                                                           the Validator’s corrections introduced cascading regressions.
Across the benchmark, 64 of 106 gold-standard rules (60%)                  This motivates regression-aware patching that reverts to the
are explicit and 42 (40%) are implicit. Because each rule                  best iteration rather than always applying the latest patch.
maps to exactly one test, the per-scenario BRPS breakdown by                  Baselines are not uniformly zero. SP-LLM achieves 48.9%
category follows directly from which tests pass: for example,              on S8 (banking), where the scenario’s self-contained transac-
in S6 where AM preserves 53.3% (5–6 of 10 rules preserved                  tion types align well with single-prompt generation. CoT-LLM
across trials), the passing set includes both explicit pricing-tier        achieves 30.0% on S6 (pricing). The gold-standard tests are
thresholds and implicit discount-stacking constraints.                     not too strict; they are scenario-specific, generated from each
C. RQ3: Residual Behavioral Failures                                       method’s own API surface, and test for specific business rules
                                                                           that any correct implementation must satisfy.
  A framework that preserves more behavior automatically
should leave fewer behavioral failures for engineers to address.           E. RQ5: BSG Quality
Table V reports failing test counts as a proxy for residual work.
                                                                              Table VII evaluates the Behavioral Specification Graph as
                              TABLE V                                      an intermediate representation by measuring how many gold-
          R ESIDUAL B EHAVIORAL FAILURES — FAIR E VALUATION                standard business rules are captured (recall) and what fraction
                                                                           of extracted rules correspond to real rules (precision).
     ID     Tests      SP-LLM         CoT-LLM     AM (No FB)          AM      Matching Protocol. Extracted BSG rules and gold-standard
     S1      12            6/12        12/12            5/12       6/12    rules use different phrasings, so matching was manual. For
     S2      11           11/11        10/11            3/11      10/11    each scenario the primary annotator compared the extracted
     S3      10           10/10        10/10           10/10      10/10
     S4      12           12/12        12/12           12/12       9/12    rule list against the gold-standard list side by side. A rule
     S5      12           12/12        12/12            9/12      12/12    was a true positive if it referred to the same behavioral
     S6      10           10/10         7/10           10/10       5/10    decision (same trigger, same effect) as a gold-standard rule
     S7      13           13/13        13/13           13/13       7/13
     S8      15            8/15        15/15           11/15      15/15    regardless of wording. Gold-standard rules with no match
                                                                           were misses; extras with no match were classified as plausible
   The residual failure pattern mirrors Table III. AM with                 (a real business decision the annotator did not include) or
feedback produces the fewest failures on S4, S6, and S7                    hallucinated (unsupported by the legacy source). A second
(the scenarios where iterative correction works). AM without               annotator spot-checked S1, S5, and S8 with full agreement on
feedback achieves the best results on S1, S2, S5, and S8. SP-              true-positive judgments; inter-rater kappa is not reported due
LLM reduces failures significantly on S1 (6/12) and S8 (8/15).             to the small spot-check sample. Single-annotator matching is
Only S3 shows universal failure across all methods; the multi-             a threat to validity (Section VII).
step validation wiring required exceeds what any configuration                The BSG achieves 92.3% mean recall and 90.2% precision
produces correctly.                                                        across the benchmark: the extraction pipeline captures most
                                                                           gold-standard business rules even though downstream code
D. RQ4: Ablation Study                                                     generation fails to preserve many in executable form. The gap
  We compare four configurations to isolate the contribution               between BSG recall (92.3%) and end-to-end BER (23.0% for
of each component. Table VI reports summary results.                       AM with feedback) locates the bottleneck in code generation
  The ablation under fair evaluation reveals several findings:             and structural alignment, not extraction. S8 (banking) achieves
  The multi-agent decomposition helps. AM without feed-                    100% recall with 93.8% precision (one plausible extra rule),
back (23.8%) outperforms both SP-LLM (12.4%) and CoT-                      so extraction quality is not restricted to the telecom scenarios
LLM (4.5%) on average, with non-zero BER on 4/8 scenarios                  used during development.
                          TABLE VII                                                         TABLE VIII
  BSG RULE E XTRACTION Q UALITY — P RECISION AND R ECALL (%)            M ODEL C OMPARISON — AGENT M ODERNIZE BER (%) FAIR
                                                                                            E VALUATION
   ID    Gold Rules   BSG Rules    Precision   Recall   Missed
                                                                           Scenario   GPT-4o-mini    GPT-4o    GPT-5.3-codex
   S1        12           25         48.0      100.0      0
   S2        12           10        100.0       83.3      2                   S1          50.0         0.0          33.3
   S3        14           13        100.0       92.9      1                   S2          12.1        18.2           0.0
   S4        13           12        100.0       92.3      1                   S3           0.0        40.0           0.0
   S5        13           10        100.0       76.9      3                   S4          25.0         0.0           0.0
   S6        12           15         80.0      100.0      0                   S5           0.0         0.0           0.0
   S7        15           14        100.0       93.3      1                   S6          53.3         0.0           0.0
   S8        15           16         93.8      100.0      0                   S7          43.6        30.8           0.0
                                                                              S8           0.0        33.3          28.9
   Avg      13.3          14.4       90.2       92.3     1.0
                                                                             Avg          23.0        15.3          7.8
                                                                           Non-zero       4/8         4/8           2/8

   S1 and S6 have 100% recall but lower precision (48%
and 80%): the Legacy Analyzer extracted additional plausible
                                                                     Codex SP-LLM scores 100% on S5, the only perfect BER;
business rules the human annotator did not include. S5 has the
                                                                   codex AM scores 0% on the same scenario. No model domi-
lowest recall (76.9%), missing 3 rules related to SLA tracking
                                                                   nates.
thresholds buried in nested conditional logic.
   The BRI-to-BSG transfer is lossless: every rule extracted       H. RQ6b: Frontier Model Study
by Agent 1 is represented in Agent 2’s BSG output. For
practitioners: if the BSG looks right after Agent 2, the problem      For both GPT-4o and codex, SP-LLM alone outperforms
is downstream in code generation, not upstream in extraction.      AM (19.6% vs. 15.3% and 16.0% vs. 7.8%). Stronger models
                                                                   make the pipeline unnecessary for BER alone. But no single
F. Qualitative Analysis                                            configuration wins everywhere, and SP-LLM produces no
   Implicit Rule Preservation (S1). The Legacy Analyzer            intermediate artifacts. In regulated domains, the audit trail
correctly identified a suspended-account exemption (BR-004)        (rule inventory, BSG, equivalence report) matters regardless
implicit in COBOL control flow; the BSG encoded it and the         of BER. Cost: mini $5, GPT-4o $12, codex $18.
Transformer preserved it. S1 scores 50.0% for both AM and
SP-LLM.                                                                                   VI. D ISCUSSION
   Held-Out Scenario (S8). SP-LLM achieves 48.9% on                A. BSGs as a Trust Boundary
this banking scenario (authored post-freeze), outperforming
                                                                     The BSG creates a trust boundary: upstream is extraction
AM (0.0%). S8’s self-contained transaction types suit single-
                                                                   (noisy, confidence-scored); downstream is generation under
prompt generation; feedback corrections to one type destabi-
                                                                   contract (verifiable). The 67–69-point gap between BSG recall
lize another. A single scenario is not a generalization claim.
                                                                   (92.3%) and end-to-end BER (23.0%) confirms that Agent 3
   Failure (S3). All methods score 0.0%: generated code
                                                                   (code generation), not extraction, is the bottleneck.
implements individual validators but fails to wire multi-step
orchestration.                                                     B. Why the Feedback Loop Is Decisive
   Feedback Success (S6). AM with feedback: 53.3%; with-
out: 0.0%. Three iterations fixed localized pricing-tier errors.      AM with feedback (23.0%) and without (23.8%) achieve
   Feedback Regression (S2). AM-NoFB: 75.8% (9/11 rules).          similar averages on different scenario subsets. Feedback helps
With feedback: 12.1% — fixing 2 rules broke 7 others.              on S4, S6, S7 (localized errors: wrong constants, missing
                                                                   branches) but degrades S2 (−63.7pp) and S8 (−28.9pp)
G. RQ6: Model Comparison                                           through cascading regressions. This motivates regression-
   To evaluate how model capability affects modernization          aware feedback that retains the best iteration. S3 remains 0.0%
quality, we ran the full AgentModernize pipeline with GPT-         everywhere, confirming structural mismatches resist point-
4o and GPT-5.3-codex (a code-specialized frontier model) on        error patching.
all eight scenarios under the same per-method fair evaluation
protocol. Table VIII shows the results.                            C. The Implicit Rule Problem
   The pipeline architecture is model-agnostic, but whether           We use implicit rule for behavioral requirements inferable
the pipeline actually helps depends on the model. Mini ben-        from code patterns (default values, error handlers doubling as
efits: AM (23.0%) beats SP-LLM (12.4%). GPT-4o does not:           constraints, cross-module dependencies) rather than stated in
SP-LLM (19.6%) beats AM (15.3%). Codex is worse still:             source. This is distinct from data constraints (type restrictions,
SP-LLM 16.0%, AM only 7.8% (non-zero on 2/8 scenarios).            value ranges), which the BSG captures as node annotations.
Weaker models need the structure; stronger models produce          We separate these categories because the gap between explicit
good enough initial code that feedback-loop corrections intro-     and implicit preservation rates reveals where LLM-based ex-
duce regressions.                                                  traction struggles.
D. Statistical Power                                                                        VIII. C ONCLUSION
   With N = 8 scenarios and 3 trials we cannot make                   We started by treating legacy modernization as a translation
strong statistical claims. Of 32 scenario-method cells, 20 yield   problem, and it did not work. AgentModernize reframes it as
σ = 0.0; the largest σ is 48.1 (AM-NoFB on S5). A larger           behavioral preservation, decomposing the task into extraction,
benchmark would strengthen confidence.                             specification, code generation, and validation, linked by Be-
                                                                   havioral Specification Graphs.
E. Comparison Scope                                                   With GPT-4o-mini, BSG-guided generation (23.9%) nearly
   We compare against LLM baselines, not commercial tools          doubles the best baseline (SP-LLM, 12.4%). With stronger
(IBM Rational, Micro Focus) or agentic coding systems.             models, SP-LLM wins—the pipeline’s benefit is inversely
Commercial tools do not publish BER metrics; agentic systems       correlated with model capability. The BSG captures 92.3% of
target different problems (e.g., resolving GitHub issues). A       gold-standard rules at 90.2% precision; code generation, not
missing baseline is “LLM + feedback without BSG”: our              extraction, is the bottleneck. Even when SP-LLM beats the
ablation shows BSG-based decomposition produces better             pipeline on BER, only the pipeline produces inspectable arti-
initial code, but does not prove BSG is required in addition to    facts that regulated industries require. Future work: regression-
feedback.                                                          aware feedback, per-scenario model selection, and human trust
                                                                   studies of BSG-inspectable modernization.
F. Limitations
                                                                                                 R EFERENCES
   We evaluated on 100–310 line scenarios; real legacy systems
                                                                    [1] S. Comella-Dorda, K. Wallnau, R. Seacord, and J. Robert, “A survey
are orders of magnitude larger and would require hierarchical           of legacy system modernization approaches,” Software Engineering
BSGs and incremental validation. The pipeline’s benefit is              Institute, Carnegie Mellon University, Tech. Rep. CMU/SEI-2000-TN-
inversely correlated with model capability: AM outperforms              003, 2000.
                                                                    [2] H. P. Breivold, I. Crnkovic, and M. Larsson, “A systematic
SP-LLM only with GPT-4o-mini (23.0% vs. 12.4%); with                    review of software architecture evolution research,” Information
GPT-4o and codex, SP-LLM wins because stronger models                   and Software Technology, vol. 54, no. 1, pp. 16–40, 2012.
produce initial code good enough that feedback introduces               doi:10.1016/j.infsof.2011.08.002
                                                                    [3] R. Kazman, S. G. Woods, and S. J. Carrière, “Requirements for
regressions.                                                            integrating software architecture and reengineering models: CORUM II,”
                                                                        in Proc. Working Conference on Reverse Engineering (WCRE), 1998.
                 VII. T HREATS TO VALIDITY                              doi:10.1109/WCRE.1998.723185
                                                                    [4] S. Rugaber and K. Stirewalt, “Model-driven reverse engi-
   Internal validity. All eight scenarios are synthetic and au-         neering,” IEEE Software, vol. 21, no. 4, pp. 45–53, 2004.
thored by a single annotator. They reflect realistic complexity         doi:10.1109/MS.2004.23
                                                                    [5] M. Chen et al., “Evaluating large language models trained on code,”
but lack the messiness of production code.                              arXiv preprint arXiv:2107.03374, 2021.
   External validity. Seven telecom and one banking scenario        [6] R. Li et al., “StarCoder: may the source be with you!” arXiv preprint
in COBOL/PL-SQL. Healthcare, government, and other do-                  arXiv:2305.06161, 2023.
                                                                    [7] C. Hou et al., “Large language models for software engineering: A sys-
mains remain untested.                                                  tematic literature review,” ACM Transactions on Software Engineering
   Construct validity. Test-based verification covers tested            and Methodology, 2024. doi:10.1145/3695988
paths only; untested edge cases may harbor regressions.             [8] H. Brunelière, J. Cabot, G. Dupé, and F. Madiot, “MoDisco:
                                                                        A model driven reverse engineering framework,” Information and
   Reliability. We use temperature 0.0 for generation and 3             Software Technology, vol. 56, no. 8, pp. 1012–1032, 2014.
trials. Of 32 cells, 20 yield σ = 0.0; the largest is 48.1 (AM-         doi:10.1016/j.infsof.2014.04.007
NoFB on S5). Five cells report 0% BER due to non-executable         [9] A. De Lucia, A. R. Fasolino, and M. Napoli, “An approach for
                                                                        reverse engineering of COBOL-based applications,” in Proc. Euro-
code (prose output or Pydantic v1/v2 incompatibility). GPT-             pean Conference on Software Maintenance and Reengineering, 2001.
5.3-codex has restricted availability; results may not transfer         doi:10.1109/CSMR.2001.914982
to other model families.                                           [10] Z. Li et al., “Large language models for code analysis: Do LLMs really
                                                                        do their job?” arXiv preprint arXiv:2310.12357, 2023.
   Selection bias. The primary annotator designed scenarios        [11] Z. Li et al., “Automating code review activities by large-scale pre-
and gold-standard rules. S8 (banking, authored after pipeline           training,” in Proc. 30th ACM Joint European Software Engineering
freeze) acts as a held-out probe but does not eliminate author-         Conference (ESEC/FSE), 2022. doi:10.1145/3540250.3549081
                                                                   [12] C. S. Xia and L. Zhang, “Less training, more repairing please: revisiting
ing bias; an independent benchmark would strengthen validity.           automated program repair via zero-shot learning,” in Proc. 30th ACM
   LLM-as-evaluator. Gold-standard tests are synthesized by             Joint European Software Engineering Conference (ESEC/FSE), 2022.
GPT-4o-mini from each method’s own code and the specifica-              doi:10.1145/3540250.3549101
                                                                   [13] R. Pan et al., “Lost in translation: A study of bugs introduced by
tion, then executed deterministically by pytest. BER depends            large language models while translating code,” in Proc. IEEE/ACM
on the test-generation prompt but not on any pipeline artifact.         International Conference on Software Engineering (ICSE), 2024.
   Artifact availability. Framework implementation, bench-              doi:10.1145/3597503.3639226
                                                                   [14] S. Hong et al., “MetaGPT: Meta programming for a multi-agent collab-
mark scenarios, BSG schemas, evaluation scripts, and prompts            orative framework,” in ICLR, 2024.
are available at [anonymized for double-blind review]. AI          [15] C. Qian et al., “ChatDev: Communicative agents for software develop-
tools (GPT-4o) were used only for grammar editing during                ment,” in ACL, 2024. doi:10.18653/v1/2024.acl-long.810
                                                                   [16] K. Huang et al., “AgentCoder: Multi-agent-based code generation with
manuscript preparation; all research content was produced by            iterative testing and optimisation,” arXiv preprint arXiv:2312.13010,
the authors.                                                            2023.
[17] R. Milner, Communication and Concurrency.           Prentice Hall, 1989.
     ISBN: 978-0-13-115007-2.
[18] W. McKeeman, “Differential testing for software,” Digital Technical
     Journal, vol. 10, no. 1, pp. 100–107, 1998.
[19] T. Y. Chen, S. C. Cheung, and S. M. Yiu, “Metamorphic testing: A new
     approach for generating next test cases,” Tech. Rep. HKUST-CS98-01,
     1998.
[20] G. T. Leavens, A. L. Baker, and C. Ruby, “JML: A notation for
     detailed design,” in Behavioral Specifications of Businesses and Systems,
     H. Kilov, B. Rumpe, and I. Simmonds, Eds. Springer, pp. 175–188,
     1999. doi:10.1007/978-1-4615-5229-1_12
[21] B. Meyer, “Applying design by contract,” IEEE Computer, vol. 25,
     no. 10, pp. 40–51, 1992. doi:10.1109/2.161279
[22] Object Management Group, “Architecture-Driven Modernization:
     Knowledge Discovery Meta-Model (KDM), v1.4,” OMG Standard
     formal/2016-02-01, 2016. Available: https://www.omg.org/spec/KDM/1.
     4
[23] A. Madaan et al., “Self-Refine: Iterative refinement with self-feedback,”
     in Advances in Neural Information Processing Systems (NeurIPS), 2023.
[24] N. Shinn et al., “Reflexion: Language agents with verbal reinforce-
     ment learning,” in Advances in Neural Information Processing Systems
     (NeurIPS), 2023.
[25] X. Zhang, X. Hou, X. Qiao et al., “A review of automatic source code
     summarization,” Empirical Software Engineering, vol. 29, art. 162, 2024.
     doi:10.1007/s10664-024-10553-6
[26] Y. Zou and M. Hung, “An approach for extracting workflows from
     e-commerce applications,” in Proc. 14th IEEE International Con-
     ference on Program Comprehension (ICPC), 2006, pp. 127–136.
     doi:10.1109/ICPC.2006.9
