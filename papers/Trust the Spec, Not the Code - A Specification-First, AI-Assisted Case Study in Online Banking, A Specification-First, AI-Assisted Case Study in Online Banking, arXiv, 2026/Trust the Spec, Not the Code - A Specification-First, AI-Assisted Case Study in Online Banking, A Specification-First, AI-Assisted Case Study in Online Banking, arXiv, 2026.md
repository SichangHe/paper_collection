                                                                     Trust the Spec, Not the Code
                                                           A Specification-First, AI-Assisted Case Study in Online Banking

                                                                                          Eitan Farchi∗

                                                                                       September 9, 2026
arXiv:2609.07365v1 [cs.SE] 7 Sep 2026




                                                                                             Abstract
                                                  Formal specification promises early error detection, explicit invariants, and correctness by de-
                                                  sign, yet its notational cost has kept it out of mainstream practice. We argue that AI removes
                                                  much of that cost: natural language enriched with lightweight mathematics, written in LATEX,
                                                  can serve as an intermediate specification language that is precise enough to reason over and
                                                  prove, while a large language model (LLM) reviews it for ambiguity, drafts proofs, and gener-
                                                  ates the implementation. The specification becomes the artifact one authors, reviews, proves,
                                                  and refines; the code becomes regenerable output. This paper is a follow-on to a prior study
                                                  that established the discipline on an organizational-knowledge-growth simulation [6]. Here we
                                                  replicate the discipline in a different domain—an online-banking fund-transfer service—and
                                                  extend it. The two domains share one spine: a conservation invariant (knowledge in the prior
                                                  study, money here), which suggests the approach generalizes across domains. We contribute:
                                                  (i) a second, independent case study of the method; (ii) a stress-test of the method on a richer
                                                  problem—scheduled/recurring transfers—whose generated code grows substantially while the
                                                  invariant and its proof do not; (iii) an AI-proposed runtime coverage model for invariants
                                                  (“never violated ̸= covered”); and (iv) a Z formalization, including paired success/failure oper-
                                                  ation schemas and an invariant proved over the inductive set of all reachable configurations,
                                                  together with an experiment in which the AI proposes the Z interfaces itself. We are explicit
                                                  about the method’s limits: the proofs and runtime checks live at the specification level and do
                                                  not establish that the generated code refines the specification—that step is delegated to the
                                                  AI. This is a case study, not a controlled experiment.

                                        Keywords: specification-driven development; formal methods; Z notation; conservation invariants;
                                        large language models; AI-assisted software engineering.


                                        1        Introduction
                                        The benefits of formal specification have never been seriously in doubt: design flaws surface before
                                        code exists, assumptions are written down as explicit invariants rather than buried in implemen-
                                        tation, and one can reason about a system instead of debugging it into shape. What kept these
                                        benefits out of industry was cost—heavyweight notations such as Z, VDM, and B demand math-
                                        ematical maturity to write and to maintain, the pool of engineers who can author or even read
                                        such specifications is small, and so teams ship informal prose and defer correctness to testing and
                                        debugging [8, 9, 4, 1].
                                            Large language models change this cost structure. Modern LLMs can read specifications written
                                        in natural language augmented with lightweight mathematics, flag ambiguities and inconsistencies,
                                        propose invariants and proofs, and generate running code [3, 2]. This enables a shift in what the
                                            ∗
                                                IBM Research. Email: farchi@il.ibm.com.


                                                                                                 1
engineer treats as primary: the specification becomes the artifact one authors, reviews, proves, and
refines, while the code becomes regenerable output that need not be read line by line. Validation
shifts left—design flaws are caught in the specification, where they are cheap, rather than in the
code, where they are not.
    A prior study introduced this discipline and applied it to a simulation of organizational knowl-
edge growth [6]. A natural question is whether the discipline transfers to a different domain with
genuinely different subject matter. This paper answers that question with a second case study in
online banking. It also extends the method in two ways—a runtime coverage model for the central
invariant and a Z formalization of the interfaces—and stress-tests it against a richer problem, sched-
uled/recurring transfers, where the operation grows substantially while the invariant and its proof
do not. Crucially, both domains turn out to rest on the same structural device—a conservation
invariant—which is the clearest evidence we have that the approach is not tied to one problem.

Research questions.
RQ1. Does the specification-first, AI-assisted discipline transfer to a new domain (online banking)
   with a different conserved quantity?
RQ2. Does the discipline scale as the specification grows in operational complexity (from one-time
   to scheduled/recurring transfers)?
RQ3. What does it take to establish, and to cover at runtime, the central invariant—and where
   are the honest limits of the confidence obtained?

Contributions (stated as a delta over [6]). The first two contributions concern scope (a new
domain and a richer problem); the last two are methodological additions beyond the predecessor’s
specify–prove–assert loop.
 1. A second, independent case study of the discipline in a new domain, giving first evidence of
    cross-domain generalization: the conservation-invariant spine recurs with money in place of
    knowledge.
 2. A stress-test of the method on a richer problem—scheduled/recurring transfers—in which the
    generated code grows markedly while the invariant and its proof are unchanged.
 3. Methodological addition 1: a runtime coverage model for invariants—proposed by the AI when
    asked what to check, then reviewed and found adequate—that distinguishes “never observed
    to fail” from “all invariant-relevant paths exercised.”
 4. Methodological addition 2: a Z interface layer, with paired success/failure (Ξ) schemas and an
    invariant proved over the inductive set of all reachable configurations, plus an experiment in
    which the AI proposes the Z interfaces from the natural-language specification.


2    Background and Relationship to Prior Work
Formal specification and Z. Z is a state-based specification notation built on typed set theory
and first-order logic; a schema groups a piece of state (or a state transition) with the predicates that
constrain it, and at the code level corresponds to a typed interface with invariants and operation
contracts [8, 9]. We use Z for the interface layer because pre/postconditions and state invariants
become explicit and reviewable, while the AI is free to implement the operation in any way it
chooses so long as the contract is met.



                                                   2
    Dimension                 Predecessor [6]                    This paper

    Domain                    Organizational        knowledge    Online banking (fund transfer)
                              growth
    Conserved quantity        Knowledge items                    Money (sum of account balances)
    Operations                Single simulation                  One-time + scheduled/recurring
                                                                 transfers
    Proof scope               Per-stage invariant                Inductive set of all reachable con-
                                                                 figurations
    Coverage model            —                                   Runtime coverage (never-violated
                                                                 ̸= covered)
    Z formalization           Limited                            Paired success/fail (Ξ) schemas;
                                                                 AI-suggested interfaces

                         Table 1: Differentiation from the predecessor study.


Conservation invariants. A conservation invariant asserts that some global quantity is pre-
served by every operation. Such invariants are attractive targets for this discipline: they are easy
to state, provable by induction over operations, and cheap to assert at runtime. The prior study
used conservation of knowledge items; here the conserved quantity is money.

The authoring flow. The discipline proceeds along a pipeline: natural language → natural math
(natural language augmented with lightweight mathematics) → proof of the key invariant → Z in-
terfaces → generated code. Reviewing the proof appears to focus the ambiguity feedback, tightening
the specification before any code exists. (In this study the Z interfaces were in fact formalized after
the code; see Sections 3 and 7.)

Relationship to the predecessor. This paper is a companion to [6], which established the
method and its motivation on an organizational-knowledge-growth simulation. We do not re-
argue that motivation or re-describe that example; we cite it and focus on what is new. Table 1
summarizes the differences.
    Beyond the immediate predecessor, the work sits alongside classical formal-methods practice [8,
9, 4, 1] and recent work on LLM-based code generation [3, 2]; it differs from automated program
verifiers such as Dafny [5] in that we do not mechanically verify the generated code—we verify the
specification and treat the code as regenerable output (see Section 9).


3     Method: One Loop, Applied to Every Problem
The discipline is a single loop applied to each problem:
 1. AI reviews the specification, flagging ambiguities and inconsistencies before any code exists.
 2. The human draws the line, resolving each ambiguity and deciding what is controlled versus
    left to the AI.
 3. Prove the invariant (here, conservation), by induction over operations.
 4. Turn the invariant into a runtime check that is asserted as the simulation runs.


                                                    3
 5. Fix the interface in Z, pinning state and operations down as precise contracts.
 6. Generate the code and leave it uninspected; if the specification is right, the code is regener-
    able.
The list above is the prescribed order, in which the Z interfaces are fixed before code is generated.
This case study was in fact conducted code-first: the natural math specification, proof, and runtime
assertion came first (Sections 4–6), and the Z formalization was added afterward as a separate pass
(Section 7) that tightened and re-verified the contracts. We report the study in that historical order
for faithfulness, but recommend the prescribed Z-before-code order going forward (see Section 7
and the conclusion); the mismatch is itself an observation about how the discipline tends to be
practised before it is internalized. The remainder of the paper applies this loop twice (one-time
and scheduled transfers), adds the coverage model, and develops the Z layer.


4      Case Study A: One-Time Transfer
Specification (natural math). This case study elaborates an existing online-banking specification—
the Instantpay mobile-banking requirements document [7]—and in particular its fund-transfer re-
quirement 3.2.1.7 (functional requirement 1.7). We begin with the simplest case, a one-time trans-
fer; Case Study B (Section 5) then develops the further transfer types the same requirement calls
for. We make the requirement precise as a natural math specification, as follows. We are given a set
of users U = {u1 , . . . , un } and a set of accounts AC = {ac1 , . . . , ack }, together with an ownership
function AC (·) : U → P(AC ) assigning to each userSthe accounts it owns. Ownership partitions
the accounts: for ui ̸= uj , AC (ui ) ∩ AC (uj ) = ∅ and u∈U AC (u) = AC , so every account belongs
to exactly one user. A balance function B : AC → N gives each account a non-negative balance.
     The one-time transfer accepts (ui , aci , uj , acj , f ) with aci ∈ AC (ui ), acj ∈ AC (uj ), and amount
f . If B (aci ) − f ⩾ 0 it updates B (aci ) 7→ B (aci ) − f and B (acj ) 7→ B (acj ) + f ; otherwise it does
nothing.

    Human prompt (excerpt)
    Generate a Python program that implements the above. Simulation: three users, six accounts (user 1
    owns accounts 1–2, user 2 owns 3–4, user 3 owns 5–6), initial balances chosen randomly; at each step
    choose a random transfer and report inputs and result. (Excerpt; the full prompt and the AI’s reply
    appear in Appendix A.)

The generated program is 106 lines of Python (generated code); inspection of the execution log
suggested it was correct, but we increase confidence by proving and then asserting an invariant
rather than by reading the code. The simulation proceeds in discrete stages; each stage selects one
transfer and either executes it (if funds suffice) or leaves the state unchanged. In Case Study B
(Section 5) a clock is added, advancing by one time unit per stage.

Ambiguities surfaced by review. ThePtarget property is a conservation invariant: the total
amount of money held across all accounts, ac∈AC B (ac), is unchanged by any transfer. Asked to
prove this invariant, the AI first surfaced issues that had to be resolved for even the statement to
be well-defined:
 1. Summation notation. aci ∈AC aci is ill-formed; the summand must be the balance B (aci ),
                               P
    not the account identifier.
 2. Negative balances. The specification does not say whether a transfer may drive a balance
    negative; the proof holds either way, as it uses only the cancellation −f + f = 0.


                                                     4
                     BEFORE                                   AFTER (transfer $40, A→B)
                 A                          $100          A                    $60
                 B         $20                            B                    $60
                     Σ = $120                                 Σ = $120

Figure 1: PThe conserved total is unchanged by a transfer (illustrative two-account slice). The
invariant ac B (ac) is asserted before and after every transfer.


 3. General vs. simulation state. The lemma must hold for arbitrary AC and B , not merely
    the fixed six-account configuration.
 4. Meaning of “amount of money.” The informal phrase in the source specification was pinned
    down, at the AI’s prompting, to the sum of the values of the balance function B —the definition
    adopted in the invariant stated above.

The invariant, proved.

Lemma 1 (Conservation of total money). Let B : AC → N be the balance function before a one-
time transfer of amount amt from account srcA to account tgtA, and let B ′ be the updated balance
function with B ′ (a)              if a = srcA, B ′ (a) = B (a) + amt if a = tgtA, and B ′ (a) = B (a)
                   P = B (a)′ − amtP
otherwise. Then a∈AC B (a) = a∈AC B (a).

Proof. Summing B ′ over AC and isolating the two affected accounts,
             X               X
                  B ′ (a) =
                                                                           
                                    B (a) + B (srcA) − amt + B (tgtA) + amt
                a∈AC                a∈AC
                                 a̸=srcA,tgtA
                                  X                             X
                             =          B (a) − amt + amt =           B (a).
                                 a∈AC                          a∈AC

The proof does not rely on B (srcA) ⩾ amt: a rejected transfer leaves B ′ = B , so the lemma holds
for aborted transfers as well. Fees or interest would require a modified statement.

RuntimePassertion. The proved equality is turned into a live oracle: the simulation computes
Sbefore = ac B (ac) and Safter around each transfer and asserts Sbefore = Safter . Figure 1 shows the
conserved total for a representative transfer.


5    Case Study B: Scheduled Transfers
We extend the specification with time and recurrence, developing the additional transfer types that
requirement 3.2.1.7 [7] calls for beyond the one-time case. We keep the stage-based simulation loop
of Case Study A and attach a clock to it: a current time t ∈ N, starting at 0 and advancing by one
unit at the start of each stage, so that stage number and clock value coincide. In addition to the
one-time transfer, a planned transfer p = (ui , aci , uj , acj , f , t ′ ) with t ′ > t is placed in a planned-
transfer set P ; when the clock reaches t ′ (that is, at the stage with time t ′ ), the corresponding
one-time transfer is executed and p is removed from P . The same stage also admits recurring
transfers—a transfer repeated every k time units—which require no new machinery: a periodic
transfer is simply a sequence of ordinary one-time transfers, so the conservation lemma applies to
each occurrence unchanged. Figure 2 shows the lifecycle.

                                                      5
                                 due t=3
                               schedule p                  execute p


                                   t=1          t=2          t=3       t=4
                                            p waits in P


Figure 2: Scheduled-transfer lifecycle: p is scheduled at t=1 for t=3, persists in P , and executes
when due.

The invariant does not change. The generated program grows to 265 lines (generated code,
about 2.5× the one-time version), yet Lemma 1 still applies: a planned transfer, when executed, is
an ordinary one-time transfer, and scheduling merely modifies P without touching balances. The
conservation invariant and its runtime assertion carry over unchanged—the operation grew, the
guarantee did not. Section 7 strengthens this into a proof over all reachable configurations.


6      A Runtime Coverage Model for the Invariant
Asserting the invariant is necessary but not sufficient: an invariant that is never observed to fail may
simply never have been exercised on the paths that could break it. We therefore distinguish never
violated from covered : coverage requires that all semantically relevant execution paths affecting the
invariant are exercised and checked. We did not design the coverage criterion ourselves. Prompted
only with the question of what should be checked to know the invariant is covered at runtime, the
AI proposed the model below; a subsequent AI-generated implementation then instrumented these
obligations and reported the coverage attained. Both prompts—the one that elicited the model and
the one that generated the checking code—appear in full in Appendix A; the first was, in essence:

    Human prompt (excerpt)
                         P
    Given the invariant [ ac∈AC B (ac) is constant], what should we check to determine that the invariant
    was covered at runtime?

The obligations the AI returned were:
 1. Pre/postPchecking. For every executed transfer (one-time or planned),
                                                                       P compute the total
    Sbefore = ac∈AC B (ac) immediately before the transfer and Safter = ac∈AC B (ac) immedi-
    ately after, and assert Sbefore = Safter .
 2. Both semantic cases. Exercise the success case (acs −f ⩾ 0) and the failure case (acs −f < 0)
    at least once for each transfer type.
 3. User and account diversity. Observe transfers across different users and distinct accounts,
    exercising ownership disjointness.
 4. Planned-transfer lifecycle. Observe insertion into P (no balance change), persistence across
    time steps, and execution when due, asserting Sbefore = Safter immediately before and after that
    execution.
 5. Multi-transfer stages. Include at least one stage with several transfers, checking the invari-
    ant after each.
The invariant is covered when all five obligations are met during execution.



                                                       6
Reviewing the coverage model. We do not take the AI’s proposal on trust. As with the
specification and the AI-proposed invariants, reviewing the proposed coverage model is itself part
of the discipline. On review we judged the model adequate: the five obligations together exercise
every path that could break conservation—both transfer outcomes (success and failure), ownership
diversity across users and accounts, the full planned-transfer lifecycle, and stages containing several
transfers—so no invariant-relevant behaviour is left unchecked. The AI-generated implementation
then instrumented these obligations and reported 100% coverage.
    This coverage model—AI-proposed, human-reviewed, then checked by AI-generated code—is
one of two methodological additions this paper makes beyond the predecessor’s runtime-assertion
approach; the other is the Z interface layer of Section 7, which the predecessor only touched on. The
generated implementation that performs the invariant check and attains full coverage is available
online (generated code).


7    Z Formalization of the Interfaces
We fix the interface layer in Z. The schemas in this section were generated by the AI : prompted to
rewrite the natural math specification so that the fund-transfer and scheduled-transfer interfaces
are made explicit in Z schema notation (leaving the rest of the specification untouched), the AI
produced the state and operation schemas below; we review and lightly edit them, exactly as we
review the specification, the proposed invariants, and the coverage model. In this study they were
generated after the code—a formalization pass that made the contracts precise and let us restate the
invariant as a property of the specification itself (Theorem 1). With hindsight we would generate
them before the code, as the method prescribes: fixing the contract first removes ambiguity earlier
and gives the generator a precise target.

Z as an internal representation, not a user-facing notation. We do not advocate Z as the
notation the user reads or writes. Its role here is internal : the schema mechanism decomposes
the specification into named interfaces with explicit inputs, invariants, and pre/postconditions,
which both sharpens ambiguity detection and—by splitting the problem into independent pieces—
mitigates the attention limits that degrade generation at scale. What the user sees can remain
the lightweight “natural language + mathematics” form: whenever an ambiguity surfaces, or an
interface itself needs to be presented, it can be rendered back into that readable form. Z works
behind the scenes; natural math stays the human-facing surface.
    Account balances are held in a state schema; the planned-transfer store is a second piece of
state; each operation is a schema with explicit pre/postconditions. We pair a success schema with
a Ξ (no-change) failure schema so that the insufficient-funds case is an explicit, reviewable contract
rather than an afterthought.

        AccountState
        balances : AC → N

A fixed ownership function assigns each account to its owning user:

        owner : AC → U


        PlannedTransferStore
        P : P(U × AC × U × AC × N1 × N)


                                                  7
        OneTimeTransfer
        ∆AccountState
        srcU , dstU : U ; srcAC , dstAC : AC ; f : N1
        owner srcAC = srcU
        owner dstAC = dstU
        balances srcAC ≥ f
        balances ′ = balances ⊕ {srcAC 7→ balances srcAC − f , dstAC 7→ balances dstAC + f }


        OneTimeTransferFail
        ΞAccountState
        srcU , dstU : U ; srcAC , dstAC : AC ; f : N1
        owner srcAC = srcU
        owner dstAC = dstU
        balances srcAC < f


        SchedulePlannedTransfer
        ∆PlannedTransferStore
        srcU , dstU : U ; srcAC , dstAC : AC ; f : N1 ; t? : N
        P ′ = P ∪ {(srcU , srcAC , dstU , dstAC , f , t?)}

A further schema ExecutePlannedTransfers(t) applies every planned transfer in P due at time t
(each an ordinary balance update) and removes it from P ; we omit its display for brevity.

An omission caught on review. The AI-generated schemas initially declared the users srcU , dstU
but never constrained them: nothing tied srcAC to srcU , so the contract permitted debiting an
account that its stated user does not own. The natural math specification requires the source
account to be owned by the source user (and likewise for the destination); we restored this as the
preconditions owner srcAC = srcU and owner dstAC = dstU above. The omission does not affect
conservation—money is conserved regardless of ownership, which is why the proof never exposed
it—but it does matter for a faithful interface contract. It is exactly the kind of gap that reviewing
the AI’s output, rather than trusting it, is meant to catch.

The invariant, over all reachable configurations. Let I be the inductive set of configurations
obtained from any legal initial configuration by finitely many applications of the four operation
schemas. The following claim is strictly stronger than Lemma 1: it is a property of the specification
itself, independent of any particular simulation or execution order.

Theorem 1 (Conservation over I ). For every configuration in I , ac∈AC balances(ac) is constant.
                                                                  P

Proof sketch. By induction on the construction of I . Base: the initial total is fixed. Step: One-
TimeTransfer changes two balances by −f and +f , preserving the sum; OneTimeTransferFail
and SchedulePlannedTransfer include ΞAccountState (or leave balances untouched), preserving the
sum; and ExecutePlannedTransfers is a finite composition of balance-preserving updates. Hence
the sum is invariant across I .


                                                    8
Letting the AI choose the interfaces. The schemas above were obtained by asking the AI
to translate the natural math specification into Z. As a stronger probe, we instead gave it only
the natural-language specification and asked it to decide the interface decomposition itself. It
performed well on substance—it identified the major interfaces unprompted (one-time transfer,
schedule, execute, and a time-advance operation), captured the ownership invariant (owner (ac1 ) =
owner (ac2 ) ⇒ ac1 = ac2 ), and expressed pre/postconditions as explicit contracts—but slipped
in ways a human must catch: it interleaved Z schemas with natural-language prose, leaked a
simulation-specific indexing detail into an interface, and quietly omitted parts of the specification
such as the initialization. The full AI-proposed interfaces, including these omissions, appear in
Appendix A. The AI can draft the interface surface; a human still curates what belongs in the
contract versus the simulation.


8      Results and Observations
Across both case studies, the code was never inspected line by line as it evolved; confidence came
from specification-level review, the conservation proof, the runtime coverage model, and the Z con-
tracts. We report the following observations, which the reader should treat as case-study evidence
rather than controlled measurements:
    • The same conservation invariant—and its proof—carried over unchanged from the one-time to
      the scheduled variant, even as the generated code grew substantially. The invariant is universal
      to the online-banking specification, not tied to any particular operation.
    • The conservation assertion held on every checked stage of every run we performed, as confirmed
      by inspecting the simulation output (viewable by following the links to the generated code).
    • The implementation appeared correct on first generation once the specification had been
      reviewed—“correct” here meaning that the logged simulation output, including the per-stage
      invariant assertion, showed the expected behaviour, again by inspection of the generated-code
      output rather than by reading the code.
    • On the positive side, the AI contributed correct lower-level invariants the author had not stated,
      and proposed usable Z interfaces from prose.
    • On the negative side, as specifications grew past a few pages the AI sometimes silently dropped
      tasks or sections—so abstraction, modularity, and decomposition still matter.


9      Discussion, Limitations, and Threats to Validity
The central gap: specification-level, not code-level, guarantees. The proofs (Lemma 1,
Theorem 1) and the runtime assertions establish properties of the specification and of observed
executions. They do not establish that the generated code refines the specification. That refinement
step is delegated to the AI and is not formally discharged here—unlike, e.g., mechanically verified
development [5]. Runtime assertions raise confidence but detect violations only on exercised paths
(hence the coverage model of Section 6), and coverage itself is argued informally rather than
measured by an independent tool.

Case study, not controlled experiment. This is a single-author case study in one domain.
The empirical observations in Section 8 are anecdotal and are flagged as such; there is no control
condition, no independent replication, and the same person authored the specification and judged


                                                    9
correctness. In particular, “correct on first generation” rests on inspection of the simulation out-
put by that same author, not on an independent oracle, so its construct validity is weak until a
measurement protocol is specified.

Tooling and reproducibility. Results depend on a specific commercial LLM assistant. The
work was carried out with ChatGPT used as an agent during the first quarter of 2026; the exact
underlying model version is not known to us, as it was not surfaced by the interface and may have
changed over the period. Re-running with a different model or at a different date may therefore
differ.

Generality. Conservation invariants are unusually well suited to this discipline. Whether the
approach extends as cleanly to properties without a conservation structure (e.g., liveness, security)
is open.


10    Conclusion and Future Work
We replicated a specification-first, AI-assisted discipline in a new domain and extended the method
with two additions—a runtime coverage model and a Z formalization proved over all reachable
configurations—while stress-testing it against a richer problem, scheduled/recurring transfers, which
the online-banking requirement calls for rather than the method. The recurrence of a single
conservation-invariant spine across two very different domains—knowledge and money—is pre-
liminary evidence that the discipline generalizes. The honest limit remains that confidence is
established at the specification level; closing the gap to the code (via refinement checking or ver-
ified generation) is the natural next step, along with controlled evaluation, additional domains,
and non-conservation properties. Two domain extensions we scoped but did not complete also
point the way: a recurring-solvency invariant—guaranteeing that an account holds sufficient funds
before a scheduled debit falls due, a liveness/scheduling property rather than a conservation one—
and support for multiple, heterogeneous transfer types within a single specification. Both would
test whether the discipline holds for properties and operation sets richer than the conservation
invariant studied here. Finally, although this study was carried out code-first with the Z interfaces
formalized afterward, our experience suggests authoring the Z contracts before generation—fixing
the interface first, then treating the code as regenerable output beneath it—and we adopt that
order as the recommended practice. We also stress that the Z layer was itself AI-generated and
is intended as an internal representation rather than a user-facing notation: its schema decom-
position sharpens ambiguity detection and helps generation scale, while the human-facing surface
stays the lightweight “natural language + mathematics” form, into which any surfaced ambiguity
or interface can be rendered back for review. Whether this internal-Z decomposition measurably
improves ambiguity detection and large-scale generation is a further question we leave open. More
broadly, we see the discipline itself—specification review, invariant proof, coverage, and internal-Z
decomposition—as a pattern that could be formalized as a reusable skill and then applied at scale:
instantiated across different AI agents and a range of use cases, and evaluated systematically rather
than through a single case study. Establishing such a skill, and measuring how it transfers across
agents and domains, is the direction we consider most promising.




                                                 10
Reproducibility and Artifacts
The paper is designed to be reproducible from the artifacts it carries. Appendix A reproduces
the original development document, including the full Human Prompt / AI Reply transcripts for
every step—the specification, the ambiguity resolutions, the invariant proof, the coverage model,
and the Z interfaces. It also retains the links to the AI-generated code (the one-time and scheduled
simulations and the coverage-checking implementation), reproduced inline in Sections 4, 5, and 6.
Together these let a reader repeat the process: re-issue the same prompts to reproduce the reported
results, or re-issue them—adapted—against a different domain or a different AI agent to test how
the discipline transfers.


Acknowledgments
This article was developed from the appendix material (the specifications, prompts, and AI re-
sponses) with the assistance of Anthropic’s Claude, used to structure and draft the manuscript.
This is distinct from the development work reported in the paper, which used ChatGPT as an
agent (Section 9). Responsibility for the correctness of the content lies entirely with the author.


References
[1] Jean-Raymond Abrial. The B-Book: Assigning Programs to Meanings. Cambridge University
    Press, 1996.

[2] Jacob Austin et al. Program synthesis with large language models.               arXiv preprint
    arXiv:2108.07732, 2021.

[3] Mark Chen et al. Evaluating large language models trained on code.              arXiv preprint
    arXiv:2107.03374, 2021.

[4] Cliff B. Jones. Systematic Software Development Using VDM. Prentice Hall, 2nd edition, 1990.

[5] K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Logic
    for Programming, Artificial Intelligence, and Reasoning (LPAR-16), 2010.

[6] Antonio Abu Nassar and Eitan Farchi. Enhancing formal software specification with artificial
    intelligence, 2026. arXiv:2601.09745.

[7] Adya Singh. Software requirements specification: Mobile banking application (instantpay).
    ResearchGate, https://www.researchgate.net/publication/375757633, 11 2023. Fund-
    transfer requirement 3.2.1.7 (functional requirement 1.7).

[8] J. M. Spivey. The Z Notation: A Reference Manual. Prentice Hall International, 2nd edition,
    1992.

[9] Jim Woodcock and Jim Davies. Using Z: Specification, Refinement, and Proof. Prentice Hall,
    1996.




                                                11
A      Original Development Document (lightly edited)
This appendix reproduces the original working document behind this paper, retained for reference.
The English has been lightly edited for readability; the technical content, the full Human Prompt
/ AI Reply transcripts, the alternative “trails” from natural math to Z, and all external links
(including the generated-code notebooks) are preserved as in the original.


A.1     The online bank
We will use the following online banking specification. See link. We consider the fund transfer requirement (3.2.1.7
Functional requirement 1.7). We start by a simple simulation of one time transfer. Next, we will add assertions and
then further develop the bank transfer to support additional types of transfer as required in 3.2.1.7 .

A.2     From natural math to proof to code
Here, the specification is written by the human in natural language augmented by mathematical notation and is
written in Latex. In addition, by reviewing the proof the confidence that the specification is clean increases. The
proof is possibly a mechanism of focusing the ambiguity feedback but that remains to be proven.

A.2.1 Fund transfer - one time transfer
Fund transfer - one time transfer
  Human Prompt
  Prompt: Generate a python program that implements the following

  We are given a set of users U = {u1 , . . . , un }. Each user has a set of accounts that belong to that user. In other
  words we have a set of accounts AC = {ac1 , . . . , ack } and a function AC (u) : U −→ P (AC ). Thus, for any
  users u ∈ U , AC (u) ⊆ AC is a subset of the accounts AC that belong to u.
  We assume that for any two users ui , uj ∈ U the intersection between AC (ui ) and AC (uj ) is empty. In addition,
    u∈U AC (u) = AC . Thus, an account belongs to one and only one user.
  S
  An account aci ∈ AC is a natural number (including zero). It represents the amount of money that the user
  that owns the account, i.e., the user u such that aci ∈ AC (u).
  The one time transfer is an interface that accepts a source user, ui ∈ U , an account aci ∈ AC (ui ), and a transfer
  amount f . It also accepts a target user uj ∈ U and an account acj ∈ AC (uj ).
  The one time transfer preforms the following operation. If aci − f ⩾ 0 then the interface updates aci to aci − f
  and acj to acj + f . Otherwise the interface does nothing.
  The simulation of one time transfer executes as follows.

      1. Randomly chose inputs for the one time transfer interface. In other words, randomly chose a source user,
         ui ∈ U , an account aci ∈ AC (ui ), and a transfer amount f . Also randomly chose a target user uj ∈ U
         and an account acj ∈ AC (uj ).
      2. Perform the transfer operation
      3. Report the input that was chosen to the transfer operation and the result of the transfer operation.
  Simulation initialization
  Choose the number of users to be three and the number of accounts to be 6. Have user one own accounts 1 and
  2, user two own account 3 and 4 and user 3 own account 5 and 6. Choose the amount of money in each account
  randomly.


Generate code Generated using ChatGPT. See generated code here link. Inspecting the execution log of
the simulation indicates that the simulation is correct but we would like to increase our confidence level in the
implementation by introducing assertions. The code is 106 LOC long.

Assertion - the overall money in the system is constant




                                                           12
  Human Prompt
                                         P
  Lemma 2. The amount of money             aci ∈AC aci   remains constant after each fun transfer.

  Provide a proof that lemma 10 is correct


    Using ChatGPT I obtained the following proof of the assertion. Reviewing it I found the proof correct.

  AI Reply
  Generated proof
  Setup and assumptions. Let AC = {ac1 , . . . , ack } be the multiset of account balances (we identify
  an account by its current numeric balance). Assume every account balance and every transfer amount is a
  real number (or integer) ⩾ 0. In particular we assume the transfer amount f satisfies f ⩾ 0. The one-time
  transfer interface selects a source account acs and a target account act (possibly belonging to different users)
  and attempts to move f units from acs to act . The interface updates balances only when acs − f ⩾ 0; otherwise
  it leaves all balances unchanged.               X
  Lemma 3. The total amount of money T =              ac is invariant under the one-time transfer operation: after
                                                   ac∈AC
  any transfer (successful or aborted) the new total T ′ equals T .

  Proof. Let the accounts before the transfer be AC = {ac1 , . . . , ack } and denote the chosen source and target
  accounts by acs and act respectively. Write the total before the transfer as
              P               P                       
         T =     ac∈AC ac =       ac∈AC \{acs ,act } ac + acs + act .


  We consider two cases.
  Case 1 — transfer aborts: If acs − f < 0, the interface does nothing. Hence every account balance remains
  the same and the total after the operation is T ′ = T .
  Case 2 — transfer succeeds: If acs − f ⩾ 0, the interface updates the two chosen accounts to

         acs′ = acs − f ,     act′ = act + f ,

  and leaves every other account unchanged. The total after the transfer is
                P                                         P                      
         T′ =       ac∈AC \{acs ,act } ac   + ac ′
                                                 s + ac ′
                                                        t =   ac∈AC \{acs ,act } ac   + (acs − f ) + (act + f ).

  The −f and +f cancel, so
             P                       
       T′ =      ac∈AC \{acs ,act } ac + acs + act = T .


  In both cases T ′ = T . Therefore the total amount of money in the system is preserved by every one-time
  transfer operation.

    TBC - add recurring transfers, and scheduled transfers
    TBC - add assertions that the some of money in the system is constant
    TBC - add assertion that recurring transfer should add money to an account before an upcoming recurring
reduction in the account.

A.2.2     Fund transfer - schedule transfer
Next, I updated the specification to include a transfer at time t and a recurring transfer every k unit of times.

  Human Prompt
  Prompt: Generate a python program that implements the following

  We are given a set of users U = {u1 , . . . , un }. Each user has a set of accounts that belong to that user. In other
  words we have a set of accounts AC = {ac1 , . . . , ack } and a function AC (u) : U −→ P (AC ). Thus, for any
  users u ∈ U , AC (u) ⊆ AC is a subset of the accounts AC that belong to u.




                                                             13
  We assume that for any two users ui , uj ∈ U the intersection between AC (ui ) and AC (uj ) is empty. In addition,
    u∈U AC (u) = AC . Thus, an account belongs to one and only one user.
  S
  An account aci ∈ AC is a natural number (including zero). It represents the amount of money that the user
  that owns the account, i.e., the user u such that aci ∈ AC (u).
  Fund transfer are a function of the current time. The current time is a natural number initialized to 0 at the
  beginning of the simulation. At each stage of the simulation the current time is first incremented by one.

  Fund transfer operations - schedule transfer The one time transfer is an interface that
  accepts a source user, ui ∈ U , an account aci ∈ AC (ui ), and a transfer amount f . It also accepts a target user
  uj ∈ U and an account acj ∈ AC (uj ).
  The one time transfer preforms the following operation. If aci − f ⩾ 0 then the interface updates aci to aci − f
  and acj to acj + f . Otherwise the interface does nothing.
  Planed transfer is a one time transfer scheduled to occur at time t. See simulation steps below for details

  Simulation The simulation of fund transfer consists of stages. In each stage the following steps are taken.
     1. Increment current time, t, by 1.
     2. One time transfer. Randomly chose inputs for the one time transfer interface. In other words, randomly
        chose a source user, ui ∈ U , an account aci ∈ AC (ui ), and a transfer amount f . Also randomly chose
        a target user uj ∈ U and an account acj ∈ AC (uj ). Thus, a one time transfer is defined by the vector
        (ui , aci , uj , acj , f ).
          (a) Perform the transfer operation (ui , aci , uj , acj , f ).
     3. Schedule a planned transfer. Randomly chose inputs for a one time transfer interface. In other words,
        randomly chose a source user, ui ∈ U , an account aci ∈ AC (ui ), and a transfer amount f . Also randomly
                                                                                                         ′
        chose a target user uj ∈ U and an account acj ∈ AC (uj ). Randomly choose some time t that is greater
                                                                              ′
        than the current time. Add the vector p = (ui , aci , uj , acj , f , t ) in the planned transfer set P .
                                                                              ′′                ′′
     4. Perform a planned transfer. For any p = (ui , aci , uj , acj , f , t ) ∈ P such that t = t the current time
                                                                                                            ′′
        perform the one time transfer (ui , aci , uj , acj , f ) and remove p = (ui , aci , uj , acj , f , t ) from P .
     5. Report the input that was chosen for each of the transfer operations and the result of each transfer
        operation performed in this stage. Identify which type of transfer was preformed (planned or one time).
        Highlight the current time of each transfer operation performed in this stage, t. Report the state of the
        planned transfer set P at that stage before the planned transfer operations were performed.
  Simulation initialization
  Choose the number of users to be three and the number of accounts to be 6. Have user one own accounts 1
  and 2, user two own account 3 and 4 and user 3 own account 5 and 6. Choose the amount of money in each
  account randomly. Current time is initialized to 0. Initialize the planned fund transfer set P to the empty set.
  An element in P is of type U × AC × U × AC × N + × N . N + stand for the natural numbers without zero and
  N stand for the natural numbers with 0.

Generated code Using ChatGPT I generated Python code see link. The code is 265 LOC and seems to be
executing fine based on inspection of the simulation. Next we also generate the assertions based on the lemma above
to increase our confidence in the implementation. But before we do that let us check that the assertion still holds.

Assertion - the overall money in the system is constant I gave the updated design definition to
ChatGPT in a new session and asked for the proof of the lemma below. The proof is essentially the same. The only
difference is the observation that periodic fund transfer translates to regular transfer - see proof below.

  Human Prompt
                                         P
  Lemma 4. The amount of money             aci ∈AC aci   remains constant after each fun transfer.

  Provide a proof that lemma 10 is correct



    Generated proof


                                                              14
  AI Reply
                                     P
  Lemma 5. The amount of money aci ∈AC aci remains constant after each fund transfer.

  Proof. Let S = ac∈AC ac denote the total amount of money before a transfer.
                 P
  Consider a one-time transfer with input (us , acs , ut , act , f ), where acs is the source account and act the target
  account.
  Case 1: acs − f ⩾ 0. The transfer is executed, yielding

         acs′ = acs − f ,    act′ = act + f .

  All other accounts remain unchanged. The new total is
                            P                       
         S ′ = ac∈AC ac ′ =
              P
                                ac∈AC \{acs ,act } ac + (acs − f ) + (act + f ).


  Rearranging gives

        S ′ = ac∈AC ac = S .
             P

  Case 2: acs − f < 0. No transfer occurs, so no balances change and S ′ = S .
  Thus every one-time transfer preserves the total amount of money.
  A planned transfer is executed exactly as a one-time transfer at its scheduled time, so it also preserves the total.
  Adding a planned transfer to the set P or advancing the simulation time does not modify any account values.
  Since every transfer preserves the total, and a simulation stage may contain several such transfers, the total also
  remains unchanged after any stage.
  Therefore,

           ac∈AC ac is invariant under the simulation.
         P




A.3     Invariant coverage
Next, in order to increase the confidence level that the implementation is correct I’ll attempt to define a coverage
model of the invariant 10 and obtain runtime feedback of the level of coverage the invariant has at simulation time.

A.3.1     Obtain a coverage model for the invariant
  Human Prompt
  Given the invariant 10 what should we check to determine that the invariant was coveraged at runtime?

    Here is the reply I got from ChatGPT.

  AI Reply
  Runtime Coverage Model for the Invariant
  Invariant.
           ac∈AC ac = constant
         P

  The invariant states that the total amount of money across all accounts must remain unchanged after every
  fund transfer operation.
  Meaning of Coverage Invariant coverage at runtime means more than observing that the invariant is
  never violated. It requires that all semantically relevant execution paths that could affect the invariant are
  exercised and checked during execution.
  Coverage Obligations The invariant is considered covered if all of the following runtime conditions are
  satisfied.
  1. Pre- and Post-Transfer Checking For every executed transfer operation (one-time or planned),
  the system computes

          Sbefore = ac∈AC ac and Safter = ac∈AC ac
                   P                         P




                                                           15
  and verifies that

          Sbefore = Safter .

  This check must be performed for both one-time transfers and planned transfers.
  2. Semantic Case Coverage of Transfer Execution Each transfer operation has two semantic
  cases, both of which must be exercised.
      • Successful transfer: acs − f ⩾ 0, where balances are updated.
       • Failed transfer: acs − f < 0, where no balances change.

  Runtime coverage requires that both cases occur at least once for one-time transfers and at least once for planned
  transfers.

  3.   User and Account Diversity Transfers must be observed across different users and distinct
  accounts, including cases where the source user and target user are different. This ensures that the disjointness
  of account ownership is exercised at runtime.

  4. Planned Transfer Lifecycle Coverage Planned transfers must be observed through all phases
  of their lifecycle:
       1. Insertion into the planned transfer set P , without modifying account balances.
       2. Persistence in P across multiple time steps.
       3. Execution at the scheduled time, with invariant checking before and after execution.

  5. Multi-Transfer Stage Coverage At least one simulation stage must include multiple transfer
  operations (e.g., a one-time transfer and one or more planned transfers). The invariant must be checked and
  preserved after each individual transfer in the stage.

  Coverage Criterion The invariant               ac∈AC ac is considered covered at runtime if all of the above con-
                                               P
  ditions are satisfied during the execution of the simulation.


A.3.2      Code generation
  Human Prompt
  Generate the python code that is specified above. Inlcude a check of the invariance 10 after each stage of the
  simulation. Check the coverage detailed above and report the increase in coverage after each stage and what
  new condition was covered. At the end of the simulation report the percentage of coverage that was achieved.

    Generated code executed nicely and achieved 100% coverage. See code here link.

A.4      From natural to natural math to proof to code
Can the business rule be specified in natural language and translated to the natural math intermediate representation
and use the claim and proof flow to increase the confidence that the specification is clean?

A.4.1      Fund transfer - one time transfer - using a natural to natural math to proof
           to code flow
First we create a natural language description of the specification and verify that it describes the one time transfer
requirement in natural language with minimal or no use of mathematical notation.

  Human Prompt
  Prompt: Generate a natural language description of the following specification keeping mathe-
  matical notation to a minium. Generate the specification as a latex section.

  We are given a set of users U = {u1 , . . . , un }. Each user has a set of accounts that belong to that user. In other
  words we have a set of accounts AC = {ac1 , . . . , ack } and a function AC (u) : U −→ P (AC ). Thus, for any



                                                           16
  users u ∈ U , AC (u) ⊆ AC is a subset of the accounts AC that belong to u.
  We assume that for any two users ui , uj ∈ U the intersection between AC (ui ) and AC (uj ) is empty. In addition,
    u∈U AC (u) = AC . Thus, an account belongs to one and only one user.
  S
  An account aci ∈ AC is a natural number (including zero). It represents the amount of money that the user
  that owns the account, i.e., the user u such that aci ∈ AC (u).
  The one time transfer is an interface that accepts a source user, ui ∈ U , an account aci ∈ AC (ui ), and a transfer
  amount f . It also accepts a target user uj ∈ U and an account acj ∈ AC (uj ).
  The one time transfer preforms the following operation. If aci − f ⩾ 0 then the interface updates aci to aci − f
  and acj to acj + f . Otherwise the interface does nothing.
  The simulation of one time transfer executes as follows.
      1. Randomly chose inputs for the one time transfer interface. In other words, randomly chose a source user,
         ui ∈ U , an account aci ∈ AC (ui ), and a transfer amount f . Also randomly chose a target user uj ∈ U
         and an account acj ∈ AC (uj ).
      2. Perform the transfer operation
      3. Report the input that was chosen to the transfer operation and the result of the transfer operation.

  Simulation initialization
  Choose the number of users to be three and the number of accounts to be 6. Have user one own accounts 1 and
  2, user two own account 3 and 4 and user 3 own account 5 and 6. Choose the amount of money in each account
  randomly.

  AI Reply
  This section provides an intuitive description of the system with minimal mathematical notation.
  We consider a collection of users, each of whom owns a personal set of accounts. Every account belongs to
  exactly one user, and no account is shared among different users. Taken together, all accounts in the system are
  distributed across all users without overlap.
  Each account stores a non-negative whole number representing the amount of money currently held in that
  account.
  The system provides a one-time transfer operation. This operation takes as input:
      • a source user and one of their accounts,
      • a transfer amount,
      • a target user and one of their accounts.
  The operation checks whether the source account contains enough money to cover the transfer amount. If it
  does, the specified amount is deducted from the source account and added to the target account. If the source
  account does not have sufficient funds, the system makes no changes.
  A simulation of this one-time transfer proceeds in three steps:
      1. The system randomly selects a source user, one of that user’s accounts, and a transfer amount. It also
         randomly selects a target user and one of that user’s accounts.
      2. The transfer operation is executed using these randomly chosen inputs.
      3. The system outputs both the chosen inputs and the result of the transfer attempt.

  Simulation Initialization For the simulation, we set up three users and six accounts. User 1 owns
  accounts 1 and 2, User 2 owns accounts 3 and 4, and User 3 owns accounts 5 and 6. Each account is assigned
  an initial amount of money chosen at random.

    I verified the natural language above and it captures the intent for a single transfer. Next, I attempt to generate
the natural math specification of the single transfer specification so that we can then obtain a proof of its correctness.
This was done in a fresh chat.

  Human Prompt
  Generate a mathematical oriented precise description using latex notation of the following specification so that
  ambiguities are removed.
  This section provides an intuitive description of the system with minimal mathematical notation.
  We consider a collection of users, each of whom owns a personal set of accounts. Every account belongs to



                                                           17
  exactly one user, and no account is shared among different users. Taken together, all accounts in the system are
  distributed across all users without overlap.
  Each account stores a non-negative whole number representing the amount of money currently held in that
  account.
  The system provides a one-time transfer operation. This operation takes as input:
      • a source user and one of their accounts,
      • a transfer amount,
      • a target user and one of their accounts.
  The operation checks whether the source account contains enough money to cover the transfer amount. If it
  does, the specified amount is deducted from the source account and added to the target account. If the source
  account does not have sufficient funds, the system makes no changes.
  A simulation of this one-time transfer proceeds in three steps:
     1. The system randomly selects a source user, one of that user’s accounts, and a transfer amount. It also
        randomly selects a target user and one of that user’s accounts.
     2. The transfer operation is executed using these randomly chosen inputs.
     3. The system outputs both the chosen inputs and the result of the transfer attempt.

  Simulation Initialization For the simulation, we set up three users and six accounts. User 1 owns
  accounts 1 and 2, User 2 owns accounts 3 and 4, and User 3 owns accounts 5 and 6. Each account is assigned
  an initial amount of money chosen at random.

     The AI reply below is interesting. Specifically, the natural math description below is different than the one I
original wrote.

  AI Reply
  System Entities. Let
          U = {u1 , u2 , u3 }
  be the set of users, and let
          AC = {ac1 , ac2 , ac3 , ac4 , ac5 , ac6 }
  be the set of accounts. Each account belongs to exactly one user. We formalise ownership through a function
          owner : AC → U .
  For the simulation initialization we define:
          owner(ac1 ) = owner(ac2 ) = u1 ,            owner(ac3 ) = owner(ac4 ) = u2 ,    owner(ac5 ) = owner(ac6 ) = u3 .
  Each account stores a non-negative integer balance. Define the balance function
          bal : AC → N0 .
  One-Time Transfer Operation. A transfer input is a tuple
          (s, as , m, t, at )
  where
          s, t ∈ U ,        as , at ∈ AC ,     owner(as ) = s, owner(at ) = t,       m ∈ N0 .
  The transfer operation is the partial function
          T : U × AC × N0 × U × AC −→ AC → N0 ,
  which transforms the balance function as follows. Given state bal and input (s, as , m, t, at ),
                                     
                                     bal′ if bal(as ) ⩾ m,
        T (bal; s, as , m, t, at ) =
                                     bal otherwise,



                                                                 18
  where bal′ is defined pointwise by:
                    
                    
                     bal(x ) − m if x = as ,
                    
           ′
        bal (x ) = bal(x ) + m if x = at ,
                    
                                  otherwise.
                    
                      bal(x )
                    

  Thus, the transfer succeeds iff the source account contains at least m units of money.
  Randomised Simulation Step. A single simulation step consists of selecting inputs uniformly at
  random and executing the transfer. Formally, the system samples:

         s ∼ U,         as ∼ { a ∈ AC : owner(a) = s },

         t ∼ U,         at ∼ { a ∈ AC : owner(a) = t },

  and a transfer amount

         m ∼ M,

  where M ⊆ N0 is a predefined finite set of admissible transfer amounts.
  Given the sampled inputs, the system computes

         balnew := T (bal; s, as , m, t, at ).

  The output of the simulation step is the tuple

         (s, as , m, t, at , balnew ).

  Simulation Initialization. Initially, each account aci is assigned a balance
         bal(aci ) ∼ D,

  where D is a specified distribution on N0 (e.g., uniform over a fixed finite range).
  Thus the initial state is completely determined by the random vector

         (bal(ac1 ), . . . , bal(ac6 )).

    There are several problems with the generation above. There are latex errors. In addition, the specification is
not stated in general but for a specific configuration. The relation correctness is still described in english and not
mathematically, e.g., the function is one on one. It is assumed that every account has a positive amount of money
which is not correct (it could be zero). In addition the transfer can be zero and that is not correct. Below I try to
improve the prompt ina new session.

  Human Prompt
  Generate a mathematical oriented precise description using latex notation of the following spec-
  ification so that ambiguities are removed. Clearly distinguish between the specific configuration
  that apply to the simulation and the general specification that has arbitrary but finite number of
  users and accounts.
  This section provides an intuitive description of the system with minimal mathematical notation.
  We consider a collection of users, each of whom owns a personal set of accounts. Every account belongs to
  exactly one user, and no account is shared among different users. Taken together, all accounts in the system are
  distributed across all users without overlap.
  Each account stores a non-negative whole number representing the amount of money currently held in that
  account.
  The system provides a one-time transfer operation. This operation takes as input:
      • a source user and one of their accounts,
      • a transfer amount,
      • a target user and one of their accounts.
  The operation checks whether the source account contains enough money to cover the transfer amount. If it
  does, the specified amount is deducted from the source account and added to the target account. If the source



                                                          19
  account does not have sufficient funds, the system makes no changes.
  A simulation of this one-time transfer proceeds in three steps:
     1. The system randomly selects a source user, one of that user’s accounts, and a transfer amount. It also
        randomly selects a target user and one of that user’s accounts.
     2. The transfer operation is executed using these randomly chosen inputs.
     3. The system outputs both the chosen inputs and the result of the transfer attempt.

  Simulation Initialization For the simulation, we set up three users and six accounts. User 1 owns
  accounts 1 and 2, User 2 owns accounts 3 and 4, and User 3 owns accounts 5 and 6. Each account is assigned
  an initial amount of money chosen at random.

    Here is what I got with the new prompt above from the AI (using ChatGPT). (Interestingly I had to insist that
the rendering will be in Latex.)

  AI Reply
  General Mathematical Specification
  Users and Accounts Let U be a finite, nonempty set of users:
          U = {u1 , . . . , un }.

  Let AC be a finite, nonempty set of accounts:

          AC = {ac1 , . . . , ack }.

  Each account belongs to exactly one user. Ownership is represented by a total function

          owner : AC → U .

  For each user u ∈ U , the set of accounts owned by u is

          AC (u) = { ac ∈ AC | owner(ac) = u }.

  These sets form a partition of AC :
                U
        AC = u∈U AC (u).

  Account Balances Each account holds a non-negative integer balance:
          bal : AC → N.

  One-Time Transfer Operation A transfer attempt is a 4-tuple
          (s, as , m, at )

  where
      • s ∈ U is the source user,
      • as ∈ AC (s) is the source account,
      • m ∈ N is the transfer amount,
      • at ∈ AC (t) is a target account for some t ∈ U .
  The transfer operation updates the balance function according to:

                                   bal′ (as ) = bal(as ) − m,
               
               
               
               if bal(a ) ⩾ m : bal′ (a ) = bal(a ) + m,
               
                         s                t          t
        bal′ =                        ′
               
               
                                  bal (ac) = bal(ac) for all ac ∈
                                                                 / {as , at },
                 if bal(as ) < m : bal′ = bal.
               




                                                           20
  Simulation-Specific Configuration
  For the simulation, instantiate the general specification with:

         Usim = {u1 , u2 , u3 },      ACsim = {ac1 , ac2 , ac3 , ac4 , ac5 , ac6 }.

  The ownership relation is fixed as:

         AC (u1 ) = {ac1 , ac2 },     AC (u2 ) = {ac3 , ac4 },    AC (u3 ) = {ac5 , ac6 }.

  Initial account balances are chosen randomly:

         bal(aci ) ∈ N        for each aci ∈ ACsim .

  Simulation Procedure A single simulation step consists of:
      1. Randomly select:

                 s ∈ Usim ,    as ∈ AC (s),      m ∈ N,      t ∈ Usim ,    at ∈ AC (t).

      2. Execute the transfer operation on these inputs.
      3. Output both the selected inputs and the resulting balance function bal′ .

   It worked. In order for it to work I had to ask to distinguish the specific simulation from the general specification.
Next, we want to determine if we can get a proof from the generated natural math description.

Assertion - the overall money in the system is constant
  Human Prompt
                                           P
  Lemma 6. The amount of money                aci ∈AC aci   remains constant after each fun transfer.

  Provide a proof that lemma 10 is correct


    Generated proof.

  AI Reply
  We provide a formal proof of Lemma 10 based on the definitions given in the general specification.

  Proof. Let bal : AC → N be the current balance function, and consider a one-time transfer

         (s, as , m, at )

  as defined in the specification. There are two cases:
  Case 1: Transfer is allowed (bal(as ) ⩾ m)
  By definition, the updated balance function bal′ satisfies:

         bal′ (as ) = bal(as ) − m,        bal′ (at ) = bal(at ) + m,        bal′ (ac) = bal(ac) for all ac ∈
                                                                                                            / {as , at }.

  The total money in the system after the transfer is
        P           ′       P                 ′          ′           ′        P
           ac∈AC bal (ac) =      / s ,at } bal (ac) + bal (as ) + bal (at ) =
                              ac ∈{a                                              / s ,at } bal(ac) + (bal(as ) − m) + (bal(at ) + m).
                                                                               ac ∈{a

  Simplifying,
         P           ′       P                                             P
            ac∈AC bal (ac) =     / s ,at } bal(ac) + bal(as ) + bal(at ) =
                              ac ∈{a                                        ac∈AC bal(ac).

  Hence, the total money remains constant in this case.
  Case 2: Transfer is not allowed (bal(as ) < m)
  By definition, the balance function does not change:

         bal′ = bal.




                                                                  21
  Therefore,
        P            ′       P
            ac∈AC bal (ac) =  ac∈AC bal(ac),

  so the total money remains constant.
  Conclusion:
  In both possible cases, the total sum of all account balances does not change. Therefore, Lemma 10 is correct:
                     ′
                                                 ∀ one-time transfers.
        P                    P
           ac∈AC bal (ac) =     ac∈AC bal(ac)




    I reviewed the proof and it looks fine.

A.4.2     Natural to natural math to proof when the natural specification is not com-
          plete
Next, I injected an error in the specification. I would like to determine if the AI will spot it. Specifically, I remove
the check that there is enough money in the account to transfer.

  Human Prompt
  Generate a mathematical oriented precise description using latex notation of the following spec-
  ification so that ambiguities are removed. Clearly distinguish between the specific configuration
  that apply to the simulation and the general specification that has arbitrary but finite number of
  users and accounts.
  This section provides an intuitive description of the system with minimal mathematical notation.
  We consider a collection of users, each of whom owns a personal set of accounts. Every account belongs to
  exactly one user, and no account is shared among different users. Taken together, all accounts in the system are
  distributed across all users without overlap.
  Each account stores a non-negative whole number representing the amount of money currently held in that
  account.
  The system provides a one-time transfer operation. This operation takes as input:
      • a source user and one of their accounts,
      • a transfer amount,
      • a target user and one of their accounts.
  The specified amount is deducted from the source account and added to the target account.
  A simulation of this one-time transfer proceeds in three steps:
      1. The system randomly selects a source user, one of that user’s accounts, and a transfer amount. It also
         randomly selects a target user and one of that user’s accounts.
      2. The transfer operation is executed using these randomly chosen inputs.
      3. The system outputs both the chosen inputs and the result of the transfer attempt.

  Simulation Initialization For the simulation, we set up three users and six accounts. User 1 owns
  accounts 1 and 2, User 2 owns accounts 3 and 4, and User 3 owns accounts 5 and 6. Each account is assigned
  an initial amount of money chosen at random.

    The AI (ChatGPT) generated the following natural math specification.

  AI Reply
  Mathematical Specification of the System
  General Specification

  Users and Accounts. Let U be a finite, nonempty set of users,
         U = {u1 , u2 , . . . , un },




                                                          22
 and let AC be a finite, nonempty set of accounts,

       AC = {a1 , a2 , . . . , am }.

 Ownership Function. We define a total function
       owner : AC → U ,

 where for each account a ∈ AC , the value owner(a) is the unique user who owns a. Thus, every account belongs
 to exactly one user, and no account is shared among different users.

 Balances. A system state is a function
       B : AC → N.

 Transfer Operation. A one-time transfer is a tuple
       (srcU , srcA, amt, tgtU , tgtA)

 such that

       owner(srcA) = srcU ,             owner(tgtA) = tgtU ,             amt ∈ N.

 The resulting state B ′ after executing the transfer on state B is
                
                
                
                 B (a) − amt if a = srcA,
                
         ′
       B (a) = B (a) + amt if a = tgtA,
                
                
                                  otherwise.
                
                B (a)


 Specific Simulation Configuration The simulation uses
       U = {u1 , u2 , u3 },       AC = {a1 , a2 , a3 , a4 , a5 , a6 }.

 The ownership function is explicitly defined by

       owner(a1 ) = u1 ,      owner(a2 ) = u1 ,

       owner(a3 ) = u2 ,      owner(a4 ) = u2 ,

       owner(a5 ) = u3 ,      owner(a6 ) = u3 .

 Initial balances are chosen randomly:

       B (ai ) ∈ N    for i = 1, . . . , 6.


Assertion - the overall money in the system is constant
 Human Prompt
                                              P
 Lemma 7. The amount of money                 aci ∈AC aci   remains constant after each fun transfer.

 Provide a proof that lemma 10 is correct or highlight why it is not.


   Following is the generated AI response that highlighted the ambiguity I intentionally injected.

 AI Reply
 Analysis of Problems and Ambiguities Before proving Lemma 10, we list the issues and ambigu-
 ities that must be resolved in order for the statement to be mathematically valid.




                                                                   23
     1. Incorrect summation notation. The expression
              P
                aci ∈AC aci

         is not meaningful: the summand should be the balance of account aci , i.e. B (aci ), not the account
         identifier itself.
     2. Unclear reference to “fun transfer”. The intended operation is the formally defined one-time transfer.
        We assume that it is the operation described earlier, producing a new state B ′ .
     3. Missing assumption about transfer execution. The specification does not say whether a transfer
        is allowed even when B (srcA) < amt, i.e. if balances may become negative. The proof below works for
        either case, because it only uses algebraic cancellation −amt + amt = 0.
     4. Missing distinction between general state and simulation state. The lemma must be stated for
        arbitrary AC and arbitrary states B , not only for the fixed six-account simulation.
     5. Incorrect type of the transferred quantity. The lemma refers to “amount of money”, but mathe-
        matically this means the sum of the values of the balance function B .

  These issues are corrected in the formal lemma and proof below.

  Lemma: Conservation of Total Money
  Lemma 8 (Conservation of total money). Let B : AC → Z be the balance function before a one-time transfer
  (srcU , srcA, amt, tgtU , tgtA), and let B ′ be the updated balance function obtained using the transfer semantics
                  
                  
                    B (a) − amt if a = srcA,
                  
            ′
          B (a) = B (a) + amt if a = tgtA,
                  
                  
                     B (a)           otherwise.
                  

  Then the total amount of money in the system is preserved:
        P         ′      P
          a∈AC B (a) =     a∈AC B (a).

  Proof. We compute the sum after the transfer using the definition of B ′ :
                ′
         P             P                                                    
          a∈AC B (a) =     a∈AC     B (a) + B (srcA) − amt + B (tgtA) + amt .
                            a̸=srcA,tgtA

  Rearrange the right-hand side:
        P         ′      P                          P
          a∈AC B (a) =     a∈AC B (a) − amt + amt =  a∈AC B (a).

  Thus the total money is unchanged by the transfer.

  Remark. The proof does not rely on the assumption that B (srcA) ⩾ amt. If your system disallows transfers
  that would make a balance negative, then rejected transfers satisfy B ′ = B , and the lemma still holds. If later
  the system includes fees, taxes, or creation/destruction of funds, this lemma must be modified accordingly.


A.4.3     From natural math to the Z formal specification notation
  To overcome attention issues when generating code from a specification, we introduce interfaces automatically.
Interface decomposition separates the specification into well-defined interaction boundaries, reducing cognitive load
and enabling local reasoning. This relationship is illustrated in Diagram 3.

                                                                Interface
                                     Attention
                                                              Decomposition

                Figure 3: Relationship between attention and interface decomposition




                                                         24
  We attempt to translate the natural language specification to another intermediate representation which we name
natural Z Schema. We explore the use of the Natural Logic Z Schema representation to overcome attention issues
in AI systems through decomposition into interfaces using the Z schema mechanism (see 4). This representation
preserves as much natural language as possible to enhance readability, while using the Z schema construct to define
interfaces, invariants, and associated proofs.

                  Natural                              Natural
                                                                                              Code
                 Language                               Logic




                                                   Natural Logic                            Proofs
                                                    Z Schema                             & Invariants

         Figure 4: Separation of code generation parts of the specification using Z Schema


  Human Prompt
  The Z formal specification notation has the notion of schema. A Z schema denotes a set of states or state
  transitions constrained by logic; at the code level it corresponds to a typed interface with invariants and operation
  contracts.
  Generate a mathematical oriented precise description using latex notation of the following spec-
  ification so that ambiguities are removed. Clearly distinguish between the specific configuration
  that apply to the simulation and the general specification that has arbitrary but finite number of
  users and accounts. Use the Z schema notation to explicitly distinguish interfaces that transfer
  funds and store and retrieve fund scheduled fund transfers or any other interfaces that you decide
  you need to define.
  This section provides an intuitive description of the system with minimal mathematical notation.
  We consider a collection of users, each of whom owns a personal set of accounts. Every account belongs to
  exactly one user, and no account is shared among different users. Taken together, all accounts in the system are
  distributed across all users without overlap.
  Each account stores a non-negative whole number representing the amount of money currently held in that
  account.
  The system provides a one-time transfer operation. This operation takes as input:
      • a source user and one of their accounts,
      • a transfer amount,
      • a target user and one of their accounts.
  The operation checks whether the source account contains enough money to cover the transfer amount. If it
  does, the specified amount is deducted from the source account and added to the target account. If the source
  account does not have sufficient funds, the system makes no changes.
  A simulation of this one-time transfer proceeds in three steps:
     1. The system randomly selects a source user, one of that user’s accounts, and a transfer amount. It also
        randomly selects a target user and one of that user’s accounts.
     2. The transfer operation is executed using these randomly chosen inputs.
     3. The system outputs both the chosen inputs and the result of the transfer attempt.

  Simulation Initialization For the simulation, we set up three users and six accounts. User 1 owns
  accounts 1 and 2, User 2 owns accounts 3 and 4, and User 3 owns accounts 5 and 6. Each account is assigned
  an initial amount of money chosen at random.




                                                           25
AI Reply
Z-Style Formal Specification with Explicit Environment We model the system using Z-style
schemas encoded in standard mathematical notation. Let USER and ACCOUNT be given finite sets, and let
        Money ≜ N.
General system state. Account ownership and balances are defined as follows:
                      
                         owns : USER ⇀ P(ACCOUNT )
         Ownership ≜
                      ∀ u1 , u2 ∈ USER, u1 ̸= u2 ⇒ owns(u1 ) ∩ owns(u2 ) = ∅
                       balance : ACCOUNT   ⇀ Money
         Balances ≜                   S
                       dom(balance) = ran(owns)
         SystemState ≜ Ownership ∧ Balances
Environment. The environment nondeterministically selects transfer parameters but does not change the
system state:
                       
                        srcUser ?, dstUser ? ∈ USER
         Environment ≜   srcAcc?, dstAcc? ∈ ACCOUNT
                         amount? ∈ Money
                       

One-time transfer interface. The system reacts to the environment inputs. If sufficient funds exist,
balances are updated; otherwise, the state is unchanged.
                                                            ′
                             
                              SystemState, SystemState , Environment
                             
                                 srcAcc?   ∈ owns(srcUser  ?)
                             
                             
                             
                             
                                 dstAcc? ∈ owns(dstUser ?)
                             
        OneTimeTransfer ≜
                                amount? ⩽ balance(srcAcc?)
                                 balance ′ = balance ⊕ {srcAcc? 7→ balance(srcAcc?) − amount?,
                             
                             
                             
                             
                             
                                            dstAcc? 7→ balance(dstAcc?) + amount?}
                             


                        SystemState, SystemState ′ , Environment
                      
                      
                                   ′
                      
                       SystemState = SystemState
                      
                      
         NoTransfer ≜   srcAcc? ∈ owns(srcUser ?)
                        dstAcc? ∈ owns(dstUser ?)
                      
                      
                      
                      
                        amount? > balance(srcAcc?)
                      


        Transfer ≜ OneTimeTransfer ∨ NoTransfer
Observation interface. The simulation observes the selected inputs and whether the transfer succeeded.
                          
                           srcUser , dstUser ∈ USER
                          
                            srcAcc, dstAcc ∈ ACCOUNT
                          
         TransferRecord ≜
                           amount ∈ Money
                          
                            success ∈ B
                          


                            SystemState, SystemState ′ , Environment, record !
                          
                          
                          
                          
                          
                          
                           Transfer
                            record !.srcUser = srcUser ?
                          
                          
                          
                          
                            record !.srcAcc = srcAcc?
                          
         SimulationStep ≜
                          
                           record !.dstUser = dstUser ?
                           record !.dstAcc = dstAcc?
                          
                          
                          
                            record !.amount = amount?
                          
                          
                          
                          
                            record !.success ⇔ amount? ⩽ balance(srcAcc?)
                          

Concrete simulation configuration. The simulation instantiates the abstract specification with fixed
sets:
        USER = {u1 , u2 , u3 },       ACCOUNT = {a1 , a2 , a3 , a4 , a5 , a6 }
with ownership
        owns = {u1 7→ {a1 , a2 }, u2 7→ {a3 , a4 }, u3 7→ {a5 , a6 }},
and balances initialized nondeterministically subject to dom(balance) = ACCOUNT .



                                                              26
    The definition above is correct but the notation became cumbersome. I’ll make a second attempt below to
obtain a that uses the Z notation only for the interfaces definitions using the schema mechanism.

From natural math to the Z formal specification notation - Second trail
  Human Prompt
  The Z formal specification notation has the notion of schema. A Z schema denotes a set of states or state
  transitions constrained by logic; at the code level it corresponds to a typed interface with invariants and operation
  contracts.
   Modify the following specification to use the Z schema notation to explicitly distinguish interfaces
  that transfer funds and store and retrieve fund scheduled fund transfers. Leave other aspects of
  the specification and do not translate them to Z.
  Here is the specification A.2.2.

    This step required several iterations. Essentially had to specify that my original natural logic specification
should "call" the new defined schemas.

  AI Reply
  The Z formal specification notation has the notion of a schema. A Z schema denotes a set of states or state
  transitions constrained by logic; at the code level it corresponds to a typed interface with invariants and operation
  contracts.
  The following is a single, clean specification written in plain Z notation. No Z libraries, schema environments,
  or special packages are assumed. The original text is minimally edited so that it explicitly refers to the relevant
  Z schemas, which are defined using standard mathematical layout only.

  System model We are given a set of users
         U = {u1 , . . . , un }.
  Each user has a set of accounts that belong to that user. We have a set of accounts
         AC = {ac1 , . . . , ack }
  and a function
         AC (·) : U → P(AC ).
  For any user u ∈ U , AC (u) ⊆ AC is the subset of accounts that belong to u.
  We assume that for any two users ui , uj ∈ U ,
         AC (ui ) ∩ AC (uj ) = ∅
  and
         S
           u∈U AC (u) = AC .

  Thus, each account belongs to exactly one user.
  Each account ac ∈ AC has a balance represented by a natural number (including zero). Account balances are
  modeled by the Z state schema AccountState defined below.
  Fund transfers are a function of the current time. The current time is a natural number initialized to 0 at the
  beginning of the simulation. At each stage of the simulation the current time is first incremented by one.

  Fund transfer operations

  One-time transfer. The one-time transfer is an interface that accepts a source user ui ∈ U , a source
  account aci ∈ AC (ui ), a target user uj ∈ U , a target account acj ∈ AC (uj ), and a transfer amount f .
  The semantics of this interface are defined by the Z schemas OneTimeTransfer and OneTimeTransferFail. If
  the source account has sufficient funds, balances are updated; otherwise, the state is unchanged.

  Planned transfer. A planned transfer is a one-time transfer scheduled to occur at a future time t.
  Planned transfers are stored in a planned transfer set P , modeled by the Z state schema PlannedTransferStore.
  Scheduling a planned transfer is defined by the Z schema SchedulePlannedTransfer. Execution of planned
  transfers due at the current time is defined by the Z schema ExecutePlannedTransfers.



                                                           27
Simulation The simulation of fund transfers consists of stages. In each stage the following steps are taken.
   1. Increment the current time t by 1.
   2. One-time transfer. Randomly choose inputs and perform the one-time transfer using the interface
      defined by OneTimeTransfer and OneTimeTransferFail.
   3. Schedule a planned transfer. Randomly choose inputs for a one-time transfer and a time t ′ > t. Add
      the planned transfer to P using the interface defined by SchedulePlannedTransfer.
   4. Perform planned transfers. For each planned transfer scheduled at time t, execute it using the
      interface defined by ExecutePlannedTransfers.
   5. Report the chosen inputs, the result of each transfer, the transfer type (one-time or planned), the current
      time t, and the state of P before planned transfers are executed.

Simulation initialization Choose three users and six accounts. User one owns accounts 1 and 2, user
two owns accounts 3 and 4, and user three owns accounts 5 and 6. Choose the initial balance of each account
randomly.
The current time is initialized to 0. The planned transfer set P is initialized to the empty set. Each element of
P has type

      U × AC × U × AC × N+ × N.

Z schemas (plain Z notation)

AccountState
                                                
      AccountState =
                   b        balances : AC → N

PlannedTransfer
                      b U × AC × U × AC × N+ × N
      PlannedTransfer =

PlannedTransferStore
                                                                
      PlannedTransferStore =
                           b          P : P(PlannedTransfer )

OneTimeTransfer
                                                                                                                  
                          ∆AccountState
                         srcU , dstU : U                                                                          
                                                                                                                  
                         srcAC , dstAC : AC                                                                       
      OneTimeTransfer =  f : N+
                      b                                                                                           
                                                                                                                   
                                                                                                                  
                         balances(srcAC ) ⩾ f                                                                     
                          balances ′ = balances ⊕ {srcAC 7→ balances(srcAC ) − f , dstAC 7→ balances(dstAC ) + f }

OneTimeTransferFail
                                                            
                              ΞAccountState
                             srcU , dstU : U                
                                                            
      OneTimeTransferFail =  srcAC
                          b         , dstAC : AC            
                             f : N+
                                                             
                                                             
                              balances(srcAC ) < f

SchedulePlannedTransfer
                                                                                  
                                  ∆PlannedTransferStore
                                 srcU , dstU : U                                  
                                                                                  
                                 srcAC , dstAC : AC                               
      SchedulePlannedTransfer =  f : N+
                              b                                                   
                                                                                   
                                 ′                                                
                                 t :N                                             
                                    ′                                          ′
                                  P = P ∪ {(srcU , srcAC , dstU , dstAC , f , t )}


                                                        28
  ExecutePlannedTransfers
                                                                                                                     
                                      ∆AccountState
                                     ∆PlannedTransferStore                                                           
                                                                                                                     
                                     t :N                                                                            
                                                                                                                     
          ExecutePlannedTransfers =
                                  b 
                                     ∀ p ∈  P •                                                                      
                                                                                                                      
                                    
                                        p6 = t ∧ balances(p2 ) ⩾ p5 ⇒                                                
                                                                                                                      
                                                 ′
                                        balances = balances ⊕ {p2 7→ balances(p2 ) − p5 , p4 7→ balances(p4 ) + p5 } 
                                        ′
                                      P = {p ∈ P | p6 ̸= t}

    There are two problems with the above specification. One is that the ExecutePlannedTransfers schema is
described for the specific configuration. The other issue is that the calls to the schema do not describe the inputs
explicitly.

From natural math to the Z formal specification notation - Third trail
  Human Prompt
  Please render again fixing two problems. One is that when stating that you will call a schema in my original
  specification you need to specify the inputs the schema will take. The other is that ExecutePlannedTransfer
  should be described in general and not for the specific simulation configuration.

  AI Reply
  The Z formal specification notation has the notion of a schema. A Z schema denotes a set of states or state
  transitions constrained by logic; at the code level it corresponds to a typed interface with invariants and operation
  contracts.
  The following is a single, clean specification written in plain Z notation (no Z libraries assumed). The original
  text is minimally edited so that:
        • whenever the text refers to a Z schema, the inputs of that schema are explicitly stated, and
        • the schema ExecutePlannedTransfers is defined independently of any particular simulation configuration.

  System model We are given a set of users
          U = {u1 , . . . , un }.

  Each user has a set of accounts that belong to that user. We have a set of accounts

          AC = {ac1 , . . . , ack }

  and a function

          AC (·) : U → P(AC ).

  For any user u ∈ U , AC (u) ⊆ AC is the subset of accounts that belong to u.
  We assume that for any two users ui , uj ∈ U ,

          AC (ui ) ∩ AC (uj ) = ∅

  and
          S
            u∈U AC (u) = AC .

  Thus, each account belongs to exactly one user.
  Each account ac ∈ AC has a balance represented by a natural number (including zero). Account balances are
  modeled by the Z state schema AccountState(balances).
  Fund transfers are a function of the current time. The current time is a natural number initialized to 0 at the
  beginning of the simulation. At each stage of the simulation the current time is first incremented by one.

  Fund transfer operations




                                                           29
One-time transfer. The one-time transfer is an interface that accepts as inputs:
      (ui , aci , uj , acj , f )

where ui , uj ∈ U , aci ∈ AC (ui ), acj ∈ AC (uj ), and f ∈ N+ .
Given these inputs, the operation is defined by invoking either the schema

      OneTimeTransfer (srcU =ui , srcAC =aci , dstU =uj , dstAC =acj , f )

or, when insufficient funds exist, the schema

      OneTimeTransferFail (srcU =ui , srcAC =aci , dstU =uj , dstAC =acj , f ).

Planned transfer. A planned transfer is a one-time transfer scheduled to occur at a future time t.
Scheduling a planned transfer accepts as inputs:

      (ui , aci , uj , acj , f , t ′ )

with t ′ > t, and is defined by invoking the schema

      SchedulePlannedTransfer (srcU =ui , srcAC =aci , dstU =uj , dstAC =acj , f , t ′ ).

Planned transfers are stored in the planned transfer set P , which is modeled by the Z state schema Planned-
TransferStore(P).
Execution of planned transfers due at the current time t is defined by invoking the schema

      ExecutePlannedTransfers(t),

which examines all planned transfers in P scheduled for time t and applies the corresponding one-time transfers.

Simulation The simulation of fund transfers consists of stages. In each stage the following steps are taken.
   1. Increment the current time t by 1.
   2. One-time transfer. Randomly choose inputs (ui , aci , uj , acj , f ) and invoke the schema

                OneTimeTransfer (srcU =ui , srcAC =aci , dstU =uj , dstAC =acj , f )

      or OneTimeTransferFail if the precondition is not met.
   3. Schedule a planned transfer. Randomly choose inputs (ui , aci , uj , acj , f , t ′ ) with t ′ > t and invoke

                SchedulePlannedTransfer (srcU =ui , srcAC =aci , dstU =uj , dstAC =acj , f , t ′ ).

   4. Perform planned transfers. Invoke

                ExecutePlannedTransfers(t)

      to execute all planned transfers scheduled at the current time.
   5. Report the chosen inputs, the result of each transfer, the transfer type (one-time or planned), the current
      time t, and the state of P immediately before planned transfers are executed.

Simulation initialization Choose three users and six accounts. User one owns accounts 1 and 2, user
two owns accounts 3 and 4, and user three owns accounts 5 and 6. Choose the initial balance of each account
randomly.
The current time is initialized to 0. The planned transfer set P is initialized to the empty set. Each element of
P has type

      U × AC × U × AC × N+ × N.

Z schemas (plain Z notation)

AccountState
                                                        
      AccountState =
                   b                 balances : AC → N



                                                             30
  PlannedTransfer
                        b U × AC × U × AC × N+ × N
        PlannedTransfer =

  PlannedTransferStore
                                                                 
        PlannedTransferStore =
                             b         P : P(PlannedTransfer )

  OneTimeTransfer
                                                                                                                  
                            ∆AccountState
                           srcU , dstU : U                                                                        
                                                                                                                  
                           srcAC , dstAC : AC                                                                     
        OneTimeTransfer =
                        b 
                           f :N +
                                                                                                                   
                                                                                                                   
                                                                                                                  
                           balances(srcAC ) ⩾ f                                                                   
                                     ′
                            balances = balances ⊕ {srcAC 7→ balances(srcAC ) − f , dstAC 7→ balances(dstAC ) + f }

  OneTimeTransferFail
                                                             
                                ΞAccountState
                               srcU , dstU : U               
                                                             
        OneTimeTransferFail =  srcAC
                            b         , dstAC : AC           
                               f : N+
                                                              
                                                              
                                balances(srcAC ) < f

  SchedulePlannedTransfer
                                                                                    
                                    ∆PlannedTransferStore
                                   srcU , dstU : U                                  
                                                                                    
                                   srcAC , dstAC : AC                               
        SchedulePlannedTransfer =  f : N+
                                b                                                   
                                                                                     
                                   ′                                                
                                   t :N                                             
                                      ′                                          ′
                                    P = P ∪ {(srcU , srcAC , dstU , dstAC , f , t )}

  ExecutePlannedTransfers
                                                                                                                       
                                    ∆AccountState
                                   ∆PlannedTransferStore                                                               
                                                                                                                       
                                   t :N                                                                                
                                                                       ′
                                                                                                                       
        ExecutePlannedTransfers =
                                b 
                                   ∀(u  i , ac i , u j , ac j , f , t   ) ∈   P •                                      
                                                                                                                        
                                         ′
                                  
                                      t   =   t  ∧   balances(ac          i ) ⩾ f ⇒                                    
                                                                                                                        
                                      balances ′ = balances ⊕ {aci 7→ balances(aci ) − f , acj 7→ balances(acj ) + f } 
                                    P ′ = {p ∈ P | π6 (p) ̸= t}

    The AI addressed the two issues correctly.

Invariant proof using the Z modeling of the interfaces Next we attempt to proof the invariants
that were prove above using the Z modeling of the interfaces.

  Human Prompt
  Given some legal configuration of the system and consider the inductive set of configurations created by the
  applications of the schema defined above, namely, OneTimeTransfer, OneTimeTransferFail, SchedulePlanned-
  Transfer, and ExecutePlannedTransfers. We refer to that inductive set as I. Prove the following claim.
                                     P
  Lemma 9. The amount of money aci ∈AC aci remains constant for all configurations in the inductive set I.


Stronger invariant claim. Note that the following claim and its proof are strictly stronger than those
presented in the previous sections. We show that the inductively defined set I (C , SCHEM A), obtained from any



                                                         31
legal initial configuration C by repeated application of the schemas in the specification (denoted by SCHEM A),
satisfies the invariant claim. In other words, every configuration reachable by any finite sequence of applications of
the operations defined by the schemas preserves the invariant.
     As a consequence, the proof is not tied to any particular simulation or execution strategy. It applies uniformly to
all possible sequences of schema applications starting from a legal configuration. This establishes the invariant as a
global property of the specification itself, rather than a property of a specific operational interpretation or execution
model.

  AI Reply
  Below is a Z-style invariant proof formatted so that displayed lines are short and fit comfortably within a page.

  Lemma Let I be the inductive set of configurations generated from an initial legal configuration by finite
  applications of the schemas

         OneTimeTransfer , OneTimeTransferFail , SchedulePlannedTransfer , ExecutePlannedTransfers.

  Lemma 10. For every configuration in I , the total amount of money
      P
        ac∈AC balances(ac)

  remains constant.

  Proof The proof proceeds by induction on the construction of the inductive set I .

  Base case. Let the initial configuration be given by
         AccountState(balances0 ),      balances0 : AC → N.

  The quantity
        P
           ac∈AC balances0 (ac)

  is fixed. Hence the invariant holds initially.

  Inductive hypothesis. Assume that for some configuration in I ,
         P
           ac∈AC balances(ac) = M ,

  for a constant M .

  Inductive step. We show that the invariant is preserved by each schema.

  Case 1: OneTimeTransfer. The schema defines
         balances ′ = balances ⊕ {srcAC 7→ balances(srcAC ) − f , dstAC 7→ balances(dstAC ) + f },

  with the precondition balances(srcAC ) ⩾ f . All other balances are unchanged. Therefore,
         P                ′      P                                 P
           ac∈AC balances (ac) =    ac∈AC balances(ac) − f + f =     ac∈AC balances(ac).


  Case 2: OneTimeTransferFail. This schema includes ΞAccountState, hence
         balances ′ = balances.

  The invariant is preserved.

  Case 3: SchedulePlannedTransfer. This schema modifies only the planned transfer store and leaves the
  account state unchanged:

         balances ′ = balances.

  The invariant is preserved.



                                                           32
  Case 4: ExecutePlannedTransfers. Each executed planned transfer updates balances as follows:
         balances(aci ) 7→ balances(aci ) − f ,
         balances(acj ) 7→ balances(acj ) + f ,

  subject to balances(aci ) ⩾ f . Each update preserves the total sum of balances. Since ExecutePlannedTransfers
  is a finite composition of such updates, and updates to the planned transfer store do not affect balances, the
  invariant is preserved.

  Conclusion. All schemas generating I preserve the total balance invariant. Since it holds in the initial
  configuration and is preserved by every inductive step, it holds for all configurations in I :

         ∀ c ∈ I • ac∈AC balances(ac) = constant.
                  P

                                                                                                                     2

Have the AI suggest the interfaces In this subsection we attempt to have the AI create the interfaces
with no inhints on their possible content.

  Human Prompt
  The Z formal specification notation has the notion of a schema. A Z schema denotes a set of states or state
  transitions constrained by logic; at the code level it corresponds to a typed interface with invariants and operation
  contracts.
   Modify the following specification to use the Z schema notation to explicitly distinguish interfaces
  that apply to the specification below. Leave other aspects of the specification and do not translate
  them to Z.
  Here is the specification A.2.2

    Here is the AI reply.

  AI Reply
  The specification below is minimally augmented with Z schema notation in a package-free form. Schemas are
  rendered using standard math displays, making interfaces, invariants, and contracts explicit. All other aspects
  remain informal and unchanged.

  Basic Sets and Types
         [U , AC ]

         N =N        N + = N \ {0}

         Transfer = U × AC × U × AC × N + × N

  Global State Interface
          FundTransferState =b
                                                                      
              accounts : AC → N
             owner : AC → U              ∀ ac1 , ac2 : AC ·           
            
             time : N                     owner (ac1 ) = owner (ac2 ) 
                                                                       
                                           ⇒ ac1 = ac2
              P : P(Transfer )

  One-Time Transfer Interface
          OneTimeTransfer = b
                                                           
              ∆FundTransferState
            us , u t : U                  owner (acs ) = us 
                                                            
            acs , act : AC                owner (act ) = ut 
              f : N+



                                                           33
  Transfer Contract
  If sufficient funds exist:

         accounts(acs ) ⩾ f

         accounts ′ = accounts ⊕ {acs 7→ accounts(acs ) − f , act 7→ accounts(act ) + f }

  Otherwise:

         accounts(acs ) < f ⇒ accounts ′ = accounts


  Planned Transfer Scheduling Interface

          SchedulePlannedTransfer =
                                  b
                                                     
               ∆FundTransferState
             us , u t : U          owner (acs ) = us 
                                                     
             acs , act : AC        owner (act ) = ut 
                     +
                                                      
             f :N                  tp > time         
               tp : N


         P ′ = P ∪ {(us , acs , ut , act , f , tp )}


  Planned Transfer Execution Interface

          ExecutePlannedTransfer =
                                 b
                                                                
              ∆FundTransferState                 p∈P
              p : Transfer                       π6 (p) = time


         P ′ = P \ {p}

  The balance update obeys the OneTimeTransfer contract.

  Simulation Clock Interface

          AdvanceTime =
                      b
                                                 time ′ = time + 1
                                                                    
              ∆FundTransferState


  Summary

      • Z-style schemas are expressed using plain LaTeX.
      • Interfaces, invariants, and contracts are explicit.
      • No additional packages are required.
      • The original informal specification is preserved.

     On the positive, side the AI was able to identify the major interfaces by itself. On the negative side, it mixed
schema with natural language description which is confusing. It also made the mistake of referring to π6 (p) which
is a specific simulation detail. It also took away details such as the simulation initialization.




                                                                     34
