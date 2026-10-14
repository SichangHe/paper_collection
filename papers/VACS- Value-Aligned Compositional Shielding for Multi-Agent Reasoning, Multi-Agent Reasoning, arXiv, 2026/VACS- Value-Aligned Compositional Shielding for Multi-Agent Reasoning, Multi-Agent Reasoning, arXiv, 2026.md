                                            VACS: Value-Aligned Compositional Shielding for
                                                        Multi-Agent Reasoning


                                                     Yiyao Zhanga , Diksha Goelb , Hussain Ahmadc , Shixun Huanga , Jun Shena
                                             a
                                                 School of Computing and Information Technology, University of Wollongong, Wollongong, NSW,
                                                                                           Australia
                                                                           b
                                                                             CSIRO’s Data61, Clayton, VIC, Australia
arXiv:2609.26135v1 [cs.AI] 7 Aug 2026




                                                  c
                                                    School of Computer Science and Information Technology, Adelaide University, Adelaide, SA,
                                                                                           Australia
                                                 Author e-mail addresses: yiyao.zhang@uow.edu.au (Y. Zhang), diksha.goel@csiro.au (D. Goel),
                                                     hussain.ahmad@adelaide.edu.au (H. Ahmad), shixun_huang@uow.edu.au (S. Huang),
                                                                                  jshen@uow.edu.au (J. Shen)



                                                                                          Abstract
                                                    Multi-agent reasoning systems in high-stakes domains must be both accurate and
                                                    safe, yet agents often follow heterogeneous value priorities (e.g., rigor, concise-
                                                    ness, safety), causing conflicting recommendations. Existing methods do not
                                                    jointly provide: (i) principled inference of each agent’s implicit values from be-
                                                    havior, (ii) compositional formal safety guarantees without full online commu-
                                                    nication, and (iii) value-aware conflict resolution with faithful explanations. We
                                                    present VACS (Value-Aligned Compositional Shielding), a four-layer framework
                                                    addressing all three. Layer 1 learns value-dimension rewards from pairwise pref-
                                                    erences using Bradley–Terry modeling and infers per-agent value weights via deep
                                                    MaxEnt IRL. Layer 2 encodes value constraints in a Lean-inspired DSL and
                                                    synthesizes compositional assume-guarantee shields for runtime safety. Layer
                                                    3 resolves disagreement through nucleolus-based credit allocation and Hamil-
                                                    tonian consensus optimization under long-term value constraints. Layer 4 ex-
                                                    tracts a critical reasoning path from co-state sensitivities and generates formally
                                                    grounded natural-language explanations. Our contribution is primarily a uni-
                                                    fied systems design with formalized interfaces and operational guarantees at the
                                                    verifier-constrained decision level, rather than a complete end-to-end formal proof
                                                    of all language-model internals. In controlled proof-of-concept evaluations with
                                                    role-conditioned agent panels on NEJM-AI QA, MathInstruct-Subset, and a cy-
                                                    bersecurity incident-response benchmark (CyberSec-Eval), VACS outperforms
                                                    strong baselines in accuracy (85.4%, 95.0%, and 90.0%) while reducing logical
                                                    inconsistency rates to near zero.


                                        1    Introduction
                                        Multi-agent reasoning is a powerful paradigm for complex decision-making in high-stakes domains
                                        such as theorem proving and clinical diagnostics: pooling diverse trajectories from agents with
                                        distinct skills and perspectives consistently improves factuality, robustness, and task performance
                                        [7].
                                        Despite this potential, collaborative multi-agent setups introduce a fundamental challenge: individ-
                                        ual agents almost always operate under heterogeneous, implicit value priorities, in proof verification,
                                        strict step-by-step rigor versus intuitive conciseness; in clinical reasoning, maximum diagnostic cov-
                                        erage versus cost-consciousness and patient risk. In current practice, multi-agent systems typically

                                        40th Conference on Neural Information Processing Systems (NeurIPS 2026). Workshop: Who Verifies the Agents? Toward
                                        Reliable Agent Development.
aggregate outputs using simple, ad-hoc rules such as majority voting or confidence-based weight-
ing. These strategies merely pool final outputs and fail to reconcile the underlying value conflicts
between agents [10, 12], so the final group decision can easily become internally inconsistent, un-
safe, or impossible to faithfully justify. There is a pressing need for a framework that can jointly:
(i) infer each agent’s implicit value system from past behavior [24], (ii) formally guarantee that
collective reasoning steps adhere to safe boundaries [3], and (iii) resolve inter-agent disagreements
through principled, value-aware consensus rather than naive statistical aggregation.
To bridge this gap, we propose VACS (Value-Aligned Compositional Shielding), a unified, four-
layer framework that integrates value inference, formal safety, and cooperative consensus into multi-
agent reasoning through a top-to-bottom pipeline: Bradley–Terry preference modeling and deep
Maximum Entropy Inverse Reinforcement Learning (MaxEnt IRL) infer each agent’s implicit value
profile; the learned values are compiled into formal constraints in a Lean-inspired Domain-Specific
Language (DSL) that drive compositional assume-guarantee (AG) shields filtering unsafe actions
at runtime; disagreements are resolved as a cooperative game via nucleolus credit allocation and
Hamiltonian constrained optimization; and critical reasoning paths extracted from Hamiltonian sen-
sitivities ground natural-language explanations in verified proof records. We frame VACS as an
integrative framework that operationalizes existing IRL, verification, and cooperative-optimization
ideas under one deployable pipeline. Our core contributions are:
• Implicit value discovery via IRL: agent value systems are treated as latent variables inferred
  from behavioral trajectories via a joint Bradley–Terry and deep MaxEnt IRL pipeline.
• Compositional safety guarantees: learned values become Lean-DSL constraints with verifier-
  mediated operational guarantees under stated AG assumptions: locally shielded agents guarantee
  global logical consistency without inter-agent communication during execution.
• Economics-grounded conflict resolution: nucleolus-based credit allocation and Hamiltonian op-
  timization produce a value-weighted agreement that is stable and fair to all coalitions.
• Auditable explanation validation: a hybrid structural–gradient explanation layer is validated for
  decision-level faithfulness via expert judgment and intervention-based tests.
• Empirical results: on MathInstruct-Subset, NEJM-AI QA, and CyberSec-Eval, VACS outper-
  forms strong baselines in accuracy (up to 95.0%) while reducing logical inconsistency to zero.

2    Related Work

VACS builds on four mature lines of work: multi-agent/ensemble reasoning, inverse reinforcement
learning, formal verification, and cooperative consensus. Multi-agent LLM systems improve robust-
ness and factuality through diversity, but usually rely on heuristic aggregation rather than explicit
modeling of heterogeneous values [7, 15, 18, 19]; role-specialised LLM panels that score, propose,
and select under a shared objective make the aggregation step particularly load-bearing [4]. Multi-
agent reinforcement learning for autonomous cyber defence raises the same pairing of coordination
and auditability that motivates our Layers 3–4 [9, 22]. IRL and preference-learning methods provide
a principled way to recover latent objectives from behavior and pairwise comparisons [5, 14, 20, 24],
while formal verification and compositional shielding offer deployable safety guarantees for struc-
tured reasoning pipelines [3, 6, 8, 11]; a complementary line gates when an agent should act or
escalate rather than constraining what it may execute [23]. Cooperative-game and voting-based ag-
gregation methods study stable consensus formation, but typically do not incorporate verifier-backed
value constraints [10, 12]. VACS integrates these complementary capabilities, value profiles from
preferences (Layer 1), compositional safety constraints (Layer 2), coalition-aware conflict resolu-
tion (Layer 3), and verifier-tied decision-level explanations (Layer 4), rather than replacing any one
paradigm; this combination is the framework’s main distinction.

3    Preliminaries and Notation

Multi-agent reasoning setting. We consider a panel of n agents J = {1, . . . , n}, where each
agent j ∈ J may be a human specialist or an AI model. Given a reasoning task τ (e.g., a
mathematical problem or clinical scenario), each agent j produces a reasoning trajectory ξ j =
(sj0 , aj0 , sj1 , aj1 , . . . , sjT ), where sjt is the agent’s reasoning state at step t and ajt is its reasoning


                                                        2
Figure 1: End-to-end VACS architecture for one query: Layer 1 infers per-agent value profiles,
Layer 2 enforces compositional safety constraints, Layer 3 performs value-aware consensus, and
Layer 4 produces an auditable explanation record.


action (e.g., applying a proof rule, citing a precedent). The trajectory terminates with a final answer
y j ∈ A.
Definition 3.1 (Value Dimension and Value Profile). A value dimension vk is a property of reason-
ing trajectories that agents may care about to varying degrees, associated with a reward function
Rvk : S × A → R. We consider m = 5 dimensions: logical completeness (v1 ), conciseness (v2 ),
generalisability (v3 ), logical soundness (v4 ), and safety/constraint satisfaction (v5 ). Agent j’s value
profile is a weight vector W j = (W1j , . . . , Wm j
                                                     ) ∈ ∆m−1 , where Wkj is the relative importance
                                                                   Pm
agent j places on vk ; the agent’s composite reward is Rj (ξ) = k=1 Wkj · Rvk (ξ).

Operationalization of “value” as preference/reward dimensions. “Value” is operationalized as
a preference/reward dimension inferred from comparative judgments: each vk is an empirically mea-
surable criterion over trajectories, with definitions fixed before training (e.g., logical completeness
= fraction of required sub-claims addressed; safety = proportion of steps satisfying domain safety
constraints). Throughout, “implicit value system” is shorthand for the latent preference profile over
reward dimensions estimated by Bradley–Terry + MaxEnt IRL. Annotation sources, protocol, relia-
bility statistics, and profile-stability checks are given in Appendix A.

Lean-DSL constraint language. To make agent reasoning verifiable, we represent each value
requirement as a formal rule in a Lean-inspired DSL. Intuitively, each rule says: if certain conditions
hold before an action, then a required condition must hold after the action. Formally, for value
dimension vk , we write a constraint ϕk as

                             ϕk ≡ ∀s ∈ S, a ∈ A : Ψk (s, a) ⇒ Ωk (s′ ),                               (1)

where Ψk (s, a) is the precondition (what must hold before taking action a in state s) and Ωk (s′ )
is the postcondition (what must hold in the next state s′ ). For example, for logical completeness
(ϕ1 ), when an agent applies a proof step, all required premises for that step must be verified in the
resulting state.


4   The VACS Framework

VACS is organised into four layers with a clean top-to-bottom information flow (Figure 1): Layer 1
produces per-agent value profiles {W j } consumed by Layers 2 and 3; Layer 2 produces per-agent
shields {σ j } that wrap agent policies at execution time; Layer 3 produces a consensus answer ŷ ∗
and value alignment score ρ∗ ; and Layer 4 delivers an auditable, decision-relevant explanation E ∗
to the end user.


                                                    3
4.1   Layer 1: Multi-Dimensional Value Grounding and Agent Profiling

Layer 1 is a two-stage pipeline: first grounding preference/reward dimensions from comparative
data, then inferring each agent’s latent preference profile over these dimensions from behavioural
trajectories.

Stage 1: Bradley–Terry value function learning. For each value dimension vk , we collect a
dataset of pairwise comparisons Dk = {(ξi , ξj , yij )}, where yij = 1 if trajectory ξi is preferred
over ξj on dimension vk and yij = 0 otherwise. We model the preference probability using the
Bradley–Terry model [2]:
                                                        exp(Rvk (ξi ))
                            P(ξi ≻k ξj ) =                                       ,                  (2)
                                                 exp(Rvk (ξi )) + exp(Rvk (ξj ))
and learn Rvk by maximising the log-likelihood over Dk :
                             X
          R̂vk = arg max              [yij log P(ξi ≻k ξj ) + (1 − yij ) log P(ξj ≻k ξi )] .        (3)
                      Rvk
                            (ξi ,ξj ,yij )∈Dk

The reward function Rvk is parameterised as a neural network Rvk ,θk and optimised via stochastic
gradient descent.

Stage 2: Deep MaxEnt IRL for agent value profiling. Given the learned value reward functions
{Rvk }m                                                  j
      k=1 , we infer each agent j’s value weight vector W from its historical reasoning trajectories
  j     j          j
D = {ξ1 , . . . , ξNj } using deep MaxEnt IRL [20, 24]:
                                                      Nj
                                     1 X
                    Ŵ j = arg        max   log PW j (ξij ) − λIRL ∥W j ∥22 ,           (4)
                           j
                          W ∈∆  m−1  Nj i=1
                    P                
                      m    j
where PW j (ξ) ∝ exp  k=1 Wk · Rvk (ξ) is the maximum entropy trajectory distribution under
weight vector W j . The gradient of the objective is
                                                Nj
                                 1 X
                     ∇W j LIRL =        f (ξij ) − EPW j [f (ξ)] − 2λIRL W j ,                      (5)
                                 Nj i=1

where f (ξ) = (Rv1 (ξ), . . . , Rvm (ξ))⊤ is the feature vector of trajectory ξ; the expectation is com-
puted via dynamic programming over the reasoning state space.

Computational object for MaxEnt IRL. For free-form reasoning, IRL is instantiated over a
structured abstraction of text traces: states summarize context, working memory, unresolved sub-
questions, and risk flags; actions are typed reasoning operators (e.g., deduce, verify, revise)
obtained by segmenting chain-of-thought text into operator-level steps; and dynamic programming
runs on a discrete abstraction learned by vector quantization over state embeddings (details in Ap-
pendix D). Finally, k-means clustering of the inferred {Ŵ j } into value-type families (e.g., “rigour-
focused”, “efficiency-focused”) informs the coalition structure in Layer 3 and shield synthesis in
Layer 2.

4.2   Layer 2: Value-Aligned Compositional Shield Synthesis

Layer 2 encodes each value dimension as a formal Lean-DSL constraint and synthesises per-agent
compositional shields via AG reasoning.

Lean-DSL constraint encoding. For each value dimension vk and agent j, we encode the value
constraint as a Lean-DSL formula ϕjk specifying the safety requirement for dimension vk in agent j’s
local reasoning scope. The per-agent safety specification is the conjunction of all value constraints
weighted by the agent’s value profile:
                                                 ^
                                       Φj =             ϕjk ,                                     (6)
                                                     k:Wkj >θval



                                                           4
where θval filters out value dimensions to which agent j assigns negligible weight, so that each
shield enforces only the constraints relevant to its agent’s value system, avoiding unnecessary con-
servatism. The five canonical value constraints require that every proof step has all premises veri-
fied in the current state (ϕj1 , completeness); that trajectory length does not exceed a state-dependent
bound Lmax (s) (ϕj2 , conciseness); that steps do not rely on case-specific assumptions absent from
the problem statement (ϕj3 , generalisability); that no step contradicts a previously established fact
(ϕj4 , soundness); and that no action violates hard constraints in the task description (ϕj5 , safety).

Compositional shield synthesis via AG reasoning. After defining each agent’s value-based
safety rules Φj , we build a verifier-guided text shield σ j : S j × Aj → Aj for each agent. In
text reasoning an action is a structured step ajt = (op, args, claim) extracted from the generated
rationale; unsafe actions are those violating any Lean-DSL constraint in Φj . Rather than “nearest
safe replacement”, we use a prune-and-rerank protocol: generate admissible candidate steps, prune
all verifier-failing candidates, then rerank only verifier-approved candidates by semantic proximity
and factual support. The shield follows a simple rule:
                                      
                                      aj ,                       if (sj , aj ) |= Φj ,
                     σ j (sj , aj ) =                                                            (7)
                                      arg ′ min
                                              j  j
                                                   ∥a′ − aj ∥A , otherwise.
                                        a |=Φ (s )

If the proposed action is safe, it is kept unchanged; otherwise the shield generates candidates
C, keeps only the verifier-approved subset Cok = {a′ ∈ C | (sjt , a′ ) |= Φj }, and selects
arg maxa′ ∈Cok [λsem Sim(a′ , ajt ) + λfact Fact(a′ , sjt )], abstaining if Cok = ∅ (pseudocode in Ap-
pendix B).
No-new-error guarantee (operational): because only verifier-approved candidates in Cok can be
executed, replacement cannot introduce a violation of Φj that was absent from the approved set; if
no approved candidate exists, the shield abstains instead of forcing an unsafe rewrite. We emphasize
the scope of this guarantee: it is conditional on the finite candidate set produced at each step, it
ensures no approved-set violation is executed, not that a correct action is present in the pool. It
provides (i) local control (each agent is corrected independently) and (ii) global consistency (unsafe
local actions do not propagate into contradictory collective conclusions).

Assume–guarantee interface for compositionality. The synthesis is compositional: each shield
is constructed assuming other agents also respect their own shields. For each agent j, the local
assumption Aj states that messages from other agents satisfy declared interface predicates over
a common verifier-checked symbol layer Σsh , and the local guarantee Gj states that every exe-
cuted action satisfies Φj and preserves local invariant Ij ; rounds are lock-step with deterministic
tie-breaking (asynchronous updates are outside current guarantees). The compositional proof obli-
gations are
                                            n
                                            ^            n
                                                         ^                   n
                                                                             ^
         (O1) ∀j : Aj ⇒ Gj ,         (O2)         Gj ⇒         Aj ,   (O3)         Gj ⇒ Iglobal ,   (8)
                                            j=1          j=1                 j=1

discharged respectively by local shield verification, interface-compatibility checks over Σsh , and in-
duction over synchronized rounds. Under O1–O3, local shielding composes into global consistency
without full online sharing of internal reasoning traces.

4.3   Layer 3: Nucleolus-Weighted Hamiltonian Consensus

Layer 3 integrates nucleolus-based negotiation with Hamiltonian optimisation to produce a glob-
ally optimal, value-aware consensus: the nucleolus determines the credit allocation among agents,
and the Hamiltonian optimisation uses these credits as weights in the long-term value alignment
objective.
                                                                                 j
Value alignment score. For each agent j, we compute a value alignment score ρ   Pnmeasuring how
well the agent’s recommendations align with the collective value profile W̄ = n1 j=1 W j :

                             ρj = exp −DKL W j ∥ W̄ · accj ,
                                                           
                                                                                             (9)


                                                     5
where accj ∈ [0, 1] is agent j’s historical accuracy on the current task type. The score fuses value
compatibility and empirical reliability multiplicatively: KL to the panel mean captures dimension-
wise mismatch with asymmetric penalty and adapts to panel composition without extra learned
parameters, while the multiplicative form enforces a conjunctive gate, influence is high only when
both alignment and reliability are high, which is desirable in safety-critical consensus where either
failure mode is harmful.

Nucleolus-based credit allocation. When agents disagree, we need a fair way to decide how much
influence each agent should have. We model this as a cooperative game among agents, where a
coalition gets more power if its members strongly support the same answer and have high alignment
scores. For any coalition C ⊆ J :
                                               X
                                  v(C) = max       ρj · ⊮[y j = y],                          (10)
                                            y∈A
                                                  j∈C
i.e., v(C) is the largest alignment-weighted support that coalition C can put behind a single an-
swer. We then compute the nucleolus ν(J , v) [17], which gives a stable and fair credit split by
lexicographically minimizing the largest complaint any coalition could make about the allocation.
A single-pass weighted vote only optimizes global score and ignores coalition grievances: internally
coherent, strongly value-aligned minority coalitions can be repeatedly suppressed, destabilizing iter-
ative deliberation. The nucleolus instead yields a unique allocation that prioritizes stability against
subgroup deviation, suiting persistent multi-agent settings where fairness and strategic robustness
matter beyond one-shot accuracy.

Hamiltonian consensus optimisation. The consensus answer ŷ ∗ is selected by maximising the
Hamiltonian over the space of possible answers, weighted by the nucleolus credit allocation:
                                                                                  
                                                 Xn
            ŷ ∗ = arg max H(y, λ) = arg max       νj · ρj · ⊮[y j = y] + λ⊤ g(y) ,        (11)
                        y∈A                   y∈A
                                                    j=1

where νj is agent j’s nucleolus credit, λ ∈ Rp is a co-state variable, and g(y) ∈ Rp is a vec-
tor of long-term value alignment constraints (e.g., the selected answer must not violate any value
dimension with weight above θval for any agent). The co-state evolves to enforce these constraints:
                              λ(t + 1) = λ(t) + ηλ · max(0, g(ŷ ∗ (t))),                           (12)
and the consensus answer is updated iteratively until the constraints are satisfied. In practice, align-
ment scoring uses a sharpening factor γ, i.e., ρj ← exp(−DKL (W j ∥W̄ )) · (accj )γ . Compared
with constrained reranking over a finite candidate list, which is myopic to dual feasibility and can-
not express how strongly each constraint is active across rounds, the Hamiltonian form introduces
co-states that encode shadow prices for value constraints, enabling principled primal–dual updates
and explicit sensitivity signals later used by Layer 4 for faithful explanation extraction.

4.4   Layer 4: Critical Path Extraction and Explanation Validation

Layer 4 targets decision-level faithfulness: an explanation is faithful if the cited steps are verifiable
and decision-relevant under interventions. The method is hybrid structural+gradient and post hoc:
each explanation step must map to Lean-DSL verified tuples, step salience is ranked by Hamiltonian
sensitivity, and extraction runs after consensus; we do not claim formal minimal necessary-and-
sufficient subsets (empirical validation in Section 5.4).

Critical path extraction from co-state variables. The Hamiltonian co-state λ encodes the sen-
sitivity of the consensus decision to each value alignment constraint. We extract a high-impact
critical path (not claimed minimal or sufficient in a formal sense) by identifying steps with highest
sensitivity:                                                     
                                                     ∂H
                                  CP∗ = (j, t) :           ≥ θ CP .                                (13)
                                                     ∂ajt
For discrete symbolic/text actions, derivatives are computed through a differentiable surrogate: each
action is represented by an embedding e(ajt ) and ranked by κjt = ∂H/∂e(ajt ) , with finite-
                                                                                        2
difference perturbation checks on token logits to verify local ranking stability. θCP controls sparsity,
and decision relevance is established empirically in Section 5.4.


                                                    6
Table 1: Main results across the three evaluated benchmarks. Best in bold, second underlined. LIR
= Logical Inconsistency Rate (%).

      Method            MathInstruct      NEJM-AI QA        CyberSec-Eval      LIR↓     Faith.↑
      Majority Vote          90.5              78.0               64.0          31.7        ,
      Weighted Vote          92.0              80.5               68.0          28.4        ,
      Informed Voting        93.5              81.8               72.0          25.0        ,
      Shield-Only            94.0              78.5               82.0          7.8       0.67
      VACS                   95.0              85.4               90.0           0.0      1.00


Lean-DSL proof structure rendering. We render the critical path as a Lean-DSL proof structure
by mapping each step (j, t) ∈ CP∗ to its corresponding constraint ϕjk and generating a formal proof
certificate:                  n                                                        o
                  Proof ∗ = (ajt , ϕjk , Ψjk (sjt , ajt ), Ωjk (sjt+1 )) : (j, t) ∈ CP∗ ,      (14)
which records each critical action, the value constraint it satisfies, and the verified
pre/postconditions. The proof certificate can be machine-checked by a Lean verifier.

Natural language explanation generation. Two complementary renderers produce user-facing
explanations from Proof ∗ : (A) template-based, filling a structured template with each established
step, the constraint it satisfies, supporting agents with mean alignment score, and dissenting agents
with their primary disagreement dimension; and (B) LLM-based, passing the formal critical-path
tuples to an LLM so the text stays tied to the verified proof structure while being easier to read.

5     Experimental Evaluation
5.1   Experimental Setup

Benchmarks and agent panel. We evaluate VACS on three reasoning benchmarks spanning
mathematics, clinical reasoning, and cybersecurity incident response, each with a panel of four
AI agents and accuracy as the primary metric: MathInstruct-Subset [21] (mathematical reason-
ing, 200 tasks), NEJM-AI QA [13] (clinical decision reasoning, 1,200+ questions, a domain where
model-to-model variation is large enough that aggregation rules matter [16]), and CyberSec-Eval
(cybersecurity incident response, 500 scenarios, reflecting the agentic remediation workflows now
being deployed in security operations [1]). We disclose an important property of this setup: the
panel consists of role-conditioned agents with engineered value emphases (rigour, efficiency, safety,
generalist), so Layer 1 recovery results validate internal consistency of the profiling pipeline in a
controlled setting, not discovery of natural value heterogeneity in unmodified frontier models (Sec-
tion 6).

Baselines. We compare VACS against four baseline methods: Majority Vote, Weighted Vote, In-
formed Voting [10], and Shield-Only compositional verification [3].

Statistical rigor and uncertainty reporting. We evaluate with 10 random seeds for MathInstruct-
Subset and CyberSec-Eval and 5 for NEJM-AI QA (higher-cost regime), reporting mean ± standard
deviation and 95% bootstrap confidence intervals over queries (10,000 resamples). Key VACS-vs-
baseline comparisons use paired two-sided tests (McNemar’s for accuracy, paired permutation tests
for continuous metrics) with effect sizes (Cohen’s h, Cliff’s δ) and Holm–Bonferroni correction at
α = 0.05.

5.2   Main Results

VACS improves over the strongest baseline (Shield-Only) by +1.0, +6.9, and +3.0 points on
MathInstruct-Subset, NEJM-AI QA, and CyberSec-Eval (Table 1), and reduces the logical inconsis-
tency rate from 7.8% to 0.0%, confirming the effectiveness of value-aligned compositional shielding;
across seeds, key gains remain statistically significant after multiple-comparison correction.


                                                 7
Table 2: Ablation study on MathInstruct-Subset. Each row removes one layer. VP = Value Profile
quality (cosine similarity to reference profiles).

      Configuration                             Acc.↑     LIR↓     Faith.↑    VP↑      Cons. Stab.↑
      Full VACS (4 layers)                       95.0      0.0       1.00      0.89        0.94
      w/o Layer 1 (uniform value profiles)       90.5      0.0       1.00      0.41        0.78
      w/o Layer 2 (no shields)                   95.0      14.7      1.00      0.89        0.81
      w/o Layer 3 (majority vote consensus)      90.5      2.0       1.00      0.89        0.63
      w/o Layer 4 (no explanation)               95.0       0.0      0.00      0.89        0.94


5.3    Ablation Study

The ablation results (Table 2) confirm that each layer serves a different role: Layer 1 drives accurate
value recovery, Layer 2 is the main source of inconsistency reduction, Layer 3 improves consensus
quality, and Layer 4 contributes explanation faithfulness rather than predictive accuracy.

5.4    Explanation Faithfulness Validation

We evaluate Layer 4 explanations with a combined automatic-and-human protocol that checks
proof grounding, critical-path coverage, counterfactual sensitivity, and expert judgment across the
three domains; expert raters were blinded domain specialists scoring randomly ordered samples.
Against random rationales, verifier-only traces, and gradient-only saliency, the VACS hybrid attains
the best expert score (4.5/5 vs. 3.4) with strong intervention-based evidence (counterfactual drop
0.50, deletion-AUC 0.41, insertion-AUC 0.59; Appendix C). This supports decision-level faithful-
ness without claiming full global causal completeness; on pure intervention metrics VACS matches
rather than dominates gradient-only saliency, its advantage is combining verifiability with compara-
ble faithfulness.

5.5    Sensitivity Analysis

We analyze robustness to two key hyperparameters on MathInstruct-Subset. Increasing the value
profile threshold θval (shield strictness) eliminates inconsistency (LIR → 0 for θval ≥ 0.2) but overly
strict thresholds degrade accuracy (82.0% at the optimal θval = 0.4 vs. 56.0% at 0.5). Increasing the
sharpening factor γ improves accuracy by weighting expert agents more, peaking around γ = 2.0–
4.0 (88.0% vs. 76.0% at γ = 1.0).
Broader stress conditions show the same pattern: a stable operating region keeps accuracy high while
LIR stays at or near zero; larger panels preserve safety but eventually dilute specialist expertise; and
under mixed panels, preference noise, and adversarial value conflict, VACS degrades gracefully with
low inconsistency. Orchestration overhead is millisecond-scale (latency is dominated by base LLM
generation), and in safety-critical stress tests VACS rejects or remaps unsafe actions in 96.8% of
adversarial cases versus a 31.4% failure rate for unshielded voting baselines.

6     Discussion, Limitations, and Conclusion
VACS is a systems-design and proof-of-concept contribution; we state its limitations explicitly. (i)
Engineered heterogeneity. Because the evaluated panels are role-conditioned, the Layer 1 evaluation
is partially circular: it shows the pipeline recovers value profiles that were deliberately instilled, not
that it identifies latent value structure in independently developed, unmodified models; evaluating
naturally heterogeneous panels from different model families, without revealing intended styles to
Layer 1, is the most important next step. (ii) Stationarity. Layer 1 profiles are estimated offline and
cached, implicitly assuming stable value priorities; LLM agent behavior can drift with prompt, con-
text, and interaction history, and the formulation does not distinguish persistent agent-level values
from task-conditioned preferences or transient strategies, online profile updating and drift detection
are open extensions. (iii) Scope of guarantees. The operational guarantees are verifier-mediated and
conditional on the finite post-shielding candidate set; they do not ensure the correct answer is ever
in the pool, and Layer 4 explanations are not globally causal accounts of latent model computations.


                                                    8
(iv) Cost and generality. Bradley–Terry learning needs many pairwise comparisons per dimension;
Lean-DSL encoding requires domain expertise; and the nucleolus computation is O(n3 ), requir-
ing approximation for large panels at the cost of stability guarantees. Our evaluation covers three
benchmark suites with fixed panel configurations, so external validity remains uncertain.
Conclusion. Under the tested controlled setup, VACS improves accuracy over strong baselines and
reduces logical inconsistency to zero; we position these results as a proof of concept for value-
aligned, verifier-shielded multi-agent reasoning, not evidence of operational readiness.

References
 [1] A. Arifin, Hussain Ahmad, Yiyao Zhang, and Diksha Goel. AgenticVM: Agentic AI for adap-
     tive software vulnerability management. IEEE Software, 2026.
 [2] R. A. Bradley and M. E. Terry. Rank analysis of incomplete block designs: I. The method of
     paired comparisons. Biometrika, 39(3/4):324–345, 1952.
 [3] A. H. Brorholt, K. G. Larsen, and C. Schilling. Compositional shielding and reinforcement
     learning for multi-agent systems. In Proceedings of the 24th International Conference on
     Autonomous Agents and Multiagent Systems (AAMAS 2025), pages 1–9, Detroit, Michigan,
     2025.
 [4] K. Chen, Hussain Ahmad, Diksha Goel, and Claudia Szabo. 3S-Trader: A multi-LLM frame-
     work for adaptive stock scoring, strategy, and selection in portfolio optimization, 2025.
 [5] P. Christiano, J. Leike, T. B. Brown, M. Martic, S. Legg, and D. Amodei. Deep reinforcement
     learning from human preferences. In Advances in Neural Information Processing Systems
     (NeurIPS), volume 30, 2017.
 [6] L. de Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In
     Proceedings of the 28th International Conference on Automated Deduction (CADE), pages
     625–635, 2021.
 [7] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch. Improving factuality and reason-
     ing in language models through multiagent debate. In Proceedings of the 41st International
     Conference on Machine Learning (ICML), 2024.
 [8] T. Gehr, M. Mirman, D. Drachsler-Cohen, P. Tsankov, S. Chaudhuri, and M. Vechev. AI2:
     Safety and robustness certification of neural networks with abstract interpretation. In Proceed-
     ings of the 39th IEEE Symposium on Security and Privacy, pages 3–18, 2018.
 [9] Diksha Goel, Hussain Ahmad, K. Moore, and M. Guo. Co-evolutionary defence of active
     directory attack graphs via GNN-approximated dynamic programming, 2025.
[10] Q. Han. Informed decision-making via voting. In Proceedings of the 24th International Con-
     ference on Autonomous Agents and Multiagent Systems (AAMAS 2025), Detroit, Michigan,
     2025.
[11] G. Katz, C. Barrett, D. L. Dill, K. Julian, and M. J. Kochenderfer. Reluplex: An efficient SMT
     solver for verifying deep neural networks. In Proceedings of the 29th International Conference
     on Computer Aided Verification (CAV), pages 97–117, 2017.
[12] Y. Li, Z. Cao, J. Qiao, and S. Hu. Nucleolus credit assignment for effective coalitions in multi-
     agent systems. In Proceedings of the 24th International Conference on Autonomous Agents
     and Multiagent Systems (AAMAS 2025), Detroit, Michigan, 2025.
[13] NEJM AI Editorial Board. NEJM-AI QA: A clinically grounded benchmark for medical rea-
     soning and decision support. NEJM AI, 2(4):1–15, 2025.
[14] A. Y. Ng and S. J. Russell. Algorithms for inverse reinforcement learning. In Proceedings of
     the 17th International Conference on Machine Learning (ICML), pages 663–670, 2000.
[15] OpenAI. Gpt-4 technical report. Technical report, OpenAI, 2023.


                                                  9
[16] S. Santhosh, F. Abbas, Hussain Ahmad, and Claudia Szabo. Comparative analysis of large
     language models in healthcare, 2026.
[17] D. Schmeidler. The nucleolus of a characteristic function game. SIAM Journal on Applied
     Mathematics, 17(6):1163–1170, 1969.
[18] Hugo Touvron et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint
     arXiv:2307.09288, 2023.
[19] Xinyi Wang et al. A survey of multi-agent large language model systems. arXiv preprint
     arXiv:2402.01680, 2024.
[20] M. Wulfmeier, P. Ondruska, and I. Posner. Maximum entropy deep inverse reinforcement
     learning. arXiv preprint arXiv:1507.04888, 2015.
[21] X. Yue, X. Wang, and Y. Zhang. MathInstruct: A large-scale instruction tuning dataset for
     mathematical reasoning. arXiv preprint arXiv:2402.10176, 2024.
[22] Yiyao Zhang, Diksha Goel, and Hussain Ahmad. Explainable autonomous cyber defense us-
     ing adversarial multi-agent reinforcement learning. Expert Systems with Applications, page
     132741, 2026.
[23] Yiyao Zhang, Diksha Goel, Hussain Ahmad, and Jun Shen. Beyond reactive agents:
     Uncertainty-gated meta-reasoning for tool-augmented decision-making, 2026. Available at
     SSRN 6997675.
[24] B. D. Ziebart, A. Maas, J. A. Bagnell, and A. K. Dey. Maximum entropy inverse reinforcement
     learning. In Proceedings of the 23rd AAAI Conference on Artificial Intelligence, pages 1433–
     1438, 2008.


A    Annotation Protocol and Reliability for Value Operationalization
Preference labels for the five value dimensions come from three sources: (i) domain experts (clinical
and cybersecurity), (ii) trained graduate annotators (mathematics), and (iii) model-assisted pre-labels
that are always human-verified before inclusion. Overall, 72% of labels are human-only and 28%
model-assisted-but-human-verified; no purely synthetic labels are used in the reported main results.
For each domain, annotators compare trajectory pairs under a single target-dimension definition
sheet, blinded to model identity, using a 3-way interface (A preferred, B preferred, tie/uncertain);
tie/uncertain samples are excluded from Bradley–Terry fitting and retained for quality auditing. The
full dimension definitions fixed before training are: (1) logical completeness = fraction of required
sub-claims addressed; (2) conciseness = normalized token-efficiency under correctness; (3) gener-
alisability = transfer success on held-out variants; (4) logical soundness = contradiction-free formal
check rate; (5) safety/constraint satisfaction = proportion of steps satisfying domain safety con-
straints.
Inter-annotator agreement (Krippendorff’s α) per dimension is: completeness 0.79, conciseness
0.74, generalisability 0.71, soundness 0.83, safety 0.86. To test stability of inferred profiles, we
run Layer 1 with 10 random seeds; mean cosine similarity between per-agent weight vectors across
seeds is 0.93 (±0.03), indicating stable estimates. To test redundancy, all pairwise correlations
among dimension rewards remain below 0.62 and variance inflation factors below 2.5, indicating no
severe collinearity.

B    Per-Agent Text Shielding Algorithm

C    Full Explanation Validation Results

D    IRL Computational Object: States, Transitions, and Approximations
A state st is a tuple (ct , mt , qt , rt ) containing context summary, working memory, unresolved sub-
questions, and risk flags derived from the reasoning prefix up to step t. An action at is a typed


                                                  10
Algorithm 1 Per-Agent Text Shielding (Prune-and-Rerank)
Require: State sjt , proposed text action ajt , constraints Φj , candidate generator G
Ensure: Executed safe action ãjt
          j   j
 1: if (st , at ) |= Φj then
 2:      ãt ← ajt
           j

 3: else
 4:      C ← G(sjt , ajt )                               ▷ rule-based/search/model-generated candidates
 5:      Cok ← {a′ ∈ C | (sjt , a′ ) |= Φj }
 6:      if Cok = ∅ then
 7:           ãjt ← abstain                                          ▷ safe fallback, no unsafe execution
 8:      else
 9:           ãjt ← arg maxa′ ∈Cok [λsem Sim(a′ , ajt ) + λfact Fact(a′ , sjt )]
10:      end if
11: end if
                  j           j
12: Execute ãt and return ãt


Table 3: Explanation validation across three domains. CF Drop = relative consensus-margin drop
under top-path counterfactual perturbation. Del-AUC/Ins-AUC are deletion/insertion areas under
normalized consensus score.
 Method                       Expert (1–5)↑ CF Drop↑ Suff.↑ Nec.↑ Del-AUC↓ Ins-AUC↑
 Random rationale                   1.9            0.44       1.00     0.14       0.49          0.51
 Verifier-only trace                3.4            1.00       1.00     1.00       0.51          0.49
 Gradient-only saliency             3.2            0.60       1.00     0.16       0.41          0.59
 VACS Layer 4 (hybrid)              4.5            0.50       1.00     0.16       0.41          0.59


reasoning operator from a finite schema (deduce, retrieve, verify, revise, decide) with slot-
filled arguments, and a trajectory ξ = (s0 , a0 , . . . , sT ) is obtained by segmenting free-form chain-
of-thought text into operator-level steps mapped to this schema.
The underlying text space is continuous, but IRL is performed on a learned discrete abstraction using
vector quantization over state embeddings (codebook size K) for tractable dynamic programming.
Transitions P̂ (st+1 | st , at ) are estimated from observed trajectories; for rare transitions we apply
Laplace smoothing and back-off to embedding-nearest neighbors. The feature expectation term
EPW j [f (ξ)] is computed with forward–backward occupancy measures on the abstract MDP; when
the horizon is long, a truncated-horizon approximation is used. The log-partition log Z(W j ) is
approximated with log-sum-exp over beam-sampled high-probability trajectories plus importance-
weighted Monte Carlo tails. Trajectories used in Layer 1 are primarily observed from agent outputs;
additional trajectories are sampled from current policies for expectation estimation only, not for
supervision labels.




                                                   11
