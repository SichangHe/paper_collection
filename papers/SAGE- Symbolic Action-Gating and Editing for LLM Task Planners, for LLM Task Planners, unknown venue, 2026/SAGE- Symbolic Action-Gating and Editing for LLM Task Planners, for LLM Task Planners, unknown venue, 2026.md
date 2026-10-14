                                                    SAGE: Symbolic Action-Gating and Editing
                                                            for LLM Task Planners
                                              Trung Minh Bui, JongSul Moon, YoungOuk Kim, Quang-Ngoc Phung, Se-Woong Jun, and Dongin Shin∗


                                            Abstract—Large language models (LLMs) are now the default
                                         cognitive core of embodied household agents, yet the plans
                                         they emit are rarely checked against a grounded model of the
                                         environment before execution, and the task-success they report
                                         is often measured on benchmarks so saturated that no method
                                         can be separated from another. We present SAGE (Symbolic
                                         Action-Gating and Editing), a single-LLM planner built from two
arXiv:2609.34268v1 [cs.RO] 28 Sep 2026




                                         lightweight mechanisms: a domain-agnostic symbolic gate (∼250
                                         lines of Python, zero tokens, O(|π|)) that blocks precondition-
                                         violating actions with typed reasons as a runtime safety monitor,
                                         and a local edit that regenerates only the failed sub-goal’s
                                         suffix, keeping completed and untouched work intact; a hybrid
                                         seed+live memory store supports cold-start coverage. Under
                                         a leak-free protocol (leave-one-out retrieval) over five open-
                                         weight models and a 75-task AI2-THOR benchmark, we report
                                         the full picture. On the standard benchmark goal-completeness
                                         saturates (52% of instances trivially solved) and SAGE ties
                                         strong hierarchical baselines; we therefore stress the regime
                                         where methods differ. On a harder, method-agnostic multi-goal
                                         composition, SAGE’s completeness lead re-emerges large (+0.06
                                         to +0.23 across four models). Under injected mid-execution
                                         failures, SAGE recovers as reliably as whole-plan replanners                Fig. 1. SAGE gates and edits. A naive plan Picks the potato before the fridge
                                         at 2.4–3.3× fewer LLM calls. As a verify-before-execute gate,               is open; the zero-token symbolic gate flags the precondition violation and
                                         the symbolic monitor blocks unsafe actions before actuation and             the sub-goal–local edit regenerates only the failed sub-goal’s suffix, yielding
                                         raises simulator-reported step-success for every planner tested (up         a certified plan without a whole-plan replan (frames: AI2-THOR). Bottom:
                                                                                                                     under injected mid-execution failures (all methods recover 100%), SAGE
                                         to +0.11), a signal the verifier never sees, so the gain is non-            recovers with 2.4–3.1× fewer LLM calls than whole-plan replanning (up to
                                         circular. Because the gate calls no model (0.008 ms/plan), it is a          3.3× on compound tasks).
                                         safety layer that runs essentially free on the edge: SAGE planning
                                         reproduces its quality on a Jetson AGX Orin, where small-model              language, an action list, and emit a plan a low-level controller
                                         verification helps most. We release the benchmark, the leak-free            executes [1]–[4]. Even modest open-weight LLMs achieve
                                         protocol, the recovery and safety-gate harnesses, and a verifier-
                                         portability study (auto-induced on ALFWorld, 0.89 held-out).                high task success on benchmarks like ALFWorld [5] and
                                            Index Terms—embodied AI, task planning, large language                   AI2-THOR [6], but at a hidden cost. Plans average 2–3×
                                         models, symbolic verification, AI2-THOR, hierarchical planning              more steps than the ground-truth reference1 , and execution
                                                                                                                     “succeeds” only because most agents add a generous retry-on-
                                                                                                                     failure loop that masks brittle plans behind extra LLM calls,
                                                                  I. I NTRODUCTION                                   each paid on a robot’s limited on-board compute, where a
                                            Large language models (LLMs) are increasingly the cog-                   zero-model-cost grounding layer (real time on a Jetson AGX
                                         nitive core of embodied agents: they read a goal in natural                 Orin) matters most.
                                                                                                                        Two design choices in current planners, plus one gap in how
                                            This work has been submitted to the IEEE for possible publication.
                                         Copyright may be transferred without notice, after which this version may   we evaluate them, are responsible. (P1) Planners do not verify
                                         no longer be accessible.                                                    plans against a grounded environment model before execution:
                                            This work was supported by the Ministry of Trade, Industry and Re-       preconditions like “Find an object before Picking it” live
                                         sources (MOTIR, Korea), Korea, under the Strategic Technology Development
                                         Program supervised by the Korea Institute for Advancement of Technology     only in the LLM’s prompt and are enforced only when the
                                         (KIAT) [Grant No. P0028443], under the Industrial Technology Innovation     simulator errors. This grounded check is domain-agnostic and
                                         Program (No. RS-2023-00232141), by the Institute of Information & Com-      cheap: a compact rule set (∼250 lines) from the action schema
                                         munications Technology Planning & Evaluation (IITP) grant funded by the
                                         Korean government (MSIT) (No. RS-2025-25441838), and by the Korea           (STRIPS-style preconditions/effects), needing no expert and
                                         Electronics Technology Institute (KETI) through its Fundamental Research    auto-inducible from data (§IV-E). (P2) On failure, planners
                                         Support Program.                                                            typically replan the entire remaining task, paying the full token
                                            The authors are with the Intelligent Robotics Research Center, Ko-
                                         rea Electronics Technology Institute (KETI), Seongnam 13449, Repub-         cost again for context that has already been handled correctly.
                                         lic of Korea (e-mails: {minhtrung, moonjongsul, kimyo, ngocpq, daniel,
                                         di shin}@keti.re.kr).                                                         1 Measured on pyplanner’s     38-task             AI2-THOR        set;   see
                                            ∗ Corresponding author: Dongin Shin.                                     record_report.json in the artifact.
Fig. 2. SAGE pipeline. A task is hierarchically decomposed; each sub-goal is expanded with few-shot retrieval from hybrid memory, then every action passes
a zero-token symbolic gate (verify-before-execute). A flagged precondition violation triggers a sub-goal-local edit that regenerates only the failed sub-goal’s
suffix and re-enters the gate; gate-passing steps form the certified plan executed in AI2-THOR.

(P3) Methodologically, standard benchmarks are so saturated                           only the failed sub-goal’s suffix and re-certifies it with
they can no longer separate strong methods. All three are                             the zero-token verifier, avoiding the re-explanation of
tractable without retraining the LLM.                                                 already-correct context (§IV-D, §IV-H).
   We propose SAGE (Symbolic Action-Gating and Editing), a                          • We expose benchmark saturation and re-separate
single-LLM planner whose name reflects its two mechanisms:                            methods (methodological). SAGE does not fix satura-
a symbolic gate on actions and a local edit of plans. It                              tion; we make it measurable. On the standard benchmark
integrates three components:                                                          goal-completeness saturates (52% of instances solved by
   1) a rule-based symbolic precondition verifier that runs                           every strong baseline) and SAGE ties; on a method-
       in O(|π|) time and zero tokens and gates precondition-                         agnostic harder benchmark (multi-goal task composition)
       violating actions before execution,                                            SAGE’s lead re-emerges large (+0.06 to +0.23 complete-
   2) hierarchical decomposition with sub-goal–localised                              ness points over the strongest baseline, Hierarchical Few-
       editing: when a step fails, only the suffix of the failed                      Shot, across four models), with shorter, more valid plans
       sub-goal is regenerated, and                                                   (§IV-C). The hybrid memory is a supporting component,
   3) a supporting hybrid memory store that combines a                                not a core solver: a curated seed pool gives cold-start
       curated seed pool of ground-truth plans with a grow-                           coverage a live-only pool lacks.
                                                                                                                                               2
       ing pool of successful runtime episodes for cold-start                       • A leak-free protocol and reproducible artifacts.

       coverage.                                                                      A      leave-one-out     retrieval    protocol    removes
   Building on a preliminary plan-quality analysis [7], this pa-                      seed↔test leakage; we demote the verifier-computed
per develops a runtime gate-and-edit study; our contributions                         precondition_strict to a diagnostic and report
are empirical and include negative results:                                           metric-validity failures (a reward-based proxy ceiling;
                                                                                      a goal-checker scoring 8% on reference plans) as
   • The symbolic gate is a non-circular runtime safety
                                                                                      findings. We release the benchmark, generators, the
      monitor (addresses P1). As a verify-before-execute gate,
                                                                                      recovery/verify-gate harnesses, and the portability study
      the zero-token verifier raises simulator-reported step-
                                                                                      (rules auto-induced on ALFWorld, 0.89 held-out).
      success for every planner (up to +0.11 for an unguarded
      Direct planner; smallest, +0.02, for SAGE, which already                                            II. R ELATED W ORK
      verifies internally) — measured by an execution signal
      the verifier never observes, so the gain is independent of                      LLM-as-planner.: SayCan [1] grounds skill selection in
      the verifier’s own score (§IV-D).                                          a learned affordance value; Inner Monologue [2] adds textual
   • The sub-goal-local edit recovers failures cheaply
                                                                                 feedback per step. ProgPrompt [3] and Code-as-Policies [4]
      (addresses P2). Under injected mid-execution failures,                     push the LLM toward program-style output. LLM+P [8]
      SAGE’s suffix-only edit recovers as reliably as whole-                        2 Code, the benchmark, the human-evaluation bundle, and an online ap-
      plan replanning (Self-Refine, ReAct, Hierarchical Few-                     pendix (online_appendix.md, all supplementary tables) are available at
      Shot) at 2.4–3.3× fewer LLM calls: it regenerates                          https://github.com/mtbui2010/sage release.
translates NL to PDDL and delegates to a classical planner;          Algorithm 1 simulate: rule-based action-gating verifica-
LLM-DP [9] maintains a symbolic world model alongside                tion.
the LLM; recent surveys [10], [11] catalogue these designs             1: σ ← σ0 , viol ← [ ]
through 2024–2025. SAGE differs by keeping the planner                 2: for t = 1 to |π| do
LLM-driven but inserting a deterministic check between plan            3:     (ok , r) ← verifyStep(at , σ)
and execution.                                                         4:     if ¬ok then
      Reasoning, refinement, and self-critique.: Chain-of-             5:         viol .APPEND((t, at , r)); break
Thought [12] elicits intermediate reasoning; ReAct [13] in-            6:     end if
terleaves thought and action; Tree-of-Thoughts [14] searches           7:     σ ← apply(at , σ)
over reasoning branches. Self-Refine [15] and Reflexion [16]           8: end for
critique with the same LLM. Concurrent 2025 work such as               9: return (viol = ∅, viol , σ)
S2 R [17] trains the self-critique via reinforcement learning,
keeping the critic inside the LLM. SAGE instead replaces the                                  III. M ETHOD
LLM critic with a zero-cost symbolic checker emitting typed             We propose SAGE, a planner for embodied LLM agents that
feedback, sidestepping the LLM self-evaluation bias.                 integrates three components into a single inference pipeline:
      Embodied planning with verification.: LLM-Planner [18]         (i) a lightweight, rule-based symbolic precondition verifier, (ii)
retrieves few-shot examples by embedding similarity. Ada-            hierarchical decomposition with sub-goal–localised repair, and
Planner [19] distinguishes in-plan refinement from out-of-           (iii) a hybrid retrieval memory seeded with curated ground-
plan replanning. ISR-LLM [20] validates LLM-emitted PDDL             truth plans and grown by successful runtime episodes.
with a classical solver. LLM-Modulo [21] generalises “LLM-              We formalise the problem (§III-A), describe each com-
generate + external-verifier”; PDDL-Instruct [22] instruction-       ponent (§III-B–§III-D), and present the planning and repair
tunes an LLM to emit PDDL with logical chain-of-thought,             algorithms (§III-E). Fig. 2 shows the full pipeline.
reporting up to 94 % planning accuracy on classical domains.
Parallel safety work in mobile robotics [23] applies safety          A. Problem formulation
filtering (control barrier functions, reference governors) at           A household task is a tuple τ = (ℓ, S0 ) where ℓ is a
the motion layer; SAGE applies an analogous check-before-            natural-language description and S0 = (o0 , V0 ) is the initial
execute discipline at the plan layer with a hand-written,            scene context: a textual observation o0 and a set of visible
vocabulary-specific verifier costing orders of magnitude less        objects V0 . A plan π = (a1 , . . . , aT ) is a sequence of
than a classical-planner verifier.                                   actions at = (verbt , objt ) drawn from a fixed vocabulary
      Memory-augmented agents.: Voyager [24] stores reusable         A (for example, {MoveTo, Find, Pick, Place, Open,
code skills; ExpeL [25] distills insights from past trajecto-        Close, TurnOn, TurnOff} plus body/idle actions); this
ries; AutoGuide [26] produces state-conditioned guidelines.          is the concrete instantiation we use, but the formulation is
SAGE’s memory is hybrid: a curated seed pool gives cold-             agnostic to its contents.
start coverage while a live pool accumulates successful plans,          Each action has a precondition pre(a) and an ef-
both surfaced via the same prompt-block format.                      fect eff(a) over a symbolic state σ with five fields:
      Hierarchical and repair-oriented planning.: HiP [27] and       arrived, found, holding, opened, on — the minimal predi-
the pyplanner Hierarchical and HierarchicalFewShot strategies        cates needed for the preconditions of A. The representa-
decompose tasks into sub-goals. DEPS [28] adds failure de-           tion is extensible: new action types contribute their own
scription + sub-goal selection in Minecraft. ReplanVLM [29]          fields. A plan is symbolically valid iff pre(at ) holds in
uses a VLM to detect failures and trigger replanning. To our         σt−1 = eff(at−1 ) ◦ · · · ◦ eff(a1 )(σ0 ) for every t. We let
knowledge SAGE is the first to (a) retain sub-goal boundaries        V(π, σ0 ) ∈ {OK} ∪ R denote the verifier verdict, where R is
at execution time and (b) restrict repair to the failed sub-goal’s   the typed set of violation reasons (e.g., N O F IND B EFORE P ICK,
suffix, preserving already-completed work and untouched fu-          P LACE W RONG L OCATION).
ture sub-goals.                                                         The planner must produce a π that is symbolically valid and
      Positioning.: Verification-based planners typically require    achieves the goal when executed in the AI2-THOR simulator.
a PDDL domain and an external classical solver (LLM+P,               We assume access only to an LLM fθ and the verifier V, not
ISR-LLM) [8], [20] or keep the critic inside the LLM                 a PDDL domain or classical planner.
(Self-Refine, Reflexion) [15], [16]; SAGE’s hand-written,
vocabulary-specific verifier needs neither and costs zero to-        B. Symbolic Action-Gating verifier
kens. Repair-oriented planners regenerate the whole remaining           The verifier is SAGE’s Action-Gating mechanism: it
plan; SAGE repairs only the failed sub-goal’s suffix. While          gates each action against the symbolic precondition state
many systems are evaluated on offline plan metrics, SAGE             before execution, a verify-before-execute discipline ad-
is grounded in simulated task-success execution. Finally, a          mitting only symbolically valid plans into the simula-
preliminary version [7] is an offline plan-quality study; this       tor. It is a deterministic function over the schema in
paper contributes the runtime verify-before-execute gate, the        pyplanner.base.STEP_SCHEMA. Critically, the verifier
sub-goal-local edit, and a leak-free empirical study of both.        never invokes an LLM: the gate V runs in O(|π|) time, costs
Algorithm 2 P LAN — SAGE initial planning.                            C. Hierarchical decomposition with sub-goal blocks
Require: task ℓ, observation o, visible objects V                        SAGE decomposes the task into 2–5 sub-goals g1 , . . . , gK
 1: E ← R ETRIEVE(M, ℓ, k)                                            via one high-level LLM call, then expands each by a second-
               decompose
 2: g1:K ← fθ            (ℓ, E)                                       level call into a contiguous block of steps π (k) . We retain
 3: σ ← (∅, ∅, ∅, ∅, ∅), V                                            the sub-goal boundaries explicitly as typed _SubgoalBlock
 4: B ← [ ]                                                           objects; the flat plan π = π (1) ∥ · · · ∥ π (K) is produced only
 5: for k = 1 to K do                                                 at execution time. SAGE’s four LLM roles use fixed system
 6:     π (k) ← fθexpand (gk , σ, E)                                  prompts, given verbatim in the online appendix.
 7:     for j = 1 to max_refines do                                      The boundaries enable sub-goal–localised repair (§III-E),
 8:         (ok , viol ) ← V(π (k) , σ)                               SAGE’s Editing mechanism: on failure it edits only the
 9:         if ok then break                                          failed sub-goal’s suffix, preserving already-completed steps
10:         end if                                                    and untouched future blocks. To our knowledge this is the
11:         π (k) ← fθrefine (gk , π (k) , viol )                     first work to combine hierarchical LLM planning with suffix-
12:     end for                                                       only repair scoped to the failed sub-goal; prior hierarchical
13:     σ                ←                  rollForward(π (k) , σ);   methods (e.g. [27], HierarchicalFewShot in pyplanner) replan
                         (k)
    B.APPEND((gk , π ))                                               the entire remainder on failure.
14: end for
15: return F LATTEN(B)                                                D. Hybrid memory retrieval
                                                                         SAGE conditions both decomposition and expansion on k
                                                                      retrieved exemplars from a hybrid store M = Mseed ∪ Mlive :
zero tokens, and gives a typed rejection reason rather than the
                                                                         • Mseed is loaded once from a curated ground-truth
free-form critique of self-refinement methods.
                                                                            file (38 simulator-verified plans), guaranteeing cold-
   The rules are hand-written (∼250 lines, LLM-free) from the               start coverage before any episode is logged. Action
AI2-THOR action ontology shipped with pyplanner (the                        names are normalised to the canonical vocabulary via
same ontology the simulator-backed reference plans satisfy),                normalize_plan before storage.
not from any observation of SAGE’s behaviour. They are                   • Mlive is appended on each successful task completion.
not ad-hoc cleverness: each rule instantiates the classical                 Persistence is a JSONL file; embedding search is optional
precondition–effect action schema of STRIPS/PDDL [30].                      via the Chroma vector store, with a Jaccard-similarity
Authoring them for a new domain is a mechanical pass over its               fallback so the system runs on a minimal install.
typed action interface: for each verb v ∈ A, list the predicates         Retrieval returns the top-k exemplars by similarity to ℓ.
its execution requires (pre) and toggles (eff), both already          Each exemplar contributes a typed (task, reasoning, plan)
declared by any discrete action API. The recipe thus transfers        triple rendered into a structured === RETRIEVED
beyond manipulation (e.g. navigation, tool use) without reward        EXAMPLE === block, the same shape used by pyplanner’s
models or expert tuning. The hand-authoring is, moreover,             HierarchicalFewShotPlanner, so the prompt
not a permanent porting cost and needs no domain expert:              engineering is shared and only the store contents differ.
the same rules are auto-inducible from logged interaction
across three ontologies, and the result is robust to rule quality     E. Algorithms
(§IV-E), so the manual pass is a one-time convenience. The               Algorithms 2 and 3 present P LAN and R EPLAN in full.
precondition_strict metric in Sec. IV is therefore an                 P LAN costs 1 + K + R LLM calls, with K sub-goals and
environment-grounded check, not a self-grading artefact: it           R ≤ K refinement passes from verifier rejection. R EPLAN
does flag violations on SAGE’s own output, and the identical          costs at most two LLM calls and never replans already-
rule set drives the heuristic precondition column in our              executed steps.
tables.                                                                     What is novel.: Each component has precedent: sym-
   Algorithm 1 sketches simulate. pre(·) is implemented as            bolic verification (LLM+P [8], ISR-LLM [20]), hierarchical
a switch over the action’s verb; the most common rules are:           decomposition (HiP [27]), and memory-augmented retrieval
                                                                      (LLM-Planner [18], ExpeL [25]). SAGE’s contribution is
  • Pick requires found ̸= ∅ and holding = ∅.                         their integration under three constraints: (i) the verifier is
  • Place r requires holding ̸= ∅ ∧ arrived = r.                      hand-written and LLM-free, costing zero tokens; (ii) repair
  • Open/Close/TurnOn/TurnOff require found = the                     is strictly local to the failed sub-goal, preserving completed
    action’s object.                                                  and untouched future work; and (iii) the memory is hybrid,
  • Container rule: PutIn c requires c ∈ opened.                      seeding curated plans and growing from successful runs, with
                                                                      a Jaccard fallback when embeddings are unavailable.
Violations are formatted into a compact natural-language
feedback block by format_violations_for_llm; §IV                                            IV. E XPERIMENTS
shows this typed feedback drives more reliable single-pass              We evaluate three claims about SAGE. (C1) Where the
refinement than the free-form critiques of Self-Refine [15].          benchmark can discriminate, SAGE’s plans are better. On
Algorithm 3 R EPLAN — sub-goal–localised suffix editing.                   qwen2.5:32b — through the same backend, varying only
Require: completed C, failed step a⋆ , reason r, blocks B                  the model identifier to guard against single-model artifacts.
    (Alg. 2)                                                               The leave-one-out completeness and compound studies use the
 1: σ ⋆ ← simulate(C).final ▷ recover state at failure, no                 four 3B–14B models (multi-seed); grounded execution and the
    LLM                                                                    safety gate, all five.
 2: (g ⋆ , B > ) ← locate(B, |C|)               ▷ which sub-goal failed;         Methods       compared.:     We      compare     SAGE
    what’s still in the future                                             against the seven baselines registered alongside it in
 3: E ← R ETRIEVE(M, g ⋆ , k)                                              pyplanner.REGISTRY: the one-shot Direct (the strongest
                repair ⋆
 4: π suf ← fθ        (g , σ ⋆ , a⋆ , r, E)                                single-call baseline), CoT [12], Few-Shot CoT [12],
 5: (ok , viol ) ← V(π suf , σ ⋆ )                                         Self-Refine [15], ReAct [13], Hierarchical, and
 6: if ¬ok then                                                            Hierarchical Few-Shot. SAGE runs with its refine-
 7:      π suf ← fθrefine (g ⋆ , π suf , viol )                            overwrite guard on by default; we also report component
 8: end if                                                                 ablations       (SAGE-NoVerifier,          SAGE-NoRepair,
 9: return π suf ∥ F LATTEN (B > )                                         SAGE-NoMemory) removing the verifier, local repair, and
                                                                           memory in turn (§IV-H).
the standard 75-task benchmark goal-completeness is satu-                        Protocol and statistics.: For memory methods we use
rated (52% of instances solved by every strong baseline), so no            a leave-one-out protocol: a test task’s own seed exemplar
method separates and SAGE merely ties — which we report                    is held out of memory, removing seed↔test leakage (non-
directly. On a harder, method-agnostic multi-goal composition,             memory baselines are leak-free by construction). The base
where headroom returns, SAGE’s completeness lead is large                  benchmark contributes n=37 held-out single-goal tasks and
and statistically significant (pooled +0.121, p < 10−4 ; signif-           the compound benchmark n=74 multi-goal tasks. The 3B–
icant on all four models under Holm–Bonferroni). (C2) SAGE                 12B models run with three seeds (averaged per task); 14B/32B
achieves higher step-level execution success than the base-                are single-seed scaling points. We report means with 95%
lines. In the AI2-THOR simulator SAGE reaches 0.71 vs. 0.60                bootstrap CIs (104 resamples) and test headline comparisons
pooled step-level success against the one-shot and hierarchical            with a paired sign-flip permutation test (2×104 permutations,
baselines, because the verifier gate removes precondition-                 p < 0.05; compound family Holm–Bonferroni corrected). Full
violating steps that abort execution (17× fewer such failures              statistics in the online appendix.
than Direct). We report goal-completeness (§IV-B) and step-                      Metrics.: We report four quantities; arrows give the
level execution success; we treat in-simulator goal-condition              good direction. completeness (↑) is plan coverage: the
success as unreliable on this benchmark (an open measurement               fraction of the task’s expected interactable objects the plan
finding, §IV-D) and do not lead with it. (C3) SAGE recovers                touches (a goal-coverage proxy in the spirit of LLM-planning
from failures more cheaply than the baselines. Editing only                benchmarks [8]). step_success (↑), our primary grounded
the failed sub-goal’s suffix lets SAGE recover from injected               metric, is the fraction of a plan’s steps the AI2-THOR sim-
mid-execution failures at 2.4–3.3× fewer LLM calls than                    ulator accepts. precondition_strict (↑) is the fraction
whole-plan replanning, at equal recovery rate. A roadmap                   of steps whose preconditions hold against the symbolic state
mapping each claim to its comparison, metric, and supporting               — a plan-validity score. llm_calls (↓) (with tokens) is
tables is given at the start of the online appendix.                       the planning/recovery cost.
A. Setup
                                                                           B. Main results — plan quality
   We ask whether grounding a small open-weight planner
with a symbolic verifier, hierarchical local repair, and memory               Under the leak-free leave-one-out protocol (full per-model
produces plans that are (i) more complete, (ii) more executable            grid in the online appendix), goal completeness on the 75-
in a simulator, and (iii) cheaper to repair after a failure,               task benchmark tells a deliberately unflattering story. We do
measured by the metrics defined below.                                     not claim a headline completeness win. Completeness is satu-
     Benchmark.: We use a 75-task AI2-THOR household                       rated: across models 52% of task-instances are already solved
set: the 38 curated, simulator-verified tasks shipped with                 (completeness = 1.0) by every strong hierarchical baseline,
pyplanner plus 37 we generate by instantiating per-scene                   leaving little headroom. SAGE ties the strongest baselines
templates and AI2-THOR-verifying each, keeping only tasks                  on the base set — in fact marginally behind Hierarchical
whose every interaction step the simulator accepts. These 37               Few-Shot on every model (0.870 vs 0.878 on qwen2.5:7b;
span four rooms (kitchen/living-room/bedroom/bathroom) and                 0.836 vs 0.858 on mistral-nemo), all within seed variance.
three difficulty tiers (14 easy / 16 medium / 7 hard), held out            This is a benchmark property, not a method one: a metric
from SAGE’s seed memory (no leakage). The compound set                     maxed on roughly half the tasks cannot separate planners.
(§IV-C) is built from these single-goal tasks.                             Easy tasks saturate for all methods while SAGE leads where
     Models.: We benchmark five open-weight Ollama mod-                    headroom remains (hard tasks: 0.811 vs 0.755 for the strongest
els over a ∼ 10× parameter range — llama3.2 (3B),                          hierarchical baseline, leak-free), so §IV-C stresses the regime
qwen2.5:7b, mistral-nemo (12B), qwen2.5:14B and                            where methods differ. The hard residual that no method solves
                              TABLE I                                           favours memory-using SAGE; the leak-free execution evidence
    G OAL COMPLETENESS ON THE HARDER MULTI - GOAL COMPOUND                      is the held-out safety-gate study (§IV-G), where the verifier
     BENCHMARK ( LEAK - FREE ). T HE BASE - SET COMPLETENESS TIE
DISAPPEARS : SAGE LEADS BY A WIDE , CONSISTENT MARGIN THAT grows                gate, not memory, drives the gain.
AS THE BASE MODEL WEAKENS , WHILE EMITTING SHORTER , MORE VALID                       (O-exec) Grounded plans execute more of their steps.:
         PLANS THAN THE VERBOSE HIERARCHICAL BASELINE .                         Step-level execution success (per-model table in the online
 Model          Direct   Hier-FS   SAGE      ∆      SAGE steps   SAGE p-valid   appendix): SAGE’s plans reach a higher fraction of accepted
 qwen2.5:7b     0.718     0.776    0.854   +0.078      12.0         0.943       steps than both the one-shot and the hierarchical baseline on
 qwen2.5:14b    0.757     0.783    0.902   +0.119      12.0         0.937
 llama3.2       0.629     0.499    0.728   +0.229      9.0          0.933       all five models, lifting the pooled mean from 0.60 (Direct) and
 mistral-nemo   0.570     0.824    0.880   +0.057      12.7         0.952       0.63 (Hierarchical) to 0.71. The mechanism is direct: SAGE’s
                                                                                verifier gate certifies every step’s preconditions before dis-
reflects a grounding gap (object-name hallucination, long-
                                                                                patch, removing at plan time the actions the simulator would
horizon coverage), not a planning-strategy one. We report
                                                                                reject mid-rollout. The failure taxonomy (online appendix)
precondition_strict only as a circular diagnostic (per-
                                                                                makes this explicit: precondition-violation failures fall from
model values in the online appendix).
                                                                                4.5% for Direct to 0.27% for SAGE (a 17× reduction), and
C. Stressing the saturated metric: harder multi-goal tasks                      SAGE’s in-simulator strict-precondition score is 0.958 versus
   The completeness tie in §IV-B is a ceiling artifact. To                      ≈ 0.86 for both baselines. The verifier suppresses the failure
recover headroom we construct a harder benchmark method-                        class it targets.
agnostically: we compose same-scene single-goal tasks into 2-                         On goal-condition success.: We do not lead with in-
and 3-goal compound tasks, de-duplicating equivalent com-                       simulator goal-condition success: it is low across all methods
positions (74 tasks; mean expected-object count 3.7 vs 2.0                      with differences that are not statistically reliable, so the avail-
in the base set); each reference plan concatenates its already                  able checkers cannot separate planners — an open measure-
simulator-verified sub-plans. The construction references noth-                 ment finding (§IV-J). For an absolute number we instead use
ing about SAGE; it lengthens the horizon and unions the goal                    a blinded, method-shuffled two-rater human evaluation (one
set, forcing a planner to cover all sub-goals.                                  author, one non-author) of a 72-item subset: SAGE leads with
   Table I reports the result. Once the ceiling is re-                          end-task success 0.53 vs. 0.40 (Direct) and 0.28 (Hierarchical),
moved, SAGE’s completeness lead re-emerges, large and                           at substantial inter-rater agreement (Cohen’s κ=0.65); the
consistent across all four models: +0.078 (qwen2.5:7b),                         zero-token partial-credit checker tracks the human consensus
+0.119 (qwen2.5:14b), +0.229 (llama3.2) and +0.057                              at Pearson r=0.82 (online appendix).
(mistral-nemo) over the strongest baseline (Hierarchical                              Failure recovery: equal reliability, far lower cost.: We
Few-Shot). The advantage is one of brevity and validity, not                    inject one mid-execution failure per task and measure recovery
per-step grounding: SAGE reaches higher coverage with fewer                     cost (details in the online appendix). Recovery rate saturates
steps (Hierarchical Few-Shot averages 17.8 vs SAGE’s 12.0                       (100% for every method here), so cost discriminates. On held-
on qwen2.5:7b; Table I) and higher precondition validity                        out tasks SAGE recovers in 1.18 LLM calls versus 2.87–
(0.94 vs 0.89), while its per-step hallucination rate (fraction                 3.71 for whole-plan replanners (Hier. Few-Shot, Self-Refine,
of steps whose object is absent from the visible set) matches                   ReAct): a 2.4–3.1× reduction at equal reliability and lowest
the baseline (0.53 vs 0.55). The baseline covers the same sub-                  latency, because the edit regenerates only the failed sub-
goals only by emitting many more steps; SAGE does so with                       goal’s suffix (+1.7 to +2.5 fewer calls vs. every baseline, all
a shorter, precondition-valid plan. The advantage is largest for                p < 10−4 ). On compound tasks the gap widens to 2.6–3.3×
the weakest model, where naive planners bloat and drift.                        (up to 3.7× lower latency): a global 2.4–3.3× envelope.
      Significance.: The gain over Hierarchical Few-Shot is
                                                                                E. Generalization to unseen environments
significant (paired sign-flip permutation, 20k permutations):
all four models reach p < 0.05 and survive Holm–Bonferroni                         A standing objection to a symbolic-verifier method is that
(per-model values in the online appendix). Pooled over                          both the 38 curated scenes and the hand-written rules overfit
296 instances the mean gain is +0.121 (95% bootstrap CI                         iTHOR. We address this with out-of-distribution studies that
[+0.092, +0.150], p < 10−4 ). Unlike the saturated base                         change nothing in SAGE — identical prompts, seed memory,
benchmark the metric here discriminates, and the advantage                      and verifier code.
is no leakage artifact: the harder tasks are a method-agnostic                       Unseen procedurally-generated houses.: On 70 unseen
composition under the same leave-one-out protocol.                              ProcTHOR houses, SAGE retains its strict-precondition lead
                                                                                (0.985): plan validity transfers to never-seen layouts (full table
D. Grounded execution in AI2-THOR                                               in the online appendix).
   Offline metrics are proxies, so we execute every plan in AI2-                     Portability: the verifier’s rules are inducible from data.:
THOR through a ZMQ action server (up to max_replan=2                            The hand-written verifier (∼250 lines) is not arbitrary tuning:
repair rounds), recording per step whether the simulator ac-                    a probe-based pipeline that mines the conjunctive precondition
cepts the interaction. We run {Direct, Hierarchical,                            per action from (state, action, success) transitions (zero manual
SAGE} on all five models over the 38 simulator-verified GT                      rules) recovers it in-domain (iTHOR, 14/16 rules), on unseen
tasks. These tasks overlap the seed memory, so this comparison                  ProcTHOR (13/16), and on text-domain ALFWorld (0.89
held-out), so porting the monitor to a new action distribution    and SAGE-NoMemory loses cold-start coverage. We state
needs interaction data, not fresh authoring. The result is also   the cost directly: SAGE spends roughly 7× the tokens of
robust to rule quality: random rule deletion degrades the gate    one-shot Direct, comparable to the most expensive baseline
smoothly and the non-expert induced set matches the hand-         (Hierarchical Few-Shot), not cheap in absolute terms. Its
written one (online appendix).                                    efficiency claim is narrow: at recovery time, repair scoped
     Published baselines.: Against LLM+P [8] and a Say-           to a single sub-goal costs 2.4–3.3× fewer LLM calls than
Can-style decoder [1], both produce valid but incomplete plans    whole-plan replanning — not a general token-cost advantage.
(completeness 0.61–0.77) whereas SAGE reaches 0.87–0.88
on the same models (online appendix).                             I. On-device deployment: where the zero-token gate matters
                                                                  most
F. External validation: EAI VirtualHome                              The safety gate matters most where compute is scarcest. The
  To rule out that SAGE’s gains are an artifact of its own        small (3–7B) open-weight models an embodied agent can run
verifier’s metrics, we evaluate on the independent Embodied       on-board (when a cloud LLM is unavailable, too costly, or
Agent Interface (EAI) VirtualHome benchmark [31], scored          disallowed) are also the ones that emit the most precondition-
by EAI’s own transition model. Without changing any SAGE          violating actions for the gate to block (§IV-G) — and the
code, we compare verifier-on against SAGE-NoVerifier              verifier, calling no model, is the cheap half of that trade. We
over 305 tasks, three seeds (per-model table in the online        confirm this on real edge silicon: an NVIDIA Jetson AGX
appendix). Two effects are robust. The verifier removes re-       Orin (64 GB, JetPack 6, CUDA 12.6, MAXN) serving 4-bit
dundant steps on every model (−2.7 to −7.4 points, largest        (Q4 K M) models on-board with Ollama, AI2-THOR on a
on the strongest — third-party evidence for the brevity-and-      host (planner-on-edge, sim-on-host). Three findings (table in
validity mechanism of §IV-C), and lifts executability for the     the online appendix). (i) The gate is free on-board: the
small open models (+3.6/+3.7 on 7B/3B) but saturates on           verifier adds a measured 0.008 ms per plan (median; 0.017 ms
14B (−1.5). Correctness is unchanged: the gate improves plan      max, O(|π|), no tokens), six orders of magnitude below
validity, not goal grounding.                                     the multi-second on-device LLM latency. (ii) No quality
                                                                  loss: on a balanced 20-task subset (seed 0), on-board plan
G. Runtime safety monitor: blocking erroneous actions before      quality matches the server within seed variance and SAGE’s
actuation                                                         completeness lift over an unguarded planner reproduces on-
   An LLM planner that emits a precondition-violating step        board (+0.12/ + 0.16/ + 0.13 for 3B/7B/14B). (iii) Feasible:
— Pick before the object is localized, Place into a closed        even 14B runs in 27 GB at 48 W. The component that helps
receptacle — will, without a check, send that action to the       small models most is thus essentially free on the edge — a
robot. Because the verifier is LLM-free it can run online as      deployable, cloud-free safety layer for the on-board planners
a verify-before-execute guard: before a step is dispatched we     that need it most, and a partial mitigation of L1 (decision-
check it against the symbolic state and, if it would violate      making on real edge hardware, execution still simulated).
a precondition, repair the sub-goal before the action is taken
rather than execute-then-recover after the actuator has already   J. Limitations
moved. This is the safety contribution: across four models           (L1) Simulation only. All execution is in AI2-THOR (no
on the 38 grounded tasks the gate blocks 206 precondition-        real-robot claim; an xArm evaluation is future work), though
violating actions before they reach the actuator (per-method      we do run the planner on edge hardware (§IV-I), a partial
gate-off/on in the online appendix) — erroneous commands          mitigation. (L2) Saturated base metric. Base-benchmark com-
that the execute-then-replan baseline would have physically       pleteness saturates (52% ceiling) and cannot separate methods;
attempted. The benefit on simulator-reported step-success is      we report the tie and locate our gains on the harder compound
independent of the verifier and, as a safety layer should, con-   benchmark, recovery cost, and the safety gate. (L2b) Checker-
centrates on the planners that emit the most unsafe steps: for    based end-task success is unreliable. Both in-simulator goal-
the unguarded Direct planner the gate raises step-success by      condition checkers fail (online appendix); we therefore obtain
+0.107 (p < 10−4 ); for planners already embedding structure      the absolute end-task number from a blinded two-rater human
the effect is smaller and not significant (CoT +0.081, p=0.09;    evaluation (72 items, κ=0.65; online appendix) rather than an
Hier +0.041; SAGE +0.016, both n.s.), as expected — they          automated checker. (L3) Hand-written verifier. The deployed
emit fewer violations to catch. We therefore claim the gate       verifier is hand-authored (∼250 lines); porting needs re-
as a deployable, zero-token safety layer that prevents unsafe     authoring or rule induction (§IV-E), not a full PDDL domain.
actuation for unverified planners, not a universal accuracy       (L4) Baseline asymmetries. SayCan uses our verifier as its
boost.                                                            affordance filter (strict-precondition 1.0 by construction); the
                                                                  ALFWorld result is a verifier-portability study, as the planners’
H. Ablations and cost                                             vocabulary (clean/heat/cool) is not yet adapted there. (L5)
  Removing any single component degrades SAGE:                    Residual hallucination. All methods, SAGE included, still
SAGE-NoVerifier loses the strict-precondition guarantee,          reference absent objects on some steps — a shared small-
SAGE-NoRepair cannot recover from injected failures,              model weakness. (L6) Execution subset. The expensive AI2-
THOR execution covers a representative method subset, not                   [3] I. Singh et al., “ProgPrompt: Generating Situated Robot Task Plans using
all seven baselines. (L7) ALFWorld floored. On ALFWorld                         Large Language Models,” in IEEE International Conference on Robotics
                                                                                and Automation (ICRA), 2023.
step-executability saturates at 1.0 while end-task success floors           [4] J. Liang et al., “Code as Policies: Language Model Programs for
(≤ 0.04): long-horizon ALFRED goals are out of reach for a                      Embodied Control,” in IEEE International Conference on Robotics and
                                                                                Automation (ICRA), 2023.
7B planner without fine-tuning, so no method separates. (L8)                [5] M. Shridhar et al., “ALFWorld: Aligning Text and Embodied Environ-
Model-dependent gate benefit. The gate’s executability gain is                  ments for Interactive Learning,” in International Conference on Learning
                                                                                Representations (ICLR), 2021.
regime-specific (§IV-F): largest for small models, saturating               [6] E. Kolve et al., “AI2-THOR: An Interactive 3D Environment for Visual
on the strongest, so we scope the claim to that regime.                         AI,” 2017, arXiv:1712.05474.
                                                                            [7] “Grace: Lightweight symbolic verification and local repair for llm task
                                                                                planning in embodied agents.”
                        V. C ONCLUSION                                      [8] B. Liu et al., “LLM+P: Empowering Large Language Models with
                                                                                Optimal Planning Proficiency,” 2023, arXiv:2304.11477.
   We presented SAGE, a planner for embodied LLM agents                     [9] G. Dagan et al., “Dynamic Planning with a Large Language Model,”
that couples symbolic action-gating (a rule-based precondition                  2023, arXiv:2308.06039.
                                                                           [10] D.-S. Jang et al., “Unlocking Robotic Autonomy: A Survey on the
verifier applied as a verify-before-execute monitor) with sub-                  Applications of Foundation Models,” International Journal of Control,
goal–localised editing, supported by hierarchical decomposi-                    Automation, and Systems (IJCAS), 2024.
                                                                           [11] S. Bian et al., “Large Language Model-Based Task Planning for Service
tion and a hybrid memory store. The components are indi-                        Robots: A Review,” arXiv preprint arXiv:2510.23357, 2025.
                                                                           [12] J. Wei et al., “Chain-of-Thought Prompting Elicits Reasoning in Large
vidually lightweight: the gate is ∼250 lines of deterministic                   Language Models,” in Advances in Neural Information Processing
Python, the edit is restricted to the suffix of a single sub-                   Systems (NeurIPS), 2022.
goal, and the memory store falls back to a Jaccard retriever               [13] S. Yao et al., “ReAct: Synergizing Reasoning and Acting in Language
                                                                                Models,” in International Conference on Learning Representations
when embeddings are unavailable. Their integration yields                       (ICLR), 2023.
a planner whose advantages we report only where the data                   [14] ——, “Tree of Thoughts: Deliberate Problem Solving with Large Lan-
                                                                                guage Models,” in Advances in Neural Information Processing Systems
supports them. Under a leak-free leave-one-out protocol over                    (NeurIPS), 2023.
four open-weight models, goal-completeness on the standard                 [15] A. Madaan et al., “Self-Refine: Iterative Refinement with Self-
                                                                                Feedback,” in Advances in Neural Information Processing Systems
benchmark is saturated and SAGE ties the strongest baselines.                   (NeurIPS), 2023.
Where the benchmark can discriminate, the advantage is                     [16] N. Shinn et al., “Reflexion: Language Agents with Verbal Reinforcement
                                                                                Learning,” in Advances in Neural Information Processing Systems
real and statistically significant: on a harder, method-agnostic                (NeurIPS), 2023.
multi-goal benchmark SAGE improves completeness by a                       [17] R. Ma et al., “S2R: Teaching LLMs to Self-verify and Self-correct via
                                                                                Reinforcement Learning,” in Proceedings of the 63rd Annual Meeting
pooled +0.121 (p < 10−4 , significant on all four models                        of the Association for Computational Linguistics (ACL), 2025.
under Holm–Bonferroni, Sec. IV-C); in grounded AI2-THOR                    [18] C. H. Song et al., “LLM-Planner: Few-Shot Grounded Planning for
                                                                                Embodied Agents with Large Language Models,” in IEEE/CVF Inter-
execution SAGE attains higher step-level success (0.71 vs.                      national Conference on Computer Vision (ICCV), 2023.
0.60 pooled, Sec. IV-D); we report step- rather than end-task              [19] H. Sun et al., “AdaPlanner: Adaptive Planning from Feedback with
                                                                                Language Models,” in Advances in Neural Information Processing
success because the available goal checkers are unreliable, an                  Systems (NeurIPS), 2023.
open measurement finding. As a verify-before-execute gate the              [20] Z. Zhou et al., “ISR-LLM: Iterative Self-Refined Large Language Model
                                                                                for Long-Horizon Sequential Task Planning,” in IEEE International
same check blocks 206 unsafe actions before actuation and                       Conference on Robotics and Automation (ICRA), 2024.
raises an unverified Direct planner’s simulator step-success               [21] S. Kambhampati et al., “Position: LLMs Can’t Plan, But Can Help
                                                                                Planning in LLM-Modulo Frameworks,” in International Conference on
by +0.107 (p < 10−4 ), an independent, non-circular safety                      Machine Learning (ICML), 2024.
result. Because the gate calls no model (0.008 ms/plan), this              [22] P. Verma et al., “Teaching LLMs to Plan: Logical Chain-of-
                                                                                Thought Instruction Tuning for Symbolic Planning,” arXiv preprint
safety layer runs essentially free on-board: SAGE planning                      arXiv:2509.13351, 2025.
reproduces its quality on a Jetson AGX Orin (Sec. IV-I),                   [23] S. Hwang et al., “Safe Motion Planning and Control for Mobile Robots:
                                                                                A Survey,” International Journal of Control, Automation, and Systems
exactly where small-model verification helps most.                              (IJCAS), 2024.
   On cost, SAGE spends ∼ 7× the tokens of a one-shot                      [24] G. Wang et al., “Voyager: An Open-Ended Embodied Agent with
                                                                                Large Language Models,” Transactions on Machine Learning Research
baseline, comparable to the most expensive baseline; its ef-                    (TMLR), 2024.
ficiency claim is narrow, at recovery time, where sub-goal–                [25] A. Zhao et al., “ExpeL: LLM Agents Are Experiential Learners,” in
                                                                                Proceedings of the AAAI Conference on Artificial Intelligence, 2024.
local editing costs 2.4–3.3× fewer LLM calls than whole-plan               [26] Y. Fu et al., “AutoGuide: Automated Generation and Selection of
replanning. The dominant residual failure is object-naming                      Context-Aware Guidelines for Large Language Model Agents,” in Ad-
                                                                                vances in Neural Information Processing Systems (NeurIPS), 2024.
ambiguity (§IV-J), orthogonal to planning strategy, motivating             [27] A. Ajay et al., “Compositional Foundation Models for Hierarchical Plan-
future grounding of the action vocabulary in vision-language                    ning,” in Advances in Neural Information Processing Systems (NeurIPS),
                                                                                2023.
embeddings.                                                                [28] Z. Wang et al., “Describe, Explain, Plan and Select: Interactive Planning
      Reproducibility.: SAGE ships as a self-contained pyplan-                  with Large Language Models Enables Open-World Multi-Task Agents,”
                                                                                in Advances in Neural Information Processing Systems (NeurIPS), 2023.
ner strategy (REGISTRY["SAGE"]) with the verifier, hybrid                  [29] A. Mei et al., “ReplanVLM: Replanning Robotic Tasks with Visual
retriever, and all benchmark scripts; the simulator-verified 75-                Language Models,” IEEE Robotics and Automation Letters (RA-L),
                                                                                2024.
task AI2-THOR set is released with the artifact.                           [30] R. E. Fikes and N. J. Nilsson, “STRIPS: A new approach to the appli-
                                                                                cation of theorem proving to problem solving,” Artificial Intelligence,
                           R EFERENCES                                          vol. 2, no. 3–4, pp. 189–208, 1971.
                                                                           [31] M. Li et al., “Embodied Agent Interface: Benchmarking Large Lan-
 [1] M. Ahn et al., “Do As I Can, Not As I Say: Grounding Language in           guage Models for Embodied Decision Making,” in Advances in Neural
     Robotic Affordances,” in Conference on Robot Learning (CoRL), 2022.        Information Processing Systems (NeurIPS), Datasets and Benchmarks
 [2] W. Huang et al., “Inner Monologue: Embodied Reasoning through
     Planning with Language Models,” in Conference on Robot Learning            Track, 2024.
     (CoRL), 2022.
