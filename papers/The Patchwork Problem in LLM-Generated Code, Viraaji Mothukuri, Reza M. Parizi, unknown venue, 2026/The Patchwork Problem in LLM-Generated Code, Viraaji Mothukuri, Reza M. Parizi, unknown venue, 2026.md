                                                           The Patchwork Problem in LLM-Generated Code
                                                                         Viraaji Mothukuri, Reza M. Parizi
                                                     Decentralized Science Lab, College of Computing and Software Engineering
                                                                        Kennesaw State University, GA, USA
                                                          vmothuku@students.kennesaw.edu rparizi1@kennesaw.edu


                                        Abstract
                                        LLM-generated code often compiles, passes tests, and appears correct, yet breaks once deployed. The root cause is
                                        frequently structural rather than logical. A generated endpoint references configuration keys never declared in the
                                        project, an import targets a package that does not exist in any registry, or a new route omits the authentication guard
                                        applied to every sibling endpoint. Each patch is locally valid but globally incoherent, and standard CI toolchains rarely
                                        surface these failures. As LLM-powered coding tools see widespread adoption, this blind spot poses a growing risk to
                                        software quality. We call this the patchwork problem. This paper formalizes structural coherence as consistency
                                        invariants over graph representations of repository artifacts, including import, call, dependency, configuration, schema,
arXiv:2607.08981v1 [cs.SE] 9 Jul 2026




                                        resource, control-flow, and routing graphs, and introduces an eight-category failure taxonomy distinguishing defects
                                        specific to LLM generation from those merely amplified by it. We present a hybrid verification framework that
                                        delegates to mature static analysis tools where they already excel and deploys purpose-built detectors for cross-cutting
                                        invariants underserved by existing toolchains, targeting provable constraint violations rather than heuristic pattern
                                        matching. Empirical evaluation across two frontier models under four prompting strategies reveals that the vast
                                        majority of structural failures evade type checking, testing, and SAST entirely, and that failure patterns diverge
                                        qualitatively between models in ways that challenge model-agnostic mitigation strategies. External validation on
                                        real-world AI-generated repositories confirms that these failures are not artifacts of controlled experimentation but
                                        are prevalent wherever LLMs write code with minimal human oversight.
                                        Keywords: LLM code generation, structural coherence, static analysis, graph invariants, code quality, neural code
                                        synthesis.

                                        1    Introduction                                                tools typically focus on taint flows rather than structural
                                                                                                         coherence. The result is a blind spot in which generated
                                        Code generation from Large Language Models has                   code enters codebases carrying latent defects that remain
                                        achieved remarkable results on isolated programming              invisible to standard toolchains. We term this the
                                        tasks [1–4], driving rapid adoption, with millions of            patchwork problem. LLM-generated patches may
                                        engineers using LLM-powered assistants daily. Yet                be individually well-formed yet fail to cohere into a
                                        a gap persists between benchmark performance and                 consistent whole, particularly at repository scale, where
                                        production utility [5]. Code that appears correct in             consistency constraints span imports, dependencies,
                                        isolation frequently fails when integrated into real             configurations, schemas, and security contracts [7].
                                        software systems [6], and the dominant failure mode is               Our approach formalizes structural coherence as
                                        structural rather than functional. A generated patch             consistency invariants over graph representations of
                                        may compile, pass type checking, and satisfy local               repository artifacts [8]. A key design insight is that
                                        tests while violating invariants that span the repository.       reliable detection requires matching each invariant class
                                        Consider a FastAPI endpoint referencing a Pydantic               to an appropriate verification strategy. Categories where
                                        model with hallucinated field names, or a Django view            mature static analysis tools already capture the relevant
                                        assuming environment variables that are never declared           language semantics can be delegated to those tools, while
                                        in the project configuration. Such patches exhibit local         categories that require cross-graph reasoning, absent from
                                        correctness but global incoherence: they pass the checks         existing toolchains, call for purpose-built detectors that
                                        developers rely on and fail only when exercised in the           target constraint violations under explicit assumptions
                                        context of the full system.                                      and produce actionable evidence. This work makes
                                            Current evaluation methodologies do not surface these        three contributions: (1) We introduce a taxonomy of
                                        failures systematically. Type checking and linting often         eight structural failure categories, each defined
                                        miss semantic inconsistencies that cross file boundaries.        by graph-based consistency invariants, distinguishing
                                        Test suites cannot cover every integration point. SAST           failures characteristic of LLM-generated patches from


                                                                                                     1
issues merely amplified by them. (2) We present a
                                                                            Table 1: Summary of related work
multi-graph verification framework that integrates
                                                                   Work     Focus                              Gap
mature static analysis tools (mypy, tsc, pylint, ESLint)           [6]      Taxonomy of hallucinations in      Descriptive;      no    formal
with purpose-built cross-graph detectors over eight                         repo-level generation              invariants
                                                                                                               detection
                                                                                                                            or     automated

repository graphs, producing localized evidence traces             [9]      Quantitative measurement of        Dependency-only;              no
for each violation. (3) We provide an empirical study              [7]
                                                                            fabricated package references
                                                                            Cross-file code completion with
                                                                                                               cross-artifact verification
                                                                                                               Evaluates    completion,      not
across 336 generations from two frontier models                             retrieval subtasks                 structural coherence

under four prompting conditions, along with external               [5]      GitHub issue resolution via
                                                                            test passage
                                                                                                               Test-based; misses failures that
                                                                                                               evade tests
validation on 43 real-world AI-generated repositories.             [10]     Repo-aligned generation with       Pass@k metric; no structural
                                                                            dependency annotations             invariant checking

                                                                   [11]     Backend     generation   with      Exploit-focused; no config or
                                                                            exploit-based         security     schema verification
2    Related Work                                                           assessment

                                                                   [12]     Security-focused          patch    Vulnerability    labels,      not
                                                                            evaluation                         structural constraints
Table 1 situates our contribution relative to prior                [13]     Multi-file        vulnerability    Security-scoped; no general
work across four research threads.         Hallucination           [14]
                                                                            scenarios
                                                                            Autonomous multi-step repo
                                                                                                               structural coverage
                                                                                                               Evaluates resolution rate, not
characterization work [6, 9] establishes the empirical                      editing                            edit coherence
                                                                   [8]      Unified code property graph for    Single-file; no cross-file or
prevalence of structural defects in generated code                          vulnerability discovery            config constraints

but characterizes them descriptively rather than                   [15]     Multi-view
                                                                            pre-training
                                                                                                contrastive    Graphs as training signal, not
                                                                                                               verification layer
as verifiable constraint violations. Repository-level              [16]     Graph-aligned fine-tuning for      Alignment       target, not
benchmarks, including RepoBench [7], SWE-bench [5],                [17]
                                                                            structural semantics
                                                                            Constrained    decoding   for
                                                                                                               constraint checking
                                                                                                               Decoding-time; no post-hoc
EvoCodeBench [10], BaxBench [11], SecRepoBench [12],                        secure generation                  structural verification

SecureVibeBench [13], and SWE-agent [14] demonstrate               [18]     Dual-judge
                                                                            detection
                                                                                               vulnerability   Vulnerability-scoped;
                                                                                                               structural coherence
                                                                                                                                             no


that snippet-level performance does not transfer reliably
to repository-scale tasks, yet their evaluation criteria
remain outcome-oriented (test passage, exploit success)           requires the import graph and symbol table, optionally
rather than diagnosing which structural invariants are            augmented with type information for generic resolution.
violated. Graph-based representations such as Code                Evidence traces record file, line, symbol, expected
Property Graphs [8], CODE-MVP [15], and GALLa [16]                module, and resolution outcome. This failure class is
leverage graphs as representational substrates but do             amplified in LLM outputs because models operating
not operationalize them as a constraint verification layer.       with incomplete context frequently invent plausible but
Secure generation approaches, including CodeGuard+                non-existent module names or reference deprecated APIs.
[17] and SafeGenBench [18], target vulnerability                      Phantom Internal API (PIA): Phantom API
prevention without formalizing structural coherence.              failures occur when generated code invokes internal
Our work addresses this gap by defining structural                functions with incorrect signatures or semantics
incoherence as violated consistency constraints across            inconsistent with declared interfaces. The invariant
graph representations and producing localized evidence            requires signature compatibility such that for call
traces that attribute failures to specific constraint             site 𝑐 invoking symbol 𝑠 with signature registry Σ,
violations.                                                       compatible(sig(𝑐), Σ(𝑠)) = true. Detection leverages
                                                                  the call graph and signature registry extracted from
                                                                  type annotations and protocol declarations.         This
3    Structural Failure Taxonomy                                  category is strongly amplified as LLMs hallucinate
                                                                  method signatures based on naming conventions rather
The patchwork problem manifests through structural
                                                                  than actual declarations, particularly for internal APIs
failures, defined as violations of consistency invariants
                                                                  underrepresented in training data.
at the repository scale, verifiable via static graph
                                                                      Dependency Hallucination (DHI): Algorithm 2
analysis without execution. These failures differ from
                                                                  validates that all external imports reference packages
functional bugs in that individual patches appear
                                                                  declared in the project’s dependency manifests. External
correct yet collectively violate project contracts. Our
                                                                  imports not found in the dependency graph trigger
taxonomy comprises eight categories, each defined
                                                                  registry queries to PyPI or npm, distinguishing fully
by formal invariants, required graph artifacts, and
                                                                  hallucinated packages (nonexistent in registries) from
failure characteristics specific to LLM outputs. Table 2
                                                                  undeclared-but-existing packages. For npm packages,
summarizes the classification.
                                                                  import names match registry names directly. For PyPI,
    Symbol Resolution Failures (SRF): A symbol
                                                                  the detector assumes direct correspondence between
resolution failure occurs when a referenced name
                                                                  import names and package names, which holds for the
cannot be resolved within the repository’s module
                                                                  majority of packages but not for cases where import and
graph.     Formally, for symbol reference 𝑟 in file
                                                                  distribution names diverge (e.g., yaml vs. PyYAML, cv2
 𝑓 with module graph M, the invariant requires
                                                                  vs. opencv-python). The resulting phantom module set
∀𝑟 ∈ refs( 𝑓 ) : ∃𝑑 s.t. resolve(𝑟, 𝑓 , M) → 𝑑. Detection


                                                              2
feeds downstream into SRF and PIA detection.                   schema(𝑃.output) ⊇ schema(𝐶.input) with type
    Build/Configuration Incoherence (BCI): Build               consistency. Detection requires the call graph with
configuration failures arise when generated code assumes       edges spanning files and the schema graph extracted
configurations inconsistent with the repository’s declared     from OpenAPI specs, Pydantic models, or Zod schemas.
state. The invariant requires that for each configuration      LLMs amplify this failure by hallucinating response
assumption 𝑎 implied by generated code, a satisfying           fields based on naming conventions.
declaration exists in the configuration space C. Detection         Security Structural Regressions (SSR): Security
operates over the build graph and configuration graph          structural regressions occur when application wiring
encompassing entrypoints, environment variables, and           violates security contracts absent classic taint flow
framework settings. Four invariant classes apply across        vulnerabilities. The invariant requires guard coverage
languages, namely entrypoint existence, environment            such that ∀𝑟 ∈ 𝑅 : guarded by(𝑟, 𝑀) for security-critical
variable declaration, module system consistency, and           routes 𝑅 and required guards 𝑀. Detection requires
framework configuration alignment. This category is            routing and middleware attachment graphs specific
amplified under weak retrieval context where models            to each framework. We scope detection to FastAPI
default to standard configurations divergent from project      (dependency injection guards), Django (permission
settings.                                                      decorators), Express (middleware chains), and Next.js
    Resource Coherence Failures (RCF): Resource                (middleware matchers). LLMs amplify this failure by
coherence failures occur when code fails to provide            wiring middleware incorrectly, even when producing
declared resources, encompassing both filesystem               syntactically correct code.
resources and computational contracts. Filesystem
resource failures arise when code references files, assets,
templates, or migrations that do not exist, with the           4 Verification Framework
existence invariant requiring exists(resolve path(𝑟, root)) =
                                                               Architecture Overview: The verification framework
true for each resource reference 𝑟 and additional ordering
                                                               employs a hybrid architecture guided by a precision-first
constraints for sequential resources such as database
                                                               design philosophy in which each taxonomy category is
migrations. Return contract failures arise when functions
                                                               matched to the verification strategy that maximizes
with declared return types contain execution paths that
                                                               detection precision for its invariant class. Categories
do not produce a value matching the declared type,
                                                               where mature static analysis tools already handle the
violating the contract that the function’s signature
                                                               relevant language semantics (symbol resolution, signature
promises to callers. Schema completeness failures arise
                                                               compatibility) delegate to those tools, inheriting their
when model definitions omit fields required by consuming
                                                               years of edge-case handling. Control flow coherence
code. Detection operates over the resource graph
                                                               employs a hybrid approach combining custom graph
mapping code references to filesystem paths, the CFG
                                                               reachability and pattern matching with SAST tool
for return-path reachability analysis, and the schema
                                                               delegation, reflecting the observation that no single
graph for field completeness validation. LLMs exhibit
                                                               layer achieves adequate coverage alone. Categories
amplified failure rates across all three sub-categories
                                                               requiring cross-graph reasoning absent from existing
by generating plausible paths based on conventions
                                                               toolchains (configuration incoherence, dependency
rather than actual repository structure, omitting return
                                                               hallucination, security regressions, resource coherence,
statements on error-handling branches, and producing
                                                               cross-file contracts) employ purpose-built detectors
incomplete schema definitions.
                                                               that target provable constraint violations rather than
    Control Flow Coherence (CFC): Control
                                                               heuristic pattern matching. This division reflects the
flow failures manifest as CFG anomalies including
                                                               empirical observation that reimplementing established
unreachable blocks, contradictory conditions, exception
                                                               analyses from scratch produces low-precision detectors
flow misuse, and dead error handling. Invariants
                                                               due to the long tail of language-specific edge cases
require full reachability from entry (∀𝑣 : reachable(𝑣 0 , 𝑣))
                                                               (exception flows, generators, context managers, async
and exception handler type consistency. Detection
                                                               patterns), while the novel cross-cutting invariants central
operates on intraprocedural CFGs with exception edge
                                                               to the patchwork problem have no existing tool coverage.
annotations. While unreachable code is a general bug
                                                               The framework operates on each repository state after
class, LLMs exhibit amplified characteristic patterns
                                                               generation, constructing graph representations from the
such as overbroad exception handling, redundant null
                                                               combined original and generated code and routing each
checks, and copy-paste control flow inconsistencies.
                                                               to the appropriate verification backend. The framework’s
    Cross-File Contract Violations (CCV): Contract
                                                               output for each finding is a localized evidence trace
violations occur when producer and consumer modules
                                                               recording the violated invariant, the implicated files and
exhibit interface mismatches across file boundaries,
                                                               line numbers, and the constraint that would need to hold
including wrong field names, incompatible serialization,
                                                               for the code to be structurally sound. All source code,
incorrect error codes, and misaligned assumptions.
                                                               graph construction scripts, detection pipelines, evaluation
The invariant requires schema compatibility whereby


                                                            3
                                                                                                                                                                                                                                                                                                                                                     P3: Retrieved Files
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    P2: Local Files Only
                                                                                                                                                                                                                                                                                                                                                                  fragmented view
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          partial view
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    task only
blind generation
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    LLM-Generated Patch
                                                                                                                                                                                                                                                                                                                Oracle Files
                                                                                                                                                                         P4: Full  Context
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 P1: Minimal
                                                                                                                                                                                                                                                                                                                                                                                                                                                               Generated Code
                                                                                                                                                                                                                                                                                                                                                                                    Routing Graph
(route + middleware)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Resource and Call Graph
(pycg / ts-morph)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Control Flow Graph
(branch analysis)
                                                                   Import Graph
(AST parsing)
                                                                                                                                                                                                                             Dependency Graph
(manifest parsing)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Config Graph
(config parsing)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Schema Graph
(type analysis)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              unreachable/dead code
dead branches
                                                                                                                                                                                                                                                                    undeclared packages
Hallucinated packages
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  undefined calls
signature mismatch
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           invalid settings
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 schema mismatches
                                                                                                                           unresolved imports
phantom dependencies
                                                                                                                                                                                                                                                                                                                               missing auth guards
       stale references
                          SRF
Symbol Resolution Failures
                                                                                                PIA
Phantom Internal API
                                                                                                                                                                                             DHI
 Dependency Hallucination
                                                                                                                                                                                                                                                                                                                                                                                                                         SSR
Security Structural Regressions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 CFC
Control Flow Coherence
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               BCI
Build/Configuration Incoherence
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          RCF
Resource Coherence Failures
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     CCV
Cross File Contract Violations
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Detection Output
Errors & Warnings
                                                                                                                                                                     Figure 1: Overview of the Proposed Framework


                                                                                                                                                                                             Table 2: Structural failure taxonomy
                                                           ID    Category                                                                                                 Primary Graph(s)                                                                                                                                                                                                                                                                                                                LLM Profile                                                                                                                                                                                            Type check evasion                                                                  Test Evasion

                                                           SRF   Symbol Resolution                                                                                        Import + Symbol Table                                                                                                                                                                                                                                                                                                           Amplified                                                                                                                                                                                                                                                  Partial                                                                                                           Partial
                                                           PIA   Phantom Internal API                                                                                     Call + Signature                                                                                                                                                                                                                                                                                                                Strongly Amplified                                                                                                                                                                                                                                          Yes                                                                                                               Yes
                                                           DHI   Dependency Hallucination                                                                                 Dependency + Registry                                                                                                                                                                                                                                                                                                           Specific to LLMs                                                                                                                                                                                                                                            Yes                                                                                                               Yes
                                                           BCI   Build/Config Incoherence                                                                                 Build + Config                                                                                                                                                                                                                                                                                                                  Amplified                                                                                                                                                                                                                                                   Yes                                                                                                               Yes
                                                           RCF   Resource Coherence                                                                                       Resource + CFG + Schema                                                                                                                                                                                                                                                                                                         Amplified                                                                                                                                                                                                                                                   Yes                                                                                                               Yes
                                                           CFC   Control Flow Coherence                                                                                   CFG                                                                                                                                                                                                                                                                                                                             General/Amplified                                                                                                                                                                                                                                          Partial                                                                                                           Partial
                                                           CCV   Cross-File Contracts                                                                                     Call + Schema                                                                                                                                                                                                                                                                                                                   Amplified                                                                                                                                                                                                                                                   Yes                                                                                                               Yes
                                                           SSR   Security Structural                                                                                      Routing + Middleware                                                                                                                                                                                                                                                                                                            Amplified                                                                                                                                                                                                                                                   Yes                                                                                                               Yes




configurations, and external validation datasets required                                                                                                                                                                                                                                                                                                                                                                                                                                                 multiple categories, motivating the hybrid architecture.
to reproduce our results are publicly available [19].                                                                                                                                                                                                                                                                                                                                                                                                                                                         Detection Algorithms: The following paragraphs
Figure 1 illustrates the end-to-end verification pipeline,                                                                                                                                                                                                                                                                                                                                                                                                                                                formalize detection for each taxonomy category.
showing how graph construction connects prompting                                                                                                                                                                                                                                                                                                                                                                                                                                                         Purpose-built detectors (Algorithms 1–3, 4, 5, and 7)
conditions to failure detection.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          target provable constraint violations, while control flow
    Graph Construction: For each repository state                                                                                                                                                                                                                                                                                                                                                                                                                                                         coherence (Algorithm 6) combines custom analysis with
after generation, the framework constructs eight graph                                                                                                                                                                                                                                                                                                                                                                                                                                                    SAST tool delegation. Detection order reflects data
representations spanning structural, behavioral, and                                                                                                                                                                                                                                                                                                                                                                                                                                                      dependencies, with DHI running first to produce the
configurational dimensions. Table 3 summarizes the                                                                                                                                                                                                                                                                                                                                                                                                                                                        phantom module set consumed by SRF and PIA.
construction method for each graph type.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Configuration Incoherence Detection (BCI):
    Figure 2 visualizes the many-to-many mapping                                                                                                                                                                                                                                                                                                                                                                                                                                                          Algorithm 1 detects provable runtime failures from
between graph representations and failure categories,                                                                                                                                                                                                                                                                                                                                                                                                                                                     unguarded environment variable accesses. It extracts
illustrating why the framework requires multiple                                                                                                                                                                                                                                                                                                                                                                                                                                                          strict access patterns that throw on missing values
coordinated analyses rather than a single monolithic                                                                                                                                                                                                                                                                                                                                                                                                                                                      (os.environ["KEY"] in Python, unguarded process.env.KEY
pass. Chords connect each graph representation (left) to                                                                                                                                                                                                                                                                                                                                                                                                                                                  in TypeScript), eliminates accesses protected by guards
the failure categories it enables detecting (right). Some                                                                                                                                                                                                                                                                                                                                                                                                                                                 (try/except, membership tests, fallback operators), and
categories require multiple graphs, and some graphs serve                                                                                                                                                                                                                                                                                                                                                                                                                                                 validates remaining accesses against the repository’s


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                4
                                                                                         Algorithm 1 Configuration Incoherence Detection
  Table 3: Graph construction methods by language                                        (BCI)
 Graph           Python                             TypeScript

 Import         ast module; relative import         ts.createProgram         with
                                                                                         Require: Repository 𝑅 with generated code 𝐺, config files 𝐶
                resolution                          tsconfig.json resolution             Ensure: Set of validated configuration incoherence findings
 Call           pycg        flow-insensitive        Compiler                  API
                points-to analysis                  type-directed resolution                 𝐹
 Dependency     pyproject.toml,                     package.json,
                requirements.txt, poetry.lock       package-lock.json, yarn.lock +        1: Extract unsafe accesses
                + PyPI validation                   npm validation
 Schema         Pydantic            BaseModel,      Zod     z.object(),   Prisma          2: 𝐴 ← ∅
                SQLAlchemy Column                   schema.prisma
 Config         .env, .env.example, Docker          Same sources
                                                                                          3: for each file 𝑓 in 𝐺 do
                Compose,
                settings
                                  framework                                               4:   if 𝑓 is Python then
 Resource       open(),          pathlib.Path,      Equivalent TS patterns                5:      𝐴 ← 𝐴 ∪ {os.environ["K"] patterns in 𝑓 }
                template             loaders,
                migration deps                                                            6:   else if 𝑓 is TypeScript then
 CFG            ast branch analysis; pylint         ts-morph branch analysis;
                delegation                          ESLint delegation                     7:      𝐴 ← 𝐴 ∪ {unguarded process.env.K in 𝑓 }
 Routing        FastAPI route decorators,           Express     router  chains,
                Django URL conf                     Next.js         middleware            8:   end if
                                                    matchers
                                                                                          9: end for
                                                                                         10: Guard elimination
                                                                                         11: for each access 𝑎 ∈ 𝐴 do
                                                                                         12:   if 𝑎 inside try/except KeyError or preceded by
                                          Config                                               membership test or has ||/?? fallback then
                              CFG                  Schema
                                                                                         13:      𝐴 ← 𝐴 \ {𝑎}
                  Resource                                  Dependency
                                                                                         14:   end if
              Routing                                             Call                   15: end for
                                                                                         16: Config-space validation
               SRF                                                  Import               17: C       ←      keys     from      .env, .env.example,
                                                                                             docker-compose.yml, settings
                 PIA                                              SSR                    18: 𝐹 ← ∅
                                                                                         19: for each access 𝑎 ∈ 𝐴 with key 𝑘 do
                        DHI                                 CCV
                                                                                         20:   if 𝑘 ∉ C then
                              BCI                  CFC
                                    RCF                                                  21:      𝐹 ← 𝐹 ∪ {(𝑎, 𝑘, file, line)}
                                                                                         22:   end if
                                                                                         23: end for
                                                                                         24: return 𝐹

            Figure 2: Graph-to-category mapping
                                                          guarded by exception handlers that re-raise or call
configuration space. Arithmetic expressions and safe      sys.exit. Filesystem resource violations check that
access patterns with explicit defaults are excluded at    referenced paths (templates, migrations, assets) resolve
extraction time. Every reported finding represents a      to existing files. Schema completeness violations flag
configuration access that will produce a runtime crash if consuming code that accesses fields absent from the
the variable is absent.                                   producing model’s definition. Every finding represents a
    Dependency Hallucination Detection (DHI):             provable violation: a reachable path missing a declared
Algorithm 2 validates that all external imports reference return, a path literal that does not resolve, or a field
packages declared in the project’s dependency manifests.  access targeting an undefined name.
External imports not found in the dependency graph            Cross-File Contract Violation Detection
trigger registry queries to PyPI or npm, distinguishing   (CCV):      Algorithm 5 detects interface mismatches
fully hallucinated packages (nonexistent in registries)   across  module    boundaries via call graph and schema
from undeclared-but-existing packages. The resulting      graph   analysis.  It targets four patterns: disconnected
phantom module set feeds downstream into SRF and          middleware     (registered  but never imported in route
PIA detection.                                            modules),     unused   decorators  referencing nonexistent
    Symbol Resolution and Phantom API                     permission    classes,  duplicate middleware   registrations
Detection (SRF, PIA): Algorithm 3 leverages               causing  double   execution,  and field naming  mismatches
the phantom module set from Algorithm 2.               A  between   producer  response  schemas   and consumer   access
LocalModulePattern filter excludes intra-generation       patterns   (e.g., user  name  vs. username).   Each  finding
cross-references and intentional placeholders to prevent  identifies a statically verifiable disconnect between two
false positives from multi-file generation tasks.         code locations that must agree for correct execution.
    Resource Coherence Detection (RCF): Algorithm 4           Control Flow Coherence Detection (CFC):
targets three sub-categories. Return contract violations  Algorithm    6 employs a hybrid three-layer approach with
construct intraprocedural CFGs for functions with         findings deduplicated    by line number. Layer 1 performs
declared return types and identify execution paths that   BFS   reachability   from  function entry nodes, flagging
terminate without producing a value, excluding branches   only  entirely  dead   functions.  Layer 2 applies pattern


                                                                                     5
Algorithm 2 Dependency Hallucination Detection                    Algorithm 4 Resource Coherence Detection (RCF)
(DHI)                                                             Require: CFGs F , resource graph R, schema graph S,
Require: Repository 𝑅 with manifests 𝑀, generated code 𝐺              generated code 𝐺
Ensure: Set of dependency hallucination findings 𝐹                Ensure: Set of resource coherence findings 𝐹
 1: 𝐷    ← parse packages from 𝑀 (pyproject.toml,                  1: 𝐹 ← ∅
    requirements.txt, package.json)                                2: for each function 𝑓 in 𝐺 with declared return type 𝑇 do
 2: Extract and validate external imports                          3:   Build intraprocedural CFG; for each path 𝜋 to
 3: 𝐹 ← ∅                                                               exit, if 𝜋 has no return of type 𝑇 and is not
 4: for each import 𝑖 in 𝐺 referencing package 𝑝 do                     exception-terminated, add ( 𝑓 , 𝜋, 𝑇) to 𝐹
 5:   if 𝑝 ∉ stdlib and 𝑝 ∉ local modules and 𝑝 ∉ 𝐷 then           4: end for
 6:      Query registry R (PyPI/npm) for 𝑝                         5: for each resource ref 𝑟 with path 𝑝 in 𝐺 do
 7:      if 𝑝 ∉ R then                                             6:   if ¬exists(resolve( 𝑝, root)) then
 8:         𝐹 ← 𝐹 ∪ {(𝑖, 𝑝, “hallucinated”)}                       7:      𝐹 ← 𝐹 ∪ {(𝑟, 𝑝)}
 9:      else                                                      8:   end if
10:         𝐹 ← 𝐹 ∪ {(𝑖, 𝑝, “undeclared”)}                         9: end for
11:      end if                                                   10: for each consumer access 𝑐. 𝑓 𝑖𝑒𝑙𝑑 produced by model 𝑀
12:   end if                                                          do
13: end for                                                       11:   if 𝑓 𝑖𝑒𝑙𝑑 ∉ fields(𝑀) then
14: return 𝐹                                                      12:      𝐹 ← 𝐹 ∪ {(𝑐, 𝑀, 𝑓 𝑖𝑒𝑙𝑑)}
                                                                  13:   end if
                                                                  14: end for
Algorithm 3 Symbol Resolution (SRF) and Phantom
                                                                  15: return 𝐹
API (PIA) Detection
Require: Import graph I, call graph K, phantom set 𝑃 from
    Algorithm 2                                                     Illustrative Example: hypertropher-app [20]
Ensure: Sets of SRF findings 𝐹𝑆 and PIA findings 𝐹𝑃
 1: 𝐹𝑆 ← ∅, 𝐹𝑃 ← ∅                                                 A Next.js/React web application built with AI coding
 2: for each import edge ( 𝑓 , 𝑚, 𝑠) in I do                       tools and published on GitHub.
 3:   if (𝑚      ∈    𝑃 or ¬resolve(𝑠, 𝑚)) and 𝑚        ∉            72 files analyzed   tsc-strict ✓   SAST ✓   11 structural failures ×
      LocalModulePattern then
 4:      𝐹𝑆 ← 𝐹𝑆 ∪ {( 𝑓 , 𝑚, 𝑠)}                                      BCI — Configuration Incoherence 7 findings
 5:   end if                                                          Four environment variables (NEXT PUBLIC SUPABASE URL,
 6: end for                                                           NEXT PUBLIC SUPABASE ANON KEY,        SUPABASE SECRET API KEY,
                                                                      NEXT PUBLIC GOOGLE MAPS API KEY) accessed without defaults
 7: for each call edge ( 𝑓 , 𝑚.𝑠, args) in K do                       across three Supabase client files and the application layout.
 8:   if 𝑚 ∈ 𝑃 and 𝑚 ∉ LocalModulePattern then                        None declared in any .env or config file. Each resolves to
 9:      𝐹𝑃 ← 𝐹𝑃 ∪ {( 𝑓 , 𝑚, 𝑠, args)}                                undefined at runtime. Invisible to tsc because process.env
                                                                      access is structurally valid regardless of key existence.
10:   end if
11: end for
12: return 𝐹𝑆 , 𝐹𝑃                                                    DHI — Dependency Hallucination 1 finding
                                                                      Import references @vercel/analytics/next, a package absent
                                                                      from package.json. The path alias filter correctly excludes 98
                                                                      @/components/ui/* local aliases, isolating the single genuinely
matching for dead code after terminators, tautological                unresolvable external dependency.
conditions, duplicate handlers, and infinite loops. Layer 3
delegates to pylint/ESLint with post-processing filters
suppressing known false positives from context managers,              RCF — Resource Coherence                           2 findings
                                                                      Functions loadingCities and previewUrl declare return types
generators, and heavy exception scaffolding.                          but contain conditional branches that never return a value.
     Security Structural Regression Detection                         CFG reachability analysis identifies the gaps. The type
                                                                      checker misses these because exception flow masks the
(SSR): Algorithm 7 identifies endpoints lacking                       incomplete returns.
authentication guards present on sibling routes. Routes
are clustered by resource segment, public endpoints are
filtered, and majority-rule analysis flags routes where a             CFC — Control Flow Coherence                        1 finding
                                                                      Dead code after a return statement at line 461. This category
dominant guard (≥90% coverage) is absent on destructive               was absent from all 336 controlled generations yet appears in
HTTP methods (POST, PUT, DELETE, PATCH).                              real-world AI-generated code, consistent with the hypothesis
                                                                      that less supervised generation surfaces failure modes that
Illustrative Example:          We trace a real-world                  controlled experiments do not elicit.
AI-generated repository through the verification pipeline
to illustrate how structural failures manifest and evade           A companion repository, VoiceTradeWithSchwab [21]
standard toolchains.                                               (voice-controlled stock trading, 100% AI-generated
                                                                   Python), exhibits 92 findings across five categories
                                                                   including phantom imports, an infinite loop, and
                                                                   unguarded trading configuration variables.



                                                              6
Algorithm 5 Cross-File Contract Violation Detection                            Algorithm 6 Control Flow Coherence Detection (CFC)
(CCV)                                                                          Require: Generated code files 𝐺, constructed CFGs F
Require: Call graph K, schema graph S, middleware config                       Ensure: Set of control flow findings 𝐹
    M, generated code 𝐺                                                         1: 𝐹 ← ∅
Ensure: Set of contract violation findings 𝐹                                    2: for each file 𝑓 in 𝐺 do
 1: 𝐹 ← ∅                                                                       3:   Graph-based reachability (Layer 1)
 2: for each middleware 𝑚 registered in M do                                    4:   for each function CFG 𝑔 ∈ F ( 𝑓 ) do
 3:   if 𝑚 ∉ import edges of any route module then                              5:      𝑅 ← BFS from entry node of 𝑔
 4:      𝐹 ← 𝐹 ∪ {(𝑚, disconnected)}                                            6:      if all body nodes ∉ 𝑅 then
 5:   end if                                                                    7:         𝐹 ← 𝐹 ∪ {( 𝑓 , 𝑔, “dead function”)}
 6:   if 𝑚 appears >1 time in registration then                                 8:      end if
 7:      𝐹 ← 𝐹 ∪ {(𝑚, duplicate)}                                               9:   end for
 8:   end if                                                                   10:   Pattern-based detection (Layer 2)
 9: end for                                                                    11:   𝐹 ← 𝐹∪ detect dead-code-after-terminator in 𝑓
10: for each cross-file call edge ( 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑟, 𝑐𝑜𝑛𝑠𝑢𝑚𝑒𝑟) in K                   12:   𝐹 ← 𝐹∪ detect tautological conditions in 𝑓
    do                                                                         13:   𝐹 ← 𝐹∪ detect duplicate except/switch-case in 𝑓
11:   𝑆 𝑃 ← output fields of 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑟; 𝑆𝐶 ← accessed fields                    14:   𝐹 ← 𝐹∪ detect infinite loops without exit in 𝑓
      in 𝑐𝑜𝑛𝑠𝑢𝑚𝑒𝑟                                                              15:   SAST delegation (Layer 3)
12:   if ∃ 𝑓 ∈ 𝑆𝐶 : 𝑓 ∉ 𝑆 𝑃 then                                               16:   𝑟 ← invoke pylint/ESLint on 𝑓 (skip if syntax error)
13:      𝐹 ← 𝐹 ∪ {( 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑟, 𝑐𝑜𝑛𝑠𝑢𝑚𝑒𝑟, 𝑆𝐶 \ 𝑆 𝑃 )}                            17:   Remove findings in context manager, generator, or
14:   end if                                                                         heavy try/finally contexts
15: end for                                                                    18:   𝐹 ← 𝐹 ∪𝑟
16: return 𝐹                                                                   19:   Deduplicate 𝐹 by line number (priority: graph >
                                                                                     pattern > SAST)
                                                                               20: end for
5      Evaluation and Results                                                  21: return 𝐹


5.1      Experimental Setup
                                                                               representing static CI checks: type checking (mypy
We evaluate structural failure detection across 336                            [26] and tsc, test execution, SAST via bandit [27]
code generations from two frontier models, GPT-4o                              and semgrep [28], and regex heuristics. Dependency
(2024-08-06, 128K context) and Claude 3.5 Sonnet                               installation is excluded as the evaluation operates on
(2024-10-22, 200K context), both at temperature zero.                          generated code before environment builds; it would catch
The evaluation corpus consists of 10 curated open-source                       at most the 3 DHI findings but none of the remaining 64.
production repositories spanning Python (Django [22],                          Detection metrics include per-category precision against
FastAPI [23]) and TypeScript (Express [24], Next.js [25]),                     ground truth and evasion rates quantifying findings that
selected for active maintenance, with a minimum 50 files                       pass each baseline undetected. Ground truth labels
and 10K LOC, type annotation coverage exceeding 50%,                           were established through two approaches. For categories
test coverage above 60%, and explicit schema definitions.1                     with small finding counts (BCI, DHI, PIA, SRF),
From these repositories, we extract 60 tasks derived                           every finding was manually reviewed and verified as
from merged pull requests and closed issues at three                           a provable constraint violation. For categories with
complexity levels, namely L1 single-file (30 tasks), L2                        larger counts (RCF, CCV), precision was established
multi-file (20 tasks), and L3 cross-cutting (10 tasks). Four                   through iterative pipeline refinement that systematically
prompting strategies control context richness ranging                          eliminated false positive patterns, with boundary cases
from P1 (minimal, task description only) through P2                            resolved by consulting the formal invariants for each
(local, 2–5 same-directory files) and P3 (retrieved, 10                        category.
similarity-ranked files) to P4 (oracle, 5–15 ground-truth
files). The evaluation has a partially unbalanced design
in which 24 early tasks were evaluated with GPT-4o
                                                                               5.2    Results
under P1 and P2 only, while the remaining 36 tasks                             Detection Performance: Table 4 reports detection
received both models across all four strategies, yielding                      results across 336 generations (192 GPT-4o, 144 Claude
192 GPT-4o generations (60 each for P1/P2, 36 each for                         3.5 Sonnet) under four prompting conditions. Our
P3/P4) and 144 Claude generations (36 per strategy).                           framework identifies 67 structural failures across eight
P1 and P2 therefore contain 96 generations each and                            active categories, with 65 (97.0%) invisible to all
P3 and P4 contain 72 each; all analyses use appropriate                        baseline methods. Compilation and type checking detect
denominators to account for this asymmetry.                                    only 2 findings independently (both RCF return-type
     We compare our framework against four baselines,                          violations), while test execution, SAST, and regex
   1 Please refer to [19] for the complete list of curated repositories,       heuristics detect none. By category, RCF accounts for
external validation datasets, and all evaluation metadata.                     the most findings (29), followed by CCV (18), BCI (12),


                                                                           7
Algorithm 7 Security Structural Regression Detection                           across all evaluations. This is consistent with two
(SSR)                                                                          properties of the evaluation corpus. The detector requires
Require: Routing            graph      G        with     routes                route clusters with at least 4 endpoints exhibiting a
    {( 𝑝𝑎𝑡ℎ, 𝑚𝑒𝑡ℎ𝑜𝑑, 𝑔𝑢𝑎𝑟𝑑𝑠)}                                                  dominant per-route guard pattern, and most vibe-coded
Ensure: Set of security regression findings 𝐹                                  projects apply authentication at the framework level
 1: Filter and cluster                                                         (e.g., global middleware, app-level decorators) rather
 2: for each route 𝑟 in G do                                                   than per-route, leaving no inconsistency to detect.
 3:    Assign 𝑟 to cluster 𝐶resource by path segment                           The two highest-finding repositories, hypertropher-app
 4: end for
                                                                               and VoiceTradeWithSchwab (detailed in the Illustrative
 5: Remove clusters matching public whitelist (health, auth,
    docs, webhook, metrics)
                                                                               Example above), exemplify how structural failures cluster
 6: Majority-rule guard analysis                                               and compound in real-world AI-generated code.
 7: 𝐹 ← ∅
 8: for each remaining cluster 𝐶 with |𝐶 | ≥ 4 do
                                                                                   Table 4: Detection results across 336 generations
 9:    𝑔 ∗ ← most common guard in 𝐶
                                                                                Method                         Findings   TP    Precision      Unique
10:    ratio ← |{𝑟 ∈ 𝐶 : 𝑔 ∗ ∈ guards(𝑟)}|/|𝐶 |
                                                                                Type Check/Lint                   2       2        100%          0
11:    if ratio ≥ 0.9 then                                                      Test Execution                    0       0        N/A           0
                                                                                SAST                              0       0        N/A           0
12:        for each route 𝑟 ∈ 𝐶 where 𝑔 ∗ ∉ guards(𝑟) do                        Regex Heuristics                  0       0        N/A           0

13:          if method(𝑟) ∈ {POST, PUT, DELETE, PATCH}                          Patch Work Framework (Ours)       67      67     see text        65

             then
14:             𝐹 ← 𝐹 ∪ {(𝑟, 𝑔 ∗ , 𝐶)}
15:          end if
16:        end for                                                                        Table 5: Per-category detection results
17:    end if                                                                   Category      N    Precision   Baseline   Detection Strategy
18: end for                                                                     RCF           29    Refined      2/29     CFG return-path + schema
                                                                                              18    Refined      0/18     Cross-graph disconnect
19: return 𝐹                                                                    CCV
                                                                                BCI           12     100%        0/12     Unsafe-access + config-space
                                                                                DHI            3     100%         0/3     Registry validation
                                                                                PIA            3     100%         0/3     Cross-graph phantom check
                                                                                SRF            2     100%         0/2     Import + symbol resolution
                                                                                CFC            0     N/A         N/A      Hybrid 3-layer
DHI (3), PIA (3), and SRF (2). Manual validation                                SSR            0     N/A         N/A      Resource-clustered auth

confirms 100% precision for BCI, DHI, PIA, and SRF
(20 of 20 verified as provable constraint violations),                             Model Comparison: Failure distributions diverge
while RCF and CCV precision was established through                            qualitatively between GPT-4o and Claude 3.5 Sonnet
iterative pipeline refinement. No baseline method detects                      as visualized in Figure 3. Overall failure rates are
any CCV, BCI, DHI, PIA, or SRF finding; type                                   comparable (GPT-4o: 39 findings in 25/192 generations,
checkers catch only 2 of 29 RCF findings. Evasion rates                        13.0%; Claude: 28 findings in 17/144 generations, 11.8%),
reinforce this gap: 97.0% of findings evade compilation                        but the models exhibit distinct failure profiles rather
(mypy --strict/tsc --strict), and 100% evade test                              than simply differing in magnitude. GPT-4o produces all
suites and SAST tools.                                                         18 CCV findings and all import-related failures (DHI,
    Two categories, CFC and SSR, produced zero                                 PIA, SRF) exclusively, while Claude generates 22 of 29
findings in the controlled evaluation despite having active                    RCF findings. Both contribute equally to BCI (6 each).
detectors. To determine whether these detectors function                       Chi-squared testing confirms distributional independence
correctly or whether controlled generation simply does not                     (𝜒2 = 25.1, 𝑝 = 2.73 × 10−7 ). With 67 total findings,
elicit these failure modes, we applied the full pipeline to 43                 these patterns are descriptive observations warranting
real-world AI-generated repositories spanning vibe-coded                       replication rather than definitive model characterizations.
projects (Cursor AI, Google Gemini, GitHub Copilot),                               Prompt Sensitivity: Table 6 reports failure counts
GPT-Engineer/Lovable applications, and self-declared                           by prompting strategy. P3 (retrieved context) exhibits
fully AI-generated projects.2 Across 1,581 analyzed files                      the highest count (24) and P1 (minimal) the lowest
the pipeline detected 1,152 findings in 35 of 43 repositories                  (8), indicating that richer context reshapes rather than
(81.4% repo-level incidence), with 474 DHI findings,                           uniformly reduces failure distributions. Notably, BCI
270 RCF findings, 177 PIA findings, 148 BCI findings,                          appears in P1 through P3 but not P4 (oracle), consistent
62 SRF findings, 16 CFC findings (6 duplicate switch                           with ground-truth files helping models identify correct
cases, 2 dead-code-after-return, 2 infinite loops), and                        configuration variables. L3 (cross-cutting) tasks exhibit
5 CCV findings. The CFC findings confirm that the                              44.6% finding incidence compared to 16.1% for L1
hybrid three-layer detector functions correctly; controlled                    and 13.4% for L2, confirming that tasks spanning
frontier generation with explicit task specifications simply                   configuration, middleware, and schema boundaries are
does not produce the unstructured code patterns that                           substantially more failure-prone. Figure 4 shows how
trigger control flow failures. SSR remained at zero                            failure category composition shifts across complexity
   2 Please refer to [19] for the complete list of all repositories with       levels, with BCI and CCV concentrated in L3 tasks
per-repo metadata and finding counts.                                          that require cross-layer reasoning.


                                                                           8
                                                                                                                                                             RCF
         SRF                                         2                                                      L1 Single-file (N=168)
                                                                                                                                                              21




         PIA                                             3                                                   L2 Multi-file (N=112)
                                                                                                                                                      CCV
                                                                                                                                                       8
                                                                                                                                                                                           BCI
                                                                                                                                                                                            4



         DHI                                             3
                                                                                                           L3 Cross-cutting (N=56)
                                                                                                                                         RCF                         CCV                              BCI
                                                                                                                                          7                           10                               8



         BCI                           6                          6                                                                  0         20             40                     60          80           100

                                                                                                                                                               Failure composition (%)

                                                                                                                                                RCF    CCV            BCI            DHI   PIA          SRF
         RCF   22                                                     7


         CFC

         CCV                                                                            18
                                                                                                  Figure 4: Failure category composition by task
         SSR
                      GPT-4o                                                                      complexity level.
                      Claude


                    −20   −15   −10        −5    0           5            10       15    20
                                      Finding Count                                               CI integration and developer review workflows, providing
                                                                                                  actionable diagnostics rather than opaque pass/fail
Figure 3: Model divergence in structural failure categories.                                      signals.
Bars extend left for GPT-4o and right for Claude 3.5
Sonnet.
                                                                                                  6    Conclusion
  Table 6: Findings by prompt strategy and category                                               This work formalized the patchwork problem in
                    Category          P1        P2       P3                P4
                                                                                                  LLM-generated code through a graph-based failure
                    RCF               0         8            13                8
                    CCV               4         5             5                4                  taxonomy and a hybrid verification framework combining
                    BCI               4         2             6                0
                    DHI               0         1            0                 2                  mature static analysis tools with purpose-built detectors.
                    PIA               0         1             0                2
                    SRF               0         0            0                 2                  Across controlled generations and real-world repositories,
                    Total             8         17           24            18                     the overwhelming majority of detected structural failures
                                                                                                  evade type checking, testing, and SAST entirely, and
                                                                                                  failure patterns diverge qualitatively between models.
     Runtime: The pipeline analyzes each file in a median                                         Our future work will focus on extending the framework
of 47 ms end-to-end (graph construction through all                                               to additional models and programming languages
seven detectors), with a 120-second timeout per external                                          and on subjecting the categories currently validated
analysis script. Registry validation queries (PyPI/npm)                                           through iterative refinement to independent precision
are cached across runs. The largest repository in Track D                                         audits. Further directions include repair mechanisms
(435 files, 70K LOC) completes in 233 seconds. Runtime                                            that leverage detected constraint violations to prompt
is dominated by graph construction (99.8% of per-file                                             for missing declarations, and integration into agentic
time); all detectors combined complete in under 1ms per                                           coding workflows and continuous integration pipelines
file. These times indicate the framework is practical as a                                        where incremental patch review replaces complete-file
CI integration for repositories of moderate size.                                                 generation.

5.3    Practical Implications
                                                                                                  References
These findings have direct consequences for teams
adopting LLM-generated code. First, standard CI                                                    [1] J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim, “A
pipelines (type checking, testing, SAST) are insufficient                                              survey on large language models for code generation,”
as quality gates for generated code; 97% of detected                                                   ACM Transactions on Software Engineering and
failures pass all four baselines, meaning structurally                                                 Methodology, vol. 35, p. 1–72, Jan. 2026.
broken code can merge undetected. Teams relying
solely on existing toolchains face a growing blind spot                                            [2] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P.
as LLM-generated code volume increases. Second, the                                                    de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda,
qualitative divergence between models suggests that                                                    N. Joseph, G. Brockman, A. Ray, R. Puri,
switching or combining models does not uniformly                                                       G. Krueger, M. Petrov, H. Khlaaf, G. Sastry,
reduce risk; different models produce different failure                                                P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov,
profiles, and mitigation strategies should be model-aware.                                             A. Power, L. Kaiser, M. Bavarian, C. Winter,
Third, the concentration of failures in L3 cross-cutting                                               P. Tillet, F. P. Such, D. Cummings, M. Plappert,
tasks (44.6% incidence versus 13–16% for simpler                                                       F. Chantzis, E. Barnes, A. Herbert-Voss, W. H.
tasks) indicates that structural verification is most                                                  Guss, A. Nichol, A. Paino, N. Tezak, J. Tang,
critical for tasks spanning configuration, routing, and                                                I. Babuschkin, S. Balaji, S. Jain, W. Saunders,
schema boundaries, precisely the tasks where LLMs                                                      C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra,
are increasingly deployed. The framework’s localized                                                   E. Morikawa, A. Radford, M. Knight, M. Brundage,
evidence traces are designed to support both automated                                                 M. Murati, K. Mayer, P. Welinder, B. McGrew,
                                                                                                       D. Amodei, S. McCandlish, I. Sutskever, and


                                                                                              9
    W. Zaremba, “Evaluating large language models                 [12] C. Shen, C. Dilgren, P. Chiniya, L. Griffith, Y. Ding,
    trained on code,” 2021.                                            and Y. Chen, “Secrepobench: Benchmarking code
                                                                       agents for secure code completion in real-world
 [3] Y. Li, D. Choi, J. Chung, N. Kushman,                             repositories,” 2026.
     J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling,
     F. Gimeno, A. Dal Lago, T. Hubert, P. Choy,                  [13] J. Chen, H. Huang, Y. Lyu, J. An, J. Shi, C. Yang,
     C. de Masson d’Autume, I. Babuschkin, X. Chen,                    T. Zhang, H. Tian, Y. Li, Z. Li, X. Zhou, X. Hu,
     P.-S. Huang, J. Welbl, S. Gowal, A. Cherepanov,                   and D. Lo, “SecureVibeBench: Benchmarking
     J. Molloy, D. J. Mankowitz, E. Sutherland Robson,                 secure vibe coding of AI agents via reconstructing
     P. Kohli, N. de Freitas, K. Kavukcuoglu, and                      vulnerability-introducing scenarios,” in Proceedings
     O. Vinyals, “Competition-level code generation with               of the 64th Annual Meeting of the Association
     alphacode,” Science, vol. 378, p. 1092–1097, Dec.                 for Computational Linguistics (Volume 1: Long
     2022.                                                             Papers) (M. Liakata, V. P. Moreira, J. Zhang,
                                                                       and D. Jurgens, eds.), (San Diego, California,
 [4] J. Austin, A. Odena, M. Nye, M. Bosma,                            United States), pp. 24144–24168, Association for
     H. Michalewski, D. Dohan, E. Jiang, C. Cai,                       Computational Linguistics, July 2026.
     M. Terry, Q. Le, and C. Sutton, “Program synthesis
     with large language models,” 2021.                           [14] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret,
                                                                       S. Yao, K. Narasimhan, and O. Press, “Swe-agent:
 [5] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei,                Agent-computer interfaces enable automated
     O. Press, and K. R. Narasimhan, “SWE-bench: Can                   software engineering,” 2024.
     language models resolve real-world github issues?,”
     in The Twelfth International Conference on Learning          [15] X. Wang, Y. Wang, Y. Wan, J. Wang, P. Zhou,
     Representations, 2024.                                            L. Li, H. Wu, and J. Liu, “Code-mvp: Learning
                                                                       to represent source code from multiple views
 [6] Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma,                        with contrastive pre-training,” in Findings of the
     W. Zhong, J. Chen, M. Mao, and Z. Zheng, “Llm                     Association for Computational Linguistics: NAACL
     hallucinations in practical code generation:                      2022, 2022.
     Phenomena,       mechanism,     and mitigation,”
     Proceedings of the ACM on Software Engineering,              [16] Z. Zhang, H. Yu, S. Li, P. Di, J. Li, and R. Wang,
     vol. 2, no. ISSTA, pp. 481–503, 2025.                            “Galla: Graph aligned large language models for
                                                                       improved source code understanding,” in Proceedings
 [7] T. Liu, C. Xu, and J. McAuley, “Repobench:                        of the 63rd Annual Meeting of the Association for
     Benchmarking repository-level code auto-completion                Computational Linguistics (ACL 2025), 2025.
     systems,” in International Conference on Learning
     Representations, vol. 2024, pp. 47832–47850, 2024.           [17] Y. Fu, E. Baker, Y. Ding, and Y. Chen, “Constrained
                                                                       decoding for secure code generation,” 2024.
 [8] F. Yamaguchi, N. Golde, D. Arp, and K. Rieck,
    “Modeling and discovering vulnerabilities with code           [18] X. Li, J. Ding, C. Peng, B. Zhao, X. Gao, H. Gao,
     property graphs,” in 2014 IEEE symposium on                       and X. Gu, “Safegenbench: A benchmark framework
     security and privacy, pp. 590–604, IEEE, 2014.                    for security vulnerability detection in llm-generated
                                                                       code,” arXiv preprint arXiv:2506.05692, 2025.
 [9] J. Spracklen, R. Wijewickrama, A. N. Sakib,
     A. Maiti, and B. Viswanath, “We have a package               [19] V. Mothukuri, “Source code of the paper: The
     for you! a comprehensive analysis of package                      patchwork problem in llm-generated code.” https:
     hallucinations by code generating {LLMs},” in 34th                //github.com/decentralizedsciencelab/Patch
     USENIX Security Symposium (USENIX Security 25),                   Work.git, 2026. Source code, evaluation pipelines,
     pp. 3687–3706, 2025.                                              detection configurations, and datasets.
[10] J. Li, G. Li, X. Zhang, Y. Dong, and Z. Jin,                 [20] wowashuwow, “hypertropher-app.” https://gith
    “Evocodebench: An evolving code generation                         ub.com/wowashuwow/hypertropher-app, 2025.
     benchmark aligned with real-world code repositories,”
     2024.                                                        [21] BSalita, “VoiceTradeWithSchwab.” https://gith
                                                                       ub.com/BSalita/VoiceTradeWithSchwab, 2025.
[11] M. Vero, N. Mündler, V. Chibotaru, V. Raychev,
     M. Baader, N. Jovanović, J. He, and M. Vechev,              [22] Django Software Foundation, “Django: The web
    “Baxbench: Can LLMs generate correct and                           framework for perfectionists with deadlines.” https:
     secure backends?,” in Forty-second International                  //www.djangoproject.com, 2024. Version 5.0.
     Conference on Machine Learning, 2025.                        [23] S.    Ramı́rez,    “FastAPI:     Modern,       fast
                                                                       (high-performance) web framework for building APIs


                                                             10
    with Python.” https://fastapi.tiangolo.com,
    2024. Version 0.110.
[24] OpenJS Foundation, “Express: Fast, unopinionated,
     minimalist web framework for Node.js.” https://
     expressjs.com, 2024. Version 4.x.

[25] Vercel, “Next.js: The React framework for the web.”
     https://nextjs.org, 2024. Version 14.
[26] mypy, “mypy: Optional static typing for Python.”
     https://mypy-lang.org, 2024. Version 1.8.

[27] PyCQA, “Bandit: A tool designed to find common
     security issues in Python code.” https://bandit.r
     eadthedocs.io, 2024. Version 1.7.
[28] Semgrep, Inc., “Semgrep: Lightweight static analysis
     for many languages.” https://semgrep.dev, 2024.
     Open-source edition.




                                                            11
