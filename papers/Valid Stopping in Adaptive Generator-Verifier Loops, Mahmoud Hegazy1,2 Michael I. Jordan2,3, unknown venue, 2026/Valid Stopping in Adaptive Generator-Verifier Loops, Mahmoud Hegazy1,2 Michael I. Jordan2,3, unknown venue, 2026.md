                                                     Valid Stopping in Adaptive Generator–Verifier Loops

                                                                      Mahmoud Hegazy1,2      Michael I. Jordan2,3
                                                                                Aymeric Dieuleveut1

                                                                       1
                                                                         CMAP, École polytechnique, IP Paris, France
                                                                  2                        3
                                                                      Inria Paris, France    EECS, UC Berkeley, USA


                                                                                               Abstract
arXiv:2610.06432v1 [stat.ML] 5 Oct 2026




                                                    Numerous agentic workflows are based on a generator–verifier loop: a generator proposes candidates,
                                                a cheap verifier scores them, and the workflow terminates when a proposal is verified as good enough.
                                                The verifier typically proxies a more costly ground-truth oracle, and as the generator searches adaptively
                                                against it, false acceptances may accumulate. Proposals can pass the proxy but fail under the costlier
                                                ground-truth check. We study when to stop these loops while controlling the false discovery rate of
                                                the accepted proposals. Our construction introduces tools of independent interest in distribution-free
                                                statistical testing and conformal risk control, including analysis of e-values constructed through index
                                                betting and a novel conformal risk control procedure for non-monotone losses. We validate the approach
                                                in synthetic settings and on a protein-design benchmark.


                                          1    Introduction
                                          A large class of inference-time systems operates as generator–verifier loops. A generator proposes candidates,
                                          a verifier supplies scores or pass/fail feedback, and the search stops when one or more candidates look
                                          acceptable. This template appears in code generation with unit-test filtering [Chen et al., 2021, Li et al.,
                                          2022], theorem proving with proof checkers [Polu and Sutskever, 2020], and mathematical reasoning with
                                          learned verifiers [Cobbe et al., 2021]. Related iterative self-feedback and verbal-reflection methods revise
                                          candidates using model-generated feedback [Madaan et al., 2023, Shinn et al., 2023]. The advantage of using
                                          verifiers can be substantial from a computational and economic point of view because, unlike the ground-truth
                                          oracle, the verifier is cheap and fast to query repeatedly.
                                          The substitution of a verifier for a ground-truth oracle, however, also induces a complex set of statistical and
                                          strategic problems. Once the generator adapts to past verifier outputs, it can search for candidates that exploit
                                          the proxy’s weaknesses. A verifier that is reliable marginally, or on isolated queries, can accumulate false
                                          acceptances under reuse. Recent analyses of inference-time search make this over-optimization phenomenon
                                          explicit [Khalaf et al., 2025, Huang et al., 2025]. A key problem is thus that of stopping a generator–verifier
                                          loop while controlling the quality of the accepted set as measured with the oracle, not merely with the proxy.
                                          We present a statistical procedure that halts after collecting κ ≥ 1 accepted proposals while controlling the false
                                          discovery rate (FDR) of the accepted set—i.e., the expected fraction of accepted proposals that the oracle would
                                          reject—below a user-specified level α. Using a small set of historical runs, we show how to deploy this procedure
                                          on an unobserved run where the true correctness labels are hidden. Formally, at round t, the generator
                                          proposes Xt , the verifier returns a score St and feedback Vt , with the oracle label Yt ∈ {0, 1} unobserved.
                                          We place no restriction on how Xt depends on the past history Ht−1 = (X1 , V1 , S1 , . . . , Xt−1 , Vt−1 , St−1 ).
                                          The procedure returns a set of accepted proposals among X1 , . . . , Xt with cardinality smaller than κ. This
                                          covers regimes in which the generator adapts aggressively to prior failures and verifier corrections. When
                                          κ = 1, the guarantee controls the FDR of the first nonempty returned set, which in the commonly employed
                                          single-return setting is exactly the probability of a false first acceptance.

                                          Contributions. We solve this stopping problem by combining three ingredients. First, as shown in Section 4,
                                          we construct marginally valid local e-values through an index-betting normalization [Koning, 2026]. The same
                                          section gives a finite-sample power analysis with matching upper and lower bounds under a fractional-moment


                                                                                                    1
condition on the likelihood ratio, and a weaker Kullback–Leibler (KL) divergence condition under which
the finite-batch normalization penalty vanishes. Second, Section 5 introduces robust-core conformal risk
control (CRC), a finite-sample calibration method for CRC with non-monotone losses. Third, in Section 6 we
show how to combine these local e-values with the weighted online e-Benjamini–Hochberg (e-BH) procedure
[Fischer et al., 2024] for stopped FDR control under arbitrary within-run dependence and how this addresses
the general generator–verifier stopping problem.

Outline. Section 2 formalizes the run-level model and gives a quick overview of the full approach. Section 3
positions our construction relative to related literature. Section 4 and Section 5 formally introduce our
e-value construction and robust-core CRC. Section 6 presents the full procedure together with a synthetic
illustration. Section 7 reports experiments on a MotifBench-derived protein-design benchmark [Zheng et al.,
2025]. In that benchmark, RFdiffusion [Watson et al., 2023] or Proteina [Geffner et al., 2025] generates
candidate backbones, ProteinMPNN [Dauparas et al., 2022] designs sequences, ESMFold [Lin et al., 2023]
provides a cheap structural proxy, and AlphaFold 3 [Abramson et al., 2024] serves as the more expensive
structural-prediction oracle that defines the benchmark label.


2     Setting and Overview
Each looped episode is referred to as a run, which is indexed by rounds t = 1, . . . , T . We note that our
approach can be extended to runs of variable length. Nonetheless, we restrict our attention to a fixed horizon
T for simplicity. At round t, the generator outputs a proposal Xt ∈ X , the verifier returns feedback Vt ∈ V
together with a score St ∈ S ⊆ R, and the ground-truth oracle would assign a label Yt ∈ {0, 1}, where Yt = 1
means that the proposal is correct. This label is generally not available during the run. Define the history

                                           Ht := (X1 , V1 , S1 , . . . , Xt , Vt , St ),

and set Ft := σ(Ht ) to be the induced filtration. Conditionally on Ft−1 , the tuple (Xt , Vt , St , Yt ) is drawn
from a kernel Kt (· | Ht−1 ). We impose no structural assumptions on dependence within a run. In particular,
the generator may adapt arbitrarily to past verifier outputs. All probability and expectation operators are
taken with respect to the resulting joint law of the trajectory.

Offline runs and score windows.              We assume access to a log of labeled historical runs,
                                                                                                  T
                          B = {Run1 , . . . , Runn },         Runi := (Xt,i , Vt,i , St,i , Yt,i ) t=1 ,

drawn i.i.d. at the run level. The independence assumption applies across runs only. Within each run, the
kernels Kt may depend arbitrarily on the past. Deployment consists of an unobserved run Runtest from the
same run-level distribution, with hidden labels Y1,test , . . . , YT,test . At time t ∈ {1, . . . , T }, the statistical task
is to decide using the labelled data whether to accept the current proposal Xt,test .
For a fixed context length K ≥ 0, we restrict our attention to procedures whose round-t decision depends on
the most recent K+1 verifier scores. For each run i ∈ {1, . . . , n} ∪ {test}, define

                                           Wt,i := (St−K,i , . . . , St,i ) ∈ S K+1 .

We use the convention Ss,i = 0 for s ≤ 0. When the run index is omitted, quantities refer to the unobserved
run Runtest . For example, Wt ≡ Wt,test and Xt ≡ Xt,test . For each round t, we form the augmented labeled
sample                                
                               Wt := (Wt,1 , Yt,1 ), . . . , (Wt,n , Yt,n ), (Wt , 0) ,
where the pseudo-label 0 is attached to Wt in lieu of its unobserved correctness label. We replace the hidden
label with 0 as we use the convention that the null hypothesis is that the proposal is incorrect.




                                                                2
Local evidence via e-values. At round t, we ask whether the current score window Wt is more likely
to correspond to a correct proposal or an incorrect one. Let P0,t and P1,t denote the marginal laws of Wt
conditional on Yt = 0 and Yt = 1, respectively, and write Ej,t for expectation under Pj,t , j ∈ {0, 1}. The local
problem is the simple-versus-simple hypothesis test

                                H0,t : Wt ∼ P0,t         against    H1,t : Wt ∼ P1,t .

Using the labeled sample  Wt , we construct an e-value for H0,t . That is, we build a nonnegative statistic
Et (Wt ) such that E0,t Et (Wt ) ≤ 1. Larger values then provide stronger evidence against H0,t . If P1,t is
absolutely continuous with respect to P0,t , denoted by P1,t ≪ P0,t , the ideal test statistic is the likelihood
ratio Lt = dP1,t /dP0,t . It satisfies E0,t [Lt (Wt )] = 1, maximizes E1,t [log Lt (Wt )], and is therefore log-optimal
among Wt -measurable valid e-values [Shafer, 2021, Larsson et al., 2025]. In our setting, however, Lt is
unknown and must be learned from Wt . A direct plug-in estimate L        b t,−test (Wt ) trained on Wt \ {(Wt,test , 0)}
is not necessarily valid, since E0,t [Lt,−test (Wt )] can exceed 1.
                                       b

Our construction restores validity by wrapping nonnegative, permutation-equivariant scoring rules with index
betting in the sense of Koning [2026]. The key step is to normalize the unobserved-run score against a
batch of offline null windows in a way that preserves exchangeability. We only require the fitting rule to be
invariant to the order of its training sample. The resulting vector of bets on the batch of windows is then
permutation-equivariant, yielding a statistic that is valid under H0,t for any such fitting rule. We defer the
formal construction and power analysis to Section 4.

Sequential testing. Once these roundwise e-values are available, the problem is reducible to an online
multiple-testing task. At round t, we return an accepted set Rt ⊆ {1, . . . , t} and measure its false discovery
proportion (FDP) by
                                                           1{Ys =0}
                                                    P
                                       FDP(Rt ) := s∈Rt             .
                                                        |Rt | ∨ 1
For a target acceptance count κ ≥ 1, define τκ := inf{t : |Rt | ≥ κ} ∧ T . Our goal is trajectory-level FDR
control along the unobserved run, uniformly over stopping times up to τκ :

                              E[FDP(Rτ )] ≤ α         for every stopping time τ ≤ τκ .                               (1)

We obtain this guarantee by aggregating the local e-values with the weighted online e-BH procedure of Fischer
et al. [2024], an online analogue of e-BH [Wang and Ramdas, 2022]. Under arbitrary dependence across time,
online e-BH guarantees                       h              i
                                            E sup FDP(Rt ) ≤ α,
                                                   t≥1

using only the marginal validity condition E0,t [Et ] ≤ 1 at each round. Since FDP(Rτ ) ≤ supt≥1 FDP(Rt ) for
every stopping time τ , this directly implies the bound in Equation (1).
Online e-BH operates through an α-spending mechanism,     allocating the per-run error budget across rounds
according to a nonnegative schedule (γt )t≥1 with t≥1 γt = 1. At time t, we accept the proposals indexed by
                                                 P

                                                                 
                                                              1
                                         Rt = s ≤ t : Es ≥          ,
                                                           αγs kt
where kt is the largest k ∈ {1, . . . , t} for which at least k indices s ≤ t satisfy Es ≥ 1/(αγs k). If no such k
exists, we set kt = 0 and Rt = ∅.
In practice, a fixed (γt )t≥1 schedule can be conservative. To overcome this, we calibrate the schedule using
the labeled logs. In particular, for λ in an ordered set Λ ⊂ (0, ∞) of candidate scales, we scale the schedule
by replacing γt with λγt . The goal is to select the largest possible λ ∈ Λ while maintaining the guarantee of
Equation (1).
Using labeled historical runs, we observe the per-run process loss

                                            ℓ(λ) := max FDP(Rt (λ)),
                                                     t≤τκ (λ)


                                                            3
whose expectation upper bounds the trajectory FDR up to the κ-acceptance time on the unobserved run.
The goal is to select the largest scale in Λ whose historical losses still certify E[ℓtest (λ)] ≤ α, for the unlabeled
deployment run. This loss is non-monotone in λ, however, so the standard monotone CRC route can fail
[Angelopoulos et al., 2024]. Section 5 introduces robust-core CRC, a finite-sample method designed for exactly
this non-monotone setting.


3     Related Work
Exchangeability-based e-values. Likelihood ratios provide a foundational tool for statistical testing.
Nonetheless, when the underlying distributions are unknown, estimating the likelihoods can compromise
finite-sample validity. Universal inference [Wasserman et al., 2020] addresses this through data splitting,
fitting the likelihood on one split and evaluating its ratio to the null likelihood on an independent split.
Within the testing-by-betting framework [Shafer, 2021], exchangeability-based e-values offer a different route
by using symmetry under the null to normalize a test statistic. In the group-invariance framework of Koning
[2026], this yields statistics of the form T (x)/EG [T (Gx)], where the denominator averages over null-preserving
transformations. Closest to our local construction, the Besag–Clifford e-value of Dombowsky et al. [2026]
normalizes a nonnegative statistic T of data X against M       PMreference samples Y (1) , . . . , Y (M ) exchangeable
with X under the null, namely (M + 1)T (X)/{T (X) + m=1 T (Y (m) )}, and is valid for every M . With
i.i.d. reference samples from the null and T proportional to the likelihood ratio, it converges almost surely
to that ratio as M → ∞. Their main interest is a null known only up to a normalizing constant, where
reference samples come from MCMC through the parallel method of Besag and Clifford [1989] and Markov
chain mixing controls the loss in expected log-growth. Exchangeability also underlies the sequential Monte
Carlo tests of Fischer and Ramdas [2025], who accumulate betting wealth as additional reference samples are
generated.
Our setting instead introduces a new hypothesis at each generator round. We construct a marginally valid
e-value for each proposal by normalizing learned scores against a finite pool of logged null windows, then
obtain stopping-time control through online multiple testing. With the true likelihood ratio as the score,
this statistic is a Besag–Clifford e-value with i.i.d. reference samples. For this local construction, Section 4
separates estimation error from the finite-pool normalization penalty relative to the ideal likelihood ratio. We
establish matching finite-sample rates for the normalization penalty under fractional-moment assumptions
that cover heavy-tailed likelihood ratios, and show that it vanishes under finite KL divergence alone.

Sequential testing and online FDR control. Sequential hypothesis testing controls the probability
of a false rejection even when the sample size is chosen adaptively or if the data arrives sequentially. In
particular, e-processes leverage test supermartingales to control the probability of a false rejection under the
null [Ramdas et al., 2023]. E-valuator [Sadhuka et al., 2025] applies this perspective to agent verification,
using successive verifier scores to flag trajectories that appear likely to end unsuccessfully. Its error criterion
is the probability of flagging a trajectory whose terminal output would actually be correct. In this paper, our
aim is to control the expected fraction of incorrect proposals accepted when the generator stops. Each round
introduces a new proposal and a corresponding hypothesis, making this an online multiple-testing problem.
The offline e-BH procedure controls FDR under arbitrary dependence among e-values [Wang and Ramdas,
2022], and Xu and Ramdas [2024] introduce e-LOND with the same dependence robustness for hypotheses
arriving sequentially. In our setting, the stopping time depends on the observed results and we leverage the
online e-BH procedure of Fischer et al. [2024], which guarantees the stronger E[supt≥1 FDP(Rt )] ≤ α result.

Risk control under non-monotone losses. Conformal risk control (CRC) generalizes the coverage
guarantees of conformal prediction to bounds on expected loss [Angelopoulos et al., 2024]. The original
procedure requires the loss to be monotone in the calibrated parameter, and its guarantee can fail when this
assumption is violated. For monotone losses, the guarantee is tight up to an O(1/n) term. Learn-then-Test
handles non-monotone losses by testing which candidate parameters satisfy the risk constraint and controlling
the familywise error rate across these tests [Angelopoulos et al., 2025]. More recently, Angelopoulos [2026]
replaces monotonicity with algorithmic stability and obtains risk guarantees with additional slack from
stability and discretization. Whereas Angelopoulos [2026]’s theory is based on leave-one-out stability, Prinster


                                                          4
et al. [2026] also study a different approach to CRC under replace-one stability, along with risk-controlled
policy selection in an agentic-loop setting that differs from ours by only using a generator, and no verifier.
Our robust-core CRC method restores monotonicity by lifting calibration to sets of parameter values, yielding
finite-sample risk control under exchangeability without requiring algorithmic stability, together with an
exact algorithm on finite grids.


4    Roundwise Marginally Valid e-Values
We now proceed to construct valid e-values for the roundwise testing problems of Section 2. Intuitively, the
construction is a betting game played against the null. We embed the unlabeled window Wt among a set
of realizations sampled from the null P0,t and ask a strategy to point to its position. Under the null, Wt is
exchangeable with the logged null windows, so no strategy can locate it more reliably. Nonetheless, under the
alternative, if Wt follows a different law P1,t from the null sample, it is possible to construct a strategy which
identifies its position more often.
Concretely, fix t and consider the simple-versus-simple test H0,t : Wt ∼ P0,t against H1,t : Wt ∼ P1,t . Let
Nt := {i ≤ n : Yt,i = 0} index the logged null windows and set n0,t := |Nt | + 1. Draw a uniformly random
ordering of the augmented null batch {Wt } ∪ {Wt,i : i ∈ Nt } and write the resulting indexed version as
                                                   (1)        (n ) 
                                        Wt0 := Wt , . . . , Wt 0,t ,
and let i⋆ ∈ {1, . . . , n0,t } denote the coordinate occupied by Wt . Conditional on the realized logged labels,
the batch size n0,t is fixed. Under H0,t the unobserved window and the logged null windows are exchangeable
                                   ⊗n
draws from P0,t , so Wt0 ∼ P0,t 0,t . The random permutation thus renders the hidden position i⋆ uniform
on {1, . . . , n0,t } and independent of the ordered batch. Under H1,t , the window Wt is the only element not
                                                                                   (i⋆ )
drawn from the null. Its position i⋆ is still uniform on {1, . . . , n0,t }, with Wt     ∼ P1,t and the remaining
coordinates drawn from P0,t .
A betting strategy is a measurable map
                               βt (Wt0 ) = βt,1 (Wt0 ), . . . , βt,n0,t (Wt0 ) ∈ [0, 1]n0,t
                                                                              
                           Pn0,t
that is budgeted, so that i=1    βt,i (Wt0 ) ≤ 1. We restrict to batch-symmetric strategies, namely those for
which permuting the coordinates of Wt0 permutes the output coordinates in the same way. The associated
index-betting e-value is the batch-size-scaled stake placed on the hidden unobserved coordinate,
                                                Etβ (·) := n0,t βt,i⋆ (·).
In words, the bettor spreads one unit of capital across the n0,t candidate positions and is paid at odds n0,t if
the hidden Wt position is guessed correctly. It is straightforward to show that Etβ is indeed a valid e-value.
Proposition 1 (Validity of index-betting e-values). For any budgeted, batch-symmetric βt , E0,t Etβ ≤ 1.
                                                                                                     


Proof. Condition on the logged labels, and hence on n0,t . Under H0,t , the ordered batch is exchangeable,
and the random ordering makes i⋆ independent of Wt0 and uniform on {1, . . . , n0,t }. Hence
                                                                             n0,t
                                                                             X
                           E0,t [Etβ | Wt0 ] = n0,t E0,t [βt,i⋆ | Wt0 ] =           βt,i (Wt0 ) ≤ 1.
                                                                             i=1




The same hidden-index
                 h      i representation supports a power analysis of the e-value, measured by the expected
                      β
log-growth E1,t log Et under the alternative. We call a strategy Kelly-optimal when it maximizes this
log-growth among budgeted, batch-symmetric strategies. Under H1,t , power is controlled by how well the
strategy identifies the coordinate occupied by Wt in the permuted batch. Proposition 2 shows that the
posterior of i⋆ given Wt0 is proportional to the likelihood ratio, and the Kelly-optimal strategy matches this
posterior, mirroring classical log-optimal betting results [Kelly, 1956, Larsson et al., 2025].


                                                            5
Proposition 2 (Kelly-optimality of likelihood-ratio betting). Assume P1,t ≪ P0,t and write Lt = dP1,t /dP0,t .
Under the hidden-index alternative indexed by H1,t above, conditional on the indexed batch Wt0 ,
                                                                    (i)
                                                   Lt (W )
                             Pr(i⋆ = i | Wt0 ) = Pn0,t t (j) ,                      i = 1, . . . , n0,t .
                                                  j=1 Lt (Wt )

Consequently,
                  among all budgeted strategies, and hence among budgeted, batch-symmetric strategies,
E log(n0,t βt,i⋆ ) | Wt0 is uniquely maximized by
                                                          (i)
                                             L (W )
                                    LR
                                   βt,i := Pn t t (j) ,                     i = 1, . . . , n0,t .
                                             0,t
                                            j=1 Lt (Wt )


The random ordering of Wt0 is an analytical device. On the original indices, the Kelly-optimal rule is

                                                                       Lt (Wt )
                                  Etidx := |Nt | + 1
                                                         
                                                                        P               .
                                                             Lt (Wt ) + i∈Nt Lt (Wt,i )


In practice, Lt is unknown and must be estimated. For each i ∈ Nt ∪ {test}, let L    b t,−i denote the score
produced by an order-invariant leave-one-out fitting rule trained on Wt with the pair indexed by i removed.
The resulting vector of leave-one-out scores is then permutation-equivariant, which is the batch symmetry
required above. For validity, it is enough that the betting function be batch-symmetric and budgeted. We
can therefore replace Lt with an estimated likelihood ratio and define the e-value

                                                                   L
                                                                   b t,−test (Wt )
                              btidx := |Nt | + 1                                                                      (2)
                                                   
                              E                                                                .
                                                       b t,−test (Wt ) + P
                                                       L                    i∈Nt Lt,−i (Wt,i )
                                                                                  b


4.1    Power decomposition and asymptotic rates
The index e-value Etidx is optimal within the index-betting family, yet may still be suboptimal relative to the
likelihood ratio Lt (Wt ). We adopt it because Lt is unknown in practice, and the index-betting construction
turns empirical proxies into valid e-values as in Equation (2). To characterize the log-optimality gap between
the empirical index e-value E   btidx and the likelihood ratio, we decompose it into a betting term and an
estimation term,
                h                         i                                      h                      i
                                     b idx = E1,t log Lt (Wt ) − log E idx + E1,t log E idx − log E idx
                                                                                                             (3)
                                                                         
            E1,t log Lt (Wt ) − log E t                               t                t
                                                                                                  b t     .
                                             |            {z              } |             {z            }
                                                             betting cost                       estimation residual

The betting cost is the fundamental price of the index-betting construction, the shortfall from Lt (Wt ) to the
best index-betting e-value Etidx , paid even when Lt is known exactly. The estimation residual is the price of
ignorance, the further gap from Etidx to E btidx . The theorem below controls it by the worst log-ratio error on
the augmented batch.
Theorem 1 (Estimation residual). Assume Lt > 0 P0,t -a.s. and that L b t,−i (Wt,i ) > 0 for every i ∈ Nt ∪{test}
a.s. Then
                  log Etidx − log E
                                  btidx ≤ 2 max       log Lt (Wt,i ) − log L b t,−i (Wt,i ) .
                                                   i∈Nt ∪{test}

Consequently, if that worst-case error, maxi∈Nt ∪{test} |log Lt (Wt,i ) − log Lb t,−i (Wt,i )|, has finite expectation
under the alternative, then
                    h                    i                                                          
                          idx        idx
               E1,t log Et − log Etb       ≤ 2E1,t    max        log Lt (Wt,i ) − log Lt,−i (Wt,i ) .
                                                                                       b
                                                             i∈Nt ∪{test}




                                                                6
Thus, convergence of the expected worst-case log-ratio error implies convergence of the estimation residual.
The remaining question is how fast the betting cost vanishes with the batch size n0,t . We show that a bounded
fractional moment of Lt under P0,t is enough for the betting cost to vanish in n0,t , at a rate controlled by the
moment exponent.
Theorem 2 (Betting cost upper bound). Condition on the realized logged labels, so that n0,t is fixed. Suppose
EP0,t [L1+δ
        t   ] < ∞ for some δ ∈ (0, 1], and set

                                                       log(1 + x)
                                             Cδ := sup            ,
                                                   x>0     xδ

which is finite for every δ ∈ (0, 1]. Then

                                                                             Cδ EP0,t L1+δ
                                                                                        
                                           idx
                                                 Cδ EP0,t Lt (Lt − 1)δ+                t
                   E1,t log Lt (Wt ) − log Et    ≤                         ≤                 .
                                                            nδ0,t                 nδ0,t

Since C1 = 1, setting δ = 1 recovers the classical O(1/n0,t ) rate, and δ < 1 extends the bound into the
heavy-tailed regime where EP0,t [L2t ] = ∞. For every δ ∈ (0, 1), this polynomial rate is tight over the moment
class P1+δ (B) = {(P0,t , P1,t ) : EP0,t [L1+δ
                                           t   ] ≤ B}.
Theorem 3 (Matching lower bound). For every δ ∈ (0, 1) and B > 1, there exists c = c(δ, B) > 0 such that
for all n0,t sufficiently large some pair (P0,t , P1,t ) ∈ P1+δ (B) satisfies
                                          h                         i
                                      E1,t log Lt (Wt ) − log Etidx ≥ c n−δ 0,t .


Since Etidx is Kelly-optimal by Proposition 2, this worst-case rate also lower bounds every budgeted batch-
symmetric strategy.
Finally, finite KL divergence alone is enough for the betting cost to vanish asymptotically.
Corollary 1 (KL-only convergence). If KL(P1,t ∥P0,t ) < ∞, then E1,t [log Lt (Wt )−log Etidx ] → 0 as n0,t → ∞.

4.2    Examples and simulations
We instantiate the local testing problem on two one-dimensional families chosen to separate light- and
heavy-tailed likelihood ratios. The light-tailed example sets P = N (0, 1) against Q = N (2.5, 1). The
heavy-tailed example tests P = Pareto(4) against Q = Pareto(1) on x ≥ 1, where Pareto(a) has density
fa (x) = ax−(a+1) . We first illustrate the likelihood-ratio behavior in these two settings.
Example 1 (Gaussian shift). A Gaussian shift sits in the light-tailed regime. If Wt ∼ N (0, Σ) under P0,t
and Wt ∼ N (µ, Σ) under P1,t , the log-likelihood ratio log Lt (Wt ) is Gaussian with mean −ρ2 /2 and variance
                                                       2
ρ2 , where ρ2 = µ⊤ Σ−1 µ. Hence EP0,t [Lkt ] = ek(k−1)ρ /2 for every k, so all moments are finite. Theorem 2
with δ = 1 therefore recovers a 1/n0,t rate.
Example 2 (Pareto pair). Let f0 (x) = ax−(a+1) and f1 (x) = bx−(b+1) on x ≥ 1 with a > b > 0, so
Lt (x) = (b/a)xa−b . Here EP0,t [L2t ] < ∞ only when a < 2b, whereas EP0,t [L1+δ
                                                                             t   ] < ∞ iff δ < b/(a − b), which
holds for some δ > 0 for a > b.
For each family, we sweep the reference set size M ∈ {50, 100, 200, 500, 1000, 2000, 4000, 5000} and report
results at nominal levels α ∈ {0.05, 0.01}, where M = n0,t − 1. For the Gaussian experiments, we use
P0,t = N (0, 1) and P1,t = N (2.5, 1), while for the Pareto experiments we use P0,t = Pareto(4) and
P1,t = Pareto(1). To estimate the likelihood ratio, we fit standardized logistic regression on 100 null
and 100 alternative observations, using feature z for the Gaussian family and log z for the Pareto family. The
fitted odds are clipped to [10−3 , 103 ]. Figure 1 reports the Type-I and Type-II error rates of three e-values,
namely the true likelihood ratio Lt , index betting with the true likelihood ratio Etidx , and index betting with
the estimated likelihood ratio E
                               btidx .



                                                         7
                                                         Lt             Etidx          btidx
                                                                                       E                    α = 0.05           α = 0.01

 ×10−3 Type-I: Gaussian                                       Type-I: Pareto                                Type-II: Gaussian             Type-II: Pareto
 10                                                                                         1.00




       1                                                                                        .75



     .1
      0                                                                                         .50

                50                  500          5000 50           500               5000              50             500       5000 50           500         5000
                                                                          Null reference size M

Figure 1: Type-I and Type-II error rates across reference sizes M for Lt , Etidx , and E
                                                                                       b idx . Solid curves with
                                                                                         t
open markers correspond to α = 0.05 and dashed curves with filled markers to α = 0.01.


In the second experiment, we aim to characterize how the tail of the likelihood ratio controls the finite-reference
penalty. To remove estimator error, Figure 2 compares only the likelihood ratio with Etidx . The sweep is
organized by the largest finite fractional moment

                                                                 δ := sup{γ > 0 : EP0,t [L1+γ
                                                                                          t   ] < ∞}.

We sweep δ over {0.025, . . . , 1} by choosing a null–alternative pair whose likelihood ratio has exactly that
fractional-moment exponent. In the Gaussian case, we use P = N (0, 1) against Q = N (0, 1 + 1/δ), while in
the Pareto case we use P = Pareto(4) against Q = Pareto(b) with b = 4δ/(1 + δ). Power is reported on a
normalized log-growth scale, EQ [log E]/ KL(Q∥P ). Since EQ [log Lt ] = KL(Q∥P ), the likelihood ratio sits at
exactly one, and a curve at 0.7 means the index e-value retains 70% of the ideal log-growth. The resulting
curves follow both directions predicted by Theorem 2. The gap closes as δ grows and as the reference batch
M grows.

                                                 Lt ceiling     Etidx, M = 500                      Etidx, M = 1000         Etidx, M = 5000
                                                Gaussian scale family                                                           Pareto family
                      1.00
log-growth retained
   Fraction of LR




                      0.75
                      0.50
                      0.25
                      0.00
                             .025         .05       .1            .25           .5              1        .025         .05       .1          .25          .5      1
                                          Largest finite fractional moment                                            Largest finite fractional moment

Figure 2: Normalized log-growth EQ [log E]/ KL(Q∥P ) of the oracle index e-value Etidx as a function of
the fractional-moment exponent δ, for reference sizes M ∈ {500, 1000, 5000}. Each point averages 2 × 105
repetitions.




                                                                                            8
5     Robust-Core Risk Control for Non-Monotone Losses
Using exchangeable labeled samples, CRC [Angelopoulos et al., 2024] calibrates a loss parameter so that the
test-time loss has controlled expectation. Let (Λ, ⪯) be a totally ordered parameter space, where λ ⪯ λ′
means that λ′ is preferred by the downstream selection criterion. For the online e-BH family introduced
in Section 2, larger values of λ stop the loop earlier, save computational costs, and are therefore preferred.
Throughout this section we treat CRC abstractly, then specialize it for our setting in Section 6.2.
We assume that ℓ1 , . . . , ℓn+1 are exchangeable random loss profiles, where each ℓi : Λ → [0, 1] is a measurable
function of λ and auxiliary randomness that typically represents the underlying data, which we leave implicit
to keep the notation light. In our setting, only ℓ1 , . . . , ℓn are observed and ℓn+1 is hidden. For A ⊆ Λ, write
inf ⪯ A, sup⪯ A, and max⪯ A for the infimum, supremum, and maximum with respect to ⪯. Whenever a rule
below selects a supremum, we assume that it lies in the feasible set. Given a level α ∈ (0, 1), a CRC method
chooses an (ℓ1 , . . . , ℓn )-dependent λ
                                        b ∈ Λ, which satisfies

                                                   E[ℓn+1 (λ)]
                                                           b ≤ α.                                              (4)

When each loss profile is non-decreasing along ⪯, i.e., λ ⪯ λ′ implies ℓi (λ) ≤ ℓi (λ′ ) for every i, the classical
CRC approach computes
                                         (                 n
                                                                        !      )
                                                     1    X
                            bCRC := sup λ ∈ Λ
                            λ                                 ℓi (λ) + 1 ≤ α ,                                  (5)
                                      ⪯           n + 1 i=1

which satisfies the guarantee in Equation (4) [Angelopoulos et al., 2024]. When monotonicity fails, the above
rule can be invalid [Angelopoulos et al., 2024]. A conservative alternative replaces each ℓi by its running
supremum ℓ̄i (λ) := supλ′ ⪯λ ℓi (λ′ ) and applies the classical rule to these envelopes,
                                           (           n
                                                                                  !        )
                                                  1   X
                              benv := sup λ ∈ Λ
                              λ                           ℓ̄i (λ) + 1                 ≤α .                     (6)
                                       ⪯        n + 1 i=1

The envelopes are non-decreasing and dominate the original curves, ℓi (λ) ≤ ℓ̄i (λ), so the monotone guarantee
applied to ℓ̄i gives
                                   E[ℓn+1 (λ
                                           benv )] ≤ E[ℓ̄n+1 (λ
                                                              benv )] ≤ α,

satisfying Equation (4). Nonetheless, the above envelope approach can be conservative as a local spike is
treated as permanent. Hence parameters that are safe on the realized curve can be discarded.

5.1    Robust core on ordered spaces
Robust-core CRC handles non-monotonicity by lifting the problem and calibrating a set in 2Λ . For a set
C ⊆ Λ, define Li (C) := supλ∈C ℓi (λ), with Li (∅) = 0. This set loss is monotone under inclusion. If C ⊆ C ′ ,
then Li (C) ≤ Li (C ′ ). Thus, even when the scalar curve λ 7→ ℓi (λ) is non-monotone, the lifted set-valued
problem has a monotone structure. We assume the relevant suprema exist. This condition holds automatically
in the finite-grid setting introduced in Section 5.2.
Let L ⊆ [0, 1]Λ be an admissible class containing all possible loss functions. A complete-data certificate is
a symmetric map G : Ln+1 → 2Λ whose output has controlled empirical set-loss for every complete tuple
ℓ1:n+1 ∈ Ln+1 :
                                              n+1
                                          1 X
                                                                                                          (7)
                                                               
                                                  Li G(ℓ1:n+1 ) ≤ α.
                                        n + 1 i=1
Symmetry means that G depends only on the unordered collection of loss curves. Concretely, for every
permutation σ of {1, . . . , n + 1},

                                    G(ℓ1 , . . . , ℓn+1 ) = G(ℓσ(1) , . . . , ℓσ(n+1) ).


                                                             9
Algorithm 1 Greedy Selector
 1: Input. Ordered parameter space (Λ, ⪯), complete loss profiles ℓ1 , . . . , ℓn+1 ∈ L, level α.
 2: Initialize. C ← ∅, R ← Λ.
 3: while R ̸= ∅ do
 4:                                          (                                           )
                                                              n+1
                                                          1 X
                                       R←       λ∈Λ\C :           Li (C ∪ {λ}) ≤ α
                                                        n + 1 i=1

 5:   if R ̸= ∅ then
 6:      λ⋆ ← max⪯ R,         C ← C ∪ {λ⋆ }.
 7:   end if
 8: end while
 9: return C.



If the unobserved loss profile ℓn+1 were observed, any parameter in G(ℓ1:n+1 ) would be safe by the original
conformal-risk-control exchangeability argument. Indeed, condition on the unordered multiset {ℓ1 , . . . , ℓn+1 }.
The index of the unobserved profile is then uniform on {1, . . . , n + 1}, while every λ ∈ G(ℓ1:n+1 ) is measurable
with respect to this unordered multiset by symmetry. Hence, for any such λ,
                                                              n+1                n+1
                                                          1 X                1 X                  
                 E[ℓn+1 (λ) | {ℓ1 , . . . , ℓn+1 }] =             ℓi (λ) ≤           Li G(ℓ1:n+1 ) ≤ α.
                                                        n + 1 i=1          n + 1 i=1

One canonical way to construct such a G is the greedy selector in Algorithm 1, which scans Λ from most to
least preferred and admits a parameter when its inclusion preserves Equation (7). The rule is permutation
invariant in ℓ1 , . . . , ℓn+1 and satisfies Equation (7) by construction.
Nonetheless, ℓn+1 is not observed and G(ℓ1 , . . . , ℓn+1 ) cannot be evaluated directly. Instead, consider the
parameters that would be certified no matter which admissible ℓn+1 is realized:
                                                      \
                                          Cn :=           G(ℓ1:n , w),
                                                            w∈L

where w is a placeholder for any possible realization of ℓn+1 . Since the realized ℓn+1 belongs to L, λ ∈ Cn
implies λ ∈ G(ℓ1 , . . . , ℓn+1 ). Following Angelopoulos [2026], we also assume a fallback parameter λsafe ∈ Λ
satisfying
                                           ℓi (λsafe ) = 0, i = 1, . . . , n + 1,                            (8)
almost surely. The robust-core estimator chooses the most preferred parameter in Cn when this set is
nonempty and falls back otherwise:
                                            (
                                    bcore := max⪯ Cn , Cn ̸= ∅,
                                    λ                                                            (9)
                                             λsafe ,    Cn = ∅.

Theorem 4 (Validity of the robust core). Under the setup above, suppose the loss profiles are exchangeable,
G is symmetric and satisfies Equation (7), and Equation (8) holds. Then E[ℓn+1 (λ
                                                                                bcore )] ≤ α.

Nonetheless, Cn is not generally computationally tractable as it requires the intersection of G(ℓ1:n , w) over all
admissible missing curves w. We now specialize to a finite grid and construct Cn with G fixed as the greedy
selector in Algorithm 1.

5.2    Finite-grid specialization
Consider a finite grid Λ = {λ1 , . . . , λm } ⊂ R listed from least to most preferred, so λ1 ⪯ · · · ⪯ λm . On a grid,
the greedy certificate of Algorithm 1 reduces to a single scan from λm down to λ1 . When the scan visits λk ,


                                                               10
it includes λk in the running set C exactly when
                                                              n+1
                                                          1 X
                           include λk in C      ⇐⇒                  max ℓi (λ) ≤ α.
                                                        n + 1 i=1 λ∈C∪{λk }

The scan reproduces Algorithm 1 because the coordinatewise maxima are monotone in C: a point that
fails when first visited cannot become feasible after C has grown. At calibration time, however, ℓn+1 is not
observed. We must compute the intersection over all possible completions w : Λ → [0, 1], where w(λk ) is the
loss the unobserved run would incur at λk . Letting U = [0, 1]Λ denote the unconstrained completion class,
the robust core specializes to                     \
                                            Cn =       G(ℓ1:n , w),
                                                     w∈U

where G(ℓ1:n , w) denotes the scan applied to the augmented tuple (ℓ1 , . . . , ℓn , w). A grid point lies in Cn
when no admissible completion can dislodge it. Since U is infinite, Cn cannot be obtained by enumerating
completions. Algorithm 2 instead tracks, for each scan branch, a finite sufficient statistic of its consistent
possibilities.

Algorithm description. Before processing λk , the include or skip decision depends on the already selected
set C only through the calibration maxima Mi = maxλ∈C ℓi (λ) and the held-out maximum u = maxλ∈C w(λ).
The vector M is pinned down by C and the observed losses, while u depends on the unobserved completion
w. Rather than carry all completions consistent with a branch, the algorithm stores only their projection
onto u, which remains an interval I = [a, b] ⊆ [0, 1] throughout the recursion. A frontier state is therefore
a pair (M, I), initialized at (0, [0, 0]) before the scan begins. After deduplication, one state may represent
branches with different selected sets, but their future decisions coincide because they share the same sufficient
pair (M, I).
                                                                       Pn
At grid point λk , write Mi′ = max{Mi , ℓi (λk )} and Θ = (n + 1)α − i=1 Mi′ . For u ∈ [a, b] and v = w(λk ) ∈
[0, 1], the scan includes λk iff
                              n
                                                  !
                       1    X
                                   ′
                                 M + max(u, v) ≤ α,          equivalently      max(u, v) ≤ Θ.
                     n + 1 i=1 i

Each state branches into at most two successors. The include branch is reachable when a ≤ Θ; then M
becomes M ′ and the held-out interval becomes [a, min{1, Θ}]. The skip branch is reachable when Θ < 1,
since choosing w(λk ) > Θ skips inclusion while leaving (M, I) fixed.
The scan moves from most to least preferred, expanding the frontier and merging coincident states. It returns
the first grid point λk at which the include branch is reachable from every frontier state and the skip branch
from none. Then every admissible completion forces inclusion of λk , so λk ∈ Cn as the grid is scanned in
order of decreasing preference.
Lemma 1 (Exactness of Robust Core Tree-CRC). Let U = [0, 1]Λ , and let G(ℓ1:n , w) be the set returned by
the complete-data greedy scan when the missing profile is w ∈ U. Algorithm 2 returns
                                                \
                                           max       G(ℓ1:n , w)
                                                 ⪯
                                                     w∈U

when this intersection is nonempty, and returns λsafe otherwise.
Theorem 4 certifies that the robust core controls risk, and Lemma 1 certifies that Algorithm 2 computes it on
the grid. Together they yield a finite-sample calibration rule for non-monotone loss profiles.

5.3    Non-monotone CRC experiment
We illustrate robust-core calibration on clipped-Gaussian non-monotone losses over the ordered grid Λ =
{λk = k/100 : k = 1, . . . , 100}. For example i and grid point λk , the loss is
                                                                       ind
                             ℓi (λk ) = clip(λk + σZi,k , 0, 1),   Zi,k ∼ N (0, 1),


                                                         11
Algorithm 2 Robust Core Tree-CRC
  1: Input. Calibration losses li (k) = ℓi (λk ), grid λ1 ⪯ · · · ⪯ λm , level α, fallback λsafe .
  2: Initialize. Frontier F ← {(M = 0n , I = [0, 0])}.
  3: for k = m, m − 1, . . . , 1 do
  4:  F ′ ← ∅, AllInclude ← true.
  5:  for each state (M, I = [a, b]) ∈ F do
  6:     M ′ ← max(M, l1:n  P(k))  coordinatewise.
                              n
  7:     Θ ← (n + 1)α − i=1 Mi′ .
  8:     if a ≤ Θ then
  9:        Add (M ′ , [a, min{1, Θ}]) to F ′ .
10:      end if
11:      if Θ < 1 then
12:         Add (M, [a, b]) to F ′ , set AllInclude ← false.
13:      end if
14:   end for
15:   Deduplicate repeated states in F ′ , set F ← F ′ .
16:   if AllInclude then
17:      return λk .
18:   end if
19: end for
20: return λsafe .



independent across examples and grid points. We separately define ℓi (0) = 0 for every run and
set the fallback λ = 0. We sweep over noise levels σ ∈ {0.20, 0.10, 0.05} and calibration sizes
n ∈ {100, 200, . . . , 1000, 1200, 1500, 2000, 2500, 3000}, at level α = 0.1. Larger λ values are more pre-
ferred and more aggressive. We compare robust-core CRC, the monotone-envelope rule of Equation (6), and
the finite-grid stable-CRC baseline of Angelopoulos [2026]. Figure 3 plots the mean selected parameter with
95% Monte Carlo intervals over 100 trials. The dotted line is the highest grid point with population risk less
than α.

                                              Robust-core CRC    Monotone-envelope CRC     Stable CRC

                                = 0.20                             = 0.10                               = 0.05
                0.10
Mean selected




                0.05

                0.00
                       100             1000    3000   100                 1000    3000   100                 1000   3000
                             calibration n                      calibration n                      calibration n

Figure 3: Mean selected parameter on the clipped-Gaussian grid, with 95% Monte Carlo intervals. The
dotted line marks the highest fixed safe parameter λ⋆ = max⪯ {λk : E[ℓi (λk )] ≤ α}. The three panels show
the three clipped-Gaussian noise levels in the sweep.

All three rules control risk, so the comparison is about the aggressiveness with which each rule is able to
select the parameter λ.
                      b Robust-core CRC assumes only exchangeability and boundedness, and its selected
parameter still climbs with n toward the fixed safe parameter λ⋆ . The two baselines stay well below it for
different reasons. The monotone-envelope rule replaces every loss profile by its running maximum, so a single
upward fluctuation at a small grid point suppresses all larger candidates. The stable-CRC baseline retains
the raw profiles but subtracts an explicit concentration slack, which shrinks slowly with n. The robust core


                                                                 12
avoids both penalties and approaches λ⋆ .
An astute reader might have noticed that Algorithm 2 is exponential in the grid size |Λ| in the worst case,
since the frontier can hold up to 2|Λ| states. Nonetheless, we note that the scan terminates as soon as it
reaches a grid point that is included from every frontier state, and that states that coincide are merged. In
practice, we found the rule to be efficient. Figure 4 reports its selection time on the clipped-Gaussian losses
above, for grid sizes up to |Λ| = 250.

                                                                  n = 100             n = 500          n = 3000

                                             σ = 0.20                             σ = 0.10                         σ = 0.05
      Median selection time (ms)




                                   3


                                   2


                                   1


                                   0
                                       20   100      175    250      20         100        175       250   20     100      175    250
                                            Grid size |Λ|                       Grid size |Λ|                     Grid size |Λ|


Figure 4: Selection time of robust-core CRC against the grid size. Each panel corresponds to one
noise level σ of the clipped-Gaussian losses and shows the median selection time in milliseconds against
the grid size |Λ|, at level α = 0.1, with one curve per calibration size n. Curves show the median over 100
independent calibration datasets of each dataset’s median time over five repetitions, and shaded bands show
pointwise 95% bootstrap intervals for this median.



6        End-to-End Valid Stoppage
We now proceed to introduce the full procedure, which combines the preceding e-value construction and
CRC results into a single pipeline. To recap our setting and notation, we consider an unlabeled deployment
run Runtest = ((Xt , Vt , St , Yt ))Tt=1 whose correctness labels Y1 , . . . , YT are unavailable. At each round t, we
observe the score window Wt := (St−K , . . . , St ) ∈ S K+1 formed from the most recent K+1 verifier scores
and return an accepted set Rt ⊆ {1, . . . , t}. These sets are nested, with R1 ⊆ R2 ⊆ · · · ⊆ RT . Our goal is to
ensure that E[FDP(Rτ )] ≤ α for every stopping time τ ≤ τκ , as formalized in Equation (1). Throughout this
section, we make use of two different splits of labelled data, the first for constructing the roundwise e-value
and the second for calibrating the online e-BH procedure to make it less conservative. We denote the dataset
used in constructing the roundwise e-values by

                                                                  B e = {Rune1 , . . . , Runene },

and use the superscript e to mark quantities belonging to runs in B e , for example St,j
                                                                                     e
                                                                                         and Yt,j
                                                                                               e
                                                                                                  . We assume
that the runs in B and Runtest are independent and identically distributed.
                  e



6.1                          Valid stoppage on the unobserved run
At round t, we use Wt to test H0,t : Wt ∼ P0,t against H1,t : Wt ∼ P1,t , where Pi,t is the distribution of
Wt |Yt = i for i ∈ {0, 1}. We construct the corresponding e-value using the leave-one-out index-betting
procedure of Section 4. Mirroring Section 2, define

                 Wte := {(Wt , 0)} ∪ (Wt,j                   and Nte := {j ≤ ne : Yt,j
                                     e        e                                    e
                                           , Yt,j ) : j ≤ ne                           = 0}.


                                                                                13
For each a ∈ Nte ∪ {test}, let L
                               b t,−a be the likelihood-ratio estimator fitted to W e with the sample indexed by
                                                                                   t
a removed, using an order-invariant fitting rule. The resulting roundwise e-value is

                                                                    L
                                                                    b t,−test (Wt )
                                 bt = |N e | + 1                                                                                     (10)
                                                   
                                 E      t                                                       .
                                                       b t,−test (Wt ) + P
                                                       L                                  e
                                                                            j∈N e Lt,−j (Wt,j )
                                                                                   b
                                                                                t



Under the round-t null, Proposition 1 gives E0,t [E
                                                  bt ] ≤ 1.

Using the online e-BH procedure, testing using the sequence of e-values (E    bt )T yields nested accepted sets
                                                                                  t=1
Rt (λ) and the κ-acceptance time τκ (λ) = inf{t : |Rt (λ)| ≥ κ} ∧ T . Explicitly, for a nonnegative unit schedule
(γt )t≥1 with t≥1 γt = 1 and a scale λ ≥ 0,
             P

                                                                            (     t                                )
                                           1                                                           1
                                                                                          1
                                                                                    X
           Rt (λ) =         s≤t:E
                                bs ≥                     ,      kt (λ) = max k :              E
                                                                                              bs ≥                ≥k       ,         (11)
                                       αλγs kt (λ)                                  s=1
                                                                                                     αλγs k

where max(∅) = 0 and 1/0 = ∞. At λ = 1, marginal validity of the roundwise e-values and the online e-BH
guarantee of Fischer et al. [2024] are sufficient to yield
                                              h              i
                                            E sup FDP(Rt (1)) ≤ α
                                                       t≥1

under arbitrary within-run dependence, and hence the trajectory guarantee of Equation (1).

6.2     Robust-core calibration
While setting λ = 1 yields a valid FDR-controlling algorithm, this choice can be conservative [Fischer
et al., 2024]. To select λ > 1, we apply the robust-core CRC algorithm using a calibration dataset
B c := {Runc1 , . . . , Runcnc }. We assume that the runs in B c and Runtest are exchangeable and that their
joint collection is independent of B e . Using B e , we apply the construction of Section 6.1 to each conformal
                                                                                   bt(i) , Rt(i) (λ), and τκ(i) (λ). Unindexed
calibration run Runci in lieu of Runtest . For i ∈ {1, . . . , nc }, this produces E
quantities Ebt , Rt (λ), and τκ continue to refer to Runtest .
                                                                                                                               (i)
Fix a finite ordered grid Λ = {λ1 < · · · < λM } ⊂ (1, ∞) and Λ0 := {0} ∪ Λ, with the convention Rt (0) = ∅.
For run i, define the loss function
                                                                    (i)
                                                                                                                                     (12)
                                                                         
                                    ℓi (λ) :=     max          FDP Rt (λ) ,         λ ∈ Λ0 ,
                                                       (i)
                                                1≤t≤τκ (λ)

                  (i)                                    (i)
so that FDP(Rτ (λ)) ≤ ℓi (λ) whenever τ ≤ τκ (λ). The fallback λ = 0 makes no discoveries, so ℓi (0) = 0.
Given that the runs in B c are labeled, the loss profiles ℓ1 , . . . , ℓnc are fully observable. The loss profile ℓ for
Runtest is nonetheless unobserved as its oracle ground-truth labels are hidden. As detailed in Section 5.2,
applying the finite-grid robust-core procedure returns the most preferred λ         bcore ∈ Λ, which remains valid for
any test loss function ℓ, or the fallback 0 when the robust core is empty.
Proposition 3 (Exchangeability of loss profiles). Suppose the runs in B c ∪ {Runtest } are exchangeable and
jointly independent of B e . Applying the same construction to each run yields loss profiles ℓ1 , . . . , ℓnc , ℓ that
are exchangeable conditional on B e and hence marginally exchangeable.
Theorem 5 (End-to-end trajectory-level FDR control). Fix κ ≥ 1 and assume the conditions of Proposition 3.
Let λ
    bcore be the robust-core choice at level α computed from ℓ1 , . . . , ℓn . Then
                                                                            c



                                                                                                                                     (13)
                                                                   
                                                         E ℓ(λ
                                                             bcore ) ≤ α,

and consequently, for every unobserved-run stopping time τ ≤ τκ (λ
                                                                 bcore ),
                                                                  
                                                  E FDP Rτ (λ
                                                            bcore ) ≤ α.


                                                                 14
               A. Oracle Qg                 B. Final verifier Vg, , T                                     C. Deployment stopped FDP
      3                                 3                                               0.3          target y =
                                                                                                     Robust-Core CRC
                                                                                                     Envelope CRC




                                                                        empirical FDP
                                                                                                     online e-BH
                                                                                        0.2
      0                                 0
x2




                                                                                        0.1
      3                                 3
                                                                                        0.0
           3        0          3             3         0           3                          0.10         0.15         0.20      0.25   0.30
                    x1                                 x1                                                          target level

Figure 5: Synthetic Gaussian-ring validation. Panels A and B show the same sampled 50-round trajectory
with no stopping rule applied, so they do not depend on α. Panel A shows the oracle field Qg := B + Gg ,
which coincides with the initial verifier field Vg,ξ,1 , and Panel B shows the final verifier field Vg,ξ,T . The filled
contours give the value of the field at each point of R2 , with brighter colors for larger values. The yellow star
marks µg , and the red cross marks µg+ξ . Panel C reports the mean stopped FDP against the target level α,
with 95% Monte Carlo intervals over 20 independent repetitions.


6.3       End-to-end validation on synthetic data
We now illustrate the full procedure on a synthetic example. In this setup, a generator moves in the plane
toward regions where the verifier score is high. We define a proposal to be correct if it is closer to a hidden
target center µg than to any other center. Over the run, the verifier moves its extra reward from the target
center to a neighboring center, so high verifier scores become less and less indicative of correctness. Let
µ0 , . . . , µ9 be equally spaced on the circle of radius R = 2.5 centered at the origin in R2 . Each run draws a
hidden target index g ∈ {0, . . . , 9} and a neighbor offset ξ ∈ {−1, +1}, with indices taken modulo 10. Writing
                                               P9
Gk (x) = exp(−∥x − µk ∥2 /2) and B(x) = k=0 Gk (x), the time-t verifier score is
                                                                                                                       t−1
                         Vg,ξ,t (x) = B(x) + wt Gg (x) + (1 − wt )Gg+ξ (x),                               wt = 1 −          .
                                                                                                                       T −1
In words, the verifier starts by placing additional mass on µg , which is then transferred to µg+ξ over the run.
Each trajectory uses T = 50 rounds and starts from a randomly drawn point X0 ∼ N (0, R2 I2 ). At round t,
the generator draws candidate locations Zt,1 , . . . , Zt,12 conditionally independently according to
                                               ind         2
                                                                  
                                   Zt,j | Xt−1 ∼ N Xt−1 , σprop I2 ,                            j ∈ {1, . . . , 12},

where σprop = R sin(π/10), which is proportional to the distance between two neighboring points on the
circle. Conditional on the candidates, the generator samples an index Jt with
                                                             Vg,ξ,t (Zt,j )
                          P Jt = j | Zt,1 , . . . , Zt,12 = P12                 ,                         j ∈ {1, . . . , 12},
                                                             ℓ=1 Vg,ξ,t (Zt,ℓ )

and sets Xt = Zt,Jt . The observed proxy score is St = Vg,ξ,t (Xt ). The oracle label is Yt = 1 if Xt is closer
to µg than to any other basin center, and Yt = 0 otherwise. Thus, a trajectory can continue receiving high
verifier scores while moving toward the incorrect neighboring basin µg+ξ . This design aims to simulate a
setting where the verifier and ground-truth correctness are increasingly misaligned as rounds pass.
We repeated the experiment for 20 runs. For each run, we use 100 sampled trajectories for the e-value
construction split B e , 500 trajectories for the conformal calibration split B c , and 350 trajectories as evaluation
runs. Each evaluation run plays the role of Runtest with its labels withheld while the stopping rule is applied.
Its correctness labels are then used only to compute stopped FDP.
The round-wise e-values use the feature log St and a roundwise likelihood-ratio estimate based on one-
dimensional Gaussian kernel density estimation. Online e-BH uses the uniform schedule γt = 1/T with κ = 1.


                                                                  15
We compare Robust-Core CRC, Envelope CRC, and the unscaled online e-BH. Robust-Core CRC selects
over the uniform grid {0, 1, . . . , 16}. Envelope CRC is optimized over the continuous interval [0, 16] using
the changepoints of the online e-BH loss. The reported loss is the FDP at stopping, averaged over the 350
evaluation runs. Bands in Figure 5 are the mean ±2 standard errors over the 20 repetitions of the experiment
at α ∈ {0.10, 0.15, 0.20, 0.25, 0.30}.
Panel C of Figure 5 plots FDP at stopping against the target level α. The diagonal y = α marks a procedure
that spends its error budget exactly. Online e-BH sits far below the diagonal because it fixes λ = 1. At
α = 0.10, Robust-Core CRC and Envelope CRC have similar mean FDPs of 0.082 and 0.085. Robust-Core
CRC is closer to the diagonal for larger α levels but the difference between Envelope CRC and Robust-Core
CRC is very minor at smaller α values.


7    Experiments




Figure 6: Motif scaffolding examples. Each column shows a MotifBench-derived task after scaffolding.
The fixed motif is magenta and the designed scaffold is grey.

To illustrate the utility of our approach in a more realistic scenario, we consider a sequential protein-design
setting, where the generator adapts to a cheap verifier. Informally, a protein generative model proposes a set
of particles in R3 representing the positions of the protein’s backbone atoms. In motif scaffolding, some of
these particles form a fixed functional motif, which the model aims to surround with a supporting section of
the protein, also known as the scaffold. Our aim is to determine whether the proposed three-dimensional
structure is designable. A three-dimensional structure is designable if there exists an amino-acid sequence
that plausibly folds into it.
A common computational test of designability compares the proposed protein backbone with the result of
a sequence-design-and-refolding procedure [Zheng et al., 2025]. First, a generative model proposes a three-
dimensional structure of the protein backbone. Then, an inverse-folding model predicts amino-acid sequences
that could produce the protein backbone proposed by the generative model. A structure-prediction model,
such as AlphaFold3 [Abramson et al., 2024], then folds each predicted sequence independently, producing
another set of structures in R3 . If the refolded structure closely matches the original proposal, this provides
evidence that the proposed protein backbone is physically plausible in the sense that it can be realized by an
amino-acid sequence.
We measure structural agreement using root-mean-square deviation (RMSD). For each comparison, we
rigidly align the relevant regions of the proposed and refolded structures. RMSD is the square root of the
average squared distance between corresponding atoms after alignment, so smaller values indicate closer
structural agreement. The score uses three RMSD terms. RMSDbb-ESM compares the complete proposed
protein backbone with the refolded one. RMSDscaffold measures agreement across the generator’s recorded
scaffold region. RMSDmotif measures how well the refolded structure preserves the prescribed motif geometry.
Appendix B.2 specifies the exact atoms and structural masks used for each term. The score also includes
pLDDTmean , the mean predicted local distance difference test score, and pTM, the predicted Template
Modeling score. Larger pLDDTmean and pTM values indicate greater confidence in the local geometry and
overall fold, respectively.
We compute these measurements using a cheap verification pipeline. The Protein Message Passing Neural


                                                      16
                        seed                      noised proposals                                         ProteinMPNN + ESMFold + Scoring


                                   perturb                                denoise




                                                                                                           0.42              0.74               0.31
                                                                                                                  round-t winner    seeds t+1

Figure 7: One round of the protein feedback loop. Four exploit candidates continue from the stored
midpoint state associated with the previous winner, while four explore candidates start from the original
motif specification. The cheap ProteinMPNN–ESMFold pipeline scores the resulting proposals, and the
midpoint state associated with the highest-scoring proposal seeds round t+1.


Network (ProteinMPNN) [Dauparas et al., 2022] predicts eight amino-acid sequences for each proposed
protein backbone. ESMFold [Lin et al., 2023], a computationally light structure-prediction model, folds each
sequence independently and therefore produces eight refolded structures. For each sequence–refold pair, the
cheap verifier computes the three RMSDs, mean pLDDT, and pTM, then combines them into an individual
proxy score

                                  S = pLDDTmean + 100 pTM − 10 RMSDbb-ESM − 5 RMSDscaffold − 20 RMSDmotif .

We note that this score function was not particularly tuned to correlate with a specific notion of ground-truth
correctness. Rather, the weighting of the different terms was heuristically selected to balance the scale and
importance of different terms. The first two terms reward refolds that ESMFold considers reliable, while the
RMSD terms penalize disagreement with the intended structure. Motif disagreement receives the largest
penalty because preserving the prescribed motif geometry is the central constraint of the task.

                                                                     RFdiffusion                           Proteina
                                       A. Cheap-verifier score                                              B. Motif RMSD and mean pLDDT
                        155                                                                                                                                 88
Cumulative-best score




                                                                                                 0.8
                                                                               Motif RMSD (Å)




                                                                                                                                                                 Mean pLDDT
                        150                                                                                                                                 87
                                                                                                 0.7
                        145                                                                                                                                 86

                        140                                                                      0.6                                                        85

                        135                                                                      0.5                                                        84
                              0    5         10     15        20   25     29                           0       5        10     15        20   25       29
                                             Feedback round                                                             Feedback round

Figure 8: Cheap-verifier trends across rounds. At each round, we retain the design with the highest
cheap-verifier score seen in each trajectory. Solid circles denote RFdiffusion and dashed squares denote
Proteina. Panel A reports cumulative-best score. Panel B reports ESMFold motif RMSD on the left axis and
mean pLDDT on the right axis.

We use this cheap verification score inside a 30-round feedback loop with RoseTTAFold diffusion (RFdiffu-
sion) [Watson et al., 2023] and Proteina [Geffner et al., 2025]. Both models generate structures by progressively
transforming a noisy intermediate state into three-dimensional coordinates. During each trajectory, we save


                                                                                     17
the generator’s partially noised state at the midpoint. The first round contains eight fresh candidates from
the original motif specification. Every later round contains four fresh explore candidates and four exploit
candidates. The explore candidates are generated from scratch while the exploit candidates are generated
from the midpoint state corresponding to the previous best-scoring structure. Appendix B.2 gives the detailed
description of the feedback structure.
Figure 8 shows rapid gains during the early feedback rounds followed by a gradual plateau for both generators.
The score curves are nondecreasing by construction because each trajectory retains its best scoring candidate
by design. Motif RMSD generally decreases over the same rounds, while mean pLDDT increases. Proteina
reaches a lower motif RMSD, whereas RFdiffusion attains a higher mean pLDDT. These trends show that
feedback finds proposals with better motif preservation and higher confidence, as scored through the cheap
verification. Thus, as rounds pass, there is a risk of favoring proposals well-scored by the cheap verifier rather
than properties associated with ground-truth correctness.

                                 A. RFdiffusion stopped FDP                           B. Proteina stopped FDP
              0.20          target       =5                            0.20
                              =1         = 10
stopped FDP




              0.15                                                     0.15
              0.10                                                     0.10
              0.05                                                     0.05
              0.00                                                     0.00
                              C. RFdiffusion returned designs                        D. Proteina returned designs
                4                                                        4
mean returned
(capped at )




                3                                                        3
                2                                                        2
                1                                                        1
                0                                                        0
                     0.05           0.10            0.15        0.20          0.05       0.10            0.15       0.20
                                           target                                               target

Figure 9: Stopped risk and utility on held-out trajectories. The robust-core calibrated online e-BH
rule is evaluated over target levels α ∈ {0.05, 0.10, 0.15, 0.20} and target acceptance counts κ ∈ {1, 5, 10}.
Panels A and B report stopped FDP for RFdiffusion and Proteina. Panels C and D report returned designs,
with counts capped at κ, for the same two generators.

For ground-truth correctness, we use AlphaFold 3 [Abramson et al., 2024] as a more computationally expensive
oracle. A selected proposal is successful when the AlphaFold 3 prediction for its associated amino-acid
sequence, predicted by ProteinMPNN, matches the prescribed motif within 0.75 Å RMSD, matches the
proposed backbone within 1.5 Å Cα RMSD over the scaffold mask, has pTM at least 0.80, and has mean
pLDDT at least 85. We also note that these criteria were heuristically selected and the pipeline may be
reimplemented with different metrics for ground truth correctness.
We generated 300 labeled trajectories for each of Proteina and RFdiffusion. A single trajectory is a 30-round
feedback run for a fixed motif-scaffolding task. For each held-out trajectory, the remaining 299 trajectories
from the same generator are split into 199 for e-value construction and 100 for conformal calibration. The
stopping rule is replayed on the held-out trajectory with its AlphaFold 3 labels withheld. Stopped FDP and
the number of returned designs are scored afterward. Additional details are provided in Appendix B.
Figure 9 shows the stopped FDP of the full procedure. In Panels A and B, stopped FDP increases as α
increases, while the curves for different values of κ remain close. Thus, allowing more accepted designs does
not substantially increase the observed error rate. Panels C and D show the corresponding increase in utility,
with larger values of both α and κ returning more designs.


                                                                  18
8    Conclusions
In this paper, we study how to safely stop generator–verifier loops that use a cheap verifier to scale inference-
time computation. While repeated verifier feedback allows the generator to efficiently explore many proposals
without repeatedly querying an expensive oracle, it can also bias the search towards samples that are
well-scored by the verifier but not by the ground-truth oracle. In our proposed approach, we cast this setting
as an online multiple-testing problem and combine index-betting e-values, robust-core conformal risk control,
and online e-BH to solve it. The resulting procedure controls stopped FDR up to the κ-acceptance time while
permitting arbitrary dependence within a run. Our synthetic experiments validate the statistical construction,
and the protein-design study shows how it can be applied to a more realistic setting.
We foresee two possible extensions of our approach. First, the current guarantee requires the logged and
deployed runs to be exchangeable or even i.i.d. This requirement remains a limitation, as in many real-
world examples data arrives sequentially and may not be exchangeable. A weighted form of conformal risk
control [Prinster et al., 2026], inspired by weighted conformal prediction under covariate shift [Tibshirani
et al., 2019] and more general distribution shifts [Barber et al., 2023, Prinster et al., 2024], could extend
our results to the non-exchangeable setting. Nonetheless, combining weighted conformal prediction with
our non-monotone construction remains an open problem. Second, many inference-time systems organize
proposals as a tree or directed acyclic graph rather than a single trajectory. Extending our framework from
looped trajectories to more adaptive tree or graph construction would require FDR control under adaptive
branching, pruning, and merging of different proposed solutions.


Acknowledgements
We thank Drew Prinster for a careful reading of an earlier version and for detailed feedback and discussion,
which improved the presentation and content of this manuscript. The work of Aymeric Dieuleveut and
Mahmoud Hegazy is supported by French State aid managed by the Agence Nationale de la Recherche
(ANR) under the France 2030 program with the reference ANR-23-PEIA-005 (REDEEM project), and
ANR-23-IACL-0005, in particular the Hi!Paris FLAG chair. This project is part of the Chair “Markets and
Learning,” supported by Air Liquide, BNP PARIBAS ASSET MANAGEMENT Europe, EDF, Orange and
SNCF, sponsors of the Inria Foundation. We also acknowledge access to the HPC resources of IDRIS under
the allocations AD011017341 and A0201017541 by GENCI. Finally, the work of Michael Jordan is supported
by the European Union (ERC-2022-SYG-OCEAN-101071601). Views and opinions expressed are however
those of the authors only and do not necessarily reflect those of the European Union or the European Research
Council Executive Agency. Neither the European Union nor the granting authority can be held responsible
for them.


References
Josh Abramson, Jonas Adler, Jack Dunger, Richard Evans, Tim Green, Alexander Pritzel, Olaf Ronneberger,
  Lindsay Willmore, Andrew J. Ballard, Joshua Bambrick, et al. Accurate structure prediction of biomolecular
  interactions with AlphaFold 3. Nature, 630:493–500, 2024. doi: 10.1038/s41586-024-07487-w. URL
  https://doi.org/10.1038/s41586-024-07487-w.
Anastasios N. Angelopoulos. Conformal risk control for non-monotonic losses, 2026. URL https://arxiv.
 org/abs/2602.20151. arXiv:2602.20151.
Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, and Tal Schuster. Conformal risk
 control. In International Conference on Learning Representations. OpenReview.net, 2024. URL https:
 //openreview.net/forum?id=33XGfHLtZg.
Anastasios N. Angelopoulos, Stephen Bates, Emmanuel J. Candès, Michael I. Jordan, and Li-
 hua Lei.    Learn then test: Calibrating predictive algorithms to achieve risk control. The
 Annals of Applied Statistics, 19(2):1641–1662, June 2025. doi: 10.1214/24-AOAS1998. URL
 https://projecteuclid.org/journals/annals-of-applied-statistics/volume-19/issue-2/


                                                       19
  Learn-then-test--Calibrating-predictive-algorithms-to-achieve-risk/10.1214/24-AOAS1998.
  full.
Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas, and Ryan J. Tibshirani. Conformal prediction
  beyond exchangeability. The Annals of Statistics, 51(2):816–845, April 2023. ISSN 0090-5364. doi:
  10.1214/23-AOS2276. URL https://doi.org/10.1214/23-AOS2276.
Julian Besag and Peter Clifford. Generalized Monte Carlo significance tests. Biometrika, 76(4):633–642, 1989.
  ISSN 1464-3510. doi: 10.1093/biomet/76.4.633. URL http://dx.doi.org/10.1093/biomet/76.4.633.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, et al. Evaluating
 large language models trained on code. arXiv preprint arXiv:2107.03374, 2021. URL https://arxiv.org/
 abs/2107.03374.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
 Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training
 verifiers to solve math word problems, 2021. URL https://arxiv.org/abs/2110.14168.
Peter J. A. Cock, Tiago Antao, Jeffrey T. Chang, Brad A. Chapman, Cymon J. Cox, Andrew Dalke, Iddo
  Friedberg, Thomas Hamelryck, Frank Kauff, Bartek Wilczynski, and Michiel J. L. de Hoon. Biopython:
  freely available python tools for computational molecular biology and bioinformatics. Bioinformatics, 25
 (11):1422–1423, March 2009. ISSN 1367-4803. doi: 10.1093/bioinformatics/btp163. URL http://dx.doi.
  org/10.1093/bioinformatics/btp163.
Justas Dauparas, Ivan Anishchenko, Nathaniel Bennett, Hua Bai, Robert J. Ragotte, Lukas F. Milles, Basile
  I. M. Wicky, Alexis Courbet, Robert J. de Haas, Nate Bethel, et al. Robust deep learning–based protein
  sequence design using ProteinMPNN. Science, 378(6615):49–56, October 2022. ISSN 1095-9203. doi:
  10.1126/science.add2187. URL http://dx.doi.org/10.1126/science.add2187.
Alexander Dombowsky, Barbara E. Engelhardt, and Aaditya Ramdas. Besag-clifford e-values for unnormalized
  testing, 2026. URL https://arxiv.org/abs/2603.15845.
Lasse Fischer and Aaditya Ramdas. Sequential monte carlo testing by betting. Journal of the Royal
  Statistical Society Series B: Statistical Methodology, 87(4):1200–1220, April 2025. ISSN 1467-9868. doi:
  10.1093/jrsssb/qkaf014. URL http://dx.doi.org/10.1093/jrsssb/qkaf014.
Lasse Fischer, Ziyu Xu, and Aaditya Ramdas. An online generalization of the (e-)benjamini-hochberg
  procedure. arXiv preprint arXiv:2407.20683, 2024. URL https://arxiv.org/abs/2407.20683.
Tomas Geffner, Kieran Didi, Zuobai Zhang, Danny Reidenbach, Zhonglin Cao, Jason Yim, Mario
  Geiger, Christian Dallago, Emine Kucukbenli, Arash Vahdat, and Karsten Kreis. Proteina: Scal-
  ing flow-based protein structure generative models. In International Conference on Learning Rep-
  resentations (ICLR), 2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/
  f4e9121ad30cd4e5528042fbfd835b3f-Abstract-Conference.html.
Audrey Huang, Adam Block, Qinghua Liu, Nan Jiang, Akshay Krishnamurthy, and Dylan J. Foster. Is best-of-
 n the best of them? Coverage, scaling, and optimality in inference-time alignment. In Proceedings of the 42nd
 International Conference on Machine Learning, volume 267 of Proceedings of Machine Learning Research,
 pages 25075–25126. PMLR, 2025. URL https://proceedings.mlr.press/v267/huang25c.html.
John L. Kelly, Jr. A new interpretation of information rate. Bell System Technical Journal, 35(4):917–926,
  July 1956. ISSN 0005-8580. doi: 10.1002/j.1538-7305.1956.tb03809.x. URL http://dx.doi.org/10.1002/
  j.1538-7305.1956.tb03809.x.
Hadi Khalaf, Claudio Mayrink Verdun, Alex Oesterling, Himabindu Lakkaraju, and Flavio du Pin
 Calmon. Inference-time reward hacking in large language models. In Advances in Neural In-
 formation Processing Systems 38. Neural Information Processing Systems Foundation, Inc., 2025.
 doi: 10.52202/085713-2064. URL https://proceedings.neurips.cc/paper_files/paper/2025/hash/
 590a0cc0306c1c63e2d66a51a407718f-Abstract-Conference.html.




                                                     20
Nick W. Koning. Measuring evidence against exchangeability and group invariance with E-values. The
  Annals of Statistics, 54(4):1843–1869, 2026. doi: 10.1214/26-aos2627. URL https://doi.org/10.1214/
  26-aos2627.
Martin Larsson, Aaditya Ramdas, and Johannes Ruf. The numeraire e-variable and reverse information
 projection. The Annals of Statistics, 53(3):1015–1043, June 2025. ISSN 0090-5364. doi: 10.1214/24-aos2487.
 URL http://dx.doi.org/10.1214/24-aos2487.
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles,
  James Keeling, Felix Gimeno, et al. Competition-level code generation with alphacode. Science, 378(6624):
 1092–1097, December 2022. ISSN 1095-9203. doi: 10.1126/science.abq1158. URL http://dx.doi.org/10.
  1126/science.abq1158.
Zeming Lin, Halil Akin, Roshan Rao, Brian Hie, Zhongkai Zhu, Wenting Lu, Nikita Smetanin, Robert Verkuil,
  Ori Kabeli, Yaniv Shmueli, et al. Evolutionary-scale prediction of atomic-level protein structure with a
  language model. Science, 379(6637):1123–1130, March 2023. ISSN 1095-9203. doi: 10.1126/science.ade2574.
  URL http://dx.doi.org/10.1126/science.ade2574.
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha
 Dziri, Shrimai Prabhumoye, et al. Self-refine: Iterative refinement with self-feedback. In Advances in Neural
 Information Processing Systems 36, NeurIPS 2023, pages 46534–46594. Neural Information Processing
 Systems Foundation, Inc., 2023. doi: 10.52202/075280-2019. URL https://proceedings.neurips.cc/
 paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving. arXiv
  preprint arXiv:2009.03393, 2020. URL https://arxiv.org/abs/2009.03393.
Drew Prinster, Samuel Don Stanton, Anqi Liu, and Suchi Saria. Conformal validity guarantees exist for any
  data distribution (and how to find them). In Proceedings of the 41st International Conference on Machine
 Learning, volume 235 of Proceedings of Machine Learning Research, pages 41086–41118. PMLR, 2024. URL
  https://proceedings.mlr.press/v235/prinster24a.html.
Drew Prinster, Clara Fannjiang, Ji Won Park, Kyunghyun Cho, Anqi Liu, Suchi Saria, and Samuel Don
  Stanton. Conformal policy control. In Proceedings of the 43rd International Conference on Machine
 Learning, volume 306 of Proceedings of Machine Learning Research, pages 99772–99824. PMLR, 2026. URL
  https://proceedings.mlr.press/v306/prinster26a.html.
Aaditya Ramdas, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. Game-theoretic statistics and safe
 anytime-valid inference. Statistical Science, 38(4):576–601, November 2023. ISSN 0883-4237. doi: 10.1214/
 23-sts894. URL http://dx.doi.org/10.1214/23-sts894.
Shuvom Sadhuka, Drew Prinster, Clara Fannjiang, Gabriele Scalia, Bonnie Berger, Aviv Regev, and Hanchen
  Wang. E-valuator: Reliable agent verifiers with sequential hypothesis testing, 2025. URL https://arxiv.
  org/abs/2512.03109.
Glenn Shafer. Testing by betting: A strategy for statistical and scientific communication. Journal of the
  Royal Statistical Society Series A: Statistics in Society, 184(2):407–431, April 2021. ISSN 1467-985X. doi:
  10.1111/rssa.12647. URL http://dx.doi.org/10.1111/rssa.12647.
Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language
  agents with verbal reinforcement learning. In Advances in Neural Information Processing Systems 36,
  NeurIPS 2023, page 8634–8652. Neural Information Processing Systems Foundation, Inc. (NeurIPS), 2023.
  doi: 10.52202/075280-0377. URL http://dx.doi.org/10.52202/075280-0377.
Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel J. Candès, and Aaditya Ramdas. Conformal prediction
  under covariate shift. In Advances in Neural Information Processing Systems 32, pages 2526–2536, 2019.
  URL https://arxiv.org/abs/1904.06019.
Ruodu Wang and Aaditya Ramdas. False discovery rate control with e-values. Journal of the Royal




                                                     21
  Statistical Society Series B: Statistical Methodology, 84(3):822–852, July 2022. ISSN 1467-9868. doi:
  10.1111/rssb.12489. URL http://dx.doi.org/10.1111/rssb.12489.
Larry Wasserman, Aaditya Ramdas, and Sivaraman Balakrishnan. Universal inference. Proceedings of the
  National Academy of Sciences, 117(29):16880–16890, July 2020. ISSN 1091-6490. doi: 10.1073/pnas.
  1922664117. URL http://dx.doi.org/10.1073/pnas.1922664117.
Joseph L. Watson, David Juergens, Nathaniel R. Bennett, Brian L. Trippe, Jason Yim, Helen E. Eisenach,
  Woody Ahern, Andrew J. Borst, Robert J. Ragotte, Lukas F. Milles, et al. De novo design of protein
  structure and function with RFdiffusion. Nature, 620(7976):1089–1100, July 2023. ISSN 1476-4687. doi:
  10.1038/s41586-023-06415-8. URL http://dx.doi.org/10.1038/s41586-023-06415-8.
Ziyu Xu and Aaditya Ramdas. Online multiple testing with e-values. In Proceedings of The 27th International
  Conference on Artificial Intelligence and Statistics, volume 238 of Proceedings of Machine Learning Research,
  pages 3997–4005. PMLR, 2024. URL https://proceedings.mlr.press/v238/xu24a.html.
Zhuoqi Zheng, Bo Zhang, Kieran Didi, Kevin K. Yang, Jason Yim, Joseph L. Watson, Hai-Feng Chen, and
  Brian L. Trippe. Motifbench: A standardized protein design benchmark for motif-scaffolding problems,
  2025. URL https://arxiv.org/abs/2502.12479.




                                                      22
A       Deferred Proofs
Throughout the proof subsections for Section 4, n denotes the number of logged null windows. Accordingly,
the augmented null batch has size n + 1, which corresponds to n0,t in the main text. We fix t and write
P := P0,t , Q := P1,t , and L := dQ/dP .

A.1     Proposition 2
Proof. All probabilities and expectations below are under the alternative. By the i.i.d. assumption of
                                                    iid
Section 2, Z0 ∼ Q is independent of Z1 , . . . , Zn ∼ P . Let Π be a uniformly random permutation of {0, . . . , n},
independent of (Z0 , . . . , Zn ). Write
                                          ek := ZΠ(k) ,
                                          Z                    J ⋆ := Π−1 (0).

Thus Ze = (Z e0 , . . . , Zen ) is the ordered batch and J ⋆ is the position occupied by Z0 . Since J ⋆ is a function of
Π alone, it is uniform on {0, . . . , n} and independent of (Z0 , . . . , Zn ).
Hence, conditional on J ⋆ = j, the different coordinates of Z
                                                            e are independent, with Zej ∼ Q and Zeℓ ∼ P for
every ℓ ̸= j. Bayes’ rule gives
                      e ⋆               ⋆
             e = P Pr(Z | J = j) Pr(J = j)            L(Zej )/(n + 1)        L(Z
                                                                               ej )
Pr(J ⋆ = j | Z)   n
                                                   = Pn                   = Pn         ,                 j = 0, . . . , n,
                      Pr(Ze | J ⋆ = ℓ) Pr(J ⋆ = ℓ)
                       ℓ=0                               L(Z eℓ )/(n + 1)
                                                               ℓ=0             L(Zeℓ )    ℓ=0

almost surely.
Consider q ∈ Rn+1 such that qj = Pr(J ⋆ = j | Z).
                                                e For any (Z0 , . . . , Zn ), any maximizing budgeted strategy
Pmust
β
  n
        satisfy βj > 0 whenever qj > 0, since otherwise its conditional expected log-wealth is −∞ and satisfy
  j=0 βj = 1 (otherwise rescaling increases the conditional expected log-wealth). Thus it remains to optimize
over the simplex, where
                         h                   i             n
                                                           X
                                         
                        E log (n + 1)βJ | Z = log(n + 1) +
                                       ⋆   e                 qj log qj − DKL (q∥β).
                                                                     j=0

Nonnegativity of the KL divergence shows that the unique maximizer is β = q. Substituting the posterior
above yields
                                     e = P L(Zj ) ,
                                               e
                               βjLR (Z)     n
                                                          j = 0, . . . , n.
                                               L(Zeℓ )
                                                    ℓ=0
This rule is batch-symmetric, so it also maximizes conditional expected log-wealth within the batch-symmetric
class.

A.2     Theorem 1
                                           iid
Proof. Let Z ∼ Q and let Z10 , . . . , Zn0 ∼ P be independent of Z. Write L0 := L(Z), L
                                                                                      b 0 := L
                                                                                             b −0 (Z),
Lj := L(Zj ), and Lj := L−j (Zj ) for 1 ≤ j ≤ n. Then
          0       b     b     0

                                                                             n
                                                                            X       
                                  log E idx = log(n + 1) + log L0 − log            Lj ,
                                                                             j=0

and similarly
                                                                             n
                                                                            X       
                                      b idx = log(n + 1) + log L
                                  log E                        b 0 − log           L
                                                                                   bj .
                                                                             j=0

Hence
                                                                        n
                                                                       X                 n
                                                                                          X   
                    log E idx − log E
                                    b idx ≤ log L0 − log L
                                                         b 0 + log               Lj − log    L
                                                                                             bj .
                                                                           j=0            j=0



                                                          23
Set
                                              m := max log Lj − log L
                                                                    bj .
                                                      0≤j≤n

Then e      Lj ≤ Lj ≤ e Lj for every j, so after summing,
         −m b            mb


                                                   n
                                                   X            n
                                                                X               n
                                                                                X
                                         e−m             L
                                                         bj ≤         Lj ≤ em         L
                                                                                      bj .
                                                   j=0          j=0             j=0

Therefore
                                                   n
                                                  X              n
                                                                  X    
                                            log          Lj − log    b j ≤ m,
                                                                     L
                                                   j=0                  j=0

and the claim follows.

A.3       Theorem 2
                                      iid
Proof. Let Z ∼ Q, let Z10 , . . . , Zn0 ∼ P , independent of Z, and set L0 := L(Z), Lj := L(Zj0 ), and Sn :=
Pn
  j=1 Lj . Since
                                                                 L0
                                               E idx = (n + 1)         ,
                                                               L0 + Sn
we have                                                                       L + S 
                                                                                0   n
                                    ∆n := log L0 − log E idx = log                    .
                                                                                n+1

Condition on L0 . By Jensen’s inequality,
                                                      L + E [S ]                   L0 − 1 
                                                          0      P     n
                              E[∆n | L0 ] ≤ log                             = log 1 +          ,
                                                              n+1                     n+1
because EP [L] = 1, hence EP [Sn ] = n.
Since u 7→ log(1 + u) is increasing and (L0 − 1)/(n + 1) ≥ −1,
                                            L0 − 1           (L0 − 1)+ 
                                     log 1 +          ≤ log 1 +             .
                                             n+1                  n+1

Set Cδ := supx>0 log(1 + x)/xδ . By the definition of Cδ ,

                                             log(1 + x) ≤ Cδ xδ ,             x ≥ 0.

Applying this with x = (L0 − 1)+ /(n + 1) yields

                                                                     Cδ (L0 − 1)δ+
                                                  E[∆n | L0 ] ≤                    .
                                                                       (n + 1)δ

Taking expectation under Q and using E1 [g(L0 )] = EP [L g(L)],

                                   Cδ E1 [(L0 − 1)δ+ ]   Cδ EP [L(L − 1)δ+ ]   Cδ EP [L1+δ ]
                      E1 [∆n ] ≤                       =                     ≤               .
                                       (n + 1)δ              (n + 1)δ            (n + 1)δ




                                                                 24
A.4     Theorem 3
                2 . For each sufficiently large n, let L have the two-point law
Proof. Fix a = B−1

                                                                                            1 − np
                     P (L = n) = p := an−(1+δ) ,        P (L = y) = 1 − p,           y :=          .
                                                                                             1−p

Then 0 < y < 1 and EP [L] = 1, so dQ = L dP defines a probability distribution. Moreover,

                                                                            B+1
                              EP [L1+δ ] = a + y 1+δ (1 − p) −→ a + 1 =         < B.
                                                                             2
Thus (P, Q) ∈ P1+δ (B) for all sufficiently large n. Under Q,

                                Q(L = n) = np = an−δ ,         Q(L = y) = 1 − np.

                               iid
Let L0 ∼ Q and L1 , . . . , Ln ∼ P be independent, and let H count how many of L0 , . . . , Ln equal n. The
average (L0 + · · · + Ln )/(n + 1) equals y when H = 0 and n(1 + y)/(n + 1) when H = 1. It exceeds one when
H ≥ 2 and n is large. Therefore,
                                                               
                                                L0 + · · · + Ln
              E1 log L0 − log E idx = E1 log
                                    
                                                    n+1
                                      ≥ (1 − np)(1 − p)n log y
                                                                                          
                                                                                  n(1 + y)
                                        + np(1 − p)n + (1 − np)np(1 − p)n−1 log
                                                                          
                                                                                             .
                                                                                   n+1

Since δ ∈ (0, 1),
                                                                                                   
                                                                                         n(1 + y)
   log y = −an−δ + O(n−2δ ),         (1 − p)n = 1 − an−δ + O(n−2δ ),           log                      = log 2 + O(n−δ ).
                                                                                          n+1

Substitution gives
                              E1 log L0 − log E idx ≥ a(2 log 2 − 1)n−δ + O(n−2δ ).
                                                  

Since 2 log 2 − 1 > 0, the right-hand side is at least a2 (2 log 2 − 1)n−δ for all sufficiently large n. Finally,
Proposition 2 shows that E idx minimizes this gap among budgeted batch-symmetric strategies, so the same
lower bound applies to every such strategy.

A.5     Corollary 1
                        iid
Proof. Let Z0 , . . . , Zn ∼ P , set Lj := L(Zj ) for 0 ≤ j ≤ n, and define
                                                              n
                                                         1 X
                                               An :=             Lj .
                                                       n + 1 j=0

By change of measure and exchangeability,
                                                        ⊗(n+1)
                              E1 log L0 − log E idx = EP
                                                  
                                                               [L0 log An ]
                                                              n
                                                         1 X ⊗(n+1)
                                                     =           E        [Lj log An ]
                                                       n + 1 j=0 P
                                                         ⊗(n+1)
                                                     = EP         [An log An ] .

Since EP [L] = 1, the strong law of large numbers gives An → 1 almost surely, hence An log An → 0 almost
surely.


                                                         25
Now let ϕ(x) := x log x, with 0 log 0 = 0. The function ϕ is convex and bounded below by −e−1 . By Jensen,
                                                              n
                                                         1 X
                                            ϕ(An ) ≤             ϕ(Lj ),
                                                       n + 1 j=0

and hence
                                                          n
                                                     1 X
                                          ϕ+ (An ) ≤         ϕ+ (Lj ).
                                                   n + 1 j=0
                                                          Pn
Since EP [ϕ+ (L)] < ∞, the empirical averages (n + 1)−1 j=0 ϕ+ (Lj ) are uniformly integrable. Therefore
{ϕ+ (An )}n≥0 is uniformly integrable and {ϕ(An )}n≥0 is uniformly integrable. Since ϕ(An ) → 0 almost surely,
it follows that
                                             E[An log An ] → 0.



A.6     Theorem 4
Proof. Let C := G(ℓ1 , . . . , ℓn+1 ). Since the true loss profile ℓn+1 belongs to L almost surely, it is one of the
completions in the intersection defining the robust core. Hence Cn ⊆ C.
If Cn ̸= ∅, the selected parameter belongs to C, so its test loss is bounded by Ln+1 (C). If Cn = ∅, the fallback
incurs zero loss by Equation (8). Nonnegativity of the set loss, with Ln+1 (∅) = 0, therefore gives

                                             ℓn+1 (λ
                                                   bcore ) ≤ Ln+1 (C)

almost surely.
Symmetry of G and exchangeability of the loss profiles imply that L1 (C), . . . , Ln+1 (C) are identically
distributed. Taking expectations and using Equation (7),

                                   E[ℓn+1 (λ
                                           bcore )] ≤ E[Ln+1 (C)]
                                                        "       n+1
                                                                          #
                                                            1 X
                                                    =E              Li (C) ≤ α.
                                                          n + 1 i=1




A.7     Lemma 1
Proof. Consider the full scan without early termination. Suppose the frontier before processing λk represents
all attainable pairs of calibration maxima M and held-out maxima u, with each state (M, [a, b]) representing
{M }×[a, b]. Initially, the only attainable pair is (0n , 0). The unprocessed coordinates of w remain unrestricted
because U = [0, 1]Λ .
For a state (M, [a, b]), let M ′ and Θ be defined as in Algorithm 2. Inclusion requires max{u, w(λk )} ≤ Θ.
This is possible if and only if a ≤ Θ, and the new held-out maximum ranges over [a, min{1, Θ}]. Every value
r in this interval is attained by taking u = a and w(λk ) = r, giving the successor (M ′ , [a, min{1, Θ}]).
Skipping is possible if and only if Θ < 1. Choosing w(λk ) = 1 then produces a skip for every u ∈ [a, b],
leaving the state (M, [a, b]) unchanged. Merging identical successor states changes neither the attainable
pairs nor the freedom to choose the remaining coordinates.
Thus AllInclude is true at λk if and only if every completion includes that point. Later decisions cannot
remove it, so this condition is equivalent to membership in the robust core. Since the scan proceeds from most
to least preferred, it returns the largest member of the core, or the fallback when no point belongs to it.




                                                         26
A.8      Proposition 3 and Theorem 5
Proof. Work conditionally on the e-value construction split B e and fix κ ≥ 1. Independence of the conformal
calibration runs and the unobserved run from B e preserves their exchangeability under this conditioning. With
B e fixed, the construction in Sections 6.1 and 6.2 applies the same map to every such run. Any permutation of
the nc conformal calibration runs and the unobserved run therefore permutes the local e-value streams in the
same way. For each λ ∈ Λ0 , the online e-BH path, the stopping time, and the process loss are deterministic
functions of the corresponding e-value stream and run labels. The same permutation consequently relabels
ℓ1 , . . . , ℓnc , ℓ. Thus, they are conditional exchangeable. Integrating over B e gives marginal exchangeability
and completes the proof of Proposition 3.
By Lemma 1, Algorithm 2 returns the robust-core estimator from Equation (9) when applied to the conformal
calibration profiles ℓ1 , . . . , ℓnc . Since the fallback satisfies ℓi (0) = 0 for i = 1, . . . , nc and ℓ(0) = 0, Theorem 4
applies conditionally on B e and yields                 h             i
                                                      E ℓ(λbcore ) B e ≤ α.

Taking expectations over B e removes the conditioning and gives Equation (13). For any unobserved-run
stopping time τ ≤ τκ (λ
                      bcore ),
                                      FDP(Rτ (λ bcore )) ≤ ℓ(λ
                                                             bcore ).




B      Additional Experiment Details
For each of the 300 motif-scaffolding targets, each generator produces a 30-round trajectory, and AlphaFold 3
evaluation takes place after generation.

B.1     MotifBench-derived benchmark construction
We restrict ourselves to tasks whose motif is a single contiguous segment and use the ten tasks of Table 1,
taken from MotifBench [Zheng et al., 2025]. Each MotifBench task specifies the fixed motif and integer ranges
for the scaffold lengths on its left and right sides. For each task, we sample 30 distinct integer pairs of left
and right scaffold lengths within the specified ranges, which gives 10 × 30 = 300 targets. We use the same
300 targets for RFdiffusion and Proteina.

                       Task            Motif residues    Motif length     Left range    Right range
                       01_1LDB         A186–206               21            0–100          0–100
                       02_1ITU         A124–147               24            0–100          0–100
                       03_2CGA         A184–194               11            0–100          0–100
                       04_5WN9         A170–189               20            10–40          10–40
                       05_5ZE9         A229–243               15            0–100          0–100
                       06_6E6R         A23–35                 13             0–65           0–65
                       07_6E6R         A23–35                 13            0–190          0–190
                       08_7AD5         A99–113                15            0–100          0–100
                       09_7CG5         A6–20                  15            0–100          0–100
                       10_7WRK         A80–94                 15            0–100          0–100

Table 1: MotifBench source tasks used to construct the 300 targets, each fixing one pair of left and right
scaffold lengths.


B.2     Protein feedback loop
A feedback trajectory contains 30 rounds with eight candidate backbones per round. The first round
generates all eight backbones from the motif specification, while each later round combines four exploit



                                                             27
backbones sampled from the preceding winner’s midpoint state with four explore backbones sampled from
fresh trajectories.
ProteinMPNN [Dauparas et al., 2022] samples eight sequences per backbone at temperature 0.1 with no
backbone noise. It uses the full N, Cα, C, and O backbone for RFdiffusion and Cα-only geometry for Proteina.
ESMFold [Lin et al., 2023] refolds every sequence with two recycles. The cheap verifier computes the proxy
score S of Section 7 for each of the 64 sequence–refold pairs, and we select the highest-scoring pair, which
determines the winning backbone and sequence. The midpoint state of the winning backbone seeds the
exploit candidates of the next round, and the winning sequence is kept for the offline AlphaFold 3 evaluation.
Algorithm 3 summarizes this feedback procedure.

Algorithm 3 Protein feedback and offline evaluation
Require: Motif task m, generator G, rounds T = 30, backbones per round B = 8, sequences per backbone
    Q=8
Ensure: Winners {(x⋆t , qt⋆ , St⋆ )}Tt=1 and oracle labels {Yt }Tt=1
 1: for t = 1, . . . , T do
 2:   if t = 1 then
 3:      Sample B fresh backbone–midpoint pairs (xj , aj ) from G(m)
 4:   else
 5:      Sample B/2 backbones xj by independent continuations from a, setting aj = a
 6:      Sample the remaining B/2 backbone–midpoint pairs afresh from G(m)
 7:   end if
 8:   for j = 1, . . . , B do
 9:      Sample Q sequences qj,1 , . . . , qj,Q from ProteinMPNN conditioned on xj
10:      for k = 1, . . . , Q do
11:          Refold qj,k with ESMFold and compute its verifier score Sj,k
12:      end for
13:   end for
14:   Select (j ⋆ , k ⋆ ) ∈ arg maxj,k Sj,k
15:   (x⋆t , qt⋆ , St⋆ ) ← (xj ⋆ , qj ⋆ ,k⋆ , Sj ⋆ ,k⋆ )
16:   a ← aj ⋆
17: end for
18: for t = 1, . . . , T do
19:   Run AlphaFold 3 on qt⋆ and compute Yt against motif m and backbone x⋆t
20: end for



Model hyperparameters.
• RFdiffusion configuration. We use RFdiffusion [Watson et al., 2023].
   – Code. We use the official RFdiffusion GitHub repository.
   – Checkpoint. Base_ckpt.pt.
   – Reverse process. diffuser.T=50 and inference.final_step=1. We retain the step-25 state for
     subsequent exploit samples.
   – Translations. diffuser.schedule_type=linear, diffuser.b_0=0.01, diffuser.b_T=0.07, and
     diffuser.crd_scale=0.25.
   – Rotations. diffuser.so3_type=igso3, diffuser.so3_schedule_type=linear,
     diffuser.min_b=1.5, diffuser.max_b=2.5, diffuser.min_sigma=0.02, and
     diffuser.max_sigma=1.5.
   – Conditioning. inference.model_runner=SelfConditioning, inference.align_motif=True,
     inference.recenter=True, and preprocess.motif_sidechain_input=True.

• Proteina configuration. We use Proteina [Geffner et al., 2025].
   – Code. We use the official Proteina GitHub repository.


                                                     28
   – Checkpoint. ckpt_name=proteina_v1.7_DFS_60M_notri_motif_scaffolding.ckpt.
   – Integration. dt=0.0025, schedule.schedule_mode=log and schedule.schedule_p=2.0.
   – Stochastic term. sampling_caflow.sampling_mode=sc, sampling_caflow.sc_scale_noise=0.4,
     sampling_caflow.sc_scale_score=1.0, sampling_caflow.gt_mode=1/t,
     sampling_caflow.gt_p=1.0, and sampling_caflow.gt_clamp_val=null.
   – Conditioning. self_cond=False, fold_cond=False, guidance_weight=1.0, and
     autoguidance_ckpt_path=null.
   – Feedback state. We retain the Cα flow state nearest t = 0.5 for subsequent exploit samples.

RMSD computations. Each RMSD is computed after a separate least-squares rigid alignment using
Biopython’s Superimposer [Cock et al., 2009]. Backbone RMSD compares all Cα atoms of the generated
backbone and the ESMFold refold. Motif RMSD compares the prescribed motif’s N, Cα, and C atoms with
the corresponding atoms in the refold. Scaffold RMSD excludes motif residues for Proteina but includes the
entire generated chain for RFdiffusion, where it equals backbone RMSD.
For the ground-truth label, we run AlphaFold 3 [Abramson et al., 2024] on the winning sequence of each
round after all trajectories have been generated. Using the recorded motif positions and scaffold mask, a
proposal is successful if its top-ranked prediction has motif N–Cα–C RMSD at most 0.75 Å, scaffold-mask
Cα RMSD at most 1.5 Å, pTM at least 0.80, and mean pLDDT at least 85.

Roundwise likelihood-ratio estimation. At round t, we use the feature Xi,t = (Si,t−1 , Si,t ) ∈ R2 , with
Si,0 = 0. We fit a separate estimator for each generator, deployment fold, split seed, and round. Let At
and Nt index evidence trajectories with AlphaFold 3 labels one and zero, respectively. We standardize each
feature coordinate using only the observations indexed by At .
On the standardized features, we use the Gaussian kernel

                                                  ∥x − x′ ∥22
                                                             
                                       ′
                               Kh (x, x ) = exp −               ,                   h = 1.
                                                     2h2

For every coordinate a in the augmented null pool N    et , the alternative and leave-one-out null density estimates
are
                          1 X                                                 1      X
         pb1,t (Xa,t ) =            Kh (Xa,t , Xi,t ), pb0,t,−a (Xa,t ) =                  Kh (Xa,t , Xj,t ).
                         |At |                                            |N
                                                                           et | − 1
                               i∈At                                                  e    j∈Nt \{a}

We define
                                                                        pb1,t (Xa,t ) + 10−6
                                                                                               
                              L
                              b t,−a (Xa,t ) = clip[10−3 ,103 ]
                                                                      pb0,t,−a (Xa,t ) + 10−6
and apply the index-betting normalization in Equation 10. If either evidence class is empty, we set Et = 1.
This case did not occur in the reported evaluation.
We use the 100 calibration trajectories to select the online e-BH scale through robust-core CRC. The held-out
labels are used only to evaluate stopped FDP.
We evaluate α ∈ {0.05, 0.10, 0.15, 0.20} and κ ∈ {1, 5, 10} using the scale grid

                                      Λ = 1.5j j ∈ {0, . . . , 7} ∪ {20}.
                                          




                                                            29
