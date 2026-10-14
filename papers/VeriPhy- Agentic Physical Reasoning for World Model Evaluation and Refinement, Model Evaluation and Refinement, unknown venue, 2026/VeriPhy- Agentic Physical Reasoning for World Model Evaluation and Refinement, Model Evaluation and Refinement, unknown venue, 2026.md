                                            VeriPhy: Agentic Physical Reasoning for World
                                            Model Evaluation and Refinement
                                            Wenzhuo Xu1§ , Yuchen Zhu2 , Chongjian Ge4 , Xuan Shen3 , Jing Shi4 , Jason Kuen4 , Yongxin Chen2 , Molei
                                            Tao2 , Christopher McComb1 , Noelia Grande Gutiérrez1 , Jiuxiang Gu4§†
                                            1
                                              Carnegie Mellon University, 2 Georgia Institute of Technology, 3 Northeastern University, 4 Adobe
                                            Research
                                            §
                                              Core Contribution, † Project Lead

                                            Visual fluency in generated video does not imply physical reliability, and a scalar quality score alone
                                            is incapable of indicating the obligation a clip violates or the moment it fails. We present VeriPhy,
arXiv:2609.03153v1 [cs.CV] 2 Sep 2026




                                            an auditable physical-verification system in which a text-only planner compiles the prompt into
                                            typed physical obligations and a statically validated execution plan before any frame is observed.
                                            During execution, observations gate and scope only declared calls to frozen low-level experts (e.g.,
                                            segmentation and tracking, counting, eleven typed physical measurements over the resulting tracks,
                                            depth, OCR, and audio-event detection). Each action returns a provenance-carrying evidence record
                                            whose payload, when usable, is either a typed measurement or an explicitly tagged learned state. Typed
                                            resolvers and fixed composition map usable records to a three-valued state (supported, contradicted,
                                            or unknown, surfaced as plausible, implausible, or abstain) with full provenance, so that every verdict
                                            is traceable to the evidence that produced it. We anchor evaluation in a 1,500-clip corpus of human-
                                            annotated flaw records that localize real generation failures in prompt reference, space, and time.
                                            On a 149-clip core carrying 304 such records, VeriPhy accounts for 228, against 164 for a published
                                            question-decomposition evaluator given the same clips and the same claims. Recall alone does not
                                            separate it from prompting the same backbone monolithically, which reaches 222; what separates
                                            them is that each decision retains its evidence record and provenance, making the traces auditable
                                            one verdict at a time and usable as the interface through which a critic verdict could be written back
                                            into generation. The core is a development set, so these figures characterize the system rather than
                                            its generalization.

                                            Date: September 2026
                                            Project Page: https://veriphy-ai.github.io




                                        1   Introduction
                                        Contemporary video generation systems can synthesize visually compelling, temporally coherent clips with
                                        synchronized audio. Perceptual plausibility, however, is not evidence of physical validity: a failure may arise
                                        not only in rendered appearance but in any observable consequence of a physical event. Within the visual
                                        stream, entities may be omitted, trajectories may be inconsistent with the forces implied by the scene, and
                                        interactions may violate contact or causal constraints. Within the acoustic stream, an expected sound may be
                                        absent, mistimed, or attributed to the wrong source; across modalities, visual and acoustic observations may
                                        encode incompatible event timing or causality. Thus an object may remain unsupported under gravity, a ball
                                        may pass through a rigid wall, a visible collision may be silent, or the sound of an impact precede contact.
                                        These failures become especially consequential as generated video moves beyond media synthesis into the
                                        training and evaluation loops of embodied systems. Recent video world models have been used to synthesize
                                        robot-training trajectories, support policy learning and evaluation, and reduce the sim-to-real gap; stronger
                                        world models have also been associated with better downstream policy performance [29, 32, 63]. Recently,
                                        evaluation has expanded beyond generic video quality to embodied task correctness and rule-level physical
                                        diagnosis [4, 15, 38, 42], while complementary work has introduced temporal localization and the evaluation
                                        of acoustic or cross-modal physical consistency [9, 14, 77, 88].



                                                                                               1
    Prior •    baseline                   VeriPhy •   auditable execution
                                          Text-only planner before frames      Generated A/V runtime

               Closed       VLM               Plan                                                          Fixed
    Claim                                                                                 Evidence
              question     yes / no        what to check      Action    Observation                      composition   Claim state
                                                                                           record
                                           how to check

         No measurement trace                              VeriPhy loop • gate / scope


    Evidence trace •      one shared A/V clock Observed             Expected      Generated          0


     0
                                                  wall contact
                                                                    2
                                                                            Penetration


                                                                                                     1
                                      Expected rebound
                                      1

                     floor contact

                          observed floor impact            expected wall impact
         Audio waveform
    3
                                                                                                     2




   Sample prompt: “A spinning basketball bounces on the floor and rebounds from a rigid wall; impact sounds align with contact.”


Figure 1 Overview of VeriPhy relative to question decomposition. The numbered views magnify rotation, floor-contact
deformation, generated wall penetration, and the counterfactual rigid-wall rebound; the waveform shares the visual
event clock. The scene is illustrative rather than a recorded execution.

Despite this progress, recent evaluators capture complementary components of physical diagnosis rather
than a single auditable evidence chain. They provide rule-level judgments [4, 42], temporal localization [9,
88], measurement-grounded tests in controlled settings [73], and audio-physical or cross-modal consistency
checks [77, 92]. These capabilities are nevertheless typically organized as benchmark-specific protocols built
around curated datasets, predefined phenomena, or manually authored rubrics. The recent AV-Phys Agent is
a particularly close point of comparison: it combines a reasoning–action loop with deterministic acoustic tools,
but its released protocol remains tied to prompt-specific human-authored rubrics and multimodal-model binary
judgments [14]. The ball–wall schematic in Figure 1, which illustrates the interface rather than a recorded
execution, makes the resulting integration gap concrete: a defensible verdict must establish that the ball
and wall are present, localize floor- and wall-contact windows, measure trajectory and relative geometry, and
determine whether any detected impact sound aligns with the wall-contact window. Although audio events
can be detected in parallel, synchrony cannot be resolved until that visual window is available. Unusable
evidence leaves the dependent claim unknown; if no claim is contradicted, any unknown makes the clip abstain,
while a terminal infrastructure failure remains a separate outcome. The gap targeted here is therefore not the
absence of any one component, but their integration within a single evaluator that compiles the prompt into
typed physical obligations and a statically validated plan, lets observations gate and scope already-declared
specialist calls, and uses fixed rules to compose usable evidence records (typed measurements or explicitly
tagged learned states) into three-valued decisions with traceable time windows, tool outputs, values, rules,
and provenance.
VeriPhy addresses these requirements as a single physical-verification system comprised of a text-only planner,
a video-aware semantic verifier, frozen specialist operators, and fixed composition. For open-ended prompts
that provide no evaluation rubric, the planner operates before any frame is seen, compiling exact prompt
spans into typed physical obligations and a statically validated execution plan. For evidence distributed
across entities, events, time, and modalities, the verifier reads timestamped frames densely on a shared A/V
clock; its observations activate, skip, or localize only calls already declared by the plan, and those scoped calls
dispatch SAM 3 grounding and tracking [7], identity-based counting, eleven track-based physical measurements,
monocular depth, optical character recognition, and audio-event detection [24]. For heterogeneous or unusable
outputs, each action emits a claim-bound record containing either a typed measurement or an explicitly tagged


                                                                        2
learned base state, together with its realized scope, measured/abstained/errored status, artifact hashes, cost,
and provenance. Typed resolvers and fixed composition map usable records to supported, contradicted, or
unknown claim states and then to plausible, implausible, or abstain at clip level; unavailable evidence remains
unknown, while terminal infrastructure failures remain separate. For opaque verdicts, the system returns
an auditable claim-level trace linking each decision to its prompt span, planned calls, localized evidence,
and composition rule. Together, these components turn an open prompt and generated A/V clip into a
dependency-aware evidence chain rather than an unordered set of model answers. Figure 1 contrasts this
design with the evaluated question-decomposition baseline, which asks one closed yes/no question per claim
without a measurement trace.
To evaluate the critic at the granularity of its trace, we assemble a corpus of 1,500 generated clips with 2,582
human-written, prompt-grounded flaw records. Each record quotes the violated prompt span and provides a
rationale, severity, confidence, and, when available, a temporal span and object track; these records are the
only ground truth used here. A flaw-level protocol scores each system finding as whole, partial, or missed
against the corresponding human record. On a 149-clip recall analysis, VeriPhy accounts for 228 of 304
annotated defects, compared with 164 for a published question-decomposition evaluator given the same clips,
claims, and served model. A monolithic prompt to that same backbone accounts for 222, so recall alone
does not isolate the value of the agentic organization; the principal distinction is that every VeriPhy decision
retains its supporting evidence and provenance. This analysis is recall-only, single-annotator, and not held
out, and therefore characterizes the current system rather than its generalization (Section 5.3).
VeriPhy casts physically grounded generation of, and a verdict on, a clip V for its prompt p as two maps we
build and benchmark separately: a generation map V̂ ∼ Gen(p, C), the control-conditioned video diffusion
of Section 3, and an evaluation map Y = Crit(V, p), the auditable critic of Section 4. Both maps and the
clip-level verdict are made precise there.
In summary, our contributions are threefold: (i) VeriPhy, an integrated physical-verification system that
compiles prompts into typed obligations, scopes specialist operators with observations, and returns three-
valued decisions with localized evidence and provenance; (ii) the 1,500-clip corpus and its flaw-level matching
protocol; and (iii) a simulation-conditioned generation testbed in which known MuJoCo geometry is rendered
as depth or silhouette control for a frozen Wan 2.2-VACE generator [33, 70, 71]. The current report evaluates
the critic and generator separately. Together, these contributions provide an auditable evaluation stack and a
concrete interface for future physical refinement.


2    Related Work
Physics-aware generation and refinement. Controllable video generation separates appearance synthesis
from structural guidance by conditioning diffusion models on depth, segmentation, reference frames, masks,
motion fields, and compositional spatiotemporal signals [33, 71, 74, 87]. Such interfaces determine how
geometric information enters a generator, but do not by themselves establish that either the condition or
the synthesized pixels obey physical laws. A complementary line derives control from physical reasoning
or simulation: scene properties can be inferred and reconstructed for simulation, simulated trajectories or
flow can guide synthesis, textual physical context can refine a prompt, and language can be compiled into a
coarse motion plan. More recent research introduces continuous controls over physical properties or couples
simulation and rendering directly with generation [2, 19, 45, 54, 56, 80, 83, 86]. Evaluation feedback has also
been used for preference optimization, verifier-guided candidate search, and localized regeneration [20, 37, 44].
These studies pursue both pre-synthesis physical conditioning and evaluation-guided refinement. The present
work decouples these two stages: simulator-derived metric depth or silhouette controls condition a frozen
video generator, while VeriPhy independently evaluates the resulting clip. This design distinguishes adherence
to the control signal from physical validity in the synthesized output; feeding diagnoses back into regeneration
remains future work.

Model judgments, decomposition, and physical evaluation. Automated video evaluation has
progressed from aggregate metrics toward increasingly structured model judgments. General protocols
factor perceptual quality, temporal consistency, and prompt alignment, while learned VLM or MLLM


                                                       3
judges map a prompt and clip to multidimensional ratings, discrete states, or natural-language explana-
tions [26, 27, 31, 46, 47, 68]. Prompt-decomposition methods instead translate a prompt into propo-
sitions, questions, or query chains and revisit the visual input through smaller checks [10, 25, 28, 43];
the checks are explicit, although their supporting evidence is generally still produced by the judging
model. Physics-oriented benchmarks further introduce phenomenon-, rule-, trajectory-, and prompt-specific
criteria, criterion-level reasoning, failure localization, controlled measurements, and audiovisual consis-
tency [3, 4, 8, 9, 14, 22, 42, 49, 51, 55, 73, 77, 88, 92]. Prior physical evaluation is therefore not uniformly
scalar, unlocalized, visual-only, or unmeasured; rather, these capabilities remain distributed across evaluators
with different scopes, output contracts, and evidence representations.

Execution harnesses, context engineering, and persistent state. Execution harnesses separate
orchestration from model judgment by making planning, dependencies, specialist routing, observation scope,
validation, termination, and trace logging explicit [35, 60, 65, 78, 82]. Modular visual and video methods
extend this organization with specialized perception, selective observation, and adaptive temporal sampling
[13, 17, 23, 39, 52, 53, 67, 69, 75, 76], while video-evaluation pipelines already combine prompt structuring with
temporal tools, formal specifications and model checking, localized repair, deterministic acoustic measurements,
or prompt-specific rubrics [12, 14, 64, 84]. Across episodes, a harness also constructs the context for each
model call by storing, retrieving, filtering, and formatting persistent state; prior work distills trajectories
into reflective lessons, reusable strategies, or structured knowledge without weight updates, and separates
recorded evidence from derived beliefs to reduce context pollution [30, 36, 57, 66, 81, 90]. These components
predate our work, and controlled studies show that additional tools or scaffolding may increase cost without
improving accuracy [18, 34]. Relative to this literature, VeriPhy contributes their integration under a common
verification contract: open prompts are compiled into typed obligations and a validated plan, observations
only gate or scope declared calls, measurements remain distinct from learned states, and fixed rules produce
initial three-valued claims with any review override preserved separately in the trace. Across episodes, it
uses offline lessons from a disjoint experience pool and separately evaluates an evolving in-context lesson
state (Section B.7 and Section 5.3.4). The reported results therefore establish experience-conditioned harness
execution, not autonomous self-improvement or open-ended replanning; automatic changes to tools, workflows,
admission policies, and external knowledge remain future work.


3     Physics-Guided Simulation Pipeline
Modern generators render physically plausible motion, yet prompt-driven synthesis supplies no known physical
target: because physics and appearance are produced jointly, the intended trajectory, contact, or counterfactual
is neither fixed in advance nor recoverable afterward, and every physical property stays confounded with
appearance. An evaluation testbed instead needs a target factored out of appearance—specified, known by
construction, and auditable independently of generator capability. We obtain one from a trusted physics
solver and render it as a geometric control, so the solver fixes the motion while the prompt supplies only
appearance (Figure 2). This is developed across two stages: Section 3.2 turns the event description into a
validated target rendered as a registered control, and Section 3.3 conditions the generator on that control and
an appearance prompt. Whether the generated video realizes the target is the open question of Section 5.2.

3.1   Preliminaries
The atomic unit is a clip–prompt pair : a clip V = {(It , τt )}t∈TV , a time-ordered sequence of frames It
at timestamps τt with duration DV (Section 4), and a natural-language prompt p. The prompt supplies
appearance only (subject, material, setting), the geometric control C carrying the physical target—a solver-
rendered video with per-frame per-pixel depth intensity Ct (u) (Section 3.2); V̂ denotes a generated sample, V
any clip fed to the critic. Generation and evaluation are thus two maps over a clip and its prompt, built and
benchmarked separately,
                                    V̂ ∼ Gen(p, C)          Y = Crit(V, p),                                 (1)
where Gen samples a clip conditioned on p, C, a mask M and a scalar strength s—asserting no physical
fidelity—and Crit is the auditable critic VeriPhy of Section 4, returning the clip-level verdict Y (Equation (10)).



                                                        4
                                                                      t = 0.00
         Physics request                    Author scene
      “a ball bounces once”                 bodies, v0 , colliders      t = 0.38


                                                                          t = 0.75

          Revise scene                      Simulate & validate
                                                                             t = 1.12
           ≤ 3 tries                        check the path
                              fail
                                                                                 t = 1.50
                                                    pass

                                           Render control                          t = 2.00

                                     depth map from solver state
                                                                                     t = 2.81


                                                                                        t = 3.75
       Appearance prompt                   Generate video
         the look, apart                control + appearance

                                                                                        Depth control   Generated video


Figure 2 Physics-guided generation. A physics request becomes a scene that is simulated and validated, revising on
failure (red loop); the validated motion is a depth control that, with an appearance prompt, conditions the generator.
Right: depth control and generated clip at matched timestamps, tracing the ball’s path.

3.2     From specification to registered control
This stage produces the geometric control, validating the motion it carries before any control is rendered, so
the generator is conditioned on a verified trajectory rather than an unconstrained request. It is a three-map
chain from the event description pev to the control C,
                                                                      Render( · ; S)
                                                                                                                          (2)
                                            Author            Sim
                                     pev −−−−−−→ S −−−→ τ −−−−−−−−−→ C,

where Author prompts a language model to compile the text into a structured scene specification S (bodies,
initial states, colliders, static surfaces, and a camera; Figure 2), Sim runs the physics solver to a trajectory τ ,
and Render converts the solver state into the depth control C of Section 3.2. The middle map is gated by a
validation loop (Equation (3)) so only a τ meeting the event’s physical predicates is rendered; the three maps
are developed in turn below.
A body is simulated from its initial state when the engine determines the motion (a ballistic arc and its
contacts), while prescribed waypoints are reserved for externally actuated or explicitly counterfactual motion.
Validation applies to the simulated trajectory, not the specification text, through a conjunction of event-specific
predicates Φev : a ballistic segment must form an arc, satisfy the required hit or miss relation, settle when
requested, and remain visible. The Sim map is therefore a bounded revise-and-resimulate loop, Solve running
the solver to a trajectory and Summarize reducing it to a text report of its realized motion. Starting from
S (0) = S, for round k = 0, 1, 2,

                                     τ (k) = Solve S (k) ,
                                                        
                                                                                                               (3)
                                  S (k+1) = Author S (k) , Summarize(τ (k) ) ,
                                                                                


where the revision on the second line is taken only while ¬ Φev (τ (k) ): a failed predicate returns a summary
of the realized motion to the authoring model, which revises the specification, for at most three revisions
(four simulations). The first τ (k) with Φev (τ (k) ) true is the validated trajectory τ of (2), passed to Render;
exhausting the budget yields an explicitly marked unvalidated fallback rather than a validated scene.
The Render map turns the validated trajectory τ and its scene S into the control C. Rendered from solver
state rather than inferred from a generated video, C is registered to the intended motion by construction,
all streams sharing the scene’s frame clock (solver, camera, and playback settings deferred to Section 5.2.1).
For each of the clip’s T frames, rendering places S’s geometry at the per-frame pose, images it with the
scene camera, and reads a depth buffer Dt (u)—camera distance at pixel u in frame t—normalized to a
near-bright, far-dark intensity Ct (u) = 1 − clip (Dt (u) − d− )/(d+ − d− ), 0, 1 ∈ [0, 1], where d− , d+ are the
1st and 97th percentiles of the non-background depths pooled over the whole clip and clip clamps to [0, 1]; the
                   −1
control C = (Ct )Tt=0 then conditions the generator in Section 3.3. Background (Dt (u) beyond d+ ) maps to 0;


                                                                  5
pooling the percentiles once fixes the mapping so the same distance is the same intensity throughout, the cut
asymmetric because the far tail abuts the background and is dominated by depth-edge noise, with a small
Gaussian blur softening rasterized boundaries. When d+ > d− fails (as a result of no non-background pixels,
coincident percentiles, or a predeclared flat scene) Render falls back to a binary moving-body silhouette,
depth otherwise preferred for preserving both outline and distance ordering.

3.3   Physics-conditioned video generation
The generator is a latent video-diffusion transformer that samples a clip by iteratively denoising a latent from
noise. We use Wan 2.2 [71]: a DiT-style denoiser run along a flow-matching schedule of S UniPC multistep
iterations, indexed by i from high noise to low as σi decreases (Equation (14)). On its own it is a text-to-video
generator conditioned only on an appearance prompt p (subject, material, setting), with no input through
which a specified motion can be imposed.
To make the motion controllable we adopt VACE [33], which augments a frozen backbone with a control branch:
a control video and a generation mask are encoded into control features added into the backbone’s transformer
blocks, so an external spatiotemporal signal steers generation without retraining the base weights [74, 87].
The composite Wan 2.2-VACE takes four inputs: the appearance prompt p, a geometric control video C, a
generation mask M , and a scalar conditioning strength s.
                                                                                                             −1
We drive VACE’s control branch with the registered depth control of Section 3.2: C is the depth video (Ct )Tt=0
carrying the validated motion, and the mask decides which pixels VACE may synthesize. We set M all-white,
so every output pixel is generated and no pixel of the simulator render is copied in—the control acts only
through the branch, never by pasting appearance. The branch then injects, at each transformer layer ℓ and
                                                 (ℓ)
step i, an additive update to the hidden state hi ; with z ctrl the encoded control and W (ℓ) the branch’s
projection at layer ℓ,
                                         (ℓ)      (ℓ)
                                        hi ← hi + s W (ℓ) z ctrl ,                                           (4)
so the control enters as a strength-s residual rather than by overwriting pixels. The same s is applied at every
control layer and stays active throughout sampling in the deployed generator, lowered when the control covers
little of the frame. Conditioned on (p, C, M, s) with a fixed seed and a set of excluded terms, the backbone
induces a distribution over clips from which V̂ ∼ Gen(p, C) is drawn. It should be noted that this is just a
sample, asserting no physical fidelity.

3.4    Control withdrawal as a mechanism probe
When can the control be released? The injection of (4) runs throughout sampling, but if the trajectory settles
by some intermediate noise level the control is redundant afterward. Switching it off partway is awkward for
VACE’s additive residual, so we study the question on a separate Wan2.2-derived backbone whose control
path is easy to interrupt—a mechanism probe, not the deployed generator—and read the commitment point
back as a property of the Wan 2.2 diffusion prior both share. Run at 40 UniPC steps with flow shift 5.0, this
backbone has no trained control branch: its only conditioning path encodes a rendered source video into
context tokens concatenated with the text and image tokens, so withdrawal is directly available—the source
tokens are removed from the attended sequence at a chosen step, distinct from the additive-residual injection
of (4): over S steps the source tokens are present at step i iff i < i∗ , where i∗ = clip(round(f S), 0, S − 1) and
f ∈ [0, 1] is the withdrawal fraction. Steps before i∗ attend over the source tokens at the scale ω the deployed
recipe uses; from i∗ onward the sequence is identical to that of an unconditioned generation.
Because i∗ is an index, its noise level depends on the schedule, so the withdrawal point is reported as σrel = σi∗ ,
the level the flow-matching schedule assigns step i∗ (the shift-dependent map is (14) in Section A.2); two runs
at the same step index thus hit different noise levels whenever S or shift κ differs, which is why Section 5.2.3
indexes by σrel . Finally, the multistep solver forms each update from derivatives cached at previous steps,
which after a withdrawal still carry the removed tokens’ influence; the measurement compares one variant
that clears that history at i∗ against one that keeps it, otherwise identical.




                                                         6
4 VeriPhy
This section presents VeriPhy, an auditable multi-tool critic that adjudicates each generated clip against its
prompt, returning a three-valued verdict whose every decision traces back to the evidence that produced it.
We score the critic against the human-annotated flaw benchmark of Section 5.1 under the matching protocol
of Section 5.3.

4.1   System overview
VeriPhy is a constrained reason–act–observe critic with four roles. A text-only planner compiles the prompt
into typed physical claims and an executable measurement plan before seeing any frame (reason). Each
act step dispatches one of two backends: specialist instruments returning targeted measurements—counts,
tracks, masks, depths, text, and sound intervals—or a video-aware semantic verifier reading timestamped
frames densely for predicates like existence and event occurrence. Each observe step consumes the returned
measurement to gate, scope, and—via a deterministic aggregator —compose the plan’s declared physical
relations into a three-valued verdict. The governing invariant: tool outputs steer execution, but only within
obligations declared before any pixel is read. Backends are listed in Table 2; the planner and semantic verifier
may share a served checkpoint but are separate calls with different inputs and responsibilities. We situate this
design in the ReAct and tool-using-agent lineage in Section B.1.
Two properties make the critic auditable. First, reasoning sits entirely up front: the planner compiles
and statically validates the typed measurement plan before observing the video, following plan-before-act
agents [35, 78] and code-as-plan systems that emit an executable program of visual primitives [23, 69]. Planning
is thus global with respect to the prompt—the naming pass sees the whole prompt and later claim groups share
its vocabulary—while execution is local in time: observations activate, skip, or localize already-declared nodes.
With the trajectory fixed before execution, every measurement traces to the obligation that requested it.
Second, evidence production and adjudication stay separate: specialist operators return typed measurements,
learned semantic base states are tagged in their evidence records, and deterministic composition over the
usable records yields the verdict. These properties give a traceable evidence chain behind every three-valued
decision: supported, contradicted, or unknown. These states are surfaced as plausible, implausible, or abstain,
respectively, and formalized in Section 4.5.
We now fix notation for the objects these roles operate on. Recall the clip–prompt pair of Section 3.1; the
critic addresses frames and, when present, an audio track on the clip’s own container clock, writing the clip as
V = {(It , τt )}t∈TV over frame indices TV = {0, . . . , TV − 1} with ordered timestamps 0 ≤ τ0 < · · · < τTV −1 ≤
DV , where It is frame t, τt its timestamp, and DV the clip duration; separating index from time permits
nonuniform decode timestamps. From the prompt the planner produces exact prompt-grounded claims and a
surface plan,
                                                     Np
                             C(p) = {ci = (si , ϕi )}i=1 ,   si ⊑ p,     (C, Π)
                                                                             e = Πθ (p),                        (5)
where Πθ is the frozen planner, Πe the surface plan, Np the claim count, si a verbatim span of p, and ϕi its
checkable assertion; the relation si ⊑ p is enforced, not inferred after execution, and types belong to the
plan’s operations and checks rather than to a free-form claim label. Figure 17 summarizes the dataflow and
Algorithm 1 gives the same one-clip procedure as executable pseudocode.

4.2   Plan synthesis and static validation
This subsection expands the planner map Πθ of (5) into two stages producing the claim set C and surface
plan Π.
      e A first pass over the whole prompt fixes a shared namespace: a stable identifier for every distinct
entity and every separately asserted event occurrence. Claims are then partitioned into groups of at most four,
each planned independently against the full prompt and the shared names, with a group’s local identifiers
mechanically renamed into the shared namespace before the groups are concatenated. This shared-namespace
planning with rename-on-assembly prevents two groups from silently referring to the same entity by different
names, or to different occurrences by one name.
The surface language follows code-as-plan visual programming [23, 69], but is deliberately restricted to the
operations in Table 1. For claim ci , the planner writes check(ci, <expr>) with one operation or a conjunction


                                                        7
Surface operation                              Question posed                                          Typed check

judge("assertion")                             dense-frame semantic verification of the                general semantic
                                               complete assertion
exists("object")                               whether the object is visible at any decoded            existence
                                               time
eq(count("phrase"), N)                         whether measured cardinality equals N                   count
before(window(A), window(B))                   whether event A precedes event B                        temporal order
during(window(A), window(B))                   whether A is temporally contained in B                  temporal     contain-
                                                                                                       ment
rel("A||B", relation)                          a fixed-vocabulary spatial relation                     spatial
traj("phrase", relation, target)               a fixed-vocabulary motion predicate                     trajectory
sound("description")                           whether the audio track contains the event              audio occurrence
text("STRING", carrier=...)                    whether the named surface renders the string            rendered text

Table 1 The planner’s surface vocabulary. count and window are structural terms. The deterministic compiler expands
a surface operation into its required execution closure. Thus before adds occurrence gates and two timing actions;
rel adds co-visibility and mask actions and, for behind or in front of, depth actions. These dependencies need not be
written as extra surface operations, but they must be present in the compiled graph. A sound operation reads the
audio track; no audio track yields unknown, not a negative measurement.

of operations. At this stage the planner has no video input: the line states what evidence would settle the
claim, not whether the claim is true.
The assembled surface plan is validated as a whole, since its binding constraints are cross-references between
claims, checks, and actions (Equation (7)). A failing group may be re-asked with its own parser or type
complaints and a format restatement, but never with a suggested answer. After a fixed number of attempts,
an unusable claim falls back to direct semantic verification; this fallback is recorded and charged as a model
call, not a specialist measurement. A failed naming pass routes all claims through the same charged fallback,
so plan failure never makes a prompt appear cheaper by silently dropping claims.

Typed representation and static validation.     The compiler turns the surface program into a typed directed
graph
                      GΠ = (A, Q, E, b),      aj = (oj , αj , ωj , rj ),   b : Q → {1, . . . , Np }.                      (6)
Here A contains evidence-producing actions, including general semantic passes and specialist calls; Q contains
typed checks; E points from a prerequisite to its consumer; and b(q) = i binds check q to claim ci . An action
records its operation oj , arguments αj , declared scope policy ωj , and result type rj .
Before any action runs, the graph must satisfy

          Valid(GΠ ) = Parse(GΠ ) ∧ Refs(GΠ ) ∧ Typed(GΠ ) ∧ Acyclic(GΠ ) ∧ [∀i, ∃q ∈ Q : b(q) = i] .                     (7)

Parse checks that the surface program parses; Refs checks identifiers and dependency closure; Typed checks
operator arity, fixed relation vocabularies, and whether every check receives the result types it requires;
Acyclic checks that the dependency graph has no cycle. For example, a directed trajectory must carry a
target, and a depth-ordering check must consume both masks and depth. An invalid whole line falls back to
the general verifier; an invalid term can be replaced by a recorded generalist sub-check. In both cases the
substitution is charged and reported rather than guessed. Figure 18 in the appendix shows a compiled plan of
this form, with the dependency closure that (7) requires made explicit.

4.3     Timeline-conditioned multi-tool execution
Execution follows a topological order. Each action’s compiled scope function gj maps prerequisite records to
the full frame index set or a declared local subset, then calls the appropriate backend:

                                                                                                         (8)
                                                                                    
                          Ωj = gj ({Rk : (ak , aj ) ∈ E}, TV ) ,  Rj = Foj V|Ωj , αj .


                                                           8
 The plan line the planner wrote, before any frame is read
   check(c1, before(window("the first domino tips forward"),
                       window("the first domino triggers a chain reaction")))
 How one ordering check is carried out, left to right


   1 Plan                                2 Gate                                3 Measure                                    4 Decide
   reads the claim as an                 the verifier confirms                 event timing returns                         the predicate resolves
   ordering A ! B,                       both A and B occur                    one window per event:                        to a state, with
   carried with slack                    occurrence gates order                A = [1.62, 1.67] s                           ! supported
                                                                               B = [2.33, 7.96] s

          A: the first domino tips forward                                                             B: the first domino triggers a chain reaction
                      A [1.62, 1.67] s                                                   B [2.33, 7.96] s

         0                 1                 2               3             4                 5                  6                 7                  8
                                                                                                                                               seconds

                  0.60 s                 1.65 s A starts           2.33 s B starts                     5.00 s                         7.90 s




 How the order was decided: the slack is ± = 14 of the shorter window = 0.0125 s, and A is before B iff Aend ∙ Bstart + ±.
 1:67 ∙ 2:33 + 0:0125              ! holds, so the claim is supported. Otherwise the windows carry no order and it stays unresolved.


Figure 3 A real temporal trace. The planner writes the line before reading any frame. The verifier first confirms both
events, the timing actions then return WA = [1.62, 1.67] s and WB = [2.33, 7.96] s, and (13) resolves their order. Every
number and displayed frame comes from the recorded run.

Here Foj is the frozen backend implementing operation oj on the scoped video V|Ωj with typed arguments
αj ; the scope function is part of the validated program. A usable measured window is padded, given a
minimum duration, and converted to the explicit indices whose timestamps fall inside it; a missing, invalid,
or overly broad window falls back to the whole clip—a conservative fallback that avoids reading failure to
localize as evidence that the requested event or relation is absent. The backend behind each capability, with
its returned object and exact frozen model, size, and license, is listed in Table 2. Three sub-checks remain
learned, resisting full symbolization—subtype identity, dense action-event recall, and depth-ordered spatial
interpretation on localized evidence—and their outputs carry a learned base-predicate tag distinguishing
them from deterministic consequences of a measurement, so no holistic scorer appears in the verdict path.
Two actions share one execution only when their complete realized signatures match—clip identity, operation
oj , typed arguments αj , references rj , and realized scope Ωj —and the executor calls each equivalence class
once, following exact common-subexpression reuse [59, 62]; because the realized scope is part of the signature,
whole-clip and localized requests never merge merely because their natural-language queries are similar.
Timing is the one capability needing a guard before its windows are used: a returned window is not evidence
the queried event occurred, since a forced localizer may return its best candidate even for an absent event.
Visible events are thus confirmed first by the dense-frame semantic verifier, audible events on the audio track,
and only supported occurrences let their intervals enter a temporal predicate. Writing the sub-check states
over the three-valued codomain V = {S, C, U} (supported, contradicted, unknown; Section 4.5), a relation
R ∈ {before, during} over occurrence states oA , oB and measured windows WA , WB resolves to contradicted
if either operand is contradicted, to unknown if either is unknown or a window is unavailable, and to the
order predicate ρR (WA , WB ) only when both events are supported—so timing may compose an order but
never establish occurrence. That predicate ρR compares interval endpoints under a boundary slack of one
quarter of the shorter window (Equation (13) in Section A.1): an order is supported or contradicted only
when one window ends before the other begins by more than the slack, otherwise U; the quarter-window rule
prevents both directions from holding. Containment (during) uses the same slack. These predicates are a
tolerance-scaled subset of Allen’s interval algebra [1]. Figure 3 traces one such ordering through a recorded
run, from the plan line written before any frame was read to the two measured windows that settle it.




                                                                       9
4.4   Physical measurements and evidence records
Physical claims are settled by eleven operations sharing one grounding step: SAM 3 segments the named
subject and tracks its identity across frames, and every operation measures over those tracks. Each maps to a
class of human complaint in the corpus.
The largest class is displacement: the dominant complaint is that something the prompt sets in motion does
not move or moves the wrong way (e.g. a static sun), with ballistic arcs comparatively rare. Three conventions
make it measurable: it is reported in multiples of the subject’s own radius, so no scene calibration is needed;
direction is taken from the furthest excursion, not the net, since a rise then fall cancels; and camera motion is
removed by dense whole-frame optical flow, needing no stationary landmark. Three further operations cover
failures with no net travel: contact measures the closest approach between two tracked masks (finer than
box overlap); shape change measures surface motion relative to the background flow (a scroll rolling in place,
which displacement reports as zero); and path shape distinguishes a circle from a figure of eight. The rest
cover time and existence: permanence, whether a subject that should vanish persists; hop counting, whether
one that should leave the ground does; damping, a spinning object that never slows; onset ordering, which of
two events comes first (or never happens); clip timing for duration and playback rate; and viewpoint motion,
separating a moving camera from a moving subject.
All eleven return a number with its evidence—frames read, tracker used, threshold applied—leaving the
decision to Section 4.5. Each may also abstain: a subject under one percent of the frame, or a track too short
to measure, yields an explicit abstention, so an unmeasurable claim never resolves as supported.

Evidence records and provenance.        Each action is serialized as a claim-bound record

                                                                                                              (9)
                                                              
             Rj,i = id(V), p, si , oj , Ωj , σj , µj , hj , κj , σj ∈ {measured, abstained, errored}.

The payload µj contains either a typed measurement or an explicitly tagged learned base state; hj contains
the native-output and artifact hashes; and κj contains calls and accelerator time, with optional wall time,
price, and token counts. Shared execution may bind the same record to several claims, but its cost is charged
once by execution identifier.
The three statuses are mutually exclusive: measured carries a payload and no abstention or error; abstained
carries a reason and no payload; errored carries an infrastructure message. A valid negative measurement—a
complete usable track lacking the requested motion—stays measured and may contradict a claim, whereas
failure to track from blur, occlusion, low quality, or an instrument refusal is abstained, not a negative
observation. The counting path can blur this: the mode of an intermittently grounded per-frame series
can report a confident zero when grounding merely failed on most frames, indistinguishable from a true
absence—hence the auxiliary fields (stable, range, frames read) are load-bearing, and Section 7 flags the
consequence for count-derived figures. A terminal errored record is retried; if still terminal, we mark the clip
⊥infra and exclude it from the evaluation set rather than relabeling it unknown.
Specialist schemas reject judgment-shaped fields, nonfinite numbers, duplicate keys, and noncanonical payloads;
every record carries the full prompt and verbatim span si , with heavy artifacts content-addressed by path and
byte hash. This guarantees a specialist cannot emit the final prompt-satisfaction label and that accepted
evidence is attributable and replayable—though it cannot unbias a learned measurement nor detect a
well-formed but wrong payload.

4.5   Verdict aggregation and diagnostics
A deterministic roll-up composes per-sub-check states into per-claim states and then the clip decision
(Equation (10)); two learned refinements then act on top of it, and the run emits a localized contradiction packet
(Equation (11)) as its diagnostic interface. For a completed trace, every sub-check resolves in V = {S, C, U},
standing for supported, contradicted, and unknown. A typed resolver ψq maps the measurements µj of its
prerequisite actions Pa(q) in GΠ to a sub-check state zq : when all required actions are measured it applies
ψq ; if any abstained or returned no usable evidence the state is U; and a terminal infrastructure error gives
⊥infra . The resolver is deterministic for count, timing, track, transcription, and other explicit predicates, and
learned only for the semantic sub-checks named above, where it uses an asymmetric gate: it may contradict


                                                       10
only when a positively contradicting feature is visible, so that unresolved evidence, unparseable output, or
a missing modality yields U rather than turning an instrument failure into an accusation about the video.
Negation is applied to the positive sub-check state, never by asking a tool to measure a negative quantity:
¬3 S = C, ¬3 C = S, and ¬3 U = U. Let Ki = {q ∈ Q : b(q) = i} be the validated checks for claim ci , after
applying this negation where required. Claim and clip composition are

                                                           the trace terminates with an infrastructure error,
                                       
                                       ⊥infra ,
      
        C,  ∃q ∈ K   : z  = C,
                                       
      
                  i    q              
                                       Implausible, ∃i : y = C,
                                                                i
 yi = S, ∀q ∈ Ki : zq = S,        Y =
                                       Plausible,         N p ≥  1 ∧ ∀i : yi = S,
        U, otherwise,
      
                                      
                                       
                                                           otherwise.
                                       
                                         Abstain,
                                                                                                          (10)
One contradiction makes the clip implausible, and Plausible asserts only over the claims the plan executed.
Those two refinements are as follows. First, a stronger reviewing model re-examines claims the video-aware
verifier passed, and its verdict stands: overruling a pass resolves the claim to contradicted rather than
unknown, replacing yi where the sub-checks would otherwise roll up to S. Both verdicts are recorded, so a row
can be re-scored on the first verifier’s alone. The direction is asymmetric by design: the reviewer examines
only passed claims, never a specialist measurement, which carries evidence a second opinion cannot inspect.
Second, a recognition engine reads frames directly to settle text claims: a generative model asked what a
sign says repairs what it sees—rendering a malformed Stly your as the well-formed Style your the prompt
requested, concealing the defect under test—whereas a recognition head returns the malformed string, which a
deterministic comparison rejects. It reads every frame rather than a sampled fraction, since a caption present
for part of a clip can fall between samples, and each record states the frames read.
Beyond the clip state Y , a run emits a localized contradiction packet

                                                                                                           (11)
                                                                 
                                 F(p, V) = ci , {Rj,i }j , Ωi , Bi : yi = C ,

where Ωi is the union of available temporal support and Bi contains available box tracks or masks. The packet
is assembled from the trace that produced the verdict, so each contradicted claim carries both the evidence
records behind the conclusion and the region of the clip in which the failure occurs: what failed, on what
evidence, and where. That space–time localization is what Section B maps onto a local edit of the generator
control (Section B.4, (21)). Closed-loop refinement is not run in this report: (11) defines the interface only,
the critic and simulation-conditioned generator are evaluated on disjoint data, and no VeriPhy packet has
been used for preference optimization, denoising guidance, candidate selection, or localized regeneration—so
we claim no clip has been made more physically correct by the critic.


5     Experiments
This section evaluates the system in the order the pipeline builds it. Section 5.1 sets out the shared setup—the
human-annotated flaw benchmark and the recall metrics and matching protocol every result is scored under.
Section 5.2 takes the physics-guided generator : whether the geometric control governs the motion, when the
trajectory commits, and how far the scene library reaches. Section 5.3 takes the VeriPhy critic: its flaw recall
on the evaluation core, against the annotated reference and published evaluators, and its agreement with
human ratings. Section 5.4 takes the context-training self-evolution of the critic—whether lessons distilled
from recorded misses raise recall without touching a weight—and Section 5.5 closes the critic’s outward
channel, feeding a verdict back as a prompt rewrite that regenerates the clip. The evaluations use distinct
held-out settings that should not be conflated; Section 5.6 sets them side by side.

5.1   Experimental setup
This setup—models, benchmark, and matching protocol—is shared by both systems; each system’s own
configuration accompanies its results.




                                                      11
Capability (model)                               Running backend                       Returned object

Planner (Qwen3-VL-30B-A3B, 31 B) [58]            prompt compiled pre-frame             claims and a typed plan
Semantic predicate (Qwen3-VL)                    dense timestamped pass                learned base state, rationale
Event timing (Qwen3-VL)                          over timestamped frames               interval, absence, or refusal
Fallback verify (gpt-5.6-sol)                    on a claim the dense pass passed      three-valued state, both kept
Grounding, masks (SAM 3, 0.9 B) [7]              SAM 3 Video, persistent IDs           per-frame masks, tracked IDs
Object count (SAM 3)                             cardinality of SAM 3 IDs              count, per-frame series
Physical measurement (TAPNext++) [91]            11 typed operations over tracks       typed measurement, evidence
Depth ordering (SenseNova-7B-MoT)                depth model on localized evidence     behind / in-front ordering
Camera cancellation (from tracks)                dense optical flow subtracted         subject-relative displacement
Rendered text (PaddleOCR PP-OCRv5)               OCR head + EasyOCR fallback           literal glyph transcription
Audio (FlexSED) [24]                             sound-event detection                 sound intervals on the track

Table 2 Execution backends and the frozen specialist behind each capability, for the evaluated run: each row names a
capability with the model or checkpoint that runs it (with its parameter count where published), the backend it runs,
and the object it returns. SAM 3 supplies grounding, masks, and counting, while TAPNext++ supplies the tracks
the eleven typed operations (Section 4.4) are taken over; the two learned components (semantic predicate and depth
ordering) and the fallback verifier are the only backends that may resolve a claim, and no holistic video-quality model
produces the clip decision. Every component is frozen at the listed revision for all reported results, and gpt-5.6-sol is a
closed model (SenseNova SOL) served through an internal proxy. All released components are under permissive licenses
(Apache-2.0, MIT, or Meta’s SAM license) except the depth-ordering model, which is CC-BY-NC-4.0 (non-commercial).

Models and specialists. The critic runs one served vision-language model for both its text-only planner and
its video-aware semantic verifier—Qwen3-VL-30B-A3B-Instruct [58], in BF16 without quantization—together
with a frozen stack of low-level specialists, one per capability: SAM 3 [7], TAPNext++ [91], a depth model,
PaddleOCR, and FlexSED [24], with a closed model as the fallback verifier. Table 2 lists, for each capability,
the backend that runs it and the object it returns, together with the exact checkpoint, size, and license; every
component is frozen at the listed revision for all reported results.

5.1.1   Benchmark

The benchmark is a corpus of 1,500 AI-generated clips: a person watched each against its prompt and recorded
every place the video failed to deliver what the text asked. The generating model is not recorded, no clip is
attributed to a specific system, and the human-written fields are ground truth throughout. Each flaw is a
localized record with four always-present fields—the violated fragment, a free-text rationale, a severity, and the
annotator’s confidence—and two optional, a time span and a box track. Two grouping tags—a modality tag
(seen, heard, or both) and a ten-item type tag—are machine-assigned by majority of three zero-temperature
model votes and never treated as ground truth. Section A.5 gives per-field coverage, the per-type breakdown,
and timing distributions.
Three recorded stages (Figure 20 in Section A.5) narrow the 1,500 clips and 2,582 flaws to the evaluation
set: clip selection keeps retrievable, dynamic clips; flaw selection keeps only “seen”- or “both”-tagged flaws
a pixel-only critic could find, leaving 1,107. A deterministic seeded procedure, stratified by severity, flaw
count, and duration, draws the frozen core—150 clips and 306 flaws (a 29-clip continuity stratum exempt
from replacement); a separate pool of 711 clips is held disjoint from both frozen sets for learning. The core is
an optimization set, so results on it measure fit to that core. One clip produced no measurement, so recall is
reported over 149 clips and their 304 flaw entries, never the full 306—the two excluded rather than counted as
missed, making the reported rate very slightly optimistic.
Unlike clip-level resources—Physion-Eval [88], VideoPhy-2 [4], and per-dimension suites such as VBench [31]
and T2V-CompBench [68]—our corpus ties each failure to the exact prompt words with an optional time span
and box track, so an allegation can be matched to a particular annotated failure rather than only correlated
with a clip-level score. This localization does not improve reliability: our corpus is single-annotator and
contains only flawed clips, whereas VideoPhy-2 provides redundant judgments and majority resolution.



                                                            12
5.1.2   Reference standard and matching protocol

The evaluation core is the reference standard: its 149 clips carry 304 annotated flaws—the denominator for
all core recall analyses. Because every clip carries at least one flaw, recall is directly measurable but precision
is not (a detector flagging everything scores perfect recall), so we report recall alongside the rate at which
accusations land on a real flaw. Recall counts flaw entries, not distinct spans, since matching claims each
entry at most once. Matching, run after critic inference, cannot affect the critic’s outputs. The comparison
unit is a sentence pair (annotator vs. critic), judged by meaning as a whole match (same defect), a partial
match (critic identifies at least one aspect of a compound annotated defect), or a non-match. Whole and
partial pairings are candidate edges for maximum bipartite matching, each finding and flaw used at most
once; every flaw is then reported as whole, partial, or missed. The matching judge, distinct from all evaluated
components, votes at temperature zero with a retry-and-refallback rule and aborts rather than reporting a
number if more than 2% of flaws yield no usable outcome.

5.2     The physics-guided generator
Three questions organize the generator experiments: whether the geometric control overrides prompt-implied
motion (Section 5.2.2), when a conditioned trajectory becomes insensitive to control withdrawal (Section 5.2.3),
and how the pipeline behaves beyond single-body probes (Section 5.2.4). The first and third use the deployed
generator; the release analysis is a separate mechanism probe on the second backbone, its withdrawal operation
defined in Section 3.4.

5.2.1   Setup: from simulation to a controllable clip

The deployed backbone is Wan 2.2-VACE-Fun-14B (WanVACEPipeline, fixed negative prompt, no appearance
reference, deterministic sampling from the recorded seed). Scenes are simulated in MuJoCo and rendered
to 81 frames at 16 fps; as the simulated duration varies, this render clock stretches playback by 1.8×–2.3×,
so trajectory shape and event order come from the simulation but absolute speed does not equal simulator
time. Generation is staged—controls rendered first, a 1.3B checkpoint screening each scene once, visibly
degenerate outputs not queued for the 14B model (a pipeline rule, not a generator property). Surviving scenes
are generated in bf16 at 848 × 480 with UniPC at 50 steps and guidance 5.0, conditioned on the control video
(globally normalized MuJoCo depth, or a silhouette for predeclared flat-scene templates), an all-white mask,
and the prompt; the conditioning scale is s = 1.0 deployed, examined separately at {0.5, 0.8, 1.0}.

5.2.2   Control fidelity under prompt variation

We fix the geometric control—one projectile-depth video—and vary only the motion clause across three
prompts sharing subject, scene, camera, material and style: a strong horizontal traverse, a neutral one, or one
adversarial to the control (drops nearly straight down, almost no sideways motion). Each runs under three
regimes—no control, control over the first 10 of 50 steps, control throughout—at three seeds (partial), two
(unconditioned), one (full). We track horizontal travel (fraction of frame width) in the finished clip; metric
and decision rules were registered before generation.
The two inputs cross over (Figure 4). Without a control the prompt sets the motion: the clause-attributable
range is 0.875 against 0.252 between seeds. The unconditioned clips also differ in framing—median tracked
ball area 8,846 pixels against 211 under the control—so travel-fraction is not comparable across regimes, and
within-regime comparisons carry the argument. With the control throughout, the clause-attributable range
falls to 0.001; in between, with the control over the first fifth of sampling then withdrawn, the two sources
swap: clause range 0.060 against a seed range of 0.427.
The trajectories locate the shortfall (Figure 4). A clip conditioned over the first ten steps tracks the control’s
arc through the flight and departs only at the landing, stopping near 0.77 of the frame while the control’s ball
rolls on to 0.99: the lost travel is the post-contact roll, not a different flight—the same phase Section 5.2.3
finds most sensitive to early withdrawal. Of the three clauses at this seed, two follow the control from the
first frames and the neutral one does not, staying a mean 0.243 of the frame from the control’s path over the
first ten frames. The control-set trajectory thus persists through the text-only steps.



                                                        13
 Where the ball actually went: the same depth control video in all nine clips, seed 42

                                                              Control                               Control on the                Control on
                                                              never applied                         first 10 of 50 steps          all 50 steps
                                                         0
 "The ball starts at the far left,
 travels quickly from left to right
 across the entire frame, lands                         0.5
 near the far right, and continues
 rolling to the right."
                                                         1        0.97                                                     0.64                        0.87
                                                         0

                                       down the frame
 "The ball flies in an arc through
 the air and then bounces on the                        0.5
 grass."

                                                         1                              0.86                               0.62                        0.87
                                                         0
 "The ball drops nearly straight
 down near the centre of the frame
                                                        0.5
 and bounces in place with almost
 no sideways motion."
                                                         1                              0.05                             0.64                          0.87
                                                              0             0.5                1    0           0.5           1   0              0.5          1
                                                                                                         across the frame


        the control video's own ball                              frame 0 of the clip              frame 80



Figure 4 Tracked ball path in nine clips at one seed, against the same depth control throughout. Each box is a single
848 × 480 frame, x left to right and y downward; each dot is one frame, sized by the tracked region’s area and shaded
from first frame to last. The pale band is the control video’s ball, in frame for 63 of its 81 frames; the number in each
box is that clip’s sideways travel. The three prompts differ only in the closing sentence beside each row; the red row
asks for the motion the control does not perform. Without the control the path follows the clause and the framing
shifts with it; with the control throughout, all three clauses reproduce its arc; with the control over the first ten steps
the path holds the arc and departs at the landing.

5.2.3   Trajectory commitment under control withdrawal

Moving the withdrawal point locates the noise level at which the simulated trajectory becomes fixed. The
withdrawal operation, its second backbone, σrel , and the two variants clearing or keeping the solver’s cached
derivatives are defined in Section 3.4 (Equation (14)). Scenes are one moving rigid body with a closed-form
trajectory (one of three yields only five post-contact frames, so its comparisons rest on two), one schedule
setting per seed. Since noise falls during sampling, a high σrel withdraws early, leaving later steps unconditioned;
a clip still following the simulation afterward was fixed before removal, and the earliest such withdrawal marks
the commitment point. Three runs probe seed variability (16 seeds, one point), transition shape (six points,
one seed), and measurement dependence (a denser sweep re-scored with an independent tracker).

Metrics. Each run pairs against a σrel = 0 run sharing simulation, control, prompt, sampler, and seed,
both tracked frame by frame (by colour, except the third run’s segmentation tracker). Retention, the per-axis
Pearson correlation between generated and control paths (Section A.3), is scored separately over airborne and
after-contact windows split at the ground-contact frame tc ; near 1 means the object moved as simulated, and
the split localises disagreements a whole-clip value hides. Two prefixed failure counts accompany it: whole-clip
disagreement (full-clip horizontal < 0.7) and late-window disagreement (whole-clip horizontal < 0.7 while
airborne horizontal > 0.9).

Airborne and after-contact agreement under an early release. The first run fixes release at σ = 0.952
over two scenes, 16 seeds each, both variants, against the never-released baseline: 96 clips, 16 per cell. Releasing
at σ = 0.952 leaves the thrown ball’s airborne flight intact—per-seed horizontal agreement drops 0.003 versus


                                                                                        14
                1
             0.99
                                                                                                         across frame, airborne
                                                                                                         across frame, after contact
              0.9                                                                                        up/down, airborne
retention




                                                                                                         up/down, after contact
                                                                                                         control never released
              0.5
                         runs opposite                                                                   expert switch (¾ 0.875)
                0        to the simulation                                                               commitment band 0.94--0.96
            ¡0:63 Ball thrown across a field    Ball dropped onto a floor      Ball rolling off a ramp
                    0.95
                        0
                        3

                               3


                                         6

                                               0.95
                                                   0
                                                   3

                                                            3


                                                                      6

                                                                            0.95
                                                                                0
                                                                                3

                                                                                           3


                                                                                                     6
                    0.9

                    0.8

                              0.7


                                       0.5

                                               0.9

                                               0.8

                                                          0.7


                                                                    0.5

                                                                            0.9

                                                                            0.8

                                                                                         0.7


                                                                                                   0.5
                                      noise level at which the control was released

  Figure 5 The release-point sweep: one clip per point, three scenes (including a ball rolling off a ramp), scored separately
  over the airborne window and the window after the simulated object first reaches the ground. The horizontal axis is
  the noise level at which the control was switched off, high noise on the left. Colour marks the window (blue airborne,
  rose after contact) and line style the axis (solid across-frame, dashed up/down); retention is the correlation between the
  generated object’s tracked path and the simulation’s, defined in the text. The thrown ball’s after-contact agreement
  falls below the threshold in both directions at the earliest withdrawal, and the vertical component is the later of the
  two to recover. Guides mark the commitment band and the backbone’s expert switch; the grey band marks the region
  below the 0.7 threshold fixed before scoring.

  never releasing (95% CI 0.001 to 0.004, n = 16 paired seeds)—while whole-clip horizontal falls 0.13 (95% CI
  −0.02 to 0.28) and vertical 0.18 (95% CI 0.07 to 0.29). The disturbance is confined to post-contact motion,
  where horizontal runs opposite to the simulation on 9 of 16 seeds at σ = 0.952 versus 0 of 16 when never
  released. Whole-clip disagreements number 3 of 16 against 1 of 16, late-window 2 of 16 against 0 of 16.
  Sweeping six points on one seed across three scenes traces retention against noise level (Figure 5). For the
  thrown ball, σ = 0.952 gives after-contact horizontal −0.63 (opposite to the simulation) with airborne still
  1.00; σ = 0.903 or later restores after-contact to 0.98+ through the latest release, σ = 0.555. A dropped ball
  stays above threshold everywhere: after-contact horizontal is 1.00 throughout, and vertical—the informative
  axis—is lowest at 0.78 (σ = 0.952), rising to 0.99+ from σ = 0.903. A ball off a ramp stays at 0.99+ in both
  axes. A third run (three thrown-ball points, three seeds, two guidance settings, 18 clips, segmentation tracker)
  reproduces the direction: airborne horizontal 1.00 (mean over 6 clips at σ = 0.952, 95% CI 0.998–1.000) while
  after-contact horizontal averages 0.69 over an interval spanning zero (−0.04 to 1.43, n = 6), recovering to 0.99
  and 1.00 at σ = 0.903 and 0.833; at the latest point the tracker finds no object on 3 of 6 clips (low-contrast
  ball on grass), excluded, widening that interval.
 Across runs the trajectory stops responding to control removal in a narrow band, σ ≈ 0.94–0.96. Under
 (14) at S = 40, κ = 5.0 this sits in the high-noise portion of sampling, consistent with the critical-window
 account [5, 40, 61] and above the backbone’s expert switch at timestep 0.875 N [16], so motion is fixed before the
 handoff; we report noise level not step index because changing S or κ moves the step but not the level [11, 50].
 The two components do not fix together: on the thrown ball, σ = 0.9522 drops after-contact agreement below
 threshold in both coordinates (−0.632 horizontal, +0.016 vertical); one point later (σ = 0.9025) horizontal
 recovers to +0.981 while vertical is still +0.260, not reaching +0.894 until σ = 0.8331; the dropped ball
 shows the same ordering, so a schedule set by horizontal alone would be too early. (Whole-clip the ordering
 reverses—vertical +0.986 against horizontal +0.421—as the large flight excursion dominates the correlation
 and hides the rebound.)
  The failure is specific: flight is reproduced, post-contact behaviour is not. Contacts are a documented failure
  mode of video generators [3], traced to a weak contact prior; where the prior is weak the control must stay
  present to override it, so applied throughout it reproduces the contact on every seed and the reversal appears
  only under early withdrawal. Clearing the cached derivatives changes the whole-clip result by at most 0.04
  horizontally (95% CI −0.04 to 0.13, n = 16), the largest per-seed difference on any window or direction.



                                                                          15
 Bouncing ball


 Simulated
 depth control



 Generated
 video

                       t = 0.00 s          t = 0.50 s           t = 0.75 s          t = 0.94 s           t = 1.19 s

 Ball thrown across a field


 Simulated
 depth control



 Generated
 video

                       t = 0.00 s          t = 1.06 s           t = 1.62 s          t = 2.25 s           t = 2.56 s

Figure 6 The same mechanism across two scenes with very different requested appearance—an indoor studio and an
outdoor field—each shown as its depth control above and the resulting generated clip below. Timestamps are per scene,
chosen from the turning points of its tracked vertical path, so each column falls within a moving interval. Appearance
changes completely with the prompt while the motion stays the simulation’s: for the thrown ball the generated and
control paths agree to a correlation of 1.0000 horizontally and 0.9998 vertically, with a median disagreement of 0.7
pixels across and 1.1 pixels down, over the 63 frames in which the ball is measurable in both before it leaves the frame.

5.2.4   Scene-library breadth and failure boundaries

The same authoring, simulation and conditioning path scales beyond the single-body probes, producing 1,314
scenes across 66 kinds (a kind is a template, a scene one parameter setting, simulated and generated once);
591 of 652 simulations passed a pre-render inspection of simulator output, not generated clips, judged to show
the intended behaviour clearly enough to generate from. Figure 7 shows twelve kinds as generated frames at
body counts up to 34, and Figure 8 three as depth control and generated clip at matched timestamps.
Fidelity does not extend uniformly. Assessed by manual inspection with the colour tracker of Section 5.2.3,
single-object scenes reproduce the simulated trajectory throughout (Figure 6), but a multi-object interaction
such as a billiards break does not—neither the deployed backbone nor the alternates produced a collision in
which every body moved as specified—and its commitment point is unmeasured, the colour tracker being
unable to follow a scatter as one path. The same rigid-body engine produces every scene, deformable
and granular kinds built from its particle-and-link primitives (springs, linked segments, contacting bodies,
buoyancy), so the library excludes fluid, smoke and finite-element soft-body solves.

5.3     The VeriPhy critic
The benchmark and metrics are in Section 5.1; this subsection reports the critic’s recall on the evaluation
core, broken down by clip property and specialist trace. How the settings here read together is deferred to
Section 5.6.

Implementation and cost. The served Qwen3-VL model (Section 5.1) runs with tensor parallelism across
two GPUs. Planner and verifier are separate calls: the planner sees the prompt and claim state but no
frames, the verifier sees densely decoded, timestamped frames and one declared predicate. Every measurement
uses the logged dense-input path with the frozen target, BF16 inference, and pinned tool revisions. Since a
detector, a tracker, and a full vision-language judgement differ in cost, cost is reported as model and tool calls


                                                           16
 One frame of the generated video per scene, at the point half the clip's motion has happened.




 Cloth draped over a cylinder    Cloth falling, crumpling         Flag rippling in wind          Rope swinging, whipping
 particle sheet                  particle sheet                   pinned particle sheet          linked segments




 Chain hanging, swinging         Grains pouring in a heap         Grains draining a funnel       Ball into a pit of balls
 linked segments                 34 small bodies                  30 small bodies                9 bodies in contact




 Loaded boat stays afloat        Cluster down a slope             Dominoes toppling in turn      Linkage swinging chaotically
 buoyancy force                  6 bodies on a ramp               20 rigid slabs                 two jointed arms


Figure 7 Twelve of the 66 scene kinds, one generated frame each. Each tile is selected by rule: frame-to-frame change is
accumulated over the clip and the tile is the frame by which half the total has occurred, which falls during the scene’s
principal motion rather than its start. The second caption line names the physics primitive, and every body count in it
is the scene’s own parameter. Each clip’s simulation passed the inspection described in the text, and the tiles were
additionally inspected manually.

per clip rather than wall-clock time, and uncertainty by resampling whole clips, since two flaws in one clip are
not independent.

Planner validity. Inspected before end-to-end evaluation without video or tool access, the prompt-only
planner produced a valid, compilable plan for all 233 claims of 22 annotated clips (one or two calls per clip);
27 claims (11.6%) carried a specialist action surviving validation, against 2.3% under an earlier tabular format.
On diagnostic sets requiring quantitative measurement the routing rate was 19/30 across counting, spatial,
and ordering claims and 10/10 for synthetic counting prompts—tests of routing and syntax, not verdict
accuracy. The supported vocabulary lacks an “on top of” predicate and rejects negated measurements; such
claims fall back to the generalist verifier.

5.3.1   Flaw recall on the evaluation core

Headline recall. Over the 149 core clips and their 304 human-annotated flaws, VeriPhy finds 228 (75.0%)
under Section 5.1.2—191 whole, 37 partial—and finds every annotated flaw on 91 of the 149 clips. Two
components drive matches: the fallback verifier gpt-5.6-sol overrode a dense-verifier pass to contradiction on
83 of the 228, and the on-screen-text recognizer transcribes malformed glyphs literally rather than normalizing
them, so string comparison catches garbled text.

Versus published evaluators. We compare VeriPhy against defect-localizing evaluators—question-
decomposition and scene-graph methods (per-question answers linkable to claims) and free-text evaluators
(unstructured flaw lists)—and test whether CLIPScore tracks aggregate clip properties. Modular video QA is
context-only, not evaluated; clip-level agreement with human ratings is deferred to Table 4.


                                                                17
 Cloth falling and draping over a cylinder


 Simulated
 depth control



 Generated
 video


                       t = 0.00 s            t = 0.94 s        t = 1.44 s                                                                t = 3.19 s                            t = 5.00 s

 Rope swinging from a fixed anchor


 Simulated
 depth control



 Generated
 video


                       t = 0.00 s            t = 1.19 s        t = 2.38 s                                                                t = 3.62 s                            t = 5.00 s

 Grains draining through a funnel


 Simulated
 depth control



 Generated
 video


                       t = 0.00 s            t = 1.19 s        t = 2.31 s                                                                t = 3.44 s                            t = 5.00 s

Figure 8 Three deformable and granular scenes, each with simulated depth control above and generated clip below, at
matched timestamps. Columns are placed at equal steps of the clip’s accumulated change, so none falls in a temporally
static interval. Pairs are shown only for scenes whose depth control remains distinguishable from its background in
every column; an object that settles onto the floor takes the same grey as the floor and leaves the control blank.
                                                                                                          Recall against cost per clip
The same served model—single-pass over the prompt
                                                                                                    80
                                                                                                          up and to the left is better
                                                                                                                                         VeriPhy 75.0%
and every frame, no planning, tools, or per-claim                                                   75
                                                                 localized-flaw recall (%) of 304




                                                                                                                  Single-pass VLM 73.0%
verification—matches 222 of the 304 flaws at one call                                               70
per clip; Figure 9 reports it separately, since free-text                                           65
lists are prompt-sensitive with no per-verdict evidence.                                            60

Question decomposition matches 164 of the 304 flaws                                                 55                                                               Scene graph 53.0%

(53.9%)—125 whole, 39 partial—versus VeriPhy’s 228,                                                 50                            Question decomp. 53.9%
on the same 149 densely-read clips and model (identical
                                                                                                             0              10              20           30             40          50
claim lists on 148). It asks one closed question per                                                                                 mean model / tool calls per clip
                                                                                                         Modular video QA: not evaluated under this protocol
claim and accepts the answer, whereas VeriPhy plans                                                      VeriPhy (localized, evidence-carrying)        per-question (structured)     free-text flaw list
measurements and may run several checks per claim.
Higher recall is not a higher per-finding match rate:          Figure 9 Localized flaw recall vs. cost per evaluator,
29% of its 557 findings match a human flaw versus 26%          over the same 149 clips and 304 flaws (Section 5.1.2).
of VeriPhy’s 871. About a third of its questions only          Horizontal axis: mean model and tool calls per clip;
check object presence (Is there a vending machine? ),          vertical: recall. Up-and-left is better. Full comparison:
answerable from one frame; twelve clips get no finding.        Table 8 in Section A.6.



                                                          18
Annotated flaw category                                             Annotated   Whole    Partial   Found   Recall

action or event occurs                                                 137        100      14       114    83%
how many                                                                37         10       8       18     49%
object identity                                                         30        14       6        20     67%
on-screen text                                                         25          21       0        21    84%
spatial relation                                                        18         10       1       11     61%
order and timing                                                        17        10       3         13    76%
attribute                                                              16          10       2        12    75%
camera and style                                                       10           7       2        9     90%
other                                                                    7          5       1         6    86%
physical motion                                                          7          4       0         4    57%

All                                                                    304        191      37      228     75.0%


Table 3 Flaw recall on the evaluation core, by annotated flaw category: 228 of 304 human-annotated flaws over 149
clips. Whole and partial are the match outcomes defined in Section 5.1.2; Found is their sum. Categories are the
annotators’ labels, assigned before any critic ran.

Clip by clip it finds fewer than VeriPhy on 70, equal
on 63, more on 16.
As a clip-level diagnostic, CLIPScore correlates across the 149 clips with severity (r = +0.035, p = 0.67) and
flaw count (r = −0.024, p = 0.77); with 86 clips carrying multiple flaws (241 of 304), a single scalar cannot
localize them.

Recall by category and clip property. By the annotators’ own categories (Table 3), recall runs from 90%
to 49%. Camera and style (90%) and on-screen text (84%) rank highest, both measured directly against an
explicit target; counting is lowest at 49% because its path reduces a per-frame series to its mode (Section 4.4),
so an intermittently detected subject reads as absent. Physical motion holds seven flaws, four found; most
concern deformation—cloth folding wrongly, a body bending where it should not—which lies outside the
trajectory measurements, and its recall is read descriptively given the size. Grouping the 304 flaws instead
by severity, duration, flaw count, and difficulty stratum keeps subgroup recall within about ten points of
the overall rate everywhere—severity 5 lowest at 18 of 28—so neither severity nor stratum clearly predicts
whether the critic finds a defect (Table 10 in Section A.8).

5.3.2   Specialist measurement traces

Figure 10 shows six matched findings from an earlier physics-routing pass over the evaluation core; they are
not from the run of Table 3 and do not contribute to its recall. Five rest on numeric measurements, the text
case on a recognition-head transcript compared as a string. The selection rule was fixed in advance—clips
whose every annotated flaw was linked to a finding, and only where the raw per-check record attributed
that finding to a specialist measurement and stored the values—excluding ten candidates for mismatched
linkage, a verifier-produced finding, or, once, an invalid rationale (a “vertical 9:16” aspect ratio misread as a
9.0-versus-16.0-second duration).

What each measurement discriminates. Each catches what an impression would not (Figure 10). The
dolphin leap is contradicted by a near-zero vertical excursion a motion-only test would have passed; the bottle’s
surface and background move alike, so its rolling is camera motion; the sun is scored by peak departure (a
rise then fall cancels) and falls short amid comparable camera motion; counting compares asserted against
measured counts exactly; and the text head returns garbled glyphs that fail string equality, which a generative
model would silently normalize to the requested phrase.

Independent measurements and coverage. A second dolphin sentence asserts the animal never dis-
appears, so two specialists evaluated the prompt’s requirement that it disappear: the vertical-travel check


                                                       19
   Dolphin — Leap detector




               0.00 s                              1.25 s                                2.50 s                               3.75 s                               5.00 s
   Annotator    The dolphin … merely swims to the surface and then dives back down without jumping out of the water.
   Measured     Hops: required yes, measured no — largest vertical excursion 0.00 of the dolphin's own radius over 37 tracked frames; 0 excursions reach the 0.30-radius threshold
   Verdict      Contradicted

   Water bottle — Surface motion vs. background flow




               0.00 s                              2.56 s                                5.12 s                               7.68 s                              10.24 s
   Annotator    The water bottle … remains in its original position and never rolls on the floor.
   Measured     Rolling: required yes, measured no — surface moves 10.20 px/frame against 11.00 px/frame of background flow, over 256 frame pairs
   Verdict      Contradicted

   Sun — Vertical travel, camera cancelled




               0.00 s                              2.00 s                                4.00 s                               6.00 s                               8.00 s
   Annotator    The sun remains completely stationary in its original position without slowly rising.
   Measured     Vertical travel: required up — largest departure from its starting height 0.71 radius, under the 0.75 that counts as travel; net −2 px over 192 tracked frames
   Verdict      Contradicted

   Babies — Counter




               0.00 s                              2.00 s                                4.00 s                               6.00 s                               8.00 s
   Annotator    There are only five babies in the video, which does not match the quantity requested in the text prompt.
   Measured     Count: prompt asserts 7, measured 5 (exact mode)
   Verdict      Contradicted

   F-22 jets — Counter




               0.00 s                              1.25 s                                2.50 s                               3.75 s                               5.00 s
   Annotator    A total of four fighter jets appear in the video, which does not match the requested quantity of three.
   Measured     Count: prompt asserts 3, measured 4 (exact mode)
   Verdict      Contradicted

   Graduation banner — OCR recognition head




               0.00 s                              2.50 s                                5.00 s                               7.50 s                              10.00 s
   Annotator    The text appearing in the video does not match the requested text “Congratulations to the graduates”.
   Measured     Text: required 'CONGRATULATIONS GRADUATES', read 'GOBADRAEAT(CRSTRORISEUND' — stable wrong transcript on 25 of 241 frames (stride 10)
   Verdict      Contradicted



Figure 10 Six flaws identified through specialist measurement, one per row. Each row gives the specialist that answered,
a five-frame filmstrip sampled uniformly across the clip, the human annotator’s sentence verbatim, the specialist’s own
required-versus-measured pair with its evidence, and the resulting claim state. Displacements are normalized by the
subject’s radius, so no scene calibration is required. In the text case, the boxed banner region of the last frame is
magnified in place, showing the render’s own glyphs. Measurement text is copied from the run’s records.



                                                                                         20
                                                                 All clips (n = 200)           Hard subset (n = 55)

Judge                                                    Exact    Within 1   PLCC      SRCC    PLCC        SRCC

VideoScore2 [27]                                         33.0%     83.0%     0.353     0.327   0.239       0.151
VeriPhy                                                  31.0%     76.0%     0.464     0.465   0.480       0.460


Table 4 Semantic-adherence agreement with human ratings on the 200-clip VideoPhy-2 sample described in the text,
scored with VideoScore2’s evaluation script. The physical-commonsense dimension is excluded because the critic does
not emit a score on that scale.

required downward motion but measured 2.07 radii upward (−317 px over 37 frames, negative denoting up),
and the persistence check required it to vanish but found it on 121 of 121 frames with no gap of three or
more; both independently contradict the requirement. Each measurement also records its temporal coverage:
in the banner case the recognition head read 25 of the clip’s 241 frames at stride ten, and a transcript stable
across those 25 evidences a persistent banner, whereas a briefly-appearing caption could fall between samples.

Specialist abstention. In the run of Table 3, physical specialists were called on 227 checks, abstaining on
166 and contradicting on 61, each abstention carrying its reason. The most common is no candidate grounding
passing the semantic guard—shown one frame with the candidate boxes and asked only whether they are
the named subject: for seagulls scattering behind fighter jets, the “seagulls” boxes held the jets and were
discarded, yielding unknown and separating a failure to find the subject from a violation by it.

5.3.3   Agreement with human clip-level ratings

Since localized recall and clip-level scalars are not directly comparable, we compare VeriPhy with VideoScore2 [27]
on human clip-level semantic-adherence ratings, both on the 1–5 scale and scored with VideoScore2’s published
script. The sample is a prespecified fixed-seed draw of 200 VideoPhy-2 [4] test clips (55 hard -flagged) to
which the scoring function was not fitted; agreement uses the four Table 4 columns, dropping per metric any
unparsed prediction.
The critic trails on exact and within-one agreement but leads on PLCC and SRCC (Table 4). A paired
bootstrap gives SRCC gain +0.138 (95% CI [+0.005, +0.277]), PLCC gain +0.110 ([−0.018, +0.242]); on
the 55 hard clips, +0.242 ([+0.018, +0.511]) and +0.309 ([+0.050, +0.583]). This fits per-claim evidence
degrading more gracefully than a single learned scalar on hard clips, though that subset is small and intervals
wide. Caveats: the single 200-clip draw describes that sample, not the benchmark; and the judges are not
cost-matched (decomposition plus tool calls versus one forward pass), so this says nothing about efficiency.

5.3.4   Held-out evaluation on Physion-Eval

Physion-Eval (Section 5.1.1) holds out clips from this system’s development: 9,569 generated clips from five
generators, each with a human report of physical glitches (8,745 with at least one). Two release limits bound
what is measurable: the matched real-world reference videos for the benchmark’s J statistic are withheld for
copyright, and glitch-free clips are not verified negatives. The release thus supports neither J nor false-alarm
rates for any evaluator—only flag rates on release clips and matched-report rates on reported-glitch clips.
VeriPhy runs over a fixed randomized stream; figures are interim, covering the first 601 clips (543 with a
reported glitch, 58 without). The in-context lesson state (Section 5.4) was active and updated as the stream
progressed, so the run is prequential over an evolving configuration, with no component seeing a label before
scoring its clip.
Three measures separate prompt-grounded findings from physics-grounded reports (Table 9). The matched-
report clip rate is the share of reported-glitch clips with a finding matching the report under Section 5.1.2.
The evidence-conditioned flag rate is the share the served model calls physically unrealistic from the check
records alone—question, verdict, reason, and numerical evidence—without frames or the reported defect. The
anomaly-phrased finding rate is the share whose finding explicitly alleges a physical anomaly rather than an
unmet prompt requirement.



                                                        21
                                                          best automated critic                                   human reference

         Untrained humans (reference)                                                                                      52.7%

        VeriPhy (evidence-conditioned)                                                     26.8%

                       Gemini 3.0 Pro                                    16.9%

                       Qwen3-VL-32B                                   14.4%

                        Qwen3-VL-8B                              12.7%

                      Claude 4.5 Opus                         10.7%

                             GPT-5.2                          10.5%

                       Gemini 2.5 Pro                         10.4%

                     Gemini 2.5 Flash                   8.2%

                 Gemini 2.5 Flash Lite           4.5%

                     Cosmos Reason 1        2.8%

                     Cosmos Reason 2      1.2%

                                     0%                 10%               20%               30%            40%     50%
                                                                              physical-implausibility flag rate



Figure 11 Physion-Eval physical-implausibility flag rate for every evaluator of Table 9, sorted high to low, with the
untrained-human reference (light) and this work’s evidence-conditioned rate (red). This work’s rate is measured on the
first 601 release clips; the benchmark’s critic rates are transcribed from its Figure 4 over its full evaluation set, so the
comparison is descriptive rather than common-protocol.

Figure 11 places this work’s evidence-conditioned flag rate against the benchmark’s published flag rate for
every critic it evaluated, with the untrained-human reference for scale; the full table, adding this work’s other
two rates and the benchmark’s J statistics, is Table 9 in Section A.7. Because this work’s rows and the
benchmark’s rows use different samples and system configurations, their juxtaposition is descriptive rather
than a common-protocol comparison.
The evidence-conditioned flag rate is nearly twice the anomaly-phrased finding rate, indicating that the
accumulated evidence supports physical-implausibility judgements beyond what individual findings’ wording
states.

5.4    Context-training self-evolution of the critic
The inward channel distills lessons from misses into the critic’s readable state, improving without touching
a weight; the formalism—distillation map (22), acceptance gate (23), edited state S = (O, M, K)—is in
Section B. We measure flaw recall.
On a plan’s miss of a human-annotated flaw, Distill (22) reads the trace and miss and writes a lesson naming
a claim property and the action it licenses (e.g. turning a singular-entity or exact-quantity requirement
into a separate cardinality check verified across beginning, middle and end ); curation groups candidates
into 33 families of equivalent advice, one lesson each, appended to the planner’s rubric. Only M changes
(S ′ = (O, M ′ , K)); a family’s name labels the defect its lesson concerns.
Implementation departs from the formalism twice. First, all 33 lessons go on every clip: the selective
form (one relevance call per lesson–claim pair) costs 132 model calls for a four-claim prompt and 495 for
a fifteen-claim one, whereas all-at-once costs no calls and adds 9 kB to a planner prompt already 17.8 kB
long. Second, the acceptance gate (23) is dropped: Uval scores only rules already seen in a run, not one
from a fresh miss—diagnostically, on 80 earlier candidates over a ten-clip set it admitted none (39 failed
its minimum-evidence criterion, 41 never triggered). The evaluated intervention is the curated 33 lessons,
without the gate.




                                                                        22
flaws found (of 502)   380      taught: 374–377 flaws (≈74.7%), flat across dose (p ≥ 0.8)    Figure 12 Flaws found against the number of experience
                                                                                              clips the lessons were distilled from, over the same 502 held-
                       370                                                                    out flaws in every condition. The dotted line marks the
                                                                                              untaught condition, 340 of 502 (67.7%). Whiskers are 95%
                       360               +35 flaws                                            intervals on the change from untaught, in flaws, computed
                                         (+7.0 pts)
                       350                                                                    from the flaws that switch status, since the conditions
                                                                                              score the same flaws. Every taught condition exceeds
                       340                                                                    the untaught one, while pairwise comparisons among the
                                    untaught 340 (67.7%)
                                                                                              taught conditions return p ≥ 0.8.
                                0           25         50      75          117
                              experience clips the lessons were distilled from

Protocol and result. Lessons distilled from experience clips are tested on held-out ones: excluding every
clip sharing an identifier or restating an experience-clip prompt leaves 306 clips with 502 flaws, so no lesson is
evaluated on the prompt it was written from. Every condition scores those flaws under Section 5.1.2’s protocol
(a flaw is found when the critic covers it wholly or in part), untaught loading an empty lesson file through the
same path; five nested conditions—no lessons, then 8, 13, 19 and 33 lessons from 25, 50, 75 and 117 clips, each
a prefix of the next—form a dose curve. With all 33 the planner finds 375 of 502 flaws (74.7%) against 340
untaught (67.7%): 62 switch missed-to-found and 27 back, net +35 at p = 3×10−4 (paired sign test). More
experience does not extend it (Figure 12): the four taught conditions find 375, 377, 374 and 375, each +34 to
+37 over untaught at p < 10−3 but no two differing by more than 3 (p ≥ 0.8 pairwise), and the unfiltered set
(363 clips, 626 flaws) matches. Later lessons reshuffle which flaws are found, not how many—36 move each
way between the 8- and 33-lesson conditions—so the gain is present already with lessons from 25 clips.

 Effect by flaw category. Both conditions score the same flaws, so we report the paired change and its
 interval from flaws that switched status (Table 5). Between untaught and 33-lesson conditions, two categories’
 95% interval excludes zero: action or event occurs, largest at 211 flaws, gains 17 (8.1 percentage points,
 [+2, +12]); on-screen text gains 8 of 73 (11.0 points, [+2, +15]). All other intervals contain zero, and reading
 smaller movements as rates overstates them: +7 points for camera and style is one flaw of 14, +16 for counting
 is three of 19. Flaws rise in both severity grades holding the bulk of the set—19 of 288 at severity 3 (p = 0.01)
 and 13 of 163 at severity 4 (p = 0.03)—the remaining 51 at grades 1, 2 and 5.

 Where the lessons point. Gains are not aligned with lesson names. All eight families from the first 25
 clips concern actions, none mentioning text, counting or spatial relations, yet at 8 lessons on-screen text posts
 the largest percentage-point gain of any category (10 of 73) before any lesson mentions text, then loses two
 after one does; the later 25 families do not move their nominal targets. This fits the first lessons supplying
 a general instruction—separate a compound requirement into checkable parts—applying well beyond the
 categories they were written from, which the plan measurements below assess.

Effect of the lessons on the plan. Lessons compile the prompt into more claims, not more checks per
claim: from untaught to 33 lessons, checks per claim rise only 1.13 → 1.18 while typed physical claims rise
2,905 → 5,106 over 306 clips (9.5 → 16.7 per clip)—as the decomposition reading predicts. This locates the
flattening: claims per clip keep rising across all five conditions (9.5, 15.1, 16.0, 16.1, 16.7), so later lessons keep
changing the plan while flaws found stall. On-screen text shows this at clip level: text checks rise 81 → 136
(already 114 at 8 lessons), yet of 56 text-flaw clips the number getting any text check does not (41 untaught
vs. 40 taught)—lessons add checks without widening the set of clips checked.

 5.5                         Writing a verdict back into generation
 The critic’s outward channel—a verdict with its evidence, fed back as a prompt rewrite that regenerates the
 clip—is claimed but not yet measured. We close that loop on a held-out generator and ask a deliberately
 narrow question: does it help on the metric that triggered it, and does an independent rater register the same
 change?
 The loop composes the two maps of (1) through a rewrite operator: from a base clip V̂ ∼ Gen(p, C) the critic
 returns Crit(V̂, p) = (v, π, F)—a verdict v ∈ {plausible, implausible, abstain}, a plausibility score π = pplausible ,


                                                                                             23
                                              Flaws found, with ℓ lessons

Flaw category                      Flaws    ℓ=0     8     13     19     33     Change     95% interval (pts)   Families

action or event occurs              211     146    169   169    166    163    +17 (+8)        [+2, +12]          20
on-screen text                       73     53     63     56     62     61     +8 (+11)       [+2, +15]           1
attribute                            46     29     30     32     31     33   +4 (+9)          [−2, +12]           2
order and timing                     22     11     13     13     13     14   +3 (+14)         [−9, +27]           3
how many                             19      9      9     11     11     12   +3 (+16)        [−10, +31]           2
object identity                      52     39     41     39     42     41   +2 (+4)           [−3, +7]           4
camera and style                     14     11     11     12     11     12   +1 (+7)           [−4, +7]           0
spatial relation                     45     28     29     30     28     28   +0 (+0)         [−10, +10]           1
physical motion                      15      9      8     12     9       9   +0 (+0)         [−11, +11]           0

All flaws                           502     340    375   377    374    375    +35 (+7)        [+3, +10]          33


Table 5 Effect of the distilled lessons on each flaw category, over the same 502 held-out flaws in every condition. A
flaw is found when the critic’s findings cover it wholly or in part, as in Table 3. The five middle columns count that
category’s flaws found with no lessons and with 8, 13, 19 and 33 lessons, distilled from 25, 50, 75 and 117 experience
clips; Change is the untaught-to-33 difference in flaws, with percentage points in brackets, since several categories
carry few enough flaws that a rate alone would overstate the movement. Because the conditions score the same flaws
the comparison is paired: the interval on the change is computed from the flaws whose found status switched, and is
given in percentage points of that category’s flaws. Bold marks the rows whose interval excludes zero. Families counts,
over all 33 lessons, those whose family name refers to that category, matching on the words in the name. The other
category, containing 5 flaws in all, is omitted from the category rows; the All flaws row includes those flaws.

and the violated obligations F = {(ej , aj )}j with their evidence. A text-only rewrite ρ folds those failures
into the prompt and the same generator resamples under the same control and seed,

                  p′ = ρ p, F when v = implausible (else p′ = p),         V̂ ′ ∼ Gen p′ , C ,             (12)
                                                                                          


so the channel acts only through the prompt—diffusion weights, control C, mask, and seed untouched—
changing appearance while fixing the motion path. We run one round, reading the change in π and v against
an independent rater applied to both.

Protocol. We run the full evaluate → rewrite → regenerate loop over Cosmos3-Nano, a generator unused
anywhere in this system’s development, on its 600 VideoPhy-2 test clips (589 complete the loop with a paired
score, so the before/after columns rest on 600 and 589). Each baseline and its regeneration are scored two
ways: by VeriPhy’s own metric (pplausible and the verdict of Section 5.3), the quantity the rewrite optimizes;
and by VideoPhy-2’s official AutoRater [4], an independent rater returning semantic adherence (SA), physical
commonsense (PC), and their joint agreement (both ≥ 4). The AutoRater is the control—not the loop’s
objective and sharing no component with the critic.

On its own metric the loop is effective. By VeriPhy’s own measurement (Figure 13) the loop is targeted
with low collateral: it acts on the 14.8% of clips it judges flawed, raises pplausible on 72.4% of those and flips
49 of 65 implausible verdicts to plausible, regressing only 1.6% of unflagged clips.

An independent rater registers no change. The same 589 clips scored by VideoPhy-2’s AutoRater
show no movement in either dimension (Table 6; Figure 14 places the two readings side by side, clips in
Figure 15): joint agreement, SA, and—critically—the physical PC dimension all stay flat to lower, within
rater noise. Stated together, not collapsed: the gain appears only on the metric the critic itself assigns, while
the one rater independent of the loop registers no change on either axis. The design cannot separate two
readings—that rewrites improve a physical quality the critic can measure but the AutoRater cannot, or that
they raise the critic’s own score without improving the clip—because the critic both triggers and judges the
effect it reports. (External position only: Cosmos3-Nano’s AutoRater joint score is unchanged by the rewrite,
22.8 → 23.1% (all) and 3.9 → 3.4% (hard), near published human-rated leaderboard entries; but human and


                                                          24
                                                   what the loop acted on, and what changed                                        before and after
                                                   VeriPhy's own metric, self-assessed: the critic that triggers a rewrite also judges its result



                                of all 589 clips                                                                                                    rewrite
                                                                                                                                                     0.862
   acted: judged flawed, prompt rewritten                                                           87/589 (14.8%)
                               of the 87 acted                                                                                             baseline
                                                                                                                                            0.797
                           pplausible increased                                                     63/87 (72.4%)
       of the 65 acted first judged implausible                                                                                  0.70         0.80        0.90
                                                                                                    49/65 (75%)                         overall mean pplausible
                verdict flipped to plausible
                                                                                                                                            all 589 clips
                        of the 502 not flagged
   collateral: verdict flipped to implausible                                                       8/502 (1.6%)
                                                                                                                                   +0.524
                                               0%           25%         50%          75%        100%
                                                                                                                                   mean ¢pplausible on the
                                                                share of the group
                                                                                                                                   87 acted clips


Figure 13 The same loop scored by VeriPhy’s own physical metric. Every quantity here is self-assessed: the critic that
triggers a rewrite is also the judge of its result, so these quantities show the loop is internally consistent—targeted
(it acts on 87 of 589 clips, 14.8%), effective on its targets (63/87 raise pplausible , 49 of the 65 acted clips first judged
implausible flip to plausible, mean ∆pplausible +0.524), and low-collateral (8/502, 1.6%)—and move the overall mean
pplausible from 0.797 to 0.862. Each bar is drawn against its own denominator. They are not an independent confirmation
and should be read against Table 6, where an independent rater registers no corresponding change, including on the
physical dimension; every value is recomputed from the per-clip records in Table 11.

                                                                                                                 All (n = 589)                 Hard subset

VideoPhy-2 AutoRater metric                                                                                 Baseline        Rewrite        Baseline       Rewrite

Mean semantic adherence (SA)                                                                                   3.12           3.13           2.75           2.76
Mean physical commonsense (PC)                                                                                 3.59           3.58           3.36           3.32
SA ≥ 4                                                                                                        27.8%          28.0%           8.9%          7.9%
PC ≥ 4                                                                                                        55.0%          54.5%          37.2%          36.2%
Joint (SA ≥ 4 and PC ≥ 4)                                                                                     22.8%          23.1%           3.9%          3.4%

Table 6 The refinement loop scored by an independent rater—VideoPhy-2’s own AutoRater [4]—on the same 589
Cosmos3-Nano clips before and after the loop. No cell moves beyond the rater’s noise: joint agreement shifts by +0.3
points over all clips and −0.5 on the hard subset, and both underlying dimensions are flat to slightly lower, including
the physical dimension the loop is meant to improve (mean PC 3.59 → 3.58 all, 3.36 → 3.32 hard). On the hard subset
every entry is unchanged or slightly lower. The rewrite therefore produces no change this independent rater can
register, in either the semantic or the physical dimension. Hard-flagged clips follow VideoPhy-2’s designation.

AutoRater joint scores share no common protocol, so this is descriptive only.) Every reported figure was
recomputed independently from the run’s per-clip files and reproduces exactly (Table 11 in Section A.9).

Scope. Confirming the rewrites improve physical fidelity as an independent judge would score it needs a
rater both independent of the critic and sensitive to the targeted physical property—which the AutoRater’s
flat PC suggests it is not on these clips. All 589 per-clip comparisons and both scoring streams ship with the
run; a curated set of before/after clips, with the critique and rewritten prompt for each, is on the project page.

5.6     Scope and interpretation
Each setting must be read on its own terms. The generator analyses (Section 5.2) are pre-registered probes
on small closed-form scenes, characterizing the deployed pipeline rather than its generality. Core recall
uses recorded annotations on development data, where an unrecorded defect cannot be scored, and its
question-decomposition baseline was specified after inspecting critic outputs. The context-training result
(Section 5.4) is held out from the distillation pool but still drawn from the development corpus. Only the


                                                                                25
                                VeriPhy's own physical metric                                               independent rater (VideoPhy-2 AutoRater)




                                                                                  All (n = 589)
                                                                                                  SA ¸ 4
        improves on flagged                                      63/87 (72.4%)
                                                                                                  PC ¸ 4
                                                                                                    Joint

         flips impl. ! plaus.                                     49/65 (75%)




                                                                                  Hard subset
                                                                                                  SA ¸ 4
                                                                                                  PC ¸ 4
 collateral (unflagged worse)    8/502 (1.6%)
                                                                                                                                           baseline
                                                                                                    Joint                                  rewrite

                            0%          25%       50%           75%        100%                         0%            20%          40%           60%
                                                                                                                  clips passing the threshold


Figure 14 The refinement loop read two ways, on the same 589 Cosmos3-Nano clips. Left: by VeriPhy’s own physical
metric—the quantity the rewrite optimizes—the loop is targeted and low-collateral: of the clips it flagged, 63/87
improve and 49/65 flip from implausible to plausible, against 8/502 unflagged clips that regress. Right: the same clips
scored by VideoPhy-2’s independent AutoRater show no movement—each dumbbell from baseline (navy) to rewrite
(red) collapses to a point at every threshold, on both the full set and the hard subset, in the semantic and the physical
dimension. Every number is transcribed from Table 6 and the self-assessed counts of Figure 13. The improvement is
thus visible on the critic’s own metric and not on the one rater independent of it. Clips in Figure 15.

interim, prequential Physion-Eval run (Section 5.3.4) is held out from development entirely—with an evolving
lesson state, a different annotation vocabulary, and no frozen-core protocol. The refinement loop (Section 5.5)
is closed on a held-out generator but confirmed only on the critic’s own metric; the one independent rater
shows no change in either dimension.


6    Conclusion
A quality score can rank two clips; it cannot identify which physical obligation was violated, or when. Work on
physical faithfulness in generated video divides into three separate pieces: a way to steer what gets generated,
a way to measure whether obligations are met, and a source of ground truth to score those measurements
against. Closing the gap takes all three at once. This report builds one artifact for each and connects them
into a single loop: a simulation-driven controllable generator (MuJoCo → Wan 2.2-VACE) in which the solver
fixes the motion and the prompt supplies only appearance; a benchmark of human-annotated defects localized
to the offending prompt words, time span, and box track; and a critic, VeriPhy, that compiles the prompt
into typed physical obligations before it reads any frame, then calls frozen experts only within the scope those
obligations declare.
That ordering is the central design decision. Because the plan is fixed before any pixel is read, every measure-
ment traces back to the obligation that asked for it, and every verdict (supported/contradicted/unknown,
surfaced as plausible, implausible, or abstain) carries the evidence that forced it. On a development core
of 149 clips carrying 304 human-marked defects, VeriPhy accounts for 228, against 164 for a published
question-decomposition evaluator reading the same clips with the same served model. Prompting that
backbone monolithically reaches 222, so recall alone does not separate the two. What separates them is that
a reader can open any one of VeriPhy’s 228 findings and see the measurement that produced it, the time
window it was taken over, and the rule that turned it into a verdict. The same reader can overturn that
verdict by disputing the evidence. The monolithic prompt returns a score with no supporting evidence.
An auditable state is also improvable without retraining. Distilling lessons from experience clips and loading
them as readable context lifts recall from 340 of 502 held-out flaws to 375 (67.7% → 74.7%, net +35 at
p = 3×10−4 ), with no lesson evaluated on the prompt it was written from (Section 5.4). The gain saturates
quickly: lessons distilled from 25 clips already find 375, the count also reached with 117 clips, and the four
taught conditions differ by no more than 3 (375, 377, 374, 375). Later lessons change which flaws are found
rather than how many. A small, legible body of experience, in the form of text a human can read, audit, and


                                                                      26
 What the critic flagged, and the clip the rewrite regenerated
 A ball appears from nothing
   baseline




              a ball hangs in mid-field with no hand on it
   rewrite




              the ball stays in the pitcher's grip
 Original prompt: A baseball player throws a fastball; the ball leaves their hand and travels towards the catcher's mitt.
 Rewritten prompt: In a sun-drenched baseball field, a dynamic moment unfolds as a player in a sleek black jersey and white pants
 stands poised on the mound, their right arm drawn back with a baseball firmly gripped and clearly visible in their palm. The camera
 captures the scene from a low angle, emphasizing the athlete's intense focus and the tension of the impending pitch. As the arm
 snaps forward, the ball is released with a continuous, fluid motion, maintaining its spherical shape and white leather texture as it
 travels in a realistic parabolic arc through the air, illuminated by the golden-hour glow. The background blurs into a vibrant
 tapestry of green grass and distant spectators, enhancing the sense of speed and precision without distorting the environment. The
 catcher, clad in protective gear, crouches expectantly, mitt poised to receive the fastball, while the umpire stands resolutely
 behind the plate, embodying the spirit of the game. This cinematic tableau, rich with detail and emotion, encapsulates the essence
 of baseball's thrilling artistry, ensuring the ball's trajectory and the player's biomechanics adhere strictly to the laws of
 physics.


 A hammer head morphs between shapes
   baseline




              the head flips between a ball-peen and a claw
   rewrite




              one consistent claw hammer
 Original prompt: A hammer is thrown and bounces once before stopping; the bounce and final resting position are clearly seen.
 Rewritten prompt: A close-up, static shot captures a solid steel hammer with a vibrant red grip poised in mid-air, its head
 glinting under soft, diffused lighting that accentuates its metallic sheen. The camera remains fixed as the hammer is released, its
 trajectory arcing naturally under gravity until it strikes a textured surface with a sharp, audible impact. Upon contact, the hammer
 undergoes a realistic, brief elastic compression at the head before rebounding upward with a loss of kinetic energy, clearly showing
 a single, distinct bounce rather than a continuous glide. The hammer maintains its rigid, unchanging form throughout the motion,
 with no deformation, splitting, or morphing of the claw or handle. As it settles after the bounce, it comes to a complete rest on
 the ground, its head tilted slightly, while the camera subtly shifts to keep the object in frame, ensuring the entire sequence of
 release, impact, bounce, and final stop is captured with continuous, momentum-conserving motion.



Figure 15 What the critic flagged, and the clip the rewrite regenerated—clips VeriPhy judged implausible and resampled
through (12). Each case is two real filmstrips: the baseline clip (grey) and the clip regenerated from the rewritten
prompt (rewrite, red), six frames early to late; red boxes mark the cited physical violation and its repair, and the full
regenerated prompt is printed verbatim beneath. Cases were chosen by an independent frame-by-frame review under
an honesty constraint—the before/after must be the same scene, not a rewrite that swaps the scene or introduces
a new artifact—which most flagged clips fail; these are cases where the fix is visible and the comparison fair. Two
further cases are in Figure 16; the quantitative reading is Figure 14.




                                                                     27
                 the coins melt into one shapeless mass




   rewrite
                 separate, clearly circular coins
 Original prompt: A person skillfully tosses several coins in the air, catching them one by one.
 Rewritten prompt: In a serene, sunlit room, a skilled individual stands poised, their hands gracefully positioned in front of them.
 The camera captures a close-up of their hands, adorned with a sleek black watch, as they deftly toss a series of rigid, gleaming
 gold coins into the air. Each coin maintains its solid circular disk shape throughout its trajectory, following a smooth, continuous
 parabolic arc under gravity without distorting, splitting, or teleporting. The coins collide with the palm and fingers with clear
 impact, resting stably on the skin surface supported by normal force, never interpenetrating the hand or losing their metallic
 integrity. The background is softly blurred, enhancing the focus on the precise choreography of the tosses. The scene is bathed in a
 warm, golden-hour glow, casting gentle shadows that accentuate the coins' unchanging metallic sheen. As the coins are caught, the
 individual's hands remain steady, embodying a sense of calm control, while the camera maintains a static position, allowing the
 What
 viewer tothe   critic
            fully      flagged,
                  appreciate      and the
                             the artistry     clipphysically
                                          of this   the rewrite     regenerated
                                                             consistent display.

 Coins fuse into a blob
 A frisbee changes shape in flight
      baseline
   baseline




                 the coins melt into one shapeless mass
                 the disc warps and briefly turns into a red ball
      rewrite
   rewrite




                 separate, clearly circular coins
 Original prompt:
      a stable     A person
               white  disc skillfully tosses several coins in the air, catching them one by one.
 Original
 Rewrittenprompt:
            prompt:AnInunderhand   throwroom,
                        a serene, sunlit sendsaaskilled
                                                 frisbeeindividual
                                                         spinning across
                                                                   standsapoised,
                                                                            beach, their
                                                                                    landing neargracefully
                                                                                         hands    the water's edge. in front of them.
                                                                                                           positioned
 The cameraprompt:
 Rewritten       capturesIna aclose-up    of theirbeach
                                sun-drenched        hands,  adorned
                                                         scene,       with afrisbee
                                                                 a vibrant    sleek black   watch,
                                                                                     is thrown        as they deftly
                                                                                                 underhand,            toss a series
                                                                                                                maintaining           of rigid,
                                                                                                                               its rigid,  solid gleaming
                                                                                                                                                 disc shape
 gold  coins
 without   anyinto  the air. Each
                 morphing,            coin or
                              splitting,    maintains   its solid
                                              color shifts        circularthrough
                                                            as it travels  disk shape
                                                                                    the throughout      its trajectory,
                                                                                          air. The camera     captures following     a smooth,
                                                                                                                         a continuous,            continuous
                                                                                                                                           unbroken
 parabolic
 trajectory arc
              fromunder   gravity without
                     the thrower's             distorting,
                                       off-screen  hand tosplitting,   or teleporting.
                                                             the water's  edge, ensuring Thethecoins
                                                                                                 disccollide
                                                                                                       never with   the palm
                                                                                                               vanishes,        and fingers
                                                                                                                          teleports,           with clear
                                                                                                                                      or reappears    at a
 impact, resting
 different  location.stably
                        The on   the skin
                             frisbee        surface
                                       follows       supported
                                                a smooth,         by normal force,
                                                             gravity-consistent   arc,never   interpenetrating
                                                                                        slowing   slightly due totheairhand  or losing
                                                                                                                        resistance       their
                                                                                                                                     before     metallic
                                                                                                                                             making   solid
 integrity.with
 contact     Thethebackground
                       golden sand,is softly
                                       whereblurred,
                                               it rolls enhancing   the focus
                                                        naturally without       on the precise choreography
                                                                             interpenetrating     the ground or of   the tosses.
                                                                                                                   exhibiting      The scene
                                                                                                                                sudden    jumps.is As
                                                                                                                                                   bathed
                                                                                                                                                      it in a
 warm, golden-hour
 approaches              glow,edge,
                the water's      casting
                                      the gentle   shadowsremains
                                           disc's motion      that accentuate
                                                                     fluid and the   coins' unchanging
                                                                                 physically                 metallic
                                                                                              grounded, finally       sheen.toAs
                                                                                                                   coming         thenear
                                                                                                                                rest   coinstheare caught,
                                                                                                                                                gently      the
                                                                                                                                                        lapping
 individual's   handsa remain
 waves, all under                 steady, embodying
                        warm, golden-hour        glow thata sense  of calm
                                                             highlights  thecontrol,  while
                                                                              seamless,       the camera
                                                                                          realistic  physicsmaintains    a static
                                                                                                              of the object's     position,
                                                                                                                               flight         allowing the
                                                                                                                                       and landing.
 viewer
 Whattothe   fully  appreciate
                  critic  flagged,the artistry
                                        and the  of this
                                                     clipphysically   consistent
                                                            the rewrite           display.
                                                                             regenerated
 A soccer ball duplicates
 A frisbee changes shape in flight
     baseline
   baseline




                 a second ball appears alongside the first
                 the disc warps and briefly turns into a red ball
     rewrite
   rewrite




                 a single ball off the foot
       a stable
 Original  prompt: white   disc player runs, plants their foot, and drop kicks a soccer ball high into the air, the ball arcing visibly.
                        A soccer
 Original prompt: An underhand throw sends a frisbee spinning across a beach, landing near the water's edge.
 Rewritten prompt: In a sun-drenched soccer field, a dynamic athlete clad in a sleek black jersey and vibrant red shorts sprints
 Rewritten
 with purpose,prompt:     In a hair
                   their long   sun-drenched     beach them.
                                     flowing behind       scene, The
                                                                  a vibrant
                                                                      camera  frisbee  is thrown
                                                                                 captures            underhand,
                                                                                             their fluid  motion maintaining     its rigid,
                                                                                                                   in a static shot,         solid disc
                                                                                                                                       emphasizing    theshape
                                                                                                                                                           player's
 withoutasany
 agility     theymorphing,    splitting,
                    plant their           or color
                                 right foot   firmlyshifts
                                                       on theas ground,
                                                                it travelsthe
                                                                            through
                                                                               single the
                                                                                       soccerair.ball
                                                                                                  Theresting
                                                                                                        cameraclearly
                                                                                                                captures   a continuous,
                                                                                                                       at their side. Withunbroken
                                                                                                                                               a sudden
 trajectory
 burst        from the
        of energy,    theythrower's   off-screen
                            swing their   left leghand
                                                    high,tomaking
                                                              the water's   edge, ensuring
                                                                     solid contact    with the  the  disc neverball
                                                                                                  stationary     vanishes,  teleports,
                                                                                                                    to execute           or reappears
                                                                                                                                 a powerful             at the
                                                                                                                                               drop kick;   a
 different  location.
 ball launches          The frisbee
                  continuously    fromfollows   a smooth,
                                         the point           gravity-consistent
                                                      of impact,   soaring into the arc,airslowing   slightlyparabolic
                                                                                             in a smooth,     due to airarc
                                                                                                                          resistance
                                                                                                                            without before      making solid
                                                                                                                                        ever splitting,
 contact
 morphing,with or the  golden from
                  appearing    sand,nowhere.
                                      where it Therolls ball's
                                                        naturally   without
                                                               trajectory   is interpenetrating      the ground
                                                                               beautifully illuminated            or golden-hour
                                                                                                             by the   exhibiting sudden     jumps.
                                                                                                                                     sunlight,       As ait warm
                                                                                                                                                casting
 approaches
 glow           the water's
       that enhances      the edge,
                              scene'sthe  disc's motion
                                        cinematic   quality,remains
                                                               while fluid   and physically
                                                                      the background        blursgrounded,   finally
                                                                                                   into a lush  greencoming   to rest
                                                                                                                       expanse,         near focus
                                                                                                                                   drawing    the gently
                                                                                                                                                    to thelapping
 waves, allskillful
 athlete's    under technique
                       a warm, golden-hour
                                  and the ball's glow  that highlights
                                                    majestic,             the seamless,
                                                                uninterrupted     flight asrealistic
                                                                                              it reachesphysics of thebefore
                                                                                                          its zenith    object's  flight andtowards
                                                                                                                              descending       landing.the
 ground.



Figure 16 Critic-guided rewrite, continued, in the layout of Figure 15: a frisbee that warps into a red ball mid-flight,
held to a single rigid object by the rewrite, and a soccer ball that duplicates during the kick—two balls in the baseline
(boxed), one in the rewrite. Red boxes mark the flagged defect and its repair; the full rewritten prompt is printed
verbatim beneath each.




                                                                                    28
edit, does work otherwise done by fine-tuning, and it accrues to a state that stays inspectable instead of being
absorbed into model parameters.
The outward channel is less developed, and its evidence is split. Feeding a verdict and its violated obligations
back as a prompt rewrite, then resampling under the same control and seed, closes the critic-to-generator loop
end to end on Cosmos3-Nano, a generator held out from this system’s development. On the metric the rewrite
optimizes, the loop behaves as designed: it fires on 87 of 589 clips (14.8%), improves 63 of those 87, flips 49
of 65 implausible verdicts to plausible, and regresses 8 of the 502 it leaves alone (1.6%). An independent
rater sharing no component with the critic registers no corresponding movement in either the physical or the
semantic dimension (Section 5.5). The disagreement is the result: it localizes the open problem to the rewrite
channel itself, which at present can edit only words. Whether a text-only edit can move a generator’s physics,
or whether the correction must instead enter through the geometric control channel this report builds, is an
open question this setup can now measure.
The next direction is one this system is already built for and does not yet use: sound. Audio resolves physical
implausibility that vision leaves ambiguous. A visible collision that is silent, or an impact heard before
contact, breaks causality in a way visual fluency cannot conceal, and it does so on a timeline that can be
measured rather than judged. VeriPhy already carries a sound-event specialist, and the architecture already
places audio intervals and visual contact windows on one shared event clock, which is what a synchrony claim
requires: a contact window from vision, an onset from audio, and a typed relation between them, with an
abstain when either stream is unusable. This report does not exercise that capacity; every measured claim
here is visual. Extending physical verification across modalities, with obligations that bind what is seen to
what is heard and a benchmark that localizes audiovisual faults as precisely as this one localizes visual ones,
is what we build next.
Section B casts these components as a single state-optimization framework, and Section C lays out the phased
plan that carries them there.


7   Limitations
The primary limitation of this work is that the control signal comes from a simulator, so scene diversity
is bounded by what is simulated, and the mapping from simulation to prompt appearance is not itself
verified for physical consistency. The corpus used here is also recall-only (no clean clips), so precision is not
directly measurable; flaws are single-annotator with no inter-annotator agreement; the scope/category tags
are machine-derived; and the source generator of the clips is unrecorded. Repeatedly designing against one
frozen set risks overfitting to it even without training on it.
Moreover, the spatial relation predicate and negative-event verification are limited; binding remains a
central failure mode, since the compiler enforces symbolic identifier consistency but cannot guarantee that
heterogeneous tools localized the same physical instance; and the reasoner-mediated sub-checks reduce but do
not remove semantic opacity.
Four limits bound what Section B.7 establishes. The acceptance gate (23) is not exercised, so the measurement
covers distillation without the admission discipline that is meant to keep a bad lesson out; a rule written
from a fresh miss has no proxy history, and closing that gap needs a Uval defined on unrun rules. The taught
planner reads 1.76 times as many claims out of a prompt as the untaught one, and flaw recall rewards asking
more, so the effect combines a better-targeted plan with a larger one; a run holding the taught arm to the
untaught arm’s question budget would separate them. The lessons are induced once from a fixed pool rather
than accumulated online, so the curve of Figure 12 measures the effect of the amount of experience distilled,
not of accumulating it during deployment; the shape beyond 117 experience clips is unmeasured. Finally,
the 502-flaw held-out set is a different population from the 304-flaw evaluation core used everywhere else in
this paper, and the two rates should not be compared directly. Every distilled prior is critic-derived rather
than ground truth, and retrieval quality, staleness, and the propagation of a wrong prior remain open. The
operator set O and the external channel K are untouched: growing the operator library through multimodal
distillation [6, 48, 81] and admitting external knowledge under a candidate-and-prune discipline [30] are future
work.



                                                       29
A     Appendix

A.1   Temporal predicates
The order and containment predicates of Section 4.3 compare interval endpoints under a slack of one quarter
of the shorter window; for windows WX = [sX , eX ],

                                        δ(A, B) = 14 min(eA − sA , eB − sB ),
                                                       
                                                       S, eA ≤ sB + δ(A, B),
                                                       
                                                                                                                (13)
                                   ρbefore (WA , WB ) = C, eB ≤ sA + δ(A, B),
                                                         U, otherwise.
                                                       
                                                       

The quarter-window rule keeps the first two cases mutually exclusive for positive durations; containment uses
the same δ.

A.2    Withdrawal noise-level schedule
Section 3.4 reports the withdrawal point by noise level σrel , not step index i∗ . For S steps at flow shift κ over
N training timesteps, the UniPC schedule assigns

                                (S − i) (1 − 1/N )                 κ s̃i
                        s̃i =                      ,   σi =                   ,   σrel = σi∗ ,                  (14)
                                         S                    1 + (κ − 1) s̃i

with s̃i the normalized flow-matching timestep at step i and σi its noise level.

A.3    Trajectory-agreement metrics
Section 5.2.3 scores how closely a generated clip’s tracked path follows the simulation’s. With pgen       ctrl
                                                                                                      t , pt
the per-frame tracked positions (t ∈ {0, . . . , T − 1}, undefined where the tracker finds nothing) and V the
frames where both are defined, retention over a window W is the per-axis Pearson correlation over W ∩ V
(Rx (W ), Ry (W )), reported only where |W ∩ V | meets a minimum count; R near 1 means the object moved
as simulated.
The windows split at the first ground-contact frame, off the control’s vertical path: with y ctrl downward, tapex =
arg mint∈V ytctrl , and ymin , ymax over the located frames, tc = min{t ≥ tapex : ytctrl ≥ ymax − 10
                                                                                                   1
                                                                                                     (ymax − ymin )},
giving airborne {t < tc } and after-contact {t ≥ tc }. Two prefixed failure modes accompany retention: a
whole-clip disagreement (full-clip horizontal < 0.7) and a late-window disagreement (full-clip horizontal < 0.7
while airborne horizontal > 0.9).

A.4    Critic dataflow and procedure
Figure 17 shows the dataflow of Section 4 and Algorithm 1 the full one-clip procedure, each step tagged
learned or deterministic with its defining equation; both summarise Section 4 and add no new step.




                                                         30
                                                                 Text-only planner
           Prompt                            extracts prompt-grounded claims and writes a surface plan
                                                  specifying the checks that would settle them ---
                                                           before any video frame is read




                                                  Every plan is checked before any tool runs
                         each line is parsed and type-checked; a line that cannot be used falls back to a general judgment,
                                     and that fallback is counted in the plan’s cost rather than treated as free


                                                                                                                                      Video




                           Semantic verifier                                                     Specialist instruments
                reads the frames densely and decides                                    SAM 3 grounds the subject and tracks it;
                whether a thing is there and whether                               eleven typed operations measure over those tracks;
                            an event happens                                              counting reads its instance identities




                                                            Typed execution records
                    specialists return measurements --- masks, tracks, counts, displacements, contacts, and windows; learned
                    base-predicate states are explicitly tagged; every record is tied to the prompt fragment that requested it



                                                           Deterministic composition
                        fixed rules combine the parts of a claim, then the claims into the clip: anything contradicted makes
                       its parent contradicted, everything supported makes it supported, and anything else is left unresolved



                                                               Fallback verification
                       a stronger model re-examines any claim the dense pass left supported; where it disagrees, the claim
                         resolves as contradicted rather than as absent evidence, and both verdicts are kept in the record




                                 Verdict                                                              Audit trace
                each claim supported, contradicted or                                  the claims checked, the evidence each call
                  unknown; the whole clip plausible,                                  returned, which claims fell back to a general
                       implausible, or abstained on                                   judgment, and the rule that combined them



             learned         deterministic        deterministic, before any tool         input


Figure 17 VeriPhy dataflow. The text-only planner writes claims and a surface plan; the compiler expands and validates
it before any video is read. SAM 3 grounds the subject and supplies the tracks the typed operations measure over, so
specialists return numbers while the video-aware verifier returns tagged learned states. Composition is deterministic;
the one learned step after it, the fallback verifier, may resolve a claim the dense pass left supported. Shaded boxes are
learned, outlined boxes deterministic.




                                                                          31
Algorithm 1 VeriPhy critic: bounded learned planning/verification embedded in deterministic compilation,
scoping, and roll-up (executable summary of Section 4).
Require: clip V = {(It , τt )}t∈TV , prompt p
Ensure: verdict Y ∈ {Plausible, Implausible, Abstain} (or ⊥infra )
 1: procedure Critic(V, p)
                                               N
            e ← Πθ (p), C = {ci = (si , ϕi )} p , si ⊑ p
 2:     (C, Π)                               i=1                      ▷ (5); text-only, video unseen (learned)
 3:     GΠ = (A, Q, E, b) ← Compile(Π), aj = (oj , αj , ωj , rj ) ▷ typed DAG, before any frame is read; (6)
                                       e
    (det.)
 4:     if ¬ Valid(GΠ ) then             ▷ Valid = Parse ∧ Refs ∧ Typed ∧ Acyclic ∧[∀i ∃q : b(q)=i]; (7) (det.)
 5:         GΠ ← Fallback(GΠ ); Charge & Report                        ▷ invalid line→general verifier, invalid
    term→recorded sub-check; never guessed
 6:       end if
 7:       for aj ∈ A in topological order of GΠ do                                      ▷ video first touched here
 8:        Ωj ← gj ({Rk : (ak , aj ) ∈ E}, TV ); Rj ← Foj (V|Ωj , αj )   ▷ obs. gate scope (det.); frozen backend,
      SAM 3 grounds tracks; (8)
 9:       end for
10:       for q ∈ Q do
11:           zq ← ψq ({µj : aj ∈ Pa(q)}) ∈ V = {S, C, U}; negate via ¬3                                  ▷ ψq
      det. for count/timing/track/transcription, learned asymmetric gate (C only on positive contradiction) for
      semantic; U if abstained, ⊥infra on infra error; Section 4.5
12:       end for
13:       for i ← 1 to Np do
14:            Ki ← {q : b(q) = i}; yi ← C if ∃q ∈ Ki : zq =C, S if ∀q ∈ Ki : zq =S, else U ▷ claim roll-up; (10)
      (det.)
15:       end for
16:       for all i with yi = U do                                       ▷ single post-composition step (learned)
17:            yi ← FallbackVerify(ci , {Rj })
18:       end for
19:     Y ← ⊥infra on infra error; Implausible if ∃i : yi =C; Plausible if Np ≥1 ∧ ∀i yi =S; else Abstain
    ▷ clip roll-up; (10) (det.)
20:     return Y
21: end procedure




A.5      Benchmark details
Field coverage is in Table 7, a full record in Figure 19, the set’s derivation in Figure 20, and the core’s
distributions in Figure 21.
By machine-assigned type, the core’s 306 flaws (median two per clip) split as actions absent or wrong 139;
wrong counts 36; wrong or missing objects 30; garbled text 25; wrong spatial arrangement 19; wrong ordering
17; wrong attributes 16; camera and style 10; physical motion 7; residual 7—counting, text, and arrangement
together 80, so this is not a physics benchmark in the narrow sense. The 150 clips run a median 8.0 s
(5.0–10.3), mostly 24 fps (118/150), under prompts of median 42 words (longest 188), many naming a shot
list, count, ordering, on-screen string, and sound at once. Sixty-six carry more than one flaw kind. Of the
237 time-spanned flaws the flagged window is bimodal—57 span a quarter of the clip or less, 95 at least
nine-tenths (Figure 21)—so a detector needs both a localized and a whole-clip check.

A.6      Published-evaluator comparison, in full
Table 8 is the full form of Figure 9, adding each evaluator’s output and the modular video-QA row (listed for
context, not evaluated under this protocol, so no figure point).




                                                         32
            check(c0, judge("a dolphin leaps out of the water"))
            check(c1, before(window("the dolphin leaps"), window("the dolphin dives back under")))
            check(c2, judge("two salmon emerge at the same moment") and eq(count("salmon"), 2))
            check(c3, judge("the salmon are behind the fishing boat") and rel("salmon||fishing boat", "behind"))

              claims from the prompt
                                                        typed checks                          measurements
             c0
                                                       event occurs                 general verifier
             the dolphin leaps


             c1                                        order in time                event timing (leap)
             it dives back after the                      (before,
             leap                                       with slack)                 event timing (dive)




                                             and       event occurs                 general verifier
             c2
             two salmon emerge to-
             gether
                                             and         count is 2                 counter




                                             and       event occurs                 general verifier
             c3
             the salmon are behind
             the boat
                                             and          behind
                                                                                    outlines and depth
                                                       (depth order)

                  a claim        a typed check          answered by the general verifier           measured by a specialist

Figure 18 A surface plan compiled into claims, typed checks, and evidence-producing actions (from Section 4.2): a
numeral adds a count check beside a semantic assertion; an ordering consumes two event windows after occurrence
gating; a depth relation consumes localization, masks, and depth from the compiler’s dependency closure. Illustrative
of the planner’s vocabulary, not an added learned verdict.

                                    Field                    Note                          Coverage

                                    violated fragment        median 8 words                306/306
                                    rationale                median 25 words               306/306
                                    severity                 1–5, centred at 3–4           306/306
                                    confidence               1–5, 239 marked 4–5           306/306
                                    time span                                              237/306
                                    box track                                              208/306

Table 7 Coverage of a flaw record’s six fields (defined in Section 5.1.1) across the 150-clip core: the first four always
present, timing and boxes only when the annotator supplies them.

A.7    Physion-Eval comparison, in full
Table 9 is the full form of Figure 11, adding this work’s matched-report and anomaly-phrased rates and
the benchmark’s J statistics—defined against withheld real-world reference videos, hence dashed for every
evaluator on the release.

A.8    Recall by clip property
Table 10 groups the 304 core flaws (run of Table 3) by severity, duration, flaw count, and difficulty stratum.
Subgroup recall stays within about ten points of the overall rate everywhere, so neither severity nor stratum
predicts whether a defect is found.



                                                                    33
      What one human flaw record contains                                                  one of the 306 records in the evaluation core

      THE PROMPT THE VIDEO WAS ASKED TO SATISFY
      A ping pong ball balanced on a hair dryer's air stream, wobbling but never falling. A hand tries to grab
      it and misses. Audio: Dryer whir, laughing.
                                                                                                  the fragment the video fails to satisfy

      WHERE THE FLAW OCCURS
         the video at 2.25 s                                  the video at 3.04 s                                the video at 3.83 s




                                  flagged 2.25–3.83 s — 1.62 s of an 8.0 s clip
                                                                                                     the rest of the clip is not flagged

   0s                                 2s                              4s                             6s                                8s

      HOW BAD IT IS, AND WHY
      severity                    3 of 5      annotator confidence 5 of 5
      the annotator's own reasoning, as written
      “The prompt requires "a hand tries to grab it but fails", meaning the object should not be caught. However, it is caught in
      the actual video, which does not match the requested result.”


Figure 19 One human flaw record in full: the quoted prompt fragment, the interval of visible failure (1.62 s of an 8 s
clip), boxes on the objects at the interval’s start/middle/end, and a severity, confidence, and rationale. No critic
output appears.

Evaluator                                   Output it produces                      Found      Recall     Mean model/tool calls per clip

VeriPhy                                     localized flaw finding                  228        75.0%                     14.1

Other evaluators with structured localized outputs
  Question decomposition [28]       per-question answers                             164       53.9%                     21.9
  Davidsonian scene graph [10]      per-question answers,                            161       53.0%                     52.1
                                    dependency-gated

Free-text localized output
  Single-pass VLM, same                     free-text flaw list                      222       73.0%                      1.0
model [58]

Table 8 Localized flaw recall over the same 149 clips and the same 304 flaws, judged by the protocol of Section 5.1.2.
The calls column reports the mean number of model and tool calls per clip and excludes calls made by the matching
protocol, which scores outputs rather than generating evaluations. Question decomposition uses the same claim list as
VeriPhy on 148 of the 149 clips. The free-text row uses the same served model as VeriPhy, prompted once with every
frame; it is listed separately because it produces an unstructured flaw list rather than structured per-question answers
or per-verdict evidence. A dash marks an evaluator not evaluated under this protocol.

A.9     Refinement figures recomputed from the raw run
Table 11 recomputes every figure of Section 5.5 from the per-clip records (all reproduce exactly) and pins two
definitions: the 8/502 collateral figure and the differing baseline and rewrite denominators.




                                                                     34
                                                             video clips                                        human-marked flaws

                                 Annotated corpus
                                                                                                1,500                                           2,582
                       every clip carries at least one
                                human-flagged flaw
                                                                894 clips set aside: 713 whose prompts describe no motion and whose flagged
                                                                moments are not actions, 181 whose video could not be retrieved

                             Physics-relevant pool
                                                                           606                                                1,171
             the prompt describes motion, or the
                    flagged moment is an action
                                                                64 flaw records set aside because the complaint is about the sound only, with
                                                                nothing to see in the picture; no clip is dropped at this step

                             Frozen evaluation set
                                                                           606                                               1,107
                 flaws a viewer can see, audio-only
                              complaints removed
                                                                every flaw kept; 29 of these clips (85 flaws) also form a continuity-focused group
                                                                carried across experiments

                        Routine evaluation core
                                                                150                                                 306
                 fixed random sample, balanced by
                     severity, flaw count and length



     A further 711 annotated clips (1,130 flaws) are held back for training and share no clip with the frozen evaluation set or its
     routine core. Bar lengths are to scale within each column.

Figure 20 Deriving the evaluation set. Only the first step removes clips; the second removes audible-but-not-visible
flaw records, leaving the clip count unchanged. The core is a fixed random sample balanced by severity, flaw count,
and length; a further 711 annotated clips, disjoint from both frozen sets, are kept for training.



                 Most clips carry one or two flaws                                                  Flagged windows are either brief or clip-long

                  63         average 2.04 per clip                                                                median 62%
                                                                                              100
            60
                       47                                                                     80
                                                                                      flaws




            40                                                                                60
    clips




                                23                                                            40
            20
                                     11
                                                                                              20
                                           4
                                                         1         1
            0                                                                                  0
                   1     2      3   4   5     6    7   8           9                           none        25%         50%        75%        all
                              flaws marked in one clip                                            share of the clip the flagged window covers

                 150 clips of the routine evaluation core, 306 human-marked flaws. The right-hand panel uses the 237 flaws that carry a
                 start and an end frame; the remaining 69 were marked without one. Of those 237, 57 fit inside a quarter of their clip
                 and 95 run almost its whole length; the median flagged window lasts 5.00 s.

Figure 21 Two core properties that shape a detector. Left: most clips are flagged in only one or two places, so many
complaints per clip are mostly ones no annotator marked. Right: flagged windows are bimodal—some failures confined
to a small part of the clip, a comparable group spanning nearly all of it—so both a localized and a whole-clip check
are needed.

B       Framework: Learning as State Optimization
The preceding sections described three artifacts: a physics-guided generator (Section 3), a 1,500-clip human-
authored defect benchmark (Section 5.1), and a physically grounded, tool-using critic whose plan-based


                                                                                 35
Evaluator                                                                                      J exo    J ego    Flag rate

Untrained humans (reference)                                                                  30.7%     56.0%     52.7%

This work, judging from the critic’s measured evidence
  Evidence-conditioned flag rate                                                                —        —        26.8%
  Matched-report clip rate                                                                      —        —        18.4%
  Anomaly-phrased finding rate                                                                  —        —        15.5%

Critics evaluated by the benchmark, judging raw frames
  Gemini 3.0 Pro                                                                              11.3%     5.5%      16.9%
  Qwen3-VL-32B                                                                                 3.2%     1.0%      14.4%
  Qwen3-VL-8B                                                                                  2.7%     0.8%      12.7%
  Claude 4.5 Opus                                                                             5.7%      2.3%      10.7%
  GPT-5.2                                                                                      4.0%     3.7%      10.5%
  Gemini 2.5 Pro                                                                               7.1%     1.1%      10.4%
  Gemini 2.5 Flash                                                                            4.4%      1.7%       8.2%
  Gemini 2.5 Flash Lite                                                                        2.0%     0.4%       4.5%
  Cosmos Reason 1                                                                              0.1%     0.5%       2.8%
  Cosmos Reason 2                                                                              0.9%     0.5%       1.2%

Table 9 Physion-Eval [88] benchmark table. This work’s rows are measured on the first 601 release clips of a fixed
randomized stream (543 with a reported glitch, 58 without): the evidence-conditioned and anomaly-phrased rows
report the share of all 601 clips flagged, and the matched-report row the share of the 543 reported-glitch clips whose
report a finding matches; the three measures are defined in the text. The benchmark’s rows are transcribed from its
Figure 4 and are measured on its full evaluation set: J is its Youden statistic averaged over the five generators, and
the flag rate is the share of generated clips called physically unrealistic, pooled over the two viewpoints. A dash in the
J columns marks a statistic defined against matched real-world reference videos that the public release withholds, so it
cannot be computed for any evaluator run on the release.

adjudication we measure in Section 5.3. This section states the abstraction that ties them together and the
form the framework is built toward. Our thesis is that a physical-reasoning agent should keep everything it
has learned in one human-readable, typed, provenance-carrying state, and should improve by optimizing that
state. Every improvement is then an edit to an object a person can read, version, and veto, and the arc of the
framework culminates in a system that evolves itself without ever touching a weight.
Section 5 reports experiments; the remainder of this section sets out the framework and the roadmap. Because
all learning is state optimization on a readable S, that boundary falls inside the formalism itself, and Table 12
marks it.

B.1   From ReAct and agent memory to a physical agent with typed state
Agentic reasoning in the ReAct lineage interleaves reason, act, and observe steps, letting a model call external
tools and condition on their returns [21, 66, 85]. Program-of-thought variants push this further: the chain of
thought is emitted as a program that composes tool calls [23, 35, 60, 65, 69, 78]. Orthogonally, a fast-growing
agent-memory literature asks where an agent’s accumulated experience should live—episodic transcripts,
distilled semantic priors, or reusable procedures [6, 30, 36, 41, 48, 57, 79, 81, 89, 90]. VeriPhy combines these
two lines and changes the carrier of memory: where these agents store free-text notes or latent vectors, it
stores structured physical-verification traces with full provenance. Auditability follows from that choice, and
it is the throughline of the framework below.

B.2    The unifying abstraction
VeriPhy maintains a single, human-readable agent state

                                                  S = (O, M, K),                                                     (15)


                                                           36
Group                                                                                      Annotated     Found      Recall

Annotator severity
  severity 1                                                                                   3            3       100%
  severity 2                                                                                  28           22       79%
  severity 3                                                                                  146         107       73%
  severity 4                                                                                  99           78       79%
  severity 5                                                                                  28           18       64%

Clip duration
  6 s or less                                                                                 76           60       79%
  6-8 s                                                                                       46           29       63%
  over 8 s                                                                                    182         139       76%

Number of annotated flaws per clip
 1                                                                                            63           49       78%
 2                                                                                            92           65       71%
 3-4                                                                                          113          87       77%
 5 or more                                                                                    36           27       75%

Difficulty stratum
  hard                                                                                        83           60       72%
  not hard                                                                                    221         168       76%

Table 10 Recall grouped by annotator severity, clip duration, number of annotated flaws in the clip, and difficulty
stratum, on the run of Table 3. Severity is the annotator’s own 1–5 judgement of how badly the clip fails.

Quantity                                                                              Reported         Recomputed

VeriPhy self-assessed metric, from the per-clip critic records (589 rows)
  acted (cited ≥ 1 failure)                                                            87/589           87/589          ✓
  of acted, pplausible increased                                                        63/87            63/87          ✓
  verdict implausible→plausible                                                         49/65            49/65          ✓
  mean ∆p (acted)                                                                      +0.524           +0.524          ✓
  mean pplausible base→rw                                                           0.797 → 0.862    0.797 → 0.862      ✓
  collateral (verdict flip plaus.→implaus.)                                             8/502            8/502          ✓

VideoPhy-2 AutoRater, rewrite side, per-clip scores (589 rows)
  joint % (All / Hard)                                                                 23.1/3.4          23.1/3.4       ✓
  mean SA (All / Hard)                                                                3.13/2.76         3.13/2.76       ✓
  mean PC (All / Hard)                                                                3.58/3.32         3.58/3.32       ✓
  SA ≥ 4 % (All / Hard)                                                                28.0/7.9          28.0/7.9       ✓
  PC ≥ 4 % (All / Hard)                                                               54.5/36.2         54.5/36.2       ✓

Table 11 Every number in Figure 13 and Table 6 recomputed independently from the run’s per-clip raw files, against
the reported value. All reproduce exactly. Two definitions are pinned by the recompute: collateral is a verdict flip
(plausible→implausible) on a non-flagged clip—8/502; scored instead as any decrease in pplausible it would be 31/502,
so the stricter reading is the one reported. The AutoRater baseline column of Table 6 is not in this check: the released
bundle synced only the rewrite-side per-clip scores and a 12-clip baseline subset, so the 600-clip baseline means are
corroborated by the run log rather than recomputed here. Baseline n = 600 and rewrite n = 589 (the 11 absent clips
did not complete regeneration or re-scoring), so the two columns of Table 6 rest on slightly different denominators.

and it improves by optimizing S. The reasoning model and the low-level physical experts are frozen, so what
the system accumulates is held in S, which is inspectable, diffable, versionable, and revertible. “Training” and
“inference” are one readable procedure applied in two directions: one map reads S to act, and channels write
to S (or to the generator) to improve.


                                                          37
O — operator library (procedural memory). A set of reusable, already-compiled measurement opera-
   tors. Each operator o ∈ O is a closure mapping a video and typed arguments to a physical measurement,
   and it carries an explicit cost node c(o) recording its spending (compute, expert calls, latency). O grows
   monotonically as recurring reasoning sub-procedures are packaged into named operators.
M — experience library (episodic + semantic memory). Versioned, human-readable priors distilled
   from past traces: nearest-neighbor plans for similar prompts and physics-failure priors over common
   defect modes. M keeps evidence (what was measured) separate from belief (what we now expect):
   evidence is retained as recorded, while belief is defeasible and is overridden by fresh measurement.
K — external knowledge channel. Retrieved external or social knowledge (physical facts, domain con-
   ventions, human corrections) admitted only through a candidate-and-pruning discipline. K is the
   deliberate open port that keeps the internal improvement loop from closing on itself (Section B.6).

The rest of the framework consists of two kinds of maps over this state: a single-episode read operator that
consumes S and emits an auditable trace (Section B.3), and write channels that update the generator and S
from that trace. The six design pillars of the paper are recovered as special cases of read-vs-write over S:
P1/P2 and the read side of P4 are “read S to produce a trace”; P3 and P6 are “write S”; P5 is “write the
generator”; and the supervisory side of P4 wraps the writes.

B.3   The single-episode operator (read path): physicalized ReAct as a program over O
Given a prompt–video pair (p, V ), one episode is a deterministic pipeline that only reads S:

                                    retrieve:   (πp , mp , kp ) = r(S, p),                                     (16)
                                    compile:    (C, G) = Reason(p, V | πp , mp , kp ),                         (17)
                               act–observe:     R = ExecO (G, V ),                                             (18)
                                 adjudicate:    (Y, F) = Φ(C, R),                                              (19)
                                       emit:    T = (C, G, R, Y, F ).                                          (20)

where the retrieval r reads from S the nearest-neighbour plan πp , the experience prior mp , and the external
knowledge kp relevant to prompt p. These maps are the abstract form of the critic of Section 4: (17) is the
claim-and-plan synthesis of (5), (18) the scoped execution of (8), and (19) the roll-up and packet of (10) and
(11). Here C is a set of typed physical obligations—explicit, machine-checkable statements of what the video
must satisfy to honor the prompt (object presence and count, contact and support, trajectory continuity, depth
ordering, on-screen text, audio events). G is a program over O: reasoning takes the form of a composition
of operator calls that the model writes and the runtime executes, in the tradition of program-of-thought
and modular visual reasoning [23, 35, 69, 78]. Executing G drives the classic reason→act→observe loop of
ReAct-style agents [85], but every act is a call into a frozen physical expert operator—promptable segmentation
and tracking [7], counting over its instance identities, the typed physical measurements taken over those tracks,
monocular depth, OCR, and audio event detection [24]—registered in O. This is the sense in which VeriPhy
specializes ReAct to physical measurement: it inherits the control-flow harness from mainstream tool-using
agents [60, 65] and specializes it with explicit physical obligations and physical-measurement operators (P1).
This general form is instantiated concretely by the critic of Section 4, which produces the same three-valued
verdict used there.
Each operator returns a measurement together with a gate on its own scope: when an operator’s preconditions
are not met (out-of-scope object, untrackable occlusion, no audio track), it emits abstain. The adjudicator Φ
in (19) is a deterministic roll-up from evidence R to a per-obligation verdict Y ∈ V|C| in the three-valued
codomain V = {S, C, U} of Section 4—one entry per obligation (supported, contradicted, or unknown)—plus a
contradiction packet F that localizes, for each unmet obligation, which measurement contradicts it and where.
unknown, and abstain for out-of-scope obligations, are first-class outcomes of the codomain, so declining to
certify is available to the critic as a verdict in its own right. The emitted trace T = (C, G, R, Y, F) carries full
provenance—every element of Y is back-traceable to the operator calls in G and the measurements in R.

CoT-as-program and cost nodes (P2). Because G is a program, recurring sub-procedures (e.g. “verify
a bounce = track the object, detect the contact frame, check the pre/post vertical-velocity sign flip”) can


                                                          38
be packaged, named, and re-registered as new
                                           P operators in O. Each operator carries its cost node c(o), so a
program has a well-defined budget c(G) = o∈G c(o) and the reasoner can trade breadth of measurement
against spending. Over many episodes O scales up into a growing procedural memory, and reasoning
increasingly becomes composition of trusted operators rather than re-derivation from scratch. What is
instantiated today is a fixed operator set O0 and a fixed compiler; the scaling-up of O via distillation is
roadmap (Section B.9).

B.4   The outward channel: verification-guided refinement (P5)
The read path produces, for a failed clip, a localized contradiction packet F (defined in Section 4.5). The
outward control channel maps F into a local edit ∆ctrl of the generator’s control signal and regenerates:

                               V ′ = Gen p, δ(F ) ,                                                      (21)
                                                     
                                                           δ : F 7−→ ∆ctrl ,

where Gen is the physics-guided pipeline of Section 3 (MuJoCo simulation [70] driving a Wan 2.2 video
model [71] through VACE control conditioning [33]), and δ(F) is an edit to the simulation and control
inputs addressing the violated obligation. Since the control signal is a rendered field over space and time,
a contradiction localized in both maps onto a local edit of the conditioning stream. The critic here is
independent and frozen, so the grading signal does not originate in the generator being graded, unlike
self-evaluating refinement loops [72] and verification-guided repair [12]. Both endpoints of (21) are built
(Section 3 and Section 5.3); the map δ and the closed loop are roadmap.

B.5   Auditability of the state and the trace
Auditability follows from the formalism. The learned object is the readable state S and every conclusion is a
deterministic roll-up Φ over provenance-carrying measurements, so any verdict Y replays back to the operator
calls in G and the measurements in R, and any state change S → S ′ is a human-readable diff of O, M , or
K. Weight-free self-evolution and its human supervision both rest on that property: the reviewer inspects
readable objects rather than gradients.
Auditability determines what a verdict can be taken to mean. A supported verdict is a critic judgment, where
the ground truth in this paper is human annotation. Determinism in the roll-up leaves evaluator drift in the
underlying operators and the compiler untouched. A prompt surviving the checks is plausible with respect to
the obligations tested, and a static critic improving says nothing about the generator.

B.6   Weight-free context-training self-evolution
The framework’s inward channel provides: a critic that improves itself without updating a weight. Everything
above—a readable state, a program over operators, provenance traces, an independent verdict—exists so that
the system’s own experience can be written into S under a guard. This inward context-training channel (P3)
is the last of the framework’s components to be instantiated.
Given a trace T and feedback ϕ (human labels, downstream outcomes, or a later, more complete measurement),
we distill a candidate state edit
                                     (∆O, ∆M, ∆K) = Distill(T, ϕ),                                   (22)
and accept it under a strict guard, the map Accept defined by (23) below. Both successful and failed episodes
are distilled (hindsight over traces [36, 57]): a success may add a plan to M or an operator to O; a failure
may add a physics-failure prior or a scope restriction. This form of self-evolution leaves weights unchanged,
in the spirit of context-distillation and experience-memory agents [6, 30, 57, 66, 79, 89, 90], and it treats
deployment-time adaptation as learning as state optimization. Acceptance is governed by
                                      (
                                       S ⊕ ∆, if Uval (S ⊕ ∆) > Uval (S),
                                  ′
                                S =                                                                      (23)
                                       S,        otherwise (do-nothing elitism),

where Uval is a held-out proxy score, ∆ = (∆O, ∆M, ∆K) is a distilled candidate edit from (22), and S ⊕ ∆
applies that edit component-wise to the state, appending the operator, plan and knowledge deltas to O, M


                                                     39
and K respectively. Candidates that do not strictly improve the proxy are pruned, and when none improves
it the state is left unchanged. That default makes the proxy monotone across updates, bounding how far a
distilled candidate can degrade S.

Admitting external knowledge (P6). A system whose only inputs are its own traces—CoT → feedback
→ context → CoT—is a closed loop that can amplify its own biases: distilled priors condition future reasoning,
whose traces distill into more priors. The external knowledge channel K is the opening provided for this.
VeriPhy may issue retrieval or ask for external or social knowledge (physical facts, human corrections, domain
conventions) and admit it into K under the same candidate-and-pruning discipline as (23): a retrieved
candidate is admitted only when it improves the held-out proxy, and K-sourced facts carry a provenance tag
distinct from distilled beliefs, so an admission can be reverted. External knowledge therefore enters under the
same elitism that governs S.
Every prior distilled into M is critic-derived : a summary of what VeriPhy’s own verification loop concluded
rather than verified truth. The external channel K is roadmap. The inward channel is instantiated, and
Section 5.4 measures it.

B.7   Distilling lessons from recorded misses
We instantiate (22) by distilling lessons from episodes in which a plan missed a human-recorded flaw and
appending them to the planner’s rubric, leaving the operator library O and external channel K untouched
so that S ′ = (O, M ′ , K). The measured effect on flaw recall—lessons distilled from recorded misses raise
held-out recall to 375 of 502 against 340 untaught, a gain already present from the smallest experience pool—is
reported with the other experiments in Section 5.4.

B.8   Human oversight
A human is kept in the loop at a few specific gates: a reviewer may audit a trace T , veto or edit a proposed
state update in (23), and approve whether a refined generation (21) or a new state S ′ is deployed. Human
feedback also enters Distill as a first-class signal ϕ. Because updates are readable diffs of S, oversight consists
of reading and approving them. The reviewing tooling and deployment protocol are roadmap; the artifacts
they act on — traces, three-valued state, provenance — exist today.

B.9   Built and roadmap components
Because all learning is state optimization on a readable S, we can mark built-vs-roadmap directly on the
formalism, and each pillar is one component of the same loop (Table 12). Instantiated today (Phase 0): the
frozen generator pipeline Gen (Section 3); the 1,500-clip defect benchmark that exercises the read path
(Section 5.1); the episode read operator (16)–(20) with a fixed operator set O0 , typed obligations C, three-
valued deterministic adjudication Φ, and provenance traces T ; the flaw-level measurement in Section 5.3
against human labels (228 of 304 for VeriPhy, 164 for question decomposition, recall-only, on the development
core, which is not held out); and the inward distillation of M via (22), measured on a held-out split in
Section 5.4 (375 of 502 against 340 untaught). Roadmap (Phase 1+): the outward control map δ and the closed
critic→generator loop (21); the scaling-up of O; the acceptance gate (23) that admits distilled candidates on
a measured proxy improvement; the external knowledge channel K; and human-in-the-loop deployment at
scale. Every roadmap item is a write path in the same formalism whose read counterpart is already exercised.
The executable plan follows in Section C.


C     An Executable Roadmap
The framework of Section B defines one learned object, the state S = (O, M, K), and three maps over it: a
read operator (built) and two write channels (roadmap). We phase the work accordingly. Phase 0 is the
read path and the two frozen endpoints already instantiated in this paper; Phase 1 moves the evaluation
onto a held-out split scored for precision as well as recall; Phases 2–6 exercise the write paths, each with a



                                                        40
 Pillar                                      Where it lives in the loop                        Status

 P1 Physical verification + opera-           compile / act–observe over frozen experts [7,     Phase 0 (built)
 tors                                        24]
 P2 CoT-as-program + cost nodes              program G over O, budget c(G)                     Phase 0 partial
 P4 Auditable trace + three-                 trace T = (C, G, R, Y, F ), provenance            Phase 0 (artifacts)
 valued Y
 P5 Verification-guided refinement           outward control channel δ, Gen                    roadmap
 P2+ Operator-library scale-up               procedural-memory growth in O                     roadmap
 P6 Breaking the loop                        external channel K, candidate+prune               roadmap
 P3 Context-training self-evolution          inward channel Distill (22)                       Phase 0 (measured, gate not
                                                                                               applied)
 P3+ Acceptance gate                         elitism (23) over distilled candidates            roadmap
 P4+ Human oversight                         supervision + deployment gate                     roadmap

Table 12 Each pillar is one component of the same loop. Only Phase 0 rows denote implemented artifacts or measured
analyses; solid arrows in Figure 22 correspond to them, dashed arrows to the roadmap rows, which are unmeasured.

                                  P4 human-in-the-loop: audit T · veto ∆S · gate deployment

                                   compile              act–observe             adjudicate           trace
                 (p,retrieve
                      V)
                                    (C, G)                ExecO                 Φ → (Y, F )    T =(C, G, R, Y, F )

                                                       frozen operators
           S = (O, M, K)                          SAM3 grounding + tracks
      O operators (procedural)                    11 typed measures / Depth
                                                                                                              δ(F ) control edit (P5)
      M experience K external                          OCR / FlexSED
                                                                                              (T, ϕ)
     human-readable, versionable
                      V ′ regenerate


                                                                                                        Gen
                                                                                              MuJoCo→Wan2.2-VACE
                       S′
   external / social knowledge                  Distill → (∆O, ∆M, ∆K)
            · retrieval                 held-out proxy prune + do-nothing elitism (P3)
      candidate+prune gate (P6)

          Built (Phase 0)              Roadmap (Phase 1+)


Figure 22 State-optimization view of VeriPhy. Everything the system learns lives in one human-readable state
S = (O, M, K). A single read operator (top, solid = built) conditions on S, compiles (p, V ) into typed obligations
C and a program G over O, runs frozen physical operators, and emits a provenance-carrying three-valued trace
T . Two structurally dual write channels (dashed = roadmap), both driven by the same independent frozen critic,
close the loop: the outward control channel edits the generator’s control signal via δ(F) and regenerates (P5); the
inward context-training channel distills T into candidate state edits accepted only under held-out proxy pruning with
do-nothing elitism (P3). The external channel K breaks the internal loop (P6). A human-in-the-loop layer wraps both
channels (P4). Solid arrows are instantiated in Section 3 and Sections 5.1 and 5.3; dashed arrows are the roadmap of
Section C.

measurable success metric and each a strict superset of what precedes it. No number below the Phase 0 line
is a result; Phases 1+ state targets and protocols, not outcomes.

Phase 0 — Built: the read path and frozen endpoints (done).

   • Delivered. The physics-guided generator Gen (MuJoCo → Wan2.2-VACE, Section 3); the 1500-clip
     human-authored defect benchmark (Section 5.1); the episode read operator with fixed O0 , typed
     obligations C, three-valued deterministic adjudication Φ, and provenance traces T (Section 4); and
     the flaw-level measurement against human labels (228 of 304 for VeriPhy against 164 for question
     decomposition, on the development core, non-held-out, Section 5.3).
   • Covers. P1 (physical-verification read path), and the read side of P2 (programs over O0 ) and P4
     (provenance traces).


                                                                   41
  • Honest limits. Recall-only, single non-held-out split; critic verdicts are judgments scored against human
    labels, not ground truth; a static evaluator result is not evidence any generator improved; the two write
    channels are not yet exercised.

Phase 1 — Held-out, precision+recall evaluation with provenance completeness.

  • Goal. Promote the critic result from dev-core / recall-only to a held-out, precision+recall protocol, and
    guarantee every verdict carries a complete provenance trace T .
  • Needs. A frozen held-out split of the benchmark disjoint from dev-core; a provenance schema for
    (C, G, R, Y, F ).
  • Experiments. Plan-based vs. per-claim adjudication on held-out clips with full confusion matrices; audit
    that every contradicted verdict localizes to frame-level evidence via F .
  • Success metric. Held-out plan-based accuracy ≥ per-claim with non-degrading precision; complete
    provenance coverage.
  • Risk. Held-out gap reveals dev-core overfitting; the three-valued codomain inflates unknown to dodge
    hard cases — mitigate by reporting the unknown rate alongside accuracy.

Phase 2 — Operator library with cost accounting (P2).

  • Goal. Turn fixed O0 into a growing, versioned O whose operators carry cost nodes c(o) and whose
    programs have measurable budgets c(G).
  • Needs. An operator registry with provenance and versioning; a compiler that detects recurring G-
    sub-programs and promotes them into named operators; per-operator cost instrumentation wired into
    Φ.
  • Experiments. Track the coverage/cost frontier as |O| grows; ablate frozen O0 vs. promoted O at matched
    budget.
  • Success metric. A Pareto improvement in obligation coverage per unit cost over the Phase 0 fixed
    pipeline at equal or lower c(G).
  • Risk. Library bloat and stale operators; promoted operators encode clip-specific shortcuts — mitigate
    with usage-frequency thresholds and held-out re-validation before promotion.

Phase 3 — Context-training self-evolution of M (P3).

  • Goal. Distill traces (success and failure) into human-readable, versionable priors in M — nearest-neighbor
    plans and physics-failure priors — accepted under held-out proxy pruning with do-nothing elitism (23),
    keeping evidence separate from belief.
  • Needs. A distillation function Distill; a held-out validation split Uval (new data, disjoint from the
    Phase 0/1 core); a diffable memory store.
  • Experiments. Compare {no memory, retrieval-only, distilled M with elitism, distilled M without elitism}
    on the held-out split; a pollution stress test injecting wrong priors and checking elitism rejects them.
  • Success metric. Monotone non-decreasing held-out proxy across accepted updates, a positive gap of “M
    with elitism” over both baselines, and zero acceptance of injected harmful priors.
  • Risk. Belief leaking into evidence, or proxy overfitting; mitigate with the evidence/belief split and
    periodic held-out refresh.

Phase 4 — Closing the control channel critic → generator (P5).

  • Goal. Implement δ : F 7→ ∆ctrl of (21), converting a contradiction packet into a targeted local edit of
    the MuJoCo/VACE control signal, and regenerate.
  • Needs. A parameterization of Wan2.2-VACE control inputs by obligation type; a differentiable-or-
    heuristic edit policy δ; a re-adjudication harness.




                                                    42
   • Experiments. On clips with contradicted verdicts, compare {blind resampling, prompt-only edit, targeted
     δ(F) edit}; report the fraction of previously violated obligations that flip to supported after regeneration,
     human-verified, and re-run the full obligation set C post-edit to report net defect change.
   • Success metric. Targeted δ(F) regeneration repairs a significantly higher fraction of localized violations
     than blind resampling at equal generation budget, confirmed by human annotation (not by the critic
     alone), with no rise in unrelated-obligation contradictions.
   • Risk. Goodharting the critic or whack-a-mole edits that fix one obligation while breaking another;
     mitigated by human verification and the net-defect audit.

Phase 5 — Breaking the loop with external knowledge K (P6).

   • Goal. Open the internal CoT→feedback→context loop by admitting external/social knowledge and
     retrieval into K under the same candidate-and-pruning discipline, with a do-nothing fallback.
   • Needs. A retrieval/ingestion interface; a candidate gate scored by Uval ; provenance tagging that marks
     K-sourced facts distinctly from distilled beliefs.
   • Experiments. On a bias-probe subset (defect modes under-represented in the internal traces), compare
     closed-loop (K = ∅) vs. open-loop (K admitted with gating); a noise-injection test on retrieved sources.
   • Success metric. Reduced error on the bias-probe subset with no regression on the general held-out split;
     zero admissions when no candidate improves the proxy (fallback correctness).
   • Risk. Context pollution from noisy or off-distribution sources; mitigated by the same elitism gate as S,
     plus source provenance so bad admissions are revertible.

Phase 6 — Human-in-the-loop deployment at scale (P4).

   • Goal. Operate both channels under human supervision: reviewers audit traces T , veto/edit candidate
     state updates, and gate deployment of refined generations and new states S ′ .
   • Needs. Trace-replay and state-diff review tooling; an approval workflow feeding Distill and K; audit
     logs over S → S ′ with rollback.
   • Experiments. Held-out study measuring reviewer time per audited trace, inter-annotator agreement on
     state-update acceptance and on three-valued verdicts, and the catch-rate of injected bad updates that
     elitism alone would have missed.
   • Success metric. Auditing cost per trace low enough to be practical, with human review reliably catching
     a measurable residual of harmful updates beyond the automatic gate.
   • Risk. Reviewer fatigue and rubber-stamping (which would reintroduce an unaudited closed loop);
     mitigate by surfacing only elitism-borderline updates for human attention.

Ordering rationale. Phase 1 secures the evaluation; Phases 2–3 grow the two components of S that the inward
channel writes (O, M ); Phase 4 exercises the outward channel; Phase 5 opens K; Phase 6 wraps everything
in human oversight. Each phase reuses the Phase 0 read path unchanged, so at every step the system remains
weight-free and auditable by construction.




                                                       43
References
 [1] James F. Allen. Maintaining knowledge about temporal intervals. Communications of the ACM, 26(11):832–843, 1983. doi:
     10.1145/182.358434.
 [2] Xiangyu Bai, He Liang, Bishoy Galoaa, Utsav Nandi, Shayda Moezzi, Yuhang He, and Sarah Ostadabbas. Moregen: Multi-
     agent motion-reasoning engine for code-based text-to-video synthesis. In CVPR, pages 7632–7642, 2026. arXiv:2512.04221.
 [3] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang, Yizhou Sun,
     Kai-Wei Chang, and Aditya Grover. Videophy: Evaluating physical commonsense for video generation. arXiv preprint
     arXiv:2406.03520, 2024.
 [4] Hritik Bansal, Clark Peng, Yonatan Bitton, Roman Goldenberg, Aditya Grover, and Kai-Wei Chang. Videophy-2: A
     challenging action-centric physical commonsense evaluation in video generation. In International Conference on Learning
     Representations (ICLR), 2026. Conference version; arXiv:2503.06800.
 [5] Giulio Biroli, Tony Bonnaire, Valentin de Bortoli, and Marc Mézard. Dynamical regimes of diffusion models. Nature
     Communications, 15:9957, 2024.
 [6] Weihao Bo, Shan Zhang, Yanpeng Sun, Jingjing Wu, Qunyi Xie, Xiao Tan, Kunbin Chen, Wei He, Xiaofan Li, Na Zhao,
     Jingdong Wang, and Zechao Li. ViLoMem: Agentic learner with grow-and-refine multimodal semantic memory. In
     IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2026. arXiv:2511.21678. Dual-stream
     visual/logical error distillation, grow-and-refine (merge/create), no weight update.
 [7] Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Dídac Surís, et al. Sam 3: Segment
     anything with concepts. arXiv preprint arXiv:2511.16719, 2025. Open-vocabulary concept segmentation/tracking; used by
     the relation depth arm.
 [8] Yongfan Chen, Xiuwen Zhu, and Tianyu Li. A physical coherence benchmark for evaluating video generation models via
     optical flow-guided frame prediction. arXiv preprint arXiv:2502.05503, 2025.
 [9] Aditya Chinchure, Sahithya Ravi, Pushkar Shukla, Vered Shwartz, and Leonid Sigal. Spotlight: Identifying and localizing
     video generation errors using VLMs. In European Conference on Computer Vision (ECCV), 2026. arXiv:2511.18102.
[10] Jaemin Cho, Yushi Hu, Roopal Garg, Peter Anderson, Ranjay Krishna, Jason Baldridge, Mohit Bansal, Jordi Pont-Tuset,
     and Su Wang. Davidsonian scene graph: Improving reliability in fine-grained evaluation for text-to-image generation. In
     ICLR, 2024. arXiv:2310.18235.
[11] Jooyoung Choi, Jungbeom Lee, Chaehun Shin, Sungwon Kim, Hyunwoo Kim, and Sungroh Yoon. Perception prioritized
     training of diffusion models. In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022.
[12] Minkyu Choi, S P Sharan, Harsh Goel, Sahil Shah, and Sandeep Chinchali. We’ll fix it in post: Improving text-to-video
     generation with neuro-symbolic feedback. arXiv preprint arXiv:2504.17180, 2025.
[13] Rohan Choudhury, Koichiro Niinuma, Kris M. Kitani, and László A. Jeni. Video question answering with procedural
     programs. In ECCV, pages 315–332, 2024. arXiv:2312.00937; the video analogue of ViperGPT.
[14] Zijun Cui, Xiulong Liu, Hao Fang, Mingwei Xu, Jiageng Liu, Zexin Xu, Weiguo Pian, Shijian Deng, Feiyu Du, Chenming
     Ge, and Yapeng Tian. Do joint audio-video generation models understand physics? arXiv preprint arXiv:2605.07061, 2026.
     Introduces AV-Phys Bench and AV-Phys Agent.
[15] Yufan Deng, Zilin Pan, Hongyu Zhang, Xiaojie Li, Ruoqing Hu, Yufei Ding, Yiming Zou, Yan Zeng, and Daquan Zhou.
     Rethinking video generation model for the embodied world. In International Conference on Machine Learning (ICML),
     2026.
[16] Du et al. Collaborative few-step distillation and low-bit quantization for Wan2.2 dual-expert video diffusion models. arXiv
     preprint arXiv:2606.00658, 2026.
[17] Yue Fan, Xiaojian Ma, Rujie Wu, Yuntao Du, Jiaqi Li, Zhi Gao, and Qing Li. Videoagent: A memory-augmented multimodal
     agent for video understanding. In ECCV, 2024. arXiv:2403.11481.
[18] Arduin Findeis, Floris Weers, Guoli Yin, Ke Ye, Ruoming Pang, and Tom Gunter. Can external validation tools improve
     annotation quality for LLM-as-a-judge? In Proceedings of the 63rd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), pages 15997–16020. Association for Computational Linguistics, 2025. doi: 10.18653/
     v1/2025.acl-long.779. https://aclanthology.org/2025.acl-long.779/.
[19] Lin Geng Foo, Mark He Huang, Alexandros Lattas, Stylianos Moschoglou, Thabo Beeler, and Christian Theobalt. Physical
     simulator in-the-loop video generation. In CVPR, pages 4301–4311, 2026. arXiv:2603.06408.
[20] Hiroki Furuta, Heiga Zen, Dale Schuurmans, Aleksandra Faust, Yutaka Matsuo, Percy Liang, and Sherry Yang. Improving
     dynamic object interactions in text-to-video generation with ai feedback. arXiv preprint arXiv:2412.02617, 2024.
[21] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu Chen. Critic: Large language
     models can self-correct with tool-interactive critiquing. In ICLR, 2024. arXiv:2305.11738.




                                                              44
[22] Jing Gu, Xian Liu, Yu Zeng, Ashwin Nagarajan, Fangrui Zhu, Daniel Hong, Yue Fan, Qianqi Yan, Kaiwen Zhou, Ming-Yu
     Liu, and Xin Eric Wang. Phyworldbench: A comprehensive evaluation of physical realism in text-to-video models. In ICLR,
     2026. Oral; arXiv:2507.13428.
[23] Tanmay Gupta and Aniruddha Kembhavi. Visual programming: Compositional visual reasoning without training. In CVPR,
     2023. arXiv:2211.11559.
[24] Jiarui Hai, Helin Wang, Weizhe Guo, and Mounya Elhilali. Flexsed: Towards open-vocabulary sound event detection. arXiv
     preprint arXiv:2509.18606, 2025. Text-queryable sound-event detection with timestamps; the audio arm.
[25] Hui Han, Siyuan Li, Jiaqi Chen, Yiwen Yuan, Yuling Wu, Yufan Deng, Chak Tou Leong, Hanwen Du, Junchen Fu, Youhua Li,
     Jie Zhang, Chi Zhang, Li-jia Li, and Yongxin Ni. Video-bench: Human-aligned video generation benchmark. In IEEE/CVF
     Conference on Computer Vision and Pattern Recognition (CVPR), pages 18858–18868, 2025. arXiv:2504.04907.
[26] Xuan He, Dongfu Jiang, Ge Zhang, Max Ku, Achint Soni, et al. Videoscore: Building automatic metrics to simulate
     fine-grained human feedback for video generation. In EMNLP, 2024. arXiv:2406.15252.
[27] Xuan He, Dongfu Jiang, Ping Nie, Minghao Liu, Zhengxuan Jiang, et al. Videoscore2: Think before you score in generative
     video evaluation. arXiv preprint arXiv:2509.22799, 2025.
[28] Yushi Hu, Benlin Liu, Jungo Kasai, Yizhong Wang, Mari Ostendorf, Ranjay Krishna, and Noah A. Smith. TIFA: Accurate
     and interpretable text-to-image faithfulness evaluation with question answering. In ICCV, 2023. arXiv:2303.11897.
[29] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Yue Liao, Peng Gao, Hongsheng Li,
     Maoqing Yao, and Guanghui Ren. EnerVerse: Envisioning embodied future space for robotics manipulation. In Advances in
     Neural Information Processing Systems (NeurIPS), volume 38, 2025.
[30] Zeyu Huang, Adhiguna Kuncoro, Qixuan Feng, Jiajun Shen, Lucio Dery, Arthur Szlam, and Marc’Aurelio Ranzato. Context
     training with active information seeking. arXiv preprint arXiv:2605.13050, 2026. Learning as state optimization: edits a
     human-readable context, weights frozen; candidate-and-prune discipline against context pollution.
[31] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang
     Jin, Nattapol Chanpaisit, Yaohui Wang, Xinyuan Chen, Limin Wang, Dahua Lin, Yu Qiao, and Ziwei Liu. VBench:
     Comprehensive benchmark suite for video generative models. In CVPR, 2024. arXiv:2311.17982.
[32] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, et al. DreamGen: Unlocking generalization in robot
     learning through video world models. In Conference on Robot Learning (CoRL), pages 5170–5194, 2025.
[33] Zeyinzi Jiang, Zhen Han, Chaojie Mao, Jingfeng Zhang, Yulin Pan, and Yu Liu. Vace: All-in-one video creation and editing.
     arXiv preprint arXiv:2503.07598, 2025. Mask-conditioned controllable video generation; the project’s stylizer.
[34] Sayash Kapoor, Benedikt Stroebl, Peter Kirgis, Nitya Nadgir, Zachary S. Siegel, Boyi Wei, Tianci Xue, Ziru Chen, Felix
     Chen, et al. Holistic agent leaderboard: The missing infrastructure for AI agent evaluation. In International Conference on
     Learning Representations (ICLR), 2026. https://openreview.net/forum?id=vUaY1t64ZZ.
[35] Sehoon Kim, Suhong Moon, Ryan Tabrizi, Nicholas Lee, Michael W. Mahoney, Kurt Keutzer, and Amir Gholami. An
     llm compiler for parallel function calling. In ICML, 2024. arXiv:2312.04511. Plans a DAG of function calls, dispatches
     independent calls in parallel.
[36] Chris Latimer, Nicoló Boschi, Chris Bartholomew, Andrew Neeser, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan.
     Hindsight is 20/20: Building agent memory that retains, recalls, and reflects. arXiv preprint arXiv:2512.12818, 2026.
     Separates observed evidence from inferred belief; confidence-reinforced, traceable updates.
[37] Daeun Lee, Jaehong Yoon, Jaemin Cho, and Mohit Bansal. Self-correcting text-to-video generation with misalignment
     detection and localized refinement. In Findings of ACL, pages 36464–36489, 2026. doi: 10.18653/v1/2026.findings-acl.1817.
[38] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang, Hongxu Yin,
     Joseph E. Gonzalez, Ion Stoica, Song Han, and Yao Lu. WorldModelBench: Judging video generation models as world
     models. In Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track, volume 38,
     2025.
[39] Keliang Li, Yansong Li, Hongze Shen, Mengdi Liu, Hong Chang, and Shiguang Shan. Lenswalk: Agentic video understanding
     by planning how you see in videos. In CVPR, pages 19518–19528, 2026. arXiv:2603.24558.
[40] Marvin Li and Sitan Chen. Critical windows: non-asymptotic theory for feature emergence in diffusion models. arXiv
     preprint arXiv:2403.01633, 2024.
[41] Jiafeng Liang, Hao Li, Chang Li, Jiaqi Zhou, Shixin Jiang, Zekun Wang, Changkai Ji, Zhihao Zhu, Runxuan Liu, Tao
     Ren, Jinlan Fu, See-Kiong Ng, Xia Liang, Ming Liu, and Bing Qin. AI meets brain: Memory systems from cognitive
     neuroscience to autonomous agents. arXiv preprint arXiv:2512.23343, 2026. Survey aligning cognitive-neuroscience memory
     with LLM/agent memory; expert-model symbolization of dense frames, procedural/strategic self-evolution.
[42] Juyi Lin, Arash Akbari, Yumei He, Lin Zhao, Haichao Zhang, et al. PhyGround: Benchmarking physical reasoning in
     generative world models. arXiv preprint arXiv:2605.10806, 2026.
[43] Zhiqiu Lin, Deepak Pathak, Baiqi Li, Jiayao Li, Xide Xia, Graham Neubig, Pengchuan Zhang, and Deva Ramanan.
     Evaluating text-to-visual generation with image-to-text generation. In ECCV, 2024. VQAScore. arXiv:2404.01291.


                                                              45
[44] Fangfu Liu, Hanyang Wang, Yimo Cai, Kaiyan Zhang, Xiaohang Zhan, and Yueqi Duan. Video-t1: Test-time scaling for
     video generation. In ICCV, pages 18671–18681, 2025.
[45] Shaowei Liu, Zhongzheng Ren, Saurabh Gupta, and Shenlong Wang. Physgen: Rigid-body physics-grounded image-to-video
     generation. In ECCV, pages 360–378, 2024.
[46] Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng, Raymond Chan,
     and Ying Shan. EvalCrafter: Benchmarking and evaluating large video generation models. In CVPR, 2024. arXiv:2310.11440.
[47] Yuanxin Liu, Lei Li, Shuhuai Ren, Rundong Gao, Shicheng Li, Sishuo Chen, Xu Sun, and Lu Hou. FETV: A benchmark for
     fine-grained evaluation of open-domain text-to-video generation. In NeurIPS, 2023. arXiv:2311.01813.
[48] Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. Seeing, listening, remembering,
     and reasoning: A multimodal agent with long-term memory. In International Conference on Learning Representations
     (ICLR), 2026. arXiv:2508.09736. M3-Agent: entity-centric multimodal memory graph over per-clip observations with
     multi-turn retrieval.
[49] Wei Luo et al. LoViF 2026: The first challenge on holistic quality assessment for 4d world model (PhyScore): Methods and
     results. In IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), pages 5008–5017,
     2026.
[50] Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon. SDEdit: Guided
     image synthesis and editing with stochastic differential equations. In International Conference on Learning Representations
     (ICLR), 2022.
[51] Fanqing Meng, Jiaqi Liao, Xinyu Tan, Quanfeng Lu, Wenqi Shao, Kaipeng Zhang, Yu Cheng, Dianqi Li, and Ping Luo.
     Towards world simulator: Crafting physical commonsense-based benchmark for video generation. In International Conference
     on Machine Learning (ICML), pages 43781–43806, 2025. Introduces the PhyGenBench benchmark; arXiv:2410.05363.
[52] Sachit Menon, Ahmet Iscen, Arsha Nagrani, Tobias Weyand, Carl Vondrick, and Cordelia Schmid. Caviar: Critic-augmented
     video agentic reasoning. arXiv preprint arXiv:2509.07680, 2025.
[53] Juhong Min, Shyamal Buch, Arsha Nagrani, Minsu Cho, and Cordelia Schmid. Morevqa: Exploring modular reasoning
     models for video question answering. In CVPR, 2024. arXiv:2404.06511.
[54] Antonio Montanaro, Luca Savant Aira, Emanuele Aiello, Diego Valsesia, and Enrico Magli. Motioncraft: Physics-based
     zero-shot video generation. In NeurIPS, 2024.
[55] Saman Motamed, Laura Culp, Kevin Swersky, Priyank Jaini, and Robert Geirhos. Do generative video models understand
     physical principles? In IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), pages 948–958, 2026.
     Physics-IQ; arXiv:2501.09038.
[56] Sriram Narayanan, Ziyu Jiang, Srinivasa Narasimhan, and Manmohan Chandraker. Phyco: Learning controllable physical
     priors for generative motion. In CVPR, pages 41892–41902, 2026. arXiv:2604.28169.
[57] Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki,
     Xiangru Tang, Vishy Tirumalashetty, George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, and Tomas
     Pfister. ReasoningBank: Scaling agent self-evolving with reasoning memory. In International Conference on Learning
     Representations (ICLR), 2026. arXiv:2509.25140. Distills reusable reasoning strategies across episodes.
[58] Qwen Team. Qwen3-vl technical report. arXiv preprint arXiv:2511.21631, 2025. The vision-language reasoner (Qwen3-VL-
     30B-A3B-Instruct) at the centre of the critic.
[59] Prasan Roy, S. Seshadri, S. Sudarshan, and Siddhesh Bhobe. Efficient and extensible algorithms for multi query optimization.
     In SIGMOD, 2000. Practical shared-subexpression MQO in a Volcano-style optimizer.
[60] Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola
     Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. In NeurIPS, 2023.
     arXiv:2302.04761.
[61] Antonio Sclocchi, Alessandro Favero, and Matthieu Wyart. A phase transition in diffusion models reveals the hierarchical
     nature of data. arXiv preprint arXiv:2402.16991, 2024.
[62] Timos K. Sellis. Multiple-query optimization. ACM Transactions on Database Systems (TODS), 13(1):23–52, 1988.
     Foundational MQO: optimize a batch of queries jointly via shared sub-expressions.
[63] Yu Shang, Xin Zhang, Yinzhou Tang, Lei Jin, Chen Gao, Wei Wu, and Yong Li. RoboScape: Physics-informed embodied
     world model. In Advances in Neural Information Processing Systems (NeurIPS), volume 38, 2025.
[64] S P Sharan, Minkyu Choi, Sahil Shah, Harsh Goel, Mohammad Omama, and Sandeep Chinchali. Neuro-symbolic evaluation
     of text-to-video models using formal verification. In CVPR, pages 8395–8405, 2025. arXiv:2411.16718.
[65] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang. Hugginggpt: Solving ai tasks with
     chatgpt and its friends in hugging face. In NeurIPS, 2023. arXiv:2303.17580.
[66] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with
     verbal reinforcement learning. In NeurIPS, 2023. arXiv:2303.11366.



                                                              46
[67] Sanjay Subramanian, Medhini Narasimhan, Kushal Khangaonkar, Kevin Yang, Arsha Nagrani, Cordelia Schmid, Andy Zeng,
     Trevor Darrell, and Dan Klein. Modular visual question answering via code generation. In ACL, 2023. arXiv:2306.05392.
[68] Kaiyue Sun, Kaiyi Huang, Xian Liu, Yue Wu, Zihan Xu, Zhenguo Li, and Xihui Liu. T2V-CompBench: A comprehensive
     benchmark for compositional text-to-video generation. arXiv preprint arXiv:2407.14505, 2024.
[69] Dídac Surís, Sachit Menon, and Carl Vondrick. Vipergpt: Visual inference via python execution for reasoning. In ICCV,
     2023. arXiv:2303.08128.
[70] Emanuel Todorov, Tom Erez, and Yuval Tassa. MuJoCo: A physics engine for model-based control. In IEEE/RSJ
     International Conference on Intelligent Robots and Systems (IROS), 2012.
[71] Wan Team. Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314, 2025. The
     Wan 2.1 open video-diffusion backbone.
[72] Qian Wang, Ziqi Huang, Ruoxi Jia, Paul Debevec, and Ning Yu. MAViS: A multi-agent framework for long-sequence video
     storytelling. arXiv preprint arXiv:2508.08487, 2025. Explore-Examine-Enhance closed loop: evaluator feedback rewrites
     prompts and regenerates. Generator-side self-evaluation.
[73] Shuai Wang, Yaxin Feng, Xuekun Jiang, Shihan Tian, Ningyu Yan, et al. GAUGE: A measurement-grounded benchmark
     for physical fidelity in simulation engines and video world models. arXiv preprint arXiv:2608.05948, 2026. Posted 6 August
     2026; use only in revisions dated August 2026 or later.
[74] Xiang Wang, Hangjie Yuan, Shiwei Zhang, Dayou Chen, Jiuniu Wang, Yingya Zhang, Yujun Shen, Deli Zhao, and Jingren
     Zhou. VideoComposer: Compositional video synthesis with motion controllability. Advances in Neural Information
     Processing Systems (NeurIPS), 2023.
[75] Xiaohan Wang, Yuhui Zhang, Orr Zohar, and Serena Yeung-Levy. Videoagent: Long-form video understanding with large
     language model as agent. In ECCV, 2024. arXiv:2403.10517.
[76] Ziyang Wang, Shoubin Yu, Elias Stengel-Eskin, Jaehong Yoon, Feng Cheng, Gedas Bertasius, and Mohit Bansal. Videotree:
     Adaptive tree-based video representation for llm reasoning on long videos. In CVPR, 2025. arXiv:2405.19209.
[77] Tianxin Xie, Wentao Lei, Kai Jiang, Guanjie Huang, Pengfei Zhang, et al. PhyAVBench: A challenging audio physics-
     sensitivity benchmark for physically grounded text-to-audio-video generation. arXiv preprint arXiv:2512.23994, 2025.
[78] Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata Mukherjee, Yuchen Liu, and Dongkuan Xu. Rewoo: Decoupling
     reasoning from observations for efficient augmented language models. arXiv preprint arXiv:2305.18323, 2023. Plan-up-front,
     then execute; the ReWOO plan-execute separation.
[79] Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: Agentic memory for LLM agents.
     In Advances in Neural Information Processing Systems (NeurIPS), 2025. arXiv:2502.12110. Persistent, self-organizing
     episodic store.
[80] Qiyao Xue, Xiangyu Yin, Boyuan Yang, and Wei Gao. Phyt2v: Llm-guided iterative self-refinement for physics-grounded
     text-to-video generation. In CVPR, pages 18826–18836, 2025. arXiv:2412.00596.
[81] Ke Yang, Zixi Chen, Xuan He, Jize Jiang, Michel Galley, Chenglong Wang, Jianfeng Gao, Jiawei Han, and ChengXiang
     Zhai. PlugMem: A task-agnostic plugin memory module for LLM agents. arXiv preprint arXiv:2603.03296, 2026. Distills
     trajectories into a knowledge-centric graph of propositional facts and prescriptive workflows with provenance edges.
[82] Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao Ge, Xiu Li, and Ying Shan. Gpt4tools: Teaching large language model to
     use tools via self-instruction. In NeurIPS, 2023. arXiv:2305.18752.
[83] Xindi Yang, Baolu Li, Yiming Zhang, Zhenfei Yin, Lei Bai, Liqian Ma, Zhiyong Wang, Jianfei Cai, Tien-Tsin Wong, Huchuan
     Lu, and Xu Jia. Vlipp: Towards physically plausible video generation with vision and language informed physical prior. In
     ICCV, pages 12360–12370, 2025. arXiv:2503.23368.
[84] Yuhang Yang, Ke Fan, Shangkun Sun, Hongxiang Li, Ailing Zeng, FeiLin Han, Wei Zhai, Wei Liu, Yang Cao, and Zheng-Jun
     Zha. Videogen-eval: Agent-based system for video generation evaluation. arXiv preprint arXiv:2503.23452, 2025.
[85] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing
     reasoning and acting in language models. In ICLR, 2023. arXiv:2210.03629.
[86] Ke Zhang, Cihan Xiao, Jiacong Xu, Yiqun Mei, and Vishal M. Patel. Think before you diffuse: Infusing physical rules into
     video diffusion. arXiv preprint arXiv:2505.21653, 2025.
[87] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In
     IEEE/CVF International Conference on Computer Vision (ICCV), 2023.
[88] Qin Zhang, Peiyu Jing, Hong-Xing Yu, Fangqiang Ding, Fan Nie, Weimin Wang, Yilun Du, James Zou, Jiajun Wu, and Bing
     Shuai. Physion-eval: Evaluating physical realism in generated video via human reasoning. arXiv preprint arXiv:2603.19607,
     2026.
[89] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A
     survey on the memory mechanism of large language model based agents. arXiv preprint arXiv:2404.13501, 2024. Landscape
     reference for agent memory; VeriPhy maintains none.



                                                              47
[90] Zeyu Zhang, Yang Zhang, Haoran Tan, Rui Li, and Xu Chen. Explicit v.s. implicit memory: Exploring multi-hop complex
     reasoning over personalized information. In ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD),
     2026. arXiv:2508.13250. Evidence that explicit external retrievable memory outperforms implicit weight-internalized memory.
[91] Artem Zholus, Carl Doersch, Yi Yang, Skanda Koppula, Viorica Patraucean, Xu He, Ignacio Rocco, Mehdi S. M. Sajjadi,
     Sarath Chandar, and Ross Goroshin. Tapnext: Tracking any point (tap) as next token prediction. arXiv preprint
     arXiv:2504.05579, 2025. The point-tracking backbone behind the kinematic (physics) arm’s TAPNext++.
[92] Ziwei Zhou, Zeyuan Lai, Rui Wang, Yifan Yang, Zhen Xing, Yuqing Yang, Qi Dai, Lili Qiu, and Chong Luo. AVGen-Bench:
     A task-driven benchmark for multi-granular evaluation of text-to-audio-video generation. arXiv preprint arXiv:2604.08540,
     2026.




                                                              48
