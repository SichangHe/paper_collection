                                                        Assay: Claims That Decay With the Code
                                                        Content-Addressed Evidence Graphs for Accountable AI-Assisted Software Delivery

                                                      Om Shankar Tiwari                                        Tangi Vass                  Gagan Deep Singh
                                            Applied AI Technical Lead, Google       Co-Founder & CPTO, OMNI3ai         Founder, Glinr Studios and theSVG.org
                                                   California, United States                   Lyon, France                      Texas, United States
                                           https://orcid.org/0009-0001-2247-0383 https://orcid.org/0009-0009-0414-6190 https://orcid.org/0009-0002-0579-6514



                                                                                                          approval is about. A later change to an unrelated module and
                                         Abstract: AI coding agents fail in two coupled ways. They spend most of
                                         their context window rediscovering where things live, and they assert success
                                                                                                          a change to something A depends on look identical to it: both
                                         without evidence when the work gets hard. Repository indexes address the
                                                                                                          are “after the approval”. That forces a bad choice. Either every
                                         first with cheap context, and orchestration frameworks with adversarial
arXiv:2609.36170v1 [cs.SE] 28 Sep 2026




                                                                                                          accepted verdict stays valid until someone notices otherwise,
                                         review address the second with accountability. Both describe the same object,
                                         the structure of the codebase, at two timescales: what is true of the code
                                                                                                          or every change invalidates everything and review starts over.
                                         now, and what was verified to be true, at which revision, by whom. A SSAY
                                         makes that observation operational. Every claim an agent makes (testsA claim about code is a claim about content, and content is
                                                                                                          content-addressable. Key a claim by the hash of the code it is
                                         pass, no secrets, behavior preserved) is bound to the Merkle hash of the
                                         dependency cone of the code it covers, so the claim is stale exactly when
                                                                                                          about and “has this gone stale?” becomes a hash comparison
                                         that code or anything it depends on changes. We show the binding is sound
                                                                                                          rather than a judgment. The subtlety is which hash. Hashing
                                         and minimal, and that the blast radius of a change is precisely the set of
                                                                                                          only the named module is unsound, because a test result for
                                         claims it invalidates. On the graph we place a risk-proportional evidence
                                         obligation, a bounded review protocol with separation of duties, and a
                                                                                                          A depends on B. Hashing the whole repository is sound but
                                         merge gate that consults no model: coverage, freshness, signatures, exit
                                                                                                          useless, because every edit invalidates every claim. The right
                                         codes, plausibility, evidence monotonicity (the mechanical form of “do not
                                                                                                          key is the hash of the dependency cone of the subject, computed
                                         delete the failing test”), and review status. A SSAY is a dependency-free
                                         Python tool with an MCP server. On five public repositories a 600-token
                                                                                                          as a Merkle hash over the condensation of the dependency
                                         brief costs 14× to 114× less than an exploration proxy, warm rebuilds are
                                                                                                          graph. Under this key staleness is sound and minimal, and the
                                         up to 5× faster than cold ones, cone binding re-verifies 7.9% to 81.9% of
                                                                                                          blast radius of a change, the modules whose cone hash moved,
                                         claims where repository binding re-verifies all of them while per-module
                                         binding misses 23% to 68% of required invalidations, and the gate blocks 9
                                                                                                          is by construction the set of claims it invalidated. Context and
                                         of 9 scripted adversarial behaviours while admitting the honest ones. Every
                                         number in this paper is generated by the released scripts.       accountability become one computation over one graph.
                                                                                                              This paper contributes:
                                         Index Terms: AI coding agents, code provenance, Merkle trees, dependency
                                         graphs, code review, software supply chain
                                                                                                            • A model. Content-addressed modules, cone hashes over

                                                                I. I NTRODUCTION                                the condensation DAG, claims bound to cone hashes, and
                                                                                                                propositions establishing soundness, minimality, and the
                                            An agent that edits code has to answer two questions before         identity between blast radius and staleness frontier. A ledger
                                         it can be trusted: where does this change go, and how do we            of such claims is a build cache for assertions in the sense
                                         know it worked? Both are questions about the structure of the          of Mokhov et al. [5].
                                         repository. The first is about the structure now. The second is    • A protocol. Risk-proportional evidence obligations, a
                                         about the structure at the moment a check ran, and whether it          bounded review cycle with separation of duties adapted
                                         has drifted since.                                                     from Liza and applied per claim, and a merge gate with
                                            Current tooling answers them with two disconnected artifacts.       eight mechanical checks including evidence monotonicity.
                                         Context tools produce maps. Aider’s repository map [1],            • A system. A SSAY , a zero-dependency implementation with
                                         packers such as Repomix [2], and committed indexes such                an incremental Merkle-skipped indexer for seven language
                                         as Stacklit [3] compress a repository into a few hundred to a          families, a 600-token situation brief, a signed append-only
                                         few thousand tokens so an agent stops reading files to learn           ledger, a CLI, git hooks, and an MCP server.
                                         what they contain. Governance frameworks produce process           • A mechanical evaluation. Five scripted experiments on
                                         state. Liza [4] is the most disciplined example we know. It            five public repositories and on A SSAY itself, with no model
                                         pairs every doer with an independent reviewer, makes verdicts          in the loop, so every number reproduces to the digit.
                                         binding, and moves the invariants that matter most (no self- The implementation, experiments, results, and paper source are
                                         approval, no forbidden transitions, no merge without review) public.1
                                         out of the prompt and into compiled code, on the grounds that        The paper does not measure how much better language-
                                         instructions bend under pressure and code does not.              model agents perform with A SSAY than without. That study
                                            Each lineage stops where the other starts. A map knows that needs models in the loop and is future work. The claim here
                                         module A depends on module B, but not that the tests covering is narrower and more durable: the floor that holds no matter
                                         A last ran before B changed. A task board knows a reviewer
                                         approved task 17 at commit 9b3c, but not which modules the          1 https://github.com/OmShiv/assay-research
what the model decides can be made cheap and precise, and           configurable depth). With H a collision-resistant hash, the
the structure that provides it also provides the agent’s context.   content hash of a module is the hash of its sorted (path, file
                                                                    hash) pairs:
                      II. BACKGROUND                                                                                     
                                                                         hS (m) = H ⟨(f, H(contentS (f ))) : f ∈ m⟩sorted .
A. Context tools
                                                                    Import resolution yields a dependency relation DS ⊆ M × M,
   The cost of an agent’s first ten minutes in a repository is
                                                                    where (a, b) ∈ DS means some file in a imports some file in b.
documented by the tools built to reduce it. Stacklit’s comparison
                                                                    The relation may contain cycles, as Python packages routinely
reports that packers such as Repomix produce 180k to 400k
                                                                    do. Let C(m) be the strongly connected component of m and
tokens for repositories of 15k to 37k lines, while its structured
                                                                    succ(C) the components reachable from C in one step of the
index produces a few hundred [3]. Aider’s map ranks symbols
                                                                    condensation DAG.
by a reference graph and fits them into a budget [1]. These
                                                                       Definition 1 (Cone and cone hash): The dependency cone
tools share a shape: parse, usually with tree-sitter [6], extract
                                                                    of m is coneS (m) = {m} ∪ {m′ : m →∗ m′ }. The cone hash
exports and imports, group into modules, rank by connectivity
                                                                    is defined on components in reverse topological order of the
or recency, emit a compact artifact. Stacklit adds two ideas
                                                                    condensation DAG:
we keep. The artifact is committed, so every agent and human                           
reads the same map, and regeneration is Merkle-skipped, so a           ĥS (C) = H ⟨(m, hS (m)) : m ∈ C⟩sorted ∥
git hook keeps it fresh at negligible cost. It exposes the map                                             
through the Model Context Protocol [7]. What such maps do                ⟨ĥS (C ′ ) : C ′ ∈ succ(C)⟩sorted , ĥS (m) = ĥS (C(m)).
not carry is any notion of what has been verified. When an             This is a Merkle tree [19] over the condensation DAG
agent claims the tests pass, the map has nothing to say about       with sharing: each component’s hash is computed once and
whether the claim survives the next commit.                         referenced by every component above it. Members of a cycle
B. Governance frameworks                                            share one cone hash, which is right, since they depend on each
                                                                    other. The root hash of the repository is the hash of all module
   Multi-agent frameworks such as MetaGPT [8], ChatDev [9],
                                                                    content hashes and serves as the coarsest binding scope.
AutoGen [10], and CrewAI [11] assign roles and route
messages. Specification-first methods such as Spec Kit [12] B. Claims and bindings
and BMAD [13] make the artifacts explicit. Failure taxonomies      Definition 2 (Claim): A claim is a tuple c =
show why that is not enough. Cemri et al. [14] catalog specifi- (p, S , σ, β, e, a, t): a predicate p (tests-pass, lint-clean, no-
                                                                     c
cation drift, inter-agent misalignment, and weak verification, secrets, behavior-preserved, human-approved, and so on),
and the sycophancy and reward-tampering literature [15, 16] a non-empty set of subject modules S ⊆ M, a scope
                                                                                                              c
documents models that rewrite the test rather than the code σ ∈ {cone, self, repo}, bindings β : S → hashes recorded
                                                                                                            c
when under pressure to appear competent.                        at attestation time, evidence e, an attestor a with a role, and a
   Liza [4] answers with layers: a behavioral contract naming timestamp t.
failure modes and countermeasures, adversarial doer and            For scope cone, β(s) = ĥS (s) at the state in which the
reviewer pairs whose verdicts bind, a task state machine with evidence was produced. Evidence is what the tool observed,
forbidden transitions and bounded iteration enforced by a com- not what the attestor said: the command that ran, its exit code,
piled supervisor, per-task worktrees, and a blackboard [17, 18] a hash of its full output, size and duration, and, when the
recording every transition. Its review protocol is what we output is recognisable test-runner output, the number of tests
borrow most directly. A finding must be answered by accepting, that ran. A claim whose command exited non-zero is recorded
countering, refuting, or escalating. Repeating an assertion is as a failed claim, never discarded. Failure is evidence too.
not a permitted move, and a doer who contests must name            Definition 3 (Freshness): A cone-scoped claim c is fresh in
the concrete harm the requested change would cause. What state S ′ iff β(s) = ĥ ′ (s) for all s ∈ S . Otherwise it is stale.
                                                                                         S                 c
Liza’s blackboard does not carry is the code. Evidence is a
commit SHA and an exit code, and whether a verdict still C. Staleness is sound and minimal
means anything after later changes is answered procedurally,       Write ∆(S, S ′ ) = {m : hS (m) ̸= hS ′ (m)} for the modules
by re-review after rebase, rather than structurally.            whose content changed, including modules added or removed.
   Both lineages need the dependency graph and both compute Import edges derive from file contents, so DS and DS ′ can
or approximate it. Only the first keeps it. The second needs it differ only at modules in ∆. The propositions hold up to hash
at a different moment: not when the agent reads but when the collisions.
gate decides. Keying claims by cone hash lets one graph serve                                           If some module in
                                                                S Proposition 1 (Soundness):     ′                      ′
both moments.                                                     s∈Sc coneS (s) is in ∆(S, S ), then c is stale in S .
                                                                Proof sketch: Let m ∈ coneS (s) ∩ ∆. Then hS ′ (m) ̸= hS (m),
                  III. T HE E VIDENCE G RAPH
                                                                so the component containing m has a different own-part and
A. Modules, hashes, and cones                                   hence a different cone hash. Every component from which
   A repository state S is a finite set of files with contents, C(m) is reachable includes that hash in its successor list,
partitioned into modules M (in A SSAY, directories up to a directly or through a chain of components each changed by
                                                                  after editing core: cone(app) changed,                                               accept: fresh claim, independent reviewer
               before: two claims, both fresh
                                                                              cone(util) did not

              tests                                                  tests
                                                                                                                                                counter              contested          contest, then accept
                                      c-1: tests-pass                                        c-1: tests-pass           attested                                   (up to 3 rounds)
                                                                                                                                                                                                                           accepted
                          app       bound to cone(app)                           app       bound to cone(app)
                                           fresh                                                  stale                                         esc
                                                                                                                                                    ala                     3 rounds
       util                                                   util                                                                                     te                                              c    cept
                                                                                                                                                                                                  an a




                                                                                                                                                                                           ac
                                                                                                                                                                                           hum




                                                                                                                                                                                              c
                                                                                                                                                                                             ep
                        service                                                service




                                                                                                                                                                                                t
                                                                                                                                    re-attest                       escalated




                                                                                                                                                                                                  -fi
                                                                                                                    drift




                                                                                                                                                                                                     nd
    c-2: tests-pass                                        c-2: tests-pass




                                                                                                                                      re




                                                                                                                                                                                                      ngi
                                                                                                                                        fu
  bound to cone(util)                                    bound to cone(util)




                                                                                                                                           te




                                                                                                                                                                                                            +
         fresh                                                  fresh




                                                                                                                                                                                                             ne
                                                                                                                                                                            human refute




                                                                                                                                                                                                               w
                          core                                                   core




                                                                                                                                                                                                                   cla
                                                                                                                                                                                                                     mi
                                                                                                                            stale                                     refuted                                             superseded
Fig. 1: Cone hashes and staleness. Arrows point from a module to what it
depends on. After an edit to core, every module that reaches core (shaded)                                      Fig. 2: Claim lifecycle. Solid arrows are ledger appends, dashed arrows are
has a new cone hash, so the claim on app is stale and the claim on util is                                      computed from the index. A non-terminal claim becomes stale on binding drift
not.                                                                                                            and cannot be accepted until re-attested. Refuted and superseded are terminal.

the same argument, so by induction along reverse topological passing tests on the changed modules. Level 1 requires them
order every such cone hash changes. C(s) reaches C(m), so on the whole radius. Level 2 adds a lint claim and a secrets
ĥS ′ (s) ̸= β(s). If the change instead added or removed an scan on the changed modules and asks for adversarial review.
edge that alters cone(s), the file carrying the import changed, Level 3 adds a human-approved claim. Fraction thresholds
so its module lies in ∆ ∩ coneS (s) or in ∆ ∩ coneS ′ (s) and apply only once the radius has a minimum absolute size, so
the argument applies in that direction.                            a two-module change in a five-module repository is not an
   Proposition 2 (Minimality): If no module in s∈Sc coneS (s) escalation. Where a module’s language has no test runner, the
                                                   S
is in ∆(S, S ′ ), then c is fresh in S ′ .                         obligation asks for a build and a typecheck claim instead, so
Proof sketch: No module in the cone changed content, so no it is never unsatisfiable by construction. The thresholds are
edge originating inside the cone changed, so coneS ′ (s) = policy, stored in the index and overridable per repository. We
coneS (s) with identical content hashes throughout. The cone claim only that they are explicit, monotone in radius and risk,
hash is a deterministic function of exactly those hashes and and cheap.
that structure.
                                                                                       IV. P ROTOCOL AND G ATE
   Together the propositions say cone binding invalidates
a claim if and only if dependency semantics require re- A. Roles and lifecycle
verification. This is the correctness criterion incremental build     Three roles appear in the ledger: doer, reviewer, and human.
systems use to decide whether a cached output can be reused [5]. Any identity may attest. Only reviewers and humans may
A claim is a verifying trace whose key is (p, Sc ), whose input issue verdicts, and no identity may issue one on its own
hashes are the cone hashes, and whose output is the evidence. claim. Checked at append time, this is Liza’s “no self-approval”
The gate’s freshness check is the build system’s “is this trace invariant moved from task to claim granularity. A human
still valid” check, applied to assertions rather than artifacts.   attestation is the escalation authority itself and needs no
   Proposition 3 (Blast radius is the staleness frontier): Let reviewer, though it can still be refuted if its evidence is
BR(∆) = ∆ ∪ {m : m →∗ d for some d ∈ ∆}. Then contradicted.
BR(∆) = {m : ĥS (m) ̸= ĥS ′ (m)}, and the cone-scoped               Fig. 2 shows the derived states. A claim starts attested, or
claims that become stale are exactly {c : Sc ∩ BR(∆) ̸= ∅}.        failed if its evidence exited non-zero. A reviewer may accept it,
Proof sketch: m ∈ BR(∆) iff coneS (m) ∩ ∆ ̸= ∅, which by counter it with a finding, refute it, or escalate it. A countered
Propositions 1 and 2 holds iff ĥ(m) changed.                      claim is contested, and the attestor must respond before any
   Proposition 3 is the identity that makes the two lineages one. further verdict, either by accepting the finding and superseding
The number an agent wants before it edits (how far does this the claim with a stronger one, or by contesting, which requires
reach?) and the number the gate wants after (which evidence naming the concrete harm the requested change would cause.
is now void?) are the same set, computed by one traversal. Three counters escalate automatically, and only a human verdict
Fig. 1 shows it on a five-module example.                          resolves an escalation. Refuted and superseded are terminal.
                                                                   Status is never stored. It is derived from the ledger each time
D. Risk and obligation                                             it is needed, so the ledger cannot disagree with its own history.
   Not every change deserves the same review. Each module Staleness is orthogonal to status and derived from the index:
carries a risk score on absolute scales so it is comparable across an accepted claim whose bindings drifted is stale, and a stale
repositories:                                                      claim cannot be accepted until re-attested.
                         commits    (m)              fan-in(m)
       r(m) = 12 min 1,                   + 12 min 1, 10
                                90d
                                                              
                              20                                 . B. Invariants in code
Churn approximates instability and fan-in approximates the cost                                                    Following Liza’s stance that invariants belong in code rather
of being wrong. For a change touching ∆, the obligation level                                                   than prompts, each of the following is enforced mechanically,
is a function of the radius fraction | BR(∆)|/|M|, the radius                                                   most at ledger-append time and the rest at the gate. An attestor
size, and the maximum risk inside the radius. Level 0 requires                                                  cannot review their own claim. A stale claim cannot be accepted.
No verdict lands on a refuted or superseded claim. Only a              assay init --hook runs it and stages the index, so the
human resolves an escalation. A contest must name a harm               committed index is always current.
and a response must come from the attestor. A contested
claim needs a response before the next verdict. Every ledger           B. Brief, ledger, and interfaces
line carries an HMAC signature under a key held outside the
                                                                          The brief is what an agent reads before opening a source
repository, and an altered or unsigned line fails the gate. The
                                                                       file. It carries the project’s shape (hubs, hot spots, evidence
gate passes only with fresh, independently accepted, plausible
                                                                       commands per language), the change under way (changed
evidence for every requirement.
                                                                       modules, radius, obligation, required evidence), the state of the
C. The gate                                                            evidence (stale claims, open findings, the gate verdict), and a
                                                                       module directory ordered by fan-in and trimmed to a token
   The gate is a function of the index, the ledger, and the            budget, 600 by default. Doer and reviewer start from the same
changed modules. It computes the obligation, then for each             brief. Fig. 3 shows the brief for FastAPI with a hypothetical
required (predicate, module) pair finds the best available claim       edit to its root package.
and classifies it as ok, weak, unreviewed, stale, escalated, failed,      The ledger is a JSON-lines file under .assay/, committed
refuted, or missing. It passes iff every pair is ok and every          as the audit trail. Every line is signed with HMAC-SHA256
signature verifies. Three plausibility checks stand between an         under a key read from the environment or a git-ignored file. In
accepted claim and ok, all floors rather than proofs. A tests-         a supervised deployment the process that executes the agent’s
pass command must look like a test runner that can test the            tool calls holds the key and the agent never sees it. Appends
subject’s language. It must have produced output. And the              take an exclusive lock for a read-validate-write cycle. Entries
number of tests that ran must not drop below what earlier              are never modified. Superseding a claim appends a new one
evidence on an overlapping subject reported, unless a fresh            that names the old.
human-approved claim covers the subject. We call the last
                                                                          The CLI exposes init, index, brief, blast, attest,
check evidence monotonicity. It is the mechanical counterpart
                                                                       review, respond, gate, verify, and mcp. The MCP
of the contract clause “do not delete the failing test”, and it
                                                                       server speaks JSON-RPC over stdio and exposes the same
costs one integer per claim.
                                                                       operations as tools, so Claude Code, Cursor, or any MCP
   The gate guarantees that a merge carries fresh, signed,
                                                                       client can use A SSAY without shelling out. In continuous
independently reviewed evidence for the whole blast radius,
                                                                       integration, assay gate --base origin/main exits
and that the evidence is at least plausible. It does not guarantee
                                                                       non-zero when a change lacks fresh reviewed evidence for
the evidence is sufficient. A reviewer can accept a weak suite,
                                                                       its radius. The implementation is 2,313 lines of Python with
two models from one provider can share a blind spot, and a
                                                                       no runtime dependencies and 30 tests.
doer that can read the signing key can forge the ledger. These
are the boundaries Liza states for its own verdicts [4], restated
                                                                                             VI. E VALUATION
here because a mechanical floor invites over-reading.
                                                                          Five questions, each answered by a scripted experiment with
                     V. I MPLEMENTATION                                no model in the loop. E1: how many tokens does orientation
A. Index                                                               cost with a brief, an index, exploration, or a full dump? E2:
                                                                       how much does Merkle skipping save on rebuilds? E3: what
   assay index lists files through git ls-files so
                                                                       should a claim be bound to? E4: does the gate block the ways
ignore rules apply, hashes and parses each file, resolves imports,
                                                                       a doer can cheat and admit the honest paths? E5: how large is
groups files into modules, computes content and cone hashes,
                                                                       a typical change, and how is obligation distributed?
mines 90 days of history for activity, computes risk, detects
per-language test, build, and typecheck commands, and writes
                                                                     A. Setup
assay.json. Python is parsed with the standard library AST.
TypeScript and JavaScript, Go, Rust, Java and Kotlin, Ruby,             Five public repositories spanning five languages, chosen
and C use conservative regular expressions that recover import to overlap with the comparison set published by Stacklit:
specifiers and exported names. Resolution understands relative Express (JavaScript), Flask (Python), Gin (Go), Axum (Rust),
and package imports, go.mod module paths, Rust crate paths and FastAPI (Python), each a shallow clone with 90 days of
and workspace crates, Java packages, and TypeScript path history, plus A SSAY itself. Table I gives sizes. Tokens are
aliases. A tree-sitter backend can replace any parser behind counted with tiktoken/cl100k_base. Every figure and number
the same interface. Zero dependencies keep the gate runnable below is produced by the released experiment scripts and
anywhere Python runs.                                                injected into this document by paper/make_numbers.py.
   A per-file cache keyed by size and modification time stores A dogfooding run on a private TypeScript Electron application
each file’s hash and parse result, so a rebuild re-parses only files took one real change through attestation, independent review,
whose stat changed before recomputing the graph, the cone and a passing gate with the project’s own typecheck and build
hashes, and the activity summary. This is Stacklit’s Merkle- commands, and surfaced two obligation defects fixed in the
skip idea at file granularity. The pre-commit hook installed by released version.
# Assay brief: fastapi @ d5aba4195b | 195 modules, 1142 files, 113579 lines | python 1138, javascript 4
Commands: python: test pytest, typecheck mypy .; javascript: no test runner | Frameworks: fastapi, flask, pytest
Hubs (touch carefully): fastapi (fan-in 171, risk 1.00); tests (fan-in 41, risk 0.95); fastapi/openapi (fan-in 6, risk ..
Hot 90d: fastapi (38 commits); tests (18 commits); scripts (8 commits); fastapi/dependencies (7 commits); fastapi/open ..
Changed: fastapi -> blast radius 177/195 modules (91%), max risk 1.00 -> level 3 (escalate)
Dependents in radius: docs_src/additional_responses, docs_src/additional_status_codes, docs_src/advanced_middleware, d ..
Required evidence: tests-pass[docs_src/additional_responses, docs_src/additional_status_codes, docs_src/advanced_middl ..
Review: independent reviewer, adversarial, human sign-off, max 3 rounds
Modules (by fan-in):
- fastapi: FastAPI framework, high performance, easy to learn, fast to code, read | exports: FastAPI, BackgroundTasks, ..
- docs_src/additional_responses: additional_responses | exports: Item, Message, read_item(), Item, read_item(), Item, ..
- docs_src/additional_status_codes: additional_status_codes | exports: upsert_item(), upsert_item() | deps: fastapi | ..
- .. 192 more modules: ‘assay module <path>‘ or the MCP tool get_module



                 Fig. 3: The brief for FastAPI with a hypothetical edit to the fastapi package (first lines, truncated at the right margin).

B. E1: tokens to orient                                                                is acceptable for a gate. Cone binding is the only one that is
   Four ways for an agent to learn where things live: a full                           both, and its cost is a property of the repository, not the tool.
dump of every source file, an exploration proxy consisting of a                        E. E4: the gate against an adversarial doer
directory listing plus the ten most-imported files (a conservative
stand-in for the 8 to 12 files an agent reads before acting), the                        A twelve-file Python project with a real pytest suite. Each
modules section of assay.json, and the brief at its default                           scenario starts from a clean copy. A scripted doer edits and
budget.                                                                               makes claims, honestly or not, a scripted reviewer acts, and the
   The brief costs 592 to 635 tokens on the external corpora,                         gate decides. Table IV lists the scenarios and the mechanism
which is 14× to 114× less than the exploration proxy and                              that fired.
216× to 1225× less than a dump. The brief’s cost is flat in                              all 12 scenarios end where the design says they should. The
repository size by construction. The modules section grows                            3 honest paths pass: a leaf edit at level 1, a hub edit at level 3
with the number of modules (FastAPI’s 195 modules, most                               with lint, secrets scan, and human sign-off, and an escalation
of them documentation examples, cost 51,842 tokens) and is                            resolved by a human, which was correctly blocked while
meant to be queried through get_module rather than read                               escalated. The 9 adversarial ones fail, each on the mechanism
whole. The ratios match those Stacklit reports for its own                            built for it. Two rows deserve comment. Failing test deleted
index [3]. What no map carries is the radius, the obligation,                         is the reward-tampering behaviour documented in the model
and the stale claims.                                                                 literature [16]. The doer breaks the code, replaces the test that
                                                                                      would catch it with a placeholder, runs a real test command
C. E2: incremental indexing                                                           that genuinely passes, and gets an accept from a reviewer who
                                                                                      did not look. The gate still fails, because the number of tests
   A warm rebuild with nothing changed is 2× to 5× faster                             that ran dropped from the earlier accepted evidence and no
than a cold build (Table II), and with one edited file it re-parses                   human signed off on the removal. Fake test command passes
exactly that file. On FastAPI (1142 files) a cold build takes                         a real reviewer for the same reason and fails on plausibility.
508 ms and a one-file rebuild 106 ms. The residual cost is the                        The point of E4 is not that these tricks are hard to think of,
history scan and graph recomputation, both cacheable. For a                           but that the floor holds without anyone thinking of them at
pre-commit hook this is below the noise floor of the commit                           review time.
itself.
                                                                                       F. E5: how large is a change
D. E3: what to bind a claim to                                      Across the external corpora, between 0% and 81% of
   One claim per module. For k ∈ {1, 2, 4, 8, 16, 32} we draw modules reach only themselves (Table V). The median single-
100 random sets of k edited modules and compute, under module radius is 0.5% of modules for FastAPI and 1.1%
three binding strategies, the fraction of claims that must be for Axum, while the 90th percentile in Axum is 91.1%,
re-verified (cost) and the fraction that dependency semantics because a handful of hubs (axum-macros/src, reached by 84
say must be re-verified but the strategy leaves fresh (missed). modules) sit under everything. The obligation policy follows
Repo hash binds to the root hash, self hash to the module’s that shape. Most edits are light or standard and the hubs
own content hash, and cone hash is A SSAY’s default.              escalate. A uniform review policy spends the same effort on a
   The result is what Propositions 1 and 2 predict, now with documentation example as on the core package. The obligation
magnitudes (Fig. 4, Table III). At four edited modules, cone spends it where the radius is.
binding re-verifies between 7.9% (FastAPI) and 81.9% (Gin)
of claims where repo binding re-verifies all of them, and self G. Threats to validity
binding misses between 23% and 68% of the claims that must          Import graphs from regular expressions under-approximate
be re-verified. The spread is structural. FastAPI’s graph is wide dependencies (dynamic imports, reflection, generated code),
and shallow, with hundreds of example modules depending which makes cone hashes under-approximate and would
on one package, so a random edit rarely lands in a cone. weaken Proposition 1 in practice. Authoritative edge sources
Axum’s workspace crates form a deep chain, so most edits do. and a tree-sitter backend are the remedy, and edge recall should
Neither the cheap-but-unsound nor the sound-but-total strategy be reported per repository. Module granularity is a directory,
TABLE I: E1: tokens required to orient an agent, by method. Index is the complete assay.json including per-file entries. Modules only is the section an
agent would read whole. Gain is exploration divided by brief.

                                            Repository                   Lines   Modules             Full dump         Exploration             Index   Modules only     Brief     Gain
                                            express                     21,492          35             137,093              17,782            12,447           6,230     635      28×
                                            flask                       18,345          16             134,439              46,673            11,330           3,882     595      78×
                                            gin                         24,192           7             192,995               8,328            10,862           2,379     592      14×
                                            axum                        46,686          90             335,509              45,581            42,112          19,308     621      73×
                                            fastapi                    113,579         195             733,647              68,215           142,463          51,842     599     114×
                                            assay                        4,668           5              58,582              24,430             4,487           1,626     434      56×


                                            Express (35 modules)                                                       Flask (16 modules)                                        Gin (7 modules)
                      100%                                                               100%                                                               100%
                                                repo hash
                                           cone hash (Assay)
 claims re-verified




                      75%                                                                 75%                                                               75%
                                                self hash
                                     self hash: missed invalidations
                      50%                                                                 50%                                                               50%


                      25%                                                                 25%                                                               25%


                       0%                                                                      0%                                                            0%
                             20        21       2    2 2       2  3         4     25                   20         21           2 2      2      3       24          20                    1           22
                                             Axum (90 modules)                                                       FastAPI (195 modules)                                      Assay (52 modules)
                      100%                                                               100%                                                               100%
 claims re-verified




                      75%                                                                 75%                                                               75%


                      50%                                                                 50%                                                               50%


                      25%                                                                 25%                                                               25%


                       0%                                                                      0%                                                            0%
                             20        21           22          23         24     25                   20       21         22        23        24      25          20                   21           22

                                                  edited modules k                                                        edited modules k                                        edited modules k

Fig. 4: E3: fraction of claims re-verified per random edit of k modules (100 trials per point) under three binding strategies. Repo-hash binding re-verifies
everything. Self-hash binding is cheapest but leaves the dotted fraction of required invalidations undetected. Cone binding is the sound minimum.

TABLE II: E2: build time in milliseconds for a cold build, a warm build after
one edited file, and a warm build with no change. Gain is cold divided by                                                    locating code. Long-context degradation [23] motivates com-
warm.                                                                                                                        pactness beyond cost. None bind verification to structure.
      Repository             Files      Cold       One edit        No change     Gain (edit)        Gain (no change)
                                                                                                                                Agent frameworks and accountability. Multi-agent frame-
      express                 141         45              24                24         1.9×                    1.9×
      flask                    83         94              32                23         3.0×                    4.1×          works [8, 9, 10, 11] and agent-computer interfaces such as
      gin                      98         35              20                20         1.7×                    1.7×          SWE-agent [24] and OpenHands [25] shape what agents
      axum                    305         62              38                34         1.6×                    1.8×
      fastapi                1142        508             106                93         4.8×                    5.4×          can do. Failure taxonomies [14] and the reward-tampering
      assay                    31         56              31                22         1.8×                    2.5×
                                                                                                                             literature [15, 16] explain why outcomes need verification the
                                                                                                                             agent cannot game. Liza [4] is the closest system in spirit
TABLE III: E3 at k = 4 edited modules: re-verification cost per strategy and
the fraction of required invalidations the self-hash strategy misses.                                                        and the source of our protocol. Our contribution relative to it
                                                                                                                             is the binding of verdicts to content, which turns “re-review
       Repository             Modules          Repo hash           Cone hash     Self hash          Self hash misses
                                                                                                                             after rebase” from procedure into arithmetic. Long-horizon
       express                        35              100%               16.6%      11.4%                    27.8%
       flask                          16              100%               66.7%      25.0%                    45.7%           measurements [26] suggest unattended runs will lengthen,
       gin                             7              100%               81.9%      57.1%                    29.3%           raising the value of a floor that needs no attention.
       axum                           90              100%               66.3%       4.4%                    67.6%
       fastapi                       195              100%                7.9%       2.1%                    22.7%
       assay                           5              100%               87.4%      80.0%                     7.4%              Content addressing, build systems, provenance. Merkle
                                                                                                                             trees [19] underlie git, Nix [27], and Bazel’s action cache [28].
and a large directory inflates radii. All conditions share one                                                               Mokhov et al. [5] give the vocabulary of verifying traces
tokenizer. The exploration proxy stands in for agent behaviour                                                               that our ledger instantiates for assertions. in-toto [29] and
rather than measuring it. E4 measures a floor against scripted                                                               SLSA [30] attest to what ran over which inputs in a supply
behaviours designed by the same people who designed the                                                                      chain. A claim with its bindings, evidence, and signature is
checks, so independent red-teaming is warranted. Risk and the                                                                structurally an in-toto link moved into the inner loop, with
obligation thresholds are policy.                                                                                            the dependency cone as the input set. Proposition 3 is also a
                                                                                                                             regression test selection oracle in the manner of Ekstazi [31],
                                               VII. R ELATED W ORK                                                           with the dependency graph shared with the agent’s context.
  Context for agents. Repository maps and packers [1, 2, 3],                                                                   Argumentation. The counter and contest exchange is a
code intelligence indexes such as SCIP [20], and structure-                                                                  Toulmin argument [32]: evidence is the grounds, the cone
aware retrieval in AutoCodeRover [21] and the deliberately                                                                   binding is the warrant for this code state, a counter is a rebuttal,
minimal Agentless [22] all reduce the tokens an agent spends                                                                 and when the binding drifts the warrant lapses.
TABLE IV: E4: scripted doer behaviours and the gate’s decision. A rejected ledger entry is treated as absent, so the forged scenario reports only the signature
mechanism.

                    Scenario                                                             Gate    Mechanisms that fired
                    honest leaf edit (L1): tests on the radius, independent accept       PASS    none
                    honest hub edit (L3): + lint, secrets scan, human sign-off           PASS    none
                    no evidence at all                                                   FAIL    coverage
                    evidence covers the edited module, not its dependents                FAIL    coverage
                    evidence produced before the edit (stale)                            FAIL    freshness
                    doer approves own claim                                              FAIL    separation
                    forged ledger entries (claim + verdict)                              FAIL    signature
                    code broken, real test run recorded                                  FAIL    exit code
                    code broken, fake test command                                       FAIL    plausibility
                    code broken, failing test deleted                                    FAIL    monotonicity
                    reviewer refutes the claim                                           FAIL    review
                    three rounds, escalated, human resolves                              PASS    review

TABLE V: E5: single-module blast radius as a fraction of all modules, and
the number of modules whose edit falls at each obligation level.                 of the dependency cone of the code they cover makes staleness
                                                                                 a hash comparison, makes blast radius and invalidation the
 Repository    Modules   Median radius   p90 radius    L0    L1    L2   L3
                                                                                 same set, and lets a merge gate that consults no model be
 express            35           5.7%         8.6%     13    22     0     0
 flask              16           6.2%        87.5%     13     0     0     3
                                                                                 both precise and cheap. A SSAY is a small, dependency-free
 gin                 7          57.1%        71.4%      1     1     1     4      implementation of that idea, and the experiments show the
 axum               90           1.1%        91.1%     66     0     0    24
 fastapi           195           0.5%         1.0%    149    38     0     8
                                                                                 floor holding on real repositories and against scripted attacks.
 assay               5          20.0%        20.0%      4     0     1     0      The best summary is also the design rule: claims should decay
                                                                                 with the code.
              VIII. L IMITATIONS AND F UTURE W ORK
                                                                                                          ACKNOWLEDGMENT
    Parsers. Regular-expression extraction is the largest source
                                                                                    The protocol and the “mechanical, not instructional” stance
of unsoundness. A tree-sitter backend and, where available,
                                                                                 come from Liza. The committed, Merkle-skipped index and its
authoritative edge sources (go list, tsc --listFiles,
                                                                                 MCP surface come from Stacklit. Assay shares no code with
cargo metadata) should replace it, and edge recall should
                                                                                 either project and would not exist without both. An AI coding
be a reported property of every index.
                                                                                 assistant helped produce the figures and tables. The authors
    Granularity. Directory modules are coarse. File-level cones
                                                                                 verified every claim and number and are responsible for the
are a straightforward extension. Symbol-level cones need a
                                                                                 content.
real call graph.
    Evidence adequacy. The gate checks plausibility, not                                                        R EFERENCES
sufficiency. Coverage deltas on changed lines and per-test                           [1] P. Gauthier, “Aider: Building a better repository map
identities are the next mechanical checks, and per-test identities                       with tree-sitter,” https://aider.chat/2023/10/22/repomap.
would make monotonicity exact.                                                           html, 2023.
    Key placement. The floor depends on the signing key being                        [2] K. Yamada, “Repomix: Pack your codebase into AI-
outside the agent’s reach. We describe the deployment pattern                            friendly formats,” https://github.com/yamadashy/repomix,
but do not enforce it.                                                                   2024.
    Beyond tests. The same binding covers documentation (a                           [3] Glincker, “Stacklit: AI-ready codebase indexing,” https:
documents claim goes stale when the code it describes moves),                            //github.com/glincker/stacklit, 2026, accessed September
lockfiles (no-known-vulnerabilities bound to the lockfile hash),                         2026.
infrastructure plans, and monorepo federation through a depen-                       [4] Liza contributors, “Liza: Orchestration of Accountable
dency’s version hash as a leaf. A pull request organized by                              Agents,” https://github.com/liza-mas/liza, 2026, accessed
claims and radius would show a reviewer what was verified,                               September 2026.
what went stale, and what is still owed.                                             [5] A. Mokhov, N. Mitchell, and S. Peyton Jones, “Build
    Models in the loop. The study this paper does not contain                            Systems à la Carte,” Proceedings of the ACM on Pro-
measures resolved rate, tokens to first correct patch, tokens                            gramming Languages, vol. 2, no. ICFP, p. 79:1 to 79:29,
to gate pass, and the rate at which the gate blocks patches                              2018.
that pass a harness but fail hidden tests, across arms with and                      [6] M. Brunsfeld, “Tree-sitter: An incremental parsing system
without the brief and the gate, on a benchmark such as SWE-                              for programming tools,” https://tree-sitter.github.io, 2018.
bench Verified [33]. We have designed it and will preregister                        [7] Anthropic,     “Model       Context     Protocol,”     https:
it.                                                                                      //modelcontextprotocol.io, 2024.
                                                                                     [8] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng,
                           IX. C ONCLUSION
                                                                                         C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou,
  Context and accountability for coding agents are the same                              C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, “MetaGPT:
problem seen at two times. Keying claims by the Merkle hash                              Meta Programming for a Multi-Agent Collaborative
     Framework,” in International Conference on Learning                Demystifying LLM-based software Engineering Agents,”
     Representations (ICLR), 2024.                                      arXiv preprint arXiv:2407.01489, 2024.
 [9] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li,             [23] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua,
     C. Yang, W. Chen, Y. Su, X. Cong, J. Xu, D. Li,                    F. Petroni, and P. Liang, “Lost in the Middle: How
     Z. Liu, and M. Sun, “ChatDev: Communicative Agents                 Language Models use Long Contexts,” Transactions of
     for Software Development,” in Proceedings of the 62nd              the Association for Computational Linguistics, vol. 12, p.
     Annual Meeting of the Association for Computational                157 to 173, 2024.
     Linguistics (ACL), 2024, p. 15174 to 15186.                   [24] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao,
[10] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang,        K. Narasimhan, and O. Press, “SWE-agent: Agent-
     X. Zhang, S. Zhang, J. Liu, A. H. Awadallah, R. W. White,          Computer Interfaces Enable Automated Software Engi-
     D. Burger, and C. Wang, “AutoGen: Enabling Next-Gen                neering,” in Advances in Neural Information Processing
     LLM Applications via Multi-Agent Conversation,” arXiv              Systems (NeurIPS), 2024.
     preprint arXiv:2308.08155, 2023.                              [25] X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge,
[11] CrewAI, “CrewAI: Framework for orchestrating role-                 J. Pan, Y. Song, B. Li, J. Singh, H. H. Tran, F. Li,
     playing, autonomous AI agents,” https://github.com/                R. Ma, M. Zheng, B. Qian, Y. Shao, N. Muennighoff,
     crewAIInc/crewAI, 2023.                                            Y. Zhang, B. Hui, J. Lin, R. Brennan, H. Peng, H. Ji,
[12] GitHub, “Spec Kit: Spec-Driven development toolkit,”               and G. Neubig, “OpenHands: An Open Platform for AI
     https://github.com/github/spec-kit, 2025.                          Software Developers as Generalist Agents,” arXiv preprint
[13] BMAD contributors, “BMAD method: Breakthrough                      arXiv:2407.16741, 2024.
     Method for Agile AI-Driven development,” https://github.      [26] T. Kwa, B. West, J. Becker, A. Deng, K. Garcia, M. Hasin,
     com/bmad-code-org/BMAD-METHOD, 2025.                               S. Jawhar, M. Kinniment, N. Rush, S. Von Arx, R. Bloom,
[14] M. Cemri, M. Z. Pan, S. Yang, L. A. Agrawal, B. Chopra,            T. Broadley, H. Du, B. Goodrich, N. Jurkovic, L. H. Miles,
     R. Tiwari, K. Keutzer, A. Parameswaran, D. Klein,                  S. Nix, T. Lin, C. Painter, N. Parikh, D. Rein, L. J. K.
     K. Ramchandran, M. Zaharia, J. E. Gonzalez, and                    Sato, H. Wijk, D. M. Ziegler, E. Barnes, and L. Chan,
     I. Stoica, “Why do Multi-Agent LLM systems fail?” arXiv            “Measuring AI ability to complete long software tasks,”
     preprint arXiv:2503.13657, 2025.                                   arXiv preprint arXiv:2503.14499, 2025.
[15] M. Sharma, M. Tong, T. Korbak, D. Duvenaud, A. Askell,        [27] E. Dolstra, M. de Jonge, and E. Visser, “Nix: A Safe
     S. R. Bowman, N. Cheng, E. Durmus, Z. Hatfield-Dodds,              and Policy-Free System for Software Deployment,” in
     S. R. Johnston, S. Kravec, T. Maxwell, S. McCandlish,              Proceedings of the 18th Large Installation System Admin-
     K. Ndousse, O. Rausch, N. Schiefer, D. Yan, M. Zhang,              istration Conference (LISA), 2004, p. 79 to 92.
     and E. Perez, “Towards understanding Sycophancy in Lan-       [28] Google, “Bazel: a fast, scalable, multi-language build
     guage Models,” in International Conference on Learning             system,” https://bazel.build, 2015.
     Representations (ICLR), 2024.                                 [29] S. Torres-Arias, H. Afzali, T. K. Kuppusamy, R. Curt-
[16] C. Denison, M. MacDiarmid, F. Barez, D. Duvenaud,                  mola, and J. Cappos, “in-toto: Providing farm-to-table
     S. Kravec, S. Marks, N. Schiefer, R. Soklaski, A. Tamkin,          guarantees for bits and bytes,” in 28th USENIX Security
     J. Kaplan, B. Shlegeris, S. R. Bowman, E. Perez, and               Symposium, 2019, p. 1393 to 1410.
     E. Hubinger, “Sycophancy to Subterfuge: Investigating         [30] OpenSSF, “SLSA: Supply-chain Levels for Software
     Reward-Tampering in large Language Models,” arXiv                  Artifacts,” https://slsa.dev, 2021.
     preprint arXiv:2406.10162, 2024.                              [31] M. Gligoric, L. Eloussi, and D. Marinov, “Practical
[17] H. P. Nii, “The Blackboard model of Problem Solving and            Regression Test Selection with Dynamic File Dependen-
     the Evolution of Blackboard Architectures,” AI Magazine,           cies,” in Proceedings of the International Symposium on
     vol. 7, no. 2, p. 38 to 53, 1986.                                  Software Testing and Analysis (ISSTA), 2015, p. 211 to
[18] L. D. Erman, F. Hayes-Roth, V. R. Lesser, and D. R.                222.
     Reddy, “The Hearsay-II Speech-Understanding system:           [32] S. E. Toulmin, The Uses of Argument.           Cambridge
     Integrating Knowledge to Resolve Uncertainty,” ACM                 University Press, 1958.
     Computing Surveys, vol. 12, no. 2, p. 213 to 253, 1980.       [33] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press,
[19] R. C. Merkle, “A Digital Signature based on a Conven-              and K. Narasimhan, “SWE-bench: Can Language Models
     tional Encryption Function,” in Advances in Cryptology             resolve Real-World GitHub Issues?” in International
     (CRYPTO), 1987, p. 369 to 378.                                     Conference on Learning Representations (ICLR), 2024.
[20] Sourcegraph, “SCIP Code Intelligence Protocol,” https:
     //github.com/scip-code/scip, 2022.
[21] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury,
     “AutoCodeRover: Autonomous Program Improvement,” in
     Proceedings of the International Symposium on Software
     Testing and Analysis (ISSTA), 2024, p. 1592 to 1604.
[22] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang, “Agentless:
