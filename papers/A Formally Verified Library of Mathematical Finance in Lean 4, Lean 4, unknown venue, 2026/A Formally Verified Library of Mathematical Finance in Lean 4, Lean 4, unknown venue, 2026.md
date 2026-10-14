                                              A Formally Verified Library of Mathematical Finance in
                                                                      Lean 4
                                                                                      Raphael Coelho*

                                                                                          July 2026



                                                                                           Abstract
                                                      We describe a library of mathematical finance built in the Lean 4 proof assistant, on top
                                                  of Mathlib and the BrownianMotion package. It is broad: more than three hundred sorry-free
                                                  theorems across eleven areas, from the measure-theoretic foundations of continuous-time
                                                  stochastic calculus through derivative pricing to applied risk, portfolio, and fixed-income
arXiv:2606.01356v3 [q-fin.MF] 18 Jul 2026




                                                  theory. To our knowledge it is the most comprehensive machine-checked development
                                                  of mathematical finance to date. Two things make it more than a catalogue. It reaches
                                                  into the continuous theory far enough to construct the L2 Itô integral as a bounded linear
                                                  isometry and to derive, rather than assume, the risk-neutral pricing measure. And it
                                                  audits its own faithfulness: every result is classified by how its Lean statement relates
                                                  to the mathematics it claims, and a build-enforced gate pins the axioms each proof
                                                  actually uses, so a reader can see precisely what has been proved and what has only
                                                  been proved under added hypotheses. We close with a finding: a formal base over classical
                                                  financial mathematics yields certified unification of known results rather than new financial
                                                  theory. The contribution is therefore methodological and infrastructural (reusable verified
                                                  foundations for mathematical finance, together with the faithfulness audit above), not a
                                                  new financial result.


                                            1 Introduction

                                            Interactive theorem provers have moved, over the last decade, from isolated landmark proofs
                                            to broad, reusable libraries. Mathlib [9] now carries a substantial measure-theoretic probability
                                            development (conditional expectation, martingales, the Radon–Nikodym theorem, Doob’s
                                            theorems) and recent work has begun to build continuous-time stochastic processes on top of
                                            it, including a dedicated BrownianMotion package [2]. Mathematical finance sits directly on
                                            this foundation: arbitrage-free pricing, the Black–Scholes model [1], the fundamental theorem
                                            of asset pricing [5], risk measurement. Almost none of it has been formalized.
                                                 What exists is narrow. Echenim and Peltier formalized the discrete Cox–Ross–Rubinstein
                                            (CRR) model [3] and market completeness in Isabelle/HOL [4], within a single model.
                                            Pusceddu and Bartoletti formalized constant-product automated market makers in Lean 4 [11].
                                            Most recently, Nagy gave one machine-verified derivation, “from Itô to Black–Scholes,” in
                                            Lean 4 [10], a focused vertical that, on the author’s own account, leaves the continuous Itô
                                            integral structurally verified rather than constructed. Each is deliberate and self-contained.
                                            None is comprehensive, and none offers a way to state how faithful a formalization is to the
                                            mathematics it claims.
                                              * Independent researcher. ORCID: 0009-0001-6601-1023. Correspondence: raphaelrrcoelho@gmail.com. Arti-
                                            fact: https://github.com/raphaelrrcoelho/formal-mathfin.




                                                                                               1
    This paper presents such a development. The library spans eleven areas. The continuous-
time stochastic-calculus foundations supply Brownian-motion martingales, the Wiener and
Itô L2 isometries, quadratic variation, a continuous Itô integral, the L2 Itô formula for C3
functions (with a two-dimensional case), and a Feynman–Kac link. The no-arbitrage pricing
foundations add the fundamental theorem of asset pricing, state prices, pricing kernels, the
convex pricing functional, and static Girsanov. On these rest Black–Scholes pricing (the call
and put formulas and their Greeks; digital, power, exchange, and Bachelier options; the pricing
PDE from Itô; Breeden–Litzenberger); the binomial model (CRR pricing and replication,
the binomial-to-Black–Scholes scaling limit, American options via the Snell envelope, the
reflection principle); and the applied layers: futures (Black-76, swaptions), fixed income
(Vasicek, duration and convexity, immunization, reduced-form and structural credit), portfolio
theory (Markowitz, the CAPM, Black–Litterman, risk parity), performance measurement,
risk measures (coherence, spectral measures, CVaR), actuarial mathematics, and DeFi. As of
writing this is 330 theorems (298 classified full, 18 library_wrapper, 14 reduced_core) over
roughly 52,300 lines of Lean, all sorry-free.
    No individual theorem here is new; the mathematics is classical throughout. The contribu-
tion is the development as a whole, along the two axes the prior art leaves open: it constructs
the continuous Itô integral that earlier efforts assume or sketch, and it makes the faithfulness
of each formalization machine-checkable. The second axis has a concrete payoff. Because
every result carries an audited statement, the library can certify when two independently built
modules denote the same mathematics: the N-asset Markowitz portfolio variance and the
Herfindahl concentration index, for one (portfolioVarN_diag_eq_herfindahl). Unifications
of this kind are what a formal base over classical theory produces: certified structure within
mathematical finance, not new financial theory.

2 Contributions

  1. Scope (§3, §7). To our knowledge the broadest formalization of mathematical finance in
     any proof assistant, measured in breadth: eleven areas and more than three hundred
     sorry-free theorems on one coherent foundation, with uniform conventions and cross-
     module reuse (the principle-based design of Section 4).

  2. A faithfulness-audit methodology (§4, §7), the most transferable contribution. Every
     theorem is classified by how its Lean statement relates to the mathematical claim: full
     (the statement is the claim), library_wrapper (a thin re-export), reduced_core (the
     claim holds, but under an added hypothesis or with an axiomatized sub-step), and
     placeholder. Delivery claims count only full and library_wrapper. A build-enforced
     gate backs the classification: AxiomAudit.lean pins, for every load-bearing theorem, the
     exact #print axioms output, so the library fails to compile if any audited result picks
     up an unexpected axiom, sorryAx above all. Formalization papers often leave implicit
     the gap between “we proved X” and “we proved a weaker X under added hypotheses”;
     this work makes it explicit and checkable, and another project could adopt the scheme
     wholesale.

  3. Depth beyond the prior formalizations. Three results reach past what earlier work
     constructs; Sections 5 and 6 develop the first two, and the third is proved here, its
     explicit-constant refinement deferred to a companion paper.

        • The continuous L2 Itô integral as a bounded linear isometry on [0, T ] (itoIntegralCLM_



                                               2
                    RT
            T), with 0 B dB = 21 BT2 − B02 − T as its worked capstone, the object Nagy’s deriva-
                                              

            tion reaches and leaves structurally verified (§5).
          • The risk-neutral measure derived, not assumed, by a static Girsanov change of
            measure, which turns the pricing hypothesis BSCallHyp into a theorem (BSCallHyp.
            exists_of_physical) (§6).
          • The binomial-to-Black–Scholes scaling limit, machine-checked end to end (binomialPrice_
            call_tendsto_bs) by a characteristic-function / Lévy-continuity argument that
            routes through put-call parity to avoid the uniform-integrability obstruction. A non-
            asymptotic, explicit-constant refinement, the project’s one bid for a new quantitative
            result, is the subject of a separate paper, aimed at a computational-finance venue.

   4. An honest map (§3, §7). We mark the reduced_core frontier precisely, report the lemmas
      contributed back to Mathlib and BrownianMotion, and state the certified-unification
      finding above as a result.

3 Related work and positioning

Formalized finance has, to date, appeared mostly at formal-methods venues rather than in the
mathematical-finance literature. We offer this work to mathematical finance directly: a verified
library is shared infrastructure for the field, whatever the novelty type of any individual
theorem. The nearest precedents compare as in Table 1.

                        this work                        Nagy (2026)                Echenim–Peltier
                                                                                    (2017)
 prover                 Lean 4                           Lean 4                     Isabelle/HOL
 scope                  11 areas, 330 theorems           one derivation (Itô→BS)    one model (CRR) +
                                                                                    completeness
 continuous Itô inte-   constructed                      structurally verified      n/a
 gral
 risk-neutral measure   derived              (Gir-       derived (two-state FTAP)   assumed
                        sanov/Esscher)
 faithfulness audit     yes (4-tier + axiom gate)        n/a                        n/a

             Table 1: This work against the nearest formalized-finance precedents.

    Nagy’s derivation [10] (SSRN 6336503, 2026) is the closest precedent, and one we build on di-
rectly: three modules (Foundations/DiscreteIto.lean, FTAPTwoState.lean, ItoLemma.lean)
adapt its discrete-Itô, two-state-FTAP, and structural-drift framework, with attribution in their
headers. Where Nagy machine-checks a single Itô-to-Black–Scholes path and, on his own
account, stops at the continuous Itô integral, this library constructs that integral and sets the
same derivation inside a comprehensive, audited development.
    Echenim and Peltier’s Isabelle/HOL formalization [4] is the established precedent for
formalized pricing, and the natural baseline for the derive-versus-assume axis. Their frame-
work takes the risk-neutral pricing setup as given; here it is derived, by the static Girsanov
construction of Section 6. The library also builds the Wiener/Itô L2 layer their discrete setting
has no need for, and adds the faithfulness audit.
    Pusceddu and Bartoletti [11] give a focused Lean 4 formalization of constant-product AMM
mechanics. The library’s DeFi module re-implements these invariants over R and is included
for breadth of coverage, not as a contribution; we claim nothing new in AMMs.



                                                     3
   Mathlib and Degenne’s BrownianMotion are the upstream foundation. The library con-
sumes Mathlib’s measure theory, conditional expectation, martingales, and Gaussian machin-
ery [9], and the BrownianMotion package’s pre-Brownian-motion infrastructure [2]; Section 7
reports the lemmas it contributes back.

4 Architecture: the principle-based design

The library stays coherent by deriving results from a few reusable principles rather than
re-proving each instrument from scratch. Three carry the pricing content, and a fourth,
cross-cutting discipline binds the whole.
    The first principle is a linear no-arbitrage pricing functional: pricing is modelled as a non-
negative linear functional on payoffs (Foundations/StatePrices.lean, PricingKernel.lean,
ConvexPricingFunctional.lean, NoArbitrageDerivations.lean). Linearity and non-negativity
already yield put-call parity, the forward price, and convexity of the call in its strike. Results
elsewhere proved instrument by instrument become corollaries of this one structure.
    The second is the Garman normal form. Every price in the Black–Scholes family has the
form A · Φ(d1 ) − K · DF · Φ(d2 ) (BlackScholes/GarmanNormalForm.lean); the call, put, digital,
power, exchange, dividend, and foreign-rate variants are instances, fixed by the choice of A, the
discount factor DF, and the effective volatility. Margrabe’s exchange-option formula [8] is one
such instance (ExchangeOption.lean, MargrabeGrounding.lean), not a separate derivation.
    The third is the Brownian-motion grounding bridge. Pricing hypotheses are stated
marginally (BSCallHyp asks only that the terminal asset be lognormal under Q), but BSCallHypFromBrownian.l
and PricingFromBrownian.lean show they follow from a pre-Brownian motion in the BrownianMotion
package. Through these bridges the flagship prices connect back to the continuous-time object.
    The fourth, the cross-cutting discipline, is the faithfulness gate. The four-tier classification
(Section 2) and the AxiomAudit.lean axiom pins are build artifacts, not documentation:
promote a theorem to full without an honest derivation, or let one acquire sorryAx, and the
build fails. The clearest products of this discipline are the certified cross-domain bridges in
Bridges/. Two modules built for different purposes turn out to denote the same mathematics:
the N-asset Markowitz variance with diagonal covariance equals the Herfindahl index scaled
by the common variance (portfolioVarN_diag_eq_herfindahl), and the actuarial survival
function coincides with the reduced-form credit survival function (survivalFromForce_eq_
hazardSurvival, which holds by rfl). Each is a machine-checked identity between definitions
developed independently.
    Accept the no-arbitrage functional, the Garman form, and the Brownian grounding, and
most of the library’s pricing content follows. The trusted core stays small.

5 The continuous Itô layer

The library’s depth comes from carrying stochastic integration to a genuine Itô integral, the
foundation earlier formalizations assume or sketch. It is built in stages.
    The Wiener integral for deterministic integrands is an L2 isometry (WienerIntegralL2.lean).
Random, adapted integrands are the real step, and the adapted Itô isometry (ItoIsometryAdapted.lean)
takes it: the cross terms E[ φ j ∆Bj · φk ∆Bk ] vanish by the weak Markov property of Brownian
increments, not by deterministic orthogonality. That is the distinction between Itô and Wiener
integration. From the isometry on simple adapted processes, a π–λ density argument and a
norm-preserving extension (LinearMap.extendOfNorm) produce the continuous Itô integral as
a bounded linear map on L2 ([0, T ]) (ItoIntegralL2.lean, ItoIntegralCLM.lean). Its worked
             RT
capstone is 0 B dB = 12 BT2 − B02 − T (ItoIntegralBrownian.lean).
                                          


                                            4
    The rest of the stochastic-calculus core surrounds this: the quadratic variation of Brownian
motion in L2 , with its exact mean-square rate (QuadraticVariationL2.lean); the integral
as a continuous L2 martingale; Itô’s formula for C3 functions with bounded derivatives, in
autonomous and time-dependent forms, and, by localization at exit times, in the unrestricted
C3 class, where the compensated residual is a continuous local martingale (ito_formula_
unrestricted); the pathwise continuous local martingale on the half-line; and a Feynman–Kac
/ heat-equation link (FeynmanKacHeatEquation.lean). All are axioms-clean.
    This is the point Nagy identifies as the natural stopping line for the Itô-to-Black–Scholes
derivation; here the integral is constructed. The continuous integral is foundational infras-
tructure, and the pricing modules reach the continuous-time world through the marginal
grounding bridge of Section 4, not by integrating against itoIntegralCLM_T. The companion
paper [6] develops the full construction and the pathwise theory in detail.

6 Deriving the risk-neutral measure

In most treatments, and in the earlier formalized CRR work, the equivalent martingale measure
is assumed: one posits a Q under which the discounted asset is a martingale, and prices as a
Q-expectation. Here it is derived. GaussianGirsanov.lean performs a static Girsanov change
of measure by an Esscher density: from the physical law of the Gaussian driver it produces a
measure under which the terminal asset has exactly the lognormal law the pricing formulas
need. So BSCallHyp (the hypothesis that the terminal asset is lognormal under Q, which the
Black–Scholes section takes as input) is itself a theorem (BSCallHyp.exists_of_physical),
and the discounted asset is a proven Q-martingale (ContinuousFTAP.lean, discountedGBM_
isMartingale).
    The change of measure is not only static. Girsanov’s theorem is formalized dynamically
as well, along a ladder of admissible
                             Rt         drifts: for θ constant, simple, continuous-adapted, and
bounded-predictable, Bt + 0 θs ds is a Q-Brownian motion under the exponential-martingale
measure (GirsanovConstantTheta.lean through GirsanovPredictableTheta.lean). And
the derived measure carries an operational consequence: on a continuous market an equivalent
martingale measure precludes arbitrage against simple predictable strategies (ContinuousMarket.lean,
isEMM_noArbitrageSimple), with the discounted geometric Brownian motion the worked in-
stance. This is the forward, model-agnostic half of the first fundamental theorem in continuous
time; its converse is the no-free-lunch theorem of Delbaen and Schachermayer, which the
library does not reach.
    The derivation pays off twice. The Black–Scholes call price stops being conditional on an
assumed measure: composed with it, the formula becomes a statement about the physical
model (bs_call_formula_of_physical). And Margrabe’s exchange-option formula follows
from the same change of numéraire (ExchangeOption.lean, MargrabeGrounding.lean) rather
than a fresh derivation.
    This derive-don’t-assume stance is the second way the library moves past the established
formalized-pricing baseline (Section 3). Its fundamental-theorem-of-asset-pricing results reach
the equivalent martingale measure by constructions matched to each setting: a Hahn–Banach
separation in the finite-state multi-period model (ftap_discrete), and, in the general one-
period model for one asset and for d assets, the minimisation of a smooth convex (softplus)
potential whose logistic weight is the density (ftap_one_period, ftap_one_period_vector);
the general multi-period case is the open rung.




                                               5
7 Evaluation and contributed lemmas

The faithfulness tiers come from the coverage_report tool: the benchmark suite tracks 330
theorems, classified as in Table 2.

      tier                                                                           count
      full: the statement is the mathematical claim                                    298
      library_wrapper: thin re-export of an upstream result                             18
      reduced_core: holds under an added hypothesis / axiomatized sub-step              14
      placeholder                                                                        0

             Table 2: Faithfulness classification of the 330 benchmark theorems.

    That is 316 of 330 delivery-claim-ready. The reduced_core items cluster in the continuous-
time and discrete-process benchmarks rather than in the pricing layer: the mathematical-finance
benchmark, by far the largest, is almost entirely full. The library is most faithful where
the mathematics is classical and elementary, and its partial cores sit at the genuinely hard
continuous-time frontier, the honest map the methodology is built to produce.
    The build is itself the evidence. A plain lake build from the repository root compiles the
whole library (some 250 modules on the pinned image), ending with AxiomAudit.lean and
Examples.lean. AxiomAudit.lean is that gate (its mechanism is described in Section 2); its
compilation is machine-checked evidence that the audited results are sorry-free and rest only
on Lean’s three standard axioms (propext, Classical.choice, Quot.sound).
    For reproducibility, Lean v4.31.0 [7], Mathlib fabf563a, and the BrownianMotion package
bdf5ea0c are pinned in lean-toolchain and lake-manifest.json; the library is about 52,300
lines; a pinned Docker image (ghcr.io/raphaelrrcoelho/mathfin-verify) reproduces the
build.
    Some of this work has fed back upstream. The stochastic time-interval API the early
development needed is now part of the upstream BrownianMotion package. The Gaussian-tail
and completing-the-square integral lemmas the pricing proofs needed, which Mathlib lacked,
were developed in the library.

8 Conclusion

This library is, to our knowledge, the most comprehensive machine-checked development of
mathematical finance to date, but its two real contributions are not its size. They are its depth,
a constructed continuous Itô integral and a derived risk-neutral measure, and the faithfulness
audit that makes every claim’s logical status checkable.
    What the library is not is equally part of the point. Machine-checking classical financial
mathematics yields certified unification of known results, not new financial theory; the
contribution is methodological and infrastructural, a verified foundation for mathematical
finance. The tier classification and the axiom gate make that honesty checkable, which is itself
part of the contribution.
    The continuous Itô integral is developed in detail in a companion paper [6]; further
companion papers will develop the static-Girsanov derivation of the risk-neutral measure and
a non-asymptotic, explicit-constant bound for the binomial-to-Black–Scholes convergence. The
open frontier is the natural next layer for a community library: the general multi-period Dalang–
Morton–Willinger theorem and its continuous-time Delbaen–Schachermayer counterpart, the
fully general (progressively measurable) Girsanov change of measure, and the handful of
results still classified reduced_core.


                                                6
References

 [1] F. Black and M. Scholes. The pricing of options and corporate liabilities. Journal of Political
     Economy, 81(3):637–654, 1973.

 [2] R. Degenne et al. brownian-motion: a Lean 4 development of Brownian motion. https:
     //github.com/RemyDegenne/brownian-motion, 2024–2026.

 [3] J. C. Cox, S. A. Ross, and M. Rubinstein. Option pricing: a simplified approach. Journal of
     Financial Economics, 7(3):229–263, 1979.

 [4] M. Echenim and N. Peltier. The binomial pricing model in finance: a formaliza-
     tion in Isabelle. In Automated Deduction – CADE-26, LNCS 10395. Springer, 2017.
     doi:10.1007/978-3-319-63046-5_33. Extended version: Journal of Automated Reasoning, 63,
     2019, doi:10.1007/s10817-019-09528-w.

 [5] J. M. Harrison and D. M. Kreps. Martingales and arbitrage in multiperiod securities
     markets. Journal of Economic Theory, 20(3):381–408, 1979.

 [6] R. Coelho. A machine-checked Itô calculus for Brownian motion. arXiv:2606.15089, 2026.

 [7] L. de Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In
     Automated Deduction – CADE-28, LNCS 12699, pages 625–635. Springer, 2021.

 [8] W. Margrabe. The value of an option to exchange one asset for another. Journal of Finance,
     33(1):177–186, 1978.

 [9] The mathlib Community. The Lean mathematical library. In Proc. 9th ACM SIGPLAN Int.
     Conf. on Certified Programs and Proofs (CPP 2020), pages 367–381. ACM, 2020.

[10] T. Nagy. From Itô to Black–Scholes: a machine-verified derivation in Lean 4. SSRN preprint
     6336503, 2026. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6336503.

[11] D. Pusceddu and M. Bartoletti. Formalizing automated market makers in the Lean 4
     theorem prover. In 5th Int. Workshop on Formal Methods for Blockchains (FMBC 2024), OASIcs
     118. Schloss Dagstuhl, 2024. doi:10.4230/OASIcs.FMBC.2024.5, arXiv:2402.06064.




                                                 7
