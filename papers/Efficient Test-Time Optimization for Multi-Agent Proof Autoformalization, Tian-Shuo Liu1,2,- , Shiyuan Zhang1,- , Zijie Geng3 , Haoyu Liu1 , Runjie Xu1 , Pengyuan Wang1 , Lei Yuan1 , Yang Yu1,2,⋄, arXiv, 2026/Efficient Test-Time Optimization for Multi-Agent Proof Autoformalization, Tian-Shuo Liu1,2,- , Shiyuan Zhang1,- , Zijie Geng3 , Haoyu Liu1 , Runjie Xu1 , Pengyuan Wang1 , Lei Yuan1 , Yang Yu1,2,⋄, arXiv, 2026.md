                                         E FFICIENT T EST-T IME O PTIMIZATION FOR M ULTI -A GENT P ROOF
                                                              A UTOFORMALIZATION

                                                                                              A P REPRINT


                                         Tian-Shuo Liu1,2,* , Shiyuan Zhang1,* , Zijie Geng3 , Haoyu Liu1 , Runjie Xu1 , Pengyuan Wang1 , Lei Yuan1 , Yang Yu1,2,⋄
                                                   1 National Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China
                                                                & School of Artificial Intelligence, Nanjing University, Nanjing, China
                                                                               2 Polixir Technologies, Nanjing, China
                                                                   3 University of Science and Technology of China, Hefei, China
                                                                                          * Equal contribution
                                                                                  ⋄ Corresponding: yuy@nju.edu.cn
arXiv:2607.11307v1 [cs.AI] 13 Jul 2026




                                                                                              A BSTRACT
                                                 Full-proof autoformalization bridges extensive mathematical proofs in natural language with for-
                                                 mally validated reasoning, offering a pathway to elevate the ceiling of verifiable mathematical
                                                 reasoning. Unlike statement-level formalization, proof autoformalization is a long-horizon challenge
                                                 requiring coordination of claims, contexts, and dependencies across many proof steps, yet has only
                                                 recently come under focused study. Current approaches either rely on costly model training or
                                                 apply excessive, unguided repair at inference time. To this end, we introduce T O M AP, a multi-agent
                                                 framework that structures proof autoformalization as a Decomposer-Formalizer-Prover pipeline
                                                 with efficient test-time optimization guided by formal verification and semantic rubrics for proof
                                                 quality. Rather than distributing test-time compute across all agents, we perform bottleneck analysis
                                                 and identify the Decomposer as the critical bottleneck: the quality of its atomic, self-contained proof
                                                 units directly determines whether downstream agents can successfully formalize and prove each
                                                 step. T O M AP therefore treats the Formalizer and Prover as downstream executors and efficiently
                                                 focuses test-time compute on Decomposer refinement. This refinement follows a loop inspired by
                                                 GEPA, evolving prompts over candidate decompositions and using formal verification progress
                                                 together with semantic proof rubrics to define a Pareto frontier that guides the next decomposition
                                                 update. Experiments on P ROOF F LOW B ENCH show that T O M AP improves over the best previous
                                                 method by 19.0% when evaluated by both syntactic correctness and semantic faithfulness, while
                                                 requiring lower test-time cost. Scaling analysis shows that most gains emerge within a few iterations
                                                 of decomposition evolution, guiding test-time budget selection.



                                         1   Introduction

                                         Large language models have made rapid progress in mathematical reasoning [Wang et al., 2026a, Lewkowycz et al.,
                                         2022, Azerbayev et al., 2023]. Among these advances, mathematical proof remains a particularly stringent target,
                                         as plausible solutions do not guarantee that intermediate claims, dependencies, and side conditions are logically
                                         valid. This has motivated a growing body of work on combining informal reasoning with formal verification, where
                                         proof assistants provide machine-checkable guarantees [Dekoninck et al., 2025, Jiang et al., 2022, Ren et al., 2025,
                                         Chen et al., 2025]. Autoformalization, translating informal mathematics into formal languages, is the central interface
                                         in this effort [Wu et al., 2022]. Early work focused on statement-level formalization. More recently, full-proof
                                         autoformalization has gained increasing attention, as translating complete proofs more effectively bridges informal
                                         and formal mathematics by leveraging the abundance of natural-language proofs while retaining the rigorous
                                         verifiability of formal systems.
                      Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

This shift, however, fundamentally changes the autoformalization problem. A theorem statement is a localized
translation target [Wu et al., 2022], whereas a full proof is a long-horizon construction of intermediate claims, local
assumptions, and dependencies that must compose into a globally checkable whole [Jiang et al., 2022]. Different
stages of this translation demand distinct LLM capabilities acquired during post-training: natural-language reasoning
for decomposition, formal-language fluency for formalization, and tactic generation for proof search under verifier
feedback [Dong et al., 2024, Ren et al., 2025, Baba et al., 2025, Liu et al., 2026]. This naturally leads to agentic, verifier-
in-the-loop pipelines in which specialized agents handle each stage while a proof assistant provides executable
feedback [Cabral et al., 2025, Wang et al., 2026b, Zhang et al., 2026]. Proof-level paired supervision remains scarce and
costly [Jana et al., 2026, Chen et al., 2025], making large-scale training difficult. Recent systems therefore rely on Lean
as a proof assistant at inference time, using staged repair or iterative refinement to improve candidate proofs [Cabral
et al., 2025, Wang et al., 2026b, Zhang et al., 2026]. In full-proof settings, however, verifier feedback arrives only
after a long generation chain and rarely reveals which upstream decision caused the failure or how the next attempt
should differ. This makes efficient test-time optimization a central challenge: under a fixed budget, where should
feedback be directed in the pipeline, and how can it drive targeted improvement rather than unguided retries?
Following recent agentic approaches to proof generation [Cabral et al., 2025, Ren et al., 2025, Dong et al., 2024], we
decompose full-proof autoformalization into three specialized agents: a Decomposer that splits the informal proof
into sub-propositions, a Formalizer that translates each into Lean, and a Prover that closes each goal. To perform
efficient test-time optimization in this pipeline, our analysis first identifies the Decomposer as the highest-leverage
stage: when it produces atomic, self-contained proof units with explicit dependencies, the downstream agents
face only local obligations that are already within their capabilities. This aligns with prior work that constructs
sketches or subgoals before detailed proving [Jiang et al., 2022, Cabral et al., 2025, Ren et al., 2025, Dong et al., 2024],
demonstrating that the key difficulty is constructing the right decomposition.
Building on this diagnosis, we introduce Test-time Optimization for Multi-Agent Proof autoformalization (T O M AP),
an efficient test-time optimizer for the decomposition agent. For each input, T O M AP maintains a pool of candidate
decompositions that split the informal proof into sub-propositions. Inspired by reflective prompt evolution [Agrawal
et al., 2025], T O M AP iteratively evolves these decompositions, evaluating each candidate against a fixed set of
proof-quality rubrics that score semantic faithfulness, atomicity, self-containedness, and dependency consistency.
The rubric scores, computed before any downstream formalization or proving, define a Pareto frontier that guides
which candidates are retained and revised across iterations. Only when the rubrics judge a candidate ready does
T O M AP commit it to the downstream Formalizer–Prover executor for Lean verification. This two-level design is
central to efficiency: rubric feedback is cheap and dense, steering the bulk of the search, while Lean verification
provides faithful but expensive ground-truth signals reserved for promising candidates. By balancing cheap proxy
feedback against costly true verification, T O M AP converts limited test-time compute into directed decomposition
improvement rather than unguided pipeline retries. Experiments on P ROOF F LOW B ENCH and miniF2F demonstrate
that T O M AP outperforms both training-based and training-free baselines, achieving higher Lean pass rates and
stronger semantic faithfulness at lower time cost. Ablations across evolution epochs reveal a clear time–performance
trade-off that provides practical guidance for iteration budget selection.

2     Full-Proof Autoformalization as a Multi-Agent LLM System
2.1   Problem Setup

Let x = (t, p) denote an input consisting of a natural-language theorem statement t and an informal proof p. Full-
proof autoformalization aims to produce a Lean proof file y that is accepted by the verifier and faithfully follows the
reasoning in p, matching the full-proof setting studied in prior work [Jana et al., 2026]. A monolithic whole-proof
generator samples
                                                   y ∼ M (· | t, p),                                                 (1)
and receives feedback from the Lean verifier V . Unlike statement-level formalization, full-proof translation requires
recovering implicit assumptions, dependency chains, and side conditions from informal text, expressing each local
claim in formal language, and generating valid tactics for every goal. These span distinct capabilities: natural-
language proof understanding, formal-language fluency, and tactic-level proof search. We therefore model full-proof
autoformalization as a multi-stage LLM system whose intermediate outputs can be inspected and revised.
The goal is to maximize end-to-end verification success under a fixed test-time budget B, measured as wall-clock time
in a fixed evaluation environment H, including the hardware, Lean version, model endpoints, maximum parallelism,
and scheduling policy:
                         θ ∗ = arg max Ex∼D 1[rfull (τ ( x; θ )) = pass] s.t. Cost(θ, B) ≤ B.
                                                                       
                                                                                                                   (2)
                                      θ


                                                              2
                     Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

2.2   Multi-Agent Proof Autoformalization Pipeline

Figure 1 illustrates the overall system. We write the LLM agent pipeline as
                                                  Ψθ = Pθ P ◦ Fθ F ◦ Dθ D ,                                          (3)
where D is the natural-language Decomposer, F is the Formalizer, and P is the Prover. These are the three LLM-
driven agents in our system. The prompt or instruction parameters are
                                                       θ = ( θ D , θ F , θ P ).                                      (4)
The Lean verifier V is not part of the agent pipeline; it is an external checker that evaluates the generated Lean proof
file and returns feedback. T O M AP adapts θ D at test time while keeping θ F and θ P fixed.
Given an input x = (t, p), the Decomposer first produces a proof-unit decomposition
                                           z = DθD ( x ) = (Gz , {n1 , . . . , nm }),                                (5)
where Gz records dependencies among proof units. Conceptually, each proof unit is represented as
                                                   n i = ( q i , u i , a i , d i , κ i ),                            (6)
where qi is a local claim, ui are in-scope variables, ai are assumptions, di are dependencies on earlier units, and κi
contains side conditions or proof hints. This tuple is a modeling abstraction; in implementation, each ni is written as
natural-language text.
The purpose of decomposition is to turn a long informal proof into local obligations that downstream agents can
plausibly formalize and prove. A useful proof unit should be atomic enough for the Formalizer and Prover to handle,
but complete enough to specify the right claim, assumptions, side conditions, and dependencies. Decomposition
quality is therefore not the same as granularity alone: simply splitting a proof into more units is not necessarily
better.
For each proof unit ni , the system constructs a local context ci from the theorem, the ordered decomposition, and the
relevant earlier units. The Formalizer produces a formal statement si = Fθ F (ni , ci ), and the Prover produces a proof
script πi = PθP (si , ci ). The statement-proof pairs are assembled into a candidate Lean proof file:

                                   y = Assemble( x, z, {(si , πi )}im=1 ) ,                 r = V ( y ).             (7)
Here r denotes the verifier feedback, including the full-proof result and any available local errors. Later sections use
this feedback to analyze bottlenecks and guide test-time optimization.

3     Weak-Link Analysis of the Multi-Agent Pipeline
Before allocating test-time computation, we first ask where verifier feedback is most useful. In a modular proof-
generation system, the stage at which a Lean error is observed is not necessarily the stage whose revision would
most improve the final proof. Following the bottleneck-localization and controlled-intervention principles distilled
from recent weak-link and causal analyses of multi-agent systems [Bian et al., 2026, Lyu et al., 2026], we measure the
feedback recoverability of each stage: when the same Lean diagnostic trace is exposed to only one editable stage while
the remaining stages are held fixed, which stage yields the largest improvement in end-to-end verification?

Protocol. For each input x = (t, p), we first execute the unmodified Decomposer-Formalizer-Prover pipeline and
record a structured Lean trace,
                                   τ ( x; θ ) = x, z, {(ni , ci , si , πi , ri )}im=1 , rfull ,
                                                                                             
                                                                                                            (8)
where ri contains obligation-level verifier diagnostics, including elaboration outcomes, goal states, and Lean error
messages, and rfull denotes whether the assembled proof file is accepted by Lean. We then construct three matched
revision conditions. Each condition receives the same diagnostic trace, uses the same verification procedure, and is
given the same correction budget; the only varying factor is the stage whose output may be revised.

       • D-Intervene. Only the Decomposer output is editable. Conditioned on the verifier trace, the Decomposer
         revises the natural-language proof-unit specification, including local claims, assumptions, side conditions,
         and context requirements. The Formalizer and Prover are kept fixed and are re-executed on the revised
         decomposition.


                                                                    3
                             Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization


                                                    Multi-Agent Pipeline for Full-Proof Autoformalization

                                                        key interface                                                   Frozen downstream executor

                     1) Input Problem                2) Decomposer (D)                            3) Formalizer (F)                                      4) Prover (P)
                                                                                      Translate subclaim into Lean statements
                                                                                                                                                     Generate tactic proofs
                Natural-language theorem t
                                                                                  lemma l1                                                            for lean statement
                Let 𝑎𝑛 be a sequence of
                                                       Decompose the               (a : ℕ → ℝ) (L r : ℝ)
                positive real numbers,                problem and proof            (ha_pos : ∀ n, 0 < a n)                                               s𝑖 → (𝑠𝑖 , 𝜋𝑖 )
                suppose that the ratio of               into subclaims             (hL_pos : 0 < L)
                consecutive terms 𝑎𝑛 /𝑎𝑛+1
                                                                                   (hL_lt_one : L < 1)
                converges to a real number 𝐿
                                                                 goal
                                                                                   (hL_lim : Filter.Tendsto (fun n => a (n + 1) / a n)
                with 0 < 𝐿 < 1 . Then the
                                                                                  Filter.atTop (nhds L))
                sequence 𝑎𝑛 converges to 0.
                                                                                   (hr_bound : L < r ∧ r < 1) :
                                                                                   r > 0 ∧ ∃ N, ∀ n ≥ N, a (n + 1) / a n < r := by sorry
                     Informal proof p                  u1        u2          u3                                                                       5) Lean Verifier (V)
                              𝑎
               Since 𝑙𝑖𝑚𝑛→∞ 𝑛+1 = 𝐿 with                                          lemma l2
                                                                                                                                                                    Fail
                                𝑎𝑛                                                                                                                   Succeed
               𝐿 < 1, we can choose a real                                         (a : ℕ → ℝ) ( r : ℝ)
               number r such that 𝐿 < 𝑟 < 1.                u4          u5         (ha_pos : ∀ n, 0 < a n) …
               By the definition of limit, there
               exists 𝑁 ∈ ℕ such that for all                                     lemma l3
                       𝑎
               𝑛 ≥ 𝑁, 𝑛+1 < 𝑟. Since each 𝑎𝑛         t, 𝑝 → (u1 , … , um )         (a : ℕ → ℝ) (r : ℝ) (hr : r > 0)                                  No goals       Error
                        𝑎𝑛
               is positive, this implies that for                                  (h_l2 : ∃ N : ℕ, ∀ n ≥ N, a (n + 1) < r * a n) …
               all 𝑛 ≥ 𝑁, 𝑎𝑛+1 < 𝑟𝑎𝑛 …                                            …
                                                                                                     u𝑖 → 𝑠𝑖                                             (𝑠𝑖 , 𝜋𝑖 ) → 𝑉i



                                                                                                                                                     ✓

                          Decomposition               Statement Formalization                 Lean Proof Completion                          Lean Verification




Figure 1: Full-proof autoformalization as a multi-agent pipeline. A natural-language theorem and informal proof are first
decomposed into proof units with local context. The downstream executor then formalizes each unit, proves each local obligation,
and verifies them.

      • F-Intervene. The decomposition and local contexts are fixed. Conditioned on the same verifier trace, the
        Formalizer revises only the formal statements {si }im=1 . The Prover is kept fixed and is re-executed on the
        revised statements.
      • P-Intervene. The decomposition, local contexts, and formal statements are fixed. Conditioned on the same
        verifier trace, the Prover revises only the proof scripts {πi }im=1 .

This matched design isolates the revision locus under identical verifier feedback, rather than comparing generic self-
correction prompts. The resulting gain estimates how much end-to-end verification can be recovered by correcting
each stage under the same diagnostic information and compute budget.

                                                                                                                                     D-Intervene                 +21.2 pp
Results. Figure 2 shows full-proof accuracy over five cor-                                                                                                                    51.1%
                                                                                                                                50   F-Intervene
rection passes on all 184 benchmark samples; samples with-                                                                           P-Intervene
                                                                                                      Full-proof accuracy (%)




out a successful baseline trace are counted as failures. D-
Intervene consistently achieves the highest accuracy, reaching                                                                  45                                            45.1%
94/184 = 51.1% at pass 5, compared with 83/184 = 45.1%
for F-Intervene and 62/184 = 33.7% for P-Intervene. Under a                                                                     40
fixed verifier-feedback budget, revising the natural-language
proof-unit specification yields the largest gain in end-to-end
                                                                                                                                35
verification.                                                                                                                                                                 33.7%

This ordering reveals why the Decomposer is the right target      30
                                                                        baseline 29.9%
for T O M AP. Intuitively, the Decomposer sets the difficulty
of every downstream obligation. Well-scoped, atomic proof             0          1     2        3      4       5
units reduce formalization and proving to local tasks while                            Correction pass
poorly specified units leave the executor with ambiguous or
incomplete goals. That D-Intervene achieves the largest gains Figure 2: Full-proof accuracy over five correction passes
despite a fixed 32B executor confirms that the bottleneck is for each interface intervention.


                                                                                       4
                              Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization


                                                    ToMap: GEPA-Style Optimization of the Decomposer
                  Cheap rubric feedback steers decomposition search; expensive Lean verification is called only for promising candidates.
                                                         GEPA Optimization Loop (cheap, dense feedback)

                              Candidate Pool Zₜ                      Rubric Judge (LLM)                         Pareto Frontier Fₜ
        Input                 𝒛₁: 1. subclaim 1                                                                                                         Reflective Evolution
                                  2. subclaim 2                          Faithfulness to




                                                                                                              Objective 2
                                                                                                 1/1
                                  3. subclaim 3                          original proof
                                  ⋮                                                                                                                    ...
                              𝒁𝟐 : 1. subclaim 1                         Provability of
                                  2. …
                                  3. …
                                                                     ✓   each subclaim
                                                                                                 0/1
                                                                                                                             Objective 1
      Theorem t                   ⋮
                                                                                                                                                          Critique → Revise →
      + Proof p                                                                                                               Pareto frontier          Propose new decomposition

                              𝒁𝟑 : 1. subclaim 1                         Lean                                                 Other candidate
                                                                                                 1/1
                                  2. …                                   friendliness
                                  3. …
                                  ⋮                                                                         Multi-objective selection                  LLM-driven improvement
                                                                                           2/3
                                         ⋮
                                 K candidate                          Cheap proxy feedback                                  Commit top           NO
                               decompositions                                                                               candidate?

                                                                                                                                     YES

                                                            Frozen Executor (expensive, strict verification)                                                          Expensive lean
                                                                                                                                                             Fail
                                                                                                                                                                     verifier feedback

            Committed                          Formalizer (F)                              Prover (P)                           Lean Verifier (V)              Verified
         decomposition z*                                                                                                                                    Lean 4 Proof
                                                                                        >_
                                                                                                                                 .lean
                                                                                                                                                ✓
         𝒁∗ : 1. subclaim 1                                  </>
             2. …
             3. …                                                                       Lean statement                             check in Lean 4
                                                                                                                                                                      ✓
             ⋮                                       Subclaims →
                                                                                          completion
                                                   Lean statements                                                                                                  QED




                                                                                                                       ✓

                  Candidate search                        Rubric scoring                                Verification gate                             Lean execution
Figure 3: T O M AP: GEPA-style test-time optimization of proof decompositions. T O M AP concentrates test-time compute
on the Decomposer interface while keeping the downstream Formalizer-Prover-Lean executor fixed. It maintains a pool of
candidate natural-language decompositions, scores them with proof-quality rubrics measuring semantic faithfulness, atomicity,
self-containedness, and dependency consistency, and uses the resulting Pareto frontier to guide reflective evolution. Only
candidates that pass the rubric-based commit gate are sent to the expensive downstream executor for Lean verification, allowing
cheap dense feedback to steer most of the search while reserving faithful verification for promising decompositions.



decomposition quality. T O M AP therefore directs all test-time compute to the Decomposer, treating the Formalizer
and Prover as fixed executors.



4   T O M AP: Test-Time Optimization of Proof Decompositions

The weak-link analysis of Section 3 identifies the Decomposer as the most recoverable agent in the pipeline. Under a
fixed test-time budget, we therefore prioritize efficient optimization of the decomposition stage. However, simply
applying self-correction through the downstream Formalizer-Prover executor with Lean verification is inefficient:
each Lean call is expensive, and a binary pass/fail signal offers little guidance for the next revision. T O M AP instead
decouples search from verification. A pool of candidate decompositions is evolved using cheap LLM-based rubric
feedback, and the downstream pipeline is invoked only when a candidate meets a quality threshold. By using dense
rubric guidance for the bulk of the search and reserving selective Lean calls for promising candidates, this two-level
design converts limited test-time compute into directed decomposition improvement.


                                                                                                 5
                       Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

Algorithm 1 T O M AP: Test-time Optimization for Multi-Agent Proof autoformalization
Require: Input x = (t, p), max iterations T, gate threshold ϵ
 1: Initialize pool Z0 ← {Dθ D ( x )} via the initial Decomposer output
 2: for t = 1, . . . , T do
 3:     Score each z ∈ Zt−1 : compute ρ(z) via LLM rubric judges
 4:     Compute Pareto frontier Ft−1
 5:     if ∃ z ∈ Ft−1 s.t. mink ρk (z) ≥ ϵ then
 6:         Commit z to Formalizer-Prover; check with V ; return τ ( x; θ )
 7:     end if
 8:     Select parent z∗ ← arg maxz∈Ft−1 ∑k ρk (z)
 9:     Derive critique c ← Critique(z∗ , ρ(z∗ ), x )
10:     Propose z̃ ← ReflectiveProposer(z∗ , c, x ); compute ρ(z̃)
11:     Update Zt ← UpdatePool(Zt−1 ∪ {z̃})
12: end for
13: Fallback: commit z∗ = arg maxz∈FT ∑k ρk (z) to Formalizer-Prover
14: Check with V ; return τ ( x; θ )



Rubric scoring.    Each candidate decomposition z is evaluated by a three-dimensional rubric vector

                             ρ(z) = ρfaithful (z), ρprovable (z), ρLeanfriendly (z) ∈ [0, 1]3 ,
                                                                                   
                                                                                                                   (9)

where ρfaithful measures semantic faithfulness to the original proof p, ρprovable measures the provability of each
proof unit, and ρLeanfriendly measures whether a proof unit is Lean-friendly, such as by eliminating ambiguous
natural-language descriptions. For compact notation, let R = {faithful, provable, Leanfriendly}. Each dimension is
scored by an LLM judge conditioned on x and z, so that ρ j (z) denotes the rubric score of candidate z on dimension
j ∈ R. The rubric vector provides dense, low-cost feedback that approximates downstream verifiability without
executing the full pipeline.

Pareto-guided evolution. T O M AP maintains a candidate pool Zt of size K. Following GEPA [Agrawal et al., 2025],
candidates on the Pareto frontier
                                  Ft = z ∈ Zt ∄ z′ ∈ Zt s.t. ρ(z′ ) ≻ ρ(z) ,
                                       
                                                                                                             (10)
where ≻ denotes component-wise dominance. Candidates in Ft serve as parents for the next generation. At each
iteration, a reflective LLM proposer selects a parent from Ft , receives a structured critique derived from its rubric
scores and the original proof, and generates a revised decomposition. The pool is updated by admitting the new
candidate and discarding dominated ones. Maintaining a Pareto frontier rather than a scalar objective ensures that
evolutionary pressure is distributed across all quality dimensions.

Verification gating.    A candidate z is committed to the Formalizer-Prover executor for Lean verification only when
                                                     min ρ j (z) ≥ ϵ.                                             (11)
                                                     j∈R

Candidates that pass the gate are assembled into a Lean proof file, checked by V , and returned if verified. If no
candidate clears the gate within T iterations, the Pareto-optimal candidate with the highest aggregate rubric score is
committed as a fallback. The gate ensures that expensive Lean calls are reserved for decompositions that already
satisfy the quality criteria predictive of downstream success. Algorithm 1 summarizes the full procedure.

5   Experiments

We conduct a series of experiments and find that, compared with other full-proof autoformalization baselines, the
translations generated by T O M AP achieve the highest semantic faithfulness, while also attaining the best overall
syntactic–semantic performance. In Section 5.1, we introduce the experimental setup, where we align the inference
budgets of substantially different reasoning pipelines as closely as possible and adopt a unified, reliable semantic
evaluation protocol. In Section 5.2, we present the main experimental results. In Section 5.3, we conduct an ablation
study on the number of optimization rounds to evaluate the efficiency of T O M AP.


                                                            6
                     Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

5.1   Experimental Setup

Benchmarks. We evaluate on two datasets comprising natural-language mathematical problems paired with
their corresponding proofs: (1) miniF2F [Zheng et al., 2021] , a widely used benchmark at the level of high-school
mathematical competitions; we use its test split, which contains 244 problems. (2) P ROOF F LOW B ENCH [Cabral et al.,
2025], an undergraduate-level mathematics dataset containing 184 problems. It is specifically designed to evaluate
automated proof formalization pipelines, with an emphasis on proof-oriented problems rather than computational
ones.

Baselines. We compare against existing methods for full-proof autoformalization: P ROOF F LOW [Cabral et al.,
2025] performs step-wise proof formalization, where each stage retains the complete failure trace and uses it for
subsequent retries. ProofBridge [Jana et al., 2026] trains both a retrieval model and a translation model, and employs
a retrieval-augmented fine-tuned model to jointly translate, producing a single Lean proof. M2F [Wang et al., 2026b],
a Codex-based verifier-certified refinement framework for project-level autoformalization. Monotonic [Zhang et al.,
2026] directly optimizes the generated Lean code through iterative translation refinement, producing a single Lean
proof. We also include two naive Codex-based baselines: Codex End2End and Codex D-Correction. The former
prompts Codex to directly translate the complete natural-language proof into a single Lean proof, whereas the latter
uses Codex as an agentic optimizer to iteratively self-correct the Decomposer for 10 iterations.

Evaluation metrics. We consider four evaluation metrics. (1) Syntactic Correctness (SC) measures whether the
Lean code for a problem fully passes verification by the Lean compiler. (2) Semantic Faithfulness (SF) assesses
whether the translation of the natural-language problem and its corresponding proof is semantically faithful. We
largely follow the evaluation protocol of ReForm [Chen et al., 2026], which adopts an LLM-as-a-judge approach with
Qwen3-235B-A22B [Yang et al., 2025] as the judge model. The judgment is binary, reported as True or False, and this
setup has been validated as a relatively reliable method for semantic evaluation. We modify the evaluation target
from the natural-language problem alone to the natural-language problem together with its corresponding proof,
and further require the Lean code to remain semantically faithful to each step of the proof. The evaluation criteria are
provided in Appx A.6. (3) Time denotes the wall-clock time spent on each problem, i.e., the total actual runtime of
the task divided by the number of problems in the task. (4) Output Tokens (OT) denotes the total number of tokens
generated by all LLM calls during the translation for each problem.

Model configuration. Detailed model configurations are provided in Appx B. T O M AP uses Goedel-Formalizer-V2-
32B and Goedel-Prover-V2-32B as its formal language models [Lin et al., 2025]. We choose these two models to cover
two representative model settings: Qwen3-30B-A3B-Instruct-2507 [Yang et al., 2025] serves as a strong open-weight
model that can be locally deployed and reproduced, while Gemini3-Pro [Team et al., 2023] represents a proprietary
frontier model accessed through APIs. T O M AP-Qwen30B and T O M AP-Gemini use Qwen3-30B-A3B-Instruct-2507
and Gemini3-Pro as the natural language model, respectively. The model configuration of P ROOF F LOW is aligned
with that of T O M AP-Gemini, while the other methods keep their original settings.

Inference budget and hyperparameter settings. Due to substantial differences in the inference pipelines of different
methods, it is difficult to compare all methods under a strictly identical inference budget. P ROOF F LOW uses the same
model configuration as our method. We measure the inference budget by the inference time on the same hardware.
Since the prompt lengths of different workflows vary substantially, in parallel invocation scenarios, the time required
to generate the same number of output tokens may differ significantly. We deploy each local model used in our
experiments on a single NVIDIA A800 80GB GPU. Both methods perform parallel invocations, and we ensure that
the degree of parallelism is sufficient to fully utilize the KV cache. For the remaining methods, we jointly control the
running time and the number of output tokens to make the comparison as fair as possible. T O M AP is configured
with 10 optimization iterations, and the gate threshold ϵ is set to 1. The detailed hyperparameters are provided in
Appx C. The Formalizer and Prover in P ROOF F LOW are each allowed up to 5 retries; ProofBridge reports Pass@64;
and Monotonic performs 10 rounds of optimization.

5.2   Main Results

The results are presented in Table 1. Our method achieves the highest scores on Semantic Faithfulness and Syntactic
Correctness ∧ Semantic Faithfulness. Methods that generate a single monolithic Lean proof can achieve relatively
high SC scores, but they struggle to faithfully translate the individual steps of natural-language proofs. In practice,
these methods appear to use the natural-language proof primarily as guidance for producing Lean tactics that pass
verification, rather than as a structure to be translated faithfully. Moreover, they may generate Lean statements that
are semantically incorrect and simplified, which can unduly inflate their Syntactic Correctness scores. By contrast,


                                                           7
                            Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

                                       Table 1: Main results on full-proof autoformalization benchmarks.
                                                 P ROOF F LOW B ENCH                                                            miniF2F
Method
                             Time(s)        OT(k)          SC         SF          SC∧SF             Time(s)         OT(k)          SC          SF          SC∧SF

                                                                        Training-Based

ProofBridge                  113.48          87.39       92.93       9.24             9.24            61.23         63.80         95.08      29.51          28.69

                                                                           Training-Free

Codex End2End       104.22                  21.34        25.00      32.61          21.20              83.62         28.92         49.18      58.20         47.54
M2F                 882.47                 194.40        35.33      38.59          12.50             503.46        197.64         10.66      19.67          7.79
Codex D-Correction 1554.50                 219.14†       57.14      23.63          10.99            1172.33†       199.84†        71.72      33.61         18.44
Monotonic           201.39                 176.42        84.78      15.22          14.67             229.04        143.01        100.00      16.80         16.80
P ROOF F LOW       2348.48†                 90.06        36.41      33.15          15.76            1125.73         49.28         61.89      46.31         35.25
T O M AP-Qwen30B    610.10                  98.81        66.30      27.71          21.10             513.44         83.33        86.89       34.02         29.92
T O M AP-Gemini     850.27                 139.25        63.59      51.09      40.22 (↑19.0%)        665.41         91.07         82.79      63.93      55.74 (↑8.2%)
 Notes. SC denotes syntactic correctness, SF denotes semantic faithfulness, and SC∧SF denotes the percentage of examples satisfying both criteria. Time is the average
 wall-clock time per problem, and OT denotes output tokens in thousands. Bold numbers mark the best semantic and joint syntactic-semantic scores. † marks the
 largest value in each cost column, i.e., Time(s) or OT(k), within the corresponding benchmark. For training-based methods, reported time is inference-only and does
 not include training cost. * T O M AP-Qwen30B and T O M AP-Gemini use Qwen3-30B-A3B-Instruct-2507 and Gemini3-Pro, respectively, as the natural-language model.



step-wise proof formalization better preserves semantic faithfulness by explicitly aligning the formalization process
with intermediate proof steps. T O M AP optimization substantially improves the quality of the decomposition; specific
examples are provided in Appx D. Compared the agentic baseline, Codex End2End, our method achieves absolute
score gains of 38.59% on P ROOF F LOW B ENCH and 33.61% on miniF2F for SC, 18.48% and 5.73% for SF, and 19.02%
and 8.20% for SC∧SF, respectively.

5.3   Ablation Study

We instantiate the Decomposer in T O M AP with Qwen3-30B-A3B-Instruct-2507 and Gemini3-Pro as the natural-
language model, respectively. The stronger Gemini3-Pro setting yields substantially higher Semantic Faithfulness,
while the two settings achieve comparable Syntactic Correctness. This contrast suggests that stronger natural-
language reasoning mainly improves whether the generated formal proof follows the original informal proof,
whereas the remaining syntactic failures are increasingly tied to the fixed formal-language executor, including
statement formalization and tactic generation.
We further study the effect of the maximum number of GEPA-style optimization rounds in Table 2. Increasing the
round budget consistently improves Syntactic Correctness, but also increases wall-clock cost. This exposes a clear
accuracy-cost trade-off: most gains are obtained within a small number of decomposition-evolution rounds, after
which additional rounds provide diminishing returns. The maximum round budget, therefore, serves as a practical
test-time hyperparameter: smaller budgets are preferable when latency or cost is constrained, while larger budgets
can be used when maximizing verification success is the primary objective.

6     Related work
Autoformalization and full-proof formalization. Autoformalization with Large Language Models [Wu et al.,
2022] studies LLM-based translation from informal mathematics to formal languages such as Isabelle and Lean.
Recent work moves from theorem-only translation toward full-proof autoformalization. P ROOF F LOW [Cabral et al.,
2025] constructs dependency graphs for faithful proof autoformalization, ProofBridge [Jana et al., 2026] aligns
natural-language and formal proof representations through joint embeddings, M2F [Wang et al., 2026b] targets auto-
formalization of mathematical literature at scale, and Monotonic [Zhang et al., 2026] studies iterative improvement
for autoformalization without relying on formal references. T O M AP performs step-wise proof autoformalization and
iteratively optimizes the pipeline by targeting the Decomposer.

Weak-link and causal analysis of multi-agent systems. Agent systems study how autonomous agents perceive task
contexts, interact with environments, and act to solve problems, with multi-agent compositions further introducing


                                                                                  8
                    Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

                             Table 2: Syntactic correctness under different maximum rounds.
                                                            P ROOF F LOW B ENCH                      miniF2F
Method                        Max Rounds
                                                            Syntactic Correctness              Syntactic Correctness
                                    1                          39.67                               57.78
                                    3                          52.72     (↑13.05%)                 75.41    (↑17.63%)
T O M AP-Qwen30B
                                    5                          59.24     (↑6.52%)                  81.15    (↑5.74%)
                                    10                         66.30     (↑7.06%)                  86.89    (↑5.74%)

                                    1                          35.33                               61.89
                                    3                          50.54     (↑15.21%)                 75.41    (↑13.52%)
T O M AP-Gemini
                                    5                          56.52     (↑5.98%)                  79.09    (↑3.68%)
                                    10                         63.59     (↑7.07%)                  82.79    (↑3.70%)




challenges in coordination, communication, and role specialization [Liu et al., 2025, Zhang et al., 2024, Yuan et al.,
2023]. Recent LLM multi-agent systems study scalable cooperation through role-playing communicative agents and
conversational multi-agent orchestration [Li et al., 2023, Wu et al., 2023, Hong et al., 2024]. In formal mathematics,
agent-based designs further modularize theorem proving into staged interactions with proof assistants [Baba et al.,
2025]. Complementary to these system templates, recent work explicitly targets bottleneck agents and analyzes
component effects via interventions in collaborative LLM systems [Bian et al., 2026, Lyu et al., 2026]. Building
on this diagnostic perspective, we compare matched-interface edits to the Decomposer, Formalizer, and Prover
under identical Lean verifier feedback to identify the most feedback-recoverable stage before allocating test-time
optimization.

GEPA-style prompt optimization. Automatic prompt improvement spans candidate search and selection [Zhou
et al., 2022], iterative optimization of natural-language instructions [Yang et al., 2024], evolutionary prompt up-
dates [Fernando et al., 2024], and trajectory-level reflective revision [Shinn et al., 2023]. GEPA [Agrawal et al.,
2025] further scales reflective evolution to compound systems using trajectory-level textual feedback and Pareto
maintenance over candidates. Closer to autoformalization, ReForm [Chen et al., 2026] studies reflective refinement
under bounded prospective optimization. T O M AP instantiates this family for full-proof pipelines by evolving
Decomposer-side prompts and proof-unit specifications under dense rubric signals, and only commits promising
candidates to frozen Formalizer-Prover execution with Lean verification.

7   Conclusion and Limitation
Full-proof autoformalization connects natural-language mathematical proofs with machine-checkable formal reason-
ing. We study it as a multi-agent LLM system grounded by Lean verification, where decomposition, formalization,
and proof search are handled by specialized agents. Our weak-link analysis identifies the Decomposer as the
most effective interface to optimize under a fixed Formalizer-Prover executor, since faithful, self-contained, and
dependency-aware proof units greatly simplify downstream proof construction. We introduce T O M AP, a GEPA-style
test-time optimizer that evolves proof decompositions. This focuses limited test-time compute on improving the
decomposition rather than repeatedly retrying the full pipeline. Experiments show that T O M AP improves end-to-end
Lean verification and semantic faithfulness on full-proof autoformalization benchmarks.
Limitations remain. Our evaluation is restricted to benchmark-scale proofs rather than long, research-level mathe-
matical proofs. Moreover, we assume that the input informal proofs are correct; extending the system to detect and
repair incorrect or incomplete proof steps is left for future work.




                                                           9
                     Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

References
L. A. Agrawal, S. Tan, D. Soylu, N. Ziems, R. Khare, K. Opsahl-Ong, A. Singhvi, H. Shandilya, M. J. Ryan, M. Jiang,
   et al. Gepa: Reflective prompt evolution can outperform reinforcement learning. arXiv preprint arXiv:2507.19457,
   2025.
Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer, A. Q. Jiang, J. Deng, S. Biderman, and S. Welleck.
  Llemma: An open language model for mathematics. arXiv preprint arXiv:2310.10631, 2023.
K. Baba, C. Liu, S. Kurita, and A. Sannai. Prover agent: An agent-based framework for formal mathematical proofs.
  arXiv preprint arXiv:2506.19923, 2025.
H. Bian, C. Zhang, J. Zhang, X. Li, Y. Guo, W. Dong, and Y. Yang. Weak-link optimization for multi-agent reasoning
  and collaboration. arXiv preprint arXiv:2604.15972, 2026.
ByteDance Seed, Y. Zhang, J. Su, Y. Sun, C. Xi, X. Xiao, S. Zheng, A. Zhang, K. Liu, D. Zan, T. Sun, J. Zhu, S. Xin,
  D. Huang, Y. Bai, L. Dong, C. Li, J. Chen, H. Zhou, Y. Huang, G. Ning, X. Song, J. Chen, S. Liu, K. Shen, L. Xiang,
  and Y. Wu. Seed-Coder: Let the code model curate data for itself. arXiv preprint arXiv:2506.03524, 2025.
R. Cabral, T. M. Do, X. Yu, W. M. Tai, Z. Feng, and X. Shen. Proofflow: A dependency graph approach to faithful
  proof autoformalization. arXiv preprint arXiv:2510.15981, 2025.
G. Chen, W. Jing, X. Chen, X. Zhao, R. Song, C. Li, K. Fan, D. Liu, and M. Liao. Reform: Reflective autoformalization
  with prospective bounded sequence optimization. International Conference on Learning Representations, 2026.
J. Chen, W. Chen, J. Du, J. Hu, Z. Jiang, A. Jie, X. Jin, X. Jin, C. Li, W. Shi, et al. Seed-prover 1.5: Mastering
   undergraduate-level theorem proving via learning from experience. arXiv preprint arXiv:2512.17260, 2025.
J. Dekoninck, I. Petrov, K. Minchev, M. Balunovic, M. Vechev, M. Marinov, M. Drencheva, L. Konova, M. Shumanov,
   K. Tsvetkov, et al. The open proof corpus: A large-scale study of llm-generated mathematical proofs. arXiv preprint
   arXiv:2506.21621, 2025.
K. Dong, A. Mahankali, and T. Ma. Formal theorem proving by rewarding llms to decompose proofs hierarchically.
  arXiv preprint arXiv:2411.01829, 2024.
C. Fernando, D. S. Banarse, H. Michalewski, S. Osindero, and T. Rocktäschel. Promptbreeder: Self-referential
  self-improvement via prompt evolution. In R. Salakhutdinov, Z. Kolter, K. Heller, A. Weller, N. Oliver, J. Scarlett,
  and F. Berkenkamp, editors, Proceedings of the 41st International Conference on Machine Learning, volume 235 of
  Proceedings of Machine Learning Research, pages 13481–13544. PMLR, 21–27 Jul 2024.
S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran,
   L. Xiao, C. Wu, and J. Schmidhuber. MetaGPT: Meta programming for a multi-agent collaborative framework. In
   The Twelfth International Conference on Learning Representations, 2024.
P. Jana, K. Kale, A. E. Tanriverdi, C. Song, S. Vishwanath, and V. Ganesh. Proofbridge: Auto-formalization of natural
   language proofs in lean via joint embeddings. In The Fourteenth International Conference on Learning Representations,
   2026.
A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample. Draft, sketch, and prove:
  Guiding formal theorem provers with informal proofs. arXiv preprint arXiv:2210.12283, 2022.
A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag,
  T. Gutman-Solo, et al. Solving quantitative reasoning problems with language models. Advances in neural
  information processing systems, 2022.
G. Li, H. A. A. K. Hammoud, H. Itani, D. Khizbullin, and B. Ghanem. Camel: Communicative agents for "mind"
  exploration of large language model society. In Thirty-seventh Conference on Neural Information Processing Systems,
  2023.
Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang, Y. Geng, J. Ge, J. Sun, et al. Goedel-prover-v2: Scaling
   formal theorem proving with scaffolded data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.
T.-S. Liu, X.-H. Liu, R. Chen, L. Jin, P. Wang, Z. Zhang, and Y. Yu. Semantic temporal abstraction via vision-
   language model guidance for efficient reinforcement learning. In The Thirteenth International Conference on Learning
  Representations, 2025.


                                                           10
                     Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

T.-S. Liu, C. Jia, H. Liu, P. Wang, S. Zhang, J. Fu, and Y. Yu. Clipping low-probability tokens in SFT yields a
   generalizable initialization for RL. In Forty-third International Conference on Machine Learning, 2026.
Z. Lyu, Z. Ji, S. Chen, L. Wang, Y. Huang, S. Wang, and S.-C. Cheung. Cam: A causality-based analysis framework
  for multi-agent code generation systems. arXiv preprint arXiv:2602.02138, 2026.
OpenAI, J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman,
 S. Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2024.
Qwen, A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, H. Lin, J. Yang, et al.
 Qwen2.5 technical report. arXiv preprint arXiv:2412.15115, 2025.
Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, et al. Deepseek-prover-v2:
  Advancing formal mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
  arXiv:2504.21801, 2025.
N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao. Reflexion: Language agents with verbal reinforcement
  learning. In Proceedings of the 37th International Conference on Neural Information Processing Systems (NeurIPS), 2023.
G. Team, R. Anil, S. Borgeaud, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, et al.
  Gemini: a family of highly capable multimodal models. arXiv preprint arXiv:2312.11805, 2023.
H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying, Z. Zhu, et al. Kimina-prover
  preview: Towards large formal reasoning models with reinforcement learning. arXiv preprint arXiv:2504.11354,
  2025.
P.-Y. Wang, T.-S. Liu, C. Wang, Z. Li, Y. Wang, S. Yan, C. Jia, X.-H. Liu, X. Chen, J. Xu, and Y. Yu. A survey on large
   language models for mathematical reasoning. ACM Comput. Surv., 2026a.
Z. Wang, W. Ma, Z. Ming, G. Zhang, K. Yuan, and Z. Wen. M2f: Automated formalization of mathematical literature
  at scale. arXiv preprint arXiv:2602.17016, 2026b.
Q. Wu, G. Bansal, J. Zhang, Y. Wu, S. Zhang, E. Zhu, B. Li, L. Jiang, X. Zhang, and C. Wang. Autogen: Enabling
  next-gen llm applications via multi-agent conversation framework. arXiv preprint arXiv:2308.08155, 2023.
Y. Wu, A. Q. Jiang, N. Baek, et al. Autoformalization with large language models. In Advances in Neural Information
   Processing Systems, 2022.
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al. Qwen3 technical report.
  arXiv preprint arXiv:2505.09388, 2025.
C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, and X. Chen. Large language models as optimizers. In The Twelfth
  International Conference on Learning Representations, 2024.
L. Yuan, Z. Zhang, L. Li, C. Guan, and Y. Yu. A survey of progress on cooperative multi-agent reinforcement learning
   in open environment. arXiv preprint arXiv:2312.01058, 2023.
L. Zhang, M. Valentino, and A. Freitas. Monotonic reference-free refinement for autoformalization. arXiv preprint
  arXiv:2601.23166, 2026.
Z. Zhang, R. Chen, J. Ye, Y. Sun, P. Wang, J. Pang, K. Li, T. Liu, H. Lin, Y. Yu, et al. Whale: Towards generalizable and
  scalable world models for embodied decision-making. arXiv preprint arXiv:2411.05619, 2024.
K. Zheng, J. M. Han, and S. Polu. Minif2f: a cross-system benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021.
Y. Zhou, A. I. Muresanu, Z. Han, K. Paster, S. Pitis, H. Chan, and J. Ba. Large language models are human-level
   prompt engineers. In The eleventh international conference on learning representations, 2022.




                                                           11
                      Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

A     Prompt
This section presents the prompts used by the agents in T O M AP, including the decomposer for natural-language
problem decomposition A.1, the formalizer for translating natural-language subclaims into Lean statements A.2,
the prover for generating Lean proofs that complete Lean statements A.3, the GEPA judge for evaluating natural-
language decompositions A.4, and the GEPA rewriter for revising natural-language decompositions A.5. It also
describes the semantic evaluation criteria used in the evaluation process A.6.

A.1   Decomposer

    Decomposer

    You are an expert at analyzing mathematical proofs and creating structured proof chains for Lean4
    formalization. Given a natural language theorem and proof, your task is to generate a structured proof chain
    in JSON format that exactly represents the logical structure of the proof.
    —
    ### Key Requirements for Lean-Friendly Formalization
    1. **Contextual Text Extraction**
        * The `"natural_language"` field must contain an **exact quote** from the proof text justifying the
    lemma’s inference.
        * The `"statement"` field should be **self-contained** and **explicit** — repeat necessary assumptions
    from earlier steps, and reference them clearly using their IDs.
    2. **Step-by-Step Granularity (CRITICAL: Maximize Prover Success Rate)**
        * **Decompose the proof into VERY small, atomic steps**. Each logical inference must be a **separate
    lemma**.
        * **PRIORITY: Break down complex steps into simpler sub-steps** that can each be proven with basic
    tactics (simp, ring, linarith, exact).
        * If a step requires multiple reasoning steps, **split it into multiple lemmas** even if they seem trivial. It’s
    better to have more, simpler lemmas than fewer, complex ones.
        * **When in doubt, decompose further**: A lemma that might be provable with `simp` or `ring` alone is
    much more likely to succeed than one requiring complex reasoning.
        * Only merge steps when they can be computed with a **single simple tactic** (like `simp`, `ring`, or
    `linarith`).
    3. **Formalization Using Lean’s Tactics (PRIORITIZE SIMPLE TACTICS)**
        * For each lemma, you must include a **Lean hint** (`lean_hint`), suggesting appropriate tactics or
    actions.
        * **TACTIC PRIORITY ORDER (use the simplest possible tactic)**:

          **TIER 1 (PREFERRED - Highest success rate):**
          * `simp` - For basic simplifications
          * `ring` - For ring/field arithmetic
          * `linarith` - For linear arithmetic
          * `exact` - When the goal matches an assumption exactly
          * `norm_num` - For numerical computations

          **TIER 2 (Use when Tier 1 is insufficient):**
          * `rw` - For rewriting with equalities
          * `apply` - For applying theorems
          * `use` - For existential goals

          **TIER 3 (Avoid if possible - Lower success rate):**
          * `by_cases` - Case analysis (split into separate lemmas instead)
          * `cases` - Pattern matching (split into separate lemmas instead)
          * `by_contra` - Proof by contradiction (split into separate lemmas instead)
          * `induction` - Induction (split into separate lemmas instead)




                                                            12
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

    * **CRITICAL RULE**: If a lemma requires tactics from Tier 2 or 3, consider splitting it into multiple
simpler lemmas that can each use Tier 1 tactics.
    * **For algebraic manipulations**: Prefer `ring` or `simp` over `ring_nf` or complex `rw` chains.
    * **For direct applications**: Prefer `exact` over `apply` when possible.
4. **Managing Dependencies**
    The "statement" field restates all required assumptions explicitly, so each lemma is self-contained and can
be understood by Lean without relying on hidden context.
5. **Lean-Friendly Statement Format**
    * For **each lemma**:
       * **Start with assumptions**: Explicitly restate all prior lemmas or assumptions.
       * **State the conclusion**: Clearly state what the lemma establishes.
    * **Example format**:
       ```json
       {
          "id": "lk",
          "natural_language": "[exact text from proof]",
          "statement": "We assume:\\n• [all dependencies with IDs]\\nTherefore, we conclude:\\n• [the new
fact] [lk]",
          "dependencies": ["tc_1", "def_1"],
          "lean_hint": "[brief tactic]"
       }
       ```
    * **For definitions** (`def_k`), provide a simple statement format:
       ```json
       {
          "id": "def_k",
          "natural_language": "[exact definition from proof]",
          "statement": "Definition:\\n• [definition content] [def_k]",
          "dependencies": ["tc_1"]
       }
       ```
6. **No Error Correction**
    * **Do not introduce new logical steps** that are not explicitly present in the natural language proof. If a
proof is incomplete or incorrect, **represent it exactly as it is written**.
### Node Types
There are **four node types** in the structured proof chain:
1. **Theorem Condition (`tc_k`)** — Assumptions and given conditions, **only formalized** (no proving).
2. **Theorem Solution (`ts_k`)** — The final conclusion of the proof, **requires formalization and proof**.
3. **Definition (`def_k`)** — Definitions, assumptions, and auxiliary results that are not part of the proof but
needed for formalization.
4. **Lemma (`lk`)** — Intermediate proof steps that require formalization and Lean tactics.
### Formalization Guidelines for Lemmas (Maximize Prover Success)
**What to Capture:**
* Each **atomic logical inference** must be captured as a **separate lemma**.
* **Decompose aggressively**: If a step involves multiple operations (e.g., substitution + simplification +
equality), split it into separate lemmas for each operation.
* For each lemma:
   * Restate **all assumptions** (dependencies) explicitly, even if they are already known.
   * Express **the conclusion** of the lemma in mathematical terms.
   * **Lean Hint**: **ALWAYS prefer the simplest possible tactic** from Tier 1 (simp, ring, linarith, exact,
norm_num).
   * **If you cannot suggest a Tier 1 tactic, the lemma is likely too complex** - consider splitting it further.
   * **Provide detailed hints**: The `lean_hint` should include:



                                                      13
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

      - The specific tactic to use (e.g., `ring`, `simp`, `linarith`)
      - Key intermediate steps if needed (e.g., "First use `rw` to substitute, then `simp`")
      - Important lemmas or facts to reference (e.g., "Use `add_comm` and `add_assoc`")
      - Any algebraic identities or simplifications needed
      - **For complex lemmas**: Break down the proof strategy into clear steps (e.g., "1. Use `rw` with
dependency [l5], 2. Apply `ring` to simplify, 3. Use `linarith` to conclude")
**Examples of Good Decomposition:**
* **Bad**: One lemma that says "Substitute x = a+b into f(x) and simplify to get f(a+b) = g(a,b)"
   * **Good**:
      - Lemma 1: "If x = a+b, then f(x) = f(a+b)" (hint: `rw [h_x_eq]` where `h_x_eq` is the assumption)
      - Lemma 2: "f(a+b) = g(a,b)" (hint: `simp [f_def]` or `ring` to simplify the expression)
* **Bad**: One lemma that says "By case analysis, either P or not P, and in both cases we get Q"
   * **Good**:
      - Lemma 1: "If P, then Q" (hint: `exact h_P_implies_Q` or `simp [h_P]`)
      - Lemma 2: "If not P, then Q" (hint: `exact h_notP_implies_Q` or `simp [h_notP]`)
      - Lemma 3: "Q" (hint: `by_cases h : P; [exact Lemma1 h, exact Lemma2 h]`)
* **Bad**: One lemma that says "From W + Y = X + Z, we get X - W = Z - Y"
   * **Good**:
      - Lemma 1: "W + Y = X + Z implies W + Y - X - Z = 0" (hint: `linarith [h_eq]` where `h_eq : W + Y = X +
Z`)
      - Lemma 2: "W + Y - X - Z = 0 implies (W - X) + (Y - Z) = 0" (hint: `ring` to rearrange)
      - Lemma 3: "(W - X) + (Y - Z) = 0 implies W - X = -(Y - Z)" (hint: `linarith`)
      - Lemma 4: "W - X = -(Y - Z) implies X - W = Y - Z" (hint: `linarith` to negate both sides)
**What **Not** to Capture:**
* **Introductions**: Do not include introductions like "Let ( x \in A )" or "Fix ( \epsilon > 0 )".
* **Meta-comments**: Avoid phrases like "It suffices to show..." or "We proceed by induction".
—
### Output Format
The output should be in **JSON format** and should follow the exact structure below. Ensure to follow this
structure **without any unrelated content**.
Note that backslashes (\) must be written as double backslashes (\\) in JSON strings.
```json
[
   {
      "id": "tc_1",
      "natural_language": "[exact text from theorem statement]",
      "statement": "Premise:\\n• [mathematical content] [tc_1]",
      "dependencies": []
   },
   {
      "id": "def_1",
      "natural_language": "[exact definition from proof]",
      "statement": "Definition:\\n• [definition content] [def_1]",
      "dependencies": ["tc_1"]
   },
   {
      "id": "l1",
      "natural_language": "[exact text from proof]",
      "statement": "We assume:\\n• [restated content with IDs]\\nTherefore, we conclude:\\n• [new fact]
[l1]",
      "dependencies": ["tc_1", "def_1"],
      "lean_hint": "[brief tactic plan]"
   },
   {
      "id": "ts_1",



                                                     14
                  Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

     "natural_language": "[final text]",
     "statement": "We assume:\\n• [all dependencies with IDs]\\nTherefore, we conclude:\\n• [theorem
solution] [ts_1]",
     "dependencies": ["tc_1","l1", "def_1"],
     "lean_hint": "[brief tactic plan]"
   }
]
```
### The `statement` field (mandatory style)
* The **exact format** for lemmas and theorem solutions:
   ```text
   We assume:
   • [actual content of tc_1] [tc_1];
   • [actual content of tc_2] [tc_2];
   • [actual content of l1] [l1];
   Therefore, we conclude:
   • [actual content of l2] [l2].
   ```
* For **theorem conditions**:
   ```text
   Premise:
   • [actual content of tc_1] [tc_1];
   ```
* For **definitions**:
   ```text
   Definition:
   • [actual content of def_1] [def_1];
   ```
—
### Quick Checklist (Prioritize Prover Success)
* **Be clear and complete**: Each step should include all necessary information (variables, assumptions, etc.),
so Lean can follow it easily.
* **Keep it VERY simple**: Break the proof into **as many small steps as possible**. Prefer many simple
lemmas over fewer complex ones.
* **Maximize Tier 1 tactics**: Each lemma should ideally be provable with `simp`, `ring`, `linarith`, `exact`,
or `norm_num`.
* **Decompose complex steps**: If a step involves substitution, simplification, and conclusion, split it into
separate lemmas.
* **Avoid complex reasoning**: If a lemma requires case analysis, contradiction, or induction, consider
splitting it into multiple simpler lemmas.
* **Stay true to the original**: Follow the author’s reasoning exactly—don’t change the logic, and don’t add
new concepts or ideas.
* **Reflect the proof as written**: Even if the proof has gaps or mistakes, represent it faithfully in Lean.
* **Test your hints**: If you suggest a tactic from Tier 2 or 3, ask yourself: "Can I split this into simpler lemmas
that use Tier 1 tactics?"
## Your Task
Now, please generate the proof decomposition for the following theorem and proof:
**Theorem:** { nl_theorem }
**Proof:** { nl_proof }




                                                        15
                   Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

A.2   Formalizer

  Formalizer
  You are a **thinking model** specialized in turning natural-language math statements into **Lean 4** code.
  You will receive:
  1. A lemma name (`lemma_header`, e.g. `lemma l3`),
  2. A natural-language statement for this proof step,
  3. Name of dependencies
  4. A Lean code skeleton with placeholders
  5. **full Lean 4 code of prior steps** (“dependencies”)
  Your job is to **emit exactly one Lean 4 code block** that compiles after replacing placeholders, while **not
  reproducing any prior lemmas/defs**. Treat prior steps only as hypotheses (see “Using Dependencies”).
  —
  ## Hard Rules (highest priority)
  **0. Single lemma only (no extras)**
  * Output must contain **exactly one lemma/theorem definition** (the `lemma_header`).
  * The fenced block must contain **exactly one** of: `lemma ` *or* `theorem `.
  * The block must contain **exactly one** occurrence of `:= by` and of `sorry`.
  1. **Provide one fenced Lean block**
     * /think /think Please think carefully before giving the final answer.
     * At the end, write **exactly one** fenced block: start with `lean4 and end with `.
  2. **Header is fixed** (keep exactly this header in this order):
  ```lean4
  import Mathlib
  import Aesop
  set_option maxHeartbeats 0
  open BigOperators Real Nat Topology Rat Filter
  ```
  3. **Proof body format**
      * The proof body must be **exactly** `:= by\nsorry`.
  4. **Lemma name unchanged**
      * Keep the `lemma_header` name and structure exactly; only fill in parameters/hypotheses and the goal.
  5. **Prohibited content inside the block**: additional `lemma`, `theorem`, `def`, `example`, `instance`,
  `axiom`, `structure`, or extra `import`/`set_option`/`open` sections beyond the single required header.
  —
  ## Using Dependencies
  Often you are given the **full Lean code** of earlier steps (“dependencies”).
  These prior lemmas contain **relevant Lean 4 information** that you may use when formalizing the current
  step, including:
  * **Type declarations** (e.g., `{n : N}`, `(A B : Set α)`, `(x : α)`, etc.)
  * **Formalized statements (goals) of the previous lemmas** — i.e., their proposition types
  * Any **constants and structures** appearing in those lemmas
  **What you must do with dependencies:**
  1. **Include every dependency as a named hypothesis** in the current lemma.
      * Use the **dependency lemma’s name** as the hypothesis name.
      * Its hypothesis type is the **proposition type of that prior lemma**, adapted to match the variables in the
  current lemma.
      * Include all dependencies as hypotheses even if you think they are not relevant or will be used.
  2. **Not mandatory to reproduce dependency code verbatim.** You are given prior code for *reference only*.
      * If needed, **adapt** the dependency statements to properly fit the current lemma’s parameters and
  context.


                                                        16
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

    * Instantiate with the current variables when possible, or generalize with ∀ if necessary.
    * Minor modifications (e.g., renaming variables, adapting types) are OK if needed for consistency.
3. **Preferred**: If the current lemma declares matching variables (same names/types), **instantiate** the
dependency with those variables (no ∀).
       * Example: prior `lemma l1 (a b : R) : a + b = b + a`, then you add `(l1 : a + b = b + a)` after declaring
`(a b : R)`.
4. **Extra hypotheses are allowed**
You may add new hypothesis, such astype/variable declarations (e.g., {α : Type*}, (n : N), (x : R)) if they are
needed to make the current lemma well-formed. These are in addition to the dependencies. Always place
them before dependency hypotheses in the parameter list.
5. **Do not duplicate** a dependency that you’ve already added.
6. If no dependencies are provided, skip this section and proceed normally.
—
## Parameter/Hypothesis Ordering (skeleton has none → write from scratch)
When you fill the skeleton parameters, **place items in this order**:
1. **Type/implicit parameters first** (e.g., `{n : N}`, `{α : Type*}`)
2. **Explicit variable declarations next** (e.g., `(A B : Set α) (x : α) (a b : R)`)
3. **Dependency hypotheses** (one per prior lemma, named by lemma name; adapted as needed)
Then place a colon `:` and the **formalized goal statement**, followed by `:= by\nsorry`.
—
## Goal Formalization
* Replace `[place correct hypothesis here]` and `[place goal here]` with the **precise Lean proposition**
matching the natural-language statement.
* The goal is to replicate the logic in the natural language statement in Lean4, so please preserve the meaning
of the natural language proof.
* Use standard Lean 4 / Mathlib 4 syntax.
—
## lean friendly formalization rules
The goal of a formalization LLM is to **choose the library’s preferred/canonical formulation** and reduce
proof glue, rather than to “translate literally.”
1. Prefer the “canonical API” (Pick the canonical API)
**Guideline**: If Mathlib has a canonical API for the same mathematical concept, use it.
**Examples**:
* “finite support” → `Finsupp.support`
* “prime divisors” → `Nat.primeFactors` / `support_factorization`
* “valuation” → `padicValNat` or `factorization` (pick one; don’t mix)
2. Encode boundary conditions into types when possible (Encode invariants in types)
**Guideline**: Use stronger types when available (`N+`, `Subsemiring`, `Units`, `Subtype`) to reduce
repeated hypotheses like `x ̸= 0`, `x ∈ S`, etc.
**Examples**: positive integers use `N+`; nonzero elements use `α× ` or `Subtype (· ̸= 0)`.
3. Avoid mixing representations: stay within one layer (One representation per theorem)
**Guideline**: Try to keep a statement within a single “world”:
* use only `Finsupp.prod` or only `Finset.prod`
* use only `Set` or only `Finset`
If you must cross worlds, it’s usually best to split into two theorems: a bridging lemma and a main lemma.
4. Align equation direction with library lemmas (Align direction with lemmas)
**Guideline**: If the library usually states a lemma as `lhs = rhs`, write your statement in that direction to
avoid scattering `.symm`.
(Direction doesn’t change the math, but it affects proof friction.)
5. Separate explicit constructions from the main statement (Two-tier theorem strategy)




                                                       17
                  Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

**Guideline**: By default, output an existence/property theorem; put an explicit witness either in a separate
theorem or inside the proof via `let`.
Applies to: situations involving complicated `∏/∑` expansions, reindexing, or casts.
6. Expected handling of Classical/DecidableEq
**Guideline**: If the statement involves `Finset`, `support`, `toFinset`, `choose`, `filter`, etc., default to
adding `by classical` in the proof skeleton; don’t force `classical` into the statement itself.
7. Make “obviously finite/nonempty” explicit via concrete structures
**Guideline**:
* “finite” → use `Finset` or `Fintype`
* “nonempty” → use `s.Nonempty` or `∃ x, x ∈ s`
* “only finitely many terms are nonzero” → use `Finsupp` or `Summable`/`HasSum` (in analysis)
## Skeleton You Must Fill
You will be given content like:
"""
Please autoformalize the following natural language problem proof step in Lean 4.
Use the following lemma name: {lemma\_header}
The natural language statement is: {statement}
The dependencies are: {dependencies}
This is the lean code skeleton you need to use:
```lean4
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat Filter
{lemma_header}
[place correct hypothesis here] :
[place goal here] := by
sorry
```
"""
The natural language statement has this format: We assume that \[desciption of lemma l1] \[l1], that
\[description of lemma l2] \[l2], ... . From the previous assumptions, we conclude that \[description of ts\_1]
\[ts\_1]. The lemma names are provided in square brackets. In the previous example these are "tc1" and "l1",
and "ts\_1" is the name of the current lemma.
Your output must **replace** `[place correct hypothesis here]` with the ordered parameter/hypothesis list
(types first, then variables, then dependencies) and replace `[place goal here]` with the formalized goal.
If additional previous context is provided (full Lean code of earlier steps), **use it** to extract relevant **type
declarations** and **dependency proposition types**, and **include each dependency** as a named
hypothesis. Add extra hypothesis if needed.
**The final fenced block must consist of the header, then exactly one `lemma_header` definition, and nothing
else.**
—
## Few-Shot Examples
### ✓ Example 1 — Absolute Value (preserve given hypotheses; demonstrate ordering)
**Input**:
* Lemma Name: `ts_1`
* Natural Language Statement: "Assuming a ≥ 0 and b ≤ 0 [tc_1] and bs (a + b) = abs a + abs b [l1], we can
conclude that |a + b| ≤ |a| + |b| [ts_1]."
* Dependencies: ["tc_1", "l1"]
* Lean4 code of tc_1 and lemma l1 [ommited here]
**Correct Output**:
```lean4


                                                        18
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat Filter
lemma ts_1 /- lemma name should be ts_1-/
   (a b : R)
   (tc_1 : (a ≥ 0 ∧ b ≤ 0))
   (l1 : abs (a + b) = abs a + abs b):
   |a + b| ≤ |a| + |b| := by
sorry
````
### ✗ Wrong Example — Replacing Given Hypotheses (don’t do this)
```lean4
lemma result
   (a b : R)
   (h1 : (a ≥ 0 ∧ b ≤ 0))
   (h2 : abs (a + b) = abs a + abs b):
   |a + b| ≤ |a| + |b| := by
sorry
```
*Why wrong: it replaces the original hypothesis names/statements (h1 and h2) the lemma name.*
### ✓ Example 2 — Add Missing Variable Types
**Input**:
* Lemma Name: `l3`
* Natural Language Statement: "Assuming 2 * d = 6 [l2], we can conclude that |a + b| ≤ |a| + |b| [l3]".
* Dependencies: ["l2"]
* Lean4 code of lemma l2 [ommited here]
**Correct Output**:
```lean4
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat Filter
lemma l3
   (d : R)
   (l2 : 2 * d = 6) :
   d = 3 := by
sorry
```
**Why this is correct**: Added missing variable `(d : R)`.
### ✓ Example 3 — Matrices with Dependencies
**Input**:
   * Lemma Name: `l4`
   * Natural Language Statement: Assuming det (A * B) = det I [l1], det I = 1 [l2], det (A * B) = det A * det B
and [l3], we can conclude that $\\det(A) \\cdot \\det(B) = 1$ [l4].
   * Dependencies: ["l1", "l2", "l3", "l4"]
   * Lean4 code of lemmas l1, l2, l3 and l4 [ommited here]
**Correct Output**:
```lean4
import Mathlib
import Aesop
set_option maxHeartbeats 0



                                                       19
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

open BigOperators Real Nat Topology Rat Filter
lemma l4
    {n : N} (A B I : Matrix (Fin n) (Fin n) R)
    (l1 : det (A * B) = det I)
    (l2 : det I = 1)
    (l3 : det (A * B) = det A * det B) :
    det A * det B = 1 := by
sorry
```
*(**Rationale**: The LLM correctly identified all the variables (`n`, `A`, `B`, and `I`) that appear across the
target statement and all three dependencies. It declared their types, placing the implicit argument `{n : N}`
first, and then formalized the goal, using the probided lean4 code of the dependencies.)*
—
## Final Compliance Checklist
* [ ] **Ordering**: types → explicit variables → dependency hypotheses
* [ ] All provided dependencies included as **named hypotheses**
* [ ] Goal precisely formalized from the natural language statement
* [ ] **Exactly one lemma/theorem** in the block (no other
`lemma`/`theorem`/`def`/`example`/`instance`)
* [ ] **Exactly one** `:= by` and **exactly one** `sorry`
* [ ] Extra hypotheses (e.g., type or variable declarations) are permitted when needed to make the lemma
well-formed, but must appear before dependency hypotheses.
* [ ] Only use unqualified names from namespaces that are explicitly opened (BigOperators Real Nat Topology
Rat Filter); for every other namespace, always write fully qualified names (e.g. Set.union, Function.injective,
etc)

Please autoformalize the following natural language problem proof step in Lean 4.
The natural language statement is: {item.statement}
The dependencies are: {dependencies}
**IMPORTANT: Do NOT include import statements or header in your output!**
The following header will be automatically added by the system:
```
{LEAN_HEADER}
```
You should ONLY output the lemma/theorem body. Use this skeleton:
```lean4
[place correct hypothesis here] :
[place goal here] := by
sorry
```
Important: 1 **Please write only one lemma or theorem**!!
2 **All variable declarations must be on a SINGLE line, or each must start with the ’variable’ keyword.**
3 **Function calls need a space before ’(’: write ’cos (x)’ not ’cos(x)’**
4 **The formalized code you generate must be faithful to the natural language semantics, ensuring that every
condition of the natural language meaning is captured. **
5 Be sure to preserve the original meaning of the natural language. It is **not required** that the generated
Lean code can be proved, because the natural-language theorem may be unprovable.




                                                      20
                   Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

A.3   Prover

  Prover
  You are an expert Lean 4 theorem prover.
  Your job is to complete partially written Lean 4 code and provide correct, verifiable proofs.
  When given a lemma/theorem and its partial Lean code, you should:
  - Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan
  outlining the main proof steps and strategies.
  - The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the
  construction of the final formal proof.
  - You may add trivial hypotheses (e.g. type declarations) if necessary.
  - Never remove or rename existing hypotheses; only adapt them in minor ways that preserve meaning.
  **leanproof tips:**
  1. Avoid proving “glue goals”: if you hit goals like False or _ ̸= 0 just to feed later steps, prefer changing the
  quantification domain or using by_cases instead of hand-deriving facts from membership in support.
  2. rw matches shapes, not meanings: when rewriting fails, check for representation mismatches (e.g.,
  Finset.prod vs Finsupp.prod) and first align forms via simpa [definition-expansions] using lemma.
  3. Fix direction with symm first: if you proved the reverse equality, use symm/.symm immediately rather
  than trying to flip it through rw/simp.
  - Respond only with Lean 4 code inside a fenced block starting with ```lean4 and ending with ```.
  - Make sure there is no “sorry” on the Lean code.

  This is the lemma/theorem I want you to prove:
  {item.statement}
  {optional_lean_hint_section}Complete the following Lean 4 code (**do not remove imports**):
  ```lean4
  {item.formalization["lean_code"]}
  ```
  CRITICAL: You MUST respond with a code block in this exact format:
  ```lean4
  [Your complete Lean 4 proof code here]
  ```
  Important rules:
  1. **Function calls need a space before ’(’: write ’cos (x)’ not ’cos(x)’**
  2. Replace ’sorry’ with actual proof code.
  3. Your response MUST include the ```lean4 code block - this is mandatory.
  ``````


A.4   GEPA Judge

  GEPA Judge

  Your job is not to run Lean. Decide whether the current proof-graph script is already good enough to enter the
  actual Lean formalize/prove flow, or whether another statement-level self-reflection rewrite is worth
  spending one GEPA optimization round.
  ### Stage
  {stage}
  ### Remaining GEPA optimization rounds
  {budget_remaining}
  ### Original theorem
  {nl_theorem}
  ### Original proof
  {nl_proof}



                                                          21
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

### Target node ids
{json.dumps(sorted(target_node_ids), ensure_ascii=False)}
### Current proof graph nodes
```json
{json.dumps(graph_payload, ensure_ascii=False, indent=2)}
```
{lean_feedback_section}
### Criteria
1. Evaluate only target nodes. Locked nodes are context only.
2. Score every target node against three criteria. Each criterion is worth 1 point, so each node has a maximum
score of 3. In `reason`, give the concrete deduction reasons; if the node gets full marks, the reason may be
brief.
2.1 Faithfulness to the original proof: the node statement should preserve the semantics of the corresponding
step in the original proof.
2.2 Strict independent provability of each node: a node may omit necessary conditions from the Original
proof, such as `k > 0` or basic constraints like `a` is an integer. Such omissions can make the proposition
unprovable.
2.3 Lean friendliness. Check the following requirements:
2.3.1. Relevant-domain Quantification
**Problem:** Mathematics often says “for all (x)” even though the argument only needs *relevant* (x), such as
nonzero terms, actually occurring terms, or points where a function is defined.
**Guideline:** By default, quantify over a clearly specified relevant set or predicate, and make that set or
predicate explicit.
**NL templates:**
* “For every (x) in the set (S), . . . ”
* “For every (x) such that (P(x)), . . . ”
**Typical triggers:** *all, any, every, for all*.
**Benefit:** Reduces Lean work where one must repeatedly prove side conditions like `P(x)` just to apply
hypotheses.
2.3.2. Make Domain/Boundary Conditions Explicit
**Problem:** Mathematical text often implicitly assumes conditions like nonzero, positive, denominator
nonzero, or nonempty set.
**Guideline:** Each node should explicitly state the needed side conditions: nonzero, positivity, nonemptiness,
invertibility, denominator (\neq 0), function domain assumptions, etc. You need to use the original full
natural-language proof to fill in the domains/ranges and conditions for each variable in this node’s
natural-language statement.
**NL templates:**
* “Assume (x \neq 0).”
* “Assume (S) is finite / nonempty.”
* “Assume (f) is defined on . . . and is continuous on . . . ”
2.3.3. Interface Stabilization (Fix the Chosen Notation/API Early)
**Problem:** The same concept can have multiple library interfaces, such as valuation/factorization/count,
norm/abs, or limit/filter.
**Guideline:** Early in the graph, explicitly declare which interface/definition is being used, and stick to it
consistently throughout downstream nodes.
**NL templates:**
* “Let (v_p(n)) denote . . . ”
* “Let (\lvert x\rvert) denote the norm . . . ”
* “Let (\lim) be taken with respect to the filter . . . ”
2.3.4. Equivalence vs. One-way Implication Annotation
**Problem:** Mathematical rewrites are often treated as equivalences, but in Lean the direction matters for
which lemmas can be applied.




                                                      22
                   Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

  **Guideline:** Every rewrite node should explicitly label whether it is an equivalence (“equivalent to”) or a
  one-way implication (“implies”).
  **NL templates:**
  * “This is equivalent to . . . ”
  * “This implies . . . ”
  2.3.5. Type/Cast Awareness
  **Problem:** Implicit coercions between (\mathbb{N}/\mathbb{Z}/\mathbb{Q}/\mathbb{R}) are a major
  source of friction in Lean.
  **Guideline:** The graph output should state which number system each object lives in, and when/where
  coercions or embeddings are intended.
  **NL template:**
  * “View (n) as an integer/real via the canonical embedding.”
  3. Combining the remaining GEPA optimization rounds and the quality of the target statements, decide
  whether to enter the actual Lean formalize/prove flow. The goal is that all nodes can pass the Lean flow. Set
  `ready_for_lean` to true when the current script is good enough to proceed.
  ### Example Output Format (content should follow the actual analysis)
  Return one JSON object:
  ```json
  {
      "target_node_scores": [
          {
              "node_id": "l1",
              "reason": "Concrete deduction reasons; brief if this node receives full marks.",
              "score": 3
          }
      ],
      "decision_reason": "Why to proceed to Lean now, or why another self-reflection rewrite is needed.",
      "ready_for_lean": true
  }
  ```

A.5   GEPA Rewriter

  GEPA Rewriter
  You are rewriting proof-decomposition node natural-language statements for Lean formalization.
  ### Stage
  {stage}
  ### Original theorem
  {nl_theorem}
  ### Original proof
  {nl_proof}
  ### Target node ids to rewrite
  {json.dumps(sorted(target_node_ids), ensure_ascii=False)}
  ### Current proof decomposition nodes
  ```json
  {json.dumps(graph_payload, ensure_ascii=False, indent=2)}
  ```
  ### Judge feedback
  ```json
  {json.dumps(judge_feedback, ensure_ascii=False, indent=2)}
  ```
  ### Rewrite rules
  1. Output updates only for target nodes that should change.



                                                       23
                  Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

2. Never output updates for locked nodes.
3. Keep every node id and dependency list unchanged.
4. Preserve the exact mathematical meaning of the original proof step. Do not invent missing proof steps or
repair an incorrect proof by changing its meaning.
5. Make the statement self-contained and Lean-friendly: include necessary assumptions, domains, type
information, nonzero/positivity/boundary conditions, and explicit references to dependency ids when
needed.
6. Keep the same statement style already used in the decomposition: `We assume:` and `Therefore, we
conclude:` for lemmas/theorem statements, `Premise:` for theorem conditions, and `Definition:` for
definitions.
7. Each node has a maximum score of 3 in the Judge feedback. The three scoring criteria are: faithfulness to
the original proof, strict independent provability of each node, and Lean friendliness. Prefer rewriting nodes
with deducted points, and use the Judge reasons to decide what to fix.
### Trick
1. The node’s natural language may omit some necessary conditions from the **original full natural-language
context** (e.g., missing k > 0, or basic constraints like a is an integer). If such conditions are necessary for this
node, you must carefully identify and include them.
2. Enhance the natural-language statement to be more Lean-friendly: make implicit “logical bridges or
cindition” explicit, while staying faithful to the semantics of the original natural-language meaning. For
example:
——
2.1. Relevant-domain Quantification
**Problem:** Mathematics often says “for all (x)” even though the argument only needs *relevant* (x)
(nonzero terms, occurring terms, points where a function is defined, etc.).
**Guideline:** By default, quantify over a clearly specified relevant set or predicate, and make that
set/predicate explicit.
**NL templates:**
* “For every (x) in the set (S), . . . ”
* “For every (x) such that (P(x)), . . . ”
**Typical triggers:** *all, any, every, for all*.
**Benefit:** Reduces Lean “glue” work where you must repeatedly prove side conditions like `P(x)` just to
apply hypotheses.
2.2. Make Domain/Boundary Conditions Explicit
**Problem:** Mathematics often implicitly assumes conditions like “nonzero/positive/denominator
nonzero/nonempty set.”
**Guideline:** Each node should explicitly state the needed side conditions: nonzero, positivity, nonemptiness,
invertibility, denominator (\neq 0), function domain assumptions, etc. **You need to use the original full
natural-language proof to fill in the domains/ranges and conditions for each variable in this node’s
natural-language statement!!!!**
**NL templates:**
* “Assume (x \neq 0).”
* “Assume (S) is finite / nonempty.”
* “Assume (f) is defined on . . . and is continuous on . . . ”
2.3. Interface Stabilization (Fix the Chosen Notation/API Early)
**Problem:** The same concept can have multiple library interfaces (e.g., valuation/factorization/count;
norm/abs; limit/filter).
**Guideline:** Early in the graph, explicitly declare which interface/definition is being used, and stick to it
consistently throughout downstream nodes.
**NL templates:**
* “Let (v_p(n)) denote . . . ”
* “Let (\lvert x\rvert) denote the norm . . . ”
* “Let (\lim) be taken with respect to the filter . . . ”
2.4. Equivalence vs. One-way Implication Annotation
**Problem:** Mathematical rewrites are often intended as equivalences, but in Lean the *direction* matters for
which lemmas can be applied.



                                                         24
                   Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

  **Guideline:** Every rewrite node should explicitly label whether it is an equivalence (“equivalent to”) or a
  one-way implication (“implies”).
  **NL templates:**
  * “This is equivalent to . . . ”
  * “This implies . . . ”
  2.5. Type/Cast Awareness
  **Problem:** Implicit coercions between (\mathbb{N}/\mathbb{Z}/\mathbb{Q}/\mathbb{R}) are a major
  source of friction in Lean.
  **Guideline:** The graph output should state which number system each object lives in, and when/where
  coercions (embeddings) are intended.
  **NL template:**
  * “View (n) as an integer/real via the canonical embedding.”
  ### Output
  Return one JSON object:
  ```json
  {
      "updates": [
         {
              "node_id": "l1",
              "natural_language": "Replacement natural language for this node.",
              "statement": "Replacement self-contained statement for this node.",
              "lean_hint": "Optional short Lean hint."
         }
      ]
  }
  ```


A.6   Evaluation Criteria

  Evaluation Criteria
  ## Guidelines for Consistency Check
  Core Checking Requirements:
  - When a critique from a previous autoformalization and consistency check result is provided, you must first
  analyze its findings and then assess their problems.
  - Must carefully compare the Natural Language and Lean code through a rigorous and explicit process.
  - Determine if the Lean theorem statement is an exact and faithful formalization of the mathematical problem
  and proof.
  - If any result is Incorrect of consistency, briefly list all inconsistencies and reasons leading to the Incorrect
  determination in comments.
  ## Evaluation Stages (All required):
  1. Math Assertion and Proof Analysis
  Identify all structurally and semantically relevant components of the mathematical problem and proof,
  including variables, types, quantifiers, constraints, logic structure, conclusion, and so on. The analysis should
  be based on the actual content of the text.
  2. Lean Statement Analysis
  Extract all structurally and semantically relevant components from the Lean statement, including variables,
  types, conditions, quantifiers, constraints, the final claim, and so on. The analysis should reflect the actual
  content present in the Lean code.
  3. Comparative Verification
  Check for exact correspondence between the math and Lean statements; you may refer to aspects like:
  - Semantic alignment, proof-step alignment, logic structure, and quantifier correctness.
  - Preservation of constraints and boundary assumptions.
  - Accurate typing and use of variables.
  - Syntactic validity and proper Lean usage (free from errors).



                                                         25
                 Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

- Use of symbols and constructs without semantic drift.
- No missing elements, no unjustified additions, and no automatic corrections or completions.
4. Final Judgement
Based solely on the above analysis, judge whether the Lean statement is a correct and exact formalization of
the mathematical problem and proof.
5. Accuracy Confirmation
If correct: clearly confirm why all elements match.
If incorrect: list all mismatches and explain how each one affects correctness.




                                                     26
                    Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

B   Model Configuration


                                      Table 3: Models used by different methods.
 Method                        Formal Language Model                        Natural Language Model

 Monotonic                     DeepSeek-Prover-V2-7B [Ren et al., 2025]     Seed-Coder-8B [ByteDance Seed et al.,
                               Goedel-Prover-V2-8B [Lin et al., 2025]       2025]
                                                                            Qwen2.5-7B [Qwen et al., 2025]
                                                                            GPT-4.1-mini [OpenAI et al., 2024]

 ProofBridge                   Kimina-Prover-RL-1.7B fine-tuned with        None
                               SFT [Wang et al., 2025]
                               NL encoder initialized from
                               all-MiniLM-L6-v2

 ProofFlow                     Goedel-Formalizer-V2-32B                     Gemini3-Pro [Team et al., 2023]
                               Goedel-Prover-V2-32B

 T O M AP w/ Qwen3-30B-A3B-    Goedel-Formalizer-V2-32B                     Qwen3-30B-A3B-Instruct-2507 [Yang et al.,
 Instruct-2507                 Goedel-Prover-V2-32B                         2025]

 T O M AP w/ Gemini3-Pro       Goedel-Formalizer-V2-32B                     Gemini3-Pro
                               Goedel-Prover-V2-32B



C   Hyperparameter Settings


                                      Table 4: Hyperparameters used in T O M AP.
                                    Hyperparameter                                          Value
                                                        Context length                      32000
                 Decomposer
                                                        Temperature                         0.7
                                                        Context length                      12000
                 Formalizer
                                                        Temperature                         0.7
                                                        Context length                      12000
                 Prover
                                                        Temperature                         0.7
                                                        Context length                      32000
                 GEPA Judge
                                                        Temperature                         0.7
                                                        Context length                      32000
                 GEPA Rewriter
                                                        Temperature                         0.7
                 GEPA_MAX_ITERS                                                             10
                 Gate threshold ϵ                                                           1



D    Decomposition Optimization Examples

This section presents several examples of decomposition optimization, illustrating that optimizing decompositions is
of practical significance for preserving the semantics of the original proof and for subsequently generating correct
Lean code. The optimization specifically includes aspects such as eliminating ambiguity in natural language,
uncovering implicit assumptions, and improving the definitions of variables.


                                                          27
                        Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

D.1   Example 1

Some conventional notations in natural language are ambiguous. For example, (i) is usually understood by default
as the imaginary unit in the complex numbers, whereas in Lean, (i) must be rigorously defined.
Natural language subclaim before optimization.
We assume:

      • x, y ∈ R;
      • z = x + iy.

Therefore, we conclude:

      • (1 + i ) z = ( x − y ) + i ( x + y ) .

Lean subclaim before optimization.
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat Filter

theorem l2 (x y : R) (z : C) (h : z = x + I * y) :
    (1 + I) * z = (x - y) + I * (x + y) := by sorry
Natural language subclaim after optimization.
We assume:

      • x, y ∈ R ;
      • z = x + iy, where i is the standard imaginary unit in C with i2 = −1.

Therefore, we conclude:

      • (1 + i )z = ( x − y) + i ( x + y) as an equality in C.

Lean subclaim after optimization.
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat Filter

theorem l2
    (x y : R)
    (z : C)
    (h1 : z = x + y * Complex.I) :
    (1 + Complex.I) * z = (x - y) + (x + y) * Complex.I := by sorry

D.2   Example 2

The decomposition fails to capture an implicit condition in the original proof: in the original proof, ( a, b) is nonempty,
i.e., a < b, whereas the decomposition imposes no such restriction.
Natural language theorem.


                                                             28
                      Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

Let a, b ∈ Q. Then for any integer n,
                                       # (( a, b) ∩ Z) ≡ # (( a, b + 2n) ∩ Z)   (mod 2)
and
                                      # (( a, b) ∩ Z) ≡ # (( a − 2n, b) ∩ Z)    (mod 2),
provided that each interval involved in the congruence is nonempty.
Natural language proof.
Let ⌈ x ⌉ denote the least integer greater than or equal to x.
Since n > 0,
                                           ( a, b + 2n) = ( a, b) ∪ [b, b + 2n),
where the union is disjoint. There are 2n integers
                                                ⌈b⌉, ⌈b⌉ + 1, . . . , ⌈b⌉ + 2n − 1
in the interval [b, b + 2n), so the first congruence of the lemma is true in this case.
We also have
                                            ( a, b − 2n) = ( a, b) minus [b − 2n, b),
and [b − 2n, b) contains exactly 2n integers, so the lemma is also true when n is negative.
The statement about
                                                      # (( a − 2n, b) ∩ Z)
is proved in a similar manner.
Natural language subclaim before optimization.
We assume:

      • a, b ∈ Q ;
      • n ∈ Z with n > 0.

Therefore, we conclude:

      • ( a, b + 2n) = ( a, b) ∪ [b, b + 2n).

Lean subclaim before optimization.
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat Filter

theorem l1
    (a b : Q) (n : Z) (hn : n > 0)
    (tc_1 : True) :
    Set.Ioo a (b + 2 * n) = Set.Ioo a b ∪ Set.Ico b (b + 2 * n) ∧
    Disjoint (Set.Ioo a b) (Set.Ico b (b + 2 * n)) := by
    sorry
Natural language subclaim after optimization.
We assume:

      • a, b ∈ Q;
      • n ∈ Z;
      • n > 0;


                                                               29
                        Efficient Test-Time Optimization for Multi-Agent Proof Autoformalization

      • a < b as real numbers, since the interval is nonempty.

Therefore, we conclude:

      • As sets of real numbers,
                                                ( a, b + 2n) = ( a, b) ∪ [b, b + 2n)
Lean subclaim after optimization.
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat Filter

theorem l1
    (a b : Q) (n : Z)
    (hn : n > 0) (hab : a < b) :
    (Set.Ioo (a : R) (b + 2 * n : R) =
        Set.Ioo (a : R) (b : R) ∪
        Set.Ico (b : R) (b + 2 * n : R)) := by
    sorry

D.3   Example 3

For the Lean language, each variable should be rigorously defined, for example by specifying which number domain
it belongs to. Such conditions may exist in the natural language, but may not have been captured in the initial version
of a given subclaim.
Natural language subclaim before optimization.
We assume:

      • B = 30 ;
      • h = 6.5 .

Therefore, we conclude:
          1
      •     Bh = 65 .
          3
Natural language subclaim after optimization.
We assume:

      • Let B, h ∈ R;
      • B = 30 ;
      • h = 6.5 .

Therefore, we conclude:
          1
      •     Bh = 65 .
          3




                                                           30
