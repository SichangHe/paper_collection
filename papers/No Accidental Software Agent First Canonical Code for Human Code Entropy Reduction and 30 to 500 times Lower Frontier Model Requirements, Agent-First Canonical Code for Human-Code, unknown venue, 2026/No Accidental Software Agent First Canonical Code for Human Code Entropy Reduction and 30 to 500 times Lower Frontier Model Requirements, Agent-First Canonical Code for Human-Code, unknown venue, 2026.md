                                                           No Accidental Software
                                                 Agent-First Canonical Code for Human-Code
                                                  Entropy Reduction and 30×–500× Lower
                                                        Frontier-Model Requirements
                                                                                                         Jepson Taylor
                                                                                                     NeverHuman Research
                                                                                                             Abstract
arXiv:2606.14357v1 [cs.SE] 12 Jun 2026




                                                   The number is the hook, but the denominator is the science: frontier coding models are paying to learn human-code
                                              entropy, not just code. Raw human repositories contain behavior, incidents, tests, edge cases, migrations, product judgment, and
                                              operational scar tissue worth preserving, but those signals are entangled with accidental representation: language fashion, framework
                                              churn, naming drift, folder folklore, duplicated contracts, generated-source confusion, dependency rituals, continuous-integration
                                              dialects, weak proof routes, and review customs built for humans rather than agents. A coding agent pays for this entropy four
                                              times: during training, during context gathering, during reasoning/tool/retry loops, and during human review. This paper proposes
                                              agent-first canonical code: a governed, proof-carrying substrate that ports routine product software into canonical profiles, behavior
                                              cells, generated truth, typed change algebra, proof lanes, constrained edit grammars, reasoning digests, semantic patch cells, runtime
                                              negative memory, and proof-carrying change objects before training and before agent operation.
                                                   The claim is deliberately ambitious, but every range has a denominator. Detailed conservative, central, and aggressive bands
                                              are hypotheses reported in the tables, not measured frontier results, and they must not be multiplied into a miracle. The decisive
                                              endpoint is all-in cost per verified correct change: source tokens, context, reasoning, tools, verification, security, provenance, review,
                                              failed loops, downstream defects, and amortized foundry cost under the same acceptance oracle.
                                                   The theoretical endpoint is the No-Accident Horizon: under a declared oracle and supported routine-product distribution, all
                                              removable accident can vanish only until the residual floor of novelty, evidence, governance, risk, and future optionality remains;
                                              a mature foundry therefore has a strongest defensible planning limit near 100× all-in verified-change cost reduction, not an
                                              unrestricted all-code guarantee.
                                                   The theoretical spine is quotienting software by behavior equivalence under a declared oracle. Many behavior-equivalent
                                              human encodings should collapse to one governed representative plus evidence, while residual novelty, legal risk, security exposure,
                                              and domain mismatch remain explicit in a disposition ledger. The limit is M INIMUM F UNCTIONAL D ESCRIPTION L ENGTH: the
                                              shortest canonical behavior specification, evidence bundle, proof obligations, and renderer that produce a working system under
                                              behavior, security, migration, provenance, and review constraints. Preliminary QLoRA evidence on Qwen2.5-Coder-14B shows
                                              that 64,088 canonically translated trajectories are learnable and suppress tested forbidden-language markers; it does not establish
                                              behavior preservation, scaling economics, or verified-change cost. The contribution is a falsifiable research program whose decisive
                                              endpoint is amortized cost per verified correct change.
                                                                                                           Index Terms
                                                  code language models, agent-first programming, canonical code, training data, corpus compression, behavior cells, software
                                              engineering, model efficiency
                                          One-sentence thesis. Raw repositories force models to learn both product behavior and accidental implementation orbits;
                                          canonical proof-carrying behavior lets them spend training, inference, review, and verification budget on verified change
                                          instead of rediscovering local software folklore.

                                         What would make this undeniable. On paired raw versus canonical repositories from the same lineage, the same
                                         model must spend materially fewer source, context, reasoning, tool, retry, and reviewer tokens to produce an accepted
                                         proof-carrying change. Only after that same-model result holds should specialist scaling curves be allowed to justify the
                                         30×–150× central training-token claim and the 8.3×–10× dense-active serving-speed claim.

                                                                 I. I NTRODUCTION                                   ing/action/retry tokens, and 10×–50× lower verified-change
                                                                                                                    cost on supported canonical product work. The denominator
                                            The conservative claim is already large: 10×–30× fewer                  comes first because the thesis is not “better style.” It is that
                                         training tokens to a fixed accepted-change capability, 3×–                 frontier coding models are paying to learn the wrong object.
                                         10× fewer context/reasoning/tool/retry tokens per verified
                                         change, and 3×–10× lower all-in cost per verified correct                    Frontier coding models are trained on a software record
                                         change after foundry amortization. The central claim is larger:            built by humans for humans. That record contains valuable
                                         30×–150× training-token efficiency, 10×–100× fewer reason-                 behavior, but it is not a canonical representation of software. It
                                                                       TABLE I
                            T HE H OOK : C ONSERVATIVE - TO -AGGRESSIVE PAYOFF R ANGES BY M EASUREMENT D ENOMINATOR

Outcome denominator                     Conservative            Central              Aggressive    What must be measured
Training tokens to fixed accepted-       10×–30×               30×–150×            150×–1,000×     Paired raw/canonical scaling curves to the same hidden-
change target                                                                                      test accepted-change capability.
Context, reasoning, tool, and retry       3×–10×               10×–100×           100×–10,000×     Files opened, planning tokens, hidden reasoning budget
tokens per verified change                                                                         where measurable, tool calls, failed repair loops, and
                                                                                                   validation reruns.
Cost per verified correct change          3×–10×               10×–50×             50×–1,000×      End-to-end dollars including source/context/action tokens,
                                                                                                   serving, verification, security/provenance, review, down-
                                                                                                   stream defects, and amortized foundry cost.
Same-model verified-change wall-           2×–5×                5×–20×              20×–100×       End-to-end elapsed time from issue receipt to accepted
clock                                                                                              proof-carrying patch under equal tool and reviewer bud-
                                                                                                   gets.
Dense-active inference speed sce-          3×–5×               8.3×–10×              10×–20×       Conditional only: matched-quality canonical specialist ver-
nario                                                                                              sus 1T-class dense-active baseline on supported canonical
                                                                                                   work.
Dense-active      infrastructure       67%–80% lower        88%–90% lower        90%–95% lower     Active-parameter, memory, batching, utilization, MoE,
cost/token                                                                                         context, and verification-overhead accounting.
Effective action/representation          10×–40×               40×–150×             100×–300×      Entropy of valid behavior-equivalent encodings and legal
space                                                                                              edit choices after contracts, profiles, and proof lanes are
                                                                                                   fixed.
Foundry amortization and reuse             2×–5×               10×–100×           100×–10,000×     Reuse of behavior cells, semantic patches, negative
                                                                                                   memory, generated projections, and proof receipts across
                                                                                                   independent product lineages.


                                                                     TABLE II
                                             E XTERNAL FACTS THE C ANONICAL -C ODE T HESIS M UST E XPLAIN

 Observed fact                          Why it matters                                            Canonical-code interpretation
 Public software is massive and         Broad code models pay to learn the whole human archive.   The archive is behavior raw material, not necessarily the
 multi-language: The Stack v2 con-                                                                optimal training substrate.
 tains over 3B files in 600+ lan-
 guages and StarCoder2 trains on
 3.3T–4.3T tokens across 619 lan-
 guages [1], [2].
 Duplication is structural: DéjàVu    Human code repeats behavior and representation.           Cells and semantic patches should capture repeated
 found 85M unique files among                                                                     behavior directly.
 428M files across 4.5M non-
 fork projects, and Jupyter studies
 found more than 70% exact snip-
 pet copies [3], [4].
 Agent benchmarks are brittle:          Passing tests is not equivalent to preserving behavior.   Ports and changes need evidence tiers, hidden tests,
 SWE-bench Verified improves cu-                                                                  fuzzing, replay, mutation tests, and proof receipts.
 ration, but UTBoost found insuf-
 ficient tests and erroneous pass
 labels in SWE-bench-family re-
 sults [5], [6].
 Agent cost matters: resource-          Accuracy without cost accounting can be economically      The denominator must be cost per verified correct change.
 constrained evaluation shows why       misleading.
 resolve rate alone hides token,
 time, and failure cost [7], [8].
 CI/security sprawl is real: re-        Repository operations are part of the software behavior   CI, secrets, permissions, and release policy must become
 cent GitHub Actions studies re-        surface.                                                  canonical substrate objects.
 port workflow heterogeneity and
 security-practice gaps, and Git-
 Guardian reported 28.65M new
 public-GitHub secrets in 2025 [9]–
 [12].



is a survival archive: hundreds of languages, millions of local                    rituals that were never designed for autonomous agents. A
conventions, duplicated frameworks, inconsistent naming, weak                      coding agent pays for that archive four times: during training,
tests, dependency sprawl, build folklore, continuous-integration                   during context gathering, during reasoning/tool/retry loops, and
(CI) dialects, repository settings, access policies, and release                   during human review.
                                                                     TABLE III
                                                        F RONT-D OOR M EASUREMENT L EDGER

 Question                      Primary denominator                    First test                                    Failure mode
 Does the substrate help be-   Same-model cost per accepted           Broad model on paired raw vs. canonical       Canonical form looks cleaner but
 fore new training?            change                                 repositories with the same issue lineage,     does not reduce files opened, con-
                                                                      hidden tests, and reviewer rubric.            text/reasoning tokens, tool calls, failed
                                                                                                                    lanes, or review.
 Does canonical data train     Tokens-to-target accepted-change       Paired scaling curves from the same           Canonical data requires similar tokens,
 more efficiently?             capability                             raw/canonical lineage.                        similar model scale, or larger models for
                                                                                                                    the same accepted-change target.
 Does the serving denomina-    Dense-active          infrastructure   Compare a broad dense-active baseline         Throughput gains disappear after batch-
 tor improve?                  cost/token and token/sec at            against a canonical specialist on sup-        ing, memory, context, verification, or
                               matched quality                        ported canonical work.                        quality corrections.
 Does behavior survive port-   Preservation tier and hidden oracle    Differential tests, replay, fuzzing, con-     Important compatibility ghosts are lost
 ing?                          pass rate                              tracts, migration checks, security checks,    or security/migration regressions rise.
                                                                      and human review.
 Does the economics close?     All-in cost per verified correct       Foundry amortization plus training, serv-     Foundry and verification overhead con-
                               change                                 ing, tools, verification, failed loops, and   sume the gains.
                                                                      review.



   The end-of-road story is stark. In the conservative version, examples from the old distribution. Canonical porting changes
canonicalization is an engineering discipline that makes coding the distribution and the action substrate. The standard constrains
agents cheaper and more reliable by cutting routine repository language roles, file grammar, naming, dependency ownership,
search and failed repair loops. In the central version, it becomes generated boundaries, database truth, continuous integration,
a new data substrate: fewer legal encodings, fewer legal edit repository policy, build/test commands, migration policy, proof
paths, and lower tokens-to-target capability. In the aggressive lanes, and agent-readable edit scope. Observable behavior is
version, routine product software approaches a behavior- preserved, rejected, or tiered according to an explicit evidence
genome regime in which most CRUD, auth, policy, migration, envelope; arbitrary human degrees of freedom collapse only
deployment, observability, billing, notification, workflow, and when they are not part of that envelope. The external-reader
integration behavior is assembled from proof-carrying cells, claim is precise: human repositories are improvable because
while bespoke code is reserved for minimum viable novelty. they mix durable behavior with accidental representation, not
The paper is ambitious because the upside is enormous; it is because human behavior, product judgment, operational lessons,
defensible only because every large number is tied to a named or edge cases are disposable.
denominator and a falsification test.                                 This is a deliberately strong position: for every supported
   The scale is enormous. GitHub reported 395 million public product-software concern there should be one governed way
and open-source repositories in Octoverse 2025, roughly 230 to express it, and for other software classes there should
new repositories per minute, and a major shift in the most- be a secondary governed profile rather than local preference.
used language [13]. The Stack v2 reports 67.5TB full, 32.1TB Humans do not merely choose different surface styles; they
deduplicated, roughly 900B train-full tokens, over 3B files, create mutually incompatible local dialects for routing, testing,
and 658 languages [1]. StarCoder2 was trained on 3.3T–4.3T continuous integration, authorization, secrets, migrations, fea-
tokens across 619 programming languages [2]. Kimi K2 reports ture flags, deployment, observability, and review. Those dialects
a 1T-total-parameter mixture-of-experts model with 32B active may work locally, but they are training noise for agents and
parameters and 15.5T pretraining tokens [14], [15]. Modern reasoning overhead at inference time. For supported classes, the
code-model work shows the same field-level direction: more falsifiable claim is that nearly every nontrivial human-authored
languages, longer context, more tokens, more data curation, repository contains reducible accidental degrees of freedom:
and more agentic training rather than a smaller human-code duplicate behavior, noncanonical representation, generated-truth
target [16], [17].                                                 drift, unconstrained edit surface, missing proof receipts, or
   The redundancy is also enormous. DéjàVu analyzed 4.5 ungoverned policy.
million non-fork GitHub projects and found that only 85 million       The decisive experiment is not a better-looking repository.
of 428 million files were unique—about 70% were clones It is a same-model, same-lineage comparison: original human
of previously created files [3]. Jupyter notebook code shows repository versus canonical repository, same issue, same
similar patterns: more than 70% of code snippets were exact behavior contract, same hidden tests, same reviewer rubric, and
copies [4]. Software has long been known to be highly repetitive a complete ledger of files opened, context tokens, reasoning
and predictable [18].                                              tokens, tool calls, invalid edits, failed proof lanes, review
   The thesis is stronger than filtering or deduplication: the burden, wall time, and accepted-patch rate. If a broad model
available training code should be ported into an agent-first performs materially better on the canonical repository before
canonical standard before training. Filtering selects cleaner a canonical specialist is trained, then substrate compression is
real. If it does not, the thesis fails early.                           moves entropy into metadata, the thesis should be rejected or
   This paper makes the case through nine explicit assumptions,         narrowed.
each with falsification criteria, a compression frontier catalog,
                                                                         III. T HE M ISSING T HEORETICAL M OVE : T RAIN ON THE
preliminary training evidence, and a paired evaluation design.
                                                                                        Q UOTIENT, N OT THE O RBIT
The core falsifiable thesis is simple: after controlling for
behavior and task, canonical proof-carrying software should                The deepest version of the thesis is not that code can be
lower same-model search cost now, lower tokens-to-target                standardized. It is that software learning should be quotiented by
accepted-change capability under paired scaling curves later,           behavior. Let P be the set of source-level programs, repositories,
and lower amortized cost per verified correct change in                 configurations, schemas, tests, and deployment artifacts. Let
production field trials. If those three gates fail, no title, figure,   O be a declared behavior oracle: public tests, hidden tests,
or compression catalog rescues the claim.                               trace equivalence, API contracts, migration replay, security
                                                                        policies, performance envelopes, accessibility checks, runtime
 II. P OSITIONING : W HAT E XISTING W ORK P ROVES , AND                 invariants, and accepted incompatibility dispositions. Define
                    W HAT I T D OES N OT                                an equivalence relation
   Adjacent work strongly supports the premise that software                     p1 ∼O p2 ⇐⇒ O(p1 ) = O(p2 )                     (1)
contains compressible regularity, but it does not yet prove
the thesis in this paper. Naturalness results show that code up to the declared preservation tier. The human soft-
is unusually repetitive and predictable [18]; clone studies ware corpus samples many points in the syntactic orbit
show massive exact and near-exact duplication in public [p]O : Python/FastAPI, Java/Spring, Node/Express, Ruby/Rails,
repositories [3], [4]; modern code LLMs show that trillion-token Go/Gin, C#/ASP.NET, hand-written DTOs, generated DTOs,
corpora can learn broad programming competence [2], [14], imperative migrations, declarative migrations, bespoke CI, and
[16], [17]; and repository-level benchmarks show that agents ad hoc review rules can all encode the same product behavior.
can now operate over real projects, although contamination, A raw code model learns both the quotient P/∼O and the orbit
weak tests, and distribution mismatch make static benchmarks noise inside each class. A canonical foundry instead learns a
fragile [5], [6], [19], [20]. This paper’s stronger claim is versioned normal-form map
different: the target distribution itself is wrong. The right move
                                                                                         κ : [p]O → (s, e, r, d),                (2)
is not only higher-quality filtering, more synthetic tasks, or
larger context windows. It is to transform the code archive into where s is the shortest accepted canonical specification, e
a canonical behavior-and-change substrate before training.         is the evidence bundle, r is the renderer/generator, and d is
   The strongest allies are not only code LLM papers. They the disposition ledger for non-preserved behavior, legal risk,
are program-analysis and programming-language systems that security defects, or domain mismatch.
already separate meaning from textual accident. OpenAPI and           This distinction clarifies why the proposal is more ambitious
Protocol Buffers show that one source of truth can generate than deduplication. Deduplication removes copied files. Near-
multiple projections of an interface [21], [22]. MLIR shows that deduplication improves pretraining quality by removing re-
domain-specific dialects can lower through reusable compiler peated text. Canonical quotienting removes degrees of freedom
infrastructure rather than forcing every domain into one flat that should not be in the model’s target language at all. The
representation [23]. Coccinelle shows that semantic patches can model is no longer asked to learn every valid implementation
encode collateral evolutions more compactly than hand-written orbit; it is asked to learn canonical representatives plus the
diffs [24]. CodeQL shows that code can become queryable proof obligations that make the representative behaviorally
semantic data for large-scale vulnerability reasoning [25]. E- acceptable.
graphs show how equivalence classes of programs can be                The theory also explains why the proposed breakthrough
represented compactly for rewrite search [26]. DreamCoder and can coexist with modern scaling laws. Scaling-law work
library-learning systems show that repeated programs can be implies that data quality and token efficiency matter; Chinchilla-
compressed into reusable abstractions that improve search [27]. style compute-optimal training links model size and training
Agent-first canonical code combines these threads into one tokens under a compute budget [28]. Canonical code does
substrate-level bet: learn from human software history, but do not repeal scaling laws. It changes the data distribution so
not force future agents to imitate its incidental coordinates.     that a token is closer to irreducible behavior and farther from
   This positioning also defines the paper’s burden of proof. A accidental representation. If the canonical token stream has
reviewer should not accept the claim because the standard is lower conditional entropy and fewer irrelevant action branches,
elegant. The claim earns belief only if paired experiments show the same physical training and inference budget should buy
lower cost per verified correct change, lower tokens-to-target more verified software capability.
accepted-change capability, lower action branching, preserved         A useful analogy is compiler IR. LLVM and MLIR do
behavior at declared evidence tiers, and lower infrastructure not eliminate source languages; they provide structured in-
cost/token where model-size claims are invoked. Conversely, termediate forms that make analysis, lowering, optimization,
if canonicalization removes useful implementation diversity, and reuse tractable [23], [29]. The canonical-code claim is
harms robustness, fails to amortize foundry cost, or merely that product software needs a higher IR: entities, permissions,
                                                                 TABLE IV
                                       F ROM R AW-C ODE I MITATION TO B EHAVIOR -Q UOTIENT L EARNING

 Layer                       Raw-code learning target                                          Canonical quotient target
 Representation              All languages, frameworks, layouts, generated artifacts,          One governed representative per behavior class, plus explicit
                             dependency rituals, and local repair customs.                     profile escape hatches.
 Generalization              Infer semantics through many surface encodings.                   Learn behavior primitives, typed deltas, proof obligations,
                                                                                               and legal edit forms.
 Search                      Explore file trees and patch locations in a high-entropy orbit.   Route to cells, owned files, generated truth, and proof lanes.
 Verification                Interpret arbitrary tests, logs, CI conventions, and reviewer     Consume structured proof receipts and behavior-oracle
                             expectations.                                                     deltas.
 Memory                      Remember past trajectories as chat/log traces.                    Compile successful and failed trajectories into reasoning
                                                                                               digests, semantic patch cells, and negative memory.
 Economic unit               Patch accepted after ad hoc reasoning and review.                 Proof-carrying change accepted under a cost ledger.



policies, effects, state machines, migrations, API contracts,                   We report the following distinct reductions:
observability, proof obligations, rollout envelopes, and runtime                                 raw source tokens
invariants. Source code is then a projection, not the source of                  Rsource =                                 ,                  (4)
                                                                                             canonical source tokens
truth. Coccinelle’s semantic patches show that many source                                       H(raw valid forms)
changes are better represented as semantic transformations than                 Rentropy =                                   ,                (5)
                                                                                             H(canonical valid forms)
text diffs [24]; e-graphs show that equivalence classes can be                               raw attempted/legal actions
exploited computationally [26]. The missing leap is to make                      Raction =                                     ,              (6)
                                                                                                canonical legal actions
these ideas the training substrate for software agents.
                                                                                                 raw tokens to target accuracy
                                                                                   Rtrain =                                       ,           (7)
   The falsifiable prediction: after controlling for behavior and                            canonical tokens to target accuracy
task, canonical quotient learning should reduce entropy, search,                                 raw wall-clock to target accuracy
and proof cost before any new specialist model is trained. If                  Rtrain-time =                                           ,      (8)
                                                                                             canonical wall-clock to target accuracy
a broad frontier model does not become cheaper and more                                          raw wall-clock per verified change
reliable when the same software lineage is presented through                      Rspeed =                                               ,    (9)
                                                                                             canonical wall-clock per verified change
the canonical representative, the quotient thesis is wrong.                                      raw dense-active infrastructure cost/token
                                                                               Rcost/token =                                                    ,
                                                                                             canonical dense-active infrastructure cost/token
                                                                                                                                             (10)
                                                                                               raw
                                                                                             Treason+tool+plan+retry  /∆
                                                                                 Rreason = canon                         ,                   (11)
                                                                                             Treason+tool+plan+retry /∆
                                                                                             Lraw
                                                                                               failed proof/repair /∆
         IV. D EFINITIONS AND C LAIM D ENOMINATORS                                 Rretry = canon                     ,                      (12)
                                                                                             Lfailed proof/repair /∆
                                                                                             Araw edit /∆
                                                                                 Rinvalid = invalid             ,                            (13)
                                                                                             Acanon
                                                                                               invalid edit /∆
                                                                                                 raw cost per verified correct change
                                                                                    Rcost =                                                .
  The paper separates public facts, preliminary measurements,                                canonical cost per verified correct change
near-term targets, central hypotheses, and moonshot targets.                                                                                 (14)
                                                                              Here ∆ denotes an accepted change. Rcost is the all-in version
   Human-code entropy is the residual representation uncer-
                                                                              of the earlier Rchange notation, and Rcost/token is only the dense-
tainty left after behavior, contracts, and execution environment
                                                                              active serving denominator. At fixed accelerator throughput,
are fixed:
                                                                              Rtrain-time ≈ Rtrain . Effective raw-corpus-equivalent training
                                                                              throughput is Seff = Sphysical Rtrain , so a 1M-token/s training
                                                                              run with a 10× canonical tokens-to-target reduction is measured
                                                                              as 10M raw-corpus-equivalent tokens/s against the same target
         Hhuman = H(representation |
                                                                       (3)    capability.
                   behavior, contracts, environment).                            The 40×–150× range belongs to effective token-space
                                                                              reduction (Rentropy ); the 1,000×–100,000× range belongs to
                                                                              action-space pruning (Raction ); the 30×–150× central range
                                                                              belongs to training-token efficiency (Rtrain ); reasoning-token,
A canonical substrate is useful only if it reduces this conditional           retry-loop, invalid-edit, verified-change cost, and dense-active
entropy without erasing behavior evidence, safety constraints,                cost/token reductions belong to separate denominators (Rreason ,
provenance, compatibility ghosts, or deliberate diversity.                    Rretry , Rinvalid , Rcost , Rcost/token ). These do not multiply cleanly.
                                                                         TABLE V
                                                                     C ORE D EFINITIONS

 Term                                   Definition
 Canonical profile                      A governed language-role, layout, naming, dependency, generated-boundary, data-truth, and validation configuration
                                        for a software class. The primary app profile is a versioned limited-stack product profile: one maintained backend/core
                                        lane, one typed product-surface lane, one browser/product-shell lane, one durable-data lane, one schema/contract lane,
                                        and one build/deploy/proof envelope. Systems software uses approved secondary profiles or governed primitives.
 Canonical port                         A behavior-preserving or behavior-dispositioned transformation from a human artifact into a canonical profile.
 Canonical training object              A machine-readable bundle: provenance, license status, original source, port disposition, behavior evidence, canonical
                                        artifact, rejected invalid paths, and validation results.
 Human-code entropy                     Conditional representational uncertainty after behavior is fixed: the languages, frameworks, layouts, names, CI rituals,
                                        dependency choices, repository policies, and proof routes that vary without changing supported behavior.
 Agent sprawl                           The inference-time expansion of context reads, reasoning tokens, tool calls, architecture discovery, invalid edits,
                                        proof-loop failures, and review burden caused by unconstrained human repositories.
 Canonical behavior cell                A named, versioned, proof-carrying software primitive: stable interface, schema, policy model, generated code,
                                        fixtures, tests, migration obligations, security negatives, repair memories, and known failure modes.
 Semantic patch cell                    A typed, governed change archetype such as add field, migrate nullable to required, add permission edge, rotate
                                        secret, add idempotency key, split table, add audit trail, or upgrade dependency safely.
 Proof lane                             A standard local or CI validation route: exact command, environment, required artifacts, log schema, and acceptance
                                        rule.
 Proof-carrying change object           The structured unit of accepted change: intent, affected cells, typed diff, schema diff, migration diff, test delta,
                                        security delta, proof obligations, lane receipts, rollback plan, and provenance/license metadata.
 Reasoning digest                       A compact, versioned summary of known architecture, generated zones, proof routes, repair strategies, failure modes,
                                        rejected plans, compatibility ghosts, and prior proof objects for a repository, profile, or cell.
 Constrained edit grammar               The machine-checkable set of legal files, typed edits, schema operations, migration forms, dependency updates, proof
                                        lanes, and generated-zone protections available to an agent.
 Behavior intermediate representa-      A product-level IR for entities, state machines, policies, permissions, effects, contracts, migrations, observability,
 tion                                   proof obligations, and runtime constraints; source code is one generated projection.
 Software genome                        The mined atlas of recurring behavior families, variants, invariants, tests, proofs, provenance, repair memories, and
                                        generated projections across raw software history.
 Minimum viable novelty                 The irreducible product intent, domain fact, policy tradeoff, external constraint, or novel algorithm that remains after
                                        routine behavior, architecture, tests, proofs, dependencies, and deployment are generated or inherited.
 Canonical repository policy            A governed configuration for CI, branch protection, review, secrets, releases, ownership, generated zones, dependency
                                        updates, and deployment permissions.
 Behavior-equivalence class             The set of implementations that expose the same observable behavior, interfaces, security invariants, and migration
                                        guarantees.
 MFDL                                   Minimum Functional Description Length: the shortest canonical specification plus proofs plus renderer needed to
                                        produce a working system.
 Cost per verified correct change       Total dollars, source/context/reasoning/action tokens, tool calls, wall time, failed loops, validation runs, and human
                                        review needed to produce an accepted proof-carrying behavior-preserving change.
 Dense-active          infrastructure   Accelerator-side serving cost per generated or processed token under a specified active-parameter regime, context
 cost/token                             length, batch size, memory system, precision, and quality target; dense and MoE baselines must be reported separately.



Many overlap. The composite effect must be measured on                           to acceptance:
paired raw/canonical corpora and reported as cost per verified
correct change.                                                                                   I(Φ(x); ∆ | i, O) ≈ I(x; ∆ | i, O),                       (16)
                                                                                                 H(Φ(x) | ∆, i, O) ≪ H(x | ∆, i, O).                        (17)
        V. C ORRECT-C HANGE I NFORMATION T HEORY
                                                                                 This is the paper’s central learning-theoretic claim. The model
  The missing theoretical move is to stop treating code as                       should see less accidental entropy without losing the facts
the primary object. The primary object is a verified behavior                    needed to make the right change.
change. A repository is only one historical encoding of the
behavior, tests, policies, provenance, and operational memory                    A. Accidental Representation Tax
needed to accept that change.                                                        For a behavior target y, define the behavior-equivalence class
  Let x be a raw repository state, i an issue or requested
change, a1:k an edit/tool trajectory, and ∆ the accepted change                                         Ey,τ = {x : O(x, y) ≥ τ }.                          (18)
object. A change is correct only under an oracle that includes
behavior, tests, security, migration safety, provenance, and                     Raw software often contains many members of this class:
reviewer acceptance:                                                             different languages, frameworks, layouts, naming schemes,
                                                                                 migration styles, tests, CI dialects, dependency wrappers, and
     O(x, i, a1:k ) → {ACCEPT, REJECT, ESCALATE}.                        (15)    repository policies. Canonicalization selects a smaller governed
                                                                                 set Cy,τ plus audited exceptions. The accidental representation
The canonical map Φ is useful only when it preserves the                         tax is:
information relevant to ∆ while deleting information irrelevant                               ART(y, τ ) = log |Ey,τ | − log |Cy,τ |.        (19)
                                                                        TABLE VI
                                                         C LAIM S TATUS AND R EQUIRED E VIDENCE

 Claim                                  Status                       Current evidence                                 Required evidence
 Canonical trajectories are learnable    M EASURED                   QLoRA convergence on 64,088 translated           Replication across model sizes, held-
                                                                     trajectories and zero measured forbidden-        out repositories, stronger profile-validity
                                                                     language markers.                                checks, and task success.
 Canonical repositories reduce same-     N EAR - TERM TARGET         Substrate design: file grammar, proof lanes,     Paired raw/canonical tasks with identical
 model search cost                                                   generated zones, and reasoning digests.          model, issue lineage, hidden tests, and cost
                                                                                                                      ledger.
 Behavior preservation is adequate       C ENTRAL HYPOTHESIS         Dossier and preservation-tier design.            Large paired ports with tiered tests, traces,
 for training                                                                                                         contracts, fuzzing, differential replay, hu-
                                                                                                                      man review, and security/migration evi-
                                                                                                                      dence.
 Training-token reduction                C ENTRAL HYPOTHESIS         Compression theory plus adjacent data-           Paired scaling curves to target accepted-
                                                                     quality evidence.                                change performance.
 Behavior-genome economics               M OONSHOT                   No direct measurement yet; proposed sub-         Cell coverage census, mature foundry,
                                                                     strate architecture.                             runtime negative memory, and verified-
                                                                                                                      change cost curves after amortization.



                               TABLE VII                                         trajectories. A crude lower bound for search work is:
                  W HAT T HIS PAPER D OES N OT C LAIM
                                                                                                                k
                                                                                                                X                       m
                                                                                                                                        X
 Not claimed                Boundary                                                              Wsearch ∝               log |At | +         ρ j Fj ,         (20)
 Universal stack des-       The primary stack is a versioned product-app                                            t=1                 j=1
 tiny                       profile, not a permanent answer for all domains.
 Automatic                  Tests, traces, and contracts are evidence; only      where Fj are failed verification or review loops and ρj are
 equivalence                proof-backed cells get proof-backed claims.
 Literal 100× source        Large ranges refer to specific denominators such
                                                                                 their token/tool/human penalties. Canonicalization wins when
 shrink                     as action space or routine-domain tokens-to-         it reduces both the action entropy and the expected number of
                            target.                                              expensive failures.
 Free canonicalization      Foundry, provenance, review, and verification
                            costs must be amortized and included.                   This is why the strongest near-term experiment is same-
 Human code lacks           Human artifacts carry behavior, edge cases, in-      model raw/canonical ablation. It does not require a new model
 value                      cidents, and product judgment; only accidental       or a full training run. It asks whether the substrate itself reduces
                            representation is targeted.
                                                                                 search work: fewer files opened, fewer tool calls, fewer invalid
                                                                                 edits, fewer failed proof lanes, fewer review comments, and
                                                                                 lower dollars per accepted change.
The exact cardinalities are not directly observable for realistic
software, but the tax can be estimated by source-token counts,                   C. Minimum Functional Description Length
identifier entropy, AST-pattern entropy, file-path entropy, depen-
dency entropy, proof-lane entropy, repository-policy entropy,                       Minimum Functional Description Length is the product-
and model perplexity under paired raw/canonical corpora.                         software analogue of MDL: not the shortest text file, but the
                                                                                 shortest behavior description plus evidence plus renderer that
   This reframes the largest claim. The model is not merely
                                                                                 satisfies the declared oracle. The practical objective is:
learning fewer bytes. It is learning fewer behavior-equivalent
encodings. That is why clone studies, naturalness results,                                                                                 
                                                                                   MFDLS,τ (y) = min |z| + λ|Π(z)| + µ|RS | + ν|G(z)|
software product-line engineering, compiler IRs, e-graphs,                                               z∈ZS
proof-carrying code, and library-learning systems all matter:                                            s.t.   O(RS (z), y) ≥ τ.                              (21)
they show different historical paths toward the same idea that
repeated behavior should be represented by reusable structure                    Here z is the canonical behavior object, Π(z) its proof/evidence
rather than re-authored text [3], [18], [23], [26], [27], [29]–[31].             bundle, RS the renderer into source, tests, migrations, CI,
                                                                                 documentation, observability, and deployment artifacts, and
                                                                                 G(z) the governance/provenance burden. This extra governance
B. Correct-Change Search Work                                                    term matters: compression that drops attribution, opt-out state,
                                                                                 security evidence, or compatibility ghosts is not a substrate
   A coding agent pays for branching. At each step t, it faces                   win.
legal or perceived choices At : files to inspect, commands to                       Falsification: this information theory fails if canonical
run, edit locations, migration strategies, dependency changes,                   artifacts preserve no more mutual information about accepted
proof lanes, and repair paths. Raw repositories inflate |At |                    changes than raw repositories, or if they reduce entropy only by
with local folklore. Canonical repositories should shrink the                    deleting behavior needed for hidden tests, product acceptance,
legal set and reject invalid moves before they become failed                     security, migration safety, or provenance.
                                                                TABLE VIII
                                         F ROM C ODE I MITATION TO C ORRECT-C HANGE I NFORMATION

 Layer                      Raw-model burden                                               Canonical information object
 Text/source                Learn many strings for same behavior.                          One governed rendering plus audited exceptions.
 Repository                 Infer local architecture, generated zones, and proof com-      File grammar, generated-zone manifest, proof lanes,
                            mands.                                                         repository-policy object.
 Behavior                   Re-implement auth, lifecycle, billing, upload, search, jobs,   Versioned behavior cells with parameters, tests, proofs, and
                            webhooks, audit, observability.                                negative cases.
 Change                     Invent raw diffs and hope tests catch mistakes.                Typed semantic patch cell with preconditions, generated
                                                                                           deltas, proof obligations, rollback.
 Evidence                   Reviewer reconstructs intent from a diff and logs.             Proof-carrying change object with receipts, provenance,
                                                                                           security delta, migration replay, review rubric.
 Memory                     Incidents and failed patches disappear into history.           Runtime negative memory: forbidden plans, compatibility
                                                                                           ghosts, regression generators, patched cells.



         VI. T HE H UMAN -C ODE E NTROPY P ROBLEM                   familiar projects, while METR’s 2026 update emphasizes that
                                                                    adoption and task-selection effects make real productivity
   Human code is chaotic because human software production measurement difficult [7], [8].
is chaotic. Teams choose languages for hiring markets, de-            These findings do not prove every human program is broken.
ployment constraints, fashion, deadlines, legacy compatibility, They prove the stronger substrate point: human software
framework momentum, and personal preference. They choose lacks a single enforced shape. The code may run, but the
continuous-integration systems and workflow YAML by copy- representation is filled with optionality that does not encode
paste. They choose names under time pressure. They create product behavior. For an agent, optionality is not freedom; it is
folders that reflect organization charts and local arguments. branching factor. If there are 20 plausible files, five plausible
They copy data transfer objects instead of generating contracts. CI fixes, three dependency-update conventions, four migration
They hand-edit generated artifacts. They split logic across styles, and several local naming dialects, the agent must spend
services because the team split. They preserve test suites that tokens and tool calls discovering local folklore before changing
prove mocks, not behavior. They keep dependencies because behavior. This is agent sprawl: the model becomes a repository
updating them breaks a release.                                     cartographer, build engineer, migration reviewer, dependency
   This is not an argument that human software history lacks archaeologist, security analyst, and code reviewer before it can
value. The public and private code record contains product safely edit behavior. A canonical substrate removes that burden
judgment, edge cases, incident responses, migration scars, by deleting opinions from the supported path.
security repairs, tests, failure histories, and operational lessons   This variation is not free. Every equivalent way to express a
that a canonical substrate must preserve or disposition. The behavior becomes probability mass the model must learn. Every
target is narrower and more aggressive: remove optional framework convention becomes a routing burden. Every naming
representation that remains after behavior is fixed, while style becomes lexical entropy. Every CI dialect becomes an
carrying forward the evidence that explains why the behavior operational trap. Every ungoverned repository setting becomes
matters.                                                            hidden state. The frontier model pays for all of it.
   None of this is rare. GitGuardian found 28.65 million new          Agent sprawl is not solved by a larger context window
hardcoded secrets added to public GitHub commits in 2025, alone. A larger window lets the model carry more accidental
a 34% year-over-year increase [12]. Synopsys reported that state; it does not remove the accidental state. The canonical
84% of assessed codebases contained open-source vulner- countermeasure is to move repeated reasoning into substrate
abilities, 74% contained high-risk vulnerabilities, and 91% law: file grammar tells the model where behavior lives,
used components ten or more versions behind the current generated-zone manifests tell it where not to edit, proof lanes
version [32]. GitHub Actions studies find exactly the same tell it what proves completion, behavior cells identify the
problem in automation: workflow complexity, heterogeneity, recurring primitive, semantic patch cells define legal change
and compliance drift are now research subjects [9]; workflow operations, reasoning digests summarize known architecture
files change continuously across large repository samples [10]; and failure modes, and proof-carrying change objects make
security-practice adoption remains uneven even in a dominant review evidence explicit.
CI/CD platform [11]. Travis CI evidence is similar: 3.7 million
jobs across 1,276 projects showed noisy and heterogeneous VII. A SSUMPTION A: V ERSIONED P RODUCT P ROFILES AND
build outcomes, including misleading pass/fail signals [33],                         C ANONICAL P ROGRAMMING
and 9,312 Travis-using projects exhibited detectable CI feature       Assumption A: For each supported software class, there
misuse [34]. OpenSSF Scorecard exists because open-source should be one governed way to express, test, secure,
projects do not consistently use secure practices [35], [36]. deploy, and repair each concern. The primary agent-first
METR’s 2025 randomized trial found experienced open-source canonical profile targets web, product, SaaS, backend, and
developers were 19% slower with early-2025 AI tools on mature data applications—not all software. We denote the current
                                                                  TABLE IX
                                          H UMAN -C ODE VARIATION T HAT B LOATS THE T RAINING TARGET

 Variation class               Human-code reality                                              Canonical target
 Language sprawl               Same backend behavior appears across many service, script-      One primary language per role, with secondary profiles for
                               ing, and systems languages.                                     true infrastructure primitives.
 Framework drift               Express, FastAPI, Spring, Django, Rails, Laravel, Next,         One canonical service grammar and one canonical
                               Remix, custom RPC, custom queues.                               UI/product grammar per profile.
 Naming drift                  User/account/customer/member;                           man-    Controlled vocabulary tied to role, boundary, and domain.
                               ager/service/handler/repo/dao; vague helpers and utils.
 Layout drift                  Arbitrary folders, mixed generated and source files, stale      Enforced file grammar, generated boundaries, and ownership
                               migrations, implicit ownership.                                 maps.
 CI/build drift                GitHub Actions, GitLab CI, Travis, Circle, custom runners,      One proof-lane grammar with reproducible commands,
                               local env assumptions, undocumented gates, skipped or flaky     artifacts, permissions, and failure classes.
                               tests.
 Dependency drift              Unpinned libraries, abandoned packages, vulnerable transi-      Governed dependency closure, upgrade lanes, and scored
                               tive dependencies, risky workflows.                             exceptions.
 Data truth drift              Data-transfer-object forks, direct queries, app-owned durable   Governed durable-data truth, generated contracts, typed
                               truth, duplicated schema definitions.                           adapters, migration policy.
 Repository-policy drift       Branch protection, code owners, required checks, release        One repository-policy object with generated GitHub/GitLab
                               permissions, environments, secrets, and deployment creden-      settings and auditable exceptions.
                               tials vary per team.
 Agent ambiguity               Model guesses where to edit and what proves completion.         Agent-readable scope, canonical commands, valid repair
                                                                                               paths, and no-edit generated zones.



          2026
profile Papp   as a versioned limited-stack product profile:                  routine changes occur against explicit role ownership rather
one maintained backend/core lane, one typed product-surface                   than local framework folklore.
lane, one browser/product-shell lane, one durable-data lane,
                                                                                 Second, file grammar is enforced. Source paths, gener-
one schema/contract lane, and one build/deploy/proof en-
                                                                              ated paths, tests, migrations, contracts, adapters, and product
velope, plus repository policy and observability. Systems
                                                                              surfaces live in predictable places.
code, kernels, compilers, databases, browsers, GPU kernels,
embedded, native mobile, and high-performance computing use                     Third, naming is canonical. Variable and module names
secondary canonical profiles or governed primitives. The thesis               encode stable roles: actor, resource, command, event, policy,
is not implementation monoculture. The thesis is that human                   adapter, projection, migration, contract, and view.
preference should not decide the shape of routine product                       Fourth, generated boundaries are sacred. Contracts
software.                                                                     generate clients, schemas, test fixtures, and adapters. Generated
   The profile is replaceable. The invariant is governed role                 outputs are not hand-edited.
ownership, generated truth, proof lanes, constrained edits,
provenance, and observability:                                                  Fifth, continuous integration, build, and proof commands
  t+1           t
                                                                              are standard. Every change maps to known local commands,
 Papp = Govern(Papp , Esecurity , Eagent ,                                    CI jobs, permissions, logs, artifacts, and failure classes.
                                                                      (22)
                       Eperformance , Eecosystem , Emigration ).
                                                                     Sixth, repository policy, dependency policy, and data
Profile components change only when evidence shows lower truth are governed. One durable-data lane owns persistent
accepted-change cost, stronger verification reliability, better truth; dependencies are pinned, owned, scored, and upgraded
security, or better ecosystem support after transition cost.      through canonical lanes; branch protection, required checks,
   Canonical does not mean a single unchecked implementation. code owners, release gates, environment secrets, and deploy
It means one governed interface, multiple independently permissions are generated from one repository-policy object.
validated implementations where correlated failure would be
                                                                     The canonical standard is therefore a compression language
catastrophic. Critical cells require independent implementations
                                                                  for software. It compresses by removing representational
where feasible, adversarial review, conformance suites, canary
                                                                  degrees of freedom that do not change the product. If two
rollout, version pinning, rollback, deprecation protocols, prove-
                                                                  repositories implement the same account-management route
nance records, and profile-specific exceptions. Unlimited drift
                                                                  with eight framework stacks, four CI systems, three naming
is rejected; audited diversity is retained.
                                                                  conventions, and incompatible deploy policies, a broad model
   The canonical standard has six hard properties:
                                                                  pays for all of them. A canonical model pays for the behavior
   First, profile roles are fixed. The profile assigns one
                                                                  once, plus the governed exceptions that matter.
supported lane to backend/core/tooling, one lane to typed
product surfaces, one lane to the browser product shell, one         Falsification: Assumption A fails if paired raw/canonical
lane to durable data, one lane to deployment envelopes, and corpora do not reduce source tokens, identifier entropy, AST-
one lane to generated contracts. The concrete technologies are pattern entropy, path grammar, perplexity, or action branching
versioned profile choices, not the thesis. The invariant is that on target software classes.
                                                                  TABLE X
                                              C ANONICAL S TANDARD AS A C OMPRESSION L ANGUAGE

 Standard element             Human-code space removed                                         Training effect
 Limited language roles       Equivalent business behavior expressed across many backend,      Fewer grammars and lower cross-language transfer burden.
                              frontend, script, and migration languages.
 Canonical file grammar       Local folder myths, mixed generated/source files, arbitrary      Repository layout becomes predictable context instead of
                              helpers, unclear ownership.                                      hidden state.
 Controlled vocabulary        Synonym drift, vague service names, local abbreviations,         Lower lexical entropy and easier long-context retrieval.
                              duplicated domain labels.
 Generated boundaries         Data-transfer-object forks, hand-edited clients, duplicated      One source of truth replaces many invalid patch paths.
                              schema truth, stale fixtures.
 Strict build/test commands   README folklore, local scripts, skipped tests, inconsistent      Model learns standard completion actions instead of guessing
                              CI gates.                                                        rituals.
 Governed dependencies        Unpinned packages, stale transitive libraries, unsafe workflow   Dependency updates become canonical maintenance tasks.
                              permissions.
 Data truth policy            Direct writes, app-owned durable truth, duplicate validation     Database and migration repairs become standard forms.
                              logic, unsafe migrations.
 Repository policy            Hand-configured GitHub/GitLab settings, inconsistent branch      Review, merge, release, and secret-handling become gener-
                              protection, unscoped workflow permissions, unclear owners.       ated infrastructure.



 VIII. A SSUMPTION B: G OVERNED F OUNDRY AND P ORT                              IX. A SSUMPTION C: B EHAVIOR P RESERVATION U NDER
                   D ISPOSITIONS                                                              D ECLARED C ONTRACTS

                                                                                 Assumption C: Canonical ports can preserve, disposition,
   Assumption B: Every available artifact in the training
                                                                              or explicitly reject behavior at a confidence level high
set can be assigned a governed port disposition, and the
                                                                              enough for training. This is the hardest assumption in agent-
cost of porting amortizes across repeated training runs,
                                                                              first canonical code. A canonical rewrite that silently deletes
serving savings, and downstream reuse.
                                                                              edge cases is not compression; it is corruption. Fully automatic
   Full coverage means every artifact enters the foundry. The                 behavior equivalence for arbitrary programs is not available in
claim is not that every repository becomes one product-app                    general; Rice’s theorem is the theoretical warning label on any
implementation. The claim is that every artifact is either                    claim that a tool can decide nontrivial semantic properties for all
transformed into a canonical training object or explicitly                    programs [43]. The foundry therefore treats behavior evidence
excluded with a reason that remains useful for governance,                    as part of the training object, not a best-effort annotation.
evaluation, or negative training. The maturity ladder is staged:                 Every canonical training object carries a preservation and
first disposition coverage, then behavior-fixture extraction, then            divergence dossier: original tests, canonical tests, differential
full canonical porting only where value, license status, and                  traces, API compatibility checks, UI replay where applicable,
preservation evidence justify the cost.                                       migration replay, security-negative cases, performance budgets
   Every canonical training object is an auditable data prod-                 for behavior that depends on latency or resource use, prove-
uct, not a loose rewrite. Its minimum schema includes                         nance/license records, accepted incompatibilities, compatibility
source identity, license, profile, disposition, transformation                ghosts, and rejected port paths. A canonical port is never
trace, behavior evidence, security evidence, canonical arti-                  behavior-preserving merely because tests pass; it is behavior-
fact, known loss, and training-use policy. Source identity                    preserving only within a declared evidence envelope.
includes repository URL, commit, content hash or Software                        The output is not binary pass/fail. It is graded behavior
Heritage identifier when available, opt-out/removal state, and                confidence for original artifact o and canonical artifact z:
original artifact digest. License and supply-chain evidence
should use existing machine-readable standards where possible:                    B(o, z) =
                                                                                               X
                                                                                                     wi ei (o, z),      0 ≤ ei ≤ 1,
                                                                                                                                          X
                                                                                                                                                wi = 1.
SPDX for license/provenance and software-bill-of-material                                      i∈E                                          i
information, CycloneDX for broader bill-of-materials and cyber-                                                                           (23)
risk metadata, SLSA/in-toto-style attestations for build and                  Here E includes test agreement, differential execution coverage,
transformation steps, OpenTelemetry semantic conventions for                  migration and data-invariant replay, security-negative coverage,
runtime evidence, and policy-as-code systems such as Open                     UI/API replay coverage, human acceptance for high-value
Policy Agent for inclusion and release rules [37]–[42].                       cases, performance/SLO agreement where applicable, and
   Falsification: Assumption B fails if a representative corpus               provenance/license completeness.
cannot be assigned governed dispositions, if license/provenance                  Compatibility ghosts are first-class. If downstream users
metadata cannot be preserved through transformation and                       depend on behavior that looks accidental—ordering, timing,
removal propagation, if behavior fixtures cannot be extracted                 error text, weak validation, legacy API quirks, migration side
for high-value classes, or if porting cost does not amortize                  effects, or undocumented defaults—the foundry must either
across at least 3× the initial foundry investment.                            preserve it, encode it as a compatibility fixture, or record an
                                                                                TABLE XI
                                                                       G OVERNED P ORT D ISPOSITIONS

 Disposition                       Meaning                                                                      Training use
 transform-permitted               License, provenance, security, and behavior evidence permit a canoni-        Canonical source, behavior object, transformation trace, accepted
                                   cal artifact or full port.                                                   patch examples.
 secondary-profile                 Artifact belongs to systems, mobile, embedded, scientific, or other          Profile-specific training and cross-profile interface examples.
                                   non-product-app profile.
 governed-primitive                Foundational component is retained behind stable wrappers, tests,            Dependency, wrapper, compatibility, upgrade, and conformance ex-
                                   versions, and ownership.                                                     amples.
 spec-only                         Source cannot be transformed, but public behavior/specification can          Abstract contracts, interface facts, and conformance targets.
                                   be represented independently.
 fixture-only                      Tests, traces, issues, API examples, or migration fixtures are usable        Behavior fixtures and weak-oracle warnings.
                                   without source projection.
 negative-only                     Artifact teaches a failure mode, vulnerability, bad migration, or rejected   Negative examples, refusal cases, and repair memories.
                                   pattern.
 metadata-only                     Only aggregate metadata, disposition statistics, or provenance facts         Governance metrics and exclusion statistics.
                                   can be retained.
 quarantine                        Artifact appears unsafe, malicious, poisoned, undispositioned, or            No positive training; security analysis and exclusion receipt only.
                                   provenance-risky.
 license-excluded                  License, attribution, opt-out, or derivative-work risk blocks inclusion.     No positive training artifact; removal propagation and audit receipt.


                Available code-            Classify role, behavior,              Disposition, profile,                Minimize valid                        Canonical
               training universe              language, license                  provenance policy                     token space                       training corpus


Fig. 1. Governed full-corpus foundry. The corpus is not filtered down to clean examples; every artifact receives provenance-aware disposition, and only
qualified artifacts become positive canonical training objects.

                                                                                 TABLE XII
                                                                      B EHAVIOR P RESERVATION D OSSIER

 Evidence lane                          What it catches                                                           Canonical training use
 Original tests                         Known intended behavior and regression expectations.                      Positive evidence and weak-oracle metadata.
 Differential traces                    Runtime behavior across original and ported artifacts.                    Equivalence scoring and edge-case discovery.
 Migration replay                       Data-shape, rollback, lock-budget, and invariant failures.                SQL/migration proof examples.
 Security negatives                     Auth bypass, injection, secret leakage, unsafe defaults.                  Labeled bad paths for refusal and repair training.
 UI/API replay                          Browser, CLI, and API compatibility surfaces.                             Product behavior fixtures.
 Human acceptance                       High-value cases where automated tests are insufficient.                  Gold labels and accepted-incompatibility manifests.
 Provenance/license                     Legal and origin constraints.                                             Inclusion, exclusion, and attribution metadata.



accepted incompatibility signed by the relevant owner. Calling                                behavior worth keeping is first identified, tested, replayed, and
it accidental is not enough to delete it.                                                     carried forward.
   The output is a preservation tier, not a blanket declaration                                 Falsification: Assumption C fails if behavior confidence re-
of equivalence:                                                                               mains low, human review rejects core ports, security/migration
   The weak-oracle problem is explicit. Tests are evidence, not                               regressions rise, or important edge behavior is routinely lost
proof. SWE-bench-style patch evaluation can be distorted by                                   during canonicalization.
insufficient tests and plausible-but-wrong patches; UTBoost
found insufficient test cases and erroneous patches previously                                      X. A SSUMPTION D: C ANONICAL B EHAVIOR C ELLS
labeled as passed in SWE-bench-family evaluation [6]. Property-                                  Assumption D: The highest-reuse software behaviors can
based testing, differential testing, compiler fuzzing, mutation                               be collapsed into certified, reusable behavior cells, and these
testing, and symbolic execution are stronger evidence lanes,                                  cells can eventually absorb 70%–90% of routine product
but they remain scoped evidence rather than universal equiva-                                 code if a behavior-cell census validates coverage.
lence [44]–[47]. CompCert shows that semantic preservation                                       This is the breakthrough beyond canonical stack align-
can be a compiler contract rather than a slogan [48]. seL4                                    ment. If the model is still writing 80 functions for cre-
shows that proof-backed systems components are possible for                                   ate/read/update/delete resource behavior, authentication, forms,
security-critical kernels, while also making clear how much                                   validation, errors, pagination, tests, clients, fixtures, and migra-
engineering work such proofs require [49]. The canonical                                      tions, we are only standardizing the mess. If the model emits
foundry should use these methods where their cost is justified                                a cell declaration and parameters, we are removing entire
and reject overclaiming elsewhere.                                                            classes of source tokens, legal edits, proof obligations, and
   This section is intentionally early because behavior preserva-                             review questions from the task.
tion is the trust anchor. The authorial claim that all human code                                A canonical behavior cell is not a library. It is a reusable
is improvable does not mean all human code is disposable. It                                  behavior unit with a stable interface, schema, policy model,
means every human artifact can be made more canonical if the                                  generated projections across the full stack (service, typed client,
                                                            TABLE XIII
                                                   C ANONICAL P RESERVATION T IERS

 Tier            Name                             Meaning                                           Training use
 P0              Rejected / metadata-only         Unsafe, unlicensed, malicious, undispositioned,   Exclusion, quarantine metadata, negative exam-
                                                  or behavior evidence is too weak.                 ples only.
 P1              Syntactic                        Builds, formats, typechecks, or parses, but no    Low-weight syntax/profile examples only.
                                                  behavior claim is made.
 P2              Interface/test                   Public interfaces are represented and origi-      Weak positive training with explicit weak-oracle
                                                  nal/canonical tests or fixtures pass.             label.
 P3              Trace/contract                   API, schema, migration, policy, compatibility     Standard product-app training target.
                                                  ghosts, and negative cases match declared
                                                  contracts and replay traces.
 P4              Property/fuzz/differential       Generated, fuzzed, property-based, symbolic,      Higher-confidence port and edge-case curricu-
                                                  mutation-tested, or production-derived inputs     lum.
                                                  exercise critical paths.
 P5              Proof-backed                     A formal or mechanized proof discharges           Certified cell, compiler/profile primitive, or
                                                  specified invariants or semantic preservation     critical dependency.
                                                  obligations.



product UI, durable-data migration, tests, fixtures, observability, cover less than 50% of routine product-app behavior, or if cell
and docs), known failure modes, security negatives, repair composition introduces more complexity than it removes.
memories, compatibility ghosts, and proof obligations. Change
                                                                                XI. P RELIMINARY L EARNABILITY AND
itself also becomes cell-shaped: common edits such as add
                                                                                   P ROFILE -A DHERENCE E VIDENCE
field, migrate nullable to required, add permission edge, rotate
secret, add idempotency key, upgrade dependency safely, split          Claim scoped to this section: canonical data is learnable
table, and add audit trail become semantic patch cells rather and can enforce target-profile adherence. There is prior
than bespoke diff inventions.                                       evidence that code model performance benefits heavily from
   For routine domains, behavior cells are the main path from data quality: Arctic-SnowCoder-1.3B used 555B tokens in
canonical code to MFDL. The agent should not decide from staged data refinement and beat or matched models trained on
scratch how authorization, audit trails, pagination, idempotency, much larger token budgets [50]. The phi-1 work showed that
upload signing, or migration rollback work in every repository. high-quality “textbook” data can produce remarkably capable
It should select a certified cell, supply parameters, apply a small models [51].
semantic patch cell when behavior changes, and return a proof-         To test whether canonical-translated data produces healthy
carrying change object with receipts.                               convergence, we ran a quantized low-rank adaptation (QLoRA)
   The 70%–90% number is a target, not a measured result in fine-tuning experiment on Qwen2.5-Coder-14B-Instruct [17],
this paper. It must be earned by a behavior-cell census that [52] using 64,088 canonically translated agentic coding tra-
measures coverage by accepted changes, source tokens, AST jectories (57,688 train, 6,400 validation). The dataset consists
nodes, runtime traces, issue tickets, security-sensitive paths, of verified multi-turn coding sessions where an agent reads a
review burden, and production incident classes. A cell is useful real GitHub issue, explores the codebase, applies a fix, and
only if it reduces verified-change cost without hiding required passes automated tests, then translates the trajectory through the
variation.                                                          canonical porting pipeline to align with the target limited-stack
   The compression ladder shows how gains compound across profile.
the standardization levels:                                            Training ran for 7,106 steps on a single NVIDIA RTX 3090
   The endgame is rung 7: models manipulate canonical               (24 GB) over approximately three days. Key hyperparameters:
software behavior graphs, and source code becomes a generated       LoRA    rank r=16, α=32, learning rate 2×10−5 with constant-
artifact. The training target moves from source text toward with-warmup schedule, effective batch size 1×8 gradient
graph operations, semantic patches, proof obligations, and accumulation, maximum sequence length 2,048 tokens, 4-bit
receipts. This is analogous to how LLVM created a reusable IR NF4 quantization with double quantization.
for program analysis and transformation [29], and how MLIR             Figure 2 shows the convergence curve generated from
explicitly aims to reduce software fragmentation [23]. Soft-        raw  training telemetry. After restart de-duplication, the run
ware product-line engineering has a related history: explicitly     contains   7,106 training steps and 711 validation evaluations.
modeling commonality and variability across product variants        Raw   training  loss drops from 2.707 at step 1 to 0.419 at step
to build reusable core assets [30]. Equality-saturation systems     7,106.  Validation  loss drops from 2.261 at step 10 to 0.646 at
such as egg show how rewrite spaces can be represented and          step 7,106,  closely  tracking the raw training curve throughout.
searched compactly when the intermediate representation is          Two  observations    are significant:
explicit [26].                                                         1) No visible train/validation divergence. Raw training
   Cells have a lifecycle, not just a registry entry:                      and validation losses fall together through the run, with
   Falsification: Assumption D fails if the top 500–2,000 cells            validation ending at 0.646 after consuming 100% of the
                                                                       TABLE XIV
                                         B EHAVIOR C ELLS : F ROM H UMAN -C ODE M ESS TO C ANONICAL P RIMITIVES

Human-code mess                                                    Canonical cell                           Why it compresses
Rails users controller, Express users route, FastAPI users         resource<User>                           One verified cell replaces thousands of reimplementa-
service, Spring user repository                                                                             tions.
Custom login/session/token/password-reset/multi-factor             auth.session / auth.oidc                 Repeated in every app with dangerous variation.
code
Hand-written role- or attribute-based permission checks            policy.check                             Security-critical code becomes a proven primitive.
scattered across layers
Custom list endpoints with ad hoc pagina-                          list.page                                Massive API/UI/DB repetition becomes one cell.
tion/sorting/filtering
Ad      hoc      form    validation    duplicated    across        schema.form.validation                   Four validation layers generated from one schema.
frontend/API/database/tests
Recurring billing glue, Stripe webhook wrappers, proration         billing.subscription                     Common SaaS surface with dangerous edge cases.
logic
Background retries, idempotency, dead-letter queues                job.retry.idempotent                     Same reliability logic reimplemented everywhere.
Object-storage upload variants, signed URLs, virus scanning        blob.upload.signed_url                   Security and storage complexity repeated constantly.
Custom webhook verification, replay, deduplication                 webhook.verify.dispatch                  Integration-heavy apps repeat this badly.
Audit trails, event history, compliance logging                    audit.append_only                        Required for compliance-heavy systems.
Expand/contract migrations, backfills, rollback plans              migration.expand                         High failure cost and high repetition.
Custom notification channels, delivery tracking, templates         notification.send                        Repeated boilerplate across channels.


                                                                      TABLE XV
                                 T HE C OMPRESSION L ADDER : F ROM R AW R EPOSITORY TO C ANONICAL B EHAVIOR G RAPH

Rung        Level                             What changes                                       Measurement
0           Raw human repo                    Original code                                      Baseline
1           Canonical layout                  Fixed paths, ownership, generated zones            File-search entropy, edit target count
2           Canonical naming                  Actor/resource/command/event/policy vocab-         Identifier entropy
                                              ulary
3           Single primary profile            Backend/core, typed surface, product shell,        Language/framework entropy
                                              durable data, contracts, build/deploy/proof
4           Contract-first generation         Schema generates clients, fixtures, validators,    Duplicate data-transfer-object/client drift
                                              docs
5           Proof lanes                       Fixed build/test/migrate/security commands         Failed-loop count
6           Behavior cells                    Authentication, resource lifecycle, billing,       Source-token and AST-pattern reduction
                                              search, uploads, jobs as primitives
7           Behavior graph                    Model emits behavior graph operations plus         Task-token and reasoning-token reduction
                                              proof obligations; source code is compiled



                               TABLE XVI                                                                              TABLE XVII
                        B EHAVIOR C ELL L IFECYCLE                                                               P ILOT C ONFIGURATION

Stage                        Required evidence                                        Field                           Value
Propose                      Behavior family, interface, parameters, variants,        Base model                      Qwen2.5-Coder-14B-Instruct
                             provenance, and expected coverage.                       Adaptation                      QLoRA, rank 16, alpha 32, 4-bit NF4,
Certify                      Preservation tier, conformance suite, security                                           double quantization
                             negatives, fuzz/property lanes, rollout risk.            Data                            64,088 translated trajectories; 57,688 train /
Deploy                       Version pinning, generated projections, proof                                            6,400 validation
                             receipts, canary plan, rollback path.                    Steps                           7,106 training steps; 711 validation evalua-
Monitor                      Runtime traces, incidents, performance budgets,                                          tions
                             compatibility ghosts, exploit reports.                   Sequence length                 2,048 tokens
Deprecate                    Migration path, old-version risk, user impact, and       Hardware                        Single NVIDIA RTX 3090, 24 GB
                             negative-memory update.                                  Forbidden marker metric         Average presence of off-profile markers
Incident response            Revocation, patched cell release, downstream                                             such as Python def, Go func, and Java
                             blast-radius scan, and postmortem fixtures.                                              public class under target-profile ser-
                                                                                                                      vice prompts



       training data. By contrast, raw open-source coding data                                ing, evaluation checkpoints measured off-profile markers
       typically requires aggressive deduplication: The Stack v2                              (Python def, Go func, Java public class, etc.) in
       reduced from 67.5 TB to 32.1 TB (52% deduplication)                                    model outputs prompted with target-profile service tasks.
       and then to 2.4 TB after quality filtering—a 96.4%                                     All 711 evaluation checkpoints recorded zero markers,
       reduction.                                                                             indicating that canonical fine-tuning successfully steered
    2) Zero forbidden-language violations. Throughout train-                                  the model toward the target profile.
                                               QLoRA Convergence on Canonical Coding Trajectories                                                               1
                                                                                                                      train loss, raw
                     2.5                                                                                              validation loss
                                                                                                                      forbidden-language markers
cross-entropy loss



                     2.0




                                                                                                                                                                markers
                     1.5

                     1.0

                     0.5                                                                                                                                        0
                           0                1000               2000                 3000             4000            5000            6000               7000
                                                                                        training step
    Fig. 2. Raw training and validation loss convergence for QLoRA fine-tuning of Qwen2.5-Coder-14B on 64,088 canonically translated trajectories. The figure
    shows the real per-step training log after restart de-duplication: 7,106 training steps and 711 validation evaluations. Training loss starts at 2.707 and ends at a
    raw final value of 0.419. Validation loss drops from 2.261 at step 10 to 0.646 at step 7,106, with a minimum of 0.644 at step 6,780. Zero forbidden-language
    markers were recorded across all evaluation checkpoints. The vector figure is generated from raw per-step training logs and evaluation telemetry only.



                                                TABLE XVIII                                      future edits through schemas, proof lanes, and semantic patch
                               W HAT THE P ILOT P ROVES AND D OES N OT P ROVE                    cells.
                                                                                                    Let X be raw human-code representations and Z be canon-
         Status                               Claim
                                                                                                 ical behavior representations. Let Y be observable software
         Shows                                Canonical translated trajectories are learnable    behavior. The canonical standard is useful only if the canonical
                                              under this parameter-efficient adaptation setup.
         Shows                                The measured forbidden-language markers can        map preserves behavior while reducing irrelevant representation
                                              be suppressed in the evaluation prompts.           entropy:
         Does not show                        Behavior preservation, full stack correctness,                        H(Z | Y ) ≪ H(X | Y ).                   (24)
                                              held-out accepted-change success, or lower
                                              cost per verified change.
                                                                  This is the formal version of “one governed way per supported
         Does not show                        Tokens-to-target reduction versus raw trajecto-
                                                                  software class.” For a supported concern, if two implementa-
                                              ries; that requires paired scaling curves from
                                                                  tions expose the same behavior and invariants, they should not
                                              the same task lineage.
                                                                  remain two equally privileged training targets. One interface
                                                                  becomes canonical; independent implementations, port traces,
      These results provide early evidence that canonical data negative paths, compatibility fixtures, or excluded artifacts
   is learnable under this parameter-efficient adaptation setup. remain only when they carry evidence, diversity, governance,
   They do not yet prove behavior preservation, cost-per-correct- or security value.
   change reduction, or 100B replacing 1T. Those require the full A. Compression Accounting Protocol
   evaluation protocol described in Section XVII.                    All ranges in this paper are priors or targets until promoted
                                                                                                 by measurement. A range becomes measured only when the
                     XII. A SSUMPTION E: C OMPRESSION T HEORY AND                                numerator, denominator, task distribution, model, evidence tier,
                      M INIMUM F UNCTIONAL D ESCRIPTION L ENGTH                                  and confidence interval are reported. For task distribution τ
      Assumption E: Removing accidental human degrees                                            and target quality q:
   of freedom reduces effective representation entropy, le-                                                                  Traw source (τ )
                                                                                                            Rsource (τ ) =                        ,          (25)
   gal action-space, and training-token demand. Agent-first                                                                Tcanonical source (τ )
   canonical code is not a source minifier. It is a canonical                                                                Draw (q, τ )
   coding theory for software behavior. The raw corpus contains                                           Rtrain (q, τ ) =                    ,              (26)
                                                                                                                           Dcanonical (q, τ )
   many strings for the same behavior because humans choose                                                                  Treason+tool,raw (τ )
   different languages, frameworks, folders, continuous-integration                                         Rreason (τ ) =                             ,     (27)
                                                                                                                           Treason+tool,canonical (τ )
   workflows, repository settings, dependency wrappers, migration
   rituals, and naming schemes. The canonical standard maps that                                                             Cverified change,raw (τ )
                                                                                                           Rchange (τ ) =                                  . (28)
   equivalence class to a smaller canonical space, then constrains                                                         Cverified change,canonical (τ )
Composite ratios cannot be multiplied unless a fitted causal            XIII. B EHAVIOR IR AND T YPED C HANGE A LGEBRA
model validates separability on held-out paired tasks. This is
especially important for language collapse, framework collapse,
generated truth, behavior cells, and proof lanes, which often           A canonical substrate should not merely prescribe file layouts.
remove the same tokens, edits, or reasoning loops.                   It needs an application-level behavior intermediate represen-
   The strongest effect is not literal token shrinkage. The          tation. The behavior IR represents entities, state machines,
strongest effect is action-space and reasoning-space collapse.       authorization edges, external contracts, effects, idempotency
A raw repository asks an agent to infer where code lives, what       requirements, migration semantics, observability, privacy zones,
is generated, which tests matter, whether a migration is safe,       rollout constraints, performance envelopes, and proof obli-
how the CI system encodes permissions, what dependency               gations. The IR lowers into governed service code, typed
path is acceptable, and what local naming convention should          product surfaces, durable-data operations, OpenAPI/Protocol
be preserved. A canonical repository turns those choices into        Buffers schemas, tests, dashboards, deployment manifests, and
explicit law. That law may add some metadata tokens, but it          documentation. OpenAPI and Protocol Buffers already show
removes entire families of invalid edits, failed repair loops, and   the value of contract-first generated projections [21], [22]; the
rediscovery reasoning.                                               canonical substrate generalizes this from API messages to
   The final block in Figure 3 deliberately separates the raw        product behavior.
independence bound from the claimable combined range. The               Routine edits should then be expressed as a typed change
conservative envelope is not the product of every row. It is         algebra rather than raw diffs:
anchored by constrained legal edits plus a small number of
independent reductions in representation, retry, and reasoning
work; stronger bands require evidence that those reductions          ∆ = (op, params, pre, post, proof s, rollback, provenance).
remain separable on paired tasks.                                                                                                 (30)
   Contract-first generation is the first large step toward that     The operation determines the required proof lanes. For example,
limit: OpenAPI and Protocol Buffers are existing examples            AddField(User.timezone, default=UTC) expands
of schema-owned surfaces that generate clients, validators,          into schema diff, migration, API projection, form state,
and transport bindings instead of hand-maintaining parallel          validation, fixtures, compatibility tests, rollout, and rollback.
representations [21], [22]. Semantic patch systems such as Coc-      AddPermissionEdge(Manager, ApproveInvoice)
cinelle and constrained generation systems such as XGrammar          expands into policy graph update, negative tests, audit event,
show complementary directions: patches and outputs can be            UI affordance, threat-model delta, and authorization proof.
represented as structured grammars rather than unconstrained         AddIdempotencyKey(WebhookDispatch)                      expands
text [24], [53].                                                     into persistence, duplicate-replay tests, observability, retry
                                                                     semantics, and incident-runbook update.
   The theoretical limit is Minimum Functional Description
Length: a frontier over canonical specifications, evidence              This is where the paper becomes more defensible and more
bundles, and renderers, not a magical globally shortest program.     ambitious. A raw diff asks the reviewer to reconstruct the
For substrate S, preservation threshold τ , behavior target y,       operation. A typed change object states the operation first and
proof/evidence bundle Π, renderer RS , and observable-behavior       makes generated diffs subordinate evidence. Proof-carrying
oracle O:                                                            code established the idea that producers can ship code with
                                                                     checkable evidence of safety [31]; CompCert and seL4 show
                                                                     that semantic preservation and machine-checked proofs can be
   MFDLS,τ (y) = min (|z| + λ|Π(z)| + µ|RS |)                        practical in constrained high-value domains [48], [49]; SLSA
                    z∈ZS
                                                                     and in-toto show that provenance and supply-chain integrity can
                                  s.t.   O(RS (z), y) ≥ τ. (29)      be standardized as artifacts [41], [42]. Proof-carrying change
                                                                     applies the same philosophy to everyday product software: the
This is not code golf and not syntax preference. It is the end       unit of work is not a patch, but a patch plus typed intent,
state where bespoke code appears only when the behavior              generated obligations, proof receipts, rollback, and provenance.
is novel. Routine product behavior becomes behavior graph               The research bet is that most product changes are not
operations, cell composition, generated surfaces, policies,          semantically arbitrary. They are drawn from a finite and
schemas, migrations, semantic patches, and proof receipts. In        learnable algebra: add field, add resource, add role, add
that limit, the model is no longer trained to imitate the long       permission, add workflow state, add integration, add notifica-
tail of human implementation choices. It is trained to operate       tion, add idempotency, split entity, migrate invariant, upgrade
a constrained software machine.                                      dependency, add audit, expose report, tighten validation, change
   Falsification: Assumption E fails if paired raw/canonical         rollout, repair flaky proof lane. If true, agentic software
corpora do not reduce measured source tokens, identifier             engineering should focus less on unconstrained patch generation
entropy, AST-pattern entropy, path grammar, proof-loop count,        and more on recognizing, composing, proving, and amortizing
perplexity, or action branching on target software classes.          these typed operations.
                                                                              TABLE XIX
                                                                 C ANONICAL R EDUCTION D ENOMINATORS

 Axis                                        Moonshot range                        Meaning
 Literal source-token                                                              Physical source shrinkage from generation, cells, and fewer duplicate surfaces.
                                             2×–8× conservative
 Effective representation-space              40×–150× central                      Fewer valid encodings for the same supported behavior.
 Agent action-space                                                                Fewer legal files, edits, workflows, proof lanes, migration paths, dependency choices,
                                             1,000×–100,000×             high-     and generated-zone mistakes.
                                             end
 Reasoning-token space                       3×–50× hypothesis                     Fewer planning, tool, architecture-discovery, retry, and repair tokens per accepted
                                                                                   change.
 Retry/review loop                           3×–50× hypothesis                     Fewer failed tests, invalid edits, ambiguous reviews, rollback surprises, and proof
                                                                                   reruns.
 Training-token budget                       30×–150× hypothesis                   Fewer examples needed to reach target canonical accuracy, conditional on paired
                                                                                   scaling curves.
 Cost per verified correct change            3×–100× hypothesis                    End-to-end cost after foundry, verification, serving, reasoning, failed-loop, and
                                                                                   maintenance amortization.


         Cumulative substrate stack, sorted by local gain                                                             local band: conservative / central / aggressive
           Raw human software universe                                                                                1.0x / 1.0x / 1.0x
                                                                                                                      baseline
                                                                                                                      2x / 5x / 15x
           + Corpus hygiene: dedup, provenance, generated/vendor/secret/malware filtering                             source/corpus reduction
                                                                                                                      3x / 10x / 50x
           + Reasoning digests and proof caches: known plans, failure modes, prior proof objects                      reasoning-token reduction
                                                                                                                      3x / 15x / 50x
           + Proof lanes and reusable receipts: verification, rollback, migration replay, policy checks               retry/review-loop reduction
                                                                                                                      4x / 20x / 60x
           + Canonical profiles: language roles, layout, naming, repository policy, dependency law, proof lanes       effective representation
                                                                                                                      8x / 40x / 120x
           + Contract-first generated truth: schemas, clients, docs, fixtures, validators, migrations                 effective representation
                                                                                                                      15x / 75x / 250x
           + Behavior cells: auth, lifecycle, search, forms, billing, uploads, jobs, webhooks, audit, observability   routine-product representation
                                                                                                                      100x / 10,000x / 100,000x
           + Constrained edit grammar and semantic patch cells                                                        legal-action reduction

           Minimum Functional Description: irreducible product intent, external contracts, domain invariants, novelty, and evidence.


          All-layer combined envelope (effective correct-change search work, not source size or dollar cost).
          Gross local-band product if fully independent: 8.64 × 105 x / 4.5 × 1011 x / 6.75 × 1015 x (orientation only; not claimed).
          Overlap-adjusted claimable envelope: 102 –103 x conservative / 104 –106 x central / 107 –109 x aggressive. The conservative band is capped
          because source hygiene, canonical representation, cells, legal edits, proofs, and reasoning caches share causal mechanisms.


Fig. 3. Canonical Compression Cascade: From Human-Code Entropy to Minimum Functional Description. The stack starts at the 1.0× raw baseline and
then adds layers sorted by conservative local gain, with ties ordered by central gain. The right column gives the local hypothesis band for each layer. The
final block combines all row multipliers two ways: a gross independent-axis product for orientation, and a deliberately smaller overlap-adjusted envelope for
effective correct-change search work. The local ranges are measured on different denominators and are not naively multiplied. Training time, inference cost,
and verified-change cost remain separate outcome denominators.



XIV. A SSUMPTION I: R EASONING -T OKEN C OMPRESSION                                          can improve outcomes, but also make inference cost a first-class
           AND AGENT-S PRAWL C OLLAPSE                                                       denominator [56]–[59].
   Assumption I: Canonical software compresses the reason-                                     The correct-change cost model is:
ing process required to produce a verified correct change.                                                Cchange = Tcontext + Treason + Taction + Tverify
Agent sprawl is a substrate failure: when a repository does not                                                                                                         (31)
                                                                                                                      + Trepair + Hreview + Afoundry .
state its own laws, teams compensate with planner agents,
search agents, reviewer agents, test-fixing agents, security                                 Here Tcontext is repository reading, Treason is planning and
agents, and release agents that repeatedly rediscover the                                    architecture inference, Taction is patch generation and tool use,
same facts. Modern coding agents do not spend only source                                    Tverify is proof-lane execution and log interpretation, Trepair
tokens. They spend planning tokens, tool tokens, hidden or                                   is failed-loop recovery, Hreview is human review burden, and
explicit reasoning tokens, file-inspection tokens, failed test                               Afoundry is amortized canonical-foundry cost.
loops, repair attempts, and human review attention. Reasoning-                                  Canonical repositories reduce these terms by compiling
model documentation and best-practice guidance already treat                                 repeated reasoning into durable artifacts. Behavior cells encode
reasoning effort as a controllable inference resource [54],                                  architecture. Generated-zone manifests tell the agent where
[55]. Chain-of-thought, self-consistency, ReAct, and test-time                               not to edit. Semantic patch cells encode common repairs.
planning work show that intermediate reasoning and tool use                                  Proof lanes encode the validation sequence. Repository policy
                                                              TABLE XX
                               T YPED C HANGES S HOULD C OMPILE TO P ROOF O BLIGATIONS , N OT M ERELY F ILES

 Change operation              Canonical parameters                   Compiled obligations
 AddField                      entity, name, type, nullability, de-   Schema diff, migration replay, generated clients, UI states, fixtures, compatibility,
                               fault/backfill                         rollback.
 AddPermissionEdge             actor, resource, action, conditions    Policy graph proof, negative tests, audit log, UI affordance, threat-model delta.
 SplitTable                    source, target, key, backfill, dual-   Data migration, read/write compatibility, rollback, observability, latency budget.
                               write window
 AddWebhook                    provider, event, signature, retry,     Contract fixture, signature verifier, replay test, dead-letter path, alerting.
                               idempotency
 UpgradeDependency             package, version, risk class, migra-   SBOM/provenance check, changelog constraints, compatibility tests, security scan,
                               tion notes                             rollback.
 RotateSecret                  provider, scope, rollout window        Secret inventory, dual-read window, audit receipt, rollback, leak scan.



encodes review, secret, dependency, and deployment law.                      or cost per accepted proof-carrying change.
Reasoning digests summarize known plans, failure modes,
                                                                                    XV. A SSUMPTION F: T RAINING AND I NFERENCE
rejected plans, compatibility ghosts, and prior proof objects.
                                                                                                   E CONOMICS
A proof-carrying change object then binds the intent, affected
cells, typed diff, schema diff, migration diff, test delta, security           Assumption F: Canonical code reduces required training
delta, proof obligations, receipts, rollback plan, and provenance            data, active inference compute, failed repairs, and review
metadata.                                                                    burden enough to lower cost per verified correct change.
   The moonshot is therefore not that agents “think less” in                   Training compute for dense transformers is commonly
the abstract. It is that agents stop spending tokens on reposi-              approximated as
tory cartography, local policy discovery, command guessing,                                         Ctrain ≈ 6N D,                  (32)
generated-zone detection, migration-law inference, and repair-               where N is parameter count and D is training tokens [28], [61].
loop archaeology when the substrate can state those facts                    The canonical program may attack both terms, but that remains
once and verify them mechanically. Structured outputs and                    a scaling-curve hypothesis. It should be stated as paired tokens-
constrained decoding are useful precedents: they move part of                to-target-accuracy, not as a naked training-speed claim. At fixed
correctness from prompt convention into machine-checkable                    hardware tokens/s, tokens-to-target reduction is also training-
shape [53], [60]. Proof-carrying code established the broader                time reduction; equivalently, physical tokens/s become raw-
principle that executable artifacts can carry evidence checked               corpus-equivalent tokens/s multiplied by Rtrain . A defensible
by a consumer rather than accepted on trust [31].                            central target is 30×–150× lower tokens-to-target capability
   The measurement unit is deliberately concrete: files opened,              under successful paired scaling curves, with additional savings
context tokens, planning tokens, hidden reasoning budget where               from lower active inference, fewer reasoning/tool tokens, fewer
observable, tool calls, invalid edits, generated-zone violations,            failed repair loops, and lower review burden.
failed proof loops, validation reruns, reviewer comments,                       For inference, the dense-active speed claim is deliberately
and retries per accepted change. Closed models may hide                      narrower than the verified-change claim. If a 100B–120B dense
some reasoning tokens, so field trials should report direct                  canonical specialist reaches the same accepted-change quality
reasoning-token counters where available and proxy them with                 as a 1T-class dense-active baseline on supported canonical work,
planning text, tool loops, wall-clock, and failed proof-lane                 then first-order active-parameter accounting implies roughly
traces where not. The conservative target is 3×–10× fewer                    8.3×–10× more same-hardware aggregate token/sec and
context/reasoning/tool/retry tokens per verified change. The                 roughly 88%–90% lower dense-active infrastructure cost/token
central target is 10×–100×. The aggressive 100×–10,000×                      before memory, batching, context, and utilization corrections.
band is only for routine supported work after behavior cells,                That claim does not apply unchanged to sparse mixture-of-
semantic patch cells, proof lanes, and negative memory mature.               experts systems: a 1T-total MoE with 32B active parameters
It is not a universal inference-speed claim.                                 may already be cheap per token, so the canonical MoE claim
   Reasoning compression is not separate from economics; it                  must be measured through router entropy, expert specialization,
is one term in the verified-change cost equation in Assumption               and end-to-end cost per verified change rather than nominal
F. A reasoning digest only matters if it reduces measured files              total parameter count.
opened, context tokens, reasoning tokens, tool calls, invalid                   The all-in economics of canonical software intelligence are:
edits, repair attempts, reviewer comments, or wall-clock at the
                                                                                     Ccorrect = Afoundry + Ctrain + Cinfer + Ctools
same accepted-change standard.                                                                                                                         (33)
                                                                                                   + Cverify + Creview + Cfailed + Cmaint .
   Falsification: Assumption I fails if, on paired raw/canonical
tasks with the same broad model, canonical repositories do                   The foundry is a capital expenditure on the training substrate.
not reduce files opened, tool calls, reasoning tokens, invalid               Its cost must be amortized across repeated model runs, served
edits, failed verification loops, wall time, reviewer comments,              tokens, downstream agent tasks, security repairs, and reusable
certified cells. Active inference compute includes context           verifier/repair expert. The model spends less capacity deciding
tokens, reasoning tokens, action/tool tokens, verification-log       what kind of software world it is inside.
interpretation, and repair attempts. The strongest business             The canonical mixture-of-experts hypothesis is therefore
metric is therefore cost per verified correct change, not raw        not merely “use sparse models.” It is that canonicalization
token price. The central specialist scenario is a matched-quality    gives sparse models better expert boundaries. A role expert
conditional, not a proven empirical result: if the 100B–120B         can specialize in migration invariants rather than every dialect
model fails to match broad-model accepted-change quality on          of migrations; a security expert can specialize in policy edges
supported canonical tasks, then the dense-active speed and           and negative cases rather than every framework’s middleware
cost/token scenario does not activate.                               idiom; a verifier expert can specialize in proof receipts and
   The simplest break-even condition is:                             failed lanes rather than repository-specific CI folklore.
                                                                        The metrics are explicit. Router entropy should fall for a
                              Cfoundry
              k∗ =                               .           (34)    fixed task distribution:
                     Craw/change − Ccanon/change                                                  X
                                                                                 Hrouter (x) = −     p(e | x) log p(e | x).      (35)
Here k ∗ is the number of accepted changes required to                                             e
repay the foundry cost under a fixed task distribution. If the
                                                                     Success also requires expert load balance, low dropped-token
canonical path does not reduce same-quality change cost, or if
                                                                     or overflow rate, specialization purity by software role, low
verification/governance cost erases the savings, the economic
                                                                     cross-expert repair churn, and equal or better task success at
claim fails even when source and action-space metrics improve.
                                                                     fixed active parameters. A canonical role mixture-of-experts
   Falsification: Assumption F fails if empirical scaling curves     should be compared against dense models and broad mixture-
show no reduction in tokens to target canonical accuracy,            of-experts baselines by accepted-patch rate and cost per verified
if active inference and reasoning tokens do not fall on              correct change, not by nominal total parameter count.
paired change tasks, if the 8.3×–10× dense-active token/sec             Falsification: Assumption G fails if router entropy, ex-
scenario disappears after memory, batching, context, utilization,    pert utilization, or task success do not improve versus
verification, or quality corrections, if a canonical specialist      language/framework-oriented mixture-of-experts routing.
needs more than 50% of broad dense-active parameters to
match broad-model accuracy on held-out canonical tasks, or if        XVII. A SSUMPTION H: E VALUATION AND FALSIFICATION
foundry cost does not amortize within 3× the initial investment.        Assumption H: The canonical substrate reduces invalid
                                                                     actions and end-to-end change cost, not merely produces
         XVI. A SSUMPTION G: C ANONICAL ROLE                         cleaner-looking code. The evaluation target is not HumanEval-
                 M IXTURE - OF -E XPERTS                             style function synthesis. The target is whether a model operating
   Assumption G: Canonical code gives mixture-of-experts             inside the canonical universe can implement, modify, test,
models cleaner expert domains, reducing router entropy               migrate, secure, and deploy ported software at lower cost than
and improving expert utilization.                                    a broad model operating inside the human-chaotic universe.
   Kimi K2 shows why dense and mixture-of-experts baselines          SWE-bench Verified is a useful precedent [5], [19], but static
must be separated: it reports 1T total parameters but only           issue benchmarks are vulnerable to weak tests, contamination,
about 32B active parameters per token [14], [15]. A dense            and benchmark aging [6], [20], [62]. This paper’s claim needs
100B canonical model is not automatically faster than a 32B-         paired raw/canonical tasks from the same software lineage.
active mixture-of-experts model on raw per-token compute.               The benchmark object is the tuple:
                                                                          (raw_repo,        canonical_repo,        issue,
The canonical opportunity for mixture-of-experts is different.            behavior_contract,
   The human-code mixture-of-experts model must route                     preservation_tier, proof_lanes, hidden_tests,
across many languages, frameworks, and repository idioms. A               reviewer_rubric, cost_ledger)
canonical-code mixture-of-experts model routes across fewer,            The proof program has three gates. Gate 1 is the same-
cleaner domains: product surface, service/core, durable data         model substrate test: run the same broad frontier model on raw
and migration, contracts/generated artifacts, security policy,       and canonical versions of the same issue lineage. This is the
dependency governance, verification, repair, and planning.           first falsification point because it isolates substrate value before
Experts specialize around canonical software roles rather than       specialist training. Gate 2 trains or adapts a canonical specialist
arbitrary language/framework combinations.                           and compares it on canonical tasks against the same broad
   This matters because routing uncertainty is another form of       baseline and the raw/canonical same-model result. Gate 3
human-code entropy. In a raw repository, a billing change might      measures paired scaling curves and verified-change economics:
require a controller, browser form, secret, CI permission, SQL       tokens-to-target, model size, serving cost, foundry amortization,
migration, queue worker, and webhook verifier, each following        and all-in cost per accepted proof-carrying change.
local conventions. In the canonical substrate, those concerns           The key ablation is direct: if the same broad frontier
have named roles, owned files, generated boundaries, and proof       model performs much better on canonical repos than
lanes. The router can learn the role graph directly: billing cell,   on the original raw repos, before canonical specialist
policy cell, SQL migration expert, UI resource-state expert,         training, then substrate compression is real. That proof
                                                                     TABLE XXI
                                                   C OST C OMPONENTS H IDDEN BY R AW T OKEN P RICING

 Component                           Raw repository burden                                           Canonical compression route
 Training compute                    Long-tail languages, frameworks, layouts, generated drift,      Paired scaling curves on canonical training objects and
                                     and weak labels.                                                behavior graphs.
 Active inference compute            Long context reads, architecture rediscovery, exploratory       Reasoning digests, file grammar, generated-zone manifests,
                                     tool use.                                                       proof-carrying change objects.
 Tool calls                          Search, test discovery, command guessing, dependency            Proof lanes, repository policy, dependency closure, standard
                                     archaeology.                                                    receipts.
 Verification cost                   Ad hoc commands, flaky gates, unclear migration safety.         Deterministic proof lanes, migration replay, rollback re-
                                                                                                     ceipts, policy checks.
 Review burden                       Reviewers reconstruct intent and proof from a raw diff.         Intent, typed diff, security delta, test delta, receipts, and
                                                                                                     rollback plan in one object.
 Failed repairs                      Invalid edits, generated-file modifications, unsafe migra-      Constrained edit grammar, semantic patch cells, negative-
                                     tions, repeated test failures.                                  path curriculum.


                                                                     TABLE XXII
                                                          C ANONICAL M ODEL T RAINING L ADDER

 Stage                         Model/data configuration                                           Purpose
 1B–3B scout                   Canonical syntax, file grammar, naming, schema, and build          Verify that the standard is learnable under small-model
                               command data.                                                      budgets.
 7B–14B repairer               Messy-to-canonical traces, generated-boundary repairs, migra-      Measure how much porting logic fits in small specialists.
                               tions, dependency updates.
 32B–70B system model          Full canonical repositories with long-context tasks, UI/product    Establish capability curve before 100B-class runs.
                               changes, DB changes, and security fixes.
 100B–120B central model       Full canonical corpus, behavior fixtures, profile routing, and     Central target for matching broad dense-active coding models
                               long-horizon planning data.                                        on canonical work.
 Mixture-of-experts canon-     Experts for product surface, service/core, durable data and        Reduce active compute and improve router precision.
 ical frontier                 migration, contracts/generated artifacts, security/policy, in-
                               fra/release, verifier/repair, and porting.



                             TABLE XXIII                                          privacy, and consent obligations for code data [1], [64].
              C ANONICAL ROLE M IXTURE - OF -E XPERTS L AYOUT                     Software Heritage’s 2025 activity report is a reminder that
                                                                                  the public software archive is enormous and must be treated
 Expert family            Canonical role
                                                                                  as infrastructure, not scrapeable exhaust [65]. Compression-
 Product surface          UI state, accessibility, visual behavior, and typed
                          user-facing flows.
                                                                                  factor overlap is handled by paired-corpus measurement;
 Service/core             Domain logic, APIs, adapters, and service invari-       the paper never multiplies language collapse, framework
                          ants.                                                   collapse, cell collapse, action-space collapse, reasoning-token
 Durable                  Durable truth, schema changes, migration safety,
 data/migration           and rollback.
                                                                                  collapse, and repair-path collapse naively. Representational
 Contracts/generated      Schemas, generated clients, fixtures, adapters, and     compression is not automatically model compression; that
                          docs.                                                   requires scaling curves.
 Security/policy          Authentication, authorization, input boundaries,
                          secrets, dependency risk.
                                                                                     Falsification: Assumption H fails if cost per verified correct
 Infra/release            Deployment envelopes, release policy, observabil-       change is not at least 3× lower after including foundry, verifi-
                          ity, and operational permissions.                       cation, serving, reasoning, failed-loop, review, and maintenance
 Verifier/repair          Validation lanes, failed traces, blocked changes.
 Porter                   Messy-to-canonical translation and disposition as-
                                                                                  cost amortization.
                          signment.
                                                                                        XVIII. C OST L EDGER AND F IELD T RIAL D ESIGN
                                                                                     The paper should be judged by one primary endpoint:
does not require waiting for a 100B-class specialist. The                         amortized cost per verified correct change. A result that
paired task must measure accepted patch rate and the full                         reduces source tokens but increases proof failures is a loss. A
trajectory: files opened, context tokens, reasoning tokens, tool                  result that improves benchmark pass rate but increases reviewer
calls, invalid edits, generated-zone violations, failed tests, failed             burden is incomplete. A result that lowers token cost while
migrations, wall time, reviewer comments, cost ledger entries,                    increasing incident remediation is not a win. The ledger must
and rollback/proof receipts.                                                      include source, context, reasoning, and action tokens; serving
   Major risks are first-class evaluation targets and are expanded                infrastructure; verification; security and provenance work; tool
in Section XIX. Licensing and provenance must travel                              runtime; wall time; human review; failed attempts; rollback
with every source artifact; The Stack v2 and the BigCode                          work; downstream defect cost where measurable; and foundry
Governance Card both emphasize governance, provenance,                            amortization.
                                                                      TABLE XXIV
                                                            C ANONICAL P ORT E VALUATION A RMS

 Arm             Model                                    Repository form                         Purpose
 A               Broad frontier model                     Original human repo                     Current-world baseline: capability and cost in the messy
                                                                                                  corpus.
 B               Broad frontier model                     Canonical repo                          Measures substrate benefit without a new model.
 C               Canonical specialist                     Canonical repo                          Measures model plus substrate effect.
 D               Canonical specialist + cells             Cellized canonical repo                 Measures behavior-cell compression benefit.
 E               Porter model                             Human repo to canonical object          Measures foundry automation throughput.


                                                                       TABLE XXV
                                     K ILLER A BLATION : R AW R EPO V ERSUS C ANONICAL R EPO WITH THE S AME M ODEL

 Metric                             Raw repository expectation                                     Canonical repository target
 Files opened                       Broad search across local architecture.                        Fewer predictable file reads from canonical path grammar.
 Tool calls                         Discover build, tests, migrations, policy, dependencies.       Invoke known proof lanes and typed patch tools.
 Reasoning tokens                   Rediscover architecture, ownership, generated zones, repair    Use reasoning digest, cell contracts, and proof obligations.
                                    strategy.
 Invalid edits                      Generated-file edits, wrong layer, unsafe migration, policy    Rejected by constrained edit grammar before proof lanes.
                                    bypass.
 Failed verification                Flaky or misselected commands and repeated repair loops.       Standard receipts and classified failures.
 Accepted patch rate                Baseline for current-world agents.                             Higher acceptance at equal or lower total cost.


                                                                     TABLE XXVI
                                                        C ONTAMINATION -AWARE B ENCHMARK T IERS

 Tier                               Use                                                            Risk controlled
 Public paired                      Reproducible raw/canonical ablations and open leaderboard      Transparent but contamination-prone; not sufficient for
                                    tasks.                                                         frontier claims.
 Private held-out                   Partner repositories, undisclosed issues, hidden tests, and    Reduces training contamination and patch memorization.
                                    blinded review.
 Live / post-cutoff                 New issues evaluated before public disclosure and paired       Tests current repository reasoning under fresh task distribu-
                                    canonicalization.                                              tions.
 Generated stress tasks             SWE-smith-style generated task families and preservation       Scales coverage and tests false-green, generated-zone, and
                                    traps [63].                                                    compatibility-ghost failures.



                              raw
                                                                                  corpus with honest rejected dispositions is more valuable than
                             C∆   + Araw
                                     foundry /N                                   a clean-looking corpus that silently drops behavior.
                   Rchange = canon               ,                        (36)
                            C∆     + Acanon
                                      foundry /N
                                                                                 XIX. R ISKS AND T HREAT M ODEL
where Afoundry is foundry construction and porting cost
amortized across N future changes. The aggressive case is            The canonical substrate is not risk-free. It deliberately
impossible if the foundry never amortizes; the conservative       concentrates    software structure, so its failure modes must be
case can be true even while the foundry is still expensive if     named    as design   constraints rather than left as caveats.
repeated verified changes become much cheaper.                       The  central  controlled-diversity  rule is: canonicalize behavior
   The first field trial should avoid the common benchmark        interfaces,  proof  receipts, and  edit  grammars; diversify critical
trap of measuring only task success. It should choose 20–         implementations      and evaluators   where   common-mode failure
50 production-like repositories with known issue lineage and      would   be  catastrophic.  N-version     programming    is a warning
hidden reviewer rubrics, port each into the canonical substrate,  as  much   as a  precedent:  diversity  is useful only  when  failures
and run arms A–D from Table XXIV. The decisive result is          are  sufficiently  independent   [66].  Unlimited   local dialects are
not that the canonical specialist wins. The decisive result is    not  useful diversity. Independently    validated  lowerings, fuzzers,
that the same broad model in arm B becomes cheaper and policy engines, monitors, and rollback paths are.
more reliable than arm A. That isolates substrate value from
model value. Then arm C tests specialist training, and arm D                 XX. C OMPRESSION F RONTIER S UMMARY
tests behavior-cell amortization.                                    The full 30-domain compression catalog is supplemental
   The paper should publish every failure. Failed ports reveal source in compression_catalog.tex. The main paper
weak behavior oracles. Compatibility ghosts reveal hidden keeps only the proof spine: every domain is a prior or target
contracts. Non-preserved behavior reveals product decisions. until paired measurement promotes it. The catalog is useful
Negative examples become training material. The foundry for search-space accounting, but it is not the evidence base by
should not hide these cases; it should classify them. A canonical itself.
                                                                   TABLE XXVII
                                                      C ANONICAL S TANDARD A BLATION L ADDER

 Ablation                          What changes                                                 What it proves
 Naming only                       Controlled vocabulary and role names; no layout or           Separates lexical entropy from structural entropy.
                                   dependency changes.
 Path grammar only                 Canonical folders, ownership, test locations, gener-         Measures repository-navigation and edit-location reduction.
                                   ated/source paths.
 Generated boundaries only         Contracts generate clients/adapters/fixtures; hand edits     Measures duplicate-truth and invalid generated-edit reduc-
                                   forbidden.                                                   tion.
 Repository policy only            Branch protection, code owners, required checks, workflow    Measures hidden-state and CI/action-space reduction.
                                   permissions, secrets, release gates.
 Dependency governance only        Pinned, owned, scored dependencies and upgrade lanes.        Measures supply-chain and repair-loop reduction.
 Proof lanes only                  Standard build/test/migration/security commands and ac-      Measures     failed-loop    reduction      without full
                                   ceptance artifacts.                                          language/profile collapse.
 Behavior cells only               Top 50 cells with generated expansion.                       Measures source-token and action-space reduction from
                                                                                                cells alone.
 Full standard                     Language roles, file grammar, naming, generated bound-       Measures total canonical substrate effect.
                                   aries, repository policy, dependencies, data truth, cells,
                                   validation.


                                                                TABLE XXVIII
                                   C ORE A SSUMPTIONS , S TRENGTH A SSESSMENTS , AND FALSIFICATION C RITERIA

 ID      Assumption                                 Strength             Falsified if
 A       One governed way can cover each sup-       Strong               Primary profile covers less than 60% of economically valuable prod-
         ported product-software concern.                                uct/web/backend/data tasks.
 B       Full-corpus foundry can assign governed    Hard                 Large fractions remain undispositioned or foundry cost exceeds downstream
         dispositions and amortize cost.                                 savings.
 C       Behavior can be preserved or disposi-      Hardest              Human review rejects core ports or security/migration regressions rise.
         tioned with graded confidence.
 D       Behavior cells absorb high-reuse routine   Very plausible       Top 500–2,000 cells cover less than 50% of product-app behavior.
         product code.
 E       Canonicalization reduces representation    Central claim        Paired corpora show no entropy, path, AST, perplexity, or action-branching
         entropy and legal action-space.                                 reduction.
 F       Canonical data reduces required model      Hypothesis           Scaling curves show no lower token or parameter need for target canonical
         size and training tokens.                                       accuracy.
 G       Canonical mixture-of-experts routes bet-   Plausible            Router entropy, utilization, and task success do not improve.
         ter by software role than by language
         accident.
 H       Canonical substrate lowers cost per ver-   Business claim       End-to-end change cost is not at least 3× lower after amortization.
         ified correct change.
 I       Canonical substrate compresses reason-     Moonshot claim       Same-model canonical tasks do not reduce files opened, tool calls, reasoning
         ing, tool, planning, and retry tokens.                          tokens, invalid edits, failed tests, wall time, or reviewer burden.



   The frontier should be read as an accounting program. Literal              goals, legal obligations, risk tolerance, taste, and genuinely new
source-token reduction is expected to be modest compared                      domain behavior. But all routine coding decisions—language,
with legal-action and reasoning-space reduction. Training-token               framework, folder, generated boundary, migration idiom, de-
reduction is the hardest claim and remains conditional on paired              pendency wrapper, proof lane, review evidence, rollback form,
scaling curves. Cost per verified correct change is the final                 and repair strategy—move out of human discretion and into
denominator because it includes foundry, verification, serving,               governed substrate law.
reasoning, failed-loop, review, and maintenance cost.
                                                                                 The defensible path starts with facts already visible in the
     XXI. F UTURE V ISION : M INIMUM V IABLE N OVELTY                         field. Public software archives are massive and structured;
                                                                              Software Heritage reported over 27 billion unique source files
   The long-term prize is not a smaller corpus of cleaner                     from 421 million projects in its 2025 activity report [65]. Raw
code. It is a post-source-code substrate in which routine                     code is repetitive and predictable [18]; large clone studies and
software is compiled from compact intent, behavior cells,                     notebook studies show heavy duplication [3], [4]. Product-line
invariants, policies, proofs, provenance, runtime evidence, and               engineering has long treated software families as managed
reusable reasoning. Source code remains useful, inspectable,                  commonality plus variability [30]. LLVM, MLIR, e-graphs,
and deployable, but it becomes one generated projection of a                  OpenAPI, Protocol Buffers, and Coccinelle are all partial
deeper object.                                                                precedents for moving from raw text toward intermediate
   This is the extreme form of MFDL: the system should contain                representations, generated projections, equivalence classes,
only minimum viable novelty. Humans still decide product                      contracts, and semantic transformations [21]–[24], [26], [29].
                                                              TABLE XXIX
                                              M INIMUM L EDGER FOR A D EFENSIBLE F IELD T RIAL

 Ledger item                   Raw repository measurement                                     Canonical repository measurement
 Discovery                     Files opened, grep/search calls, dependency reads, archi-      Cell lookups, profile docs read, reasoning digest reads.
                               tecture notes.
 Context/pre-fill              Input tokens, cache hit rate, long-context latency.            Reduced context tokens, generated-zone manifests, cached
                                                                                              profile/cell context.
 Planning/reasoning            Planning tokens, hidden reasoning budget where measur-         Typed change recognition, bounded proof-plan tokens, no-
                               able, self-repair tokens, tool-selection deliberation.         reason lanes.
 Generation/action             Output tokens, patch size, tool calls, action tokens.          Typed operation, generated diff, proof object, rollback
                                                                                              object.
 Serving                       Dense-active or MoE cost/token, token/sec, memory, batch-      Matched-quality canonical specialist serving ledger plus
                               ing, utilization.                                              verification overhead.
 Verification                  Test commands, failed lanes, log interpretation, flaky         Standard proof-lane receipts, classified failures, determin-
                               reruns.                                                        istic replay.
 Security/provenance           SBOM, license/provenance review, secret scan, policy           Carried metadata, transformation receipts, governed policy
                               checks.                                                        gates.
 Review                        Reviewer comments, review minutes, rework cycles.              Intent audit, proof receipt audit, residual novelty audit.
 Reliability                   Escaped defects, incident tickets, rollback time.              Runtime invariant violations, negative-memory updates,
                                                                                              rejected cells.
 Amortization                  None or local scripts only.                                    Foundry cost spread over future changes, repos, profiles,
                                                                                              and cells.


                                                               TABLE XXX
                                                   C ANONICAL S UBSTRATE T HREAT M ODEL

 Risk                          Failure mode                                                   Required mitigation
 Behavior loss                 Port drops hidden edge behavior, migration side effects,       Declared contracts, preservation tiers, differential replay,
                               timing assumptions, or compatibility ghosts.                   accepted-incompatibility manifests, and human escalation.
 Weak oracles                  Tests pass while behavior diverges.                            Treat tests as evidence only; add fuzzing, property tests,
                                                                                              mutation tests, generated tests, hidden review, and trace
                                                                                              replay.
 Licensing/provenance          Canonical artifact loses attribution, opt-out state, source    SPDX/CycloneDX metadata, source hashes, transformation
                               lineage, or derivative-risk status.                            traces, removal propagation, and policy gates.
 Canonical monoculture         One flawed auth, migration, billing, or policy cell creates    One governed interface with independent implementations
                               correlated failure at scale.                                   for critical cells, conformance suites, canaries, rollback,
                                                                                              and cell advisories.
 Useful-diversity loss         Profile excludes a domain-specific implementation choice       Secondary profiles, governed primitives, explicit exception
                               that carries performance, safety, accessibility, regulatory,   process, and profile lifecycle evidence.
                               or ecosystem value.
 Benchmark contamination       Public paired tasks leak into training or static tests age     Public, private held-out, and live/post-cutoff benchmark
                               out.                                                           tiers.
 Foundry cost                  Porting, proof, review, and governance costs exceed down-      Break-even accounting, staged dispositions, high-reuse
                               stream savings.                                                prioritization, and amortization receipts.
 Governance capture            Canonical rules favor one vendor, stack, or implementation     Versioned public specs, independent conformance suites,
                               without evidence.                                              audit logs, and appeal paths.
 Generated-code opacity        Source becomes generated but reviewers cannot understand       Proof-carrying change objects, generated-zone manifests,
                               obligations or failures.                                       readable diffs, and reviewer rubrics.
 Scaling-curve uncertainty     Representation compression does not translate to training-     Paired raw/canonical scaling curves and fixed-target
                               token or model-size reduction.                                 accepted-change benchmarks.



Proof-carrying code, CompCert, seL4, and SLSA show that                     learning supports the general idea that learned abstractions
evidence and provenance can become first-class artifacts rather             can shorten future program search [27]; the canonical foundry
than after-the-fact paperwork [31], [41], [48], [49].                       applies that logic to production software behavior.
   Software genome. The foundry should mine raw repositories,                  Behavior IR. The substrate needs an application-level
issues, tests, traces, incidents, dependency histories, and repair          intermediate representation above source code. A behavior
patches into a global atlas of behavior families: authentication,           IR represents entities, state machines, policies, permissions,
tenant boundaries, resource lifecycle, billing, uploads, jobs,              effects, external contracts, migration semantics, observabil-
webhooks, audit, observability, migrations, notifications, per-             ity, runtime SLOs, and proof obligations. It lowers into
missions, retries, cache invalidation, and product workflows.               governed service code, typed product surfaces, durable-data
The output is not a snippet library. It is a behavior gene bank:            operations, UI, docs, tests, dashboards, deployment manifests,
canonical intent, variants, anti-examples, contracts, tests, proof          and formal/specification artifacts. This is the product-software
templates, repair memories, provenance, legal transformations,              analogue of compiler IR: agents edit semantic deltas, not
and generated implementations. DreamCoder-style library                     arbitrary file trees.
                                                                            TABLE XXXI
                                                           M AIN -PAPER C OMPRESSION F RONTIER S UMMARY

 Layer                              Current status                         Main mechanism                                          Required measurement
 Corpus hygiene                     Partly measured in prior cor-          Deduplication,                         gener-           Raw/canonical token counts, removal re-
                                    pora                                   ated/vendor/secret/malware          filtering,          ceipts, license disposition rates.
                                                                           provenance assignment.
 Canonical profile                  Near-term target                       Fixed roles, path grammar, generated zones,             Same-model raw/canonical files opened, in-
                                                                           proof lanes, dependency law, repository                 valid edits, proof-lane failures, accepted
                                                                           policy.                                                 patch rate.
 Contract-first generation          Central hypothesis                     Schemas generate clients, fixtures, valida-             Duplicate-truth removal, generated-edit vio-
                                                                           tors, docs, migrations, and adapters.                   lations, schema drift rate, migration failures.
 Behavior cells                     Central hypothesis                     Auth, resource lifecycle, search, billing,              Behavior-cell census by accepted changes,
                                                                           uploads, jobs, webhooks, audit, observability           AST nodes, traces, issues, review burden,
                                                                           as certified cells.                                     and security paths.
 Semantic patch cells               Central hypothesis                     Typed edits such as add field, split table,             Legal action count, invalid edit count, proof
                                                                           rotate secret, add idempotency key, and add             receipt completeness, repair-loop reduction.
                                                                           permission edge.
 Runtime and negative mem-          Moonshot                               Incidents, reverted patches, production                 Incident recurrence, compatibility-ghost cap-
 ory                                                                       traces, and rejected plans become invariants            ture, negative-test reuse, post-deployment
                                                                           and forbidden paths.                                    regression rate.


                                                                           TABLE XXXII
                                                   T HREE B UILD -O UT S TAGES FOR THE C ANONICAL S UBSTRATE

 Stage                     Substrate built                                      Main compression denominator                         Target range
 1. Canonical repo         Primary/secondary profiles, file grammar, gen-       Training tokens, active context, tool discovery,
                           erated zones, proof lanes, repository policy.        invalid edits.                                       3×–10×        training;      2×–8×    infer-
                                                                                                                                     ence/reasoning/tool; 2×–5× verified-change
                                                                                                                                     cost.
 2. Correct-change sub-    Behavior cells, semantic patch cells, proof-         Action space, repair loops, review burden, re-       30×–150×           training;     10×–100×
 strate                    carrying change objects, reasoning digests, neg-     peated reasoning.                                    inference/reasoning/tool; 10×–50× verified-
                           ative corpus.                                                                                             change cost.
 3. Behavior genome        Behavior IR, software genome, runtime-derived        Routine-domain         training,       ac-
                           invariants, agent-native OS, verification markets,   tion/reasoning/search space, institutional           150×–1,000×     routine-domain      training;
                           evolutionary foundry.                                memory, non-novel implementation.                    100×–10,000×     inference/action/reasoning;
                                                                                                                                     50×–1,000× verified-change cost.




                                TABLE XXXIII                                               bounded-reason lanes.
                     T YPED C HANGE A LGEBRA E XAMPLES
                                                                                              Proof-carrying changes. Future agents should not submit
 Operation                               Parameters
                                                                                           raw diffs. They should submit typed change objects containing
 AddField                                User, timezone,
                                                                                           intent, affected behavior cells, semantic patch, generated source
                                         nullable=false, backfill=UTC                      diff, schema diff, migration diff, tests, security delta, proof
 AddPermissionEdge                       actor=Manager,                                    obligations, receipts, rollback plan, and provenance/license
                                         action=ApproveInvoice
 SplitTable                              source=Events,                                    metadata. Human review shifts from reconstructing intent from
                                         target=AuditEvents                                text to auditing changed obligations, assumptions, and residual
 AddIdempotencyKey                       endpoint=WebhookDispatch
 RotateSecret                            provider=Stripe                                   novelty.
                                                                                              Evolutionary foundry. Once behavior cells have evaluators,
                                                                                           cells can improve continuously. Agents propose variants;
   Typed change algebra. Routine changes should become                                     tests, proofs, fuzzers, benchmarks, security scanners, and
typed operations with known proof obligations: Each operation                              runtime monitors select survivors. AlphaDev and FunSearch are
expands into schema diff, migration plan, generated client                                 narrow but important evidence that evaluator-guided program
updates, UI state changes, security review, observability deltas,                          search can discover useful algorithms beyond ordinary human
tests, rollback, and receipts.                                                             implementation [67], [68]. The canonical version extends the
   Reasoning compiler. The most important future gain is                                   loop to product behavior: better retries, indexes, migrations,
cognitive amortization. Successful and failed trajectories should                          policy encodings, UI state machines, rollback paths, and proof
compile into reusable plans: issue type to affected cells,                                 envelopes.
repository profile to legal actions, failure signature to repair                              Runtime and negative memory. The substrate should learn
strategy, migration class to proof obligations, dependency                                 from production traces, incidents, rejected patches, reverted
update to compatibility checks. Current reasoning and acting                               commits, review objections, failed migrations, security bugs,
methods show why intermediate reasoning helps [56]–[58]; the                               flaky tests, and rollbacks. Runtime behavior reveals implicit
canonical future is to spend that reasoning once, store it as                              compatibility contracts; negative examples become forbidden
substrate law, and execute known work through no-reason or                                 plans, red-team tests, proof obligations, and repair memories.
This is how the system avoids destroying hidden behavior while       invariants would turn production traces, rollbacks, failed
still compressing historical accident.                               migrations, and reverted patches into negative memory and
   Verification markets and agent-native software OS. A              proof obligations. Verification markets would let independent
mature substrate needs independent evaluators: proof-lane            proof-lane providers, fuzzers, conformance suites, cell auditors,
providers, fuzzing services, conformance suites, cell auditors,      provenance validators, and runtime monitors compete on
provenance validators, and runtime monitors competing on             evidence quality. Agent-native operating systems would
evidence quality. The agent-facing operating system is then          expose typed changes, behavior cells, proof lanes, policy
not a terminal plus repository checkout. It is a governed            decisions, provenance receipts, runtime traces, and negative
environment exposing typed changes, behavior cells, proof            memory as native system calls rather than leaving agents inside
lanes, policy decisions, provenance receipts, runtime traces,        an unstructured terminal and repository checkout.
and negative memory as native system calls.                             A mature canonical foundry should therefore publish two
   The extreme endpoint is not zero code and not zero engi-          ledgers. The corpus ledger reports what was ingested, rejected,
neering judgment. It is no accidental software: no accidental        ported, preserved, proven, license-cleared, or quarantined. The
architecture, no accidental dependency choice, no accidental         change ledger reports every accepted and failed task: context
CI, no accidental migration ritual, no accidental security policy,   tokens, reasoning tokens, tool calls, invalid actions, proof
no accidental review burden, and no repeated reasoning where         failures, repair loops, wall-clock, review comments, and dollars.
the substrate has already learned the law. The human and agent       The paper’s central numbers should rise or fall with those
frontier moves to irreducible novelty.                               ledgers.

 XXII. T HE F IRST S IX E XPERIMENTS T HAT D ECIDE THE                           XXIV. T HE N O -ACCIDENT H ORIZON
                          T HESIS                                       The strongest form of this paper is not that all future software
   The paper becomes stronger if it stops asking readers to          becomes free. That would be false for arbitrary future programs
believe a grand end state and instead offers a near-term kill        and misleading for reviewers. The stronger and defensible
chain. The first decisive program should be small enough to run      claim is narrower: once accidental representation, repeated
before a full foundry exists and strong enough that a negative       architecture, duplicated contracts, routine behavior families,
result hurts.                                                        proof-route discovery, generated-surface drift, dependency ritu-
   These experiments also protect the paper from its own             als, migration folklore, and repair loops have been quotiented
ambition. The 150×–1,000× story is not the starting claim; it        away, software converges to a residual floor. That floor is the
is the long-horizon envelope after cells, proof lanes, negative      No-Accident Horizon.
memory, and behavior IR mature. The starting claim is harsher        A. The Limit Question
and cleaner: if same-model raw/canonical ablation does not
produce obvious cost and search-work savings, the training-          Let At be the admissible software evidence available at time
token moonshot should not be believed.                            t: repositories, issues, pull requests, tests, traces, incidents,
                                                                  vulnerabilities, reviews, schemas, deployment histories, rejected
 XXIII. F RONTIER E XTENSIONS T HAT M AKE THE T HESIS             patches, documentation, provenance, license metadata, and
                      H ARDER TO I GNORE                          rollback evidence. Let Mt = Φ(At ) be the best governed
   The current paper should be read as a substrate thesis plus a canonical memory produced from that evidence. The memory
research agenda. The strongest next ideas are not cosmetic; they is admissible only if it preserves provenance, weak-oracle
turn the claim from a compression manifesto into a defensible labels, rejected dispositions, security constraints, migration law,
experimental program.                                             and behavior evidence.
   The most important addition is the behavior-cell coverage         Let Y ∼ Pt (Y | At ) be a future software demand drawn
census. If 70–90% of routine product-software changes fall into   from   a declared workload distribution, and let Oτ,H be an
reusable cells and semantic patch cells, the aggressive thesis    acceptance   oracle at evidence tier τ and future horizon H. The
becomes plausible. If coverage stalls at 20–30%, canonical code   oracle  includes  behavior, hidden compatibility, security, migra-
may still be valuable, but the paper becomes an engineering-      tion safety,  provenance,     review policy, and future adaptability.
efficiency paper rather than a training-substrate revolution. The A  foundry   F  maps   (M  t , Y ) to a proof-carrying change object
second most important addition is the paired repository arena,    or to a  refusal. Its all-in   accepted-change cost is
because it directly tests the economic question: can the same CF (Y ) = Cintent + Ccontext + Creason + Ctool + Cverify
or smaller model produce accepted proof-carrying changes
                                                                                + Creview + Crisk + Camortized foundry + Cdefect .
with fewer total tokens, tool calls, failed loops, and reviewer
                                                                                                                                  (37)
interventions?
   Four frontier extensions should remain explicitly future work, The raw baseline Craw (Y ) is the same ledger for the original
not current evidence. Behavior genomes would mine raw human repository and process under the same oracle. The
repositories, traces, incidents, and repairs into a global atlas denominator is therefore cost per verified correct change, not
of behavior families with variants, invariants, tests, proofs, lines of code, source bytes, prompt tokens, or benchmark solve
provenance, and generated projections. Runtime-derived rate.
                                                                     TABLE XXXIV
                                              S IX E XPERIMENTS T HAT C ONVERT THE T HESIS INTO E VIDENCE

 Experiment                       Pass condition                                                      Fails the thesis if
 Same-model substrate abla-       A broad frontier or strong open model solves paired                 Canonical repositories look cleaner but do not reduce search
 tion                             canonical tasks with materially fewer files, tokens, tool calls,    work or accepted-change cost.
                                  failed loops, and reviewer comments than raw tasks.
 Training tokens to accepted-     Same model family reaches fixed accepted-change quality             Representation compression does not become sample-
 change target                    with fewer canonical tokens than raw tokens, with confidence        efficiency gain.
                                  intervals.
 Reasoning/tool/retry reduc-      Paired canonical tasks show fewer planning tokens, hidden           The model spends the same search budget despite the
 tion                             reasoning tokens where measurable, tool calls, invalid edits,       canonical substrate.
                                  proof failures, validation reruns, and retries.
 Foundry behavior preserva-       Ports survive hidden tests, fuzzing, mutation tests, replay,        Canonicalization passes easy tests while losing compatibility
 tion                             migration checks, security negatives, and human adjudica-           ghosts or security behavior.
                                  tion.
 Cost per verified correct        Porting, proof, governance, serving, verification, review, and      Foundry cost or verification overhead erases downstream
 change                           maintenance costs are repaid by repeated accepted-change            economics.
                                  savings.
 Specialist   versus   broad      A canonical specialist matches or beats a broad model on            Supported-domain specialization fails to improve accepted-
 model                            supported canonical work at lower all-in cost.                      change quality, speed, or cost after corrections.


                                                                  TABLE XXXV
                                    H IGHEST-L EVERAGE A DDITIONS FOR A S TRONGER C ANONICAL -C ODE P ROGRAM

 Addition                            Why it matters                                                    Concrete artifact
 Behavior-cell coverage census       Converts moonshot language into a measured market map:            A labeled corpus with per-file and per-change coverage by
                                     what fraction of product software is resource lifecycle,          cell family, plus residual novelty estimates.
                                     auth, policy, workflow, billing, notification, observability,
                                     integration, or migration routine?
 Canonicalization loss function      Prevents the foundry from optimizing prettiness instead of        Multi-objective score: behavior preservation, proof strength,
                                     preserved behavior and lower change cost.                         source entropy, action entropy, security posture, provenance
                                                                                                       quality, and amortized cost.
 Paired repository arena             Makes the decisive claim testable without waiting for full-       Raw/canonical repository pairs, identical issues, hid-
                                     corpus porting.                                                   den tests, proof lanes, reviewer rubrics, and full to-
                                                                                                       ken/tool/dollar traces.
 Negative memory bank                Turns incidents, reverted patches, flaky tests, security bugs,    Versioned forbidden-plan cells and regression generators
                                     and failed migrations into reusable anti-examples.                attached to behavior cells and proof lanes.
 Renderer pluralism                  Keeps the profile ambitious without becoming brittle or           One behavior IR rendered to the primary product profile
                                     cultish.                                                          and to secondary governed profiles where domain con-
                                                                                                       straints require it.
 Foundry amortization ledger         Makes the economics credible.                                     Per-port cost, review cost, proof cost, reuse count, served-
                                                                                                       token savings, accepted-change savings, and break-even
                                                                                                       k∗ .
 Adversarial equivalence audit       Protects against canonical ports that pass easy tests while       Differential replay, fuzzing, mutation testing, symbolic
                                     losing edge behavior.                                             checks where feasible, security review, and human product-
                                                                                                       owner adjudication.



   For a distribution and oracle, define the removable-work                         foundry has a positive guaranteed No-Accident Horizon. In
fraction as                                                                         the distribution-free case,
                                  inf F ∈Fadm EY ∼Pt [CF (Y )]
   ΛNA (Pt , Oτ,H ) = 1 −                                      .           (38)                               inf ΛNA (P, Oτ,H ) = 0.                           (40)
                                        EY ∼Pt [Craw (Y )]                                                     P

The corresponding ideal multiplier is                                               Proof sketch. If a system could always construct, prove, or
                                                                                    correctly reject every arbitrary future behavior at finite bounded
                                         1
                           MNA =              .                            (39)     residual cost, it could decide nontrivial semantic properties of
                                      1 − ΛNA                                       arbitrary programs by encoding those properties as software
This normalization is severe. A 10× result means 90%                                intents. That contradicts the Turing–Rice boundary [43], [69],
removable work, a 100× result means 99% removable work,                             [70]. If the future distribution is unconstrained, no-free-
and a 1,000× result means 99.9% removable work.                                     lunch reasoning gives the learning-theoretic version of the
                                                                                    same warning: an optimizer wins only by exploiting non-
B. No Universal Software Inverse                                                    uniform structure in the task distribution [71]. The shortest
  No universal software inverse. For arbitrary computable pro-                      adequate description of an arbitrary target is also not generally
grams or adversarial future software demands, no computable                         computable in the Kolmogorov sense [72]. A foundry can
dominate useful regions of software space, but it cannot own        E. Numerical Limit Estimate
the shortest proof-carrying description of every possible future       The strongest defensible numerical answer is a regime table,
program.                                                            not a single slogan. Table XXXVI states the removable-work
   This negative result is the boundary that makes the positive
                                                                    fraction ΛNA and reciprocal multiplier MNA for increasingly
theory scientific. The claim is not that a model learns all
                                                                    favorable assumptions.
possible future programs. The claim is that economically im-
                                                                       The table says three things. First, the universal mathematical
portant software is concentrated in repeated behavior families,
                                                                    problem has no positive guaranteed compression. Second, broad
organizational patterns, integration rituals, schemas, policies,
                                                                    commercial software is compressible but still contains enough
migrations, operational failures, and product conventions. That
                                                                    hardware, scientific, regulatory, adversarial, organizational, and
concentration is exactly what canonical code exploits [3], [4],
                                                                    algorithmic novelty that a universal 100× all-in claim is not
[18], [27], [30].
                                                                    defensible. Third, the paper’s real frontier is supported routine
C. The Horizon Equation                                             product software after behavior-genome maturity. In that regime,
   Normalize today’s raw all-in cost mass to one. Decompose         the strongest defensible final-limit planning number is
it into an irreducible floor η and disjoint reducible strata
                                                                     Λ⋆NA,product ≈ 0.990        ⇐⇒         ⋆
                                                                                                           MNA,product ≈ 100 × .
q1 , . . . , qJ :
                                                                                                                             (45)
                J
                X                                                   A cautious theoretical band is
           η+         qj = 1,    qj ≥ 0,      η ≥ 0.        (41)
                j=1                                                                  Λ5%–95%
                                                                                      NA,product ∈ [0.967, 0.998],
Each qj is a removable source of accidental work: repre-                             5%–95%
                                                                                    MNA,product ∈ [30×, 500×].                   (46)
sentation search, repository discovery, duplicate truth, proof-
lane discovery, invalid edit attempts, routine behavior im-         This is a theoretical limit estimate, not a measured result. It is
plementation, generated surface maintenance, retry loops,           stronger than the near-term central target because it assumes
local architecture reconstruction, dependency rituals, migration    mature behavior cells, semantic patch cells, reusable proof
folklore, or repeated review reasoning. Let rj ≥ 1 be the           receipts, negative memory, renderers, and broad amortization.
asymptotic reduction achieved on stratum j by behavior cells,       It is weaker than an unqualified 1,000× claim because
semantic patch cells, proof-carrying changes, canonical profiles,   Equation 43 respects the residual floor.
negative memory, renderers, and reusable evidence.
   The residual cost fraction is                                    F. Falsification Rules
                          J
                         X   qj                 1                      The theory is designed to fail cleanly. Estimate η, qj ,
             sNA = η +          ,     MNA =        .        (42)
                             r                 sNA                  and rj on paired raw/canonical repositories from the same
                         j=1 j
                                                                    lineage under the same model, issue distribution, hidden tests,
Equation 42 is the Amdahl law of inverse software [73]. If          proof lanes, reviewer rubric, and cost ledger. The No-Accident
two techniques reduce the same failed-search loop, they do not      Horizon collapses into ordinary engineering efficiency if any
multiply; they compete for the same qj . The exhausted-options      of the following hold:
limit is
                                         1                            1) the irreducible floor η remains above 3% for routine
                         lim     MNA = .                  (43)           product changes after mature canonicalization;
                   r1 ,...,rJ →∞         η
                                                                      2) behavior-cell and semantic-patch coverage fail to exceed
The foundry does not escape the denominator. It drives every
                                                                         roughly 85% of accepted routine change cost mass;
reducible term toward zero until only η remains.
                                                                      3) covered strata do not reach at least 100× reduction
D. Future-Adaptive Minimum Functional Description Length                 in context, reasoning, invalid-action, retry, and proof-
  The irreducible floor is not merely source length. It is the           discovery cost;
cost of new information, acceptance, evidence, governance,            4) proof, security, provenance, migration, or review over-
and adaptability. An oracle-relative form is                             head grows enough to erase the saved search cost;
                                                                     5) canonical ports lose important compatibility ghosts or
    E[CF (Y )] ≥ E αKO (Y | Mt ) + βLO (Y ) + γEτ (Y )
                                                                        increase downstream defects at equal review standards;
                     + δG(Y ) + ζVH (Y ) .                (44)        6) foundry amortization does not compound across inde-
Here KO (Y | Mt ) is the target behavior not already implied             pendent repositories.
by canonical memory, LO (Y ) is the description length of the       Conversely, the 100× exhausted-options limit becomes con-
acceptance oracle, Eτ (Y ) is the minimum evidence burden,          servative if η < 0.5%, covered routine-change mass exceeds
G(Y ) is governance and provenance burden, and VH (Y ) is           95%, cell-covered strata reach thousands-fold reductions, and
the option-value burden across horizon H. This is the MFDL          proof receipts reuse across many unrelated product lineages
boundary in future-adaptive form: canonicalization can shorten      without loss of behavior or provenance.
descriptions and make proofs reusable, but it cannot make             The final claim is therefore precise enough to defend
required new information disappear [72], [74].                      and large enough to matter: the universe of economically
                                       1x       1x current
(larger reductions lower on chart)


                                       3x
     Improvement multiplier




                                      10x


                                                                                                                Conservative
                                      30x
                                                             No-Accident Horizon

                                                             100x planning limit
                                     100x



                                     300x
                                                                                                                Aggressive
                                     500x

                                            0                    0.25                  0.50                        0.75                               1.0
                                                                           Canonical substrate maturity

Fig. 4. Convergence from current all-in verified-change cost toward the No-Accident Horizon. The conservative curve approaches a 30× mature-foundry limit,
the aggressive curve approaches a 500× upper-tail limit for supported routine-product work, and the dashed line marks the 100× theoretical planning horizon.
The band is a theoretical exhausted-options estimate, not a measured result and not a distribution-free guarantee.



important code can be built increasingly close to the No-                            behavior only within declared contracts. Report preservation
Accident Horizon, but never beyond it. For arbitrary fu-                             tiers, weak-oracle failures, compatibility ghosts, and accepted
ture programs, the guaranteed horizon is zero. For routine                           incompatibilities. Run the same broad model on raw and
product/application software under a mature behavior-genome                          canonical tasks before training a specialist. Measure files
foundry, the strongest defensible final-limit estimate is about                      opened, context tokens, reasoning tokens, tool calls, invalid
100× lower all-in cost per verified correct change, with a                           edits, failed proof lanes, reviewer comments, wall-clock, and
cautious 30×–500× theoretical band. Values above 1,000×                              cost per accepted proof-carrying change. Then run paired
belong to closed behavior-cell lanes where the irreducible floor                     scaling curves before claiming training-token compression.
is below 0.1%, not to unconstrained software as a whole.                                The thesis remains bold because the target is not cleaner
                                                                                     code. The target is a canonical mirror of the software universe:
                                            XXV. L IMITS AND C ONCLUSION             behavior preserved or dispositioned, routine product work
   This paper does not prove the full economic thesis. It does                       collapsed into certified cells, changes expressed as typed
not prove behavior preservation at corpus scale, does not                            operations, proof lanes generated and checked, provenance
prove paired training-token reduction, does not prove that                           carried through every transformation, and runtime failures
a 100B-class canonical specialist replaces all broad frontier                        compiled into negative memory. Human code contains the
coding systems, does not apply to all novel systems or                               behavior, edge cases, incidents, product judgment, and hard-
unsupported domains, and does not prove that behavior cells                          won lessons that matter. Raw human representation is the
cover 70%–90% of routine product behavior. The QLoRA                                 wrong thing to imitate when it encodes local accident rather
pilot is deliberately narrower: canonical translated trajectories                    than durable behavior.
are learnable under a parameter-efficient adaptation setup, and                         The theoretical limit is the No-Accident Horizon developed
the measured forbidden-language markers remain at zero. The                          in Section XXIV. In that limit, agents do not invent local
rest of the thesis must be earned through the claim ledger                           architecture, rediscover repository folklore, guess migration
in Table VI, beginning with the same-model raw/canonical                             law, or re-learn the same auth, billing, upload, policy, and
substrate test.                                                                      audit patterns in every codebase. They operate a constrained
   The research agenda is therefore concrete. Build paired                           software machine and spend compute only where novelty,
raw/canonical repositories from the same lineage. Assign                             evidence, governance, risk, and future optionality remain.
every source artifact a legal/provenance disposition. Port                              The end state is no accidental software: no accidental
                                                                  TABLE XXXVI
                                             N O -ACCIDENT H ORIZON : F INAL -L IMIT E STIMATES BY S COPE

 Scope                             Interpretation                        Conservative   Central exhausted-options limit     Aggressive upper tail
 Arbitrary programs as mathemat-   Distribution-free future soft-          0% / 1×                 0% / 1×                No positive universal bound
 ical objects                      ware, including adversarial and
                                   incompressible targets.
 Broad economically requested      Product apps plus systems, em-         75% / 4×               88% / 8.3×                      96% / 25×
 software                          bedded, data, scientific, security,
                                   mobile, infrastructure, creative
                                   tools, and genuinely new algo-
                                   rithms.
 Routine product and application   SaaS, internal tools, resource        96.7% / 30×            99.0% / 100×                    99.8% / 500×
 software                          lifecycles, auth, policy, billing,
                                   uploads, jobs, webhooks, au-
                                   dit, migrations, observability,
                                   deployment, and integrations.
 Closed behavior-cell lanes        Narrow lanes where the future         99.0% / 100×          99.9% / 1,000×                 99.98% / 5,000×
                                   change is almost entirely cell
                                   selection, parameterization, ren-
                                   derer output, and reusable proof
                                   receipts.



architecture, dependency choice, CI ritual, migration path,                        1) Language Role Collapse: Approach. Rebuild service,
security policy, review burden, or repeated reasoning once                      UI, migration, and scripting roles into fixed profile lanes;
the substrate has learned the law. This paper is a falsifiable                  generate adapters at profile boundaries; remove language-
program for replacing accidental software representation with a                 choice, runtime-choice, and cross-language repair paths.
canonical, proof-carrying substrate for verified correct change.                   The same backend behavior—HTTP routing, database access,
In the strongest form, every remaining unit of engineering buys                 queue consumption, serialization—appears in Python/FastAPI,
novelty, judgment, evidence, governance, or safety.                             Java/Spring, Node/Express, Ruby/Rails, PHP/Laravel, Go/Gin,
                                                                                and C#/ASP.NET, among others. A canonical standard collapses
                   A PPENDIX A                                                  these into one service/core lane and one typed product-surface
 S UPPLEMENTAL C OMPRESSION C ATALOG : C ODE -S PACE                            lane. The model no longer spends capacity learning seven
                   G AIN P RIORS                                                syntactically distinct encodings of identical semantics.
   This supplemental catalog lists the major coding-work gains                  Estimates. Conservative: 4×–6×. Central: 6×–12×. Ag-
available once agent-first canonical code is treated as a substrate             gressive: 12×–20×.
rather than a style guide. Each domain states what is rebuilt,                     2) Framework Collapse: Approach. Rebuild routing, mid-
what becomes generated, what agent action paths disappear,                      dleware, state, and persistence into one service/UI grammar;
and conservative, central, and aggressive gain estimates. The                   generate framework glue; remove local framework DSL choices
gains do not multiply cleanly—many overlap, and several                         and handler-shape variants.
domains share the same underlying token mass. The composite                        Within a single language, framework conventions—
effect must be measured on paired raw/canonical corpora; the                    middleware chains, routing DSLs, ORM query builders,
estimates presented here are prior ranges and target hypotheses,                template engines, configuration idioms—introduce a second
not measured results. Where a per-domain source range such                      layer of representational divergence. Express, Django, Rails,
as 3×–8× is stated, it denotes the ratio of raw-corpus tokens                   Spring, and Laravel each impose a distinct grammar over
to canonical-corpus tokens required to represent equivalent                     the same behavioral primitives. Canonical conversion replaces
behavior. Composite ranges use the explicit denominator named                   all framework-specific grammars with one canonical service
in the row: representation space, action space, training tokens,                grammar, eliminating the combinatorial surface the model must
reasoning/tool/retry tokens, or cost per verified correct change.               memorize.
                                                                                Estimates. Conservative: 3×–5×. Central: 5×–10×. Ag-
A. Infrastructure Compression                                                   gressive: 10×–15×.
   Infrastructure compression eliminates the representational                      3) Generated Truth Collapse: Approach. Rebuild
cost of decisions that carry no behavioral consequence: which                   schemas as the source of truth; generate data transfer
language encodes a REST handler, which framework provides                       objects, clients, validators, fixtures, mocks, and docs; remove
routing, which folder tree organizes source files. These de-                    hand-edited projections and drift repairs.
cisions dominate open-source corpora yet contribute nothing                        Hand-written data transfer objects, API client stubs, re-
to the space of behaviors a model must learn to produce.                        quest/response validators, serialization fixtures, and test facto-
Domains 1–6 target this stratum.                                                ries are all downstream projections of a single schema contract.
In raw corpora these projections diverge, drift, and duplicate.   that the canonical runtime can instantiate, compose, and verify.
Canonical form replaces them with contract-first generation:      Where infrastructure compression removes representational
one source of truth (an API schema or cell contract) produces     divergence, cell compression removes behavioral divergence—
all projections deterministically. The model learns to emit the   the phenomenon whereby identical application semantics
contract, not its many manual echoes.                             (pagination, authentication, billing) are re-implemented from
Estimates. Conservative: 2×–3×. Central: 3×–6×. Ag-               scratch in every codebase with local variation that encodes
gressive: 6×–10×.                                                 no new information. Domains 7–20 target this stratum. To
   4) Layout and Naming Collapse: Approach. Rebuild               keep the catalog compact, several high-win cells are folded
repositories into canonical paths and controlled vocabulary;      into adjacent domains: tenant/org/user belongs to identity and
generate owner maps and generated-zone manifests; remove          policy, feature flags and experiments belong to configuration
file-hunt, synonym, and helper-placement choices.                 policy, cache/invalidation belongs to governed dependency
   Arbitrary folder structures (src/controllers/ vs.              and observability contracts, and UI resource state belongs
app/handlers/ vs. lib/api/), file-naming conven-                  to list/search cells. Patch intermediate representation, reasoning
tions (userService.ts vs. user_service.py vs.                     digests, supply-chain closure, and notebook-to-pipeline com-
UserService.java), and organizational myths consume               pression are treated separately in the meta-compression layer
representational capacity without encoding behavior. A canon-     because their denominators are action, reasoning, governance,
ical repository grammar fixes vocabulary and topology, con-       and workflow entropy rather than source tokens alone.
verting layout noise into a stable, predictable structure the        1) Resource Lifecycle Cells: Approach. Rebuild resource
model can exploit as prior knowledge rather than re-learn per     lifecycle work as typed cell declarations; generate routes,
repository.                                                       SQL, UI state, tests, and fixtures; remove handwritten cre-
Estimates. Conservative: 2×–3×. Central: 3×–5×. Ag-               ate/read/update/delete surfaces and repeated controller edits.
gressive: 5×–8×.                                                     Create, read, update, delete, list, archive, restore, and status
                                                                  transition constitute the single most repeated pattern in product
   5) Dependency Collapse: Approach. Rebuild integrations         software. In raw corpora, each resource lifecycle surface is
behind governed adapters; generate configuration, retry, error,   hand-written with per-project validation, authorization, serial-
and observability wrappers; remove bespoke vendor glue and        ization, and error handling. Canonical resource lifecycle cells
unsafe upgrade routes.                                            reduce this to a typed resource declaration: the model emits
   Every production codebase wraps third-party services—          cell parameters (fields, transitions, access policies) rather than
Stripe, S3, GitHub, Slack, OpenAI, Redis, email providers,        writing route handlers, SQL queries, and test fixtures.
observability backends—in locally invented adapter layers with
inconsistent error handling, retry policies, and configuration    Estimates. Conservative: 3×–8×. Central: 8×–20×. Ag-
surfaces. Canonical adapters provide governed wrappers with       gressive: 20×–50×.
standard interfaces. The model learns one adapter contract per       2) Authentication / Identity / Policy Cells: Approach.
external service rather than hundreds of bespoke wrappers, and    Rebuild identity, tenant, organization, session, and policy
local glue code vanishes entirely.                                behavior as governed cells; generate guards, recovery flows,
Estimates. Conservative: 2×–3×. Central: 3×–5×. Ag-               fixtures, and negative tests; remove bespoke auth plumbing.
gressive: 5×–8×.                                                     Login flows, session management, token issuance and
                                                                  validation, external identity-provider integration, role-based
   6) Build and Test Collapse: Approach. Rebuild local and        access control, attribute-based access control, permission
CI validation as proof lanes; generate GitHub/GitLab workflow     checks, password reset, multi-factor authentication, and account
settings, artifacts, and required checks; remove build folklore   recovery are repeated in nearly every production application—
and permission guesswork.                                         with dangerous variation. Security-critical code is the worst
   Custom shell scripts, undocumented CI gate configurations,
                                                                  candidate for bespoke re-implementation and the best candidate
Makefile folklore, local environment assumptions, and ad-hoc
                                                                  for cell compression. A canonical identity cell encapsulates the
test harnesses constitute a significant fraction of repository
                                                                  full policy surface; the model configures it rather than writing
tokens. Canonical form replaces them with standard proof
                                                                  cryptographic plumbing.
lanes: a fixed set of commands that produce expected artifacts
(type-checked binary, migration proof, test evidence, security    Estimates. Conservative: 3×–10×. Central: 10×–30×.
scan). The model learns the proof protocol, not the archaeology   Aggressive: 30×–100×.
of each project’s build system.                                      3) Form and Input Validation Cells: Approach. Rebuild
Estimates. Conservative: 2×–3×. Central: 2×–4×. Ag-               validation as schema-owned constraints; generate frontend,
gressive: 4×–6×.                                                  API, database, and test projections; remove four-layer drift and
                                                                  hand-maintained form logic.
                                                                     Validation logic is duplicated across at least four layers
B. Behavior Cell Compression                                      in typical applications: frontend form validators, API request
  Behavior cells are the canonical unit of application logic: a   schemas, database constraints, and test assertions. Each layer
named, typed, proof-carrying declaration of a behavioral intent   uses a different validation DSL, and drift between layers is a
                                                            TABLE XXXVII
                                      I NFRASTRUCTURE C OMPRESSION D OMAINS (1–6): G AIN E STIMATES

#   Domain                                                                                            Conservative   Central   Aggressive
1   Language Role Collapse                                                                              4×–6×        6×–12×    12×–20×
2   Framework Collapse                                                                                  3×–5×        5×–10×    10×–15×
3   Generated Truth Collapse                                                                            2×–3×         3×–6×     6×–10×
4   Layout/Naming Collapse                                                                              2×–3×         3×–5×      5×–8×
5   Dependency Collapse                                                                                 2×–3×         3×–5×      5×–8×
6   Build/Test Collapse                                                                                 2×–3×         2×–4×      4×–6×



persistent source of bugs. Canonical validation cells generate          retry semantics and idempotency checks. Canonical job cells
all four projections from a single schema, eliminating cross-           declare the reliability contract; the runtime enforces it.
layer inconsistency and the representational cost of maintaining        Estimates. Conservative: 2×–5×. Central: 5×–15×. Ag-
parallel validation grammars.                                           gressive: 15×–30×.
Estimates. Conservative: 2×–5×. Central: 5×–15×. Ag-                       7) File Upload and Media Cells: Approach. Rebuild
gressive: 15×–30×.                                                      uploads as storage and policy declarations; generate signed
   4) Pagination / Search / Filter Cells: Approach. Re-                 URLs, scanners, transforms, fixtures, and audit events; remove
build list/search behavior as a resource-state cell; gener-             ad hoc storage/security code.
ate durable-data queries, API cursors, product-surface state,              Signed URL generation, virus scanning, image processing
empty/error/loading views, and tests; remove custom list                pipelines, storage backend abstraction, content-type validation,
implementations.                                                        and access control for uploaded media combine security,
   Paginated lists with sorting, filtering, full-text search, cursor-   storage, and processing complexity that is repeated in nearly
based or offset pagination, and search index synchronization            every user-facing application. Canonical media cells declare
represent massive UI/API/database repetition. The same behav-           upload constraints, processing steps, and access policies;
ioral contract—“return a filtered, sorted, paginated view of a          infrastructure details are resolved by the runtime.
resource collection”—is implemented independently at every              Estimates. Conservative: 3×–8×. Central: 8×–20×. Ag-
layer with per-project conventions. A canonical pagination cell         gressive: 20×–40×.
parameterizes the contract once; all layers are generated.
                                                                           8) Billing / Subscription / Payment Cells: Approach. Re-
Estimates. Conservative: 3×–8×. Central: 8×–20×. Ag-                    build payments as subscription and ledger state machines; gen-
gressive: 20×–50×.                                                      erate webhook handlers, idempotency, reconciliation, fixtures,
   5) SQL Migration and Data Invariant Cells: Approach.                 and alerts; remove brittle payment glue.
Rebuild data change as declared invariants, lock budgets, and              Subscription lifecycle management, invoice preview and pro-
expand/contract plans; generate SQL and replay checks; remove           ration, payment method lifecycle, webhook handling for Stripe
opaque migration scripts and unsafe rollbacks.                          and other payment providers, dunning flows, and tax calculation
   Expand/contract migrations, data backfills, rollback plans,          represent a common SaaS surface with dangerous edge cases
data-shape invariants, and lock-budget management carry high            in currency handling, idempotency, and state reconciliation.
failure cost and high repetition. In raw corpora, migration files       Canonical billing cells parameterize the subscription model
are opaque SQL scripts with no machine-readable invariant or            and payment provider; the full webhook surface, idempotency
proof of safety. Canonical migration cells declare the schema           layer, and state machine are generated.
transition, invariant constraints, and acceptable lock budgets; Estimates. Conservative: 3×–10×. Central: 10×–30×.
the runtime generates the SQL and verifies safety properties Aggressive: 30×–100×.
before execution.
                                                                      9) Notification / Email / Template Cells: Approach. Re-
Estimates. Conservative: 2×–5×. Central: 5×–10×. Ag- build outbound messaging as channel and template policy;
gressive: 10×–20×.                                                  generate provider adapters, preferences, retries, and observabil-
   6) Background Job / Queue / Scheduler Cells: Approach. ity; remove local email/SMS/push wrappers.
Rebuild async work as idempotent job contracts; generate              Multi-channel notification dispatch (email, SMS, push, in-
retries, dead-letter routing, schedules, metrics, and tests; remove app),  delivery tracking, template rendering with variable
queue-specific reliability rewrites.                                substitution, user preference management, and retry logic for
   Retry policies, idempotency guarantees, exponential backoff, transient delivery failures. Canonical notification cells declare
dead-letter queue routing, scheduled task management, and con- channels, templates, and delivery policies; the runtime handles
currency limits constitute the reliability layer of asynchronous provider integration and observability.
processing. The same reliability logic is re-implemented in             Estimates. Conservative: 2×–5×. Central: 5×–15×. Ag-
every codebase that uses background jobs, with subtle bugs in           gressive: 15×–30×.
   10) Webhook and Integration Cells: Approach. Rebuild               14) Error Handling and Result Envelope Cells: Approach.
integrations as signed event contracts; generate verification,     Rebuild failure handling as typed result envelopes; generate
replay, deduplication, dispatch, and fixtures; remove provider-    error codes, retry classifications, UI messages, and tests; remove
specific webhook boilerplate.                                      stringly exceptions and null-path ambiguity.
   Inbound webhook verification, signature validation, idem-          Typed error envelopes, machine-readable error codes, retry
potent event processing, replay handling, deduplication, and       classification (transient vs. permanent), user-facing vs. internal
provider-specific payload parsing. Integration-heavy applica-      error separation, and structured error metadata. Raw codebases
tions repeat this pattern per external provider, each with         exhibit a chaotic mixture of exceptions, HTTP status codes,
a different signing scheme and payload format. Canonical           null returns, and string error messages. Canonical error cells
integration cells declare the provider contract and verification   impose a typed result algebra; the model learns to classify and
method; the idempotency and processing pipeline are standard.      route errors rather than invent ad-hoc handling per call site.
Estimates. Conservative: 2×–5×. Central: 5×–15×. Ag-               Estimates. Conservative: 2×–4×. Central: 4×–8×. Ag-
gressive: 15×–30×.                                                 gressive: 8×–12×.
   11) Audit Log and Event History Cells: Approach. Re-
build audit as append-only event policy; generate event writers,   C. Meta-Compression
retention, queries, and tamper checks; remove scattered com-          Meta-compression operates not on source tokens but on the
pliance logging.                                                   action space and reasoning space of the agent itself. Where
   Append-only event streams, compliance audit trails, ac-         infrastructure and cell compression shrink the representation a
tor/action/resource/timestamp recording, and tamper-evident log    model must learn to read and write, meta-compression shrinks
integrity are required in compliance-heavy systems (healthcare,    the space of trajectories a model must explore during gener-
finance, government). In raw corpora, audit logging is either      ation. The gains here are measured not in token-count ratios
absent, ad-hoc, or inconsistently applied. Canonical audit cells   but in the reduction of invalid action paths, wasted inference
declare the event schema and retention policy; the runtime         steps, unproductive exploration, review burden, supply-chain
guarantees append-only semantics and query access.                 ambiguity, and workflow reinvention. Domains 21–30 target
Estimates. Conservative: 2×–5×. Central: 5×–10×. Ag-               this stratum.
gressive: 10×–20×.                                                    1) Repair-Path Collapse: Approach. Rebuild patching as
   12) Observability / Logging / Tracing Cells: Approach.          constrained edit policy; generate legal edit maps, proof routes,
Rebuild telemetry as a cross-cutting contract; generate logs,      and no-edit zones; remove arbitrary file, command, migration,
spans, metrics, health checks, and correlation IDs; remove         and dependency choices.
inconsistent instrumentation edits.                                   In a canonical environment, the agent no longer selects
   Structured logging, distributed tracing with context propa-     among arbitrary files to edit, frameworks to invoke, proof
gation, metrics collection and export, request-ID propagation      commands to run, generated artifacts to modify, or migration
across service boundaries, and health-check endpoints. These       strategies to attempt. The canonical grammar constrains every
cross-cutting concerns are woven inconsistently through raw        dimension of the action space simultaneously: which files are
codebases, often with conflicting log formats and missing trace    mutable, which cells accept parameters, which proof lanes
context. Canonical observability cells declare the instrumenta-    must pass, which artifacts are generated. Invalid edit paths—
tion contract; the runtime injects it uniformly.                   the overwhelming majority of the raw action space—vanish
                                                                   entirely. This is the single largest compression domain by
Estimates. Conservative: 2×–3×. Central: 3×–8×. Ag-                estimated magnitude, because the space of wrong actions in
gressive: 8×–15×.                                                  unconstrained codebases is combinatorially vast.
   13) Configuration / Secrets / Environment Cells: Approach. Estimates. Conservative: 10×–100×. Central: 100×–
Rebuild configuration, secrets, feature flags, and experiments 10,000×. Aggressive: 10,000×–100,000×.
as typed policy; generate env validation, rotation checks, flag
                                                                      2) Negative-Path Curriculum: Approach. Rebuild mis-
gates, and rollout tests; remove .env folklore.
                                                                   takes as labeled curriculum; generate invalid edits, missing
   Secret rotation, environment-specific configuration, feature proofs, unsafe migrations, and generated-zone violations;
flag management, configuration validation at startup, and secret- remove ambiguous definitions of wrongness.
leakage prevention. In raw corpora, .env files, hardcoded             Canonical form enables a training curriculum that includes
secrets, and undocumented environment variables constitute a not only correct canonical code but also labeled negative
persistent security and reliability risk. Canonical configuration examples: editing generated files, applying patches to the
cells declare the configuration schema with types, defaults, and wrong architectural layer, writing unsafe migrations without
secret classifications; the runtime validates at boot and enforces lock-budget declarations, duplicating generated data-transfer-
rotation policies.                                                 object definitions, and skipping proof lanes. These negatives
Estimates. Conservative: 2×–4×. Central: 4×–8×. Ag- are cheap to produce in a canonical environment (any violation
gressive: 8×–15×.                                                  of the grammar is a negative) and expensive to produce in raw
                                                             TABLE XXXVIII
                                      B EHAVIOR C ELL C OMPRESSION D OMAINS (7–20): G AIN E STIMATES

#    Domain                                                                                        Conservative   Central   Aggressive
7    Resource Lifecycle                                                                                3×–8×       8×–20×    20×–50×
8    Authentication / Identity / Policy                                                                3×–10×     10×–30×   30×–100×
9    Form / Input Validation                                                                           2×–5×       5×–15×    15×–30×
10   Pagination / Search / Filter                                                                      3×–8×       8×–20×    20×–50×
11   SQL Migration / Data Invariants                                                                   2×–5×       5×–10×   10×–20×
12   Background Job / Queue / Scheduler                                                                2×–5×       5×–15×   15×–30×
13   File Upload / Media                                                                               3×–8×       8×–20×    20×–40×
14   Billing / Subscription / Payment                                                                  3×–10×     10×–30×   30×–100×
15   Notification / Email / Template                                                                   2×–5×       5×–15×   15×–30×
16   Webhook / Integration                                                                             2×–5×       5×–15×    15×–30×
17   Audit Log / Event History                                                                         2×–5×       5×–10×    10×–20×
18   Observability / Logging / Tracing                                                                 2×–3×        3×–8×    8×–15×
19   Config / Secrets / Environment                                                                    2×–4×        4×–8×     8×–15×
20   Error Handling / Result Envelope                                                                  2×–4×        4×–8×    8×–12×



corpora (where “wrong” is ambiguous). The model learns the               Many changes recur across repositories: add field, migrate
boundary of correct behavior, not just its interior.                  nullable to required, add permission edge, rotate secret, add
Estimates. Conservative: 2×–5×. Central: 5×–15×. Ag-                  idempotency key, upgrade dependency safely, split table, add
gressive: 15×–50×.                                                    audit trail, deprecate API field, or convert sync work to an
                                                                      idempotent job. Semantic patch cells make those changes first-
   3) Proof-Carrying Change Objects: Approach. Rebuild                class. The agent binds parameters and discharges obligations
diffs as structured change objects and patch IR; generate intent,     instead of inventing edits file by file.
affected cells, proofs, receipts, and rollback evidence; remove
bare diff-only completion paths.                                      Estimates. Conservative: 10×–50×. Central: 50×–
                                                                      1,000×. Aggressive: 1,000×–10,000×.
   In canonical form, a patch is not a raw diff. It is a structured
change object comprising: the declared intent, the affected              6) Constrained Edit Grammar: Approach. Rebuild edit-
cells, the generated delta, the migration proof, the security ing as legal typed operations over behavior IR, cells, schemas,
proof, and the test evidence. The model learns to produce the and policies; reject illegal files, operations, and proof omissions
proof route—the full trajectory from intent to verified change— before generation.
rather than a bare textual patch whose correctness must be               Repair-path collapse removes many wrong trajectories after
inferred post-hoc. This transforms code generation from a the agent chooses a path. A constrained edit grammar removes
single-shot prediction problem into a structured reasoning chain them before choice. Generated files are immutable; migrations
with verifiable intermediate steps.                                   must declare lock budgets and rollback; policy changes must
Estimates. Conservative: 2×–5×. Central: 5×–10×. Ag- emit negative tests; dependency changes must route through
gressive: 10×–20×.                                                    governed upgrade lanes. The agent sees a small legal action
                                                                      set instead of a whole filesystem.
   4) Reasoning Digest and Plan-Cache Compression: Ap-
proach. Rebuild repeated agent cognition as versioned rea- Estimates. Conservative: 100×–1,000×. Central: 1,000×–
soning digests; generate task routes, known failure modes, 100,000×. Aggressive: 100,000×+.
proof obligations, and repair playbooks; remove repeated repo            7) Proof-Lane Receipt Reuse: Approach. Rebuild verifi-
archaeology.                                                          cation as reusable receipts; generate migration replay, rollback
   Current agents spend inference tokens rediscovering archi- evidence, policy checks, and security receipts; remove repeated
tecture, ownership, generated zones, tests, migration rituals, proof interpretation and review reconstruction.
and safe repair strategies. Canonical repositories should store a        Proof lanes define commands. Receipt reuse defines the
compact reasoning map: task class to affected cells, issue type evidence object that survives the command: what was checked,
to legal edit set, failure signature to repair strategy, policy delta which obligations changed, which logs matter, what failed
to required test matrix, and dependency update to compatibility before repair, and what rollback means. Reviewers and agents
checks. This turns repeated thought into substrate memory.            inspect the receipt instead of reconstructing proof meaning
Estimates. Conservative: 3×–8×. Central: 8×–50×. Ag- from raw logs.
gressive: 50×–200×.                                                   Estimates. Conservative: 3×–8×. Central: 8×–30×. Ag-
   5) Semantic Patch Cells: Approach. Rebuild recurring               gressive: 30×–100×.
changes as typed transformations; generate blast radius, precon-        8) Supply-Chain and Dependency Closure: Approach.
ditions, proofs, tests, and rollbacks; remove raw-diff invention      Rebuild package selection as governed capability resolution;
for common edits.                                                     generate adapters, provenance, license, bill-of-materials, vul-
nerability, upgrade, and rollback evidence; remove arbitrary           seven parallel decoders for the same semantic space. Agent
package choice.                                                        action-space reduction is larger still, because it compounds
   Dependencies are hidden code expansion. A single import             source compression with the elimination of invalid edit trajec-
can carry transitive code, build scripts, licenses, vulnerabilities,   tories (Domain 21). Reasoning-token reduction is a separate
and runtime behavior. Canonical form should resolve verified           denominator: it measures how often the agent must rediscover
capabilities rather than package names: password hashing, email        architecture, tests, proof routes, repair strategy, dependency
send, payment webhook, rate limit, or object storage. Each             law, and review expectations that can instead be compiled into
capability has approved providers, adapters, provenance, proof         reasoning digests, proof receipts, and semantic patch cells.
lanes, and upgrade routes.                                                12) Theoretical Limit: Minimum Functional Description
Estimates. Conservative: 2×–5×. Central: 5×–20×. Ag-                   Length: The compression frontier converges toward a the-
gressive: 20×–100×.                                                    oretical limit we term the Minimum Functional Description
   9) Notebook-to-Pipeline Compression: Approach. Re-                  Length: the shortest canonical specification, plus proofs, plus
build exploratory notebooks as typed data pipelines; generate          renderer needed to produce a fully working system. Minimum
environment locks, provenance, tests, parameter cells, and             Functional Description Length is not a code-golf metric; it is
scheduled jobs; remove copy-pasted exploratory state.                  the information-theoretic minimum over the space of behavioral
   Notebook-heavy software often stores executable history             specifications that can be mechanically verified and rendered
rather than reproducible behavior. Canonical conversion sep-           into executable artifacts. For routine product software—the
arates exploration from pipeline truth: cells become typed             SaaS platforms, internal tools, and resource-heavy services that
data steps, parameters become schema, plots and reports                constitute the majority of commercial codebases—we estimate
become generated projections, and environments become locked           that 70–90% of behavior may eventually be expressible as
artifacts. The agent learns the pipeline graph rather than the         cell composition, generated surfaces, and policy configuration.
accidental order of notebook execution.                                The remaining 10–30% is true domain-specific logic: novel
                                                                       algorithms, unique business rules, and irreducible problem-
Estimates. Conservative: 3×–10×. Central: 10×–50×.
                                                                       specific reasoning that no canonical grammar can absorb
Aggressive: 50×–200×.
                                                                       without becoming domain-specific itself.
   10) Runtime and Negative Memory Compression: Approach.                 The theoretical limit is not shorter code. The theoretical
Rebuild incidents, reverts, failed patches, hidden compatibility,      limit is no bespoke code unless the behavior is novel.
and production traces as living invariants and forbidden plans;
remove repeated rediscovery of bad worlds.
   The raw corpus mostly preserves accepted code, but software                                        R EFERENCES
expertise also lives in what failed: unsafe migrations, auth
bypasses, flaky tests, reverted patches, support incidents, and         [1] BigCode Project, “The Stack v2,” https://huggingface.co/datasets/bi
                                                                            gcode/the-stack-v2, 2024, dataset card: 67.5TB full, 32.1TB deduped,
production-only edge cases. Canonical memory turns those                    roughly 900B train-full tokens, over 3B files, 658 languages; accessed:
failures into anti-examples, negative tests, proof obligations,             2026-05-14.
and reasoning warnings. Every failure becomes a compression             [2] A. Lozhkov, R. Li, L. B. Allal, F. Cassano, J. Lamy-Poirier, N. Tazi,
                                                                            A. Tang, D. Pykhtar, J. Liu, Y. Wei, T. Liu, M. Tian, D. Kocetkov,
artifact.                                                                   A. Zucker, Y. Belkada, Z. Wang, Q. Liu, D. Abulkhanov, I. Paul, Z. Li,
Estimates. Conservative: 2×–5×. Central: 5×–25×. Ag-                        W.-D. Li, M. Risdal, J. Li, J. Zhu, T. Y. Zhuo, E. Zheltonozhskii,
                                                                            N. O. O. Dade, W. Yu, L. Krauss, N. Jain, Y. Su, X. He, M. Dey,
gressive: 25×–100×.                                                         E. Abati, Y. Chai, N. Muennighoff, X. Tang, M. Oblokulov, C. Akiki,
                                                                            M. Marone, C. Mou, M. Mishra, A. Gu, B. Hui, T. Dao, A. Zebaze,
   11) Composite Gain Estimates: The per-domain estimates                   O. Dehaene, N. Patry, C. Xu, J. McAuley, H. Hu, T. Scholak, S. Paquet,
above cannot be multiplied naı̈vely: language collapse and                  J. Robinson, C. J. Anderson, N. Chapados, M. Patwary, N. Tajbakhsh,
                                                                            Y. Jernite, C. M. Ferrandis, L. Zhang, S. Hughes, T. Wolf, A. Guha,
framework collapse share token mass; resource lifecycle cells               L. von Werra, and H. de Vries, “StarCoder 2 and The Stack v2:
and validation cells overlap on the same source files; repair-path          The next generation,” arXiv preprint arXiv:2402.19173, 2024. [Online].
collapse subsumes portions of every other domain. Table XL                  Available: https://arxiv.org/abs/2402.19173
                                                                        [3] C. V. Lopes, P. Maj, P. Martins, V. Saini, D. Yang, J. Zitny, H. Sajnani, and
presents composite estimates across five measurement axes,                  J. Vitek, “DéjàVu: A map of code duplicates on GitHub,” in Proceedings
derived from conservative overlap-discounting of the individual             of the ACM on Programming Languages, vol. 1, no. OOPSLA, 2017,
domains. These composites represent the full-stack prior: the               pp. 84:1–84:28, analyzed 4.5M non-fork GitHub projects: only 85M of
                                                                            428M files were unique (about 70% clones).
expected gain when all canonical transformations are applied            [4] M. H. Nguyen, B. Adams, and A. E. Hassan, “Jupyter notebooks
simultaneously to a representative product codebase.                        on GitHub: Characteristics and code clones,” arXiv preprint
   The distinction between literal source-token reduction and               arXiv:2007.10146, 2020, found more than 70% of all code snippets
                                                                            were exact copies and about half of notebooks had no unique snippet.
effective representation-space reduction is critical. Source                [Online]. Available: https://arxiv.org/abs/2007.10146
tokens measure the physical size of the corpus; representation          [5] OpenAI and Princeton NLP, “SWE-bench Verified: Human-validated
space measures the number of distinct behavioral encodings                  software engineering tasks,” https://www.swebench.com/verified.html,
the model must learn to produce. A 5× source-token reduction                2024, human-validated subset of 500 SWE-bench instances.
                                                                        [6] B. Yu, Y. Zhu, P. He, and D. Kang, “UTBoost: Rigorous evaluation of
that also collapses seven languages into one yields a far larger            coding agents on SWE-Bench,” arXiv preprint arXiv:2506.09289, 2025,
effective reduction, because the model no longer maintains                  aCL 2025. [Online]. Available: https://arxiv.org/abs/2506.09289
                                                                    TABLE XXXIX
                                                M ETA -C OMPRESSION D OMAINS (21–30): G AIN E STIMATES

#     Domain                                                                                   Conservative            Central                Aggressive
21    Repair-Path Collapse                                                                      10×–100×           100×–10,000×          10,000×–100,000×
22    Negative-Path Curriculum                                                                    2×–5×               5×–15×                  15×–50×
23    Proof-Carrying Change Objects                                                               2×–5×               5×–10×                  10×–20×
24    Reasoning Digests / Plan Cache                                                              3×–8×               8×–50×                 50×–200×
25    Semantic Patch Cells                                                                       10×–50×            50×–1,000×            1,000×–10,000×
26    Constrained Edit Grammar                                                                 100×–1,000×       1,000×–100,000×             100,000×+
27    Proof-Lane Receipt Reuse                                                                    3×–8×               8×–30×                 30×–100×
28    Supply-Chain / Dependency Closure                                                           2×–5×               5×–20×                 20×–100×
29    Notebook-to-Pipeline                                                                        3×–10×             10×–50×                 50×–200×
30    Runtime / Negative Memory                                                                   2×–5×               5×–25×                 25×–100×


                                                                TABLE XL
              C OMPOSITE G AIN E STIMATES ACROSS A LL 30 C OMPRESSION D OMAINS (D ENOMINATOR -S PECIFIC ; N OT M ULTIPLICATIVE )

Measurement Axis                                                                                    Conservative            Central             Aggressive
Literal source-token reduction                                                                        2×–8×                3×–10×                10×–30×
Effective representation-space reduction                                                             20×–40×              40×–150×             100×–300×
Agent action-space reduction                                                                       100×–1,000×        1,000×–100,000×           100,000×+
Training-token efficiency                                                                            10×–30×              30×–150×            150×–1,000×
Reasoning/tool/retry-token reduction                                                                  3×–10×              10×–100×            100×–10,000×
Cost per verified correct change                                                                      3×–10×               10×–50×             50×–1,000×



 [7] J. Becker, A. Rush, B. Barnes, and N. Rush, “Measuring the impact of             dels, 2025, documents 1T total parameters, 32B activated parameters, and
     early-2025 ai on experienced open-source developer productivity,” arXiv          long-context mixture-of-experts serving profile; accessed: 2026-05-14.
     preprint arXiv:2507.09089, 2025, randomized controlled trial reporting      [16] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang,
     19% longer completion time with AI tooling in the studied setting.               G. Chen, X. Bi, Y. Wu, Y. K. Li, F. Luo, Y. Xiong, and
     [Online]. Available: https://arxiv.org/abs/2507.09089                            W. Liang, “DeepSeek-Coder: When the large language model meets
 [8] J. Becker, N. Rush, T. Cunningham, D. Rein, and K. Mahamud, “We are              programming,” arXiv preprint arXiv:2401.14196, 2024. [Online].
     changing our developer productivity experiment design,” https://metr.org         Available: https://arxiv.org/abs/2401.14196
     /blog/2026-02-24-uplift-update/, 2 2026, discusses selection effects and    [17] Qwen Team, “Qwen2.5-Coder technical report,” arXiv preprint
     updated evidence after the early-2025 developer productivity experiment;         arXiv:2409.12186, 2024. [Online]. Available: https://arxiv.org/abs/2409.1
     accessed: 2026-05-28.                                                            2186
 [9] E. Abrokwah and T. A. Ghaleb, “An empirical study of complexity,            [18] A. Hindle, E. T. Barr, Z. Su, M. Gabel, and P. Devanbu, “On the natural-
     heterogeneity, and compliance of GitHub Actions workflows,” arXiv                ness of software,” in Proceedings of the 34th International Conference
     preprint arXiv:2507.18062, 2025, registered report accepted at ICSME             on Software Engineering (ICSE), 2012, pp. 837–847, foundational work
     2025. [Online]. Available: https://arxiv.org/abs/2507.18062                      showing that software is highly repetitive and predictable, supporting
[10] R.-M. Karampatsis, M. Linares-Vásquez, O. Chaparro, and G. Bavota,              the use of statistical language models for code.
     “An empirical study of the evolution of GitHub Actions workflows,”          [19] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and
     https://arxiv.org/abs/2602.14572, 2026, reports analysis of 49K+                 K. Narasimhan, “SWE-bench: Can language models resolve real-world
     repositories, 267K+ workflow change histories, and 3.4M+ workflow file           github issues?” arXiv preprint arXiv:2310.06770, 2023. [Online].
     versions.                                                                        Available: https://arxiv.org/abs/2310.06770
[11] Y. Kubo, F. Kanei, M. Akiyama, T. Wakai, and T. Mori, “Action               [20] I. Badertdinov, A. Golubev, M. Nekrashevich, A. Shevtsov, S. Karasik,
     required: A mixed-methods study of security practices in GitHub                  A. Andriushchenko, M. Trofimova, D. Litvintseva, and B. Yangel,
     Actions,” in Proceedings of the Network and Distributed System Security          “SWE-rebench: An automated pipeline for task collection and
     Symposium (NDSS), 2026, analyzed 338,812 public repositories and                 decontaminated evaluation of software engineering agents,” arXiv
     found low implementation rates across five GitHub Actions security               preprint arXiv:2505.20411, 2025. [Online]. Available: https://arxiv.org/
     practices. [Online]. Available: https://www.ndss-symposium.org/ndss-p            abs/2505.20411
     aper/action-required-a-mixed-methods-study-of-security-practices-in-g       [21] OpenAPI Initiative, “OpenAPI Specification version 3.1.0,” https://spec
     ithub-actions/                                                                   .openapis.org/oas/v3.1.0.html, 2021, accessed: 2026-05-28.
[12] GitGuardian, “State of secrets sprawl 2026,” https://www.gitguardian.       [22] Google, “Protocol buffers overview,” https://protobuf.dev/overview/,
     com/state-of-secrets-sprawl-report-2026, 2026, reports 28.65 million             2026, accessed: 2026-05-28.
     new hardcoded secrets in public GitHub commits in 2025 and 34%              [23] C. Lattner, M. Amini, U. Bondhugula, A. Cohen, A. Davis, J. Pienaar,
     year-over-year growth; accessed: 2026-05-28.                                     R. Riddle, T. Shpeisman, N. Vasilache, and O. Zinenko, “MLIR: Scaling
[13] GitHub, “Octoverse 2025: A new developer joins github every second               compiler infrastructure for domain specific computation,” in Proceedings
     as ai leads typescript to number one,” https://github.blog/news-insights/        of the IEEE/ACM International Symposium on Code Generation and
     octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-l            Optimization (CGO), 2021, pp. 2–14.
     eads-typescript-to-1/, 2025, reports more than 180 million developers,      [24] Linux Kernel Documentation, “Coccinelle,” https://docs.kernel.org/dev-t
     395 million public/open-source repositories, about 230 new repositories          ools/coccinelle.html, 2026, accessed: 2026-05-28.
     per minute, and TypeScript overtaking Python and JavaScript in August       [25] GitHub, “CodeQL documentation,” https://codeql.github.com/docs/, 2026,
     2025; accessed: 2026-05-28.                                                      accessed: 2026-05-14.
[14] Moonshot AI, “Kimi K2: Open agentic intelligence,” arXiv preprint           [26] M. Willsey, C. Nandi, Y. R. Wang, O. Flatt, Z. Tatlock, and P. Panchekha,
     arXiv:2507.20534, 2025. [Online]. Available: https://arxiv.org/abs/2507          “egg: Fast and extensible equality saturation,” Proceedings of the ACM
     .20534                                                                           on Programming Languages, vol. 5, no. POPL, pp. 1–29, 2021. [Online].
[15] ——, “Kimi K2 model documentation,” https://platform.kimi.ai/docs/mo              Available: https://arxiv.org/abs/2004.03082
[27] K. Ellis, C. Wong, M. Nye, M. Sable-Meyer, L. Cary, L. Morales,              [46] Y. Jia and M. Harman, “An analysis and survey of the development of
     L. Hewitt, A. Solar-Lezama, and J. B. Tenenbaum, “DreamCoder:                     mutation testing,” IEEE Transactions on Software Engineering, vol. 37,
     Growing generalizable, interpretable knowledge with wake-sleep                    no. 5, pp. 649–678, 2011.
     bayesian program learning,” arXiv preprint arXiv:2006.08381, 2020.           [47] C. Cadar, D. Dunbar, and D. Engler, “KLEE: Unassisted and automatic
     [Online]. Available: https://arxiv.org/abs/2006.08381                             generation of high-coverage tests for complex systems programs,” in
[28] J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai,                      Proceedings of the 8th USENIX Symposium on Operating Systems Design
     E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl,                        and Implementation (OSDI), 2008, pp. 209–224. [Online]. Available:
     A. Clark, T. Hennigan, E. Noland, K. Millican, G. van den Driessche,              https://www.usenix.org/event/osdi08/tech/full papers/cadar/cadar.pdf
     B. Damoc, A. Guy, S. Osindero, K. Simonyan, E. Elsen, J. W. Rae,             [48] X. Leroy, S. Blazy, D. Kästner, B. Schommer, M. Pister, and C. Ferdinand,
     O. Vinyals, and L. Sifre, “Training compute-optimal large language                “The CompCert C verified compiler: Documentation and user’s manual,”
     models,” arXiv preprint arXiv:2203.15556, 2022. [Online]. Available:              https://compcert.org/man/manual.pdf, 2024, accessed: 2026-05-28.
     https://arxiv.org/abs/2203.15556                                             [49] seL4 Foundation, “seL4 verification proofs,” https://sel4.systems/Verific
[29] C. Lattner and V. Adve, “LLVM: A compilation framework for lifelong               ation/proofs.html, 2026, accessed: 2026-05-28.
     program analysis and transformation,” in Proceedings of the International    [50] Y. Wei, F. Cassano, J. Liu, Y. Ding, N. Jain, H. de Vries, L. von Werra,
     Symposium on Code Generation and Optimization (CGO), 2004, pp. 75–                A. Guha, and L. Zhang, “Arctic-SnowCoder: Demystifying high-quality
     86.                                                                               data in code pretraining,” arXiv preprint arXiv:2409.02326, 2024, 1.3B
[30] P. Clements and L. Northrop, Software Product Lines: Practices and                model using 555B tokens in staged data refinement beat or matched
     Patterns. Addison-Wesley, 2002.                                                   models trained on much larger token budgets. [Online]. Available:
[31] G. C. Necula, “Proof-carrying code,” in Proceedings of the 24th                   https://arxiv.org/abs/2409.02326
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming                    [51] S. Gunasekar, Y. Zhang, J. Aneja, C. C. T. Mendes, A. D. Giorno,
     Languages, 1997, pp. 106–119. [Online]. Available: https://people.eecs.           S. Gopi, M. Javaheripi, P. Kauffmann, G. de Rosa, O. Saarikivi,
     berkeley.edu/∼necula/papers.html                                                  A. Salim, S. Shah, H. S. Behl, X. Wang, S. Bubeck, R. Eldan,
[32] Synopsys, “New synopsys report finds 74% of codebases contained high-             A. T. Kalai, Y. T. Lee, and Y. Li, “Textbooks are all you
     risk open source vulnerabilities,” https://news.synopsys.com/2024-02-2            need,” arXiv preprint arXiv:2306.11644, 2023. [Online]. Available:
     7-New-Synopsys-Report-Finds-74-of-Codebases-Contained-High-Ris                    https://arxiv.org/abs/2306.11644
     k-Open-Source-Vulnerabilities%2C-Surging-54-Since-Last-Year, 2024,           [52] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer,
     reports 84% of assessed codebases contained open-source vulnerabilities,          “QLoRA: Efficient finetuning of quantized LLMs,” arXiv preprint
     74% contained high-risk vulnerabilities, and 91% used components ten              arXiv:2305.14314, 2023. [Online]. Available: https://arxiv.org/abs/2305.1
     or more versions behind; accessed: 2026-05-28.                                    4314
[33] K. Gallaba, C. Macho, M. Pinzger, and S. McIntosh, “Noise and                [53] Y. Dong, C. F. Ruan, Y. Cai, R. Lai, Z. Xu, Y. Zhao, and T. Chen,
     heterogeneity in historical build data: An empirical study of Travis CI,”         “XGrammar: Flexible and efficient structured generation engine for large
     in Proceedings of the International Conference on Automated Software              language models,” arXiv preprint arXiv:2411.15100, 2024, mLSys 2025.
     Engineering (ASE), 2018, pp. 87–97, analyzed 3.7 million build jobs               [Online]. Available: https://arxiv.org/abs/2411.15100
     across 1,276 open-source projects.                                           [54] OpenAI, “Reasoning models,” https://platform.openai.com/docs/guides/
[34] K. Gallaba and S. McIntosh, “Use and misuse of continuous integration             reasoning, 2026, openAI API documentation; accessed: 2026-05-28.
     features: An empirical study of projects that (mis)use Travis CI,” IEEE      [55] ——, “Reasoning best practices,” https://platform.openai.com/docs/guide
     Transactions on Software Engineering, vol. 46, no. 1, pp. 33–50, 2020,            s/reasoning-best-practices, 2026, openAI API documentation; accessed:
     study of CI feature use and misuse across 9,312 open-source systems.              2026-05-28.
[35] OpenSSF, “OpenSSF Scorecard,” https://github.com/ossf/scorecard,             [56] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
     2026, accessed: 2026-05-14.                                                       and D. Zhou, “Chain-of-thought prompting elicits reasoning in large
[36] L. Simon, A. Birgisson, A. Ghodsi, T. Lauinger, B. Callaway, Z. Du-               language models,” arXiv preprint arXiv:2201.11903, 2022. [Online].
     rumeric, M. Hicks, D. Stefan, and S. Torres-Arias, “On the path toward            Available: https://arxiv.org/abs/2201.11903
     ecosystem-wide automated security metrics for open source software,”         [57] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang,
     in Proceedings of the 2022 ACM SIGSAC Conference on Computer and                  A. Chowdhery, and D. Zhou, “Self-consistency improves chain of
     Communications Security, 2022, pp. 1607–1620.                                     thought reasoning in language models,” arXiv preprint arXiv:2203.11171,
                                                                                       2022. [Online]. Available: https://arxiv.org/abs/2203.11171
[37] SPDX Project, “SPDX overview,” https://spdx.dev/about/overview/, 2026,
     open standard for communicating software bill-of-material information,       [58] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and
     provenance, license, and security metadata; accessed: 2026-05-28.                 Y. Cao, “ReAct: Synergizing reasoning and acting in language
                                                                                       models,” arXiv preprint arXiv:2210.03629, 2022. [Online]. Available:
[38] OWASP Foundation, “CycloneDX: Bill of materials standard,” https:
                                                                                       https://arxiv.org/abs/2210.03629
     //cyclonedx.org/, 2026, eCMA-424 bill-of-materials standard; accessed:
                                                                                  [59] J. Lin, X. Zeng, J. Zhu, S. Wang, J. Shun, J. Wu, and D. Zhou,
     2026-05-28.
                                                                                       “Plan and budget: Effective and efficient test-time scaling on
[39] OpenTelemetry, “Semantic conventions,” https://opentelemetry.io/docs/             reasoning large language models,” arXiv preprint arXiv:2505.16122,
     concepts/semantic-conventions/, 2026, accessed: 2026-05-28.                       2025, revised 2026; accepted to ICLR 2026. [Online]. Available:
[40] Open Policy Agent, “Open Policy Agent documentation,” https://ww                  https://arxiv.org/abs/2505.16122
     w.openpolicyagent.org/docs, 2026, general-purpose policy engine and          [60] OpenAI, “Structured model outputs,” https://platform.openai.com/docs/g
     Rego policy language; accessed: 2026-05-28.                                       uides/structured-outputs, 2026, openAI API documentation; accessed:
[41] OpenSSF, “SLSA: Supply-chain levels for software artifacts,” https:               2026-05-28.
     //slsa.dev/, 2024, accessed: 2026-05-14.                                     [61] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess,
[42] in-toto Project, “in-toto: A framework to secure the integrity of software        R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws
     supply chains,” https://in-toto.io/, 2026, accessed: 2026-05-14.                  for neural language models,” arXiv preprint arXiv:2001.08361, 2020.
[43] MIT OpenCourseWare, “Rice’s theorem,” https://ocw.mit.edu/course                  [Online]. Available: https://arxiv.org/abs/2001.08361
     s/6-045j-automata-computability-and-complexity-spring-2011/reso              [62] OpenAI, “Why SWE-bench Verified no longer measures frontier coding
     urces/mit6 045js11 lec09/, 2011, lecture notes for 6.045J Automata,               capabilities,” https://openai.com/index/why-we-no-longer-evaluate-swe
     Computability, and Complexity; accessed: 2026-05-28.                              -bench-verified/, 2026, accessed: 2026-05-28.
[44] K. Claessen and J. Hughes, “QuickCheck: A lightweight tool for random        [63] J. Yang, K. Lieret, C. E. Jimenez, A. Wettig, K. Khandpur, Y. Zhang,
     testing of Haskell programs,” in Proceedings of the ACM SIGPLAN                   B. Hui, O. Press, L. Schmidt, and D. Yang, “SWE-smith: Scaling
     International Conference on Functional Programming (ICFP), 2000, pp.              data for software engineering agents,” arXiv preprint arXiv:2504.21798,
     268–279.                                                                          2025. [Online]. Available: https://arxiv.org/abs/2504.21798
[45] X. Yang, Y. Chen, E. Eide, and J. Regehr, “Finding and understanding         [64] BigCode Collaboration, S. Hughes, H. de Vries, J. Robinson, C. M.
     bugs in C compilers,” in Proceedings of the ACM SIGPLAN Conference                Ferrandis, L. B. Allal, L. von Werra, J. Ding, S. Paquet, and Y. Jernite,
     on Programming Language Design and Implementation (PLDI), 2011,                   “The BigCode project governance card,” arXiv preprint arXiv:2312.03872,
     pp. 283–294.                                                                      2023. [Online]. Available: https://arxiv.org/abs/2312.03872
[65] Software Heritage, “Software heritage activity report: 2025,” https://ww
     w.softwareheritage.org/2026/01/16/software-heritage-activity-report-2
     025/, 2026, reports 2025 archive activity; accessed: 2026-05-28.
[66] A. Avizienis, “The N-Version approach to fault-tolerant software,” IEEE
     Transactions on Software Engineering, vol. SE-11, no. 12, pp. 1491–1501,
     1985.
[67] D. J. Mankowitz, A. Michi, A. Zhernov, M. Gelmi, M. Selvi,
     C. Paduraru, E. Leurent, S. Iqbal, J.-B. Lespiau, A. Ahern,
     T. Köppe, K. Millikin, S. Gaffney, S. Elster, J. Broshear, C. Gamble,
     K. Milan, R. Tung, M. Jiang, H. Wang, E. Özcan, D. Silver,
     D. Hassabis, P. Kohli, M. Riedmiller, O. Vinyals, and D. H.
     Silver, “Faster sorting algorithms discovered using deep reinforcement
     learning,” Nature, vol. 618, pp. 257–263, 2023. [Online]. Available:
     https://www.nature.com/articles/s41586-023-06004-9
[68] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar,
     E. Dupont, F. J. R. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, P. Kohli,
     and A. Fawzi, “Mathematical discoveries from program search with
     large language models,” Nature, vol. 625, pp. 468–475, 2024. [Online].
     Available: https://www.nature.com/articles/s41586-023-06924-6
[69] A. M. Turing, “On computable numbers, with an application to the
     Entscheidungsproblem,” Proceedings of the London Mathematical Society,
     vol. s2-42, no. 1, pp. 230–265, 1936.
[70] H. G. Rice, “Classes of recursively enumerable sets and their decision
     problems,” Transactions of the American Mathematical Society, vol. 74,
     no. 2, pp. 358–366, 1953.
[71] D. H. Wolpert and W. G. Macready, “No free lunch theorems for
     optimization,” IEEE Transactions on Evolutionary Computation, vol. 1,
     no. 1, pp. 67–82, 1997.
[72] M. Li and P. M. B. Vitányi, An Introduction to Kolmogorov Complexity
     and Its Applications, 3rd ed. Springer, 2008.
[73] G. M. Amdahl, “Validity of the single processor approach to achieving
     large scale computing capabilities,” in Proceedings of the AFIPS Spring
     Joint Computer Conference, 1967, pp. 483–485.
[74] P. D. Grünwald, The Minimum Description Length Principle. MIT
     Press, 2007.
