  When Do Agent Loops Mistake Stagnation for Progress?
 Self-Evaluation Bias and Externally Grounded Verification in Long-Running Autonomous LLM
                                         Agent Loops

                                                     Hyundoo Park · Byungho Choi
                                                Independent Researchers, Republic of Korea


         Abstract. Long-running autonomous agents increasingly plan, act, and judge their own completion without
         continuous human intervention. When an agent grades its own work, however, self-evaluation bias takes hold:
         plausible changes are accepted as progress, and the loop reports advancement while real-world outcomes
         stagnate or regress. We name this failure mode the progress mirage and show, with controlled measurement, that
         it is a question of what the evaluator is grounded in. We built a testbed that holds the agent and its tool surface
         fixed across all conditions and manipulates only the information-channel type of the evaluator that gates the
         loop. A world-state oracle (a synthetic user simulator) that is unfakeable in principle is enforced by container
         and network isolation, and the agent’s inability to reach that oracle is empirically verified by a boundary proof
         at every run and a canary scan at every cycle. Running a real frontier agent repeatedly under three evaluator
         arrangements yields the following results. The agent claimed its change was an improvement in all 54 cycles, yet
         56 percent of those cycles had a measured delta of zero or below. Self-report was thus an uninformative signal,
         and the self-verdict gate that trusts it degenerated into accept-all, eroding the best deployed state it had reached
         by 19 percent through subsequent acceptance of regressions. Even the strongest in-band judge — one that reads
         the full artifact text, the change diff, and its own verdict history — accepted cycles of which 44 percent were
         real-world regressions and rejected 38 percent of real improvements, so the preregistered adversarial hypothesis
         that a strong judge closes the gap was rejected. In contrast, on a boundary task whose success specification is
         verifiable from the artifact itself, the same judge’s mirage vanished to 0 and the gap to out-of-band collapsed
         within the registered threshold (H2 accepted), showing that the gap is not an artifact of the apparatus but depends
         on where the success signal resides. Further, in a sign-only variant that removes the oracle numbers from the
         feedback and returns only the acceptance verdict, real-world output remained similar to full feedback (mean
         110.0 versus 113.0), decomposing at pilot scale the benefit of out-of-band evaluation as coming from the gate’s
         grounding rather than from the information content of the feedback. The cause of the gap is not the evaluator’s
         quality but what the evaluator is grounded in. We generalize these results into an architecture centered on an
         out-of-band evaluator, report the anonymized six-week, 61-cycle field observation of a single deployment that
         motivated it, and situate the architecture relative to platform built-in loop/goal primitives via the distinction of
         loop plumbing vs. the reward brain. Our main conclusion is as follows. For open-ended real-world objectives
         whose success signal lives in the state of the world outside the transcript, scaling up the judge is not enough; out-
         of-band evaluation with access to the real world is a structural requirement for preventing the progress mirage.

         Keywords. LLM agents, autonomous loops, progress mirage, self-evaluation bias, evaluator grounding, out-of-band
         evaluation, reward hacking, benchmarks



Draft note. This manuscript is a preliminary draft comprising a                1 Introduction
controlled pilot measurement and the anonymized single-deployment
field observation that motivated it. The measurement holds the agent
fixed and manipulates the information-channel type of the evaluator;              Over the past few years, agents built on large language
the field observation is presented as motivation only. Generalization to
multiple models and tasks, and the full measurement after the prereg­          models (LLMs) have moved beyond one-shot responses
istration freeze, are deferred to follow-up work.                              toward autonomously executing multi-step tasks. An agent
                                                                               gathers context, invokes tools, verifies results, and retries,
                                                                               repeating this cycle without human intervention at every
                                                                               step. Recently, major platforms have begun to offer this
                                                                               cycle as a first-class feature: a loop form that re-executes
                                                                               a prompt at fixed intervals, and a goal form in which, once


                                                                           1
When Do Agent Loops Mistake Stagnation for Progress?                                                                 preliminary draft



a completion condition is defined, a separate small model             1.1 Our Approach
judges at every turn whether it is satisfied. The focus of               We propose an architecture that places the evaluator
the work thereby shifts from “instructing the agent on                out-of-band. The evaluator runs as a separate process,
individual tasks” to “designing the cycle that issues the             apart from the agent, and independently accesses real-
prompts.” We call this design activity loop engineering.              world ground truth rather than the conversation transcript.
   As cycles grow longer and human intervention becomes               Concretely, it reads databases, version-control history,
rarer, one question becomes decisive: who judges comple­              web analytics, and append-only ledgers with its own tools.
tion? The simplest answer is that the agent judges itself.            The evaluator enforces a reward function that asks whether
But an evaluator that grades its own work is systemati­               real-world metrics actually moved, and for cycles that fail
cally biased toward leniency. This self-evaluation bias has           this test it leaves a rejection artifact that the next loop
been observed repeatedly in preference-model and LLM-                 iteration is forced to read first at boot. This closes the path
as-judge research [Zheng et al., 2023], and it connects to            by which a cycle could terminate on self-evaluation alone.
reports that self-correction does not work reliably without           Figure 1 summarizes this structure.
external signals [Huang et al., 2024]. Self-reflection tech­             An out-of-band evaluator alone is not sufficient, and
niques such as Reflexion and Self-Refine depend directly              we present four auxiliary mechanisms around it. These
on the quality of self-evaluation [Shinn et al., 2023],               auxiliary mechanisms are design notes derived from field
[Madaan et al., 2023]; when the evaluation signal is weak,            observation; they are not individually validated by our
iteration can converge not on improvement but on elabo­               controlled measurements. First, state is recorded only as
rate stagnation.                                                      append-only logs or views derived from them, because
   Elaborate stagnation is precisely the failure mode this            a field overwritten in place becomes a device that man­
paper addresses. If the reward function is set up to score            ufactures falsehood. Second, handoff between sessions
outputs (analysis, new frames, self-checks) as progress,              happens through files, not conversation. Third, a frame-
a sufficiently capable agent will optimize that reward.               adversarial review makes the agent periodically attack its
Every cycle produces new analysis and passes the verdict              own deepest assumptions. Fourth, a self-healing scheduler
criterion. Progress accumulates in the loop’s own logs.               revives dead sessions.
Yet real-world metrics — users, revenue, indexed pages                   We support our claims with two kinds of evidence. First,
— do not move. This is an instance of reward misspeci­                as motivation, we present an anonymized six-week, 61-
fication and specification gaming [Amodei et al., 2016],              cycle field observation of a single production deployment.
[Krakovna et al., 2020], [Skalse et al., 2022]. An agent              In this deployment, every evaluated cycle was accepted
optimizing a proxy reward drifts away from the true goal to           under an in-band self-verdict that rewarded analysis,
the extent that the proxy diverges from it, and as autonomy           while real-world outcomes stagnated; when the reward
grows, this divergence persists longer and with greater               function was moved to real-world outcomes and enforced
confidence.                                                           out-of-band, the behavior reversed. A single observation,
   The heart of the problem lies in what the evaluator                however, cannot establish causality. The core evidence of
can see. Platform built-in judges are generally in-band:              this paper is therefore controlled measurement. We built
they judge based only on what the agent has placed into               loop-engineering-lab, a testbed that holds the agent and its
the conversation within the same session. When the task               tool surface fixed and manipulates only the information-
is well-bounded and verifiable from the transcript alone              channel type of the evaluator gating the loop; we enforced
(tests pass, the build succeeds, a file exists), this suffices.       a world-state oracle that is ungameable in principle via
But when the goal is open-ended and grounded in the real              container and network isolation; and we ran a real fron­
world — when the evidence of completion resides not                   tier agent repeatedly under three evaluator arrangements,
in the conversation but in the state of external systems              measuring the progress mirage and real-world output.
— an in-band evaluator is structurally unable to see that                The measurements are as follows. The agent claimed
evidence. If the agent writes “the metrics improved” into             in every cycle that its change was an improvement, and
the transcript, the in-band evaluator can only assess the             evaluators bound to the transcript accepted as progress a
statement; it has no means of verifying its truth. The eval­          substantial fraction of the cycles in which real-world met­
uator is trapped inside the narrative the agent constructs.           rics stagnated or regressed. The self-verdict loop eroded
                                                                      the best deployed state it had reached by accepting subse­


                                                                  2
When Do Agent Loops Mistake Stagnation for Progress?                                                             preliminary draft



quent regressions, while the out-of-band evaluation loop               explicit where the boundary lies within which in-band
grounded in the world-state oracle reached higher real-                evaluation suffices.
world output than the self-verdict loop. Yet even the
                                                                    1.3 Organization
strongest in-band judge — one that reads the transcript
                                                                       Section 2 reviews related work. Section 3 describes the
critically — failed to close this acceptance-error gap.
                                                                    architecture under test and the measurement apparatus.
When the success signal lives in the state of the world
                                                                    Section 4 presents the measurement results together with
outside the transcript, the cause of the gap is not the
                                                                    the motivating field observation. Section 5 discusses im­
evaluator’s quality but what the evaluator is grounded in.
                                                                    plications and trade-offs. Section 6 addresses threats to
Conversely, on a boundary task where success is verifiable
                                                                    validity, and Section 7 concludes.
within the transcript, the gap narrowed sharply. This falsi­
fication control supports the claim that our results are not        2 Background and Related Work
the product of an apparatus designed to favor a particular
arrangement, but the effect of evaluator grounding.
                                                                       This work concerns the loops of long-running au­
1.2 Contributions                                                   tonomous LLM agents. Our central claim is that when
  Our contributions are as follows.                                 an agent loop grades its own completion, self-evaluation
1. We formalize the progress mirage — the failure mode              bias causes it to accept process and analysis as progress
   in which a long-running autonomous agent mistakes                while real-world outcomes remain stagnant. We name this
   analysis and process for progress, so that the loop re­          phenomenon the progress mirage and propose an archi­
   ports advancement while real-world outcomes stagnate             tecture that separates the generator (the agent) from the
   — as a measurable phenomenon, and diagnose its cause             evaluator, placing the evaluator in a separate out-of-band
   as the in-band structure that traps the evaluator inside         process with independent access to ground-truth signals
   the transcript.                                                  (databases, version control, web analytics, append-only
2. We present loop-engineering-lab, a testbed that mea­             ledgers) rather than the agent’s conversation transcript.
   sures this phenomenon. For an open-ended task that               This section situates that contribution within five clusters
   cannot be verified by tests, it installs a synthetic-user        of literature, and at the end of each cluster makes explicit
   world-state oracle, enforces the agent’s in-principle            the gap our work fills.
   inability to reach that oracle via container and network         2.1 Autonomous LLM Agents and Self-Reflection
   isolation, and empirically verifies it with a boundary               That Depends on Self-Evaluation
   proof at every run. The measurement apparatus that                  The paradigm of using an LLM as an agent was estab­
   exposes a new failure mode is itself a contribution.             lished by ReAct, which interleaves reasoning and acting
3. We measure the causal effect of evaluator grounding              [Yao et al., 2023]. ReAct showed a synergy between
   under control. Holding the agent fixed and swapping              the two capabilities: reasoning traces guide action plans,
   only the evaluator’s information-channel type — in-              and actions collect observations from the external environ­
   band-self, a strong in-band-judge, and out-of-band               ment. Subsequent work extended this into a self-reflection
   — we measure the progress-mirage rate, real-world                family in which the agent critiques and improves its own
   output, and the number of cycles to the first real out­          outputs. Reflexion reinforces the agent with verbal feed­
   come. This design includes a preregistered adversarial           back instead of weight updates, accumulating the agent’s
   hypothesis testing whether the strongest in-band judge           own reflections on prior failures in episodic memory to
   closes the advantage of out-of-band.                             improve decision-making in the next attempt [Shinn et al.,
4. We generalize these results into an architecture cen­            2023]. Self-Refine likewise proposes an iterative refine­
   tered on an out-of-band evaluator, and situate it relative       ment loop in which the same LLM plays all three roles
   to platform built-in loop/goal primitives via the distinc­       of generation, feedback, and refinement [Madaan et al.,
   tion of loop plumbing vs. the reward brain. We argue             2023].
   that plumbing (scheduling, pacing, session revival) can             The shared premise of these methods is that the model
   be delegated to built-in primitives, whereas the reward          can reliably judge the quality of its own outputs. Huang et
   brain grounded in the real world cannot. We also make            al., however, showed that intrinsic self-correction without
                                                                    external feedback fails to improve performance on reason­


                                                                3
When Do Agent Loops Mistake Stagnation for Progress?                                                               preliminary draft



ing tasks and sometimes degrades it [Huang et al., 2024].            admits “easy” solutions that distort its intent — as a core
This critical result suggests that loops relying solely on           accident risk in AI safety [Amodei et al., 2016]. Krakovna
self-evaluation may fail to produce accurate progress sig­           et al. named behavior that satisfies the literal specification
nals. All of this literature, however, targets one-shot tasks        of an objective without achieving the intended outcome
or short bundles of attempts; it does not address how a              specification gaming, cataloguing many cases in which
long-running autonomous loop spanning multiple context               reinforcement-learning agents find shortcuts that collect
windows distorts its self-grading relative to ground-truth           reward without completing the task as intended [Krakovna
outcomes.                                                            et al., 2020]. Skalse et al. gave the first formal definition
                                                                     of reward hacking, defining a proxy as unhackable only
2.2 LLM-as-Judge and Self-Evaluation Bias
                                                                     when increasing the expected proxy reward can never de­
   Why self-evaluation cannot be trusted has been system­
                                                                     crease the expected true reward [Skalse et al., 2022]. Pan
atically established in the LLM-as-judge literature. Zheng
                                                                     et al. demonstrated empirically that more capable agents
et al., proposing MT-Bench and Chatbot Arena, which
                                                                     exploit the gaps in misspecified proxy rewards more effec­
use strong LLMs as evaluators, reported that LLM judges
                                                                     tively, raising proxy reward while lowering true reward,
exhibit position bias, verbosity bias, and self-enhancement
                                                                     with a phase transition at a capability threshold where true
bias [Zheng et al., 2023]. Self-enhancement bias in partic­
                                                                     reward drops sharply [Pan et al., 2022].
ular — the evaluator’s tendency to prefer outputs similar
to its own — is a direct threat to self-grading loops. Pan­             This risk has also been characterized quantitatively.
ickssery et al. characterized this more precisely, showing           Gao et al. showed scaling laws for overoptimization, in
that LLM evaluators can recognize their own generations              which optimizing against a proxy reward model beyond
(self-recognition) and that a linear correlation exists be­          a certain scale actually harms true reward [Gao et al.,
tween the strength of this recognition ability and the               2023], and Manheim and Garrabrant classified the failures
strength of self-preference bias [Panickssery et al., 2024].         that arise when a proxy stands in for a goal as variants
                                                                     of Goodhart’s law [Manheim and Garrabrant, 2018]. This
   This cluster establishes that evaluation is structurally
                                                                     cluster provides, in general form, the core problem of
biased when generator and evaluator are the same model.
                                                                     our work: the divergence between proxy and true reward.
These studies, however, measure preference verdicts over
                                                                     Our progress mirage can be read as an LLM-agent-loop-
static response pairs and restrict the evaluator’s input to
                                                                     specific instance in which completion verdicts based on
model-produced text (responses, transcripts). Recent work
                                                                     self-evaluation are themselves a hackable proxy reward,
that widens the target to agent trajectories rests on the same
                                                                     and the more capable the agent, the more effectively it
limitation. AgentRewardBench quantified the systematic
                                                                     optimizes this proxy while real-world outcomes stagnate.
errors of LLM-judge verdicts on web-agent trajectories
                                                                     The reward-hacking literature, however, mainly targets
against human ground-truth labels [Lù et al., 2025], but
                                                                     reward functions in reinforcement-learning environments
does not treat the evaluator’s information channel itself as
                                                                     and does not treat the termination condition of a long-
a manipulated variable. Chain-of-thought monitoring, in
                                                                     running autonomous LLM agent loop as a reward-specifi­
which another model watches the reasoning process, like­
                                                                     cation problem.
wise showed that as long as the monitoring signal remains
in model-produced text, the agent can be optimized to                2.4    Generator-Evaluator Separation, RLHF Re­
circumvent that channel [Baker et al., 2025]. We hold that                 ward Modeling, and Process vs. Outcome Super­
the way to escape this bias lies in separating the evaluator’s             vision
input from text: what the evaluator grades must be not                  The design that separates the evaluator from the gener­
the transcript in which the agent narrates what it did, but          ator is already established in RLHF reward modeling.
ground-truth signals recorded in external systems.                   Christiano et al. proposed deep reinforcement learning
2.3 Reward Hacking and Specification Gaming                          from human preferences, learning a separate reward model
                                                                     from human preferences to optimize the policy, thereby
   The failure in which a self-grading loop mistakes
                                                                     structurally separating the generating policy from the
process for progress is isomorphic to reward hacking
                                                                     evaluative reward signal [Christiano et al., 2017]. Ouyang
and specification gaming in the reward-specification liter­
                                                                     et al.‘s InstructGPT applied this separation to large-scale
ature. Amodei et al. formalized reward hacking — arising
                                                                     language-model alignment, fine-tuning the policy with a
when the objective function the designer wrote down
                                                                     reward model trained on human feedback over output


                                                                 4
When Do Agent Loops Mistake Stagnation for Progress?                                                             preliminary draft



rankings [Ouyang et al., 2022]. Bai et al.’s Constitutional        substantially [Yang et al., 2024]. These studies demon­
AI externalized the source of the evaluation signal into a         strate that execution-based grading is more reliable than
set of principles, performing alignment based on AI feed­          self-report, but they use evaluation as a one-time grading
back [Bai et al., 2022].                                           step for a benchmark, not as a standing in-loop reward
   The question of where the evaluation signal is taken            function that enforces the termination condition of a run­
from also connects to the process vs. outcome super­               ning loop.
vision debate. Uesato et al. systematically contrasted                Industry engineering guidance addresses this gap more
process-based and outcome-based feedback in mathemat­              directly. Anthropic’s guidance on building effective agents
ical problem solving [Uesato et al., 2022], and Lightman           presents design principles for raising the complexity of
et al. showed that process supervision, which gives feed­          agentic systems only as much as needed and for secur­
back at every intermediate reasoning step, outperforms             ing reliability when agents operate autonomously across
outcome supervision, which gives feedback only on the              multiple turns [Anthropic, 2024]. Harness guidance for
final result, on mathematical reasoning tasks [Lightman et         long-running agents goes a step further, recommending
al., 2023]. From our perspective, this contrast shows that         a structure that combines progress files with version-
the choice of evaluation target is decisive.                       control history so the agent maintains progress across
   The scalable-oversight family, which seeks to extend            context windows, and that has the next session confront,
supervision by strengthening the evaluator — debate,               as ground truth, a list marking each feature “passing” or
which elicits truth through argumentation [Irving et al.,          “failing” [Anthropic, 2025]. Related harness-design guid­
2018]; recursive reward modeling, which recursively del­           ance likewise holds that each component of a harness
egates evaluation itself to learned reward models [Leike           encodes an assumption about what the model cannot do on
et al., 2018]; and weak-to-strong generalization, in which         its own [Anthropic, 2025b]. These engineering guidelines
a weak supervisor guides a strong model [Burns et al.,             connect directly to our concern, but they have not been
2023] — commonly focuses on building better judges.                formalized into a peer-reviewed architecture, and they
Our adversarial hypothesis HA1 directly tests exactly this         do not generalize the approach of isolating the evaluator
premise — that raising judge quality makes supervision             into an out-of-band separate process without access to the
sufficient — on open-ended real-world objectives, and its          agent’s transcript, defining a reward function over plural
rejection suggests there are domains where the ceiling is          real-world signals such as databases, web analytics, and
not judge quality but the judge’s information channel. But         append-only ledgers.
the evaluation signals of RLHF reward models and process           2.6 Direct Comparison with Contemporaneous
supervision all take model-produced text (responses, rea­              Measurement Studies
soning steps) as input. Our work inherits the generator-
                                                                      The exact combination we address — the causal effect
evaluator separation principle of reward modeling but
                                                                   of the evaluator’s information-channel type (transcript
differs in replacing the evaluator’s input with ground-truth
                                                                   reading vs. world-state querying) on self-deception under
signals from external systems rather than model-produced
                                                                   open-ended real-world objectives — is closest to a cluster
text, and in placing the evaluator as a separate process
                                                                   of measurement studies that formed rapidly in late 2025
operating inside the loop at execution time rather than at
                                                                   and 2026. We therefore contrast this cluster individually
training time.
                                                                   and make explicit the empty cell our work occupies.
2.5 Autonomous Software-Engineering Agents and                        SpecBench quantifies reward hacking in long-horizon
    Harness Design                                                 coding agents as the pass-rate gap between visible valida­
   The literature on long-running coding agents and their          tion tests and hidden held-out tests, showing that the gap
harnesses provides the most direct precedent for ground­           grows steeply with task length [Zhao et al., 2026]. It
ing evaluation in ground truth. SWE-bench has models               shares our concern with the in-band vs. out-of-band gap,
modify a codebase on tasks built from real GitHub issues           but SpecBench’s ground truth is held-out unit tests and
and corresponding pull requests, judging completion not            the evaluation channel on both sides is test execution. Our
by the model’s self-report but by running the repository’s         work differs in that (a) it takes as ground truth a world-
test suite [Jimenez et al., 2024]. SWE-agent designed              state oracle (synthetic user conversions) that cannot be
an agent-computer interface that lets the agent edit files,        verified by tests, and (b) it treats the evaluator’s informa­
navigate the repository, and run tests, raising performance


                                                               5
When Do Agent Loops Mistake Stagnation for Progress?                                                                preliminary draft



tion-channel type itself as the manipulated variable while             half of 2026. Advani characterized false success — agents
holding the agent fixed.                                               confidently declaring completion while the environment
   Pan et al. showed spontaneous reward hacking in itera­              state is failure — on large trajectory sets from verifiable
tive self-refinement on open-ended essay tasks, where the              benchmarks (tau2-bench, AppWorld), showing that no
LM evaluator’s score rises while actual quality stagnates              combination of five judges and five prompts detects it reli­
or declines [Pan et al., 2024]. This is the same phenome­              ably [Advani, 2026]. That result is directionally consistent
non as our progress mirage, but their evaluator is another             with our rejection of HA1, with two differences: Advani’s
text-reading judge, and they include no world-state oracle,            tasks are verifiable, with programmatic ground truth, and
no channel-type manipulation, and no judge-quality abla­               the judges are merely compared against fixed ground truth
tion.                                                                  — the evaluator’s information-channel type itself is not
   EvilGenie reports that on coding tasks an in-band LLM               manipulated. Wang et al. compared four verifier config­
judge is highly effective at detecting reward hacking and              urations for coding-agent reward — tests, rubrics, user
that held-out tests add little [Gabor et al., 2025]. This result       verification, and agent verification — showing that none
appears at first to conflict with our claim, but it is in fact         is a panacea [Wang et al., 2026], and Flynt, starting from
consistent with our boundary hypothesis H2. In coding                  cases where frontier judges score ungrounded responses
settings where the hack is identifiable (unambiguous) from             highly, proposes deterministic trajectory-based grading
the transcript, a strong in-band judge suffices. Our claim is          [Flynt, 2026]. In the context of agent-organization design,
restricted to open-ended objectives whose success signal               Xie reported a large divergence between self-reported
lives in world state outside the transcript, and we measure            success rates and measured recovery rates as agent self-
both regimes within the same experiment to draw that                   deception [Xie, 2026]. All of these confirm, from different
boundary. EvilGenie therefore reads not as a counterexam­              angles, the existence of the phenomenon we target, but
ple but as external confirmation of the boundary condition.            none performs a controlled measurement that manipulates
                                                                       only the evaluator’s information-channel type on non-
   Çağatan and Zhao show, in text-based AI Safety Grid­
                                                                       verifiable open-ended tasks whose success signal is in
worlds, a separation between observed reward and hidden
                                                                       principle outside the transcript.
safety objectives, reporting that standard reinforcement-
learning optimization widens the gap [Çağatan and Zhao,                   New adjacent work identified in a pre-submission res­
2026]. This is a toy RL environment, not a real-world or­              can (2026-07-23) also falls within the same map. Scope­
acle responding to deployed artifacts. RewardHackingA­                 Judge performs an ablation over five levels of transcript
gents benchmarks evaluation-integrity attacks in which                 context visible to a judge that gates a security agent’s
ML-engineering agents tamper with metric computation                   tool calls before execution [Caldwell et al., 2026]. The
or induce train/test leakage, together with defenses (eval­            grammar of manipulating what the evaluator sees is shared
uator locking) [Atinafu and Cohen, 2026]. That is a threat             with our design, but all five levels vary the amount of
model in which the agent actively attacks the evaluator,               in-transcript context, and the object of judgment is com­
whereas we isolate the agent by network so that it cannot              pliance with a pre-declared scope rather than progress
reach the evaluator (the oracle) at all and empirically                on an open-ended goal; a world-state channel outside the
verify this unreachability at every run; the threat models             transcript appears at no level. On the training side, RePro
differ and the two works are complementary.                            trains agents to self-generate progress signals [Ma et al.,
                                                                       2026]; since this strengthens in-band self-signals, our re­
   Two further adjacent strands exist. First, the line that
                                                                       sults supply the boundary condition for where such signals
evaluates agents with synthetic users. tau-bench grades
                                                                       can be sound (tasks whose success signal is verifiable
an agent by comparing the final state of a database after
                                                                       inside the transcript). Work on early diagnosis of wasted
conversation with a simulated user against a ground-truth
                                                                       computation in multi-agent systems shares our concern
answer [Yao et al., 2024], sharing raw material with our or­
                                                                       with wasted cycles but does not manipulate the evaluator’s
acle (world state produced by a synthetic user simulator).
                                                                       information channel [Li et al., 2026].
But tau-bench’s grading is one-time grading on a verifiable
benchmark with a specified answer state, and it does not                  In sum, the uniqueness of this work lies in the combi­
treat the evaluator arrangement as a manipulated variable.             nation of three anchors, with the center of gravity on the
Second, a line measuring the divergence between agents’                second. (1) We ground a non-verifiable open-ended task,
completion claims and actual success formed in the first               for which no answer specification exists in principle, with


                                                                   6
When Do Agent Loops Mistake Stagnation for Progress?                                                                 preliminary draft



a world-state oracle; (2) with the same agent and the same             3 Method: The Architecture Under Test and the
task, we manipulate only the information-channel type of                 Measurement Apparatus
the evaluator gating the loop (to our knowledge this design
appears nowhere in the cluster above); and (3) we separate
                                                                          This section consists of two parts. The first half
the irreducibility of grounding vs. judge quality with an
                                                                       describes the architecture we propose and validate — a
ablation inside the same apparatus. Since anchor (3) alone
                                                                       design centered on an out-of-band evaluator. This archi­
already receives strong evidence from Advani’s results,
                                                                       tecture is the treatment manipulated in the measurement.
we position (3) as an auxiliary pillar to (2). Given how
                                                                       The second half describes loop-engineering-lab, the appa­
fast the field is moving, we state this combination as our
                                                                       ratus that measures the treatment’s causal effect under
criterion of occupancy and preregister the position that,
                                                                       control. The core of the measurement is to hold the agent
should work performing the identical combination appear,
                                                                       and its tool surface fixed across all conditions and to swap
we will narrow our claim to the residual gap.
                                                                       only the information-channel type of the evaluator that
2.7 Summary of the Research Gap                                        terminates the loop. We first cover the design principles,
    In sum: the self-reflection literature (2.1) builds loops          the out-of-band evaluator, the real-world reward function,
that depend on self-evaluation but assumes its reliability;            the four auxiliary mechanisms, the cycle protocol, and
the LLM-as-judge literature (2.2) establishes self-evalua­             the three layers of cadence, and then describe in turn
tion bias but restricts the evaluation input to model-pro­             the apparatus’s open-ended task, the world-state oracle,
duced text; the reward-hacking literature (2.3) generalizes            isolation and boundary proof, the three evaluator arms, the
the proxy vs. true reward divergence but does not apply                dependent variables, and the pilot scope.
it to the termination conditions of LLM agent loops. The
                                                                       3.1 Design Principles
reward-modeling and process-supervision literature (2.4)
                                                                          The architecture follows three principles. First, the
establishes generator-evaluator separation but takes the
                                                                       entity that works and the entity that judges are separated.
evaluation signal from text and places it at training time.
                                                                       Second, the judging entity looks at the state of the world,
The autonomous software-engineering agent and harness
                                                                       not at the narrative constructed by the working entity.
literature (2.5) demonstrates execution-based ground-
                                                                       Third, the outcome of the verdict is recorded in a form
truth grading but does not formalize it as a standing reward
                                                                       the next iteration cannot evade. These three principles are
function of a running loop.
                                                                       realized, respectively, as generator-evaluator separation,
   Our work fills the following gaps. First, we formalize              out-of-band access, and forced feedback.
the progress mirage — self-evaluation bias mistaking
process and analysis for progress in long-running au­                  3.2 Generator-Evaluator Separation and the Out-
tonomous LLM agent loops — as a reward-specification                       of-Band Evaluator
problem. Second, we separate the generator (agent) from                  The generator is the agent. The generator doubts, forms
the evaluator, isolating the evaluator into an out-of-band             hypotheses, sets direction, delegates work to a worker that
separate process without access to the agent’s conversation            executes it, and reviews the results in the first instance.
transcript, and define a real-world reward function over               But because the generator’s self-review is exposed to self-
plural ground-truth signals: databases, version control,               evaluation bias, it holds no authority to close a cycle. That
web analytics, and append-only ledgers. Third, the evalu­              authority belongs to the evaluator.
ator records rejection artifacts that the next loop iteration is          The evaluator does not operate inside the same session
forced to confront, so that the loop’s termination condition           as the generator. It runs as a separately scheduled process
is governed not by in-band self-verdicts but by out-of-band            and accesses real-world ground truth directly, rather than
evaluation anchored in real-world signals. These three                 the generator’s conversation transcript. Concretely, the
are the loop-engineering contributions this paper offers in            evaluator reads the operational database, version-control
place of transcript-based in-band self-judgment.                       history, web analytics, and an append-only ledger with its
                                                                       own tools. This separation is the crux. An in-band evalu­
                                                                       ator has no means to verify the truth of the statement when
                                                                       the agent writes “the metrics improved,” whereas an out-
                                                                       of-band evaluator puts the same question directly to the
                                                                       world. Figure 1 summarizes this structure.


                                                                   7
When Do Agent Loops Mistake Stagnation for Progress?                                                               preliminary draft



   This design belongs to the same lineage as generator-              When a derived view is needed, it is computed determin­
discriminator separation and the reward-model separation              istically from the append-only log.
of RLHF [Christiano et al. 2017], [Ouyang et al. 2022],
                                                                      3.6 File-Based Handoff
but is distinguished by placing the evaluator’s input in
                                                                         Handoff between sessions happens through files, not
external system state rather than in the model’s internal
                                                                      conversation. A long-running loop necessarily spans mul­
representations or the conversation.
                                                                      tiple sessions due to context limits, and if progress is
3.3 The Real-World Reward Function                                    carried across session changes only as conversation sum­
   The reward function the evaluator enforces asks about              maries, loss and distortion accumulate. If the artifacts,
outcomes, not process. That is, it asks not “did this cycle           ledgers, derived views, and next-step plans are all kept in
produce new analysis” but “did real-world metrics actu­               files, each subsequent session starts from the same ground
ally move.” As the reward-misspecification literature has             truth. The importance of progress files and pass/fail crite­
shown, an agent optimizing a proxy reward drifts from the             rion lists in long-running agent harness design has also
goal to the extent that the proxy diverges from it [Pan et            been emphasized in industry reports [Anthropic 2025].
al. 2022], [Skalse et al. 2022]. The reward function must
                                                                      3.7 Frame-Adversarial Review
therefore be tied to a signal as close to the goal as possible,
                                                                         The agent is made to periodically and adversarially
not to a proxy.
                                                                      attack its own deepest assumptions. A small number of
   Concretely, the reward function forces every cycle to              assumptions underpinning the operation are made explicit
read the real-world arrival ledger first and compute how              in a registry, and periodically — and whenever specific
many days the metrics have been flat. When stagnation ex­             conditions are met (e.g., metrics worsening consecutively)
ceeds a threshold, an operating mode is forcibly switched             — the agent is forced to output, for each assumption,
on, and in that mode ACCEPT is possible through only                  “if this assumption is wrong, what is the alternative,
three paths: deploying a real acquisition mechanism live,             and what are the grounds for keeping or discarding it.”
deepening product value verified against external (non-in­            Given the observation that self-reflection techniques can
ternal) personas, or escalating the binary forcing function           converge on stagnation without external signals [Huang et
upward. Cycles that only produce analysis or only touch               al. 2024], this adversarial ritual functions as a device for
policy wording are blocked in this mode. This transposes              surfacing frame-level errors that self-evaluation misses.
the distinction between process reward and outcome re­                The efficacy of this mechanism is, however, capped by
ward into an operating rule [Lightman et al. 2023].                   model capability; we discuss this limit in Section 6.
3.4 Rejection Artifacts and Forced Feedback                           3.8 Self-Healing Scheduler
   The evaluator’s verdict does not evaporate. If the real-              Because the loop must operate for long periods without
world signal is zero and the cycle presents no valid                  continuous human intervention, recovery from missed
evidence (e.g., a version-control commit or a live URL),              boots and session deaths is required. A separate scheduler
the evaluator leaves a rejection artifact as a file. The next         checks the elapsed time of the last active session and
loop iteration is wired to read this rejection artifact first         reboots sessions that have stalled past their normal period,
at boot. This closes the path by which a cycle could ter­             restricted to active hours. This mechanism belongs to
minate on self-evaluation alone, and the previous cycle’s             operational plumbing, not to the essence of the architec­
failure becomes the next cycle’s first input. Because the             ture, and can be replaced by platform-provided scheduling
evaluator is separated from the generator and looks at the            primitives. We return to this distinction in Section 5.
world directly, even if the agent dresses up stagnation as
progress, it will face that dressing-up at the next boot.             3.9 Cycle Protocol
                                                                        A cycle proceeds in the following order. Figure 2 sum­
3.5 Append-Only State
                                                                      marizes it.
   State is recorded only as append-only logs or views
                                                                      1. BOOT. Read first the rejection artifact left by the pre­
derived from them. Overwriting the same field in place is
                                                                         vious cycle.
forbidden. If in-place updates are allowed, the state file
                                                                      2. AUDIT. Measure actual state first, not cached sum­
becomes not a record of truth over time but a device for
                                                                         maries.
re-narrating the past to fit the current story — a channel
through which self-evaluation bias seeps into state itself.


                                                                  8
When Do Agent Loops Mistake Stagnation for Progress?                                                               preliminary draft



3. INTENT. Pose one broad question, not a narrow classi­             rendered landing page, page payload size, the number of
   fication.                                                         funnel steps, and copy length — computes a weighted
4. Generate-execute ping-pong. Early phases pass                     logistic conversion probability, and produces a conversion
   through doubt and reframing, middle phases through                count over a fixed cohort. Within a repetition, the same
   hypothesis injection, late phases through strategic               cohort random numbers are used across cycles (common
   guidance; when the worker brings back results, the                random numbers), so the conversion count is a monotone
   generator receives and reviews them again.                        deterministic function of artifact features and the sign of
5. ACCEPT. The termination condition is not a cycle                  a delta cannot be flipped by sampling noise. This conver­
   count but the production of a new frame (frame-tran­              sion count is recorded in an oracle store the agent cannot
   scendence).                                                       access. These conversions respond only to the physical
6. STATE WRITE. Record state append-only.                            properties of the deployed artifact, not to the agent’s
7. External verification. The evaluator, in a separate               narrative. The agent writing “I raised conversion” and the
   process, checks real-world signals directly and leaves            simulator’s conversion count actually rising are entirely
   a rejection artifact if needed.                                   separate things.
3.10 Three Layers of Cadence                                            The oracle’s ungameability is guaranteed by three in­
   Three layers of cadence overlay the cycle above. Layer            variants. The values the oracle reads are (a) outside the
A is rare human intervention injecting direction in ad-              agent’s write access, (b) produced by an independent
hoc sessions. Layer B is the operating headquarters’ own             process (the simulator) rather than by the agent’s state­
loop, consisting of briefings, critiques, and retrospectives         ments, and (c) in principle unverifiable from the transcript
at fixed times. Layer C is the ping-pong loop that forcibly          alone. Because this task is grounded by a world-state
separates generator and evaluator. The human role is con­            oracle rather than hidden unit tests, it is distinct from the
fined to Layer A’s rare direction injection and permanent            held-out tests of the coding-benchmark lineage.
escalations; the loop runs the rest by itself.                       3.13 Isolation and Boundary Proof
3.11 Measurement Apparatus: loop-engineering-lab                        To make ungameability a matter of enforcement rather
   The core claim of the architecture above is that placing          than convention, the two trust zones are physically sepa­
the evaluator out-of-band reduces self-deception and in­             rated. The agent container and the oracle container are
creases real-world output. To measure this under control,            placed on two separate networks with no route between
we build a testbed that holds the agent and its tool                 them. The agent uses the external internet for model API
surface identical across all conditions and swaps only the           calls but has no path to the oracle network at all, so even
evaluator that gates the loop. The evaluator’s information-          with a shell and network tools it cannot reach the oracle.
channel type (transcript reading vs. world-state querying)           The only shared surface is the agent’s deployed-artifact
is the sole independent variable, and agent capability is            volume, which the oracle reads read-only. The oracle store
controlled. Any difference between conditions therefore              lives inside the oracle container and on no shared volume.
stems solely from what the evaluator can see, not from the           The trusted party is the host runner, which accesses both
agent being smarter.                                                 sides for instrumentation only; only the agent — the party
                                                                     with the incentive to game — is isolated.
3.12 The Open-Ended Task and the World-State
                                                                        We prove this isolation by measurement, not assump­
     Oracle
                                                                     tion. The oracle serves a secret canary string on a port on
   The task is to edit a signup-funnel web app (landing              its own network. At the start of every measurement run
page, funnel step definitions, marketing copy) to maxi­              (each combination of arm and repetition), the trusted host
mize actual signups. This task is open-ended: there are              fetches the canary (proving the server is alive), the agent
many routes to raising conversion (a clear CTA, fewer                fails to fetch it even when given the oracle’s exact IP
steps, copy length, lighter pages, and so on) and no single          (no route), and the agent is confirmed unable to read the
unit test that verifies a correct answer. The crux is that the       oracle store from its own filesystem; all of this is recorded
success signal lies outside the agent’s transcript.                  in a per-run boundary log. Isolation is judged established
   Success is measured by a synthetic user simulator.                only when the host obtains the canary and the agent
Each cycle, the simulator extracts the actual properties             obtains it neither by network nor by filesystem; if it is
of the deployed artifact — the presence of a CTA on the              not established, measurement does not begin. In addition,


                                                                 9
When Do Agent Loops Mistake Stagnation for Progress?                                                                preliminary draft



every cycle the full agent-side output and artifact files are            Across the three arms the agent (model, tools, task,
scanned for the canary string, and the apparatus is wired             cycle budget) is identical. Only the gate evaluator and the
to abort measurement if it ever appears (zero occurrences             feedback it returns to the loop differ. Each arm’s trajectory
in this measurement). All measurements in this paper were             is an independent rollout, so the three evaluators do not
collected only with this boundary proof established.                  judge the same candidate sequence; comparisons between
                                                                      arms are made at the level of the distribution over repeti­
3.14 The Three Evaluator Arms
                                                                      tions. In addition, an independent monitor with no role in
  The evaluator arrangement is the key independent vari­
                                                                      gating records the oracle’s actual trajectory in all arms.
able; three implementations sit behind the same interface.
                                                                      This monitor is what allows the in-band arms’ self-decep­
1. in-band-self: judges from the agent’s self-report alone.
                                                                      tion to be measured against an external standard.
   In implementation, if the agent actually edits files
   and reports the rationale for the change, the cycle is             3.15 Cycle Protocol and Dependent Variables
   accepted. In our measurement the agent claimed in                     Each cycle proceeds in four steps. (1) The agent pro­
   every cycle that its change was an improvement, so                 duces a candidate change. (2) The gate evaluator issues a
   this arm effectively operates as an accept-all baseline.           verdict according to its arm. (3) The monitor records the
   This is not a defect; it is what this arm is designed to           oracle delta (candidate vs. deployed state). (4) On accep­
   measure. Self-claims carry no information, and a self-             tance the candidate is promoted to the deployed state; on
   verdict gate passes that uninformative signal straight             rejection the artifact is rolled back to the last accepted
   through. The feedback merely returns the agent’s own               state and the rationale is fed back as input to the next
   claims, with no ground truth.                                      cycle. This repeats up to the cycle budget. This gated-
2. in-band-judge: a separate, stronger model reads the                deployment model, in which rejected candidates are never
   agent’s change summary, the full text of the produced              promoted to deployment, is the device that makes the gate
   files, the diff of the change against the deployed state,          actually govern state. As its algebraic consequence, the
   and its own past verdict history — but not the oracle —            out-of-band arm’s deployed state is structurally monotone
   and judges whether the change is an improvement. The               non-decreasing (it accepts only positive deltas), and the
   input cap is set generously and cap-hit status is logged           accept-all arm’s deployed state equals the last candidate.
   every cycle (zero hits in this measurement). The verdict           The shape of a deployment trajectory is therefore partly a
   prompt is a critical prompt that demands evidence and              theorem of the gate rule, and Section 4.5 interprets it on
   defaults to rejection, and it even includes a domain               that premise.
   warning that plausible decorative edits (adding social                Dependent variables are computed mechanically from
   proof, lengthening copy) can bloat the page and hurt               raw cycle logs with no human discretion. The progress-
   conversion (the full prompt is in the public repository).          mirage rate is the fraction of evaluator-accepted cycles
   It is thus the strongest in-band baseline constructible            whose monitor-measured oracle delta is zero or below. The
   in a single call, hinted at the oracle’s penalty direction.        preregistration draft’s wording was “cycles whose delta is
   This arm tests the adversarial hypothesis HA1.                     zero,” but that definition would exclude from the mirage
3. out-of-band: accepts only when the oracle’s actual con­            the worse error of accepting regressions (negative deltas),
   version delta is positive. The feedback is an acceptance           so this paper uses the zero-or-below definition as primary,
   or rejection rationale containing the post-gate oracle             discloses this definitional change as an amendment, and
   scalars (the delta and the current conversion count).              reports numbers under both definitions (Section 4.2). real-
   This treatment is therefore not a pure gate arrange­               outcome-at-budget is the conversion count of the deployed
   ment but the combination of a gate and ground-truth                (last-accepted) state at the end of the budget. time-to-first-
   feedback — a deliberate choice that models exactly                 real-outcome is the number of cycles until the oracle delta
   what a real deployment’s out-of-band evaluator returns             first turns positive, with right-censoring recorded. The
   (threats in Section 6). To decompose this combination              wasted-cycle ratio is the fraction of cycles whose oracle
   we include a sign-only variant that removes the oracle             delta is zero or below. In addition, to view the gate’s
   numbers from the feedback and returns only the accep­              discrimination independently of base rates, we report con­
   tance verdict; its measurement is reported in Section              ditional acceptance rates — the acceptance rate given delta
   4.6.                                                               zero-or-below and the acceptance rate given positive delta
                                                                      — and their complement, the false-rejection rate.


                                                                 10
When Do Agent Loops Mistake Stagnation for Progress?                                                                                 preliminary draft



3.16 Pilot Scope and Preregistration Status                                 Generator: agent                               Execution: workers
   The measurements reported in this paper are a pilot.             doubt, hypothesis, plan, delegate                     code, deploy, content

They comprise the open-ended task family T1 and the                                                        ↓ outputs
boundary contrast task B1 (Section 4.4), the three eval­
                                                                    Artifacts: commits, live URLs, measured metrics, append-only ledgers
uator arms, one fixed frontier agent model (the in-band-
judge’s judge is a stronger model), 3 independent repeti­
                                                                       Out-of-band evaluator                           In-band evaluator (contrast)
tions per arm, and a cycle budget of 6, plus a sign-only             separately scheduled process                          same-session model
variant decomposing the out-of-band feedback, with 3                reads DB, version control, and                   sees only the conversation tran­
repetitions (Section 4.6). Analysis is performed by scripts         web analytics with its own tools                              script

using only the standard library, producing the dependent                            ↓ real-world signals = 0 and no valid evidence
variables and the hypothesis verdict table from append-
                                                                     Rejection artifact written → the next iteration is forced to read it first
only cycle logs.
                                                                   Figure 1. The out-of-band verification architecture. The generator
   We state the preregistration’s status precisely. The hy­
                                                                   (agent) and the evaluator are separated, and the evaluator is a separate
potheses and verdict thresholds were registered before             process with independent access to real-world ground truth (databases,
measurement in documents and version-control commits,              version control, web analytics, ledgers) rather than the conversation
but the commit-hash freeze procedure that the registration         transcript. When real-world signals do not move, it leaves a rejection
document itself prescribed was not completed by the time           artifact that the next loop iteration is forced to confront. An in-band
                                                                   evaluator sees only the conversation, so verdicts grounded in real-
of the pilot. This pilot is therefore an exploratory mea­
                                                                                world reward are structurally impossible for it.
surement under a pre-freeze registration draft, and both
the difference between the registered definition and the            1.      BOOT             2.     AUDIT            3. INTENT           4. generate-
                                                                         read rejec­               measure               broad                execute
paper’s definition (the mirage definition above) and mid-                tion      file           actual state           opener             ping-pong
run apparatus modifications are disclosed as amendments                      first                                                          doubt, hy­
(the preregistration document and apparatus history in                                                                                       pothesize,
                                                                                                                                               enact
the appendix). Among the registered factors, the reward-
function axis (process vs. outcome) and the hypotheses                                                           ↓
attached to it — H3 and the cost hypothesis HA2 — were
                                                                    5.        ACCEPT                 6. STATE WRITE             7. external verifica­
not run in this pilot and no results are reported for them.               frame-transcen­                append-only                      tion
Multiple models, a task with a server-side event log as a                      dence                        record                 enforce (separate
second oracle, the reward-function axis, and the full mea­                  (not a count)                                                cron)

surement after the commit-hash freeze are future work.                                    on rejection ⤶ step 7 feeds back into step 1
                                                                   Figure 2. The loop cycle. One iteration runs from BOOT (confronting
                                                                   the previous rejection) through external verification, and the termina­
                                                                   tion condition is frame-transcendence (production of a new frame), not
                                                                   a cycle count. A rejection from external verification feeds back into
                                                                   the next BOOT, preventing cycles from terminating on self-evaluation
                                                                                                    alone.


                                                                   4 Measurement Results

                                                                      This section reports the results of the controlled pilot
                                                                   collected with the apparatus of Section 3. The agent
                                                                   (model, tools, task, cycle budget) was held identical across
                                                                   all conditions, and only the information-channel type of
                                                                   the evaluator gating the loop was swapped among in-band-
                                                                   self, in-band-judge, and out-of-band. At the start of each of
                                                                   the nine T1 runs and nine B1 runs, the isolation boundary
                                                                   proof was performed and established (per-run boundary
                                                                   logs), and the canary scan of agent-side output and arti­
                                                                   facts found zero occurrences in every cycle. The judge


                                                              11
When Do Agent Loops Mistake Stagnation for Progress?                                                                preliminary draft



input cap was hit zero times. Analysis was performed                  of accepting regressions. In this pilot, the unproductive
with standard-library scripts over raw cycle logs, with no            cycles that the in-band arms accepted all had negative
human discretion. The oracle trajectories used to judge               deltas (actual damage). We report numbers under both
mirage in the two in-band arms are the measurements of                definitions; the rationale for the definitional amendment is
an independent monitor that those evaluators could not                in amendment A1.
observe; in the out-of-band arm, the gate itself queries the             The remaining registered dependent variables are also
same oracle by definition.                                            reported in full. time-to-first-real-outcome was identically
4.1 Summary of Results                                                1 cycle in all arms and all repetitions (zero right-censor­
  Table 1 summarizes the results for the three evaluator              ing). The starting state contained large first levers —
arms. Each arm was run in 3 repetitions, the cycle budget             introducing a clear CTA and cutting funnel steps — so
was 6, and the mean real-world conversion of the starting             the agents in all arms produced a real improvement in the
(baseline) state was 33.3.                                            first cycle; this variable therefore did not separate the arms
                                                                      under this task configuration (H3 was not run, along with
  Eval­ mi­ Accepted P(ac­ P(ac­ Deployed Fi­              Fi­
                                                                      the reward-function axis; amendment A9). The wasted-
   ua­     rage      cy­ cept|delta
                                 cept|delta peak   nal    nal
                                                                      cycle ratio (fraction of all cycles with delta zero or below)
   tor rate (range)cles     <=      > 0)         deployed real
  arm                        0)                           gain
                                                                      was coincidentally identical at 0.56 across the three arms,
in-band-0.56 (0.50,6.0 / 1.00 1.00 95.0 76.7 +43.3                    meaning the regression rate of candidate generation was
   self 0.67)         6                                               similar; what separated the arms was the gate’s discrimi­
in-band-0.44 (0.33,3.0 / 0.40 0.63 100.0 86.7 +53.3                   nation in filtering out those regression candidates. reward-
 judge 0.67)          6                                               hack incidence was not implemented in the pilot analysis
   out- 0.00 (struc­2.7 / 0.00 1.00 113.0 113.0 +79.7                 and is not reported (amendment A4).
    of- tural)        6
  band                                                                4.2 Self-Report Is an Uninformative Signal: in-
                                                                          band-self Degenerates into Accept-All (H1)
   Table 1. Measurement results by evaluator arrangement
                                                                         We begin with the most basic observation. The agent
(mean over 3 repetitions per arm, budget 6). The progress-
                                                                      claimed in all 54 T1 cycles (100 percent) that its change
mirage rate is the fraction of evaluator-accepted cycles
                                                                      would raise conversion. Yet by oracle measurement, 56
whose oracle-measured delta is zero or below (the primary
                                                                      percent of those cycles had a delta of zero or below.
definition of amendment A1). Parentheses are bootstrap
                                                                      The frontier agent’s self-claimed improvement was thus
percentile intervals over 3 trajectories and, at this sample
                                                                      uninformative as a signal of real-world progress. As its
size, should be read as observed ranges (Section 6.5).
                                                                      direct consequence, the in-band-self gate that trusts self-
Conditional acceptance rates show the gate’s discrimina­
                                                                      claims degenerated into an accept-all baseline, accepting
tion independently of base rates. The out-of-band arm’s
                                                                      all 18 cycles, and its mirage rate of 0.56 simply equals the
mirage of 0 and deployment monotonicity (final = peak)
                                                                      agent’s regression-generation rate. This is not a defect of
are definitional consequences of the gate rule (Section
                                                                      the gate; it is what this arm is designed to measure. The
3). Figure 4 visualizes the mirage rates and deployment
                                                                      self-evaluation channel contains no information to filter.
trajectories.
                                                                         An honest point must be made here. The out-of-band
   The mechanical verdicts on the preregistered hypothe­
                                                                      mirage rate of 0 is not an empirical finding but a conse­
ses are as follows. H1 is accepted: the mirage rate of
                                                                      quence of definition. Out-of-band accepts only when the
in-band-self exceeds out-of-band by 0.56, far above the
                                                                      oracle delta is positive, so accepting a cycle with delta
preregistered threshold of 0.20. The adversarial hypothesis
                                                                      zero-or-below is structurally impossible and the mirage
HA1 is rejected: even the strongest in-band-judge — given
                                                                      is always 0. This value should not be read as the core
untruncated input, the diff, and its verdict history — has
                                                                      evidence of this work. Our empirical claims come from
a mirage rate 0.44 above out-of-band, the exact opposite
                                                                      two places. First, how many regressions the transcript-
of HA1′s prediction that the gap would close to within the
                                                                      bound evaluators (the self-verdict, and the strongest judge
0.05 threshold. Recomputed under the registration draft’s
                                                                      of Section 4.3) actually accept as progress, and how many
literal definition (delta exactly zero), all three arms have
                                                                      real improvements they reject. These values are not fixed
mirage 0.00 and H1 becomes undecidable — because
                                                                      by definition and must be measured. Second, whether
that definition excludes from the mirage the worse error
                                                                      that gap narrows on a task whose success signal is inside


                                                                 12
When Do Agent Loops Mistake Stagnation for Progress?                                                                  preliminary draft



the transcript (the falsification control of Section 4.4).             This is the most important result of our measurement; it is
Together these show that our results are not merely the                consistent with contemporaneous work reporting judges’
product of an apparatus designed to favor out-of-band.                 failure to use information on verifiable tasks [Advani,
                                                                       2026], and goes beyond it by manipulating the information
4.3 Even the Strongest In-Band Judge Fails to Close
                                                                       channel itself to isolate the cause.
    the Gap (HA1)
   Our adversarial hypothesis was that the weakness of                 4.4 Falsification Control: On a Task Where Success
in-band lies not in the information channel but in judge                   Is Visible, the Gap Disappears (H2)
quality. To test it, the in-band-judge arm gave a model                   To show that our results are not merely the product of
stronger than the agent everything: the change summary,                an apparatus designed to favor out-of-band, we must also
the full text of produced files (no truncation; zero cap hits),        measure the condition under which our claim ought to fail.
the diff against the deployed state, and its own past verdict          That condition is the boundary task B1. In B1, success is
history — withholding only the oracle — under a critical               a structural specification verifiable from the artifact itself:
prompt that demands evidence, defaults to rejection, and               the number of five requirements satisfied — form pres­
warns of the risk of decorative edits. It is the strongest in-         ence, an email input, a submit control, exactly 3 canonical
band baseline constructible in a single call.                          steps, and copy of 40 to 80 words. This specification is
   This strong judge was distinctly more critical than the             given identically to all evaluators and is verifiable from the
self-verdict. It cut acceptances from 6 cycles to 3, and               artifact alone. A transcript-reading judge therefore holds
in conditional acceptance terms accepted only 40 percent               effectively the same information as the oracle. If our claim
of regressions (the self-verdict accepted 100 percent), so             is right, the gap between in-band and out-of-band must
the direction of its discrimination was right. But the gap             narrow on this task.
remained. Of the cycles it accepted, 44 percent were still                The results support that prediction exactly as registered.
real-world regressions — a gap of 0.44 to out-of-band,                 Table 2 contrasts the mirage rates on T1 and B1. The
nine times the preregistered threshold of 0.05. At the same            same strengthened judge’s mirage rate was 0.44 on the
time, the judge rejected 37.5 percent of real improvements             hidden-metric task T1 but vanished to 0.00 on the visible-
(false rejection). The strong judge’s errors are thus bidi­            specification task B1. In conditional acceptance terms,
rectional: not a problem of leniency but a ceiling on                  the B1 judge showed perfect discrimination, rejecting
discrimination.                                                        every unproductive cycle and accepting every satisfying
   The judge’s actual verdict rationales reveal what this              cycle, and the gap to out-of-band was 0.00, meeting the
ceiling is. In one cycle the agent added a styled hero                 preregistered threshold (0.05 or below), so H2 is accepted.
section and benefit bullets; the judge accepted it as a clean,         The augmentation edits the agent kept producing after
friction-reducing change, but actual conversion fell by 23             the specification was fully satisfied — wording polish,
(page bloat). In another cycle it accepted concise social              adding placeholders — which do not change the satisfied
proof right above the CTA as adding no friction or bloat,              count, the judge correctly judged unproductive against
but conversion fell by 10. In the opposite direction, it re­           the specification and rejected. Set beside the fact that the
jected the removal of a verification step (measured +7) as             same judge accepted 40 percent of regressions on T1, the
merely inflating unverified signups, and rejected rewrites             conclusion is sharp: the judge’s failure is not a matter of
it judged, from circumstantial evidence, to have broken                capability but of where the success signal resides, and
links (measured +15, +16). These rationales are one and                the moment ground truth enters the transcript, the failure
all plausible as conversion-optimization orthodoxy, and                disappears.
some are even sound from a real-world perspective. The                    One more contrast: in-band-self remained at mirage
problem is that nothing in the transcript says what sign that          0.50 even on the visible task. The self-verdict passes its
orthodoxy actually produces in this world (the simulator’s             own claims through without even checking them against
response function). From the full file text and the diff, the          the specification (accept-all), so it fails even when the
judge could compute feature values themselves, such as                 success signal is in plain view. The boundary condition
page size and copy length, but it could not know which                 of H2 is thus a statement about competent in-band evalu­
features move conversion and by how much (the sign and                 ation; the self-verdict is uninformative as a gate regardless
magnitude of the weights). The cause of the gap is not the             of task type. This asymmetry — the self-verdict fails
judge’s critical capacity but what the judge is grounded in.           everywhere, the judge succeeds exactly when the signal is


                                                                  13
When Do Agent Loops Mistake Stagnation for Progress?                                                                   preliminary draft



visible — is itself evidence of falsifiability: the apparatus        we treat the mirage rate and conditional acceptance rates
was not designed to make in-band lose unconditionally.               as the primary diagnostics.
  Evaluator arm        T1 mirage (hid­ B1 mirage (visi­                 In this pilot out-of-band was also highest in final output,
                          den metric)     ble specification)         but we do not claim this ordering is stable from a 3-
    in-band-self              0.56               0.50                repetition pilot. What can be claimed is structural: only
   in-band-judge              0.44               0.00                a discriminating gate preserves the best state reached
    out-of-band         0.00 (structural)  0.00 (structural)         (preventing erosion), and a transcript-bound gate cannot
    Table 2. Mirage rates by task type (mean over 3 repe­            provide that guarantee, erring in both directions — accept­
titions per arm, budget 6 for both tasks). T1′s mirage               ing regressions and rejecting improvements.
consists mostly of accepting actual damage (negative                    Finally, we disclose a case that exposes the gap between
deltas), whereas B1′s unproductive cycles are delta-0                the oracle and real-world value. When the agent removed
augmentation edits, so the two columns differ in kind. Out-          the email verification step, the oracle (which counts only
of-band is 0 by definition on both tasks. In the first run           conversions) rewarded it as an improvement, while the
(apparatus v1, with judge-input truncation), the B1 judge            judge rejected it as inflation of unverified signups. An
mirage was 0.17; after removing truncation and providing             out-of-band gate bound to a narrow metric passes such
the diff and verdict history in v2, it dropped to 0. The v1          changes. This is a construct-validity problem of the oracle
residual was thus an instrumentation defect (conflating              metric itself, separate from the in-band vs. out-of-band
state with delta), not the information channel — a fact that         gap, and is discussed in Section 6.
is itself consistent with our claim that the gap is caused by        4.6 Decomposing the Gate Effect from the Informa­
information access.                                                      tion Effect: Sign-Only Feedback
4.5 Real-World Output: The Gate’s Discrimination                        As stated in Section 3, the out-of-band treatment is not
    Governs the Deployed State                                       a pure gate placement but a combination of the gate and
   All three arms ended with positive final real gains               ground-truth feedback. The effect of the accept-or-reject
(Table 1), because the starting state contained a large lever        verdict itself overlaps with an information effect, in which
that agents in every arm captured in the first cycle. What           the oracle scalars carried in the feedback (the delta and
separated the arms came after.                                       the current conversion count) steer the agent’s subsequent
   in-band-self accepted all six cycles and still ended              candidate generation. To decompose this combination, we
lowest (from a mean peak of 95.0 down to a final 76.7,               additionally ran a sign-only variant on T1 with 3 repeti­
a 19 percent retreat). The erosion — a good state, once              tions, removing the oracle numbers from the feedback
reached, being whittled away by subsequent plausible                 and returning only the acceptance verdict. The apparatus,
regressions — reproduced in all three repetitions. in-band-          agent model, task, cycle budget, per-run boundary proofs,
judge filtered out many large regressions, reducing erosion          and per-cycle canary scans are identical to the measure­
(peak 100.0, final 86.7), but still retreated through the            ment of Section 4.1 (boundary proofs held in all 3 runs;
regressions it accepted, and forfeited the gains of the real         zero canary appearances); the only thing that changes is a
improvements it rejected (+7, +15, +16, and others). out-            single feedback string. The full variant returns the oracle
of-band ended equal to its peak in all three repetitions             delta and current value along with the verdict; the sign-
(113.0). As stated in Section 3, however, this monotonicity          only variant returns the fact of the verdict alone.
is itself a definitional consequence of the gate rule, so              out-of-   final de­      mean       accepted         wasted-
the empirical content here is not the monotonicity but the              band       ployed                   cycles         cycle ra­
difference in heights reached by three arms fed candidate              variant      value                                     tio
streams with the same regression rate (0.56). In an early                        (per rep­
                                                                                   etition)
apparatus variant without the gate (apparatus history in
                                                                      full feed­ 130, 117,       113.0       2.7 / 6          0.56
the appendix; a configuration where rejected cycles also
                                                                         back         92
remain deployed), final output did not separate the arms —
                                                                       (Section
meaning final output reveals the evaluator-channel effect                 4.1)
only in combination with the gate rule, which is also why             sign-only 122, 104,        110.0       3.0 / 6          0.50
                                                                       feedback      104



                                                                14
When Do Agent Loops Mistake Stagnation for Progress?                                                                 preliminary draft



   Table 3. Comparison of out-of-band feedback variants               divergence. When the evaluator reads the world, the same
(3 repetitions each, budget 6). In both variants the mirage           regressions are rejected and the state reached is preserved.
is 0 by definition and the deployment trajectory is monot­
                                                                      4.8 The Motivating Field Observation
one (Section 3). What is compared is the real-world output
                                                                         The phenomenon our measurement targets was ob­
the gate reaches and the quality of the candidate stream.
                                                                      served in a real deployment before the controlled testbed.
   The result points to the gate as the load-bearing compo­           A production consumer web service operated an au­
nent. Even the sign-only gate, which never sees the oracle            tonomous director-worker loop for about six weeks, 61
numbers, reached a mean final output of 110.0, similar to             cycles. Completion of each cycle was judged by the loop
the 113.0 of full feedback (per-repetition ranges 104 to              itself, on the basis of the conversation transcript and
122 versus 92 to 130, overlapping), and provided the same             analysis that cycle produced. That is, it was an in-band
structural guarantee of preserving the best state reached.            self-verdict, and the acceptance criterion was the produc­
The regression rate of the candidate stream (wasted-cycle             tion of a new analytical frame.
ratio) was also similar, 0.50 versus 0.56, so no evidence
                                                                         The consequence is isomorphic to our in-band-self arm.
was observed at this scale that oracle-number feedback
                                                                      All 57 evaluated cycles were accepted, while over the
materially steers candidate generation. What remains as
                                                                      same period every ground-truth signal outside the loop
the source of the in-band versus out-of-band gap is there­
                                                                      (arrival ledger, web analytics, append-only signup ledger,
fore not the information content of the feedback but what
                                                                      payment records, search indexing) was zero or flat. The
the gate is grounded in, consistent with the conclusion
                                                                      loop’s internal verdicts indicated progress; the state of
of Section 4.3. Since this is a 3-repetition pilot, we do
                                                                      the world indicated stagnation. More telling is that the
not claim the information effect is absent; establishing its
                                                                      loop did not stop even after recognizing the stagnation.
magnitude is deferred to the expanded repetitions of the
                                                                      Because the reward function rewarded analysis rather than
full measurement after the preregistration freeze.
                                                                      outcomes, even awareness of stagnation could be accepted
4.7 Anatomy of the Progress Mirage                                    as part of a new analysis. When the reward function was
   A single trajectory compresses the phenomenon (the                 moved to real-world outcomes and enforced by an out-of-
first in-band-self repetition, straight from the raw log).            band verifier, the behavior of the immediately following
In the first three cycles the agent made genuine improve­             cycles reversed from analysis to shipping. This single
ments: removing two pre-friction steps from the funnel                observation is not a controlled experiment and cannot
took conversions from 33 to 47 (+14); rewriting a passive             establish causality; we present it as motivation only. The
landing page with a benefit-led headline and a clear CTA              causal evidence is provided by the controlled measure­
took them to 95 (+48); removing a verification step took              ments of Sections 4.1 through 4.7.
them to 104 (+9). Up to this point the loop’s self-record
                                                                      4.9 Scope of the Results
and the world agreed. Over the next three cycles the
                                                                         The results of this section are a pilot: one open-ended
agent continued with conversion-optimization orthodoxy:
                                                                      task family and one boundary task, one fixed agent model,
social-proof copy above the CTA (-6), an inline email input
                                                                      one stronger judge model, and 3 repetitions per arm. The
on the landing page (-1), a named testimonial quote (-6).
                                                                      measurements reported in this paper were performed with
With each change the agent claimed it would raise conver­
                                                                      apparatus v2 — a strengthened judge receiving verdict
sion, and in-band-self accepted them all. The deployed
                                                                      history and diffs, per-run boundary proofs, and per-cycle
state slid from 104 to 91. In the loop’s self-record, six im­
                                                                      canary scans — and the mirage ordering across arms was
provements accumulated; in the world, three steps forward
                                                                      identical in earlier apparatus versions as well (apparatus
were followed by three steps back.
                                                                      history in the appendix). The direction of the effect is clear,
   This is the anatomy of the progress mirage. Even a ca­             but its magnitude is specific to this apparatus’s feature
pable frontier agent cannot tell, from inside the transcript,         weights (Section 6), and generalization to other domains,
whether its change raised or lowered a real-world metric.             models, and longer horizons is to be settled by the full
In the early phase, the large levers lie where plausibility           measurement after the preregistration freeze (multiple
and effect coincide, so the self-verdict is also correct. Once        models, a second oracle, the reward-function axis, sensi­
the levers are exhausted, plausibility and effect diverge,            tivity sweeps).
and an evaluator trapped in the transcript cannot see the



                                                                 15
When Do Agent Loops Mistake Stagnation for Progress?                                                                             preliminary draft



                                                                                  grounded in real-world outcomes, this premise fails. How
                                                                                  many users arrived, how many signups occurred, whether
                                                                                  a payment happened, whether a page was indexed — these
                                                                                  are not facts that exist inside the generator’s conversation.
                                                                                  They exist in the state of the world: databases, version con­
                                                                                  trol, web analytics, append-only ledgers. The transcript
Figure 4. Pilot measurement results (a real frontier agent, isolated              can contain the generator’s narration of that world, but it
containers, 3 repetitions per arm, apparatus v2). (a) Progress-mirage             cannot contain the world itself.
rate by evaluator arm. Bars are repetition means; error bars are min
and max. For in-band-self and the strengthened in-band-judge, a sub­
                                                                                     Self-evaluation bias arises in this gap. When the evalu­
stantial fraction of accepted cycles in fact had an oracle delta of zero          ator reads only the generator’s narration, the only signal
or below, whereas the out-of-band 0 is a definitional consequence of              available to it is how plausible the change is. And changes
the gate rule. (b) Trajectories of actual conversions in the deployed             produced by a powerful LLM are almost always plausible.
(last-accepted) state (repetition means). All three arms rise on the first
                                                                                  The archetype from Section 4: the strongest in-band-judge
cycle’s large lever; the self-verdict then keeps deploying plausible
regressions and erodes from the peak, the judge filters some regres­              accepted the addition of star ratings and user counts as
sions so erosion is gentler, and out-of-band deploys no regressions and           frictionless social proof, while actual conversion fell. The
                       preserves the state reached.                               judge can assess plausibility against conversion-optimiza­
                                                                                  tion orthodoxy, but what effect that orthodoxy actually
5 Discussion                                                                      has in the world is not in the transcript, so it cannot
                                                                                  know. That all 57 cycles in the motivating field observa­
   The measurements of Section 4 showed, under con­                               tion were accepted while real-world signals stayed at zero
trolled conditions, that the progress mirage is not an acci­                      (Section 4.8) is likewise not a chance malfunction but a
dent of a single service but structurally inherent to long-                       consequence of the same structure. An evaluator can only
running agent loops in which the generator evaluates its                          reward what it can see, and an evaluator that sees only the
own completion. This section interprets those results. We                         transcript can only see process.
first analyze why in-band evaluation is not sufficient (5.1),                        Note that the in-band judge’s errors are not one-direc­
present the core principle of out-of-band evaluation (5.2),                       tional. The judge rejects real-world improvements for the
and lay out the auxiliary design principles that support it                       same reason it accepts real-world regressions (Section
(5.3). We then generalize the relationship to the built-in                        4.5). In a terrain where plausibility diverges from effect,
agent primitives offered by contemporary platforms via                            there are genuine improvements that look implausible, and
the distinction of “loop plumbing vs. the reward brain”                           a transcript-only judge rejects them. The problem of in-
(5.4), and finally discuss when loop engineering is not                           band evaluation is thus not leniency but the absence of
justified — the conditions under which its costs exceed its                       discrimination — which is why this paper reports rejection
benefits (5.5).                                                                   errors (false rejections) alongside acceptance errors (the
5.1 Why In-Band Evaluators Are Not Sufficient                                     mirage).
   The root of the problem lies in what the evaluator reads.                         This is the lesson of HA1′s rejection. If the gap were a
An in-band evaluator issues ACCEPT/REJECT verdicts                                matter of judge quality, a stronger and more critical judge
based on the transcript the generator produced, within                            should close it. Yet in the measurements of Section 4, the
the same information channel as the generator. In the                             strongest in-band-judge’s mirage rate was effectively the
measurements of Section 4, more than half of the cycles                           same as in-band-self’s. No matter how critical the judge is
accepted by the two transcript-bound evaluators (the self-                        made, it cannot see ground truth that is not in the transcript.
verdict and the strongest judge) were in fact real-world                          For open-ended real-world objectives, then, the limit of
regressions, and both evaluators’ acceptance behavior was                         evaluation is lifted not by scaling the judge but by moving
effectively independent of the sign of the oracle delta                           the evaluator’s information channel to the world. This is
(Table 1 and the conditional acceptance rates of Section                          where our work departs from prior measurements that vary
4.3) — precisely because of this difference in channel.                           judge strength within the transcript channel, and it also
                                                                                  suggests a boundary condition for the scalable-oversight
  For in-band evaluation to be sufficient, one premise
                                                                                  family focused on building better judges (debate, recursive
must hold: the ground truth needed for the verdict must
                                                                                  reward modeling, weak-to-strong): there exist objective
be contained in the transcript. But when the reward is


                                                                             16
When Do Agent Loops Mistake Stagnation for Progress?                                                               preliminary draft



domains where the ceiling is the judge’s information                 Without this redefinition of the reward function, out-of-
channel, not the judge’s quality.                                    band access alone is meaningless: even if the evaluator
   Especially dangerous is that even when the generator              reads the world, nothing changes if it uses those readings
recognizes stagnation, in-band evaluation cannot convert             to reward process.
that recognition into a corrective signal (Section 4.8). Even           When these three properties operate together, the
awareness of stagnation is recorded in the transcript as             reward function finally becomes a real-world reward func­
part of a new analysis, and therefore becomes rewardable             tion. And crucially, the evaluator’s reject is not a mere
process too. As a result, the generator converges on mea­            refusal: it is recorded as a rejection artifact, an input
suring itself rather than producing outcomes — because               the next iteration is forced to read first. The rejection is
measurement always generates new transcript, it is the               thereby embedded in the starting condition of the next
most easily rewarded behavior under in-band reward. In               cycle, and the generator begins its next work confronting
short, in-band evaluation is sound only insofar as the               its own most recent failure. We interpret the shift from
reward is transcript-checkable; the moment the reward is             measuring to shipping in the cycles immediately after
grounded in the world, it becomes a device that mistakes             the intervention in the field observation of Section 4.8 as
process for outcome.                                                 arising because the evaluator read the world directly and
                                                                     returned the result as the forced input of the next boot. To
5.2 The Core Principle: An Out-of-Band Evaluator
                                                                     emphasize again, this is an interpretation of a single case,
    with Independent World Access
                                                                     not a proof of causality. The causal evidence is provided
   The core principle we propose is to separate the gener­
                                                                     by the measurements of Section 4, which implement the
ator (agent) from the evaluator and to grant the evaluator
                                                                     same feedback structure under controlled conditions.
independent world access rather than the transcript. Con­
cretely, the evaluator has the following three properties.           5.3 Auxiliary Design Principles
   First, the evaluator runs as a separately scheduled                  If the out-of-band evaluator is the core principle, several
process. It is not an appendage invoked inside the                   auxiliary principles prop it up so that it operates reliably.
generator’s conversation turns but a distinct executing              One point must be made clear up front: these auxiliary
entity on a schedule independent of the generator. This              principles are design notes derived from the field observa­
separation is the heart of out-of-band. Only when evalua­            tion of Section 4.8, and our controlled measurements did
tion happens outside the generator’s context does it remain          not validate them individually. What the measurements
uncontaminated by the generator’s narration.                         support is the out-of-band gate and rejection feedback
   Second, the evaluator does not trust the generator’s              only; the principles below should be read as unvalidated
self-judgment and does not read the transcript. It reads             prescriptions for making that gate run reliably in a real
ground-truth signal sources directly: databases, version             deployment.
control, web analytics, append-only ledgers. Moving what                Append-only state. If the loop is allowed to mutate
the evaluator reads from the generator’s output to the state         its own state in place, that state readily becomes a “lie
of the world is the only structural means of blocking self-          generator.” When the generator overwrites the previous
evaluation bias. When the evaluator looks at the world               cycle’s conclusions, neither the evaluator nor a human can
directly, no matter how plausible an analysis the generator          reconstruct after the fact what actually happened. This is
produces, the world’s zero reads as zero.                            why ground-truth signal sources such as arrival ledgers
   Third, the reward function must encode outcomes, not              and signup ledgers must be append-only. When only ap­
process. The evaluator’s verdict rule must be not “was a             pends are allowed and overwrites are forbidden, past zeros
new frame produced” but “did a real-world signal move,               remain past zeros, and the generator loses the room to re-
or is there at least verifiable evidence of traction that            narrate them as progress. For the out-of-band evaluator
could move it (a commit or a live URL).” The out-of-                 to obtain trustworthy signals, the signal sources must be
band gate of the measurement apparatus (accept only when             immutable.
the oracle delta is positive) and the verifier of the field             File-based handoff. Information transfer between gen­
observation in Section 4.8 (reject if the sum of real-world          erator and evaluator — above all the delivery of rejection
signals is zero and there is no valid traction evidence) are         artifacts — happens through external files, not the conver­
two instances implementing this rule in its simplest form.           sation context. When the evaluation’s output persists as
                                                                     a file and the next boot is forced to read that file, the


                                                                17
When Do Agent Loops Mistake Stagnation for Progress?                                                              preliminary draft



rejection signal does not depend on the volatility of the           are states of the world, and no matter how precisely one
generator’s context window. This is a simple mechanism              adjudicates the transcript, one cannot reach that world. For
that keeps evaluation and generation loosely coupled                such goals, in-band evaluation is structurally insufficient,
while guaranteeing that a rejection reaches the next cycle.         and out-of-band evaluation that reads the world directly
   Frame-adversarial review. If the generator thinks only           is required. This is why our contribution complements
in directions that agree with its own assumptions, new              platform primitives rather than replacing them.
frames become nothing more than tools for rationalizing                Generalizing this distinction yields “loop plumbing
self-evaluation bias more elaborately. Preventing this re­          vs. the reward brain” (Figure 3). Loop plumbing is the
quires a review step that forces the generator to attack            mechanical part that keeps an autonomous loop turning:
its own assumptions. In the field observation of Section            the scheduler, pacing between cycles, session recovery.
4.8, the operating rule that forced every cycle to read             The reward brain is the part that decides what counts
the real-world arrival ledger first and compute how many            as progress: the domain-grounded evaluator. The central
days the metrics had been flat (days-flat) can be seen as a         claim is this: loop plumbing can be delegated to platform
frame-adversarial device that made the generator confront           primitives, but the reward brain cannot. Plumbing gener­
falsifiable facts before presenting its “things are going           alizes independent of domain, whereas the reward brain
well” self-narrative.                                               requires domain knowledge of which world signals con­
   Self-healing scheduling. The out-of-band evaluator               stitute real progress for that service. The platform can turn
must keep running independently of the generator, and               the loop, but the platform cannot know what the loop
stably — because the moment the evaluation process dies,            should be turning toward.
the loop regresses to a self-grading state. The evaluator’s         5.5 Costs and Limits: When Loop Engineering Is
scheduling must therefore be designed to recover on its                 Not Justified
own (self-healing) even when sessions drop or processes
                                                                       Out-of-band evaluation is not free. Whether to adopt
halt. The evaluator’s availability is not an accessory fea­
                                                                    it depends on comparing costs and benefits, and in the
ture; it is the integrity of the reward function itself.
                                                                    following cases loop engineering is not justified.
5.4 Relation to Platform Built-in Primitives: Loop                     The cost of building and maintaining the out-of-
    Plumbing vs. the Reward Brain                                   band validator. Creating a separate evaluation process,
   Contemporary agent platforms provide several built-in            wiring up independent access to ground-truth signal
primitives for composing autonomous loops — represen­               sources, and keeping it running in a self-healing manner
tatively, a “loop” feature in which the model itself judges         carry real engineering cost. If the work finishes quickly,
the result after every turn, and a “goal” feature in which          is one-off in nature, or has transcript-checkable comple­
the model evaluates whether the goal has been achieved.             tion, this overhead exceeds the benefit. Loop engineering
The evaluation style these primitives adopt is essentially          is justified for long-running autonomous loops — cases
in-band: when a turn ends, a single model reads that turn’s         where evaluation can go cumulatively wrong and waste
transcript and judges completion.                                   resources over a long period.
   We do not claim this in-band style is wrong. On the                 The service-specificity of the reward function. The
contrary, it has an appropriate scope of application. When          reward brain is bound to its domain (Section 5.4). Which
the task is bounded and completion is transcript-checkable          signals constitute real progress differs from service to
— whether output of a specific format was generated,                service, so one service’s reward function cannot be trans­
whether all required items were mentioned, whether the              planted to another as-is. This means out-of-band evalua­
code compiles — the answer is contained in the transcript.          tion is not a reusable generic component but a part that
For such tasks, a model reading the transcript and judging          must be designed anew for each service. In early stages
is sufficient, and building a separate out-of-band evaluator        where the domain signal is unclear or not yet defined,
is unnecessary overhead.                                            what to reward is itself undecided, and fixing the reward
   The problem is when the goal is an open-ended real-              function may be premature.
world objective. As discussed in Section 5.1, in that case            The risk of over-constraint. Narrowing the reward
the ground truth needed for the verdict is not in the tran­         function to outcomes narrows the generator’s action space
script. Organic user growth, signups, payments, indexing            by the same amount. There are two concrete instances. In



                                                               18
When Do Agent Loops Mistake Stagnation for Progress?                                                                      preliminary draft



the field observation of Section 4.8, the operating mode                     Loop plumbing                        Reward brain
triggered after stagnation crossed its threshold blocked cy­          delegable to platform primitives       domain-bound, kept custom
cles that only analyzed and cycles that only touched policy
wording. And the out-of-band gate of our measurement                  session   resurrection,   interval     real-world reward function
                                                                                   pacing
(accept only when the delta is positive), as seen in Section
                                                                                                           ground-truth-reading   external
4.5, eliminates the room for judgment that seems reason­               repeated execution, scheduling                  verifier
able in real-world terms, and also rejects all valid steady-
state edits with delta zero (refactoring, maintenance edits).          platform loop / goal primitives     append-only ledgers, frame-ad­
This is the right prescription in a stagnation regime, but                   (in-band evaluator)                  versarial review

applying the same constraint indiscriminately can also               Figure 3. The distinction between loop plumbing and the reward brain.
block legitimately needed exploratory analysis or valley-            Plumbing such as scheduling, pacing, and session resurrection can be
                                                                     delegated to a platform’s built-in loop/goal primitives, but the real-
crossing search (paths that accept temporary regress). Not
                                                                     world reward function and the ground-truth-reading external verifier
all analysis is a symptom of self-evaluation bias; some              are domain-bound and cannot be delegated. The evaluator of the
analysis is genuine groundwork for the next action. If               built-in primitives is in-band (it sees the conversation), whereas the
the reward function defines outcomes too narrowly and                open-ended real-world goals treated in this paper require out-of-band
too short-term, the generator can be over-constrained into                                         evaluation.

chasing only measurable short-term signals at the expense
of long-term value. Designs that switch constraints on and
                                                                     6 Threats to Validity
off by situation — e.g., threshold-based mode switching
that activates an outcome-forcing mode only when days                   This section makes explicit the threats to the validity of
of stagnation cross a threshold — are therefore important.           this work. Because the core evidence is the controlled pilot
The goal of out-of-band evaluation is not to bind the                measurement and the field observation serves only as mo­
generator but to force the generator to face the fact when           tivation, the weight of the threats shifts from the limits of
the world has stopped moving.                                        causal claims to the construct validity of the measurement
   Finally, we restate the status of the evidence. The causal        apparatus and the scope of the pilot. We do not hide these
evidence of this work is the controlled pilot measurement            threats; alongside each, we describe how the preregistered
of Section 4; the field observation of Section 4.8 is an             full measurement (PREREGISTRATION.md) is designed
anonymized single case providing motivation; and the                 to resolve it further.
auxiliary principles of Section 5.3 are unvalidated design           6.1 Construct Validity: Does the Oracle Capture
notes derived from that field case. Whether the out-of-                  Real Value?
band evaluation architecture proposed here works identi­                This is the largest threat to this work. The
cally in other domains, with other models, over longer time          measurement’s ground truth is the conversion count pro­
horizons, and whether each auxiliary principle is in fact            duced by a synthetic user simulator — a weighted logistic
a necessary condition, remain questions for the preregis­            over four properties of the deployed artifact (CTA pres­
tered full measurement and follow-up research.                       ence, payload size, number of funnel steps, copy length).
                                                                     The foreseeable objection runs: if the simulator was
                                                                     designed so that plausibility and effect diverge, isn’t the
                                                                     transcript judge’s defeat a built-in conclusion?
                                                                        Our defense is twofold. First, independence. The
                                                                     oracle’s values are produced by an independent process
                                                                     from the physical properties of the deployed artifact, not
                                                                     from the agent’s narrative, and the existence of the in-
                                                                     band vs. out-of-band gap derives from this independence,
                                                                     not from any particular weights. Second, the divergence
                                                                     between plausibility and effect is not an artifact of the sim­
                                                                     ulator but a documented property of real-world conversion
                                                                     optimization. The large-scale online controlled experi­
                                                                     ment literature has repeatedly demonstrated that a majority


                                                                19
When Do Agent Loops Mistake Stagnation for Progress?                                                                preliminary draft



of ideas experts judge plausible (around two-thirds by                the evaluator. Two confounds remain. First, agent stochas­
some reports) fail to move metrics or actively hurt them in           ticity: each arm’s trajectory is an independent agent run,
real experiments [Kohavi et al., 2009], [Kohavi, Tang and             so the arms do not share identical rollouts; this is mitigated
Xu, 2020]. The very reason practitioners run A/B tests is             by multiple repetitions. Second, the information content of
that plausibility does not reliably predict effect. Our simu­         the feedback: each arm’s gate verdict returns to the loop
lator reproduces that sign structure (a majority of plausible         as a different feedback string, and in particular the out-of-
decorative edits being neutral or negative on the metric) in          band feedback contains the post-gate oracle scalars (the
a simple form.                                                        delta and current value). The out-of-band treatment is thus
   Even so, the existence of the gap and its magnitude must           not a pure gate arrangement but the combination of a gate
be distinguished. The absolute level of the mirage rate this          and ground-truth feedback, and indeed a second-order ef­
pilot reports is specific to this simulator’s feature weights;        fect is observed in which the agent’s regression-candidate
with different weights (e.g., giving social proof a positive          generation rate falls in the out-of-band arm. This combina­
channel), the agent’s regression-generation rate and the              tion is a deliberate treatment that faithfully models what a
magnitude of the mirage would also change. Our claim is               real deployment’s out-of-band evaluator actually provides
confined to the existence and direction of the gap; we do             (rejection rationales). This pilot additionally ran a sign-
not claim generalization of its magnitude. For reference,             only variant that returns only the sign, providing first data
the mirage ordering across arms was invariant across the              for this decomposition (Section 4.6): a gate that never sees
three versions of the measurement apparatus (before the               the oracle numbers largely preserved real-world output, so
gate rollback was introduced, before CTA-detection rein­              the gate was observed to be the load-bearing component;
forcement, and final; apparatus history in the appendix).             but at a scale of 3 repetitions, the precise magnitude of the
The preregistered full measurement includes a sensitivity             information effect is to be settled by the expanded repeti­
sweep over feature weights (including a variant that puts             tions of the preregistered full measurement.
the correlation between plausibility and effect on a dial)            6.3 Limits of Ungameability
and a second oracle type (server-side event logs) that                   Oracle isolation is proven by measurement, not as­
reduces dependence on the simulator.                                  sumed. In the measurements reported here, a boundary
   Finally, we state the limit that the oracle is a measure­          proof was performed at the start of every run (each
ment channel, not a value function. Because this oracle               combination of arm and repetition), agent-side output and
counts only conversions, it rewards as a conversion                   artifacts were scanned every cycle for the oracle canary
increase even a change that, say, removes a confirmation              string, and the apparatus was wired to abort measurement
step and inflates unverified signups. Indeed the log con­             on any canary occurrence (zero occurrences). But this
tains a case in which the judge rejected such a change for a          proof covers network paths and filesystem access; it does
reason sound in real-world terms (unverified-signup infla­            not rule out every other bypass. We state the remaining
tion), yet by the oracle’s standard it was tallied as a false         surfaces. (a) File-layer attacks such as symlinks through
rejection of a real improvement (Section 4.5). That out-of-           the shared artifact volume (this can be narrowed by real-
band evaluation tied to a narrow metric can reproduce the             path verification on the oracle-side read). (b) Because
surrogate-metric problem one level up is an honest limit              the in-band-judge input includes the raw text of files
of this design; in real deployments, the construct validity           the agent wrote, an adversarial agent could plant verdict
of the oracle metric itself (quality-adjusted metrics, plural         instructions in a file — prompt injection (not observed in
signals) becomes a separate design problem.                           this measurement, and under our threat model the agent
6.2 Internal Validity: Is the Evaluator Channel                       was not induced to attack the evaluator). (c) Because
    Really the Only Difference?                                       the out-of-band feedback exposes one oracle scalar per
   The pilot holds the agent model, tool surface, task, and           cycle, over a very long horizon the feature weights could
cycle budget identical across all arms and swaps only                 be reverse-engineered from numeric feedback alone. That
the evaluator gating the loop, so the measured effect is              is, the apparatus’s guarantee is unfakeability (the agent
attributable to the evaluator’s information-channel type.             cannot manufacture oracle values by narrative), not long-
The rollback rule, under which rejected cycles are not                horizon unoptimizability. Also, while the agent does not
promoted to deployment, makes the gate actually govern                know the simulator’s feature set and weights in advance,
state, causally linking the real-outcome measurements to              the narrowness of a four-feature surface is a simplification


                                                                 20
When Do Agent Loops Mistake Stagnation for Progress?                                                               preliminary draft



that is safe only at pilot scale. The full measurement nar­          motivation is anonymized, and the original deployment
rows this surface with feature expansion and adversarial             itself is not reproducible.
red-team scenarios.
                                                                     6.7 Cost and Over-Constraint Risk
6.4 External Validity: The Scope of the Pilot                           Out-of-band evaluation carries cost: additional oracle
   This measurement is a pilot with one open-ended task              queries and infrastructure. In the testbed, oracle queries are
family, one fixed agent model, one stronger judge model,             cheap, but the possibility that in real deployments the cost
and 3 repetitions per arm. Whether the same effect holds in          offsets the benefit (adversarial hypothesis HA2) was not
other domains, with less capable models, and over longer             tested in this pilot and is tested by the budget-normalized
horizons is beyond this pilot’s scope. The synthetic user            analysis of the preregistered full measurement. Moreover,
is an approximation of real users; in particular, this oracle        if the reward function is tied only to outcome metrics, it
responds instantly and without noise. Real-world metrics             can over-constrain the agent’s exploration and miss better
are noisy and delayed, and under those conditions a simple           solutions (Section 5.5). This over-constraint risk is miti­
gate that accepts only positive deltas can reject true im­           gated by designs that tie the reward function to outcomes
provements for lack of statistical power. Gate design under          while leaving paths open, and by threshold-based mode
noisy oracles (e.g., interval-estimate-based acceptance) is          switching, but the right point of balance is beyond the
an extension axis of the full measurement. Full resolution           scope of this work.
of external validity is deferred to replication on a real
service.                                                             7 Conclusion
6.5 Conclusion Validity and Prevention of Selective
    Reporting                                                           When a long-running autonomous agent loop grades its
                                                                     own work, self-evaluation bias makes it mistake analysis
   The per-cell repetition count of the pilot is small. The
                                                                     for progress: the loop reports advancement while real-
intervals in Table 1 are bootstrap percentile intervals over
                                                                     world outcomes stagnate. This paper named this failure
3 trajectories — at this sample size, closer to observed
                                                                     mode the progress mirage and diagnosed its cause as the
ranges than calibrated 95 percent confidence intervals.
                                                                     in-band structure that traps the evaluator inside the con­
Definitive conclusions about effect size and durability are
                                                                     versation transcript.
deferred to the full measurement after the preregistration
freeze. Analysis is performed by standard-library scripts               As the remedy, we proposed an architecture that sepa­
over raw cycle logs with no human discretion, and every              rates the generator from the evaluator and places the evalu­
registered dependent variable is reported even when the              ator out-of-band. The evaluator runs as a separate process,
result is unfavorable to our hypotheses or uninformative             accesses real-world ground truth directly rather than the
(e.g., cycles to first real outcome identical across arms)           conversation, enforces a real-world reward function, and,
(Section 4.1). Definitional differences between the regis­           when the function is not satisfied, leaves a rejection arti­
tration document and the paper are not concealed but                 fact that the next iteration is forced to confront. Append-
disclosed as amendments, with numbers reported under                 only state, file-based handoff, frame-adversarial review,
both definitions (Section 4.1).                                      and a self-healing scheduler were presented alongside as
                                                                     auxiliary design notes derived from field observation; their
6.6 Reproducibility
                                                                     individual validation is future work.
   The analysis is fully reproducible: applying the analy­
                                                                        We tested this diagnosis and remedy with a controlled
sis scripts to the released raw cycle logs recomputes
                                                                     pilot measurement. In a testbed that holds the agent and
every number in the paper. The measurement trajectories
                                                                     tool surface fixed and swaps only the information-channel
themselves include non-deterministic LLM calls and so
                                                                     type of the evaluator gating the loop, we enforced a world-
differ across executions; what is fixed is the simulator’s
                                                                     state oracle that is ungameable in principle via container
cohort randomness. Within a repetition the same seed is
                                                                     and network isolation and proved that isolation by per-
used across cycles (common random numbers), so the
                                                                     run measurement. Running a real frontier agent repeatedly
conversion count is a monotone deterministic function of
                                                                     under three evaluator arrangements, the in-band self-ver­
artifact features and the sign of a delta cannot be flipped
                                                                     dict that sees only the transcript accepted as progress a
by sampling noise. The testbed is released together with
                                                                     substantial fraction of cycles in which real-world metrics
its container configuration; the field observation used as
                                                                     stagnated or regressed, whereas the out-of-band evalua­


                                                                21
When Do Agent Loops Mistake Stagnation for Progress?                                                                       preliminary draft



tion that queries the world-state oracle did not; and even               [Bai et al. 2022]      Y. Bai et al., “Constitutional AI:
the strongest in-band judge, reading the transcript criti­                                      Harmlessness from AI Feedback,”
                                                                                                arXiv:2212.08073, 2022.
cally, failed to close the gap. The cause of the gap is not the          [Baker et al. 2025]    B. Baker, J. Huizinga, L. Gao, Z. Dou, M. Y.
evaluator’s quality but what the evaluator is grounded in.                                      Guan, A. Madry, W. Zaremba, J. Pachocki,
    The practical implication is summarized by the dis­                                         and D. Farhi, “Monitoring Reasoning Mod­
                                                                                                els for Misbehavior and the Risks of Pro­
tinction between loop plumbing and the reward brain.                                            moting Obfuscation,” arXiv:2503.11926,
Plumbing — scheduling, pacing, session revival — can be                                         2025.
delegated to the platform’s built-in loop/goal primitives;               [Burns et al. 2023]    C. Burns et al., “Weak-to-Strong General­
                                                                                                ization: Eliciting Strong Capabilities with
the reward brain grounded in the real world — the out-of-
                                                                                                Weak Supervision,” arXiv:2312.09390,
band evaluator with access to ground truth and the domain                                       2023.
reward function — cannot. Because the evaluator of the                   [Çağatan and Zhao Ö. V. Çağatan and X. Zhao, “Reward Hack­
built-in primitives is in-band, looking at the conversation,             2026]                  ing in Language Model Agents: Revisiting
                                                                                                AI Safety Gridworlds,” arXiv:2606.15385,
it suffices for well-bounded transcript-verifiable tasks but
                                                                                                2026.
is structurally insufficient for open-ended real-world ob­               [Caldwell et al. 2026] S. Caldwell, M. Harley, A. Dawson, M.
jectives whose success signal lies outside the transcript.                                      Kouremetis, V. Abruzzo, and W. Pearce,
                                                                                                “ScopeJudge: Cost-Aware Pre-Execution
   This measurement is a pilot on one task family and
                                                                                                Gating for Offensive Security Agents,”
one agent model, and the motivating field observation                                           arXiv:2607.07774, 2026.
is an anonymized single-deployment observation, not                      [Christiano et al. P. Christiano, J. Leike, T. B. Brown, M.
causal proof. Future work is to freeze the preregistration               2017]                  Martic, S. Legg, and D. Amodei, “Deep Re­
                                                                                                inforcement Learning from Human Prefer­
(PREREGISTRATION.md) and then extend the measure­                                               ences,” in Advances in Neural Information
ment with multiple models, two kinds of world-state                                             Processing Systems (NeurIPS), 2017.
oracle, and a transcript-verifiable contrast task testing the            [Flynt 2026]           J. Flynt, “GroundEval: A Deterministic
boundary hypothesis, to settle the generalization scope                                         Replacement for LLM-as-Judge in State­
                                                                                                ful Agent Evaluation,” arXiv:2606.22737,
and durability of the effect, and to quantify the cost-                                         2026.
benefit of out-of-band evaluation. Nevertheless, this pilot              [Gabor et al. 2025]    J. Gabor, J. Lynch, and J. Rosenfeld, “Evil­
puts one fact on the record by measurement. As we attach                                        Genie: A Reward Hacking Benchmark,”
                                                                                                arXiv:2511.21654, 2025.
autonomous agents to ever more open-ended real-world
                                                                         [Gao et al. 2023]      L. Gao, J. Schulman, and J. Hilton, “Scal­
goals, grounding the evaluator in the world rather than the                                     ing Laws for Reward Model Overoptimiza­
transcript is not a choice but a structural requirement for                                     tion,” in Proc. Int. Conf. Machine Learning
preventing the progress mirage.                                                                 (ICML), 2023.
                                                                         [Huang et al. 2024] J. Huang et al., “Large Language Models
                                                                                                Cannot Self-Correct Reasoning Yet,” in
References                                                                                      Proc. Int. Conf. Learning Representations
                                                                                                (ICLR), 2024.
[Advani 2026]        L. Advani, “From Confident Closing to               [Irving et al. 2018]   G. Irving, P. Christiano, and D. Amodei,
                     Silent Failure: Characterizing False Suc­                                  “AI Safety via Debate,” arXiv:1805.00899,
                     cess in LLM Agents,” arXiv:2606.09863,                                     2018.
                     2026.                                               [Jimenez et al. 2024] C. E. Jimenez et al., “SWE-bench: Can
[Amodei et al. 2016] D. Amodei, C. Olah, J. Steinhardt, P. Chris­                               Language Models Resolve Real-World
                     tiano, J. Schulman, and D. Mané, “Concrete                                 GitHub Issues?,” in Proc. Int. Conf. Learn­
                     Problems in AI Safety,” arXiv:1606.06565,                                  ing Representations (ICLR), 2024.
                     2016.                                               [Kohavi et al. 2009] R. Kohavi, R. Longbotham, D. Sommer­
[Anthropic 2024]     Anthropic, “Building Effective AI Agents,”                                 field, and R. M. Henne, “Controlled Exper­
                     Anthropic Engineering Blog, 2024.                                          iments on the Web: Survey and Practical
                                                                                                Guide,” Data Mining and Knowledge Dis­
[Anthropic 2025]     Anthropic, “Effective Harnesses for Long-
                                                                                                covery, vol. 18, no. 1, pp. 140–181, 2009.
                     Running Agents,” Anthropic Engineering
                                                                         [Kohavi, Tang and R. Kohavi, D. Tang, and Y. Xu, Trust­
                     Blog, 2025.
                                                                         Xu 2020]               worthy Online Controlled Experiments: A
[Anthropic 2025b]    Anthropic, “Agent Harness Design Notes,”
                                                                                                Practical Guide to A/B Testing. Cambridge
                     Anthropic Engineering Blog, 2025.
                                                                                                University Press, 2020.
[Atinafu and Cohen Y. Atinafu and R. Cohen, “Reward­
                                                                         [Krakovna et al. V. Krakovna et al., “Specification Gaming:
2026]                HackingAgents: Benchmarking Evalua­
                                                                         2020]                  The Flip Side of AI Ingenuity,” DeepMind,
                     tion Integrity for LLM ML-Engineering
                                                                                                2020.
                     Agents,” arXiv:2603.11337, 2026.


                                                                    22
When Do Agent Loops Mistake Stagnation for Progress?                                                                          preliminary draft


[Leike et al. 2018]    J. Leike, D. Krueger, T. Everitt, M. Mar­         [Uesato et al. 2022]   J. Uesato et al., “Solving Math Word Prob­
                       tic, V. Maini, and S. Legg, “Scalable                                    lems with Process- and Outcome-Based
                       Agent Alignment via Reward Modeling:                                     Feedback,” arXiv:2211.14275, 2022.
                       A Research Direction,” arXiv:1811.07871,          [Wang et al. 2026]     B. Wang et al., “The Verification Horizon:
                       2018.                                                                    No Silver Bullet for Coding Agent Re­
[Li et al. 2026]       X. Li, W. Yan, Y. Wu, P. Liang, M. Yuan,                                 wards,” arXiv:2606.26300, 2026.
                       J. Liu, and J. Yang, “Early Diagnosis of          [Xie 2026]             H. Xie, “Forage V2: Knowledge Evolution
                       Wasted Computation in Multi-Agent LLM                                    and Transfer in Autonomous Agent Organi­
                       Systems via Failure-Aware Observability,”                                zations,” arXiv:2604.19837, 2026.
                       arXiv:2606.01365, 2026.                           [Yang et al. 2024]     J. Yang et al., “SWE-agent: Agent-
[Lightman et al. H. Lightman et al., “Let’s Verify Step by                                      Computer Interfaces Enable Automated
2023]                  Step,” in Proc. Int. Conf. Learning Repre­                               Software Engineering,” in Advances in
                       sentations (ICLR), 2024 (arXiv 2023).                                    Neural Information Processing Systems
[Lù et al. 2025]       X. H. Lù et al., “AgentRewardBench:                                      (NeurIPS), 2024.
                       Evaluating Automatic Evaluations of Web           [Yao et al. 2023]      S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran,
                       Agent Trajectories,” arXiv:2504.08942,                                   K. Narasimhan, and Y. Cao, “ReAct: Syn­
                       2025.                                                                    ergizing Reasoning and Acting in Language
[Ma et al. 2026]       X. Ma, C. Zheng, J. Qiu, J. Hong, Y. Yao,                                Models,” in Proc. Int. Conf. Learning Rep­
                       X. Qu, J. Yin, X. Lou, J. Wang, W. Liu, W.                               resentations (ICLR), 2023.
                       Zhang, Z. Zhang, and H. Zhao, “Retrospec­         [Yao et al. 2024]      S. Yao, N. Shinn, P. Razavi, and K.
                       tive Progress-Aware Self-Refinement for                                  Narasimhan, “τ-bench: A Benchmark for
                       LLM Agent Training,” arXiv:2606.14302,                                   Tool-Agent-User Interaction in Real-World
                       2026.                                                                    Domains,” arXiv:2406.12045, 2024.
[Madaan et al. 2023] A. Madaan et al., “Self-Refine: Iterative           [Zhao et al. 2026]     B. Zhao, D. Srikanth, Y. Wu, and Z.
                       Refinement with Self-Feedback,” in Ad­                                   Jiang, “SpecBench: Measuring Reward
                       vances in Neural Information Processing                                  Hacking in Long-Horizon Coding Agents,”
                       Systems (NeurIPS), 2023.                                                 arXiv:2605.21384, 2026.
[Manheim           and D. Manheim and S. Garrabrant, “Cate­              [Zheng et al. 2023]    L. Zheng et al., “Judging LLM-as-a-Judge
Garrabrant 2018]       gorizing Variants of Goodhart’s Law,”                                    with MT-Bench and Chatbot Arena,” in Ad­
                       arXiv:1803.04585, 2018.                                                  vances in Neural Information Processing
[Ouyang et al. 2022] L. Ouyang et al., “Training Language Mod­                                  Systems (NeurIPS) Datasets and Bench­
                       els to Follow Instructions with Human                                    marks, 2023.
                       Feedback,” in Advances in Neural Informa­         Industry/engineering sources (agent harness design, etc.) will carry
                       tion Processing Systems (NeurIPS), 2022.          URLs and access dates in the submission version. Citations will be
[Pan et al. 2022]      A. Pan, K. Bhatia, and J. Steinhardt, “The        converted to the target venue’s bibliography format at submission time.
                       Effects of Reward Misspecification: Map­
                       ping and Mitigating Misaligned Models,”
                       in Proc. Int. Conf. Learning Representa­
                       tions (ICLR), 2022.
[Pan et al. 2024]      J. Pan, H. He, S. R. Bowman, and S. Feng,
                       “Spontaneous Reward Hacking in Itera­
                       tive Self-Refinement,” arXiv:2407.04549,
                       2024.
[Panickssery et al. A. Panickssery, S. R. Bowman, and S.
2024]                  Feng, “LLM Evaluators Recognize and Fa­
                       vor Their Own Generations,” in Advances
                       in Neural Information Processing Systems
                       (NeurIPS), 2024.
[Shinn et al. 2023]    N. Shinn, F. Cassano, E. Berman, A.
                       Gopinath, K. Narasimhan, and S. Yao,
                       “Reflexion: Language Agents with Verbal
                       Reinforcement Learning,” in Advances in
                       Neural Information Processing Systems
                       (NeurIPS), 2023.
[Skalse et al. 2022] J. Skalse, N. H. R. Howe, D. Krashenin­
                       nikov, and D. Krueger, “Defining and Char­
                       acterizing Reward Hacking,” in Advances
                       in Neural Information Processing Systems
                       (NeurIPS), 2022.




                                                                    23
