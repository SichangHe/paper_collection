                                         Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in
                                                                            LLM Agents
                                                                          Yitao Wu1 , Si Shen2 , Rui Yang3∗ , Hong Peng3 , Bin Hu3
                                                                                                   1
                                                                                             saofund.ai, Shenzhen, China
                                                                            2
                                                                            Shenzhen Xingqing Zhiti Technology Co., Ltd., Shenzhen, China
                                                              3
                                                                School of Information Technology and Engineering, Lanzhou University, Lanzhou, China
                                                        yitaowu123@gmail.com, sishen4@acm.org, rykeryang@163.com, pengh@lzu.edu.cn, bh@lzu.edu.cn

                                                                                                                      (a) Clean feedback
                                                                        Abstract                                                                                                                                       Figure legend

                                                                                                                                                                                                                                       Agent
                                                                                                                                                                                                                       User
                                                                                                                                                                                                                                     (Planner)
                                           Verify-repair loops are a standard means for large language                                                                                                                  Agent
                                                                                                                                                                                                                                       Plan
                                                                                                                                                                                                                       (Veriﬁer)
                                           model (LLM) agents to correct faulty plans in code generation,                 User             Initial plan p0           Accept (correct)             Commit p0               Agent
                                                                                                                                               (valid)                                              (valid)             (Repairer)
                                           mathematical reasoning, and tool use. When both the verifier               (b) Noisy feedback
                                           and the repairer are noisy, repair can damage already-correct
                                           plans, and reported acceptance keeps rising while true validity
                                           falls, so existing methods lack a principled basis for deciding
                                                                                                                          User
arXiv:2607.17641v1 [cs.AI] 20 Jul 2026




                                           when repair should stop. We propose VRR-Stop, a robust stop-                                Initial plan p0           Reject       Repair damages            Accept       Final output p1
                                                                                                                                           (valid)           (false reject)   (valid → invalid)     (false accept)      (invalid)
                                           ping framework for noisy verify-repair-repeat (VRR) loops.                                                                          (probability β)

                                           A four-parameter noise model separates verifier false accep-
                                           tance and false rejection from the repair and damage behavior         Figure 1: Clean feedback accepts and commits the valid plan
                                           of the repairer. Belief filtering turns repeated verification votes   p0 , whereas noisy feedback can damage it into an invalid p1 .
                                           into an estimate of committed validity, and the loop commits
                                                                                                                 Verifier and repair errors can therefore compound, making
                                           or repairs according to the sign of the true marginal gain,
                                           which requires only sign identifiability rather than accurate         continued repair harmful.
                                           recovery of all parameters. When verifier discrimination ap-
                                           proaches zero, calibration itself fails and estimation error can
                                           flip the stopping sign, so we pair VRR-Stop with VRR-Guard,           suffice to reflect true validity. When both the verifier and
                                           an estimation-free fallback that replaces the incumbent candi-        the repairer are noisy, the two premises fail simultaneously,
                                           date only under a sufficient verification margin. On a GSM8K          turning the gains of the loop into an unpredictable systemic
                                           stress setting, VRR-Stop improves final true validity by 60.6         risk.
                                           percentage points over fixed five-round repair at an average
                                           cost of 0.72 repair rounds. Across settings, stopping reliability        Figure 1 illustrates a typical instance of this mismatch.
                                           is governed jointly by verifier discrimination and the decision       A truly valid initial plan p0 can be falsely rejected by the
                                           margin rather than by the absolute size of estimation error.          verifier under noisy feedback, turned into an invalid plan p1
                                                                                                                 by a harmful repair, and finally falsely accepted by the veri-
                                         Code — anonymous.4open.science/r/vrr-artifact-2583                      fier. Verifier errors and repairer errors thus compound inside
                                                                                                                 the loop, so true quality can decline over rounds instead of
                                                                                                                 improving. Prior studies likewise observe that proxy signals
                                                                1    Introduction                                in self-repair, LLM judges, and inference-time search can
                                         On complex multi-step tasks such as code generation, tool in-           decouple from true quality (Huang et al. 2024; Kamoi et al.
                                         vocation, and web automation, a single plan generated by an             2024a; Pan et al. 2024a,b; Khalaf et al. 2025). Verification
                                         LLM agent often contains logical gaps, constraint violations,           pass rates therefore cannot be equated with the true validity of
                                         or failing tool calls, and once such errors enter execution they        plans, and multi-round repair does not guarantee monotone
                                         can derail the entire task. Verify-repair loops are therefore           improvement. The central question of this paper is therefore
                                         widely adopted, in which a verifier checks the candidate plan,          how, in agent systems that rely on verify-repair loops, one
                                         a repairer produces a revision from the feedback, and the loop          can decide when repair has degenerated from improving true
                                         iterates toward a valid solution. A large body of work shows            quality into fitting verifier noise.
                                         that this feedback mechanism corrects explicit errors and sig-             Existing feedback-driven research can be examined from
                                         nificantly improves plan executability and reasoning quality            three directions with respect to this stopping problem. Self-
                                         (Madaan et al. 2023; Shinn et al. 2023; Lightman et al. 2024).          correction and reflective feedback let the model revise its
                                         In practice, however, the paradigm implicitly relies on two             output from its own feedback, verbal reflection, or the envi-
                                         premises that do not always hold, namely that multi-round               ronment (Madaan et al. 2023; Shinn et al. 2023; Kamoi et al.
                                         repair tends to improve true quality and that verifier outputs          2024b), yet verifier feedback and repairer behavior remain
                                                                                                                 entangled in the loop, and pass-rate fluctuations cannot be
                                            ∗
                                                Corresponding author.                                            attributed to either source. How to separate verifier noise
from repairer noise, and to characterize how true validity           repair and damage behavior, and stops according to the true
evolves with repair rounds, is a key loop-noise modeling             marginal gain of continued repair.
problem. Process supervision, external verifiers, and gener-            Verifier-guided inference and proxy over-optimization.
ative reward models constrain intermediate reasoning with            Verifier-guided methods score candidates with outcome ver-
explicit checking signals (Cobbe et al. 2021; Lightman et al.        ifiers, process reward models, or generative verifiers for can-
2024; Zhang et al. 2025a; Khalifa et al. 2026), but their            didate selection, search, or further reasoning (Cobbe et al.
effectiveness presupposes reliable feedback. When the feed-          2021; Lightman et al. 2024; Zhang et al. 2025a; Khalifa
back itself is noisy, how to estimate parameters from weak           et al. 2026), with recent work scaling sampling and verifi-
supervision while guaranteeing that estimation error does            cation budgets (Zhao, Awasthi, and Gollapudi 2025; Zhong
not turn “should stop” into “should continue” is a difficult         et al. 2025). The gains are bounded by verifier coverage,
stopping identifiability problem. Studies of test-time search        ranking error, and ROC characteristics (Stroebl, Kapoor, and
and proxy-signal optimization show that imperfect verifiers,         Narayanan 2026; Yu, Li, and Wang 2025; Dorner et al. 2026;
false acceptance, self-bias, and reward over-optimization can        Lu et al. 2025), and proxy scores in feedback loops decouple
limit or even reverse inference-time gains (Gao, Schulman,           from true quality through training- and inference-time re-
and Hilton 2023; Stroebl, Kapoor, and Narayanan 2026; Yu,            ward hacking (Pan et al. 2024a,b; Gao, Schulman, and Hilton
Li, and Wang 2025; Dorner et al. 2026; Zhou et al. 2025;             2023; Khalaf et al. 2025). HedgeTune (Khalaf et al. 2025)
Lu et al. 2025). How to detect such failure in time, and to          tunes the operating point of selection-style mechanisms, and
design a conservative stopping mechanism that does not rely          ROC-n-reroll (Dorner et al. 2026) analyzes how imperfect
on accurate parameter estimation so that continued repair no         verifiers limit resampling. Unlike these selection-style mech-
longer causes harm, is an urgent safety fallback problem.            anisms over independent candidates, a verify-repair loop
   Targeting the basic dilemma that continued repair does not        keeps rewriting the same candidate, so the repairer can both
always improve true quality, we start from the three prob-           fix invalid plans and damage valid ones. VRR-Stop targets the
lems of loop-noise modeling, stopping identifiability, and           state transitions and stopping decision of this path-dependent
safety fallback, and propose VRR-Stop, a robust stopping             rewriting rather than re-establishing proxy over-optimization
framework for noisy verify-repair-repeat (VRR) loops. The            itself.
contributions of this paper are as follows. (i) We propose              Self-correction dynamics and reliable stopping. A prob-
a four-parameter loop-dynamics model that explicitly sepa-           abilistic theory of self-correction describes accuracy con-
rates verifier false acceptance, verifier false rejection, and the   verging to a fixed ceiling at a single rate (Yang et al. 2025),
repair and damage behavior of the repairer, thereby charac-          which cannot express the interior peaks and late-stage de-
terizing how the true validity of plans evolves over multiple        cline caused by joint verifier and repairer noise. Unlabeled
repair rounds. (ii) We derive a stopping criterion driven by         accuracy estimation infers judge reliability from multiple
the sign of the true marginal gain, and give a weakly super-         classifiers (Platanios, Blum, and Mitchell 2016), Youden’s J
vised estimation method based on multi-round verification            measures how well a judge preserves class differences (Collot
records and a small number of labeled transition samples.            et al. 2026), and uncertainty-aware process verification flags
The stopping decision requires only that the gain sign be            unreliable reward-model steps (Ye et al. 2025). More recent
identifiable rather than accurate recovery of all parameters.        work treats stopping itself as a test-time decision dimension,
(iii) We give an explicit criterion for stopping-sign identifia-     via adaptive early stopping and confidence-based trace fil-
bility, show that decision reliability is jointly determined by      tering for chain-of-thought reasoning (Sun et al. 2026; Fu
the verifier discrimination J and the decision margin ∆, and         et al. 2026) or statistically valid evaluation under imperfect
empirically expose this boundary in low-discrimination ver-          judges (Feng et al. 2026), but these methods address single-
ifier scenarios. (iv) We design VRR-Guard, a conservative            pass generation or independent sampling and do not model
fallback that does not rely on accurate parameter estimation         the true-state transitions induced by repair. VRR-Stop uses
and avoids fixed-round-repair-style degradation under sign           Youden’s J for stopping identifiability rather than static judge
unidentifiability or distribution shift.                             ranking, and switches to the guarded keep-best fallback when
                                                                     the sign is unidentifiable.
                    2    Related Work
Iterative self-correction. Self-Refine revises outputs with                   3    Preliminaries and Motivation
self-generated feedback, Reflexion stores verbal feedback as
experience, CRITIC obtains verifiable critiques from exter-          3.1   Verify-Repair Loops
nal tools, and SCoRe trains self-correction with reinforce-
                                                                     We consider a canonical verify-repair loop. Given a task
ment learning (Madaan et al. 2023; Shinn et al. 2023; Gou
                                                                     instance, the agent first generates an initial plan p0 . In round
et al. 2024; Kumar et al. 2025). Follow-up studies find that,
                                                                     k, the system issues M independent verification queries on
without reliable external signals, models may fail to rec-                                                                       (m)
ognize their own errors and can corrupt previously correct           the current plan pk ; each query returns a binary signal ak ∈
answers (Huang et al. 2024; Kamoi et al. 2024a,b). This line         {0, 1} (1 for accept), yielding the acceptance count Sk =
                                                                     PM       (m)
focuses on producing better feedback and revisions, but does            m=1 ak      ∈ {0, . . . , M }. Based on Sk and the history,
not formalize termination as a decision problem in which the         the system updates the committed validity bk = Pr(yk =
verifier and the repairer are simultaneously noisy. VRR-Stop         1 | Hk ) and decides whether to commit the current plan or
separates verifier false acceptance and false rejection from         to repair it. The observables and the decision variable of a
single round are given in Eq. (1):
         XM         (m)
   Sk =            a ,        π(Hk ) ∈ {Commit, Repair},
              m=1 k
                                                              (1)
where π(Hk ) is the stopping policy over the observable his-
tory Hk . If π(Hk ) = Commit, the loop terminates and com-
mits pk ; otherwise the repairer produces the next plan pk+1
from the current plan and the verification feedback.
   To separate observable verifier outputs from unobservable
true quality, let yk ∈ {0, 1} denote the true validity of pk ,       Figure 2: The population verification rate Āt can keep in-
i.e., whether the plan actually satisfies the task constraints, is   creasing while the true-validity rate Qt peaks and then de-
executable, and completes the goal. The observable history           clines. The shaded interval marks ∆Qt < 0, where continued
up to round k is defined in Eq. (2):                                 repair becomes harmful.
        Hk = (p0 , S0 , . . . , pk , Sk ),   yk ∈ {0, 1}.     (2)
Since yk is generally unavailable at deployment, the stopping        validity, and stop when it no longer exceeds a minimum-gain
policy must act on Hk alone. An accepted plan is therefore           threshold, as specified in Eq. (4):
not necessarily valid, and a rejected plan is not necessarily
invalid.                                                                          Gk = E[yk+1 − yk | Hk , continue] ,
                                                                                        
                                                                                          Repair, Gk > τ,                        (4)
3.2   Noise Model                                                              π(Hk ) =
                                                                                          Commit, Gk ≤ τ,
Observed signals do not equal true validity, and repair is
not a monotone improvement process. To capture both kinds            where τ ≥ 0 converts extra computation into a minimum
of uncertainty, we adopt a compact noise model, given in             acceptable validity gain or acts as a conservative margin;
Eq. (3):                                                             τ = 0 when cost is ignored. Eq. (4) adopts the one-step
                                                                     gain as the stopping target, comparing only a commit now
                          (m)
            ρ0 = Pr(ak          = 1 | yk = 0),                       against exactly one more repair round, without look-ahead
                     (m)                                             over multi-round trajectories. Since yk is unobservable at
            ρ1 = Pr(ak = 0 | yk = 1),                                deployment, Eq. (4) only defines the target; estimating Gk is
             α = Pr(yk+1 = 1 | yk = 0, repair),               (3)    deferred to the method section.
             β = Pr(yk+1 = 0 | yk = 1, repair),
             J = 1 − ρ0 − ρ 1 ,                                      3.4   Motivation
                                                                     More repair is not always beneficial. When the damage
where ρ0 is the probability that an invalid plan is falsely ac-      probability is non-negligible, simply adding repair rounds
cepted, ρ1 the probability that a valid plan is falsely rejected,    can push true quality past a peak into sustained decline.
α the probability that repair turns an invalid plan valid, and       Iterative refinement methods such as Self-Refine, Reflexion,
β the probability that repair damages a valid plan. J is the         and CRITIC assume that outputs improve over rounds of
discrimination ability of the verifier. As J approaches 0, ac-       feedback (Madaan et al. 2023; Shinn et al. 2023; Gou et al.
ceptance signals can no longer support fine-grained stopping         2024). Let Qt = Pr(yt = 1) be the population true-validity
decisions.                                                           rate (subscript t indexes population-level round dynamics,
   The model treats repeated queries on the same plan as             distinct from the per-instance index k). If every round triggers
conditionally independent observations given the true state,         repair, then Qt+1 = Qt (1 − β) + (1 − Qt )α, so whenever
and treats ρ0 , ρ1 , α, β as stable within a local decision win-     Qt is already high or β is non-negligible, Qt+1 − Qt ≤ 0
dow. The former supports Bayesian updates from acceptance            and repair noise accumulates over rounds. As Fig. 2 shows,
counts; the latter lets the one-step marginal gain be character-     Qt enters a declining regime after t⋆ , the round at which
ized by compact parameters. The conditional-noise assump-            the marginal gain turns negative. This risk is not a corner
tion also ignores instance-level difficulty heterogeneity. The       case under extreme parameters. Self-correction is known to
same verifier may err at different rates on different plans,         corrupt correct answers (Huang et al. 2024; Kamoi et al.
and repeated queries may be correlated; a beta-binomial              2024a), and our measured repair trajectories reach β close to
estimator diagnoses such within-class heterogeneity (Ap-             0.94. Multi-round repair therefore cannot be treated as a safe
pendix E). Both assumptions are local approximations rather          default; an explicit stopping mechanism is required.
than global stationarity claims; their applicable range under           Verifier signals can improve without true validity im-
non-stationarity is analyzed in the experiments.                     proving. Treating verifier pass rates as a quality metric makes
                                                                     the system overestimate the benefit of repair (Zhao, Awasthi,
3.3   Stopping Objective                                             and Gollapudi 2025; Zhong et al. 2025; Khalifa et al. 2026).
The question is when, given Hk , the system should repair            With Āt = E[St /M ], the population verification rate satis-
once more rather than commit. We define the true marginal            fies Āt = ρ0 + (1 − ρ0 − ρ1 )Qt , where 1 − ρ1 and ρ0 are the
gain of one more repair round as the expected change in true         verifier true- and false-positive rates. When J = 1 − ρ0 − ρ1
is low or the noise parameters drift, the system can exhibit        executed, the true state transitions by α, β and the predict
Āt+1 − Āt > 0 while Qt+1 − Qt ≤ 0: the dashed curve in            step is b−
                                                                             k+1 = (1 − β)bk + α(1 − bk ). The recursion relies
Fig. 2 keeps rising while true validity already falls. Verifier     on one explicit assumption, namely that the repair transi-
calibration can degrade quickly after switching models, veri-       tion is conditionally independent of Hk given yk . Although
fiers, or task distributions, so optimizing pass rates alone does   plans entering repair are filtered by verification signals, their
not guarantee quality gains; verifier noise and true validity       transitions are still governed by α, β; the labeled transition
must be modeled separately.                                         samples are collected from frozen trajectories in which every
   Stopping requires identifiable evidence. Heuristic stop-         round triggers repair, consistent with this assumption.
ping rules such as fixed round budgets, consecutive-pass               Subtracting the current belief from the predictive belief
counts, or score thresholds cannot reliably judge whether           gives the true marginal gain of one more repair round, and
repair is still worthwhile. Existing test-time scaling and          setting it to zero yields the critical posterior belief, as in
verifier-guided methods focus on exploiting more sampling,          Eqs. (6)–(7):
verification, or repair, and rarely model whether the param-
eters required for stopping are identifiable under weak su-                     Gk = b−
                                                                                      k+1 − bk = (1 − bk )α − bk β,                  (6)
pervision. What the decision actually needs is the sign of                       b⋆ = α/(α + β),           α + β > 0,                (7)
∆Qt = Qt+1 − Qt , while the available signals are only
the acceptance counts {S0 , . . . , St } and a few labeled repair   where the first term of Eq. (6) is the expected gain from fixing
transitions. If estimation error flips the sign of ∆Q
                                                    dt , the sys-   an invalid plan and the second the expected loss from damag-
tem mistakes “should stop” for “should continue” and enters         ing a valid one. b⋆ is exactly the fixed point of the population
a regime of sustained damage. Class balance, verifier calibra-      dynamics Qt+1 = Qt (1 − β) + (1 − Qt )α of the motiva-
tion, and Youden’s J all affect judge reliability, and accuracy     tion subsection. Repair can only push validity toward b⋆ , and
estimation without labels itself requires assumptions (Collot       once the belief crosses it, the expected direction of further
et al. 2026; Platanios, Blum, and Mitchell 2016). A stopping        repair is downward. The belief space thus splits into a repair-
policy should therefore be near-optimal when evidence suf-          beneficial regime (bk < b⋆ ) and a repair-harmful regime
fices and fall back to a conservative decision when it does         (bk ≥ b⋆ ). The boundary depends only on the repairer’s α
not.                                                                and β; verifier noise ρ0 , ρ1 does not move the boundary but
                                                                    determines, through bk , whether the comparison is reliable
                        4    Method                                 (next subsection).
                                                                       Stopping follows the one-step objective of Eq. (4) with
Figure 3 gives an overview. Given the verify-repair his-            Gk from Eq. (6). All experiments use τ = 0; a nonzero
tory Hk and one-off weakly supervised calibration data, the         threshold shifts the boundary to b⋆τ = (α − τ )/(α + β), and
framework estimates the committed validity of the current           no repair is issued if α ≤ τ . The rule ties the stopping time
plan round by round and outputs commit or repair. It con-           to a direct comparison between repair benefit and damage
sists of a belief estimator that turns the M verification votes     risk rather than to a preset budget or pass-rate threshold.
of each round into the posterior bk (stage one), a stopping         When the round budget Kmax is exhausted, the current plan
criterion that forms the marginal gain Gk and acts on its           is committed.
sign (stages two and three), and the conservative fallback
VRR-Guard that takes over commitment when calibration               4.2    Calibration and Sign Identifiability
is unreliable (stage four). The three components address, in
order, the loop-noise modeling, stopping identifiability, and       At deployment, none of bk , ρ0 , ρ1 , α, β is directly observ-
safety fallback problems raised in the introduction.                able. Calibration uses two kinds of weak supervision. For
                                                                    repeated verification records, per-plan acceptance counts
4.1    Belief Filtering and the Stopping Boundary                   are modeled as a two-component binomial mixture whose
                                                                    components correspond to truly valid and invalid plans; a
Given Hk , the committed validity bk = Pr(yk = 1 | Hk ) is
                                                                    binomial-mixture expectation-maximization (EM) estimator
the posterior probability that the current plan is truly worth
                                                                    recovers the mixture weight and ρ̂0 , ρ̂1 without labels. For
committing; it is not the verification pass rate, which can rise
merely through false acceptance.                                    repair transitions, α̂, β̂ are frequency estimates from at most
   The belief evolves by an update–predict recursion. The           300 labeled before-after plan pairs, with labels produced by
initial belief is the generator prior b−
                                       0 = π̂, estimated on the
                                                                    each task’s validity-judging rule.
calibration folds as the true-validity rate of initial plans. In        Substituting the estimates into Eq. (6) gives Ĝk = (1 −
round k, the M queries are conditionally independent given          b̂k )α̂ − b̂k β̂, with b̂k computed from Eq. (5) under ρ̂0 , ρ̂1 , so
yk , so Sk is binomial and the observation update is given in       calibration error propagates into Ĝk . Let the error radius Bk
Eq. (5):                                                            satisfy Pr(|Ĝk − Gk | ≤ Bk ) ≥ 1 − η, where η is a user-
                       b−          Sk M −Sk                         chosen tolerance; Bk shrinks as the calibration sample size,
                        k (1 − ρ1 ) ρ1                              the verification budget M , and the discrimination J grow.
bk =                                                        ,
      b−          Sk M −Sk + (1 − b− )ρSk (1 − ρ )M −Sk
       k (1 − ρ1 ) ρ1                k   0        0                 The sign-identifiability condition is given in Eq. (8):
                                                          (5)
where b−k is the predictive belief before observing this                         Ĝk − Bk > τ       or Ĝk + Bk ≤ τ.                 (8)
round’s votes; the binomial coefficients cancel. If repair is
                             Task & loop context                             1 Committed validity                   2    Marginal gain characterization                  3    Stopping criterion
                                                                                          estimation
                                                                                                                                                                     Visual boundary (optimal point)                               identiﬁable stop                             Final commit
         "Create a tool-use plan                                                                                                                                                                                               (         , identiﬁable)
         to schedule a meeting."                                             History        Current plan                Two outcomes of another repair

                                                                                                                        Repair success           Repair success
                                                                                                                                                                                                              not identiﬁable
                                                    Planner                                                                 (gain)                   (gain)
                                                                                                                                                                        STOP                    GO
                                                                                                                                                                                                                                                                                    commit
                                                                                Planner
                                                                                                                                                                                                                           4       Guarded fallback                             (identiﬁable stop)
                                               LLM planner                                                                                                                                                                         (if calibration unreliable)

                                               generates                                                                                                                         Stop Point
                                                                                                                                                                             (Optimal Boundary)                                Is the new plan better?
                                                         writes an initial
                                                         tool-use plan
                                                                                                                                                                                                                                             VS
                                                                                                                        Marginal gain (one more repair)                         Decision rule
         Veriﬁer                                                                                                                                                                                                   Current                         Best Champion
                              Verify                                                                                                                                                                              Candidate                            So Far
                                                                                                                                                                                                                (current plan)                       (champion)                     commit
                                                                                   Current Plan Validity
                                                                                                                                                                      If the current plan's quality is:                                                                             (fallback)
                                       [1] Check availability
      LLM veriﬁer                                                                                                                                                                                                Veriﬁer votes (repeat                     times)
                                       [2] Reserve room
                   history                                                                                                                                             above the stop point                      Veriﬁer           Veriﬁer    Veriﬁer            Veriﬁer



                                       [3] Create calendar event                                                   Repair gain                        Damage risk                       STOP
                                                                              0%                      100%          (beneﬁt)                            (cost)
                                       [4] Send conﬁrmation
         Repairer
                                                                             Likelihood that the plan will                                                              below the stop point
                                                                                                                    Marginal Gain = Repair Gain - Damage Risk                                                         Replace champion only
                                                                                succeed if committed.                                                                                                                when current plan receives
                                                                                                                                                                                        CONTINUE
                                          Initial plan     (true valid)                                                                                                                                               signiﬁcantly more votes
                                                                                                                              calibrated from weak supervision                                                              (margin ).
      LLM repairer

                                                                                           continue & reliable calibration (next repair round)




Figure 3: Overview of VRR-Stop, which estimates committed validity bk and stops according to the marginal gain Gk . VRR-
Guard is evaluated separately as a conservative fallback when calibration is unreliable.


Proposition 1 (Stopping-sign consistency) If Eq. (8)                                                                                                truly invalid, queries are conditionally indepen-
holds, the action taken under Ĝk agrees with the action                                                                                            dent given true states, and J ≥ 0. Then the per-
under the true Gk with probability at least 1 − η.                                                                                                  round    erroneous-replacement        probability  satisfies
                                                                                                                                                                                                              
                                                                                                                                                    Pr[S(p) ≥ S(c) + δ] ≤ exp − (M J + δ)2 /(2M ) ,
   The proof and a sample-complexity bound are in Ap-                                                                                               and the probability of at least one such replacement within
pendix A; the guarantee presupposes that Bk attains its nom-                                                                                        Kmax rounds is at most Kmax times this bound.
inal coverage. Writing the decision margin as ∆k = |Gk −τ |,
whether the premise of Proposition 1 can be met is governed                                                                                            The lemma follows from a Hoeffding bound on the dif-
jointly by J, the calibration sample size, and ∆k . As J → 0                                                                                        ference of two independent binomials (proof and exact per-
or ∆k → 0, the required evidence grows rapidly, and near-                                                                                           verifier tail probabilities in Appendix A), showing that erro-
zero J can defeat even a large margin because the posterior                                                                                         neous replacement decays exponentially in δ and M J and
itself cannot be located reliably. In the experiments, VRR-                                                                                         giving the margin an analytic basis. The bound is conser-
Stop acts directly on the sign of Ĝk ; Eq. (8) and Proposition 1                                                                                   vative; with M = 8, the replay ablation of Appendix I
serve as reliability-analysis tools for the flip-risk evaluation                                                                                    selects δ = 5 as the most robust setting. Because Eq. (9)
in the experiments.                                                                                                                                 compares vote counts across rounds, it implicitly assumes
                                                                                                                                                    within-trajectory stationarity of verifier noise; degradation
                                                                                                                                                                                            Noisy feedback                            Clean feedback
4.3   Guarded Keep-Best Fallback                                                                                                                    under drift is tested in the shift        False experiments.
                                                                                                                                                                                                    reject                   VRR-GuardCorrect accept

                                                                                                                                                    does not strictly dominate no-repair. It forfeits part of the
When a separation test on held-out labeled samples reports Jˆ                                                                                                                                                  Repairer                                                        [1] Check availability
                                                                                                                                                    achievable gain in repair-beneficial regimes in exchange for
near zero, or Eq. (8) fails throughout the evaluation window,                                                                                                                                                                                                                  [2] Reserve room
                                                                                                                                                    near-no-repair downside protection when calibration is un-                                                                 [3] Create calendar event
calibrated stopping is no longer trustworthy and VRR-Guard                                                                                                                         LLM repairer
                                                                                                                                                    reliable.                       rewrites p0                                                                                [4] Send conﬁrmation
should be used instead. The test compares acceptance rates                                                                                                                                 Harmful repair
of valid and invalid plans directly on labeled samples and                                                                                             Pseudocode integrating both               stopping modes                appears
                                                                                                                                                                                                                           Accepted              in
                                                                                                                                                                                                                                    p0 Final output


does not depend on the binomial-mixture EM, avoiding di-                                                                                            Appendix A, where the mode-selection threshold Jmin                              Correctcor-
                                                                                                                                                                                                                                              accept

                                                                                                                                                                                                     [1] Check availability
agnosing a possibly broken estimator with its own output. We                                                                                        responds to the held-out separation test above; scenarios              Correct ﬁnal output
                                                                                                                                                                                                                                               are
                                                                                                                                                                                                     [2] Reserve room

partition evaluation scenarios offline by this criterion rather
                                                                                                                                                                      if rejected,
                                                                                                                                                    partitioned offline      without
                                                                                                                                                                      repair again
                                                                                                                                                                                      tuning          J  min       online.   Each
                                                                                                                                                                                                     [3] Create calendar event
                                                                                                                                                                                                                                        round                                      - veriﬁer accepts
                                                                                                                                                                                                                                                                                   - true validity

than deploying an online threshold switch.                                                                                                          costs M verifier calls plus a constant-time belief update, and
                                                                                                                                                                                                     [4] Send conﬁrmation


   VRR-Guard maintains the incumbent best candidate ck ,                                                                                            repair calls occur only on Repair.
                                                                                                                                                                                   Damaged plan p1
                                                                                                                                                                                                  Calibration is a one-off cost
initialized as c0 = p0 . For any plan p, let S(p) =                                                                                                 using repeated verification records    Verify againand at most 300 labeled

PM        (m)                                                                                                                                       transitions. Hyperparameters are the verification budget M ,
   m=1 a      (p) be its acceptance count, so Sk = S(pk ).                                                                                          gain threshold τ , retention margin δ, and              False repair
                                                                                                                                                                                                               Veriﬁer
                                                                                                                                                                                                                            ﬁnal outputKmax .
                                                                                                                                                                                                                          budget
                                                                                                                                                                                                                      Wrong
Given a retention margin δ, the retention rule is given in                                                                                                                                                 accept
                                                                                                                                                                                                                                                                           - veriﬁer accepts
                                                                                                                                                                                                                                                                           - true validity
Eq. (9):                                                                                                                                                                                                   LLM veriﬁer

                                                                                                                                                                                          5          Experiments
                                                                                                                                                                                                          checks plan p1


                    pk ,     S(pk ) ≥ S(ck−1 ) + δ,                                                                                                 We organize the evaluation around four research questions.
            ck =                                            (9)
                    ck−1 , otherwise,                                                                                                               RQ1: Does multi-round verify-repair monotonically im-
                                                                                                                                                    prove true validity, or does reported acceptance rise while
and the incumbent ck , not the last plan, is committed at                                                                                           true validity falls? RQ2: When repair can be harmful, does
termination.                                                                                                                                        VRR-Stop avoid the degradation of heuristic stopping and
Lemma 1 (Bound on erroneous replacement) Suppose                                                                                                    approach the true-parameter myopic reference? RQ3: With
the incumbent c is truly valid and the new plan p                                                                                                   limited calibration samples and varying verifier discrimina-
tion, when is the stopping sign identifiable, and how does                                         Repair loop: true validity
estimation error flip the decision? RQ4: When calibration                                          Resample control: true validity
                                                                                                   Verifier acceptance
fails or the distribution shifts, does the conservative fallback                        1.00
retreat to near no-repair instead of collapsing?                                                                  K ⋆ =2

                                                                                        0.75




                                                                          Probability
5.1   Setup
Tasks, models, and protocol. The evaluation covers mathe-                               0.50
matical reasoning (GSM8K (Cobbe et al. 2021), MATH-500
(Hendrycks et al. 2021; Lightman et al. 2024)), code gen-                               0.25
eration (MBPP (Austin et al. 2021)), and tool use (BFCL
(Patil et al. 2025)); true validity is judged by answer match-                          0.00
                                                                                               0      1       2        3       4     5   6
ing, symbolic verification, unit tests, and an executor, re-
                                                                                                              Repair round k
spectively. Generators and verifiers span the Qwen2.5 (Yang
et al. 2024), Mistral (Jiang et al. 2023), and Llama (Grattafiori
et al. 2024) families. End-to-end evaluation uses Kmax = 5          Figure 4: Loop dynamics under the non-stationary stress
repair rounds and M = 8 verification queries per round;             setting (N = 300, prompt mismatch from round 3). True
the non-stationary loop-dynamics diagnostic runs to round           validity peaks at K ⋆ = 2 and then collapses, while indepen-
6. All calibration parameters are estimated with five-fold          dent resampling shows no comparable decline.
cross-fitting, so no instance’s stopping decision touches its
own label; the full protocol and model configurations are in
Appendix B.                                                         the risk. With a process-reward-model verifier of J = 0.805
   Metrics and baselines. The primary metric is the true            on GSM8K, fixed five-round repair still drives validity from
validity V of the final commit (95% bootstrap confidence            0.727 to 0.097, and on MATH-500 (J = 0.77) from 0.798
intervals from B=10,000 resamples) and the mean repair              to 0.150 while the TPM reference holds 0.798, so verifier
rounds ⟨K⟩; verifier reliability is described by ρ0 , ρ1 and        quality strengthens stopping reliability but cannot eliminate
Youden’s J = 1 − ρ0 − ρ1 ; paired differences use exact             repair damage (Appendix H). On the N = 500 stress traces,
McNemar tests and instance-level bootstrap. Baselines fall          55% of instances see a correct plan repaired into an incor-
into three groups. Fixed-budget repair corresponds to the           rect one, and 24% of these damaging repairs win majority
common configurations of Self-Refine, Reflexion, CRITIC,            acceptance, raw-label statistics that are independent of any
and SCoRe (Madaan et al. 2023; Shinn et al. 2023; Gou               stopping rule (Appendix C).
et al. 2024; Kumar et al. 2025). Heuristic stopping relies
only on verification signals and includes majority stopping         5.3        Stopping Performance
and confidence-threshold stopping (Wang et al. 2023). Ref-          For RQ2, Table 1 evaluates end-to-end gains on the GSM8K
erence policies include no-repair, the true-parameter myopic        / Qwen2.5-3B stress setting. Fixed five-round repair de-
(TPM) reference, and hindsight best-round selection, the lat-       grades the no-repair baseline from 0.700 to 0.116, whereas
ter two serving only as diagnostics. Formal definitions are in      VRR-Stop reaches 0.722 with only 0.72 repair rounds on
Appendix A.                                                         average. Against fixed five-round repair, the paired gain is
                                                                    60.6 percentage points (95% CI [+56.0, +65.0], McNemar
5.2   Loop Dynamics                                                 p < 2 × 10−85 ); VRR-Stop also beats majority stopping
Addressing RQ1, Fig. 4 shows that, under a 256-token ini-           (+3.2 pp, p < 2 × 10−4 ) and the TPM reference (+2.8 pp,
tial budget, validity starts at 0.45, rises to 0.87 after two       p < 6 × 10−4 ), while its difference from no-repair (+2.2
repair rounds, then collapses after prompt mismatch is in-          pp) has a CI crossing zero. Under the fixed-budget deploy-
jected at round 3, reaching only 0.12 at round 6, which forms       ment mode of iterative-feedback baselines, Reflexion and
an interior optimum at K ⋆ = 2, whereas an independent-             Self-Refine end at 0.095 and 0.080 on this stress setting,
resampling control with the same budget stays between 0.47          while VRR-Stop on the same batches of trajectories reaches
and 0.85 throughout. The paired gain of the peak round              0.740 and 0.710. The ordering replicates across sample sizes
over the final round is 74.7 percentage points (95% CI              and domains, with three disjoint GSM8K windows giving
[+69.3, +79.7]), and the control exhibits no comparable             0.752±0.037 against the reference 0.757±0.058 and Qwen-
path-dependent decline, so the degradation stems from re-           7B stress retaining 0.875 by learning to never repair. Cali-
peated rewriting of the same candidate rather than sampling         brated stopping thus terminates the loop in time when repair
noise. Non-stationary loops thus contain an intrinsic bound-        is harmful, preserving validity at lower cost than heuristic
ary where the gain turns negative; reliable stopping depends        voting; all remaining baselines and paired tests are in Ap-
on identifying the gain sign in time, not on preset budgets.        pendices D and G.
The pattern is not specific to this diagnostic. Across eight
settings, six exhibit monotone decline with damage proba-           5.4        Calibration and Identifiability
bilities between 0.615 and 0.938, BFCL multi-turn stays flat        For RQ3, we sweep a controlled J–∆ grid (∆ is the deci-
under a near-inert repair operator, and only the favorable set-     sion margin of the calibration subsection) and evaluate four
ting improves, so harmful repair is the rule rather than the        cross-family verifiers on GSM8K, with N = 300 calibration
exception under stress. A stronger verifier does not remove         samples and M = 8 queries per plan. Figure 5 shows that
Table 1: Stopping performance on the GSM8K / Qwen2.5-3B                                        Table 2: Robustness under calibration failure and distribution
prompt-mismatch stress setting (N =500, M =8, Kmax =5),                                        shift, replayed on saved trajectories with M = 8 and δ = 5;
abbreviated; the TPM reference applies the same stopping                                       shift codes M, V, T denote model, verifier, and task shift.
rule with ground-truth parameters as a diagnostic.
                                                                                                Setting                   J    None Fixed 5 Calib. Guard
       Method                            True validity V [95% CI]         ⟨K⟩
                                                                                                Qwen-3B fav. (–)      0.39 0.740       0.875   0.845   0.810
       No repair                              0.700 [.658,.740]           0.00                  Qwen-3B stress (–)    0.46 0.700       0.116   0.722   0.742
       Majority stopping                      0.690 [.648,.730]           0.92                  Qwen-7B stress (M)    0.23 0.875       0.075   0.875   0.875
       ConfStop-0.85                          0.562 [.518,.604]           1.92                  Mistral-7B stress (V) 0.18 0.507       0.047   0.463   0.487
       Fixed repair K=5                       0.116 [.088,.144]           5.00                  Llama-3-8B stress (M) 0.03 0.803       0.057   0.223   0.793
       VRR-Stop                               0.722 [.682,.760]           0.72                  MATH-500 (T)          0.22 0.798       0.150   0.798   0.796
       TPM reference                          0.694 [.652,.734]           0.89                  BFCL single (T)       0.07 0.812       0.372   0.782   0.810


                       0.6                                               0.5
                                                      synthetic                                in all seven settings and never collapses. In the Llama set-
                                                      grid limit
                       0.5              Qwen-3B
                                                                                               ting where calibrated stopping fails, VRR-Guard recovers to
                                                                         0.4
                                                                                               0.793, exceeding the failed VRR-Stop by 57.0 percentage
      Youden index J




                       0.4                                                                     points (95% CI [+51.0, +62.7], McNemar p < 1 × 10−47 )
                                                                               Pr[sign flip]
                                                       Qwen-7B: safe
                                                                         0.3                   and fixed five-round repair by 73.7 points. Its conservatism
                                                       (beyond grid)
                       0.3                                                                     costs about 2.0 and 0.3 pp against no-repair on Mistral and
                                                                         0.2                   BFCL (the latter’s paired CI contains zero), and its 0.810
                       0.2                                                                     in the favorable setting trails fixed five-round repair’s 0.875.
                                        Mistral       Llama: collapsed                         Against margin-free verifier-best selection, the retention mar-
                                                      (J-driven)         0.1
                       0.1                                                                     gin contributes +45.0 pp in the Llama scenario and between
                                                                                               −4.0 and +8.0 pp elsewhere, concentrating its value where
                       0.0                                               0.0
                          0.0     0.2       0.4      0.6           0.8
                                                                                               verification signals are least trustworthy. The value of VRR-
                                decision margin ¢ = jG(¼)j                                     Guard is to pull the system back to a near-no-repair safe state
                                                                                               when the sign is unidentifiable, not to dominate everywhere;
                                                                                               full results and paired tests are in Appendices F and G. Ab-
Figure 5: Stopping-sign flip probability over J and ∆ under                                    lations of the calibration input, the retention margin δ, and
the deployed rule; markers denote real verifiers. Flip risk                                    the calibration sample size corroborate these design choices,
concentrates at low J and low ∆, and near-zero J fails even                                    with binomial EM the best input, δ = 5 most robust, and
with a large margin (Llama).                                                                   Ncalib = 300 sufficient (Appendix I).

                                                                                                                    6    Conclusion
flip risk concentrates where low J meets low ∆. The flip
probability reaches 0.183 for J ≤ 0.15 and ∆ ≤ 0.10, ver-                                      This paper addresses the stopping decision in LLM verify-
sus 0.014 for J ≥ 0.4 or ∆ ≥ 0.30, a roughly 13-fold gap.                                      repair loops, whose crux is that the paradigm implicitly as-
Among the real verifiers, calibrated stopping stays within 2.8                                 sumes multi-round repair improves true quality and verifi-
percentage points of the TPM reference for Qwen-3B, Qwen-                                      cation signals represent true validity, and both assumptions
7B, and Mistral (all J ≥ 0.18), whereas Llama has J of only                                    fail together when the verifier and the repairer are noisy.
0.03. Despite a decision margin of about 0.74, its validity                                    We propose VRR-Stop, which builds on a four-parameter
collapses from the reference 0.803 to 0.223 (−58.0 pp, 95%                                     noise model and couples belief filtering with a marginal-gain
CI [−63.7, −52.0], McNemar p < 2 × 10−48 ). The failure                                        sign criterion, turning stopping into a calibratable, identifi-
mechanism is that the likelihood surface of the binomial-                                      able sign decision, with the fallback VRR-Guard covering
mixture EM flattens as J → 0. With N = 120 the estimate                                        the unidentifiable regime. On the GSM8K / Qwen2.5-3B
is ρ̂1 = 0.27, yet enlarging the sample to 300 worsens it                                      stress setting, VRR-Stop improves final true validity by 60.6
to 0.077 against a true 0.609, and a parameter sweep shows                                     percentage points over fixed five-round repair and slightly
calibrated stopping recovers only for ρ̂1 ≳ 0.30. Stopping                                     exceeds the true-parameter myopic reference, while VRR-
reliability is thus determined by whether finite evidence can                                  Guard restores validity from 0.223 to 0.793 when calibra-
stabilize the gain sign, not by the absolute size of parameter                                 tion fails at near-zero discrimination. The method is limited
error; near-zero J mandates abandoning fine-grained cali-                                      by its local-stationarity approximation and binary validity
bration for the conservative fallback (Appendix E).                                            representation; future work will model round-varying repair
                                                                                               dynamics and online switching between the two modes.
5.5         Guarded Fallback under Shift
For RQ4, Table 2 examines calibration failure and distribu-                                                       Acknowledgments
tion shift. Fixed five-round repair falls far below no-repair                                  This work was supported in part by the Brain Science
in most shifted settings (e.g., Qwen-7B drops from 0.875 to                                    and Brain-like Intelligence Technology-National Science
0.075), whereas VRR-Guard stays near the no-repair level                                       and Technology Major Project (No. 2021ZD0200600, No.
2021ZD0200408), and in part by the National Natural Sci-                               0.4            Favorable
                                                                                                                                                  continue
ence Foundation of China (Grant No. U24B20186), and sup-
ported by the Supercomputing Center of Lanzhou University.
                                                                                                      BFCL multi-turn              b * = 0.564               b * = 0.954




                                                                  marginal gain G(b)
  A    Derivations, Algorithms, and Reference                                          0.0

                       Policies                                                                              b * = 0.289
                                                                                                    GSM8K stress
This appendix provides the complete derivations of the stop-
ping quantities in the main text, proofs of the two formal                             -0.4
results, the construction of the calibration estimators and the
error radius, and formal definitions of all comparison poli-
                                                                                                                                                  stop
cies. Pseudocode integrating the two stopping modes is given
in Algorithm 1; the mode-selection threshold Jmin corre-                               -0.8
sponds to the separability check on held-out labeled samples                                  0.0          0.2             0.4              0.6     0.8            1.0
in the guarded-fallback subsection of the main text. Eval-                                                                       belief b
uation scenarios were partitioned offline according to this
check, and the specific value of Jmin was not tuned online.       Figure 6: Expected benefit G(b) = (1 − b)α − bβ of running
                                                                  one more repair round, where b is the probability that the
A.1    Belief Recursion and the Stopping Boundary                 current plan is already correct, α is the probability that repair
Conditioned on the true state yk , the M verification queries     fixes an incorrect plan, and β is the probability that repair
are conditionally independent, so the acceptance count is         breaks a correct one; the three lines use the (α, β) values
binomial: Sk | yk =1 ∼ Bin(M, 1 − ρ1 ) and Sk | yk =0 ∼           measured in Table 5. Wherever a line lies above zero, one
Bin(M, ρ0 ). Applying Bayes’ rule to the predictive belief        more repair is expected to help; below zero it is expected to
b−                                                                hurt; the crossing b⋆ = α/(α+β) (vertical dashes) marks the
  k , the two binomial coefficients cancel between numerator
and denominator, which yields Eq. (5). Given yk , the repair      confidence level at which repairing stops paying off. Because
transition is conditionally independent of the history Hk , so    b⋆ ranges from 0.954 (favorable) down to 0.289 (stress), the
Pr(yk+1 =1 | Hk , repair) = (1 − β)bk + α(1 − bk ); this          same confidence can mean continue in one setting and stop
is the prediction step. Subtracting the current belief from       in another, so no fixed round budget or universal confidence
the predictive belief gives Eq. (6). Setting Gk = 0 yields        threshold is safe across settings.
the boundary b⋆ = α/(α + β) of Eq. (7), which is also the
fixed point of the affine map b 7→ (1 − β)b + α(1 − b) and
coincides with the fixed point of the population dynamics in         This bound is conservative relative to the exact tail prob-
the motivation subsection of the main text. Under a nonzero             PThe exact value is the finite sum Pr[S(p) − S(c) ≥
                                                                  ability.
threshold, Gk > τ is equivalent to bk < b⋆τ = (α − τ )/(α +       δ] = i−j≥δ Pr[S(p)=i] Pr[S(c)=j]. Substituting the cal-
β). Fig. 6 illustrates the geometry of this boundary with three   ibrated values of each verifier in Table 5 (M = 8, δ = 5),
empirically measured repair operators.                            the single-round erroneous-replacement probabilities are
                                                                  5.6×10−6 for Qwen-3B, 1.0×10−6 for Qwen-7B, 5.3×10−5
A.2    Proof of Proposition 1                                     for Mistral, and 5.9 × 10−3 for Llama; even in the worst case
                                                                  of near-zero J, the five-round union bound does not exceed
Let E = {|Ĝk − Gk | ≤ Bk }; by the definition of Bk ,            3%.
Pr(E) ≥ 1 − η. If Ĝk − Bk > τ , then on E we have
Gk ≥ Ĝk − Bk > τ , so the true action and the estimated          A.4                         Calibration Estimators and Identifiability
action are both Repair. If Ĝk + Bk ≤ τ , then on E we have
Gk ≤ Ĝk + Bk ≤ τ , so both are Commit. In either case the        Calibration from repeated verification records treats the
two actions agree with probability at least Pr(E) ≥ 1 − η,        round-1 acceptance counts as a two-component binomial
which completes the proof.                                        mixture, S ∼ π Bin(M, 1 − ρ1 ) + (1 − π) Bin(M, ρ0 ). The
                                                                  E-step of expectation-maximization (EM) computes each
A.3    Proof and Numerical Evaluation of Lemma 1                  plan’s responsibility of belonging to the valid component,
                                                                  and the M-step updates the mixture weight and the two
Suppose the current candidate c is truly valid and the            acceptance rates from responsibility-weighted frequencies;
new plan p is truly invalid; then S(p) ∼ Bin(M, ρ0 ) and          after multiple random restarts the solution with the high-
S(c) ∼ Bin(M, 1 − ρ1 ), and the two are independent               est log-likelihood is retained, and the component labels are
given the true states. Pairing the m-th queries, the differ-      fixed by the convention that the component with the higher
ences Xm = a(m) (p) − a(m) (c) ∈ [−1, 1] are i.i.d. with          acceptance rate corresponds to the valid class. The mixture
E[Xm ] = ρ0 − (1 − ρ1 ) = −J. Applying Hoeffding’s in-            is identifiable if and only if the two component acceptance
                  PM
equality to D = m=1 Xm gives Pr(D − E[D] ≥ t) ≤                   rates differ, that is, J ̸= 0. As J → 0 the likelihood sur-
exp(−t2 /(2M )); taking t = M J + δ ≥ 0 yields the single-        face flattens and the estimator no longer carries information
round bound, and the statement over Kmax rounds follows           about ρ0 , ρ1 ; this is exactly the mechanism behind the failure
from a union bound, which completes the proof.                    of calibrated stopping in the Llama scenario. The transition
parameters are estimated from labeled pre/post-repair plan           Algorithm 1 VRR-Stop with the guarded fallback (intended
pairs: α̂ is the frequency of invalid-to-valid transitions and β̂    deployment procedure; experiments evaluate the two modes
the frequency of valid-to-invalid transitions. The prior π̂ is       separately on saved trajectories)
the validity rate of initial plans on the calibration folds, and
                                                                     Require: plan p0 ; calibrated π̂, ρ̂0 , ρ̂1 , α̂, β̂; thresholds
all estimation is performed outside the held-out folds of the
                                                                         τ, η, Jmin ; margin δ; budgets M, Kmax
cross-fitting.
                                                                      1: mode ← Stop if labeled-sample diagnostic gives Jˆ ≥
A.5    Error Radius and Sample Complexity                                Jmin else Guard
                                                                      2: b− ← π̂; c ← p0 ; Sc ← −∞
The error radius Bk is constructed by propagating confi-              3: for k = 0, 1, . . . , Kmax do
dence bounds on the calibrated estimates through Eq. (5)              4:    query the verifier M times on pk and collect Sk
and the expression for Ĝk , taking the worst-case excur-             5:    bk ← posterior update of b− with Sk {Eq. (5)}
sion of Ĝk over the endpoints of each parameter interval.            6:    if Sk ≥ Sc + δ then
In an idealized single-query loop, the calibration sample             7:       c ← pk ; Sc ← Sk {keep-best tracking, Eq. (9)}
size required for the stopping sign to be identifiable satis-         8:    end if
fies N ≳ C1 log(1/δc )/(M J 2 ∆2 ), where δc is the allowed           9:    if mode = Stop then
failure probability. This bound is derived under the idealized       10:       Ĝk ← (1 − bk )α̂ − bk β̂; construct Bk
single-query loop; we do not claim a corresponding explicit          11:       if Ĝk + Bk ≤ τ then
bound for the deployed rule, and decision reliability under          12:          return pk {commit, stop sign identifiable}
deployment conditions is characterized directly by the flip-         13:       else if Ĝk − Bk ≤ τ then
risk simulation in the identifiability experiments of the main       14:          mode ← Guard {sign not identifiable, Eq. (8)}
text.                                                                15:       end if
                                                                     16:    end if
A.6    Formal Definitions of Baselines and                           17:    if k = Kmax then
       References                                                    18:       return pk if mode = Stop else c
No-repair commits p0 directly. Fixed-K repairs uncondition-          19:    end if
ally for K rounds and then commits pK . Majority stopping            20:    pk+1 ← repair pk with verifier feedback
commits the current plan when Sk > M/2 and otherwise                 21:    b− ← (1 − β̂)bk + α̂(1 − bk ) {predict step}
keeps repairing until the budget is exhausted. ConfStop-             22: end for
τconf replaces the commit condition with Sk /M ≥ τconf .
Accepted-first commits the first candidate on the trajec-
tory that receives majority acceptance, and commits the fi-          to stabilize the acceptance-rate estimates, whereas the end-
nal round at budget exhaustion when no round is majority-            to-end loop issues M = 8 queries per round; the two share
accepted. Last-accepted commits the last majority-accepted           the same verifier configuration. The calibration stage uses at
candidate, and commits the initial plan when no round is             most 300 labeled samples.
accepted. Verifier-best-of-trajectory commits the candidate
                                                                        Construction of evaluation settings. The favorable set-
with the highest acceptance count, breaking ties toward the
                                                                     ting is the standard generate-verify-repair loop without per-
earlier round. The true-parameter myopic (TPM) reference
                                                                     turbation. In the prompt-mismatch (PM) stress setting, the
executes the same myopic stopping rule as VRR-Stop but
                                                                     copy of the problem statement received by the repairer
with the true loop parameters (ρ0 , ρ1 , α, β, π); it isolates the
                                                                     is injected with numeric- or condition-level perturbations,
effect of calibration error on the decisions and is not a hind-
                                                                     while the verifier and the ground-truth judgment always use
sight policy that selects trajectories after observing ground
                                                                     the original statement; the repairer can therefore produce
truth. Hindsight best-round selection picks the best round on
                                                                     plausible-looking but incorrect revisions from a corrupted
each trajectory according to the true labels; it serves only
                                                                     premise. The repair temperature is 1.0 in the stress setting
as a trajectory-structure diagnostic and is not deployable.
                                                                     and 0.7 elsewhere. The main text’s non-stationarity diagnos-
The stationarity and independence assumptions of the four-
                                                                     tic adds two further constructions: initial drafts are generated
parameter model are local approximations; their scope of
                                                                     under a 256-token budget, and perturbations are injected
validity and failure modes are discussed in Appendix H.
                                                                     from round 3 onward and run through round 6.
                                                                        Calibration protocol and cross-fitting. To prevent the
            B     Full Experimental Setup                            same instance from being used both for parameter estima-
This appendix provides the complete experimental setup re-           tion and for stopping evaluation, the VRR-Stop results and
quired for auditing and reproduction; the runtime environ-           the true-parameter myopic (TPM) reference reported in the
ment, random seeds, and prompt templates are given in Ap-            main text both use five-fold cross-fitting: the stopping de-
pendix J.                                                            cision for each instance uses only the ρ0 , ρ1 , α, β and prior
  Task windows and verifiers. Table 4 lists the verifier             parameters estimated from the other four folds. Decisions
type, evaluation windows, and label source of each task; the         from the five held-out folds are pooled at the instance level
verifier for MATH-500 is a process reward model (PRM).               before computing the final validity and the mean number of
The calibration probe issues 16 verification queries per plan        repair rounds; the random seed of the fold split is fixed and
released with the replay artifacts. In-sample calibration re-              Table 4: Datasets, verifiers, and evaluation windows. Probe
sults serve only as a sensitivity audit, not as the deployment             windows feed the calibration probe (16 votes per plan); e2e
protocol. The prior π̂ is the frequency estimate of the true               and stress windows feed end-to-end evaluation (M =8).
validity rate of initial plans on the calibration folds. The tran-
sition parameters are estimated from the pre/post plan pairs                                Task            Verifier type              Windows (N )
of the first repair round on the frozen trajectories; during                                GSM8K           LLM judge     probe 300 / e2e 200
data generation, repair was triggered in every round without                                                              stress 200, 500
verifier gating, so the transition samples are free of selection                            MATH-500 PRM                  500
bias induced by the acceptance signal.                                                      MBPP     LLM judge            150
   Definition of shift scenarios. Each shift scenario reruns                                BFCL     LLM judge / executor 400 / 199
the entire loop (generation, repair, and judging) on the target
model or task. The shift codes in Table 2 mark the dominant                                1.0
change dimension of each scenario relative to the Qwen-3B                                                          Qwen-3B stress   Qwen-7B stress   Mistral stress

baseline: M denotes a change of generator family or scale, V                                         Favorable
a change of verifier family, and T a change of task together                               0.5
with its accompanying verifier; the evaluation protocol and
the calibration pipeline remain unchanged. The generator and
verifier models of each setting are listed in Table 3.                                     0.0




                                                                           true validity
                                                                                           1.0
Table 3: Generator and verifier models of each evaluation                                         Llama stress     MATH-500         BFCL single      BFCL multi
setting. In every shift scenario the whole loop (generation,
repair, and judging) runs on the target models; the shift codes                            0.5
of Table 2 mark the dominant change dimension relative to
the Qwen-3B baseline.
                                                                                           0.0
 Setting               Generator                 Verifier                                        0    2          5 0   2       5 0      2         5 0     2           5
 Qwen-3B fav./stress (–) Qwen2.5-3B-Instruct      same model (LLM judge)                                                   repair round
 Qwen-7B stress (M)      Qwen2.5-7B-Instruct      same model (LLM judge)
 Mistral-7B stress (V)   Mistral-7B-Instruct-v0.3 same model (LLM judge)
 Llama-3-8B stress (M) Llama-3-8B-Instruct        same model (LLM judge)   Figure 7: Mean true validity per repair round when every plan
 MATH-500 (T)            Qwen2.5-Math-7B-Instruct Qwen2.5-Math-PRM-7B      is repaired unconditionally, averaged over each trace’s eval-
 BFCL single (T)         Qwen2.5-7B-Instruct      same model (LLM judge)
 BFCL multi (T)          Qwen2.5-7B-Instruct      official executor
                                                                           uation window; the eight panels are the settings of Table 5.
                                                                           Round 0 equals the no-repair baseline and round k equals the
                                                                           fixed-budget value Fixed K=k, so each curve traces the full
   Hyperparameters. End-to-end evaluation uniformly uses                   path between the two extremes reported in the tables. Six
M = 8, Kmax = 5 (the non-stationarity diagnostic runs                      settings collapse within the first rounds and never recover,
through round 6), τ = 0, δ = 5, and B = 10,000 bootstrap                   BFCL multi-turn stays flat, and only the favorable setting
resamples. The coverage level η is a confidence parameter                  improves.
of the reliability-analysis layer and does not enter end-to-
end deployment. Only two hyperparameters were tuned: the
retention margin δ was swept over {0, . . . , 8} by pure replay            rises monotonically, and BFCL multi-turn, which is approx-
on all seven settings, selecting the value most robust across              imately flat, true validity declines monotonically with the
settings, and the calibration sample size was examined over                round index in the remaining six settings; the damage prob-
Ncalib ∈ {50, 100, 200, 300}. The remaining settings were                  ability β ranges from 0.615 to 0.938 and is typically several
fixed a priori and not tuned: M = 8 and Kmax = 5 follow                    times the repair probability α, so the stopping boundary b⋆
common verify-repair budgets, τ = 0 by definition of the                   is pushed below 0.29. The MATH-500 row shows that a
cost-free objective, and systematic sweeps of M and τ are                  strong verifier (J = 0.77) does not prevent a high-β repairer
left to future work (Appendix I). A manifest mapping each                  from damaging correct plans, whereas the near-inert oper-
figure and table of the main text to its raw data artifacts is             ator of BFCL multi-turn (α = 0.02, β = 0.04) provides a
released with the anonymous code repository.                               counterexample of multi-round repair without collapse. The
                                                                           finite-trace diagnostic in the last column shows that, outside
   C       Full Loop Dynamics and Failure Cases                            the flat setting, the gap between myopic stopping and the
This appendix examines whether the phenomenon of RQ1                       hindsight best round is at most 4 percentage points. Fig. 7
persists across settings and unfolds the complete chain of a               plots the per-round true-validity trajectories of all settings.
harmful repair on a single instance.
                                                                           C.2                   A Representative Failure Trace
C.1        Cross-Setting Loop Dynamics                                     Table 5 and Fig. 4 give the aggregate view; this section un-
Table 5 summarizes the round-1 parameter estimates and                     folds the same mechanism on a single instance. The pattern
trajectory shapes of the eight settings on their respective                is not a hand-picked pathology: on the N = 500 stress traces,
evaluation windows. Apart from the favorable setting, which                the round-1 validity of 0.70 drops to 0.25 after a single re-
Table 5: Full loop dynamics across the eight settings, where PM-stress denotes the prompt-mismatch stress setting. All parameters
are per-call round-1 estimates on each trace’s evaluation window (the Qwen2.5-3B PM-stress row uses the N =500 window),
b⋆ = α/(α + β) is the stopping boundary of Eq. (7), and the last column is a finite-trace diagnostic rather than a formal
dynamic-programming regret. Read each row by weighing repair α against damage β: wherever β dominates, b⋆ collapses
toward zero and the trajectory shape turns into a monotone decline, so harmful repair is the rule across the stress rows rather
than an exception.

    Setting       Model                 Verifier     ρ0      ρ1     J       α       β     b⋆ (Eq. 7)     Shape      Best-K − myopic
    Favorable     Qwen2.5-3B          LLM judge    0.438   0.169   0.39   0.423   0.020     0.954      monotone ↑        0.025
    PM-stress     Qwen2.5-3B          LLM judge    0.364   0.177   0.46   0.320   0.786     0.289      monotone ↓        0.016
    PM-stress     Qwen2.5-7B          LLM judge    0.725   0.048   0.23   0.000   0.909     0.000      monotone ↓        0.000
    PM-stress     Mistral-7B          LLM judge    0.707   0.111   0.18   0.014   0.862     0.015      monotone ↓        0.040
    PM-stress     Llama-3-8B          LLM judge    0.358   0.609   0.03   0.051   0.938     0.051      monotone ↓        0.000
    MATH-500      Qwen2.5-Math-7B       PRM        0.109   0.118   0.77   0.020   0.617     0.031      monotone ↓        0.000
    BFCL single   Qwen2.5-7B          LLM judge    0.875   0.057   0.07   0.147   0.615     0.192      monotone ↓        0.027
    BFCL multi    Qwen2.5-7B           Executor    0.659   0.223   0.12   0.048   0.037     0.564         flat          −0.015


pair round, 55% of instances experience a correct plan being            denotes the difference relative to the true-parameter myopic
repaired into an incorrect one, and 24% of these damaging               (TPM) reference. The three families of baselines exhibit a
repairs receive majority acceptance among the eight judg-               clear stratification. Heuristic stopping rules that rely solely on
ments. All of these are raw-label statistics, independent of            the verifier signal approach but never exceed no-repair (Ma-
the stopping rule and its calibration. The trace comes from             jority stopping and Accepted-first both at 0.690, Verifier-best
GSM8K test instance #292 (Qwen2.5-3B, M = 8 judgments                   at 0.696); confidence-threshold stopping and Last-accepted
per round); the complete causal chain is shown in Fig. 8.               degrade moderately (0.562 and 0.504); fixed-budget repair
   As shown in Fig. 8, the initial plan correctly derives 75            collapses severely and worsens monotonically with the bud-
dollars from 150/10 = 15 billing intervals, yet receives                get (0.246, 0.122, and 0.116 for K = 1, 3, 5). VRR-Stop
only four of the eight votes and suffers a false rejection. The         at 0.722 is the only deployable strategy that exceeds both
upstream perturbation corrupts only the repairer’s copy of              the no-repair baseline and the TPM reference. The reference
the problem statement, changing every 10 minutes to every               row at the bottom of the table is diagnostic only and is not
17 minutes; the repairer then competently rewrites the plan             deployable.
from the corrupted premise into an incorrect answer of 40                  Sample size and multi-window replication. On the
dollars, and the verifier, which judges against the uncorrupted         N = 200 window of the same setting, VRR-Stop attains
original problem, instead gives it six votes and commits it.            0.705 (95% CI [0.640, 0.765], ⟨K⟩ = 0.82) against a TPM
True validity flips from 1 to 0 while the reported acceptance           reference of 0.695, directionally consistent with 0.722 versus
rises. This is the trade-off between the repair benefit (1−bk )α        0.694 at N =√500; the confidence intervals shrink by roughly
and the damage loss bk β of the belief-filtering subsection             a factor of 2.5, and the strategy ranking is unchanged.
of the main text unfolding on a single instance: a high-β               Across three disjoint GSM8K windows, calibrated stopping
rewrite compounded by the missed detection of a verifier                attains 0.752 ± 0.037, the TPM reference 0.757 ± 0.058,
false acceptance.                                                       and fixed 5-round repair 0.118 ± 0.007. Calibrated stopping
   The case text is taken from a replay capture of the stress-          and the reference strategy alternate in per-window ranking;
setting pipeline, and a second instance exhibits the same type          the two are close but not identical, which is the expected
of chain; both full transcripts (including the eight judgment           behavior of a calibration that tracks the true parameters.
responses per round, the two candidate solutions, and the                  Cross-model and cross-domain replication. The
exact repair prompts) are released with the anonymous code              Qwen2.5-7B stress setting exhibits the largest collapse in
repository. Per-instance sampling is not bitwise reproducible           the paper: fixed 5-round repair falls from the no-repair level
across inference-engine versions, so the case cites the replay          of 0.875 to 0.075, whereas VRR-Stop preserves 0.875 with
transcripts rather than the original frozen trajectories; the           zero repair rounds on average, matching the TPM reference;
aggregate conclusions are unaffected.                                   in this setting, calibrated stopping learns not to repair at all.
                                                                        On MBPP, under both the favorable and the stress settings,
    D    Full Stopping and Cross-Benchmark                              calibrated stopping coincides with the TPM reference (0.533
                                                                        and 0.493, respectively), remaining stable across domains
                       Results                                          and calibration protocols.
This appendix examines the stability of the RQ2 conclusions                Direct comparison with iterative-feedback baselines.
across additional baselines, larger samples, different models,          Under the fixed-budget deployment mode of the stress set-
and different tasks; all numbers are reported under the five-           ting, Reflexion and Self-Refine reach final validities of 0.095
fold cross-fitting protocol.                                            and 0.080, whereas VRR-Stop on the same trajectories at-
   Full baselines. Table 6 completes the full set of compar-            tains 0.740 and 0.710 (TPM reference: 0.710 and 0.705).
ison strategies on the stress setting of Table 1, where ∆V              This comparison audits the fixed-budget deployment mode
                                                   original problem — what the veriﬁer always grades


                                                                                         corrupted copy: 'every 10 minutes' → 'every 17 minutes'

                                                                                                                               REPAIR UNDER A CORRUPTED
          USER TASK                           ROUND 0: GENERATE + VERIFY                                                                                                                                                          ROUND 1: VERIFY + COMMIT
                                                                                                                                        PREMISE

                                                  Planner         [1] 2.5 h = 150 min;
        Susan earns $5 every 10 min-
        utes for an online task. She                              [2] 150 / 10 = 15;
                                                                                                                                                    Repairer      Premise corruption
                                                                                                                                                                                                                                     Veriﬁer
                                                                                                                                                                                                                                                                     still grades the
        works between 8 a.m. and 11                                                                                                                                                                                                                                 ORIGINAL problem
                                               LLM planner
                                                                  [3] billable intervals;                                                                       (repairer's copy only)
        a.m. and pauses in between for                                                                                                                                                                                            LLM veriﬁer
                                               generates          [4] 15 × $5 = $75;                            rejected
                                                                                                                                    LLM repairer
                                                                                                                                                                                                              revised
        half an hour. How much money                                                                              plan                                                                                          plan

        does she earn?                                           Initial plan            (true invalid)
                                                                                                                                                                                                                                               Veriﬁer votes(6/8 accept)
                                                                                                                                                                                                                        Veriﬁer      Veriﬁer    Veriﬁer   Veriﬁer    Veriﬁer    Veriﬁer   Veriﬁer   Veriﬁer

                                                                                                                                                                 [1] 150 / 17 = 8 remainder 14;
                                              falsely           Veriﬁer votes(4/8 accept)                                                                        [2] '8 full intervals at $5 each give $40;
                                             REJECTED                                                                           Repairer
                                                                                                                                                                 [3] the leftover 14 minutes earn nothing.
                   Gold answer: $75                                 Veriﬁer    Veriﬁer     Veriﬁer    Veriﬁer



                                                                                                                                                                 [4] ........
                                                                                                                                                                                                                                                 falsely                        $40 (wrong)
                                            sent to repair         Veriﬁer    Veriﬁer     Veriﬁer    Veriﬁer               LLM repairer
                                                                                                                                                                     Revised plan         (true valid)                                          ACCEPTED
                                                                                                                                                                      deviates from the gold answer.



                             True validity: 1 → 0 (falls)                                                                                                                       Reported acceptance: 4/8 → 6/8 (rises)


Figure 8: End-to-end failure trace of GSM8K instance #292. The two top rails show the fork that drives it: the original problem
(blue, solid) is what the verifier always grades, while the corrupted copy (amber, dashed) that turns every 10 minutes into every
17 minutes reaches only the repairer. A valid plan under-accepted at 4/8 is competently rewritten from the corrupted premise
into an invalid one, which the verifier accepts at 6/8 and commits to the user, so true validity falls from 1 to 0 while reported
acceptance rises.


of iterative feedback and does not claim to reproduce the full                                                                                                 (a) Per-plan rates                                                              (b) Distributions
                                                                                                                                                      1.00                                                                                                Invalid (n=79)
training details of the original methods.                                                                                                                                                                                            8
                                                                                                                                                                                                                                                          Valid (n=221)
                                                                                                                             acceptance rate k/16

E    Full Calibration and Identifiability Results                                                                                                     0.75
                                                                                                                                                                                                                                     6
This appendix examines when the parameter estimates can be




                                                                                                                                                                                                                        density
trusted, when they fail, and locates the mechanism of failure.                                                                                        0.50
                                                                                                                                                                                                                                     4
   Cross-family calibration stress. Table 7 shows that the
dominant calibration bias points in a different direction
                                                                                                                                                      0.25
for each of the four verifiers: the Qwen family underesti-                                                                                                                                                                           2
                                                                                                                                                                                          True
mates the false-acceptance rate, Llama underestimates the
                                                                                                                                                                                          EM
false-rejection rate, and the false-acceptance bias of Mistral                                                                                        0.00                                                                           0
reaches 0.66. Decision consequences are decoupled from                                                                                                              Invalid                         Valid                                      0.0                             0.5                            1.0
bias magnitude: the largest bias, on Mistral, costs only 0.3                                                                                                                                                                                    acceptance rate k/16
percentage points, whereas the smaller bias on Llama pro-
duces a 58.0-point collapse; the dividing line is the discrim-                                                               Figure 9: Per-plan judge acceptance on the N =300 probe
ination ability J, not the bias itself. Fig. 9 supplies the up-                                                              window (M =16), split by true validity, shown as per-plan
stream evidence for all of this: on the probe window, re-                                                                    rates with class means in panel (a) and as class distributions
peated verification yields acceptance-rate distributions for                                                                 in panel (b). Solid lines mark the true mean acceptance of
the two classes that overlap yet remain separable, which is                                                                  each class and dashed lines the label-free EM estimates; EM
why weakly supervised calibration is feasible—and why it is                                                                  recovers the valid-class rate almost exactly (0.91 vs 0.88)
fragile.                                                                                                                     but underestimates the invalid-class rate (0.23 vs 0.49), the
   Identifiability collapse on Llama. Table 8 exposes                                                                        dominant source of downstream calibration error. The two
the failure mechanism. Binomial expectation-maximization                                                                     classes overlap yet remain separable, which is why weakly
(EM) yields ρ̂1 = 0.27 at N = 120, yet increasing the sam-                                                                   supervised calibration is feasible but fragile.
ple to 300 worsens the estimate to 0.077: as J approaches
zero the likelihood surface flattens, and additional samples
only make EM converge more confidently to a degenerate                                                                       identifiable-fraction grids underlying Fig. 5 are released with
solution. The capped beta-binomial estimator gives 0.620 at                                                                  the anonymous code repository.
N = 120 but is unstable across random seeds. A parameter
sweep under the deployed rule completes the picture: cali-
brated decisions recover the stop-early optimum only when                                                                                                                F          Full Robustness Results
ρ̂1 is no lower than 0.30 to 0.35, with the midpoint crossing                                                                This appendix examines whether the gains of VRR-Guard are
at ρ̂1 ≈ 0.17, so the EM estimate of 0.077 sits deep in the                                                                  confined to a single scenario and delineates the boundaries
collapse zone.                                                                                                               of its costs.
   Stopping-decision agreement numbers for the estimator-                                                                       Full results. Table 9 extends Table 2 with the TPM refer-
input ablation are given in Appendix I; the flip-rate and                                                                    ence column and replay bootstrap intervals for Guard. VRR-
Table 6: Full stopping results on the GSM8K / Qwen2.5-3B prompt-mismatch stress setting (N =500); ∆V is measured against
the TPM reference (positive = better), verifier-only baselines are offline replays on the same saved trajectories, and the final
row is a non-deployable diagnostic. VRR-Stop is the only deployable strategy above both the no-repair baseline and the TPM
reference.

                                  Method                           V [95% CI]        ⟨K⟩     ∆V (pp)
                                  No repair                      0.700 [.658,.740]   0.00     +0.6
                                  Majority stopping              0.690 [.648,.730]   0.92     −0.4
                                  ConfStop-0.85                  0.562 [.518,.604]   1.92     −13.2
                                  Fixed repair K=1               0.246 [.208,.284]   1.00     −44.8
                                  Fixed repair K=3               0.122 [.094,.152]   3.00     −57.2
                                  Fixed repair K=5               0.116 [.088,.144]   5.00     −57.8
                                  Accepted-first                 0.690 [.648,.730]   0.92     −0.4
                                  Last-accepted                  0.504 [.460,.546]   2.28     −19.0
                                  Verifier-best-of-trajectory    0.696 [.654,.736]   0.73     +0.2
                                  VRR-Stop                       0.722 [.682,.760]   0.72     +2.8
                                  TPM reference                  0.694 [.652,.734]   0.89      0.0

Table 7: Cross-family calibration stress (per-row N is each trace’s evaluation window, J uses the family-level convention, and
Gap is Vstop − VTPM in percentage points; the TPM reference is not a hindsight upper bound). Dominant bias reports the largest
EM estimation error as estimate minus truth, so negative values are underestimates. Decision damage tracks J rather than the
size of the dominant calibration bias.

                         Judge           Family     N       J      Dominant bias     Vstop    VTPM     Gap (pp)
                         Qwen2.5-7B      Qwen      200    0.23     ∆ρ0 = −0.29       0.875    0.875    +0.0
                         Qwen2.5-3B      Qwen      500    0.46     ∆ρ0 = −0.19       0.722    0.694    +2.8
                         Mistral-7B      Mistral   300    0.18     ∆ρ0 = −0.66       0.463    0.467    −0.3
                         Llama-3-8B      Llama     300    0.03     ∆ρ1 = −0.53       0.223    0.803    −58.0


Table 8: Identifiability collapse on the Llama-3-8B judge               free Verifier-best on the same trajectories, Guard is 45.0
(target ρ1 = 0.609). Under the deployed rule, a parameter               percentage points higher in the Llama scenario (95% CI
sweep shows calibrated stopping recovers the stop-early op-             [+39.0, +51.0]), while the differences in the remaining set-
timum only for ρ̂1 ≳ 0.30–0.35 with the midpoint crossing               tings lie between −4.0 and +8.0 percentage points. The
at ρ̂1 ≈ 0.17, so the EM estimate of 0.077 sits deep in the             retention margin δ is nearly neutral in most scenarios; its
collapse zone.                                                          value is realized precisely where the verifier signal is least
                                                                        trustworthy.
  Estimator                   ρ̂1 (N =120)     ρ̂1 (N =300)                A no-collapse counterexample, and cost. Under the
  Binomial EM                     0.27             0.077                near-inert repair operator of BFCL multi-turn (α = 0.02,
  Capped beta-binomial EM        0.620        unstable (seed)           β = 0.04), all strategies coincide within confidence inter-
                                                                        vals: multi-round repair is not inherently harmful, and severe
                                                                        degradation appears only together with a high break proba-
                                                                        bility. Regarding cost, each round consumes a fixed M veri-
Guard stays near the no-repair level in all seven settings,
                                                                        fication calls and at most one repair call, so the cost ordering
whereas fixed 5-round repair degrades sharply in every set-
                                                                        of the strategies is exactly the ⟨K⟩ ordering reported in each
ting except favorable. The Mistral row also provides a direct
                                                                        table; VRR-Guard operates by replaying saved trajectories
counterexample showing that the TPM reference is not a
                                                                        and incurs no additional verification calls.
hindsight upper bound: its 0.467 falls below the no-repair
0.507. Fig. 10 places the repair cost and true validity of two
representative scenarios on the same plane.                                           G      Paired Statistical Tests
   Honest boundaries. Guard does not dominate every-                    This appendix provides same-trajectory paired statistical sup-
where. On Mistral and BFCL it falls below no-repair by                  port for the percentage-point claims in the main text. All
2.0 and 0.3 percentage points, with paired intervals of                 comparisons are paired per instance on the same batch of
[−3.7, −0.7] and [−1.3, +0.5] respectively, the latter con-             task instances and saved repair trajectories; differences in
taining zero (Appendix G). Under the favorable setting,                 true validity are assessed with 10,000 instance-level boot-
Guard’s 0.81 is below the 0.875 of fixed 5-round repair—                strap resamples, directional binary comparisons use exact
the opportunity cost of conservatism in a scenario where                McNemar tests, and a positive ∆V indicates that the left-
repair helps.                                                           hand strategy is better on the same instances. The decision
   Role of the retention margin. Compared with margin-                  sequences of VRR-Stop and the TPM reference follow the
Table 9: Full guarded-stopping results with the TPM reference column and replay bootstrap CIs; shift codes M, V, and T mark
a change of model family, verifier family, or task relative to the Qwen-3B baseline. The TPM reference is a diagnostic rather
than a hindsight upper bound (note Mistral: TPM 0.467 < No repair 0.507). VRR-Guard stays within a few points of no-repair
in every row, including the Llama row where calibrated stopping collapses.

                          Setting                                J        No repair            Fixed K=5   VRR-Stop     TPM ref.   VRR-Guard      Guard 95% CI
                          Qwen-3B favorable (–)                 0.39          0.740                0.875    0.845        0.850        0.810         [.755,.865]
                          Qwen-3B stress (–)                    0.46          0.700                0.116    0.722        0.694        0.742         [.702,.780]
                          Qwen-7B stress (M)                    0.23          0.875                0.075    0.875        0.875        0.875         [.825,.920]
                          Mistral-7B stress (V)                 0.18          0.507                0.047    0.463        0.467        0.487         [.430,.543]
                          Llama-3-8B stress (M)                 0.03          0.803                0.057    0.223        0.803        0.793         [.747,.837]
                          MATH-500 (T)                          0.22          0.798                0.150    0.798        0.798        0.796         [.760,.832]
                          BFCL single (T)                       0.07          0.812                0.372    0.782        0.780        0.810         [.770,.848]


                      (a) Qwen-3B stress                         (b) Llama stress                          estimates.
                0.9                                                   No repair
                                        VRR-Stop
                       VRR-Guard                                              TPM                          H.1      Repair Benefit and Damage Risk
                                         TPM
                                                                       VRR-Guard                           Whether to continue repairing depends on the relative mag-
                                         Majority                                                          nitude of the repair benefit and the damage loss, not on the
                0.6    No repair
                                   Verifier-best                                                           number of repair rounds already executed. By Eq. (6), the
                                               ConfStop-0.85
true validity




                                                                                                           true marginal gain of a single repair round is

                                                                               Verifier-best
                                                                                                                              Gk = (1 − bk )α − bk β.
                                                                                                           The first term captures the expected benefit of an invalid plan
                0.3             Fixed K=1                                          VRR-Stop
                                                                                  Majority
                                                                                                           becoming valid through repair, and the second term captures
                                                                        Fixed K=1
                                                                                                           the expected loss of a valid plan being damaged by repair.
                                         Fixed K=3
                                                                                       ConfStop-0.85       Even under the same maximum repair budget, different val-
                                                                           Fixed K=3
                                                Fixed K=5                                                  ues of bk , α, β yield different optimal stopping times; verifier
                                                                                        Fixed K=5          noise ρ0 , ρ1 shifts this timing indirectly through the posterior
                0.0
                      0     1       2       3       4       5     0       1       2    3       4     5     belief bk .
                          mean repair rounds                           mean repair rounds                     The results in Appendix C exhibit pronounced differences
                                                                                                           across settings. In the GSM8K stress setting and on MATH-
Figure 10: True validity versus mean repair rounds for each                                                500, the repairer rarely corrects invalid plans yet frequently
stopping strategy under a working calibration (a, Qwen-3B                                                  damages valid ones: fixed five-round repair reduces true va-
stress) and a failed one (b, Llama stress); up-left is better, and                                         lidity from 0.700 to 0.116 and from 0.798 to 0.150, respec-
the hollow marker is the ground-truth-parameter diagnostic                                                 tively. BFCL multi-turn instead shows nearly inert repair
TPM rather than a deployable strategy. Fixed-budget repair                                                 dynamics, with α = 0.02 and β = 0.04, and no statis-
forms a dominated slide that pays more rounds for less va-                                                 tically distinguishable difference among stopping policies.
lidity, and in panel (b) calibrated VRR-Stop itself falls into                                             This counterexample shows that multi-round repair is not in-
that region while VRR-Guard stays at the no-repair corner.                                                 herently harmful; substantial degradation emerges only when
The pair thus covers both regimes, with calibrated stopping                                                the repairer has a non-negligible capacity to damage valid
earning the low-cost, high-validity corner when calibration                                                states.
holds and the guarded fallback keeping that corner when it                                                    Verifier discrimination ability and repairer safety also re-
fails.                                                                                                     quire separate examination. On GSM8K, the process re-
                                                                                                           ward model verifier Qwen2.5-Math-PRM-7B (Zhang et al.
                                                                                                           2025b) attains a Youden’s index of J = 0.805 (this setting
same cross-fitting protocol as the main text.                                                              uses Qwen2.5-3B as the generator and is independent of the
                                                                                                           MATH-500 row in Table 5), yet the stronger verifier does not
                                                                                                           prevent the repairer from damaging correct plans. In this set-
                                H        Extended Discussion                                               ting, fixed five-round repair still reduces validity from 0.727
This appendix elaborates on applicability conditions and                                                   to 0.097, whereas the true-parameter myopic (TPM) refer-
method boundaries that the main text does not cover in de-                                                 ence remains at 0.663. Improving verifier quality therefore
tail, including how harmful repair arises, how calibration                                                 strengthens the reliability of stopping decisions but cannot
error affects stopping decisions, the failure modes of differ-                                             eliminate the risk introduced by the repair operation itself.
ent verifiers, and the benefits and costs of the conservative
fallback strategy. A common thread across the subsections is                                               H.2      Non-Stationarity and Interior Peaks
that calibration quality should be measured by whether the                                                 The repairer’s state-transition probabilities may change
decision sign flips, not by the absolute error of parameter                                                across rounds. In the favorable setting of Qwen2.5-3B, the re-
Table 10: Paired replay statistics for load-bearing comparisons. Positive ∆V means the left strategy has higher true validity on
the same saved instances. Every headline percentage claim in the main text maps to one row of this table.

         Section / setting      Comparison                                   ∆V [95% paired CI]               Paired test
         RQ1 interior peak      round 2 vs final round                    +0.747 [+0.693, +0.797]        paired bootstrap
         RQ1 interior peak      round 0 vs final round                    +0.327 [+0.257, +0.397]        paired bootstrap
         RQ2 Qwen-3B stress     VRR-Stop vs Fixed-K=5                     +0.606 [+0.560, +0.650]     McNemar p < 2 × 10−85
         RQ2 Qwen-3B stress     VRR-Stop vs ConfStop-0.85                 +0.160 [+0.126, +0.194]     McNemar p < 1 × 10−18
         RQ2 Qwen-3B stress     VRR-Stop vs Majority stopping             +0.032 [+0.016, +0.050]     McNemar p < 2 × 10−4
         RQ2 Qwen-3B stress     VRR-Stop vs TPM reference                 +0.028 [+0.014, +0.044]     McNemar p < 6 × 10−4
         RQ2 Qwen-3B stress     VRR-Stop vs No repair                     +0.022 [−0.004, +0.048]        paired bootstrap
         RQ3 Llama stress       VRR-Stop vs TPM reference                 −0.580 [−0.637, −0.520]     McNemar p < 2 × 10−48
         RQ4 Llama stress       VRR-Guard vs failed VRR-Stop              +0.570 [+0.510, +0.627]     McNemar p < 1 × 10−47
         RQ4 Llama stress       VRR-Guard vs Fixed-K=5                    +0.737 [+0.683, +0.787]     McNemar p < 2 × 10−62
         RQ4 Llama stress       VRR-Guard vs Verifier-best (unguarded)    +0.450 [+0.390, +0.510]        paired bootstrap
         RQ4 Mistral stress     VRR-Guard vs No repair                    −0.020 [−0.037, −0.007]        paired bootstrap
         RQ4 BFCL               VRR-Guard vs No repair                    −0.003 [−0.013, +0.005]        paired bootstrap


pair success rate under the per-round convention drops from              stays in the same decision region, so the final action does not
0.415 in the first round to 0.032 in the fifth (Table 5 reports          change.
a first-round value of 0.423 under the per-call convention),                Llama-3-8B exhibits the opposite outcome. Its verifier
while the damage probability stays low throughout. This pat-             discrimination ability is only J = 0.03, and the binomial-
tern admits a natural interpretation: easily repairable errors           mixture estimate underestimates the false-rejection rate by
are eliminated first, and the remaining errors are harder to             about 0.53, which systematically inflates the posterior belief
fix. Describing the entire repair process with transition prob-          bk and thus substantially underestimates the damage risk rep-
abilities estimated from the first round should therefore be             resented by bk β. The estimation error eventually crosses the
regarded only as a locally stationary approximation.                     stopping boundary, driving VRR-Stop down to 0.223 from
   The non-stationarity diagnostic trajectory in the main                the TPM reference of 0.803. The direct cause of the degrada-
text’s loop-dynamics experiment further illustrates the in-              tion is not the parameter bias itself but the fact that the bias
terior peak that repair can produce. Early repair completes              flips the decision sign between continuing and stopping.
initial solutions truncated by the generation-length limit, rais-           BFCL single-call provides further corroboration. Its ver-
ing true validity to 0.87 at round two. After context drift is           ifier has a J of only 0.07, but the states it visits carry large
introduced at round three, true validity gradually declines to           decision margins, and VRR-Stop differs from the TPM refer-
0.12. This trajectory demonstrates that the optimal submis-              ence by only 0.3 percentage points. A uniform trust threshold
sion time can occur at an intermediate round, but it does not            therefore cannot be set from the J value alone. The controlled
imply that a stopping policy based on stationary parameters              experiment shown in Fig. 5 likewise indicates that when low
can necessarily locate that peak. In paired replay, VRR-Stop             J coincides with a low decision margin ∆, the sign-flip rate
and the TPM reference attain 0.693 and 0.720 (cross-fitted               reaches 0.183, whereas it is only 0.014 in regions with high J
convention), both far below the 0.867 obtained by post hoc               or high ∆. The reliability of stopping decisions is jointly de-
selection of round two.                                                  termined by verifier discrimination ability, decision margin,
   This result delineates the capability boundary of the cur-            and calibration sample size.
rent method. VRR-Stop judges whether one more repair
round still yields a positive gain under the current local               H.4    Family-Conditional Verifier Failures
model; it does not search the full trajectory for the post hoc           The current experiments further show that different model
optimal round. When the repair mechanism changes abruptly                families can exhibit different directions of verifier failure.
at some round, α and β estimated from the first round can-               Across the eight Qwen configurations, the binomial-mixture
not represent this change in advance. The interior-peak ex-              estimate underestimates the false-acceptance rate in every
periment thus both confirms the necessity of the stopping                case, with ∆ρ0 ranging from −0.16 to −0.31 (the full list
problem and indicates room for further research on round-                of biases is released with the anonymous code repository).
dependent dynamic models.                                                For Llama-3-8B, the false-acceptance rate is estimated es-
                                                                         sentially accurately, but the false-rejection rate is markedly
H.3    Decision Robustness under Calibration Error                       underestimated (by about 0.53 at N =300). Mistral-7B in-
Parameter estimation error affects the stopping action only              stead shows a pronounced tendency toward false acceptance,
when it changes the sign of Gk − τ . For Mistral-7B, the                 with a true false-acceptance rate of about 0.71, yet its large
estimation bias of the false-acceptance rate reaches ∆ρ0 =               decision margin prevents the stopping sign from flipping.
−0.66, yet VRR-Stop attains a true validity of 0.463, within                These results indicate that verifier noise should not be
0.3 percentage points of the TPM reference at 0.467. Despite             treated as a fixed bias transferable across models. The same
the large parameter error, the corresponding marginal gain               calibration method can underestimate the false-acceptance
rate in one model family and the false-rejection rate in an-      Qwen2.5-3B clearly violates it. Conclusions on that trajec-
other, and the two biases propagate through the posterior         tory therefore rest on single-round marginal gains and finite-
belief into Eq. (6) in different directions. That said, the       trajectory diagnostics rather than on global monotonicity.
existing experiments cover only three model families, and         The TPM reference likewise serves only to isolate decision
some configurations share tasks and samples. These findings       differences caused by parameter calibration; it is not a glob-
should therefore be read as family-conditional patterns ob-       ally optimal upper bound over the finite horizon. Post hoc
served within the current experimental scope, not as universal    selection of the best round can be used to analyze trajectory
laws determined by model architecture.                            structure but cannot serve as a deployable policy.
   The process reward model and the executors used in our ex-        Deploying VRR-Stop should begin with estimating the
periments also impose different calibration conditions. A de-     noise parameters and their error ranges from repeated ver-
terministic verifier produces no new stochastic observations      ification records and a small number of labeled transition
under repeated queries on the same plan, so the binomial-         samples. Only when Ĝk − Bk > τ or Ĝk + Bk ≤ τ does the
mixture estimate based on repeated acceptance counts cannot       available evidence suffice to support a definite continue or
be applied directly. The stopping criterion itself remains ap-    stop action. If the confidence interval straddles the stopping
plicable in this case, but ρ0 and ρ1 must be estimated directly   boundary, or if the model, verifier, or task distribution shifts,
from a small number of labeled samples.                           the system should switch to VRR-Guard or recollect labeled
                                                                  samples for recalibration. Existing parameters should not be
H.5    Safety and Upside of the Guarded Fallback                  transferred directly to a new model family, verifier, or repair
When Eq. (8) fails to hold, VRR-Guard no longer relies            prompt.
on precise noise parameters; instead, it raises the evidential       Future work can model round-dependent αt and βt to de-
strength required to replace the current candidate. The policy    tect late context drift and interior peaks. The binary true state
retains the best candidate so far and performs a replacement      can also be extended to multi-level plan quality, describing
only when the verification acceptance count of a new candi-       partial correctness and distinct error types. Another direc-
date exceeds that of the current one by at least δ. It does not   tion is to estimate instance-conditional noise that depends
prevent the system from generating subsequent candidates;         on plan features, so that plans of different difficulty receive
it avoids committing a possibly degraded repair result when       different stopping boundaries. Finally, per-instance marginal
the evidence is insufficient.                                     gains can support cross-task compute allocation, selecting
   In the Llama-3-8B scenario, VRR-Guard restores true va-        the instances most worth further repair when the total infer-
lidity to 0.793, an improvement of 57.0 percentage points         ence budget is limited.
over the failed VRR-Stop and 73.7 percentage points over
fixed five-round repair. When unsupervised calibration ap-                       I    Additional Ablations
proaches non-identifiability, retaining the existing candidate
is thus more robust than continuing to rely on erroneous          This appendix reports sensitivity analyses that have already
parameters.                                                       been run and can be replayed at zero cost.
   This robustness comes with an observable opportunity              Calibration-input ablation. In the GSM8K stress set-
cost. In the favorable setting, VRR-Guard reaches a validity      ting, the final validity under three calibration inputs—
of 0.810, below the 0.875 of fixed five-round repair. In the      binomial expectation-maximization (EM), method of mo-
Mistral-7B and BFCL settings, VRR-Guard falls short of no-        ments (MoM), and labeled maximum-likelihood estimation
repair by 2.0 and 0.3 percentage points, respectively, and the    (MLE)—is 0.722, 0.690, and 0.690, respectively, with the
paired interval for BFCL contains zero. VRR-Guard therefore       differences in stopping decisions concentrated on a few bor-
carries no theoretical guarantee of strictly dominating no-       derline instances. Beta-binomial EM (BB-EM) yields 0.666
repair. It is better viewed as a conservative fallback close      (95% CI [0.624, 0.706], ⟨K⟩ = 1.26): its overly flexible fit
to the no-repair baseline: it bounds the downside risk when       pushes ρ̂0 up to 0.508, which systematically depresses the
calibration is unreliable, at the cost of forgoing part of the    posterior belief and induces excessive repair. Table 8 pro-
potential benefit in scenarios where repair is beneficial.        vides a comparative diagnosis of the two EM variants under
                                                                  within-class heterogeneity.
H.6    Scope and Deployment Implications                             Retention-margin ablation. A pure replay sweep over
This work represents whether a plan is truly valid with a         δ ∈ {0, . . . , 8} (M = 8) across all seven settings shows
binary state. This binary validity representation suits tasks     that δ = 5 is the most robust choice, trailing the per-setting
with well-defined labels, such as answer correctness, tool        optimal δ by at most 4.0 percentage points in any setting.
executability, and constraint satisfaction, but it cannot fully      Calibration-sample-size sensitivity. Under subsampled
describe partial correctness, multiple error types, or long-      re-estimation with Ncalib ∈ {50, 100, 200, 300}, the decision
horizon plans with staged goals. For such tasks, the state        agreement rate rises from 0.973 to 0.997, the sign-flip rate
space needs to be extended to multi-level or structured rep-      falls from 0.016 to 0.002, and the absolute validity gap to
resentations, and the corresponding stopping boundary may         the TPM reference shrinks from 0.012 to 0.001. Systematic
no longer be given by a single threshold.                         ablations of the verification budget M and the gain threshold
   The strict condition α + β ≤ 1 holds on seven of the eight     τ were not run within the scope of this work and are left for
empirical trajectories, but the GSM8K stress trajectory of        future work.
             J    Reproducibility Details                           Gou, Z.; Shao, Z.; Gong, Y.; Shen, Y.; Yang, Y.; Duan, N.; and
All experiments were run on a single server equipped with           Chen, W. 2024. CRITIC: Large Language Models Can Self-
eight NVIDIA A800 80GB PCIe GPUs, with each ex-                     Correct with Tool-Interactive Critiquing. In The Twelfth In-
periment completed on a single GPU. The software en-                ternational Conference on Learning Representations (ICLR).
vironment comprises Ubuntu 22.04, CUDA 12.8, PyTorch                OpenReview.net.
2.10.0 (cuDNN 9.10.2), and the inference engine vLLM                Grattafiori, A.; Dubey, A.; Jauhri, A.; Pandey, A.; Kadian,
0.19.1 (Kwon et al. 2023). The temperature for generation,          A.; Al-Dahle, A.; et al. 2024. The Llama 3 Herd of Models.
judging, and repair is 0.7, with the repair temperature raised      CoRR, abs/2407.21783.
to 1.0 in the stress setting. Code versions, random seeds, the      Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart,
complete generation, judging, and repair prompts for each           S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measuring
task, and an index of raw data files are released with the          Mathematical Problem Solving With the MATH Dataset. In
anonymous code repository. True validity is adjudicated by          Vanschoren, J.; and Yeung, S., eds., Proceedings of the Neu-
exact match on GSM8K, symbolic verification on MATH-                ral Information Processing Systems Track on Datasets and
500, sandboxed unit tests on MBPP (5-second timeout), and           Benchmarks 1 (NeurIPS Datasets and Benchmarks 2021).
abstract syntax tree (AST) matching plus the official executor      Huang, J.; Chen, X.; Mishra, S.; Zheng, H. S.; Yu, A. W.;
on BFCL; Appendix B describes how the generator prior is            Song, X.; and Zhou, D. 2024. Large Language Models Can-
obtained.                                                           not Self-Correct Reasoning Yet. In The Twelfth International
   Per-instance LLM trajectories are single stochastic real-        Conference on Learning Representations (ICLR). OpenRe-
izations and are not bit-wise reproducible across inference-        view.net.
engine versions. All numbers in this paper are computed by          Jiang, A. Q.; Sablayrolles, A.; Mensch, A.; Bamford, C.;
deterministic replay of frozen trajectories and do not depend       Chaplot, D. S.; de las Casas, D.; Bressand, F.; Lengyel, G.;
on regeneration.                                                    Lample, G.; Saulnier, L.; Lavaud, L. R.; Lachaux, M.-A.;
                                                                    Stock, P.; Le Scao, T.; Lavril, T.; Wang, T.; Lacroix, T.; and
                         References                                 El Sayed, W. 2023. Mistral 7B. CoRR, abs/2310.06825.
Austin, J.; Odena, A.; Nye, M.; Bosma, M.; Michalewski, H.;         Kamoi, R.; Das, S. S. S.; Lou, R.; Ahn, J. J.; Zhao, Y.; Lu,
Dohan, D.; Jiang, E.; Cai, C.; Terry, M.; Le, Q.; and Sutton,       X.; Zhang, N.; Zhang, Y.; Zhang, R. H.; Vummanthala, S. R.;
C. 2021. Program Synthesis with Large Language Models.              Dave, S.; Qin, S.; Cohan, A.; Yin, W.; and Zhang, R. 2024a.
arXiv:2108.07732.                                                   Evaluating LLMs at Detecting Errors in LLM Responses. In
                                                                    First Conference on Language Modeling (COLM).
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;
Kaiser, L.; Plappert, M.; Tworek, J.; Hilton, J.; Nakano, R.;       Kamoi, R.; Zhang, Y.; Zhang, N.; Han, J.; and Zhang, R.
Hesse, C.; and Schulman, J. 2021. Training Verifiers to Solve       2024b. When Can LLMs Actually Correct Their Own Mis-
Math Word Problems. arXiv:2110.14168.                               takes? A Critical Survey of Self-Correction of LLMs. Trans-
                                                                    actions of the Association for Computational Linguistics, 12:
Collot, S.; Fraser, C.; Zhao, J.; Shen, W. F.; Willi, T.; and       1417–1440.
Leontiadis, I. 2026. Balanced Accuracy: The Right Metric
for Evaluating LLM Judges - Explained through Youden’s J            Khalaf, H.; Verdun, C. M.; Oesterling, A.; Lakkaraju, H.; and
statistic. In Matusevych, Y.; Eryiğit, G.; and Aletras, N., eds.,   Calmon, F. d. P. 2025. Inference-Time Reward Hacking in
Proceedings of the 19th Conference of the European Chapter          Large Language Models. In Advances in Neural Information
of the Association for Computational Linguistics (Volume 5:         Processing Systems 38 (NeurIPS 2025). Spotlight.
Industry Track), 927–936. Rabat, Morocco: Association for           Khalifa, M.; Agarwal, R.; Logeswaran, L.; Kim, J.; Peng, H.;
Computational Linguistics. ISBN 979-8-89176-384-5.                  Lee, M.; Lee, H.; and Wang, L. 2026. Process Reward Models
                                                                    That Think. Transactions on Machine Learning Research.
Dorner, F. E.; Chen, Y.; Cruz, A. F.; and Yang, F. 2026. ROC-
n-reroll: How Verifier Imperfection Affects Test-Time Scal-         Kumar, A.; Zhuang, V.; Agarwal, R.; Su, Y.; Co-Reyes, J. D.;
ing. In The Fourteenth International Conference on Learning         Singh, A.; Baumli, K.; Iqbal, S.; Bishop, C.; Roelofs, R.;
Representations (ICLR).                                             Zhang, L. M.; McKinney, K.; Shrivastava, D.; Paduraru, C.;
                                                                    Tucker, G.; Precup, D.; Behbahani, F.; and Faust, A. 2025.
Feng, C.; Shen, M.; Balashankar, A.; Gerner-Beuerle, C.;            Training Language Models to Self-Correct via Reinforce-
and Rodrigues, M. R. D. 2026. Noisy but Valid: Robust Sta-          ment Learning. In The Thirteenth International Conference
tistical Evaluation of LLMs with Imperfect Judges. In The           on Learning Representations (ICLR). OpenReview.net.
Fourteenth International Conference on Learning Represen-
                                                                    Kwon, W.; Li, Z.; Zhuang, S.; Sheng, Y.; Zheng, L.; Yu, C. H.;
tations (ICLR). ArXiv:2601.20913.
                                                                    Gonzalez, J. E.; Zhang, H.; and Stoica, I. 2023. Efficient
Fu, Y.; Wang, X.; Tian, Y.; and Zhao, J. 2026. Deep Think           Memory Management for Large Language Model Serving
with Confidence. In The Fourteenth International Confer-            with PagedAttention. In Flinn, J.; Seltzer, M. I.; Druschel, P.;
ence on Learning Representations (ICLR).                            Kaufmann, A.; and Mace, J., eds., Proceedings of the 29th
Gao, L.; Schulman, J.; and Hilton, J. 2023. Scaling Laws for        Symposium on Operating Systems Principles (SOSP ’23),
Reward Model Overoptimization. In Proceedings of the 40th           611–626. Koblenz, Germany: ACM. ISBN 9798400702297.
International Conference on Machine Learning, volume 202            Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
of Proceedings of Machine Learning Research.                        B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
K. 2024. Let’s Verify Step by Step. In The Twelfth Inter-       Yang, Z.; Zhang, Y.; Wang, Y.; Xu, Z.; Lin, J.; and Sui, Z.
national Conference on Learning Representations (ICLR).         2025. A Probabilistic Inference Scaling Theory for LLM
OpenReview.net.                                                 Self-Correction. In Proceedings of the 2025 Conference on
Lu, J.; Teehan, R.; Jin, J.; and Ren, M. 2025. When Does        Empirical Methods in Natural Language Processing, 13573–
Verification Pay Off? A Closer Look at LLMs as Solution         13587. Suzhou, China: Association for Computational Lin-
Verifiers. arXiv:2512.02304.                                    guistics.
Madaan, A.; Tandon, N.; Gupta, P.; Hallinan, S.; Gao, L.;       Ye, Z.; Melo, L. C.; Kaddar, Y.; Blunsom, P.; Staton, S.;
Wiegreffe, S.; Alon, U.; Dziri, N.; Prabhumoye, S.; Yang,       and Gal, Y. 2025. Uncertainty-Aware Step-wise Verification
Y.; Gupta, S.; Majumder, B. P.; Hermann, K.; Welleck, S.;       with Generative Reward Models. In ICLR 2025 Workshop
Yazdanbakhsh, A.; and Clark, P. 2023. Self-Refine: Itera-       on Quantify Uncertainty and Hallucination in Foundation
tive Refinement with Self-Feedback. In Oh, A.; Naumann,         Models.
T.; Globerson, A.; Saenko, K.; Hardt, M.; and Levine, S.,       Yu, F.; Li, Y.; and Wang, B. 2025. Scaling Flaws
eds., Advances in Neural Information Processing Systems,        of Verifier-Guided Search in Mathematical Reasoning.
volume 36, 46534–46594. Curran Associates, Inc.                 arXiv:2502.00271.
Pan, A.; Jones, E.; Jagadeesan, M.; and Steinhardt, J. 2024a.   Zhang, L.; Hosseini, A.; Bansal, H.; Kazemi, M.; Kumar,
Feedback Loops With Language Models Drive In-Context            A.; and Agarwal, R. 2025a. Generative Verifiers: Reward
Reward Hacking. In Proceedings of the 41st International        Modeling as Next-Token Prediction. In The Thirteenth Inter-
Conference on Machine Learning, volume 235 of Proceed-          national Conference on Learning Representations (ICLR).
ings of Machine Learning Research, 39154–39200. PMLR.           OpenReview.net.
Pan, J.; He, H.; Bowman, S. R.; and Feng, S. 2024b.             Zhang, Z.; Zheng, C.; Wu, Y.; Zhang, B.; Lin, R.; Yu, B.;
Spontaneous Reward Hacking in Iterative Self-Refinement.        Liu, D.; Zhou, J.; and Lin, J. 2025b. The Lessons of Develop-
arXiv:2407.04549.                                               ing Process Reward Models in Mathematical Reasoning. In
                                                                Che, W.; Nabende, J.; Shutova, E.; and Pilehvar, M. T., eds.,
Patil, S. G.; Mao, H.; Cheng-Jie Ji, C.; Yan, F.; Suresh, V.;   Findings of the Association for Computational Linguistics:
Stoica, I.; and E. Gonzalez, J. 2025. The Berkeley Func-        ACL 2025, 10495–10516. Vienna, Austria: Association for
tion Calling Leaderboard (BFCL): From Tool Use to Agen-         Computational Linguistics. ISBN 979-8-89176-256-5.
tic Evaluation of Large Language Models. In Forty-second
International Conference on Machine Learning.                   Zhao, E.; Awasthi, P.; and Gollapudi, S. 2025. Sample, Scru-
                                                                tinize and Scale: Effective Inference-Time Search by Scal-
Platanios, E. A.; Blum, A.; and Mitchell, T. M. 2016. Es-       ing Verification. In Proceedings of the 42nd International
timating Accuracy from Unlabeled Data: A Bayesian Ap-           Conference on Machine Learning, volume 267 of Proceed-
proach. In Proceedings of the 33rd International Conference     ings of Machine Learning Research. Vancouver, BC, Canada:
on Machine Learning, volume 48 of Proceedings of Machine        PMLR.
Learning Research.
                                                                Zhong, J.; Li, Z.; Xu, Z.; Wen, X.; Li, K.; and Xu, Q. 2025.
Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and       Solve-Detect-Verify: Inference-Time Scaling with Flexible
Yao, S. 2023. Reflexion: Language Agents with Verbal Rein-      Generative Verifier. arXiv:2505.11966.
forcement Learning. In Oh, A.; Naumann, T.; Globerson, A.;
                                                                Zhou, Y.; Xu, A.; Wang, P.; Xiong, C.; and Joty, S. 2025.
Saenko, K.; Hardt, M.; and Levine, S., eds., Advances in Neu-
                                                                Evaluating Judges as Evaluators: The JETTS Benchmark of
ral Information Processing Systems, volume 36, 8634–8652.
                                                                LLM-as-Judges as Test-Time Scaling Evaluators. In Pro-
Curran Associates, Inc.
                                                                ceedings of the 42nd International Conference on Machine
Stroebl, B.; Kapoor, S.; and Narayanan, A. 2026. The Limits     Learning, volume 267 of Proceedings of Machine Learning
of Inference Scaling Through Resampling. In The Four-           Research. Vancouver, BC, Canada: PMLR.
teenth International Conference on Learning Representa-
tions (ICLR).
Sun, R.; Cheng, W.; Li, D.; Chen, H.; and Wang, W. 2026.
Stop When Enough: Adaptive Early-Stopping for Chain-of-
Thought Reasoning. In Proceedings of the 64th Annual
Meeting of the Association for Computational Linguistics.
San Diego, California, USA: Association for Computational
Linguistics. ArXiv:2510.10103.
Wang, X.; Wei, J.; Schuurmans, D.; Le, Q.; Chi, E.; Narang,
S.; Chowdhery, A.; and Zhou, D. 2023. Self-Consistency
Improves Chain of Thought Reasoning in Language Mod-
els. In The Eleventh International Conference on Learning
Representations (ICLR). OpenReview.net.
Yang, A.; Yang, B.; Zhang, B.; Hui, B.; Zheng, B.; Yu, B.;
Li, C.; Liu, D.; Huang, F.; Wei, H.; et al. 2024. Qwen2.5
Technical Report. arXiv:2412.15115.
