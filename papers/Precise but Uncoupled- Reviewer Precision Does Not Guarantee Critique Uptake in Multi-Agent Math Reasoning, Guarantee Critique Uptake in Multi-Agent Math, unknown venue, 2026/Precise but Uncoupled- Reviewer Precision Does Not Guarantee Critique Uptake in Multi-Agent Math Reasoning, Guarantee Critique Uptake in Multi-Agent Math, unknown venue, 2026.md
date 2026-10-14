                                          Precise but Uncoupled: Reviewer Precision Does Not
                                           Guarantee Critique Uptake in Multi-Agent Math
                                                              Reasoning


                                                 Chih-Hsuan Yang∗                        Jingyan Jiang                   Vikram Vasudevan
                                             Argonne National Laboratory           Argonne National Laboratory          Oregon State University

                                               Cheng-Hau Yang                         Huihuo Zheng                          Le Chen
                                           Argonne National Laboratory          Argonne National Laboratory        Argonne National Laboratory

                                                Eliu A. Huerta                   Venkatram Vishwanath                    Ian T. Foster
                                           Argonne National Laboratory          Argonne National Laboratory        Argonne National Laboratory
arXiv:2607.15388v1 [cs.AI] 16 Jul 2026




                                              University of Chicago                                                   University of Chicago

                                                                                     Rajeev Thakur
                                                                                Argonne National Laboratory



                                                                                          Abstract

                                                     Many recent math- and science-oriented agent systems adopt hierarchical designs
                                                     with specialized reviewer roles, motivated by the idea that routing critique through
                                                     a dedicated review stage should help turn wrong candidates into correct ones on
                                                     hard problems. We study that expectation on 4,181 verifier-grounded Omni-MATH
                                                     problems [7, 2], a hard ten-tier benchmark with enough headroom to separate
                                                     protocols, using matched gpt-oss-120b actors as the primary actor family. On
                                                     tiers 1–2, multi-agent collaboration adds at most about 2 percentage points over
                                                     the matched single-agent baseline. From tier 4 onward, the gains open sharply,
                                                     reaching about 10 to 20 percentage points on tiers 6–9. In that regime, broadcast-
                                                     style peer discussion attains higher final accuracy than a planner–executor–reviewer
                                                     pipeline (PER). We use that divergence as a starting observation and ask when
                                                     reviewer quality translates into effective solver updates. On this benchmark, the
                                                     PER–broadcast accuracy gap is not accounted for by reviewer precision alone.
                                                     Here reviewer precision asks how often a reviewer warning truly points to a real
                                                     error. PER’s reviewer has higher precision (0.861 vs. 0.644), yet correct critique
                                                     is much less likely to change the next candidate the protocol carries forward, and
                                                     reviewer-guided repair is correspondingly lower. These results show that reviewer
                                                     detection quality and critique uptake are empirically separable. Within matched
                                                     PER interventions, forcing explicit acknowledgment lowers final accuracy instead
                                                     of improving follow-through, while placing reviewer guidance directly in the
                                                     solver’s working context partially improves follow-through without closing the gap.
                                                     Taken together, these interventions point in the same direction: critique appears
                                                     more likely to be acted upon when it is presented more directly in the solver’s
                                                     working context, although this evidence is directional rather than causal. Under
                                                     reviewer-centric evaluation, a system can look strong at spotting errors yet still fail
                                                     to solve more problems if the protocol does not act on those critiques.

                                            ∗ Corresponding author: bellayang@anl.gov.




                                         Preprint.
    PER: critique is routed, but can remain non- Broadcast: critique is shared, and approval is
    binding                                      collective
    Planner → Executor → Reviewer                               Peer discussion ↔ shared candidate
    Reviewer signal enters a separable advice field             Critique enters the shared deliberation state
    Solver can acknowledge the signal yet preserve the          Every peer sees the same candidate before submis-
    candidate                                                   sion
    Submission decision is role-local after routed review       Submission requires collective re-approval

Figure 1: Why reviewer quality and realized repair can diverge. In PER, information flow and decision
flow can separate: a reviewer can send a correct warning without changing the next candidate. In
broadcast, critique is embedded in shared candidate state and group approval, making bypass harder
by design.


1     Introduction

A common design choice: use a specialized reviewer. Recent work on LLM reasoning has moved
from single-chain prompting toward richer inference-time systems with multiple interacting calls,
branches, or agents [6, 30, 13, 25, 35]. Within that broader landscape, open peer deliberation—that
is, agents publicly critiquing and revising a shared candidate—remains influential [6, 29], but many
recent math- and science-oriented systems adopt hierarchical designs with specialized reviewer roles.
MALT [18] decomposes reasoning into generator, verifier, and refinement agents trained end-to-end;
DPSDP [34] trains an actor–critic pair through reinforcement learning; and recent surveys and scaling
analyses argue that role heterogeneity can be a primary source of multi-agent gains [22, 11, 9]. A
common operational expectation in these systems is that routing critique through a dedicated review
stage should improve repair—that is, convert a wrong candidate into a correct one—on hard problems.
We refer to that more specific expectation as the role-specialization hypothesis: when critique matters,
separating reviewer and solver roles should improve repair.

A hidden failure mode: reviewer–solver coupling. That expectation leaves out a second question.
A reviewer can detect an error correctly, and the downstream solver can still fail to act on that critique.
Throughout the paper, solver means the role that produces the next candidate answer; in PER this
is the Executor role. We call the resulting failure reviewer–solver decoupling. This failure mode
remains hard to detect if evaluation reports only final pass rate or reviewer precision [8, 24, 14, 3]. We
make that failure visible by separating reviewer quality from solver response: on evaluator-verified
useful critique, does the next candidate change, and does that change lead to repair?

Main finding. We evaluate four protocols on 4,181 problems from the Omni-MATH benchmark
family [7, 2], an olympiad-level setting where substantial headroom remains under current frontier
models [7, 2]. On the easiest tiers, collaboration adds little. Once the benchmark becomes hard
enough for collaboration to matter, however, the two collaborative designs begin to diverge: broadcast
achieves higher final accuracy than PER. We treat that divergence as the starting point for a process
analysis: does the gap reflect reviewer quality, or does useful critique fail to reach the solver’s next
candidate? On reviewer detection, PER’s reviewer has higher precision than broadcast’s (0.861
vs. 0.644). On reviewer-to-action uptake, however, the ordering reverses: when the reviewer gives
critique that the evaluator later confirms as useful, the protocol changes its carried-forward candidate
only 33.6% of the time in PER versus 93.5% in broadcast, and ReviewerGuidedRepairRate is 0.051
versus 0.286. Under this evaluation, the PER–broadcast accuracy gap is therefore not accounted for
by reviewer precision alone and is instead consistent with differences in critique uptake.
Relative to the matched single-agent iterative baseline, the collaboration gains open sharply from
tier 4 onward. We track that gap with three primary diagnostics: whether useful critique is ignored
(NeglectRate), whether the next answer changes (CouplingRate), and whether that change repairs
the problem (ReviewerGuidedRepairRate). Within PER, ACK-required is a failed compliance-style
control. EMB, which presents reviewer guidance directly in the solver’s working context, recovers
only part of the PER–broadcast gap, as does a deeper-reflection variant. We treat the within-PER
probes as directional support for this pattern, not as isolated causal proof.


                                                            2
Why Omni-MATH? On standard easy math benchmarks, strong systems are already close to
ceiling, so it is harder to tell whether collaboration is helping. Omni-MATH gives this paper room to
separate protocols: it contains 4,181 competition-level problems, remains far from saturated under
current evaluations, and supplies ten benchmark-defined difficulty tiers rather than a scale tuned to
one model family [7, 2].

The single-agent anchor. We read the tier curves relative to Single-Agent Iterative, which is the
paper’s matched non-collaborative anchor. The single-agent baseline already has iterative opportunity
and verifier interaction, so gain over Single-Agent isolates what deliberation and review add rather
than mixing collaboration with the value of simply getting more attempts.

Scope of the claim. This is a test-time study: we keep the underlying model family fixed and vary
the protocol used at inference time, including role structure, feedback routing, and retry behavior. Our
claim is not that one protocol universally wins, nor that PER–broadcast alone isolates a single causal
variable. The PER–broadcast comparison is evidence about complete protocol designs that differ in
shared state, approval rules, and discussion structure. Within that comparison, reviewer precision
and critique uptake can separate sharply under a common PER-style reviewer-to-solver interface;
the within-PER probes provide more limited direction-of-change evidence on how feedback delivery
relates to the uptake gap. The appendix carries the fuller recovery, cost, and protocol-control details:
a cross-evaluator disagreement replay, a higher-cost PER-inner6 stress test, and a reduced cross-
family replication with Gemma 3 actors in which the overall ranking shifts but the precision–uptake
separation persists, suggesting that uptake is an important evaluation axis rather than a complete
account of protocol quality.

Contributions.    We make four integrated contributions:

1. Finding. In this matched benchmark/model regime, hierarchical PER attains lower repair and
   lower final accuracy than broadcast even though PER’s reviewer has higher precision; the clearest
   observable difference is much lower uptake of useful critique.
2. Interventions. Within-PER probes that hold the model family, reviewer backbone, and budget
   fixed provide directional evidence consistent with the interface story: ACK-required is a failed
   compliance control, and EMB partially recovers the gap by placing reviewer guidance directly in
   the solver’s working context.
3. Measurement. We introduce a measurement framework that separates within-attempt review
   from verifier-guided repair, together with coupling-sensitive metrics that make detection, uptake,
   and realized repair measurable under matched protocol comparisons.
4. Implications. The same analysis shifts evaluation away from reviewer quality alone and toward
   whether the protocol acts on critique, while the appendix gives a verifier-cost-aware deployment
   view for this benchmark regime rather than a universal protocol winner.

2   Related Work
Inference-time structure and multi-agent reasoning. Prior work shows that reasoning can im-
prove when inference is given more structure, whether through deliberate reasoning traces, branching
search, or multi-agent interaction [28, 27, 32, 6, 30, 13]. Within multi-agent systems, open peer
deliberation remains influential, but recent math- and science-oriented systems often move toward
specialized or hierarchical role assignments [18, 34, 22, 11, 9]. Our paper focuses on one narrow
question inside that trend: when a system includes a specialized reviewer, should reviewer quality
alone predict whether collaboration helps?

Collaboration value. Recent agent evaluations also make a broader point: adding interaction or
extra agents is not useful by itself unless collaboration improves outcomes relative to a matched
non-collaborative baseline, and does so at acceptable coordination or verifier cost [15, 9, 11]. Our
paper adopts that lens directly. We compare collaborative protocols not only by absolute accuracy, but
also by gain over Single-Agent Iterative, which already has retry opportunity and verifier interaction.
This lets us ask not only whether a protocol solves more problems, but whether deliberation itself
adds value and through which stage that value is realized.


                                                   3
Self-correction, verifier-guided repair, and separable stages. A separate line of work shows
that detection, revision, and successful repair are not the same event [16, 23, 24, 1, 8, 14]. These
results are important because they move evaluation away from the assumption that noticing an error
is already most of the work. We extend that logic to a multi-agent reviewer-to-solver interface: a
reviewer can identify a valid problem, yet the downstream solver can still fail to turn that critique into
a better next candidate.

Process-aware evaluation. Recent evaluation work also argues that answer-only metrics miss
important process differences, especially in agent systems where interaction, cost, and evaluator
design matter [19, 15, 9]. Our contribution is narrower than a benchmark or taxonomy paper. We
focus on evaluator-verified useful critique and ask three linked questions: was the critique right, did
it change the next candidate, and did that change repair the problem? Appendix G gives the fuller
literature map and term lineage.

3     Task Setting and Evaluation
3.1   Benchmark: Omni-MATH 2

We use Omni-MATH 2 [2], a cleaned and filtered version of Omni-MATH [7]. Our filtered corpus
contains 4,181 competition-level mathematics problems organized into ten benchmark-provided
difficulty tiers, with tier 10 the hardest. Each problem includes evaluator-usable final answers
and reference material, which lets us study verifier-grounded recovery rather than free-form judge
preferences.
This benchmark is useful here for two reasons. First, it remains far from saturated under current
evaluations [7, 2], so protocol differences still have room to appear on both first-pass and multi-
attempt outcomes. Second, the benchmark-provided tier structure lets us ask where collaboration
matters, not only whether one protocol has the highest aggregate score. We therefore use Omni-
MATH not as a generic math benchmark, but as a hard setting in which reviewer precision, critique
uptake, and verifier-guided repair can separate. Tier counts and broader literature context are deferred
to Appendix J and Appendix O.

3.2   Task Setting

We study verifier-gated mathematical reasoning on exact-answer or equivalence-checkable olympiad
problems [7, 2]. A protocol may deliberate internally, submit a final answer, receive evaluator
feedback, and optionally retry under a fixed outer-loop budget. Throughout the paper, protocol
means the full interaction procedure: agent roles, communication topology, revision policy, evaluator-
submission rule, and feedback-routing rule.
This paper separates two stages that are easy to conflate if we look only at final accuracy. The first
stage is within-attempt review: before any external verdict, agents may critique a current candidate
and revise it. The second stage is verifier-guided retry: after a failed submission, the protocol may
use evaluator feedback to attempt recovery on a later outer-loop attempt. That distinction matters
because a protocol can appear strong for different reasons: it can produce better first-pass candidates,
recover better after failure, or spend substantially more verifier interaction to reach the same endpoint.
The main paper therefore keeps outcomes, review-to-action transitions, and verifier burden separate.

3.3   Compared Protocols

We compare four protocols arranged as a ladder from no collaboration to open peer deliberation.
Baseline LLM is a direct one-shot solver with no iterative repair memory and no explicit interaction.
Single-Agent Iterative uses the same base model but allows repeated outer-loop attempts with
question-scoped failure and candidate-revision memory, without introducing a separate reviewer. Our
structured role-based MAS instantiates a Planner–Executor–Reviewer pipeline (PER): the planner
decomposes the problem, the executor produces the next candidate answer, and the reviewer decides
whether that candidate is ready for evaluator submission or should be sent back for revision. In later
sections we use solver as the name for this candidate-producing role. Finally, broadcast deliberation
uses three peers in a hybrid interaction pattern: confidence polling allocates one public speaker at a


                                                    4
time during discussion, but once a current candidate exists, all three peers enter an approval phase
that can approve, reject, or revise that candidate before submission; under our matched configuration,
submission requires unanimous approval [6, 30, 13, 25].
These four protocols let us separate three things that are often mixed together in agent papers: the
value of getting more attempts, the value of adding a specialized reviewer, and the value of making
critique part of a shared deliberation state. PER and broadcast instantiate two common design patterns:
role-specialized review pipelines and shared-state peer deliberation. PER routes reviewer feedback as
a separable signal inside a hierarchical pipeline, whereas broadcast embeds critique inside shared
peer context and treats the current candidate as protocol-level state.

3.4   Metrics, Controls, and Evaluator

The paper keeps three kinds of quantity in view. Outcome asks whether the protocol solves the
problem. Mechanism asks what happened between critique and the next candidate. Verifier burden
asks how much external feedback the protocol consumes to get there. We summarize outcomes
with FinalPassRate and Pass@1. We summarize mechanism with NeglectRate, CouplingRate, and
ReviewerGuidedRepairRate, which follow the chain detection → uptake → repair: did the reviewer
correctly flag a real problem, did that critique change the solver’s next candidate, and did the change
actually fix the problem? We track verifier burden with AvgEvalCalls/problem, the average number
of evaluator (verifier) calls per problem, because protocol differences in recovery and coordination
can shift verifier cost even when token cost rises more slowly. CouplingRate is evaluator-grounded
because it is computed only on evaluator-verified useful revise episodes. It is an operational answer-
transition statistic, not a semantic measure of reasoning alignment: it asks whether reviewer feedback
changes the next candidate the protocol actually carries forward, which is a necessary but not
sufficient condition for critique utilization. In that sense it is a protocol-level uptake or binding metric:
under broadcast, uptake can be realized through shared candidate updates and collective re-approval,
whereas under PER it depends more on routed reviewer-to-solver follow-through. Appendix H gives
the exact definition together with deterministic normalization and equivalence-aware audits, and
shows that the observed uptake gap is stable under those alternative answer-change definitions.
Across the matched configurations, all acting agents and the evaluator use gpt-oss-120b2 , a
public open-weight reasoning model, served through public GPU-backed HPC infrastructure via
an OpenAI-compatible server, with temperature 0 throughout. We also hold the evaluator contract,
outer-loop budget, and memory reset policy fixed across protocols. Even with those controls, PER and
broadcast still differ in how the full system operates: who can see the current candidate, how agents
communicate, how discussion proceeds, and who must approve before submission. We therefore
use the PER–broadcast comparison as evidence about whole protocol designs, not as an isolation
of one factor at a time. More targeted direction-of-change evidence comes from the within-PER
probes. As a robustness check, Appendix B replays all saved submitted answers with two other open
evaluators under the same prompt/parser; pairwise disagreement remains low on the full benchmark
(3.38%–5.76%; κ = 0.850–0.915), where κ denotes Cohen’s chance-corrected agreement coefficient
[5]. That range is generally read as strong agreement [12, 17], so we treat the replay as trustworthy
as a robustness check rather than as a replacement judge; disagreement rises mainly on the hard
collaborative slice where answer equivalence is most brittle.
To probe the reviewer-to-solver interface more directly, we also test two full-benchmark PER variants
while holding the model family, reviewer setup, and outer-loop budget fixed. ACK-required adds
mandatory verbal acknowledgment of critique while keeping routed advice unchanged; EMB places
reviewer guidance directly in the solver working context. Appendix I.3 gives the exact interface
changes.


4     Results

We organize the evaluation around four questions: outcomes over a matched single-agent baseline
(RQ1), post-failure recovery (RQ2), whether the PER–broadcast accuracy gap is better explained by
   2 Specifically, the public OpenAI checkpoint openai/gpt-oss-120b, released under Apache 2.0 and downloadable

from https://huggingface.co/openai/gpt-oss-120b; see the official release and model documentation in OpenAI
[21, 20].


                                                      5
Table 1: Overall outcome and cost comparison over N = 4,181 problems. FinalPassRate and Pass@1
are computed over all problems, not averaged by tier. Pass@1 is the fraction of problems solved
on the first submitted attempt, so across protocols it reflects each protocol’s own pre-submission
deliberation budget rather than a compute-matched one-step score. “Tokens per Extra Solve” means
the average number of generated tokens required to solve one additional problem relative to Baseline
LLM, the one-shot entry point for the overall cost ladder; tier-level collaboration gains elsewhere are
reported relative to Single-Agent Iterative. “Average evaluator calls” means the average number of
evaluator (verifier) calls per problem. Appendix Figure 19 gives a fuller multi-metric view.
 Protocol                  FinalPassRate   Pass@1   Avg. Tokens   Tokens per Extra Solve   Avg. Evaluator Calls
 Baseline LLM (one-shot)      56.8%        56.8%       18,385              —                      1.00
 Single-Agent Iterative       78.8%        57.4%      48,123             135K                     1.69
 PER (role-based MAS)         85.2%        72.8%     400,351             1.34M                    2.19
 Broadcast deliberation       89.2%        78.6%     616,499             1.84M                    1.35



reviewer detection quality or critique uptake (RQ3), and how protocol choice changes when verifier
calls are cheap or expensive (RQ4).

4.1   Outcomes, Cost, and Recovery

Across all 4,181 Omni-MATH problems, the three multi-step protocols substantially exceed the
one-shot baseline. Within this matched setting, broadcast achieves the highest FinalPassRate and
Pass@1, followed by PER and then the single-agent iterative baseline (Table 1). We treat that ranking
as the starting observation for the process analysis below, not as a universal verdict on protocol
design.
Omni-MATH defines these ten tiers independently of the models we evaluate, so the clearer tier-level
comparison is gain over Single-Agent rather than raw protocol rank. Excluding the tiny tails at tiers 3
and 10, collaboration gains are near zero on tiers 1–2 and then open sharply from tier 4 onward. On
tiers 6–9, PER improves FinalPassRate by about 10 to 16 percentage points over Single-Agent, while
Broadcast improves it by about 14 to 20 percentage points. Pass@1 gains follow the same pattern,
showing that the hard-tier value of collaboration appears before verifier-guided retries.
In this benchmark/model regime, Single-Agent Iterative is the efficiency leader, PER occupies a
higher-cost middle position, and broadcast is the accuracy leader at the high-cost end. PER uses more
evaluator calls per problem than broadcast (2.19 vs. 1.35), so it is verifier-heavier despite generating
fewer tokens overall.
Broadcast’s aggregate edge comes mostly from avoiding first failure rather than from dramatically
stronger post-failure recovery. After one failure, broadcast and Single-Agent have nearly identical
conditional recovery on the second attempt, at 37.2% and 37.0%, while PER recovers less efficiently
at 32.4%. Single-Agent leads on cost-per-solve, while broadcast becomes the better choice once
verifier cost makes Pass@1 the primary objective; Appendix M and Appendix M.1 give the fuller
deployment view.

4.2   Mechanism: The Reviewer–Solver Decoupling Gap

The role-specialization hypothesis under difficulty. The next question is which process difference
best tracks the observed PER–broadcast accuracy gap in this setting. If specialized reviewers are
supposed to help most on problems that genuinely require critique to be integrated, then the key issue
is not just whether PER’s reviewer is accurate, but whether the protocol converts that signal into
solver action. We organize RQ3 around a simple chain: detection, uptake, and repair. The clearest
separation appears in uptake.
The pattern appears even before we ask whether revisions succeed. Among problems with a wrong
initial candidate, broadcast repairs 25.7% and neglects 26.2%, whereas PER repairs only 11.0%
and neglects 48.8%; try-but-fail rates are much closer (48.1% vs. 40.2%). For PER, neglect is the
dominant failure mode, not inability to repair after attempting revision. That pattern persists across
difficulty. On the more populated hard tiers 6–9, PER reviewer precision remains high (0.81–0.87),
yet even evaluator-verified useful critique changes the next candidate only 0.32–0.37 of the time,
while broadcast remains around 0.93–0.96. Those same tiers are also where the matched single-agent


                                                     6
                                                           (a) FinalPassRate gain over Single-Agent                                                                                     (b) Pass@1 gain over Single-Agent




          FinalPassRate gain over Single-Agent (pp)
                                                                     PER                                                                                                                      PER




                                                                                                                           Pass@1 gain over Single-Agent (pp)
                                                      40             Broadcast                                                                                  40                            Broadcast

                                                      30                                                                                                        30

                                                      20                                                                                                        20

                                                      10                                                                                                        10

                                                       0                                                                                                          0
                                                           1     2         3     4     5   6    7     8   9 10                                                                     1      2            3     4          5      6      7       8     9 10
                                                                                  Difficulty tier                                                                                                            Difficulty tier
 Gain = protocol FinalPassRate/Pass@1 minus Single-Agent Iterative (the matched non-collaborative anchor). Gray bands: small-N tiers (tier 3: n = 20, tier 10: n = 15).


Figure 2: Tier-level collaboration gain over Single-Agent Iterative. Single-Agent Iterative is the
matched non-collaborative anchor: it already has iterative opportunity and verifier interaction, so gain
over Single-Agent more directly reflects what deliberation and review contribute. (a) FinalPassRate
gain. Gains are near zero on tiers 1–2 and open sharply from tier 4 onward. (b) Pass@1 gain.
The same pattern holds before any verifier-guided retry, confirming that the hard-tier advantage is
earned during pre-submission deliberation rather than from extra outer-loop attempts. All gains are
measured in percentage points. Gray bands mark the benchmark’s small-N tiers (tier 3: n = 20; tier
10: n = 15).

                                                                               Inner-Loop Failure Modes                                                                                                    Reviewer & Coupling Dimensions
                                                                                                                                                                                                  PER                                     coupling gap
                                                                                                                                                                                  1.0             Broadcast
                                                                                                                                                                                                                                          0.93                  0.92
            PER 11%                                                              49%                        40%                                                                               0.86                      0.87
                                                                                                                                                                                  0.8                            0.75
                                                                                                                                                                Rate / fraction




                                                                                                                                                                                                                                                                       0.71
                                                                                                                                                                                                      0.64
                                                                          2.3×                                                                                                    0.6
                                                                          more
                                                                        neglect
                                                                                                                                                                                  0.4                                              0.34
                                                                                                                                                                                                                                                         0.29
    Broadcast                                                  26%                   26%                  48% Repair                                                              0.2
                                                                                                              Neglect
                                                                                                              Try-but-fail                                                                                                                        0.05
                                                                                                                                                                                  0.0
                                                      0%             20%             40%        60%         80%         100%                                                                                       ll           ate                              ce
                                                                                                                                                                                              ision          Reca         lingR
                                                                                                                                                                                                                                                    ed
                                                                                                                                                                                                                                              Guiedpair Resistan
                                                                 Fraction of wrong-initial-candidate cases                                                                             Prec
                                                                                                                                                                                                                     Coup                      R


Figure 3: What observable process difference tracks the PER–broadcast gap? Not reviewer
precision alone, but whether evaluator-verified useful critique changes the next candidate the protocol
carries forward. Left: NeglectRate is the dominant inner-loop failure mode for PER (48.8% of
wrong-initial-candidate cases neglect available critique), while TryButFailRate is much closer across
protocols. Right: the aggregate metrics show the core paradox: PER has higher reviewer precision
(0.861 vs. 0.644), yet evaluator-verified useful critique changes the protocol’s next candidate only
33.6% of the time under PER versus 93.5% under broadcast (CouplingRate), and ReviewerGuid-
edRepairRate is correspondingly 5.6× lower (5.1% vs. 28.6%). The shaded box highlights the
coupling and repair dimensions where the gap between protocols is largest.


baseline drops below 70% final accuracy, so the growing collaboration gain does not coincide with
any drop in reviewer precision. Appendix Figure 11 gives the full tier view.

Review-conditioned decomposition: the coupling gap. Figure 3 makes the decomposition explicit.
On detection, PER’s reviewer has higher precision (0.861 vs. 0.644). On uptake, the contrast is
sharper: under PER, evaluator-verified useful revise episodes produce an immediate answer transition
only 33.6% of the time; under broadcast, they do so 93.5% of the time. On repair, the same gap
reappears: ReviewerGuidedRepairRate is 0.051 for PER versus 0.286 for broadcast. In the main
comparison, the higher-coupling protocol is also the higher-repair protocol, so these answer-transition
events align with realized correction rather than appearing as spurious or cosmetic changes. PER is
also more resistant to misleading review: it declines to revise correct answers 92% of the time when


                                                                                                                       7
                          (a) Final outcomes                                     (b) Detection uptake repair
                                                                        100%      NeglectRate
         90%                                    89.2%                             CouplingRate
                                                                                  RGR
                                     86.3%                              80%
               85.2%
         85%
                          82.5%
                                                                        60%
         80%
  Rate




                                                                 Rate
                                                    78.6%

         75%                            74.5%                           40%
                  72.8%
                             71.0%
         70%                                                            20%
                                             FinalPassRate
                                             Pass@1
         65%                                                             0%
                 PER        PER        PER      Broadcast                       PER        PER    PER   Broadcast
                (base)     +ACK       +EMB                                     (base)     +ACK   +EMB

Figure 4: Within-PER intervention evidence for the uptake story. All values are full-benchmark
aggregates (N = 4,181); the model family, reviewer setup, and outer-loop budget are held fixed
across conditions, varying only how critique reaches the solver. (a) Final outcomes. ACK-
required lowers FinalPassRate (85.2%→82.5%) and Pass@1, while EMB partially recovers both.
(b) Detection→uptake→repair. ACK-required sharply worsens NeglectRate (0.488→0.792) and
CouplingRate (0.336→0.175), confirming it as a failed compliance-style control. EMB reduces
neglect and partially restores coupling (0.698 NeglectRate, 0.227 CouplingRate), consistent with
presenting reviewer feedback more directly improving follow-through within the PER family, while
still falling short of broadcast’s shared-state design. Read as directional evidence for the uptake story,
not as a single clean ablation.



the reviewer falsely flags them, versus 71% for broadcast. Because CouplingRate is a protocol-level
answer-transition statistic, part of this contrast reflects each protocol’s own update and submission
rules, not only the model’s internal response to critique. The same interface that makes useful critique
easier to bypass also makes false alarms easier to resist.
The same mechanism is visible in individual traces. In one tier-5 PER trace, the reviewer proposes
a corrected boxed answer yet the pipeline still submits the earlier candidate unchanged. In a tier-6
broadcast trace with the same qualitative structure, peer critique replaces the live candidate before
re-approval and submission. Appendix P gives the full trace excerpts.
We treat PER versus broadcast as evidence about complete protocol designs, not routing alone; the
within-PER probes below test whether more direct critique presentation increases uptake.


Within-PER coupling interventions. The uptake gap also shifts within PER itself. These within-
PER probes are the source of the paper’s directional evidence that more direct critique delivery
improves uptake. We hold the model family, reviewer setup, and outer-loop budget fixed and vary
only how critique reaches the solver. Figure 4 shows the direction of movement. ACK-required
adds mandatory verbal acknowledgment but keeps routed advice unchanged; it does not rescue PER:
FinalPassRate falls from 85.2% to 82.5%, NeglectRate rises from 0.488 to 0.792, and CouplingRate
drops from 0.336 to 0.175. In this prompt configuration, the solver can satisfy the new instruction
without changing the candidate itself. This pattern is consistent with superficial compliance: verbal
acknowledgment can separate from an actual update to the underlying candidate.
EMB places reviewer feedback directly in the solver’s working context. Relative to the matched
ACK-required control, FinalPassRate rises from 82.5% to 86.3%, Pass@1 from 71.0% to 74.5%, and
NeglectRate falls from 0.792 to 0.698. Compared with exact base PER, the gain is more selective:
end-to-end outcomes improve, but direct uptake diagnostics do not uniformly dominate base PER.
We read Base PER → EMB → Broadcast as a sequence of designs with progressively more direct
reviewer feedback rather than as a single clean ablation: ACK-required does not fix the uptake gap,
while more direct presentation of reviewer feedback is associated with better follow-through.


                                                             8
A deeper-reflection PER stress test. We also test whether PER is simply under-iterated locally. A
separate full-benchmark PER variant with a deeper local reflective budget (PER-inner6) improves
over base PER on Pass@1, FinalPassRate, and HintAwareCorrectionScore, but it still trails broadcast
and still uses more evaluator calls per problem than broadcast (2.07 vs. 1.35). We read deeper local
reflection as a partial recovery of PER rather than as a full explanation of the broadcast advantage.
Details appear in Appendix Tables 14 and 15, Figure 6, and Appendix C.


5   Conclusion

Specialized reviewers help only when correct critique changes the next candidate the protocol carries
forward. In our study, PER’s reviewer has higher precision, yet the next answer changes far less often
after evaluator-verified useful critique, and realized repair is correspondingly lower. NeglectRate,
CouplingRate, and ReviewerGuidedRepairRate separate detection, uptake, and repair so that each
step is independently measurable. The main finding is more limited than a protocol ranking: in
this hard benchmark and primary shared-model setting, higher reviewer precision does not by itself
guarantee better collaborative reasoning, and reviewer precision and critique uptake can come apart.
This result matters both for evaluation design and for system design. A system that detects errors
but fails to act on the corresponding critique can appear strong under reviewer-centric evaluation
while failing to improve actual problem solving. Improving reviewer quality alone may therefore not
improve outcomes unless the interface helps correct feedback change the next candidate.
The within-PER intervention suite then adds directional support for that account. In the tested prompt
configuration, ACK-required is a failed compliance-style control, EMB is a partial recovery step, and
deeper local reflection helps only partially while still using more evaluator calls than broadcast. Taken
together, these results are consistent with critique presented more directly in the solver’s working
context playing an important role inside hierarchical pipelines, even though they do not isolate a
single causal factor or imply that uptake alone determines the final ranking. The current evidence
also does not yet distinguish cleanly between two nearby failure modes inside PER: critique that
is not fully incorporated at all, and critique that is seen but treated as less authoritative than the
solver’s existing reasoning. A reduced cross-family replication with Gemma 3 27B actors preserves
the same precision–uptake separation even as the overall ranking shifts. In that replication, PER’s
reviewer still has higher precision (PER: 0.881, Broadcast: 0.722), while Broadcast shows much
higher useful-critique uptake (Broadcast: 0.742, PER: 0.092) and a correspondingly larger repair rate.
This suggests that uptake is an important hidden evaluation axis, but not by itself a universal predictor
of protocol quality across model families; see Appendix D. Within hierarchical agent pipelines,
reviewer quality alone is not a sufficient design principle; performance also depends on whether the
protocol turns correct critique into the next candidate it carries forward.


6   Limitations and Broader Impact

This paper studies protocol structure in a deliberately restricted but rigorous setting: verifier-grounded
olympiad-level math from the Omni-MATH benchmark family [7, 2]. Our conclusions are therefore
about protocol behavior under this benchmark, not about universal superiority of one interaction style
across every domain. The main benchmark evidence comes from one primary actor family, while
Appendix D adds a reduced cross-family replication with Google’s open-weight Gemma 3 27B actors
from a different family while holding the evaluator fixed. Even with that addition, protocol rankings
may still vary with model family or deployment details such as prompt templates and context budgets.
Our claim is thus about a common PER-style feedback interface under the matched configurations
used in this study, not about the impossibility of hierarchical specialization itself. We expect the
detection–uptake–repair decomposition to generalize more readily than the exact rate values, which
may differ in domains where correctness is less binary than math benchmarking. CouplingRate is an
operational answer-transition statistic on evaluator-verified useful revise episodes, not a free-form
semantic judgment about whether the solver “understood” the critique. Our current within-PER
probes also do not isolate whether lower uptake comes primarily from information formatting, role-
hierarchy weighting, or both. Appendix H and Appendix B provide the stricter answer-transition
audit and cross-evaluator replay.


                                                    9
The broader impact is two-sided. On the positive side, coupling-aware evaluation can reduce
overclaiming by showing when valid critique fails to become action, which matters for benchmark
design and settings where corrective feedback is costly or safety-critical [10]. In safety-critical
settings, correct critique that is ignored can be functionally equivalent to no critique at all. On the
other hand, stronger feedback uptake can also increase effective capability. We therefore view clearer
mechanistic evaluation as a tool for both capability assessment and more trustworthy oversight.

Data and code. The public release website is available at https://huggingface.co/spaces/
AgentsSci/scientific-agent-protocol-traces-site. Code and data will be released after
institutional approval.

Acknowledgments
This research used resources of the Argonne Leadership Computing Facility, a U.S. Department
of Energy (DOE) Office of Science user facility at Argonne National Laboratory (ANL) operated
under Contract No. DE-AC02-06CH11357. The work was also supported under the same contract by
the DOE Office of Science’s Advanced Scientific Computing Research Program and by Laboratory
Directed Research and Development (LDRD) funding from ANL, provided by the Director, DOE
Office of Science.

References
 [1] Johin Johny Arimbur. How many tries does it take? Iterative self-repair in LLM code generation
     across model scales and benchmarks. arXiv preprint arXiv:2604.10508, 2026. URL https:
     //arxiv.org/abs/2604.10508.
 [2] Marthe Ballon, Andres Algaba, Brecht Verbeken, and Vincent Ginis. Benchmarks saturate
     when the model gets smarter than the judge. arXiv preprint arXiv:2601.19532, 2026. URL
     https://arxiv.org/abs/2601.19532.
 [3] Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari,
     Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, and
     Joseph E. Gonzalez. Why do multi-agent LLM systems fail? arXiv preprint arXiv:2503.13657,
     2025. URL https://arxiv.org/abs/2503.13657.
 [4] Ding Chen, Qingchen Yu, Pengyuan Wang, Mengting Hu, Wentao Zhang, Zhengren Wang,
     Bo Tang, Feiyu Xiong, Xinchi Li, Chao Wang, Minchuan Yang, and Zhiyu Li. xverify: Efficient
     answer verifier for reasoning model evaluations. arXiv preprint arXiv:2504.10481, 2025. URL
     https://arxiv.org/abs/2504.10481.
 [5] Jacob Cohen. A coefficient of agreement for nominal scales. Educational and Psychological
     Measurement, 20(1):37–46, 1960. doi: 10.1177/001316446002000104.
 [6] Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mordatch. Improv-
     ing factuality and reasoning in language models through multiagent debate. arXiv preprint
     arXiv:2305.14325, 2023. URL https://arxiv.org/abs/2305.14325.
 [7] Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Qingxiu Dong, Lei Li, Chenghao
     Ma, Liang Chen, Runxin Xu, Zhengyang Tang, Benyou Wang, Daoguang Zan, Shanghaoran
     Quan, Ge Zhang, Lei Sha, Yichang Zhang, Xuancheng Ren, Tianyu Liu, and Baobao Chang.
     Omni-math: A universal olympiad level mathematic benchmark for large language models.
     arXiv preprint arXiv:2410.07985, 2024. URL https://arxiv.org/abs/2410.07985.
 [8] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying
     Song, and Denny Zhou. Large language models cannot self-correct reasoning yet. arXiv preprint
     arXiv:2310.01798, 2024. URL https://arxiv.org/abs/2310.01798.
 [9] Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, and Arvind Narayanan. Ai
     agents that matter. arXiv preprint arXiv:2407.01502, 2024. URL https://arxiv.org/abs/
     2407.01502.


                                                  10
[10] Zachary Kenton, Noah Y. Siegel, Janos Kramar, Jonah Brown-Cohen, Samuel Albanie, Jannis
     Bulian, Rishabh Agarwal, David Lindner, Yunhao Tang, Noah D. Goodman, and Rohin Shah.
     On scalable oversight with weak llms judging strong llms. arXiv preprint arXiv:2407.04622,
     2024. URL https://arxiv.org/abs/2407.04622.

[11] Yubin Kim, Ken Gu, Chanwoo Park, Chunjong Park, Samuel Schmidgall, A. Ali Heydari, Yao
     Yan, Zhihan Zhang, Yuchen Zhuang, Yun Liu, Mark Malhotra, and Paul Pu Liang. Towards
     a science of scaling agent systems. arXiv preprint arXiv:2512.08296, 2025. URL https:
     //arxiv.org/abs/2512.08296.

[12] J. Richard Landis and Gary G. Koch. The measurement of observer agreement for categorical
     data. Biometrics, 33(1):159–174, 1977. doi: 10.2307/2529310.

[13] Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard
     Ghanem. CAMEL: Communicative agents for mind exploration of large scale language model
     society. arXiv preprint arXiv:2303.17760, 2023. URL https://arxiv.org/abs/2303.
     17760.

[14] Yin Li. Decomposing LLM self-correction: The accuracy-correction paradox and error depth
     hypothesis. arXiv preprint arXiv:2601.00828, 2026. URL https://arxiv.org/abs/2601.
     00828.

[15] Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding,
     Kai Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui
     Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and
     Jie Tang. Agentbench: Evaluating llms as agents. In International Conference on Learning
     Representations, 2024. URL https://arxiv.org/abs/2308.03688.

[16] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri
     Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad
     Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-
     refine: Iterative refinement with self-feedback. In Advances in Neural Information Processing
     Systems, 2023. URL https://arxiv.org/abs/2303.17651.

[17] Mary L. McHugh. Interrater reliability: The kappa statistic. Biochemia Medica, 22(3):276–282,
     2012. doi: 10.11613/BM.2012.031.

[18] Sumeet Ramesh Motwani, Chandler Smith, Rocktim Jyoti Das, Rafael Rafailov, Ivan Laptev,
     Philip H. S. Torr, Fabio Pizzati, Ronald Clark, and Christian Schroeder de Witt. Malt: Improving
     reasoning with multi-agent LLM training. arXiv preprint arXiv:2412.01928, 2024. URL
     https://arxiv.org/abs/2412.01928.

[19] Linyong Nan, Ellen Zhang, Weijin Zou, Yilun Zhao, Wenfei Zhou, and Arman Cohan. On
     evaluating the integration of reasoning and action in LLM agents with database question
     answering. arXiv preprint arXiv:2311.09721, 2023. URL https://arxiv.org/abs/2311.
     09721.

[20] OpenAI. gpt-oss-120b model, 2025. URL https://developers.openai.com/api/docs/
     models/gpt-oss-120b. Accessed: 2026-05-01.

[21] OpenAI.     Introducing gpt-oss, 2025.                 URL    https://openai.com/index/
     introducing-gpt-oss/. Accessed: 2026-05-01.

[22] Shuo Ren, Can Xie, Pu Jian, Zhenjiang Ren, Chunlin Leng, and Jiajun Zhang. Towards scientific
     intelligence: A survey of llm-based scientific agents. arXiv preprint arXiv:2503.24047, 2025.
     URL https://arxiv.org/abs/2503.24047.

[23] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and
     Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. In Advances in
     Neural Information Processing Systems, 2023. URL https://arxiv.org/abs/2303.11366.


                                                 11
[24] Guiyao Tie, Zenghui Yuan, Zeli Zhao, Chaoran Hu, Tianhe Gu, Ruihang Zhang, Sizhe Zhang,
     Junran Wu, Xiaoyue Tu, Ming Jin, Qingsong Wen, and Lixing Chen. Can llms correct them-
     selves? a benchmark of self-correction in llms. arXiv preprint arXiv:2510.16062, 2025. URL
     https://arxiv.org/abs/2510.16062.

[25] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan, and
     Hoang D. Nguyen. Multi-agent collaboration mechanisms: A survey of llms. arXiv preprint
     arXiv:2501.06322, 2025. URL https://arxiv.org/abs/2501.06322.

[26] Ken Tsui. Self-correction bench: Uncovering and addressing the self-correction blind spot in
     large language models. OpenReview, 2025. URL https://openreview.net/forum?id=
     7K1kXowjK1.

[27] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha
     Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
     models. In International Conference on Learning Representations, 2023. URL https://
     arxiv.org/abs/2203.11171.

[28] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi,
     Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language
     models. In Advances in Neural Information Processing Systems, 2022. URL https://arxiv.
     org/abs/2201.11903.

[29] Haolun Wu, Zhenkun Li, and Lingyao Li. Can LLM agents really debate? a controlled study
     of multi-agent debate in logical reasoning. arXiv preprint arXiv:2511.07784, 2025. URL
     https://arxiv.org/abs/2511.07784.

[30] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun
     Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W. White, Doug Burger,
     and Chi Wang. Autogen: Enabling next-gen LLM applications via multi-agent conversation.
     arXiv preprint arXiv:2308.08155, 2023. URL https://arxiv.org/abs/2308.08155.

[31] Zhe Yang, Yichang Zhang, Yudong Wang, Ziyao Xu, Junyang Lin, and Zhifang Sui. Con-
     fidence v.s. critique: A decomposition of self-correction capability for llms. arXiv preprint
     arXiv:2412.19513, 2024. URL https://arxiv.org/abs/2412.19513.

[32] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik
     Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. In
     Advances in Neural Information Processing Systems, 2023. URL https://arxiv.org/abs/
     2305.10601.

[33] Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan,
     and Michal Shmueli-Scheuer. Survey on evaluation of llm-based agents. arXiv preprint
     arXiv:2503.16416, 2025. URL https://arxiv.org/abs/2503.16416.

[34] Yurun Yuan and Tengyang Xie. Reinforce LLM reasoning through multi-agent reflection. arXiv
     preprint arXiv:2506.08379, 2025. URL https://arxiv.org/abs/2506.08379.

[35] Qiyuan Zhang, Fuyuan Lyu, Zexu Sun, Lei Wang, Weixu Zhang, Wenyue Hua, Haolun Wu,
     Zhihan Guo, Yufei Wang, Niklas Muennighoff, Irwin King, and Xue Liu. A survey on test-
     time scaling in large language models: What, how, where, and how well? arXiv preprint
     arXiv:2503.24235, 2025. URL https://arxiv.org/abs/2503.24235.

[36] Yunxiang Zhang, Muhammad Khalifa, Lajanugen Logeswaran, Jaekyeom Kim, Moontae Lee,
     Honglak Lee, and Lu Wang. Small language models need strong verifiers to self-correct
     reasoning. In Findings of the Association for Computational Linguistics: ACL 2024, 2024. URL
     https://aclanthology.org/2024.findings-acl.924/.

[37] Yilun Zhou, Austin Xu, Peifeng Wang, Caiming Xiong, and Shafiq Joty. Evaluating judges as
     evaluators: The jetts benchmark of llm-as-judges as test-time scaling evaluators. arXiv preprint
     arXiv:2504.15253, 2025. URL https://arxiv.org/abs/2504.15253.


                                                 12
[38] Yuxuan Zhu, Tengjun Jin, Yada Pruksachatkun, Andy Zhang, Shu Liu, Sasha Cui, Sayash
     Kapoor, Shayne Longpre, Kevin Meng, Rebecca Weiss, Fazl Barez, Rahul Gupta, Jwala
     Dhamala, Jacob Merizian, Mario Giulianelli, Harry Coppock, Cozmin Ududec, Jasjeet Sekhon,
     Jacob Steinhardt, Antony Kellermann, Sarah Schwettmann, Matei Zaharia, Percy Liang, and
     Daniel Kang. Establishing best practices for building rigorous agentic benchmarks. arXiv
     preprint arXiv:2507.02825, 2025. URL https://arxiv.org/abs/2507.02825.


Appendix

This supplementary material is organized in two layers. The first appendix pages defend the paper’s
main claim with the highest-priority robustness checks; the later sections provide the fuller metric
catalog, protocol configurations, extended results tables, trace examples, and process diagnostics
referenced from the main paper.


A     Robustness Checks for the Main Claim

Because some reviewers may skim only the first appendix pages, we front-load the checks that most
directly protect the paper’s core claim. Table 2 summarizes the four main concerns and the appendix
evidence that addresses them. The rest of the appendix then serves the second job: reference material,
fuller metric definitions, protocol documentation, and extended plots.

Table 2: High-priority robustness checks for the paper’s main claim. These are the appendix items
most directly aimed at protecting the precision–uptake story rather than supplying background
reference material.
 Concern                      Check                                   Main result                                      Where
 Coupling metric is brittle   Deterministic and equivalence-aware     Strict and legacy CouplingRate are numeri-       Table 3
                              answer-transition audits on the same    cally identical for both PER and Broadcast,
                              useful-revise episodes                  with zero strict-vs-legacy disagreement
 Single evaluator artifact    Cross-evaluator     replay   with       Full-benchmark disagreement stays at 3.38%–      Appendix B
                              gpt-oss-120b, Llama, and Gemma          5.76% with κ = 0.850–0.915; disagreement
                              under the same prompt/parser            rises on the hard collaborative slice but does
                                                                      not reverse the main pattern
 PER just needs more lo-      Higher-cost PER-inner6 stress test      PER-inner6 improves over base PER (Fi-           Appendix C
 cal reflection                                                       nalPassRate 85.2%→86.3%) but still trails
                                                                      Broadcast (89.2%) and still uses more evalu-
                                                                      ator calls (2.07 vs. 1.35)
 Single actor family only     Reduced cross-family replication with   The overall ranking shifts, but the precision–   Appendix D
                              Google Gemma 3 27B actors and fixed     uptake separation remains strong (PER preci-
                              gpt-oss-120b evaluator                  sion 0.881 vs. 0.722; uptake 0.092 vs. 0.742)




A.1    Coupling Metric Robustness

The paper-facing CouplingRate is an operational immediate answer-transition statistic on evaluator-
verified useful revise episodes. The main robustness question is whether the PER–broadcast uptake
gap depends on a fragile answer-normalization choice. To check that, we re-audit the same episodes
with two stricter definitions: a deterministic normalized answer key and an equivalence-aware exact
answer checker. The practical result is stable: for both PER and Broadcast, the strict deterministic
audit matches the legacy paper-facing CouplingRate exactly, and the equivalence-aware variant
changes only a few PER cases without altering the qualitative gap.


B     Evaluator Selection and Leakage Controls

        • Evaluator correctness matters in verifier-gated math benchmarks because judge errors can
          distort model and protocol comparisons as systems improve [2, 36, 4, 37].
        • gpt-oss-120b is a public OpenAI open-weight reasoning model released under Apache
          2.0, with public downloads and deployment documentation [21, 20].


                                                                   13
Table 3: Pooled strict answer-transition audit for the main PER and broadcast comparison. Legacy
CouplingRate is the paper-facing uptake metric used in the main text; Strict CouplingRate re-audits
the same useful-revise episodes with a deterministic normalized answer-key rule; EquivalenceAware
CouplingRate replaces that rule with the exact deterministic answer-equivalence checker. The
practical point is that the uptake gap is definition-stable: for both protocols, strict and legacy rates are
numerically identical and strict-vs-legacy disagreement is zero on all eligible useful-revise episodes.
This shows that the PER–broadcast coupling gap does not depend on a fragile normalization choice
or on one particular legacy pipeline label.

               Useful revise       Legacy                 Strict           EquivalenceAware      Strict-vs-legacy
   Protocol      episodes        CouplingRate          CouplingRate          CouplingRate         disagreement
   PER            5,253        0.336 (1,766/5,253)   0.336 (1,766/5,253)   0.340 (1,787/5,253)      0 / 5,253
   Broadcast      5,214        0.935 (4,876/5,214)   0.935 (4,876/5,214)   0.935 (4,876/5,214)      0 / 5,214



       • In smoke-test disagreements between gpt-oss-120b and a smaller evaluator, manual review
         by a PhD-level annotator with math background favored gpt-oss-120b. We therefore use
         gpt-oss-120b as the evaluator.
       • To mitigate same-model-family coupling, correctness judgment is restricted to the submitted
         boxed answer, the ground-truth answer, and minimal reference explanation when needed for
         answer equivalence. The evaluator does not read agents’ reasoning traces when deciding
         pass/fail.
       • Only after a fixed FAIL verdict, and only for hinted feedback, may a hint-generation pass
         inspect compact reasoning context to produce a short non-answer-revealing repair hint. A
         hint scanner is applied before any hint is forwarded to acting agents.
       • The same evaluator and judging mechanism are used across all protocols for fairness.

As a robustness check against single-evaluator sensitivity, we replay the exact saved submit-
ted answers under the same evaluator prompt/parser with three open models: gpt-oss-120b,
Meta-Llama-3.1-70B-Instruct, and gemma-3-27b-it. The first replay covers the full paper
experiment output (16,724 submission instances; 10,590 unique candidate answers after deduplica-
tion). Table 4 shows that overall pairwise agreement remains high: instance-level disagreement stays
between 3.38% and 5.76%, with Cohen’s κ between 0.850 and 0.915. Cohen’s κ is a chance-corrected
inter-rater agreement coefficient [5]; by common heuristics, the observed range is generally read as
strong agreement [12, 17]. We therefore treat the replay as trustworthy as a robustness check rather
than as a second ground-truth source, and we report raw disagreement alongside κ because agreement
coefficients can still be affected by label prevalence. The disagreements are not uniform, however.
They rise on the collaborative modes and on the hard tiers where answer equivalence and partially
correct boundary cases are more common. For example, gpt-oss-120b versus Llama disagrees on
4.38% of baseline outputs but on 6.21% of PER outputs and 6.57% of broadcast outputs. On the
hard tiers 7–10, the corresponding per-mode disagreement reaches 9.95% for PER and 9.47% for
broadcast in the full replay.
Because those hard collaborative cases are exactly where evaluator sensitivity matters most, we also
run a second replay restricted to PER and broadcast on tiers 7–10 (1,694 submission instances).
This focused replay is not a replacement benchmark-wide result; it is a stress test that removes
the remaining missing judgments and gives all three evaluators 100% valid coverage on the same
hard slice. Under that restriction, overall pairwise disagreement rises to 9.68% for gpt-oss-120b
versus Llama, 9.39% for gpt-oss-120b versus Gemma, and 5.25% for Llama versus Gemma,
with κ = 0.755, 0.761, and 0.875, respectively. The largest tier/mode cell is tier-9 PER, where
gpt-oss-120b versus Llama reaches 12.33% disagreement on n = 146 instances; tier 8 is also near
9–10% for both PER and broadcast. Tier 10 has only 30 total focused-slice instances and should
not be overinterpreted. Across the focused replay, 206 of 1,694 instances are contested by at least
one evaluator pair, split almost evenly between PER (104) and broadcast (102). We therefore use
gpt-oss-120b as the main evaluator and treat the replay suite as a robustness check rather than a
replacement judge: disagreement is real and concentrates where the benchmark is hardest, but the
overall agreement levels are high enough that the main protocol story is unlikely to be a trivial artifact
of one evaluator.


                                                          14
Table 4: Cross-evaluator replay over saved paper-experiment submissions. The first block is the
full benchmark; the second is the focused hard collaborative slice (PER/Broadcast, tiers 7–10).
Coverage is the fraction of submission instances for which both evaluators returned a valid binary
judgment. Disagreement is computed on submission instances rather than deduplicated candidates;
the unique-candidate replay is slightly harsher but does not change the qualitative picture.

                                Slice                           Evaluator pair                       Coverage      Disagreement           κ
                                Full benchmark                  gpt-oss-120b vs. Llama               99.83%            5.76%             0.850
                                                                gpt-oss-120b vs. Gemma               99.45%            4.35%             0.884
                                                                Llama vs. Gemma                      99.53%            3.38%             0.915
                                Focused hard slice              gpt-oss-120b vs. Llama               100.0%            9.68%             0.755
                                                                gpt-oss-120b vs. Gemma               100.0%            9.39%             0.761
                                                                Llama vs. Gemma                      100.0%            5.25%             0.875


                                  (a) Disagreement concentrates on                                   (b) gpt-oss vs Llama disagreement
                                       hard collaborative cases                                        by tier & protocol (hard slice)
                        14
                                             Full benchmark (N = 16,724)                                                                         14%
                                             Hard collaborative slice                      Tier 7       9.2%                  9.5%
                        12                   (PER/Broadcast, tiers 7 10, N = 1,694)      (n=358)
                                                                                                                                                 12%
Disagreement rate (%)




                        10          =0.755             =0.761




                                                                                                                                                      Disagreement rate (%)
                                                                                           Tier 8                                                10%
                                                                                         (n=328)       10.1%                 10.1%
                         8
                                                                                                                                                 8%
                               =0.850
                         6                                                  =0.875         Tier 9                                                6%
                                                 =0.884                                  (n=146)       12.3%                  8.2%
                         4                                            =0.915                                                                     4%
                         2                                                                Tier 10        0.0%
                                                                                                        (n=15)
                                                                                                                              6.7%
                                                                                                                             (n=15)              2%
                                                                                      (n=15, tiny)
                         0                                                                                                                       0%
                                gpt-oss           gpt-oss              Llama                            PER                Broadcast
                               vs Llama          vs Gemma            vs Gemma

Figure 5: Cross-evaluator disagreement robustness. (a) Grouped bars compare pairwise disagree-
ment rates on the full benchmark (N = 16,724; light bars) versus the focused hard collaborative
slice (PER and Broadcast, tiers 7–10, N = 1,694; dark bars). Cohen’s κ is annotated above each bar.
Overall agreement is high (disagreement 3.4–5.8%, κ = 0.850–0.915), but disagreement roughly
doubles on the hard collaborative slice (5.3–9.7%, κ = 0.755–0.875). (b) gpt-oss-120b vs. Llama
disagreement heatmap for the hard collaborative slice, stratified by tier and protocol. Disagreement
concentrates at tiers 8–9 (∼9–12%); tier 10 has only 15 instances per protocol and its lower rate
should not be overinterpreted (hatched). The pattern confirms that the main protocol story is not a
trivial single-evaluator artifact, but evaluator sensitivity is real exactly where answer equivalence is
most ambiguous.


C                            Deeper-Reflection PER Stress Test

We also test whether PER’s local reflective loop is simply too shallow. To stress-test that hypothesis,
we ran a separate full-benchmark PER variant with a deeper local reflection budget (PER-inner6).
This probe is intentionally distinct from ACK-required and EMB: it changes inner-loop depth rather
than the critique surface. We therefore do not treat it as a missing cell in the within-PER coupling-
intervention continuum.
The resulting pattern is informative rather than destabilizing. PER-inner6 improves over base PER
on first-pass and final outcomes, suggesting that deeper local reflection can partially recover PER.
But it still does not match broadcast, and it does not remove the practical verifier-cost asymmetry.
In particular, PER-inner6 remains cheaper than broadcast in generation tokens yet still uses more
evaluator calls per problem. The small drop in AvgEvalCalls/problem from base PER (2.19) to
PER-inner6 (2.07) should therefore be read as a second-order consequence of better early repair:
more problems are solved before an external verifier failure can trigger another outer retry, even
though the protocol spends substantially more inner-loop reasoning on each surviving hard case. The


                                                                                            15
cleanest reading is therefore that deeper local reflection helps, but does not make the feedback-uptake
interface issue disappear.

Table 5: Deeper-reflection PER stress test over the completed full benchmark (N = 4,181). PER-
inner6 increases the local reflective budget but does not change the acting/evaluator model family
or benchmark slice. This is a stress test of the shallow-local-reflection hypothesis, not a new main
protocol family.

                            Final            HintAware               AvgEvalCalls/ AvgReflective Misleading
Protocol                   PassRate Pass@1 CorrectionScore AvgTokens   problem       Rounds      ReviewHarm
PER                           85.2%     72.8%           70.4%                       400K                   2.19                1.17              0.083
PER-inner6                    86.3%     74.8%           73.9%                       557K                   2.07                2.06              0.183
Broadcast                     89.2%     78.6%           81.8%                       616K                   1.35                4.23              0.313


                                      PER-inner6 Stress Test: Deeper Reflection Partially Improves PER
                                                   but Does Not Close the Broadcast Gap
                              (a) Token cost vs. accuracy frontier                                                   (b) Metric comparison
                                                                                                   90%       PER                89.2%
                90.0%                                                                                        PER-inner6
                                                                                                             Broadcast 85.2%86.3%
                                                                                                   85%
FinalPassRate




                                                                           Broadcast                                                             81.8%
                88.0%
                                                                                                   80%
                                                                                            Rate
                                                                          1.35 eval calls                       78.6%
                                                        PER-inner6
                86.0%                                                                                        74.8%
                                                                                                   75%   72.8%
                                                                                                                                             73.9%
                                                        2.07 eval calls
                                                                                                                                         70.4%
                 PER                                                                               70%
                84.0%
         2.19 eval calls                                                                           65%
                        400       450       500       550            600                                   Pass@1        FinalPassRate   HintAware
                               Avg tokens / problem (thousands)                                                                          Corr. Score

Figure 6: Deeper-reflection PER stress test: PER-inner6 (brown-orange) increases local reflective
rounds from 1.17 to 2.06 per problem. Panel (a) shows the token-cost vs. accuracy frontier; annota-
tions give AvgEvalCalls/problem beside each point. Panel (b) compares Pass@1, FinalPassRate, and
HintAwareCorrectionScore across the three protocols. PER-inner6 partially closes the accuracy gap
to Broadcast (FinalPassRate: 86.3% vs. 85.2% base PER, 89.2% Broadcast) while still using more
evaluator calls per problem (2.07) than Broadcast (1.35). The gap is narrowed but not closed; deeper
local reflection helps, while the verifier-cost asymmetry persists.


D                Cross-Family Partial Replication with Gemma 3 Actors
To probe whether the main precision–uptake separation depends entirely on the primary actor family,
we ran a reduced four-mode replication with Google’s open-weight gemma-3-27b-it actors, a
different 27B actor family from the primary gpt-oss-120b run, while keeping the evaluator fixed at
gpt-oss-120b. This addendum uses the tier-sampled subset currently available from that sweep
(N = 835 problems across the same ten benchmark tiers, with tiers 3 and 10 still small-N ). The
subset contains a random sample of 100 problems per tier when available; for tiers with fewer than
100 problems, we include the full tier. Table 6 reports the stable cross-family signal we rely on in
the paper: the raw protocol ranking shifts, but reviewer precision and critique uptake remain sharply
separated. To keep this appendix addition conservative, we summarize the pooled RQ1 outcomes
together with the review-conditioned RQ3 metrics; we do not use the current reduced-run RQ2 export
in the paper text until its attempt-depth columns are fully reconciled with the launch budget.
The cross-family takeaway is narrower than a replication of the primary ranking. On this smaller-
model subset, PER has the higher final accuracy, yet Broadcast remains much more likely to turn
correct critique into the next candidate the protocol carries forward and to realize repair from that
critique. We therefore interpret the Gemma addendum as evidence that reviewer precision and critique
uptake remain separable even when protocol ranking shifts across actor families, not as a second
protocol leaderboard.


                                                                              16
Table 6: Reduced cross-family replication with Gemma 3 actors and a fixed gpt-oss-120b evaluator
(N = 835 tier-sampled problems). FinalPassRate and Pass@1 are computed over all sampled
problems. Avg. Model Calls is the average number of model calls per problem. Reviewer precision
asks how often a reviewer warning truly points to a real error. Useful-critique uptake is the paper-
facing CouplingRate on evaluator-verified useful-critique episodes. Reviewer-guided repair is the
fraction of those useful-review episodes that the next candidate actually fixes. The ranking differs
from the primary gpt-oss-120b actor run, but the precision–uptake separation remains strong.

                               Final          Avg. Model Reviewer Useful-critique Reviewer-guided
Protocol                      PassRate Pass@1   Calls    precision    uptake           repair
Baseline LLM (one-shot)        42.6%     42.6%         2.62        —             —                 —
Single-Agent Iterative         60.5%     42.5%        6.92        —             —                 —
PER (role-based MAS)           65.6%     43.4%        22.83      0.881         0.092             0.009
Broadcast deliberation         58.7%     38.3%       130.11      0.722         0.742             0.174


E     Notation
       • Let N denote the number of evaluated problems.
       • Let yifinal ∈ {0, 1}: eventually solved within budget.
                (1)
       • Let yi ∈ {0, 1}: first outer-loop submission passes.
       • Let ai : index of first successful outer-loop submission.
       • Let T denote the set of difficulty tiers, and let Dt = {i : d(i) = t} be the subset of problems
         in tier t.
       • Let fi = ai − 1: number of failed outer-loop submissions before first success.
       • Let hi : number of hint-bearing feedback rounds before first success.
       • Let Ri : number of reflective-refinement rounds on problem i.
                (0)   (1)
       • Let zi , zi        ∈ {0, 1}: correctness of initial and final internal candidates in the inner loop.
                (0)  (1)
       •   Let xi , xi : extracted initial and final candidate answers (for NeglectRate splitting).
       • Let ri ∈ {Revise, Agree}: extracted review action on review-labeled subset.
       • Let gi ∈ {0, 1}: whether evaluator feedback was incorporated in the next revision.
       • Let ti : total token cost for problem i. Let ci : model/API calls. Let ei : evaluator calls. Let
         wi : wall-clock time.
       • Let d(i): difficulty tier. Let s(i): mathematical sub-domain.

F     Extended Term Lineage
This section expands the brief paper-facing terminology into its longer literature lineage and the
specific measurement gaps each term is meant to expose.

G     Literature Map for the Evaluation Lens
This section situates the paper’s evaluation lens relative to the adjacent multi-agent, self-correction,
and benchmark-design strands it draws on.

H     Full Metric Catalog
H.1    Outcome and Efficiency Metrics

Final success and first-pass success.
                                                 N                              N
                                      1 X final                          1 X (1)
                      FinalPassRate =      y    ,               Pass@1 =      y .                        (1)
                                      N i=1 i                            N i=1 i


                                                       17
Table 7: Extended term lineage table. This version keeps the literature anchors and the specific
measurement gaps; the main paper uses only the brief terminology needed to follow the mechanism
argument.

    Term                     Definition                    Literature anchor              What prior work misses
    Within-attempt review Reviewer critiques solver    Self-Refine [16]; intrinsic        Multi-agent extension:
    (inner loop)          draft; solver may revise—all self-correction [24]               reviewer and solver are
                          before any external verifier                                    separate agents
                          verdict is issued
    Verifier-guided repair   System retries after the      Extrinsic correction [24];     Protocol-level comparison
    (outer loop)             external verifier issues a    iterative self-repair [1]      of who benefits from
                             FAIL signal                                                  verifier feedback
    ReflectiveRepairRate     Among wrong initial           Protocol-level transition      Not separated from
                             candidates, fraction          [16, 31]                       reviewer quality
                             corrected by end of the inner
                             loop (extended)
    NeglectRate (new)        Among reviewer-flagged        “Self-correction blind spot”   Never measured in
                             wrong answers, fraction       [26] (single-agent analog)     multi-agent settings
                             where solver makes no
                             revision (submits same
                             answer)
    TryButFailRate (new) Among reviewer-flagged            Error depth hypothesis [14]    Not separated from
                         wrong answers, fraction           (single-agent)                 neglect—opposite
                         where solver revises but                                         implications for system
                         answer remains wrong                                             design
    Reviewer–Solver          Whether a reviewer’s correct No prior work measures this Root cause of PER’s repair
    Coupling (new)           flag reliably produces solver at the agent-interface level gap
                             revision (high coupling) or
                             not (decoupling)
    ReviewerGuided           Among problems where          Decomposes reviewer            Prior work treats reviewer
    RepairRate (new)         reviewer correctly identifies precision from solver          quality and system repair as
                             a wrong answer (TP),          compliance                     one
                             fraction that the solver
                             actually fixes
    MisleadingResistance Among problems where          Review false-positive              Trade-off between safety
    (new)                reviewer incorrectly flags a handling in prior work is           against false alarms and
                         correct answer (FP), fraction usually implicit                   responsiveness to valid
                         the solver resists revising                                      critique
    ConditionalRecoveryRate@k
                          Count of problems first          Hazard-rate framing of        Marginal gain masks
    (new)                 solved at attempt k divided      outer-loop recovery; survival diminishing returns; hazard
                          by the count that reached        analysis analog               rate models verifier-call
                          attempt k                                                      value directly




Average resource metrics and paper display labels. The runtime metric code emits
AvgTotalTokens, AvgModelCalls, and TotalEvaluatorAttempts. In the paper tables we
shorten these to AvgTokens, AvgModelCalls, and AvgEvalCalls/problem. AvgWallClock is an


                                                           18
Table 8: Compact literature map for the evaluation lens of this paper. The goal is not exhaustive
coverage, but to show the main strands our framing draws on and the specific gap we target.
 Strand                           Representative papers                             Typical emphasis                      Gap we target
 Peer deliberation and debate     Multi-Agent Debate [6], AutoGen [30],             Whether interaction among peers       Usually reports outcome gains,
                                  CAMEL [13], Can Agents Debate? [29]               improves final task performance       not whether critique is actually
                                                                                    or factuality                         acted on
 Hierarchical   and       role-   MALT [18], DPSDP [34], scientific-agent           Specialized roles, reviewer/critic    Usually treats reviewer quality
 specialized MAS                  surveys [22], Scaling Agent Systems [11]          decomposition, and coordination       and realized repair as one com-
                                                                                    gains                                 bined effect
 Self-correction and reflection   Self-Refine [16], Reflexion [23], Correct-        Intrinsic vs. extrinsic correction,   Mostly single-agent; does not
                                  Bench [24], Cannot Self-Correct [8], De-          error detection, revision, and re-    isolate reviewer–solver cou-
                                  composing Self-Correction [14]                    pair                                  pling across distinct agents
 Agent evaluation and cost-       AgentBench [15], Reasoning + Action               Outcome validity, cost account-       Lacks this paper’s inner/outer-
 aware benchmarking               evaluation [19], AI Agents That Matter [9],       ing, and benchmark discipline         loop decomposition on a
                                  rigorous benchmark design [38, 33]                                                      verifier-gated olympiad bench-
                                                                                                                          mark




analysis-side summary built from recorded wall times rather than a core runtime metric.
                                                                                N
                                                                       1 X
               AvgTokens ≡ AvgTotalTokens =                                  ti ,                                                                      (2)
                                                                       N i=1
                                                                                N
                                                                       1 X
                                        AvgModelCalls =                      ci ,                                                                      (3)
                                                                       N i=1
                                                                                N
                                                                       1 X        TotalEvaluatorAttempts
                            AvgEvalCalls/problem =                           ei =                        ,                                             (4)
                                                                       N i=1                N
                                                                                N
                                                                       1 X
                                          AvgWallClock =                     wi .                                                                      (5)
                                                                       N i=1

Tokens per extra solved problem (relative to a reference protocol). For a protocol p relative to a
reference protocol b (Baseline LLM in the main paper), evaluated on the same matched problem set,
we report the report-side derived quantity
                                                        P  (p)        (b)
                                                                           
                                                           i ti − ti
                    Tokens/ExtraSolved(p | b) = P                                .           (6)
                                                          final,(p)     final,(b)
                                                     i yi           − yi

On a matched set this is equivalent to the difference in average token cost divided by the difference in
final pass rate. It answers: how many additional generation tokens are spent, on average, for each
extra solved problem relative to the reference.

H.2     Outer-Loop Metrics

Cumulative and conditional recovery.
                                                                       N
                                                                 1 X
                                     OuterPass@k =                     1[yifinal = 1 ∧ ai ≤ k],                                                        (7)
                                                                 N i=1

               ∆@k ≡ MarginalRecoveryGaink = OuterPass@k − OuterPass@(k − 1),                                                                          (8)
                                                     OuterPass@k − OuterPass@(k − 1)
                                  CRR@k =                                            .                                                                 (9)
                                                          1 − OuterPass@(k − 1)

Attempt-sensitive accuracy.
                                                          N
                                                            (
                                                       1 X a1i ,                              yifinal = 1,
                                          MRRattempt =                                                                                               (10)
                                                       N i=1 0,                               otherwise.


                                                                        19
Correction scores.
                                                                               (
                                                                                       1
                                                                                   1+fi +λhi ,    yifinal = 1,
                           HintAwareCorrectionScorei =                                                                               (11)
                                                                                   0,             otherwise.

H.3    Inner-Loop Metrics

Transition rates.          Let
                                                                (0)          (1)
                                                  X
                                       Linner =            1[zi       and zi       are both labeled]                                 (12)
                                                      i

denote the number of labeled inner transitions.
                                                      (0)         (1)           P
                                                 i 1[zi    = 0 ∧ zi = 1]
                 RepairRate ≡ ReflectiveRepairRate =P        (0)
                                                                         ,          (13)
                                                        i 1[zi   = 0]
                                               P      (0)         (1)
                                                   1[z = 1 ∧ zi = 1]
PreservationRate ≡ ReflectivePreservationRate = i Pi         (0)
                                                                         ,          (14)
                                                        i 1[zi   = 1]
                                               P      (0)         (1)
                                                   1[z = 1 ∧ zi = 0]
             HarmRate ≡ ReflectiveHarmRate = i Pi            (0)
                                                                         ,          (15)
                                                        i 1[zi   = 1]
                                               P      (0)         (1)      P    (0)      (1)
                                                 i 1[zi    = 0 ∧ zi = 1] − i 1[zi = 1 ∧ zi = 0]
      NetRepairGain ≡ ReflectiveNetRepairGain =                                                                                             .
                                                                                                                  Linner
                                                                                                                                     (16)

NeglectRate and TryButFailRate (StillWrong decomposition).
                                   P     (0)        (1)     (0) (1)
                                      1[zi = 0 ∧ xi = xi ∧ zi = 0]
                   NeglectRate = i            P       (0)
                                                                    ,                                                                (17)
                                                i 1[zi    = 0]
                                   P     (0)        (1)     (0) (1)
                                      1[zi = 0 ∧ xi ̸= xi ∧ zi = 0]
                TryButFailRate = i            P       (0)
                                                                    .                                                                (18)
                                                i 1[zi    = 0]

      StillWrongTotal ≡ ReflectiveStillWrongRate = NeglectRate + TryButFailRate                                                      (19)
                                                 = 1 − RepairRate.                                                                   (20)
Neglect measures pure signal non-response (solver submits identical answer); TryButFail measures
effort without success—opposite implications for system design.

Table 9: Within-attempt reflective-refinement transitions, computed over all labeled inner-loop obser-
vations (one per outer-loop attempt per problem), not averaged by tier. RepairRate, NeglectRate, and
TryButFailRate are fractions over problems whose initial inner-loop candidate is wrong. NeglectRate
means the solver keeps the same wrong answer. TryButFailRate means the solver changes the
answer but it remains wrong. StillWrongTotal is the paper display label for ReflectiveStillWrongRate,
so Neglect plus TryButFail equals StillWrongTotal. NetRepairGain is the net correctness change
produced by the inner review loop: wrong-to-correct transitions minus correct-to-wrong transitions,
divided by the number of labeled inner-loop transitions. Tier-by-tier breakdowns are in Figure 9.
 Protocol                 RepairRate    NeglectRate       TryButFailRate    StillWrongTotal   PreservationRate   HarmRate   NetRepairGain
 PER (role-based)           11.0%         48.8%               40.2%             89.0%             96.5%           3.5%        +5.8 pp
 Broadcast deliberation     25.7%         26.2%               48.1%             74.3%             93.5%           6.5%        +6.7 pp



H.4    Review-Conditioned Decomposition

Define the count tensor:
                   N
                             (0)                              (1)
                   X
      Cu,r,v =            1[zi      = u ∧ ri = r ∧ zi               = v],      u, v ∈ {0, 1}, r ∈ {Revise, Agree}.                   (21)
                   i=1


                                                                       20
Reviewer detection counts.
                TP = C0,Revise,1 + C0,Revise,0 , FP = C1,Revise,1 + C1,Revise,0 ,                (22)
                FN = C0,Agree,1 + C0,Agree,0 , TN = C1,Agree,1 + C1,Agree,0 .                    (23)

Detection rates and response rates.
                                             TP                              TP
                                Precision =        ,            Recall =           ,             (24)
                                           TP + FP                         TP + FN
                                             FP
                                     FAR =         ,            BalAcc = 21 (Recall + 1 − FAR),
                                           FP + TN
                                                                                                 (25)
                                      C0,Revise,1
            ReviewerGuidedRepairRate =            ,                                              (26)
                                         TP
                                      C0,Revise,0
   ReviewerDetectedButNotFixedRate =              ,                                              (27)
                                         TP
                                      C1,Revise,1
     MisleadingReviewResistanceRate =             ,                                              (28)
                                         FP
                                      C1,Revise,0
          MisleadingReviewHarmRate =              .                                              (29)
                                         FP
Feedback-follow-through metrics and paper-facing aliases. The implementation also extracts
whether reviewer feedback produces an immediate answer transition in the next revision step. Here
“useful” and “misleading” are evaluator-verified properties of the pre-review candidate: useful revise
episodes begin from an evaluator-labeled wrong candidate, while misleading revise episodes begin
from an evaluator-labeled correct candidate. Let Felig denote eligible reviewer-feedback episodes,
Fuseful evaluator-verified useful revise-feedback episodes, and Fmislead evaluator-verified misleading
revise-feedback episodes.
                            ReviewerFeedback
                                                      #(followed feedback)                       (30)
                            IncorporationRate =                            .
                                                              Felig
         LegacyCouplingRate ≡ UsefulReviseFeedback
                                                              #(followed useful feedback)        (31)
                                     IncorporationRate =                                  .
                                                                       Fuseful
                      MisleadingReview
                                             #(followed misleading feedback)                    (32)
                      SusceptibilityRate =                                     .
                                                          Fmislead
In the main paper we shorten LegacyCouplingRate to CouplingRate, because this is the uptake statistic
used throughout the review-conditioned decomposition. Operationally, a useful revise episode i
is counted as followed if the extracted answer changes from the pre-review candidate a−    i to the
immediately following candidate a+i . Extraction is deterministic: we compare boxed  answers  when
present and otherwise compare normalized final-answer strings.
In the main-paper tables, MisleadingResistance is a shortened display label for MisleadingReviewRe-
sistanceRate. Likewise, CouplingRate is the paper-facing display label for the legacy uptake statistic
above. In plain language, CouplingRate is the fraction of evaluator-verified useful revise episodes in
which the immediately following candidate answer differs from the rejected pre-review answer. It is
therefore an answer-transition statistic, not a free-form human judgment about whether the solver
“really understood” the critique. ReviewerGuidedRepairRate and NeglectRate remain separate on
purpose: together they distinguish answer change, non-response, and realized repair rather than
collapsing them into a single uptake score. The stricter answer-transition audits used to test this
metric’s stability are front-loaded in Table 3.
If M = TP + FP + FN + TN is the total number of review-labeled instances, then the net quantity
used in the main-paper net-value comparison is
                                                   C0,Revise,1 − C1,Revise,0
                 NetCouplingValuePer1000 = 1000 ·                            .            (33)
                                                              M

                                                 21
This is equivalent to (TP × ReviewerGuidedRepairRate) − (FP × MisleadingReviewHarmRate)
per 1,000 review instances.

Table 10: Supplemental review-conditioned counts and detection summary. The main paper focuses
on precision, recall, coupling, and repair, so this appendix table reports the detection counts needed
to contextualize those quantities without introducing partially populated columns.

     Protocol                        Review instances      Precision     Recall     AvgEvalCalls/problem
     PER (role-based)                    10,804              0.861        0.754                2.19
     Broadcast deliberation              11,587              0.644        0.872                1.35



Table 11: Review-conditioned decomposition for the main PER and broadcast comparison. Precision
and Recall characterize reviewer detection quality. CouplingRate is the paper-facing immediate
answer-change statistic on evaluator-verified useful review episodes. ReviewerGuidedRepairRate
measures realized repair after reviewer-positive wrong cases. MisleadingResistance is the paper
display label for MisleadingReviewResistanceRate.

                                                  Coupling         ReviewerGuided             Misleading
    Protocol            Precision Recall            Rate             RepairRate               Resistance
    PER (role-based)         0.861     0.754       0.336                 0.051                   0.921
    Broadcast                0.644     0.872       0.935                 0.286                   0.708
    deliberation




I     Protocol Configurations

All descriptions in this appendix section refer to the matched paper configs rather than to alternate
development configs elsewhere in the broader codebase. Under those paper configs, every acting
role and the evaluator use gpt-oss-120b at temperature 0. Because gpt-oss-120b is public and
open-weight, reproducing the model access path does not require proprietary weights; the paper
abstracts only over the local OpenAI-compatible serving layer used to host the matched runs on
GPU-backed HPC infrastructure.

Table 12: Matched paper protocol knobs at a glance. This table is intended as a quick reference for
the exact comparison ladder used in the paper.

      Protocol    Outer         Inner/pre-submission         Feedback surface       Submission gate
                  budget        structure
      Baseline    1 outer       None                         Plain evaluator          Direct one-shot solver
      LLM         attempt                                    pass/fail only           submission
      Single-     Up to 3       No reviewer;                 Hinted evaluator         Same solver resubmits
      Agent       outer         question-scoped repair       feedback                 after each failure
      Iterative   attempts      ledgers                      plus prior submitted
                                reused across retries        answer
      PER         Up to 3       2 inner rounds per outer     Reviewer/evaluator       Reviewer can route back
                  outer         attempt:                     critique                 to Planner/Executor or
                  attempts      Planner→Executor→            routed through           approve submission
                                Reviewer                     separable
                                                             ${advice} fields
      Broadcast   Up to 3       4 discussion rounds          Shared candidate state Unanimous re-approval
                  outer         plus up to 2 approval        plus shared peer history before submission after
                  attempts      rounds                       and hinted evaluator     deliberation
                                                             feedback




                                                        22
I.1   Prompt Surfaces and Output Contracts

This subsection records the exact information surfaces that matter for scientific interpretation and for
reproduction. We do not print every full template inline because the release package will include the
exact config files, but we do make the visible fields and output contracts explicit.

Baseline LLM. The baseline solver sees only ${task_description} and is instructed to solve
in one shot. Its output contract is strict: the final two non-empty lines must be Final Answer:
<answer> and then \boxed{<answer>}. The evaluator sees ${task_description}, the extracted
solver submission ${solution}, and evaluator-only reference material ${result}; it must output
exactly Verdict, Correctness, and Response.

Single-Agent Iterative. The first attempt uses the same direct-solve interface as the baseline. Later
attempts additionally expose ${former_solution} and a compact question-scoped memory block
in ${advice} that summarizes prior failure information without revealing the gold answer. The
solver keeps the same two-line final-answer contract as the baseline. The evaluator contract is the
same as in the baseline, except that hinted repair feedback may be returned after a fixed FAIL verdict.

PER. PER uses three different acting prompt surfaces. The Planner sees ${task_description},
${previous_plan}, and ${advice}, and must open with a DELTA: section that states con-
crete plan updates without producing a final answer. The Executor sees ${task_description},
the Planner output in ${solution}, and ${advice}; its final line must be exactly one
\boxed{<answer>}. The Reviewer sees ${task_description}, ${previous_plan}, the cur-
rent candidate in ${preliminary_solution}, and ${advice}. It must emit a short diagnosis/fix
block and then exactly one final route tag: [Route:Planner], [Route:Executor], or [Agree].
A Final Answer For Evaluator block is allowed only on [Agree]. The evaluator again sees
only ${task_description}, the extracted candidate ${solution}, and evaluator-only reference
material ${result}.

Broadcast deliberation. Each deliberator sees ${task_description}, outer-loop feedback in
${advice}, the current shared candidate ${candidate_answer}, its role description, private
deferred notes ${private_memory}, a current turn label, its own speaking history, the current phase,
and a phase-specific instruction. Deliberators may emit confidence polls and may optionally propose
Candidate Answer: \boxed{<answer>} inside discussion. The shared transcript, candidate
state, and approval history together determine whether the protocol can submit. The evaluator contract
is parallel to PER: it judges the extracted final submission against evaluator-only reference material
and returns Verdict, Correctness, and Response.

Representative prompt excerpts. To make the paper-facing interface more concrete, we include
two short literal excerpts here. The release package will contain the full exact YAML templates.
         PER Reviewer excerpt. “You are the Reviewer in a Planner→Executor→Reviewer
         pipeline for difficult math problems.” The prompt then makes the routing contract ex-
         plicit: “If ${advice} contains a failure indicator such as FAIL or Score: False, you
         MUST end with ONLY [Route:Planner] or [Route:Executor]. You MUST NOT
         output [Agree].” It also fixes the response shape with a strict format of Diagnosis:, Fix
         Instruction:, an optional Final Answer For Evaluator: block only on agreement,
         and “End with EXACTLY ONE tag on the last line.”

         Broadcast deliberator excerpt. “You are one peer in a small math deliberation
         group.” The shared-state surface is then exposed directly: “Outer-loop feedback from
         the evaluator or prior attempt: ${advice}” and “Current shared candidate answer:
         ${candidate_answer}.” The prompt also makes proposal behavior explicit: “If
         you want the group to consider a concrete final answer, include Candidate Answer:
         \boxed{<answer>}.” The current phase and phase-specific instruction are visible in the
         same active prompt context as the candidate answer.

         Evaluator excerpt. “You are the Evaluator in a Planner→Executor→Reviewer loop for
         olympiad-style mathematics.” The prompt then fixes the judge contract: “Decide whether
         the submitted candidate final answer is mathematically equivalent to the ground truth,”
         “Do not reveal, quote, restate, or hint at the ground truth,” and “Output a clear verdict


                                                    23
         label: Verdict: PASS or Verdict: FAIL.” The required output footer is exactly three
         lines: Verdict: PASS or FAIL, Correctness: 0 or 1, and Response: <brief
         non-leaking repair hint>.

Answer extraction and normalization example. The paper-critical extraction path first takes the
last well-formed \boxed{...} answer if one exists; otherwise it falls back to the last non-empty line
and strips a trailing period. For example, if a solver ends with

         Final Answer:     1/2
          1/2 .

the extracted answer is 1/2. If no boxed answer is present and the final line is n \neq 5., the
fallback extractor returns n \neq 5. For numeric-only exact matching, commas are removed and
decimal strings are normalized through Decimal(...).normalize(), so strings such as 1, 1.0,
and 1. compare equal in the numeric path. Symbolic and set-valued Omni-MATH judgments
continue through the evaluator/rule path rather than this numeric-only fallback.

I.2   Reproducibility Artifact, Compute Path, and Asset Licenses

The acting/evaluator model is the public OpenAI checkpoint openai/gpt-oss-120b. In our paper
runs, those public weights are served through a public OpenAI-compatible inference endpoint on
GPU-backed HPC infrastructure, while paper-scale benchmark orchestration runs on standard GPU-
backed HPC nodes that submit batched benchmark shards to that endpoint rather than performing
model inference locally. Our jobs use the CPU side of those nodes while calling the remote inference
endpoint.
Paper-scale first-pass jobs use one mixed CPU/GPU node per submitted batch job, with worker
parallelism 10 for broadcast and 20 for PER, single-agent iterative, and baseline. Representative
first-pass batch-job wall times range from 00:27 to 03:53; the appendix and report artifact also record
per-tier/per-mode wall-clock summaries, while the main paper reports protocol-level token cost,
evaluator calls, and hard-tier wall-clock behavior.
The public release website is available at https://huggingface.co/spaces/AgentsSci/
scientific-agent-protocol-traces-site. Code and data will be released after institutional
approval. The staged release package will contain the exact paper-critical config, runtime, evaluation,
and reporting files needed to reproduce the matched benchmark results. The package is organized
around a shallow top level—README.md, configs/paper/, data/omni-math-2-filtered/,
couplingbench/, couplingbench_cli/, scripts/, report/, and figures/—so that readers
can see the paper-critical path immediately. Paper-scale throughput used public GPU-backed HPC in-
frastructure, but small-scale spot checks do not require those exact systems once the public checkpoint
is served through a compatible endpoint.

Reproduction path. The release package will support three reproduction levels. First, a smoke test
reruns any paper config on a small shard once openai/gpt-oss-120b is served through an OpenAI-
compatible endpoint. Second, a paper-scale rerun executes couplingbench_cli/benchmark.py
over the paper manifest or over tier shards and then rebuilds the aggregate report folders
with build_tier_mode_report_folder.py. Third, table and figure regeneration reruns the
RQ1/RQ2/RQ3 analysis scripts, the stricter coupling analysis, the problem-clustered bootstrap script,
the compact per-problem export script, and the associated plotting utilities over those rebuilt reports.
The lightweight package does not currently ship the full raw trace tree for the completed intervention
reruns; instead it includes paper-facing intervention summary CSVs alongside the main four-mode
aggregate tables. The exact commands, expected environment variables, packaged report-table
filenames, and example output directory structure will be listed in the release README.md.
We use only public assets. gpt-oss-120b is released under Apache 2.0 together with the OpenAI gpt-
oss usage policy [21, 20]. The public dataset cards for Omni-MATH (https://huggingface.co/
datasets/omniomni/omni-math) and Omni-MATH-2 (https://huggingface.co/datasets/
martheballon/Omni-MATH-2) list MIT licensing; in the paper we use the filtered Omni-MATH-2
subset described in Section 3.1 while crediting both the original Omni-MATH and Omni-MATH-2
benchmark authors [7, 2]. The evaluator replay and reduced cross-family addendum additionally use


                                                  24
Table 13: Staged release artifact inventory for the paper-critical runtime and analysis path. Paths are
relative to the release package root.

      Artifact path(s)                  Contents                                   Role in reproduction
      configs/paper/                    Exact matched configs for baseline,        Reproduces the protocol ladder and
                                        single-agent iterative, PER, broadcast,    within-PER intervention suite used in the
                                        ACK-required, and EMB (config key          paper
                                        embedded-advice)
      README.md plus top-level de-      Environment assumptions, smoke-test        Gives the release package an executable
      pendency files                    commands, full-benchmark command           entry point rather than only a file dump
                                        patterns, and analysis regeneration
                                        steps
      couplingbench_cli/                Main benchmark runner with trace and       Executes a paper config on a dataset
      benchmark.py                      artifact-copy support                      shard or full manifest
      couplingbench_cli/rq1_            RQ1 outcome/cost analysis                  Regenerates the main outcome and effi-
      outcome_cost.py                                                              ciency tables
      couplingbench_cli/rq2_            RQ2 recovery analysis                      Rebuilds OuterPass@k / CRR@k sum-
      recovery.py                                                                  maries
      couplingbench_cli/rq3_            Review-conditioned and collaboration-      Rebuilds the main RQ3 repair and cou-
      protocol_refinement.py,           decomposition analysis                     pling tables
      couplingbench_
      cli/collaboration_
      decomposition.py
      couplingbench_cli/                Stricter answer-transition robustness      Produces strict and equivalence-aware
      strict_coupling_rate.py           analysis                                   coupling summaries plus audit samples
      scripts/bootstrap_                Problem-level and problem-clustered        Recomputes paired PER–broadcast out-
      problem_clustered_                bootstrap uncertainty analysis over        come and mechanism intervals without
      metrics.py                        saved paper results                        rerunning model inference
      scripts/export_paper_             Compact per-problem outcome and            Lets reviewers inspect problem-level be-
      per_problem_tables.py             review-summary exports keyed by sta-       havior and reconnect aggregate tables
      plus report/per_problem/          ble paper IDs                              to individual benchmark items without
                                                                                   opening raw traces
      couplingbench/                    Evaluator logic, answer extraction, and    Fixes the evaluator contract and answer-
      evaluation/                       equivalence handling                       judging path
      scripts/preprocess_               Dataset filtering and manifest construc-   Recreates the exact 4,181-problem
      omni_math.py plus the paper       tion                                       benchmark slice and tier assignments
      manifest                                                                     used in the paper
      scripts/                          Batch orchestration and report rebuild-    Reconstructs top-level tier/mode report
                                        ing utilities                              folders and aggregate CSVs from per-
                                                                                   shard outputs
      report/     and    figure-input   Generated paper tables and figure in-      Lets readers verify the exact tables and
      CSVs                              puts packaged with the staged re-          plots shown in the paper without rerun-
                                        lease artifact, including compact per-     ning the full benchmark first
                                        problem tables and paper-facing inter-
                                        vention summaries
      figures/plot_all_                 Figure-regeneration helper over pack-      Rebuilds the paper-facing figures from
      figures.py                        aged report tables                         the saved aggregate CSVs



the public models Meta-Llama-3.1-70B-Instruct and gemma-3-27b-it for robustness analysis,
under their respective model licenses and usage terms.

I.3      Exact Within-PER Coupling Probe Details

This subsection makes the two within-PER interventions explicit at the prompt/interface level. Across
both variants, we keep the same model family, full benchmark, planner prompt, reviewer prompt,
evaluator contract, inner-round budget, and outer-loop budget. The only intended change is how
reviewer critique is surfaced to the downstream solver.

ACK-required. Base PER already routes reviewer/evaluator critique through a separable down-
stream advice field. The ACK-required variant keeps that routing path unchanged and flips the
paper-config control require_explicit_critique_uptake=true. Operationally, this augments
the solver-side instruction with a mandatory acknowledgment preface before the next candidate.
In the blind paper config, the solver is required to begin its response with a sentence of the form


                                                              25
“I acknowledge that the reviewer noted . . . ” and then provide the revised candidate. This probe
therefore tests whether verbal compliance enforcement alone can increase substantive uptake while
leaving the rest of the PER routing structure intact. A useful way to read the negative result is that the
new sentence creates an additional cheap completion target under the same routed-advice interface:
the solver can satisfy the acknowledgment requirement locally without making the critique bind on
the candidate state. In the main paper we therefore interpret its failure as being specific to this prompt
configuration rather than as proof that every acknowledgment-style control must fail.

EMB. EMB is the paper-facing short name for the config key embedded-advice. This variant
changes the critique surface rather than adding a new acknowledgment obligation. It flips the
paper-config control embed_action_feedback_in_history=true. Reviewer feedback is inserted
directly into the executor’s primary working context together with the current candidate, so the next
solver step reads the critique as part of the same active context used to generate the revision. The
role hierarchy remains planner–executor–reviewer, but critique is no longer presented only as a
separable role-local advice block. This is the smallest shared-context intervention we test inside the
PER family. It therefore probes whether a more shared feedback surface improves follow-through
and repair without switching all the way to full broadcast deliberation. When this variant improves
final outcomes without uniformly improving the narrower review-conditioned subset metrics relative
to base PER, we read that as an upstream-trajectory effect rather than a contradiction: the set of
evaluator-verified useful-review episodes is itself protocol-induced, so some of the end-to-end gain
can come from solving or simplifying trajectories before they enter that subset.

Controls held fixed across the probes. Across ACK-required and EMB, the acting/evaluator
model family, full benchmark, evaluator prompt, evaluator correctness contract, outer-loop budget,
inner-round budget, and PER role topology remain fixed. The intended manipulation is therefore the
critique-to-solver interface, not a change in model family, dataset coverage, or retry budget.

Completed suite status. The current intervention results in the main paper come from completed
full-benchmark reruns over all 4,181 problems. ACK-required and EMB remain directly comparable
on identical questions throughout the full benchmark. In the main paper we therefore use ACK-
required versus EMB as the cleanest within-family causal comparison, while also showing base
PER and broadcast as exact full-benchmark baselines to illustrate the broader Base PER → EMB →
Broadcast progression toward more directly shared feedback surfaces.

Table 14: Completed within-PER intervention suite aggregate over the full benchmark (N =
4,181). Base PER and broadcast are exact full-benchmark baselines; ACK-required and EMB
are directly matched on identical questions. UsefulCoupling is the paper-facing display label for
UsefulReviseFeedbackIncorporationRate. EMB should be read as the smallest shared-context step
inside PER rather than as a full replacement for broadcast-style shared deliberation.
                            Final          HintAware                        ReviewerGuided Useful
      Protocol             PassRate Pass@1 Correction AvgTokens NeglectRate     Repair     Coupling
      PER                   85.2%   72.8%    70.4%        400K     0.488          0.051        0.336
      PER + ACK-required    82.5%   71.0%    68.9%        402K     0.792          0.032        0.200
      PER + Embedded        86.3%   74.5%    72.0%        422K     0.698          0.044        0.247
      Broadcast             89.2%   78.6%    81.8%        616K     0.262          0.286        0.935



I.4     Broadcast Interaction Topology

The current broadcast protocol is best understood as a hybrid rather than as unrestricted open
discussion. Each discussion turn begins with a confidence poll from all deliberators. That poll
is used to choose a single public speaker for the turn, but it can also surface a candidate answer
before a long public exchange occurs. Once a current candidate exists, the protocol switches into
an all-peer approval phase in which every deliberator may approve, reject, or propose a revision.
Review-conditioned broadcast quantities in the paper therefore arise from this approval phase, not
from the one-speaker public discussion turns.
Candidate ownership in broadcast is similarly protocol-level rather than speaker-level. The current
candidate can be promoted from the selected speaker’s public message, from the selected speaker’s


                                                     26
Table 15: FinalPassRate by tier for the completed full-benchmark intervention suite. The small-bin
caution remains the same as in the main benchmark: tier 3 has n = 20 and tier 10 has n = 15, so
both should be interpreted cautiously.

                   Tier   Base PER     PER + ACK-required     PER + Embedded       Broadcast
                   1        99.1%             98.3%                99.1%            99.1%
                   2        95.0%             93.8%                94.8%            95.2%
                   3        85.0%             90.0%                90.0%            85.0%
                   4        88.0%             86.1%                89.6%            92.6%
                   5        82.7%             79.2%                84.7%            89.2%
                   6        79.3%             77.7%                80.7%            82.9%
                   7        76.8%             72.4%                76.8%            80.7%
                   8        83.5%             78.0%                82.9%            86.6%
                   9        82.2%             78.8%                82.9%            83.6%
                   10       73.3%             73.3%                86.7%            93.3%



poll candidate, or from the strongest poll candidate available at that turn; later, the approval stage may
replace it through the configured peer-revision rule. For the paper configs, this means that broadcast
should be read as a protocol that combines turn allocation, shared candidate state, and peer approval,
rather than as a simple “speaker proposes, group judges” loop.

Table 16: Critique routing and approval structure in PER and broadcast. This table summarizes
the protocol differences most relevant to the coupling gap: how critique is delivered, whether the
downstream candidate-producing role can bypass it, and what approval constraints apply before
submission. Because the protocols also differ in prompts and memory surfaces, the table should be
read as mechanistic support for the coupling interpretation, not as a pure ablation.

      Architectural dimension       PER                                Broadcast
      Reviewer signal delivery      Separable ${advice} field          Embedded in shared chat history
      Solver exposure to critique   Independent (can skip ${advice})   Mandatory (part of shared context)
      After verifier FAIL           Hard-route back to reviewer        Unanimous re-approval required
      Inner review rounds           2                                  4 discussion + 2 approval
      Approval policy               Planner–Executor decision          Unanimous (all deliberators)
      Decoupling risk               High                               Low



I.5     Implementation-Level Memory Contract

The main paper describes memory only at the level needed for scientific comparison. This subsection
records the implementation details that matter for reproducibility and for reviewer questions about
state visibility, persistence, and fairness.

Shared per-question repair ledgers. Single-Agent Iterative, PER, and broadcast all maintain
the same two structured question-scoped ledgers. The failed-attempt memory stores one compact
record per rejected evaluator submission: extracted submitted answer, evaluator signal, compact
evaluator hint, repair summary, and source stage. The candidate-revision memory stores a compact
trajectory of candidate proposals and revisions: event id, stage, source, action type, normalized
candidate answer, optional review or rationale text, optional parent revision link, and evaluator signal
when present. In the paper configs, the failed-attempt ledger keeps at most three records and the
candidate-revision ledger keeps at most five. These ledgers are the main mechanism that persists
repair-relevant information across outer attempts within a question.

Baseline LLM and Single-Agent Iterative. The one-shot baseline instantiates standard per-run
chat-memory objects for its solver and evaluator, but because the protocol has only one attempt it
does not populate any iterative repair ledger and never routes prior failure information back to the
solver. Single-Agent Iterative reuses the same solver/evaluator pattern, but before each new outer
attempt it explicitly resets the solver’s raw chat history. Cross-attempt persistence therefore comes
from the two structured question-level ledgers, not from carrying the full prior transcript forward.


                                                      27
This keeps retry behavior tied to compact rejected-answer and candidate-trajectory state rather than
to an ever-growing conversational context.


PER. PER uses the same failed-attempt and candidate-revision ledgers, but now shares them across
Planner, Executor, and Reviewer. Reviewer or evaluator feedback is routed into later role invocations
through the ${advice} field together with the current question-memory context, rather than through
a shared multi-agent transcript. In addition, the Planner and Reviewer use summary-enabled chat
history in the paper config: has_summary=true, summary updates every three messages, a 300-
token summary cap, and a 200-token recent-message budget. The Executor uses standard chat history
without summary compression. PER therefore combines shared structured repair memory with
role-local summarized conversational state.


Broadcast deliberation. Broadcast uses the same two shared question-level ledgers, but adds
protocol-specific per-deliberator state. Each deliberator maintains a public chat history rendered
through the summary_plus_recent path; a private deferred-note buffer capped at eight entries; that
agent’s own speaking-history buffer capped at eight labeled turns; and a current turn label. In the
current paper config, however, deliberators use chat_history without enabling learned summary
updates, so summary_plus_recent should be read as the chosen render path rather than as a true
running summary. In practice it supplies a bounded recent shared transcript view, with a five-message
fallback and heuristics that preserve messages around final-answer markers. The private notes are also
specific in purpose: they are deferred contribution notes created for non-selected, high-confidence
agents, storing the agent’s reason to speak and intended contribution when it was not chosen for the
public turn. The paper-config prompt surface exposes evaluator advice, the current shared candidate
answer, private deferred notes, current turn label, and own speaking history. This is the main memory
distinction between PER and broadcast. PER routes critique as role-specific advice inside a pipeline;
broadcast embeds critique and candidate evolution into shared peer discussion while still preserving
a small amount of agent-private context.


Reset semantics and evaluator-feedback routing. All question-scoped memories, raw chat his-
tories, summaries, deferred notes, and speaking histories are reset between dataset examples when
a new problem begins. Acting agents never receive ground-truth answers or official solutions. The
evaluator’s correctness verdict is computed from the extracted submitted final answer together with
evaluator-only reference material. If hint mode is enabled and the verdict is FAIL, a separate post-
verdict pass may read compact reasoning summaries to produce a non-answer-revealing repair hint,
but the correctness decision is already fixed before that hint step. In broadcast, the resulting evaluator
feedback is inserted into the shared deliberation memory as a public message and is also returned
as the next outer-round advice string. In Single-Agent Iterative and PER, the evaluator feedback is
returned as structured advice and reintroduced together with the question-level repair ledgers on the
next attempt.


Prompt-control interpretation. Neither PER nor broadcast instructs agents that reviewer signals
may be unreliable. The two protocols also use genuinely different role-specific prompt scaffolds and
memory surfaces, so we do not interpret their gap as a pure prompt-control ablation. Instead, under
matched paper configs, we treat the coupling difference as architectural evidence about how review
signals are routed, remembered, and acted on.


Blind-safe implementation and compute setup. All experiments in the paper configs were
executed through an OpenAI-compatible inference endpoint on GPU-backed HPC infrastructure, with
batched runs orchestrated over benchmark shards rather than by interactive single-problem prompting.
In the public release artifact path, this corresponds to public gpt-oss-120b weights served through a
public inference endpoint with paper-scale batch orchestration on public HPC compute. The scientific
conclusions do not depend on a particular serving stack: all protocols use the same acting model,
the same evaluator model, the same question set, and the same paper-config attempt budgets, while
protocol-level cost is reported directly through generated tokens, model/API calls, evaluator calls,
and wall-clock summaries.


                                                   28
I.6   Artifact Paths For Metric Reproduction

The matched experiment configs referenced throughout the paper live in the release package’s
configs/paper/ directory. The benchmark runner copies the resolved config into each run di-
rectory for traceability, while the main-paper metrics and review-conditioned summaries are repro-
duced through the analysis entry points listed in Table 13. In particular, RQ1 tables come from
rq1_outcome_cost.py, RQ2 recovery tables from rq2_recovery.py, the review-conditioned re-
pair tables from rq3_protocol_refinement.py and collaboration_decomposition.py, and
stricter answer-transition robustness from strict_coupling_rate.py. The figure-generation utili-
ties used for the draft are likewise included in the release package so that readers can regenerate both
the tables and the plots from the same matched paper runs.
For the two new “still wrong” metrics, the implementation logic is intentionally simple:

1. Filter to labeled inner-loop transitions with both initial and final correctness labels.
2. Restrict to transitions whose initial candidate is wrong.
3. Count Neglect when the final candidate is still wrong and the normalized final answer is unchanged
   from the initial one.
4. Count TryButFail when the final candidate is still wrong but the normalized final answer changed.
5. Divide both counts by the number of wrong-initial transitions to obtain NeglectRate and TryBut-
   FailRate.

This corresponds exactly to the implementation of the paper’s inner-loop met-
ric module:        ReflectiveNeglectRate is “wrong → same wrong answer,” while
ReflectiveTryButFailRate is “wrong → changed-but-still-wrong answer.” Readers who
want to port these metrics to another stack therefore need only candidate-answer normalization,
initial/final correctness labels, and review-episode boundaries rather than the full experimental
runtime.

J     Tier Sample Breakdown and Domain Distribution
       • Full per-tier problem counts, domain distribution, and sample size notes.
       • The ten-tier difficulty axis is inherited from the original Omni-MATH metadata rather than
         constructed solely for LLM benchmarking. In Omni-MATH, the benchmark designers first
         organize sources by real Olympiad/contest hierarchy, then assign per-problem difficulty
         scores mainly from AoPS community ratings; only problems not covered by AoPS:Ratings
         receive GPT-4o-based difficulty assignment [7]. Omni-MATH 2-Filtered keeps these inher-
         ited metadata while cleaning solvability and evaluation issues [2].
       • As a result, the tier variable is a hybrid metadata scale: mostly human- and community-
         grounded, with limited LLM assistance for missing ratings. The resulting tier imbalance
         is inherited from the benchmark distribution itself rather than introduced by our protocol
         evaluation. The tier axis is therefore useful for stratified analysis, but it should not be
         overread as a perfectly smooth model-calibrated latent difficulty axis. This is one reason
         local wiggles in tier-wise protocol curves are not, by themselves, unexpected.
       • Per-tier counts in the filtered benchmark are: tier 1 = 116, tier 2 = 517, tier 3 = 20, tier 4 =
         1,106, tier 5 = 1,078, tier 6 = 497, tier 7 = 358, tier 8 = 328, tier 9 = 146, tier 10 = 15.
       • Tiers 3 and 10 are especially small and should be interpreted cautiously; tier 1 is moderate
         rather than tiny, and tiers 2 and 4–9 are well populated.
       • Domain metadata are retained as fine-grained sub-domain paths from Omni-MATH-2-
         filtered; any coarser rollups such as number theory, combinatorics, algebra, geometry,
         analysis, and other are analysis-side aggregations rather than raw dataset labels.

K     Difficulty-Tier Extended Results
       • Full per-tier FinalPassRate, Pass@1, OuterPass@k, CRR@k for all protocols.


                                                   29
                                            (a) OuterPass@k                                        (b) CRR@k (conditional recovery)                                               (c) CRR@2 by tier (hard-tier reversal)
                                                                                                                                                               80%
                       100%                                                              100%                                                                                                                                        Single-Agent
                                                                     89.2%                                                                                     70%                                                                   PER
                              78.6%                                  85.2%                       78.6%                                                                                                                               Broadcast
                       80%                                                               80%                                                                   60%                                                 BC 51%


Cumulative pass rate
                              72.8%                                  78.8%                       72.8%
                                                                                                                             Broadcast advantage               50%
                                                                                                                             concentrates at k = 1;
                       60%                                                               60%




                                                                                                                                                       CRR@2
                                                                                 CRR@k
                                                                                                                             k 2 single-agent                  40%
                              57.4%                                                              57.4%

                       40%                                                               40%                                                                   30%
                                                                                                                                                               20%                                                          SA 31%
                       20%         Single-Agent                                          20%          Single-Agent                                             10%
                                   PER                                                                PER
                                   Broadcast                                                          Broadcast                                                 0%   Gray = small-N tiers (3, 10; n 20)
                        0%                                                                0%
                               1                  2              3                                1                     2                     3                       1       2        3       4          5    6     7        8        9     10
                                          Outer-loop attempt k                                               Outer-loop attempt k                                                                  Difficulty tier


Figure 7: (a) Cumulative outer-loop pass rate across three outer attempts. (b) Conditional recovery
rate at attempt k (CRR@k), meaning the probability of solving the problem at attempt k given failure
on all earlier attempts. Broadcast’s advantage concentrates at the first attempt (78.6% first-pass
success), while CRR@2 is nearly tied with Single-Agent (37.2% vs. 37.0%). This makes CRR@2
the key quantity when verifier calls are expensive: a second verifier call helps only if the protocol is
meaningfully more likely to solve the problem on that attempt. (c) CRR@2 by difficulty tier. The
aggregate tie hides a large broadcast advantage on hard tiers 7–10, including about a 20 percentage
point gap on tier 9. Gray bands mark the small-N tiers (3 and 10; n ≤ 20).


                              • CRR@2 by tier (main paper Figure 7(c)) reveals the difficulty-gated broadcast advantage:
                                tiers 7–10 show broadcast CRR@2 consistently above single-agent; tier 9: broadcast 50.8%,
                                single 30.8%.
                              • Figure 10 (below) shows the full-size aggregate recovery curves (panels (a) and (b) of
                                Figure 7).
                              • Figure 9 shows inner-loop transition rates (RepairRate, NeglectRate, TryButFailRate) per
                                tier for PER and broadcast.


Table 17: Verifier-guided outer-loop recovery under hinted feedback (default), N = 4,181, with at
most three outer attempts. ∆@k is the increase in cumulative pass rate from attempt k−1 to attempt
k, measured in percentage points. CRR@k is the probability of solving at attempt k given failure on
all prior attempts. OuterPass@3 equals FinalPassRate for each protocol.
                 Protocol                                 OuterPass@1                      ∆@2 (pp)                  OuterPass@2                  ∆@3 (pp)                OuterPass@3                         CRR@2               CRR@3
                 Single-Agent Iterative                          57.4%                          +15.7                  73.2%                          +5.6                     78.8%                          37.0%               21.0%
                 PER (role-based)                                72.8%                          + 8.8                  81.6%                          +3.5                     85.2%                          32.4%               19.3%
                 Broadcast deliberation                          78.6%                          + 8.0                  86.6%                          +2.7                     89.2%                          37.2%               19.7%




Table 18: Final pass rate, in percent, by protocol and difficulty tier. Bold values mark the highest
accuracy within each tier. A horizontal rule separates easy tiers (1–3) from medium and hard tiers
(4–10). Broadcast is the accuracy leader on tiers 4–10, while the protocols stay within 5 percentage
points of one another on the easy tiers. Gray entries show the one-shot Baseline LLM.

                                                                             Tier           Baseline                 Single            PER             Broadcast
                                                                             1                           93                 99              99                         99
                                                                             2                           87                 93              95                         95
                                                                             3                           60                 80              85                         85
                                                                             4                           70                 86              88                         93
                                                                             5                           56                 78              83                         89
                                                                             6                           38                 69              79                         83
                                                                             7                           29                 61              77                         81
                                                                             8                           30                 69              84                         87
                                                                             9                           21                 66              82                         84
                                                                             10                          20                 53              73                         93




                                                                                                                        30
Table 19: Protocol guidance by difficulty-tier group. “Best accuracy” is the protocol with the highest
FinalPassRate. “Cost-efficient alternative” is the cheapest protocol within 5 percentage points of that
best result. Guidance is split by verifier-cost regime. On tiers 4–10, broadcast is the accuracy leader,
while PER is the cost-efficient fallback when verifier calls are cheap.
    Tier group              Best accuracy              Cost-efficient alt. (≤5 pp gap)   Cheap verifier                          Expensive verifier
    Easy (tier 1–3)         Single / PER / Broadcast   Baseline or Single                Use Baseline or Single                  Use Single (high CRR@1, low token cost)
    Medium (tier 4–7)       Broadcast                  PER                               Use PER (1.5× cheaper than Broadcast)   Use Broadcast (highest OuterPass@1)
    Hard (tier 8–10)        Broadcast                  PER                               Use PER if budget-constrained           Use Broadcast (highest first-pass rate)




                          Final Pass Rate by Protocol and Difficulty Tier (RQ4)
                                       * = best protocol per tier
                   Tier 1     93%          99%           99%           99%                                                                              100%
                   Tier 2              87%                         93%                           95%                       95%
                   Tier 3              60%                          80%                          85%                       85%                          80%

                   Tier 4              70%                          86%                          88%                       93%
                                                                                                                                                        60%




                                                                                                                                                                 Final pass rate
Difficulty tier




                   Tier 5              56%                          78%                          83%                       89%

                   Tier 6              38%                          69%                          79%                       83%
                                                                                                                                                        40%
                   Tier 7              29%                          61%                          77%                       81%

                   Tier 8              30%                          69%                          84%                       87%                          20%
                   Tier 9              21%                          66%                          82%                       84%

                  Tier 10              20%                          53%                          73%                       93%                          0%
                                  Baseline                Single-Agent      PER                                      Broadcast
                                                                   Protocol
Figure 8: FinalPassRate heatmap by protocol and difficulty tier. Each cell shows the percentage of
problems solved, and darker color means higher accuracy. Broadcast is the accuracy leader from tier
4 onward; the protocols cluster within 5 percentage points on easy tiers 1–3. Tiers 3 and 10, marked
with gray borders, have small sample sizes (n ≤ 20) and should be interpreted cautiously.


L                 NeglectRate by Tier and Tier-Stratified Signal Routing

Figure 11 shows the two coupling-mechanism metrics that most directly explain the PER–broadcast
repair gap: NeglectRate (left) and RepairRate (right), stratified by difficulty tier with 95% Wilson
confidence intervals. Dashed horizontal lines mark the pooled aggregate values reported in Table 9.
The NeglectRate panel shows that PER’s neglect is structurally elevated across the full difficulty
range, not concentrated at a single tier. For tiers 4–9 (the well-populated tiers, IQR 0.45–0.51), PER’s
NeglectRate is consistently above 0.44, while broadcast’s IQR is 0.16–0.29. The RepairRate panel
mirrors this: broadcast’s repair advantage is visible at every tier, and the gap persists even at the
hardest well-populated tiers (7–9) where problems are presumably harder and all protocols struggle.
Together these two panels support the structural interpretation of Finding A: the coupling gap is not
an artefact of easy problems where review is unnecessary, nor of a few extreme tiers, but a consistent
property of PER’s architecture across the full difficulty spectrum sampled by this benchmark.


                                                                                         31
                                                                Inner-Loop Transition Rates by Difficulty Tier (RQ3, Finding A & G)
                                              Neglect Rate                                                            Repair Rate                                                                                                 Try-but-Fail Rate
                100%                                                                         100%                                                                                                              100%
                                                                                                                                                   PER
                                                                                                                                                   Broadcast
                       80%                                                                   80%                                                                                                               80%




                                                                                                                                                                                           Try-but-Fail Rate
Neglect Rate




                                                                               Repair Rate
                       60%                                                                   60%                                                                                                               60%

                       40%                                                                   40%                                                                                                               40%

                       20%                                                                   20%                                                                                                               20%
                                                   PER                                                                                                                                                                                   PER
                                                   Broadcast                                                                                                                                                                             Broadcast
                       0%                                                                     0%                                                                                                                0%
                              1   2     3     4   5    6    7   8       9 10                         1    2    3     4                      5                         6    7   8   9 10                               1   2   3    4    5    6    7   8       9 10
                                              Difficulty tier                                                        Difficulty tier                                                                                                Difficulty tier
                                                                                               Gray shading = small-N tiers (3, 10; n 20 problems)


Figure 9: Inner-loop transition rates by difficulty tier for PER and Broadcast. The three rates are
RepairRate, NeglectRate, and TryButFailRate. PER’s NeglectRate stays substantially higher across
the benchmark, ranging from 0.44 to 0.78; over the better-populated tiers 4–9, the middle 50% of
PER values lie between 0.45 and 0.51, compared with 0.16 to 0.29 for Broadcast. Because the paper
configs do not vary by tier, this gap is consistent with a structural rather than difficulty-specific
explanation.

                                                                                               Outer-Loop Recovery (RQ2)
                                                  Cumulative OuterPass@k                                                 CRR@k (prob. of solving at k | failed k 1)                        Conditional Recovery Rate@k
                       100%                                                                                                                                           100%                                                                       Single-Agent
                                                                                                          89.2%                                                                                                                                  PER
                                      78.6%                                                               85.2%                                                                    78.6%                                                         Broadcast
Cumulative pass rate




                        80%           72.8%                                                               78.8%                                                       80%          72.8%
                                                                                                                                                                                                                                         Broadcast's advantage
                        60%                                                                                                                                           60%                                                                concentrates at k=1;
                                      57.4%                                                                                                                                        57.4%                                                 k=2 single-agent
                        40%                                                                                                                                           40%
                                            Single-Agent
                        20%                 PER                                                                                                                       20%
                                            Broadcast
                         0%                                                                                                                                               0%
                                       1                            2                                 3                                                                             1                                         2                           3
                                                       Outer-loop attempt k                                                                                                                                     Outer-loop attempt k

Figure 10: Outer-loop recovery curves for Single-Agent Iterative, PER, and Broadcast across three
outer attempts. The left panel shows cumulative pass rate after each attempt. The right panel shows
conditional recovery rate, meaning the probability of solving the problem on attempt k given failure
on all earlier attempts. Broadcast achieves the highest cumulative pass rate, while its conditional
recovery advantage over Single-Agent is concentrated on harder tiers rather than appearing uniformly
at every attempt.


                             • Per-tier NeglectRate for PER (consistently 0.44–0.78) and Broadcast (0.00–0.50); confidence
                               intervals are widest at tiers 3 and 10 due to small N .
                             • Full tier-stratified reviewer confusion: TP/FP/FN/TN counts per tier per protocol.


M                            Efficiency: Evaluator Calls and Wall-Clock Time
M.1                          Explicit Verifier-Cost Threshold Model

To make RQ4 operational, we scalarize each protocol p by its average generation-token cost Tp ,
average verifier-call count Vp , and final success rate Ap . A simple deployment objective is expected
cost per solved problem:
                                                      Tp + λVp
                                         Kp (λ) =               ,
                                                         Ap
where λ is the cost of one verifier call measured in generation-token units. The numerator is the
expected scalarized cost incurred on one benchmark problem under protocol p, and the division by Ap


                                                                                                                     32
                                                                       Coupling Mechanism by Difficulty Tier: NeglectRate and RepairRate (RQ3)


NeglectRate (wrong initial, no revision attempted)




                                                                                                                            RepairRate (wrong initial, corrected by review)
                                                                       NeglectRate by difficulty tier                                                                                        RepairRate by difficulty tier
                                                     100%                                                                                                                     100%
                                                                                                                                                                                                              PER
                                                                                                                                                                                                              Broadcast
                                                     80%                                                                                                                      80%

                                                     60%                                                                                                                      60%

                                                     40%                                                                                                                      40%

                                                     20%                                                                                                                      20%
                                                                                           PER
                                                                                           Broadcast
                                                      0%                                                                                                                       0%
                                                            1      2    3       4      5       6       7   8     9    10                                                             1   2   3    4      5        6       7   8   9   10
                                                                                    Difficulty tier                                                                                                   Difficulty tier
                                                                            Shaded bands = 95% Wilson CI. Dashed lines = pooled aggregate. Gray = small-N tiers (3, 10; n 20).


Figure 11: NeglectRate (left) and RepairRate (right) by difficulty tier for PER and Broadcast. Shaded
bands show 95% Wilson confidence intervals computed from per-tier transition counts, and dashed
horizontal lines show the pooled aggregate values from Table 9. Gray bands mark the small-N tiers 3
and 10 (n ≤ 20). PER’s NeglectRate stays elevated across the full difficulty range, while Broadcast’s
RepairRate advantage appears at every tier. The gap does not narrow on the hard tiers, where the
role-specialization hypothesis would predict structured review to help most.

                                                                Reviewer Detection Quality by Tier (RQ3): PER more precise, Broadcast higher recall
                                                                       Reviewer Precision by Tier                                                                                            Reviewer Recall by Tier
                                                     100%                                                                                                                     100%

                                                      80%                                                                                                                     80%
Precision




                                                      60%                                                                                                                     60%
                                                                                                                            Recall




                                                      40%                                                                                                                     40%

                                                      20%                                                                                                                     20%
                                                                                           PER                                                                                                               PER
                                                      0%                                   Broadcast                                                                           0%                            Broadcast
                                                            1      2    3       4       5      6       7   8     9     10                                                            1   2   3    4       5       6       7   8   9   10
                                                                                    Difficulty tier                                                                                                   Difficulty tier

Figure 12: Reviewer confusion matrix proportions (TP/FP/FN/TN) by difficulty tier for all protocols.


converts that into expected cost per successful final solve. Equivalently, over N benchmark problems
the protocol incurs total expected cost N (Tp + λVp ) and returns N Ap successful final solves, so the
ratio simplifies to the expression above. This is intended as a compact decision aid rather than as a
claim that deployment should optimize only one scalar objective. In particular, it treats token cost
and verifier cost explicitly, while leaving factors such as implementation preference for explicit role
structure outside the objective.
For settings where remaining wrong at the end is itself costly, a richer extension is
                                                                                                Jp (λ, µ) = Tp + λVp + µ(1 − Ap ),
where µ is the penalty for final failure. Here the objective is not “cost per solved problem,” but
expected scalarized deployment loss per benchmark problem: generation cost, plus verifier cost,
plus a failure penalty charged exactly when the final output is wrong. This second form is closer to
autonomous-science or engineering settings in which an incorrect final output can waste a simulation,
robot cycle, or wet-lab assay. The simple Kp (λ) model is enough for the paper’s main crossover
calculations, while Jp (λ, µ) clarifies why high-failure-penalty domains push toward more accurate
first-pass protocols even before verifier costs become dominant.


                                                                                                                            33
                                        Reviewer Quality: FAR and CouplingRate by Difficulty Tier (RQ3)
                                      Reviewer FAR by Tier                            Reviewer-Solver CouplingRate by Tier
                   (FP / (FP+TN): fraction of correct answers wrongly flagged) (fraction of TP cases where solver actually revises)
                         100%
                                                     PER                                          100%
                                                     Broadcast
                         80%
False Alarm Rate (FAR)

                                                                                                  80%




                                                                                   CouplingRate
                         60%
                                                                                                  60%
                         40%                                                                      40%
                                                                                                             PER
                         20%                                                                      20%        Broadcast
                                                                                                             PER agg. 0.335
                                                                                                             BC agg. 0.934
                          0%                                                                       0%
                                1   2   3   4      5     6        7   8   9   10                         1    2     3     4      5     6        7   8   9   10
                                                Difficulty tier                                                               Difficulty tier

Figure 13: Reviewer false alarm rate (FAR) by difficulty tier. FAR measures the fraction of correct
answers incorrectly flagged for revision. PER has lower FAR and thus higher precision, but higher
NeglectRate.

Table 20: Verifier-cost
                       crossover thresholds under the simple cost-per-solved objective Kp (λ) =
 Tp + λVp /Ap , using the full-benchmark aggregates from Table 1. Here λ⋆ is the verifier-call cost,
measured in generation-token units, at which the two protocols tie.

           Comparison                               λ⋆ (tokens / verifier          Interpretation
                                                    call)
           PER vs. Broadcast                        ≈ 2.1 × 105                    Below this threshold, PER is cheaper per solved problem
                                                                                   on the scalarized objective; above it, Broadcast’s higher
                                                                                   success rate and lower verifier-call count outweigh its
                                                                                   larger generation budget.
           Single-Agent vs. Broad-                  ≈ 9.9 × 105                    Broadcast only overtakes single-agent when verifier calls
           cast                                                                    are extremely expensive relative to generation, because
                                                                                   single-agent is far cheaper in tokens but has lower first-
                                                                                   pass and final success.
           Single-Agent vs. PER                     no positive crossover          Under this scalarized objective, single-agent remains
                                                                                   cheaper per solved problem on the full-benchmark ag-
                                                                                   gregates. PER is therefore best read as a structured inter-
                                                                                   mediate design point rather than as the global minimizer
                                                                                   of Kp (λ) under the current paper configs.



                            • Full per-tier AvgEvalCalls/problem showing PER issues 1.57–1.79× more verifier calls than
                              broadcast.
                            • Wall-clock time per problem by tier: PER tier 9 = 795 s, broadcast = 668 s; PER tier 10 =
                              2,021 s, broadcast = 519 s (4× inflation).
                            • Verifier-cost breakeven analysis: the full-benchmark scalarized crossover occurs at roughly
                              2.1 × 105 token-equivalent units per verifier call for PER vs. broadcast, and at roughly
                              9.9 × 105 for single-agent vs. broadcast (Table 20).
                            • Table 21 adds tier-group versions of the same crossover, showing that the verifier-cost
                              decision boundary moves with difficulty instead of staying fixed at the global aggregate.
                            • Figure 14 shows the raw cost–performance frontier and first-pass rate by tier; Figure 15
                              extends that view to the scalarized Kp (λ) crossover curves with a difficulty-conditioned
                              regime-strip chart.
                            • Figure 17 shows per-tier AvgEvalCalls/problem; Figure 18 shows wall-clock time per
                              problem by tier.
                            • Figure 16 shows the harm-aware protocol decision map under Jp (λ, µ) for tiers 7–10,
                              illustrating when a failure-penalty dimension makes PER a viable compromise.


                                                                                   34
Table 21: Difficulty-aware
                             verifier-cost crossover thresholds under the same objective Kp (λ) =
  Tp + λVp /Ap . Tier-group aggregates are problem-count weighted, P        not simple
                                                                                   P averages over
tier-level
P          metrics:
                 P   for each   group   G, we
                                           P    compute  T p,G
                                                           P    =        N   T
                                                                      t∈G t p,t  /   t∈G Nt , Vp,G =
        N  V
   t∈G t p,t   /       N
                   t∈G t   , and  A p,G =         N A
                                              t∈G t p,t  /        N
                                                              t∈G t ,  where N t is the number of an-
alyzed problems in tier t. The group sizes are N1–4 = 1,759, N5–6 = 1,575, and N7–10 = 847. The
overall row reproduces the full-benchmark aggregate; the grouped rows expose how the scalarized
crossover shifts with difficulty.

           Tier group                           PER vs. Broadcast λ⋆         Single-Agent                                vs.     Interpretation
                                                                             Broadcast λ⋆
           Overall                              ≈ 2.08 × 105                 ≈ 9.88 × 105                                        Full-benchmark aggregate used by
                                                                                                                                 Figure 15.
           Tiers 1–4                            ≈ 1.32 × 105                 ≈ 1.05 × 106                                        On easier problems, broadcast
                                                                                                                                 needs a relatively lower verifier-
                                                                                                                                 cost premium than in the global av-
                                                                                                                                 erage to overtake PER, but single-
                                                                                                                                 agent remains hard to dislodge.
           Tiers 5–6                            ≈ 1.92 × 105                 ≈ 1.04 × 106                                        Mid-difficulty problems already
                                                                                                                                 move the PER/broadcast crossover
                                                                                                                                 upward relative to tiers 1–4.
           Tiers 7–10                           ≈ 2.89 × 105                 ≈ 7.18 × 105                                        Hard tiers shift the PER/broadcast
                                                                                                                                 crossover furthest right while mak-
                                                                                                                                 ing broadcast competitive against
                                                                                                                                 single-agent at a lower verifier-
                                                                                                                                 cost threshold.



                        • Figure 19 provides the full multi-metric overview.

                                  (a) Cost Performance Frontier                                                                        (b) Pass@1 by Tier
                                                                                                           100%
                  90%                                               Broadcast
                                                                                First-pass rate (Pass@1)




                                                              PER                                          80%
Final pass rate




                  80%                         Single-Agent
                                                                                                           60%
                  70%         PER: 2.19 eval calls/problem
                              Broadcast: 1.35 eval calls/problem
                                 o1-mini 60.5%                                                             40%          Baseline
                  60% Baseline                                                                                          Single-Agent
                                                                                                           20%          PER
                  50%                                                                                             Gray =Broadcast
                                                                                                                         small-N tiers (3, 10; n 20)
                                                                                                            0%
                        104                         105                106                                         1      2      3      4      5       6      7   8   9   10
                                 Avg tokens / problem (log scale)                                                                           Difficulty tier

Figure 14: (a) Raw cost–performance frontier. Generation tokens per problem versus FinalPassRate
for all four protocols. Single-Agent achieves the best tokens-per-extra-solved-problem ratio; PER
and Broadcast incur substantially higher generation costs for their respective accuracy gains. Notably,
PER is not simply intermediate in cost: it uses more verifier calls per problem than Broadcast (2.19
vs. 1.35), as annotated in the figure, so it is verifier-heavier despite generating fewer tokens overall.
Dashed reference: o1-mini 60.5%. (b) First-pass rate (Pass@1) by difficulty tier. Broadcast’s
first-pass advantage over PER and Single-Agent opens at harder tiers. Gray bands mark small-N
tiers (tiers 3 and 10, n ≤ 20). Figure 15 extends this raw view to the scalarized Kp (λ) model where
verifier-call cost λ is varied explicitly.


N                   Headline Outcome Confidence Intervals
Appendix Table 3 gives the pooled audit counts behind this robustness check. For both PER and
broadcast, StrictLegacyDisagreementRate is 0, so the stricter deterministic answer-transition
definition agrees exactly with the paper-facing CouplingRate on all eligible useful-revise episodes.
We therefore use the strict audit as a measurement-stability check, not as a replacement metric.


                                                                                   35
                                                   (a) Full-benchmark aggregate Kp( )                                                      (b) Low- zoom




    cost per solved problem (K tokens)
                                                                 Single                    Broadcast
                                                                cheapest                   cheapest            1000
                                                                             PER/BC
                                         104     Single-Agent                2.1×10    SA/BC
                                                                                       9.9×10
                                                 PER
                                                 Broadcast

                                         103                                                                    500



                                         102                                                                                                             Single-Agent stays cheapest
                                                                                                                                                      throughout this zoomed regime
                                                                                                                 50
    Kp( )




                                           103        104            105           106                 107         103                      104                      105
                                                  Verifier cost (token-equivalents per call)                                   Verifier cost (token-equivalents per call)

                                                                                      (c) Who wins where (by difficulty group)
          Overall

  Tiers 1 4

  Tiers 5 6

 Tiers 7 10
                                                        104                                                   105                                                       106
                                                                                        Verifier cost (token-equivalents per call)

Figure 15: Verifier-cost crossover analysis under the scalarized objective Kp (λ) = (Tp + λVp )/Ap .
Panel (a): full-benchmark curves for all three protocols. Broadcast overtakes PER when one verifier
call costs about 2.1 × 105 token-equivalent units, and overtakes Single-Agent at about 9.9 × 105 .
Under this objective, PER never becomes cheaper than Single-Agent. Panel (b): separate low-verifier-
cost zoom, showing more clearly the regime in which Single-Agent remains cheapest. Panel (c):
difficulty-conditioned winner strip chart, with one row for the full benchmark and one for each tier
group. Blue means Single-Agent is cheapest; green means Broadcast is cheapest; the orange diamond
marks the PER/Broadcast pairwise crossover, not the actual winner switch. The main takeaway is
that the Single-Agent/Broadcast boundary moves leftward on the hard tiers 7–10, making Broadcast
defensible at a lower verifier cost for harder problems.


Table 22: Overall outcome uncertainty over N = 4,181 problems. FinalPassRate and Pass@1
intervals are 95% Wilson intervals over per-problem success indicators. The Broadcast–PER gap
intervals are 95% Newcombe intervals for the difference in independent proportions. These intervals
capture per-problem sampling uncertainty under the fixed paper configs; they do not substitute for
multi-seed variance across different stochastic runs.
                                                    Protocol                                   FinalPassRate (95% CI)            Pass@1 (95% CI)
                                                    Baseline LLM (one-shot)                      56.8% [55.2, 58.3]             56.8% [55.2, 58.3]
                                                    Single-Agent Iterative                       78.8% [77.5, 80.0]             57.4% [55.9, 58.9]
                                                    PER (role-based MAS)                         85.2% [84.1, 86.2]             72.8% [71.5, 74.2]
                                                    Broadcast deliberation                       89.2% [88.2, 90.1]             78.6% [77.3, 79.8]
                                                    Broadcast − PER gap                           4.0 pp [2.6, 5.5]                  5.8 pp [3.9, 7.6]




O                                        Literature Context: Published Omni-MATH Accuracy

                                          • Published single-model accuracy numbers on Omni-MATH for reference context only.
                                            Evaluator setup, prompting, problem subset, and test-time budget are not matched to this
                                            paper’s experiments.

                                          • Do not treat these as direct comparisons; they establish benchmark headroom motivation.



                                                                                                        36
            Failure/harm penalty (token-equivalents per unsolved problem)
                                                                                        Harm-Aware Protocol Decision Map Tiers 7 10
                                                                                     Jp( , ) = Tp + Vp + (1 Ap); color = cheapest protocol
                                                                            14M

                                                                            12M                                                                     Expensive verifier
                                                                                                                                                    & high-harm stakes
                                                                            10M
                                                                                                                    Cheap verifier,
                                                                            8M                                     high-harm stakes


                                                                            6M                            PER
                                                                                                        cheapest                                    Broadcast
                                                                                                                                                    cheapest
                                                                            4M
                                                                                                    Single-Agent
                                                                            2M                        cheapest
                                                                                     Cheap                                                          Expensive
                                                                                    verifier,                                                        verifier
                                                                                    low risk
                                                                            0M
                                                                              103                      104                     105                                  106
                                                                                                Verifier cost (token-equivalents per call)
                                                                                                  Single-Agent cheapest        Broadcast cheapest
                                                                                                  PER cheapest

Figure 16: Harm-aware protocol decision map for tiers 7–10 under the richer scalarized objective
Jp (λ, µ) = Tp + λVp + µ(1 − Ap ), where λ is verifier cost and µ is the per-problem failure penalty.
Color shows which protocol minimizes Jp . On the hard-tier aggregate (tiers 7–10), PER has a visible
preference region at moderate µ and low-to-moderate λ, meaning it can be the best compromise
when mistakes carry substantial downstream cost but verifier calls are not yet extremely expensive.
Broadcast dominates at high λ or very high µ; Single-Agent dominates at low λ and low µ. On
the full-benchmark aggregate, the PER preference region collapses to near-empty; the hard-tier
conditioning shown here is required to expose the PER-as-compromise scenario.

Table 23: Episode-level uncertainty for the main review-conditioned rates. CouplingRate is the
paper-facing immediate answer-change rate on evaluator-verified useful review episodes. Intervals
are 95% Wilson intervals over pooled eligible review episodes; the Broadcast–PER CouplingRate
gap uses a 95% Newcombe interval. Because multiple review episodes can come from the same
problem across outer attempts, these should be read as descriptive episode-level uncertainty rather
than as fully independent problem-level variance estimates.
 Protocol                                                                           CouplingRate (95% CI)     ReviewerGuidedRepairRate (95% CI)     MisleadingResistance (95% CI)
 PER (role-based MAS)                                                                  33.6% [32.3, 34.9]               5.1% [4.5, 5.7]                   92.1% [90.1, 93.7]
 Broadcast deliberation                                                                93.5% [92.8, 94.1]             28.6% [27.4, 29.9]                  70.8% [69.1, 72.4]
 Broadcast − PER Coupling gap                                                          59.9 pp [57.9, 61.8]                   —                                   —




P    Trace Examples

The examples in this section are illustrative mechanism traces, not prevalence estimates. We selected
them from the matched paper results directory using pre-specified criteria: we first preferred mid-
tier cases (tiers 5–7), then preferred same-question PER/broadcast pairs when available, and then
prioritized visible mechanism over dramatic outcome. For PER, the target pattern was substantively
useful reviewer signal / solver-or-submission-unrepaired / evaluator-FAIL. For broadcast, the target
pattern was visible peer critique followed by an explicit protocol candidate update and re-approval of
the revised candidate. We found three same-question tier-6 pairs where PER failed and broadcast
passed, but the cleanest reviewer-neglect trace and the cleanest visible candidate-revision trace did
not coincide on a single problem, so the two excerpts below come from different mid-tier problems.
All frequency claims in the paper remain metric-based.


                                                                                                                 37
                                    Verifier Call Count by Tier and Protocol (Finding E)
                  PER issues 1.57-1.79x more verifier calls than Broadcast despite higher generation cost

                        Avg evaluator (verifier) calls per problem
                                                                     6          Baseline
                                                                                Single-Agent
                                                                                PER
                                                                     5          Broadcast

                                                                     4
                                                                                                                                         PER: 2.87
                                                                     3

                                                                     2

                                                                     1                                                                   Broadcast: 1.64
                                                                            1        2         3       4         5         6         7        8          9        10
                                                                                                               Difficulty tier

Figure 17: Average evaluator (verifier) calls per problem by difficulty tier and protocol. Across tiers
4–9, PER issues about 1.6 to 1.8 times as many verifier calls as Broadcast.
Avg wall-clock time per problem (seconds, log scale)




                                                                                        Wall-Clock Time per Problem by Tier (Finding F)
                                                                                PER tier 10: 2021 s vs. Broadcast 519 s 4x wall-clockPER:
                                                                                                                                       inflation
                                                                                                                                           2021s
                                                                                    Single-Agent
                                                       1000s                        PER
                                                                                    Broadcast

                                                                                                                                                             Broadcast: 519s
                                                                     100s




                                                                      10s

                                                                                1        2         3       4           5         6        7          8        9        10
                                                                                                                     Difficulty tier
Figure 18: Wall-clock time per problem by difficulty tier and protocol. At tier 10, PER averages
2,021 seconds per problem versus 519 seconds for Broadcast, or about four times as long. The gap is
driven by PER’s higher evaluator-call frequency and sequential reviewer–solver turns.


For readability, the monospaced blocks below preserve stage labels and trace wording while eliding
unrelated algebra; any bracketed stage tags and surrounding interpretation are ours.

P.1                                                                  PER: Correct Review Signal, Unrepaired Submission

This tier-5 PER trace shows the decoupling pattern directly. The reviewer twice identifies a real
flaw in the current derivation, and the second review even proposes a materially different threshold,
but the submitted answer remains the earlier wrong candidate. This is the mechanism counted by


                                                                                                                     38
                                                                       Comprehensive Multi-Metric Overview by Difficulty Tier (All Protocols)
                                   Final Pass Rate by Tier                                                                     First-Pass Rate (OuterPass@1) by Tier                                                                   Avg Tokens per Problem by Tier
                100%                                                                                         100%                                                         Baseline                                1000K
                                                                                                                                                                          Single-Agent
                 90%                                                                                          90%                                                         PER




                                                                                                                                                                                         Avg tokens (thousands)
                 80%                                                                                          80%                                                         Broadcast
FinalPassRate

                 70%                                                                                          70%
                                                                                                                                                                                                                  100K




                                                                                      Pass@1
                 60%                                                                                          60%
                 50%                                                                                          50%
                 40%        Baseline                                                                          40%                                                                                                                                            Baseline
                 30%        Single-Agent                                                                      30%                                                                                                     10K                                    Single-Agent
                            PER                                                                                                                                                                                                                              PER
                 20%        Broadcast                                                                         20%                                                                                                                                            Broadcast
                       1     2     3       4       5       6       7    8    9   10                                        1     2    3     4       5    6        7   8      9     10                                             1    2     3       4       5    6        7   8   9   10
                                               Difficulty tier                                                                                  Difficulty tier                                                                                          Difficulty tier
                           NeglectRate by Tier (RQ3, Finding A)                                                                  CRR@2 by Tier (RQ2, Finding C)                                                                 Avg Verifier Calls/Problem by Tier (Finding E)
                 80%                                                                                                                                                                                                                  Baseline
                                                                                                                     80%                                                                                                  3.0
                                                                                                                                                                                                                                      Single-Agent




                                                                                       Conditional Recovery Rate@2
                 70%
                                                                                                                                                                                                                                      PER
                 60%                                                                                                                                                                                                                  Broadcast
                                                                                                                     60%                                                                                                  2.5
                 50%




                                                                                                                                                                                                           AvgEvalCalls
   NeglectRate




                 40%                                                                                                 40%                                                                                                  2.0
                 30%
                 20%                                                                                                 20%                                                                                                  1.5
                 10%                                                                                                                                Single-Agent
                                                       PER                                                                                          PER
                  0%                                   Broadcast                                                     0%                             Broadcast                                                             1.0
                       1     2     3       4       5       6       7    8    9   10                                        1     2    3     4       5    6        7   8      9     10                                             1    2     3       4       5    6        7   8   9   10
                                               Difficulty tier                                                                                  Difficulty tier                                                                                          Difficulty tier


Figure 19: Multi-metric overview across all tiers and protocols. The panels show FinalPassRate,
Pass@1, pass rate after two outer attempts, pass rate after three outer attempts, average generated
tokens, and average evaluator calls per problem. This figure is intended as a quick cross-reference for
the paper’s four research questions.

Table 24: Paired problem-clustered bootstrap uncertainty for the main PER–broadcast gaps. Each
bootstrap replicate resamples the shared problem IDs with replacement and recomputes all associated
per-problem outcomes or review-conditioned episodes jointly, preserving within-problem clustering.
Intervals are 95% percentile intervals over 500 bootstrap replicates on the matched 4,181-problem
set.
          Metric                                                            PER (clustered 95% CI)                                        Broadcast (clustered 95% CI)                                              Broadcast − PER gap (clustered 95% CI)
          FinalPassRate                                                       85.2% [84.0, 86.2]                                                  89.2% [88.3, 90.1]                                                                     +4.0 pp [3.1, 4.9]
          Pass@1                                                              72.8% [71.6, 74.0]                                                  78.6% [77.5, 79.8]                                                                     +5.8 pp [4.7, 7.0]
          CouplingRate                                                        33.6% [32.2, 35.0]                                                  93.5% [92.9, 94.1]                                                                   +59.9 pp [58.2, 61.4]
          ReviewerGuidedRepairRate                                              5.1% [4.4, 5.7]                                                   28.6% [26.7, 30.7]                                                                   +23.5 pp [21.7, 25.5]
          Strict CouplingRate                                                 33.6% [32.4, 35.1]                                                  93.5% [92.9, 94.1]                                                                   +59.9 pp [58.2, 61.4]
          RepairGivenChangeRate                                               15.1% [13.5, 17.2]                                                  30.6% [28.7, 32.6]                                                                   +15.4 pp [13.0, 18.2]
          MisleadingResistance                                                92.1% [89.8, 94.0]                                                  70.8% [68.4, 73.0]                                                                  −21.3 pp [−24.0, −18.6]
          MisleadingReviewSusceptibility                                      19.9% [17.2, 22.7]                                                  64.8% [63.0, 66.6]                                                                   +45.0 pp [41.8, 48.3]



N EGLECT R ATE: a substantively useful review signal exists, but it does not become the answer
actually sent to the evaluator.

Problem context. The task asks for the largest initial value a0 such that the recurrence an+1 =
              n
a2n −2−(2020·2 −1) remains bounded. The evaluator label for this run is 1+ 22020
                                                                             1
                                                                                 , while the submitted
answer is 1 .

                            [reviewer_0] Diagnosis: Lemma 1 incorrectly claims a1 ≥ 0 for every
                            a0 ; in fact a1 = a20 − ε0 can be negative. ... [Route:Executor]
                            [executor_1] ... Thus the largest real number for which the
                            sequence remains bounded is 1 .
                            [reviewer_1] Diagnosis: The argument that any initial value greater
                                                                                            √
                            than 1 yields an unbounded sequence is incorrect; for 1 < a0 ≤ 1 + ε0
                            we have a1 ≤ 1 and the sequence remains bounded. ... Change final
                                              p
                            boxed answer to       1 + 2−2019 . [Route:Planner]
                             [evaluation_submission] Actual extracted final answer sent to
                             evaluator: 1
                             [evaluation] Evaluation signal: FAIL


                                                                                                                                                39
                                Reviewer detection coupling repair profile
                                          (PER vs.\ Broadcast)
                                                    Precision                         PER
                                                                                      Broadcast
                                                                      1.0
                                                            0.750.8
                                                          0.87
                                                                0.6
                         Misleading          0.93            0.4
                                                                                   Recall
                         Resistance                 0.34 0.2

                                                      0.64
                                                      0.86




                                  Reviewer                              Coupling
                                   Guided                                 Rate
                                   Repair

Figure 20: Five-dimensional detection–coupling–repair profile for PER (dashed orange) and Broad-
cast (solid green). Axes show raw values on a 0–1 scale. PER dominates on Precision (0.861
vs. 0.644) and MisleadingResistance (0.921 vs. 0.708); Broadcast dominates on Recall (0.872 vs.
0.754), CouplingRate (0.935 vs. 0.336), and ReviewerGuidedRepairRate (0.286 vs. 0.051). The
shape difference makes the precision–repair gap concrete: the protocols diverge most sharply on the
coupling and repair dimensions, not on the detection dimensions alone.

Table 25: Published Omni-MATH overall final pass rates [7] alongside this paper’s four protocols.
Reference rows are context only; experimental conditions are not matched.

   System                                                             Overall FinalPassRate
   Published single-model references [7]
   Meta-Llama-3.1-70B-Instruct                                                 24.2%
   GPT-4o                                                                      30.5%
   Qwen2.5-MATH-72B-Instruct                                                   36.2%
   OpenAI o1-preview                                                           52.6%
   OpenAI o1-mini                                                              60.5%
   This paper (gpt-oss-120b, N = 4,181; baseline plain feedback, iterative/collaborative modes hinted)
   Baseline LLM (one-shot)                                     56.8%
   Single-Agent Iterative                                      78.8%
   PER (role-based MAS)                                        85.2%
   Broadcast deliberation                                      89.2%



The key point is not just that PER fails. The decisive detail is that the reviewer-generated correction
remains a separable signal rather than becoming the active submission state. Even after a concrete
corrected answer appears in the review channel, the pipeline still submits the earlier candidate. This
is exactly the reviewer–solver uncoupling mechanism that the main text isolates.

P.2   Broadcast: Peer Critique Replaces the Live Candidate

This tier-6 broadcast trace shows the complementary mechanism. The first public answer enters
review with an overly large endpoint, peer approval produces a correction proposal, and the system
explicitly replaces the current candidate before the next approval round. The corrected candidate is
then the object of further scrutiny and is ultimately accepted by the evaluator.

Problem context. The task asks for all possible final values after repeatedly pairing the numbers
1, . . . , 1024 and replacing each pair by its non-negative difference. The final accepted answer in this
run is {0, 2, 4, . . . , 1022} .


                                                         40
         [poll_0 / Mira] Candidate Answer:             {0, 2, 4, . . . , 524800}

         [poll_0 / Talia] Candidate Answer:             {0, 2, 4, . . . , 1022}

         [discussion_0 / Mira] Candidate enters review as {0, 2, 4, . . . , 1024}

         [approval_0 / Talia] Proposed Correction:                {0, 2, 4, . . . , 1022}
         [system] Protocol candidate update. Previous Candidate:
          {0, 2, 4, . . . , 1024} . Current Candidate For Further Review:
          {0, 2, 4, . . . , 1022} .

         [approval_1 / Rowan] approve {0, 2, 4, . . . , 1022}

         [approval_1 / Talia] approve {0, 2, 4, . . . , 1022}
         [evaluation] PASS

This is the coupling pattern that the paper attributes to broadcast. The critique is not merely attached
as external advice to a solver role. It becomes shared protocol state: the current candidate itself is
replaced, re-reviewed, and then submitted in revised form. Even though the surrounding discussion
is short, the repair signal is embedded in the live candidate trajectory rather than being left as a
side-channel comment.

Q    Process Diagnostics (Flagged Subsets)
       • The main quantitative metrics are computed over the full evaluated set whenever candidate
         labels are available. Looping, drift, early convergence, wrong convergence, and productive
         convergence are diagnostic categories for flagged subsets of traces, not headline metrics.
       • Diagnostic flag criteria and planned reporting role:
            – Looping: repeated boxed answers, repeated review routes, >2 turns with no candidate
               change.
            – Drift: candidate revisions move away from problem constraints or abandon useful
               verifier feedback.
            – Early convergence: agreement reached with fewer than 2 distinct candidates; low
               substantive revision count.
            – Wrong convergence: unanimous approval followed by verifier FAIL.
            – Productive convergence: unanimous approval followed by verifier PASS.
       • Role-specific trace slices: useful objection, error preservation, neglected errors, and redun-
         dant repetition.
       • Cross-protocol: compare how interaction structure shapes reasoning trajectory shape (not
         just final answer), including where structured review produces targeted refinement and
         where peer deliberation yields useful diversity vs. harmful drift [6, 25, 19].




                                                  41
NeurIPS Paper Checklist
    1. Claims
      Question: Do the main claims made in the abstract and introduction accurately reflect the
      paper’s contributions and scope?
      Answer: [Yes]
      Justification: The abstract and introduction state the paper as a mechanism-focused evalu-
      ation of reviewer–solver coupling, not as a new SOTA method, and explicitly qualify the
      claims to matched configs and verifier-grounded math (Abstract; Secs. 1 and 7).
      Guidelines:
         • The answer [N/A] means that the abstract and introduction do not include the claims
           made in the paper.
         • The abstract and/or introduction should clearly state the claims made, including the
           contributions made in the paper and important assumptions and limitations. A [No] or
           [N/A] answer to this question will not be perceived well by the reviewers.
         • The claims made should match theoretical and experimental results, and reflect how
           much the results can be expected to generalize to other settings.
         • It is fine to include aspirational goals as motivation as long as it is clear that these goals
           are not attained by the paper.
    2. Limitations
      Question: Does the paper discuss the limitations of the work performed by the authors?
      Answer: [Yes]
      Justification: The paper includes a dedicated limitations section covering domain scope,
      shared-model dependence, prompt/interface scope, token cost, and trace-parsed diagnostics
      (Sec. 7).
      Guidelines:
         • The answer [N/A] means that the paper has no limitation while the answer [No] means
           that the paper has limitations, but those are not discussed in the paper.
         • The authors are encouraged to create a separate “Limitations” section in their paper.
         • The paper should point out any strong assumptions and how robust the results are to
           violations of these assumptions (e.g., independence assumptions, noiseless settings,
           model well-specification, asymptotic approximations only holding locally). The authors
           should reflect on how these assumptions might be violated in practice and what the
           implications would be.
         • The authors should reflect on the scope of the claims made, e.g., if the approach was
           only tested on a few datasets or with a few runs. In general, empirical results often
           depend on implicit assumptions, which should be articulated.
         • The authors should reflect on the factors that influence the performance of the approach.
           For example, a facial recognition algorithm may perform poorly when image resolution
           is low or images are taken in low lighting. Or a speech-to-text system might not be
           used reliably to provide closed captions for online lectures because it fails to handle
           technical jargon.
         • The authors should discuss the computational efficiency of the proposed algorithms
           and how they scale with dataset size.
         • If applicable, the authors should discuss possible limitations of their approach to
           address problems of privacy and fairness.
         • While the authors might fear that complete honesty about limitations might be used by
           reviewers as grounds for rejection, a worse outcome might be that reviewers discover
           limitations that aren’t acknowledged in the paper. The authors should use their best
           judgment and recognize that individual actions in favor of transparency play an impor-
           tant role in developing norms that preserve the integrity of the community. Reviewers
           will be specifically instructed to not penalize honesty concerning limitations.
    3. Theory assumptions and proofs


                                                 42
   Question: For each theoretical result, does the paper provide the full set of assumptions and
   a complete (and correct) proof?
   Answer: [N/A]
   Justification: The paper is empirical and does not claim formal theorems or proofs.
   Guidelines:
      • The answer [N/A] means that the paper does not include theoretical results.
      • All the theorems, formulas, and proofs in the paper should be numbered and cross-
         referenced.
      • All assumptions should be clearly stated or referenced in the statement of any theorems.
      • The proofs can either appear in the main paper or the supplemental material, but if
         they appear in the supplemental material, the authors are encouraged to provide a short
         proof sketch to provide intuition.
      • Inversely, any informal proof provided in the core of the paper should be complemented
         by formal proofs provided in appendix or supplemental material.
      • Theorems and Lemmas that the proof relies upon should be properly referenced.
4. Experimental result reproducibility
   Question: Does the paper fully disclose all the information needed to reproduce the main ex-
   perimental results of the paper to the extent that it affects the main claims and/or conclusions
   of the paper (regardless of whether the code and data are provided or not)?
   Answer: [Yes]
   Justification: We disclose the public benchmark, matched protocol structure, evaluator
   contract, budgets, temperature-0 paper configs, prompt-surface/output contracts, routing
   and memory details, and concrete reproduction paths. The paper includes a public release
   website; code and data will be released after institutional approval. The actor/evaluator
   model gpt-oss-120b is public and open-weight rather than a private API-only dependency,
   and the reported runs host those public weights on GPU-backed HPC infrastructure through
   an OpenAI-compatible server (Secs. 3–4; App. B, App. I, and App. I.2).
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • If the paper includes experiments, a [No] answer to this question will not be perceived
         well by the reviewers: Making the paper reproducible is important, regardless of
         whether the code and data are provided or not.
      • If the contribution is a dataset and/or model, the authors should describe the steps taken
         to make their results reproducible or verifiable.
      • Depending on the contribution, reproducibility can be accomplished in various ways.
         For example, if the contribution is a novel architecture, describing the architecture fully
         might suffice, or if the contribution is a specific model and empirical evaluation, it may
         be necessary to either make it possible for others to replicate the model with the same
         dataset, or provide access to the model. In general. releasing code and data is often
         one good way to accomplish this, but reproducibility can also be provided via detailed
         instructions for how to replicate the results, access to a hosted model (e.g., in the case
         of a large language model), releasing of a model checkpoint, or other means that are
         appropriate to the research performed.
      • While NeurIPS does not require releasing code, the conference does require all submis-
         sions to provide some reasonable avenue for reproducibility, which may depend on the
         nature of the contribution. For example
        (a) If the contribution is primarily a new algorithm, the paper should make it clear how
             to reproduce that algorithm.
        (b) If the contribution is primarily a new model architecture, the paper should describe
             the architecture clearly and fully.
        (c) If the contribution is a new model (e.g., a large language model), then there should
             either be a way to access this model for reproducing the results or a way to reproduce
             the model (e.g., with an open-source dataset or instructions for how to construct
             the dataset).


                                             43
       (d) We recognize that reproducibility may be tricky in some cases, in which case
           authors are welcome to describe the particular way they provide for reproducibility.
           In the case of closed-source models, it may be that access to the model is limited in
           some way (e.g., to registered users), but it should be possible for other researchers
           to have some path to reproducing or verifying the results.
5. Open access to data and code
   Question: Does the paper provide open access to the data and code, with sufficient instruc-
   tions to faithfully reproduce the main experimental results, as described in supplemental
   material?
  Answer: [No]
  Justification: The benchmark inputs are public, and the paper links the public release website.
  Code and data will be released after institutional approval. The appendix lists the planned
  artifact contents and relative paths for the staged release package (App. I.2 and App. I.6).
   Guidelines:
      • The answer [N/A] means that paper does not include experiments requiring code.
      • Please see the NeurIPS code and data submission guidelines (https://neurips.cc/
        public/guides/CodeSubmissionPolicy) for more details.
      • While we encourage the release of code and data, we understand that this might not
        be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not
        including code, unless this is central to the contribution (e.g., for a new open-source
        benchmark).
      • The instructions should contain the exact command and environment needed to run to
        reproduce the results. See the NeurIPS code and data submission guidelines (https:
        //neurips.cc/public/guides/CodeSubmissionPolicy) for more details.
      • The authors should provide instructions on data access and preparation, including how
        to access the raw data, preprocessed data, intermediate data, and generated data, etc.
      • The authors should provide scripts to reproduce all experimental results for the new
        proposed method and baselines. If only a subset of experiments are reproducible, they
        should state which ones are omitted from the script and why.
      • For public release, the authors should release institutionally approved public versions
        when applicable.
      • Providing as much information as possible in supplemental material (appended to the
        paper) is recommended, but including URLs to data and code is permitted.
6. Experimental setting/details
   Question: Does the paper specify all the training and test details (e.g., data splits, hyperpa-
   rameters, how they were chosen, type of optimizer) necessary to understand the results?
  Answer: [Yes]
  Justification: The paper and appendix specify the benchmark, matched protocol ladder,
  outer/inner-loop budgets, evaluator contract, model family, temperature, and protocol-
  specific memory/routing details needed to understand the results (Secs. 3–5; App. B and
  App. I.5).
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The experimental setting should be presented in the core of the paper to a level of detail
        that is necessary to appreciate the results and make sense of them.
      • The full details can be provided either with the code, in appendix, or as supplemental
        material.
7. Experiment statistical significance
   Question: Does the paper report error bars suitably and correctly defined or other appropriate
   information about the statistical significance of the experiments?
  Answer: [Yes]


                                            44
   Justification: The paper now reports headline 95% confidence intervals for FinalPassRate
   and Pass@1, including a Newcombe interval for the Broadcast–PER gap, and the appendix
   reports Wilson intervals for tier-wise NeglectRate and related diagnostics together with the
   assumptions behind those intervals (Sec. 5; App. N and App. L).
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The authors should answer [Yes] if the results are accompanied by error bars, confidence
         intervals, or statistical significance tests, at least for the experiments that support the
         main claims of the paper.
      • The factors of variability that the error bars are capturing should be clearly stated (for
         example, train/test split, initialization, random drawing of some parameter, or overall
         run with given experimental conditions).
      • The method for calculating the error bars should be explained (closed form formula,
         call to a library function, bootstrap, etc.)
      • The assumptions made should be given (e.g., Normally distributed errors).
      • It should be clear whether the error bar is the standard deviation or the standard error
         of the mean.
      • It is OK to report 1-sigma error bars, but one should state it. The authors should
         preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis
         of Normality of errors is not verified.
      • For asymmetric distributions, the authors should be careful not to show in tables or
         figures symmetric error bars that would yield results that are out of range (e.g., negative
         error rates).
      • If error bars are reported in tables or plots, the authors should explain in the text how
         they were calculated and reference the corresponding figures or tables in the text.
8. Experiments compute resources
   Question: For each experiment, does the paper provide sufficient information on the com-
   puter resources (type of compute workers, memory, time of execution) needed to reproduce
   the experiments?
   Answer: [Yes]
   Justification: The appendix now records the concrete compute path: public gpt-oss-120b
   weights served through a public OpenAI-compatible inference endpoint on GPU-backed
   HPC infrastructure, standard GPU-backed orchestration nodes used only for benchmark
   coordination, worker parallelism by protocol, and representative first-pass wall-clock times,
   while the main paper reports protocol-level token, evaluator-call, and hard-tier wall-clock
   costs (Sec. 5; App. I.2 and App. I.5).
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The paper should indicate the type of compute workers CPU or GPU, internal cluster,
         or cloud provider, including relevant memory and storage.
      • The paper should provide the amount of compute required for each of the individual
         experimental runs as well as estimate the total compute.
      • The paper should disclose whether the full research project required more compute
         than the experiments reported in the paper (e.g., preliminary or failed experiments that
         didn’t make it into the paper).
9. Code of ethics
   Question: Does the research conducted in the paper conform, in every respect, with the
   NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?
   Answer: [Yes]
   Justification: The work is a benchmark-based protocol evaluation with no human subjects,
   no deceptive data collection, and an explicit discussion of limitations and broader impacts
   (Sec. 7).
   Guidelines:


                                             45
       • The answer [N/A] means that the authors have not reviewed the NeurIPS Code of
          Ethics.
       • If the authors answer [No], they should explain the special circumstances that require a
          deviation from the Code of Ethics.
       • The authors should make sure institutional, legal, and release-review requirements are
          satisfied.
10. Broader impacts
    Question: Does the paper discuss both potential positive societal impacts and negative
    societal impacts of the work performed?
    Answer: [Yes]
    Justification: The paper includes a broader-impact discussion covering both the positive
    value of coupling-aware evaluation and the potential capability gains from stronger feedback
    uptake (Sec. 7).
    Guidelines:
       • The answer [N/A] means that there is no societal impact of the work performed.
       • If the authors answer [N/A] or [No], they should explain why their work has no societal
          impact or why the paper does not address societal impact.
       • Examples of negative societal impacts include potential malicious or unintended uses
         (e.g., disinformation, generating fake profiles, surveillance), fairness considerations
         (e.g., deployment of technologies that could make decisions that unfairly impact specific
          groups), privacy considerations, and security considerations.
       • The conference expects that many papers will be foundational research and not tied
          to particular applications, let alone deployments. However, if there is a direct path to
          any negative applications, the authors should point it out. For example, it is legitimate
          to point out that an improvement in the quality of generative models could be used to
          generate Deepfakes for disinformation. On the other hand, it is not needed to point out
          that a generic algorithm for optimizing neural networks could enable people to train
          models that generate Deepfakes faster.
       • The authors should consider possible harms that could arise when the technology is
          being used as intended and functioning correctly, harms that could arise when the
          technology is being used as intended but gives incorrect results, and harms following
          from (intentional or unintentional) misuse of the technology.
       • If there are negative societal impacts, the authors could also discuss possible mitigation
          strategies (e.g., gated release of models, providing defenses in addition to attacks,
          mechanisms for monitoring misuse, mechanisms to monitor how a system learns from
          feedback over time, improving the efficiency and accessibility of ML).
11. Safeguards
    Question: Does the paper describe safeguards that have been put in place for responsible
    release of data or models that have a high risk for misuse (e.g., pre-trained language models,
    image generators, or scraped datasets)?
    Answer: [N/A]
    Justification: The paper does not release a new model, new scraped dataset, or other high-
    misuse asset.
    Guidelines:
       • The answer [N/A] means that the paper poses no such risks.
       • Released models that have a high risk for misuse or dual-use should be released with
          necessary safeguards to allow for controlled use of the model, for example by requiring
          that users adhere to usage guidelines or restrictions to access the model or implementing
          safety filters.
       • Datasets that have been scraped from the Internet could pose safety risks. The authors
          should describe how they avoided releasing unsafe images.
       • We recognize that providing effective safeguards is challenging, and many papers do
          not require this, but we encourage authors to take this into account and make a best
          faith effort.


                                             46
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [Yes]
    Justification: The paper and appendix explicitly credit and document the external assets
    used in the experiments: gpt-oss-120b is identified as a public OpenAI checkpoint
    released under Apache 2.0 with the OpenAI usage policy; the public Omni-MATH / Omni-
    MATH-2 dataset cards used for benchmarking are cited and noted as MIT-licensed; and
    the auxiliary public models used only for evaluator replay and cross-family robustness
    checks (Meta-Llama-3.1-70B-Instruct and gemma-3-27b-it) are also credited and
    used subject to their respective model licenses and usage terms. The benchmark papers and
    repositories are credited directly (Sec. 3; App. I.2 and App. B).
    Guidelines:
       • The answer [N/A] means that the paper does not use existing assets.
       • The authors should cite the original paper that produced the code package or dataset.
       • The authors should state which version of the asset is used and, if possible, include a
          URL.
       • The name of the license (e.g., CC-BY 4.0) should be included for each asset.
       • For scraped data from a particular source (e.g., website), the copyright and terms of
          service of that source should be provided.
       • If assets are released, the license, copyright information, and terms of use in the
          package should be provided. For popular datasets, paperswithcode.com/datasets
          has curated licenses for some datasets. Their licensing guide can help determine the
          license of a dataset.
       • For existing datasets that are re-packaged, both the original license and the license of
          the derived asset (if it has changed) should be provided.
       • If this information is not available online, the authors are encouraged to reach out to
          the asset’s creators.
13. New assets
    Question: Are new assets introduced in the paper well documented and is the documentation
    provided alongside the assets?
    Answer: [Yes]
    Justification: The staged reproducibility artifact is planned to contain the exact paper configs,
    prompt-bearing YAMLs, compact per-problem tables, analysis scripts, packaged report
    tables, and reproduction instructions. It does not introduce a new model or dataset, but the
    planned release artifact is documented alongside the paper (App. I.2).
    Guidelines:
       • The answer [N/A] means that the paper does not release new assets.
       • Researchers should communicate the details of the dataset/code/model as part of their
          submissions via structured templates. This includes details about training, license,
          limitations, etc.
       • The paper should discuss whether and how consent was obtained from people whose
          asset is used.
       • For public release, remember to use approved public assets when applicable.
14. Crowdsourcing and research with human subjects
    Question: For crowdsourcing experiments and research with human subjects, does the paper
    include the full text of instructions given to participants and screenshots, if applicable, as
    well as details about compensation (if any)?
    Answer: [N/A]
    Justification: The paper does not involve crowdsourcing or research with human subjects.
    Guidelines:


                                              47
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
          with human subjects.
       • Including this information in the supplemental material is fine, but if the main contribu-
          tion of the paper involves human subjects, then as much detail as possible should be
          included in the main paper.
       • According to the NeurIPS Code of Ethics, workers involved in data collection, curation,
          or other labor should be paid at least the minimum wage in the country of the data
          collector.
15. Institutional review board (IRB) approvals or equivalent for research with human
    subjects
    Question: Does the paper describe potential risks incurred by study participants, whether
    such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
    approvals (or an equivalent approval/review based on the requirements of your country or
    institution) were obtained?
    Answer: [N/A]
    Justification: The paper does not involve crowdsourcing or research with human subjects.
    Guidelines:
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
          with human subjects.
       • Depending on the country in which research is conducted, IRB approval (or equivalent)
          may be required for any human subjects research. If you obtained IRB approval, you
          should clearly state this in the paper.
       • We recognize that the procedures for this may vary significantly between institutions
          and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the
          guidelines for their institution.
       • For public release, include institutional information only after the relevant review
          requirements are satisfied.
16. Declaration of LLM usage
    Question: Does the paper describe the usage of LLMs if it is an important, original, or
    non-standard component of the core methods in this research? Note that if the LLM is used
    only for writing, editing, or formatting purposes and does not impact the core methodology,
    scientific rigor, or originality of the research, declaration is not required.
    Answer: [Yes]
    Justification: LLMs are the core acting agents and evaluator in the studied protocols, and the
    paper describes their role, model family, feedback contract, and protocol usage throughout
    the main text and appendix (Secs. 3–5; App. B and App. I.5).
    Guidelines:
       • The answer [N/A] means that the core method development in this research does not
          involve LLMs as any important, original, or non-standard components.
       • Please refer to our LLM policy in the NeurIPS handbook for what should or should not
          be described.




                                             48
