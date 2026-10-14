                                          Synthesizing Voltage Ride-Through Controllers for Data Centers
                                                                     Wayne Wang                    Archit Bhatnagar                       Tongyuan Miao            Saniya Kalamkar
                                                                                                    Wenqi Cui†                 Inigo Incer          Ang Chen
                                                                                                  University of Michigan                   † New York University


                                          Abstract                                                                                         ERCOT (US) and Energinet (Europe). VRT requires the data center
                                          Data centers are among the power grid’s fastest-growing loads.                                   to remain connected and follow specified response criteria if the
                                          Since data center servers are sensitive electronic components, they                              grid voltage sags or swells during a transient fault.
                                          need to be protected against the grid’s voltage disturbances during                                 While VRT has been well studied for power devices and gener-
                                          grid faults. While this can be achieved by simply disconnecting from                             ators, data centers present a new range of challenges. First, DCs
                                          the grid upon disturbances, disconnection can further destabilize                                represent a large load, whereas VRT standards were originally de-
                                          the power system if many data centers trip at once. To address                                   signed for generators. Further, DCs comprise a system of devices,
                                          this emerging concern, voltage ride-through (VRT) grid codes have                                each with its own protective response mechanisms invisible to the
                                          been proposed to standardize data center behavior. They require                                  grid, requiring system-level joint control. The growth of AI work-
                                          a data center to stay connected for a period of time through the                                 loads compounds these challenges: a single data center campus
                                          disturbance, hold an active power floor, and recover its draw within                             now draws hundreds of megawatts, its training workload swings
arXiv:2608.07289v1 [eess.SY] 7 Aug 2026




                                          a deadline upon restoration. However, systematically designing                                   within seconds, and the hardware at risk (e.g., GPU clusters) is
                                          and certifying controllers that satisfy these coupled temporal and                               costly enough that individual protections are tuned to trip early.
                                          operational requirements remains challenging.                                                       Today, a data center’s response to a voltage event heavily de-
                                             We propose SolVRT, a system that synthesizes a grid-code-                                     pends on individual device protection settings, power electronics
                                          compliant VRT controller for a given data center using formal                                    vendor behavior, and controller heuristics. Under this uncertainty,
                                          methods. We develop a specification language that expresses a grid                               DC operators default to early disconnection to protect their in-
                                          code in Signal Temporal Logic (STL) as the basis for formal rea-                                 ternal operation. A hand-tuned controller might help the DC ride
                                          soning. Our encoding algorithm takes the specification, along with                               through, but provides no compliance guarantee since grid codes
                                          a model of the data center’s power topology, and translates the                                  impose several timed requirements that the data center must satisfy
                                          constraints into a controller synthesis problem. This step produces                              simultaneously. A principled design for the data center to control
                                          a correct-by-construction controller if a solution can be found, or                              internal devices and ride through voltage events with guaranteed
                                          a proof that no such controller exists. For the latter case, SolVRT                              grid code compliance is still missing. This difficulty is compounded
                                          provides a diagnostic step: it traces the facility’s “conflict frontier,”                        by the fact that the grid codes exist as natural language documents
                                          isolates the conflicting clauses that led to non-compliance, and com-                            describing numeric constraints, which are hard to analyze formally
                                          putes the smallest hardware or workload change that would enable                                 in a machine-checkable manner. This interface between grid re-
                                          compliance. We evaluate SolVRT through closed-loop simulations                                   quirements and data center capabilities is described in informal
                                          of a 200 MW data center connected to a 140-bus transmission sys-                                 text, making it difficult for grid operators to anticipate data center
                                          tem. The results demonstrate that SolVRT can synthesize compliant                                behavior, for data centers to guarantee compliance, or to reason
                                          VRT controllers, certify infeasibility when compliance is unattain-                              about the hardware or workload provisioning that would achieve
                                          able, and identify targeted modifications that enable compliance.                                compliance under all conditions.
                                                                                                                                              In this paper, we take a fresh look at VRT from the perspective
                                          1     Introduction                                                                               of formal methods. If we can formalize grid codes in a machine-
                                                                                                                                           checkable language, a range of synthesis and verification methods
                                          Data centers (DCs) are large electric loads with fluctuating demands
                                                                                                                                           becomes available to attack this problem. We argue for treating
                                          and high sensitivity to power quality; their response to grid voltage
                                                                                                                                           VRT requirements as a formal assume-guarantee specification, a
                                          disturbances has been a rising concern. For instance, if the grid ex-
                                                                                                                                           method widely used in safety-critical domains such as aerospace
                                          periences voltage sags upon contingencies and faults, data centers
                                                                                                                                           engineering [21, 35]. With the assume-guarantee interface, the grid
                                          may simply disconnect from the grid in order to protect internal
                                                                                                                                           states assumptions on the voltage disturbance, and the data center
                                          devices (e.g., by switching to local power sources such as UPSes and
                                                                                                                                           must uphold guarantees on its response over explicit signals when-
                                          diesel generators). From the grid’s perspective, however, simulta-
                                                                                                                                           ever those assumptions hold. Both assumptions and guarantees are
                                          neous disconnection of large loads introduces further disturbances
                                                                                                                                           timed constraints on real-valued signals, and Signal Temporal Logic
                                          during an already-stressed event. In a 2024 incident in Virginia,
                                                                                                                                           (STL) expresses exactly such predicates over signal trajectories [29].
                                          a single transmission-line fault caused voltage sags that tripped
                                                                                                                                           Compliance can be established by solving whether a controller
                                          roughly 1,500 MW of data center load at once, most of which stayed
                                                                                                                                           exists that enables the data center to satisfy the guarantee under
                                          offline for hours [31].1 This has prompted the development of volt-
                                                                                                                                           the assumption while respecting all constraints.
                                          age ride-through (VRT) requirements from grid operators, such as
                                                                                                                                              Following this intuition, we propose a grid-code-aware system
                                          1 A larger event of the same type occurred in Virginia on July 22, 2026, with a reported         SolVRT that solves the VRT compliance problem for data centers
                                          total load loss roughly 3 GW. Detailed analysis of this incident was not available at the        using formal methods by synthesizing a code-compliant controller
                                          time of writing.
                                                                                                                                      1
                                                                                                                                           Wang et al.


for a given data center. When this synthesis is infeasible, SolVRT
diagnoses the unsatisfiable clauses and provides change recom-
mendations. We make three contributions. First, we develop a new
domain-specific language (DSL) for expressing data center VRT grid
codes. The specification makes voltage event assumptions, response
requirements, timers, active-power floor, and internal protection
limits explicit and machine-checkable—using STL predicates to
capture the core requirements. Next, our algorithm encodes the
specification into a controller synthesis problem with other con-
straints, including disturbance traces, plant models, and hardware
constraints. When the synthesis query is feasible, SolVRT outputs
a model predictive controller (MPC) as witness. If synthesis is infea-       Figure 1: Low-voltage ride-through envelopes of the two
sible, the diagnosis and provisioning step takes over. We diagnose           codes: ERCOT NOGRR282’s band envelope (May 2026) and
the violating clauses and provide provisioning recommendations by            Energinet TR 3.4.3’s voltage–time curve.
modeling infeasibility as the conflict frontier. This allows SolVRT to
identify the unsatisfiable core of the conflict and compute the mini-
mal changes needed on hardware capability or workload flexibility            a floor during the sag, and restore its draw within a deadline af-
to restore compliance for a given data center and specification.             ter the sag clears. Codes differ only in the values that each part
   With a comprehensive simulation using a 200MW data center                 takes. For example, Energinet’s VRT code [15]—the Danish code
and a 140-bus transmission system, we are the first to formalize             for transmission-connected demand facilities—places requirements
VRT requirements for data centers as a controller synthesis problem          on the same structure of three obligations as the ERCOT code, and
and demonstrate its practicality. We hope this paper will inspire            the two codes only differ in the requirement values. Regarding how
future work that studies DC/grid coordination through the lens of            long the facility must stay connected during voltage sags or swells,
formal analysis to increase the resilience of cross-infrastructure           ERCOT specifies voltage ranges with corresponding ride-through
interactions. We will release SolVRT in open source.                         durations; in contrast, Energinet requires a piecewise-constant
                                                                             voltage–time curve. Regarding active power that the facility must
2 Background and Related Work                                                keep drawing during the fault, ERCOT requires a level proportional
                                                                             to the sag for certain voltage ranges, while Energinet permits a floor
2.1 What are VRT and LVRT                                                    of zero for all depths. Regarding recovery of active power draw
Voltage ride-through (VRT) has traditionally been defined as a               after the fault, ERCOT sets a single target of 90% of the pre-fault
generator-side requirement [20, 37]. Its central objective is to en-         draw within two seconds, whereas Energinet stages three targets
sure that generators, including synchronous machines and inverter-           over 30 seconds (80/90/95% at 5/20/30 s) and caps the overshoot.
based resources such as solar photovoltaic and wind generation, re-              VRT grid codes may require data centers to ride through both
main connected during short-duration voltage disturbances caused             voltage sags and swells, but sags are the more challenging case.
by grid-side faults. By preventing premature disconnection, VRT              Upon sags, low-voltage ride-through (LVRT) involves all three
requirements help avoid cascading loss of generation and support             requirements (connection, minimum power draw, recovery); but
system stability during and after fault events.                              high-voltage ride-through (HVRT), in the example of ERCOT, im-
   Comparable ride-through requirements have not been imposed                poses a connection requirement and an unchanged active power
on loads, which were typically smaller, more dispersed, and had a            draw, making it an easier subset of the LVRT problem.
less explicitly regulated dynamic voltage response. However, the                 Hence, we focus on LVRT in this paper, although SolVRT’s gram-
rapid growth of large electronic loads, particularly DCs, is changing        mar can encode voltage swell and related power draw requirements
this assumption. Since a single DC today can represent a substantial         as well and the synthesis query stays the same. Unlike conven-
amount of load, its disconnection during a voltage disturbance can           tional LVRT requirements that are often specified for an individual
create an abrupt loss of demand and potentially worsen grid dynam-           generator or power-electronic device, data-center LVRT must be
ics. As a result, large-load ride-through capability is emerging as          understood as a system-level property. A data center consists of
an important reliability requirement. For example, ERCOT [16] is             multiple interacting components, including UPS systems, battery
developing large computational/electronic load ride-through rules            energy storage, switchgear, power-electronics interfaces, internal
through NOGRR282/NPRR1308, motivated by observed DC and                      distribution networks, and workload-dependent power consump-
cryptomining load trips during normal voltage disturbances. When             tion. In practice, during a voltage sag, tripping is initiated not by the
data centers are clustered in a region, the grid-side impact is aggra-       computing equipment itself but by facility protection tuned to pro-
vated. In the 2024 Virginia incident [31], a single localized trans-         tect it. In the 2024 Virginia event, UPS control schemes that count
mission fault propagated to data-center facilities across the region         voltage disturbances tripped the facility after repeated sags [31].
as a voltage sag, triggering their independent protection at once            LVRT analysis and certification for data centers is therefore fun-
and amplifying the fault into a total load loss of roughly 1,500 MW.         damentally different from conventional device-level verification:
   These emerging codes share a three-part structure: the DC must            it requires certifying that the aggregated data-center system satis-
stay connected while the voltage disturbance lies within a ride-             fies grid-side ride-through requirements while respecting internal
through envelope (Figure 1), keep its active power draw above                device constraints.
                                                                         2
Synthesizing Voltage Ride-Through Controllers for Data Centers


2.2     Data Center Electrical and Compute Models                              In particular, temporal logics support the expression of state-
From an electrical perspective, prior work models DC power deliv-           ments over signals that change over time. Within the class of tem-
ery using UPS systems, BESS, switchgear, power-electronics con-             poral logics, Linear Temporal Logic (LTL) and Metric Temporal
verters, and internal distribution topology [42]. These components          Logic (MTL) operate over boolean propositions, while LVRT grid
make the load behavior different from a passive constant-power              codes constrain real-valued signals against numeric thresholds un-
load through a combination of protection settings, converter limits,        der deadlines. Signal Temporal Logic (STL) specifies requirements
and reactive-power capability, which affects the data center’s capa-        over exactly such real-valued signals in continuous time [29]. Its
bility to comply with LVRT grid codes during a voltage disturbance.         atomic predicate is any Boolean-valued statement 𝜇 over the signals
We adopt LinDistFlow [5, 46], a standard linearized power-flow              𝑥 being considered. Its formulas combine predicates with Boolean
approximation for radial distribution networks, to model the in-            operators and time-bounded temporal operators,
ternal network of the DC. Specifically, the DC network extends
                                                                             𝜑 ::= 𝜇 (𝑥) | ¬𝜑 | 𝜑 ∧𝜓 | 𝜑 ∨𝜓 | □ [𝑎,𝑏 ] 𝜓 | ^ [𝑎,𝑏 ] 𝜓 | 𝜑 U[𝑎,𝑏 ] 𝜓, (1)
from the grid interconnection point through transformers and dis-
tribution lines to internal buses, where compute loads and UPS
                                                                            where □ [𝑎,𝑏 ] reads “always on [𝑎, 𝑏],” ^ [𝑎,𝑏 ] reads “eventually within
and BESS converters are connected. UPS and BESS resources are
                                                                            [𝑎, 𝑏],” and 𝜑 U[𝑎,𝑏 ] 𝜓 reads “𝜑 until 𝜓 within [𝑎, 𝑏]”. Beyond the
especially relevant for LVRT because they sit between the grid
                                                                            boolean verdict 𝑥 |= 𝜑, STL has a quantitative robustness 𝜌 (𝜑, 𝑥):
and the computing load [3, 39]. They can buffer active power, pro-
                                                                            positive exactly when 𝑥 satisfies 𝜑, with its magnitude being the
vide or consume reactive power, and protect internal equipment
                                                                            margin of satisfaction or violation [6, 17]. These operators can ex-
from voltage disturbances. Their behavior is constrained by hard-
                                                                            press many cyber-physical requirements, such as maintaining a
ware ratings: active-power limits, reactive-power limits, energy
                                                                            signal within a safe range, responding within a deadline, or satisfy-
limits, and apparent-power capacity. In power-electronics models,
                                                                            ing a condition over a time interval. LVRT has this same structure,
active power 𝑃 and reactive power 𝑄 often share the same con-
                                                                            since voltage ride-through, active power floor, and recovery are
verter capacity 𝑆, e.g., 𝑃 2 + 𝑄 2 ≤ 𝑆 2 . These converter resources
                                                                            all time-dependent. Synthesis from temporal-logic specifications,
are typically what prior ride-through controller designs actuate:
                                                                            which decides whether any controller can satisfy a given specifica-
centralized and decentralized voltage control over the facility’s
                                                                            tion, is studied extensively in robotics and control [7, 25]. For STL
internal distribution network [42], grid-forming control of UPS
                                                                            in particular, synthesis can be formulated as an optimization prob-
and BESS converters [1, 36], passivity-based converter control for
                                                                            lem [33, 34]: Given a plant model 𝑦 = 𝑔(𝑢, 𝑤) mapping a control
DC facilities [40], and coordinated grid-side storage that absorbs
                                                                            signal 𝑢 and a disturbance 𝑤 to the output 𝑦, a feasible control set
load transients [26, 30]. These designs are validated on simulated
                                                                            𝐾, and an STL formula 𝜑, synthesis solves
faults, but treat the grid code informally: they can neither certify
compliance nor establish that no compliant controller exists.                                                   
                                                                              𝑢 ★ = arg min 𝐽 (𝑢) s.t. 𝜌 𝜑, 𝑦 ≥ 0, 𝑦 = 𝑔(𝑢, 𝑤), 𝑢 ∈ 𝐾, (2)
   In terms of compute, data centers are increasingly dynamic loads.                     𝑢

Prior work on GPU and AI workload power management shows                    for a control cost 𝐽 . The constraint 𝜌 ≥ 0 requires even the tightest
that software can change the power profile through power caps,              clause of 𝜑 at its tightest instant to hold. BluSTL [14] implements
frequency scaling, scheduling, and workload shifting, for efficiency        this method by encoding the bounded STL formulas as mixed-
and demand response [2, 12, 28, 41]. A related line coordinates             integer constraints over a discretized time window, solving (2) in-
data centers with the grid in normal operation, including voltage           side a receding-horizon loop and applying the first action each step,
regulation via GPU-level actuation [27]. These software knobs act           yielding a model predictive controller (MPC). For power systems,
on timescales too coarse for a low-voltage event, so they cannot            this synthesis approach has targeted generation-side frequency
serve as fault-time controls. The workload still impacts the ride-          regulation with energy storage [43, 44] and grid-supportive DER
through problem through the pre-fault active power, which sets              modes [45], but not load-side ride-through. We build our synthesis
the grid code’s power floor and recovery target.                            on a Python reimplementation of BluSTL and instantiate (2) for our
                                                                            plant and specification in §3.3.

                                                                            3    SolVRT Design
2.3     The Case for LVRT Formal Specifications                             LVRT grid codes require data centers to stay connected during low
Formal specifications are logical statements with precise seman-            voltage events. To do so, a data center must carefully control its en-
tics, in stark contrast to natural language, which is the common            ergy storage resources and UPS systems. This section investigates
method for describing grid codes. Their precision is what enables           how the data center should perform this control. We first formalize
automated verification and synthesis, and safety-critical domains           grid codes using STL, which expresses LVRT requirements in a
have long adopted them for exactly this reason. Specifically, assume-       machine-readable format. We then provide a synthesis algorithm
guarantee specifications have been proposed as the algebra of com-          to find a controller for a given data center, deriving a control law
positional system design [9, 21, 22]: one side states assumptions on        and certifying its compliance with the grid code. If no such control
its environment, and the other upholds guarantees whenever those            law can be found, we perform diagnosis to suggest changes to the
assumptions hold. They have been applied to aircraft electric power         data center’s parameters to achieve compliance—e.g., by increas-
systems [32], space missions [35], and networked control [10, 23];          ing power electronic device capacity, redesigning the data center
this paper argues for taking a similar approach to LVRT analysis.           topology, or shaping workload power consumption.
                                                                        3
                                                                                                                                           Wang et al.




Figure 2: High-level architecture of SolVRT, comprising three main components: grid code formalization (§3.2), controller
synthesis (§3.3), and diagnosis and provisioning (§3.4). A grid code is encoded as a formal spec in our STL-based DSL. The
spec and the data center’s parameters are encoded into a controller synthesis query. When feasible, the query returns a
correct-by-construction MPC controller; when infeasible, diagnosis and provisioning computes changes that restore compliance.
A simplified internal power topology of a data center is shown on the left, with LVRT signals at their measurement points.


      symbol   meaning                                                         of the power floor during the fault and the recovery target during
      𝑣𝑔       grid voltage at the point of connection                         recovery. (iii) 𝑣𝑔 : The grid voltage 𝑣𝑔 at the point of data center /
      𝑣𝑖       min internal bus voltage over 𝑛 compute buses                   grid connection is the disturbance: this signal sags during a grid
      𝑝        aggregate active power drawn from the grid                      fault, and triggers an LVRT response from the data center. Figure 2
      𝑝 pre    pre-fault active power (i.e., 𝑝 at the time of the fault)       shows where these three signals are measured in the data center.
        Table 1: Signals used to encode LVRT grid code.                        The duration for which the data center is required to stay connected
                                                                               to the grid depends on the severity of the sag. For more severe sags,
                                                                               the required duration is shorter; if the sag exceeds the threshold,
3.1     LVRT Grid Codes                                                        the data center is allowed to instantaneously disconnect, and the
Grid operators have introduced LVRT grid codes, which regulate                 grid code requirements are lifted. Table 1 lists the signals.
the behavior of a data center during a voltage event and usually                  As §2 describes, LVRT codes share the same three obligations
contain three components. The grid codes require the data center               and differ only in the values each takes. The next subsection intro-
to stay connected during a grid voltage sag, keep active power draw            duces a language that the grid code author can use to turn these
above a level during the sag, and recover active power draw within             requirements into formal specifications.
a deadline after the sag is cleared. The following simplified example
is provided by ERCOT [16]:
                                                                               3.2    Formalizing LVRT Grid Codes
      ERCOT LVRT grid code snippet                                             As discussed in §3.1, the LVRT requirement is defined over multiple
                                                                               post-fault time segments, with time-coupled conditions and nontriv-
   A data center shall remain connected to the Transmission
                                                                               ial rules for active-power floors during voltage sags and recovery.
   Grid during voltage conditions requiring ride-through. When
                                                                               This temporal coupling and piecewise structure make it challenging
   grid voltage falls below 0.9 pu but remains above 0.8 pu, the
                                                                               to directly verify data center compliance using static operating-
   data center shall continue consuming active power during
                                                                               point analysis or conventional device-level checks. STL, on the
   the low voltage condition, and may reduce it proportional to
                                                                               other hand, has enough expressivity to write these requirements.
   the voltage drop, but shall return to 90% of its pre-disturbance
                                                                               Specifically, through the always (□) and eventually (^) operators
   level within two seconds of voltage returning above 0.9 pu.
                                                                               over time intervals, it provides a convenient basis for the formal-
                                                                               ization of the LVRT requirements. Encoding LVRT requirements
   LVRT involves the following three signals. (i) 𝑣𝑖 : In order for            in STL not only removes ambiguity, but also enables automated
a data center to stay connected, its internal compute bus voltage              synthesis of a controller for a given data center and grid code. Such
𝑣𝑖 must be above a threshold; otherwise, overly low voltages will              a synthesized controller is guaranteed to satisfy the requirements
trigger protection mechanisms that disconnect the data center from             under all possible scenarios when such a controller exists. Next, we
the grid and switch to a backup power source (e.g., diesel genera-             use the ERCOT example to illustrate this encoding in a new specifi-
tors), in order to prevent damage to power electronics inside the              cation language for LVRT grid codes. Figure 3 defines the language,
data center. (ii) 𝑝: The data center draws an aggregate active power           and the rest of this subsection instantiates it for the ERCOT code.
𝑝 from the grid; at the time of the fault, the power draw 𝑝 pre is                A specification begins with variable declarations. Signals are
called the pre-fault active power, read off the workload trace at              time-varying quantities measured at the points shown in Figure 2
the fault instant. This is the reference value, and it sets the scale          (e.g., grid voltage 𝑣𝑔 ); parameters are constant values for a data
                                                                           4
Synthesizing Voltage Ride-Through Controllers for Data Centers


center (e.g., the equipment trip level 𝑣 trip ); variables are computed                   𝑠𝑝𝑒𝑐         ::= 𝑑𝑒𝑐𝑙 +     𝑎𝑠𝑠𝑢𝑚𝑒      𝑔𝑢𝑎𝑟𝑎𝑛𝑡𝑒𝑒
from signals and parameters. ERCOT declarations are as follows.                           𝑑𝑒𝑐𝑙         ::= signal 𝑥 | param 𝑥
 1   signal Vg, Vi, p; // definitions in Table 1                                                         | var 𝑥 [ = 𝑒𝑥𝑝𝑟 ]
 2   param Vtrip;      // equipment tripping voltage                                                     | event 𝑒 = (fall | rise) (𝑥, 𝑐𝑜𝑛𝑠𝑡 ) [after 𝑒 ]
 3   param T_hold;     // recovery hold window
 4   var    p_pre;     // power draw at time of fault                                     𝑎𝑠𝑠𝑢𝑚𝑒       ::= assume { (𝑑𝑒𝑐𝑙 | 𝑝𝑟𝑒𝑑)+ }
                                                                                          𝑔𝑢𝑎𝑟𝑎𝑛𝑡𝑒𝑒    ::=   guarantee { (𝑑𝑒𝑐𝑙 | 𝜑)+ }
Among these, 𝑝 pre and 𝑇hold are interpretations we make where the                        𝜑            ::=   𝑝𝑟𝑒𝑑 | Always[𝐼 ] 𝜑 | Eventually[𝐼 ] 𝜑
ERCOT text is underspecified, rather than values taken literally                          𝐼            ::=   [𝜏, 𝜏 ]      𝜏 ::= 𝑒 | 𝜏 + 𝑑𝑢𝑟 | 𝑑𝑢𝑟
from it; §5 details both.                                                                 𝑝𝑟𝑒𝑑         ::=   𝑒𝑥𝑝𝑟 (≥ | ≤ |<) 𝑒𝑥𝑝𝑟 | 𝑒𝑥𝑝𝑟 in [ 𝑐𝑜𝑛𝑠𝑡, 𝑐𝑜𝑛𝑠𝑡 )
   An event is defined when a signal of interest crosses a threshold.                     𝑒𝑥𝑝𝑟         ::=   𝑐𝑜𝑛𝑠𝑡 | 𝑥 | 𝜏 | 𝑥 at 𝑒 | 𝑒𝑥𝑝𝑟 (+ | − | ·) 𝑒𝑥𝑝𝑟
For instance, in the code below, a fault event occurs when 𝑣𝑔 falls                                      |   { (𝑝𝑟𝑒𝑑 ⇒ 𝑒𝑥𝑝𝑟 )+ }
below the required 0.90 pu, and a recovery event occurs when 𝑣𝑔
                                                                                        Figure 3: Grammar of the grid code specification language.
is brought back after a fault. The pre-fault power draw is taken
                                                                                        Keywords are in bold; 𝑥 stands for declared names, 𝑒 for de-
from 𝑝 right before the fault event.
                                                                                        clared events. signals are measured and params data-center-
 5   event fault    = fall(Vg, 0.90);
 6   event recovery = rise(Vg, 0.90) after fault ;                                      supplied, while vars are derived; an event binds the time
 7   p_pre = p at fault; // sample just before fault                                    instant of a threshold crossing. The assume block describes
                                                                                        the admissible disturbance; the guarantee block is a conjunc-
   §3.1 describes the grid voltage sag ranges and the maximum
                                                                                        tion of clauses 𝜑: STL predicates over time windows 𝐼 , which
durations for which the data center must stay connected. These are
                                                                                        are event-anchored or relative. A predicate is a comparison
the conditions under which a data center is required to perform
                                                                                        or a band-membership test.
LVRT. The assume block captures them as follows:
 8   assume {
 9     var duration = {     // ride-through envelope                                    Hold the power floor. Throughout the fault duration, the active power
10       Vg in [0.80, 0.90) => 2.0s;                                                    must not fall below the floor level 𝜇 defined in the guarantee block:
11       Vg in [0.50, 0.80) => 0.5s;
12       Vg in [0.35, 0.50) => 0.25s;                                                                           𝜑 flr := □ [𝑡 𝑓 , 𝑡𝑟 ] (𝑝 ≥ 𝜇).                (5)
13       Vg in [0.00, 0.35) => 0.15s;
14     }                                                                                Recovery. After the recovery event, the active power must reach a
15     recovery - fault <= duration                                                     target lower bound, 𝑙 = 0.9 · 𝑝 pre , within a deadline 𝑇 = 2 seconds,
16   }
                                                                                        and then hold that level for a window 𝑇hold . The eventually operator
In the assume block, the ride-through envelope maps each sag depth                      ^ over [𝑡𝑟 , 𝑡𝑟 + 𝑇 ], with a nested always operator □ over [0,𝑇hold ],
to its maximum sag duration, and the final line assumes the grid                        captures this:
voltage recovers within that duration.                                                                   𝜑 rec := ^ [𝑡𝑟 , 𝑡𝑟 +𝑇 ] □ [0,𝑇hold ] (𝑝 ≥ 𝑙).        (6)
   If these assumptions hold, the data center is to uphold three
LVRT guarantees shown in the code below. The guarantee block                            The code’s text requires only the return of active power within the
first defines the active power floor level 𝜇 that the grid code re-                     deadline after grid voltage recovers. We additionally require the
quires, then states the three clauses expressed in STL operators and                    level to hold for 𝑇hold , so that a momentary spike in power draw
anchored at the two events, fault and recovery.                                         does not count as recovery; §5 discusses this interpretation in detail.
18   guarantee {                                                                           On the other hand, if the grid voltage goes beyond the envelope,
19       // active power floor                                                          the assumptions are violated and the data center does not need to
20       var mu = {
21         Vg in [0.50, 0.90) => Vg * p_pre;
                                                                                        perform LVRT.
22         Vg in [0.00, 0.50) => 0;
23       }                                                                              3.3      Synthesizing LVRT Controllers
24       // clause 1: data center stays connected:
25       Always[fault, recovery] (Vi >= Vtrip);                                         Given an LVRT specification, our goal is to determine whether
26       // clause 2: holds power floor:                                                a data center can satisfy it. We address this task using controller
27       Always[fault, recovery] (p >= mu);
28       // clause 3: power draw eventually recovers                                    synthesis. The data center exposes two signals, the internal bus
29       Eventually[recovery, recovery+2s](Always[0, T_hold] (p >= 0.9 * p_pre));       voltage 𝑣𝑖 and the aggregate active power 𝑝. Neither can be con-
30   }
                                                                                        trolled directly, as they are derived from the active and reactive
The full requirement is the conjunction of three STL clauses, each                      power (𝑃 and 𝑄) that the BESS/UPS devices inject. We express the
a formula 𝜑 of the grammar (Figure 3) with its time windows an-                         two converter control actions together as 𝑢 := (𝑃, 𝑄), which is the
chored at the declared events. We refer to them as connection                           control input for the data center.
(𝜑 conn ), active power floor (𝜑 flr ), and recovery (𝜑 rec ):                             To characterize how the control input 𝑢 affects the LVRT ca-
                                                                                        pability of data centers, we require a plant model of the data cen-
                           𝜑 := 𝜑 conn ∧ 𝜑 flr ∧ 𝜑 rec .                      (3)       ter’s internal electrical network. We adopt the LinDistFlow model
                                                                                        (§2), under which the internal bus voltage 𝑣𝑖 is an affine function
Stay connected. The data center’s internal voltage 𝑣𝑖 must stay above                   of the grid-side voltage and the converter injections 𝑢 := (𝑃, 𝑄).
the power-electronics trip threshold 𝑣 trip over the fault window                       The active power 𝑃 contributes directly to the aggregate active
[𝑡 𝑓 , 𝑡𝑟 ]:                                                                            power 𝑝 in the LVRT specification, while both 𝑃 and reactive power
                        𝜑 conn := □ [𝑡 𝑓 , 𝑡𝑟 ] (𝑣𝑖 ≥ 𝑣 trip ).               (4)       𝑄 affect internal voltage. These two actions are coupled by the
                                                                                    5
                                                                                                                                          Wang et al.


converter apparent-power rating 𝑆, which imposes the constraint
𝑃 2 + 𝑄 2 ≤ 𝑆 2 . Thus, the reactive power used to support voltage
reduces the remaining active-power headroom available to satisfy
the active-power floor, and a converter with insufficient capacity
may be unable to satisfy both requirements simultaneously. We
denote these rating limits as the feasible control set 𝐾.
    The controller synthesis procedure searches for control actions
whose resulting 𝑣𝑖 and 𝑝 satisfy the specification discussed in §3.2,
or certifies that none exists. A grid code like ERCOT’s expresses the
grid-voltage assumption as a set of bands, with each voltage band
paired with a maximum ride-through duration. The assume block
admits infinitely many disturbance traces, one for every sag shape
inside the envelope, and the controller must satisfy the guarantees
under all of them. Therefore, we synthesize against the single worst-
case trace 𝑣𝑔′ that lower-bounds them all, holding each band at its
lowest voltage for its full duration and ordering the bands from              Figure 4: The conflict frontier. The frontier (blue) is the
deepest to shallowest,                                                        largest active power floor the data center can sustain while
                                                                              staying connected at each sag depth. The grid requirement
                  𝑣𝑔′ (𝑡) = min { 𝑣 : dur(𝑣) ≥ 𝑡 },                (7)        𝜇 = 𝑣𝑔 𝑝 pre (red) is the floor the code demands. Left of their
                                                                              crossing, the conflict edge, the requirement is feasible; right
where dur(𝑣) is the maximum ride-through duration the specifica-
                                                                              of it the requirement exceeds the capability (solid red) and
tion’s assume block assigns to a sag of depth 𝑣. The result is the
                                                                              no controller exists. Provisioning (dashed) raises the frontier
longest and deepest sag the assumption admits, the binding case
                                                                              until the requirement lies inside the feasible region.
for the connection clause; it is the lower boundary of the ERCOT
region in Figure 1. When a code instead specifies a voltage–time
curve, as Energinet does (the dashed curve in Figure 1), we use that          methods to diagnose the clauses of the grid code that cannot be met
curve directly as 𝑣𝑔′ [15].                                                   and compute the changes that could restore feasibility. We obtain
   The synthesis problem takes two disturbance signals, inputs                both from the same synthesis query by treating the voltage sag
the controller observes but does not choose: the grid voltage, for            depth and active-power floor as parameters of the specification and
which we use the worst-case trace 𝑣𝑔′ , and the workload’s active             computing, for each sag depth, the largest floor at which the query
power draw 𝑤 comp , the compute demand the facility must serve. We            stays feasible.
write the two disturbances together as 𝑤 = (𝑣𝑔′ , 𝑤 comp ). With the             We call the resulting boundary the conflict frontier, a new ab-
disturbances and the plant model in place, we instantiate the clauses         straction that we use for diagnosis, as shown in Figure 4. This is the
in the specification. The voltage trace sets the fault and recovery           maximum active power the data center can guarantee to draw from
times 𝑡 𝑓 and 𝑡𝑟 , turning each time window into a numeric interval.          the grid while staying connected as a function of sag depth. This
The workload trace sets the pre-fault draw 𝑝 pre = 𝑝 (𝑡 𝑓 ), turning          abstraction allows us to diagnose which grid code clauses cannot
the active power floor 𝜇 and recovery target into numeric bounds.             be jointly met. Afterward, we modify the data center’s parameters
The plant model replaces the output signals 𝑣𝑖 and 𝑝 with their               until the requirement lies fully inside the feasible region under the
expressions in the control 𝑢 and the disturbance 𝑤. Substituting all          frontier.
three into the clauses of (3) completes the instantiation, producing
the concrete STL formula 𝜑 over the control variables. Algorithm 1               The conflict frontier. The frontier slopes downward because the
in Appendix A lists the full procedure.                                       connection clause and the active power floor clause draw on the
   With the clauses 𝜑, the plant model mapping 𝑔, the feasible set            same resource. To maintain the connection clause during a deeper
𝐾, and the disturbance 𝑤 all concrete, we instantiate the synthesis           voltage sag, the UPS’s grid-facing converter needs to reserve a larger
problem (2) of §2, with output 𝑦 := (𝑣𝑖 , 𝑝) and cost 𝐽 (𝑢) = ∥𝑢 ∥,           portion of its apparent-power rating for reactive-power support 𝑄
selecting the least-effort compliant control 𝑢 ★ composed of per-             to maintain the data center internal voltage 𝑣𝑖 . Under the converter
step 𝑃 and 𝑄. We solve the instantiated problem with our Python               rating constraint 𝑃 2 + 𝑄 2 ≤ 𝑆 2 , this increased reactive-power pro-
reimplementation of BluSTL (§2). A feasible query yields an MPC               vision reduces the remaining capacity available for active-power 𝑃.
controller that satisfies the instantiated guarantees for the specified       Consequently, the largest floor the converter can sustain decreases
voltage trace, workload trace, plant model, and hardware limits.              as the sag depth increases. The requirement 𝜇 = 𝑣𝑔 · 𝑝 pre also de-
An infeasible query means that no such controller exists for that             creases with depth, so the most challenging sag is not necessarily
synthesis instance, which we consider next.                                   the deepest one; the binding depth is wherever the requirement
                                                                              exceeds the frontier the most.
3.4    Diagnosis and Provisioning                                                Computing the frontier. The active power floor for each voltage
The control synthesis query in §3.3 yields a binary result about the          sag depth is monotone: a lower floor is always easier to sustain
feasibility of synthesizing a control law that satisfies the grid code.       since it requires lower 𝑃 and frees the converter headroom for 𝑄.
In cases where such a controller does not exist, we further develop           Leveraging monotonicity, we locate the largest sustainable active
                                                                          6
Synthesizing Voltage Ride-Through Controllers for Data Centers


power floor for each voltage sag depth using binary search. Sweep-            4     Results
ing the voltage sag depth traces the frontier, the largest sustainable        The evaluation answers three key questions: (a) on a live grid, does
floor at each depth. The grid code’s requirement is the second curve          the synthesized controller comply with the grid code where alter-
over the same axes, where the code demands the active power floor             native control schemes fail (§4.1); (b) when the synthesis query is
𝜇 = 𝑣𝑔 · 𝑝 pre at each depth. When the requirement exceeds the fron-          infeasible, can SolVRT diagnose which clauses conflict or whether
tier, no controller exists, and the crossing marks the conflict edge,         any individual clause is unsatisfiable (§4.2); and (c) what is the
the deepest sag the data center can both ride through and hold the            smallest hardware or workload change that restores compliance
required floor. We compute the frontier with inspiration from two             (§4.3)?
established directions of work. Parametric STL treats values inside
a temporal-logic spec as parameters [4], often used in specification             Setup. We evaluate on a data center instantiated from the Vulcan
mining to derive the tightest spec a fixed model satisfies [19, 24];          facility data [38]: eight compute nodes, each modeled as a 20 MW
we likewise treat the active-power floor and the voltage sag depth            load supplied through an upstream UPS with a 25 MVA grid-facing
as parameters of the STL spec, but the inner oracle at each param-            converter; two 20 MVA battery (BESS) units sit at the facility’s
eter value is whether a controller (2) exists, instead of whether a           distribution bus; and a 40 MW cooling plant brings the rated facility
fixed model satisfies the formula. Multiparametric programming                draw to 200 MW. The compute draw follows the measured power of
characterizes how the solution of an optimization varies with its             a synchronous AI training job [12], normalized to peak and scaled
parameters [8], used in explicit model predictive control to precom-          to the facility’s compute capacity.
pute the control law as a function of state; we likewise sweep these               Live grid simulator. The controller of §3.3 is synthesized against
parameters, but keep only the boundary of the feasible region as              the worst-case trace of the grid code envelope; §4.1 runs it closed-
the conflict frontier, instead of the control law across it.                  loop on a grid simulator, which changes its input in two ways. First,
                                                                              the measured voltage is one realized transient inside the assumed
   Diagnosis. To attribute an infeasibility to specific clauses, we           envelope, produced by the grid model, not the worst-case bound
recompute (2) over subsets of the guarantee clauses and isolate the           of (7). Second, the loop is closed: the data center’s own 𝑃 and 𝑄 enter
minimal infeasible subset, which is the set of clauses for which              the grid’s power-flow solution and change the grid voltage the data
no controller exists but dropping any single clause makes the rest            center measures next. We connect the data center to ANDES [13]
feasible. This is the Irreducible Infeasible Subsystem (IIS) of the           on the 140-bus NPCC system on bus 128. The disturbance is a
program [11]. IIS extraction usually explains an infeasible program           three-phase fault near the interconnection, applied at 𝑡=1 s and
to the author; in our case, we leverage IIS to identify the set of            held for its band’s ride-through duration before clearing (2 s for
grid code clauses in conflict, turning the infeasibility reported by          a sag in [0.8, 0.9), 0.5 s for sags in [0.5, 0.8)). The closer the fault,
the solver into a diagnosis. With three clauses, as in the ERCOT              the deeper the interconnection voltage sags; we vary the fault
example, every subset can be tested with ease. If a grid code presents        impedance on the transmission grid to simulate faults at different
more guarantee clauses, we can rely on the MILP solver to extract             electrical distances, producing voltages of different depths inside
an irreducible infeasible subset on its own [18]. A clause that is            the envelope the code assumes. Every 0.02 s the controller reads
infeasible on its own cannot be satisfied with any controller. Clauses        the interconnection voltage, re-solves with the measurement held
that are feasible individually but infeasible together are in conflict,       constant over its horizon, converts the first action to aggregate
such as the connection and active power floor clauses competing               𝑃 and 𝑄, and writes them to the load; ANDES takes the 𝑃 and 𝑄
for the apparent power rating 𝑆.                                              and advances, and the next interconnection voltage measurement
                                                                              closes the loop. In every run, the facility’s undervoltage protection
                                                                              disconnects the data center if the internal voltage 𝑣𝑖 remains below
   Provisioning. Provisioning closes the gap between the require-             𝑣 trip = 0.9 for 0.02 s, and a disconnected facility draws zero power.
ment and the frontier by raising the frontier or lowering the require-
ment through three knobs. 1) The UPS/BESS power-conversion-                      Experiment design. The subsections map to the three questions
system (PCS) apparent-power rating 𝑆 raises the frontier directly: a          and isolate one variable at a time. To answer (a), §4.1 varies the con-
larger apparent power rating allows more 𝑃 and 𝑄 simultaneously,              troller on a provisioned variant of the facility with converters rated
with more reactive power headroom to maintain internal voltage                at 𝑆=40 MVA per node, large enough that a compliant controller
and more active power to maintain the active power floor. 2) As               exists at every voltage sag depth the grid code covers: no controller
part of the plant model, increasing the interconnection reactance             and a penalty-based controller from prior work [42] serve as base-
of lines and transformers raises the converter’s voltage authority:           lines against the controller synthesized from (2), each run with the
a larger reactance gives more internal-voltage change per unit of             live grid simulator on the same faults. To answer (b) and (c), §4.2
reactive power injection, so lower 𝑄 holds the internal voltage at a          and §4.3 hold the synthesized controller fixed and return to the
given sag depth and more of the rating 𝑆 is left for 𝑃. 3) Adjusting          as-built 25 MVA rating, where the synthesis query is infeasible and
the workload power profile acts on the requirement: lowering the              the diagnosis and provisioning of §3.4 take over.
pre-fault draw 𝑝 pre lowers the active power floor requirement dur-
ing the fault, lowering the grid code requirement curve against the           4.1    Ride-through Effectiveness on a Live Grid
conflict frontier. Each of the three knobs is monotone, allowing us              No controller (Figure 5). With the UPS and BESS taking no control
to apply binary search to derive the value at which the query first           action to inject active or reactive power, the internal voltage fol-
becomes feasible, i.e., the smallest change that restores compliance.         lows the grid voltage. The fault sags 𝑣𝑔 to 0.71 and 𝑣𝑖 follows; after
                                                                          7
                                                                                                                                           Wang et al.




Figure 5: No-controller baseline. The fault at 𝑡=1 s trips the
data center; both the internal voltage and the active power
draw drop to zero, violating all three clauses.




                                                                              Figure 7: Synthesized controller on three sag depths. Thin
                                                                              dotted curves in the top panel are each run’s grid voltage
                                                                              𝑣𝑔 ; the shallow sag is held for its band’s 2 s duration and the
                                                                              mid and low sags for 0.5 s, all inside the ERCOT envelope.
                                                                              In every run the controller holds 𝑣𝑖 just above 𝑣 trip while the
                                                                              draw 𝑝 tracks the workload above its floor 𝜇.

                                                                              toward nominal, with a weight 𝑐 penalizing deviation from normal
                                                                              operation. It’s expressed as min𝑢 ∥𝑣𝑖 − 1∥ 2 + 𝑐 ∥𝑢 − 𝑢 nom ∥ 2 over the
                                                                              same feasible set 𝐾, where 𝑢 nom is normal operation: the converters
                                                                              simply import compute draw and provide no reactive support. This
                                                                              is the objective of the controller that Xie et al. used [42], written
                                                                              in our notation and with their per-device effort weights collapsed
                                                                              to the single scalar 𝑐 and their box bounds replaced by 𝐾, so the
                                                                              penalty controller commands the same hardware as the synthesized
Figure 6: Penalty-based controller under three penalty                        one. In such a penalty-based controller, no grid code clause of 𝜑
weights on the same fault. The grid voltage 𝑣𝑔 differs across                 appears in the objective. We run three weights on the same fault
runs because the loop is closed. Controller with high cost                    as the no-controller run. At 𝑐=5 (high control cost) the controller
trips data center at the fault onset; one with moderate cost                  is reluctant to act, with 𝑣𝑖 reaching only 0.79 and the data center
holds 𝑣𝑖 near 0.90 and trips mid-fault at 𝑡=1.34 s; one with low              tripping at the fault onset. At 𝑐=0.001 (low control cost) it holds
cost rides through.                                                           𝑣𝑖 ≈ 1 and the active power draw stays above the floor as a result,
                                                                              which is grid code compliant. At 𝑐=0.8 (medium control cost), the
the 0.02 s pickup the protection disconnects the facility. All three          controller holds 𝑣𝑖 ≈ 0.90 with almost no margin through the
clauses fail together: 𝑣𝑖 drops below 𝑣 trip and the data center dis-         first 0.3 s of the fault, then 𝑣𝑖 slips under the threshold and the
connects (connection); as a result, the 160 MW draw drops to zero,            data center trips at 𝑡=1.34 s; the active power draw drops to zero,
below the ≈110 MW floor (floor), and it never returns to 0.9 𝑝 pre            and the floor and recovery clauses fail with it. Compliance thus
within the 2 s deadline (recovery). The grid recovers after the fault         depends entirely on the hand-picked weight, and the formulation
is cleared and 𝑣𝑔 settles above its pre-fault value: the disconnection        gives no prior indication of the compliant range: a weight that
becomes a disturbance. At one facility the post-fault voltage over-           survives the fault onset can fail partway through, and the floor
shoot is modest, but it becomes a systemic event when a cluster of            and recovery are met only incidentally. In our case, the synthesis
facilities trips at the same time, as observed in the Virginia incident       query (2) decides compliance offline before the fault instead of
in 2024 [31], the behavior the code is written to prevent.                    during it: it either returns a compliant controller by construction,
                                                                              or reports infeasibility at design time with no compliant controller.
   Penalty controller (Figure 6). Penalty-based voltage control is
the standard alternative, which can hold the internal voltage to                 Synthesized controller (Figure 7). The controller synthesized from (2)
avoid tripping, but compliance depends on a hand-tuned weight                 rides through three voltage sag depths inside the assumed voltage
and carries no guarantee. We implement a data-center voltage                  envelope and complies with the grid code. During each fault, the
controller from prior work [42]: at each step, the control law chooses        controller holds 𝑣𝑖 slightly above 𝑣 trip (a 0.005 pu robustness mar-
the converter’s P and Q injections that pull the internal voltage             gin), injecting more reactive power the deeper the sag: roughly 70,
                                                                          8
Synthesizing Voltage Ride-Through Controllers for Data Centers




Figure 8: Conflict frontier of the as-built facility, swept at 81
depths (0.005 pu apart). The frontier is capped at 100% of 𝑝 pre ,
since a floor above the pre-fault draw is meaningless. The
orange marker at 𝑣𝑔 = 0.63 is the depth examined in Figure 9,                  Figure 9: The conflict at 𝑣𝑔 = 0.63. Only the connection clause
with its clause-subset diagnosis in the box.                                   is enforced for demonstration; with best effort on the active
                                                                               power clause, the converter headroom is not enough for ac-
170, and 300 MVAr at depths 0.83, 0.70, and 0.54. The converter ac-            tive power to satisfy the floor clause, causing a violation.
tive power simply tracks the compute demand and meets the floor
with no curtailment, because at this rating the reactive support
                                                                               §3.4, finding at each depth between 0.90pu and 0.50pu the largest
and the full compute load fit inside the apparent-power headroom
                                                                               floor the data center can sustain while staying connected, and re-
together, so compliance with active power floor as well as recovery
                                                                               solving the query over clause subsets at each depth. The required
costs no active power control action. The guarantee is conditional
                                                                               floor crosses the frontier at 𝑣𝑔 ≈ 0.65pu, the conflict edge. Between
on exactly this headroom, where the facility’s 40 MVA converters
                                                                               0.65pu and 0.62pu the data center can either stay connected or
sit above the minimum that §4.3 derives; on the as-built 25 MVA
                                                                               maintain the active power floor, but not both. Below 0.62pu, hold-
rating, the 𝑃 and 𝑄 no longer fit together and the query returns
                                                                               ing internal voltage to stay connected alone is infeasible, at what
infeasible and no controller exists. The next subsections turn that
                                                                               we call the connection wall. At the wall the frontier ends at 40 MW
infeasibility into a diagnosis and a provisioning decision.
                                                                               (20% of 𝑝 pre ) rather than zero, where the converters are fully spent
                                                                               on reactive support, and the residual is the cooling draw, which is
4.2     Infeasibility Diagnosis
                                                                               served without a converter and sits outside the control knobs we
This subsection and the next fix the controller and return to the              model. Inside the conflict region, raising the capability or lowering
baseline data center with the as-built 25 MVA rating in the Vulcan             the requirement both restore feasibility; below the wall, only raising
system [38]. The question is design-time feasibility, so no grid               the capability can help.
simulator is involved. The synthesis query of §3.3 takes three inputs.
The specification is the ERCOT code of §3.2. The plant model is the               The conflict on the time axis (Figure 9). Figure 9 shows what the
Vulcan facility at its as-built rating, modeled with LinDistFlow. The          conflict means in the time domain: even the largest active power
grid-voltage disturbance is the worst-case envelope of (7), restricted         draw the facility can sustain while staying connected falls short
to the depths where the active power floor applies (𝑣𝑔 ≥ 0.5); below           of the floor the spec requires. An infeasible query returns no con-
0.5 the code releases the active power floor and permits momentary             troller, so there is no control action trajectory to see the violation.
cessation, the facility briefly stopping its grid power draw and               We therefore plot a relaxation instead, by keeping enforcement
restoring it once the voltage returns, so no converter action is               on the connection clause and making the best effort toward the
required during the fault. The workload disturbance is the measured            active power floor clause. Staying connected takes 234 MVAr of
trace with the grid fault aligned to the trace peak. A fault can land          reactive power 𝑄, which nearly fills the converter headroom 𝑆, and
anywhere on the trace, and 𝑝 pre , the active power draw at the fault          the remaining active power 𝑃 supports an active power draw of
instant, sets the floor 𝜇 = 𝑣𝑔 𝑝 pre , so this alignment is the worst          only 92 MW, 34 MW below the 126 MW floor requirement. In other
case, 𝑝 pre = 200 MW. The synthesis query returns infeasible for               words, the connection clause is only satisfiable by giving up the
this combination of grid code spec, plant model, and disturbance,              active power floor clause inside the conflict region.
meaning no controller satisfies 𝜑.
   The conflict frontier (Figure 8). The synthesis against the as-built        4.3    Provisioning
facility fails in two ways, requiring different fixes. At moderate volt-       For a provisioning team, this subsection answers the question of
age sag depths, the connection and the active power floor clauses              which hardware to specify so that the facility is capable of comply-
conflict: each clause is satisfiable alone, but their conjunction is           ing with the LVRT grid code. Each knob is monotone, so a binary
not (the minimal infeasible subset of §3.4). At deeper voltage sags,           search on the synthesis query returns the smallest value at which it
connection is infeasible alone. Recovery is never among the fail-              turns feasible, a design requirement derived directly from the grid
ing clauses. We locate the two modes with the conflict frontier of             code and available before the facility is built or upgraded.
                                                                           9
                                                                                                                                            Wang et al.


                                                                                 connection wall to reach full grid code compliance. A workload cap
                                                                                 only lowers the grid code floor requirement and is still bounded
                                                                                 by the hardware constraints. Even a facility capped to a third of its
                                                                                 rated power draw clears only the conflict band. Hardware provi-
                                                                                 sioning is the more fundamental fix, while workload capping alone
                                                                                 is only a stop-gap for sags above the connection wall.


                                                                                 5   Discussion
Figure 10: Provisioning. (a) Hardware: each knob is plotted                         Grid code ambiguity. Formalizing ERCOT’s grid code exposed
at the minimal value that restores compliance, the converter                     two underspecified terms. First, the code scales its active power
rating 𝑆 raised from 25 to 38 MVA or the interconnection                         floor and recovery requirements to the facility’s “pre-disturbance
reactance scaled by 1.49; either lifts the frontier above the                    level” but does not define how that value is read. Over a fluctuating
requirement at every depth down to 𝑣𝑔 = 0.50. (b) Workload: at                   AI workload, different methods of deriving the “pre-disturbance
the minimal cap of 32% of rated draw, the capped requirement                     level” could give drastically different values. We take the instanta-
(dashed) falls below the frontier at every depth where the                       neous active power draw (§3.1) for this work, instead of taking an
facility can connect, removing the conflict, while compliance                    average over some window. Second, the recovery clause requires
is still bounded by the connection wall.                                         the facility to “return to 90% of its pre-disturbance level within
                                                                                 two seconds,” but presumably, a facility that touches the level at
                                                                                 the deadline and drops off immediately still violates the code. We
   Provisioning, hardware (Figure 10a). Provisioning closes the gap              add the hold window 𝑇hold of (6) so that recovery means genuine
between the requirement and the capability. §3.4 exposes two hard-               restored consumption rather than a momentary spike. These nu-
ware knobs and they help raise the frontier: the UPS converter                   ances emerged only when translating the natural-language grid
rating 𝑆 and the interconnection reactance. A larger 𝑆 widens the                code into a formal specification. This highlights the value of a for-
eight per-node apparent power rating headroom with more 𝑄 for                    mal approach, as it forces ambiguous requirements to surface and
connection and more 𝑃 for the floor at the same time. A larger                   be made explicit before they are enforced.
reactance moves more internal voltage per unit of 𝑄, so less of each
headroom holds 𝑣𝑖 and more remains for 𝑃. Both are monotone
and bisection returns the minimal change, 𝑆 from 25 to 38 MVA                        Modeling state-of-charge. We do not model energy storage state
per node (+50%) or reactance scaled by 1.49 in the model. Both                   of charge. Batteries in UPS and BESS may charge or discharge
hardware knobs lift the frontier above the requirement at every                  during ride-through. On the discharging side, riding-through a
depth down to 𝑣𝑔 = 0.50, the bottom of the active power floor band.              voltage event spends a small fraction of the stored energy, since a
Both knobs also push the connection wall below 0.50. The BESS                    VRT event lasts only a few seconds, while the UPS’s storage capacity
apparent power rating is a separate yet weaker knob, so we don’t                 is provisioned to carry the full compute load for tens of seconds and
demonstrate in Figure 10. Because BESS reactive power reaches the                the BESS for minutes. On the charging side, it requires batteries not
internal buses only through the facility trunk, its reactive power               held at full charge, and the headroom needed is likewise a small
injection barely helps maintain internal voltage to avoid tripping.              fraction of their provisioned capacity. Thus, we do not model the
                                                                                 state-of-charge (SoC), and assume the UPS and BESS have both
   Provisioning, workload (Figure 10b). The workload enters this                 enough stored energy for discharging and enough headroom for
analysis only through the pre-fault draw. During a fault the UPS                 charging during a VRT event.
battery carries the compute, which costs little energy over events
of a few seconds, and the grid-side draw becomes a control that the
synthesis sets freely, up to the converter rating. What the workload                Beyond one code and one facility. Similar to LVRT grid codes,
does during the fault therefore never appears in the fault-time con-             other grid codes regulate data center behavior for other types of
straints, but only as 𝑝 pre , the active power draw at the fault instant,        grid disturbances (e.g., frequency ride-through). ERCOT writes fre-
which sets the requirement 𝜇 = 𝑣𝑔 𝑝 pre . The software knob caps the             quency ride-through in the same document as voltage ride-through
pre-fault workload. The cap lowers 𝑝 pre and the requirement with it             with the same structure: an assumption envelope on grid frequency,
and leaves the frontier where it is. In our model, capping the draw              a power draw requirement dependent on the pre-disturbance level,
at 32% of rated (𝑝 pre = 64 MW) brings the requirement below the                 and a power draw recovery clause. SolVRT has the potential to
capability at every depth the data center can connect, with no hard-             solve frequency ride-through with minimal changes: our specifica-
ware change, removing the {𝜑 conn, 𝜑 flr } conflict entirely. However,           tion language can express these clauses with the same shape, just
the connection wall does not move with software changes alone,                   with frequency declared as the disturbance signal instead; however,
as it stays constrained by the maximum reactive power the UPS                    the plant model and control knobs differ, and we leave the adapta-
hardware can inject; no software capping connects the data center                tion to future work. On the data center side, while SolVRT certifies
below 0.62 and compliance down to 0.50 stays infeasible.                         individual data centers’ compliance with the LVRT grid code, the
   The contrast summarizes the provisioning section. Hardware                    aggregated behavior of clustered data centers and their impact on
raises data center capability by moving both the frontier and the                the grid remains an open grid-side question.
                                                                            10
Synthesizing Voltage Ride-Through Controllers for Data Centers


6    Conclusion                                                                               [14] Alexandre Donzé and Vasumathi Raman. 2015. BluSTL: Controller Synthesis
                                                                                                   from Signal Temporal Logic Specifications. In 1st and 2nd International Workshop
Data centers have grown into loads large enough that their protec-                                 on Applied Verification for Continuous and Hybrid Systems (ARCH). 160–168.
tive disconnection threatens the grid during voltage disturbances,                            [15] Energinet. 2024. Technical Regulation 3.4.3 Requirements for Transmission-
                                                                                                   Connected Demand Facilities, Revision 1.           Technical Report 3.4.3. En-
and emerging VRT grid codes now require them to ride through                                       erginet.     https://en.energinet.dk/media/bkpf4hef/technical-regulation-343-
such voltage events. This paper solves data center compliance with                                 requirements-for-transmission-connected-demand-facilities-revision-1.pdf
VRT grid codes using a controller synthesis approach. SolVRT ex-                              [16] ERCOT. 2026. Board Priority - Large Computational Load Ride-Through Require-
                                                                                                   ments. Nodal Operating Guide Revision Request 282NOGRR-30. Electric Reliabil-
presses a grid code as an assume-guarantee specification in Signal                                 ity Council of Texas. https://www.ercot.com/files/docs/2026/05/11/282NOGRR-
Temporal Logic, synthesizes a controller that complies by construc-                                30-ERCOT-Comments-051126.docx
tion whenever one exists, and turns infeasibility into a conflict                             [17] Georgios E. Fainekos and George J. Pappas. 2009. Robustness of Temporal Logic
                                                                                                   Specifications for Continuous-Time Signals. Theoretical Computer Science 410,
frontier, a diagnosis of the conflicting clauses, and a provisioning                               42 (2009), 4262–4291.
recommendation for the smallest hardware or workload change that                              [18] Gurobi Optimization, LLC. 2026. Model.computeIIS: Python API Refer-
                                                                                                   ence. Gurobi Optimizer Reference Manual. Gurobi Optimizer 13.0 documenta-
restores compliance. On a model of a 200 MW facility in a closed                                   tion. https://docs.gurobi.com/projects/optimizer/en/current/reference/python/
loop with a transmission grid simulator, the synthesized controller                                model.html#Model.computeIIS
rides through faults that trip the uncontrolled facility, and the diag-                       [19] Bardh Hoxha, Adel Dokhanchi, and Georgios Fainekos. 2018. Mining parametric
                                                                                                   temporal logic properties in model-based design for cyber-physical systems.
nosis traces the as-built rating’s infeasibility to converter capacity,                            International Journal on Software Tools for Technology Transfer 20, 1 (Feb. 2018),
for which a hardware upgrade restores feasibility. As grid operators                               79–93. doi:10.1007/s10009-017-0447-4
write ride-through rules for large loads and data center operators                            [20] IEEE. 2022. IEEE Standard 2800-2022: Interconnection and Interoperability of
                                                                                                   Inverter-Based Resources Interconnecting with Associated Transmission Electric
adapt to comply, SolVRT gives both sides a machine-checkable                                       Power Systems.
interface between grid requirements and data center capabilities.                             [21] Inigo Incer. 2022. The Algebra of Contracts. Ph. D. Dissertation. EECS Depart-
                                                                                                   ment, University of California, Berkeley. http://www2.eecs.berkeley.edu/Pubs/
                                                                                                   TechRpts/2022/EECS-2022-99.html
                                                                                              [22] Inigo Incer, Albert Benveniste, and Alberto Sangiovanni-Vincentelli. 2023. Some
                                                                                                   Algebraic Aspects of Assume-Guarantee Reasoning. arXiv 2309.08875 (2023).
References                                                                                         arXiv:2309.08875 [cs.LO] https://arxiv.org/abs/2309.08875
 [1] Yousef Abudyak, Mohsen Alizadeh, and Wei Sun. 2026. Mitigating Data Centers              [23] Inigo Incer, Noel Csomay-Shanklin, Aaron D. Ames, and Richard M. Murray.
     Load Risks and Enabling Grid Support Functions through Grid-Forming Control.                  2024. Layered Control Systems Operating on Multiple Clocks. IEEE Control
     arXiv:2602.01013.                                                                             Systems Letters 8 (2024), 1211–1216. doi:10.1109/LCSYS.2024.3410150
 [2] Fatih Acun, Can Hankendi, Ethan Levine, Hudson Reynolds, Joshua Bardwick,                [24] Xiaoqing Jin, Alexandre Donzé, Jyotirmoy V. Deshmukh, and Sanjit A. Seshia.
     and Ayse K. Coskun. 2026. Investigating Power Consumption Flexibility of AI                   2015. Mining Requirements From Closed-Loop Control Models. IEEE Transactions
     Data Centers for Demand Response Participation. In Proceedings of the 17th ACM                on Computer-Aided Design of Integrated Circuits and Systems 34, 11 (Nov. 2015),
     International Conference on Future and Sustainable Energy Systems. ACM, Banff ,               1704–1717. doi:10.1109/TCAD.2015.2421907
     Alberta , Canada, 344–348. doi:10.1145/3744255.3798112                                   [25] Hadas Kress-Gazit, Morteza Lahijanian, and Vasumathi Raman. 2018. Synthesis
 [3] Baris Aksanli, Alper Sinan Akyurek, and Tajana Rosing. 2015. Minimizing the                   for Robots: Guarantees and Feedback for Robot Behavior. Annual Review of
     effects of data centers on microgrid stability. In 2015 Sixth International Green             Control, Robotics, and Autonomous Systems 1 (2018), 211–236.
     and Sustainable Computing Conference (IGSC). IEEE, Las Vegas, NV, USA, 1–9.              [26] Soumya Kundu, Kaustav Chatterjee, Rakib R. Hossain, Sai Pushpak Nandanoori,
     doi:10.1109/IGCC.2015.7393720                                                                 and Veronica Adetola. 2025. Managing Risks from Large Digital Loads Using
 [4] Eugene Asarin, Alexandre Donzé, Oded Maler, and Dejan Nickovic. 2012.                         Coordinated Grid-Forming Storage Network. arXiv:2508.11080.
     Parametric Identification of Temporal Properties. In Runtime Verification, Sar-          [27] Zhirui Liang, Jae-Won Chung, Mosharaf Chowdhury, Jiasi Chen, and Vladimir
     fraz Khurshid and Koushik Sen (Eds.). Springer, Berlin, Heidelberg, 147–160.                  Dvorkin. 2026. GPU-to-Grid: Voltage Regulation via GPU Utilization Control.
     doi:10.1007/978-3-642-29860-8_12                                                              arXiv:2602.05116.
 [5] M.E. Baran and F.F. Wu. 1989. Optimal capacitor placement on radial distribution         [28] Zhenhua Liu, Adam Wierman, Yuan Chen, Benjamin Razon, and Niangjun Chen.
     systems. IEEE Transactions on Power Delivery 4, 1 (1989), 725–734. doi:10.1109/               2013. Data center demand response: avoiding the coincident peak via workload
     61.19265                                                                                      shifting and local generation. In Proceedings of the ACM SIGMETRICS/inter-
 [6] Ezio Bartocci, Jyotirmoy Deshmukh, Alexandre Donzé, Georgios Fainekos, Oded                   national conference on Measurement and modeling of computer systems. ACM,
     Maler, Dejan Ničković, and Sriram Sankaranarayanan. 2018. Specification-Based                 Pittsburgh PA USA, 341–342. doi:10.1145/2465529.2465740
     Monitoring of Cyber-Physical Systems: A Survey on Theory, Tools and Appli-               [29] Oded Maler and Dejan Nickovic. 2004. Monitoring Temporal Properties of
     cations. In Lectures on Runtime Verification: Introductory and Advanced Topics,               Continuous Signals. In Formal Techniques, Modelling and Analysis of Timed and
     Ezio Bartocci and Yliès Falcone (Eds.). Springer International Publishing, Cham,              Fault-Tolerant Systems (FORMATS/FTRTFT). 152–166.
     135–175. doi:10.1007/978-3-319-75632-5_5                                                 [30] Sina Mohammadi, Wayne Wang, Marcus Chen I Wada, Rouzbeh Haghighi, Ali
 [7] Calin Belta and Sadra Sadraddini. 2019. Formal Methods for Control Synthesis:                 Hassan, Hualong Liu, Archit Bhatnagar, Ang Chen, and Wencong Su. 2026. Grid
     An Optimization Perspective. Annual Review of Control, Robotics, and Autonomous               Integration of AI Data Centers: A Critical Review of Energy Storage Solutions.
     Systems 2 (2019), 115–140.                                                                    arXiv:2603.00415 [eess.SY] https://arxiv.org/abs/2603.00415
 [8] Alberto Bemporad, Manfred Morari, Vivek Dua, and Efstratios N. Pistikopoulos.            [31] North American Electric Reliability Corporation. 2025. Incident Review: Consid-
     2002. The explicit linear quadratic regulator for constrained systems. Automatica             ering Simultaneous Voltage-Sensitive Load Reductions. Technical Report. North
     38, 1 (Jan. 2002), 3–20. doi:10.1016/S0005-1098(01)00174-1                                    American Electric Reliability Corporation. https://www.nerc.com/globalassets/
 [9] Albert Benveniste, Benoît Caillaud, Dejan Nickovic, Roberto Passerone, Jean-                  our-work/reports/event-reports/incident_review_large_load_loss.pdf
     Baptiste Raclet, Philipp Reinkemeier, Alberto Sangiovanni-Vincentelli, Werner            [32] Pierluigi Nuzzo, Huan Xu, Necmiye Ozay, John B. Finn, Alberto L. Sangiovanni-
     Damm, Thomas A. Henzinger, and Kim G. Larsen. 2018. Contracts for System                      Vincentelli, Richard M. Murray, Alexandre Donzé, and Sanjit A. Seshia. 2014. A
     Design. Foundations and Trends in Electronic Design Automation 12, 2–3 (2018),                Contract-Based Methodology for Aircraft Electric Power System Design. IEEE
     124–400.                                                                                      Access 2 (2014), 1–25.
[10] Yuxiao Chen, James Anderson, Karan Kalsi, Aaron D. Ames, and Steven H. Low.              [33] Vasumathi Raman, Alexandre Donzé, Mehdi Maasoumy, Richard M. Murray,
     2019. Compositional Set Invariance in Network Systems with Assume-Guarantee                   Alberto Sangiovanni-Vincentelli, and Sanjit A. Seshia. 2014. Model Predictive
     Contracts. In American Control Conference (ACC). 1027–1034.                                   Control with Signal Temporal Logic Specifications. In 53rd IEEE Conference on
[11] John W Chinneck and Erik W Dravnieks. 1991. Locating minimal infeasible                       Decision and Control (CDC). 81–87. doi:10.1109/CDC.2014.7039363
     constraint sets in linear programs. ORSA Journal on Computing 3, 2 (1991),               [34] Vasumathi Raman, Alexandre Donzé, Dorsa Sadigh, Richard M. Murray, and
     157–168.                                                                                      Sanjit A. Seshia. 2015. Reactive Synthesis from Signal Temporal Logic Specifi-
[12] Esha Choukse, Brijesh Warrier, Scot Heath, et al. 2025. Power Stabilization for               cations. In Proceedings of the 18th International Conference on Hybrid Systems:
     AI Training Datacenters. arXiv:2508.14318.                                                    Computation and Control (HSCC). 239–248. doi:10.1145/2728606.2728628
[13] Hantao Cui, Fangxing Li, and Kevin Tomsovic. 2021. Hybrid Symbolic-Numeric               [35] Nicolas Rouquette, Inigo Incer, and Alessandro Pinto. 2023. Early Design Ex-
     Framework for Power System Modeling and Analysis. IEEE Transactions on                        ploration of Space System Scenarios Using Assume-Guarantee Contracts. In
     Power Systems 36, 2 (2021), 1373–1384. doi:10.1109/TPWRS.2020.3017019
                                                                                         11
                                                                                                                                                                       Wang et al.


     2023 IEEE International Conference on Space Mission Challenges for Informa-              [46] Hao Zhu and Hao Jan Liu. 2016. Fast Local Voltage Control Under Limited
     tion Technology (SMC-IT). IEEE, Pasadena, CA, USA, 15–24. doi:10.1109/SMC-                    Reactive Power: Optimality and Stability Analysis. IEEE Transactions on Power
     IT56444.2023.00011                                                                            Systems 31, 5 (2016), 3794–3803. doi:10.1109/TPWRS.2015.2504419
[36] Mohamed Shamseldein. 2025.          From Liability to Asset: A Three-Mode
     Grid-Forming Control Framework for Centralized Data Center UPS Systems.
     arXiv:2512.16497.                                                                        A      The Encoding Procedure
[37] Marina Tsili and Stavros Papathanassiou. 2009. A Review of Grid Code Technical
     Requirements for Wind Farms. IET Renewable Power Generation 3, 3 (2009),
                                                                                              Algorithm 1 lists the full encoding procedure of §3.3. It constructs
     308–332.                                                                                 the worst-case trace from the specification’s assume block, resolves
[38] Deepthi Vaidhynathan, Kumaraguru Prabakar, Gregory Martin, Anand Ramesh,                 the event times, instantiates the declared variables and the guaran-
     Ben Wheeler, Christopher Coco, Jimmy Clidaras, Matthieu Monsch, Sangsun Kim,
     Saurav Talukdar, and Shilpa Marti. 2025. Vulcan Test Platform: Demonstrating             tee clauses, binds the plant outputs, and calls the synthesis query (2).
     the Data Center as a Flexible Grid Asset. Renewable Energy (2025).
[39] Di Wang, Sriram Govindan, Anand Sivasubramaniam, Aman Kansal, Jie Liu, and
     Badriddine Khessib. 2014. Underprovisioning backup power infrastructure for              Algorithm 1 Encoding a specification to a synthesis query.
     datacenters. In Proceedings of the 19th international conference on Architectural          1: function Encode(𝑠𝑝𝑒𝑐 , plant, workload 𝑤𝑐𝑜𝑚𝑝 )
     support for programming languages and operating systems. ACM, Salt Lake City
                                                                                                2:    if 𝑠𝑝𝑒𝑐.assume declares envelope { (𝑣𝑘 , 𝑑𝑘 ) }𝑘=1
                                                                                                                                                     𝑛 then
     Utah USA, 177–192. doi:10.1145/2541940.2541966
[40] Lizhi Wang, Fei Feng, Ella Chou, and Yashen Lin. 2026. Resilient Energy-                   3:        𝑣𝑔′ (𝑡 ) ← min{ 𝑣𝑘 : 𝑑𝑘 ≥ 𝑡 }                                  ⊲ Eq. (7)
     Based Control for DC Data Centers under Grid and Load Disturbances.                        4:    else
     arXiv:2605.21691.                                                                          5:        𝑣𝑔′ ← 𝑠𝑝𝑒𝑐.assume                    ⊲ already a piecewise lower bound
[41] Adam Wierman, Zhenhua Liu, Iris Liu, and Hamed Mohsenian-Rad. 2014. Op-                    6:    𝑡 𝑓 ← min{ 𝑡 : 𝑣𝑔′ (𝑡 ) < 0.9 }
     portunities and challenges for data center demand response. In International               7:    𝑡𝑟 ← min{ 𝑡 > 𝑡 𝑓 : 𝑣𝑔′ (𝑡 ) ≥ 0.9 }                   ⊲ event times from 𝑣𝑔′
     Green Computing Conference. 1–10. doi:10.1109/IGCC.2014.7039172                            8:    𝑤 ← (𝑣𝑔′ , 𝑤𝑐𝑜𝑚𝑝 )                                      ⊲ disturbance inputs
[42] Yiheng Xie, Wenqi Cui, and Adam Wierman. 2026. Enhancing Data Center Low-
     Voltage Ride-Through. In Proceedings of the 17th ACM International Conference              9:    (𝑣𝑖 , 𝑝 ) ← plant (𝑢, 𝑤 )            ⊲ the plant model mapping 𝑦 = 𝑔(𝑢, 𝑤 )
     on Future and Sustainable Energy Systems (e-Energy). arXiv:2510.03867.
[43] Zhe Xu, A. Agung Julius, and Joe H. Chow. 2017. Optimal Energy Storage Control           10:     𝑣𝑎𝑙𝑠 ← ∅
     for Frequency Regulation under Temporal Logic Specifications. In American                11:     for all binding 𝑏 ∈ 𝑠𝑝𝑒𝑐.var do                         ⊲ instantiate binding
     Control Conference (ACC). 1874–1879.                                                     12:         𝑣𝑎𝑙𝑠 ← 𝑣𝑎𝑙𝑠 ∪ { 𝑏 [ 𝑡 𝑓 , 𝑡𝑟 , 𝑤 ] }          ⊲ e.g. 𝑝𝑝𝑟𝑒 = 𝑤𝑐𝑜𝑚𝑝 (𝑡 𝑓 )
[44] Zhe Xu, A. Agung Julius, and Joe H. Chow. 2019. Energy Storage Controller                13:     𝜑←∅
     Synthesis for Power Systems with Temporal Logic Specifications. IEEE Systems             14:     for all clause 𝑐 ∈ 𝑠𝑝𝑒𝑐.guarantee do                     ⊲ instantiate clause
     Journal 13, 1 (2019), 748–759.                                                           15:        𝜑 ← 𝜑 ∪ { 𝑐 [ 𝑡 𝑓 , 𝑡𝑟 , 𝑣𝑎𝑙𝑠 ] }
[45] Yichen Zhang, Mohammed Olama, Alexander Melin, Yaosuo Xue, Seddik Djouadi,
     and Kevin Tomsovic. 2019. Synthesizing Distributed Energy Resources in Mi-               16:     𝐾 ← { 𝑢 : 𝑃2 + 𝑄2 ≤ 𝑆2 }                ⊲ apparent-power cap, 𝑆 from plant
     crogrids with Temporal Logic Specifications. In IEEE Innovative Smart Grid               17:     return Synthesize( (𝑣𝑖 , 𝑝 ), 𝜑, 𝐾, 𝑤 )                          ⊲ solve (2)
     Technologies (ISGT). 1–5.




                                                                                         12
