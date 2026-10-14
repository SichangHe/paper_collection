                                                LeanFlow: A Case Study in Workflow-Driven Lean Autoformalization


                                                                  Lazar Milikić 1 Simon Guilloud 1 Khanh Nguyen 1 Viktor Kunčak 1


                                                                  Abstract                                     able Lean project while preserving the intended statements
                                                                                                               and managing a long sequence of dependent proof obliga-
                                              We present and evaluate LeanFlow, an LLM                         tions. M2F (Wang et al., 2026) and recent textbook- or
                                              agent system specialized for translating mathe-                  project-scale systems (Gloeckle et al., 2026; Math, Inc.,
                                              matical papers into buildable Lean projects. Re-                 2025; Hariharan et al., 2026; Tsoukalas et al., 2026) show
                                              cent verifier-in-the-loop systems show that large                that verifier-in-the-loop formalization can produce large
                                              formal artifacts can be produced, but it remains                 Lean artifacts; we examine which parts of the runtime help
                                              unclear which runtime mechanisms affect com-                     agents keep the source claims fixed and finish the resulting
                                              pletion, auditability, or efficiency in document-                proof work.
                                              to-project formalization. We study this question
                                              through case studies on two previously unfor-                    Motivated by this document-scale setting, we introduce
arXiv:2607.20503v1 [cs.AI] 26 Jun 2026




                                              malized mathematical papers in number theory                     LeanFlow as a Lean-specific runtime that separates math-
                                              and measure theory, using model, proof-workflow,                 ematical editing from workflow control. It first runs a de-
                                              and toolset ablations with Kimi-K2.6 and GPT-                    terministic source preflight: the runtime resolves the input
                                              5.5; we report task outcome, API calls, input to-                document, extracts or records source blocks, labels, refer-
                                              kens, and output tokens. With Kimi-K2.6, the full                ences, PDFs, figures, and support files, and refuses ambigu-
                                              workflow completes both document-level projects                  ous TEX roots before the model starts. The formalizer then
                                              within the 2000-call budget, while no-queue vari-                builds a blueprint, a project-local source map linking source
                                              ants reach the budget limit; with GPT-5.5, all                   spans to planned Lean declarations, dependencies, proof
                                              document-level variants complete, and the full                   notes, and recorded scope changes. Before proof search, a
                                              workflow has the lowest or tied-lowest input-                    statement/source gate checks that the generated declaration
                                              token cost on both sources. As complementary                     types still match the original source claims. During proving,
                                              calibration, LeanFlow reaches 75.7% BEq+ on                      a programmatic workflow manager owns the theorem queue,
                                              the PFR slice of RLM25 and solves all five ICML                  failed-attempt memory, retry budgets, verification records,
                                              2026 AI for Math TCS challenge projects in our                   logs, and checkpoints. The model proposes edits and helper
                                              GPT-5.5 runs.                                                    lemmas, while the manager assigns one target at a time and
                                                                                                               advances only after external Lean verification accepts the
                                                                                                               edit.
                                         1. Introduction                                                       This separation has different benefits across the two model
                                                                                                               settings in our experiments. For Kimi-K2.6 (Moonshot AI,
                                         Autoformalization is moving from isolated theorem transla-
                                                                                                               2026), workflow control is decisive in our two document-
                                         tion toward turning whole mathematical sources into Lean
                                                                                                               level runs: the full workflow finishes both sources, while
                                         projects. Early language-model formalization work focused
                                                                                                               no-queue variants exhaust the call budget. For GPT-5.5, all
                                         on translating individual natural-language statements into
                                                                                                               document-level variants finish, so the observed benefit is
                                         proof-assistant syntax (Wu et al., 2022), and many theorem-
                                                                                                               not a binary success difference; the same structure instead
                                         proving benchmarks still ask the model to prove one sup-
                                                                                                               improves token efficiency and preserves an explicit audit
                                         plied formal statement at a time (Zheng et al., 2022; Azer-
                                                                                                               trail for the proof work.
                                         bayev et al., 2023). A document-level agent faces a dif-
                                         ferent problem: it must convert mathematical prose, TEX               LeanFlow also introduces LeanProbe1 , a cached same-file
                                         structure, references, definitions, and proofs into a build-          verifier built on LeanInteract (Poiroux et al., 2025b), for
                                            1
                                                                                                               repeated proof-repair checks. LeanProbe gives the prov-
                                              EPFL, Lausanne, Switzerland. Correspondence to: Lazar            ing agent low-latency diagnostics and proof-state feedback
                                         Milikić <lazar.milikic@epfl.ch>.
                                                                                                               while leaving final acceptance to standard Lean/Lake checks.
                                         The 3 rd AI for Math Workshop at the 43rd International Confer-       In the sequential same-file benchmark summarized in Ta-
                                         ence on Machine Learning (ICML), Seoul, South Korea, 2026.               1
                                         Copyright 2026 by the author(s).                                             https://github.com/epfl-lara/LeanProbe


                                                                                                           1
                                    LeanFlow : A case study in workflow-driven Lean agents

ble 6, cached checking is roughly 9–14× faster than rerun-             We release on GitHub the LeanFlow implementation, Lean-
ning growing-prefix Lake checks.                                       Probe verifier, and generated case-study projects.
Our main evaluation ablates LeanFlow on real document-
level formalizations, where the system must recover state-             2. Related Work
ments from source documents and then complete the result-
                                                                       Formal theorem proving with language models. Lean
ing proof work. We compare queue management with free-
                                                                       4 (de Moura & Ullrich, 2021) and Mathlib (The mathlib
running proof loops, full Lean tool access with terminal-only
                                                                       Community, 2020) provide the verification substrate for
interaction, and source-blueprint checkpoints with direct
                                                                       many recent neural theorem-proving systems. Benchmarks
source-to-code generation. Proof-only benchmarks remain
                                                                       such as miniF2F (Zheng et al., 2022), ProofNet (Azerbayev
useful calibration, but they provide the formal statement in
                                                                       et al., 2023), PutnamBench (Tsoukalas et al., 2024), Formal-
advance and only test whether the system can replace the
                                                                       MATH (Yu et al., 2025), SorryDB (Letson et al., 2026), and
proof placeholder. We therefore report RLM25-PFR agent
                                                                       VeriSoftBench (Xin et al., 2026) measure different proof-
runs and the ICML 2026 AI for Math TCS challenge (AI for
                                                                       only or repository-scale capabilities. They provide useful
Math Workshop, 2026) as complementary measurements.
                                                                       calibration, but most start from an existing formal statement
The two document-level case studies are Frisch and Vaser-              or repository context. Our work instead studies the runtime
stein’s Parametrization of Pythagorean Triples by a Single             needed when the source begins as mathematical prose, and
Triple of Polynomials (Frisch & Vaserstein, 2007) and Lyons            the output must be a buildable project.
and Zumbrun’s A Calculus Proof of the Cramer–Wold The-
orem (Lyons & Zumbrun, 2017). The Pythagorean source
combines integer-valued polynomial definitions, an obstruc-            Autoformalization across scales. Early LLM autoformal-
tion over Z[x1 , . . . , xn ], explicit rational-polynomial wit-       ization work studied natural-language-to-formal translation
nesses, and custom plain-TEX theorem macros. The Cramer–               at theorem scale (Wu et al., 2022); later work improved
Wold source combines probability measures on Euclidean                 process supervision and evaluation for Lean statements (Lu
space, closed half-space values, Crofton reconstruction of             et al., 2024; Poiroux et al., 2025c;a). M2F (Wang et al.,
average-distance functions, odd-dimensional Laplacian in-              2026) and Automatic Textbook Formalization (Gloeckle
version, and an even-to-odd embedding step. These sources              et al., 2026) formalize long mathematical sources into Lean
are short enough for controlled ablations, but they are still          projects, audit generated statements, and repair proofs un-
full mathematical papers with nontrivial definitions, repre-           der a pinned environment. Math, Inc.’s Gauss system is
sentation choices, and proof dependencies. Both require                an autoformalization agent for large Lean projects (Math,
source-aware definitions and reusable Lean infrastructure              Inc., 2025). In the sphere-packing project (Hariharan et al.,
that the prose leaves implicit.                                        2026), it helps complete a sorry-free formalization of the
                                                                       dimension-8 result from an existing blueprint and Lean de-
This paper makes three main contributions:                             velopment. AlphaProof Nexus (Tsoukalas et al., 2026) uses
                                                                       an agentic evolutionary framework for formal proof search
   • A document-to-project workflow for Lean formaliza-                over a large set of formalized conjectures. Direct compari-
     tion. LeanFlow starts from a paper or TEX project,                son with M2F is difficult from the currently available public
     records which source text supports each generated dec-            artifacts: reproducing our document-level runs under M2F
     laration, checks statements before proof search, and              would require the same source documents, model, Mathlib
     moves to the next theorem only after Lean accepts the             version, budget, prompts, workflow logs, tool surface, and
     current proof edit.                                               final acceptance criteria. Our study is smaller in document
                                                                       volume but different in emphasis: we isolate queue con-
                                                                       trol, tool routing, statement handoff, and model-side budget
   • A fast local verifier for proof repair. LeanProbe caches
                                                                       under the two model settings in our experiments.
     the Lean environment before the current declaration
     and returns proof states and diagnostics through a CLI
     and MCP server; final acceptance remains a standard               Lean tooling for agents. Retrieval and environment ac-
     Lean/Lake build.                                                  cess are central to practical Lean proving. LeanDojo (Yang
                                                                       et al., 2023) studies retrieval-augmented theorem proving,
   • An evaluation on full mathematical sources and proof-             and LeanExplore (Asher, 2025) provides search over Lean
     only benchmarks. We ablate queue control, tool access,            declarations. LeanInteract (Poiroux et al., 2025b) exposes
     and source checkpoints on two paper formalizations                a Python interface to Lean execution. LeanFlow builds on
     with Kimi-K2.6 and GPT-5.5, and report RLM25-PFR                  this tool ecosystem but introduces LeanProbe as its own
     and ICML 2026 AI for Math TCS challenge runs as                   cached same-file verifier for agent loops; final acceptance
     calibration.                                                      still comes from standard Lean/Lake verification.

                                                                   2
                                          LeanFlow : A case study in workflow-driven Lean agents

                                                     Formalizer
                                                                                         redraft



                                 Preflight             Blueprint          Lean draft               Statement/source
      Source artifact
                                 manifest            source map        statements with                   gate
    .tex, PDF, TEX tree
                            blocks, PDFs, refs    deps, names, notes    sorry proofs               approve or redraft



                                                                                   Formal statements




                          Workflow state record                                                                          Final gates
                                                                        Prover queue                      LeanProbe
                                                                       one declaration                  cached checks    Lake build
                                                                          at a time                       warm env      sorry/axioms


                                                                                                            Prover

Figure 1. LeanFlow document-to-project pipeline. Dashed regions separate the formalizer and prover phases; the green silo is the
project-local workflow state record shared by both. The formalizer emits a well-typed statement skeleton and a durable blueprint, and
formal theorem statements pass through a statement/source gate before the prover queue attempts proof closure under verifier and hygiene
gates. The workflow state records activity, proof checkpoints, failed attempts, route decisions, prover plans, and outcomes, so redrafts and
build failures persist outside the transient conversation state.


3. Problem Setting                                                         Algorithm 1 LeanFlow agent workflow contract
Let D be a mathematical source artifact: a LATEX file, a PDF,               1: Resolve source document D and pinned Lean environ-
or a directory containing a TEX project. Let E be a pinned                     ment E.
Lean environment: a Lean toolchain, a fixed mathematical-                   2: Extract a preflight manifest: source blocks, labels, ref-
library revision such as a Mathlib commit, and the Lake                        erences, PDFs, figures, and support files.
project configuration used for checking. The mathematical                   3: Create a “blueprint” mapping source spans to planned
result should not depend on this particular snapshot, but                      declarations, dependencies, scope changes, and proof
the evaluation of builds, diagnostics, imports, and available                  notes.
lemmas is always relative to E. The goal is to produce a                    4: Draft Lean declarations with placeholders only for
Lean project P together with declaration-level provenance.                     theorem-like proofs; verify that the statement layer type-
For each generated declaration d ∈ Decl(P ), the workflow                      checks.
should record                                                               5: Run a statement/source gate; if faithfulness fails, redraft
                                                                               before proof search.
                     π(d) ⊆ Span(D),
                                                                            6: while the requested file or project still contains assigned
where π(d) is the finite set of source spans, labels, sections,                proof obligations do
pages, equations, or bibliography references justifying d.                  7:    Assign one theorem-like declaration from the queue.
                                                                            8:    Use search, proof context, and LeanProbe-backed
We separate three checks. Statement type-checking asks
                                                                                  checks to repair the assigned proof.
whether the generated Lean declaration is well typed under
                                                                            9:    Persist failures, diagnostics, route decisions, and
E when theorem-like proof bodies are replaced by explicit
                                                                                  proof checkpoints after each attempt.
sorry placeholders. Statement faithfulness asks whether
                                                                           10:    Accept the assignment only after verification, no rel-
that well-typed declaration states the source claim, includ-
                                                                                  evant sorry, and an acceptable axiom profile.
ing statement type, quantifiers, domains, hypotheses, and
                                                                           11: end while
conclusion. Proof completion asks whether a faithful decla-
ration has a complete proof with no unacceptable placehold-
ers or custom axioms. The final project gate is stricter than a
theorem-local check: the requested file or full Lake project
                                                                           backed Lean declarations and proof plans, and prove,
must build under E, and a hygiene scan must report no
                                                                           which repairs or completes Lean proofs until the requested
unapproved sorry, admit, unsafe, or hidden axiom.
                                                                           file or project compiles successfully. The workflows are
                                                                           deliberately separated. Formalization may introduce def-
4. Method                                                                  initions, names, imports, and theorem statements, but it
                                                                           stops at a proof skeleton with source-backed sorry bodies.
4.1. Workflow Overview
                                                                           Proof repair then treats those declarations as fixed targets: it
Figure 1 and Algorithm 1 summarize the document-to-                        may edit proof bodies and add local helper lemmas, but it
project contract. LeanFlow uses two primary workflows:                     may not modify theorem statements, add axioms, or leave
formalize, which turns a source document into source-                      the assigned proof partially solved.

                                                                       3
                                   LeanFlow : A case study in workflow-driven Lean agents

4.2. Source-Backed Skeleton Construction                              Table 1. Statement/source review checks applied before proof
                                                                      repair.
LeanFlow begins by resolving the source deterministically
using document processing tools. For a TEX project direc-              Check            Rejection signal
tory, deterministic preflight uses regular expression search to        Statement type The type of the generated Lean declaration
identify and select a main entry point, follow local includes,                        does not fully match the source statement, so
record bibliography files, figures, PDFs, and support files,                          a proof may certify a different claim
                                                                       Quantifiers    Order, dependency, or implicit parameters
and fail on ambiguous roots before the agent starts. The                              changed
same pass extracts standard theorem-like environments, cus-            Variable types Variables range over the wrong type
tom theorem declarations, plain-TEX theorem/proof blocks,              Hypotheses     Added assumption, missing side condition,
labels, references, citations, section structure, and nearby                          changed nonemptiness
proof environments when available. For PDFs, it records                Conclusion     Weakened equality, image statement, equiva-
                                                                                      lence, or existence
extracted text, metadata, and image inventories through                Encoding       A local encoding is used without the def-
local Poppler tools such as pdftotext, pdfinfo, and                    bridge         initions or equivalence/evaluation lemmas
pdfimages; the model reads this bounded source view                                   needed to recover the source statement
through read pdf.                                                      Proof notes    Source proof idea missing for a nontrivial the-
                                                                                      orem
The formalize workflow next creates a project-local                    Hygiene        Hidden axiom, unsafe, admit, or unre-
blueprint before the proof skeleton is considered ready.                              ported sorry
The blueprint is the durable source map for the run: it
lists source statements, planned Lean names, dependen-
cies, source locators, statement-fidelity checks, proof notes,        file to the file-scoped declaration queue. This outer queue
and known scope changes. For each source theorem or                   is needed because document formalizations produce many
lemma, it spells out the parts of the formal type that are            dependent proof obligations. Without route control, the
most prone to drift: statement type, quantifier order, pa-            agent can spend calls on the wrong file, revisit failed paths,
rameter domains, codomains, hypotheses, side conditions,              or move to later work before earlier dependencies are stable.
and follow-on equivalences. The generated Lean module
must type-check with theorem bodies left as by sorry;                 4.5. File-Scoped Declaration Queue
proof filling is deferred until the statement/source gate has
approved the skeleton.                                                Figure 2 shows the declaration queue and repair loop inside
                                                                      an assigned file. Once the project queue selects a file, the
4.3. Statement/Source Gate                                            manager builds a file-scoped declaration queue from pend-
                                                                      ing sorry declarations and diagnostics. The front queue
The statement/source gate checks the generated skeleton               item becomes the active declaration; the prover loop repairs
before proof search begins. Compilation only shows that a             only that declaration before the manager advances to the
declaration is well typed; it does not show that the declara-         next queue item. For the active queue item, the manager
tion is the theorem stated in the paper. LeanFlow therefore           stores the target, theorem-local failed attempts and diag-
launches a fresh LLM reviewer context—a separate model                nostics, retry counters, and the latest verification record; it
context with no human in the loop—over the blueprint, gen-            also tracks the remaining declarations in the file and each
erated Lean declarations, and original source spans. The              accepted or failed outcome. It builds the bounded context
reviewer is a single invocation of a thinking model; it can           shown to the model, runs or routes verification, and lets
approve, reject, or request redrafting, but it does not fill          the model advance only after the assigned declaration is
proof bodies. If any check in Table 1 fails, the formalizer           clean. The model sees the current target, a small view of
returns to the skeleton before the prove workflow starts; the         the remaining file work, relevant source/proof context, and
prover should not receive a weakened, strengthened, or in-            theorem-local failed attempts.
comparable target. We call the version that passes this gate
the reviewed skeleton.                                                The file-scoped declaration queue keeps proof search fo-
                                                                      cused by exposing only one active assignment at a time. It
                                                                      prevents common long-run failures: losing the active the-
4.4. Project-wide Prover Queue
                                                                      orem after compaction, retrying a previously failed proof
The project-wide prover queue chooses which file the prover           shape, changing a future statement, or advancing because
should work on next. When a requested project still contains          a text search no longer finds sorry while Lean still re-
sorry, the manager scans the files, ranks candidate files             ports open goals. After each edit, the proving LLM agent
using declaration dependencies, local hints, examples, and            refreshes the structured Lean state and asks the manager
size estimates, records the route decision, and hands one             whether to continue the same declaration, accept the edit,
                                                                      restore a baseline sorry, or assign the next declaration.

                                                                  4
                                         LeanFlow : A case study in workflow-driven Lean agents

                          Queue manager                                     inline Lean comments at the failing location. A failed candi-
                        theorem assignment
                                                                            date can be returned as model-readable Lean with compact
                                                                            comments containing the local proof state and the diagnostic
                              Context tools
                            inspect, search,                                beside the failing tactic, as illustrated in Figure 3.
                               proof state
                                                                            Table 2. Default tool surface exposed to the agent currently com-
                            Candidate edit                                  prises 27 tools. The following table groups them by purpose. The
                            proof or helper                                 manager decides which tool class is relevant for the current proof
                                                                            obligation or failure mode.
                         LeanProbe check                                      Tool class          Agent use
                        cached environment
                                                                              Source readers      Inspect TEX/PDF inputs, extracted text, image inventory,
                                                                                                  and source spans
                                                                              File editing        Read, search, patch, and write project files under man-
                                                                                                  ager checks
                                clean?                                        Lean verification   Run canonical Lean/Lake checks and LeanProbe cached
                      no                       yes                                                target checks
                                                                              Search/context      Retrieve local/Mathlib facts, nearby declarations, and
           record failure                       accept edit                                       theorem context
              replan                            next target                   Proof exploration   Try bounded proof candidates, request reasoning help,
                                                                                                  and decompose helpers
Figure 2. File-scoped proving loop. Failed checks update theorem-             Code hygiene        Scan for remaining sorry, custom axioms, unsafe con-
                                                                                                  structs, and axiom profiles
local memory; accepted edits advance to file/Lake verification                Workflow memory     Reattach skills, blueprints, session notes, and theorem-
sweeps.                                                                                           local failed attempts
                                                                              Terminal fallback   Run explicit shell commands when the bounded tools
                                                                                                  are insufficient
    LeanProbe feedback on a failed candidate
  theorem add comm candidate (x y : Nat) :
    x + y = y + x := by                                                     This information is used for fast local repair inside the queue
   /- <feedback>
   -- proof state:
                                                                            loop, not for final acceptance. The final gates remain module
   x y : Nat                                                                or project Lake builds and verification that the project is
   ⊢ x + y = y + x
   </feedback> -/
                                                                            free from unapproved axiom declarations and remaining
    rfl                                                                     sorry placeholders. Table 2 summarizes the tool classes
   /- <feedback>                                                            exposed to the model; ablations in Section 5 remove this
   -- error: tactic ’rfl’ failed                                            surface to isolate its effect.
   </feedback> -/


Figure 3. Example LeanProbe feedback embedded into a failed                 5. Evaluation
Lean candidate. The proof state is injected before the failing tactic
(green marker) and the diagnostic after it (red marker); the failing        The experiments test whether the LeanFlow workflow com-
tactic is underlined in red.                                                ponents in Figure 1 improve real formalization and proving
                                                                            runs. Each completed run reports task outcome, API calls,
                                                                            input tokens, and output tokens from the workflow logs; the
4.6. LeanProbe and Tool Surface                                             released LeanFlow artifacts include the run configurations,
                                                                            prompts, and logs used for these tables. All model-backed
LeanProbe is a declaration-level verifier for repeated
                                                                            runs use fixed decoding settings across conditions: temper-
proof attempts in one Lean file. It is a standalone
                                                                            ature 0.3, top-p = 0.95, and a maximum output budget of
CLI, Python library, and MCP server built on LeanIn-
                                                                            65,536 tokens per model turn. We count only model API
teract (Poiroux et al., 2025b), and is openly available at
                                                                            calls. For GPT-5.5, one Codex CLI model turn is one call;
epfl-lara/LeanProbe. At assignment time, Lean-
                                                                            for Kimi-K2.6, one request to the EPFL-hosted inference
Probe runs a prepare step for the active declaration: it
                                                                            endpoint is one call. Terminal commands, file reads and
checks imports, the file header, and all prior declarations,
                                                                            edits, Lean/Lake invocations, LeanProbe checks, and other
then stores the resulting environment immediately before the
                                                                            structured tool invocations are not counted as API calls. For
target. Each check step replaces the target declaration with
                                                                            cost accounting, the GPT-5.5 runs used the Codex CLI under
one candidate proof or helper block and checks it against
                                                                            a US$200 GPT Pro subscription; one month of this subscrip-
that cached environment. The cache advances only after a
                                                                            tion covered all GPT-5.5 experiments reported here. The
complete declaration replacement is accepted, so failed can-
                                                                            Kimi-K2.6 runs used a self-hosted EPFL deployment on
didates give diagnostics without changing the environment
                                                                            8×H200 GPUs, and token-cost estimates use CHF 0.4802
seen by later obligations.
                                                                            per million input tokens and CHF 1.4406 per million output
LeanProbe returns proof-agent feedback: diagnostics, warn-                  tokens. Because these two models use different account-
ings, sorry detection, tactic metadata, goal states, and                    ing regimes, the tables report calls and tokens rather than

                                                                        5
                                   LeanFlow : A case study in workflow-driven Lean agents

converting all rows to a single monetary scale.                       full tool surface versus terminal-only interaction. Table 3 is
                                                                      organized by source so that completion behavior and model-
5.1. Document-Level Case Studies                                      side budget can be compared within the same mathematical
                                                                      project. Here and in later tables, queue means the two-
The two document-level case studies are selected for mathe-           layer queue system: the project-wide file queue plus the
matical content and area diversity. Frisch and Vaserstein’s           file-scoped declaration queue. All four conditions for a
Pythagorean-polynomial paper (Frisch & Vaserstein, 2007)              given source start from the same reviewed skeleton and
requires formalizing the classical T (a, b, c) parametrization,       use the same proof goal, prompt template, model settings,
parity and divisibility side conditions, the obstruction to a         and call budget; only the queue system and tool surface are
single integer-coefficient polynomial triple, and the explicit        changed. All document-level proving runs have a maximum
four-variable triple of integer-valued rational polynomials.          budget of 2000 prover-agent API calls, where one call is
Lyons and Zumbrun’s Cramer–Wold paper (Lyons & Zum-                   one model turn in the proof-repair loop. In the terminal-
brun, 2017) requires formalizing closed half-spaces as mea-           only condition, the agent may still read and edit files, search
surable sets, equality of measures from matching half-space           with shell tools such as rg, and run commands such as
values, the Crofton step from half-space values to average-           lake build, but it has no access to LeanProbe, MCP-
distance functions, the odd-dimensional Laplacian recovery            backed Lean tools, structured declaration search, or proof-
argument, and the even-to-odd embedding R2m ,→ R2m+1 .                state APIs. In the no-queue condition, an outer runner still
Section A gives the detailed source-to-Lean decomposi-                keeps the prover running until the project succeeds or the
tion for both case studies. To the best of our knowledge,             call budget expires, but both queue layers are disabled: the
neither source theorem had a prior proof-assistant formal-            manager does not route files through a project queue, does
ization. The completed Pythagorean project comprises                  not restrict the model to one top-of-queue declaration, and
83 Lean declarations (34 of them theorem/lemma state-                 does not use theorem-local failed-attempt history to gate the
ments) and the Cramer–Wold project 114 declarations (101              next target. Source preflight, the statement/source gate, final
theorem/lemma statements); both build sorry-free and                  Lean/Lake verification, and hygiene checks are held fixed
free of unapproved axioms.                                            across conditions.
For the workflow ablations reported in Table 3, each source           Table 3 shows that the combined queue system is decisive
first runs through the pre-proof stages in Figure 1 and Algo-         for Kimi-K2.6 in these two document-level runs: both no-
rithm 1: source resolution, blueprint construction, statement         queue variants exhaust the 2000-call budget on both case
generation with proof placeholders, and statement/source              studies, while full LeanFlow succeeds in 1043 calls on
review. The result is a reviewed skeleton, i.e., a Lean state-        Pythagorean triples and 1278 calls on Cramer–Wold. The
ment layer that type-checks with theorem bodies left as               effect of the tool surface is most visible on the analytic
placeholders and has passed the source-faithfulness checks            case study, where Kimi-K2.6 with a queue but terminal-only
in Table 1. The Pythagorean reviewed skeleton is produced             interaction still fails on Cramer–Wold. For GPT-5.5, all
with Kimi-K2.6; the Cramer–Wold reviewed skeleton is                  document-level variants succeed, so these rows do not estab-
produced with GPT-5.5 because the initial representation              lish LeanFlow as necessary for completion under this model.
setup for probability measures, half-spaces, and the analytic         Instead, they support an efficiency and auditability claim:
inversion target requires more representation choices than            full LeanFlow has the lowest or tied-lowest input-token cost
the Pythagorean source. These pre-proof stages are held               on both sources, although the Cramer–Wold no-queue/full-
fixed across the proof-repair ablations, and the 2000-call            tools run uses slightly fewer calls at a higher input-token
budget in Table 3 begins after the reviewed skeleton has              cost.
been accepted. Statement translation, skeleton construc-
tion, the statement/source gate, and proof repair all run
                                                                      5.3. RLM25-PFR Autoformalization
autonomously, with no human edits to the reviewed skele-
tons or to the proof runs in Table 3; expert involvement is           We evaluate on RLM25-PFR, the PFR slice of
limited to verifying faithfulness after the fact (Section 6),         RLM25 (Poiroux et al., 2025a;c), rather than on the
because no automated faithfulness guarantee is currently              full RLM25 benchmark. This slice contains 145 theorem-
available.                                                            statement examples from the Polynomial Freiman–Ruzsa
                                                                      project. We report it separately from the document-to-
5.2. Workflow Ablations on Real Sources                               project case studies because each example is an independent
                                                                      theorem task rather than a complete source document.
The primary evaluation is an ablation study: it compares
the full LeanFlow against variants that remove the queue              Each RLM25-PFR example is run as a two-stage Lean work-
system and/or the specialized Lean tools. For each model,             flow with one shared 200-call model budget per example.
we run the full 2 × 2 design: queue versus no queue, and              First, the agent receives the informal statement, project con-


                                                                  6
                                    LeanFlow : A case study in workflow-driven Lean agents

Table 3. Long-form workflow ablation on the two document-level case studies. Workflow abbreviations encode queue-system and tool
configuration: Full = both queue layers with full tools; NoQ+Tools = no queue system with full tools; Q+CLI = both queue layers with
terminal-only interaction; NoQ+CLI = no queue system with terminal-only interaction. Outcome is success when the requested project
builds under E from the reviewed skeleton with no remaining sorry and no unapproved axioms within the 2000-call budget, and failure
otherwise. Calls are prover-agent API calls with a 2000-call cap.

Source                  Model                 Workflow               Outcome                 Calls                  In tok.               Out tok.
Pythagorean             Kimi-K2.6             Full                   success                 1043                   46.9M                 514.1K
Pythagorean             Kimi-K2.6             NoQ+Tools              failure                 2000                  160.2M                 682.0K
Pythagorean             Kimi-K2.6             Q+CLI                  success                 1561                   91.3M                 537.8K
Pythagorean             Kimi-K2.6             NoQ+CLI                failure                 2000                  157.5M                 615.5K
Cramer–Wold             Kimi-K2.6             Full                   success                 1278                   66.0M                 684.1K
Cramer–Wold             Kimi-K2.6             NoQ+Tools              failure                 2000                  127.8M                 583.2K
Cramer–Wold             Kimi-K2.6             Q+CLI                  failure                 2000                  113.1M                 579.0K
Cramer–Wold             Kimi-K2.6             NoQ+CLI                failure                 2000                  167.0M                 496.4K
Pythagorean             GPT-5.5               Full                   success                   258                 14.3M                  190.5K
Pythagorean             GPT-5.5               NoQ+Tools              success                   568                 45.0M                  240.3K
Pythagorean             GPT-5.5               Q+CLI                  success                   277                 14.3M                  177.0K
Pythagorean             GPT-5.5               NoQ+CLI                success                   984                 89.9M                  340.7K
Cramer–Wold             GPT-5.5               Full                   success                   495                 25.9M                  305.5K
Cramer–Wold             GPT-5.5               NoQ+Tools              success                   448                 32.8M                  259.7K
Cramer–Wold             GPT-5.5               Q+CLI                  success                   959                 59.5M                  518.0K
Cramer–Wold             GPT-5.5               NoQ+CLI                success                   476                 49.7M                  281.6K


text, and any available informal proof or blueprint material,        Table 4. RLM25-PFR agent-run results on the PFR slice. Proof suc-
                                                                     cess is the share of examples whose final Lean code verifies with
and synthesizes a Lean declaration that must type-check,
                                                                     no remaining placeholders or unapproved axioms under the 200-
typically with a placeholder proof. The generated statement          call per-example budget; BEq and BEq+ are statement-equivalence
is evaluated against the reference formal statement using            metrics against reference formal statements. Calls and tokens are
the benchmark’s BEq and BEq+ statement-equivalence met-              totals over the slice and include both statement synthesis and proof
rics. Second, the generated statement is treated as a fixed          completion.
proof target: the prover may fill proof bodies and add local          Model    Workflow          Proof succ. BEq     BEq+ Calls In tok.    Out tok.
helper lemmas, but it may not weaken statements, introduce            GPT-5.5 LeanFlow            81.2%     70.8% 75.7% 3541 203.2M 2.1M
custom axioms, or leave sorry/admit placeholders. The                 GPT-5.5 terminal-only agent 80.6%     68.1% 72.9% 4053 236.6M 2.3M
call budget is shared by statement synthesis and proof com-
pletion, and the call totals in Table 4 include both stages.
Runs are autonomous after launch, with no human edits
to the generated statements or proofs. If the 200-call bud-          5.4. Challenge Tasks
get is exhausted before final verification, the example is
                                                                     Project-level proving tasks provide the formal statements
counted as a proof failure. Proof success requires final
                                                                     and isolate proof construction. The ICML 2026 AI for Math
Lean/Lake verification and the same hygiene scan used in
                                                                     Track 2 TCS proving challenge tests project-level algorith-
our document-level runs. Table 4 summarizes the com-
                                                                     mic proof tasks in graph theory, combinatorics, computa-
pleted GPT-5.5 runs. In this single GPT-5.5 run, LeanFlow
                                                                     tional complexity, and algorithm correctness using CSLib
reduces calls (3,541 vs. 4,053) and input tokens (203.2M
                                                                     and a comparator-backed pass-rate metric (AI for Math
vs. 236.6M) while increasing BEq+ from 72.9% to 75.7%;
                                                                     Workshop, 2026). The five challenge projects cover bi-
because the runs lack variance estimates, we treat the BEq+
                                                                     nary heap operations, a heap-backed Dijkstra proof, Kruskal
change as a small effect rather than a significance claim.
                                                                     minimum spanning trees, segment-tree construction and
The gap between proof success and statement-equivalence
                                                                     range queries, and treap invariant/runtime obligations. Each
metrics reinforces why verified proof completion cannot
                                                                     run uses the same 2000-call proof budget as the document-
replace statement/source checks: a proved declaration can
                                                                     level proof-repair runs. Success means that the final project
still formalize the wrong mathematical claim.
                                                                     passes the official SafeVerify/comparator check and also
To our knowledge, no published baseline reports provide              passes our local final Lean/Lake verification and hygiene
proof-of-completion results for the RLM25-PFR two-stage              scan with no remaining sorry/admit placeholders or un-
setting; the original source (Poiroux et al., 2025a) is not          approved axioms. We run all five projects with GPT-5.5
concerned with producing proofs of statements.                       under three conditions: full LeanFlow, no queue system
                                                                     with LeanProbe still available, and no queue system with
                                                                     only terminal Lean/Lake interaction. For Kimi-K2.6, we

                                                                 7
                                   LeanFlow : A case study in workflow-driven Lean agents

additionally run the Kruskal project with full LeanFlow and          the current cached environment, while accepted declarations
without either the queue system or the specialized tool sur-         advance the environment for later targets.
face. All challenge runs are autonomous after launch, with
                                                                     Table 6 supports the design choice of checking candidate ed-
no human edits to the proof files during the run. The public
                                                                     its frequently instead of waiting for large repair batches. The
Track 2 leaderboard lists our competition submission under
                                                                     prepare step is paid once before a target, and then each can-
the lmilikic identifier at rank 2 in the combined Phase
                                                                     didate proof replacement is checked in milliseconds to tens
1+2 ranking (AI for Math Workshop, 2026).
                                                                     of milliseconds. Sequential checks also match the queue
Table 5 shows that all GPT-5.5 variants solve all five TCS           design: the environment advances only after a complete
projects, so these rows do not isolate a single decisive work-       declaration succeeds, so failed candidates are diagnosed
flow component. The results are also consistent with Lean-           without changing the context for later obligations. The de-
Probe being useful as a feedback surface: workflow logs              tailed LeanProbe experimental setup and per-file results are
show that GPT-5.5 used LeanProbe in 37% of recorded                  reported in Section B.
agent steps in TCS runs where the tool was available, and
NoQ+Probe uses fewer calls and lower input tokens than               5.6. Statement-Skeleton Case Study
NoQ+CLI on four of five projects. This aligns with the tool
design in Section 4.6, where failed candidates can return            We use a qualitative Pythagorean-polynomial comparison to
local compiler diagnostics and proof-state feedback before           check whether the source-to-statement stages in Algorithm 1
the next proof attempt. For Kimi-K2.6, the tested Kruskal            prevent statement drift before proof search. The no-review
run succeeds with the full workflow, while the no-queue              condition skips the blueprint and statement/source review
terminal-only variant reaches the 2000-call budget.                  stages in Steps 3 and 5: after seeing the source, the model
                                                                     is asked to produce Lean translations directly, without a
                                                                     recorded source-to-declaration map or an independent faith-
5.5. LeanProbe Utility
                                                                     fulness check before proving. The no-review draft and the
LeanProbe is evaluated separately because it changes ver-            reviewed skeleton both build, but they formalize different
ifier latency rather than model capability. We compare               mathematical objects. The no-review draft would support a
cached LeanProbe checks against terminal lake env                    less source-faithful function-level formalization of the result:
lean checks on two workloads that match the proof loop               it defines the main witnesses as rational-valued functions on
in Figure 2. The repeated-target workload measures many              integer inputs. The reviewed skeleton is the source-faithful
candidate replacements for one active declaration after a            version under the checks in Table 1: it defines the witnesses
single prepare step. The sequential workload measures a              as rational multivariate polynomials and separately proves
queue-style file run: partial candidates are rejected against        integer-valuedness, matching the paper’s theorem. The de-


Table 5. AI4Math TCS challenge outcomes by project and workflow condition. Workflow abbreviations encode queue-system and tool
configuration: Full = both queue layers with full tools; NoQ+Probe = no queue system with LeanProbe available; NoQ+CLI = no queue
system with terminal-only Lean/Lake interaction. Calls are prover-agent API calls with a 2000-call per-project cap.

Project                Model                Workflow                 Outcome             Calls             In tok.          Out tok.
Binary heap            GPT-5.5              Full                     success                54             2.86M              49.8K
Binary heap            GPT-5.5              NoQ+Probe                success                27            741.3K               7.1K
Binary heap            GPT-5.5              NoQ+CLI                  success                72             5.03M              71.1K
Dijkstra               GPT-5.5              Full                     success                61             4.04M              75.1K
Dijkstra               GPT-5.5              NoQ+Probe                success                20            770.2K              26.0K
Dijkstra               GPT-5.5              NoQ+CLI                  success                29             1.15M              23.9K
Segment tree           GPT-5.5              Full                     success                62            4.01M               35.0K
Segment tree           GPT-5.5              NoQ+Probe                success                85            7.01M               42.2K
Segment tree           GPT-5.5              NoQ+CLI                  success                73            4.67M               45.4K
Treap                  GPT-5.5              Full                     success              142            10.88M               85.1K
Treap                  GPT-5.5              NoQ+Probe                success              144            10.80M               95.6K
Treap                  GPT-5.5              NoQ+CLI                  success              188            14.10M              116.8K
Kruskal                GPT-5.5              Full                     success                47            1.75M               16.2K
Kruskal                GPT-5.5              NoQ+Probe                success                37            1.56M               17.7K
Kruskal                GPT-5.5              NoQ+CLI                  success                53            2.94M               26.8K
Kruskal                Kimi-K2.6            Full                     success              942            107.9M                3.1M
Kruskal                Kimi-K2.6            NoQ+CLI                  failure             2000            189.1M              930.4K


                                                                 8
                                   LeanFlow : A case study in workflow-driven Lean agents

Table 6. LeanProbe latency benchmarks. Repeated-target times are average ranges in seconds after one prepare step; sequential rows
report total seconds per compact file with five declarations and ten partial/full candidate scenarios.

  Workload OS        Full-file Lake Cached check       Workload       OS       Growing-prefix Lake Cached total    Speedup
  TCS        macOS 2.082–2.617s 0.031–0.049s           Compact files macOS 36.474–67.992s           3.789–4.775s 9.63–14.24×
  TCS        Linux 1.495–1.886s 0.032–0.054s           Compact files Linux 22.593–23.186s           2.301–2.547s 9.05–9.82×


tailed declaration-level contrast is reported in Appendix A         control outside the model: the runtime records source-to-
(Table 7).                                                          Lean decisions, reviews statements before proof search,
                                                                    assigns proofs one at a time, checks candidate edits quickly,
6. Threats to Validity                                              and accepts only builds that pass the verifier and contain no
                                                                    leftover placeholders or unapproved axioms. The document-
The evaluation has several limitations. Buildability is nec-        level evidence is model-dependent: in our two case studies,
essary but not sufficient: a project can build while encod-         workflow control is decisive for Kimi-K2.6 completion un-
ing a different claim. The statement/source gate runs au-           der budget, while for GPT-5.5 it mainly improves token effi-
tonomously, but we still confirm faithfulness by expert in-         ciency and audit discipline because every document-level
spection, because there is currently no automated way to            variant completes.
guarantee that a well-typed declaration matches the source;
reducing this manual confirmation is important future work.         Impact Statement
The workflow also assumes that the source definitions and
theorem statements are the targets to preserve. After the           This work aims to make Lean autoformalization more in-
statement/source gate accepts a skeleton, the prover is not         spectable, reproducible, and verifier-grounded. Potential
allowed to change definitions or theorem statements; this           positive impacts include reducing the engineering burden of
improves auditability, but it can make a proof obligation           proof repair, improving the auditability of machine-assisted
impossible if the source contains a typo, an omitted side           formalization, and making document-level formal verifi-
condition, or an undetected mistranslation. Such errors             cation workflows easier to study. Potential risks include
must be caught during statement/source review or expert             over-reliance on generated formal artifacts, mistaking build-
audit rather than silently repaired during proof search. The        ability for source faithfulness, and unequal access to the
document-level evidence covers only two case studies; the           compute and model resources needed for long formalization
Cramer–Wold skeleton was initialized with GPT-5.5 rather            runs. LeanFlow is designed to mitigate these risks by record-
than Kimi-K2.6 because of its representation choices. The           ing source-to-Lean decisions, separating statement review
ablations are single runs, so they do not estimate variance;        from proof search, preserving workflow logs and check-
repeated document-level runs would be more informative              points, and accepting final artifacts only after external Lean
but costly, since each can require hundreds to thousands of         verification with no leftover placeholders or unapproved
calls, tens to hundreds of millions of input tokens, and sub-       axioms. The system is intended to assist expert formalizers
stantial wall-clock time. Several mechanisms also remain            rather than replace human mathematical judgment.
bundled: queue/tool ablations do not isolate blueprinting,
statement review, failed-attempt memory, hygiene scanning,          Author Contributions
and LeanProbe feedback. The complementary benchmarks
do not fully exercise document-to-project formalization, the        Lazar Milikić led the system design, implementation, ex-
RLM25-PFR rows cover only the PFR slice rather than                 periments, and paper writing. Simon Guilloud helped with
the full RLM25 benchmark, the GPT-5.5 rows support ef-              benchmarking code, research direction, and paper writing.
ficiency claims more than necessity claims, and we do not           Khanh Nguyen contributed with research direction and pa-
include a matched document-level M2F comparison. Calls              per writing. Viktor Kunčak supervised the project, con-
and token counts are useful proxies for model-side effort,          tributed to the research direction, and helped revise the
but not full measures of wall-clock, monetary, or human             manuscript.
engineering cost.
                                                                    Acknowledgments
7. Conclusion
                                                                    This research is supported by the AI For Math Fund, admin-
LeanFlow treats autoformalization as an evolving Lean               istered by Renaissance Philanthropy and funded by XTX
project with durable workflow state, not as independent the-        Markets. We also gratefully acknowledge the support of the
orem prompts. The central design choice is to keep project          EPFL School of Computer and Communication Sciences.


                                                                9
                                   LeanFlow : A case study in workflow-driven Lean agents

References                                                            Moonshot AI. Kimi-K2.6: Open-weights native mul-
                                                                       timodal agentic model. https://huggingface.
AI for Math Workshop. ICML 2026 AI for math workshop
                                                                       co/moonshotai/Kimi-K2.6, 2026. Hugging Face
  track 2 leaderboard.      https://ai4math2026.
                                                                       model card for moonshotai/Kimi-K2.6.
  github.io/track2/leaderboard/,                  2026.
  Track 2 theoretical computer science proving in Lean                Poiroux, A., Bosselut, A., and Kuncak, V. RLMEval: Evalu-
  leaderboard and challenge scoring summary.                            ating research-level neural theorem proving, 2025a. URL
                                                                        https://arxiv.org/abs/2510.25427.
Asher, J. LeanExplore: A search engine for Lean 4 dec-
  larations, 2025. URL https://arxiv.org/abs/                         Poiroux, A., Kuncak, V., and Bosselut, A. LeanInteract: A
  2506.11085.                                                           python interface for Lean 4. https://github.com/
                                                                        augustepoiroux/LeanInteract, 2025b.
Azerbayev, Z., Piotrowski, B., Schoelkopf, H. W., Ayers,
  E. W., Radev, D., and Avigad, J. ProofNet: Autoformaliz-            Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Reli-
  ing and formally proving undergraduate-level mathemat-                able evaluation and benchmarks for statement autoformal-
  ics, 2023. URL https://arxiv.org/abs/2302.                            ization. In Proceedings of the 2025 Conference on Empir-
  12433.                                                                ical Methods in Natural Language Processing, pp. 17947–
                                                                        17969, Suzhou, China, 2025c. Association for Computa-
de Moura, L. and Ullrich, S. The Lean 4 theorem prover                  tional Linguistics. doi: 10.18653/v1/2025.emnlp-main.
  and programming language. In Automated Deduction –                    907. URL https://aclanthology.org/2025.
  CADE 28, pp. 625–635. Springer, 2021. doi: 10.1007/                   emnlp-main.907/.
  978-3-030-79876-5 37.
                                                                      The mathlib Community. The Lean mathematical library.
Frisch, S. and Vaserstein, L. Parametrization of Pythagorean            In Proceedings of the 9th ACM SIGPLAN International
  triples by a single triple of polynomials, 2007. URL                  Conference on Certified Programs and Proofs, pp. 367–
  https://arxiv.org/abs/0706.0290.                                      381. Association for Computing Machinery, 2020. doi:
                                                                        10.1145/3372885.3373824.
Gloeckle, F., Rammal, A., Arnal, C., Munos, R., Cabannes,
  V., Synnaeve, G., and Hayat, A. Automatic textbook for-             The PhysLib community.       PhysLib: The Lean
  malization, 2026. URL https://arxiv.org/abs/                          physics library.        https://github.com/
  2604.03071.                                                           leanprover-community/physlib,           2024.
                                                                        Formerly PhysLean/HepLean.
Hariharan, S., Birkbeck, C., Lee, S., Ma, H. K. G., Mehta,
  B., Poiroux, A., and Viazovska, M. A milestone in for-              Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M.,
  malization: The sphere packing problem in dimension                   Jennings, M., Thakur, A., and Chaudhuri, S. Putnam-
  8, 2026. URL https://arxiv.org/abs/2604.                              Bench: Evaluating neural theorem-provers on the put-
  23468.                                                                nam mathematical competition, 2024. URL https:
                                                                        //arxiv.org/abs/2407.11214.
Letson, A., Sarra, L., Poiroux, A., Dressler, O., Lezeau,
  P., Aranha, D., Pu, F., Hill, A., Hidalgo, M. C., Berman,           Tsoukalas, G., Kovsharov, A., Shirobokov, S., Surina, A.,
  J., Tsoukalas, G., and Taelman, L. SorryDB: Can AI                    Firsching, M., Bérczi, G., Ruiz, F. J. R., Suggala, A., Wag-
  provers complete real-world Lean theorems?, 2026. URL                 ner, A. Z., Wieser, E., Yu, L., Huang, A., Horváth, M. Z.,
  https://arxiv.org/abs/2603.02668.                                     Ferrauiolo, A., Michalewski, H., Grosu, C., Hubert, T.,
                                                                        Balog, M., Kohli, P., and Chaudhuri, S. Advancing math-
Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C., Shen,          ematics research with ai-driven formal proof search, 2026.
  J., Jin, H., Zhang, J., Wang, H., Yang, Z., Tang, J., and             URL https://arxiv.org/abs/2605.22763.
  Guo, Z. Process-driven autoformalization in Lean 4, 2024.
  URL https://arxiv.org/abs/2406.01940.                               Wang, Z., Ma, W., Ming, Z., Zhang, G., Yuan, K., and
                                                                       Wen, Z. M2F: Automated formalization of mathematical
Lyons, R. and Zumbrun, K. A calculus proof of the Cramér–             literature at scale, 2026. URL https://arxiv.org/
  Wold theorem, 2017. URL https://arxiv.org/                           abs/2602.17016.
  abs/1607.03206.
                                                                      Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
Math, Inc. Introducing Gauss, an agent for autoformal-                 nik, M., and Szegedy, C. Autoformalization with large
 ization. https://www.math.inc/gauss, 2025.                            language models, 2022. URL https://arxiv.org/
 Company announcement.                                                 abs/2205.12615.

                                                                 10
                                  LeanFlow : A case study in workflow-driven Lean agents

Xin, Y., Chen, Q., Durrett, G., and Dillig, I. VeriSoft-
  Bench: Repository-scale formal verification benchmarks
  for Lean, 2026. URL https://arxiv.org/abs/
  2602.18307.
Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
  LeanDojo: Theorem proving with retrieval-augmented
  language models, 2023. URL https://arxiv.org/
  abs/2306.15626.
Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M., Zhang,
  Y., Zheng, Y., Xin, H., Huang, W., Wen, Y., and Liu,
  W. FormalMATH: Benchmarking formal mathematical
  reasoning of large language models, 2025. URL https:
  //arxiv.org/abs/2505.02735.
Zheng, K., Han, J. M., and Polu, S. MiniF2F: A cross-
  system benchmark for formal olympiad-level mathemat-
  ics. In International Conference on Learning Represen-
  tations, 2022. URL https://openreview.net/
  forum?id=9ZPegFuFTFv.




                                                                11
                                     LeanFlow : A case study in workflow-driven Lean agents

A. Document Case Study Details
The LeanFlow implementation is available on GitHub at epfl-lara/LeanFlow, the LeanProbe verifier at
epfl-lara/LeanProbe, and the generated formalization projects at epfl-lara/AutoformalizedProjects.
Each released project is self-contained and pins its own Lean toolchain and Mathlib revision (for example, Lean
v4.30.0-rc2 for the Pythagorean project and v4.29.1 for Cramer–Wold), so builds are reproducible without a
single global environment. The two case studies have also been contributed to the community lean-pool repository of
AI-produced Lean developments (pull requests #185 and #186).

Pythagorean-polynomial source. The Frisch–Vaserstein source first defines Pythagorean triples, polynomial parametriza-
tion over Z[x1 , . . . , xn ], and integer-valued parametrization over Int(Zn ) ⊆ Q[x1 , . . . , xn ]. The formalization therefore
introduces both integer-coefficient and rational-polynomial representations before stating the main claims. The source-level
proof obligations are: the standard two-family parametrization of triples, the obstruction to a single integer-coefficient
triple, the explicit four-variable integer-valued witness, the positive-triple variant, and the four-square unrestricted-parameter
variant. The obstruction proof is algebraic: it uses the UFD structure of Z[x1 , . . . , xn ], a gcd decomposition, parity facts,
and the examples (3, 4, 5) and (4, 3, 5) to force a contradiction. The construction proof uses the source map

                                          T (a, b, c) = c(a2 − b2 )/2, cab, c(a2 + b2 )/2
                                                                                            


and the parity condition that makes all three coordinates integral. The reviewed Lean layout separates these concerns into
basic definitions, source handoff lemmas, obstruction lemmas, integer-valued construction lemmas, positive-triple lemmas,
and explanatory material for cited background. This layout also records source claims that are likely to be omitted in a
proof-only draft: the finite-cover theorem for integer-valued parametrizations, the displayed binomial-polynomial identity,
and the non-UFD motivation for Int(Z).

Table 7. Declaration-level contrast in the Pythagorean statement skeleton. The no-review draft is generated directly from the source; the
reviewed skeleton is the version accepted by the statement/source review conditions described in Table 1.

  Source requirement      No-review draft                                        Reviewed skeleton
  Integer-valued poly- IntegerValued4 is a predicate definition on func- RatPoly n is a type abbreviation for rational mul-
  nomial objects       tions Z → Z → Z → Z → Q; integer-valuedness is tivariate polynomials; IsIntValued is a predicate
                       checked only after evaluation at integer inputs.  definition, and IntValuedSubring n is a sub-
                                                                         ring definition.
  Displayed witnesses f param, g param, and h param are function def- f param, g param, and h param are polynomial
  are polynomials     initions of four integer arguments, so the displayed definitions of type RatPoly 4; evaluation at integer
                      source witnesses are encoded only by their evalua- tuples is handled separately by ratPolyEval.
                      tions.
  Main theorem type       integer valued is a theorem proving integer- exists int valued is a theorem with con-
                          parametrization                                       parametrization
                          valuedness and image equality for the function model. clusion IntValuedParametrizes ..., so it
                                                                                states existence of integer-valued rational polynomials
                                                                                that parametrize the triples.
  Background claims re- The direct translation omits theorem or definition dec- The reviewed skeleton keeps theorem declarations
  tained                larations for the finite-cover result and the integer- for the finite-cover result and non-UFD claim, plus
                        valued-polynomial ring background.                      polynomial definitions and theorems for the binomial-
                                                                                polynomial identity.



Cramer–Wold source. The Lyons–Zumbrun source states that Borel probability measures on Rn are determined by their
values on closed half-spaces. The formalization represents Rn as Lean Euclidean space, defines closed half-spaces by a
normal vector and threshold, and records half-space value functions and the average-distance function
                                                   Z
                                          fµ (y) = (∥y − x∥ − ∥x∥) dµ(x).

The first analytic proof block packages the Crofton/Fubini argument showing that half-space values determine fµ . The
second proof block packages the odd-dimensional inversion step: after reindexing dimensions as 2m + 1, the needed kernel

                                                                   12
                                  LeanFlow : A case study in workflow-driven Lean agents

identity is that an (m + 1)-fold Laplacian of the norm kernel recovers a nonzero multiple of the point mass at the origin. In
Lean-facing terms, this requires a tempered-distribution norm kernel, Fourier/Laplacian algebra for iterated Laplacians,
transport between the Euclidean model used by PhysLib (The PhysLib community, 2024) and the project’s odd-dimensional
space, and a bridge from PhysLib’s real distribution API to Mathlib’s complex tempered distributions. The analytic
formalization also produced reusable PhysLib infrastructure for distributional Laplacians of norm-kernel fundamental
solutions, contributed upstream in leanprover-community/physlib#1175. The even-dimensional Cramer–Wold
theorem is then reduced to the odd-dimensional one by embedding R2m into R2m+1 and transporting half-space values
along that embedding. The reviewed skeleton keeps the Crofton and inversion blocks as named proof targets rather than
folding them into the final theorem; this makes clear which missing analytic facts are mathematical infrastructure, not
model-generated assumptions.

B. LeanProbe Benchmark Results
This appendix records the detailed LeanProbe benchmark rows behind Table 6. The snapshot was refreshed on May 13,
2026, with Lean 4.30.0-rc2. These rows are verifier-latency measurements, not model-performance measurements: they
isolate the cost of checking candidate Lean edits under different reuse policies. The benchmark suite has two parts: grouped
repeated-target checks, which stress many alternatives for one active declaration, and sequential same-file checks, which
stress queue-style advancement through a file. All runs use one measured run per target/file, no benchmark warmups, warm
Lake caches from prior validation, and a fresh-server baseline. LeanProbe remains a feedback surface; final file or project
acceptance still uses standard Lean/Lake verification.




Grouped repeated-target benchmark. The repeated-target workload measures the agent pattern of trying several com-
plete replacements for one active declaration. For each target, the benchmark writes a temporary full file and times
terminal lake env lean; then it starts LeanProbe, prepares the environment immediately before the target, checks
the replacement against that cached environment, optionally requests proof-state feedback, and finally repeats the check
with a fresh LeanProbe/LeanInteract server to measure the no-cache baseline. The compact groups are Mathlib-facing
examples: analysis real covers elementary real-analysis facts, algebra order covers ordered algebra and in-
equalities, sets functions covers set/function image and preimage reasoning, and number theory nat covers
elementary natural-number arithmetic. The TCS groups are longer challenge-style extracts: tcs binary heap contains
heap operations such as heapify, extract min, insert, merge, and remove; tcs treap analysis contains
the two probability-sum obligations used in the treap analysis; and tcs weighted graph contains weighted-graph
helper declarations through the Sym2order prefix. In Table 8, Targets is the number of active declarations in the group,
Lake full is full-file terminal verification, Prepare is the one-time cached-environment setup, Cached is a target replacement
check after prepare, Feedback includes diagnostic/proof-state metadata, Fresh is the same check with a fresh server, and
Fresh/cached is the fresh-check time divided by the cached-check time.




Sequential same-file benchmark. The sequential workload models a queue-managed file run rather than repeated attempts
on one target. Each compact file has five declarations and ten scenarios: for every targetable declaration, the benchmark
checks a partial declaration containing sorry and then the complete declaration. LeanProbe reports the partial scenario and
detects the sorry, but it advances the cached environment only after the complete declaration succeeds. The Lake baselines
rerun terminal checks for every scenario, either on a growing prefix that includes accepted prior declarations or on a full
temporary file in which only the current declaration is replaced. In Table 9, Lake prefix and Lake full are these two terminal
baselines, Probe cached is one warm LeanProbe/LeanInteract server walking the whole file, Probe fresh restarts LeanProbe
for every scenario, and the three speedup columns divide the corresponding baseline total by the cached LeanProbe total.

                                                             13
                                      LeanFlow : A case study in workflow-driven Lean agents

Table 8. LeanProbe repeated-target grouped results. Times are averages in seconds; fresh/cached is the ratio between a fresh LeanProbe
server and a cached check.

                 Platform Group                   Targets Lake full Prepare Cached Feedback Fresh Fresh/cached
                 macOS      analysis real               5      3.893     6.024     0.039      0.022 4.014         139.7×
                 macOS      algebra order               5      3.900     3.683     0.048      0.039 3.987         106.7×
                 macOS      sets functions              5      3.708     3.502     0.008      0.007 3.766         454.7×
                 macOS      number theory nat           5      3.731     3.478     0.011      0.006 3.776         420.0×
                 Linux      analysis real               5      2.276     2.315     0.025      0.024 2.412         103.2×
                 Linux      algebra order               5      2.301     2.317     0.046      0.043 2.516          78.2×
                 Linux      sets functions              5      2.233     2.257     0.011      0.009 2.383         245.8×
                 Linux      number theory nat           5      2.199     2.217     0.009      0.008 2.390         322.0×
                 macOS      tcs binary heap             9      2.576     2.931     0.049      0.042 2.589         155.9×
                 macOS      tcs treap analysis          2      2.082     2.219     0.034      0.034 2.181          77.8×
                 macOS      tcs weighted graph          9      2.617     2.461     0.031      0.028 2.603         194.9×
                 Linux      tcs binary heap             9      1.886     1.807     0.054      0.051 1.877         103.2×
                 Linux      tcs treap analysis          2      1.495     1.441     0.036      0.040 1.560          53.1×
                 Linux      tcs weighted graph          9      1.771     1.683     0.032      0.034 1.761         127.5×



Table 9. LeanProbe sequential same-file results. Each file has five declarations and ten partial/full scenarios. Times are total seconds for
the file.

     Platform File                   Decls. Scen. Lake prefix Lake full Probe cached Probe fresh vs prefix            vs full vs fresh
     macOS      analysis real             5     10       67.992     40.216            4.775      44.699     14.24× 8.42× 9.36×
     macOS      algebra order             5     10       46.870     48.163            4.339      40.953     10.80× 11.10× 9.44×
     macOS      sets functions            5     10       45.421     42.237            3.916      37.797     11.60× 10.79× 9.65×
     macOS      number theory nat         5     10       36.474     36.648            3.789      36.736      9.63× 9.67× 9.70×
     Linux      analysis real             5     10       22.765     22.958            2.515      24.890      9.05× 9.13× 9.90×
     Linux      algebra order             5     10       23.186     23.489            2.547      25.147      9.10× 9.22× 9.87×
     Linux      sets functions            5     10       22.679     22.567            2.384      24.195      9.51× 9.47× 10.15×
     Linux      number theory nat         5     10       22.593     22.829            2.301      24.086      9.82× 9.92× 10.47×


Repeated-target rows isolate the cost of checking many replacements for one active declaration after a single prepare step.
For n complete replacement attempts on the same target, the comparison is

                          Probe total(n) = Prepare + n · Cached,                 Lake total(n) = n · Lake full.

The preparation cost is therefore amortized as soon as a target receives several candidate repairs: after setup, each additional
candidate costs the cached-check time instead of another full-file lake env lean run. The grouped rows report this
steady-state behavior directly through Cached, Fresh, and Fresh/cached; the sequential rows report the end-to-end cost when
successful declarations advance the environment. Sequential rows model queue-style proving in one file: partial sorry
scenarios are diagnosed but not cached, while complete accepted declarations advance the environment for later targets.
This matches the proof-loop policy used in our runs: keep the LeanProbe server warm, prepare once before a target when
several repairs are likely, and advance the cached environment only after a complete declaration has been accepted.




                                                                    14
