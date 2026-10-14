                                        Conformal Language Modeling via Posterior Sampling


                                            Nicolas Emmenegger∗ Theo X. Olausson∗ Armando Solar-Lezama                        Chara Podimata
                                                                   Massachusetts Institute of Technology
                                                               {nemm,theoxo,asolar,podimata}@mit.edu



                                                                                        Abstract
arXiv:2606.03731v1 [cs.LG] 2 Jun 2026




                                                    Large Language Models remain plagued by hallucinations. Recent work has sought
                                                    to tame their prevalence using statistical techniques based on conformal prediction,
                                                    with both theoretical and empirical success. However, these methods operate
                                                    in a post-hoc fashion, treating the sampling procedure itself as atomic and then
                                                    surgically altering samples to remove hallucinated claims. This disconnect between
                                                    filtering and generation can result in samples that are incoherent, inconsistent, or
                                                    simply unlikely under the model itself. Moreover, post-hoc surgery is unable to
                                                    shift probability mass towards more useful and helpful responses. To address these
                                                    issues, we propose to instead sample from approximations to an LLM posterior,
                                                    where the conditioning event corresponds to a calibrated, high-scoring region. We
                                                    develop a calibration procedure tailored to the setting of conditional sequential
                                                    generation that effectively identifies this region and achieves target risk control.
                                                    Empirically, we apply our method to case studies focused on open-ended biography
                                                    generation and mathematical problem solving; compared to prior work, we obtain
                                                    the same statistical guarantees, with higher downstream utility.


                                        1     Introduction
                                        Large Language Models (LLMs) are increasingly deployed in high-stakes settings ranging from
                                        medical diagnosis [Gaber et al., 2025] to legal research and case analysis [Dehghani et al., 2025].
                                        Yet even the most sophisticated models available today still routinely hallucinate false claims [Fan
                                        et al., 2026]. This has motivated a growing body of work on quantifying and reducing hallucinations,
                                        including methods that train LLMs to predict their own confidence [Damani et al., 2026], methods
                                        that produce calibrated predictions of factuality [Detommaso et al., 2024], or methods that generate
                                        sets of outputs containing a factual response with high probability [Quach et al., 2024].
                                        One particularly promising recent direction has been to leverage conformal prediction [Mohri and
                                        Hashimoto, 2024, Cherian et al., 2024, Rubin-Toles et al., 2025], a statistical wrapper yielding
                                        assumption-lean guarantees. This line of work seeks to control the expected value of a loss function
                                        ℓ : X × Y → R≥0 , such as a measure of an output y’s factuality with respect to a prompt x. To
                                        control this quantity, conformal methods split the output into distinct claims, and leverage a heuristic
                                        score function, which serves as an (imperfect) proxy of the loss. By observing the relationship
                                        between the scores and the true losses on a held-out calibration set, these methods then calibrate
                                        a post-hoc filtering mechanism that provably controls the risk. Formally, given a calibration set
                                        Dcal = {(xi , yi , s i , ℓi )}ni=1 of n samples from the LM alongside their claim-level scores sij and
                                        observed losses ℓi = ℓ(xi , yi ), they construct a mapping F that filters out low-confidence claims
                                        so that the resulting F (ytest ) satisfies E[ℓ(xtest , F (ytest )] ≤ α, for some user-defined risk tolerance
                                        α ∈ (0, 1).
                                        While post-hoc surgical altering of outputs makes sense in situations where the user is satisfied with a
                                        partially filtered generation, it may lead to samples that have low downstream utility in tasks where
                                            ∗ Equal contribution.




                                        Preprint.
claims have strong interdependencies. In other words, while post-hoc filtering guarantees a bound
on the expected number of responses containing a false claim, it often renders many of the model’s
responses incomplete or simply unhelpful to the user.
To produce samples that are fluent, coherent and satisfying to the user, such methods therefore
typically repair the filtered output using either a language model [Mohri and Hashimoto, 2024], thus
reintroducing the risk of fabricating claims, or change the filtering mechanism symbolically through
complicated dependency-graph schemes [Rubin-Toles et al., 2025]. However, even with some degree
of fluency restored, these methods cannot recover from (over-)agressively filtered responses.
Against this backdrop, in this paper, we ask: Can we design a risk-controlling calibration routine
that respects the underlying generative process and moves probability mass towards useful responses
whenever the model has the capacity to solve the task at hand?
We answer this question affirmatively by shifting the target of calibration from a post-hoc filter to the
sampling distribution itself. Our key idea is that risk control should reweight the LM’s distribution
towards completions that are more reliable and more useful, rather than altering the completions in
a post-hoc manner. We reframe conformal language modeling as posterior sampling from the LM,
conditioned on an event that corresponds to the response falling within a high-confidence region of
the output space. That is, instead of calibrating a post-hoc filtering mechanism, we directly calibrate
a sampling distribution Q(·|xtest , Dcal ) such that
                          EDcal ,xtest ,ytest ∼Q(·|xtest ,Dcal ) [ℓ(xtest , ytest )] ≤ α.            (1)

1.1   Roadmap and Contributions

Modeling. In Sec. 2, we formulate conformal LM factuality control as posterior sampling from a
calibrated family, indexed by a one-dimensional parameter τ . We define a family of potentials which
threshold completions by their cumulative claim-level factuality scores. This amounts to conditioning
the LM distribution on high-confidence regions. While, as we show, this is cleanly motivated by
a probabilistic formulation, our method’s safety guarantees will be agnostic to the choice of score
function.
Calibration. In Sec. 3, we develop an off-policy calibration procedure for selecting the posterior
threshold τ , without requiring samples from each candidate posterior. We face two major challenges:
firstly, the posterior’s conditional normalizing constant Z τ (x) now needs to be estimated from
samples, which is ill-conditioned (or even ill-defined) when the model has low (or no) mass on the
high-confidence region. Secondly, estimating a plug-in of the importance reweighted loss naively
yields a non-monotone objective, making conformal guarantees hard to obtain. We solve the former
issue by modeling the calibration objective as an empirical distribution posterior that is extended
by an explicit abstention path, effectively modeling the prior as a mixture distribution. We solve
the second issue by explicitly monotonizing the objective, and show experimentally that this has a
negligible impact on conservativeness. Finally, we connect the empirical posterior distribution to the
true population posterior. Using a Glivenko-Cantelli argument, we show that the empirical posterior
risk converges to the population posterior risk as the number of calibration samples grows.
Experiments. In Sec. 4, we evaluate our method on two case studies: open-ended biography
generation [Min et al., 2023] and math reasoning [Hendrycks et al., 2021]. Our method tracks
the desired factuality level while significantly improving downstream utility relative to a post-hoc
conformal filtering baseline, especially in settings with strong claim interdependencies.

2     Preliminaries and Modeling
2.1   The Posterior Family

We model an LLM with vocabulary V and prompt x as a distribution pLLM (y | x) ∈ ∆(V ∗ ) over
completions, where V ∗ is the Kleene closure of V (up to some max length L, omitted for brevity).
We call pLLM the LM prior and extend it with a potential function Φ(y | x) to obtain a posterior
                                 pΦ
                                  LLM (y | x) ∝ pLLM (y | x)Φ(y | x).                                (2)
Our goal is to pick Φ so that substituting pΦ
                                            LLM (·|x) for Q(·|x) in Equation (1) controls risk at the
target level. To do so, we make Φ(·|x) depend on a heuristic notion of how “risky” y is, and control the


                                                        2
                                                                                                     τ
perceived risk by setting a one-dimensional parameter τ , yielding a posterior pΦ            τ
                                                                                LLM (·|x) = pLLM (·|x)
                                            τ
defined via the parametrized potentials   Φ . The RHS of Equation (2) implicitly depends on the
normalization constant Z τ (x) = y∈V ∗ Φτ (y|x) dpLLM (y|x), which — as we will see below —
                                    R

corresponds to the probability mass that survives the threshold τ for prompt x. We next turn to the
question of how to instantiate Φτ for a given τ .

2.2    From Heuristic Scores to Potentials

To build a family of potential functions that allow us to control the risk, we draw inspiration from
prior work on conformal prediction and leverage a heuristic scoring function. We design this scoring
function so that it gives an estimated confidence for y’s most recent claim ci being correct conditional
on the prompt x and all preceding claims c <i = (c1 , . . . , ci−1 ) being assumed to be correct.2
Formally, that is, the scoring function is of the form s : V ∗ × V ∗ × (V ∗ )∗ → S, where S ⊂ R is
chosen to be (0, 1] w.l.o.g. Using c<i to denote the prior claims whenever clear from context, we will
abuse probabilistic conditioning notation and write s(ci , x, (c1 , . . . , ci−1 )) as
                                   si := s(ci | x, c<i ) := s(ci | x, c1 , . . . , ci−1 ).
Intuitively, the “oracle” score
                           s(ci | x, c <i ) = 1 {ci is factual given c <i and prompt x}

   Q immediately give us an α = 0 level risk-controlling potential by letting Φ(y | x) =
would
1 { i si = 1}, ensuring that all samples from pΦ   LLM contain only true claims. In practice, such
an oracle cannot be obtained. The purpose of this paper is to show that with a heuristic choice of s,
we can, however, still control the risk by appropriately picking a threshold τ such that
                                             (K                       )
                                               Y
                              Φτ (y | x) = 1       s(ci | x, c<i ) ≥ τ ,                         (3)
                                                           i=1

where
Q      K is the (random) number of claims in the output. We will sometimes write S(y | x) =
  i∈[K] s(ci | x, c <i ) to denote completion-level scores. We build intuition for this definition by
recalling the chain rule of probabilities. Assume that we are in an idealized scenario where the
scores si act as correctness forecasts satisfying a weaker-than-oracle (but still unrealistic) notion of
conditional calibration. Informally, assume (see also a detailed derivation in Appendix A)that
                        P[c i is factual | s ≤i ; previous claims c <i are all factual] = si .                                (4)

That is, the score is a calibrated forecast of the correctness of the present claim given that all preceding
claims were factual. Under this assumption and additional technicalities outlined in Appendix A,
where the statement can be found in full detail, one can show the following observation.
Observation 1 (Idealized validity; informal). Under an idealized, stepwise-calibrated3 scoring
function s(·), sampling y ∼ p1−α LLM (· | x) induced by Φ
                                                           1−α
                                                                (y | x) satisfies E[ℓ(x, y)] ≤ α.

Intuitively, if the scores were stepwise-calibrated forecasts of conditional
                                                                 Q            correctness given the
preceding prefix, a martingale argument (Appendix A) would yield i≤K si = P(y correct | x, s ≤K ).
The product of scores then acts as a sequential probability-of-correctness estimate, and the choice
τ = 1 − α directly (conservatively) controls risk at level α.
In practice, heuristic scores are far from calibrated in this sense, and it is generally impossible to
achieve calibrated forecasts that are this strong [Van Calster et al., 2016, Hébert-Johnson et al., 2018].
We must therefore choose τ from data via a procedure that makes essentially no assumptions on the
scorer; this is the main theoretical subject of this paper, which we return to in Section 3.

2.3    Calibrated Posterior Sampling on a Mixture Prior

Before we turn to the question of calibrating the threshold τ , we note that our discussion so far relies
on the assumption that the posterior is well-defined for all x and τ .
   2 In this paper, we will routinely use the notation u
                                                         ≤i and u <i to denote prefix vectors of sequences (ui )i .
   3 By “stepwise-calibrated”, we mean that each claim-level score is calibrated as a forecast of the current claim’s correctness,

conditional on the prompt, the previous scores, and the event that all strictly earlier claims were correct.


                                                                 3
                                          τ
                                               (x) = y∈V ∗ Φτ (y | x) dpLLM (y | x) > 0 for all x ∈ X
                                                      R
Formally, this amounts to requiring ZLLM
and τ ∈ [0, 1]. Since this would require the ability to generate samples that pass the potential’s
thresholding mechanism by mapping to thresholds that are arbitrarily close to 1, this is too stringent
of an assumption on the scoring mechanism. Post-hoc methods such as that of Mohri and Hashimoto
[2024] sidestep this issue by treating an all-claims-dropped generation (i.e., outputting the empty set
of claims) as an implicit abstention that is always factual. In our setting, pτLLM inherits its support
from pLLM , which may not include an explicit abstention path. The language model prior pLLM may
have no practical amounts of mass on any score-passing outputs at all; strict thresholds thus leave no
direct route to safe output, prohibiting calibration. To get around this issue, we therefore calibrate not
against pLLM itself but against the mixture prior
                                pβ (y | x) = (1 − β) pLLM (y | x) + β δabstain (y),                   (5)
where δabstain is a point mass on a designated abstention response, β > 0 is a small pre-specified mass,
and we require that the scorer assigns S(abstain | x) = 1 for all x ∈ X . The resulting posterior then
retains a factual escape valve at cutoff τ ; abstaining is always factual. Analogously to (2), we define
the mixture posterior pτβ (y | x) ∝ pβ (y | x)Φτ (y | x). Conveniently for what follows, this also makes
the conditional normalizing constant well behaved, i.e., Zβτ (x) = y∈V ∗ Φτ (y | x) dpβ (y | x) ≥ β for
                                                                     R

all τ . We often drop the subscript β and just write p := pβ and pτ = pτβ , and similarly Z τ = Zβτ .
Note that p0 = p0β = pβ is simply the prior, since thresholding has no effect at τ = 0 when S ⊆ [0, 1].

2.4    Instantiating the Scoring Function

While the validity of our method is agnostic to the accuracy of the scorer, yielding risk-controlling
guarantees under very minimal assumptions, the scorer does have an impact on how stringently the
system filters out generations (see Appendix D.3 for a scorer ablation). We follow prior work and
elicit scores by asking an external LLM to rate its confidence in each claim on a scale from 0 to
1 [Mohri and Hashimoto, 2024]. Empirically, this does not yield continuously-distributed scores,
instead concentrating on a small, discrete set. Following Mohri and Hashimoto [2024], in order to
calibrate to arbitrary targets of factuality 1 − α, we therefore add a small random perturbation. For an
elicited score s̃i , we set the final score as si ∼ U [max(0, s̃i − γ), min(1, s̃i + γ)], where γ = 0.01
is a small constant, the exact choice of which has no significant downstream effects, so long as it is
on the order of the granularity of the elicited scores4 .
While having flexibility on the choice of scorer is convenient, it also presents a methodological chal-
lenge. Since pτ (· | x) depends on both s and τ , calibration via fixed-sequence testing [Angelopoulos
et al., 2025] would require specifying a sensible grid of thresholds τ to consider in advance, and
drawing a new calibration set for each (s, τ ) pair — a prohibitively expensive process that would
require to be repeated whenever s is modified. Even setting computational burden aside, how to pick
such a grid is not clear a priori, especially because the spread of the scores is unknown and could be
concentrated within some small range, making it difficult to select a sensible discretization a-priori.
Instead, we will aim to develop an off-policy calibration routine which only requires samples from
the (mixture) prior, eliminating the need for expensive on-policy data collection altogether.

3     Methodology: Calibrating the Threshold τ
Having defined the potential family Φτ and the mixture prior p, we turn to the central question of
the paper: how to pick τ so that posterior sampling controls risk at level α, using only samples
from the base model. We will have access to a calibration set of prompts C = {x1 , . . . , xn } from
PX , and assume that x1 , . . . , xn , xtest are exchangeable. We present our approach in 3 steps: (1)
derivation of an idealized calibration rule under known normalization constant; (2) construction of a
tractable empirical approximation; and (3) proof that this yields risk control for the resulting posterior
sampler(s).
Known Normalization Constant.R Assume that we have access to an oracle for the conditional
normalization constant Z τ (x) = y∈V ∗ Φτ (y | x) dp(y | x). If that was the case, then we could
estimate the posterior risk using importance reweighting. To see this, note first that from Section 2.1:
    4 LLM scorers tend to return scores that are capped at one or two decimal points.




                                                              4
pτ (y | x)      τ
                   | x)
 p(y | x) = ΦZ(y                                                                  τ
               τ (x) . So, instead of sampling directly from the posterior p , we can i.i.d. sample

outputs yi from the mixture prior p(· | xi ), keep only samples whose score exceeds τ , and then
re-weigh their losses to account for the fact that they were sampled from the prior rather than the
posterior. To obtain a finite-sample guarantee, we add a conservative correction term 1/(β(n + 1)) for
the unseen test point and conservatively monotonize the objective by lower bounding the likelihood
ratio’s denominator. This gives an idealized calibration rule:
                                        n
                                  1 X Φτ (yi | xi )
                                                                                       
                                                                             1
                τ̂id = inf τ                                  ℓ(x ,
                                                                 i iy ) +           ≤ α   .        (6)
                                n + 1 i=1 Z S(yi | xi ) (xi )             β(n + 1)
We briefly comment on this calibration rule. Note that since τ 7→ Z τ (xi ) is a monotone non-
increasing5 map and by the thresholding nature of Φτ , each term in the sum is an upper bound on
Φτ (yi |xi )
  Z τ (xi ) ℓ(xi , yi ). Fixing the denominator to not depend on τ has an additional crucial property: the
ratio is now monotone in τ . Therefore, the LHS of the constraint in (6) inherits this monotonicity,
yielding our first risk control guarantee.
Proposition 3.1. If x1 , . . . , xn , xtest are exchangeable, samples from PX and we have access to
Z τ (xi ) for all τ ∈ [0, 1], then computing τ̂id according to Equation (6) and sampling the test point
from the true posterior ytest ∼ pτ̂id (· | xtest ) satisfies E[ℓ(xtest , ytest )] ≤ α, where the randomness is
over the draw of the calibration prompts, the calibration responses, and the draw from the test-time
posterior.
The proof is deferred to Appendix B.1.
Unknown Z τ (x). In practice, computing Z τ (x) is intractable6 , and the rule (6) cannot be
evaluated. A natural idea is to estimate, at each calibration prompt, the conditional posterior
risk Ey∼pτ (· | xi ) [ℓ(xi , y)] from base-model samples. To this end, we draw M i.i.d. responses
yij ∼ pLLM (· | xi ) (aka “particles”) for each i ∈ [n] and form the empirical (mixture) prior
                                                     1 X
                          p̂(y | xi , Ti ) = (1 − β)     δyij (y) + β δabstain (y),            (7)
                                                     M
                                                             j∈[M ]

where we use the shorthand Ti = (yi1 , . . . , yiM ) and the abstention atom is attached analytically
with mass β rather than sampled. This stratification matches the abstention weight to that of the
population mixture prior pβ but, crucially, ensures that there is deterministic abstention mass, making
the plug-in estimator well-defined. The induced empirical posterior is
                       Φτ (y | xi ) p̂(y | xi , Ti )                                 1 X τ
  p̂τ (y | xi , Ti ) =                               , Ẑ τ (xi , Ti ) = β + (1 − β)    Φ (yij | xi ). (8)
                             Ẑ τ (xi , Ti )                                         M
                                                                                                j∈[M ]
                                                τ                                      τ
The explicit abstention path implies Ẑ (xi , Ti ) ≥ β which makes p̂ well-defined for all τ ∈ [0, 1].
Calibrating against the empirical posterior. The definition of p̂ signifies that we are essentially
stratifying the sampling from both modes of the mixture prior. This will naturally lead to a calibration
routine that does not control the risk under the population posterior pτ , but instead under the
empirical posterior p̂τ . To this end, given Ti , we consider the conditional risk under p̂τ , namely
Ey∼p̂τ (· | xi ,Ti ) [ℓ(xi , y)], and write the shorthand
                                                   1             τ
                                                      P
                                           (1 − β) M    j∈[M ] Φ (yij | xi ) ℓ(xi , yij )
                                Ĥi (τ ) =                1
                                                            P           τ
                                                                                          ,           (9)
                                              β + (1 − β) M     j∈[M ] Φ (yij | xi )

because the abstention atom contributes ℓ(x, abstain) = 0 to the numerator and can be omitted.
Ĥi (τ ) is a deterministic function of the calibration data alone, with no further randomness over a
sampler: calibration simply inspects the support of p̂τ , it does not draw from the corresponding
empirical distribution.
As a step function of τ 7 , Ĥi need not be monotone: pruning a correct particle at a slightly higher
threshold while leaving incorrect particles to survive can transiently raise the average loss among the
   5 This is because as τ increases, the probability mass of completions that pass τ can only decrease.
   6 Indeed, computing it requires summing/integrating over all possible completions y that the LM could generate.
   7 To see this, note that the only way that τ affects Ĥ (τ ) is through the score indicators Φτ (y |x ) = 1 {S(y |x ) ≥ τ }.
                                                          i                                          ij i          ij i
As such, Ĥi (τ ) only changes when τ crosses one of the sampled scores S(yij |xi ).


                                                              5
Algorithm 1 Off-policy Conformal Risk Control with Path Monotonization
Require: Calibration prompts x1 , . . . , xn ; particle budget M ; abstention mass β; target level α
 1: for i = 1, . . . , n do
 2:     for j = 1, . . . , M do
 3:         Sample yij ∼ pLLM (· | xi ), score it to obtain Φτ (yij | xi ), and annotate ℓ(xi , yij )
 4:     end for
 5: end for
 6: Form Ĥi (τ ) via((9) and H̄i (τ ) via (10)            )
                                   n
                              1 X                 1
 7: return τ̂ = inf τ                 H̄i (τ ) +       ≤α .
                            n + 1 i=1            n+1


accepted particles. We restore monotonicity sample-pathwise via the monotone upper envelope:
                                          H̄i (τ ) = sup Ĥi (τ ′ ),                                    (10)
                                                     τ ′ ≥τ

a non-increasing pointwise upper bound on Ĥi . Monotonization is the lever that makes conformal-
risk-control style arguments work. Empirically (see Sec. 4), Ĥi is close to monotone for moderate
M , and H̄i introduces little slack.
The full procedure is given in Algorithm 1. We can give the following conformal guarantee, which
approaches a guarantee on a sample from the population posterior as M grows (c.f. Corollary 3.4).
Theorem 3.2 (Finite-sample risk control for the empirical posterior). Let prompts x1 , . . . , xn , xtest
be exchangeable, and assume that conditionally, all calibration and test particles are drawn indepen-
dently with yij ∼ pLLM (·|xi ) and (ytest )j ∼ pLLM (·|xtest ). Let τ̂ be the output of Algorithm 1. If
ytest ∼ p̂τ̂ (·|xtest , Ttest ), then E[ℓ(xtest , ytest )] ≤ α, where the expectation is over the calibration
prompts and particles, test prompt and particles, and the draw from the test-time posterior.
Given base-model samples, per-claim scores, and factuality annotations on the calibration set,
Algorithm 1 returns a threshold τ̂ which controls the risk of the empirical-posterior sampler. The
proof (in Sec. B.2), follows a standard conformal-risk-control template: H̄i is a monotone envelope of
a plug-in estimator for the empirical-posterior risk, exchangeability of the calibration tuples bounds
an “oracle” threshold τ ⋆ at level α, and monotonicity transfers this bound from τ ⋆ to τ̂ .
From empirical to population posterior. Calibrating against p̂τ̂ raises a natural question: does
the guarantee transfer to the population posterior pτ̂ ? Because τ̂ is data-dependent, pointwise
convergence at fixed τ is not enough; we need the convergence to be uniform in τ . Luckily, the
threshold-indexed family {Φτ (· | x) : τ ∈ [0, 1]} is a one-dimensional threshold class and hence
Glivenko-Cantelli, giving us the following result.
Lemma 3.3 (Uniform asymptotic equivalence of conditional risks). Fix abstention mass β > 0, and
                                    i.i.d.
let TM = (y1 , . . . , yM ) with yj ∼ pLLM (· | x). Then for PX -a.e. x,
                                                                                 a.s.
                       sup Êy∼p̂τ (· | x,TM ) [ℓ(x, y)] − Ey∼pτ (· | x) [ℓ(x, y)] → 0.
                     τ ∈[0,1]

Note that this is an almost surely statement about the draw of the calibration particles TM , as M → ∞,
uniformly over all τ ∈ [0, 1]. Combined with Theorem 3.2, this gives us the following corollary.
Corollary 3.4. As the number of calibration particles grows, for ytest ∼ pτ̂M (· | xtest ) we have
lim supM →∞ E[ℓ(xtest , ytest )] ≤ α.
In other words, the calibration guarantee transfers asymptotically to any deployment sampler that
targets the population posterior. This means that we achieved the goal we set out to, modulo error
that shrinks as M grows. We also point out that we need not necessarily enter the asymptotic regime
for the finite-particle, stratified way of constructing the empirical posterior to make sense. Different
ways to sample from the posterior are possible that still exactly or approximately inherit the finite
sample guarantee in Theorem 3.2. For instance, Sequential Monte Carlo steering [Lew et al., 2023,
Zhao et al., 2024, Loula et al., 2025] fixes the initial number of particles, in which case our method
amounts to extending the proposal distribution with an appropriately weighted abstention particle;
see Sections 5 and 6 for further discussion on efficient sampling and particle filtering methods.


                                                      6
4     Experiments

We now empirically evaluate our framework’s validity (that is, whether it controls the level of risk at
test-time) and utility (whether the resulting generations are useful). We focus on two distinct case
studies: one within the hallucination-prone task of open-ended biography generation, and one within
mathematical reasoning where inter-claim dependencies are stronger.
Datasets and models. For the biography generation, we use 682 entities from the FActScore dataset
[Min et al., 2023]; for mathematical reasoning, we use the standard test set of 500 problem instances
from MATH [Hendrycks et al., 2021]. We average over 10 random splits of the data, with 50 instances
used as the test set and the remaining used for calibration; results are reported as the mean over the
splits, with shaded areas showing approximate 95% CIs using the studentized Wald interval. For
generation we use Llama-3.3-70B-Instruct8 [Grattafiori et al., 2024], a model with intermediate
capacity on these tasks. We serve the model on a single NVIDIA RTX A6000 with 48GB of VRAM,
taking ∼30s per prompt to generate answers. To elicit scores, we use OpenAI’s GPT-4o, a larger
and more capable (but still unreliable) estimator of truth; App. D.3 compares against a raw token
log-probability scorer and the cheaper GPT-4o-mini. Finally, to ensure that the per-claim labels are
as accurate as possible, we label the data using GPT-5.4; for FActScore, we include a copy of the
entity’s Wikipedia article in the prompt.
Base generations and mixture prior setup. We sample 20 base generations from pLLM for each
instance, using a moderate temperature of 0.8 (prompts in Appendix E.1). We fix β = 0.1 for both
datasets and report plug-in estimates of the metrics using the empirical posterior over each instance’s
20 generations. For example, to compute the empirical risk over a test set Dtest = {xi }N          i=1 , we
average (9) over the test instances xi . We note that for a fixed and finite number of calibration samples
M , at very small values of β, the asymptotic guarantees of Corollary 3.4 may not translate to the
population posterior pτ ; for a thorough investigation, see Appendix D.4.
Baseline. We compare against Mohri and Hashimoto [2024], the closest prior work. We re-implement
Mohri and Hashimoto [2024]’s algorithm so that it does not require the use of a separate model to
decompose generations into atomic claims; instead, we encourage the generator to keep clauses brief
and split on sentences. We do so to illustrate a tight integration of each method into the generation
loop without any reliance on additional restructuring steps, and to enable a direct comparison to our
method. For brevity, we refer to this baseline as MH.

4.1    Validity                                                                                        1.0   ours
                                                                                                             MH
                                                                                                             y=x
                                                                                                       0.8
                                                                                empirical factuality




Figure 1 shows the empirical risk obtained versus the desired
target 1 − α on FActScore (results on MATH in App. D.1).               0.6
As expected from Theorem 3.2, our method achieves valid                0.4
coverage at all levels. Coverage is also empirically tight; mono-
tonization of the objective does not introduce excessive slack.        0.2
Note that low targets (≈ 0.4 for FActScore, ≈ 0.5 for MATH)            0.0
                                                                              0.4       0.6          0.8
fall below the base model’s capacity, so both methods reduce                       target factuality
to sampling directly from the prior and therefore flatline. The
remaining gap between the two is due to β. As our method Figure 1. Empirical vs. target factual-
samples from the mixture prior p̂ instead of pLLM , it is slightly ity on FActScore; ours ( ) and MH ( ).
                                                                   Both attain valid coverage.
more conservative at targets below the model’s base capacity.

4.2    Utility

We use LLM-judge scoring as our primary measure of the downstream utility of the samples we
obtain. For FActScore we construct a Likert-style questionnaire along three axes (completeness,
fluency, and helpfulness; rubric in Appendix E.4.1) and ask GPT-5.4 to rate its level of agreement
between 1-5 for each. Abstentions are passed to the judge as a pre-formatted response of the form
“I don’t know who or what {entity} is.“ For MATH, we simply ask GPT-5.4 whether the proof is
complete, that is, whether it leads to a final answer and that final answer matches the reference

    8 To reduce cost, we use the (4-bit weights, 16-bit activations)-quantized variant provided by RedHatAI on HuggingFace.




                                                             7
                    5                                                                  5
                                                            ours                                                           ours                           1.0                                   ours                       1.0   ours
                                                            MH                                                             MH                                                                   MH                               MH
                    4                                                                  4                                                                  0.8                                                              0.8



mean Likert score




                                                                   mean Likert score




                                                                                                                                      completeness rate




                                                                                                                                                                                                       completeness rate
                                                                                                                                                          0.6                                                              0.6
                    3                                                                  3
                                                                                                                                                          0.4                                                              0.4
                    2                                                                  2
                                                                                                                                                          0.2                                                              0.2

                    1                                                                  1                                                                  0.0                                                              0.0
                            0.4        0.6            0.8                                  0.4        0.6            0.8                                        0.4        0.6            0.8                                     0.4        0.6            0.8
                                  target factuality                                              target factuality                                                    target factuality                                                 target factuality

                        (a) FActScore Likert.                                          (b) Likert | non-abstain.                                          (c) MATH completeness.                                (d) Complete | non-abstain.
Figure 2. LLM-judge utility for ours ( ) vs. MH ( ) as target factuality varies. Unconditional panels (a, c)
include abstentions (judged on FActScore, marked incomplete for MATH); conditional panels (b, d) show results
for both methods conditioned on the output not being an abstention.

(prompt in Appendix E.4.2). Abstentions are naturally scored as incomplete. To reduce annotation
cost, we subsample a single generation9 for each prompt xi for this experiment.
In addition to these metrics, we also compute a series of proxy metrics on all the outputs yij : (i-ii) the
average number of claims per output, both with abstentions counting as zero claims and conditioned
on non-abstention; (iii) the total fraction of emitted claims that are true, aggregated over all prompts;
and (iv) the fraction of non-abstaining outputs that are entirely factual, with no false claims at all.
Downstream results. Figure 2 reports the FActScore Likert and MATH completeness scores, both
unconditionally (with abstentions scored as described above) and conditioned on obtaining a non-
abstaining sample. FActScore: Non-abstaining generations from our method degrade less sharply than
those from MH as the target factuality increases; the per-axis breakdown in Figure 5 (Appendix D.2)
reveals that this is predominantly driven by less degradation in completeness and helpfulness, rather
than fluency. In the unconditional average, which conflates response quality with response frequency,
our method underperforms MH. This indicates that the LM judge prefers a highly edited response
to refusals in this setting; how such a refusal should be valued relative to a riskier-but-partially-
informative answer ultimately depends on the context in which the system is deployed, and this
may not reflect the preference of actual users. MATH: With a more objective notion of utility, the
gains from our method become clearer: while the mixture prior initially increases the probability of
sampling an abstaining (and thus incomplete) response, MH begins to generate incomplete answers at
very high rates for targets ≥ 0.6. Our method not only degrades less, but in the instances where it
does not abstain, the rate of completeness even increases with the target factuality. These findings
thus suggest that our method produces useful generations even at high target levels of factuality.
Proxy results. Figure 3 shows the claim-level proxy metrics, with FActScore on the top row and
MATH on the bottom. First column: At intermediate targets, our method emits roughly as many
claims per instance as MH. The mixture prior places β of the mass on zero-claim abstentions, deflating
our method’s average at low targets; this reverses at high targets, where MH increasingly produces
heavily filtered generations. Second column: Restricting our attention to non-abstaining responses,
our method emits substantially more claims on both datasets. Intuitively, MH distributes rejected
claims evenly across instances, while our method concentrates filtering on hard instances and leaves
easier prompts with full-length generations. Third column: The fraction of emitted claims which are
correct is similar for both methods, increasing (as expected) with the target level. Fourth column:
The one axis on which our method may lose ground is the fraction of non-abstaining outputs that
are entirely factual. On FActScore in particular, we observe a slight decrease in the chance that
conditioned on not being an abstention, any given sample is completely factual. Ultimately, whether
non-abstaining, hallucination-free responses can be obtained is controlled by the capacity of the
underlying pLLM : posterior sampling can only shift the mass of the samples towards safer regions if
such regions of support exist.
Summary. While both our method and MH control similar objectives, the resulting downstream utility
differs significantly. As the target level of risk control increases, our method produces more helpful
and complete outputs (as judged by an external LM). However, since our sampler cannot stray far
from the support of pLLM , instances poorly known to the LLM can only be pushed towards factuality
by abstaining, leading to a small uptick in the chance that any given non-abstaining answer has at
least one incorrect claim in settings where the model lacks the capacity to solve the task.


                        9 For our method, from the posterior. For MH, from the base model with subsequent filtering.




                                                                                                                                  8
         4.0                                       ours            4.0                                                                 1.0     ours                                                       1.0   ours
                                                   MH                                                                                          MH                                                               MH
         3.5




                                                                                                                                                                                hallucination-free rate
                                                                   3.5                                                                 0.8                                                                0.8




                                                                                                                     claim precision
         3.0
                                                                   3.0                                                                 0.6                                                                0.6
         2.5

claims




                                                          claims
         2.0                                                       2.5
                                                                                                                                       0.4                                                                0.4
         1.5                                                       2.0
         1.0                                                                                                                           0.2                                                                0.2
                                                                   1.5   ours
         0.5                                                             MH
                                                                                                                                       0.0                                                                0.0
                   0.4        0.6            0.8                          0.4        0.6            0.8                                         0.4        0.6            0.8                                    0.4        0.6            0.8
                         target factuality                                      target factuality                                                     target factuality                                                target factuality

              (a) Claims per output.                               (b) Claims | non-abstain.                                                 (c) Claim precision.                             (d) Hallucination-free rate.
                                                   ours                                                   ours                         1.0     ours                                                       1.0                                    ours
         12                                        MH              12                                     MH                                   MH                                                                                                MH




                                                                                                                                                                                hallucination-free rate
         10                                                                                                                            0.8                                                                0.8
                                                                   10




                                                                                                                     claim precision
          8                                                         8                                                                  0.6                                                                0.6
claims




                                                          claims
          6                                                         6                                                                  0.4                                                                0.4
          4
                                                                    4
          2                                                                                                                            0.2                                                                0.2
                                                                    2
          0                                                                                                                            0.0                                                                0.0
                  0.4         0.6            0.8                          0.4        0.6            0.8                                         0.4        0.6            0.8                                    0.4        0.6            0.8
                         target factuality                                      target factuality                                                     target factuality                                                target factuality

               (e) Claims per output.                              (f) Claims | non-abstain.                                                 (g) Claim precision.                             (h) Hallucination-free rate.
               Figure 3. Claim-level proxy metrics for ours ( ) vs. MH ( ) on FActScore (top) and MATH (bottom).


5               Related Work

Calibrated stopping rules. A complementary body of recent work calibrates stopping rules for
reasoning models and agents [Wu et al., 2025, Sadhuka et al., 2025, Zhou et al., 2026]. These methods
similarly avoid the limitations of post-hoc filtering (Section 1), but the target of calibration is different:
they calibrate decision rules over the reasoning process (when to stop thinking, or when to reject
an agent trajectory), whereas we calibrate a family of output distributions. On the methodological
side, these methods respectively build upon fixed sequence testing [Angelopoulos et al., 2025] and
E-values [Ramdas and Wang, 2025], and leverage on-policy samples; this is impractical in our setup,
where the distribution of scores can be arbitrarily bimodal and no natural grid is available in advance.
Both the goal and the approach presented in this work are thus orthogonal from such efforts.
Particle methods for semantic steering of language models. Our method is inspired by a line
of work that frames semantically constrained generation as posterior sampling [Lew et al., 2023,
Zhao et al., 2024, Loula et al., 2025]. Similarly to our setup, these works treat a language model as
a probabilistic prior and then build a suitably defined posterior distribution. However, their goal is
different than ours, predominantly being concerned with sampling efficiency. Meanwhile, we focus
on how to leverage unreliable potentials, a challenge which has not been explored by this literature.
Conformal prediction and risk control under distribution shift. Conformal methods [Saunders
et al., 1999, Angelopoulos et al., 2024a] have widely been adapted to work under known distribution
shift [Tibshirani et al., 2019, Angelopoulos et al., 2024b], tackling the issue via weighted exchange-
ability. While we draw inspiration from this approach, we face an additional complication: label
distribution shift that is itself directly affected by the calibration parameter. This prevents us from
applying methods based on vanilla variants of weighted exchangeability (c.f. App. C). We refer to the
works of Fannjiang et al. [2022] and Prinster et al. [2024] for a more thorough treatment of conformal
guarantees under more general (covariate) shifts.


6               Discussion: Limitations & Future Directions

The β parameter. This parameter governs the mixture prior between the LM completions and
the explicit abstention response. Its main role is to ensure that the posterior remains well-defined
by assigning fixed mass to an always-factual abstention atom, guaranteeing that the normalization
constant is bounded away from zero. As a result, β controls a utility-abstention tradeoff, but not
the validity of the procedure on the empirical posterior p̂τ̂ . Larger β values provide a stronger
fallback path, but shift more probability mass toward abstention and can reduce the informativeness
of non-abstaining outputs. Smaller β values preserve more mass on LM completions, improving
utility when the model is capable, but leave less fallback mass when high-confidence completions
are rare. Additionally, the choice of β and its relative scale compared to M has an effect on the
convergence rate of the empirical posterior p̂τ̂ to the population posterior pτ̂ (c.f. Corollary 3.4).


                                                                                                                 9
Measuring downstream utility. Our empirical evaluation measures downstream utility using LLM-
judge scoring, focusing on properties such as completeness, fluency, and mathematical coherence.
While this provides a scalable first validation, it is not a substitute for human evaluation. A natural
next step is to complement these experiments with human annotations. Moreover, human preference
annotations would shed more light on the trade-off between the utility of responses vs abstentions,
as discussed in Section 4. Such studies would thus help clarify whether the utility improvements
measured by LLM judges correspond to user-perceived improvements in realistic deployment settings.
Efficient posterior sampling. Another practical consideration is how posterior particles are sampled.
In our experiments, the posterior is approximated using finite sets of base-model completions
sampled from the underlying LM, together with the abstention atom. These particles are rescored
and reweighted to form an empirical posterior, which is sufficient to validate the finite-sample
guarantees proved in the paper. However, this approximation may become inefficient when high-
scoring completions are rare or concentrated in low-probability regions of the base distribution.
Developing more efficient posterior samplers is therefore an important direction for future work.

References
Anastasios Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, and Tal Schuster. Conformal risk
  control. In International conference on learning representations, volume 2024, pages 55198–55218,
  2024a.
Anastasios N Angelopoulos, Rina Foygel Barber, and Stephen Bates. Theoretical foundations of
  conformal prediction. arXiv preprint arXiv:2411.11824, 2024b.
Anastasios N Angelopoulos, Stephen Bates, Emmanuel J Candès, Michael I Jordan, and Lihua Lei.
  Learn then test: Calibrating predictive algorithms to achieve risk control. The Annals of Applied
 Statistics, 19(2):1641–1662, 2025.
John J Cherian, Isaac Gibbs, and Emmanuel J Candès. Large language model validity via enhanced
  conformal prediction methods. Advances in Neural Information Processing Systems, 37:114812–
  114842, 2024.
Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen, Yoon Kim, and Jacob
 Andreas. Beyond binary rewards: Training lms to reason about their uncertainty. International
 conference on learning representations, 2026.
Fatemeh Dehghani, Roya Dehghani, Yazdan Naderzadeh Ardebili, and Shahryar Rahnamayan. Large
  language models in legal systems: A survey. Humanities and Social Sciences Communications, 12
  (1):1977, 2025.
Gianluca Detommaso, Martin Bertran, Riccardo Fogliato, and Aaron Roth. Multicalibration for
  confidence scoring in llms. In Proceedings of the 41st International Conference on Machine
  Learning, 2024.
Dongyang Fan, Sebastien Delsad, Nicolas Flammarion, and Maksym Andriushchenko. Halluhard: A
  hard multi-turn hallucination benchmark. arXiv preprint arXiv:2602.01031, 2026.
Clara Fannjiang, Stephen Bates, Anastasios N Angelopoulos, Jennifer Listgarten, and Michael I
  Jordan. Conformal prediction under feedback covariate shift for biomolecular design. Proceedings
  of the National Academy of Sciences, 119(43):e2204569119, 2022.
Farieda Gaber, Maqsood Shaik, Fabio Allega, Agnes Julia Bilecz, Felix Busch, Kelsey Goon, Vedran
  Franke, and Altuna Akalin. Evaluating large language model workflows in clinical decision support
  for triage and referral and diagnosis. npj Digital Medicine, 8(1):263, 2025.
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
  Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of
  models. arXiv preprint arXiv:2407.21783, 2024.
Ursula Hébert-Johnson, Michael Kim, Omer Reingold, and Guy Rothblum. Multicalibration: Cali-
  bration for the (computationally-identifiable) masses. In International Conference on Machine
  Learning, pages 1939–1948. PMLR, 2018.


                                                  10
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv
  preprint arXiv:2103.03874, 2021.
Alexander K Lew, Tan Zhi-Xuan, Gabriel Grand, and Vikash K Mansinghka. Sequential monte carlo
  steering of large language models using probabilistic programs. arXiv preprint arXiv:2306.03081,
  2023.
João Loula, Benjamin LeBrun, Li Du, Ben Lipkin, Clemente Pasti, Gabriel Grand, Tianyu Liu, Yahya
  Emara, Marjorie Freedman, Jason Eisner, et al. Syntactic and semantic control of large language
  models via sequential monte carlo. In International Conference on Learning Representations,
  volume 2025, pages 64758–64791, 2025.
Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Koh, Mohit Iyyer, Luke
  Zettlemoyer, and Hannaneh Hajishirzi. Factscore: Fine-grained atomic evaluation of factual
  precision in long form text generation. In Proceedings of the 2023 Conference on Empirical
  Methods in Natural Language Processing, pages 12076–12100, 2023.
Christopher Mohri and Tatsunori Hashimoto. Language models with conformal factuality guarantees.
  In International Conference on Machine Learning, pages 36029–36047. PMLR, 2024.
Drew Prinster, Samuel Don Stanton, Anqi Liu, and Suchi Saria. Conformal validity guarantees
  exist for any data distribution (and how to find them). In Proceedings of the 41st International
  Conference on Machine Learning, pages 41086–41118, 2024.
Victor Quach, Adam Fisch, Tal Schuster, Adam Yala, Jae Ho Sohn, Tommi Jaakkola, and Regina
  Barzilay. Conformal language modeling. In International Conference on Learning Representations,
  volume 2024, pages 11654–11681, 2024.
Aaditya Ramdas and Ruodu Wang. Hypothesis testing with e-values. Foundations and Trends® in
  Statistics, 1(1-2):1–390, 2025.
Maxon Rubin-Toles, Maya Gambhir, Keshav Ramji, Aaron Roth, and Surbhi Goel. Conformal
 language model reasoning with coherent factuality. In The Thirteenth International Conference on
 Learning Representations, 2025.
Shuvom Sadhuka, Drew Prinster, Clara Fannjiang, Gabriele Scalia, Aviv Regev, and Hanchen
  Wang. E-valuator: Reliable agent verifiers with sequential hypothesis testing. arXiv preprint
  arXiv:2512.03109, 2025.
Craig Saunders, Alexander Gammerman, and Volodya Vovk. Transduction with confidence and
  credibility. In Proceedings of the Sixteenth International Joint Conference on Artificial Intelligence,
  1999.
Ryan J Tibshirani, Rina Foygel Barber, Emmanuel Candes, and Aaditya Ramdas. Conformal
  prediction under covariate shift. Advances in neural information processing systems, 32, 2019.
Ben Van Calster, Daan Nieboer, Yvonne Vergouwe, Bavo De Cock, Michael J Pencina, and Ewout W
  Steyerberg. A calibration hierarchy for risk models was defined: from utopia to empirical data.
  Journal of clinical epidemiology, 74:167–176, 2016.
Aad W van der Vaart and Jon A Wellner. Weak convergence and empirical processes. With applications
  to statistics. Springer Series in Statistics, 1996.
Menghua Wu, Cai Zhou, Stephen Bates, and Tommi Jaakkola. Thought calibration: Efficient and
 confident test-time scaling. In Proceedings of the 2025 Conference on Empirical Methods in
 Natural Language Processing, pages 14302–14316, 2025.
Stephen Zhao, Rob Brekelmans, Alireza Makhzani, and Roger Baker Grosse. Probabilistic inference
  in language models via twisted sequential monte carlo. In International Conference on Machine
  Learning, pages 60704–60748. PMLR, 2024.
Cai Zhou, Zekai Wang, Menghua Wu, Qianyu Julie Zhu, Flora C Shi, Chenyu Wang, Ashia Wilson,
  Tommi Jaakkola, and Stephen Bates. Online reasoning calibration: Test-time training enables
  generalizable conformal llm reasoning. arXiv preprint arXiv:2604.01170, 2026.


                                                   11
A     Consequences of Calibrated Scores

In this section, we make the informal statement about calibrated forecasts from Section 2.2 precise.
Define the random variable Zi := 1 {claim i is conditionally correct}, and the indicator Ei :=
1 {claim i ends with an EOS token}. We will reason about the filtration F = {Fi }i∈N where Fi :=
σ(x, s ≤i , E≤i ). Note that the inclusion of information about end of sequence tokens will allow us to
make statements about random stopping times (in particular the random K) and can be thought of as
a technical artefact void of any deeper meaning.
                            Qi−1
For shorthand, let Z<i = j=1 Zj and Z≤i = Z<i Zi . Suppose then that the scores were such that

                                     E[Zi | Fi , Z<i = 1] = si              for i ≥ 1.                                   (11)

Intuitively, this means that conditioned on all prior scores and the prior claims being correct, the
score si is a calibrated predictor of the correctness of the subsequent claim ci . When k > K, it is
trivially satisfied.
Suppose also that the current score si does not give any additional information about the correctness
of past claims that is not already captured by the preceding scores s <i ; that is,

                                            1 {Z<i = 1} ⊥ si , Ei | Fi−1 .                                               (12)

Intuitively, this means that the correctness of a prefix can be asserted without looking at the rest of the
sentence. We will also write 1 {Z<i = 1} ⊥ Fi | Fi−1 . This essentially assumes that future scores
give no additional information about past correctness, if the past scores are available, which we find
plausible10 . Note also that if Fk−1 reveals that some claim c1 , . . . , ck−1 contains an EOS token, then
we assume for mathematical convenience that sk is deterministically 1 conditional on the information
in Fk−1 . Then, no information is gained from Fk either, and the assumption is also trivially satisfied
when k > K.
This appendix supplies the formal statement and derivation backing the informal Observation 1 in
Section 2.2. Concretely:
Proposition A.1 (Formal version of Observation 1). Let {si }i≥1 be the claim-level score sequence
produced when sampling y ∼ pLLM (· | x), let K denote the random number of claims in y, and let Zi
indicate conditional correctness of claim i (Section 2.2). Suppose s satisfies the stepwise-calibration
condition (11) and the conditional independence condition (12). Then for any τ ∈ [0, 1],
                                                                            
                                                            QK
                                        P Z≤K = 1              i=1 si ≥ τ        ≥ τ.


Setting τ = 1 − α gives E[ℓ(x, y) | Φ1−α (y | x) = 1] ≤ α.

The remainder of the appendix develops the argument. We pick up the discussion from Section 2.2
again. Recall that we defined the σ-algebras Fi := σ(x, s ≤i , E≤i ). Formally, we define the stopping
time K to be

                                               K = inf {k | Ek = 1} .

Making what we mentioned above about mathematical convenience more precise, we also set Zk = 1,
sk = 1 and ck = ∅ for k > K. Clearly, K is a valid stopping time, since the event {K ≤ ℓ} is
Fℓ -measurable, because Fℓ includes E≤ℓ in its definition, and the information contained in the events
E1 , . . . , Eℓ is sufficient to determine whether K = ℓ has occurred.
Let us first fix k.

  10 And in any case, this development is purely motivating, and not required for the correctness and calibration guarantees in

Section 3.


                                                             12
                           E[Z≤k | Fk ] = E[Z<k Zk | Fk ]
                                        = E[Z<k E[Zk | Fk , Z<k ] | Fk ]
                                          (i)
                                          = E[Z<k E[Zk | Fk , Z<k = 1] | Fk ]
                                          (ii)
                                          = E[Z<k sk | Fk ]
                                          = sk P(Z<k = 1 | Fk )
                                          (iii)
                                              = sk P(Z<k = 1 | Fk−1 ).
We briefly comment on the steps:
      (i) follows because
                       E[Zk | Fk , Z<k ] = 1 {A} E[Zk | Fk , A] + 1 {Ac } E[Zk | Fk , Ac ]
          and for any event A that is determined by Z<k (meaning deterministic conditional on the
          realization of the random variable Z<k ). Multiplying by 1 {A} for A = {Z<k = 1} shows
          the step.
     (ii) follows because of (11)
    (iii) follows because of (12)
A proof by induction shows that for any fixed k ≥ 1
                                                             Qk
                                          E[Z≤k | Fk ] =      i=1 si .                           (13)

Since K is a stopping time and K ≤ L almost surely11 , we can deduce that for the stopped σ-algebra,
                                                     QK
                                      E[Z≤K | FK ] = i=1 si ,                                  (14)
which shows the first part of our claim.
We are now interested in
      "          K
                          #                  K
                                                     !              K
                                                                            !
                Y                            Y                      Y
    E ℓ(x, y) |     si ≥ τ = P ℓ(x, y) = 1 |   si ≥ τ = P Z≤K = 0 |   si ≥ τ .
                   i=1                                 i=1                         i=1
In words, this is the probability of incorrectness of some claim jointly over the claims, when we
sample from the posterior distribution conditional on the scores being above the threshold τ . We will
now show that this quantity is in turn upper bounded by 1 − τ , suggesting that calibrated scores lead
to the choice τ = 1 − α and guarantee α-level risk control.
To see why, let us first rewrite
                                                                  QK
                                QK                  P(Z≤K = 1 and i=1 si ≥ τ )
                P(Z≤K = 1 |        i=1 si ≥ τ ) =           QK
                                                          P( i=1 si ≥ τ )
                                                      h n              QK      oi
                                                    E 1 Z≤K = 1 and i=1 si ≥ τ
                                                  =           QK
                                                            P( i=1 si ≥ τ )
                                                      h     nQ            oi
                                                               K
                                                    E Z≤K 1    i=1 si ≥ τ
                                                  =       QK                 .
                                                        P( i=1 si ≥ τ )
                                QK
We focus onnthe numerator.oSince i=1 si is FK -measurable for the random stopping time K, the
             QK
event Aτ =     i=1 si ≥ τ is also FK -measurable. Therefore

                                   E[Z≤K 1Aτ ] = E[E[Z≤K 1Aτ | FK ]]
                                               = E[E[Z≤K | FK ]1Aτ ]
                                                    QK
                                               = E[ i=1 si 1Aτ ]
                                               ≥ τ E[1Aτ ]
                                               = τ P(Aτ ).
  11 The maximum length of the LLM response




                                                      13
Dividing by P(Aτ ) gives
                                                 E[Z≤K | Aτ ] ≥ τ.
Since Z≤K is binary, and setting τ = 1 − α, this is equivalent to
                                 P(Z≤K = 1 | Φ1−α (y | x) = 1) ≥ 1 − α.

B     Deferred Proofs from Section 3
B.1    Proof of Proposition 3.1 (Known Z τ (x))

We collect the auxiliary results needed for the proof, then present the main argument. Along with
monotonicity by design, the proof will make use of the following likelihood ratio reweighting:
Fact 1. Fix x and τ . Suppose we draw y ∼ p(· | x) and y ′ ∼ pτ (· | x). Then
                                   τ                
                                   Φ (y | x)
                      Ey∼p(· | x)            ℓ(x, y)   = Ey′ ∼pτ (· | x) [ℓ(x, y ′ )] .                 (15)
                                    Z τ (x)

Proof of Fact 1
Proof. We have
                                                       X
                          Ey∼pτ (· | x) [ℓ(x, y)] =            ℓ(x, y) pτ (y | x)
                                                       y∈V ∗
                                                       X          Φτ (y | x) p(y | x)
                                                   =          ℓ(x, y)
                                                                       Z τ (x)
                                                     y∈V ∗

                                                                         Φτ (y | x)
                                                                                   
                                                   = Ey∼p(· | x) ℓ(x, y) τ            .
                                                                           Z (x)


                                                                                    τ
                                                               Φ (yi | xi )
We now turn to the monotonized importance weights w̄i (τ ) = Z S(yi | xi ) (x )
                                                                                , as well as their re-
                                                                                          i
                                             τ
                                          i | xi )
lationship to the weights wi (τ ) = Φ Z(y
                                        τ (x ) . We write ℓi = ℓ(xi , yi ) as a shorthand in what
                                             i
follows.
Lemma B.1. The monotonized weights w̄i (τ ) satisfy:

      (1) w̄i (τ )ℓi is non-increasing in τ .
      (2) w̄i (τ )ℓi ≥ wi (τ )ℓi for all τ , and hence Ep0 [w̄i (τ )ℓi ] ≥ Epτ [ℓi ].
      (3) w̄i (τ )ℓi ≤ 1/β.

Proof. (1): w̄i (τ )ℓi = Z S(yi |ℓixi ) (x ) 1{S(yi | xi ) ≥ τ } is constant for τ ≤ S(yi | xi ) and zero for
                                        i

τ > S(yi | xi ). (2): For τ ≤ S(yi | xi ), Z S(yi | xi ) (xi ) ≤ Z τ (xi ) (since Z τ is non-increasing), so
w̄i (τ ) ≥ wi (τ ); for τ > S(yi | xi ), both are zero. The expectation bound follows from Fact 1. (3):
Z S(yi | xi ) (xi ) ≥ β since the abstention atom always survives, and ℓ, Φτ ∈ {0, 1}.

The proof of Proposition 3.1 assumes a hallucinated completion from the mixture prior on the test
                                        i.i.d.
prompt. Formally, we assume that yn+1 ∼ p(· | xtest ) conditionally independently of the sample
ytest given xtest . We also denote xn+1 = xtest for convenience. The selection rule τ̂id is then
compared to the “oracle” one that assumes access to a hallucinated base completion:
                               (           n+1
                                                                                 )
                       ∗              1 X Φτ (yi | xi )
                     τid = inf τ |                                ℓ(xi , yi ) ≤ α .          (16)
                                    n + 1 i=1 Z S(yi | xi ) (xi )
                   ∗
Lemma B.2. τ̂id ≥ τid almost surely.


                                                         14
                                                        1
                                                                           Pn                    1
Proof. For any τ in the feasible set of τ̂id , we have n+1                   i=1 w̄i (τ )ℓi + β(n+1)   ≤ α. Since
w̄n+1 (τ )ℓn+1 ≤ 1/β by Lemma B.1:
                              n+1                     n
                          1 X                    1 X                     1
                                  w̄i (τ )ℓi ≤           w̄i (τ )ℓi +          ≤ α.
                        n + 1 i=1              n + 1 i=1              β(n + 1)
                                 ∗            ∗
So τ is in the feasible set of τid , giving τid ≤ τ̂id a.s.

Main Proof of Proposition 3.1

Proof. Step 1: Reduce to monotonized weights at τ̂id . Recall that the test response ytest is drawn
from pτ̂id (· | xtest ) for a fresh test prompt xtest ∼ PX exchangeable with the calibration prompts,
where τ̂id = τ̂id (D1:n ) depends only on the calibration set. Let us denote by xn+1 = xtest and
let yn+1 ∼ p(· | xn+1 ) be a hallucinated sample from the mixture prior. Since τ̂id is chosen
without knowledge of the realization of (xn+1 , yn+1 ), Fact 1 gives E[ℓ(xtest , ytest ) | τ̂id , xtest ] =
E[wn+1 (τ̂id )ℓ(xn+1 , yn+1 ) | τ̂id , xtest ]. By Lemma B.1, w̄n+1 (τ ) ≥ wn+1 (τ ) pointwise, so
                          E[ℓ(xtest , ytest ) | τ̂id ] ≤ E[w̄n+1 (τ̂id ) ℓn+1 | τ̂id ],   a.s.
From this
                             E[ℓ(xtest , ytest )] ≤ E[w̄n+1 (τ̂id ) ℓn+1 ]                                    (17)
where we took the expectation over the randomness in τ̂id again.
                                ∗                           ∗
Step 2: Transfer from τ̂id to τid . By Lemma B.2, τ̂id ≥ τid   a.s. Since by Lemma B.1 w̄n+1 (τ )ℓn+1 is
non-increasing in τ :
                                                            ∗
                               w̄n+1 (τ̂id ) ℓn+1 ≤ w̄n+1 (τid ) ℓn+1 , a.s.                        (18)
Step 3: Exchangeability. The hallucinated calibration set D1:n+1 = {(xi , yi )}n+1                12
                                                                               i=1 is exchangeable ,
       ∗        ∗
and τid    = τid  (D1:n+1 ) is permutation invariant. Therefore, conditional on the multiset E =
{(xi , yi )}i∈[n+1] , we have
                                                                  n+1
                                       ∗                      1 X            ∗
                            E[w̄n+1 (τid ) ℓn+1 | E] =                w̄i (τid )ℓi ≤ α,
                                                            n + 1 i=1
                                         ∗
where inequality uses the definition of τid in (16). Integrating out E again gives us
                                                 "        n+1
                                                                           #
                                  ∗                   1 X            ∗
                       E[w̄n+1 (τid ) ℓn+1 ] = E              w̄i (τid ) ℓi ≤ α.
                                                   n + 1 i=1

Finally, we combine the pieces to obtain
                                      (17)                          (18)
                                                                            ∗
                  E[ℓ(xtest , ytest )] ≤ E[w̄n+1 (τ̂id ) ℓn+1 ] ≤ E[w̄n+1 (τid ) ℓn+1 ] ≤ α.



B.2      Proof of Theorem 3.2 (Empirical Posterior Calibration)

We first give an equivalent of Fact 1 for this setting.
Lemma B.3 (Risk under Empirical Posterior). Let γ be any [0, 1]-valued random variable. For any i,
suppose that conditional on observing (xi , Ti , γ) we draw y ∼ p̂γ (· | xi , Ti ). Then
                                         E[ℓ(xi , y) | xi , Ti , γ] = Ĥi (γ).

Proof. Conditional on (xi , Ti , γ), the distribution p̂γ (· | xi , Ti ) is finitely supported on
                                        (1−β)Φγ (yij | xi )/M
{yi1 , . . . , yiM , abstain} with mass     Ẑ γ (xi ,Ti )
                                                              on each yij and mass Ẑ γ (xβ ,T ) on abstain.
                                                                                           i  i
Summing ℓ against these weights and using ℓ(xi , abstain) = 0 yields the result.
   12 Indeed, we assumed the prompts were exchangeable, and the responses were conditionally independent draws from

p(· | xi ).


                                                          15
Lemma B.4. The monotonized estimator H̄i (τ ) = supτ ′ ≥τ Ĥi (τ ′ ) satisfies:

     (1) H̄i (τ ) is non-increasing in τ .

     (2) H̄i (τ ) ≥ Ĥi (τ ) for all τ .
     (3) H̄i (τ ) ≤ 1.

Proof. (1) If τ1 < τ2 , then H̄i (τ1 ) = supτ ′ ≥τ1 Ĥi (τ ′ ) ≥ supτ ′ ≥τ2 Ĥi (τ ′ ) = H̄i (τ2 ). (2) Immediate.
                                                           1
                                                               P τ                      τ
(3) The numerator of (9) is bounded above by (1−β) M             j Φ (yij | xi ) ≤ Ẑ (xi , Ti ), so Ĥi (τ ) ≤ 1,
and a supremum of values in [0, 1] is in [0, 1].
Lemma B.5. Let us refer to the test prompt xtest and tuple Ttest as xn+1 and Tn+1 respectively.
Define the oracle                    (                          )
                                                n+1
                            ⋆              1 X
                           τ = inf τ |              H̄i (τ ) ≤ α .                        (19)
                                         n + 1 i=1
Then τ̂ ≥ τ ⋆ almost surely.
                                                                     1
                                                                                   Pn                    1
Proof. For any τ in the feasible set of τ̂ , Algorithm 1 guarantees n+1                  i=1 H̄i (τ ) + n+1   ≤ α.
Since by Lemma B.4, H̄n+1 (τ ) ≤ 1,
                                 n+1                   n
                             1 X                  1 X                 1
                                     H̄i (τ ) ≤           H̄i (τ ) +     ≤ α,
                           n + 1 i=1            n + 1 i=1            n+1
so τ is in the feasible set of τ ⋆ , giving τ ⋆ ≤ τ̂ a.s.

Main Proof of Theorem 3.2
The proof follows the general approach for conformal risk control proofs Angelopoulos et al. [2024a]

Proof. The test response is ytest ∼ p̂τ̂ (· | xtest , Ttest ). Write (xn+1 , Tn+1 ) := (xtest , Ttest ) for
the test tuple. Since the prompts (xi )n+1
                                       i=1 are exchangeable and, conditional on these prompts, the
particles in each Ti are drawn i.i.d. from pLLM (· | xi ), the tuples (xi , Ti )n+1
                                                                                i=1 are exchangeable as
well.

Step 1: Empirical Posterior Risk at τ̂ . When ytest ∼ p̂τ̂ (· | xtest , Ttest ), Lemma B.3 applied with
γ = τ̂ gives
                          E[ℓ(xtest , ytest ) | xtest , Ttest , τ̂ ] = Ĥn+1 (τ̂ ).
Combining with Lemma B.4 (2) and taking the outer expectation,
                             E[ℓ(xtest , ytest )] = E[Ĥn+1 (τ̂ )] ≤ E[H̄n+1 (τ̂ )].                          (20)

Step 2: Transfer from τ̂ to τ ⋆ . By Lemma B.5, τ̂ ≥ τ ⋆ a.s. Since H̄n+1 (τ ) is non-increasing in τ , by
Lemma B.4,
                                      H̄n+1 (τ̂ ) ≤ H̄n+1 (τ ⋆ ), a.s.                               (21)

Step 3: Exchangeability. The tuples (xi , Ti )n+1
                                              i=1 are exchangeable, and τ
                                                                          ⋆
                                                                            = τ ⋆ ((xi , Ti )n+1
                                                                                             i=1 )
is a symmetric function of these tuples. Conditioning on the multiset E = {(xi , Ti )}i∈[n+1] ,
exchangeability gives
                                                         n+1
                                                     1 X
                           E[H̄n+1 (τ ⋆ ) | E] =             H̄i (τ ⋆ ) ≤ α,     a.s.,
                                                   n + 1 i=1
by the definition of τ ⋆ in (19). Integrating over E,
                                             E[H̄n+1 (τ ⋆ )] ≤ α.                                             (22)

Combining (20), (21), and (22) yields E[ℓ(xtest , ytest )] ≤ α.


                                                       16
B.3    Proof of Lemma 3.3

Before proving the lemma, we will need a technical lemma bounding the bracketing number van der
Vaart and Wellner [1996] of some function classes. Let us denote briefly by PY,S|x the conditional
joint distribution of responses and scores given a prompt x.13
Lemma B.6. Assume the distribution of the scores is continuous14 . Let h : V ∗ × S → {0, 1} be a
fixed measurable map. Define the function class
                                G = {(y, s) 7→ h(y, s)1 {s ≥ τ } | τ ∈ [0, 1]} ,
and identify its elements as gτ . Then, for every ε > 0,
                                                             
                                    N[ ] ε, G, ∥·∥L1 (PY,S|x ) < ∞.

Proof. Let P = PY,S|x . For τ ∈ [0, 1], write
                                           gτ (y, s) = h(y, s)1 {s ≥ τ } .
Fix τ1 ≤ τ2 . Then for every τ ∈ [τ1 , τ2 ],
        gτ2 (y, s) = h(y, s)1 {s ≥ τ2 } ≤ h(y, s)1 {s ≥ τ } ≤ h(y, s)1 {s ≥ τ1 } = gτ1 (y, s),
where we used that h ≥ 0. Hence the bracket
                                                       [gτ2 , gτ1 ]
contains all functions gτ with τ ∈ [τ1 , τ2 ].
The L1 (P )-width of this bracket is
                      ∥gτ1 − gτ2 ∥L1 (P ) = EP [h(Y, S) (1 {S ≥ τ1 } − 1 {S ≥ τ2 })]
                                             = EP [h(Y, S)1 {τ1 ≤ S < τ2 }] .
Define the finite measure µh on [0, 1] by
                                       µh (A) = EP [h(Y, S)1 {S ∈ A}] .
Since h ∈ {0, 1}, we have µh ([0, 1]) ≤ 1. With this notation,
                                        ∥gτ1 − gτ2 ∥L1 (P ) = µh ([τ1 , τ2 )).

Now fix ε > 0. Since µh is a finite measure on [0, 1], we can partition [0, 1] into finitely many intervals
Ik = [ak , ak+1 ) such that each interval has µh -mass at most ε. Since the scores are continuous, this
measure has no atoms. For each such interval Ik = [ak , ak+1 ), the bracket
                                                      [gak+1 , gak ]
has L1 (P )-width
                                   gak − gak+1 L1 (P ) = µh ([ak , ak+1 )) ≤ ε.
Thus finitely many L1 (P )-brackets of width at most ε cover G. Therefore
                                                           
                                  N[ ] ε, G, ∥·∥L1 (PY,S|x ) < ∞.



We are ready to prove Lemma 3.3.
                                                                                                       i.i.d.
Fix a prompt x and abstention mass β > 0. Write TMQ = (y1 , . . . , yM ) with yj ∼ pLLM (· | x).
Recall Φτ (y | x) = 1 {S(y | x) ≥ τ } where S(y | x) = i si is the completion-level score. Define
the quantities
                               M
                          1 X τ
           ÂM (τ ) :=          Φ (yj | x) ℓ(x, yj ),            A(τ ) := Ey∼pLLM [Φτ (y | x) ℓ(x, y)],
                          M j=1
 13We only model the joint distribution to handle randomized scorers; for deterministic scorers this is not necessary and a

measure over V ∗ suffices.
 14We enforce this by adding noise to the elicited scores.




                                                           17
                                        M
                                 1 X τ
                   B̂M (τ ) :=         Φ (yj | x),                B(τ ) := Ey∼pLLM [Φτ (y | x)].
                                 M j=1
The empirical and population mixture normalizers are
                           τ
                         ẐM = β + (1 − β)B̂M (τ ),                   Z τ = β + (1 − β)B(τ ),
both in [β, 1]. We dropped the dependence on x, as we fixed this variable already.

Step 1: Uniform convergence via Glivenko–Cantelli. Instantiating h(y, s) = ℓ(x, y) and h(y, s) = 1
shows that {y 7→ 1{S(y | x) ≥ τ } : τ ∈ [0, 1]} and {y 7→ ℓ(x, y)1{S(y | x) ≥ τ } : τ ∈ [0, 1]}
have finite Bracketing number, by Lemma B.6. By Theorem 2.4.1. in van der Vaart and Wellner
[1996], both of these classes are therefore Glivenko-Cantelli. Therefore
                                               a.s.                                               a.s.
              sup ÂM (τ ) − A(τ ) −−−−→ 0,                           sup B̂M (τ ) − B(τ ) −−−−→ 0.      (23)
             τ ∈[0,1]                         M →∞                τ ∈[0,1]                      M →∞



Step 2: Uniform convergence of the empirical-posterior risk. Recall that the empirical and population
conditional risks are given by

               R̂M = Ey∼p̂τ (· | x,TM ) [ℓ(x, y)]               and      RM = Ey∼pτ (· | x) [ℓ(x, y)].
This can be rewritten as
                                        (1 − β)ÂM (τ )                              (1 − β)A(τ )
                        R̂M (x, τ ) =                       ,         R(x, τ ) =                  .
                                                 τ
                                               ẐM                                       Zτ

Adding and subtracting (1 − β)ÂM (τ )/Z τ , we get

                               (1 − β)ÂM (τ )            (1 − β)A(τ )
R̂M (x, τ ) − R(x, τ ) =                              −
                                          τ
                                        ẐM                   Zτ

                               (1 − β)ÂM (τ )            (1 − β)ÂM (τ ) (1 − β)ÂM (τ ) (1 − β)A(τ )
                           =                          −                  +               −
                                          τ
                                        ẐM                    Zτ              Zτ             Zτ

                               (1 − β)ÂM (τ ) (1 − β)A(τ )   (1 − β)ÂM (τ ) (1 − β)ÂM (τ )
                           ≤                  −             +                −
                                    Zτ             Zτ                τ
                                                                   ẐM             Zτ

                               1−β                                      1  1
                           =      τ
                                    ÂM (τ ) − A(τ ) + (1 − β)ÂM (τ ) τ − τ
                                Z                                     ẐM Z
                                                                      τ
                             1−β                                    ẐM  − Zτ
                           =     ÂM (τ ) − A(τ ) + (1 − β)ÂM (τ )           .
                              Zτ                                        τ Zτ
                                                                      ẐM
Since
          τ
            − Z τ = β + (1 − β)B̂M (τ ) − β + (1 − β)B(τ ) = (1 − β)(B̂M (τ ) − B(τ )),
                                                       
        ẐM

and since ÂM (τ ) ≤ 1, Z τ ≥ β, and ẐM
                                       τ
                                         Z τ ≥ β 2 , it follows that
                                            1−β                    (1 − β)2
           R̂M (x, τ ) − R(x, τ ) ≤             ÂM (τ ) − A(τ ) +          B̂M (τ ) − B(τ ) .
                                             β                        β2

Taking the supremum over τ ∈ [0, 1] on both sides and applying (23),
                                                                              a.s.
                                   sup R̂M (x, τ ) − R(x, τ ) −−−−→ 0.                                   (24)
                                  τ ∈[0,1]                                   M →∞

The same argument applies for PX -a.e. x, completing the proof of Lemma 3.3.


                                                            18
B.4    Proof of Corollary 3.4

Since the guarantee above holds uniformly over τ , it in particular holds for the selected threshold
τ̂M ∈ [0, 1] from Algorithm 1 when run with M samples from pLLM :
                 R̂M (xtest , τ̂M ) − R(xtest , τ̂M ) ≤ sup R̂M (xtest , τ ) − R(xtest , τ ) .
                                                                 τ ∈[0,1]

So by (24) and by the bounded convergence theorem,
                         "                                                        #
                              E     sup R̂M (xtest , τ ) − R(xtest , τ )              −−−−→ 0.
                                  τ ∈[0,1]                                            M →∞


By Theorem 3.2,
                                        E[R̂M (xtest , τ̂M )] ≤ α.
                pop     τ̂M
Therefore, for ytest ∼ p (· | xtest ),
                                       pop
                          E[ℓ(xtest , ytest )] = E[R(xtest , τ̂M )] ≤ α + o(1),
and hence
                                                                  pop
                                             lim sup E[ℓ(xtest , ytest )] ≤ α.
                                             M →∞


C     Design Choices for the Conformal Routine
This appendix provides motivation and design rationale for the calibration rule in Section 3. The
arguments here are not needed for the validity proofs of Proposition 3.1 and Theorem 3.2. Instead,
they explain how the rule arises from an idealized known-normalizer setting and why we use a
fixed-denominator, monotonized objective. We highlight the connections to traditional approaches to
conformal prediction with (fixed) covariate and label shift.
                                                                                                 ∗
The calibration procedures developed in Section 3 are intuitively derived from the oracles τid      and
  ⋆
τ in (16) and (19) respectively, both of which use a fixed denominator of n + 1 and importance-
reweights prior samples to evaluate/estimate the posterior risk. A natural alternative is to use an
adaptive (self-normalized) denominator, as is common in the distribution-shift conformal prediction
literature [Tibshirani et al., 2019, Angelopoulos et al., 2024b, Fannjiang et al., 2022, Prinster et al.,
2024]. Fundamentally, this oracle arises as follows. Suppose that Ui ∼ P for i ∈ [n] and Un+1 ∼ Q.
Then conditional on the multiset of observed values E = {U1 , . . . , Un , Un+1 }
                                             n+1                                      dQ(Ui )
                                                                                      dP (U )
                                             X                                         i
                             Un+1 | E ∼             vi δUi    where         vi = Pn+1 dQ(U )
                                                                                             .
                                                                                                i
                                              i=1                                  i=1 dP (Ui )

This can be found in Proposition 7.6. of Angelopoulos et al. [2024b]. Extensions exist under Feedback
covariate shift Fannjiang et al. [2022] and more arbitrary dependencies Prinster et al. [2024]. As a
consequence, if we had xi ∼ PX for i ∈ [n + 1] and yn+1 ∼ pτ (· | xn+1 ) for fixed τ , we’d have
                                               n+1                                Φτ (yi | xi )
                                                                                   Z τ (xi )
                                               X
                    (xn+1 , yn+1 ) | E ∼             vi δ(xi ,yi )   where vi = Pn+1 Φτ (y
                                                                                             j | xj )
                                               i=1                               j=1    Z τ (xj )


In the known Z τ case, this could suggest15 an oracle selection rule
                                     P                                       
                                            n+1 Φτ (yi | xi )
                           ∗
                                    
                                            i=1     τ
                                                  Z (xi )     ℓ(xi , yi )     
                         τSN  = inf τ |       Pn+1 Φτ (yi | xi )          ≤ α   ,
                                                         τ
                                                                              
                                                              i=1     Z (xi )
              ∗
Intuitively, τSN computes a weighted average of the losses, with weights proportional to each point’s
                                τ
likelihood under the posterior p . One issue however, is that this is ill defined. For the weighted
exchangeability to make sense, yn+1 now needs to be sampled according to pτ . However, τ depends
                                                                   ∗
on yn+1 . This creates a circular dependency, that the choice of τid and τ ⋆ is able to sidestep, by
depending only on a hallucinated calibration set completions from the prior.
  15 Ignoring for a second that monotonizing this objective is also trickier than if the denominator is fixed.




                                                               19
Population-Level Equivalence
                                          ∗       ∗
We might still be curious about why τid      and τSN  are different, even though both seem principled.
                                           ∗                             ∗
In fact, the expected denominator in τSN       coincides with that in τid  . Writing wi (τ ) = Φτ (yi |
      τ
xi )/Z (xi ), a direct calculation using the tower rule gives
             "n+1         # n+1                            n+1
               X               X         Φτ (Yi | Xi )            X  Z τ (Xi ) 
           E       wi (τ ) =       E E                   Xi =          E τ          = n + 1.
               i=1             i=1
                                            Z τ (Xi )             i=1
                                                                          Z (Xi )
Thus, in expectation, the self-normalized denominator equals n + 1. The two oracles can therefore
be expected to behave similarly in large samples. Indeed, empirical experimentation has shown us
that their resulting approximations behave very similarly in practice too. As our theoretical analysis
            ∗
employs τid   , our Algorithm 1 also uses a fixed denominator.

D                        Extensive Experimental Results
D.1                          MATH Calibration Validity

Figure 4 shows the results of the empirical validity experiment (Figure 1) for both FActScore and
MATH. MATH mirrors FActScore: empirically, valid coverage is achieved at all levels, with a
flatlining region at targets low enough that both methods degrade to sampling from the prior.

                       1.0       ours                                                           1.0   ours
                                 MH                                                                   MH
                                 y=x                                                                  y=x
                       0.8                                                                      0.8
empirical factuality




                                                                         empirical factuality

                       0.6                                                                      0.6

                       0.4                                                                      0.4

                       0.2                                                                      0.2

                       0.0                                                                      0.0
                                  0.4          0.6            0.8                                      0.4        0.6            0.8
                                          target factuality                                                  target factuality
                                        (a) FActScore.                                                       (b) MATH.
Figure 4. Target vs. observed factuality on FActScore (a) and MATH (b); ours (blue) and MH (orange). Both
methods produce empirically valid coverage on both tasks. Averaged over 10 splits; shaded area shows 95% CIs.


D.2                          Per-statement Likert Scores

Figure 5 breaks down the FActScore downstream utility results from Figure 2 across the three axes
(see Appendix E.4). These results reveal that even at high targets, the LM judge considers non-
abstaining outputs from both methods to be fluent and coherent. However, as the target factuality
increases, outputs from MH quickly degrade in terms of their completeness and helpfulness. Note that
Figure 2 is the arithmetic mean of these axes.

D.3                          Alternative scoring functions and base models

The main text elicits per-claim scores for Llama-3.3-70B-Instruct generations by asking GPT-4o
to rate its confidence on a 0-1 scale (Section 2.4). A natural, cheaper alternative is to read off
the scorer’s own token log-probabilities for a forced T/F judgement; we compute this scorer as
s = (pT + pN )/(pT + pN + pF ) using GPT-4o. Figure 6 shows the impact that this alternative
formulation has on calibration validity and sample utility. Both scorers produce empirically valid
calibration curves, as predicted. Furthermore, for our method both scorers yield similar utilities; for
MH, the logprob-based scorer yields slightly higher strict factuality among non-abstaining outputs at
high targets in this experiment.
In Figure 7, we perform a related comparison: replacing both the base model and the scorer with
smaller (and thus cheaper, but less capable) variants within the same family. Specifically, we


                                                                    20
                  5                                                                         5                                                                               5
                                                                   ours                                                                                                                                              ours
                                                                   MH                                                                                                                                                MH
                  4                                                                         4                                                                               4

agreement




                                                                                agreement




                                                                                                                                                                agreement
                  3                                                                         3                                                                               3

                  2                                                                         2                                                                               2
                                                                                                   ours
                                                                                                   MH
                  1                                                                         1                                                                               1
                             0.4           0.6           0.8                                        0.4        0.6                       0.8                                       0.4          0.6            0.8
                                     target factuality                                                    target factuality                                                                target factuality
         (a) Completeness | non-abstaining.                                                     (b) Fluency | non-abstaining.                                               (c) Helpfulness | non-abstaining.
Figure 5. Breakdown of the FActScore Likert results from Figure 2 (panel b) per statement that the judge is
asked to rate its agreement with: (a) whether the biography covers the most important facts a reader would
expect to find in a short biography; (b) whether the biography reads as coherent prose with smooth transitions
and no abrupt or disjointed jumps; and (c) whether this would be a satisfactory and helpful answer if a user
asked for a short biography of the entity. The main-text Likert score is the per-output average over these three.
Conditioned on non-abstention; averaged over 10 splits; shaded area shows 95% CI.


                       1.0                                                                                                                         1.0     ours | elicit                 MH | elicit
                                                                                                                                                           ours | logprob                MH | logprob
                       0.8                                                                                                                         0.8




                                                                                                                         hallucination-free rate
empirical factuality




                       0.6                                                                                                                         0.6

                       0.4                                                                                                                         0.4

                       0.2         ours | elicit               MH | logprob                                                                        0.2
                                   ours | logprob              y=x
                                   MH | elicit
                       0.0                                                                                                                         0.0
                                     0.4                0.6                   0.8                                                                            0.4                    0.6                 0.8
                                                    target factuality                                                                                                           target factuality
                               (a) Target vs. observed factuality.                                                                                 (b) Strict factuality of non-abstaining outputs.
Figure 6. Scorer-elicitation ablation on FActScore: confidence-rating elicitation (main text) vs. raw token
log-probabilities. Averaged over 10 splits; shaded area shows 95% CI.



gather generations from Llama-3.1-8B-Instruct [Grattafiori et al., 2024], which we then score using
GPT-4o-mini instead of GPT-4o. We fix the rest of the experimental setting as in Section 4.
As one can observe, validity is agnostic to the capacity of the base model and the scorer, while
downstream utility can be affected somewhat, especially at higher target rates. Overall, however,
these differences are small, indicating that calibrated factuality successfully translates to downstream
utility.

                       1.0                                                                                                                         1.0     ours | 4o                     MH | 4o
                                                                                                                                                           ours | 4o-mini                MH | 4o-mini
                       0.8                                                                                                                         0.8
                                                                                                                         hallucination-free rate
empirical factuality




                       0.6                                                                                                                         0.6

                       0.4                                                                                                                         0.4

                       0.2         ours | 4o                   MH | 4o-mini                                                                        0.2
                                   ours | 4o-mini              y=x
                                   MH | 4o
                       0.0                                                                                                                         0.0
                                     0.4                0.6                   0.8                                                                            0.4                    0.6                 0.8
                                                    target factuality                                                                                                           target factuality
                               (a) Target vs. observed factuality.                                                                                 (b) Strict factuality of non-abstaining outputs.
Figure 7. Model capacity ablation on MATH: GPT-4o vs. GPT-4o-mini scoring, all on Llama-3.1-8B-Instruct
generations (in contrast to the larger Llama-3.3-70B-Instruct used elsewhere). Averaged over 10 splits; shaded
area shows 95% CI.



                                                                                                             21
D.4                          Ablating β at M = 20 with fixed-budget rejection sampling

This appendix probes how our finite-particle guarantee for rejection sampling (Lemma 3.3 and
Corollary 3.4) interacts with β and a fixed-budget rejection sampling deployment procedure. We fix
M = 20 as in the main experiments, but at deployment we run rejection sampling up to a hard cap of
50 attempts; if a non-abstaining, non-accepted generation has not been reached within this budget,
we return a fallback sample. We consider two fallback choices that intuitively give upper and lower
bounds on the unknown behavior of the true mixture posterior:

                             • Worst-case fallback: a synthetic sample consisting of a single claim which is incorrect but
                               has a score 1.0, contributing maximally to the risk estimate. This deliberately pessimistic
                               view assumes that every budget-exhausted prompt would produce a fully false, accepted
                               output.
                             • Abstention fallback: when the budget is exhausted, the abstain response is determinis-
                               tically sampled. Since this contributes zero to the loss/risk estimate, this is an optimistic
                               view motivated by the observation that the mixture prior would have eventually emitted an
                               abstention had we kept drawing. This fallback would also likely be the choice of practition-
                               ers using budget-constrained sampling techniques, especially in deployment settings where
                               abstention is favored over returning a possibly incorrect generation.

We contrast these two fallbacks as the true behavior under indefinite rejection sampling lies somewhere
between the two. By comparing the two, we can thus get a sense of how far the asymptotic guarantee
of Corollary 3.4 can be from being empirically valid at M = 20 under different values of β. However,
note that fully characterizing the precise support of the posterior is not possible with finite sample
sizes; these fixed-budget fallbacks only give a coarse and loose approximation.

                       1.0                                                                       1.0                                               1.0   ours | =0.001           ours | =0.2
                                                                                                                                                         ours | =0.01            MH
                                                                                                                                                   0.8   ours | =0.1
                       0.8                                                                       0.8
empirical factuality




                                                                          empirical factuality




                       0.6                                                                       0.6                                               0.6

                       0.4                                                                       0.4                                               0.4

                       0.2    ours | =0.001           ours | =0.2                                0.2   ours | =0.001           ours | =0.2         0.2
                              ours | =0.01            MH                                               ours | =0.01            MH
                              ours | =0.1             y=x                                              ours | =0.1             y=x                 0.0
                       0.0                                                                       0.0
                               0.4                0.6               0.8                                 0.4                0.6               0.8          0.4                0.6               0.8
                                              target factuality                                                        target factuality                                 target factuality

(a) Target vs. observed factuality (worst- (b) Target vs. observed factuality (ab- (c) Calibrated threshold τ̂ (does not de-
case fallback).                            stention fallback).                     pend on the fallback).
Figure 8. Fixed-budget rejection-sampling β-ablation on FActScore. (a, b) Target vs. empirical factuality under
the worst-case (fully-false) and abstention fallbacks; (c) Calibrated τ̂ vs. target (identical for both fallbacks,
since calibration is unaffected). Averaged over 10 splits; shaded area shows 95% CI.

Calibration validity. Figures 8a and 8b show target factuality 1 − α against observed factuality
on the held-out test split for different values of β, under the worst-case and abstention fallbacks
respectively. At a relatively low calibration budget of M = 20, as β ↓ 0 the calibration guarantee
begins to fall apart under the worst-case fallback, yielding undercalibrated responses at high targets
due to an increasing fraction of prompts hitting the budget cap; at β = 0.1 and β = 0.2, coverage is
empirically valid and tight. These correspond to prompts for which the language model has a hard
time generating responses that pass the scorer threshold. We conjecture that with a reliable scorer, we
would eventually return an abstention particle, but this is impossible to verify under this sampling
design. Under the abstention fallback, by contrast, coverage holds across the whole range of β.
Proxy metrics. Figure 9 reports two factuality proxy metrics from the main experiments, evaluated
under the fixed-budget rejection-sampling procedure rather than the analytic plug-in, again under
both fallbacks. Under the worst-case fallback, the proxy metrics degrade as calibration fails at
low β, mirroring the calibration plots. Under the abstention fallback, both strict factuality among
non-abstaining samples and claim precision remain high across the whole range of β, since the
budget-exhausted prompts do not affect the metrics. Generally speaking, except for in the instances
of worst-case fallback-induced miscalibration, lower β leads to a closer gap in strict factuality among
non-abstaining samples; this is because a lower forced probability of abstention in the mixture prior
yields higher values of τ̂ (Figure 8c), thus applying stricter checks on the outputs.


                                                                                                                        22
                          1.0   ours | =0.001           ours | =0.2                                   1.0   ours | =0.001           ours | =0.2                            1.0                                                                 1.0
                                ours | =0.01            MH                                                  ours | =0.01            MH
                                ours | =0.1                                                                 ours | =0.1
                          0.8                                                                         0.8                                                                  0.8                                                                 0.8




hallucination-free rate




                                                                            hallucination-free rate




                                                                                                                                                         claim precision




                                                                                                                                                                                                                             claim precision
                          0.6                                                                         0.6                                                                  0.6                                                                 0.6

                          0.4                                                                         0.4                                                                  0.4                                                                 0.4

                          0.2                                                                         0.2                                                                  0.2   ours | =0.001           ours | =0.2                           0.2   ours | =0.001           ours | =0.2
                                                                                                                                                                                 ours | =0.01            MH                                          ours | =0.01            MH
                                                                                                                                                                                 ours | =0.1                                                         ours | =0.1
                          0.0                                                                         0.0                                                                  0.0                                                                 0.0
                                 0.4                0.6               0.8                                    0.4                0.6               0.8                             0.4                0.6               0.8                            0.4                0.6               0.8
                                                target factuality                                                           target factuality                                                    target factuality                                                   target factuality

(a) Strict fact. | non-abst. (b) Strict fact. | non-abst. (abst. (c) Claim precision (worst- (d) Claim precision (abst. fall-
(worst-case).                fallback).                          case).                      back).
Figure 9. Proxy metrics under the fixed-budget rejection sampling procedure on FActScore, comparing the
worst-case (fully-false) and abstention budget-exhausted fallbacks.


E                               Prompts

E.1                             Generation prompts

We do not set a special system prompt for generation; the dataset-specific prompts below are passed
as the user’s first turn.
FActScore.

                                         You are a helpful assistant that writes biographies. You will be given the name of a well-
                                         known entity, such as a historical figure, scientist, artist, or music group. Write a concise
                                         biography of that entity. Include only facts you are confident are correct, and omit details
                                         you are uncertain about. Brief biographies are fine, do not pad with guesses. Keep each
                                         sentence focused on a single fact. Prefer short, atomic sentences over long sentences with
                                         multiple clauses.
                                         Example:
                                         Tell me a bio of Albert Einstein.
                                         Albert Einstein was a famed physicist. He was born in Germany in 1879. Einstein is best
                                         known for developing the theory of relativity. He published the equation E=mc2 in 1905. In
                                         1921, he won the Nobel Prize in Physics. He died in 1955.
                                         Now:
                                         Tell me a bio of {entity}.

Where the entity is the entity’s name, as given in the dataset.
MATH.

                                         You are a mathematical reasoning assistant. Solve problems step by step in a concise manner.
                                         IMPORTANT: Use exactly one sentence per ATOMIC logical reasoning step, NEVER chain
                                         more than one step in a sentence. Only include reasoning steps which you are confident are
                                         correct.
                                         Example:                                √
                                         Problem: Find the value of x such that x + 7 = 9.
                                         Solution:
                                         We need to solve for x where the square root of (x + 7) equals 9.
                                         Squaring both sides gives x + 7 = 81.
                                         Subtracting 7 from both sides yields x = 74.
                                         We verify: sqrt(74 + 7) = sqrt(81) = 9.
                                         Therefore, x = 74.
                                         Now solve:
                                         Problem: {raw_prompt}
                                         Solution:

Where the raw_prompt is the textual specification of the problem, as given in the dataset.

E.2                             Data labeling prompts

FActScore. The biography is segmented into one claim per line and the entity’s Wikipedia article is
included in-context as the source of truth.


                                                                                                                                                        23
         [TASK DESCRIPTION]
         You are a fact-checking assistant, assessing a biography written about a notable person or
         entity. You will be supplied the name of the entity, a Wikipedia article about that entity, and
         a biography. The biography consists of a series of claims, conversational remarks or other
         statements, given line by line.
         Your task is to classify each line following these guidelines:
            • true: The line makes one or more factual claims about the entity, and EVERY claim is
              supported by the Wikipedia article.
            • false: The line makes one or more factual claim about the entity, but AT LEAST ONE
              claim is contradicted by the Wikipedia article.
            • neutral: The line is purely conversational or otherwise does not make any factual
              claims about the requested entity.
            • refusal: The line professes ignorance about the entity on the speaker’s part, it expresses
              that the speaker is uncertain about who the name might be referring to, or the speaker
              is indicating that they do not have enough information to say which one out of multiple
              entities is being referred to.
         IMPORTANT: All lines containing factual claims about the entity MUST be evaluated as
         either ‘true’ or ‘false’.
         [ENTITY] {entity}
         [WIKIPEDIA ARTICLE] {wikipedia_content}
         [BIOGRAPHY TO EVALUATE] {claims_text}
         [RESPONSE FORMAT] You must return an answer which follows the given JSON schema,
         with exactly N annotations, one for each line in order.

MATH.
        You are evaluating a mathematical proof/solution.
        Problem: {problem}
        Reference solution: {reference_solution}
        Generated solution steps to annotate (claims start with [CLAIM #]):
        {claims_text}
        For each step, classify as:
            • true: If the step is a mathematically correct derivation, assuming the previous steps
              are correct. Claims can be true without significantly advancing the proof.
            • false: If the step contains an error, or contradicts the previous steps.
            • neutral: use for neutral claims. For instance when all of the claims in the output
              together are expressing uncertainty or inability to solve the problem (e.g. “I am not
              able to solve. . . ”), label each one of them as neutral. Use neutral too for steps that are
              exclusively filler text (e.g. “Let me answer this for you. . . ”).
         Also determine:
            • complete: Does the proof reach a final answer AND is the final answer correct
              (matches reference)?
         IMPORTANT: You MUST return exactly N annotations, one for each step in order.

E.3   Score function prompts

We here list the prompts corresponding to the full-response elicitation strategy, that is the strategy
described in Section 2.4. We also give the prompt used for the alternative logprob-based score
function used in Appendix D.3.
FActScore (full-response elicitation).

         You will be given a context (e.g., a question) and a statement made in response to that
         question. Your job is to rate this statement on a scale from 0.0 to 1.0. The score should
         represent your confidence in the claims made by the statement, where a 1 is obvious facts
         and results like ‘The earth is round’ and ‘1+1=2’. A 0 is for claims that are objectively false,
         like “the earth is flat”. On the other hand, if you’re unsure, you should assign probabilities
         that are strictly in between 0 and 1. If the statement is not a factual claim (e.g., “I don’t
         know”, “I cannot answer that”, “I’m sorry but. . . ”, questions, or expressions of uncertainty),
         assign a score of 1.0 since these are not false claims. You may think out loud first, but you


                                                       24
          MUST end your response with “Score: X.XX” where X.XX is a number between 0.0 and
          1.0.
          ### The context:
          {prompt}
          ### Previously accepted facts (assume these are correct):
          {prior_claims}
          ### The statement:
          {new_claim}
          ### Your response:

MATH (full-response elicitation).
          You are evaluating a step in a mathematical derivation.
          You are given:
            1. A math problem
            2. Previous reasoning steps S
            3. A new step C
          Give your best estimate of the probability that the new step C is true, using S as context. In
          other words, you should estimate P(C correct | S). Rate your confidence on a scale from 0.00
          to 1.00, and make sure your uncertainty estimates are calibrated, meaning, that the average
          rate of correctness should correspond to your prediction, conditional on your prediction.
          Reserve 1.00 for claims you are certain are correct, except for:
             • If the step is not a mathematical claim (e.g., “Let me think. . . ”, “I’ll solve this by. . . ”),
               assign 1.00.
             • Similarly, if the step is an abstention (e.g. “I do not know how to solve this”), assign
               1.00.
          Important: return confidence to two decimal digits!
          Think briefly, then end with “Score: X.XX” where X.XX is between 0.00 and 1.00.
          ### Math Problem:
          {prompt}
          ### Previous steps (assume correct):
          {prior_claims}
          ### New step to evaluate:
          {new_claim}
          ### Your evaluation:

MATH (logprob elicitation).
          You are evaluating a step in a mathematical derivation. Reply with only a single letter. You
          will get a list of prior claims, and a new step. Reply:
             • Y = Yes: The step is mathematically valid given the prior steps.
             • N = No: The step contains an error or contradicts the previous steps.
             • C = Conversation: the step is not a mathematical claim (e.g., “Let me think about this
               carefully.”, “I’ll try a different approach.”) OR an expression of uncertainty (“I’m not
               sure about this.”, “I don’t know how to solve this problem.”).
          Reply with exactly one letter: Y, N, C.
          Problem: {prompt}
          Prior steps:
          {prior_claims}
          New step: {new_claim}

E.4     Downstream evaluation prompts

E.4.1    FActScore: Likert scale
System prompt.
          You are a careful, impartial judge rating short encyclopedia-style biographies. For each
          statement below, indicate your level of agreement on a 1-5 scale: 1 = strongly disagree, 2 =
          disagree, 3 = neither agree nor disagree, 4 = agree, 5 = strongly agree.


                                                          25
User prompt.
        Rate the following biography of {entity} on three independent axes.
        For each statement, return an integer from 1 (strongly disagree) to 5 (strongly agree):
          1. completeness: “The biography covers the most important facts about {entity}, as
             one would expect to find in a short biography.”
          2. fluency: “The biography reads as coherent prose: sentences flow smoothly into one
             another, with no awkward phrasing, abrupt transitions, redundancy, or disjointed jumps
             between unrelated points.”
          3. helpfulness: “If a reader asked for a short biography of {entity}, this would be a
             satisfactory and helpful answer.”
        Biography:
        """
        {text}
        """

E.4.2   MATH: Completeness
We re-use the data labeling prompt from Appendix E.2. The downstream evaluation only consumes
the complete field, discarding the rest of the output.




                                                    26
