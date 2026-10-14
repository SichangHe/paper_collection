                                         JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                        i




                                              S AN DRA: Safe Large-Language-Model-Based
                                              Decision Making for Automated Vehicles Using
                                                         Reachability Analysis
                                                                                  Yuanfei Lin∗ , Sebastian Illing∗ , and Matthias Althoff



                                            Abstract—Large language models (LLMs) have been widely
                                         applied to knowledge-driven decision-making for automated vehi-                                                               Prompt
                                         cles due to their strong generalization and reasoning capabilities.                                                         You are currently driving in an T-
                                                                                                                              Environment
                                         However, the safety of the resulting decisions cannot be ensured                                                            intersection scenario under rainy
                                         due to possible hallucinations and the lack of integrated vehicle                                                           conditions. There is no adjacent
                                                                                                                                                                     lane. Your velocity is 5m/s ...
                                         dynamics. To address this issue, we propose S AN DRA, the first
                                         safe large-language-model-based decision making framework for
                                                                                                                                                                                          LLM
                                         automated vehicles using reachability analysis. Our approach
                                         starts with a comprehensive description of the driving scenario                                                                         KEEP, FOLLOW- LANE
                                         to prompt LLMs to generate and rank feasible driving actions.
arXiv:2510.06717v2 [cs.RO] 11 Jul 2026




                                                                                                                                                                                 STOP, FOLLOW- LANE
                                         These actions are translated into temporal logic formulas that                                                                                    ...
                                                                                                                                            FOLLOW- LANE
                                         incorporate formalized traffic rules, and are subsequently in-
                                                                                                                                                 STOP                            Reachability analysis
                                         tegrated into reachability analysis to eliminate unsafe actions.
                                         We validate our approach in both open-loop and closed-loop                        Fig. 1: An example usage of S AN DRA, where the LLM is prompted to
                                         driving environments using off-the-shelf and finetuned LLMs,                      generate a ranked list of longitudinal and lateral action pairs ordered from
                                         showing that it can provide provably safe and, where possible,                    best to worst. The action pair corresponding to stopping while staying on the
                                         legally compliant driving actions, even under high-density traffic                current lane is verified as safe using reachability analysis and then executed.
                                         conditions. To ensure transparency and facilitate future research,
                                         all code and experimental setups are publicly available at
                                         github.com/CommonRoad/SanDRA.                                                     mated vehicles.
                                            Index Terms—Formal methods, autonomous driving, methods                              a) LLMs as Decision Makers: LLMs are trained on vast
                                         for safety, large language models, decision making, formalization                 and diverse internet-scale data, enabling them to understand
                                         of traffic rules.                                                                 common driving logs and reason about traffic scenarios [3],
                                                                                                                           [4]. For this reason, they have been applied to automated
                                                                 I. I NTRODUCTION                                          driving to generate software programs, high-level actions,

                                         D      ECISION-making is essential for automated vehicles
                                                to navigate safely and interact appropriately with other
                                         traffic participants. Traditional methods rely on finite state ma-
                                                                                                                           waypoints, and control signals; an overview is shown in Tab. I.
                                                                                                                           The majority of these approaches employ LLMs to choose
                                                                                                                           suitable driving actions given sensor inputs and/or narrative
                                         chines for simple scenarios [1, Sec. II-B] and neural networks                    descriptions of the driving context. However, the safety of
                                         to handle more complex behaviors like lane changes [2]. Re-                       the selected actions is typically unverified or delegated to
                                         cent efforts have shifted toward a knowledge-driven paradigm                      hardcoded rules [5], [6], another LLM [7]–[9], or software
                                         with the emergence of large language models (LLMs) that                           modules evaluating criticality measures [10]–[12]. Despite
                                         enable human-like and context-sensitive decision-making [3],                      being instructed to generate safe actions, LLMs often fail to
                                         [4]. However, their limited understanding of underlying physi-                    fully capture critical scenario information and may hallucinate,
                                         cal models, tendency to hallucinate, and implicit consideration                   leading to frequent rule violations and collisions [7], [12],
                                         of traffic rules pose critical safety concerns that are unaccept-                 [13]. A similar fragility arises from their limited understanding
                                         able for real-world deployment. To address this, we propose                       of vehicle dynamics when directly generating waypoints to
                                         using reachability analysis to verify the safety of decisions                     be followed, resulting in kinematically infeasible trajectories
                                         generated by LLMs before their execution (cf. Fig. 1).                            [14]–[16]. In contrast, another category of work employs
                                                                                                                           LLMs to adjust key components of the software stack without
                                         A. Related Work                                                                   altering its overall structure [17]–[19], allowing existing safety
                                           Below, we concisely review related works on LLM-based                           mechanisms to remain effective. However, these approaches
                                         decision-making and safety verification approaches for auto-                      still utilize only a limited portion of the full potential of LLMs
                                              ∗ The first two authors have contributed equally to this work.
                                                                                                                           and lack formal guarantees of correctness.
                                               Manuscript received Month Date, Year; revised Month Date, Year.                   b) Safety Verification: Formal verification is the process
                                               The authors are with the Department of Computer Engineering,                of verifying whether system executions comply with a formal
                                         Technical University of Munich, 85748 Garching, Germany. Matthias Al-             specification. For a review on verifying motion plans for
                                         thoff is also with the Munich Center for Machine Learning (MCML),
                                         80538 Munich, Germany. {yuanfei.lin, sebastian.illing,                            automated vehicles, we refer to [26]. Among the various
                                         althoff}@tum.de (Corresponding author: Yuanfei Lin.)                              techniques, such as backup control barrier functions [27],
                                         ©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
                                         reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                         reuse of any copyrighted component of this work in other works.
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                ii



TABLE I: Related work on LLMs as decision makers and their support for          Obstacles        Future movement          Initial state          Lanelet
safety-verified decision outputs.

                                                     Safety   Formally
 Work          Output
                                                     check    correct
  [5]–[10]     High-level actions                      ✓         ✗                                                                        Lane Ladj l
                                                                            d
  [11]–[13]    High-level actions                      ✗         ✗
  [14], [15]   High-level actions & waypoints          ✗         ✗                 s                                                      Lane Lcur
  [18], [19]   High-level actions & controller pa-     ✓         ✗
               rameters
  [16]         Waypoints                               ✗         ✗       Fig. 2: Exemplary road network with lanes defined by lanelets. The ego vehicle
  [17], [20]   Programs                                ✓         ✗       is currently following lane Lcur , as determined by the high-level routing
  [21], [22]   Control signals                         ✗         ✗       module to reach the goal. Alternatively, it may switch to the left-adjacent
  [23], [24]   Traffic descriptions                    ✗         ✗       lane Ladj l instead of remaining on Lcur .
  [25]         Traffic descriptions & waypoints        ✗         ✗
 Ours          High-level actions & trajectories       ✓         ✓
                                                                         Sec. III details the proposed framework for safe LLM-based
                                                                         decision making. In Sec. IV, we demonstrate the advantages
gatekeeper [28], and shielding [29], reachability analysis is            of our approach. Finally, Sec. V concludes the article.
the most widely used approach for online safety verification
of automated vehicles [30]–[33]. The specification is typically                                    II. P RELIMINARIES
expressed as a temporal logic formula, such as linear temporal           A. General Setup
logic (LTL) or metric temporal logic (MTL), encompassing
                                                                            The vehicle for which the decision-making is performed is
safety specifications [34], [35], formalized traffic rules [36]–
                                                                         referred to as the ego vehicle. We use the index k ∈ N0 to
[38], and driving actions [39]–[41]. These formulas can be
                                                                         denote the discrete time step corresponding to the continuous
integrated into the software stack of automated vehicles to
                                                                         time tk = k∆t, where ∆t ∈ R+ is a fixed time increment.
generate specification-compliant trajectories, monitor traffic
                                                                         The dynamics of the ego vehicle is modeled as:
rule compliance, and repair trajectories that violate these speci-
fications [33], [42], [43]. Specifically, by coupling reachability                                 xk+1 = f (xk , uk ),                                 (1)
analysis with model checking, one can obtain driving corridors
for automated vehicles that satisfy the given formulas [44],             where xk ∈ Xk is the state within the permissible state
[45]. If the reachable set defining these corridors becomes              space Xk ∈ Rnx , and uk ∈ Uk is the control input within
empty within the planning horizon, a specification-compliant             the admissible input space Uk ∈ Rnu . Without loss of
action no longer exists. In addition, verification techniques can        generality, we set the current time step to 0 and denote the
be integrated into deep learning-based frameworks as safety              decision-making horizon by h. The solution of (1) at time
layers, such as reinforcement learning [2], [46], [47]. However,         step k is denoted as χk (x0 , u[0,k] ), where u[0,k] is the input
to the best of our knowledge, no such integration exists yet             trajectory. The solution over the time interval [0, k] is denoted
for an LLM-based decision-making framework.                              by χ[0,k] (x0 , u[0,k] ). The operator occ(·) returns the spatial
                                                                         occupancy of the entity.
B. Contributions                                                            As shown in Fig. 2, we describe the road network as a set of
                                                                         lanelets li , i ∈ N+ , each defined by left and right boundaries
   In this work, we present S AN DRA, the first framework for
                                                                         represented as polylines [48]. We then define a lane Lj as
integrating LLMs safely into decision making for automated
                                                                         a set of connected lanelet sections. A lane Lj is adjacent to
vehicles through reachability analysis, combining the strengths
                                                                         another lane Lj ′ if there exists a lanelet in Lj whose border
of machine learning and formal methods. In particular, our
                                                                         fully overlaps with the border of a lanelet in Lj ′ . We denote
contributions are:
                                                                         the lane currently occupied by the ego vehicle as Lcur , with
   1) designing a lightweight prompt that guides LLMs to
                                                                         Ladj l and Ladj r referring to its left and right adjacent lanes,
       generate and prioritize driving action candidates;
                                                                         respectively. Using the centerline of Lcur , we can construct a
   2) mapping driving actions to LTL formulas and using them
                                                                         curvilinear coordinate system in which vehicles are described
       to label human trajectories for LLM finetuning;
                                                                         by their longitudinal position s and lateral deviation d [49]
   3) combining reachability analysis with the LTL formulas
                                                                         (cf. Fig. 2). In addition, we denote the relative longitudinal
       of action candidates, along with formalized traffic rules,
                                                                         distance, orientation, velocity, steering angle, and acceleration
       to verify their safety. The computed reachable sets can
                                                                         as ∆s, θ, v, δ, and a, respectively.
       be used as constraints for the downstream trajectory
       planning module; and
   4) evaluating safety performance in both open- and closed-            B. Specification-Compliant Reachability Analysis
       loop simulations, with the closed-loop setup incorpo-                Since decision making typically focuses on short-term driv-
       rating both most-likely and set-based predictions of              ing behaviors, we employ reachability analysis over a finite
       surrounding traffic participants.                                 time horizon and formalize driving actions as formulas in
   The remainder of this article is structured as follows:               LTL over finite traces (LTLf ) [50]. In this setting, temporal
Sec. II describes the general setup and necessary preliminaries.         operators are interpreted over finite traces bounded by the
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                      iii




                                                  Prompt                            LLM

      Weather       Route                          <System>              Longitudinal      Lateral

                                  Describer       <Ego vehicle>
    Personalized    Lanes
     preference                                                                                           Reachable sets
                                                  <Obstacles>                        ...                                              Safe actions

                                                                                Action to LTLf              Reachability              Motion planner
                   Driving                                                                                    analysis
     Obstacles      laws                                Formalized               Rule to LTLf                                        Fail-safe planner
                                                        traffic rules
Fig. 3: S AN DRA overview diagram. Our tool S AN DRA takes planning and environmental information as inputs and processes them to generate a structured
description of the current scenario. The description is then used to prompt the LLM to produce a ranked sequence of longitudinal and lateral action pairs,
ordered from best to worst. After converting the actions and traffic rules to LTLf formulas, we take their conjunction and apply reachability analysis to verify
the safety of the resulting behavior. Once verified, the action pair is either executed directly or its corresponding reachable sets are passed to the motion
planner to generate safe trajectories. If no verified actions are available, a fail-safe plan is executed.



decision-making horizon h. To ensure safety over an infinite                       C. Problem Formulation
time horizon, fail-safe planning is required [33, Sec. X].                            This article addresses two key challenges: designing
   1) Linear Temporal Logic over Finite Traces: Given a set                        lightweight scenario representations for prompting LLMs for
of atomic propositions AP and formulas φ, φ1 , and φ2 , the                        decision making of automated vehicles, and bridging their
syntax of LTLf is defined according to the grammar [50,                            natural language outputs with safety verification techniques.
Sec. 2]:                                                                           For the latter, we focus on translating language to LTLf
                                                                                   formulas φ; we additionally verify the legal safety1 of each
                 φ ::= σ | ¬φ | φ1 ∧ φ2 | Gφ | Fφ,                        (2)
                                                                                   candidate action by ensuring that its corresponding reachable
                                                                                   set for the ego vehicle remains non-empty throughout the
where σ ∈ AP is an atomic proposition, and the symbols ¬                           decision-making horizon h, i.e.,
and ∧ denote Boolean negation and conjunction connectives,
respectively. The temporal operator Gφ requires that φ will                                           ∀k ∈ {0, . . . , h} : Rk (φ) ̸= ∅.
always hold over the finite trace, whereas Fφ requires that φ
                                                                                   We emphasize that the degree of safety guarantee depends on
eventually holds within the finite trace. Further logic operators
                                                                                   the accuracy of predictions for other traffic participants. If an
can be derived from (2) (see [51, Sec. 5.1.1]), such as
                                                                                   inaccurate prediction leads to a safety-critical situation, we
φ1 ∨ φ2 := ¬(¬φ1 ∧ ¬φ2 ) (disjunction) and φ1 → φ2 :=
                                                                                   apply the safety concept described in [33, Sec. X].
¬φ1 ∨ φ2 (implication). If a finite trace χ[0,k] (x0 , u[0,k] )
satisfies the specification φ, we write χ[0,k] (x0 , u[0,k] ) |= φ.
For formalized driving actions and traffic rules, each atomic                                                   III. S AN DRA
proposition is typically associated with a predicate, defined as                     This section first introduces the overall algorithm of S AN -
a function of vehicle states.                                                      DRA in Sec. III-A, followed by detailed explanations of its
   2) Specification-Compliant Reachable Sets: We assume                            key components in Secs. III-B-III-E.
that the predicted time-varying occupancies of all obstacles
are given as Ok ⊂ R2 at each time step k. Based on this,                           A. Overall Algorithm
we define the set of forbidden states of the ego vehicle as                           As shown in Fig. 3, at each decision-making cycle, S AN -
XkF = {xk ∈ Xk | occ(xk ) ∩ Ok ̸= ∅}. The specification-                           DRA takes as input both environmental and planning data,
compliant reachable set of the ego vehicle Rek at time step k                      including high-level routes from navigation systems, drivable
is defined as the set of states reachable from an initial state                    lanes, detected obstacles, and other contextual information
in X0 , while avoiding the forbidden states XτF for every step                     such as traffic rules [53] and weather conditions.2 To enable
τ ∈ {0, . . . , k}, via a drivable trajectory that satisfies φ.                    personalization, different driving styles can be incorporated
Formally, we have [45, Sec. II-C]:                                                 through predefined driving preferences [12] or verbal com-
                                                                                  mands from humans [20]. All input data are automatically
 Rek (φ) := χk (x0 ,u[0,k] ) ∃x0 ∈ X0 , ∀τ ∈ {0, . . . , k},                       converted into a narrative description within S AN DRA. This
                                                                                   is achieved by first mapping each input type to predefined
                                                       / XkF ∧
                         ∃uτ ∈ Uτ : χτ (x0 , u[0,τ ] ) ∈         (3)               semantic categories, e.g., vehicle state, user command, traffic
                                                                                  rules, second instantiating template sentences for each cate-
                                    χ[0,k] (x0 , u[0,k] ) |= φ .                   gory, and finally assembling these sentences into a coherent
                                                                                   story that preserves temporal and spatial relationships. The
Obtaining Rek (φ) is generally infeasible [52]. Therefore, we                          1 We define legal safety as the property that the ego vehicle cannot cause
use a tight overapproximation Rk (φ) ⊇ Rek (φ) that encloses                       any traffic rule violations [33].
all safe and specification-compliant states [30], [45].                                2 https://openweathermap.org/api
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                          iv



resulting narrative is used to prompt the LLM, which performs
reasoning and generates a sequential ordering of κ ∈ N+                  <System>: You are driving a car and need to make a
                                                                         high-level driving decision. [User command] . First, care-
feasible longitudinal and lateral action pairs (cf. Tab. II and          fully observe the environment; then, reason through your
Sec. III-B). Although the actions are presented separately               decision step by step and present it in natural lan-
for clarity, they are in fact considered jointly to generalize           guage, and finally, return the top [κ] advisable lon-
across diverse road structures, unlike the other approaches              gitudinal–lateral action pairs ranked from best to worst.
for generating driving decisions listed in Tab. I. Note that to           {Feasible longitudinal actions} . {Feasible lateral actions} .
                                                                         The past action pairs are {previous actions} .
obtain a comprehensive representation of the scenario, other
sensor modalities can also be tokenized as vision tokens [54]
                                                                         <Ego vehicle>: You are currently driving in a {road type}
and be combined with textual tokens from the narrative in                scenario with {weather condition} . (There is a {left / right} -
a shared embedding space, enabling the use of multi-modal                adjacent lane with the {same / opposite} direction. There are
LLMs [12]. Afterwards, the returned action pairs are converted           incoming lanes on the {left / right} .) Your velocity is {v} ,
into LTLf formulas (cf. Sec. III-C), which are then conjuncted           your orientation is {θ} , your steering angle is {δ} , and your
with the formalized traffic rules for legal safety (cf. Sec. III-D).     acceleration is {a} .
With this, the safety verification is carried out through the
                                                                         <Obstacles>: Here is an overview of all relevant obstacles
computation of reachable sets that satisfy the formulas (cf.             surrounding you:
Sec. III-E). The first verified action pair can be executed by            {Obstacle 1: {Lane information}. {State}. {(Criticality)}.} .
the controller, or its corresponding reachable sets can be used           {Obstacle 2: {Lane information}. {State}. {(Criticality)}.} .
as a constraint by various trajectory planners to generate safe          ...
trajectories [33, Sec. VIII]. When the connection to the cloud         Fig. 4: LLM prompt design. Automatically generated content in the prompt
is lost or other failures occur that cause the LLM to fail to          is marked with {curly brackets} , while manual inputs are in [square
respond in time, produce hallucinations, or when no feasible            brackets] , and (round brackets) denote optional elements depending on
                                                                       the road structure and its regulatory features.
verified action is available, we revert to a fail-safe trajectory
to guarantee safety [33, Sec. X] (cf. Sec. III-E).
                                                                       angle, and acceleration. A snippet of the ego vehicle prompt
                                                                       is shown in Fig. 1.
B. Prompt Design and LLM Querying                                         3) Obstacle Prompt: This prompt block describes the sur-
   We construct a describer module that converts driving               rounding traffic participants in the scenario, including their
context information into template-based descriptive text, struc-       IDs, types, and states. These obstacles are identified either
tured into three key components, with full details provided in         through lane-based adjacency or using Lidar-like beams rela-
Fig. 4; the latter two form the user prompt. In addition to            tive to the ego vehicle [56, Fig. 2]. In addition, the descrip-
the automatically converted content, minimal manual inputs             tion is enriched with criticality measures [57], e.g., time-to-
specify driving styles, hyperparameters, and regulation-related        collision, to quantify the threat level posed by the obstacles
aspects. The modular design of the prompt enables easy                 to the ego vehicle. For instance, for dynamic vehicles at
adaptation and extension. Note that all directional aspects,           interstates, we use the following prompt:
such as {left / right} lanes or {same / opposite} directions,
                                                                         Car {id} : it is driving on your {same / left adjacent / right
are derived from the topological relations of the road network            adjacent} lane in the {same / opposite} direction and is
(cf. Fig. 6).                                                             {∆s in front of / behind} you. Its velocity is {v} , its orien-
   1) System Prompt: In the system prompt, we introduce                  tation is {θ} , its steering angle is {δ} , and its acceleration
the decision-making task for LLMs, which may also include                is {a} . (The time-to-collision is {time-to-collision} .)
personalized commands, e.g., “drive faster”. The LLM is                    The prompt is fed into the LLM, which can be either an
guided to generate longitudinal and lateral action pairs ranked        off-the-shelf model or a model finetuned on recorded driving
from best to worst by prompting it to decide in a chain-of-            datasets. To enhance reliability and facilitate parsing, we define
thought manner [55]. Specifically, we prefilter and provide            the desired output as a schema, i.e., a sequence of longitudinal-
the feasible actions based on current lane information, gen-           lateral action pairs, and guide the LLM to produce actions
eralizing the approaches from [5], [7], [12]. The longitudinal         in a format that conforms to this schema.3 Moreover, for
actions are determined by whether the maneuvers are allowed            finetuning, we use recorded driving datasets and automatically
in the current driving context, whereas the lateral actions            label each scenario, using the prompt design in Fig. 4 as input
are obtained by querying the lane structure at the current             and the action pair of a randomly selected vehicle – labeled
position of the ego vehicle (cf. Fig. 2). For instance, in Fig. 1,     according to the LTLf formula shown in Tab. II – as output.
all longitudinal actions are contextually allowed, since the           When κ > 1 action pairs are required, the labeled action pair
scenario is set in a rural environment; however, as the occupied       is used as the top-1 option, and the remaining positions are
lane of the ego vehicle has no adjacent lanes, the only feasible       filled with other feasible action pairs chosen at random. The
lateral action is FOLLOW- LANE.                                        LLM is finetuned based on the collected input-output pairs to
   2) Ego Vehicle Prompt: This section provides dynamic                adapt it for our decision-making tasks [58].
information about the ego vehicle, including environmental
context and road network configurations. It also covers the
current vehicle state, including velocity, orientation, steering           3 https://openai.com/index/introducing-structured-outputs-in-the-api/
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                    v



TABLE II: High-level action space for the ego vehicle and the corresponding   D. Formalized Traffic Rules
LTLf formula.
                                                                                 Traffic rules cover both general regulations (indexed by
 Action                Direction                LTLf formula                  R G) [37, Sec. III-A] and rules for specific use cases or road
 K EEP                                          G(|a| ≤ alim )                types, such as interstate [37, Sec. III-B] and intersection [38].
 ACCELERATE
                       Longitudinal action
                                                G(a > alim )                  Because embedding traffic rules into prompts may lead to
 D ECELERATE                                    G(a < −alim )                ambiguous interpretations and relies on the LLM to reason
 S TOP                                          FG in standstill(x)
                                                                             implicitly, we explicitly incorporate them into the verifica-
 F OLLOW- LANE                                  G in lane(x, Lcur ) 
 L EFT- LANE           Lateral action           FG in lane(x, Ladj l ) 
                                                                              tion process to ensure legal safety. To achieve this, each
 R IGHT- LANE                                   FG in lane(x, Ladj r )        action specification φ1 , φ2 , . . . , φκ is individually augmented
                                                                              by conjoining it with these formalized rules expressed in
                                                                              LTLf [36], which are themselves conjuncted. When these rules
                                                                              are formalized in other temporal logics, such as MTL [37],
C. Action to LTLf                                                             [38], they can be rewritten in LTLf using conversion tools,
                                                                              e.g., Spot [59].
   We incorporate string representations of actions into reach-
                                                                              Running Example: Let us extend the running example by
ability analysis by converting them to LTLf formulas. To the
                                                                              additionally considering the German Road Traffic Regulation
best of our knowledge, such a conversion of driving actions
                                                                              (StVO), where we select the safe distance rule R G1 as an
has not yet been presented in the literature. Analogous to
                                                                              example [37, Sec. III-A] (translated from German):
the traffic rule formalization in [37], [38], we propose a
two-step process: first, concretizing the string descriptions,                     The distance to a vehicle ahead must generally be
and second, formalizing them using logic. For instance, the                        large enough that one can stop safely even if that
action STOP can be concretized as “the ego vehicle eventually                      vehicle brakes suddenly. [...] (§ 4(1) StVO).
maintaining a velocity close to zero within the decision-making               Given the reaction time td of the ego vehicle, the large enough
horizon”, where the closeness to zero is quantified by the                    safe distance is defined as [37, Sec. IV-C]:
measurement uncertainty verr ∈ R0 . Afterward, we extract                                                       2
                                                                                                               vobs         v2
and specify predicates in higher-order logic based on the con-                         dsafe (v, vobs ) =                −          + vtd ,                (5)
                                                                                                            −2|aobs,min | −2|amin |
cretization, reusing existing ones from the formalized traffic
rules [37], [38] where applicable. With this, the action STOP                where vobs denotes the velocity of the obstacle obs, and amin
is formalized as FG in standstill(x) , where the predicate                    and aobs,min represent the minimum accelerations of the ego
in standstill(x) ↔ −verr ≤ v ≤ verr indicates whether the                     and leading vehicles, respectively, with aobs,min < amin < 0.
ego vehicle is in standstill [38, Sec. IV-B].                                 The concretized safe distance rule can be formalized in LTLf
                                                                              as [33, (2)]:4
   As summarized in Tab. II, we formalize the most commonly
used longitudinal and lateral actions based on their temporal                    φR G1 = G precedes(xobs , x) →
                                                                                                                                                           (6)
and spatial concretizations, which can be easily extended to
                                                                                                                                           
                                                                                                              keeps safe distance(x, xobs ) ,
additional action definitions. The longitudinal actions KEEP,
ACCELERATE , and DECELERATE are interpreted as confining
                                                                              where the meaning of the predicate precedes(xobs , x) is self-
the acceleration of the ego vehicle to a certain range and                    explanatory, and keeps safe distance(x, xobs ) holds if and
are distinguished based on a predefined acceleration threshold                only if the relative longitudinal distance ∆s between the ego
alim ∈ R0 . In contrast, lateral     actions are based on the predi-          vehicle and the preceding vehicle obs exceeds the threshold
                           W
cate in lane(x, Lj ) ↔ li ∈Lj in lanelet(x, li ) that specifies               dsafe (cf. (5)):
whether the ego vehicle is occupying a particular lane Lj ,                        keeps safe distance(x, xobs ) ↔ ∆s > dsafe (v, vobs ).
determined by checking its associated lanelets (cf. Fig. 2),
with in lanelet(x, li ) ↔ occ(x) ∩ occ(li ) ̸= ∅ [44, Sec. V].
                                                                              E. Safety Verification
The action FOLLOW- LANE is interpreted as the ego vehicle
staying in the currently occupied lane Lcur . We concretize                      The online safety verification relies on dynamic models
the lane change actions LEFT- LANE and RIGHT- LANE as the                     that predict the future behaviors of both the ego vehicle
ego vehicle eventually remaining in the corresponding adjacent                and other traffic participants, capturing legally feasible future
lane Ladj l or Ladj r within the decision-making horizon; thus,               evolutions of the scenario while accounting for measurement
FG is used as the outermost temporal operator. By translating                 and modeling uncertainties [30]. For the behavior of other
the LLM action pairs into LTLf formulas, we obtain a sequence                 vehicles, we use their most likely trajectories [60] to prune
of specifications φ1 , φ2 , . . . , φκ through the conjunction of the         traffic-rule-violating solution spaces [44], [45], while set-
longitudinal and lateral actions.                                             based predictions define the forbidden states XkF to ensure
                                                                              safety during decision-making (cf. (3)) [61]. Examples of
Running Example: The LTLf formula corresponding to the                        both types of predictions are illustrated in Fig. 5a. These
action pair ACCELERATE and FOLLOW- LANE is formalized as                      predictions serve complementary purposes: the most likely

                                                                                   4 For simplicity, the case without a prior cut-in is omitted. Details of the
                                                        
          φacc foll = G(a > alim ) ∧ G in lane(x, Lcur ) .             (4)    rule formalization process can be found in [33, Sec. IV].
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                 vi



    Initial state        Obstacle      Most likely pred.         Set-based pred.                 TABLE III: General parameters for the evaluations.
        Reach. set with φacc foll            Reach. set with φacc foll ∧ φR G1     Description                                    Notation and value
                                                                                   Threshold                                      alim = 0.2m/s2 ; verr = 0.1m/s
                                                                                                                                  longitudinal acceleration: [−6, 6]m/s2 ;
                                                                                   Reachability analysis                          lateral acceleration: [−4, 4]m/s2 ;
                                                                                                                                  maximum velocity: 30m/s
                    (a) Most likely and set-based predictions.
                                                                                   Set-based prediction                           maximum acceleration: 12m/s2
                                                                                   Safe distance dsafe                            td = 0.4s; amin = −6m/s2 ; aobs,min = −1
                                                                                     Dataset evaluation
                                                                                   Temporal setting                               ∆t = 0.04s
                                                                                   Longitudinal: 0.0% STOP, 55.8% KEEP,
                        (b) Reachable set at time step k.
                                                                                   21.4% ACCELERATE, 22.8% DECELERATE
Fig. 5: Prediction of other traffic participants and reachable set of the ego      Lateral: 98.7% FOLLOW- LANE,
vehicle. The specifications φacc foll and φR G1 are given in (4) and (6),          0.9% LEFT- LANE, 0.4% RIGHT- LANE
respectively.                                                                      Longitudinal: 0.0% STOP, 62.1% KEEP,
                                                                                   24.3% ACCELERATE, 13.6% DECELERATE
                                                                                   Lateral: 98.4% FOLLOW- LANE,
trajectories primarily capture interactions with other traffic                     1.0% LEFT- LANE, 0.6% RIGHT- LANE
participants, while the set-based predictions are required to                        Highway-env simulation
ensure safety. However, other prediction strategies that provide                   Action mapping (highway-env vs. our approach)
either multiple trajectory hypotheses or safety-guaranteeing                        LANE LEFT                                  LEFT- LANE, KEEP/ DECELERATE/ ACCELERA
occupancy representations, i.e., conservative regions that over-                    IDLE                                       FOLLOW- LANE, KEEP
                                                                                    LANE RIGHT                                 RIGHT- LANE, KEEP/ DECELERATE/ ACCELER
approximate the possible future states of other agents, can
                                                                                    FASTER                                     FOLLOW- LANE, ACCELERATE
also be integrated into our approach [60]. With this setup, we
                                                                                    SLOWER                                     FOLLOW- LANE, DECELERATE
perform reachability analysis combined with model checking                         Hyperparameter                              κ = 3; number of historical actions: 5
to compute the reachable sets Rk (φ) for k ∈ [0, h] that satisfy                   Frequency setting                           simulation: 15Hz; policy: 5Hz
the joint action and traffic-rule specification φ [44], [45]. We                   Temporal setting
                                                                                                                               scenario duration: 30 steps; ∆t = 0.2s;
iterate through the specification sequence until we identify an                                                                h = 15 (most likely), h = 8 (set-based)
action pair that is verified as safe, which is then returned.
   To ensure safety over an infinite time horizon, we compute                      A. General Settings
fail-safe solutions in parallel that can always safely transfer
the ego vehicle to an invariably safe state [62], i.e., a state                       We evaluated S AN DRA using the open-source Common-
that remains safe for an infinite time horizon. This guarantees                    Road framework [65]. In our implementation, we used the
collision-free operation for all behaviors of other traffic par-                   CommonRoad-Reach toolbox [66] for reachability analysis
ticipants that are consistent with the assumed traffic rules and                   and the Spot tool [59] for LTLf model checking. In the
modeling assumptions [33, Sec. X]. An example of such an                           reachability analysis, we employed a point-mass model that
invariably safe state is engaging a provably correct adaptive                      overapproximated the vehicle dynamics, conservatively sub-
cruise controller [63] at the end of the planning horizon on                       suming all feasible behaviors by using bounded accelerations
highways. We refer to the inductive proof in [64, Sec. III]                        as inputs to compute the reachable sets. Additionally, we used
showing that the verification pipeline guarantees that the ego                     time-to-collision as the criticality measure, computed with the
vehicle remains within a safe state at all times and that a fail-                  CommonRoad-CriMe toolbox [57]. In closed-loop evaluations,
safe solution is always available.                                                 the widely-used highway-env [67] simulation environment
                                                                                   was employed to assess the safety of driving actions, where
Running Example: As shown in Fig. 5b, the reachable set                            the most likely trajectories were predicted under a constant-
at time step k with respect to φacc foll (cf. (4)) considers the                   velocity assumption. The set-based predictions of the other
set-based prediction of the preceding vehicle as the forbidden                     vehicles were computed based on [61]. We used GPT-4o [68]
states, with colliding regions removed. By further considering                     as the cloud-based LLM and Qwen3 [69] as the local LLM.
φR G1 along with the most likely prediction of the preceding                       The experiments were conducted on a desktop equipped with
vehicle (cf. (6)), reachable states that violate the safe distance                 an AMD Ryzen 7 9800X 8-core processor and an NVIDIA
rule are additionally pruned.                                                      RTX 5090 GPU. The parameters used in the numerical exper-
                                                                                   iments are shown in Tab. III; all remaining parameters were
                                                                                   as defined in the original paper.
                             IV. E VALUATION                                          1) Scenarios: For open-loop batch evaluation, we used
                                                                                   highway scenarios from the highD dataset [70] to finetune
   In this section, we evaluate the effectiveness of our proposed                  LLMs and urban scenarios from the MONA dataset [71]
framework under the settings described in Sec. IV-A. We begin                      to evaluate the performance of our approach. Both datasets
with a case study in Sec. IV-B, followed by several ablation                       contained recordings of naturalistic vehicle trajectories, where
studies in Sec. IV-C to validate the design choices of the                         the trajectories of other obstacles were treated as their most
S AN DRA framework. Finally, we assess its performance in                          likely predictions. For each scenario, a vehicle was randomly
a closed-loop decision-making setting in Sec. IV-D.                                selected as the ego vehicle, a decision-making problem was
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                           vii



                                                                                               where we define braking justification(x) as the case in
                  Other vehicle                                                                which the ego vehicle executes a fail-safe action.
                                                                                             • R G3: “The ego vehicle must not exceed the speed
                                                                                               limit.6 ”, which was formalized as [37, Tab. I]:
                                                              Ego vehicle   Most likely
                                                                            trajectory

                                      (a) Initial scenario.
                                                                                                    φR G3 = G keeps lane speed limit(x)∧
                  Reachable set at step 23
                                                                                                                    keeps fov speed limit(x)∧
                                                                                                                                                                   (8)
                                                                                                                    keeps type speed limit(x)∧
                                                                                                                                                
                                                                                                                    keeps braking speed limit(x) .

                             3D view                                                      B. Case Study
             (b) Reachable sets for the actions ACCELERATE and RIGHT- LANE.                  Consider a German urban scenario (cf. Fig. 6a) where the
                                                                                          ego vehicle was heading toward a signalized intersection with
                        Reachable sets                                                    a velocity of 7.7m/s and acceleration of −2.1m/s2 . Given the
                                                                                          lane structure – with a right adjacent lane to the ego vehicle
                                                                             Planned      – all longitudinal actions were feasible, while the available
                                                                            trajectory
                                                   Sampled trajectories                   lateral actions were limited to FOLLOW- LANE and RIGHT-
                                                                                          LANE. The user command was set to “drive faster”, with the
(c) Reachable sets for the actions DECELERATE and FOLLOW- LANE as well                    number of ranked action pairs limited to κ = 3, a decision-
as the planned trajectory.
                                                                                          making horizon of h = 25, and a time increment of ∆t = 0.1s.
                                                                                          After automatically describing the environment and providing
                                                                                          the prompt to GPT-4o, we obtained a ranked sequence of three
                                                                                          longitudinal-lateral action pairs:
                                                                    Set-based
                                                                    prediction               1) ACCELERATE, RIGHT- LANE,
                                  3D view
                                                                                             2) KEEP, RIGHT- LANE, and
(d) Reachable sets for the actions DECELERATE and FOLLOW- LANE with the                      3) DECELERATE, FOLLOW- LANE.
set-based prediction of the other obstacles.
                                                                                             We verified the safety of the first action pair by computing
                                                                                          the reachable sets that satisfy the corresponding action formula
v[m/s]




         5                                                                                in LTLf , as shown in Fig. 6b. The reachable set at time
         0                                                                                step 23 was notably small and became empty at time step 24
             0      5       10       15     20      25
                                 k                              Fail-safe                 due to complete overlap with the predicted occupancy of the
                                                               trajectory
                                                                                          preceding vehicle. As a result, the first action pair was verified
                                                                                          to be unsafe. The second-best result, KEEP and RIGHT- LANE,
(e) Fail-safe trajectory when no verified action is available, with the velocity
profile decelerating to a standstill.                                                     likewise resulted in empty reachable sets due to collisions.
                                                                                          Afterwards, we computed the reachable sets satisfying the last
Fig. 6: CommonRoad scenarios5 in which the ego vehicle approaches a
signalized intersection. (6b) and (6c) use the most likely predictions of other           action pair DECELERATE and FOLLOW- LANE, as shown in
obstacles, while (6d) employs set-based predictions. When formalized traffic              Fig. 6c, and used a sampling-based planner [73] to find the
rules are incorporated in (6e), no safe action is found and a fail-safe mode is           optimal trajectory within these sets. By sampling only within
activated. The trajectory of the ego vehicle is referenced from the rear axle,
and, in the 3D view, the upward axis denotes time steps.                                  the obtained reachable sets, the trajectory was found faster
                                                                                          than sampling the entire solution space.
formulated based on its initial state, and the vehicle was                                   Fig. 6d shows that the last action pair was provably safe
subsequently removed from the scenario. The trajectory of the                             within the decision-making horizon, provided the reachable
ego vehicle was labeled with high-level actions based on the                              sets remained non-empty under the set-based prediction of
LTLf formulas in Tab. II, whose distribution was summarized                               other obstacles. However, the action pair was not legally safe,
in Tab. III.                                                                              as the reachable sets became empty when the action formula
   2) Traffic Rules: We adopted the German traffic rules from                             was conjoined with φR G1 ∧ φR G2 ∧ φR G3 . This occurred be-
[37, Sec. III-A], which were formalized in MTL and rewritten                              cause the initial velocity of the ego vehicle was too high for it
in LTLf . In addition to the safe distance rule R G1 introduced                           to brake smoothly and avoid a collision if the preceding vehicle
in the running example (cf. (6)), the following general traffic                           braked suddenly; that is, the safe distance rule φR G1 could
rules were considered (see Fig. 4):                                                       not be satisfied without violating the unnecessary braking rule
   • R G2: “The ego vehicle is not allowed to brake abruptly                              φR G2 . In such a situation, a fail-safe solution was required
     without reason.”, which was formalized as [72, (11)]:                                to guarantee safety over an infinite time horizon, bringing the
                 φR G2 = G brakes abruptly(x) →                                           ego vehicle to a standstill, as shown in Fig. 6e.
                                                                                   (7)
                                             braking justification(x) ,                        6 The speed limit value was automatically obtained from the environment,
                                                                                          e.g., from traffic signs, and integrated into the rule description as “the
         5 CommonRoad-ID: DEU Goeppingen-37 1 T-4                                         maximum allowed speed is speed limit ”.
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                     viii



                 h = 10 (0.4s)                   h = 25 (1.0s)             h = 50 (2.0s)           DRA, using the recorded trajectories of other obstacles;
100%                                                                                               and
                                                                                                • Top-κ accuracy: the proportion of scenarios where the
                                                                                                   dataset label appeared among the top κ action pairs.
  50%
                                                                                             Please note that the final state recorded in the dataset was
                                                                                             withheld from the LLM to avoid revealing the ground-truth de-
     0%
                       Safe@1             Safe@3        Top-1 accuracy Top-3 accuracy        cision outcome. Moreover, we did not include the formalized
                                (a) Different decision-making horizons.
                                                                                             traffic rules in the reachability analysis, as it was shown that
                                                                                             many human drivers violated rules in the dataset [37], [38],
                 “Drive aggressively”            No command             “Drive cautiously”
                                                                                             making it unsuitable as an upper-limit performance indicator.
100%
                                                                                                1) Decision-Making Horizon h: In Fig. 7a, we present the
                                                                                             evaluation results under different decision-making horizons h
  50%                                                                                        (10, 25, and 50), without user commands and using GPT-
                                                                                             4o as the LLM. Although longer horizons imposed stricter
     0%                                                                                      safety requirements, the safe@κ results did not decrease with
                       Safe@1             Safe@3        Top-1 accuracy Top-3 accuracy        increasing h. This was because shorter horizons often pre-
                                    (b) Different user commands.                             vented lane-change maneuvers from completing successfully,
                 Without traffic rule prompt                     With traffic rule prompt    and in our test scenarios, the stricter requirements of longer
100%                                                                                         horizons were not pronounced enough to clearly affect the
                                                                                             trend. In contrast, the matching metric top-κ remained largely
                                                                                             unchanged as the horizon increased, since it was not affected
  50%
                                                                                             by h. In the following ablation studies, we used h = 25
                                                                                             as the default decision-making horizon to better illustrate the
     0%                                                                                      differences between the various setups.
                       Safe@1             Safe@3        Top-1 accuracy Top-3 accuracy
                                                                                                2) User Commands: We included three different setups
                               (c) With and without traffic rule prompt.
                                                                                             for driving styles: no command, the command “driving ag-
                                    Finetuned                                 Finetuned
                 GPT-4o              GPT-4o            Qwen3-0.6B            Qwen3-0.6B      gressively”, and the command “driving cautiously”. All styles
100%                                                                                         used GPT-4o as the underlying LLM. The results in Fig. 7b
                                                                                             showed that, on average, a safe action could be found with
                                                                                             κ = 3 in 99.8% of cases, where 100% was achieved when
  50%
                                                                                             using fail-safe planning. Since our focus was on the safety
                                                                                             of driving decisions, κ = 3 was recommended as it balanced
     0%                                                                                      the maximum number of iterations with the effectiveness of
                       Safe@1             Safe@3        Top-1 accuracy Top-3 accuracy
                                                                                             finding safe decisions. Among all command options, driving
                               (d) Metric comparison of different LLMs.                      cautiously was the most effective for identifying safe actions
       GPT-4o




                Inference                                                                    at both k = 1 and k = 3. In addition, the top-κ accuracy
                Verification                                                                 results indicated that the behaviors of human drivers in the
                                                                                             MONA dataset most closely aligned with a cautious driving
Qwen3-




                Inference                                                                    style, which was consistent with typical driving patterns in
 0.6B




                Verification                                                                 urban environments. Because the off-the-shelf LLM a) was
 Verifying all 12                                                                            not pretrained on structured driving data, b) received inputs
  action comb.                                                                               in a textual format (which human drivers typically do not use
                                               10−1             100                  101     for decision-making), and c) had to generate explicit driving
                                                 Computation time [s]
                                                                                             actions, its top-1 accuracy remained relatively low across all
(e) Runtime comparison of the approaches shown in (7d) and of the exhaustive                 commands.
verification of all action combinations without LLM assistance. For improved
clarity, outliers and runs exceeding 30s are excluded.                                          3) Traffic Rule Prompt: We compared our prompt design
Fig. 7: Ablation studies on the effectiveness of the main components of
                                                                                             with and without the narrative concretization of three general
S AN DRA.                                                                                    traffic rules using GPT-4o as the underlying LLM without user
                                                                                             commands. The concretization, illustrated below, is appended
                                                                                             to the bottom of the LLM prompt (cf. Fig. 4).
C. Ablation Study
                                                                                               <Traffic rules>: Please adhere to the traffic regulations in
   We conducted ablation studies on the main components of                                     {country} :
the S AN DRA framework, evaluating their effectiveness using                                         [(R G1: Safe distance to preceding vehicle rule .)]
two metrics in an open-loop setting on the 800 MONA test                                             [(R G2: Unnecessary braking rule .)]
scenarios (cf. Tab. III):                                                                            [(R G3: Maximum speed limit rule .)]

         •       Safe@κ: the proportion of scenarios where at least one of                   As shown in Fig. 7c, including the traffic rules in the prompt
                 the returned κ action pairs was verified as safe by S AN -                  made it slightly easier to identify safe actions among the
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                     ix



TABLE IV: Evaluation of safety and matching performance by action type,           achieved the highest safe@κ score in the longitudinal and
with the best values in each column highlighted in bold according to the action
direction.
                                                                                  lateral directions, respectively, which was aligned with the safe
                                                                                  distance rule φR G1 , as deceleration maintained longitudinal
Action               Safe@1          Safe@3       Top-1 Acc.      Top-3 Acc.      spacing and lane following protected lateral safety. Since the
K EEP                 90.8%          98.8%          51.8%           85.0%
                                                                                  majority of driving behaviors in the training dataset involved
ACCELERATE            85.5%          97.9%          11.0%           35.4%         maintaining velocity and following the lane (cf. Tab. III), the
D ECELERATE           92.0%          99.0%          25.0%           68.2%         KEEP and FOLLOW- LANE actions achieved the highest top-κ
F OLLOW- LANE         90.5%          98.8%          40.4%           74.9%         accuracy among all actions.
L EFT- LANE           83.9%          98.2%           1.8%           33.9%
R IGHT- LANE          74.3%          97.1%           0.0%           20.0%
                                                                                  D. Closed-Loop Evaluation
                                                                                     In the highway-env simulation, our longitudinal and lateral
first returned action pairs. With respect to accuracy against                     action pairs were mapped to the embedded discrete meta-
the dataset labels, the presence or absence of the traffic rule                   actions, as listed in Tab. III. Note that the longitudinal action
prompt did not make any noticeable difference. Given this                         STOP was excluded, as it was not applicable in the given
minor effect and the fact that not all safe actions were traffic-                 highway driving context. Due to the absence of explicit
rule-compliant, we chose to not include the traffic rule prompt                   emergency maneuvers in the simulation environment and the
in our framework. Instead, it was necessary to incorporate                        modeling of other vehicles using the intelligent driver model
formalized traffic rules into safety verification to enhance legal                [67], the meta-action SLOWER was adapted as the fail-safe
safety in decision-making.                                                        behavior by increasing its braking intensity.7 Furthermore, we
   4) LLMs: We conducted supervised finetuning of both                            utilized GPT-4o as the LLM, incorporating the user command
GPT-4o and Qwen3-8B on the highD dataset. Each training                           “do not change lanes too often” alongside the traffic rule
example consisted of a system prompt and a user prompt de-                        prompt encoding the general rules listed in Sec. IV-A2.
scribing a driving scenario (cf. Fig. 4), deliberately excluding                     1) Evaluation Settings: We compared our approach to
explicit user commands. The output was a JSON-formatted                           the state-of-the-art framework DiLu [7], which featured a
action ranking, with the labeled action pair ranked highest and                   decision-making agent equipped with memory, reasoning, and
the remaining positions filled with randomly ordered feasible                     reflection capabilities, as well as a memory module for re-
action pairs. GPT-4o was finetuned via the OpenAI API, while                      taining experience. Note that we disabled memory collection
low-rank adaptation [58] was applied to the locally hosted                        during evaluation to maintain a fair comparison. Following
Qwen3 model. Both models used instruction finetuning on the                       [7], we adapted six metrics to evaluate the performance of
collected training samples, with the objective of predicting the                  safe decision-making in a closed-loop setting:
labeled action rankings from the scenario prompt, using cross-                       • Success rate: the percentage of scenarios where the ego

entropy loss over the token sequence. As shown in Fig. 7d,                              vehicle completed the full duration without collisions;
both finetuned models achieved high safe@1 and safe@3                                • Collision-free steps: the average collision-free time steps

scores exceeding 99%, along with a significant increase in top-                         across all scenarios;
1 accuracy compared to their pretrained counterparts. Addi-                          • Rule-compliant steps: the average number of time steps

tionally, Qwen3 achieved comparable top-κ accuracy to GPT-                              across all scenarios during which the ego vehicle re-
4o despite having a much smaller model size. The runtime                                mained compliant with the given traffic rule;
performance of the GPT-4o and Qwen3-0.8B models with                                 • Success steps: the average number of time steps across

κ = 3, including both their original and finetuned versions,                            all scenarios that were both collision-free and compliant
was shown in Fig. 7e. Qwen3-0.8B achieved an average                                    with all traffic rules;
computation time of 0.67s, which was considerably shorter                            • Traveled distance: the average longitudinal distance

than that of GPT-4o at 5.56s, and was suitable for local de-                            traveled from the initial state to the end of the scenario
ployment with low latency. For both models, safety verification                         simulation; and
consumed only a negligible portion of the overall decision-                          • Fail-safe rate: percentage of time steps during which a

making process, with an average runtime of 0.033s and a                                 fail-safe action was executed.
standard deviation of 0.018s. We additionally reported the                        The evaluation was conducted under three different environ-
runtime of randomly enumerating all 12 action combinations                        mental settings:
without LLM assistance. This exhaustive computation was                            ⃝1 highway with four lanes and a vehicle density8 of 2;
more expensive than verifying the top-3 action pairs suggested                     ⃝2 highway with four lanes and a vehicle density of 3; and
by the LLM, yet still faster than the LLM inference itself,                        ⃝3 highway with five lanes and a vehicle density of 3.
indicating potential room for improvement in online LLM                           Each setting was evaluated using 10 different random seeds9
acceleration.                                                                     and repeated three times. The ego vehicle updated its decision
   5) Action Type: We categorized the safe@κ and top-κ ac-
                                                                                       7 The time constant for the speed response was set to 0.6s, and the speed
curacy metrics from the above ablation studies by action type
                                                                                  increment step was set to 15m/s.
(cf. Tab. II) in Tab. IV to illustrate how different actions impact                    8 The larger the density, the smaller the vehicle longitudinal spacing.
safety and the accuracy of action predictions. The results                             9 Highway-env seeds: 5838, 2421, 7294, 9650, 4176, 6382, 8765, 1348,
indicated that the DECELERATE and FOLLOW- LANE actions                            4213, and 2572.
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                    x



TABLE V: Closed-loop evaluation across three settings, where values in bold denote the best performance. Note that the traveled distance is computed only
for runs that were successfully completed.

                                                                                Rule-compliant steps
Method                         Setting   Success rate   Collision-free steps                              Success steps   Traveled distance     Fail-safe rate
                                                                               φR G1 φR G2 φR G3

                                 ⃝
                                 1         93.3%               27.7            15.7      24.4      27.7       12.3             116.5m                 -
DiLu [7]                         ⃝
                                 2         53.3%               18.8            12.1      14.7      18.8       8.0               94.8m                 -
                                 ⃝
                                 3         76.7%               23.8            13.8      19.6      23.8       9.6              102.4m                 -
S AN DRA +                       ⃝
                                 1         83.3%               28.5            23.3      21.7      28.5       15.3             114.4m              6.5%
 most likely pred. +             ⃝
                                 2         73.3%               25.6            17.5      19.5      25.6       10.9              93.7m              6.8%
 w/o traffic rules in verif.     ⃝
                                 3         83.3%               25.8            16.9      20.6      25.8       11.1              98.7m              7.3%
S AN DRA +                       ⃝
                                 1        100.0%               30.0            28.5     26.8       30.0       20.0              84.4m              25.2%
 most likely pred. +             ⃝
                                 2         96.7%               29.4            27.2     26.3       29.4       19.9              68.4m              25.0%
 w/ traffic rules in verif.      ⃝
                                 3        100.0%               30.0            27.5     27.2       30.0       20.3              72.5m              26.1%
S AN DRA +                       ⃝
                                 1        100.0%               30.0            25.0      16.2      30.0       16.5             113.6m              3.8%
 set-based pred. +               ⃝
                                 2        100.0%               30.0            21.4      14.3      30.0       14.1              88.6m              7.4%
 w/o traffic rules in verif.     ⃝
                                 3        100.0%               30.0            19.6      13.7      30.0       13.1              86.4m              7.9%
S AN DRA +                       ⃝
                                 1        100.0%               30.0            28.4      25.3      30.0       20.8              85.6m              25.9%
 set-based pred. +               ⃝
                                 2        100.0%               30.0            27.7      23.9      30.0       20.9              70.1m              26.9%
 w/ traffic rules in verif.      ⃝
                                 3        100.0%               30.0            27.6      23.3      30.0       20.2              72.2m              25.8%



every three simulation steps, and the selected action was held                         FASTER       SLOWER       IDLE       LANE RIGHT         LANE LEFT
constant between updates (cf. Tab. III).                                         1.0
   2) Safety Evaluation: The results in Tab. V showed that all
variants of S AN DRA achieved a performance comparable to                        0.5
or better than DiLu in terms of success rate. This held even
though it did not incorporate few-shot examples from past                        0.0
                                                                                                    S AN DRA + S AN DRA + S AN DRA +           S AN DRA +
driving experiences into the prompt. By relying solely on the                           DiLu [7]      most likely most likely set-based          set-based
zero-shot prompt, our approach not only reduced token usage                                           w/o rules   w/ rules    w/o rules          w/ rules
but also eliminated dependency on the quality and availability                   Fig. 8: Action distribution of the ego vehicle in the highway-env simulation,
of prior examples. Regarding formal safety, relying solely on                    where fail-safe actions are not taken into account.
most likely predictions was insufficient, particularly in critical
scenarios where the actual behavior of the other obstacles                       performance.
might have deviated significantly, e.g., under setting ⃝.  2 Al-
                                                                                    4) Conservatism: The traveled distance reported in Tab. V
though formalized traffic rules were considered and fail-safe                    indicated that, without integrating rules into the verification
actions were frequently triggered, these fallback interventions                  process, the set-based approach did not induce overly con-
could still fail, i.e., when the current scenario had already left               servative behavior for the ego vehicle, particularly in less
the ego vehicle without any feasible safe action. In contrast,                   dense scenarios (e.g., setting ⃝  1 ). This was further supported
set-based prediction allowed the ego vehicle to account for all                  by the low fail-safe rate and by the fact that S AN DRA
possible behaviors of other vehicles over the decision-making                    allowed more lane-change options than DiLu, regardless of
horizon, thereby ensuring safety at all times.                                   the prediction model (cf. Fig. 8). In contrast, incorporating
   3) Rule Compliance: For traffic rule compliance, we ob-                       traffic rules in the reachability analysis increased the rate of
served that S AN DRA substantially improved adherence to the                     fail-safe actions, since most highway-env scenarios were not
safe distance rule φR G1 compared to DiLu, irrespective of                       initialized with the ego vehicle maintaining a safe distance to
the specific variant. The greatest improvement was achieved                      preceding vehicles; consequently, the first few time steps were
when formalized rules were incorporated into the reachability                    often required for emergency braking. This also resulted in
analysis. However, this also resulted in more fail-safe actions,                 additional acceleration actions (cf. Fig. 8), as the ego vehicle
i.e., emergency braking, which in turn reduced the traveled                      needed to recover the distance lost during the fail-safe period.
distance, particularly in our dense traffic settings. When com-                  Reducing the number of fail-safe actions would have required
bining most likely predictions with traffic rules in the verifica-               either relaxing the traffic rules or adopting trajectory repair for
tion, compliance with φR G2 was generally higher, whereas set-                   rule compliance [43], both of which, however, were beyond
based predictions maintained larger longitudinal gaps between                    the scope of this work.
vehicles, often resulting in unnecessary braking. Furthermore,                      5) Example Scenario: An example scenario from highway-
all runs complied with the speed limit rule φR G3 . Overall,                     env was shown in Fig. 9a, where DiLu failed to account
integrating set-based predictions with formalized traffic rules                  for the dynamic coupling between ego vehicle braking and
into the safety verification yielded the highest number of                       the distance to the preceding vehicle, resulting in a rear-
success steps, i.e., the best collision-free and legally compliant               end crash at simulation step 8 (cf. Fig. 9b). This issue
  JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                               xi



                   Ego vehicle           Other vehicle                Past occupancies        DiLu exhibited a high degree of violations from the very
                                                                                              beginning, ultimately leading to a collision. In contrast, safety
                                                                                              verification using set-based predictions in S AN DRA improved
                                 dsafe                                                        rule compliance of the ego vehicle from the very beginning.
                                                                                              Moreover, the variant that incorporated formalized traffic rules
                                         (a) Initial scenario.                                achieved the highest robustness in rule compliance on average
                                                                                              across scenarios.

                                                                                                                         V. C ONCLUSION
                                                                                                 We present the first framework for safe decision-making
  (b) Termination of the scenario at time step 8 due to a collision using DiLu.
                                                                                              in automated vehicles using LLMs. By translating natural
                                                                                              language driving actions into LTLf formulas, we enable
                                                                                              the coupling of set-based reachability analysis with model
                                                                                              checking to verify the safety of each action. Unlike existing
                                                                                              methods, our approach supports lightweight LLM prompt-
  (c) Safe decision-making at time step 8 using S AN DRA with set-based
  prediction of other obstacles, without incorporating traffic rules in the safety            ing, addresses inherent safety gaps in LLMs, and provides
  verification.                                                                               provable safety guarantees through set-based predictions of
                                                                                              surrounding obstacles and the verification of formalized traffic
                                                                                              rules. Additionally, our approach bridges decision-making and
                                                                                              downstream trajectory planning by leveraging the computed
                                                                                              reachable sets as planning constraints. Future work includes
  (d) Safe decision-making at time step 8 using S AN DRA with set-based pre-                  exploring the selection of optimal decision-making horizons,
  diction of other obstacles, incorporating traffic rules in the safety verification.         employing vision-language models with surround-view images
              DiLu ((b))
                                 S AN DRA + set-based             S AN DRA + set-based.       or point clouds as inputs to achieve a broader multimodal
                                 w/o rules in verif. ((c))         w/ rules in verif. ((d))
                                                                                              understanding of the environment, and deploying our approach
Robustness




             0.1
                                                                                              on a research vehicle in real-world scenarios.
             0.0
         −0.1                                                                                                          ACKNOWLEDGMENT
                   0                8    10                      20                     30
                                               Time step k                                       The authors gratefully acknowledge the financial support
  (e) Robustness evaluation of the simulated trajectories for compliance with                 provided by the German Research Foundation (DFG) under
  the traffic rules.                                                                          grant AL 1185/9-1, as well as the provision of API credits
  Fig. 9: Illustrative comparison in highway-env10 under setting ⃝,
                                                                 2 in which
                                                                                              through the OpenAI Research Access Program.
  the past occupancies of vehicles are shown for the previous five time
  steps.                                                                                                                    R EFERENCES
                                                                                               [1] B. Paden, M. Čáp, S. Z. Yong, D. Yershov, and E. Frazzoli, “A survey of
                                                                                                   motion planning and control techniques for self-driving urban vehicles,”
  was mitigated by S AN DRA through set-based prediction of                                        vol. 1, no. 1, pp. 33–55, 2016.
  surrounding obstacles, which considered possible emergency                                   [2] H. Krasowski, X. Wang, and M. Althoff, “Safe reinforcement learning
  braking maneuvers of the preceding vehicle during decision-                                      for autonomous lane changing using set-based prediction,” in Proc. of
                                                                                                   the IEEE Int. Conf. on Intell. Transp. Syst., 2020, pp. 1–7.
  making. Since the ego vehicle was initially too close to the                                 [3] C. Cui, Y. Ma, X. Cao, W. Ye, Y. Zhou, K. Liang, J. Chen, J. Lu,
  preceding vehicle (cf. Fig. 9a), it first executed a series of                                   Z. Yang, K.-D. Liao, et al., “A survey on multimodal large language
  fail-safe actions to create sufficient space before following the                                models for autonomous driving,” in Proc. of the IEEE/CVF Winter Conf.
                                                                                                   on Applications of Computer Vision, 2024, pp. 958–979.
  LLM-planned actions (cf. Figs. 9c and 9d). When formalized                                   [4] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen,
  traffic rules were incorporated in the verification process, this                                J. Tang, X. Chen, Y. Lin, et al., “A survey on large language model based
  phase was prolonged (cf. Fig. 9d) to satisfy additional safe-                                    autonomous agents,” Frontiers of Computer Science, vol. 18, no. 6, p.
                                                                                                   186345, 2024.
  distance requirements in the rule R G1 (cf. (6)).                                            [5] Y. Jin, R. Yang, Z. Yi, X. Shen, H. Peng, X. Liu, J. Qin, J. Li, J. Xie,
     To quantify the extent to which the ego vehicle complied                                      P. Gao, et al., “SurrealDriver: Designing LLM-powered generative driver
  with or violated the three traffic rules in MTL, we additionally                                 agent framework based on human drivers’ driving-thinking data,” in
                                                                                                   Proc. of the IEEE/RSJ Int. Conf. on Intell. Robots and Syst., 2024, pp.
  presented the robustness [33, Sec. VI] of trajectories obtained                                  966–971.
  from the example scenarios in Fig. 9e. A positive robustness                                 [6] T. Cai, Y. Liu, Z. Zhou, H. Ma, S. Z. Zhao, Z. Wu, and J. Ma,
  value indicated satisfaction of the rules, whereas a negative                                    “Driving with regulation: Interpretable decision-making for autonomous
                                                                                                   vehicles with retrieval-augmented reasoning via LLM,” arXiv preprint
  value indicated violation. The larger the absolute value of                                      arXiv:2410.04759, 2024.
  the robustness, the stronger the satisfaction or violation of                                [7] L. Wen, D. Fu, X. Li, X. Cai, T. Ma, P. Cai, M. Dou, B. Shi, L. He, and
  the rules. For a systematic measure of robustness for the                                        Y. Qiao, “DiLu: A knowledge-driven approach to autonomous driving
                                                                                                   with large language models,” in Proc. of the Int. Conf. on Learning
  general traffic rules in Sec. IV-A2, we refer the reader to                                      Representations, 2024.
  [74]. Without explicitly considering rules in decision-making,                               [8] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao,
                                                                                                   “Reflexion: Language agents with verbal reinforcement learning,” Proc.
                                                                                                   of the Advances in Neural Information Processing Syst., vol. 36, pp.
             10 Highway-env seed: 5838                                                             8634–8652, 2023.
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                      xii



 [9] K. Jiang, X. Cai, Z. Cui, A. Li, Y. Ren, H. Yu, H. Yang, D. Fu,             [31] C. Pek, S. Manzinger, M. Koschi, and M. Althoff, “Using online
     L. Wen, and P. Cai, “KoMa: Knowledge-driven multi-agent framework                verification to prevent autonomous vehicles from causing accidents,”
     for autonomous driving with large language models,” IEEE Trans. on               Nature Machine Intell., vol. 2, no. 9, pp. 518–528, 2020.
     Intell. Veh., vol. 10, no. 10, pp. 4655–4668, 2025.                         [32] H. Ahn, K. Berntorp, P. Inani, A. J. Ram, and S. Di Cairano,
[10] Z. Zhou, H. Huang, B. Li, S. Zhao, Y. Mu, and J. Wang, “SafeDrive:               “Reachability-based decision-making for autonomous driving: Theory
     Knowledge-and data-driven risk-sensitive decision-making for au-                 and experiments,” IEEE Trans. on Control Syst. Technology, vol. 29,
     tonomous vehicles with large language models,” Accident Analysis &               no. 5, pp. 1907–1921, 2020.
     Prevention, vol. 224, p. 108299, 2026.                                      [33] M. Althoff, S. Maierhofer, G. Würsching, Y. Lin, F. Lercher, and
[11] H. Pang, Z. Wang, and G. Li, “Large language model guided deep                   R. Stolz, “No more traffic tickets: A tutorial to ensure traffic-rule
     reinforcement learning for decision making in autonomous driving,”               compliance of automated vehicles,” Proc. of the IEEE, pp. 1–30, 2025,
     arXiv preprint arXiv:2412.18511, 2024.                                           early Access.
[12] G. Kou, F. Jia, W. Mao, Y. Liu, Y. Zhao, Z. Zhang, O. Yoshie, T. Wang,      [34] N. Aréchiga, “Specifying safety of autonomous vehicles in signal
     Y. Li, and X. Zhang, “PADriver: Towards personalized autonomous                  temporal logic,” in Proc. of the IEEE Intell. Veh. Symp., 2019, pp. 58–63.
     driving,” pp. 1–8, 2025.                                                    [35] M. Hekmatnejad, S. Yaghoubi, A. Dokhanchi, H. B. Amor, A. Shrivas-
[13] W. Wang, J. Xie, C. Hu, H. Zou, J. Fan, W. Tong, Y. Wen, S. Wu,                  tava, L. Karam, and G. Fainekos, “Encoding and monitoring responsi-
     H. Deng, Z. Li, et al., “DriveMLM: Aligning multi-modal large language           bility sensitive safety rules for automated vehicles in signal temporal
     models with behavioral planning states for autonomous driving,” arXiv            logic,” in Proc. of the ACM/IEEE Int. Conf. on Formal Methods and
     preprint arXiv:2312.09245, 2023.                                                 Models for Syst. Design, 2019, pp. 1–11.
[14] J. Mao, Y. Qian, H. Zhao, and Y. Wang, “GPT-driver: Learning to drive       [36] K. Esterle, L. Gressenbuch, and A. Knoll, “Formalizing traffic rules for
     with GPT,” arXiv preprint arXiv:2310.01415, 2023.                                machine interpretability,” in Proc. of the IEEE Connected and Automated
[15] C. Sima, K. Renz, K. Chitta, L. Chen, H. Zhang, C. Xie, P. Luo,                  Veh. Symp., 2020, pp. 1–7.
     A. Geiger, and H. Li, “DriveLM: Driving with graph visual question          [37] S. Maierhofer, A.-K. Rettinger, E. C. Mayer, and M. Althoff, “Formal-
     answering,” in Proc. of the European Conf. on Computer Vision, 2024,             ization of interstate traffic rules in temporal logic,” in Proc. of the IEEE
     pp. 256–274.                                                                     Intell. Veh. Symp., 2020, pp. 752–759.
[16] H. Shao, Y. Hu, L. Wang, S. L. Waslander, Y. Liu, and H. Li, “LMDrive:      [38] S. Maierhofer, P. Moosbrugger, and M. Althoff, “Formalization of
     Closed-loop end-to-end driving with large language models,” in Proc.             intersection traffic rules in temporal logic,” in Proc. of the IEEE Intell.
     of the IEEE/CVF Conf. on Computer Vision and Pattern Recognition,                Veh. Symp., 2022, pp. 1135–1144.
     2024, pp. 15 120–15 130.                                                    [39] A. Corso and M. J. Kochenderfer, “Interpretable safety validation for
[17] Y. Lin, C. Li, M. Ding, M. Tomizuka, W. Zhan, and M. Althoff,                    autonomous vehicles,” in Proc. of the IEEE Int. Conf. on Intell. Transp.
     “DrPlanner: Diagnosis and repair of motion planners for automated                Syst., 2020, pp. 1–6.
     vehicles using large language models,” IEEE Robot. and Automation           [40] Y. E. Sahin, R. Quirynen, and S. Di Cairano, “Autonomous vehicle
     Letters, vol. 9, no. 10, pp. 8218–8225, 2024.                                    decision-making and monitoring based on signal temporal logic and
[18] N. Baumann, C. Hu, P. Sivasothilingam, H. Qin, L. Xie, M. Magno,                 mixed-integer programming,” in Prof. of the American Control Conf.,
     and L. Benini, “Enhancing autonomous driving systems with on-board               2020, pp. 454–459.
     deployed large language models,” in Proc. of Robot.: Science and Syst.,     [41] M. Klischat and M. Althoff, “Synthesizing traffic scenarios from formal
     2025.                                                                            specifications for testing automated vehicles,” in Prof. of the IEEE Intell.
[19] H. Sha, Y. Mu, Y. Jiang, L. Chen, C. Xu, P. Luo, S. E. Li, M. Tomizuka,          Veh. Symp., 2020, pp. 2065–2072.
     W. Zhan, and M. Ding, “LanguageMPC: Large language models as deci-          [42] E. Plaku and S. Karaman, “Motion planning with temporal-logic spec-
     sion makers for autonomous driving,” arXiv preprint arXiv:2310.03026,            ifications: Progress and challenges,” AI communications, vol. 29, no. 1,
     2025.                                                                            pp. 151–162, 2016.
[20] C. Cui, Z. Yang, Y. Zhou, Y. Ma, J. Lu, L. Li, Y. Chen, J. Panchal,         [43] Y. Lin, Z. Xing, X. Han, and M. Althoff, “Traffic-rule-compliant trajec-
     and Z. Wang, “Personalized autonomous driving with large language                tory repair via satisfiability modulo theories and reachability analysis,”
     models: Field experiments,” in Proc. of the IEEE Int. Conf. on Intell.           IEEE Trans. on Robot., pp. 1–18, 2025, early Access.
     Transp. Syst., 2024, pp. 20–27.                                             [44] E. Irani Liu and M. Althoff, “Specification-compliant driving corridors
[21] L. Chen, O. Sinavski, J. Hünermann, A. Karnsund, A. J. Willmott,                for motion planning of automated vehicles,” IEEE Trans. on Intell. Veh.,
     D. Birch, D. Maund, and J. Shotton, “Driving with LLMs: Fusing object-           vol. 8, no. 9, pp. 4180–4197, 2023.
     level vector modality for explainable autonomous driving,” in Proc. of      [45] F. Lercher and M. Althoff, “Specification-compliant reachability analysis
     the IEEE Int. Conf. on Robot. and Autom., 2024, pp. 14 093–14 100.               for autonomous vehicles using on-the-fly model checking,” in Proc. of
[22] Z. Xu, Y. Zhang, E. Xie, Z. Zhao, Y. Guo, K.-Y. K. Wong, Z. Li, and              the IEEE Intell. Veh. Symp., 2024, pp. 1484–1491.
     H. Zhao, “DriveGPT4: Interpretable end-to-end autonomous driving via        [46] X. Li, Z. Serlin, G. Yang, and C. Belta, “A formal methods approach
     large language model,” IEEE Robot. and Automation Letters, vol. 9,               to interpretable reinforcement learning for robotic planning,” Science
     no. 10, pp. 8186–8193, 2024.                                                     Robot., vol. 4, no. 37, p. eaay6276, 2019.
[23] C. Cui, Y. Ma, X. Cao, W. Ye, and Z. Wang, “Drive as you speak: En-         [47] H. Krasowski and M. Althoff, “Provable traffic rule compliance in safe
     abling human-like interaction with large language models in autonomous           reinforcement learning on the open sea,” IEEE Trans. on Intell. Veh.,
     vehicles,” in Proc. of the IEEE/CVF Winter Conf. on Applications of              vol. 9, no. 12, pp. 7617–7634, 2024.
     Computer Vision, 2024, pp. 902–909.                                         [48] P. Bender, J. Ziegler, and C. Stiller, “Lanelets: Efficient map represen-
[24] X. Han, Z. Wu, X. Xia, and J. Ma, “Traffic regulation-aware path                 tation for autonomous driving,” in Proc. of the IEEE Intell. Veh. Symp.,
     planning with regulation databases and vision-language models,” in               2014, pp. 420–425.
     Proc. of the IEEE Int. Conf. on Robot. and Autom., 2025.                    [49] G. Würsching and M. Althoff, “Robust and efficient curvilinear coordi-
[25] J.-J. Hwang, R. Xu, H. Lin, W.-C. Hung, J. Ji, K. Choi, D. Huang, T. He,         nate transformation with guaranteed map coverage for motion planning,”
     P. Covington, B. Sapp, et al., “EMMA: End-to-end multimodal model                in Proc. of the IEEE Intell. Veh. Symp., 2024, pp. 2694–2701.
     for autonomous driving,” arXiv preprint arXiv:2410.23262, 2024.             [50] G. De Giacomo, M. Y. Vardi, et al., “Linear temporal logic and linear
[26] N. Mehdipour, M. Althoff, R. D. Tebbens, and C. Belta, “Formal                   dynamic logic on finite traces.” in Proc. of the Int. Joint Conf. on
     methods to comply with rules of the road in autonomous driving: State            Artificial Intell., vol. 13, 2013, pp. 854–860.
     of the art and grand challenges,” Automatica, vol. 152, no. 110692, 2023.   [51] C. Baier and J.-P. Katoen, Principles of model checking. MIT press,
[27] Y. Chen, M. Jankovic, M. Santillo, and A. D. Ames, “Backup control               2008.
     barrier functions: Formulation and comparative study,” in Proc. of the      [52] A. Platzer and E. M. Clarke, “The image computation problem in hybrid
     IEEE Conf. on Decision and Control, 2021, pp. 6835–6841.                         systems model checking,” in Proc. of the Int. Workshop on Hybrid
[28] D. R. Agrawal, R. Chen, and D. Panagou, “gatekeeper: Online safety               Systems: Computation and Control. Springer, 2007, pp. 473–486.
     verification and control for nonlinear systems in dynamic environments,”    [53] United Nations Economic Commission for Europe, “Convention on
     IEEE Trans. on Robotics, vol. 40, pp. 4358–4375, 2024.                           road traffic,” United Nations Conference on Road Traffic, 1968,
[29] M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, and                 (consolidated version of 2006). [Online]. Available: https://www.unece.
     U. Topcu, “Safe reinforcement learning via shielding,” Proc. of the AAAI         org/fileadmin/DAM/trans/conventn/Conv road traffic EN.pdf
     Conf. on Artificial Intell., vol. 32, no. 1, 2018.                          [54] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal,
[30] M. Althoff and J. M. Dolan, “Online verification of automated road               G. Sastry, A. Askell, P. Mishkin, J. Clark, et al., “Learning transferable
     vehicles using reachability analysis,” IEEE Trans. on Robot., vol. 30,           visual models from natural language supervision,” in Prof. of the Int.
     no. 4, pp. 903–918, 2014.                                                        Conf. on Machine Learning, 2021, pp. 8748–8763.
JOURNAL OF XX, VOL. XX, NO. X, MONTH YEAR                                                                                                                     xiii



[55] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,                                   Yuanfei Lin received his B.Eng. degree in Auto-
     D. Zhou, et al., “Chain-of-thought prompting elicits reasoning in large                               motive Engineering from Tongji University, China,
     language models,” Proc. of the Advances in Neural Info. Processing                                    in 2018, and dual M.Sc. degrees in Mechanical
     Syst., vol. 35, pp. 24 824–24 837, 2022.                                                              Engineering and Mechatronics and Robotics at the
[56] X. Wang, H. Krasowski, and M. Althoff, “Commonroad-RL: A con-                                         Technical University of Munich, Germany, in 2020.
     figurable reinforcement learning environment for motion planning of                                   In 2023, he was a visiting scholar at the University of
     autonomous vehicles,” in Proc. of the IEEE Int. Conf. on Intell. Transp.                              California, Berkeley, USA. He completed his Ph.D.
     Syst., 2021, pp. 466–472.                                                                             in Computer Science at the Technical University of
[57] Y. Lin and M. Althoff, “CommonRoad-CriMe: A toolbox for criticality                                   Munich, Germany, in 2025. His research interests
     measures of autonomous vehicles,” in Proc. of the IEEE Intell. Veh.                                   include motion planning, formal methods, and large
     Symp., 2023, pp. 1–8.                                                                                 language models for automated vehicles.
[58] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang,
     W. Chen, et al., “LoRA: Low-rank adaptation of large language models,”
     Proc. of the Int. Conf. on Learning Representations, vol. 1, no. 2, p. 3,
     2022.
[59] A. Duret-Lutz, A. Lewkowicz, A. Fauchille, T. Michaud, E. Renault, and                                Sebastian Illing is currently pursuing a M.Sc. de-
     L. Xu, “Spot 2.0 – a framework for LTL and ω-automata manipulation,”                                  gree in Computer Science at the Technical Univer-
     in Proc. of the Int. Symposium on Automated Technology for Verification                               sity of Munich, Germany. He received his B.Sc. in
     and Analysis, 2016, pp. 122–129.                                                                      Informatics: Games Engineering in 2024, also from
[60] S. Lefèvre, D. Vasquez, and C. Laugier, “A survey on motion prediction                               the Technical University of Munich, Germany. His
     and risk assessment for intelligent vehicles,” ROBOMECH J., vol. 1,                                   research interests include large language models for
     no. 1, pp. 1–14, 2014.                                                                                autonomous driving and 3D Computer Vision.
[61] M. Koschi and M. Althoff, “Set-based prediction of traffic participants
     considering occlusions and traffic rules,” IEEE Trans. on Intell. Veh.,
     vol. 6, no. 2, pp. 249–265, 2020.
[62] C. Pek and M. Althoff, “Efficient computation of invariably safe states
     for motion planning of self-driving vehicles,” in Proc. of the IEEE/RSJ
     Int. Conf. on Intell. Robot. and Syst., 2018, pp. 3523–3530.
[63] M. Althoff, S. Maierhofer, and C. Pek, “Provably-correct and comfort-
     able adaptive cruise control,” IEEE Trans. on Intell. Veh., vol. 6, no. 1,                            Matthias Althoff is an associate professor in com-
     pp. 159–174, 2020.                                                                                    puter science at the Technical University of Munich,
[64] C. Pek and M. Althoff, “Fail-safe motion planning for online verification                             Germany. He received his diploma engineering de-
     of autonomous vehicles using convex optimization,” IEEE Trans. on                                     gree in Mechanical Engineering in 2005, and his
     Robot., vol. 37, no. 3, pp. 798–814, 2021.                                                            Ph.D. degree in Electrical Engineering in 2010, both
[65] M. Althoff, M. Koschi, and S. Manzinger, “CommonRoad: Composable                                      from the Technical University of Munich, Germany.
     benchmarks for motion planning on roads,” in Proc. of the IEEE Intell.                                From 2010 to 2012 he was a postdoctoral researcher
     Veh. Symp., 2017, pp. 719–726.                                                                        at Carnegie Mellon University, Pittsburgh, USA, and
[66] E. Irani Liu, G. Würsching, M. Klischat, and M. Althoff,                                             from 2012 to 2013 an assistant professor at Tech-
     “CommonRoad-Reach: A toolbox for reachability analysis of automated                                   nische Universität Ilmenau, Germany. His research
     vehicles,” in Proc. of the IEEE Int. Intell. Transp. Systems Conf., 2022,                             interests include formal verification of continuous
     pp. 2313–2320.                                                               and hybrid systems, reachability analysis, planning algorithms, nonlinear
[67] E. Leurent, “An environment for autonomous driving decision-making,”         control, automated vehicles, and power systems.
     https://github.com/eleurent/highway-env, 2018.
[68] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark,
     A. Ostrow, A. Welihinda, A. Hayes, A. Radford, et al., “GPT-4o system
     card,” arXiv preprint arXiv:2410.21276, 2024.
[69] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, et al., “Qwen3
     technical report,” arXiv preprint arXiv:2505.09388, 2025.
[70] R. Krajewski, J. Bock, L. Kloeker, and L. Eckstein, “The highD dataset:
     A drone dataset of naturalistic vehicle trajectories on German highways
     for validation of highly automated driving systems,” in Proc. of the IEEE
     Int. Conf. on Intell. Transp. Syst., 2018, pp. 2118–2125.
[71] L. Gressenbuch, K. Esterle, T. Kessler, and M. Althoff, “MONA: The
     Munich motion dataset of natural driving,” in Proc. of the IEEE Int.
     Conf. on Intell. Transp. Syst., 2022, pp. 2093–2100.
[72] Y. Lin and M. Althoff, “Rule-compliant trajectory repairing using
     satisfiability modulo theories,” in Proc. of the IEEE Intell. Veh. Symp.,
     2022, pp. 449–456.
[73] G. Würsching and M. Althoff, “Sampling-based optimal trajectory
     generation for autonomous vehicles using reachable sets,” in Proc. of
     the IEEE Int. Intell. Transp. Syst. Conf., 2021, pp. 828–835.
[74] Y. Lin, H. Li, and M. Althoff, “Model predictive robustness of signal
     temporal logic predicates,” IEEE Robot. and Automation Letters, vol. 08,
     no. 12, pp. 8050–8057, 2023.
