                                                From Reasoning Strings to Partial Orders: Verifier-Certified Rule Transport
                                                                 through Quotient Policy Optimization
                                                                        Bang Xie1 , Hao Liu1 , Zhiyuan Peng1 , Xin Yin2 ,
                                                                    Chenhao Ying1∗ , Yuan Luo1 , Senjian Zhang1 , Wei Chen1
                                                                                    1
                                                                                        Shanghai Jiao Tong University, Shanghai, China
                                                                                           2
                                                                                             Zhejiang University, Hangzhou, China
                                                                                                  yingchenhao@sjtu.edu.cn

                                                                        Abstract
arXiv:2609.27833v1 [cs.LG] 20 Aug 2026




                                                                                                                 improve reasoning without a separately trained critic (Shao
                                                                                                                 et al. 2024; Mroueh 2025). Their optimization unit is still a
                                           Many computations admit several valid execution orders be-
                                           cause independent subgoals or disjoint state updates can com-
                                                                                                                 sampled trajectory, which leaves open when two successful
                                           mute. Reinforcement learning with verifiable rewards usually          rollouts should share credit. Two legal traces may differ only
                                           treats each successful trace as a separate token sequence, so         by commuting steps, yet trajectory-level optimization treats
                                           serialization choices can be mistaken for logical dependen-           them as separate events. Indiscriminate order augmentation
                                           cies. We introduce Verifier-Certified Rule Transport (VCRT),          creates the opposite error by rewarding invalid permutations.
                                           which replays adjacent operation pairs with native verifiers.             Transfer requires a policy to distinguish harmless reorder-
                                           Pairs whose two orders are accepted and reach the same                ing from violated prerequisites. A sequence model may over-
                                           canonical state provide commutation certificates; rejected or         fit a familiar proof script, while indiscriminate order invari-
                                           state-changing reversals provide anti-diamonds. VCRT uses
                                                                                                                 ance can admit invalid reversals. We therefore supervise re-
                                           anti-diamonds to preserve genuine prerequisites and assigns
                                           policy credit to the total probability mass of each certified         lations between operations: commutation, precedence, and
                                           orbit. It also constrains post-swap consistency, source reten-        conflict. Positive pairs share a verifier-certified outcome; neg-
                                           tion, and policy drift. We evaluate leave-one-environment-out         ative pairs introduce one controlled ordering violation.
                                           transfer across ProofWriter, CLRS, and Lean through a shared              We ask whether native verifiers can provide the missing
                                           anonymized relation-graph interface. All training and check-          structural supervision. ProofWriter supplies a deductive rule
                                           point decisions are frozen before held-out evaluation, which          engine (Tafjord, Dalvi, and Clark 2021), CLRS exposes al-
                                           uses one greedy trajectory per item without search or veri-           gorithmic state transitions (Veličković et al. 2022), and Lean
                                           fier feedback. VCRT obtains a 77.60% macro pass rate versus           checks proof programs with a trusted kernel (de Moura and
                                           64.53% for the strongest matched baseline, a paired gain of
                                                                                                                 Ullrich 2021; Yang et al. 2023). For a pair of operations, we
                                           13.06 points (95% bootstrap CI [12.58, 13.54]). Lean ac-
                                           counts for most of this gain at 33.49 points, while ProofWriter       replay both orders. When both paths are accepted and reach
                                           and CLRS improve by 2.85 points on average. Mechanism                 the same canonical terminal state, they form a reasoning
                                           tests consistently favor anti-diamond supervision, whereas            diamond. When reversal is rejected or changes the verified
                                           No-Orbit is statistically indistinguishable from full VCRT.           terminal state, the pair forms an anti-diamond. These lo-
                                           The evidence does not establish a general benefit from exact          cal certificates distinguish commutativity from precedence
                                           orbit aggregation.                                                    without relying on textual similarity.
                                                                                                                     Verifier-Certified Rule Transport (VCRT) converts these
                                                                1    Introduction                                certificates into a quotient policy objective. Successful lin-
                                                                                                                 earizations connected by certified swaps form a verifier orbit.
                                         Autoregressive generation imposes an order on output to-
                                                                                                                 VCRT applies the PPO ratio to the orbit’s total policy mass.
                                         kens. The computation represented by those tokens may al-
                                                                                                                 An anti-diamond margin separates legal and illegal mass,
                                         low several orders: proofs contain independent subgoals, al-
                                                                                                                 while auxiliary constraints control post-swap action distri-
                                         gorithms update disjoint state components, and deductive
                                                                                                                 butions, source retention, and action-level KL. A dual-view
                                         systems apply unrelated rules in either sequence. A gen-
                                                                                                                 interface keeps native states, verdicts, versions, and prove-
                                         erated trace is then one linear extension of a partially or-
                                                                                                                 nance in a sealed certificate view, while the policy receives
                                         dered computation. Sequence-level supervision can reward
                                                                                                                 only an anonymized relation graph. Figure 1 summarizes the
                                         that particular presentation instead of the dependencies that
                                                                                                                 resulting supervision.
                                         make it valid.
                                            Reinforcement learning with verifiable rewards (RLVR)                    Our evaluation holds out one complete reasoning environ-
                                         reduces ambiguity about final correctness by replacing a                ment at a time. The model trains on the other two and is
                                         learned preference score with an executable check (Cobbe                evaluated once on the third after every method, run configu-
                                         et al. 2021; Shao et al. 2024; DeepSeek-AI 2025). Group Rel-            ration, and checkpoint has been frozen. This setup measures
                                         ative Policy Optimization (GRPO) and related objectives can             whether a policy can use the same certified relation vocabu-
                                                                                                                 lary in an unseen environment. Dependency extraction from
                                            ∗
                                                Corresponding author.                                            unrestricted text lies outside the experiment. We contribute:
 • Native replay certificates for commuting operations and        grounded equivalence construction and quotient ratio, not
   prerequisite-violating reversals. No-Anti underperforms        cross-domain contrastive learning itself.
   full VCRT in each held-out fold.
                                                                  Executable reasoning environments. Formal theorem
 • A quotient-policy objective over certified trajectory or-      proving combines generative models, curriculum learning,
   bits, together with commutation, retention, and policy-        mathematical pretraining, benchmarks, and large-scale Lean
   drift constraints. The empirical benefit of exact orbit ag-    proving (Polu and Sutskever 2020; Polu et al. 2023; Azer-
   gregation remains environment-dependent.                       bayev et al. 2024; Zheng, Han, and Polu 2022; Xin et al.
 • A frozen leave-one-environment-out evaluation under a          2024). Verifier-guided logic systems use deduction, symbolic
   shared relation interface. VCRT gains 13.06 points over        solvers, or machine-checkable theories (Ling et al. 2023;
   the strongest matched baseline, replicates positively on       Pan et al. 2023; Tafjord, Dalvi, and Clark 2021); CLRS and
   Granite-4.1-3B, and keeps source decline below one             LeanDojo expose executable algorithmic and proof states
   point.                                                         (Veličković et al. 2022; Yang et al. 2023; de Moura and Ull-
                                                                  rich 2021). We use these systems as certifiers of local state
                   2    Related Work                              transitions: environment-private states establish supervision,
                                                                  while the learned policy receives only a common anonymous
Reasoning traces, search, and tools. Chain-of-thought,            relation interface.
self-consistency, STaR, and Minerva exploit intermediate or
self-generated solutions, while search and tool-assisted meth-
ods broaden the executable trace set (Wei et al. 2022; Wang                      3    Problem Formulation
et al. 2023; Zelikman et al. 2022; Lewkowycz et al. 2022;         Let environment e ∈ E have states Se , actions Ae , transition
Yao et al. 2023a; Gao et al. 2023; Chen et al. 2023; Yao          function Te , and native verifier Ve . A transition is certified
et al. 2023b; Schick et al. 2023). Such methods are com-          when
                                                                                   a
monly studied on verifiable benchmarks including MATH                            s−→e s′ ,      Ve (s, a, s′ ) = 1.            (1)
(Hendrycks et al. 2021). For VCRT, multiple traces define a
training-time equivalence relation only after verifier certifi-   A trajectory
                                                                        Q      τ = (a1 , . . . , aT ) has policy probability πθ (τ |
cation; inference uses one greedy trace.                          x) = t πθ (at | ht , x).

Reinforcement learning with verifiable rewards. RLHF              Partial Orders and Linearizations
established preference-based policy learning (Christiano
et al. 2017; Ouyang et al. 2022); PPO, DPO, and                   For an instance x, let Px = (Ax , ≺x ) denote a finite strict
REINFORCE-style updates provide different policy controls         partial order over its operations. A complete trajectory is a
(Schulman et al. 2017; Rafailov et al. 2023; Ahmadian et al.      linear extension when it contains every operation once and
2024). GRPO supports verifier-driven reasoning without a          respects every relation a ≺x b. The autoregressive model
learned critic, while outcome and process verifiers scale su-     necessarily emits one linear extension, but the underlying
pervision (Shao et al. 2024; Mroueh 2025; Cobbe et al. 2021;      partial order may admit many. Let LE(Px ) be the legal set. If
Uesato et al. 2022; Lightman et al. 2024; DeepSeek-AI 2025).      two adjacent operations are incomparable under ≺x , swap-
VCRT retains the verifier reward but replaces the sampled-        ping them preserves membership in LE(Px ); repeated adja-
trajectory ratio with a certified-orbit ratio.                    cent swaps connect all linear extensions of the same finite
                                                                  partial order. In practice, however, ≺x is not given to the
Policy equivalence and partial-order semantics. Trace             learner. We therefore use native execution to certify individ-
semantics and partial-order reduction identify or avoid           ual swap edges and define only the connected component
redundant independent-event interleavings (Mazurkiewicz           supported by those certificates.
1987; Godefroid 1996). MDP equivalence, abstraction, and
homomorphisms formalize behavior-preserving state or pol-         Diamonds and Anti-Diamonds
icy quotients (Givan, Dean, and Greig 2003; Li, Walsh, and
                                                                  Consider two local orders,
Littman 2006; van der Pol et al. 2020); POMO exploits
symmetric optima in routing (Kwon et al. 2020). Reason-                          a      b′              b      a′
ing equivalence is instance-dependent. VCRT certifies each                    s−
                                                                               → sa −
                                                                                    → sab ,           s→
                                                                                                       − sb −→ sba .            (2)
local swap and terminal state before adding trajectories to an    They form a reasoning diamond when all four transitions are
orbit.                                                            accepted, the adapted actions preserve their canonical sig-
Cross-domain and contrastive reasoning optimization.              natures, and a frozen canonicalizer ϕe satisfies ϕe (sab ) =
Recent multi-domain contrastive policy optimization aligns        ϕe (sba ). An anti-diamond is a matched pair for which re-
correct trajectories across domains and contrasts them with       versal is rejected, violates a precondition, or reaches a non-
incorrect rollouts (Yu et al. 2026), making it the closest        equivalent verified state. When exactly one complete order
policy-optimization precedent to our setting. VCRT uses           is accepted, it certifies a precedence relation.
a different supervision object: positives are linearizations           Two successful trajectories are verifier-equivalent, τ ∼V
connected by verifier-certified swaps, negatives are matched      τ ′ , if adjacent certified swaps transform one into the other.
dependency violations, and the PPO ratio is applied to certi-     Their orbit is
fied orbit mass. Our novelty claim is limited to this verifier-                        [τ ]V = {τ ′ : τ ′ ∼V τ }.             (3)
       Certified partial-order supervision
       Orbit equivalence shares credit among legal reorderings while anti-diamonds preserve true dependencies


       (a) Certified orbit                                          (b) Anti-diamond                               (c) Optimization effect

                                   same verifier-certified orbit            op A                    op B               trajectory-level                             orbit-level objective
                                                                                                                          objective                                        (VCRT)
        op A           op B
                                         A→B→C                                        A<B                                                            maximize
                                                                                   (must precede)                    A→B→C                  ≈ 1 total legal mass    A→B→C                  ≈ 0.5
                                            certified                                                                                             π(ABC) +
                                         commuting swap                                                                                            π(BAC)
                op C                                                 A→B                              B→A            B→A→C                  ≈0                      B→A→C                  ≈ 0.5


               A⊥B                       B→A→C                                       dependency
          (independent)
                                                                        ✓             preference           X          illegal orders (examples)                      illegal orders (examples)

           A, B < C                                                   accepted                        rejected       B→C→A                  ≈0                      B→C→A                   ≈0


               legal reorderings share probability mass              illegal reversals must stay low probability




                                                ✓           Learns commutativity without losing dependency sensitivity




Figure 1: Verifier-certified partial-order supervision. VCRT shares credit across certified legal reorderings while separating
dependency-violating reversals.


The relation is local and certificate-based. Equal final rewards                                        or reach a distinct verified terminal hash. Candidates with
or answers are insufficient because every connecting swap                                               nondeterministic replay, ambiguous action correspondence,
must have replay evidence.                                                                              missing provenance, or checker-version disagreement are ex-
  In Lean, two independent sibling subgoals form a rea-                                                 cluded rather than assigned a soft label.
soning diamond when both execution orders reach the same                                                   After certification, the adapter writes the policy record
verified terminal state. If an action depends on an unproved                                            while retaining enough audit information to reconstruct its
lemma, reversing the pair is rejected by the kernel and pro-                                            label.
vides an anti-diamond certificate for that prerequisite.
                                                                                                        Exact Orbit Mass
      4        Verifier-Certified Rule Transport                                                        For a verified orbit O, define quotient-policy mass
Certificate and Policy Views                                                                                                                  X
                                                                                                                 π̄θ (O | x) = Zθ (O | x) =       πθ (τ | x).                                      (4)
Figure 2 shows the separation between certification and pol-
                                                                                                                                                                   τ ∈O
icy input. The audit view retains native execution, verifier
outcomes, canonical states, versioning, and provenance. The                                             Because the training instances are exactly enumerable, Equa-
policy view removes environment identifiers, verdict text,                                              tion 4 uses the complete orbit sum. Uncertified failures re-
failure messages, and legal-action masks; it exposes only                                               main singleton orbits.
randomly renumbered action pointers and anonymous typed
relations. All methods receive this same policy view.                                                   Representative invariance. Because Equation 4 sums
                                                                                                        over the complete certified class, Zθ ([τ ]V | x) = Zθ ([τ ′ ]V |
Certificate Construction                                                                                x) whenever τ ∼V τ ′ . The policy update therefore cannot de-
                                                                                                        pend on which representative of a successful orbit happened
Construction begins from an accepted native transition and a                                            to be sampled. A sampled subset would require a separate
candidate neighboring operation. The adapter executes both                                              estimator and approximation analysis.
local orders from the same pre-state, records all intermediate
states, and checks every transition with the environment’s na-                                          Reduction to ordinary trajectory optimization. When
tive semantics. A positive certificate requires four accepted                                           an orbit contains one trajectory, Zθ ({τ } | x) = πθ (τ | x).
transitions, matching operation signatures after adaptation,                                            Thus failures and instances without certified commutations
and identical frozen canonical hashes at the two terminal                                               use the ordinary trajectory likelihood ratio. VCRT changes
states. For an anti-diamond, the legal order must be accepted                                           credit assignment only where the verifier supplies evidence
and the minimally changed reversal must either be rejected                                              for equivalence.
      Verifier-Certified Rule Transport (VCRT)
      From native execution certificates to selective partial-order policy optimization

       (1)     Native sources         (2)     Certificates                    (3)      Policy view                    (4)     Selective objective        (5)      LOEO transfer

                                         Diamond            Anti-diamond                                                                                 Leave one environment out
                                                                                     sealed certificate                          legal orbit
                    ProofWriter
             ✓                                s                   s                 verdicts • raw IDs • traces             π(AB) + π(BA)                PW + CLRS                 Lean
                      rule engine
                                         A         B                                                                         share probability mass
                                                                                                   Ψe
                                     a                 b     A            B                                                                               PW + Lean                CLRS
                        CLRS                                                                                                dependency preference
             ✓                                                                      anonymous relation                         log π(legal)
                     state checker       B         A
                                                                                         graph                                > log π(illegal)
                                              t                   X                 op A                 op B                 retain order sensitivity
                                                                                                                                                         CLRS + Lean               PW


                        Lean                 A⊥B                 A<B
             >_                          both orders         reverse order            produces → requires
                        kernel            accepted              rejected                                                      VCRT objective               Decisive evidence
                                                                                                                           L_orbit + α L_anti
                                                                                       fixed operation                  + Φ_comm + Φ_retain +             • task pass rate ↑
                                                                                          signature                              Φ_KL
                                         Certificate requirements                                                                                         • diamond gap        ↓
                                                                                        operator • subject
             accepted / rejected          native replay • terminal hash                requires • produces                                                • anti margin     ↑
              state transitions          checker version • provenance                        current
                                                                                                                             updated policy
                                                                                                                                                               held-out opened once




Figure 2: VCRT pipeline from native replay certificates to anonymized relation-graph training and leave-one-environment-out
evaluation.


Why optimize mass rather than uniformity. Averaging                                                    Applying the ratio to total legal mass gives alternatives
log likelihood over legal linearizations would favor a partic-                                         credit in proportion to their current probability without
ular distribution inside the legal set and would change when                                           forcing a uniform distribution over traces. The gradient of
additional equivalent traces are enumerated. Orbit mass in-                                            log Zθ (O | x) is a posterior-weighted average of trajectory
stead treats the certified set as one event. Moving probabil-                                          score gradients:
ity between two legal members leaves the target unchanged                                                                     X πθ (τ | x)
as long as their total mass is preserved. Exact enumeration                                              ∇θ log Zθ (O | x) =                  ∇θ log πθ (τ | x). (8)
makes that quotient literal in the four-operation setting; ille-                                                                   Zθ (O | x)
                                                                                                                                            τ ∈O
gal reversals remain outside the orbit and are handled by the
separation loss.                                                                                       Consequently, legal alternatives receive credit in proportion
                                                                                                       to their current mass without forcing a uniform distribution
Orbit-GRPO                                                                                             over stylistically different traces.
At the start of an update, the behavior policy πk , sampled                                            Dependency Separation and Constraints
trajectories, advantages, and orbit masses are frozen. For                                                                                              P
group size G, the leave-one-out advantage is                                                           For any finite trajectory set S, let Zθ (S | x) = τ ∈S πθ (τ |
                               1 X                                                                     x). Let O+ and O− denote the legal and illegal trajectory
                 Ai = Ri −             Rj .             (5)                                            sets for an anti-diamond. Their log-mass margin is
                             G−1
                                                   j̸=i
                                                                                                                   ∆θ = log Zθ (O+ | x) − log Zθ (O− | x),                                 (9)
For a successful sampled trajectory in orbit Oi , the ratio is
                                                                                                       and the separation loss is
                                    Zθ (Oi | xi )
                           ρO
                            i (θ) =               .                                 (6)                                      1
                                    Zk (Oi | xi )                                                                              max(0, m − ∆θ )2 .
                                                                                                                            Lanti =                          (10)
                                                                                                                             2
For singleton failures, it reduces to the ordinary trajectory
ratio. Below, ρi denotes ρO                                                                            For two certified swap histories hab and hba , a canonical
                            i for a certified successful orbit
and the ordinary trajectory ratio for a singleton failure. The                                         action alignment M defines
policy loss is                                                                                                Lcomm = JS(M# πθ (· | hab ) ∥ M# πθ (· | hba )) .                           (11)
               1 X
  Lorbit = −         min(ρi Ai , clip(ρi , 1 − ϵ, 1 + ϵ)Ai ) .                                         The frozen map M uses a bijection over canonical operation
               G i                                                                                     signatures; ambiguous pairs are excluded. Batch constraints
                                                             (7)                                       cap expected commutation loss at 0.01, source-orbit mass
Algorithm 1 VCRT Online Update                                     Table 1: Frozen LOEO construction. Each source contributes
                                                                   five schemas with 500 episodes per schema. “Replay” counts
Require: Source environments, native verifiers, policy πθ          all candidate orders checked during construction.
 1: Freeze πk and sample G complete trajectories per
    prompt.
                                                                     Held out       Source environments     Episodes    Replay
 2: Replay trajectories and form exact certified orbits.
 3: Freeze rewards, leave-one-out advantages, and old orbit          Lean           ProofWriter + CLRS       5,000      120,000
    masses.                                                          ProofWriter       CLRS + Lean           5,000      120,000
 4: for two optimizer epochs do                                      CLRS           ProofWriter + Lean       5,000      120,000
 5:   Recompute new trajectory and orbit masses.
 6:   Evaluate Equations 7 through 12.
 7:   Update LoRA parameters and constraint duals.                 labels, reference traces, and verdicts are unavailable to train-
 8: end for                                                        ing, model selection, and checkpoint selection.
                                                                   Generalization target. The split withholds an entire native
decline at 0.05, and action KL at 0.20. The complete objective     execution system rather than a random subset of episodes.
is                                                                 Action identifiers are renumbered and environment names
                                                                   are absent from the policy record, while the relation vocab-
 LVCRT = Lorbit + αLanti + Φcomm + Φretain + ΦKL . (12)            ulary is shared. Success therefore requires reusing decisions
                                                                   associated with commutation, precedence, and conflict un-
Here, each Φ is an augmented-Lagrangian penalty for the            der new native semantics. It does not require the model to
corresponding batch constraint.                                    recover those relations from raw source language, because
                                                                   certification and policy learning are deliberately separated.
Optimization Semantics
The anti-diamond loss and three auxiliary constraints have         Schema coverage and full-chain audit. Table 1 reports
different roles. The anti-diamond loss distinguishes prereq-       the frozen construction. Every fold must match these counts
uisites from legal swaps; the commutation constraint aligns        and achieve 100% replay agreement before training.
next-action distributions after equivalent histories; retention
                                                                   Models and optimization. The primary backbone is
bounds source decline; and action KL limits movement from
                                                                   Qwen3.5-2B at a hash-locked revision. All methods use
the behavior policy. The checker fixes orbit membership be-
                                                                   LoRA (Hu et al. 2022) with rank 64, scale 128, dropout 0.05,
fore optimization, so these terms shape probability allocation
                                                                   and attention and MLP projection targets. Training runs for
within that partition.
                                                                   400 updates, two source prompts per update, eight genera-
    Each update freezes replay verdicts, advantages, and old-
                                                                   tions per prompt, and two optimizer epochs. AdamW uses
policy probabilities, then recomputes only new-policy quan-
                                                                   learning rate 5×10−6 ; the paper checkpoint is update 400.
tities during optimization.
Training and inference boundary. Native replay is used             Methods. We compare Outcome-GRPO, which uses na-
to construct supervision on source episodes, not as a de-          tive terminal reward and a trajectory ratio; Canonical-
coding tool. During training, certificates determine which         GRPO, which shares the relational pointer interface but
sampled successes share an orbit and which matched rever-          has no orbit objective; and VCRT, which uses Equations 4
sals receive the anti-diamond penalty. At held-out inference,      through 12. Each core method runs three LOEO folds and
the model receives the anonymous relation record, emits one        three independent runs. The mechanism study evaluates No-
pointer sequence, and is scored once by the native checker.        Orbit, which uses singleton ratios, and Shuffled-Orbit,
The reported improvement therefore cannot be attributed to         which replaces the certified 12-of-24 orbit with a frozen
test-time search, repair, or verifier-guided resampling.           random set of equal size, across all three folds and runs. No-
                                                                   Anti, which removes the anti-diamond margin, is evaluated
                                                                   in a prespecified dedicated ablation.
               5   Experimental Design
Research question. Does verifier-certified dependency su-          Matched-comparison controls. All trained methods start
pervision improve transfer to a held-out reasoning environ-        from the same hash-locked backbone, see the same episode
ment, and which components account for the gain over out-          order, and use the same update count and checkpoint sched-
come GRPO and single-trajectory canonical GRPO?                    ule. Canonical-GRPO shares the anonymous relation inter-
                                                                   face with VCRT, controlling for the representation. The com-
Environments and isolation. The three environments are             ponent ablations distinguish effects within the bundled VCRT
ProofWriter, CLRS, and Lean. Each leave-one-environment-           objective.
out (LOEO) fold trains on two environments and withholds
the third. Each environment contributes five frozen schemas        Evaluation. Held-out evaluation opens once, after all pre-
with 500 episodes per schema. Each episode contains four           specified runs reach update 400 and their checkpoints are
operations and 24 complete candidate orders, of which ex-          frozen. Each item receives one temperature-zero greedy tra-
actly 12 form the certified positive orbit. Every fold therefore   jectory. There is no search, repair, reranking, retrieval, self-
contains 5,000 source episodes and 120,000 replayed trajec-        consistency, or verifier feedback during generation. The na-
tories. Native replay consistency is 100%. Held-out tasks,         tive checker scores the final trajectory. Primary outcomes are
held-out pass rate, source retention, three-fold direction, and   one point, and shuffling the orbit changes both sign and mag-
a paired bootstrap 95% confidence interval for VCRT against       nitude across environments. The component evidence there-
the strongest matched baseline.                                   fore favors learning which orders are illegal more clearly than
                                                                  redistributing credit among all legal orders.
Statistical analysis. Accuracy and verifier pass rate co-
incide because every generated complete pointer trajectory        Retention, Robustness, and Compute
receives one deterministic native replay verdict. We select the
                                                                  The largest source-task decline across the Qwen runs is 0.96
stronger of Outcome-GRPO and Canonical-GRPO by its pre-
                                                                  points, satisfying the prespecified two-point guardrail. On
specified three-fold macro average, then compute episode-
                                                                  Granite-4.1-3B, VCRT improves the frozen canonical back-
paired differences and a 95% bootstrap interval using a fixed
                                                                  bone by 36.36 points on Lean, 9.96 on ProofWriter, and 6.40
random state. Source retention is the difference between each
                                                                  on CLRS; the three-fold paired gain is 17.57 points (95% CI
trained checkpoint and its matched frozen backbone; the
                                                                  [16.35, 18.83]). Training consumes 376.55 aggregate GPU
guardrail is a maximum decline of two absolute percentage
                                                                  hours. Both backbones improve in every held-out direction,
points.
                                                                  so the positive macro result is not tied to one initialization.
Unit of comparison. All methods are evaluated on the              The replication supports the direction of transfer, but it is not
same held-out items, so the primary interval resamples paired     used to claim a scaling trend.
item-level score differences rather than pooling unrelated
trajectories. Run means describe optimizer variation, fold                               7    Discussion
means describe transfer direction, and the macro average          The matched comparisons separate the input representation
gives each held-out environment equal weight. These sum-          from part of the training objective, but they do not assign the
maries are reported separately because a narrow pooled inter-     full gain to a single component. Outcome-GRPO uses ter-
val does not imply that every run or environment improves.        minal reward with a trajectory ratio, and Canonical-GRPO
                                                                  adds the same relational pointer interface used by VCRT.
                        6   Results                               Canonical-GRPO therefore controls for that interface. The
                                                                  remaining 13.06-point macro gap belongs to the complete
Transfer under the Shared Interface                               VCRT objective, which bundles orbit credit, anti-diamond
Table 2 reports the matched comparison. Against Canonical-        separation, commutation consistency, retention, and KL con-
GRPO, VCRT gains 13.06 macro pass-rate points, with an            trol.
episode-paired 95% bootstrap CI of [12.58, 13.54]. The fold          Anti-diamond supervision has the clearest component-
gains are 33.49 points on Lean, 2.11 on ProofWriter, and          level evidence. Removing its margin hurts every held-out
3.59 on CLRS. Lean contributes approximately 85% of the           fold, even though the size of the loss varies by environment.
macro gain; ProofWriter and CLRS improve by 2.85 points           This result ties the gain to sensitivity to verified prerequisites
on average. The held-out Lean score is 100%, but five four-       within the bundled objective. It does not isolate whether the
operation sibling-goal schemas may impose a ceiling on this       margin acts independently of the commutation and retention
fold. Averaging by run also yields positive gains, although       terms, so we avoid attributing the entire macro improvement
two of nine fold-by-run comparisons are negative. The im-         to anti-diamonds alone.
provement is consistent in the fold and run aggregates, but          The orbit ablations tell a different story. No-Orbit is 0.58
not in every individual comparison. Canonical-GRPO itself         points above full VCRT on the macro average, with an inter-
improves over Outcome-GRPO by 9.16 points on Lean, 1.15           val that includes zero. Shuffled-Orbit loses heavily on Lean,
on ProofWriter, and 10.13 on CLRS. Thus the anonymous re-         gains on ProofWriter, and also has an interval crossing zero.
lational interface accounts for part of the gain over outcome-    Exact orbit mass may interact with the density and type of
only training. The additional increase from 64.53 to 77.60        certified commutations, but the current folds do not show
macro pass rate is the quantity attributable to the complete      a stable average advantage. The experiments support the se-
VCRT objective under the matched interface.                       mantic partition between legal and illegal orders more clearly
                                                                  than the choice to aggregate all legal orders into one ratio.
Mechanism and Ablations                                           Search-free interpretation. The held-out scores come
Table 3 shows that No-Anti is worse in every environment,         from one temperature-zero trajectory, so the comparison con-
while No-Orbit is statistically indistinguishable from full       cerns the policy learned during source training. There is no
VCRT on average. Shuffled-Orbit is worse on Lean and              larger candidate budget for VCRT and no opportunity to
CLRS but better on ProofWriter, and its pooled interval           ask the checker which branch to keep. This matters because
crosses zero. The prespecified “all ablations decrease” cri-      certified commutations enlarge the supervised success event
terion is therefore not met. Across the ablations, support        during optimization, but they do not enlarge the inference
is strongest for verified dependency separation; exact orbit      budget. The gain is therefore consistent with a policy that
aggregation remains environment-dependent. The signs are          has learned to respect portable dependency relations, rather
informative. Removing the anti-diamond margin reduces all         than a decoder that succeeds by exploring more orders.
three held-out means, including the two folds with modest            Lean contributes about 85% of the macro gain and
main-comparison gains. By contrast, replacing the orbit ratio     reaches 100% on five four-operation sibling-goal schemas.
with singleton ratios changes the macro result by less than       ProofWriter and CLRS improve by 2.85 points on average,
Table 2: Held-out pass rate (%) with one greedy trajectory per item. Each entry is the mean over three runs; “Macro” averages
all three LOEO directions.

                    Method                   Held-Out Lean       Held-Out ProofWriter          Held-Out CLRS     Macro
                    Outcome-GRPO                 57.35                    54.69                    61.12         57.72
                    Canonical-GRPO               66.51                    55.84                    71.25         64.53
                    VCRT                        100.00                    57.95                    74.84         77.60

Table 3: Mechanism ablations. Entries are full VCRT minus the ablation in held-out pass-rate points, so positive values favor
VCRT. Fold columns average three runs; intervals are shown where available.

                               Ablation          ProofWriter      CLRS      Lean       Macro          95% CI
                               No-Anti                   8.48      4.68    23.12       12.09               n/a
                               No-Orbit                 −0.08     −1.65     0.00       −0.58     [−3.38, 2.36]
                               Shuffled-Orbit           −8.43      5.40    31.19        9.39    [−7.71, 32.17]


Table 4: Held-out gains over the matched canonical baseline.               certified objective adds value beyond that representation.
The Qwen row compares with Canonical-GRPO; the Granite                     Third, the ablations identify dependency separation as the
row compares with its frozen canonical backbone.                           most stable part of the bundle. They do not provide compa-
                                                                           rable evidence that summing all certified legal orders into
   Backbone           Lean     ProofWriter      CLRS     Macro             one ratio is necessary. This narrower conclusion follows the
   Qwen3.5-2B         33.49           2.11       3.59    13.06             observed folds and avoids using the overall gain as evidence
   Granite-4.1-3B     36.36           9.96       6.40    17.57             for every term in the objective.

                                                                                   8     Limitations and Broader Impact
and two of nine fold-by-run comparisons are negative. The                  Verifier and representation scope. VCRT requires deter-
present Lean setting cannot distinguish strong transfer from               ministic verifiers and a supplied certified relation graph. The
ceiling saturation. The 0.96-point maximum source decline                  experiment therefore measures use of verified dependencies
also makes broad source-task forgetting an unlikely account                in a held-out environment rather than induction of those de-
of the held-out gain.                                                      pendencies from raw text.
   Finally, the experiment measures transfer through a shared,             Scale and external validity. The matched result concerns
pre-certified relation interface. The policy receives anony-               compact backbones, three structured environments, and a
mous pointers instead of environment names or raw verifier                 shared greedy-evaluation interface. Exact enumeration is
output, but it is still given the relations required for the deci-         practical for the four-operation episodes studied here; longer
sion. The reported result is therefore about using a common                traces, larger models, and less formal environments remain
relational vocabulary in a held-out environment. Dependency                outside the reported evidence.
extraction from unrestricted language and transfer across un-
related input modalities remain outside the evidence.                      Reproducibility essentials. Reproduction requires the
                                                                           frozen five-by-500 schema construction, all 24 candidate
Engineering contract. Adding an environment does not                       orders, update-400 checkpoints, matched item pairing, and
require exposing its native state to the policy. It requires               fixed backbone, verifier, and canonicalizer versions.
an adapter that can replay two local orders from one pre-
state, match the operations across those replays, and com-                 Broader impact. A checker error can be reused across
pare canonical terminal states under a fixed verifier version.             many updates, propagating its effect beyond one trajectory.
The resulting certificate can then be reduced to the same                  Deployments should therefore validate checkers indepen-
anonymous pointer-and-relation record used by the other                    dently and report certificate error rates.
environments. This boundary is important operationally:
environment-specific semantics stay in certificate construc-                                      9    Conclusion
tion, while training and evaluation consume one shared pol-                Across the three LOEO folds, VCRT gains 13.06 points (CI
icy format. The 100% replay-agreement gate in Table 1                      [12.58, 13.54]) over the strongest matched baseline, although
checks that boundary before optimization begins.                           Lean contributes most of the improvement. No-Anti is worse
                                                                           in every held-out fold, whereas replacing orbit aggregation
What the results support. The experiments separate three
                                                                           with singleton ratios does not reduce the macro score. The
claims that would otherwise be easy to conflate. First,
                                                                           current evidence favors verifier-certified dependency sepa-
Canonical-GRPO shows that the shared relation represen-
                                                                           ration as the transferable component and leaves exact orbit-
tation is useful even without orbit optimization. Second, the
                                                                           mass optimization unresolved.
remaining matched gain shows that the bundled verifier-
                        References                                  I.; Gutman-Solo, T.; Wu, Y.; Neyshabur, B.; Gur-Ari, G.; and
Ahmadian, A.; Cremer, C.; Gallé, M.; Fadaee, M.; Kreutzer,          Misra, V. 2022. Solving Quantitative Reasoning Problems
J.; Pietquin, O.; Üstün, A.; and Hooker, S. 2024. Back to Ba-       with Language Models. In Advances in Neural Information
sics: Revisiting REINFORCE-Style Optimization for Learn-            Processing Systems, volume 35, 3843–3857.
ing from Human Feedback in LLMs. In Proceedings of the              Li, L.; Walsh, T. J.; and Littman, M. L. 2006. Towards a Uni-
62nd Annual Meeting of the Association for Computational            fied Theory of State Abstraction for MDPs. In Proceedings
Linguistics, 12248–12267.                                           of the 9th International Symposium on Artificial Intelligence
Azerbayev, Z.; Schoelkopf, H.; Paster, K.; Dos Santos, M.;          and Mathematics.
McAleer, S.; Jiang, A. Q.; Deng, J.; Biderman, S.; and              Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
Welleck, S. 2024. Llemma: An Open Language Model for                B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
Mathematics. In International Conference on Learning Rep-           K. 2024. Let’s Verify Step by Step. In International Confer-
resentations.                                                       ence on Learning Representations.
Chen, W.; Ma, X.; Wang, X.; and Cohen, W. W. 2023. Pro-             Ling, Z.; Fang, Y.; Li, X.; Huang, Z.; Lee, M.; Memisevic, R.;
gram of Thoughts Prompting: Disentangling Computation               and Su, H. 2023. Deductive Verification of Chain-of-Thought
from Reasoning for Numerical Reasoning Tasks. Transac-              Reasoning. In Advances in Neural Information Processing
tions on Machine Learning Research.                                 Systems, volume 36.
Christiano, P. F.; Leike, J.; Brown, T.; Martic, M.; Legg,          Mazurkiewicz, A. 1987. Trace Theory. In Petri Nets: Appli-
S.; and Amodei, D. 2017. Deep Reinforcement Learning                cations and Relationships to Other Models of Concurrency,
from Human Preferences. In Advances in Neural Information           volume 255 of Lecture Notes in Computer Science, 278–324.
Processing Systems, volume 30.                                      Springer.
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;
Kaiser, L.; Plappert, M.; Tworek, J.; Hilton, J.; Nakano, R.;       Mroueh, Y. 2025. Reinforcement Learning with Verifiable
Hesse, C.; and Schulman, J. 2021. Training Verifiers to Solve       Rewards: GRPO’s Effective Loss, Dynamics, and Success
Math Word Problems. arXiv preprint arXiv:2110.14168.                Amplification. arXiv preprint arXiv:2503.06639.
de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theorem              Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright,
Prover and Programming Language. In Automated Deduc-                C. L.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray,
tion – CADE 28, 625–635.                                            A.; Schulman, J.; Hilton, J.; Kelton, F.; Miller, L.; Simens,
                                                                    M.; Askell, A.; Welinder, P.; Christiano, P.; Leike, J.; and
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing Reason-
                                                                    Lowe, R. 2022. Training Language Models to Follow In-
ing Capability in LLMs via Reinforcement Learning. arXiv
                                                                    structions with Human Feedback. In Advances in Neural
preprint arXiv:2501.12948.
                                                                    Information Processing Systems, volume 35, 27730–27744.
Gao, L.; Madaan, A.; Zhou, S.; Alon, U.; Liu, P.; Yang,
Y.; Callan, J.; and Neubig, G. 2023. PAL: Program-Aided             Pan, L.; Albalak, A.; Wang, X.; and Wang, W. Y. 2023. Logic-
Language Models. In Proceedings of the 40th International           LM: Empowering Large Language Models with Symbolic
Conference on Machine Learning, volume 202 of Proceed-              Solvers for Faithful Logical Reasoning. In Findings of the
ings of Machine Learning Research, 10764–10799. PMLR.               Association for Computational Linguistics: EMNLP 2023,
                                                                    3806–3824.
Givan, R.; Dean, T.; and Greig, M. 2003. Equivalence
Notions and Model Minimization in Markov Decision Pro-              Polu, S.; Han, J. M.; Zheng, K.; Baksys, M.; Babuschkin, I.;
cesses. Artificial Intelligence, 147(1–2): 163–223.                 and Sutskever, I. 2023. Formal Mathematics Statement Cur-
                                                                    riculum Learning. In International Conference on Learning
Godefroid, P. 1996. Partial-Order Methods for the Verifica-
                                                                    Representations.
tion of Concurrent Systems, volume 1032 of Lecture Notes
in Computer Science. Springer.                                      Polu, S.; and Sutskever, I. 2020. Generative Language
Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart,          Modeling for Automated Theorem Proving. arXiv preprint
S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measuring          arXiv:2009.03393.
Mathematical Problem Solving with the MATH Dataset. In              Rafailov, R.; Sharma, A.; Mitchell, E.; Manning, C. D.; Er-
Advances in Neural Information Processing Systems, vol-             mon, S.; and Finn, C. 2023. Direct Preference Optimiza-
ume 34, 12310–12322.                                                tion: Your Language Model Is Secretly a Reward Model.
Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.;   In Advances in Neural Information Processing Systems, vol-
Wang, L.; and Chen, W. 2022. LoRA: Low-Rank Adaptation              ume 36, 53728–53741.
of Large Language Models. In International Conference on            Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli,
Learning Representations.                                           M.; Hambro, E.; Zettlemoyer, L.; Cancedda, N.; and Scialom,
Kwon, Y.-D.; Choo, J.; Kim, B.; Yoon, I.; Gwon, Y.; and             T. 2023. Toolformer: Language Models Can Teach Them-
Min, S. 2020. POMO: Policy Optimization with Multiple               selves to Use Tools. In Advances in Neural Information
Optima for Reinforcement Learning. In Advances in Neural            Processing Systems, volume 36.
Information Processing Systems, volume 33, 21188–21198.             Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and
Lewkowycz, A.; Andreassen, A.; Dohan, D.; Dyer, E.;                 Klimov, O. 2017. Proximal Policy Optimization Algorithms.
Michalewski, H.; Ramasesh, V.; Slone, A.; Anil, C.; Schlag,         arXiv preprint arXiv:1707.06347.
Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.;           Zelikman, E.; Wu, Y.; Mu, J.; and Goodman, N. D. 2022.
Zhang, H.; Zhang, M.; Li, Y. K.; Wu, Y.; and Guo, D.             STaR: Bootstrapping Reasoning With Reasoning. In Ad-
2024. DeepSeekMath: Pushing the Limits of Mathemati-             vances in Neural Information Processing Systems, vol-
cal Reasoning in Open Language Models. arXiv preprint            ume 35.
arXiv:2402.03300.                                                Zheng, K.; Han, J. M.; and Polu, S. 2022. miniF2F: A Cross-
Tafjord, O.; Dalvi, B.; and Clark, P. 2021. ProofWriter:         System Benchmark for Formal Olympiad-Level Mathemat-
Generating Implications, Proofs, and Abductive Statements        ics. In International Conference on Learning Representa-
over Natural Language. In Findings of the Association for        tions.
Computational Linguistics: ACL-IJCNLP 2021, 3621–3634.
Uesato, J.; Kushman, N.; Kumar, R.; Song, H. F.; Siegel,
N. Y.; Wang, L.; Creswell, A.; Irving, G.; and Hig-
gins, I. 2022.    Solving Math Word Problems with
Process- and Outcome-Based Feedback. arXiv preprint
arXiv:2211.14275.
van der Pol, E.; Worrall, D. E.; van Hoof, H.; Oliehoek,
F. A.; and Welling, M. 2020. MDP Homomorphic Networks:
Group Symmetries in Reinforcement Learning. In Advances
in Neural Information Processing Systems, volume 33.
Veličković, P.; Badia, A. P.; Budden, D.; Pascanu, R.; Banino,
A.; Dashevskiy, M.; Hadsell, R.; and Blundell, C. 2022. The
CLRS Algorithmic Reasoning Benchmark. In Proceedings
of the 39th International Conference on Machine Learning,
volume 162 of Proceedings of Machine Learning Research,
22084–22102. PMLR.
Wang, X.; Wei, J.; Schuurmans, D.; Le, Q. V.; Chi, E. H.;
Narang, S.; Chowdhery, A.; and Zhou, D. 2023. Self-
Consistency Improves Chain of Thought Reasoning in Lan-
guage Models. In International Conference on Learning
Representations.
Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Ichter, B.;
Xia, F.; Chi, E. H.; Le, Q. V.; and Zhou, D. 2022. Chain-
of-Thought Prompting Elicits Reasoning in Large Language
Models. In Advances in Neural Information Processing Sys-
tems, volume 35, 24824–24837.
Xin, H.; Guo, D.; Shao, Z.; Ren, Z.; Zhu, Q.; Liu, B.; Ruan,
C.; Li, W.; and Liang, X. 2024. DeepSeek-Prover: Advancing
Theorem Proving in LLMs through Large-Scale Synthetic
Data. arXiv preprint arXiv:2405.14333.
Yang, K.; Swope, A. M.; Gu, A.; Chalamala, R.; Song, P.; Yu,
S.; Godil, S.; Prenger, R.; and Anandkumar, A. 2023. Le-
anDojo: Theorem Proving with Retrieval-Augmented Lan-
guage Models. In Advances in Neural Information Process-
ing Systems, volume 36.
Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T. L.; Cao,
Y.; and Narasimhan, K. 2023a. Tree of Thoughts: Deliberate
Problem Solving with Large Language Models. In Advances
in Neural Information Processing Systems, volume 36.
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan,
K.; and Cao, Y. 2023b. ReAct: Synergizing Reasoning and
Acting in Language Models. In International Conference on
Learning Representations.
Yu, Z.; Luo, W.; Sun, Y.; Fang, H.; Cong, R.; Lu, C.; and
Gong, C. 2026. Harmony in Diversity: Multi-domain Con-
trastive Policy Optimization for Large Reasoning Models.
arXiv preprint arXiv:2605.25443.
