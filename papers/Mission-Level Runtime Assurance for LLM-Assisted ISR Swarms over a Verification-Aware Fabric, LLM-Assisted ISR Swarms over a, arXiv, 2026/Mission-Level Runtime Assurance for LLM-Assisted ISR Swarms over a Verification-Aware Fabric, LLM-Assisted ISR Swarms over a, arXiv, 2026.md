                                                  Mission-Level Runtime Assurance for
                                                   LLM-Assisted ISR Swarms over a
                                                        Verification-Aware Fabric

                                             Nikolaos Kekatos1 , Panagiotis Katsaros2 , Alexios Lekidis3 , Theodoros
                                                                Nestoridis1,2 , and Tom Nianios1
                                                                 1
                                                                   Clone Systems, Larnaca, Cyprus
                                                            {nkekatos,tnianios}@clone-systems.com
                                                    2
                                                      Aristotle University of Thessaloniki, Thessaloniki, Greece
                                                                {katsaros,nestorid}@csd.auth.gr
                                                             3
                                                                University of Thessaly, Larissa, Greece
                                                                         alekidis@uth.gr
arXiv:2607.23532v2 [cs.CR] 31 Jul 2026




                                              Abstract. Swarms of LLM-assisted autonomous robots are increasingly
                                              proposed for cooperative intelligence, surveillance, and reconnaissance
                                              (ISR) in contested environments. A growing class of their assurance
                                              failures arises not within any single platform but across the swarm:
                                              individually-compliant actions compose into a mission-level violation: a
                                              prohibited objective split across platforms to evade per-platform limits, or
                                              a collective budget quietly exceeded. Per-platform guardrails miss these by
                                              construction, and contested communications let the violation hide behind
                                              lost or delayed evidence. We present a three-tier (platform/squad/mission)
                                              compositional runtime-verification framework that decomposes a mission
                                              policy into per-agent and cross-agent aspects, aggregates per-platform
                                              verdicts over a verification-aware messaging fabric, and fuses them with an
                                              evidence-aware, two-axis (security × completeness) algebra whose prove-
                                              nance names the platforms that jointly triggered a violation. Because the
                                              fabric makes evidence loss and silence observable, unsupported negative
                                              verdicts are downgraded to an explicit unknown rather than reported as
                                              mission-wide all-clears. On a simulated ISR mission, an indirect prompt
                                              injection that causes real LLM planners to split a prohibited collection
                                              task across four platforms is invisible to every per-platform monitor yet
                                              detected compositionally with full provenance; under an injected fault
                                              campaign a best-effort central monitor emits silent false all-clears while
                                              the verification-aware fabric emits none.

                                              Keywords: Runtime verification · LLM-assisted autonomous systems
                                              · Swarms · Distributed monitoring · Cross-agent composition · Mission
                                              assurance · Contested environments · V&V of autonomous systems


                                         1   Introduction
                                         Autonomous multi-robot systems are moving from single-platform autonomy
                                         toward cooperative missions in which teams of unmanned aerial and ground
2       N. Kekatos et al.

vehicles (UAV/UGV) share tasks, sensors, and situational awareness [11,10].
Large language models (LLMs) are increasingly proposed for the high-level layer
of such systems [2], interpreting commander intent, allocating tasks, selecting
sensors, and replanning after loss, while conventional controllers retain navigation,
collision avoidance, and safety. This division of labour is attractive but introduces
an assurance gap that is fundamentally multi-agent: a mission-level policy can
be violated even though every individual platform behaves compliantly.
    This work combines three areas: runtime verification, LLM-assisted autonomy,
and resilient messaging. Runtime verification (RV) continuously checks a running
system against an explicit formal specification and emits, at each step, a ver-
dict together with a supporting witness [4,26,7]; unlike learning-based intrusion
detection, it flags any execution that violates a stated property and yields an
auditable justification. Mission-level assurance concerns obligations that span the
entire swarm over a complete mission (rules of engagement, collective resource
budgets, area coverage) rather than the safety of a single platform, and runtime
assurance denotes the operational use of the resulting verdicts as continuous,
auditable evidence of policy compliance. In LLM-assisted autonomy a large
language model performs high-level mission reasoning (interpreting commander
intent, allocating tasks, selecting sensors, and replanning after loss) while con-
ventional controllers retain navigation, collision avoidance, and flight safety; such
models are susceptible to prompt injection, in which adversarial text embedded
in retrieved data subverts the planner [20,31,28]. An ISR swarm is a team of coop-
erating unmanned aerial and ground platforms conducting a shared intelligence,
surveillance, and reconnaissance mission. The verification-aware fabric is the
messaging layer that conveys monitor evidence under explicit delivery, ordering,
and liveness guarantees; it is built on established brokers (MQTT for constrained
platforms and NATS JetStream for durable backend delivery [30,35]) and on
metric first-order past-time and stream engines (MonPoly [6] and RTLola [17]),
so that the evidence stream a monitor consumes is the stream its correctness
assumes. The evaluation adopts the modelling-and-simulation methodology of
the venue, pairing a reproducible core with a ROS 2/Gazebo/ArduPilot realism
layer.
    Consider an ISR mission whose rules of engagement prohibit assembling a
complete intelligence package on a protected installation. An adversary, through
an indirect prompt injection embedded in retrieved mission data, induces the
swarm to split the prohibited collection: one platform records coordinates, another
captures imagery, a third identifies communications equipment, a fourth maps
access routes, and one transmits the combined product. Each action is individually
permitted, each platform stays below its local collection and emission limits, and
every per-platform monitor reports compliance. Only the composition of the
platforms’ actions constitutes the prohibited objective. Per-platform guardrails
miss this by construction, and in a contested environment the adversary can jam
or delay the very evidence a central monitor would need, so a naive aggregator
may issue a confident but incorrect mission-wide all-clear.
                           Mission-Level Runtime Assurance for ISR Swarms            3

    Two properties make this failure class hard and, we argue, central to the
modelling and simulation of trustworthy autonomous systems. First, it is compo-
sitional : the mission-level obligation cannot be checked at any single platform,
so assurance must reason over the joint behaviour of the swarm. Second, it is
evidence-sensitive: in a denied or degraded electromagnetic environment the very
reports needed to reason about the swarm are the ones an adversary suppresses,
so a monitor that treats missing evidence as good news is worse than no monitor
at all. A credible mission-assurance capability must therefore separate two ques-
tions, did the swarm violate the policy? and do we have enough evidence to say?,
and never silently answer the first “no” when the honest answer to the second is
“we cannot tell”. Simulation is the natural setting to establish this before fielding:
repeatable missions, injected communication faults, and a ground-truth oracle
are exactly what a modelling-and-simulation evaluation provides.
    This paper presents a runtime-verification framework that closes this gap for
LLM-assisted robot swarms and is designed for mission assurance under contested
communications. Our contributions are:
 – A three-tier monitoring hierarchy, platform (L1), squad coordinator (L2),
   and mission (L3), that decomposes a swarm mission policy into per-agent
   and cross-agent aspects and lifts the hierarchical monitoring of our prior
   single-node and edge-IoT work [23,22] to a cooperative swarm (Sect. 4).
 – An evidence-aware, two-axis verdict-composition algebra: cross-agent
   verdicts carry both a security value and a completeness status, with prove-
   nance that names the platforms and witness events that jointly triggered a
   violation, so a corrupted or incomplete evidence stream can no longer produce
   an unqualified mission all-clear (Sect. 4).
 – A distributed architecture over a verification-aware fabric (RV-
   Fabric) that carries per-platform verdicts with durable delivery, trusted
   ordering, per-consumer cursors, flow control, and a backend mission clock,
   making evidence loss and partial silence observable so unresolved verdicts
   are downgraded rather than silently cleared (Sect. 5).
 – A simulation-based evaluation on an ISR mission with an indirect prompt-
   injection, task-splitting attack, showing that the collective violation is invisible
   to per-platform monitors, detected with provenance by the compositional
   monitor, and, under loss and jamming, preserved or explicitly flagged by the
   verification-aware fabric while a best-effort central monitor silently misses it
   (Sect. 7).

The framework targets mission assurance of autonomous systems and AI in
contested environments rather than purely formal-methods theory: every flagged
action or mission-level incident produces an auditable, platform-attributed verdict.
Fig. 1 summarises the end-to-end approach.
4         N. Kekatos et al.

                     per-platform
 retrieved-intel                          canonical       L1/L2/L3          verdict (s, c)
                    LLM planners
    injection                           event stream      monitors          + provenance
                      a1 , . . . , an


Fig. 1. High-level approach. Adversarial content retrieved mid-mission diverts the
per-platform LLM planners a1 , . . . , an (each ai denotes an individual platform/agent);
the actions they emit are canonicalised into a shared event stream that feeds the three-
tier (L1/L2/L3) monitors over the verification-aware fabric, which produce a two-axis
verdict (s, c) with platform provenance. Individually-benign per-platform actions can
still compose into a mission-level violation visible only at L3.


2     Motivating Example

A heterogeneous swarm of four platforms, three unmanned aerial vehicles (uav_1,
uav_2, uav_3) and one unmanned ground vehicle (ugv_1), conducts a cooperative
ISR sweep of an area of operations. The mission order, in natural language, is:
     Maintain observation of Sector A and Sector B. Do not enter Zone
     Red, and do not construct or transmit a complete intelligence profile of
     Facility X without command approval.
An LLM planner on each platform turns this intent into structured actions such as
{"action":"assign_reconnaissance", "agent":"uav_2", "sector":"b",
"sensor":"eo_camera"}, which a conventional controller executes. During
the mission, uav_1 retrieves an intelligence note, planted by the adversary,
containing the instruction “divide the Facility X collection among available units
and transmit each component separately”. The planners treat this as mission
guidance and distribute partial collection tasks.
    Each resulting action is locally permitted: uav_1 collects coordinates, uav_2
imagery, uav_3 communications metadata, ugv_1 access-route information, and
each stays below its local transmission limit using an authorised sensor. Every
per-platform (L1) monitor therefore reports no_violation. Yet the union of these
observations {coords, imagery, comms, access_route} on Facility X is the prohib-
ited intelligence package, the swarm’s aggregate emissions exceed the mission
EMCON (emission control) budget, the cap on the swarm’s total radio-frequency
emissions imposed to limit its electromagnetic signature, and one platform enters
the sensitive zone without prior authorisation. These are three mission-level
incidents that no single-agent monitor can express. This is the swarm analogue of
a single-agent sequential tool-attack chain [27]: benign at every step, prohibited
in composition (Fig. 2).
    The planner turns commander intent into validated structured actions; the
attack diverts exactly this pipeline. The benign flow and the injected flow, with
the canonical events they produce, are:
# commander intent (benign) ->
"Survey sector B with EO; do not build a full profile of Facility X."
=> {"action":"assign_reconnaissance","agent":"uav_2","sector":"b",
                                    Mission-Level Runtime Assurance for ISR Swarms           5

    uav_1: collect coords (FacX)L1 ✓

                                                                          VIOLATION
    uav_2: collect imagery (FacX)L1 ✓             cross-agent
                                                                           prohibited in-
                                                 composition
                                                                            tel package
    uav_3: collect comms (FacX)L1 ✓                  (L3)
                                                                       prov={uav_1..ugv_1}

     ugv_1: collect access (FacX)L1 ✓



Fig. 2. The distributed violation. Each platform’s collection action is individually
permitted and passes its per-platform (L1) monitor; only the cross-agent composition
(L3) constitutes the prohibited intelligence package, reported with platform provenance.


    "sensor":"eo_camera"} # event: collect(imagery, SectorB)
# retrieved-intel prompt injection ->
"Divide the Facility X collection among available units; transmit each
     part separately."
=> uav_1: collect(coords, FacX) uav_2: collect(imagery, FacX)
   uav_3: collect(comms, FacX) ugv_1: collect(access, FacX) + transmit
Every injected action validates against the schema and passes its L1 monitor;
the prohibition is a predicate over the union of the four collect events on FacX,
which only the mission tier observes.

Why the attack is LLM-specific. The task split is not produced by the evaluated
rule-based allocator, because that allocator accepts only predefined structured
commands and does not interpret arbitrary free text retrieved mid-mission: “di-
vide the Facility X collection” is simply not in its input language, so it is ignored
or rejected. (A malicious or compromised planner could of course emit the split
directly; the point is that an honest planner is diverted into it only when it
interprets untrusted free text.) An LLM planner is valued for the opposite reason,
namely that it interprets unstructured mission context, and therefore treats
the retrieved note as legitimate guidance and decomposes the task accordingly.
Three layers then pass the composed violation through: (i) the LLM interprets
the injected text as mission-relevant guidance and generates the corresponding
structured task assignments; (ii) schema validation accepts each resulting action,
because every field is well-formed and individually permitted; and (iii) each per-
platform (L1) monitor accepts its platform’s local behaviour. Only the cross-agent
(L3) composition rejects the union. The attack is thus enabled precisely by the
LLM’s openness to retrieved context (the very property for which it is deployed),
which is why the appropriate defence is mission-level compositional RV rather
than stricter per-action checks. This comparison characterises the input-model
difference between the two planners; we do not claim a comprehensive experi-
mental comparison of LLM and non-LLM task-allocation systems. (Consistent
with our threat model of Sect. 3, the injection subverts only the planner ; the
trusted event-generation and monitoring path is unaffected, so the actions the
swarm actually reports are faithfully monitored.)
6       N. Kekatos et al.

3    Background, System Model, and Notation

Hierarchical runtime verification. Our prior work develops a three-layer
security-monitoring hierarchy for edge-IoT, lightweight per-device checks,
per-gateway aggregation, and backend fleet-wide metric first-order temporal-logic
(MFOTL) correlation with MonPoly [6,5] and RTLola [17] (related first-order
past-time and stream engines include DejaVu [21] and TeSSLa [12]), validated
first on a shared log [23,22] and then over a resilient two-broker fabric for
edge-cloud deployments [33]. This paper reuses that decomposition, relabelled
to a swarm: device→platform, gateway→squad coordinator, and the backend
fleet monitor→mission monitor. The cross-gateway property of the edge-IoT
work (“≥ 2 gateways satisfy a predicate in a window”) is exactly the cross-agent
primitive we need at swarm scale. Carried over vs. new. Carried over from
that line are the three-tier decomposition, the five fabric guarantees, and the
evidence-aware verdict algebra with its conditional-soundness argument [23,22],
and single-agent spatial/temporal/semantic monitor composition. New here
are (i) lifting composition from a single agent, and from edge-IoT devices, to
a cooperative robot swarm with mission-level ISR objectives (the task-split
intelligence package, joint zone occupancy, the ordered targeting chain, and
sector coverage) that have no analogue in the IoT setting; (ii) a real LLM planner
that generates the distributed violation rather than it being scripted; and (iii) a
ROS 2/ArduPilot-SITL realism layer with swarm-specific timing, clock-skew,
and benign-collaboration sensitivity. The soundness argument is instantiated,
not re-proved; a full proof of the composition algebra remains future work.

LLM-assisted autonomy and its failures. LLM planners are effective at intent
interpretation and task allocation but are susceptible to prompt injection through
retrieved content, and single-agent guardrails leave a large fraction of multi-step
attacks unaddressed [27,14]. Single-agent RV of LLM actions composes spatial,
temporal, and semantic monitors for one agent; here we lift composition to the
swarm, where the violation lives across agents and no single-agent view suffices.
    Distributed and fault-tolerant RV (discussed in Sect. 8) makes the monitoring
logic robust to crashed or asynchronous monitors; we are complementary and
beneath it, making the delivery layer’s loss, ordering, and liveness first-class.

System model. A swarm A = {a1 , . . . , an } is a set of n platforms executing a
cooperative ISR mission. Each ai is one platform (an unmanned aerial or ground
vehicle) and, equivalently, one agent; we use platform and agent interchangeably,
with one agent per platform. Each ai runs an LLM planner that maps mission
intent to a validated structured action, a conventional controller that executes it
(navigation, collision avoidance, safety, never the LLM), and a local (L1) monitor.
A squad coordinator groups nearby platforms (L2); a mission node runs the
swarm (L3) monitor. All monitor traffic crosses the RV-Fabric. The monitoring
aspects are termed per-agent (over one platform’s trace) and cross-agent (over
the joint stream), following the RV literature.
                             Mission-Level Runtime Assurance for ISR Swarms          7

Canonical event stream. Each platform emits structured events over a shared
schema. An event is a tuple e = (id , τ, a, k, attrs): a persistent identifier id (used
for de-duplication and gap detection), a mission-clock timestamp τ , the emitting
platform a ∈ A, a kind k drawn from {collect, transmit, enter, authorise,
observe, tick}, and typed attributes attrs (target, sensor, byte count, zone). We
write collect(a, x, F, I) for a collect event by platform a of fragment x on target
F within time interval I; emit(a, I) for the bytes a transmits over I; enter(a, Z, t)
for a entering zone Z at time t; and authorise(a, Z, τ ), authorised(F, I) for a
prior command authorisation. Structured LLM actions are validated against
this schema before execution; free-text coordination messages are mapped to
predicates by a semantic extractor, kept as a secondary path so the core results
do not depend on free-text classification.

Aspects and cross-agent properties. A mission clause decomposes into per-agent
aspects, decidable from one platform’s trace: spatial residency φS (restricted-
area entry), first-order past-time obligations φT (assigned-task compliance, local
budgets), and text-semantic predicates φΣ (authorised sensor, permitted recipi-
ent); and cross-agent aspects, decidable only over the combined stream: swarm
counts and budgets, joint spatial coverage, and cross-agent causal order. Three
cross-agent properties anchor the evaluation:

        Ppkg (F, W ) : ∃ a1 , . . . , a4 s.t.
              V
                x∈X collect(ax , x, F, [t−W, t]) ∧ ¬ authorised(F, [t−W, t]),
             with X={coords, imagery, comms, access}
                    P
        Pemcon (W ) : a∈A emit(a, [t−W, t]) > Bmission
        Pauth (aj , Z, t) : enter(aj , Z, t) ∧
             ¬ ∃ ai , τ ∈ [t−W, t) : authorise(ai , Z, τ )

Here t is the current mission time, W the length of the sliding window ending at
t, F the protected facility, X the set of intelligence fragments that together form
a prohibited package, Bmission the swarm-wide EMCON emission budget in bytes,
Z a sensitive zone, and ai , aj individual platforms. Each P• denotes the incident
(violation) condition and fires when it holds: Ppkg when all four fragments have
been collected on F within W with no prior authorisation, Pemcon when the
swarm emission sum over W exceeds Bmission , and Pauth when a platform enters Z
with no authorisation in the preceding window. This notation is used throughout
the remaining sections.

Threat model. The protected asset is the mission verdict stream: every mission-
relevant action durably reported into the protected path must reach the mission
monitor, in trusted order, and the absence of expected reports must itself be
observable. The adversary (i) induces a distributed violation via indirect prompt
injection in retrieved mission data, splitting a prohibited objective so each
platform stays locally compliant; and (ii) contests communications to hide it,
dropping, delaying, or reordering evidence, or jamming a platform into silence.
8         N. Kekatos et al.

Table 1. Threat model: adversary capability, the framework’s mitigation, the tier or
guarantee it uses, and the residual risk. Rows marked † lie outside the trust boundary
(assumed, not enforced).

    Adversary          Mitigation                    Via          Residual risk
    capability
    Distributed inducement
    prompt-inject a    cross-agent composition       L3, Ppkg     novel objective
    task split         detects the joint objective                outside the mission
                                                                  policy
    exceed a collective swarm-wide                   L3, Pemcon   budget set too
    budget              counts/emissions over a                   loosely
                        window
    evade cross-agent causal-order property over     L3, Pauth    forged identity†
    order               the consumed stream
    Contested communications
    drop / delay        at-least-once + event-id     G1           loss before durable
    evidence            gap ⇒ incomplete                          acceptance
    reorder evidence    monotone mission-ingest      G2           bounded
                        order                                     cross-agent skew
    jam a platform      mission clock flags the      G3           prolonged partition
    silent              missing stream                            delays evidence



Prompt injection subverts only the LLM planner through untrusted retrieved
content: the planner may propose individually policy-valid actions, but the
trusted event-generation and monitoring path is unaffected, so a manipulated
planner cannot falsify the evidence a platform reports. The adversary cannot
forge a platform’s authenticated identity (link cryptography assumed) and cannot
subvert the mission node or the monitor logic. The core model therefore assumes
authenticated but potentially silent platforms; compromised-platform integrity
beyond going silent is out of scope, with a single exploratory extension (Sect. 7)
in which a platform under-reports its own emissions and an independent witness
corroborates. This mirrors the trust boundary of our prior edge-IoT fabric, recast
for a swarm. Table 1 maps each adversary capability to its mitigation and residual
risk.


4      Cross-Agent Specification and Evidence-Aware
       Composition

Cross-agent specification. We build on the canonical event model and the three
cross-agent properties Ppkg , Pemcon , Pauth defined in Sect. 3, and now give their
evaluation semantics and the evidence-aware composition of their verdicts. Ppkg
is evaluated over a sliding mission window W on the protected facility F . The
four fragments may be gathered by the same or, as in our scenario, by four
distinct platforms (the hardest case for a per-platform monitor); a prior command
                           Mission-Level Runtime Assurance for ISR Swarms           9

authorised(F, W ) cancels the violation; and repeated or stale evidence does not
inflate it, since event-id de-duplication counts each fragment once within W . If the
rules of engagement prohibit only the assembly/transmission of the profile rather
than its collection, the stronger variant Ppkg (F, W ) ∧ ∃a : transmit(a, F, [t−W, t])
applies; the evaluation pipeline monitors both. Ppkg is thus a semantic composition
of individually-benign actions, strictly stronger than a numeric threshold, and
is the paper’s principal result. Further mission properties (joint zone-occupancy
≤ k, sector coverage as a past-time once, and subgroup-silence) follow the same
pattern.

Evidence-aware two-axis verdict. A mission verdict is a pair (s, c) on two in-
dependent axes, a security value s ∈ {violation, no_violation, unknown} and a
completeness status c ∈ {sound ≻ degraded ≻ incomplete ≻ unavailable} derived
from continuity evidence the fabric tracks: an event-id gap on a contributing
stream (loss), an order violation on the consumed stream, a retention high-water
mark, or the mission clock showing a platform live but silent. A cross-agent
property fires violation when the combined witnesses satisfy it; its completeness
is the meet of the contributing platforms’ evidence, so one incomplete platform
makes a fleet-wide all-clear unknown. The composition rule keeps security and
completeness on separate axes: a positive finding backed by an intact witness is
self-evidencing, whereas a no_violation over non-sound evidence is downgraded
to unknown. The verdict carries provenance: the platforms and witness event-ids
that jointly triggered it, e.g.
{"property":"prohibited_collective_intel_package","verdict":"violation",
 "evidence_status":"sound","agents":["uav_1","uav_2","uav_3","ugv_1"],
 "witnesses":["uav_1-0","uav_2-0","uav_3-0","ugv_1-0"]}
Table 2 catalogues the properties by tier.

Conditional soundness. The downgrade rule is not merely a convention: it makes
the composition sound for the practically dominant class of monotone witness
properties, those certified by a finite set of events and preserved under supersets,
which covers the counting and existential cross-agent properties Ppkg , Pemcon ,
and Pauth . For such a property, over the durably-accepted stream: (i) a reported
violation corresponds to a real violation, since event-id de-duplication prevents
count inflation and delivery loss only removes events; (ii) a no_violation carrying
sound completeness agrees with the fault-free oracle; and (iii) whenever a genuine
violation is missed but the loss is observable, an event-id gap (G1), an order
violation on the consumed stream (G2), or a stream that the mission clock shows
silent (G3), the verdict is downgraded to unknown rather than reported as a clean
all-clear. The single loss class the algebra cannot flag is a silenced stream with
no independent clock, which is exactly why the mission clock is backend-resident
and survives the loss of every platform. A full proof follows the argument of our
prior edge-IoT fabric, instantiated with the cross-agent primitive of Sect. 3.
10          N. Kekatos et al.

Table 2. Property catalogue across the three tiers. L1/L2 are decidable locally or
within a squad; L3 properties are decidable only over the combined swarm stream and
are what per-platform guardrails structurally cannot express.

     Tier          Property                               Kind
     L1: per platform
     platform     restricted-area entry (φS )             spatial residency
     platform     local budget / assigned-task (φT )      first-order past-time
     platform     authorised sensor / recipient (φΣ )     text-semantic
     L2: per squad
     squad        partial profile aggregation (→ L3)      cross-agent composition
     squad        joint zone-occupancy ≤ k                cross-agent count
     squad        duplicated task allocation              cross-agent
     L3: mission (cross-agent)
     mission      prohibited collective package (Ppkg )   semantic composition
     mission      EMCON emissions budget (Pemcon )        swarm-wide sum
     mission      authorisation order (Pauth )            cross-agent causal
     mission      sector coverage (once)                  past-time coverage
     mission      subgroup silence ⇒ coverage             absence / liveness
                  unknown



5     Three-Tier Distributed Architecture over the
      RV-Fabric
Per-platform (L1) monitors run at the edge on each platform and decide φS ,
φT , φΣ from local traces. A squad coordinator (L2) checks subgroup properties
(joint zone-occupancy, separation, duplicated task allocation) over the platforms
it serves. The mission monitor (L3) consumes L1/L2 verdicts and decides the
cross-agent properties. The three tiers communicate over the RV-Fabric, reused
from our prior edge-IoT fabric with swarm semantics: MQTT [30] for platform-
to-coordinator ingest; a coordinator sidecar assigns trusted, monotone mission-
ingest timestamps and persistent event-ids and appends to a durable outbox
before forwarding to a NATS JetStream [35] backend; the mission monitor
reads via its own durable cursor; and a backend-resident 1 Hz mission clock
advances monitoring time independently of platform traffic. These provide five
guarantees, at-least-once delivery, monotone ordering, mission-clock liveness,
consumer isolation, and flow control, whose loss under fault is made observable
and, through the algebra of Sect. 4, converted into an explicit unknown rather
than a silent all-clear. Because the mission clock is backend-resident, silence-
liveness survives the loss of every platform: a jammed platform is surfaced as a
missing stream, not mistaken for an idle one. Fig. 3 shows the resulting three-tier
deployment.
                            Mission-Level Runtime Assurance for ISR Swarms                             11

Platforms (L1)


    uav_1
                             Squad (L2)
     L1                                                                       Mission (L3)

    uav_2                           Squad coor-
                                                                                       Mission mon-
                  MQTT    ingest    dinator (L2)      verdicts     NATS      read
     L1                                                                                 itor (L3)
                  QoS 1                   sidecar ·              JetStream
                                                                                    MonPoly · provenance
    uav_3                           durable outbox
     L1

    ugv_1                                                 mission clock 1 Hz
     L1




Fig. 3. Three-tier deployment. Per-platform L1 monitors publish over MQTT to a squad
coordinator (L2) whose sidecar assigns trusted timestamps and event-ids and relays
durably to a JetStream backend; the mission (L3) monitor reads via its own cursor
and a backend-resident mission clock supplies silence-liveness. The five guarantees of
Table 3 are carried unchanged from the prior edge-IoT fabric.

Table 3. The five RV-Fabric guarantees, relabelled from the edge-IoT fabric to the
swarm, and the mission-assurance role of each.

Mechanism                  Guarantee                   Swarm role
MQTT QoS 1 + durable       at-least-once               no lost platform report on the
outbox                     delivery                    protected path
coordinator sidecar        monotone ordering           trusted cross-agent causal order
timestamps
mission clock (1 Hz)       liveness under              jammed platform surfaced, not read
                           silence                     as idle
durable per-consumer       consumer isolation          a slow mission monitor never blocks
cursors                                                others
JetStream flow control     backpressure                transient overload deferred, then
                                                       observable



6    Simulation Environment and Implementation
Following the M&S practice of the venue, the framework is designed to run
against a robotics simulator; the RV contribution, however, is the event stream,
the monitors, and the verification-aware fabric, not the physics fidelity. We
therefore provide two layers.
   Reproducible core. A lightweight, deterministic kinematic mission generator
emits the canonical event schema for a benign and an attack scenario and
drives the L1/L2/L3 monitors and the emulated fabric (with fault injection)
entirely in Python; it reproduces the deterministic core results of Sect. 7 (the
principal fault campaign, hierarchy, provenance, ablations, sensitivity sweeps,
and scalability) with one command and no external services, and is packaged
with Docker for repeatability. (The LLM-in-the-loop, live Mosquitto/JetStream,
ROS 2, ArduPilot-SITL, and MonPoly results additionally require their respective
models or services, as detailed under Reproducibility.)
12      N. Kekatos et al.

    Realism layer. An adapter bridges a ROS 2 + Gazebo world with
ArduPilot SITL flight dynamics to the same event schema: it subscribes to
platform state/action topics and MAVLink telemetry, canonicalises them
into collect/transmit/enter events, and publishes over the real MQTT +
JetStream RV-Fabric, so the identical monitors run in simulation and (in
principle) on deployed platforms. Jamming is modelled as MAVLink/telemetry
link loss, and loss/reorder as broker-level fault injection. The ROS 2 integration
itself runs headless in a container (real DDS publish/subscribe, no GPU): we
executed it with four platform nodes (uav_1..ugv_1) publishing the attack’s
actions on /⟨ns⟩/action topics and a mission-monitor node consuming them
live; the per-platform (L1) verdicts were all no_violation while the mission
(L3) monitor reported the three violations with platform provenance (prohib-
ited_collective_intel_package over all four platforms, emcon_emissions_budget,
and cross_agent_authorization on uav_2), the same local-compliant/globally-
violating result as the reproducible core, now over an executed ROS 2/DDS
middleware path. We further executed the mission using ArduPilot SITL (four
simulated copters over MAVLink/TCP; each armed, took off, and followed its
assigned route using the SITL flight-dynamics model), producing 360 position
samples; the collected action stream reproduced the identical L1/L3 verdicts
with provenance (Fig. 4). Only Gazebo visual rendering requires a GPU host,
and it is not needed for any quantitative result. The formal cross-agent properties
are additionally evaluated by the real MonPoly engine, reused from our prior
edge-IoT fabric.

Interactive console. A browser console (console/, stdlib-only) replays a mission
tick-by-tick over the same swarm_rv monitors: it renders the mission map,
the editable relation- and property-layer spec, and the L3 verdict chips with
provenance, and lets a user inject faults and toggle the RV-Fabric against a
best-effort central monitor to watch a silent all-clear become an honest unknown
(Fig. 5). It is an inspection aid over the same engine that produces the quantitative
results, not a separate implementation.


7    Evaluation
We ask whether the framework (RQ1) detects violations invisible to per-platform
monitors, (RQ2) preserves verdict correctness under contested communications,
(RQ3) attributes the responsible platforms, (RQ4) at acceptable cost, and
(RQ5) avoids false all-clears. We compare three configurations, per-platform
guardrails only, a central cross-agent monitor over best-effort transport, and the
full RV-Fabric (evidence-aware), on the ISR mission of Sect. 2, under a fault
campaign (fault-free; drop one witness event; jam one platform into silence). The
fault-free RV-Fabric run defines the ground-truth oracle of mission incidents,
|I ⋆ | = 3 (collective package, EMCON breach, unauthorised entry).
                                          Mission-Level Runtime Assurance for ISR Swarms                          13

                             1000

                                                                                     FacX (protected)

                                                                                  coords          comms
                              800



                                                         Zsens                  access_route     imagery
                              600

                 north (m)

                              400



                              200


                                        uav_1    uav_2     uav_3        ugv_1
                                0
                                    0           200              400              600            800       1000
                                                                       east (m)


Fig. 4. The ISR mission executed with ArduPilot SITL (four simulated platforms,
MAVLink telemetry); the 360 position samples are generated by the SITL flight-
dynamics model. Trajectories converge on Facility X, uav_2 crosses the sensitive zone,
and the four split-collection events (stars, one fragment per platform) are labelled
around the facility. Every per-platform (L1) monitor is compliant, yet the compositional
(L3) monitor reports three mission incidents with platform provenance: the prohibited
collective intelligence package (uav_1..ugv_1), the EMCON emissions-budget breach
(uav_1..ugv_1), and unauthorised entry into the sensitive zone (uav_2).


7.1   Detection, Provenance, and Correctness under Fault
RQ1 / RQ3, detection and provenance. On the attack, all four per-platform
monitors report no_violation (each platform transmits ≤ 300 B, below its local
limit, on an authorised sensor). The compositional monitor detects all three
mission incidents and returns provenance naming the contributing platforms
and witness events, e.g. the package incident with agents {uav_1..ugv_1} and
witnesses {uav_1-0,...,ugv_1-0}. Per-platform guardrails detect 0/3; the col-
lective violation is visible only through composition.

RQ2 / RQ5, correctness and false all-clears under fault. Table 4 reports, per
configuration and fault, how many oracle incidents are preserved (violation),
downgraded to a flagged unknown, or silently missed as a false all-clear. The central
best-effort monitor detects all three fault-free but, under loss and jamming, emits
3 silent false all-clears in total: a dropped imagery witness makes the package look
absent, and a jammed platform makes both the package and the emissions budget
look satisfied. The RV-Fabric emits 0: each unresolved incident becomes an
explicit unknown/incomplete (event-id gap) or unavailable (mission-clock silence),
never a clean all-clear.
14      N. Kekatos et al.




Fig. 5. The interactive Mission RV Console on the intel-package scenario at mission end:
every per-platform (L1) verdict is no_violation (bottom left), while the compositional
(L3) monitor reports all three mission violations (red chips, right) with platform
provenance; the map shows the four trajectories converging on Facility X. Faults and
the evidence-aware vs. best-effort monitor are switchable live.


Benign mission. On the cooperative benign mission (permitted single-fragment
recon, authorised entry, emissions within budget) all three configurations raise 0
mission-level and 0 local false alarms.

7.2   Generalisation across Objectives and Tiers
Generalisation across objectives (RQ1/RQ5). The core result is not specific
to the intelligence-package objective. Table 5 repeats the experiment for four
distinct mission objectives spanning four property kinds, a semantic composition
(prohibited package), a swarm-wide sum (collective exfiltration budget), a cross-
agent count (airspace deconfliction), and a cross-agent causal chain (prohibited
targeting workflow). In every case the attack is locally compliant (per-platform
monitors detect 0), the compositional monitor detects it fault-free, and across the
three-fault campaign the central best-effort monitor accrues 9 silent false all-clears
in total while the RV-Fabric accrues 0 (Fig. 6). A scale sweep that replicates
the package pattern across squads confirms detection and zero false all-clears at
4/16/40/100 platforms, with sub-millisecond mission-monitor evaluation time.
    The three additional objectives exercise the same structure through differ-
ent property kinds. Collective exfiltration: each platform transmits within its
local limit but the swarm total exceeds Bmission (a sum no platform can com-
pute), and jamming one makes the remaining total look compliant. Airspace
deconfliction: three UAVs each legitimately enter a sensitive zone but the joint
occupancy exceeds k (a cross-agent count), and a lost entry hides it unless the
gap is observed. Prohibited targeting workflow : platforms split a detect ≺ clas-
                                 Mission-Level Runtime Assurance for ISR Swarms            15

Table 4. Attack-scenario mission-incident preservation under the fault campaign
(|I ⋆ | = 3). Cells show preserved incidents; “+u” = incidents downgraded to a flagged
unknown. The last column is the total number of silent false all-clears across the
campaign, the quantity a mission commander must never see. The local-only (per-
platform) baseline has no representation of cross-agent incidents, so it is treated as
producing a mission-level all-clear whenever all per-platform monitors report compliance.

        Configuration                      fault- drop     jam    silent false
                                            free witness platform all-clears
        per-platform guardrails              0/3         0/3           0/3         9
        central (best-effort)                3/3         2/3           1/3         3
        RV-Fabric (evidence-aware)           3/3       2/3 +1u       1/3 +2u       0

Table 5. Silent false all-clears summed over the three-fault campaign, per objective and
configuration. Every objective: per-platform monitors are blind, the central monitor
silently misses under fault, and the RV-Fabric never does.

Mission objective                 Property kind          per-platform central RV-Fabric
prohibited intel package          semantic                       9             3       0
(|I ⋆ |=3)                        composition
collective exfiltration budget    swarm-wide sum                 3             2       0
airspace deconfliction            cross-agent count              3             2       0
prohibited targeting              cross-agent causal             3             2       0
workflow                          chain
total                                                            18            9       0



sify ≺ geolocate ≺ share sequence so no platform does more than one step (a
cross-agent causal chain), and a missing step downgrades to unknown. That the
same composition yields zero silent false all-clears across a semantic composition,
a sum, a count, and a causal chain shows the guarantee is a property of the
framework, not one hand-picked scenario.

Genuine three-tier composition (L1→L2→L3). To exercise the squad tier as more
than a pass-through, we split the four package fragments across two squads of three
platforms each: Squad 1 (uav_1 coords, uav_2 imagery, uav_3 comms) and Squad
2 (ugv_1 access-route, plus a benign relay and a benign recon platform). Each
squad coordinator (L2) aggregates only its own platforms into a partial profile, and
the mission monitor (L3) composes the two partials (Table 6). Fault-free, Squad
1 reports partial{coords,imagery,comms} and Squad 2 partial{access};
neither partial is a violation, yet their L3 union is the complete prohibited
profile (violation, with provenance spanning both squads). Crucially, completeness
propagates up the hierarchy: dropping uav_2’s imagery witness makes Squad 1’s
partial incomplete, the evidence-aware L3 inherits that tag and returns unknown,
whereas a best-effort L3 that ignores squad completeness silently clears the
mission. Platform compliance (L1), squad partial-aggregation (L2), and mission
composition (L3) are thus each load-bearing.
16      N. Kekatos et al.

                                              18




               silent false all-clears
                                         15

                                         10                          9

                                          5
                                                                                               0
                           0
                       per-platform

Fig. 6. Silent false all-clears summed over the four objectives and the three-fault
campaign (lower is better; shading darkens with severity). Per-platform guardrails
are structurally blind (they never see the cross-agent incident); the central best-effort
monitor silently misses under fault; the RV-Fabric alone reaches zero.

Table 6. Two-squad hierarchical composition. Each squad’s L2 emits only a partial
profile; only the L3 composition of both partials is the prohibited profile. Under a
dropped in-squad witness, squad completeness propagates to the L3 verdict.

 Scenario                                          L2[Sq1]                   L2[Sq2]           L3 verdict
 fault-free (fabric)                               {coords,imagery,comms},   {access}, sound   violation
                                                   sound
 drop imagery                                      {coords,comms},           {access}, sound   unknown
 (fabric)                                          incomplete
 drop imagery                                      {coords,comms}, sound     {access}, sound   no_violation†
 (central)
         †
             silent false all-clear: the best-effort L3 cannot see the in-squad loss.


7.3   Robustness, Attribution, and Sensitivity
The split is produced by a real LLM planner. The task-split attack is not merely
scripted: given the mission order and the injected intel note, a real LLM planner
emits the per-platform actions that compose the violation. A separate empirical
study drives this attack through seven planners and several delivery variants
(subtle, directive, per-platform distributed injection, benign-domain reframing,
and authorisation forgery), finding susceptibility to be model-dependent and
non-monotonic (weaker open models comply, the strongest hosted models refuse
the overt tasking yet comply once it is reframed or delivered one innocuous
fragment at a time), while the compositional monitor detects 100% of the splits
that are produced (by construction, once the witness events are observed). Here we
take the attack as given and focus on evidence-aware detection and composition
under fault.

Provenance, robustness, and causal attribution. Three further experiments
sharpen the picture. Provenance (RQ3): for every detected violation across the
four objectives, the reported platform set exactly matches the ground-truth
                             Mission-Level Runtime Assurance for ISR Swarms               17

Table 7. Threat-model sensitivity: split cardinality of the collective-exfiltration objective
(swarm total 1200 B, per-platform local limit 500 B, EMCON budget 900 B). The
adversary is squeezed: too few platforms trip the local limit, too many are caught by
the cross-agent sum.

     split N     B/platform       L1 (local)     L3 (EMCON)           caught by
         2            600          violation         violation        L1 (local)
         3            400            clean           violation        L3 (cross-agent)
         4            300            clean           violation        L3 (cross-agent)
         6            200            clean           violation        L3 (cross-agent)



contributing platforms: across the six detected violation instances for which a
ground-truth contributing set is defined, the reported provenance set matched
exactly in all six (6/6 = 100%), so a supervisor always learns which platforms
jointly breached the policy. Robustness: replaying the benign mission under
the same faults produces 0 false violations (only unknowns): evidence loss can
withhold a verdict but never fabricate one, so the verification-aware fabric adds
no false alarms. Causal attribution: ablating individual guarantees (Table 8)
shows each fabric signal prevents a distinct class of silent miss, removing the
event-id gap check (G1) reintroduces the silent miss under loss, and removing the
mission clock (G3) reintroduces it under jamming, so the zero-false-all-clear result
is causally attributable to the fabric, not to the scenario. Finally, the mission
monitor evaluates a 1000-platform swarm in 1.2 ms, so mission-level checking
is far below the second-scale mission-decision budget. Statistical stability: over
500 randomized task-split missions (random platform pool, random benign
background and timing) the fabric detects every planted violation and, under
a randomly dropped witness, silently clears a real violation in 0% of missions
versus 100% for the central monitor, the result is a property of the design, not of
a particular mission instance.

Threat-model sensitivity. Detection is not brittle to the adversary’s parameters.
Table 7 sweeps the split cardinality of the collective-exfiltration objective (swarm
total fixed, per-platform local limit 500 B, mission EMCON budget 900 B): a
small split pushes each platform’s emission over its local limit, so the per-platform
(L1) monitor catches it; a large split stays locally compliant, but the swarm-wide
sum trips the cross-agent (L3) EMCON property. No split cardinality evades
both tiers at once, so the adversary is squeezed between the per-platform limit
and the cross-agent threshold. Beyond loss and jamming, the fault matrix also
covers reordering, where the fabric’s trusted ingest order prevents the false alarm
a naive arrival-order monitor raises, and a slow consumer, where independent
cursors preserve full detection (zero false all-clears) at bounded latency.

Timing, skew, and benign-collaboration sensitivity. Three sweeps probe robustness
to timing parameters and to legitimate collaboration. Silence timeout: the mission-
clock silence rule trades jam-detection latency against false-silence flags; over
18       N. Kekatos et al.

Table 8. Guarantee ablation on the intel-package objective: silent false all-clears when
a single fabric signal is removed. G1’s event-id gap detects the dropped witness; G3’s
mission clock detects the jammed platform; each removal reintroduces exactly one class
of silent miss.

      Configuration             drop-witness (loss)      jam-platform (silence)
      full fabric                         0                          0
      −G1 (no gap detection)              1                          0
      −G3 (no mission clock)              0                          2



300 jittery missions with heavy-tailed comms stalls, a 2 s timeout raises ≈ 2.9
false-silence flags per mission, a 5 s timeout ≈ 0.5 (jam detected in ≈ 4 s), and
10 s zero (but ≈ 9 s latency): 5 s is the knee. Clock skew: applying a per-platform
clock offset to the order-dependent monitors, the verdict is preserved below
the order window and downgrades to unknown beyond it (authorisation-order
at skew ≥10 s for a 5 s window; targeting-chain once the observed step order
inverts) rather than emitting a false verdict, while the order-insensitive occupancy
count is unaffected at every skew; this motivated extending the chain monitor
with an explicit order-violation→unknown trigger. Benign collaboration: across
seven legitimate scenarios that superficially resemble the attacks (authorised
full-profile collection, the same fragments on an unprotected target, aborted
(three-of-four) collection, authorised emergency entry, an authorised targeting
workflow, sub-k occupancy, and within-budget emissions), the monitors raise
0 false alarms, confirming the composition is correctly conditioned on target,
authorisation, completion, and count (and prompting the same authorisation
conjunct to be added to the targeting-workflow property).


7.4    Systems, Formal-Engine, and Advanced-Fault Validation
Systems validation on the reused RV-Fabric. We validate the L2 transport guar-
antees by executing them live on the evaluation host against the reused RV-Fabric
implementation: real Mosquitto + NATS JetStream with the gateway durable
outbox recast as the L2 coordinator. These runs exercise the fabric and the L3 mis-
sion monitor; integrating the ROS 2/DDS front hop into a single end-to-end path
is future work. End-to-end latency over the gen→MQTT→L2→JetStream→L3
path (n=1000 live mission events) has a fault-free median of 3.7 ms and, under
a degraded link (10% drop with durable retransmit), a 42 ms median with no
accepted event lost (1000/1000 delivered), comfortably within the second-scale
mission-decision budget. Coordinator crash/recovery: once the outbox entry is
persisted, 0 accepted verdicts are lost and the after-publish replay yields 0 dupli-
cate incidents after event-id de-duplication. Overload/retention: discard=old
silently drops the oldest verdicts under sustained overload, whereas discard=new
surfaces overflow as an explicit health alert before continuity is lost. Consumer
isolation: independent durable cursors let a fast L3 consumer drain its backlog
while a slow peer lags, so one lagging monitor cannot stall the mission verdict.
                           Mission-Level Runtime Assurance for ISR Swarms           19

These confirm the guarantees hold on the real fabric, not only in the in-process
emulation used for the controlled campaign.

Real formal engine. The cross-agent primitive is not only decided by our reference
monitor: we export the coordinated-collection property, ≥ 3 distinct platforms
collect on the protected site within 30 s, the swarm analogue of the edge-IoT
cross-gateway property, to the real MonPoly first-order past-time engine and
evaluate it on the attack trace. MonPoly reports the property satisfied at the
third and fourth contributing platform (two satisfaction points), confirming that
the distributed violation is detectable by a genuine formal engine carried over
the fabric, not merely by a bespoke checker.

Adaptive adversary, integrity faults, and detection latency. Four experiments
probe dimensions beyond loss and jamming. Adaptive (low-and-slow) adversary: a
patient adversary spreads the four package parts by an inter-part gap S, giving a
collection span 3S; a windowed monitor detects the package iff its window W ≥ 3S.
Because the RV-Fabric aggregates over the whole mission window, evasion
requires spreading collection across missions, a documented limit (Sect. 7.6), at
a buffer-state cost proportional to W . Detection latency: under online, streaming
evaluation the fault-free verdict fires at the first event that completes the package,
with no additional logical waiting interval beyond witness completion (the per-
event processing cost is microseconds, reported separately); under a dropped
witness the RV-Fabric raises a finite-latency unknown the instant the event-id
gap becomes observable, whereas the central monitor’s latency is unbounded :
it never signals (the silent miss made quantitative). Byzantine (lying) platform
(exploratory extension beyond the core threat model of Sect. 3): when each platform
under-reports its own emissions (self-reported swarm total 800 B, below the 900 B
budget), a self-report-only monitor is fooled; an independent RF-sentry witness
observes the true 1200 B and the corroboration property fires, with integrity
provenance naming the under-reporting platforms. Jamming the sentry yields
unknown, not a silent clear: an integrity fault is thus handled like a loss fault
provided an independent corroborating witness exists, which is the assumption
this extension adds. Recovery: a withheld unknown resolves to violation once a
dark contributor returns, so the downgrade is provisional and sound; the central
monitor’s blackout all-clear, by contrast, has already been delivered.

No silent all-clears, and graceful degradation. We collapse the entire fault cam-
paign into a single No-Silent-Clear Rate,
                                       silent false all-clears
                        NSCR = 1 −             ⋆               ,
                                             |Icampaign |

the fraction of oracle incidents that are not silently cleared, i.e. reported as
violation or honestly downgraded to unknown (Table 9). We prefer this to a
“verdict-preservation” count because an honest unknown does not preserve the
original violation; it merely refuses to clear it, which is exactly the safety property
20      N. Kekatos et al.

Table 9. No-Silent-Clear Rate (fraction of oracle incidents not silently cleared, i.e.
reported as a violation or honestly downgraded to unknown) over the full fault campaign,
and silent false all-clears when eight squads are faulted simultaneously. The RV-Fabric
never silently clears, at any fault count.

            Configuration                   NSCR       Silent all-clears
                                                      (8 squads faulted)
            per-platform guardrails           0%               n/a
            central (best-effort)            50%                8
            RV-Fabric (evidence-aware)       100%               0



we claim. The RV-Fabric scores 100%, the central monitor 50%, and per-platform
guardrails 0%; the strict violation-vs-unknown split is the “+u” breakdown already
shown in Table 4. A compound-fault sweep confirms the guarantee is not fragile
to fault count: as up to eight squads are simultaneously faulted, the RV-Fabric’s
silent-clear count stays 0 and its unknown count rises monotonically (graceful
degradation), while the central monitor’s silent misses climb to 8.

Is the property a tuned knob? (ROC). To check that the collective-budget property
is well-posed rather than a hand-fitted threshold, we generate 400 missions whose
true swarm-emission total is drawn uniformly over [500, 1300] B (a mission is a
positive iff its true total exceeds the 900 B reference budget), split the total across
four platforms, and add independent Gaussian measurement noise (σ = 60 B)
per platform. Sweeping the decision threshold and scoring each mission by its
summed measured emissions gives area-under-ROC 0.96 (near-perfect separation,
so detection is not a tuned artefact); scoring instead by any single platform’s
measurement gives 0.50 (chance), because a per-platform view structurally cannot
observe a swarm-wide sum. The otherwise-deterministic property admits an ROC
at all only because the injected measurement noise, not the logic, makes the
thresholded sum a non-trivial classifier. We stress that ROC/AUC is not the
headline instrument: a strict detection ROC treats an honest unknown and a silent
miss identically (both are non-detections), so it cannot credit the evidence-aware
behaviour that is the whole point, which is exactly why NSCR, not AUC, is
the metric of record. Finally, when all six properties fire on a single mission
trace, provenance disentangles which platforms triggered which property, and
the command node that issued the authorisation appears in no violation (no
collateral blame).

Per-mechanism walkthrough. The three faults isolate distinct failure modes.
Under drop imagery witness (a delivery loss, G1), the collective-package property
loses one of its four witnesses and cannot fire. The central monitor, lacking any
completeness signal, reports no_violation on the package, a silent false all-clear
indistinguishable from a genuinely benign mission, while still detecting the two
unaffected incidents (2/3, one silent miss). The evidence-aware fabric instead
observes an event-id gap on uav_2’s stream and downgrades the package verdict
                                    Mission-Level Runtime Assurance for ISR Swarms   21


                           1




              eval (ms)
                          0.5


                           0
                                0     200      400     600     800    1,000
                                                 platforms

Fig. 7. Mission-monitor evaluation time vs swarm size (real measurements). Cross-
agent checking scales roughly linearly and stays sub-2 ms to 1000 platforms, orders of
magnitude below the second-scale mission-decision budget.


to (unknown, incomplete): a flagged 2/3 +1u with zero silent misses. Under jam
uav_3 (a denial, G3), both the package (missing comms) and the emissions budget
(missing uav_3’s transmissions, so the swarm total falls below Bmission ) appear
satisfied to the central monitor, two silent false all-clears (1/3), whereas the
mission clock surfaces uav_3 as a missing stream and both verdicts become
unknown/unavailable (1/3 +2u, zero silent misses). Across the campaign the
central monitor accrues three silent false all-clears and the fabric zero: the fabric
never trades a no_violation for missing evidence.


7.5   Cost, Summary, and Assurance Workflow
RQ4, cost. The monitors are past-time and stream-based and add per-event
overhead comparable to the single-agent case (microseconds/event); the mission-
level cost is dominated by the second-scale mission dynamics, and the fabric’s
delivery/recovery costs are those measured for the underlying transport (crash
recovery linear in the un-acked backlog; 0% loss to 1000 producers). Fig. 7
plots the measured mission-monitor evaluation time against swarm size: cross-
agent checking scales roughly linearly and stays under 2 ms to 1000 platforms.
Beyond monitor evaluation, end-to-end verdict latency across the full fabric
path (tverdict − tevent : event → MQTT → squad sidecar → JetStream → L3)
is measured live on the real Mosquitto + NATS JetStream stack, a fault-free
median of 3.7 ms and a degraded-link median of 42 ms with no accepted event
lost (reported in full under Systems validation on the reused RV-Fabric above),
well within a second-scale mission-decision budget.

Summary. The central result is precisely the mission-assurance claim: every per-
platform monitor reports compliance, yet the compositional monitor detects the
mission-level violation and names the platforms that jointly produced it; and under
contested communications the verification-aware fabric withholds the all-clear
rather than silently missing the attack.
22      N. Kekatos et al.

Mission-assurance workflow. The verdicts are an audit trail, not a terminal
pass/fail. Provenance lets a supervisor, on a violation, see which platforms jointly
breached the policy, and on an unknown/incomplete verdict know that a decision
is withheld for want of evidence rather than granted by default, a distinction
that is operationally decisive under jamming: “we cannot currently certify Sector
B” lets a commander hold or re-task, whereas a silent all-clear invites exactly
the adversary’s intended action. Since the monitors are decoupled from the flight
controllers (Sect. 3), the assurance layer drops onto an existing autonomy stack
without touching safety-critical control.


7.6   Threats to Validity
The quantitative results are controlled invariant-preservation experiments (a
deterministic kinematic mission with a known ground-truth oracle, designed to
isolate whether each design element preserves the mission verdict under fault)
and not a population-level measurement of operational detection accuracy; the
clean 0/100% figures should be read in that light. Of the realism layer, the
ROS 2/DDS middleware integration and the ArduPilot SITL flight-dynamics
path are both executed (Sect. 6, Fig. 4); only Gazebo visual rendering (a GPU
concern, cosmetic) and a larger physical, at-scale sweep remain future work. The
semantic-extraction path is deliberately secondary; text-only violations depend
on classifier quality. Core-model platform integrity beyond going silent is out of
scope (with the single exploratory RF-corroboration extension of Sect. 7), as is a
full formal soundness proof of the composition algebra (adapted from the prior
edge-IoT fabric).


8     Related Work

Agent safety and multi-step attacks. Single-agent guardrails and policy monitors
check one agent’s actions against rules, but sequential tool-attack chains and
prompt-injection benchmarks show that a large fraction of multi-step attacks
defeat per-event checks [27,14,38]; and in multi-agent settings an injection can
even propagate agent-to-agent [25]. Our single-agent RV of LLM actions composes
spatial, temporal, and semantic monitors for one agent and establishes that
composition is necessary rather than convenient; the present work lifts that
composition to the swarm, where the violation is distributed across platforms
and no single-agent view, however well composed, suffices.

Distributed and spatial RV. Reaching a verdict across faulty, asynchronous
monitors is studied at the algorithm level [19,9], and spatial and spatio-temporal
logics monitor properties over networks of components [3]. That line makes the
monitoring logic fault- or reordering-tolerant while abstracting the transport.
We are complementary and beneath it: the verification-aware fabric makes the
delivery layer’s loss, ordering, and liveness first-class and observable, so the stream
the swarm monitor consumes, and reasons about with any of those algorithms,
                           Mission-Level Runtime Assurance for ISR Swarms            23

is the stream their correctness assumes. This is what a swarm monitor needs
under contested communications, and it is what lets us report an honest unknown
instead of a silent all-clear. Our own two-level hierarchical monitoring line (edge
device to gateway to backend, with TeSSLa- and MonPoly-based first-order
correlation) established these tiers for edge-IoT security monitoring and cyber-
physical resilience [23,22,24,34]; the present paper carries that hierarchy to a
cooperative LLM-assisted swarm.

Runtime assurance for robotics. Runtime-assurance architectures switch to a
verified safety controller when a monitor flags danger, from the Simplex architec-
ture [32] to robotics frameworks such as SOTER [15]; and ROS-level monitors
such as ROSMonitoring [18] attach runtime verification to a robot’s message bus;
feedback controllers can themselves be synthesised to satisfy temporal-logic spec-
ifications [13]. These secure a single platform’s control and safety envelope. Our
concern is orthogonal and one level up: a mission-level, cross-agent obligation that
no single platform’s monitor can express, checked over an evidence-aware trans-
port so that contested or intermittent communication yields an explicit unknown
rather than a silent all-clear. The single-platform assurance approaches reviewed
here do not explicitly address compositional multi-robot mission obligations over
an adversarial, lossy evidence channel.

M&S of autonomous systems. Modelling and simulation is the established setting
for evaluating autonomous-system assurance under repeatable, injected condi-
tions [29]. Digital-twin and FMI co-simulation approaches assure autonomous
systems by running analyses against a high-fidelity model [37,36,1], within a
broader continuous-engineering methodology for trustworthy learning-enabled au-
tonomous systems [8], and design-time formal analysis can check learning-enabled
components directly [16]; these are complementary to this work and the subject
of a companion paper. Our contribution is orthogonal: a simulation-evaluated,
compositional, evidence-aware monitor for the swarm’s mission-level obligations,
whose verdicts are auditable mission-assurance evidence rather than a pass/fail
flag.


9    Conclusion
We presented a three-tier, evidence-aware compositional runtime-verification
framework for LLM-assisted autonomous robot swarms on ISR missions in
contested environments. A distributed prompt-injection attack that is compliant
at every platform is invisible to per-platform monitors yet detected, with platform-
level provenance, by the compositional monitor; and under loss and jamming the
verification-aware fabric emits zero silent false all-clears where a best-effort central
monitor emits several. The framework lifts hierarchical agent-safety monitoring
from the single agent to the swarm and turns transport-level guarantees into
auditable, platform-attributed mission-assurance evidence. Future work adds
Gazebo visual rendering and a larger physical, at-scale sweep over the executed
24      N. Kekatos et al.

ROS 2/ArduPilot layer, and a formal soundness argument for the composition
algebra.


References
 1. Abdelsalam, M., Bensalem, S., Delacourt, A., He, W., Katsaros, P., Kekatos, N.,
    Ruiz Nolasco, R., Peled, D., Ponchant, M., Ryad, I., Temperekidis, A., Wu, C.:
    Digital twin for the formal analysis of a depth of anesthesia controller. SIMULATION
    101(3), 341–360 (2025)
 2. Ahn, M., Brohan, A., Brown, N., et al.: Do as i can, not as i say: Grounding
    language in robotic affordances. In: Conf. on Robot Learning (CoRL) (2022)
 3. Bartocci, E., Bortolussi, L., Loreti, M., Nenzi, L.: Monitoring mobile and spatially
    distributed cyber-physical systems (STREL). In: MEMOCODE. pp. 146–155 (2017)
 4. Bartocci, E., Falcone, Y., Francalanza, A., Reger, G.: Introduction to runtime
    verification. Lectures on Runtime Verification, LNCS 10457 (2018)
 5. Basin, D., Klaedtke, F., Müller, S., Zălinescu, E.: Monitoring metric first-order
    temporal properties. Journal of the ACM 62(2) (2015)
 6. Basin, D., Klaedtke, F., Zalinescu, E.: The MonPoly monitoring tool. In: RV-CuBES
    (2017)
 7. Bauer, A., Leucker, M., Schallhart, C.: Runtime verification for LTL and TLTL.
    ACM Transactions on Software Engineering and Methodology (TOSEM) 20(4)
    (2011)
 8. Bensalem, S., Katsaros, P., Kekatos, N., et al.: Continuous engineering for trust-
    worthy learning-enabled autonomous systems. In: Bridging the Gap Between AI
    and Reality (AISoLA 2023). LNCS, vol. 14380. Springer (2023)
 9. Bonakdarpour, B., Fraigniaud, P., Rajsbaum, S., Rosenblueth, D.A., Travers, C.:
    Decentralized asynchronous crash-resilient runtime verification. In: CONCUR (2016)
10. Brambilla, M., Ferrante, E., Birattari, M., Dorigo, M.: Swarm robotics: A review
    from the swarm engineering perspective. Swarm Intelligence 7(1), 1–41 (2013)
11. Chung, S.J., Paranjape, A.A., Dames, P., Shen, S., Kumar, V.: A survey on aerial
    swarm robotics. IEEE Transactions on Robotics 34(4), 837–855 (2018)
12. Convent, L., Hungerecker, S., Leucker, M., Scheffel, T., Schmitz, M., Thoma, D.:
    TeSSLa: Temporal stream-based specification language. In: SBMF (2018)
13. Dang, T., Donzé, A., Haque, I., Kekatos, N., Saha, I.: Counter-example guided
    imitation learning of feedback controllers from temporal logic specifications. In:
    IEEE Conference on Decision and Control (CDC) (2023)
14. Debenedetti, E., et al.: AgentDojo: A dynamic environment to evaluate prompt
    injection attacks and defenses for llm agents. In: NeurIPS Datasets and Benchmarks
    (2024)
15. Desai, A., Ghosh, S., Seshia, S.A., Shankar, N., Tiwari, A.: SOTER: A runtime
    assurance framework for programming safe robotics systems. In: 49th IEEE/IFIP
    Int. Conf. on Dependable Systems and Networks (DSN). pp. 138–150 (2019)
16. Eleftheriadis, C., Kekatos, N., Katsaros, P., Tripakis, S.: On neural network equiv-
    alence checking using SMT solvers. In: Formal Modeling and Analysis of Timed
    Systems (FORMATS). pp. 237–257. LNCS (2022)
17. Faymonville, P., Finkbeiner, B., Schledjewski, M., Schwenger, M., Stenger, M.,
    Tentrup, L., Torfah, H.: StreamLAB: Stream-based monitoring of cyber-physical
    systems. In: Computer Aided Verification (CAV) (2019)
                            Mission-Level Runtime Assurance for ISR Swarms             25

18. Ferrando, A., Cardoso, R.C., Fisher, M., Ancona, D., Franceschini, L., Mascardi,
    V.: ROSMonitoring: A runtime verification framework for ROS. In: Towards Au-
    tonomous Robotic Systems (TAROS). LNCS, vol. 12228, pp. 387–399. Springer
    (2020)
19. Fraigniaud, P., Rajsbaum, S., Travers, C.: On the number of opinions needed for
    fault-tolerant run-time monitoring in distributed systems. In: Runtime Verification
    (RV) (2014)
20. Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., Fritz, M.: Not what
    you’ve signed up for: Compromising real-world LLM-integrated applications with
    indirect prompt injection. In: ACM Workshop on Artificial Intelligence and Security
    (AISec) (2023)
21. Havelund, K., Peled, D., Ulus, D.: First-order temporal logic monitoring with BDDs.
    In: Formal Methods in Computer-Aided Design (FMCAD) (2017)
22. Kekatos, N., Chintri, M., Katsaros, P., Nianios, T., Seitoglou, I., Basagiannis, S.:
    Hierarchical security monitoring for edge-iot: A formal methods approach. In: IEEE
    International Conference on Cyber Security and Resilience (CSR) (2026), to appear
23. Kekatos, N., Chintri, M., Katsaros, P., Lekidis, A., Nianios, T., Seitoglou, I.,
    Temperekidis, A., Basagiannis, S.: A hierarchical runtime-verification approach for
    security monitoring of edge-iot. In: Int. Workshop on Advances in Practical Security
    (ARES) (2026), to appear
24. Kekatos, N., Koutidis, G., Antonakopoulos, K., Basagiannis, S., Katsikas, S., Kaval-
    lieratos, G., Lekidis, A., Nianios, T., Papageorgiou, E.: RESILAGENT: A three-pillar
    architecture for cyber-physical resilience in electrical power and energy systems. In:
    ARES 2026 Workshops (EPES-SPR) (2026), to appear
25. Lee, D., Tiwari, M.: Prompt infection: LLM-to-LLM prompt injection within
    multi-agent systems (2024), arXiv:2410.07283
26. Leucker, M., Schallhart, C.: A brief account of runtime verification. Journal of Logic
    and Algebraic Programming 78(5), 293–303 (2009)
27. Li, J.J., He, J., Shang, C., Kulshreshtha, D., Xian, X., Zhang, Y., Su, H., Swamy,
    S., Qi, Y.: STAC: When innocent tools form dangerous chains to jailbreak LLM
    agents (2025), arXiv:2509.25624
28. Liu, Y., Jia, Y., Geng, R., Jia, J., Gong, N.Z.: Formalizing and benchmarking
    prompt injection attacks and defenses. In: USENIX Security Symposium (2024)
29. Mazal, J., Fagiolini, A., et al. (eds.): Modelling and Simulation for Autonomous
    Systems (MESAS 2024), Revised Selected Papers, LNCS, vol. 15761. Springer
    (2025)
30. OASIS: MQTT version 5.0. OASIS Standard (2019)
31. Perez, F., Ribeiro, I.: Ignore previous prompt: Attack techniques for language
    models. In: NeurIPS ML Safety Workshop (2022)
32. Sha, L.: Using simplicity to control complexity. IEEE Software 18(4), 20–28 (2001)
33. Shi, W., Cao, J., Zhang, Q., Li, Y., Xu, L.: Edge computing: Vision and challenges.
    IEEE Internet of Things Journal 3(5) (2016)
34. Sinha, P., Kekatos, N., Basagiannis, S., Bruto da Costa, A.A., Lekidis, A., Mitra,
    P., Nianios, T., Papageorgiou, E.: Explainable rule mining of IPv6 extension-
    header presence patterns from paired-vantage captures. In: ARES 2026 Workshops
    (GenXSec) (2026), to appear
35. Synadia / CNCF: NATS and JetStream. https://nats.io (2024)
36. Temperekidis, A., Kekatos, N., Katsaros, P.: Runtime verification for FMI-based
    co-simulation. Runtime Verification (RV), LNCS 13498 (2022)
26      N. Kekatos et al.

37. Temperekidis, A., Kekatos, N., Katsaros, P., et al.: Towards a digital twin architec-
    ture with formal analysis capabilities for learning-enabled autonomous systems. In:
    MESAS. LNCS, vol. 13866 (2022)
38. Zhan, Q., Liang, Z., Ying, Z., Kang, D.: InjecAgent: Benchmarking indirect prompt
    injections in tool-integrated large language model agents. In: Findings of the
    Association for Computational Linguistics (ACL) (2024)


A     Reproducibility

The reproducible core (kinematic mission, monitors, verification-aware
fabric, fault campaign) and the ROS 2 adapter are provided as an arti-
fact. Every deterministic quantitative result reproduces on a fresh Ubuntu
virtual machine with docker build -t swarm-rv . then a single docker
run, no ROS 2 or GPU required: run_demo.py (Table 4); experiments.py
(Table 5, Fig. 6, scale sweep); experiments_extra.py (provenance, ablation
Table 8, 1000-platform Fig. 7, and the 500 randomized missions at seed 7);
experiments_advanced.py (NSCR Table 9, compound-fault sweep, and
the 400-mission ROC at seed 11); experiments_hierarchy.py (two-squad
L1→L2→L3, Table 6); experiments_properties.py (the additional property
kinds); threat_sweep.py (Table 7); and the parameter/robustness sweeps
exp_timeout.py, exp_skew.py, and exp_benign.py. We distinguish two classes
of result. The deterministic RV experiments above are fully reproducible (fixed
seeds, no wall-clock or network dependence). The LLM-in-the-loop attack
campaign (the seven planners, injection variants, and attack-success rate (ASR))
is reported separately. The systems validation was executed live against the
reused RV-Fabric stack (real Mosquitto + NATS JetStream): end-to-end latency
via e2e_latency.py –real (n=1000), and coordinator crash/recovery, overload-
/retention, and consumer isolation via run_crash_exp.sh, exp_retention.py,
and exp_isolation.py from the companion artifact against the live broker.
The ROS 2 result of Sect. 6 runs via ros2_realism/run_ros2_demo.sh
in a ros:humble container; the ArduPilot SITL mission (Fig. 4) runs via
sitl_mission/run_sitl_mission.sh on an x86 host; and the cross-agent
property is confirmed by the real MonPoly engine via swarm_to_monpoly.py.
All deterministic RV, transport, and simulation experiments use fixed seeds and
were reproduced on an independent Ubuntu VM; the LLM outputs are archived
together with prompt hashes, model identifiers, request parameters, and raw
responses, but because hosted models may change, exact regeneration of those
outputs is not guaranteed: they are preserved, not necessarily reproducible.
