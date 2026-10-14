                                                       Can LLMs help find Ambiguities in Protocol Specifications?

                                             Ziyue Dang* 1 , Sixu Tan* 2 , Atharva Nevasekar2 , Zhaowei Tan2 , George Varghese1 , and Songwu Lu1
                                                                                                         1 UCLA

                                                                                        {ziyue.dang, varghese, slu}@cs.ucla.edu
                                                                                             2 University of California, Riverside

                                                                                           {stan073, aneva018, ztan}@ucr.edu
arXiv:2609.38752v1 [cs.NI] 30 Sep 2026




                                         Abstract                                                               was originally loosely designed to let applications spec-
                                                                                                                ify network preferences, the IETF completely rewrote the
                                         Internet protocol specifications written in RFCs are subject           rules multiple times [8, 55, 67]. These mid-lifecycle updates
                                         to ambiguities and multiple interpretations that can cause in-         caused discrepancies between legacy network hardware and
                                         teroperability failure. While these have presumably cleared            modern equipment. This raises the question: is there a better
                                         up after years of experience, such ambiguities can bedevil             way to find specification ambiguities early for newer proto-
                                         the adoption of newer protocols like 5G. The 5G specifica-             cols without requiring protocol designers to abandon English
                                         tions pair a formal message syntax (ASN.1) with message-               prose specifications instead of hard to learn formal languages
                                         handling procedures written in natural language. This creates          such as LOTOS [39], Estelle [38], or SDL [40].
                                         semantic underspecification: a syntactically valid message                We ground our study of protocol ambiguity in the more
                                         can reach a state whose procedures never say how to han-               recent 5G protocols that are arguably less mature than the
                                         dle it, so standard-compliant implementations diverge. We              classic Internet suite. The 5G system provides mobile inter-
                                         frame this as a gap or a fork in a partially specified commu-          net access for billions of users. Its design has been standard-
                                         nicating state machine, and present S PEC L ENS, which puts            ized by the 3GPP (3rd Generation Partnership Project) [2]
                                         that view in front of a language model as a scaffold. Stronger         and O-RAN (Open Radio Access Network) [61] specifica-
                                         models do not remove the need for it: they broaden the search          tions. These specifications define both the message formats
                                         without disciplining it, and fewer than half their findings sur-       (syntax) and the message handling procedures written in nat-
                                         vive inspection. Across 36 procedures from six 3GPP and O-             ural language. At the end of the paper we also turn our lens
                                         RAN protocols, experts accept 185 of 197 S PEC L ENS find-             briefly on a very mature protocol, DNS, and find (perhaps
                                         ings, and 60 drive observable divergence between the Ope-              surprisingly) several unresolved ambiguities.
                                         nAirInterface and srsRAN implementations under differen-                  More precisely, we study semantic underspecification:
                                         tial test. While we use 5G as a canonical example of a newer           procedural text that fails to guide the processing of syntac-
                                         protocol, we also show ambiguity results for the more mature           tically valid messages. Note that our problem is not about
                                         DNS protocol.                                                          identifying specification errors (where erroneous descrip-
                                                                                                                tions are given) or implementation bugs (where code fails
                                                                                                                to meet requirements), both studied extensively in prior
                                         1      Introduction                                                    work [46, 66, 63, 19].
                                                                                                                   Since protocols are defined in natural language, Large
                                         Early protocol standards, exemplified by ISO and ITU,
                                                                                                                Language Models (LLMs) are conceptually promising, given
                                         relied on complete specifications (ideally in formal lan-
                                                                                                                their strengths in semantic understanding and reasoning.
                                         guages) designed before implementation. By contrast, the
                                                                                                                However, we find that a naïve direct prompting approach
                                         Internet relied on “rough consensus and running code” [23]
                                                                                                                does not work. It rediscovers a few shallow, high-probability
                                         and English language specifications in RFCs. While these
                                                                                                                gaps across many fields and misses many cross-step cases.
                                         were wildly successful, the historic axiom “be conserva-
                                                                                                                   Will more powerful models solve the problem? Many soft-
                                         tive in what you send, be liberal in what you accept” often
                                                                                                                ware engineering scaffolds became redundant with the ad-
                                         masked specification flaws. These sometimes surfaced as at-
                                                                                                                vent of Claude 4.5. We found experimentally (§7.2) that re-
                                         tack vectors that required implementation changes: for ex-
                                                                                                                moving the scaffold altogether by giving whole specifica-
                                         ample, overlapping IP fragments [18] and malformed IP op-
                                                                                                                tions to frontier agentic models (e.g., Opus 5.0), buys breadth
                                         tions [29]. In some instances, such as the TOS field, which
                                                                                                                but not discipline. Fewer than half the findings mined with-
                                             * Equal contribution (co-first authors).                           out our scaffold survive inspection, and a third conflate free-


                                                                                                            1
          (a) An information-element (IE) syntax table.                               (b) A natural-language procedure description.
                                               Figure 1: The two parts of a 3GPP/O-RAN specification.



dom the standard purposely grants with specification failure.                nally, communicating state machines are one model among
Further, a third of our scaffolded findings are missed with-                 several: a richer model such as timed automata [10] may pro-
out a scaffold. Worse, without scaffolding, the model output                 duce a finer-grain taxonomy at the cost of harder extraction.
is an unstructured grab bag of underspecification candidates,
riddled with false positives and negatives.
   Instead, we propose S PEC L ENS, a scaffolded LLM-driven                  2     Background
analysis framework that systematically uncovers underspec-
ifications in 5G protocols. S PEC L ENS works with avail-                    The 5G system is defined by two standards bodies. The 3rd
able LLM tools, but departs from conventional end-to-end                     Generation Partnership Project (3GPP) specifies the radio ac-
prompting. Our key contribution is to model a specification                  cess network (RAN) and its core-network protocols [2], and
as a set of communicating state machines and to use this                     the O-RAN Alliance specifies an open, disaggregated real-
model to infer a set of underspecification categories that flow              ization of that RAN [61]. Disaggregation divides the RAN
directly from the state machine definition.                                  into components that may come from different vendors, such
                                                                             as a central unit (CU) and one or more distributed units
   We then orchestrate a staged inference workflow using our
                                                                             (DUs), and connects them over standardized interfaces: F1
state machine lens: context construction, taxonomy-based
                                                                             between the CU and a DU, E1 inside a split CU, NG be-
mining, gap/fork triage, and impact analysis with a deter-
                                                                             tween the RAN and the core, and E2 between the RAN and
ministic state-machine engine that also derives a differential
                                                                             its near-real-time controller. These interfaces are served by
test (§5). Rather than replacing domain experts, S PEC L ENS
                                                                             dedicated protocols: F1AP [6], E1AP [5], NGAP [3], and
produces a ranked set of under-specified cases with textual
                                                                             E2AP [56] for control-plane signaling, GTP-U [4] for the
evidence, an impact estimate, and a test design.
                                                                             user plane, and E2 service models such as E2SM-KPM [57]
   Our preliminary evaluation covers 36 procedures across
                                                                             for the content exchanged over E2. Because independently
six 3GPP and O-RAN protocols, run with three LLM back-
                                                                             built components must interoperate across these interfaces,
ends. The findings hold up under scrutiny: reading each can-
                                                                             the interface specifications carry the full weight of defining
didate against the standard, two domain experts conserva-
                                                                             compatible behavior.
tively support 185 of 197 proposals, and 195 are supported
                                                                                A specification fixes that behavior in two parts, shown in
by code or at least one expert. 60 of the findings drive ob-
                                                                             Figure 1. The syntax, expressed in ASN.1, defines the for-
servable divergence between the independent OpenAirInter-
                                                                             mat of each message and the information elements (IEs) it
face and srsRAN stacks under differential test, most of them
                                                                             may carry (Figure 1a). The procedures, written in natural
incompatible decisions such as one implementation accept-
                                                                             language, describe how a node processes a received message
ing where the other rejects. Some are outright hazards: a sin-
                                                                             and how it updates its internal state (Figure 1b). Syntax and
gle legal PDU SESSION RESOURCE RELEASE COMMAND
                                                                             procedures together fix a message’s semantics: the action a
carrying one stale session identifier frees a single session on
                                                                             node takes and the state it reaches upon receiving that mes-
one implementation but tears down the device’s entire con-
                                                                             sage. These semantics are state-dependent. The same syntac-
nection on the other.
                                                                             tically valid message can demand different handling accord-
   We also describe early results with the more mature (50+                  ing to the receiver’s protocol state, which comprises its ac-
years) DNS, finding, perhaps surprisingly, a few: e.g., how                  tive connections, pending operations, and the history of mes-
much to advance a zone’s SOA serial number on an update                      sages exchanged so far.
(RFC 2136 [79]).
   Our results in 5G and DNS open up three directions
(§10). Several validated underspecifications are already ex-                 3     The Problem of Underspecification
ploitable: this motivates mining using an adversarial lens
rather than an interoperability one. Second, our unit of anal-               We study semantic underspecification: cases in which a
ysis is one document, while a modern protocol’s contract is                  specification admits a syntactically valid message in a reach-
spread across many, so the ambiguities that live in the inter-               able protocol state, yet its natural-language procedures do
play between documents are ones we cannot yet express. Fi-                   not determine how the receiver should handle it. Such a case


                                                                         2
                                                                                               8.3.2.1 General. The purpose of the UE Context Release Request procedure is to
                                                                                               enable the gNB-DU to request the gNB-CU to release the UE-associated logical F1-
                            Specification                                                      connection [. . . ].
                                                                                               8.3.2.2 Successful Operation. The gNB-DU [. . . ] initiates the procedure by gen-
                                                                                               erating a UE CONTEXT RELEASE REQUEST message towards the affected gNB-
 Ambiguity Level      What is a "Finding"              Illustrative Example                    CU [. . . ]. The UE Context Release procedure may be initiated upon reception of a
                                                                                               UE CONTEXT RELEASE REQUEST message.
                       A word or phrase has
      Lexical                                    "The system shall respond quickly" —          8.3.2.3 Abnormal Conditions. If one or more candidate cells in the Candidate
                      multiple meanings or is
   ([13, 50, 86])                                        "quickly" is undefined.
                               vague                                                           Cells To Be Cancelled List IE [. . . ] were not prepared using the same UE-associated
                         A sentence admits      "with [invalid header] OR [unsupported         signaling connection, the gNB-CU shall ignore those non-associated candidate cells.
     Syntactic
                       multiple grammatical method]" v.s. "with [an invalid header or
   (SAGE [88])
                            parse trees. Assets         an unsupported method]"
      Logical                                      Section A says timer T expires →           Figure 3: F1AP UE Context Release Request (TS 38.473 §8.3.2): the Ab-
                            Contradiction,
 (CellularLint [66],                             release; Section B says → retry. RFC         normal Conditions clause covers only stray candidate cells, not a request
                     nonexistent reference, or
RFCScope [63], [22,                             writes "QDCODE" in one sentence but           naming a connection the gNB-CU does not hold.
                       a term never defined.
      32, 47])                                       "QDCOUNT" everywhere else.
                          Syntax permits a      A config update allows the same item in
     Semantic        message, but procedural both "add" and "delete" lists (syntax-
      (Ours)         text provides no handling valid); but procedure never addresses
                             guidance                       this combination.


Figure 2: Where semantic underspecification sits among prior ambiguities.                     a message m in a state s; it moves the machine to a next
                                                                                              state s′ and may emit messages of its own. We write it as
                                                                                              (s, m) → (s′ , o), with the current state and input on the left
is not an error. Each individual statement may be correct; the                                and the resulting state and output on the right.
specification is simply silent, or admits several incompati-
ble readings, about a scenario its own syntax permits. This                                      A complete protocol would fix exactly one such transition
sets our target apart from most prior work on specification                                   for every reachable state and every message that can arrive
quality, which looks for a defect that is present in the text                                 there. A natural-language specification does not. It induces a
or in a model built from it: a contradiction or broken cross-                                 transition relation δ spec that may leave a case out or permit
reference between clauses [66, 63], a word or phrase open to                                  more than one resolution, so the behaviors it allows form a
more than one meaning [86, 50], or a transition missing from                                  set of runs Rspec rather than a single one. A conformant im-
a state machine an analyst has already built by hand [46].                                    plementation is any deterministic choice inside that set, a re-
Figure 2 places these notions on a common scale. Semantic                                     finement δ impl ⊆ δ spec , so two conformant implementations
underspecification sits at the boundary between a specifica-                                  can differ wherever δ spec fails to pin the transition down. Un-
tion’s formal syntax and its prose, where the two are together                                derspecification is that freedom.
meant to fix behavior but do not.
   Underspecification is a structural consequence of how                                         The F1AP UE Context Release Request procedure shows
these documents are written, not an accident of any one of                                    how that freedom arises (Figure 3) [6]. A gNB-DU asks the
them. Message syntax is defined formally in ASN.1, admit-                                     gNB-CU to release a UE’s F1 connection by sending a UE
ting an enormous space of valid messages and field combina-                                   CONTEXT RELEASE REQUEST, upon which the gNB-CU
tions. The procedures that give those messages meaning are                                    may initiate the release. The procedure constrains just one
prose, which cannot enumerate every combination of mes-                                       edge case, stray candidate cells, and is silent on another: a
sage and state. What remains is a residue of syntactically                                    request that names a UE-associated connection the gNB-CU
valid scenarios for which the procedures prescribe no clear                                   does not currently hold. That configuration is reachable and
behavior. In a single-vendor deployment such a scenario may                                   the message can arrive in it, yet no transition is defined there.
never surface; across the multi-vendor open interfaces of §2                                  Release handling underspecified in this way is not hypothet-
it becomes an interoperability hazard [69, 65], because two                                   ical: §7.4 shows that gaps around releasing a context that is
independently built components can resolve the same silent                                    not currently active drive observable divergence between in-
case in incompatible ways. The residue also grows rather                                      dependent gNB implementations.
than shrinks, since each release adds messages, fields, and
                                                                                                 We can state the condition exactly. Fix a reachable state s
interfaces faster than prose can cover their combinations.
                                                                                              and a message m that can arrive there, and let ∆spec (s, m) be
                                                                                              the set of next states the specification allows. The scenario
3.1     A state-machine view of specifications                                                is well specified when this set holds exactly one element.
                                                                                              It is underspecified in one of two forms: |∆spec (s, m)| = 0, a
To make “does not determine how the receiver should handle                                    gap, where no transition is given, or |∆spec (s, m)| ≥ 2, a fork,
it” precise, we model a protocol as a set of communicating                                    where several are. The case above is a gap. We return to what
state machines, one per role, that exchange messages over                                     the two forms imply in §3.3, and give the full run semantics,
channels [17]. Each machine has a set of local states and a set                               together with a test that separates underspecification from
of transitions. A transition fires when the machine receives                                  questions the model cannot answer, in Appendix A.


                                                                                          3
3.2    Where underspecification lives                                   are consequential (§5.4).
The case above under-constrains a single transition, but not
every opening is local. A protocol’s behavior is a set of runs,         3.4    Challenges
and a run is an arrangement of transition firings, each with its
own content. Underspecification can therefore enter at either           Three aspects of the problem make it hard, and each chal-
level: in how firings are arranged across a run, or in what one         lenge shapes the design in §5.
firing consumes and produces. These levels split into four              Discovery. Discovery is hard because the target is an ab-
components, which structure the search in §5.2.                         sence. Classical audits key on something present: a con-
Local content. A transition’s trigger is the current state              tradiction, an ambiguous term, a transition missing from a
together with the message that enables it; its effect is the next       model already drawn. An underspecified case offers no key-
state and any output it produces. A trigger is underspecified           word and no malformed structure, and does not take shape
when it is unclear whether a transition applies at all in a given       until one fixes the state and message that expose it. Those
state on a given message. An effect is underspecified when              pairs are enormous in number, since a procedure’s dozens
the message is accepted but its consequences, the next state,           of information elements across several messages and states
the response, or the cleanup, are left open.                            combine multiplicatively. Enumerating them blindly is infea-
Temporal arrangement.             Across several firings, two           sible, reading every procedure by hand does not scale, and
questions arise that no single transition answers; they are the         neither a formal model built up front nor an open-ended re-
safety and liveness sides into which a run property classi-             quest to a language model recovers the missing cases (§4).
cally decomposes [9]. Ordering, the safety side, asks which             Discovery must turn this blind search into a structured one.
enabled transition fires first, whether two are ordered or may          Triage. A discovered opening does not announce its own
interleave, and whether they must fire as one atomic step.              remedy. Deciding whether the text is silent about the case
Eventuality, the liveness side, asks whether some transition            or instead covers it too loosely to pin one outcome requires
must eventually fire, such as a response sent, a loop exited,           weighing what the cited clauses actually settle, and the an-
or a resource released.                                                 swer fixes the repair: write the missing rule, or narrow an
   These four components are exhaustive for the model. A                over-permissive one.
run-set is an arrangement of firings, governed by Ordering              Impact and validation. A finding matters only when its
and Eventuality, over firings whose content is governed by              resolutions diverge observably, and establishing that is ex-
Trigger and Effect, so any under-constraint falls in one of             pensive: candidates are numerous and some protocols lack
them. They are also independent: a trigger can be missing               a second implementation to test against. Assessing impact
while its intended effect is clear, ordering can be open while          needs both a conceptual analysis that runs without an imple-
every local transition is fixed, and an eventuality can be open         mentation and, where implementations exist, execution that
even when every step is individually defined. Real findings             confirms the divergence.
often combine components, but the four components name
distinct ways a specification can be silent.
                                                                        4     Scaffolding with State-Machines
3.3    Gaps, forks, and when they matter                                Reasoning about underspecification demands two things at
Gap and fork are not a fifth category but the two forms any             once: a precise vocabulary for protocol behavior, and the
of the four components can take, and they call for different            ability to read the natural-language procedures that define
remedies. A gap is silence: the specification gives no rule,            it. A state machine provides the first, and a large language
so the defect is a design omission and the remedy is to add             model (LLM) provides the second. Each is necessary, and
the missing rule. A fork is over-permission: the text does ap-          neither suffices alone.
ply, but it is loose enough to admit two or more incompatible
readings of the same case, so the remedy is to narrow it until          4.1    FSMs: right mental model, wrong tool
one behavior survives, or to make the choice explicit and ne-
gotiated on the wire. Both repairs belong in the specification;         A communicating state machine is the natural abstraction for
they differ in whether a rule must be written or an existing            a protocol. Protocol behavior is reactive and stateful, and a
one tightened. Two conditions decide whether a gap or fork              state machine renders it explicit: each rule is a transition,
is worth reporting. Reachability: a missing rule in a state no          each state a condition, and the meaning of a message is
run reaches changes no behavior. Observable divergence: if              where the two meet. This is what makes FSM a good basis
every admissible reading yields the same outcome the under-             for reasoning. It is explainable, it localizes a defect to a tran-
specification is latent and we set it aside, whereas readings           sition or state, and, as §3 showed, the categories and forms
that accept where another rejects, or emit different responses,         of underspecification fall directly out of it.


                                                                    4
   Turning a real specification into such a machine, how-            is a claim of absence over a document, which a model
ever, is itself the hard problem. Manual formal models pay           trained to guess, not to abstain, will make whether or not
for their precision with expert effort and narrow scope, a           it holds [42, 77]. A common refinement, iterating the prompt
paper-length undertaking per procedure [14, 64], and recov-          with its own best findings as few-shot examples for the next
ering a machine from the prose automatically yields mod-             round, does not supply the missing breadth either. Few-shot
els that remain partial and scoped to what could be ex-              examples steer a model’s output distribution toward them-
tracted [7, 62, 91]. The difficulty is intrinsic to the docu-        selves [93]; so seeding later rounds with prior findings keeps
ments, which are large, incomplete, and full of implicit state       the search near those prototypes and rediscovers the same
and unstated guards, the very properties that let underspeci-        gap families instead of surfacing new ones (§7.2).
fication exist. No complete and authoritative state machine             §1 reported that model capability does not make the scaf-
of these protocols is available to check, so a method that           fold useless. When we expanded capability inside one fam-
searches for undefined transitions inherits both the cost and        ily from gpt-5.4 nano to mini to full (isolating the workflow
the incompleteness of whatever model it starts from [46].            from the model), we found that cases spanning several proto-
   The target also moves. 3GPP revises these specifications          col steps (for Ordering and Eventuality) are ones that a local
at quarterly plenaries and a new release takes two to three          prompt misses most: our pipeline on the weakest model finds
years [2], so a model faithful to one version soon drifts be-        more of them than naïve prompting finds on the strongest,
hind. Full formalization is therefore the wrong primary tool.        roughly 1/2 against 1/3, a gap that never closes (§7.2). Re-
We keep the state machine for what it is good at, a precise          moving the scaffold entirely by letting two frontier agentic
and explainable account of behavior, and use it as a lens and        models direct their own process over whole specifications
a local instrument rather than a global model to build. As           also missed several underspecifications. What the scaffold
a lens it defines what counts as underspecification and sorts        contributes is therefore not knowledge the model lacks but a
each finding into Trigger, Effect, Ordering, or Eventuality          standard of admission it has no reason to apply on its own, a
(§3). As a local instrument it supplies, for one finding at a        property of the problem rather than of any model generation.
time, only the small fragment of transitions and candidate
completions needed to compare behaviors and derive a test
(§5). The entire FSM never has to be built.
                                                                     4.3   Putting the two together
                                                                     The two limitations are complementary, which we can ex-
4.2   Naïve prompting is not enough                                  ploit. A state machine has the structure that prompting lacks
                                                                     but cannot read the prose; an LLM reads the prose but, if un-
What the state machine cannot supply is the reading of the           constrained, lacks the structure. S PEC L ENS places the state
prose that says which transitions exist in the first place.          machine in front of the LLM as a reasoning scaffold rather
That is where an LLM excels. Protocol procedures are                 than a model to construct: the state-machine view turns an
natural-language text threaded with long cross-references,           open-ended request into bounded, typed, and located ques-
and LLMs are suited to exactly this material: they have been         tions over named transitions, and the LLM answers each one
applied directly to specifications and RFCs [71, 52], their          from the specification text. Decomposing an ill-posed task
context windows hold a procedure together with the clauses           into constrained sub-questions is the established way to steer
it refers to [51], and their reasoning weighs one reading of a       a model clear of these failure modes [96]. The scaffold sup-
clause against another [83, 82, 72].                                 plies structure, process, and coverage; the LLM supplies the
    The obvious way to use an LLM is to supply a procedure           reading. The pipeline of §5 is how the two are combined.
and ask it to list the underspecifications. §7.2 measures how           The division also says which half is affected by model ca-
this falls short: against our pipeline on the same procedures,       pability. The reading improves with every model generation,
open-ended prompting covers a narrower slice of the proto-           and S PEC L ENS inherits that improvement unchanged. What
col, repeats one shallow gap across many information ele-            the scaffold holds fixed, a lens for what counts as an opening
ments, and reaches fewer of the cross-step cases.                    and a deterministic verdict on whether it matters, answers the
    The failure is structural, and §3 already named its cause:       question instead of the model.
the target is an absence. Asking a model to list what a
document fails to say is an under-constrained generation
task, and under-constraint is where LLMs are known to be             5     Design of S PEC L ENS
weak [86]. They collapse onto their most probable output
and re-emit one gap template rather than exploring distinct          §4 argued for placing the state machine in front of the LLM
ones [45]; they default to local, single-step completion and         as a scaffold. S PEC L ENS realizes that scaffold as the six-
under-explore the reasoning about arrangement and change             stage pipeline of Figure 4. Each stage poses the LLM one
across a run that Ordering and Eventuality require [43, 78].         bounded question, grounded in specification text and an-
Asserting that a specification does not constrain some case          swered as typed JSON, while the scaffold owns everything


                                                                 5
                                                                   LLM Tool (e.g., ChatGPT, Claude, Gemini, etc.)

                                               API call                API call                          API call               API call

                                                                                                           Impact Analysis                 Reporting w/ Test
                          Spec Ingestion           Underspec             Triage (Stage 3)
                                                                                                              (Stage 4)                        Design
                            (Stage 1)            Mining (Stage 2)
                                                    FSM-inspired         Underspec form: Gap               Narrative generation +             (Stage 5)
                           Procedure closure
                                                     Taxonomy                 vs. Fork                   FSM transition comparison          Ranked underspecs +
                             construction
                                                                                                                                           differential test designs
          Specification

                                                                       Iterative Execution &                              Downstream:
                                                Vector Database       Deduplication (Stage 6)
                                                                      Run k times to improve coverage;
                                                                      deduplication across iterations


                          Challenge 1:                                Challenge 2:                  Challenge 3: Impact Differential testing for Expert
                           Discovery                                    Triage                         & Validation       concrete evidence      review


                                                             Figure 4: The S PEC L ENS pipeline.



around it: the state passed between stages, the iteration that                        reader would assemble. When it is still insufficient, the min-
drives coverage, and the judgments that decide whether a                              ing stage may request additional sections once from a ta-
finding matters.                                                                      ble of contents, under a fixed character budget, rather than
   Two principles shape the design. The task is decomposed                            silently reasoning from a partial view.
using the CFSM of §3. Each stage asks about one part of the
model: a transition’s trigger or effect, the arrangement of fir-
ings over a run, the form of an opening, or the completions                           5.2       Stage 2: Taxonomy-based mining
that fill it. The consequential judgments are computed by a
                                                                                      Mining turns the four categories of §3.2 into the search it-
deterministic FSM engine rather than by the LLM: the model
                                                                                      self, in two scoped passes over the closure. A local pass
extracts a small state machine from the prose; the engine de-
                                                                                      mines Trigger and Effect, the content of a single transition,
cides which behaviors diverge and how to tell them apart.
                                                                                      and a temporal pass mines Ordering and Eventuality, the ar-
Appendix B gives the prompt for each stage’s question.
                                                                                      rangement of firings across a run. Splitting them bounds each
   The stages map to the three challenges of §3.4. Stages 1
                                                                                      prompt to a single category.
and 2 address discovery, Stage 3 triage, and Stages 4 and 5
                                                                                         The temporal pass is gated on applicability, because con-
impact and validation, while Stage 6 runs underneath, iterat-
                                                                                      currency and loops are the structural sources of temporal un-
ing until coverage saturates. Popping up a level, the pipeline
                                                                                      derspecification, and most procedures have neither. Ordering
instantiates a recipe that is not specific to protocols: choose
                                                                                      is mined only when the procedure admits concurrent or over-
a lens, turn it into bounded typed questions, and adjudicate
                                                                                      lapping transactions over shared state. Eventuality is mined
deterministically. This is the core of our scheme; by contrast,
                                                                                      only when a run can fail to progress through a loop, a retry,
the closure construction and deduplication thresholds are en-
                                                                                      or a pending obligation that is not forced to occur. A strictly
gineering details other implementations could replace.
                                                                                      sequential request and response admits neither, and the pass
                                                                                      returns nothing rather than manufacture a finding. Across
5.1    Stage 1: Context construction                                                  both passes, every finding must cite the messages, IEs, and
                                                                                      sections it concerns and must argue reachability with a con-
3GPP and O-RAN specifications are organized around pro-
                                                                                      crete run. Breadth comes from examining every transition
cedures: named message exchanges that each accomplish
                                                                                      and message using these two passes instead of an open-ended
one task, such as UE Context Release or E2 Setup, with
                                                                                      request, which is why the search does not collapse onto one
a dedicated subsection listing a procedure’s messages, in-
                                                                                      template (§7.2).
formation elements, and handling rules. Implementers rea-
son at this granularity, and so does S PEC L ENS: its unit of
analysis is the procedure, not a fixed-size document chunk.                           5.3       Stage 3: Gap/fork triage
A procedure’s full meaning is nonetheless scattered across
non-contiguous sections, message and IE tables, so Stage 1                            Stage 3 assigns each finding its form. Reading the cited ex-
builds a procedure closure: it locates the sections whose ti-                         cerpts, the LLM decides whether the specification pins a
tles or text match the target procedure, renders their message                        single required behavior for the scenario: silence makes the
and IE tables as Markdown, and resolves local clause refer-                           finding a Gap, and text loose enough to admit two or more
ences recursively, inlining each referenced clause and guard-                         incompatible behaviors makes it a Fork, the |∆| = 0 versus
ing against reference cycles. The result is a self-contained                          |∆| ≥ 2 distinction of §3.3 applied to one finding. Whether
bundle carrying the same cross-reference closure a human                              the looseness was intended is a separate question the model


                                                                                6
   Impact (severe to benign) Decision State Output                               pending message; each completion becomes one branch car-
                                                                                 rying its decision, next state, and expected outputs. Each
   Conflicting Actions                     ✗                                     impact level yields a discriminator, observing the accept-or-
   Inconsistent Internal States            ✓          ✗                          reject decision, probing with the engine’s distinguishing in-
   Inconsistent Notifications              ✓          ✓          ✗               put, comparing emitted notifications, or watching whether
   Latent (dropped)                        ✓          ✓          ✓               progress occurs. Only then is the LLM invoked, for con-
                                                                                 cretization alone: it maps the symbolic states and messages
Table 1: The impact ladder as a cascade over three dimensions: the deci-
sion, the resulting state, and the emitted output. ✓ marks a dimension the       to real message and IE names and fills mandatory IEs with
pair agrees on and ✗ one it differs on.                                          realistic values, but may not change the branch expectations
                                                                                 or the discrimination method. The test’s logic is therefore
                                                                                 fixed by the model and traceable to it, while the LLM sup-
cannot settle, so the stage records its reading without acting                   plies the protocol-specific values it is best equipped to know.
on it, and it defaults to Gap when the evidence is unclear.
                                                                                 5.6    Stage 6: Iteration and deduplication
5.4     Stage 4: Impact analysis                                                 A single mining pass is probabilistic and does not always
Stage 4 decides whether a finding is consequential, and it is                    cover a complex procedure, so S PEC L ENS iterates. Each it-
where the deterministic scaffold does the most work. It runs                     eration re-runs mining from a fresh start and deliberately
in two steps whose separation is the point. First, the LLM                       does not seed the model with earlier findings, since show-
enumerates two to four permissible completions, distinct be-                     ing the model its own prototypes narrows the search rather
haviors the cited text allows, varied by category: competing                     than broadening it (§4). A two-stage filter deduplicates each
trigger rules, differing state updates, orderings, or liveness                   run’s output against a persistent vector store: a keyword fil-
assumptions for eventuality. It then extracts a small partial                    ter proposes candidates sharing the finding’s category and
CFSM fragment from the spec text: the transitions the spec-                      overlapping in its messages, IEs, or sections, and an embed-
ification does pin down, the exposing configuration with a                       ding check removes any whose scenario description is within
concrete reachability trace, the under-constrained slot, and                     a cosine similarity threshold of an existing one. Novel find-
each completion rendered as a transition with a decision, one                    ings are added to the store for the next iteration. Mining stops
of accept, reject, ignore, or no-progress, and a progress flag.                  when two consecutive runs are at least eighty percent dupli-
When the configuration or the slot cannot be grounded in the                     cates. This is what makes the tool terminate and bounds its
text, the model is instructed to leave those fields empty.                       cost to a few passes per procedure (§7.5).
   Second, a deterministic engine, not the LLM, computes                            The six stages produce a ranked report: for each under-
the verdict. A finding whose reachability trace or slot is miss-                 specification, its category and form, the competing interpre-
ing is flagged as un-modelable and set aside, so no severity                     tations, the predicted impact, and a differential test design.
is invented. The engine then compares every pair of comple-                      That single output supports two independent downstream
tions along three dimensions in decreasing severity, its deci-                   uses. A standards reviewer can audit whether the proposal
sion, its resulting state, then its output, as in Table 1, and the               is genuinely unresolved by the normative text, which needs
first dimension on which the pair differs fixes its class. Only                  no implementation and applies even to protocols for which
the state comparison needs more than a syntactic check: two                      none exists. Where two comparable implementations do ex-
different next states count as a divergence only if some later                   ist, differential testing confirms that they resolve the open-
message would treat them differently. Pairs that agree on all                    ing differently. The two establish different things, standards-
three are latent and dropped, and a findings worst surviving                     level plausibility and real implementation consequence, and
class prioritizes it for review and testing. Deciding severity                   §7.3 and §7.4 evaluate each in turn.
mechanically keeps the LLM from grading its own findings,
and the distinguishing message the state check finds becomes
the discriminator the generated test probes with.
                                                                                 6     Implementation
                                                                                 S PEC L ENS owns the workflow and treats the LLM as a re-
5.5     Stage 5: Test design                                                     placeable component; a stronger backend improves it with
                                                                                 no pipeline changes. The system does the durable work, con-
Stage 5 turns a consequential finding into a differential test,                  structing the context, tracking progress and validating each
the clearest instance of the design’s central split. S PEC L ENS                 stage’s output, while the LLM contributes only targeted rea-
first assembles a test plan mechanically from Stage 4’s ar-                      soning at each stage. The implementation is about 5,500
tifacts: the setup is the reachability trace that drives an im-                  lines of Python, of which two components carry the weight
plementation to the exposing configuration, the trigger is the                   of the design: the deterministic FSM engine, which performs


                                                                             7
the reasoning the pipeline does not delegate to an LLM, and             additionally confirmed end-to-end on a live OAI and srsRAN
the component-test harness, which confirms a finding against            testbed (Appendix C).
real implementations. We plan to publicly release the code,
the prompts, and the test harness.
                                                                        7     Evaluation
6.1    The deterministic FSM engine
                                                                        S PEC L ENS produces, for each procedure, a ranked set of un-
The engine is about 575 lines. It consumes the partial CFSM             derspecifications, each with its interpretations, its predicted
fragment that the model-extraction stage emits and returns              impact, and a differential test. We answer four questions:
an impact verdict and a symbolic test plan, in three steps.                Effectiveness (§7.2): Does the FSM-scaffolded pipeline
Loading parses the JSON into typed structures, coercing tol-            discover underspecifications better than naïve prompting?
erantly so that a model that emits a bare string for a list, or            Proposal validity (§7.3): Do domain experts find the pro-
omits a field, is normalized or flagged rather than let it crash        posals grounded in the standard?
the run. Judging applies the ladder of §5.4; the one step be-              Downstream utility (§7.4): Do the proposals expose real
yond comparing recorded fields is a small bounded search                divergence between implementations?
over the specified transitions that decides whether two result-
                                                                           Feasibility (§7.5): Is the workflow affordable, terminat-
ing states are observably distinct. Planning turns the verdict,
                                                                        ing, and portable across model backends.
its branches, and the distinguishing message into the sym-
                                                                           This evaluation leaves two questions open: it reports no
bolic skeleton the concretization stage fills in. Every step ex-
                                                                        recall, since the space of valid-but-unhandled cases admits
cept the model’s own extraction is deterministic, so the ver-
                                                                        no ground truth, and it scopes each analysis to a single pro-
dict is reproducible.
                                                                        cedure, leaving cross-procedure interactions for future work.

6.2    Provider-agnostic pipeline
                                                                        7.1    Setup
The scaffold around the engine is model-agnostic, calling
the LLM only for targeted reasoning at each stage, so ev-               We run S PEC L ENS on the 36 procedures that OpenAirIn-
ery backend we test runs the full pipeline unchanged (§7.5).            terface and srsRAN both implement, drawn from four RAN
python-docx parses the Word specifications into a section               control-plane protocols (F1AP, NGAP, E1AP, and E2AP),
tree from which Stage 1 assembles the procedure closure.                the GTP-U user plane, and the E2SM-KPM service model;
A unified client interface abstracts the provider’s APIs, and           Appendix D lists them. We use three backends: gpt-5.4-
each stage’s output is validated against the expected struc-            mini [58], claude-haiku-4.5 [11], and gemini-3-flash [30].
ture, with tolerant coercion rather than a rigid grammar, be-              The four studies use different populations, which we state
fore the next stage consumes it. A persistent chromadb vec-             once here. Effectiveness pools the pipeline’s findings and a
tor store holds accepted findings, with embeddings fixed to             naïve prompt’s findings across all three backends, and adds
one provider so a finding’s identity stays stable no matter             two smaller comparisons that vary the model rather than
which backend mined it.                                                 the method: a capability sweep inside one model family,
                                                                        and an agentic setting in which two frontier models mine
6.3    Component-test harness                                           whole specifications while directing their own process and
                                                                        tool use. Proposal validity uses the 197 proposals that gpt-
Validating a finding (§7.4) means checking whether two in-              5.4-mini delivers; of these, 40 are confirmed by static review
dependent implementations resolve the underspecification                of the two implementations, and the remaining 157 are au-
differently on production code. The harness compiles the                dited against the specification text by experts. Downstream
generated test against the pinned sources of OpenAirInter-              utility tests every delivered finding, from any LLM backend,
face [60] with its bundled FlexRIC [70], and srsRAN [73]. It            whose scenario the two implementations actually exercise;
then invokes the relevant handler in the tested process, and            60 of these confirm a divergence (§7.4). Feasibility compares
stubs the surrounding SCTP, MAC, RRC, and DU-manager                    the three backends head to head.
dependencies, so an observed divergence is attributed to                   Two of the studies rely on judgments rather than execu-
control-plane logic rather than to transport or timing. Cases           tion. Proposal validity is decided by two standards-literate
that end in a process abort run in a forked subprocess, and             experts. Effectiveness is scored by a deterministic check-
liveness cases advance a manual clock instead of waiting, so            list computed from each finding’s text and by two blinded
every test is deterministic and quick. All results are pinned           LLM judges from different model families (GPT-5.4 and
to fixed codebase commits.1 A smaller subset of findings is             DeepSeek-v4-Pro), which decide only concrete, checkable
   1 OpenAirInterface 09c9bb99, its bundled FlexRIC ef6d722f, and       properties rather than quality (Appendix E). Because the two
srsRAN 4bf15439.                                                        judges and the checklist agree, no conclusion rests on a sin-


                                                                    8
                                             S PEC L ENS       Naïve                Primary category                              Findings       Share
   Coverage and redundancy (deterministic)                                          Genuine underspecification                       244          46%
   Distinct sections touched         336                         287
                                                                                    Optionality read as a gap                         96          18%
   Distinct messages touched         127                         103
                                                                                    Deliberate policy freedom                         89          17%
   Repeated missing-rule findings    155                         269
                                                                                    Malformed input, not valid syntax                 38          7%
   Grounding and reach (blinded judge)                                              Delegated to another document                     30          6%
   Cite two or more sections          83%                       66%                 Editorial or reference defect                     27           5%
   Reviewer-ready                     88%                       68%                 Duplicate finding                                  6          1%
   Cross-step (temporal) finding      58%                       42%
                                                                                  Table 3: One primary category per finding for the 530 that gpt-5.6-sol and
Table 2: Discovery quality on 525 S PEC L ENS findings and 551 naïve-             claude-opus-5 mined agentically over the same six protocols.
prompting findings, pooled over the three backends. Judge rows are the pri-
mary judge; the second judge agrees (§7.2).
                                                                                  totypes, so the rounds converge on the same issue families:
                                                                                  seed similarity rises (0.67 against 0.64 for an unseeded con-
gle model’s opinion. Runtime divergence, in contrast, is de-                      trol) while within-round diversity falls (0.41 against 0.44).3
cided objectively by the compiled component tests of §6.3.                        Refinement constrains the answer space, while the taxonomy
                                                                                  shows the whole problem space.
7.2     Effectiveness against naïve prompting                                        The pipeline and the baseline use the same backend, so
                                                                                  the pipeline’s advantage cannot come from a stronger model;
The baseline is the obvious way to use an LLM: the same                           to confirm it comes from the workflow, we do a capabil-
procedure closure, a direct instruction to list the underspeci-                   ity sweep within one family, from gpt-5.4 nano to mini to
fications, and none of the taxonomy of Stage 2 (Figure 10).                       full, and run both at every tier (Table 8). The pipeline wins
We compare 525 findings from the S PEC L ENS pipeline                             on breadth, redundancy, and cross-step reach at every tier,
against 551 from naïve prompting, produced under all three                        and its run on the weakest model beats naïve prompting’s
backends and judged blind (§7.1). To keep the comparison                          run on the strongest: 50 to 60% of its findings using gpt-
fair, the pipeline findings are scored on their bare claim, the                   5.4-nano span several protocol steps, against about 30% for
same fields the baseline exposes. Table 2 collects the head-                      naïve prompting using gpt-5.4-full. A stronger model does
line results; Appendix E defines each instrument.                                 let naïve prompting ground itself, which closes the ground-
   The pipeline covers more of each protocol. It touches                          ing gap. However, it never explores the temporal cases suffi-
336 distinct specification sections and 127 distinct messages,                    ciently: its share holds near 30% from the smallest model to
against 287 and 103 for the baseline, and it does so while re-                    the largest, while the pipeline stays near 50% regardless of
peating itself less. Clustering findings by the protocol locus                    model. The gains are due to the workflow; a stronger back-
they name, 269 of the naïve findings only restate a missing-                      end lifts both without letting the naïve prompt catch up with
rule pattern already recorded at the same location, against                       the cases the taxonomy targets.
155 for the pipeline; the taxonomy keeps moving the model                            A second natural question is how well agentic mining does
to a fresh transition, whereas an open prompt falls back to                       with no scaffold at all. We give the naïve prompt of Fig-
one high-probability template, “optional IE absent, so behav-                     ure 10, unchanged, to two frontier models, gpt-5.6-sol [59]
ior is undefined,” instantiated per field.                                        and claude-opus-5 [12], with an entire specification as con-
   The judged metrics agree.2 The pipeline grounds each                           text and no imposed workflow: each decides how to proceed,
claim more densely, with 83% of findings citing two or                            writing scripts and calling tools. The 530 findings this pro-
more sections against 66%, and a larger share is reviewer-                        duces broaden the search and ground themselves about as
ready, meeting at least four of six concreteness criteria (Ap-                    densely as the pipeline does, so capability substitutes for part
pendix E): 88% against 68% under the first judge and 86%                          of what the workflow supplies, but not for the standard of
against 67% under the second. It also reaches more of the                         what counts. Assigning each finding one primary category
ordering and eventuality cases a local prompt tends to skip:                      against the cited text (Table 3), 244 are genuine underspeci-
58% against 42% under the first judge and 54% against 39%                         fications using the definition of §3, while 185 treat freedom
under the second.                                                                 the standard grants on purpose as a failure to specify: e.g.,
   Refining the baseline does not close the gap, as §4.2 pre-                     one calls QoS pre-emption underspecified while quoting the
dicted. Feeding a round’s well-grounded findings back as                          clause that makes the process operator-dependent.
few-shot examples steers the next round toward those pro-                            Beyond precision, agentic mining does poorly on recall.
                                                                                  In a four-procedure case study cross-checking 36 pipeline
   2 Every reviewer-ready and cross-step comparison reported in this sub-

section is significant at p < 10−6 by Fisher’s exact test.                           3 Appendix E gives the metrics.




                                                                              9
                              Gap      Fork      Total                                             NG F1 E1 E2 GTP-U E2SM Total
             Effect            24        71       95                          Validated cases 21 19 9                7       2          2       60
             Trigger           13        15       28
             Ordering           0        17       17                            Table 5: The 60 differential-test-validated divergences by protocol.
             Eventuality        3         2        5
             Total             40       105       145                        category and form. For instance, an effect gap is closed by
                                                                             adding a postcondition, a trigger gap by completing the re-
Table 4: The 145 unanimously accepted proposals by category and form.
                                                                             ceive table. Appendix F lists each underspecification pattern
                                                                             together with a draft repair template.
findings against the same models’ output, claude-opus-5 re-
covers 14 completely, while 22 are at best partial, naming                   7.4    Downstream utility: differential testing
the feature family but not the transition that makes a claim
reviewable. Capability thus broadens untriaged mining with-                  A proposal has downstream utility if two independently built
out disciplining or sharpening it. Appendix E details both the               implementations resolve the underspecification differently
breakdown of cross-checks and the missed findings.                           once the test runs. We compile every underspecification that
   These are the gains the decomposition predicts (§4). Turn-                both implementations exercise (from any LLM backend)
ing one open-ended request into bounded, located questions                   against the pinned OAI and srsRAN sources, and run it as
makes the search cover more transitions, repeat itself less,                 a software component test (§6.3).
and reach the temporal cases. An open-ended prompt results                      60 grouped cases produce a real divergence, spread across
in local completion. While a stronger model can match the                    all six protocols (Table 5; a full list is in Appendix G). By
grounding of our workflow, it cannot emulate our pipeline’s                  the observed outcome, 32 are conflicting actions such as ac-
breadth and temporal reach.                                                  cept versus reject; 16 are inconsistent internal states, exposed
                                                                             only by a later operation; and 12 are inconsistent notifica-
                                                                             tions. The findings are therefore not merely textual, and a
7.3    Proposal validity                                                     deployment that adds more implementations can only exac-
A proposal is valid if the underspecification it raises is gen-              erbate these divergences. The generated test designs carry
uinely unresolved by the normative text, not hallucinated. We                most of the weight, reducing the effort of writing manual
check the 197 proposals gpt-5.4-mini delivers in two ways.                   tests: of the 60, 37 run exactly as designed and 19 more keep
For 40 whose scenario both implementations exercise, static                  the generated trigger while adapting only the harness that
review confirms that they resolve it differently. The remain-                observes it for implementation specific reasons.
ing 157 were examined by two standards-literate experts,                        Stage 4 also predicts each finding’s impact class from the
who read each proposal against the cited specification and                   specification text alone, before any code runs. The prediction
marked it as an underspecification when no on-point state-                   is deliberately conservative, highlighting the worst outcome
ment in the specification settles it.                                        the text permits while two implementations often converge
   The experts accept the vast majority. Individually they ac-               on a milder one, so an exact match understates it: the worst-
cept 94.3% and 96.8% of the 157 proposals; together they                     outcome prediction matches 63% of the validated cases ex-
accept 145 unanimously (92.4%) and 155 with at least one                     actly, and the observed outcome falls within the engine’s full
vote (98.7%), and flag only 2 as false positives in common,                  predicted set for 72%. Since the prediction only ranks which
agreeing on 147 of the 157 (Appendix F). Folding in the                      findings to test first, highlighting potential severity is crucial.
40 confirmed by code-review, 185 of the 197 proposals are                       The divergences recur along one axis: OAI tends to toler-
conservatively supported, accepted by both experts or code-                  ate a stale item and proceed, to lack a liveness timer, or to
review, and 195 are supported by code or at least one expert,                reclaim state late. On the other hand, srsRAN validates up
so the proposals are well-grounded.                                          front, rejects, and bounds its waits. Several legal messages
   Because the accepted proposals carry a category and a                     reach an assertion that aborts the OAI or FlexRIC process.
form, they also indicate what repairing underspecification re-               The categories of §3.2 are thus not protocol-specific. We now
quires (Table 4). First, forks outnumber gaps roughly two                    describe two cases concretely; Appendix H provides more.
to one. Second, regardless of form, the under-constrained                    Releasing one session versus dropping the connection.
part is usually the effect (the resulting state or output) not               A PDU SESSION RESOURCE RELEASE COMMAND lets
the trigger or the ordering. Since the effect accounts for                   the core network tell a base station to free some of a device’s
95 of the 145 proposals, stating the post-state, output, and                 data sessions, each named by a PDU Session ID. The spec-
cleanup alone would address nearly two-thirds of underspec-                  ification gives no rule for a PDU Session ID that names a
ifications. The fixes fall into a few recurring patterns, one per            session which is not currently active, a stale or duplicated


                                                                        10
      Backend           cost ($) time (min) saturated runs/proc. costs a small bounded multiple of one mining pass rather
                                                                          than an open-ended budget. Combined with the per-proposal
  gpt-5.4-mini            0.38          1.84         36/36            4.7 cost, a full sweep of the six protocols costs tens of dollars.
claude-haiku-4.5 0.21                   0.52         36/36            3.3
                                                                             The backends do not, however, find the same things.
 gemini-3-flash           0.08          0.78         36/36            4.1
                                                                          Matched strictly by the deduplicator of §5.6 or leniently by a
                                                                          manual conceptual pass, only 5 to 17% of gaps are found by
Table 6: Cost, latency, and termination per backend. Cost and latency are
per delivered proposal, across the whole pipeline.                        all three, and 28 to 54% by at least two. How to combine the
                                                                          backends is therefore strategic: their union maximizes cover-
                                                                          age for a recall-oriented pre-release audit, their intersection
                                                                          maximizes precision for a fast high-confidence screen, and a
                                                                          single backend is the economical default for routine use.


                                                                        8    Generalizing to DNS
                                                                        Underspecification is a property of any standard that pairs
                                                                        a formal message syntax with natural-language procedures,
                                                                        not a feature of 5G, so we test it on the DNS RFCs. Port-
           Figure 5: Mining saturates within a few passes.              ing S PEC L ENS replaced under 10% of the workflow: the six
                                                                        stages ran unchanged, and the specification parser, prompt
                                                                        framing, and additive cross-RFC reference graph were the
entry that a live network produces routinely. OAI skips the             only substantive changes (Appendix I). We mine a hand-
stale ID and frees the sessions that remain, keeping the de-            ful of procedures across the RFC family and confirm each
vice attached; srsRAN rejects the whole command and tears               finding differentially on the Ferret testbed [41] against inde-
down the device’s entire context, every session and the sig-            pendent authoritative servers: BIND [37], Knot [24], Tech-
naling connection with it. The same message thus frees one              nitium [76], YADIFA [27], and Hickory DNS [33].
session on OAI and disconnects the device on srsRAN, and                   The pipeline surfaces genuine DNS underspecifications of
an attacker able to inject a single bogus PDU Session ID can            both forms of the taxonomy. We present one effect fork here
turn a routine release into a full disconnection.                       and give the rest in Appendix I. RFC 2136 [79] requires an
Keeping a conflicting identity versus reconciling it. A                 accepted update to advance the zone’s SOA serial number
DOWNLINK NAS TRANSPORT message names one sig-                           but does not fix the increment or granularity. RFC 1982 [25]
naling association by a pair of identifiers. The specification          allows any positive delta. Hence, one three-mutation update
gives no rule for a message whose AMF-UE-NGAP-ID is                     advanced the number by one on BIND and Knot and by three
already bound to a different RAN-UE-NGAP-ID, a stale or                 on Technitium. This carries less operational weight than the
spoofed pairing a live network can produce. OAI keys on                 5G findings, yet each is a genuine ambiguity the text leaves
the RAN-UE-NGAP-ID alone and leaves both pairings live;                 open. Note, however, that a DNS contract is spread across a
srsRAN reconciles them and returns an Error Indication. On              family of RFCs, so establishing that a gap is genuinely open
OAI the surviving pairing is a context-confusion primitive:             requires confirming that no sibling RFC closes it.
an attacker who injects one crafted pair can leave it standing,
so later signaling meant for that device can be delivered to
the wrong device.                                                       9    Related Work
7.5     Operational feasibility                                         Testing implementations against specifications. A large
                                                                        body of work checks an implementation against its speci-
To be usable at scale the workflow must be cheap, must ter-             fication. Conformance testing derives cases from the stan-
minate, and must run on whatever backend is at hand. All                dard [19, 84, 74, 28, 92], protocol fuzzing perturbs a live
three backends complete the full pipeline unchanged, which              stack [81, 52, 36, 95, 49], model-based testing generates
settles portability; Table 6 reports the rest. A delivered pro-         suites from a behavioral model [54], and differential and
posal costs cents, not dollars, from $0.08 on gemini to $0.38           parser-validation methods compare independent implemen-
on gpt-5.4-mini across the whole pipeline, and takes between            tations [94]. Closest to our domain, several frameworks test
half a minute and two minutes of wall time, the spread re-              5G and O-RAN interfaces and cores directly [75, 15, 87, 44].
flecting how much reasoning each model is configured to do.             These methods share one assumption: the specification is
   Mining runs are also bounded (Figure 5). All 36 saturate             the oracle of correct behavior, so a divergence is the im-
for all three backends, in 3 to 5 passes each, so a procedure           plementation’s fault. Studies of the specifications themselves


                                                                   11
show that assumption is not always safe [68, 66]. S PEC L ENS           scope one slice (Appendix H). What changes under a secu-
works upstream, asking whether the specification determines             rity framing is the criterion: an adversary asks which open-
a behavior at all and running differential tests to confirm a           ings a sender can exploit from outside, not which ones two
gap rather than to grade an implementation.                             receivers resolve differently. That is a different search over
Formalizing and analyzing specifications. A second line                 the same taxonomy; we only ran the second one.
of work builds formal models to verify protocol behavior, ei-           Across not within specifications:         S PEC L ENS reasons
ther constructing state machines by hand [14, 90, 64, 35] or            over a procedure closure inside a single document (§5.1), and
extracting them from prose with NLP and, more recently,                 that boundary is a choice we should relinquish. DNS forced
LLMs [7, 62, 91, 80, 89, 20]. Our approach descends from                the first step, since a DNS contract is spread over a family
the same lineage, communicating finite-state machines [17]              of RFCs; establishing that a gap is open means confirming
and the safety and liveness decomposition of a run [9], but             that no sibling RFC closes it (§8). 3GPP is the harder case:
put to a different use. Model checking over such a model can            one user-visible behavior spans NGAP, F1AP, E1AP, RRC,
flag an undefined transition [46], yet the finding is only as           and NAS at once, and error handling is routinely delegated
sound as the model, and building a faithful whole-protocol              across documents. 30 of the 530 findings mined agentically
model of a large, frequently revised specification is itself            already turn on a normative reference outside the document
the bottleneck (§4). S PEC L ENS never builds one: it reads             they came from (§7.2). The interesting claim is not that a
the partial state machine the specification already induces,            cross-document view finds more underspecifications. It ad-
one finding at a time. An LLM does the reading, but reading             mits a kind we cannot currently express, where no single
what a specification says is not finding what it fails to say, a        document is silent yet the hand-off between two of them is
task on which post-trained models are documented to do less             unclosed: each is complete on its own terms but their com-
well [45, 43, 78, 42, 77].                                              position is not.
Ambiguity and underspecification detection. Closest to                  State machine models: We chose communicating state
our paper is work that looks for imprecision in a specifica-            machines because they are the standard, minimal, and ex-
tion directly, though the term “ambiguity” is overloaded and            plainable account of a reactive protocol, and because the four
covers several distinct concepts (Figure 2). A sentence may             categories fall directly out of them (§3.2). The choice has a
admit more than one grammatical parse (syntactic) [88]; a               price, elaborated in Appendix A: data is folded into a finite
transition may be missing from a hand-built state machine               symbolic state, and duration is not represented at all. Other
(structural) [46]; a word may carry more than one meaning               lenses pay differently. An extended state machine adds con-
(lexical) [50, 86, 13]; two clauses may contradict or a refer-          text variables, guards, and update actions, so it models data
ence may dangle (logical) [66, 63]; a request may be open to            flow alongside control [21], and its communicating variant is
more than one reading of intent [53]; and analogous bench-              the direct successor to ours [16]. Under that lens several Ef-
marks target legal text [32, 47, 22]. All such earlier work tar-        fect findings stop being one merged state and become guard
gets something present, a token or structure with a signal to           and update questions the model can check, such as which of
key on. Semantic underspecification is the absence beneath              two flow descriptors sharing an identifier wins. Timed au-
the text, the level prior work has largely ignored.                     tomata [10] can express what runs cannot: deadlines, timers,
                                                                        and retry policy, where a visible share of our divergences
                                                                        live. The tradeoff is significant: a richer lens yields a finer
10     Open Questions                                                   taxonomy but a harder extraction problem, the model now
                                                                        having to recover variables, guards, and clocks from prose.
Scope:      S PEC L ENS targets standards that pair a for-
mal message syntax with natural-language procedures, not
deployment-oriented documents such as GSMA operational                  11     Conclusion
specifications [31]. It locates where the text leaves behavior
open (§3.3); automating the fix is an open problem. Because             Semantic underspecification is a structural blind spot in stan-
the expert-audit track validates findings against the text alone        dards that pair formal syntax with natural-language prose.
(§7.3), S PEC L ENS can act as a pre-release quality gate for           We addressed it by framing underspecification as a gap or
standards bodies.                                                       fork in a partially specified communicating state machine,
From interoperability to security: We have framed an                    and built S PEC L ENS to put that view in front of a language
opening as a vendor-interoperability hazard, but several val-           model as a scaffold. Across 36 5G procedures, our findings
idated findings are already exploitable: one crafted identifier         hold up under two independent checks, expert audit and dif-
pair plants a context-confusion primitive (§7.4); one legal             ferential testing. The same pipeline ports to DNS.
message reaches an assertion that ends a base-station pro-                 The scaffold earns its place for a reason that outlasts any
cess, and an under-constrained measurement filter can return            one model generation: more capable models can provide in-
every device a base station tracks to a subscription meant to           creased understanding, but not the criterion that decides what


                                                                   12
counts as an underspecification. Future models may simplify            References
scaffold construction but will still need our state machine
based (or related) classification. Further, our scaffolding is          [1] D. Eastlake 3rd. Domain Name System (DNS) IANA
already built; our results indicate more powerful models do                 Considerations. RFC 6895 (BCP 42), IETF, 2013.
not unearth more underspecifications.
                                                                        [2] 3rd Generation Partnership Project. 3gpp, 2025.
   Finally, state machine models are classically used as an ar-
tifact to build implementations. Our paper turns this around,           [3] 3rd Generation Partnership Project (3GPP). NG-RAN;
treating a formal model instead as a lens: this makes prose                 NG Application Protocol (NGAP). Technical Report
specifications analyzable at the scale they are written in com-             TS 38.413, 3rd Generation Partnership Project (3GPP),
plex modern protocols like 5G. Our taxonomy also fixes                      2020. Release 15, V15.8.0 (2020-07).
where formal verification takes over: S PEC L ENS outputs
each finding already localized, with competing completions              [4] 3rd Generation Partnership Project (3GPP). General
and a discriminating test that model-based testing [54] can                 Packet Radio System (GPRS) Tunnelling Protocol User
consume; one method finds where a model is worth building                   Plane (GTPv1-U). Technical Report TS 29.281, 3rd
and the other verifies what happens once it is.                             Generation Partnership Project (3GPP), 2021. Release
                                                                            16, V16.2.0 (2021-03).
                                                                        [5] 3rd Generation Partnership Project (3GPP). NG-RAN;
                                                                            E1 application protocol (E1AP). Technical Report
                                                                            TS 38.463, 3rd Generation Partnership Project (3GPP),
                                                                            2021. Release 16, V16.8.0 (2021-12).
                                                                        [6] 3rd Generation Partnership Project (3GPP). NG-RAN;
                                                                            F1 application protocol (F1AP). Technical Report TS
                                                                            38.473, 3rd Generation Partnership Project (3GPP),
                                                                            2025. Release 16, V16.21.0 (2025-03).
                                                                        [7] Abdullah Al Ishtiaq, Sarkar Snigdha Sarathi Das, Syed
                                                                            Md Mukit Rashid, Ali Ranjbar, Kai Tu, Tianwei Wu,
                                                                            Zhezheng Song, Weixuan Wang, Mujtahid Akon, Rui
                                                                            Zhang, et al. Hermes: Unlocking security analysis of
                                                                            cellular network protocols by synthesizing finite state
                                                                            machines from natural language specifications. In 33rd
                                                                            USENIX Security Symposium (USENIX Security 24),
                                                                            pages 4445–4462, 2024.
                                                                        [8] P. Almquist. Type of Service in the Internet Protocol
                                                                            Suite. RFC 1349, IETF, 1992. Obsoleted by RFC 2474.
                                                                        [9] Bowen Alpern and Fred B. Schneider. Defining live-
                                                                            ness. Information Processing Letters, 21(4):181–185,
                                                                            1985.
                                                                       [10] Rajeev Alur and David L. Dill. A theory of timed au-
                                                                            tomata. Theoretical Computer Science, 126(2):183–
                                                                            235, 1994.
                                                                       [11] Anthropic.  Claude Haiku 4.5.     https://www.
                                                                            anthropic.com/claude/haiku, 2025.
                                                                       [12] Anthropic. Claude Opus 5. https://www.anthropic.
                                                                            com/claude/opus, 2026.
                                                                       [13] Atul Bansal, Veronica Muriga, Jason Li, Lucy Duan,
                                                                            and Swarun Kumar. Can we make fcc experts out of
                                                                            llms? In Proceedings of the 26th International Work-
                                                                            shop on Mobile Computing Systems and Applications,
                                                                            pages 85–90, 2025.


                                                                  13
[14] David Basin, Jannik Dreier, Lucca Hirschi, Saša                      Jul 1992. https://groups.csail.mit.edu/ana/
     Radomirovic, Ralf Sasse, and Vincent Stettler. A for-                People/DDC/future_ietf_92.pdf.
     mal analysis of 5g authentication. In Proceedings of
     the 2018 ACM SIGSAC conference on computer and                  [24] CZ.NIC. Knot DNS. Open-source authoritative DNS
     communications security, pages 1383–1396, 2018.                      server software.

[15] Nathaniel Bennett, Weidong Zhu, Benjamin Simon,                 [25] R. Elz and R. Bush. Serial Number Arithmetic. RFC
     Ryon Kennedy, William Enck, Patrick Traynor, and                     1982, IETF, 1996. Proposed Standard.
     Kevin RB Butler. Ransacked: A domain-informed                   [26] R. Elz and R. Bush. Clarifications to the DNS Specifi-
     approach for fuzzing LTE and 5G RAN-core inter-                      cation. RFC 2181, IETF, 1997. Proposed Standard.
     faces. In Proceedings of the 2024 ACM SIGSAC Con-
     ference on Computer and Communications Security,                [27] EURid vzw/asbl. YADIFA. Open-source authoritative
     pages 2027–2041, 2024.                                               DNS server software.

[16] Chourouk Bourhfir, Rachida Dssouli, El Mostapha                 [28] Jonas Fridén, Sam Agneessens, Aidin Razavi, Aurelian
     Aboulhamid, and Nathalie Rico. A guided incremen-                    Bria, and Torbjörn Elfström. 5g over-the-air confor-
     tal test case generation procedure for conformance test-             mance testing. In 2020 14th European Conference on
     ing for CEFSM specified protocols. In Proc. IFIP TC6                 Antennas and Propagation (EuCAP), pages 1–5. IEEE,
     11th Int. Workshop on Testing Communicating Systems                  2020.
     (IWTCS), pages 275–290, 1998.
                                                                     [29] Fyodor. Remote OS detection via TCP/IP stack finger-
[17] Daniel Brand and Pitro Zafiropulo. On communicating                  printing. Phrack Magazine, 8(54), 1998.
     finite-state machines. Journal of the ACM, 30(2):323–
                                                                     [30] Google DeepMind. Gemini 3 Flash. https://
     342, 1983.
                                                                          deepmind.google/models/gemini/flash/, 2025.
[18] CERT Coordination Center. IP denial-of-service at-
                                                                     [31] GSMA. GSMA operational specifications, 2025.
     tacks. CERT Advisory CA-97.28, Carnegie Mellon
     University Software Engineering Institute, Dec 1997.            [32] Dan Hendrycks, Collin Burns, Anya Chen, and Spencer
[19] Yi Chen, Di Tang, Yepeng Yao, Mingming Zha, Xi-                      Ball. Cuad: An expert-annotated nlp dataset for legal
     aoFeng Wang, Xiaozhong Liu, Haixu Tang, and Baoxu                    contract review. In Proceedings of the Neural Informa-
     Liu. Sherlock on specs: Building {LTE} confor-                       tion Processing Systems Track on Datasets and Bench-
     mance tests through automated reasoning. In 32nd                     marks (NeurIPS Datasets and Benchmarks), 2021.
     USENIX Security Symposium (USENIX Security 23),                 [33] Hickory DNS Project. Hickory DNS (formerly Trust-
     pages 3529–3545, 2023.                                               DNS). Open-source DNS server software written in
[20] Yi Chen, Yepeng Yao, XiaoFeng Wang, Dandan Xu,                       Rust.
     Chang Yue, Xiaozhong Liu, Kai Chen, Haixu Tang, and             [34] P. Hoffman and K. Fujiwara. DNS Terminology. RFC
     Baoxu Liu. Bookworm game: Automatic discovery of                     9499 (BCP 219), IETF, 2024.
     lte vulnerabilities through documentation analysis. In
     2021 IEEE Symposium on Security and Privacy (SP),               [35] Kaiyu Hou, You Li, Yinbo Yu, Yan Chen, and Hai
     pages 1197–1214. IEEE, 2021.                                         Zhou. Discovering emergency call pitfalls for cellular
                                                                          networks with formal methods. In Proceedings of the
[21] Kwang-Ting Cheng and A. S. Krishnakumar. Auto-                       19th Annual International Conference on Mobile Sys-
     matic functional test generation using the extended fi-              tems, Applications, and Services, pages 296–309, 2021.
     nite state machine model. In Proc. 30th Design Au-
     tomation Conference (DAC), pages 86–91, 1993.                   [36] Changze Huang, Di Wang, and Zhi Quan Zhou. Llm-
                                                                          assisted model-based fuzzing of protocol implementa-
[22] Manan Roy Choudhury, Adithya Chandramouli, Man-                      tions. arXiv preprint arXiv:2508.01750, 2025.
     nan Anand, and Vivek Gupta. Better call clause: A dis-
     crepancy benchmark for auditing llms legal reasoning            [37] Internet Systems Consortium. BIND 9. Open-source
     capabilities. In Findings of the Association for Com-                DNS server software.
     putational Linguistics: EACL 2026, pages 5776–5818,
                                                                     [38] ISO/IEC. Information Processing Systems – Open
     2026.
                                                                          Systems Interconnection – Estelle: A Formal Descrip-
[23] David D. Clark.     A cloudy crystal ball: Visions                   tion Technique Based on an Extended State Transition
     of the future.    Plenary presentation, 24th Inter-                  Model. Technical Report ISO 9074, International Or-
     net Engineering Task Force (IETF), Cambridge, MA,                    ganization for Standardization, 1989.


                                                                14
[39] ISO/IEC. Information Processing Systems – Open Sys-                 bugs: Large language model assisted fuzzing of mat-
     tems Interconnection – LOTOS: A Formal Description                  ter IoT devices. In 33rd USENIX Security Symposium
     Technique Based on the Temporal Ordering of Obser-                  (USENIX Security 24), pages 4783–4800, 2024.
     vational Behaviour. Technical Report ISO 8807, Inter-
     national Organization for Standardization, 1989.               [50] Taslim     Mahbub,    Dana      Dghaym,     Aadhith
                                                                         Shankarnarayanan, Taufiq Syed, Salsabeel Shap-
[40] ITU-T.      Specification and Description Language                  sough, and Imran Zualkernan. Can gpt-4 aid in
     (SDL). Technical Report Recommendation Z.100, In-                   detecting ambiguities, inconsistencies, and incom-
     ternational Telecommunication Union, 1993.                          pleteness in requirements analysis? a comprehensive
                                                                         case study. IEEE Access, 2024.
[41] Siva Kesava Reddy Kakarla, Ryan Beckett, Todd Mill-
     stein, and George Varghese. SCALE: Automatically               [51] Kim Martineau and IBM Research. Why larger LLM
     finding RFC compliance bugs in DNS nameservers. In                  context windows are all the rage. https://research.
     19th USENIX Symposium on Networked Systems De-                      ibm.com/blog/larger-context-window, Jul 2024.
     sign and Implementation (NSDI 22), pages 307–323,                   Accessed 2026-07-25.
     2022.
                                                                    [52] Ruijie Meng, Martin Mirchev, Marcel Böhme, and Ab-
[42] Adam Tauman Kalai, Ofer Nachum, Santosh S. Vem-                     hik Roychoudhury. Large language model guided pro-
     pala, and Edwin Zhang. Why language models hallu-                   tocol fuzzing. In Proceedings of the 31st Annual
     cinate. arXiv preprint arXiv:2509.04664, 2025.                      Network and Distributed System Security Symposium
                                                                         (NDSS), volume 2024, 2024.
[43] Subbarao Kambhampati. Can large language models
     reason and plan? Annals of the New York Academy of             [53] Rajdeep Mondal, Nikolaj Bjorner, Todd Millstein, Alan
     Sciences, 1534(1):15–18, 2024.                                      Tang, and George Varghese. Tackling ambiguity in user
                                                                         intent for llm-based network configuration synthesis. In
[44] Abderaouf Khichane, Ilhem Fajjari, Nadjib Aitsaadi,                 Proceedings of the 24th ACM Workshop on Hot Topics
     and Mourad Gueroui. 5gc-analyser: Demistifying the                  in Networks, pages 176–183, 2025.
     5g core network through statistical analysis. In ICC
     2024-IEEE International Conference on Communica-               [54] Rajdeep Mondal, Rathin Singha, Todd Millstein,
     tions, pages 3682–3688. IEEE, 2024.                                 George Varghese, Ryan Beckett, and Siva Ke-
                                                                         sava Reddy Kakarla. Eywa: Automating model-based
[45] Robert Kirk, Ishita Mediratta, Christoforos Nalmpan-                testing using llms. In 23rd USENIX Symposium on
     tis, Jelena Luketina, Eric Hambro, Edward Grefen-                   Networked Systems Design and Implementation (NSDI
     stette, and Roberta Raileanu. Understanding the ef-                 26), May 2026.
     fects of RLHF on LLM generalisation and diversity. In
                                                                    [55] K. Nichols, S. Blake, F. Baker, and D. Black. Defini-
     International Conference on Learning Representations
                                                                         tion of the Differentiated Services Field (DS Field) in
     (ICLR), 2024. arXiv:2310.06452.
                                                                         the IPv4 and IPv6 Headers. RFC 2474, IETF, 1998.
[46] Daniel Klischies, Moritz Schloegel, Tobias                          Proposed Standard. Obsoletes RFC 1349.
     Scharnowski, Mikhail Bogodukhov, David Rup-
                                                                    [56] O-RAN Alliance. O-ran.wg3.e2ap-r003-v03.00: O-ran
     precht, and Veelasha Moonsamy. Instructions unclear:
                                                                         e2 application protocol (e2ap). Technical specification,
     undefined behaviour in cellular network specifications.
                                                                         O-RAN Alliance, 2022. v03.00 (2022-11).
     In 32nd USENIX Security Symposium (USENIX
     Security 23), pages 3475–3492, 2023.                           [57] O-RAN Alliance. O-ran.wg3.e2sm-kpm-r003-v03.00:
                                                                         O-ran e2 service model (e2sm), kpm. Technical speci-
[47] Yuta Koreeda and Christopher D Manning. Contractnli:
                                                                         fication, O-RAN Alliance, 2022. v03.00 (2022-11).
     A dataset for document-level natural language infer-
     ence for contracts. In Findings of the Association             [58] OpenAI. GPT-5.4-mini. https://platform.openai.
     for Computational Linguistics: EMNLP 2021, pages                    com/docs/models, 2026.
     1907–1919, 2021.
                                                                    [59] OpenAI. GPT-5.6 Sol. https://openai.com/index/
[48] E. Lewis. The Role of Wildcards in the Domain Name                  gpt-5-6/, 2026.
     System. RFC 4592, IETF, 2006. Proposed Standard.
                                                                    [60] OpenAirInterface Software Alliance.   Openair-
[49] Xiaoyue Ma, Lannan Luo, and Qiang Zeng. From                        interface 5g.   https://openairinterface.org/
     one thousand pages of specification to unveiling hidden             oai-5g-ran-project/.


                                                               15
[61] O-RAN Alliance. O-ran alliance, 2025.                            [72] Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao,
                                                                           Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch,
[62] Maria Leonor Pacheco, Max von Hippel, Ben Wein-                       Adam R Brown, Adam Santoro, Aditya Gupta, Adrià
     traub, Dan Goldwasser, and Cristina Nita-Rotaru. Au-                  Garriga-Alonso, et al. Beyond the imitation game:
     tomated attack synthesis by extracting finite state ma-               Quantifying and extrapolating the capabilities of lan-
     chines from protocol specification documents. In 2022                 guage models. Transactions on machine learning re-
     IEEE Symposium on Security and Privacy (SP), pages                    search, 2023.
     51–68. IEEE, 2022.
                                                                      [73] srsRAN. srsRAN – open source ran. https://www.
[63] Mrigank Pawagi, Lize Shao, Hyeonmin Lee, Yixin                        srsran.com/.
     Sun, and Wenxi Wang. Rfcscope: Detecting logical
     ambiguities in internet protocol specifications. In 2025         [74] Xikai Sun, Fan Dang, Shiqi Jiang, Jingao Xu, Ke-
     40th IEEE/ACM International Conference on Auto-                       bin Liu, Xin Miao, Zihao Yang, Weichen Zhang,
     mated Software Engineering (ASE), pages 1234–1246.                    Haimo Lu, Yawen Zheng, and Yunhao Liu. ipanda:
     IEEE, 2025.                                                           An llm-based agent for automated conformance test-
                                                                           ing of communication protocols.     arXiv preprint
[64] Aleksi Peltonen, Ralf Sasse, and David Basin. A com-
                                                                           arXiv:2507.00378, 2025.
     prehensive formal analysis of 5g handover. In Pro-
     ceedings of the 14th ACM conference on security and              [75] Sixu Tan, Zeyu Li, Zhutian Liu, Harsh Patel, and
     privacy in wireless and mobile networks, pages 1–12,                  Zhaowei Tan. Automated model-based fuzzing for
     2021.                                                                 5g o-ran. In Proceedings of the 31st Annual Interna-
                                                                           tional Conference on Mobile Computing and Network-
[65] Margaret H. Pinson et al. 5g challenge prelimi-
                                                                           ing, pages 201–215, 2025.
     nary event: Evaluating modular, interoperable, multi-
     vendor, open ran solutions. Technical Memorandum                 [76] Technitium Software. Technitium DNS Server. Open-
     TM-23-568, National Telecommunications and Infor-                     source DNS server software.
     mation Administration (NTIA), 2023.
                                                                      [77] Thinh Hung Truong, Timothy Baldwin, Karin Ver-
[66] Mirza Masfiqur Rahman, Imtiaz Karim, and Elisa                        spoor, and Trevor Cohn. Language models are not
     Bertino. CellularLint: A systematic approach to iden-                 naysayers: An analysis of language models on negation
     tify inconsistent behavior in cellular network specifica-             benchmarks. In Proceedings of the 12th Joint Confer-
     tions. In 33rd USENIX Security Symposium (USENIX                      ence on Lexical and Computational Semantics (*SEM),
     Security 24), pages 5215–5232, 2024.                                  2023. arXiv:2306.08189.
[67] K. Ramakrishnan, S. Floyd, and D. Black. The Addi-
                                                                      [78] Karthik Valmeekam, Matthew Marquez, Alberto Olmo,
     tion of Explicit Congestion Notification (ECN) to IP.
                                                                           Sarath Sreedharan, and Subbarao Kambhampati. Plan-
     RFC 3168, IETF, 2001. Proposed Standard.
                                                                           Bench: An extensible benchmark for evaluating large
[68] Muhammad Taqi Raza and Songwu Lu. A system-                           language models on planning and reasoning about
     atic way to lte testing. In The 25th Annual Interna-                  change. In Advances in Neural Information Processing
     tional Conference on Mobile Computing and Network-                    Systems (NeurIPS), Datasets and Benchmarks Track,
     ing, pages 1–15, 2019.                                                2023. arXiv:2206.10498.

[69] Samsung Electronics Co., Ltd. Overcoming challenges              [79] P. Vixie, S. Thomson, Y. Rekhter, and J. Bound. Dy-
     of multi-vendor open ran. White paper, Samsung Net-                   namic Updates in the Domain Name System (DNS UP-
     works, 2020.                                                          DATE). RFC 2136, IETF, 1997. Proposed Standard.

[70] Robert Schmidt, Mikel Irazabal, and Navid Nikaein.               [80] Fares Wael, Youssef Maklad, Ali Hamdi, and Wael
     FlexRIC: an SDK for next-generation SD-RANs. In                       Elsersy. An agentic flow for finite state machine extrac-
     Proceedings of the 17th International Conference on                   tion using prompt chaining. In 2025 Intelligent Meth-
     emerging Networking EXperiments and Technologies                      ods, Systems, and Applications (IMSA), pages 328–
     (CoNEXT), pages 411–425, 2021.                                        333. IEEE, 2025.

[71] Prakhar Sharma and Vinod Yegneswaran. Prosper: Ex-               [81] Jincheng Wang, Le Yu, and Xiapu Luo. Llmif: Aug-
     tracting protocol specifications using large language                 mented large language model for fuzzing iot devices. In
     models. In Proceedings of the 22nd ACM Workshop                       2024 IEEE Symposium on Security and Privacy (SP),
     on Hot Topics in Networks, pages 41–47, 2023.                         pages 881–896. IEEE, 2024.


                                                                 16
[82] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel,               [92] Ping Zhang, Xiaoli Yang, Jianqiao Chen, and Yuzhen
     Barret Zoph, Sebastian Borgeaud, Dani Yogatama,                      Huang. A survey of testing for 5g: Solutions, op-
     Maarten Bosma, Denny Zhou, Donald Metzler, et al.                    portunities, and challenges. China Communications,
     Emergent abilities of large language models. Transac-                16(1):69–85, 2019.
     tions on Machine Learning Research, 2022.
                                                                     [93] Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and
[83] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten                     Sameer Singh. Calibrate before use: Improving few-
     Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.                shot performance of language models. In Interna-
     Chain-of-thought prompting elicits reasoning in large                tional Conference on Machine Learning (ICML), 2021.
     language models. Advances in neural information pro-                 arXiv:2102.09690.
     cessing systems, 35:24824–24837, 2022.
                                                                     [94] Mingwei Zheng, Danning Xie, and Xiangyu Zhang.
[84] Yunze Wei, Kaiwen Chi, Shibo Du, Xiaohui Xie, Ziyu                   Large language models for validating network protocol
     Geng, Yuwei Han, Zhen Li, Zhanyou Li, and Yong Cui.                  parsers. In 2025 IEEE Security and Privacy Workshops
     Large language model driven automated network pro-                   (SPW), pages 56–64. IEEE, 2025.
     tocol testing. In Proceedings of the 2025 Applied Net-
     working Research Workshop, pages 32–38, 2025.                   [95] Ming Zhong, Zisheng Zeng, Yijia Guo, Dandan Zhao,
                                                                          Bo Zhang, Shenghong Li, Hao Peng, and Zhiguo Ding.
[85] B. Wellington. Secure Domain Name System (DNS)                       Intelligent test case generation method for fuzzing iot
     Dynamic Update. RFC 3007, IETF, 2000. Proposed                       protocols based on llm. Automated Software Engineer-
     Standard.                                                            ing, 33(1):6, 2026.
[86] Frank Wildenburg, Michael Hanna, and Sandro
                                                                     [96] Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
     Pezzelle. Do pre-trained language models detect and
                                                                          Nathan Scales, Xuezhi Wang, Dale Schuurmans,
     understand semantic underspecification? ask the dust!
                                                                          Claire Cui, Olivier Bousquet, Quoc Le, and Ed Chi.
     In Findings of the Association for Computational Lin-
                                                                          Least-to-most prompting enables complex reasoning
     guistics: ACL 2024, pages 9598–9613, 2024.
                                                                          in large language models. In International Con-
[87] Tianchang Yang, Syed Md Mukit Rashid, Ali Ranjbar,                   ference on Learning Representations (ICLR), 2023.
     Gang Tan, and Syed Rafiul Hussain. ORANalyst: Sys-                   arXiv:2205.10625.
     tematic testing framework for open RAN implementa-
     tions. In 33rd USENIX Security Symposium (USENIX
     Security 24), pages 1921–1938, 2024.
[88] Jane Yen, Tamás Lévai, Qinyuan Ye, Xiang Ren,
     Ramesh Govindan, and Barath Raghavan. Semi-
     automated protocol disambiguation and code genera-
     tion. In Proceedings of the 2021 ACM SIGCOMM 2021
     Conference, pages 272–286, 2021.
[89] Shiyu Yuan, Jingda Yang, Sudhanshu Arya, Carlo Lip-
     izzi, and Ying Wang. From ambiguity to explicit-
     ness: Nlp-assisted 5g specification abstraction for for-
     mal analysis. In 2023 IEEE 12th International Confer-
     ence on Cloud Networking (CloudNet), pages 229–237.
     IEEE, 2023.
[90] Jingjing Zhang, Qiang Wang, Lin Yang, and Tao Feng.
     Formal verification of 5g-eap-tls authentication pro-
     tocol. In 2019 IEEE fourth international conference
     on data science in cyberspace (DSC), pages 503–509.
     IEEE, 2019.
[91] Miao Zhang, Runhan Feng, Hongbo Tang, Yu Zhao, Jie
     Yang, Hang Qiu, and Qi Liu. Automated extraction of
     protocol state machines from 3gpp specifications with
     domain-informed prompts and llm ensembles. arXiv
     preprint arXiv:2510.14348, 2025.


                                                                17
A      A Communicating State-Machine                                            The step relation generates finite behaviors, but a protocol
                                                                             behavior is a set of complete runs. Under linear-time trace se-
       Model                                                                 mantics a run property decomposes into a safety part, which
This appendix expands the state-machine view of §3.1. It                     finite prefixes are allowed, and a liveness part, what must
gives the run semantics the main text abbreviates, restates                  eventually happen [9]. This is the temporal layer. Ordering
gap and fork over that semantics, and states the test that sep-              is the safety side, constraining which interleavings of firings
arates underspecification from questions the model cannot                    are allowed, and Eventuality is the liveness side, constrain-
answer.                                                                      ing obligations that no finite prefix can refute. Concurrency
                                                                             makes Ordering nontrivial, and loops make Eventuality non-
                                                                             trivial. The four components are exhaustive because a run-set
A.1     Communicating state machines                                         is a temporal arrangement of firings over transitions with lo-
A protocol of n roles is a tuple P = ⟨(Si ), (oi ), (Mi j ), (δi )⟩.         cal content, and independent because each can vary while the
For each role i, Si is a finite set of local states with initial             others are fixed.
state oi ∈ Si , and for each ordered pair i ̸= j, Mi j is the set of
messages i may send to j. A role acts by sending or receiving.               A.4     Scope: specified, underspecified, or out-
Writing −m for sending m and +m for receiving it, the local                          side the model
transition relation is
                                                                             Not every behavioral question is one the model can answer.
δi ⊆ Si ×Ai ×Si ,       Ai = {−m : m ∈ Mi j }∪{+m : m ∈ M ji }.              A question is in scope exactly when its answer is a property
                                                                             of the run-set Rspec : any two specifications that generate the
   A global configuration γ = (s,C) records every role’s local
                                                                             same runs must answer it the same way. An in-scope ques-
state s = (s1 , . . . , sn ) and the contents C = (Ci j ) of the FIFO
                                                                             tion is specified when one rule applies and underspecified
channels, each Ci j ∈ Mi∗j . The initial configuration γ0 = (o, ε)
                                                                             when it is a gap or a fork. It is out of model when its an-
places every role in its initial state with empty channels. The
                                                                             swer can differ between two specifications that generate the
step relation ⇒ is the usual one: a send appends m to Ci j
                                                                             very same runs, in which case no slot in the model records it.
and advances the sender, and a receive consumes m from the
                                                                             The one-line test is whether the answer could change without
head of C ji and advances the receiver. A run is a sequence
                                                                             adding, removing, or reordering any run.
γ0 ⇒ γ1 ⇒ · · · , and the behavior of the protocol is the set R
                                                                                Three familiar questions fall outside it, one per standing
of runs from γ0 .
                                                                             assumption. Whether a choice is committed early or late is
                                                                             branching-time, and two specifications can resolve it differ-
A.2     Specifications as partial machines                                   ently while permitting the same runs. Whether a reply meets
                                                                             a deadline is real-time, and runs record order rather than du-
A natural-language specification rarely determines a unique
                                                                             ration. Distinctions the abstraction has already merged are
complete protocol. It may omit a case, permit several read-
                                                                             invisible to it, so scope is always relative to that abstraction.
ings, or leave a progress obligation implicit, so we read it as
inducing a partial, possibly nondeterministic relation δi ,
                                                            spec                Two refinements decide the live cases. A gap counts only
whose runs form the set Rspec . A conformant implementa-                     under reachability: some run must reach the configuration
tion is a deterministic refinement: it chooses concrete transi-              that exposes it, or the missing rule changes no behavior. And
tions within what the specification allows, δi
                                              impl     spec
                                                   ⊆ δi , un-                the model cannot judge intent: text loose enough to admit
der the chosen abstraction. Underspecification is any place                  incompatible readings may be so by design rather than by
where Rspec is left open, so that two conformant refinements                 oversight, so the model locates the opening and names its
may disagree.                                                                form while a human decides whether to close it or to docu-
                                                                             ment it.

A.3     Local and temporal under-constraint
Fix a reachable local state si and an admissible action a ∈ Ai ,
                                                                             B     Key prompts (abridged)
and let
                                                                             Each pipeline stage (§5) is a single text-in, typed-JSON-
              spec                                    spec
             ∆i (si , a) = { s′i : (si , a, s′i ) ∈ δi }.                    out call. Figures 6–9 give the load-bearing parts of four of
                                                                             them; boilerplate, output schemas, and quoting limits are
                                       spec
The step is well specified when |∆i (si , a)| = 1, a gap when                elided, and the full templates will be included in the planned
the set is empty, and a fork when it holds two or more ele-                  code release. The CFSM framing is carried verbatim into the
ments. This is the local layer, and it splits a transition into its          prompts, and the impact verdict is not asked of the model at
Trigger, whether a rule applies to (si , a) at all, and its Effect,          all: it is computed by the deterministic engine over the frag-
which next state and output the rule yields.                                 ment the model extracts. Figure 10 gives the naïve baseline


                                                                        18
 SYSTEM: You are a rigorous 3GPP/O-RAN control-plane analyst. You                  SYSTEM: You decide the *form* of an underspecification: whether
 model a specification as a communicating finite-state machine                     the spec is silent (Gap) or permits several alternatives (Fork),
 (CFSM) and hunt for places where the spec leaves the run-set                      in CFSM run-set terms.
 under-constrained.
                                                                                   Consider the set Delta of behaviors the spec permits at the
 Model the procedure as communicating state machines exchanging                    under-constrained transition or temporal property:
 messages; a transition is (state, +message) -> (state', emitted                   - Gap (|Delta| = 0): no rule applies / no eventual obligation
 output), and an underspecification is an under-constraint of the                    stated. A design defect; the specification itself should be
 run-set they generate.                                                              fixed.
 - Message/IE tables give syntax only. Assume syntax is valid.                     - Fork (|Delta| >= 2): more than one compliant behavior is
 - Behavioral text is where behavior should be pinned down,                          allowed, possibly deliberate vendor latitude. The remedy is to
   often silently.                                                                   test / document / tighten.
 - The 3GPP criticality mechanism (reject/ignore/notify) is                        Intent: you can locate a fork but cannot decide whether it was
   syntax-level error handling, NOT a semantic validator; it does                  meant. Record the read in intent_note without treating it as
   not resolve a behavioral gap.                                                   decisive.

 [LOCAL pass] Mine ONLY the content of a single transition:
 - Trigger: a reachable state where it is unclear whether a                       Figure 7: Stage 3, gap/fork triage (abridged): |∆| = 0 (Gap) versus |∆| ≥ 2
   message is handled, more than one rule could apply, or a guard
   is never stated.                                                               (Fork).
 - Effect: a message is accepted but the resulting state
   update, response, or outcome is left open or reads two
   contradictory ways.
                                                                                   SYSTEM: You extract a small, faithful partial CFSM fragment from
 [TEMPORAL pass] Mine ONLY the arrangement of firings, and gate                    the actual spec text and formalize each candidate behavior as a
 first:                                                                            transition. You never invent rules the spec does not support;
 - Ordering applies only if the procedure admits concurrency /                     when something cannot be grounded in the text, leave that field
   overlap.                                                                        empty rather than guessing.
 - Eventuality applies only if a run can fail to make progress
   (loop, retry, pending obligation nothing forces to occur).                      - A transition is (state, action) -> (next_state, outputs);
 If neither precondition holds, return an empty findings array.                      action is +MSG/-MSG.
                                                                                   - specified_transitions: only transitions the spec actually
 Reachability: report a finding only if the exposing                                 pins down. For every pair of completions ending in different
 configuration is plausibly reachable; give a concrete run.                          next_states, include >= 1 downstream transition that later
 Prefer consequential over latent cases. Cite involved {messages,                    reads those states and behaves differently for each -- the
 ies, sections}; argue reachability inline.                                          engine uses these to test whether the divergence is
                                                                                     observable. A missing one makes a real divergence look latent.
                                                                                   - exposing_config.reach_trace: a concrete event sequence to
                                                                                     the exposing configuration (the reachability witness). slot:
Figure 6: Stage 2, taxonomy-based mining (abridged): two scoped calls,               the (process, state, action) the spec leaves open, with its
local and temporal, the temporal one gated on applicability before mining.           form.
                                                                                   - Do NOT rank severity; it is computed mechanically
                                                                                     downstream.
                                                                                   Field contract: decision in {accept, reject, ignore,
of §7.2, which shares these inputs and output schema but                           no_progress}; progresses is a boolean; outputs and reach_trace
                                                                                   are arrays of strings.
withholds the framing.

                                                                                  Figure 8: Stage 4, CFSM model extraction (abridged): the model builds the
C      End-to-end testbed validation                                              fragment and formalizes the narratives; it never grades severity.


The component tests of §6.3 isolate the control-plane logic
under test. To confirm that the divergences also surface in                       GTP-U (TS 29.281).             Echo Request, Echo Response, G-
a running network, we reproduced six of them end to end.                          PDU.
Two RAN implementations, OpenAirInterface and srsRAN,
ran on a workstation with an Intel Xeon W5-3435X and                              NGAP (TS 38.413). PDU Session Resource Setup, Mod-
64 GB of DDR5 memory under Ubuntu 22.04, each attached                            ify, and Release; Initial Context Setup; UE Context Release;
to its 5G core. For each finding we encoded the trigger with                      Paging; Initial UE Message; Downlink and Uplink NAS
pycrate, filled abstract fields such as transaction identifiers                   Transport; NG Setup; UE Radio Capability Info Indication.
from the live session, injected it over SCTP with pysctp, and                     E1AP (TS 38.463). gNB-CU-UP E1 Setup; Bearer Con-
read the response from console logs and returned messages.                        text Setup, Modification, and Release.
Table 7 lists the six reproduced cases; each corresponds to a                     F1AP (TS 38.473). Reset; F1 Setup; gNB-DU and gNB-
confirmed divergence in Appendix G.                                               CU Configuration Update; UE Context Setup, Release, and
                                                                                  Modification; Initial UL, DL, and UL RRC Message Trans-
                                                                                  fer; Paging.
D      Evaluated procedures                                                       E2AP. RIC Subscription, RIC Subscription Delete, RIC
The 36 evaluated procedures, those that both OpenAirInter-                        Indication, RIC Control, E2 Setup.
face and srsRAN implement, are listed below by specifica-                         E2SM-KPM. Periodic Report; common condition-based
tion.                                                                             UE-level measurement.


                                                                             19
 SYSTEM: You turn a formal differential-test plan into a                              Underspecification exercised                       Protocol
 concrete, executable interoperability test, preserving the
 plan's branch expectations and discrimination method.                                Inconsistent CU/DU UE-ID pair in a                 F1AP
 You are given a DETERMINISTIC plan (setup, trigger, branches,                        partial F1 RESET
 discriminator) derived from the finding's CFSM model. Concretize                     Duplicate or already-active PDU Ses-               NGAP
 it: 1. Realize SETUP as concrete messages/IEs that reach the
 exposing configuration. 2. Send the TRIGGER, with mandatory IEs                      sion ID during concurrent setup
 and the test-critical IEs that exercise the under-constraint. 3.                     PDU Session ID reused while its release            NGAP
 For EACH branch, give the concrete expected observable,
 consistent with that branch's decision / expected_outputs /                          is still pending
 next_state. Do not invent branches. 4. Implement the                                 Unknown PDU Session ID in a RE-                    NGAP
 DISCRIMINATOR exactly as planned: observe_decision,
 downstream_probe, compare_notifications, or observe_progress.                        LEASE COMMAND
 Symbolic labels come from the model; map them to real message/IE                     Downlink NAS identifiers resolving no              NGAP
 names. You must NOT alter the branch expectations or the
 discrimination method.                                                               live UE association
                                                                                      E2 Setup outcome with no matching                  E2AP
                                                                                      live transaction
Figure 9: Stage 5, test concretization (abridged): the plan is fixed upstream;
the model fills in concrete IE values only.
                                                                                             Table 7: The six divergences reproduced on the live testbed.

 SYSTEM: You are a rigorous 3GPP/O-RAN specification analyst.
                                                                                       gpt 5.4 nano / mini / full          S PEC L ENS            Naïve
 You audit 3GPP/O-RAN RAN control-plane specifications for
 underspecification. A specification is underspecified at a point                      Temporal reach (judge 2)   50 / 45 / 51    44 / 29 / 33
 where its syntax is well defined (the messages and information
 elements are declared, and it is clear what parses) but the
                                                                                       Temporal reach (judge 1)   60 / 45 / 53    37 / 25 / 30
 intended behavior is left open: the text does not pin down what                       Messages per 100 findings 75 / 100 / 53 63 / 68 / 34
 an implementation must actually do. Two implementations can then
 both follow the specification and still behave differently.
                                                                                       Repeats per finding       .20 / .15 / .27 .33 / .18 / .44
                                                                                       Cite two or more sections 95 / 95 / 100 33 / 100 / 100
 # Task Read the specification context below and report every
 underspecification you can find in it.
                                                                                      Table 8: Capability progression on a five-procedure microbenchmark
 # Breadth & uniqueness Report all distinct underspecifications                       (§7.2). Rows are percentages, except repeats per finding (a [0, 1] rate).
 you can justify (0..N; there is no target count). Ensure unique
 titles; anchor each with the concrete section numbers it occurs
 in and short supporting quotes.
                                                                                      F1AP worst at 20 of 86, where 57 of 86 are deliberate policy
Figure 10: The naïve baseline for Stage 2 (§7.2), abridged. Its inputs and
                                                                                      freedom or plain optionality. Delegation is the other recur-
output schema match the miner of Figure 6, but everything the frame-                  ring misread: one finding calls GTP-U path failure undefined
work contributes is withheld: no CFSM framing, no Trigger/Effect/Order-               while quoting the clause that hands it to a procedure in an-
ing/Eventuality taxonomy, no gap/fork form, and no reachability argument.             other document.
Only a one-paragraph definition and an open-ended instruction to list every
underspecification remain.                                                            What agentic mining misses. Table 3 counts what agen-
                                                                                      tic mining reports; a second audit asks what it fails to re-
                                                                                      port. We took four procedures whose pipeline reports align
E      Effectiveness: instruments and re-                                             cleanly with the chat outputs, F1AP UE Context Setup,
                                                                                      NGAP PDU Session Resource Setup, E2AP RIC Subscrip-
       sults                                                                          tion, and E2SM-KPM Periodic Report, and cross-checked
                                                                                      each of the 36 pipeline findings against both models’ output,
Reviewability checklist. A blinded finding is scored on                               counting it fully recovered only when the chat finding could
six concrete criteria: (1) it is bounded to the cited mate-                           substitute for it in a review package. gpt-5.6-sol recovers 12
rial; (2) it names both a message and an information ele-                             fully and 17 partially and misses 7; claude-opus-5 recovers
ment; (3) it cites two or more sections; (4) it supplies two                          14 and 13 and misses 9. Taking the better of the two per find-
or more evidence quotes; (5) it has at least six concrete an-                         ing, 14 of 36 are fully recovered, 22 are at best partial, and
chors in total; and (6) it is judged highly actionable. A find-                       5 of those are missed by both. The misses give one exam-
ing meeting at least four criteria is reviewer-ready. The first                       ple per category of §3.2: an SRB ID of 0 the receive proce-
five criteria are deterministic; only actionability uses a judge.                     dure never gives meaning to and a repeated QoS Flow Iden-
On a deterministic-only variant of the score the pipeline is                          tifier in one request; a Serving NID the receive path need not
reviewer-ready for 81% of findings against 59% for naïve.                             store and ordinary SRB setup success that is never reported;
Agentic mining, per protocol and per model. Of the                                    a conditional-handover replacement whose prepared target is
530 findings behind Table 3, gpt-5.6-sol produced 269 and                             absent; and a periodic-report trigger nothing forces to fire.
claude-opus-5 261, judged genuine at 41% and 51%. The                                 Redundancy metric. Clustering findings by the proto-
spread by protocol is far wider: E2AP best at 62 of 97,                               col locus they name, a repeat is any finding that only re-


                                                                                 20
expresses a missing-rule pattern already recorded at that lo-          G     Confirmed divergences by protocol
cus, the “optional IE absent, so behavior is undefined” tem-
plate instantiated per field. The raw count is 155 for the             The 60 confirmed divergences of §7.4 are listed below,
pipeline against 269 for naïve; the repeats per finding row            grouped by protocol. Each entry names the underspeci-
of Table 8 divides it by the backend’s number of findings,             fication, then how OpenAirInterface (OAI) and srsRAN
and lower means less templating. Both are deterministic and            resolve it with a code location, and the severity as ob-
use no judge.                                                          served / predicted: CA (Conflicting Actions), IIS (Inconsis-
Reach. A finding is cross-step, the temporal reach row of              tent Internal States), or IN (Inconsistent Notifications). Lo-
Table 8 and the cross-step row of Table 2, when a blinded              cations are file:line in the pinned revisions of §6.3.
judge labels it Ordering or Eventuality (interleaving, retry,          NGAP (gNB peer).
timeout, liveness, late or duplicate handling) rather than a
single local step.                                                      • Conflicting UE-ID pair in DL NAS Transport. OAI
Iterative few-shot. The few-shot sub-experiment is 18                     keys by RAN-UE-ID only and retains the stale context
runs: three backends, three procedures, treatment and con-                (ngap_gNB_nas_procedures.c:334); srsRAN releases
trol, four rounds each. Treatment seeds round N+1 with                    the old context and emits an Error Indication. CA / CA
prior rounds’ curated findings; control runs the identical loop         • Unknown PDU Session ID in RELEASE COM-
with no exemplars. The similarity and diversity gaps of §7.2              MAND. OAI skips the ID, keeping the UE (rrc_gNB_
are measured on the raw pre-deduplication generations, and                NGAP.c:1922); srsRAN rejects the whole command
hold in 6 of 8 and 7 of 8 pairs respectively. Both treatment              and releases the entire UE (pdu_session_resource_
and control mode-collapse: about 80% of what rounds 2 to                  release_routine.cpp:194). CA / CA
4 generate is already a duplicate. Count-based metrics are              • Duplicate / already-active PDU Session ID in SETUP.
run-to-run noisy and we draw no conclusions from them.                    OAI fails all, then admits the fresh ID (rrc_gNB_NGAP.
                                                                          c:908); srsRAN fails the duplicate and admits the fresh
                                                                          ID atomically (ngap_validators.cpp:42). CA / CA
F     Expert audit and repair patterns                                  • One infeasible QoS flow among feasible ones in
                                                                          MODIFY. OAI keeps the session, skipping the bad
Repair patterns. The 40 gaps among the 145 unanimous                      flow (rrc_gNB_NGAP.c:1082); srsRAN fails the whole
proposals cluster into three fixes: complete the postcondition            PDU session (up_resource_manager_helpers.cpp:
(24 Effect gaps, a shall rule fixing the next state, output, or           388). CA / CA
cleanup), complete the receive table (13 Trigger gaps, requir-          • MODIFY releasing the last flow of a session. OAI re-
ing accept, reject, ignore, or error for the omitted input and            claims the emptied DRB, reporting success (rrc_gNB_
state), and close the lifecycle (3 Eventuality gaps, a timer or           NGAP.c:1029); srsRAN rejects the whole request (up_
retry bound and a terminal state). The 105 forks cluster into             resource_manager_helpers.cpp:174). CA / IIS
four: pin the effect or expose the choice (71 Effect forks),            • Preferred UP security with no mandated treatment.
make guards mutually exclusive (15 Trigger forks), define                 OAI emits no Security Result; srsRAN reports protection
atomicity and happens-before (17 Ordering forks), and re-                 not-performed. IN / CA
quire termination (2 Eventuality forks).
                                                                        • Two QoS flows with the same QFI. OAI keeps the first
Drafting templates. Each pattern maps to a normative                      descriptor, srsRAN the last. IIS / CA
template:
                                                                        • NG SETUP FAILURE Time-to-Wait, no retry pol-
 • Gap / Trigger. “Upon receiving M in state S, the node                  icy. OAI reads only the cause and never retries (ngap_
   shall A; if C is false, it shall B and enter S′ .”                     gNB_handlers.c:96); srsRAN waits the delay and re-
 • Gap / Effect. “After accepting M, the node shall update                tries (ng_setup_procedure.cpp:120). IIS / IIS
   X, emit Y , and remove or retain Z.”                                 • Late / duplicate NG SETUP RESPONSE. OAI re-
 • Fork / Effect. “The node shall use behavior A. If B is sup-            counts, incrementing the association counter (ngap_gNB_
   ported, support shall be negotiated by C; absence of C                 handlers.c:305); srsRAN drops it via the transaction
   means A.”                                                              sink (ng_setup_procedure.cpp:60). IIS / CA
 • Fork / Ordering. “A shall complete before B; simultane-              • RELEASE COMMAND for an unknown UE con-
   ous events resolve in favor of A; failure rolls back X but             text. OAI silently drops (ngap_gNB_handlers.c:878);
   retains Y .”                                                           srsRAN drops and emits an Error Indication (ngap_
 • Eventuality. “If no response arrives within T , the node               impl.cpp:702). IN / CA
   shall retry at most N times and then enter terminal state            • Replayed RELEASE COMMAND after release
   St while emitting E.”                                                  scheduled. OAI silently drops; srsRAN emits Error In-


                                                                  21
   dication interaction-with-other-proc (ngap_impl.                    polls forever (gnb_config.c:2699); srsRAN times
   cpp:722). IN / IN                                                   out at 3000 ms (f1ap_du_setup_procedure.cpp:35).
 • ICS FAILURE cause on a DU-originated setup                          CA / CA
   failure. OAI’s CU handler is unimplemented and aborts             • DU state after F1 SETUP FAILURE with Time-
   (f1ap_cu_ue_context_management.c:65); srsRAN                        to-Wait. OAI calls exit(1) (mac_rrc_dl_handler.
   emits ICS Failure with protocol/unspecified                         c:196); srsRAN waits and retries (f1ap_du_setup_
   (initial_context_setup_routine.cpp:62). CA / IN                     procedure.cpp:128). CA / IIS
 • UE Context RELEASE REQUEST cause selection.                       • Unsupported new gNB-CU UE F1AP ID in DL
   OAI hard-codes radio-connection-lost (rrc_gNB.c:                    RRC transfer. OAI keeps the old binding (f1ap_rrc_
   2681); srsRAN maps the DU’s F1AP cause (f1ap_                       message_transfer.c:373); srsRAN rebinds to the new
   cause_converters.cpp:29). IN / IN                                   ID (f1ap_du_impl.cpp:270). IIS / IIS
 • RELEASE COMPLETE payload composition. OAI                         • Paging DRX / Priority optional hints. OAI drops
   never attaches User Location Information, srsRAN al-                both for the cell default (f1ap_paging.c:214); srsRAN
   ways (ue_context_release_routine.cpp:55). IN / IN                   preserves DRX for paging-frame selection (paging_
 • Invalid UE security capabilities plus PDU-session                   scheduler.cpp:144). IIS / IIS
   setup. OAI continues into per-session setup; srsRAN               • Full-vs-delta CellGroupConfig when a source
   emits ICS Failure naming the session. CA / CA                       config exists. OAI omits Full Configuration
 • Unknown local UE ID on Initial Context Setup.                       (mac_rrc_dl_handler.c:615); srsRAN emits it
   OAI emits ICS Failure; srsRAN emits Error Indication                (ue_configuration_procedure.cpp:351). IN / IN
   unknown-local-UE-ID. IN / CA                                      • Measurement-gap creation discretionary after Meas-
 • RELEASE COMMAND NAS forwarding vs tear-                             Config. OAI creates no gap (mac_rrc_dl_handler.c:
   down ordering. OAI defers cleanup to the release re-                683); srsRAN derives a gap from SMTC1 (du_meas_
   sponse; srsRAN releases the NAS first. IIS / IIS                    config_manager.cpp:99). IN / IN
 • Unsupported REROUTE NAS REQUEST. OAI’s de-                        • Transmission stop/restart transition point undefined.
   coder default aborts the CU (ngap_gNB_decoder.c);                   OAI defers via a timeout, staying schedulable (mac_
   srsRAN drops the message gracefully. CA / IIS                       rrc_dl_handler.c:892); srsRAN disconnects DRBs
 • Uplink NAS before the AMF association exists. OAI                   before the Response (du_ue_controller_impl.cpp:
                                                                       274). IIS / IIS
   forwards without the AMF-ID guard; srsRAN drops until
   the association exists. CA / CA                                   • RRC delivery not ordered against teardown in RE-
                                                                       LEASE COMMAND. OAI runs a delivery-blind 100 ms
 • Duplicate Initial UE Message while first association
   pending. OAI can emit a second Initial UE Message;                  timer (mac_rrc_dl_handler.c:973); srsRAN awaits
   srsRAN suppresses it. CA / CA                                       the delivery callback or 120 ms (f1ap_du_ue_context_
                                                                       release_procedure.cpp:64). IIS / IIS
 • Released-list duplicate canonicalization. OAI dedupli-
   cates by internal session; srsRAN drops duplicate entries.        • Per-item semantics of a partial-F1 RESET. OAI
   IN / IN                                                             aborts on any partial RESET (f1ap_du_interface_
                                                                       management.c); srsRAN resolves the UE and ACKs
F1AP (CU ↔ DU).                                                        (f1ap_du_impl.cpp:156). CA / IIS
                                                                     • Unmodeled optional IEs in GNB-CU CONFIGURA-
 • GNB-CU CONFIGURATION UPDATE with PCI
                                                                       TION UPDATE. OAI’s decoder models a subset and
   omitted. OAI flattens PCI to zero and aborts on an asser-
                                                                       drops the message; srsRAN ignores the IE and ACKs
   tion (f1ap_interface_management.c:1751); srsRAN
                                                                       (f1ap_cu_impl.cpp). IIS / IIS
   projects the CGI only and ACKs (cu_configuration_
   procedure.cpp:53). CA / IIS                                       • Dedicated-SI list in GNB-DU CONFIGURA-
                                                                       TION UPDATE. OAI default-rejects and drops
 • SRB ID = 0 in UE CONTEXT MODIFICATION. OAI
                                                                       (f1ap_interface_management.c:1584);            srsRAN
   passes SRB0 to the RLC guard and asserts (mac_rrc_
                                                                       ignores contents and ACKs (f1ap_cu_impl.cpp:266).
   dl_handler.c:209); srsRAN maps 0 to SRB0 and re-
                                                                       IIS / IIS
   turns success. CA / CA
                                                                     • Receive-state precondition for GNB-DU CONFIGU-
 • F1 SETUP REQUEST with the optional gNB-DU
                                                                       RATION UPDATE. OAI requires a bound DU, drop-
   Name absent. OAI proceeds to Setup Response (f1ap_
                                                                       ping otherwise (rrc_gNB_du.c:987); srsRAN ACKs un-
   interface_management.c:790); srsRAN fails setup
                                                                       conditionally. IIS / CA
   (f1_setup_procedure.cpp:37). CA / CA
                                                                     • CU System Information in F1 SETUP RESPONSE.
 • No timeout when F1 Setup is unanswered. OAI


                                                                22
   OAI applies the CU-owned SIBs at the DU (f1ap_                    context_release_procedure.cpp:43). IIS / IIS
   interface_management.c:662); srsRAN reads only                  • Admitted PDU session with zero successful child
   the CGI. IIS / IIS                                                DRBs. OAI reports both DRBs successful; srsRAN re-
 • Old gNB-DU UE F1AP ID on release, RRC container                   ports parent success with DRB failures. CA / CA
   absent. OAI retains the old context; srsRAN schedules           • Duplicate CU-CP UE E1AP ID in Bearer Context
   its removal (f1ap_du_impl.cpp:187). IIS / IIS                     Setup. OAI reuses the CU-UP UE ID; srsRAN allocates
 • Paging Cell List not validated against served cells.              a fresh one, keeping two contexts. IIS / CA
   OAI never inspects the list; srsRAN validates each cell         • Contradictory inactivity-monitoring configuration.
   and pages none if unmatched (f1ap_du_impl.cpp:587).               OAI returns SETUP RESPONSE; srsRAN returns
   IIS / IIS                                                         SETUP FAILURE. CA / CA
 • Absent DU-to-CU RRC container on reestablish-                   • Rejection granularity for an unsupported child re-
   ment. OAI has no reject gate and proceeds (rrc_gNB.c:             source. OAI reports the child successful; srsRAN reports
   1435); srsRAN rejects the reestablishment. CA / CA                a parent failure. CA / IIS
E2AP (E2 node; OAI’s E2 agent is FlexRIC).                         • Storage scope when multiple PLMNs carry distinct
 • RIC Control Ack Request extension ordinal. FlexRIC                child lists. OAI has no NR-CGI support field and loses
   asserts the value is ACK and aborts (msg_handler_                 that scope; srsRAN retains PLMN, slice, and NR-CGI
   agent.c:246); srsRAN’s decoder rejects the extension              per item. IIS / CA
   value (e2ap.h:2783). CA / CA                                    • Success response when preferred UP confidentiality is
 • Whether the RAN Function ID must match on sub-                    not performed. OAI omits the Security Result; srsRAN
   scription delete. FlexRIC ignores the key miss and                emits not-performed. IN / CA
   keeps the subscription (msg_handler_agent.c:200);               • Local reaction to a wrong-role first CU-UP Setup
   srsRAN keys by requestor only and erases it (e2_                  PDU. OAI’s global dispatch forwards it to the CU-CP
   subscription_manager_impl.cpp:88). IIS / CA                       path; srsRAN’s role-scoped ingress drops it. CA / IN
 • Optional Call Process ID in RIC CONTROL AC-                    GTP-U.
   KNOWLEDGE. FlexRIC sets it to NULL (msg_
                                                                   • Header-only container G-PDU with a zero-length T-
   handler_agent.c:270); srsRAN echoes the request
                                                                     PDU. OAI guards callbacks on size and delivers noth-
   field (e2_ric_control_procedure.cpp:72). IN / CA
                                                                     ing (gtp_itf.cpp:1188); srsRAN extracts the empty T-
 • No retry/abort bound when E2 Setup is unan-                       PDU and calls up (gtpu_tunnel_nru_rx_impl.h:52).
   swered. FlexRIC retransmits forever on a 3 s timer                IIS / IIS
   (e2_agent.c:474); srsRAN’s transaction expires (e2_
                                                                   • Unknown comprehension-required extension header.
   setup_procedure.cpp:80). CA / IN
                                                                     OAI skips the extension, delivering the T-PDU (gtp_
 • Subscription DELETE for no matching subscrip-                     itf.cpp:1217); srsRAN’s comprehension check drops
   tion. FlexRIC returns success; srsRAN returns DELETE              the G-PDU. CA / IN
   FAILURE. CA / CA
                                                                  E2SM-KPM.
 • Unsupported RIC SUBSCRIPTION MODIFICA-
   TION REQUEST. FlexRIC’s dispatch guard aborts the               • Boolean guard over a Style-4 Matching Condition
   agent; srsRAN declines without crashing. CA / CA                  list. OAI evaluates each condition, suppressing the re-
                                                                     port on an empty one (ran_func_kpm.c:338); srsRAN’s
 • Post-setup state for functions omitted from the Ac-               matcher is a stub, reporting every tracked UE (e2sm_
   cepted list. FlexRIC still services them via its plugin           kpm_du_meas_provider_impl.cpp:223). CA / IIS
   registry; srsRAN promotes only Accepted-list functions.
   CA / CA                                                         • Receive rule for an unsupported Measurement ID.
                                                                     OAI admits, then aborts during reporting; srsRAN rejects
E1AP (CU-CP ↔ CU-UP).                                                at admission. CA / CA
 • No progress rule if CU-CP never answers CU-UP E1
   Setup. OAI has no response timer and pends (e1ap.
   c:500); srsRAN sets a 3000 ms deadline, then a fatal           H     Additional 5G case studies
   setup error (e1ap_cu_up_setup_procedure.cpp:33).
   CA / CA                                                        A single message that aborts a base station. The physi-
 • CU-CP cleanup after BEARER CONTEXT RE-                         cal cell identity is optional in GNB-CU CONFIGURATION
   LEASE COMPLETE. OAI does no cleanup on Com-                    UPDATE. Omitted for an already-configured cell, OAI flat-
   plete, reclaiming later (rrc_gNB.c:3356); srsRAN re-           tens it to zero, compares it with the configured value, and
   moves the E1 UE context immediately (bearer_                   reaches an assertion that ends the process; srsRAN keeps its


                                                             23
local value and acknowledges. One legal message thus aborts             DNS metadata fields and entry points, and drop the intent-
the OAI distributed unit, a remotely triggerable denial of ser-         judgment language from triage. The larger effort was addi-
vice.                                                                   tive: cross-RFC reference-graph ingestion, corpus indexing,
An under-constrained measurement filter. E2SM-KPM                       and DNS planning, validation, and audit are new modules,
Report Style 4 scopes UE-level measurements by a Match-                 not edits to the 5G path. We run the findings differentially on
ing Condition list, but fixes no Boolean guard over it: neither         the Ferret testbed [41] across BIND [37], Knot [24], Techni-
how conditions combine nor what a condition matching no                 tium [76], YADIFA [27], and Hickory DNS [33].
device means. OAI evaluates item by item and suppresses the             QCLASS NONE in a standard query (Trigger, Gap).
whole report once any condition matches nothing; srsRAN’s               RFC 6895 registers class value 254 as QCLASS NONE, a
matcher does not evaluate the list and returns every device it          value meaningful in queries and updates [1], and RFC 2136
tracks. The empty-match and combination semantics are the               gives it a meaning only inside UPDATE prerequisite and
gap, and srsRAN’s non-evaluation compounds it: a subscrip-              update sections [79]. No RFC defines how an authorita-
tion meant to scope one slice can receive measurements for              tive server processes an OPCODE=QUERY question carry-
every device tracked.                                                   ing it, and RFC 9499 still describes a query as a name,
A final message that one implementation may drop. On                    type, and class without a rule for this class [34]. The mes-
UE Context Release the specification does not order RRC                 sage decodes, so the opening is at transition selection. On
delivery against teardown. OAI arms a delivery-blind 100 ms             a query for the name www.campus.edu. of type A, BIND
timer and can delete the UE before the final RRC message is             returns FORMERR, Knot REFUSED, Technitium REFUSED
delivered; srsRAN waits for the delivery callback or 120 ms.            with recursion-available set, YADIFA NOTIMP, and Hick-
A last RRCRelease carrying a redirect can therefore be lost             ory DNS NOERROR with the IN record 192.0.2.50, four in-
on OAI under load: the network treats the UE as released                compatible outcomes for one syntactically valid message.
while the UE never receives its redirect.                               Ordinary clients query class IN, so the case bears on robust-
Silent QoS-policy divergence. A PDU session setup with                  ness rather than a demonstrated production failure. Hickory
two flows carrying the same QoS identifier has no receive               DNS returning IN data for a non-IN question is the sharper
rule. OAI commits the first descriptor and srsRAN the last,             edge, since DNS classes are separate namespaces [1], though
and both return success, so the same request installs different         we do not show that answer entering a cache.
QoS on the two implementations. A UE’s flow is enforced at              SOA serial increment granularity (Effect, Fork).
one QoS class on OAI and another on srsRAN, and neither                 RFC 2136 §3.6 requires an accepted update that does not
the core network nor the operator is told the two disagree.             itself change the SOA serial to advance it automatically
A subscription one implementation keeps and the other                   before the change becomes visible, and it lists several
erases.     On a RIC subscription delete carrying a mis-                permissible triggering events without mapping one update
matched function identifier, FlexRIC does not find the en-              message or one mutation to one serial unit [79]. RFC 1982
try yet returns success, leaving the subscription live; srsRAN          §3.1 defines advancement as addition of any positive
erases it. Both first responses are identical, so a static read-        integer [25], and RFC 3007 §1.1 requires an increment but
ing would conclude the implementations agree. The desync                no scheme [85]. Measuring each server’s serial immediately
appears only later, when a controller that believes a subscrip-         before and after one accepted update that adds an A record,
tion gone still receives indications from FlexRIC.                      adds a TXT record, and deletes an A record: BIND and Knot
                                                                        advance from 3 to 4, a delta of one; Technitium advances
                                                                        from 6 to 9, a delta of three; YADIFA rejects the update and
I    DNS Generalization                                                 is not a witness. The before measurement removes a setup
                                                                        confound, since Technitium’s import had already advanced
This appendix backs the DNS case study of §8: the adapta-               its serial to 6. Ordinary resolution is unaffected, since a
tion footprint, the RFC bases and per-server outcomes be-               secondary checks only whether the serial is newer. Stateful
hind the findings we present, and the family-level filter we            automation is not: a client that reads the serial, updates, and
apply before treating a divergence as a finding. We report              reuses the predicted value in a later exact-serial prerequisite
these findings as case studies and do not claim a complete              succeeds under a per-transaction policy and fails under a
count.                                                                  per-mutation one.
Adaptation footprint. The tracked S PEC L ENS workflow                  Duplicate add with a different TTL (Effect, Fork). Here
is about 4,770 lines of code and 777 lines of prompt text.              the opening is a conflict between clauses rather than silence.
Adapting it to DNS replaced about 26 lines of code, roughly             For a zone record host1.campus.edu. of type A at TTL 300,
0.5%, and 40 to 50 lines of prompt text, roughly 5 to 6%,               an accepted update adds the same owner, class, type, and data
for some 1.2 to 1.4% of the tracked workflow overall. The               at TTL 60. RFC 2136 §1.1.1 excludes TTL from RR equal-
workflow edits are mechanical: thread a domain flag through             ity and §2.5.1 says duplicate additions are silently ignored,
the existing stages, switch prompt rendering by domain, add             which preserve TTL 300, while §3.4.2.2 says a duplicate-


                                                                   24
RDATA add replaces the zone RR with the update RR, which
installs TTL 60 [79]. BIND and YADIFA install 60; Knot
and Technitium keep 300. RFC 2181 §5 forbids the mixed-
TTL and duplicate state but does not select which TTL sur-
vives this update [26]. The normative text points two ways,
so implementations diverge; we report it as an effect fork,
with the caveat that its source is a contradiction, so no im-
plementation can honor both clauses at once. This case car-
ries the clearest operational consequence. Operators lower
a TTL before changing an address, so if the duplicate add
is ignored, a cutover takes effect later than the management
system expects and a desired-state controller reissuing the
change never converges on the preserving servers. Deleting
and re-adding the RRset avoids this, but the portability gap
remains.
Filtering against the RFC family. Because a DNS con-
tract spans several RFCs, some candidate divergences close
once the whole family is read; we exclude them. Whether
a same-message add and delete of one record leaves it
present or absent is fixed by the in-order processing rule
of RFC 2136 §3.4.2 [79], so a server that diverges there is
nonconformant rather than exercising a gap. We also do not
count gaps an RFC itself flags as undefined, such as the se-
mantics of a wildcard-owned NS RRset, which RFC 4592
§4.2 leaves explicitly open [48]; these are real but already
acknowledged, so they are weak as discoveries.




                                                                25
