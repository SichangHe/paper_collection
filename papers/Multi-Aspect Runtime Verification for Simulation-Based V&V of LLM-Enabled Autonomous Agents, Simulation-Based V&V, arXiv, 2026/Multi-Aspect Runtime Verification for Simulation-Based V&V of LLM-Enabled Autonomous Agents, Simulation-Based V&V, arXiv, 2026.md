                                                   Multi-Aspect Runtime Verification for
                                                          Simulation-Based V&V
                                                   of LLM-Enabled Autonomous Agents⋆

                                             Nikolaos Kekatos1 , Dimitrios Nikou2 , Anastasios Temperekidis1 , Alexios
                                              Lekidis3 , Nikolaos Kolokotronis4 , Panagiotis Katsaros5 , and Stylianos
                                                                           Basagiannis2
                                                                        1
                                                                         Clone Systems, Cyprus
                                                               2
                                                                International Hellenic University, Greece
arXiv:2610.08928v1 [cs.CR] 6 Oct 2026




                                                                   3
                                                                      University of Thessaly, Greece
                                                                 4
                                                                    University of Peloponnese, Greece
                                                             5
                                                               Aristotle University of Thessaloniki, Greece



                                                Abstract. LLM-based agents are entering decision-support roles in de-
                                                fence staff work, where the obligations they must respect are already
                                                written down and already binding, and where retraining is not available
                                                as a control because models arrive as procured components on a vendor
                                                update cadence. What can be placed under engineering control is the
                                                interface between the agent and the systems it acts on. Those obliga-
                                                tions are at once spatial (where data and actions may reside), temporal
                                                (in what order, within what windows), and text-semantic (what is read,
                                                said, or acted upon). A single tool call rarely violates anything. The
                                                violation lives in the composition of a multi-step interaction, which is
                                                why per-event guardrails miss sequential tool-attack chains that succeed
                                                on frontier models. We present a multi-aspect runtime-verification frame-
                                                work that decomposes a natural-language policy clause into a typed triple
                                                ⟨φS , φT , φΣ ⟩ over one canonical event stream, checks each aspect with
                                                its own monitoring specification, and fuses the verdicts through a four-
                                                valued algebra that carries provenance. The spatial aspect is interpreted
                                                over a weighted two-sorted location graph in which mission geometry and
                                                information-release topology are one object, so a single monitor decides
                                                both where an effect may land and where a record may travel. We show
                                                that these spatial obligations are not in general subsumed by a first-
                                                order temporal specification, since containment is the transitive closure
                                                of a runtime-mutable edge relation. The past-time aspect runs on the
                                                unmodified MonPoly engine, which agrees with our reference monitor at
                                                every time point. Across two mission domains, casualty evacuation and
                                                contested sustainment, and one civil domain, composition under the pre-
                                                cautionary blocking policy drives attack success to zero with no observed
                                                false positives and microsecond-scale per-event cost, while every single
                                                aspect and every pair leaves a substantial share of attacks succeeding. In
                                                a closed-loop experiment a policy-naive planner reaches a violating state
                                        ⋆
                                            This is a preprint of an article accepted for publication in Modelling and Simulation
                                            for Autonomous Systems (MESAS 2026), Springer LNCS.
2      N. Kekatos et al.

      in most unshielded missions and in none when shielded, and four refused
      episodes in five still recover to a compliant outcome. Every blocked action
      ships an auditable, clause-grounded verdict.

      Keywords: Runtime verification · LLM agents · Agent safety · Compo-
      sitional monitoring · Past-time temporal logic · Trustworthy AI · V&V
      of autonomous systems



1   Introduction

Large language models are moving into decision-support roles inside military
staff work [28,7,23]. The U.S. Department of Defense catalogued generative-
AI use cases across fifteen areas spanning command and control and decision
support, and stood up a dedicated fielding effort to accelerate them [28]; its
Thunderforge programme puts LLM-based agents into campaign development,
course-of-action generation, wargaming and resource allocation, with initial mis-
sion partners at two combatant commands [7]. NATO’s revised AI strategy ad-
dresses generative AI directly and calls for an Alliance-wide testing, evaluation,
verification and validation capability to support responsible adoption [23]. That
last point is the gap this paper addresses.
     Defence adoption changes the verification problem rather than merely enlarg-
ing it. A staff agent operates under obligations that are already written down and
already binding: rules of engagement, classification and release policy, targeting
law, and the protections that attach to medical and humanitarian activity. These
are not preferences to be traded against utility, and an operator who accepts a
recommendation inherits responsibility for it, so a system that cannot say which
obligation it checked and on what evidence cannot be held to account after the
fact. The same adoption also removes the option of retraining as a control: mod-
els arrive as procured components, are updated on a vendor cadence, and are
deployed into coalition settings where the releasing authority and the consuming
command differ. What can be placed under engineering control is the interface
between the agent and the systems it acts on, which is where a monitor sits. This
is the capability NATO’s strategy asks for, applied at the level of the individual
action rather than the model.
     Why put a language model in this loop at all is a fair question, and the an-
swer bounds what we claim. The inputs are unstructured language: evacuation
requests, spot reports, clearance traffic, manifests written under time pressure.
Turning those into a tasking that respects marking, routing, sharing and reten-
tion rules is a matching and sequencing problem over text, which is difficult to
cover exhaustively with fixed rules. What the agent does with that is propose
and order tool calls; nothing here puts a model between a sensor and an actuator,
and the consequential actions it can request are mediated calls that an executor
still performs. The assurance argument does not require agreeing that such an
agent should be fielded. If it is, these obligations are what it must not violate;
if the judgement is that it stays advisory, the same mechanism is what makes
                   Multi-Aspect Runtime Verification of LLM-Based Agents         3

advisory enforceable, since an advisory system that can open a release channel
is not advisory in the sense that matters.
    This work asks whether consequential actions of tool-using LLM agents can
be prevented from reaching policy-violating states when compliance depends
jointly on spatial state, temporal history and semantic content. Such an agent
calls tools, moves data, designates points on the ground and commits the organ-
isation to actions with legal consequences, under obligations of several kinds at
once: spatial, where an effect lands and where a record may travel; temporal, in
what order and inside which window; and text-semantic, what a narrative field
says as opposed to what a structured field claims.
    The difficulty is that these obligations are rarely broken by any one action.
A tool call inspected in isolation is almost always admissible; the violation lives
in the composition of a multi-step interaction. This is exactly the regime in
which per-event guardrails fail by construction, and it is the regime attackers
have found: sequential tool-attack chains succeed against frontier models at rates
above 90% [20], and per-call policy layers such as AgentSpec [29], Progent [25],
GuardAgent [30] and constrained-action proxies for security operations [18] can-
not see a violation that no single call exhibits.
    Runtime verification is the natural response, and mature engines exist for
each aspect in isolation: stream-based monitors such as TeSSLa [5,14], first-
order past-time monitors such as DejaVu [11], spatio-temporal logics such as
STREL [1] and SaSTL [22]. They are almost always deployed one at a time,
against a specification written for that engine. The control this paper argues
for separates the aspects a policy clause constrains, checks each with a monitor
mature for that aspect, and composes the verdicts into one auditable decision.
    Two commitments distinguish what follows. First, the spatial aspect is
treated as spatial. Much work on agent compliance reduces “where” to a label
lookup, which cannot express standoff, masking, corridor containment, or the
difference between a disallowed destination that exists in the topology and one
that is reachable. We interpret φS over a weighted two-sorted location graph in
which physical mission geometry and information-release topology are the same
mathematical object. Second, a monitor must be able to say that it is not sure:
verdicts live in a four-valued domain, so a component that only guesses cannot
manufacture a definite refusal.

Contributions.

 – A multi-aspect assurance model. Trace-level obligations are decomposed
   into spatial, temporal and semantic aspects over one canonical event stream,
   with the spatial aspect interpreted over a two-sorted location graph that car-
   ries mission geometry and information-release topology in the same struc-
   ture, so one reachability query decides both where an effect may land and
   where a record may travel. An expressiveness argument motivates keeping
   the spatial aspect separate from the temporal one (Sects. 3, 3.5).
 – Preventive composition and enforcement. A guarded four-valued com-
   position, reusing the four-symbol domain of RV-LTL [4], carries provenance,
4         N. Kekatos et al.

      and a shield evaluates each proposed call on a shadow world model and com-
      mits only what the composed verdict permits, which turns monitoring into
      prevention rather than reporting (Sects. 3.6, 4).
    – Simulation-based V&V evidence. An evaluation across three instantia-
      tions establishes when composition is required, whether the temporal aspect
      agrees with an independent engine, whether enforcement preserves mission
      effectiveness in closed loop, and where assurance fails when the tool surface
      is incomplete or evidence can be forged (Sect. 5).

What we reuse, and what we add. Every monitoring engine here is established
and none is advanced by us: stream-based monitoring [5,14,9], BDD-based first-
order past-time monitoring and its timed extension [11,10], MFOTL and its
decision procedure [2], the spatial modalities and their graph semantics [1,22],
abstaining classification with a quantified error budget [24], and the observation
that multi-step tool use defeats per-call guardrails [20]. What we add is the two-
sorted location graph in which mission geometry and release topology become
one metric structure; the argument motivating a separate spatial monitor from
the expressiveness and capability boundaries of Sect. 3.5; the four-valued com-
position with provenance, and the observation that presumptive verdicts belong
to the composition layer rather than to any engine; the shadow-evaluate-then-
commit shield that makes the framework preventive; and three instantiations
showing that a new domain costs a vocabulary.
In short, Sect. 3 defines what must be checked, Sect. 4 defines how the frame-
work is validated in simulation, and Sect. 5 reports whether the resulting shield
prevents violations, at what cost, and under what assurance assumptions.

2      Operational Scenario and Assurance Problem
Decision support for medical evacuation is established, but its systems are
machine-learning and optimisation systems rather than language models in-
voking tools [21,19]. We model the composition of two documented trends:
LLM agents entering planning workflows [7], and AI decision support entering
evacuation and sustainment. The agents here are representative near-term roles
rather than fielded systems, and the monitoring problem does not turn on that
distinction: it arises wherever multi-step tool use meets multi-aspect obligations.
     A casualty-evacuation tasking agent supports a medical operations cell, work-
ing under a standing clause: aircraft flying under the protective medical mark-
ing shall carry nothing outside their medical function; casualty records may be
shared only with facilities covered by a medical-sharing arrangement and only
with authority for that casualty; urgent casualties are to be evacuated within
the hour. The agent makes four calls, each admissible on its own and each seen
only in part by one aspect: it requests the protective marking, which φT sees
granted and never revoked; it plans a route across the forward line, which φS
sees as lawful for a protected flight; it amends the manifest, where the cargo field
still reads cargo and only the narrative names ammunition, so φΣ sees narrative
alone; and it crosses the line, which no aspect refuses by itself.
                    Multi-Aspect Runtime Verification of LLM-Based Agents          5

    The composition is a violation: a medical aircraft carrying materiel outside
its medical function loses the protection the marking asserts, so continuing to
display it is improper use of the protective emblem. Whether that rises to perfidy
turns on an intent a monitor cannot establish, so the framework refuses the
crossing on the objective elements alone. Only a monitor that reads the manifest
narrative, remembers when the marking was granted, and knows the aircraft has
left friendly-held airspace can refuse step 4, and only by combining all three.
    The same structure recurs throughout the evaluation: a casualty record that
escapes its release domain because a coalition feed was enabled two steps earlier;
a “sanitised” summary that still carries identifiers; and a convoy declared hu-
manitarian to obtain corridor access whose load was later amended. In each case
the aspects are separable, none suffices, and the violation is a trace property.

Requirements. The scenario fixes what a mechanism has to provide.

R1, trace memory. The monitor must relate actions across time. A call in-
   spected independently of what preceded it cannot see this violation.
R2, heterogeneous evidence. Compliance depends jointly on spatial state,
   temporal history and content, so one kind of evidence is not enough.
R3, pre-commit evaluation. The action that first makes the prohibited state
   reachable must be stopped before it executes, not reported after.
R4, auditability. A refusal must name the obligation it rests on and the ev-
   idence that produced it, because an operator inherits responsibility for ac-
   cepting or overriding it.

Section 3 constructs the framework to satisfy R1–R4.


3     Multi-Aspect Runtime Assurance Framework
A policy clause written in natural language is compiled into a typed triple
⟨φS , φT , φΣ ⟩ interpreted over a single canonical event stream. Everything in this
section is contributed here, with two exceptions that are inherited and cited as
such: the spatial modalities and their graph semantics, and the underlying mon-
itoring logics. What is new is the event schema, the two-sorted location graph,
the expressiveness limits motivating the decomposition, and the composition al-
gebra. This section fixes the event schema (Sect. 3.1), the location graph that
gives the spatial aspect its semantics (Sect. 3.2), the qualitative spatial fragment
over it (Sect. 3.3), the three aspects of the triple (Sect. 3.4), and the four-valued
algebra that fuses their verdicts with provenance (Sect. 3.6).

3.1   Canonical Event Model
All three aspects read one stream. Canonicalisation maps every agent action,
tool invocation, tool result and observation to an event

                             e = ⟨ τ, α, κ, ι, ā, λ ⟩,
6      N. Kekatos et al.

where τ is a mission timestamp, α the actor, κ the event kind (tool_call,
tool_result, observation, user_msg), ι the tool identifier, ā the typed argu-
ment vector, and λ a set of semantic labels. A single stream is what makes the
aspects composable: they do not observe three different abstractions of the agent,
they observe the same trace through three different lenses, so their verdicts are
about the same event and can be fused pointwise.
    Three design choices matter for soundness. First, canonicalisation sits on
the trusted path between the planner and the tool executor, so an agent whose
planning has been diverted still emits faithful events; the monitor’s view is not
mediated by the component under suspicion. Second, the shield evaluates each
tool_call before its effect is committed, on a shadow copy of the world model,
and commits only if the composed verdict permits it. A blocked call therefore
never mutates mission state, which is what allows a violation to be prevented
rather than merely reported.
    Third, and easily overlooked: one tool call is one time-point database.
A single call typically makes several facts true at once, a record acquires a
location, a channel opens, a marking is assigned, and these are simultaneous,
not successive. A monitor that advances one event per step would, if fed them
one at a time, place them at distinct time points and thereby stretch every
bounded window in φT by the number of facts the call happened to produce.
Canonicalisation therefore emits the whole set at a single timestamp, and the
MFOTL export of Sect. 5.2 preserves that grouping. This is a property of the
interface rather than of any engine, and it has to be stated, because getting it
wrong is silent: the windows simply drift.
    We also fix a convention for undefined operands. A spatial predicate over an
object with no location, or a temporal predicate over an obligation never armed,
evaluates to false rather than raising or defaulting to satisfaction, so a record
that does not yet exist is never “outside its release domain”.

3.2   Two-Sorted Spatial World Model
The spatial aspect is interpreted over a weighted, two-sorted location graph

                            L = (V, E, w, sort, δ),

where w assigns a non-negative weight to each edge, sort partitions V into phys
and info vertices, and δ assigns a release domain to each informational vertex.
Vertices additionally carry the labels the spatial predicates read.
   Physical vertices are terrain cells, landing zones, threat emitters and mask-
ing terrain; their edges are undirected and weighted by distance in kilometres.
Informational vertices are hosts and enclaves, each in a release domain such as
Med, Med-Coalition, Partner or Log; their edges are directed, because a release
channel is one-way, and carry the domain-crossing weight
                                     (
                                       0 if δ(u) = δ(v),
                         w(u, v) =
                                       1 otherwise.
                   Multi-Aspect Runtime Verification of LLM-Based Agents         7

    Putting both sorts in one graph is the central modelling decision of this
paper, and it is not a convenience. It means a single spatial monitor answers
both where the aircraft may go and where the data may travel, because under
the domain-crossing weight the informational sort carries a distance that counts
release-domain boundaries.
    Fig. 1 shows both sorts of the MEDEVAC graph. In the informational sort
med holds the marked record, med_coalition is a domain it may lawfully reach
and partner one it may not, so a move inside a domain weighs 0 and a move
across a boundary weighs 1; opening one channel at turn 4 puts a partner vertex
inside the record’s reach and fires S1 before the record moves. In the physical
sort, with standoff d = 4 km, LZB violates it over an admissible 3 km path while
LZC is nearer at 2.5 km and safe, its only route running through masking terrain
the path predicate excludes. Proximity alone would not separate the two.
    The two sorts differ in what kind of space they are. On the physical sort,
undirected edges with positive kilometre weights give a genuine metric. On the
informational sort the shortest-path distance d(u, v) is non-negative, satisfies
d(u, u) = 0 and obeys the triangle inequality, but it is neither symmetric, since
release channels are directed, nor separating, since two distinct hosts in the same
release domain lie at distance 0. It is therefore a quasi-pseudometric rather than
a metric, and deliberately so: hosts within one domain should be indistinguish-
able to a clause about domain crossings, and a one-way channel should not imply
its converse. Non-negativity and the triangle inequality are all the shortest-path
semantics of the spatial operators requires, so both sorts are admissible inter-
pretations of the same operators. A clause about standoff from a threat and a
clause about a casualty record leaving a release domain are then instances of
the same operator, and the data-residency property of the civil instantiation, “at
least one copy in an approved store”, is the degenerate zero-distance case.
8       N. Kekatos et al.

                      med

                          med_rear
                    0                                                   partner

          med_fwd             0            c2_cop         1           coalition_cop


            1         marked record r               opens at turn 4
                                                                      × disallowed

        partner_med

          med_coalition (allowed)

                (a) informational sort: runtime topology

                        3.0
           LZA                                                            8.0 km > d ✓
                                              5.0
                        1.0                 2.0
           LZB                                                threat      3.0 km < d ×
                                              1.5
           LZC          1.0   mask                                        2.5 km < d, masked ✓
                           excluded by
                          path predicate
           (b) physical sort: path-constrained reachability

Fig. 1. Two sorts of one location graph. In (a) opening a release channel makes a
disallowed domain reachable; in (b) masking excludes a shorter physical path. One
reachability semantics evaluates both.


3.3   Spatial Operators and Reachability Semantics
Over L we use the Boolean fragment of the spatial operators of STREL [1],
whose satisfaction is decided by a shortest-path computation restricted to the
vertices admitted by a path predicate. Writing (L, s) |=l ϕ for satisfaction of ϕ
at vertex l under a labelling s, and d(l, l′ ) for the least weight of an admissible
path:

       ♢[0,d] ϕ at l ≡ ∃ l′ . d(l, l′ ) ≤ d ∧ ϕ(l′ ),
        □[0,d] ϕ at l ≡ ∀ l′ . d(l, l′ ) ≤ d ⇒ ϕ(l′ ),
                                                     P
R[0,d] (ϕ1 , ϕ2 ) at l ≡ ∃ π = l0 · · · lk , l0 = l,   i w(li , li+1 ) ≤ d,
                                     ϕ2 (lk ) ∧ ∀i < k. ϕ1 (li ),
      E[d,∞) ϕ at l ≡ ∃ π from l, ϕ throughout π, reaching l′ with d(l, l′ ) ≥ d.

   The operator that does the real work below is R, and it is the difference
between a spatial monitor and a proximity check. A ♢ query sees the masked
emitter of Fig. 1(b) and raises an alarm; a R query, whose path predicate ex-
cludes masking vertices, does not. The same asymmetry holds on the infor-
mational sort: a record is endangered by a disallowed enclave only when some
opened channel leads there, and the mere existence of the enclave is not enough.
Proximity over-approximates; reachability is what the obligation says.
                     Multi-Aspect Runtime Verification of LLM-Based Agents            9

3.4    Aspect-Specific Obligations
We instantiate the framework on an LLM-based MEDEVAC/CASEVAC tasking
agent that triages incoming 9-line requests, designates landing zones, requests
aeromedical clearance and launch authority, coordinates with coalition medi-
cal facilities, and manages casualty records. Its obligations are simultaneously
spatial, temporal and text-semantic, and no one of them is decoration.

Spatial aspect φS (stream-based; TeSSLa). Let PHI(r) denote that record r is
typed as carrying casualty identifiers, loc(r) its current locations, trav(l) that l
is a home enclave or the endpoint of an opened channel, and disallowed(l) that
δ(l) ∈
     / {Med, Med-Coalition}:

      S1 : ∀r. PHI(r) ⇒ ∀l ∈ loc(r). ¬ disallowed(l)
                                              
                ∧ ¬ R trav, disallowed ∧ trav at l,                  (PII containment)
                                           
      S2 : ∀m. ¬ R[0,dso ] ¬masking, threat at lz(m),                     (LZ standoff)
      S3 : ∀r. PHI(r) ⇒ ∃ l ∈ loc(r). ♢[0,0] medical_enclave at l.       (survivability)

S1 conjoins the target predicate with trav because a record can only land where
an inbound channel is open, and R also detects a record already outside its
permitted domains. S3 is the mission reading of the civil residency clause.

Temporal aspect φT (first-order past-time; DejaVu, MonPoly). With ⊖ for “at
some point in the past” bounded by a window:

      T1 : any action increasing the reachability of r towards X
                ⇒ ⊖≤Wa pii_release(r, X),                            (release authority)
      T2 : launch(m) ⇒ ⊖≤Wv clearance(m) ∧ ⊖≤Wv launch_auth(m)
                                              
                ∧ urgent(m) ⇒ ⊖≤1h casualty(m) ,        (launch conditions)
      T3 : a purge removing the last replica of r ⇒ ⊖≤Wr retention_release.
                                                                     (retention)

The first-order parameterisation carries the weight in T1 : an authority is granted
for a casualty and a partner, so an authority legitimately held for one casualty
does not discharge the obligation for another. The golden-hour conjunct of T2
is a genuine mission deadline rather than an ordering constraint, and it is the
clause that no spatial or semantic aspect can express. A fourth clause, T4 , carries
the protected-status obligation: an airframe that crosses the forward line while
holding the protective marking must not be carrying non-medical materiel. Its
spatial arming condition is supplied by the guard semantics of Sect. 3.6 rather
than by the clause itself, which is why it needs no separate displayed formula
here and why its refusal carries provenance from two aspects.

Semantic aspect φΣ (semantic kernel). φΣ has two duties. Typing: PHI(r) holds
if r carries an explicit classification marking (deterministic, verdict ⊤) or if a
10      N. Kekatos et al.

content test fires on its 9-line free text (presumptive, ⊤p ). This typing is the
precondition the other two aspects need, and it is supplied at runtime, so an
ablation that removes φΣ genuinely leaves φS and φT with no protected object
to quantify over. Laundering: an artefact derived from a marked source, carrying
no marking of its own, whose content test nonetheless fires, may not be released,
however impeccable its geometry and its authorities.
    The second duty is what distinguishes a semantic monitor from semantic in-
formation, and Sect. 5 shows the distinction is not academic: no trusted canon-
icaliser can label an artefact the agent has not created yet.

3.5   Expressiveness Limits and Motivation for Decomposition
All three aspects observe the same stream, so the obvious alternative is one first-
order temporal formula over a combined signature, handed to a single engine
such as MonPoly [3]. For the temporal and semantic aspects that alternative has
force. For the spatial aspect it does not.
    Fix a signature in which the location graph is a binary relation E, with unary
relations for vertex labels and the event predicates of Sect. 3.1; at any time point
a monitor sees a finite structure over it.
Proposition 1 (Non-definability of spatial containment). Let G be the
class of location graphs of unbounded size. There is no MFOTL formula ψ over
this signature such that, for every L ∈ G and every trace σ, ψ holds at a time
point of σ if and only if S1 is violated at that point.
Proof sketch. S1 requires R, the reflexive-transitive closure of the traversable-
edge relation restricted by a vertex predicate. Reachability is not first-order
definable uniformly over finite graphs of unbounded size. MFOTL’s temporal
operators quantify over time points and do not add transitive closure over the
spatial edge relation available at a point, so no fixed MFOTL formula over this
signature characterises S1 uniformly over G.
   The statement concerns MFOTL as monitored by MonPoly and its verified
successor [2]. Temporal logics extended with fixpoint, regular or recursive oper-
ators do express transitive closure, and we make no claim about those.
   The qualification uniformly is where the weight lies. On its own Proposition 1
has little practical bite, because for a fixed, known graph reachability unrolls into
a disjunction over the finitely many simple paths, and mission graphs are small.
The binding argument is the next one.

Dynamic topology. For a fixed finite graph, reachability can be compiled by
enumerating simple paths. That does not solve the runtime problem considered
here. Opening a release channel changes the traversable graph during execution,
so an encoding compiled against the initial topology ceases to characterise S1
after the first such change and would have to be regenerated. The motivating
attack of Sect. 2 and attack M1 turn on exactly such an event. An encoding
parameterised by a vertex bound rather than by a topology avoids regeneration,
                   Multi-Aspect Runtime Verification of LLM-Based Agents         11

since it reads the edge relation at the current time point; what it does not avoid
is Proposition 1, because the bound must still be fixed in advance.
    Together the non-definability result and this runtime-topology observation
say that the spatial obligations considered here are not subsumed by a sin-
gle first-order temporal specification that is fixed in advance and uniform over
graphs of unbounded size. For a deployment whose vertex set is known and
bounded, an unrolled encoding exists; what it costs, and how it is maintained as
the network grows, is an engineering question rather than an expressiveness one.
They do not establish that exactly three aspects are necessary, and we do not
claim it. The converse direction is no theorem either. It rests on a documented
capability boundary: BDD-based first-order monitors of the DejaVu family com-
pare data values for equality and disequality rather than magnitude [11], while
every metric predicate in φS , spatial constraints such as standoff distance and
corridor width, is a magnitude comparison. Nothing here says a sufficiently engi-
neered single engine is impossible; what it says is that the split follows the shape
of the obligations rather than the convenience of the implementer.

The semantic aspect is an interface. φΣ is specified as an abstract component:
it types an artefact and returns a verdict in V4 , emitting a presumptive value
exactly when its judgement is heuristic. Nothing else in the framework depends
on how it reaches that judgement. The architecture expects an abstaining clas-
sifier with a calibrated error bound [24], whose abstention region maps onto ⊤p
and ⊥p ; what we evaluate is a lexical cue matcher, which is a controlled baseline
occupying that slot and not a claim about detector robustness. Substituting a
calibrated classifier changes the confidence attached to a verdict and no other
part of the composition.

3.6   Guarded Four-Valued Composition and Provenance
Each aspect emits a verdict in V4 = {⊤, ⊥, ⊤p , ⊥p } (satisfied, violated, pre-
sumably satisfied, presumably violated). We reuse the four-symbol domain and
ordering of RV-LTL [4] and give the presumptive values a provenance inter-
pretation: they record that a heuristic rather than a deterministic component
produced the judgement.
    Two uncertainties are usually conflated under such values and we use only
one. The classical reading is trace-extension uncertainty: a verdict on a finite
prefix that a longer trace could overturn. The reading we use is provenance
uncertainty: the judgement rests on a heuristic component rather than a deter-
ministic one. The first does not arise here, and that is structural rather than a
simplification, because every clause of Sect. 3.4 is either a past-time obligation
decided definitively at each point or a predicate over the current world state.
No clause is a future-time obligation, so no verdict is ever revised by extending
the trace, and the presumptive values are free to carry exactly one meaning.
This would not survive admitting liveness: an obligation such as “the casualty
must reach a surgical facility”, which this framework cannot currently express,
reintroduces trace-extension uncertainty as an independent axis and the domain
12      N. Kekatos et al.

would have to become a product of truth status and confidence status. We record
this as the cost of the present design. A calibrated classifier [24] is the natural
occupant of the provenance slot; what we evaluate is weaker, and Sect. 4 says
exactly what it is.
    Verdicts are fused by

          vS ⊗ vT ⊗ vΣ = max⪯ {vS , vT , vΣ },        ⊤ ≺ ⊤p ≺ ⊥p ≺ ⊥,

so a definite violation dominates, a presumptive violation dominates satisfaction,
and the composed verdict is ⊤ only when every aspect is satisfied. Whether that
verdict causes a refusal is decided by the configurable blocking policy B of Sect. 4.

Guarded clauses. A flat join is not quite enough, and the protected-status clause
of Sect. 2 is where it breaks. Crossing the forward line is lawful; carrying materiel
is lawful; holding the protective marking is lawful. The obligation arms only once
the aircraft is beyond the line, and that condition is spatial, yet if φS reported
a violation whenever it held, the shield would refuse every lawful crossing. The
spatial aspect is necessary to the verdict without being an aspect that fires.
     We therefore give each aspect two interfaces: it produces a verdict va ∈ V4
on the current trace, and it can evaluate guard predicates γ that are true or false
on that trace. A clause is a pair c = ⟨Γc , Oc ⟩ of a finite guard set and a set of
obligation aspects, and its verdict is
              (
               ⊤                if ∃ γ ∈ Γc . ¬γ(σ) (the clause is not armed),
      [[c]] = N          c
                  a∈Oc va (σ) otherwise,

The shield composes the verdicts of all armed clauses. Clauses without guards
reduce to ordinary composition, which covers every clause in Sect. 3.4 except
the protected-status one.
   Two properties follow immediately and are the reason to prefer this to a
conditional in the enforcement code.

Refusal monotonicity. By construction, adding a guard cannot introduce a re-
fusal: [[⟨Γ ∪ {γ}, O⟩]] ⪯ [[⟨Γ, O⟩]] pointwise. If the added guard is false the clause
is unarmed and returns ⊤, the minimum of ⪯; otherwise every guard holds and
the obligation verdict is unchanged. Guards may therefore suppress refusals but
cannot create false positives.
    Second, provenance becomes two-sorted. A decision now reports both the
obligation aspects that fired and the guard aspects that armed the clause, which
is strictly more information for an operator: the protected-status refusal is re-
ported as fired by {T, Σ} under a spatial guard, rather than as a bare two-aspect
verdict with the geometry invisible.
    Every decision carries a provenance set π, recording the aspects that deter-
mined the verdict together with the aspects whose guards armed the clause.
Provenance is not diagnostic decoration: it is what makes a blocked action au-
ditable against the clause that blocked it, and it is what lets an operator see
                   Multi-Aspect Runtime Verification of LLM-Based Agents       13

that a refusal rests on, say, geometry and authority jointly rather than on a sin-
gle classifier. It is also the measurement that distinguishes this framework from
a disjunction of independent guardrails, Sect. 5 reports the fraction of blocks
whose evidence spans two or more aspects.


3.7   Model Independence, Applicability and Trust Assumptions

The framework is independent of the planner and the model, insofar as con-
sequential actions pass through the trusted canonicalisation and enforcement
interface, and depends on neither the weights nor the decoding strategy.
    The assurance claim it supports is correspondingly bounded. It does not
extend to actions that reach the world without traversing the interface, to world-
state changes the canonicaliser cannot observe, or to obligation-discharging
events whose principal cannot be attributed. These are not incidental caveats.
Section 5 reports an experiment in which three record-placing tools reached
a constrained effect without passing the spatial clause, and another in which
a forged authority discharged an obligation the agent was itself bound by.
Enforcement completeness is therefore a property of the tool surface and of
evidence attribution, and not of the clause set alone.


4     Simulation-Based V&V Methodology

The framework is realised as four components on the path between the agent’s
planner and its tool executor: a canonicaliser, three aspect monitors, a com-
poser and a shield (Fig. 2). The past-time monitor is an existing engine used
unmodified; the spatial and semantic monitors are reference implementations,
as Sect. 5 states. What this section contributes is the arrangement, and the
shadow-evaluate-then-commit discipline that makes the framework preventive
rather than diagnostic.

Canonicalisation. Every planner output, tool invocation, tool result and re-
trieved observation is translated into the event schema of Sect. 3.1 and appended
to a single stream that all three monitors consume. The canonicaliser also main-
tains the world model the monitors read: the location graph and its opened
channels, where each record resides, the authority and clearance logs, landing
zones and routes. Because it sits on the trusted path rather than inside the
planner, an agent whose planning has been diverted still emits faithful events.

Aspect monitors and their engines. The three aspects are checked by moni-
tors mature for their respective logics. φS is a stream-based computation over
the location graph: each spatial clause reduces to a shortest-path query re-
stricted to the vertices admitted by its path predicate, which is expressible as a
TeSSLa [5,14] stream transformation over the graph’s edge relation. φT is a first-
order past-time specification of the kind DejaVu [11] decides with BDD-encoded
14        N. Kekatos et al.

                                                              tool result

mission request
                                            read       φS                   composer
                                                                            N
                                                      graph                     , guards
                                            event                                       v, π
               proposed
                  call
      LLM              canonicaliser                   φΣ                    shield            commit     tool
     planner              trusted path               typing                 policy B                    executor
               apply to shadow                                                     ⊥p

                          world model      read        φT                   operator
                           + shadow                 past-time               escalation
                                                                                                    committed action

                                         commit or roll back


Fig. 2. The monitor on the path between planner and executor. The two heavy-
bordered boxes are the system boundary: a mission request enters at the planner and a
committed action leaves at the executor. Shading separates the untrusted planner, the
three aspect monitors, the world model and the trusted runtime. φΣ runs first because
its typing arms the other two, which are then independent. The composer applies the
guarded composition of Sect. 3.6 and attaches provenance. Every call is applied to a
shadow of the world model and committed only if the policy permits, so a refused call
never mutates mission state.



quantification over unbounded data domains; plain QTL carries no metric win-
dow, so the bounded obligations need either the timed extension [10] or a logic
that has them natively, and the same obligations are expressible in MFOTL and
are checked by MonPoly [3] in our artefact. φΣ is a semantic kernel combining
deterministic marking lookup with a content test whose hits become presumptive
verdicts rather than silent satisfaction.
    We are precise about what that content test is, because the distinction mat-
ters for how much the presumptive verdicts mean. In our implementation it is a
lexical cue matcher : a fixed list of identifier and materiel cues, matched against
the narrative field. It is not learned and it is not calibrated, so ⊤p here records
only that a cue fired, without a quantified error rate. A conformal classifier with a
guaranteed abstention budget [24] is the obvious occupant of this slot and would
give the presumptive verdicts probabilistic content; substituting one changes no
other component, because the composition consumes a verdict and not a score.
We have not done it, and we do not claim the four-valued domain is calibrated,
only that it is sound in direction: a heuristic component can raise a presumption
but can never, on its own, produce the definite refusal that only a deterministic
marking or a spatial or temporal violation can.
   An important architectural consequence of the shared event stream is that
the three monitors need not agree on an abstraction of the agent, only on the
trace. φΣ runs first on each event, because its typing is the precondition that
arms the obligations of the other two aspects; φS and φT are then independent
and could run concurrently.
                   Multi-Aspect Runtime Verification of LLM-Based Agents       15

                                                 N
Composer and shield. The composer applies           to the per-aspect verdicts and
attaches the provenance set. The shield turns the composed verdict into an action
under a configurable policy: it refuses a call whose composed verdict lies in a
blocking set B ⊆ V4 . With B = {⊥} only definite violations are refused and a
presumptive violation ⊥p is escalated to the operator; with the precautionary
B = {⊥, ⊥p } a presumptive violation is refused outright. Sect. 5 reports both.
    Crucially, the shield evaluates each call against a shadow of the world model:
the call’s effect is applied, the aspects are evaluated, and the effect is rolled
back. The shield commits the effect only once the policy permits it. A refused
call therefore never mutates mission state. This is what makes the framework
a preventive control rather than a detector, and it is why a violation that lives
in the composition of several steps can be stopped at the step that would first
make it reachable, rather than after the fact.

Cost. Per event, φT and φΣ are constant-time table and cue lookups. φS dom-
inates: each spatial clause costs one predicate-restricted Dijkstra computation,
O(|E| + |V | log |V |) on the location graph. Only calls that touch geometry or
record placement pay this, which is why the measured latency distribution in
Sect. 5 is markedly bimodal.


4.1   System Under Test and V&V Architecture

The experiments below are simulation-based verification and validation of an
autonomous decision-support agent, and it is worth naming the correspondence
explicitly because the rest of the paper is written in the vocabulary of runtime
verification rather than that of modelling and simulation.
    The simulation state is the world model of Sect. 4: the two-sorted location
graph with its opened channels and switchable topology, the placement of each
casualty record, the authority and clearance logs, the designated landing zones
and the planned routes. It is a model of an operational environment rather than
a log of one, and it is the only thing the monitors read.
    The executable trace is the canonical event stream. Every planner output,
tool invocation, tool result and retrieved observation becomes a typed event,
so a mission run is a sequence of state transitions over the simulation state
regardless of whether the actions were produced by a scripted planner, by a
generator, or by a language model.
    The experimental design is the scenario families of Sect. 5.1. Each family
fixes a mission template and randomises the factors that matter to the obliga-
tions under test: topology and switch state, standoff geometry, authority timing
relative to the deadline, record content, and the position of the violating step
within an otherwise admissible sequence. Drawing n = 400 per domain with
Wilson intervals is a designed experiment over that factor space rather than a
hand-built attack suite.
    The measures are the ones a V&V argument needs rather than the ones
a security paper would report alone: whether the prohibited effect is reached,
16     N. Kekatos et al.

whether admissible traffic is refused, what the enforcement costs per event, and
which aspects supplied the evidence for each decision.
    Two properties make this arrangement particularly relevant to simulation-
based V&V. First, the shield sits between planner and executor and reads only
canonical events, so the same specification runs unchanged whether the planner
is simulated or live; the study of Sect. 5.3 substitutes a language model for the
scripted planner and changes nothing else. Second, because the world model is
simulated, the counterfactual is available: a proposed action can be applied to
a shadow copy, evaluated, and rolled back, which is what makes enforcement
preventive rather than diagnostic. Neither property survives if the monitor is
attached to a fielded system after the fact, which is the argument for doing this
work in simulation first.


4.2   Domain Instantiations and Implementation Status

We evaluate three instantiations of the same framework, the same composition
algebra and the same shield.

 – MEDEVAC, the casualty-evacuation tasking agent of Sect. 3.4: nine attack
   and nine benign traces over the location graph, spanning 65 tool calls.
 – Contested logistics, a sustainment movement-planning agent that routes
   convoys, books cross-border transit, maintains consignment manifests, and
   coordinates with allied depots, host-nation customs, and a contracted carrier.
   Nine attack and nine benign traces.
 – Civil, a GDPR data-handling agent with five attack and five benign traces,
   the instantiation in which the spatial aspect degenerates to the residency
   label check that motivated this work.

    Attacks count as successful iff the violating outcome is reached despite the
shield; a benign trace counts as a false positive iff any of its calls is refused.
    The logistics instantiation is where the two-sorted location graph earns its
keep most directly, because both sorts arise from one story: materiel moves
through physical space, routes, ambush arcs, defilade, a declared humanitar-
ian corridor, while its paperwork moves through information space, across the
national logistics enclave, coalition logistics C2, host-nation customs, and the
carrier’s commercial transport-management system. Contracted carriage is ordi-
nary in sustainment, so a manifest reaching a carrier’s system is a real disclosure
boundary rather than a modelling convenience.
    Implementing it also quantifies the framework’s portability. The logistics in-
stantiation contributes roughly forty lines of genuinely new content: the release
domains a controlled consignment may occupy, four vertex-label names, three
classifier cue lists, and an alias map from the logistics tool vocabulary onto the
canonical operations. The location graph, the spatial fragment, the four-valued
algebra, the shield, the shadow-evaluate-then-commit discipline and every clause
structure are inherited unchanged. A second domain costs a vocabulary rather
than an implementation.
                    Multi-Aspect Runtime Verification of LLM-Based Agents         17

Implementation status of each aspect. We state this once, plainly, because it
bounds every number below. φT is specified in MFOTL and executed on the un-
modified MonPoly engine (Sect. 5.2). φS and φΣ are reference implementations
of the specifications in Sect. 3: the spatial clauses are written for a stream engine
over the location graph and the artefact ships them, but no stream engine exe-
cutes them here. The composition algebra, provenance, canonical schema, world
model, shield and metrics are the real framework in each case. Where the paper
says an aspect is checked by a monitor mature for its logic, it names the intended
engine rather than claiming that all three have been run on one.

4.3   Research Questions and Evaluation Strategy
We ask four questions, one per finding below. RQ1, effectiveness: does multi-
aspect composition prevent violations that partial monitoring misses, and at
what cost in false refusals on benign traffic? RQ2, validity and efficiency:
is the implementation correct enough to trust, judged against an independent
engine, and cheap enough to run online? RQ3, closed-loop behaviour: does
enforcement keep the agent out of violating states while still letting it com-
plete a compliant mission (Sect. 5.3)? RQ4, assurance robustness: can the
enforcement mechanism itself be bypassed?


5     Experimental Results
This section reports four findings, one per research question: what composition
buys over partial monitoring, whether the implementation is correct and cheap
enough to trust, whether enforcement holds in closed loop without preventing
the mission, and whether the enforcement mechanism itself can be bypassed.

5.1   Multi-Aspect Effectiveness and Robustness
Table 1 reports every configuration we evaluated. Unshielded, all nine attacks
succeed in both mission domains. Under full composition with the precautionary
policy, none does, and no benign trace is refused.
    The two mission suites yield identical rows at every configuration, and iden-
tical per-attack provenance. We are explicit about what this does and does not
show. The logistics traces were designed as deliberate structural twins of the
MEDEVAC ones, L1 mirrors M1, L7 mirrors M7, and so on, precisely so that
the two tables could be read against each other. The agreement is therefore
evidence that the framework ports across two domain instantiations of equiv-
alent attack families with its clause structure and separability intact; it is not
independent corroboration of the rates and does not double the sample.
    Two comparisons carry the argument. The per-call guardrail baseline is an
AgentSpec-style control [29] with trusted typing but no trace history: it refuses
any release, staging or purge of a record typed as carrying casualty identifiers.
Having no memory, it cannot see a prior authority, whether a replica survives,
18        N. Kekatos et al.

Table 1. Both mission suites (9 attacks, 9 benign each; the MEDEVAC and contested-
logistics instantiations agree at every row). ASR = attack success rate, FPR = benign
false-positive rate, |π| ≥ 2 = fraction of refusals whose evidence spans two or more
aspects. Every proper subset of the three aspects leaves attacks succeeding.

     Configuration                        ASR      FPR      µs/event     |π| ≥ 2
     No monitor                            100%       0%            —          —
     φS only                                78%       0%           1.9        0%
     φT only                                78%       0%           1.8        0%
     φΣ only                                78%       0%           3.4        0%
     φS × φ T                               56%       0%           2.0        0%
     φS × φ Σ                               33%       0%           3.6        0%
     φT × φ Σ                               44%       0%           3.5       17%
     Full composition, default B = {⊥}      11%      0%            3.6       33%
     Full composition, precautionary         0%      0%            3.6       33%
     φS × φT , trusted labels               33%      0%             —          —
     Per-call guardrail baseline            67%     33%             —          —



or whether the destination domain is permitted, so it both misses two thirds of
the attacks and refuses a third of legitimate casualty handling. This is precisely
the regime STAC-style attacks [20] exploit.
    The trusted-labels row is the sharper result. It runs φS × φT without the
semantic monitor but with the labels that monitor would have supplied, sepa-
rating “the framework needs semantic information” from “the framework needs
a semantic monitor”. In the civil instantiation this configuration reaches 0%:
semantic information sufficed. In the mission instantiation it leaves a third of
attacks succeeding, because no canonicaliser can label an artefact the agent has
not created yet (M5), and no label describes what a load manifest says (M7).
Semantic monitoring is an irreducible aspect rather than a labelling convenience.

What each aspect contributes. Table 2 isolates which monitor catches which
attack, with typing supplied to every column so that the comparison is between
the three monitors rather than a re-test of the fact that φΣ supplies typing.
    The result is unambiguous. Each single aspect leaves at least 78% of attacks
succeeding; the best pair still leaves a third. Among the evaluated configura-
tions, only full composition closes the suite. Provenance quantifies how often the
aspects genuinely interlock: 33% of refusals carry evidence from two or more as-
pects, including M7, whose refusal rests jointly on the past-time obligation and
the semantic reading of the load manifest.
    M7 illustrates a case a flat disjunction of monitors would not handle: φS
contributes the spatial guard, arming the obligation once the aircraft leaves
friendly-held airspace without itself being the aspect that fires. M9 exercises
the four-valued domain, since the record is typed by the content test alone and
                    Multi-Aspect Runtime Verification of LLM-Based Agents            19

Table 2. Attack-by-aspect isolation. No aspect catches more than four of nine; no
pair catches all; only the composition does. The contested-logistics twin of each attack
isolates to the same aspect.

      ID        Attack (MEDEVAC / logistics twin)               φS     φT     φΣ
      M1/L1     feed escape to a disallowed domain               ✓
      M2/L2     authority held for the wrong object                    ✓
      M3/L3     point designated inside a threat arc             ✓
      M4/L4     mission deadline missed                                ✓
      M5/L5     sanitisation / consolidation laundering                       ✓
      M6/L6     retention purge                                  ✓     ✓
      M7/L7     protected status retained after amendment                     ✓
      M8/L8     corridor breach                                  ✓
      M9/L9     presumptive typing



the composed verdict is ⊥p ; under the default policy the call is escalated rather
than refused, which is why the default row of Table 1 shows 11%, and under the
precautionary policy it is refused at no cost in false positives here.

Robustness under randomised scenarios. Nine designed traces per domain estab-
lish that the aspects are separable but cannot carry the headline rates: 0/9 has
a Wilson 95% interval of [0, 29.9%]. We therefore sample from a family around
each designed composition, varying what a deployment would vary: which cross-
domain channels exist, distance to the threat and whether masking terrain lies
on the path, corridor clearance, clearance and authority offsets, the report-to-
launch delay straddling the deadline in both directions, identifier density in de-
rived artefacts, whether an amended load is genuinely materiel, and benign filler
calls interleaved at random positions. Benign variants are drawn from the same
family and differ only in the single parameter that decides the property, so the
generator measures whether the shield still separates them once everything else
is randomised.
    At n = 400 per domain across seven families, full composition misses no at-
tack and refuses no benign trace: miss rate 0.0%, Wilson [0, 1.8%]; false positives
0.0%, Wilson [0, 2.0%]. Single aspects miss between 71.4% and 85.4%, and the
best pair still misses 27.7%. Every family separates cleanly, and the MEDEVAC
and logistics generators agree to the sample.
    The generator earned its place immediately by finding a defect the designed
suite could not. Opening a release channel keyed its authority lookup by the
destination’s release domain, while a direct release keyed the same obligation
by the named partner. The hand-written escape attack grants no authority at
all, so both lookups failed and the inconsistency was invisible; the generated
benign variants, which do grant authority before opening a legitimate feed, were
refused 33 times out of 33. Keying both by the destination enclave fixes it, and
leaves every designed-suite result and the engine agreement below unchanged.
20      N. Kekatos et al.

We report this because it is the substantive argument for generated suites: a
designed suite tests the properties the designer had in mind.


5.2   Monitor Validation and Runtime Cost

This section checks the monitor implementations against an independent engine,
marks the boundary of what a second engine can express, and reports what
enforcement costs per event.

Agreement with an independent engine. The φT clauses are first-order past-time
obligations, and our MissionPastTimeMonitor is a reference implementation of
them. To check that the clauses are engine-checked and not merely engine-ready,
we exported both mission suites to a MonPoly log and the four φT clauses to
MFOTL, and ran the unmodified MonPoly [3] binary over them. T2 is split into
its three conjuncts so that every formula is safe-range, giving six clauses: T1 pairs
a raised reach with the absence of a prior release inside a 720 window; T2a and
T2b pair a launch with a missing clearance or launch authority inside 360; T2c
adds the golden hour, a launch on an urgent casualty with no casualty record
inside 60; T3 pairs a last-replica purge with no retention release inside 1440;
and T4 pairs a crossing under a protective marking with non-medical materiel
aboard. The encodings ship with the artefact.
    Across the eighteen MEDEVAC traces, canonicalised to 32 time points, the
reference monitor reports a φT violation at six time points. MonPoly fires at
exactly those six and at no others, with each clause firing on precisely the attacks
it was written for: T1 on M1 and M2, T2c on M4, T3 on M6, T4 on M7. The
contested-logistics suite reproduces this clause for clause. Neither T2a nor T2b
ever fires, which is correct, no attack in either suite omits a clearance.

A second engine, and what it cannot do. We repeated the exercise on De-
jaVu [11], whose decision procedure is BDD-encoded first-order past-time rather
than MFOTL. Plain QTL has past operators but no metric windows, so DejaVu
can only be given the untimed first-order fragment of φT . On that fragment it
flags five of the six time points at which the reference monitor reports a violation,
and no others. The sixth is the golden-hour breach of T2 , where the clearances
are present and only the elapsed time is wrong, and DejaVu is right not to flag
it: the property it was given does not mention time.
     That disagreement is a capability boundary rather than a defect. The un-
timed first-order fragment lies within DejaVu’s capability, whereas the metric
windows require either its timed extension or an engine such as MonPoly, which
discharges the complete φT specification in our evaluation. The exercise also ex-
posed an event-placement defect in our own export, corrected before the experi-
ments reported here. One further difference: MonPoly is two-valued and reports
the M9 firing as a definite violation, whereas the composed verdict is ⊥p : the
four-valued domain is a property of the framework rather than of an engine.
                   Multi-Aspect Runtime Verification of LLM-Based Agents         21

Runtime cost. All timings are measured on an Apple M4 Pro (12 cores, 24 GB)
under macOS 15.3 with CPython 3.14, single-threaded, with the monitors in-
process; no figure below includes model-inference or network time.
    Replaying every trace 1000 times under full composition yields 65,000 per-
event measurements per mission suite. MEDEVAC: mean 5.2 µs, median 4.9 µs,
p95 10.3 µs, p99 13.3 µs. Contested logistics is indistinguishable at mean 5.3 µs,
median 5.0 µs. The civil suite, whose spatial aspect is the degenerate zero-
distance case, averages 2.0 µs.
    The distribution is bimodal, as Sect. 4 anticipates: a lower mode near 1.4 µs
for calls that cost a table lookup, and an upper mode for calls that touch ge-
ometry or record placement and pay for a predicate-restricted shortest-path
computation. The median call falls in the upper mode, which is also why the
mission suites cost about two and a half times the civil one. These measurements
place monitor execution firmly in the microsecond range; model inference and
network time are excluded from the timings.


5.3   Closed-Loop Agent Evaluation

We evaluate closed-loop enforcement in two complementary settings. First, a
small language-model-in-the-loop experiment checks that the shield prevents
prohibited effects arising from model-generated tool calls. Second, a determin-
istic policy-naive planner isolates enforcement as the experimental variable and
measures prevention, recovery and mission cost at scale.


Language-model planner under adversarial injection. Every experiment
above evaluates the monitor on traces we wrote or generated. This one substi-
tutes a language model (Llama 3.2 3B, run locally) for the scripted planner,
changing nothing else: its JSON tool calls are canonicalised and passed to the
shield, and refusals are returned so it can replan. Four conditions cross an in-
jected instruction with the shield, at n = 12 episodes each.
    Under injection the planner reaches the prohibited state in 6 of 12 unshielded
episodes, a 50.0% escape rate with a Wilson 95% interval of [25.4, 74.6]. No
shielded episode reaches it, 0 of 12, interval [0.0, 24.2]. Without injection the
planner still reaches it once in 12 unshielded episodes, and never when shielded.
The shield is not free: it refuses 2.4 calls per injected episode and 4.6 per benign
one, so on this suite the utility cost of enforcement falls mainly on traffic that
was never going to violate anything. These are refusals of intermediate calls
that the planner can replan around, not the trace-level false positives counted
in Table 1, and the two should not be read against each other. They do show
that enforcement can carry a real utility cost on episodes that would never have
violated the policy.
    Two things bound what this shows. The planner is a 3B local model, so
these counts are not an estimate of attack success against larger models, and
STAC reports success above 90% against frontier systems [20]. And n = 12 per
condition gives intervals wide enough that the 50% and the 8% are not separable
22      N. Kekatos et al.

with confidence. What the experiment does establish is narrower and still worth
having: the enforcement path operates on actual model-generated tool behaviour,
not only on traces we authored, and no shielded episode reached the prohibited
state under either the injected or the non-injected condition. Sect. 5.3 supplies
the larger controlled experiment that quantifies prevention, recovery and cost
with enforcement as the only variable.

Harness defects. Harness validation exposed several silent integration and mea-
surement defects, each capable of invalidating an episode without producing an
execution error. All results reported here use the corrected harness; the individ-
ual defects and their regression checks are documented with the artefact.

Controlled prevention, recovery and cost. The preceding experiment shows that
the shield intercepts prohibited effects arising from model-generated tool be-
haviour, but its small sample and stochastic planner do not isolate enforcement
as the causal variable. We therefore complement it with a deterministic policy-
naive planner, for which enforcement is the only difference between runs.

Design. A casualty is urgent and the planner minimises evacuation time. It
is policy-naive by construction: it sees the mission, the tool surface and the
transit times, and not the release rules, which is the architectural assumption
the framework rests on. On a refusal it reads the provenance and revises: a spatial
refusal means the destination is wrong, so it tries the next facility; a temporal
refusal means a precondition is missing, so it seeks the authority and retries. Four
factors are drawn independently over 400 episodes: whether the fastest facility is
the non-compliant one, whether a compliant facility is reachable at all, whether
command has pre-issued the release authority, and whether the record carries
PHI. The second factor matters most: in 79 episodes no compliant route to the
goal exists, and a correct shield must then refuse and let the mission fail rather
than permit the violation.

Result. The four measures are safety (violation rate), mission effectiveness (de-
livery rate), recovery (compliant delivery after a refusal) and cost (extra tool calls
and planning rounds). Unshielded, the planner reaches a violating world state
in 77.0% [72.6, 80.9] of episodes and delivers the record in every one. Shielded,
violations are 0.0% [0.0, 1.0] and delivery falls to 85.0% [81.2, 88.2]. Of the 308
episodes containing a refusal, 80.5% [75.7, 84.6] recover to a compliant delivery
and 60 are abandoned; the abandoned episodes are those in which no compliant
facility was reachable, so the 15-point drop in delivery is the price of the guaran-
tee and not a monitor defect. Enforcement costs a median of two extra tool calls
and one extra planning round. The refusals are two-aspect in 248 of 308 cases,
firing {S, T } on the first attempt and {T } on the retry, which is the composition
of Sect. 3.6 doing visible work in a closed loop.
    The precautionary policy B = {⊥, ⊥p } is indistinguishable from the default
here, because the semantic typing is deterministic for these records and no pre-
sumptive verdict arises. That is a property of this scenario rather than a finding
about the policies.
                    Multi-Aspect Runtime Verification of LLM-Based Agents         23

5.4   Enforcement-Surface Robustness

The experiments above ask whether an agent can be induced to violate a clause.
This one asks a different question, namely whether the objective can be reached
anyway with the clauses in place. Three probes are directed at the enforcement
mechanism rather than at the planner, and two of them found real defects.

Equivalent-path evasion. A clause is enforced only if every tool capable of pro-
ducing the effect it constrains is routed through the check. We audited the record-
placing tools and found three, record creation, replication, and derivation of a
summary, that placed a record without traversing φS . The consequence is not
subtle: the feed-mirror attack the framework blocks can be walked around by
replicating the record to the disallowed enclave directly, or simply by reorder-
ing it, opening the channel first while no marked record exists and creating the
record afterwards. Both reach the objective with no clause firing.
    Each of the three was found by a different accident: an equivalent-path audit,
a reordering probe, and a live agent run that wandered into the ordering by itself.
Three accidents are not a method, so the artefact now carries a coverage test
that asserts the property directly: for every tool that can place a record, it places
one somewhere disallowed and requires a refusal. All five now enforce φS .
    We draw the general lesson explicitly, because the paper’s other results do
not imply it: enforcement completeness is a property of the tool surface,
not of the clause set. Sect. 3 reasons about clauses and Sect. 5.2 discharges
one on a real engine, but neither says anything about whether the surface is
covered. That obligation is separate, it does not follow from any expressiveness
argument, and on our evidence it is easy to get wrong.

Precondition forgery. An obligation is worthless if the party bound by it can
discharge it. Our tool surface exposed the authority-granting operations to the
agent itself, so the agent could satisfy T1 by granting itself the release authority
and then releasing, which it did, unblocked. The retention release of T3 fell too.
    The fix was latent in the design: the canonical event schema of Sect. 3.1 carries
an actor, which we had not used. Discharging events now record their principal,
and only events attributed to a principal other than the agent may satisfy an
obligation. This is a threat-model commitment rather than an implementation
detail, and it belongs beside the trusted-path assumption: canonicalisation must
not merely record that an authority exists but who issued it.
    One result here was unexpected and cuts in the framework’s favour. In these
cases composition gave defence in depth against forged temporal evidence: the
self-granted authority did satisfy φT , and φS refused the prohibited effect any-
way. This benefit was not anticipated in the experimental design, and we make
no claim about forged evidence on the other aspects.
    Returning provenance with a refusal could in principle help an attacker re-
plan; we tested it and found no effect at our sample size, which bounds the
concern without dispelling it.
24     N. Kekatos et al.

Scope of this version. External-corpus replay and comparison against a richer
stateful policy baseline are outside the scope of this evaluation. Generalisation
beyond the constructed attack families, and improvement over alternative state-
ful enforcement architectures, therefore remain to be established.


6    Discussion and Threats to Validity

Four things, each bounded by the suite it was measured on. On the evaluated
obligation families no proper subset of the three aspects closes the suite and
the full composition under the precautionary policy does. The temporal aspect
agrees with MonPoly at every time point, and per-event monitoring cost stays in
the microsecond range. In a controlled closed loop the shield keeps the planner
out of violating states while most refused episodes still recover to a compliant
outcome. And an attack on the enforcement mechanism itself found real defects:
equivalent action paths that reached a constrained effect without traversing the
clause, and a forged authority discharging an obligation that bound the agent.

Deployment and applicability. The last of those is the one that generalises, and
the Conclusion states it as the paper’s broadest claim. A specification can be
right and the deployment still unsound if a second tool reaches the same effect,
or if the party bound by an obligation can issue the authority that discharges
it. Sect. 3.7 states the assumption; the experiments show its cost when it fails.

Threats to validity. Internal. The designed suites are small by construction, so
0/9 carries a Wilson interval of [0%, 29.9%]; the generated suite narrows this to
[0%, 1.8%] at n = 400 per domain but samples around the same seven families, es-
tablishing robustness to parameter variation rather than coverage of an unknown
attack distribution. The logistics traces are structural twins of the MEDEVAC
ones, so their agreement measures portability rather than replication, and we
pool the two nowhere. φT is discharged on the unmodified MonPoly engine; φS
and φΣ remain reference implementations, so those numbers are ours rather
than an engine’s. Two enforcement defects (Sect. 5.4) were found only after the
rest of the evaluation was complete and every number here was re-run against
the corrected implementation; we cannot claim that audit was exhaustive.
    External. We compare against an AgentSpec-style per-call control that
we reimplemented, not against published implementations of Progent [25] or
GuardAgent [30]; those systems target a different interface, and a like-for-like
comparison would need a shared benchmark that does not yet exist for multi-
aspect obligations. The mission attacks were designed by us against our own
properties, and a suite designed against a specification will flatter it. This ver-
sion includes no independent external-corpus replay, so external attack coverage
remains an open validity limitation. The semantic aspect as implemented is
a fixed lexical cue matcher, so an attacker who paraphrases around the cues
defeats it: the laundering results establish that the aspect is separable and un-
covered by any spatial or temporal clause, and not that this detector is robust.
                   Multi-Aspect Runtime Verification of LLM-Based Agents        25

The language-model-in-the-loop experiment uses one small model and twelve
episodes per condition, so it establishes that the enforcement path functions
on model-generated behaviour rather than general robustness across models.
The golden hour, standoff distance, corridor width and freshness windows are
configurable mission-policy parameters rather than validated doctrinal values;
they set where each property fires, not whether the aspects separate.


7   Related Work

Agent safety and guardrails. AgentSpec [29] lets a developer write rules over
individual tool invocations; Progent [25] enforces least-privilege on the tool set
an agent may reach; GuardAgent [30] places a second model in a supervisory
role; LlamaGuard [12] classifies content. All are valuable and all are per-event:
each inspects a call, or a message, in isolation. The STAC line of work [20] is the
direct demonstration that this is insufficient, and AgentDojo [6] and SafeAgent-
Bench [31] supply the benchmarks. Our position is that per-event controls cannot
express the properties this paper is about, because those properties are proper-
ties of a trace and, more specifically, of several aspects of a trace at once.


Runtime verification engines. The engines this work targets are mature.
TeSSLa [5,14] and RTLola [9] provide stream-based monitoring; DejaVu [11,10]
provides first-order past-time monitoring over unbounded domains; Mon-
Poly/VeriMon [3,2] decides MFOTL, and MFOTL monitors have been dis-
tributed across the tiers of an IoT deployment [27]: that work spreads one logic
over a topology, where the question here is which aspects a clause constrains at
one point of enforcement. MonPoly is used unmodified for the temporal aspect
and the other mappings identify the intended formalism and its capability
boundary; the artefact carries the MFOTL encodings. The contribution is the
decomposition, the shared canonical stream making the aspects comparable,
and the fusing algebra.


Spatial and spatio-temporal specification. STREL [1] and SaSTL [22] established
monitoring over graphs of locations with distance-indexed modalities, and hier-
archical CPS monitoring has been applied to fielded systems [26]. Layered de-
ployments place engines at the device, gateway and cloud tiers of an edge-IoT
fleet [15,17], and a fabric of such monitors can be made to survive node loss and
delayed evidence [16]; those architectures distribute one notion of monitoring
across tiers, where the question here is how several aspects compose at a single
point of enforcement. Existing work interprets these logics over a single, physi-
cal, notion of space. Our departure is to observe that a release topology is also a
metric space once edges are weighted by domain crossings, and that placing both
sorts in one graph lets one monitor discharge obligations usually split between
geofencing and data-loss prevention.
26      N. Kekatos et al.

Assurance and accountability. Clause-grounded, provenance-carrying verdicts
speak directly to record-keeping and traceability obligations, including Article 12
of the EU AI Act [8] and the management-system requirements of ISO/IEC
42001 [13]. A refusal that names the aspects and the clause behind it is auditable
in a way that a classifier score is not.

Relation to our own work. This paper is deliberately single-agent: the compo-
sition is across aspects. A companion submission addresses composition across
agents in an LLM-enabled swarm over a distributed verification-aware fabric.
The two share no scenario, property, measurement or artefact; the cross-agent
aggregation, the messaging fabric and the swarm properties are entirely that
paper’s, and the multi-aspect decomposition, the location graph and the three
instantiations evaluated here are entirely this one’s.


8    Conclusion

Compliance obligations for autonomous decision-support agents are jointly spa-
tial, temporal and text-semantic, and are typically violated by none of their steps
and all of them together. We decomposed a policy clause into a typed triple over
a shared canonical event stream, interpreted the spatial aspect over a two-sorted
location graph in which mission geometry and release topology are one object,
and fused the aspect verdicts through a four-valued algebra whose provenance
makes every refusal auditable against the clause behind it. Across a casualty-
evacuation planner, a contested-sustainment planner and a civil data-handling
agent, no single aspect and no pair closed the attack suite, while the precaution-
ary composition closed the evaluated suite with no observed false positives and
microsecond-scale overhead. In closed-loop simulation the shield additionally re-
duced violations from 77% to zero while 80.5% of refused episodes recovered to
a compliant delivery, which shows that enforcement can preserve mission effec-
tiveness wherever a valid alternative exists, while correctly refusing the violating
action when no compliant alternative exists. For the evaluated obligation fami-
lies, full multi-aspect composition was the only tested configuration that closed
the suite. More broadly, the evaluation shows that a runtime-assurance claim
rests on three things together: correct obligations, complete mediation of con-
sequential actions, and trustworthy attribution of the evidence that discharges
their preconditions.

Future work. Four directions follow from the limitations above. Integrate ex-
ternal engines into the closed-loop harness, replacing the remaining reference
implementations: φS has never been executed on a stream engine here, and the
full timed φT is checked offline on MonPoly rather than inside the loop. Repeat
the closed-loop harness against an optimised attacker of the kind that produces
STAC’s rates, and against a weaker planner. Generate scenarios from indepen-
dently specified mission models rather than from seven families of our own, so
that coverage is tested beyond the structures we anticipated. And generalise
                    Multi-Aspect Runtime Verification of LLM-Based Agents            27

the guarded composition beyond its Boolean arming semantics, to uncertain
and nested guards and a formal treatment of guard provenance: the protected-
status pattern suggests that guard structure can support richer operators than
the guarded maximum used here. That last one is the most interesting formal
question this work has raised.

References
 1. Bartocci, E., Bortolussi, L., Loreti, M., Nenzi, L.: Monitoring mobile and spatially
    distributed cyber-physical systems. Formal Methods and Models for System Design
    (MEMOCODE) (2017). https://doi.org/10.1145/3127041.3127050
 2. Basin, D., Dardinier, T., Hauser, N., Heimes, L., Krstić, S., Raszyk, M., Schnei-
    der, J., Traytel, D., Zingg, S.: VeriMon: A formally verified monitoring tool. In:
    Theoretical Aspects of Computing (ICTAC). LNCS, vol. 13572, pp. 1–6. Springer
    (2022). https://doi.org/10.1007/978-3-031-17715-6_1
 3. Basin, D., Harvan, M., Klaedtke, F., Zalinescu, E.: MONPOLY: Monitoring usage-
    control policies. In: Runtime Verification (RV 2011). LNCS, vol. 7186, pp. 360–364.
    Springer (2012). https://doi.org/10.1007/978-3-642-29860-8_27
 4. Bauer, A., Leucker, M., Schallhart, C.: Runtime verification for LTL and TLTL.
    ACM Transactions on Software Engineering and Methodology 20(4), 14:1–14:64
    (2011). https://doi.org/10.1145/2000799.2000800
 5. Convent, L., Hungerecker, S., Leucker, M., et al.: TeSSLa: Temporal stream-
    based specification language. In: Brazilian Symposium on Formal Methods (SBMF)
    (2018). https://doi.org/10.1007/978-3-030-03044-5_10
 6. Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., Tramèr,
    F.: AgentDojo: A dynamic environment to evaluate prompt injection attacks and
    defenses for LLM agents. In: NeurIPS Datasets and Benchmarks (2024)
 7. Defense Innovation Unit: Thunderforge: AI for American defense — AI agents for
    military planning and operations. U.S. DoD prototype programme; initial mission
    partners U.S. Indo-Pacific and European Command (2025)
 8. European Parliament and Council: Regulation (eu) 2024/1689 laying down har-
    monised rules on artificial intelligence (ai act). Official Journal of the European
    Union (2024), http://data.europa.eu/eli/reg/2024/1689/oj
 9. Faymonville, P., Finkbeiner, B., Schledjewski, M., et al.: StreamLAB: Stream-based
    monitoring of cyber-physical systems. In: Computer Aided Verification (CAV)
    (2019)
10. Havelund, K., Peled, D.: First-order timed runtime verification using BDDs. In:
    Automated Technology for Verification and Analysis (ATVA). LNCS, vol. 12302,
    pp. 3–24. Springer (2020). https://doi.org/10.1007/978-3-030-59152-6_1
11. Havelund, K., Peled, D., Ulus, D.: First-order temporal logic monitoring with
    BDDs. In: Formal Methods in Computer Aided Design (FMCAD). pp. 116–123
    (2017). https://doi.org/10.23919/FMCAD.2017.8102249
12. Inan, H., Upasani, K., Chi, J., et al.: Llama Guard: LLM-based input-output safe-
    guard for human-AI conversations. arXiv preprint arXiv:2312.06674 (2023)
13. International Organization for Standardization: ISO/IEC 42001:2023 — infor-
    mation technology — artificial intelligence — management system. ISO/IEC
    42001:2023 (2023), https://www.iso.org/standard/81230.html
14. Kallwies, H., Leucker, M., Schmitz, M., et al.: TeSSLa: An ecosystem for runtime
    verification. In: Runtime Verification (RV). LNCS, vol. 13498. Springer (2022).
    https://doi.org/10.1007/978-3-031-17196-3_20
28      N. Kekatos et al.

15. Kekatos, N., Chintri, M., Katsaros, P., et al.: Hierarchical security monitoring
    for edge-IoT: A formal methods approach. In: IEEE International Conference on
    Cyber Security and Resilience (CSR). IEEE (2026)
16. Kekatos, N., Chintri, M., Katsaros, P., et al.: A resilient runtime-verification fabric
    for security monitoring of critical edge-IoT infrastructure. In: Critical Information
    Infrastructures Security (CRITIS). LNCS, Springer (2026)
17. Kekatos, N., Chintri, M., Katsaros, P., et al.: Hybrid hierarchical runtime ver-
    ification for edge-IoT security: Combining MonPoly and RTLola. In: Kieseberg,
    P., Skopik, F., Atli, B., Asplund, M. (eds.) Availability, Reliability and Security.
    ARES 2026 EU Projects Symposium Workshops. LNCS, vol. 16903, pp. 222–240.
    Springer, Cham (2027). https://doi.org/10.1007/978-3-032-37218-5_14
18. Koutidis, G., Kekatos, N., Nianios, T., Lekidis, A.: Constrained-action AI remedi-
    ation for SIEM/XDR via a NeMo-Guardrails proxy. In: IEEE International Con-
    ference on Cyber Security and Resilience (CSR). IEEE (2026)
19. Krygier, J., Lubkowski, P., Maslanka, K., et al.: Smart medical evacuation support
    system for the military. Sensors 24(14), 4581 (2024). https://doi.org/10.3390/
    s24144581
20. Li, J.J., He, J., Shang, C., et al.: STAC: When innocent tools form dangerous
    chains to jailbreak LLM agents (2025), arXiv:2509.25624
21. Lubkowski, P., Krygier, J., Sondej, T., et al.: Decision support system proposal for
    medical evacuations in military operations. Sensors 23(11), 5144 (2023). https:
    //doi.org/10.3390/s23115144
22. Ma, M., Bartocci, E., Lifland, E., Stankovic, J.A., Feng, L.: SaSTL: Spatial aggre-
    gation signal temporal logic for runtime monitoring in smart cities. In: Proceedings
    of the 11th ACM/IEEE International Conference on Cyber-Physical Systems (IC-
    CPS) (2020). https://doi.org/10.1109/ICCPS48487.2020.00013
23. North Atlantic Treaty Organization: Summary of the NATO revised artificial
    intelligence strategy. https://www.nato.int/cps/en/natohq/official_texts_
    227237.htm (2024), adopted 10 July 2024
24. Quach, V., Fisch, A., Schuster, T., et al.: Conformal language modeling. In: Inter-
    national Conference on Learning Representations (ICLR) (2024)
25. Shi, T., He, J., Wang, Z., et al.: Progent: Programmable privilege control for LLM
    agents. arXiv preprint arXiv:2504.11703 (2025)
26. Temperekidis, A., Kekatos, N., Katsaros, P.: Runtime verification for FMI-based
    co-simulation. In: Runtime Verification (RV). LNCS, vol. 13498. Springer (2022).
    https://doi.org/10.1007/978-3-031-17196-3_19
27. Tsigkanos, C., Bersani, M.M., Frangoudis, P.A., Dustdar, S.: Edge-based runtime
    verification for the Internet of Things. IEEE Trans. Serv. Comput. 15(5), 2713–
    2727 (2022). https://doi.org/10.1109/TSC.2021.3074956
28. U.S. Department of Defense, Chief Digital and Artificial Intelligence Office: Task
    force lima executive summary. https://www.ai.mil/ (2024)
29. Wang, H., Poskitt, C.M., Sun, J.: AgentSpec: Customizable runtime enforcement
    for safe and reliable LLM agents. In: Proceedings of the 48th IEEE/ACM Interna-
    tional Conference on Software Engineering (ICSE) (2026)
30. Xiang, Z., Zheng, L., Li, Y., et al.: GuardAgent: Safeguard LLM agents by a guard
    agent via knowledge-enabled reasoning. arXiv preprint arXiv:2406.09187 (2024)
31. Yin, S., Pang, X., Ding, Y., et al.: SafeAgentBench: A benchmark for safe task
    planning of embodied LLM agents. arXiv preprint arXiv:2412.13178 (2024)
