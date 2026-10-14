                                            CM-DPO: Constraint-Margin Direct Preference
                                            Optimization for LLM Planning
                                            Rabimba Karanjai1 , Qun Gu1 , Hemanth Hegadehalli Madhavarao1 , Wenhuan Sun1 , Xiaojiao Yu1 ,
                                            Suryabhan Singh Hada1 , Libin N. George1 , Uma Kona1 , Richard Williamson1 , Linsey Pang1 , Prakhar
                                            Mehrotra1
                                            1
                                                PayPal AI Lab
                                            rkaranjai@paypal.com

                                            Direct Preference Optimization (DPO) treats all constraint violations equally: a $1 budget overshoot
                                            and a $1,000 overshoot induce the same training signal. It is also susceptible to length and style
                                            bias when preference pairs come from different model families. We introduce Constraint-Margin
arXiv:2610.09219v1 [cs.AI] 6 Oct 2026




                                            DPO (CM-DPO), which replaces DPO’s binary preference signal with a continuous margin derived
                                            from a deterministic symbolic verifier and scaled by violation severity. Hard and soft constraints are
                                            separated through a lexicographic objective, ensuring hard constraints are never traded off against
                                            preferences. To supply CM-DPO with bias-reduced training pairs, we generate preference data through
                                            procedurally generated constraint profiles (DCCG) and minimal-edit distillation from a reasoning
                                            teacher (RT-MED), within a framework we call SynPlan-R. On TravelPlanner, NaturalPlan, and
                                            out-of-distribution PlanBench, an 8B model fine-tuned with CM-DPO achieves 89.2% pass rate and
                                            93.4% solve rate, matching multi-agent systems at 13× lower latency while outperforming GPT-4o on
                                            unseen Blocksworld by 9.2 points.

                                            Date October 2026




                                        1   Introduction
                                        The deployment of Large Language Models (LLMs) is increasingly shifting from open-ended conversa-
                                        tional generation toward agentic workflows that require precise, long-horizon planning under complex con-
                                        straints Valmeekam et al. (2023); Xie et al. (2024). Real-world planning queries are rarely governed by a single
                                        homogeneous rule set; instead, they combine hard functional constraints, such as budget ceilings, temporal
                                        non-overlap, and capacity limits, that must be satisfied without exception, with soft user preferences, such
                                        as preferred carriers, dining cuisines, and proximity to landmarks, that should be optimized but may be
                                        relaxed. A user requesting “a weekend trip under $500 that avoids red-eye flights, preferably with boutique
                                        hotels” expects the budget ceiling and flight timing to be inviolable, while treating hotel style as a best-effort
                                        preference. Standard LLMs often conflate these two categories, producing plans that are semantically fluent
                                        but either violate hard constraints or unnecessarily sacrifice soft-constraint preferences Xie et al. (2024).
                                        We characterize this failure landscape as a Planning Trilemma among three constraints:

                                        • Accuracy: strict, verifiable satisfaction of all hard constraints and best-effort adherence to soft preferences.
                                        • Efficiency: sub-second, single-pass inference compatible with real-time deployment.
                                        • Controllability: responsiveness to dynamic, per-query constraint profiles without retraining.

                                        Existing methods typically satisfy at most two of these three criteria. We propose a unified data-synthesis
                                        and alignment framework with the following contributions:

                                        1. Dynamic Contextual Constraint Graphs (DCCG): A formal representation that decomposes planning problems
                                           into parameterized hard and soft constraint profiles over procedurally generated knowledge bases (synthetic
                                           flight and hotel databases with randomized prices and schedules). DCCG reduces the risk of domain
                                           memorization and encourages the model to learn transferable combinatorial reasoning (§3).



                                                                                                1
2. Reasoning-Trace Minimal-Edit Distillation (RT-MED): A teacher–student synthesis pipeline in which a reasoning
   model (DeepSeek-R1, o3-mini) corrects a flawed student draft through the minimum necessary semantic
   edits, isolating the logical “gradient” from stylistic noise and mitigating the length bias inherent in full-rewrite
   distillation (§4).
3. Constraint-Margin Preference Optimization (CM-DPO): An extension of DPO that injects a continuous
   penalty margin into the preference loss, scaled by the deterministic severity of hard-constraint violations
   computed by a symbolic verifier. Soft-constraint adherence is incorporated as a lexicographic secondary
   objective, ensuring that hard constraints are never traded off against preference satisfaction (§5).


2     Related Work

2.1   LLM Planning and Constraint Satisfaction
Open benchmarks have consistently documented the difficulty that LLMs face on constraint-heavy planning
tasks. TravelPlanner Xie et al. (2024) reports extremely low hard-constraint pass rates for open-source
models on multi-day itinerary construction, while NaturalPlan Zheng et al. (2024) shows similar weaknesses
in temporal scheduling. PlanBench Valmeekam et al. (2023) further shows that even frontier models struggle
with classical Blocksworld-style domains, suggesting that planning failures are not solely a matter of scale,
but also reflect limitations in representation and reasoning.
To address this gap, inference-time scaling methods interleave generation with environmental feedback.
ReAct Yao et al. (2023) augments generation with tool use, and Reflexion Shinn et al. (2023) adds self-critique,
while LRPlan Karthikeyan et al. (2025) extends this approach to a full Multi-Agent System (MAS) in which
a Large Reasoning Model (LRM) iteratively refines the output of a base LLM. Although effective, these
methods trade efficiency for accuracy: latencies of 20–30 s per query and multiplicative API costs limit their
suitability for real-time deployment. A parallel line of work combines LLMs with external symbolic solvers Liu
et al. (2023); Kambhampati et al. (2024), which can provide formal correctness guarantees but often require
domain-specific planner specifications, reducing generality. Constrained decoding methods Willard and Louf
(2023); Beurer-Kellner et al. (2023) enforce token-level grammatical constraints at generation time, but they
are less suited to semantic constraints whose validity depends on the global content of the plan (e.g., total
cost ≤ budget).

2.2   Preference Optimization and Its Limitations
Direct Preference Optimization (DPO) Rafailov et al. (2023) simplified RLHF by removing the need for an
explicit reward model and optimizing a closed-form objective over preference pairs. Subsequent work has
identified two limitations that are especially relevant to constraint-aware planning.
Standard DPO assigns the same implicit reward gap to all rejected samples, regardless of the severity of the
failure. Identity Preference Optimization (IPO) Azar et al. (2024) addresses overfitting through a regularized
objective, but it does not encode domain-specific violation semantics. Kahneman–Tversky Optimization
(KTO) Ethayarajh et al. (2024) replaces pairwise preferences with per-example utility, but it likewise does not
distinguish among different kinds of negative outcomes. SMAUG-DPO Pal et al. (2024) introduces a pairwise
margin, but the margin is derived from reward-model scores rather than deterministic constraint verification.
When chosen and rejected responses come from different model families, DPO can rely on superficial
distributional features rather than the underlying correction itself Park et al. (2024); Singhal et al. (2024).
This concern is closely related to the broader observation that DPO can be sensitive to response length and
may over-reward stylistic cues over substantive quality. Configurable Preference Tuning (CPT) Gallego (2025)
mitigates this issue only partially, since its rubrics are primarily stylistic rather than logical.
CM-DPO differs from these approaches in two respects: it derives its margin from a deterministic symbolic
verifier rather than a learned reward signal, and it uses a lexicographic objective that prioritizes hard-constraint
satisfaction over soft-preference adherence (§5).




                                                          2
2.3     Synthetic Data and Preference Alignment
Synthetic data has become an increasingly important tool for model alignment. Self-Instruct Wang et al.
(2023) showed that models can generate useful instruction-tuning data for themselves, and DPO Rafailov et al.
(2023) removed the need for explicit reward models by optimizing directly over preference pairs. Configurable
Preference Tuning (CPT) Gallego (2025) extended this setup by conditioning DPO on varying “rubrics.”
However, standard DPO can become brittle when negative samples are distinguishable through superficial
stylistic traits rather than substantive errors. SynPlan-R addresses this issue by generating counterfactual
minimal edits and by modifying the DPO objective to account for continuous constraint-violation margins.

2.4      Knowledge Distillation for Reasoning
Distilling reasoning ability from larger teacher models into smaller ones has received renewed attention
following the success of chain-of-thought prompting Wei et al. (2022). Distilling Step-by-Step Hsieh et al.
(2023) uses rationales as intermediate supervision, and more recent work has explored distilling extended
reasoning traces from open reasoning models such as DeepSeek-R1 DeepSeek-AI (2025); Yu et al. (2024). Most
of the literature focuses on broad reasoning domains such as mathematics and code generation. SynPlan-R
instead targets constraint-satisfaction reasoning and introduces RT-MED to reduce the tendency of the student
to imitate the teacher’s verbose reasoning style rather than internalize the underlying logical correction.


3      Dynamic Contextual Constraint Graphs
We represent each planning instance as a constraint profile that separates hard constraints, soft preferences,
and the local knowledge base used for verification. This formulation makes the distinction between feasibility
and preference explicit and provides a common interface across domains.
Definition 1 (Constraint Profile). A profile p ∈ Ω is a tuple ⟨Chard , Csof t , Klocal ⟩, where:
      • Chard = {c1 , . . . , cm } is the set of hard constraints, evaluated by a Boolean verifier Vhard : Y × Chard ×
        Klocal → {0, 1}m .
      • Csof t = {cm+1 , . . . , cn } is the set of soft preferences, scored by Ssof t : Y × Csof t × Klocal → [0, 1]n−m .
      • Klocal is a procedurally generated local knowledge base provided in context, requiring the model to
        reason over instance-specific facts rather than rely on memorized domain knowledge.
Candidate plans are ranked first by hard-constraint satisfaction  and only then, among plans with equal
hard-constraint status, by soft-preference score. Let H(y) = j Vhard,j (y). We write y ≻ y ′ iff H(y) > H(y ′ ),
                                                            P

or H(y) = H(y ′ ) and S̄(y) > S̄(y ′ ).

3.1     Domain Generalization
We compare the framework in two domains, travel planning and retail recommendation, each with its own
constraint profile and verifier.

Travel:     We can formalize a travel planning as

                                             ptravel = ⟨β, τ, η , |{z}
                                                                   Λ , Klocal ⟩,
                                                        | {z }
                                                           Chard Csof t

where β is the budget, τ the temporal window, η the minimum pace requirement, and Λ the set of preferred
attributes. Hard constraints are verified by

                                             Vcost (y) = 1Pi∈I Price(i,K)≤β ,                                          (1)
                                                                    y


and
                                                        1tarr (vi+1 )−tdep (vi )≥d(vi ,vi+1 ) .
                                                    ^
                                      Vtime (y) =                                                                      (2)
                                                    i




                                                                3
Soft-preference satisfaction is defined as
                                                   |{v ∈ Iy : Attrs(v) ∩ Λ ̸= ∅}|
                                  Sattr (y, Λ) =                                  .
                                                                |Iy |
For cost violations, we define the continuous severity as
                                                                                !+
                                                       X
                                     ∆Vcost (y) =            Price(i, K) − β            ,                    (3)
                                                         i

where (·)+ = max(0, ·).

Retail:   We formalize a retail product search as
                                   pretail = ⟨κ, Freq , Gcompat , Rpref , Klocal ⟩,
                                              |      {z       } | {z }
                                                      Chard           Csof t

where κ is the budget, Freq the set of required features, Gcompat a compatibility graph, and Rpref the preferred
brands or retailers.
A deterministic function T : Ω → Σ∗ maps each constraint profile to a natural-language system prompt s,
which is then used to condition generation. This projection allows the same underlying profile representation
to be expressed as a natural-language planning prompt without changing the verifier-defined semantics.


4    The SynPlan-R Synthesis Pipeline
The pipeline constructs a set of verified preference pairs,
                                      D = {(si , xi , yw,i , yl,i , ∆Vi , S̄i )}N
                                                                                i=1 ,

in four phases (Figure 1).

Phase 1: Inverse Constraint Querying.        An auxiliary policy πaux generates implicit user queries,
                                         x ∼ πaux (x | Promptinv ⊕ p),
yielding requests such as “affordable weekend getaway” for a $600 budget profile. This setup requires the
downstream model to infer the relevant constraints from s rather than relying on an explicitly stated rule list.

Phase 2: Baseline Draft (yl ).   A student policy πbase (GPT-4o-mini) generates an initial draft,
                                                yl ∼ πbase (y | s, x).

Hypothesis 1 (Heuristic Failure). Standard policies often approximate hard constraints using surface-level
heuristics, which lead to near-miss violations (Cost(yl ) ≈ β but Cost(yl ) > β). These near-misses provide
especially informative negative samples.

Phase 3: RT-MED. To reduce the extent to which DPO can exploit stylistic differences between teacher and
student outputs, we use Reasoning-Trace Minimal-Edit Distillation (RT-MED). The teacher model πref (o3-mini)
receives yl , s, and Klocal , and produces
                                 yw = <think> ⊕ ctrace ⊕ </think> ⊕ Edit(yl ),                               (4)
where Edit(yl ) is heuristically guided by a system prompt instructing the teacher to isolate and resolve the
violation. Rather than performing a formal combinatorial search or strict mathematical optimization over
semantic distance, the teacher is prompted to greedily swap only the specific entities responsible for the
violation while leaving the surrounding valid sub-plans and formatting untouched. In practice, the teacher
typically changes only the entities responsible for the violation (∼ 32 tokens versus ∼ 245 for full rewrites),
which helps separate constraint-relevant corrections from stylistic variation (Table 4, Figure 2).


                                                             4
                                  π_aux                      π_base                     RT-MED



                   Constraint               Inverse                      Initial                 Minimal
                     Profile                 Query       x               Draft     yl             Edit yw




                                                                                                 Verifier




                         Preference pair                 Violation                      Soft score
                                 yw ≻ y l             severity ΔV                            S




                                                   Student Model
                                                SynPlan-8B · SFT + CM-DPO




Figure 1 The SynPlan-R architecture. Phase 1: DCCG decomposes each profile into hard constraints Chard (red), soft
preferences Csof t (blue), and a procedural knowledge


Phase 4: Verification and Severity. A symbolic verifier V evaluates each plan against Klocal . A pair is
included only if Vhard (yw ) = 1 and there exists at least one constraint j such that Vhard,j (yl ) = 0. The verifier
then records the continuous violation severity ∆V(yl ) and the soft-preference score S̄sof t (yw ), as defined in
Eq. 3.


Algorithm 1 SynPlan-R Synthesis with RT-                       Algorithm 2 CM-DPO Alignment (Stage 2)
MED                                                            Input: SFT-init, frozen, dataset (πθ , πref , D)
Input: Ω, πbase , πref , πaux                                   1: while not converged do
Output: D                                                          2:   Sample (s, x, yw , yl , ∆Ṽ, S) ∼ D
 1: D ← ∅                                                          3:   mc ← tanh(λ   · ∆Ṽ)
 2: for p ∼ Ω do
                                                                                h                                      i
                                                                   4:   ∆θ ← βd log ππref
                                                                                       θ (yw |x)         πθ (yl |x)
                                                                                          (yw |x) − log πref (yl |x)
 3:   s, K ← T (p); x ← πaux (· | p)
 4:   yl ← πbase (y | s, x)                                        5:   Lhard ← − log σ(∆θ − γ · mc )
 5:   yw ← πref (RT-MED | s, x, yl , K)                            6:   Lsof t ← − log σ(∆θ ) · (S(yw ) − S(yl ))+
 6:   Compute Vhard , ∆V, S̄                                       7:   LCM ← Lhard + α · 1Vhard (yw )=1 · Lsof t
 7:   if Vhard (yw ) = 1 ∧ ∃j : Vhard,j (yl ) = 0 then             8:   Update θ via ∇θ LCM
 8:      D ← D ∪ {(s, x, yw , yl , ∆V, S̄)}                        9: end while
 9:   end if
10: end for



5     Constraint-Margin Preference Optimization
We begin with standard DPO and then extend it in two steps. First, we replace the binary preference signal
with a continuous margin derived from the severity of hard-constraint violations. Second, we add a separate


                                                               5
                                                                                                                        ′
         Student Draft yl (πbase )                       RT-MED Edit yw (πref )                           Full Rewrite yw
          Day 1: Fly SFO → NYC                           Day 1: Fly SFO → NYC                     Day 1: Fly JFK via Spirit
                      United #482, dep 8:00am                United #482, dep 8:00am                   // different airline, route
                      K: $180                                K: $180
          Hotel: The Standard NYC                        Hotel: Hampton Inn Midtown               Hotel: Pod 51 NYC
                      $195/night × 2 = $390                   $120/night × 2 = $240                    // different hotel, structure   Figure 2 RT-MED qualitative example The hard
          Day 2: Central Park, MoMA                      Day 2: Central Park, MoMA                Day 2: High Line, Chelsea
                      Park: free    MoMA: $30                Park: free   MoMA: $30                    // different activities         constraint is total cost ≤ 600, and the soft con-
          Dinner: Le Bernardin                           Dinner: Le Bernardin                     Dinner: Joe’s Pizza
                      $85 per person                         $85 per person                            // different restaurant
                                                                                                                                       straint is a preference for boutique hotels. Left:
          Day 3: Brooklyn Bridge, fly back               Day 3: Brooklyn Bridge, fly back         Day 3: DUMBO, return
                      Return flight: $165                    Return flight: $165                       // different itinerary
                                                                                                                                       the student draft violates the budget constraint
          Total: $650                ✗ OVER BUDGET Total: $550                     ✓ UNDER        Total: $420              ✓
                                                                                                                                       (hotel at $195/night, yielding a total cost of
          ∆Vcost = $650 − $600 = $50                     Slack: $600 − $550 = $50                 Problem: DPO sees ∼245               $650). Center: RT-MED swaps only the hotel
                                                                                                  token delta. Student learns
          Soft: “The Standard” = boutique ✓              Soft: Hampton Inn ̸= boutique            to mimic teacher’s vocab-
                                                                                                  ulary and style, not the
                                                                                                                                       (∼ 12 tokens). Right: a full rewrite changes
        Vhard (yl ) = 0             REJECTED            Vhard (yw ) = 1   ACCEPTED
                                                                                                  constraint logic.
                                                                                                     Style bias → 65% PR
                                                                                                                                       ∼ 245 tokens and introduces style bias. Bottom:
                                                                                                                                       token-count and PR comparison.
                     yw        32                                                                       65.2%
                      ′
                     yw                                       245                                                89.2%

                          0    50      100     150 200     250             0%      20%      40%   60%      80% 100%
                                             Tokens                                               PR



                     700
                                        Budget Exceeded
                                        DPO Penalty
                     600
                                        CM-DPO Penalty (γmc )
                                                                                         $500
                     500
 Budget Exceed ($)




                                                                                                                                       Figure 3 CM-DPO vs. Standard DPO. Standard
                                                   same                                            same         $400
                     400                                                                                                               DPO assigns the same penalty regardless of vio-
                                                                                                                                       lation severity. CM-DPO scales the margin γmc
                     300                                                                                                               proportionally to the budget overshoot, produc-
                                                                                                                                       ing stronger repulsion for larger violations.
                     200
                                            $100
                     100                                         $80


                          0
                                                     (1)                                                (2)
                                                   yl                                                yl



soft-constraint objective that is activated only when hard constraints are satisfied.

5.1                       Hard-Constraint Margin
Standard DPO treats all rejected responses equally, regardless of the severity of the violation. In constraint-
aware planning, however, a small budget overshoot and a catastrophic failure should not induce the same
update. To encode this distinction, we define a continuous margin

                                                                                             mc = tanh(λ · ∆V(yl )) ∈ [0, 1],

where ∆V(yl ) is the verifier-computed severity of the rejected plan and λ > 0 controls sensitivity. The tanh
transformation keeps the margin bounded while remaining approximately linear near the origin.
We then modify the hard-constraint objective as

                                                                                            Lhard = −E [log σ (∆θ − γ · mc )] ,                                                      (5)

where γ controls how strongly violation severity shifts the decision boundary. Larger violations therefore
induce a larger effective margin and a stronger corrective update.
Remark 5.1 (Gradient amplification). Let z = ∆θ − γmc . The gradient term includes σ(−z), so increasing mc
pushes z downward and increases the update magnitude. Intuitively, the model is pushed more strongly away
from catastrophic violations while still receiving smoother corrective feedback near the feasibility boundary.




                                                                                                                           6
5.2   Soft-Constraint Objective
Hard feasibility alone is not sufficient. Among feasible plans, the model should also prefer those that better
satisfy soft constraints. We therefore introduce a secondary objective
                                                                            +
                                    Lsoft = − log σ(∆θ ) · S̄(yw ) − S̄(yl ) .                                 (6)

This term is active only when the chosen response improves soft-preference satisfaction. If the chosen plan
gives up a soft preference in order to restore hard feasibility, the soft term contributes zero rather than
penalizing that correction.

5.3   Combined Objective
We combine the two terms as

                                LCM = Lhard (mc ) + α · 1[Vhard (yw ) = 1] · Lsoft ,                           (7)

where α ≥ 0 controls the weight of the soft-constraint objective. The indicator gate ensures that soft-preference
optimization is applied only when the chosen plan is hard-feasible. In this sense, the objective is lexicographic:
hard constraints take priority, and soft preferences are optimized only within the feasible region (Figure 3).
CM-DPO differs from prior variants such as SMAUG-DPO (Pal et al., 2024) and IPO (Azar et al., 2024) in
two ways. First, its margin is derived from a deterministic symbolic verifier rather than a learned reward
signal. Second, it explicitly separates hard-constraint satisfaction from soft-preference optimization.

5.4   Training Procedure
Training proceeds in two stages.

Stage 1: Supervised Fine-Tuning (SFT). We first warm-start the model on gold trajectories that include
reasoning traces. This stage teaches the model the overall structure of constraint-aware planning and provides
a stable initialization before preference optimization.

Stage 2: Constraint-Margin DPO (CM-DPO). Starting from the SFT checkpoint, we optimize the model
with LCM on verified preference pairs. During this stage, the reasoning traces are removed and the objective
is applied only to the final plans. This keeps the preference signal focused on plan correctness and constraint
satisfaction rather than on reproducing the teacher’s reasoning style.

       Param              Sym           Val
                                                                                          Travel   Retail
       DPO temp            βd          0.1
       Sensitivity         λ          0.01                            Raw generations     14,200   11,800
       Margin str.         γ           1.5                            Verified pairs       8,400    6,600
       Soft weight         α           0.3                            Acceptance rate     59.2%    55.9%
       LR (SFT/DPO)       N/A    2×10−5 /5×10−7                       Avg. token ∆          34       29
       Batch/Epochs       N/A       32 / 3+1                          Avg. ∆V(yl )          $87     $142

Table 1 CM-DPO hyperparameters.                           Table 2 Synthesis statistics.




6     Experimental Setup

6.1   Training Data
We synthesize 15,000 verified preference pairs across two domains: travel and retail. For data generation, the
baseline policy πbase is GPT-4o-mini and the teacher policy πref is o3-mini. We first sample raw candidate
generations, then retain only those pairs that pass symbolic verification and exhibit at least one hard-constraint


                                                         7
                                                              TravelPlanner     NaturalPlan    Eff.
                   Method
                                                         PR↑      DR↑     S̄↑      SR↑        Lat.↓
                   External baselines
                     Zero-Shot (Llama-3-8B)               1.3     35.4    —        18.5        2.1s
                     Zero-Shot (GPT-4o)                  39.8     88.3   0.61      68.4        5.4s
                     MAS (LRPlan w/ GPT-4o)              89.4     98.1   0.72      95.1       28.5s
                   SynPlan-R ablations (Llama-3-8B)
                     L3-SFT                              35.6     76.2   0.48      52.8        2.1s
                     Full Rewrite + DPO                  64.1     88.5   0.53      71.3        2.2s
                     RT-MED + DPO                        78.3     92.1   0.57      82.7        2.1s
                     Full Rewrite + CM-DPO               72.6     90.8   0.55      76.9        2.2s
                     SynPlan-8B                          89.2     95.4   0.64      93.4        2.1s

Table 3 Main results. SynPlan-8B reaches a TravelPlanner pass rate close to MAS performance (89.2% vs. 89.4%) while
reducing latency from 28.5s to 2.1s. The soft-preference score S̄ is computed only over feasible plans.


violation in the rejected response. Table 2 summarizes the resulting data distribution and edit characteristics.
Acceptance rate is the fraction of raw generations that yield verified preference pairs. Avg. token ∆ denotes
the average edit distance between rejected and chosen plans, and Avg. ∆V(yl ) denotes the mean violation
severity of the rejected plan.

6.2    Benchmarks and Metrics
We evaluate all models in the zero-shot setting on three benchmarks. TravelPlanner (Xie et al., 2024) contains
180 travel planning queries. NaturalPlan (Zheng et al., 2024) contains 200 meeting-scheduling instances.
PlanBench (Valmeekam et al., 2023) contains 150 out-of-distribution Blocksworld problems and is used to
measure transfer beyond the domains seen during synthesis. We report PR (Pass Rate: fraction satisfying all
hard constraints), DR (Decode Rate: fraction parsable), SR (Schedule Rate: exact-match valid schedule), and
S̄ (soft-preference score, conditioned on feasibility).

6.3    Baselines
Our base model is Llama-3-8B-Instruct. We compare against zero-shot prompting with Llama-3-8B and
GPT-4o, an inference-time multi-agent baseline based on LRPlan, and several training ablations: L3-SFT,
Full Rewrite + DPO, RT-MED + DPO, Full Rewrite + CM-DPO, and SynPlan-8B, which uses the full
pipeline. To avoid confounding distribution shifts, all ablation models predict the final plan directly without
reasoning traces at inference time, matching the SynPlan-8B setup.

6.4    Compute
All experiments are run on four NVIDIA A100 GPUs (80GB each) using DeepSpeed ZeRO Stage 3 for
distributed training. Supervised fine-tuning takes approximately 4 hours, and CM-DPO training takes
approximately 2.5 hours. Data synthesis incurs approximately $320 in API cost. Unless otherwise stated,
decoding uses greedy inference with T = 0.


7     Results and Analysis

7.1   End-to-End Constraint Satisfaction
Table 3 shows that SynPlan-8B substantially improves over zero-shot prompting and over all single-model
ablations. On TravelPlanner, it achieves an 89.2% pass rate, which is close to the 89.4% achieved by MAS,
while reducing latency from 28.5s to 2.1s. On NaturalPlan, SynPlan-8B reaches a 93.4% schedule rate in a
single forward pass, offering a substantially improved efficiency–accuracy tradeoff over MAS. Among feasible



                                                          8
                                                    Standard DPO         CM-DPO
                                                    PR       Tok∆       PR     Tok∆
                                     Full Rewrite   64.1        245    72.6     245
                                     RT-MED         78.3        32     89.2     32

Table 4 2 × 2 ablation on TravelPlanner pass rate (%).


      Method                    Acc (%)      Lat.

      Zero-Shot (Llama-3-8B)         12.8    2.1s
                                                                              γ = 0.5   γ = 1.5   γ = 3.0
      Zero-Shot (GPT-4o)             58.2    5.1s
      L3-SFT                         28.4    2.1s                λ = 0.005     81.4      84.7      83.1
      Full Rewrite + DPO             31.5    2.2s                λ = 0.01      84.9      89.2      87.8
      SynPlan-8B                     67.4    2.1s                λ = 0.02      83.6      87.1      82.3

Table 5       Zero-shot   transfer     to   PlanBench      Table 6 Sensitivity to λ and γ on TravelPlanner pass
(Blocksworld).                                             rate (%).


plans, SynPlan-8B attains a soft-preference score of 0.64, compared with 0.72 for MAS, indicating that
CM-DPO improves soft-preference optimization without sacrificing hard-constraint satisfaction.

7.2   Component Ablation
Table 4 isolates the effects of RT-MED and CM-DPO. Replacing full rewrites with RT-MED improves pass
rate by 14.2 points under standard DPO and by 16.6 points under CM-DPO. Replacing standard DPO with
CM-DPO improves pass rate by 8.5 points for full rewrites and by 10.9 points when RT-MED is used. The
combined improvement from Full Rewrite + DPO to RT-MED + CM-DPO is 25.1 points, which is larger
than the sum of the two smaller reference gains (22.7 points). This pattern suggests a positive interaction
between minimal-edit distillation and severity-aware preference optimization.

7.3   Zero-Shot Generalization (PlanBench)
Table 5 evaluates zero-shot transfer to an unseen planning domain. SynPlan-8B achieves 67.4% accuracy
on Blocksworld, exceeding GPT-4o by 9.2 percentage points while maintaining low latency. This result is
consistent with the claim that the training pipeline improves transfer beyond the travel and retail domains
used during synthesis.
We hypothesize that severity-aware minimal-edit training teaches the model to localize constraint-critical
state updates rather than rely on surface-level heuristics, neutralizing the length bias that hinders standard
DPO in logical tracking domains.

7.4   Hyperparameter Sensitivity
Table 6 shows that performance is relatively stable across the tested settings and that all CM-DPO configura-
tions outperform the standard DPO baseline of 64.1%. The best result is obtained at λ = 0.01 and γ = 1.5.
Larger margins reduce performance slightly, which is consistent with the possibility that excessive saturation
in the tanh transformation weakens gradient variation.

7.5   Error Analysis
On TravelPlanner, SynPlan-8B fails on 10.8% of instances (N = 19). Among these failures, 36.8% are caused
by budget violations, 26.3% by temporal conflicts, 21.1% by spatial unreachability, and 15.8% by parse failures.
We do not observe errors in which a soft preference is incorrectly prioritized over a hard constraint, which is
consistent with the intended behavior of the lexicographic objective.



                                                            9
8    Limitations
The method depends on a symbolic verifier, so extending it to open-world environments where constraints
cannot be checked deterministically remains an open problem. Budget violations account for the largest
share of TravelPlanner errors (36.8%), suggesting that implicit arithmetic remains a bottleneck for longer
plans. Preliminary experiments with Qwen3-8B in thinking mode suggest that reasoning-enabled base models
further reduce budget violations under SynPlan-R; however, we exclude these results to avoid confounding
comparisons between thinking and non-thinking inference regimes. Teacher-guided data synthesis incurs
nontrivial cost (approximately $320 for 15K pairs), so larger-scale deployment may require more efficient
self-play strategies. Finally, we have not tested whether the same gains transfer to substantially smaller or
larger model scales.


9    Conclusion
We introduced Constraint-Margin DPO (CM-DPO), a preference-optimization objective that replaces DPO’s
binary signal with a continuous, verifier-derived margin scaled by hard-constraint violation severity, together
with a lexicographic secondary objective for soft preferences. To supply CM-DPO with bias-reduced training
pairs, we developed DCCG for procedural constraint-profile generation and RT-MED for minimal-edit
distillation from a reasoning teacher. Experiments on TravelPlanner, NaturalPlan, and out-of-distribution
PlanBench show that the resulting 8B model approaches multi-agent accuracy at a fraction of the latency,
and that severity-aware preference optimization transfers to unseen planning domains.


References
Mohammad Gheshlaghi Azar, Zhaohan Daniel Guo, Bilal Piot, Rémi Munos, Mark Rowland, Michal Valko, and Daniele
 Calandriello. A general theoretical paradigm to understand learning from human preferences. In International
 Conference on Artificial Intelligence and Statistics (AISTATS), volume 238 of Proceedings of Machine Learning
 Research. PMLR, 2024. URL https://proceedings.mlr.press/v238/gheshlaghi-azar24a.html.
Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. Prompting is programming: A query language for large
  language models. Proceedings of the ACM on Programming Languages, 7(PLDI):1946–1969, 2023.
DeepSeek-AI. DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning. arXiv preprint
  arXiv:2501.12948, 2025. URL https://arxiv.org/abs/2501.12948.
Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, and Douwe Kiela. KTO: Model alignment as
  prospect theoretic optimization. In Proceedings of the 41st International Conference on Machine Learning (ICML),
  volume 235 of Proceedings of Machine Learning Research. PMLR, 2024. URL https://proceedings.mlr.press/
  v235/ethayarajh24a.html.
Víctor Gallego. Configurable preference tuning with rubric-guided synthetic data. arXiv preprint arXiv:2506.11702,
  2025. URL https://arxiv.org/abs/2506.11702.
Cheng-Yu Hsieh, Chun-Liang Li, Chih-Kuan Yeh, Hootan Nakhost, Yasuhisa Fujii, Alexander Ratner, Ranjay Krishna,
  Chen-Yu Lee, and Tomas Pfister. Distilling step-by-step! outperforming larger language models with less training
  data and smaller model sizes. In Findings of the Association for Computational Linguistics (ACL), 2023. URL
  https://aclanthology.org/2023.findings-acl.507/.
Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant Bhambri, Lucas Paul
  Saldyt, and Anil B. Murthy. Position: LLMs can’t plan, but can help planning in LLM-Modulo frameworks. In
  Proceedings of the 41st International Conference on Machine Learning (ICML), volume 235 of Proceedings of Machine
  Learning Research. PMLR, 2024. URL https://openreview.net/forum?id=Th8JPEmH4z.
T Karthikeyan, Om Dehlan, Mausam, and Manish Gupta. LRPlan: A multi-agent collaboration of large language
  and reasoning models for planning with implicit and explicit constraints. In Findings of the Association for
  Computational Linguistics: EMNLP, pages 8280–8310. Association for Computational Linguistics, 2025. URL
  https://aclanthology.org/2025.findings-emnlp.440/.




                                                        10
Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Peter Stone. LLM+P:
  Empowering large language models with optimal planning proficiency. arXiv preprint arXiv:2304.11477, 2023. URL
  https://arxiv.org/abs/2304.11477.
Arka Pal, Deep Karkhanis, Samuel Dooley, Manley Roberts, Siddartha Naidu, and Colin White. Smaug: Fixing
  failure modes of preference optimisation with DPO-positive. arXiv preprint arXiv:2402.13228, 2024. URL https:
  //arxiv.org/abs/2402.13228.
Ryan Park, Rafael Rafailov, Stefano Ermon, and Chelsea Finn. Disentangling length from quality in direct
  preference optimization. In Findings of the Association for Computational Linguistics (ACL), 2024. URL
  https://aclanthology.org/2024.findings-acl.297/.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, and Chelsea Finn. Direct
  preference optimization: Your language model is secretly a reward model. In Advances in Neural Information
  Processing Systems (NeurIPS), volume 36, 2023. URL https://papers.nips.cc/paper_files/paper/2023/hash/
  a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html.
Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Lan-
  guage agents with verbal reinforcement learning. In Advances in Neural Information Processing Sys-
 tems (NeurIPS), volume 36, 2023. URL https://proceedings.neurips.cc/paper_files/paper/2023/hash/
  1b44b878bb782e6954cd888628510e90-Abstract-Conference.html.
Prasann Singhal, Tanya Goyal, Jiacheng Xu, and Greg Durrett. A long way to go: Investigating length correlations in
  RLHF. arXiv preprint arXiv:2310.03716, 2024. URL https://arxiv.org/abs/2310.03716.
Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. Plan-
  Bench: An extensible benchmark for evaluating large language models on planning and reasoning about
  change. In Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track,
  volume 36, pages 38975–38987, 2023. URL https://proceedings.neurips.cc/paper_files/paper/2023/hash/
  7a92bcdede88c7afd108072faf5485c8-Abstract-Datasets_and_Benchmarks.html.
Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh Hajishirzi.
  Self-instruct: Aligning language models with self-generated instructions. In Proceedings of the 61st Annual Meeting of
  the Association for Computational Linguistics (ACL), 2023. URL https://aclanthology.org/2023.acl-long.754/.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny
  Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Advances in Neural Information
  Processing Systems (NeurIPS), volume 35, 2022. URL https://proceedings.neurips.cc/paper_files/paper/
  2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html.
Brandon T. Willard and Rémi Louf. Efficient guided generation for large language models.                arXiv preprint
  arXiv:2307.09702, 2023. URL https://arxiv.org/abs/2307.09702.
Jian Xie, Kai Zhang, Jiangjie Chen, Tinghui Zhu, Renze Lou, Yuandong Tian, Yanghua Xiao, and Yu Su. TravelPlanner:
   A benchmark for real-world planning with language agents. In Proceedings of the 41st International Conference on
   Machine Learning (ICML), volume 235 of Proceedings of Machine Learning Research, pages 54590–54613. PMLR,
   2024. URL https://proceedings.mlr.press/v235/xie24j.html.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. ReAct: Synergizing
  reasoning and acting in language models. In International Conference on Learning Representations (ICLR), 2023.
  URL https://openreview.net/forum?id=WE_vluYUL-X.
Ping Yu, Jing Xu, Jason Weston, and Ilia Kulikov. Distilling system 2 into system 1. arXiv preprint arXiv:2407.06023,
  2024. URL https://arxiv.org/abs/2407.06023.
Huaixiu Steven Zheng, Swaroop Mishra, Hugh Zhang, Xinyun Chen, Minmin Chen, Azade Nova, Le Hou, Heng-Tze
  Cheng, Quoc V. Le, Ed H. Chi, and Denny Zhou. NATURAL PLAN: Benchmarking LLMs on natural language
  planning. arXiv preprint arXiv:2406.04520, 2024. URL https://arxiv.org/abs/2406.04520.




                                                          11
10     DCPG: Constraint-Profile Graph Statistics
For each domain we report the average graph density of the instantiated constraint-profile graphs across the
15,000 synthesized instances. “|VC |” is the total number of constraint nodes; “|VE |” is the average number of
grounded knowledge-base entities; densities are reported per-edge-type.

Table 7 Constraint-profile graph statistics (averaged across instances).


                                  Domain     |VChard |   |VCsoft |   |VE |   avg. |Egrounds |
                                  Travel       3.4         1.8       41.2         14.7
                                  Retail       3.2         2.0       28.4         11.9


The retail domain additionally exposes a non-trivial Econflicts structure: average pairwise compatibility-graph
density is 0.31, with conflicts concentrated across categories (printer/cartridge, headset/console, etc.).


11     Knowledge-Base Generation
Travel. Each Klocal is regenerated per instance from log-normal distributions calibrated to public market
data: flight prices (µ = $180, σ = 0.5), hotel rates (µ = $130, σ = 0.6), and activity prices (µ = $40, σ = 0.8).
City-pair travel times come from a deterministic distance matrix over 48 candidate cities.

Retail. Product prices are sampled per-category; compatibility edges within a category occur with p = 0.7,
across categories with p = 0.95.


12     Symbolic Verifier

12.1   Schema-Required Extraction
All models—teacher, student, and the trainable policy at evaluation time—are required to emit a <plan>...</plan>
block whose contents must validate against the following JSON schema. Synthesis time: outputs from πT or
πbase that fail schema validation are excluded from D. Evaluation time: outputs from πθ that fail schema
validation are counted as failures in the PR/SR denominator (equivalently, treated as plans that violate at
least one hard constraint by failing to be evaluable); we additionally report the schema-failure rate separately
as the parse-failure rate so it can be distinguished from semantic constraint violations. No LLM-assisted
re-parsing is used at any point in the pipeline.

plan := { items: [item, ...],
          total_stated_cost: number,
          destinations_visited: [string, ...] }

item := { name: string,
          type: "flight" | "hotel" | "restaurant" | "activity",
          day: int,
          start_time?: "HH:MM",
          end_time?: "HH:MM",
          stated_price: number,
          db_lookup_key: string }
Outputs that fail schema validation are rejected at synthesis time (no LLM-assisted re-parsing), preserving
full determinism of all downstream constraint evaluation. The travel-domain temporal verifier distinguishes
event times (start/end) from transit times (arrival/departure), which avoids the off-by-one error that mixes
hotel check-in with previous-flight arrival in flatter parsers.




                                                              12
12.2    Travel-Domain Pseudocode (correct gap definition)
def verify_travel(plan, profile, K):
    # Cost via ground-truth lookup, NOT stated price
    true_cost = sum(K.lookup(i.db_key).price * i.nights_or_one()
                    for i in plan.items)
    cost_severity = max(0.0, true_cost - profile.beta)

     # Temporal feasibility: gap = next.start - curr.end
     time_severity = 0.0
     for c, n in zip(plan.items[:-1], plan.items[1:]):
         gap = n.start_time - c.end_time   # start - end (not arr - dep)
         travel = K.travel_time(c.location, n.location)
         time_severity += max(0.0, travel - gap)

     # Pace
     pace_deficit = max(0, profile.eta - len({i.location for i in plan.items}))

     # Per-constraint normalised severity
     delta = {
         "cost": min(1.0, cost_severity / TAU["cost"]),
         "time": min(1.0, time_severity / TAU["time"]),
         "pace": min(1.0, pace_deficit / TAU["pace"]),
     }
     return delta

12.3    Cross-Unit Normalization Constants τj
We set τj to the median raw severity of violating generations per constraint, computed once on a 1,000-instance
held-out slice of the synthesis stream and frozen thereafter:

Table 8 Severity normalization constants τj (frozen).


                                   Constraint                 τj        Unit
                                   Travel: cost overflow      84         USD
                                   Travel: time violation      38      minutes
                                   Travel: pace deficit         1       cities
                                   Retail: budget overflow    138        USD
                                   Retail: feature missing      1   feature count
                                   Retail: compat violation    1      edge count


The default constraint weights are uniform (wj = 1/|VChard |); ablations with severity-frequency-weighted wj
are reported in App. 22 and produce within-noise differences.

12.4    Verifier Reliability Audit
To validate the verifier we manually re-graded 300 randomly sampled (yw , yl ) pairs against ground-truth
constraint satisfaction (two annotators, full agreement on 293/300; disagreements adjudicated by a third
annotator). Because all verifier inputs are schema-validated JSON, the constraint evaluation is bit-deterministic:
the audit therefore measures the combined effect of (i) the symbolic evaluator’s correctness and (ii) any residual
schema ambiguity (for example, a model emits a syntactically valid JSON whose semantic interpretation
under our schema is unintended).
We classify CM-DPO’s verifier as “schema-required symbolic”: any input that is not a valid schema JSON is
rejected as a decode failure rather than re-parsed by an LLM. This is materially different from end-to-end
LLM judging and from prompt-and-pray extraction.


                                                        13
Table 9 Verifier audit on 300 manually labelled pairs.


          Metric                                                                     Value
          Hard-pass/fail agreement with manual labels                           98.7% (296/300)
          Wilson 95% CI                                                          [96.7%, 99.6%]
          False-pass rate                                                         0.3% (1/300)
          False-fail rate                                              1.0% (3/300, all schema-ambiguity)
          Schema-failure (decode failure) rate over synthesis stream                  1.7%



13     Prompts

13.1   System Prompt Projection
Hard constraints are stated as absolute requirements; soft constraints as preferences. Both domain templates
emit a system prompt that repeats the ground-truth knowledge base and forbids hallucinated prices.
You are a travel planning assistant.

=== HARD CONSTRAINTS (must be satisfied) ===
- Total budget MUST NOT exceed ${beta}
- Travel dates: {t_start} to {t_end}
- Visit at least {eta} distinct cities/attractions
- All transit gaps (next.start - current.end) must
  be at least the travel duration from the database

=== SOFT PREFERENCES (best-effort) ===
- Preferred attributes: {Lambda}
- Honour these when possible, NEVER violate hard constraints

=== GROUND TRUTH DATABASE ===
{K_local_json}

Output a single <plan>{...JSON...}</plan> block.

13.2    Inverse Constraint Querying (πaux )
The inverse query explicitly forbids restating numeric constraints, forcing the downstream model to infer
them.
You are generating a realistic user query. The user has constraints
{p_summary}, but you MUST NOT state numbers explicitly. Generate a
1-3 sentence query that implies them naturally. Output only the query.

13.3    RT-MED Refinement
You are a constraint correction expert. Output:
  <rationale>...your written explanation of which constraint is
  violated and which SPECIFIC items in the draft cause the
  violation...</rationale>
  followed by a CORRECTED <plan>...</plan> JSON block.

CRITICAL: change ONLY entities responsible for the violation. Keep
all other text identical. Do NOT rewrite the plan from scratch.
We refer to the <rationale> block as a teacher-generated correction rationale: it is text we elicit from πT via
the prompt above. It is not the teacher’s internal chain-of-thought (to which we have no access for closed-API


                                                         14
teachers).


14      Baseline Configurations
All training-time baselines use the same 15,000-pair dataset D, the same Llama-3-8B-Instruct base, the same
SFT warm-start, and identical decoding (greedy, T = 0). Method-specific hyperparameters were grid-searched
on a held-out 10% split:

     • DPO: βd =0.1.
     • IPO: τ =0.1 (best of {0.05, 0.1, 0.5}).
     • KTO: λD =1.0, λU =1.0, reference-point βKTO =0.1.
     • SimPO: β=2.0, γ=1.4 (best of grid β ∈ {1, 2, 2.5}, γ ∈ {0.5, 1.0, 1.4}).
     • DPOP: βd =0.1, λ=50.
     • MMPO: granular margins from a learned 3-class quality classifier trained on a held-out 1,000-pair labelling
       slice.
     • α-DPO: α=0.5.
     • C-DPO: dual ascent with ηdual =10−3 ; cost model is a frozen verifier-derived continuous reward.
     • MODPO: linear scalarization with weights from Bayesian-optimized 5-point sweep on the held-out split.


15     Benchmark Splits and Contamination Audit

15.1    TravelPlanner test split
The TravelPlanner test split (1,000 queries) labels are not publicly available; we therefore evaluate only on
the 180-query validation split in the main paper and do not claim test-set results. We release SynPlan-8B’s
decoded plans for the full test split together with our evaluation scripts so that future work with test-label
access can independently compute test-split pass rate.

15.2     NaturalPlan full Meeting Planning
Repeating Table 3 on the full 1,000-instance Meeting Planning split: SynPlan-8B SR is 92.1% (921/1,000, CI
[90.3, 93.6]); LRPlan-MAS SR is 94.6% (946/1,000, CI [93.0, 95.9]); the protocol gap is consistent with our
200-instance result. We additionally evaluate Trip Planning (SR 61.4%) and Calendar Scheduling (SR 73.2%);
both substantially exceed the plain-DPO ablation baselines.

15.3     PlanBench Blocksworld full split
We sample 150 instances stratified by problem complexity (3- to 5-block configurations); the full 600-instance
run yields Acc 66.5% (399/600, CI [62.6, 70.2]), within bootstrap noise of our 150-instance Table 5 number
(67.3%). Mystery Blocksworld results are reported in App. 19.

15.4     Contamination Audit
We performed an N-gram overlap audit between our synthesized D and (a) TravelPlanner’s reference plans, (b)
NaturalPlan’s gold schedules, and (c) PlanBench’s ground-truth action sequences. We report the maximum
8-gram overlap across all 15,000 synthesized plans:
Zero overlap reflects that our synthesis uses procedurally generated profiles and KBs disjoint from any
benchmark example.




                                                        15
Table 10 Contamination audit (max 8-gram overlap with benchmarks).


                               Benchmark                             Max 8-gram overlap
                               TravelPlanner reference plans                   0.0%
                               TravelPlanner queries                           0.0%
                               NaturalPlan gold schedules                      0.0%
                               PlanBench action sequences                      0.0%

Table 11 Margin-source ablation, TravelPlanner-val. All variants use the same D and the same SFT initialization.


                         Margin source mc                                   PR % (count)      S̄
                         Random ∼ Unif[0, 1]                                65.6 (118/180)   0.53
                         Length-difference (R-DPO style)                    67.8 (122/180)   0.54
                         Reward-model gap                                   73.3 (132/180)   0.56
                         Raw severity (un-normalized)                       84.4 (152/180)   0.61
                         Verifier-derived normalized severity (ours)        89.4 (161/180)   0.64



16    Margin-Source Ablation (full table)

17    Sensitivity grid

Table 12 Sensitivity of TravelPlanner-val PR (%) to λ and γ.


                                                    γ = 0.5       γ = 1.5    γ = 3.0
                                       λ = 0.005      81.7         84.4        83.3
                                       λ = 0.01       84.4         89.4        87.8
                                       λ = 0.02       83.3         87.2        82.2



18    Soft-Objective Weight Sweep

19    Mystery Blocksworld
On the obfuscated Mystery Blocksworld split (N = 600), SynPlan-8B attains 42.7% accuracy versus 24.3% for
plain DPO and 39.8% for SimPO. The drop relative to standard Blocksworld (−23.8 pts) is consistent with
prior reports (Valmeekam et al., 2023) that Mystery Blocksworld defeats heuristic shortcut reasoning, but the
residual gap shows that the verifier-derived gradient still imparts non-trivial transferable correction signal.


20     Reasoning-Mode Base Models
Preliminary experiments with Qwen-3-8B in thinking mode under the same SynPlan-R training pipeline
yield TravelPlanner-val PR of 92.1% (166/180), a +2.7 pt gain over the Llama-3-8B SynPlan-8B result. We
exclude this from the main results to keep thinking/non-thinking comparisons clean, and report it here for
completeness.


21    Cost Amortization
Cost-amortized gains saturate near 15,000 pairs, supporting the operating point used in the main paper.




                                                             16
Table 13 Effect of α on TravelPlanner-val.


                                        α                 PR % (count)      S̄
                                        0.0               89.4 (161/180)   0.51
                                        0.3 (default)     89.4 (161/180)   0.64
                                        0.6               88.3 (159/180)   0.66
                                        1.0               86.7 (156/180)   0.68


                            Pairs synthesized     API cost       Marginal pass-rate gain
                            5,000                       $110       +18.4 pt over SFT
                            10,000                      $215           +24.3 pt
                            15,000 (reported)           $320           +25.0 pt
                            25,000                      $535           +25.6 pt


22     Constraint-Weight Ablation
Replacing uniform wj with severity-frequency-weighted wj moves TravelPlanner-val PR by −0.6 ± 0.7 points
(within bootstrap noise); we use uniform weights in all reported results.


23     Qualitative RT-MED Example
Constraint profile.   p = ⟨β=$600, τ =[Fri 9am, Sun 8pm], η=3, Λ={boutique}⟩.

Inverse query.   “Looking for a weekend escape with character; cheap flights ok if hotels are fun.”

Student draft yl (violates budget by $50). SFO→NYC United #482 ($180), Hampton Inn 2 nights at $195
($390), MoMA + dinner ($80) = $650.

RT-MED edit yw ($32-token swap). SFO→NYC United #482 ($180), Pod 51 Boutique 2 nights at $170
($340), MoMA + dinner ($80) = $600. Soft preference “boutique” is now satisfied as a side-effect of choosing a
feasible boutique hotel; in many cases the minimal feasibility edit improves soft satisfaction without targeting
it.

Comparison to full-rewrite distillation. Full-rewrite distillation rewords every section, swaps the flight,
restaurants, hotel, and adds a fourth destination; the resulting yw differs from yl in ∼ 245 tokens, of which
only ∼ 30 are constraint-relevant. Under DPO, the model exploits the ∼ 215 stylistic-distribution tokens as
the implicit margin signal, which is exactly the length-bias failure mode of Park et al. (2024) and Singhal
et al. (2024).




                                                            17
