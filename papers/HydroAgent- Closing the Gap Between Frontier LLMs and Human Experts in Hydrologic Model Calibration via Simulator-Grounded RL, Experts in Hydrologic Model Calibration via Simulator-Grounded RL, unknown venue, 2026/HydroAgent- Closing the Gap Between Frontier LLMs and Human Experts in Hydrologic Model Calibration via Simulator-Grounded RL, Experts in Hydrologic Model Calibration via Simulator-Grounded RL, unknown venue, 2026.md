                                             HydroAgent: Closing the Gap Between Frontier LLMs and Human
                                            Experts in Hydrologic Model Calibration via Simulator-Grounded RL
                                         Zhi Li1 , Songkun Yan2 , Jie Cao3 , Mofan Zhang4 , Anjiang Wei5 , Jinwoong Yoo6 , Yang Hong2
                                              1
                                                Civil, Environmental, and Architectural Engineering, University of Colorado Boulder
                                                      2
                                                        Civil Engineering and Environmental Sciences, University of Oklahoma
                                                              3
                                                                Department of Computer Science, University of Oklahoma
                                                              4
                                                                Civil and Environmental Engineering, Stanford University
                                                                 5
                                                                   Department of Computer Science, Stanford University
                                                                          6
                                                                            NASA Goddard Space Flight Center
                                                                                Correspondence: Zhi.Li-2@colorado.edu


                                                               Abstract
arXiv:2605.17792v1 [cs.LG] 18 May 2026




                                                                                                          the multi-modal richness of Earth data—remote
                                                                                                          sensing, in-situ time series, and forecaster
                                             Calibrating distributed hydrologic models is
                                                                                                          narrative—makes domain agents an unusually
                                             a critical bottleneck across operational water-
                                                                                                          leveraged direction for AI in physical science.
                                             resources management—streamflow prediction,
                                             water-supply assessment, reservoir operation,
                                             drought monitoring, infrastructure design, and           1   Introduction
                                             flood forecasting all depend on it: each basin
                                             demands a domain expert to translate hydro-              Hydrologic models are the infrastructure layer be-
                                             graph signatures into adjustments of a high-             neath a remarkable amount of public life—they
                                             dimensional parameter vector, and the resulting          are how human society manages water. Every
                                             workflow does not transfer between watersheds.           reservoir release a water utility schedules, every
                                             We ask a sharper version of a now-common                 irrigation allotment a basin authority issues, ev-
                                             question: can frontier large language model              ery drought outlook a farmer plans against, ev-
                                             (LLM) agents replace the human hydrologic
                                                                                                      ery hydropower bid a grid operator submits, ev-
                                             modeler, and if not, what would it take? We
                                             benchmark nine frontier LLM agents—Claude                ery wastewater-treatment design a city engineer
                                             Opus 4.6/4.7, Sonnet 4.6, GPT-5/5.4/5.4-pro,             approves, and every flash-flood watch a forecaster
                                             and Gemini 2.5-pro/3.1-pro/3-flash—on the                issues derives from a numerical rainfall-runoff
                                             calibration of the operational CREST dis-                model that has been calibrated, in advance, against
                                             tributed hydrologic model used by the U.S.               historical streamflow at the relevant gauge. The
                                             National Weather Service for flash-flood fore-           stakes are not abstract: flooding is the deadliest
                                             casting. Mean best-of-twenty-rounds Nash–
                                                                                                      weather hazard in the United States (Li et al., 2021)
                                             Sutcliffe Efficiency (NSE) across four held-out
                                             gauges spanning 329–40,792 km2 ranges from               and among the costliest natural disasters globally,
                                             −0.16 (GPT-5.4) to 0.75 (Sonnet 4.6); the ceil-          with more than 1.8 billion people directly exposed
                                             ing is reproducible across all three frontier ven-       to one-in-hundred-year flood risk and the burden
                                             dors and across capability tiers — the strongest         falling disproportionately on the poorest popula-
                                             models concentrate in the 0.65–0.75 band, and            tions (Rentschler et al., 2022; McDermott, 2022),
                                             no model reaches the human-expert reference              and accurate, timely streamflow forecasts are the
                                             except for Opus-4.7 at one testing gauge. We             difference between an evacuation that works and
                                             argue this gap is not a parameter-count prob-
                                                                                                      one that does not. The same models also price na-
                                             lem: it is a domain-grounding problem. We
                                             then propose H YDROAGENT, a recipe that fine-            tional flood insurance, set the design standards of
                                             tunes the open-weight Qwen3-4B model with                bridges, levees, and stormwater systems, and tell
                                             supervised fine-tuning on 2,576 expert cali-             municipalities how much water they can deliver
                                             bration trajectories and Group-Relative Pol-             through the dry months. As climate change accel-
                                             icy Optimization using NSE as a verifiable re-           erates the hydrologic cycle and pushes flash floods
                                             ward sourced from online CREST simulations—              and droughts into regions that have never experi-
                                             reinforcement learning with simulation feed-
                                                                                                      enced them at current intensities (Li et al., 2022),
                                             back (RLSF). Our central thesis is that, for
                                             Earth-system science, a small domain-tuned               demand for accurate, basin-specific simulations is
                                             policy with simulator-in-the-loop RL is a more           rising at exactly the moment when the supply of
                                             compute-efficient and physically faithful path           trained hydrologic modelers cannot keep pace. AI
                                             than scaling generic frontier models, and that           is the obvious candidate to absorb that workload;

                                                                                                  1
the question this paper asks is how.                         calibration grounding: the model has not learned
    Hydrologic model calibration is the act of               which parameter to move when the recession limb
choosing a small number of physical parameters—              is too steep. To test whether that gap can be nar-
soil-water capacity, infiltration shape, channel-            rowed without scaling, we propose H YDROAGENT,
routing coefficients—so that a numerical rainfall-           a domain-specific agent built on the open-weight
runoff model reproduces observed streamflow at               Qwen3-4B-Instruct model (Qwen Team, 2025). As
a stream gauge. It is the human-in-the-loop step             Figure 1, training proceeds in two phases: (i) su-
that makes every downstream use of the model                 pervised fine-tuning (SFT) on 2,576 calibration
trustworthy—reservoir operation, water-supply al-            trajectories distilled from a stronger teacher, and
location, drought outlook, hydropower scheduling,            (ii) reinforcement learning (RL) with simulation
infrastructure design, and flood warning alike—and           feedback (RLSF) using Group-Relative Policy Op-
it is the step that does not scale: each gauge in the        timization (GRPO) (Shao et al., 2024; DeepSeek-
conterminous United States requires hours to days            AI, 2025), where each rollout invokes an online
of an expert hydrologist’s attention, and what they          CREST simulation and the reward is a clipped NSE
learn about one basin transfers only loosely to the          plus shaped per-turn signals.
next. The mismatch between the climate-driven                   The argument we want to defend in this paper
rise in demand sketched above and the human sup-             has three pieces. First, frontier LLM agents are
ply of calibration expertise is the gap that motivates       within striking distance of human-expert perfor-
this paper.                                                  mance on hydrologic-model calibration but do not
    The recent surge in agentic large language               yet meet it; the gap is reproducible across model
models—models that interleave chain-of-thought               families. Second, that gap closes faster by post-
reasoning with tool use over many turns (Yao et al.,         training a small open model with simulator-in-the-
2023; Schick et al., 2023; Qin et al., 2024)—raises          loop RL than by waiting for the next frontier re-
an obvious question. These models have absorbed              lease; one does not need a 400-billion-parameter
graduate-level hydrology textbooks, can read CSV             generalist to operate a 13-parameter physics sim-
gauge files, can edit control files, and can shell out       ulator, and recent work on agentic AI for Earth
to a Linux binary. Can they simply do the cali-              observation has independently argued that generic
bration? If yes, the cost structure of operational           agent recipes leave structural problems—geospatial
hydrology shifts overnight. If no, the manner of             consistency, physical validity, error propagation
failure tells us where the gap actually lives.               across long tool chains—unaddressed in ways that
    This paper investigates that question along two          domain-tuned designs can fix (Munir et al., 2026).
complementary axes.                                          Third, Earth-system science is an unusually fertile
Axis 1: Where do frontier agents stand? We                   ground for this recipe because the data are rich and
give nine frontier LLM agents—Claude Opus 4.6,               multi-modal: rasterized remote-sensing imagery
Opus 4.7, Sonnet 4.6, GPT-5, GPT-5.4, GPT-5.4-               (spatial-2D + time), in-situ measurements (time se-
pro, Gemini 2.5-pro, Gemini 3.1-pro, and Gemini              ries), and expert narrative (e.g., National Weather
3-flash—the same task an entry-level hydrologist             Service warning messages and forecaster discus-
receives: a basin description, gauge time series,            sions) all carry information that a domain agent can
raster forcings (MRMS gauge-corrected precipita-             be trained to fuse with a physical solver to yield
tion, daily PET), the CREST control-file template,           steerable, physically consistent predictions.
and the goal of achieving high NSE values. Each              Contributions. (1) The first systematic benchmark
agent runs the calibration independently on each             of nine frontier LLM agents on the calibration of an
of four held-out gauges spanning 329–40,792 km2 ,            operational distributed hydrologic model, including
inside the same Linux sandbox under the terminal-            a public release of all 9 × 20 trajectories for repro-
2 agent harness in the harbor evaluation frame-              ducibility (Section 3). (2) A domain-specific recipe
work with a fixed compute budget (2-hour timeout);           (H YDROAGENT) that fine-tunes Qwen3-4B with
the same harness is also used to evaluate our fine-          SFT + GRPO using NSE as a verifiable simulator-
tuned model in Section 4, so frontier-model and              grounded reward, with full training configuration
H YDROAGENT numbers are directly comparable.                 sufficient to reproduce the run on 4×H100 (Sec-
Axis 2: Is a small, simulator-grounded model                 tion 2). (3) A position—defended quantitatively—
enough? Frontier-model evaluation suggests that              that for Earth-system tasks with cheap-to-evaluate
the challenge is not raw reasoning capacity but              physical simulators, a domain-tuned 4B-parameter

                                                         2
agent can substantially close the gap to frontier            gradient-based calibration and motivating an agent-
generalists (Section 4).                                     in-the-loop approach, and (ii) a single basin/event
                                                             simulation completes in seconds-to-minutes, which
2     Methods                                                makes simulator-feedback RL practical at the roll-
                                                             out scales we report.
This section describes (i) the CREST hydrologic
simulator that defines our task and reward, (ii) the         2.2   Calibration Environment and Task
calibration environment exposed to the agent, and
(iii) the SFT + RLSF training recipe used to pro-            We instantiate one calibration episode per
duce H YDROAGENT. The training infrastructure is             basin/event pair. Each episode exposes four tools
verl 0.5 (Sheng et al., 2024) with SGLang multi-             to agents:
turn rollouts on 4× NVIDIA H100 (80 GB) GPUs;                 • set_parameters: write the 13 scalar mul-
configurations sufficient to reproduce the run are              tipliers (wm, b, im, ke, fc, under, leaki,
given in Appendix A.                                            alpha, beta, alpha0, iwu, th, isu) into a
                                                                control-file copy. Each parameter has a doc-
2.1    The CREST/EF5 Hydrologic Simulator                       umented physically-motivated range (e.g., wm ∈
The Coupled Routing and Excess STorage                          [0.1, 10.0], im ∈ [0, 1]); the full list of bounds
(CREST) model (Wang et al., 2011; Li et al., 2023)              and physical interpretations is given in Ap-
is a distributed, grid-based, conceptual rainfall-              pendix B.
runoff model. At each grid cell and each hourly               • run_simulation: invoke the EF5 binary on
time step, CREST partitions incoming precipitation              the patched control file and parse the result-
into impervious runoff, infiltration, and evapotran-            ing time-series CSV, returning the full simu-
spiration as a function of a soil-water capacity grid           lated/observed discharge series at hourly res-
(wm), a variable infiltration-curve shape parameter             olution along with a summary of multiple
(b), an impervious-area fraction (im), an evapotran-            hydrologic-fit signatures: peak-flow magnitude
spiration scaling (ke), and a saturated hydraulic               error and timing offset, total-volume ratio (a
conductivity (fc); routes interflow with leakage                water-balance closure indicator), recession-limb
(leaki) and velocity (under); and routes channel                slope, time-to-peak, baseflow level, and event
and overland flow with kinematic-wave parameters                count. These criteria are exposed as text
α, β, and α0 . Initial soil moisture (iwu) and a small          the LLM interprets jointly—a peak under-
set of state parameters complete the parameter vec-             prediction with a balanced volume ratio implies
tor; spatial heterogeneity is encoded in raster grids,          a routing-velocity issue, while a balanced peak
and per-basin calibration is performed by tuning a              with a volume surplus implies an evapotranspi-
vector of scalar multipliers on those grids, which              ration or impervious-fraction issue.
preserves the spatial pattern while shifting magni-           • evaluate: aggregate the latest simulation
tudes.                                                          against the gauge time series. Returns the Nash–
   CREST is hosted by the Ensemble Framework                    Sutcliffe Efficiency  (Nash and Sutcliffe,
                                                                                                       P 1970),
                                                                NSE = 1 − t (Qt − Qt ) / t (Qobs
                                                                                     obs       sim 2
                                                                               P
For Flash Flood Forecasting (EF5) (Flamig et al.,                                                            t   −
2020), which is the operational hydrologic engine               Qobs )2 , alongside a panel of complementary
of the FLASH project (Gourley et al., 2017) at the              metrics—Kling–Gupta Efficiency components
NOAA National Severe Storms Laboratory and is                   (correlation, variability ratio, bias ratio), root-
used in real time by U.S. National Weather Service              mean-square error, percent bias, and high-/low-
forecasters to issue flash-flood watches and warn-              flow KGE—together with the running best-NSE
ings across the CONUS. CREST/EF5 has been de-                   and target-status. The agent therefore reasons
ployed globally, including in data-sparse satellite-            over a multi-criteria diagnostic rather than a sin-
forced settings (Xue et al., 2013), and projections             gle scalar; NSE is the headline reward signal
suggest that the demand for accurate calibration                but the auxiliary metrics are what disambiguate
of CREST-class models will grow: under SSP5–                    which physical process is the next thing to ad-
8.5, flash-flood frequency over the CONUS is pro-               just.
jected to increase (Li et al., 2022). Two facts about         • parse_failure: understands the difference be-
CREST shape our experimental design: (i) it is non-             tween model simulated and observed streamflow
differentiable in the parameter vector, ruling out              from its metrics: CC, KGE, NSE, peak_error,

                                                         3
Figure 1: Overview of the hydrologic calibration benchmark and evaluation pipeline: Dataset, Task, Agents,
Evaluations. Phase 1: supervised fine-tuning (SFT) on 2,576 expert calibration trajectories distills tool-call format
and basic hydrologic reasoning into Qwen3-4B. Phase 2: Group-Relative Policy Optimization (GRPO) draws K=8
rollouts per prompt; each rollout proposes a CREST parameter set, executes the EF5 hydrologic simulator, scores a
clipped Nash–Sutcliffe Efficiency, and updates the policy with group-normalized advantages. The simulator is the
verifier: there is no learned reward model.


   time_lag. Reasons the root cause and provides             get. We use 10 CONUS gauges spanning 539–
   possible reasons. An example of the reason-               2401 km2 (selected from the audit pool described
   ing output is “The model has stabilized with an           in Appendix A) for training, and four held-out
   NSE of 0.2248, CC of 0.591, and KGE of 0.5588,            gauges (ranging from 329 to 40,792 km2 ) for eval-
   indicating a well-calibrated simulation that ac-          uation, matching the protocol used in our frontier-
   curately captures the observed hydrograph in              model benchmark (Section 3). We adopt the widely
   terms of timing and volume. Although the peak             used hydrologic performance rubric of Moriasi
   discharge (374.93) is still below the observed            et al. (2015), which classifies streamflow simula-
   value (622.97), the timing error (lag = 32 hours)         tions as unsatisfactory (NSE ≤ 0.50), satisfactory
   is minimal, and the model’s performance across            (0.50 < NSE ≤ 0.70), good (0.70 < NSE ≤ 0.85),
   all metrics is consistent and physically realistic.       and very good (NSE > 0.85); the 0.8075 target
   Further improvements would require adjusting              therefore sits at the top of the good band and is the
   channel routing or impervious fraction.”                  threshold an experienced operational hydrologist
   The agent receives the basin descriptor, the              routinely meets on this gauge.
gauge directory, the precipitation/PET raster di-
                                                             2.3   Stage 1: Supervised Fine-Tuning
rectories, the control-file template, and the eval-
uation window, and must improve NSE over up                  The base model is Qwen3-4B-Instruct-2507
to 50 multi-turn iterations. Episodes terminate              (Qwen Team, 2025), chosen because it is the largest
on target attainment, on five rounds without im-             open-weight model that fits comfortably in BF16
provement, or on the per-episode wall-clock bud-             with full FSDP fine-tuning and K=8 multi-turn

                                                         4
rollouts on 4×H100 (80 GB), and because it ships                     wise), ∆NSEt is the change in best-NSE on turn
with native Hermes-style tool calling. We construct                  t, NSE⋆ is the episode-best NSE, τ is the gauge-
2,576 SFT trajectories by distilling a strong pro-                   specific target, neval counts valid evaluate calls,
prietary teacher (GPT-51 ) on 73 calibration runs                    nimprove counts evaluations that beat the running
across 29 U.S. gauges (excluding the 4 gauges                        best, and an episode is empty when the agent never
in the test set). The individual iterative episodes                  produces a parseable evaluation. The improvement
within each calibration run are reorganized into a                   bonus is the key inductive bias: it explicitly trains
single long-horizon trajectory — preserving the                      iterate-until-you-cannot-improve, which is what a
full hypothesise → simulate → diagnose → adjust                      hydrologist actually does.
sequence in its original tool-call order — so that the                  We use full BF16 fine-tuning under FSDP (no
model learns the chain-of-thought of iterative pa-                   LoRA), with actor learning rate 1×10−6 , KL an-
rameter refinement rather than only the converged                    chor coefficient 0.2 to the SFT initialization, en-
parameter set. Trajectories whose final NSE does                     tropy coefficient 0.01, sampling temperature 1.0
not exceed 0.6 are dropped, and the surviving se-                    with top-p 0.95, batch = 4 prompts ×K=8 roll-
quences are quality-weighted by their final-NSE                      outs per step, and 30 epochs over the 10-gauge
percentile. SFT teaches the model the tool-call                      training set. The strong KL anchor is necessary:
grammar, the parameter-bounds convention, and a                      lower values let the policy drift to token-level de-
basic hydrologic-reasoning style (“recession limb                    generate outputs by step ∼40. Rollouts are served
is too steep ⇒ increase wm or leaki”).                               by SGLang in synchronous mode with native multi-
                                                                     turn tool dispatch; EF5 invocations are gated by a
2.4   Stage 2: Reinforcement Learning with
                                                                     32-way semaphore to prevent CPU/IO contention.
      Simulation Feedback (RLSF)
                                                                     Training takes about 5 hours per checkpoint ca-
We refer to our RL stage as Reinforcement Learn-                     dence on 4×H100. Full Hydra configurations are
ing with Simulation Feedback (RLSF) to distin-                       in Appendix A.
guish it from human-feedback RL (Lee et al., 2024)
and from pure verifiable-text-reward RL (Lambert                     3     AI Agents for Hydrologic Modeling:
et al., 2024; DeepSeek-AI, 2025): the verifier here                        Where Do We Stand?
is a numerical Earth-system simulator producing
continuous physical-error metrics. The optimizer                     Hydrologic calibration is a stringent test of agen-
is GRPO (Shao et al., 2024), which is critic-free                    tic scientific reasoning: the task is long-horizon,
and uses group-relative advantage normalization—                     simulator-grounded, multi-objective, and physi-
a property that fits cheap-but-noisy simulator re-                   cally constrained. Effective calibration requires
wards well. For each prompt we draw K=8 roll-                        sustained iterative refinement over delayed feed-
outs; each rollout is a multi-turn calibration episode               back rather than one-shot reasoning. We therefore
invoking up to 50 tool calls. The reward decom-                      evaluate nine frontier LLM agents on a geograph-
poses into per-turn shaping and a terminal score:                    ically held-out EF5 calibration benchmark (§3.1)
                                                                    to measure both final performance (§3.2) and long-
               
               
               +0.02       valid set_parameters                     horizon engagement (§3.3).
               
               +0.05       valid run_simulation
      rtturn =                                                       3.1    Benchmark Setup
               
               ∆NSEt valid evaluate
                                                                     We evaluate nine frontier LLM agents on the cal-
               
               
               −0.5        parse_failure
                                                                     ibration of the four held-out gauges of Table 2
 rterminal = clip(NSE⋆ , −1, 1)                                      (drainage areas 329–40,792 km2 across distinct hy-
               + 0.5 · 1{NSE⋆ >τ } + 0.02 neval                      droclimatic regions of the CONUS). Each agent
               + 0.10 max(0, nimprove −1)                            runs each gauge (§3.2) independently inside the
                                                                     same Linux sandbox under the terminal-2 agent
               − 1.0 · 1{empty}
                                                                     harness in the harbor evaluation framework. The
where 1{·} is the indicator function (taking value                   harness exposes a single Bash terminal: the agent
1 when the bracketed condition holds and 0 other-                    reads the per-gauge task brief (basin descriptor, pa-
   1
                                                                     rameter table with bounds, EF5 invocation contract,
     Due to budget constraints, we use GPT-5 for initial agent
development and trajectory collection, while evaluating the          NSE target), inspects the data directory, edits the
four test gauges using nine latest frontier models.                  control file, runs ef5 /app/control.txt, parses

                                                                 5
the simulated-versus-observed CSV, and iterates.            the DREAM approximate-Bayesian-computation
Each round consists of up to 10 candidate param-            sampler (Vrugt and Sadegh, 2013) to calibrate the
eter sweeps; the budget is 20 rounds per gauge              same gauges, and is well within the achievable
(i.e., up to 200 EF5 simulations per gauge, 800             range for the basins in our panel. The same per-
across the panel) and we track the running-best             model comparison on the remaining three held-out
NSE per round per gauge. Figure 2a visualizes the           gauges (01403060, 06279500, 07144100) is also
per-model best-NSE bars on the canonical evalua-            provided in Figures 2b, 2c and 2d respectively; the
tion gauge 02338660. Hydrologic-model calibra-              qualitative ranking and the rounds-used/best-NSE
tion is a long-horizon task: in our pilot runs, 20          coupling described next persist across that panel,
rounds is the lower end of what suffices to reach           with absolute values shifting by basin difficulty.
the target on a typical gauge, and the multi-criteria          Best-NSE and rounds-used are tightly correlated:
diagnostic the agent must integrate (Section 2.2)           the three good-band models average 17.7 rounds on
only becomes informative after several rounds of            02338660, while the rest average 5.5 and the pro-
trial parameter moves. Whether each agent actu-             tier reasoning models from OpenAI and Google
ally uses that horizon is itself an outcome of the          terminate after one or two rounds with budget re-
experiment, reported alongside each best-NSE bar            maining. Calibration is a long-horizon task whose
in Figure 2.                                                reward sharpens only with iteration, and a class of
   The nine evaluated models are: Anthropic                 frontier models is policy-trained to stop early.
Claude Opus 4.6, Opus 4.7, and Sonnet 4.6; Ope-
nAI GPT-5, GPT-5.4, and GPT-5.4-pro; Google
Gemini 2.5-pro, Gemini 3.1-pro, and Gemini 3-               3.3   What Goes Wrong?
flash. The choice is intended to span the three fron-
tier families and to cover the speed/quality variants       Three failure modes recur across the trajectories.
currently in production (April 2026). All models            Premature termination: pro-tier reasoning models
are accessed through the harness’s default API in-          stop after a handful of rounds despite the 20-round
tegration with default sampling temperatures.               budget—Gemini 3.1-pro after 1 round, GPT-5.4-
                                                            pro after 2, and GPT-5.4 after 1—reaching an NSE
3.2   Results                                               they evidently consider “acceptable” and walk-
Figure 2 reports the best-NSE attained by each              ing away from a clearly improvable hydrograph.
model on the 4 gauges in the test set, alongside            Out-of-bounds proposals: weaker models repeat-
its typical rounds-used out of the 20-round budget.         edly propose parameter values outside documented
In Figure 2a, results are consistent across vendors.        physical ranges (e.g., negative im, wm>10), wast-
Mapped onto the Moriasi et al. (2015) performance           ing EF5 calls on rejections. Diagnosis-action mis-
rubric (visualized as bands in the figure), two mod-        match: models often correctly identify that a hydro-
els reach the good band (0.70 < NSE ≤ 0.85): Son-           graph has, for example, an over-pronounced reces-
net 4.6 (0.754, 20 rounds) and Opus 4.7 (0.749, 20          sion, but propose adjustments to channel-routing
rounds), with Gemini 3-flash (0.729, 13 rounds)             parameters rather than to the soil-moisture/leakage
at the same level; three more land in satisfac-             parameters that actually drive recession shape. We
tory (0.50 < NSE ≤ 0.70)—Opus 4.6 (0.667, 20                interpret these patterns as failures of calibration-
rounds), Gemini 3.1-pro (0.627, 1 round), and GPT-          relevant grounding and of long-horizon engage-
5.4-pro (0.613, 2 rounds); and the remainder are            ment, not of base reasoning capacity. The strongest
unsatisfactory (NSE ≤ 0.50), with Gemini 2.5-pro            models (Sonnet 4.6, Opus 4.7) use the full hori-
(0.250, 8 rounds) marginal and GPT-5 (−0.189, 3             zon and avoid the first two failure modes but still
rounds) and GPT-5.4 (−0.159, 1 round) failing to            exhibit the third, which is consistent with their bet-
produce a positive NSE within budget. On this               ter but still sub-target performance. The bottle-
gauge no model crosses the human-expert refer-              neck is therefore twofold: a model has to (a) be
ence at NSE=0.85; across the four-gauge panel,              willing to keep iterating across many rounds and
only Opus-4.7 reaches the reference, and only on            (b) know which parameter to move when. We ar-
one of the held-out gauges (see Figures 2b, 2c and          gue in the next section that exactly this gap is what
2d respectively). The reference itself is produced          an agent post-trained with simulator-in-the-loop
by an experienced hydrologist who pairs domain              RL—on long, multi-turn calibration episodes that
knowledge of CREST parameter sensitivities with             explicitly reward iteration—is designed to close.

                                                        6
                     (a) 02338660                                             (b) 01403060




                     (c) 06279500                                             (d) 07144100

Figure 2: Best-of-twenty-rounds Nash–Sutcliffe Efficiency (NSE) across four evaluation gauges, where GPT-5 and
GPT-5.4 failed to achieve positive NSE within budget and are omitted. Performance bands follow Moriasi et al.
(2015); the dashed line at NSE = 0.85 denotes the human-expert reference. Error bars are computed from four
runs per model. Almost all models underperform human expert except Opus-4.7 on gauge 06279500, which is the
largest basin and a documented difficult case (Appendix A).


4   How does HydroAgent Improve                           error improves on three of four basins (+1% to
    Streamflow Prediction?                                +87%, with a −163% degradation on 02338660).
                                                          Timing offset (|Lag|, where smaller is better) like-
We evaluate H YDROAGENT-4B—Qwen3-4B-                      wise contracts on all four basins, by +23% to
Instruct fine-tuned with SFT on 2,576 expert              over +200%. The pattern is consistent with
trajectories (Section 2.3) and then with GRPO             Section 2.4: the per-turn ∆NSE shaping and
under simulator-feedback rewards (Section 2.4)—           the volume/peak-weighted multi-criteria diagnostic
against its untuned base on the four held-out             surfaced by run_simulation (Section 2.2) jointly
gauges of Table 1. Both agents share the same             steer the policy to first stabilize magnitude metrics
terminal-2 harness in the harbor framework, the           and then align peak placement, so that absolute tim-
same 20-round budget, and the same task brief;            ing error shrinks together with NSE and correlation
only the policy weights differ. Figure 3 reports          rather than at their expense. The one residual cost
the relative change in four hydrologic-fit metrics        mode is peak-ratio error on 02338660 (−163%),
across this panel.                                        where compressing the late-recession volume bias
   The pattern is consistent: simulator-grounded          necessarily redistributes flow across event peaks;
post-training improves the metrics calibration is         we return to this trade-off in the limitations para-
judged by. Nash–Sutcliffe Efficiency improves             graph below.
on all four basins, from +5% on the canonical
test gauge 02338660 to over +200% on 01403060             5   Related Work
(where the baseline was deeply negative and is
now positive). Discharge correlation improves on          LLMs and foundation models for Earth sci-
all four basins, by 0 to +41%. Peak-flow ratio            ence. A first wave of work pre-trains domain-

                                                      7
Table 1: Per-gauge ablation of the SFT + RLSF training
stack on the four held-out gauges. Higher NSE is better.

     Gauge      Method       Best NSE   Sims   Turns   Parse fail
                Baseline        0.34     15      50            0
     07144100   SFT-only        0.07      1      15            4
                HydroAgent      0.65     13      50            0
                Baseline      −1.41      13      50            1
     06279500   SFT-only      −2.27       1      13            4
                HydroAgent    −0.84      17      50            0
                Baseline       0.65      13      50            0
     02338660   SFT-only     −17.53       1      11            4
                HydroAgent     0.68      12      50            0        Figure 3: Relative change in four hydrologic-fit metrics
                Baseline      −0.15      16      50            0        for H YDROAGENT-4B versus the Qwen3-4B-Instruct
     01403060   SFT-only       0.58       4      16            4        baseline on the four held-out gauges. Bubble color
                HydroAgent     0.40      14      50            0
                                                                        encodes direction and size encodes magnitude. For
                                                                        |Lag|, smaller is better.


specialized text or vision models for the Earth                         marks such as MLAgentBench (Huang et al., 2024)
sciences. K2 (Deng et al., 2024) and GeoGalac-                          and ScienceAgentBench (Chen et al., 2025) mea-
tica (Lin et al., 2024) continue-train LLMs on                          sure such agents on data-driven discovery tasks
geoscience corpora; ClimateBERT (Webersinke                             (best agents solve 32–42 %). AQUAH (Yan et al.,
et al., 2022), ClimateGPT (Thulke et al., 2024), and                    2025), the closest prior work, is a vision-enabled
ChatClimate (Vaghefi et al., 2023) target climate-                      LLM agent that takes a natural-language hydrology
domain text and retrieval; OceanGPT (Bi et al.,                         query, configures a model, runs the simulation, and
2024), EarthGPT (Zhang et al., 2024), and Remote-                       produces a PDF report—but it is prompt-only at the
CLIP (Liu et al., 2024) extend to ocean and remote-                     LLM core. We complement these by (i) measuring
sensing modalities. A second, much-discussed                            frontier agents on a closed-loop physical-simulator
wave builds neural surrogates of physical systems—                      task with quantitative streamflow rewards, and (ii)
Pangu-Weather (Bi et al., 2023), GraphCast (Lam                         showing that fine-tuning the LLM with simulator-
et al., 2023), FourCastNet (Pathak et al., 2022),                       grounded RL closes a substantial part of the gap.
GenCast (Price et al., 2024), ClimaX (Nguyen
et al., 2023), and Aurora (Bodnar et al., 2025)—                        RL fine-tuning with verifiable / environment
replacing numerical solvers in the medium-range                         feedback. A line of recent work shows that scal-
forecast pipeline. Nearing et al. (2024) pushes                         ing RL with rule-based or environment-based re-
a pure-LSTM rainfall-runoff regressor to global-                        wards can elicit strong reasoning behavior in open
scale ungauged-flood prediction. Our setting dif-                       LLMs. DeepSeek-R1 (DeepSeek-AI, 2025) and
fers in a basic respect from both waves: we do                          Kimi k1.5 (Kimi Team, 2025) train pure-RL rea-
not build a domain knowledge model, and we do                           soners with verifier rewards; Tülu 3 (Lambert et al.,
not replace the simulator with a learned surrogate.                     2024) formalizes Reinforcement Learning with Ver-
We keep the operational physics-based simulator                         ifiable Rewards (RLVR); RLEF (Gehring et al.,
(CREST), and we ask an LLM agent to operate it.                         2024) and SWE-RL (Wei et al., 2025) ground
                                                                        code-LLM RL in unit-test execution and software-
LLM agents for scientific simulation and discov-                        evolution histories. GRPO (Shao et al., 2024) pro-
ery. Coscientist (Boiko et al., 2023) and Chem-                         vides a critic-free policy-optimization objective us-
Crow (M. Bran et al., 2024) couple GPT-4 to tools                       ing group-normalized advantages, which we adopt.
and lab instruments for autonomous chemistry;                           RAGEN (Wang et al., 2025), ArCHer (Zhou et al.,
FunSearch (Romera-Paredes et al., 2024) pairs an                        2024), Reflexion (Shinn et al., 2023), ReAct (Yao
LLM with an evolutionary outer loop and a ver-                          et al., 2023), ToolLLM (Qin et al., 2024), ToRA
ifier for combinatorial discovery; The AI Scien-                        (Gou et al., 2024), Toolformer (Schick et al., 2023),
tist (Lu et al., 2024) and SciAgents (Ghafarollahi                      Voyager (Wang et al., 2024), and Eureka (Ma et al.,
and Buehler, 2025) extend this idea to open-ended                       2024) all explore variations of multi-turn agent
ML research and bioinspired-materials hypothe-                          training and tool use; RLAIF (Lee et al., 2024)
sis generation; AutoGen (Wu et al., 2023) pro-                          trades human labelers for an LLM judge. Ours
vides general multi-agent infrastructure. Bench-                        differs in the verifier: instead of a unit-test run-

                                                                    8
ner or LLM judge, our reward is a numerical hy-            SMA, VIC, mHM) and other small open backbones
drologic simulator producing continuous physical-          is an open question. Third, the strict pair-to-pair
error metrics (NSE), and the agent is rewarded for         scalar comparator (NSE and friends) can be re-
converging on a calibration trajectory with mono-          placed with a vision-language verifier that reads
tonically improving NSE. Our infrastructure builds         a rendered hydrograph plot—simulated, observed,
on verl/HybridFlow (Sheng et al., 2024) for multi-         and residual—directly: hydrologists do not, in prac-
turn GRPO with native tool dispatch.                       tice, reason in terms of a single NSE value. A
Hydrologic modeling and calibration. The dom-              vision-LLM critic in the loop would make the re-
inant deep-learning thread in hydrology trains             ward robust to the well-known pathologies of NSE
LSTMs on the CAMELS (Addor et al., 2017) or                (peak dominance, single-event sensitivity), enable
Caravan (Kratzert et al., 2023) datasets to regress        shape-aware credit assignment a scalar cannot pro-
streamflow directly (Kratzert et al., 2018, 2019,          vide, align learning with how domain experts actu-
2022). A complementary differentiable-physics              ally evaluate calibrations, and likely close the resid-
thread embeds neural networks inside process-              ual peak-ratio gap visible in Figure 3 on 02338660.
based models (Feng et al., 2022; Shen et al., 2023).       Over-reliance on an AI calibration agent risks prop-
Classical calibration of non-differentiable simula-        agating mis-specified parameter sets into opera-
tors relies on derivative-free global optimizers and       tional forecasts, where they could trigger false
Bayesian samplers: SCE-UA (Duan et al., 1992),             flash-flood warnings, suppress true ones, or misallo-
DDS (Tolson and Shoemaker, 2007), PEST (Do-                cate emergency-response resources—an argument
herty, 2015), and the DREAM family of Markov-              for keeping a human hydrologist in the loop and
chain Monte Carlo / approximate Bayesian compu-            treating the simulator-grounded reward as a verifier
tation samplers (Vrugt and Sadegh, 2013), which is         rather than a substitute for expert judgment.
the de facto reference for diagnostic Bayesian cali-       Conclusion. Frontier LLM agents fall system-
bration of conceptual rainfall-runoff models in the        atically short of human-expert performance on
hydrology literature. These optimizers do not lever-       hydrologic-model calibration, plateauing at a panel-
age cross-basin or domain-textual context; they            mean NSE of 0.65–0.75 across four held-out
treat each calibration as a black box. We provide          basins via failure modes that are not parameter-
an LLM-agent baseline along the same dimension             count problems but domain-grounding problems.
and argue that the agent’s pre-trained domain pri-         Post-training a 4B-parameter open base with SFT
ors make it a competitive complement, especially           and GRPO under a simulator-grounded reward—
when each simulator call is expensive.                     H YDROAGENT—narrows that gap on every held-
                                                           out basin in our panel (panel-mean NSE −0.14 →
6   Discussion and Conclusion                              +0.20). For Earth-system tasks with cheap-to-
                                                           evaluate physical simulators, a small domain-tuned
Limitations and future work. The headline result           policy with simulator-in-the-loop RL is a more
is established on a small CONUS-only panel—ten             compute-efficient and physically faithful path than
training basins (539–2,401 km2 ) and four held-out         scaling generic frontier models.
basins (329–40,792 km2 )—and a panel mean over
four gauges is too small a sample to defend a claim        Acknowledgments
of cross-regime generalization. Three directions
follow naturally. First, scaling the held-out eval-        We thank the operational hydrology community at
uation to a global hydrologic dataset—e.g., Car-           the NOAA National Severe Storms Laboratory and
avan (Kratzert et al., 2023), which standardizes           the U.S. National Weather Service for sustained
∼6,830 gauges with consistent forcings—would               discussions on CREST/EF5 and on the practical
test whether H YDROAGENT’s gains transfer to               realities of basin calibration. We are grateful to
hydroclimatic regimes (Mediterranean, monsoon,             Modal for providing the cloud computing infras-
alpine, polar) absent from our training panel; we          tructure that supported the GPU training runs and
view this global follow-up as the most important           large-scale agent rollouts underlying this research.
next experiment. Second, the recipe has been               We also thank the developers of the verl / Hybrid-
demonstrated only on CREST and a single small              Flow framework and the SGLang serving stack,
open base (Qwen3-4B); whether SFT+RLSF trans-              whose multi-turn tooling made this work tractable
fers to other distributed hydrologic models (SAC-          on a modest GPU budget.

                                                       9
References                                                     Zachary L Flamig, Humberto Vergara, and Jonathan J
                                                                 Gourley. 2020.     The ensemble framework for
Nans Addor, Andrew J Newman, Naoki Mizukami,                     flash flood forecasting (EF5) v1.2: description
  and Martyn P Clark. 2017. The CAMELS data                      and case study. Geoscientific Model Development,
  set: catchment attributes and meteorology for large-           13(10):4943–4958.
  sample studies. Hydrology and Earth System Sci-
  ences, 21(10):5293–5313.                                     Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard
                                                                 Mella, Quentin Carbonneaux, Taco Cohen, and
Kaifeng Bi, Lingxi Xie, Hengheng Zhang, Xin Chen,                Gabriel Synnaeve. 2024. RLEF: Grounding code
  Xiaotao Gu, and Qi Tian. 2023. Accurate medium-                LLMs in execution feedback with reinforcement
  range global weather forecasting with 3D neural net-           learning. arXiv preprint arXiv:2410.02089.
  works. Nature, 619(7970):533–538.
                                                               Alireza Ghafarollahi and Markus J Buehler. 2025. SciA-
Zhen Bi, Ningyu Zhang, Yida Xue, Yixin Ou, Dax-                  gents: Automating scientific discovery through bioin-
  iong Ji, Guozhou Zheng, and Huajun Chen. 2024.                 spired multi-agent intelligent graph reasoning. Ad-
  OceanGPT: A large language model for ocean sci-                vanced Materials, 37(9):2413523.
  ence tasks. In Proceedings of the 62nd Annual Meet-
  ing of the Association for Computational Linguistics         Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,
  (ACL).                                                         Yujiu Yang, Minlie Huang, Nan Duan, and Weizhu
                                                                 Chen. 2024. ToRA: A tool-integrated reasoning
Cristian Bodnar, Wessel P Bruinsma, Ana Lucic, Megan             agent for mathematical problem solving. In Inter-
  Stanley, Johannes Brandstetter, Patrick Garvan, Maik           national Conference on Learning Representations
  Riechert, Jonathan A Weyn, Haiyu Dong, Anna                    (ICLR).
  Vaughan, and 1 others. 2025. A foundation model
  for the Earth system. Nature, 641:1180–1187.                 Jonathan J Gourley, Zachary L Flamig, Humberto Ver-
                                                                 gara, Pierre-Emmanuel Kirstetter, Robert A Clark III,
Daniil A Boiko, Robert MacKnight, Ben Kline, and                 Elizabeth Argyle, Ami Arthur, Steven Martinaitis,
  Gabe Gomes. 2023. Autonomous chemical research                 Galateia Terti, Jessica M Erlingis, Yang Hong, and
  with large language models. Nature, 624(7992):570–             Kenneth W Howard. 2017. The FLASH project:
  578.                                                           Improving the tools for flash flood monitoring and
                                                                 prediction across the United States. Bulletin of the
Ziru Chen, Shijie Chen, Michael Ning, Qianheng Zhang,
                                                                 American Meteorological Society, 98(2):361–372.
   Boshi Wang, Botao Yu, Yifei Li, Zeyi Liao, Chen
   Wei, Zitong Lu, and 1 others. 2025. ScienceAgent-           Qian Huang, Jacky Vora, Percy Liang, and Jure
   Bench: Toward rigorous assessment of language                 Leskovec. 2024. MLAgentBench: Evaluating lan-
   agents for data-driven scientific discovery. In In-           guage agents on machine learning experimentation.
   ternational Conference on Learning Representations            In Proceedings of the 41st International Conference
  (ICLR).                                                        on Machine Learning (ICML).
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing rea-             Kimi Team. 2025.      Kimi k1.5: Scaling rein-
  soning capability in LLMs via reinforcement learning.          forcement learning with LLMs. arXiv preprint
  arXiv preprint arXiv:2501.12948.                               arXiv:2501.12599.
Cheng Deng, Tianhang Zhang, Zhongmou He, Qiyuan                Frederik Kratzert, Martin Gauch, Grey Nearing, and
  Chen, Yuanyuan Shi, Yi Xu, Luoyi Fu, Weinan                    Daniel Klotz. 2022. NeuralHydrology—a Python
  Zhang, Xinbing Wang, Chenghu Zhou, Zhouhan Lin,                library for deep learning research in hydrology. Jour-
  and Junxian He. 2024. K2: A foundation language                nal of Open Source Software, 7(71):4050.
  model for geoscience knowledge understanding and
  utilization. In Proceedings of the 17th ACM Interna-         Frederik Kratzert, Daniel Klotz, Claire Brenner, Karsten
  tional Conference on Web Search and Data Mining                 Schulz, and Mathew Herrnegger. 2018. Rainfall–
  (WSDM).                                                         runoff modelling using Long Short-Term Memory
                                                                 (LSTM) networks. Hydrology and Earth System Sci-
John Doherty. 2015. PEST: Model-independent param-                ences, 22(11):6005–6022.
  eter estimation, user manual (6th edition). Technical
  report, Watermark Numerical Computing.                       Frederik Kratzert, Daniel Klotz, Guy Shalev, Gün-
                                                                 ter Klambauer, Sepp Hochreiter, and Grey Nearing.
Qingyun Duan, Soroosh Sorooshian, and Vijai Gupta.               2019. Towards learning universal, regional, and local
  1992. Effective and efficient global optimization for          hydrological behaviors via machine learning applied
  conceptual rainfall-runoff models. Water Resources             to large-sample datasets. Hydrology and Earth Sys-
  Research, 28(4):1015–1031.                                     tem Sciences, 23(12):5089–5110.
Dapeng Feng, Jiangtao Liu, Kathryn Lawson, and                 Frederik Kratzert, Grey Nearing, Nans Addor, Tyler
  Chaopeng Shen. 2022. Differentiable, learnable, re-            Erickson, Martin Gauch, Oren Gilon, Lukas Gud-
  gionalized process-based models with multiphysi-               mundsson, Avinatan Hassidim, Daniel Klotz, Sella
  cal outputs can approach state-of-the-art hydrologic           Nevo, and 1 others. 2023. Caravan—a global com-
  prediction accuracy. Water Resources Research,                 munity dataset for large-sample hydrology. Scientific
  58(10):e2022WR032404.                                          Data, 10(1):61.


                                                          10
Remi Lam, Alvaro Sanchez-Gonzalez, Matthew Will-                Yecheng Jason Ma, William Liang, Guanzhi Wang, De-
  son, Peter Wirnsberger, Meire Fortunato, Ferran Alet,           An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke
  Suman Ravuri, Timo Ewalds, Zach Eaton-Rosen,                    Zhu, Linxi Fan, and Anima Anandkumar. 2024. Eu-
  Weihua Hu, and 1 others. 2023. Learning skillful                reka: Human-level reward design via coding large
  medium-range global weather forecasting. Science,               language models. In International Conference on
  382(6677):1416–1421.                                            Learning Representations (ICLR).
Nathan Lambert, Jacob Morrison, Valentina Pyatkin,              Thomas K J McDermott. 2022. Global exposure to
  Shengyi Huang, Hamish Ivison, Faeze Brahman,                    flood risk and poverty. Nature Communications,
  Lester James V Miranda, Alisa Liu, Nouha Dziri,                 13(1):3529.
  Shane Lyu, and 1 others. 2024. Tülu 3: Pushing fron-
  tiers in open language model post-training. arXiv             Daniel N Moriasi, Margaret W Gitau, Naresh Pai, and
  preprint arXiv:2411.15124.                                      Prasad Daggupati. 2015. Hydrologic and water qual-
                                                                  ity models: Performance measures and evaluation
Harrison Lee, Samrat Phatale, Hassan Mansoor, Thomas              criteria. Transactions of the ASABE, 58(6):1763–
  Mesnard, Johan Ferret, Kellie Ren Lu, Colton Bishop,            1785.
  Ethan Hall, Victor Carbune, Abhinav Rastogi, and
  Sushant Prakash. 2024. RLAIF vs. RLHF: Scaling                Muhammad Akhtar Munir, Muhammad Umer Sheikh,
  reinforcement learning from human feedback with                Akashah Shabbir, Muhammad Haris Khan, Fahad
  AI feedback. In Proceedings of the 41st International          Khan, Xiao Xiang Zhu, Begum Demir, and Salman
  Conference on Machine Learning (ICML).                         Khan. 2026. Agentic AI for remote sensing: Techni-
                                                                 cal challenges and research directions. arXiv preprint
Zhi Li, Mengye Chen, Shang Gao, Jonathan J Gour-                 arXiv:2604.24919.
  ley, Tiantian Yang, Xinyi Shen, Pierre Kirstetter, and
  Yang Hong. 2021. A multi-source 120-year US flood             J Eamonn Nash and J Vasilis Sutcliffe. 1970. River
  database with a unified common format and pub-                   flow forecasting through conceptual models part I—
  lic access. Earth System Science Data Discussions,               a discussion of principles. Journal of Hydrology,
  2021:1–25.                                                      10(3):282–290.

Zhi Li, Shang Gao, Mengye Chen, Jonathan J Gour-                Grey Nearing, Deborah Cohen, Vusumuzi Dube, Mar-
  ley, Changjie Liu, Andreas F Prein, and Yang Hong.              tin Gauch, Oren Gilon, Shaun Harrigan, Avinatan
  2022. The conterminous United States are projected              Hassidim, Daniel Klotz, Frederik Kratzert, Asher
  to become more prone to flash floods in a high-end              Metzger, and 1 others. 2024. Global prediction of
  emissions scenario. Communications Earth & Envi-                extreme floods in ungauged watersheds. Nature,
  ronment, 3(1):86.                                               627:559–563.

Zhi Li, Xianwu Xue, Robert Clark, Humberto Vergara,             Tung Nguyen, Johannes Brandstetter, Ashish Kapoor,
  Jonathan J Gourley, Guoqiang Tang, Xinyi Shen,                  Jayesh K Gupta, and Aditya Grover. 2023. ClimaX:
  Guangyuan Kan, Ke Zhang, Jiahu Wang, Mengye                     A foundation model for weather and climate. In
  Chen, Shang Gao, Jiaqi Zhang, Tiantian Yang, Yixin              Proceedings of the 40th International Conference on
  Wen, Pierre Kirstetter, and Tiantian Hong. 2023. A              Machine Learning (ICML).
  decadal review of the CREST model family: De-
  velopments, applications, and outlook. Journal of             Jaideep Pathak, Shashank Subramanian, Peter Harring-
  Hydrology X, 21:100159.                                          ton, Sanjeev Raja, Ashesh Chattopadhyay, Morteza
                                                                   Mardani, Thorsten Kurth, David Hall, Zongyi
Zhouhan Lin, Cheng Deng, Le Zhou, Tianhang Zhang,                  Li, Kamyar Azizzadenesheli, and 1 others. 2022.
  Yi Xu, Yutong Xu, Zhongmou He, Yuanyuan Shi,                     FourCastNet: A global data-driven high-resolution
  Beiya Dai, Yunchong Song, and 1 others. 2024. Ge-                weather model using adaptive Fourier neural opera-
  oGalactica: A scientific large language model in geo-            tors. arXiv preprint arXiv:2202.11214.
  science. arXiv preprint arXiv:2401.00434.
                                                                Ilan Price, Alvaro Sanchez-Gonzalez, Ferran Alet,
Fan Liu, Delong Chen, Zhangqingyun Guan, Xiaocong                  Tom R Andersson, Andrew El-Kadi, Dominic Mas-
  Zhou, Jiale Zhu, Qiaolin Ye, Liyong Fu, and Jun                  ters, Timo Ewalds, Jacklynn Stott, Shakir Mohamed,
  Zhou. 2024. RemoteCLIP: A vision language foun-                  Peter Battaglia, and 1 others. 2024. Probabilistic
  dation model for remote sensing. IEEE Transactions               weather forecasting with machine learning. Nature,
  on Geoscience and Remote Sensing.                                637:84–90.

Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foer-             Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan
  ster, Jeff Clune, and David Ha. 2024. The AI scien-             Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang,
  tist: Towards fully automated open-ended scientific             Bill Qian, and 1 others. 2024. ToolLLM: Facilitating
  discovery. arXiv preprint arXiv:2408.06292.                     large language models to master 16000+ real-world
                                                                  APIs. In International Conference on Learning Rep-
Andres M. Bran, Sam Cox, Oliver Schilter, Carlo Bal-              resentations (ICLR).
  dassari, Andrew D White, and Philippe Schwaller.
  2024. Augmenting large language models with chem-             Qwen Team. 2025. Qwen3 technical report. arXiv
  istry tools. Nature Machine Intelligence, 6:525–535.           preprint arXiv:2505.09388.


                                                           11
Jun Rentschler, Melda Salhab, and Bramka Arga Jafino.          Jasper A Vrugt and Mojtaba Sadegh. 2013. Toward
  2022. Flood exposure and poverty in 188 countries.              diagnostic model calibration and evaluation: Approx-
  Nature Communications, 13(1):3527.                              imate Bayesian computation. Water Resources Re-
                                                                  search, 49(7):4335–4345.
Bernardino    Romera-Paredes,      Mohammadamin
  Barekatain, Alexander Novikov, Matej Balog,                  Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Man-
  M Pawan Kumar, Emilien Dupont, Francisco JR                    dlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
  Ruiz, Jordan S Ellenberg, Pengming Wang, Omar                  Anima Anandkumar. 2024. Voyager: An open-ended
  Fawzi, Pushmeet Kohli, and Alhussein Fawzi. 2024.              embodied agent with large language models. Trans-
  Mathematical discoveries from program search with              actions on Machine Learning Research (TMLR).
  large language models. Nature, 625:468–475.
                                                               Jiahu Wang, Yang Hong, Li Li, Jonathan J Gourley,
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta              Sadiq I Khan, Koray K Yilmaz, Robert F Adler, Fred-
  Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola                erick S Policelli, Shahid Habib, Daniel Irwn, and 1
  Cancedda, and Thomas Scialom. 2023. Toolformer:                 others. 2011. The coupled routing and excess storage
  Language models can teach themselves to use tools.              (CREST) distributed hydrological model. Hydrologi-
  In Advances in Neural Information Processing Sys-               cal Sciences Journal, 56(1):84–98.
  tems 36 (NeurIPS).
                                                               Zihan Wang, Kangrui Wang, Qineng Wang, Pingyue
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,                  Zhang, Linjie Li, Zhengyuan Yang, Heng Chen, and 1
  Junxiao Song, Mingchuan Zhang, Y K Li, Y Wu, and               others. 2025. RAGEN: Understanding self-evolution
  Daya Guo. 2024. DeepSeekMath: Pushing the limits               in LLM agents via multi-turn reinforcement learning.
  of mathematical reasoning in open language models.             arXiv preprint arXiv:2504.20073.
  arXiv preprint arXiv:2402.03300.
                                                               Nicolas Webersinke, Mathias Kraus, Julia Anna Bin-
Chaopeng Shen, Alison P Appling, Pierre Gentine,                 gler, and Markus Leippold. 2022. ClimateBert: A
  Toshiyuki Bandai, Hoshin Gupta, Alexandre Tar-                 pretrained language model for climate-related text.
  takovsky, Marco Baity-Jesi, Fabrizio Fenicia, Daniel           arXiv preprint arXiv:2110.12010.
  Kifer, Li Li, and 1 others. 2023. Differentiable mod-
  elling to unify machine learning and physical models
  for geosciences. Nature Reviews Earth & Environ-             Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin
  ment, 4:552–567.                                               Carbonneaux, Lingming Zhang, Daniel Fried,
                                                                 Gabriel Synnaeve, Rishabh Singh, and Sida I Wang.
Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin                 2025. SWE-RL: Advancing LLM reasoning via
  Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin                 reinforcement learning on open software evolution.
  Lin, and Chuan Wu. 2024. HybridFlow: A flexi-                  arXiv preprint arXiv:2502.18449.
  ble and efficient RLHF framework. arXiv preprint
  arXiv:2409.19256.                                            Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran
                                                                 Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun
Noah Shinn, Federico Cassano, Edward Berman, Ash-                Zhang, Shaokun Zhang, Jiale Liu, and 1 others.
  win Gopinath, Karthik Narasimhan, and Shunyu Yao.              2023. AutoGen: Enabling next-gen LLM applica-
  2023. Reflexion: Language agents with verbal rein-             tions via multi-agent conversation. arXiv preprint
  forcement learning. In Advances in Neural Informa-             arXiv:2308.08155.
  tion Processing Systems 36 (NeurIPS).
                                                               Xianwu Xue, Yang Hong, Ashutosh S Li-
David Thulke, Yingbo Gao, Petrus Pelser, Rein Brune,             maye, Jonathan J Gourley, George J Huffman,
  Rricha Jalota, Floris Fok, Michael Ramos, Ian van              Sadiq Ibrahim Khan, Chhimi Dorji, and Sheng Chen.
  Wyk, Abdallah Nasir, Hayden Goldhahn, and 1 oth-               2013. Statistical and hydrological evaluation of
  ers. 2024. ClimateGPT: Towards AI synthesizing                 TRMM-based multi-satellite precipitation analysis
  interdisciplinary research on climate change. arXiv            over the Wangchu basin of Bhutan: Are the latest
  preprint arXiv:2401.09646.                                     satellite precipitation products 3B42V7 ready for
                                                                 use in ungauged basins? Journal of Hydrology,
Bryan A Tolson and Christine A Shoemaker. 2007. Dy-              499:91–99.
  namically dimensioned search algorithm for com-
  putationally efficient watershed model calibration.          Songkun Yan, Zhi Li, Siyu Zhu, Yixin Wen, Mofan
  Water Resources Research, 43(1):W01413.                        Zhang, Mengye Chen, Jie Cao, and Yang Hong. 2025.
                                                                 AQUAH: Automatic quantification and unified agent
Saeid Ashraf Vaghefi, Dominik Stammbach, Veruska                 in hydrology. arXiv preprint arXiv:2508.02936.
  Muccione, Julia Bingler, Jingwei Ni, Mathias
  Kraus, Simon Allen, Chiara Colesanti-Senni, To-              Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
  bias Wekhof, Tobias Schimanski, and 1 others. 2023.            Shafran, Karthik Narasimhan, and Yuan Cao. 2023.
  ChatClimate: Grounding conversational AI in cli-               ReAct: Synergizing reasoning and acting in language
  mate science. Communications Earth & Environ-                  models. In International Conference on Learning
  ment, 4(1):480.                                                Representations (ICLR).


                                                          12
Wei Zhang, Miaoxin Cai, Tong Zhang, Yin Zhuang, and          Table 2: Gauge configurations used in this study. The
 Xuerui Mao. 2024. EarthGPT: A universal multi-              10 training gauges span 539–2,401 km2 across diverse
  modal large language model for multi-sensor image          hydroclimatic regions of the CONUS; four held-out
  comprehension in remote sensing domain. IEEE               gauges, ranging from 329 to 40,792 km2 , form the test-
 Transactions on Geoscience and Remote Sensing,              ing set used only for evaluation in Sections 3 and 4.
  62:1–20.
                                                              Split   Gauge ID    Basin (km2 )   Window (UTC)
Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine,
  and Aviral Kumar. 2024. ArCHer: Training lan-                       11383500            539    2018-05-19 → 2018-07-17
  guage model agents via hierarchical multi-turn RL.                  11043000            575    2019-03-15 → 2019-05-13
                                                                      11152000            632    2018-05-29 → 2018-07-27
  In Proceedings of the 41st International Conference                 02294781          1,064    2018-04-29 → 2018-06-27
  on Machine Learning (ICML).                                         02312000          1,476    2018-11-15 → 2019-01-13
                                                              Train
                                                                      07195430          1,489    2018-01-04 → 2018-03-04
A   Reproducibility details                                           11179000          1,639    2018-06-03 → 2018-08-01
                                                                      14301000          1,727    2018-09-11 → 2018-11-09
                                                                      14207500          1,828    2018-04-09 → 2018-06-07
Gauge configurations. The 10 training gauges                          11376000          2,401    2018-09-21 → 2018-11-19
and the four held-out test gauges, with their basin                   02338660            329    2018-07-01 → 2018-08-31
areas, evaluation windows, and provenance notes,                      01403060          2,033    2018-11-11 → 2019-01-09
                                                              Test
are listed in Table 2; their geographic distribution                  06279500         40,792    2018-06-13 → 2018-08-11
                                                                      07144100          3,209    2019-03-30 → 2019-05-28
is shown in Figure 4. The split between train-
ing and testing gauges is a random partition of
the audit pool, not stratified by basin size or re-          calibration runs across 29 U.S. gauges. Each cali-
gion, so that any cross-basin generalization ob-             bration run yields, on average, ∼35 such fragments
served in Sections 3 and 4 reflects the agent rather         after slicing on tool-call boundaries. Fragments are
than a hand-curated train/test alignment. Training           quality-weighted by their parent run’s final-NSE
gauges were selected by sliding a 60-day window              percentile; runs whose final NSE falls below the
over each gauge’s hourly observation series and
                                      √                      per-gauge floor are dropped.
scoring by log10 (Qpeak /Q + 1) × trise trecess to
                                                             Evaluation harness (frontier and H YDROA-
favour clean flood events. The held-out test set is
                                                             GENT ). All evaluations reported in this paper—
intentionally diverse in scale—spanning 329 km2
                                                             both the nine frontier agents in Section 3 and the
to 40,792 km2 —to stress-test cross-basin gener-
                                                             H YDROAGENT-4B checkpoint in Section 4—are
alization; 02338660 is the canonical evaluation
                                                             conducted under the same terminal-2 agent har-
gauge used in Sections 3 and 4, while 01403060,
                                                             ness in the harbor evaluation framework. Each
06279500, and 07144100 are reserved for the held-
                                                             agent receives the same system prompt, the same
out panel referenced in Section 4 and will be eval-
                                                             data layout (/app/data/), the same EF5 binary
uated once the corresponding MRMS/PET clip is
                                                             path (/EF5/bin/ef5), the same parameter table
built.
                                                             with bounds, the same 20-round / 10-sweep budget,
Forcings and static grids. CREST/EF5 inputs
                                                             and the same NSE target (0.8075 on the held-out
include hourly MRMS gauge-corrected precipita-               gauge). Frontier agents are accessed through the
tion GeoTIFFs, daily PET GeoTIFFs, a CONUS-
                                                             harness’s default API integration with default sam-
wide DEM, flow-direction and flow-accumulation
                                                             pling temperature; H YDROAGENT-4B is served by
rasters, and CREST/KW default parameter rasters
                                                             SGLang behind the harness’s local-model adapter,
(wm, b, im, ksat, α, β, leaki, α0 ). All scalar mul-
                                                             with greedy decoding for reproducibility. The
tipliers documented in Section 2.2 apply to these            training-time rollout stack (verl + SGLang multi-
grids.
                                                             turn) is decoupled from the evaluation harness so
GRPO hyperparameters. The Hydra-style config-                that no information leaks across the two; check-
uration that overlays verl’s ppo_trainer defaults            points are scored only through the harbor harness.
to produce our GRPO recipe is summarized in Ta-
ble 3; one training step takes approximately 30 min          B    CREST parameter reference
of wall time on 4×H100 80 GB and the run check-
points every ∼5 h.                                           Table 4 gives the physical interpretation of every
SFT data. 2,576 turn-level trajectory fragments—             tunable CREST parameter that the agent sets via
i.e., ⟨prompt, tool-call, tool-result⟩ slices rather         set_parameters (see Section 2.2). Parameters
than complete episodes—distilled from 73 GPT-5               are scalar multipliers applied to the spatially dis-

                                                        13
Table 3: GRPO training configuration for H YDROAGENT-4B. All keys are Hydra paths layered on top of verl’s
ppo_trainer defaults; rollouts are served by SGLang in synchronous mode with native multi-turn tool dispatch
(Hermes format).

 Group        Key / setting                         Value / note
              algorithm.adv_estimator               grpo
 Algorithm    kl_loss_coef                          0.2 (low_var_kl) anchor to SFT init
              entropy_coeff                         0.01
              actor.optim.lr                        1×10−6
              lr_warmup_steps_ratio                 0.05
 Optimizer
              Precision                             BF16
              Sharding                              FSDP, no LoRA
              data.train_batch_size                 4 prompts
 Batching     ppo_mini_batch_size                   4
              data.max_response_length              4096 tokens
              rollout.n                             K = 8 rollouts per prompt
              rollout.temperature                   1.0
 Rollout
              rollout.top_p                         0.95
              multi_turn.max_assistant_turns        50
              trainer.total_epochs                  30
 Trainer      trainer.save_freq                     10 steps
              trainer.test_freq                     25 steps
              GPUs                                  4×H100, 80 GB
 Hardware
              EF5 concurrency                       32 (per-worker semaphore × 4 workers)



                                                                 under, leaki jointly shape the recession limb and
                                                                 the long tail; alpha, beta, alpha0 control routing
                                                                 and therefore time-to-peak and peak attenuation;
                                                                 ke and iwu primarily shift the long-term water bal-
                                                                 ance and antecedent state. A competent calibration
                                                                 agent must learn both the marginal and the inter-
                                                                 action effects, which is the main reason the multi-
                                                                 criteria diagnostic exposed in Section 2.2 (volume
                                                                 ratio, peak error, time-to-peak, recession slope) is
Figure 4: Geographic distribution of the gauges used in          necessary: a single NSE value compresses these
this study across the conterminous United States. Train-         distinct physical signals into one number and gives
ing gauges (10) span basins from the Pacific Northwest,
                                                                 the agent no leverage to disambiguate which group
California, the Southwest, the Midwest, the Southeast,
and the Atlantic seaboard, covering a wide range of              of parameters to move next.
climatic regimes (Mediterranean, semi-arid, humid sub-
tropical, humid continental); the held-out test gauge            C    Ablation: contribution of SFT and
02338660 sits in the humid-subtropical Southeast. The                 RLSF
geographic spread is intentional: it stresses the agent’s
ability to generalize across distinct hydroclimatic re-
                                                                 To isolate what each post-training stage contributes
gions rather than within a single region’s flow regime.          to the headline result of Section 4, we evaluate three
                                                                 policies under the identical terminal-2/harbor har-
                                                                 ness (Appendix A) used elsewhere in the paper:
tributed parameter rasters; the bounds are the physi-            (i) the untuned base Qwen3-4B-Instruct-2507;
cally reasonable ranges enforced by the calibration              (ii) Qwen3-4B-hydro-sft, the same base after
environment. Process roles follow Li et al. (2023);              only Stage 1 (supervised fine-tuning on 2,576 ex-
Wang et al. (2011) and the AQUAH parameter de-                   pert calibration trajectories, Section 2.3); and (iii)
scription in Yan et al. (2025).                                  H YDROAGENT, the SFT-initialized policy after
   The eleven calibrated parameters are not inde-                Stage 2 (GRPO under simulator-grounded NSE re-
pendent in their effect on the simulated hydrograph:             wards, Section 2.4; checkpoint global_step_90).
wm, b, im jointly determine the rainfall-to-runoff               All three policies share identical decoding settings
partition and dominate event-peak magnitude; fc,                 (greedy), the same 50-turn / 20-round budget, the

                                                            14
Table 4: CREST scalar-multiplier parameters exposed to the agent, their valid ranges, and their physical roles.
Process attribution follows Li et al. (2023); Wang et al. (2011); Yan et al. (2025). The first eleven parameters are
calibrated; the last two (th, isu) are state parameters held at fixed values during our experiments but exposed
through the same interface for completeness.

     Parameter   Range          Process                Physical role
     wm          [0.1, 10.0]    Soil moisture          Mean soil-water storage capacity (mm). Controls how much
                                                       rainfall a soil column can absorb before saturation; larger wm
                                                       delays runoff onset and sustains baseflow.
     b           [10−6 , 3.0]   Infiltration           Shape exponent of the variable infiltration curve. Larger b con-
                                                       centrates saturation in a smaller fraction of the basin, producing
                                                       flashier runoff response.
     im          [0.0, 1.0]     Surface partitioning   Impervious-area fraction. Sets the share of rainfall that bypasses
                                                       infiltration entirely and routes directly as overland flow.
     ke          [0.8, 1.2]     Evapotranspiration     Multiplier on the PET forcing. Tunes the bias of the input PET
                                                       grid against basin water balance; affects long-term volume but
                                                       not event peaks.
     fc          [0.1, 2.0]     Subsurface             Saturated hydraulic conductivity multiplier. Governs the rate of
                                                       vertical drainage from the soil store to the interflow store.
     under       [0.1, 10.0]    Interflow              Interflow (subsurface) velocity. Faster under sharpens the reces-
                                                       sion; slower under extends the tail of the hydrograph.
     leaki       [0.1, 10.0]    Interflow              Leakage rate from the interflow store to deeper groundwater.
                                                       Higher leaki steepens recession and reduces total simulated
                                                       volume.
     alpha       [0.1, 3.0]     Channel routing        Coefficient in the kinematic-wave channel relation Q = α Aβ .
                                                       Increases peak conveyance for a given cross-sectional flow area.
     beta        [0.1, 3.0]     Channel routing        Exponent in the kinematic-wave channel relation Q = α Aβ .
                                                       Controls non-linearity of channel response with flow magnitude.
     alpha0      [0.0, 3.0]     Overland routing       Overland (non-channel) routing coefficient. Governs hillslope-
                                                       flow celerity before water enters the channel network; affects
                                                       time-to-peak.
     iwu         [0.1, 100.0]   Initial state          Initial soil-water content as percentage of wm. Sets antecedent
                                                       moisture and therefore the basin’s runoff-coefficient memory at
                                                       simulation start.
     th          fixed at 10    Network                Channel-initiation threshold (cells of accumulated drainage area
                                                       required to declare a channel). Defines the channel network
                                                       rather than its dynamics.
     isu         fixed at 0     Initial state          Initial interflow-storage content. Held at zero in our experiments.



same parameter table with bounds, and the same                  11–16 turns of the 50-turn budget, and produces 4
NSE target (0.8075); only the weights differ. The               malformed tool-call attempts in every episode. Dis-
four held-out gauges are those of Table 2.                      tillation has reproduced the surface of the teacher
                                                                trajectories—tool-call grammar, parameter nam-
   Table 1 reports per-gauge best NSE alongside
                                                                ing, and a hydrologic-reasoning style—but has
three diagnostic signals that turn out to be central to
                                                                collapsed the iterative behavior that produced the
the interpretation: the number of distinct EF5 sim-
                                                                teacher’s good final NSE. The policy commits a sin-
ulator invocations the agent successfully launches
                                                                gle parameter guess and stops; whether that guess
per episode (sims), the number of dialog turns ac-
                                                                turns out to be reasonable (01403060: 0.58, the
tually consumed out of the 50-turn cap (turns), and
                                                                only gauge where SFT-only beats both other vari-
the count of malformed tool-call attempts the har-
                                                                ants) or grossly miscalibrated (02338660: −17.53)
ness had to reject (parse fail).
                                                                is essentially luck-of-the-draw, because the SFT-
Stage 1 (SFT) alone is not sufficient—and is                    only policy is no longer willing to refine in re-
sometimes harmful. Compared to the untuned                      sponse to feedback. This is the same premature-
base, SFT-only regresses on three of the four held-             termination pathology Section 3 identifies in pro-
out gauges, including a catastrophic collapse on the            tier frontier reasoning models, induced here by the
canonical evaluation gauge 02338660 (+0.65 →                    maximum-likelihood objective itself: when teacher
−17.53, an ≈ 18-point NSE drop). The diagnos-                   trajectories converge in 4–5 tool calls, the SFT-only
tic columns of Table 1 explain why. SFT-only                    policy learns to emit the converged distribution di-
launches only 1–4 EF5 simulations per episode                   rectly instead of the deliberation that produced it.
(vs. 13–16 for the baseline), exits the harness after

                                                           15
As an isolated post-training stage, SFT distills for-        D    Per-gauge frontier-model results on the
mat and style at the cost of long-horizon engage-                 held-out test panel
ment, and on a panel-mean basis is worse than the
untuned base (−4.79 vs. −0.14).                              Cross-gauge observations. Three patterns repro-
Stage 2 (RLSF) restores iteration and grounds                duce across the four-gauge panel. First, the qualita-
it in simulator feedback. Adding GRPO with the               tive ranking is preserved: Sonnet 4.6 and Opus 4.7
simulator-grounded NSE reward recovers iterative             retain the top two slots on every gauge that admits
behavior and improves best NSE on three of four              a positive NSE, while GPT-5 and GPT-5.4 fail to
held-out gauges relative to the SFT-only initializa-         reach a positive NSE on any gauge—the right-tail
tion: 02338660 from −17.53 to +0.61 (∆NSE =                  unsatisfactory cluster is a property of the model,
+18.14), 06279500 from −2.27 to −0.84 (+1.43),               not of a particular basin. Second, the rounds-used /
and 07144100 from +0.07 to +0.65 (+0.58). The                best-NSE coupling described in Section 3.2 is ro-
diagnostic columns confirm that the gains travel             bust to the change of basin: on every gauge, the
with restored interaction: simulation counts return          models that reach the good band consume close
to 12–17 per episode, the full 50-turn budget is             to the full 20-round budget, and the pro-tier rea-
consumed on every gauge, and parse failures fall             soning models (Gemini 3.1-pro, GPT-5.4-pro) con-
to zero across the panel. The lone regression—               tinue to self-terminate within 1–2 rounds. Third,
01403060, +0.58 → +0.40—is the gauge where                   basin difficulty re-scales but does not invert the
SFT-only’s single-shot guess happened to land in a           band assignments: on 06279500—the 40,792 km2
high-NSE region; RLSF’s greedy decoding settles              basin whose scale is documented in Appendix A as
on a different local optimum but does not collapse.          exceeding our training pool—no frontier model
Relative to the untuned base, the full SFT + RLSF            exceeds the satisfactory threshold, and several
stack lifts panel-mean NSE from −0.14 to +0.20               drop a band relative to 02338660; conversely, on
and panel-median NSE from +0.09 to +0.50, and                01403060 and 07144100 the absolute best-NSE
converts a third basin from negative to positive             values shift but the same set of models occupies the
NSE.                                                         good/satisfactory/unsatisfactory partition. Taken
The two stages are complementary, not sub-                   together, the per-gauge panel reinforces the main-
stitutable. The marginal contribution of adding              text reading that the frontier ceiling at NSE ≈ 0.75
RLSF on top of SFT is ∆NSE = +4.99 in panel                  is a domain-grounding ceiling rather than a basin-
mean (−4.79 → +0.20); the marginal contribu-                 specific artifact.
tion of using SFT alone over the untuned base is             E   Hydrograph comparison on the
∆NSE = −4.65 in panel mean (−0.14 → −4.79).
                                                                 held-out test panel
The asymmetry is the central finding of the ablation:
SFT distills the tool-call vocabulary that prevents a        Figures 5–8 show, for each of the four held-
4-per-episode parse-failure tax once RLSF is lay-            out test gauges, the gauge observation alongside
ered on top, but in isolation it strips the model            the simulated discharge produced by the base
of the iterative engagement that the calibration             Qwen3-4B-Instruct-2507 agent (slate gray) and
task demands; only when paired with simulator-in-            by H YDROAGENT after SFT + RLSF post-training
the-loop RL does SFT’s grammar transfer pay off.             (amber). Each panel reports the EF5/CREST per-
Equivalently, RLSF is what supplies long-horizon             run statistics in the corresponding line color: NSE,
credit assignment grounded in physical-error feed-           percent bias, Pearson correlation, modified corre-
back, but starting GRPO from the untuned base                lation (modCC), MAE, RMSE, peak-magnitude
instead of the SFT initialization is precluded by the        error (cms), and peak-timing error (hours). The
high parse-failure rate of the untuned base on the           basin-average rainfall is rendered on an inverted
tool-call schema—empirically observed in early pi-           secondary axis (green). The headline NSE com-
lots, and the reason our pipeline anchors GRPO to            parison rebuilds, gauge by gauge, the panel-mean
the SFT initialization with KL coefficient 0.2 (Sec-         improvement summarized in Figure 3: HydroA-
tion 2.4, Table 3). The headline result of Section 4         gent matches or exceeds the base model on NSE
is therefore not attributable to either stage alone:         for every gauge, with the largest gains on 01403060
it is the product of the SFT → RLSF sequence, in             (negative → positive) and 07144100 (low- to high-
which SFT provides the format and RLSF supplies              band positive). Visually, HydroAgent’s recession
the iteration.                                               limbs are noticeably better-aligned with the ob-

                                                        16
served hydrograph than the base model’s, while
the timing of simulated peaks remains the weakest
residual error—consistent with the volume-/peak-
weighted shaping of the RLSF reward (Section 2.4)
and the observation discussed in Section 4.




                                                              Figure 7: Gauge 06279500 (basin area 40,792 km2 ;
                                                              June–August 2018). The largest basin in the test panel
                                                              and a documented difficult case (Appendix A). HydroA-
                                                              gent reduces the magnitude of the negative NSE substan-
                                                              tially (−1.41 → −0.84) but does not reach a positive
                                                              value within budget—an artifact of the basin’s scale
                                                              relative to our training pool (≤2,401 km2 ). This likely
                                                              reflects a limitation of the underlying physical model in
                                                              heavily human-managed basins.




Figure 5: Gauge 02338660 (basin area 329 km2 ; July–
August 2018). HydroAgent improves NSE from 0.65
to 0.68 and reduces RMSE; both runs share a similar
peak-timing offset.




                                                              Figure 8: Gauge 07144100 (basin area 3,209 km2 ;
                                                              March–May 2019). HydroAgent more than doubles
                                                              NSE from 0.33 to 0.68, with a visibly tighter recession
                                                              limb and a peak-magnitude reduction matching the ob-
                                                              served series.




Figure 6: Gauge 01403060 (basin area 2,033 km2 ;
November 2018–January 2019). The base model pro-
duces a runaway over-prediction on the late-November
event (>1,000 m3 s−1 against an observed peak near
600 m3 s−1 ); HydroAgent collapses that bias and lifts
NSE from −0.15 to +0.42.


                                                         17
