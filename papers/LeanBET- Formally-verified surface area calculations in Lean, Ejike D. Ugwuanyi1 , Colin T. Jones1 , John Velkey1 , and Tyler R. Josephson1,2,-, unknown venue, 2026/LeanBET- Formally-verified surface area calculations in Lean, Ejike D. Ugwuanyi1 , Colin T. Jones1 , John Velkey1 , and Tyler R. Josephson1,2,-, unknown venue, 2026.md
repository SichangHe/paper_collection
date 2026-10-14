                                              LeanBET: Formally-verified surface area calculations in Lean
                                                       Ejike D. Ugwuanyi1 , Colin T. Jones1 , John Velkey1 , and Tyler R. Josephson1,2,*

                                                           1 Department of Chemical, Biochemical, and Environmental Engineering,

                                                               University of Maryland, Baltimore County, Baltimore, MD, USA
                                                                 2 Department of Computer Science and Electrical Engineering,
arXiv:2605.16169v1 [cs.LO] 15 May 2026




                                                               University of Maryland, Baltimore County, Baltimore, MD, USA
                                                                          * Corresponding author, email: tjo@umbc.edu




                                                                                           May 18, 2026


                                                                                               Abstract

                                                   The Brunauer–Emmett–Teller (BET) method is a standard tool for estimating surface areas from ad-
                                               sorption isotherms, yet practical implementations involve multiple algorithmic steps whose correctness
                                               is rarely made explicit. In this work, we present a fully executable and formally verified BET analysis
                                               pipeline implemented in the Lean 4 theorem prover.
                                                   Our formalization covers the complete BET Surface Identification (BETSI)-style workflow, includ-
                                               ing window enumeration, monotonicity checks, knee selection, and linear regression. We carry out
                                               computations in floating-point arithmetic and develop the corresponding correctness proofs over the real
                                               numbers, using a shared polymorphic implementation that supports both. On the proof side, we show that
                                               the regression coefficients returned by the algorithm agree with their specification-level definitions and
                                               minimize the least-squares error under the stated assumptions. We also formalize the algebraic deriva-
                                               tion of the BET linearized expression and connect that result directly to the executable analysis pipeline.
                                               We further prove that the window enumeration is sound and complete, and that the admissibility checks
                                               and knee-based selection satisfy their formal specifications.
                                                   We evaluate the implementation against the BETSI reference method on benchmark adsorption
                                               isotherms. Compared to BETSI, LeanBET agrees to machine precision for 18 of the 19 isotherms,
                                               with only a 0.03% deviation for the UiO-66 dataset. This demonstrates that a scientific computing work-
                                               flow can be built in Lean, yielding both formal verification guarantees and numerical agreement with an
                                               established Python reference implementation.
                                               Keywords: Formal verification, Lean 4, BET surface area, gas adsorption


                                         1.   Introduction

                                         Scientific computing often relies on mathematical models whose derivations are written on paper, while their
                                         implementations are carried out separately in software. This separation can make it difficult to verify that
                                         the final computation faithfully reflects the underlying theory. Formal verification provides a way to address
                                         this problem. It is a method of checking, with machine assistance, that a computation follows from clearly
                                         stated mathematical definitions and logical steps. By expressing both the mathematics and the computation
                                                                                                            2


in a form that can be checked mechanically, formal verification helps bridge the gap between theory and
implementation. In this work, we use derivation as specification. The algebraic development of the BET
adsorption equation is formalized and directly linked to an executable analysis pipeline. We demonstrate
this approach to scientific computing by formalizing the theory behind Brunauer–Emmett–Teller Theory
and its implementation in surface area calculations.
   The Brunauer–Emmett–Teller (BET) theory describes multilayer physical adsorption of gas molecules
on solid surfaces and remains one of the most widely used frameworks for quantifying specific surface
area from adsorption isotherms[1]. In practice, BET analysis is usually carried out by selecting a relative
pressure range, fitting the linearized BET equation over that interval, and extracting the monolayer capacity
and surface area from the resulting regression parameters. Although the method is standard, the final surface
area can depend strongly on the chosen fitting range. As a result, BET calculations that begin from the same
isotherm may still lead to different reported values, reducing reproducibility across users, laboratories, and
software implementations[2][3].
   Despite its longevity and prevalence, BET surface area analysis has long been known to rest on a set
of restrictive assumptions about adsorption behavior[4]. The BET model extends the Langmuir monolayer
adsorption framework to multilayer adsorption, assuming uniform surface sites, non-interacting adsorbate
layers beyond the first, and a constant enthalpy of adsorption for layers above the monolayer[1]. These
assumptions only hold approximately for many real materials, and the BET plot often exhibits linearity
over a narrow and sometimes ambiguous relative-pressure range; hence, selecting an appropriate fitting
region has become a central practical challenge in BET analysis[5]. To mitigate this ambiguity, a set of
consistency criteria frequently attributed to Rouquerol and co-workers and adopted in practice has been used
to help identify valid regions of linearity in BET plots and to exclude unphysical solutions such as negative
monolayer capacities. These criteria include requiring a positive BET constant C, a monotonically increasing
n(1 − P/P0 ) term over the selected range, and that the calculated monolayer coverage corresponds to a
relative pressure within that range [6]. However, even when such criteria are applied, additional subjectivity
remains, because multiple relative pressure intervals may satisfy the same consistency rules. This leaves the
lower and upper bounds of the fitting range unspecified, leading to variability in reported BET areas.
   This subjectivity has profound consequences. In a recent round-robin study involving 61 laboratories
and a shared set of high-quality adsorption isotherms, Osterrieth et al. demonstrated that BET surface
areas calculated from the same data varied widely across laboratories, even when most participants reported
using the consistency criteria in their analysis [3]. For some materials, the highest and lowest reported
BET areas differed by more than a factor of five, highlighting that reproducibility issues arise not from
experimental measurement alone, but also the fitting algorithms and human choices used to interpret that
data. To address this reproducibility crisis, Osterrieth et al. introduced BET Surface Identification (BETSI),
a Python-based computational framework that exhaustively enumerates all consecutive fitting windows on
an isotherm, applies ordinary least-squares regression to each, and filters the resulting candidates using the
Rouquerol criteria to produce an unambiguous BET area assignment [3]. While BETSI substantially reduces
the subjectivity associated with manual fitting, it remains a numerical algorithm implemented in general-
purpose software, leaving open the possibility of hidden implementation assumptions or subtle errors that
could compromise its scientific guarantees.
   In this work, we present a different approach to BETSI-style analysis. Figure 1 provides a schematic
                                                                                                                             3



                                                                                                          Compare        P
                                            Perform linear        Filter out invalid        Obtain
    Adsorption          Linearize the                                                                    result with     A
                                            regression for         fits, and select       surface area                   S
       data               raw data                                                                          BETSI
                                            subsets of data          optimal one           and error      standard       S
 Programming
 Proving                           Proof that linear regression       Rouquerol criteria                 Testing
                                  minimizes least squares error       + selection criteria
                                                                                                         ✔ 18/19 BETSI
                                         Formal proof of BET Theory


                                  follows from a body of assumptions about             Proof linking
     Proof that algebra
                                                                                        output to
     for linearization is
                                                                                        meaningful
           correct
                                                                                       parameters




Figure 1: Overview of the formally verified BET analysis pipeline. The executable algorithm (top row)
transforms adsorption data through BET linearization, windowed linear regression, and BETSI-style filter-
ing to compute surface area and error metrics. Each computational step is paired with a corresponding
formal proof (bottom blocks) establishing algebraic correctness of the BET linearization, least-squares op-
timality of linear regression, and soundness of the selection criteria. Numerical results are finally compared
against the BETSI reference implementation.


overview of the formally verified BET analysis pipeline, illustrating how each executable transformation is
justified by a corresponding mathematical proof. Rather than focusing solely on numerical performance or
agreement with reference values, we develop a verified BETSI implementation in which correctness prop-
erties are formally specified and mechanically verified. The algorithm is implemented in Lean 4 which is
both a programming language and theorem proving system that allows executable code and mathematical
proofs to be written in the same environment [7]. When the algorithm returns a BET fit, Lean provides a
machine-checked proof that the result satisfies the BETSI criteria as mathematically defined. The central
contribution of this paper is therefore not a new BET algorithm, but a formally verified guarantee of correct-
ness. The implementation is designed to be polymorphic, supporting efficient execution using floating-point
arithmetic while enabling proofs over the real numbers. By separating computation from specification and
proving soundness of the executable checks, we demonstrate how formal methods can be applied to a clas-
sical problem in adsorption science without sacrificing practical usability.
    The remainder of this paper is organized as follows. Section 2 reviews the theoretical background of
BET analysis and the BETSI procedure. Section 3 introduces Lean 4 and outlines the design principles used
to integrate executable code with formal verification. Section 4 describes the polymorphic implementation
of BETSI. Section 5 presents the formal specifications and verified soundness of the BETSI algorithm.
Section 6 reports numerical results and comparisons with existing implementations. Finally, Section 7
discusses the conclusions and outlook.
                                                                                                                4


2.     Background

2.1.     BET Theory and Linearization

The Brunauer–Emmett–Teller (BET) method provides a classical framework for estimating the specific
surface area of a solid from gas adsorption isotherms [1]. The method extends the Langmuir monolayer
adsorption model [8] to multilayer adsorption by assuming that adsorption occurs in successive layers and
that, beyond the first layer, the heat of adsorption is equal to the heat of liquefaction of the adsorbate. Bobbin
et al.[9] were the first to rigorously formalize its derivation, encoding it as a machine-verified proof in the
Lean 3 theorem prover, an achievement that clarified precisely which definitions are necessary and sufficient
to imply the adsorption isotherm equation. The model is built on six definitions:

       • The first-layer adsorption rate y = P ·C1 ,

       • The multilayer adsorption rate x = P ·CL ,

       • The BET constant C = y/x,

       • The geometric layer occupancy si = Cxi s0 ,

       • The total adsorbed area A = ∑∞
                                      i=0 si , and

       • The total adsorbed volume V = V0 ∑∞
                                           i=0 i · si .

These definitions require the convergence condition 0 < x < 1, a constraint absent from the original 1938
derivation but essential to the validity of both infinite sums. Under this condition, both series admit closed
forms, and their ratio V /A yields an expression in x and C. Recognising that x = P ·CL is simply the relative
pressure P/P0 when the saturation pressure is identified as P0 = 1/CL , the ratio reduces to the standard
nonlinear BET isotherm,
                                                      C · nm · (P/P0 )
                                     n(P) =                                 ,                                (1)
                                              (1 − P/P0 ) 1 + (C − 1)(P/P0 )
where p = P/P0 is the relative pressure, nm is the monolayer capacity, and C is the adsorption energy
constant. The formal derivation of Equation (1) from these definitions is presented as a machine-checked
theorem in Section 5.3.
       Rearranging Equation (1) into an affine form yields the linearized BET equation,

                                                p      C−1     1
                                                     =     p+     .                                           (2)
                                            n(1 − p)   nmC    nmC

When the BET equation is valid, a plot of p/[n(1 − p)] versus p reveals a linear region from which nm and
C can be recovered by linear regression. Despite the apparent simplicity of this procedure, practical BET
analysis is critically dependent on the identification of an appropriate pressure range over which Equation (2)
holds.

2.2.     Rouquerol Criteria

To reduce ambiguity in the choice of the BET fitting range, the analysis applies a sequence of self-consistency
checks to each candidate pressure window [6]. The four criteria are as follows:
                                                                                                              5


     (i) The quantity n(1 − P/P0 ) must be monotonically non-decreasing over the fitting window.

  (ii) The fitted BET parameters must be physically admissible: C > 0 and nm > 0.

 (iii) The relative pressure corresponding to monolayer coverage, P/P0 nm , must lie within the selected
         fitting window.
                                                                                   √
 (iv) The monolayer pressure predicted analytically by the fitted model, P/P0 = 1/( C + 1), must agree
         with the value read from the isotherm to within a prescribed tolerance of 20%.

       A candidate window is considered valid only if all four criteria are satisfied simultaneously.

2.3.     BETSI Algorithm

The BET Surface Identification (BETSI) approach was developed to address the reproducibility challenges
inherent in BET analysis by providing a fully algorithmic procedure for window selection and evaluation
[3]. Rather than relying on manual inspection or subjective judgment, BETSI systematically enumerates all
admissible pressure windows within an isotherm and applies a sequence of physical and statistical filters to
identify valid BET regions. At a high level, the BETSI procedure consists of the following steps. First, all
contiguous pressure windows containing at least two data points are generated. For each window, the BET
equation is linearized and a least-squares regression is performed. Windows that fail to satisfy the Rouquerol
criteria or that yield physically inadmissible parameters are discarded. For the remaining candidates, the
BET equation is inverted to estimate the pressure corresponding to monolayer coverage, and a relative error
criterion is applied. Finally, among the passing windows, a knee selection strategy is used to identify a
single representative BET fit.
       This approach adds an additional criterion to the four from Rouquerol, to admit a unique solution:

     (v) If several windows satisfy the previous conditions, the final result is chosen from those reaching the
         largest admissible end index, with the percentage error used to break any remaining ties.

       The strength of the BETSI approach lies in its systematic nature and its ability to remove user-dependent
choices from BET analysis. However, as with any numerical algorithm, its correctness ultimately depends
on the faithful implementation of each step and on the interpretation of the underlying criteria. The work
presented here builds on the BETSI methodology by providing a formally verified implementation in which
these correctness properties are explicitly specified and mechanically checked.


3.     Lean 4 Framework and Design Approach

3.1.     Lean 4 as the Formalization Tool

The formal verification work presented in this paper is carried out using the Lean 4 theorem prover [7].
Lean 4 is not only a theorem prover but also an efficient functional programming language, which makes it
possible to develop executable code and machine-checked proofs within the same environment [10]. This
dual role has motivated a growing body of work on verified computation in Lean. For example, SciLean
explores scientific computing workflows in Lean [11], while TorchLean extends this idea to neural-network
                                                                                                              6


models and verification [12]. Earlier, Selsam et al.[13] demonstrated that Lean could be used to implement
and verify core properties of a machine learning system. Our work follows this general direction, but focuses
on adsorption analysis, using Lean to connect the derivation, implementation, and verification of BET-style
surface area computation.
       All results reported in this work were developed using Lean 4, together with the accompanying math-
ematical library Mathlib v4.27.0-rc1. The Lean build system lake was used to manage dependencies
and compilation. The specific Lean version used for this work is Lean 4.27.0, although the design does not
rely on features unique to this release.
       A key advantage of Lean for scientific computing applications is that executable code and mathematical
specifications can be expressed side by side. Numerical algorithms can be written in a style similar to
conventional functional programming, while correctness properties are stated as logical propositions and
proved within the same environment. This avoids the need to translate algorithms into a separate verification
language and reduces the risk of mismatches between code and specification [14][15].

3.2.     Polymorphic Numeric Design

A central challenge in this formalization is that the two roles we need from a numeric representation are
not available in a single type. Floating-point numbers are executable and therefore suitable for running
the BETSI pipeline on real data, but they are not the basis of the mathematical proofs developed here.
Real numbers, by contrast, provide the natural setting for specification and proof, but in Lean they are
noncomputable and therefore not suitable for direct execution of the full analysis. Our solution is to express
the BETSI algorithm using polymorphic types, so that the same algorithmic structure can be instantiated over
floating-point values for computation and over real numbers for proof (Figure 2). In this way, polymorphism
provides the mechanism that links executable computation with proof-oriented specification. Thus, we prove
correctness for functions over real numbers, and perform execution for functions over floating-point values.
This approach differs from methods that reason directly about floating-point operations, including formally
verified floating-point libraries such as Flocq [16] and tools for automated round-off error certification such
as Gappa [17]. Within the Lean ecosystem, related efforts include experimental developments such as Flean
[18], which aim to formalize floating-point semantics directly. It also contrasts with approaches based on
interval arithmetic, which provide certified bounds on numerical error (e.g., CoqInterval [19] and LeanCert
[20]).
       In our implementation, we handle the alignment between Real- and Float-valued functions using the
typeclass BETLike, which organizes the instances for the arithmetic operations used in all the functions in
this work. Unlike the RealLike typeclass from LeanLJ [21], which uses Boolean-valued comparisons suited
for computation, BETLike uses proposition-valued ordering that integrates naturally with Lean’s mathemat-
ical proof infrastructure.

3.3.     Executable Checks and Derivation as Specification

Specifications in this work come from two distinct sources. The first is the set of mathematical properties that
each function is expected to satisfy. The monotonicity check corresponds to a sequence being nondecreasing,
the regression step to solving a least-squares problem, and the window enumeration to producing every
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          7


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               <latexit sha1_base64="w0PVX34BPDtylG0k1mC5WXsMb0I=">AAAB9HicbVDLSgNBEOz1GeMr6tHLYBDiJeyKRPEU9OIxgnlAsoTeyWwyZPbhzGwwLPkOLx4U8erHePNvnCR70MSChqKqm+4uLxZcadv+tlZW19Y3NnNb+e2d3b39wsFhQ0WJpKxOIxHJloeKCR6yuuZasFYsGQaeYE1veDv1myMmFY/CBz2OmRtgP+Q+p6iN5PqlJ3JNOijiAZ51C0W7bM9AlomTkSJkqHULX51eRJOAhZoKVKrt2LF2U5SaU8Em+U6iWIx0iH3WNjTEgCk3nR09IadG6RE/kqZCTWbq74kUA6XGgWc6A9QDtehNxf+8dqL9KzflYZxoFtL5Ij8RREdkmgDpccmoFmNDkEpubiV0gBKpNjnlTQjO4svLpHFedirlyv1FsXqTxZGDYziBEjhwCVW4gxrUgcIjPMMrvFkj68V6tz7mrStWNnMEf2B9/gAngZES</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               f (x : ↵)

                                     f (x : R)
                                     <latexit sha1_base64="MnlaUSNxjsl/vfQKzgCTFpmsqwY=">AAAB+nicbVDLSgMxFL3js9bXVJdugkWomzIjUsVV0Y3LKvYBbSmZNNOGZjJDklHL2E9x40IRt36JO//GTDsLbT0QOJxzL/fkeBFnSjvOt7W0vLK6tp7byG9ube/s2oW9hgpjSWidhDyULQ8rypmgdc00p61IUhx4nDa90VXqN++pVCwUd3oc0W6AB4L5jGBtpJ5d8EuP6AJ1AqyHnpfcTo57dtEpO1OgReJmpAgZaj37q9MPSRxQoQnHSrVdJ9LdBEvNCKeTfCdWNMJkhAe0bajAAVXdZBp9go6M0kd+KM0TGk3V3xsJDpQaB56ZTCOqeS8V//PasfbPuwkTUaypILNDfsyRDlHaA+ozSYnmY0MwkcxkRWSIJSbatJU3JbjzX14kjZOyWylXbk6L1cusjhwcwCGUwIUzqMI11KAOBB7gGV7hzXqyXqx362M2umRlO/vwB9bnD9k8kx0=</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     <latexit sha1_base64="FMepnFhpv4t1lx4dlbEQFn3MkXk=">AAAB/HicbVDLSsNAFJ34rPUV7dLNYBHqpiQiVVwVBXFZwT6gDWUynbRDJ5MwcyMNof6KGxeKuPVD3Pk3Th8LbT1w4XDOvdx7jx8LrsFxvq2V1bX1jc3cVn57Z3dv3z44bOgoUZTVaSQi1fKJZoJLVgcOgrVixUjoC9b0hzcTv/nIlOaRfIA0Zl5I+pIHnBIwUtcuBKURvsIdYCPIbkVEYHzatYtO2ZkCLxN3TopojlrX/ur0IpqETAIVROu268TgZUQBp4KN851Es5jQIemztqGShEx72fT4MT4xSg8HkTIlAU/V3xMZCbVOQ990hgQGetGbiP957QSCSy/jMk6ASTpbFCQCQ4QnSeAeV4yCSA0hVHFzK6YDoggFk1fehOAuvrxMGmdlt1Ku3J8Xq9fzOHLoCB2jEnLRBaqiO1RDdURRip7RK3qznqwX6936mLWuWPOZAvoD6/MHrXCULA==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        f (x : Float)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Proofs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Execution
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="1n+DhQXc4F++BP4QKN7vkNq9pF4=">AAAB9HicbVDLSgNBEOyNrxhfUY9eBoPgKeyKRI9BLx4jmAckS5idzCZDZnfWmd5gWPIdXjwo4tWP8ebfOHkcNLGgoajqprsrSKQw6LrfTm5tfWNzK79d2Nnd2z8oHh41jEo143WmpNKtgBouRczrKFDyVqI5jQLJm8Hwduo3R1wboeIHHCfcj2g/FqFgFK3kd5A/YVbTSoVm0i2W3LI7A1kl3oKUYIFat/jV6SmWRjxGJqkxbc9N0M+oRsEknxQ6qeEJZUPa521LYxpx42ezoyfkzCo9EiptK0YyU39PZDQyZhwFtjOiODDL3lT8z2unGF77mYiTFHnM5ovCVBJUZJoA6QnNGcqxJZRpYW8lbEA1ZWhzKtgQvOWXV0njouxVypX7y1L1ZhFHHk7gFM7Bgyuowh3UoA4MHuEZXuHNGTkvzrvzMW/NOYuZY/gD5/MHgdKSmQ==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="NuuhMtfBYCg8TWNSEduYPC4bMZI=">AAAB+XicbVDLSgNBEJz1GeNr1aOXwSB4Crsi0WNQBI8RzAOSJcxOOsmQ2QczvSFhyZ948aCIV//Em3/jbLIHTSxoKKq66e7yYyk0Os63tba+sbm1Xdgp7u7tHxzaR8cNHSWKQ51HMlItn2mQIoQ6CpTQihWwwJfQ9Ed3md8cg9IiCp9wGoMXsEEo+oIzNFLXtjsIE0zvJ8CTTJl17ZJTduagq8TNSYnkqHXtr04v4kkAIXLJtG67ToxeyhQKLmFW7CQaYsZHbABtQ0MWgPbS+eUzem6UHu1HylSIdK7+nkhZoPU08E1nwHCol71M/M9rJ9i/8VIRxglCyBeL+omkGNEsBtoTCjjKqSGMK2FupXzIFONowiqaENzll1dJ47LsVsqVx6tS9TaPo0BOyRm5IC65JlXyQGqkTjgZk2fySt6s1Hqx3q2PReualc+ckD+wPn8AV42UIw==</latexit>




Figure 2: Polymorphic functions link proofs (over idealized Real numbers) with execution (over floating
point numbers), using a polymorphic function f that uses generic type α. To set up proofs, α is specialized
to Real, and to set up executions, α is specialized to Float. Figure taken from [21] with permission.


valid contiguous sublist of the isotherm. For each of these, we prove the property holds whenever the
corresponding executable check succeeds, one function at a time.
       The second source is the BET derivation itself. Working through the algebra of the BET model is what
produces the linearized form p/[n(1 − p)] at the center of the pipeline. The derivation does not just motivate
this transformation; it implies it, and in doing so fixes what the code must compute. This is what we mean
by derivation as specification.
       One further point is worth stating clearly. The correctness established here is a property of the code,
not of any particular run. Once the proofs compile, every execution inherits that guarantee automatically.
A returned result carries evidence that it passed all the checks, but that evidence is trustworthy because the
code was proved correct beforehand, not because the individual run was validated after the fact.


4.     Implementation of LeanBET

This section describes the structure of our implementation of the BETSI algorithm. The presentation focuses
on how the algorithm operates on adsorption data. All components are written in a polymorphic style,
allowing the same implementation to be used for floating-point execution and real-valued reasoning. The
full source is available at https://github.com/ATOMSLab/LeanBET. In Section 5, we highlight the
proofs verifying the functions described here.

4.1.     Data Structures

The core object used throughout the analysis is the adsorption isotherm, represented as a finite ordered list
of data points. Each point contains a relative pressure value and the corresponding uptake, each with type α
(for proofs, we specialize α to Real, for execution, we specialize α to Float). This provides the input for all
later fitting and filtering steps.
                                                                                                             8




 structure Point (α : Type) where
   p : α -- reduced pressure
   n : α -- amount adsorbed
   deriving Repr

 abbrev Isotherm (α : Type) := List (Point α)


       Additional structures are used to store intermediate and final results. A fit record BETFit stores the
slope and intercept of the linearized BET regression, the coefficient of determination, the derived monolayer
capacity and BET constant, and the index range of the fitting window. A final result record BETSIResult
also stores the selected window together with auxiliary quantities used in the last stage of filtering, such as
the pressure values and percentage error. Keeping these quantities explicit makes the procedure easier to
inspect, easier to verify, and easier to compare across candidate windows. Variables in these either have type
α or type Nat (for the natural numbers) – since natural numbers are computable, we don’t need to invoke
polymorphism for them.


 structure BETFit (α : Type) where
   slope : α
   intercept : α
   rSquared : α
   nm : α
   c : α
   range : Nat × Nat
   nPoints : Nat
   deriving Repr

 structure BETSIResult (α : Type) where
   fit     : BETFit α
   window : List (Point α)
   p_nm    : α
   p_read : α
   pcError : α
   deriving Repr




4.2.     BET Linearization

The next step applies the standard BET linearization to each data point in the isotherm. Here p denotes the
relative pressure, defined as p = P/P0 , and n denotes the corresponding uptake. In the present implemen-
tation, the isotherm is represented directly in terms of relative pressure and uptake, so the transformation is
applied to reduced pressure values.
       Following the linearized BET form introduced earlier in Eq. (2), each point is mapped to the pair
                                                                                                                   9

             
         p
  p,           . This is the quantity used in the regression step. The transformation is applied only when
     n(1 − p)
the denominator n(1 − p) is defined and nonzero, thus avoiding division by zero. In this way, the executable
transformation mirrors the algebraic linearization developed in Section 2.

4.3.     Window Enumeration

BET analysis is carried out over contiguous subsets of the isotherm, which we refer to as windows. The
implementation enumerates every contiguous window containing at least two points and records its start
index, end index, and associated sublist of data. Each such window is then passed to the regression and
admissibility steps described below.
       This gives a finite collection of candidate fitting ranges drawn from the experimental isotherm. By
storing the window boundaries explicitly, the later stages of the algorithm can track which interval produced
each candidate fit and result.

4.4.     Linear Regression

For each window, the transformed data are fitted by least-squares linear regression, according to the lin-
earized BET relation in Eq. (2). The regression operates on a list of pairs (xi , yi ), where xi = pi is the relative
pressure and yi = pi /[ni (1 − pi )] is the BET-transformed uptake.


 /-- Least-squares linear regression returns (slope, intercept, r2 ). -/
 def linearRegression {α} [BETLike α] (data : List (α × α)) : Option (α × α × α) :=
     do
   if data.length < 2 then none else
     let n : α := BETLike.ofNat data.length
     let xs : List α := data.map Prod.fst
     let ys : List α := data.map Prod.snd
     let xBar : α := listSum xs / n
     let yBar : α := listSum ys / n
     let cov : α := listSum <| data.map (fun (x, y) => (x - xBar) * (y - yBar))
     let vr : α := listSum <| data.map (fun (x, _) => (x - xBar) ^ (2 : Nat))

        if BET.isZero vr then none else
          let slope : α := cov / vr
          let intercept : α := yBar - slope * xBar
          let yHat : List α := xs.map (fun x => slope * x + intercept)
          let ssTot : α := listSum <| ys.map (fun y => (y - yBar) ^ (2 : Nat))
          let ssRes : α := listSum <| (List.zip ys yHat).map (fun (y, yh) => (y - yh) ^
        (2 : Nat))
          let r2 : α := if BET.isZero ssTot then BETLike.one else BETLike.one - (ssRes /
        ssTot)
          some (slope, intercept, r2)
                                                                                                               10


       Given n such pairs, the slope and intercept of the fitted line are

                                          ∑ni=1 (xi − x̄)(yi − ȳ)
                                    m=                             ,       b = ȳ − mx̄,                      (3)
                                              ∑ni=1 (xi − x̄)2

where x̄ and ȳ are the sample means. The goodness of fit is assessed via the coefficient of determination,

                                                           ∑ni=1 (yi − ŷi )2
                                              R2 = 1 −                        ,                               (4)
                                                           ∑ni=1 (yi − ȳ)2

where ŷi = mxi + b is the fitted value at xi . From the returned slope and intercept, the monolayer capacity
and BET constant are recovered via

                                                    1                         m
                                           nm =        ,          C = 1+        .                             (5)
                                                   b+m                        b

The function returns none if fewer than two points are provided or if the variance of the xi values is zero,
since the regression is undefined in those cases.

4.5.     Admissibility Checks

Each candidate fit is then tested against the Rouquerol admissibility criteria described in Section 2. These
checks include monotonicity conditions on derived adsorption quantities, minimum data requirements, co-
efficient of determination, and basic physical constraints such as positivity of the fitted parameters. A
candidate is retained only if it satisfies all of the required conditions. The outcome is a filtered collection of
admissible candidate fits, which are then passed to the final selection stage.

4.6.     Final Selection

The Rouquerol criteria alone do not guarantee a unique result, and when multiple candidate windows pass
all four conditions, a fifth criterion is needed. BETSI supplies this through a knee-selection rule, and in
LeanBET this rule is implemented as a two-stage function over the polymorphic type BETLike α.
       The first stage filters the list of passing candidates by end index, retaining only those whose fitting
window reaches the largest pressure index among all retained candidates. This is implemented as a list
traversal that compares end indices using the BETLike ordering, and returns a sublist. The second stage
selects from that sublist the candidate with the smallest percentage error, implemented as a fold over the
filtered list.
       The correctness of the selection, that the returned result genuinely belongs to the maximal-end-index
candidates is not assumed but proved, as stated in Theorems A.6 and A.7. Together with the Rouquerol
checks this completes the LeanBET implementation of the full BETSI procedure.


5.     Formal Specification and Verified Soundness of the BETSI Algorithm

This section presents the formal interpretation of the BETSI algorithm together with the correctness guaran-
tees established for its implementation. The goal is to make precise what it means for a BETSI result to be
valid and to show that every result produced by the algorithm satisfies this interpretation. All specifications
                                                                                                                 11


and proofs are carried out in Lean 4, using a shared polymorphic formulation that supports both floating-
point execution and real-number reasoning. Throughout this section, key results are stated as informal
theorems in natural language, labeled Theorem A.1 through Theorem A.7; the complete machine-checked
Lean proofs and supporting lemmas are available in the accompanying repository.

5.1.     Specification of the BETSI-style Procedure

The BETSI-style procedure considered in this work consists of a sequence of conceptual steps: enumerating
admissible windows of an adsorption isotherm, fitting linearized BET models to those windows, applying
physical and statistical admissibility criteria, and selecting a final result based on the knee principle. In this
development, each of these steps is given an explicit mathematical specification, independent of any partic-
ular numerical implementation. The derivation also plays an important role here: it justifies the linearized
BET form used in the regression step and helps connect the scientific model to the executable analysis.
       Window enumeration is specified as the collection of all contiguous sublists of the isotherm containing
at least two data points, together with their corresponding index ranges. This makes precise the search space
over which BET fitting is carried out and ensures that no admissible window is omitted by design.
       Monotonicity conditions, such as those appearing in the extended Rouquerol criteria, are specified as
properties of derived sequences. For example, the sequence n(1 − p) associated with a window is required
to be nondecreasing, and the sequence obtained from BET linearization must satisfy the same property.
       The regression step is specified in terms of least-squares fitting. Given a list of linearized data points, a
valid regression result is defined as one whose slope and intercept minimize the sum of squared residuals,
provided that the variance of the independent variable is nonzero. From these regression parameters, the
BET constants nm and C are defined using their standard theoretical formulas.
       Finally, the knee-selection principle is specified as follows: among all admissible candidate results,
those whose fitting window extends to the largest pressure index are retained, and from this subset the result
with the smallest percentage error is selected. This captures the intended physical interpretation of the knee
as the upper limit of reliable BET behavior.
       Taken together, these specifications define what it means for a reported result to be valid, independently
of how that result is computed.

5.2.     Executable Checks and Soundness

The algorithm realizes these specifications through executable checks on numerical data. In practice, these
checks are written so they can run efficiently on floating-point inputs. For example, monotonicity is checked
by scanning finite lists, and the admissibility conditions are implemented as decision steps in the code.
       The main correctness goal is soundness: whenever one of these checks succeeds and the algorithm
returns a result, the corresponding mathematical specification is satisfied. In other words, every reported
result meets the formal validity conditions defined for the BETSI-style procedure.
       The executable pipeline runs with floating-point arithmetic, while the main correctness statements are
proved over the real numbers. As with any floating-point implementation, this leaves a small possibility
that a comparison very close to a threshold could behave differently in execution than it would over exact
real values. In practice, however, this is not a serious concern for the adsorption datasets considered here,
                                                                                                          12


since the relevant inequalities are not usually decided at machine-precision boundaries (for instance, 0.1
+ 0.2 > 0.3 is true for IEEE-754 floats, but only deviates at the 17th decimal place). For this application,
experimental noise is far greater than double-precision round-off values.
       This design places the emphasis on the correctness of accepted results. The algorithm enforces the
BETSI-style admissibility conditions and rules out outputs that are physically inadmissible or internally
inconsistent. As a result, each surface area reported by the implementation comes with a machine-checked
guarantee that it satisfies the formal specification.

5.3.     Soundness of the Linearized BET Model

The formal guarantees for the linearization step rest on two connected results. The first shows that the BET
isotherm (Eq. (1)) is a theorem derived from the layer model, not an assumption. The second shows that the
executable linearizeBET function, fed this proved isotherm, returns exactly the affine BET line.

Derivation of the BET Isotherm from the Layer Model

The infinite sums for A and V defined in Section 2.1 both converge when 0 < x < 1. Under this condi-
tion, evaluating their closed forms and taking the ratio V /A gives the theorem brunauer_26_from_seq
intermediate result,
                                          V             Cx
                                               =                   .                                     (6)
                                         V0 · A (1 − x)(1 − x +Cx)
Substituting x = P/P0 then gives the standard BET isotherm, which is machine-checked in theorem brunau
er_28_from_seq. This means that the resulting equation follows from the layer definitions whenever the
convergence condition holds, rather than being stated as a hypothesis.

  Theorem A.1: The BET isotherm follows from the layer model

  Let S be a BET system with saturation pressure P0 = 1/CL , and let P > 0 satisfy the convergence
  condition 0 < x < 1, where x = P ·CL . Then the ratio of total adsorbed volume to total adsorbed area
  satisfies
                                                 V
                                                   = V0 · n(P),
                                                 A
  where n(P) is the standard BET isotherm

                                                    C · nm · (P/P0 )
                                   n(P) =                                 .
                                            (1 − P/P0 ) 1 + (C − 1)(P/P0 )

  Thus, whenever the convergence condition holds and P0 = 1/CL , the standard BET isotherm is a direct
  consequence of the infinite layer definitions for A and V .
                                                                                                              13


Algebraic Correctness of the Linearization

Given the proved isotherm, the following theorem confirms that packaging n(P) into the executable def
linearizeBET function returns exactly the affine BET line, with slope and intercept encoding nm and C.

  Theorem A.2: BET linearization is algebraically correct

  Given that the adsorption amount satisfies the nonlinear BET equation and p = P/P0

                                                          Cnm p
                                         n(p) =                        ,
                                                  (1 − p) 1 + (C − 1)p

  with C ̸= 0, nm ̸= 0, p ̸= 0, and p ̸= 1. Then the BET-transformed quantity

                                                        p
                                                   n(p)(1 − p)

  is affine in p, namely
                                               p       1    C−1
                                                     =    +     p.
                                          n(p)(1 − p) Cnm   Cnm
  Thus, whenever the nonlinear BET model holds, the standard BET plot is exactly linear, with intercept
  1/(Cnm ) and slope (C − 1)/(Cnm ).


       This theorem is the formal counterpart of the derivation presented earlier in Section 2. It shows that the
quantity computed by the linearization step in the executable analysis is precisely the one predicted by BET
theory.

5.4.     Soundness and Completeness of Window Enumeration

The window-enumeration step defines the search space over which BET fitting is carried out. In the ex-
ecutable pipeline, a window is generated by choosing a start index, an end index, and returning the cor-
responding contiguous slice of the isotherm. For the later stages of the analysis to be meaningful, this
enumeration step must do exactly what it is intended to do: it must generate only valid candidate windows,
and it must generate all of them.
       Formally, a valid window is a contiguous sublist of the original isotherm whose start and end indices lie
within bounds and satisfy i < j, so that the window contains at least two data points. The verification of
this stage therefore has two parts. First, we show that every window returned by the executable procedure
satisfies these validity conditions. Second, we show that every valid contiguous window determined by
admissible indices is in fact returned by the procedure.
                                                                                                                        14


  Theorem A.3: Window enumeration returns exactly the valid contiguous fitting windows

  Let I = [p0 , . . . , pN−1 ] be an input isotherm, and let W = I[i : j + 1] = [pi , pi+1 , . . . , p j ] denote the
  contiguous sublist of I from index i to index j inclusive. Soundness. Every triple (i, j,W ) returned by
  the window-enumeration procedure satisfies

                                  0≤i< j<N              and       W = I[i : j + 1].

  Completeness. Conversely, for every pair of indices i, j satisfying

                                                   0 ≤ i < j < N,

  the corresponding contiguous sublist
                                                  W = I[i : j + 1]

  appears among the windows returned by the procedure.
  Hence the executable enumeration procedure produces exactly the valid contiguous fitting windows,
  and each such window contains at least two points.


       This theorem shows that the fitting stage neither misses admissible candidate ranges nor introduces
malformed ones. This supports the later regression, admissibility, and selection theorems, which can be
stated over the intended BET search space itself.
       Note that a Python implementation of BETSI could in principle ensure soundness by implementing
Boolean if-then conditions to filter out invalid windows. However, Python does not have the machinery to
assert completeness of the procedure; our implementation proves that we miss no windows.

5.5.     Soundness of Linear Regression and BET Parameter Extraction

A successful regression means that the executable routine returns values m, b, and r2 . To state correctness
precisely, we compare this result to an arbitrary alternative pair of coefficients (m′ , b′ ), representing any
other candidate line.

  Theorem A.4: Successful regression returns a least-squares minimizer

  Let D = {(xi , yi )}ni=1 be a nonempty dataset of linearized adsorption points, and suppose the variance
  of the xi values is positive. If the executable regression routine returns

                                     linearRegression(D) = some(m, b, r2 ),

  then for every alternative pair of coefficients (m′ , b′ ),

                                        SSres (D, m, b) ≤ SSres (D, m′ , b′ ).

  That is, the returned slope m and intercept b define a least-squares minimizer.
                                                                                                              15


       Once these coefficients are obtained, the monolayer capacity nm and BET constant C are computed
directly from m and b using the standard formulas.

  Theorem A.5: BET parameter extraction agrees with the certified regression line

  Suppose the executable regression routine returns

                                      linearRegression(D) = some(m, b, r2 ).

  Then the quantities extracted from the returned line,

                                              1                           m
                                      nm =              and      C = 1+     ,
                                             b+m                          b

  agree with their definitions from the linearized BET model.


       Together, these theorems show that the regression stage correctly computes the slope and intercept of the
fitted line, and that the physical parameters derived from this line are consistent with the underlying model.
Parts of the formal development were interactively refined using proof-assistant tooling.

5.6.     Soundness of Admissibility Checks and Final Selection

After regression, each candidate window is tested against the admissibility conditions derived from the
Rouquerol criteria together with additional constraints used in the BETSI-style procedure. These include
monotonicity of derived quantities, positivity of fitted parameters, and consistency conditions relating the
monolayer pressure to the fitting range.
       In the implementation, these conditions are evaluated through executable checks on finite sequences and
fitted parameters. Each check returns a Boolean value indicating whether the condition is satisfied.

  Theorem A.6: Soundness of admissibility checks

  Let Z be a candidate window, and suppose all admissibility checks succeed for Z. Then the corre-
  sponding derived quantities satisfy the formal conditions: the relevant sequences are nondecreasing,
  the fitted parameters satisfy C > 0 and nm > 0, and the monolayer pressure lies within the fitting range
  and meets the prescribed consistency condition.
  Thus, any window accepted by the algorithm satisfies the full set of admissibility requirements.


       After filtering, the algorithm selects a single result using the knee-based rule. First, it determines the
largest end index among all admissible windows. Then it restricts attention to those windows whose end
index matches this maximum. Among these, the result with the smallest percentage error is selected.
                                                                                                                16


     Theorem A.7: Soundness of knee-based selection

     Let R be the set of admissible candidate results, and let jmax be the largest end index among them. If
     the selection procedure returns a result r, then:

          • r ∈ R,

          • the fitting window of r ends at jmax , and

          • among all candidates in R with end index jmax , r has minimal percentage error.


       This theorem shows that the filtering step has a simple mathematical meaning. The final result is selected
from the admissible candidates and satisfies the intended maximal-end-index and minimal-error criteria.

5.7.     Summary of Guarantees

Taken together, the results of this section show that the LeanBET implementation is connected to a clear
mathematical account of the analysis pipeline. Each main stage is supported by a formal statement explain-
ing what the executable step means and what it guarantees when it succeeds.
       The linearization result shows that the transformed quantity used in the fit is exactly the one predicted by
the nonlinear BET model. The window-enumeration result shows that the search space consists of exactly
the valid contiguous fitting windows. The admissibility result (Theorem A.6) includes monotonicity: it
shows that whenever the admissibility checks succeed, the relevant derived sequences are nondecreasing,
as required by the formal specification. The regression result shows that a successful fitted line is a least-
squares minimizer, and the parameter-extraction result shows that the reported nm and C values agree with
the corresponding quantities defined from that certified line. Finally, the knee-selection results show that the
final reported result is chosen from the admissible candidates retained according to the intended maximal-
end index rule.
       Together, these theorems do more than justify isolated pieces of code. They show that the main exe-
cutable steps of the analysis remain aligned with their mathematical meaning from the beginning to the end.
As a result, when the algorithm reports a final BET result, that result is not simply the output of a numer-
ical workflow. It is the output of an executable pipeline whose main stages are tied to machine-checked
mathematical guarantees.


6.     Results and Discussion

Across the benchmark set, LeanBET agrees with the BETSI reference implementation to machine preci-
sion for 18 of the 19 isotherms. The only exception is UiO-66 result, for which the two results differ by
about 0.36 m2 /g, or approximately 0.03%. The full numerical comparison is available in the accompanying
repository (see Data Availability).
       This level of agreement is important because both implementations rely on IEEE 754 floating-point
arithmetic. In that setting, agreement to machine precision across nearly the entire test set provides strong
evidence that the Lean implementation faithfully reproduces the intended computational workflow while
also supporting formal mathematical guarantees.
                                                                                                           17


     The reason for the small difference observed for UiO-66 eludes us, as of this writing. Despite careful
comparison, we did not determine why that case differs while the others agree to machine precision. The
deviation is much greater than machine precision, but much smaller than typical experimental uncertainties.
At present, we simply report the discrepancy as an isolated case and note the otherwise close agreement
between BETSI and LeanBET.
     Implementing this workflow in Lean was not trivial, but the availability of IEEE 754 floating-point exe-
cution together with comparison against a benchmark test suite made it possible to check the implementation
while developing the formal results around it.
     As we developed this code, we developed floating-point functions to run tests against BETSI in parallel
with Real-valued functions, for exploring derivations and proofs. These were only merged into polymorphic
functions at a much later stage. We do not recommend starting a new project with polymorphic functions;
writing code for proofs and programs is simply more ergonomic without the typeclass complications.
     These efforts were started by two undergraduate students, one who had specialized in studying theorem
proving in Lean, and one who had studied functional programming in Lean. A graduate student who stud-
ied both ultimately refactored the separate implementations to create a polymorphic artifact, thus linking
the proofs to the program, while expanding the specifications and fixing implementation details that are
not represented by the criteria. For instance, BETSI uses PCHIP (Piecewise Cubic Hermite Interpolating
Polynomial) interpolation, and our original implementation used linear interpolation, a detail which didn’t
violate specifications, though it did break agreement with BETSI when different windows were selected. We
thus see tests as a critical part of the development process, augmenting the specifications. To put it another
way: even with a suite of theorems specifying the derivation of the theory and numerous constraints the
implementation must satisfy, there exist multiple variations of the software that would satisfy the proofs; in
our case, these were only eliminated by comparison with benchmark tests.


7.   Conclusion

We have presented LeanBET, a formally verified implementation of BET-style surface area analysis in
Lean 4. The development combines executable floating-point computation with proof-oriented specifica-
tions over the real numbers, allowing the main steps of the workflow to be connected to explicit mathematical
statements. These include the BET linearization, window enumeration, monotonicity checks, least-squares
regression, BET parameter extraction, and final knee-based selection.
     When compared against the BETSI reference implementation on a benchmark set of adsorption isotherms,
LeanBET agrees to machine precision in 18 of the 19 cases. The only exception is UiO-66, where a small
discrepancy remains, but this does not affect the overall conclusion of very strong agreement across the
benchmark set.
     More broadly, this work shows that a practically useful scientific-computing workflow can be translated
into Lean without sacrificing numerical agreement. In this setting, formal verification does not replace
numerical computation; it helps explain and justify it. By linking the executable pipeline to machine-
checked mathematical statements, LeanBET provides a clearer basis for correctness, reproducibility, and
trust in BET surface area analysis.
                                                                                                       18


Acknowledgements

This material is based on work supported by the National Science Foundation (NSF) CAREER Award
#2236769.


Declaration of Interest

The authors declare no competing financial or personal interests that could influence the work reported in
this paper.


Data Availability

All code, proofs, and benchmark files are on the ATOMS Lab Github.


ORCID

Ejike D. Ugwuanyi https://orcid.org/0009-0006-4335-5428
Colin T. Jones https://orcid.org/0009-0007-9013-8036
John Velkey https://orcid.org/0000-0001-5156-7451
Tyler R. Josephson https://orcid.org/0000-0002-0100-0227

References
 [1] Stephen Brunauer, P. H. Emmett, and Edward Teller. Adsorption of Gases in Multimolecular Layers.
     Journal of the American Chemical Society, 60(2):309–319, February 1938. URL: https://pubs.a
     cs.org/doi/abs/10.1021/ja01269a023, doi:10.1021/ja01269a023.
 [2] Titus S. Van Erp and Johan A. Martens. A standardization for BET fitting of adsorption isotherms.
     Microporous and Mesoporous Materials, 145(1-3):188–193, November 2011. URL: https://link
     inghub.elsevier.com/retrieve/pii/S1387181111002435, doi:10.1016/j.micromeso.20
     11.05.022.
 [3] Johannes W. M. Osterrieth, James Rampersad, David Madden, Nakul Rampal, Luka Skoric, Bethany
     Connolly, Mark D. Allendorf, Vitalie Stavila, Jonathan L. Snider, Rob Ameloot, João Marreiros,
     Conchi Ania, Diana Azevedo, Enrique Vilarrasa-Garcia, Bianca F. Santos, Xian-He Bu, Ze Chang,
     Hana Bunzen, Neil R. Champness, Sarah L. Griffin, Banglin Chen, Rui-Biao Lin, Benoit Coasne,
     Seth Cohen, Jessica C. Moreton, Yamil J. Colón, Linjiang Chen, Rob Clowes, François-Xavier Coud-
     ert, Yong Cui, Bang Hou, Deanna M. D’Alessandro, Patrick W. Doheny, Mircea Dincă, Chenyue
     Sun, Christian Doonan, Michael Thomas Huxley, Jack D. Evans, Paolo Falcaro, Raffaele Ricco,
     Omar Farha, Karam B. Idrees, Timur Islamoglu, Pingyun Feng, Huajun Yang, Ross S. Forgan,
     Dominic Bara, Shuhei Furukawa, Eli Sanchez, Jorge Gascon, Selvedin Telalović, Sujit K. Ghosh,
     Soumya Mukherjee, Matthew R. Hill, Muhammed Munir Sadiq, Patricia Horcajada, Pablo Salcedo-
     Abraira, Katsumi Kaneko, Radovan Kukobat, Jeff Kenvin, Seda Keskin, Susumu Kitagawa, Ken-
     ichi Otake, Ryan P. Lively, Stephen J. A. DeWitt, Phillip Llewellyn, Bettina V. Lotsch, Sebas-
     tian T. Emmerling, Alexander M. Pütz, Carlos Martí-Gastaldo, Natalia M. Padial, Javier García-
     Martínez, Noemi Linares, Daniel Maspoch, Jose A. Suárez del Pino, Peyman Moghadam, Rama Okta-
     vian, Russel E. Morris, Paul S. Wheatley, Jorge Navarro, Camille Petit, David Danaci, Matthew J.
     Rosseinsky, Alexandros P. Katsoulidis, Martin Schröder, Xue Han, Sihai Yang, Christian Serre,
     Georges Mouchaham, David S. Sholl, Raghuram Thyagarajan, Daniel Siderius, Randall Q. Snurr,
     Rebecca B. Goncalves, Shane Telfer, Seok J. Lee, Valeska P. Ting, Jemma L. Rowlandson, Takashi
     Uemura, Tomoya Iiyuka, Monique A. van der Veen, Davide Rega, Veronique Van Speybroeck,
     Sven M. J. Rogge, Aran Lamaire, Krista S. Walton, Lukas W. Bingel, Stefan Wuttke, Jacopo An-
     dreo, Omar Yaghi, Bing Zhang, Cafer T. Yavuz, Thien S. Nguyen, Felix Zamora, Carmen Mon-
     toro, Hongcai Zhou, Angelo Kirchon, and David Fairen-Jimenez. How Reproducible are Surface
                                                                                                       19


     Areas Calculated from the BET Equation? Advanced Materials, 34(27):2201502, 2022. _eprint:
     https://advanced.onlinelibrary.wiley.com/doi/pdf/10.1002/adma.202201502. URL: https://online
     library.wiley.com/doi/abs/10.1002/adma.202201502, doi:10.1002/adma.202201502.
 [4] Filip Ambroz, Thomas J. Macdonald, Vladimir Martis, and Ivan P. Parkin. Evaluation of the BET
     Theory for the Characterization of Meso and Microporous MOFs. Small Methods, 2(11):1800173,
     November 2018. URL: https://onlinelibrary.wiley.com/doi/10.1002/smtd.201800173,
     doi:10.1002/smtd.201800173.
 [5] D.D. Do, H.D. Do, and D. Nicholson. A computer appraisal of BET theory, BET surface area and the
     calculation of surface excess for gas adsorption on a graphite surface. Chemical Engineering Science,
     65(10):3331–3340, May 2010. URL: https://linkinghub.elsevier.com/retrieve/pii/S00
     09250910000965, doi:10.1016/j.ces.2010.02.023.
 [6] J. Rouquerol, D. Avnir, C. W. Fairbridge, D. H. Everett, J. M. Haynes, N. Pernicone, J. D. F. Ramsay,
     K. S. W. Sing, and K. K. Unger. Recommendations for the characterization of porous solids (Technical
     Report). Pure and Applied Chemistry, 66(8):1739–1758, January 1994. Publisher: De Gruyter. URL:
     https://www.degruyterbrill.com/document/doi/10.1351/pac199466081739/html
     ?lang=en&srsltid=AfmBOopFxwrug7MNUSub2cm3Lny11J5tySwMkMTA5FTdBiX0dzo2wMhO,
     doi:10.1351/pac199466081739.
 [7] Leonardo De Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language.
     In André Platzer and Geoff Sutcliffe, editors, Automated Deduction – CADE 28, volume 12699, pages
     625–635. Springer International Publishing, Cham, 2021. Series Title: Lecture Notes in Computer
     Science. URL: https://link.springer.com/10.1007/978- 3- 030- 79876- 5_37, doi:
     10.1007/978-3-030-79876-5_37.
 [8] Irving Langmuir. THE ADSORPTION OF GASES ON PLANE SURFACES OF GLASS, MICA
     AND PLATINUM. Journal of the American Chemical Society, 40(9):1361–1403, September 1918.
     URL: https://pubs.acs.org/doi/abs/10.1021/ja02242a004, doi:10.1021/ja02242a004.
 [9] Maxwell P. Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong Dang, Catherine M. Wraback,
     and Tyler R. Josephson. Formalizing chemical physics using the Lean theorem prover. Digi-
     tal Discovery, 3(2):264–280, 2024. URL: https://xlink.rsc.org/?DOI=D3DD00077J,
     doi:10.1039/D3DD00077J.
[10] David Thrane Christiansen. Functional Programming in Lean. Microsoft, 2023. URL: https:
     //leanprover.github.io/functional_programming_in_lean/.
[11] Tomáš Skřivan. lecopivo/SciLean, April 2025. original-date: 2021-09-27T21:50:10Z. URL: https:
     //github.com/lecopivo/SciLean.
[12] Robert Joseph George, Jennifer Cruden, Xiangru Zhong, Huan Zhang, and Anima Anandkumar.
     TorchLean: Formalizing Neural Networks in Lean, 2026. Version Number: 1. URL: https:
     //arxiv.org/abs/2602.22631, doi:10.48550/ARXIV.2602.22631.
[13] Daniel Selsam, Percy Liang, and David L. Dill. Developing Bug-Free Machine Learning Systems
     With Formal Mathematics. In Proceedings of the 34th International Conference on Machine Learning,
     pages 3047–3056. PMLR, July 2017. ISSN: 2640-3498. URL: https://proceedings.mlr.pres
     s/v70/selsam17a.html.
[14] Adrián Doña Mateo. Exploring the capabilities of the Lean interactive theorem prover. Technical
     report, Computer Science and Mathematics School of Informatics University of Edinburgh, 2023.
     URL: https://webhomes.maths.ed.ac.uk/~adona/files/honours_project.pdf.
[15] Jeremy Avigad and Simon Hudon. Programming in Lean. Online tutorial manuscript, Carnegie Mellon
     University, 2019. URL: https://avigad.github.io/programming_in_lean/programming_in_
     lean.pdf.
[16] Sylvie Boldo and Guillaume Melquiond. Flocq: A Unified Library for Proving Floating-Point Al-
     gorithms in Coq. In 2011 IEEE 20th Symposium on Computer Arithmetic, pages 243–252, Tuebin-
     gen, Germany, July 2011. IEEE. URL: http://ieeexplore.ieee.org/document/5992132/,
     doi:10.1109/ARITH.2011.40.
                                                                                                  20


[17] Florent De Dinechin, Christoph Quirin Lauter, and Guillaume Melquiond. Certifying floating-point
     implementations using Gappa, 2008. Version Number: 1. URL: https://arxiv.org/abs/0801.0
     523, doi:10.48550/ARXIV.0801.0523.
[18] Joseph McKinsey. Flean: Floating Point Numbers in Lean, 2025. URL: https://josephmckinsey
     .com/flean.html.
[19] Guillaume Melquiond. Floating-point arithmetic in the Coq system. Information and Computation,
     216:14–23, July 2012. URL: https://linkinghub.elsevier.com/retrieve/pii/S0890540112
     000739, doi:10.1016/j.ic.2011.09.005.
[20] Alejandro Radisic. LeanCert: Verified Numerical Computation in Lean 4, 2026. URL: https:
     //github.com/alerad/leancert.
[21] Ejike D. Ugwuanyi, Colin T. Jones, John Velkey, and Tyler R. Josephson. Benchmarking energy
     calculations using formal proofs. Molecular Physics, 123(21-22):e2539421, November 2025. URL:
     https://www.tandfonline.com/doi/full/10.1080/00268976.2025.2539421, doi:10.108
     0/00268976.2025.2539421.
