                                        Duet: An Expressive Higher-order Language and Linear
                                        Type System for Statically Enforcing Differential Privacy

                                        JOSEPH P. NEAR, University of Vermont
                                        DAVID DARAIS, University of Vermont
arXiv:1909.02481v1 [cs.PL] 5 Sep 2019




                                        CHIKE ABUAH, University of Vermont
                                        TIM STEVENS, University of Vermont
                                        PRANAV GADDAMADUGU, University of California, Berkeley
                                        LUN WANG, University of California, Berkeley
                                        NEEL SOMANI, University of California, Berkeley
                                        MU ZHANG, University of Utah
                                        NIKHIL SHARMA, University of California, Berkeley
                                        ALEX SHAN, University of California, Berkeley
                                        DAWN SONG, University of California, Berkeley
                                        During the past decade, differential privacy has become the gold standard for protecting the privacy of
                                        individuals. However, verifying that a particular program provides differential privacy often remains a manual
                                        task to be completed by an expert in the field. Language-based techniques have been proposed for fully
                                        automating proofs of differential privacy via type system design, however these results have lagged behind
                                        advances in differentially-private algorithms, leaving a noticeable gap in programs which can be automatically
                                        verified while also providing state-of-the-art bounds on privacy.
                                           We propose Duet, an expressive higher-order language, linear type system and tool for automatically
                                        verifying differential privacy of general-purpose higher-order programs. In addition to general purpose
                                        programming, Duet supports encoding machine learning algorithms such as stochastic gradient descent, as
                                        well as common auxiliary data analysis tasks such as clipping, normalization and hyperparameter tuning–each
                                        of which are particularly challenging to encode in a statically verified differential privacy framework.
                                           We present a core design of the Duet language and linear type system, and complete key proofs about privacy
                                        for well-typed programs. We then show how to extend Duet to support realistic machine learning applications
                                        and recent variants of differential privacy which result in improved accuracy for many practical differentially
                                        private algorithms. Finally, we implement several differentially private machine learning algorithms in Duet
                                        which have never before been automatically verified by a language-based tool, and we present experimental
                                        results which demonstrate the benefits of Duet’s language design in terms of accuracy of trained machine
                                        learning models.


                                        1   INTRODUCTION
                                        Advances in big data and machine learning have achieved large-scale societal impact over the
                                        past decade. This impact is accompanied by a growing demand for data collection, aggregation
                                        and analysis at scale. This resulting explosion in the amount of data collected by organizations,
                                        however, has raised important new security and privacy concerns.
                                           Differential privacy [22, 24, 25] is a promising technique for addressing these issues. Differential
                                        privacy allows general statistical analysis of data while protecting data about individuals with a
                                        strong formal guarantee of privacy. Because of its desirable formal guarantees, differential privacy
                                        has received increased attention, with ongoing real-world deployments at organizations including
                                        Google [26], Apple [1], and the US Census [31, 34]. A number of systems for performing differentially
                                        private data analytics have been built and demonstrated to be effective [32, 33, 36, 39, 41, 43, 45].
                                           Differential privacy plays an increasingly important role in machine learning, as recent work has
                                        shown that a trained model can leak information about data it was trained on [27, 49, 53]. Differential
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
2                                Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
privacy provides a robust solution to this problem, and as a result, a number of differentially private
algorithms have been developed for machine learning [3, 13, 17, 28, 42, 50, 51, 54].
   Few practical approaches exist, however, for automatically proving that a general-purpose program
satisfies differential privacy—an increasingly desirable goal, since many machine learning pipelines
are expressed as programs that combine existing algorithms with custom code. Enforcing differential
privacy for a new program currently requires a new, manually-written privacy proof. This process is
arduous, error-prone, and must be performed by an expert in differential privacy (and re-performed,
each time the program is modified).
   We present Duet, a programming language, type system and tool for expressing and stati-
cally verifying privacy-preserving programs. Duet supports (1) general purpose programming
features like compound datatypes and higher-order functions, (2) library functions for matrix-based
computations, and (3) multiple state-of-the-art variants of differential privacy–(ϵ, δ )-differential
privacy [25], Rényi differential privacy [38], zero-concentrated differential privacy (zCDP) [16],
and truncated-concentrated differential privacy (tCDP) [15]–and can be easily extended to new
ones. Duet strikes a strategic balance between generality, practicality, extensibility, and precision
of computed privacy bounds.
   The design of Duet consists of two separate, mutually embedded languages, each with its own
type system. The sensitivity language uses linear types with metric scaling (as in Fuzz [44]) to
bound function sensitivity. The privacy language uses linear types without metric scaling (novel
in Duet) to compose differentially private computations. Disallowing the use of scaling in the
privacy language is essential to encode more advanced variants of differential privacy (like (ϵ, δ ))
in a linear type system.
   Linear typing [5, 30] is a good fit for both privacy and sensitivity analysis, because resources are
tracked per-variable and combined additively. In particular, our linear typing approach to privacy
allows for independent privacy costs for multiple function arguments, a feature shared by Fuzz and
DFuzz (which only support pure ϵ-differential privacy), but not supported by prior type systems
for (ϵ, δ )-differential privacy. This limitation of prior work is due to the treatment of privacy as a
computational “effect”–a property of the output, embodied in an indexed monad–as opposed to
our treatment of privacy as a “co-effect”–a property of the context, embodied in linear typing.
   Our main idea is to co-design two separate languages for privacy and sensitivity, and our main
insight is that a linear type system can (1) model more powerful variants of differential privacy
(like (ϵ, δ )) when strengthened to disallow scaling, and (2) interact seamlessly with a sensitivity-
type system which does allow scaling. Each language embeds inside the other, and the privacy
mechanisms of the underlying privacy definition (e.g. the Gaussian mechanism [25]) form the
interface between the two languages. Both languages use similar syntax and identical types. The
two languages aid type checking, the proof of type soundness, and our implementation of type
inference; programmers need not be intimately aware of the multi-language design.
   In addition to basic differential-privacy primitives like the Gaussian mechanism, we provide
a core language design for matrix-based data analysis tasks, such as aggregation, clipping and
gradients. Key challenges that we overcome in our design are how each of these features compose
in terms of function sensitivity, and how to statically track bounds on vector norms (due to clipping,
for the purposes of privacy)—and each in a way that is general enough to support a wide range of
useful applications.
   We demonstrate the usefulness of Duet by implementing and verifying several differentially
private machine learning algorithms from the literature, including private stochastic gradient
descent [13] and private Frank-Wolfe [51], among many others. We also implement a variant of
stochastic gradient descent suitable for deep learning. For each of these algorithms, no prior work
has demonstrated an automatic verification of differential privacy, and Duet is able to automatically
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                                     3
infer privacy bounds that equal and in some cases improve upon previously published manual privacy
proofs.
   We have implemented a typechecker and interpreter for Duet, and we use these to perform
an empirical evaluation comparing the accuracy of models trained using our implementations.
Although the “punchline” of the empirical results are unsurprising due to known advantages of
the differential privacy definitions used (e.g., that using recent variants like zero-concentrated
differential privacy results in improved accuracy), our results show the extent of the accuracy
improvements for specific algorithms and further reinforce the idea that choosing the best definition
consistently results in substantially better accuracy of the trained model.
  Contributions. In summary, we make the following contributions:
• We present Duet, a novel language, linear type system and tool for expressing and automatically
  verifying differentially private programs. Unlike previous work, Duet supports a combination of
  (1) general purpose, higher order programming, (2) advanced definitions of differential privacy,
  (3) independent tracking of privacy costs for multiple function arguments, and (4) auxiliary
  differentially-private data analysis tasks such as clipping, normalization, and hyperparameter
  tuning.
• We formalize Duet’s type system and semantics, and complete key proofs about privacy of
  well-typed programs.
• We demonstrate a battery of case studies consisting of medium-sized, real-world, differentially
  private machine learning algorithms which are successfully verified with optimal (or near-
  optimal) privacy bounds. In some cases, Duet infers privacy bounds which improve on the best
  previously published manually-verified result.
• We conduct an experimental evaluation to demonstrate Duet’s feasibility in practice by training
  two machine learning algorithms on several non-toy real-world datasets using Duet’s interpreter.
  These results demonstrate the effect of improved privacy bounds on the accuracy of the trained
  models.

2   PRELIMINARIES
2.1 Background: Differential Privacy
This section briefly summarizes the basics of differential privacy. See Dwork and Roth’s refer-
ence [25] for a detailed description. Differential privacy considers sensitive input data represented
by a vector x ∈ D n , in which x i represents the data contributed by user i. The distance between
two inputs x, y ∈ D n is d(x, y) = |{i |x i , yi }|. Two inputs x, y are neighbors if d(x, y) = 1, i.e., if
they differ in only one index. A randomized mechanism K : D n → Rd preserves (ϵ, δ )-differential
privacy if for any neighbors x, y ∈ D n and any set S of possible outputs:
                                  Pr[K(x) ∈ S] ≤ e ϵ Pr[K(y) ∈ S] + δ
The main idea is that when ϵ and δ are very small, then the resulting output distributions will be
very close, and therefore nearly indistinguishible.
   The ϵ parameter, also called the privacy budget, controls the strength of the privacy guarantee.
The δ parameter allows for a non-zero probability that the guarantee fails, and is typically set to a
negligible value. The case when δ = 0 is called pure or ϵ-differential privacy; the case when δ > 0
is called approximate or (ϵ, δ )-differential privacy. Typical values for ϵ and δ are ϵ ∈ [0.1 − 10] and
δ = n12 where n is the number of input entries [25].
  Function sensitivity. A function’s sensitivity is the amount its output can change when its input
changes. For example, the function f (x) = x +x has a sensitivity of 2, since increasing or decreasing
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
4                                Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
               Variant                    Sequential Composition                  k-Loop Basic Mechanism
              ϵ -DP [25]                   ϵ1 + ϵ2 ≜ ϵ1 + ϵ2                         kϵ       Laplace
            (ϵ, δ )-DP [25]   (ϵ1, δ 1 ) + (ϵ2, δ 2 ) ≜ (ϵ1 + ϵ2, δ 1 + δ 2 )     (kϵ, kδ )   Gaussian
               RDP [38]         (α, ϵ1 ) + (α, ϵ2 ) ≜ (α, ϵ1 + ϵ2 )                (α, kϵ )   Gaussian
              zCDP [16]                    ρ1 + ρ2 ≜ ρ1 + ρ2                         kρ       Gaussian
              tCDP [15]     (ρ 1, ω 1 ) + (ρ 2, ω2 ) ≜ (ρ 1 + ρ 2, min(ω1, ω 2 )) (k ρ, ω)  Sinh-normal
                                    Fig. 1. Variants of Differential Privacy


its input by 1 has the effect of increasing or decreasing its output by 2. A real-valued function f is
called n-sensitive if maxx,y:|x −y | ≤1 | f (x) − f (y)| = n.
   This idea can be generalized to vector-valued functions. The global L1 sensitivity of a query
f : D n → Rd is written GS f and defined GS f = maxx,y:d (x,y)=1 | f (x) − f (y)|1 where | − |1 is the
L1 norm (i.e., sum of pointwise distances between elements). The L2 sensitivity is analogous, using
the L2 norm.

  Differential privacy mechanisms. Two basic differential privacy mechanisms are the Laplace
mechanism [24], which preserves (ϵ, 0)-differential privacy, and the Gaussian mechanism [25],
which preserves (ϵ, δ )-differential privacy. For a function f : D n → Rd with L1 sensitivity of ∆1 ,
the Laplace mechanism adds noise drawn from Lap( ∆ϵ1 ) to each element of the output. For f with
                                                                                            2∆2 ln(1.25/δ )
L2 sensitivity of ∆2 , the Gaussian mechanism adds noise drawn from N (0, 2 ϵ 2           ) to each
element.
   The exponential mechanism [35] selects an element of a set based on the scores assigned to each
element by a scoring function. Let u : D n × R → R be a scoring function with L1 sensitivity ∆. The
mechanism selects and outputs an element r ∈ R with probability proportional to exp( ϵu(x,r  )
                                                                                         2∆ ), and
preserves (ϵ, 0)-differential privacy.

    Composition. A key property of differential privacy is that differentially private computations
compose. The sequential composition theorem says that if M1 and M2 satisfy (ϵ, δ )-differential
privacy, then their combination satisfies (2ϵ, 2δ )-differential privacy.
    Tighter bounds on privacy cost can be achieved using the advanced composition theorem [25],
at the expense of increasing δ . The advanced composition theorem says that for 0 < ϵ ′ < 1 and
δ ′ > 0, the class of (ϵ, δ )-differentially private mechanisms satisfies (ϵ ′, kδ + δp′)-differential privacy
under k-fold adaptive composition (e.g. a loop with k iterations) for ϵ ′ = 2ϵ 2k ln(1/δ ′).
    The moments accountant was introduced by Talwar et al. [3] specifically for stochastic gradient
descent in deep learning applications. It provides tight bounds on privacy loss in iterative applica-
tions of the Gaussian mechanism, as in SGD. The Rényi differential privacy and zero-concentrated
differential privacy generalize the ideas behind the moments accountant.

   Variants of differential privacy. In addition to ϵ and (ϵ, δ )-differential privacy, other variants of
differential privacy with significant benefits have recently been developed. Three examples are Rényi
differential privacy (RDP) [38], zero-concentrated differential privacy (zCDP) [16], and truncated
concentrated differential privacy (tCDP) [15]. Each one has different privacy parameters and a
different form of sequential composition, summarized in Figure 1. The basic mechanism for RDP
and zCDP is the Gaussian mechanism; tCDP uses a novel sinh-normal mechanism [15] which decays
more quickly in its tails. All three can be converted to (ϵ, δ )-differential privacy, allowing them
to be compared and composed with each other. These three variants provide asymptotically tight
bounds on privacy cost under composition, while at the same time eliminating the “catastrophic”
privacy failure that can occur with probability δ under (ϵ, δ )-differential privacy.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                                   5
   Group privacy. Differential privacy is normally used to protect the privacy of individuals, but
it turns out that protection for an individual also translates to (weaker) protection for groups of
individuals. A mechanism which provides pure ϵ-differential privacy for individuals also provides
kϵ-differential privacy for groups of size k [25]. Group privacy also exists for (ϵ, δ )-differential
privacy, RDP, zCDP, and tCDP, but the scaling of the privacy parameters is nonlinear.

2.2   Related Work
Language-based approaches for differential privacy fall into two categories: approaches based
on type systems, and those based on program logics. Barthe et al. [10] provide a survey. The
type-system based approaches are most related to our work, but program-logic-based approaches
have also received considerable attention in recent years [7, 9, 11, 12, 46, 47].

   Linear Type Systems. Type-system-based solutions to proving that a program adheres to differ-
ential privacy began with Reed and Pierce’s Fuzz language [44], which is based on linear typing.
Fuzz, as well as subsequent work based on linear types aided by SMT solvers [29], supports type
inference of privacy bounds with type-level dependency and higher-order composition of pro-
grams. However, these systems only support the original and most basic variant of differential
privacy called ϵ-differential privacy. More recent variants, like (ϵ, δ )-differential privacy [25] and
others [15, 16, 38], improve on ϵ-differential privacy by providing vastly more accurate answers for
the same amount of privacy “cost” (at the expense of introducing a negligible chance of failure).
   As described by Azevedo de Amorim et al. [21], encoding (ϵ, δ )-differential privacy in linear
type systems like Fuzz is particularly challenging because these systems place restrictions on the
interpretation of the linear function space, and (ϵ, δ )-differential privacy does not satisfy these
restrictions. In particular, using Fuzz requires that the desired notion of privacy can be recovered
from an instantiation of function sensitivity for an appropriately defined metric on probabilistic
functions. No such metric can be defined for (ϵ, δ )-differential privacy, preventing a straightforward
interpretation of linear functions as (ϵ, δ )-differentially private functions.
   In their work, Azevedo de Amorim et al. [21] define a path construction to encode non-linear
scaling via an indexed probability monad, which can be used to extend Fuzz with support for
arbitrary relational properties (including (ϵ, δ )-differential privacy). However, this approach (1)
internalizes the use of group privacy [25] which in many cases provides sub-optimal bounds on
privacy cost–and (2) is unable to provide privacy bounds for more than one input to a function–a
useful capability of the original Fuzz language, and a necessary feature to obtain optimal privacy
bounds for multi-argument functions.

   Higher-order Relational Type Systems. Following the initial work on linear typing for differential
privacy [44], a parallel line of work [6, 8] leverages relational refinement types aided by SMT solvers
in order to support type-level dependency of privacy parameters (à la DFuzz [29]) in addition to
more powerful variants of differential privacy such as (ϵ, δ )-differential privacy. These approaches
support (ϵ, δ )-differential privacy, but did not support usable type inference until a recently proposed
heuristic bi-directional type system [19]. Although a direct case study of bidirectional type inference
for relational refinement types has not yet been applied to differential privacy, the possibility of
such a system appears promising.
   The overall technique for supporting (ϵ, δ )-differential privacy in these relational refinement
type systems is similar to (and predates) Azevedo de Amorim et al.–privacy cost is tracked through
an “effect” type, embodied by an indexed monad. It is this “effect”-based treatment of privacy
cost that fundamentally limits these type system to not support multi-arity functions, resulting in
non-optimal privacy bounds for some programs.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
6                                Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
                         SA    HO     DT     MA     Rel-ext   ϵ -DP    (ϵ, δ )-DP   Rényi/zCDP/tCDP        SVT-imp
       Fuzz [44]         ✓     ✓       ✗     ✓        ✗         ✓           ✗               ✗                 ✗
       DFuzz [29]        ✓     ✓      ✓      ✓        ✗         ✓           ✗               ✗                 ✗
       PathC [21]        ✓     ✓      ✗1      ✗       ✓         ✓          ✓               ✓2                 ✗
       HOARe2 [8]        ✓     ✓      ✓       ✗       ✓         ✓          ✓               ✓2                 ✗
       LightDP [55]       ✗     ✗     ✓      ✓        ✗         ✓          ✓               ✓2                ✓
       Fuzzi [56]        ✓      ✗     ✗1     ✓        ✓         ✓          ✓               ✓                 ✓
       Duet              ✓     ✓      ✓      ✓        ✗         ✓          ✓               ✓                  ✗
Fig. 2. Legend: SA = capable of sensitivity analysis; HO = support for higher order programming, program composition,
and compound datatypes; DT = support for dependently typed privacy bounds; MA = support for distinct privacy bounds
of multiple input arguments; Rel-ext = supports extensions to support non-differential-privacy relations; ϵ -DP = supports ϵ -
differential-privacy; (ϵ, δ )-DP = supports (ϵ, δ )-differential-privacy; Rényi/zCDP/tCDP: supports Rényi, zero-concentrated
and truncated concentrated differential privacy; SVT-imp: supports verified implementation of the sparse vector technique. 1:
This limitation is not fundamental and could be supported by simple extension to underlying type theory. 2: Not described
in prior work, but could be achieved through a trivial extension to existing support for (ϵ, δ )-differential privacy.




   First-order Relational Type Systems. Yet another approach is LightDP which uses a light-weight
relational type system to verify (ϵ, δ )-differential privacy bounds of first-order imperative pro-
grams [55], and is suitable for verifying low-level implementations of differentially-private mecha-
nisms. A notable achievement of this work is a lightweight, automated verification of the Sparse
Vector Technique [25] (SVT). However, LightDP is not suitable for sensitivity analysis, an important
component of differentially-private algorithm design. Differential privacy mechanisms often require
knowledge of (or place restrictions on) function sensitivity of arguments to the mechanism. In
principle, a language like Fuzz could be combined with LightDP to fully verify both an application
which uses SVT, as well as the implementation of SVT itself.

   Type Systems Enriched with Program Logics. At a high level, Fuzzi [56] has a similar aim to Duet:
supporting differential privacy for general-purpose programs and supporting recent variants of
differential privacy. Duet is designed primarily as a fully-automated type system with a rich set
of primitives for vector-based and higher-order programming; low-level mechanisms in Duet
are opaque and trusted. On the other hand, Fuzzi is designed for general-purpose programming,
low-level mechanism implementation, and their combination; however, to achieve this, Fuzzi has
less support for higher-order programming and automation in typechecking.

2.3    Our Approach
We show the strengths and limitations of Duet in relation to approaches from prior work in
Figure 2. In particular, strengths of Duet w.r.t. prior work are: (1) Duet supports sensitivity analysis
in combination with higher order programming, program composition, and compound datatypes,
building on ideas from Fuzz (SA+HO); (2) Duet supports type-level dependency on values, which
enables differentially private algorithms to be verified w.r.t. symbolic privacy parameters, building
on ideas from DFuzz (DT); (3) Duet supports calculation of independent privacy costs for multiple
program arguments via a novel approach (MA); and (4) Duet supports (ϵ, δ )-differential privacy—
in addition to other recent powerful variants, such as Rényi, zero-concentrated and truncated
concentrated differential privacy—via a novel approach ((ϵ, δ )-DP, Rényi/ZC/TC)).
   In striking this balance, Duet comes with known limitations: (1) Duet is not easy to extend with
new relational properties (Rel-ext); and (2) Duet is not suitable for verifying implementations of
low-level mechanisms, such as the implementation of advanced composition, gradient operations,
and the sparse-vector technique (SVT-imp).
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                                                    7
3     DUET: A LANGUAGE FOR PRIVACY
This section describes the syntax, type system and formal properties of Duet. Our design of Duet
is the result of two key insights.
(1) Linear typing, when restricted to disallow scaling, can be a powerful foundation for enforcing
    (ϵ, δ )-differential privacy. Privacy bounds in (ϵ, δ )-differential privacy do not scale linearly, and
    cannot be accurately modeled by linear type systems which permit unrestricted scaling.
(2) Sensitivity and privacy cost are distinct properties, and warrant distinct type systems to enforce
    them. Our design for Duet is a co-design of two distinct, mutually embedded languages: one
    for sensitivity which leverages linear typing with scaling a la Fuzz, and one for privacy which
    leverages linear typing without scaling and is novel in this work.
Before describing the syntax, semantics and types for each of Duet’s two languages, we first
provide some context which motivates each design decision made. We do this through several
small examples and type signatures drawn from state-of-the-art type systems such as Fuzz [44],
HOARe2 [8] and Azevedo de Amorim et al’s path construction [21].

3.1    Design Challenges
   Higher-Order Programming. An important design goal of Duet is to support sensitivity analysis of
higher-order, general purpose programs. Prior work (Fuzz and HOARe2 ) has demonstrated exactly
this, and we build on their techniques. In Fuzz, the types for the higher-order map function and a
list of reals named xs looks like this:
                               map : (τ1 ⊸s τ2 ) ⊸∞ list τ1 ⊸s list τ2
                                 xs : list R
The type of map reads: “Take as a first argument an s-sensitive function from τ1 to τ2 which map is
allowed to use as many times as it wants. Take as second argument a list of τ1 , and return a result
list of τ2 which is s-sensitive in the list of τ1 .” Two programs that use map might look like this:
                                        map (λ x → x + 1) xs                 (1)
                                        map (λ x → x + x) xs                 (2)
The Fuzz type system reports that (1) is 1-sensitive in xs, and that (2) is 2-sensitive in xs. To arrive at
this conclusion, the Fuzz type checker is essentially counting how many times x is used in the body
of the lambda, and type soundness for Fuzz means that these counts correspond to the semantic
property of function sensitivity.
   In HOARe2 the type for map is instead:
map : (∀s ′ . {x :: τ1 | Dτ1 (x ◁ , x ▷ ) ≤ s ′ } → {y :: τ2 | Dτ2 (y◁ , y▷ ) ≤ s · s ′ })
   → ∀s ′ . {xs :: list τ1 | D(l ist τ1 ) (xs ◁ , xs ▷ ) ≤ s ′ } → {y :: list τ2 | D(list τ2 ) (ys ◁ , ys ▷ ) ≤ s · s ′ }
This type for map means the same thing as the Fuzz type shown above, and HOARe2 likewise
reports that (1) is 1-sensitive and (2) is 2-sensitive, each in xs, and where Dτ is some family of
distance metrics indexed by types τ . To arrive at this conclusion, HOARe2 generates relational
verification conditions (where, e.g., x ◁ is drawn from a hypothetical “first/left run” of the program,
and x ▷ is drawn from a hypothetical “second/right run” of the program) which are discharged by
an external solver (e.g., SMT). In this approach, sensitivity is not concluded via an interpretation of
a purely syntactic type system (e.g., linear typing in Fuzz), rather the relational semantic property
of sensitivity (and its scaling) is embedded directly in the relational refinements of higher-order
function types.
   In designing Duet, we follow the design of Fuzz in that programs adhere to a linear type
discipline, i.e., the mechanics of our type system is based on counting variables and (in some cases)
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
8                                Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
scaling, and we prove a soundness theorem that says well-typed programs are guaranteed to be
sensitive/private programs. Our type for map is identical to the one shown above for Fuzz.
  Non-Linear Scaling. Fuzz encodes an ϵ-differentially private function as an ϵ-sensitive function
which returns a monadic type ⃝ τ . The Laplace differential privacy mechanism is then encoded in
Fuzz as an ϵ-sensitive function from R to ⃝ R:
                                         laplace : R ⊸ϵ ⃝ R
Because the metric on distributions for pure ϵ-differential privacy scales linearly, laplace can be
applied to a 2-sensitive argument to achieve 2ϵ-differential privacy, e.g.:
                                            laplace (x + x)
gives 2ϵ-differential privacy for x. Adding more advanced variants of differential privacy like (ϵ, δ )
to Fuzz has proved challenging because these variants do not scale linearly. Azevedo de Amorim
et al’s path construction successfully adds (ϵ, δ )-differential privacy to Fuzz by tracking privacy
“cost” as an index on the monadic type operator ⃝ϵ,δ . However, in order to interpret a function
application like the one shown, the group privacy property for (ϵ, δ )-differential privacy must be
used, which results in undesirable non-linear scaling of the privacy cost. The derived bound for this
program using group privacy (for k = 2) is not (2ϵ, 2δ ) but (2ϵ, 2e ϵ δ ) [25]. As a result, achieving
a desired ϵ and δ by treating an s-sensitive function as 1-sensitive and leveraging group privacy
requires adding much more noise than simply applying the Gaussian mechanism with a sensitivity
of s.
   In HOARe2 , the use of scaling which might warrant the use of group privacy is explicitly dis-
allowed in the stated relational refinement type. This is in contrast to sensitivity, which likewise
must explicitly allow arbitrary scaling. The type for gauss in HOARe2 (the analogous mechanism to
laplace in the (ϵ, δ )-differential privacy setting) is written:
                            gauss : {x :: R | DR (x ◁ , x ▷ ) ≤ 1} → Mϵ,δ R
Notice the assumed sensitivity of x to be bounded by 1, not some arbitrary s ′ to be scaled in the
output refinement (as was seen in the type for map in HOARe2 above). In this way, HOARe2 is able
to restrict uses of gauss to strictly 1-sensitive arguments, a restriction that is not possible in a pure
linear type system where arbitrary program composition is allowed and interpreted via scaling.
   In Duet, we co-design two languages which are mutually embedded inside one another. The
sensitivity language is nearly identical to Fuzz, supports arbitrary scaling, and is never interpreted
to mean privacy. The privacy language is also linearly typed, but restricts function call parameters
to be strictly 1-sensitive—a property established in the sensitivity fragment. The gauss mechanism
in Duet is (essentially) given the type:
                                       gauss : R@⟨ϵ, δ ⟩ ⊸∗ R
where ⊸∗ is the function space in Duet’s privacy language, and the annotation @⟨ϵ, δ ⟩ tracks the
privacy cost of that argument following a linear typing discipline.
   Multiple Private Parameters. Both HOARe2 and the path construction track (ϵ, δ )-differential
privacy via an indexed monadic type, notated Mϵ,δ and ⃝ϵ,δ respectively. E.g., a program that
returns an (ϵ, δ )-differentially private real number has the type Mϵ,δ (R) in HOARe2 . These monadic
approaches to privacy inherently follow an “effect” type discipline, and as a result the monad index
must track the sum total of all privacy costs to any parameter. For example, a small program that
takes two parameters, applies a mechanism to enforce differential privacy for each parameter, and
adds them together, will report a double-counting of privacy cost. E.g., in this HOARe2 program
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                                   9
(translated to Haskell-ish “do”-notation):
           let f = λ x y → do { r 1 ← дaussϵ,δ x ; r 2 ← дaussϵ,δ y ; return (r 1 + r 2 ) }

The type of f in HOARe2 reports that it costs (2ϵ, 2δ ) privacy:
              f : {x :: R | DR (x ◁ , x ▷ ) ≤ 1} → {y :: R | DR (y◁ , y▷ ) ≤ 1} → M2ϵ,2δ R

This bound is too conservative in many cases: it is the best bound in the case that f is applied to the
same variable for both arguments (e.g., in f a a), however, if f is applied to different variables (e.g.,
in f a b) then a privacy cost of (2ϵ, 2δ ) is still claimed, interpreted as for either or both variables
2ϵ, 2δ privacy is consumed. A better accounting of privacy in this second case should report (ϵ, δ )-
differential privacy independently for both variables a and b, and such accounting is not possible in
either HOARe2 or the path construction.
   In Duet, we track privacy following a co-effect discipline (linear typing without scaling), as
opposed to an effect discipline, in order to distinguish privacy costs independently for each variable.
The type of the above program in Duet is:
                                   f : (R@⟨ϵ, δ ⟩, R@⟨ϵ, δ ⟩) ⊸∗ R

indicating that f “costs” (ϵ, δ ) for each parameter independently, and only when f is called with
two identical variables as arguments are they combined as (2ϵ, 2δ ).
  Due to limitations of linear logic in the absence of scaling, privacy lambdas must be multi-
argument in the core design of Duet—they cannot be recovered by single-argument lambdas. As a
consequence, our privacy language is not Cartesian closed.

3.2   Duet by Example
  Sensitivity. Duet consists of two languages: one for tracking sensitivities (typeset in green),
and one for tracking privacy cost (typeset in red). The sensitivity language is similar to that of
DFuzz [29]; its typing rules track the sensitivity of each variable by annotating the context. For
example, the expression x + x is 2-sensitive in x; the typing rules in Figure 4 allow us to conclude:
                                         {x :2 R} ⊢ x + x : R

In this case, the context {x :2 R} tells us that the expression is 2-sensitive in x. The same idea works
for functions; for example:
                                    ∅ ⊢ λx : R ⇒ x + x : R ⊸2 R

Here, the context is empty; instead, the function’s sensitivity to its argument is encoded in an
annotation on its type (the 2 in R ⊸2 R). Applying such a function to an argument scales the
sensitivity of the argument by the sensitivity of the function. This kind of scaling is appropriate for
sensitivities, and even has the correct effect for higher-order functions. For example:
                {y :2 R} ⊢ (λx : R ⇒ x + x) y : R
                {y :4 R} ⊢ (λx : R ⇒ x + x) (y + y) : R
                {y :4 R, z :2 R} ⊢ (λx : R ⇒ x + x) (y + y + z) : R
                {y :1 R} ⊢ λx : R ⇒ y : R ⊸0 R
                {y :1 R, z :0 R} ⊢ (λx : R ⇒ y) z : R
                {y :2 R, z :0 R} ⊢ (λ f : R ⊸0 R ⇒ (f z) + (f z)) (λx : R ⇒ y) : R
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
10                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
  Privacy. Differentially private mechanisms like the Gaussian mechanism [25] specify how to add
noise to a function with a particular sensitivity in order to ensure differential privacy. In Duet,
such mechanisms form the interface between the sensitivity language and the privacy language.
For example:
                          {x :ϵ,δ R} ⊢ gauss[R+ [2.0], ϵ, δ ] <x > {x + x } : R
In a gauss expression, the first three elements (inside the square brackets) represent the maximum
allowed sensitivity of variables in the expression’s body, and the desired privacy parameters ϵ and
δ . The fourth element (here, <x >) is a list of variables whose privacy we are interested in tracking.
Variables not in this list will be assigned infinite privacy cost.
    The value of the gauss expression is the value of its fifth element (the “body”), plus enough noise
to ensure the desired level of privacy. The body of a gauss expression is a sensitivity expression, and
the gauss expression is well-typed only if its body typechecks in a context assigning a sensitivity
to each variable of interest which does not exceed the maximum allowed sensitivity. For example,
the expression gauss[R+ [1.0], ϵ, δ ] <x > {x + x } is not well-typed, because x + x is 2-sensitive in
x, but the maximum allowed sensitivity is 1.
    Privacy expressions like the example above are typed under a privacy context which records
privacy cost for individual variables. The context for this example ({x :ϵ,δ R}) says that the
expression provides (ϵ, δ )-differential privacy for the variable x. Tracking privacy costs using a
co-effect discipline allows precise tracking of the privacy cost for programs with multiple inputs:
                    {x :ϵ,δ R, y :ϵ,δ R} ⊢ gauss[R+ [1.0], ϵ, δ ] <x, y> {x + y} : R
The Bind rule encodes the sequential composition property of differential privacy. For example:
     {x :2ϵ,2δ R} ⊢                                    {x :ϵ,δ R, y :ϵ,δ R} ⊢
          v 1 ← gauss[R+ [1.0], ϵ, δ ] <x > {x } ;          v 1 ← gauss[R+ [1.0], ϵ, δ ] <x > {x } ;
          v 2 ← gauss[R+ [1.0], ϵ, δ ] <x > {x } ;          v 2 ← gauss[R+ [1.0], ϵ, δ ] <y> {y} ;
          return v 1 + v 2                                  return v 1 + v 2
     :R                                                :R
In the example on the left, the Gaussian mechanism is applied to x twice, so the total privacy cost
for x is (2ϵ, 2δ ). In the example on the right, x and y are each used once, and their privacy costs are
tracked separately. The Return rule provides a second interface between the sensitivity and privacy
languages: a return expression is part of the privacy language, but its argument is a sensitivity
expression. The value of a return expression is exactly the value of its argument, so the variables
used in its argument are assigned infinite privacy cost. return expressions are therefore typically
used to compute on values which are already differentially private (like v 1 and v 2 above), since
infinite privacy cost is not a problem in that case.
   Gradient descent. Machine learning problems are typically defined in terms of a loss function
L(θ ; X , y) on a model θ , training samples X = (x 1 , x 2 , ..., x n ) (in which each sample is typically
represented as a feature vector) and corresponding labels y = (y1 , y2 , ..., yn ) (i.e. the prediction
target). The training task is to find a model θˆ which minimizes the loss on the training samples (i.e.
θˆ = argminθ L(θ ; X , y).
   One solution to the training task is gradient descent, which starts with an initial guess for θ
and iteratively moves in the direction of an improved θ until the current setting is close to θˆ. To
determine which direction to move, the algorithm evaluates the gradient of the loss, which yields a
vector representing the direction of greatest increase in L(θ ; X , y). Then, the algorithm moves in
the opposite direction.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      11
   To ensure differential privacy for gradient-based algorithms, we need to bound the sensitivity of
the gradient computation. The gradients for many kinds of convex loss functions are 1-Lipschitz [54]:
if each sample in X = (x 1 , ..., x n ) has bounded L2 norm (i.e. ∥x i ∥2 ≤ 1), then for all models θ and
labelings y, the gradient ∇(θ ; X , y) has L2 sensitivity bounded by 1. For now, we will assume the
existence of a function called gradient with this property (more details in Section 4).
           gradient : MUL2 [1, n] R ⊸∞ MUL∞ [m, n] D ⊸ 1 MUL∞ [m, 1] D ⊸ 1 MUL2 [1, n] R
                                                                  m                       m

The function’s arguments are the current θ , a m × n matrix X containing n training samples, and a
1 × n matrix y containing the corresponding labels. In Duet, the type MUL∞ [m, n] D represents a
m × n matrix of discrete real numbers; neighboring matrices of this type differ arbitrarily in a single
row. The function’s output is a new θ of type MUL2 [1, n] R, representing a matrix of real numbers
with bounded L2 sensitivity (see Section 4 for details on matrix types). We can use the gradient
function to implement a differentially private gradient descent algorithm:
                        noisy-gradient-descent(X , y, k, ϵ, δ ) ≜
                          let θ 0 = zeros (cols X 1 ) in
                          loop[δ ′] k on θ 0 <X 1 , y> {t, θ ⇒
                               дp ← mgauss[ m1 , ϵ, δ ] <X , y> {gradient θ X y} ;
                               return θ − дp }
The arguments to our algorithm are the training data (X and y), the desired number of iterations
k, and the privacy parameters ϵ and δ . The first line constructs an initial model θ 0 consisting of
zeros for all parameters. Lines 2-4 represent the iterative part of the algorithm: k times, compute
the gradient of the loss on X and y with respect to the current model, add noise to the gradient
using the Gaussian mechanism, and subtract the gradient from the current model (thus moving in
the opposite direction of the gradient) to improve the model.
   The typing rules presented in Figure 4 allow us to derive a privacy bound for this algorithm
which is equivalent to manual proof of Bassily et al. [14]. Based on the type of the gradient function,
the ⊸-E rule allows us to conclude that the gradient operation is m1 -sensitive in the training data,
which is reflected by the sensitivity annotations in the context:
                        {θ :∞ τ1 , X : 1 τ2 , y : 1 τ3 } ⊢ gradient θ X y : MUL2 [1, n] R
                                       m         m
                        where τ1 = MUL2 [1, n] R
                              τ2 = MUL∞ [m, n] D
                              τ3 = MUL∞ [m, 1] D
Next, the MGauss rule represents the use of the Gaussian mechanism, and transitions from the
sensitivity language (implementing the gradient) to the privacy language (in which we use the
noisy gradient). The rule allows us to conclude that since the sensitivity of the gradient computation
is m1 , our use of the Gaussian mechanism satisfies (ϵ, δ )-differential privacy. This context is a privacy
context, and its annotations represent privacy costs rather than sensitivities.
                                                          1
      {θ :∞ τ1 , X : ⟨ϵ,δ ⟩ τ2 , y : ⟨ϵ,δ ⟩ τ3 } ⊢ mgauss[ , ϵ, δ ] <X , y> {gradient θ X y} : MUL2 [1, n] R
                                                          m
Finally, the Loop rule for advanced composition allows us to derive a bound on the total privacy cost
of the iterative algorithm, based on the number of times the loop runs:
  {θ :∞ τ1 , X : ⟨ϵ ′p
                     ,kδ +δ ′ ⟩ τ2 , y : ⟨ϵ ′,kδ +δ ′ ⟩ τ3 } ⊢ loop[δ ] k on θ 0 <X 1 , y> {t, θ ⇒ ...} : ML2 [1, n] R
                                                                     ′                                     U

  where ϵ = 2ϵ 2k log(1/δ )
           ′                           ′
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
12                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
   Variants of Differential Privacy. The typing rules presented in Figure 4 are specific to (ϵ, δ )-
differential privacy, but the same framework can be easily extended to support the other variants
described in Figure 1. New variants can be supported by making three simple changes: (1) Modify
the privacy cost syntax p to describe the privacy parameters of the new variant; (2) Modify the
sum operator + to reflect sequential composition in the new variant; and (3) Modify the typing
for basic mechanisms (e.g. gauss) to reflect corresponding mechanisms in the new variant. The
extended version of this paper includes typing rules for the variants in Figure 1.
   As an example, considering the following variant of the noisy gradient descent algorithm pre-
sented earlier, but with ρ-zCDP instead of (ϵ, δ )-differential privacy. There are only two differences:
the loop construct under zCDP has no δ ′ parameter, since standard composition yields tight bounds,
and the mgauss construct has a single privacy parameter (ρ) instead of ϵ and δ .

                         noisy-gradient-descent(X , y, k, ρ) ≜
                           let θ 0 = zeros (cols X 1 ) in
                           loop k on θ 0 <X 1 , y> {t, θ ⇒
                                дp ← mgauss[ m1 , ρ] <X , y> {gradient θ X y} ;
                                return θ − дp }

Typechecking for this version proceeds in the same way as before, with the modified typing rules;
the resulting privacy context gives both X and y a privacy cost of kρ.

   Mixing Variants. Duet allows mixing variants of differential privacy in a single program. For
example, the total privacy cost of an algorithm is often given in (ϵ, δ ) form, to enable comparing
the costs of different algorithms; we can use this feature of Duet to automatically derive the cost
of our zCDP-based gradient descent in terms of ϵ and δ .

                     noisy-gradient-descent(X , y, k, ρ, δ ) ≜
                       let θ 0 = zeros (cols X 1 ) in
                       ZCDP [δ ] { loop k on θ 0 <X 1 , y> {t, θ ⇒
                                    дp ← mgauss[ m1 , ρ] <X , y> {gradient θ X y} ;
                                    return θ − дp } }

The ZCDP {...} construct represents embedding a mechanism which satisfies ρ-zCDP in another
mechanism which provides (ϵ, δ )-differential privacy. The rule for typecheckingpthis construct
encodes the property that if a mechanism satisfies ρ-zCDP, it also satisfies (ρ + 2 ρ log(1/δ ), δ )-
differential privacy [16]. Using this rule, we can derive a total privacy cost for the gradient descent
algorithm in terms of ϵ and δ , but using the tight bound on composition that zCDP provides.

{X : ⟨ϵ ′,δ ⟩ τ2 , y : ⟨ϵ ′,δp⟩ τ3 , k :∞ R+ [k], ρ :∞ R+ [ρ]} ⊢ noisy-gradient-descent(X , y, k, ρ, δ ) : MUL2 [1, n] R
where ϵ ′ = kρ + 2 kρ log(1/δ )

We might also want to nest these conversions. For example, when the dimensionality of the training
data is very small, the Laplace mechanism might yield more accurate results than the Gaussian
mechanism (due to the shape of the distribution). To use the Laplace mechanism in an iterative
algorithm which satisfies zCDP, we can use the fact that any ϵ-differentially private mechanism
also satisfies 12 ϵ 2 -zCDP; by nesting conversions, we can determine the total cost of the algorithm
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      13
in terms of ϵ and δ .
          noisy-gradient-descent(X , y, k, ϵ, δ ) ≜
              let θ 0 = zeros (cols X 1 ) in
              ZCDP [δ ] { loop k on θ 0 <X 1 , y> {t, θ ⇒
                           дp ← EPS_DP { mlaplace[ m1 , ϵ] <X , y> {gradient θ X y} } ;
                           return θ − дp } }
                                 τ3 , k :∞ R+ , ρ :∞ R+ } ⊢ noisy-gradient-descent(X , y, k, ϵ, δ ) : MUL2 [1, n] R
  {X : ⟨ϵ ′,δ ⟩ τ2 , y : ⟨ϵ ′,δ ⟩q
  where ϵ ′ = 12 kϵ 2 + 2    1   2
                             2 kϵ log(1/δ )

Such nestings are sometimes useful in practice: in Section 5, we will define a variant of the
Private Frank-Wolfe algorithm which uses the exponential mechanism (which satisfies ϵ-differential
privacy) in a loop for which composition is performed with zCDP, and report the total privacy cost
in terms of ϵ and δ .
   Contextual Modal Types. A new problem arises in the design of Duet governing the interaction
of sensitivity and privacy languages: in general—and for very good reasons which are detailed in
the next section—let-binding intermediate results in the privacy language doesn’t always preserve
typeability. Not only is let-binding intermediate results desirable for code readability, it can often
be essential in order to achieve desirable performance. Consider a loop body which performs an
expensive operation that does not depend on the inner-loop parameter:
                          λ xs θ 0 → loop k times on θ 0 { θ →
                                          gaussϵ,δ (f (expensive xs) θ )) }
A simple refactoring achieves much better performance:
                            λ xs θ 0 → let temp = expensive xs in
                                       loop k times on θ 0 { θ →
                                            gaussϵ,δ (f temp θ ) }
However instead of providing (ϵ, δ )-differential privacy for xs, as was the case before the refactor,
the new program provides (ϵ, δ )-differential privacy for temp—an intermediate variable we don’t
care about—and makes no guarantees of privacy for xs.
  To accommodate this pattern we borrow ideas from contextual modal type theory [40] to allow
“boxing” a sensitivity context, and “unboxing” that context at a later time. In terms of differential
privacy, the argument that the above loop is differentially private relies on the fact that temp ≡
expensive(xs) is 1-sensitive in xs (assuming expensive is 1-sensitive), a property which is lost by
the typing rule for let in the privacy language. We therefore “box” this sensitivity information
outside the loop, and “unbox” it inside the loop, like so:
                          λ xs θ 0 → let temp = box (expensive xs) in
                                      loop k times on θ 0 { θ →
                                           gaussϵ,δ (f (unbox temp) θ ) }
In this example, the type of temp is a □[xs@1] data (a “box of data 1-sensitive in xs”) indicating
that when unboxed, temp will report 1-sensitivity w.r.t xs, not temp. f is then able to make good
on its promise to gauss that the result of f is 1-sensitive in xs (assuming f is 1-sensitive in its first
argument), and gauss properly reports its privacy “cost” in terms of xs, not temp.
   We use exactly this pattern in many of our case studies, where expensive is a pre-processing
operation on the input data (e.g., clipping or normalizing), and f is a machine-learning training
operation, such as computing an improved model based on the current model θ and the pre-
processed input data temp.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
14                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
                       m, n ∈ N          r ∈R                rÛ, ϵ, δ ∈ R+          x, y ∈ var
                         s ∈ sens F rÛ | ∞                              p ∈ priv F ϵ, δ | ∞
                    τ ∈ type F N | R | N[n] | R+ [Ûr ] | box[Γs ] τ              numeric and box
                              | τ ⊸s τ | (τ @p, ..., τ @p) ⊸∗ τ                  functions
                   Γs ∈ tcxts ≜ var ⇀ sens × type F {x :s τ , ..., x :s τ }      sens. contexts
                   Γp ∈ tcxtp ≜ var ⇀ priv × type F {x :p τ , ..., x :p τ }      priv. contexts
                    es ∈ exps F N[n] | N[Ûr ] | n | r | real e                 numeric literals
                              | e + e | e − e | e · e | 1/e | e mod e          arithmetic
                              | x | let x = e in e | e e                       let/sens. app.
                              | sλ x : τ ⇒ e | pλ (x : τ , ..., x : τ ) ⇒ e    sens./priv. fun.
                              | box e | unbox e                                sensitivity capture
                    ep ∈ expp F return e | x ← e ; e | e(e, ..., e)            ret/bind/priv. app.
                              | loop[e] e on e <x, ..., x > {x, x ⇒ e}         finite iteration
                              | gauss[e, e, e] <x, ..., x > {e}                gaussian noise
                                           Fig. 3. Core Types and Terms


3.3   Duet Syntax & Typing Rules
Figure 3 shows a core subset of syntax for both languages. We only present the privacy fragment
for (ϵ, δ )-differential privacy in the core formalism, although support for other variants (and
combined variants) is straightforward as sketched in the previous section. See the extended version
of this paper for the complete presentation of the full language including all advanced variants of
differential privacy. We use color coding to distinguish between the sensitivity language, privacy
language, and shared syntax between languages. The sensitivity and privacy languages share
syntax for variables and types, which are typeset in blue. Expressions in the sensitivity language
are typeset in green, while expressions in the privacy language are typeset in red.1
   Types τ include base numeric types N and R and their treatment is standard. We include singleton
numeric types N[n] and R+ [Ûr ]; these types classify runtime numeric values which are identical to
the static index n or rÛ, e.g., N[n] is a type which exactly describes its runtime value as the number n.
Static reals only range over non-negative values, and we write rÛ for elements of the non-negative
reals R+ . Singleton natural numbers are used primarily to construct matrices with some statically
known dimension, and to execute loops for some statically known number of iterations. Singleton
real numbers and are used primarily for tracking sensitivity and privacy quantities. Novel in Duet
is a “boxed” type box[Γs ] τ which delays the “payment” of a value’s sensitivity, to be unboxed
and “paid for” in a separate context. Boxing is discussed in more detail later in this section. The
sensitivity function space (a la Fuzz) is written τ1 ⊸s τ2 and encodes an s-sensitive function from τ1
to τ2 . The privacy function space (novel in Duet) is written (τ1 @p1 , ..., τn @pn ) ⊸∗ τ and encodes a
multi-arity function that preserves pi -privacy for its ith argument. Privacy functions are multi-arity
because functions of multiple arguments cannot be recovered from iterating functions over single
arguments in the privacy language, as can be done in the sensitivity language.
   In our implementation and extended presentation of Duet in the extended version of this paper,
we generalize the static representations of natural numbers and reals to symbolic expression η,
which may be arbitrary symbolic polynomial formulas including variables. E.g., suppose ϵ is a
type-level variable ranging over real numbers and x:N[ϵ], then 2x:N[2ϵ]. Our type checker knows
this is the same type as N[ϵ+ϵ] using a custom solver we implemented but do not describe in

1 Colors were chosen to minimize ambiguity for colorblind persons following a colorblind-friendly palette: http://mkweb.

bcgsc.ca/colorblind/img/colorblindness.palettes.png
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      15

                                                                                                                                             Γ ⊢e :τ
                                                                                                   Real-S                            Real-D
Nat            Real                Singleton Nat                Singleton Real
                                                                                                       Γ ⊢ e : N[n]                         Γ ⊢e :N
                                                                     +             +                                   +
⊢n:N             ⊢r :R             ⊢ N[n] : N[n]                 ⊢ R [Ûr ] : R [Ûr ]               ⊢ real e : R [n]                   Γ ⊢ real e : R
      Times-DS                                                 Mod-DS
                                          +                                                           +
       Γ1 ⊢ e 1 : R       Γ2 ⊢ e 2 : R [Ûr ]                    Γ1 ⊢ e 1 : R           Γ2 ⊢ e 2 : R [Ûr ]                   Var

                                                                            rÛ
                rÛΓ1 ⊢ e 1 · e 2 : τ                             ⌉Γ1 ⌈ ⊢ e 1 mod e 2 : τ                 {x :1 τ } ⊢ x : τ
               Let                                                             ⊸-I
               Γ1 ⊢ e 1 : τ1           Γ2 ⊎ {x :s τ1 } ⊢ e 2 : τ2                     Γ ⊎ {x :s τ1 } ⊢ e : τ2
                 sΓ1 + Γ2 ⊢ let x = e 1 in e 2 : τ2                                        Γ ⊢ (λ x : τ1 ⇒ e) : τ1 ⊸s τ2
 ⊸-E                                       ⊸∗ -I
 Γ1 ⊢ e 1 : τ1 ⊸s τ2     Γ2 ⊢ e 2 : τ1                                           Γ ⊎ {x 1 :p1 τ1 , ..., x n :pn τn } ⊢ e : τ
                                                               ∞
         Γ1 + sΓ2 ⊢ e 1 e 2 : τ2                         ⌉Γ ⌈      ⊢ (pλ (x 1 : τ1 , ..., x n : τn ) ⇒ e) : (τ1 @p1 , ..., τn @pn ) ⊸∗ τ
            Box-I                                       Box-E                                                  Sub
                    Γ ⊢e :τ                                  Γ ⊢ e : box[Γ ′ ] τ                               Γ1 ⊢ e : τ         Γ1 ≤ Γ2
             ⊢ box e : box[Γ] τ                          Γ + Γ ′ ⊢ unbox e : τ                                        Γ2 ⊢ e : τ

                    Return                                             Bind                                                                  Γ ⊢e :τ
                             Γ ⊢e :τ                                     Γ1 ⊢ e 1 : τ1         Γ2 ⊎ {x :∞ τ1 } ⊢ e 2 : τ2
                    ⌉Γ⌈∞ ⊢ return e : τ                                             Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
                    ⊸∗ -E
                    Γ ⊢ e : (τ1 @p1 , ..., τn @pn ) ⊸∗ τ                   ⌉Γ1 ⌈1 ⊢ e 1 : τ1         ···        ⌉Γn ⌈1 ⊢ en : τn
                                         ⌉Γ⌈∞ + ⌉Γ1 ⌈p1 + ··· + ⌉Γn ⌈pn ⊢ e(e 1 , ..., en ) : τ
   Loop (Advanced Composition)
   Γ1 ⊢ e 1 : R+ [δ ′ ]     Γ2 ⊢ e 2 : N[n]             Γ3 ⊢ e 3 : τ             Γ4 + ⌉⌊Γ4′⌋⌈ϵ,δ
                                                                                             {x ′ , ...,x ′ }
                                                                                                              ⊎ {x 1 :∞ N, x 2 :∞ τ } ⊢ e 4 : τ
                                                                                               1           n
                                          √
             ∞           ∞            2ϵ 2n ln(1/δ ′ ),δ ′ +nδ
        ⌉Γ3 ⌈ + ⌉Γ4 ⌈        + ⌉⌊Γ4′⌋⌈ {x ′ , ...,x ′ }        ⊢ loop[e 1 ] e 2 on e 3 <x 1′ , ..., x n′ > {x 1 , x 2 ⇒ e 4 } : τ
                                          1        n
           Gauss
                         +
            Γ1 ⊢ e 1 : R [Ûr s ]         Γ2 ⊢ e 2 : R+ [ϵ]           Γ3 ⊢ e 3 : R+ [δ ]            Γ4 + ⌉⌊Γ4′⌋⌈r{x
                                                                                                                Ûs
                                                                                                                   , ...,x }
                                                                                                                             ⊢ e4 : R
                                                                                                                      1     n

                             ⌉Γ4 ⌈∞ + ⌉⌊Γ4′⌋⌈ϵ,δ
                                             {x ′ , ...,x ′ }
                                                              ⊢ gauss[e 1 , e 2 , e 3 ] <x 1′ , ..., x n′ > {e 4 } : R
                                                  1      n


                                                       Fig. 4. Core Typing Rules


this paper. Because the typelevel representation of a natural number can be a variable, its value is
therefore not statically determined, rather it is statically tracked via typelevel symbolic formulas.
   Type contexts in the sensitivity language Γs track the sensitivity s of each free variable whereas
in the privacy language Γp they track privacy cost p. Sensitivities are non-negative reals rÛ extended
with a distinguished infinity element ∞, and privacy costs are specific to the current privacy mode.
In the case of (ϵ, δ )-differential privacy, p has the form ϵ, δ or ∞ where ϵ and δ range over R+ .
   We reuse notation conventions from Fuzz for manipulating contexts, e.g., Γ1 +Γ2 is partial and
defined only when both contexts agree on the type of each variable; adding contexts adds sensitivities
pointwise, i.e., {x:s1 +s2 τ } ∈ Γ1 +Γ2 when {x:s1 τ } ∈ Γ1 and {x:s2 τ } ∈ Γ2 ; and scaling contexts scales
sensitivities pointwise, i.e., {x:ss ′ τ } ∈ sΓ when {x:s ′ τ } ∈ Γ.
   We introduce a new operation not shown in prior work called truncation and written ⌉s 1 ⌈s2 for
truncating a sensitivity and ⌉Γ ⌈s for truncating a sensitivity context, which is pointwise truncation
of sensitivities. Sensitivity truncation ⌉ ⌈s maps 0 to 0 and any other value to s:
                                                                                0 if s 1 = 0
                                                                              
                  ⌉ ⌈ ∈ sens × sens → sens                         ⌉s 1 ⌈s2 ≜
                                                                               s 2 if s 1 , 0
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
16                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
Truncation is defined analogously for privacies ⌉p1 ⌈p2 , for converting between sensitivities and
privacies ⌉s ⌈p and ⌉p ⌈s , and also for liftings of these operations pointwise over contexts ⌉Γ ⌈p , ⌉Γ⌈p
and ⌉Γ⌈s . Sensitivity truncation is used for typing the modulus operator, and truncating between
sensitivities and privacies is always to ∞/∞ and appears frequently in typing rules that embed
sensitivity terms in privacy terms and vice versa.
   The syntax and language features for both sensitivity and privacy languages are discussed next
alongside their typing rules. Figure 4 shows a core subset of typing rules for both languages. In the
typing rules, the languages embed within each other—sensitivity typing contexts are transformed
into privacy contexts and vice versa. Type rules are written in logical style with an explicit sub-
sumption rule, although a purely algorithmic presentation is possible (not shown) following ideas
from Azevedo de Amorim et al [20] which serves as the basis for our implementation.

3.4   Sensitivity Language
Duet’s sensitivity language is similar to that of DFuzz [29], except that we extend it with significant
new tools for machine learning in Section 4. We do not present standard linear logic connectives
such as sums, additive products and multiplicative products (a la Fuzz), or symbolic type-level
expressions (a la DFuzz), although each are implemented in our tool and described formally in
the extended version of this paper. We do not formalize or implement general recursive types in
order to ensure that all Duet programs terminate. Including general recursive types would be
straightforward in Duet (following the design of Fuzz), however such a decision comes with known
limitations. As described in Fuzz [44], requiring that all functions terminate is necessary in order to
give both sound and useful types to primitives like set-filter. The design space for the combination
of sensitivity types and nontermination is subtle, and discussed extensively in prior work [4, 44].
   Typing for literal values is immediate (Nat, Real). Singleton values are constructed using the same
syntax as their types, and where the type level representation is identical to the literal (Singleton Nat,
Singleton Real). Naturals can be converted to real numbers through the explicit conversion operation
real (Real-S, Real-D). For the purposes of sensitivity analysis, statically known numbers are considered
constant, and as a consequence any term that uses one is considered 0-sensitive in the statically
known term. The result of this is that the sensitivity environment Γ associated with the subterm at
singleton type is dropped from the output environment, e.g., in Real-S. This dropping is justified
by our metric space interpretation JN[n]K for statically known numbers as singleton sets {n}, and
because for all x, y ∈ JN[n]K, x = y and therefore |x − y| = 0.
   Type rules for arithmetic operations are given in multiple variations, depending on whether or not
each argument is tracked statically or dynamically. We show only the rule for multiplication when
the left argument is dynamic and the right argument is static (Times-DS). The resulting sensitivity
environment reports the sensitivities of e 1 scaled by rÛ—the statically known value of e 2 —and the
sensitivities for e 2 are not reported because its value is fixed and cannot vary, as discussed above.
When both arguments are dynamic, the resulting sensitivity environment is ∞(Γ1 + Γ2 ), i.e., all
potentially sensitive variables for each expression are bumped to infinity. The modulus operation
is similar to multiplication in that we have cases for each variation of static or dynamic arguments,
however the context is truncated rather than scaled in the case of one singleton-typed parameter;
we show only this static-dynamic variant in the figure (Mod-DS).
   Typing for variables (Var) and functions (⊸-I, ⊸-E) is the same as in Fuzz: variables are reported
in the sensitivity environment with sensitivity 1; and closures are created by annotating the arrow
with the sensitivity s of the argument in the body, and by reporting the rest of the sensitivities Γ
from the function body as the sensitivity of whole closure as a whole; and function application
scales the argument by the function’s sensitivity s.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      17
   The first new (w.r.t. DFuzz) term in our sensitivity language is the privacy lambda. Privacy
lambdas are multi-arity (as opposed to single-arity sensitivity lambdas) because the privacy language
does not support currying to recover multi-argument functions. Privacy lambdas are created in the
sensitivity language with pλ (x : τ , ..., x : τ ) ⇒ e and applied in the privacy language with e(e, ..., e).
The typing rule for privacy lambdas (⊸∗ -I) types the body of the lambda in a privacy type context
extended with its formal parameters, and the privacy cost of each parameter is annotated on its
function argument type. Unlike sensitivity lambdas, the privacy cost of variables in the closure
environment are not preserved in the resulting typing judgment. The reason for this is twofold: (1)
the final “cost” for variables in the closure environment depends on how many times the closure is
called, and in the absence of this knowledge, we must conservatively assume that it could be called
an infinite number of times, and (2) the interpretation of an ∞-sensitive function coincides with
that of an ∞-private function, so we can soundly convert between ∞-privacy-cost and ∞-sensitivity
contexts freely using truncation.
   The final two new terms in our sensitivity language are introduction and elimination forms for
“boxes” (Box-I and Box-E). Boxes have no operational behavior and are purely a type-level mechanism
for tracking sensitivity. The rules for box introduction capture the sensitivity context of the
expression, and the rule for box elimination pays for that cost at a later time. Boxes are reminiscent
of contextual modal type theory [40]—they allow temporary capture of a linear context via boxing—
thereby deferring its payment—and re-introduction of the context at later time via unboxing. In
a linear type system that supports scaling, this boxing would not be necessary, but it becomes
necessary in our system to achieve the desired operational behavior when interacting with the
privacy language, which does not support scaling. E.g., in many of our examples we perform some
pre-processing on the database parameter (such as clipping) and then use this parameter in the
body of a loop. Without boxing, the only way to achieve the desired semantics is to re-clip the
input (a deterministic operation) every time around the loop—boxing allows you to clip on the
outside of the loop and remember that privacy costs should be “billed” to the initial input.

3.5   Privacy Language
Duet’s privacy language is designed specifically to enable the composition of individual differ-
entially private computations. It has a linear type system, but unlike the sensitivity language,
annotations instead track privacy cost, and the privacy language does not allow scaling of these
annotations, that is, the notation pΓ is not used and cannot be defined. Syntax return e and x←e;e
(pronounced “bind”) are standard from Fuzz, as are their typing rules (Return, Bind), except for our
explicit conversion from a sensitivity context Γ to a privacy context Γ by truncation to infinity in
the conclusion of Return. Bind encodes exactly the post-processing property of differential privacy—it
allows e 2 to use the value computed by e 1 any number of times after paying for it once.
   Privacy application e(e, ..., e) applies a privacy function (pλ, created in the sensitivity language)
to a sequence of 1-sensitivity arguments—the sensitivity is enforced by the typing rule. The type
rule (⊸∗ -E) checks that the first term produces a privacy function and applies its privacy costs to
function arguments which are restricted by the type system to be 1-sensitive. We use truncation in
well-typed hypothesis for e 1 ... en to encode the restriction that the argument must be 1-sensitive.
This restriction is crucial for type soundness—arbitrary terms cannot be given tight privacy bounds
statically due to the lack of a tight scaling operation in the model for (ϵ, δ )-differential privacy. The
same is true for other advanced variants of differential privacy.
   The loop expression is for loop iteration fixed to a statically known number of iterations. The
syntax includes a list of variables (<x, ..., x >) to indicate which variables should be considered
when calculating final privacy costs, as explained shortly. The typing rule (Loop) encodes advanced
composition for (ϵ, δ )-differential privacy. e 1 is the δ ′ parameter to the advanced composition bound
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
18                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
and e 2 is the number of loop iterations—each of these values must be statically known, which we
encode with singleton types (a la DFuzz). Statically known values are fixed and their sensitivities do
not appear in the resulting context. e 3 is the initial value passed to the loop, and for which no claim
is made of privacy, indicated by truncation to infinity. e 4 is a loop body with free variables x 1 and x 2
which will be iterated e 2 times with the first variable bound to the iteration index, and the second
variable bound to the loop state, where e 3 is used as the starting value. The loop body e 4 is checked
in a privacy context Γ4 + ⌉⌊Γ4′⌋⌈ϵ,  δ
                                   {x 1′ , ...,x n′ }
                                                      , shorthand for ⌉ ⌊Γ4′⌋ {x 1′ , ...,x n′ } ⌈ϵ, δ where ⌊Γ4′⌋ {x 1′ , ...,x n′ } is a
context restricted to only the variables x 1′ , ..., x n′ . The ϵ, δ is an upper bound on the privacy cost
of the variables x i′ in the loop body, and the resulting privacy bound is restricted to only those
variables. This allows variables for which the programmer is not interested in tracking privacy
to appear in Γ4 in the premise, and the rule’s conclusion makes no claims about privacy for these
variables. We make use of this feature in all of our examples programs.
   The gauss expression is a mechanism of (ϵ, δ )-differential privacy; other mechanisms are used
for other privacy variants. Like the loop expression, mechanism expressions take a list of variables
to indicate which variables should be considered in the final privacy cost. The typing rule (Gauss)
is similar in spirit to Loop: it takes parameters to the mechanism which must be statically known
(encoded as singleton types), a list of variables to consider for the purposes of the resulting privacy
bound, and a term {e} for which there is a bound rÛ on the sensitivity of free variables x 1 , ..., x n . The
resulting privacy guarantee is that the term in brackets {e} is ϵ, δ differentially private. Whereas
loop and advanced composition consider a privacy term loop body with an upper bound on privacy
leakage, gauss considers a sensitivity term body with an upper bound on its sensitivity.

3.6     Metatheory
We denote sensitivity language terms e ∈ exp into total, functional, linear maps between metric
spaces—the same model as the terminating fragment of Fuzz. Every term in our language terminates
by design, which dramatically simplifies our models and proofs. This restriction poses no issues in
implementing most differentially private machine learning algorithms, because such algorithms
typically terminate in a statically determined number of loop iterations in order to achieve a
particular privacy cost.
   Types in Duet denote metric spaces, as in Fuzz. We notate metric spaces D, their underlying
carrier set ∥D ∥, and their distance metric |x − y|D , or |x − y| where D can be inferred from
context. Sensitivity typing judgments Γ ⊢ e : τ denote linear maps from a scaled cartesian product
interpretation of Γ:
                                            Γ
                              J{x 1 :s1 τ1 ,...,x n :sn τn } ⊢ τ K ≜ !s1 Jτ1 K ⊗ ··· ⊗ !sn Jτn K ⊸ Jτ K
Although we do not make metric space scaling explicit in our syntax (for the purposes of effective
type inference, a la DFuzz [20]), scaling becomes apparent explicitly in our model. Privacy judgments
Γ ⊢ e : τ denote probabilistic, privacy preserving maps from an unscaled product interpretation of Γ:

                                        Γ
                          J{x 1 :p1 τ1 ,...,x n :pn τn } ⊢ τ K ≜ (Jτ1 K@p1 ,...,Jτn K@pn ) ⊸∗ ∥Jτ K∥
The multi-arity (ϵ, δ )-differential-privacy-preserving map is defined:
          (D 1 @(ϵ1 , δ 1 ),...,D n @(ϵn , δn )) ⊸∗ X ≜
                { f ∈ ∥D 1 ∥ × ··· × ∥D n ∥ → D(X )
                | |x i − y|D i ≤ 1 ⇒ Pr[f (x 1 ,...,x i ,...,x n ) = d] ≤ e ϵi Pr[f (x 1 ,...,y,...,x n ) = d] + δi }
where D(X ) is a distribution over elements in X .
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      19
  We give a full semantic account of typing in the extended version of this paper, as well as prove
key type soundness lemmas, many of which appeal to well-known differential privacy proofs from
the literature.
  The final soundness theorem, proven by induction over typing derivations, is that the denotations
for well-typed open terms es and ep in well-typed environments γs and γp are contained in the
denotation of their typing contexts Γs ⊢ τ and Γp ⊢ τ .
    Theorem 3.1.
    (1) If Γp ⊢ ep : τ and Γp ⊢ γp then Jep Kγp ∈ JΓp ⊢ τ K
    (2) If Γs ⊢ es : τ and Γs ⊢ γs then Jes Kγs ∈ JΓs ⊢ τ K
A corollary is that any well-typed privacy lambda function satisfies (ϵ, δ )-differential privacy for
each of its arguments w.r.t. that argument’s privacy annotation used in typing.

4     LANGUAGE TOOLS FOR MACHINE LEARNING
Machine learning algorithms typically operate over a training set of samples, and implementations
of these algorithms often represent datasets using matrices. To express these algorithms, Duet
includes a core matrix API which encodes sensitivity and privacy properties of matrix operations.
   We add a matrix type Mcℓ [m, n] τ , encode vectors as single-row matrices, and add typing rules
for gradient computations that encode desirable properties. We also introduce a type for matrix
indices idx[n] for type-safe indexing. These new types are shown in Figure 6, along with sensitivity
operations on matrices—encoded as library functions because their types can be encoded using
existing connectives—and new matrix-level differential privacy mechanisms—encoded as primitive
syntactic forms because their types cannot be expressed using existing type-level connectives.
   In the matrix type Mcℓ [m, n] τ , the m and n parameters refer to the number of rows and columns
in the matrix, respectively. The ℓ parameter determines the distance metric used for the matrix
metric for the purposes of sensitivity analysis; the c parameter is used to specify a norm bound on
each row of the matrix, which will be useful when applying gradient functions.

4.1    Distance Metrics for Matrices
Differentially private machine learning algorithms typically move from one distance metric on
matrices and vectors to another as the algorithm progresses. For example, two input training
datasets are neighbors if they differ on exactly one sample (i.e. one row of the matrix), but they
may differ arbitrarily in that row. After computing a gradient, the algorithm may consider the
L2 sensitivity of the resulting vector—i.e. two gradients д1 and д2 are neighbors if ∥д1 − д2 ∥2 ≤ 1.
These are very different notions of distance—but the first is required by the definition of differential
privacy, and the second is required as a condition on the input to the Gaussian mechanism.
   The ℓ annotation on matrix types in Duet enables specifying the desired notion of distance
between rows. The annotation is one of L∞, L1, or L2; an annotation of L∞, for example, means
that the distance between two rows is equal to the L∞ norm of the difference between the rows.
The distance between two matrices is always equal to the sum of the distances between rows. The
distance metric for the element datatype τ determines the distance between two corresponding
elements, and the row metric ℓ specifies how to combine elementwise distances to determine the
distance between two rows.
   Figure 5 presents the complete set of distance metrics for matrices, as well as real numbers and
the new domain data for elements of the D type, which is operationally a copy of R but with a
discrete distance metric. Many combinations are possible, including the following common ones:
Ex. 1: |X − X ′ |MU [m, n] D = maxj |X i, j − X i,′ j |D
                              Í
                   L∞
                                 i
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
20                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
                        Domain                 Carrier: X ∈ set
                                                             Metric: | − | ∈ X → X → R ⊎ {∞}
                         real                         R      |r 1 − r 2 | ≜ |r
                                                                             1 − r 2 |R
                                                                               0 when r 1 = r 2
                      data                     R             |r 1 − r 2 | ≜
                                                                               1 when r 1 , r 2
              matrix[n 1 , n 2 ]L∞ (D) M[n 1 , n 2 ](∥D ∥) |m 1 − m 2 | ≜ maxj |m 1 [i, j] − m 2 [i, j]|D
                                                                            Í
                                                                             i
              matrix[n 1 , n 2 ]L1 (D) M[n 1 , n 2 ](∥D ∥) |m 1 − m 2 | ≜ |m 1 [i, j] − m 2 [i, j]|D
                                                                            Í
                                                                            i, j r
              matrix[n 1 , n 2 ]L2 (D) M[n 1 , n 2 ](∥D ∥) |m 1 − m 2 | ≜                                     2
                                                                            Í Í
                                                                                     |m 1 [i, j] − m 2 [i, j]|D
                                                                              i     j

                                               Fig. 5. Distance Metrics for Matrices




Distance is the number of rows on which X and X ′ differ; commonly used to describe neighboring
input datasets.
Ex. 2: |X − X ′ |MU [m, n] R =    |X i, j − X i,′ j |R
                               ÍÍ
                   L1
                                   i       j
Distance is the sum of elementwise differences.
                             Í rÍ
Ex. 3: |X − X |MU [m, n] R =
              ′                    |X i, j − X i,′ j |R2
                   L2
                                   i            j
Distance is sum of the L2 norm
                             rÍof the differences between corresponding rows.
Ex. 4: |X − X |MU [1, n] R =
              ′                |X 1, j − X 1,′ j |R2
                   L2
                                       j
Represents a vector; distance is L2 sensitivity for vectors, as required by the Gaussian mechanism.
  These distance metrics are used in the types of library functions which operate over matrices.

4.2   Matrix Operations
Figure 6 summarizes the matrix operations available in Duet’s API. We focus on the non-standard
operations which are designed specifically for sensitivity or privacy applications. For example,
fr-sens allows converting between notions of distance √ between rows; when converting from L2 to
L1, the distance between two rows may increase by   √ n (by Cauchy-Schwarz), so the corresponding
version of fr-sens has a sensitivity annotation of n.
   undisc allows converting from discrete to standard reals, and is infinitely sensitive. discf allows
converting an infinitely sensitive function which returns a real to a 1-sensitive function returning
a discrete real; we can recover a 1-sensitive function from reals to discrete reals (disc : R ⊸1 D) by
applying discf to the identity function.
   above-threshold encodes the Sparse Vector Technique [25], discussed in Section 5.7. pfld-rows
encodes parallel composition of privacy mechanisms, and is discussed in Section 5.5. sample
performs random subsampling with privacy amplification, and is discussed in Section 5.4.
                                      д
   Gradients are computed using L∇ℓ [ ; , ] and U∇[ ; , ]. The first represents an ℓ-Lipschitz
gradient (typical in convex optimization problems like logistic regression) like the gradient function
introduced in Section 3.2; it is a 1-sensitive function which produces a matrix of real numbers.
The second represents a gradient without a known Lipschitz constant (typical in non-convex
optimization problems, including training neural networks); it produces a matrix of discrete reals.
We demonstrate applications of both in Section 5.
                                                               д
   In order to produce a matrix with sensitivity bound L2, L∇L2 requires input of type ML2   ℓ [m, n] D
for any ℓ. We obtain such a matrix by clipping, a common operation in differentially private machine
learning. Clipping scales each row of a matrix to ensure its c norm (for c ∈ {L∞, L1, L2}) is less
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      21
        ℓ ∈ norm F L1 | L2 | L∞                 c ∈ clip F ℓ | U                τ ∈ type B ... | D | idx[n] | Mcℓ [n, n] τ

               rows : Mcℓ [m, n] τ ⊸0 N[m]                                  convert : Mℓℓ′ [m, n] D ⊸1 MUℓ [m, n] R
                cols : Mcℓ [m, n] τ ⊸0 N[n]                                    clipℓ : Mcℓ′ [m, n] D ⊸1 Mℓℓ′ [m, n] D
               discf : (τ ⊸∞ R) ⊸1 τ ⊸1 D                                fr-sensL∞ : McL∞ [m, n] τ ⊸√n McL2 [m, n] τ
             undisc : D ⊸∞ R                                              fr-sensL2 : McL2 [m, n] τ ⊸√n McL1 [m, n] τ
          transpose : McL1 [m, n] τ ⊸1 MUL1 [n, m] τ                       to-sensℓ : McL1 [m, n] τ ⊸1 Mcℓ [m, n] τ

                  mcreate : N[m] ⊸0 N[n] ⊸0 (idx[m] ⊸∞ idx[n] ⊸∞ τ ) ⊸mn MUL1 [m, n] τ
                  #[ , ] : Mcℓ [m, n] τ ⊸1 idx[m] ⊸∞ idx[n] ⊸∞ τ
             #[ , 7→ ] : Mcℓ [m, n] τ ⊸1 idx[m] ⊸∞ idx[n] ⊸∞ τ ⊸1 MUℓ [m, n] τ
                       fld : (τ1 ⊸s1 τ2 ⊸s2 τ3 ) ⊸mn τ2 ⊸s2mn McL1 [m, n] τ1 ⊸s1 τ2
                      map : (τ1 ⊸s τ2 ) ⊸mn Mcℓ [m, n] τ1 ⊸s MUℓ [m, n] τ2
                  fld-row : (τ1 ⊸s1 τ2 ⊸s2 τ2 ) ⊸m τ2 ⊸s2 m Mcℓ [m, n] τ1 ⊸s1 MUℓ [m, 1] τ2
                map-row : (Mcℓ1 [1, n 1 ] τ1 ⊸s Mcℓ2 [1, n 2 ] τ2 ) ⊸m Mcℓ1 [m, n 1 ] τ1 ⊸s Mcℓ2 [m, n 2 ] τ2
                                 1                  2                     1                    2
               д
             L∇ℓ [ ; , ] : Mℓℓ′ [1, n] R ⊸∞ Mℓℓ′′ [1, n] D ⊸1 D ⊸1 MUℓ [1, n] R
              U∇[ ; , ] : Mℓℓ′ [1, n] R ⊸∞ ML∞  ℓ′′ [1, n] D ⊸ D ⊸ MU [1, n] D
                                                                    1   1    L∞

  above-threshold : (Mcℓ [1, n] (τ ⊸1 R)@∞, R+ [ϵ]@0, τ @⟨ϵ, 0⟩, R@∞) ⊸∗ idx[n]
        pfld-rows : (McL∞
                        1
                           [m, n 1 ] D@⟨ϵ, δ ⟩, McL∞   2
                                                           [m, n 2 ] D@⟨ϵ, δ ⟩,
                     ((McL∞
                          1
                             [1, n 1 ] D@⟨ϵ, δ ⟩, McL∞   2
                                                            [1, n 2 ] D@⟨ϵ, δ ⟩, D@∞) ⊸∗ τ )@∞,
                     τ @∞
                    ) ⊸∗ τ
           sample : (N[m 2 ]@⟨0, 0⟩,
                     McL∞ [m 1 , n 1 ] D@⟨2m 2ϵ1 /m 1 , m 2δ 1 /m 1 ⟩, McL∞ [m 1 , n 2 ] D@⟨2m 2ϵ2 /m 1 , m 2δ 2 /m 1 ⟩,
                     ((McL∞ [m 2 , n 1 ] D@⟨ϵ1 , δ 1 ⟩, McL∞ [m 2 , n 2 ] D@⟨ϵ2 , δ 2 ⟩) ⊸∗ τ )@∞
                    ) ⊸∗ τ                                                                                    Γ ⊢e :τ
      MGauss
      Γ1 ⊢ e 1 : R+ [Ûr ]      Γ2 ⊢ e 2 : R+ [ϵ]       Γ3 ⊢ e 3 : R+ [δ ]         Γ4 + ⌉⌊Γ5⌋⌈r{x
                                                                                              Û                     c
                                                                                                 , ...,x } ⊢ e 4 : ML2 [m, n] R
                                                                                               1       n

           ⌉Γ1 + Γ2 + Γ3 ⌈0,0 + ⌉Γ4 ⌈∞ + ⌉Γ5 ⌈ϵ,δ ⊢ mgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : MU
                                                                                                         L∞ [m, n] R
  Exponential
  Γ1 ⊢ e 1 : R+ [Ûr ]       Γ2 ⊢ e 2 : R+ [ϵ]       Γ3 ⊢ e 3 : Mcℓ [1, m](τ )        Γ4 + ⌉⌊Γ5⌋⌈r{x
                                                                                                 Û
                                                                                                    , ...,x } ⊎ {x :∞ τ } ⊢ e 4 : R
                                                                                                   1       n

            ⌉Γ1 + Γ2 ⌈0,0 + ⌉Γ3 + Γ4 ⌈∞ + ⌉Γ5 ⌈ϵ,0 ⊢ exponential[e 1 , e 2 ] <x 1 , ..., x n > e 3 {x ⇒ e 4 } : τ

                                                   Fig. 6. Matrix Typing Rules


than 1:
                                                                xi
                                                                           if   ∥x i ∥c > 1
                                                           
                                           clipc x i ≜         ∥x i ∥c
                                                            xi             if   ∥x i ∥c ≤ 1
The clipping process is encoded in Duet as clip (Figure 6), which introduces a new bound on the c
norm of its output.

4.3   Vector-Valued Privacy Mechanisms
Both the Laplace and Gaussian mechanisms are capable of operating directly over vectors; the
Laplace mechanism adds noise calibrated to the L1 sensitivity of the vector, while the Gaussian
mechanism uses its L2 sensitivity. With the addition of matrices to Duet, we can introduce typing
rules for these vector-valued mechanisms, using single-row matrices to represent vectors. We
present the typing rule for MGauss in Figure 6; the rule for MLaplace is similar. We also introduce
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
22                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
a typing rule for the exponential mechanism, which picks one element out of an input vector based
on a sensitive scoring function (Figure 6, rule Exponential).

5     CASE STUDIES
In this section, we demonstrate the use of Duet to express and verify a number of different algo-
rithms for differentially private machine learning. Our case studies fall into three broad categories:
differentially private optimization algorithms (i.e. training algorithms), useful additions or modifi-
cations to those algorithms, and algorithms for data preprocessing or easing deployment. Our case
studies are summarized in the following table.
       Technique                                 Ref.       §     Privacy Concept
       Optimization Algorithms
       Noisy Gradient Descent                    [14, 50]   5.1   Composition
       Gradient Descent w/ Output Perturbation   [54]       5.2   Parallel Composition (sensitivity)
       Noisy Frank-Wolfe                         [51]       5.3   Exponential mechanism
       Variations on Gradient Descent
       Minibatching                              [14]       5.4   Amplification by subsampling
       Parallel-composition minibatching         —          5.5   Parallel composition
       Gradient clipping                         [3]        5.6   Sensitivity bounds
       Preprocessing & Deployment
       Hyperparameter tuning                     [18]       A.1   Exponential mechanism
       Adaptive clipping                         —          5.7   Sparse Vector Technique
       Z-Score normalization                     [2]        A.2   Composition
       Combining All of the Above                           5.8   Composition
   There are four basic approaches to differentially private convex optimization: input perturba-
tion [17], objective perturbation [17], gradient perturbation [14, 50], and output perturbation [17, 54].
Of these, the latter three are known to provide competitive accuracy, and the latter two (gradient
perturbation and output perturbation) are the most widely used; our first two case studies verify
these two techniques. Our third case study verifies the noisy Frank-Wolfe algorithm [51], a variant
of gradient perturbation especially suited to high-dimensional datasets.
   Our next three case studies demonstrate the use of Duet to verify commonly-used variations on
the above algorithms, including various kinds of minibatching and a gradient clipping approach
used in deep learning.
   Finally, we explore techniques for preprocessing input datasets so that the preconditions of the
above algorithms are satisfied. Appropriate preprocessing is a vital step in practical deployments,
both for providing privacy and ensuring accuracy of the final model, but practical preprocessing
techniques have not received much attention in prior work. Due to space constraints, two of these
case studies (hyperparameter tuning and Z-score normalization) appear in the extended version of
this paper.
   In Section 5.8, we discuss the use of Duet to combine all of these components—many of which
leverage different variants of differential privacy—to build a complete machine learning system.
Duet provides direct support for embedding one privacy variant in a program written using a
different variant, and automatically converts the embedded variant to match the surrounding
program. This ability is vital for designing practical systems, since recent variants provide tight
composition, but some useful algorithms are only defined for pure-ϵ or (ϵ, δ )-differential privacy.

5.1    Noisy Gradient Descent
We begin with a fully-worked version of the differentially-private gradient descent algorithm from
Section 3.2. This algorithm was first proposed by Song et al. [50] and later refined by Bassily et
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      23
al. [14]. Gradient descent is a simple but effective training algorithm in machine learning, and has
been applied in a wide range of contexts, from simple linear models to deep neural networks.
   The program below implements noisy gradient descent in Duet (without minibatching, though
we will extend it with minibatching in Section 5.4). It performs k iterations of gradient descent,
starting from an initial guess θ 0 consisting of all zeros. At each iteration, the algorithm computes a
noisy gradient using noisy-grad, scales the gradient by the learning rate η, and subtracts the result
from the current model θ to arrive at the updated model.
      noisy-grad(θ, X , y, ϵ, δ ) ≜                         zeros(n) ≜ mcreateL∞ 1 n (sλ i j ⇒ 0.0)
        let s = R[1.0]/real (rows X ) in                    noisy-gradient-descent(X , y, k, η, ϵ, δ ) ≜
        let z = zeros (cols X ) in
                                                              let X 1 = box (mclipL2 X ) in
        let дs = mmap-row (sλ X i yi ⇒
                                                              let θ 0 = zeros (cols X 1 ) in
                     L∇LRL2 [θ ; X i , yi ]) X y in           loop[δ ′ ] k on θ 0 <X 1 , y> {t, θ ⇒
        let д = fld-row (sλ x 1 x 2 ⇒ x 1 + x 2 ) z дs in
                                                                   дp ← noisy-grad θ (unbox X 1 ) y ϵ δ ;
        let дs = map (sλ x ⇒ s · x) д in
                                                                   return θ − η · дp }
        mgauss[s, ϵ, δ ] <X , y> {дs }
   To ensure differential privacy, this definition uses gradient perturbation—adding noise directly to
the gradient in each iteration. The mgauss construct is used in the definition of noisy-grad to add
thepright amount of noise. Under (ϵ, δ )-differential privacy, Duet derives a total privacy cost of
(2ϵ 2k log(1/δ ′), kδ + δ ′)-differential privacy for this implementation, which matches the total
cost manually proven by Bassily et al. [14]. Duet can also derive a total cost for other privacy
variants: the same program satisfies kρ-zCDP, or (α, kϵ)-RDP.


5.2     Gradient Descent with Output Perturbation
An alternative to gradient perturbation is output
                                                          gd-output-perturbation(xs, ys, k, η, ϵ, δ ) ≜
perturbation—adding noise to the final trained              let m 0 = zeros (cols X ) in
model, rather than during the training process.             let c = box (mclipL2 xs) in
Wu et al. [54] present a competitive algorithm              let s = real k/real b in
based on this idea, which works by bounding the             mgauss[s, ϵ, δ ] <xs, ys> {
total sensitivity (rather than privacy) of the iter-          loop k on m 0 { a, θ ⇒
ative gradient descent process. Their algorithm                  mfold-row b, θ, unbox c, ys { θ, xb, yb ⇒
leverages parallel composition for sensitivity: it                 let д = ∇LR  L2 [θ ; xb, yb] in
divides the dataset into small chunks called mini-                   θ  −  η · д }}}
batches, and each iteration of the algorithm processes one minibatch. A single pass over all mini-
batches (and thus, the whole dataset) is often called an epoch. If the dataset has size m and each
minibatch is of size b, then each epoch comprises m/b iterations of the training algorithm. This
approach to minibatching is often used (without privacy) in deep learning. The sensitivity of a
complete epoch in this technique is just 1/b.
   We encode parallel composition for sensitivity in Duet using the mfold-row function, defined
in Section 4, whose type matches that of foldl for lists in the Fuzz type system [44]. mfold-row
considers each row to be a “minibatch” of size 1, but is easily extended to consider multiple rows at
a time (as in our encoding below). Duet derives a sensitivity bound of k/b for the training process,
and a total privacy cost of (ϵ, δ )-differential privacy, matching the manual analysis of Wu et al. [54].


5.3     Noisy Frank-Wolfe
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
24                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
We next consider a variation on gradient per-
                                                         frank-wolfe X y k ϵ δ ≜
turbation called the private Frank-Wolfe al-                 let X 1 = clip-matrixL∞ X in
gorithm [51]. This algorithm has dimension-                  let d = cols X in
independent utility, making it useful for high-              let θ 0 = zeros d in
dimensional datasets. In each iteration, the                 let idxs = mcreateL∞ [1,2·d]{i,j ⇒
algorithm takes a step of fixed size in a single                             ⟨j mod d,sign(j − d)⟩} in
dimension, using the exponential mechanism                   ZCDP [δ ] { loop k on θ 0 {t, θ ⇒
to choose the best direction based on the gradi-                let µ = 1.0/((real t) + 2.0) in
ent. The sensitivity of each update is therefore                let д = L∇LR   L∞ [θ ; X 1 , y] in
dependent on the L ∞ norm of each sample,                       ⟨i, s⟩  ←   EPS   DP {
                                                                                          1
rather than the L 2 norm.                                           exponential[      rows X 1 , ϵ] idxs {⟨i, s⟩ ⇒
   Our implementation uses the exponential                             s · д#[0, i]} ;}
                                                                let дp = (zeros d)#[0, i 7→ s · 100] in
mechanism to select the direction in which the
                                                                return ((1.0 − µ) · θ ) + (µ · дp ) } }
gradient has its maximum value, then updates
θ in only the selected dimension. To get the right sensitivity, we compute the gradient with L∇LR                  L∞ ,
which requires an L∞ norm bound on its input and ensures bounded L∞ sensitivity.
   We mix several variants of differential privacy in this implementation. Each use of the exponential
mechanism provides ϵ-differential privacy; each iteration of the loop satisfies 12 ϵ 2 -zCDP, and
                                          q
the whole algorithm satisfies ( 12 ϵ 2 + 2 12 ϵ 2 log(1/δ ), δ )-differential privacy. The use of zCDP for
composition is an improvement over the manual analysis of Talwar et al. [51], which used advanced
composition.

5.4   Minibatching
An alternative form of minibatching to
the one discussed in Section 5.2 is to ran- minibatch-gradient-descent X y k b η ϵ δ ≜
domly sample a subset of of the data in           let X 1 = clip-matrix X in
                                                  loop [δ ] k on zeros (cols X 1 ) <X 1 , y> {t, θ ⇒
each iteration. Bassily et al. [14] present
                                                    sample b on X 1 , y {X 1′ , y ′ ⇒
an algorithm for differentially private
                                                      дp ← noisy-grad θ X 1′ y ′ ϵ δ ; return θ − η · дp }}
stochastic gradient descent based on this
idea: their approach samples a single random example from the training to compute the gradient in
each iteration, and leverages the idea of privacy amplification to improve privacy cost. The privacy
amplification lemma states that if mechanism M(D) provides (ϵ, δ )-differential privacy for the
datset D of size n, then running M on uniformly random γn entries of D (for γ ≤ 1) provides
(2γϵ, γ δ )-differential privacy [14, 52] (this bound is loose, but used here for readability).
   We encode the privacy amplification lemma in Duet using the sample construct defined in
Section 4. Similar privacy amplification lemmas exist for RDP [52] and tCDP [15]. Privacy amplifi-
cation is not possible under zCDP. We can use sampling with privacy amplification to implement
minibatching SGD in Duet.
   Under p (ϵ, δ )-differential privacy with privacy amplification, Duet derives a total privacy cost of
(4(b/m)ϵ 2k log(1/δ ′), (b/m)kδ + δ ′)-differential privacy for this algorithm, which is equivalent
to the manual proof of Bassily et al. [14].

5.5   Parallel-Composition Minibatching
As a final form of minibatching, we consider extending the parallel composition approach used by
Wu et al. [54] for sensitivity to parallel composition of privacy mechanisms for minibatching in the
gradient perturbation approach from Section 5.1. Since the minibatches are disjoint in this approach,
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      25
we can leverage the parallel composition property for privacy mechanisms (McSherry [37], Theo-
rem 4; Dwork & Lei [23], Corollary 20), which states that running an (ϵ, δ )-differentially private
mechanism k times on k disjoint subsets of a database yields (ϵ, δ )-differential privacy (in contrast
to sequential composition, which yields (kϵ, kδ )-differential privacy). The intuition matches that
of the sensitivity case: the targeted individual falls into just one subset, and computations on the
other subsets do not affect privacy.
   We encode this concept in Duet using the pfld-rows construct defined in Section 4. The
arguments to pfld-rows include the dataset and a function representing an (ϵ, δ )-differentially
private mechanism, and pfld-rows ensures (ϵ, δ )-differential privacy for the dataset. This version
considers minibatches of size 1, and is easily extended to consider other sizes. We can use pfld-rows
to implement epoch-based minibatching with gradient perturbation, even for privacy variants like
zCDP which do not admit sampling:
      epoch b ρ η ≜                                        epoch-minibatch-GD X y ρ η k b ≜
       pλ xs ys θ ⇒                                         let m 0 = zeros (cols xs) in
         let s = R+ [1.0]/real b in                         loop k on m 0 <X , y> {a, θ ⇒
         д ← mgauss[s, ρ] <xs, ys> {∇LR [θ ; xs, ys] } ;      pfld-rows(b, θ, mclipL2 X , y, epoch b ρ η)
         return θ − η · д                                   }
   This algorithm is similar in concept to the output perturbation approach of Wu et al. [54], but
leverages parallel composition of privacy mechanisms for gradient perturbation instead, and has
not been previously published. The algorithm runs k epochs with a batch size of b, for a total of kb
iterations. Duet derives a privacy cost of kρ-zCDP for the algorithm.



5.6     Gradient Clipping
The gradient functions we have used so far have bounded sensitivity (i.e. they are 1-Lipschitz).
Many gradient functions used in practical machine learning (e.g. gradients of deep neural networks)
have unbounded sensitivity.
   A common approach for achieving differential privacy in this setting is to clip the output of
the “black-box” gradient function (called U ∇), instead of clipping the input samples [3, 48]. This
requires computing the gradient for each sample individually, clipping each gradient (using clip),
then calling conv to transform the resulting matrix of D elements to a matrix of R elements and
taking its average. The conv construct is typed by the Convert rule, which encodes the fact that
a D matrix with bounded norm can be converted to a R matrix with bounded sensitivity. This
results in a sensitivity of n1 for the averaged clipped gradient, even though the sensitivity of U ∇ is
unbounded.
        noisy-clipped-grad θ X y ϵ δ ≜                     noisy-clipping-GD X y k b η ϵ δ ≜
          let s = R[1.0]/real (rows X ) in                   let θ 0 = zeros (cols X ) in
          let z = zeros (cols X ) in                         loop [δ ] k on θ 0 <X , y> {t, θ ⇒
          let д = conv (clipL2 (U ∇[θ ; x i , yi ])) in         sample b on X , y {X ′, y ′ ⇒
          mgaussL2 [s, ϵ, δ ] <X , y> {s · д}                     дp ← noisy-clipped-grad θ X ′ y ′ ϵ δ ;
                                                                  return θ − η · дp } }

   Under (ϵ, δ )-differential privacy, Duet derives a privacy cost of (2ϵ 2k log(1/δ ′), kδ + δ ′)-
                                                                            p

differential privacy for this algorithm. Using zero-concentrated differential privacy or Rényi differ-
ential privacy, Duet matches the manually-derived privacy cost proven by Talwar et al. [3]. This
approach can be combined with the previously-discussed solutions for minibatching to produce
practical training algorithms for deep learning.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
26                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
5.7    Adaptive Clipping
Our mclip[L2] construct clips samples to have an L2 norm of 1. However, the best clipping
parameter for a dataset depends on the data, and data-independent clipping can eliminate useful
information and reduce accuracy. An ideal solution would determine the scale of the given dataset
first, and then re-scale the data before clipping so that the clipping process does not eliminate too
much information from the data.
   We can achieve this goal by considering several possible ways to scale the dataset and testing
how many samples are modified during clipping for each possibility. We would like to ensure
that only outliers (say, 10% of the samples) are modified during clipping. We encode this test in a
1-sensitive Duet function called testScaleParam.
   We would like to find a value for b (the scaling parameter) for which testScaleParam returns
at least 0.9 · real (rows xs) (i.e. at least 90% of the samples remain un-clipped). Since we can define
such a numeric threshold as our goal, and testScaleParam has sensitivity 1, we can apply the
Sparse Vector Technique in the form of the AboveThreshold function (Dwork & Roth [25], Algorithm
1). AboveThreshold runs an arbitrary stream of 1-sensitive queries under a fixed privacy budget,
returning the index of the first query whose (noisy) result is greater than a given threshold. This is
perfect for our setting: it allows testing many values for b (hundreds or thousands, potentially),
in increasing order, to find the smallest one which does not cause a large loss of information.
We encode this concept in Duet as above-threshold, defined in Section 4, and we can use it to
adaptively pick a scaling parameter which meets the criteria listed above.
      testScaleParam b xs ≜                                   selectClippingParam xs ϵ bs ≜
         let clipped = mclipL2 (b · xs) in                      let tarдet = 0.9 · real (rows xs) in
         let f iltered = mfilter zip[clipped, xs] {sλ row ⇒     let f s = mmap testScaleParam bs in
              let ⟨clipped, oriд⟩ = row#[N[0], N[0]] in         above-threshold(ϵ, f s, tarдet, xs)
                 clipped ≡ oriд } in
         R+ [0.5] · real (rows f iltered)
  This function builds the necessary stream of 1-sensitive queries using testScaleParam for
each of the possible values of b, then finds the first one which leaves at least 90% of the samples
untouched under clipping. For this program, Duet derives a total privacy cost of ϵ-differential
privacy, no matter how many elements bs contains.

5.8    Composing Privacy Variants to Build Complete Learning Systems
Putting together the pieces we have described to build real machine learning systems that preserve
differential privacy often requires mixing privacy variants in order to obtain optimal results. We
can use Duet’s ability to mix variants of differential privacy to combine components in a way that
optimizes the use of the privacy budget. We demonstrate this ability with an example that performs
several data-dependent analyses as pre-processing steps before training a model. Our example
uses Duet’s ability to mix variants to compose z-score normalization (using both pure ϵ and
(ϵ, δ )-differential privacy), hyperparameter tuning (with (ϵ, δ )-differential privacy), and gradient
descent (with zCDP), returning a total (ϵ, δ ) privacy cost.
   As this example demonstrates,
the ability to combine variants is adaptiveClippingGradientDescent xs ys k ϵ δ ηs bs ≜
important for building systems          means ← colMeans(xs, ϵ, δ, bs);
                                        scales ← EPS_DP { colScaleParams(xs, ϵ, bs, means) };
composed of many different algo-
                                        let xsn = box (normalize xs means scales) in
rithms. In Section 6, we leverage
                                        η ← pick_η(unbox xsn , ys, k, ϵ, δ, ηs);
this facility of Duet to evaluate       ZCDP [δ ] { noisyGradientDescentZCDP(b · (unbox xsn ), ys, k, η, ϵ, δ ) }
the accuracy of gradient descent
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      27
and Frank-Wolfe under different privacy variants, by converting the total privacy cost of each to
(ϵ, δ ) before comparing them.

6     IMPLEMENTATION & EVALUATION
This section describes our implementation of Duet, and our empirical evaluation of Duet’s ability
to produce accurate differentially private models. Our results demonstrate that the state-of-the-art
privacy bounds derivable by Duet can result in huge gains in accuracy for a given level of privacy.

6.1    Implementation & Typechecking Performance
We have implemented a prototype of Duet in              Technique              LOC Time (ms)
Haskell that includes type inference of privacy         Noisy G.D.               23      0.51ms
bounds, and an interpreter that runs on all             G.D. + Output Pert.      25      0.39ms
examples described in this paper. We do not             Noisy Frank-Wolfe        31      0.59ms
implement Hindley-Milner-style constraint-              Minibatching             26      0.51ms
based type inference of quantified types; our           Parallel minibatching    42      0.65ms
type inference is syntax-directed and limited           Gradient clipping        21      0.40ms
to construction of privacy bounds as symbolic           Hyperparameter tuning 125        3.87ms
formulas over input variables. Our implemen-            Adaptive  clipping       68      1.01ms
                                                        Z-Score normalization   104      1.51ms
tation of type inference roughly follows the
bottom-up approach of DFuzz’s implementa-
                                                  Fig. 7. Summary of Typechecking Performance on Case
tion [20]. Type checking requires solving con-
                                                  Study Programs
straints over symbolic expressions containing
log and square root operations. Prior work (DFuzz and HOARe2 ) uses an SMT solver during type-
checking to check validity of these constraints, but SMT solvers typically do not support operators
like log and square root, and struggle in the presence of non-linear formulas. Because of these
limitations, we implement a custom solver for inequalities over symbolic real expressions instead
of relying on support from off-the-shelf solvers. Our custom solver is based on a simple decidable
(but incomplete) theory which supports log and square root operations, and a more general subset
of non-linear (polynomial) formulas than typical SMT theories.
   The Duet typechecker demonstrates very practical performance. Figure 7 summarizes the
number of lines of code and typechecking time for each of our case study programs; even medium-
size programs with many functions typecheck in just a few milliseconds. Our implementation is
open source and freely available on GitHub at: https://github.com/uvm-plaid/duet.

6.2    Evaluation of Private Gradient Descent and Private Frank-Wolfe
We also study the accuracy of the models produced by the Duet implementations of private gradient
descent and private Frank-Wolfe in Section 5. We evaluate both algorithms on 4 datasets. Details
about the datasets can be found in Figure 8.
   We ran both algorithms on each dataset with per-iteration ϵi ∈ {0.0001, 0.001, 0.01, 0.1} and
then used Duet to derive the corresponding total privacy cost. We fixed δ = n12 , where n is the size
of the dataset. For private gradient descent, we set η = 1.0, and for private Frank-Wolfe we set the
size of each corner c = 100.
   We randomly shuffled each dataset, then chose 80% of the dataset as training data and reserved
20% for testing. We ran each training algorithm 5 times on the training data, and take the average
testing error over all 5, to account for the randomness in the training process.
   We present the results in Figure 9. Both algorithms are             Dataset Samples Dim.
capable of generating accurate models at reasonable values            Synthetic    10,000     20
of ϵ. Note that all three models in the results provide exactly           Adult    45,220    104
                                                                   KDDCup99        70,000     114
                                                                    Facebook       40,949      54

                                                                Fig. 8. Dataset Used in Accuracy Evalu-
                                                                ation
    Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
    28                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
                                                                   Noisy Gradient Descent
                        Synthetic                                  Adult             KDDCup99                                                  Facebook
                                                                                                                                     0.75
           0.9                                                                                0.96
                                                     0.75                                                                             0.7
Accuracy




                                          Accuracy




                                                                                   Accuracy




                                                                                                                          Accuracy
                                                                                              0.94
           0.8                                        0.7                                     0.92                                   0.65
           0.7                                       0.65                                      0.9                                    0.6

                                                      0.6                                     0.88                                   0.55
           0.6
                 0.01          1    100                     0.01        1   100                      0.01       1    100                    0.01       1   100
                           ϵ                                        ϵ                                       ϵ                                      ϵ
                                                                     Noisy Frank-Wolfe
                        Synthetic                                  Adult            KDDCup99                                                   Facebook
                                                                                                1                                     0.8
                                                      0.8
                                                                                                                                      0.7
Accuracy




                                          Accuracy




                                                                                  Accuracy




                                                                                                                          Accuracy
           0.8                                                                                0.9
                                                      0.7
                                                                                                                                      0.6
           0.6                                        0.6                                     0.8                                     0.5
                 0.01          1    100                     0.01        1   100                      0.01       1   100                     0.01       1   100
                           ϵ                                        ϵ                                       ϵ                                      ϵ

                                                        Adv. Comp.                           Rényi DP               zCDP
                 Fig. 9. Accuracy Results for Noisy Gradient Descent (Top) and Noisy Frank-Wolfe (Bottom).



    the same privacy guarantee for a given value of ϵ, yet their
    accuracies vary significantly. The results demonstrate the
    huge advantages afforded by recently developed variants of
    differential privacy—recent variants with tighter composi-
    tion bounds yield significantly better accuracy for a given
    level of privacy.

    7        CONCLUSION
    We have presented Duet, a language and type system for expressing and statically verifying
    privacy-preserving programs. Unlike previous work, Duet is agnostic to the underlying privacy
    definition, and requires only that it support sequential composition and post-processing. We have
    extended Duet to support several recent variants of differential privacy, and our case studies
    demonstrate that Duet derives state-of-the-art privacy bounds for a number of useful machine
    learning algorithms. We have implemented a prototype of Duet, and our experimental results
    demonstrate the benefits of flexibility in privacy definition.

    ACKNOWLEDGMENTS
    The authors would like to thank Arthur Azevedo de Amorim, Justin Hsu, and Om Thakkar for
    their helpful comments. This work was supported by the Center for Long-Term Cybersecurity,
    Alibaba AIR, DARPA & SPAWAR via N66001-15-C-4066, IARPA via 2019-1902070008, and NSF award
    1901278. The U.S. Government is authorized to reproduce and distribute reprints for Governmental
    purposes not withstanding any copyright annotation therein. The views, opinions, and/or findings
    expressed are those of the authors and should not be interpreted as representing the official views
    or policies of any US Government agency.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      29
REFERENCES
 [1] [n. d.]. Apple previews iOS 10, the biggest iOS release ever. http://www.apple.com/newsroom/2016/06/
     apple-previews-ios-10-biggest-ios-release-ever.html.
 [2] 2019. scikit-learn: Standardization, or mean removal and variance scaling. https://scikit-learn.org/stable/modules/
     preprocessing.html#preprocessing-scaler
 [3] Martin Abadi, Andy Chu, Ian Goodfellow, H Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep
     learning with differential privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications
     Security. ACM, 308–318.
 [4] Arthur Azevedo de Amorim, Marco Gaboardi, Justin Hsu, Shin-ya Katsumata, and Ikram Cherigui. 2017. A semantic
     account of metric preservation. In POPL, Vol. 52. ACM, 545–556.
 [5] Andrew Barber. 1996. Dual Intuitionistic Linear Logic. Technical Report ECS-LFCS-96-347. University of Edinburgh.
 [6] Gilles Barthe, Gian Pietro Farina, Marco Gaboardi, Emilio Jesus Gallego Arias, Andy Gordon, Justin Hsu, and Pierre-Yves
     Strub. 2016. Differentially Private Bayesian Programming. In Proceedings of the 2016 ACM SIGSAC Conference on
     Computer and Communications Security (CCS ’16). ACM, New York, NY, USA, 68–79. https://doi.org/10.1145/2976749.
     2978371
 [7] Gilles Barthe, Noémie Fong, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016. Advanced
     probabilistic couplings for differential privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and
     Communications Security. ACM, 55–67.
 [8] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu, Aaron Roth, and Pierre-Yves Strub. 2015.
     Higher-Order Approximate Relational Refinement Types for Mechanism Design and Differential Privacy. In POPL.
     ACM, 55–68.
 [9] Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016. Proving differential privacy
     via probabilistic couplings. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science. ACM,
     749–758.
[10] Gilles Barthe, Marco Gaboardi, Justin Hsu, and Benjamin Pierce. 2016. Programming language techniques for differential
     privacy. ACM SIGLOG News 3, 1 (2016), 34–53.
[11] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella-Béguelin. 2013. Probabilistic relational reasoning for
     differential privacy. ACM Transactions on Programming Languages and Systems (TOPLAS) 35, 3 (2013), 9.
[12] Gilles Barthe and Federico Olmedo. 2013. Beyond differential privacy: Composition theorems and relational logic for
     f-divergences between probabilistic programs. In International Colloquium on Automata, Languages, and Programming.
     Springer, 49–60.
[13] Raef Bassily, Adam Smith, and Abhradeep Thakurta. 2014. Private empirical risk minimization: Efficient algorithms and
     tight error bounds. In Foundations of Computer Science (FOCS), 2014 IEEE 55th Annual Symposium on. IEEE, 464–473.
[14] Raef Bassily, Adam Smith, and Abhradeep Thakurta. 2014. Private empirical risk minimization: Efficient algorithms and
     tight error bounds. In Foundations of Computer Science (FOCS), 2014 IEEE 55th Annual Symposium on. IEEE, 464–473.
[15] Mark Bun, Cynthia Dwork, Guy N Rothblum, and Thomas Steinke. 2018. Composable and versatile privacy via
     truncated CDP. In Proceedings of the 50th Annual ACM SIGACT Symposium on Theory of Computing. ACM, 74–86.
[16] Mark Bun and Thomas Steinke. 2016. Concentrated differential privacy: Simplifications, extensions, and lower bounds.
     In Theory of Cryptography Conference. Springer, 635–658.
[17] Kamalika Chaudhuri, Claire Monteleoni, and Anand D Sarwate. 2011. Differentially private empirical risk minimization.
     Journal of Machine Learning Research 12, Mar (2011), 1069–1109.
[18] Kamalika Chaudhuri and Staal A Vinterbo. 2013. A stability-based validation procedure for differentially private
     machine learning. In Advances in Neural Information Processing Systems. 2652–2660.
[19] Ezgi Çiçek, Weihao Qu, Gilles Barthe, Marco Gaboardi, and Deepak Garg. 2018. Bidirectional Type Checking for
     Relational Properties. CoRR abs/1812.05067 (2018). arXiv:1812.05067 http://arxiv.org/abs/1812.05067
[20] Arthur Azevedo De Amorim, Marco Gaboardi, Emilio Jesús Gallego Arias, and Justin Hsu. 2014. Really Natural Linear
     Indexed Type Checking. In Proceedings of the 26nd 2014 International Symposium on Implementation and Application of
     Functional Languages. ACM, 5.
[21] Arthur Azevedo de Amorim, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. 2018. Metric Semantics for
     Probabilistic Relational Reasoning. CoRR abs/1807.05091 (2018). arXiv:1807.05091 http://arxiv.org/abs/1807.05091
[22] Cynthia Dwork. 2006. Differential Privacy. In Automata, Languages and Programming, Michele Bugliesi, Bart Preneel,
     Vladimiro Sassone, and Ingo Wegener (Eds.). Lecture Notes in Computer Science, Vol. 4052. Springer Berlin Heidelberg,
     1–12. https://doi.org/10.1007/11787006_1
[23] Cynthia Dwork and Jing Lei. 2009. Differential privacy and robust statistics. In Proceedings of the forty-first annual
     ACM symposium on Theory of computing. ACM, 371–380.
[24] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006. Calibrating noise to sensitivity in private data
     analysis. In Theory of Cryptography Conference. Springer, 265–284.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
30                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
[25] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations of differential privacy. Foundations and Trends®
     in Theoretical Computer Science 9, 3–4 (2014), 211–407.
[26] Úlfar Erlingsson, Vasyl Pihur, and Aleksandra Korolova. 2014. Rappor: Randomized aggregatable privacy-preserving
     ordinal response. In Proceedings of the 2014 ACM SIGSAC conference on computer and communications security. ACM,
     1054–1067.
[27] Matt Fredrikson, Somesh Jha, and Thomas Ristenpart. 2015. Model Inversion Attacks That Exploit Confidence
     Information and Basic Countermeasures. In Proceedings of the 22Nd ACM SIGSAC Conference on Computer and
     Communications Security (CCS ’15). ACM, New York, NY, USA, 1322–1333. https://doi.org/10.1145/2810103.2813677
[28] Arik Friedman, Shlomo Berkovsky, and Mohamed Ali Kaafar. 2016. A differential privacy framework for matrix
     factorization recommender systems. User Modeling and User-Adapted Interaction 26, 5 (2016), 425–458.
[29] Marco Gaboardi, Andreas Haeberlen, Justin Hsu, Arjun Narayan, and Benjamin C Pierce. 2013. Linear dependent
     types for differential privacy. In POPL, Vol. 48. ACM, 357–370.
[30] Jean-Yves Girard. 1987. Linear Logic. Theor. Comput. Sci. 50, 1 (Jan. 1987), 1–102. https://doi.org/10.1016/0304-3975(87)
     90045-4
[31] Samuel Haney, Ashwin Machanavajjhala, John M Abowd, Matthew Graham, Mark Kutzbach, and Lars Vilhuber. 2017.
     Utility cost of formal privacy for releasing national employer-employee statistics. In Proceedings of the 2017 ACM
     International Conference on Management of Data. ACM, 1339–1354.
[32] Noah Johnson, Joseph P Near, and Dawn Song. 2018. Towards practical differential privacy for SQL queries. Proceedings
     of the VLDB Endowment 11, 5 (2018), 526–539.
[33] Noah M. Johnson, Joseph P. Near, and Dawn Xiaodong Song. 2017. Towards Practical Differential Privacy for SQL
     Queries. CoRR abs/1706.09479 (2017). http://arxiv.org/abs/1706.09479
[34] Ashwin Machanavajjhala, Daniel Kifer, John Abowd, Johannes Gehrke, and Lars Vilhuber. 2008. Privacy: Theory
     meets practice on the map. In Proceedings of the 2008 IEEE 24th International Conference on Data Engineering. IEEE
     Computer Society, 277–286.
[35] Frank McSherry and Kunal Talwar. 2007. Mechanism design via differential privacy. In Foundations of Computer
     Science, 2007. FOCS’07. 48th Annual IEEE Symposium on. IEEE, 94–103.
[36] Frank D McSherry. 2009. Privacy integrated queries: an extensible platform for privacy-preserving data analysis. In
     Proceedings of the 2009 ACM SIGMOD International Conference on Management of data. ACM, 19–30.
[37] Frank D McSherry. 2009. Privacy integrated queries: an extensible platform for privacy-preserving data analysis. In
     Proceedings of the 2009 ACM SIGMOD International Conference on Management of data. ACM, 19–30.
[38] Ilya Mironov. 2017. Renyi differential privacy. In Computer Security Foundations Symposium (CSF), 2017 IEEE 30th.
     IEEE, 263–275.
[39] Prashanth Mohan, Abhradeep Thakurta, Elaine Shi, Dawn Song, and David Culler. 2012. GUPT: privacy preserving
     data analysis made easy. In Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data.
     ACM, 349–360.
[40] Aleksandar Nanevski, Frank Pfenning, and Brigitte Pientka. 2008. Contextual Modal Type Theory. ACM Trans. Comput.
     Logic 9, 3, Article 23 (June 2008), 49 pages. https://doi.org/10.1145/1352582.1352591
[41] Arjun Narayan and Andreas Haeberlen. 2012. DJoin: differentially private join queries over distributed databases. In
     Presented as part of the 10th USENIX Symposium on Operating Systems Design and Implementation (OSDI 12). 149–162.
[42] Nicolas Papernot, Martín Abadi, Ulfar Erlingsson, Ian Goodfellow, and Kunal Talwar. 2016. Semi-supervised knowledge
     transfer for deep learning from private training data. arXiv preprint arXiv:1610.05755 (2016).
[43] Davide Proserpio, Sharon Goldberg, and Frank McSherry. 2014. Calibrating data to sensitivity in private data analysis:
     A platform for differentially-private analysis of weighted datasets. PVLDB 7, 8 (2014), 637–648.
[44] Jason Reed and Benjamin C Pierce. 2010. Distance makes the types grow stronger: a calculus for differential privacy.
     ICFP 45, 9 (2010), 157–168.
[45] Indrajit Roy, Srinath TV Setty, Ann Kilzer, Vitaly Shmatikov, and Emmett Witchel. 2010. Airavat: Security and Privacy
     for MapReduce.. In NSDI, Vol. 10. 297–312.
[46] Tetsuya Sato. 2016. Approximate relational Hoare logic for continuous random samplings. Electronic Notes in Theoretical
     Computer Science 325 (2016), 277–298.
[47] Tetsuya Sato, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. 2019. Approximate span liftings:
     Compositional semantics for relaxations of differential privacy. In 2019 34th Annual ACM/IEEE Symposium on Logic in
     Computer Science (LICS). IEEE, 1–14.
[48] R. Shokri and V. Shmatikov. 2015. Privacy-preserving deep learning. In 2015 53rd Annual Allerton Conference on
     Communication, Control, and Computing (Allerton). 909–910. https://doi.org/10.1109/ALLERTON.2015.7447103
[49] R. Shokri, M. Stronati, C. Song, and V. Shmatikov. 2017. Membership Inference Attacks Against Machine Learning
     Models. In 2017 IEEE Symposium on Security and Privacy (SP). 3–18. https://doi.org/10.1109/SP.2017.41
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      31
[50] Shuang Song, Kamalika Chaudhuri, and Anand D Sarwate. 2013. Stochastic gradient descent with differentially private
     updates. In Global Conference on Signal and Information Processing (GlobalSIP), 2013 IEEE. IEEE, 245–248.
[51] Kunal Talwar, Abhradeep Guha Thakurta, and Li Zhang. 2015. Nearly optimal private lasso. In Advances in Neural
     Information Processing Systems. 3025–3033.
[52] Yu-Xiang Wang, Borja Balle, and Shiva Kasiviswanathan. 2018. Subsampled Rényi Differential Privacy and Analytical
     Moments Accountant. CoRR abs/1808.00087 (2018). arXiv:1808.00087 http://arxiv.org/abs/1808.00087
[53] X. Wu, M. Fredrikson, S. Jha, and J. F. Naughton. 2016. A Methodology for Formalizing Model-Inversion Attacks. In
     2016 IEEE 29th Computer Security Foundations Symposium (CSF). 355–370. https://doi.org/10.1109/CSF.2016.32
[54] Xi Wu, Fengan Li, Arun Kumar, Kamalika Chaudhuri, Somesh Jha, and Jeffrey Naughton. 2017. Bolt-on Differential
     Privacy for Scalable Stochastic Gradient Descent-based Analytics. In Proceedings of the 2017 ACM International
     Conference on Management of Data (SIGMOD ’17). ACM, New York, NY, USA, 1307–1322. https://doi.org/10.1145/
     3035918.3064047
[55] Danfeng Zhang and Daniel Kifer. 2017. LightDP: Towards automating differential privacy proofs. In POPL, Vol. 52.
     ACM, 888–901.
[56] Hengchu Zhang, Edo Roth, Andreas Haeberlen, Benjamin C. Pierce, and Aaron Roth. 2019. Fuzzi: A Three-Level Logic
     for Differential Privacy. Accepted for publication in PACMPL / ICFP 2019.


A     ADDITIONAL CASE STUDIES
A.1    Hyperparameter Tuning
Each of the gradient descent algorithms we have seen so far require a setting for the η hyperparam-
eter, and many other hyperparameters (e.g. λ for regularization) are often used in practice. When
privacy is not a concern, these hyperparameters are typically tuned by training many models on
different hyperparameter combinations and picking the model with the best accuracy on the testing
data (a grid search). However, this approach cannot satisfy differential privacy, since selecting the
best model based on the (sensitive) test data might reveal something about that data.
   To tune hyperparameters with differential privacy, we must be careful to ensure that each trained
model contributes to the overall privacy cost, and that the comparison of model accuracies is done
in a differentially private way. We can encode a simple algorithm for this purpose, originally due to
Chaudhuri and Vinterbo [18], using the exponential mechanism:




   This algorithm trains one model per value of η in the set ηs and uses the exponential mechanism
to select the value of η which maximizes the model’s accuracy. Note that each prediction is infinitely
sensitive in the sample x, but the combination of mmap-row and discf ensures the resulting matrix
of D values is 1-sensitive in xs.
   This algorithm re-trains the final model using the selected value of η so that a larger proportion
of the privacy budget can be used for this model—each model trained during hyperparameter
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
32                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
tuning only receives a budget of (ϵ/n, δ /n), where n is the number of elementspin ηs; the final model
is trained using a budget of (ϵ, δ ). Duet derives a total privacy cost of (2ϵ 2k log(n/δ ) + ϵ/n +
2ϵ 2k log(1/δ ), 2kδ + 2δ )-differential privacy.
   p


A.2   Adaptive Z-Score Normalization
The adaptive clipping described in Section 5.7 results in a global scaling parameter for all features of
the input dataset. More sophisticated preprocessing approaches—including those commonly used
in non-private machine learning [2]—modify each feature individually to ensure standardization:
zero mean, and unit variance. Standardization can be even more important in differentially-private
machine learning, since a feature with very small variance may be especially susceptible to noise
added during training.
   Standardization for each feature is often achieved by z-score normalization (in scikit-learn,
provided by preprocessing.StandardScaler): subtract the feature’s mean, and divide by its standard
deviation. We can approximate this kind of normalization under differential privacy by computing
a differentially private mean and scaling parameter for each feature individually, then normalizing
based on these. Computing differentially private means requires first adaptively picking a clipping
parameter for each column, to give bounded sensitivity for the mean itself.




   Note that pmap-col does not provide parallel composition, because examining each of n columns
individually allows examining some aspect of a single individual’s data n times. The next task is to
determine the scaling parameter for each feature. This can be accomplished using pickScaleParam
from Section 5.7, but we must first subtract the mean from each element of the column.




  Finally, we can define a normalize function which normalizes the dataset, given the mean and
scale of each column, and use this function to pre-process the data before training.




   Note that we partially apply normalize to obtain normalizeF because normalize is not 1-sensitive
in its first two arguments. Applying normalize in the argument to noisySGD would therefore not
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      33
satisfy the requirement of pλ application that all arguments be 1-sensitive. Fortunately, we are not
concerned about the privacy of the first two arguments to normalize (they are already differentially
private), so we
             p partially apply the function and return the result. Duet derivesp a total privacy cost
of (3nϵ + 2ϵ 2k log(1/δ ′), kδ + nδ + δ ′)-differential privacy for xs, and (2ϵ 2k log(1/δ ′), kδ + δ ′)-
differential privacy for ys (since the labels do not participate in normalization).


B   FULL TYPE SYSTEM AND FORMALISM
Figure 10 shows the full type system. It includes a type-level language of non-negative real-valued
symbolic expressions η, in particular including type-level variables β. Type-level variables β (ranging
over non-negative reals, not types) are quantified in privacy function types. The function and
application expression forms for privacy lambda explicitly introduce and instantiate these quantified
type-level variables—they are not inferred through unification in our implementation.
   Figure 11 shows type-level metafunctions used in the typing rules. Each of the operations are
over types, and return a triple which encodes the resulting sensitivity “cost” of the operation in the
sensitivity language. E.g., s 1 , s 2 , τ = τ1 + τ2 means that when you add an expression at type τ1 to an
expression at type τ2 , the resulting type is τ3 , the sensitivity of the left argument should be scaled
by s 1 , and the sensitivity of the second argument should be scaled by s 2 . The mod rules is special in
that the sensitivities returned are interpreted as max bounds on the arguments, not scaling factors.
The main purpose of these metafunctions are to support a form of ad-hoc polymorphism in the
type system. E.g., adding two naturals returns a natural, adding two reals returns a real, and adding
two statically known numbers returns another statically known number—known to be the sum of
the arguments.
   Rules for multiplication and mod are particularly important as a non-infinity sensitivity can be
given the left operand if the right operand is known statically. Multiplication of a non-statically
known value to the inverse of a statically known value is commonly used in our examples to scale
a result, resulting in a lower scaled sensitivity cost.
   Figure 12 shows the full language definition of sensitivity and privacy languages. From this core
language we derive helpers and typecheck all case studies mentioned in the main body of the paper.
Included in the sensitivity language are standard linear logic connectives, as described by Fuzz [44].
We also include basic language features like conditionals, and loops—both with static and non-static
loop bounds. Note that privacy lambdas include an explicit list of quantified type-level variables
β which range over non-negative real-valued expressions. conv is a conversion operation that
matrices containing data clipped to some norm ℓ to matrices of real numbers, but with sensitivity ℓ.
   Figure 13 shows arithmetic metafunctions for sensitivities and privacy annotations. Note that
privacy annotations support + but not ·. The “ceiling” operator is defined in this figure in four forms:
sensitivity-to-sensitivity, privacy-to-sensitivity, privacy-to-privacy and sensitivity-to-privacy. We
write ≈ instead of = because our implementation uses an incomplete (but well-defined) decision
procedure for deciding when two real-valued expressions are equal.
   Figure 14 shows the kinding system which establishes well-formedness of type variables, symbolic
non-negative real-valued expressions, and types. The context ∆ is used to track kinds of type-level
variables, which are either N or R+ . We implement a solver for determining when two symbolic
real expressions are equal or one is less-than-or-equal to another, and we use the type information
in the solver, in addition to merely establishing type well-formedness.
   Figure 15 shows the typing rules for the fragment of the sensitivity language that concerns
literals and operations over basic primitive types. These typing rules use type-level metafunctions
defined in Figure 11.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
34                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
   Figure 16 shows the typing rules for matrix operations, including clipping, gradients, and aggre-
gate operations like maps and folds. We include both unary and binary variants of two different
types of maps—element-wise and row-wise.
   Figure 17 shows the typing rules for control flow—e.g., loops and ifs—and compound types in
the sensitivity language. Compound types include sums, multiplicative products, additive products,
sensitivity functions and privacy functions.
   Figure 18 shows the typing rules for the entire privacy language. The running theme in each of
these rules is to clip contexts up to infinity in the conclusion of rules where no privacy guarantee
can be made, and to assume a clipped context up to some fixed value in the assumption of rules
where the privacy guarantee requires a bound on sensitivity or privacy on an argument, written
in curly brackets. Note that many rules take an explicit list of variables to be considered for the
purpose of the assumed bound, written in ascii angle brackets.
   Figures 19 and 20 define the metric spaces used to interpret types. We call the model for types a
“domain”, because we extend the usual notion of metric space with an additional operation which
captures how to interpret the norm of values in the underlying set. The distance metric and the
norm metric may not be related, and their interpretations do not inter-depend on each other in the
semantics.
   Figure 21 shows the semantics of types and typing judgments in terms of domains, metrics and
norms defined in Figures 19 and 20. Our soundness result is that for well-typed terms there exists
an interpretation for terms which inhabits the interpretation of a typing context.
   Each of the figures mentioned above is displayed next. After these figures, we present key
theorems from the literature which are used in our proof of type soundness, after which we present
key cases of the proof. After presenting key proof cases, we re-presented rules which change when
adapting the type system to Rényi differential privacy, zero-concentrated differential privacy, and
truncated-concentrated differential privacy.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      35
      n∈N                                                             natural numbers
      r ∈R                                                            real numbers
    r + ∈ R+                                                          non-negative real numbers
      β ∈ rvar                                                        real-expression variable
      x ∈ var                                                         variables
      κ ∈ kind F N | R+                                               real-expression kinds
     ∆ ∈ kcxt ≜ rvar ⇀ kind                                           kind context
               F {β:κ, ..., β:κ}
      η ∈ rexp F β | n | r +                                          var, nat and real
               | η ⊔η | η ⊓η                                          max and min
               | η +η | η · η                                         plus and times
                        √
               | 1/η | η | ln η                                       inverse, root and log
      s ∈ sens F η | ∞                                                sensitivity
      p ∈ priv F ηϵ , ηδ | ∞                                          privacy cost
      ℓ ∈ norm F L1 | L2 | L∞                                         norms
      c ∈ clip F ℓ | U                                                clipping
      τ ∈ type F N[η] | R+ [η] | N | R | data                         numeric types
               | idx[η] | matrixcℓ [η, η] τ                           matrix types
               | τ ⊎τ | τ ×τ | τ & τ                                  compound types
               | τ ⊸s τ | ∀ [β:κ, ..., β:κ] (τ @p, ..., τ @p) ⊸∗ τ    function types

                                  Fig. 10. Types and Kinds (shared)
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
36                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

            ⊔           ∈ τ × τ ⇀ sens × sens × τ                      ⊓            ∈ τ × τ ⇀ sens × sens × τ
   N[η 1 ] ⊔ N[η 2 ] ≜ ⟨0, 0, N[η 1 ⊔ η 2 ]⟩                  N[η 1 ] ⊓ N[η 2 ] ≜ ⟨0, 0, N[η 1 ⊓ η 2 ]⟩
  R+ [η 1 ] ⊔ R+ [η 2 ] ≜ ⟨0, 0, R+ [η 1 ⊔ η 2 ]⟩            R+ [η 1 ] ⊓ R+ [η 2 ] ≜ ⟨0, 0, R+ [η 1 ⊓ η 2 ]⟩
        N⊔N             ≜ ⟨1, 1, N⟩                                N⊓N              ≜ ⟨1, 1, N⟩
        R⊔R             ≜ ⟨1, 1, R⟩                                R⊓R              ≜ ⟨1, 1, R⟩
                                                                       ·            ∈ τ × τ ⇀ sens × sens × τ
                                                              N[η 1 ] · N[η 2 ] ≜ ⟨0 , 0 , N[η 1 · η 2 ]⟩
            +           ∈ τ × τ ⇀ sens × sens × τ            R+ [η 1 ] · R+ [η 2 ] ≜ ⟨0 , 0 , R+ [η 1 · η 2 ]⟩
   N[η 1 ] + N[η 2 ] ≜ ⟨0, 0, N[η 1 + η 2 ]⟩                  N[η 1 ] · N          ≜ ⟨0 , η 1 , N⟩
  R+ [η 1 ] + R+ [η 2 ] ≜ ⟨0, 0, R+ [η 1 + η 2 ]⟩            R+ [η 1 ] · R         ≜ ⟨0 , η 1 , R⟩
        N+N             ≜ ⟨1, 1, N⟩                                N · N[η 2 ] ≜ ⟨η 2 , 0 , N⟩
        R+R             ≜ ⟨1, 1, R⟩                                 R · R+ [η 2 ] ≜ ⟨η 2 , 0 , R⟩
                                                                   N·N             ≜ ⟨∞, ∞, N⟩
                                                                    R·R            ≜ ⟨∞, ∞, R⟩
                                                  √ ∈ τ ⇀ sens × τ
           1/ ∈ τ ⇀ sens × τ                                                            ln ∈ τ ⇀ sens × τ
                                                                 √
    1/R+ [η] ≜ ⟨0 , R+ [1/η]⟩                                                          + [η] ≜ ⟨0 , R+ [ln η]⟩
                                            p +               +
                                                R [η] ≜ ⟨0 , R [ η]⟩               ln R
                                                  √
           1/R ≜ ⟨∞, R⟩                             R ≜ ⟨∞, R⟩                          ln R ≜ ⟨∞, R⟩
              mod              ∈ τ × τ ⇀ sens × sens × τ
                                                                          − ∈ τ × τ ⇀ sens × sens × τ
            N mod N[η 2 ] ≜ ⟨η 2 , 0 , N⟩
                                                                       N − N ≜ ⟨1, 1, N⟩
   idx[η 1 ] mod idx[η 2 ] ≜ ⟨η 2 , η 1 , idx[η 1 ⊓ η 2 ]⟩
                                                                       R − R ≜ ⟨1, 1, R⟩
            N mod N            ≜ ⟨∞, ∞, N⟩
                                         =?      ∈ τ × τ ⇀ sens × sens × τ
                                      N =? N ≜ ⟨1, 1, N⟩
                                      R =? R ≜ ⟨1, 1, N⟩

                                        Fig. 11. Type Metafunctions
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      37
      д ∈ grad F LS | LR | GR | HSV M                                  gradients2
      e ∈ exp F N[n] | N[r + ] | dyn e | n | r | real e                naturals and reals
                | e ⊔ e | e ⊓ e | e + e | e · e | 1/e                  arithmetic
                  √
                | e | ln e | e mod e | e − e | e =? e                  arithmetic
                | mcreateℓ [e, e]{x, x ⇒ e} | e#e                      matrix creation and index
                | rows e | cols e                                      matrix transpose and lengths
                           ℓ
                | clip e | conv e                                      clipping and conversion
                       д
                | L∇ℓ [e; e, e] | U ∇[e; e, e]                         gradient
                | mmap e {x ⇒ e}                                       matrix map
                | mmap e, e {x, x ⇒ e}                                 matrix binary map
                | mmap-row e {x ⇒ e}                                   matrix map rows
                | mmap-row e, e {x, x ⇒ e}                             matrix binary map rows
                | mfold-row e on e {x, x ⇒ e}                          fold row
                | if e {e} {e}                                         conditional
                | sloop e on e {x, x ⇒ e}                              static finite iteration
                | loop e on e {x, x ⇒ e}                               finite iteration
                | x | let x = e in e | λ x:τ ⇒ e | e e                 variables and functions
                | pλ [β:κ, ..., β:κ] (x:τ , ..., x:τ ) ⇒ e             privacy function
                | inl[τ ] e | inr[τ ] e | case e {x ⇒ e} {x ⇒ e} sums
                | ⟨e, e⟩ | let x, x = e in e                           mult. products
                | ⟨e,, e⟩ | prl e | prr e                              add. products
     Γs ∈ tcxts ≜ var ⇀ sens × type                                    type contexts
                F {x:s τ , ..., x:s τ }
  e ∈ exp F return e | x ← e ; e | e[η, ..., η](x, ..., x) ret, bind and apply
             | sloop[e] e on e <x, ..., x > {x, x ⇒ e}     finite iteration
             | gauss[e, e, e] <x, ..., x > {e}             gaussian noise
             | mgauss[e, e, e] <x, ..., x > {e}            gaussian noise for matrices
             | laplace[e, e] <x, ..., x > {e}              laplacean noise
             | exponential[e, e] e <x, ..., x > {x ⇒ e} exponential mechanism
             | rand-resp[e, e] <x, ..., x > {e}            randomized response
             | sample e on x, x {x, x ⇒ e}                 sampling
             | rand-nat(e, e)                              random natural
 Γp ∈ tcxtp ≜ var ⇀ priv × type                            type contexts
            F {x:p τ , ..., x:p τ }

                              Fig. 12. Sensitivity and Privacy Languages
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
38                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                   ·         ∈ (sens × sens → sens)
               +     ∈ (sens × sens → sens)                                  ⊎ (tcxts × tcxts → tcxts )
                     ⊎ (tcxts × tcxts → tcxts )                    η 1 · η 2 ≜ η1η 2
           η1 + η2 ≜ η1 + η2                                                     0 if s 2 ≈ 0
                                                                    ∞ · s2 ≜
            ∞ + s2 ≜ ∞                                                          ∞ if s 2 ̸≈ 0
            s1 + ∞ ≜ ∞                                                           0 if s 1 ≈ 0
                                                                    s1 · ∞ ≜
       (Γ1 + Γ2 )(x) ≜ Γ1 (x) + Γ2 (x)                                           ∞ if s 1 ̸≈ 0
                                                              (Γ1 · Γ2 )(x) ≜ Γ1 (x) · Γ2 (x)
                           + ∈ (priv × priv → priv)                     ⌉ ⌈ ∈ (sens × sens → sens)
                                 ⊎ (tcxtp × tcxtp → tcxtp )                     ⊎ (tcxt
                                                                                    s × sens → tcxts )
     (ηϵ1 , ηδ1 ) + (ηϵ2 , ηδ2 ) ≜ ηϵ1 +ηϵ2 , ηδ1 +ηδ2                               0 if η ≈ 0
                                                                          ⌉η⌈s ≜
                      ∞ + p2 ≜ ∞                                                     s if η ̸≈ 0
                      p1 + ∞ ≜ ∞                                         ⌉∞⌈s ≜ s
                 (Γ1 + Γ2 )(x) ≜ Γ1 (x) + Γ2 (x)                      ⌉Γ ⌈s (x) ≜ ⌉Γ(x)⌈s
                                           ⌉ ⌈ ∈ (priv × sens → sens)
                                                  ⊎ (tcxt
                                                       p × sens → tcxts )
                                                s      0 if ηϵ ≈ 0 ∧ ηδ ≈ 0
                                     ⌉ηϵ , ηδ ⌈ ≜
                                                       s if ηϵ ̸≈ 0 ∨ ηδ ̸≈ 0
                                           ⌉∞⌈s ≜ s
                                       ⌉Γ⌈s (x) ≜ ⌉Γ(x)⌈s
             ⌉ ⌈ ∈ (priv × priv → priv)                              ⌉ ⌈ ∈ (sens × priv → priv)
                      ⊎ (tcxt
                          p     ×  priv   →  tcxt p )                       ⊎ (tcxt
                                                                                 s × priv → tcxtp )
                           0, 0   if   η ϵ  ≈ 0 ∧ η  δ ≈ 0                       0, 0 if η ≈ 0
        ⌉ηϵ , ηδ ⌈p ≜                                                 ⌉η⌈p ≜
                           p      if ηϵ ̸≈ 0 ∨ ηδ ̸≈ 0                           p     if η ̸≈ 0
              ⌉∞⌈p ≜ p                                               ⌉∞⌈p ≜ p
           ⌉Γ⌈p (x) ≜ ⌉Γ(x)⌈p                                     ⌉Γ ⌈p (x) ≜ ⌉Γ(x)⌈p

                              Fig. 13. Sensitivity and Privacy Metafunctions
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      39

                                                                                                                               ∆⊢η :κ

         RVar                                                                                 Max
          β:κ ∈ ∆                  Nat                          Real
                                                                                              ∆ ⊢ η1 : κ            ∆ ⊢ η2 : κ
                                                                       +       +
          ∆⊢β :κ                    ∆⊢n:N                       ∆⊢r :R                                 ∆ ⊢ η1 ⊔ η2 : κ
   Min                                            Plus                                            Times
    ∆ ⊢ η1 : κ            ∆ ⊢ η2 : κ              ∆ ⊢ η1 : κ               ∆ ⊢ η2 : κ               ∆ ⊢ η1 : κ          ∆ ⊢ η2 : κ
           ∆ ⊢ η1 ⊓ η2 : κ                                ∆ ⊢ η1 + η2 : κ                                   ∆ ⊢ η1 · η2 : κ
    Div                                                  Root                           Log                           Weaken
    ∆ ⊢ η 1 : R+            ∆ ⊢ η 2 : R+                  ∆ ⊢ η : R+                     ∆ ⊢ η : R+                    ∆⊢η :N
                                +                            √
                ∆ ⊢ η 1 /η 2 : R                         ∆ ⊢ η : R+                     ∆ ⊢ ln η : R    +
                                                                                                                      ∆ ⊢ η : R+



                                                                                                                                 ∆⊢s

                                         Sens
                                         ∆ ⊢ η : R+                                     Inf

                                            ∆⊢η                                         ∆⊢∞

                                                                                                                                 ∆⊢p

                              Sens
                              ∆ ⊢ ηϵ : R+            ∆ ⊢ ηδ : R+                                 Inf

                                           ∆ ⊢ ηϵ , ηδ                                           ∆⊢∞



                                                                                                                                 ∆⊢τ

   Static Nat              Static Real                                                                                 Index
   ∆⊢η :N                  ∆ ⊢ η : R+               Nat                     Real              Data
                                                                                                                        ∆⊢η :N
                                     +
   ∆ ⊢ N[η]                ∆ ⊢ R [η]                ∆⊢N                      ∆⊢R              ∆ ⊢ data                 ∆ ⊢ idx[η]
    Matrix                                                             +-F                                   ×-F
    ∆ ⊢ ηm : N             ∆ ⊢ ηn : N             ∆⊢τ                  ∆ ⊢ τ1           ∆ ⊢ τ2               ∆ ⊢ τ1        ∆ ⊢ τ2
                ∆ ⊢ matrixcℓ [ηm , ηn ] τ                                    ∆ ⊢ τ1 + τ2                           ∆ ⊢ τ1 × τ2
                      &-F                                               ⊸-F
                          ∆ ⊢ τ1         ∆ ⊢ τ2                            ∆ ⊢ τ1        ∆ ⊢ τ2           ∆⊢s
                             ∆ ⊢ τ1 & τ2                                            ∆ ⊢ τ1 ⊸s τ2
                  ⊸∗ -F
                  ∆ ′ = ∆ ⊎ {β 1 :κ 1 , ..., βn :κn }           ∆ ′ ⊢ τi (∀i)           ∆ ′ ⊢ pi (∀i)          ∆′ ⊢ τ
                                   ∆ ⊢ ∀ [β 1 :κ 1 , ..., βn :κn ] (τ1 @p1 , ..., τn @pn ) ⊸∗ τ


                                            Fig. 14. Kinding and Type Formation
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
40                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                                                                           ∆, Γ ⊢ e : τ

                                                                           Dynamic Nat                           Dynamic Real
 Singleton Nat                    Singleton Real
                                                                              ∆, Γ ⊢ e : N[η]                      ∆, Γ ⊢ e : R+ [η]
 ∆, Γ ⊢ N[n] : N[n]                ∆, Γ ⊢ R+ [r + ] : R+ [r + ]            ∆, 0Γ ⊢ dyn e : N                      ∆, 0Γ ⊢ dyn e : R
    Dynamic Index                                                                                   Singleton Real Nat
     ∆, Γ ⊢ e : idx[η]                  Nat                         Real
                                                                                                           ∆, Γ ⊢ e : N[η]
     ∆, 0Γ ⊢ dyn e : N                  ∆, Γ ⊢ n : N                ∆, Γ ⊢ r : R                    ∆, 0Γ ⊢ real e : R+ [η]
        Real Nat                               Max
             ∆, Γ ⊢ e : N                      ∆, Γ1 ⊢ e 1 : τ1         ∆, Γ2 ⊢ e 2 : τ2               ⟨s 1 , s 2 , τ ⟩ = τ1 ⊔ τ2
           ∆, Γ ⊢ real e : R                                       ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 ⊔ e 2 : τ
                           Min
                           ∆, Γ1 ⊢ e 1 : τ1          ∆, Γ2 ⊢ e 2 : τ2             ⟨s 1 , s 2 , τ ⟩ = τ1 ⊓ τ2
                                                ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 ⊓ e 2 : τ
                           Plus
                           ∆, Γ1 ⊢ e 1 : τ1          ∆, Γ2 ⊢ e 2 : τ2             ⟨s 1 , s 2 , τ ⟩ = τ1 + τ2
                                                ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 + e 2 : τ
   Times                                                                                     Inverse
    ∆, Γ1 ⊢ e 1 : τ1       ∆, Γ2 ⊢ e 2 : τ2          ⟨s 1 , s 2 , τ ⟩ = τ1 · τ2              ∆, Γ ⊢ e : τ            ⟨s, τ ′⟩ = 1/τ
                      ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 · e 2 : τ                                                ∆, sΓ ⊢ 1/e : τ ′
                 Root
                                                   √                       Log
                 ∆, Γ ⊢ e : τ          ⟨s, τ ′⟩ = τ                        ∆, Γ ⊢ e : τ              ⟨s, τ ′⟩ = ln τ
                                    √
                         ∆, sΓ ⊢ e : τ ′                                                ∆, sΓ ⊢ ln e : τ ′
                        Mod
                         ∆, Γ1 ⊢ e 1 : τ1          ∆, Γ2 ⊢ e 2 : τ2         ⟨s 1 , s 2 , τ ⟩ = τ1 mod τ2
                                                      s1
                                              ∆, ⌉Γ1 ⌈ + s 2 Γ2 ⊢ e 1 mod e 2 : τ
                           Minus
                           ∆, Γ1 ⊢ e 1 : τ1          ∆, Γ2 ⊢ e 2 : τ2             ⟨s 1 , s 2 , τ ⟩ = τ1 − τ2
                                                ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 − e 2 : τ
                          Eq
                           ∆, Γ1 ⊢ e 1 : τ1          ∆, Γ2 ⊢ e 2 : τ2             ⟨s 1 , s 2 , τ ⟩ = τ1 =? τ2
                                                ∆, s 1 Γ1 + s 2 Γ2 ⊢ e 1 =? e 2 : τ


                                  Fig. 15. Sensitivity Typing—Literals and Arithmetic
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      41

                                                                                                                            ∆, Γ ⊢ e : τ

    Matrix Creation
    ∆, Γ1 ⊢ e 1 : N[ηm ]          ∆, Γ2 ⊢ e 2 : N[ηn ]        ∆, Γ3 ⊎ {x 1 :∞ idx[ηm ], x 2 :∞ idx[ηn ]} ⊢ e 3 : τ
            ∆, 0(Γ1 + Γ2 ) + ηm ηn Γ3 : mcreateℓ [e 1 , e 2 ]{x 1 , x 2 ⇒ e 3 } : matrixUℓ [ηm , ηn ] τ
  Matrix Index                                                                           Matrix Rows
   ∆, Γ1 ⊢ e 1 : matrixcℓ [ηm , ηn ] τ         ∆, Γ2 ⊢ e 2 : idx[ηm ]                    ∆, Γ ⊢ e : matrix⋆ [η , η ] τ
                                                                                                          ⋆ m n
             ∆, Γ1 + 0Γ2 ⊢ e 1 #e 2 : matrixcℓ [1, ηn ] τ                                      ∆, 0Γ ⊢ rows e : N[ηm ]
                                                            Clip
        Matrix Cols                                         (this could work for R, but we never need it at that type for examples)

         ∆, Γ ⊢ e : matrix⋆ [η , η ] τ
                          ⋆ m n                                     ∆, Γ ⊢ e : matrix⋆ [1, ηn ] data
                                                                                     ℓ
             ∆, 0Γ ⊢ cols e : N[ηn ]                           ∆, Γ ⊢ clipc e : matrixcℓ [1, ηn ] data
                                       Convert
                                                          ℓ
                                         ∆, Γ ⊢ e : matrix⋆ [1, ηn ] data
                                        ∆, Γ ⊢ conv e : matrixUℓ [1, ηn ] R
   Lipschitz Gradient
                                                                     ℓ
   ∆, Γ1 ⊢ eθ : matrix⋆
                      ⋆
                        [1, ηn ] R             ∆, Γ2 ⊢ e x s : matrix⋆ [1, ηn ] data                          ∆, Γ3 ⊢ ey : data
                                                д
                           ∆, ∞Γ1 + Γ2 + Γ3 ⊢ L∇ℓ [eθ ; e x s , eys ] : matrixUℓ [1, ηn ] R
   Unbounded Gradient
   ∆, Γ1 ⊢ eθ : matrix⋆
                      ⋆
                        [1, ηn ] R             ∆, Γ2 ⊢ e x s : matrix⋆
                                                                     L∞ [1, η n ] data                         ∆, Γ3 ⊢ ey : data
                         ∆, ∞Γ1 + Γ2 + Γ3 ⊢ U ∇[eθ ; e x s , ey ] : matrixUL∞ [1, ηn ] data
                        Matrix Map
                        ∆, Γ1 ⊢ e 1 : matrix⋆
                                            ℓ
                                              [ηm , ηn ] τ1         ∆, Γ2 ⊎ {x:s τ1 } ⊢ e 2 : τ2
                         ∆, sΓ1 + ηm ηn Γ2 ⊢ mmap e 1 {x ⇒ e 2 } : matrixUℓ [ηm , ηn ] τ2
             Matrix Binary Map
                                     ∆, Γ1 ⊢ e 1 : matrix⋆
                                                         ℓ
                                                           [ηm , ηn ] τ1
                 ∆, Γ2 ⊢ e 2 : matrix⋆
                                     ℓ
                                       [η m , η n ] τ 2 ∆, Γ3 ⊎ {x 1 :s1 τ1 , x 2 :s2 τ2 } ⊢ e 3 : τ3
              ∆, s 1 Γ1 + s 2 Γ2 + ηm ηn Γ3 ⊢ mmap e 1 , e 2 {x 1 , x 2 ⇒ e 3 } : matrixUℓ [ηm , ηn ] τ3
 Matrix Map Rows
 ∆, Γ1 ⊢ e 1 : matrixcℓ11 [ηm , ηn1 ] τ1         ∆, Γ2 ⊎ {x:s matrixcℓ11 [1, ηn1 ] τ1 } ⊢ e 2 : matrixcℓ22 [1, ηn2 ] τ2
                      ∆, sΓ1 + ηm Γ2 ⊢ mmap-row e 1 {x ⇒ e 2 } : matrixcℓ22 [ηm , ηn2 ] τ2
       Matrix Binary Map Rows
               ∆, Γ1 ⊢ e 1 : matrixcℓ11 [ηm , ηn1 ] τ1         ∆, Γ2 ⊢ e 2 : matrixcℓ22 [ηm , ηn2 ] τ2
       ∆, Γ3 ⊎ {x 1 :s1 matrixcℓ11 [1, ηn1 ] τ1 , x 2 :s2 matrixcℓ22 [1, ηn2 ] τ2 } ⊢ e 3 : matrixcℓ33 [1, ηn3 ] τ3
            ∆, s 1 Γ1 + s 2 Γ2 + ηm Γ3 ⊢ mmap-row e 1 , e 2 {x 1 , x 2 ⇒ e 3 } : matrixcℓ33 [ηm , ηn3 ] τ3
       Matrix Fold Rows
       ∆, Γ1 ⊢ e 1 : matrixcℓ [ηm , ηn ] τ1   ∆, Γ2 ⊢ e 2 : τ2    ∆, Γ3 ⊎ {x:s1 τ1 , y:s2 τ2 } ⊢ e 3 : τ2
                         ηm
           ∆, s 1 Γ1 + s 2 Γ2 + ηm Γ3 ⊢ mfold-row e 1 on e 2 {x, y ⇒ e 3 } : matrixcℓ [1, ηn ] τ2


                                        Fig. 16. Sensitivity Typing—Matrices
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
42                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                                                                             ∆, Γ ⊢ e : τ

                                     If
                                      ∆, Γ1 ⊢ e 1 : N          ∆, Γ2 ⊢ e 2 : τ           ∆, Γ3 ⊢ e 3 : τ
                                            ∆, ∞Γ1 + Γ2 + Γ3 ⊢ if e 1 {e 2 } {e 3 } : τ
                   Static Loop
                   ∆, Γ1 ⊢ e 1 : N[η]            ∆, Γ2 ⊢ e 2 : τ          ∆, Γ3 ⊎ {x 1 :∞ idx[η], x 2 :s τ } ⊢ e 3 : τ
                                             η
                                  ∆, 0Γ1 + s Γ2 + ηΓ3 ⊢ sloop e 1 on e 2 {x 1 , x 2 ⇒ e 3 } : τ
  Loop
   ∆, Γ1 ⊢ e 1 : N            ∆, Γ2 ⊢ e 2 : τ            ∆, Γ3 ⊎ {x 1 :∞ N, x 2 :1τ } ⊢ e 3 : τ              Var

                 ∆, Γ1 + Γ2 + ∞Γ3 ⊢ loop e 1 on e 2 {x 1 , x 2 ⇒ e 3 } : τ                                    ∆, Γ + {x:1τ } ⊢ x : τ
          Let                                                                         ⊸-I
           ∆, Γ1 ⊢ e 1 : τ1           ∆, Γ2 ⊎ {x:s τ1 } ⊢ e 2 : τ2                    ∆ ⊢ τ1         ∆, Γ ⊎ {x:s τ1 } ⊢ e : τ2
                  ∆, sΓ1 + Γ2 ⊢ let x = e 1 in e 2 : τ2                                ∆, Γ ⊢ (λ x:τ1 ⇒ e) : τ1 ⊸s τ2
                                           ⊸-E
                                           ∆, Γ1 ⊢ e 1 : τ1 ⊸s τ2              ∆, Γ2 ⊢ e 2 : τ1
                                                        ∆, Γ1 + sΓ2 ⊢ (e 1 e 2 ) : τ2
⊸∗ -I
           ∆ ′ = ∆ ⊎ {β 1 :κ 1 , ..., βn :κn }            ∆ ′ ⊢ τi (∀i)          ∆ ′, Γ ⊎ {x 1 , :p1 τ1 , ..., x n :pn τn } ⊢ e : τ
∆, ⌉Γ⌈∞ ⊢ (pλ [β 1 :κ 1 , ..., βn :κn ] (x 1 :τ1 , ..., x n :τn ) ⇒ e) : ∀ [β 1 :κ 1 , ..., βn :κn ] (τ1 @p1 , ..., τn @pn ) ⊸∗ τ
                         ⊎-I-1                                                   ⊎-I-2
                          ∆ ⊢ τ2           ∆, Γ ⊢ e : τ1                           ∆ ⊢ τ1           ∆, Γ ⊢ e : τ2
                         ∆, Γ ⊢ inl[τ2 ] e : τ1 ⊎ τ2                              ∆, Γ ⊢ inr[τ1 ] e : τ1 ⊎ τ2
                  ⊎-E
                  ∆, Γ1 ⊢ e 1 : τ1 ⊎ τ2             ∆, Γ2 ⊎ {x 1 :s τ1 } ⊢ e 2 : τ3         ∆, Γ2 ⊎ {x 2 :s τ2 } ⊢ e 3 : τ3
                                      ∆, sΓ1 + Γ2 ⊢ case e 1 {x 1 ⇒ e 2 } {x 2 ⇒ e 3 } : τ3
           &-I                                                      &-E-1                                  &-E-2
           ∆, Γ ⊢ e 1 : τ1           ∆, Γ ⊢ e 2 : τ2                 ∆, Γ ⊢ e : τ1 & τ2                     ∆, Γ ⊢ e : τ1 & τ2
                  ∆, Γ ⊢ ⟨e 1 , e 2 ⟩ : τ1 & τ2                      ∆, Γ ⊢ prl e : τ1                      ∆, Γ ⊢ prr e : τ2
   ×-I                                                       ×-E
   ∆, Γ1 ⊢ e 1 : τ1              ∆, Γ2 ⊢ e 2 : τ2             ∆, Γ1 ⊢ e 1 : τ1 × τ2            ∆, Γ2 ⊎ {x 1 :s τ1 , x 2 :s τ2 } ⊢ e 2 : τ3
        ∆, Γ1 + Γ2 ⊢ ⟨e 1 , e 2 ⟩ : τ1 × τ2                             ∆, sΓ1 + Γ2 ⊢ let x 1 , x 2 = e 1 in e 2 : τ3


                                     Fig. 17. Sensitivity Typing—Iteration and Connectives
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      43

                                                                                                                        ∆, Γ ⊢ e : τ

              Return                                              Bind
                         ∆, Γ ⊢ e : τ                             ∆, Γ1 ⊢ e 1 : τ1        ∆, Γ2 ⊎ {x:∞τ1 } ⊢ e 2 : τ2
               ∆, ⌉Γ ⌈ ⊢ return e : τ
                         ∞
                                                                            ∆, Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
                ⊸∗ -E
                 ∆ ⊢ ηi : κi (∀i)               ∆, Γ ⊢ e : ∀ [β 1 :κ 1 , ..., βn :κn ] (τ1 @p1 , ..., τn @pn ) ⊸∗ τ
                      ∆, ⌉Γ⌈∞ + {x 1 :p1 τ1 , ..., x n :pn τn } ⊢ e[η 1 , ..., ηn ](x 1 , ..., x n ) : τ [ηi /βi ]
Static Loop (Advanced Composition)
                 ∆, Γ1 ⊢ e 1 : R+ [ηδ ′ ]
                                                                                              η ,η δ
                 ∆, Γ2 ⊢ e 2 : R+ [ηn ]            ∆, Γ3 ⊢ e 3 : τ        ∆, Γ4 + ⌉⌊Γ5⌋⌈ {xϵ ′ , ...,x   ′     ⊎ {x 1 :∞ N, x 2 :∞τ } ⊢ e 4 : τ
                                                                                                   1     n}

                                                    2·η 2·η ln(1/η δ ′ ),η δ ′ + η n η δ
                                                          p
∆, ⌉Γ1 + Γ2 ⌈0,0 + ⌉Γ3 ⌈∞ + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {x ′ϵ, ...,x ′ n}                              ⊢ loop[e 1 ] e 2 on e 3 <x 1′ , ..., x n′ > {x 1 , x 2 ⇒ e 4 }
                                                       1     n
       Gauss
                                                                                                                 η
       Γ1 ⊢ e 1 : R+ [ηs ]        Γ2 ⊢ e 2 : R+ [ηϵ ]           Γ3 ⊢ e 3 : R+ [ηδ ]              Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : R
                                                                                                                    1     n
                                                        η ,η δ
            ⌉Γ1 + Γ2 + Γ3 ⌈0,0 + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {xϵ , ...,x         ⊢ gauss[e     1 , e 2 , e 3 ]   <x 1 , ..., x n  >  {e 4} : R
                                                           1     n}
MGauss
                                                           Γ1 ⊢ e 1 : R+ [ηs ]
                                                                               η
          Γ2 ⊢ e 2 : R+ [ηϵ ]        Γ3 ⊢ e 3 : R+ [ηδ ]           Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : matrix⋆            L2 [ηm , η n ] R
                                                                                  1        n
                                         η ϵ ,η δ
⌉Γ1 + Γ2 + Γ3 ⌈ + ⌉Γ4 ⌈ + ⌉⌊Γ5⌋⌈ {x , ...,x } ⊢ mgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : matrixUL∞ [ηm , ηn ] R
                  0,0         ∞
                                             1      n
               Laplace
                                  +                                                           η
                     Γ1 ⊢ e 1 : R [ηs ]           Γ2 ⊢ e 2 : R+ [ηϵ ]         Γ3 + ⌉⌊Γ4⌋⌈ {xs , ...,x } ⊢ e 3 : R
                                                                                                  1      n
                                                     η ,0
               ⌉Γ1 + Γ2 ⌈0,0 + ⌉Γ3 ⌈∞ + ⌉⌊Γ4⌋⌈ {xϵ , ...,x } ⊢ laplace[e 1 , e 2 ] <x 1 , ..., x n > {e 3 } : R
                                                        1     n
   Exponential
                                                          Γ1 ⊢ e 1 : R+ [ηs ]
                    +                                     ⋆                                      η
      Γ2 ⊢ e 2 : R [ηϵ ]         Γ3 ⊢ e 3 : matrix⋆ [1, ηm ](τ )                Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊎ {x:∞τ } ⊢ e 4 : R
                                                                                                    1       n
                                                   η ,0
    ⌉Γ1 + Γ2 ⌈   0,0
                       + ⌉Γ3 + Γ4 ⌈    ∞
                                           + ⌉⌊Γ5⌋⌈ {xϵ , ...,x } ⊢ exponential[e 1 , e 2 ] <x 1 , ..., x n > e 3 {x ⇒ e 4 } : τ
                                                       1       n
              Rand-Resp
                                                                                            η
                        Γ1 ⊢ e 1 : N[ηn ]            Γ2 ⊢ e 2 : R+ [ηϵ ]        Γ3 + ⌉⌊Γ4⌋⌈ {xn , ...,x } ⊢ e 3 : N
                                                                                                1       n
                                                       η ,0
              ⌉Γ1 + Γ2 ⌈     0,0
                                   + ⌉Γ3 ⌈ ∞
                                               + ⌉⌊Γ4⌋⌈ {xϵ , ...,x } ⊢ rand-resp[e 1 , e 2 ] <x 1 , ..., x n > {e 3 } : N
                                                           1       n
             Sample
              ∆, Γ1 ⊢ e 1 : N[ηm2 ]            ηm 2 ≤ ηm 1             ηϵ ′ = 2·ηm2 ·1/ηm1                ηδ ′ = ηm2 ·1/ηm1
              Γ2 ⊇ {x 1 :(ηϵ ′ ηϵ1 ,ηδ ′ ηδ1 ) Mcℓ11 [m 1 , n 1 ] τ1 , x 2 :(ηϵ ′ ηϵ2 ,ηδ ′ ηδ2 ) Mcℓ22 [m 1 , n 2 ] τ2 }
              ∆, Γ3 ⊎ {y1 :(ηϵ1 ,ηδ1 ) Mcℓ11 [m 2 , n 1 ] τ1 , y2 :(ηϵ2 ,ηδ2 ) Mcℓ22 [m 2 , n 2 ] τ2 } ⊢ e 2 : τ3
                              ⌉Γ1 ⌈0,0 + Γ2 + Γ3 ⊢ sample e 1 on x 1 , x 2 {x 3 , x 4 ⇒ e 2 } : τ3
                                                Rand-Nat
                                                      Γ1 ⊢ e 1 : N         Γ2 ⊢ e 2 : N
                                                 ⌉Γ1 + Γ2 ⌈ ⊢ rand-nat(e 1 , e 2 ) : N
                                                            ∞




                                                     Fig. 18. Privacy Type Systems
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
44                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
       ν, ϵ, δ ∈ R+∞ F r + | ∞
            D ∈ dom ≜ (∥D ∥ ∈ set) × (| |D ∈ ∥D ∥ → R+∞ ) × (| − |D ∈ ∥D ∥ × ∥D ∥ → R+∞ )
            | |DL∞ ∈ matrix[m, n](∥D ∥) → R+∞                          | |DL1 ∈ matrix[m, n](∥D ∥) → R+∞
            |X |DL∞ ≜                                                  |X |DL1 ≜
                      ÍÃ                                                         ÍÍ
                          |X i, j |D                                                |X i, j |D
                         i   j                                                      i   j
                                          | |DL2 ∈ matrix[m,
                                                      rÍ n](∥D ∥) → R∞
                                                                      +

                                          |X |DL2 ≜       |X i, j |D2
                                                    Í
                                                   i    j
                        | − |D ∈ matrix[m, n](∥D ∥) × matrix[m, n](∥D ∥) → R+∞
                                 L∞

                        |X − Y |DL∞ ≜
                                       ÍÃ
                                             |X i, j − Yi, j |D
                                        i j
                         | − |DL1 ∈ matrix[m, n](∥D ∥) × matrix[m, n](∥D ∥) → R+∞
                         |X − Y |DL1 ≜
                                       ÍÍ
                                            |X i, j − Yi, j |D
                                       i j
                         | − |DL2 ∈ matrix[m,
                                         rÍ n](∥D ∥) × matrix[m, n](∥D ∥) → R∞
                                                                                +

                         |X − Y |DL2 ≜         |X i, j − Yi, j |D2
                                       Í
                                       i     j

                                            ∥ N̂[n]∥ ≜ {n}
                                         ∥ R̂+ [r + ]∥ ≜ {r + }
                                                ∥ N̂∥ ≜ N
                                                 ∥ R̂∥ ≜ R
                                             ∥data∥ ≜ R
                                          ∥idx[n]∥ ≜ {m ∈ N | m < n}
                                 c U [m, n](D)∥ ≜ matrix[m, n](∥D ∥)
                           ∥matrix   ⋆
                                 c ℓ [m, n](D)∥ ≜ X ∈ matrix[m, n](∥D ∥) |X | ℓ ≤ 1
                                                         
                           ∥matrix   ⋆                                                           D
                                        ∥D 1 ⊎Dˆ 2 ∥ ≜ ∥D 1 ∥ ⊎ ∥D 2 ∥
                                               ˆ 2 ∥ ≜ ∥D 1 ∥ × ∥D 2 ∥
                                         ∥D 1 ×D
                                              ˆ
                                      ∥D 1 & D 2 ∥ ≜ ∥D   1 ∥ × ∥D 2 ∥
                                    ∥D 1 ⊸c ν D 2 ∥ ≜  f ∈ ∥D 1 ∥ → ∥D 2 ∥ |x − y|D 1 ≤ s ⇒ | f (x) − f (y)|D 2 ≤ s · ν
                                                           f ∈ ∥D 1 ∥ × ··· × ∥D n ∥ → D(X ) |x i − y|D i ≤ 1 ⇒
 ∥(D 1 @(ϵ1 , δ 1 ), ..., D n @(ϵn , δn )) ⊸c∗ X ∥ ≜
                                                                 Pr[f (x 1 ,...,x i ,...,x n ) = d] ≤ e ϵi Pr[f (x 1 ,...,y,...,x n ) = d] + δi }
                ∥ ∀ˆ [β 1 , ..., βn ∈ R∞ ] D [βi ] ∥ ≜ ∀(β 1 ...βn ∈ R+∞ ). ∥D [βi ] ∥
                                        +



                                                     Fig. 19. Metrics (1)
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      45
                                                                 |n|N̂[n] ≜ 0
                                                             |r + |R̂+ [r + ] ≜ 0
                                                                      |n|N̂ ≜ n
                                                                       |r |R̂ ≜ |r |
                                                                   |r |data ≜ |r |
                                                               |m|idx[n] ≜ m
                                                   |X |matrix ⋆
                                                                [m,n](D)
                                                                              ≜ |X |Dℓ
                                                              ℓ
                                                        c
                                               |x 1 ∈ ∥D 1 ∥|D 1 ⊎D  ˆ 2 ≜ |x 1 |D 1
                                               |x 2 ∈ ∥D 2 ∥|D 1 ⊎D  ˆ 2 ≜ |x 2 |D 2
                                                     |x 1 , x 2 |D 1 ×D
                                                                     ˆ 2 ≜ |x 1 |D 1 + |x 2 |D 2
                                                     |x 1 , x 2 |D 1 &D
                                                                     ˆ 2 ≜ |x 1 |D 1 ⊔ |x 2 |D 2
                                                                              Ã
                                                        | f |D 1 ⊸
                                                                 c ν D2 ≜            | f (x)|D 2
                                                                               x ∈ ∥D 1 ∥
                             | f |(D 1 @(ϵ1,δ2 ), ..., D n @(ϵn ,δn ))⊸
                                                                      c ∗X ≜ ∞
                                                                               Ã
                                           |x |∀ˆ [β1, ..., βn ∈R+∞ ] D [β ] ≜   |x [νi /βi ] |D [νi /βi ]
                                                                        i
                                                                               ν i ∈R+∞

                                  |n − n|N̂[n] ≜ 0
                              |r − r + |R̂+ [r + ] ≜ 0
                                +

                                            |n 1 − n 2 |N̂ ≜ |n 1 − n 2 |
                                              |r 1 − r 2 |R̂ ≜ |r
                                                                 1 − r2 |
                                                                 0 if r 1 = r 2
                                          |r 1 − r 2 |data ≜
                                                                 1 if r 1 , r 2
                                    |m 1 − m 2 |idx[n] ≜ |m 1 − m 2 |
                     |X 1 − X 2 |matrix                                        ℓ
                                        c ⋆ [m,n](D) ≜ |X 1 − X 2 |D
                                              ℓ
                                                                 |x 1 − x 2 |D 1 if {x 1 , x 2 } ⊆ ∥D 1 ∥
                                                                
                                                                                      if {x 1 , x 2 } ⊆ ∥D 2 ∥
                                                                
                                                                
                                                      ˆ 2 ≜ |x 1 − x 2 |D 2
                                     |x 1 − x 2 |D 1 ⊎D
                                                                ∞                    if (x 1 ∈ ∥D 1 ∥ ∧ x 2 ∈ ∥D 2 ∥) ∨ (x 1 ∈ ∥D 2 ∥ ∧ x 2 ∈ ∥D 1 ∥
                                                                
                                                                
                   |⟨x 1 , y1 ⟩ − ⟨x 2 , y2 ⟩|D 1 ×D  ˆ 2 ≜ |x 1 − x 2 |D 1 + |y 1 − y 2 |D 2
                   |⟨x 1 , y1 ⟩ − ⟨x 2 , y2 ⟩|D 1 &D  ˆ 2 ≜ |x 1 − x 2 |D 1 ⊔ |y 1 − y 2 |D 2
                                                                   Ã
                                 | f 1 − f 2 |D 1 ⊸c ν D2 ≜               | f 1 (x) − f 2 (x)|D 2
                                                               x∈ ∥D 1 ∥
                                                                 0 if f 1 = f 2
 | f 1 − f 2 |[D 1 @(ϵ1,δ2 ), ..., D n @(ϵn ,δn )]⊸ c ∗D ≜
                                                                 ∞ if f 1 , f 2
                                                                  Ã
               |x 1 − x 2 |∀ˆ [β1, ..., βn ∈R+∞ ] D [β ] ≜              |x 1[νi /βi ] − x 2[νi /βi ] |D [νi /βi ]
                                               i
                                                        ν i ∈R+∞


                                                         Fig. 20. Metrics (2)
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
46                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                                            J K     ∈ rexp × kenv → R+∞

                                                       JβKγ ≜ γ (β)
                                                       JnKγ ≜ n
                                                      Jr + Kγ ≜ r +
                                               Jη 1 ⊔ η 2 Kγ ≜ Jη 1 Kγ ⊔ Jη 2 Kγ
                                               Jη 1 ⊓ η 2 Kγ ≜ Jη 1 Kγ ⊓ Jη 2 Kγ
                                               Jη 1 + η 2 Kγ ≜ Jη 1 Kγ + Jη 2 Kγ
                                                Jη 1 · η 2 Kγ ≜ Jη 1 Kγ · Jη 2 Kγ
                                                    J1/ηKγ ≜ 1/JηK      γ
                                                      √ γ       p
                                                                       γ
                                                     J ηK ≜ JηK
                                                    Jln ηKγ ≜ lnJηKγ

                                                                                            J K     ∈ sens × kenv → R+∞

                                                         JηKγ ≜ JηKγ
                                                        J∞Kγ ≜ ∞

                                                                                    J K     ∈ priv × kenv → R+∞ × R+∞

                                                 Jηϵ , ηδ Kγ ≜ Jηϵ Kγ , Jηδ Kγ
                                                      J∞Kγ ≜ ∞, 0

                                                                                          J K     ∈ type × kenv → dom

                                                      JN[η]Kγ ≜ N̂[JηKγ ]
                                                     JR+ [η]Kγ ≜ R̂+ [JηKγ ]
                                                         JNKγ ≜ N̂
                                                         JRKγ ≜ R̂
                                                      JdataKγ ≜ data
                                                    Jidx[η]Kγ ≜ idx[JηKγ ]
                                  Jmatrixcℓ [ηm , ηm ] τ Kγ ≜ matrixc c [Jηm Kγ , Jηn Kγ ](Jτ Kγ )
                                                                          ℓ
                                                   Jτ1 ⊎ τ2 K ≜ Jτ1 Kγ ⊎Jτ
                                                             γ          ˆ 2 Kγ
                                                   Jτ1 × τ2 Kγ ≜ Jτ1 Kγ ×Jτ
                                                                        ˆ 2 Kγ
                                                             γ
                                                  Jτ1 & τ2 K ≜ Jτ1 K &γ  ˆ Jτ2 Kγ
                                                             γ
                                                Jτ1 ⊸s τ2 K ≜ Jτ1 K ⊸ γ  c Js Kγ Jτ2 Kγ
J∀ [β 1 :κ 1 , ..., βn :κn ] (τ1 @p1 , ..., τn @pn ) ⊸∗ τ Kγ ≜ ∀ˆ [β 1 , ..., βn ∈ R+∞ ] (Jτ1 Kγ @Jp1 Kγ , ..., Jτn Kγ @Jpn Kγ ) ⊸
                                                                                                ′       ′             ′       ′
                                                                                                                                 c ∗ ∥J
                                                                 where γ = γ ⊎ {β 1 , ..., βn }
                                                                            ′


                                                                           J ,      ⊢ K ∈ kcxt × tcxt × type → dom
            ∆                         Γ
 J{β 1 :κ 1 , ..., βn :κn }, {x 1 :s1 τ1 , ..., x n :sn τn } ⊢ τ K ≜ ∀ˆ [β 1 , ..., βn ∈ R+∞ ] (Jτ1 Kγ ⊸
                                                                                                       c Js1 Kγ ···(Jτn Kγ ⊸
                                                                                                                           c Jsn Kγ Jτ Kγ ))
                                                                     where γ = {β 1 , ..., βn }

                                                                           J ,      ⊢ K ∈ kcxt × tcxt × type → dom
            ∆                         Γ
 J{β 1 :κ 1 , ..., βn :κn }, {x 1 :p1 τ1 , ..., x n :pn τn } ⊢ τ K ≜ ∀ˆ [β 1 , ..., βn ∈ R+∞ ] (Jτ1 Kγ @Jp1 Kγ , ..., Jτn Kγ @Jpn Kγ ) ⊸
                                                                                                                                       c ∗ ∥Jτ Kγ ∥
                                                                     where γ = {β 1 , ..., βn }
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      47
C    THEOREMS & LEMMAS
  Theorem C.1 (Gaussian mechanism). If | f (γ ) − f (γ [x i 7→ d])| ≤ r , then for f ′ = λγ . f (γ ) +
                      2 log(1.25/δ )r 2
N (0, σ 2 ) and σ 2 =        ϵ2
                                        , and all ϵi , δi > 0:

                              Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d ′]) = d] + δi


  Proof. By the assumption, ∥ f (γ ) − f (γ [x i 7→ d])∥2 ≤ r . The conclusion follows by Dwork and
Roth [25], Theorem A.1.                                                                           □
   Theorem C.2 (Advanced composition). If:
· Pr[f (γ ) = d] ≤ e ϵi Pr[f (γ [x i 7→ d ′]) = d] + δi
· δ′ > 0 √
                       ′
· ϵˆ = e 2ϵi 2n log(1/δ )
   ˆ
· δ = δ + nδi
          ′

Then:

                                              Pr[iter(k, f (γ ), ι) = d ′′] ≤
                                      e ϵ̂ Pr[iter(k, f (γ [x i 7→ d ′]), ι) = d ′′] + δˆ

Where iter is defined as:

                                          iter(0, f , d) ≜ d
                                          iter(n, f , d) ≜ iter(n − 1, f , f (d))

   Proof. By its definition, iter(n, f , d) is an instance of n-fold adaptive composition of the (ϵi , δi )-
differentially private mechanism f . The conclusion follows from Dwork and Roth [25], Theorem
3.20.
                                                                                                         □
    Theorem C.3 (Seqential Composition). If:
                                 |γ [x i ] − d | ≤ 1 =⇒
                              Pr[f 1 (γ ) = d ′] ≤ e ϵi Pr[f 1 (γ [x i 7→ d]) = d ′] + δi

and:
                                                 |γ [x i ] − d | ≤ 1 =⇒
                                              Pr[f 2 (γ [x 7→ d ′]) = d ′′] ≤
                                   e ϵi Pr[f 2 (γ [x 7→ d ′, x i 7→ d]) = d ′′] + δi′
                                      ′




then:
                                                 |γ [x i ] − d | ≤ 1 =⇒
                                     Pr[f 1 (γ ) = d ′, f 2 (γ [x 7→ d ′]) = d ′′] ≤
                  e ϵi +ϵi Pr[f 1 (γ [x i 7→ d]) = d ′, f 2 (γ [x 7→ d ′, x i 7→ d]) = d ′′] + δi + δi′
                        ′
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
48                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song


   Proof. The conclusion follows from Dwork and Roth [25], Theorem B.1.
                                                                                                                   □

D PROOFS
We define the semantics of each language simultaneously with its proof of correctness. That is,
we give a denotation for well typed terms that inhabits the interpretation of the typing judgment.
We simplify the proof slightly to not consider symbolic real expressions in singleton and matrix
types—the denotation for those expressions is straightforward as elements of real numbers extended
with infinity, so we just consider this set in the proof below. (In this section, we use the same
variable names at different colors to indicate distinct metavariables, e.g., Γ and Γ are not the same.)
  Theorem D.1 (Soundness). There exists an interpretation of well typed terms Γ ⊢ e : τ and
Γ ⊢ e : τ , notated JeK and JeK, such that JeK ∈ JΓ ⊢ τ K and JeK ∈ JΓ ⊢ τ K.
   Proof. We construct the interpretaion by induction on typing derivations Γ ⊢ e : τ and Γ ⊢ e : τ
which are defined mutually inductively.
   We show key cases for the proof in each language. For the sensitivity language Γ ⊢ e : τ , there
is only one interesting case that is not already considered in prior work (Fuzz and DFuzz): the
introduction rule for the privacy lambda.

                                                                         J K ∈ {e ∈ exp | Γ ⊢ e : τ } → JΓ ⊢ τ K

             Γ
- Case ⌉Γ⌈∞ ⊢ (pλ (...,x n :τn ) ⇒ e) : (...,τn @pn ) ⊸∗ τ :
  By inversion:
                                    Γ ⊎ {x 1 , :p1 τ1 , ..., x n :pn τn } ⊢ e : τ

   By induction hypothesis (IH):
                            JeK = f ∈ JΓ ⊎ {x 1 , :p1 τ1 , ..., x n :pn τn } ⊢ τ K

   Define:
                                        Jpλ (...,x n :τn ) ⇒ eK ≜ f ′ where
                                          f ′(γ ) = λγ ′ . f ′(γ ⊎ γ ′)

   To show f ′ ∈ JΓ ⊢ (...,τn @pn ) ⊸∗ τ K, i.e.:
                                            Γ
                                         ′ ′ ′
                          (1)    ∀γ ∈ Jx i :rÛi τi K, d ∈ Jτi K.
                                 |γ [x i ] − d |Jτi′ K ≤ 1
                                     =⇒ | f ′(γ ) − f ′(γ [x i 7→d])|J(...,τn @pn )⊸∗ τ K ≤ rÛi′

   and
                                 (2) ∀γ ∈ JΓK, γ ′ ∈ J{x i , :ϵi ,δi τi }K, d ∈ Jτi K.
                                     |γ [x i ] − d |Jτi K ≤ 1
                                         =⇒ Pr[f ′(γ )(γ ′) = d] ≤
                                                 e ϵi Pr[f ′(γ )(γ ′[x i 7→d]) = d]+δi
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      49



   * (1) Subcase: rÛi′ = ∞
     The property holds trivially when rÛi′ = ∞.
   * (1) Subcase: rÛi′ = 0
     It must be that {x i′:0,0τi′ } ∈ Γ.
     By IH, f is constant w.r.t. x i′ i.e. Pr[f ′(γ )(γ ′) = d] = Pr[f ′(γ )(γ ′[x i′7→d]) = d]
     Therefore | f (γ ) − f (γ [x i′7→d])|Jτi′ K = 0.
   * (2) follows immediately from IH and the definition of J(...,τn @pn )⊸∗τ K
   For the privacy language Γ ⊢ τ we repeat the Return and Bind rules (from Fuzz and DFuzz) in
addition to our novel rules for privacy lambda application, mgauss, and loop. The rest of the rules
in the privacy language are straightforward adaptations of these proofs.

                                                                           J K ∈ {e ∈ exp | Γ ⊢ e : τ } → JΓ ⊢ τ K

              Γ
- Case: ⌉Γ⌈∞ ⊢ return e : τ
  By inversion:
                                                           Γ ⊢e :τ

   By Induction Hypothesis (IH):
                                                      JeK = f ∈ JΓ ⊢ τ K

   Define:
                                        Jreturn eK ≜ f ′ where
                                                            1 if d = f (γ )
                                          Pr[f ′(γ ) = d] ≜
                                                            0 if d , f (γ )

   To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                          Γ
                            ∀γ ∈ Jx i :ϵi , δi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                               =⇒ Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d]) = d] + δi


   * Subcase: ϵi , δi = ∞, 0
     The property holds trivially when ϵi , δi = ∞, 0
   * Subcase: ϵi , δi = 0, 0
     It must be that {x i′:0τi′ } ∈ Γ.
     By IH, f is constant w.r.t. x i i.e.
     | f (γ ) − f (γ [x i 7→d])|Jτi K = 0
     Therefore Pr[f ′(γ ) = d] = Pr[f ′(γ [x i 7→d]) = d]
                             Γ
- Case: ⌉Γ1 ⌈ + {x 1 :p1 τ1 , ..., x n :pn τn } ⊢ e(x 1 ,...,x n ) : τ
                  ∞

  By inversion:
                                              Γ ⊢ e : (τ1 @p1 , ..., τn @pn ) ⊸∗ τ
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
50                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song


  By Induction Hypothesis (IH):
                                   JeK = f ∈ JΓ ⊢ (τ1 @p1 , ..., τn @pn ) ⊸∗ τ K


  Define:
                               Je(x 1 ,...,x n )K ≜ f ′ where
                                  Pr[f ′(γ ) = d] ≜ Pr[f (γ )(γ [x 1 ], ..., γ [x n ]) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                        Γ
                          ∀γ ∈ Jx i :ϵi , δi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                             =⇒ Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d]) = d] + δi

  By definition of + for privacy contexts:
  ϵi , δi = ϵi′ + ϵi′′, δi′ + δi′′ for
  {x i :ϵi′,δi′ τi } ∈ ⌉Γ1 ⌈∞ and ϵi′′, δi′′ = Jpi K.

  * Subcase ϵi′, δi′ = ∞, 0:
    ϵi , δi = ∞, 0; the property holds trivially
  * Subcase ϵi′, δi′ = 0, 0:
    ϵi , δi = ϵi′′, δi′′; the property follows by IH and definition of ⊸∗ instiated to index i.
            Γ
- Case Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
  By inversion:
                                                Γ1 ⊢ e 1 : τ1
                                                Γ2 ⊎ {x:∞τ1 } ⊢ e 2 : τ2

  By Induction Hypothesis (IH):
                                       (1)   Je 1 K = f 1 ∈ JΓ1 ⊢ τ1 K
                                       (2)   Je 2 K = f 2 ∈ JΓ2 ⊎ {x:∞τ1 } ⊢ τ2 K

  Define:
                             Jx←e 1 ;e 2 K ≜ f ′ where
                               Pr[f ′(γ ) = d] ≜ Pr[f 1 (γ ) = d ′, f 2 (γ [x7→d ′]) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                        Γ
                          ∀γ ∈ Jx i :ϵi , δi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                             =⇒ Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d]) = d] + δi

  By definition of + for privacy contexts:
  ϵi , δi = ϵi′ + ϵi′′, δi′ + δi′′ for
  {x i :ϵi′,δi′ τ } ∈ Γ1 and {x i :ϵi′′,δi′′ τ } ∈ Γ2 .
  Property holds via IH.1, IH.2 and theorem C.3 instantiated with (ϵi′, δi′) and (ϵi′′, δi′′).
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      51
- Case:
                               Γ

    ⌉Γ1 + Γ2 + Γ3 ⌈ + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ϵ,δ
                       0,0
                                                 {x 1, ...,x n }
     ⊢ mgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : MUL∞ [m, n] R
  By inversion:
                                         Γ1 ⊢ e 1 : R+ [Ûr ]
                                         Γ2 ⊢ e 2 : R+ [ϵ]
                                         Γ3 ⊢ e 3 : R+ [δ ]
                                         Γ4 + ⌉⌊Γ5⌋⌈r{x
                                                     Û
                                                        , ...,x }
                                                                  ⊢ e 4 : M⋆
                                                                           L2 [m, n] R
                                                           1   n


  By Induction Hypothesis (IH):
                                   Je 1 K = f 1 ∈ JΓ1 ⊢ R+ [Ûr ]K
                                   Je 2 K = f 2 ∈ JΓ2 ⊢ R+ [ϵ]K
                                   Je 3 K = f 3 ∈ JΓ3 ⊢ R+ [δ ]K
                                   Je 4 K = f 4 ∈ JΓ4 + ⌉⌊Γ5⌋⌈r{x
                                                               Û
                                                                  , ...,x }
                                                                            ⊢ M⋆
                                                                               L2 [m, n] RK
                                                                   1   n


  Define:
                               Jmgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 }K ≜ f ′ where
                                 Pr[f ′(γ ) = d] ≜ Pr[f 4 (γ ) + N (0, σ 2 ) = d]
                                        2 log(1.25/δ )r 2
                                 σ2 =          ϵ2
                                 r = f 1 (γ )
                                 ϵ = f 2 (γ )
                                 δ = f 3 (γ )

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                           Γ
                             ∀γ ∈ Jx i :ϵi , δi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                                =⇒ Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d]) = d] + δi
                                      2 log(1.25/δ )rÛ 2
  By IH, we have that σ 2 =                 ϵ2
  By definition of + for privacy contexts:
  ϵi , δi = ϵi′ + ϵi′′ + ϵi′′′ + ϵi′4 + ϵi′5 , δi′ + δi′′ + δi′′′ + δi′4 + δi′5 for
  {x i :ϵi′,δi′ τ } ∈ ⌉Γ1 ⌈0,0
  {x i :ϵi′′,δi′′ τ } ∈ ⌉Γ2 ⌈0,0
  {x i :ϵi′′′,δi′′′ τ } ∈ ⌉Γ3 ⌈0,0
  {x i :ϵi′4,δi′4 τ } ∈ ⌉Γ4 ⌈∞
  {x i :ϵi′5,δi′5 τ } ∈ ⌉⌊Γ5⌋⌈ϵ,δ
                              {x 1, ...,x n }
  Each of ϵi′, ϵi′′, ϵi′′′, δi′, δi′′, δi′′′ must be 0.

  * Subcase ϵi′4 , δi′4 = ∞, 0:
    ϵi , δi = ∞, 0; the property holds trivially
  * Subcase ϵ ′4 , δ ′4 = 0, 0:
    ϵi , δi = ϵi′5 , δi′5 = ϵ, δ
    By IH, | f 4 (γ ) − f 4 (γ [x i 7→ d])|JRK ≤ r
    The property follows from Theorem C.1.
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
52                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song
- Case:
                                    Γ
                                             √
                                         2ϵ 2n ln( 1′ ),δ ′ +nδ
    ⌉Γ1 +Γ2 ⌈0,0 +⌉Γ3 ⌈∞ +⌉Γ4 ⌈∞ +⌉⌊Γ5⌋⌈ {...,x ′ } δ
                                                 n
    ⊢ loop[e 1 ] e 2 on e 3 <...,x n′ > {x 1 ,x 2 ⇒ e 4 } : τ
  By inversion:
                                   Γ1 ⊢ e 1 : R+ [δ ′]
                                   Γ2 ⊢ e 2 : R+ [n]
                                   Γ3 ⊢ e 3 : τ
                                   Γ4 + ⌉⌊Γ5⌋⌈ϵ,δ
                                               {x ′ , ...,x ′ }
                                                                ⊎ {x 1 :∞ N, x 2 :∞τ } ⊢ e 4 : τ
                                                      1   n


  By Induction Hypothesis (IH):
                                Je 1 K = f 1 ∈ JΓ1 ⊢ R+ [δ ′]K
                                Je 2 K = f 2 ∈ JΓ2 ⊢ R+ [n]K
                                Je 3 K = f 3 ∈ JΓ3 ⊢ e 3 : τ K
                                Je 4 K = f 4 ∈ JΓ4 +⌉⌊Γ5⌋⌈ϵ,δ
                                                          {...,x ′ }
                                                                     ⊎{x 1 :∞ N,x 2 :∞τ } ⊢ τ K
                                                                  n


  Define:
                             Jloop[e 1 ] e 2 on e 3 <...,x n′ >{x 1 ,x 2 ⇒e 4 }K ≜ f ′ where
                               Pr[f ′(γ ) = d] ≜
                                 Pr[iter(f 2 (γ ), f 3 (γ )
                                           ,(λxi.f 4 (γ [x 1 7→i][x 2 7→x]))) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                          Γ
                            ∀γ ∈ Jx i :ϵi , δi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                               =⇒ Pr[f ′(γ ) = d] ≤ e ϵi Pr[f ′(γ [x i 7→ d]) = d] + δi

  By definition of + for privacy contexts:
  ϵi , δi = ϵi′ + ϵi′′ + ϵi′′′ + ϵi′4 + ϵi′5 , δi′ + δi′′ + δi′′′ + δi′4 + δi′5 for
  {x i :ϵi′,δi′ τ } ∈ ⌉Γ1 ⌈0,0
  {x i :ϵi′′,δi′′ τ } ∈ ⌉Γ2 ⌈0,0
  {x i :ϵi′′′,δi′′′ τ } ∈ ⌉Γ3 ⌈∞
  {x i :ϵi′4,δi′4 τ } ∈ ⌉Γ4 ⌈∞
  {x i :ϵi′5,δi′5 τ } ∈ ⌉⌊Γ5⌋⌈ϵ,δ
                              {x 1, ...,x n }
  Each of ϵi′, ϵi′′, δi′, δi′′ must be 0.

  * Subcase ϵi′′′, δi′′′ = ∞, 0 or ϵi′4 , δi′4 = ∞, 0:
    ϵi , δi = ∞, 0; the property holds trivially
  * Subcase ϵi′′′, δi′′′ = 0, 0 and ϵ ′4 , δ ′4 = 0, 0:
    ϵi , δi = ϵi′5 , δi′5 = 2ϵ 2n ln(1/δ ′), δ ′ + nδ
                              p

    By IH: Pr[f ′(γ ) = d] ≤ e ϵ Pr[f ′(γ [x i 7→ d]) = d] + δ
    The property holds √by Theorem C.2:
                                  2n log(1/δ ′ )
     Pr[f ′(γ ) = d] ≤ e 2ϵ                        Pr[f ′(γ [x i 7→d]) = d]+δ
                                                                                                   □
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      53
E    RÉNYI DIFFERENTIAL PRIVACY
    Theorem E.1 (Gaussian mechanism (Rényi Differential Privacy)). If | f (γ )− f (γ [x i 7→ d])| ≤
r , then for f ′ = λγ . f (γ ) + N (0, σ 2 ) and σ 2 = αr 2 /(2ϵ), and all α, ϵ > 0:

                                      D α (f ′(γ )∥ f ′(γ [x i 7→ d ′])) ≤ ϵ


    Proof. By Mironov [38], Proposition 7, we have that:

                              D α (f ′(γ )∥ f ′(γ [x i 7→ d ′])) ≤ αr 2 /(2σ 2 ) = ϵ
                                                                                                                 □
    Theorem E.2 (Adaptive seqential composition (Rényi differential privacy)). If:
                                  |γ [x i ] − d | ≤ 1 =⇒
                                       D α (f 1 (γ )∥ f 1 (γ [x i 7→ d])) ≤ ϵi

and:
                                             |γ [x i ] − d | ≤ 1 =⇒
                            D α (f 2 (γ [x 7→ d ′])∥ f 2 (γ [x 7→ d ′, x i 7→ d])) ≤ ϵi′

and:
                         Pr[f 3 (γ ) = d ′′] = Pr[f 1 (γ ) = d ′, f 2 (γ [x 7→ d ′]) = d ′′]

then:
                                             |γ [x i ] − d | ≤ 1 =⇒
                                    D α (f 3 (γ )∥ f 3 (γ [x i 7→ d])) ≤ ϵi + ϵi′


    Proof. The result follows directly from Mironov [38], Proposition 1, setting f = f 1 and д =
f2 .                                                                                           □

  Theorem E.3 (Soundness). There exists an interpretation of well typed terms Γ ⊢ e : τ and
Γ ⊢ e : τ , notated JeK and JeK, such that JeK ∈ JΓ ⊢ τ K and JeK ∈ JΓ ⊢ τ K.
  Proof. We include the cases that are different from the proof for (ϵ, δ )-differential privacy: Bind
and Gauss.

                                                                       J K ∈ {e ∈ exp | Γ ⊢ e : τ } → JΓ ⊢ τ K

           Γ
- Case Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
  By inversion:
                                             Γ1 ⊢ e 1 : τ1
                                             Γ2 ⊎ {x:∞τ1 } ⊢ e 2 : τ2
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
54                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                                                                        ∆, Γ ⊢ e : τ

  Static Loop
                                                                                η ,η
       ∆, Γ1 ⊢ e 1 : R+ [ηn ]           ∆, Γ2 ⊢ e 2 : τ         ∆, Γ3 + ⌉⌊Γ4⌋⌈ {xα ′ , ...,x
                                                                                        ϵ
                                                                                             ′ } ⊎ {x 1 :∞ N, x 2 :∞τ } ⊢ e 3 : τ
                                                                                   1     n
                                                       η ,η n ·η ϵ
  ∆, ⌉Γ1 + Γ1 ⌈  0,0
                       + ⌉Γ2 ⌈ + ⌉Γ3 ⌈
                              ∞            ∞
                                               + ⌉⌊Γ4⌋⌈ {xα ′ , ...,x ′  ⊢ loop e 1 on e 2 <x 1′ , ..., x n′ > {x 1 , x 2 ⇒ e 3 } : τ
                                                           1          n}
      Gauss
                                                                                                         η
      Γ1 ⊢ e 1 : R+ [ηs ]           Γ2 ⊢ e 2 : R+ [η α ]        Γ3 ⊢ e 3 : R+ [ηϵ ]          Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : R
                                                                                                             1     n
                                                        η ,η
           ⌉Γ1 + Γ2 + Γ3 ⌈0,0 + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {xα , ...,x
                                                       ϵ
                                                            }
                                                              ⊢ gauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : R
                                                           1     n
MGauss
                                                        Γ1 ⊢ e 1 : R+ [ηs ]
                                                                           η
         Γ2 ⊢ e 2 : R+ [η α ]          Γ3 ⊢ e 3 : R+ [ηϵ ]      Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : matrix⋆
                                                                                                        L2 [ηm , η n ] R
                                                                                  1      n
                                           η ,η
⌉Γ1 + Γ2 + Γ3 ⌈0,0 + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {xα , ...,x
                                            ϵ
                                                 }
                                                   ⊢ mgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : matrixUL∞ [ηm , ηn ] R
                                               1    n




                       Fig. 22. Privacy Type System Modifications, Rényi Differential Privacy




  By Induction Hypothesis (IH):
                                           (1)     Je 1 K = f 1 ∈ JΓ1 ⊢ τ1 K
                                           (2)     Je 2 K = f 2 ∈ JΓ2 ⊎ {x:∞τ1 } ⊢ τ2 K

  Define:
                                Jx←e 1 ;e 2 K ≜ f ′ where
                                  Pr[f ′(γ ) = d] ≜ Pr[f 1 (γ ) = d ′, f 2 (γ [x7→d ′]) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                                    Γ
                                     ∀γ ∈ Jx i :α i , ϵi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                                        =⇒ D α i (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ ϵi

  By definition of + for privacy contexts:
  ϵi = ϵi′ + ϵi′′ for
  {x i :α i ,ϵi′ τ } ∈ Γ1 and {x i :α i ,ϵi′′ τ } ∈ Γ2 .
  Property holds via IH.1, IH.2 and theorem E.2 instantiated with (α i , ϵi′) and (α i , ϵi′′).
- Case:
                                Γ

    ⌉Γ1 + Γ2 + Γ3 ⌈ + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈α,ϵ
                        0,0
                                                 {x 1, ...,x n }
     ⊢ mgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : MUL∞ [m, n] R
  By inversion:
                                          Γ1 ⊢ e 1 : R+ [Ûr ]
                                          Γ2 ⊢ e 2 : R+ [α]
                                          Γ3 ⊢ e 3 : R+ [ϵ]
                                          Γ4 + ⌉⌊Γ5⌋⌈r{x
                                                      Û
                                                         , ...,x }
                                                                   ⊢ e 4 : M⋆
                                                                            L2 [m, n] R
                                                           1    n
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      55


    By Induction Hypothesis (IH):
                              Je 1 K = f 1 ∈ JΓ1 ⊢ R+ [Ûr ]K
                              Je 2 K = f 2 ∈ JΓ2 ⊢ R+ [α]K
                              Je 3 K = f 3 ∈ JΓ3 ⊢ R+ [ϵ]K
                              Je 4 K = f 4 ∈ JΓ4 + ⌉⌊Γ5⌋⌈r{x
                                                          Û
                                                             , ...,x }
                                                                       ⊢ M⋆
                                                                          L2 [m, n] RK
                                                              1     n


    Define:
                           Jmgauss[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 }K ≜ f ′ where
                             Pr[f ′(γ ) = d] ≜ Pr[f 4 (γ ) + N (0, σ 2 ) = d]
                             σ 2 = r2ϵα
                                      2


                             r = f 1 (γ )
                             α = f 2 (γ )
                             ϵ = f 3 (γ )

    To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                             Γ
                               ∀γ ∈ Jx i :α i , ϵi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                                  =⇒ D α i (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ ϵi

    By IH, we have that σ 2 = r2ϵα
                                    2


    By definition of + for privacy contexts:
    ϵi = ϵi′ + ϵi′′ + ϵi′′′ + ϵi′4 + ϵi′5 for
    {x i :α i ,ϵi′ τ } ∈ ⌉Γ1 ⌈0,0
    {x i :α i ,ϵi′′ τ } ∈ ⌉Γ2 ⌈0,0
    {x i :α i ,ϵi′′′ τ } ∈ ⌉Γ3 ⌈0,0
    {x i :α i ,ϵi′4 τ } ∈ ⌉Γ4 ⌈∞
    {x i :α i ,ϵi′5 τ } ∈ ⌉⌊Γ5⌋⌈α,ϵ
                                {x 1, ...,x n }
    Each of ϵi′, ϵi′′, ϵi′′′ must be 0.

    * Subcase ϵi′4 = ∞:
      ϵi = ∞; the property holds trivially
    * Subcase ϵ ′4 = 0:
      α i , ϵi = α i , ϵi′5 = α, ϵ
      By IH, | f 4 (γ ) − f 4 (γ [x i 7→ d])|JRK ≤ r
      The property follows from Theorem E.1.
                                                                                                            □

F    ZERO-CONCENTRATED DIFFERENTIAL PRIVACY
   Theorem F.1 (Gaussian mechanism (Zero-Concentrated Differential Privacy)). If | f (γ ) −
f (γ [x i 7→ d])| ≤ r , then for f ′ = λγ . f (γ ) + N (0, σ 2 ) and σ 2 = r 2 /(2ρ), and all ρ > 0 and α ≥ 1:

                                        D α (f ′(γ )∥ f ′(γ [x i 7→ d ′])) ≤ α ρ


    Proof. By Bun and Steinke [16], Lemma 2.4, we have that:
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
56                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song

                                                                                                                              ∆, Γ ⊢ e : τ

  Static Loop
                                                                                        η
        ∆, Γ1 ⊢ e 1 : R+ [ηn ]          ∆, Γ2 ⊢ e 2 : τ               ∆, Γ3 + ⌉⌊Γ4⌋⌈ {xρ ′ , ...,x ′ } ⊎ {x 1 :∞ N, x 2 :∞τ } ⊢ e 3 : τ
                                                                                            1       n
                                                          η ·η
  ∆, ⌉Γ1 + Γ1 ⌈0,0 + ⌉Γ2 ⌈∞ + ⌉Γ3 ⌈∞ + ⌉⌊Γ4⌋⌈ {xn ′ , ...,x
                                                       ρ
                                                            ′ } ⊢ loop e 1 on e 2 <x 1 , ..., x n > {x 1 , x 2 ⇒ e 3 } : τ
                                                                                     ′          ′
                                                              1       n
                    Gauss
                                                                                                        η
                      Γ1 ⊢ e 1 : R+ [ηs ]        Γ2 ⊢ e 2 : R+ [η ρ ]               Γ3 + ⌉⌊Γ4⌋⌈ {xs , ...,x } ⊢ e 3 : R
                                                                                                            1   n
                                                      η
                    ⌉Γ1 + Γ2 ⌈0 + ⌉Γ3 ⌈∞ + ⌉⌊Γ4⌋⌈ {xρ , ...,x } ⊢ gauss[e 1 , e 2 ] <x 1 , ..., x n > {e 3 } : R
                                                          1       n
   MGauss
                       +                          +                                 η
        Γ1 ⊢ e 1 : R [ηs ]           Γ2 ⊢ e 2 : R [η ρ ]               Γ3 + ⌉⌊Γ4⌋⌈ {xs , ...,x } ⊢ e 3 : matrix⋆
                                                                                                               L2 [ηm , η n ] R
                                                                                        1       n
                                        η
   ⌉Γ1 + Γ2 ⌈ + ⌉Γ3 ⌈
                0           ∞
                                + ⌉⌊Γ4⌋⌈ {xρ , ...,x } ⊢ mgauss[e 1 , e 2 ] <x 1 , ..., x n > {e 3 } : matrixUL∞ [ηm , ηn ] R
                                            1       n




             Fig. 23. Privacy Type System Modifications, Zero-Concentrated Differential Privacy




                                     D α (f ′(γ )∥ f ′(γ [x i 7→ d ′])) ≤ αr 2 /(2σ 2 ) = α ρ
                                                                                                                                             □

  Theorem F.2 (Adaptive seqential composition (Zero-Concentrated differential pri-
vacy)). For all α ≥ 1, if:
                                                      |γ [x i ] − d | ≤ 1 =⇒
                                              D α (f 1 (γ )∥ f 1 (γ [x i 7→ d])) ≤ α ρ i


and:
                                                      |γ [x i ] − d | ≤ 1 =⇒
                                  D α (f 2 (γ [x 7→ d ′])∥ f 2 (γ [x 7→ d ′, x i 7→ d])) ≤ α ρ i′


and:
                                Pr[f 3 (γ ) = d ′′] = Pr[f 1 (γ ) = d ′, f 2 (γ [x 7→ d ′]) = d ′′]


then:
                                                      |γ [x i ] − d | ≤ 1 =⇒
                                         D α (f 3 (γ )∥ f 3 (γ [x i 7→ d])) ≤ α(ρ i + ρ i′ )


  Proof. The result follows directly from Bun and Steinke [16], Lemma 2.3, setting M = f 1 and
M ′ = f2 .                                                                                   □

  Theorem F.3 (Soundness). There exists an interpretation of well typed terms Γ ⊢ e : τ and Γ ⊢ e : τ ,
notated JeK and JeK, such that JeK ∈ JΓ ⊢ τ K and JeK ∈ JΓ ⊢ τ K.
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      57
  Proof. We include the cases that are different from the proof for (ϵ, δ )-differential privacy: Bind
and Gauss.


                                                                           J K ∈ {e ∈ exp | Γ ⊢ e : τ } → JΓ ⊢ τ K


            Γ
- Case Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
  By inversion:
                                                   Γ1 ⊢ e 1 : τ1
                                                   Γ2 ⊎ {x:∞τ1 } ⊢ e 2 : τ2

  By Induction Hypothesis (IH):
                                        (1)   Je 1 K = f 1 ∈ JΓ1 ⊢ τ1 K
                                        (2)   Je 2 K = f 2 ∈ JΓ2 ⊎ {x:∞τ1 } ⊢ τ2 K

  Define:
                             Jx←e 1 ;e 2 K ≜ f ′ where
                               Pr[f ′(γ ) = d] ≜ Pr[f 1 (γ ) = d ′, f 2 (γ [x7→d ′]) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                               Γ
                                ∀γ ∈ Jx i :α i , ϵi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                                   =⇒ ∀α . D α (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ ρ i

  By definition of + for privacy contexts:
  ρ i = ρ i′ + ρ i′′ for
  {x i :ρ i′ τ } ∈ Γ1 and {x i :ρ i′′ τ } ∈ Γ2 .
  Property holds via IH.1, IH.2 and theorem F.2 instantiated with ρ i′ and ρ i′′.
- Case:
                         Γ
                                    ρ
    ⌉Γ1 + Γ2 ⌈0 + ⌉Γ3 ⌈∞ + ⌉⌊Γ4⌋⌈ {x , ...,x }
                                         1    n
     ⊢ mgauss[e 1 , e 2 ] <x 1 , ..., x n > {e 3 } : MUL∞ [m, n] R
  By inversion:
                                     Γ1 ⊢ e 1 : R+ [Ûr ]
                                     Γ2 ⊢ e 2 : R+ [ρ]
                                     Γ3 + ⌉⌊Γ4⌋⌈r{x
                                                 Û
                                                    , ...,x }
                                                              ⊢ e 3 : M⋆
                                                                       L2 [m, n] R
                                                      1    n



  By Induction Hypothesis (IH):
                               Je 1 K = f 1 ∈ JΓ1 ⊢ R+ [Ûr ]K
                               Je 2 K = f 2 ∈ JΓ2 ⊢ R+ [ρ]K
                               Je 3 K = f 3 ∈ JΓ3 + ⌉⌊Γ4⌋⌈r{x
                                                           Û
                                                              , ...,x }
                                                                        ⊢ M⋆
                                                                           L2 [m, n] RK
                                                               1     n
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
58                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song


    Define:
                             Jmgauss[e 1 , e 2 ] <x 1 , ..., x n > {e 3 }K ≜ f ′ where
                               Pr[f ′(γ ) = d] ≜ Pr[f 3 (γ ) + N (0, σ 2 ) = d]
                                      r2
                               σ 2 = 2ρ
                               r = f 1 (γ )
                               ρ = f 2 (γ )

    To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                           Γ
                               ∀γ ∈ Jx i :ρ i τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                                  =⇒ ∀α . D α (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ ρ i
                                    2     r
    By IH, we have that σ 2 = 2ρ
    By definition of + for privacy contexts:
    ρ i = ρ i′ + ρ i′′ + ρ i′′′ + ρ i′4 for
    {x i :ρ i′ τ } ∈ ⌉Γ1 ⌈0,0
    {x i :ρ i′′ τ } ∈ ⌉Γ2 ⌈0,0
    {x i :ρ i′′′ τ } ∈ ⌉Γ3 ⌈∞
                            ρ
    {x i :ρ i′4 τ } ∈ ⌉⌊Γ4⌋⌈ {x , ...,x }
                               1       n
    Each of ρ i′ , ρ i′′ must be 0.

    * Subcase ρ i′′′ = ∞:
      ρ i = ∞; the property holds trivially
    * Subcase ρ i′′′ = 0:
      ρ i = ρ i′4 = ρ
      By IH, | f 3 (γ ) − f 3 (γ [x i 7→ d])|JRK ≤ r
      The property follows from Theorem F.1.
                                                                                          □

G     TRUNCATED CONCENTRATED DIFFERENTIAL PRIVACY
    Theorem G.1 (Sinh-normal mechanism (Truncated Concentrated Differential Privacy)).
                                                           √
If | f (γ ) − f (γ [x i 7→ d])| ≤ r , ρ > 0, and ω > 1/ ρ, then for
                                                                     1
                                      f ′ = λγ . f (γ ) + ωr arsinh( N (0, σ 2 ))
                                                                    ωr
and σ = r /(2ρ), we have:
         2     2



                              ∀α ∈ (1, ω). D α (f ′(γ )∥ f ′(γ [x i 7→ d ′])) ≤ α ρ


    Proof. The result follows directly from Bun et al.[15], Proposition 4.                □
  Theorem G.2 (Adaptive seqential composition (Truncated Concentrated Differential
Privacy)). If:
                                |γ [x i ] − d | ≤ 1 =⇒
                              ∀α ∈ (1, ωi ). D α (f 1 (γ )∥ f 1 (γ [x i 7→ d])) ≤ α ρ i
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      59

                                                                                                                              ∆, Γ ⊢ e : τ

  Static Loop
                                                                                     η ,η
        ∆, Γ1 ⊢ e 1 : R+ [ηn ]            ∆, Γ2 ⊢ e 2 : τ            ∆, Γ3 + ⌉⌊Γ4⌋⌈ {xρ ′ , ...,x
                                                                                             ω
                                                                                                  ′ } ⊎ {x 1 :∞ N, x 2 :∞τ } ⊢ e 3 : τ
                                                                                        1        n
                                                           η ·η ,η
  ∆, ⌉Γ1 + Γ1 ⌈0,0 + ⌉Γ2 ⌈∞ + ⌉Γ3 ⌈∞ + ⌉⌊Γ4⌋⌈ {xn ′ , ...,x
                                                       ρ ω
                                                            ′ } ⊢ loop e 1 on e 2 <x 1 , ..., x n > {x 1 , x 2 ⇒ e 3 } : τ
                                                                                     ′          ′
                                                             1       n
        SinhNormal
                                                                                                                 η
        Γ1 ⊢ e 1 : R+ [ηs ]           Γ2 ⊢ e 2 : R+ [η ρ ]           Γ3 ⊢ e 3 : R+ [η ω ]            Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : R
                                                                                                                     1   n
                                                    η ,η
        ⌉Γ1 + Γ2 + Γ3 ⌈0,0 + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {xρ , ...,x
                                                    ω
                                                         }
                                                           ⊢ sinh-normal[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : R
                                                       1         n
MSinhNormal
                                                               Γ1 ⊢ e 1 : R+ [ηs ]
                              +                              +                    η
                Γ2 ⊢ e 2 : R [η ρ ]           Γ3 ⊢ e 3 : R [η ω ]      Γ4 + ⌉⌊Γ5⌋⌈ {xs , ...,x } ⊢ e 4 : matrix⋆
                                                                                                               L2 [ηm , η n ] R
                                                                                             1        n
                                              η ,η ω
⌉Γ1 + Γ2 + Γ3 ⌈   0,0
                        + ⌉Γ4 ⌈   ∞
                                      + ⌉⌊Γ5⌋⌈ {xρ , ...,x    ⊢ msinh-normal[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : matrixUL∞ [ηm , ηn ] R
                                                  1        n}




           Fig. 24. Privacy Type System Modifications, Truncated Concentrated Differential Privacy



and:
                                                   |γ [x i ] − d | ≤ 1 =⇒
                         ∀α ∈ (1, ωi ). D α (f 2 (γ [x 7→ d ′])∥ f 2 (γ [x 7→ d ′, x i 7→ d])) ≤ α ρ i′
                                   ′



and:
                                  Pr[f 3 (γ ) = d ′′] = Pr[f 1 (γ ) = d ′, f 2 (γ [x 7→ d ′]) = d ′′]

then:
                                                  |γ [x i ] − d | ≤ 1 =⇒
                              ∀α ∈ (1, ωi ⊓ ωi ). D α (f 3 (γ )∥ f 3 (γ [x i 7→ d])) ≤ α(ρ i + ρ i′ )
                                             ′




  Proof. The result follows directly from Bun et al. [15], Lemma 2, setting M = f 1 and M ′ = f 2 .                                          □

  Theorem G.3 (Soundness). There exists an interpretation of well typed terms Γ ⊢ e : τ and
Γ ⊢ e : τ , notated JeK and JeK, such that JeK ∈ JΓ ⊢ τ K and JeK ∈ JΓ ⊢ τ K.
  Proof. We include the cases that are different from the proof for (ϵ, δ )-differential privacy: Bind
and SinhNormal.

                                                                                      J K ∈ {e ∈ exp | Γ ⊢ e : τ } → JΓ ⊢ τ K

              Γ
- Case Γ1 + Γ2 ⊢ x ← e 1 ; e 2 : τ2
  By inversion:
                                                       Γ1 ⊢ e 1 : τ1
                                                       Γ2 ⊎ {x:∞τ1 } ⊢ e 2 : τ2
Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel
60                               Somani, Mu Zhang, Nikhil Sharma, Alex Shan, and Dawn Song


  By Induction Hypothesis (IH):
                             (1)            Je 1 K = f 1 ∈ JΓ1 ⊢ τ1 K
                             (2)            Je 2 K = f 2 ∈ JΓ2 ⊎ {x:∞τ1 } ⊢ τ2 K

  Define:
                            Jx←e 1 ;e 2 K ≜ f ′ where
                              Pr[f ′(γ ) = d] ≜ Pr[f 1 (γ ) = d ′, f 2 (γ [x7→d ′]) = d]

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                        Γ
                           ∀γ ∈ Jx i :ρ i , ωi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                              =⇒ ∀α ∈ (1, ωi ). D α (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ α ρ i

  By definition of + for privacy contexts:
  ρ i , ωi = ρ i′ + ρ i′′, ωi′ ⊓ ωi′′ for
  {x i :ρ i ,ωi′ τ } ∈ Γ1 and {x i :ρ i ,ωi′′ τ } ∈ Γ2 .
  Property holds via IH.1, IH.2 and theorem G.2 instantiated with (ρ i , ωi′) and (ρ i , ωi′′).
- Case:
                             Γ
                                            ρ,ω
    ⌉Γ1 + Γ2 + Γ3 ⌈ + ⌉Γ4 ⌈∞ + ⌉⌊Γ5⌋⌈ {x , ...,x }
                     0,0
                                              1      n
     ⊢ msinh-normal[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 } : MUL∞ [m, n] R
  By inversion:
                                   Γ1 ⊢ e 1 : R+ [Ûr ]
                                   Γ2 ⊢ e 2 : R+ [ρ]
                                   Γ3 ⊢ e 3 : R+ [ω]
                                   Γ4 + ⌉⌊Γ5⌋⌈r{xÛ
                                                     , ...,x }
                                                               ⊢ e 4 : M⋆
                                                                        L2 [m, n] R
                                                   1    n


  By Induction Hypothesis (IH):
                       Je 1 K = f 1 ∈ JΓ1 ⊢ R+ [Ûr ]K
                       Je 2 K = f 2 ∈ JΓ2 ⊢ R+ [ρ]K
                       Je 3 K = f 3 ∈ JΓ3 ⊢ R+ [ω]K
                       Je 4 K = f 4 ∈ JΓ4 + ⌉⌊Γ5⌋⌈r{x
                                                   Û
                                                      , ...,x }
                                                                ⊢ M⋆
                                                                   L2 [m, n] RK
                                                            1     n


  Define:
                       Jmsinh-normal[e 1 , e 2 , e 3 ] <x 1 , ..., x n > {e 4 }K ≜ f ′ where
                         Pr[f ′(γ ) = d] ≜ Pr[f 4 (γ ) + ωr arsinh( ωr       1
                                                                                N (0, σ 2 )) = d]
                                r 2
                         σ 2 = 2ρ
                         r = f 1 (γ )
                         ρ = f 2 (γ )
                         ω = f 3 (γ )

  To show f ′ ∈ JΓ ⊢ τ K, i.e.:
                                        Γ
                           ∀γ ∈ Jx i :ρ i , ωi τi K, d ∈ Jτi K. |γ [x i ] − d |Jτi K ≤ 1
                              =⇒ ∀α ∈ (1, ωi ). D α (f ′(γ )∥ f ′(γ [x i 7→ d])) ≤ α ρ i
                            r       2
  By IH, we have that σ 2 = 2ρ
Duet: An Expressive Higher-order Language and Linear Type System for Statically Enforcing
Differential Privacy                                                                      61
  By definition of + for privacy contexts:
  ρ i , ωi = ρ i′ + ρ i′′ + ρ i′′′ + ρ i′4 + ρ i′5 , ωi′ + ωi′′ + ωi′′′ + ωi′4 + ωi′5 for
  {x i :ρ i ,ωi′ τ } ∈ ⌉Γ1 ⌈0,0
  {x i :ρ i ,ωi′′ τ } ∈ ⌉Γ2 ⌈0,0
  {x i :ρ i ,ωi′′′ τ } ∈ ⌉Γ3 ⌈0,0
  {x i :ρ i ,ωi′4 τ } ∈ ⌉Γ4 ⌈∞
                              ρ,ω
  {x i :ρ i ,ωi′5 τ } ∈ ⌉⌊Γ5⌋⌈ {x , ...,x }
                                 1       n
  Each of ρ i′ , ρ i′′, ρ i′′′, ωi′, ωi′′, ωi′′′ must be 0.

  * Subcase ρ i′4 = ∞:
    ρ i = ∞; the property holds trivially
  * Subcase ρ ′4 = 0:
    ρ i , ωi = ρ i , ωi′5 = ρ, ω
    By IH, | f 4 (γ ) − f 4 (γ [x i 7→ d])|JRK ≤ r
    The property follows from Theorem G.1.
                                                                                            □
