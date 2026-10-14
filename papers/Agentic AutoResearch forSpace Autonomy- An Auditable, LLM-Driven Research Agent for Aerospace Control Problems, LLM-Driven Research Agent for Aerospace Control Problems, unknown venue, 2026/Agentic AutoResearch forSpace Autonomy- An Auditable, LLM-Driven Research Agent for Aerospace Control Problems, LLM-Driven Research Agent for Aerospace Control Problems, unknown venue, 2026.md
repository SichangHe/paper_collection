                                           Agentic AutoResearch for Space Autonomy: An Auditable,
                                          LLM-Driven Research Agent for Aerospace Control Problems

                                                                                      Amit Jain∗ and Richard Linares†
                                                                         Massachusetts Institute of Technology, Cambridge, MA, 02139

                                                      Spacecraft guidance, navigation, and control functions are increasingly realized as learned
                                                  policies distilled from expert solvers. Developing such a policy is itself a research process:
                                                  an investigator selects an architecture and hyperparameters, runs experiments, and must
                                                  determine whether an apparent improvement is genuine or merely seed noise. This paper
arXiv:2606.20394v1 [cs.RO] 18 Jun 2026




                                                  presents AutoResearch, a framework in which a large language model autonomously drives that
                                                  loop for aerospace control problems, coupled with a credibility layer, built into the loop, that
                                                  certifies each reported result against the problem’s own measured seed noise. The language
                                                  model serves only as the offline research agent that develops the control policy; the trained
                                                  policy it produces is then deployed onboard the spacecraft, while the model itself never operates
                                                  the vehicle. At each iteration the agent reads a plain-language problem description and the
                                                  run history, proposes a single edit to the training script, executes it, and logs the outcome.
                                                  No reported result is credited until it passes the same three checks: measured per-problem
                                                  seed noise, reseeded verification of the best configuration, and leave-one-out pruning of the
                                                  agent’s edits. The same loop is applied, unchanged, to two aerospace control problems: a
                                                  Clohessy–Wiltshire relative rendezvous and a safety-constrained collision-avoidance docking
                                                  past a keep-out zone, each calibrated against a known optimal-control benchmark. In both,
                                                  the audited policy clears the measured seed noise by many standard deviations; an undirected
                                                  search over the same parameters does not. On the docking problem the gap becomes categorical:
                                                  undirected search yields no feasible policy, while the learned policy stays outside the keep-out
                                                  zone on every seed. The contribution is the autonomous, auditable research process itself: a
                                                  reusable means of developing learned control policies and certifying that their reported gains
                                                  are genuine.


                                                                                                   I. Introduction
                                              Spacecraft autonomy increasingly depends on learned components. Guidance, navigation, and control functions that
                                         were once specified entirely by hand, among them rendezvous and proximity-operations planners, and powered-descent
                                         guidance laws, are now frequently realized as policies trained from data or distilled from expert solvers [1]. Building such
                                         a component is an iterative research process in its own right: the investigator picks an architecture and hyperparameters,
                                         runs experiments, diagnoses failure modes, and decides whether an apparent improvement is a real gain or just
                                         seed-to-seed variation. The loop is slow and labor-intensive, and when it is run informally it invites over-claiming,
                                         since a single favorable run is easily mistaken for a robust result, a failure mode well documented across machine
                                         learning [2, 3].
                                              The recent emergence of large language models (LLMs) that can read source code, reason about it, and act on
                                         it raises a concrete question for the aerospace community: can the research loop itself be automated, and can it be
                                         automated in a way that remains transparent, reproducible, and honest? Recent LLM-driven research agents show that
                                         autonomous experimentation is feasible [4, 5], and LLMs have been used directly as optimizers [6]. But speed without
                                         statistical discipline is what the reproducibility literature warns against: an agent that runs experiments faster only
                                         compounds the risk of mistaking noise for progress.
                                              This paper takes up that question for aerospace control problems and presents AutoResearch, an agentic framework in
                                         which an LLM autonomously proposes, executes, and analyzes machine-learning experiments, paired with a credibility
                                         layer that lives inside the loop rather than being bolted on afterward. Throughout, the LLM serves strictly as the research
                                         agent that drives experimentation: it reads run histories, forms hypotheses, and selects the next configuration to try. It
                                            ∗ Postdoctoral Associate, Department of Aeronautics and Astronautics.
                                            † Associate Professor, Department of Aeronautics and Astronautics.




                                                                                                                 1
operates offline, within the research loop, and produces the trained control policy that ultimately flies the spacecraft.
The autonomy under study is thus that of the research process itself.

Contributions. This paper makes three contributions.
    1) A reusable framework for agentic experimentation. The framework defines a family contract: a plain-language
        description, one editable training script with a delimited hyperparameter region, a single structured metric, and
        an append-only run log. One LLM-driven agent loop then applies unchanged across aerospace problems whose
        physics differ sharply (Sec. III).
    2) A credibility layer that makes autonomous results trustworthy. The credibility layer integrates measured
        per-problem seed noise, reseeded verification of the agent’s best configuration, and leave-one-out pruning of its
        individual edits, applied uniformly so that a real improvement is separated from seed luck and the contribution of
        each edit is made explicit (Sec. III.D).
    3) Audited results on two aerospace control problems. The same loop runs, unchanged, on a Clohessy–Wiltshire
        relative rendezvous and a safety-constrained collision-avoidance docking past a keep-out zone, each a calibrated
        problem whose optimal solver fixes a best-achievable benchmark and whose fixed baseline configuration sets the
        scale of measured noise. In both, the audited policy clears that measured seed noise by many standard deviations;
        a parallel undirected search over the same parameters trails it, and does so decisively on the docking problem,
        where it produces no feasible policy at all while the learned policy holds the hard safety constraint and stays
        clear of the keep-out zone on every seed. Leave-one-out pruning then shows which of the agent’s edits actually
        carry each result. The novelty is the autonomous research loop and its audit taken together, the process that both
        produces the policy and certifies it (Secs. IV–V).
    The remainder of the paper reviews related work (Sec. II), describes the framework and its credibility layer (Sec. III),
states the two demonstration problems and reports their audited results (Secs. IV–V), and closes with limitations and
future work (Sec. VI).


                                                  II. Related Work
    This work draws on several lines of research and is best understood by how it departs from each. The first is the
use of large language models (LLMs) as autonomous agents that conduct, rather than merely assist, research. The AI
Scientist [4] closes the full loop of idea generation, experimentation, analysis, and writing for small machine-learning
studies, and FunSearch [5] pairs an LLM with an automated evaluator and evolutionary search to discover programs
that improve on known mathematical constructions. A closely related thread treats the LLM itself as the optimization
operator: OPRO [6] states the optimization task in natural language and has the model propose successively better
solutions from a prompt of prior trials and their scores, while OptFormer [7] learns a transformer-based universal
hyperparameter optimizer from large tuning corpora. These systems establish that an LLM can drive an end-to-end
search or discovery loop. What they do not settle is whether a reported improvement is statistically real or merely a
favorable random seed, the question the credibility layer is built to answer.
    A fast-growing literature now builds LLM agents that autonomously run machine-learning experiments rather than
merely optimize a scalar. MLAgentBench [8] casts ML experimentation as an agent task of reading and writing code,
executing it, and iterating on a metric; AIDE [9] frames ML engineering as a tree search over candidate programs;
AutoML-Agent [10] orchestrates a multi-agent pipeline from data to deployment; and the MLE-bench benchmark [11]
measures such agents against human Kaggle leaderboards. Closer to the hyperparameter-tuning core of the present loop,
AgentHPO [12] has an LLM propose configurations, read the resulting trials, and iterate, an agentic successor to OPRO.
Most relevant in spirit is Curie [13], which likewise seeks rigor in autonomous LLM experimentation, but enforces it
procedurally, through experimental-setup validation, controlled design, and reproducible, re-runnable workflows. The
credibility layer here is complementary, and statistical where Curie is procedural: it denominates each reported number
in a measured per-problem seed noise and gates it on reseeded verification and leave-one-out ablation of the agent’s own
edits. A recurring lesson from this cluster, made explicit by MLE-bench, is that such agents are high-variance and
ought to be scored over many seeds; this work takes that lesson inside the loop, turning a reporting convention into an
acceptance gate.
    Automated hyperparameter search, of course, predates LLMs, and it supplies the baseline adopted here. Bergstra
and Bengio [14] established random search as both an effective method and the natural baseline against which any
adaptive search must be measured, and modern frameworks such as Optuna [15] provide efficient define-by-run search
and pruning. This paper adopts that baseline directly: each LLM campaign here is run against a random search over the


                                                             2
same editable surface under a matched per-iteration budget, anchored to a shared first iteration so both arms start from a
common configuration.
    Seed sensitivity and under-powered evaluation are recurring hazards in machine learning. Henderson et al. [2]
showed that deep reinforcement-learning results are highly sensitive to random seeds and implementation details;
Agarwal et al. [3] argued that evaluation in the few-seed regime must report uncertainty rather than point estimates; and
the NeurIPS reproducibility program [16] codified reporting practices to combat the same failure. Together these works
motivate the central design choice of this paper: an agent that experiments faster only compounds the over-claiming risk
unless its conclusions are filtered through measured seed noise, reseeded verification, and ablation of its own edits, so
that filtering is built directly into the loop.
    The problems on which the framework is exercised come from learned guidance, navigation, and control for
spacecraft. Behavioral cloning has a long lineage in control, from ALVINN [17] to the no-regret analysis of DAgger [18],
and has been used to distill optimal guidance solvers into fast feedback policies, as when Sánchez-Sánchez and Izzo [1]
represent optimal landing guidance with deep networks for onboard evaluation. The control formulations relied on here
are classical: relative orbital motion via the Clohessy–Wiltshire equations [19], convex powered-descent guidance [20],
and safety enforcement through control barrier functions [21]. They also build on the authors’ prior work in optimal
feedback control and stochastic reachability analysis [22–26]; this reachability analysis underlies the screening of
feasible initial conditions in the present demonstration problem. On the learning side, reinforcement learning has
been applied directly to spacecraft guidance and control, as in deep reinforcement learning for six-degree-of-freedom
planetary landing [27] and adaptive guidance with reinforcement meta-learning [28], and the authors have previously
unified multi-phase trajectory optimization in a single transformer-based reinforcement-learning policy [29].
    Most relevant, and most important to distinguish from the present work, is a recent line that places language models
inside the spacecraft control loop. LLMs have been used as autonomous spacecraft operators that act on natural-language
prompts [30], vision-language models have been cast as operator agents in the space domain [31], a reasoning LLM
trained with group relative policy optimization has been used to synthesize stabilizing control policies [32], and compact
networks applied recursively have served as efficient optimal controllers [33]. In each of these the model, or a network it
trains, is the controller. The approach here inverts that arrangement: the LLM never flies or commands the vehicle; it is
the offline research agent that proposes, runs, and analyzes the experiments which produce and validate such controllers.
    These threads have not previously been brought together. LLM agents now routinely automate machine-learning
experimentation [8, 9, 11], and a recent line pursues experimental rigor [13]; the reproducibility literature shows that
fast experimentation without statistical discipline is dangerous [2, 3]; and the aerospace-learning literature supplies
well-posed, safety-critical control problems whose learned components are just the sort a research agent would tune. To
the authors’ knowledge, though, no prior system gates each reported result through an in-loop statistical credibility
audit of measured seed noise, reseeded verification, and leave-one-out ablation of the agent’s own edits, and none has
been applied to aerospace control problems with a known optimal-control benchmark. That combination is the paper’s
contribution: an LLM-driven research agent whose every headline result is so gated, demonstrated on two aerospace
control families.


                                       III. The AutoResearch Framework
     AutoResearch turns the machine-learning research loop into a closed, machine-readable state machine. The human
investigator specifies a problem once, in a fixed format called a family; an LLM-driven agent then repeatedly proposes a
configuration, runs it, reads the result, and decides what to try next, until a stopping condition fires. A separate credibility
layer operates offline on the recorded trail and decides whether any apparent improvement is real, reproducible, and
understood. The two are kept distinct on purpose: the loop is free to search quickly, even optimistically, because nothing
it reports is believed until the credibility layer has audited it. Figure 1 shows the loop, and the remainder of this section
makes each of its pieces precise.


A. Problem formalization
   AutoResearch formalizes the research loop as optimization over a configuration space. A family fixes a finite set of
𝑑 editable hyperparameters, each with a declared domain, so the space of configurations the agent may explore is the
product
                            Ö𝑑
                                              
                     Θ =       Θ𝑗,      Θ 𝑗 ∈ [ℓ 𝑗 , 𝑢 𝑗 ] ∩ Z, [ℓ 𝑗 , 𝑢 𝑗 ] ⊂ R, [ℓ 𝑗 , 𝑢 𝑗 ] log , C 𝑗 ,          (1)
                               𝑗=1



                                                               3
                                       The agent loop • fast inner loop
                                                                                                                                      The credibility audit • offline, post hoc
                                  proposer
                                                                         or
                                                                                           Stop               audit the best run
                                                        1                              close family
                                                    Propose                                                                                        best configuration
                                                   an experiment



                        5                                                                                                                        measured seed noise
                              Record                                           Patch                                                 𝜎 from repeated seeds of a baseline configuration
                                                                                           2
                            run & proposal                               editable region
                                         history    LLM
                                                    agent
        problem brief                                                                                                                            reseeded verification
+ starting train.py                                                                                                                           clears it by 2𝜎 , every seed feasible



          orchestrator                 Parse                         Run
                                      one metric                   subprocess                                                                   leave-one-out pruning
                                  4                                              3                                                                which edits carry the result
                                                                                 runner

                                       one action per turn: propose, or stop                                                                         VERDICT ✓
                                                                                                                                                real, reproducible improvement


Fig. 1 The AutoResearch agent loop and its credibility audit. Left: the language model drives a fast inner loop,
reading the problem description, the run history, and the current hyperparameters and emitting one action
per turn, either an experiment or a stop. The three tinted zones on the loop mark its proposer, runner, and
orchestrator modules (Sec. III.C). A proposed experiment travels once around the loop: the runner patches the
editable region of train.py, runs it, parses one metric line, logs it, and feeds the updated history back. Right:
when the loop stops, its best configuration enters an offline credibility audit that measures a per-problem seed
noise, reseeds the candidate to confirm it clears it by a fixed margin under fresh seeds, and prunes its individual
edits. The audit, not the raw loop, is the step that confirms a genuine improvement reproduces across fresh seeds.


where each axis Θ 𝑗 is an integer interval, a real interval, a log-scaled real interval, or a finite categorical set C 𝑗 . These
four domain types are the ones the framework can sample and patch, and they induce the natural per-axis laws used by
the random search below: an integer or real axis is drawn uniformly, a log-scaled axis as exp U (log ℓ 𝑗 , log 𝑢 𝑗 ) , and a
categorical axis uniformly over C 𝑗 . Because the agent may assign only keys that already exist in the editable region, Θ is
fixed for the duration of a campaign; introducing a genuinely new degree of freedom is a deliberate human act, not a
move the agent can make.
    Evaluating a configuration is expensive and stochastic. Training and scoring a single configuration 𝜃 at random seed
𝑠 yields a scalar metric
                                                                                                                          1 ∑︁
                                             𝑓 : Θ × S → R,                    𝐹 (𝜃) = E𝑠∼S 𝑓 (𝜃; 𝑠) ≈                              𝑓 (𝜃; 𝑠),                                            (2)
                                                                                                                           |S ′ | ′𝑠∈ S

where 𝑓 (𝜃; 𝑠) is one full training run and 𝐹 (𝜃) is the seed-averaged quantity that actually matters. The basic tension is
visible already: the agent must search on single noisy draws of 𝑓 , while any honest claim has to be made about the
mean 𝐹. An orientation 𝜎dir ∈ {+1, −1} is fixed: it equals +1 when larger metric values are better and −1 when smaller
values are better. The oriented gap 𝜎dir 𝑓 (𝑎) − 𝑓 (𝑏) is then positive exactly when configuration 𝑎 is better than 𝑏.
This single sign lets every later threshold be written once, independent of whether the family maximizes or minimizes.
    The agent is then a proposal policy that maps the recorded history to the next configuration to try,
                                                                                                                                   𝑡 −1
                                                   𝜃 𝑡 = 𝜋 H𝑡 −1 ,                   H𝑡 −1 =              (𝜃 𝑖 , 𝑓 (𝜃 𝑖 ; 𝑠𝑖 ), 𝑎 𝑖 ) 𝑖=1 ,                                              (3)

where 𝑎 𝑖 is the structured annotation attached to proposal 𝑖: the hypothesis, the axes touched, and the self-declared kill
criterion described in Sec. III.C. When 𝜋 is a language model that reads the trail in context and emits the next trial, the
LLM acts as an optimizer [6]. This contrasts with amortized approaches, which learn a universal tuner offline from
large corpora of past studies [7]. The natural non-adaptive reference is random search [14], which ignores the history




                                                                                               4
entirely and draws
                                                𝑑
                                                Ì
                                      iid                                                   
                                  𝜃 𝑡rs ∼ 𝑃 =          𝑃𝑗,     𝜃 rs,★
                                                                 𝑁    = arg opt 𝑓 𝜃 𝑡rs ; 𝑠𝑡 ,                            (4)
                                                 𝑗=1                       𝑡≤𝑁

with 𝑃 𝑗 the per-axis law of Eq. (1) and the optimum oriented by 𝜎dir (a best-of-𝑁 selection). The contrast between
the history-dependent policy of Eq. (3) and the memoryless sampling of Eq. (4) is the adaptivity this paper sets out to
measure. Sequential model-based and Bayesian optimization sit between the two, fitting a surrogate to the observed
pairs and choosing each query by an acquisition rule [15, 34]. The LLM policy can be read as a surrogate-free,
language-conditioned member of that family. Its practical advantage is that it reasons directly over the same source code
and run log a human researcher would.


B. The family abstraction and its contract
     A family is a self-contained research problem, realized as a directory of four artifacts: a plain-language description
(program.md) of the goal, the metric, the baseline, and the allowed scope of changes; a single editable training script
(train.py) implementing the dynamics, data, model, and evaluation; a registry (family.json) holding the target metric,
the reference baseline, and the current best configuration; and an append-only log (runs.jsonl) of every completed
experiment. Because every family exposes the same contract, the identical agent loop applies unchanged across problems
with very different dynamics. That contract rests on four invariants.
     The first is a delimited editable region. train.py marks the configurable block with an opening banner, then a series
of top-level NAME = value assignments, then a closing # Fixed Configuration banner, and these assignments are
exactly the axes of Θ in Eq. (1). The agent may change only values inside that region, and only keys that already exist; the
dynamics, the expert solver, the dataset, and the evaluation protocol live beneath the second banner and are immutable
to it. The second invariant is a single structured metric. On success, train.py prints exactly one line of the form
FINAL_METRIC: {"run_id": ..., "<metric>": <float>, ...}, whose primary key matches family.json; 𝑓 (𝜃; 𝑠)
is read straight from that line, with no free-form parsing. Auxiliary fields, such as a success rate or a constraint-violation
rate, are logged for the agent to reason about but never change the optimization target. The third invariant keeps two
separate logs. train.py appends one row per successful experiment to runs.jsonl, while the orchestrator records
every iteration, including invalid proposals, failures, and stops, to proposals.jsonl. The success log is therefore
never contaminated by dead ends, yet the full decision trail stays reconstructable. The fourth invariant is a read-only
preparation step. A prepare.py supports a one-time, expensive –warm-cache and a fast precondition –check; the
orchestrator runs the check before the first live experiment, and the agent never edits either.


C. The agent loop
    The loop is built from three small, independently testable modules, summarized in Algorithm 1: a proposer that
wraps the LLM, a runner that executes a configuration, and an orchestrator that drives the state machine and enforces
termination.
    The proposer presents the model with the current state and forces it to return exactly one of two structured tool calls,
with no free-text channel to scrape. The propose_experiment tool requires a hypothesis, a dictionary of hyperparameter
overrides, one or more axis labels classifying which part of the search space the move touches, an expected mechanism,
an explicit comparison to the prior best, and a numerical failure prediction that serves as a kill criterion written down
before the run. The stop_research tool requires only a status, a conclusion, and the set of axes tested. Forcing
structured output makes every decision in Eq. (3) machine-readable and removes a common source of brittleness in
LLM agents. Each turn the model is shown the same evidence a human would have, in a fixed order: any warnings
raised by the orchestrator, the full program.md, the family.json registry, a compact summary of the random-search
arm, the runs.jsonl history, and the current values of the editable hyperparameters.
    To guard against a model that merely recalls a good configuration from answer-bearing fields rather than searching,
the framework supports a blind mode. The description is replaced by a redacted variant that states the invariant problem
facts but withholds the target and the baseline, and the run history is reduced to (configuration, primary-metric) pairs.
Blind mode is the honest test of iterative search, and is the setting used for the campaign reported in this paper. The
framework supports both Anthropic and OpenAI backends for 𝜋, as well as the key-free random proposer that realizes
Eq. (4). The campaigns reported in this paper use Anthropic’s Claude Sonnet 4.5.
    The runner reads the editable region of train.py by matching the two banners and extracts the top-level assignments.
It applies the proposed overrides by rewriting only the matching value expressions, preserving comments and formatting


                                                              5
Algorithm 1 The AutoResearch agent loop for one family.
Require: family contract (Θ, 𝜃 0 , 𝑓 , 𝜎dir ); policy 𝜋; budgets (𝑡 max , 𝐶max , 𝑅max , 𝜙max , 𝐺 max )
 1: H0 ← ∅; V ← ∅                                                                        ⊲ V: configurations already evaluated
 2: 𝑏 0 ← undefined; 𝜙 ← 0; 𝑡 ← 1
 3: while no trigger of 𝑇★ is active and 𝑡 ≤ 𝑡 max do
 4:     (𝜃 𝑡 , 𝑎 𝑡 ) ← 𝜋(H𝑡 −1 )                                                         ⊲ one forced tool call: propose or stop
 5:     if 𝑎 𝑡 is a stop request then
 6:           enforce justification gate; break
 7:     end if
 8:     if 𝜃 𝑡 ∈ V or keys(𝜃 𝑡 ) ⊈ Θ then
 9:           record invalid; 𝜙 ← 𝜙 + 1; continue
10:     end if
11:     𝑦 𝑡 ← 𝑓 (𝜃 𝑡 ; 𝑠𝑡 )                                                         ⊲ isolated subprocess, wall-clock timeout
12:     𝑣 𝑡 ← Verdict(𝑦 𝑡 , 𝑏 𝑡 −1 )                                                                                    ⊲ Eq. (8)
13:     H𝑡 ← H𝑡 −1 ∪ {(𝜃 𝑡 , 𝑦 𝑡 , 𝑎 𝑡 , 𝑣 𝑡 )}; V ← V ∪ {𝜃 𝑡 }
14:     update best 𝑏 𝑡 ; 𝜙 ← 0; 𝑡 ← 𝑡 + 1
15: end while
16: return trail H                                                                      ⊲ audited offline by the credibility layer


and refusing any key absent from Θ. It then executes train.py as an isolated subprocess under a wall-clock timeout,
inheriting the allocation’s GPU, and parses the single FINAL_METRIC line from standard output. Editing real source in
place, rather than threading a configuration object, means the agent operates on the same artifact a human researcher
would edit, and that each recorded experiment is reproducible by re-running the patched script.
    The orchestrator assembles the context, validates each proposal, invokes the runner, updates the registry’s best
configuration when a run improves on it, and writes one record per iteration to proposals.jsonl. Two of its
responsibilities are worth specifying. First, it restricts the search to distinct points: a proposal is rejected if either its
override map or the full configuration it would produce has been seen before, so that

                                   𝜃 𝑡 ∉ V = {𝜃 1 , . . . , 𝜃 𝑡 −1 }       and   𝑜 𝑡 ∉ {𝑜1 , . . . , 𝑜 𝑡 −1 },                     (5)

where 𝑜 𝑡 is the canonicalized override map of proposal 𝑡. The agent therefore cannot spend budget re-evaluating a
known point, and a campaign of 𝑁 accepted iterations explores 𝑁 distinct configurations. Second, it terminates the
campaign at a stopping time defined as the first iteration at which any trigger becomes active,
                    n                                                                                   o
        𝑇★ = min 𝑡 ≥ 1 : 𝑐 𝑡 > 𝐶max ∨ 𝑟 𝑡 ≥ 𝑅max ∨ 𝜌𝑡 ∨ 𝑡 ≥ 𝑡max ∨ 𝜙𝑡 ≥ 𝜙max ∨ 𝑔𝑡 > 𝐺 max ∨ Π𝑡 ,                (6)

where
        𝑐 𝑡 is elapsed   wall-clock against budget 𝐶max , 𝑟 𝑡 the number of successful runs against a cap 𝑅max , 𝜌𝑡 =
  𝜎dir (𝑏 𝑡 − 𝑦 tgt ) ≥ 0 the predicate that the running best 𝑏 𝑡 has reached the family target 𝑦 tgt , 𝑡 max the iteration cap, 𝜙𝑡 the
count of consecutive failed or invalid proposals against a cap 𝜙max (three in these runs), 𝑔𝑡 the cumulative LLM spend
against a monetary cap 𝐺 max , and Π𝑡 the plateau predicate of Eq. (9) below. These triggers are checked in the fixed
precedence in which they are written. The agent’s own stop_research is an additional termination path, admitted only
through a justification gate. A stop is accepted when the target is genuinely met, or else when at least six experiments
have completed and at least four distinct axes have been exercised; a positive close asserted without the target actually
being reached is rejected outright. Every campaign is therefore bounded in time, in number of experiments, and in cost,
and premature or over-stated closure is structurally difficult.


D. The credibility layer
    The components above let an agent search quickly; making its results trustworthy is the job of the credibility
layer. Deep reinforcement-learning and machine-learning results are well known to be sensitive to random seeds and
implementation detail [2], evaluation in the few-seed regime must report uncertainty rather than a point estimate [3],
and the community has codified reporting practices to combat this failure [16]. An agent that experiments faster only
compounds the over-claiming risk unless its conclusions are filtered. Every claim is therefore denominated in a measured
unit of noise, and the three checks that follow are applied uniformly to every family.


                                                                       6
Measured seed noise. Before any improvement is credited, the framework measures how much the metric moves from
one random seed to the next, for reasons unrelated to the agent’s edits. This is the family’s seed noise: the run-to-run
variability a real gain must exceed, analogous to the noise floor a signal must rise above to be detected. A fixed baseline
configuration 𝜃 0 is run across 𝐾 seeds, yielding
                                                         v
                                                         u
                                                         t
                                 𝐾                                   𝐾
                              1 ∑︁                             1 ∑︁                        2
                       𝜇0 =         𝑓 (𝜃 0 ; 𝑠𝑖 ), 𝜎 =                   𝑓 (𝜃 0 ; 𝑠𝑖 ) − 𝜇0 ,  𝐾 ≥ 2,                   (7)
                              𝐾 𝑖=1                          𝐾 − 1 𝑖=1

the sample mean and the Bessel-corrected sample standard deviation of the metric. The quantity 𝜎 is not a tuned
hyperparameter but a measured property of the family, and it is the unit in which all subsequent claims are denominated.
Because 𝜎 is itself estimated from finitely many seeds, 𝐾 must be large enough that the acceptance margin below is not
dominated by uncertainty in 𝜎. 𝐾 is therefore reported with every result. In the demonstration of Sec. V the mean
difference and its confidence interval are also reported, alongside the standardized margin, so the claim does not rest on
a sigma-count drawn from too few samples. This is the discipline the few-seed literature calls for [3], applied to the
noise estimate itself.
    The same 𝜎 also supplies the in-loop machinery of Sec. III.C. After each run the orchestrator assigns a cheap,
single-seed verdict relative to the prior best 𝑏 𝑡 −1 ,
                                    
                                    
                                    
                                     confirmed       𝛿 ≥ 𝑡ˆnf ,
                                    
                                                                                                          
                          𝑣(𝜃 𝑡 ) = regressed         𝛿 ≤ −𝑡ˆnf ,           𝛿 = 𝜎dir 𝑓 (𝜃 𝑡 ; 𝑠𝑡 ) − 𝑏 𝑡 −1 ,          (8)
                                    
                                    
                                    
                                     within noise
                                                     |𝛿| < 𝑡ˆnf ,

where the threshold 𝑡ˆnf is the measured 𝜎 when available and a fallback of max 0.05 |𝑏 𝑡 −1 |, 10−12 otherwise. The
                                                                                                       
same threshold drives the plateau predicate that feeds the stopping time of Eq. (6): with a sliding window of the last 𝑤
successful runs (here 𝑤 = 6) and the pre-window best 𝑏 pre ,
                                       h                                             i
                                 Π𝑡 = ∀ 𝑟 ∈ last 𝑤 runs : 𝜎dir 𝑓𝑟 − 𝑏 pre < 𝜅 𝑡ˆnf ,                                  (9)

so the campaign is declared stuck when an entire window fails to beat the pre-window best by more than 𝜅 noise units
(with scale 𝜅 = 1 by default).

Reseeded verification. A single-seed best run can be a fluke of the seed, so the agent’s reported best is not believed
on the strength of the run that produced it. The layer reconstructs each configuration’s full setting by walking
proposals.jsonl, deduplicates by configuration with the seed removed, ranks the candidates, and re-runs the top few at
a set of fresh, held-out seeds disjoint from those that generated them. A train-loss parity guard excludes any reseed
whose best training loss exceeds twice that of its source run, so a seed throttled by resource contention cannot pollute
the aggregate. Over the valid reseeds S𝑅 the reseeded mean 𝜇 𝑅 and standard deviation 𝜎𝑅 are formed, and 𝜇 𝑅 , not the
single-seed best, is reported as the headline number. The improvement is credited only when it clears the seed noise by
a standardized margin and is feasible on every seed,
                                                                                                          
                                                        Ó                                  𝜎dir 𝜇 𝑅 − 𝜇0
              accept 𝜃ˆ ⇐⇒ 𝜎dir 𝜇 𝑅 − 𝜇0 ≥ 2𝜎 ∧                            ˆ
                                                           𝑠∈ S𝑅 Feasible( 𝜃; 𝑠) ,    𝑚 =                   .       (10)
                               |        {z        }      |         {z         }                   𝜎
                                   effect-size gate                  all-seeds safety

The gate is a one-sided test in units of the measured standard deviation, in the spirit of a standardized effect size [35].
The reported margin 𝑚 counts how many noise units separate the reseeded result from the baseline, and a result is
promoted to the family best only when 𝑚 ≥ 2 and the hard safety constraint holds on all of S𝑅 . For the rendezvous
campaign of Sec. V this margin is roughly 𝑚 ≈ 15.0.

Leave-one-out pruning. Acceptance establishes that the result is real; pruning asks which of the agent’s edits actually
                                                    ˆ the layer reverts each modified parameter 𝑖 to its family default in
carry it. Starting from the accepted configuration 𝜃,
isolation, holds the rest fixed, and remeasures. Writing the oriented change from that reversion as
                                                 
                        Δ𝑖 = 𝜎dir 𝑓 (𝜃 −𝑖 ) − 𝜇 𝑅 ,     𝜃 −𝑖 = 𝜃ˆ with parameter 𝑖 reset to default,                 (11)


                                                               7
a negative Δ𝑖 means reverting the parameter hurts, so the parameter is load-bearing, while a positive Δ𝑖 means reverting
it helps, so the agent moved it the wrong way. The decision is taken in noise units and escalated only when a single
probe seed is inconclusive, with Δ𝑖(1) the one-seed estimate and Δ𝑖(2) a two-seed mean,

                                 
                                 
                                  keep        Δ𝑖(1) ≤ −𝜎    (clearly load-bearing),
                                 
                                               Δ𝑖(2) < 0.5 𝜎 (no signal, a hitchhiker),
                                 
                                 
                                  drop
                                 
                                 
                   decision(𝑖) =                                                                                            (12)
                                 
                                 
                                  drop†       Δ𝑖(2) > 0 (reverting helps, flag interaction),
                                 
                                 
                                               −𝜎 < Δ𝑖(2) ≤ −0.5 𝜎 (borderline, kept conservatively).
                                 
                                  keep
                                 
This separates load-bearing edits from inert hitchhikers and, through the † case, surfaces edits moved in the wrong
direction. A subtlety the single-parameter test cannot see is that a group of parameters can each be individually inert,
|Δ𝑖(2) | < 0.5𝜎, yet matter jointly, so that dropping all of them together regresses the metric. The layer guards against this
by re-verifying the pruned recipe 𝜃 pruned at fresh seeds and retaining the simplification only if it still clears the same gate,
                                                                        
                          publish 𝜃 pruned ⇐⇒ 𝜎dir 𝐹 (𝜃 pruned ) − 𝜇0 ≥ 2𝜎 ∧ target retained;                               (13)
otherwise the full configuration is kept. In the rendezvous campaign this is what happens: five edits prove load-bearing
and four are individually inert, but the four together are not, so the re-verification of Eq. (13) forces the full recipe to be
retained.
    Finally, as an external sanity check and not as a promotion gate, the framework runs the undirected random search
of Eq. (4) over the same editable surface from the same shared first iteration under a matched per-experiment budget.
Comparing the two arms’ best results in the same noise units gives a verdict,
                                                                                
                                            
                                            
                                            
                                             LLM wins       𝜎dir 𝑏 LLM − 𝑏 rs > 2𝜎,
                                            
                                                                               
                                     𝑉 = random wins 𝜎dir 𝑏 LLM − 𝑏 rs < −2𝜎,                                              (14)
                                            
                                            
                                            
                                             tie            otherwise,
                                            
which confirms that the agent’s guidance does more than blind sampling would, while keeping the seed-noise gate of
Eq. (10) as the claim on which the result actually rests.


                                            IV. Demonstration Problems
    The framework is exercised on two spacecraft-guidance problems that share the same Clohessy–Wiltshire relative
dynamics and pose the same research task: learn, by behavioral cloning, a feedback policy that matches an optimal-control
solver across a wide range of initial conditions. They differ in just one way that matters for the audit. The first is an
unconstrained rendezvous, in which the chaser may fly any path to the target. The second is a collision-avoidance
docking, in which the chaser must reach a point just outside a spherical keep-out zone while starting on its far side, so
the straight-line approach pierces the zone and the policy must actively detour around it. The second therefore binds a
hard safety constraint that the first does not.
    These problems are chosen not for their guidance content, which is classical, but because each is bracketed in a
way that lets the credibility layer (Sec. III.D) do its work. At the bottom, the optimal-control expert defines a known,
near-zero performance benchmark; just above it, a fixed baseline configuration fixes the scale of seed-to-seed metric
noise. An apparent improvement can then be judged against both a meaningful benchmark and a measured noise, which
is what the layer needs to certify that a gain is real and not just a lucky seed. The docking problem adds a binding
safety constraint that an accuracy-only metric cannot capture, stressing the same layer along a second axis. In both, the
contribution is the autonomous, auditable process that produces the policy, not a new guidance law.


A. Relative orbital dynamics
    The chaser’s motion relative to the target is modeled with the linear Clohessy–Wiltshire–Hill (CWH) equations [19]
in the target’s local-vertical/local-horizontal (LVLH) frame. Writing the relative position as r = [𝑥, 𝑦, 𝑧] ⊤ , the per-axis
thrust as u = [𝑢 𝑥 , 𝑢 𝑦 , 𝑢 𝑧 ] ⊤ , the deputy mass as 𝑚, and the chief mean motion as 𝑛, the continuous-time equations of
motion are                                                                 𝑢𝑦
                                                          𝑢𝑥                                  𝑢𝑧
                                     𝑥¥ − 2𝑛 𝑦¤ − 3𝑛2 𝑥 =    , 𝑦¥ + 2𝑛𝑥¤ =    ,   𝑧¥ + 𝑛2 𝑧 =    .                       (15)
                                                          𝑚                𝑚                  𝑚

                                                               8
With the state x = [r⊤ , r¤ ⊤ ] ⊤ ∈ R6 , these collect into the linear state-space form x¤ = 𝐴𝑐 x + 𝐵 𝑐 u, with

                             "                #          3𝑛2         0      0            0        2𝑛   0           "          #
                                 03      𝐼3                                                                                03
                    𝐴𝑐 =                               Γ= 0                           Ω = −2𝑛                   𝐵𝑐 =
                                                                                                          
                                                  ,                   0      0 ,                      0   0 ,              1
                                                                                                                                        ,   (16)
                                 Γ       Ω                                                                
                                                                                                                             𝑚 𝐼3
                                                          0
                                                                     0     −𝑛2           0
                                                                                                      0   0

where 𝐼3 and 03 are the 3 × 3 identity and zero blocks. The simulator advances the state with a forward-Euler
discretization at step Δ𝑡,
                           x 𝑘+1 = 𝐴 x 𝑘 + 𝐵 u 𝑘 ,  𝐴 = 𝐼6 + Δ𝑡 𝐴𝑐 ,   𝐵 = Δ𝑡 𝐵𝑐 ,                       (17)
and the cloned policy is evaluated in closed loop on these same matrices, so the student imitates trajectories the simulator
can replay exactly. Both problems use mean motion 𝑛 = 1.13 × 10−3 rad s−1 (a low-Earth orbit), step Δ𝑡 = 10 s, and
deputy mass 𝑚 = 500 kg; they differ in horizon, thrust authority, and constraints, as detailed below.


B. Rendezvous
      The rendezvous problem runs over a horizon of 𝐻 = 80 steps (800 s), with each thrust axis box-constrained to
|𝑢 𝑖 | ≤ 0.25 N. The chaser must close from a wide range of initial conditions to the target at the origin.

Expert demonstrations. The demonstrations come from the optimal control: among all thrust histories that satisfy
the linear dynamics, the per-axis thrust box, and a terminal-equality constraint driving the state to the origin, it is the
one of least control effort, the finite-horizon minimum-energy solution
                             𝐻
                             ∑︁−1
                    min               ∥u 𝑘 ∥ 22       s.t.   x 𝑘+1 = 𝐴x 𝑘 + 𝐵u 𝑘 , x0 = x (𝑖) , x 𝐻 = 0, ∥u 𝑘 ∥ ∞ ≤ 𝑢 max .                 (18)
                    {u 𝑘 }
                             𝑘=0

Because the dynamics are linear and the cost convex, this optimal-control problem is a convex quadratic program, solved
to global optimality. Initial conditions are sampled from a fixed box (positions in [±75, ±75, ±37.5] m, velocities in
[±0.08, ±0.08, ±0.04] m/s) and then screened for reachability: Eq. (18) is solved for each candidate, and only initial
conditions the expert can drive to the origin within tolerance are retained. As a result the expert’s success rate on the
evaluation set is 1.0 by construction, which makes the success criterion (below) a genuine test of the cloned policy’s
quality rather than an artifact of infeasible starts.

Policy and metric. The cloned policy is a time-conditioned multilayer perceptron whose input is the seven-vector
[𝑥, 𝑦, 𝑧, 𝑥,
          ¤ 𝑦¤ , 𝑧¤, 𝜏], where the time-to-go feature 𝜏 = (𝐻 − 𝑘)/𝐻 decreases from 1 at the first step to 1/𝐻 at the last.
The time feature is essential: the finite-horizon expert is a time-varying controller, and a policy that observes only the
physical state is asked to imitate a one-to-many map and fails near the terminal time. Writing s for this time-augmented
policy input, in both problems the policy 𝜋 𝜃 is trained by behavioral cloning on the expert demonstrations: the input is
standardized componentwise to zero mean and unit variance, s̃ = (s − 𝝁s )/𝝈 s , the expert action is normalized by the
thrust limit, ũe = ue /𝑢 max , and the weights 𝜃 minimize the mean-squared action error
                                                                              𝑁
                                                                          1 ∑︁                    2
                                                                 min            𝜋 𝜃 (s̃𝑖 ) − ũe𝑖 2                                         (19)
                                                                  𝜃       𝑁 𝑖=1

over the 𝑁 state-action pairs in the demonstration set (the chosen number of expert trajectories unrolled over
                                                                                                             the horizon).
At evaluation the policy output is rescaled and saturated to the thrust box, u = clip 𝑢 max 𝜋 𝜃 (s̃), ±𝑢 max , and applied
in closed loop. The primary metric is the mean terminal distance, the mean Euclidean position error at the final step
over a held-out set of 128 reachability-screened initial conditions, in meters, with lower being better. A per-condition
success requires a terminal distance below 25 m and a terminal speed below 0.05 m s−1 . The optimal-control expert
reaches the origin essentially exactly, so it sets a near-zero performance benchmark; the learning question is how close a
behaviorally cloned policy can come to it.




                                                                                  9
C. Collision-avoidance docking
    The docking problem uses the same dynamics (Eqs. (15)–(17)) over a longer horizon of 𝐻 = 240 steps (2400 s) and
with a larger per-axis thrust box |𝑢 𝑖 | ≤ 2 N, to give the detour the needed control authority. The chief occupies a hard
keep-out sphere of radius 𝑅KOZ = 5 m centered at the LVLH origin c. The docking target g sits at 𝑅goal = 8 m, 3 m
outside the keep-out surface, on a per-episode random bearing, and the chaser starts 40 m to 110 m out on the far side,
biased opposite the docking point, so a direct run to the target would cross the sphere.

Expert demonstrations. The expert is again the finite-horizon minimum-energy optimal control, driving both the
position and the relative velocity to the docking state while enforcing the keep-out as a sequence of per-step radial
half-space constraints, in the spirit of convex-optimization guidance [20],
                                𝐻
                                ∑︁−1
                       min             ∥u 𝑘 ∥ 22   s.t.   x 𝑘+1 = 𝐴x 𝑘 + 𝐵u 𝑘 ,     x0 = x (𝑖) ,   x 𝐻 = [g⊤ , 0⊤ ] ⊤ ,   (20)
                       {u 𝑘 }
                                𝑘=0                       ∥u 𝑘 ∥ ∞ ≤ 𝑢 max ,      n̂⊤𝑘 (r 𝑘 − c) ≥ 𝑅KOZ + 𝛿,

where n̂ 𝑘 is the unit radial direction of the current iterate’s position from the keep-out center and 𝛿 is a standoff
margin. The half-space is a convex restriction of the non-convex “stay outside the ball” constraint, refined over a few
sequential-convex-programming iterations into a smooth detour that hugs the keep-out and ends exactly at the goal. The
resulting trajectories are collision-free and terminal-zeroing, so the expert defines a near-zero accuracy benchmark and
is feasible by construction. As in the first family the expert is time-varying, so the cloned policy is given a time-to-go
feature, and only collision-free, goal-reaching demonstrations survive a reachability screen.

Policy, metric, and safety gate. The cloned policy is a time-conditioned multilayer perceptron mapping the ten-vector
[ r⊤ , v⊤ , g⊤ , 𝜏 ] ⊤ (relative position, relative velocity, the docking-target position g, and the normalized time-to-go 𝜏)
to a three-axis thrust command, and it is trained by the same behavioral-cloning objective as the rendezvous policy
(Eq. (19)), differing only in its inputs and in the metric below. Evaluation is pure closed-loop rollout, never anchored to
the expert reference, so compounding error is visible by design. The primary metric is a safety-aware docking score, in
meters-equivalent and lower is better,
                                                       score = 𝑑¯T + 10 𝜈,  ¯                                            (21)
where 𝑑¯T is the mean terminal distance to the docking point and 𝜈¯ is the mean fraction of rollout steps spent inside
the keep-out zone, both averaged over a held-out set of 128 far-side initial conditions. The 10× weight makes a single
sustained violation cost more than the entire docking-accuracy budget, so accuracy cannot be bought with violations.
Feasibility itself is a separate hard gate rather than a score term: a strict run requires a success rate of at least 0.80 (an
initial condition succeeds when the terminal distance and speed are within tolerance with zero keep-out violations) and
a mean violation rate of exactly zero and a nonnegative minimum keep-out clearance. A run is credited only if it lowers
Eq. (21) and clears this gate; the family target is a score at or below 0.7 under the gate.

Run-time safety lever. Because the constraint is hard, the editable surface includes a discrete-time predictive control-
barrier-function (CBF) safety filter [21] that can minimally edit each thrust command at rollout time to keep the chaser
outside the keep-out zone, the standard run-time-assurance paradigm. For this relative-degree-two system a one-step
lookahead cannot be filtered, so the filter predicts the two-step state under a held action, x𝑡+2 = 𝐴2 x𝑡 + ( 𝐴𝐵 + 𝐵)u, and
requires the radial component of the predicted position to stay outside 𝑅KOZ + 𝛿. This reduces to a single-constraint
quadratic program that minimally corrects the base-policy command uBC ,

                                 u★ = arg min ∥u − uBC ∥ 22            s.t.    𝜷⊤ u ≥ 𝜌,       ∥u∥ ∞ ≤ 𝑢 max ,            (22)
                                                   u

with 𝜷 = ( 𝐴𝐵 + 𝐵) ⊤ n̂ 1:3 and 𝜌 = (𝑅KOZ + 𝛿) − n̂⊤ 𝐴2 x𝑡 1:3 , where n̂ is the radial direction anchored at r𝑡+1 and
                                                             

[ · ] 1:3 takes the position rows. It has a closed-form solution (half-space projection plus box clip) and is exposed
to the agent as a single Boolean parameter: with the filter off, even a well-trained policy clips the keep-out on its
boundary-riding detours and is infeasible; with it on, the keep-out is enforced and the policy is strict-feasible. The filter
is a soft assurance, not a guarantee, since a sufficiently poor policy can still miss the dock. Whether to engage it is one
of the choices the agent must make, and it lets the credibility layer separate an accuracy improvement from a safety one.



                                                                         10
D. Editable surface
     Across both problems the agent may edit only the hyperparameters in Table 1; the dynamics, the keep-out geometry,
the experts, the datasets, the evaluation protocol, the penalty weight, the filter standoff 𝛿, and input-noise augmentation
(fixed off at zero in both families) are immutable. In blind mode the agent is shown the operational bounds of each
parameter, that is, the values the runner and dataset accept, but not which values are good; it must discover the good
region empirically. The description also defines an axis taxonomy (data, optimizer, architecture, training budget,
regularization, and, for the docking problem, safety) that the agent must use to classify each proposal, so the recorded
trail reveals which parts of the search space were actually explored.

Table 1 The editable hyperparameter surface shared by the two demonstration problems, as shown to the agent
in blind mode. Bounds are operational limits, not hints about the optimum, and the code name of each parameter
is given for reference. The last two parameters exist only in the docking problem; “n/a” marks a parameter
absent from the rendezvous problem. The random-search baseline samples uniformly from a bounded sub-range
of these same parameters.

      Hyperparameter       Code name                    Axis              Rendezvous            Docking

      Demonstrations       N_DEMOS                      data              int [1, 256]          {32, 64, 128, 256}
      Training epochs      EPOCHS                       training budget   int [5, 5000]         int [10, 120]
      Learning rate        LEARNING_RATE                optimizer         [10−5 , 10−2 ]        [10−4 , 5 × 10−3 ]
      Batch size           BATCH_SIZE                   optimizer         int [16, 1024]        {64, 128, 256, 512}
      Weight decay         WEIGHT_DECAY                 optimizer         [0, 10−2 ]            [0, 10−3 ]
      Gradient clip        GRAD_CLIP                    optimizer         [0.1, 10]             [0.5, 5]
      Hidden width         HIDDEN_DIM                   architecture      int [16, 1024]        {64, 128, 256}
      Depth                N_LAYERS                     architecture      int [1, 8]            int [1, 4]
      Activation           ACTIVATION                   architecture      tanh / ReLU / GELU    tanh / ReLU / GELU
      Dropout              DROPOUT                      regularization    [0, 0.5)              [0, 0.3]
      Safety filter        RUNTIME_CBF_FILTER           safety            n/a                   {off, on}
      Recovery augment     RECOVERY_AUGMENT_FRAC        data              n/a                   [0, 0.5]




                                                      V. Results
    The agent was run on both demonstration problems in blind mode (Sec. III.C), each for a single campaign, and
the identical credibility check (Sec. III.D) was applied to the best configuration it found. The outcome takes the same
three-part shape on both: the agent drives the cloned policy down to the numerical neighborhood of the optimal-control
benchmark; reseeding on fresh seeds confirms the gain is real, not a one-seed accident; and a parallel undirected search
over the same parameters trails it. The rendezvous shows the audit in the clean, unconstrained case; the docking then
adds a hard keep-out constraint, so the audit must certify accuracy and safety at once and the gap to undirected search
sharpens from quantitative to categorical. The two are taken in turn.


A. Rendezvous
    On the rendezvous problem the agent ran a single blind-mode campaign of 57 experiments. Figure 2 summarizes
both halves of the result: how the search descended, and the recipe it converged on.
    Both the agent and the random search begin from the same first experiment, whose policy leaves a mean terminal
distance of roughly sixteen meters. From there the agent works the error down in stages, as the running-best curve in
Fig. 2(a) shows, reaching a single-seed best of 0.094 m. That is close to the optimal-control expert, which reaches the
origin to within numerical tolerance. The configuration behind that single-seed best is wider and trained longer than the
default, but no deeper, holding at four layers: a hidden width of 640 with GELU activations, the full set of 256 expert
demonstrations, a small learning rate, and a large training budget. Along the way the agent explored still wider networks,
up to roughly 900 units. The trend holds across the campaign (Fig. 2(b)), and it matches the intuition that a clean
imitation problem with an exactly reachable expert rewards capacity and thorough training over heavy regularization.
    Figure 3 shows what that configuration achieves in the state space the problem actually cares about. Starting from


                                                            11
                                    (a) The agent finds it; undirected search plateaus




                                            (b) . . . and converges on a recipe




Fig. 2 The Clohessy–Wiltshire rendezvous search. (a) The agent (green) drives the cloned policy’s mean
terminal distance from about 16 m to 0.094 m over 57 experiments, while a matched random search (blue) over
the same parameters plateaus near 0.635 m. (b) The recipe it converges on: the network is fixed at four layers
early, then the hidden width and training length grow while the learning rate anneals and dropout falls to zero, a
directed search rather than a random walk.




                                                           12
Fig. 3 The learned policy flies the rendezvous. From five held-out initial conditions, the cloned policy (solid)
steers the spacecraft to the target along paths that overlay the optimal-control solution (dashed), and the position
norms decay smoothly to zero over the 800 s horizon.

Table 2 Credibility-audited results on the Clohessy–Wiltshire rendezvous problem. Lower mean terminal
distance is better; the optimal-control expert reaches the origin essentially exactly. The reseeded mean is the
headline number, and the single-seed best is shown for traceability.

                     Arm                           Mean term. dist. (m)   Success rate   vs. seed noise

                     Seed noise (n=10)                 4.04 ± 0.26           ∼0.75         reference
                     Matched random (best of 60)          0.635               1.0          not gated
                     LLM agent, single-seed best          0.094               1.0          not gated
                     LLM agent, reseeded (n=10)       0.101 ± 0.007           1.0        15.0𝜎, PASS



five held-out initial conditions, the cloned policy steers the spacecraft to the target along trajectories that overlay the
expert’s, and the corresponding position-norm histories decay smoothly to zero over the eight-hundred-second horizon.
The improvement is not a quirk of the scalar metric; it is a guidance law that flies the rendezvous.
    Still, a single-seed best could be luck, and the credibility check tests that directly. The measured seed noise is
4.04 m ± 0.26 m over ten seeds, and at that level the policy succeeds on only about three-quarters of the evaluation
cases. Reseeding the agent’s best configuration over ten fresh seeds, disjoint from those that measured it, yields
0.101 m ± 0.007 m, with a perfect success rate on every seed. The reseeded mean improves on the calibrated comparator
by a mean difference of 3.94 m (95% confidence interval [3.75, 4.12] m), which is 𝑚 ≈ 15.0 units of the measured noise
standard deviation, far beyond the two-sigma acceptance threshold. Because that standard deviation is itself measured
over ten seeds, the margin rests on a firm denominator. This gate is the primary evidence that the result is genuine,
resting on nothing more than the problem’s own measured noise.
    The audit also revises which configuration to designate as best. The campaign’s single best run used one of the
wider networks the agent explored, a hidden width of 640, reaching 0.094 m at its seed. But under ten fresh seeds a
narrower network (hidden width 512) proved the more reproducible of the two leading candidates, and it is promoted
as the audited family best. The single-seed best (0.094 m) and the reseeded headline (0.101 m) are therefore different
configurations, and keeping the reproducible one is the whole point of the audit. Table 2 collects the arms.
    As a secondary check, the agent is compared against undirected search over the same parameters, both anchored to
the shared first experiment under a matched per-experiment budget (Fig. 2(a)). The agent reaches 0.094 m (reseeded
0.101 m) while random search across 60 trials plateaus near 0.635 m, a separation of more than six to one. This is best
read as suggestive rather than decisive: the agent reached a larger training budget than the random sweep happened to
sample, so part of the gap reflects the region explored, not the search strategy alone, and tightening the random arm to a
matched range is future work. The central claim stands on the seed-noise gate above, which does not depend on this
comparison.



                                                            13
Table 3 Credibility-audited results on the collision-avoidance docking problem. Lower score (Eq. (21), meters-
equivalent) is better; the optimal-control expert reaches the dock essentially exactly. Strict feasibility requires
success ≥ 0.80, zero KOZ violations, and nonnegative clearance on every seed.

                         Arm                               Score      Strict-feasible   vs. seed noise

                         Seed noise (n=10)              8.45 ± 1.55    no (no dock)      reference
                         Random search (best of 24)        6.46           0 of 24        not gated
                         LLM agent, single-seed best       0.33             yes          not gated
                         LLM agent, reseeded (n=10)     0.38 ± 0.07      10 of 10       5.2𝜎, PASS



    The credibility check asks not only whether the result is real but which of the agent’s edits produced it. Leave-one-out
pruning reverts each edit in turn and remeasures. Five edits prove load-bearing: the number of demonstrations, the
training budget, the learning rate, the hidden width, and the depth. The remaining four, batch size, weight decay,
gradient clipping, and the activation choice, carry no individual signal. Dropping all four together, however, regresses
the reseeded metric from 0.101 m to 0.192 m, so they matter in combination even though none matters in isolation, and
the full configuration is therefore retained as the family best. This separates edits that matter, those that do not, and
those that matter only in combination, a distinction an informal report would miss.

B. Collision-avoidance docking
     On the docking problem the agent ran a single blind-mode campaign of 23 experiments. The story parallels the
rendezvous, with the stakes raised: the policy must now respect a hard keep-out constraint, so the audit certifies accuracy
and safety at once. The agent’s advantage is no longer just that it docks more accurately; the undirected baseline never
produces a single feasible policy, while the agent is strict-feasible on every reseed. Figure 4 summarizes the search.
     From a default configuration that docks poorly but stays outside the keep-out zone, the agent works the score down
in stages to a single-seed best of 0.33, well inside the family target of 0.7. As in the rendezvous, the search is methodical,
not a random walk, with the run-time CBF filter held on throughout, and the same intuition applies. Figure 5 shows
what the configuration buys in the state space: starting on the far side of the chief, the cloned policy detours around the
keep-out sphere and docks, its trajectories overlaying the optimal-control expert’s.
     The same gate that certified the rendezvous now carries a second burden, to certify safety alongside accuracy. The
measured seed noise is 8.45 ± 1.55 over ten seeds. Reseeding the agent’s best configuration over ten fresh seeds, disjoint
from those that measured it, yields 0.38 ± 0.07. Crucially, every one of the ten reseeds is strict-feasible: a success rate
above the gate, a mean violation rate of exactly zero, and a nonnegative minimum keep-out clearance. As in the first
family, the effect is reported directly: the reseeded mean improves on the calibrated comparator by a difference of 8.07
(95% confidence interval [6.97, 9.18]), which is 𝑚 ≈ 5.2 units of the measured noise standard deviation, far beyond the
two-sigma acceptance threshold. Both halves of the gate, the effect-size margin and strict feasibility on every seed, are
met.
     As in the rendezvous family, reseeding also revises which configuration to designate as best. The campaign’s best
single run used a narrower network (hidden width 128, reaching 0.33 at its seed). But under ten fresh seeds that network
is erratic (mean 0.61, standard deviation 0.24), whereas a wider network (hidden width 256) is far more reproducible
(0.38 ± 0.07) and is promoted as the family best. Table 3 collects the arms.
     On this problem the gap between directed and undirected search is categorical, not merely quantitative. Over 24
trials sampling the same editable parameters, random search never produces a single strict-feasible policy. Its best score
is 6.46, more than an order of magnitude above the agent’s reseeded mean, and even that is the single luckiest draw
rather than the start of a trend. The rest of the cloud sits at tens to hundreds of meters, closed-loop policies that drift
away from the target rather than docking. Two distinct failures keep every random configuration out of the gate. First,
random search leaves the run-time safety filter switched off in more than half of its draws. Every draw that turned it off
penetrated the keep-out zone, while every draw that happened to leave it on stayed clear; this is why the on/off switch is
the load-bearing safety lever. Second, even the filter-on draws never learn to dock, so their success rate never approaches
the gate’s threshold. Either way, not one random configuration is strict-feasible. The agent, by contrast, is strict-feasible
on all ten reseeds: it learns both to keep the run-time filter engaged and to imitate the detouring expert. Panel (a) of
Fig. 4 shows the two best-so-far traces over the cloud of raw per-experiment scores.



                                                             14
                                       (a) The agent finds it; undirected search cannot




                                              (b) . . . and converges on a recipe




Fig. 4 The collision-avoidance docking search. (a) The agent (green) reduces the safety-aware docking score
(Eq. (21), log scale) from its default to 0.33 over 23 experiments, keeping the safety filter engaged so every credited
run is strict-feasible; a matched random search (blue) never clears the keep-out gate, reaching only 6.46. (b) The
recipe it converges on: the full demonstration set early, the network deepened from two to four layers, longer
training, an annealed learning rate, and the run-time CBF filter kept on throughout. Pruning finds only the
demonstration count and training budget load-bearing; the audit promotes a wider 256-unit network as more
reproducible than the single-seed best’s 128.



                                                             15
Fig. 5 The learned policy docks while respecting the keep-out zone. From held-out far-side initial conditions,
the cloned policy (solid) detours around the keep-out sphere (shaded) and reaches the docking point, overlaying
the optimal-control solution (dashed); the minimum keep-out clearance stays nonnegative on every rollout.


    Finally, leave-one-out pruning reverts each edit in turn and remeasures against the measured seed noise. Two edits
prove load-bearing: the number of demonstrations and the training budget. Reverting the demonstration count alone
returns the score to about 6.6, back near the baseline, while batch size, weight decay, learning rate, hidden width, and
depth carry no individual signal. A distilled recipe that keeps only those two edits and reverts the rest, including the
network back to its default width, still clears the seed noise by about five standard deviations, still meets the family target,
and remains strict-feasible on every verification seed. The win therefore distills to a simple recipe, more demonstrations
and more training, rather than an elaborate architecture. The wider network and tuned learning rate the agent also
adopted improve the reseeded mean and its reproducibility, which is why the audit designates the wide network at 0.38
as the family best, though neither is required to clear either bar. At a coarser, small-sample seed noise the learning rate
had looked load-bearing; it dropped out once the noise was remeasured over ten seeds, a reminder that pruning resolves
only effects that are large relative to the measured noise.


                                        VI. Conclusion and Future Work
    This paper presented AutoResearch, an agentic framework in which a large language model autonomously drives the
machine-learning research loop for aerospace control problems, paired with a credibility layer that separates genuine
progress from seed luck. The framework’s reusable family contract, a plain-language description, one editable training
script, a single structured metric, and an append-only run log, lets the identical agent loop apply across very different
problems, while measured seed noise, reseeded verification, and leave-one-out pruning make each headline result
auditable. On the Clohessy–Wiltshire rendezvous problem the agent reduced the terminal error of a behaviorally
cloned policy until it cleared the measured seed noise by a wide margin, verified by reseeding over ten fresh seeds,
while remaining strict-feasible, and pruning then identified which of its edits actually carried the result. On a second,
safety-constrained family, collision-avoidance docking past a keep-out zone, the same machinery certified a strict-feasible
policy that an undirected search could not match, showing that the loop and its audit carry from one problem to another
despite the change in physics.
    Several limitations bound these results. Each campaign runs for tens of iterations rather than the thousands typical of
large-scale automated search, trading throughput for credibility per experiment, and each uses a single language-model
backend whose influence on the search is not yet characterized. The random-search comparison is a secondary check
rather than the headline: its sampling covered a smaller training budget than the agent’s winning configuration reached,
so the central claim rests on the seed-noise gate rather than on that comparison. Each result also comes from a single
agent run, so while reseeding controls for training-seed luck in the final configuration, the run-to-run variance of the
agent’s own search is not yet characterized.
    Several directions remain. Future work will characterize sensitivity to the choice of language-model backend
and tighten the random-search arm to an exactly matched sampling range. The broader aim is unchanged: to make


                                                              16
LLM-driven experimentation a dependable tool for developing and validating the learned autonomy that future space
missions will require, fast, and honest about what the evidence supports.


                                                          References
 [1] Sánchez-Sánchez, C., and Izzo, D., “Real-Time Optimal Control via Deep Neural Networks: Study on Landing Problems,”
     Journal of Guidance, Control, and Dynamics, Vol. 41, No. 5, 2018, pp. 1122–1135. doi:10.2514/1.G002357.

 [2] Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D., and Meger, D., “Deep Reinforcement Learning That Matters,”
     Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 32, 2018.

 [3] Agarwal, R., Schwarzer, M., Castro, P. S., Courville, A. C., and Bellemare, M. G., “Deep Reinforcement Learning at the Edge
     of the Statistical Precipice,” Advances in Neural Information Processing Systems (NeurIPS), 2021. ArXiv:2108.13264.

 [4] Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., and Ha, D., “The AI Scientist: Towards Fully Automated Open-Ended
     Scientific Discovery,” arXiv preprint arXiv:2408.06292, 2024.

 [5] Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont, E., Ruiz, F. J. R., Ellenberg, J. S., Wang,
     P., Fawzi, O., Kohli, P., and Fawzi, A., “Mathematical discoveries from program search with large language models,” Nature,
     Vol. 625, 2024, pp. 468–475. doi:10.1038/s41586-023-06924-6.

 [6] Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X., “Large Language Models as Optimizers,” International
     Conference on Learning Representations (ICLR), 2024. ArXiv:2309.03409.

 [7] Chen, Y., Song, X., Lee, C., Wang, Z., et al., “Towards Learning Universal Hyperparameter Optimizers with Transformers,”
     Advances in Neural Information Processing Systems (NeurIPS), 2022. ArXiv:2205.13320.

 [8] Huang, Q., Vora, J., Liang, P., and Leskovec, J., “MLAgentBench: Evaluating Language Agents on Machine Learning
     Experimentation,” arXiv preprint arXiv:2310.03302, 2023.

 [9] Jiang, Z., Schmidt, D., Srikanth, D., Xu, D., Kaplan, I., Jacenko, D., and Wu, Y., “AIDE: AI-Driven Exploration in the Space of
     Code,” arXiv preprint arXiv:2502.13138, 2025.

[10] Trirat, P., Jeong, W., and Hwang, S. J., “AutoML-Agent: A Multi-Agent LLM Framework for Full-Pipeline AutoML,”
     International Conference on Machine Learning (ICML), 2025. ArXiv:2410.02958.

[11] Chan, J. S., Chowdhury, N., Jaffe, O., Aung, J., Sherburn, D., Mays, E., Starace, G., Liu, K., Maksin, L., Patwardhan, T., Weng,
     L., and Mądry, A., “MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering,” International
     Conference on Learning Representations (ICLR), 2025. ArXiv:2410.07095.

[12] Liu, S., Gao, C., and Li, Y., “Large Language Model Agent for Hyper-Parameter Optimization,” arXiv preprint arXiv:2402.01881,
     2024.

[13] Kon, P. T. J., Liu, J., Ding, Q., Qiu, Y., Yang, Z., Huang, Y., Srinivasa, J., Lee, M., Chowdhury, M., and Chen, A., “Curie:
     Toward Rigorous and Automated Scientific Experimentation with AI Agents,” arXiv preprint arXiv:2502.16069, 2025.

[14] Bergstra, J., and Bengio, Y., “Random Search for Hyper-Parameter Optimization,” Journal of Machine Learning Research,
     Vol. 13, 2012, pp. 281–305.

[15] Akiba, T., Sano, S., Yanase, T., Ohta, T., and Koyama, M., “Optuna: A Next-generation Hyperparameter Optimization
     Framework,” Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2019,
     pp. 2623–2631.

[16] Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d’Alché Buc, F., Fox, E., and Larochelle, H.,
     “Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program),”
     Journal of Machine Learning Research, Vol. 22, No. 164, 2021, pp. 1–20.

[17] Pomerleau, D. A., “ALVINN: An Autonomous Land Vehicle in a Neural Network,” Advances in Neural Information Processing
     Systems (NeurIPS), 1988.

[18] Ross, S., Gordon, G. J., and Bagnell, J. A., “A Reduction of Imitation Learning and Structured Prediction to No-Regret Online
     Learning,” Proceedings of the 14th International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR, Vol. 15,
     2011, pp. 627–635.



                                                                17
[19] Clohessy, W. H., and Wiltshire, R. S., “Terminal Guidance System for Satellite Rendezvous,” Journal of the Aerospace Sciences,
     Vol. 27, No. 9, 1960, pp. 653–658. doi:10.2514/8.8704.

[20] Açıkmeşe, B., and Ploen, S. R., “Convex Programming Approach to Powered Descent Guidance for Mars Landing,” Journal of
     Guidance, Control, and Dynamics, Vol. 30, No. 5, 2007, pp. 1353–1366. doi:10.2514/1.27553.

[21] Ames, A. D., Coogan, S., Egerstedt, M., Notomista, G., Sreenath, K., and Tabuada, P., “Control Barrier Functions: Theory and
     Applications,” 18th European Control Conference (ECC), 2019, pp. 3420–3431.

[22] Jain, A., Eapen, R. T., and Singla, P., “Sparse Approximate Hamilton-Jacobi Solutions for Optimal Feedback Control
     with Terminal Constraints,” 2023 62nd IEEE Conference on Decision and Control (CDC), 2023, pp. 1269–1274. doi:
     10.1109/CDC49753.2023.10384267.

[23] Jain, A., Eapen, R. T., and Singla, P., “A Hamilton-Jacobi Approach for Nonlinear Model Predictive Control in Applications
     with Navigational Uncertainty,” arXiv preprint arXiv:2503.23603, 2025.

[24] Jain, A., and Singla, P., “Stochastic Reachability Analysis Using Sparse-Collocation Method,” AIAA SciTech 2023 Forum, 2023.

[25] Jain, A., Stochastic Reachability Analysis And Optimal Feedback Control Using Sparse-Collocation Method, The Pennsylvania
     State University, 2023.

[26] Jain, A., Singla, P., and Eapen, R., “Sparse Approximation Method for Accurate Uncertainty Propagation through a Nonlinear
     System,” The Journal of the Astronautical Sciences, Vol. 73, No. 3, 2026, p. 54.

[27] Gaudet, B., Linares, R., and Furfaro, R., “Deep Reinforcement Learning for Six Degree-of-Freedom Planetary Landing,”
     Advances in Space Research, Vol. 65, No. 7, 2020, pp. 1723–1741. doi:10.1016/j.asr.2019.12.030.

[28] Gaudet, B., Linares, R., and Furfaro, R., “Adaptive Guidance and Integrated Navigation with Reinforcement Meta-Learning,”
     Acta Astronautica, Vol. 169, 2020, pp. 180–190. doi:10.1016/j.actaastro.2020.01.007.

[29] Jain, A., Rodriguez-Fernandez, V., and Linares, R., “Multi-Phase Spacecraft Trajectory Optimization via Transformer-Based
     Reinforcement Learning,” arXiv preprint arXiv:2511.11402, 2025.

[30] Rodriguez-Fernandez, V., Carrasco, A., Cheng, J., Scharf, E., Siew, P. M., and Linares, R., “Language Models are Spacecraft
     Operators,” arXiv preprint arXiv:2404.00413, 2024.

[31] Carrasco, A., Nedungadi, M., Zucchelli, E. M., Jain, A., Rodriguez-Fernandez, V., and Linares, R., “Visual Language Models
     as Operator Agents in the Space Domain,” AIAA SciTech 2025 Forum, 2025. ArXiv:2501.07802.

[32] Jain, A., and Linares, R., “Autonomous Reasoning for Spacecraft Control: A Large Language Model Framework with Group
     Relative Policy Optimization,” arXiv preprint arXiv:2601.04334, 2026.

[33] Jain, A., and Linares, R., “Tiny Recursive Control: Iterative Reasoning for Efficient Optimal Control,” AIAA SciTech 2026
     Forum, 2026. ArXiv:2512.16824.

[34] Shahriari, B., Swersky, K., Wang, Z., Adams, R. P., and de Freitas, N., “Taking the Human Out of the Loop: A Review of
     Bayesian Optimization,” Proceedings of the IEEE, Vol. 104, No. 1, 2016, pp. 148–175. doi:10.1109/JPROC.2015.2494218.

[35] Cohen, J., Statistical Power Analysis for the Behavioral Sciences, 2nd ed., Lawrence Erlbaum Associates, Hillsdale, NJ, 1988.




                                                               18
