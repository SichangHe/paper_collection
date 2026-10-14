                                                          Proof-Carrying Cognition:
                                           Closing the Verification Gap with Reality-Settled Reward

                                                  Eshwar Reddy M                                                 Sourav Karmakar
                                                AI Engineer, Testsigma                                      Senior AI Scientist, Intuit India
                                                University of San Diego
                                           malireddy.eshwar@gmail.com                                  souravkarmakar29@gmail.com


                                        Abstract                                                    exchange rate ρ is not quantitatively predictive,
arXiv:2609.09776v1 [cs.AI] 9 Sep 2026




                                                                                                                                 2
                                                                                                    and the closed form N 1/ρ overstates the penalty
                                        Recent frontier progress in large language models           at practical N (the exact finite-N form of Proposi-
                                        has come predominantly from reinforcement learn-            tion 1 predicts matching budgets to within 3.4%).
                                        ing on reasoning traces—and has been sharply con-           (2b) Real-model evidence: in pre-registered ex-
                                        centrated in domains that possess a cheap, sound            periments with a real frontier-family generator, real
                                        verifier. We argue that the field’s binding con-            LLM judges, and real unit-test execution as gold,
                                        straint is therefore the verification gap: the ab-          the weak judge loses soundness under best-of-N
                                        sence of a scalable, incorruptible source of reward         on both MBPP and HumanEval (p < 10−3 ); a
                                        for reasoning outside narrowly formal domains.              stronger judge is significantly more robust—so the
                                        We make four contributions. (1) Theory: in a                gap binds conditionally on judge capability relative
                                        joint-Gaussian model of best-of-N selection we              to task difficulty; a learned settlement model an-
                                        prove that verifier–gold correlation ρ is the exact         chored to executed outcomes cuts the judge’s pric-
                                        exchange rate between test-time compute and capa-           ing error by 59%, while naive in-context anchoring
                                        bility, and that an unsound verifier must pay a poly-       makes it worse; and a prompt-level LLM adver-
                                                                         2
                                        nomial compute penalty N 1/ρ to match a sound               sary failed to inflate the judge—while mining the
                                        one. (2) Demonstration: in program-synthesis                same candidate banks shows selection alone manu-
                                        testbeds with an executable ground truth—a mini-            factures +0.53 hacking gaps from honest samples:
                                        mal six-token domain and a pre-registered scaled            the operative Goodhart pressure is selection, not
                                        replication in a ∼ 1010 -program domain with                persuasion. A pre-registered diagnosis of every
                                        2–4× more tasks and stronger instruments—we                 failure yields a repaired, margin-free exchange-
                                        show that unsound verifiers lose Soundness-under-           rate law (the copula form predicts realized sound-
                                        Pressure as optimization pressure grows (from 0.94          ness of real LLM judges to 4% median error) and
                                        to 0.32 for a shallow verifier at N =4096), collaps-        a design constraint for the paradigm: average-
                                        ing absolutely in the small domain and plateauing           calibration anchoring provably cannot move sound-
                                        in the rich one, while a sound verifier improves            ness and empirically amplifies tail deceptions—the
                                        monotonically; that reality-anchored settlement             world model must match the expressiveness of the
                                        beats a frozen verifier under both i.i.d. and di-           deception surface. (3) Paradigm: we propose
                                        rected adversarial pressure, including against an           proof-carrying cognition, a training loop in which
                                        adversary that explicitly models the settlement pro-        reasoning steps are emitted as typed probabilistic
                                        cess, driving the hacking gap from ∼ 0.27 to ∼ 0;           claims, priced by a self-built world model whose
                                        that soundness scales log-linearly with settled la-         only loss is prediction of held-out reality, and set-
                                        bels, with on-policy settlement ∼ 10× more label-           tled by strictly proper scoring rules—making re-
                                        efficient than random labeling and decisively bet-          ality, rather than human judgment, the ultimate
                                        ter than an uncertainty-sampling control; and that          reward function. (4) Benchmark: we specify
                                        settlement improves the resolution of claims, not           Soundness-under-Pressure, the headline metric for
                                        merely their calibration. The replication also fal-         a reality-settled reasoning benchmark, and argue
                                        sified two of our quantitative claims, which we             that building this benchmark is the field’s single
                                        report and repair: outside the Gaussian model the

                                                                                                1
most important near-term action. (2c) Under real                    Corollary 1); simulation matches theory to
GRPO training, a frozen learned RM traces the                       within 0.011σ (Figure 1).
full overoptimization curve—proxy reward climbs
                                                                  • Demonstration (§6–§7).           In program-
while executed reward collapses by 90%—and the
                                                                    synthesis testbeds with an executable gold
identical RM refit on a 10% settlement stream pre-
                                                                    verifier: learned verifiers are Goodharted un-
serves executed reward at 6× the frozen arm’s and
                                                                    der best-of-N pressure (relative soundness
outperforms an equal-budget LLM-judge-updated
                                                                    0.94 → 0.32 at scale; absolute collapse in
control, isolating reality as the label source; the
                                                                    the minimal domain) while a sound verifier
registered drift-alarm criterion failed its first test
                                                                    climbs monotonically; reality-anchored set-
and is reported as such.
                                                                    tlement beats a frozen verifier under directed
1    Introduction                                                   adversarial pressure, including a settlement-
                                                                    aware adversary, driving the hacking gap to
Two inventions define modern machine learning:
                                                                    ∼ 0; verifier soundness scales log-linearly
backpropagation, which solved credit assignment
                                                                    with settled labels, with on-policy settlement
over parameters (Rumelhart et al., 1986), and the
                                                                    ∼ 10× more label-efficient than random la-
transformer, which solved bandwidth over context
                                                                    beling; and settlement raises claim resolution,
(Vaswani et al., 2017). We argue that the next
                                                                    rebutting the concern that settlement-based
invention of comparable consequence must solve
                                                                    reward favors vague claims. §7 reports a pre-
credit assignment over thoughts: determining, scal-
                                                                    registered scaled replication, including the
ably and incorruptibly, whether a step of reasoning
                                                                    parts of our story it falsified.
is correct.
   The argument proceeds from an empirical ob-                    • Paradigm (§5). We propose proof-carrying
servation. Frontier capability gains now come pre-                  cognition (Algorithm 1): reasoning as portfo-
dominantly from reinforcement learning on chains                    lios of falsifiable, priced claims, with reality
of thought (Wei et al., 2022; OpenAI, 2024; Guo                     as the only unamortized loss.
et al., 2025), and these gains are sharply concen-
                                                                  • Benchmark (§9). We give a formal met-
trated in domains with a cheap, sound verifier:
                                                                    ric, Soundness-under-Pressure, and a con-
mathematics with checkable answers (Hendrycks
                                                                    struction recipe for a reality-settled reasoning
et al., 2021), code with executable tests (Chen
                                                                    benchmark.
et al., 2021), and formal proof with a kernel
(Trinh et al., 2024; AlphaProof and AlphaGeome-               Scope note: this is a hybrid position-and-proof-of-
try teams, Google DeepMind, 2024). The underly-               concept paper. The experiments in §3–§6 are real
ing recipe—sample many traces, keep those a veri-             and reproducible but deliberately minimal; they
fier accepts, reinforce (Zelikman et al., 2022)—is            validate mechanisms, not frontier-scale claims.
a self-improvement engine whose throttle is veri-
fier coverage. Where the verifier is sound, months            2     The Bottleneck: Generation Has Scaled;
of training have produced superhuman-adjacent                       Verification Has Not
performance. Where the only reward is a human
                                                              2.1    The verification gap
preference label (Christiano et al., 2017; Ouyang
et al., 2022) or an LLM judge, the same models                Define a verifier for a domain D as an oracle V :
plateau at fluent but unaccountable reasoning, be-            claims(D) → [0, 1] that is (a) sound—its accep-
cause preference-based reward is noisy, gameable,             tances track ground truth; (b) cheap—evaluating
and shallower than the reasoning it evaluates (Gao            V costs far less than generating a candidate; and
et al., 2023).                                                (c) robust under optimization—an adversarially
   This paper names that constraint the verification          trained generator cannot systematically obtain re-
gap and attacks it from four directions:                      ward from V for false claims. The verification
                                                              gap is the observation that such oracles exist today
    • Theory (§3). We prove that in best-of-N                 only for formally grounded domains (proof kernels,
      selection, verifier–gold correlation ρ is the ex-       program execution, game rules), and that every
      change rate between compute and capability,             substitute used elsewhere—human raters, reward
      with an unsound verifier paying a polynomial            models, LLM judges—fails property (c) under suf-
                     2
      penalty N 1/ρ in candidates (Proposition 1,             ficient optimization pressure. Gao et al. (2023)

                                                          2
                                                                          that outruns
                                                                        verifier          scoresthe         verifier’s unaided
                                                                                                        highest—is            the canonical competence.
                                                                                                                                                     mecha-
  gold reward of selected ( )   verifier corr.                          nism by which test-time compute is converted into
         3                              = 1.0                             3 Theory: Verifier Correlation Is the
                                        = 0.8                           capability (Cobbe et al., 2021; Snell et al., 2024),
                                                                                   Compute–Capability Exchange Rate
                                        = 0.5                           and its induced optimization pressure grows as
         2                              = 0.2                             WeNfirst
                                                                        log        . make the cost of unsoundness quantita-
                                                                          tive
                                                                        Propositionin      the cleanest
                                                                                                     1 (Verifier    possible  exchangemodel.rate).Best-of-NLet
         1                                                              (Gi , Pi )i=1 be i.i.d. jointly Gaussian pairs, stan-the
                                                                          selection—sample
                                                                                         N                       N   candidates,           keep   the   one
                                                                          verifier scores
                                                                        dardized,             with Corr(G,highest—is    P ) =the         canonical
                                                                                                                                   ρ, where       G is mecha-
                                                                                                                                                         gold
         0                                                                nism        by     which       test-time
                                                                        reward and P the proxy verifier’s score. Let      compute          is converted       into
                 21       23     25      27        29 211               i capability
                                                                          ∗  = arg max            (Cobbe
                                                                                                    i Pi . Then
                                                                                                                et al., 2021; Snell et al., 2024),
               candidates N (optimization pressure)                       and      its      induced         optimization
                                                                                                                                      pressure grows as
                                                                          log N        .                                            √                         
                                                                        E[Gi∗ ] = ρ E max Pi = ρ 2 ln N 1+o(1) .
                                                                                                            i
 Figure 1: Simulation (dots; 20,000 trials per point) ver-                Proposition 1 (Verifier exchange rate). Let
Figure 1: Simulation (dots; 20,000 trials per point) ver-                                                                                     p
 sus theory (lines; ρ E[maxN ]) for best-of-N selection
                                                                                       i )i=1 be i.i.d.Gjointly                  Gaussian 1pairs,   − ρ2 stan-
                                                                         (G                 N
sus theory (lines; ρ E[maxN ]) for best-of-N selection Proof.                  i , PDecompose                       i = ρPi +                                Zi
 under a proxy verifier with correlation ρ to gold. Maxi-
under    a  proxy   verifier with  correlation    ρ  to gold.   Maxi-     dardized,
                                                                        with         Z           with
                                                                                               standard  Corr(G, Gaussian,P   )   =    ρ,  where
                                                                                                                                        independent G   is   gold
                                                                                                                                                             of
 mum absolute deviation from theory across all points:                                   i
mum      absolute   deviation   from   theory    across
 0.011σ. At N =4096, the ρ=0.5 verifier realizes 50.2%    all  points:  (Preward
                                                                            1 ,  . .  .  , P and
                                                                                               N  ).  P     the
                                                                                                          The      proxy
                                                                                                                   index        iverifier’s
                                                                                                                                  ∗   is   a     score.
                                                                                                                                              function       ofLet
0.011σ.      At N  =4096,    the ρ=0.5    verifier   realizes  50.2%      i ∗ = arg max P . Then
 of the sound verifier’s gain, matching Proposition 1 ex- (P1 , . . . , PN ) alone;                    i i        conditioning on these, Zi∗
of  the sound verifier’s gain, matching Proposition 1 ex-
 actly.                                                                                                   Gaussian       with mean zero, so
                                                                        remains standard                                               √                          
actly.
                                                                        E[Z
                                                                          E[G    ∗
                                                                                i i]∗  ]    =      ρ 0E   and
                                                                                                            max     E[G
                                                                                                                    P   i i∗=  ] ρ= 2 ln     ρ E[P     ] = .
                                                                                                                                                N i∗1+o(1)
                                                                                                               i
 2.2 Other bottlenecks reduce to it                                     √E[maxi Pi ]. The asymptotic E[max
                                                                        ρ                                                                          i Pi ] ∼
                                                                                                                                                 pfor Gaus-
quantified                                                                  2  ln    N      is   standard      extreme-value             theory
 The data the        failure
                 wall.         directly: optimizing
                           High-quality       human textagainst           Proof. Decompose Gi = ρPi + 1 − ρ2 Zi
                                                                is fi- sians.
anite,
   fixedbut learned   reward    model     yields    proxy
               self-generated data is unbounded—if it         reward      with Zi standard Gaussian, independent of
that
 can rises     while AlphaGo
        be trusted.    gold reward Zeropeaks     andetthen
                                           (Silver       al., falls—
                                                               2017) Corollary                      ). The index
                                                                         (P1 , . . . , P1N(Polynomial                      compute  i∗ ispenalty
                                                                                                                                              a function
                                                                                                                                                       of un-of
Goodhart’s        law   (Strathern,     1997)     operating
 showed that with a perfect verifier (game rules), soundness).    as  a  (P   1  , .  .  .  , P         alone;       conditioning
                                                                                                  NTo match the expected gold reward
                                                                                                    )                                         on   these,      Z i∗
hard    ceiling.    A  model    cannot    climb
 self-play alone yields superhuman skill with no    above    the   dis-   remains
                                                                        that     a sound       standard
                                                                                                    verifierGaussian
                                                                                                                 (ρ=1) attains      withwith mean N zero,
                                                                                                                                                      candi-so
crimination
 human data.ability        of its judge
                    AlphaProof              (Leike et
                                    (AlphaProof        andal.,Alpha-
                                                                2018; dates,
                                                                          E[Zi∗a] proxy                 0 andwith
                                                                                               = verifier              E[G  correlation
                                                                                                                               i ∗ ]     =      ρ E[P
                                                                                                                                                  requires
                                                                                                                                                        i∗ ]    =
Bowman
 Geometryet teams,
                 al., 2022).
                           Google DeepMind, 2024) ex-                     ρ E[maxi Pi ]. The2 asymptotic E[maxi Pi ] ∼
                                                                          √                    ′
 tended this to mathematics, reaching IMO silver-                             2 ln NN is=standard       N 1/ρ (asymptotically).
                                                                                                                        extreme-value theory for
2.2 Other bottlenecks reduce to it
 medal standard on millions of autoformalized prob-                       Gaussians. √                                          √
The
 lemsdata       wall. High-quality
          adjudicated      by the Leanhuman  kernel.textTheis finite,
                                                                 data   Proof. Set ρ 2 ln N ′ =                                     2 ln N and solve:
                                                                                 ′
                                                                        lnCorollary                     2 .
but
 wallself-generated
         is not a shortage  dataofistext;
                                      unbounded—if
                                            it is a shortage   it can
                                                                    of       N = ln N/ρ            1 (Polynomial              compute penalty of un-
be    trusted. reward
 trustworthy       AlphaGo       Zero (Silver
                            for synthetic            et al., 2017)
                                              reasoning.                  soundness).                 To    match        the    expected gold reward
                                                                             Two readings. First, within this model class,
showed that with a perfect verifier (game rules), verifier                that a sound verifier (ρ=1) attains with N candi-
 Unreliable agency. Long-horizon autonomy                                                correlation is the exchange rate between
self-play alone yields superhuman skill with no test-time                 dates, a proxy verifier with correlation ρ requires
 fails because errors compound with no mechanism                                             compute and capability: every unit of
human data. AlphaProof (AlphaProof and Alpha- inference compute
 to check intermediate steps before commitment. A                                            N ′ = Nis1/ρworth(asymptotically).
                                                                                                                              exactly ρ of its sound-
                                                                                                                    2

Geometry teams, Google DeepMind, 2024) ex- verifier value                                           (Figure       1  and     the     100,000-trial repli-
 sound step-level verifier converts open-loop gener-                                                   √                           √
tended this to mathematics, reaching IMO silver- cation                                of     §7
                                                                          Proof. Set ρ 2 ln N =      confirm        this
                                                                                                                      ′      to    within         and and
                                                                                                                                               0.011σ     solve:
 ation into closed-loop, auditable action.                                                                                             2 ln N
medal standard on millions of autoformalized prob- 0.007σ                 ln N =    ′    respectively).
                                                                                              ln N/ρ . Outside the model class the
                                                                                                           2
 Superhuman
lems    adjudicated   reasoning
                         by the Lean in kernel.
                                         open domains.
                                                    The data wall   In  identity is not quantitatively predictive in either
 science,     strategy,   law,  and   medicine,       humans
is not a shortage of text; it is a shortage of trust- direction:  can     Two readings.                   First, within
                                                                                               in the synthetic            testbedthis ofmodel
                                                                                                                                             §7, aclass,
                                                                                                                                                     verifierveri-
 no longer
worthy          reliably
            reward         grade superhuman
                      for synthetic     reasoning.homework; with          fier correlation
                                                                                   measured ρ is            ≈the 0.50 exchange
                                                                                                                          realizes rate  onlybetween
                                                                                                                                                 ≈ 0.32 of   test-
 scalable oversight
Unreliable       agency.(Amodei        et al., 2016;
                             Long-horizon        autonomyBowman  fails thetimesound verifier’s value at N =4096 (exploitablein-
                                                                                      compute            and      capability:            every     unit   of
 et  al., 2022)   is precisely   the  demand      for
because errors compound with no mechanism to structure verification       ference beyond     compute          is worthnoise),
                                                                                                          Gaussian             exactly       ρ ofreal
                                                                                                                                         while      itsLLM
                                                                                                                                                         sound-
 that outruns
check              the verifier’s
           intermediate      steps unaided      competence. A judges
                                     before commitment.                   verifier(§8)     value  with (Figure
                                                                                                          near-zero  1 and       the 100,000-trial
                                                                                                                            linear      correlation (ρrepli- ≈
sound step-level verifier converts open-loop gener- 0.12)                 cation   realizeof §70.74         at N =32
                                                                                                       confirm          this(good
                                                                                                                                to within top-ranking
                                                                                                                                                 0.011σde-    and
 3 Theory: Verifier Correlation Is the
ationCompute–Capability
         into closed-loop, auditable           action.                  spite
                                                                          0.007σ  poorrespectively).
                                                                                              linear fit). Only          the qualitative
                                                                                                                      Outside         the   modelordering—
                                                                                                                                                      class    the
                                         Exchange Rate
Superhuman reasoning in open domains. In higher-fidelity                  identity is not             judges      convert pressure
                                                                                                         quantitatively                       to capability
                                                                                                                                      predictive     in either
 We first strategy,
science,       make thelaw, costand
                                  of medicine,
                                      unsoundness         quantita-
                                                      humans      can better—survived
                                                                          direction: in theevery            synthetic testbed.testbed  Theofrepair
                                                                                                                                                §7, a(§8.1)
                                                                                                                                                        verifier
 tivelonger
no      in thereliably
                  cleanestgrade
                              possible    model. homework;
                                   superhuman           Best-of-N       iswith
                                                                             to statemeasured   the law   ρ≈  in 0.50
                                                                                                                   the invariant
                                                                                                                             realizes that  onlyselection
                                                                                                                                                   ≈ 0.32 of
 selection—sample
scalable                   N candidates,
              oversight (Amodei        et al.,keep
                                                 2016; theBowman
                                                            one the     actually
                                                                          the sound        sees: verifier’s value at N =4096 (exploitable
et al., 2022) is precisely the demand for verification                    structure beyond Gaussian noise), while real LLM

                                                                               3
judges (§8) with near-zero linear correlation (ρ ≈           and AlphaProof (AlphaProof and AlphaGeome-
0.12) realize 0.74 at N =32 (good top-ranking de-            try teams, Google DeepMind, 2024) are existence
spite poor linear fit). Only the qualitative ordering—       proofs that self-improvement loops close when the
higher-fidelity judges convert pressure to capability        verifier is sound. The kernel functions as a trust
better—survived every testbed. The repair (§8.1)             anchor—analogous to the small trusted computing
is to state the law in the invariant that selection          base of secure systems—from which learned ver-
actually sees:                                               ifiers extend coverage but to which they must be
                                                             re-anchored.
Proposition 2 (Margin-free exchange rate). Let
                                                             Process-level verification. Outcome reward is
          i=1 be i.i.d. with continuous margins
(Gi , Pi )N
                                                             sparse and rewards lucky wrong reasoning; step-
and Gaussian copula parameter ρc , and i∗ =
                                                             level reward is dense and localizes error. Process
arg maxi Pi .    Then the law of Gi∗ —hence
                                                             reward models outperform outcome-only supervi-
Snd@N —depends only on ρc and the margin of
                                                             sion on hard mathematics (Uesato et al., 2022;
G; the margin of P is irrelevant.
                                                             Lightman et al., 2024), extending Cobbe et al.
Proof. i∗ is invariant under strictly increasing             (2021), and verifier-guided search gives test-time
transforms of P , so transform P to standard Gaus-           compute its own scaling behavior (Snell et al.,
sian; the conditional law of G given the ranks of            2024)—which, by Proposition 1, is worth exactly
(P1 , . . . , PN ) is determined by the copula and G’s       as much as the verifier is sound.
margin.                                                      Adversarial prover–verifier co-training. Debate
                                                             (Irving et al., 2018) and prover–verifier games
   Estimating ρc from rank correlation and simulat-          (Kirchner et al., 2024) train generator and verifier
ing with empirical margins predicts per-problem              against each other; Kirchner et al. (2024) report
realized soundness with median error 4.1% on real            the property we most need—models trained to con-
LLM-judge data, where Pearson-based prediction               vince a weaker verifier produce reasoning that is
errs by 79 points (§8.1). Second, the penalty for            genuinely easier for humans to check.
unsoundness is superlinear in candidates. Two cau-           Limits. (1) Coverage: autoformalization of em-
                                  2
tions on the closed form N 1/ρ : it is asymptotic,           pirical claims (“this drug target is promising”) is
and at practical budgets it materially overstates the        unsolved. (2) Drift: learned verifiers degrade under
penalty (by up to 24× at ρ=0.5, N ≤ 16; §7). The             optimization pressure when the anchor is distant
exact finite-N consequence of Proposition 1—N ′              (Gao et al., 2023). (3) The legibility tax: checkable
solves ρ E[maxN ′ ] = E[maxN ]—predicts empiri-              formats may exclude valid intuitions that resist
cal matching budgets to within 3.4% and should be            formalization. These limits motivate our proposal.
used instead at finite N . We note honestly that this
linear-Gaussian model predicts a slowed climb, not           5     Proof-Carrying Cognition
the decline observed empirically under heavy opti-           We now state the central hypothesis of this paper.
mization (Gao et al., 2023); decline requires mis-           Hypothesis. Stop verifying reasoning against hu-
specification, and §7 shows it is domain-dependent:          man judgment. Verify it against predicted reality,
present in the minimal domain, absent (plateau in-           using a world model the system itself constructs
stead) in a richer one at the pressures we could             and is scored on—so that every chain of thought
apply.                                                       becomes a portfolio of falsifiable bets, and reality
4   The Validated Attack: Asymmetric Ver-                    becomes the reward function.
                                                                We call the paradigm proof-carrying cognition
    ification
                                                             (PCC), by analogy to proof-carrying code: an arti-
The strongest evidence-backed approach to the gap            fact is admitted not because an authority approves
exploits a structural asymmetry: checking is often           it, but because it carries the material needed to
far cheaper than generating—morally the P-versus-            check it. Science operates this way institutionally;
NP gap, and the only free lunch available to this            PCC makes an AI system’s internal reasoning op-
program. Three mechanisms have real support.                 erate this way, step by step, at training scale.
Formal grounding. Autoformalization (Wu et al.,
2022) lets a sound kernel adjudicate reasoning               5.1    Architecture and training loop
with zero Goodharting: a proof checker cannot                PCC has three components (Figure 2; Algo-
be flattered. AlphaGeometry (Trinh et al., 2024)             rithm 1).

                                                         4
                                                             Claim ledger
                                          emits                                        claims                  World model
                  Reasoner                             typed probabilistic claims:
                                                                                                         prices claims; trained only
           latent chain of thought                     causal edges, code, formal
                                                                                                             on held-out reality
                                                    statements, calibrated forecasts
                                                                         near-term prices                                 settled by

                                                                                                        Reality
                               reward                Internal prediction market
                                                                                              experiments, execution traces,
                                                  instances stake calibration capital;
                                                      proper scoring rules settle      anchors time-lagged observations


 Figure 2: Proof-carrying cognition. Reasoning steps are emitted as typed, probabilistic claims in a claim ledger. A
Figure    2: world
 self-built  Proof-carrying   cognition.
                   model prices           Reasoning
                                  claims densely  andsteps are emitted
                                                      immediately;       as typed,
                                                                     reality settlesprobabilistic
                                                                                     them sparselyclaims in a claim ledger.
                                                                                                    but incorruptibly, and
Atheself-built
      world model’s own loss is anchored exclusively to that settlement. Reward for reasoning is expectedincorruptibly,
               world model    prices  claims densely and  immediately;    reality settles them sparsely  but   score under
and   the scoring
 proper   world model’s   own
                  rules, not   lossapproval.
                             judge   is anchored exclusively to that settlement. Reward for reasoning is expected score
under proper scoring rules, not judge approval.

  probabilistic claims: causal graphs with quanti-                          Algorithm 1 Proof-Carrying Cognition (one
Claim      ledger.     Reasoning       stepsfullyare emitted     not        Algorithm 1 Proof-Carrying Cognition (one
                                                                            epoch)
  tative edges,   executable     snippets,            formal state-
only
  mentsaswhere
            natural-language          thoughts
                    possible, calibrated            but as typed,
                                                 forecasts   where
                                                                            epoch)
                                                                            Require: reasoner πθ ; world model Wϕ ; settle-
probabilistic      claims:    causal    graphs      with  quantita-         Require:         reasoner          θ ; world    modelrule      ; settle-
  not. The ledger generalizes autoformalization                (Wu                ment queue           Q; πproper       scoring       WϕS;     drift
tive   edges,
          2022)executable      snippets,      fully formal    state-              ment queue
  et al.,         from theorems        to empirical     assertions.               threshold       τ Q; proper scoring rule S; drift
ments where possible, calibrated forecasts where                                  threshold       τ of tasks do
                                                                              1: for   each batch
  Self-built
not.           world
       The ledger        model. A
                      generalizes         persistent, versioned
                                       autoformalization       (Wu            1: for π  each     batch of tasks do claims {(ci , pi )}
                                                                              2:          θ emits traces with typed
etmodel    pricesfrom
    al., 2022)      ledger    claims.toIts
                         theorems              only training
                                           empirical            loss
                                                        assertions.           2:        π       emits        tracesr ←with P typed claims
                                                                              3:       near-term reward
                                                                                           θ
                                                                                                                               i S(pi , Wϕ (ci ))
  is prediction
Self-built         of held-out
               world     model.reality:        experimental
                                     A persistent,              out-
                                                        versioned
                                                                              4: {(ciupdate
                                                                                        , pi )} πθ by RL on r P
  comes,prices
model       execution
                   ledger traces,
                             claims.time-lagged      observations.
                                         Its only training     loss           3:        near-termclaims  reward      r←
                                                                              5:       enqueue                    with          i S(pihandles
                                                                                                                         settlement    , Wϕ (ci )) in
isThis   extendsofthe
    prediction            world-model
                      held-out     reality: tradition     (Ha out-
                                               experimental     and           4: Q update πθ by RL on r
  Schmidhuber,
comes,     execution 2018;    LeCun,
                         traces,          2022) with
                                   time-lagged           a specific
                                                     observations.            5: end enqueue           claims with settlement handles in
                                                                              6:         for
  institutional
This    extendsrole:      the world model
                   the world-model                is amortized
                                             tradition    (Ha and re-             Q
                                                                              7: for each settled claim (c, y) dequeued from Q
  ality—dense,      immediate      reward     now,
Schmidhuber, 2018; LeCun, 2022) with a specific      with  periodic               end for
                                                                              6: do
  settlement keeping
institutional    role: thethe    amortizer
                              world    modelhonest.
                                                  is amortized re-            7: for update
                                                                                        each settled        claim             dequeued
                                                                              8:                   Wϕ on        loss (c,
                                                                                                                      ℓ(W y)ϕ (c),  y) from  ▷ only Q
ality—dense, immediate reward now, with periodic                                  do
                                                                                  loss: reality
  Terminology. We reserve world model for the
settlement keeping the amortizer honest.                                      8:
                                                                              9:        update Wϕ staked
                                                                                       pay/charge          on lossinstances
                                                                                                                       ℓ(Wϕ (c),byy)S(p, ▷y)only
  full generative component above. The learned pre-
Terminology. We reserve world model for the full                                  loss:for
                                                                             10: end       reality
  dictors in our experiments (§6–§8) are deliberately
generative component above. The learned predic-                               9: driftpay/charge
                                                                             11:          D ← E [ |W       staked
                                                                                                              ϕ (c) − instances    by S(p,
                                                                                                                        y| ] on settled    claims
                                                                                                                                              y)
  minimal settlement models—amortizers of settled
tors   in our over
  outcomes      experiments        (§6–§8) are deliberately
                       shallow features—and            should not                 end
                                                                             10: if
                                                                             12:     D for> τ then                         
minimal      settlement     models—amortizers
  be read as world models in the model-based-RL          of settled          11: driftdownweight
                                                                             13:          D ← E |Wnear-term   ϕ (c) − y|reward;on settled
                                                                                                                                      raise claims
                                                                                                                                             settle-
outcomes       over   shallow     features—and
  or generative sense; building the latter at training should    not              if D >
                                                                             12: ment      rateτ  then
be   read   as  world    models
  scale is untested (§10).           in  the   model-based-RL                13: end downweight
                                                                             14:         if                  near-term reward; raise settle-
or generative sense; building the latter at training                              ment rate
  Internal
scale         prediction
        is untested          market. Instances of the rea-
                        (§10).                                               14: end if
Internal
  soner stakeprediction
                calibration  market.
                               capital on      claims; of
                                           Instances    settlement
                                                           the rea-         source—human labels, LLM judges, learned
  uses strictly
soner              proper scoring
          stake calibration       capital rules
                                              on (Savage,     1971;
                                                   claims; settle-          PRMs—is a model of correctness, and a sufficiently
  Gneiting
ment      usesand    Raftery,
                strictly         2007),
                            proper          adjudicated
                                      scoring                by the
                                                   rules (Savage,           5.2 Why
                                                                            strong   optimizer  it can        work games
                                                                                                      eventually         where  anycurrent
                                                                                                                                     fixed model  ap-
 worldGneiting
1971;      model near-term
                     and Raftery,and reality
                                        2007), long-term.
                                                   adjudicatedThe by                proaches         fail
                                                                            of correctness (Gao et al., 2023). Reality is the
  construction
the   world model  is deliberately
                         near-term and  reminiscent      of logical
                                              reality long-term.            unique    reward function
                                                                            PCC dissolves           the Goodhart that cannot
                                                                                                                          problembe gamed,     only
                                                                                                                                      structurally
  induction
The            (Garrabrant
       construction             et al., 2016),
                        is deliberately             where market
                                             reminiscent     of log-        predicted.       The    classical      objection—reality’s
                                                                            rather than patching it. Every existing reward                    feed-
  dynamics     over   settled   claims     yield   asymptotically
ical induction (Garrabrant et al., 2016), where mar-                        back    is too sparselabels,    and slow       to train   on—is       an-
                                                                            source—human                             LLM       judges,     learned
  calibrated,
ket   dynamics  non-exploitable
                    over settled claimsbeliefs.yield asymptoti-             swered     by     amortization,         and   the  amortizer’s     drift
                                                                            PRMs—is a model of correctness, and a suffi-
cally calibrated, non-exploitable beliefs.                                  is itself measurable
                                                                            ciently     strong optimizer   (line 10eventually
                                                                                                                       of Algorithm      1) rather
                                                                                                                                      games      any
  5.2 Why it can work where current                                         than   an  invisible      failure     mode.    PCC    thus  combines
          approaches fail                                                   fixed model of correctness (Gao et al., 2023). Re-
                                                                            the
                                                                            alitydensity      of a learned
                                                                                   is the unique          reward  verifier  withthat
                                                                                                                     function      the incorrupt-
                                                                                                                                        cannot be
 PCC dissolves the Goodhart problem structurally                            ibility  of  a   formal    kernel,     extended
                                                                            gamed, only predicted. The classical objection—     for the  first time
 rather than patching it. Every existing reward                             into  empirical
                                                                            reality’s     feedback domains,
                                                                                                          is tooand     it obeys
                                                                                                                    sparse    and the
                                                                                                                                    slowbitter   les-
                                                                                                                                            to train

                                                                        5
                                                                                               N
                                                                                               N                11      1616       128 51251220482048
                                                                                                                                 128
  reward of selected program                sound verifier (execution)
                               0.8          learned verifier (gold reward)                     Snd@N
                                                                                               Snd@N          1.00
                                                                                                               1.00 0.64
                                                                                                                     0.64 0.40
                                                                                                                            0.40 0.310.310.130.13
                                            learned verifier (proxy reward)
                               0.6                                                      Table
                                                                                         Table1:1:Soundness-under-Pressure
                                                                                                    Soundness-under-Pressure     (Definition 1) 1)
                                                                                                                                   (Definition   of of
                                                                                        the learned  verifier in the program-synthesis  testbed.
                                                                                         the learned verifier in the program-synthesis testbed.  AA
                               0.4                                                      sound  verifier scores  1.00  at every N by construction.
                                                                                         sound verifier scores 1.00 at every N by construction.

                               0.2
                                                                                        6.2     Result 1: learned verifiers collapse under
                               0.0                                                              pressure;
                                                                                          reasoning rather        sound
                                                                                                                     than ones       do not
                                                                                                                             executing      it—fit on 1,000 la-
                                       21        23     25      27      29    211       Figure
                                                                                          beled 3random
                                                                                                      shows gold        reward
                                                                                                                 programs          oftask.
                                                                                                                                 per  the selected
                                                                                                                                             Resultsprogram
                                                                                                                                                         aggregate
                                     candidates N (optimization pressure)               as60optimization
                                                                                              tasks; shadedpressure   bands are(best-of-N
                                                                                                                                     ±1 s.e. ) increases.
                                                                                        Both verifiers start at 0.079 at N =1. The execution
 Figure 3: Goodharting under optimization pressure.                                     verifier climbs monotonically to 0.831 at N =2048.
Figure 3: Goodharting under optimization pressure.
 Best-of-N selection by the sound (execution) verifier                                  The       Resultverifier’s
                                                                                          6.2 learned           1: learned   proxyverifiers     collapse
                                                                                                                                      score rises             under
                                                                                                                                                        through-
Best-of-N selection by the sound (execution) verifier
 improves monotonically to 0.83 gold reward. Selec-                                     out, but  pressure;
                                                                                                       the goldsound  rewardones       doselections
                                                                                                                                   of its   not             peaks
improves      monotonically to 0.83 gold reward. Selec-
 tion by the learned verifier inflates its own proxy score
tion  by  the  learned   verifier                                                       near N =512 and declines to 0.104—the qualita-
 (dashed) while     realized  goldinflates
                                   reward its ownnear
                                           peaks   proxy score
                                                       N =512                             Figure      3 shows goldcurve        reward
(dashed)   while   realized   gold reward  peaks  near
 and falls to 0.10 at N =2048—the overoptimization sig-N =512                           tive   overoptimization                      of ofGaotheet selected
                                                                                                                                                     al. (2023), pro-
and  fallsoftoGao
 nature        0.10etat al.
                        N =2048—the       overoptimization
                            (2023), reproduced             sig-
                                                  with a fully                          here with a fully transparent gold standard. Table 1in-
                                                                                          gram      as     optimization           pressure      (best-of-N      )
nature   of Gao
 transparent    goldetstandard.
                       al. (2023), reproduced with a fully                                creases.
                                                                                        reports      theBoth     verifiers
                                                                                                           induced              start at metric
                                                                                                                         soundness        0.079 at  (defined
                                                                                                                                                       N =1. in  The
transparent gold standard.                                                                execution
                                                                                        §9):    it collapsesverifierfromclimbs 1.00monotonically
                                                                                                                                     to 0.13 as N grows.   to 0.831
                                                                                          at N =2048.pressure
                                                                                        Optimization              The learneddoes not verifier’s
                                                                                                                                         merely fail  proxy    score
                                                                                                                                                          to help
 son (Sutton,    2019):                                                                 anrises   throughout,
                                                                                             unsound        verifier;but      the goldinverts
                                                                                                                         it actively      reward   it. of its selec-
on—is     answered       byitamortization,
                               substitutes computation
                                                  and the amor- and
 settleddrift
          data is
                foritself
                       hand-built    judgment.                                            tions peaks near N =512 and declines to 0.104—
tizer’s                      measurable       (line 10 of Algo-                         6.3     Result 2: reality-anchored                   settlement
                                                                                          the qualitative         overoptimization curve              of Gao et al.
rithm 1) rather than an invisible failure mode. PCC
                                                                                          (2023), here with a fully transparentcapability
                                                                                                bounds        drift    and     compounds           gold standard.
thus  combines the
 6 Minimal                density ofDemonstrations
                     Empirical          a learned verifier with
                                                                                        WeTable
                                                                                              then1 reports
                                                                                                       run the the        inducedloop
                                                                                                                    settlement        soundness         metric (de-
                                                                                                                                             of Algorithm         1
the incorruptibility of a formal kernel, extended
                                                                                        infined    in §9): each
                                                                                            miniature:          it collapses
                                                                                                                        round, from sample  1.00    to 0.13
                                                                                                                                               a pool          as N
                                                                                                                                                          of 512
for
 We the    first time
      validate            into empirical
                  the paper’s      two core domains,
                                                mechanisms    andinit
                                                                                        programs,          select the top
                                                                                          grows. Optimization                     32 bydoes
                                                                                                                             pressure      the learned
                                                                                                                                                 not merely   veri-
                                                                                                                                                                  fail
obeys    the   bitter   lesson    (Sutton,     2019):
 a testbed small enough to be fully reproducible           it substi-
                                                                                        fier,  settle     them     by   execution,       append
                                                                                          to help an unsound verifier; it actively inverts it.       the   settled
tutes
 on a computation           and settled
       laptop, yet possessing          thedata
                                             onefor    hand-built
                                                   property     that                    labels to the verifier’s training set, and refit—versus
judgment.
 matters: an executable, incorruptible gold verifier.                                   a frozen-verifier baseline. Over ten rounds (Fig-
 All numbers below are measured, not estimated;                                           6.34), Result
                                                                                        ure         the frozen   2: verifier’s
                                                                                                                         reality-anchored
                                                                                                                                    anchor drift settlement
                                                                                                                                                       stays flat
6codeMinimal
        and seedsEmpirical
                        are released  Demonstrations
                                         with the paper. We                             (≈ 0.10)  boundsand itsdrift      and compounds
                                                                                                                   achieved        gold rewardcapability
                                                                                                                                                      decreases
 stress
We       the scope
     validate            honestly:
                 the paper’s       twothese
                                         core are    mechanism
                                                mechanisms         in                   from 0.154 to 0.125: repeatedly harvesting the
 demonstrations,        not  frontier-scale
a testbed small enough to be fully reproducibleevidence.                                  We then
                                                                                        same             run the features
                                                                                                  exploitable         settlement        loopno
                                                                                                                                    yields      of compound-
                                                                                                                                                     Algorithm 1
on a laptop, yet possessing the one property that                                         in miniature:
                                                                                        ing.     The anchored     each verifier’s
                                                                                                                           round, sample          a pool
                                                                                                                                         drift falls    by of 26% 512
matters:    an executable,       incorruptible                                            programs,         select   the    top   32  by  the   learned      verifier,
 6.1 Setup:        program synthesis          withgold       verifier.
                                                      executable                        (0.101 → 0.075) and its achieved gold reward
All numbers                                                                               settle them         by(0.154
                                                                                                                    execution,        append Thethe      settled la-
        groundbelow truth are measured, not estimated.                                  roughly      doubles                  → 0.306).             mechanism
We stress the scope honestly: these are mechanism                                       isbels   to thetheverifier’s
                                                                                            exactly           paper’s training
                                                                                                                            thesis inset,     and refit—versus
                                                                                                                                         microcosm:         settle-
demonstrations,
 Tasks are drawnnot          frontier-scale
                        by sampling             evidence.
                                          a hidden     target pro-                        a frozen-verifier
                                                                                        ment                          baseline.own
                                                                                                converts the verifier’s               Over     ten rounds
                                                                                                                                          selection     pressure(Fig-
 gram of length 4 over a six-token integer DSL                                            ure training
                                                                                        into   4), the frozensignal,verifier’s
                                                                                                                         so the places anchor     driftthe
                                                                                                                                              where       stays   flat
                                                                                                                                                              veri-
6.1 Setup: program synthesis with executable                                            fier
                                                                                          (≈ is0.10)
                                                                                                  mostand   wrong      are precisely
                                                                                                                 its achieved        goldthe    placesdecreases
                                                                                                                                            reward         reality
 (+1, −1, ×2, ×3, negate, square); a candidate pro-
 gram’sground       truth is the fraction of eight input–
           gold reward                                                                  corrects
                                                                                          from 0.154  it first.to 0.125: repeatedly harvesting the
Tasks
 outputare    drawn
          points        by sampling
                   it matches             a hidden (the
                                 under execution        target   pro-
                                                              sound                       same exploitable features yields no compound-
gram    of length
 verifier).             4 oververifier
              The learned         a six-token       integer
                                           is a ridge           DSL
                                                         regressor                      6.4
                                                                                          ing. Result        3: an adversarial
                                                                                                   The anchored              verifier’sgenerator
                                                                                                                                           drift fallshacks by 26%a
 over token
(+1,   −1, ×2,  unigram/bigram
                      ×3, negate, countssquare); anda length—a
                                                         candidate                              frozen       verifier;      settlement
                                                                                          (0.101 → 0.075) and its achieved gold reward      inverts     the
 deliberatelygoldshallow     judge,isstanding     in for of anyeight
                                                                ver-                            exploit
program’s               reward         the fraction                                       roughly doubles (0.154 → 0.306). The mecha-
 ifier that evaluates
input–output        pointssurface      features
                              it matches      underof reasoning
                                                         execution                      Best-of-N
                                                                                          nism is exactly  appliesthe  i.i.d.   pressure;
                                                                                                                           paper’s     thesisRLinapplies
                                                                                                                                                      microcosm:di-
 rather
(the     thanverifier).
      sound     executingThe   it—fit   on 1,000
                                   learned           labeled
                                              verifier          ran-
                                                          is a ridge                    rected     pressure.       We    therefore      attack
                                                                                          settlement converts the verifier’s own selection       each     verifier
 dom programs
regressor     over pertokentask. Results aggregate
                              unigram/bigram              60 tasks;
                                                      counts     and                    with   an adaptive
                                                                                          pressure                 adversary:
                                                                                                         into training              steepest-ascent
                                                                                                                               signal,   so the places     search
                                                                                                                                                              where
 shaded    bands    are  ±1   s.e.
length—a deliberately shallow judge, standing in                                        that  proposes        16   mutations        per  step
                                                                                          the verifier is most wrong are precisely the places   and    moves     to
for any verifier that evaluates surface features of                                       reality corrects it first.

                                                                                    6
                                   0.12
       anchor drift |proxy gold|
                                                                                                             frozen verifier




                                                                            gold reward of selected
                                                                                                      0.35
                                   0.11                                                                      reality-anchored
                                                                                                      0.30
                                   0.10
                                                                                                      0.25
                                   0.09                                                               0.20
                                   0.08                                                               0.15
                                          frozen verifier
                                   0.07   reality-anchored                                            0.10

                                          2       4          6     8   10                                    2       4          6     8      10
                                                settlement round                                                   settlement round

 Figure 4: The settlement loop of Algorithm 1 in miniature (60 tasks, ±1 s.e.). Left: anchor drift |proxy − gold|
Figure 4: The settlement loop of Algorithm 1 in miniature (60 tasks, ±1 s.e.). Left: anchor drift |proxy − gold|
 on selected claims. Anchored settlement reduces drift by 26%; the frozen verifier does not improve. Right: gold
on selected claims. Anchored settlement reduces drift by 26%; the frozen verifier does not improve. Right: gold
 reward of the top selection per round. Anchoring roughly doubles achieved reward (0.154 → 0.306) while the
reward of the top selection per round. Anchoring roughly doubles achieved reward (0.154 → 0.306) while the
 frozen verifier stagnates and slightly degrades (0.154 → 0.125).
frozen verifier stagnates and slightly degrades (0.154 → 0.125).

 the highest-scoring one, for 250 steps (40 tasks).                                      should beat settling at random. We sweep settle-
6.4 Result 3: an adversarial generator hacks                                             vative, which is the safe failure direction but not a
 The anchored condition settles the adversary’s own                                      ment budgets S ∈ {0, 50, 150, 500, 1500} on a
       a frozen verifier; settlement inverts the                                         free one.
 trajectory (25 visited programs) by execution ev-                                       weaker base verifier (500 random labels) under two
       exploit
 ery 25 steps and refits—charging a total settlement                                     acquisition
                                                                                         6.5 Resultpolicies:       on-policy
                                                                                                          4: soundness           (iteratively
                                                                                                                             scales             label the
                                                                                                                                      with settlement,
 budget of 250
Best-of-N            reality
               applies    i.i.d.queries
                                  pressure;per run,   which we
                                                RL applies     di-                       programs     the  current   verifier
                                                                                                and on-policy settlement is >10×selects)   and   random
                                                                                                                                                    more
 report as the explicit price of trust.                                                  (the same    number
                                                                                                label-efficient  of labels    on  random     programs),
rected pressure. We therefore attack each verifier
                                                                                         then measure the Soundness AUC of Definition 1
withFigure   5 showsadversary:
      an adaptive       three regimes.       Against thesearch
                                      steepest-ascent       sound
                                                                                         If settlement is the fuel of trustworthy verifica-
 verifier, adversarial      pressure     is simply    capability:                        on fresh pools (40 tasks).
that proposes 16 mutations per step and moves to                                         tion, soundness should scale with the settled-label
 gold
the     reward climbsone,
     highest-scoring        to 0.869.
                                   for 250 Against    the tasks).
                                              steps (40    frozen                           Figure 6: on-policy settlement scales approx-
                                                                                         budget—and settling where the verifier is deployed
The anchored condition settles the adversary’sproxy
 learned   verifier,   the  adversary      saturates   the   own                         imately log-linearly, 0.500 → 0.706, while ran-
                                                                                         should beat settling at random. We sweep set-
 within   ∼15     steps   and    locks    permanently
trajectory (25 visited programs) by execution ev-          into a                        dom labeling crawls, 0.531 → 0.595. Strikingly,
                                                                                         tlement budgets S ∈ {0, 50, 150, 500, 1500} on a
 hacked optimum: gold reward flatlines at 0.178                                          150 on-policy settled labels (0.617) outperform
ery 25 steps and refits—charging a total settlement                                      weaker base verifier (500 random labels) under two
 with a persistent positive hacking gap (+0.037)—                                        1,500 random labels (0.595): on-policy settlement
budget of 250 reality queries per run, which we                                          acquisition policies: on-policy (iteratively label the
 the verifier permanently overvalues exactly the pro-                                    is more than 10× more label-efficient. The mech-
report as the explicit price of trust.                                                   programs the current verifier selects) and random
 grams the adversary produces. Against the an-                                           anism is the thesis in one line—the verifier’s se-
   Figure 5 shows three regimes. Against the sound                                       (the same number of labels on random programs),
 chored verifier, settlement re-prices the adversary’s                                   lection pressure concentrates settlement exactly
verifier, adversarial pressure is simply capability:                                     then measure the Soundness AUC of Definition 1
 region each round: the hacking gap does not merely                                      where the verifier is most wrong—and it is why
gold reward climbs to 0.869. Against the frozen                                          on fresh pools     (40 tasks).
 shrink but inverts to −0.101—after settlement, the                                      Algorithm     1 settles  the claims the reasoner actually
learned verifier, the adversary saturates the proxy                                         Figure
 verifier systematically distrusts the region the ad-                                    stakes,  not6:a random
                                                                                                           on-policy    settlement
                                                                                                                    audit   sample. scales approx-
within ∼ 15 steps and locks permanently into a                                           imately log-linearly, 0.500 → 0.706, while ran-
 versary inhabits—and gold reward reaches 0.297,
hacked optimum: gold reward flatlines at 0.178                                           dom labeling
 a 67% improvement over frozen, still rising at step                                     6.6    Result 5:crawls,      0.531buys
                                                                                                             settlement        → 0.595.       Strikingly,
                                                                                                                                     resolution,    not
with a persistent positive hacking gap (+0.037)—                                         150 on-policy       settled
                                                                                                just calibration       labels    (0.617)    outperform
 250. Two honest observations: anchoring restores
the verifier permanently overvalues exactly the                                          1,500 random labels (0.595): on-policy settlement
 trustworthiness (the adversary can no longer sus-
programs      thescores)
                    adversary      produces.                                             A  standingthanobjection    to label-efficient.
                                                                                                                          settlement-based    Thereward
 tain inflated             but does     not closeAgainst      the
                                                    the capacity                         is more          10× more                                  mech-
anchored                                                                                 (§11,  failure   mode    2) is  that  it teaches    systems    to
 gap to theverifier,     settlementshallow
              sound verifier—a            re-prices   the adver-
                                                 feature   model                         anism is the thesis in one line—the verifier’s se-
sary’s   region    each   round:      the   hacking    gap does                          make    safe,   vague   claims:    probabilities
                                                                                         lection pressure concentrates settlement exactly     near   base
 remains shallow—and the inverted gap means                    an-
not  merely    shrink   but  inverts   to  −0.101—after       set-                       rate
                                                                                         wherearethenever   badlyiswrong.
                                                                                                        verifier               Proper scoring
                                                                                                                     most wrong—and            it isrules
                                                                                                                                                      why
 chored pricing errs conservative, which is the safe
tlement,    the verifier     systematically                                              decompose       exactly   along    this  axis  (Gneiting     and
 failure direction     but not    a free one. distrusts the                              Algorithm 1 settles the claims the reasoner actually
region the adversary inhabits—and gold reward                                            Raftery,    2007):   the  Brier
                                                                                         stakes, not a random audit sample.score   splits  into  reliabil-
reaches    0.297,                                                                        ity (miscalibration; lower is better) and resolution
 6.5 Result       4: asoundness
                        67% improvement
                                     scales withover      frozen,
                                                     settlement,
still rising   at step   250.    Two    honest   observations:                           6.6 far
                                                                                         (how   Result
                                                                                                     claims5: usefully
                                                                                                               settlementdepartbuysfromresolution,     not
                                                                                                                                          the base rate;
        and on-policy settlement is >10× more
anchoring     restores trustworthiness (the adversary                                    higherjust    calibration
                                                                                                  is better).   We run twelve settlement rounds
        label-efficient
can no longer sustain inflated scores) but does not                                      of probabilistic
                                                                                         A standing           claimsto(“this
                                                                                                         objection              program matches
                                                                                                                          settlement-based        rewardat
 If settlement
close              is thegap
        the capacity         fueltoofthetrustworthy      verifica-
                                            sound verifier—a                             least  2/8    I/O  points”),    1,920     settled
                                                                                         (§11, failure mode 2) is that it teaches systems to claims   per
 tion, soundness      should     scale  with
shallow feature model remains shallow—and the  the settled-label                         round    across
                                                                                         make safe,        60 tasks,
                                                                                                         vague   claims:refitting    the claim
                                                                                                                             probabilities        model
                                                                                                                                               near  base
 budget—and
inverted          settlinganchored
           gap means         where thepricing
                                           verifiererrs
                                                     is deployed
                                                          conser-                        on
                                                                                         ratesettled  outcomes
                                                                                               are never    badlyeach
                                                                                                                    wrong. round.
                                                                                                                                Proper scoring rules

                                                                            7
                                               program




                                                                                                                                    (proxygold)gold)
                                                                                                                                                                         frozen
                                           program       0.8                                                                                            0.10             reality-anchored
                                                                                                                                                                       frozen
                                                                                                                                                       0.10
                                                                                                                                                        0.05
                                    of current
                                                         0.8                                                                                                           reality-anchored
                                                         0.6                          sound verifier (execution)
                                                                                                                                                       0.05
                                of current

                                                                                      learned, reality-anchored                                         0.00




                                                                                                                                (proxy
                                                         0.6                         sound  verifier
                                                                                      learned, frozen(execution)
                                                         0.4




                                                                                                                            gap gap
                                                                                     learned, reality-anchored                                         0.00
                                                                                                                                                        0.05
                             reward



                                                         0.4                         learned, frozen
                                                                                                                                                       0.05




                                                                                                                       hacking
                                                         0.2                                                                                            0.10
                         reward




                                                                                                                    hacking
                                                         0.2                                                                                           0.10
                                                                                                                                                        0.15
                    goldgold




                                                               0       50      100       150         200      250                                      0.15        0      50      100       150      200        250
                                                               0    adversarial
                                                                      50     100optimization
                                                                                    150 200   step 250                                                         0        adversarial
                                                                                                                                                                         50     100 optimization
                                                                                                                                                                                       150 200step 250
                                                                    adversarial optimization step                                                                      adversarial optimization step
 Figure 5: Adversarial optimization against three verifiers (40 tasks, ±1 s.e.). Left: against a sound verifier,
Figure 5: Adversarial optimization against three verifiers (40 tasks, ±1 s.e.). Left: against a sound verifier,
 adversarial   pressure is capability (0.869);       against  a frozen learned
                                                                            tasks, verifier,
                                                                                    ±1 s.e.).the  adversary    locks    into verifier,
                                                                                                                              a hacked
 Figure   5: Adversarial
adversarial   pressure is optimization      againstagainst
                            capability (0.869);       three verifiers
                                                              a frozen(40learned   verifier,  theLeft: against
                                                                                                  adversary       a sound
                                                                                                                locks    into a hacked
 optimum
 adversarialwithin ∼15
               pressure  steps  (0.178,  flat); anchored   settlement  keeps  repairing  the  landscape   (0.297   and   rising, +67%
optimum     within  ∼ 15issteps
                            capability
                                  (0.178,(0.869);   against a settlement
                                            flat); anchored     frozen learned   verifier,
                                                                             keeps          the the
                                                                                     repairing   adversary   locks(0.297
                                                                                                     landscape       into aandhacked
                                                                                                                                  rising,
 over  frozen).
 optimum         Right:
            within        the frozen
                         steps (0.178,
                   ∼15Right:          verifier’s  hacking
                                        flat); verifier’s   gap
                                               anchored settlement(proxy  −
                                                                      keeps  gold)  locks
                                                                             repairing     in positive;
                                                                                        the landscape    settlement
                                                                                                        (0.297 and     inverts  it—the
                                                                                                                      rising, +67%
+67%    over  frozen).           the frozen               hacking gap    (proxy   − gold)    locks in positive;    settlement    inverts
 verifier learnsRight:
 over frozen).   to distrust  the adversary’s
                         the frozen  verifier’sregion.
                                                 hacking gap (proxy − gold) locks in positive; settlement inverts it—the
it—the verifier learns to distrust the adversary’s region.
 verifier learns to distrust the adversary’s region.

                                                                                                                                             6.7 What these demonstrations do and do not
                                                                   on-policy settlement                                                      comes gains
                                                                                                                                            6.7 What
                                                                                                                                                                    exactly the discriminative signal that
                                                                                                                                                      show these demonstrations do and do not
                    0.70                                           random labels
                                                                   on-policy       (same budget)
                                                                             settlement                                                      resolution          measures.        This does not retire the fail-
                                                                                                                                             They   show
                                                                                                                                                       show, withagent      measured          numbers,
                    0.70                                                                                                                                                                              whichthat         (i) the
              AUC




                                                                   random labels (same budget)                                               ure mode—an                           choosing                       claims        to
                    0.65                                                                                                                    They     show,
                                                                                                                                             exchange-rate       with  lawmeasured
                                                                                                                                                                              of §3   is   numbers,
                                                                                                                                                                                            quantitatively   that    (i)
                                                                                                                                                                                                                     exactthe  in
            AUC




                    0.65                                                                                                                     stake could still select easy ones, which is why
    Soundness




                    0.60                                                                                                                    exchange-rate
                                                                                                                                             its  model class;       law(ii)ofunsound
                                                                                                                                                                                §3 is quantitatively
                                                                                                                                                                                              verifiers           exact
                                                                                                                                                                                                              invert        in
                                                                                                                                                                                                                         under
                                                                                                                                             RSR-Bench              must    score resolution             explicitly—but
  Soundness




                    0.60                                                                                                                    its model
                                                                                                                                             i.i.d.  pressureclass; and(ii) unsound
                                                                                                                                                                             are   locked   verifiers
                                                                                                                                                                                                 into      invert under
                                                                                                                                                                                                        hacked        optima
                                                                                                                                             it shows the training dynamics do not intrinsically
                    0.55                                                                                                                    i.i.d.
                                                                                                                                             under  pressure
                                                                                                                                                       directed      and   are locked
                                                                                                                                                                      adversarial             into hacked
                                                                                                                                                                                       pressure;         (iii) theoptima
                                                                                                                                                                                                                      anchor-
                    0.55                                                                                                                     collapse        toward       vagueness.
                                                                                                                                            under    directed adversarial
                                                                                                                                             ing mechanism               at the heartpressure;of PCC  (iii)produces
                                                                                                                                                                                                              the anchor-    the
                    0.50                                                                                                                    ing
                    0.50                                                                                                                     6.7mechanism
                                                                                                                                             predictedWhat             at the
                                                                                                                                                                   these         heart of and
                                                                                                                                                                            demonstrations
                                                                                                                                                               behavior—bounded                 PCCeven  produces
                                                                                                                                                                                                                and dothenot
                                                                                                                                                                                                          do inverted         ex-
                                                                                                                                            predicted show   behavior—bounded
                                                                                                                                             ploitation, compounding capability—against both and    even    inverted       ex-
                                                           0           50       150            500          1500
                                                           0        settled-label
                                                                      50              500S
                                                                              150 budget                   1500                             ploitation,
                                                                                                                                             kinds             compounding
                                                                                                                                                       of pressure;                  capability—against
                                                                                                                                                                             (iv) soundness            scales       withboth
                                                                                                                                             They show,             with measured             numbers,           that    (i) set-
                                                                                                                                                                                                                              the
                                                                    settled-label budget S                                                  kinds
                                                                                                                                             tlement,of pressure;
                                                                                                                                                              log-linearly (iv) and
                                                                                                                                                                                  soundness
                                                                                                                                                                                          with
                                                                                                                                             exchange-rate law of §3 is quantitatively exact in     ascales
                                                                                                                                                                                                       large      with    set-
                                                                                                                                                                                                                  on-policy
                                                                                                                                            tlement,
                                                                                                                                             efficiency     log-linearly
                                                                                                                                                                multiplier;     and
                                                                                                                                                                                  andwith         a large on-policy
                                                                                                                                                                                         (v) verifiers
                                                                                                                                                                                                settlement         sharpens
 Figure 6: Soundness scales with settlement (40 tasks,                                                                                       its model class;            (ii) unsound                          invert     under
 Figure  6: Soundness                                                                                                                       efficiency
                                                                                                                                             claims           multiplier;
                                                                                                                                                         rather     than        and
                                                                                                                                                                           blunting   (v)     settlement
                                                                                                                                                                                          them.      They      dosharpens
                                                                                                                                                                                                                   notoptima
                                                                                                                                                                                                                          show
 ±1 s.e.).
Figure      Soundness scales
         6: Soundness    AUC vs.
                        scales
                                 withsettled-label
                                        settlement (40
                                  with settlement (40
                                                          tasks,
                                                      budget   S.
                                                           tasks,                                                                            i.i.d. pressure and are locked into hacked
 ±1  s.e.).
 On-policy  Soundness
             settlement AUC
                          (labelvs.   settled-label
                                   what    the       budget
                                               verifier       S.
                                                         selects)                                                                           claims
                                                                                                                                             that   a  rather
                                                                                                                                                       claim      than    blunting
                                                                                                                                                                   language       richthem.
                                                                                                                                                                                          enough   Theyfor  doopen-ended
                                                                                                                                                                                                                 not show
±1 s.e.). Soundness AUC vs. settled-label budget S.                                                                                          under
                                                                                                                                            that
                                                                                                                                                       directed
                                                                                                                                                  a claim exists,
                                                                                                                                                                       adversarial
                                                                                                                                                                 language       rich
                                                                                                                                                                                        pressure; (iii) the anchor-
                                                                                                                                                                                      enough for open-ended
 On-policy   settlement
 scales log-linearly;    (label   what labels
                            on-policy
                      150(label           the verifier  selects)
                                                beat 1,500   ran-                                                                            reasoning                      that   world-model              amortization
On-policy
 scales
            settlement
        log-linearly;10×
                                  what the verifier
                      150 on-policy
                                                        selects)
                                        labels beat 1,500 ran-                                                                               ing mechanism
                                                                                                                                            reasoning          exists,   at
                                                                                                                                                                          thattheworld-model
                                                                                                                                                                                   heart of PCCamortization  produces the
 dom
scaleslabels—over
        log-linearly;10×
                       150  label efficiency.
                              on-policy     labels beat 1,500                                                                                scales,      that    these    effects    survive        when       the   genera-
 dom labels—over           label  efficiency.                                                                                                predicted
                                                                                                                                            scales,     that   behavior—bounded
                                                                                                                                                                these LLMeffectstrained         and
                                                                                                                                                                                    survivebywhen      even  theinverted
                                                                                                                                                                                                                   genera-     ex-
random labels—over 10× label efficiency.                                                                                                     tor  is   a
                                                                                                                                             ploitation,   frontier
                                                                                                                                                                 compounding                         RL
                                                                                                                                                                                       capability—against   rather      than
                                                                                                                                                                                                                           both a
                                                                                                                                            tor  is
                                                                                                                                             search  a   frontier
                                                                                                                                                         process,      LLM
                                                                                                                                                                        or that trained
                                                                                                                                                                                   anchoring  by   RL can rather     than
                                                                                                                                                                                                             closewith       a
                                                                                                                                                                                                                       (rather
                                                                                                                                             kinds process,
                                                                                                                                            search      of    pressure;
                                                                                                                                                                      or that (iv)  soundness
                                                                                                                                                                                 anchoring              scales                set-
                                                                                                                                             than narrow)            the   capacity       gap tocan        close (rather
                                                                                                                                                                                                      a sound         verifier.
                                                                                                                                             tlement,
                                                                                                                                            than   narrow)    log-linearly
                                                                                                                                                                   the capacity    and     with     a
                                                                                                                                                                                       gap to a sound   large     on-policy
                                                                                                                                                                                                                   verifier.
                                                                                                                                             Those       are precisely         the questions           the programme
decompose exactly along this axis (Gneiting and                                                                                              efficiency
                                                                                                                                            Those     are       multiplier;
                                                                                                                                                              precisely       the and     (v) settlement
                                                                                                                                                                                   questions         the            sharpens
                                                                                                                                                                                                            programme
                                                                                                                                             of §10 is designed to answer.
Raftery, 2007): the Brier score splits into reliabil-                                                                                        claims        rather      than
                                                                                                                                            of §10 is designed to answer.      blunting         them.        They       do not
     Figure    7: reliability
                           lowerfalls
ity Figure
     (miscalibration;                    0.0064
                                   is better)  and →
               7: reliability falls 0.0064 → 0.0039
                                                          0.0039
                                                      resolution                                                                             7 Scaled Pre-registered Replication open-
                                                                                                                                             show      that     a  claim     language         rich   enough         for
 (−40%)
(how         and
        far claims resolution     doubles,
                      usefully depart     from0.051
                                                 the →  →   0.101
                                                       base0.101
                                                             rate;                                                                          7endedScaled         Pre-registered
                                                                                                                                                         reasoning         exists, thatReplication
                                                                                                                                                                                               world-model amorti-
 (−40%)      and resolution      doubles,    0.051
 (+98%).
higher    is   In thisWe
             better).    setting,
                             run   settlement
                                  twelve         did not
                                           settlement        push
                                                          rounds                                                                             The
                                                                                                                                             zation  demonstrations
                                                                                                                                                         scales,      that       of §6
                                                                                                                                                                              these         are deliberately
                                                                                                                                                                                      effects        survive when         mini-
                                                                                                                                                                                                                              the
 (+98%). In this setting, settlement did not push                                                                                           The demonstrations of §6 are deliberately mini-
 claims    toward the      vague    base rate; it matches
                                                      sharpened                                                                              mal,    so
                                                                                                                                             generator      we    commissioned              an    adversarial         replica-
of  probabilistic
 claims    toward the claims   (“this
                           vague    baseprogram
                                          rate; it sharpenedat                                                                              mal,    so we is        a frontier LLM
                                                                                                                                                                commissioned                   trained by RL
                                                                                                                                                                                        an adversarial                   rather
                                                                                                                                                                                                                   replica-
 them,
least     because     a claim   model    refit  on   settled  out-                                                                           tion
                                                                                                                                             than   at
                                                                                                                                                     a    larger scale,
                                                                                                                                                         search       process, withor  every
                                                                                                                                                                                       that        pass/fail can
                                                                                                                                                                                                 anchoring         criterion
                                                                                                                                                                                                                          close
 them,2/8     I/O points”),
          because                1,920 refit
                     a claim model       settled    claimsout-
                                               on settled     per                                                                           tion at larger scale, with every pass/fail criterion
 comes
round      gains  exactly    the  discriminative      signal  that                                                                           pre-registered
                                                                                                                                             (rather       than       before any
                                                                                                                                                                    narrow)      the   experiment
                                                                                                                                                                                       capacity          gap ran to (the
                                                                                                                                                                                                                      a     pre-
                                                                                                                                                                                                                         sound
 comesacross       60 tasks,
           gains exactly    the refitting   the claim
                                 discriminative           model
                                                     signal  that                                                                           pre-registered before any experiment ran (the pre-
 resolution     measures.each Thisround.
                                     does not retire the fail-                                                                               registration,
                                                                                                                                             verifier. Those        raw    per-task      data,     and     analysis       code
on   settled  outcomes
 resolution measures. This does not retire the fail-                                                                                        registration,         raware      precisely
                                                                                                                                                                         per-task     data,the   andquestions
                                                                                                                                                                                                        analysis the   code  pro-
 ure   mode—an
    Figure             agent choosing
              7: reliability                which claims
                                  falls 0.0064                  to                                                                           are
                                                                                                                                             grammereleased  of     with
                                                                                                                                                                  §10    is  the paper).
                                                                                                                                                                             designed        to    The suite was de-
                                                                                                                                                                                                  answer.
 ure   mode—an        agent choosing        which →       0.0039
                                                      claims   to                                                                           are released with the paper). The suite was de-
 stake could
(−40%)            still
             and still   select easy
                  resolution            ones, which
                                 doubles,                 is why                                                                             signed to break our claims, not to confirm them:
 stake could            select easy            which→is 0.101
                                       ones,0.051           why                                                                             signed to break our claims, not to10confirm them:
 RSR-Bench
(+98%).       In  must
                 this     score
                        setting, resolution
                                   settlement  explicitly—but
                                                 did   not  push                                                                             7 uses
                                                                                                                                             it     Scaled
                                                                                                                                                         a 10-token Pre-registered
                                                                                                                                                                            DSL with ∼10         Replication
                                                                                                                                                                                                          candidate pro-
 RSR-Bench must score resolution explicitly—but                                                                                             it uses a 10-token DSL with4 ∼1010 candidate pro-
 it shows the training
claims                       dynamics     do  not intrinsically                                                                              grams       (versus       ∼4.6     ×   10     ),  16   I/O    points, 2–4×
 it showstoward      the vague
             the training   dynamicsbase do
                                          rate;
                                             not itintrinsically
                                                     sharpened                                                                               The demonstrations
                                                                                                                                            grams      (versus ∼4.6 ×of10          §64 ),are16deliberately
                                                                                                                                                                                                  I/O points,minimal, 2–4×
 collapse
them,        toward vagueness.
         because                                                                                                                             more     tasks     with paired Wilcoxon                statistics, a strong
 collapse    towardavagueness.
                        claim model refit on settled out-                                                                                    so we
                                                                                                                                            more    tasks commissioned
                                                                                                                                                               with paired Wilcoxon an adversarialstatistics,replication
                                                                                                                                                                                                                  a strong

                                                                                                                                8
                                  0.0065                                                                       0.10
             reliability (miscalibration)
                                  0.0060
                                    0.0065                                                                      0.10
                                                                                                               0.09
        reliability (miscalibration)
                                  0.0055
                                    0.0060
                                                                                                                0.09
                                                                                                               0.08




                                                                                          resolution
                                  0.0050
                                    0.0055
                                                                                                                0.08




                                                                                      resolution
                                                                                                               0.07
                                  0.0045
                                    0.0050
                                                                                                                0.07
                                                                                                               0.06
                                    0.0045
                                  0.0040
                                    0.0040
                                  0.0035                                                                        0.06
                                                                                                               0.05
                                             2       4     6    8    10     12                                  0.05                     2            4          6                                              8               10                   12
                                    0.0035           settlement
                                                 2     4     6 round
                                                                  8    10    12                                                           2           settlement
                                                                                                                                                       4      6 round
                                                                                                                                                                   8    10                                                                           12
                                                      settlement round                                                                                 settlement round
 Figure 7: Brier decomposition over twelve settlement rounds (1,920 settled claims per round). Settlement improves
Figure 7: Brier decomposition over twelve settlement rounds (1,920 settled claims per round). Settlement improves
 calibration  (reliability
   Figure 7: (reliability  −40%, left)
              Brier decomposition      while
                                   overwhile doubling
                                        twelve        resolution
                                               settlement rounds (1,920  right):
                                                                 (+98%,settled   claims
                                                                               claims perget sharper,
                                                                                          round).     not vaguer.
                                                                                                  Settlement  improves
calibration                −40%, left)       doubling resolution (+98%, right):   claims  get sharper, not vaguer.
   calibration (reliability −40%, left) while doubling resolution (+98%, right): claims get sharper, not vaguer.
                                                                                                                                                                                                                    (b) Compute penalty: exact form fits;
        Registered claim                                    Verdict                                (a) Prop. 1 at scale: dots=sim (100k), lines= E[max]                                                               asymptotic overstates up to 24×
       Registered claim                                   Verdict                                                    4
                                                                                                                                                    N                                                105




                                                                                                                                                                                             N to match
                                                                                                                         =0.1          =0.7                                                                          (b)empirical,
                                                                                                                                                                                                                         Compute=0.5
                                                                                                                                                                                                                                   penalty: exact form fits;
          Registered     claim
 H1a Prop. 1 exact (Gaussian)                                 Verdict
                                                              pass

                                                                                                    E[gold of selected] ( )
                                                                                                             (a) Prop. 1 at
                                                                                                                         =0.3          =0.9 (100k), lines= E[max
                                                                                                                            scale: dots=sim                      ]4
                                                                                                                                                              N 10
                                                                                                                                                                                                                       asymptotic
                                                                                                                                                                                                                        exact form overstates up to 24×
                                                                                                               34        =0.5          =1.0                      105                                                     N 2 (asymptotic)
                                                                                                                                                                                                                         1/
 H1a   Prop.
           1/ρ1
              2
                exact   (Gaussian)                            pass




                                                                                                                                                                                     N 0 to match
                                                                                                                           =0.1         =0.7                                                                              empirical, =0.8
                                                                                                                                                                                                                                       =0.5
 H1b
   H1a N1/ρ
          Prop.  accurate
                  1 exact    at practical
                            (Gaussian)      N                  fail
                                                                pass
                                                                                                                                                                                                                         empirical,


                                                                                              E[gold of selected] ( )




                                                                                                                                                                                0
             2                                                                                                 23          =0.3         =0.9                    10 3
                                                                                                                                                                 104
                                                                                                                                                                                                                          exactform
                                                                                                                                                                                                                         exact    form
 H1b Nexchange
             1/ρaccurate    at practical                        fail                                                                                                                                                     NN1/ 2 (asymptotic)




                                                                                                                                                                              proxy budget
                                                                                                                                                                                                                            1/ 2 (asymptotic)
 H1c
   H1b N
                 2 rate transfers      beyond
                    accurate at practical N
                                            N Gaussian         fail
                                                                 fail
                                                                                                                           =0.5         =1.0
                                                                                                                                                                                                     10 2                 empirical, =0.8
                                                                                                                     12                                                                               103
 H2a
 H1c    weak
   H1c exchangeverifier
                    rate collapses
                         transfers     absolutely
                                      beyond
                                         beyondGaussian        fail
                                                                fail                                                                                                                                                      exact form




                                                                                                                                                                        proxy budget
          exchange     rate  transfers           Gaussian        fail∗                                                                                                                               10 1
                                                                                                                                                                                                                          N 1/ 2 (asymptotic)
 H2b
 H2a    strong
   H2a weak
          weak  verifier
              verifier     also
                        collapses
                 verifier        declines
                            collapses absolutely
                                         absolutely         invalid
                                                                fail
                                                                 fail
                                                                                                                     01                                                                               102
                                                                                                                                  22    25      28        211    214                                            22                              23         24
 H2c
 H2b    sound
   H2b strong
          strongverifier
               verifier   monotone
                         also
                   verifier     declines
                             also  declines                   pass∗ ∗
                                                          invalid
                                                             invalid                                                          0         N (candidates)                                                    101                 sound verifier budget N
 H3     anchored
   H2c sound
 H2c      sound      > frozen
                   verifier
               verifier          (gold and drift)
                             monotone
                         monotone                             pass
                                                                pass
                                                              pass
                                                                                                                                   22     25     28
                                                                                                                                         N (candidates)
                                                                                                                                                           211    214                                               22                          23
                                                                                                                                                                                                                               sound verifier budget N
                                                                                                                                                                                                                                                           24

 H4H3 anchoring
          anchored    survives
                          frozen all(gold
                                      3 adversaries
                                           and drift)        partial
                                                                pass
 H5H4 on-policy
                       >
 H3 anchored > frozen (gold and drift)
                        3× labelall
                     ≥ survives      efficiency
                                                              pass
                                                              pass
                                                                                         Figure 8: Theory at scale. (a) Proposition 1 holds to
          anchoring
 H4 anchoring        survives           3 adversaries
                                 all 3 adversaries            partial
                                                            partial                                                                                 . (b)
 H6H5 settlement
          on-policyraises
                       ≥ 3×resolution
                                label efficiency              pass
                                                                pass
                                                                                          Figure over
                                                                                         0.007σ   8: Theory
                                                                                                        100,000    trials (a)
                                                                                                               at scale.   per Proposition
                                                                                                                               point, N to1 2holds
                                                                                                                                                 14
                                                                                                                                                       to
 H5 on-policy ≥ 3× label efficiency                           pass                       Figure 8: Theory at scale. (a)        Proposition
                                                                                                                                2             1 holds   to
   H6     settlement raises resolution                          pass                     But
                                                                                          0.007σ   over 100,000
                                                                                              the asymptotic        trialsNper point,
                                                                                                                penalty     1/ρ
                                                                                                                                   (dashed)     214   (b)
                                                                                                                                         N tooverstates
                                                                                                                                                    .
 H6 settlement raises resolution ∗                            pass                       0.007σ over 100,000 trials per          point,
                                                                                                                                 2       N to 214 . (b)
 Table 2: Pre-registered verdicts. Our registered H2b                                    the
                                                                                          Butempirically  required
                                                                                               the asymptotic   penaltybudget
                                                                                                                           N (dots)
                                                                                                                             1/ρ       by up overstates
                                                                                                                                 2 (dashed)   to 24× at
                                                                                         But
                                                                                          the the
                                                                                         practicalasymptotic    penalty
                                                                                                    N ; therequired
                                                                                              empirically    exact   finite-N
                                                                                                                       budget   form(dashed)
                                                                                                                          N 1/ρ(dots)  by up overstates
                                                                                                                                       (solid)tomatches
                                                                                                                                                  24× at
 criterion
   Table 2:(final    gold below
               Pre-registered      per-task
                                verdicts.  ∗ peak over N ) is
                                            Our registered H2b
Table   2:  Pre-registered    verdicts.  ∗
                                           Our registered  H2b                           the empirically
                                                                                         within
                                                                                          practical N ; therequired
                                                                                                 3.4%.                 budget (dots)
                                                                                                              exact finite-N            by up tomatches
                                                                                                                                form (solid)      24× at
 biased  toward
   criterion        detecting
                (final        decline;
                       gold below      a valid peak
                                     per-task  exploratory
                                                     over N test
                                                             ) is
criterion    (final  gold  below   per-task  peak  over  N ) test
                                                              is                         practical  N
                                                                                          within 3.4%.; the  exact   finite-N   form    (solid)  matches
 shows
   biasedthetoward
               strongdetecting
                       verifier does notacollapse
                                decline;           (see text).
                                           valid exploratory
biased  toward     detecting  decline; a valid exploratory  test                         within 3.4%.
   shows the strong verifier does not collapse (see text).
shows the strong verifier does not collapse (see text).
                                                                                         frozen verifier stays hacked against every adver-
 learned verifier (gradient-boosted trees over 359                                        frozen
                                                                                         sary        verifier gap
                                                                                                (persistent       stays∼0.26–0.28),
                                                                                                                            hacked against         every
                                                                                                                                               while          adver-
                                                                                                                                                        anchored
    learnedheld-out
 features,       verifier (gradient-boosted
                             ρ ≈ 0.77) alongside        trees
                                                           the over
                                                                 shallow359               sary (persistent
                                                                                         settlement
                                                                                         anchored         drivesgap
                                                                                                         settlement  the∼0.26–0.28),
                                                                                                                            gap
                                                                                                                            beat tothe∼0–0.04  whileagainst
                                                                                                                                           frozen       anchored
                                                                                                                                                      verifier   all
                                                                                                                                                                   on
    features,
atridge  verifier
    larger        held-out
               scale, (ρwith     ≈ 0.77)
                               ρevery
                          ≈ 0.50),            alongside
                                       anpass/fail           the shallow
                                            uncertainty-sampling
                                                        criterion     pre-                settlement
                                                                                         three—including   drives     the
                                                                                                                    the      gap    to  ∼0–0.04
                                                                                                                           settlement-aware
                                                                                         achieved gold reward for both verifier classes               against
                                                                                                                                                      adversary, all
    ridge
registered   verifier
 control forbefore      (ρ   ≈
                   the on-policy0.50),   an
                            any experiment    uncertainty-sampling
                                       claim, and—theran. The    gapsuite
                                                                      our                 three—including
                                                                                         which
                                                                                         (weak:    relocated         the
                                                                                                     0.312 vs.to0.180,      settlement-aware
                                                                                                                       unsettled p =regions
                                                                                                                                         2.7 × 10 afteradversary,
                                                                                                                                                      −9  ;each   re-
                                                                                                                                                             strong:
was control
 Limitations
       designed for previously
                     the   on-policy
                      to break     our   claim,
                                         claims,and—the
                                      conceded—a      not to      gap our
                                                            settlement-
                                                                confirm                   which
                                                                                         fit and vs.
                                                                                         0.358      relocated
                                                                                                    still0.272,    to
                                                                                                           could not    unsettled
                                                                                                                     p =sustain        regions
                                                                                                                              5.5 ×inflated  −6
                                                                                                                                         10 ) whileafter
                                                                                                                                                    scores each   re-
                                                                                                                                                               (gap
                                                                                                                                                              reduc-
    Limitations
 aware
them:         uses apreviously
          itadversary      that detects
                         10-token       conceded—a
                                       DSL  refits
                                                withand    10settlement-
                                                        ∼ deliberately
                                                               10 candi-                  fit and
                                                                                         ing
                                                                                         0.039       still
                                                                                                   vs.
                                                                                               anchor       could0.264,
                                                                                                        frozen
                                                                                                            drift     not sustain
                                                                                                                    (−12%         < 10inflated
                                                                                                                              p and      −15
                                                                                                                                         −44%  ; goldscores    (gap
                                                                                                                                                    respectively,
                                                                                                                                                         0.279    vs.
    aware
 relocates    adversary
                to unsettled that  detects
                                  regions.     refits  and
                                                Verdicts    deliberately
                                                             on the    ten                0.039     vs.  frozen
                                                                                                            −7      0.264, −6  p   <
                                                                                                                       10 ).directed   10 −15 ; gold 0.279 vs.
                                                                                                                                   The registered          H4 pres-
                                                                                                                                                                ver-
date   programs        (versus ∼     4.6 × 10      4 ), 16 I/O    points,                both p p< =
                                                                                         0.206,         104.0).×Under                         adversarial
    relocateshypotheses:
 registered       to unsettledsix   regions.
                                        passed,   Verdicts
                                                    three      on theand
                                                            failed,     ten               0.206,
                                                                                         dict  is    p = 4.0 × 10
                                                                                                   nonetheless
                                                                                                                            −6 ). The registered H4 ver-
                                                                                                                       partial:      in  the   steepest-ascent
2–4× more tasks with paired Wilcoxon statistics, a                                       sure (H4; 100 tasks, 300 steps, Figure 11), the
    registered
 one registered     hypotheses:      six  passed,
                       criterion(gradient-boosted     three
                                    was itself invalid;trees  failed,
                                                              we report and               dict anchored
                                                                                         cell,   is nonetheless         partial:      in thefrozen
                                                                                                                                               steepest-ascent
strong    learned verifier                                           over                frozen     verifiergold staysdid      not beat
                                                                                                                           hacked       against every  (0.207     vs.
                                                                                                                                                              adver-
    one  registered
 all offeatures,
         it.             criterion   was    itself  invalid;    we report                 cell,   anchored       gold     did  not
                                                                                                                     Exploratory      beat   frozen
                                                                                                                                         diagnosis      (0.207    vs.
359                    held-out ρ ≈ 0.77) alongside the                                  0.211,    p = 0.46).
                                                                                         sary (persistent         gap    ∼ 0.26–0.28),          while attributes
                                                                                                                                                         anchored
    all of it.                                                                            0.211,
                                                                                         this        p  =
                                                                                               to adversary 0.46).    Exploratory        diagnosis       attributes
shallow ridge verifier (ρ ≈ 0.50), an uncertainty-                                       settlement       drivesparalysis—that
                                                                                                                      the gap to ∼ 0–0.04   hill climber
                                                                                                                                                       against com-all
 What survived—and                 goton-policy
                                         stronger. claim,  The anchor-                    this tocandidates
                                                                                         pares      adversaryagainstparalysis—that
                                                                                                                                a  stale     hill climber
                                                                                                                                          pre-refit     score  com-
                                                                                                                                                                and
sampling        control for the                                    and—                  three—including the settlement-aware adversary,
    What
 inggap       survived—and
       mechanism           replicatedgot   stronger.
                                           everywhere       The
                                                              we anchor-
                                                                    could                 pares candidates
                                                                                         freezes     after the to   against
                                                                                                                   first        a stale pre-refit
                                                                                                                            settlement;       withafter score
                                                                                                                                                      the       and
                                                                                                                                                            incum-
the          our
    ingpressure
         mechanism
                    Limitations       previously
                             replicated     everywhere
                                                        conceded—a
                                                                we could
                                                                                         which
                                                                                          freezes
                                                                                                   relocated
                                                                                                      after    the
                                                                                                                       unsettled
                                                                                                                    first   settlement;
                                                                                                                                       regionswith    the
                                                                                                                                                           each
                                                                                                                                                            incum-
                                                                                                                                                                   re-
 aim
settlement-aware        at  it.   Under       the   settlementrefitsloop                 bent    rescored       after   refits,   anchoring       wins     the  cell
    aim pressure atadversary  it. Under    thatthedetects
                                                      settlement      and
                                                                      loop               fit andrescored
                                                                                          bent      still could      not    sustain     inflatedwins scores (gap
 (H3;   120
deliberately    tasks    weak,
                     relocates    60
                                   to  tasks
                                       unsettledstrong,    12
                                                       regions. rounds),
                                                                     Ver-                too
                                                                                         0.039(0.282      vs. after
                                                                                                                 0.211,  refits,
                                                                                                                             p p=< anchoring
                                                                                                                                     5.8    × 10
                                                                                                                                          −15      −6 ). theWecellre-
    (H3; 120 tasks weak, 60 tasks strong, 12 rounds),                                     too (0.282 vs. 0.211,−6p = 5.8 × 10 ).0.279
                                                                                                   vs.  frozen     0.264,              10       ; gold
                                                                                                                                                   −6       We re- vs.
 anchored
dicts   on thesettlement
                   ten            beathypotheses:
                         registered       the frozen verifier           on               port    the   registered        failure     and    the   diagnosis       to-
    anchored        settlement      beat the frozensix           passed,
                                                             verifier    on              0.206,
                                                                                          port the  p=      4.0 × 10failure
                                                                                                        registered             ). Theandregistered
                                                                                                                                            the diagnosis   H4 ver-
                                                                                                                                                                  to-
 achieved
three            gold
        failed, gold      reward
                    and one          for
                                registered  both     verifier
                                                criterion         classes
                                                              wasclasses
                                                                    itself               gether.
                                                                                         dict   is  Settlement scaling
                                                                                                    nonetheless         partial:  (H5,
                                                                                                                                     in  80
                                                                                                                                         the  tasks)   replicated
                                                                                                                                                steepest-ascent
    achieved                reward     for both        verifier
                                                            −9                            gether. Settlement scaling (H5, 80 tasks) replicated
 (weak: we
invalid;     0.312     vs. all
                  report     0.180,
                                 of it.pp==2.7      × 10 −9; strong:                     with
                                                                                         cell,  a sharper control:
                                                                                                                 gold didSoundness            AUC scales(0.207log-
    (weak: 0.312         vs. 0.180,              2.7
                                                   −6 × 10 ; strong:                      with anchored
                                                                                                  a sharper control:           not beat frozen
                                                                                                                              Soundness        AUC scales          vs.
                                                                                                                                                                log-
           vs. 0.272, p = 5.5 stronger.
 0.358 survived—and
What                                       × 10 ) whileanchor-     reduc-                linearly     in   the   settled      budget      (R  2   =    0.92),    on-
    0.358 vs. 0.272, p =got           5.5 × 10−6 ) The     while reduc-                  0.211,
                                                                                          linearly  p= in 0.46).     Exploratory
                                                                                                            the settled       budget diagnosis
                                                                                                                                          (R2 = 0.92),   attributes
                                                                                                                                                                 on-
 ing
inging anchor
      mechanism     drift   (−12%
                          replicated   and     −44%
                                          everywhere      respectively,
                                                              we could                   policy
                                                                                         this  to  settlement
                                                                                                    adversary        at S=300 already
                                                                                                                    paralysis—that           hill beats
                                                                                                                                                   climberrandom
                                                                                                                                                               com-
         anchor−7     drift   (−12% and          −44% respectively,                       policy settlement at S=300 already−4                    beats random
 both
aim     p    <
       pressure  10     ).  Under     directed     adversarial       pres-               labeling      at S=3000          (p =a 3.7      × 10 −4; the        ∼10×
    both    p < 10 at ).it.Under
                       −7        Under       the settlement
                                        directed     adversarialloop  pres-              pares
                                                                                          labelingcandidates
                                                                                                        at S=3000  against (p = stale
                                                                                                                                    3.7 ×pre-refit
                                                                                                                                             10 ; the    score
                                                                                                                                                             ∼10×and
 sure 120
(H3;    (H4;tasks        tasks, 60
                  100 weak,        300    steps,
                                      tasks          Figure
                                                strong,         11), the
                                                           12 rounds),                   multiplier),
                                                                                         freezes     afterand thethefirstuncertainty-sampling
                                                                                                                            settlement; with thecontrol      incum-
    sure (H4;        100 tasks,      300    steps,    Figure     11), the                 multiplier),       and   the    uncertainty-sampling              control

                                                                                  9
                                         (a) Best-of-N: plateau, not collapse (120 tasks)                     (b) Relative soundness degrades for both      tered claimspenalty
                                                                                                                                                          closed-form             did not issurvive,          all on the quantitative-
                                                                                                                                                                                                  asymptotic-only              (H1b): at
                                       0.6         sound (execution)                                    1.0
                                                                                                                                                            theorythe  side.empirical
                                                                                                                                                                                 (i) The exchange               rate does      not    transfer
                        of selection

                                                   strong learned (GBM)
                                       0.5(a) Best-of-N: learned
                                                   weak   plateau,  not collapse (120 tasks)
                                                                 (ridge)                                0.8
                                                                                                              (b) Relative soundness degrades for both    ρ=0.5                                 budget
                                                                                                                                                          closed-form penalty is asymptotic-only (H1b):        needed       to   match      ata
                                       0.6
                                       0.4         sound (execution)                                    1.0
                                                                                                                                                            quantitatively
                                                                                                                                                          sound      verifier      at (H1c):
                                                                                                                                                                                       N    ∈   {4,across
                                                                                                                                                                                                      8,   16}   120
                                                                                                                                                                                                                   is    tasks
                                                                                                                                                                                                                       8–24×      the    order-
                                                                                                                                                                                                                                   smaller
                  selection




                                                                                                                                                          ρ=0.5 the2 empirical budget needed to match a




                                                                                          Snd@N Snd@N
                                                   strong learned (GBM)
                                       0.5
                                       0.3         weak learned (ridge)                                 0.6
         gold ofreward




                                       0.4
                                       0.2
                                                                                                        0.8
                                                                                                                    strong (GBM)
                                                                                                                                                            ing N
                                                                                                                                                          than
                                                                                                                                                          sound   isverifier
                                                                                                                                                                      preserved
                                                                                                                                                                     1/ρ
                                                                                                                                                                                   at N(Spearman
                                                                                                                                                                              predicts,     ∈while
                                                                                                                                                                                                {4, 8,the  16}0.59
                                                                                                                                                                                                               exact   between
                                                                                                                                                                                                                         finite-N
                                                                                                                                                                                                                   is 8–24×          per-task
                                                                                                                                                                                                                                       form
                                                                                                                                                                                                                                   smaller
                                       0.3                                                              0.4
                                                                                                        0.6         weak (ridge)
                                                                                                                                                            ρ  and
                                                                                                                                                          matches     realized
                                                                                                                                                                        within                  (Figure
                                                                                                                                                                                       Snd@4096),              but
                                                                                                                                                                                                              8b);    the   realized
                                                                                                                                                                                                                            corollary      frac-
                                                                                                                                                                                                                                             is
 gold reward




                                       0.1                                                                          sound = 1
                                                                                                                                                          than N     1/ρ   2
                                                                                                                                                                                     3.4%
                                                                                                                                                                              predicts, while the exact finite-N form
                                       0.2                                                                          strong3(GBM) 5
                                       0.1
                                                21     23     25
                                                                   N
                                                                       27     29   211                  0.4      21 weak2(ridge)
                                                                                                                    sound = 1
                                                                                                                                 2
                                                                                                                                   N
                                                                                                                                     27     29   211
                                                                                                                                                            tion
                                                                                                                                                          now      falls
                                                                                                                                                                  stated     short
                                                                                                                                                                             with      of
                                                                                                                                                                                     that  ρ   on
                                                                                                                                                                                             caveat. 76%
                                                                                                                                                          matches within 3.4% (Figure 8b); the corollary is    of
                                                                                                                                                                                                           (iii)    tasks
                                                                                                                                                                                                                   Absolute  (median
                                                                                                                                                                                                                                 collapse    gap
                                                21     23     25
                                                                   N
                                                                       27     29   211                           21    23     25
                                                                                                                                   N
                                                                                                                                       27   29   211      is0.27;
                                                                                                                                                          now         mean
                                                                                                                                                              domain-dependent
                                                                                                                                                                  stated     with 0.32
                                                                                                                                                                                     thatrealized
                                                                                                                                                                                              (H2a):
                                                                                                                                                                                             caveat. (iii)  vs. ρAbsolute
                                                                                                                                                                                                           in   the   rich   domain
                                                                                                                                                                                                                       ≈ 0.50).         Propo-
                                                                                                                                                                                                                                 collapse the
  Figure 9: Goodharting in the rich domain (120 tasks,                                                                                                    weak
                                                                                                                                                            sition  verifier’s
                                                                                                                                                                      1   should     gold     reward
                                                                                                                                                                                       therefore          beplateaus
                                                                                                                                                                                                               read     as (0.191
                                                                                                                                                                                                                            an         peak
                                                                                                                                                                                                                                 optimistic
Figure 9: Goodharting in the rich domain (120 tasks,                                                                                                      is domain-dependent (H2a): in the rich domain the
  ±1 s.e.). (a) The weak verifier plateaus rather than                                                                                                    atceiling    once0.184 thegold at N
                                                                                                                                                                                       proxy      has exploitable decline(0.191
                                                                                                                                                                                                                              not signif-
                                                                                                                                                                                                                             structure;
±1Figure
      s.e.).9: (a)
                Goodharting
                     The weakinverifier
                                  the richplateaus
                                           domain rather
                                                    (120 tasks,
  collapsing; the strong verifier keeps climbing through
                                                            than                                                                                          weakN =256,
                                                                                                                                                                    verifier’s                    =4096;
                                                                                                                                                                                              reward        plateaus                   peakwe
  ±1 s.e.). (a)
collapsing;      theThe   weak
                      strong     verifier
                              verifier    plateaus
                                       keeps       rather
                                             climbing      than
                                                        through                                                                                           icant,
                                                                                                                                                          athave    revised
                                                                                                                                                                    p
                                                                                                                                                              N =256,  =     0.25)
                                                                                                                                                                              0.184    instead
                                                                                                                                                                                   §3 accordingly.   of
                                                                                                                                                                                         at N =4096; (ii) inverting
                                                                                                                                                                                                                  decline  as
                                                                                                                                                                                                                       The not it  does
                                                                                                                                                                                                                              closed-form
                                                                                                                                                                                                                                     signif-in
  N =4096. (b) Relative soundness Snd@N nonetheless
N collapsing;
    =4096. for (b)theRelative
                      strong verifier
                              soundnesskeeps climbing  through
                                                   nonetheless                                                                                            the   minimal
                                                                                                                                                            penalty p =is0.25)  domain—the
                                                                                                                                                                                       instead ofcollapse
                                                                                                                                                                               asymptotic-only                 (H1b):ofasat  Figuredoes3 in  isthe
  degrades          both (0.94   → 0.32 Snd@N
                                          weak, 0.94   → 0.59                                                                                             icant,                                          inverting            itρ=0.5
  N  =4096.
degrades        (b)  Relative
              for bothis(0.94  soundness
                                 → 0.32   Snd@N
                                          weak,evennonetheless
                                                        → 0.59
                                                 0.94when                                                                                                 real   but    not    universal         at  these       pressures.        Finally,
  strong): pressure       increasingly  wasted,             it is                                                                                           empirical
                                                                                                                                                          the   minimalbudget   domain—theneeded to          match of
                                                                                                                                                                                                         collapse        a sound
                                                                                                                                                                                                                             Figureverifier
                                                                                                                                                                                                                                         3 is
  degradespressure
strong):       for bothis(0.94
                           increasingly   weak, 0.94
                                 → 0.32 wasted,   even →   0.59it
                                                        when                                                                                              our    own    registered
  not inverted.                                                                                                                                             at N
                                                                                                                                                          real   but∈not          8, 16}H2b
                                                                                                                                                                          {4,universal              criterion
                                                                                                                                                                                              isat8–24×              turnedthan
                                                                                                                                                                                                                  smaller
                                                                                                                                                                                                     these pressures.           out    toNbe
                                                                                                                                                                                                                                   Finally, 1/ρ2
isstrong):   pressure is increasingly wasted, even when it is
    not inverted.                                                                                                                                         statistically        invalid      (comparing             a turned
                                                                                                                                                                                                                      final   value
  not inverted.                                                                                                                                             predicts,
                                                                                                                                                          our                while
                                                                                                                                                                 own registered         theH2b exact       finite-N
                                                                                                                                                                                                    criterion              form        totobea
                                                                                                                                                                                                                                outmatches
                                                                                                                                                          per-task
                                                                                                                                                            within 3.4%
                                                                                                                                                          statistically maximum     (Figure
                                                                                                                                                                               invalid       over8b);
                                                                                                                                                                                            (comparing13 noisy          points
                                                                                                                                                                                                              thea corollary
                                                                                                                                                                                                                      final   value detects
                                                                                                                                                                                                                                       istonowa
                                                                       Settlement scaling (80 tasks)
                                                                                                                                                          “decline”
                                                                                                                                                          per-task
                                                                                                                                                            stated with  even
                                                                                                                                                                        maximum    in  monotone
                                                                                                                                                                                 that caveat.over 13      curves),
                                                                                                                                                                                                        (iii)noisy
                                                                                                                                                                                                                Absoluteand   the    honest is
                                                                                                                                                                                                                        pointscollapse
                                                                                                                                                                                                                                    detects
                                                                       Settlement   scaling (80 tasks)
                                                                        on-policy settlement                                                              exploratory          answer        runs     against
                                                          uncertainty sampling                                                                            “decline”      even
                                                                                                                                                            domain-dependent       in monotone (H2a):       in theour
                                                                                                                                                                                                          curves),      andgeneralized
                                                                                                                                                                                                                        rich  the
                                                                                                                                                                                                                               domainhonestthe
                                                0.65      on-policy settlement                                                                            claim:     the    strong     verifier’s       gold     reward      rises   mono-
                                                          random labels                                                                                   exploratory          answer        runs     against
                                                                                                                                                            weak verifier’s gold reward plateaus (0.191              our    generalized    peak
                                       AUCAUC




                                                0.65      uncertainty sampling                                                                            tonically      through        N   =4096         (0.056       →   0.357;      4096
                                                          random labels                                                                                   claim:     the strong
                                                                                                                                                            at N =256,          0.184  verifier’s
                                                                                                                                                                                            at N =4096; gold reward  decline rises
                                                                                                                                                                                                                                 notmono-signif-
                                                0.60                                                                                                      vs.                                    even(0.056as its Snd@N             erodes
                                Soundness




                                                                                                                                                                1024: p = 0.0023)
                                                                                                                                                          tonically
                                                                                                                                                            icant, p through
                                                                                                                                                                          = 0.25)Ninstead   =4096       of inverting   → 0.357;        4096 in
                                                                                                                                                                                                                              as it does
                                                0.60                                                                                                      to
                                                                                                                                                          vs. 0.59.      Within        the    pressure
                                                                                                                                                                                                 even      as  this
                                                                                                                                                                                                                 its   suite   coulderodesap-
                             Soundness




                                                                                                                                                                1024:     p    =   0.0023)
                                                                                                                                                            the minimal domain—the collapse of Figure 3 is            Snd@N
                                                0.55                                                                                                      ply,
                                                                                                                                                          toreal  verifier      strength        bought real           robustness,         not
                                                                                                                                                              0.59.but Within
                                                                                                                                                                          not universalthe pressureat these    thispressures.
                                                                                                                                                                                                                       suite could        ap-
                                                                                                                                                                                                                                      Finally,
                                                0.55                                                                                                      merely
                                                                                                                                                          ply,         delay.
                                                                                                                                                                  verifier           Whether
                                                                                                                                                                                strength        boughta   strong
                                                                                                                                                                                                              real     verifier
                                                                                                                                                                                                                      robustness,   inverts
                                                                                                                                                                                                                                          not
                                                                                                                                                            our own registered H2b criterion turned out to be
                                                0.50                                                                                                      at  pressures
                                                                                                                                                          merely       delay.   beyond
                                                                                                                                                                                     Whether  N =4096 a strong  is open;      what     is al-
                                                                                                                                                            statistically
                                                                                                                                                          ready     established
                                                                                                                                                                                  invalid
                                                                                                                                                                                        is that
                                                                                                                                                                                               (comparing
                                                                                                                                                                                                   its   compute
                                                                                                                                                                                                                      averifier
                                                                                                                                                                                                                         final
                                                                                                                                                                                                                        is
                                                                                                                                                                                                                                    inverts
                                                                                                                                                                                                                                  value
                                                                                                                                                                                                                           increasingly
                                                                                                                                                                                                                                             to a
                                                0.50 10        101         102        103                                                                 atper-task
                                                                                                                                                              pressures         beyond                          is  open;     what     is  al-
                                                        0                                                                                                                                     N  =4096
                                                                                                                                                          wasted           maximum
                                                                                                                                                                      relative       toisathat  over 13
                                                                                                                                                                                             sound              noisy points isdetects
                                                                                                                                                                                                          verifier—which                  the
                                                     100  settled-label
                                                               101        budget
                                                                           102   S ( +1
                                                                                      10)3                                                                ready
                                                                                                                                                           “decline”established
                                                                                                                                                                            even     in  monotone  its compute
                                                                                                                                                                                                             curves),   is and
                                                                                                                                                                                                                           increasingly
                                                                                                                                                                                                                                  the honest
                                                                                                                                                          economic         argument          for   settlement
                                                                                                                                                          wasted relative to a sound verifier—which is the             either   way.      We
                                                                            settled-label budget S (+1)                                                     exploratory           answer        runs      against       our generalized
 Figure 10: Settlement scaling at scale (80 tasks). On-
                                                                                                                                                          also
                                                                                                                                                          economicnote the       toy
                                                                                                                                                                           argument    suite’s      inverted
                                                                                                                                                                                             for settlement         hacking
                                                                                                                                                                                                                       either way.gap (§6,We
                                                                                                                                                            claim:
                                                                                                                                                          Result       the
                                                                                                                                                                     3) did   strong      verifier’s       gold     reward      rises    mono-
 policy settlement scales log-linearly (R2 =0.92) and
 Figure 10: Settlement scaling at scale (80 tasks). On-
                                                                                                                                                          also    note    the nottoy reproduce
                                                                                                                                                                                       suite’s inverted  at scale:      anchored
                                                                                                                                                                                                                    hacking       gapgaps(§6,
                                                                                                                                                          gotonically       through N =4096
                                                                                                                                                               to approximately                zero (honest  (0.056 → 0.357;               4096
Figure  10: both
 dominates   Settlement
                  randomscaling  at scale
                           labeling  and an(80uncertainty-
                                               tasks). On-
 policy settlement scales log-linearly (R22=0.92) and                                                                                                     Result     3) did not reproduce                at scale:pricing)
                                                                                                                                                                                                                        anchoredrather  gaps
                                                                                                                                                            vs.
                                                                                                                                                          than   1024:       p   =   0.0023)         even      as   its  Snd@N          erodes
policy settlement
 sampling           scales on-policy
          control: S=300   log-linearly   (Rbeat
                                      labels  =0.92)
                                                 S=3000
 dominates both random labeling and an uncertainty-
                                                       and                                                                                                go tonegative
                                                                                                                                                                    approximately (conservative           distrust).
                                                                                                                                                                                               zero (honest            pricing) rather
 random labels.
dominates   both  random   labeling  and   an uncertainty-                                                                                                  to 0.59. Within the pressure this suite could apply,
 sampling control: S=300 on-policy labels beat S=3000                                                                                                     than negative (conservative distrust).
sampling    control: S=300 on-policy labels beat
 random labels.                                                                                                                                           8verifier     strength and
                                                                                                                                                                 Real-Code              bought       real robustness, not merely
                                                                                                                                                                                                Real-Model
S=3000 random labels.                                                                                                                                       delay.    Whether a strong verifier inverts at pressures
 barely improves on random (0.587 vs. 0.579 at                                                                                                                   Experiments
                                                                                                                                                          8 Real-Code                  and Real-Model
                                                                                                                                                            beyond N =4096 is open; what is already estab-
 barely improvesefficiency
 S=3000)—the         on random  comes  specifically
                                   (0.587           from
                                            vs. 0.579  at                                                                                                        Experiments
                                                                                                                                                            lished is testbeds,
                                                                                                                                                          Synthetic         that its compute howeverishardened,  increasingly          wasted
                                                                                                                                                                                                                               are prox-
 settling
bent      where   selection
       rescored after
 S=3000)—the                 pressure
                        refits, comes
                   efficiency          concentrates,
                                anchoring             not
                                            wins thefrom
                                       specifically   cell                                                                                                  relative
                                                                                                                                                          ies.    We to
                                                                                                                                                          Synthetic           a soundran
                                                                                                                                                                         therefore
                                                                                                                                                                            testbeds,       verifier—which
                                                                                                                                                                                                  two further
                                                                                                                                                                                             however          hardened,  is theare economic
                                                                                                                                                                                                                        pre-registered prox-
 from
too     generic
      (0.282
 settling     vs.active
          where    0.211,learning.
                  selection    = 5.8Calibration-versus-
                            ppressure    10−6 ). Wenot
                                       concentrates,
                                       ×               re-                                                                                                suites
                                                                                                                                                            argumenton   real for substrate
                                                                                                                                                                                    settlement    (criteria
                                                                                                                                                                                                        either
                                                                                                                                                          ies. We therefore ran two further pre-registered        frozen
                                                                                                                                                                                                                    way.     before
                                                                                                                                                                                                                            We      alsoexe-
                                                                                                                                                                                                                                           note
 resolution
 from        (H6,
        generic     100
                 active   tasks, 15
                         learning.
port the registered failure and −10  rounds)  replicated:
                                     Calibration-versus-
                                       the diagnosis to-                                                                                                  cution;
                                                                                                                                                            the toy
                                                                                                                                                          suites      raw
                                                                                                                                                                    on suite’sdata    and
                                                                                                                                                                         real substrate      code
                                                                                                                                                                                       inverted        released).
                                                                                                                                                                                                        hacking
                                                                                                                                                                                                  (criteria       frozen The   real-code
                                                                                                                                                                                                                        gapbefore
                                                                                                                                                                                                                               (§6, Result
                                                                                                                                                                                                                                         exe-
 resolution
 resolution
gether.      +70%
             (H6, 100
         Settlement   (p =tasks,
                       scaling   ×
                             3.2(H5,      ) with
                                 1510rounds)
                                     80 tasks)   reliabil-
                                              replicated:
                                               replicated                                                                                                 suite    uses    MBPP        (Austin        et  al.,
                                                                                                                                                          cution; raw data and code released). The real-codego
                                                                                                                                                            3)   did   not     reproduce          at    scale:   2021):     974
                                                                                                                                                                                                                     anchored       human-
                                                                                                                                                                                                                                     gaps
 ity
with improved,
 resolution
       a sharper
             +70%not  traded  away.   −10
                      (p = 3.2Soundness
                   control:      × 10 ) withAUCreliabil-
                                                   scales                                                                                                 written
                                                                                                                                                          suite    usesPython
                                                                                                                                                                           MBPPprograms
                                                                                                                                                            to approximately                          et whose
                                                                                                                                                                                           zero (honest
                                                                                                                                                                                       (Austin                         real974
                                                                                                                                                                                                                   pricing)
                                                                                                                                                                                                          al., 2021):         unit
                                                                                                                                                                                                                                rather tests,
                                                                                                                                                                                                                                    human-  than
 ity
 Whatimproved,
log-linearly     innot
           failed—andthetradedhowaway.
                          settled  budget   (R2 =it.0.92),
                                     we repair             Three on-                                                                                      executed        locally,       are    the     sound       verifier;      learned
                                                                                                                                                            negative
                                                                                                                                                          written          (conservative
                                                                                                                                                                       Python         programs      distrust).
                                                                                                                                                                                                          whose real unit tests,
policy    settlement
 registered     claims   at did
                            S=300
 What failed—and how we repair   not   already
                                        survive, beats
                                                    all  random
                                                         on
                                                    it. Three   the                                                                                       verifiers
                                                                                                                                                          executedare           trained
                                                                                                                                                                          locally,       areacross
                                                                                                                                                                                                the sound  problems         (486learned
                                                                                                                                                                                                                    verifier;        train /
labeling    at               (p                 −4 ; the ∼ 10×
 quantitative-theory
 registered claims did not survive, allrate
                           side. (i) The  exchange       on does                                                                                          487
                                                                                                                                                            8 eval),    arelike      reward        models,         over surface          and/
                S=3000           =  3.7  ×  10                  the                                                                                       verifiersReal-Code    trained     and
                                                                                                                                                                                             across      Real-Model
                                                                                                                                                                                                           problems         (486 Experi-
                                                                                                                                                                                                                                     train
multiplier),
 not  transfer  and    the  uncertainty-sampling
                 quantitatively     (H1c):   across
 quantitative-theory side. (i) The exchange rate      120 control
                                                            tasks
                                                             does                                                                                         AST      features
                                                                                                                                                          487 eval),               of  real    code.       The      real-model         suite,
                                                                                                                                                                   mentslike reward models, over surface and
barely
 the      improves
 not ordering
      transfer          on random
                  is preserved
                 quantitatively          (0.587
                                  (Spearman
                                    (H1c):        vs.120
                                                 0.59
                                             across     0.579
                                                            tasksat
                                                        between                                                                                           run by
                                                                                                                                                          AST         the author
                                                                                                                                                                   features        of realagainst
                                                                                                                                                                                               code.the    The  production
                                                                                                                                                                                                                    real-model     Claude
                                                                                                                                                                                                                                       suite,
 per-task
S=3000)—the
 the         ρ and
      ordering        realized Snd@4096),
                      efficiency
                  is preserved    (Spearman       but between
                                   comes specifically
                                                 0.59   the from
                                                              real-                                                                                       API,
                                                                                                                                                          run    byuses
                                                                                                                                                            Synthetic theaauthor
                                                                                                                                                                               real generator
                                                                                                                                                                              testbeds,         however
                                                                                                                                                                                          against        (claude-haiku-4-5,
                                                                                                                                                                                                         the      hardened, Claude
                                                                                                                                                                                                                production          are 32–
                                                                                                                                                                                                                                          prox-
 ized  fraction
settling   where   falls  short
                    selection    of    on
                                 pressure
                                     ρ           of  tasks
                                            concentrates,
                                           76%
 per-task ρ and realized Snd@4096), but the real-            (me-not                                                                                      48   samples/problem),
                                                                                                                                                            ies.    We     therefore           two
                                                                                                                                                                                             ran       real
                                                                                                                                                                                                     two
                                                                                                                                                          API, uses a real generator (claude-haiku-4-5, 32–   LLM
                                                                                                                                                                                                              further   judges     scoring
                                                                                                                                                                                                                           pre-registered
 dian
from    gap
        generic
             0.27;    mean
                   active     0.32   realized
                             learning.          vs.
                                          Calibration-versus-
 ized fraction falls short of ρ on 76% of tasks (me- ρ  ≈  0.50).                                                                                         code
                                                                                                                                                          48suites without
                                                                                                                                                                      on real
                                                                                                                                                               samples/problem), executing
                                                                                                                                                                                    substrate  twoit (criteria
                                                                                                                                                                                                      (claude-haiku-4-5
                                                                                                                                                                                                       real LLMfrozen   judgesbefore  weak;ex-
                                                                                                                                                                                                                                   scoring
 Proposition
resolution
 dian gap 0.27;   1 should
               (H6,           therefore
                       100 tasks,
                      mean    0.32         be read
                                      15 rounds)
                                     realized   vs. ρas ≈an0.50).
                                                             opti-
                                                     replicated:                                                                                          claude-sonnet-4-6
                                                                                                                                                            ecution).
                                                                                                                                                          code     without   The          strong),
                                                                                                                                                                                    real-code
                                                                                                                                                                                 executing                and     local   execution
                                                                                                                                                                                                       suite uses MBPP weak;
                                                                                                                                                                                                  it (claude-haiku-4-5                     of
                                                                                                                                                                                                                                      (Austin
 mistic
resolutionceiling
 Proposition  +70%1 once(pthe
                    should     proxy hasbeexploitable
                            =therefore
                               3.2×10     −10 )read      anstruc-
                                                withasreliability
                                                             opti-                                                                                        the   real2021):
                                                                                                                                                            et al.,   test suites
                                                                                                                                                          claude-sonnet-4-6        974ofstrong),
                                                                                                                                                                                             MBPP and
                                                                                                                                                                                           human-written  and HumanEval
                                                                                                                                                                                                                  localPython
                                                                                                                                                                                                                          execution  (Chen
                                                                                                                                                                                                                                   programsof
 ture;
improved,we   have
 mistic ceiling       revised
               not once
                    traded       §3
                           theaway.   accordingly.      (ii)
                               proxy has exploitable struc-    The                                                                                        et  al.,
                                                                                                                                                            whose
                                                                                                                                                          the       2021)      as
                                                                                                                                                                        realsuites
                                                                                                                                                                real test           gold.
                                                                                                                                                                                  unitoftests,
                                                                                                                                                                                             MBPP     executed
                                                                                                                                                                                                          and HumanEval locally, (Chen are the
What
 ture; wefailed—and
              have revised how§3  weaccordingly.
                                       repair it. Three (ii) regis-
                                                               The                                                                                        etsound     verifier;
                                                                                                                                                              al., 2021)              learned verifiers are trained across
                                                                                                                                                                               as gold.

                                                                                                                                                         10
                                          steepest ascent                     evolutionary                                          settlement-aware
                                                                                                                            steepest ascent                     evolutionary
                                0.6                                0.6                                                     0.6
           gold reward


                                                       sound                                                        0.6                              0.6
                                0.4                                0.4                                                     0.4




                                                                                               gold reward
                                                       anchored
                                                       frozen                                                                             sound
                                                                                                                    0.4                   anchored   0.4
                                0.2                                0.2                                                     0.2            frozen
                                                                                                                    0.2                              0.2
                                0.0                                0.0                                                     0.0
                                                                   0.3                                              0.0   0.30                       0.0
    hacking gap (proxy gold)




                               0.25                                                                                       0.25                       0.3




                                                                                        hacking gap (proxy gold)
                               0.20                                0.2                                             0.25   0.20
                               0.15                                                                                0.20   0.15                       0.2
                                                                   0.1                                             0.15
                               0.10                                                                                       0.10
                                                                                                                                                     0.1
                               0.05                                                                                0.10   0.05
                                                                   0.0
                               0.00                                                                                0.05   0.00                       0.0
                                      0    100     200       300         0    100     200 0.00 300                                 0    100     200      300
                                          adversary step                     adversary step     0                                100   adversary
                                                                                                                                       200       step 0
                                                                                                                                               300              100      200     300
                                                                                                                            adversary step                     adversary step
 Figure 11: Adversarial pressure at scale (100 tasks, 300 steps, ±1 s.e.). Top: gold reward of the adversary’s
Figure 11: Adversarial pressure at scale (100 tasks, 300 steps, ±1 s.e.). Top: gold reward of the adversary’s
 champion against sound (green), anchored (blue), and frozen (red) verifiers,      for steepest-ascent,  evolutionary,  and300 steps, ±1 s.e.)
champion against sound (green), anchored (blue), and frozenFigure (red) 11:  Adversarial
                                                                        verifiers,         pressure at scale
                                                                                   for steepest-ascent,       (100 tasks,
                                                                                                         evolutionary,   and
 settlement-aware adversaries. Bottom: hacking gap (proxy −champion
                                                                 gold). Frozen  verifiers
                                                                           against  soundstay   hacked
                                                                                            (green),   (gap ∼0.26–0.28);
                                                                                                     anchored  (blue), and frozen (red) verifier
settlement-aware adversaries. Bottom: hacking gap (proxy − gold). Frozen verifiers stay hacked (gap ∼ 0.26–0.28);
 anchored settlement drives the gap to ∼0 against all three adversaries,   including
                                                                settlement-aware       the one that
                                                                                   adversaries.      models
                                                                                                 Bottom:    the settlement
                                                                                                          hacking  gap (proxy − gold). Frozen
anchored settlement drives the gap to ∼ 0 against all three adversaries, including the one that models the settlement
 process. The steepest-ascent gold cell is the registered failure discussed
                                                                anchored     in the text.
                                                                          settlement   drives the gap to ∼0 against all three adversaries, inclu
process. The steepest-ascent gold cell is the registered failure discussed in the text.
                                                                process. The steepest-ascent gold cell is the registered failure discussed in

                                               best-of-Nmodels,                     surface verifier falls from Snd@4 = 0.325 to
problems (486Real  trainLLM
                         / 487judges
                                 eval),under
                                         like reward                                                                                                                  surface verifi
            1.00                           weak mbpp                                               Real LLM
                                                                                    Snd@256 = 0.016,      andjudges
                                                                                                               evenunder   best-of-N
                                                                                                                    the gradient-boosted
over surface and AST features ofweakreal              code. The
                                                 humaneval                                    1.00
            0.95                           strong mbpp                              verifier reaches  only 0.052 — real      code under a
                                                                                                                       weak mbpp                                      Snd@256 = 0
real-model suite, run by the author            against
                                           strong humanevalthe pro-                                                    weak humaneval
                                                                                                                                                                      verifier reache
            0.90 API, uses a real generatorsound = 1                                global verifier
                                                                                              0.95 is a far harsher regime      than any of
                                                                                                                       strong mbpp
duction Claude                                             (claude-                                                    strong humaneval
                          Snd@N




                                                                                    our per-task
                                                                                              0.90synthetic worlds. sound = 1                                         global verifier
            0.85
haiku-4-5, 32–48 samples/problem), two real LLM
                                                                                                              Snd@N




                                                                                                                                                                      our per-task sy
judges scoring
            0.80 code without executing it (claude-                                            0.85
                                                                                    Judge capability          buys robustness (registered
haiku-4-50.75 weak; claude-sonnet-4-6 strong), and                                             0.80
                                                                                    pass, against        our strong-form thesis). The                                 Judge capab
local execution 0of the1 real 2test suites        of MBPP       and                 strong judge’s
                                                                                               0.75 soundness AUC exceeds the weak                                    pass, agains
                  2      2       2      23      24       25                                                                             −4 ), and—                    strong judge’s
HumanEval (Chen et al., 2021)        N    as  gold.                                 judge’s (0.85620 vs.21 0.814,    22 p=9×10
                                                                                                                            23      24     25
The Goodhart mechanism is real (registered                                          exploratory—its own N =2N → 32 degradation                                        judge’s (0.85
                                                                                    is not significant (0.855 → 0.821, p=0.43).                                       exploratory—
passes).
 Figure 12:TheRealweak
                    LLM LLMjudgesjudge     loses Soundness-
                                    under best-of-N        selection
                                                                                    This                                                                              is not signifi
                                                                                    Figureconverges       withjudges
                                                                                                                  §7’sunder
                                                                                                                         finding     that aselection
                                                                                                                                               strong
under-Pressure
 over real generated as code
                        N grows:
                               (executed
                                       Snd@2tests as= gold;
                                                        0.835prob-
                                                                 →                   Figure 12: Real LLM                        best-of-N
                                                                                             12: Real LLM      judges   under   best-of-N    selection                This converge
                                                                                     over realverifier
                                                                                    learned    generated    codeclimbing:
                                                                                                                   (executed tests     as gold;  prob-
Snd@32 = 0.729 on MBPP (p=10 , n=60)/
 lems  with  zero  gold  variance    excluded,       −4
                                                  n=60      MBPP                    over real generated code (executed tests as gold;inde-
                                                                                                          kept                   across   two     prob-
 18 HumanEval).       The weak     judge’s Snd@N          degrades                   lems
                                                                                    pendentwith   zero gold   variance  excluded,     n=60   MBPP
                                                                                                                                                binds//               learned verifie
and   0.889 → 0.750          on HumanEval            (p=.004)—                      lems withmethodologies,
                                                                                                 zero gold variance theexcluded,
                                                                                                                         verification n=60gapMBPP
 significantly on both benchmarks; the strong judge is                               18 HumanEval). The weak judge’s Snd@N degrades                                   pendent metho
Figure 12. On real human code with cross-problem                                    conditionally—when
                                                                                    18  HumanEval). The weak   judge judge’s
                                                                                                                       capability     is at or
                                                                                                                                  Snd@N         below
                                                                                                                                             degrades
 significantly more robust.                                                          significantly on both benchmarks; the strong judge is                            conditionally—
verifiers, the collapse is catastrophic: the surface                                significantly
                                                                                    task             on
                                                                                         difficulty—and both   benchmarks;
                                                                                                              scaling
                                                                                     significantly more robust.         the     the
                                                                                                                             judge   strong   judge
                                                                                                                                      materially     is
                                                                                                                                                    re-
                                                                                    significantly   more   robust.
                                                                                    pairs soundness at the pressures we could apply.                                  task difficulty—
verifier falls from Snd@4 = 0.325 to Snd@256 =                                                                                                                        pairs soundne
0.016,     and evenmechanism
                         the gradient-boosted               verifier                Whether the repair persists at frontier-difficulty
 The Goodhart                           is real (registered                                                                                                           Whether the
reaches   only   0.052—real       code  under      a global    veri-                tasks  under RL-scale
                                                                                     The Goodhart                 pressureisisreal
                                                                                                           mechanism               precisely     what
                                                                                                                                        (registered
 passes). The weak LLM judge loses Soundness-                                       (0.856   vs.  0.814,  p=9×10       −4 ), and—exploratory—                         tasks under R
fier is a far harsher                                                               RSR-Bench
                                                                                     passes). The    (§9)weak
                                                                                                           mustLLMmeasure.
                                                                                                                        judge loses Soundness-
 under-Pressure      as regime
                         N grows:  thanSnd@2
                                         any of our        per-task
                                                     = 0.835      →                 its own N =2 →                 degradation                                        RSR-Bench (§
synthetic   worlds.                                                                  under-Pressure      as N 32grows:      Snd@2is=not        signifi-
                                                                                                                                           0.835    →
 Snd@32 = 0.729 on MBPP (p=10 , n=60)                 −4                            Anchoring:
                                                                                    cant  (0.855     the
                                                                                                      →  mechanism
                                                                                                          0.821,          matters,
                                                                                                                    p=0.43).       This and  so  does
                                                                                                                                          converges
Judge    capability      buysonrobustness           (registered                      Snd@32 = 0.729 on MBPP (p=10 , n=60)                −4                           Anchoring: th
 and 0.889       → 0.750             HumanEval          (p=.004)                    headroom
                                                                                    with            (registered     failures,      reported).       In
pass,  against                                                                       and §7’s
                                                                                           0.889 finding   that a strong
                                                                                                      → 0.750               learned
                                                                                                                    on HumanEval        verifier  kept
                                                                                                                                           (p=.004)                   headroom (r
— Figure       12.ourOnstrong-form
                          real humanthesis).code with The strong
                                                              cross-                the LLM
                                                                                    climbing:   settlement     loop   (40  problems,      8 rounds),
judge’s   soundness     AUC     exceeds     the   weak      judge’s                 — Figure across12. On  tworeal
                                                                                                                 independent
                                                                                                                     human code     methodologies,
                                                                                                                                         with cross-                  the LLM settle
 problem verifiers, the collapse is catastrophic: the                               neither
                                                                                    the      anchored arm
                                                                                         verification           raised achieved       gold over the
                                                                                     problem    verifiers,gapthe binds
                                                                                                                  collapse conditionally—when
                                                                                                                              is catastrophic: the                    neither anchor

                                                                               11
judge capability is at or below task difficulty—and            Mechanism             Loop drift     Adv. |gap|
scaling the judge materially repairs soundness at              frozen judge (none)     0.352            0.326
the pressures we could apply. Whether the repair               in-context ledger       0.397            0.457
persists at frontier-difficulty tasks under RL-scale           isotonic model            —        tail +0.52→0.76
pressure is precisely what RSR-Bench (§9) must                 feature head            0.146            0.254
measure.
                                                            Table 3: Mechanism ablation of anchoring on the
Anchoring: the mechanism matters, and so does               real-model data (weak judge). Loop drift: final-round
headroom (registered failures, reported). In the            |score − gold| on selections (RL2). Adv. |gap|: out-
LLM settlement loop (40 problems, 8 rounds), nei-           of-problem |judge − gold| on adversarial candidates
ther anchored arm raised achieved gold over the             (RL3c); the isotonic row reports its signed tail effect
frozen judge—a ceiling effect: the generator solves         on mined deceptions (F4). Only the feature-level settle-
MBPP so well (mean candidate gold 0.81; the                 ment head helps on both.
frozen judge’s top-1 was already perfect on 34/40
problems) that there was no headroom, and the
                                                            ist and is future work (§10).
registered RL2a/RL2b verdicts are FAIL. Where
                                                            Adversarial pressure: selection, not persuasion
headroom existed—the real-code suite, whose
                                                            (registered failures, informative). The prompt-
frozen cross-problem verifier earned gold 0.000—
                                                            level adversary failed its manipulation check—the
anchored settlement lifted achieved gold to 0.153
                                                            “subtly wrong” code it wrote was mostly right (ad-
(p=.004), though its registered drift clause failed
                                                            versarial gold 0.839, matching honest quality)—
(drift rose as selections moved into higher-value,
                                                            so RL3a is an invalid test of hackability rather
harder-to-price regions). The sharpest real-model
                                                            than evidence of robustness. The iterative adver-
result is how to anchor: a learned settlement head
                                                            sary, shown the judge’s score after each of four
over the judge’s score and code features, refit on
                                                            revisions, drove score and gold down (0.679 →
executed outcomes (a deliberately minimal instan-
                                                            0.567; 0.878 → 0.733): at this capability level,
tiation of Algorithm 1’s amortizer), cut pricing
                                                            directed prompt-space search could not climb a
drift by 59% (0.352 → 0.146, p ≈ 0) and cut
                                                            real judge, and the operative Goodhart pressure
|judge − gold| on adversarial code from 0.326 to
                                                            on LLM judges is the selection pressure of RL1,
0.254; naive in-context anchoring (showing the
                                                            not persuasion. One registered criterion (RL3c)
judge a ledger of its own settled errors) made the
                                                            passed for the wrong reason: it assumed judges
judge worse on both metrics (p < 10−9 ). Amor-
                                                            overvalue adversarial code, but these judges un-
tize reality into a trained pricing model; do not
                                                            dervalue everything (mean gap −0.20), so the in-
merely show a judge its mistakes.
                                                            context ledger “reduced the gap” by worsening
Positioning against standard baselines. The
                                                            underconfidence; on the substantive |gap| metric
frozen-vs-anchored contrast is the comparison
                                                            only the world-model head helps. We disclose this
to online reward-model retraining: the anchored
                                                            as the suite’s second mis-specified criterion (with
arm retrains its verifier online, and what the
                                                            §7’s H2b) and record the process lesson: regis-
paradigm adds is the label source (settled exe-
                                                            ter criteria on |error|. Finally, the on-policy label-
cution rather than fresh preference or judge la-
                                                            efficiency claim failed on real code for a second
bels) and the schedule (the verifier’s own selec-
                                                            time (on-policy@240 AUC 0.144 vs. random@720
tions). The uncertainty-sampling control of §7 sep-
                                                            0.170, p=0.64): when the verifier is very weak, its
arates this from generic active learning: committee-
                                                            selections are uninformative places to settle, so the
variance acquisition barely beat random labeling
                                                            10× multiplier of §7 is a property of moderately-
(0.587 vs. 0.579 at S=3000) where on-policy set-
                                                            competent verifiers, not a universal.
tlement reached 0.664. Verifier ensembles and
process reward models are verifier-strength inter-          8.1 From failures to findings: a pre-registered
ventions, orthogonal to the settlement axis; the                diagnosis-and-repair program
verifier-strength axis is measured directly here
(H2b, RL1b) and buys real robustness. Table 3               Rather than leave the registered failures as caveats,
gives the mechanism-level ablation of anchoring             we treated each as a hypothesis about mechanism,
itself; a full-architecture ablation (typed claims,         froze numerical predictions for every diagnosis
market, staking) requires those components to ex-           before computing it, and ran the analyses on the
                                                            raw data. Four repairs succeeded; two failed and

                                                       12
are kept failed.                                             The feature-based head also failed to transfer Snd
Repaired: the exchange rate lives in the cop-                across problems (p=0.55), consistent with cross-
ula (F1). Proposition 2 resolves both directions             problem code verification being the hard regime
of the transfer anomaly at once: RichDSL’s heavy,            throughout our suites.
clumped margins made Pearson ρ overstate tail                Bounded: the conditional-binding conjecture
concordance (realized 0.32 < ρp =0.50), while                (F2). Weak-judge degradation concentrates on
the LLM judge’s coarse, saturated scores made it             hard problems (hardest tercile 0.092 vs. easiest
understate massively (ρp =0.12 yet realized 0.74).           −0.001; p=0.054), but the strong judge is flat
Rank-copula simulation with empirical margins                across all of MBPP’s difficulty range—MBPP-
predicts per-problem Snd@32 with median error                hard is not hard for it. “The gap binds where
0.041 on the real LLM data versus 0.793 for Pear-            task difficulty reaches judge capability” there-
son (p=2 × 10−4 , n=21); on RichDSL a residual               fore remains a conjecture with directional weak-
0.137 error remains (p=0.37)—its verifier errors             judge support only, and it fixes RSR-Bench’s de-
are feature-structured beyond any elliptical copula,         sign brief: difficulty-stratified, selection-pressure-
which is precisely the misspecification settlement           swept, execution-settled.
exists to correct.                                           Failed repairs, kept failed (F5, F6). The
Repaired: selection is the adversary (F3). The               competence-threshold explanation of the on-
instructed adversary of RL3a failed its manipula-            policy-efficiency discrepancy is ruled out: in
tion check, but mining the candidate banks shows             RichDSL the on-policy advantage is significantly
that ordinary sampling plus selection manufactures           positive even for a near-incompetent base veri-
deception: choosing the max-(judge−gold) candi-              fier (+0.087 at 150 labels, p=0.018) and not in-
date from 32 honest samples yields a +0.527 hack-            creasing in competence (+0.096 at 600, +0.050
ing gap against the weak judge, versus −0.209 for            at 2400); and the coverage hypothesis is ruled out
instructed deception (p=3 × 10−13 ), with severe             as well (F7, predictions frozen before running): a
natural hacks (judge ≥ 0.8, gold ≤ 0.2) on 13% of            mixed policy—half on-policy, half random labels
informative problems. Two sub-predictions failed:            per batch—performs like pure on-policy (0.148 vs.
severe hacks were rarer than predicted, and the              0.147 AUC at S=720) and below random (0.170)
strong judge’s maximum gap (0.631) exceeds the               under the identical protocol. With competence and
weak judge’s—the gap statistic conflates ranking             coverage both excluded, the leading untested can-
with calibration. The unification stands: RL1’s              didate is covariate shift: settled-selection labels
soundness decay and reward hacking are the same              correct pricing in the selected region while degrad-
phenomenon, selection pressure over honest varia-            ing global ranking under a cross-problem verifier—
tion; no deceptive generator is required. The mined          consistent with settlement improving drift but not
max-gap programs form a natural seed corpus for              selection throughout the real suites. Why on-policy
RSR-Bench’s adversarial split.                               settlement wins in per-task worlds and loses for
Repaired, with a warning: calibration is not                 cross-problem code verifiers is the program’s top
soundness (F4). The minimal settlement model—                open problem. And on the real-data hard sub-
an isotonic judge→gold map fit on executed                   set, the hybrid head improved pricing (p=0.009)
outcomes from half the problems—cuts out-of-                 but not achieved gold (p=0.36, n=19): capability
problem pricing error by 29.9% (p=5 × 10−119 ;               gains from anchoring remain demonstrated only in
registered threshold 30%, missed by 0.1pp). But              the synthetic and real-code CPU suites.
a monotone recalibration provably cannot change
                                                             8.2 Reality-anchored reward under real
selection, hence cannot move Snd@N ; and be-
                                                                 policy-gradient training
cause these judges are underconfident on average,
recalibration raises scores and amplifies the over-          The proxies above (best-of-N , search, iterative
valued tail (mined-deception gap 0.52 → 0.76).               prompting) approximate but do not instantiate the
Deception lives in the residual, not the mean. This          optimization process of modern RLVR. A fourth
yields the paradigm’s sharpest design constraint:            pre-registered suite (criteria R-A–R-E and amend-
the settlement model must be at least as expressive          ment R-B′ frozen before any run) closes that
as the deception surface; average-calibration an-            gap: GRPO fine-tuning of Qwen2.5-1.5B-Instruct
choring is not merely insufficient but tail-perverse.        (QLoRA, group size 8, 400 steps, fixed small KL)
                                                             on MBPP, under four reward arms identical in

                                                        13
 Arm                   Proxy Gold Peak        Gap            budget—only the labels differ (an LLM judge’s es-
                                                             timates instead of executed outcomes). Online up-
 frozen RM             0.615   0.063   0.617 +0.552
 online-judge          0.530   0.288   0.635 +0.241          dating alone recovers much of the damage (0.288
 anchored              0.528   0.397   0.665 +0.131          vs. frozen’s 0.063), but reality-sourced labels beat
 execution (ceiling)   0.460   0.460   0.687 0.000           judge-sourced labels by +0.109 executed reward
                                                             with half the hacking gap (+0.131 vs. +0.241),
Table 4: Final-window (25-step) training outcomes,           and the judge arm partially degenerates anyway
seed 0. Gold = executed reward; Peak = best rolling-         (∼ 24-token completions, KL 0.443). The mecha-
window gold; Gap = proxy − gold. The frozen arm’s            nism is visible in the logs: the judge’s labels erred
proxy is the highest and its reality the lowest.
                                                             against execution by 0.321 on average across refits
                                                             (range 0.18–0.46)—the RM was being re-anchored
                                                             to a proxy of a proxy. Online-ness is worth a lot;
everything but the reward signal: (A) frozen—a               reality is worth more, and the difference is the
settlement RM (ridge over surface/AST features)              judge’s blindness on-policy.
fit once on 1,600 executed base-model samples,               Registered criteria at seed 0—including a fail-
then frozen (the overoptimization setup of Gao               ure. Both R-A clauses hold (proxy +0.173 ≥
et al. (2023)); (B) anchored—the identical RM,               0.10; final gold 0.063 ≤ peak −0.03); both R-
refit every 25 steps on a settled σ=10% of the               B clauses hold (anchored gold exceeds frozen by
window’s rollouts (Algorithm 1, live); (C) execu-            0.334 ≥ 0.05; smaller gap); both R-B′ clauses
tion—real test execution as reward (sound ceiling);          hold; R-C holds (0.397 ≥ 0.8 × 0.460 = 0.368).
(D) online-judge—identical to (B) but refit labels           R-D fails: the settled-drift statistic does not rank-
come from an LLM judge rather than execution,                predict the concurrent hacking gap (Spearman
isolating the label source from online-ness. The             ρs = 0.06 over 15 refits, vs. the registered ≥ 0.5),
RM is deliberately minimal—a model organism:                 and an exploratory cross-arm variant (drift vs. the
arms (A), (B), (D) share an identical model class,           frozen-minus-anchored gap) is also null (ρs =
so the treatment isolates the settlement update rule         −0.40, p = 0.14) with no range-restriction ex-
itself, and a weak RM makes overoptimization ob-             cuse available (gap variance is comparable across
servable at accessible scale. RM strength is not             arms). At this scale and refit cadence, settlement
assumed orthogonal to settlement; their interaction          repaired the reward while its drift alarm did not
is characterized in §7 (H2b), §8 (RL1b), and F4.             see what it was repairing—the repair effect and the
True executed reward is logged for every rollout in          alarm effect are separable, and prediction 4 of §9.1
every arm (as metrics; it trains only arm C).                is already under adverse pressure. We also note the
Results. Table 4 and Figure 13 report the four               anchored arm’s final gold sits below its own mid-
matched runs. The frozen arm traces the full                 run peak (0.665); replication seeds run identically
overoptimization curve of Gao et al. (2023): proxy           under the same registration, and held-out evalua-
reward climbs 0.442 → 0.615 while executed re-               tions (R-E) accompany the full-suite verdicts. All
ward rises to a rolling peak of 0.617 and then col-          runs execute on a single consumer machine (Apple
lapses to 0.063—a 90% destruction of real capa-              M1, 16GB); the canonical 972-problem split and
bility under continued proxy gains—as the policy             initial RM were computed once and fixed before
converges to ∼ 17-token degenerate completions               any training run.
at KL 1.35 from base. The anchored twin ends
the same 400 steps at executed reward 0.397 (6×
                                                             9   RSR-Bench: A Reality-Settled Reason-
frozen), hacking gap +0.131 vs. +0.552, ordinary
                                                                 ing Benchmark
∼ 44-token completions, and KL 0.096: each of
its 15 refits repriced what the RM had begun to              Every prior revolution in this field was preceded
overpay before the policy could commit to it—at              by the metric that made it legible: ImageNet be-
roughly one-tenth of the ceiling arm’s execution             fore deep learning’s coronation (Deng et al., 2009),
budget, while retaining 86% of the ceiling arm’s             scaling-law perplexity before large pretrained mod-
final executed reward (0.397 vs. 0.460).                     els (Kaplan et al., 2020), MATH and HumanEval
Reality as the label source (R-B′ ). The online-             before reasoning RL (Hendrycks et al., 2021; Chen
judge control isolates the paper’s title claim: iden-        et al., 2021). Today the field optimizes judges it
tical RM, identical refit cadence, identical 10%             knows to be gameable because nothing better ex-

                                                        14
           Executed reward (solid) vs.\ proxy reward (dashed)                                   Hacking gap during training
          0.8                                                 0.6                            frozen RM
                                                                                             online-judge ( =10%, LLM labels)
                                                                                   0.4       anchored ( =10%, execution)
          0.6                                                                                anchored settled drift




                                                                      proxy gold
                                                                                   0.2
 reward




          0.4
                    execution (ceiling)                                            0.0
          0.2       anchored ( =10%, execution)
                    online-judge ( =10%, LLM labels)
                    frozen RM                                                      0.2
                0         100       200     300                 400                      0         100       200     300               400
                                  GRPO step                                                                GRPO step

 Figure 13: The overoptimization curve with a settlement knob (seed 0; rolling mean, window 15). Left: executed
Figure 13: The overoptimization curve with a settlement knob (seed 0; rolling mean, window 15). Left: executed
 reward (solid) and proxy reward (dashed). The frozen RM’s proxy climbs while executed reward collapses; the
reward (solid) and proxy reward (dashed). The frozen RM’s proxy climbs while executed reward collapses; the
 identical RM refit on a 10% settlement stream (anchored) tracks the execution ceiling; the equal-budget judge-
identical RM refit on a 10% settlement stream (anchored) tracks the execution ceiling; the equal-budget judge-
 labeled control sits between them. Right: the hacking gap (proxy − gold) during training, with the anchored arm’s
labeled control sits between them. Right: the hacking gap (proxy − gold) during training, with the anchored arm’s
 settled-drift measurements (×). Settlement repeatedly closes the gap the frozen arm rides to collapse — but drift
settled-drift measurements (×). Settlement repeatedly closes the gap the frozen arm rides to collapse—but drift
 magnitude does not rank-track the gap (the registered R-D criterion fails; see text).
magnitude does not rank-track the gap (the registered R-D criterion fails; see text).

          Reward source         Dense      Sound       Robust                 Algorithm 1 (line 10) adapts to measured drift, and
ists to climb. We therefore specify the missing                                  Reward   source       Dense
      Human preference ✓       ∼        ×                                     which the label-efficiency  resultsSound   Robust
                                                                                                                  bound where they
metric.
      LLM judge        ✓       ∼        ×                                                                ✓
                                                                              hold. The crucial design property is that Snd@N
                                                                                 Human   preference                ∼        ×
          Outcome reward                     ✓
Definition
      Process1RM
                                  ×
                (Soundness-under-Pressure).
                              ✓        ∼         ∼ For a
                                                         ∼
                                                                                         verifiers under ✓
                                                                                 LLM judge
                                                                              measures                   the optimization
                                                                                                                   ∼      pressure
                                                                                                                            ×
                              ✓        ✓ and candidate
                                                 ✓
                                                                                 Outcome   reward        ×         ✓        ∼
                                                                              they will actually face, which single-point accuracy
proxyFormal
       verifier  V , gold standard
             kernel                   G,
                                                                                 Process  RM             ✓         ∼        ∼
              µ, let xN be ✓
      PCC (proposed) V
distribution                          ✓†
                              the candidate     ✓†
                                              selected by                     does not.
                                                                                   Formal kernel              ✓           ✓          ✓
V from N i.i.d. draws of µ, and xN the candidate
                                        G
                                                                                   PCC (proposed)             ✓           ✓†         ✓†
 Table 5: Reward sources by density, soundness, and                           Construction recipe. Assemble tens of thou-
selected  byunder
 robustness  G. Thenoptimization pressure. ∼ = partial; †
                                                                              sands
                                                                              Table of5: typed
                                                                                          Reward claims  across
                                                                                                    sources       science,soundness,
                                                                                                             by density,      engineering, and
 = conjectured, contingent onanchor-drift  control; §6
 validates both  cells at toy  E G(x
                              scale and
                                       V)
                                       N§10 tests them at
                                                                              and  forecasting,
                                                                              robustness    under each  with a known
                                                                                                   optimization   pressure.settlement    date†
                                                                                                                              ∼ = partial;
              Snd@N =                     ,                                 and   mechanically      checkable    ground truth:        time-
                               E G(x
 scale. Formal kernels are sound       G )robust but cover
                                     and                                      = conjectured,    contingent   on anchor-drift     control;   §6
                                       N
only formalizable domains.                                                    sliced  scientific   claims  settled  by  later   replication,
                                                                              validates both cells at toy scale and §10 tests them at
and the headline benchmark score is the area un-                              scale. Formal kernels are sound
                                                                              performance-engineering         claimsand    robustby
                                                                                                                       settled      butexecu-
                                                                                                                                         cover
der Snd@N over log N .                                                        only formalizable
                                                                              tion,                 domains.
                                                                                     forecasts settled     by events (Halawi et al.,
 selected by G. Then                                                          2024). Freeze corpora at date T ; settle after T .
    A sound verifier scores 1 at every N ; Table 1                            Score submitted verifiers by Snd@N against the
shows how sharply               E [ G(x   V )]
               Snd@Na shallow
                           =         verifier
                                          N departs from
                                               ,                              settled gold, and score submitted reasoners by set-
                                E
it. On cost: Snd@N is an evaluation
                                  [ G(x   G)]
                                          N metric, not a                     tled claim portfolios under proper scoring rules
training-loop requirement, and it amortizes—one                               (Gneiting and Raftery, 2007). Table 5 situates the
 and the headline benchmark score is the area under
pool of Nmax candidates, generated and scored                                 Construction
                                                                              paradigm          recipe. Assemble
                                                                                           this benchmark              tens to
                                                                                                              is designed     of measure.
                                                                                                                                  thousands
 Snd@N over log N .
once, yields the whole curve by subsampling (our                              of typed claims across science, engineering, and
     A sound
entire         verifier
        real-model       scores 1 at every
                      measurement                   ; Tableon1
                                         of twoNjudges                        forecasting,     each with    a the
                                                                                                               known      settlement date
                                                                              9.1    What would       falsify      paradigm:
 shows
two      how sharply
      benchmarks        a shallow
                     cost   ∼ 3.5 ×verifier
                                        10 API departs
                                                    calls,from
                                                            i.e.              and mechanically        checkable     ground     truth:
                                                                                                                                   scaletime-
                                           4
                                                                                     registered predictions at the next
tens of dollars). Inside training, PCC’s marginala
 it. On  cost: Snd@N      is an  evaluation     metric,  not                  sliced scientific claims settled by later replication,
 training-loop
cost             requirement,
      over standard    RLVR isand   theitsettlement
                                           amortizes—onerate—                 We   do not claim to have established
                                                                              performance-engineering           claims settleda paradigm;
                                                                                                                                     by exe-
 pool  of  N       candidates,    generated
the fraction of staked claims actually executed—
             max                                 and   scored                 paradigm
                                                                              cution, forecasts settled by events (Halawi et au-
                                                                                           claims   are not  establishable      by  their   al.,
 once, yields
which           the whole
         Algorithm    1 (linecurve
                                10) by   subsampling
                                      adapts   to measured (our               thors.
                                                                              2024). We      claimcorpora
                                                                                        Freeze       to haveatmade
                                                                                                                 date Tone    measurable,
                                                                                                                          ; settle   after T .
 entire  real-model    measurement
drift, and which the label-efficiency    of  two   judges
                                              results bound  on               and
                                                                              Scorewesubmitted
                                                                                        stake it onverifiers
                                                                                                      numbered by predictions
                                                                                                                   Snd@N against    that any
                                                                                                                                           the
 two benchmarks
where               cost crucial
        they hold. The    ∼3.5×10      4
                                   designAPI   calls, i.e.
                                             property   is tens
                                                           that               frontier   laboratory    can  test  with   the   released
                                                                              settled gold, and score submitted reasoners by set-          in-
 of  dollars).  Inside  training,   PCC’s     marginal
Snd@N measures verifiers under the optimization            cost               struments     in days.   Each   is stated   so
                                                                              tled claim portfolios under proper scoring rulesthat   a  clean
 over standard
pressure           RLVR
           they will        is the
                     actually   face,settlement     rate—the
                                        which single-point                    negative
                                                                              (Gneitingresult     refutes the
                                                                                            and Raftery,        corresponding
                                                                                                           2007).   Table 5 situates compo-the
 fraction of
accuracy      staked
            does  not.claims actually executed—which                          nent.
                                                                              paradigm this benchmark is designed to measure.

                                                                      15
9.1 What would falsify the paradigm: regis-                       exceeds judge capability (measured at one
    tered predictions at the next scale                           point: +0.53 vs. −0.21; §8.1, F3).
We do not claim to have established a paradigm;
                                                                We commit to reporting confirmations and refu-
paradigm claims are not establishable by their au-
                                                             tations of these predictions alike; each is stated so
thors. We claim to have made one measurable, and
                                                             that it can be tested without our involvement.
we stake it on numbered predictions that any fron-
tier laboratory can test in days. Each is stated so          10   Validation Programme at Scale
that a clean negative result refutes the correspond-
                                                             The full hypothesis is falsifiable through three
ing component.
                                                             staged experiments.
                                                             Retrodiction gyms. Train the claim-ledger system
  1. Conditional binding. For every judge, on                on time-sliced corpora—papers, markets, code-
     tasks in its frontier stratum (single-sample            bases up to date T —and score claims against re-
     accuracy in [0.3, 0.7]), Snd@N declines by              ality after T , yielding millions of settled “experi-
     ≥ 0.10 from N =2 to N =256. Evidence so                 ments” at zero laboratory cost (Halawi et al., 2024).
     far: confirmed for the weak judge; untestable           Falsification criterion: if PCC-trained reasoning
     for the strong judge on MBPP (no frontier               does not beat judge-rewarded reasoning on retro-
     stratum exists there—§8.1, F2). Refuted if a            dictive forecasting and on reproduction of later-
     frontier judge holds Snd@256 within 0.05 of             discovered results, the hypothesis fails.
     Snd@2 on its own frontier stratum.                      Closed-loop empirical domains. Deploy where
  2. Copula law. For frontier judges on frontier             reality settles fast and automatically: software per-
     tasks, per-problem realized soundness lies              formance engineering (execution is the settler),
     within ±0.10 (median) of the rank-copula pre-           robotic manipulation, automated cloud-lab biol-
     diction of Proposition 2 (measured: 0.041 for           ogy. Measure whether world-model-priced reward
     the weak judge on MBPP). Refuted by sys-                beats PRM reward on downstream success and
     tematic departures beyond that band.                    on calibration under distribution shift—the metric
                                                             distinguishing a self-improving loop from a self-
  3. Overoptimization boundary.               Policy-        deceiving one.
     gradient training against a frozen learned RM           Anchor-drift audits. Continuously measure diver-
     diverges (proxy up, executed reward flat or             gence between world-model settlement and real-
     down) whenever the RM’s on-policy sound-                ized settlement (Algorithm 1, line 10). This scalar
     ness is below the policy’s achievable gold,             is the health metric of the system and, not inci-
     and reality-anchored refitting at a settlement          dentally, an alignment metric: a system rewarded
     rate adapted to measured drift removes the di-          for calibrated truth-tracking is structurally disin-
     vergence at a small fraction of full settlement.        centivized from deceiving its overseers, because
     Operationalized at 1.5B scale in our registra-          deception manifests as settlement loss.
     tion (criteria R-A–R-C); predicted to persist
     at every scale at which the precondition holds.         11   Failure Modes
                                                             We flag three honestly. (1) The claim language
  4. Drift is a universal alarm. Wherever di-
                                                             may be too lossy to carry the best reasoning—the
     vergence occurs, the settled-drift statistic of
                                                             legibility tax, sharpened. (2) Market dynamics
     Algorithm 1 (line 10) rank-predicts the frozen-
                                                             may reward safe, vague claims; scoring must pay
     vs-anchored gap online (ρs ≥ 0.5; registered
                                                             for resolution as well as calibration (Gneiting and
     as R-D). Refuted by hacking that drift does
                                                             Raftery, 2007). (3) A system optimizing predicted
     not see. First evidence is adverse: the regis-
                                                             reality could learn to make reality predictable in
     tered seed-0 test failed (ρs =0.06; §8.2).
                                                             undesirable ways; settlement must score prediction
  5. Selection-manufactured deception. The                   of a world the agent does not manipulate. This is
     maximum hacking gap obtainable by pure                  an open, safety-critical design problem (see Ethics
     best-of-N selection over honest samples                 Statement).
     grows with N at the extreme-value rate                  Meta-reward hacking and the trusted comput-
     implied by the copula, and dominates in-                ing base. Settlement does not eliminate trust; it
     structed deception until adversary capability           relocates it. An agent can attack the settlement

                                                        16
substrate itself: sandbox exploits, manipulation              Limitations
of the measured environment, strategic delay of
settlement, or staking only easy-to-settle claims.            The experiments in §3–§7 are synthetic: DSLs of
The honest accounting is a trusted computing base             six and ten tokens, ridge/gradient-boosted/logistic
(TCB): PCC’s TCB is the executor/measurement                  verifiers, and best-of-N , hill-climbing, evolution-
apparatus plus the settlement scheduler and stak-             ary, and settlement-aware search are proxies for—
ing rules—small and auditable, like a proof ker-              not instances of—frontier reasoners, learned re-
nel’s checker, but not zero. Concrete mitigations:            ward models, and RL training; a single-CPU suite
hardened and randomized execution environments,               cannot test frontier-scale claims. The scaled repli-
audit-by-resettlement of a random claim fraction,             cation (§7) falsified the quantitative transfer of
scoring rules that price claim selection (paying for          Proposition 1 outside its Gaussian model class (it is
resolution, §6 Result 5), and settlement-lag limits.          a ceiling, with realized value ≈ 0.32 at measured
                                                                                                                  2
In our own suites the TCB was subprocess isola-               ρ ≈ 0.50), showed the closed-form penalty N 1/ρ
tion with resource limits; every mined deception              overstates costs at practical N , and showed that
was semantic—none attacked the harness—but at                 absolute Goodhart collapse is domain-dependent:
higher capability that will not remain true by de-            a strong learned verifier kept converting pressure
fault, and TCB hardening should be treated as a               into capability through N =4096, so “sufficient
first-class component of the paradigm.                        pressure inverts any surface verifier” remains un-
                                                              established beyond that range. Anchoring was
                                                              tested against a settlement-aware search adversary
12    Conclusion                                              and survived, but not against a learning adversary
                                                              trained end-to-end against the settlement process;
The verification gap is the binding constraint on             anchoring also narrows rather than closes the ca-
the next major leap in language-model capability.             pacity gap to a sound verifier (0.28–0.31 vs. 0.59–
We have made its cost exact—unsound verification              0.68 under adversarial pressure), so verifier expres-
                                               2
pays a polynomial compute penalty N 1/ρ —and                  siveness remains a separate axis, and one regis-
demonstrated, in the smallest system that can ex-             tered adversarial cell failed as registered (steep-
press them, the collapse of learned verifiers under           est ascent; diagnosed, exploratorily, as adversary
i.i.d. pressure, their capture by adversarial pres-           paralysis). Result 5 and H6 show the training dy-
sure, and the repair mechanism: reality-anchored              namics do not intrinsically favor vague claims, but
settlement, which inverted the adversary’s exploit,           do not test an agent that strategically selects which
scaled soundness log-linearly with settled labels at          claims to stake. The real-model suite (§8) cov-
over 10× on-policy label efficiency, and sharpened            ers one model family, two code benchmarks at
claims rather than blunting them. Proof-carrying              or below the generator’s capability frontier (with
cognition is our conjecture for how this mechanism            heavy saturation: 50% of MBPP and 89% of Hu-
scales to open-ended empirical reasoning. We have             manEval problems showed zero gold variance and
not established that conjecture, and no laboratory-           were excluded by the pre-specified filter), anchor-
scale study could; what we have done is make it               ing by in-context learning and a learned reranker
measurable—an exchange-rate law that survives its             rather than RL training, pressure only to N =32,
own falsification in repaired form, a soundness met-          and a prompt-level adversary that failed its own
ric that prices verifiers under the pressure they will        manipulation check; its adversarial results bound
actually face, a settlement rule that preserved real          the threat model rather than the defense. Two regis-
reward under live policy-gradient pressure (even              tered criteria across the program (H2b, RL3c) were
as its registered drift alarm failed its first test—          themselves mis-specified and are disclosed as such.
reported as such), and five registered predictions            The single most important untested regime is tasks
(§9.1) that any frontier laboratory can confirm or            at the judge’s capability frontier under RL-scale
refute. The reality-settled benchmark of §9 is the            optimization pressure. Key unresolved questions
field’s single most important near-term investment            for PCC itself include the expressiveness of the
for the same reason ImageNet was: paradigms are               claim language relative to latent reasoning, scoring
not argued into existence, they are climbed into              rules that reward resolution without incentivizing
existence—and this one makes truth, rather than               vagueness or manipulation, the cost of a versioned
persuasion, the thing that wins.                              world model at training scale, and whether retrod-

                                                         17
iction transfers to genuinely novel discovery. The               reinforcement learning from human preferences.
framing of the field’s trajectory reflects the authors’          In Advances in Neural Information Processing
reading of the 2023–2026 literature and may not                  Systems, volume 30, 2017.
represent consensus.
                                                               Karl Cobbe, Vineet Kosaraju, Mohammad Bavar-
Ethics Statement                                                 ian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
A system trained to predict reality could act to                 Matthias Plappert, Jerry Tworek, Jacob Hilton,
make reality more predictable in harmful ways; set-              Reiichiro Nakano, Christopher Hesse, and John
tlement design must score prediction of unmanip-                 Schulman. Training verifiers to solve math word
ulated outcomes, and we identify this as a safety-               problems. arXiv preprint arXiv:2110.14168,
critical open problem rather than a solved one.                  2021.
Conversely, the paradigm has a favorable align-
                                                               Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai
ment property: reward for calibrated truth-tracking
                                                                  Li, and Li Fei-Fei. ImageNet: A large-scale hi-
structurally penalizes deception of overseers, and
                                                                  erarchical image database. In IEEE Conference
the anchor-drift scalar is a deployable oversight
                                                                  on Computer Vision and Pattern Recognition,
signal. Reality-settled benchmarks in sensitive do-
                                                                  2009.
mains (e.g., biology) must be curated to avoid cre-
ating dual-use optimization targets. No human                  Leo Gao, John Schulman, and Jacob Hilton. Scal-
subjects or private data are involved.                           ing laws for reward model overoptimization. In
References                                                       International Conference on Machine Learning,
                                                                 2023.
AlphaProof and AlphaGeometry teams, Google
  DeepMind. AI achieves silver-medal standard                  Scott Garrabrant, Tsvi Benson-Tilsen, Andrew
  solving International Mathematical Olympiad                    Critch, Nate Soares, and Jessica Taylor. Logi-
  problems. DeepMind Blog, 2024.                                 cal induction. arXiv preprint arXiv:1609.03543,
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul                 2016.
  Christiano, John Schulman, and Dan Mané.                     Tilmann Gneiting and Adrian E. Raftery. Strictly
  Concrete problems in AI safety. arXiv preprint                 proper scoring rules, prediction, and estimation.
  arXiv:1606.06565, 2016.                                        Journal of the American Statistical Association,
Jacob Austin, Augustus Odena, Maxwell Nye,                       102(477):359–378, 2007.
  Maarten Bosma, Henryk Michalewski, David
                                                               Daya Guo, Dejian Yang, Haowei Zhang, Junx-
  Dohan, Ellen Jiang, Carrie Cai, Michael Terry,
                                                                 iao Song, Ruoyu Zhang, Runxin Xu, Qihao
  Quoc Le, et al. Program synthesis with large lan-
                                                                 Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al.
  guage models. arXiv preprint arXiv:2108.07732,
                                                                 DeepSeek-R1: Incentivizing reasoning capabil-
  2021.
                                                                 ity in LLMs via reinforcement learning. arXiv
Samuel R. Bowman, Jeeyoon Hyun, Ethan Perez,                     preprint arXiv:2501.12948, 2025.
  Edwin Chen, Craig Pettit, Scott Heiner, Kamilė
  Lukošiūtė, Amanda Askell, Andy Jones, Anna                 David Ha and Jürgen Schmidhuber. Recurrent
  Chen, et al. Measuring progress on scalable over-              world models facilitate policy evolution. In Ad-
  sight for large language models. arXiv preprint                vances in Neural Information Processing Sys-
  arXiv:2211.03540, 2022.                                        tems, volume 31, 2018.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming                    Danny Halawi, Fred Zhang, Chen Yueh-Han,
 Yuan, Henrique Ponde de Oliveira Pinto, Jared                   and Jacob Steinhardt. Approaching human-
 Kaplan, Harri Edwards, Yuri Burda, Nicholas                     level forecasting with language models. arXiv
 Joseph, Greg Brockman, et al. Evaluating large                  preprint arXiv:2402.18563, 2024.
 language models trained on code. arXiv preprint
                                                               Dan Hendrycks, Collin Burns, Saurav Kadavath,
 arXiv:2107.03374, 2021.
                                                                 Akul Arora, Steven Basart, Eric Tang, Dawn
Paul F. Christiano, Jan Leike, Tom Brown, Miljan                 Song, and Jacob Steinhardt. Measuring mathe-
  Martic, Shane Legg, and Dario Amodei. Deep                     matical problem solving with the MATH dataset.

                                                          18
  In NeurIPS Datasets and Benchmarks Track,                 David Silver, Julian Schrittwieser, Karen Si-
  2021.                                                       monyan, Ioannis Antonoglou, Aja Huang,
                                                              Arthur Guez, Thomas Hubert, Lucas Baker,
Geoffrey Irving, Paul Christiano, and Dario                   Matthew Lai, Adrian Bolton, et al. Mastering
  Amodei. AI safety via debate. arXiv preprint                the game of Go without human knowledge. Na-
  arXiv:1805.00899, 2018.                                     ture, 550(7676):354–359, 2017.
Jared Kaplan, Sam McCandlish, Tom Henighan,                 Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral
  Tom B. Brown, Benjamin Chess, Rewon Child,                  Kumar. Scaling LLM test-time compute opti-
  Scott Gray, Alec Radford, Jeffrey Wu, and Dario             mally can be more effective than scaling model
  Amodei. Scaling laws for neural language mod-               parameters. arXiv preprint arXiv:2408.03314,
  els. arXiv preprint arXiv:2001.08361, 2020.                 2024.
Jan Hendrik Kirchner, Yining Chen, Harri Ed-                Marilyn Strathern. ‘improving ratings’: audit in
  wards, Jan Leike, Nat McAleese, and Yuri                   the British university system. European Review,
  Burda. Prover-verifier games improve leg-                  5(3):305–321, 1997.
  ibility of LLM outputs.     arXiv preprint
  arXiv:2407.13692, 2024.                                   Richard S. Sutton. The bitter lesson. Incomplete
                                                              Ideas (blog), 2019.
Yann LeCun. A path towards autonomous machine
  intelligence. OpenReview preprint, 2022.                  Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He,
                                                              and Thang Luong. Solving olympiad geometry
Jan Leike, David Krueger, Tom Everitt, Miljan                 without human demonstrations. Nature, 625
  Martic, Vishal Maini, and Shane Legg. Scalable              (7995):476–482, 2024.
  agent alignment via reward modeling: a research
  direction. arXiv preprint arXiv:1811.07871,               Jonathan Uesato, Nate Kushman, Ramana Kumar,
  2018.                                                       Francis Song, Noah Siegel, Lisa Wang, Anto-
                                                              nia Creswell, Geoffrey Irving, and Irina Hig-
Hunter Lightman, Vineet Kosaraju, Yuri Burda,                 gins. Solving math word problems with process-
  Harrison Edwards, Bowen Baker, Teddy Lee,                   and outcome-based feedback. arXiv preprint
 Jan Leike, John Schulman, Ilya Sutskever, and                arXiv:2211.14275, 2022.
  Karl Cobbe. Let’s verify step by step. In Interna-
  tional Conference on Learning Representations,            Ashish Vaswani, Noam Shazeer, Niki Parmar,
  2024.                                                       Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
                                                              Lukasz Kaiser, and Illia Polosukhin. Attention is
OpenAI. Learning to reason with LLMs. OpenAI                  all you need. In Advances in Neural Information
  Blog, 2024.                                                 Processing Systems, volume 30, 2017.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo                    Jason Wei, Xuezhi Wang, Dale Schuurmans,
  Almeida, Carroll Wainwright, Pamela Mishkin,                Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi,
  Chong Zhang, Sandhini Agarwal, Katarina                     Quoc V. Le, and Denny Zhou. Chain-of-thought
  Slama, Alex Ray, et al. Training language mod-              prompting elicits reasoning in large language
  els to follow instructions with human feedback.             models. In Advances in Neural Information Pro-
  In Advances in Neural Information Processing                cessing Systems, volume 35, 2022.
  Systems, volume 35, 2022.
                                                            Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li,
David E. Rumelhart, Geoffrey E. Hinton, and                   Markus N. Rabe, Charles Staats, Mateja Jamnik,
  Ronald J. Williams. Learning representations                and Christian Szegedy. Autoformalization with
  by back-propagating errors. Nature, 323(6088):              large language models. In Advances in Neu-
  533–536, 1986.                                              ral Information Processing Systems, volume 35,
                                                              2022.
Leonard J. Savage. Elicitation of personal probabil-
  ities and expectations. Journal of the American           Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah
  Statistical Association, 66(336):783–801, 1971.             Goodman. STaR: Bootstrapping reasoning with

                                                       19
    reasoning. In Advances in Neural Information              Soundness AUC is the mean of Snd@N over
    Processing Systems, volume 35, 2022.                      N ∈ {20 , . . . , 211 } on a fresh pool of 2,048.
                                                              Experiment 6. 60 tasks, 12 rounds; claim event
A     Experimental Details                                    “gold reward ≥ 0.25”; pools of 256 per round,
                                                              mixed acquisition (16 top-probability + 16 ran-
The DSL world. Programs are strings of length                 dom), 32 claims settled per round (1,920 per round
1–6 over six tokens acting on an integer register             pooled across tasks); 200 initial random labels per
initialized to the input x: A (v+1), S (v−1), D               task. Brier decomposition uses 10 equal-width
(v×2), T (v×3), N (−v), Q (v 2 ), with executions             probability bins; reliability and resolution are com-
aborted if |v| > 106 . A task is drawn by sam-                puted on each round’s settled claims before that
pling a hidden target program of length 4 whose               round’s refit, so every point is out-of-sample.
outputs on the evaluation inputs x ∈ {−3, . . . , 4}          Compute and seeds. All experiments complete
are all defined and take more than two distinct val-          in under ten minutes total on a single CPU. Seeds:
ues. Gold reward of a candidate is the fraction               0–4 (suite 1), 10–12 (suite 2), fixed in the scripts.
of the eight input–output pairs it matches under
execution. Random programs average gold reward
                                                              B    Scaled Replication Details
0.079; multiple functionally equivalent solutions
typically exist.                                              RichDSL. Programs of length 1–10 over ten to-
Verifiers. The learned verifier is ridge regression           kens acting on an integer register v initialized to
(α=1) over 43 features: 6 token counts, 36 bigram             input x: A (v+1), S (v−1), D (v×2), T (v×3), H
counts, and length—a deliberately shallow judge               (v div 2, truncating), N (−v), Q (v 2 ), P (v+x), M
evaluating the surface of a program rather than               (v mod 7), G (max(v, 0)). Values with |v| > 109
executing it. Experiment 6 uses logistic regres-              become invalid (scored as mismatch). Inputs
sion (C=1, predictions clipped to [0.001, 0.999];             x ∈ {−8, . . . , 7}; targets are length-6 programs
a clipped constant predictor when training labels             valid on all inputs with more than three distinct
are degenerate).                                              outputs. Random programs average gold reward
Experiment 1. 20,000 trials per (ρ, N ) point; N ∈            0.018. Statistical unit is the task; tests are paired
{20 , . . . , 212 }; ρ ∈ {0.2, 0.5, 0.8, 1.0}. Theory         two-sided Wilcoxon signed-rank unless a direction
lines use Monte-Carlo E[maxN ] (2 × 105 trials),              was pre-registered; intervals are 95% bootstrap
not the asymptotic formula.                                   CIs.
Experiment 2. 60 tasks; learned verifier trained on           Verifiers.           Weak:       ridge (α=1) on
1,000 labeled random programs per task; candidate             111       features        (unigrams,         bigrams,
pools of 2,048 fresh programs; N ∈ {20 , . . . , 211 }        length).        Strong:      gradient-boosted trees
subsampled without replacement per point.                     (HistGradientBoostingRegressor,
Experiment 3. 60 tasks, 10 rounds; pool 512, set-             100 iterations; 60 in the H3 loop) on 359 features
tle top 32 by proxy per round; anchored condition             (adding positional token indicators, 128 hashed
appends settled labels and refits, frozen does not;           trigrams, first/last one-hots). Both trained on 2,000
both start from 300 base labels.                              labeled random programs per task (600 base labels
Experiment 4.            40 tasks, 250 steps of               in the loop experiments).
steepest-ascent search: 16 mutations (substi-                 H1.       Gaussian simulation:          100,000 tri-
tute/insert/delete a token) per step, moving to the           als per point, N ∈ {2 , . . . , 214 }, ρ ∈
                                                                                                0

best-scoring candidate when it does not decrease              {0.1, 0.3, 0.5, 0.7, 0.9, 1.0}; the penalty sweep
the score. Anchored condition settles up to 25 re-            uses 20,000 trials to N =217 . Transfer (H1c):
cently visited programs every 25 steps (250 reality           per-task Pearson ρ(proxy, gold) on fresh pools of
queries per run) and refits. The sound condition              4,096 vs. realized Snd@4096, 120 tasks.
scores candidates by execution directly.                      H2. 120 tasks; pools of 4,096; N ∈ {20 , . . . , 212 },
Experiment 5.             40 tasks; base verifier             eight subsample repetitions per point.
trained on 500 random labels; budgets S ∈                     H3. 12 rounds; pool 1,024/round; settle the top 32
{0, 50, 150, 500, 1500}. On-policy acquisition al-            by proxy; anchored refits on all settled labels; 120
ternates pools of 256, settling the top 16 by the             tasks (weak), 60 (strong).
current verifier and refitting; the random condi-             H4.        300 steps, 24 mutations (substi-
tion adds S labels of random programs at once.                tute/insert/delete) per step, 100 tasks; anchored

                                                         20
settlement of the 25 most recent unique visited
programs every 25 steps (300 reality queries/run).
Steepest ascent moves to the best mutation
when not worse; the evolutionary adversary
keeps the top 16 of population-plus-children;
the settlement-aware adversary detects refits
(score drop without moving) and restarts at the
proxy-best of 64 random probes filtered to the
32 most edit-distant from all settled programs.
Its population (evolutionary) or the anchored
model’s scores are recomputed after refits; the
steepest climber’s stale incumbent score is the
registered-failure artifact discussed in §7.
H5. Budgets S ∈ {0, 100, 300, 1000, 3000} in
batches of 20; on-policy settles the top 20 by the
current verifier from pools of 512; uncertainty
sampling scores pool variance under a 3-member
bootstrap-ridge committee; Soundness AUC is the
mean of Snd@N over N ∈ {20 , . . . , 212 } on fresh
pools of 4,096; 80 tasks.
H6. Claim event “gold ≥ 0.125” (base rate
≈ 0.19; a pre-run, documented amendment from
the minimal suite’s 0.25, whose base rate ≈ 0.05
in RichDSL is too degenerate for 10-bin decompo-
sition); 15 rounds; pools of 256; 16 top-probability
+ 16 random claims settled per round; decompo-
sition computed out-of-sample before each refit;
100 tasks.
Compute and seeds. ∼ 75 minutes on a single
CPU. Tasks are independently seeded by index
(bases 20,000 / 50,000 / 60,000 / 70,000 / 90,000 /
110,000), so chunked and monolithic invocations
produce identical results.




                                                       21
