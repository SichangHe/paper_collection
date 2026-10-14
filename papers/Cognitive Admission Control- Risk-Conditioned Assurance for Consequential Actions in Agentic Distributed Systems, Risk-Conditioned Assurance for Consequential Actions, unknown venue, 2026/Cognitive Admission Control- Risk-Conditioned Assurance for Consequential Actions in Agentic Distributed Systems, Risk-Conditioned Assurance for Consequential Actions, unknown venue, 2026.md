                                                                          Cognitive Admission Control:
                                                              Risk-Conditioned Assurance for Consequential Actions
                                                                         in Agentic Distributed Systems

                                                                                     Jun He                        Deying Yu
                                                                                  OpenKedge.io                    OpenKedge.io
arXiv:2609.16313v1 [cs.DC] 14 Sep 2026




                                                                  Abstract                                     accepts a generated tool call whose supporting observations
                                         In agentic distributed systems, an agent may be authorized to         may be incomplete, stale, or derived from a shared faulty
                                         mutate external infrastructure while lacking evidence that the        source.
                                         mutation is ready to execute. Cognitive Admission Control                Existing systems already separate untrusted computation
                                         (CAC) makes this evidence requirement explicit. A policy              from trusted enforcement. Access-control engines evalu-
                                         maps a typed action and its modeled risk to assurance obli-           ate policy predicates, proof-carrying code checks consumer-
                                         gations specifying predicates, evidence classes, scope, fresh-        specified safety conditions, and agent transaction runtimes
                                         ness, and witness-set constraints. A deterministic evaluator          validate proposed work before commitment [2–4]. The prob-
                                         distinguishes satisfied, violated, and unresolved obligations;        lem addressed here is how to make missing evidence an ex-
                                         unresolved conditions produce targeted evidence-acquisition           plicit part of this interface: which evidence must an action
                                         requests. Successful admission produces a certificate binding         supply, what remains unresolved, and which parts of a suc-
                                         the action, its witness manifest, and dispatch-time guards.           cessful evaluation must still hold when execution begins?
                                            We formalize the admission calculus and the assumptions               We propose Cognitive Admission Control (CAC), a
                                         connecting it to mediated execution. The guarantees are               policy-governed admission layer for consequential actions
                                         policy-relative: physical safety additionally requires sound          in agentic distributed systems. CAC maps a typed proposal
                                         evidence, an adequate environment model, and preservation             and a controller-visible risk profile to a set of assurance obli-
                                         of relevant conditions through the effect. A TypeScript pro-          gations. Each obligation specifies a predicate, acceptable
                                         totype is evaluated in 2,730 controlled local trials with in-         evidence classes, scope, freshness, and any set-level require-
                                         dependent effect observation and matched fault schedules.             ments. The evaluator returns satisfied, violated, or unknown.
                                         Across 390 CAC trials, 120 effects complete without mod-              Missing evidence produces a remediation contract; affirma-
                                         eled harm and no harmful effects occur. A live-policy base-           tive violation produces denial. A successful evaluation yields
                                         line achieves the same completion count but admits the con-           a certificate binding the proposal, the supporting witnesses,
                                         structed correlated-witness failure. Mechanism ablations iso-         and dispatch-time guards.
                                         late guard, evidence-class, structural-cut, and remediation              Consider a failover policy requiring a receipt for replica-
                                         behavior. A further 9,000 measurements exercise the com-              tion state and a separate receipt confirming primary fencing.
                                         plete local dispatch path with persistent replay protection.          A fresh lag measurement cannot discharge the fencing obli-
                                         These results establish tested implementation behaviors and           gation, regardless of how many times the agent repeats it or
                                         local costs, not production failure rates or comparisons of           how much reasoning it performs. Once both obligations are
                                         language-model capability.                                            satisfied, the certificate remains usable only within its scope
                                                                                                               and validity interval. If a bound state version changes, the
                                                                                                               gateway rejects dispatch. Preserving the same conditions until
                                         1   Introduction                                                      the database applies the effect requires target-side conditional
                                                                                                               execution or a transaction protocol.
                                         In agentic distributed systems [1], an autonomous agent au-              This design makes a policy’s assurance requirements in-
                                         thorized to promote a database replica may still lack evidence        spectable and actionable. It does not make the policy correct
                                         that the replica is current, that the old primary is fenced, or       by construction. An omitted dependency can produce an in-
                                         that the proposed target matches the approved scope. The              complete obligation set, and an authentic sensor can report a
                                         access decision and the operational preconditions answer dif-         false value. We therefore separate policy-relative admission,
                                         ferent questions. This distinction matters when a runtime             mediated dispatch, and physical-world safety throughout the


                                                                                                           1
model.                                                                   2.2   Independent Enforcement
                                                                         The proposer may generate proofs, collect telemetry, or sug-
1.1    Contributions                                                     gest verification steps. It cannot set the evaluator’s required
The paper makes three contributions:                                     predicates or unilaterally mark them satisfied. Model confi-
                                                                         dence is usable only if the governing policy explicitly defines
    1. A typed admission calculus connecting risk-conditioned            and justifies its evidentiary role; confidence is not a general
       obligation selection, ternary evidence discharge, and             substitute for a fresh external observation.
       targeted evidence acquisition (Sections 3–4).                        The admission verdict and canonical witness selection are
    2. Explicit refinement conditions connecting a successful            deterministic for fixed proposal, modeled state, evidence, and
       evaluation to a witness manifest, a bounded capabil-              evaluation context. Certificate issuance additionally uses an
       ity, and guarded dispatch. The formal results state the           issuance time and a fresh nonce, so repeated evaluations need
       information and trust assumptions needed for these con-           not produce byte-identical certificates. The trust boundary
       nections (Section 5).                                             separates the evidence-producing process from the code that
                                                                         interprets evidence and authorizes dispatch.
    3. A TypeScript prototype with bounded witness search and
       persistent local replay protection, evaluated in 2,730 con-
                                                                         2.3   Consequential and Lightweight Paths
       trolled trials and 9,000 complete-path timing samples.
       Independent effect observation, matched fault schedules,          Policy classifies operations by their modeled consequences.
       and mechanism ablations make the tested behaviors re-             Operations below its threshold may use ordinary authorization
       producible (Sections 7–10).                                       and lightweight mediation. Consequential actions require the
                                                                         obligation-based admission path. Read-only operations are
   The contribution is the admission interface and its compo-
                                                                         not automatically low-risk: disclosure, resource contention,
sition rules, not a new access-control expressiveness result, a
                                                                         or diagnostic side effects may make them consequential. Clas-
proof of general agent safety, or an empirical comparison of
                                                                         sification belongs to the trusted control plane; a classification
language models. The current evaluation establishes selected
                                                                         miss is outside the conditional guarantee for correctly classi-
prototype behaviors; it does not establish a production safety
                                                                         fied actions.
rate.

2     From Authority to Readiness                                        3     System, Risk, and Evidence Model

Authorization and readiness can be evaluated by the same pol-            3.1   State and Trust Boundary
icy engine. Their distinction is informational: a check over             An agent proposes operations to an execution gateway K. The
identity and scope cannot determine an operational condi-                agent may produce incorrect plans or evidence, but cannot
tion absent from its inputs. ABAC may incorporate dynamic                modify the trusted evaluator, signing keys, policy, or gateway.
state, and a sufficiently expressive policy engine can imple-            Complete mediation requires that target credentials and net-
ment CAC’s predicates. CAC specifies the evidence lifecycle              work access remain confined to K. Identity, observation chan-
around those predicates: acquisition, provenance, conflict               nels, policy configuration, and the gateway’s state sources are
handling, expiration, and binding to dispatch.                           explicit trust dependencies, not properties established by the
                                                                         agent.
2.1    Resources, Evidence, and Discharge                                   Let S ∗ be the external state space and S the space of
                                                                         controller-visible snapshots. A valid snapshot s ∈ S rep-
Let R bound tokens, context, retrieval calls, inspection calls,
                                                                         resents a nonempty set γA (s) ⊆ S ∗ of possible external
verification compute, elapsed time, and cost:
                                                                         states under environment model A. The live state s∗ need
               R = ⟨T, Cctx , M, Atool , Vcpu , L, $⟩.        (1)        not be uniquely determined by s. Model fidelity requires
                                                                         s∗ ∈ γA (s) and coverage of relevant external transitions. An
A process consumes resources to produce evidence E; the                  inconsistent snapshot with empty concretization is rejected,
evaluator checks E against required obligations Ω:                       not treated as vacuously safe. An agent’s internal belief ŝ is a
           acquisition   discharge under Π                               separate object and supplies no privileged access to s∗ .
       R −−−−−→ E −−−−−−−−−→ admission verdict.               (2)
More compute can improve reasoning [5, 6]. Its allocation                3.2   Intent and Action
alone does not certify that a particular observation was made
or remains current. Likewise, a database role observation does           Definition 1 (Intent and proposal). An intent i =
not establish replication completeness: distinct predicates              ⟨goal, scope, constraints⟩ specifies desired external states,
require evidence with the appropriate semantics.


                                                                     2
permitted targets, and operational constraints. A proposal                 All receipt timestamps must be comparable in a declared
is                                                                      clock domain. We use a normalized time scale with no future-
              q = ⟨i, a, params, scope,                                 dated receipts. A distributed deployment must provide authen-
                                                       (3)
                    principal, sv , constraints⟩,                       ticated time normalization and conservative skew bounds; un-
where a identifies a tool operation and sv is the state version         related local monotonic-clock readings cannot be subtracted
used to formulate it. The evaluator checks a normalized,                directly.
schema-valid proposal. Its canonical representation includes            Definition 4 (Evidence receipt).
every field affecting interpretation or execution.
                                                                                 e = ⟨id, claim, class, source, provenance,
Definition 2 (Modeled consequence and safety). Let                                                                                    (8)
                                                                                      scope, tobs , νs , integrity, dependencies⟩.
PostA (q, s) contain all possible external post-states at-
tributable to q from states in γA (s) under the declared transi-        The receipt binds a typed claim to its source, observation time,
tion model. The proposal is consequential when its worst-case           scope, and state version. Receipt identifiers are unique and
modeled loss crosses a policy threshold:                                content-bound; duplicate identifiers with different contents
                                                                        are rejected. Authenticity establishes origin and integrity
                   sup         LossΠ (x, y) ≥ τΠ .           (4)        under the registered trust roots. It does not establish the truth
                 x∈γA (s)
               y∈PostA (q,x)
                                                                        of the claim.

Here PostA (q, x) denotes transitions from a particular exter-          3.5     Obligations and Witness Eligibility
nal state x; their union defines PostA (q, s). Modeled safety
is                                                                      Definition 5 (Assurance obligation). An obligation ω de-
                                                                        clares a predicate, verification kind, scope, accepted evidence
 SafeΠ (q, s) ⇐⇒ ∀y ∈ PostA (q, s) : InvariantΠ (y). (5)                classes Eclass , freshness horizon ∆tmax , set constraints, op-
                                                                        tional EFD requirement, guard templates, and enforcement
Loss thresholds classify actions; they do not themselves prove          mode (required or advisory). Typical kinds are observation,
safety. Unknown or unsupported transition models require                verification, simulation, quorum, and dual control. Its identi-
conservative classification or escalation.                              fier and policy epoch bind these fields.

3.3   Risk and Policy                                                     A receipt is locally eligible exactly when it is authentic,
                                                                        belongs to an accepted class, covers the required scope, has a
The controller computes a policy-relative risk vector                   compatible state version, and satisfies
           ρ(q, s) = ⟨C, Bblast , I, U, D, P ⟩ ∈ R,          (6)                        0 ≤ teval − e.tobs ≤ ω.∆tmax .                (9)

representing consequence severity, blast radius, irreversibility,       We          denote          this         conjunction           by
observational uncertainty, dependency exposure, and adverse             LocallyEligibleΠ (e, ω, s, teval ) and its candidate pool
plausibility. Each coordinate has a declared preorder. The              by Eω . Rejection diagnostics may overlap: an untrusted
product preorder is ρ1 ⪯ ρ2 iff every coordinate of ρ1 is               receipt can also be stale.
below the corresponding coordinate of ρ2 . Profiles can be                 For W ⊆ Eω , WitnessValidΠ (W, ω, s) checks the de-
incomparable. These are policy categories, not calibrated               clared set constraints, such as distinct-source cardinality, prin-
probabilities unless an estimator is separately validated.              cipal separation, or reconciliation. Counting receipts does
   The policy snapshot Π maps the proposal, snapshot, and               not count independent sources. Separate entailment relations
risk to obligations. The mapping is trusted configuration.              determine whether W supports the predicate or its negation.
Determinism makes its output reproducible, not necessarily              Both polarities must satisfy their declared witness-validity
conservative or adequate.                                               requirements; a single negative receipt is not automatically
                                                                        a valid quorum counter-witness. A policy may separately
3.4   Evaluation Context and Receipts                                   declare that one trusted veto is sufficient.

Definition 3 (Evaluation context).                                      3.6     Structural Epistemic Fault Domains
            χ = ⟨Πeval , teval , Bop , Deval , Aeval ⟩       (7)        Following EFD [7], let BE be a finite basis of modeled root
                                                                        faults, D(v) ⊆ BE the exposure set of verifier v, and Γ a
pins policy and source registrations, evaluation time, opera-           nonempty family of nonempty decisive coalitions of a panel
tional budget, dependency topology, and authorization state.            Q. The structural cut is
Declarative admissibility is independent of Bop ; budget ex-
haustion may terminate the operational procedure without                      κE (Q, Γ) = min{|F | : F ⊆ BE , ∃C ∈ Γ,
                                                                                                                                     (10)
changing whether the evidence logically satisfies policy.                                            ∀v ∈ C, F ∩ D(v) ̸= ∅}.

                                                                    3
The minimum of an empty feasible set is +∞. In a deploy-                Canonical selection and finite search. Among maximal
ment, an unknown exposure profile must be rejected rather               witnesses of the selected polarity, the specification ranks by
than interpreted as a fault-free verifier. The shorthand κE (W )        policy priority, best worst-case freshness, structural cut when
uses the distinct sources in W and the obligation’s declared            required, smallest sufficient cardinality, and a canonical en-
coalition rule, proposition, and temporal context.                      coding tie-breaker. This defines a unique result on finite
   A cut of at least k excludes decisive corruption by fewer            inputs. It does not imply efficient exhaustive subset search:
than k modeled roots only if every erroneous approval is cov-           a pool of n receipts has 2n subsets. Implementations must
ered by an active root, the exposure map is conservative, and           restrict the witness grammar or bound search. A truncated
Γ matches the actual authorization rule. This is a structural           search returns unknown or abort, never a permit inferred
guarantee, not a statement of statistical independence.                 from incomplete conflict inspection. The prototype enumer-
                                                                        ates both polarities up to twelve unique eligible receipts per
                                                                        obligation and otherwise returns unknown. It implements
4     Cognitive Admission Control
                                                                        a policy-defined priority order over exact source identifiers;
4.1   Required Obligations                                              witnesses with equal priority remain incomparable across
                                                                        polarities.
The policy selects obligations using the typed proposal and
modeled state:                                                          4.3   Declarative Admissibility
                ΩΠ (q, s) = FΠ (ρ(q, s), q, s).             (11)        Definition 6 (CAC admissibility). AdmissibleΠ (q, s, E, χ)
Required obligations constrain admission; advisory obliga-              holds when:
tions produce diagnostics. Policies may emit dual-control                 1. q is schema-valid, bound to an injective canonical encod-
requirements when risk exceeds autonomous authority. An                      ing, authorized under χ.Aeval , and statically compliant
approval receipt cannot override a separate violated obliga-                 with Π = χ.Πeval ;
tion.
                                                                          2. the policy resolver enumerates every obligation triggered
4.2   Discharge Semantics                                                    by the fixed inputs;

For a required obligation ω, let W+             −                         3. every required obligation returns S ATISFIED(Wω ) under
                                       ω and Wω be the finite
sets of eligible, valid witness sets supporting its predicate                the discharge rule;
and its negation, respectively. Entailment and validity are               4. the derived guard set Gq and permitted invocation enve-
total policy-defined procedures over a restricted predicate                  lope Eq satisfy the coverage conditions below.
language. They do not invoke an unrestricted theorem prover
with an assumed termination guarantee.                                  Admissibility is independent of operational budget. It makes
   A policy supplies a strict partial preference order on valid         no assertion about obligations absent from the policy.
                                                             −
witnesses. Let Mω be the maximal elements of W+       ω ∪ Wω .
Write Pω and Nω for the presence of positive and negative               Witness manifest. The manifest preserves the relation be-
witnesses in Mω , respectively. The discharge result Dω =               tween each required obligation and its canonical witness:
Discharge(ω, E, s, χ) is:                                                     Wq = {(ω, Wω ) : ω ∈ Required(ΩΠ (q, s))}.           (13)
            
            
              S ATISFIED(W )            Pω ∧ ¬Nω ,                     Local eligibility supplies freshness and version compatibil-
            
            V IOLATED(W )               Nω ∧ ¬Pω ,                     ity. Set validity supplies the declared quorum and separation
     Dω =                                                  (12)
            
              U NKNOWN    (Conflict)    P ω ∧ Nω ,                     conditions. Advisory results are recorded separately.
            
               U NKNOWN(c)               ¬Pω ∧ ¬Nω .
            
                                                                        Envelope coverage. An exact-action certificate allows
A witness cannot support both polarities under a well-formed            only q. An envelope certificate may allow a variant
entailment relation. Equal-priority or incomparable oppos-              q ′ , but parameter attenuation alone is insufficient: a
ing witnesses produce conflict. Only after the polarity is              different target can require different evidence. Define
established does the evaluator select a canonical witness from          ManifestCoversΠ (Wq , q ′ , s, χ) to require that every obliga-
Mω .                                                                    tion for q ′ has a compatible manifest witness which remains
   When no valid witness exists, c identifies a failed structural       eligible, valid, and affirmatively entails that obligation under
constraint, stale or future-dated evidence, untrusted prove-            the same conflict semantics. Envelope soundness requires,
nance, incompatible version, or missing usable evidence. A              for every allowed consequential q ′ ,
fixed diagnostic precedence makes c reproducible; it does
not alter the semantic verdict. The policy must distinguish a                     ManifestCoversΠ (Wq , q ′ , s, χ)
                                                                                                                                   (14)
missing observation from evidence that its predicate is false.                       ∧ RequiredGuardsΠ (q ′ , s, χ) ⊆ Gq .

                                                                    4
The controller restricts envelope mode to approved templates             The earliest expiry of a supporting receipt bounds certifi-
with independently justified semantic coverage. The template           cate lifetime:
also fixes the subject and action interpretation and establishes
static compliance for each allowed variant; the gateway sep-                    twit =         min         (e.tobs + ω.∆tmax ),      (16)
                                                                                         (ω,W )∈Wq , e∈W
arately rechecks live authorization. The controller checks
template identity, policy epoch, parameter domain, coverage            with +∞ for an empty manifest. The mint enforces
requirements, and guards online. Exact-action mode reduces
                                                                             tissued ≤ texp ≤ min(twit , tpolicy , tauth , tcap ).   (17)
coverage to q itself, but still requires guard completeness.
General envelope verification is not claimed to be decidable;          If the bound precedes issuance, admission must be refreshed.
signed template approval is a trust assumption, not a substitute       A distributed clock implementation must subtract any uncer-
for its semantic justification.                                        tainty needed to make this expiry conservative.

4.4    Operational Decisions and Remediation                           4.6   Gateway Validation and Dispatch
The controller returns one of five outcomes:                           The gateway authenticates the presenter as the certified sub-
   • P ERMIT(Cq ) when admissibility and certificate validity          ject and validates the certificate without consuming it:
     checks succeed;                                                                AdmissionValid(C, q ′ , χlive ) ⇐⇒
   • D ENY for authorization, static-compliance, or decisive                           VerifySig(C)
     required-obligation violation;                                                     ∧ PresenterAuthorized(C)
   • D EFER with unresolved obligations and typed acquisi-                              ∧ tissued ≤ tnow ≤ texp
     tion requests;                                                                     ∧ NonceUnused(C)
                                                                                                                                     (18)
   • E SCALATE when unresolved approval obligations need                                ∧ EnvelopeValid(C, q ′ )
     an authorized reviewer, retaining all other unresolved                             ∧ GuardsHold(C.G, slive )
     requirements;                                                                      ∧ PolicyEpochCompatible(C)
   • A BORT when evaluation cannot finish within its opera-                             ∧ AuthorizationStillValid(C, q ′ )
     tional bounds.                                                                     ∧ NotRevoked(C).
Exhaustion may prevent a permit even when the logical ad-              The live context fixes the authenticated requester, current
mission conditions are satisfiable. A fresh evaluation context         time, policy, authorization, and observed guard state for this
is captured on each remediation turn; evidence obtained after          check. A comparison of untrusted identity strings is not
one evaluation is reconsidered in the next. Finite budgets             authentication. Unknown guards fail closed.
bound the number of attempts, but useful completion requires              After successful validation, the gateway performs an
available evidence and a sufficiently stable environment.              atomic unused-to-consumed nonce transition. Only the win-
   A consequential diagnostic action must itself undergo ad-           ner may dispatch:
mission or use a separately approved bounded diagnostic
capability. Recursive evidence acquisition cannot bypass the                      AuthorizedDispatchK ⇐⇒
execution boundary. Preventing cyclic dependencies requires                          AdmissionValid(C, q ′ , χlive )                 (19)
an additional well-founded acquisition discipline; it is not                         ∧ CAS(C.nonce, Unused, Consumed).
implied by the discharge rules.
                                                                       Here CAS denotes an operational event, not a pure logical
4.5    Certificates and Expiration                                     query. Both exact-action and envelope certificates are single-
                                                                       use. The forwarded operation must be the operation validated,
A certificate binds the subject, authority context, mode, pro-         and retries by the gateway or transport must not silently du-
posal digest, envelope, policy epoch, witness digest, guards,          plicate it. Consumption and forwarding need not be atomic
issuance and expiration times, nonce, and signature. Digests           with each other; a crash between them can lose the operation.
use domain-separated canonical encodings:                              Nor are guard reads atomic with target execution. Section 5
                                                                       separates those guarantees.
       ProposalDigest(q) = H(dprop ∥ Canon(q)),
                                                           (15)
      WitnessDigest(Wq ) = H(dwit ∥ Canon(Wq )).
                                                                       5     Formal Properties
The distinct fixed tags dprop and dwit prevent cross-type in-
terpretation. Canonicalization rejects ambiguous encodings             The first two results explain why limited observations or
and includes all security-relevant fields.                             resource accounting alone do not establish readiness. The


                                                                   5
remaining results state implementation obligations connecting          5.2   Admission and Enforcement
the calculus to dispatch. They are conditional properties
                                                                       Theorem 3 (Admission refinement). Assume finite, schema-
of the specified controller; the prototype is not a verified
                                                                       valid inputs; complete policy resolution; total determin-
implementation of the entire specification.
                                                                       istic discharge with sound witness validation; and suc-
                                                                       cessful guard/envelope validation. If Algorithm 1 returns
5.1   Information and Non-Substitution                                 P ERMIT(Cq ), then AdmissibleΠ (q, s, E, χ) holds and every
Theorem 1 (Authority–readiness separation). Fix q. Let                 required obligation has a corresponding valid witness in the
an authorization mechanism observe only α(q, s). Suppose               bound manifest.
states s1 , s2 share an allowed projection α0 , but a required         Proof. The algorithm reaches minting only after authoriza-
readiness predicate p is true in s1 and false in s2 . The mech-        tion and static compliance succeed. Each required obligation
anism allows both states and hence does not establish p. If            must either add a satisfied witness or prevent the permit path
CAC requires an obligation for p whose satisfaction implies            by violation, unresolved status, or failure. Complete reso-
p(s), it cannot admit s2 .                                             lution ensures no triggered obligation is omitted. The final
Proof. Equal projections give equal authorization decisions.           guard/envelope check establishes the remaining admission
Since α0 is allowed, authorization succeeds in s2 , where p            condition. Canonical manifest construction binds exactly the
fails. Sound discharge of the required obligation would imply          collected obligation–witness pairs.
p(s2 ), a contradiction.                                                 This is a refinement argument for the specified algorithm,
   The result concerns missing information, not the expres-            not a proof that its evidence claims are true or that a particular
siveness of authorization languages. It does not apply to a            implementation matches every premise.
mechanism whose inputs and policy already establish p.
                                                                       From       admission       to     modeled      safety. Let
Theorem 2 (Budget does not determine admission). Fix                   ConditionsΠ (q, s) mean that the semantic conditions
q, s, χ with sufficient operational budget. Suppose two                required by policy actually hold. Evidence soundness means
evidence-acquisition procedures are feasible within the same
resource envelope R: one returns evidence satisfying all ad-                 AdmissibleΠ (q, s, E, χ) =⇒ ConditionsΠ (q, s).
mission conditions, and the other omits a required witness
without establishing a violation. Then allocation of R alone           Policy adequacy is the independent specification obligation
does not determine admission.
                                                                        PolicyAdequate(Π, A) ⇐⇒ ∀q, s : ConditionsΠ (q, s)
Proof. The first procedure permits admission. The second                                                          =⇒ SafeΠ (q, s).
cannot satisfy the missing obligation and yields a non-permit                                                                     (20)
outcome. Both are feasible under the same budget.                      Combining the two gives modeled safety at the evaluated
                                                                       state. External safety additionally requires model fidelity and
  The feasibility assumption is necessary: a zero-budget pro-          preservation or atomic revalidation of all decisive conditions
cess or an unsatisfiable policy need not admit either execution.       until the effect. These assumptions cannot be derived from a
The result does not imply that additional compute cannot im-           certificate signature.
prove evidence acquisition.
                                                                       Property 1 (Mediated dispatch). Assume complete media-
Proposition 1 (Compensatory scores can bypass a required               tion, authentic certificates issued only by the specified mint,
condition). Suppose a scalar rule admits when f (z) ≥ θ. A             correct gateway validation, and a durable linearizable nonce
required obligation remains unsatisfied along an attainable            store shared by all gateway workers. Every governed dispatch
sequence zn , while f (zn ) → +∞ through unrelated proxy               has a valid certificate and consumes its nonce exactly once.
features. For every finite θ, the scalar rule admits some zn           No certificate authorizes more than one gateway dispatch.
that violates conjunctive admission.
                                                                       Proof. Complete mediation makes the gateway the only dis-
Proof. By divergence, there is an n for which f (zn ) ≥ θ.             patch path. Validation rejects an invalid certificate. Atomic
The required obligation remains unsatisfied by assumption,             unused-to-consumed transition has at most one successful
so CAC admissibility is false.                                         caller per nonce; only that caller may dispatch. Unforgeabil-
  This applies, for example, to a positive-weight unbounded            ity and correct minting connect an accepted certificate to an
proxy in an additive score. It excludes non-compensatory               admission evaluation, except with negligible cryptographic
scalar encodings of conjunction and does not assume that all           failure probability.
practical proxy features are unbounded.                                   A crash after consumption can lose an operation. A failed
                                                                       or ambiguous target response does not permit reuse. Thus the


                                                                   6
property gives at-most-once gateway dispatch, not exactly-             Untrusted proposer and evidence producers
once effects, successful execution, or automatic recovery.                                                                Remediation
Durability and retention must prevent nonce resurrection after                                                            (missing evidence)
restart.                                                                    Trusted policy resolver and evaluator
                                                                            Typed obligations; discharge; remediation
Property 2 (Execution-envelope preservation). Assume
collision-resistant hashing of an injective canonical encoding
and correct gateway checks. In exact-action mode, a dis-                                Certificate mint
patched proposal matches the certified proposal. In envelope                Proposal, witnesses, guards, expiry, nonce
mode, it satisfies the explicit envelope predicate. If the tem-
plate’s semantic coverage and guard-preservation obligations
hold, the manifest covers every required obligation of the                            Execution gateway
dispatched variant at the evaluated snapshot.                             Authentication, validation, nonce consumption

Proof. A different exact-action encoding fails digest equality
except with negligible collision probability. In envelope mode               Target adapter and external service
the gateway rejects a false envelope predicate; the universal               Conditional effect or separate transaction
template assumption supplies coverage and guard preserva-             Figure 1: Proposed deployment interface. The prototype
tion for an accepted variant.                                         exercises local evaluator, certificate, and gateway calls; a
  Parameter bounds alone do not prove semantic coverage.              production boundary additionally requires credential and net-
A signature on an approved template authenticates approval,           work confinement.
not its proof.
                                                                      Proposition 3 (Structural-cut bound, imported from EFD).
Property 3 (Guard-bound dispatch validity). If any required           Assume conservative exposure, closed causal accounting, au-
bound guard is false or cannot be evaluated at gateway val-           thorization alignment with Γ, and that an uncorrupted verifier
idation time, the gateway rejects dispatch. This requires             rejects a false proposition. If κE (Q, Γ) ≥ k, fewer than k
fail-closed evaluation of every bound guard and binding of            active modeled roots cannot induce a decisive false approval.
the checked request to the forwarded request.
                                                                      Proof. Any decisive false approval requires every member
Proof. Guard validity is a conjunct of AdmissionValid. Fail-          of some C ∈ Γ to be corrupted. Closed causal accounting
ure of a conjunct prevents the nonce-consumption and dis-             and conservative exposure then require the active fault set
patch path.                                                           to intersect every member’s exposure set, contradicting the
                                                                      minimum in Equation (10).
Validation versus effect time. Mode A checks guards be-                  The bound concerns modeled roots. It gives no probability
fore forwarding. Mode B translates relevant guards into               of failure and no protection against omitted common causes.
atomic target-side preconditions, covering only the state those       Appendix A gives explicit counterexamples at the boundaries
preconditions protect. Mode C delegates preservation through          of these statements.
commitment to a separately justified transaction protocol. The
nonce CAS serializes capability use; it does not freeze the
environment or serialize changes to unrelated guard state.            6      Reference Controller and Trust Boundary
                                                                      The prototype separates schemas, policy resolution, evidence
5.3   Monotonicity and Structural Cuts                                checks, work-loop evaluation, certificates, gateway valida-
Proposition 2 (Threshold-policy monotonicity). Fix pro-               tion, and domain adapters into TypeScript packages. The
posal, policy epoch, and all non-risk inputs. If ΩΠ (ρ) =             benchmark invokes them in one process. Figure 1 shows the
{ωj : τj ⪯ ρ} for fixed obligations ωj , then ρ1 ⪯ ρ2 implies         intended deployment boundary; network confinement and
ΩΠ (ρ1 ) ⊆ ΩΠ (ρ2 ).                                                  authenticated remote interfaces are deployment requirements,
                                                                      not consequences of package separation.
Proof. If τj ⪯ ρ1 , transitivity gives τj ⪯ ρ2 .

   Replacing an obligation by a stronger predicate requires           6.1     Trust Requirements
a semantic strength order, not literal set inclusion. Nothing         The enforcement TCB contains the policy resolver, evidence
follows for incomparable risk profiles or changing non-risk           evaluator, mint, gateway, and replay store. Their correctness
inputs.                                                               establishes policy-relative enforcement. External identity,
                                                                      time, telemetry, and topology services supply trusted inputs.


                                                                  7
Algorithm 1 CAC admission specification                                Table 1: Corrected local scenario families. Each named case
Require: Typed q, snapshot s, evidence E, context χ                    has thirty parameter instances per controller.
 1: if budget exhausted or verification cannot finish then             Family               Cases and tested boundary
 2:      return A BORT
                                                                       Target state         Healthy, excessive lag, offline candidate
 3: end if
                                                                       Evidence             Initially missing, unavailable, wrong class,
 4: if schema, authorization, or static compliance fails then
                                                                                            invalid rollback
 5:      return D ENY                                                  Dispatch change      Candidate drift, authorization revocation
 6: end if                                                             Target response      Benign failure, committed effect with lost
 7: Ω ← FΠ (ρ(q, s), q, s)              ▷ Complete resolution                               response
 8: W ← ∅; U ← ∅                                                       Source dependence    Correlated witnesses, independent witnesses
 9: for each required ω ∈ Ω do
10:      r ← Discharge(ω, E, s, χ)                                     6.3   Implementation Coverage
11:      if r = V IOLATED(W ) then
                                                                       The artifact implements typed receipts, Ed25519 signatures,
12:           return D ENY
                                                                       policy-defined guard templates, and nonce consumption. Both
13:      else if r = U NKNOWN(c) then
                                                                       positive and negative witnesses must satisfy the same set con-
14:           U ← U ∪ {ω}
                                                                       straints. Exhaustive bounded subset search replaces singleton-
15:      else
                                                                       or-aggregate selection, and canonical ranking uses the com-
16:           Add (ω, W ) from r to W
                                                                       puted structural cut rather than source count. The direct
17:      end if
                                                                       eligibility helper and diagnostics reject future timestamps
18: end for
                                                                       consistently. Predicate evaluation uses a bounded conjunction
19: if U contains approval obligations then
                                                                       language over typed fields and literal comparisons; it honors
20:      return E SCALATE(U )
                                                                       declared thresholds and cannot substitute a generic success
21: else if U ̸= ∅ then
                                                                       flag for missing evidence. Unsupported guards fail closed.
22:      return D EFER(U )
                                                                          The controller’s normal permit path mints an exact-action
23: end if
                                                                       certificate. Envelope utilities now independently bind the
24: Derive Gq , Eq from approved policy templates
                                                                       action class and evidence-covered proposal, reject absent
25: if coverage, guards, or issuance bounds are unverified
                                                                       constrained values, and enforce validity bounds. They con-
    then
                                                                       servatively require readmission when a proposal changes,
26:      return A BORT
                                                                       even if the new resource is allowed by the template. Gen-
27: end if
                                                                       eral semantic coverage across distinct proposals therefore
28: Cq ← Mint(q, W, Gq , Eq , χ)
                                                                       remains outside the implemented fragment. Guard anno-
29: return P ERMIT(Cq )
                                                                       tations remain authored policy, not automatically verified
                                                                       invariant-preservation proofs. The 133 passing tests support
Evidence-producing models remain outside the TCB, but
                                                                       the exercised behaviors; they are not a proof of conformance
any model output accepted as a witness inherits the policy’s
                                                                       to the entire calculus.
explicit verifier assumptions.
   The gateway requires an authenticated subject binding and
exclusive access to target credentials. The replay store must          7     CACBench: Controlled Local Scenarios
be shared and durable across workers. The prototype sup-
plies both an in-memory store and a persistent local-file store.       CACBench exercises the model’s enforcement and avail-
The latter uses exclusive creation followed by file and di-            ability boundaries. The corrected suite contains thirteen lo-
rectory flushes before dispatch; an eight-process race and a           cal failover state machines, summarized in Table 1. It in-
restarted store produce one successful nonce consumption.              cludes useful completion, harmful execution, refusal, and
This requires local-filesystem semantics and does not estab-           ambiguous-response cases. The suite is constructed around
lish distributed linearizability, storage behavior under hard-         CAC’s mechanisms and is not a representative sample of
ware failure, or network isolation.                                    operational incidents.

6.2   Specification Algorithm                                          State and evidence. The world records primary and can-
                                                                       didate identities, candidate role, unreplicated bytes, rollback
Algorithm 1 states the permit-path conditions needed by Theo-          validity, and effect counters. The tested policy requires zero
rem 3. Unsupported inputs, indeterminate template coverage,            reported replication lag, standby health, and a rollback attes-
and exhausted verification bounds must prevent permit.                 tation. Telemetry receipts carry source identity, class, obser-
                                                                       vation time, scope, and state version. The initial-evidence
                                                                       and acquisition paths can be controlled independently: an


                                                                   8
underprepared but healthy target supplies missing evidence,             pating controllers. Before and after each target invocation, it
while an unavailable source supplies none.                              copies the world state and its completed-effect and harmful-
                                                                        effect counters. The target transition updates those counters
Faults at the boundary. Dispatch drift takes the candi-                 according to the scenario’s preconditions; controller verdicts
date offline after initial evidence is available. Revocation            and response codes do not set the outcome labels. Traces
removes the actor’s authority at the same pre-dispatch phase.           retain invocation parameters, telemetry receipts, dispatch-
A harmful effect can still return a successful acknowledge-             boundary events, pre/post snapshots, and target responses.
ment, forcing the evaluator to distinguish target response from         This is separation within one trusted process, not isolation
ground-truth outcome. The benign-failure case returns an er-            against malicious controller code.
ror before changing state; the ambiguous case changes state                The distinction is tested explicitly. A harmful transition
successfully before losing its response.                                can return a successful acknowledgement; a request can fail
                                                                        without modifying state; and an operation can complete while
                                                                        its response is lost. The observer records these cases sep-
Correlated approval. Three approving sources share one
                                                                        arately. Ambiguous responses do not trigger an automatic
modeled root in the correlated-witness case. The policy re-
                                                                        retry.
quires all three and a structural cut of at least two. The
paired independent-witness case uses three disjoint roots and
a healthy target. These fixtures test enforcement of declared           Matched interventions. A shared pre-dispatch hook in-
exposure maps with synthetic receipts. They do not invoke               jects state drift or revokes authority immediately before each
language models, a formal solver, or a deployed telemetry               controller’s final execution gate. CAC therefore checks live
service.                                                                guards after the same scheduled transition that the live-policy
                                                                        baseline sees. Evidence availability and the telemetry API are
                                                                        common across controllers; the number and timing of calls
Legacy diagnostics. The historical F1–F11, E1, remedia-
                                                                        are part of each strategy. This schedule tests pre-gate drift, not
tion, and assumption-violation fixtures remain in the artifact.
                                                                        the later interval between forwarding and effect application.
Their archived logs are retained for provenance, and selected
fixtures remain regression tests. They are not pooled into the
corrected comparison. The new state machines are defined in             8.2   Comparators and Ablations
repairedScenarios.ts; the observer and run protocol                     AuthOnly checks an actual in-memory authorization snap-
are described next.                                                     shot and static proposal constraints before proceeding to dis-
                                                                        patch. LivePolicy additionally rechecks live authorization,
8     Evaluation Methodology                                            reacquires typed replica and rollback observations at the dis-
                                                                        patch boundary, and evaluates the required predicates. It
8.1   Execution and Observation                                         rejects missing evidence and affirmative counterevidence. It
                                                                        does not issue an admission certificate or enforce EFD struc-
We evaluate the TypeScript implementation in thirteen con-              tural cuts. This comparator tests the contribution relative to
trolled local state machines. Each scenario instantiates a              an environmental policy check, without claiming to reproduce
failover proposal, visible state, telemetry producers, autho-           a published access-control engine.
rization state, and a target transition function. The runner               The CAC controller uses the evidence work loop, certifi-
retains a separate privileged world snapshot and records ev-            cate, gateway, and declared EFD policy. Four ablations each
ery attempted target effect. These experiments execute the              remove one mechanism: NoGuard skips dispatch guards;
controller and its cryptographic checks; the target is a local          NoEFD removes structural-cut requirements; NoRemedia-
model, not a deployed PostgreSQL or Kubernetes service. No              tion denies on deferral; and NoTypedEvidence broadens eli-
language-model API is invoked.                                          gible evidence classes. The typing ablation does not change
   For each scenario, thirty seeds vary cluster identifiers, can-       tool selection. We exclude the historical extra-simulation-
didate identities, and, where applicable, the magnitude of              obligation intervention because an unavailable receipt cannot
excessive replication lag. Every controller receives a fresh            establish a general cost of static policy.
world for the same scenario and seed. Controller order ro-
tates across seeds. The matrix contains 13 × 7 × 30 = 2,730
                                                                        8.3   Outcomes and Reproducibility
trials. Seeds instantiate parameters within constructed fail-
ure categories; they do not sample independent operational              For each intent trajectory j, the observer determines whether
incidents.                                                              a harmful effect occurred and whether an effect completed
                                                                        without harm:
Independent outcome observation. The runner withholds                                              N
                                                                                               1 X
privileged world state and scoring functions from the partici-                     U IER =           1[UnsafeEffect∗ (j)].           (21)
                                                                                               N j=1


                                                                    9
                         N
                    1 X                                                   Table 2: Independently observed local effects across thirteen
         SICR =           1[Complete(j)                                   constructed scenarios and thirty parameter seeds. Completion
                    N j=1                                    (22)
                                                                          means an observed completed effect without harm; it does not
                               ∧ ¬UnsafeEffect∗ (j)].                     certify authorization. Counts are descriptive, not population
These predicates refer to the local transition model. Com-                estimates.
pletion without modeled harm does not certify authorization:                Controller           Trials   Attempts    Complete    Harm
a failover after revocation may complete physically while
                                                                            AuthOnly               390         390         180      180
violating access policy. We report counts and individual                    LivePolicy             390         180         120       30
mechanism contrasts, without population-level confidence                    CAC                    390         150         120        0
intervals or significance claims.                                           NoGuard                390         180         120       30
   The run protocol fixes scenarios, seeds, controller identi-              NoRemediation          390         120          90        0
ties, source revision, and measurement settings. The study                  NoTypedEvidence        390         180         120       30
saves full JSONL traces and a SHA-256 manifest in a new di-                 NoEFD                  390         180         120       30
rectory, refusing to overwrite existing output. An independent
Python analysis checks file hashes, unique trial IDs, response            9.2   Isolated Mechanism Contrasts
categories, effect counters, aggregate counts, and timing sam-            Dispatch guards. All controllers encounter the same
ple counts before generating the paper’s tables. The revised              candidate-offline transition before their final gate. CAC and
source passes 133 tests and strict TypeScript checking. One               LivePolicy prevent target invocation. NoGuard proceeds in
test compares the production structural-cut routine with di-              thirty trials, each producing an observed harmful effect. This
rect fault propagation for all 43,561 three-voter profile/rule            isolates the tested guard check under a matched schedule. It
combinations over three roots.                                            does not validate atomic preservation after forwarding.

Historical archive. The previous 5,261-record batch is pre-               Evidence classes. The wrong-class fixture supplies an au-
served separately. Its controller-dependent labels, scripted              thenticated static-verification receipt claiming zero lag while
model comparators, and incomplete timers cannot be repaired               the world contains excessive unreplicated data. CAC refuses it
retrospectively. Its statistical and cost reports are not evidence        as replica telemetry. NoTypedEvidence admits thirty harmful
for the results below. The corrected experiments report no                actions, with the same initial evidence and tool API. Unlike
model-token or monetary savings.                                          the archived F11 contrast, this intervention changes eligibility
                                                                          alone. It illustrates one erroneous evidence substitution, not
9     Observed Prototype Results                                          the completeness of the evidence-class taxonomy.

9.1   Completion, Refusal, and Harm                                       Structural cuts. The correlated-witness fixture supplies
Table 2 reports the corrected local matrix. CAC attempts                  three approving sources exposed to one common fault, with
150 target effects across 390 trials, completes 120 with-                 an all-of-three policy requiring a cut of at least two. CAC
out modeled harm, and produces no harmful effects. It                     rejects the resulting cut of one. NoEFD and LivePolicy each
completes the healthy, underprepared, ambiguous-response,                 admit thirty harmful transitions. When the three sources
and independent-witness scenarios in all thirty parameter in-             instead have disjoint modeled roots and report a healthy world,
stances each. Thirty additional attempts encounter the benign             CAC completes all thirty trials. This checks enforcement of a
target failure and leave state unchanged. The remaining 240               supplied dependency model; it does not measure errors from
trials do not reach the target. The zero-harm count describes             actual model panels or discover hidden correlations.
these fixtures, not a bound on deployment failure probability.
   AuthOnly attempts all 390 effects, producing 180 harmful               Evidence acquisition and availability. CAC completes
effects and 180 completions without modeled harm. Its com-                thirty initially underprepared intents after obtaining telemetry.
pletion count includes physically successful operations after             NoRemediation completes none of those trials, reducing its
authorization revocation; it is not a count of policy-compliant           total from 120 to 90. Both refuse all thirty intents for which
executions. LivePolicy completes the same 120 intents as                  evidence remains unavailable, even though the modeled target
CAC, incurs the same thirty benign failures, and permits                  would otherwise be safe. Evidence availability therefore
thirty harmful effects in the correlated-witness scenario. This           limits completion; failure to observe harm alone is insufficient
suite therefore does not establish a general utility advantage            to assess usefulness.
over a competent live-policy check.




                                                                     10
Table 3: Complete local path, in milliseconds: range of per-               The total is the elapsed interval from resolution through
process medians and p99s over three fresh processes, each               the awaited target return. It includes assertions within that
with 1,000 measured samples per workload. Includes file-                interval, local guard-read cost, and persistent replay protec-
backed guard reads and persistent nonce consumption; target             tion. It excludes receipt acquisition, model inference, remote
execution is an in-process callback.                                    service execution, and subsequent replay-check timing. The
                                                                        target callback increments an execution counter; it is not a
       Obligations/receipts   Median range     p99 range
                                                                        database mutation. These measurements establish local im-
       1/1                       4.65–5.69   10.28–37.37                plementation cost, not end-to-end deployment latency.
       4/4                       5.89–9.66   14.46–22.48
       8/8                     24.91–26.86   41.41–58.39
                                                                        10.2   Scaling and Limits
9.3    Response Semantics and Boundaries                                Separate sweeps use one, four, eight, and twelve distinct
In the benign-failure fixture, CAC reaches the target thirty            receipts. They time eligibility, full discharge, canonical en-
times, receives failure responses, and records neither com-             coding, and a manifest containing the entire receipt set; no
pletion nor harm. In the ambiguous-response fixture, thirty             receipt count is silently capped. Full-discharge timing in-
effects complete but their responses are lost. The independent          cludes eligibility and canonical selection as well as subset
observer records completion, while the gateway returns an               search, so these components must not be interpreted as a non-
ambiguous outcome and does not retry. These cases show                  overlapping decomposition. A separate EFD sweep varies
why response status, execution attempt, completion, and harm            both voters and roots over two, four, six, and eight, with dis-
must remain separate fields.                                            joint exposures and a two-of-n rule. The computed cut is two
   The older assumption-violation fixtures remain diagnostic            at every size. Each process repeats each scaling point five
examples of omitted dependencies, false trusted evidence,               times.
and insufficient guards. The corrected study makes no claim                The discharge implementation enumerates nonempty sub-
to eliminate those boundaries. Its results establish executable         sets and checks both polarities. It is deliberately bounded at
enforcement and recovery behaviors in a controlled model,               twelve unique eligible receipts per obligation; larger pools
including matched comparisons and observed effects. Oper-               return unknown. Exact cut computation is also combinatorial.
ational reliability still requires real workloads, deployment-          These measurements do not establish high-throughput behav-
level observers, and target-side concurrency tests.                     ior for large coalitions. Stronger witness search and durable
                                                                        replay protection cost more than an unchecked primitive call,
                                                                        and remote evidence acquisition may dominate both. A de-
10     Complete Local Execution Costs                                   ployment evaluation must measure that additional work and
                                                                        effect-time concurrency under its actual storage and service
We measure a complete local path on macOS/ARM64 with                    configuration.
Node.js v25.2.1 and an Apple M4 reported as ten logical                    The full-discharge sweep illustrates the cost of that bound:
CPUs. Three fresh processes each execute 1,000 measured                 per-process medians increase from 0.072–0.079 ms for one
iterations for workloads with one, four, or eight obligations           receipt to 67.31–72.69 ms for twelve. This supports explicit
and the corresponding number of distinct Ed25519-signed re-             admission input limits, not an extrapolation to thousands of
ceipts. Twenty warm-up iterations per workload are excluded.            receipts. Variation across the three full-path processes also
The archive retains all 9,000 measured samples and actual               cautions against treating a single median or p99 as a stable
host metadata. We do not assume an isolated host or pool                service-level objective.
process repetitions into a population confidence interval.

10.1    Measurement Boundary                                            11     Integration with Execution Systems
Each iteration resolves policy, discharges every required obli-         Admission and commitment address different stages of
gation, constructs the witness manifest, and mints a fresh              an operation within post-deterministic distributed systems
certificate. It then awaits a live-state JSON read from the             (PDDS) [1]. A migration can have a conflict-free read set
local filesystem and invokes the gateway with that new certifi-         yet lack a policy-required backup receipt. Conversely, an ad-
cate. The gateway checks signature, binding, authorization,             mitted migration can conflict with another transaction before
guards, time, and policy epoch; atomically creates a spent-             commitment. A CAC certificate therefore supplies authoriza-
nonce record; flushes the file and its directory; and invokes an        tion to attempt the bounded operation; the storage or workflow
instrumented target callback. Every iteration asserts success-          runtime must still enforce its own isolation and settlement
ful discharge, exactly one target call, successful dispatch, and        rules [8–10].
a consumed nonce. A subsequent replay rejection is checked
and timed separately.


                                                                   11
Target-side preconditions. A target that supports atomic                 Prototype scope. The corrected study uses independently
conditional mutation can check certified versions at the same            observed local state transitions, a live-policy comparator, and
linearization point as the effect. This covers only the pred-            matched interventions. Its target models still encode a small
icates represented by those preconditions. Checking one                  set of known preconditions and serialize each effect. They do
resource version does not atomically validate an arbitrary               not implement database replication, fencing, network parti-
multi-resource guard set. When guards span services, their               tions, or service recovery. The complete-path timings include
preservation requires a suitable transaction or coordination             real local file operations but an in-process target callback.
protocol; generic composition alone provides no serializabil-            These limits preclude claims of production reliability, model-
ity theorem.                                                             family generalization, economic savings, or high-throughput
                                                                         EFD scaling.
Capability gateways. CAC can supply the evidence-
discharge decision to a capability broker such as SAB [11].              Validation needed. A deployment evaluation should extend
The broker supplies authentication, confinement, and revoca-             the implemented observer and matched-schedule protocol to
tion; the admission policy supplies the required evidence and            separate services. It should include realistic safe workloads,
its interpretation. Such integration remains an architectural            expensive sensors, harmful partial failures, process crashes,
interface in this work, not an evaluated deployment.                     distributed replay stores, and post-forwarding races. The
                                                                         present multi-process replay test and performance repetitions
Policy updates. Learned lessons and incident analyses may                address local behavior; representative scenario sampling is
propose new obligations. They cannot alter the active pol-               still required for population inference. Comparisons should
icy without the governing approval process. Policy epochs,               also include a neighboring deterministic admission implemen-
evidence-source registrations, and envelope templates are                tation and real proposer/verifier execution. General envelope
trusted configuration. A revision to any of them may invali-             coverage needs a domain-specific proof or a checked coverage
date previously issued certificates.                                     relation before relaxed action binding is enabled.

                                                                         Long-running workflows. A single admission certifies one
12    Discussion and Limitations
                                                                         bounded dispatch. Multi-step migrations or progressive roll-
Policy adequacy. CAC exposes the obligations used to jus-                outs need fresh admission at relevant transitions and separate
tify an action; it does not infer a complete safety specification        recovery semantics. Continuous monitoring may complement
from natural-language intent. Policy authors must connect                that design, but its safety and liveness properties are outside
each obligation to a domain invariant and justify the associ-            the present model.
ated guards. An omitted dependency, permissive entailment
rule, or incomplete envelope proof can preserve syntactic                13    Related Work
admission correctness while permitting harm.
                                                                         Authorization and proof-carrying execution. Complete
Evidence trust. Signatures establish provenance under a                  mediation and separation of privilege are established protec-
key-trust model, not the truth of a sensor reading. Struc-               tion principles [2]. ABAC explicitly includes environmental
tural cuts provide a lower bound on modeled fault coverage               conditions [12]; it is not restricted to static identity checks.
only when exposure maps conservatively include the causes                CAC’s predicates can be implemented in a sufficiently expres-
of erroneous approval and the coalition rule matches actual              sive policy engine. The proposed distinction is the contract
authorization. Undisclosed common dependencies can invali-               for acquiring, retaining, and revalidating evidence for those
date that bound. Reconciliation can detect some discrepancies            predicates.
but cannot repair arbitrary coordinated falsehoods.                         Proof-carrying code requires an untrusted producer to pro-
                                                                         vide a consumer-checkable proof of compliance with a safety
                                                                         policy [3]. CAC shares that producer/checker separation. Its
Availability and cost. A conjunctive policy can block in-
                                                                         witnesses also include time-sensitive observations and policy-
definitely if a required witness is unavailable. Operational
                                                                         governed verifier receipts, which need not be formal proofs
budgets bound attempts but do not guarantee completion.
                                                                         of a program’s semantics. CAC adds a missing-evidence pro-
Recursive admission for consequential diagnostics needs a
                                                                         tocol and dispatch binding; it inherits rather than replaces the
well-founded dependency discipline or a bounded failure path.
                                                                         need to justify the consumer’s policy.
Evidence collection can dominate controller processing, and
false refusal matters as much as unsafe dispatch when evalu-
ating an operational system.                                             Agent admission and repair. Mnemosyne separates gener-
                                                                         ated proposals from deterministic admission under executable
                                                                         constraints and supports bounded repair, compensation, and


                                                                    12
active contract records [4]. These overlap directly with CAC’s           and persistent local replay protection. Controlled experiments
enforcement boundary and work loop. We therefore do not                  observe effects independently, isolate selected mechanisms,
claim deterministic admission, obligations, or repair in isola-          and measure the complete local dispatch path. CAC and a
tion as novel. CAC concentrates on risk-conditioned evidence             live-policy baseline achieve equal completion on the tested
selection, receipt-level freshness and provenance, and struc-            suite, while structural-cut enforcement blocks the constructed
tural witness requirements. Whether this interface improves              correlated-witness failure. CAC’s practical value now de-
upon a configured Mnemosyne-style runtime requires an im-                pends on whether deployed systems can obtain the required
plementation comparison absent from the current study.                   evidence at acceptable cost while completing useful work
                                                                         under realistic faults.
Commitment and freshness. Commit-time authorization                      AI-Use Disclosure. OpenAI Codex and Google Antigravity
binds durable effects to authority evidence that remains                 assisted with LaTeX formatting, draft structuring, language
eligible at commitment [13]. CAC shares freshness and                    editing, implementation and test development, notation and
effect-binding requirements but specifies which evidence                 schema consistency checks, analysis scripting, and figure
must first be acquired. Pre-dispatch checking is weaker than             preparation. The authors remain responsible for the study,
commitment-time checking unless the target preserves the                 code, and reported results. All reported measurements come
bound conditions. Atomix coordinates effect grouping and                 from executed code and frozen artifacts rather than model-
progress-aware settlement [10]; database concurrency control             generated estimates.
supplies separate isolation mechanisms [8, 9]. Admission
does not subsume either form of settlement.                              References
Verifier structure and capabilities. The structural-cut def-              [1] Jun He and Deying Yu. Post-deterministic distributed
inition and fault-coverage bound are imported from EFD [7],                   systems: A new foundation for trustworthy autonomous
whose controller already enforces cuts for quorum admis-                      infrastructure. arXiv preprint arXiv:2606.01722, 2026.
sion. CAC integrates that requirement with other typed obli-
gations; it does not introduce EFD-based admission itself.                [2] Jerome H. Saltzer and Michael D. Schroeder. The pro-
Capability boundaries such as SAB [11] address the broker                     tection of information in computer systems. Proceed-
and credential interface. Their enforcement properties remain                 ings of the IEEE, 63(9):1278–1308, 1975.
independent deployment assumptions here.                                  [3] George C. Necula. Proof-carrying code. In Proceed-
                                                                              ings of the 24th ACM SIGPLAN-SIGACT Symposium on
Reasoning and verification. ReAct interleaves reasoning                       Principles of Programming Languages, pages 106–119,
and actions, Reflexion uses feedback, and process supervision                 1997.
and test-time compute can improve reasoning quality [5, 14–
                                                                          [4] Edward Y. Chang, Longling Geng, and Emily J. Chang.
16]. CAC can consume evidence produced by such methods.
                                                                              Mnemosyne: Agentic transaction processing for vali-
Its logical separation result says that resource allocation alone
                                                                              dating and repairing AI-generated workflows. arXiv
does not certify an external condition; it does not show that
                                                                              preprint arXiv:2607.00269, 2026.
these methods are ineffective, nor does the scripted B0–B5
comparison measure them.                                                  [5] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Ku-
                                                                              mar. Scaling LLM test-time compute optimally can be
                                                                              more effective than scaling model parameters. arXiv
14    Conclusion
                                                                              preprint arXiv:2408.03314, 2024.
Cognitive Admission Control makes evidence requirements                   [6] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
explicit at the execution boundary between autonomous agent                   Bosma, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou.
proposals and external services in agentic distributed sys-                   Chain-of-thought prompting elicits reasoning in large
tems. A policy maps action risk to typed obligations; the                     language models. Advances in Neural Information Pro-
controller distinguishes satisfied, violated, and unresolved                  cessing Systems, 35:24824–24837, 2022.
conditions, requests missing evidence, and binds a successful
evaluation to a scoped certificate and dispatch guards. Its               [7] Jun He and Deying Yu. The illusion of independent
guarantees concern admission and mediated dispatch under                      quorums: Epistemic fault domains and correlated cog-
stated assumptions. Physical safety additionally depends on                   nitive failures in agentic quorums. arXiv preprint
the adequacy of the policy, evidence sources, environment                     arXiv:2609.02925, 2026.
model, and target-side enforcement.                                       [8] H. T. Kung and John T. Robinson. On optimistic meth-
   The repaired TypeScript prototype exercises bounded wit-                   ods for concurrency control. ACM Transactions on
ness search, independently bound certificates, live guards,                   Database Systems, 6(2):213–226, 1981.


                                                                    13
 [9] Dan R. K. Ports and Kevin Grittner. Serializable snap-              For Proposition 1, take f (x, y) = x + y, threshold 1, and
     shot isolation in PostgreSQL. Proceedings of the VLDB            require x ≥ 1. Along (0, n) the required condition fails
     Endowment, 5(12):1850–1861, 2012.                                while the score eventually exceeds the threshold. In contrast,
                                                                      the scalar indicator 1[x ≥ 1 ∧ y ≥ 1] faithfully represents
[10] Bardia Mohammadi, Nearchos Potamitis, Lars Klein,                conjunction. The issue is substitutability, not scalar notation
     Akhil Arora, and Laurent Bindschaedler. Atomix:                  itself.
     Timely, transactional tool use for reliable agentic work-
     flows. arXiv preprint arXiv:2602.14849, 2026.
                                                                      A.2   Monotonicity Scope
[11] Jun He and Deying Yu. Sovereign assurance boundary:
                                                                      The threshold proposition fixes the rule base and all non-risk
     Certificate-bound admission for agentic infrastructure.
                                                                      inputs. A policy that removes a backup obligation when a
     arXiv preprint arXiv:2606.11632, 2026.
                                                                      new emergency flag becomes true is not covered even if its
[12] Vincent C. Hu, David Ferraiolo, Rick Kuhn, Adam                  risk estimate increases. Similarly, replacing a five-second
     Schnitzer, Kenneth Sandlin, Robert Miller, and Karen             freshness obligation by a one-second obligation strengthens
     Scarfone. Guide to attribute based access control                policy semantically but does not preserve literal identity of
     (ABAC) definition and considerations. Technical Re-              obligation records.
     port SP 800-162, National Institute of Standards and
     Technology, 2014. Updated August 2019.                           A.3   Quorum Extension
[13] Igor Santos-Grueiro. Temporary authority, permanent              Let Q = {a, b, c} use a two-of-three rule with D(a) =
     effects: Commit-time authorization for LLM agents.               D(b) = {f } and D(c) = {g}. Coalition {a, b} is decisive
     arXiv preprint arXiv:2607.10487, 2026.                           and covered by {f }, so κE = 1. Add d with exposure {h}
                                                                      while keeping a two-vote threshold. Coalition {a, b} remains
[14] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak                 decisive, hence the cut remains one. An independent new
     Shafran, Karthik Narasimhan, and Yuan Cao. ReAct:                source cannot repair a coalition rule that still permits approval
     Synergizing reasoning and acting in language models.             by the original correlated pair.
     arXiv preprint arXiv:2210.03629, 2022.                              By contrast, requiring both members of {c, d} gives a cut
[15] Noah Shinn, Federico Cassano, Ashwin Gopinath,                   of two when their exposure sets are disjoint and the declared
     Karthik Narasimhan, and Shunyu Yao. Reflexion:                   basis covers all error causes. This is a property of the coalition
     Language agents with verbal reinforcement learning.              structure and exposure model together.
     Advances in Neural Information Processing Systems,
     36:8634–8652, 2023.                                              A.4   Conflicts, Expiration, and Envelopes

[16] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri              If equally preferred valid witnesses support opposite polari-
     Edwards, Bowen Baker, Teddy Lee, Jan Leike, John                 ties, deterministic tie-breaking must not select a polarity by
     Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify           receipt identifier. The verdict is unknown; identifier order-
     step by step. arXiv preprint arXiv:2305.20050, 2023.             ing may select a canonical witness only after the semantic
                                                                      decision.
                                                                         A receipt dated after the evaluation instant satisfies an
A     Formal Boundary Examples                                        upper-age bound alone, even if arbitrarily far in the future.
                                                                      The lower bound in Equation (9) excludes it. Cross-host time
A.1   Projection and Budget Counterexamples
                                                                      comparison requires the declared normalization assumptions.
For Theorem 1, consider two snapshots with the same prin-                Finally, an exact proposal digest prevents substitution but
cipal, database identifier, and failover permission. The can-         does not derive a missing guard. If a policy omits primary
didate is fenced in one snapshot and unfenced in the other.           fencing, hashing the exact failover request does not make the
Authorization based on those shared fields cannot distinguish         omission safe. Envelope soundness requires witness cover-
them. The conclusion requires a sound fencing obligation; a           age and guard completeness in addition to syntactic action
falsely signed assertion can defeat the safety premise while          binding.
preserving syntactic admission.
   For Theorem 2, let both procedures have access to one              A.5   Bounded Exhaustive Cross-Checks
observation call. One calls a source that establishes the sole
required predicate; the other reads unrelated documentation.          The independent script scripts/check_finite_
Equal allocation permits different evidence outcomes. If the          model.py enumerates three voters and three modeled roots,
required source is inaccessible to both, the example does not         all 343 nonempty exposure profiles, and all 127 nonempty
establish that either can obtain admission.                           families of nonempty coalitions. Across 43,561 profile/rule


                                                                 14
{                                                                        C    Open Problems
    "id": "replication-current",
    "kind": "OBSERVE",                                                   Guard sufficiency. Automatically deriving a minimal guard
    "predicate": "replication_lag_bytes <= 0",
    "target": "cluster.candidate",
                                                                         set requires a semantic connection from each witness to the
    "scope": ["postgres/prod-cluster-a"],                                state on which its claim depends. A dependency annotation
    "maxFreshnessMs": 2000,                                              supplies a candidate, not a proof that all relevant changes
    "evidenceClasses": ["POSTGRES_TELEMETRY"],                           are covered. Multi-resource guards also need a target-side
    "efdRequirement": null,
    "setConstraints": null,
                                                                         preservation mechanism.
    "enforcement": "REQUIRED"
}                                                                        Conservative risk classification. The policy must account
Listing 1: Illustrative replication observation obligation; the          for indirect effects and incomplete dependency graphs. A
two-second horizon is a policy example, not an evaluated                 typed operation narrows the interpretation problem but does
optimum.                                                                 not determine all consequences. Unknown scope or unre-
                                                                         solved aliases should produce a conservative bound or escala-
                                                                         tion, not an unqualified low-risk classification.
combinations and 348,488 fault states, minimum coalition
coverage agrees with direct propagation of faults to voters,
                                                                         Bounded evidence search. General witness selection and
and no sub-cut fault set covers a decisive coalition. The
                                                                         fault-cut computation can be combinatorial. An implemen-
script also verifies the quorum-extension counterexample
                                                                         tation needs a restricted evidence language and explicit re-
and threshold monotonicity for all 216 comparable pairs in a
                                                                         source bounds. A useful research target is a sound conserva-
three-coordinate, three-level risk domain. These finite checks
                                                                         tive approximation that improves availability without treating
supplement the arguments above; they neither prove the
                                                                         incomplete search as proof of satisfaction.
unbounded results nor test the TypeScript implementation.

                                                                         Remediation liveness. A diagnostic action can depend on
B     Illustrative Policy Contract                                       admission of another diagnostic action. Shared budgets bound
                                                                         attempts, but deadlock freedom and successful completion
A failover policy should distinguish the observed lag con-
                                                                         require additional assumptions about the dependency graph,
dition from the fencing condition. The following design
                                                                         sensor availability, and environmental stability.
example uses fields corresponding to the prototype’s obli-
gation records. It is an excerpt, not a complete deployable
profile; source registration, predicate interpretation, version          Fault-profile validation. Exposure maps must match actual
compatibility, and guard bindings must also be supplied.                 evidence paths and authorization coalitions. Attestation may
   The claim must identify the primary and candidate and the             establish a declared configuration, while empirical correla-
replication positions it compares. A role-only observation               tion studies can expose some missing dependencies. Neither
cannot establish this predicate. Policy separately requires              method by itself proves that all common causes have been
evidence that the old primary is fenced and that the chosen              enumerated.
target remains the intended standby. Guards must preserve the
relevant conditions or translate them into target-side atomic
preconditions. Zero observed lag at one instant does not by
itself exclude a concurrent write before fencing.
   A simple trace illustrates the three discharge outcomes.
With no receipt, the replication obligation is unknown and the
controller requests telemetry. An eligible receipt affirmatively
showing positive lag violates this example’s zero-lag require-
ment. An eligible zero-lag receipt satisfies this obligation, but
admission still waits for fencing and every other required con-
dition. A valid certificate becomes unusable when a bound
version changes or the earliest supporting receipt expires.
   The archived R1 fixture uses a positive lag tolerance and a
fixed safe oracle. The corrected local study evaluates a literal
zero-lag predicate and observes target effects separately, but
its serial transition model does not validate primary fencing
or exclude concurrent writes in a real database.



                                                                    15
