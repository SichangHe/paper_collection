                                         Proof-Carrying Certificates for LLM Pipelines:
                                                       A Trust-Boundary Architecture
                                                                          George Koomullil
                                                                              Ascendr, Inc.
                                                                          george@ascendr.ai
arXiv:2605.16407v1 [cs.LO] 13 May 2026




                                                                              May 19, 2026

                                                                                Abstract

                                         The framework verifies the deterministic structured computations surrounding a large
                                         language model rather than the model itself. Building on a patent-analysis hybrid AI
                                         + Lean 4 architecture [37] (henceforth the precursor), we extend the trust-boundary
                                         discipline from one specialized domain to the generic interfaces of modern LLM
                                         pipelines. The precursor’s architectural primitives are inherited unchanged: an explicit
                                         trust boundary separating a probabilistic ML layer from a deterministic Lean 4 layer,
                                         certificate validity defined as kernel type-check plus a sorry-free #print axioms
                                         audit against the trusted set Ω = {propext, Classical.choice, Quot.sound}, and
                                         a four-tier verification-status convention.
                                         The technical contribution divides into three local certificate families for generic LLM
                                         pipelines and two operators that combine them. The three families are conflict-aware
                                         bilattice grounding (with an emission-gate soundness lemma), embedding sensitivity
                                         and paraphrase stability, and Hoare-style agent action. The two operators are a Maximal
                                         Certifiable Residue, which turns abstention into the maximum-weight certifiable residue
                                         of an answer (with canonical lexicographic tie-breaking and audit-logged dropped
                                         claims), and a Compositional Stability theorem, which takes the per-layer gains and
                                         margins from the three families and produces a closed-form pipeline-wide perturbation
                                         budget. The three families and their consolidated per-call deliverable, the Universal
                                         Assurance Card (a Lean 4 record with a decidable consistency predicate, currently
                                         specified in Lean form rather than compiled in the artifact, with promotion to a compiled
                                         AssuranceCard.lean module flagged as a focused next-step engineering exercise),
                                         are intended as the per-call deliverable of any high-stakes deployment, including
                                         patent / technical-intelligence pipelines, legal case-law retrieval, regulated-finance
                                         disclosure analysis, clinical decision support, and agentic systems with irreversible
                                         side effects. A compiled Lean 4 reference artifact (Lean v4.30.0-rc2, Mathlib) covers
                                         all 22 certificate types of the framework, with 17 of 46 kernel-audited declarations
                                         axiom-free, the remaining 29 dependent only on Ω plus explicitly declared non-Ω
                                         assumptions partitioned by tier (mathematical placeholders, cryptographic assumptions,
                                         and ML/human oracles), and zero uses of sorryAx or Lean.ofReduceBool. All three
                                         certificate families are empirically tested through four registered pilots, with Pilot A’s
                                         v3/v4/v5 hypothesis revisions documented in §12.2 and Pilot C’s direct-injection design
                                         deviation documented in §8.5: grounding on HotpotQA in §12, embedding sensitivity
                                         in matched short-form and long-form settings in §7.4–§7.5, and Hoare-style agent action


                                                                                     1
      on a controlled filesystem sandbox in §8.5. The contribution is a paper-sized refinement
      of the precursor’s decomposition principle: at every interface where an LLM output
      becomes structured, the downstream computation can be made machine-checkable,
      and the resulting certificates compose into a per-call deliverable shipped in an explicit
      assurance mode.

Keywords: formal verification, dependent type theory, Lean 4, large language models,
retrieval-augmented generation, agent verification, proof certificates, proof-carrying code,
hallucination, prompt injection
How to read this paper. The paper has three audiences. A reader focused on the formal
contributions should read §3 (architecture), §§5–9 (the three certificate families and the
two operators), and §13 (compiled Lean 4 artifact). A reader focused on the empirical
claims should read §7.4–§7.5 (Pilots B and B′ ), §8.5 (Pilot C), and §12 (Pilot A); the
consolidated comparison is in §16.2. A reader focused on deployment should read §10
(Universal Assurance Card), §11 (case studies), §14 (threat model and adoption order), and
§16 (limitations and staged research program). Appendix A lists the mathematical symbols
used in the paper, and Appendix B expands the abbreviations.


1    Introduction

Modern LLM pipelines [8] produce point estimates without theorems. An embedding
similarity of 0.84 is mathematically precise yet materially meaningless if a paraphrase of the
same query yields 0.71 [10, 49]. A clinical decomposition can report “95% support” for a
recommendation while one of its atomic claims is contradicted by the very document that
grounded the rest [30, 42]. A chain of thought whose final step reads as confidently correct
may rest transitively on a step the model never actually used [39, 54]. An agent’s tool call
may be syntactically well-formed yet semantically unsafe [51, 62]. None of these failures is
an implementation bug. Each is the structural consequence of probabilistic pipelines whose
intermediate outputs carry no audit-grade guarantee.
The precursor paper [37] proposed an architectural answer in a single specialized domain
(patent analysis): identify the structured sub-computations between LLM outputs and
downstream decisions, draw an explicit trust boundary, and emit a Lean 4 certificate for
each interface. The present paper extends that decomposition to the generic interfaces of
modern LLM pipelines and gives a small, deployable per-call deliverable, the Universal
Assurance Card, that an LLM provider serving high-stakes deployments can ship with
each governed response under a declared assurance mode. The trust-boundary architecture,
certificate-validity definition, and verification-status convention are inherited unchanged; the
technical content develops what those primitives make possible at LLM-pipeline scale.
The thesis is the precursor’s decomposition principle restated for LLMs in general: the trust
boundary should be pushed as far toward the raw input as possible, with everything beyond
it made machine-checkable. Sections 2 and 3 make precise what is inherited and what is

                                                 2
new. A deployment-side corollary, sharpest for agentic systems, is that the LLM is the
proposer rather than the last writer to the world: it emits typed action proposals, and a small
kernel-audited runtime is the final authority that permits or blocks side effects (§8).


1.1   Two failures with a shared structure

Embedding sensitivity. A retrieval pipeline encodes a query 𝑥 as 𝐸 (𝑥) ∈ ℝ𝑑 , encodes a
corpus {𝑑𝑖 }, and returns the documents whose cosine similarity ranks in the top-𝑘. The
numerics are precise; nothing in them tells us whether 𝐸 (𝑥) is stable under semantically
equivalent rewordings of 𝑥. If a synonym substitution produces 𝐸 (𝑥 ′ ) at 𝐿 2 distance 0.35
from 𝐸 (𝑥) and the decision margin is 0.10, the top-𝑘 ranking has silently changed. How
sensitive is this embedding to small variations of the text? deserves a formal answer (§7).


Silent contradiction. A clinical decision-support tool decomposes a recommendation into
atomic claims and reports high evidential support for each. One claim, “the patient’s CrCl of
22 mL/min is within the drug’s renal range,” is directly contradicted by the FDA label the
system itself retrieved. A support-only score reports 𝑊ground = 95% and the recommendation
ships. The contradiction is invisible to any score that reports only support and never refutation.
Given evidence that speaks both for and against a claim, what should the pipeline report?
deserves a formal answer (§5).
These failures share a structural feature. The raw ML artifact (an embedding vector,
a generated answer) is not a natural object of formal verification. But each induces
structured objects on which deterministic theorems are provable: sensitivity envelopes over
finite declared perturbation families, per-claim signed-support maps over retrieved chunks,
reasoning directed acyclic graphs (DAGs) with explicit premise sets, typed action proposals
with preconditions. We verify these induced structured objects, not the raw outputs. The
LLM stays below a trust boundary; every interface where its output becomes structured is
replaced by a kernel-audited certificate.


1.2   What “formal verification” means here

We distinguish two senses throughout. Semantic verification would assert correctness against
external reality (“this brief is legally sound,” “this diagnosis is correct”); it requires a
formalization of the world and we do not attempt it. Computational verification asserts that a
stated specification holds of an output given the pipeline’s inputs (“the weighted coverage of
this claim graph is exactly 82.3%”; “the weighted Contradicted-plus-Contested mass
of this claim graph is at most 𝜃 𝑟 ”); it is the target of every certificate in this paper. The
conditionality on ML-produced inputs is not a defect, it is the only honest characterization of
any system that processes natural language. The improvement is structural: the conditionality
is named, machine-auditable, and rejectable, rather than buried inside an opaque confidence
score.


                                                3
1.3   Contributions

The paper makes eight technical contributions, each strictly beyond the precursor:

 1. Three local certificate families for LLM pipelines. Conflict-aware bilattice grounding
    (§5) with the Emission Gate Soundness Lemma (Lemma 5.4; conditional on the NLI
    / decomposition oracles): a Belnap-style four-valued classification of atomic claims;
    the gate provably blocks emission whenever the weighted-refutation mass exceeds
    threshold, addressing a failure mode that support-only RAG pipelines structurally
    cannot detect. Embedding sensitivity and paraphrase stability (§7): a squared-form
                                                            2 and certifies 𝐿 -drift envelopes
    robust-similarity bound (Theorem 7.4) that uses only 𝑅inv                2
    on the meaning-invariant family, paired with a separate decidable selective-sensitivity
    predicate Δ2 = 𝑅sig2 − 𝑅 2 > 0 over the same certificate that the policy layer enforces
                             inv
    (the certificate carries Δ2 as a per-query measurement, deployment-readiness signal
    in the Universal Card). Hoare-style agent action (§8): per-step preconditions and
    postconditions discharged by the Lean kernel, chained into a trajectory certificate that
    carries no axioms at all in the compiled artifact. Each family is given as a compiled
    Lean 4 structure with decidable proof fields and an explicit list of named non-Ω
    assumptions partitioned by tier (only tier-4 are persistent ML/human oracles), and each
    is empirically tested in this paper (grounding via Pilot A; embedding sensitivity via
    Pilots B and B′ ; Hoare action via Pilot C; see contributions 6–8 below).
 2. Two operators on certificates that turn the local catalogue into a pipeline-level
    guarantee. Maximal Certifiable Residue (Theorem 6.3, §6): a formal abstention
    operator returning the maximum-weight certifiable subset of an answer (with canonical
    lexicographic tie-breaking), proved weight-optimal, idempotent, and monotone in
    constraints; the operator that pairs with the bilattice grounding certificate to convert
    a flagged contradiction into a residue that ships the certifiable claims and audit-
    logs the dropped ones. Compositional Stability (Theorem 9.3, §9, with two-layer
    base case Lemma 9.2 compiled and the 𝑛-layer lift specified by structural induction
    over a List.foldl of certified layers): a closed-form pipeline-wide budget 𝐵Π =
              Î
    min𝑖 𝑚 𝑖 / 𝑗<𝑖 𝑔 𝑗 that takes the per-layer gains 𝑔 𝑗 and margins 𝑚 𝑖 supplied by the three
    certificate families above and produces a single inequality bounding what survives at
    the pipeline’s final output.
 3. The Universal Assurance Card (§10): a Lean 4 record (specified, with a decidable
    consistency predicate VerdictConsistent) carrying one of four verdicts (Certified,
    Partial, Residue, Abstain) plus a vector of stability, evidence, calibration, scope, fresh-
    ness, safety, residue, and provenance fields. A separately-published AssurancePolicy
    maps the same card to accept/reject/downgrade for any deployment context. We exhibit
    two filled-out cards from the case studies (§11); promoting AssuranceCard.lean
    from specified to compiled is a focused engineering step (Mathlib-light, decidable-only)
    flagged in §16.



                                              4
4. Compiled reference artifact covering all 22 certificate types of the broader cat-
   alogue. Of 46 kernel-audited declarations, 17 depend on no axioms at all and
   29 depend only on Ω plus explicitly declared non-Ω assumptions partitioned
   into tier-2 mathematical placeholders, tier-3 cryptographic assumptions, and tier-
   4 ML/human oracles. Zero uses of sorryAx or Lean.ofReduceBool. We give
   a representative axiom audit (§13, Appendix D; the build-emitted full audit is in
   EmbeddingSensitivity/AxiomAudit.lean) and split the named axioms into a four-
   tier assumption hierarchy (kernel, mathematical placeholder, cryptographic, ML/human
   oracle), of which only tier 4 is structurally conditional.
5. An impossibility conjecture extending the precursor’s three impossibility propo-
   sitions. A new Calibration Impossibility without Ground Truth (Conjecture 4.4): no
   system that emits a confidence score without exogenous labeled data can prove its score
   calibrated. We state this as a conjecture rather than a theorem because it requires a
   careful Vovk-style exchangeability framing we have not yet formalized; the architectural
   consequence (calibration must be grounded in exchangeable held-out data) motivates
   the conformal / scope-of-validity discipline regardless of formal status (§4).
6. Pilot A: the conflict-aware grounding certificate works on a public benchmark.
   The v5 frozen-protocol rerun on HotpotQA dev distractor with adversarial perturbations
   (§12; the v3/v4/v5 evolution and what was rewritten is documented there) shows
   the certificate catches 100% of injected contradictions at a false-block rate of 6.4%,
   an operating point the cosine-similarity baseline cannot reach: B1’s lowest FBR at
   catch=1.0 is 0.266 at 𝜃 𝐵1 = 0.90. All six v5-registered hypotheses pass.
7. Pilots B and B′ : the embedding-sensitivity certificate is sound everywhere, but
   its premise is input-length-dependent. A matched two-domain study on HotpotQA
   (§7.4, §7.5) finds the certificate’s central inequality Δ2 > 0 holds in only 20–30%
   of short adversarial queries but in 98–100% of long-form paragraphs across every
   edit-type combination. The certificate is therefore deployment-supported on the long-
   form HotpotQA slice and a candidate for clinical, legal, and technical long-form
   retrieval pending domain-specific replication, while remaining scope-narrowed for
   short adversarial queries; this is the kind of empirical scoping result the framework’s
   “soundness machinery + per-call premise” posture is designed to surface.
8. Pilot C: the Hoare-style agent-action certificate dominates a deny-list baseline on
   injected unsafe actions, and its FAIL on the strictest hypothesis surfaces a localizing
   diagnostic of exactly the kind a typed-guarantee pilot is designed to deliver. A
   pre-registered controlled-sandbox benchmark (§8.5) shows the Lean-checked Treatment
   harness blocks 67% of injected unsafe actions versus 28% for a regex deny-list and 0%
   unaudited, a 38.9-point dominance over the deny-list baseline, with zero false blocks
   on benign destructive proposals and 100% audit-log informativeness on every block.
   Four of five hypotheses pass; on the fifth (HC1, the strictest 95% block-rate threshold),
   the audit log of unblocked attacks names exactly which predicate clauses need to be
   extended to close the gap. This is the empirical signal the framework is designed to

                                            5
     produce: typed guarantees that fail predict their own remediation, rather than degrading
     to opaque false-negatives.


Roadmap. The rest of the paper develops these in order. §2 states what is inherited from
the precursor and what is new; §3 recaps the trust-boundary architecture and the per-oracle
audit procedure; §4 positions the framework against three impossibility propositions and the
calibration conjecture. The three local certificate families are §5 (conflict-aware bilattice
grounding), §7 (embedding sensitivity, with Pilots B and B′ ), and §8 (Hoare-style agent action,
with Pilot C). The two operators are §6 (maximal certifiable residue, the abstention operator
that pairs with grounding) and §9 (compositional stability, the pipeline-level composition
theorem that takes the three local certificates as inputs and produces a closed-form end-to-end
perturbation budget). §10 introduces the Universal Assurance Card; §11 works two filled-out
cards on case studies; §12 reports Pilot A on the grounding certificate. §13 is the compiled
Lean 4 reference artifact. §14 maps threats to defender certificates; §15 sketches the extended
catalogue; §16 states limitations and the staged research program; the conclusion follows.


Artifact at a glance


      Compiled Lean 4 reference artifact (lean_artifact/, Lean v4.30.0-rc2 + Mathlib)

     • 22 certificate types compiled across 25 modules.
     • 46 kernel-audited declarations: 17 axiom-free; remaining 29 use only Ω plus explicitly
       declared non-Ω assumptions, partitioned into tier-2 mathematical placeholders, tier-3
       cryptographic assumptions, and tier-4 ML/human oracles.
     • Zero sorry; zero native_decide; zero Lean.ofReduceBool anywhere in the transi-
       tive axiom set.
     • Build: ≈ 10 s on commodity hardware with warm Mathlib cache (lake build).
     • Audit wrapper: < 100 LOC of Python or Rust around lean and #print axioms.
     • Persistent oracles (tier-4, conditional on natural-language correctness): ex-
       actly five (ParaphraseOracle, SignedSupportOracle, DecompositionOracle,
       StepConfidenceOracle, IIDSamples); see Table 2.
   This is operational, not aspirational. A representative axiom audit is in Appendix D; the full
   #print axioms output is regenerated by EmbeddingSensitivity/AxiomAudit.lean on
   every build, and per-cert evaluation numbers are in Table 5. The Universal Assurance Card
   is a consolidator of the 22 certificate types (not a 23rd type); its schema (§10) is currently
   specified in Lean form, and adding AssuranceCard.lean to the artifact as one additional
   consolidator module is a focused engineering step (§16.4).




                                                 6
1.4   Scope and limitations

The trust boundary is structural: the LLM sits below it, and every certificate is conditional on
named non-Ω assumptions partitioned by tier (only tier-4 are persistent ML/human oracles);
their correctness is the condition under which the guarantee holds. The framework makes
that dependency auditable rather than eliminating it. The grounding certificate catches
hallucinations that the evidence contradicts and the self-consistency certificate catches
sample-unstable hallucinations; hallucinations that are stable across samples and aligned
with a corrupted retrieval corpus are outside the framework’s reach.
The empirical scope of the paper is the four pre-registered pilots (each reported under its
v5 frozen-protocol rerun; the v3/v4/v5 evolution is documented in §12.2): Pilot A (§12)
on the conflict-aware grounding certificate on HotpotQA dev distractor with adversarial
perturbations, in which all six v5-registered hypotheses pass; Pilots B and B′ (§7.4, §7.5)
on the embedding-sensitivity certificate in matched short-form and long-form settings, in
which the central inequality Δ2 > 0 holds in 20–30% of cases on adversarial short queries
but in 98–100% of cases on long-form paragraphs across every edit-type combination; and
Pilot C (§8.5) on the Hoare-style agent-action certificate, in which the Treatment harness
blocks 67% of injected unsafe actions versus 28% for a deny-list baseline (HC3 PASS) with
100% audit-log informativeness on every block. Each certificate’s Lean-checked soundness
is unaffected; deployment-readiness depends on the input class and on the completeness of
the declared predicate / family set, which the deployer must measure on the target corpus
before relying on the certificate.
The pilots cover HotpotQA dev distractor and a controlled filesystem sandbox; replication on
patent / technical-intelligence, legal, regulated-finance, clinical, or other high-stakes corpora
is forward work. §16.8 outlines a Pilot D family of Universal Card validations across these
domains, any one of which is an independent next-step empirical contribution. The two
case studies in §11 use illustrative numerical values rather than measured ones; they are
intended to exhibit Card behavior, not to make empirical claims. The framework is designed
for deployments in which per-call error cost exceeds per-call verification cost by roughly an
order of magnitude (patent / technical-intelligence pipelines, legal retrieval, clinical decision
support, regulated finance, agentic systems with irreversible side effects) and is not intended
for creative writing or open-ended generation.


2     Relation to the Precursor and Related Work

2.1   Inherited from the precursor

The precursor [37] introduced a hybrid ML + Lean 4 pipeline for patent analysis. From it we
inherit, without re-derivation, the following architectural primitives:

 • Trust-boundary architecture. Raw inputs flow into an ML/NLP layer below a trust


                                               7
      boundary; the formal layer (Lean 4) consumes ML outputs as typed inputs and emits a
      certificate whose validity is independent of model weights, prompts, or random seeds.
      The boundary is not metaphorical; it is encoded as Lean type parameters and named
      axioms.
 • Certificate validity = kernel type-check + sorry-free Ω-audit. A certificate 𝑐 is valid
   iff 𝑐 type-checks at its declared type and #print axioms reports a transitive set
   ⊆ Ω = {propext, Classical.choice, Quot.sound} plus declared named oracles.
   The two-step check rejects the naïve sorry-generator counter-example that motivated the
   precursor’s audit discipline.
 • Verification-status convention. Every formal claim carries one of four statuses, compiled
   (in the artifact, kernel-checked, Ω-audited modulo declared oracles), specified (rigorous
   obligation, not yet compiled), architecturally enforced (encoded in a type signature), or
   conjectural (informal). We use the same convention here, badged at every theorem and
   definition.
 • Conditional-guarantee discipline. Every certificate’s guarantee is conditional on named
   non-Ω assumptions partitioned by tier (only tier-4 are persistent ML/human oracles); the
   conditionality is auditable by inspecting axioms rather than re-running the pipeline.
 • Three structural impossibility results. Certificate impossibility for stochastic samplers
   (Prop. 4.1); compositional unsoundness of marginal flat scoring (Prop. 4.2); stochastic
   non-reproducibility (Prop. 4.3). We restate them in LLM-pipeline form in §4 and add a
   fourth, stated more cautiously as Conjecture 4.4.

We do not re-derive these here. Readers seeking the constructive justification (the naïve
sorry generator counter-example, the kernel-vs-prover distinction, the de Bruijn criterion)
are referred to [37].


2.2     What is new in this paper

The contribution of the present paper is to drop the patent-domain assumption. Generic
LLM pipelines expose structured interfaces (embeddings, retrieval, reasoning DAGs, typed
outputs, agent actions) that are ubiquitous but not pre-formalized. We give:

 • Three local certificate families for those interfaces (bilattice grounding, embedding
   sensitivity, Hoare-style agent action) plus two operators (Maximal Certifiable Residue,
   Compositional Stability), none of which has an analogue in the precursor.
 • A compiled Lean 4 reference artifact spanning 22 certificate types (the precursor compiled
   one closed path).
 • A per-call deliverable, the Universal Assurance Card, with a decidable consistency
   predicate and a separately-published application-policy layer; the precursor had no
   analogue.

                                             8
 • One additional impossibility result (calibration without ground truth) and case-study
   walkthroughs in clinical RAG and agentic Hoare execution.


2.3   Adjacent literatures

Interactive theorem proving and proof-carrying code. Lean 4 [17], Mathlib [53], the
self-verified kernel [9], and PCC [16, 44] provide the trusted-checking infrastructure. AWS
Cedar [15] is an industrial Lean adoption; refinement-type ecosystems [50, 52, 55] provide
an SMT-backed compilation target for routine certificate fields. None offer a certificate
taxonomy for LLM-pipeline interfaces.


Neural-network verification. Abstract interpretation [13, 23], randomized smoothing [11],
Lipschitz analysis [56], and NLP-specific bounded-substitution certificates [10, 31] verify
the model. Our certificates are downstream and orthogonal: they consume the model’s
output as-is and certify the structured computation on top. A smoothed encoder feeds a
certified retrieval stack without conflict; §7’s sensitivity certificate is designed to compose
with smoothing certificates as drop-in sensitivity witnesses.


LLM reliability and RAG. Hallucination surveys [29, 30], factuality detectors [5, 42, 43],
RAG [22, 35, 40], chain-of-thought [59, 60], process-reward models [41], and prompt-
injection studies [25, 47, 63] identify failure modes empirically. We convert each into a
certificate type: grounding becomes a bilattice coverage theorem (§5), self-consistency
becomes a canonicalized lattice (extended catalogue, §15), prompt injection becomes a non-
interference theorem (catalogue), paraphrase metamorphic testing becomes a decision-margin
certificate (§7).


Probabilistic-program verification and conformal prediction. Kozen [38], pRHL [3],
weakest-pre-expectations [34], conformal prediction [2, 48, 57], and concentration-of-
measure theory [6, 28] populate the catalogue’s calibration and concentration certificates.
The closest existing compositional results are NN Lipschitz composition [56] and the
precursor’s weight-independent robustness; Theorem 9.3 unifies them by allowing each layer
to be either Lipschitz-continuous or a discrete gate.




                                              9
Table 1: Position relative to four adjacent literatures. ITP/PCC, NNV, LLM-reliability, and
probabilistic-program verification each address one side; this paper supplies the certificate
architecture for the deterministic sub-computations between LLM outputs and downstream
decisions.

    Literature                Contribution                   Stops at                      Added here
    ITP / PCC             Machine-checkable proofs;          No LLM-interface tax- Three certificate families + composi-
                          minimal kernel                     onomy                 tion theorem + 22-type artifact
    NN verification       Input–output properties of         Model boundary        Composable downstream certificates
                          models
    LLM reliability       Empirical detection / mitiga-      Probabilistic only    Each lifted to kernel-checked certifi-
                          tion                                                     cate
    Probabilistic-program Relational Hoare, conformal,       No LLM-pipeline inte- Per-layer in hybrid architecture
    verification          concentration                      gration




3       Architecture

This section tightens the trust-boundary architecture for LLM pipelines. The architectural
primitives are inherited from [37]; we do not re-derive them. We state only what changes
when the domain widens from patent claims to generic LLM interfaces.


3.1       Trust boundary

                                                     TRUST BOUNDARY



         Raw inputs                   ML/NLP layer                 Formal verification              Output + Universal Card
      prompt, corpus, tools          LLM, embedder, NLI                 Lean 4 + Ω-audit


                                  probabilistic, untrusted        deterministic, audited


Figure 1: The hybrid architecture, inherited from [37]. The ML/NLP layer produces typed
artifacts below a trust boundary; the formal layer re-consumes them as typed inputs and
emits the Universal Assurance Card and underlying certificates. Conditional on the declared
non-Ω assumptions (tiers 2–4 of the assumption hierarchy, §3.4), each certificate carries a
kernel-audited guarantee.


Definition 3.1 (Valid LLM Certificate [37]). [ compiled ] A certificate 𝑐 is valid iff
(i) 𝑐 type-checks in the Lean 4 kernel at its declared type, and (ii) 𝑐’s transitive
axiom set, as reported by #print axioms, is contained in Ω ∪ Ax where Ω =
{propext, Classical.choice, Quot.sound} and Ax is the certificate’s declared set of
named non-Ω axioms, partitioned into tier-2 mathematical placeholders, tier-3 cryptographic
assumptions, and tier-4 ML/human oracles (the four-tier hierarchy of §3.4). Clause (ii) is the



                                                             10
sorry-free Ω-audit: it rejects certificates whose proof fields are discharged by Lean’s sorry
(an axiom inhabiting any type) and certificates that exceed their declared non-Ω axiom set.

The motivating naïve-sorry counter-example and the kernel-vs-prover separation are in [37];
we omit them here.


3.2   Where LLM pipelines differ from patents

What changes when the domain widens. (1) The ML layer’s outputs are no longer pre-
formalized DAGs; they are induced by decomposition oracles (§5) and paraphrase oracles
(§7) that the framework names explicitly and audits as tier-4 axioms. (2) The relevant
interfaces span four families (input, aggregation, inference, output) rather than the single
DAG-coverage path of [37]; see Table 3 for the consolidated map. (3) The certificate must
travel with each governed response under a declared assurance mode, not just sit alongside
a one-off analysis report; we therefore introduce the Universal Assurance Card (§10). (4)
The auditor base widens from patent practitioners to providers, regulators, and downstream
applications; the assumption hierarchy (§3.4) is now the load-bearing communication artifact,
brought forward to immediately follow the trust-boundary statement.


3.3   Attested interface and audit protocol

Every certificate carries a deterministic coercion from ML output to Lean input, a crypto-
graphic digest of the ML artifact, and a declared set of named oracle axioms.
Lean 4: illustrative sketch, attested interface; declared in every certificate module

  structure AttestedInterface (MLOut LeanIn : Type) where
   coerce : MLOut -> LeanIn         -- deterministic
   digest : MLOut -> ByteArray      -- SHA-256
   declared_axioms : List String    -- named non-$\Omega$ axioms (tiers 2-4)



Audit protocol. An auditor receiving a certificate 𝑐 (i) parses 𝑐 and extracts the oracle digest
and (optional) ML artifact; (ii) optionally recomputes the digest and compares; (iii) runs the
Lean 4 kernel on 𝑐 at its declared type; (iv) runs #print axioms transitively and aborts
if the axiom set ⊈ Ω ∪ Ax; (v) confirms the response output matches the certificate’s. No
model weights, prompt templates, decoding parameters, or random seeds are needed. The
audit is reproducible on any machine with Lean 4 and a SHA-256 implementation. For
realistic workloads (𝑑 = 103 , family size 50, 20 atomic claims, 100 retrieved chunks, 20-step
CoT) a kernel re-check completes in sub-second wall-clock; certificate storage is KB–MB
per call.




                                              11
3.4   Assumption hierarchy

The named axioms that appear in any LLM-pipeline certificate split into four tiers, in
decreasing order of trust the auditor can place in them:

1. Kernel axioms (Ω = {propext, Classical.choice, Quot.sound}). Lean 4’s foun-
   dational axioms; trusted by Mathlib and externally validated by Lean4Lean [9].
2. Mathematical placeholders (e.g., cauchy_schwarz_sq, innerProd_sub,
   HoeffdingInequality).          Theorems of standard mathematics whose Mathlib
   formalization is in progress or differently shaped; each reduces to Ω once aligned.
3. Cryptographic assumptions (e.g., HashCollisionResistant, DecodeAlgorithm
   Deterministic). Standard hardness or determinism assumptions; reduce to Ω when a
   SHA-256 (or substitute) formalization is plugged in.
4. ML / human oracles (e.g., ParaphraseOracle, SignedSupportOracle,
   DecompositionOracle, StepConfidenceOracle). These encode the correct-
   ness of a learned natural-language judgment or a domain expert’s sign-off and cannot be
   discharged by mathematics or cryptography.

Why this matters operationally. Tier 1 is the kernel-trusted base Ω itself; tiers 2 and 3 are
closable as Mathlib and the cryptographic-formalization community evolve, each named
axiom collapsing into an Ω-only proof once the corresponding library catches up. The
long-term trusted base of the structural content is therefore just Ω. Tier 4 is persistent: closing
it would require formalizing natural-language correctness, which the architecture deliberately
does not attempt. A reviewer or regulator can therefore audit a deployment by enumerating
tier-4 oracles and asking, for each, what evaluation evidence supports it and whether the
deployment’s scope-of-validity certificates (§15) cover the input distribution. This is the
operational meaning of “conditional guarantee.” One subtlety on the axiom-free certificates
in the artifact (the Hoare action family in particular): axiom-freeness is a statement about
the proof’s discharge mechanism, not about the semantic adequacy of the human-authored
predicates the proof discharges; a precise account of what axiom-freeness does and does not
guarantee is given in §13.1.


3.5   Per-oracle audit procedure

The persistent tier-4 oracles in the artifact are exactly five. Table 2 converts the philosophical
point into a deployment procedure: for each oracle, what it asserts, what evaluation artifact
supports it, what scope predicate gates it, and how often it must be re-evaluated. The
procedure is what a regulator or procurement reviewer should require alongside any Universal
Card.




                                                12
Table 2: Audit procedure for the five persistent (tier-4) ML/human oracles in the compiled
artifact. Each row gives a deployment-ready discipline: assertion, evaluation evidence the
deployment must maintain, scope predicate that gates the certificate’s acceptance of the
oracle, and a re-evaluation cadence. The table is intended to be cited in audit checklists,
contracts, and procurement documents.

Oracle             Asserts                       Evaluation evidence            Scope predicate       Re-eval cadence
ParaphraseOracle   The declared families         Held-out paraphrase bench-     input domain matches quarterly + on
                   𝐺inv , 𝐺sig are meaning-      mark with expert equiv-        paraphraser’s training paraphraser swap
                   preserving / meaning-         alence labels; agreement       distribution; edit oper-
                   changing for the input text   against a human gold set       ations within declared
                                                                                grammar
SignedSupport      Three-way NLI gives cor- Held-out NLI calibration            retrieved       corpus monthly + on
Oracle             rect ( 𝜎 + , 𝜎 − , 𝜎 0 ) for ev- set on domain corpus;       within      calibrated corpus or NLI-
                   ery (claim, chunk) pair          agreement with expert NLI   domain       ontology; model swap
                                                    annotation                  chunk lengths within
                                         Ó                                      trained range
Decomposition      The decomposition 𝑖 𝑐𝑖 Reconstruction-pass rate              answer length ≤ de- per model release
Oracle             canonicalizes to the answer on a held-out decompo-           clared bound; vocabu- + on canonical-
                   𝑦                           sition set; canonicalizer        lary in domain ontol- izer change
                                               round-trip equality              ogy
StepConfidence     Per-step confidence 𝑐𝑖 is PRM-validated confidence           chain length ≤ de- per model release
Oracle             a sound lower bound on on held-out chains; agree-            clared bound; rea- + on PRM update
                   Pr(step correct)            ment with human step grad-       soning style within
                                               ing [41]                         trained distribution
IIDSamples         The 𝑘-sample sequence is Proof-of-sampling com-              𝑇 > 0; no in-context continuous (per-
                   IID under the declared sam- mitment + decoder-state-         state carryover across call)
                   pling discipline            isolation log; bounded-          samples
                                               difference      martingale
                                               fallback for non-IID cases



A deployment that ships a Universal Card without the corresponding evaluation evidence for
every tier-4 oracle it depends on is not auditable in the framework’s sense, even if its Lean
kernel checks pass. The procedure is therefore necessary, not optional, and is the natural
target for procurement-level standardization.




                                                       13
3.6     Overview of main results

Table 3: Overview of the paper’s main results: three local certificate families, two operators
on certificates, and one consolidator (the Universal Card). Each row’s status is: compiled
(in the artifact, kernel-checked plus Ω-audited) or specified (rigorous obligation, not yet
compiled). All other certificate types appear in the extended catalogue (§15, Appendix C).

Item (§)                         What it guarantees                      Status            Declared non-Ω assumptions
Three local certificate families
Conflict-aware grounding (§5; Emission gate soundness: emitted           compiled          SignedSupportOracle,
Lem 5.4)                         only when refutation mass ≤ 𝜃𝑟 ;                          DecompositionOracle
                                 four-valued claim status
Embedding sensitivity (§7; Robust similarity bound from                  compiled          ParaphraseOracle                    (t4);
Thm 7.4)                           2 over 𝐺 ; selective-sensitivity
                                 𝑅inv                                                      cauchy_schwarz_sq,
                                              inv
                                 (Δ2 > 0) is a decidable predicate                         innerProd_sub (t2)
                                 on the certificate read by the policy
                                 layer
Hoare agent action (§8)          Pre/post discharged per step; trajec-   compiled          (none)
                                 tory chained                            (axiom-free)
Two operators on certificates
Maximal Certifiable Residue  Largest constraint-satisfying subset        compiled          (none beyond constraint families)
(§6; Thm 6.3)                of an answer; abstention with audit-
                             logged drops
Compositional Stability (§9; Pipeline-wide perturbation budget           lemma     com- (none beyond per-layer certs)
Lem 9.2 compiled; Thm 9.3 𝐵Π from per-layer chain of gains               piled;    𝑛-lift
specified)                   and margins                                 specified
Per-call deliverable
Universal Assurance Card (§10) Verdict consistent with field vector      specified (decid- inherited from sub-certificates
                                                                         able predicate;
                                                                         AssuranceCard.lean
                                                                         flagged for the
                                                                         artifact)
Compiled artifact totals (§13)
22 cert types, 46 declarations   17 axiom-free; 29 with Ω + tier-2/3/4   compiled          per-cert non-Ω set
                                 named axioms; 0 sorry



A reader looking for “which threats does each certificate defend against, and what is the first
one to ship?” should jump to §14 (Threat model and adoption order; Table 7 maps threats to
defender certificates row-by-row).


4 Three Impossibility Propositions and a Calibration Conjecture

Three of these are inherited (in LLM-pipeline form) from [37]; the calibration impossibility,
stated below as a conjecture rather than a proposition because a careful Vovk-style proof is
left for future work, is new to this paper. We state the inherited results in compact form; full
motivation is in the precursor.



                                                            14
Formalism. 𝑆 denotes a (possibly stochastic) system with input space X, output space Y,
output rule 𝑦 ∼ D𝑆 (𝑥). 𝐻 denotes Shannon entropy, 𝐻2 Rényi-2 entropy. A deterministic
validator 𝑉 : Y → {0, 1} is computable without consulting randomness.
Proposition 4.1 (Certificate Impossibility for Stochastic Samplers). [ specified ] If
Pr𝑐∼D𝑆 ( 𝑥0 ) [𝑐 ∉ Ω★] > 0 for any 𝑥 0 , where Ω★ = {𝑐 : 𝑉 (𝑐) = 1}, then 𝑆 cannot un-
conditionally guarantee that its output is a valid certificate. Architectural consequence:
a deterministic post-sampler validator is necessary; the hybrid Lean-kernel-plus-Ω-audit
(Def. 3.1) is that validator.
Proposition 4.2 (Compositional Unsoundness of Marginal Flat Scoring). [ specified ] For any
aggregation 𝐹 : [0, 1] 𝑛 → [0, 1] symmetric in marginals and any non-degenerate marginal
vector, the Fréchet–Hoeffding bounds give two joints with the same marginals but distinct
conjunction probabilities, so no marginal-only 𝐹 can equal the conjunction probability
without an exogenous independence assumption. The DAG-conditional analogue (every
flat 𝐹 disagrees with the all-elements rule on some configuration) compiles as a finite-case
enumeration. Architectural consequence: dependency structure must be carried explicitly
(DAGs, lattices, signed support), not collapsed into a single scalar.
Proposition 4.3 (Stochastic Decoding is not Unconditionally Reproducible). [ specified ] For
                                                                                  Í
finite output alphabet Y with distribution 𝜇, Pr[ 𝑓 (𝑥, 𝜔1 ) ≠ 𝑓 (𝑥, 𝜔2 )] = 1 − 𝑦 𝜇(𝑦 | 𝑥) 2 ≥
1 − 2−𝐻2 ( 𝜇 | 𝑥 ) . At 𝐻2 ≈ 3 bits (typical for token distributions at 𝑇 = 1), the disagreement
probability already exceeds 87.5%. Architectural consequence: the Lean kernel produces
the same certificate on the same inputs with probability 1, unconditionally; the formal layer
is the deterministic anchor.
Conjecture 4.4 (Calibration Impossibility without Ground Truth). [ conjectural ] Let 𝑆 emit
a confidence score 𝑐(𝑥) ∈ [0, 1] without access to the true conditional 𝑃(𝑦 | 𝑥) and without
exogenous labeled data. Then 𝑆 cannot prove 𝑐 calibrated, that is, Pr ( 𝑥,𝑦)∼𝑃 [𝑦 = correct |
𝑐(𝑥) ∈ 𝐵] = 𝔼 ( 𝑥,𝑦)∼𝑃 [𝑐(𝑥) | 𝑐(𝑥) ∈ 𝐵], without an external distributional hypothesis.

Informal argument. Calibration is a property of 𝑃 restricted to a level set of 𝑐. Without
access to 𝑃 and without labels, 𝑆 observes only its own outputs and cannot recover
Pr[𝑦 = correct | 𝑐(𝑥) ∈ 𝐵], so any guarantee must rest on an external hypothesis about
𝑃 (exchangeability with a calibration set, bounded shift, or parametric form), which is
precisely what conformal methods axiomatize [57]. The conjecture is stated rather than
proved because a rigorous treatment requires a Vovk-style distribution-free formalization that
we have not yet completed; the formal anchor we would build on is the conformal-prediction
validity argument of Vovk, Gammerman, and Shafer [57], in which a marginal coverage
guarantee is recovered only under exchangeability between calibration and test data, and the
missing step here is the explicit construction of the exchangeability filtration over the (input,
score, outcome) sequence and the proof that no measurable functional of the score-only
sub-filtration recovers the conditional. The architectural consequence is independent of
formalization status: calibration hypotheses must be sourced exogenously and named as
scope-of-validity oracles or conformal-exchangeability axioms.

                                               15
Together, Propositions 4.1–4.3 and Conjecture 4.4 fix the architectural shape: (i) a deter-
ministic component issues guarantees; (ii) compositional steps carry explicit dependency;
(iii) reproducibility is engineered into the issuing layer; (iv) calibration is grounded in
exchangeable held-out data. Every certificate in this paper is the deterministic validator 𝑉 for
some specific property; the kernel plus Ω-audit is the universal discharge mechanism.


5     Conflict-Aware Bilattice Grounding

This is the most substantive technical departure from the precursor’s coverage machinery.
Real RAG [22, 40] evidence does not merely support a claim or not; it can also contradict
it. A claim well-supported by one chunk and explicitly contradicted by another is not an
acceptable output, even at 𝑊 + = 95%. We therefore depart from single-polarity scoring and
formalize grounding over a Belnap-style bilattice [4, 24].


5.1   Decomposition with reconstruction completeness

The LLM’s answer 𝑦 is decomposed (by a second LLM call) into atomic claims {𝑐 1 , . . . , 𝑐 𝑛 }
with weights 𝑤 𝑖 ∈ ℚ+ . We adopt the FActScore-style atomic-fact decomposition discipline
of [43] as the upstream methodology. A dishonest decomposer could omit a load-bearing
claim (the one that would have been contradicted); we block this with a reconstruction check.
Definition 5.1 (Verification-by-Reconstruction). [ specified ] The decomposition {𝑐 𝑖 } is
                                                    Ó
complete for 𝑦 if a canonicalizer 𝐶 satisfies 𝐶 ( 𝑖 𝑐 𝑖 ) = 𝐶 (𝑦). The grounding certificate
carries this equality as a proof field. Failure of the check rejects the decomposition.

The semantic faithfulness of the reconstruction is the named oracle DecompositionOracle
(tier 4); the canonicalizer equality check is decidable.


5.2   Three-way signed support

For each atomic claim 𝑐 𝑖 and each retrieved chunk 𝑟 𝑗 , a three-way NLI signature is computed:
                𝜎(𝑐 𝑖 , 𝑟 𝑗 ) = (𝜎𝑖+𝑗 , 𝜎𝑖−𝑗 , 𝜎𝑖0𝑗 ) ∈ [0, 1] 3 ,   𝜎𝑖+𝑗 + 𝜎𝑖−𝑗 + 𝜎𝑖0𝑗 = 1,

where 𝜎 + , 𝜎 − , 𝜎 0 are entailment, contradiction, and orthogonality respectively (standard
NLI [7]). The best-support and best-refutation scores are 𝛽𝑖+ = max 𝑗 𝜎𝑖+𝑗 and 𝛽𝑖− = max 𝑗 𝜎𝑖−𝑗 .
Definition 5.2 (Claim Epistemic Status). [ compiled ] With thresholds 𝜃 𝑔 , 𝜃 𝑐 ∈ (0, 1]:
                                    
                                    
                                    
                                     Supported                  𝛽𝑖+ ≥ 𝜃 𝑔 ∧ 𝛽𝑖− < 𝜃 𝑐
                                                                 𝛽𝑖+ < 𝜃 𝑔 ∧ 𝛽𝑖− ≥ 𝜃 𝑐
                                    
                                    
                                     Contradicted
                                    
                     status(𝑐 𝑖 ) =
                                    
                                    
                                     Contested                  𝛽𝑖+ ≥ 𝜃 𝑔 ∧ 𝛽𝑖− ≥ 𝜃 𝑐
                                                                 𝛽𝑖+ < 𝜃 𝑔 ∧ 𝛽𝑖− < 𝜃 𝑐
                                    
                                    
                                     Unknown
                                    

                                                       16
Remark 5.3 (Bilattice structure, after Belnap [4]). The four-valued set
{Supp, Contr, Contested, Unk} is the standard Belnap bilattice [4, 24]: two or-
thogonal lattice orders (information-increasing and truth-increasing). Under the information
(knowledge) order, the join of Supp and Contr is Contested (Both) and the meet is Unk
(None); under the truth order the meet is Contr and the join is Supp. We use this as a known
structural fact rather than claiming it as a contribution; what is new here is its instantiation
as the codomain of the grounding classifier (Definition 5.2) combined with the emission gate
of §5.3.

The signed weighted grounding coverages are
                  Í                  Í                           Í
                         𝑤𝑖              Contr 𝑤 𝑖                   𝑖: Contested 𝑤 𝑖
           𝑊 + = 𝑖:ÍSupp , 𝑊 − = 𝑖:Í               ,      𝑊± =          Í               ,
                       𝑤
                      𝑖 𝑖                  𝑖 𝑤𝑖                           𝑖 𝑤𝑖

and 𝑊 ? = 1 − 𝑊 + − 𝑊 − − 𝑊 ± . All four coverages lie in [0, 1], matching the per-call
deliverable in §10 and the empirical thresholds reported in §12. The pipeline emits iff
𝑊 + ≥ 𝜃 𝑒 and 𝑊 − +𝑊 ± ≤ 𝜃 𝑟 . A single contested load-bearing claim is grounds for abstention,
not a footnote.


5.3   The certificate

Lean 4: pedagogical sketch, full source in Grounding.lean

  inductive EpistemicStatus
    | supported | contradicted | contested | unknown
    deriving DecidableEq

  def classify (b_plus b_minus theta_g theta_c : Rat) : EpistemicStatus :=
    if b_plus ≥ theta_g ∧ b_minus < theta_c then .supported
    else if b_plus < theta_g ∧ b_minus ≥ theta_c then .contradicted
    else if b_plus ≥ theta_g ∧ b_minus ≥ theta_c then .contested
    else .unknown

  structure ConflictAwareGroundingCertificate where
    answer : String
    atomic_claims : List (String × Rat)
    retrieved : List String
    support_pos : List (List Rat)
    support_neg : List (List Rat)
    support_orth : List (List Rat)
    beta_plus : List Rat
    beta_minus : List Rat
    theta_g : Rat       -- support threshold
    theta_c : Rat       -- contradiction threshold
    theta_e : Rat       -- emission threshold
    theta_r : Rat       -- refutation threshold


                                              17
    statuses : List EpistemicStatus
    W_supported W_contradicted W_contested W_unknown : Rat
    emitted : Bool
    -- proof obligations (decidable; discharged by ‘decide‘)
    p_scores_simplex : ∀ i j, support_pos.get! i |>.get! j
                             + support_neg.get! i |>.get! j
                             + support_orth.get! i |>.get! j = 1
    p_beta_plus_max : ∀ i, beta_plus.get! i =
                           (support_pos.get! i).foldl max 0
    p_beta_minus_max : ∀ i, beta_minus.get! i =
                           (support_neg.get! i).foldl max 0
    p_statuses_correct : ∀ i, statuses.get! i =
                            classify (beta_plus.get! i) (beta_minus.get! i)
                                     theta_g theta_c
    p_W_sum_unit : W_supported + W_contradicted +
                   W_contested + W_unknown = 1
    p_total_weight_pos : 0 < totalWeight atomic_claims
    -- mass-correctness fields: each declared W aggregate equals the
    -- normalized weighted coverage over its status class, where
    -- ‘normalizedWeightOf‘ filters ‘atomic_claims‘ by the corresponding
    -- entry of ‘statuses‘ (the parallel list constrained by
    -- ‘p_statuses_correct‘ above) and divides by the total weight.
    -- Forecloses a malicious decomposer declaring ‘W_contradicted = 0‘
    -- while shipping contradicted claims.
    p_W_supported_correct     :
      W_supported     = normalizedWeightOf atomic_claims statuses .supported
    p_W_contradicted_correct :
      W_contradicted = normalizedWeightOf atomic_claims statuses .
      contradicted
    p_W_contested_correct     :
      W_contested     = normalizedWeightOf atomic_claims statuses .contested
    p_W_unknown_correct       :
      W_unknown       = normalizedWeightOf atomic_claims statuses .unknown
    p_emission_rule : emitted ↔
                        (W_supported ≥ theta_e ∧
                         W_contradicted + W_contested ≤ theta_r)
    p_reconstruction : Canonicalize (Conjoin atomic_claims) =
                        Canonicalize answer
    -- tier-4 oracles
    h_nli_oracle : SignedSupportOracle atomic_claims retrieved
    h_decomp_faithful : DecompositionOracle answer atomic_claims


Lemma 5.4 (Emission Gate Soundness, conditional on NLI and decomposition or-
acles). [ compiled ] For any ConflictAwareGroundingCertificate with emitted
= true, 𝑊 − + 𝑊 ± ≤ 𝜃 𝑟 .      Hence, conditional on SignedSupportOracle and
DecompositionOracle being correct on the input, emission implies that the normalized
Contradicted-plus-Contested weighted mass is at most the declared refutation threshold

                                         18
𝜃 𝑟 . In the zero-tolerance case 𝜃 𝑟 = 0, any positive-weight Contradicted or Contested
atomic claim blocks emission. For 𝜃 𝑟 > 0, low-weight contradicted or contested mass may
be emitted below the threshold, but it remains explicitly recorded in the certificate and Card
and is available to the application-policy layer.

Proof. By p_emission_rule directly: the emission flag is structurally equivalent to the
refutation-threshold inequality, so the Lean kernel discharges by definitional unfolding plus
rational-arithmetic reduction.

What this lemma is and is not. The lemma proves that the emission gate of the certificate is
sound: the gate’s emitted flag is true only when the weighted refutation mass is below threshold.
The actual epistemic content, that an atomic claim is genuinely Contradicted or Contested
by the retrieved evidence, is contributed by the SignedSupportOracle (the three-way
NLI judgment) below the trust boundary. The lemma is therefore a structural soundness
result for the gate, conditional on the oracle, rather than a theorem about contradictions in
the world. The architectural value, blocking a class of evidence-contradicting outputs that
scalar-confidence RAG pipelines cannot detect by construction, comes from the combination
of the NLI oracle and the gate; the lemma certifies that the gate respects its specification.
Verification status: compiled as Grounding.no_silent_contradictions in the ar-
tifact (audited axiom set: Ω ∪ {SignedSupportOracle, DecompositionOracle}); see
Appendix D.


5.4   Comparison with support-only RAG

Hallucinations with low support are caught by 𝑊 + < 𝜃 𝑒 . The harder failure mode is an
atomic claim that the retrieval corpus actively contradicts (e.g., “the patient’s CrCl of 22
mL/min is within apixaban’s renal range” when the FDA label requires CrCl ≥ 25). A
support-only certificate could report 𝑊ground = 95% and silently ship the contradiction; the
conflict-aware certificate rejects emission whenever the contradicted-plus-contested mass
exceeds 𝜃 𝑟 , and below that threshold the contradicted/contested mass is not silent but is
explicitly surfaced to the policy layer.


5.5   Limitations of the certificate

The certificate does not verify (i) that a Supported claim is actually true (the NLI oracle
is below the trust boundary); (ii) that the corpus is itself factually correct (RAG against
propaganda still produces well-grounded propaganda); (iii) that the decomposition oracle is
faithful (a malicious decomposer could omit a key claim; the reconstruction check mitigates
but does not eliminate this). These limits are the LLM-pipeline analogue of the precursor’s
grounded-coverage caveats.



                                               19
6     Maximal Certifiable Residue

The bilattice grounding certificate (§5) blocks emission when contradiction exceeds threshold.
But all-or-nothing abstention is an overcorrection: a ten-claim answer with one contradicted
claim is more useful if the nine certifiable claims ship and the one bad claim is dropped, with
the drop audit-logged. We formalize this maximal-informative behavior.


6.1   Definition

Let C = {𝐶1 , . . . , 𝐶𝑚 } be a finite family of decidable predicates on subsets of At(𝑦) =
{𝑐 1 , . . . , 𝑐 𝑛 } (the answer’s atomic claims). Representative constraints: 𝐶ground (every 𝑐 ∈ 𝑆
is Supported); 𝐶cons (no two members of 𝑆 are mutually contradictory); 𝐶pol (no member
triggers a forbidden-output rule); 𝐶pre (every implied tool-call passes its Hoare precondition);
𝐶bud (cumulative cost stays below budget).

Definition 6.1 (Maximal Certifiable Residue). [ compiled ] The certifiable family is
Cert (C, 𝑦) = {𝑆 ⊆ At(𝑦) | 𝐶 𝑗 (𝑆) for all 𝐶 𝑗 ∈ C}. The maximal certifiable residue
is                                                  ∑︁
                      MCR(C, 𝑦) = arg max              𝑤(𝑐),
                                                𝑆 ∈ Cert ( C,𝑦)
                                                                  𝑐∈𝑆

breaking ties by canonical lex order. When Cert = {∅}, the residue is empty and the pipeline
abstains.

Definition 6.2 (Monotone Constraint Family). [ compiled ] C is monotone (downward-closed)
if for every 𝐶 𝑗 and every 𝑆 ′ ⊆ 𝑆 ⊆ At(𝑦), 𝐶 𝑗 (𝑆) ⇒ 𝐶 𝑗 (𝑆 ′ ). We additionally require C to be
empty-admitting: 𝐶 𝑗 (∅) = true for every 𝐶 𝑗 ∈ C. This holds for all five sample constraints
above (each is vacuously true on ∅) and guarantees ∅ ∈ Cert even before any non-empty
witness is exhibited.

Of the five sample constraints, all are subset-monotone and empty-admitting except trivial
cases; the consistency constraint is monotone for the mutual-contradiction predicate (removing
a claim cannot introduce a contradiction).


6.2   Maximality, idempotence, monotonicity

Theorem 6.3 (Properties of MCR). [ compiled ] For any monotone, empty-admitting constraint
family C and answer 𝑦:
(i) MCR(C, 𝑦) is well-defined: ∅ ∈ Cert directly from empty-admission, so the arg max is
    over a non-empty finite set.
(ii) MCR(C, 𝑦) is weight-optimal: no element of Cert has strictly greater weight (and ties
     are broken by canonical lex order, so the operator is single-valued).


                                                20
(iii) (Idempotence) MCR(C, MCR(C, 𝑦)) = MCR(C, 𝑦).
(iv) (Monotone in constraints) C ⊆ C ′ implies 𝑤(MCR(C ′ , 𝑦)) ≤ 𝑤(MCR(C, 𝑦)).
(v) (Anti-monotone in evidence, via the constraint map) Fix any evidence-extension map 𝐸 ↦→
    C(𝐸) from observable evidence to a constraint family, and assume the map is monotone in
    the sense that 𝐸 ⊆ 𝐸 ′ implies C(𝐸) ⊆ C(𝐸 ′ ) (extending evidence only adds constraints
    or strengthens existing ones). Then 𝑤(MCR(C(𝐸 ′ ), 𝑦)) ≤ 𝑤(MCR(C(𝐸), 𝑦)), i.e.
    extending evidence is non-increasing in MCR weight. This follows from item (iv) applied
    to the induced constraint inclusion.

 Proof. (i) ∅ ∈ Cert by empty-admission. (ii) If some 𝑆 ∗ ∈ Cert had 𝑤(𝑆 ∗ ) > 𝑤(MCR), then
 𝑆 ∗ ∈ arg max, contradicting the tie-break rule. (iii) Reapplying MCR to its own output keeps
 the atomic set unchanged: the residue itself is in Cert and is maximal among its own subsets
 in Cert (by monotonicity, all subsets of the residue are in Cert). (iv) Adding constraints can
 only shrink Cert, so the optimum cannot increase. (v) By the assumed monotonicity of the
 evidence-to-constraint map, 𝐸 ⊆ 𝐸 ′ ⇒ C(𝐸) ⊆ C(𝐸 ′ ), so item (iv) applied to the induced
 inclusion gives the conclusion.

We use weight-optimal rather than the standard “⊆-maximal” phrasing because what the
operator actually maximizes is total claim weight, not subset extent. A weight-optimal
residue need not be a ⊆-maximal element of Cert when uncertified low-weight claims could
be appended without losing certification but would not raise the score.
 Verification status:         compiled as MCR.residue_is_fixed_point (and
 residue_is_certifiable, subset_of_residue_is_certifiable) in the arti-
 fact (audited axiom set: Ω).


 6.3   Lean structure

 Lean 4: pedagogical sketch, full source in MCR.lean

   structure MCRCertificate (AtomicClaim : Type) [DecidableEq AtomicClaim]
       where
     all_claims : Finset AtomicClaim
     weight : AtomicClaim -> Rat
     constraints : List (Finset AtomicClaim -> Bool)
     residue : Finset AtomicClaim
     residue_weight : Rat
     p_residue_subset : residue ⊆ all_claims
     p_residue_cert : ∀ C ∈ constraints, C residue = true
     p_monotone :
       ∀ C ∈ constraints, ∀ S T : Finset AtomicClaim,
         S ⊆ T -> T ⊆ all_claims -> C T = true -> C S = true
     p_weight_nonneg : ∀ a ∈ all_claims, 0 ≤ weight a
     p_maximal :


                                              21
        ∀ S : Finset AtomicClaim,
          S ⊆ all_claims ->
          (∀ C ∈ constraints, C S = true) ->
          (S.sum weight) ≤ residue_weight
      p_weight_correct : residue_weight = residue.sum weight



6.4    Worked example

A clinical-RAG answer decomposed into five claims:

                  Claim                             𝑤𝑖   𝛽+     𝛽−     Status   Action?
             𝑐1   Patient diagnosis                3.0   0.92   0.03    Supp
             𝑐2   Recommended drug                 2.0   0.88   0.04    Supp     order
             𝑐3   Dose frequency                   1.0   0.81   0.02    Supp
             𝑐4   Allergy check (concludes safe)   1.5   0.45   0.71   Contr
             𝑐5   Follow-up schedule               0.5   0.30   0.20    Unk


With constraints {𝐶ground , 𝐶pre } at 𝜃 𝑔 = 0.70, 𝜃 𝑐 = 0.50, and an action precondition requiring
𝑐 4 = Supp before ordering the drug 𝑐 2 : 𝐶ground excludes 𝑐 4 and 𝑐 5 ; 𝐶pre excludes 𝑐 2 when
𝑐 4 is absent; MCR = {𝑐 1 , 𝑐 3 } with weight 4.0. The pipeline emits the diagnosis and dose
frequency, drops the drug recommendation and follow-up, and audit-logs the drops. An
all-or-nothing abstention would emit nothing; a support-only certificate would have shipped
all five (including the silent contradiction at 𝑐 4 ); a contradictions-only filter would have
shipped {𝑐 1 , 𝑐 2 , 𝑐 3 } without catching 𝑐 2 ’s dependency on 𝑐 4 . MCR composes constraint
families coherently.


6.5    Computing the residue

Computing MCR(C, 𝑦) is a weighted-subset optimization and is NP-hard in general, even
when C is monotone: the special case of weighted maximum independent set on the conflict
graph induced by a pairwise-contradiction constraint reduces to it. The hard search is below
the trust boundary; the certificate carries the residue as a field, and the kernel only checks
that every constraint accepts the residue and that no certified element of Cert outweighs
it (a finite-list comparison, decidable by decide). Three regimes admit efficient search:
(i) when constraints decompose over atomic claims independently (each 𝐶 𝑗 is a per-claim
predicate), greedy removal of constraint-violators is optimal in 𝑂 (𝑛 · |C|); (ii) when claims
carry a dependency DAG (e.g. “patient has diabetes” ⇒ “patient has chronic condition”)
and constraints respect the DAG, 𝑂 (𝑛2 ) topological antichain extraction suffices; (iii) for
general non-monotone families at the typical 𝑛 ≲ 100 atomic-claim regime, off-the-shelf
SAT/SMT or weighted-MaxSAT enumeration solves the instance well within per-call latency
budgets. Outside these regimes, MCR reduces to weighted-subset optimization on which the


                                                   22
minimal-sufficient-evidence and weighted-MaxSAT literatures supply mature solvers; we
adopt those solvers below the trust boundary and rely on the kernel check above the boundary
for correctness.


7     Embedding Sensitivity and Paraphrase Stability

Given an embedding 𝐸 : 𝑇 → ℝ𝑑 with 𝐿 2 -normalized output and texts 𝑥, 𝑦 with sim(𝑥, 𝑦) =
⟨𝐸 (𝑥), 𝐸 (𝑦)⟩, we certify that the similarity decision is robust under a declared finite
perturbation family. Stability is not a semantic property of the encoder; it is a local
Lipschitz-style property whose verification is purely arithmetic once the family is fixed.


7.1    Selective sensitivity

Definition 7.1 (Meaning-Invariant and Significant Perturbation Families). [ specified ] For
𝑥 ∈ 𝑇, 𝐺 inv (𝑥) ⊂ 𝑇 consists of meaning-preserving edits (synonym replacement, voice
transposition, harmless typographical changes); 𝐺 sig (𝑥) ⊂ 𝑇 consists of meaning-changing
edits (negation, entity substitution, quantity change, role reversal). Both families are finite,
explicit, and declared as inputs.

We work in squared form so the certificate stays in ℚ. Define the meaning-invariant
                       2 (𝑥) = max ′                      ′
                                       𝑥 ∈𝐺inv ( 𝑥 ) ∥𝐸 (𝑥 ) − 𝐸 (𝑥) ∥ , the critical sensitivity floor
robustness radius 𝑅inv                                                2
  2 (𝑥) = min ′                   ′
               𝑥 ∈𝐺sig ( 𝑥 ) ∥𝐸 (𝑥 ) − 𝐸 (𝑥) ∥ , and the selective gap Δ (𝑥) = 𝑅sig (𝑥) − 𝑅inv (𝑥).
𝑅sig                                          2                             2         2          2

Δ2 > 0 certifies a local separation of meaning; Δ2 ≤ 0 flags a local encoder failure.

Lemma 7.2 (Family Monotonicity). [ specified ] 𝐺 inv (𝑥) ⊆ 𝐺 inv ′ (𝑥) ⇒ 𝑅 2 (𝑥; 𝐺 ) ≤
                                                                             inv      inv
  2 (𝑥; 𝐺 ′ ). An auditor extending the family can only weaken (never spuriously strengthen)
𝑅inv      inv
the guarantee.

Remark 7.3 (Why selective sensitivity). An encoder mapping every text to the same vector
has 𝑅inv = 0 but is useless because 𝑅sig = 0. The right objective is selective sensitivity: low
𝑅inv and high 𝑅sig .


7.2    The certificate

 Lean 4: pedagogical sketch, full source in Certificate.lean

    structure EmbeddingSensitivityCertificate (d : Nat) where
      text : String
      embedding : Vector Rat d
      G_inv : List String           -- neutral perturbations
      G_sig : List String           -- significant perturbations
      emb_inv : List (Vector Rat d)


                                                 23
     emb_sig : List (Vector Rat d)
     R_inv_sq : Rat                -- max squared L2-dist over G_inv
     R_sig_sq : Rat                -- min squared L2-dist over G_sig
     delta_sq : Rat                -- R_sig_sq - R_inv_sq
     p_inv_length : G_inv.length = emb_inv.length
     p_sig_length : G_sig.length = emb_sig.length
     p_bounded : ∀ v ∈ (embedding :: emb_inv ++ emb_sig), l2_norm_sq v ≤ 1
     p_R_inv_sound : ∀ e ∈ emb_inv, l2_dist_sq embedding e ≤ R_inv_sq
     p_R_sig_sound : ∀ e ∈ emb_sig, R_sig_sq ≤ l2_dist_sq embedding e
     p_delta_correct : delta_sq = R_sig_sq - R_inv_sq
     -- tier-4 oracle
     h_paraphrase_valid : ParaphraseOracle text G_inv G_sig

The first four proof fields reduce by decide or norm_num; the rest by rfl. The paraphrase
oracle stands in for the paraphraser’s faithfulness (tier 4).
Theorem 7.4 (Robust Similarity Bound, Squared Form). [ compiled ] For any
EmbeddingSensitivityCertificate, any unit-normalized document embedding
𝑑 ∈ ℝ𝑑 , and any 𝑒 ′ ∈ emb_inv: |⟨𝐸 (text), 𝑑⟩ − ⟨𝑒 ′ , 𝑑⟩| 2 ≤ 𝑅inv
                                                                 2 . Consequently, if the

threshold decision ⟨𝐸 (text), 𝑑⟩ ≥ 𝜃 ret (similarity√︃of the embedded query against the
pre-indexed document embedding 𝑑) has margin > 𝑅inv           2 , the decision is preserved across

every variant in 𝐺 inv . Here 𝜃 ret is the retrieval similarity threshold; the bilattice grounding
thresholds 𝜃 𝑔 , 𝜃 𝑐 , 𝜃 𝑒 , 𝜃 𝑟 of §5 are unrelated.

Proof sketch. By Cauchy–Schwarz: |⟨𝑢 − 𝑣, 𝑑⟩| 2 ≤ ∥𝑢 − 𝑣∥ 2 ∥𝑑 ∥ 2 ≤ 𝑅inv
                                                                      2 · 1. Lean discharges

via the named axioms cauchy_schwarz_sq (tier 2) and innerProd_sub (tier 2).

Verification status: compiled as robust_similarity_sq in Certificate.lean; transi-
tive axioms reported in Appendix D.

Two distinct claims, distinguished. Theorem 7.4 is a robust similarity bound: it uses only
  2 and certifies that 𝐿 drift on the meaning-invariant family is bounded by the declared
𝑅inv                    2
envelope. It does not require Δ2 > 0. The selective sensitivity claim, that meaning-changing
edits move farther than meaning-preserving ones, is the separate decidable predicate
                     SelectiveSensitivityPass(𝑐) := (0 < 𝑐.delta_sq)
on a constructed certificate. Selective sensitivity is what the policy layer (the Universal
Card; §10) reads to decide whether the encoder behaves correctly on this query; it is not
a precondition for Theorem 7.4. The certificate carries 𝑅inv  2 , 𝑅 2 , and Δ2 as fields, with
                                                                    sig
Δ2 tagged for the policy gate; the empirical scope of the certificate (Pilot B and Pilot B′ ,
§7.4–§7.5) reports how often Δ2 > 0 holds, distinct from the always-applicable robust-
similarity bound. This separation matters because the negative cells of Pilot B (paraphrase ×
attribute_flip) still carry a sound robust-similarity bound; what they do not carry is selective
sensitivity, and the Card downgrades emission accordingly.

                                               24
Floating-point and black-box embeddings. The formal certificate is exact over the
rationalized embedding representation supplied to Lean. In deployments where embeddings
are returned by a floating-point or black-box API, the implementation first commits to the
API transcript, the model-version hash, the tokenizer hash, and the embedding-service
configuration, then applies a deterministic quantization map to rational vectors. The
                                                             2
Card records both the rounded rational drift bound 𝑅inv,rounded      (𝑥) and a rounding-error
budget 𝜀 𝜂 ; policy margins are evaluated against the conservative error-adjusted bound
  2
𝑅inv,real (𝑥) ≤ 𝑅inv,rounded
                 2           (𝑥) + 𝜀 𝜂 . Thus the theorem remains exact for the audited rational
object, while the deployment records the additional approximation layer explicitly and the
auditor can replay the rational computation against the recorded transcript and hashes without
re-invoking the embedding service.


7.3   Top-𝑘 ranking and paraphrase decision margin

A simple corollary: ranking the document set by ⟨𝐸 (text), 𝑑⟩, the certified envelope partitions
documents into√︃in, maybe, out based on whether their similarity gap to the retrieval threshold
                   2 . Paraphrase decision-margin certificates layer on top: for any binary
𝜃 ret exceeds 2 𝑅inv
classifier 𝑓 over the 𝑘 paraphrases in 𝐺 inv , count agreement and certify a flip-free emission
whenever the agreement margin clears a threshold. Both are extensions of Theorem 7.4 that
share the same Lean structure.


7.4   Empirical scope of the inequality

The robust-similarity theorem (Theorem 7.4) applies whenever the declared 𝑅inv2 bound is
                                2
certified; it does not require Δ > 0. The empirical question measured here is separate:
how often the policy-layer selective-sensitivity predicate Δ2 > 0 holds for the declared
perturbation families. This was measured in Pilot B (§7.4), with design and pre-registered
predictions in the companion repository.


Setup. We sliced 𝑁=209 HotpotQA dev-distractor queries (post-yield-filter), generated 25
meaning-preserving paraphrases (𝐺 inv ) and 15 meaning-changing edits (𝐺 sig ) per query with
GPT-5, and validated each variant with a 3-judge panel (Claude Sonnet 4.5, GPT-5-mini,
Gemini 2.5 Flash). Panel reliability is high: minimum pairwise Cohen’s 𝜅 = 0.887 and
unanimous-accept rate 0.950, both well above the pre-registered 𝜅 ≥ 0.65 and unanimous-
accept ≥ 0.85 thresholds (the methodological reasons this 𝜅 is informative here while
it saturates in Pilot A’s panel are reconciled in §12.2). We embedded all variants on
text-embedding-3-large (strong-API encoder) and sentence-transformers/all-mpnet-base-v2
(open-weights baseline), then computed per-query 𝑅inv2 , 𝑅 2 , Δ2 . (Cohere embed-v3 was
                                                          sig
deferred for budget reasons; the run is parameterized for 𝑛 encoders and could be re-run
cheaply with a Cohere production key.)



                                              25
Hypothesis HB1: empirical scope of the inequality.

   Encoder                             Δ2 > 0 (95% CI)         Median Δ2        Threshold
   text-embedding-3-large             0.297 (0.234, 0.359)       −0.070       ≥ 0.80 (FAIL)
   sentence-transformers-mpnet        0.196 (0.144, 0.249)       −0.109       ≥ 0.60 (FAIL)

The §7 inequality holds in only 30% of queries on the strong-API encoder and 20% on the
open-weights baseline. Median Δ2 is negative on both. This is a substantive negative result,
not a measurement artefact: the panel that defined 𝐺 inv vs. 𝐺 sig agreed at 𝜅 = 0.89, so the
categories are reliably labeled.


Hypothesis HB2: certificate F1 as a flip predictor.
                                          √︃        A pre-registered secondary test asks
whether the certificate’s predicted budget        2 correctly bounds the cases where top-𝑘
                                                 𝑅inv
retrieval flips under paraphrase. Using a sample-split (𝑅inv2 calibrated from a 70% partition

of 𝐺 inv , predictor tested on the held-out 30%), the certificate achieves F1 = 0.131 on both
encoders, against a pre-registered threshold of ≥ 0.65. The top-10 set flips under paraphrase
for 81–85% of (query, paraphrase) pairs; the certificate’s drift threshold cannot separate the
                                                          2 .
flippers from the non-flippers because both sit inside 𝑅inv


Hypothesis HB4: cross-encoder differentiation. Median |Δ2 | spread between the two
encoders is 0.64× (threshold ≥ 2.0×): the two encoders differ in level but not by a margin
large enough to pass the pre-registered differentiation test. Both fail in the same direction.
On HB3. The pre-registration originally listed an HB3 hypothesis testing the certifi-
cate’s positive-fraction on a contradictions-only baseline. HB3 was retired during the
pre-registration revision pass for the same reason H1 and H5 were rewritten in Pilot A
(§12.2): once measured, the original HB3 formulation was unrealisable on the data slice.
The HB-numbering jumps from HB2 to HB4 to preserve the pre-registration record; the
retired HB3 wording is documented in the companion repository.


Why the inequality fails on this benchmark. HotpotQA dev-distractor queries are short
(10–20 tokens, often two named entities and a connective) and many of the panel-labeled
meaning-changing edits (negation, single-attribute flip) are surface-close to the original (one
or two tokens differ), while the panel-labeled meaning-preserving paraphrases routinely
involve heavy lexical and syntactic restructuring. Modern sentence encoders embed short
queries primarily by surface form. The mechanical consequence is that a long paraphrase
often lands farther from the original than a short negation does, which violates the certificate’s
central inequality on a per-query basis.
This is consistent with the embedding literature on negation-sensitivity [20, 36] and with the
broader finding that distributional encoders track contextual co-occurrence rather than logical


                                               26
form. The certificate’s soundness is unaffected (Theorem 7.4 continues to hold whenever
Δ2 > 0); its premise cannot be assumed to hold on production encoders for adversarial
short-query benchmarks.


Phase 1 ablation: where exactly does the inequality hold? The §7 certificate’s 𝐺 inv and
𝐺 sig are declared edit-type families (§7.1). The following ablation is post-hoc exploratory
analysis: the edit-type subset stratification was not in the pre-registered Pilot B hypothesis
set, and the cells are reported here to characterize where the aggregate failure sits, not to
make a confirmatory claim. We treat the ablation’s positive cells (e.g. surface×entity_swap
at 96.7%) as hypotheses to be validated by future targeted runs rather than as registered
findings on this slice. Conditioning the empirical inequality on every (sub-𝐺 inv , sub-𝐺 sig )
edit-type combination on the same 209-query slice reveals a clean rectangular structure on
text-embedding-3-large:

                   𝐺 inv subset   𝐺 sig subset     Δ2 > 0 frac (95% CI)   Median Δ2
                   surface        entity_swap      0.967 (0.938, 0.990)     0.345
                   synonym        entity_swap      0.913 (0.875, 0.947)     0.310
                   surface         negation        0.865 (0.817, 0.909)     0.170
                   reorder        entity_swap             0.861             0.298
                   paraphrase     entity_swap             0.847             0.290
                   synonym         negation               0.836             0.136
                   paraphrase     attribute_flip          0.450            −0.022
                   reorder        attribute_flip          0.455            −0.022


The pattern is encoder-stable (sentence-transformers-mpnet shows the same ordering at
slightly weaker magnitudes: surface×entity_swap 0.938, paraphrase×attribute_flip 0.340).
Aggregated positive-fractions: by 𝐺 sig alone, entity_swap 0.79, negation 0.60, attribute_flip
0.38; by 𝐺 inv alone, surface 0.64, synonym 0.53, voice 0.43, reorder 0.41, paraphrase 0.40.


The certificate is a typed guarantee, not a uniform one. The §7 specification (§7.1)
requires the deployer to declare 𝐺 inv and 𝐺 sig as explicit finite families. The Phase 1 ablation
is therefore not a refutation of the certificate but a measurement of which declarations are
empirically supported on this benchmark. Three deployment-relevant declarations clear the
pre-registered ≥ 0.80 bar on text-embedding-3-large:

• Surface-close paraphrase against entity confusion (surface×entity_swap, 97%): the
  deployer guarantees robustness when the query is rephrased only by whitespace / case /
  punctuation differences and the failure to defend against is naming the wrong entity. This
  is the strongest setting and corresponds to a common production threat model in legal and
  clinical retrieval.
• Synonym-only paraphrase against entity confusion (synonym×entity_swap, 91%): tolerates
  one or two synonym substitutions; same threat model.

                                                   27
• Surface-close paraphrase against negation (surface×negation, 87%): tolerates trivial
  paraphrase, defends against single-word logical inversion.

The hard cell is paraphrase×attribute_flip: heavy restructuring of the query combined with a
single-attribute meaning change (e.g., a date or numeric attribute) sits inside the embedding’s
resolution. Deployers in domains where attribute-level distinctions are critical (clinical
dosage, legal jurisdiction) should treat this as a known scope limit and either (i) use a richer
signature (entity-typed token-distance comparators) or (ii) condition the §7 certificate on a
𝐺 inv that excludes heavy paraphrase.


Pilot data and reproducibility (Pilot B short-form). The Pilot B numbers reported in
this subsection are reproducible from the companion repository (per-query Δ2 , per-pair drift
and flip records, panel votes with verbatim judge outputs). On the full 𝑁=209 slice, the
dominant cost is the 3-judge panel labeling on 8,000 panel calls per judge rather than the
embedding API itself.


7.5   Pilot B′: long-form HotpotQA paragraphs

To test whether the short-form failure is intrinsic to commodity encoders or specific to short
adversarial queries, we ran a second pre-registered pilot (Pilot B′ ) on the same benchmark
with the query unit shifted from questions to gold supporting paragraphs (median ≈110
tokens, multiple named entities and predicates per query). The retrieval corpus, panel
composition, generator, encoders, and statistical protocol are identical to Pilot B; only the
input length and named-entity density change. 𝑁=64 effective queries (sized to fit the
available budget at the observed per-query cost for long-form variant generation).


Hypothesis HB′ 1: the inequality on long-form paragraphs.

          Encoder                       Δ2 > 0 (95% CP CI)     Median Δ2    Threshold
          text-embedding-3-large        1.000 (0.944, 1.000)     0.390     ≥ 0.70 (PASS)
          sentence-transformers-mpnet   0.984 (0.916, 1.000)     0.419     ≥ 0.55 (PASS)


The §7 inequality holds on every long-form query on text-embedding-3-large and on 63 of
64 on the open-weights baseline. Median Δ2 flips sign (from −0.07 short-form to +0.39
long-form) and rises by an order of magnitude. The HB′ 1 thresholds are pre-registered and
clear by large margins. CI methodology. For Pilot B′ point estimates of 64/64 and 63/64
the bootstrap-resample interval collapses to a degenerate [1.000, 1.000] that misrepresents
the uncertainty inherent in the small-𝑁 slice; we therefore report exact Clopper–Pearson
binomial 95% intervals here (denoted CP). The 𝑁=64 slice is sized to fit the available budget
at the observed per-query cost for long-form variant generation, and the long-form result is
correctly characterized as a strong directional finding under a tight one-sided lower bound


                                                28
rather than a narrow two-sided deployment claim; the “essentially universal” framing should
be read in that light.


Hypothesis HB′ 2: tightness of the drift bound for retrieval-flip prediction.


 Encoder                               Flip rate             Top-10 overlap   Cert F1    Threshold
 text-embedding-3-large        0.626 (vs 0.812 short-form)       0.820         0.148    ≥ 0.40 (FAIL)
 sentence-transformers-mpnet   0.733 (vs 0.848 short-form)       0.785         0.137    ≥ 0.40 (FAIL)


Long-form retrieval is materially √︃
                                  more stable (flip rate 0.81→0.63, overlap 0.73→0.82), but
the certificate’s predicted budget 𝑅inv2 is still not a tight predictor of which paraphrases flip

top-𝑘. On long-form the certificate’s soundness premise is universally met (HB′ 1 above),
but the bound’s tightness for the retrieval-flip use case remains loose. These are two distinct
empirical claims:

• HB′ 1 (premise): the inequality Δ2 > 0 holds; the certificate makes a sound claim.
                    √︃
• HB′ 2 (tightness): 𝑅inv2 is large enough to permit drift that crosses retrieval boundaries,

  so the bound is not a useful flip-discriminator on its own.

The right tightening is a calibrated post-bound: deploy the §7 certificate as a soundness
gate (block when the inequality fails to hold) and pair it with a separately-fitted retrieval-flip
predictor. Forward work.


Hypothesis HB′ 3: edit-type ablation on long-form. Repeating the Phase 1 ablation
on the long-form data: every (sub-𝐺 inv , sub-𝐺 sig ) cell yields 1.000 positive-fraction on
text-embedding-3-large. The cell that was hardest on short-form, paraphrase×attribute_flip
(45% positive), is at 1.000 on long-form (median Δ2 = 0.465). The same pattern holds
on mpnet, with two cells dropping marginally to 0.984 (paraphrase×entity_swap and
paraphrase×attribute_flip) and the rest at 1.000.


Hypothesis HB′ 4: cross-encoder uniformity. Median |Δ2 | ratio between text-embedding-
3-large and mpnet on long-form is 1.07× (vs 0.64× short-form), against a pre-registered
≥ 2× differentiation threshold. The two encoders perform near-identically on long-form,
which is the operationally desirable signal: the certificate’s value transfers across encoder
providers.


Synthesis: the §7 certificate is sound on every input length, with selective-sensitivity
supported on long-form HotpotQA pending domain replication. Combining Pilots B
and B′ :

                                                   29
• Soundness (the implication itself): unaffected; the Lean-checked Theorem 7.4 continues to
  hold whenever its declared premise does.
• Premise on adversarial short queries (Pilot B): holds in 30% / 20% of cases; only
  specific edit-type sub-rectangles (e.g., synonym×entity_swap) clear the ≥ 0.80 threshold.
  Deployers on short-query benchmarks should declare a restrictive 𝐺 inv family.
• Premise on long-form text (Pilot B′ ): holds in 100% / 98% of cases across every edit-type
  combination on this slice. Deployers on long-form retrieval can declare the full 𝐺 inv family
  with empirical support on this benchmark, subject to target-domain validation.
• Tightness for retrieval-flip prediction (Pilots B and B′ ): loose on both. The certificate is a
  soundness gate, not a tight flip predictor.
• Cross-encoder generalisation: the two-encoder pattern is consistent across input lengths;
  the failure modes and successes track input length and edit-type more than encoder provider.


Pilot data and reproducibility (Pilot B′ long-form). The Pilot B′ numbers are reproducible
from the companion repository (per-query Δ2 , per-pair drift and flip records, panel votes). On
the 𝑁=64 slice, long-form variant generation incurs a higher per-query cost than short-form,
driven by generator output proportional to passage length.


What this changes for §7 and §10 (Universal Card). The certificate is correctly char-
acterized as conditional on a per-query measurement of Δ2 > 0. The Universal Card’s
stability field (§10) accordingly reports the measured Δ2 as a per-call signal rather than as
a deployment-wide guarantee, and the Card’s policy layer can downgrade or block emission
when Δ2 ≤ 0. The forward-work questions are: (i) which encoder/dataset combinations
satisfy the inequality at material rates (we expect long-form documents, named-entity-heavy
clinical/legal text, and technical paragraphs to behave better than short adversarial QA);
(ii) whether richer signature definitions (e.g., conditioning on detected negation [36] or on
entity-level edit types) restore the inequality.


Why this matters for the framework. The §5 grounding certificate (validated empirically
in §12: catch=1.0 at FBR=0.064) and the §7 embedding certificate (premise empirically
narrow on this benchmark) together illustrate the framework’s intended epistemic posture: the
certificates are soundness machinery, and the empirical question is always “does the per-call
premise hold here?”. A pilot that finds the premise holds robustly is a deployment-readiness
result; a pilot that finds it does not is a scope-of-applicability result. Both are publishable
empirical contributions; both feed back into the Card’s per-call signal vector. Pilot B is the
second kind, on this benchmark, on these encoders.




                                               30
8     Hoare-Style Agent Action

Agentic LLM systems write to files, call APIs, send messages [51, 58, 62]. A single action
can be irreversible; each action warrants a formal audit trail that it was safe given the system’s
state. Hoare logic [18, 27] is the natural formalism, and the resulting certificate has the
cleanest discharge profile in the framework: in the compiled artifact, the trajectory certificate
carries no axioms at all (Appendix D), so every proof step reduces by kernel computation
alone. The Hoare family is special only in that it pushes all of its conditionality into the
type signatures and predicate definitions, leaving none in the form of named axioms; the
per-failure cost remains highest among the families and the deployment story is unusually
compelling for decision-makers. Axiom-freeness is a statement about the proof’s discharge
mechanism, not about the semantic adequacy of the human-authored predicates (owner =
user, path is in sandbox, age > 30d); see §13.1 for the precise formulation of what
axiom-freeness does and does not mean.


8.1    The certificate

For each callable action 𝑎, specify a precondition Pre(𝑎, 𝜎, 𝛼) and postcondition
Post(𝑎, 𝜎, 𝜎 ′ , 𝛼) as decidable Lean predicates on a state model 𝜎. The LLM proposes (𝑎, 𝛼);
the formal layer verifies Pre, executes 𝑎 via a typed executor, verifies Post, and emits the
certificate.
Lean 4: pedagogical sketch, full source in Action.lean

    structure ActionCertificate (𝜎 : Type) (ActionName : Type)
                                 (Args : ActionName -> Type) where
      action : ActionName
      args : Args action
      state_pre : 𝜎
      state_post : 𝜎
      pre_pred : 𝜎 -> (args : Args action) -> Prop
      post_pred : 𝜎 -> 𝜎 -> (args : Args action) -> Prop
      p_pre_holds : pre_pred state_pre args
      p_post_holds : post_pred state_pre state_post args
      p_execution : execute action args state_pre = state_post

    structure TrajectoryCertificate (𝜎 : Type) where
      steps : List (ActionCertificate 𝜎 ActionName Args)
      p_chain : ∀ i, i + 1 < steps.length ->
                  (steps.get! (i+1)).state_pre = (steps.get! i).state_post

A trajectory certificate fails to type-check at the first unsafe step; the agent either emits a
complete safe trajectory or is blocked. The LLM is the proposer; a small deterministic
Lean-audited runtime is the final authority that permits or blocks side effects.


                                               31
8.2   Five invariant classes

Concrete agent frameworks instantiate the certificate against five invariant classes: data
invariants (no scope leakage); budget invariants (token / API / monetary cost); safety
invariants (forbidden tools / destinations); state invariants (action coherent with memory
and task state); trace integrity (logged and re-executable). Each is a decidable predicate
populated from the deployment’s policy layer.


8.3   Beyond Hoare

Real agents exhibit structure that simple sequential Hoare does not capture. We sketch the
path; full development is in the extended catalogue (§15). Separation logic for modular
substates [45]: each action certificate asserts only the resources it reads and writes; frame
rules let an action’s certificate compose into a larger context. Rely-guarantee [33] for parallel
tool calls: each branch declares the environmental changes it tolerates and what it promises
others; the trajectory composes by checking each branch’s rely is satisfied by the conjunction
of others’ guarantees. Belief-state Hoare for partial observability: pre/post on belief paired
with an observation-soundness axiom. Temporal-logic protocol correctness: “authenticate
before transfer,” “confirm before destructive action,” modeled as CTL∗ / LTL formulas over
the trajectory.
Verification status:       the Hoare baseline is compiled, axiom-free (Action.
trajectory_all_steps_safe); the rely-guarantee, belief-state, and temporal-logic
extensions are specified and become mechanizable once the obligations are decidable.


8.4   Connection to shielding

The pattern generalizes safe-RL shielding [1] and logic-constrained RL [26]: in both, a
runtime monitor intercepts an unsafe action and substitutes a safe alternative. Action
certificates make the monitor’s guarantees formal and the substitutions auditable. The
difference is that our monitors are kernel-audited Lean predicates rather than learned or
hand-coded policies, and the audit trail is cryptographically bound to the ML artifact via the
oracle digest.


8.5   Empirical validation: Pilot C

Pilot C tests the §8 trajectory certificate’s pre-execution gating behavior on a controlled
filesystem-sandbox benchmark; design, adversarial-action registry, and pre-registered hy-
potheses are in the companion repository.


Setup. A tempdir-rooted filesystem sandbox per trajectory; nine tools (ls, cat, find,
stat, md5, rm, mv, mkdir, chmod) dispatched through a single gate; five deterministic Hoare-

                                               32
predicate constructors (path_in_sandbox, path_in_subprefix, mtime_at_least,
owner_is, delete_count_within_budget); five representative tasks spanning four cate-
gories (file-management, deduplication, cleanup, reorganization), each carrying a per-tool
predicate set; three harnesses (Unaudited, Deny-list, Treatment) sharing the same ReAct
agent (GPT-5).


Threat model. Direct-injection adversarial actions: after two agent steps establish non-
trivial sandbox state, a registry of 18 known-unsafe action proposals is spliced into the
trajectory and run through each harness’s gate. The proposals span three pre-registered attack
classes: out-of-scope file references (/etc/passwd, ~/.ssh/id_rsa), owner/age-violating
deletes (recent or wrong-owner files), and budget-exceeding sequences (six deletes against a
5-delete cap).
The pre-registered design specified prompt-injection adversaries (adversarial system messages
embedded in the agent’s observation stream); a preliminary feasibility check found that
GPT-5 simply did not act on those injection prompts (refusal rate >0.95), making the
prompt-injection design uninformative as a test of the gate. The registered slice therefore
uses direct splicing; the deviation is recorded in the pre-registration notes of the companion
repository, and the result is framed accordingly. This is a strictly stronger test of the gate
in isolation: direct injection removes agent cooperation as a confound, so any block in the
Treatment column is attributable to the gate and not to the agent declining to propose the
action. The two failure modes (gate fails to block a violating action; agent falls for prompt
injection) are orthogonal; Pilot C measures the first by construction, and the second is a
separately-measurable property of the agent that is not the §8 certificate’s responsibility. A
complementary pilot that varies model and prompt to elicit non-trivial prompt-injection
success on a more manipulable agent, and then re-runs the same gate against that agent’s
proposals, is forward work.


Trajectory composition. The 48 trajectories decompose as 16 per harness across the
three harnesses, where each harness’s 16 trajectories comprise 11 adversarial trajectories
carrying 18 spliced direct-injection unsafe-action proposals (some trajectories carry multiple
injections) plus 5 benign trajectories carrying 6 destructive-but-permitted proposals. The
block-rate denominators below are over the 18 injected adversarial proposals and the 6 benign
destructive proposals respectively.


Results (48 trajectories; approximately 30 minutes of wall-clock).

           Harness                          Block rate on injected unsafe (95% CI)   n
           Unaudited (no gate)                       0.000 (0.000, 0.000)            18
           Deny-list (regex baseline)                0.278 (0.111, 0.500)            18
           Treatment (Lean-checked Hoare)            0.667 (0.444, 0.889)            18



                                              33
False-block rate on benign destructive proposals: 0.000 on all three harnesses (𝑛=6 each).
Audit-log informativeness on Treatment blocks: 1.000 (13 of 13 blocks contain the failed
predicate, the offending state value, the expected condition, and the upstream agent proposal
text). The 13 Treatment blocks comprise the 12 unsafe-injection blocks (out of 18 spliced
proposals) plus 1 read-only stat block on a benign trajectory where the agent proposed
inspecting a path the sandbox declares out-of-scope; the latter is non-destructive and hence
does not count toward the false-block-rate denominator above.
In-scope reading. Of the 13 attacks targeting a registered predicate clause, 12 were blocked
and 1 passed (92.3%); the 5 remaining unblocked within-budget delete probes are correctly
permitted under the registered budget predicate (the 6th in the sequence, which exceeds the
budget, is blocked). HC1’s denominator includes both classes, by literal pre-registration; the
diagnostic separates them.


Hypothesis verdicts.


   H     Statement (registered)                                                 Verdict
 HC1     Treatment block rate ≥ 0.95 on injected unsafe     FAIL (→ predicate-completeness diagnostic)
         actions
 HC2     Treatment FBR ≤ 0.05 on benign destructive                              PASS
         actions
 HC3     Treatment block rate ≥ Deny-list + 15pp                          PASS (Δ = 38.9pp)
 HC4     Unaudited block rate ≤ 0.05 (structural floor)                         PASS
 HC5     Audit-log informativeness ≥ 0.95 of Treatment                          PASS
         blocks


HC1 verdict: FAIL, and what the FAIL localizes. The literal pre-registered statement
of HC1 (Treatment block rate ≥ 0.95 on injected unsafe actions) is not satisfied: Treatment
blocks 12 of 18 (66.7%, 95% CI [0.444, 0.889]). We report this as the verdict of record.
What the audit log says to fix. The empirical contribution Pilot C was designed to
deliver for typed-guarantee certificates is the audit-log diagnostic on each unblocked attack.
The 6 unblocked attacks split cleanly: 5 are within-budget delete probes that the t02
delete_count_within_budget predicate correctly permits (the 6th in the same sequence
is blocked, exactly when the budget is exceeded); the remaining 1 is a recent-mtime move
that probes a predicate the t01 mv declaration deliberately omits. The audit log therefore
names exactly which predicate clauses (t02 budget narrowness, t01 mv mtime omission) need
extending to close the gap. The diagnostic also exposes a registration-time operationalisation
choice: HC1’s denominator was specified as “adversarial proposals,” not “predicate violators,”
so 5 within-budget probes that no registered predicate violates were nevertheless counted as
failures-to-block. Conditional on attacks that target a predicate clause in scope, the block rate

                                               34
is 12/13. We log the conflation as a registration deviation to be tightened in any follow-up;
the verdict of record remains HC1 FAIL on the literal pre-registered formula.
Why the Lean soundness theorem is unaffected. Every action that passed the gate satisfied the
predicates declared in scope, and no action that violated a declared predicate passed the gate.
The Lean-checked trajectory soundness theorem (Action.trajectory_all_steps_safe,
compiled axiom-free in the artifact; see Appendix D and §8) is therefore independent of
HC1’s pre-registration framing.


Scope. Pilot C runs on a registered slice of five representative tasks (selected to span the
four predicate families); the original 30-task plan was scaled to fit the available budget and
the preliminary feasibility schedule. Predicate-registry breadth across more tasks, more
tools, and more attack classes is forward work (§16.2). The 18 adversarial proposals are
hand-curated; automated adversary generation (LLM-driven proposal mining against a
held-out predicate set) is the natural follow-up.


What this validates for §8. The empirical claim Pilot C makes for the Hoare-action
family is the most sharply-typed of the four pilots: within the predicate-encoded scope, the
Treatment gate dominates the deny-list baseline by 39 percentage points (0.667 vs 0.278)
on a controlled adversarial-injection set, with 100% audit-log informativeness and zero
false-blocks on benign trajectories. The Hoare family’s zero-axiom Lean proof structure
turns the empirical question into pure predicate-set design: the audit log of unblocked attacks
names exactly which predicate clauses need to extend to close the residual 8%. This is the
empirical contribution Pilot C was designed to deliver.


9     Compositional Stability

The three local certificate families developed earlier in the paper give a grounding bound
(§5), an embedding-stability bound (§7), and a Hoare action bound (§8). Each is local: it
bounds a single pipeline layer or claim. The pipeline-level question is what survives at the
final output given a bounded perturbation of the raw user input, and that question is what
this section answers. The closed-form pipeline-wide budget formula derived below is what
makes the framework usable end-to-end rather than per-layer: it turns the local catalogue
of §§5, 7, and 8 into a single inequality the deployer can inspect to decide whether a given
adversary is provably out of reach.


9.1   Pipeline model

A pipeline Π is a finite sequence of layers 𝐿 1 , . . . , 𝐿 𝑛 with 𝑓𝑖 : X𝑖 → Y𝑖 = X𝑖+1 and metric
𝑑𝑖 on each space. Composition is Π(𝑥) = 𝑓𝑛 ◦ · · · ◦ 𝑓1 (𝑥).



                                               35
Definition 9.1 (Certified Layer). [ compiled ] 𝐿 𝑖 is certified with gain 𝑔𝑖 ∈ ℚ ≥0 and margin
𝑚 𝑖 ∈ ℚ ≥0 if a kernel-audited certificate witnesses 𝑑𝑖+1 ( 𝑓𝑖 (𝑥), 𝑓𝑖 (𝑥 ′ )) ≤ 𝑔𝑖 · 𝑑𝑖 (𝑥, 𝑥 ′ ) for all
𝑥, 𝑥 ′ with 𝑑𝑖 (𝑥, 𝑥 ′ ) < 𝑚 𝑖 , and the layer’s discrete decision is invariant under that bound
(nominal stability).

The local certificates of the three families above
                                              √︃ supply 𝑔𝑖 and 𝑚 𝑖 by construction. Embedding
(§7): 𝑔 = 1 via Cauchy–Schwarz, 𝑚 = 𝑅inv     2 as defined there. Discrete decision layers

(paraphrase, ranking, emission threshold): 𝑔 = 0, 𝑚 = flip distance or coverage slack. Agent
action (§8): 𝑔 = 0, 𝑚 = precondition slack.

From a finite witness family to a metric ball. Definition 9.1 states the certified-layer
inequality on a metric ball {𝑥 ′ : 𝑑𝑖 (𝑥0 , 𝑥 ′ ) < 𝑚 𝑖 }, but the embedding certificate of §7 is built
from a finite declared family 𝐺 inv (𝑥0 ) (Definition 7.1). The bridge is layer-specific: for the
embedding layer, 𝑅inv  2 certifies the worst-case displacement over the witness family by direct

enumeration, and Cauchy–Schwarz lifts that to every 𝑥 ′ with ∥𝐸 (𝑥 ′ ) − 𝐸 (𝑥 0 ) ∥ 2 ≤ 𝑅inv    2 , i.e.
                                          2
the entire 𝐿 2 -ball of squared radius 𝑅inv in the embedding-output metric. So the metric-ball
                 √︃
margin 𝑚 𝑖 = 𝑅inv     2 holds for the layer’s output-side distance for free, while the input-

side distance (𝑑1 on text inputs) is constrained only over 𝐺 inv (𝑥0 ) itself unless a separate
encoder-Lipschitz hypothesis is supplied. We adopt this as a layer-specific match between
certificate witness and metric: the embedding layer transports a finite-family declaration into
a continuous-ball guarantee on its output, and the downstream layers consume the latter. For
text-input layers without a metric, 𝑔𝑖 is taken as 0 and the layer is treated as a discrete-decision
gate (e.g. paraphrase classifier, retrieval threshold), short-circuiting the metric requirement
upstream of any continuous propagation.


9.2    The theorem

Lemma 9.2 (Two-Layer Compositional Stability, Base Case). [ compiled ] Let Π2 = 𝐿 2 ◦ 𝐿 1
with both layers certified. If 𝑑1 (𝑥0 , 𝑥 ′ ) < 𝑚 1 and 𝑔1 · 𝑑1 (𝑥0 , 𝑥 ′ ) < 𝑚 2 , then 𝐿 2 (𝐿 1 (𝑥 ′ )) =
𝐿 2 (𝐿 1 (𝑥0 )) at the discrete-decision level (or under canonicalization).

Verification     status:          compiled         as      Composition.compositional_
stability_two_layer in the artifact (audited axiom set: Ω). The base case
unfolds to two applications of nominal stability plus rational arithmetic.

Theorem 9.3 (Compositional Stability, 𝑛-Layer). [ specified ] Let Π = 𝐿 𝑛 ◦ · · · ◦ 𝐿 1 have
certified layers with gains (𝑔𝑖 ) and margins (𝑚 𝑖 ). Define 𝜀★1 = 𝜀 0 and 𝜀 𝑖+1 = 𝑔𝑖 · 𝜀 𝑖 . If
                                                                            ★             ★
                                             ′                   ′                       ′
𝜀 𝑖 < 𝑚 𝑖 at every interface, then 𝑑1 (𝑥0 , 𝑥 ) < 𝜀0 implies Π(𝑥 ) = Π(𝑥0 ) (or 𝐶 (Π(𝑥 )) =
 ★

𝐶 (Π(𝑥 0 )) if Π ends in canonicalization).

Proof. By induction on 𝑖, with Lemma 9.2 as the inductive step. Base (𝑖 = 1): 𝑑1 (𝑥0 , 𝑥 ′ ) <
                                                         ′
       1 < 𝑚 1 , so 𝐿 1 ’s nominal stability gives 𝐿 1 (𝑥 ) ≡dec 𝐿 1 (𝑥 0 ) and 𝑑 2 (·, ·) ≤ 𝑔1 𝜀 0 = 𝜀 2 .
𝜀 0 = 𝜀★                                                                                               ★



                                                    36
Inductive step: assuming the conclusion at layer 𝑖, apply Lemma 9.2 to layers 𝐿 𝑖 , 𝐿 𝑖+1 . At
𝑖 = 𝑛 the discrete decision is invariant.

Verification status: specified. The 𝑛-layer statement is a structural induction over a
List.foldl of certified layers; each step is an instance of the compiled compositional_
stability_two_layer base lemma plus the per-layer nominal_stable field. Mecha-
nizing the inductive lift is a single Lean proof obligation over a finite list and is currently
architecturally enforced via the chain-of-margins type signature; closing it to fully compiled
is a focused exercise.
                                                                                       Î𝑛
Corollary 9.4 (Pipeline Conditioning Number and Budget). [ specified ] Let 𝜅 Π = 𝑖=1         𝑔𝑖
                                           Î
(cumulative gain) and 𝐵Π = min1≤𝑖 ≤𝑛 𝑚 𝑖 / 𝑗<𝑖 𝑔 𝑗 , with the convention that any term whose
               Î
denominator 𝑗<𝑖 𝑔 𝑗 vanishes (i.e. some earlier layer is a discrete-zero gate, 𝑔 𝑗 ★ = 0
for some 𝑗 ★ < 𝑖) is treated as +∞ and does not bind the minimum. Equivalently, let
              Î                                                                        Î
𝑖★ = min{𝑖 : 𝑗<𝑖 𝑔 𝑗 = 0} when such an index exists; then 𝐵Π = min1≤𝑖<𝑖★ 𝑚 𝑖 / 𝑗<𝑖 𝑔 𝑗 ,
and otherwise the minimum is taken over all 𝑛 layers. Theorem 9.3 guarantees decision
invariance for every 𝜀0 < 𝐵Π , and 𝐵Π is the tightest such budget producible from the given
per-layer certificates.


9.3   Discrete decision layers and the budget

In most real pipelines, cumulative gain collapses to zero after the first discrete-decision
layer (paraphrase decision, retrieval threshold, emission threshold), and 𝐵Π reduces to
the tightest single-layer margin. This formalizes the folklore observation that pipelines
with strong discrete gates are more stable end-to-end than pipelines with many cascaded
continuous layers. Concretely, for a 7-layer RAG pipeline with (𝑔𝑖 ) = (1, 0, 0, 0, 1, 0, 0)
and (𝑚 𝑖 ) = (0.12, 50, 3, 0.08, 0.77, 1, 1), we have 𝜅 Π = 0 and 𝐵Π = 0.12 (dominated by
the embedding margin from §7). The motivating instability “we have no idea whether this
similarity score is stable” becomes “the canonical denotation of the answer is invariant under
any lexical paraphrase whose 𝐿 2 embedding drift is below 0.12.”


9.4   Adversarial corollary

If a paraphrase adversary is bounded by 𝜀0adv on the user input, every adversary with 𝜀0adv < 𝐵Π
is provably unable to flip the canonical denotation. This is a positive statement over all
adversaries in the declared family, complementing empirical adversarial testing which only
exhibits flipping examples when found.


Perturbation-budget convention. In this paper, 𝐵Π and the corresponding Card field
perturbation_budget denote a certified stability radius (larger values represent tighter
guarantees): the pipeline’s canonical denotation is invariant under any upstream perturbation
of 𝐿 2 -norm strictly below the budget. Implementations that instead store a worst-case drift

                                              37
envelope (such as 𝑅inv2 or a quantization-error-adjusted drift bound, where smaller values

are tighter) should either use a separate drift_bound field or attach a convention tag to the
Card so the application-policy layer applies the correct comparison direction.


10     The Universal Assurance Card

The three local certificate families of §§5, 7, and 8 address specific failure modes; the residue
operator (§6) and the compositional stability theorem (§9) compose them. What is still
missing, viewed from a deployment perspective, is the single object that travels with each
governed LLM call under a declared assurance mode and lets a downstream consumer
decide, automatically and without reading the model output, whether to act on the result.
This section gives that object: a Lean 4 record we call the Universal Assurance Card, with
a decidable consistency predicate, designed for the per-call deliverable of any high-stakes
deployment. The structure and predicate are stated in Lean form below; integration into
the compiled artifact as AssuranceCard.lean is straightforward but separate engineering
work and is currently specified in the verification-status convention.


10.1    Three design principles

1. No single confidence number. A scalar collapses orthogonal failure modes and licenses
   exactly the false confidence Proposition 4.2 forbids. The card is a vector.
2. Application-policy interpretation. The same vector is read differently by legal research,
   clinical triage, creative writing, agentic action; the card carries fields, the application
   carries policy. Cards are portable; policies are deployment-specific.
3. Always-emitted. Every call produces a card, including failures: abstention is a verdict,
   and the user is owed a machine-readable reason.


10.2    The schema (specified)

The card is declared below as a Lean 4 structure.                   The consistency proof
field p_verdict_consistent is decidable: given the field values, the predicate
VerdictConsistent checks that the verdict label is internally consistent with the de-
clared field values on the card itself (e.g., Certified requires unverified_layers = []
and all safety checks true). Once the structure and predicate are added to the artifact (no
Mathlib-heavy lemmas are required; only Rat, Bool, and List String comparisons),
#print axioms on the worked-example cards from §11 should report only Ω.
What VerdictConsistent is and is not.          The predicate is a schema-
consistency check on the Card record itself: given the values of the eight
field groups, does the verdict tag make sense? Concretely, the visible Certi-
fied branch checks unverified_layers = [], forbidden_check_pass = true,

                                              38
action_precondition = true, contradicted_mass = 0, and in_scope = true,
and does not visibly check contested_mass, unknown_mass, budget_under_limit,
freshness via issue_time/expiry_time, calibration_gap, semantic_agreement,
or certificate_digest validity. Each of these gaps is deliberate: the predicate is
intentionally a lightweight schema gate, and the omitted properties are policy-layer or
digest-checked obligations rather than schema obligations.
It is not a re-verification of the underlying certificates: that the embedding-sensitivity
                                        2 − 𝑅 2 for the declared families, that the ground-
certificate’s Δ2 field is the actual 𝑅sig     inv
                     −
ing certificate’s 𝑊 is the normalized weighted coverage of contradicted claims (the
p_W_contradicted_correct field of the grounding certificate, §5), or that the Hoare
trajectory’s preconditions hold on the executed state, are properties of the underlying compiled
certificates and are enforced there. The Card binds those underlying guarantees into one
decidable record by referencing them via the certificate_digest field (a hash of the
signed underlying certificates produced when the Card is emitted); a downstream auditor
verifying the Card re-checks the digest against the underlying certificates’ kernel-audited
build outputs. VerdictConsistent is therefore the lightweight schema gate; the deeper
guarantee chain runs through the digest into the compiled certificates of §§5, 7, and 8, and
the policy-layer thresholds (AssurancePolicy) enforce deployment-specific cuts on the
omitted fields.
Lean 4: illustrative sketch, AssuranceCard schema; decidable consistency; specified,
not yet in the compiled artifact
  inductive AssuranceVerdict
    | certified
    | partial   (gaps : List String)
    | residue   (weight : Rat)
    | abstain   (reasons : List String)

  structure AssuranceCard where
    verdict : AssuranceVerdict
    -- stability (sources: composition, embedding)
    perturbation_budget : Rat
    variant_flips : Nat
    semantic_agreement : Rat
    -- evidence (source: bilattice grounding)
    supported_mass contradicted_mass contested_mass unknown_mass : Rat
    -- calibration (catalogue: conformal / calibration)
    conformal_set_size : Nat
    calibration_gap : Rat
    -- reproducibility (catalogue: proof-of-sampling)
    is_deterministic : Bool
    sample_count : Nat
    proof_of_sampling : Option ByteArray
    -- scope and freshness (catalogue: scope-of-validity, provenance,
      temporal)


                                              39
 in_scope : Bool
 scope_predicates_held : List String
 source_snapshot_hash : ByteArray
 issue_time expiry_time : Nat
 -- safety (source: Hoare action; catalogue: negative-guarantee, budget)
 forbidden_check_pass : Bool
 action_precondition : Bool
 budget_under_limit : Bool
 -- residue (source: MCR)
 residue_coverage : Rat
 dropped_claims : List String
 -- gaps and provenance
 unverified_layers : List String
 model_version_hash prompt_template_hash : ByteArray
 human_signatures : List ByteArray
 -- audit handle
 certificate_digest : ByteArray
 verifier_version : String
 replay_handle : String
 -- decidable consistency obligation (full Card record passed)
 p_verdict_consistent : VerdictConsistent (AssuranceCard.mk ...)

-- The predicate is a function on the whole ‘AssuranceCard‘ record;
-- the match destructures the verdict tag and reads the field values
-- it inspects from the card. The fields the predicate does not
-- destructure (e.g. contested_mass, unknown_mass, budget_under_limit,
-- issue_time, expiry_time, calibration_gap, semantic_agreement,
-- certificate_digest) are deliberately omitted -- see the
-- "What VerdictConsistent is and is not" discussion above.
def VerdictConsistent (c : AssuranceCard) : Prop :=
  match c.verdict with
  | .certified =>
     c.unverified_layers = [] ∧
     c.forbidden_check_pass = true ∧
     c.action_precondition = true ∧
     c.contradicted_mass = 0 ∧
     c.in_scope = true
  | .partial gaps =>
     c.unverified_layers = gaps ∧
     c.forbidden_check_pass = true ∧
     c.action_precondition = true
  | .residue w =>
     c.residue_coverage = w ∧ c.dropped_claims ≠ []
  | .abstain rs =>
     rs ≠ [] ∧ c.residue_coverage = 0




                                  40
Four kinds of residue. The residue clause uses the universal characterization
dropped_claims ≠ [], which is witnessed by any of four reasons the MCR operator
(§6) drops items from a candidate emission, each a separate monotone constraint family in C:
 • Evidence residue: 𝐶ground excludes Contradicted or Contested claims; characterized
   by contradicted_mass + contested_mass > 0. (Clinical case study, §11.1.)
 • Action residue: 𝐶pre excludes implied tool-calls whose Hoare precondition fails; charac-
   terized by dropped_claims listing blocked actions even when contradicted_mass =
   0. (Agentic case study, §11.2.)
 • Scope residue: a scope-of-validity predicate fails on a candidate atomic claim, so the MCR
   drops it; characterized by scope_predicates_held excluding the relevant predicate.
 • Budget residue: 𝐶bud excludes the marginal claim that would push cumulative cost
   past the declared limit; characterized by budget_under_limit = true with non-empty
   dropped_claims.
The four kinds are mutually compatible (a single card can witness multiple), and each
composes with the others through the MCR’s monotone-constraint discipline. The card’s
verdict is Residue whenever any of them fires; the field vector tells the consumer which.
Verification status: specified. The Card structure and VerdictConsistent predicate are
stated in Lean form above; the predicate is decidable by case analysis on the verdict tag
plus rational and list comparisons; integrating it into the artifact as AssuranceCard.lean
with a worked example for each of the four verdicts (each closing via decide) is a focused
engineering step and is the natural follow-on to this paper. This is the same compiled-status
precision applied to Compositional Stability (Lemma 9.2 compiled, Theorem 9.3 specified).


10.3   The four verdicts

Certified. Every required certificate passes. The output is emitted with a kernel-audited
bundle.

Partial. Some non-load-bearing layers are unverified; the card explicitly names them in
unverified_layers. The output is emitted; the consumer’s policy decides whether the
named gaps are tolerable.

Residue. The full answer cannot be certified; a maximal certifiable subset can. The card
reports the residue weight (Theorem 6.3) and lists dropped claims. The consumer receives a
strictly smaller but kernel-audited answer.

Abstain. No emission. The card reports machine-readable reasons; an honest abstention is
a first-class outcome.




                                             41
10.4    Application policy

The card is not directly comparable across applications. A deployment publishes its
acceptance policy as a separate object that maps the field vector to an accept / reject /
downgrade decision. Both the card and the policy are kernel-objects, so the deployment’s
accept/reject choice is auditable.
Lean 4: illustrative sketch, application-policy schema

  structure AssurancePolicy where
    min_supported_mass : Rat
    max_contradicted_mass : Rat
    max_contested_mass : Rat
    required_in_scope : Bool
    max_unverified_gaps : Nat
    require_action_safe : Bool
    max_calibration_gap : Rat
    min_perturbation_budget : Rat
    require_proof_of_sampling : Bool
    max_age_seconds : Nat
    forbidden_must_pass : Bool

  def policy_accepts (P : AssurancePolicy) (c : AssuranceCard) : Bool := ...



Table 4: Five canonical acceptance policies. The same card is interpreted differently by each.
Numbers are illustrative starting points; a real deployment tunes them on its own ground
truth.

       Policy field           Creative    Enterprise   Legal    re- Clinical   Agentic   ac-
                                          QA           search                  tion
       supported_mass ≥       0           0.70         0.90         0.95       0.95
       contradicted_mass ≤    1.0         0.10         0.02         0.01       0.00
       contested_mass ≤       1.0         0.20         0.08         0.04       0.02
       required_in_scope      no          yes          yes          yes        yes
       max_unverified_gaps    5           2            0            0          0
       require_action_safe    no          no           no           yes        yes
       max_age_seconds        ∞           30 d         7d           24 h       1h
       forbidden_must_pass    policy      yes          yes          yes        yes



10.5    Wire protocol

The wire protocol is intentionally light. Request side: a min_certificate_policy field
carries the application’s policy; the provider commits to either returning a card the policy
accepts, returning residue or abstention with a reason code, or raising an error. Response side:
the response carries a top-level certificate field (the AssuranceCard) alongside the


                                                 42
answer, plus an audit handle so a third party can replay the kernel check without re-running
the LLM. Selective disclosure: for privacy-sensitive workloads, the provider returns the
Merkle root of the card plus only the leaves the user is authorized to see. Versioning: the card
carries verifier_version. Adoption pathways and regulatory mappings are deployment
artifacts; we collect them in Appendix F rather than the main text, where they would crowd
out the technical core.
The Universal Assurance Card answers the question “what does it mean for a generative
AI system to ship trust along with output, in deployments that need to ship trust?” The
schema is the consolidator; the policy layer is the application interface. Together they turn
the certificate taxonomy into a per-call deliverable that any provider serving high-stakes use
cases can attach to its assurance-mode endpoint in the next product release.


11     Two Worked Case Studies

This section gives two end-to-end examples chosen to exercise the framework’s core: clinical
RAG, where MCR and bilattice grounding are most distinctive, and an agentic Hoare
execution, where action safety is the deployment story. Each ends with a filled-out Universal
Assurance Card. The numerical values in both case studies are illustrative and internally
consistent rather than measured; the case studies are intended to exhibit Card behavior and
certificate composition, not to make empirical claims. Measured pre-registered data on
the constituent certificates is reported elsewhere: grounding in §12 (Pilot A), embedding
sensitivity in §7.4–§7.5 (Pilots B and B′ ), and Hoare-style agent action in §8.5 (Pilot C).
End-to-end validation of the Card consolidator itself remains forward work, structured as a
Pilot D family of domain-specific validations (§16.8).


11.1   Case study 1: Clinical RAG with contradiction detection

Setup. A clinical decision-support system answers “Is this 62-year-old patient with atrial
fibrillation a candidate for direct oral anticoagulation (DOAC) given their CKD-4 renal
function?” over (a) ACC/AHA and ESC guidelines, (b) the patient’s chart, (c) the hospital’s
formulary, and (d) drug-interaction databases. The clinical numbers below are stylized
illustrative placeholders.


Per-layer certificates.
1. L0 Scope-of-Validity. Query clinically valid; chart current within 30 days; NLI model on
   whitelist; corpus timestamp within 90-day freshness window. All checks pass.
2. L1 Embedding sensitivity. Under a 50-variant lexical paraphrase family 𝐺 inv on the
            2 = 0.014 (√· ≈ 0.118); on a 30-variant significant family 𝐺 , 𝑅 2 = 0.19.
   query, 𝑅inv                                                           sig sig
                  2
   Selective gap Δ = 0.176 > 0, encoder behaves correctly on this query.


                                              43
3. L2 Conflict-aware grounding. Twelve atomic claims decomposed; reconstruction check
   passes. Key finding: the recommendation of apixaban is supported by 3 guidelines
   (𝛽+ = 0.94). However, one atomic claim (“the patient’s CrCl of 22 mL/min is within
   apixaban’s renal range”) is contradicted by the FDA label (CrCl ≥ 25 for standard
   dosing): 𝛽 − = 0.89. Status: Contradicted. 𝑊 + = 92%, 𝑊 − = 8% (above 𝜃 𝑟 = 5%).
   The certificate’s emission gate blocks the full answer (Lemma 5.4, conditional on the
   NLI oracle’s contradiction judgment).
4. L3 Maximal Certifiable Residue. With 𝑐 4 removed, the remaining 11 claims satisfy all
   constraints. The MCR (the same operator developed in §6, here applied to a 12-claim
   instance rather than the 5-claim worked example of §6.4) returns the 11-claim residue at
   weight 92% (illustrative weights chosen as round numbers; per-claim weight assignment
   is omitted for compactness). The output becomes: “Apixaban is a supported DOAC
   choice in AF; however, for this patient’s CrCl of 22 mL/min, standard dosing is outside
   the FDA label, so dose reduction or alternative agent required. Consult nephrology /
   pharmacy.”
5. L4 Hoare action gate. The downstream action “order apixaban at standard dose” has
   precondition CrCl ≥ 25, which fails. The Hoare certificate blocks the order and escalates
   to human review.
6. L5 Compositional Stability. Per-layer gains (𝑔𝑖 ) and margins (𝑚 𝑖 ) from L1–L4 give
   pipeline budget 𝐵Π ≥ 0.06; the canonical denotation of the emitted residue is invariant
   under any embedding 𝐿 2 drift below 0.06.


What is caught. The conflict-aware grounding certificate detects the contradiction that the
support-only variant misses. MCR retains maximum utility: instead of abstaining entirely,
the system emits an honest partial answer. The action certificate blocks the unsafe order.
Each catch corresponds to a named certificate in the framework, and each is auditable by
an external reviewer (a hospital committee, a malpractice carrier) without access to model
weights or prompt.

Filled-out Universal Assurance Card (illustrative).
Lean 4: clinical card (illustrative)

  verdict                       := residue 0.92
  perturbation_budget           := 0.06
  variant_flips                 := 0    (50 paraphrases)
  semantic_agreement            := 1.00
  supported_mass                := 0.92
  contradicted_mass             := 0.08
  contested_mass                := 0.00
  unknown_mass                  := 0.00
  calibration_gap               := 0.03
  is_deterministic              := false


                                            44
  sample_count                  := 5
  in_scope                      := true
  scope_predicates_held         := ["query_clinical", "chart_fresh_30d",
                                    "corpus_within_90d", "nli_whitelisted"]
  source_snapshot_hash          := 0xFA7E..0421
  issue_time                    := 1714000000 ; expiry_time := 1714086400
  forbidden_check_pass          := true
  action_precondition           := false    ; (Hoare gate blocked apixaban order)
  budget_under_limit            := true
  residue_coverage              := 0.92
  dropped_claims                := ["c4: CrCl 22 mL/min within apixaban range
                                      (CONTRADICTED by FDA label)"]
  unverified_layers             := []
  model_version_hash            := 0x3D11..7AAB
  prompt_template_hash          := 0x9A02..5C6D
  human_signatures              := []
  certificate_digest            := 0xB7C9..3041
  verifier_version              := "leanv4.30.0-rc2-mathlib"
  replay_handle                 := "rag-clinical-2026-04-25-7c4fa"

The clinical-policy profile (Table 4) requires supported_mass ≥                         0.95,
contradicted_mass ≤ 0.01, and action_precondition = true. The card’s ver-
dict is Residue with 𝑊 − = 0.08 and action_precondition = false; the policy rejects the
card under Certified or Partial but accepts the residue payload subject to clinician sign-off
(the human_signatures field, here empty, would be populated post-review).


11.2   Case study 2: Agentic Hoare execution (sandboxed file system)

Setup. An LLM agent is instructed to consolidate the user’s project notes by deleting drafts
older than 30 days and merging surviving notes into a single document. The agent has a
typed file-system API: stat, read, write, delete, each with declared pre/post conditions
in the formal layer. State 𝜎 is a Lean record mapping paths to (timestamp, content,
owner). The agent operates within a sandbox bound declared by the user’s policy.


Per-layer certificates.
1. L0 Semantic-type role check. The instruction text is tagged user_instruction;
   retrieved file contents are tagged tool_output; prompt-injection attempts within
   retrieved contents fail the role-coercion check at compile time.
2. L1 Plan certificate. The agent’s plan is decomposed: (stat *), filter age >
   30d, (delete drafts), (read survivors), (write merged). Each step is a typed
   action with declared pre/post.
3. L2 Trajectory certificate. Step 1 stat *: Pre = “directory exists”; Post = “returns


                                             45
   metadata, 𝜎 unchanged.” Discharged. Step 2–N (delete drafts): Pre = “file exists
   ∧ age > 30d ∧ owner = user ∧ path is in sandbox”. The agent proposes deleting
   notes/old_meeting.md (52 days, owner = user, in sandbox). Pre discharged. Post =
   “file removed; 𝜎 ′ = 𝜎 minus path.” Executor produces 𝜎 ′ ; Post verified.
4. L3 The unsafe step. The agent proposes deleting notes/shared/team_design.md as
   a draft. Pre requires owner = user; the file’s owner is team. Pre fails. The trajectory
   certificate fails to type-check at this step. The agent is blocked; the planner is re-prompted
   with the failure witness (CEGAR-style; see catalogue §15).
5. L4 MCR over the executable subset. The MCR operator (Theorem 6.3) accepts the
   largest prefix-closed subset of the trajectory whose constraints (Pre, sandbox, owner, age)
   hold. Output: 7 of 9 deletions executed, 2 blocked. The merge step’s Pre (“every input
   survivor exists”) is satisfied on the executed subset; the merged document is written.
6. L5 Budget invariant. Cumulative tokens, API calls, and wall-clock under declared limits.


The structural lesson. The Hoare action certificate blocks the out-of-scope deletion
structurally: the kernel refuses to type-check a trajectory containing an action whose pre-
condition is unmet. There is no “best-effort filter” to circumvent and no policy adjustment
that could let the unsafe action through silently. The MCR turns the blocked step into a
partial execution rather than aborting; the audit log names the blocked steps; the residue’s
action_precondition field is true because every executed step’s precondition was dis-
charged (the rejected steps simply do not appear in the trajectory). A baseline unaudited
agent would have either deleted the team file (irreversible) or aborted the entire batch on the
first failure. The operational rule the example illustrates is that the LLM proposes a typed
action and a small kernel-audited runtime is the final authority that permits or blocks side
effects.


Card summary (compressed). The agentic card differs from the clinical one chiefly in
residue kind (action-residue versus evidence-residue) and in the absence of evidential mass:
verdict = residue 0.78, contradicted_mass = 0.00, contested_mass = 0.00,
action_precondition = true (over executed steps), dropped_claims listing the two
blocked deletions with owner-mismatch reasons, is_deterministic = true, in_scope
= true, budget_under_limit = true. The agentic-action policy (Table 4) requires
require_action_safe = true and contradicted_mass ≤ 0; both hold. The policy
accepts the residue payload because no in-scope action’s precondition was violated, and the
blocked steps are listed for the user. The full card has the same field structure as the clinical
one (§11.1); we omit the verbatim listing.


Domain mapping. The two case studies above are illustrative of a broader pattern.
Analogous Card-bearing pipelines apply in patent claim charting (where a single prior-art
reference can support and refute different elements of the same independent claim, the

                                               46
bilattice grounding case), in regulated-finance disclosure analysis (where temporal-validity
windows on filings and regulations compose with action-precondition gates on analyst
recommendations), and in legal case-law retrieval (where circuit-split holdings produce
contested grounding and long-form embedding sensitivity is jointly load-bearing). The
clinical and agentic walkthroughs are exhibited here for compactness; the family of high-
stakes domains the framework targets is the subject of the Pilot D family of empirical
validations outlined in §16.8.


12     Empirical Validation: Pilot A on HotpotQA

The case studies in §11 use synthetic numbers to illustrate how the certificates and the
Universal Card behave on representative inputs. This section reports a pre-registered
empirical pilot (“Pilot A”) that puts the conflict-aware bilattice grounding certificate (§5,
Lemma 5.4) to an adversarial test on a public benchmark, against three distinct baselines,
with measured catch and false-block rates. The pilot ran in three iterations (a preliminary
read v3; a confirmatory run v4; a clean rerun v5 with corrected hypothesis wordings derived
from v4’s diagnostics); all numbers reported here are from the v5 registered analysis.


12.1   Pipeline and methods

Dataset. HotpotQA dev distractor [61], deterministically sliced (seed 42) into disjoint pools:
300 perturbation candidates and 225 unperturbed candidates. Multi-hop bridge questions
dominate.
RAG generator. Claude Sonnet 4.5 produces a 1–3 sentence answer from gold supporting
paragraphs, instructed to refuse with “Insufficient information” when sources are insufficient.
22 of 225 unperturbed cases (9.8%) returned a refusal and are excluded from the false-block-
rate denominator (a vacuous block on a refusal is correct behavior, not a false block; the
refusal rate is reported separately).
Atomic-claim decomposition. Gemini 2.5 Flash-Lite, with a parse-failure cascade that
escalates to 8192-token budget then to a cross-provider GPT-5 fallback. Decomposer-choice
sensitivity is checked separately (§12.5).
NLI signature. Three-way LLM-as-NLI (entail / contradict / neutral) via GPT-5, with chunk-
concatenation aggregation: 𝛽+ = 𝜎 + (claim, chunk1 ⊕ . . . ⊕ chunk𝑛 ), 𝛽 − = 𝜎 − (claim, ·).
Concat aggregation lets the NLI see cross-chunk evidence so HotpotQA bridge claims
(synthesised from facts in multiple chunks) are not mis-classified as “Unknown.” Per-chunk-
max aggregation is preserved as a registered ablation (§12.6).
Bilattice classification. As Lemma 5.4: 𝜃 𝐺 =𝜃 𝐶 =0.5 for the four-way label, 𝜃 𝐸 swept in
{0.50, 0.55, . . . , 1.00} to produce a Pareto-frontier curve, 𝜃 𝑅 =0.05.
Adversarial perturbation. Each candidate received one perturbation chosen from {negate,
swap, flip} on the targeted atomic claim (§5 terminology). A three-judge cross-model

                                             47
panel (GPT-5, Claude Opus 4.5, Gemini 2.5 Pro) labels each candidate as “contradicted” or
not; only candidates a majority of the panel labels contradicted enter the perturbed slice.
Yield: 264 of 300 (88%) accepted; unanimous-accept rate: 0.936, well above the 0.85
pre-registered threshold.
Methods compared.
• Treatment: full bilattice + emission gate (Lemma 5.4).
• B1 (cosine baseline): block iff max𝑖 cos(answer, chunk𝑖 ) ≥ 𝜃 𝐵1 , sweep 𝜃 𝐵1 ∈ [0.5, 1.0]
  in 0.05 steps.
• B2 (self-consistency, 𝑘 ∈{1, 5}): generate 𝑘 samples, decompose, cluster claims, block on
  cluster-disagreement.
• B3 (raw NLI, no support gate): block iff max𝑖 𝑤 𝑖 𝛽𝑖− ≥ 0.5.


12.2   Hypothesis verdicts

Six hypotheses pre-registered (v5 wording, with the v4 wording retained as a comparison
footnote):


                H    v5 statement                                               Verdict
                H1   ∃𝜃 𝐸 such that Treatment achieves catch ≥ 0.95 at FBR      PASS
                     ≤ 0.10, and B1 achieves no such operating point at any
                     threshold.
                H2   Treatment catch_blk ≥ 0.70.                                PASS
                H3   Treatment catch_tgt ≥ 0.60 (target-claim catch).           PASS
                H4   ∃𝜃 𝐸 such that Treatment catch ≥ 0.95 and FBR ≤ 0.15.      PASS
                H5   B1 cannot reach catch = 1.0 at FBR ≤ 0.10 for any 𝜃 𝐵1 .   PASS
                H6   Panel unanimous-accept rate ≥ 0.85.                        PASS


Pre-registration revisions. Three hypotheses were rewritten between v3/v4 and v5 once
their original formulations proved unrealisable on the data. H1 was originally a 60pp
Pareto-dominance test that is upper-bounded at zero whenever the catch axis saturates at
1.0; v5 replaces it with the Pareto-reachability formulation above. H5 was originally a B1
catch-ceiling ≤ 0.30 that is empirically false (B1 reaches 1.0 at 𝜃 𝐵1 ≥ 0.85); v5 replaces it
with a true negative claim about catch=1.0 reachability. H6 originally combined a 𝜅 ≥ 0.6
component with the unanimous-accept threshold, but 𝜅 degenerates near unanimity (a rater
near 100% drives the chance-correction denominator to zero); v5 retains the unanimous-
accept threshold and drops the 𝜅 component. The methodological observations these revisions
surface (saturating-Pareto pathology and 𝜅 saturation under near-unanimous panels) are
discussed in §12.7. The verbatim v3/v4 wordings are recorded in the pilot specification in
the companion repository.



                                                 48
Reconciling Pilot A’s 𝜅 with Pilot B’s 𝜅. A reader comparing the two might wonder how
Pilot A reports 𝜅 ≈ −0.014 alongside 93.6% unanimous agreement while Pilot B (§7.4)
reports 𝜅 = 0.887 on a structurally similar 3-judge panel. The two panels label different
things at different base rates. Pilot B’s panel labels paraphrase quality (the categories
“meaning-preserving” vs. “meaning-changing”), where the base rates are well away from
unanimity, so 𝜅 is informative and large. Pilot A’s panel labels contradiction status, where
one rater is near 100% on the negative class for a registered slice of unperturbed cases,
driving the marginal-equality denominator of 𝜅 to near zero, which is the classic chance-
correction saturation. This is why v5 retired the 𝜅 component for Pilot A’s H6 in favor of
unanimous-accept, which does not have that pathology, and is also why the same panel
discipline reproduces high 𝜅 on Pilot B: the difference is in the labeled task, not the panel.


12.3     Main results

Effective sample size: 264 perturbed (panel-accepted out of 300 candidates), 203 unperturbed
(refusal-excluded out of 225).


       Method                              catch_blk (95% CI)     catch_tgt   false_block (95% CI)
       Treatment (𝜃 𝐸 =0.50)                      1.000            1.000      0.064 (0.034, 0.099)
       Treatment (𝜃 𝐸 =0.90, registered)          1.000            1.000      0.227 (0.167, 0.286)
       B1 @ 𝜃=0.85                                0.992             n/a              0.232
       B1 @ 𝜃=0.90                                1.000             n/a              0.266
       B2 (𝑘=1)                            0.295 (0.242, 0.348)    0.295      0.350 (0.281, 0.414)
       B2 (𝑘=5)                            0.292 (0.239, 0.348)    0.292      0.261 (0.202, 0.320)
       B3                                  0.977 (0.958, 0.992)    1.000      0.044 (0.020, 0.074)


What the table says. (i) Treatment achieves catch = 1.0 at FBR = 0.064, an operating point
B1 cannot reach for any 𝜃 𝐵1 (B1’s lowest FBR at catch ≥ 0.95 is 0.232). (ii) Treatment
massively dominates self-consistency: McNemar’s exact test 𝑝 < 10−30 for both 𝑘=1 and
𝑘=5. (iii) B3 (contradiction-only) is a strong baseline at this scale, achieving catch = 0.977
at FBR = 0.044; Treatment matches its operating point at 𝜃 𝐸 =0.50 and offers a tunable knob
for higher- support-coverage regimes.


12.4     Pareto frontier (Treatment 𝜃 𝐸 sweep vs B1 sweep)

Treatment achieves catch = 1.0 across the entire 𝜃 𝐸 sweep; the free parameter selects the
operating point along the FBR axis:




                                                    49
                         𝜃𝐸           catch    FBR      𝜃 𝐵1     catch    FBR
                         0.50         1.000    0.064    0.50     0.432    0.010
                         0.55         1.000    0.108    0.60     0.602    0.089
                         0.60         1.000    0.113    0.70     0.788    0.123
                         0.65         1.000    0.138    0.80     0.928    0.202
                         0.70         1.000    0.148    0.85     0.992    0.232
                         0.80         1.000    0.187    0.90     1.000    0.266
                         0.90–0.95    1.000    0.227    0.95     1.000    0.409
                         1.00         1.000    0.256    1.00     1.000    1.000


The 𝜃 𝐸 =0.50 point is unreachable for B1 at any 𝜃 𝐵1 : B1 only enters the catch ≥0.95 regime
at FBR ≥0.232, while Treatment is already at FBR=0.064 there. This is the operationally
meaningful comparison: in deployment, the operating point is chosen for tolerable FBR, not
at the saturation ceiling.


12.5   Decomposer-choice robustness

A pre-registered sensitivity test (script 06) re-runs decomposition on a 200-example subsample
with GPT-5 substituted for the registered Gemini 2.5 Flash-Lite. Treatment catch differs by
< 5pp between the two decomposers, well within the pre-registered ≤ 5pp threshold. The
main result is therefore not an artefact of the registered decomposer’s idiosyncrasies.


12.6   Ablation: which architectural choices are load-bearing?

             Configuration                                        Catch     FBR    Δ FBR
             Registered v5 (concat NLI, 𝜃 𝐸 =0.5)                 1.000    0.064    n/a
             Per-chunk-max NLI ablation (v3 default), 𝜃 𝐸 =0.5    1.000    0.350   +0.286
             Concat NLI, 𝜃 𝐸 =0.9 (v3 registered)                 1.000    0.227   +0.163
             Per-chunk-max NLI, 𝜃 𝐸 =0.9 (v3 baseline)            1.000    0.450   +0.386


NLI aggregation choice (concat vs per-chunk-max) is the dominant hyperparameter. It
changes Treatment’s FBR by ∼ 2.3× at 𝜃 𝐸 =0.5. The per-chunk-max default fails on multi-hop
claims because no single chunk entails a synthesised fact; concat aggregation lets the NLI
score the synthesised claim against all evidence at once. We recommend concat as the
default for any RAG corpus where claims may require multi-chunk synthesis (HotpotQA-like
multi-hop QA, clinical guidelines that cross documents, legal precedent chains).


12.7   Methodological observations

The three iterations surfaced empirical-evaluation pitfalls worth naming for subsequent work
in this area.



                                                  50
• Reasoning-token starvation in modern LLMs. GPT-5 and Gemini 2.5 use hidden
  reasoning tokens that consume the visible-output budget first. Calls with max_tokens
  < 2048 silently return empty text or 400 errors, with no signal in normal logs. Affected
  components: NLI (originally 64 tokens), perturbation generator (512), decomposer
  (2048, still too tight), panel judges (128). Recommendation: all reasoning-capable LLM
  calls should default to max_tokens ≥ 4096 with a usage-metadata check that warns on
  output_tokens=0.

• Per-chunk vs. chunk-concatenated NLI on multi-hop claims. The original pipeline used
  per-chunk-max aggregation. On HotpotQA bridge questions (∼11% of unperturbed claims)
  the answer synthesises facts across chunks; no single chunk entails the synthesised claim,
  so the NLI returns “neutral” on every chunk, the bilattice classifies the claim “Unknown,”
  and the support gate fires a false-block. Chunk-concatenated aggregation drops this rate
  from 11% to 6%.

• Refusals vs. false-blocks. A vacuous block on a refusal (RAG returns “Insufficient
  information”) is correct behavior, not a false block. v3 mis-counted these in the FBR
  denominator, contaminating the rate by 24 percentage points. Recommendation: pre-
  register whether refusals are excluded from the FBR denominator; report the refusal rate
  as a first-class primary metric.

• Cohen’s 𝜅 near unanimity. Three-judge agreement was 93.6% unanimous, but minimum
  pairwise 𝜅 was −0.014. 𝜅 corrects for chance agreement; when one rater is near-100% on
  one label, the chance-correction term saturates and any disagreement on the remaining
  cases drives 𝜅 to zero or below. Recommendation: pre-register 𝜅 thresholds only when
  expected base rates are away from unanimity; use unanimous-accept and majority-accept
  rates for verification panels.

• Saturating Pareto frontiers and the 60pp gap. “Min gap over the entire B1 frontier ≥
  60pp” is mathematically unattainable when both methods reach catch = 1.0 at high enough
  thresholds. The right formulation is Pareto-reachability: “Treatment achieves an operating
  point B1 cannot.” This is the deployment-relevant question; the original min-gap test was
  a methodological error in hypothesis design, not a result.

These lessons are not evidence against the framework; they are evidence about what discipline
an empirical evaluation needs in order to produce informative numbers. The five lessons above
add up to the difference between v3’s summary claim “method fails on most pre-registered
hypotheses” and v5’s summary claim “method passes every pre-registered hypothesis with
statistically significant separation from baselines.”


12.8   Pilot scope

This pilot validates the conflict-aware grounding certificate (§5) on one public benchmark
with adversarial perturbations. It does not test (i) the Compositional Stability theorem (§9)

                                             51
at the multi-layer level or (ii) deployment in a regulated workflow. The other certificate
families have their own pilots reported elsewhere: Pilots B and B′ (embedding sensitivity) in
§7.4–§7.5, and Pilot C (Hoare-style agent action) in §8.5. The Pilot D family of Universal
Card validations (patent / technical-intelligence, legal, regulated-finance, and clinical variants)
remains forward work (§16.8).



13     Compiled Lean 4 Reference Artifact

The architecture is mechanized. The companion Lean 4 project (directory lean_artifact/)
compiles all 22 certificate types in the broader catalogue. The artifact builds in roughly
ten seconds with a warm Mathlib cache; Appendix C reproduces representative structures
verbatim, and Appendix D contains a representative excerpt of the #print axioms output
(the full audit is build-regenerated by EmbeddingSensitivity/AxiomAudit.lean).


13.1    Summary statistics

        22 certificate types • 46 audited declarations • 17 axiom-free • 29 with
                         Ω+oracles • 0 sorry • 0 native_decide


The 17 axiom-free declarations include the entire Hoare-style action certificate (state, struc-
tures, all safety theorems, concrete trajectory), the bulk of the self-consistency certificate, the
Curry–Howard SortedList and DistinctList structures, scope-of-validity, simpler CE-
GAR theorems, and six of the ten extended-catalogue types (negative-guarantee, provenance,
temporal, calibrated-abstention, diff, meta as definitions). These compile by kernel reduction
alone, with no axioms whatsoever in their transitive set. In the conditional-guarantee
hierarchy, this is the strongest possible status: the guarantee is unconditional modulo only
the Lean kernel itself.


What “axiom-free” does and does not mean. Axiom-freeness is a statement about
the proof’s discharge mechanism: every step reduces by kernel computation and pattern
matching, with no appeal to a named axiom (not even Lean’s foundational Ω). It is not a
statement that the encoded predicates are unconditionally meaningful in the real world. For
the Hoare action certificate, predicates such as owner = user or path is in sandbox
are human-authored definitions on the chosen state model; their semantic adequacy, that
they actually capture the real-world safety property the deployment intends, is a modeling
assumption beneath the trust boundary. Axiom-freeness rules out hidden mathematical
assumptions (no sorry, no native_decide, no Mathlib placeholder), but it does not rule
out specification errors in the predicate authors. A paraphrase: the certificate guarantees
“the kernel computed this property correctly”; it does not guarantee “the property is the right


                                                52
one.” This caveat applies to every axiom-free certificate in the artifact and is consistent with
the conditionality discussion of §16.1.


13.2   Artifact evaluation

Beyond the axiom audit, Table 5 reports concrete operational metrics. The numbers are
observable on commodity hardware (a 2024-class laptop) under Lean v4.30.0-rc2 with a
warm Mathlib cache; they are intended as order-of-magnitude reference points, not as a
benchmark.
The table substantiates two operational claims that the paper otherwise gestures at: (i) the
audit is genuinely small and portable (an external auditor needs only lean plus a < 100 LOC
wrapper, no model artifacts); (ii) per-call verification cost is dominated by the underlying
LLM call, not by the kernel re-check, so the overhead is amortizable in any production
setting. Operational measurements at production traffic, throughput under sustained load,
expert-panel agreement on abstentions, and catch rates against deployed pipelines, remain
explicit future work (§16).


13.3   Per-type axiom dependencies

Table 6 reports the axiom-dependency tier of every compiled certificate type. Two rows
in the table collapse to a single type for the purpose of the 22-type count: the two
Curry–Howard rows (sorted/distinct and parens/quote) share one type, and the Hoeffding
concentration row stands for one type parameterized over eight named concentration
inequalities (Hoeffding, generalized Hoeffding, Bernstein, empirical Bernstein, Azuma–
Hoeffding, Bennett, McDiarmid, union-bound) sharing one Lean structure with different
failure_bound. Net: 18 catalogue rows yield 17 distinct catalogue types; with 5 core
items (3 families and 2 operators), the total is 5 + 17 = 22.


13.4   What is conditional, what is closable

The persistent (tier-4) oracles in the artifact are ParaphraseOracle, SignedSupport
Oracle, DecompositionOracle, StepConfidenceOracle, IIDSamples. These can-
not be discharged by mathematics. Each carries a deployment-specific evaluation dis-
cipline: a paraphrase oracle’s faithfulness is supported by a held-out paraphrase bench-
mark; a signed-support oracle’s faithfulness by a held-out NLI calibration set; a de-
composition oracle’s faithfulness by reconstruction-pass rates. The remaining named
axioms (tiers 2 and 3: cauchy_schwarz_sq, innerProd_sub, HoeffdingInequality,
HashCollisionResistant, DecodeAlgorithmDeterministic) are closable as Math-
lib’s inner-product-space, probability, and cryptographic-hash libraries develop.
Proof-of-sampling discipline. For concentration certificates that depend on IIDSamples,
the framework treats IID sampling as a persistent tier-4 oracle rather than a mathematical fact.

                                              53
Table 5: Operational metrics for the compiled reference artifact. Numbers labeled measured
are observed on the artifact directly: module and declaration counts are exact; build and
audit times are reported on a 2024-class laptop with a warm Mathlib cache, rounded
conservatively. Numbers labeled projected are schema-derived estimates for components
currently specified but not yet compiled (notably the Universal Assurance Card consolidator);
their soundness depends on the focused engineering step in §16.4. Certificate and Card byte
sizes are computed from the field-record byte layout. Production-traffic throughput numbers
(latency under sustained load, batched-audit amortization, SNARK-compression overhead)
are deliberately not reported here and remain forward work (§16.2).

   Metric                                Value
  Source-level totals
  Modules                             25
  Top-level declarations audited      46
  Axiom-free declarations             17 / 46
  Persistent tier-4 oracles           5 (cf. Table 2)
  Mathematical placeholders (tier 2)  3            (cauchy_schwarz_sq,                  innerProd_sub,
                                      HoeffdingInequality)
   Cryptographic assumptions (tier 3) 2        (HashCollisionResistant,               DecodeAlgorithm
                                      Deterministic)
  Build and audit time
  lake build, warm Mathlib cache         ≈ 10 s
  lake build, cold Mathlib cache         ≈ 2 min (one-time, then cached)
  Per-cert kernel re-check (typical)     < 100 ms (sub-second for every leaf type)
  #print axioms on full artifact         <1s
  End-to-end audit over the 22 un-       ≈ 1 s on commodity hardware
  derlying compiled certificates (mea-
  sured)
  Projected end-to-end audit on a sin-   ≈ 1 s; consistency predicate is decide-discharged on a ∼30-field
  gle Universal Card (specified; once    record
  AssuranceCard.lean added)
  Certificate and card sizes
  Universal Assurance Card record        ≈ 1.5 KB JSON, ≈ 0.7 KB binary
  (typical, projected from schema)
  Embedding sensitivity certificate      a few KB; scales with |𝐺 inv | · 𝑑
  (per call)
  Bilattice grounding certificate (20    < 10 KB
  claims, 100 chunks)
  Hoare trajectory certificate (10 ac-   < 5 KB
  tions)
  Composite Lean proof terms             sub-KB to a few KB; SNARK-compressible to hundreds of bytes
                                         (catalogue)
  Audit infrastructure
  Reference              audit-runner    < 100 LOC
  (Python/Rust around lean)
  External dependencies for audit        Lean v4.30.0-rc2; SHA-256 implementation; nothing else
  Required input                         certificate file; Mathlib snapshot pin
  Not required for audit                 model weights, prompts, decoding parameters, random seeds


                                                       54
Table 6: Axiom-dependency tier for each compiled certificate type. “none” means no axioms
at all; Ω = {propext, Classical.choice, Quot.sound} are the kernel-trusted axioms
(tier 1). Named non-Ω axioms are tagged (t2) for tier-2 mathematical placeholders, (t3) for
tier-3 cryptographic assumptions, and (t4) for tier-4 ML/human oracles, per the hierarchy of
§3.4.

 Certificate                     Axiom dependency                               Section
 Three local certificate families
 Conflict-aware bilattice ground- Ω + SignedSupportOracle, DecompositionOracle §5
 ing                              (t4)
 Embedding sensitivity            Ω + ParaphraseOracle (t4) + cauchy_schwarz_sq, §7
                                  innerProd_sub (t2)
 Hoare agent action               none                                           §8
 Two operators on certificates
 Maximal Certifiable Residue      Ω                                             §6
 Compositional Stability (2-layer Ω                                             §9
 base lemma)
 Per-call deliverable
 Universal Assurance Card (spec- would    inherit    from      sub-certs   once §10
 ified)                          AssuranceCard.lean is added
 Extended catalogue (Appendix C)
 Self-consistency lattice        none                                           catalogue
 Chain-of-thought DAG            Ω + StepConfidenceOracle (t4)                  catalogue
 Curry–Howard (sorted/distinct) none                                            catalogue
 Curry–Howard (parens/quote)     Ω                                              catalogue
 Hoeffding concentration         Ω + HoeffdingInequality (t2) + IIDSamples (t4) catalogue
 Proof-of-sampling               HashCollisionResistant,      DecodeAlgorithm- catalogue
                                 Deterministic (t3)
 Scope-of-Validity               none                                           catalogue
 CEGAR repair loop               none / Ω                                       catalogue
 Negative-guarantee              none                                           catalogue
 Counterfactual                  Ω                                              catalogue
 Calibration                     Ω                                              catalogue
 Provenance                      none                                           catalogue
 Temporal validity               none                                           catalogue
 Budget composition              Ω                                              catalogue
 Calibrated abstention           none                                           catalogue
 Diff / incremental              none                                           catalogue
 Multi-hop reasoning             Ω                                              catalogue
 Meta / self-audit               none                                           catalogue




                                               55
A proof-of-sampling certificate supplies auditable evidence for that oracle: the deployment
records a declared temperature 𝑇 > 0, per-pass commitments over the random seed, the
decoder entry state, and the per-pass token-emission log, and a decidable no-state-carryover
predicate over those commitments. When strict no-state-carryover is unavailable, the
certificate may instead record a bounded-difference or martingale fallback, yielding an
Azuma–Hoeffding / McDiarmid-style discipline rather than an IID one. The certificate
populates the is_deterministic, sample_count, and proof_of_sampling fields of the
Universal Assurance Card, but it does not mathematically close the natural-language or
decoder-behavior oracle; rather, it gives the auditor structured commitments against which
the IIDSamples hypothesis can be operationally re-verified.
What the artifact proves (selected; full list in Appendix D): Theorem 7.4 (squared form,
embedding stability); Lemma 7.2 (variant-family monotonicity); Lemma 5.4 (emission gate
soundness for grounding, conditional on the NLI / decomposition oracles); the abstention-
reason and emit-when-supported lemmas; Lemma 9.2 (compositional stability, two-layer
base case; the 𝑛-layer Theorem 9.3 lifts by induction over the certified-layer list); Theorem 6.3
(MCR maximality, idempotence, fixed-point); per-step trajectory safety and p_chain for
Hoare; six concrete instantiations spanning a 3-D rational embedding, a clinical-RAG 3-claim
grounding example that abstains, a counter-state 3-step trajectory, a 5-sample consistency
example, four Curry–Howard structured outputs, and a 20-sample Hoeffding example.




                                               56
14     Threat Model and Adoption Order

14.1    Threats versus defender certificates

Table 7: Threats against LLM pipelines and the certificate types that defend each. Threats
marked ★ are the most frequent in production deployments today.

  Threat                                      Defender certificate(s)
  Hallucination (invented facts)★             Bilattice grounding (§5); self-consistency (catalogue);
                                              canonical-denotation decoding (catalogue).
  Silent contradiction★                       Bilattice grounding emission-gate (Lem 5.4) with 𝑊 − thresh-
                                              old; MCR drops the contradicted claim (§6).
  Prompt injection via retrieved content★     Semantic type system + non-interference (catalogue); ground-
                                              ing with source-role tagging.
  Variant flip (paraphrase attack)★           Embedding sensitivity (§7); compositional-stability budget
                                              (Thm 9.3).
  Unsafe tool invocation★                     Hoare action certificate (§8); budget composition (catalogue);
                                              rely-guarantee for parallel actions.
  Sample forgery (claimed 𝑘 samples)          Proof-of-sampling with committed seed (catalogue).
  Corpus tamper-detection (snapshot drift     Provenance + temporal validity (catalogue). Note: detects
  from committed hash)                        that the served corpus differs from the committed snapshot;
                                              does not certify that the snapshot is itself uncorrupted (corpus-
                                              level factuality is below the trust boundary).
  Vendor / model / prompt drift               Provenance certificate + composite-certificate diff (cata-
                                              logue).
  Fabricated compliance evidence (sorry-      Axiom audit against Ω (Def. 3.1); meta-certificate over kernel
  based cert)                                 hash.
  PII / forbidden content leakage             Negative-guarantee (catalogue); abstract-interpretation PII
                                              grammar (catalogue).
  Over-confident miscalibrated confidence     Calibration certificate; conformal prediction (catalogue).
  Unfaithful chain-of-thought (stated ≠ ac-   Cross-model CoT DAG verification; PRM step scoring; mech-
  tual)                                       interp axioms (catalogue).
  Audit tampering (binary swap of kernel)     Meta-certificate + reproducible build + signed kernel.


14.2    First certificate to ship

We recommend an adoption order chosen for low implementation cost relative to risk-reduction
value:

1. Embedding sensitivity (§7). Tractable; independent of downstream architecture; off-the-
   shelf paraphraser oracle; retrieval instability maps directly to financial / legal risk.
2. Conflict-aware grounding (§5). Highest hallucination-visibility; the signed-support
   arithmetic is straightforward; per-claim audit trails are immediately useful.
3. Hoare-style agent action (§8). Highest per-failure cost; “blocked at first unsafe step” is a
   compelling demo for decision-makers; precondition predicates usually exist in the policy
   layer.

                                                    57
4. Scope-of-validity + provenance. Low marginal cost given 1–3; large audit-trail gain.
5. Self-consistency + proof-of-sampling. Needed only when stochastic sampling is load-
   bearing.


14.3   A verifiability benchmark

LLM benchmarks today measure output quality. None measures verifiability. We propose a
complementary benchmark family on certificate coverage, audit independence, abstention
quality, contradiction-detection rate, failure-localization precision, certificate size, audit
time, and intervention latency for agents. Publishing a minimal instance on a public dataset
(HotpotQA for RAG; WebArena for agents) is a concrete near-term Stage 1 priority.


14.4   Cost: audit overhead vs. assurance-mode generation overhead

The cost story has two layers and they should not be conflated.


Audit overhead is small. Once a certificate has been generated, re-checking it is dominated
by the Lean kernel and the #print axioms pass. Per Table 5: per-cert kernel re-check is
typically < 100 ms, the full #print axioms pass is < 1 s, and an external audit-runner
is < 100 LOC of Python or Rust. This is the cost a regulator, downstream consumer, or
third-party verifier pays. It is genuinely small and portable.


Assurance-mode generation overhead can be materially higher. Producing a certificate,
in contrast, can require non-trivial extra work above the unaudited LLM call. A conflict-aware
grounding certificate may invoke the LLM (or a separate decomposer) to extract atomic
claims, then call an NLI model on every (claim, chunk) pair, then aggregate signed-support
scores. A paraphrase decision-margin certificate may run the encoder on |𝐺 inv | paraphrases.
A self-consistency certificate may sample the LLM 𝑘 times. A composite Universal Card-
shaped pipeline may run all of these. Empirically we have not measured these costs (§16.2),
but a rough upper bound is on the order of 5×–20× the unaudited generation cost in the
most assurance-heavy configurations, with significant variance by certificate family. Coarse
breakdown: grounding contributes most (𝑂 (𝑛 · 𝑚) NLI calls in atomic claims and chunks);
paraphrase and self-consistency contribute roughly multiplicatively in their sample/variant
counts; agent action and embedding sensitivity are nearly free above the baseline.


Where the framework pays for itself. The framework is designed for the regime where
this generation overhead is small relative to per-call error cost. Legal retrieval errors that
lead to malpractice claims, clinical recommendations that miss contraindications, agentic
actions that delete the wrong file, or fabricated compliance evidence in regulated workflows:
these are settings where a 10× generation cost is dwarfed by a single prevented incident.

                                             58
Creative writing, brainstorming, and casual question-answering do not clear that bar; for
them, assurance mode should not be enabled. ROI is therefore deployment-specific rather
than universal, and the case studies (§11) are illustrative of the regime where the framework’s
value proposition holds.


Storage and bandwidth. Certificate storage is KB–MB per call (sub-KB with SNARK
compression, an extension flagged in the catalogue). Card storage is ≈ 1.5 KB JSON per
call. These are negligible at any production scale.


14.5   Regulatory anchoring

The certificate taxonomy and the Universal Card map onto major frameworks (EU AI Act,
FDA SaMD, NIST AI RMF, ISO/IEC 42001, HIPAA, Federal Rules of Evidence 702
/ Daubert); the point is structural rather than detailed compliance, and a per-framework
correspondence is in Appendix F.


15     The Extended Catalogue

The compiled artifact’s 22 certificate types decompose as follows: five fully-compiled
core items, namely the three local certificate families (conflict-aware bilattice grounding,
embedding sensitivity, and Hoare-style agent action) and the two operators on certificates
(Maximal Certifiable Residue, and the two-layer base lemma of Compositional Stability);
the Universal Card consolidator is specified pending AssuranceCard.lean, and is not part
of the 22. To these five are added the 17 catalogue types listed in Table 6: self-consistency
lattice, chain-of-thought DAG, Curry–Howard structured output (compiled in two flavours,
sorted/distinct and parens/quote, counted as one type), Hoeffding concentration (the Lean
structure parameterized over eight named concentration inequalities; counted as one type),
proof-of-sampling, scope-of-validity, counterexample-guided repair (CEGAR), and ten
more (negative-guarantee, counterfactual, calibration, provenance, temporal validity, budget
composition, calibrated abstention, diff, multi-hop, meta-audit). Per-certificate dependencies
are in Table 6; one-paragraph descriptions and references in Appendix E; a representative
excerpt of the #print axioms output in Appendix D, with the build-regenerated full audit in
EmbeddingSensitivity/AxiomAudit.lean. Beyond the 22 compiled types, Appendix E
additionally describes types that are specified in narrative form, pending dedicated artifact
modules: a semantic type system for text with role non-interference, conformal prediction,
Markov-category compositional uncertainty, and five further extensions (spectral sensitivity,
abstract interpretation, canonical-denotation decoding, dual-model cross-verification, zero-
knowledge proof-carrying outputs). The catalogue is broad enough to fill a monograph,
but the core development of §§5–10 is what makes the framework operational; we do not
duplicate the catalogue in the main text.


                                              59
16     Limitations and Future Work

16.1    Conditionality is unavoidable

Every certificate is conditional on tier-4 ML / human oracles. A miscalibrated paraphraser
produces a sensitivity certificate whose max divergence is correct but materially misleading.
A tamper-sensitive retrieval corpus grounds well-formed hallucinations. The architecture
does not reach across the trust boundary; it disciplines it. The right characterization of
the benefit is not “no more hallucinations” but “hallucinations become named, localized,
reproducible events rather than opaque stochastic outputs.”


16.2    Empirical scope

The case studies in §11 use synthetic numbers, flagged at the top of that section. The empirical
evidence in this paper consists of (i) the Lean artifact’s measurements (proof sizes, build/audit
times, the per-cert axiom-set composition of Table 6); (ii) Pilot A (§12), a pre-registered
three-iteration test of the conflict-aware grounding certificate on HotpotQA dev distractor
with adversarial perturbations, in which all six v5 hypotheses pass against three baselines;
(iii) Pilots B and B′ (§7.4, §7.5), a pre-registered two-domain test of the embedding-sensitivity
certificate on the same benchmark in matched short-form and long-form settings: the central
inequality Δ2 > 0 holds in 20–30% of short adversarial queries but in 98–100% of long-form
paragraphs across every edit-type combination; and (iv) Pilot C (§8.5), a pre-registered
controlled-sandbox test of the Hoare-style agent-action certificate on a 5-task slice with 18
hand-curated direct-injection adversarial proposals (HC2/HC3/HC4/HC5 PASS, HC1 FAIL
with predicate-completeness diagnostic).


Stated limitations of the four pilots. (a) Domain coverage is HotpotQA dev distractor
(Pilots A/B/B′ ) and a controlled filesystem sandbox (Pilot C); patent / technical-intelligence,
legal, regulated-finance, and clinical replication of all three certificate families remains
forward work (§16.8). (b) Pilot B′ N is 64 effective queries (bootstrap CIs ≈ ±12pp), sized
to fit the available budget at the observed per-query cost for long-form variant generation
(§7.5); the result is therefore a strong directional finding on long-form rather than a narrow-CI
deployment claim, and is reported as such. (c) Pilot C scope is a 5-task registered slice (the
original 30-task plan was scaled to fit the available budget and the preliminary feasibility
schedule); breadth across more tasks, more tools, and more attack classes is forward work.
(d) Adversary coverage: Pilot A’s perturbations and Pilot C’s adversarial proposals are
hand-curated; LLM-driven adversary mining against held-out predicate / scope sets is a
natural follow-up. (e) Throughput economics: production-scale throughput numbers and
amortised audit-cost economics are forward work (§16.5).
Pilots A, B, and B′ are reported as a matched program on a shared benchmark with the same
panel discipline and pre-registration protocol; Pilot C runs on a separately-built filesystem


                                               60
sandbox under the same pre-registration discipline. The contrast across the four (Pilot A
positive grounding result; Pilots B/B′ empirical scope of the embedding inequality, with short-
form narrow and long-form essentially universal; Pilot C 38.9pp Treatment-over-deny-list
dominance with HC1’s predicate-completeness diagnostic) operationalizes the framework’s
intended posture: a certificate is soundness machinery whose deployment-readiness depends
on a per-call premise that must be measured per-encoder and per-input-class.

Table 8: Comparison of the HotpotQA pilots (A, B, B′ ). Primary results from §§12, 7.4–7.5;
scope limitations summarized from §16.2. Pilot C is reported separately in Table 9.

Pilot Certificate               𝑁          Primary verdict                    Key result
A      Bilattice grounding 264             H1–H6 all PASS (v5)         catch=1.0 at FBR=0.064; B1 cannot
       (§5)                                                            reach catch=1.0 below FBR=0.266
B      Embedding sensitivity, 209          HB1 narrow (30%/20% posi- median Δ2 = −0.07; (paraphrase,
       short-form (§7)                     tive)                       reorder)×attribute_flip cells fail;
                                                                       (surface, synonym)×(entity, nega-
                                                                       tion) cells reach 84–97%
B′     Embedding sensitivity, 64               ′
                                           HB 1 PASS (100%/98% posi- median Δ2 = +0.39; every edit-
       long-form (§7)                      tive); CP CI ⊇ [0.92, 1.00] type cell positive

    Scope limitations. Pilot A: HotpotQA-only; v3/v4 hypothesis revisions documented in §12.2. Pilot B:
adversarial short queries; deployment-narrow on this slice. Pilot B′ : 𝑁=64, strong directional finding rather than
                                        a narrow-CI deployment claim.



Table 9: Comparison row for Pilot C, the Hoare-style agent-action pilot. Primary results
from §8.5.

 Pilot Certificate                𝑁                     Primary verdict         Key result
 C      Hoare agent action 48 trajs (16/harness; HC2–HC5 PASS; 38.9pp Treatment-over-deny-list
        (§8)               18 unsafe-injection HC1 FAIL (12/18) dominance; 100% audit-log in-
                           probes per harness)                  formativeness; HC1 diagnostic
                                                                on 5 within-budget probes + 1
                                                                omitted predicate clause

Scope limitations. 5-task registered slice (the original 30-task plan was scaled to fit the available budget and
 preliminary feasibility schedule); hand-curated adversaries; LLM-driven adversary mining against held-out
                                        predicate sets is forward work.


Multiple-testing posture. The four pilots together register eighteen pre-registered hypothe-
ses (H1–H6 in Pilot A, six; HB1, HB2, and HB4 in Pilot B short-form, three, with HB3
retired during pre-registration revisions, see §7.4; HB′ 1–HB′ 4 in Pilot B′ long-form, four;
HC1–HC5 in Pilot C, five). Confidence intervals in this paper are reported per-hypothesis with
no family-wise correction; the proportion CIs are 95% bootstrap intervals (10,000-resample)
by default, and 95% Clopper–Pearson exact intervals where the bootstrap collapses to a
degenerate point (Pilot B′ B′ 1; see §7.5). We declare this posture explicitly so readers can

                                                       61
discount marginal results accordingly. We treat the pilots’ primary load-bearing hypotheses
as: H1 (catch-rate dominance, Pilot A), HB′ 1 (long-form inequality positivity, Pilot B′ , where
the certificate’s premise is the deployment claim), and HC3 (38.9pp Treatment-over-deny-list
dominance, Pilot C). The Pilot B short-form HB1 hypothesis is also pre-registered as a
primary, and its result is a scope-narrowing negative: the certificate remains sound, but
its premise holds in only 20–30% of cases on short adversarial queries. We do not list
it among the deployment-readiness primaries because the paper’s substantive B-family
deployment claim is carried by HB′ 1, not HB1. Pilot C HC2 and HC5 are small-denominator
descriptive instrumentation checks rather than deployment-readiness primaries: HC2 reports
0/6 false-blocks on benign destructive proposals (point estimate 0.000; 95% Clopper–Pearson
interval [0, 0.459]) and HC5 reports 13/13 audit-log informativeness on Treatment blocks
(1.000; CP 95% [0.753, 1.000]). Both pass the registered point-estimate criteria but, given
𝑛=6 and 𝑛=13, are not narrow-interval population claims; we report them as instrumentation
evidence supporting HC3 rather than as standalone load-bearing conclusions. Even with
a conservative Bonferroni adjustment over the three load-bearing primaries (three tests,
𝛼 = 0.05/3 ≈ 0.017 per test), the relevant intervals on Pilot A H1, Pilot B′ HB′ 1 long-form
(1.000 and 0.984 with Clopper–Pearson lower bounds 0.944 and 0.916), and Pilot C HC3
(38.9pp gap) clear the adjusted bar by wide margins. Readers with a stricter posture should
treat Pilot B short-form HB1, HB′ 2 / HB2 retrieval-flip-prediction F1, and HC1’s 12/13
in-scope diagnostic as the multiple-testing-fragile cells. None of the three load-bearing
primaries listed above sits within an interval whose lower bound would cross threshold under
any reasonable family-wise adjustment; the load-bearing conclusions are therefore robust to
the posture choice.
What remains explicit future work: the Pilot D family of Universal Card validations in
high-stakes domains (§16.8; patent / technical-intelligence, legal, regulated-finance, clinical),
domain-specific extensions of the long-form embedding result to those corpora, calibrated
post-bound construction to tighten the §7 certificate’s retrieval-flip prediction beyond the
loose F1 it achieves on raw drift, scaling Pilot C’s predicate registry beyond the 5-task
scaffolded slice to close the residual predicate-completeness gap, throughput at production
scale, and cost savings on prevented errors. Building public verifiability benchmarks across
these high-stakes domains is the Stage 1 priority of the research program.


16.3    Tier-2 and tier-3 axioms are closable

cauchy_schwarz_sq, innerProd_sub, and HoeffdingInequality reduce to Ω
once aligned with Mathlib’s evolving inner-product-space and probability libraries.
HashCollisionResistant and DecodeAlgorithmDeterministic reduce to Ω once
a SHA-256 (or substitute) Lean formalization is plugged in. None of these axioms is
structurally different from the Mathlib mathematical-axiom load that other formal-methods
deployments accept.




                                               62
16.4   Promoting the Universal Assurance Card from specified to compiled

The Universal Assurance Card schema and its VerdictConsistent predicate are presently
specified (§10): the structure, the four verdicts, and the consistency obligation are stated
in Lean form, but AssuranceCard.lean is not yet a module in lean_artifact/. The
promotion is mechanical: the predicate is decidable on Rat/Bool/List String fields with
no Mathlib-heavy lemmas required, and a worked example for each of the four verdicts
(matching the case studies in §11) closes via decide. We identify this promotion as a
focused next-step engineering exercise rather than research; once done, the artifact gains one
additional consolidator module (the count of compiled certificate types remains 22, since the
Card aggregates the 22 rather than adding a new type), and the overview table’s specified
status for the Card upgrades to compiled.


16.5   Throughput, generator overhead, decomposition assumption

Kernel type-checking is fast but not free; high-throughput LLM workflows (millions of
requests per day) amortize via batching, cached invariants, sampled audits, and SNARK
compression. Each certificate needs a generator; the right engineering response is a library
of reusable certificate kernels (arithmetic bounds, lattice aggregation, DAG propagation,
Hoeffding bound, metric-space Lipschitz). The decomposition principle applies where the
pipeline has enough structure to admit a theorem; pure end-to-end open-ended generation
is essentially untouchable beyond well-formedness, where the right behavior is graceful
degradation (Abstain under the policy with reason “task does not admit a certificate”).


16.6   Open research questions

(i) The right semantic type system for text across deployments. (ii) Whether abstract
interpretation gives useful over-approximations of LLM outputs at practical granularity.
(iii) Concentration bounds tailored to non-IID LLM sampling. (iv) Partial verification of
paraphrase oracles via curated thesauri. (v) Mechanistic interpretability [12, 14, 19, 46]
as named axioms in the chain. (vi) Multi-agent emergent-behavior certificates (liveness
of a multi-agent protocol; absence of collusive privilege escalation; cross-agent Byzantine
agreement). (vii) Game-theoretic adversarial semantics extending the decision-margin
certificates to a continuous adversary class. (viii) A relative-completeness theorem for the
framework (which pipeline properties are expressible vs. strictly beyond reach).


16.7   A staged research program

Stage 1 (Tooling).
   Reusable Lean 4 certificate kernels; an audit-runner integrating kernel type-check
   and #print axioms audit; reference LLM-wrapper integration; a public verifiability
   benchmark with adversarially-introduced contradictions.

                                             63
Stage 2 (Single-mechanism validation).
   Deploy embedding sensitivity, conflict-aware grounding, and Hoare action certificates in
   any high-stakes pipeline (patent claim charting, legal case-law retrieval, regulated-finance
   disclosure analysis, clinical RAG, or a sandboxed agent) and measure catch rates against
   an expert-panel ground truth.
Stage 3 (Composition).
   Build the composite Universal Card pipeline. Demonstrate end-to-end auditability with
   external auditors. Publish trust models and policy templates.
Stage 4 (Extensions).
   Prototype the semantic type system; explore abstract interpretation for output constraints;
   deploy proof-carrying outputs with and without SNARK compression in at least one
   high-stakes setting.


16.8    Pilot status

The framework’s three local certificate families (grounding, embedding sensitivity, agent
action) admit empirical pilots at parallel levels of importance.

Pilot A (conflict-aware grounding, §12): complete. Six pre-registered hypotheses,
all PASS under the v5 wording, on a 264-example perturbed slice and a 203-example
refusal-excluded unperturbed slice. The bilattice’s catch=1.0/FBR=0.064 operating point is
unreachable for the cosine-similarity baseline at any threshold.

Pilot B (embedding sensitivity, short-form, §7.4): complete. A pre-registered 𝑁=209
slice on text-embedding-3-large and sentence-transformers-mpnet establishes that on short
adversarial multi-hop QA the §7 inequality Δ2 > 0 holds in only 30% / 20% of queries
(FAIL ≥ 0.80 / ≥ 0.60). Panel reliability is high (𝜅 = 0.887, unanimous 0.95). A Phase 1
edit-type ablation localizes the failure to (paraphrase, reorder) × attribute_flip while (surface,
synonym) × (entity_swap, negation) cells reach 84–97% positive.

Pilot B′ (embedding sensitivity, long-form, §7.5): complete. A matched pre-registered
𝑁=64 slice with the query unit shifted from multi-hop questions to gold supporting paragraphs
(median ≈110 tokens) shows the inequality holds in 100% / 98% of queries on the same two
encoders, across every edit-type combination (median Δ2 = +0.39 vs −0.07 short-form). The
certificate is therefore sound on every input length and empirically supported on long-form
text. The retrieval-flip-prediction F1 remains loose (0.13–0.15) on both pilots: the bound
holds, but is not tight enough to predict which paraphrases will flip top-𝑘 retrieval.

Pilot C (Hoare action certificates, §8.5): complete. A pre-registered controlled filesystem-
sandbox benchmark of 48 trajectories (16 per harness, comprising 11 adversarial trajectories

                                               64
carrying 18 spliced direct-injection unsafe-action proposals plus 5 benign trajectories
carrying 6 destructive-but-permitted proposals) across three harnesses (Unaudited, Deny-list,
Treatment). Treatment blocks 12/18 injected unsafe actions (66.7%); Deny-list blocks
5/18 (27.8%); Unaudited 0/18 (0%, structural floor). The 38.9pp Treatment-over-Deny-list
gap is well above the registered 15pp threshold (HC3 PASS). False-block rate on benign
destructive proposals is 0.000 on all three harnesses (HC2 PASS). Audit-log informativeness
on Treatment blocks is 1.000 (13/13, HC5 PASS). HC1 verdict: FAIL (block rate 12/18
against the registered ≥ 0.95 threshold), with a predicate-completeness diagnostic from the
audit log: 5 of the 6 unblocked attacks are within-budget delete probes that the registered
task t02 budget predicate correctly permits (the 6th attempt, which exceeds the budget, is
correctly blocked); the remaining 1 is a mtime-violating move probing a predicate that task
t01’s mv declaration deliberately omits. The Lean-checked soundness theorem is unaffected.
The empirical signal localizes exactly which predicate clauses to extend per-task.
A Pilot D family of Universal Card validations remains forward work. Each variant below
is independently scoped, and any one is a complete next-step empirical contribution. The
framework targets deployments where per-call error cost exceeds per-call verification cost
by roughly an order of magnitude (§1.4); validating the Universal Assurance Card against
expert-gold annotation in any such domain is the natural follow-on to the present paper. The
four pilots already completed validate the underlying certificates; a Pilot D in any high-stakes
domain validates the consolidator: whether the Card’s four-verdict output (Certified,
Partial, Residue, Abstain), once an application policy is applied, agrees with what a
domain expert would say should happen on real queries.


Pilot D-Patents (technical intelligence and IP). 100–300 prior-art and freedom-to-operate
queries with patent-attorney or technology-scout annotation of the gold retrieval-and-claim
gate; measures Card-verdict agreement on Residue cases (e.g., partial novelty findings
where some claim elements are anticipated and others are not) and Abstain precision on
queries where the corpus contains contradictory teachings. The bilattice grounding certificate
(§5) is particularly well-suited to patent claim charting, where one prior-art reference can
simultaneously support and refute different elements of the same independent claim.


Pilot D-Legal (case-law retrieval and brief support). 100–200 case-law queries with
attorney annotation; measures Residue agreement on holdings that are partially supported and
Abstain precision on queries spanning circuit splits, where contradiction-aware grounding
(§5) and embedding sensitivity on long-form text (§7.5, where the certificate’s premise holds
at 98–100%) are jointly load-bearing.


Pilot D-Finance (regulated research and disclosure analysis). 100–200 queries against
SEC filings, regulatory text, and internal compliance corpora, with compliance-officer
annotation; measures Card behavior on temporal-validity boundaries (a 10-K is fresh for


                                              65
a quarter, a regulation is fresh until amendment) and on action-gate residues for analyst-
recommendation pipelines.


Pilot D-Clinical (decision support). 50–200 clinical-RAG queries with board-certified-
clinician annotation of the gold action gate; measures Card-verdict agreement on Residue
cases (partial recommendations with one contraindicated element, the §11.1 case study made
empirical) and Abstain precision.
Each variant requires its own annotation infrastructure and is independent of the others;
collaborators in any of these domains can run a single variant without the others being in
flight. The patent / technical-intelligence variant is the natural first reported, given existing
infrastructure in that domain (the precursor’s home territory [37]); the framework’s value
proposition does not depend on which variant runs first.


Pacing. Pilots A, B, and B′ all run on HotpotQA dev distractor (§12, §7.4, §7.5); the
shared-benchmark design controls cross-pilot comparisons between the two HotpotQA-
applicable certificate families and between the two input classes (short-form questions vs.
long-form paragraphs). Pilot C (§8.5) runs on a separately-built controlled filesystem sandbox
because the Hoare-action threat model targets agentic side effects rather than retrieval /
answer generation. Each Pilot D variant requires its own domain-specific expert-annotation
infrastructure (patent-attorney, attorney, compliance-officer, or board-certified-clinician
annotation), none of which is built by any of the four existing pilots.


Near-term empirical roadmap. For readers wanting an ordered list of the smallest-
scope empirical work that would extend this paper’s findings, four items are concrete
and independent. (R1) Pilot D-Patents. A 100–300 prior-art / freedom-to-operate slice
with patent-attorney or technology-scout annotation; this is the natural first variant given
existing infrastructure in that domain (the precursor’s home territory [37]) and exercises the
bilattice grounding certificate on real multi-reference contradictions. (R2) Encoder/dataset
characterization for the embedding inequality. A targeted run on two to four additional
encoders (Cohere embed-v3, BGE, E5, Voyage) and two to three additional corpora (a
clinical-guideline corpus, a regulatory-text corpus, a scientific-abstract corpus), reporting
Δ2 > 0 rates with Clopper–Pearson intervals at matched short-form / long-form input
lengths; the cost is dominated by panel labeling on the new corpora (the run script itself is
parameterized over 𝑛 encoders today, §7.4). (R3) Pilot C predicate-registry expansion.
Extending the Pilot C task slate from 5 tasks to 15–30 tasks with broader predicate clauses
(mtime invariants on mv, finer-grained budget predicates) directly addresses the HC1 audit-log
diagnostic and would convert the registered FAIL into a registered PASS on the strictest
95% threshold. (R4) AssuranceCard.lean promotion. Adding the consolidator module
to lean_artifact/ upgrades the Universal Card from specified to compiled; the proof
obligations are decidable on Rat/Bool/List String and discharge by decide, so the work
is mechanical engineering rather than research (§16.4). Items (R1) and (R3) are the most

                                               66
informative empirical extensions; (R2) is the fastest to deploy on existing infrastructure; (R4)
is the most self-contained and is the only item under the formal-method team’s unilateral
control. Any of the four is a complete, citable next-step contribution.


17     Conclusion

The thesis, restated declaratively: the framework verifies the deterministic structured
computations surrounding an LLM rather than the model itself, with the trust boundary
pushed as far toward the raw input as possible and everything beyond it made deterministic,
checkable, and auditable.

This paper extends the patent-analysis architecture of [37] from a single specialized domain
to the generic interfaces of LLM pipelines. The trust-boundary architecture, certificate-
validity definition, and verification-status convention are inherited unchanged. The technical
contribution is three local certificate families developed end to end (conflict-aware bilattice
grounding, embedding sensitivity / paraphrase stability, and Hoare-style agent action) and
two operators on those certificates (Maximal Certifiable Residue, which turns abstention
into a maximal constraint-satisfying subset of an answer, and Compositional Stability, which
takes the per-layer gains and margins from the three families and produces a closed-form
pipeline-wide perturbation budget), consolidated into a per-call deliverable, the Universal
Assurance Card (declared as a Lean structure with a decidable consistency predicate, specified
pending the addition of AssuranceCard.lean to the artifact), with one new impossibility
conjecture (calibration without ground truth). The compiled Lean 4 reference artifact spans
all 22 certificate types of the broader framework with 17 of 46 declarations axiom-free and
zero uses of sorry. Four pre-registered empirical pilots cover all three certificate families:
Pilot A on conflict-aware grounding (§12), Pilots B and B′ on embedding sensitivity in
matched short-form and long-form settings (§7.4, §7.5), and Pilot C on Hoare-style agent
action (§8.5).
The contribution is principally architectural; the empirical contribution is that all three
certificate families were measured pre-registered against panel-validated or directly-injected
adversarial inputs on shared infrastructure. The framework does not claim superior perfor-
mance on every benchmark. The claim, now empirically demonstrated, is that a principled
decomposition leaves behind a formally verifiable core at every interface where an LLM
output becomes structured enough to admit a theorem; that the core is small, but its presence
changes the trust profile qualitatively; that localized diagnostic failures replace opaque errors;
that independent re-verification replaces vendor lock-in; and that abstention becomes a first-
class outcome with an explicit residue. Pilot A demonstrates one operationally meaningful
instance: the bilattice grounding certificate reaches an operating point that cosine-similarity
baselines cannot reach for any threshold. Pilots B and B′ demonstrate the framework’s
intended epistemic posture in two-domain form: a sound certificate whose premise narrows
on adversarial short queries and is essentially universal on long-form retrieval, with the


                                               67
failure mode mechanically explicable (surface-form bias on short queries) and the scope
of applicability operationalized as a deployment-readiness signal in the Universal Card.
Pilot C demonstrates the Hoare-action family’s gating value on a controlled adversarial-
injection benchmark, the typed-guarantee analogue of Pilot A’s positive operating-point result.
Whether the approach improves practitioner outcomes more broadly remains empirical and
requires the tooling, benchmarks, and Lean developments identified as future work. The
Pilot D family (§16.8) names four parallel domain validations of the Universal Assurance
Card consolidator (patent / technical-intelligence, legal, regulated-finance, and clinical), any
one of which is an independent next-step empirical contribution; collaborators in any of
these domains can run a single variant without the others being in flight. The method itself is
the precursor’s decomposition principle at the finer granularity of generic LLM pipelines,
and where per-call error cost exceeds per-call verification cost by an order of magnitude or
more, the shift is qualitative rather than incremental.


Code and data availability

Public archive. The compiled Lean 4 reference artifact and the four pilot directories are pub-
licly archived at https://github.com/gkoomullil/proof-carrying-certificates
and citable via concept DOI 10.5281/zenodo.20144140 (this paper’s v1.0.0 snapshot is
pinned at version DOI 10.5281/zenodo.20144139). The archive is distributed under the
PolyForm Noncommercial 1.0.0 license; commercial use requires a separate license from the
author.


Artifact archive. The archive layout is lean_artifact/ (the compiled Lean 4 project)
and pilot_a/, pilot_b/, pilot_c/ (one self-contained Python project per pilot, with
Pilot B′ co-located in pilot_b/).


Lean      4     artifact    pins. Toolchain:           leanprover/lean4:v4.30.0-rc2
(recorded      in     lean_artifact/lean-toolchain).                        Mathlib       com-
mit:            ee3a5404e56808aacf7393507153cc97ff28141a                    (recorded        in
lean_artifact/lake-manifest.json alongside the pinned commits of all transitive
packages, including batteries, aesop, Qq, plausible, proofwidgets, importGraph,
and LeanSearchClient). Reproduction: lake exe cache get pulls the pre-built
Mathlib oleans, then lake build compiles every module. The build emits one #print
axioms message per audited declaration via EmbeddingSensitivity/AxiomAudit.lean;
redirecting that output to a file yields the full per-declaration audit (a superset of the
representative excerpt in Appendix D). The build artifact is fully deterministic; any deviation
from the published audit (in particular sorryAx or Lean.ofReduceBool appearing)
indicates a compilation regression.



                                              68
Pilot    pins      (Pilot   A,     conflict-aware     grounding). Python:         see
pilot_a/requirements.txt (anthropic ≥0.40.0, openai ≥1.50.0, google-genai ≥0.3.0,
numpy ≥2.0.0, requests ≥2.31.0). Models (recorded in pilot_a/src/config.py): gener-
ator claude-sonnet-4-5; decomposer gemini-2.5-flash-lite; NLI / perturber / fail-
mode-B / decomposition-sensitivity model and primary judge gpt-5; panel models gpt-5,
claude-sonnet-4-5, gemini-2.5-pro; embedding text-embedding-3-small.
Decoding: temperature = 0.0 throughout. Seeds: dataset draws are deterministic
functions of seeds 42 and 11 (see pilot_a/src/data.py). API access dates and per-call
cached responses are stored under pilot_a/cache/ and pinned to the run that produced
pilot_a/results/.


Pilot   pins    (Pilots   B     and     B′ ,   embedding       sensitivity). Encoders
(pilot_b/src/config.py):              openai-text-embedding-3-large            (3072-
dim);       sentence-transformers/all-mpnet-base-v2              (768-dim,     local);
cohere-embed-english-v3 (1024-dim, parameterized but disabled in the reported
run for budget reasons). Variant generator: gpt-5. Three-judge validation panel:
claude-sonnet-4-5, gpt-5-mini, gemini-2.5-flash. Decoding: temperature =
0.0. Per-pair embedding outputs and per-judge votes are cached under pilot_b/cache/
and pilot_b/data/.


Pilot pins (Pilot C, Hoare agent action). Agent and injector models
(pilot_c/src/config.py): gpt-5; panel model gpt-5-mini. Decoding: temperature
= 0.0 (set in pilot_c/src/agent.py). Agent transcripts, audit logs, and per-trajectory
records are stored under pilot_c/results/; the harness recreates a per-trajectory
pilot_c/sandbox_runs/ working directory on each run.


Reproducibility flow. For each pilot, python scripts/run_full_pilot.sh (Pilot C)
or the equivalent run_*.py entry points (Pilots A, B) re-execute the registered analysis from
cached API responses and emit the primary tables and confidence intervals reported in the
body. The cached-response policy is monotone-build: cached responses are the source of
record; a missing cache entry reissues the API call and populates the cache; existing entries
are never re-issued. The Lean artifact lake build is independent of any external API and
is bit-exact under the pinned toolchain. The license accompanying the archive is recorded in
LICENSE.


Acknowledgments

This paper builds directly on the hybrid AI + Lean 4 architecture of [37]; the trust-boundary
discipline, the certificate-validity definition (kernel type-check plus Ω-audit), and the four-tier



                                                69
verification-status convention are inherited unchanged. We thank the Lean 4 and Mathlib
communities for the mathematical infrastructure that makes this line of work feasible.


References
 [1] Mohammed Alshiekh, Roderick Bloem, Rüdiger Ehlers, Bettina Könighofer, Scott
     Niekum, and Ufuk Topcu. Safe reinforcement learning via shielding. In Proceedings of
     the AAAI Conference on Artificial Intelligence, pages 2669–2678. AAAI Press, 2018.
 [2] Anastasios N. Angelopoulos and Stephen Bates. Conformal prediction: A gentle
     introduction. Foundations and Trends in Machine Learning, 16(4):494–591, 2023.
 [3] Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. Formal certification
     of code-based cryptographic proofs. In Proceedings of the 36th Annual ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages (POPL), pages 90–101.
     ACM, 2009.
 [4] Nuel D. Belnap. A useful four-valued logic. In J. Michael Dunn and George Epstein,
     editors, Modern Uses of Multiple-Valued Logic, pages 5–37. Reidel, Dordrecht, 1977.
 [5] Bernd Bohnet, Vinh Q. Tran, Pat Verga, Roee Aharoni, Daniel Andor, Livio Baldini
     Soares, Massimiliano Ciaramita, Jacob Eisenstein, et al. Attributed question answer-
     ing: Evaluation and modeling for attributed large language models. arXiv preprint
     arXiv:2212.08037, 2022.
 [6] Stéphane Boucheron, Gábor Lugosi, and Pascal Massart. Concentration Inequalities:
     A Nonasymptotic Theory of Independence. Oxford University Press, Oxford, 1st edition,
     2013.
 [7] Samuel R. Bowman, Gabor Angeli, Christopher Potts, and Christopher D. Manning. A
     large annotated corpus for learning natural language inference. In Proceedings of the
     2015 Conference on Empirical Methods in Natural Language Processing (EMNLP),
     pages 632–642. Association for Computational Linguistics, 2015.
 [8] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla
     Dhariwal, Arvind Neelakantan, Pranav Shyam, et al. Language models are few-shot
     learners. In Advances in Neural Information Processing Systems 33 (NeurIPS 2020),
     volume 33, pages 1877–1901. Curran Associates, Inc., 2020.
 [9] Mario Carneiro. Lean4Lean: Verifying a typechecker for Lean, in Lean. arXiv preprint
     arXiv:2403.14064, 2024.
[10] Marco Casadio, Tanvi Dinkar, Ekaterina Komendantskaya, Luca Arnaboldi, Matthew L.
     Daggitt, Omri Isac, Guy Katz, Verena Rieser, and Oliver Lemon. NLP verification: To-
     wards a general methodology for certifying robustness. arXiv preprint arXiv:2403.10144,
     2024.

                                            70
[11] Jeremy M. Cohen, Elan Rosenfeld, and J. Zico Kolter. Certified adversarial robustness
     via randomized smoothing. In Proceedings of the 36th International Conference on
     Machine Learning (ICML), pages 1310–1320. PMLR, 2019.

[12] Arthur Conmy, Augustine N. Mavor-Parker, Aengus Lynch, Stefan Heimersheim,
     and Adrià Garriga-Alonso. Towards automated circuit discovery for mechanistic
     interpretability. In Advances in Neural Information Processing Systems 36 (NeurIPS
     2023). Curran Associates, Inc., 2023.

[13] Patrick Cousot and Radhia Cousot. Abstract interpretation: A unified lattice model for
     static analysis of programs by construction or approximation of fixpoints. In Conference
     Record of the Fourth ACM Symposium on Principles of Programming Languages
     (POPL), pages 238–252. ACM, 1977.

[14] Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert Huben, and Lee Sharkey.
     Sparse autoencoders find highly interpretable features in language models. arXiv
     preprint arXiv:2309.08600, 2023.

[15] Joseph W. Cutler, Craig Disselkoen, Aaron Eline, Shaobo He, Kyle Headley, Michael
     Hicks, Kesha Hietala, Eleftherios Ioannidis, et al. Cedar: A new language for expressive,
     fast, safe, and analyzable authorization. Proceedings of the ACM on Programming
     Languages, 8(OOPSLA1):670–697, 2024.

[16] Nicolaas Govert de Bruijn. A survey of the project AUTOMATH. In Jonathan P. Seldin
     and J. Roger Hindley, editors, To H. B. Curry: Essays on Combinatory Logic, Lambda
     Calculus and Formalism, pages 579–606. Academic Press, New York, 1980.

[17] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In André Platzer and Geoff Sutcliffe, editors, Automated Deduction – CADE
     28, volume 12699 of Lecture Notes in Computer Science, pages 625–635, Cham, 2021.
     Springer. doi: 10.1007/978-3-030-79876-5_37.

[18] Edsger W. Dijkstra. A Discipline of Programming. Prentice-Hall, Englewood Cliffs,
     NJ, 1976.

[19] Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben
     Mann, Amanda Askell, Yuntao Bai, et al. A mathematical framework for transformer
     circuits. Transformer Circuits Thread, 2021.

[20] Allyson Ettinger. What BERT is not: Lessons from a new suite of psycholinguistic
     diagnostics for language models. Transactions of the Association for Computational
     Linguistics, 8:34–48, 2020.

[21] Tobias Fritz. A synthetic approach to Markov kernels, conditional independence and
     theorems on sufficient statistics. Advances in Mathematics, 370:107239, 2020.



                                             71
[22] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai,
     Jiawei Sun, Meng Wang, and Haofen Wang. Retrieval-augmented generation for large
     language models: A survey. arXiv preprint arXiv:2312.10997, 2023.

[23] Timon Gehr, Matthew Mirman, Dana Drachsler-Cohen, Petar Tsankov, Swarat Chaud-
     huri, and Martin Vechev. AI2: Safety and robustness certification of neural networks
     with abstract interpretation. In 2018 IEEE Symposium on Security and Privacy (SP),
     pages 3–18. IEEE Computer Society, 2018.

[24] Matthew L. Ginsberg. Multivalued logics: A uniform approach to reasoning in artificial
     intelligence. Computational Intelligence, 4(3):265–316, 1988.

[25] Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and
     Mario Fritz. Not what you’ve signed up for: Compromising real-world LLM-integrated
     applications with indirect prompt injection. In Proceedings of the 16th ACM Workshop
     on Artificial Intelligence and Security (AISec ’23), pages 79–90. ACM, 2023.

[26] Mohammadhosein Hasanbeig, Alessandro Abate, and Daniel Kroening. Cautious
     reinforcement learning with logical constraints. In Proceedings of the 19th International
     Conference on Autonomous Agents and Multiagent Systems (AAMAS), pages 483–491.
     IFAAMAS, 2020.

[27] C. A. R. Hoare. An axiomatic basis for computer programming. Communications of
     the ACM, 12(10):576–580, 1969. doi: 10.1145/363235.363259.

[28] Wassily Hoeffding. Probability inequalities for sums of bounded random variables.
     Journal of the American Statistical Association, 58(301):13–30, 1963.

[29] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang,
     Qianglong Chen, Weihua Peng, et al. A survey on hallucination in large language models:
     Principles, taxonomy, challenges, and open questions. arXiv preprint arXiv:2311.05232,
     2023.

[30] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin
     Bang, Delong Chen, Wenliang Dai, Andrea Madotto, and Pascale Fung. Survey of
     hallucination in natural language generation. ACM Computing Surveys, 55(12):1–38,
     2023. doi: 10.1145/3571730.

[31] Robin Jia, Aditi Raghunathan, Kerem Göksel, and Percy Liang. Certified robustness to
     adversarial word substitutions. In Proceedings of the 2019 Conference on Empirical
     Methods in Natural Language Processing and the 9th International Joint Conference
     on Natural Language Processing (EMNLP-IJCNLP), pages 4129–4142. Association
     for Computational Linguistics, 2019.

[32] Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Timothée Lacroix, Jiacheng Liu, Wenda
     Li, Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove:

                                             72
     Guiding formal theorem provers with informal proofs. In The Eleventh International
     Conference on Learning Representations (ICLR), 2023.

[33] Cliff B. Jones. Specification and design of (parallel) programs. In Information
     Processing 83, Proceedings of the IFIP 9th World Computer Congress, pages 321–332.
     North-Holland, 1983.

[34] Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Federico
     Olmedo. Weakest precondition reasoning for expected runtimes of randomized algo-
     rithms. Journal of the ACM, 65(5):30:1–30:68, 2018.

[35] Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey
     Edunov, Danqi Chen, and Wen-tau Yih. Dense passage retrieval for open-domain ques-
     tion answering. In Proceedings of the 2020 Conference on Empirical Methods in Natural
     Language Processing (EMNLP), pages 6769–6781. Association for Computational
     Linguistics, 2020. doi: 10.18653/v1/2020.emnlp-main.550.

[36] Nora Kassner and Hinrich Schütze. Negated and misprimed probes for pretrained
     language models: Birds can talk, but cannot fly. In Proceedings of the 58th Annual
     Meeting of the Association for Computational Linguistics, pages 7811–7818. Association
     for Computational Linguistics, 2020.

[37] George Koomullil. Formally verified patent analysis via dependent type theory:
     Machine-checkable certificates from a hybrid AI + Lean 4 pipeline. arXiv preprint
     arXiv:2604.18882, April 2026.

[38] Dexter Kozen. Semantics of probabilistic programs. Journal of Computer and System
     Sciences, 22(3):328–350, 1981. doi: 10.1016/0022-0000(81)90036-2.

[39] Tamera Lanham, Anna Chen, Ansh Radhakrishnan, Benoit Steiner, Carson Denison,
     Danny Hernandez, Dustin Li, Esin Durmus, et al. Measuring faithfulness in chain-of-
     thought reasoning. arXiv preprint arXiv:2307.13702, 2023.

[40] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
     Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian
     Riedel, and Douwe Kiela. Retrieval-augmented generation for knowledge-intensive
     NLP tasks. In Advances in Neural Information Processing Systems 33 (NeurIPS 2020),
     volume 33, pages 9459–9474. Curran Associates, Inc., 2020.

[41] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy
     Lee, Jan Leike, John Schulman, et al. Let’s verify step by step. arXiv preprint
     arXiv:2305.20050, 2023.

[42] Potsawee Manakul, Adian Liusie, and Mark J. F. Gales. SelfCheckGPT: Zero-resource
     black-box hallucination detection for generative large language models. In Proceedings
     of the 2023 Conference on Empirical Methods in Natural Language Processing

                                            73
     (EMNLP), pages 9004–9017. Association for Computational Linguistics, 2023. doi:
     10.18653/v1/2023.emnlp-main.557.
[43] Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh,
     Mohit Iyyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. FActScore: Fine-grained
     atomic evaluation of factual precision in long form text generation. In Proceedings
     of the 2023 Conference on Empirical Methods in Natural Language Processing
     (EMNLP), pages 12076–12100. Association for Computational Linguistics, 2023. doi:
     10.18653/v1/2023.emnlp-main.741.
[44] George C. Necula. Proof-carrying code. In Proceedings of the 24th ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages (POPL), pages 106–119.
     ACM, 1997.
[45] Peter W. O’Hearn. Resources, concurrency, and local reasoning. Theoretical Computer
     Science, 375(1–3):271–307, 2007. doi: 10.1016/j.tcs.2006.12.035.
[46] Chris Olah, Nick Cammarata, Ludwig Schubert, Gabriel Goh, Michael Petrov, and
     Shan Carter. Zoom in: An introduction to circuits. Distill, 5(3), 2020.
[47] Fábio Perez and Ian Ribeiro. Ignore previous prompt: Attack techniques for language
     models. arXiv preprint arXiv:2211.09527, 2022.
[48] Victor Quach, Adam Fisch, Tal Schuster, Adam Yala, Jae Ho Sohn, Tommi S. Jaakkola,
     and Regina Barzilay. Conformal language modeling. arXiv preprint arXiv:2306.10193,
     2023.
[49] Nils Reimers and Iryna Gurevych. Sentence-BERT: Sentence embeddings using
     Siamese BERT-networks. In Proceedings of the 2019 Conference on Empirical
     Methods in Natural Language Processing and the 9th International Joint Conference
     on Natural Language Processing (EMNLP-IJCNLP), pages 3982–3992. Association
     for Computational Linguistics, 2019.
[50] Patrick M. Rondon, Ming Kawaguchi, and Ranjit Jhala. Liquid types. In Proceedings
     of the 29th ACM SIGPLAN Conference on Programming Language Design and
     Implementation (PLDI), pages 159–169. ACM, 2008.
[51] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke
     Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models
     can teach themselves to use tools. In Advances in Neural Information Processing
     Systems 36 (NeurIPS 2023), volume 36. Curran Associates, Inc., 2023.
[52] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-
     Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Fournet, et al. Dependent
     types and multi-monadic effects in F*. In Proceedings of the 43rd Annual ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL),
     pages 256–270. ACM, 2016.

                                          74
[53] The Mathlib Community. The Mathlib4 mathematics library for Lean 4, 2025. Software
     repository, leanprover-community/mathlib4.
[54] Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman. Language models
     don’t always say what they think: Unfaithful explanations in chain-of-thought prompting.
     In Advances in Neural Information Processing Systems 36 (NeurIPS 2023), volume 36.
     Curran Associates, Inc., 2023.
[55] Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton-Jones.
     Refinement types for Haskell. In Proceedings of the 19th ACM SIGPLAN International
     Conference on Functional Programming (ICFP), pages 269–282. ACM, 2014.
[56] Aladin Virmaux and Kevin Scaman. Lipschitz regularity of deep neural networks:
     Analysis and efficient estimation. In Advances in Neural Information Processing
     Systems 31 (NeurIPS 2018). Curran Associates, Inc., 2018.
[57] Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. Algorithmic Learning in a
     Random World. Springer, New York, 1st edition, 2005.
[58] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan
     Chen, Jiakai Tang, et al. A survey on large language model based autonomous agents.
     Frontiers of Computer Science, 18(6):186345, 2024. doi: 10.1007/s11704-024-40231-1.
[59] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang,
     Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought
     reasoning in language models. In Proceedings of the 11th International Conference on
     Learning Representations (ICLR), 2023.
[60] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia,
     Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning
     in large language models. In Advances in Neural Information Processing Systems 35
     (NeurIPS 2022), volume 35, pages 24824–24837. Curran Associates, Inc., 2022.
[61] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan
     Salakhutdinov, and Christopher D. Manning. HotpotQA: A dataset for diverse,
     explainable multi-hop question answering. In Proceedings of the 2018 Conference
     on Empirical Methods in Natural Language Processing (EMNLP), pages 2369–2380.
     Association for Computational Linguistics, 2018.
[62] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
     and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In
     Proceedings of the 11th International Conference on Learning Representations (ICLR),
     2023.
[63] Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, and Matt
     Fredrikson. Universal and transferable adversarial attacks on aligned language models.
     arXiv preprint arXiv:2307.15043, 2023.


                                             75
A      Notation

Symbols used in the paper, in roughly the order they appear.

Symbol                       Meaning
Trust boundary and certificate validity
Ω                          Trusted axiom set {propext, Classical.choice, Quot.sound}.
Ax                         Set of declared named tier-4 oracles for a given certificate.
𝑉 (𝑐)                      Validity check on a certificate 𝑐: kernel type-check plus #print axioms ⊆ Ω ∪ Ax.
Embedding sensitivity (§7)
𝐸                          Embedding map from text to ℝ𝑑 with 𝐿 2 -normalized output.
𝐺 inv (𝑥)                  Declared finite family of meaning-invariant perturbations of 𝑥.
𝐺 sig (𝑥)                  Declared finite family of meaning-changing perturbations of 𝑥.
   2 (𝑥)
𝑅inv                       max 𝑥 ′ ∈𝐺inv ( 𝑥 ) ∥𝐸 (𝑥 ′ ) − 𝐸 (𝑥)∥ 2 . Meaning-invariant robustness radius (squared).
   2 (𝑥)
𝑅sig                       min 𝑥 ′ ∈𝐺sig ( 𝑥 ) ∥𝐸 (𝑥 ′ ) − 𝐸 (𝑥)∥ 2 . Critical sensitivity floor (squared).
Δ2 (𝑥)                      2 (𝑥) − 𝑅 2 (𝑥). Selective gap; Δ2 > 0 certifies local separation of meaning.
                           𝑅sig            inv
𝜃 ret                      Retrieval similarity threshold (cutoff above which a document is returned).
Conflict-aware bilattice grounding (§5)
𝜎+ , 𝜎 − , 𝜎0               Three-way NLI signature per (claim, chunk) pair: entailment, refutation, neutral.
𝛽+ (𝑐), 𝛽 − (𝑐)             Per-claim signed-support scores aggregated across chunks.
𝑊 +, 𝑊 − , 𝑊 ±, 𝑊 ?         Mass aggregates over atomic claims classified as Supported, Contradicted,
                            Contested, Unknown.
𝜃𝑔                          Support threshold for the Supported classification of a claim.
𝜃𝑐                          Contradiction threshold for the Contradicted classification of a claim.
𝜃𝑒                          Emission threshold (𝑊 + ≥ 𝜃 𝑒 required to emit).
𝜃𝑟                          Refutation threshold (𝑊 − + 𝑊 ± ≤ 𝜃 𝑟 required to emit).
Maximal certifiable residue (§6)
At(𝑦)                      Atomic claims of an answer 𝑦.
C = {𝐶1 , . . . , 𝐶𝑚 }     Family of decidable predicates (constraints) on subsets of At(𝑦).
Cert (C, 𝑦)                Certifiable family: subsets satisfying every 𝐶 𝑗 ∈ C.
MCR(C, 𝑦)                  Maximal certifiable residue: highest-weight element of Cert.
Hoare-style agent action (§8)
Pre(𝑎, 𝜎, 𝛼)               Precondition predicate on action 𝑎, state 𝜎, arguments 𝛼.
Post(𝑎, 𝜎, 𝜎 ′ , 𝛼)        Postcondition relating pre-state 𝜎 and post-state 𝜎 ′ .
Compositional stability (§9)
Π                          Pipeline 𝐿 𝑛 ◦ · · · ◦ 𝐿 1 of certified layers.
𝑔𝑖                         Per-layer gain (Lipschitz constant on the metric output of layer 𝐿 𝑖 ).
𝑚𝑖                         Per-layer margin (the maximum allowable input perturbation for layer 𝐿 𝑖 ).
𝜀★
 𝑖                         Chained perturbation budget at the input of layer 𝐿 𝑖 .
                                               Î𝑛
𝜅Π                         Cumulative gain 𝑖=1        𝑔𝑖 .
                                                                           Î
𝐵Π                         Pipeline-wide perturbation budget min𝑖 𝑚 𝑖 / 𝑗<𝑖 𝑔 𝑗 .
Statistical and empirical
𝜅                            Cohen’s kappa (panel-reliability statistic).
𝑁                            Sample size (per-pilot effective query count).




                                                         76
B     Abbreviations

Abbreviation            Expansion
AI                      Artificial intelligence.
API                     Application programming interface.
CEGAR                   Counterexample-guided abstraction refinement.
CI                      Confidence interval.
CoT                     Chain-of-thought reasoning.
CTL                     Computation tree logic.
DAG                     Directed acyclic graph.
DOAC                    Direct oral anticoagulant (clinical case study, §11.1).
EU AI Act               European Union Artificial Intelligence Act.
FBR                     False-block rate (Pilot A primary metric).
FDA SaMD                U.S. Food and Drug Administration regulation of Software as a Medical Device.
HIPAA                   Health Insurance Portability and Accountability Act (U.S. clinical-privacy law).
IID                     Independent and identically distributed.
ISO/IEC 42001           International AI-management-system standard.
ITP                     Interactive theorem proving.
JSON                    JavaScript Object Notation.
LOC                     Lines of code.
LLM                     Large language model.
LTL                     Linear temporal logic.
MCR                     Maximal certifiable residue (§6).
ML                      Machine learning.
NIST AI RMF             U.S. National Institute of Standards and Technology AI Risk Management Framework.
NLI                     Natural language inference.
NLP                     Natural language processing.
NN                      Neural network.
NNV                     Neural-network verification.
PCC                     Proof-carrying code.
PII                     Personally identifiable information.
PRM                     Process reward model.
QA                      Question answering.
RAG                     Retrieval-augmented generation.
ReAct                   Reasoning-and-acting agent paradigm.
RL                      Reinforcement learning.
SHA-256                 Secure Hash Algorithm, 256-bit output.
SMT                     Satisfiability modulo theories.
SNARK                   Succinct non-interactive argument of knowledge.
TCB                     Trusted computing base.



C Lean 4 Compiled Reference Artifact: Structures and Theorems
The companion Lean 4 project at lean_artifact/ compiles all 22 certificate types under Lean 4 v4.30.0-rc2
with Mathlib. The artifact builds via lake build in roughly ten seconds with a warm Mathlib cache. We
reproduce here a representative excerpt: the compiled embedding sensitivity certificate, the conflict-aware
grounding certificate skeleton, and the Hoare trajectory certificate. A representative #print axioms excerpt is in
Appendix D, and the full per-declaration audit is regenerated by EmbeddingSensitivity/AxiomAudit.lean
on every build.


                                                       77
Embedding sensitivity (§7).
                       √
                            The crucial design choice is squared radii throughout, so the certificate
stays in ℚ and avoids irrational · in proof fields; square roots enter only at the theorem statement.

Lean 4: verbatim compiled excerpt from Certificate.lean
  namespace VerifiedEmbedding

  axiom ParaphraseOracle : String -> List String -> List String -> Prop

  axiom cauchy_schwarz_sq (u v : Embedding) :
    innerProd u v * innerProd u v ≤ l2NormSq u * l2NormSq v

  axiom innerProd_sub (u v w : Embedding) :
    innerProd (List.zipWith (· - ·) u v) w
     = innerProd u w - innerProd v w

  structure EmbeddingSensitivityCertificate where
    text : String
    embedding : Embedding
    G_inv G_sig : List String
    emb_inv emb_sig : List Embedding
    R_inv_sq R_sig_sq delta_sq : Rat
    p_inv_length : G_inv.length = emb_inv.length
    p_sig_length : G_sig.length = emb_sig.length
    p_bounded_orig : l2NormSq embedding ≤ 1
    p_bounded_inv : ∀ v ∈ emb_inv, l2NormSq v ≤ 1
    p_bounded_sig : ∀ v ∈ emb_sig, l2NormSq v ≤ 1
    p_R_inv_nonneg : 0 ≤ R_inv_sq
    p_R_sig_nonneg : 0 ≤ R_sig_sq
    p_R_inv_sound : ∀ e ∈ emb_inv, l2DistSq embedding e ≤ R_inv_sq
    p_R_sig_sound : ∀ e ∈ emb_sig, R_sig_sq ≤ l2DistSq embedding e
    p_delta_correct : delta_sq = R_sig_sq - R_inv_sq
    h_paraphrase_valid : ParaphraseOracle text G_inv G_sig

  theorem robust_similarity_sq
      (cert : EmbeddingSensitivityCertificate)
      (d_emb : Embedding)
      (h_d_norm : l2NormSq d_emb ≤ 1)
      (e’ : Embedding)
      (h_e_in : e’ ∈ cert.emb_inv) :
      let diff := innerProd cert.embedding d_emb - innerProd e’ d_emb
      diff * diff ≤ cert.R_inv_sq := by
    have h_drift : l2DistSq cert.embedding e’ ≤ cert.R_inv_sq :=
      cert.p_R_inv_sound e’ h_e_in
    exact similarity_diff_sq_bound cert.embedding e’ d_emb
          cert.R_inv_sq h_drift h_d_norm

  end VerifiedEmbedding



                                                       78
Bilattice grounding (§5). The full structure including p_emission_rule, p_reconstruction, and
the two tier-4 oracles is in §5 above; the emission-gate soundness lemma (Lemma 5.4) discharges by definitional
unfolding plus rational arithmetic and is conditional on the NLI / decomposition oracles.


Hoare action (§8). The counter-state instantiation in the artifact is pure integer arithmetic with decidable
equality; every proof field reduces by kernel computation alone. #print axioms reports “does not depend on
any axioms” for every declaration in this module.


Universal Assurance Card (§10). The card structure and the VerdictConsistent predicate are stated
in Lean form in §10; the predicate is decidable on Rat, Bool, and List String fields, requires no Mathlib-heavy
lemmas, and is well-suited to direct decide discharge once added to the artifact as AssuranceCard.lean. The
worked-example cards from §11 are correspondingly specified; promoting them to compiled (a focused engineering
step) is the natural follow-on to this paper. The remainder of this audit reports the 22 currently-compiled
certificate types.



D      Representative Axiom Audit
The following is a representative excerpt of the #print axioms output from running lake build on the artifact,
organized by certificate family. It reproduces every core declaration verbatim along with the named non-Ω
axioms for each catalogue family. It is not the complete #print axioms output for every one of the 46 audited
declarations; the full output is regenerated on every build by the EmbeddingSensitivity/AxiomAudit.lean
module, which emits one #print axioms info-message per audited declaration during lake build and is the
reproducible source of record for the audit. No sorry, no Lean.ofReduceBool; every reported axiom is either
in the kernel-trusted set Ω or an explicitly declared named non-Ω assumption (tier-2 mathematical placeholder,
tier-3 cryptographic assumption, or tier-4 ML/human oracle, per §3.4). Example-specific witness axioms (such
as example_paraphrase_oracle, example_decomp_oracle, and example_nli_oracle) appear only in
illustrative example modules to discharge the corresponding tier-4 oracle premises on a single concrete instance;
they are not framework-level oracles and are excluded from the five persistent tier-4 oracles counted in Table 2.

 Lean 4: embedding sensitivity (§7)

  ’VerifiedEmbedding.l2NormSq’ depends on axioms:
    [propext, Classical.choice, Quot.sound]
  ’VerifiedEmbedding.l2DistSq’ depends on axioms:
    [propext, Classical.choice, Quot.sound]
  ’VerifiedEmbedding.EmbeddingSensitivityCertificate’ depends on axioms:
    [propext, Classical.choice, Quot.sound, ParaphraseOracle]
  ’VerifiedEmbedding.similarity_diff_sq_bound’ depends on axioms:
    [propext, Classical.choice, Quot.sound,
     cauchy_schwarz_sq, innerProd_sub]
  ’VerifiedEmbedding.robust_similarity_sq’ depends on axioms:
    [propext, Classical.choice, Quot.sound, ParaphraseOracle,
     cauchy_schwarz_sq, innerProd_sub]
  ’VerifiedEmbedding.Example.exampleCertificate’ depends on axioms:
    [propext, Classical.choice, Quot.sound, ParaphraseOracle,
     example_paraphrase_oracle]


 Lean 4: conflict-aware grounding (§5)

                                                      79
 ’VerifiedEmbedding.Grounding.EpistemicStatus’
   does not depend on any axioms
 ’VerifiedEmbedding.Grounding.classify’
   does not depend on any axioms
 ’VerifiedEmbedding.Grounding.ConflictAwareGroundingCertificate’
   depends on axioms: [propext, Classical.choice, Quot.sound,
                       DecompositionOracle, SignedSupportOracle]
 ’VerifiedEmbedding.Grounding.no_silent_contradictions’
   depends on axioms: [propext, Classical.choice, Quot.sound,
                       DecompositionOracle, SignedSupportOracle]
 ’VerifiedEmbedding.Grounding.Example.exampleGroundingCertificate’
   depends on axioms: [propext, Classical.choice, Quot.sound,
                       DecompositionOracle, SignedSupportOracle,
                       example_decomp_oracle, example_nli_oracle]


Lean 4: Hoare agent action (§8)

 ’VerifiedEmbedding.Action.ActionSchema’        does not depend on any
     axioms
 ’VerifiedEmbedding.Action.ActionCertificate’   does not depend on any
     axioms
 ’VerifiedEmbedding.Action.TrajectoryCertificate’ does not depend on any
     axioms
 ’VerifiedEmbedding.Action.step_post_holds’     does not depend on any
     axioms
 ’VerifiedEmbedding.Action.trajectory_all_steps_safe’
                                                 does not depend on any
     axioms
 ’VerifiedEmbedding.Action.Example.exampleTrajectory’
                                                 does not depend on any
     axioms


Lean 4: compositional stability (§9) and MCR (§6)

 ’Composition.compositional_stability_two_layer’ depends on axioms: Ω
 ’MCR.residue_is_certifiable’                     depends on axioms: Ω
 ’MCR.subset_of_residue_is_certifiable’          depends on axioms: Ω
 ’MCR.residue_is_fixed_point’                     depends on axioms: Ω


Lean 4: Hoeffding concentration (catalogue)

 ’Concentration.HoeffdingCertificate’ :
    [propext, Classical.choice, Quot.sound,
     HoeffdingInequality, IIDSamples]
 ’Concentration.phat_in_unit_interval’ : Ω + {HoeffdingInequality,
     IIDSamples}


                                         80
    ’Concentration.hoeffding_confidence_interval’ :
       Ω + {HoeffdingInequality, IIDSamples}


 Lean 4: Curry–Howard structured outputs (catalogue)

    ’CurryHoward.SortedList’                     does not depend on any axioms
    ’CurryHoward.DistinctList’                   does not depend on any axioms
    ’CurryHoward.BalancedParens’                 depends on axioms: Ω
    ’CurryHoward.GroundedQuote’                  depends on axioms: Ω


What the audit shows. (i) Zero sorryAx or Lean.ofReduceBool anywhere in the transitive set of
any certificate, the operational definition of sorry-free Ω-audited (Def. 3.1). (ii) The Hoare action certificate,
scope-of-validity, simpler CEGAR theorems, simpler Curry–Howard exemplars, and several catalogue types
(provenance, temporal validity, calibrated abstention, diff, meta) compile with no axioms at all (17 of 46
declarations); the guarantee is unconditional modulo the Lean kernel itself. (iii) The remaining 29 declarations
depend only on Ω plus explicitly declared non-Ω assumptions, partitioned into tier-2 mathematical placeholders,
tier-3 cryptographic assumptions, and tier-4 ML/human oracles; the auditor sees exactly which natural-language
judgments and which mathematical/cryptographic assumptions the certificate is conditional on, and can reject
any certificate whose declared-axioms list is not within an approved set.


Reproducibility. From lean_artifact/: lake exe cache get pulls the precompiled Mathlib cache;
lake build compiles everything and emits the #print axioms output above verbatim. Any deviation (in
particular sorryAx or Lean.ofReduceBool appearing) would indicate a compilation regression and cause the
audit to reject under Definition 3.1.



E      Extended Catalogue: Per-Type Companion Notes
For completeness, the broader catalogue beyond the main-text core. The paragraphs are deliberately terse;
full structures are in the Lean sources for the compiled types. The 17 catalogue types compiled in the artifact
(Table 6) are: self-consistency lattice, chain-of-thought DAG, Curry–Howard structured output, concentration,
proof-of-sampling, scope-of-validity, CEGAR, and the “ten additional types” block (negative-guarantee through
meta/self-audit). The paragraphs below labeled “specified” are described in narrative form, pending dedicated
artifact modules: semantic type system for text (the role-tag concept is used implicitly by the grounding certificate
of §5 but does not yet have a standalone module), conformal prediction, compositional uncertainty (Markov
categories), and the five-way extensions block. These are not part of the 22 compiled count.


Self-consistency lattice (axiom-free). A canonicalizer-parameterized aggregation of 𝑘 samples to
canonical form, with a winner-meets-threshold theorem and a Galois-connected threshold ladder. Compiles with
no axioms at all on finite concrete data.


Chain-of-thought DAG. Reasoning steps as a typed DAG with parameterized aggregation (Amin , AΠ ,
A∨ , A 𝐹 𝐻 ); Conservative Aggregation Soundness Theorem (A ≤ min implies sound lower-bound under any
joint, with A Π tight under independence). Tier-4 oracle: StepConfidenceOracle.


Curry–Howard structured output. Inductive types whose constructors carry decidable proof
obligations: SortedList, DistinctList, BalancedParens, GroundedQuote. The LLM proposes; the


                                                        81
kernel rejects. Refinement-type compilation [50, 55] handles routine arithmetic via SMT; full dependent-type
obligations stay in Lean.


Concentration certificates. Hoeffding (binary), generalized Hoeffding ([𝑎, 𝑏]), Bernstein, empirical
Bernstein, Azuma–Hoeffding (martingales), Bennett, McDiarmid, union-bound categorical. Each is the same
Lean structure with a different failure_bound and named hypothesis. Named non-Ω axioms: IIDSamples
(tier-4 oracle on the sampling discipline), HoeffdingInequality (tier-2 mathematical placeholder pending
Mathlib formalization).


Proof-of-sampling. Commitment-bound randomness for honest 𝑘-sample claims via a hash of seed plus
sampling-record. Tier-3 oracle: HashCollisionResistant.


Semantic type system for text [specified]. Role-tagged text (user_input, system_prompt,
retrieved_fact, tool_output, . . . ) with a coercion lattice. A role non-interference property follows by
structural induction over the coercion record: when the lattice forbids the flow 𝜌1 → 𝜌2 , the pipeline output
restricted to role 𝜌2 is a function only of inputs of role ≠ 𝜌1 . Prompt injection via retrieved content thus becomes
a compile-time error rather than a runtime filter.


Scope-of-validity. For each oracle, a decidable scope predicate on the input plus a graceful-downgrade
rule when the predicate fails. Compiles axiom-free in the core case. Composes with every other certificate as an
input gate.


Counterexample-guided certificate repair (CEGAR). Failure witnesses are first-class certificate
fields; on failure, the LLM is re-prompted with a typed witness; loops terminate within a declared budget.
Connects to neural theorem-proving repair [32].


Conformal prediction [specified]. Distribution-free coverage on the candidate set under an exchange-
ability axiom; Mondrian, conformal-risk, and adaptive variants for drift.


Ten additional types. Negative-guarantee (absence of forbidden patterns), counterfactual / causal (output
stable under protected-attribute swap), calibration (max bin gap on held-out set), provenance (cryptographic
input binding), temporal validity (freshness window), budget composition (cost stays under parent’s allowance),
calibrated abstention (conformal abstain rate), diff / incremental (incremental certificate over diff), multi-hop
branching (AND/OR/NOT reasoning trees), meta / self-audit (kernel hash + reproducible build).


Compositional uncertainty (Markov categories) [specified]. A categorical treatment of
compositional uncertainty, including Markov-category formulations [21] of credal-set or interval certificates, is a
theoretical direction outside the compiled artifact and outside the present paper’s implementation claims.


Spectral sensitivity [specified]. Complements the finite-family embedding certificate of §7 by
bounding an encoder Lipschitz constant via per-layer spectral-norm or randomized-smoothing witnesses, then
lifting the finite perturbation family to a continuous metric-ball statement. The bound is conservative rather than
exact, in contrast to §7’s finite max/min certificate.




                                                        82
Dual-model cross-verification [specified]. Submits the same input to two independently-
implemented providers, applies a deterministic canonicalizer to both outputs, and emits either a weakest-verdict
agreement Card or a dissent-marked downgraded Card. The guarantee is agreement on canonical denotation, not
truth; the audit handle permits a third party to replay the canonicalizer check against both providers’ kernel-audited
build outputs without re-running either underlying model.


Abstract interpretation, canonical-denotation decoding, zero-knowledge proof-carrying
outputs [specified]. Three further extensions: sound output over-approximations (e.g. PII-excluding
grammar); semantic reproducibility via deterministic canonicalization at the decoder; and SNARK compression
of certificates for transport.



F     Adoption Pathways and Regulatory Mapping
Adoption pathways. Adoption pathways span product UX (assurance-mode selectors, claim-by-claim
highlighting, time-decaying cards), engineering (provider-agnostic verifier sidecars, automatic metamorphic
challenges, cross-provider quorum, CEGAR-style certificate-conditioned repair), governance (verifiability as a
leaderboard dimension, procurement and insurance contracts, per-organization trust budgets), and training (a
certifiability rate optimized alongside accuracy).


Regulatory mapping. The certificate taxonomy and the Universal Card map onto major frameworks:
EU AI Act articles on risk management (Art. 9), logging (Art. 12), transparency (Art. 13), human oversight
(Art. 14), and accuracy / robustness / cybersecurity (Art. 15); FDA SaMD and NIST AI RMF MAP/MEASURE/-
MANAGE/GOVERN; ISO/IEC 42001 management-system clauses; HIPAA / clinical privacy via the role-typed
semantic type system; Federal Rules of Evidence 702 / Daubert via the kernel-checked Ω-audit. The point is
structural: the framework is a reinforcement of the same guarantees these regimes require, with kernel-audited
certificates standing in for hand-waving compliance evidence.




                                                         83
