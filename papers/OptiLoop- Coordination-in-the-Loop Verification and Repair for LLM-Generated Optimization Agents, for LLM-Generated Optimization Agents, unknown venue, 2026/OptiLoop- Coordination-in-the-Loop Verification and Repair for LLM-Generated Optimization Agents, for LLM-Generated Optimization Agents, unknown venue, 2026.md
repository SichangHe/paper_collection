                                                            OptiLoop: Coordination-in-the-Loop Verification and Repair
                                                                    for LLM-Generated Optimization Agents


                                                                                       Yujia Xu 1 Zhiheng Wang 1 Thi Dinh 1


                                                                      Abstract                                     should be validated in the loop itself rather than
arXiv:2605.27630v1 [math.OC] 26 May 2026




                                                                                                                   through isolated execution alone.
                                                   Many decentralized decision problems require
                                                   multiple parties to coordinate on shared decisions
                                                   while keeping objectives, constraints, and data            1. Introduction
                                                   private. Large language models (LLMs) offer
                                                   a promising way to lower the barrier to partici-           Many decision problems of practical interest are decentral-
                                                   pation by generating local optimization agents             ized: multiple stakeholders hold private objectives, con-
                                                   from natural-language specifications. In coor-             straints, and data, yet must still coordinate on shared de-
                                                   dination settings, however, executability is not           cisions. This setting arises in supply planning, resource
                                                   enough: a generated agent may compile, solve,              allocation, and scheduling, where privacy requirements, or-
                                                   and pass local checks while still being seman-             ganizational boundaries, and stakeholder autonomy make
                                                   tically wrong, for example by misrepresenting              a single monolithic optimization model undesirable or in-
                                                   costs, mis-scoping constraints, or responding in-          feasible. A common alternative is to use iterative coordi-
                                                   correctly to incentives. Such errors often surface         nation methods, such as Alternating Direction Method of
                                                   only during coordination, as systematic behav-             Multipliers (ADMM)-style consensus protocols, which re-
                                                   ioral failures rather than infeasibility. We propose       peatedly solve local subproblems while updating shared
                                                   coordination-in-the-loop verification and repair           decisions through structured feedback signals such as dual
                                                   for LLM-generated optimization agents. We in-              prices, penalty terms, and residual-based diagnostics (Nedic
                                                   stantiate this idea with an Alternating Direction          & Ozdaglar, 2009; Boyd et al., 2011). These protocols can
                                                   Method of Multipliers (ADMM)-style consensus               scale well while respecting decentralized control, but they
                                                   protocol and introduce OptiLoop, a pipeline that           rely on a central assumption: each participant implements a
                                                   generates local optimization agents from text, ver-        correct local optimization agent that faithfully represents its
                                                   ifies them through short, bounded coordination             intended private objective and constraints.
                                                   runs against a fixed reference counterparty, ex-
                                                                                                              In practice, this assumption is often the primary bottleneck.
                                                   tracts structured behavioral and static evidence,
                                                                                                              Implementing a local optimization agent requires operations-
                                                   and applies evidence-driven repair. When fail-
                                                                                                              research expertise to formalize business logic as variables,
                                                   ures are structural rather than implementational,
                                                                                                              constraints, and objectives, and engineering expertise to im-
                                                   OptiLoop escalates from localized code fixes to
                                                                                                              plement solver code that correctly responds to protocol feed-
                                                   corrected-formulation repair, and it can addition-
                                                                                                              back. Large language models (LLMs) offer a potential way
                                                   ally reuse episodic lessons from prior instances.
                                                                                                              to reduce this burden by translating natural-language spec-
                                                   On 40 held-out test scenarios, OptiLoop-Full im-
                                                                                                              ifications into mathematical formulations and executable
                                                   proves objective match from 66.0% to 93.0% and
                                                                                                              optimization code. Prior work has shown that LLMs can
                                                   social match from 68.5% to 89.0% relative to a
                                                                                                              often generate executable optimization models from text
                                                   strong local-validation baseline, while reducing
                                                                                                              (Ramamonjison et al., 2023; AhmadiTeshnizi et al., 2024;
                                                   mean objective gap from 15.3% to 3.5% and mean
                                                                                                              Huang et al., 2025). In decentralized coordination settings,
                                                   social gap from 7.6% to 2.0%. These results show
                                                                                                              however, executability alone is insufficient.
                                                   that, for generated optimization agents deployed
                                                   inside decentralized decision loops, correctness           A generated optimization agent may compile, solve, and
                                               1
                                                                                                              pass local checks while still being semantically wrong. It
                                                Amazon, Seattle, WA 98109, USA. Correspondence                may omit a cost term, attach a variable cost to fixed data, or
                                           to: Yujia Xu <yujiaxu@amazon.com>, Zhiheng Wang <zhi-
                                           hengw@amazon.com>, Thi Dinh <thid@amazon.com>.                     mis-scope a constraint while still returning feasible, well-
                                                                                                              formed outputs. Such failures often do not manifest as
                                           Preprint. May 28, 2026.                                            infeasibility; instead, they alter how the agent responds to

                                                                                                          1
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents




                           Figure 1. OptiLoop coordination-in-the-loop verification and repair workflow.


coordination incentives. As a result, errors that remain in-          and the generated agent must be verified for correct behavior
visible under isolated execution may appear only inside the           within that specific environment.
coordination loop, as wrong-sign price response, degener-
ate proposals, slow or unstable convergence, or persistent            Contributions. First, we formalize coordination-in-the-
disagreement with a trusted counterparty. Thus, isolated ex-          loop verification as a validation principle for LLM-
ecution can verify that an agent runs, but not that it behaves        generated local optimization agents in decentralized coor-
coherently under coordination.                                        dination settings, emphasizing deployment-time feedback
This paper proposes coordination-in-the-loop verification             signals rather than isolated execution checks. Second, we in-
and repair for LLM-generated optimization agents. The cen-            troduce OptiLoop, which operationalizes this principle in an
tral idea is to validate a candidate agent using the structured       ADMM-style consensus protocol via diagnostic coordina-
feedback signals produced by the coordination protocol it-            tion episodes, structured evidence extraction, and escalation
self, treating coordination trajectories as semantics-aware           from localized code repair to corrected-formulation repair
verification evidence. We instantiate this principle with an          for structural failures. Third, we provide a benchmark and
ADMM-style consensus protocol and introduce OptiLoop,                 ablation study showing that coordination-in-the-loop verifi-
a pipeline for generating, verifying, and repairing optimiza-         cation exposes semantic failures missed by local validation
tion agents from natural language. As shown in Figure 1,              and materially improves correctness on held-out decentral-
OptiLoop first generates and locally validates a candidate            ized scenarios.
agent, then runs a short coordination episode against a fixed
trusted counterparty to extract behavioral and static evi-            2. Related Work
dence, and finally uses that evidence to select among ac-
ceptance, localized code repair, and corrected-formulation            OptiLoop sits at the intersection of three lines of work:
repair. The key difference from execution-driven validation           iterative coordination for decentralized optimization, LLM-
is that coordination is used not merely to confirm that an            based optimization modeling from natural language, and
agent runs, but to determine whether it behaves correctly un-         verification and repair for generated programs. Our con-
der incentives and to drive the choice of repair. We study this       tribution is to connect these strands through coordination-
problem in a stack-relative setting, where the coordinator            in-the-loop verification: instead of validating a generated
and trusted counterparty are fixed deployment infrastructure          optimization agent only in isolation, we evaluate and repair
                                                                      it using the structured feedback signals produced by the

                                                                  2
           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

coordination protocol itself.                                        (Jiang et al., 2024) or reduce long repair loops through
                                                                     batched generation and selection (Bouscary & Amin, 2026).
Iterative coordination and decomposition. Large-scale                OptiLoop is closest in spirit to recent efforts on optimization-
and decentralized optimization problems are often solved             aware verification and repair, but differs in the source of
by decomposing them into local subproblems and coordi-               its verification signal. Rather than relying only on isolated
nating shared decisions through structured feedback. Dis-            execution, solver-side checks, or generic self-correction,
tributed optimization methods use message passing to align           OptiLoop uses short, bounded coordination runs to extract
local objectives (Nedic & Ozdaglar, 2009). Consensus                 structured evidence from incentive response, agreement dy-
and penalty-based methods such as ADMM coordinate lo-                namics, and convergence behavior. It then escalates from
cal copies through dual variables and proximal penalties,            localized code fixes to corrected-formulation repair when
with convergence monitored through residuals (Boyd et al.,           failures are structural.
2011). Dual and Lagrangian decomposition similarly update
multiplier-like prices in response to constraint violations
(Fisher, 1981), while master–subproblem methods such as              3. Problem Setting
Benders decomposition refine a master problem using cuts             We consider a decentralized setting in which multiple parties
returned by subproblems (Rahmaniani et al., 2017; Xu et al.,         must coordinate on a shared public decision while keeping
2026). Across these methods, a common pattern is itera-              their objectives, constraints, and auxiliary variables private.
tive interaction through feedback signals. OptiLoop builds           Let x ∈ RA×J×T          denote the public decision tensor, in-
                                                                                  ≥0
on this structure by treating coordination trajectories as a         dexed by item i ∈ {1, . . . , A}, node j ∈ {1, . . . , J}, and
source of verification evidence.                                     period t ∈ {1, . . . , T }. Party m has private data Θm , private
                                                                     auxiliary variables ym , and a local copy xm of the public
LLMs for optimization modeling and code genera-                      decision. Its local optimization problem is
tion. A growing literature studies how to translate natural-
language problem descriptions into optimization models and              min cm (xm , ym ; Θm )        s.t.   (xm , ym ) ∈ Fm (Θm ).
                                                                      x m , ym
implementations. NL4Opt frames this problem as a bench-
                                                                                                                                    (1)
mark for extracting variables, constraints, and objectives
                                                                     Define the induced private value function
from text (Ramamonjison et al., 2023). OptiMUS proposes
a modular workflow that formulates optimization models,              fm (x) := min cm (x, ym ; Θm )          s.t.   (x, ym ) ∈ Fm (Θm ),
generates solver code, executes it, and iteratively debugs                        ym
failures (AhmadiTeshnizi et al., 2024). ORLM studies au-                                                                            (2)
tomated optimization modeling using synthetic instruction            and the party-specific feasible public-decision set
data and benchmark suites (Huang et al., 2025). Related
                                                                           Xm := {x ∈ RA×J×T
                                                                                       ≥0    : ∃ ym such that
work also explores multi-agent LLM reasoning for opera-
tions research tasks (Xiao et al., 2023; Quan et al., 2025)                                               (x, ym ) ∈ Fm (Θm )}.
and structure-guided modeling procedures (Pan et al., 2025).
Together, these systems show that LLMs can often gener-              For M parties, a canonical consensus problem is
ate executable optimization models, especially when paired                               M
with modular prompting, decomposition, or iterative refine-                      min
                                                                                         X
                                                                                               fm (xm )
ment.                                                                       x1 ,...,xM
                                                                                         m=1
                                                                                                                                    (3)
                                                                                   s.t. x1 = · · · = xM ,     xm ∈ Xm      ∀m.
Verification and repair. Most LLM-based optimization-
modeling systems still validate candidates primarily through         We instantiate coordination with an ADMM-style consensus
local signals such as successful execution, feasibility, and         protocol (Boyd et al., 2011). The coordinator maintains a
basic correctness checks, then rely on debugging or regen-           consensus plan z ∈ RA×J×T       , party-specific dual tensors
                                                                                             ≥0
eration when failures are detected (AhmadiTeshnizi et al.,           λm ∈ RA×J×T , and elementwise penalty weights ρ ∈
2024). A complementary line of work studies feedback-                RA×J×T   . At iteration k, party m solves
                                                                       >0
driven self-correction with episodic memory, showing that
language agents can improve across attempts by storing                       xk+1 ∈ arg min fm (x)
                                                                              m
and reusing lessons without updating model weights (Shinn                              x∈Xm
                                                                                                      p                             (4)
et al., 2023). Recent work has also emphasized that local val-                      − ⟨λkm , x⟩ + 12 ∥ ρk ⊙ (x − z k )∥22 .
idation is incomplete for optimization because code may ex-
ecute successfully while the underlying formulation remains          where ⊙ denotes elementwise multiplication. As in standard
semantically wrong (Lian et al., 2026). Other approaches             consensus ADMM, the linear dual term encodes the current
introduce optimization-specific self-correction objectives           coordination incentives, while the quadratic penalty term

                                                                 3
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

stabilizes the local update by penalizing deviation from the          We do not propose a new coordination algorithm; the
current consensus iterate. The coordinator then updates               ADMM-style loop and the reference counterparty are fixed
                                                                      infrastructure, and our contribution is to generate, verify,
              M
          1 X k+1                                                     and repair a local optimization agent so that it behaves cor-
z k+1 =        x  ,                                        (5)
          M m=1 m                                                     rectly under feedback-driven coordination.

λk+1 = λkm + ρk ⊙ z k+1 − xk+1
                               
 m                         m     ,           m = 1, . . . , M.
                                                            (6)       4. Methodology

We monitor the primal and dual residuals                              4.1. OptiLoop Pipeline

                     M
                                                                      Given a natural-language problem description and typed
                                             1/2
                                                                      data fields, OptiLoop generates an executable local opti-
                    X
           rk+1 =           ∥xk+1
                              m −z
                                   k+1 2
                                      ∥2             ,     (7)
                      m=1
                                                                      mization agent implementing the interface defined in Sec-
                    √                                                 tion 3. The pipeline has four stages: (1) formulation and
           sk+1 =       M ∥ρk ⊙ (z k+1 − z k )∥2 ,         (8)        code generation, (2) lightweight local validation, (3) in-
and terminate when both fall below prescribed tolerances.             loop verification through a short, bounded coordination run
These residuals measure, respectively, disagreement among             against a fixed counterparty, and (4) evidence-driven diag-
local copies of the public decision and progress of the con-          nosis and repair. The key idea is that coordination behavior
sensus iterate across coordination steps. Exact stopping              provides a semantics-aware verification signal: an agent that
criteria and penalty-adaptation rules are deferred to Ap-             appears plausible under isolated execution may still behave
pendix B.2.                                                           incorrectly when exposed to coordination incentives. This
                                                                      bounded coordination run is not used merely to confirm ex-
OptiLoop treats each party as a black-box optimization                ecutability, but to test whether the generated agent responds
agent implementing                                                    coherently to prices, penalties, and consensus pressure in-
                                              k+1
                                                                      side the deployed feedback loop. Formulation and code
 solve(z k , λkm , ρk ) −→ xk+1
                                                  
                            m , obj decompm         .                 generation are knowledge-augmented through a curated li-
                                                                      brary of operations-research building blocks, together with
Here xk+1
       m    is the proposed public plan and obj decomp
                                                                      learned extensions distilled from training scenarios, that
is an objective decomposition aligned with (4). In our im-
                                                                      provide reusable coordination, constraint, and objective tem-
plementation,
                                                                      plates; additional details are deferred to Appendix A.1.
             private(x) ≈ fm (x),                                     A full pseudocode listing of the pipeline is given in Al-
             price(x) = ⟨λm , x⟩,                          (9)        gorithm 1. Here, q denotes the natural-language problem
                          √             2                             specification, D the typed data schema, Afix the fixed trusted
             prox(x) = 12   ρ ⊙ (x − z) 2 .
                                                                      counterparty, and R the maximum repair budget. OptiLoop
so that the local augmented objective can be read as                  maintains a structured formulation F , generated solver code
                                                                      C, optional retrieved memory M, a coordination trajectory
          private(x) − price(x) + prox(x).                            τ , an extracted evidence report E, and a diagnosis action a.
                                                                      The algorithm shows OptiLoop’s bounded repair loop: after
Here, price(x) captures the current coordination incentive            a failed diagnosis, it applies either localized code repair or
induced by the dual signal: increasing a component of x               corrected-formulation repair, up to budget R.
is rewarded or penalized according to the corresponding
entry of λm . The term prox(x) is a quadratic penalty that            4.2. Evidence Extraction from Coordination
discourages large deviations from the current consensus plan
z, with ρ controlling the strength of this pull component-            Local validation alone cannot reliably detect semantic mod-
wise.                                                                 eling errors that preserve executability while distorting eco-
                                                                      nomic behavior. OptiLoop addresses this gap by convert-
In our target application, correctness is defined relative to         ing a short coordination episode into a structured evidence
a fixed deployed coordination stack: the coordinator, inter-          report E for diagnosis and repair. We run the generated
face contract, and trusted counterparty implementation are            agent against a fixed counterparty, observe the trajectory
held fixed, while the generated agent is evaluated under the          τ of proposals, consensus variables, dual signals, penal-
scenario-specific inputs and coordination signals that arise          ties, residuals, and objective decompositions, and combine
within that environment. Under this definition, correctness           these in-loop signals with lightweight static analysis of the
is not an abstract property of the generated code in isolation;       generated code.
it is a behavioral property of the agent within the deployed
coordination environment.                                             The evidence report contains two complementary sources

                                                                  4
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

Algorithm 1 OptiLoop: Coordination-in-the-Loop Verification and Repair
     Require: Natural-language specification q, typed data schema D, fixed counterparty agent Afix , maximum
          repair budget R
       1: M ← R ETRIEVE M EMORY(q) {optional; empty if memory is disabled}
       2: F ← F ORMULATE(q, D, M) {structured mathematical formulation}
       3: C ← C ODE G EN(F, D, M) {solver code implementing solve}
       4: for r = 1, 2, . . . , R do
       5:   local ← L OCALVALIDATE(C)
       6:   if local = FAIL H ARD then
       7:       C ← PATCH O R R EGENERATE(C, local)
       8:       continue
       9:   end if
     10:    τ ← C OORD RUN(C, Afix ) {short coordination episode}
     11:    E ← E XTRACT E VIDENCE(τ, C) {behavioral and static checks}
     12:    a ← D IAGNOSE(q, F, C, E) {a ∈ {ACCEPT, C ODE F IX, R EFORMULATE}}
     13:    if a = ACCEPT then
     14:        return (F, C)
     15:    else if a = C ODE F IX then
     16:        C ← C ODE F IX(C, E) {localized implementation repair}
     17:    else if a = R EFORMULATE then
     18:        F ← C ORRECT F ORMULATION(q, F, E, M) {structural formulation repair}
     19:        C ← C ODE G EN(F, D, M)
     20:    end if
     21: end for
     22: return (F, C) {best candidate after bounded repair}


of evidence. Behavioral checks evaluate whether the agent             simple rules; for example, ACCEPT is disallowed when hard-
responds coherently to coordination signals, including incen-         fail evidence is present, in which case the system escalates
tive response, degeneracy, marginal behavior, and agreement           to R EFORMULATE.
dynamics. Static checks target code- and formulation-level
                                                                      C ODE F IX targets localized implementation failures such
anti-patterns, such as missing cost terms, costs applied to
                                                                      as missing fields, shape mismatches, or straightforward
fixed data rather than decision variables, inconsistent pri-
                                                                      parameter-binding errors. Patches are intentionally min-
vate decision variables, or malformed outputs. Together,
                                                                      imal in order to reduce the chance of introducing new errors.
these checks address the common case in which a generated
                                                                      R EFORMULATE addresses cases in which the generated
model passes local validation but encodes the wrong eco-
                                                                      formulation itself is wrong. OptiLoop produces a revised
nomics or constraint structure. Static checks can localize
                                                                      formulation F ′ conditioned on the original problem descrip-
suspicious implementation patterns, while in-loop behav-
                                                                      tion, the current formulation, and the evidence report, and
ioral checks test whether the agent behaves correctly as a
                                                                      then regenerates solver code from F ′ . This allows the sys-
participant in the coordination protocol.
                                                                      tem to overwrite faulty modeling choices directly rather
Table 1 summarizes the evidence checks used by OptiLoop,              than relying on prompt-level retrying alone. Additional
listing each check’s source, severity, and diagnostic signal;         implementation details for the diagnosis actions, determin-
implementation thresholds are deferred to Appendix A.2.               istic post-processing rules, and corrected-formulation repair
                                                                      procedure are provided in Appendix A.3.
4.3. Diagnosis and Repair
                                                                      4.4. Episodic Experience Reuse
Given the evidence report E, OptiLoop selects one of three
actions: ACCEPT, C ODE F IX, or R EFORMULATE. If the                  OptiLoop optionally uses episodic experience reuse to re-
agent appears behaviorally coherent and no severe issues are          duce recurring error patterns. At generation time, it retrieves
detected, it is accepted. If the evidence indicates a localized       relevant lessons from prior training instances and injects
implementation problem, OptiLoop applies a targeted code              them into formulation and code generation. The memory
patch. If the evidence instead suggests a structural modeling         store includes both instance-level bug-and-fix patterns and
error, OptiLoop escalates to reformulation. To ensure safety          higher-level modeling principles. Memory is updated only
and consistency, the diagnosis output is filtered through             on training scenarios and frozen during evaluation. Ap-

                                                                  5
             OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

  #   Check                          Source         Severity                                 Diagnostic signal
  1   Utility sign consistency     Behavioral     Hard       Wrong sign in the private utility convention.
  2   Price-response sanity test   Behavioral     Hard       PO moves in the wrong direction under positive coordination prices.
  3   Convergence trajectory       Behavioral      Soft      Residuals converge, decrease, stagnate, oscillate, or decay slowly.
  4   Degenerate plan              Behavioral Hard / warning All-zero or near-zero PO plan when nontrivial fulfillment is expected.
  5   Social-gradient              Behavioral Informational  Local mismatch between private response and social objective near
      perturbation                                           consensus.
  6   Cost–data anti-pattern         Static   Hard / warning Cost parameter is applied to fixed data instead of a decision variable.
  7   Decision-variable audit        Static   Informational Private decision variables are checked against the described decisions.
  8   Marginal-cost consistency    Behavioral      Soft      Marginal utility changes in the wrong direction as PO increases.
  9   Demand-coverage sanity       Behavioral Informational Proposed decisions appear inconsistent with demand or service
                                                             requirements.
 10 Dual-price outlier sanity      Behavioral Informational Large or unstable dual prices indicate persistent disagreement.
 11 Missing cost parameters          Static       Hard       Cost-like input field appears in data but is absent from generated code.
Table 1. Evidence checks used by OptiLoop. Behavioral checks use solver outputs or coordination traces, while static checks analyze
the generated formulation or code without running coordination. Hard signals require repair or escalation; soft signals contribute
supporting evidence; informational signals help localize the failure but do not by themselves trigger repair. The evidence-class ablation in
Appendix C.1 evaluates static and behavioral evidence independently.



pendix A.4 provides further details on what is stored in                 Appendix D provides worked examples of representative
episodic memory, how lessons are retrieved, and how they                 scenarios and failure modes targeted by OptiLoop.
are injected during generation.
                                                                         We use 40 scenarios for training and 40 disjoint scenarios
                                                                         for testing. The split is by scenario instance: both splits
5. Experiments                                                           share common modeling primitives, but the test set intro-
                                                                         duces harder compositions, less common cost structures,
Overview. We evaluate OptiLoop in a controlled ablation
                                                                         more ambiguous natural-language phrasing, and more com-
study designed to isolate the contributions of local valida-
                                                                         plicated constraints, including shared capacity, returns or
tion, coordination-in-the-loop verification and repair, and
                                                                         rework flows, and cross-ASIN coupling. As summarized in
episodic experience reuse. The ablation ladder is cumulative:
                                                                         Appendix B.1, the held-out test set also introduces structural
Baseline-Gen performs natural-language-to-formulation-
                                                                         tags absent from training, including novel cost structures
to-code generation only; Baseline-LocalVal adds syntax
                                                                         and deliberate natural-language challenges. Episodic mem-
checks and local solve validation; OptiLoop-Core further
                                                                         ory is built only from the training scenarios and frozen at
adds coordination-based evidence extraction, diagnosis, and
                                                                         test time.
repair; and OptiLoop-Full additionally incorporates frozen
episodic memory learned from the training scenarios. All
methods use the same underlying LLM and solver stack,
and differ only in which verification, repair, and memory
components are enabled. These baselines are controlled                   Counterparty and coordination protocol. Our evalu-
component ablations of a shared generation pipeline, de-                 ation targets an asymmetric onboarding setting in which
signed to isolate the incremental value of each OptiLoop                 a newly generated agent is integrated into an existing de-
component.                                                               ployed coordination stack. All coordination episodes there-
                                                                         fore pair the generated agent with a hand-coded counter-
Scenarios and split. We evaluate on a bounded hand-                      party agent representing trusted platform-side infrastructure.
authored benchmark of 80 scenarios, each defined by a                    The coordinator, counterparty implementation, and inter-
natural-language description, typed data-field metadata, and             face contract are held constant across scenarios, while the
a concrete data dictionary. Each scenario specifies the gener-           prompt-specified inputs and data vary by instance. This
ated agent’s private modeling problem, including public co-              design isolates errors in the generated agent while matching
ordination variables, auxiliary private variables, parameters,           the intended deployment setting. In-loop verification uses
constraints, and scenario-specific business rules. The sce-              the ADMM-style consensus protocol from Section 3: during
narios instantiate recurring supply-chain primitives such as             generation-time verification, OptiLoop runs short, bounded
order aggregation, inventory balance, warehouse and trans-               coordination episodes to extract evidence from the result-
portation capacity, production and shipping costs, holding               ing agent–counterparty interaction, whereas final evaluation
costs, backlog penalties, and service-level constraints, com-            uses longer runs with early stopping and adaptive penalty
bined with linear, quadratic, and piecewise cost structures.             updates.

                                                                     6
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

Metrics. We report four metrics. Objective match                     2.0%. Thus, coordination-in-the-loop verification improves
(obj match) measures whether the generated agent re-                 not only strict pass/fail correctness, but also the quality of
produces the intended private objective behavior at fixed            imperfect solutions when exact matching is not achieved.
consensus inputs: for reference consensus plans, we com-
pare its objective value with that of the hand-coded reference       6.2. Ablation insights
agent and count a scenario as matched if the relative error
is below 0.1%. Objective gap is the corresponding mean               The main ablation results in Figure 2 separate three sources
relative error, averaged across test conditions and capped at        of improvement. First, Baseline-LocalVal improves over
100% per scenario. Social match (social match) mea-                  generation alone because many invalid agents fail basic exe-
sures whether the final coordinated solution is within 0.1%          cution, feasibility, or interface checks. Second, OptiLoop-
of the optimum of the corresponding centralized joint prob-          Core improves over Baseline-LocalVal because some agents
lem, whose objective is the sum of the two parties’ private          pass local validation but still behave incorrectly during coor-
objectives. Social gap is the corresponding mean relative            dination. These failures are semantic rather than syntactic:
optimality gap, again capped at 100% per scenario. Match             the model may solve successfully, but attach costs to fixed
metrics capture strict correctness, while gap metrics capture        inputs, omit relevant cost terms, or respond in the wrong
the severity of remaining errors. Objective metrics evaluate         direction to prices. In these cases, the agent is not wrong be-
whether the generated local agent encodes the intended pri-          cause it crashes or violates an interface contract; it is wrong
vate model, while social metrics evaluate whether that local         because it encodes the wrong economics under coordination
correctness translates into a good coordinated outcome.              incentives. Coordination-in-the-loop checks expose these
                                                                     errors by testing the generated agent as an economic partici-
                                                                     pant rather than only as executable code. Third, OptiLoop-
Implementation and reproducibility. All methods use                  Full further improves over OptiLoop-Core because episodic
the same underlying LLM, prompting interface, solver stack,          memory helps prevent recurring mistakes before repair is
and evaluation harness, so performance differences reflect           needed, improving both correctness and residual gaps.
the enabled verification and repair components rather than
changes in generation infrastructure. We report five inde-           We also ablate the evidence used by OptiLoop-Core.
pendent runs per method. Although decoding temperature               Static-only evidence uses code-level and interface checks,
is fixed at zero, the serving stack can exhibit small run-to-        Behavioral-only evidence uses coordination traces, and
run nondeterminism, so repeated runs measure end-to-end              Full combines both. Figure 3 shows the recovery pattern
robustness rather than sampling diversity. Additional im-            on the 13 test scenarios where Baseline-LocalVal fails to
plementation and reproducibility details are provided in             achieve objective match. Static-only recovers 4 scenarios
Appendix B.                                                          and Behavioral-only recovers 5, but the recovered subsets
                                                                     differ; Full recovers 8 scenarios, including cases that neither
                                                                     ablation fixes alone. This supports the claim that static local-
6. Results                                                           ization and behavioral confirmation provide complementary
6.1. Main correctness results                                        signals. Appendix C.1 gives the full ablation.

Figure 2 summarizes the main correctness results across              6.3. Efficiency and repair behavior
five independent runs on 40 held-out test scenarios; exact
values are reported in Table 2. The match metrics improve            Table 3 summarizes the efficiency and repair behavior of the
monotonically across the ablation ladder. Adding local vali-         pipeline. OptiLoop-Core improves correctness at the cost of
dation to generation improves objective match from 45.0%             additional coordination and diagnosis calls: compared with
to 66.0% and social match from 48.0% to 68.5%, confirm-              Baseline-LocalVal, its average cost increases from 3.6 to
ing that many failures are still basic execution, feasibility,       6.7 LLM calls and from 51 to 95 seconds per scenario. This
or interface errors. Adding coordination-in-the-loop diag-           overhead reflects the extra short coordination run, evidence
nosis and repair further improves both match metrics to              extraction, diagnosis, and possible repair.
80.0%, indicating that a substantial fraction of locally valid
                                                                     OptiLoop-Full recovers much of that overhead through
agents still behave incorrectly once exposed to coordination
                                                                     episodic experience reuse. With memory enabled, the av-
signals.
                                                                     erage number of LLM calls drops from 6.7 to 4.9, runtime
OptiLoop-Full delivers the strongest overall performance,            decreases from 95 to 67 seconds, and the mean number
reaching 93.0% objective match and 89.0% social match.               of repair iterations falls from 0.77 to 0.31. The diagnosis
The gap metrics show the same pattern, but also quantify             distribution also shifts: the fraction of scenarios accepted
the severity of the remaining errors: relative to Baseline-          without repair rises from 51.5% to 80.5%, while CodeFix
LocalVal, OptiLoop-Full reduces the mean objective gap               becomes rare. This suggests that retrieved lessons primarily
from 15.3% to 3.5% and the mean social gap from 7.6% to              prevent recurring mistakes during generation, rather than

                                                                 7
                           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

                                                                                                           25
                   100   (a) Objective Match                        93
                                                                                                                (b)                                          Objective Gap
                              Social Match                               89                                                                                  Social Gap
                                                       80 80                                               20




                                                                                   Mean Relative Gap (%)
                   80                                                                                            16.4
                                         66 68
Success Rate (%)




                                                                                                                               15.3
                                                                                                           15
                   60                                                                                                                           12.2
                           45 48
                   40                                                                                      10
                                                                                                                                      7.6
                                                                                                                        6.2                            6.0
                   20                                                                                      5                                                    3.5
                                                                                                                                                                      2.0




                                                                                                                                                                             better
                    0                                                                                      0
                           Baseline      Baseline      OptiLoop    OptiLoop                                      Baseline       Baseline        OptiLoop        OptiLoop
                             Gen         LocalVal       Core         Full                                          Gen          LocalVal         Core             Full

Figure 2. Main ablation results on 40 held-out test scenarios. Left: objective match and social match success rates at 0.1% tolerance.
Right: mean relative objective and social gaps to reference solutions, capped at 100% per scenario.

                                   Method               Obj Match (%)         Social Match (%)                          Obj Gap (%)         Social Gap (%)
                                   Baseline-Gen            45.0 ± 3.1            48.0 ± 3.3                              16.4 ± 3.6           6.2 ± 1.7
                                   Baseline-LocalVal       66.0 ± 4.5            68.5 ± 4.2                              15.3 ± 2.6           7.6 ± 1.9
                                   OptiLoop-Core           80.0 ± 4.0            80.0 ± 4.0                              12.2 ± 3.4           6.0 ± 1.9
                                   OptiLoop-Full           93.0 ± 2.1            89.0 ± 2.9                               3.5 ± 1.1           2.0 ± 0.2
Table 2. Correctness metrics (mean ± std across 5 runs on 40 test scenarios). Match metrics report success rate (%) at 0.1% tolerance; gap
metrics report mean relative gap to reference (%), capped at 100% per scenario.



merely making later repair cheaper.                                                               sensus points while still encoding the wrong global cost
                                                                                                  decomposition. Short coordination runs expose some incen-
6.4. Failure analysis                                                                             tive errors, but may not fully identify mistakes that appear
                                                                                                  only in untested operating regions.
Appendix C.2 provides a bug-level taxonomy of the resid-
ual failures, mapping each failure mode to its root cause,                                       Ambiguous specifications. A second class of failures
strongest evidence signal, evidence class, and typical repair                                    comes from natural-language descriptions that admit multi-
action. This taxonomy complements the broader scenario-                                          ple reasonable formalizations. Examples include underspec-
level categories discussed below by showing which errors                                         ified capacity sharing, return or rework flows, and colloquial
are primarily exposed by behavioral checks, which are                                            cost descriptions. In-loop evidence can show that a candi-
caught by static checks, and which require both. It also clar-                                   date agent behaves inconsistently with the reference stack,
ifies why in-loop behavioral evidence is necessary: many                                         but it cannot always determine which business interpretation
residual errors are structurally valid programs that remain                                      was intended without additional clarification.
executable and locally plausible, yet still encode the wrong
economics or constraint scope under coordination.
                                                                                                 Complex constraint composition. The remaining fail-
Even with the full pipeline, 7% of scenario-run instances                                        ures tend to combine several otherwise familiar modeling
fail, corresponding to 14 failure instances across 6 distinct                                    primitives at once. When inventory balance, order aggre-
scenarios. These residual cases are mostly not syntax or                                         gation, shared capacities, lane restrictions, and service con-
interface failures; they are structural or interpretive errors                                   straints interact, the generated agent may omit one con-
that can remain plausible under local validation. We group                                       straint, apply it at the wrong index level, or aggregate the
them into the following three broad categories:                                                  wrong variables. Such errors often preserve feasibility and
                                                                                                 executability, but distort the coordinated solution. These
                                                                                                 cases suggest that future versions should probe a broader
Novel cost structures. Some failures involve cost forms
                                                                                                 set of operating points during verification and explicitly
that are underrepresented in the generation and repair con-
                                                                                                 request clarification when the specification is intrinsically
text, especially piecewise or tiered costs such as regular-
                                                                                                 ambiguous.
versus-overtime production. In these cases, the generated
formulation can respond reasonably near the tested con-                                          Appendix D complements the aggregate results with three

                                                                                   8
             OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

                    Method                     LLM Calls          Time (s)   Accept     CodeFix     Reformulate     #Repairs
                    Baseline-Gen                   2.0             36 ± 0      —           —             —             —
                    Baseline-LocalVal           3.6 ± 0.2          51 ± 2      —           —             —             —
                    OptiLoop-Core               6.7 ± 0.2          95 ± 3    51.5%       25.5%         23.0%          0.77
                    OptiLoop-Full               4.9 ± 0.2          67 ± 3    80.5%        1.0%         18.5%          0.31
 Recovery
Table        of 13 scenarios
       3. Efficiency and repair where
                                metrics Baseline-LocalVal
                                        (mean ± std). LLMfails
                                                          Calls: mean LLM invocations per scenario. Time: wall-clock seconds per
scenario. Accept/CodeFix/Reformulate: fraction of scenarios ending with each diagnosis action. #Repairs: mean number of repair
iterations per scenario.



                                                                                 on price response, residual behavior, and short coordination
           Static-only                         Behavioral-only
          recovers (4)                          recovers (5)                     trajectories. Extending this library to other coordination
                                                           1                     and decomposition mechanisms, such as Benders decom-
                                                          #61                    position, column generation, or dual decomposition, is an
                    2              2            2
                   #50            #36          #65
                                                                                 important direction for future work.
                   #62            #37          #66
                                                                                 Our evaluation also has several limitations. First, it is
                                                                                 matched to the target onboarding setting, where a gener-
                                                                                 ated agent is verified against a fixed coordinator and trusted
                     2                                                           counterparty, so transfer across coordination stacks or coun-
                    #46
                    #68                                                          terparties remains open. Second, our experiments use a
                         Full (OptiLoop-Core)                                    bounded synthetic scenario suite with reference objectives
                              recovers (8)                                       computed by hand-coded solvers, so broader scenario cov-
                                                                                 erage, larger problem scales, and public benchmark suites
                 Neither recovers: 4 [#54, #63, #64, #69]                        would strengthen the empirical case for generality. Third,
                                                                                 although OptiLoop-Full is substantially more efficient than
       Static: 4/13 Behavioral: 5/13 Full: 8/13 Either ablation: 7/13
                                                                                 OptiLoop-Core, it remains more expensive than simple gen-
Figure 3. Recovery of the 13 test scenarios where Baseline-                      eration or local validation, making the current system better
LocalVal fails. Each circle represents the set of scenarios recovered            suited to offline onboarding and pre-deployment verification
by one evidence mode. Numbers inside each region report the num-                 than to latency-sensitive settings.
ber of scenarios in that region, and labels of the form #k denote
benchmark scenario IDs. Static-only and Behavioral-only recover
different subsets, and Full recovers additional scenarios that nei-              8. Conclusion
ther ablation fixes alone.
                                                                                 We introduced OptiLoop, a coordination-in-the-loop veri-
                                                                                 fication and repair pipeline for LLM-generated optimiza-
concrete scenarios. These examples show how the same                             tion agents. By using short coordination episodes to ex-
pipeline behaves across different difficulty levels: a standard                  tract structured behavioral evidence, OptiLoop supports tar-
case where static checks catch an objective-construction mis-                    geted repair ranging from localized code fixes to corrected-
take, a coordination-sensitive case where the error is visible                   formulation repair for structural modeling errors. In a con-
only through behavioral response, and a hard case where                          trolled benchmark study, coordination-in-the-loop diagnosis
novel costs or ambiguous language leave multiple plausible                       and episodic experience reuse consistently improve correct-
formulations. The second case most directly illustrates the                      ness and reduce error relative to local validation alone.
motivation for in-loop verification, since the agent appears
locally valid but reveals its semantic error only when placed                    Taken together, these findings show that local validation is
in the coordination protocol.                                                    incomplete for decentralized LLM-generated optimization
                                                                                 agents: some semantic failures remain hidden under iso-
                                                                                 lated execution and surface only during coordination. This
7. Discussion and Limitations                                                    suggests that generated optimization agents should be eval-
OptiLoop is instantiated with an ADMM-style consensus                            uated, and when necessary repaired, in the same feedback
protocol, but its broader contribution is the coordination-in-                   context in which they will ultimately be deployed.
the-loop verification principle: when generated optimization
agents operate inside feedback-driven decision loops, those
signals provide semantics-aware evidence for verification
and repair. Our current evidence library is therefore special-
ized to ADMM-style coordination, relying most strongly

                                                                             9
           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

References                                                             optimization problems based on their natural language
                                                                       descriptions. In NeurIPS 2022 competition track, pp.
AhmadiTeshnizi, A., Gao, W., and Udell, M. Optimus:
                                                                       189–203. PMLR, 2023.
  Scalable optimization modeling with (mi) lp solvers and
  large language models. arXiv preprint arXiv:2402.10172,            Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and
  2024.                                                                Yao, S. Reflexion: Language agents with verbal reinforce-
                                                                       ment learning. Advances in neural information process-
Bouscary, M. and Amin, S. Optihive: Ensemble selection
                                                                       ing systems, 36:8634–8652, 2023.
  for llm-based optimization via statistical modeling. In
  Proceedings of the AAAI Conference on Artificial Intelli-          Xiao, Z., Zhang, D., Wu, Y., Xu, L., Wang, Y. J., Han, X.,
  gence, volume 40, pp. 30085–30093, 2026.                             Fu, X., Zhong, T., Zeng, J., Song, M., et al. Chain-of-
                                                                       experts: When llms meet complex operations research
Boyd, S., Parikh, N., Chu, E., Peleato, B., and Eckstein, J.           problems. In The twelfth international conference on
  Distributed optimization and statistical learning via the            learning representations, 2023.
  alternating direction method of multipliers, 2011.
                                                                     Xu, Y., Klibi, W., and Montreuil, B. Dynamic deployment
Fisher, M. L. The lagrangian relaxation method for solving             of pooled human-robot resources in urban parcel logistics.
  integer programming problems. Management science, 27                Transportation Research Part B: Methodological, 205:
  (1):1–18, 1981.                                                     103409, 2026.
Huang, C., Tang, Z., Hu, S., Jiang, R., Zheng, X., Ge, D.,
 Wang, B., and Wang, Z. Orlm: A customizable frame-
 work in training large models for automated optimization
  modeling. Operations Research, 73(6):2986–3009, 2025.

Jiang, C., Shu, X., Qian, H., Lu, X., Zhou, J., Zhou, A.,
   and Yu, Y. Llmopt: Learning to define and solve gen-
   eral optimization problems from scratch. arXiv preprint
   arXiv:2410.13213, 2024.

Lian, J. J., Sun, Y., Chen, H., Zhang, C., and Teo, C.-P.
  Reloop: Structured modeling and behavioral verifica-
  tion for reliable llm-based optimization. arXiv preprint
  arXiv:2602.15983, 2026.

Nedic, A. and Ozdaglar, A. Distributed subgradient meth-
  ods for multi-agent optimization. IEEE Transactions on
  automatic control, 54(1):48–61, 2009.

Pan, X., Fang, J., Wu, F., Zhang, S., Hu, Y.-X., Li, S., and
  Li, X.-Y. Guiding large language models in modeling op-
  timization problems via question partitioning. In Proceed-
  ings of the Thirty-Fourth International Joint Conference
  on Artificial Intelligence, IJCAI, pp. 16–22, 2025.

Quan, Y., Xu, Y., Chen, G., Benaben, F., and Montreuil, B.
  Leveraging large language models for risk assessment in
  hyperconnected logistic hub network deployment. arXiv
  preprint arXiv:2503.21115, 2025.

Rahmaniani, R., Crainic, T. G., Gendreau, M., and Rei,
  W. The benders decomposition algorithm: A literature
  review. European Journal of Operational Research, 259
  (3):801–817, 2017.

Ramamonjison, R., Yu, T., Li, R., Li, H., Carenini, G., Ghad-
  dar, B., He, S., Mostajabdaveh, M., Banitalebi-Dehkordi,
  A., Zhou, Z., et al. Nl4opt competition: Formulating

                                                                10
           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

A. Additional Methodology Details
A.1. Knowledge-Augmented Generation
OptiLoop integrates a curated library of operations-research building blocks into the generation pipeline. The library contains
reusable modeling patterns, including coordination terms (e.g., dual-price/subsidy terms and proximal penalties), inventory
balance constraints, order aggregation constraints, warehouse capacity limits, truck volume limits, and objective-assembly
templates. Each block is represented in both mathematical notation and solver-oriented Python/Xpress form. During code
generation, the same blocks, together with a one-shot example and the required solve interface specification, guide the
model in producing executable Xpress solver code.
Beyond the curated library, OptiLoop maintains a learned knowledge base that grows during training. After each successful
generation, an additional LLM call compares the generated code against the existing block library and extracts any new
reusable constraint or objective patterns not already covered, together with common-pitfall notes derived from error-fix pairs
encountered during retries. These learned blocks are appended to the curated base and made available in future generations.
This knowledge base is distinct from episodic experience reuse. The OR block library provides reusable modeling primitives
during generation, whereas episodic memory retrieves instance-level lessons and repair patterns from prior runs.

A.2. Evidence checks
OptiLoop computes an evidence report from two sources: short coordination runs and lightweight static analysis of the
generated agent code. Some checks are hard-fail signals that trigger mandatory escalation, while others provide soft or
informational evidence used by diagnosis.

Thresholds and constants. Unless otherwise noted, the degeneracy warning threshold is 80% zeros; the price-response
test samples 4 public variables and fails if a majority move in the wrong direction; ADMM verification runs are capped at
300 iterations and evaluation runs at 2000 iterations; and the stopping tolerance is 10−4 for both primal and dual residuals.

A.3. Diagnosis and repair rules
Inputs. The diagnosis module receives: (i) the natural-language description, (ii) the generated formulation, (iii) the
evidence report (Table 1), (iv) the generated agent code, (v) data-field shape/type metadata, and (vi) short-term history
across retries.

Actions. The diagnosis module outputs an action a ∈ {ACCEPT, C ODE F IX, R EFORMULATE}. We apply deterministic
post-processing rules to ensure safety and consistency:

 1. If a = ACCEPT and has fail is true, override to R EFORMULATE.

 2. If a = ACCEPT and has fail is false, accept as-is.

 3. If a = C ODE F IX, apply a minimal patch (typically 1–2 lines) and re-run local validation and a short verification
    episode. If the patch does not change the objective behavior, we accept the patched agent as an escape hatch.

 4. If a = R EFORMULATE, perform structural repair as described below; retries are bounded.

Corrected-formulation repair. When the action is R EFORMULATE, the repair module may emit an explicit corrected
mathematical formulation F ′ (sets/indices, parameters, variables, objective, constraints). If present, OptiLoop replaces the
current formulation with F ′ , regenerates solver code from F ′ , and re-enters verification. This mechanism directly overwrites
structural modeling errors and mitigates repeated failure modes observed under prompt-level “retry with feedback.”

A.4. Episodic memory
OptiLoop optionally uses episodic experience reuse to reduce recurring semantic errors. Memory stores (i) scenario-level
lessons describing error patterns and fixes and (ii) meta-lessons distilled across scenarios. Retrieved lessons are injected as
mandatory rules during formulation and code generation.

                                                              11
           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

What is stored. Each lesson includes a brief problem summary, the failure pattern (what went wrong), the fix pattern
(what corrected it), and a short “do/don’t” rule (e.g., “variable costs must multiply decision variables, not fixed inputs”).
Meta-lessons are always included; scenario lessons are retrieved by similarity to the current prompt.

Retrieval and usage. At generation time, OptiLoop retrieves the top-K most relevant scenario lessons (we use K=3) and
injects them alongside meta-lessons into the formulation and code-generation prompts. Memory is updated only during
training and frozen at test time.

B. Additional Experimental Details
B.1. Benchmark split and evaluation setup
Benchmark split details. We evaluate on 80 hand-authored scenarios with a 40/40 train/test split by scenario instance
rather than by constraint family. Both splits share common modeling primitives such as order aggregation, inventory
balance, warehouse capacity, and transportation costs. The held-out test set, however, introduces additional structural tags,
including congestion costs, piecewise costs, shared-capacity constraints, returns or rework flows, cross-ASIN coupling, and
deliberately ambiguous or terse natural-language phrasing. This split is intended to evaluate generalization under partial
structural overlap: familiar building blocks recur across splits, but the test scenarios require new compositions, less common
cost structures, and linguistic interpretations not seen in the scenarios used to construct episodic memory.

Optimization primitives. The benchmark is built around a retailer–vendor sourcing setting in which a retail platform
coordinates purchase-order decisions with vendors. The shared public decision is the purchase-order quantity, while the
generated vendor-side agent models how it can feasibly and profitably respond to that proposed sourcing plan. Depending
on the scenario, the vendor-side private model may introduce additional variables such as shipment quantities, warehouse
inventory, production quantities, truck counts, shortfall variables, or transfer quantities. These variables determine the
vendor’s feasible response to the public purchase-order decision.
The constraint structure includes several common families. Order-aggregation constraints link the public purchase-order
quantity to private shipment or fulfillment decisions. Inventory-balance constraints track stock across time using initial
inventory, inbound flow, outbound flow, and demand or service requirements. Capacity constraints limit warehouse
throughput, production, storage, transportation lanes, truck volume, or shared resources. Business-rule constraints encode
requirements such as minimum order quantities, blackout periods, allowed lanes, service levels, priority rules, or terminal
inventory targets.
The objective terms also vary across scenarios. Vendor models may include transportation costs, production costs, holding
costs, backlog or shortfall penalties, fixed truck costs, congestion costs, preference weights, and revenue-like utility terms.
These terms are intentionally diverse because many semantic formulation errors arise from objective construction rather
than constraint syntax. For example, a generated model may incorrectly treat a decision-dependent transportation cost as a
fixed constant, use the wrong sign for a utility term, or omit a penalty that appears only implicitly in the natural-language
description.
These primitives make the benchmark more than a code-generation task. The generated vendor-side agent must infer the
algebraic role of each data field: whether it is an index set, parameter, decision-dependent coefficient, bound, cost, or target.
The held-out scenarios therefore test whether the method can assemble familiar sourcing and supply-chain primitives into
new formulations, rather than merely reproduce surface-level code patterns from training scenarios.

Tag overlap. Each scenario is annotated with structural tags (e.g., order aggregation, inventory balance,
congestion cost). Table 4 summarizes the distribution across splits. Both splits share 22 common tags covering
standard modeling primitives, while the test set introduces 28 tags absent from training, including novel cost structures, novel
constraint types, and deliberate linguistic challenges. This split therefore evaluates generalization to unseen compositions
and cost structures rather than simple memorization of recurring training patterns.

Two-party setting and counterparty details. All experiments use the two-party case, consisting of one generated
vendor-side agent and one fixed platform-side counterparty. The counterparty is implemented as a hand-coded Xpress
optimization model and represents a canonical retail inventory-control agent. It optimizes over the shared purchase-order
plan x, balancing inventory holding cost and backlog penalty subject to standard inventory-balance dynamics, with an

                                                              12
             OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

                                       Tag                           Train    Test    Category
                                       Shared tags (present in both splits)
                                       order aggregation              29       36     Logistics
                                       inventory balance              20       31     Inventory
                                       holding cost                   12       19     Objective
                                       transport cost                 15       11     Objective
                                       warehouse capacity             11        9     Capacity
                                       profit maximization            10       4      Objective
                                       truck volume                    6        6     Logistics
                                       safety stock                    3        6     Inventory
                                       blackout window                 4        5     Business rule
                                       outbound rate                   3        4     Capacity
                                       margin target                   2        4     Business rule
                                       inter warehouse transfer        3        3     Logistics

                                       Representative test-only tags (absent from training)
                                       novel structure                 0        5     Structure
                                       ambiguous nl                    0        4     NL challenge
                                       multi echelon                   0        2     Structure
                                       tiered cost                     0        2     Cost structure
                                       large scale                     0        2     Scale
                                       max composition                 0        2     Complexity
                                       factory capacity                0        2     Capacity
                                       rephrased                       0        2     NL challenge
                                       congestion cost                 0        1     Cost structure
                                       piecewise cost                  0        1     Cost structure
                                       shared capacity                 0        1     Capacity
                                       cross asin coupling             0        1     Structure
                                       returns rework                  0        1     Structure
                                       lead time                       0        1     Structure
                                       inventory aging                 0        1     Cost structure
                                       terse phrasing                  0        1     NL challenge
                                       verbose phrasing                0        1     NL challenge
Table 4. Structural tag distribution across train and test splits. We show the 12 most frequent shared tags and 17 representative test-only
tags, out of 22 shared and 28 test-only tags overall. Every scenario also carries the QP tag, since all models are convex quadratic programs.




additional terminal penalty that encourages ending inventory to remain near a safety-stock target. The counterparty is
held fixed across methods, scenarios, and coordination episodes, so that differences in performance reflect the quality of
the generated agent and the verification pipeline rather than variation in the trusted platform-side model. Consequently,
anomalies observed during in-loop verification can be attributed to the generated agent’s formulation or behavior rather than
to counterparty variability.

B.2. ADMM stopping and penalty adaptation.
We instantiate coordination-in-the-loop verification with an ADMM-style consensus protocol (Boyd et al., 2011). For
consistency with the consensus formulation in Section 3, we use the standard consensus-ADMM primal residual and its
corresponding dual residual, generalized to elementwise penalty weights.


Stopping rule.      We monitor the primal and dual residuals

                                                           M
                                                          X                         1/2
                                                 rk+1 =            ∥xk+1
                                                                     m −z
                                                                          k+1 2
                                                                             ∥2             ,                                           (10)
                                                             m=1
                                                          √
                                                 sk+1 =       M ∥ρk ⊙ (z k+1 − z k )∥2 ,                                                (11)

and stop early when both rk+1 < 10−4 and sk+1 < 10−4 .

                                                                    13
           OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

Penalty adaptation.    We adapt ρ to balance primal and dual progress:
                                                 
                                                      k
                                                 2ρ
                                                         if rk+1 > 10 · sk+1 ,
                                         ρk+1 = 12 ρk if sk+1 > 10 · rk+1 ,                                             (12)
                                                 
                                                  k
                                                   ρ      otherwise.

In verification runs we cap ADMM at 300 iterations; in evaluation runs we allow up to 2000 iterations, with the same
stopping and adaptation rules.

B.3. Implementation and evaluation protocol
Reproducibility details. The LLM is Claude Sonnet 4 (us.anthropic.claude-sonnet-4-20250514-v1:0)
accessed via Amazon Bedrock. We use temperature = 0.0 and a maximum output length of 16,000 tokens. All optimization
models are solved with FICO Xpress (QP-capable). When episodic memory is enabled, retrieval uses Amazon Titan Text
Embeddings v2 (1024 dimensions). The memory store contains 50 frozen entries derived only from the training split:
40 scenario-specific lessons and 10 meta-lessons. All methods use the same model and inference settings; the reported
run-to-run variability arises from small serving-side nondeterminism despite temperature-zero decoding.

Runs and evaluation. We report five independent repetitions per method. During generation-time verification, OptiLoop
runs short coordination episodes capped at 300 iterations. During final evaluation, coordination runs are capped at 2000
iterations with early stopping and adaptive penalty updates, using the stopping tolerances and penalty-adaptation rules
reported in Appendix B.2.

C. Supplementary Results
C.1. Additional Evidence-Ablation Details
Section 6.2 summarizes the evidence-type ablation. Here we provide the full ablation setup and scenario-level recovery
details. We hold generation, local validation, repair budget, and evaluation protocol fixed, and compare four modes: (i)
Baseline-LocalVal, which performs no in-loop diagnosis; (ii) Static-only, which uses only code-level and interface evidence
(Checks 6, 7, 11); (iii) Behavioral-only, which uses only in-loop coordination evidence (Checks 1–5, 8–10); and (iv) Full
(OptiLoop-Core), which combines both evidence sources. In Static-only mode, the ADMM summary is also suppressed,
including residual trajectories, per-variable residuals, and dual prices, so that the diagnosis LLM cannot infer behavioral
signals from raw coordination traces.
Figure 3 in the main text visualizes recovery on the 13 test scenarios where Baseline-LocalVal fails to achieve objective
match. Static-only evidence recovers 4 scenarios, Behavioral-only evidence recovers 5, and Full evidence recovers 8. The
recovered subsets differ: scenarios #50 and #62 are recovered only by static checks, which detect missing cost parameters
and cost-applied-to-fixed-data patterns, while scenario #61 is recovered only by behavioral checks, which detect wrong-sign
marginal response during coordination. Scenarios #36 and #37 are recovered by either evidence type independently.
Scenarios #46 and #68 are recovered only by Full evidence, indicating that static localization and behavioral confirmation
can jointly enable repairs that neither signal enables independently. Scenarios #54, #63, #64, and #69 remain unrecovered
by any method and correspond to the hard residual cases discussed in Appendix C.2.
Because diagnosis and repair are LLM-mediated, Full evidence is not a strict per-scenario union of Static-only and
Behavioral-only evidence. Adding evidence can change the selected repair action, the regenerated formulation, and the
resulting coordination trajectory.

C.2. Failure-mode Taxonomy
Section 6.4 summarizes the residual failure categories. Table 5 provides a bug-level taxonomy that maps each failure
mode to its root cause, strongest evidence signal, evidence class, and typical repair action. The taxonomy clarifies why
local validation is insufficient: several failures produce executable and feasible solver code while still encoding the wrong
incentive response, cost structure, or constraint scope.
The three scenario-level categories discussed in Section 6.4 arise from different bug-level mechanisms in Table 5. Novel
cost structures most often lead to missing or mis-specified objective terms. Ambiguous specifications can produce wrong

                                                             14
             OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

  Failure mode                  Root cause                                   Best signal                   Evidence class    Typical fix
  Interface / shape           Wrong tensor shape or missing                  Local validation              Neither (local)   CodeFix
  mismatch                    decomposition output
  Wrong incentive response Sign error, missing coupling term, or             Private-objective sign (C1)   Behavioral        Reformulate
                              mis-specified objective                        + price-response (C2)
  Cost attached to fixed data Cost multiplies a parameter rather             Pattern check (C6) +          Both              Reformulate
                              than a decision variable                       price-response (C2)
  Missing cost term           Cost key exists in data but unused in          Missing-cost (C11)            Static            CodeFix or
                              code                                                                                           Reformulate
  Constraint scope bug        Missing index, incorrect aggregation,          Convergence (C3) +           Both               Reformulate
                              or omitted constraint                          decision-variable audit (C7)
  Degenerate proposals        All-zero plan, dominated objective, or         Degeneracy (C4)              Behavioral         Reformulate
                              bad bounds
Table 5. Failure-mode taxonomy for generated optimization agents. Check numbers refer to the evidence checks in Table 1. The
Evidence class column indicates whether the failure is primarily caught by behavioral (in-loop) checks, static (code-level) checks, or both,
corresponding to the ablation in Section 6.2.



incentive response or constraint-scope bugs because multiple formalizations are plausible from the text. Complex constraint
composition primarily appears as scope, indexing, or aggregation errors. Together, these cases explain why the remaining
failures are mostly structural rather than syntactic.

D. Worked Scenario Examples
We provide three representative scenarios spanning the difficulty range: an easy training scenario, a medium test scenario
that illustrates a failure mode caught by coordination-in-the-loop verification, and a hard test scenario with novel cost
structure.

D.1. Example 1: Training Scenario (Easy)
Tags.    QP, order aggregation, warehouse capacity, transport cost

Natural-language specification. “A vendor operates a single warehouse and ships 2 ASINs to 2 Retail inbound nodes
over 3 weeks. The warehouse has a maximum outbound shipping capacity of 150 units per ASIN per week. Transportation
costs vary by destination: to node 1, $2 per unit; to node 2, $3 per unit. The vendor wants to minimize total transportation
cost while respecting the warehouse outbound capacity.”

Data schema.

   • transport cost: shape (J, )
   • warehouse capacity: float
   • Problem size: A = 2, J = 2, T = 3

Intended formulation. The agent defines shipment variables si,w,j,t ≥ 0 (or equivalently si,j,t in the single-warehouse
case), enforces order aggregation                      X
                                             poi,j,t =     si,w,j,t ,                                              (13)
                                                                         w
and imposes the outbound-capacity constraint
                                    X
                                        si,w,j,t ≤ warehouse capacity                           ∀i, t.                                     (14)
                                             j

The objective is                                         X
                                                   min           transport costj · si,j,t .                                                (15)
                                                         i,j,t


                                                                       15
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

Why this scenario is easy. This scenario uses only familiar linear costs and constraints from the OR block library. The
main modeling pitfall is attaching transportation cost to a fixed input parameter rather than to the shipment decision variable
— a bug that Check 6 (cost×data anti-pattern) is designed to catch.

D.2. Example 2: Test Scenario (Medium) — Failure Caught Only by Behavioral Evidence
Tags.   QP, order aggregation, inventory balance, shared capacity, ambiguous nl

Natural-language specification. “Our operation is straightforward, but the capacity situation is a bit nuanced. We have
two warehouses, three products, two Retail docks, and three weeks. Making products A, B, and C costs $0.15, $0.25, and
$0.20 per unit, respectively. Shipping costs $0.10 per unit on every lane. Holding inventory costs $0.20 per unit per week.
Each warehouse starts with 40 units of every product and receives 25 units of each product each week. The catch is that
products A and B share a production line: together, they cannot exceed 100 units per warehouse per week. Product C has its
own line with capacity 80 units per warehouse per week. In addition, each warehouse can ship at most 150 units per week in
total across all products and destinations. Keep costs down.”

Data schema.

   • production cost: shape (A, )
   • transport cost per unit: float
   • holding cost: float
   • initial inventory: shape (A, W )
   • procurement: shape (A, W, T )
   • shared line capacity: float
   • dedicated line capacity: float
   • outbound capacity: float
   • Problem size: A = 3, W = 2, J = 2, T = 3

Common LLM failure. The specification says that each warehouse receives 25 units of each product every week.
This is a fixed inflow. However, because the text also says that “making products” has a per-unit cost, the LLM may
introduce an extra controllable production variable prod[w, a, t]. The generated inventory balance then becomes inv =
prev inv + prod + procurement − shipments. This is wrong because the model now has two sources of supply: the fixed
procurement inflow and the new production decision. Since production is costly, the optimizer can set prod = 0 and still
use the fixed procurement inflow to satisfy orders. The model compiles and returns feasible purchase-order quantities, but
the economic meaning is wrong: fulfilled units are no longer charged the intended production cost.

Why static checks miss it. From the code alone, the formulation looks reasonable. It has an inventory balance, it has
production-capacity constraints, and it has a production-cost term in the objective. The variable prod also appears plausible
because the natural-language specification mentions both “making products” and shared production capacity. A static
checker can flag the variable for review, but the diagnosis LLM may still accept it as intended. The key error is not a missing
constraint or a syntax failure. The key error is that prod interacts with the fixed procurement inflow to create a free source
of supply. That interaction is hard to detect by inspecting individual code fragments.

How behavioral checks catch it. Check 8 (marginal-cost consistency) solves the agent at two consensus levels (z=30
and z=80) and computes the marginal change in utility per unit of PO. For a cost-minimizing vendor, asking it to ship
more units should make reported private cost increase, because additional PO volume should create additional production,
shipping, holding, or capacity cost. In other words, if the vendor is asked to do more work, the model should not report that
the vendor is better off. Instead, the generated model has a positive marginal: increasing PO increases reported utility. This
happens because the optimizer sets prod = 0 to avoid production cost and absorbs additional volume through the fixed

                                                              16
            OptiLoop: Coordination-in-the-Loop Verification and Repair for LLM-Generated Optimization Agents

procurement inflow, so the production-cost term contributes nothing to fulfilled units. This wrong-sign marginal is a clear
behavioral signal that the private cost function is structurally incomplete. The behavioral-only diagnosis LLM therefore
triggers R EFORMULATE, producing a corrected formulation that removes the spurious production variable and applies
production cost to the fulfilled flow.

Result. The wrong-sign behavioral signal triggers R EFORMULATE. The corrected formulation removes the spurious
production variable and attaches the per-unit production cost to the fulfilled flow. In our ablation, behavioral-only verification
fixes this scenario and reaches a 0% objective gap, while static-only verification fails with an 89.9% gap. This example
shows why behavioral verification is useful: the incorrect model is executable, feasible, and locally plausible, but its response
to a higher purchase-order target reveals that its economics are wrong.

D.3. Example 3: Test Scenario (Hard)
Tags.   QP, order aggregation, inventory balance, congestion cost, ambiguous nl

Natural-language specification. “We run a couple of warehouses and move two product lines to Retail through two
receiving docks over three weeks. Our stuff costs about $0.30 per unit to make. We keep track of what’s in the warehouse—at
the start of the planning window we’ve got 50 of everything everywhere. Each warehouse gets 30 units of each product per
week from our suppliers. Storage runs us $0.40 per unit sitting around each week. Shipping is $1.50 per unit base, but when
a lane gets busy the cost goes up—there’s a congestion factor of 0.02 per unit squared on top of the base rate.”

Data schema.

   • production cost: float
   • initial inventory: shape (A, W )
   • procurement: shape (A, W, T )
   • holding cost: float
   • base transport cost: float
   • congestion factor: float
   • Problem size: A = 2, W = 2, J = 2, T = 3

Intended formulation. The correct model requires shipment variables, inventory-balance constraints, and order aggrega-
tion:                                                   X
                                              poi,j,t =    si,w,j,t .                                             (16)
                                                                 w
Inventory evolves according to standard balance equations using initial inventory, weekly procurement, outbound shipments,
and ending inventory. The transportation term includes both a linear base cost and a quadratic congestion term applied to the
shipment decision:          X
                                  base transport cost · si,w,j,t + congestion factor · s2i,w,j,t
                                                                                                 
                                                                                                                         (17)
                            i,w,j,t

The full objective also includes production and holding costs.

Common LLM failure. The LLM often treats congestion factor as a fixed surcharge or multiplies it by
base transport cost (a data×data pattern) rather than applying it as a quadratic term on the shipment decision
variable. The informal phrasing (“gets busy,” “on top of the base rate”) makes the correct interpretation ambiguous.

Why this scenario is hard. This scenario combines informal natural-language phrasing with a nonlinear transport-cost
structure. Both the ambiguous nl and congestion cost tags are absent from the training split, so episodic memory
provides no direct precedent. The agent must infer that the congestion factor defines a per-lane quadratic cost on the
shipment decision variable. Even with full evidence, this scenario fails in approximately 30% of runs, placing it among the
residual hard cases discussed in Section 6.4.

                                                               17
