                                                From Capability to Assurance in Autonomous
                                                      Penetration-Testing Harnesses:
                                                A Framework and Reference Implementation
                                                                                              Joas Antonio dos Santos
                                                                               Independent Researcher — AI and Offensive Security
                                                                                               São Paulo, SP, Brazil
                                                                                         joas.santos@redteamleaders.com


                                            Abstract—Research on large-language-model (LLM) agents for        [12] now measure offensive capability across hundreds to
arXiv:2609.22664v1 [cs.CR] 19 Sep 2026




                                         penetration testing is evaluated almost entirely by capability:      thousands of real targets.
                                         whether the agent captures a flag or reproduces a proof-of-
                                                                                                                 Almost all of this progress is measured with one family of
                                         concept. This metric is appropriate for a benchmark but silent
                                         on the properties that decide whether an autonomous agent            metrics: task or subtask success, operationalized as capturing a
                                         can be used in an authorized engagement—whether a reported           flag or reproducing a proof-of-concept (PoC). That instrument
                                         finding is true, whether the agent remained inside its authorized    is right for a benchmark. It is silent, however, on three
                                         scope, and whether an operator can audit what it did. We             properties that determine whether an autonomous agent can
                                         call these assurance properties and argue that they belong to
                                                                                                              be used in a paid, authorized engagement:
                                         the harness—the runtime wrapping the model—and can be
                                         enforced in code. This paper makes three contributions. First,         • Truth. A flag capture is self-verifying; a client report is
                                         we define a framework of five assurance properties (evidence             not. An agent that emits a fluent but unproven vulnera-
                                         grounding, non-destructive claim reduction, computed severity,           bility narrative—the “hallucinated compliance” pattern of
                                         enforced authorization, and tamper-evident accountability), each
                                         with a formal model and an explicit acceptance test, and we              Nguyen and Husain [14]—imposes remediation cost and
                                         connect them to prior work in capability-based security, tamper-         destroys credibility.
                                         evident logging, and software provenance. Second, we position          • Authorization. The engagement boundary belongs to the
                                         representative systems (PentestGPT, the Cochise reference har-           client. If scope exists only as prompt text, an agent that
                                         ness, MAPTA, and the trajectory judge PentestJudge) within               follows an off-target redirect or acts on a discovered
                                         the framework using published, coded criteria, and identify a
                                         consistent assurance gap. Third, we study one open-source imple-         subdomain has crossed a legal line, discovered only by
                                         mentation, NeuroSploit (pinned to an exact commit), reporting            reading the report.
                                         its architecture, its complexity cost measured by documented           • Accountability. Afterwards the operator must state what
                                         commands, and a version-pinned, content-addressed artifact               was done, to what, under whose authority, and with what
                                         bundle from a run against a public deliberately-vulnerable target.       result. Prose logs are lossy and reorderable.
                                         We are precise about what is and is not evidenced: we execute
                                         the deterministic P4 and P5 acceptance tests directly and, in           These are assurance questions, and our central claim is that
                                         doing so, find and report a real enforcement gap, which we           they are properties of the harness—the runtime that surrounds
                                         reflect by scoring both P4 and P5 as partial. We therefore claim     the model with a shell, tool wrappers, a token budget, a
                                         an initial existence argument that the properties are realizable
                                         together—not a comparative-performance result—and we specify         memory policy, and an output parser—not of the model’s
                                         the multi-target, ablation, and adversarial evaluation protocol      weights. The harness is where an assurance obligation can
                                         required to turn the framework’s obligations into measurements.      be enforced in code rather than requested in a prompt, and
                                         The contribution is a vocabulary, a set of realizable design         the same base model in two harnesses can differ by tens
                                         obligations, and a measurable evaluation plan for autonomous         of percentage points on the same benchmark [5], [9], which
                                         offensive agents whose output can withstand scrutiny.
                                            Index Terms—autonomous penetration testing, large language        already establishes the harness as the decisive engineering
                                         models, assurance, evidence grounding, capability-based autho-       surface. The assurance properties themselves are not new
                                         rization, tamper-evident logging, CVSS, offensive security           inventions: they instantiate, for offensive agents, long-standing
                                                                                                              ideas from capability-based security [19]–[21], enforceable
                                                               I. I NTRODUCTION                               security policies [24], tamper-evident logging [25]–[27], and
                                            Autonomous penetration testing has become a measurable            provenance [29], [30]. Our framework’s role is to name which
                                         engineering discipline. Since Fang et al. showed that an LLM         of them a pentest harness owes, and to state each as a testable
                                         agent could exploit real one-day web vulnerabilities from a          obligation.
                                         CVE description [1], systems such as PentestGPT [2], HPTSA              Research questions.
                                         [3], MAPTA [4], CHECKMATE [5], Pentest-R1 [6], and the RQ1 What assurance properties should an autonomous
                                         Cochise reference harness [7] have advanced the state of the penetration-testing harness provide, and can each be
                                         art, and benchmarks such as CyberGym [11] and ExploitGym     stated as an implementation-independent obligation with
    an explicit acceptance test?                                                                       TABLE I
RQ2 Where do existing systems sit with respect to these                A SSURANCE PROPERTIES (P1–P5) ACROSS REPRESENTATIVE SYSTEMS ,
                                                                       CODED PER A PPENDIX I. ✓= ADDRESSED IN THE ANALYZED ARTIFACT;
    properties under objective, coded criteria?                         ∼= PARTIAL / PROCESS - LEVEL ; —= NOT ADDRESSED IN THE ANALYZED
RQ3 Are the properties realizable in a single system, at what           ARTIFACT ( ABSENCE OF A CLAIM , NOT PROOF OF ABSENCE IN CODE ).
    complexity cost, and what evaluation would measure how            N EURO S PLOIT P4/P5 ARE ∼ BECAUSE THE PRIMARY- TARGET CHECK (P4)
                                                                       AND EXTERNAL ANCHORING (P5) ARE NOT YET IN THE TESTED BUILD ;
    completely each is satisfied?                                                          SEE S ECTIONS V-D AND VIII.
   Contributions.
                                                                                                  PentestGPT   Cochise   MAPTA   PentestJudge   NeuroSploit
   1) A framework of five assurance properties (Section IV),                                          [2]        [7]      [4]        [13]          [34]
                                                                      P1 Evidence grounding           —          —        ✓          ∼              ✓
      each with a formal model and an acceptance test, related        P2 Non-destr. reduction         —          —        ∼          ∼              ✓
      to prior security literature; this answers RQ1.                 P3 Computed severity            —          —        —          —              ∼
                                                                      P4 Enforced authorization       —          —        —          —              ∼
   2) A positioning of representative systems using published         P5 Tamper-evident audit         —          —        —          —              ∼
      coding criteria (Section II and Appendix I), answering          Trajectory judging              —          ∼        —           ✓             ∼
                                                                      Released implementation         ✓          ✓        ✓           ✓             ✓
      RQ2.
   3) A reference implementation study of NeuroSploit [34],
      pinned to an exact commit, with complexity measured
                                                                      C. Security foundations
      by documented commands and a content-addressed ar-
      tifact bundle (Sections V–VII); and a measurable eval-             Each property below has a lineage. P4 is a capability [19],
      uation protocol—multi-target precision/recall, ablation,        [20]; the concrete token design follows Macaroons [21] and
      and adversarial P4/P5 batteries (Appendix H)—that               JWT [22] with HMAC [23]. P5 is tamper-evident logging [25],
      specifies what remains to be measured. Together these           [26] over a hash chain [27], whose full-rewrite weakness is
      answer RQ3.                                                     addressed by external anchoring as in Certificate Transparency
                                                                      [28] and supply-chain attestation [29]. P1 relates to grounding
    We state scope precisely. We make no comparative-
                                                                      and attribution for LLM output [17], [18] and to prompt-
 performance claim: no shared benchmark for assurance prop-
                                                                      injection defenses for tool-using agents [15], [16]. P3 builds on
 erties exists, and constructing one is the central open problem
                                                                      CVSS v3.1 [31], and the enforcement stance follows Schnei-
 (Section VIII). The reference study is an initial existence
                                                                      der’s enforceable security policies [24] and W3C provenance
 argument, not a proof that every property holds on every
                                                                      [30].
 action; Section VII is explicit about what the archived artifacts
 do and do not evidence.                                              D. The assurance gap
                                                                         Appendix I states objective coding criteria and applies them,
             II. BACKGROUND AND P OSITIONING                          per analyzed version, to representative systems; Table I sum-
 A. Autonomous offensive agents and their harnesses                   marizes. The pattern is consistent: capability is addressed and,
                                                                      at best, trajectory-level judging; finding-level truth, enforced
    Early autonomous LLM pentesters were single-agent ReAct
                                                                      scope, and per-action accountability are left to the surrounding
 loops [1], [8]. Multi-agent designs followed: HPTSA showed
                                                                      process. This gap—not any single missing feature—is what the
 a planner dispatching task-specific subagents outperforms a
                                                                      framework names.
 generalist on zero-day-class web targets [3], and the Planner–
 Executor–Perceptor pattern was formalized in CHECKMATE,                                            III. T HREAT M ODEL
 which, holding the base model fixed, obtains a > 20% success            Setting. An operator runs a harness against systems for
 improvement and > 50% cost reduction from the harness alone          which a client has granted written authorization. Operator and
 [5]. MAPTA added tool-grounded execution with end-to-end             authorizing party may differ. The target is partially observable
 exploit validation [4]. Cochise [7] is the closest work in intent:   and may be hostile to the agent.
 a deliberately small (630 LOC) Python reference harness                 Assets. (A1) client systems and data, including assets ad-
 for reproducible traces. The properties we study concern             jacent to but outside scope; (A2) report integrity—no false
 assurance of output.                                                 findings, no silently dropped real ones; (A3) the operator’s
                                                                      ability to prove, afterwards, that the engagement stayed within
 B. Evaluation and judging                                            authorization.
    Cybench evaluates agents on 40 professional CTF tasks and            Adversaries and failure modes. (T1) the model as a
 is reported in most frontier-model system cards [9]. PentestE-       source of confident hallucination; (T2) a hostile target per-
 val shows end-to-end pipeline success collapsing to ≤31%             forming prompt injection through tool output [15], [16]; (T3)
 even when per-stage scores are high [10]. CyberGym [11] and          scope drift onto discovered-but-unauthorized assets, including
 ExploitGym [12] scale evaluation to real code. PentestJudge          redirects, DNS rebinding, alternate IP encodings, and mid-
 [13] argues a flag-only reward is gameable and grades agent          run DNS changes; (T4) an after-the-fact dispute, including
 behavior; that is an assurance argument at the trajectory level,     an adversary who can edit, remove, reorder, or wholesale-
 which our framework complements at the level of findings,            rewrite the log. The framework addresses T1, T3, and T4
 authorization, and per-action accountability.                        structurally; T2 is reduced but not eliminated (Section VIII).
For T4 we distinguish a local adversary (can edit files but not      C. P3 — Computed, evidence-graded, impact-separated
forge external signatures) from a full-rewrite adversary (can        severity
recompute an unanchored chain); P5’s acceptance test targets            Severity is computed from evidence by a deterministic
both only when external anchoring is present (Appendix G).           function and capped by demonstrated impact; potential impact
                                                                     is recorded separately so that safely-unexploited worst cases
     IV. A F RAMEWORK OF A SSURANCE P ROPERTIES                      are not understated. Let g be the CVSS v3.1 base function
                                                                     [31] over a full metric vector whose values each cite a receipt;
   We state five properties as obligations on the harness, each      let ℓd (f ) be the demonstrated-impact rung and ℓp (f ) the
with a formal model and an acceptance test: a concrete check         potential-impact rung on
that decides whether an implementation satisfies the property.
                                                                              reached < read < wrote < RCE < crossed.             (3)
A finding f is a claim about a target; the evidence ledger
E = {e1 , . . . , em } is the set of receipts collected during an    P3 requires a demonstrated score and a separately-recorded
engagement (raw tool output: an HTTP response, an out-of-            potential score,
band callback, an error oracle, a shell transcript, or, white-box,                                        
a source citation). Each receipt e records a target, an action         sevd (f ) = min g(f ), cap(ℓd (f )) , sevp (f ) = g(f ), (4)
reference, a timestamp, and a content hash.                          each annotated with an evidence-confidence level. The sepa-
                                                                     ration prevents the failure the reviewer of an authorized test
A. P1 — Evidence grounding                                           rightly fears: correctly declining to demonstrate destructive
                                                                     impact must not silently lower the recorded risk. Appendix E
   No claim enters the reported world model with-                    gives the cap table and a worked example. Acceptance test
out a receipt that a decision procedure outside the                  (T-P3): two findings of the same CWE with different demon-
model accepts. Let cite(c) ⊆ E be the receipts a                     strated impact must receive different sevd ; class-only scoring
claim c names. Define the external decision procedure                fails.
supports (formalized in Appendix B) returning a verdict in
{Confirmed, Rejected, NeedsReview}. P1 requires                      D. P4 — Enforced, attributable authorization
                                                                       Scope is a signed grant, bound to a client, an operator, an
  ∀c ∈ f : cite(c) ̸= ∅ ∧ supports(c, cite(c)) ̸= Rejected,          engagement, and an asset set, that in-session behavior can
                                                              (1)    narrow but never widen, with replay and revocation controls.
with any NeedsReview claim labelled and withheld from                Let A be an authorization token carrying issuer (client key id),
asserted status. The obligation is that supports is not “an LLM      audience (harness instance), engagement id, operator id, scope
agrees”; model agreement is not evidence. Acceptance test (T-        (hosts, CIDRs, URL prefixes), action ceiling, environment,
P1): inject a syntactically plausible but fabricated receipt (a      validity window [nbf , exp], and nonce; let σ be its signature.
transcript with no matching action hash); the finding must not       P4 requires that an action a on target t be admitted only if
reach asserted status.
                                                                      verify(A, σ, Kiss ) ∧ nbf ≤ now ≤ exp ∧ fresh(nonce)
                                                                       ∧ aud(A) = self ∧ (t, a) ⊑ A ∧ (t, a) ⊑ cfg,
B. P2 — Non-destructive claim reduction                                                                                        (5)
                                                                     where cfg is local configuration and ⊑ is “within.” A is
   An overstated finding is reduced to what its evidence
                                                                     a ceiling: no in-session reasoning can yield (t, a) ̸⊑ A.
supports, never silently deleted or inflated, and a claim
                                                                     Appendix F specifies the token, key custody, revocation, and
with no security-relevant mechanic is not force-retained.
                                                                     rotation, and notes that HMAC [23] proves only holder-of-key,
Decompose f into separable claims and partition them
                                                                     so separating client from operator argues for an asymmetric
into supported mechanic M (f ) and unsupported impact
                                                                     signature (client-held private key, harness-held public key),
I(f ). The reduction returns one of four typed outcomes
                                                                     which we present as the recommended evolution of the current
(Appendix D): supported finding (M (f ) rewritten), in-
                                                                     HMAC form. Acceptance test (T-P4): the adversarial scope
formational observation (a benign but true fact), insuffi-
                                                                     battery of Appendix H (off-scope redirect, DNS rebinding,
cient evidence, or invalid claim. Formally,
                                                                     alternate IP encodings, userinfo URLs, over-broad wildcard,
                                                                    expired/tampered token, in-session widening) must each be
         rewrite(M (f )) M (f ) security-relevant,
         
                                                                     denied.
       ′
      f = demote(M (f )) M (f ) true but benign,              (2)
         
         
          ∅               otherwise.                                 E. P5 — Externally-anchored tamper-evident accountability
                                                                        Every action is recorded in an append-only log whose
Acceptance test (T-P2): a finding whose impact is unproven           integrity is verifiable, and whose root is anchored outside the
but whose mechanic is proven (e.g., a measured missing rate          writing process so that a full rewrite is detectable. Actions
limit) must be retained and downgraded, not rejected; a finding      produce records r1 , . . . , rn chained by hi = H(ri ∥ hi−1 ),
with neither must not be force-retained.                             h0 = H(genesis). A hash chain alone detects only local
             P4 authorization ceiling · P5 hash-chained audit (every action)
                                                                                          1. Grounding (P1). Receipt required; ungrounded ⇒ withheld.
                                      Agent selection               Parallel run over
   Recon & belief state              (surface-matched)                model pool
                                                                                          2. Deterministic validator (P1). Per-CWE, outside the model.

  Evidence-graded report          Chaining & attack graph         Verification (P1–P3)
                                                                                          3. Adversarial vote. N -model agreement + refute, over survivors.


Fig. 1. NeuroSploit pipeline. Recon/select/run/verify/chain/report are wrapped            4. Prosecutor (P2). Four typed outcomes; rewrites, no silent delete.
by the P4 ceiling and the P5 chain.



edits; a full-rewrite adversary can recompute it. P5 therefore                               Fig. 2. Verification pipeline realizing P1–P2; severity (P3) follows.
additionally requires periodic anchoring of hi —an external
signature, a trusted timestamp, a write-once store, or publi-
                                                                                         A. Planning as an anti-hallucination gate
cation to a transparency log [26], [28]—so that no post-hoc
chain can match the anchored roots. Acceptance test (T-P5):                                 The target is partially observable, so the harness tracks a
the tamper battery of Appendix H (record removed, altered,                               belief : a property graph whose nodes carry a probability and
reordered; evidence substituted; token swapped; log truncated;                           an evidence count, updated from observations by a Bayesian
whole-chain rebuilt) must each be detected; the last only when                           step; per-node Shannon entropy H(b) measures diffuseness.
anchoring is enabled.                                                                    The “recon vs. exploit” choice is a value-of-information de-
                                                                                         cision: with Vobs (b) and Vexploit (b) the expected payoffs, the
Relationships and completeness. P1 is prerequisite to P2 and                             planner observes while
P3. P4 and P5 are independent of P1–P3 and of the model.
The five are proposed as necessary for an engagement that                                                          Vobs (b) > Vexploit (b),                          (6)
must withstand scrutiny; they are not claimed exhaustive—                                which holds when the belief is diffuse; the same inequality
trajectory-level judging [13] is a candidate sixth, kept com-                            bars asserting exploitability while H(b) is high, reinforcing
plementary because it ranges over runs rather than findings or                           P1 at the planning layer.
actions.
                                                                                         B. Realizing P1–P3
                 V. R EFERENCE I MPLEMENTATION                                              Grounding (P1) enforces a receipt in the engagement-
                                                                                         appropriate mode (empirical / symbolic / either). Determin-
  To address RQ3 we study NeuroSploit [34], an open-
                                                                                         istic per-CWE validators (Appendix C) implement supports
source Rust harness developed by the author (disclosed as
                                                                                         outside the model: 27 validators, keyed to CWE classes
a competing interest, Section IX). It is used as an existence
                                                                                         and referencing 31 CWE identifiers, each returning Con-
argument and a source of complexity measurements, not a
                                                                                         firmed/Rejected/NeedsReview. Adversarial N -model vot-
product claim; any harness satisfying P1–P5 would serve.
                                                                                         ing runs only over survivors. The evidence prosecutor realizes
All measurements in this paper are pinned to one commit
                                                                                         P2 with the four typed outcomes above. Severity (P3) is then
(Table II) and produced by the commands in Appendix A.
                                                                                         computed and impact-separated (Appendix E). Figure 2 shows
                                                                                         the order; deterministic checks precede model-based ones.
                             TABLE II
 E VALUATED VERSION ( ALL S ECTION VI–VII NUMBERS REFER TO THIS                          C. Realizing P4–P5
                              STATE ).
                                                                                            Authorization is a signed capability token (Appendix F)
Item                      Value                                                          verified as the P4 ceiling, with a two-layer scope guard:
Commit SHA                8894649ccb42a04c4763085b3b663e49fd98ddf5                       hard scope (allowlist defaulting to the engagement target,
Describe/tag              v4.0.0-32-g8894649                                             so discovery cannot widen scope) and soft scope (read-only
Commit date               2026-09-18
Measurement date          2026-09-18                                                     zones, forbidden methods, rate ceilings). Every action emits a
OS                        macOS 15.1 (Darwin 24.1.0, arm64)                              hash-chained record (Appendix G) with a verify() routine;
Toolchain                 rustc/cargo 1.96.0                                             external anchoring is discussed there as the defense against full
                                                                                         rewrite. An additive OT risk model reff = raction + casset +
  Figure 1 shows the pipeline: recon builds a belief state;                              rproto + ppriv + bradius forbids disruptive industrial function
a selector chooses surface-matched agents from a markdown                                codes while permitting the reads OT findings come from.
knowledge base; agents run in parallel over a model pool;                                These mechanisms are exercised both by the unit-test suite
outputs pass the verification pipeline; survivors are chained                            (Section VI) and by a command-line acceptance battery we
and reported. The P4 authorization ceiling and the P5 audit                              ran directly (Section V-D); the latter also surfaced a real
chain wrap every action.                                                                 enforcement gap, reported below.
D. Executed acceptance tests for P4 and P5                                                      TABLE IV
                                                                      C OMPLEXITY OF THE PINNED INSTANCE ( COMMANDS IN A PPENDIX A).
   Because the P4 and P5 acceptance tests are deterministic
and need no model, we executed them on the pinned                       Component                                                         Metric
build (Table II). Table III reports the P4 capability-token
                                                                        Rust modules (harness crate)                                          40
battery. Token issuance, verification, tamper rejection,                Rust LOC (harness crate)                                          23,370
wrong-key rejection, and expiry detection all behave as                 Rust LOC (workspace, excl. target)                                28,802
specified, and constrain() correctly drops an out-of-grant              Automated tests (#[test]/#[tokio::test])                             312
host from local scope (the audit record for an off-grant                Deterministic validators (impl CweValidator)                          27
run shows the hard scope reduced to the granted host).                  CWE identifiers referenced by validators                              31
                                                                        Agent definitions (markdown)                                         446
However, when the run’s primary target lies outside the                 Supported model providers                                             18
grant, the offline engagement still reconned it and logged
engagement-start as allow: the token constrains
the agent scope but the tested build does not refuse
                                                                           VII. R EFERENCE RUN AND A RTIFACT B UNDLE
an out-of-grant primary target at engagement start. We
therefore score P4 as partial (Table I) and list this as a              To characterize behavior—not to claim a compar-
limitation (Section VIII). For P5, an offline run produced           ative result—we examine an archived black-box run
a hash-chained audit.jsonl (fields seq, prev_hash,                   against http://testaspnet.vulnweb.com/, a public
hash= sha256(digest)), and the audit module’s tests—                 deliberately-vulnerable application published by Acunetix for
the_chain_verifies_and_notices_tampering,                            testing (an ASP.NET/IIS 8.5 site; recon recorded zero security
removing_a_record_breaks_the_chain_too,                              headers and a non-Secure ASP.NET_SessionId cookie).
reopening_continues_the_same_chain,                                  The run scheduled 245 surface-matched agents and produced
refusals_are_recorded_not_just_actions—                              27 findings after verification, from 25 distinct agents, spanning
pass, covering the alter/remove/reorder cases of T-P5; external      13 CWE classes, in 3.55 hours, with 32 PoC scripts and 27
anchoring against a full-rewrite adversary remains design-           evidence screenshots (Table V).
only. Of the harness’s 312 passing unit tests, 109 exercise the
P1–P5 modules directly—P1 (grounding, validation) 52, P2                                       TABLE V
                                                                          A RCHIVED REFERENCE RUN ( T E S T A S P N E T . V U L N W E B . C O M ,
(claims, prosecutor) 19, P4 (capability, scope) 27, P5 (audit)                                BLACK - BOX ).
11—while the remainder cover recon, planning, chaining, and
reporting; P3’s severity-cap logic is covered within the P1          Quantity                                                                       Value
validation and P2 claim tests rather than a dedicated module.
                                                                     Agents scheduled                                                        245
The full suite reports 312 passed at the pinned commit.              Agents producing a verified finding                                      25
                                                                     Findings after verification                                              27
                            TABLE III                                  Critical / High / Medium / Low / Info                   1 / 6 / 14 / 4 / 2
  E XECUTED P4 CAPABILITY- TOKEN BATTERY (CLI, DETERMINISTIC ).      Distinct CWE classes                                                     13
                                                                     PoC scripts / evidence screenshots                                  32 / 27
Case                            Expected   Observed                  Wall-clock time                                                       3.55 h
                                                                     Artifact bundle root (SHA-256)                       5e018a1e...55bce3
Valid token                     verify     verified, grant printed
Tampered token                  refuse     refused (signature)
Wrong signing key               refuse     refused                      What the archived run evidences, precisely. The artifacts
Expired (exp past)              refuse     flagged expired           record, per finding, the receipt text, PoC reference, adversarial
Off-grant host in local scope   drop       dropped from hard scope   votes, a validated flag, a review_status, and a
Off-grant primary target        refuse     reconned (gap)
                                                                     severity label (P1, P2, and the labelling half of P3). They
                                                                     do not contain populated CVSS vectors (the cvss field is
                                                                     empty for all 27), nor a capability token, nor an audit-log
                  VI. I MPLEMENTATION C OST
                                                                     file: this run predates full instrumentation of those outputs.
   Table IV reports the pinned instance, measured by Ap-             CVSS-vector computation (P3) is evidenced by the code and
pendix A. Enforcing P1–P5 is not free: the validators, token         its 312 unit tests, not by this archived run. Token verifica-
and audit machinery, and multi-model verification account for        tion (P4) and the hash-chained audit log (P5) are evidenced
a substantial fraction of the code, and the multi-model vote         separately by the executed acceptance battery of Section V-D,
adds per-finding token and latency cost over a single-model          which produced a real capability token and a hash-chained
pipeline (quantified by the protocol of Appendix H). The             audit.jsonl and also revealed the P4 primary-target gap.
scale itself is a data point for RQ3: assurance is realizable        The archived target run itself contains no audit log; the bundle
at tens of modules and tens of thousands of lines, an order          additionally contains a separate audit.jsonl produced by
of magnitude beyond a trace-reproduction harness such as             the deterministic P5 acceptance run (Section V-D) and must
Cochise (630 LOC [7]), which is consistent with the gap being        not be read as the audit trail of the archived engagement.
real engineering rather than a prompt.                               The archived run’s model version, temperature, vote count,
token budget, concurrency, and seed were not persisted and          could inflate recall; the honest negative partially counters an
are reported as unknown; the harness default at that time           over-optimistic reading, but external validity is limited until
was anthropic:claude-opus-4-8. Producing a single                   diverse, partly-private targets are used.
fully-instrumented engagement run that carries all five proper-         Precision–recall. P1’s outside-the-model rule maximizes
ties’ artifacts end-to-end—with those parameters recorded—is        precision and can suppress true positives (the testphp nega-
part of the protocol in Appendix H.                                 tive); whether the resulting report is more useful than a higher-
   Reproducibility. The non-sensitive artifacts (recon, find-       recall one is the empirical question the protocol answers.
ings, PoCs, exploitation notes, the executed acceptance re-             Residual surface (T2). No harness eliminates prompt in-
sults, and the produced audit.jsonl; the public target              jection through hostile tool output; adversarial content can in-
contains no third-party data) form a content-addressed bundle       fluence an agent’s next step before verification runs. P1 limits
assurance-artifacts-v1.tar.gz (40 files, 84 KB,                     the consequences—an injected instruction cannot manufacture
MIT-licensed), available from the project repository [34] at        a receipt that passes a per-CWE validator—but the planning
the pinned commit (Table II), with per-file SHA-256 manifest        layer remains a target, and confining every agent-authored
root                                                                command is only partial in the current implementation.
               5e018a1e1a9dc2d19dd82eb0fb3e8af2                         P4 primary-target gap (found by executing T-P4). The
               7351357f72932d7e7a7df5ae8655bce3
                                                                    acceptance battery of Section V-D revealed that, while the
The published hash is a content identifier for the bundle,          token correctly constrains agent scope, an offline engagement
not an external anchor for the audit chain (Appendix G).            whose primary target lies outside the grant is reconned and
Appendix A lists the commands to recompute every number             logged allow rather than refused. This is a concrete enforce-
and the manifest root, and the pinned commit (Table II) fixes       ment gap between the specification of P4 and the tested build;
the code.                                                           it is the reason P4 is scored partial, and closing it (checking
   An honest negative. On separate runs against                     the primary target against the constrained scope at engagement
testphp.vulnweb.com (a PHP/MySQL sibling known                      start) is the first fix the reference implementation owes.
to contain SQL injection), the instance scheduled 245                   Property strength. As specified, P4’s HMAC form proves
agents but reported zero confirmed findings. We report              holder-of-key, not client intent; the asymmetric evolution (Ap-
this. The deterministic SQLi validator (CWE-89) requires            pendix F) is required to bind client and operator cryptograph-
a reproducible baseline-versus-attack differential; those           ically. P5’s guarantee against a full-rewrite adversary holds
runs terminated at the observation phase—consistent with            only with external anchoring enabled (Appendix G); without
Equation (6)—before an agent produced one. The behavior is          it the mechanism detects local, partial tampering only. We state
correct by P1 yet is a false negative against a truly vulnerable    these as scoped guarantees, not absolutes.
target, illustrating that a strict evidence rule trades recall
for precision. The protocol of Appendix H is designed to                        IX. E THICS AND R ESPONSIBLE U SE
quantify exactly this trade-off.                                       All runs discussed were conducted against targets pub-
   VIII. D ISCUSSION , L IMITATIONS , AND T HREATS TO               lished by their owners for security testing (the Acunetix
                        VALIDITY                                    vulnweb.com family); no third-party data, credentials, or
                                                                    personal information are disclosed, and evidence contains
   No assurance benchmark; single instrumented run (pri-
                                                                    only synthetic markers chosen by the harness. Autonomous
mary threats). No shared, public benchmark measures truth-
                                                                    offensive tooling is dual-use; the assurance properties defined
under-scrutiny, scope enforcement, or auditability, so every
                                                                    here—enforced authorization (P4), tamper-evident account-
ranking claim is out of scope, and the empirical evidence
                                                                    ability (P5), and the OT safety model—are precisely the
here is one archived behavioral run plus a unit-tested code-
                                                                    mechanisms that constrain misuse and make an authorized en-
base. The paper’s claim is an initial existence argument, not
                                                                    gagement defensible. We describe an architecture and release
a demonstration that each property holds on every action.
                                                                    no exploit payloads for unpatched third-party vulnerabilities.
Appendix H specifies the missing measurements: at least three
                                                                       Competing interests and funding. The author is the
to five vulnerable applications with known ground truth (e.g.,
                                                                    developer of NeuroSploit, the reference instance; this is the
OWASP Juice Shop, WebGoat, DVWA at fixed versions, a
                                                                    paper’s sole competing interest and the reason the study is
deliberately-vulnerable API, one authorized real scope), ≥ 3
                                                                    framed as an existence argument rather than a comparison.
runs per target, and reported true/false positives and negatives,
                                                                    The work received no external funding.
precision, recall, cost, tokens, and time; an ablation removing
each of P1’s deterministic validators, the vote, the prosecutor,       Availability. The implementation is open source [34],
and the P3 cap, and comparing common logging against P5;            pinned by Table II; the run artifact bundle is anchored by the
adversarial P4 and P5 batteries; and baselines (NeuroSploit         manifest root in Section VII, enabling independent inspection.
with P1–P5 disabled, a plain ReAct loop, a single-model
                                                                                           X. C ONCLUSION
configuration, and a conventional scanner on the same targets).
   Possible memorization. The archived run targets a widely-          The useful frontier for autonomous penetration testing is
used public application that may appear in training data, which     shifting from capability to assurance, and assurance is a
property of the harness. We defined five implementation-             present (e.g., IDOR requires an owner-resource receipt and a
independent properties, each with a formal model and an              cross-identity receipt). (4) Contradiction: if any receipt refutes
acceptance test, related them to capability-based security,          the claim (e.g., the anonymous request was denied), return
tamper-evident logging, and provenance, positioned existing          Rejected. (5) Verdict: Confirmed iff roles present, bound, and
systems against them, and studied one open-source imple-             the class predicate holds; else NeedsReview. The procedure
mentation as a version-pinned, content-addressed existence           is deterministic and model-free; it is the operational meaning
argument—while stating precisely what its archived run does          of “outside the model” in P1.
and does not evidence and specifying the multi-target, ablation,
                                                                                           A PPENDIX C
and adversarial protocol that would turn the framework’s obli-
                                                                                D ETERMINISTIC VALIDATOR C ATALOG
gations into measurements. Building that assurance benchmark
is the work we hope this framework enables.                             The 27 validators reference 31 CWE identifiers, including
                                                                     CWE-16, 22, 78, 79, 89, 113, 200, 209, 306, 307, 319, 347,
                      ACKNOWLEDGMENT                                 352, 384, 524, 525, 530, 548, 601, 611, 614, 639, 644, 650,
   The author thanks the maintainers of the public vulnerable-       863, 915, 918, 942, 1004, 1021, 1336. Representative predi-
target and benchmark ecosystems. Generative language-model           cates: SQLi (89) a reproducible baseline-vs-attack differential;
tooling assisted with drafting, reference verification, and copy-    XSS (79) a browser executing a harness-chosen marker (proof
editing; all sources were checked by the author against their        by execution); IDOR (639) identity B reading identity A’s
original records, and the author takes full responsibility for the   resource with content-overlap confirmation, rejecting identical
content, including any errors.                                       identities or generic login-page bodies; SSRF (918) an out-of-
                                                                     band callback carrying the marker or retrieval of a controlled
                       A PPENDIX A                                   internal resource; missing authentication (306) a protected
               R EPRODUCIBILITY C OMMANDS                            resource served to an anonymous request with content match,
  All numbers in Tables II–V were produced at the pinned             rejecting the case where the anonymous request is denied.
commit by the following, on the environment of Table II.
                                                                                                A PPENDIX D
# version
git rev-parse HEAD                                                                     T HE E VIDENCE P ROSECUTOR
git describe --tags --always
git log -1 --format=%ci
                                                                        The prosecutor answers, in order: what was observed;
rustc --version                                                      which sentence exceeds it; what would make the impact
# complexity (Table III)
                                                                     factual; and whether the finding survives removing the impact
find agents_md -name ’*.md’ -type f | wc -l # agents: 446            sentence. It returns one of {supported finding, informa-
find crates/harness/src -name ’*.rs’ | wc -l # modules: 40
find crates/harness/src -name ’*.rs’ -print0 \
                                                                     tional observation, insufficient evidence, invalid claim};
  | xargs -0 cat | wc -l # LOC: 23370                                it cannot silently delete, and it cannot force-retain a claim
grep -rE ’#\[test\]|#\[tokio::test\]’ \
  crates/harness/src | wc -l # tests: 312
                                                                     with no security-relevant mechanic (which becomes informa-
grep -rE ’impl CweValidator for’ \                                   tional observation or insufficient evidence). The finding is
  crates/harness/src/validation.rs | wc -l # validators: 27
                                                                     rebuilt from the returned minimal supported claim, decoupling
# build + tests                                                      the reduction (this component) from rejection (the vote and
cargo test --locked
                                                                     validators), which is what prevents a proven mechanic from
# a fresh, fully-instrumented run (protocol, App. F)                 being lost to an overstated headline.
neurosploit run <target> \
  --capability-token <path> \                                                               A PPENDIX E
  --model <provider:model@version> \
  --votes <n> --seed <seed> \                                                  S EVERITY C AP AND W ORKED E XAMPLE
  --config artifact/config.yaml \
  --audit artifact/audit.log                                           Severity uses the CVSS v3.1 base metrics [31]; each metric
# integrity                                                          value must cite a receipt. The demonstrated-impact ladder (3)
shasum -a 256 <each artifact> > MANIFEST.sha256
shasum -a 256 MANIFEST.sha256 # bundle root                          caps the base score:
                                                                             Rung        Typical impact metrics   cap (base)
                           A PPENDIX B
                                                                             reached     C:N/I:N/A:N, no data     ≤ 6.9 (Med)
          T HE S U P P O R T S D ECISION P ROCEDURE                          read        C:L/H, I:N               ≤ 8.9 (High)
   Input: a claim c, its cited receipts cite(c), the engagement              wrote       I:L/H                    ≤ 9.4
mode, and the target/action binding of each receipt. Output:                 RCE         C:H/I:H/A:H              ≤ 10.0 (Crit)
                                                                             crossed     scope S:C, C/I/A:H       ≤ 10.0 (Crit)
Confirmed, Rejected, or NeedsReview. Procedure. (1)
Binding: each receipt’s action hash must match a logged              Example.      A       reflected       SQL       error     on
action against an in-scope target and postdate that action; a        login.aspx       with     no     data   extraction:   vector
receipt that cannot be bound is dropped. (2) Class dispatch:         AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N                   yields
route to the per-CWE validator (Appendix C); a class with            a low base, and ℓd = reached caps at Med; the potential
no validator yields NeedsReview (never auto-Confirmed).              score sevp records C:H/I:H (a full extraction) so the un-
(3) Composition: all receipt roles the class requires must be        demonstrated worst case is not lost. A NeedsReview metric
leaves the finding at label-only severity with no computed          common logging vs. anchored P5—reporting the change in
base until resolved.                                                false-positive rate and cost attributable to each. Baselines:
                                                                    NeuroSploit with P1–P5 disabled, a plain ReAct loop, a single-
                       A PPENDIX F                                  model configuration, and a conventional scanner on the same
          C APABILITY T OKEN AND K EY C USTODY                      targets. Adversarial P4 (T-P4): off-scope redirect, DNS re-
   Wire     form:    ns-cap.v1.<b64url(payload)>.                   binding, alternate IPv6/decimal/hex encodings, CNAME to ex-
<b64url(mac)>. Payload fields: iss (client key id),                 ternal host, userinfo URL, over-broad wildcard, unauthorized
aud (harness instance), eng (engagement id), op (operator           port, mid-run DNS change, discovered subdomain, expired
id), scope (hosts/CIDRs/URL prefixes), ceiling (max                 token, tampered token, in-session widening—each must be
action kind, risk), env, nbf, exp, nonce. Verification              denied and logged. Adversarial P5 (T-P5): record removed,
follows Section IV. Custody: the current HMAC form uses             altered, reordered; evidence substituted; token swapped; log
a shared secret and proves holder-of-key only; to bind client       truncated; whole chain rebuilt—each must be detected (the
and operator, an asymmetric signature (client-held Ed25519          last with anchoring).
private key, harness-held public key) is the recommended
evolution, following the caveat model of Macaroons [21] and                              A PPENDIX I
the registered-claims model of JWT [22]. Replay: nonce                     C OMPARATIVE C ODING P ROTOCOL (TABLE I)
freshness plus short exp. Revocation: a revocation list keyed          Each cell of Table I was assigned from the analyzed artifact
by eng/iss and short lifetimes. Rotation: iss key id selects        of each system, using fixed criteria. Analyzed artifacts:
the verifying key, enabling overlap during rotation.                PentestGPT [2] (paper and public repository), Cochise [7]
                                                                    (paper and 630-LOC release), MAPTA [4] (paper), Pentest-
                      A PPENDIX G                                   Judge [13] (paper), and NeuroSploit [34] (source at the pinned
          AUDIT L OG S CHEMA AND A NCHORING                         commit, Table II). Coding rule: ✓ = the artifact describes or
   Each          record          carries         timestamp,         implements a mechanism meeting the property’s acceptance
agent, hypothesis, action, target,                                  test (Section IV); ∼ = a partial or process-level mechanism
policy_decision, tool, result,                                      that does not fully meet the test; — = the artifact makes
evidence_hash, capability_token,                             and    no claim to the property. An — records the absence of a
hi = H(ri ∥hi−1 ). verify() recomputes the chain                    claim in the analyzed artifact and is not evidence of absence
and localizes the first break. Against a local adversary            in code that was not reviewed. Per-property predicate:
this detects removal, alteration, and reordering. Against a         P1—an out-of-model check that a receipt supports a claim;
full-rewrite adversary, external anchoring is required: periodic    P2—a documented rule that reduces rather than deletes an
signing of hi with a key outside the run, a trusted timestamp,      overstated finding; P3—a computed, evidence-graded severity
a write-once store, or publication of roots to a transparency       (not by-class); P4—a signed, verifiable scope grant enforced
log [25], [26], [28]. The acceptance test T-P5 exercises            as a ceiling; P5—an append-only, integrity-verifiable action
removal, alteration, reordering, evidence substitution, token       log. NeuroSploit assignments: P1 ✓ (grounding and 27
swap, truncation, and whole-chain rebuild; the last passes          validators, Section V-D); P2 ✓ (prosecutor with four typed
only with anchoring enabled.                                        outcomes); P3 ∼ (calculator and cap implemented, but CVSS
                                                                    vectors not populated in the archived run); P4 ∼ (token
                      A PPENDIX H                                   integrity enforced, primary-target check missing); P5 ∼ (hash
        E VALUATION P ROTOCOL ( TO BE EXECUTED )                    chain present and tested, external anchoring design-only). A
   This protocol specifies the measurements not yet performed;      second independent coder is recommended before peer review;
it is stated so results are comparable when produced. The           the criteria are published here so the coding is contestable.
deterministic P4 and P5 batteries below were partially ex-
ecuted already (Section V-D, Table III); the multi-target,                                     R EFERENCES
ablation, and baseline measurements, which require live model       [1] R. Fang, R. Bindu, A. Gupta, and D. Kang, “LLM Agents can Au-
runs, remain to be executed. Targets: ≥ 3–5 applications                tonomously Exploit One-day Vulnerabilities,” arXiv:2404.08144, 2024.
                                                                    [2] G. Deng et al., “PentestGPT: Evaluating and Harnessing Large Language
with published ground truth—OWASP Juice Shop, WebGoat,                  Models for Automated Penetration Testing,” in Proc. 33rd USENIX
DVWA (pinned versions), a deliberately-vulnerable API, and              Security Symp., 2024. arXiv:2308.06782.
one authorized real scope—each with an enumerated expected-         [3] Y. Zhu, A. Kellermann, A. Gupta, P. Li, R. Fang, R. Bindu, and D.
                                                                        Kang, “Teams of LLM Agents can Exploit Zero-Day Vulnerabilities,”
vulnerability list. Design: ≥ 3 runs per target with fixed              arXiv:2406.01637, 2024.
model/version, temperature, vote count, seed, token budget,         [4] I. David and A. Gervais, “Multi-Agent Penetration Testing AI for the
and concurrency, all recorded in the run config. Metrics: true          Web (MAPTA),” arXiv:2508.20816, 2025.
                                                                    [5] L. Wang et al., “Automated Penetration Testing with LLM Agents and
positives, false positives, false negatives against ground truth;       Classical Planning (CHECKMATE),” arXiv:2512.11143, 2025.
precision, recall; cost, tokens, wall-clock; and, for P3, the       [6] H. Kong, D. Hu, J. Ge, L. Li, H. Li, and T. Li, “Pentest-R1: Towards
CVSS delta between evidence-graded and by-class scoring.                Autonomous Penetration Testing Reasoning Optimized via Two-Stage
                                                                        Reinforcement Learning,” arXiv:2508.07382, 2025.
Ablation: remove each deterministic validator, the vote, the        [7] A. Happe and J. Cito, “Cochise: A Reference Harness for Autonomous
prosecutor, and the P3 cap; run with and without P4; compare            Penetration Testing,” arXiv:2605.11671, 2026.
 [8] R. Fang, R. Bindu, A. Gupta, Q. Zhan, and D. Kang, “LLM Agents can
     Autonomously Hack Websites,” arXiv:2402.06664, 2024.
 [9] A. K. Zhang et al., “Cybench: A Framework for Evaluating Cyberse-
     curity Capabilities and Risks of Language Models,” arXiv:2408.08926,
     2024.
[10] R. Yang, M. Cheng, G. Deng, T. Zhang, J. Wang, and X. Xie, “Pen-
     testEval: Benchmarking LLM-based Penetration Testing with Modular
     and Stage-Level Design,” arXiv:2512.14233, 2025.
[11] Z. Wang, T. Shi, J. He, M. Cai, J. Zhang, and D. Song, “CyberGym:
     Evaluating AI Agents’ Real-World Cybersecurity Capabilities at Scale,”
     arXiv:2506.02548, 2025.
[12] Z. Wang et al., “ExploitGym: Can AI Agents Turn Security Vulnerabil-
     ities into Real Attacks?” arXiv:2605.11086, 2026.
[13] S. Caldwell, M. Harley, M. Kouremetis, V. Abruzzo, and W. Pearce,
     “PentestJudge: Judging Agent Behavior Against Operational Require-
     ments,” arXiv:2508.02921, 2025.
[14] V. K. Nguyen and M. I. Husain, “Penetration Testing of Agentic AI:
     A Comparative Security Analysis Across Models and Frameworks,”
     arXiv:2512.14860, 2025.
[15] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz,
     “Not What You’ve Signed Up For: Compromising Real-World LLM-
     Integrated Applications with Indirect Prompt Injection,” in Proc. 16th
     ACM Workshop on Artificial Intelligence and Security (AISec), 2023.
[16] Y. Yang, C. Gao, D. Wu, Y. Chen, Y. Li, and S. Wang, “MCPSecBench:
     A Systematic Security Benchmark and Playground for Testing Model
     Context Protocols,” arXiv:2508.13220, 2025.
[17] L. Gao et al., “RARR: Researching and Revising What Language
     Models Say, Using Language Models,” in Proc. ACL, 2023.
[18] P. Manakul, A. Liusie, and M. J. F. Gales, “SelfCheckGPT: Zero-
     Resource Black-Box Hallucination Detection for Generative Large Lan-
     guage Models,” in Proc. EMNLP, 2023.
[19] J. B. Dennis and E. C. Van Horn, “Programming Semantics for Multi-
     programmed Computations,” Comm. ACM, vol. 9, no. 3, pp. 143–155,
     1966.
[20] M. S. Miller, K.-P. Yee, and J. Shapiro, “Capability Myths Demolished,”
     Systems Research Lab, Johns Hopkins Univ., Tech. Rep. SRL2003-02,
     2003.
[21] A. Birgisson, J. G. Politz, Ú. Erlingsson, A. Taly, M. Vrable, and M.
     Lentczner, “Macaroons: Cookies with Contextual Caveats for Decentral-
     ized Authorization in the Cloud,” in Proc. NDSS, 2014.
[22] M. Jones, J. Bradley, and N. Sakimura, “JSON Web Token (JWT),” RFC
     7519, IETF, 2015.
[23] H. Krawczyk, M. Bellare, and R. Canetti, “HMAC: Keyed-Hashing for
     Message Authentication,” RFC 2104, IETF, 1997.
[24] F. B. Schneider, “Enforceable Security Policies,” ACM Trans. Inf. Syst.
     Secur., vol. 3, no. 1, pp. 30–50, 2000.
[25] B. Schneier and J. Kelsey, “Secure Audit Logs to Support Computer
     Forensics,” ACM Trans. Inf. Syst. Secur., vol. 2, no. 2, pp. 159–176,
     1999.
[26] S. A. Crosby and D. S. Wallach, “Efficient Data Structures for Tamper-
     Evident Logging,” in Proc. 18th USENIX Security Symp., 2009.
[27] R. C. Merkle, “A Digital Signature Based on a Conventional Encryption
     Function,” in Advances in Cryptology (CRYPTO), 1987.
[28] B. Laurie, A. Langley, and E. Kasper, “Certificate Transparency,” RFC
     6962, IETF, 2013.
[29] S. Torres-Arias, H. Afzali, T. K. Kuppusamy, R. Curtmola, and J.
     Cappos, “in-toto: Providing Farm-to-Table Guarantees for Bits and
     Bytes,” in Proc. 28th USENIX Security Symp., 2019.
[30] L. Moreau and P. Missier (eds.), “PROV-DM: The PROV Data Model,”
     W3C Recommendation, 2013.
[31] FIRST.org, “Common Vulnerability Scoring System v3.1:
     Specification Document,” 2019. https://www.first.org/cvss/v3.1/
     specification-document. Accessed: 2026-09-18.
[32] OWASP Foundation, “OWASP Top 10:2021,” 2021. https://owasp.org/
     Top10/. Accessed: 2026-09-18.
[33] MITRE Corporation, “MITRE ATT&CK Framework,” 2023. https://
     attack.mitre.org/. Accessed: 2026-09-18.
[34] J. A. dos Santos, “NeuroSploit: An Autonomous Multi-Model
     Penetration-Testing Harness,” open-source software, commit 8894649,
     2026. https://github.com/JoasASantos/NeuroSploit. Accessed: 2026-09-
     18.
