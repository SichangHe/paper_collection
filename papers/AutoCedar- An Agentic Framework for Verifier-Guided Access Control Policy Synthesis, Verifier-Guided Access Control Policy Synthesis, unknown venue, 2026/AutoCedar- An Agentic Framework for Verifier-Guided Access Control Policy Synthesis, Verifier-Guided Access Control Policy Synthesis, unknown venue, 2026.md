                                                AUTO C EDAR: An Agentic Framework for
                                             Verifier-Guided Access Control Policy Synthesis
                                                                     Adarsh Vatsa, Sachi Shome, Yingming Zhou, and William Eiers
                                                                                          Stevens Institute of Technology
                                                                                 {avatsa, sshome, yzhou136, weiers}@stevens.edu


                                           Abstract—Large Language Models are increasingly used to            internal signal for whether a rule matches intent. Automated
                                        turn natural-language requirements into code. In access control,      vulnerability discovery throws the resulting gap into relief
                                        that shortcut is dangerous: a generated policy can compile and        rather than closing it: Anthropic’s Project Glasswing reports
                                        read correctly while granting access that no one approved. The
                                        difficulty is not only writing policy code. It is fixing what the     that around fifty partners using Claude Mythos have found
                                                                                                              more than ten thousand critical vulnerabilities in important
arXiv:2607.03656v1 [cs.SE] 4 Jul 2026




                                        requirements mean before code is written, and then checking
                                        that the final policy actually satisfies that intent. We present      software, and similarly a parallel scan of over a thousand open-
                                        AUTO C EDAR, a verifier-guided system that first turns natural-       source projects surfaced 6,202 high or critical findings out of
                                        language access-control requirements into a reviewed, checkable       23,019 candidates, yet the disclosed bugs are overwhelmingly
                                        target, and then synthesizes Cedar policies against that target.
                                        AUTO C EDAR decomposes schema and policy authoring into small         memory-safety failures and cryptographic defects, with autho-
                                        intent atoms: reviewable claims about vocabulary and behavior.        rization logic barely represented [3]. The reason is structural:
                                        Once those atoms pass mechanical validation and human intent          a memory bug carries its own ground truth, since a buffer
                                        review, the model proposes a candidate policy, the verifier checks    overflow trips a sanitizer and crashes with no statement of
                                        it against the approved target, and each failure is turned into a     intent required, while “user A can read user B’s record” is
                                        repair signal that tells the model whether to broaden, narrow,
                                        or restructure the policy without changing the target. Because        a defect only relative to a policy the code never states. The
                                        the model’s work is split into small problems, each grounded          moment when more authorization logic is being written by
                                        in reviewed intent and backed by verifier feedback, end-to-end        fewer human eyes is also the moment when the field’s most
                                        policy authoring becomes tractable. AUTO C EDAR converges on          powerful bug-finders are least able to catch it. Which makes
                                        all 221 tasks of CedarBench, our benchmark of authorization           correctness at authoring time, not detection after deployment,
                                        tasks paired with executable semantic boundaries. Across three
                                        requirements-corpus case studies covering healthcare, education,      the place where the leverage actually lies.
                                        and conference management, AUTO C EDAR converts noisy prose              A natural tool for authoring-time correctness is the large
                                        and extracted access-control fragments into reviewed schemas,         language model, which can turn natural-language requirements
                                        formal checks, and a globally verified Cedar policy store for         into policy text directly [4], [5]. But a model can produce a
                                        each scenario.                                                        syntactically valid, plausible-looking policy that is semanti-
                                                                                                              cally wrong, with no internal signal that anything is off: Vatsa
                                                               I. I NTRODUCTION
                                                                                                              et al. [5] report that policies written via roundtrip generation
                                           Access control is ubiquitous across deployed software sys-         have semantic equivalence rates of 45.8% for non-reasoning
                                        tems, yet the gap between natural-language access control             models and 93.7% for reasoning models relative to the ground-
                                        requirements and the formal policies that enforce them remains        truth policies. A natural response is to pair the model with a
                                        a persistent source of misconfiguration and vulnerability. This       verifier, so that correctness guarantees come from the verifier
                                        gap makes access control the most common source of security           rather than the model, separating generation from checking.
                                        failures: it ranks first in the OWASP Top 10 and appeared in          We argue this is only half of the problem: the requirements
                                        every tested application in their survey [1]. What makes these        themselves are usually incomplete, leaving cases unsaid. No
                                        failures so persistent is not that any single access control rule     amount of verification against an under-specified, informal
                                        is hard to write; individual rules can look reasonable while          intent can fill that gap. The Cedar [6] policy language makes
                                        combining to permit or deny requests no author intended.              verification more tractable since policies are declarative, typed
                                        Instead, it is that correctness is a property of the entire system:   against an explicit schema, and open to symbolic comparison
                                        a policy is correct only when its entire set of rules, taken          so the property we want is not that a generated policy looks
                                        together, permits exactly the requests it should and no others.       reasonable, but that the set of requests it permits falls inside
                                           This problem compounds in modern software development,             a reviewed authorization boundary. This boundary does not
                                        where AI tools now author a large and growing share of                exist in ordinary requirements text; it has to be constructed,
                                        committed code. Fewer than half of developers say they always         reviewed, and kept fixed while the policy is synthesized.
                                        verify AI-generated code before it ships, and a substantial              In this work we present AUTO C EDAR, which constructs that
                                        share report that reviewing it takes more effort than reviewing       reviewed boundary by completing intent rather than merely
                                        human-written code [2]. Authorization logic is not exempt:            translating requirements into policy text. Instead of treating the
                                        more of it is being generated, faster, by systems with no             requirements as a finished specification, AUTO C EDAR surfaces
their gaps during authoring: when the requirements leave                 Policies. A Cedar policy π is a set of one or more declarative
something unsaid, a property the schema cannot yet support            rules which describes what principals can perform which
triggers a repair that the reviewer resolves, so the intent is com-   actions on which resources in what context. π specifies the
pleted before the policy is finalized rather than left implicit.      effect, scope, and optional conditions:
AUTO C EDAR converges on all 221 tasks of CedarBench,
our benchmark of authorization tasks paired with executable           effect (principal, action, resource)[when φ1 ][unless φ2 ]
semantic boundaries, and across three ACRE/REDE-derived               where effect ∈ {permit, forbid}; scope restricts which
requirements corpora for healthcare, education, and conference        principals, actions, and resources the policy applies to; φ1 ,φ2
management it turns fragments that cannot be deployed on              are boolean conditions over entity attributes drawn from Σ.
their own into globally checked Cedar policy stores. Because
that completed intent is recorded explicitly rather than baked        B. Terminology
silently into the final rules, AUTO C EDAR also produces a               Requests, schemas, and policies. We write a Cedar au-
durable, updatable log of intent: when requirements change,           thorization request as ρ = (p, α, o, γ): principal, action,
the log is edited and a fresh, verified policy is re-authored from    resource, and context. For a fixed schema Σ, these declarations
it, making the system not a one-shot synthesizer but a substrate      induce the request universe RΣ , the domain over which every
for ongoing policy maintenance. It thus turns text expressing         comparison, witness, and certification claim is quantified. A
access-control intent, in any format, into deployable, verified       policy bundle P is a finite set of permit and forbid rules
Cedar. The contribution is the boundary-preserving authoring          guarded by Cedar conditions.
loop: AUTO C EDAR fixes what the policy is supposed to mean,             Permit-set denotation. Once Σ fixes the universe, two
keeps that target outside the model’s control, and uses verifier      policy texts should be compared by behavior. Cedar uses deny-
evidence to search for policy code that satisfies it.                 overrides semantics: a request is permitted only when at least
    Contributions. We make four contributions.                        one matching permit applies and no matching forbid
    1) AUTO C EDAR, a verifier-guided authoring loop that turns       applies. We write semΣ (P ) = {ρ ∈ RΣ | permitΣ (P, ρ)}
       fragmented natural-language access-control intent into a       for the permit-set denotation of P , writing sem(P ) when Σ
       reviewed Cedar schema and boundary plan of floors,             is fixed. Two different Cedar encodings are equivalent for
       ceilings, liveness slices, and derived checks.                 synthesis when they permit exactly the same requests.
    2) A CEGIS-style synthesis discipline for LLM policy gen-            Symbolic policy comparison. Cedar comes with a symbolic
       eration: the model proposes candidates, the verifier owns      compiler cedar symcc which translates Cedar policies into
       the target, failure history, and accept/reject decision.       SMT formulae, enabling comparison between policies through
    3) A signal-layer contract that translates verifier evidence      formulae satisfiability. symcc allows us to compare the permit
       into target-preserving repair packets across target admis-     sets over the supported Cedar fragment rather than over a finite
       sion, semantic direction, local Cedar diagnostics, and         test suite. For policy bundles P1 and P2 , it can decide inclusion
       search history.                                                sem(P1 ) ⊆ sem(P2 ), equivalence sem(P1 ) = sem(P2 ), and
    4) CedarBench, a 221-scenario verification benchmark,             satisfiability or emptiness properties; when an inclusion check
       plus three ACRE/REDE-derived case studies showing              fails, it returns a concrete request in the relevant set difference.
       end-to-end transformation from NL/NLACP intent into            This follows the same lineage as SMT-based policy analyzers
       deployable, globally checked Cedar policy stores.              such as Zelkova [8]. The property we use is that many
The implementation, benchmarks, and reproduction                      requirements can themselves be encoded as Cedar policies.
materials are available at https://github.com/neselab/                                       III. AUTO C EDAR
cedar-synthesis-engine.
                                                                         AUTO C EDAR starts from a problem that a direct translator
           II. BACKGROUND AND P RELIMINARIES                          cannot solve: policy text cannot be checked until the intended
                                                                      behavior has been made checkable. The system therefore has
A. Cedar Policy Language
                                                                      two jobs. First, it turns requirements into a reviewed semantic
   Cedar is a language for writing authorization policies and         target over a Cedar schema. Then it lets an LLM search for
making authorization decisions based on those policies [6],           policy text while a verifier checks candidates against the target.
[7]. We now summarize the relevant elements of Cedar below.
   Schema. A Cedar schema Σ fixes the vocabulary that                 A. Overview
policies are permitted to reference. It defines the types of             The failure mode of direct LLM synthesis is simple: policy
entities recognized by the application or context in which the        text gets written before intent is fixed. AUTO C EDAR reverses
policy operates. The entities include principals (who is doing        this order, turning requirements into a reviewed, checkable
the access), actions (what is being performed), resources (what       target before the model proposes any candidate.
is being accessed), and context (environment information)                Figure 1 shows the full workflow, and Algorithm 1 spells
referenced in policies. Cedar uses Σ to validate policies at          out the control flow. Requirements enter as a document D.
authoring time, ensuring that every entity, attribute, and action     AUTO C EDAR indexes D into a source DAG GD , then pro-
a policy references is consistent with Σ.                             poses schema atoms and property atoms from bounded source
                  Reviewed target: fixed before candidate search

                      GD                A                    Σ                 Π                     F , C, G
                  source DAG      approved atoms          schema              plan                compiled checks

                                                                                fixed target
                  Untrusted proposal, deterministic checking

                      mt                LLM                 Pt               Cedar                  Qt           all pass     evidence
                     repair           proposer           candidate          checker               records                   (Σ, Π, P, T )
            next mt+1                                                                                 failures
                                                                                                                             T trace
                        signal layer Φ: outcome class, direction, witness, provenance, history                      source → atom → boundary
                                                                                                                     check → candidate clause

Fig. 1. AUTO C EDAR as fixed-target construction plus verifier-guided search. Raw requirements D are indexed into a source DAG GD : stable source nodes
and bounded context packets used to propose atoms. A is the set of approved schema and property atoms, Σ is the Cedar schema, Π is the boundary plan, and
F , C, G are the approved floors, ceilings, and liveness slices. Some review-level constraints are derived: they are checked only after AUTO C EDAR compiles
them into primitive verifier obligations. The model proposes candidates Pt from repair packets mt , while the Cedar checker validates Pt and runs cedar
symcc to produce check records Qt against the fixed plan. The signal layer Φ turns failed records into the next repair packet; passing records produce an
evidence package whose trace T records source spans, atoms, boundaries, checks, and associated candidate clauses.



packets. A reviewer accepts only atoms that match the intended                 Algorithm 1 AUTO C EDAR synthesis workflow
behavior; approved schema atoms compile into a schema Σ,                       Require: Access-control requirements D; iteration budget K
                                                                               Ensure: Verified evidence package (Σ, Π, P, T ) or a reportable failure
and approved property atoms compile into a boundary plan                        1: Index D into source DAG GD with source nodes and bounded context
Π. Only then does candidate-policy search begin: the model                         packets
proposes policy bundle Pt , the verifier produces check records                 2: Propose and review schema atoms from source packets
                                                                                3: Propose property atoms one packet at a time with coverage tracking
Qt , and the signal layer turns failed records into the next repair             4: while a property exposes missing schema support or target conflict do
packet mt+1 . Success is a Cedar file plus evidence that it                     5:    Repair schema or property atoms; rerun mechanical and intent review
satisfies the fixed target.                                                     6: end while
                                                                                7: Compile approved atoms into schema Σ and boundary plan Π
   AUTO C EDAR does not prompt over D as one undiffer-                          8: if Σ fails validation or admission checks reject Π then
entiated blob. Instead, it uses GD : stable source nodes and                    9:    return target-admission failure with reviewer-facing diagnostics
                                                                               10: end if
bounded context packets that keep each proposal tied to a                      11: H ← ∅; m ← summary of the fixed target
local, auditable slice of the requirements. Schema atoms say                   12: for t = 1 to K do
what exists in the authorization world: users, documents, roles,               13:    Ask the model for a candidate policy Pt using repair packet m
                                                                               14:    if Pt does not parse or type-check under Σ then
actions, attributes, and context fields. Property atoms say what               15:       m ← local diagnostic repair packet for Pt
behavior should hold over that world: which requests must                      16:    else
be allowed, which requests must not leak through, which                        17:       Qt ← verifier records for checking Pt against Π
                                                                               18:       if all records in Qt pass then
workflow classes must remain possible, and which constraints                   19:           Record trace T with source spans, atoms, boundaries, records,
should compile into verifier checks. The human review step                                   and associated clauses
decides whether those atoms capture the intended behavior.                     20:           return (Σ, Π, Pt , T )
                                                                               21:       end if
   The target is not fixed after the first pass of review. During              22:       m ← Φ(Qt , Pt , Π, H)
target construction, AUTO C EDAR may discover that a property                  23:    end if
atom needs schema support the current schema does not                          24:    Append the candidate, diagnostics or verifier records, and m to H
                                                                               25: end for
provide, that a current property should be rejected or repaired,               26: return budget failure with target, history, and verifier records
that a prior property now conflicts with the emerging target,
or that an approved source node still lacks coverage. These                    is the evidence trace recording source text, approved atoms,
repairs happen before candidate-policy search. The fixed target                boundaries, verifier records, and candidate clauses associated
begins only after schema repair, property repair, coverage                     with those records.
accounting, and admission checks have produced an approved
Cedar schema Σ and boundary plan Π. The LLM then has a                         B. Verification-Guided Search
narrower job: propose a candidate Cedar policy Pt under that                      The verifier cannot check a candidate against the original
fixed target. The verifier checks the candidate against the entire             prose. It needs a semantic target. In this setting, that tar-
plan. If the candidate is too broad, too narrow, syntactically                 get is not a preexisting reference implementation, because
invalid, or has made an approved workflow impossible, AU -                     writing the implementation is the problem. AUTO C EDAR
TO C EDAR sends the model a repair packet rather than a vague                  instead builds a reviewed boundary of acceptable behavior. A
failure message. If every check passes, AUTO C EDAR returns                    boundary is necessary because two Cedar policies can express
(Σ, Π, P, T ), where Σ is the Cedar schema, Π is the approved                  the same access-control behavior with different clauses, and
boundary plan, P is the synthesized policy bundle, and T                       two policies that look almost identical can permit different
requests. A single golden policy would make the target too
                                                                                                                   TIGHTEN
                                                                                                                                      RΣ requests
brittle. A boundary lets the verifier ask the question that
matters: is the candidate inside the approved behavior and does
                                                                              UΠ ceiling
it include the required behavior?                                             maximum approved access
   Once a schema Σ fixes the typed request universe RΣ , every
candidate policy bundle P denotes a set of permitted requests                                         candidate
                                                                                                      sem(Pt )
sem(P ) ⊆ RΣ . The primitive plan asks three questions about
that set. What must be inside it? What must stay outside                               LOOSEN                                EXPAND

it? What workflow class must not be emptied? AUTO C EDAR                                         LΠ floor                     Gk
represents those answers as a boundary plan Π = (C, F, G)                                     required access            live workflow
where C is a set of ceiling policies, F is a set of floor
policies, and G is a set of reviewed liveness slices. Each ceiling
Ci says that a candidate must not permit requests outside
sem(Ci ). Each floor Fj says that a candidate must at least          Fig. 2. The synthesis sandwich. The dashed rectangle is an intermediate
include sem(Fj ). Each liveness slice Gk ⊆ RΣ says that an           candidate: it must stay inside the ceiling envelope, grow to include required
approved request class cannot disappear. The third case matters      access, and hit each live workflow slice. Final acceptance requires LΠ ⊆
                                                                     sem(P ) ⊆ UΠ and sem(P ) ∩ Gk ̸= ∅. The same verifier call therefore
because a policy that denies everything can satisfy many safety      induces different repair directions: a request outside the ceiling tightens, a
constraints while still being useless.                               missing floor loosens, and an empty liveness slice expands.
   Beyond the primitive plan, AUTO C EDAR also accepts au-
thoring conveniences (such as disjointness and rate-limit-style      Theorem 1 (Synthesis sandwich). A candidate policy bundle
intent) that it grounds, reviews, and compiles into checks           P satisfies Π iff
or patches over Π when their meaning is expressible in it.            LΠ ⊆ sem(P ) ⊆ UΠ             and         ∀Gk ∈ G. sem(P ) ∩ Gk ̸= ∅.
They extend what the author can state rather than what the
plan represents. Disjointness is especially important for global     Proof.
                                                                     S       The floor clauses of Definition 1 are equivalent to
policy stores: it can patch same-action floors so that one             Fj ∈F sem(Fj ) ⊆ sem(P ), which is LΠ ⊆  T sem(P ). The
approved workflow does not accidentally permit a mutually            ceiling clauses are equivalent to sem(P ) ⊆ Ci ∈C sem(Ci ),
exclusive one. Rate-limit-style atoms are governed by the same       which is sem(P ) ⊆ UΠ . The liveness clauses are unchanged
discipline: they contribute only through the finite, verifier-       by the definition of LΠ and UΠ . Combining the three equiva-
facing obligations that AUTO C EDAR can compile from the             lences gives the result.
reviewed atom, not through a claim about runtime enforcement
outside Cedar’s policy semantics.                                       The theorem says exactly what the verifier certifies at the
                                                                     end of a run: the final policy is no smaller than the approved
Definition 1 (Plan satisfaction). For a permit set S ⊆ RΣ ,          floors, no larger than the approved ceilings, and not empty
write S |= Π iff                                                     on any approved liveness slice. Floors and ceilings form the
                  ∀Ci ∈ C. S ⊆ sem(Ci ),                             sandwich in Fig. 2. Liveness prevents the sandwich from being
                  ∀Fj ∈ F. sem(Fj ) ⊆ S,                             satisfied by a policy that silently drops a required workflow.
                  ∀Gk ∈ G. S ∩ Gk ̸= ∅.                                 Plan compatibility. Some targets are broken before the
                                                                     first LLM call. A reviewer may approve a floor that a ceiling
A candidate policy bundle P satisfies Π, written P |= Π, iff         forbids, or a liveness slice that lies entirely outside the upper
sem(P ) |= Π.                                                        bound. In those cases the problem is not that the model needs
                                                                     a better prompt. The target itself must be repaired. At the set
   Definition 1 is the point where the prose target becomes
                                                                     level, the ideal compatibility condition is simple:
something the verifier can own: a candidate is too permissive
when it escapes a ceiling, too restrictive when it misses a floor,              LΠ ⊆ UΠ         and      ∀Gk ∈ G. UΠ ∩ Gk ̸= ∅.
and has lost an approved workflow when it fails to intersect
a liveness slice. These are not different phrasings of the same      The first clause says the required requests fit inside the
error; they are different semantic failures.                         approved upper bound; the second says every approved live-
   The admissible interval. The candidate policy must exist          ness slice is reachable somewhere inside that bound. This
between these two bounds: it must be permissive enough to            condition abstracts away Cedar syntax, so it should not be
include all floors and restrictive enough not to exceed any          read as an implementation claim that AUTO C EDAR solves
ceiling. Let                                                         a complete global feasibility problem. The current system
                \                           [                        uses verifier-backed admission checks: schema validation,
        UΠ =        sem(Ci ),      LΠ =        sem(Fj ),             boundary validation, pairwise floor-versus-ceiling checks after
              Ci ∈C                       Fj ∈F                      derived-constraint compilation, identity-consistency checks,
with the usual conventions that an empty ceiling intersection        and liveness and probe checks. These are target-admission
is RΣ and an empty floor union is ∅.                                 checks, not repair packets. They use some of the same verifier
                                                                     machinery that the signal layer later uses, but they run before
search and decide whether the target is coherent enough to               Reviewers are not asked to certify an unchecked generated
give to the model at all. If they fail, AUTO C EDAR reports a         policy. They approve the target that the verifier will later
target-construction problem to the reviewer instead of asking         enforce. When two admissible Cedar encodings of the same
the LLM to synthesize around an impossible plan.                      intent behave differently, AUTO C EDAR can present the differ-
                                                                      ence as a request rather than as a Cedar diff: for example,
Proposition 1 (Conditional soundness). If AUTO C EDAR re-
                                                                      whether a role-scoped user may read a sensitive field under
turns a policy bundle P for an approved plan Π, then the
                                                                      a particular context. The reviewer chooses behavior, and the
returned artifact has passed Cedar validation, and cedar
                                                                      chosen behavior becomes part of Π.
symcc has certified the inclusion checks in Theorem 1 and the
                                                                         After synthesis, the trace T records source spans, approved
implemented liveness checks in Π. Consequently, the returned
                                                                      atoms, boundary policies, verifier records, and the candidate
policy is semantically valid with respect to the approved
                                                                      clauses associated with those records. It is an audit aid, not a
boundary plan: it stays within all ceilings, includes all floors,
                                                                      proof of clause provenance. It lets a reviewer ask why a clause
and passes the approved liveness checks. Validity with respect
                                                                      was included and which approved boundary it helped satisfy,
to organizational intent holds only under the explicit assump-
                                                                      while the semantic guarantee still comes from the verifier.
tion that the human-approved plan accurately captures that
                                                                      Benchmark runs may use simulated review as a measurement
intent. AUTO C EDAR makes no stronger claim. A compatible
                                                                      instrument, but those runs do not create intent authority. The
plan may still lack a concise Cedar implementation, or the
                                                                      correctness claim rests on human-approved targets.
model may fail to find one within budget.
C. Intent Construction and Review                                     D. Signal-Layer
   A verifier can say that P |= Π, but it cannot say whether             The first failed candidate is where verifier-guided synthesis
Π was the right plan. That judgment belongs before search,            is most prone to misdirection. The verifier can be completely
because once the plan is approved every later guarantee               precise and still not tell the model what to do next. A failed
is relative to it. AUTO C EDAR therefore makes human re-              check might mean that the target itself is broken, that the
view attach to behavior rather than to final Cedar syntax.            candidate is too broad, that it is too narrow, that it cannot type-
During target construction, each atom is proposed from a              check, that a reviewed workflow has disappeared, or that the
bounded source packet and carries source-node attribution.            model is cycling through the same bad repair. If AUTO C EDAR
AUTO C EDAR formalizes each reviewable unit as an atom                sends these outcomes back as one generic rejection, the model
a = (s, k, u, z, σsym , σintent ), where s is the source span or      can move in exactly the wrong direction: loosen a ceiling
source-node set, k is the atom kind, u is the plain-English           failure, tighten a floor failure, or remove the workflow the
rendering shown to the reviewer, z is the Cedar artifact or           reviewer wanted preserved.
schema edit, σsym is the mechanical status, and σintent is               The signal layer is the translation boundary that prevents
the review status. An atom enters the approved atom set iff           this collapse. It does not make the verifier stronger. It makes
σsym (a) = pass and σintent (a) = accept. σsym says z is well         verifier evidence usable without letting that evidence rewrite
formed under Cedar syntax, typing, and boundary-admission             the reviewed target. A signal record is a typed object q =
checks. σintent says that the reviewer accepts u as the intended      (ℓ, o, τ, κ, w, e), where ℓ says which layer produced the record,
interpretation of the source span. Neither status implies the         o names the oracle or check, τ records the boundary or
other, and only approved atoms contribute to Σ or Π.                  diagnostic kind, κ records the relation being tested, w is any
   The split between schema atoms and property atoms is not           witness or counterexample, and e is localization evidence such
bookkeeping. A schema atom decides what concepts exist in             as a candidate/reference excerpt, diff, or diagnosis. AUTO -
the policy world: entity types, actions, attributes, relationships,   C EDAR then computes Φ(Qt , Pt , Π, Ht ) → mt+1 , from the
and context fields. It authorizes no request by itself. A property    current records Qt , failed candidate Pt , approved plan Π, and
atom decides behavior over that vocabulary: a floor, a ceiling,       search history Ht . The output is the next repair packet. The
a liveness slice, or a derived constraint such as disjointness        packet may select, normalize, compress, and order evidence.
that compiles into verifier-facing checks. A correct-looking          It may not mutate Π, invent a witness, reverse polarity, or add
boundary over the wrong vocabulary is still wrong, and a good         an unapproved obligation.
vocabulary can still support a boundary that is too broad, too           This typing is what keeps the current implementation from
narrow, or missing a required workflow.                               becoming a flat list of checks. Signals fall into four classes:
   This is why target construction can backtrack. A property          target admission, semantic direction, local diagnostics, and
atom may require schema hooks that do not exist yet, such             history. Each has distinct obligations for what may and may
as a relationship field, status flag, or context attribute. AU -      not reach the model. Table I states these four obligations;
TO C EDAR does not show that unsatisfiable property to the            Algorithm 2 gives the full translation. These are different uses
reviewer as if it were ready. It records the missing support,         of verifier evidence, not different excuses to change the oracle.
repairs the schema candidate, and reruns the mechanical and              O1 keeps malformed targets out of the search loop. An atom
intent checks before the property can enter the plan. The             that never matches any request, a disjointness constraint whose
target becomes fixed only after this repair loop and coverage         compiled form is not actually disjoint, a floor that is outside a
accounting finish.                                                    same-action ceiling, or an identity check that compares a staff
                             TABLE I                                                 disagree, the record is malformed feedback and should not
S IGNAL - LAYER OBLIGATIONS AND REPAIR INFORMATION PRESERVATION                      become a model instruction.
                                                                                        O3 keeps local diagnostics local. A candidate that does not
 Obligation           Preserved signal and invariant
                                                                                     parse, does not validate, or can raise runtime Cedar errors
 O1: target well      Target-admission records preserve schema validity,
 formed               satisfiable atoms, never-errors, match                         has no meaningful permit-set denotation to compare against
                      vacuity/broadness, identity consistency,                       the synthesis sandwich. AUTO C EDAR may ask the model
                      derived-constraint compilation, duplicate/equivalent           to fix the offending expression, declaration, optional-attribute
                      atoms, and floor-ceiling consistency before search
                      starts.                                                        guard, or clause under the same schema. It may also point
                                                                                     to the candidate block that failed, show the reference block
 O2: semantic         Boundary kind, checked relation, witness, and
 direction            action-local evidence preserve whether the candidate           it was checked against, or explain a session-binding or set-
                      should TIGHTEN, LOOSEN, EXPAND, or repair a                    membership encoding mismatch. None of those local repairs
                      disjointness collapse.                                         becomes a new floor, ceiling, or liveness requirement.
 O3: local            Parse, validation, setup, runtime-safety, excerpt/diff,           O4 makes search history part of the repair state. A sin-
 diagnostic repair    session-binding, membership-drift, union-ceiling,
                      role-intersection, and global-constraint diagnostics           gle verifier call cannot say whether search is improving,
                      keep local repairs local.                                      repeating, or oscillating. AUTO C EDAR records recurring failed
 O4: history and      Candidate hashes, recurring failure sets, oscillation          boundaries, repeated candidates, and failures that trade off
 non-progress         windows, and repeated action-local diffs surface               against each other across iterations. It can tell the model that
                      non-progress without changing the oracle.
                                                                                     it is cycling between a floor and a ceiling, or that a role-
                                                                                     scoped forbid rule keeps removing access required by a floor.
Algorithm 2 Signal-layer translation Φ
                                                                                     History changes the repair packet, not the oracle. This is
Require: Check records Qt ; candidate Pt ; approved plan Π; history Ht
Ensure: Repair packet mt+1                                                           how AUTO C EDAR remembers non-progress without letting the
 1: Select failed records and attach their layer ℓ, oracle o, kind τ , relation κ,   model rewrite the target.
    witness w, and localization evidence e
 2: if any target-admission record fails then                                                IV. C EDAR B ENCH : A C EDAR B ENCHMARK
 3:     return target-construction diagnostic; do not ask model to repair Pt
 4: end if                                                                              If the claim were only that an LLM can produce Cedar syn-
 5: for all candidate-side semantic records q do                                     tax, an ordinary natural-language-to-policy benchmark would
 6:     if q is a ceiling or disjointness over-permission failure then
 7:         mark direction TIGHTEN                                                   be enough. AUTO C EDAR is making a different claim. It
 8:     else if q is a floor failure then                                            says that the hard part is holding a global semantic target
 9:         mark direction LOOSEN                                                    fixed while verifier evidence guides a stochastic proposer.
10:     else if q is a liveness failure then
11:         mark direction EXPAND                                                    CedarBench exists to measure that interface.
12:     end if                                                                          The current CedarBench repository contains 221 tasks.
13:     attach only approved boundary text, witness w, and localization              Seventy-nine are mutation tasks rooted in official Cedar exam-
        evidence e
14: end for                                                                          ple domains for GitHub-style repositories, document clouds,
15: Convert parse, validation, setup, runtime-safety, and structural diagnostics     hotel chains, sales organizations, streaming services, tag-and-
    into local repair hints                                                          role systems, tax-preparation workflows, and clinical data
16: Compare Pt and failed records with Ht to detect repetition, oscillation
17: return repair packet with selected boundaries, directions, witnesses, local      access. The other 142 are hand-authored real-world tasks
    hints, and history summary                                                       covering scoped tokens, delegation, revocation, time windows,
                                                                                     break-glass access, role intersections, and large policy stores.
user to a patient entity is not a hard synthesis problem. It is                      Every task is executable: it has a prose specification, a Cedar
an invalid target. The right response is to send the reviewer                        schema, a Python verification plan, and Cedar reference poli-
or target construction step a precise diagnostic, not to ask the                     cies. The reference policies are not deployment answers. They
LLM to synthesize around an invalid target.                                          are formal witnesses for the reviewed floors, ceilings, liveness
   O2 preserves direction. The same witness can require op-                          probes, and related checks that define the target for that task.
posite repairs depending on which boundary produced it. A                               Each CedarBench task pairs a requirement with the objects
request outside an approved ceiling is excess permission; a                          AUTO C EDAR needs to make the requirement checkable: a
request inside an approved floor may be missing permission.                          vocabulary, reviewed semantic boundaries, and executable
Direction is therefore a function of the typed check record:                         verifier checks. The unit of measurement is not whether a
                                                                                    generated snippet looks plausible in isolation. It is whether
               
                TIGHTEN, q.τ ∈ {ceiling, disjoint},                                 a candidate policy store satisfies the whole reviewed target:
               
               LOOSEN, q.τ = floor,
                                                                                     floors are included, ceilings are not exceeded, liveness slices
      Dt (q) =
               
                EXPAND,      q.τ = liveness,                                        remain reachable, and the final artifact validates under the
                                                                                     shared schema.
               
                 LOCAL,       q.τ ∈ {parse, type, safety}.
               
                                                                                        This matters because independent translation hides failure
The relation field q.κ still has to agree with the kind: an upper-                   mode we care about. A system can translate fifty fragments
bound failure tightens, a lower-bound failure loosens, and a                         into fifty locally reasonable rules and still produce global
nonempty failure expands. If the boundary and relation kind                          trouble: one rule grants outside the intended scope, another
relies on implicit exception, and a later rule makes an approved                                  TABLE II
workflow unreachable. CedarBench therefore makes cross-             C EDAR B ENCH SYNTHESIS EFFECTIVENESS FOR AUTO C EDAR ON ALL 221
                                                                             SCENARIOS . A LL REPORTED NUMBERS ARE AVERAGES .
policy interference visible: whether the policy store, taken as
a whole, lands inside the approved authorization boundary.                 Model           Convergence    Iters     Time    Tokens      Cost
   CedarBench should not be read as a production-policy                    GPT-5.5 low   221/221, 100%    1.67     24.59s    9,084   $0.0405
distribution or as proof that every organizational intent has              Haiku 4.5     221/221, 100%    2.51      8.93s   12,397   $0.0185
been captured perfectly. Its target is narrower and more useful
for this paper: it gives AUTO C EDAR a replayable substrate for                                 TABLE III
                                                                     S IGNAL - LAYER ABLATION ON A 100- SCENARIO C EDAR B ENCH SLICE .
asking whether reviewed intent constraints, symbolic checks,          L OSS IS THE MEAN FINAL VERIFIER - VIOLATION COUNT. M EAN ITER .
and model-facing repair signals actually work together.             AVERAGES SYNTHESIS ITERATIONS OVER COMPLETED SCENARIOS , SO IT
                                                                                CAN BE FRACTIONAL . C OST IS TOTAL RUN COST.
                      V. E XPERIMENTS
                                                                       Mode                          Scen. Conv. Mean loss Mean iter.          Cost
   We consider the following research questions:
                                                                       Schema only                       100       85       15.58      1.00    $1.42
RQ1 Synthesis effectiveness: To what extent can AUTO -                 Schema + atoms, one-shot          100       84        0.27      1.00    $1.62
C EDAR synthesize Cedar policies that satisfy formal verifi-           Native verifier loop              100       94        0.10      2.37    $5.73
                                                                       Full signal stack                 100      100        0.00      2.20    $5.83
cation targets, and at what computational cost?
RQ2 Signal-layer contribution: How does verifier-to-model
                                                                    for both model configurations we tested. Table II reports per-
feedback contribute to AUTO C EDAR synthesis performance?
                                                                    scenario averages over all 221 CedarBench scenarios. Both
RQ3 Verification validity: Does satisfying the verification
                                                                    models converge on every scenario. GPT-5.5 low takes fewer
plan produced by AUTO C EDAR reliably predict policy cor-
                                                                    repair iterations and fewer tokens per scenario. Haiku 4.5 takes
rectness with respect to NL intent?
                                                                    more iterations, but is faster and cheaper in this run. Thus we
RQ4 Baseline comparison: How does AUTO C EDAR policy
                                                                    find that AUTO C EDAR can successfully synthesize Cedar
quality compare to direct LLM-based policy generation?
                                                                    policies that satisfy formal verification targets.
A. Experimental Setup                                               C. RQ2: Signal-Layer Contribution
   Datasets. Our evaluation considers two datasets: the Cedar-         The ablation asks how useful the Signal Layer contribution
Bench benchmark discussed in Section IV, and three natural-         is inside of AUTO C EDAR. We use a fixed 100-scenario Cedar-
language access-control requirements corpora drawn from             Bench slice and hold fixed the model (GPT-5.5 low), selected
iTrust, CyberChair, and the IBM course registration system,         scenarios, Cedar validator, schemas, verification plans, and
following the ACRE/REDE access-control extraction line of           reference policies. The schema-only condition is also not a raw
work [9], [10]. The reported external-corpus scenarios use          natural-language-to-Cedar baseline: it receives the approved
401 IBM Course Management sentences, 303 CyberChair sen-            schema produced by AUTO C EDAR’s schema-generation stage
tences, and 471 iTrust-for-Text2Policy sentences, from which        and must synthesize only the policy. We then compare four
access control sentences were extracted from. We use these          full-slice conditions: the model sees only that approved schema
access control sentences in our experiments, rather than the full   and prose, sees the schema plus property atoms in a one-shot
natural language description of each system. Those corpora          setting, sees native verifier feedback in an iterative loop, or
provide realistic natural-language and NLACP-style access-          sees the full AUTO C EDAR repair-oriented signal stack.
control material, but they do not provide Cedar schemas or             Table III shows why pass rate alone is misleading. Residual
policies.                                                           loss counts how many verifier violations remain at the end
   Metrics. We record the model configuration, iteration bud-       of a run, so it separates a near miss from a policy that is
get, number of checks, convergence status, final loss, wall-        still far from the reviewed target. Schema-only and one-shot
clock time, token usage, and estimated API cost. The current        schema-plus-atoms converge on 85/100 and 84/100, but their
CedarBench driver runs the checked-in targets with a 20-            residual losses differ sharply: 15.58 versus 0.27. The formal
iteration budget and checkpoints each scenario so long runs         target pulls the model close even when the first candidate is not
can be resumed. We report both GPT-5.5 low, a strong pro-           accepted. Native verifier feedback is also strong, converging
poser, and Haiku 4.5, a cheaper and faster proposer, because        on 94/100 with mean loss 0.10. The full signal stack closes the
the question is not only whether the loop works with the            last six failures, reaching 100/100 with zero loss and similar
strongest model but whether verifier-guided repair still carries    cost. RQ2 therefore has a split answer: reviewed targets
a smaller model. We use the Cedar CLI and cedar symcc               reduce the size of mistakes, and shaped repair signals close
with the cvc5 SMT solver [11]. Model cost is reported               the stubborn remainder.
separately from local solver time and human review time.
                                                                    D. RQ3 & RQ4: Policy Correctness and Baseline Comparison
B. RQ1: Synthesis Effectiveness                                        We note that to the best of our knowledge, AUTO C EDAR is
  RQ1 asks the most direct question: once the target has            the only tool that can synthesize Cedar policies and schemas
been made executable, can AUTO C EDAR actually synthesize           from natural-language requirements against a formal verifica-
policies that satisfy it? On CedarBench, the answer is yes          tion target. A direct LLM baseline can generate policy text,
                             TABLE IV                                                                         TABLE V
 VALIDATION PASS RATES . C ATEGORY 1: NL ONLY; MODEL GENERATES                       C EDAR B ENCH PROPERTY- CHECKING RESULTS FOR C ATEGORY 2.
   SCHEMA AND POLICY. C ATEGORY 2: NL + AUTO C EDAR SCHEMA ;
                 MODEL GENERATES POLICY ONLY.                                           Generator or method   Full property pass   Property-check pass rate

                               CedarBench (221)            Real-world (3)               GPT-5.5               79.6% (176/221)        88.1% (4397/4991)
Setting      Model
                             Pass@1       Pass@3        Pass@1       Pass@3             Haiku 4.5               1.4% (3/221)         72.6% (2758/3798)
Category 1   Haiku 4.5        0/221         0/221           0/3             0/3         AUTO C EDAR           100.0% (221/221)       100.0% (all checks)
Category 1   GPT-5.5        155/221       199/221           0/3             0/3
Category 2   Haiku 4.5      146/221       148/221           0/3             0/3
Category 2   GPT-5.5        196/221       204/221           0/3             0/3
             AUTO C EDAR: 221/221 CedarBench; 3/3 real-world.


but without a reviewed boundary plan there is no formal
notion of correctness to check against. To answer RQ3 and
RQ4, we conduct three experiments which all study policy
correctness and baseline comparison from different angles.
We therefore organize around three evidence types: formal
correctness, semantic correctness, and human alignment. We
use two baseline categories throughout. In Category 1, the
model receives only the natural-language (NL) intent and must
generate both the Cedar schema and policy. In Category 2,
the model receives the same NL intent together with the
schema produced by AUTO C EDAR and must generate only
the Cedar policy. Category 2 puts all candidate policies under
the same AUTO C EDAR schema and approved property atoms,
so the policies can be checked against the same formal targets.
Category 1 lets each model invent its own schema, so there is
no common property target for comparing those outputs; we
therefore report only validation for that category.
   1) Formal Correctness: We probe formal correctness at two
levels. First, Validation uses cedar validate to check                                Fig. 3. Error profile of validation-passing policies on CedarBench
whether the generated Cedar artifacts are well-formed: the
policy must parse, type-check, and conform to its schema. Sec-                          b) Property checking: We run property checking only
ond, Property checking uses cedar symcc to ask whether                            after the validation gate. On CedarBench, this means the
a validation-passing Category 2 policy satisfies the approved                     validation-passing Category 2 policies: 148 Haiku-4.5 policies
floor, ceiling, and liveness atoms for the same NL intent. We                     and 204 GPT-5.5 policies at Pass@3. On the real-world
can run property checks in Category 2 only because the policy                     scenarios, this means the two GPT-5.5 Category 2 policies for
is written against the AUTO C EDAR schema, so the approved                        IBM and CyberChair that could be made validation-passing
atoms and the candidate policy share the same vocabulary. For                     with only trivial syntax or casing repairs.
the real-world scenarios, when a generated Category 2 policy                         Table V reports CedarBench results. AUTO C EDAR satis-
failed validation only because of trivial syntax or casing errors,                fies all approved properties for all 221 scenarios; GPT-5.5
we repaired those errors without changing the policy logic and                    fully passes 176/221 and Haiku 4.5 only 3/221. Individual
then included it in property checking; policies requiring non-                    property-check pass rates expose near misses: GPT-5.5 sat-
trivial modeling changes were left unevaluated.                                   isfies 4397/4991 checks and Haiku 4.5 satisfies 2758/3798.
      a) Validation: Table IV reports validation results for both                 Table VI shows the same pattern on the real-world scenarios:
input settings on CedarBench and the three real-world scenar-                     AUTO C EDAR passes every property, while repaired GPT-5.5
ios, with Pass@1 denoting the initial generation and Pass@3                       policies pass 20/21 for IBM and 8/20 for CyberChair.
denoting validation in at least one of three independent gener-                      Figure 3 plots ceiling violations against floor and live-
ations. On CedarBench, Haiku 4.5 fails all Category 1 cases,                      ness violations for validation-passing Category 2 policies.
while GPT-5.5 improves from 155/221 at Pass@1 to 199/221                          AUTO C EDAR sits at the origin; GPT-5.5 has small scattered
at Pass@3. Supplying the AUTO C EDAR schema in Category 2                         misses; Haiku 4.5 collapses toward over-permissive or over-
improves validation for both models, with GPT-5.5 reaching                        restrictive/dead policies. Figure 4 shows the gap by domain:
204/221 at Pass@3. On the real-world scenarios, neither direct                    GPT-5.5 collapses on tags, streaming, and doccloud,
baseline validates in Category 1 or Category 2 across three                       while Haiku 4.5 is near-zero throughout.
attempts; the common failures are invalid Cedar syntax and                           2) Semantic Correctness: We evaluate semantic correctness
schema-policy mismatches. AUTO C EDAR validates on all 221                        using authorization requests. This experiment addresses RQ3
CedarBench scenarios and all three real-world scenarios.                          by checking whether policies make the expected authorization
                                                                               better handled the request, or chose tie/neither, and could
                                                                               explain their judgment.
                                                                                  The study produced 98 probe-level answers across two
                                                                               scenarios: iTrust credentials, sessions, and patient scope; and
                                                                               gradebook external-grade conflicts. Participants selected the
                                                                               AUTO C EDAR artifact in 82/98 answers (83.7%), the direct
                                                                               LLM baseline in 8/98 answers (8.2%), and tie/neither in 8/98
Fig. 4. Fully-correct rate (%) across CedarBench’s domains. Each cell is the   answers (8.2%). The preference was strongest on iTrust, where
percentage of that domain’s scenarios in which every property atom passes.     AUTO C EDAR was selected in 52/56 answers (92.9%). Grade-
                                                                               book was more ambiguous but still favored AUTO C EDAR:
                               TABLE VI                                        30/42 answers (71.4%) selected the AUTO C EDAR artifact.
 R EAL - WORLD PROPERTY AND SEMANTIC REQUEST RESULTS . BASELINE
  ROWS ARE C ATEGORY 2; “ REPAIR ” MEANS ONLY TRIVIAL SYNTAX OR
                                                                                  The qualitative explanations match the technical failure
         CASING FIXES . N/A INDICATES INVALID SCHEMA / POLICY.                 modes above. Participants preferred artifacts that made the
                                                                               relevant boundary explicit: sensitive credential fields, session
Scenario             Policy
                                               Properties           Requests   state, represented-patient scope, grade kind, and role-conflict
                                                passed              matched
                                                                               forbids. They criticized baseline artifacts when they used
IBM                  GPT-5.5 (repair)            20/21               72/76     broad permits or lacked the schema fields needed to enforce
IBM                  Haiku 4.5                    N/A                 N/A
IBM                  AUTO C EDAR                 21/21               76/76     the intended boundary. This study is not a proof of policy
CyberChair           GPT-5.5 (repair)             8/20               58/68
                                                                               correctness, and it does not yet evaluate the live HITL work-
CyberChair           Haiku 4.5                    N/A                 N/A      flow; optional HITL feedback was sparse. It does show that,
CyberChair           AUTO C EDAR                 20/20               68/68     under concrete review questions, readers more often judged the
iTrust               GPT-5.5                      N/A                 N/A      AUTO C EDAR-derived artifact as the one that better matched
iTrust               Haiku 4.5                    N/A                 N/A      access-control intent.
iTrust               AUTO C EDAR                 35/35               38/38
                                                                                  4) Answering RQ3+RQ4: Taken together, the formal prop-
                                                                               erty checks, semantic request tests, and blinded artifact-
decisions on concrete scenarios derived from the NL intent.
                                                                               judgment study provide complementary evidence for RQ3
For each real-world scenario, we constructed a semantic test
                                                                               and RQ4. For RQ3, the results show that AUTO C EDAR’s
set from the NL intent. First, each request was justified by
                                                                               verification plan is a useful predictor of NL-level correct-
one or more explicit access-control statements in the NL.
                                                                               ness: policies satisfying the approved atoms also match all
Second, we instantiated a scenario-specific entity database
                                                                               semantic requests in the real-world scenarios, while failed
containing the principals, resources, relationships, and state
                                                                               atoms correspond to concrete request-level errors. For RQ4,
needed to make those requests executable. Third, we included
                                                                               direct LLM generation improves when given the AUTO C EDAR
only requests whose expected decision was determined by the
                                                                               schema, but schema guidance alone is insufficient: validation-
NL intent itself. Each semantic request was translated into a
                                                                               passing GPT-5.5 and Haiku 4.5 policies still violate floor or
Cedar request under the AUTO C EDAR schema.
                                                                               ceiling properties and fail request tests. AUTO C EDAR performs
   Table VI shows that AUTO C EDAR matches all semantic                        better because it does not stop at producing syntactically valid
requests across the three real-world scenarios: 76/76 for IBM,                 Cedar; it synthesizes against explicit, reviewed correctness
68/68 for CyberChair, and 38/38 for iTrust. The repaired                       targets and uses verifier feedback to close the gap between NL
GPT-5.5 baselines match 72/76 requests for IBM and 58/68                       intent and executable policy. Thus, the combined evidence
requests for CyberChair. Haiku 4.5 and the iTrust baselines                    supports both the validity of the verification targets and
are N/A because they did not pass Cedar validation. The                        the advantage of verifier-guided synthesis over direct LLM
request failures align with the property failures. In IBM, the                 policy generation.
failed requests exercise the same valid registration behavior
captured by the failed floor property. In CyberChair, the failed                                VI. T HREATS TO VALIDITY
requests exercise the same role-boundary mistakes exposed by                      Target validity. AUTO C EDAR certifies a policy against the
the failed ceiling properties. Thus, the request-level failures                reviewed Cedar schema and verification target, not against
provide concrete examples of the same policy weaknesses                        organizational truth in the abstract. If a requirement is missing
detected by property checking.                                                 from the source material, or if a reviewer approves the wrong
   3) Human Alignment: This experiment asks whether human                      atom, the verifier will faithfully check the wrong boundary.
readers prefer the policy artifacts produced by AUTO C EDAR                    In our experiments, the CedarBench plans are benchmark
or by direct LLM generation when they must answer con-                         artifacts and the external-corpus plans were constructed for
crete access-control questions. We ran a blinded artifact-                     this study; they should be read as reviewed semantic targets for
judgment study with 14 participants. Participants saw require-                 evaluation, not as independently audited production policies.
ment context, an access request, and Cedar excerpts from two                      Request coverage. Symbolic checks are the primary ac-
anonymized systems. The A/B labels were randomized per                         ceptance criterion, but request-level evaluation is still only
probe. For each probe, participants selected which artifact                    a sample of concrete behavior. Generated requests can miss
corner cases, especially in domains with large entity graphs,           Symbolic analysis as oracle, not repair. Policy analyzers
temporal conditions, or context-dependent workflow state. We         such as Zelkova use SMT solving to reason about cloud poli-
therefore use request tests as a sanity check on policy behavior,    cies [8], and related systems quantify or repair permissiveness
not as a replacement for the floor, ceiling, liveness, and           in access-control policies [23], [24]. These tools can produce
disjointness obligations.                                            the semantic facts we need: inclusion results, equivalence
   Model and reviewer effects. LLM outputs are nondeter-             results, and witnesses. A stochastic proposer needs something
ministic, and direct-generation baselines are especially sensi-      different from the raw oracle output. It needs to know whether
tive to retries; this is why we report retry-based validation        a witness means excess permission, missing permission, or
results rather than a single sample. The HITL parts of the           a vanished workflow. AUTO C EDAR focuses on that missing
evaluation also depend on the reviewer population and review         interface between symbolic policy evidence and model-facing
procedure. A small or author-driven review study can show            repair.
whether the artifacts are inspectable, but it cannot by itself
                                                                                              VIII. C ONCLUSION
prove how production engineers would review the same targets
under deployment pressure.                                              An LLM that writes a plausible policy has not earned au-
                                                                     thority over access control. AUTO C EDAR assigns it a narrower
                    VII. R ELATED W ORK                              role: propose candidates after a reviewed target has been fixed,
                                                                     and let a verifier judge every proposal against that target.
   CEGIS when the proposer is stochastic. Counterexample-            Floor policies state what access must remain possible, ceiling
guided inductive synthesis pairs generation with a verifier          policies state what access must not leak, and liveness slices
that rejects bad candidates [12], [13]. In classical settings,       keep approved workflows from disappearing.
the generator is often symbolic or enumerative, so earlier              The paper’s main claim is that the hard interface is not
counterexamples can be removed from the search space by              only between natural-language and Cedar. It is also between
construction. An LLM breaks that assumption. It can read             a symbolic checker and a stochastic proposer. A verifier can
counterexamples and try again, but it does not maintain a            return an exact failure, but a model needs a repair instruction
symbolic version space and can reintroduce an old failure in         that preserves boundary identity, witness request, repair direc-
the next sample. Recent LLM systems still use this verifier-         tion, provenance, and search history. The signal layer is that
in-the-loop pattern for repair, execution-guided debugging,          contract. It lets the model use verifier evidence without letting
formal proofs, and planning [14]–[18]. AUTO C EDAR keeps             the model change the oracle.
the useful discipline of CEGIS–every accepted candidate is              The resulting guarantee is intentionally narrow. A returned
checked against the full target–while making explicit what the       policy is certified by cedar symcc against the approved
LLM does not provide: monotone elimination of prior failures.        boundary plan; the plan’s correspondence to organizational
   Verifier-guided formalization. Formal mathematics sys-            intent remains a human-review judgment. That separation is
tems show how much an LLM can gain from a mechan-                    the point. Verifier-guided LLM systems for security-sensitive
ically checked environment: language-model provers have              synthesis should expose the target, the intent boundary, and the
been paired with automated theorem provers, interactive proof        verifier-to-model signal as auditable state rather than hiding
environments, retrieval over verified libraries, proof repair, and   them inside prompts.
proof-assistant feedback during search or training [15], [16],
                                                                                                  R EFERENCES
[19]–[21]. LEAP [18] combines informal proof sketches, Lean
compiler feedback, and a graph that records proof decompo-            [1] OWASP Foundation, “A01 Broken Access Control – OWASP Top
                                                                          10:2025,” OWASP Top 10:2025, 2025, accessed: 2026-06-28.
sition and memoizes verified subgoals. Roundtrip verification         [2] SonarSource, “Sonar Data Reveals Critical “Verification Gap” in AI
work makes the neighboring point for autoformalization: the               Coding,” SonarSource press release, 2026, accessed: 2026-06-28.
formal tool can expose semantic drift and support scoped              [3] Anthropic, “Project Glasswing: An Initial Update,” Anthropic research
                                                                          update, 2026, accessed: 2026-06-28.
repair [22]. AUTO C EDAR starts from organizational intent            [4] A. Vatsa, P. Patel, and W. Eiers, “Synthesizing access control policies
and must first construct the object to be checked: a reviewed             using large language models,” in Proceedings of the 4th International
schema, boundary plan, and audit trace that records how                   Workshop on Natural Language-Based Software Engineering, 2025,
                                                                          arXiv:2503.11573.
source spans, approved atoms, verifier records, and candidate         [5] A. Vatsa, B. Hall, and W. Eiers, “Exploring large language models
clauses were associated.                                                  for access control policy synthesis and summarization,” arXiv preprint
   LLM policy authoring. Prior work asks whether LLMs                     arXiv:2510.20692, 2025.
                                                                      [6] J. W. Cutler, C. Disselkoen, A. Eline, S. He, K. Headley, M. Hicks,
can synthesize access-control policies from examples, request             K. Hietala, E. Ioannidis, J. Kastner, A. Mamat, D. McAdams, M. Mc-
specifications, or natural language [4], and whether they can             Cutchen, N. Rungta, E. Torlak, and A. M. Wells, “Cedar: A new lan-
summarize or reconstruct existing policies at scale [5]. Those            guage for expressive, fast, safe, and analyzable authorization (extended
                                                                          version),” arXiv preprint arXiv:2403.04651, 2024.
studies expose the failure mode that motivates this paper:            [7] “Cedar policy language,” cedarpolicy.com, accessed: 2026-06-24.
syntax and plausibility are easier than semantic equivalence          [8] J. Backes, P. Bolignano, B. Cook, C. Dodge, A. Gacek, K. Luckow,
to the intended request set. AUTO C EDAR therefore moves the              N. Rungta, O. Tkachu, and C. Varming, “Semantic-based automated
                                                                          reasoning for AWS access policies using SMT,” in Proceedings of the
question from “can the model write a policy?” to “can it search           18th Conference on Formal Methods in Computer-Aided Design, 2018,
under a reviewed target checked by a verifier?”                           pp. 1–9.
 [9] J. Slankas and L. Williams, “Access control policy extraction from
     unconstrained natural language text,” in Proceedings of the 2013 Inter-
     national Conference on Social Computing. IEEE, 2013, pp. 435–440.
[10] J. Slankas, X. Xiao, L. Williams, and T. Xie, “Relation extraction for
     inferring access control rules from natural language artifacts,” in Pro-
     ceedings of the 30th Annual Computer Security Applications Conference.
     ACM, 2014, pp. 366–375.
[11] H. Barbosa, C. W. Barrett, M. Brain, G. Kremer, H. Lachnitt, M. Mann,
     A. Mohamed, M. Mohamed, A. Niemetz, A. Nötzli, A. Ozdemir,
     M. Preiner, A. Reynolds, Y. Sheng, C. Tinelli, and Y. Zohar, “cvc5: A
     versatile and industrial-strength SMT solver,” in Tools and Algorithms
     for the Construction and Analysis of Systems, ser. Lecture Notes in
     Computer Science, vol. 13243. Springer, 2022, pp. 415–442.
[12] A. Solar-Lezama, “Program synthesis by sketching,” Ph.D.
     dissertation, University of California, Berkeley, December 2008.
     [Online]. Available: https://www2.eecs.berkeley.edu/Pubs/TechRpts/
     2008/EECS-2008-177.html
[13] A. Abate, C. David, P. Kesseli, D. Kroening, and E. Polgreen, “Coun-
     terexample guided inductive synthesis modulo theories,” in Computer
     Aided Verification. Springer, 2018, pp. 270–288.
[14] S. Polu and I. Sutskever, “Generative language modeling for automated
     theorem proving,” arXiv preprint arXiv:2009.03393, 2020.
[15] A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li, M. Jamnik,
     G. Lample, and Y. Wu, “Draft, sketch, and prove: Guiding formal
     theorem provers with informal proofs,” in International Conference on
     Learning Representations, 2023.
[16] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
     generation and repair with large language models,” in Proceedings of
     the 31st ACM Joint European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering, 2023, pp.
     1229–1241.
[17] S. Varambally, T. Voice, Y. Sun, Z. Chen, R. Yu, and K. Ye, “Hilbert:
     Recursively building formal proofs with informal reasoning,” arXiv
     preprint arXiv:2509.22819, 2025.
[18] P.-N. Kung, L. Song, D. Hwang, J. Yoon, C.-L. Li, S. Severini, M. Olsak,
     E. Lockhart, Q. V. Le, B. Gokturk, T. Luong, T. Pfister, and N. Peng,
     “LEAP: Supercharging LLMs for formal mathematics with agentic
     frameworks,” arXiv preprint arXiv:2606.03303, 2026.
[19] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski, T. Odrzygóźdź,
     P. Miłoś, Y. Wu, and M. Jamnik, “Thor: Wielding hammers to integrate
     language models and automated theorem provers,” in Advances in
     Neural Information Processing Systems, 2022. [Online]. Available:
     https://arxiv.org/abs/2205.10893
[20] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
     S. Godil, R. Prenger, and A. Anandkumar, “LeanDojo: Theorem
     proving with retrieval-augmented language models,” in Advances in
     Neural Information Processing Systems, 2023. [Online]. Available:
     https://arxiv.org/abs/2306.15626
[21] H. Xin, Z. Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu,
     L. Zhang, X. Lu, Q. Du, W. Gao, Q. Zhu, D. Yang, Z. Gou, Z. F.
     Wu, F. Luo, and C. Ruan, “DeepSeek-Prover-V1.5: Harnessing proof
     assistant feedback for reinforcement learning and monte-carlo tree
     search,” arXiv preprint arXiv:2408.08152, 2024. [Online]. Available:
     https://arxiv.org/abs/2408.08152
[22] D. Amrollahi, J. Lopez, and C. Barrett, “Faithful autoformalization
     via roundtrip verification and repair,” arXiv preprint arXiv:2604.25031,
     2026.
[23] W. Eiers, G. Sankaran, A. Li, E. O’Mahony, B. Prince, and T. Bultan,
     “Quantifying permissiveness of access control policies,” in Proceedings
     of the 44th International Conference on Software Engineering, 2022,
     pp. 1805–1817.
[24] W. Eiers, G. Sankaran, and T. Bultan, “Quantitative policy repair for
     access control on the cloud,” in Proceedings of the 32nd ACM SIGSOFT
     International Symposium on Software Testing and Analysis, 2023, pp.
     564–575.
