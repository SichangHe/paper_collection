                                                 A XLE: A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities


                                               Jimmy Xin 1 Alex Schneidman 2 † Chris Cummins 3 † Karun Ram 1 Srihari Ganesh 1 Jannis Limperg 1


                                                                    Abstract                                   for formalization. L EAN 4 has also emerged as the language
                                                                                                               of choice for AI-driven mathematics: AlphaProof (Hubert
                                               We present A XLE (Axiom Lean Engine), a cloud                   et al., 2025), DeepSeek-Prover (Ren et al., 2025), Kimina-
                                               service for L EAN 4 proof manipulation, extrac-                 Prover (Wang et al., 2025), Seed-Prover (Chen et al., 2025),
                                               tion, and verification. Recent progress in AI for
arXiv:2606.26442v1 [cs.LO] 24 Jun 2026




                                                                                                               Aristotle (The Harmonic Team, 2025), Leanstral (Mistral
                                               mathematics—reinforcement learning pipelines,                   AI, 2026), and more all use L EAN 4 as their formal backend.
                                               agentic proving workflows, dataset curation—                    These efforts—spanning model training, reinforcement-
                                               demands L EAN 4 tooling that scales to millions                 learning pipelines, agentic proving workflows, and dataset
                                               of requests while remaining correct and robust;                 curation—share a common need for L EAN 4 tooling that is
                                               existing infrastructure offers parallel compilation             not only fast and correct, but that supports the high concur-
                                               but not scalable proof verification, higher-level               rency these workloads require.
                                               proof manipulation, multi-version support, or per-
                                               request isolation at the throughput modern AI                   Several prior systems provide infrastructure for interacting
                                               workflows require. A XLE provides 14 L EAN 4                    with L EAN 4 at scale (§6). However, these efforts have vari-
                                               metaprogramming tools spanning strict proof ver-                ous limitations in scope. First, compilation is not verifica-
                                               ification, declaration metadata extraction, seman-              tion: A passing compile accepts proofs containing sorry,
                                               tic source manipulation, lemma extraction, and                  unsound axioms, or incorrectly restated theorems—all com-
                                               deterministic proof repair and simplification. The              mon failure modes in AI-generated proofs. Strict verifica-
                                               service runs as a multi-tenant cloud deployment                 tion techniques exist (Lean FRO, 2023; 2025; GasStation-
                                               with per-request isolation and concurrent sup-                  Manager, 2025), but no prior system makes them available
                                               port for multiple L EAN 4 and M ATHLIB ver-                     as a fast, scalable cloud service. Second, prior work lacks
                                               sions, accessible via a Python SDK, command-                    additional higher-level manipulation primitives and meta-
                                               line interface, web UI, MCP server, and HTTP                    data extraction that agentic and dataset-curation workloads
                                               API. A XLE is publicly available and free to use                depend on, all of which require custom functionality im-
                                               at https://axle.axiommath.ai and via                            plemented in L EAN’s metaprogramming framework. Third,
                                               the axiom-axle PyPI package, with no local                      shared-process architectures risk state leakage and crash
                                               L EAN 4 installation required. It has served over               propagation across requests. Fourth, most infrastructure is
                                               500 million requests to date and is the underlying              pinned to a single L EAN 4 or M ATHLIB version, whereas
                                               infrastructure for Axiom Math’s proving efforts,                AI systems frequently target multiple versions for training
                                               including its 12/12 score on the 2025 Putnam                    data from different eras or for cross-version compatibility.
                                               competition.                                                    Finally, existing systems do not offer elastic scalability un-
                                                                                                               der a simple interface: automatically scaling capacity up
                                                                                                               during training runs and down during idle periods, with load
                                         1. Introduction                                                       balanced across workers.
                                                                                                               A XLE (Axiom Lean Engine) was built to address these gaps.
                                         L EAN 4 (de Moura & Ullrich, 2021) is a programming lan-
                                                                                                               It provides 14 L EAN 4 metaprogramming tools, served from
                                         guage and proof assistant in which users write programs and
                                                                                                               a hosted multi-tenant cloud deployment with per-request
                                         proofs together, with correctness guaranteed by a dependent
                                                                                                               isolation and concurrent support for multiple L EAN 4 ver-
                                         type system. Its community-driven mathematics library,
                                                                                                               sions. A XLE has been deployed in production, including as
                                         M ATHLIB (The mathlib Community, 2020), contains over
                                                                                                               the underlying infrastructure for Axiom Math’s 12/12 score
                                         250,000 formal theorems and has become a central resource
                                                                                                               on the 2025 Putnam competition and autoformalizations
                                           †
                                             Work done while at Axiom Math. 1 Axiom Math 2 Thinking            of Fel’s conjecture on numerical semigroups (Chen et al.,
                                         Machines Lab 3 Recursive Superintelligence, Inc. Correspondence       2026b) and the partial-regularity-of-primes result related to
                                         to: Jimmy Xin <axle@axiommath.ai>.                                    Vandiver’s conjecture (Chen et al., 2026a), among others.
                                         Preprint. June 26, 2026.                                              The service is free and publicly accessible; Appendix D

                                                                                                           1
                            A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

collects the relevant resource URLs, installation commands,          or restated theorems would teach the policy to game the
and support channels.                                                reward (see Appendix C). Per-request isolation is equally
                                                                     important, since a malformed candidate must not corrupt
Our contributions are:
                                                                     subsequent verifications on the same worker. A XLE’s strict-
                                                                     verification tool verify_proof (§4) and its per-request
 1. Complete suite of proof-manipulation tools. A XLE                isolation directly target this regime, and the service handles
    provides 14 metaprogramming tools, each imple-                   the concurrent verification load these rollouts produce. Raw
    mented as a L EAN 4 metaprogram: strict proof ver-               speed matters too: A typical verification completes well
    ification, declaration metadata extraction, semantic             under a second, keeping step-level rollout times bounded
    source manipulation, lemma extraction, and determin-             even with thousands of parallel candidates. Importantly,
    istic proof repair and simplification.                           verify_proof adds little overhead beyond plain compi-
 2. Strict proof verification at scale.          A XLE’s             lation, so the strictness checks do not penalize throughput.
    verify_proof rejects candidates containing
    sorry, non-whitelisted axioms, or signature                      2.2. Agentic Proving
    mismatches—failure modes that are common in                      A second class of workloads is agentic pipelines (Thakur
    AI-generated proofs and that plain compilation                   et al., 2024; Ospanov et al., 2025; Varambally et al., 2025;
    accepts. A XLE makes strict L EAN 4 proof verification           Math Inc., 2025; Liu et al., 2026), in which an LLM itera-
    available at production throughput rather than as a              tively proposes, inspects, and refines proof candidates. A
    single-process command-line tool.                                single attempt may involve dozens of turns: Propose a proof,
 3. Multi-environment support. A single A XLE endpoint               verify it, inspect errors or remaining goals, extract those
    serves multiple L EAN 4 and M ATHLIB versions con-               goals as standalone lemmas, attempt them recursively, repair
    currently, enabling cross-version compatibility checks           localized failures, and merge the resulting fragments into a
    and seamless support for models targeting different              complete proof. These workflows demand a richer toolkit
    L EAN 4 versions.                                                than verification alone—lemma extraction from sorry po-
                                                                     sitions and elaboration errors, declaration metadata and de-
 4. Free public cloud service. A XLE is deployed as a free,          pendency analysis for retrieving relevant context, merging
    publicly accessible cloud service with per-request isola-        of partial proofs from parallel attempts, and deterministic
    tion and automatic retries; users access it through a web        repair of common errors in LLM-generated drafts. Sitting
    UI at https://axle.axiommath.ai, a Python                        inside the agent’s inner loop, the tools must be fast, robust,
    SDK and CLI via the axiom-axle PyPI package, an                  and stable; they must be invoked dozens of times per attempt
    MCP server, and an HTTP API, none of which require               without bottlenecking the agent or producing spurious errors
    a local L EAN 4 installation.                                    that are uninterpretable to an LLM. Appendix B demon-
                                                                     strates one such decompose-solve-merge loop end-to-end
                                                                     on a non-trivial L EAN 4 lemma.
2. Motivating Applications
A XLE serves the proof-engineering needs of AI-driven                2.3. Dataset Curation and Filtering
L EAN 4 mathematics. Although the tools and infrastructure
are general, the principal workloads fall into three cate-           A third class of workloads is the construction and filtering
gories: reinforcement learning and model training, agentic           of training datasets from existing L EAN 4 corpora such as
proving, and dataset curation. Each places distinct demands          M ATHLIB. Common operations include extracting theorem-
on A XLE’s tools, latency profile, and scalability; subsequent       level metadata in bulk, filtering by structural properties (de-
sections describe the tools and infrastructure that meet them.       pendency complexity, proof length, tactic usage), deduplicat-
                                                                     ing across multiple sources, and normalizing or simplifying
                                                                     statements for downstream consumption. These workloads
2.1. Reinforcement Learning and Model Training
                                                                     are throughput-bound rather than latency-bound—a single
Reinforcement learning over formal proofs has become a               build may issue millions of requests over hours or days—
central paradigm for training L EAN 4 proving models (Hu-            and can span multiple L EAN 4 and M ATHLIB versions,
bert et al., 2025; Ren et al., 2025; Wang et al., 2025; Chen         since training corpora are often pinned to specific releases
et al., 2025; The Harmonic Team, 2025). A typical RL                 or built across version boundaries. A XLE’s high request
step samples thousands of candidate proofs from a policy,            throughput, concurrent multi-version support, and metadata-
evaluates each, and uses the outcome as a reward signal.             and dependency-extraction tools are aimed at this workload.
This workload bursts at each rollout boundary into a flood
of concurrent verification requests, and demands strict cor-
rectness: A verifier that accepts sorry, unsound axioms,

                                                                 2
                             A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

3. Service Overview                                                  4. Tools
A XLE is a hosted, multi-tenant cloud service. A client issues       All of A XLE’s tools are implemented as L EAN metapro-
a tool request—a tool name, an input payload, and a target           grams operating on parsed and elaborated L EAN syntax.
L EAN 4 environment—to A XLE’s HTTPS endpoint, and                   This section walks through the principal tools; a complete
receives a JSON response with the tool’s structured output.          summary is given in Table 1, and per-tool reference docu-
Authentication is by API key. No local L EAN 4 installation          mentation is available online.1
is required.
                                                                     4.1. Compilation Checking and Proof Verification
3.1. Client Surfaces
                                                                     The simplest tool is check, which compiles a L EAN file
Clients reach A XLE through any of five interchangeable              and reports any errors, warnings, and linter messages. Its
methods for submitting JSON-encoded tool calls: a Python             strict counterpart, verify_proof, takes a candidate file
SDK and a command-line interface, both distributed via               and a separate formal statement file defining the theorems to
the axiom-axle PyPI package; an MCP server dis-                      be proved, and accepts the candidate only if its declarations
tributed via axiom-axle-mcp (or hosted at https:                     match the formal statements and constitute a valid proof.
//mcp.axiommath.ai) for agent integrations; a hosted
                                                                     Compilation alone is frequently unsuitable for AI-generated
web UI at https://axle.axiommath.ai; and the
                                                                     proof workloads. L EAN 4 permits user-defined macros,
underlying HTTPS API.
                                                                     custom tactics, metaprograms, and new axioms; the same
                                                                     features that make L EAN expressive also create many ways
3.2. Multi-Version Environments                                      for a file to compile without proving the intended statement.
Each request carries an environment field that selects a             The verify_proof tool rejects any declarations that:
particular L EAN 4 version paired with a M ATHLIB snapshot
and any project-specific pre-built dependencies. A single               • contain sorry;
A XLE deployment serves multiple environments concur-
                                                                        • use any axiom outside the small whitelist of
rently behind the same endpoint, which AI workloads use
                                                                          known-consistent axioms shipped in the L EAN
for cross-version compatibility checks, evaluation against
                                                                          standard library (propext,      Quot.sound,
legacy proofs, and serving models trained against different
                                                                          Classical.choice);
M ATHLIB eras. The available environments are exposed
by the API; by default, the public tier serves a range of re-           • have a type which does not match the formal state-
cent L EAN 4–M ATHLIB release snapshots, with additional                  ment (e.g., the candidate proves a weakened or restated
custom environments available on request.                                 version of the theorem);

3.3. Per-Request Isolation                                              • are marked unsafe, and can therefore use kernel-
                                                                          bypassing primitives such as unsafeCast.
Each request runs in its own sandboxed process. State a
request mutates—loaded definitions, set options, registered          A XLE intentionally does not defend against certain rare
attributes, allocated memory—does not persist into any later         classes of adversarial inputs, prioritizing performance
request, and a crash or runaway elaboration in one request           over maximal strictness. Several existing tools pro-
does not affect concurrent or subsequent requests. The               vide stronger forms of strict proof verification, including
sandbox additionally blocks network access and prevents              lean4checker (Lean FRO, 2023), Comparator (Lean
the candidate from writing to the filesystem—useful for              FRO, 2025), and SafeVerify (GasStationManager, 2025).
AI-generated input that may contain unbounded loops or               For scalability, verify_proof assumes that every decla-
unintended side effects.                                             ration in the loaded L EAN environment was added through
                                                                     L EAN’s normal kernel-checked elaboration path: it does not
3.4. Scaling and Reliability                                         re-verify the environment from scratch and hence does not
                                                                     defend against inputs that use L EAN metaprogramming to
A XLE scales in response to sustained load and uses queue-
                                                                     install unchecked declarations directly into the environment
ing to absorb short request bursts from existing capacity.
                                                                     and make invalid proofs appear valid. For the typical case
Per-request wall-clock timeouts are configurable by the
                                                                     of AI-generated proofs this is rarely an issue (§5.2), and
caller, up to a service-wide cap; transient infrastructure
                                                                     verify_proof is substantially faster and more scalable
failures (worker crashes, network errors) trigger automatic
                                                                     than the alternatives, as Section 5 discusses. Appendix C
retries without surfacing to the client. Per-API-key fair-
                                                                     gives concrete examples for this discussion.
share queueing ensures one heavy caller cannot starve other
tenants on the deployment.                                              1
                                                                            https://axle.axiommath.ai/v1/docs/

                                                                 3
                             A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

4.2. Declaration Extraction                                            ifiers from a removed section. Other transformations in-
                                                                       clude theorem2lemma, which swaps the theorem key-
extract_decls extracts structured metadata for every
                                                                       word for lemma (and vice versa), and theorem2sorry,
declaration in a file—theorems, definitions, structures, in-
                                                                       which replaces proofs with sorry stubs while leav-
stances, and so on. Its principal output for each decla-
                                                                       ing statements intact. Several of these (for example,
ration is a self-contained L EAN snippet that includes the
                                                                       theorem2sorry and normalize) are routine building
declaration together with all its transitive dependencies
                                                                       blocks in dataset-preparation pipelines: theorem2sorry
within the file, ready to compile in isolation. Alongside
                                                                       turns finished proofs into sorry-stubbed problem statements,
this, extract_decls returns per-declaration metadata:
                                                                       and normalize standardizes surface syntax across cor-
name, kind, signature, body, source-line range, a stable type
                                                                       pora before training.
hash, whether the declaration contains sorry, lightweight
statistics such as proof length and tactic counts, any L EAN-
                                                                       4.5. Lemma Extraction
emitted messages, and dependency information at three
levels: type (constants appearing in the stated type), value           have2lemma and sorry2lemma lift proof obligations
(constants in the elaborated body, including intermediate              from inside a partial proof into standalone top-level lemmas.
constants used by the elaborator during proof construction),           The mechanism is built on M ATHLIB’s extract_goal
and syntactic (constants the source code names literally).             tactic: At the target location—an unresolved have for
Dataset pipelines use extract_decls to turn a multi-                   have2lemma, an explicit sorry or the position of an
declaration file into one standalone snippet per declaration;          elaboration error for sorry2lemma—the tool captures
agents use it to isolate the chunk of a larger file they need to       the proof state, generalizes over its local context, and emits
work on.                                                               a fresh lemma whose statement equals the captured goal.
                                                                       The extracted lemma is callsite-reconstructable: A XLE can
4.3. Semantic Merge
                                                                       additionally rewrite the original proof to invoke the new
merge is the inverse of extract_decls: It takes a col-                 lemma in place of the original obligation, with the cor-
lection of L EAN source fragments and combines them into               rect arguments supplied. A separate transformation tool,
a single compilable file. Naïve concatenation does not work            have2sorry, replaces have steps with sorry stubs
in general—declarations must appear in dependency order,               without extracting a lemma; it is useful for sketching proof
duplicate declarations must be unified, and name conflicts             outlines that subsequent calls fill in. An agent stuck on a
must be resolved.                                                      proof step uses have2lemma or sorry2lemma to isolate
                                                                       the obligation, solves the resulting lemma independently,
merge handles each. Duplicate declarations are detected by
                                                                       and optionally reassembles the pieces with merge.
α-equivalence of types, optionally using definitional equal-
ity. Among duplicates, merge keeps a single compiling                  We note that due to bugs and limitations in existing utilities
representative—that also has only compiling dependencies—              like extract_goal, this tool, and several others, may
if one exists; otherwise it keeps one invalid representative.          fail on certain inputs. More details on the failure modes can
Surviving declarations are then topologically sorted by their          be found in the documentation.
dependencies. When two declarations share a name but their
types do not match, the conflict is resolved by renaming one           4.6. Proof Optimization
of them and updating references using A XLE’s rename
tool.                                                                  simplify_theorems and repair_proofs trans-
                                                                       form existing proofs through pipelines of small, determin-
A typical application is combining proof fragments from                istic passes—simplify_theorems to tidy up a com-
multiple AI candidates into a single compiling file—a rou-             piling proof, repair_proofs to coax a failing one into
tine operation in agentic workflows.                                   compiling.
                                                                       simplify_theorems prunes structure the proof does
4.4. File- and Theorem-Level Transformations
                                                                       not actually use, like tactics flagged as unused or unreach-
A XLE exposes a family of source-level transformations.                able by L EAN’s linters, and have steps whose hypothesis
Among these are rename, which renames a declaration                    is never referenced. The pipeline iterates to a fixed point,
and propagates the change to every reference site—handling             with each pass surfacing new opportunities for the next; if
namespace resolution, dot notation, constructor projections,           any pass introduces an error, the iteration is rolled back, so
and named structure fields—and normalize, which ex-                    the tool never breaks a working proof.
pands abbreviated names, unfolds notation, and removes
                                                                       repair_proofs targets common failure modes in AI-
section and namespace blocks while preserving com-
                                                                       generated drafts by attempting to prove residual un-
pile semantics like maintaining noncomputable mod-
                                                                       proven goals, truncating proofs when there are no

                                                                   4
                              A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

Tool                         Output                                        5.1. Latency and Throughput on a Single Machine
check                        errors, warnings, linter messages             Table 2 compares A XLE to two alternatives on a randomly-
verify_proof                 verification pass/fail, failed declara-
                             tions
                                                                           sampled 5,000-proof check workload from the Goedel
extract_decls                per-declaration metadata, dependen-           workbook dataset: Kimina Lean Server (Dos Santos et al.,
                             cies, standalone snippets                     2025)—a long-running L EAN REPL pool—and a baseline
merge                        merged compilable file with conflicts         that spawns a fresh L EAN process per request. All three run
                             resolved                                      at concurrency 8 on a single r7a.2xlarge AWS instance
normalize                    normalized source preserving seman-
                             tics
                                                                           (8 vCPU, 64 GiB), with a 150 s per-request budget.
rename                       file with renames applied and refer-          All three systems return the same verdict on every one of
                             ences updated
repair_proofs                repaired file with unfixable goals left
                                                                           the 5,000 proofs (Table 2). On throughput, raw L EAN is
                             as-is                                         about 2× slower than the other two: it pays the full cold-
simplify_theorems            file with unused tactics and hypothe-         start cost on each request of reloading M ATHLIB modules,
                             ses pruned                                    which dominates when the median proof needs less than
disprove                     counterexample or proof of negation           a second of actual elaboration. A XLE and Kimina both
theorem2sorry                file with proofs replaced by sorry
theorem2lemma                file with theorem swapped for
                                                                           keep M ATHLIB preloaded and avoid paying the start-up
                             lemma                                         cost. Kimina is marginally faster (0.75 s vs. 1.05 s latency,
have2lemma                   top-level lemmas extracted from               2.13 req/s vs. 2.09 req/s throughput). This gap comes from
                             have positions                                A XLE’s per-request isolation (§3): every request runs in
have2sorry                   file with have steps replaced by              a sandboxed worker process, which adds overhead, while
                             sorry
sorry2lemma                  top-level lemmas extracted from
                                                                           Kimina dispatches into a warm REPL from a long-running
                             sorry positions                               pool. Appendix A.2 reports an A XLE-only concurrency
Table 1. Complete list of A XLE’s tools and their primary outputs.         scaling experiment on the same workload.

                                                                           5.2. verify_proof vs. Strict Proof Checkers
                                                                           verify_proof is one of several published tools that
                                                                           aim to perform strict proof checking in L EAN 4: Given
                                                                           a candidate and a formal statement, decide whether
                                                                           the candidate proves the statement. We compare it
                                                                           against Comparator (Lean FRO, 2025) and SafeVer-
goals remaining, attempting to replace unsafe con-                         ify (GasStationManager, 2025) on a set of 1,000 produc-
structs that verify_proof would reject (like the                           tion verify_proof requests, running each alternative on
native_decide tactic), and cleaning up cross-version                       the same r7a.4xlarge (16 vCPU, 128 GiB) at concur-
porting issues such as set_option commands naming                          rency 4. The per-request budget is 600 s.
options that no longer exist.
                                                                           Speed. Table 3 reports the per-request median latency,
                                                                           aggregate throughput, total wall time, and success rate.
5. Evaluation                                                              verify_proof’s median is sub-second, roughly 10×
We evaluate two aspects of A XLE’s design: per-request                     faster than SafeVerify and 99× faster than Comparator at
cost and aggregate throughput against alternative ways                     the median. The throughput gap is dominated by each alter-
to run L EAN at scale (§5.1), and strict-proof-verification                native’s per-request defense work. In addition to reloading
quality and speed against other published strict check-                    imports on every request, both Comparator and SafeVerify
ers (§5.2). The throughput workload is drawn from the                      run an environment replay step that re-typechecks each dec-
public banach1729/goedel-workbook-lean427                                  laration to verify its soundness, and they include additional
dataset (banach1729, 2026), a set of Lean Work-                            safeguards such as sandboxing, rebuilding expressions, and
book competition-math proofs pinned to L EAN 4.27.0.                       detecting suspicious use of Nat literals. verify_proof
The strict-checker comparison uses an internal paired                      trusts that constants were added through the standard kernel-
verify_proof corpus drawn from production traffic.                         checked elaboration path (§4, Appendix C) and so does not
To keep the candidate set identical across systems on the                  re-check the environment. verify_proof finishes the
throughput workload, every request’s import block is nor-                  workload at 0.43 req/s, while SafeVerify runs at 0.107 req/s
malized to a single import Mathlib; candidates with                        and Comparator at 0.026 req/s.
non-Mathlib dependencies are dropped (discussed as a lim-                  Agreement. A XLE and Comparator agree on every one of
itation in §7). Additional experiments are in Appendix A,                  the 938 conclusive pairs (Table 4). The remaining 62 are
with setup details in §A.1.

                                                                       5
                               A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

        system                                         median latency        p90 latency    throughput    total wall    verdict counts
        A XLE                                                    1.05 s            5.96 s   2.09 req/s         2389 s   4708 / 287 / 5
        Kimina Lean Server (Dos Santos et al., 2025)             0.75 s            6.38 s   2.13 req/s         2351 s   4708 / 287 / 5
        L EAN invoked directly (no shared M ATHLIB)              5.14 s            9.81 s   1.03 req/s         4873 s   4708 / 287 / 5
Table 2. Per-request latency and aggregate throughput on a 5,000-proof check workload from the Goedel workbook dataset, at
concurrency 8 on a single r7a.2xlarge. “Verdict counts” is pass / fail / timeout at the 150 s budget. All three systems return the same
verdict on every one of the 5,000 proofs.


                    system                                    median latency        throughput    total wall     success
                    A XLE verify_proof                                    0.97 s     0.43 req/s     9,205 s      100.0%
                    SafeVerify (GasStationManager, 2025)                  10.1 s    0.107 req/s    37,258 s       99.9%
                    Comparator (Lean FRO, 2025)                           95.7 s    0.026 req/s   151,267 s       93.8%
Table 3. Per-request median latency and aggregate throughput on 1,000 paired production verify_proof requests; all three systems
use the same instance at the same concurrency (Appendix A.1). “Success” is the share of requests that produce an accept-or-reject verdict
within the 600 s per-request budget; the remaining are heavier candidates that exhaust the budget.



Comparator-side timeouts at the 600 s budget: Comparator’s                these provide a scalable hosted service, isolation between
median latency is 95.7 s and its slowest candidates cross 10              requests, multi-version support, or anything beyond compi-
minutes. A XLE and SafeVerify agree on 992 of 999 con-                    lation and tactic-state access.
clusive pairs. The 7 disagreements all arise from a single
                                                                       LeanDojo (Yang et al., 2023) pairs a Python interface
mechanism: When a candidate places private helpers
                                                                       for proof-state interaction with an extracted dataset and a
inside a namespace, L EAN stores each private declaration
                                                                       retrieval-augmented prover; Pantograph (Aniva et al., 2025)
under a mangled symbol that includes the surrounding mod-
                                                                       exposes L EAN 4’s proof states for tactic-level interaction
ule name, and the same source compiled into two different
                                                                       and tree-search procedures; ProofWala (Thakur et al., 2025)
module names ends up with two distinct sets of mangled
                                                                       provides a multilingual Coq/Lean framework for proof-step
symbols. SafeVerify performs a whole-environment com-
                                                                       data collection and parallel proof search. These operate
parison between the target and submission .olean files
                                                                       at the tactic-state level, requiring a long-running proof-
and flags every such mangled symbol as missing. However,
                                                                       state object A XLE deliberately does not maintain; A XLE
the user-named theorem itself matches in both files, and so
                                                                       works at the declaration level (file in, transformed source
verify_proof and Comparator both accept the submis-
                                                                       or per-declaration metadata out) and is request-scoped and
sion. Appendix C.2 shows the pattern with an example.
                                                                       stateless, which is what enables the tool suite (§4) and per-
None of the disagreements reflect a soundness issue on                 request isolation. Jixia (FrenzyMath, 2024) is a command-
verify_proof’s part. We did not encounter naturally-                   line static-analysis tool that extracts source-level metadata—
occurring requests that incorrectly pass verify_proof                  declarations, symbols, elaboration info, and the parsed
while failing Comparator or SafeVerify, although such ex-              AST—from a compiled L EAN 4 file through a plugin ar-
amples can be deliberately crafted (§C.3).                             chitecture; it is closest in scope to a single A XLE tool
                                                                       (extract_decls).
6. Related Work
                                                                          6.2. Strict Proof Verification
6.1. L EAN 4 Services and Tooling
                                                                          lean4checker (Lean FRO, 2023), Comparator (Lean FRO,
The Lean REPL (Lean community, 2023) provides JSON-                       2025), and SafeVerify (GasStationManager, 2025) run can-
over-stdio access to a long-running L EAN process. Lean-                  didates in more scrutinous settings than verify_proof,
Interact (Poiroux et al., 2025) wraps it as a Python library              catching the environment-manipulation attacks of Ap-
for parallel processing; leanclient (Dressler, 2025) and lean-            pendix C at the cost of speed and concurrency. A XLE’s
lsp-mcp2 take a different route and wrap L EAN’s LSP, the                 deliberate trade-off is throughput on cooperating-client pop-
latter packaged as an MCP server for agentic proof sessions.              ulations; the alternatives suit verification of untrusted ex-
The Kimina Lean Server (Dos Santos et al., 2025) pools                    ternal code. Note that lean4checker inspects a candidate
many REPL instances behind a REST API with header-level                   environment but does not verify proofs against an external
LRU caching, aimed at high-throughput verification in RL                  formal statement, so it is not included in the comparison in
training. It matches A XLE in throughput. However, none of                §5.2.
   2
       https://github.com/oOo0oOo/lean-lsp-mcp

                                                                   6
                               A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

         comparison                            both accept    both reject   vp stricter   alt. stricter   inconclusive   agreement
         verify_proof vs. Comparator                     58          880             0               0             62    100.00%
         verify_proof vs. SafeVerify                     51          941             0               7              1     99.30%
Table 4. Verdict agreement on 1,000 paired production verify_proof requests. “vp stricter” indicates that verify_proof rejected
and the alternative accepted; “alt. stricter” indicates the reverse. “Inconclusive” counts requests where one side produced no clean verdict
(excluded from the agreement percentage).



6.3. Agentic Proving Pipelines                                           like Pantograph (Aniva et al., 2025) and lean-lsp-mcp.
APOLLO (Ospanov et al., 2025) and HILBERT (Varambally
                                                                         7.2. Future Work
et al., 2025) are agentic systems that combine LLM rea-
soning with formal verification through decompose-repair-                Concrete directions include broader multi-file support
recombine loops. They exercise exactly the operations                    beyond fixed-header environments, detailed proof state
A XLE exposes (sub-lemma extraction, source repair, se-                  extraction, and additional capabilities for tools like
mantic merging), but implement them as heuristic string- or              simplify_theorems and repair_proofs. We wel-
model-based orchestrations around the Lean REPL rather                   come community suggestions for additional tools and fea-
than as L EAN metaprograms behind a shared service.                      tures.

7. Conclusion                                                            Acknowledgements
A XLE is a cloud service for L EAN 4 proof manipulation,                 We thank the Lean FRO for their help and feedback, the rest
built on the premise that these tools belong in consoli-                 of the Axiom Math team as A XLE’s initial internal users,
dated infrastructure for AI4math rather than remaining af-               and our early public users for their feedback during the
terthoughts in each downstream system. Its 14 L EAN 4                    initial release.
metaprograms—spanning capabilities in verification, source
manipulation, dependency and lemma extraction, simplifi-
                                                                         Impact Statement
cation, and repair—serve all three principal AI4math work-
loads (reinforcement learning of prover models, agentic                  A XLE is freely available infrastructure for AI-driven
proving pipelines, and scalable dataset curation) from a                 L EAN 4 formal mathematics. We see no specific societal
single multi-tenant service with concurrent multi-version                risks beyond those already attendant on advances in machine
support.                                                                 learning for theorem proving.

7.1. Limitations                                                         AI Disclosure AI tools were used for prose drafting and
A XLE has two limitations worth noting.                                  editing throughout. All design decisions and quantitative
                                                                         results are the authors’.
Multi-file projects. Custom L EAN projects can be added
as additional environments (Section 3), but onboarding them              References
is higher-friction than selecting a new L EAN version: The               Aniva, L., Sun, C., Miranda, B., Barrett, C., and Koyejo,
project must be built and registered ahead of time, with                   S. Pantograph: A machine-to-machine interaction in-
no way to drop in arbitrary user-supplied dependencies at                  terface for advanced theorem proving, high-level rea-
request time. As a result, the public service does not offer               soning, and data extraction in Lean 4. In Gurfinkel,
generalized multi-file support. Each environment exposes                  A. and Heule, M. (eds.), Tools and Algorithms for the
a fixed import header, typically just import Mathlib,                     Construction and Analysis of Systems (TACAS), pp. 104–
and external imports beyond what that header provides are                 123. Springer Nature Switzerland, 2025. doi: 10.1007/
not accepted.                                                              978-3-031-90643-5_6.

Proof search and interactive sessions. A XLE is built                    banach1729. Goedel-workbook-lean-4.27: Lean workbook
around request-scoped, stateless tool invocations and does                 competition-math proofs from DeepSeek-Prover-
not support proof-tree search, interactive proof sessions,                 V1.5, migrated to Lean 4.27.0 / Mathlib v4.27.0.
or tactic-state-level manipulations—all of which require a                 https://huggingface.co/datasets/
long-running proof-state object A XLE does not maintain.                   banach1729/goedel-workbook-lean427,
Users who need that style of interaction should look at tools              2026.

                                                                     7
                            A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

Chen, E., Cummins, C., Eltschig, B., et al. Almost all primes         agentic reasoning system for formal mathematics. arXiv
  are partially regular. arXiv preprint arXiv:2602.05090,             preprint arXiv:2601.14027, 2026.
  2026a.
                                                                    Math Inc. Gauss: An agent for autoformalization. https:
Chen, E., Cummins, C., Grubisic, D., et al. Fel’s conjecture         //www.math.inc/gauss, 2025.
  on syzygies of numerical semigroups. arXiv preprint
  arXiv:2602.03716, 2026b.                                          Mistral AI. Leanstral: An open-source code agent for Lean
                                                                     4.      https://mistral.ai/news/leanstral,
Chen, L. et al. Seed-Prover: Deep and broad reason-                  2026.
  ing for automated theorem proving. arXiv preprint
  arXiv:2507.23726, 2025.                                           Ospanov, A., Farnia, F., and Yousefzadeh, R. APOLLO:
                                                                      Automated LLM and Lean collaboration for advanced for-
de Moura, L. and Ullrich, S. The Lean 4 theorem prover                mal reasoning. arXiv preprint arXiv:2505.05758, 2025.
  and programming language. In Automated Deduction
                                                                    Poiroux, A., Kunčak, V., and Bosselut, A. LeanInteract: A
  (CADE 28), volume 12699 of Lecture Notes in Computer
                                                                      Python interface for Lean 4. https://github.com/
  Science, pp. 625–635. Springer, 2021. doi: 10.1007/
                                                                      augustepoiroux/LeanInteract, 2025.
  978-3-030-79876-5_37.
                                                                    Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,
Dos Santos, M., de Saxé, H., Wang, H., Wang, R., Bakšys,
                                                                      Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. DeepSeek-
  M., Ünsal, M., Liu, J., Liu, Z., and Li, J. Kimina Lean
                                                                      Prover-V2: Advancing formal mathematical reasoning
  Server: A high-performance Lean server for large-scale
                                                                      via reinforcement learning for subgoal decomposition.
 verification. In NeurIPS 2025 Workshop on AI for Math,
                                                                      arXiv preprint arXiv:2504.21801, 2025.
  2025. arXiv preprint arXiv:2504.21230.
                                                                    Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaud-
Dressler, O. leanclient: A Python client for interacting with
                                                                      huri, S. An in-context learning agent for formal theorem-
  the Lean 4 language server. https://github.com/
                                                                      proving. In Conference on Language Modeling (COLM),
  oOo0oOo/leanclient, 2025.
                                                                      2024. arXiv preprint arXiv:2310.04353.
FrenzyMath. jixia: A static analysis tool for Lean
                                                                    Thakur, A., Tsoukalas, G., Durrett, G., and Chaudhuri,
  4. https://github.com/frenzymath/jixia,
                                                                      S. ProofWala: Multilingual proof data synthesis and
  2024.
                                                                      theorem-proving. arXiv preprint arXiv:2502.04671,
GasStationManager. Safeverify: A Lean 4 script for ro-                2025.
  bustly verifying submitted proofs of theorems and im-
                                                                    The Harmonic Team. Aristotle: IMO-level automated theo-
  plementations of functions. https://github.com/
                                                                      rem proving. arXiv preprint arXiv:2510.01346, 2025.
  GasStationManager/SafeVerify, 2025.
                                                                    The mathlib Community. The Lean mathematical library.
Hubert, T. et al. Olympiad-level formal mathematical rea-
                                                                      In Proceedings of the 9th ACM SIGPLAN International
  soning with reinforcement learning. Nature, 2025. doi:
                                                                      Conference on Certified Programs and Proofs (CPP), pp.
 10.1038/s41586-025-09833-y.
                                                                      367–381, 2020. doi: 10.1145/3372885.3373824.
Lean community.     A read–eval–print loop                          Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and
  for Lean 4.        https://github.com/                              Ye, K. Hilbert: Recursively building formal proofs with
  leanprover-community/repl, 2023.                                    informal reasoning. arXiv preprint arXiv:2509.22819,
Lean FRO. lean4checker: Replay the Environment for                    2025.
  a given Lean module. https://github.com/                          Wang, H. et al. Kimina-Prover Preview: Towards large
  leanprover/lean4checker, 2023. Integrated into                     formal reasoning models with reinforcement learning.
  Lean 4 v4.28.0 as leanchecker; repository archived                 arXiv preprint arXiv:2504.11354, 2025.
  2026.
                                                                    Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu,
Lean FRO. Comparator: A trustworthy judge for Lean                    S., Godil, S., Prenger, R., and Anandkumar, A. Lean-
  proofs. https://github.com/leanprover/                              Dojo: Theorem proving with retrieval-augmented lan-
  comparator, 2025.                                                   guage models. In Advances in Neural Information Pro-
Liu, J., Zhou, Z., Zhu, Z., Dos Santos, M., He, W., Liu,              cessing Systems (NeurIPS), 2023.
  J., Wang, R., Xie, Y., Zhao, J., Wang, Q., Zhi, L., Li, J.,
  and Li, W. Numina-Lean-Agent: An open and general

                                                                8
                             A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

                                 in-flight   median latency   p90 latency     throughput   scaling
                                        1            0.96 s          5.73 s   0.29 req/s   1.00×
                                        2            0.97 s          5.80 s   0.57 req/s   1.98×
                                        4            0.98 s          5.79 s   1.11 req/s   3.87×
                                        8            1.05 s          5.99 s   2.09 req/s   7.27×
                                       16            4.68 s          11.4 s   2.09 req/s   7.27×
Table 5. A XLE’s per-request median latency, p90 latency, and aggregate throughput at varying in-flight concurrency on a r7a.2xlarge
(8 vCPU), on the 5,000-proof Goedel-Lean4.27 check workload. “Scaling” is throughput relative to c=1. Throughput scales linearly
to the box’s vCPU count; pushing beyond 8 concurrent requests oversubscribes the physical cores, inflating latency without adding
throughput.



A. Further Evaluation
A.1. Experimental Setup
Hardware and isolation. Every measurement runs on a single AWS EC2 instance, with the specific instance varying
across experiments. All systems are pre-warmed before measurement with a single import Mathlib request. The
per-request budget is 150 s for the check workload (§5.1) and 600 s for the verify_proof workload (§5.2). For A XLE,
the L EAN executor workflow is isolated from the client-interaction logic (rate-limiting, queueing, load balancing, etc.). For
a fair comparison with raw L EAN invocations and Kimina, measurements only include per-request computation. Public
users should expect additional (minimal) server-side and network overhead.

Workloads. The latency/throughput comparison (§5.1) uses 5,000 random proofs sampled with a fixed seed from the
public banach1729/goedel-workbook-lean427 HuggingFace dataset (banach1729, 2026)—DeepSeek-Prover-
V1.5 outputs on the Lean Workbook competition-math corpus, published as compilable L EAN files migrated to L EAN 4.27.0.
Every system and concurrency setting sees the same 5,000 in the same order. Imports are normalised to a single import
Mathlib and candidates with non-Mathlib dependencies are dropped (discussed in §7). The dataset’s published claim is
that 94.1% of its proofs compile cleanly on the target snapshot; our sample lands at 94.16% (4708 / 5000) under all three
systems, which is consistent with the reported figure. The strict-checker comparison (§5.2) uses a separate 1,000-request
paired verify_proof sample drawn randomly from production traffic; each row pairs a target formal statement with a
candidate proof from the same production request.

Latency/throughput setup (§5.1). A XLE, Kimina Lean Server, and the direct-invocation baseline all run on a single
r7a.2xlarge (8 vCPU, 64 GiB), each at concurrency 8. Production A XLE’s check does some extra bookkeeping
Kimina’s /verify does not—custom per-declaration logging and sorry-state extraction—so for the comparison we disable
that bookkeeping in A XLE, leaving the same parse-and-elaborate work Kimina does. Kimina is built from source against
L EAN 4.27.0 and runs with its default settings. The direct-invocation baseline runs separate L EAN 4.27.0 subprocesses, one
per request.

Strict-checker setup (§5.2). A XLE, Comparator, and SafeVerify all run on a single r7a.4xlarge (16 vCPU, 128 GiB)
at concurrency 4. Each alternative is driven through a thin Python wrapper that compiles target and submission to oleans
(for SafeVerify) or stages them in a shared Lake project (for Comparator), then runs the upstream binary. The per-request
budget is 600 s for every system; Comparator’s median replay is 95.7 s but several take up to 10 minutes, and 62 requests
exceed the time budget. A XLE is configured with use_def_eq=False on the per-target signature check, matching what
Comparator and SafeVerify do (neither reduces expressions before comparing).

A.2. Concurrency Scaling for A XLE on the Same Instance
To show how A XLE scales by number of in-flight requests, we sweep its concurrency on the same 5,000-proof Goedel-
Lean4.27 workload and the same r7a.2xlarge as §5.1.
As expected, throughput scales near-linearly from c=1 through c=8. Median and p90 latency remain flat in the same range,
confirming that adding workers does not slow individual requests; it only adds capacity. Past c=8 the workers oversubscribe
the 8 physical cores: throughput plateaus at 2.09 req/s while median latency jumps roughly 4.5× (to 4.68 s) and p90 nearly
doubles. The verdict split is identical at every concurrency (4708 / 287 / 5); concurrency changes the speed, not the verdict.

                                                                 9
                           A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

B. Tool Demo
This appendix walks through using A XLE to prove a non-trivial L EAN 4 lemma. Taken from the public starting_demo
notebook in the A XLE examples repository,3 it illustrates the subproblem decomposition pattern: Starting from an LLM-
generated proof attempt that does not compile end-to-end, we use A XLE to break it into independent sub-obligations, solve
each, and reassemble the result.

The target statement
We aim to prove a divisibility lemma on greatest common divisors of consecutive odd numbers.
 import Mathlib

 lemma gcd_dvd_two_mul_diff (m n : N) :
     (Nat.gcd (2 * m + 1) (2 * n + 1) : Z) | 2 * ((m : Z) - (n : Z)) := by sorry


The initial LLM attempt
The agent produces the following proof attempt—a reasonable two-step strategy, but with tactics that do not all elaborate
cleanly:
 lemma gcd_dvd_two_mul_diff (m n : N) :
      (Nat.gcd (2 * m + 1) (2 * n + 1) : Z) | 2 * ((m : Z) - (n : Z)) := by
   have h1 : Nat.gcd (2 * m + 1) (2 * n + 1) | (2 * m + 1) - (2 * n + 1) := by
      apply Nat.gcd_dvd_sub
   have h2 : (2 * m + 1) - (2 * n + 1) = 2 * (m - n) := by ring
   rw [h2] at h1
   rcases le_or_gt n m with hn | hn
   · rw [← Nat.cast_sub hn]; exact_mod_cast h1
   · rw [show (2 : Z) * (↑m - ↑n) = -(↑(2 * n + 1) - ↑(2 * m + 1)) from by push_cast; ring
     ]
      exact dvd_neg.mpr (dvd_sub (by exact_mod_cast Nat.gcd_dvd_right _ _)
        (by exact_mod_cast Nat.gcd_dvd_left _ _))


Calling check on the attempt confirms it fails. The relevant errors:
 error: Unknown constant ‘Nat.gcd_dvd_sub‘
 error: unsolved goals
   m n : N
   h1 : (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1)
   ⊢ 1 + m * 2 - (1 + n * 2) = (m - n) * 2


Rather than discarding the attempt, we use A XLE to isolate the failing pieces and fix each independently.

Step 1: Decompose with have2lemma
have2lemma lifts each have step into a standalone lemma and rewrites the main proof to invoke it at the call site,
preserving the overall structure:
 result = await client.have2lemma(
     content=initial_attempt,
     reconstruct_callsite=True,
     environment=ENVIRONMENT,
 )
 decomposed = result.content


The decomposed file:
  3
    https://colab.research.google.com/github/AxiomMath/axiom-lean-engine/blob/main/
examples/starting_demo.ipynb

                                                            10
                             A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities


 import Mathlib

 lemma gcd_dvd_two_mul_diff.h1 (m n : N) :
     (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1) := sorry

 lemma gcd_dvd_two_mul_diff.h2 (m n : N)
     (h1 : (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1)) :
     2 * m + 1 - (2 * n + 1) = 2 * (m - n) := sorry

 lemma gcd_dvd_two_mul_diff (m n : N) :
      (Nat.gcd (2 * m + 1) (2 * n + 1) : Z) | 2 * ((m : Z) - (n : Z)) := by
   have h1 : Nat.gcd (2 * m + 1) (2 * n + 1) | (2 * m + 1) - (2 * n + 1) :=
      gcd_dvd_two_mul_diff.h1 m n
   have h2 : (2 * m + 1) - (2 * n + 1) = 2 * (m - n) :=
      gcd_dvd_two_mul_diff.h2 m n h1
   rw [h2] at h1
   rcases le_or_gt n m with hn | hn
   · rw [← Nat.cast_sub hn]; exact_mod_cast h1
   · rw [show (2 : Z) * (↑m - ↑n) = -(↑(2 * n + 1) - ↑(2 * m + 1)) from by push_cast; ring
     ]
      exact dvd_neg.mpr (dvd_sub (by exact_mod_cast Nat.gcd_dvd_right _ _)
        (by exact_mod_cast Nat.gcd_dvd_left _ _))


Step 2: Extract sub-problems with extract_decls
We then run extract_decls to obtain each sub-problem as an independent, self-contained L EAN snippet. The re-
turned document map contains three entries: gcd_dvd_two_mul_diff.h1, gcd_dvd_two_mul_diff.h2, and
the rewritten main lemma—each with the dependencies it needs to compile in isolation.

Step 3: Solve each sub-problem independently
The first sub-problem is a straightforward divisibility fact that the agent solves on the first attempt:
 lemma gcd_dvd_two_mul_diff.h1 (m n : N) :
     (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1) := by
   exact Nat.dvd_sub (Nat.gcd_dvd_left _ _) (Nat.gcd_dvd_right _ _)

The second is a simple arithmetic identity, so we save the LLM call and hand it directly to repair_proofs:
 repaired = await client.repair_proofs(
     content=h2_sorry,
     names=["gcd_dvd_two_mul_diff.h2"],
     environment=ENVIRONMENT,
 )

The tool closes the goal with a single terminal tactic:
 lemma gcd_dvd_two_mul_diff.h2 (m n : N)
     (h1 : (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1)) :
     2 * m + 1 - (2 * n + 1) = 2 * (m - n) := by grind


Step 4: Reassemble with merge
We merge the two solved sub-problems with the main decomposed proof. Declarations with matching types are reconciled
by preferring the compiling version, and the surviving declarations are topologically ordered:
 result = await client.merge(
     documents=[h1_proof, repaired.content, decomposed],
     environment=ENVIRONMENT,
 )
 final_proof = result.content


                                                               11
                             A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

The merged output:
 import Mathlib

 lemma gcd_dvd_two_mul_diff.h1 (m n : N) :
     (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1) := by
   exact Nat.dvd_sub (Nat.gcd_dvd_left _ _) (Nat.gcd_dvd_right _ _)

 lemma gcd_dvd_two_mul_diff.h2 (m n : N)
     (h1 : (2 * m + 1).gcd (2 * n + 1) | 2 * m + 1 - (2 * n + 1)) :
     2 * m + 1 - (2 * n + 1) = 2 * (m - n) := by grind

 lemma gcd_dvd_two_mul_diff (m n : N) :
      (Nat.gcd (2 * m + 1) (2 * n + 1) : Z) | 2 * ((m : Z) - (n : Z)) := by
   have h1 : Nat.gcd (2 * m + 1) (2 * n + 1) | (2 * m + 1) - (2 * n + 1) :=
      gcd_dvd_two_mul_diff.h1 m n
   have h2 : (2 * m + 1) - (2 * n + 1) = 2 * (m - n) :=
      gcd_dvd_two_mul_diff.h2 m n h1
   rw [h2] at h1
   rcases le_or_gt n m with hn | hn
   · rw [← Nat.cast_sub hn]; exact_mod_cast h1
   · rw [show (2 : Z) * (↑m - ↑n) = -(↑(2 * n + 1) - ↑(2 * m + 1)) from by push_cast; ring
     ]
      exact dvd_neg.mpr (dvd_sub (by exact_mod_cast Nat.gcd_dvd_right _ _)
        (by exact_mod_cast Nat.gcd_dvd_left _ _))


Step 5: Final verification
Finally, verify_proof confirms that the assembled file actually proves the original formal statement:
 result = await client.verify_proof(
     formal_statement=formal_statement,
     content=final_proof,
     environment=ENVIRONMENT,
 )
 # result.okay == True

The complete proof is now verified end-to-end. The pipeline used two generative-model calls (the initial attempt and
the proof of h1); every other step was a mechanical invocation of A XLE’s tools. Decompose with have2lemma and
extract_decls, solve sub-problems independently, reassemble with merge, and check with verify_proof—this
is the basic shape of many agentic proving workflows A XLE is designed to support.

C. Strict Verification: Case Studies
This appendix grounds the verification claims in concrete cases, organized into three groups:

 1. Two snippets that compile cleanly under check but are rejected by verify_proof’s rule checks (§C.1).
 2. The residual verdict disagreements between verify_proof and Comparator/SafeVerify on the 1,000 paired requests
    of §5.2—inter-tool differences that do not affect soundness on the user-named theorem (§C.2).
 3. One adversarial kernel-bypass that verify_proof accepts but a kernel-replay checker rejects (§C.3). This is the
    soundness gap for adversarial-input populations; we have not observed it in production traffic.

C.1. Cases verify_proof Catches
Both snippets below compile under plain check; verify_proof rejects each on a different rule.

Hidden axiom via a custom macro. The snippet below defines a macro totally_safe_decl that, despite its name,
expands to an axiom declaration—introducing hello_world : False. A custom fake_simp tactic then uses this
axiom to “prove” 1 = 2.

                                                             12
                           A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities


 syntax (name := totally_safe_decl) (priority := default + 1) declModifiers
   group("totally_safe_decl " declId ppIndent(declSig)) : command

 @[macro «totally_safe_decl»] def expandTotallySafeDecl : Macro := fun stx =>
   let stx := stx.modifyArg 1 fun stx =>
     let stx := stx.modifyArg 0 (mkAtomFrom · "axiom" (canonical := true))
     stx.setKind ‘‘Parser.Command.axiom
   pure <| stx.setKind ‘‘Parser.Command.declaration

 totally_safe_decl hello_world : False

 elab "fake_simp" : tactic => do
   evalTactic (← ‘(tactic| exact hello_world))

 theorem main : 1 = 2 := by exfalso; fake_simp

verify_proof rejects main on the axiom-whitelist check, with error message:

       In ’main’:     Axiom ’hello_world’ is not in the allowed set of standard
       axioms

This is not an entirely contrived pattern. Math Inc’s FormalQualBench encountered it in the wild: both Codex and OpenCode
submitted solutions that pass a plain lake build but reach the goal through an elaborator-level workaround.4 One
BanachStoneTheorem submission built an axiom via concatenation ("ax" ++ "iom") and elaborated it at command
time, so the keyword never appears literally in the source; the injected axiom then discharged the goal. verify_proof
properly rejects this pattern.

Namespace shadowing the intended definition. Another case redefines sqrt inside a local namespace, then opens that
namespace before stating a theorem whose name and surface syntax match the intended M ATHLIB statement.
 namespace hack
 def sqrt (r : R) := r
 end hack

 section
 open hack

 theorem impossible : sqrt 4 = 4 := by rfl

 end

The file compiles—rfl closes the goal because hack.sqrt 4 unfolds to 4. verify_proof rejects it on the signature-
match check, with error message:

       Theorem
       √         ’impossible’ does not match expected signature:                          expected type
         4 = 4, got hack.sqrt 4 = 4

C.2. Inter-Tool Differences Without Soundness Implications
On the 1,000-request paired sample (§5.2), the only residual verdict disagreement is the 7 SafeVerify-stricter cases of
Table 4 (verify_proof and Comparator accept; SafeVerify rejects). All 7 follow the same pattern. The candidate places
private helpers inside a namespace and uses them in the proof of a public theorem. L EAN mangles each private
declaration’s internal name with a module path—_private.Module.0.Namespace.name—so the same source
compiled into two different modules ends up with two different mangled names. SafeVerify performs a whole-environment
comparison between the target’s .olean and the submission’s .olean, and reports each mangled private helper present
in one olean but not the other as “declaration not found in submission”. The public theorem itself (the one named by the
   4
       https://www.math.inc/formalqualbench

                                                           13
                          A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

formal statement) is identical in both oleans and would type-check, but SafeVerify’s checks the entire environment and
rejects the whole submission.
A minimal example:
 import Mathlib

 namespace Paper

 private def castForm (x : R) : R := x + 1

 private lemma castForm_add (x y : R) :
     castForm (x + y) = castForm x + castForm y - 1 := by
   unfold castForm; ring

 -- the user-named theorem the formal statement asks us to prove
 theorem main (x : R) : castForm x = x + 1 := rfl

 end Paper


In the target olean (compiled from the formal statement), castForm and castForm_add are stored as
_private.Target.0.Paper.castForm and _private.Target.0.Paper.castForm_add. In the submis-
sion olean (compiled from the candidate), the same source produces _private.Submission.0.Paper.castForm
and _private.Submission.0.Paper.castForm_add. SafeVerify walks every declaration in the target olean and
looks it up by name in the submission olean; the _private.Target.* names have no counterpart on the submission
side, and SafeVerify reports them as missing:
 Found a problem in Submission.olean with declaration
   _private.Target.0.Paper.castForm:
   declaration not found in submission
 Found a problem in Submission.olean with declaration
   _private.Target.0.Paper.castForm_add:
   declaration not found in submission


verify_proof and Comparator only check for matching signatures on the named theorem (Paper.main) and accept.
None of these cases reflect a soundness gap on the user-named theorem.

C.3. Cases verify_proof Does Not Catch
verify_proof assumes every declaration in the environment was added through the standard, kernel-checked path, and
so does not catch inputs that smuggle declarations into the environment by other means. The canonical example, from
lean4checker’s adversarial test suite, installs a declaration directly through Environment.addDeclCore with kernel
checking disabled:
 import Lean.Elab.Term

 open Lean in
 run_elab
   modifyEnv fun env => Id.run do
     let decl := .thmDecl { name := ‘false, levelParams := [],
                             type := .const ‘‘False [], value := .const ‘‘False [] }
     let .ok env := env.addDeclCore (doCheck := false) 0 decl none |
       let _ : Inhabited Environment := ⟨env⟩
       unreachable!
     env


The result is an environment with a declaration false : False, never typechecked. verify_proof accepts
false : False as-is; a kernel-replay checker like lean4checker (Lean FRO, 2023) re-runs the environment through the
kernel from a clean state, detects the ill-formed declaration, and rejects.
Related kernel-bypass patterns work similarly: They evade the kernel’s normal type-checking step at elaboration time and
then use the unchecked declaration in the proof. The lean4checker, Comparator (Lean FRO, 2025), and SafeVerify (GasSta-

                                                          14
                            A XLE : A Cloud Infrastructure for L EAN 4 Theorem Proving Utilities

tionManager, 2025) test suites collect cases of this form.5 None of these patterns arise in the cooperating-client population
verify_proof targets; workloads verifying adversarial or external code should layer a strict checker on top. Readers
interested in the broader landscape of L EAN 4 proof verification can consult the L EAN reference.6

D. Resources
Resource                  URL or command
Service                   https://axle.axiommath.ai
Documentation             https://axle.axiommath.ai/v1/docs/
Python SDK and CLI        pip install axiom-axle
MCP server                pip install axiom-axle-mcp, or hosted at https://mcp.axiommath.ai
Example notebook          https://colab.research.google.com/github/AxiomMath/
                          axiom-lean-engine/blob/main/examples/starting_demo.ipynb
Release announcement      https://axiommath.ai/territory/releasing-axle
Discussion                Axiom Lean Engine topic on the Lean Zulip
Email support             axle@axiommath.ai




  5
    https://github.com/leanprover/lean4checker/tree/master/Lean4CheckerTests, https://github.
com/leanprover/comparator/tree/master/tests/projects, https://github.com/GasStationManager/
SafeVerify/tree/main/SafeVerifyTest.
  6
    https://lean-lang.org/doc/reference/latest/ValidatingProofs/

                                                             15
