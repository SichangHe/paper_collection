                                         Contextual Linear Types for Diﬀerential Privacy ∗
                                        MATÍAS TORO, Computer Science Department (DCC), University of Chile, Chile
                                        DAVID DARAIS† , Galois, Inc., USA
arXiv:2010.11342v3 [cs.PL] 1 Mar 2023




                                        CHIKE ABUAH, Computer Science Department, University of Vermont, USA
                                        JOE NEAR, Computer Science Department, University of Vermont, USA
                                        DAMIÁN ÁRQUEZ, Computer Science Department (DCC), University of Chile & IMFD, Chile
                                        FEDERICO OLMEDO, Computer Science Department (DCC), University of Chile & IMFD, Chile
                                        ÉRIC TANTER, Computer Science Department (DCC), University of Chile & IMFD, Chile
                                        Language support for diﬀerentially-private programming is both crucial and delicate. While elaborate pro-
                                        gram logics can be very expressive, type-system based approaches using linear types tend to be more light-
                                        weight and amenable to automatic checking and inference, and in particular in the presence of higher-order
                                        programming. Since the seminal design of Fuzz, which is restricted to 𝜖-diﬀerential privacy in its original
                                        design, signiﬁcant progress has been made to support more advanced variants of diﬀerential privacy, like
                                        (𝜖, 𝛿)-diﬀerential privacy. However, supporting these advanced privacy variants while also supporting higher-
                                        order programming in full has proven to be challenging. We present Jazz, a language and type system which
                                        uses linear types and latent contextual eﬀects to support both advanced variants of diﬀerential privacy and
                                        higher-order programming. Latent contextual eﬀects allow delaying the payment of eﬀects for connectives
                                        such as products, sums and functions, yielding advantages in terms of precision of the analysis and annota-
                                        tion burden upon elimination, as well as modularity. We formalize the core of Jazz, prove it sound for privacy
                                        via a logical relation for metric preservation, and illustrate its expressive power through a number of case
                                        studies drawn from the recent diﬀerential privacy literature.

                                        CCS Concepts: • Security and privacy → Logic and veriﬁcation; • Theory of computation → Linear
                                        logic; Type structures; Program semantics.

                                        Additional Key Words and Phrases: Type Systems, Diﬀerential Privacy
                                        ACM Reference Format:
                                        Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter. 2023.
                                        Contextual Linear Types for Diﬀerential Privacy . ACM Trans. Program. Lang. Syst. 1, 1 (January 2023),
                                        99 pages. https://doi.org/10.1145/000000

                                        ∗ This work is partially funded by ANID FONDECYT Projects 11181208, 1190058, 3200583, ANID Millennium Science Ini-

                                        tiative Program code ICN17_002, and NSF award CCF-2119939.
                                        † Work done in part while at University of Vermont.



                                        Authors’ addresses: Matías Toro, Computer Science Department (DCC), University of Chile, Santiago, Chile; David Darais,
                                        Galois, Inc., Portland, USA; Chike Abuah, Computer Science Department, University of Vermont, Burlington, USA; Joe Near,
                                        Computer Science Department, University of Vermont, Burlington, USA; Damián Árquez, Computer Science Department
                                        (DCC), University of Chile & IMFD, Santiago, Chile; Federico Olmedo, Computer Science Department (DCC), University of
                                        Chile & IMFD, Santiago, Chile; Éric Tanter, Computer Science Department (DCC), University of Chile & IMFD, Santiago,
                                        Chile.


                                        Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                        provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                        the full citation on the ﬁrst page. Copyrights for components of this work owned by others than ACM must be honored.
                                        Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                        prior speciﬁc permission and/or a fee. Request permissions from permissions@acm.org.
                                        © 2023 Association for Computing Machinery.
                                        0164-0925/2023/1-ART $15.00
                                        https://doi.org/10.1145/000000


                                                                          ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
2                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


1   INTRODUCTION
   Note. This paper uses colorblind-friendly colors in notation to convey information, and is best con-
sumed using an electronic device or color printer.
   Over the past decade, diﬀerential privacy [32] has become the de-facto gold standard in protect-
ing the privacy of individuals when processing sensitive data. In contrast to traditional approaches
like de-identiﬁcation, diﬀerential privacy provides a formal, composable privacy guarantee. Diﬀer-
entially private algorithms typically protect privacy by selecting from a handful of basic mecha-
nisms to perturb their outputs. For example, the Laplace mechanism can be used to add noise to the
population count of a city to prevent an adversary from successfully guessing whether or not a par-
ticular individual lives in that city. Most programming-language-based approaches to diﬀerential
privacy are applied to verifying either the implementation of a mechanism, such as the Exponential
mechanism, or the composition of multiple uses of mechanisms, such as computing a histogram
using the Laplace mechanism (multiple times) as a primitive.
   There are two challenges when writing diﬀerentially private programs. First, noise must be
added to the right values in the program in order to achieve some guarantee of privacy; this includes
the ﬁnal output of the program, as well as many intermediate program values. Second, the correct
amount of noise must be added in those places to achieve the desired amount of privacy. In the
diﬀerential privacy framework, privacy is a quantitative feature—more noise gives more privacy.
Adding too little noise is as ineﬀective as adding no noise at all, and adding too much noise renders
the result of the computation useless. Programmers must therefore ensure they have added enough
noise, in the right places, and that the noise is minimal—a daunting task.
   Since diﬀerential privacy is a probabilistic, multi-run (hyper [25]) property, it is not straightfor-
ward to develop test cases for diﬀerentially private algorithms. Consequently, diﬀerentially private
algorithms are usually developed by experts in the ﬁeld, and these experts produce manual proofs
of privacy for each new algorithm. This reliance on experts is limiting. First, there is a practical
need for developing privacy-preserving applications without access to an expert in diﬀerential
privacy. Even still, experts aren’t perfect: for example, several incorrect versions of the Sparse
Vector Technique [31, 32] have appeared in published papers [41], despite being authored and
peer-reviewed by experts in diﬀerential privacy.
   Due to these challenges, verifying diﬀerential privacy in programs via type checking has re-
ceived considerable attention. The ﬁrst such approach, Fuzz [49], uses linear types to verify pure
𝜖-diﬀerential privacy. Fuzz and its successor DFuzz [34] have a number of attractive properties,
including support for automation and higher-order programming. Fuzz was the ﬁrst to use linear
types to bound function sensitivity: how much a function’s output changes given a change to its
input. Sensitivity is then used to determine the (minimal) amount of noise required to achieve
privacy. Fuzz uses the same sensitivity type system to also track privacy, which is advantageous
due to its simplicity, but as a consequence is unable to support advanced variants of diﬀerential
privacy, like (𝜖, 𝛿). A recent approach [29] extends the terminating fragment of Fuzz using graded
comonadic liftings to support advanced variants such as (𝜖, 𝛿)-diﬀerential privacy. In the follow-
ing, we call this extended language Fuzz𝜖𝛿 . Another approach, HOARe2 , uses relational reﬁnement
types to encode diﬀerential privacy [14], and improves on Fuzz-like systems in its ability to sup-
port advanced variants. In general, type-based approaches like Fuzz and HOARe2 are used to verify
programs which compose mechanisms, and not the implementations of mechanisms.
   An alternative set of approaches use program logics [15–17, 50] to verify both the implementa-
tions of mechanisms and simple forms of composing mechanisms, while also supporting advanced
variants like (𝜖, 𝛿)-diﬀerential privacy [32], zero-concentrated diﬀerential privacy [21], and Rényi



ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                        3


diﬀerential privacy [44]. However, these beneﬁts come at the expense of automation and support
for higher-order programming.
   The Duet language [46] and type system strikes a new balance in this space by building on
the designs of Fuzz and DFuzz. Like Fuzz, Duet supports automation and higher-order program-
ming, and like Fuzz𝜖𝛿 , HOARe2 and recently developed program logics, Duet supports advanced
variants of diﬀerential privacy. Like all type-based approaches, Duet cannot be used to verify
implementations of mechanisms, however even when verifying programs which compose mech-
anisms there is still room to improve: Duet is not expressive enough to support higher-order
programming in full generality—something Fuzz, DFuzz, Fuzz𝜖𝛿 and HOARe2 are each able to
achieve.
   This paper presents Jazz, the successor to Duet which signiﬁcantly improves upon its design.
Jazz is a linear type system with support for latent contextual eﬀects for function sensitivity and
diﬀerential privacy; this combination supports advanced privacy variants (like Duet, Fuzz𝜖𝛿 and
HOARe2 ), automation (like Duet and DFuzz), and fully general higher-order programming (like
Fuzz/DFuzz, Fuzz𝜖𝛿 and HOARe2). Like Duet, the Jazz language is built from two mutually-
embedded sublanguages—one for sensitivity, and one for privacy—which allows it to support ad-
vanced variants of diﬀerential privacy automatically through typechecking. Also like Duet (and
Fuzz/DFuzz, Fuzz𝜖𝛿 and HOARe2 ), Jazz is designed for verifying the composition of mechanisms,
and not their direct implementation.
   The key insight of Jazz is the incorporation of latent contextual eﬀects into a linear type system.
A latent eﬀect is one that is deferred or delayed; rather than accounting for the eﬀect immedi-
ately, it is tracked and accounted for later. A contextual eﬀect is one that tracks eﬀect information
for each variable in the context, including closure variables used in higher-order function bodies.
Technically, this is similar to the open closure types introduced by Scherer and Hoﬀmann [51], spe-
cialized to the tracking of sensitivity and privacy, and generalized to positive type constructors
such as sums and products. In addition to supporting higher-order programming in the presence
of advanced privacy variants, these latent contextual eﬀects also can yield advantages in terms of
precision of the analysis, annotation burden, and modularity.

   The challenge of higher-order programming. Consider the 𝑛-iteration loop combinator in Fuzz,
loop𝑛 , which has type 𝜏 → (𝜏 → 𝜏) ⊸𝑛 𝜏. This type describes a two argument function that
takes some value of type 𝜏 as the ﬁrst argument, a function as second argument (which accepts
and returns values of type 𝜏), and returns a ﬁnal value of type 𝜏. The modality in the return type
for the function argument and ﬁnal return type indicates that the function is probabilistic (due to
the use of diﬀerential privacy mechanisms), and when appearing in the codomain of a linear arrow
⊸ indicates that the function satisﬁes diﬀerential privacy.
   Both function sensitivity and diﬀerential privacy are two-run (hyper)properties of a function
output w.r.t. some particular input. For example, a function of body 2𝑥 + 3𝑦 is 2-sensitive in 𝑥 and
3-sensitive in 𝑦, meaning that if e.g. input 𝑥 varies by at most 𝑑 and 𝑦 is held constant, then the
function output varies at most by 2𝑑. When a closure is created, the closure captures sensitivities
as well as values, so the sensitivity of the closure 𝜆𝑥. 2𝑥 + 3𝑦 would be “3 in 𝑦”. The situation is
analogous when tracking privacy and creating closures which capture privacy costs. Looking back
to the type of loop𝑛 in Fuzz, the second argument will be a closure whose captured environment
tracks a privacy cost for each closure variable. The interpretation of the linear function type ⊸𝑛
is to scale the privacy eﬀects in the closure environment of the looping function of type 𝜏 → 𝜏
by 𝑛. We call this scaling implicit and pervasive in Fuzz because it occurs at every let-binding
and function call. In the original Fuzz language, such scaling is only sound and precise for pure

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
4                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


𝜖-diﬀerential privacy, and as a consequence of this pervasive scaling, Fuzz could not be instanti-
ated to advanced diﬀerential privacy variants, until recently, where Fuzz𝜖𝛿 now support advanced
variants such as (𝜖, 𝛿)-diﬀerential privacy through a path metric construction.
   The Duet language prohibits this pervasive scaling in its type system in order to support ad-
vanced diﬀerential privacy variants, but as a consequence it cannot initially derive a type for loop𝑛 ,
and instead it must deﬁne a custom typing rule for loop𝑛 . The issue is that Duet prohibits all scal-
ing of privacy quantities. However, scaling is allowable (i.e., sound) in special restricted instances
when using advanced variants. The challenge is then to disallow implicit pervasive scaling while
allowing explicit restricted scaling. Because no type can be written for loop𝑛 in Duet, it (and many
other higher-order functions) must be given explicit typing rules. This poses a signiﬁcant restric-
tion on higher-order programming, for instance loop𝑛 cannot be lambda-abstracted in Duet.
   Jazz directly solves the challenge of encoding the explicit, restricted scaling that is required to
support both advanced privacy variants and higher-order programming. In Jazz, the type of the
                                                  ⌉Σ ⌈𝜖, 𝛿     ⌉Σ ⌈𝑛𝜖, 𝑛𝛿
𝑛-iteration construct is: loop𝑛 : 𝜏 → (𝜏 −−−−−→            → 𝜏. In this type, the privacy eﬀect on the
                                               → 𝜏) −−−−−−−→
closure is given an explicit representation notated ⌉Σ⌈𝜖, 𝛿 , which means “(𝜖,𝛿)-privacy for variables
in the closure environment Σ”. This eﬀect is latent because the eﬀect isn’t “paid for” until (and each
time) the function is called, and it is contextual because it includes a privacy eﬀect (which may be
“zero”) for each free variable in the context. This eﬀect is then explicitly scaled by 𝑛, the number
of loop iterations, in the ﬁnal eﬀect of applying the function.1 More powerful looping combina-
tors such as advanced composition can also be encoded with these latent contextual eﬀects; such
combinators cannot be described in any prior linear type system—including Fuzz and DFuzz.
   Contributions. Jazz supports writing higher-order programs, and automatically verifying that
such programs satisfy advanced variants of diﬀerential privacy. The novel features of Jazz—linear
types with latent contextual eﬀects—are crucial for practical diﬀerentially-private programming.
We illustrate this expressive power by showing how to encode numerous mechanisms and tools
for diﬀerential privacy as Jazz primitives, including the Laplace, Gaussian, and Exponential mech-
anisms, advanced composition, and privacy ampliﬁcation by subsampling. We also demonstrate
the use of Jazz to verify larger algorithms in two case studies: the MWEM algorithm [38] and
a recently-proposed diﬀerentially-private machine learning algorithm based on gradient descent
with adaptive gradient clipping [53]. Note that these examples are expressible in Duet only by
adding new core typing rules for each primitive used, which strictly speaking requires re-proving
the metatheory of the extended language. In contrast, Jazz subsumes Duet and supports all these
examples without having to add new typing rules, and with a much smaller core language. Fi-
nally, Jazz is amenable to reasonably eﬃcient automated typechecking; we have implemented a
typechecker for the language that can verify privacy costs for our case studies in milliseconds.
   We prove the type soundness of Jazz using a step-indexed logical relation over a mixed big-
step/denotational semantics with embedded discrete probability distributions as probability mass
functions (PMFs).2
   In summary, the contributions of this paper are:
    • Jazz, a practical, higher-order, general purpose programming language for writing diﬀeren-
      tially private programs, which supports advanced variants of diﬀerential privacy.

1 In addition to the color red, we notate the arrow in privacy function types with a double head ։ to further visually

distinguish them from sensitivity function arrows →. We describe details such as the deﬁnition of the ⌉ ⌈ notation later.
2 We restrict ourselves to discrete distributions because considering continuous distributions would complicate the lan-

guage semantics (continuous distributions interact badly with higher-order functions) and our main focus here is on the
type system.


ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                        5


     • A novel linear type system for Jazz which includes latent contextual eﬀects, allowing to de-
       lay the payment of eﬀects of connectives such as product, sums and functions, until actually
       eliminated; e.g. if the second element of a pair is never used, it does not contribute to the
       eﬀect of the program.
     • A formalization and proof of type soundness of 𝜆J , the core language of Jazz, based on a
       proof technique with step-indexed logical relations.
     • A prototype implementation of the Jazz typechecker, together with a library of primitives for
       diﬀerential privacy, and case studies that demonstrate the expressive power and practicality
       of Jazz.
We ﬁrst brieﬂy introduce some key concepts of diﬀerential privacy (§ 2) and then give an overview
of key design choices and beneﬁts of contextual linear types in Jazz (§ 3). Jazz is a two-language
design, and what follows is a presentation of each sub-language in two multi-section arcs. First,
we present the sensitivity-only language design (§ 4) and metatheory (§ 5). This language does not
include diﬀerential privacy operations in the language, or privacy quantities in types. Next, build-
ing on this sensitivity core, we present the full privacy language design and metatheory (§ 6 and
7). Finally, we discuss implementation details including gaps between the actual implementation
of Jazz and its formal model (§ 8), present a few case studies in Jazz (§ 9), discuss related work
(§ 10), and conclude (§ 11).

2   A DIFFERENTIAL PRIVACY PRIMER
Diﬀerential privacy is a mathematical deﬁnition of what it means for a computation over sensitive
data to preserve privacy [32]. It interprets privacy as a form of plausible deniability and relies on
the use of randomization to achieve it. Informally, a randomized algorithm is diﬀerentially private
if the probability that it outputs a particular value remains almost the same with or without a
single individual’s data used as part of the input. Formally, the deﬁnition is parameterized by two
privacy parameters 𝜖 and 𝛿 that specify to what extent two probabilities are “almost the same”, and
by a distance metric over the algorithm’s (sensitive) input whose role we discuss shortly.
    Definition 2.1 (Differential privacy). Given a randomized algorithm (or mechanism) M ∈
𝐴 → 𝐵 and a distance metric 𝔇𝐴 ∈ 𝐴 × 𝐴 → R, the algorithm M satisﬁes (𝜖, 𝛿)-diﬀerential privacy
if for all 𝑥, 𝑥 ′ ∈ 𝐴 such that 𝔇𝐴 (𝑥, 𝑥 ′) ≤ 1 and all possible sets 𝑆 ⊆ 𝐵 of outcomes, Pr[M(𝑥) ∈ 𝑆] ≤
𝑒 𝜖 Pr[M(𝑥 ′) ∈ 𝑆] + 𝛿.
The paramenter 𝜖 quantiﬁes the adversary ability to distinguish two neighbouring inputs upon
observing the corresponding algorithm outputs. It represents the privacy guarantee provided by
the algorithm—the smaller, the less information is leaked about its input. On the other hand, the
parameter 𝛿 represents a failure probability: with probability at most 𝛿, the algorithm is allowed to
violate privacy altogether. In combination, 𝜖 and 𝛿 are typically understood as the “privacy cost”
incurred by publicly releasing the algorithm output, associated to a given sensitive input. The case
where 𝛿 = 0 is called pure (or pure 𝜖-) diﬀerential privacy, and the case where 𝛿 > 0 is called
approximate diﬀerential privacy. Several other recently-proposed variants of the deﬁnition build
on the advantages of (𝜖, 𝛿)-diﬀerential privacy while eliminating the potential for failure; these
include Rényi diﬀerential privacy (RDP) [44], zero-concentrated diﬀerential privacy (zCDP) [21],
and truncated concentrated diﬀerential privacy (tCDP) [20].
    Two algorithm inputs are said to be neighbors if the distance between them is bounded by 1
(i.e. 𝔇(𝑥, 𝑥 ′) ≤ 1). In order for the formal deﬁnition to match our informal statement, the dis-
tance metric 𝔇𝐴 should ensure that neighboring inputs diﬀer by at most one individual’s data.
Formalizing this notion depends heavily on the domain, so diﬀerent deﬁnitions of 𝔇 are used in
diﬀerent domains. When considering a relational database table represented as a bag of tuples, one

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
6                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


commonly-used deﬁnition for 𝔇DB is symmetric diﬀerence [42]: 𝔇DB (𝑥, 𝑥 ′) = |(𝑥 − 𝑥 ′) ∪ (𝑥 ′ − 𝑥)|.
Under this deﬁnition, 𝔇DB (𝑥, 𝑥 ′) = 1 for tables that diﬀer in one row; if the data contributed by each
individual is bounded to a single row, then this is a good approximation of neighboring inputs.
   The deﬁnition of diﬀerential privacy implies two key properties: post-processing and compo-
sition. Post-processing means that the output of a diﬀerentially-private mechanism stays diﬀer-
entially private, no matter what additional processing is applied. Composition allows bounding
the privacy cost of multiple computations over the same underlaying data: running an (𝜖1 , 𝛿 1 )-
diﬀerentially private mechanism followed by an (𝜖2 , 𝛿 2 )-diﬀerentially private mechanism satisﬁes
(𝜖1 + 𝜖2 , 𝛿 1 + 𝛿 2 )-diﬀerential privacy. The privacy parameters 𝜖 and 𝛿 are often called the privacy
cost because of the additive nature of composition.

   Basic Mechanisms, composition, and scaling. Diﬀerential privacy mechanisms typically add noise
to the output of a deterministic function scaled to the function’s sensitivity [32]. A function 𝑓 ∈
𝐴 → 𝐵 with distance metrics 𝔇𝐴 and 𝔇𝐵 is called 𝑠-sensitive if 𝔇𝐴 (𝑥, 𝑦) ≤ 𝑑 =⇒ 𝔇𝐵 (𝑓 (𝑥), 𝑓 (𝑦)) ≤
𝑠𝑑 for every 𝑑 ∈ R and every 𝑥, 𝑦 ∈ 𝐴. Two commonly-used mechanisms are the Laplace [32]
and the Gaussian [7, 32] mechanisms.                Given an 𝑠-sensitive function 𝑓 ∈ 𝐴 → R, the Laplace
mechanism releases 𝑓 (𝑥) + Lap 𝜖𝑠 , where Lap(𝑏) denotes a random sample from the Laplace dis-
                                            

tribution centeredÄ at 0 with scale    ä      𝑏; it satisﬁes 𝜖-diﬀerential privacy. The Gaussian mechanism
                       2𝑠 2 ln(1.25/𝛿)
releases 𝑓 (𝑥) + N            𝜖2
                                         , where N(𝜎 2 ) denotes a random sample from the Gaussian distri-
bution centered at 0 with variance 𝜎 2 and 𝜖, 𝛿 ∈ (0, 1); it satisﬁes (𝜖, 𝛿)-diﬀerential privacy. While
the original Gaussian mechanism requires 𝜖 < 1, Balle and Wang [7] introduce a variant—called
analytic Gaussian mechanism—that drops the requirement that 𝜖 < 1.
   For implementation purposes, naive ﬂoating-point truncations of the real-valued Laplace distri-
bution lead to fatal privacy breaches [43]. Canonne et al. [22] have shown that the Laplacian and
Gaussian mechanisms can both be discretized, while still providing formal privacy guarantees.
   Advanced composition [32] yields tighter bounds on privacy cost for many iterative algorithms,
but requires (𝜖, 𝛿)-diﬀerential privacy. For 𝜖, 𝛿, 𝛿 ′ ≥ 0, the class of (𝜖, 𝛿)-diﬀerentially private
mechanisms satisﬁes (𝜖 ′, 𝑘𝛿 +𝛿 ′ )-diﬀerential      p privacy under 𝑘-fold adaptive composition (e.g. a loop
with 𝑘 iterations) where 𝜖 ′ = 𝑘𝜖(𝑒 𝜖 − 1) +𝜖 2𝑘 ln(1/𝛿 ′ ). Advanced composition is especially useful
for iterative algorithms that perform many diﬀerentially private steps in sequence (e.g. iterative
machine learning algorithms).
   Diﬀerential privacy is stated in terms of neighboring inputs, i.e. inputs 𝑥 and 𝑥 ′ such that
𝔇𝐴 (𝑥, 𝑥 ′) ≤ 1. When 𝔇𝐴 (𝑥, 𝑥 ′) > 1, an 𝜖-diﬀerentially private mechanism provides 𝔇𝐴 (𝑥, 𝑥 ′)·𝜖-
diﬀerential privacy. Distances larger than one are typically interpreted as groups of individuals,
e.g., 𝔇𝐴 (𝑥, 𝑥 ′) = 𝑘 represents a change to 𝑘 individual’s input data. Therefore, an 𝜖-diﬀerentially
private mechanism provides 𝑘𝜖-diﬀerential group privacy [32] for groups of size 𝑘. A similar prop-
erty holds for (𝜖, 𝛿)-diﬀerential privacy and the more recently developed advanced variants, but
the scaling of privacy cost is nonlinear for all of these variants. For example, on inputs at distance 𝑘,
an algorithm satisfying (𝜖, 𝛿)-diﬀerential privacy yields outputs that are only (𝑘𝜖,𝑘𝛿𝑒 (𝑘−1)𝜖 )-close–
instead of (𝑘𝜖,𝑘𝛿)-close. This nonlinearity makes it diﬃcult to apply techniques based on linear
types (which generally internalize linear scaling of costs [34, 49]) for these variants of diﬀerential
privacy.

   Veriﬁcation Techniques for Diﬀerential Privacy. A number of techniques have been proposed
for verifying that a program satisﬁes diﬀerential privacy, including approaches based on linear
logic [29, 34, 46, 49, 59], couplings and program logics [5, 12, 13, 15–17, 50], and randomness
alignments [54, 58]. Our work is most closely related to Fuzz [49] and its descendants DFuzz [34],
Duet [46], and Fuzz𝜖𝛿 [29], which are based on linear type systems. In particular, these approaches

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                        7


focus heavily on fully automated veriﬁcation of diﬀerential privacy properties through typecheck-
ing, and are typically less expressive than program logics, which by contrast support signiﬁcantly
less (or no) automation. We defer a more complete discussion of related work to Section 10.

3 OVERVIEW OF JAZZ
Jazz builds on the linear type system of Fuzz [49] and the two-language design of Duet [46] by
introducing latent contextual eﬀects. This section introduces and motivates the design of Jazz’s
two languages— one for sensitivity and one for privacy—using simple examples. The design of
each language is described in Sections 4 and 6 respectively, and each metatheory is described in
Sections 5 and 7.

3.1 A Two-Language Design
Jazz follows Duet in being structured as two mutually-embedded sublanguages, one for sensitivity
and one for privacy. In a nutshell, this is because supporting scaling of both sensitivity and privacy
in a uniform and tight fashion is sound only for 𝜖-diﬀerential privacy, and not for (𝜖, 𝛿)-diﬀerential
privacy, which has nonlinear group privacy, as discussed in Section 2.
   Let us elaborate on this. Recall that the framework of diﬀerential privacy builds on randomiza-
tion to achieve privacy, and the randomization is typically calibrated according to the sensitivity of
the function whose output one wants to protect. Therefore, in a language to describe diﬀerentially
private computations, we can mostly distinguish two class of functions: On the one hand, random-
ized (eﬀectful) functions that are annotated with privacy information, and on the other hand pure
functions that are annotated with sensitivity information. However, when composing functions,
the way their information is combined highly depends on the class of the composed functions.
   For example, when composing two functions from the sensitivity fragment, their information
is naturally combined via scaling. Consider, for instance, a 3-sensitive function 𝑓 ; it is not hard to
see that the expression
                                                      𝑓 (𝑥 + 𝑥)
is (2 · 3)-sensitive in 𝑥. The same scaling pattern remains valid when composing a function from
the sensitivity fragment with a function from the privacy fragment, provided the latter satisﬁes
pure diﬀerential privacy: If 𝑔 is an e.g. 𝜖-diﬀerentially private function, then the computation
                                                      𝑔(𝑥 + 𝑥)
is (2 · 𝜖)-diﬀerentially private in 𝑥. This uniform scaling behavior, which besides being sound is
also tight, lies at the heart of Fuzz/DFuzz design. In fact, in Fuzz/DFuzz both class of functions
live within the same space, following the same typing rules. To enable this uniform treatment, the
languages rely on the two fundamental ingredients: i) the presence of a monad/modality to encode
randomization, and ii) the association of a metric space to each type, which in the case of monadic
types is tailored to encode diﬀerential privacy. Said otherwise, in Fuzz/DFuzz diﬀerential privacy
is encoded as a sensitivity claim about functions (with a monadic return type).
   Unfortunately, this linear scaling—pervasive in Fuzz/DFuzz—is no longer sound when compos-
ing a function from the sensitivity fragment with a function from the privacy fragment that satis-
ﬁes approximate—rather than pure—diﬀerential privacy. Returning to the previous example, if 𝑔 is
instead (𝜖, 𝛿)-diﬀerentially private, then 𝑔(𝑥 + 𝑥) does not satisfy (2𝜖, 2𝛿)-diﬀerential privacy in 𝑥,
but only (2𝜖, 2𝛿𝑒 𝜖 )-diﬀerential privacy as dictated by the group privacy property for approximate
diﬀerential privacy (see Section 2 and Dwork and Roth [32, §2.3]). In eﬀect, this is why approxi-
mate diﬀerential privacy lies out of the scope of Fuzz/DFuzz “uniform” design—although recently,

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
8                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


de Amorim et al. [29] has shown that using diﬀerent metrics allows approximate diﬀerential pri-
vacy functions to be linear, extending a terminating subset of Fuzz to support (𝜖, 𝛿)-diﬀerentially
privacy via a path metric construction.
   In view of this, Duet introduced a two-language design, separating a sensitivity sublanguage in
which scaling remains implicit (internalized by the typing rules) and pervasive (modeling function
composition), and a privacy sublanguage in which scaling is explicit and restricted (ad-hoc typing
rules are needed e.g. to model some privacy combinators). Jazz builds upon this approach and
signiﬁcantly improves both sublanguages thanks to latent contextual eﬀects, as we illustrate next.

   Coloring convention. As noted in the introduction, this paper uses colorblind-friendly colors in
notation to convey information, and is best consumed using an electronic device or color printer.
Jazz consists of two mutually embedded sublanguages, and each language is given its own color.
Furthermore, these two languages share the same language of types, so we use a third color for
the shared fragment. Consequently, we use three color schemes throughout the paper: (1) blue for
general math notation and the type system shared between languages; (2) green for the sensitiv-
ity language; and (3) red for the privacy language. We have carefully chosen the schemes to be
distinguishable (as much as possible) for persons with various forms of color blindness.3

3.2    Sensitivity
                                                                                            s
In the sensitivity sublanguage of Jazz, the identity function is written 𝜆 𝑥. 𝑥. We write sensitivity
               s                                                                    p
lambdas as 𝜆 to more easily distinguish them from privacy lambdas, written 𝜆 (described later).
The identity function is 1-sensitive in its argument 𝑥: if 𝑥 changes by 𝑑, then the function’s output
                                                                                s
also changes by 𝑑. Similarly to the identity function, the doubling function 𝜆 𝑥 . 𝑥 + 𝑥 is 2-sensitive
in 𝑥: if 𝑥 changes by 𝑑, then the function’s output changes by 2𝑑.
   Fuzz extends the notion of sensitivity to multi-argument functions by assigning a sensitivity
                                                            s    s
to each argument. For example, the curried function 𝜆 𝑥 . 𝜆 𝑦. 𝑥 + 𝑥 + 𝑦 is 2-sensitive in 𝑥 and
1-sensitive in 𝑦. If 𝑥 changes by 𝑑𝑥 and 𝑦 changes by 𝑑 𝑦 , then the function’s output changes by
2𝑑𝑥 + 1𝑑 𝑦 .
   In general, the sensitivity of a function can be written as a linear combination of the changes
in its inputs. In Jazz, we express function sensitivities as linear formulas over the function’s input
variables, using the variable name itself as a placeholder for the change in that input. Jazz’s type
system gives the following types for the three examples we have seen so far:
                                                  s                 𝑥
                                                 (𝜆 𝑥 . 𝑥) : (𝑥 : R) →
                                                                     − R
                                             s                      2𝑥
                                            (𝜆 𝑥 . 𝑥 + 𝑥) : (𝑥 : R) −−→ R
                                    s   s                           0𝑥            2𝑥+𝑦
                               (𝜆 𝑥 . 𝜆 𝑦. 𝑥 + 𝑥 + 𝑦) : (𝑥 : R) −−→ (𝑦 : R) −−−−→ R

The linear formulas written above function arrows represent the sensitivity eﬀect of the corre-
                                                                                                Σ
sponding function. The general form of sensitivity function types is (𝑥 : 𝜏1 ) → − 𝜏2 , where Σ is the
sensitivity eﬀect of the function, expressed as a linear formula. Note that 𝑥 is in scope for Σ and
𝜏2 . Importantly, occurrences of 𝑥 in Σ and 𝜏2 represent the sensitivity of the variable 𝑥, rather than
its value, so Jazz supports sensitivity-dependent types. Also, we usually drop “null” eﬀects over
                               0𝑥
function arrows such as −−→ above, and instead just write →.


3 We chose colors following the 24-Color Palette from http://mkweb.bcgsc.ca/colorblind. E.g., to persons with deuteranopia

(the most common form of color blindness), colorschemes // appear as // respectively.


ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                        9


  As usual, Jazz accommodates higher-order functions by scaling sensitivities. For example, ap-
plying a 2-sensitive function twice yields a 4-sensitive function:
                                s     s                    s                      4𝑦
                              (𝜆 𝑓 . 𝜆 𝑦. 𝑓 𝑦 + 𝑓 𝑦) (𝜆 𝑥 . 𝑥 + 𝑥) : (𝑦 : R) −−→ R
In addition to function types, other type connectives in Jazz like sums and products also carry sen-
sitivity eﬀects, such as 𝜏1 Σ1 ⊕ Σ2 𝜏2 for sums, 𝜏1 Σ1 ⊗ Σ2 𝜏2 for multiplicative products, and 𝜏1 Σ1 &Σ2 𝜏2
for additive products. These connectives are extensions of the linear type connectives 𝜏1 ⊕𝜏2 , 𝜏1 ⊗𝜏2
and 𝜏1 & 𝜏2 from Fuzz, augmented with latent sensitivity eﬀects.
   We say that sensitivity eﬀects in Jazz are latent because they only contribute to the sensitivity of
an expression when the type connective is actually eliminated. For instance, in the third example
above—a curried function—the sensitivity eﬀect on the ﬁrst argument is delayed until the second
argument is received. If a second argument is never received, then the sensitivity eﬀect on the
ﬁrst argument can be ignored. Likewise, the annotations Σ1 and Σ2 in the type 𝜏1 Σ1 ⊗ Σ2 𝜏2 encode
the latent sensitivity cost for each component of the connective: for 𝜏1 (the left) and 𝜏2 (the right)
respectively. In contrast to Fuzz, creating a pair in Jazz can have no immediate sensitivity cost:
only projecting out of a pair has a cost in sensitivity, depending on which component is projected.
Additionally, we say that sensitivity eﬀects are contextual because Σ can refer to variables in scope.

3.3   Privacy
To encode diﬀerential privacy, Jazz makes use of privacy functions (notated ։) rather than of
sensitivity functions (notated →) as in the previous examples. As such, privacy functions are anno-
tated with privacy—rather than sensitivity—eﬀects. The type of a function from 𝜏1 to 𝜏2 which is
(𝜖,𝛿)-diﬀerentially private in its argument is as follows:
                                                               (𝜖, 𝛿)𝑥
                                                  (𝑥 : 𝜏1 ·𝑑) −−−−→
                                                                  → 𝜏2
Semantically, this type describes functions 𝑓 , where if 𝔇𝜏1 (𝑥, 𝑥 ′) ≤ 𝑑 then 𝑓 (𝑥) and 𝑓 (𝑥 ′) yield
distributions which are “(𝜖,𝛿)-close” according to the deﬁnition of (𝜖, 𝛿)-diﬀerential privacy.
   The annotation 𝑑 is necessary to support (and unique to) advanced variants of diﬀerential pri-
vacy like (𝜖, 𝛿)-diﬀerential privacy. In the pure 𝜖-diﬀerential privacy framework, it is common to
ﬁrst establish the property for 𝑑 = 1, that is, if 𝔇𝜏1 (𝑥, 𝑥 ′) ≤ 1 then 𝑓 (𝑥) and 𝑓 (𝑥 ′) are 𝜖-close. Once
established, this property then implies that if 𝔇𝜏1 (𝑥, 𝑥 ′) ≤ 𝑑 then 𝑓 (𝑥) and 𝑓 (𝑥 ′) are 𝑑𝜖-close, for
any 𝑑. However, this linear scaling does not carry over to advanced variants like (𝜖, 𝛿)-diﬀerential
privacy. As a consequence, 𝑑 must be speciﬁed directly as a parameter and cannot be recovered by
scaling the property instantiated to 𝑑 = 1. We refer to this distance—𝑑—as the relational distance
since it pertains to the (two-run) relational property of diﬀerential privacy, and speciﬁcally, the
distance between inputs 𝑥 and 𝑥 ′ for each of the two executions 𝑓 (𝑥) and 𝑓 (𝑥 ′). We also use this
terminology in the context of sensitivity, e.g., an 𝑠-sensitive function is one which upon inputs
within relational distance 𝑑 returns outputs within relational distance 𝑠𝑑.
   As explained in Section 2, diﬀerential privacy is usually achieved by the use of mechanisms like
the Laplace (for 𝜖-diﬀerential privacy) or the Gaussian mechanism (for (𝜖, 𝛿)-diﬀerential privacy).
In Jazz, the primitive function implementing the Laplace mechanism has the following type:

             laplace : ∀(𝑑ˆ : R) (𝜖ˆ : R). (𝑑 : R[𝑑])
                                                  ˆ → (𝜖 : R[𝜖])        ˆ −∞(𝑑+𝜖)+(
                                                             ˆ → (𝑥 : R·𝑑)
                                                                                    ˆ
                                                                                   𝜖,0)𝑥
                                                                           −−−−−−−−−→  →R
There are three logical parameters to the laplace function: 𝑑 is the relational distance (explained
above) used in the statement of privacy satisﬁed by the function, 𝜖 is the privacy level we want to
enforce, and 𝑥 is the value we (want to protect and) are adding noise to. When executing laplace,
the amount of noise added is Lap 𝑑𝜖 which depends on both 𝑑 and 𝜖, so they must be runtime

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
10                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


values. Also, when typechecking laplace, the amount of privacy obtained depends on 𝜖, and the
distance 𝑑 must also be tracked to enforce that the computation feeding laplace with its argument
𝑥 produces values within relational distance no larger than 𝑑. Because the values of 𝑑 and 𝜖 are
required for both runtime execution and type checking, we require a form of dependent types.
    To support dependent types, we use a singletons approach—a technique initially developed for
dependently typed programming in Haskell [33, 39], and which we borrow directly from DFuzz
in the context of supporting parameterized diﬀerentially private functions [34]. In this approach,
each dependent argument has two representations—one for the type and term level respectively.
In the type of laplace, 𝑑ˆ is the type-level representation of term-level variable 𝑑, and likewise for
𝜖ˆ and 𝜖. (We further discuss singletons and their implementation in Section 8.)
    The ﬁnal argument 𝑥 : R·𝑑ˆ will have Laplace noise added to it and then returned as the result of
the laplace function. The annotation “·𝑑” ˆ in the type of 𝑥 places a precondition on the computation
used to supply the value to protect: its output must have relational distance no larger than 𝑑.  ˆ After
all, the noise added is only guaranteed to give 𝜖-diﬀerential privacy for values that result from
computations with relational distance 𝑑.  ˆ
    The ﬁnal privacy eﬀect for the function is ∞(𝑑 + 𝜖) + (𝜖,
                                                            ˆ 0)𝑥, indicating that no privacy promises
are made for the values 𝑑 and 𝜖, and that privacy is promised for input 𝑥 with cost (𝜖,   ˆ 0); we write
∞(𝑑 + 𝜖) as shorthand for ∞𝑑 + ∞𝜖.
    Like Fuzz, DFuzz, and Duet, Jazz extends the notion of diﬀerential privacy from single-argument
to multi-argument functions, assigning each argument a privacy cost (e.g. the privacy eﬀect ∞(𝑑 +
       ˆ 0)𝑥 for the laplace function describes privacy costs for 𝑑, 𝜖, and 𝑥). This approach is for-
𝜖) + (𝜖,
malized in Section 7.3. By convention, most diﬀerentially private programs expect a single input
to contain the sensitive data, and the privacy cost assigned to this argument is most important in
ensuring privacy. The costs associated with the other arguments are typically inﬁnite, indicating
that the program does not preserve privacy for these inputs.
    We can give a similar type to the gauss
                                           function,  which provides (𝜖, 𝛿)-diﬀerential privacy by
                                                  2𝑑 2 ln(1.25/𝛿)
adding Gaussian noise drawn from N                       𝜖2
                                                                    :


                                                                                                            ˆ
gauss : ∀(𝑑ˆ : R) (𝜖ˆ : R) (𝛿ˆ : R). (𝑑 : R[𝑑])
                                            ˆ → (𝜖 : R[𝜖])                   ˆ −∞(𝑑+𝜖+𝛿)+(
                                                                  ˆ → (𝑥 : R·𝑑)
                                                       ˆ → (𝛿 : R[𝛿])
                                                                                           ˆ 𝛿)𝑥
                                                                                          𝜖,
                                                                                −−−−−−−−−−−→   →R

In Jazz, privacy primitives are used in the privacy sublanguage. For example, the following privacy-
sublanguage expression partially applies the Gaussian mechanism to values for 𝑑, 𝜖 and 𝛿, resulting
in a privacy function that satisﬁes (1.5, 10−5 )-diﬀerential privacy for any input at relational distance
4:

                                                                        (1.5, 10−5 )𝑥
                                    gauss 4 1.5 10−5 : (𝑥 : R·4) −−−−−−−−→
                                                                         →R


Note that we omit the instantiation of forall-quantiﬁed type variables 𝑑,  ˆ 𝜖ˆ and 𝛿ˆ to type-level
                       −5
constants 4, 1.5 and 10 , as they can be inferred from the value-level arguments 𝑑, 𝜖 and 𝛿.
   The privacy sublanguage also contains monadic bind (notated ←) and return constructs for
                                                                    p
composing diﬀerentially private computations. Privacy functions 𝜆 (𝑥 ·𝑑). 𝑒 are created in the sen-
sitivity sublanguage (because function creation is “pure”), although the function body 𝑒 lives in the
privacy sublanguage. The annotation 𝑑 is the relational distance explained previously for privacy
function types. For example, the following function computes two diﬀerentially private results and

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       11


adds them together:
               p
              𝜆 (𝑥 ·1). 𝑟 1 ← gauss 1 1.5 0.001 𝑥;                                        (2.0,0.002)𝑥
                        𝑟 2 ← gauss 2 0.5 0.001 (𝑥 + 𝑥);              :       (𝑥 : R·1) −−−−−−−−→
                                                                                                →R
                        return (𝑟 1 + 𝑟 2 )
The bind operator encodes the sequential composition property of diﬀerential privacy (Section 2),
adding up the 𝜖 and 𝛿 values of subcomputations. The return operator encodes the post-processing
property of diﬀerential privacy. The relational distance parameter of 1 is in general inferrable
during type checking; we include it as a visible term-level parameter for presentation purposes.
   Beyond Duet. The privacy sublanguage of Jazz brieﬂy introduced here lifts a number of impor-
tant limitations of the privacy sublanguage of Duet. We sketch two of these here, and postpone
further comparison to later sections.
   First, to avoid scaling in the privacy sublanguage, Duet requires the arguments to privacy func-
tions to have a maximum sensitivity or relational distance of 1. This limitation makes it impossible
to give general types to the gauss and laplace functions as we just shown in Jazz. As a result, Duet
includes a dedicated type rule for each basic diﬀerential privacy mechanism, where each rule is
parametric in the sensitivity or relational distance of the argument. Jazz’s addition of relational
distance annotation “·𝑑” in the types of function arguments eliminates the need for special type
rules, and mechanisms can instead be encoded as primitives with an axiomatized type. The pri-
mary beneﬁt of this is that the metatheory need not be extended each time a new mechanism is
considered.
   Second, while pervasive scaling is generally undesirable for privacy costs, some constructs such
as advanced composition rely on the ability to scale privacy costs in controlled ways that are
supported by theorems speciﬁc to that privacy model. Because Duet’s privacy language disallows
scaling entirely, these constructs are impossible to encode as functions and must also be given
special typing rules. The latent privacy eﬀects in Jazz allow constructs like advanced composition
to be given regular function types. Overall, the Jazz design makes diﬀerential privacy by typing
in the presence of higher-order programming possible for advanced diﬀerential privacy variants.
The following sections dive into these beneﬁts, by focusing ﬁrst on the sensitivity sublanguage
(Section 4), and then the privacy sublanguage (Section 6). Sections 5 and 7 develop the metatheory
of each respective sublanguage.

4 DESIGN OF JAZZ’S SENSITIVITY TYPE SYSTEM
Jazz builds upon prior approaches to encoding diﬀerential privacy using linear types. In this sec-
tion, we ﬁrst overview some limitations of these approaches related to the tracking of sensitivities,
and then discuss how they can be addressed by Jazz. In this section we color expressions and
metavariables green as they pertain to the sensitivity fragment of Jazz.

4.1 Linear Products and Sums
Existing approaches based on linear types [34, 46, 49] provide elementary datatype abstractions
to programmers such as pairs (products) and tagged unions (sums). However, some of the sensitiv-
ity analysis they implement for these datatypes can lead to overly imprecise—or even unsound—
approximations in some circumstances.
   We now brieﬂy overview these datatype abstractions; a summary is provided in Table 1.
Linear products. Because existing systems are based on intuitionistic linear logic, two product
types emerge: multiplicative products ⊗ and additive products &. Multiplicative pairs encode two

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
12                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


 Datatype           Intro.         Elimination          Distance
 Multiplicative h𝑒 1 , 𝑒 2 i       let 𝑥 1, 𝑥 2 = 𝑒     𝔇𝜏1 ⊗𝜏2 (h𝑒 11 , 𝑒 12 i, h𝑒 21 , 𝑒 22 i) , 𝔇𝜏1 (𝑒 11 , 𝑒 21 ) + 𝔇𝜏2 (𝑒 12, 𝑒 22 )
 product (⊗)                       in 𝑒 ′
 Additive           (𝑒 1 , 𝑒 2 )   (1) fst 𝑒            𝔇𝜏1 &𝜏2 ((𝑒 11 , 𝑒 12 ), (𝑒 21, 𝑒 22 )) , max(𝔇𝜏1 (𝑒 11, 𝑒 21 ), 𝔇𝜏2 (𝑒 12 , 𝑒 22 ))
 product (&)                       (2) snd 𝑒
 Sum (⊕)            (1) inl 𝑒      case 𝑒 of            𝔇𝜏1 ⊕𝜏2 (inl 𝑒 11, inl 𝑒 21 ) , 𝔇𝜏1 (𝑒 11 , 𝑒 21 )
                    (2) inr 𝑒      {𝑥 1 ⇒ 𝑒 1 }         𝔇𝜏1 ⊕𝜏2 (inr 𝑒 12, inr 𝑒 22 ) , 𝔇𝜏2 (𝑒 12 , 𝑒 22 )
                                   {𝑥 2 ⇒ 𝑒 2 }         𝔇𝜏1 ⊕𝜏2 (inl 𝑒 11, inr 𝑒 22 ) , 𝔇𝜏1 ⊕𝜏2 (inr 𝑒 12 , inl 𝑒 21 ) , ∞
Table 1. Datatype abstractions provided by systems based on linear types [49].
For defining the distance associated to the datatypes (table last column), we assume that 𝑒11 , 𝑒21 : 𝜏1 and 𝑒12 , 𝑒22 : 𝜏2 .




resources, both of which can be used. Additive pairs encode two resources, but in contrast to mul-
tiplicative pairs, only one of them can be used at a time—a computation may use either their left
or right component, but not both. This constraint is reﬂected on the management of type envi-
ronments in their typing rules. Consider, for instance, the multiplicative product h𝑥, 𝑥i and the
additive product (𝑥, 𝑥). Fuzz generates the following type derivations for the pairs:
           ⊗I                                                            &I
           𝑥 :1 R ⊢ 𝑥 : R            𝑥 :1 R ⊢ 𝑥 : R                     𝑥 :1 R ⊢ 𝑥 : R                  𝑥 :1 R ⊢ 𝑥 : R
                  𝑥 :2 R ⊢ h𝑥, 𝑥i : R ⊗ R                                        𝑥 :1 R ⊢ (𝑥, 𝑥) : R & R

where judgment 𝑥 :𝑠 𝜏 ⊢ 𝑒 : 𝜏 ′ denotes that expression 𝑒 is an 𝑠-sensitive computation on 𝑥
(and has type 𝜏 ′ assuming that 𝑥 has type 𝜏). The type derivation on the left (for multiplicative
products) adds (variablewise) the environments of both components (𝑥 :2 R = 𝑥 :1 R + 𝑥 :1 R),
reporting a sensitivity of 2 in 𝑥. On the other hand, the type derivation on the right (for additive
products) calculates the maximum (variablewise) between the environments of both components
(𝑥 :1 R = max(𝑥 :1 R, 𝑥 :1 R)), reporting a sensitivity of 1 in 𝑥. The elimination rules also follow
these principles: while a multiplicative pair is destructed via pattern matching giving access to
both its components, an additive product is destructed via projection operators that give access to
a single component.
   When applied to sensitivity analysis, these type connectives no longer encode accessibility of
a pair of resources, rather they encode an abstraction of the sensitivities of each component of
the pair. The sensitivity for the whole pair is coarse and either tracks the sum of sensitivities of
each component (in the case of multiplicative products) or their maximum (in the case of additive
products), as reﬂected in the last column of Table 1.
Linear sums. Rather than a simultaneous occurrence of resources, sums encode an alternative oc-
currence of resources. Sums are introduced via inl and inr constructors, and destructed via a
case expression with one branch for each of the constructors.
   In the context of sensitivity analysis, the sensitivity of a sum in(l/r) 𝑒 encodes both the sen-
sitivities of the contained expression 𝑒, as well as the sensitivities for the direction of the injection
(left or right). For example, inl (𝑥+𝑥) is 2-sensitive in 𝑥, however if 𝑦 ≤ 10 then inl 𝑥 else inr 𝑥
is ∞-sensitive in 𝑦 because a change in 𝑦 could change the direction of the injection.
   As usual, these systems leverage sums to encode boolean values, e.g., the boolean type is encoded
as B , unit ⊕ unit, where unit represents the unit type, inhabited by unit value tt. Under this
encoding, an if−then−else expression becomes syntactic sugar for a case expression. Also note

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       13


that boolean values true , inl tt and false , inr tt are at distance ∞ from each other in this
encoding. This observation will be particularly relevant in some of the forthcoming examples.

4.2 Limitations of Prior Sensitivity Linear Type Systems
Fuzz [49] is the ﬁrst work to leverage linear (or aﬃne) types for reasoning about program sensitiv-
ity. Since its introduction, other systems based on linear types were developed to address diﬀerent
limitations of Fuzz. These primarily comprise DFuzz [34], which allows value-dependent sensitiv-
ities and privacy costs, and Duet [46], which allows advanced variants of diﬀerential privacy.
   Being based on the same underlying sensitivity analysis, all these systems suﬀer from common
limitations related to the sensitivity tracking for products and sums. Through a series of minimal—
yet instructive—examples, we now discuss the limitations we have identiﬁed.
Limitations related to linear products. In Fuzz-like systems, each product and sum type introduces
an approximation for the sensitivity analysis they underpin. When using pair types, this approxi-
mation forces the programmer to predict how each pair will be used in later parts of the program,
and select the right one to achieve precision: if only one component of the pair is used, then the ad-
ditive product will give perfect precision; conversely, if both components of the pair are used with
the same sensitivity, then the multiplicative product will give perfect precision. This is limiting for
abstraction, e.g., a library author must commit to one product type, and clients of the library may
turn out to require the other.
   Imprecision issues remain even if functions can be inlined: (1) the optimal product choice may
be inﬂuenced by the dynamic control ﬂow of the program, which cannot be predicted statically in
general; and (2) for multiplicative products in particular, if both components of the pair are used
with diﬀerent sensitivities in the body of the pattern match, the sensitivity estimation may give
imprecise results. To illustrate these limitations, consider the following examples as seen by Fuzz.
  Example 4.1 (dynamic control). The program below contains a branch on a boolean variable,
which determines the usage pattern of an additive pair: while one branch uses one component of
the pair, the other branch uses both.
                                       // variant using an additive pair (·, ·)
                                       let 𝑝 = (2 ∗ 𝑥, 𝑥) in
                                       if 𝑏 then 3 ∗ fst 𝑝
                                            else 2 ∗ (fst 𝑝 + snd 𝑝)
First, observe that the program is semantically equivalent to 6 ∗ 𝑥, which is 6-sensitive in 𝑥. For
the sensitivity analysis à la Fuzz, the pair 𝑝 is assigned 2-sensitivity in 𝑥 (the max of each side).
The if rule pessimistically takes the maximum between the sensitivities of each branch. This
maximum sensitivity is attained by the else-branch and gives 8 = 2 · (2 + 2), where the underlined
2 corresponds to the sensitivity of pair 𝑝 in variable 𝑥.
   Now assume that we rewrite the program using a multiplicative—rather than additive—pair:
                                    // variant using a multiplicative pair h·, ·i
                                    let 𝑥 1, 𝑥 2 = h2 ∗ 𝑥, 𝑥i in
                                    if 𝑏 then 3 ∗ 𝑥 1
                                         else 2 ∗ (𝑥 1 + 𝑥 2 )
In this case, the pair is considered 3-sensitive (rather than 2-sensitive) in 𝑥, an estimate that is
obtained by adding the sensitivities of its two components, instead of taking their maximum. To
obtain the overall program sensitivity, the pair sensitivity is scaled by the maximum sensitivity of
the two branches in either component of the pair; this maximum is attained by the then-branch

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
14                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


and gives 3 (since the else-branch has sensitivity 2 in both pair components). Overall, this gives
an even worse sensitivity in variable 𝑥 of 9 = 3 · 3.
  In summary, following Fuzz-like analysis, there is no choice of product connective that yields
the precise sensitivity bound in 𝑥 of 6.                                                        
  Example 4.2 (imprecise scaling). This example shows how imprecision can arise when compo-
nents of a pair are scaled before introduction, and then in an asymmetric way after elimination.
We only show the multiplicative pair variant.
                                             let 𝑥 1, 𝑥 2 = h2 ∗ 𝑥, 𝑦i in
                                             𝑥1 + 2 ∗ 𝑥2
The above program is semantically equivalent to 2∗𝑥 +2∗𝑦, which is 2-sensitive in 𝑥 and 2-sensitive
in 𝑦. However, the type-based analysis yields a sensitivity bound of 4 in 𝑥, doubling its actual value.
The analysis proceeds roughly as follows. The left component of the pair is 2-sensitive in 𝑥, and
the right component is 1-sensitive in 𝑦. As hinted in the previous example, for multiplicative pairs
Fuzz-like systems sum the sensitivities of each component to yield the sensitivity of the whole, so
the resulting pair is 2-sensitive in 𝑥 and 1-sensitive in 𝑦; note that h2 ∗ 𝑥 + 𝑦, 0i, h0, 2 ∗ 𝑥 + 𝑦i or
even h𝑥, 𝑥 +𝑦i would also result in the exact same sensitivity analysis. The eﬀect of eliminating the
pair via pattern matching is to scale the pair sensitivity by the maximum sensitivity of the body
(𝑥 1 + 2 ∗ 𝑥 2 ) in the pattern variables (𝑥 1 and 𝑥 2 ), 2 in this case. The result is a ﬁnal sensitivity of
4 = 2 · 2 in 𝑥 and 2 = 2 · 1 in 𝑦, which is precise for 𝑦, but imprecise for 𝑥.
    If the program is converted to instead use additive pairs, the sensitivity of the pair construction
is 2 in 𝑥 and 1 in 𝑦 (the pointwise max from of each side), and the sensitivity of the whole expression
is 6 in 𝑥 and 3 in 𝑦—strictly worse than the analysis when using multiplicative pairs.
    We could ﬁx this program in Fuzz, just like in the previous example, by rewriting the program to
use the scaling operator: either let 𝑥 1, 𝑥 2 = h!2 ∗ 𝑥,𝑦i in let 𝑥 2′ = 𝑥 2 in 𝑥 1 + 2 ∗ 𝑥 2 or let 𝑥 1, 𝑥 2 =
h2 ∗ 𝑥, !𝑦i in let 𝑥 2′ = 𝑥 2 in 𝑥 1 + 2 ∗ 𝑥 2 . This may be considered as an annotation burden for
programmers because (1) the programmer must know beforehand that the analysis is imprecise
(which might be hard for long and complex programs), and (2) the programmer must manually
know where to apply scaling to achieve better precision. Also, this process relies in an algorithmic
version of the type system of Fuzz, which is not trivial to achieve [27]. Finally, note that scaling
in Fuzz is restricted to non-zero sensitivities. This means that a program such as let 𝑥 1, 𝑥 2 =
h2 ∗ 𝑥, !𝑦i in 𝑥 1 would be pessimistically considered to be 2-sensitive in 𝑥 and 2-sensitive in 𝑦,
although the program is really 2-sensitive in 𝑥 and 0-sensitive in 𝑦.                                         
Limitations related to linear sums. In addition to imprecision with the product types, Fuzz-like
systems also exhibit imprecision with sum types. In these systems, the sensitivity analysis for a
sum introduction is straightforward: the sensitivity of in(l/r) 𝑒 is simply the sensitivity of 𝑒.
The sensitivity analysis for a sum elimination via expression case 𝑒 of {𝑥 1 ⇒ 𝑒 1 }{𝑥 2 ⇒ 𝑒 2 } is,
however, more involved. First, it computes the sensitivity of 𝑒 𝑖 in binder 𝑥𝑖 for 𝑖 = 1, 2 and retains
the greatest, say 𝑟 . The sensitivity of the overall case expression in some variable, say 𝑥, is then
computed as the sum between (1) the max sensitivity of 𝑒 𝑖 in 𝑥 for 𝑖 = 1, 2, and (2) the sensitivity
of 𝑒 in 𝑥, scaled by 𝑟 . This brings both unsound and imprecise estimations.
   Example 4.3 (discontinuous predicate). An unsound corner case of the above sensitivity analysis
arises, for example, for the program:
                                        if (𝑥 ≤ 10) then true else false
The program, which desugars to case (𝑥 ≤ 10) {𝑥 1 ⇒ true}{𝑥 2 ⇒ false}, is semantically ∞-
sensitive in 𝑥 because changing 𝑥 by, say 1, could change the result from true to false, which are

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       15


inﬁnitely far apart values. Intuitively, we can attribute this to the discontinuity of the program at
𝑥 = 10. As for DFuzz and derivative systems like Duet (which support null sensitivities), they
derive a sensitivity of 0 in 𝑥. To illustrate this, let us consider the corresponding type derivation
in Duet:
         ⊎-E
        𝑥 :∞ R ⊢ 𝑥 ≤ 10 : B             𝑥 :0 R, 𝑥 1 :0 R ⊢ true : B           𝑥 :0 R, 𝑥 2 :0 R ⊢ false : B
                          𝑥 :0 R ⊢ case (𝑥 ≤ 10) {𝑥 1 ⇒ true}{𝑥 2 ⇒ false} : B
The reported sensitivity environment is 0·𝑥 :∞ R + 𝑥 :0 R = 𝑥 :(0·∞+0) R = 𝑥 :0 R: the left summand
0·∞ originates from the fact that branches are 0-sensitive in their binders, and expression 𝑥 ≤ 10
is ∞-sensitive in 𝑥, and the right summand 0 originates from the fact that both branches are 0-
sensitive in 𝑥. Since the product operation (for sensitivities) adopted by DFuzz regards 0·∞ = 0,
the analysis wrongly infers an overall sensitivity of 0 in 𝑥.                                     
   Although DFuzz and derivative systems do not account for this corner case and are, therefore,
unsound, this soundness problem is not present in Fuzz as its type system is constrained to non-
null sensitivities (therefore, leaving the program out of its scope). Follow-up work such as [26]
and Fuzz𝜖𝛿 introduces rules that recover the analysis soundness by interpreting ∞·0 = 0·∞ = ∞
rather than ∞·0 = 0, but this leads to imprecision elsewhere in the system. For example, with this
ﬁx the program let 𝑦 = 𝑥 ≤ 10 in 1 reports sensitivity ∞ in 𝑥 despite the term being equivalent
to the constant 1:
                             𝑥 :∞ R ⊢ 𝑥 ≤ 10 : B             𝑥 :0 R, 𝑦 :0 B ⊢ 1 : R
                                    𝑥 :0·∞ R ⊢ let 𝑦 = 𝑥 ≤ 10 in 1 : R

   A more recent work [28] deﬁnes a non-commutative multiplication operator where 0·∞ = ∞
but ∞·0 = 0. In doing so, it addresses the soundness problem for case expressions, and even
though not supporting let-like operations, it could be extended to do so in a precise manner (e.g.
𝑥 :∞·0 R ⊢ let 𝑦 = 𝑥 ≤ 10 in 1 : R). This multiplication operator is, however, awkward to
manipulate and not amenable to automation due to lack of support for non-commutative ring
theories in SMT solvers. Even still, imprecisions continue to arise in this design, as we will see in
the forthcoming Example 4.4.
   Besides the corner case described above leading to unsound estimates, imprecise estimates can
also arise when eliminating sums. Imprecision arises because, loosely speaking, the analysis ap-
proximates the sensitivity of a sum elimination via a case expression as the maximum sensitivity
of its branches. As illustrated by the following example, this analysis can dismiss signiﬁcant infor-
mation.
  Example 4.4 (conﬂated branches). Consider the following program:
                               let 𝑎 = if 𝑏 then inl (𝑥 ∗ 𝑥) else inr 𝑥 in
                               case 𝑎 of {𝑥 1 ⇒ 0}{𝑥 2 ⇒ 𝑥 2 }
A sum is created as either the left injection of an expression that is ∞-sensitive in 𝑥 (since 𝑥 ∗ 𝑥
is so), or the right injection of an expression 1-sensitive in 𝑥. In Fuzz-like systems, such a sum is
conservatively deemed ∞-sensitive in 𝑥. The sum is then eliminated with a constant left branch,
and a right branch that is 1-sensitive in its binder. The ground truth for the program is that it is 1-
sensitive in 𝑥, as the left injection ∞-sensitive in 𝑥 is eliminated to a constant. However, the usual
linear typing discipline does not match the sensitivities of each injection with the case-branch
that each injection would see, reporting an imprecise ﬁnal sensitivity of ∞ in 𝑥.                    

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
16                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


4.3 Latent Contextual Eﬀects for Precise Sensitivity Tracking in Jazz
Jazz adopts a novel approach to sensitivity tracking for product and sum types, which can address
the previous limitations without the need to rely on scaling of types. The key insight is to delay
the tracking of sensitivities whenever possible, and to split it into two separate analyses: one for
each side of the product or sum. Technically, the main idea is to encode latent sensitivity eﬀects at
the type-connective level. For instance, for multiplicative pairs Jazz has type 𝜏1 Σ1 ⊗ Σ2 𝜏2 , where
Σ1 and Σ2 denote the latent sensitivity eﬀects of each of the pair components. This is in contrast to
the Fuzz type 𝜏1 ⊗ 𝜏2 , which pays for all of its sensitivity eﬀects upfront, when the pair is created.
Precise products. Consider the three related multiplicative pair constructions:
                        𝑒 1 , h2 ∗ 𝑥 + 𝑦, 0i        𝑒 2 , h0, 2 ∗ 𝑥 + 𝑦i         𝑒 3 , h𝑥, 𝑥 + 𝑦i
For the purpose of sensitivity analysis, Fuzz is unable to distinguish them, as it derives the very
same type judgment for all three, namely
                                𝑥 :2 R, 𝑦 :1 R ⊢ 𝑒 : R ⊗ R          for 𝑒 ∈ {𝑒 1 , 𝑒 2, 𝑒 3 }
The type judgment says that the pairs are 2-sensitive in 𝑥 and 1-sensitive in 𝑦 (the subscript annota-
tions in the type environment), but does not say how this sensitivity eﬀect is distributed between
the pair components. In other words, Fuzz treats pairs as a whole. In contrast, Jazz can derive
three diﬀerent type judgments, precisely capturing the sensitivity of each pair component:
     𝑥 : R, 𝑦 : R ⊢ 𝑒 1 : R 2𝑥+𝑦 ⊗ R       𝑥 : R, 𝑦 : R ⊢ 𝑒 2 : R ⊗2𝑥+𝑦 R             𝑥 : R, 𝑦 : R ⊢ 𝑒 3 : R 𝑥 ⊗𝑥+𝑦 R
Recall from Section 3.2 that in Jazz we use linear formulas to denote sensitivity eﬀects and there-
fore, in e.g. the ﬁrst type judgment above, 2𝑥 +𝑦 refers to the sensitivity eﬀect Σ , {𝑥 ↦→ 2, 𝑦 ↦→ 1},
meaning 2-sensitive in 𝑥, and 1-sensitive in 𝑦. Moreover, we elide null sensitivity eﬀects likes 0𝑥+0𝑦.
This ﬁne-grained tracking of the sensitivity of each pair component allows, in turn, deferring the
payment of the pair sensitivity eﬀect to the precise point where the pair is used, i.e. eliminated,
and therefore paying only for what (and how it) is used. For example, if pair 𝑒 3 is used in a context
where only its ﬁrst component is referred, we pay for sensitivity eﬀect 𝑥. Fuzz, in contrast, would
always pay 2𝑥 + 𝑦.
   Let us discuss the beneﬁts that this ﬁne-grained tracking brings to Examples 4.1 and 4.2. Con-
sider ﬁrst the program from Example 4.1, more concretely, the variant with additive pairs. The
sensitivity of the then-branch is calculated as 6𝑥 from scaling by 3 the (latent) sensitivity eﬀect
2𝑥 of the left component of pair 𝑝. Likewise, the sensitivity of the else-branch is calculated also
as 6𝑥 from scaling by 2 the sum of (latent) sensitivity eﬀects 2𝑥 and 𝑥 of the respective left and
right component of the pair. As a result, Jazz reports the precise sensitivity of 6𝑥 for the whole
program. An analogous ﬁne-grained tracking for the program from Example 4.2 gives also precise
sensitivity 2𝑥 + 2𝑦.
Precise sums. The use of latent sensitivity eﬀects yields tighter sensitivity bounds also for sums.
However, the handling of sums impose an additional technical challenge related to the impossibil-
ity of delaying sensitivity eﬀects. To illustrate this phenomenon, consider expressions:
           𝑒 4 , inl (𝑥 ∗ 𝑥)       𝑒 5 , inr (𝑥 ∗ 𝑥)         𝑒 6 , if (𝑥 ≤ 10) then inl 1 else inr 1
All three expressions are ∞-sensitive in 𝑥. Fuzz sensitivity analysis conﬂates the three expressions
to the same type, and some Fuzz derivative systems with support for 0-sensitivities such as DFuzz,
derive an unsound type (w.r.t. the embodied sensitivity analysis) for 𝑒 6 : 𝑥 :0 R ⊢ 𝑒 6 : R ⊕ R.
                   𝑥 :∞ R ⊢ 𝑒 4 : R ⊕ R          𝑥 :∞ R ⊢ 𝑒 5 : R ⊕ R           𝑥 :∞ R ⊢ 𝑒 6 : R ⊕ R

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                           17


Jazz derives instead:
                  𝑥 : R ⊢ 𝑒 4 : R ∞𝑥 ⊕ R           𝑥 : R ⊢ 𝑒 5 : R ⊕∞𝑥 R           𝑥 : R ⊢ 𝑒6 : R ⊕ R
The types of 𝑒 4 and 𝑒 5 encode a latent sensitivity eﬀect for each side of the sum. In contrast, the type
of 𝑒 6 is not able to represent its ∞-sensitivity in 𝑥 as a latent eﬀect because 𝑥 inﬂuences which
injection is used to create the sum itself, not the value inside the injection. Instead, the eﬀect
must be paid for eagerly in the so-called ambient sensitivity eﬀect (which was elided in previous
examples). Therefore type judgments in Jazz have shape Γ ⊢ 𝑒 : 𝜏 ; Σ, where Σ represents the
ambient sensitivity eﬀect and Γ is a “traditional” environment, mapping variables to types. Thus,
expression 𝑒 6 is formally typed as:
                                               𝑥 : R ⊢ 𝑒 6 : R ⊕ R ; ∞𝑥
with ambient sensitivity eﬀect ∞𝑥. 𝑒 4 is typed as 𝑥 : R ⊢ 𝑒 4 : R ∞𝑥 ⊕ R ; ∅, i.e., with an empty
ambient sensitivity eﬀect, and analogously for 𝑒 5 .
   To showcase the beneﬁts of this design, let us re-examine Example 4.4. In Jazz, the type for 𝑎
is R ∞𝑥 ⊕𝑥 R with ambient eﬀect 𝑏.4 To compute the sensitivity of the case-expression over 𝑎, we
join—by taking the variable-wise maximum—the ambient eﬀect of 𝑎, namely 𝑏, with the “global”
sensitivity eﬀect of the second branch, namely [𝑏 + 𝑥/𝑥 2 ]𝑥 2 —the ﬁrst branch is dismissed because
it has no ambient eﬀect. To compute the purported sensitivity eﬀect of the second branch, we take
its ambient eﬀect 𝑥 2 and replace every occurrence of the branch binder, also 𝑥 2 , with the eﬀect
𝑏 + 𝑥 of the right component of 𝑎, computed as the sum between its ambient eﬀect 𝑏 and its latent
eﬀect 𝑥. This yields an overall sensitivity of 𝑏 + 𝑥 = 𝑏 ⊔ [𝑏 + 𝑥/𝑥 2 ]𝑥 2 for the case-expression.
   Consider now Example 4.3. The guard 𝑥 ≤ 10 of the conditional expression has type unit⊕unit
with ambient eﬀect ∞𝑥. Since the branches are constant and have no ambient eﬀect, they do not
contribute to the sensitivity of the conditional. Jazz analysis then concludes that the sensitivity of
the conditional reduces to the ambient sensitivity of the guard, namely ∞𝑥, recovering soundness
(and precision).
    Jazz recovers soundness and precision for all four examples discussed in Section 4.2, as sum-
marized in Table 2. With this observation, we conclude our motivation for the design of the Jazz
sensitivity type system, based on latent contextual eﬀects.
  Example 4.5 (Prepayment of eﬀects). We remark that the use of latent contextual eﬀects does not
always yield better precision than eager (Fuzz-like) systems. Consider the following program:


                             let 𝑦1 , 𝑦2 = (let 𝑥 1, 𝑥 2 = 𝑝 in h𝑥 1 , 𝑥 2 i) in 𝑦1 + 𝑦2
Using latent eﬀects, the subexpression h𝑥 1, 𝑥 2 i has type R 𝑥 1 ⊗𝑥 2 R; ∅. Thus the subexpression
let 𝑥 1, 𝑥 2 = 𝑝 in h𝑥 1, 𝑥 2 i has type R 𝑝 ⊗𝑝 R; ∅, i.e. it represents a pure expression where the cost
of accessing either of its component is 𝑝. The ambient eﬀect of the whole expression is the sum
of the cost of accessing the pair (∅), plus the cost of accessing 𝑦1 (𝑝), plus the cost of accessing 𝑦2
(𝑝), yielding eﬀect 2𝑝. In Fuzz, the same program reports sensitivity 𝑝, yielding better precision
than Jazz. To recover Fuzz’s precision, Jazz allows eﬀects of products, sums, and functions to
be paid for eagerly, by combining contextual and linear eﬀects: parts of the sensitivity eﬀect of
each component of the product can contribute to the ambient eﬀect of the product. For instance,

4 At ﬁrst sight, one might think that 𝑎 is ∞-sensitive in 𝑏 because a change in 𝑏 may ﬂip the direction of the returned

injection. However, any change on the value of 𝑏 necessarily results in an inﬁnite variation since true and false are ∞ far
apart. Therefore, the induced variation on the value of 𝑎 is trivially bounded by ∞, scaled by 1, turning 𝑎 1-sensitive in 𝑏.


                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
18                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


                 Fuzz(*)                          DFuzz-like TS(**)                                  Jazz
      Reported          Bound               Reported          Bound                  Reported            Bound Qual-
      Sensitivity       Quality             Sensitivity       Quality                Sensitivity         ity

                                                   Example 4.1 (additive)
      8𝑥                loose               8𝑥                loose                  6𝑥                  tight
                                                 Example 4.2 (multiplicative)
      2𝑥 + 2𝑦           tight               4𝑥 + 2𝑦           loose (in 𝑥)           2𝑥 + 2𝑦             tight
                                                        Example 4.3
      ∞𝑥                tight               0𝑥                unsound                ∞𝑥                  tight
                                                        Example 4.4
      ∞𝑥 + 𝑏            loose (in 𝑥)        ∞𝑥 + 0𝑏           loose (in 𝑥)           𝑥 +𝑏                tight
                                                              unsound in 𝑏
                                                        Example 4.5
      𝑝                 tight               𝑝                 tight                  2𝑝                  loose (latent)
                                                                                     𝑝                   tight (prepay)
                       (*): sensitivities strictly greater than 0, programs transformed using scaling.
                             (**): sensitivities can be greater or equal to 0, no scaling allowed.
          Table 2. Comparison of sensitivity type-system: Fuzz and DFuzz-like type systems vs Jazz.



consider environment Γ = 𝑥 : R, 𝑦 : R. Jazz can produce the following type derivations for
expression 𝑒 = h𝑥, 𝑦i:
     Γ ⊢ 𝑒 : R 𝑥 ⊗ 𝑦 R; ∅          Γ ⊢ 𝑒 2 : R ⊗ 𝑦 R; 𝑥          Γ ⊢ 𝑒 3 : R 𝑥 ⊗ R; 𝑦          Γ ⊢ 𝑒 3 : R ⊗ R; 𝑥 + 𝑦
In the ﬁrst type derivation, the eﬀect of both components are latent, and thus the ambient eﬀect is
empty. In the second (resp. third) type derivation, the latent eﬀect of the type is the ambient eﬀect
of the right (resp. left) component, and the ambient eﬀect of the product is the ambient eﬀect of
the left (resp.right) component. In the last type derivation, the latent eﬀect of the type is empty,
everything is paid upfront, coinciding with Fuzz-like type systems. Going back to the example, if
we prepay the eﬀects of the subexpression h𝑥 1 , 𝑥 2 i then the product has type R ∅ ⊗∅ R; 𝑥 1 +𝑥 2 . Now
the subexpression let 𝑥 1, 𝑥 2 = 𝑝 in h𝑥 1, 𝑥 2 i has type R ∅ ⊗∅ R; 𝑝, because using multiplicative
products we only pay for 𝑝 proportional to the maximum sensitivity between 𝑥 1 and 𝑥 2 , i.e. (1⊔1)𝑝.
The ambient eﬀect of the whole expression is the sum of the cost of accessing the pair (𝑝), plus the
cost of accessing 𝑦1 and 𝑦2 (∅), yielding the tight ambient eﬀect 𝑝.
  As a ﬁnal remark, note that contrary to Fuzz, Jazz does not currently support recursive types;
such functions are required to be primitives, as illustrated in § 8.
  The following section presents the formal development of latent contextual eﬀects for sensitivity
typing, and includes a step-by-step type derivation for all four examples.

5    SAX: JAZZ’S SENSITIVITY TYPE SYSTEM, FORMALLY
In this section, we present a core sensitivity sublanguage of Jazz, called Sax, for which we develop
the sensitivity metatheory. In particular, we prove the type soundness property known as sensitiv-
ity metric preservation [49]. The core subset of Jazz that extends Sax with privacy is presented in
later sections.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       19




      𝑟∈R
      𝑏∈B
      𝑥 ∈ var
      𝑒 ∈ sexpr F 𝑟 | 𝑒 + 𝑒 | 𝑒 ∗ 𝑒 | 𝑒 ≤ 𝑒                                  real numbers
                        s
                | 𝑥 | 𝜆 (𝑥 : 𝜏). 𝑒 | 𝑒 𝑒                                     variables, functions, applications
                | tt                                                         unit
                | inl𝜏2 𝑒 | inr𝜏1 𝑒 | case 𝑒 of {𝑥 ⇒ 𝑒 } {𝑥 ⇒ 𝑒}             sums
                | (𝑒, 𝑒) | fst 𝑒 | snd 𝑒                                     add. products
                | h𝑒, 𝑒i | let 𝑥, 𝑥 = 𝑒 in 𝑒                                 mult. products
                | 𝑒 :: 𝜏                                                     ascription
      𝑠 ∈ 𝑠𝑒𝑛𝑠 , R∞ ≥0                                                       sensitivities
      Σ ∈ 𝑠𝑒𝑛𝑣 , var ⇀ 𝑠𝑒𝑛𝑠 F 𝑠𝑥 + . . . + 𝑠𝑥                                sensitivity environments
                                        Σ
      𝜏 ∈ type F R | unit | (𝑥 : 𝜏) −→𝜏
               | 𝜏 Σ ⊕ Σ 𝜏 | 𝜏 Σ &Σ 𝜏 | 𝜏 Σ ⊗ Σ 𝜏                            types
      Γ ∈ tenv , var ⇀ type F {𝑥 : 𝜏, . . . , 𝑥 : 𝜏 }                        type environments



                                                  Fig. 1. Sax: Syntax



5.1   Syntax and Type System
The Sax type system is technically a type-and-eﬀect system [36]. It supports real numbers, func-
tions, sums and products. As Sax only deals with ambient eﬀects, all metavariables and keywords
are typeset in green.

   Syntax. Figure 9 presents the syntax of Sax. Expressions 𝑒 are mostly standard and include: real
number 𝑟 , addition 𝑒 + 𝑒, multiplication 𝑒 ∗ 𝑒, comparison 𝑒 ≤ 𝑒, variable 𝑥, sensitivity lambda
 s
𝜆 (𝑥 : 𝜏). 𝑒, application 𝑒 𝑒, unit value tt, sum constructors inl𝜏2 𝑒 and inr𝜏1 𝑒, and the sum
destructor case 𝑒 of {𝑥 ⇒ 𝑒} {𝑥 ⇒ 𝑒}.
   Sax also supports two linear products types: additive and multiplicative. With additive products,
the sensitivity of a pair may be approximated as the max of the sensitivities of each side; this
sensitivity is paid for every projection. With multiplicative products, the sensitivity of a pair may
be approximated as the sum of the sensitivities of each side; this sensitivity is paid for every tuple
pattern match, scaled by the sensitivities of pattern variables in the body. We write additive product
constructions (𝑒, 𝑒) and destructions fst 𝑒 and snd 𝑒, and multiplicative product constructions
h𝑒, 𝑒i and destructions let 𝑥, 𝑥 = 𝑒 in 𝑒.
   Finally, an expression 𝑒 can be an ascription 𝑒 :: 𝜏, or a derived expressions such as a boolean
𝑏, a conditional if 𝑒 then 𝑒 else 𝑒, or a let expression let 𝑥 = 𝑒 in 𝑒. Booleans are encoded as
true , inl tt, false , inr tt, and B as unit∅ ⊕∅ unit, conditionals as if 𝑒 1 then 𝑒 2 else 𝑒 3 ,
                                                                                 s
case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 }, and let expressions as let 𝑥 = 𝑒 1 in 𝑒 2 , (𝜆 (𝑥 : 𝜏1 ).𝑒 2 ) 𝑒 1 .
   A sensitivity 𝑠 is either a non-negative real number or the symbol ∞, which represents an un-
bounded sensitivity; we notate this set R∞ ≥0 , R ≥0 ⊎{∞}. A sensitivity environment Σ is a mapping
from variables to their sensitivities. For convenience, we write sensitivity environments as ﬁrst-
order polynomials, e.g. Σ = 1𝑥 + 2𝑦 corresponds to an environment Σ such that Σ(𝑥) = 1 and
Σ(𝑦) = 2. A type 𝜏 is either the real number type R, the boolean type B, the unit type unit, a
                          Σ
                      − 𝜏, a sum type 𝜏 Σ ⊕ Σ 𝜏, an additive product type 𝜏 Σ &Σ 𝜏, or a multiplica-
function type (𝑥 : 𝜏) →
                    Σ Σ
tive product type 𝜏 ⊗ 𝜏. The sensitivity environment annotation Σ is called the latent contextual

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
20                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


sensitivity eﬀect (also called latent eﬀect when clear from the context) and represents a delayed
eﬀect that emerges when a term of said type is eliminated. The latent eﬀect Σ of a function of type
         Σ
        − 𝜏 corresponds to the eﬀects of applying the function, i.e., a static approximation of the
(𝑥 : 𝜏) →
sensitivity of each variable used in its body. The sensitivity environment Σ1 (resp. Σ2 ) in 𝜏1 Σ1 ⊕ Σ2 𝜏2
corresponds to the latent eﬀect of the injected value using inl (resp. inr). And similarly, Σ1 and
Σ2 in 𝜏1 Σ1 &Σ2 𝜏2 or 𝜏1 Σ1 ⊗ Σ2 𝜏2 correspond to the latent eﬀect of accessing the ﬁrst and second
components of the pair, respectively. Finally, a type environment Γ is, as usual, a mapping from
variables to types.
   Type system. The Sax type system is presented in Figure 2. The judgment Γ ⊢ 𝑒 : 𝜏 ; Σ says that
the term 𝑒 has type 𝜏 and ambient sensitivity eﬀect Σ (or ambient eﬀect when clear from the con-
text) under type environment Γ. The ambient eﬀect Σ represents an upper bound (conservative
approximation) of the real sensitivity of 𝑒 after executing the program. The use of a sensitivity
environment Σ is diﬀerent from Duet, where sensitivities are tracked in Γ and presented as a nec-
essary condition to type check the expression. In other words, in SaxΣ is used to infer sensitivities,
whereas in Duet Γ is used to check sensitivities.
- Rules rlit and unit are standard and report no eﬀect, as no variable is accessed. These two rules
  present no novelty with respect to Duet.
- Rule var is mostly standard; it reports an ambient eﬀect 1𝑥.
  For example,
                                                   var
                                                    (𝑥 : R)(𝑥) = R
                                                   𝑥 :R⊢𝑥 :R;𝑥


- Rule plus computes the resulting ambient eﬀect as the addition of the ambient eﬀects of both
  subterms. To add sensitivity environments we use the + operator, which is simply deﬁned as the
  addition of polynomials, e.g. (1𝑥 + 2𝑦) + (3𝑥) = 4𝑥 + 2𝑦.
  For example, in the following type derivation
                                      plus
                                     𝑥 :R ⊢𝑥 :R;𝑥               𝑥 :R⊢𝑥 :R;𝑥
                                               𝑥 : R ⊢ 𝑥 + 𝑥 : R ; 2𝑥
  we write 2𝑥 instead of 𝑥 + 𝑥.
- Rules times and leq are similar to plus, but the resulting sensitivity eﬀect is scaled by inﬁnity
  because (1) the sensitivity of a multiplication when neither side is a constant is unbounded, and
  (2) the distance between distinct boolean values is deemed inﬁnite, as explained in Section 4.2.
  Scaling a sensitivity environment Σ by sensitivity 𝑠, written 𝑠Σ, produces a new sensitivity en-
  vironment in which each sensitivity in Σ is multiplied by 𝑠. For multiplication we assume that
  0𝑠 = 𝑠0 = 0 for all 𝑠 ∈ R∞≥0 and we deem ∞𝑠 = 𝑠∞ = ∞ for 𝑠 ≠ 0.
  Rules l-scale and r-scale address the overapproximation yielded by rule times when one of
  the factors is a real number. For instance, for program 0.5 ∗ 𝑥 rule l-scale reports a (precise)
  sensitivity of 0.5𝑥, whereas rules times would report ∞𝑥.
- Rule lam typechecks sensitivity functions and is novel with respect to Duet. The type of the
  function is annotated with a latent eﬀect Σ, computed as a subset of the eﬀect of its body. On
  a fully-latent discipline, the whole body eﬀect is left as latent and the ambient eﬀect Σ ′ of the
  function is empty. On the other hand, full eagerness of eﬀects, as in Duet, is achieved when the
  latent eﬀect Σ is empty and the full eﬀect of the body is paid upon construction.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                            21




                                               var                             plus
               rlit                             Γ (𝑥) = 𝜏                      Γ ⊢ 𝑒 1 : R ; Σ1           Γ ⊢ 𝑒 2 : R ; Σ2
               Γ ⊢𝑟 :R;∅                      Γ ⊢𝑥 :𝜏 ;𝑥                                Γ ⊢ 𝑒 1 + 𝑒 2 : R ; Σ1 + Σ2

   times                                                                                l-scale                       r-scale
   Γ ⊢ 𝑒 1 : R ; Σ1        Γ ⊢ 𝑒 2 : R ; Σ2          𝑒1 ≠ 𝑟         𝑒2 ≠ 𝑟                Γ ⊢𝑒 :R;Σ                     Γ ⊢𝑒 :R;Σ
                   Γ ⊢ 𝑒 1 ∗ 𝑒 2 : R ; ∞(Σ1 + Σ2 )                                    Γ ⊢ 𝑟 ∗ 𝑒 : R ; 𝑟Σ              Γ ⊢ 𝑒 ∗ 𝑟 : R ; 𝑟Σ

               leq                                                            lam
               Γ ⊢ 𝑒 1 : R ; Σ1         Γ ⊢ 𝑒 2 : R ; Σ2                                Γ, 𝑥 : 𝜏1 ⊢ 𝑒 : 𝜏2 ; Σ + Σ′
                                                                                    s                           Σ
                      Γ ⊢ 𝑒 1 ≤𝑒 2 : B ; ∞(Σ1 + Σ2 )                                                        → 𝜏2 ; Σ ′
                                                                             Γ ⊢ 𝜆 (𝑥 : 𝜏1 ). 𝑒 : (𝑥 : 𝜏1 ) −

                  app
                                      Σ                                                            unit
                  Γ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ) −
                                      → 𝜏2 ; Σ1           Γ ⊢ 𝑒 2 : 𝜏1 ; Σ2
                          Γ ⊢ 𝑒 1 𝑒 2 : [Σ2 /𝑥]𝜏2 ; Σ1 + [Σ2 /𝑥]Σ                                 Γ ⊢ tt : unit ; ∅

                        inl                                                     inr
                              Γ ⊢ 𝑒 : 𝜏1 ; Σ + Σ ′                                       Γ ⊢ 𝑒 : 𝜏2 ; Σ + Σ ′
                       Γ ⊢ inl𝜏2 𝑒 : 𝜏1 Σ ⊕ ∅ 𝜏2 ; Σ′                          Γ ⊢ inr𝜏1 𝑒 : 𝜏1 ∅ ⊕ Σ 𝜏2 ; Σ′

          case
             Γ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1           Γ , 𝑥 : 𝜏11 ⊢ 𝑒 2 : 𝜏2 ; Σ2             Γ , 𝑦 : 𝜏12 ⊢ 𝑒 3 : 𝜏3 ; Σ3
                         Γ ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } :
                            [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ; Σ1 ⊔ ([Σ1 + Σ11 /𝑥]Σ2 ⊔ ([Σ1 + Σ12 /𝑦]Σ3 ))

   pair                                                               proj1                                 proj2
   Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 + Σ1′        Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 + Σ2′             Γ ⊢ 𝑒 : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ              Γ ⊢ 𝑒 : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ
        Γ ⊢ (𝑒 1 , 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ1′ ⊔ Σ2′                   Γ ⊢ fst 𝑒 : 𝜏1 ; Σ + Σ1               Γ ⊢ snd 𝑒 : 𝜏2 ; Σ + Σ2

                                      tup
                                      Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 + Σ1′            Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 + Σ2′
                                              Γ ⊢ h𝑒 1, 𝑒 2 i : 𝜏1 Σ1 ⊗ Σ2 𝜏2 ; Σ1′ + Σ2′

          untup
              Γ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊗ Σ12 𝜏12 ; Σ1                Γ , 𝑥 1 : 𝜏11, 𝑥 2 : 𝜏12 ⊢ 𝑒 2 : 𝜏2 ; 𝑠 1𝑥 1 + 𝑠 2 𝑥 2 + Σ2
          Γ ⊢ let 𝑥 1 , 𝑥 2 = 𝑒 1 in 𝑒 2 : [Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ; (𝑠 1 ⊔ 𝑠 2 )Σ1 + 𝑠 1 Σ11 + 𝑠 2 Σ12 + Σ2

                                                     ascr
                                                     Γ ⊢𝑒 :𝜏 ;Σ              𝜏 <: 𝜏 ′
                                                        Γ ⊢ (𝑒 :: 𝜏 ′ ) : 𝜏 ′ ; Σ




                                                     Fig. 2. Sax: Type system


  Since the splitting of Σ + Σ ′ is non-deterministic, a lambda expression can be given many types,
  ranging from fully-latent to fully-eager disciplines. We show this behavior later when explaining

                                    ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
22                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                                                                                          [Σ/𝑥]𝜏
                                            [Σ/𝑥]R = R
                                            [Σ/𝑥]B = B
                                         [Σ/𝑥]unit = unit
                                                Σ′                      [Σ/𝑥]Σ′
                               [Σ/𝑥]((𝑦 : 𝜏1 ) −−→ 𝜏2 ) = (𝑦 : [Σ/𝑥]𝜏1 ) −−−−−−→ [Σ/𝑥]𝜏2
                                 [Σ/𝑥](𝜏1 Σ1 ⊕ Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 ⊕ [Σ/𝑥]Σ2 [Σ/𝑥]𝜏2
                                 [Σ/𝑥](𝜏1 Σ1 &Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 &[Σ/𝑥]Σ2 [Σ/𝑥]𝜏2
                                 [Σ/𝑥](𝜏1 Σ1 ⊗ Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 ⊗ [Σ/𝑥]Σ2 [Σ/𝑥]𝜏2
                                                                                                          [Σ/𝑥]Σ
                                                  [Σ/𝑥]∅ = ∅
                                            [Σ/𝑥](Σ′ + 𝑠𝑥) = [Σ/𝑥]Σ′ + 𝑠Σ
                                            [Σ/𝑥](Σ′ + 𝑠𝑦) = [Σ/𝑥]Σ′ + 𝑠𝑦



                    Fig. 3. Sax: Auxiliary definitions of the static semantics (selected rules)


     rules pair and tup. The implementation addresses this issue through the use of additional type
     annotations. Without loss of generality, in this paper, we assume the fully-latent derivation for
     all lambdas unless stated otherwise. The same applies to other language constructs that exhibit
     this kind of non-deterministic prepayment of latent eﬀects.
                                      s
     For example, consider program 𝜆 (𝑥 : R). 𝑥 + 𝑥 and its type derivation:
                                      lam
                                                    𝑥 : R ⊢ 𝑥 + 𝑥 : R ; 2𝑥
                                            s                            2𝑥
                                     ∅ ⊢ 𝜆 (𝑥 : R). 𝑥 + 𝑥 : (𝑥 : R) −−→ R ; ∅
  The ambient eﬀect of the program is empty (values are pure) but its latent eﬀect is 2𝑥, the ambient
  eﬀect of its body.
- Rule app deals with function application. Unlike Duet, as variable 𝑥 may be free in 𝜏2 (e.g. 𝜏2
  can be a function type whose latent eﬀect includes 𝑥), the resulting type replaces 𝑥 with the
  ambient eﬀect Σ2 of its argument using the sensitivity environment substitution operator deﬁned
                                                               ∅             2𝑥+𝑦+𝑧
     in Figure 3. For instance, consider type (𝑥 : R) −              → R. After application, if Σ2 = 3𝑦,
                                                      → (𝑧 : R) −−−−−−
                                                            2𝑥+𝑦+𝑧                    6𝑦+𝑦+𝑧                7𝑦+𝑦
  the resulting type would be [3𝑦/𝑥]((𝑧 : R) −−−−−−   → R) = ((𝑧 : R) −−−−−−→ R) = ((𝑧 : R) −−−−→ R).
  The ambient eﬀect of an application is computed as the ambient eﬀect of the function Σ1 , plus its
  latent eﬀect; but as 𝑥 is free we substitute it by Σ2 , e.g. if Σ = Σ ′ + 𝑠𝑥, then [Σ2/𝑥](Σ1 + Σ ′ + 𝑠𝑥) =
  Σ1 + (Σ ′ + 𝑠Σ2 ). This is diﬀerent from Duet as, where the latent eﬀect of the function Σ is paid
  when the function is created.
                                                  s
  For instance, consider the open program (𝜆 (𝑥 : R). 2 ∗ 𝑥 + 𝑦) (3 ∗ 𝑦) and the following type
  derivation:
                 app
                           s                                   2𝑥+𝑦
                𝑦 : R ⊢ 𝜆 (𝑥 : R). 2 ∗ 𝑥 + 𝑦 : (𝑥 : R) −−−−→ R ; ∅                𝑦 : R ⊢ 3 ∗ 𝑦 : R; 3𝑦
                                                s
                                   𝑦 : R ⊢ (𝜆 (𝑥 : R). 2 ∗ 𝑥 + 𝑦) (3 ∗ 𝑦) : R ; 7𝑦
  The resulting ambient eﬀect cannot depend on 𝑥 (otherwise it would be free), therefore it is
  computed as the substitution of 𝑥 by the ambient eﬀect of the argument [3𝑦/𝑥](2𝑥 + 𝑦) = 7𝑦.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       23


- Contrary to previous work [34, 49] , and in particular Duet, Rule inl does not necessarily
  report the eﬀect of its body. The payment of eﬀects for the subexpression (or a subset of it)
  can be delayed, and eventually payed only if the sum is accessed or used. The term is tagged
  with type 𝜏2 to aid type inference. The resulting type is just a sum type where the latent eﬀect
  of the left type is Σ, a subset of the ambient eﬀect of its subterm, and the latent eﬀect of the
  right type is empty (as it will never be used/accessed so we choose the tighter ambient eﬀect).
  Non-determinism is addressed similarly to rule lam. Rule inr is deﬁned similarly.
  For instance, consider the type derivations of expressions 𝑒 4 = inl (𝑥 ∗ 𝑥) and 𝑒 5 = inr (𝑥 ∗ 𝑥)
  of Section 4.3:
            inl                                                    inr
                   𝑥 : R ⊢ (𝑥 ∗ 𝑥) : R ; ∞𝑥                               𝑥 : R ⊢ 𝑥 ∗ 𝑥 : R ; ∞𝑥
                                     ∞𝑥    ∅
                      R
            ∅ ⊢ inl (𝑥 ∗ 𝑥) : R           ⊕ R;∅                   ∅ ⊢ inrR (𝑥 ∗ 𝑥) : R ∅ ⊕∞𝑥 R ; ∅
  For expression 𝑒 4 , the latent eﬀect of the left type is ∞𝑥, and of the right type is empty (it is
  the tighter upper bound as the right component cannot be accessed). An analogous argument is
  used for 𝑒 5 .
- Rule case is more involved. The resulting type of the case is just the least upper bound (join) of
  the branch types 𝜏2 and 𝜏3 . The join operator is deﬁned in Figure 4. Note that similarly to rule
  app, 𝜏2 and 𝜏3 may have 𝑥 and 𝑦 as free variables respectively, thus we replace those variables
  with the ambient eﬀects of using the sum term 𝑒 1 : Σ1 +Σ11 and Σ1 +Σ12 respectively. The resulting
  ambient eﬀect is computed as follows: we join the cost of reducing 𝑒 1 : Σ1 , with the join of the
  cost of taking each branch. This is diﬀerent from Duet, where Σ1 is added to the cost of taking
  each branch, leading to a looser bound. Similarly to types 𝜏2 and 𝜏3 , ambient eﬀects Σ2 and Σ3
  may have 𝑥 and 𝑦 free, so we substitute them away from the eﬀects. Note that we use the join
  between Σ1 and the cost of the branches (instead of the addition for instance), otherwise the
  result would be less precise when the branches use 𝑥 or 𝑦.
  For instance, the type derivation of Example 4.4 is described below:
                  case
                  Γ ⊢ 𝑒 : R ∞𝑥 ⊕𝑥 R; 𝑏            Γ, 𝑥 1 : R ⊢ 0 : R; ∅      Γ, 𝑥 2 : R ⊢ 𝑥 2 : R; 𝑥 2
                  Γ ⊢ case 𝑒 of {𝑥 1 ⇒ 0}{𝑥 2 ⇒ 𝑥 2 } : R; 𝑏 ⊔ (0𝑏 + 0(∞𝑥)) ⊔ (1𝑏 + 1(𝑥))
  where Γ = 𝑏 : B, 𝑥 : R, and 𝑒 = if 𝑏 then {inl (𝑥 ∗ 𝑥)} else {inr 𝑥 }. As 0∞ = 0, the resulting
  ambient eﬀect is 𝑏 ⊔ (0𝑏 + 0(∞𝑥)) ⊔ (1𝑏 + 1(𝑥)) = 𝑏 ⊔ (0𝑏 + 0𝑥) ⊔ (𝑏 + 𝑥) = 𝑏 + 𝑥, where previous
  work reported ∞ on 𝑥.
  Notice that if we change the program to case 𝑒 of {𝑥 1 ⇒ 0}{𝑥 2 ⇒ 1}, then the resulting
  ambient eﬀect is 𝑏 ⊔ (0𝑏 + 0(∞𝑥)) ⊔ (0𝑏 + 0(𝑥)) = 𝑏, i.e. the payment is not zero but 𝑏, the cost of
  reducing expression 𝑒 to a value.
  Example 4.3 is desugared and type checked as follows:
     case
               Γ ⊢ 𝑥 ≤ 10 : B; ∞𝑥           Γ, 𝑥 1 : R ⊢ true : R; ∅         Γ, 𝑥 2 : R ⊢ false : R; ∅
     Γ ⊢ case 𝑥 ≤ 10 of {𝑥 1 ⇒ true}{𝑥 2 ⇒ false} : B; ∞𝑥 ⊔ (0(∞𝑥) + 0(∅)) ⊔ (0(∞𝑥) + 0(∅))
  where B = unit ∅ ⊕∅ unit. As ∞𝑥 ⊔ (0(∞𝑥) + 0(∅)) ⊔ (0(∞𝑥) + 0(∅)) = ∞𝑥 ⊔ 0𝑥 = ∞𝑥, the
  expression is ∞-sensitive in 𝑥.
- Rules pair and tup are novel and non-deterministic: the ambient eﬀects are computed using
  subsets of the ambient eﬀect of each component. If the ambient eﬀects of the left component is
  Σ1 + Σ1′ and of the right component is Σ2 + Σ2′ (for some Σ1, Σ1′ , Σ2, Σ2′ ), then the latent eﬀects
  of using the left component is Σ1 , and for the right component is Σ2 . For additive products, the

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
24                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                                                                                                 𝜏 ⊔𝜏
                                                      R⊔R=R
                                                      B⊔B=B
                                                unit ⊔ unit = unit
                                    Σ                  Σ′                        Σ⊔Σ′
                                    → 𝜏2 ⊔ (𝑦 : 𝜏1′ ) −−→ 𝜏2′ = (𝑦 : 𝜏1 ⊓ 𝜏1′ ) −−−−→ (𝜏2 ⊔ 𝜏2′ )
                          (𝑦 : 𝜏1 ) −
                                                  ′     ′                         ′        ′
                            𝜏1 ⊕ Σ2 𝜏2 ⊔ (𝜏1′ Σ1 ⊕ Σ2 𝜏2′ ) = (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 ⊕ Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ )
                                Σ 1
                                                  ′     ′                         ′        ′
                            𝜏1 Σ1 &Σ2 𝜏2 ⊔ (𝜏1′ Σ1 &Σ2 𝜏2′ ) = (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 &Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ )
                                                  ′     ′                         ′        ′
                            𝜏1 Σ1 ⊗ Σ2 𝜏2 ⊔ (𝜏1′ Σ1 ⊗ Σ2 𝜏2′ ) = (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 ⊗ Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ )

                                                                                                                 𝜏 ⊓𝜏
                                                      R⊓R=R
                                                      B⊓B=B
                                                unit ⊓ unit = unit
                                    Σ                  Σ′                        Σ⊓Σ′
                                    → 𝜏2 ⊓ (𝑦 : 𝜏1′ ) −−→ 𝜏2′ = (𝑦 : 𝜏1 ⊔ 𝜏1′ ) −−−−→ (𝜏2 ⊓ 𝜏2′ )
                          (𝑦 : 𝜏1 ) −
                                                   ′    ′                         ′        ′
                            𝜏1 Σ1 ⊕ Σ2 𝜏2 ⊓ (𝜏1′ Σ1 ⊕ Σ2 𝜏2′ ) = (𝜏1 ⊓ 𝜏1′ ) Σ1 ⊓Σ1 ⊕ Σ2 ⊓Σ2 (𝜏2 ⊓ 𝜏2′ )
                                                  ′     ′                       ⊓Σ′      ⊓Σ′
                            𝜏1 1 & 2 𝜏2 ⊓ (𝜏1 1 & 2 𝜏2 ) = (𝜏1 ⊓ 𝜏1 ) 1 1 & 2 2 (𝜏2 ⊓ 𝜏2′ )
                                Σ    Σ         ′ Σ     Σ   ′             ′   Σ        Σ
                                                   ′    ′                       ⊓Σ′ Σ ⊓Σ′
                            𝜏1 1 ⊗ 2 𝜏2 ⊓ (𝜏1 1 ⊗ 2 𝜏2 ) = (𝜏1 ⊓ 𝜏1 ) 1 1 ⊗ 2 2 (𝜏2 ⊓ 𝜏2′ )
                                Σ    Σ         ′ Σ     Σ   ′             ′   Σ


                                                                                                                Σ⊔Σ
                                          ∅⊔∅=∅
                            (Σ + 𝑠𝑥) ⊔ (Σ′ + 𝑠 ′𝑥) = (Σ ⊔ Σ′ ) + (𝑠 ⊔ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊔ Σ′ )
                                   Σ ⊔ (Σ′ + 𝑠𝑥) = (Σ ⊔ Σ′ ) + 𝑠𝑥               (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                                   (Σ + 𝑠𝑥) ⊔ Σ′ = (Σ ⊔ Σ′ ) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ′ ))
                                                                                                                Σ⊓Σ
                                          ∅⊓∅=∅
                            (Σ + 𝑠𝑥) ⊓ (Σ′ + 𝑠 ′𝑥) = (Σ ⊓ Σ′ ) + (𝑠 ⊓ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊓ Σ′ )
                                   Σ ⊓ (Σ′ + 𝑠𝑥) = (Σ ⊓ Σ′ )                    (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                                   (Σ + 𝑠𝑥) ⊓ Σ′ = (Σ ⊓ Σ′ )                   (𝑥 ∉ 𝑑𝑜𝑚(Σ′ ))



                        Fig. 4. Sax: Join and Meet of types and sensitivity environments



     ambient eﬀect is the maximum between Σ1′ and Σ2′ , and for multiplicative products, the sum
     between Σ1′ and Σ2′ .
     For instance, let us consider examples 𝑒 1 = (2 ∗ 𝑥 + 𝑦, 0), 𝑒 2 = (0, 2 ∗ 𝑥 + 𝑦), and 𝑒 3 = (𝑥, 𝑥 + 𝑦) from
     Section 4.3. We present next “lazy” type derivations for each of the examples:
      pair                                                           pair
      Γ ⊢ 2 ∗ 𝑥 + 𝑦 : R ; 2𝑥 + 𝑦           Γ ⊢0:R;∅                  Γ ⊢0:R;∅                Γ ⊢ 2 ∗ 𝑥 + 𝑦 : R ; 2𝑥 + 𝑦
                                            ∅
           Γ ⊢ (2 ∗ 𝑥 + 𝑦, 0) : R   2𝑥+𝑦
                                           & R;∅                           Γ ⊢ (0, 2 ∗ 𝑥 + 𝑦) : R ∅ &2𝑥+𝑦 R ; ∅
                                        pair
                                        Γ ⊢𝑥 :R;𝑥             Γ ⊢ 𝑥 +𝑦 : R ; 𝑥 +𝑦
                                           Γ ⊢ (𝑥, 2 ∗ 𝑥 + 𝑦) : R 𝑥 &𝑥+𝑦 R ; ∅

  where Γ = 𝑥 : R, 𝑦 : R.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                        25


  Now, let us consider examples (2𝑥, 𝑥) and h2𝑥, 𝑥i. Here are six possible type derivations of paying
  eagerly for eﬀects:
         pair                                                       tup
         Γ ⊢ 2𝑥 : R ; ∅ + 2𝑥             Γ ⊢ 𝑥 :R;𝑥 +∅              Γ ⊢ 2𝑥 : R ; ∅ + 2𝑥           Γ ⊢ 𝑥 :R;𝑥 +∅
                                         𝑥
                      Γ ⊢ (2𝑥, 𝑥) : R & R ; 2𝑥                                Γ ⊢ h2𝑥, 𝑥i : R ⊗𝑥 R ; 2𝑥
       pair                                                      tup
      Γ ⊢ 2𝑥 : R ; 𝑥 + 𝑥          Γ ⊢ 𝑥 :R;𝑥 +∅                  Γ ⊢ 2𝑥 : R ; 𝑥 + 𝑥          Γ ⊢ 𝑥 :R;𝑥+∅
                                 𝑥   𝑥
                Γ ⊢ (2𝑥, 𝑥) : R & R ; 𝑥                                    Γ ⊢ h2𝑥, 𝑥i : R ⊗𝑥 R ; 𝑥
                                                                                             𝑥


     pair                                                        tup
     Γ ⊢ 2𝑥 : R ; ∅ + 2𝑥          Γ ⊢ 𝑥 : R ; ∅+𝑥                Γ ⊢ 2𝑥 : R ; ∅ + 2𝑥             Γ ⊢ 𝑥 : R ; ∅+𝑥
                Γ ⊢ (2𝑥, 𝑥) : R & R ; 2𝑥                                   Γ ⊢ h2𝑥, 𝑥i : R ⊗ R ; 3𝑥
  Note that the diﬀerence between the two form of products is only present when eﬀects are paid
  eagerly for both components.
- Rules proj1 and proj2 type check the deconstruction of an additive product. The ambient eﬀect is
  computed as the cost of reducing the product (Σ), plus the cost of accessing either the ﬁrst or the
  second component correspondingly (Σ1 or Σ2 ). This diﬀers from Duet where, and conservatively,
  the cost of accessing both components are paid when the pair is created. In Sax we only paid for
  the component we are accessing.
  For instance, let us consider the ﬁrst projections of last examples:
              proj1                                                proj1
            Γ ⊢ (2 ∗ 𝑥 + 𝑦, 0) : R 2𝑥+𝑦 &∅ R ; ∅                  Γ ⊢ (0, 2 ∗ 𝑥 + 𝑦) : R ∅ &2𝑥+𝑦 R ; ∅
              Γ ⊢ fst (2 ∗ 𝑥 + 𝑦, 0) : R ; 2𝑥 + 𝑦                      Γ ⊢ fst (0, 2 ∗ 𝑥 + 𝑦) : R ; ∅

                                         proj1
                                         Γ ⊢ (𝑥, 2 ∗ 𝑥 + 𝑦) : R 𝑥 &𝑥+𝑦 R ; ∅
                                             Γ ⊢ fst (𝑥, 2 ∗ 𝑥 + 𝑦) : R ; 𝑥
  Contrary to previous work, the ambient eﬀects of all three projections are diﬀerent, as they
  capture precisely the variables accessed on the corresponding component.
- Rule untup typechecks the deconstruction of a multiplicative product, and is a little more in-
  volved. To compute the ambient eﬀect we start by paying for Σ2 , the ambient eﬀect of subex-
  pression 𝑒 2 . We also want to pay Σ11 and Σ12 , the cost of accessing the left and the right com-
  ponents respectively, proportionally to the sensitivity of the left and right variables 𝑥 1 and 𝑥 2
  in 𝑒 2 , i.e. 𝑠 1 Σ11 + 𝑠 2 Σ12 . But we also have to pay for Σ1 , the ambient eﬀect of 𝑒 1 . We could
  pay (𝑠 1 + 𝑠 2 )Σ1 , but that would be an unnecessary over-approximation. For instance, program
  let 𝑥 1, 𝑥 2 = 𝑝 in 𝑥 1 + 𝑥 2 would pay twice for 𝑝 (the ambient eﬀect of 𝑒 1 ), even though the
  whole pair is used only once. Instead we want to pay proportional to the the maximum sen-
  sitivity between 𝑥 1 and 𝑥 2 , i.e. (𝑠 1 ⊔ 𝑠 2 )Σ1 . Finally, the ambient eﬀect of the let expression is
  (𝑠 1 ⊔ 𝑠 2 )Σ1 + 𝑠 1 Σ11 + 𝑠 2 Σ12 + Σ2 .
  For instance, let us consider the typing derivation of Example 4.2:
               untup
               Γ ⊢ (2 ∗ 𝑥, 𝑦) : R 2𝑥 ⊗ 𝑦 R ; ∅         Γ, 𝑥 1 : R, 𝑥 2 : R ⊢ 𝑥 1 + 2 ∗ 𝑥 2 : R ; 𝑥 1 + 2𝑥 2
                          Γ ⊢ let 𝑥 1, 𝑥 2 = (2 ∗ 𝑥,𝑦) in 𝑥 1 + 2 ∗ 𝑥 2 : R ; 1(2𝑥) + 2(𝑦)
  where Γ = 𝑥 : R, 𝑦 : R. The resulting ambient eﬀect is 1(2𝑥) + 2(𝑦) = 2𝑥 + 2𝑦.

                                 ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
26                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                              if
                 blit                         Γ ⊢ 𝑒 1 : B ; Σ1      Γ ⊢ 𝑒 2 : 𝜏 ; Σ2        Γ ⊢ 𝑒 3 : 𝜏 ; Σ3
                 Γ ⊢𝑏:B;∅                         Γ⊢ if 𝑒 1 then 𝑒 2 else 𝑒 3 : 𝜏 ; Σ1 ⊔ (Σ2 ⊔ Σ3 )

                                     let
                                      Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1     Γ, 𝑥 : 𝜏1 ⊢ 𝑒 2 : 𝜏2 ; Σ2
                                    Γ ⊢ let 𝑥 = 𝑒 1 in 𝑒 2 : [Σ1 /𝑥]𝜏2 ; [Σ1 /𝑥]Σ2




                                            Fig. 5. Sax: Derived type rules


     Now consider Γ = 𝑝 : R ∅ ⊗∅ R, and the following typing derivation:
                untup
                   Γ ⊢ 𝑝 : R ∅ ⊗∅ R ; 𝑝           Γ, 𝑥 1 : R, 𝑥 2 : R ⊢ h𝑥 1, 𝑥 2 i : R Σ1 ⊗ Σ2 R ; Σ3
                                                                            ′   ′
                               Γ ⊢ let 𝑥 1, 𝑥 2 = 𝑝 in h𝑥 1 , 𝑥 2 i : R Σ1 ⊗ Σ2 R ; Σ3′
                                    Γ,𝑦1 : R, 𝑦2 : R ⊢ 𝑦1 + 𝑦2 : R ; 𝑦1 + 𝑦2
                Γ ⊢ let 𝑦1 , 𝑦2 = (let 𝑥 1, 𝑥 2 = 𝑝 in h𝑥 1, 𝑥 2 i) in 𝑦1 + 𝑦2 : R ; Σ3′ + Σ1′ + Σ2′

  We can typecheck subexpression let 𝑥 1, 𝑥 2 = 𝑝 in (𝑥 1, 𝑥 2 ) in diﬀerent ways. If we do not prepay
  eﬀects, then Σ1 = 𝑥 1, Σ2 = 𝑥 2 , and Σ3 = ∅. Thus Σ1′ = Σ2′ = 𝑝, and Σ3′ = ∅. Finally the ambient
  eﬀect of the program is 2𝑝.
  If we prepay the accesses of 𝑥 1 and 𝑥 2 , then Σ1 = ∅, Σ2 = ∅, and Σ2 = 𝑥 1 + 𝑥 2 . Thus Σ1′ = Σ2′ = ∅,
  and Σ3′ = (1 ⊔ 1)𝑝 = 𝑝. Finally the ambient eﬀect of the program is 𝑝.
- Rules for booleans, conditionals and let expressions are derived rules from sums, case, and ap-
  plication rules respectively, and can be found in Figure 5.
- Finally, Rule ascr is the only rule that supports the use of subtyping, and takes the role of check-
  ing whether the subexpression is subtype of a given type.
   Subtyping for types and sensitivity environments is presented in Figure 6, and is mostly standard.
We only allow subtyping for the sensitivity parts of types. A sensitivity environment is subtype
of another if their sensitivities are less than or equal than the other for each variable. For instance,
          𝑥+𝑦                  𝑥+2𝑦+3𝑧
(𝑥 : R) −−−→ R <: (𝑥 : R) −−−−−−→ R because 𝑥 + 𝑦 <: 𝑥 + 2𝑦 + 3𝑧 (𝑥 ≤ 𝑥, 𝑦 ≤ 2𝑦, and 0𝑧 ≤ 3𝑧).

5.2     Type Safety
Type safety is established relative to the runtime semantics of Sax. We adopt a big-step semantics
with explicit substitutions. Concretely, we use 𝛾 ⊢ 𝑒 ⇓ 𝑣 to represent that conﬁguration 𝛾 ⊢ 𝑒
—formed by expression 𝑒 and value environment 𝛾 mapping variables to values— reduces to value
𝑣 after some number of steps. Reducion rules are rather standard and can be found in Appendix B,
Figure 27.
   To establish Sax type safety, we employ simple unary logical relations, called the type safety
logical relations, that characterize well-typed, non-stuck execution. This relation is well deﬁned
because it is deﬁned by induction over the structure of types. The type safety result itself is derived
as a corollary of the fundamental property of the type safety logical relations.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                            27




                                                                                                                  Σ <: Σ
                                                       △
                                          Σ <: Σ′    ⇐⇒ ∀𝑥. Σ(𝑥) ≤ Σ′ (𝑥)
                                                                                                                  𝜏 <: 𝜏
                          base                                lam
                          𝜏 ∈ {R, unit}                       𝜏1′ <: 𝜏1                Σ <: Σ′        𝜏2 <: 𝜏2′
                                                                              Σ                           Σ′
                              𝜏 <: 𝜏                                    → 𝜏2 <: (𝑥 : 𝜏1′ ) −−→ 𝜏2′
                                                              (𝑥 : 𝜏1 ) −

                                  sum
                                  𝜏1 <: 𝜏1′       Σ1 <: Σ1′       𝜏2 <: 𝜏2′                   Σ2 <: Σ2′
                                                                    ′ Σ′1         Σ′2
                                              𝜏1 Σ1 ⊕ Σ2 𝜏2 <: 𝜏1             ⊕         𝜏2′

                                  pair
                                  𝜏1 <: 𝜏1′       Σ1 <: Σ1′       𝜏2 <: 𝜏2′                   Σ2 <: Σ2′
                                              𝜏1 Σ1 &Σ2 𝜏2 <: 𝜏1    ′ Σ′1     &   Σ′2   𝜏2′

                                  tup
                                  𝜏1 <: 𝜏1′       Σ1 <: Σ1′       𝜏2 <: 𝜏2′                   Σ2 <: Σ2′
                                                                          ′        ′
                                              𝜏1 Σ1 ⊗ Σ2 𝜏2 <: 𝜏1′ Σ1 ⊗ Σ2 𝜏2′




                                                Fig. 6. Sax: Subtyping



   The type safety logical relations is deﬁned in Figure 7. For simplicity, we only present the cases
for real numbers, variables, functions, and sums. The other cases are similar and straightforward.
The unary logical relations are split into mutually recursive value relations V, computation rela-
tion E, and environment relation G, and deﬁned as follows:
- Any value is in 𝐴𝑡𝑜𝑚J𝜏K if the value type checks to some 𝜏 ′ <: 𝜏 under an empty type environ-
  ment.
- A real number is in the value relation at type R if the number is in 𝐴𝑡𝑜𝑚JRK.
- Similarly, a unit value tt is always related at type unit.
- An inl(resp. inr) value is in the value relation at 𝜏1 ∅ ⊕∅ 𝜏2 if the value is in 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊕∅ 𝜏2 K
  and the underlying value 𝑣 is in the value relation at 𝜏1 (resp. 𝜏2 ).
                                                         𝑠𝑥                                      𝑠𝑥
- A closure is in the value relation at type (𝑥 : 𝜏1 ) −−→ 𝜏2 if it satisﬁes 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ) −−→ 𝜏2 K,
  and given any value 𝑣 in the value relation at argument type 𝜏1 , the extended conﬁguration
  𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 is in the computation relation at type 𝜏2 /(𝑥 : 𝜏1 ). We use the ./Γ operator to remove
  variables from a type and is deﬁned as follows:

                                    𝜏/Γ = [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏, ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ)


- A conﬁguration is in the computation relation at type 𝜏, if the conﬁguration reduces to some
  value 𝑣, which is itself in the value relation at type 𝜏.
- Finally, a value environment 𝛾 is in the environment relation at Γ if the domains of 𝛾 and Γ
  are the same, and for each variable in the domain of 𝛾 the underlying value 𝛾(𝑥) is in the value
  relation at type Γ(𝑥)/Γ (we use the ./Γ operator to emphasize that the type is closed).

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
28                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                 ∅ ⊢ 𝑣 : 𝜏 ′; ∅         𝜏 ′ <: 𝜏                 𝑟 ∈ 𝐴𝑡𝑜𝑚JRK                        tt ∈ 𝐴𝑡𝑜𝑚JunitK
                            𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏K                             𝑟 ∈ VJRK                          tt ∈ VJunitK

            ′                                                                   ′
        inl𝜏2 𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊕ ∅ 𝜏2 K               𝑣 ∈ VJ𝜏1 K             inr𝜏1 𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊕ ∅ 𝜏2 K           𝑣 ∈ VJ𝜏2 K
                         𝜏2′             ∅ ∅                                                 𝜏1′           ∅ ∅
                      inl      𝑣 ∈ VJ𝜏1 ⊕ 𝜏2 K                                            inr      𝑣 ∈ VJ𝜏1 ⊕ 𝜏2 K

                                (𝑣 1 , 𝑣 2 ) ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ &∅ 𝜏2 K        𝑣 1 ∈ VJ𝜏1 K            𝑣 2 ∈ VJ𝜏2 K
                                                       (𝑣 1 , 𝑣 2 ) ∈ VJ𝜏1 ∅ &∅ 𝜏2 K

                                h𝑣 1 , 𝑣 2 i ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊗ ∅ 𝜏2 K       𝑣 1 ∈ VJ𝜏1 K            𝑣 2 ∈ VJ𝜏2 K
                                                                          ∅ ∅
                                                       h𝑣 1 , 𝑣 2 i ∈ VJ𝜏1 ⊗ 𝜏2 K

                  s                                    𝑠𝑥
                h𝜆 𝑥 : 𝜏.𝑒, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ) −−→ 𝜏2 K             ∀𝑣 ∈ VJ𝜏1 K.𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 ∈ EJ𝜏2 /(𝑥 : 𝜏1 )K
                                                   s                                𝑠𝑥
                                               h𝜆 𝑥 : 𝜏1 .𝑒, 𝛾i ∈ VJ(𝑥 : 𝜏1 ) −−→ 𝜏2 K

            𝛾 ⊢𝑒 ⇓𝑣             𝑣 ∈ VJ𝜏K                    𝑑𝑜𝑚(Γ) = 𝑑𝑜𝑚(𝛾)              ∀𝑥 ∈ 𝑑𝑜𝑚(𝛾).𝛾(𝑥) ∈ VJΓ(𝑥)/ΓK
                      𝛾 ⊢ 𝑒 ∈ EJ𝜏K                                                     𝛾 ∈ GJΓK




                                           Fig. 7. Sax: Type Safety Logical Relations


   As usual, the fundamental property of the type safety logical relation states that well-typed open
terms are in the relation closed by an adequate environment 𝛾:
  Proposition 5.1 (Fundamental Property of the Type Safety Logical Relation).
Let Γ ⊢ 𝑒 : 𝜏; Σ, and 𝛾 ∈ GJΓK. Then 𝛾 ⊢ 𝑒 ∈ EJ𝜏/ΓK.
     Type safety for closed terms follows immediately as a corollary:
  Corollary 5.1 (Type Safety and Normalization of Sax).
Let ⊢ 𝑒 : 𝜏; ∅, then ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 and 𝜏 ′ , such that ⊢ 𝑣 : 𝜏 ′ ; ∅ and 𝜏 ′ <: 𝜏.

5.3     Type Soundness
This section establishes the type soundness of Sax, stated in terms of a metric preservation result.
Loosely speaking, metric preservation captures the maximum variation of an open term when it
is closed under two diﬀerent (but related) environments.
   Logical relations. To establish this soundness result, we make use of logical relations [4, 6]. In
particular, we deﬁne (mutually recursive) logical relations for sensitivity values, computations and
environments; see Figure 8. The logical relations for values (V𝑑 J𝜎K) and computations (E𝑑 J𝜎K) are
indexed by a relational distance 𝑑 ∈ R∞ ≥0 and a so called relational distance type 𝜎, which is a regular
type where sensitivity environments are enriched with a constant 𝑑 ∈ R∞        ≥0 denoting the distance
induced by pair of substitutions. Formally, the syntax of relational distance types is deﬁned as
follows:
                                                       Σ+𝑑
            𝜎 = R | B | unit | (𝑥 : 𝜎) −−−→ 𝜎 | 𝜎 Σ+𝑑 ⊕ Σ+𝑑 𝜎 | 𝜎 Σ+𝑑 &Σ+𝑑 𝜎 | 𝜎 Σ+𝑑 ⊗ Σ+𝑑 𝜎

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                         29



                                                              △
                                    (𝑟 1 , 𝑟 2 ) ∈ V𝑑 JRK ⇐⇒ |𝑟 1 − 𝑟 2 | ≤ 𝑑
                                                              △
                               (𝑣 1 , 𝑣 2 ) ∈ V𝑑 JunitK ⇐⇒ 𝑣 1 = tt ∧ 𝑣 2 = tt
                                                              △
          (inl 𝑣 1 , inl 𝑣 2 ) ∈ V𝑑 J𝜎1 𝑑 1 ⊕𝑑 2 𝜎2 K ⇐⇒ (𝑣 1 , 𝑣 2 ) ∈ V𝑑+𝑑 1 J𝜎1 K
                                                              △
          (inr 𝑣 1 , inr 𝑣 2 ) ∈ V𝑑 J𝜎1 𝑑 1 ⊕𝑑 2 𝜎2 K ⇐⇒ (𝑣 1 , 𝑣 2 ) ∈ V𝑑+𝑑 2 J𝜎2 K
                                                              △
     ((𝑣 11 , 𝑣 12 ), (𝑣 21 , 𝑣 22 )) ∈ V𝑑 J𝜎1 𝑑 1 &𝑑 2 𝜎2 K ⇐⇒ ∃𝑑 1′ , 𝑑 2′ , 𝑑 = 𝑑 1′ ⊔ 𝑑 2′ ∧
                                                                (𝑣 11 , 𝑣 21 ) ∈ V𝑑 1 +𝑑 1′ J𝜎1 K ∧ (𝑣 12 , 𝑣 22 ) ∈ V𝑑 2 +𝑑 2′ J𝜎2 K
                                                              △
    (h𝑣 11 , 𝑣 12 i, h𝑣 21 , 𝑣 22 i) ∈ V𝑑 J𝜎1 𝑑 1 ⊗𝑑 2 𝜎2 K ⇐⇒ ∃𝑑 1′ , 𝑑 2′ , 𝑑 = 𝑑 1′ + 𝑑 2′ ∧
                                                               (𝑣 11 , 𝑣 21 ) ∈ V𝑑 1 +𝑑 1′ J𝜎1 K ∧ (𝑣 12 , 𝑣 22 ) ∈ V𝑑 2 +𝑑 2′ J𝜎2 K
                                          Δ·Σ+𝑠𝑥              △
             (𝑣 1 , 𝑣 2 ) ∈ V𝑑 J(𝑥 : 𝜎1 ) −−−−−−→ 𝜎2 K ⇐⇒ ∀𝑑 ′, 𝑣 1′ , 𝑣 2′ , 𝛾 1, 𝛾 2, (𝑣 1′ , 𝑣 2′ ) ∈ V𝑑 ′ J𝜎1 K =⇒
                                                                 (𝛾 1 ⊢ 𝑣 1 𝑣 1′ , 𝛾 2 ⊢ 𝑣 2 𝑣 2′ ) ∈ E𝑑 +Δ·Σ+𝑠𝑑 ′ J𝑑 ′𝑥(𝜎2 )K
                                                              △
                        (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑 J𝜎K ⇐⇒ ∀𝑣 1, (𝑑 < ∞ ∧ 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑣 1 ) =⇒
                                                            ∃𝑣 2 , 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑣 2 ∧ (𝑣 1 , 𝑣 2 ) ∈ V𝑑 J𝜎K
                                                              △
                                    (𝛾 1 , 𝛾 2 ) ∈ GΔ JΓK ⇐⇒ 𝑑𝑜𝑚(𝛾 1 ) = 𝑑𝑜𝑚(𝛾 2 ) = 𝑑𝑜𝑚(Γ)∧
                                                             ∀𝑥 ∈ dom(Γ). (𝛾 1 (𝑥), 𝛾 2 (𝑥)) ∈ VΔ(𝑥) JΔ(Γ(𝑥))K



                                   Fig. 8. Sax: logical relations for metric preservation



Notice that the logical relations do not mention sensitivity environments Σ because they are de-
ﬁned over closed terms and values. Nevertheless, relational distance types 𝜎 do mention sensitiv-
ity environments Σ. We use a combination of sensitivity environments and relational distances
(Σ + 𝑑), because functions types introduce binders that cannot be substituted until application.
                                                      𝑥+𝑦
For instance, consider type (𝑥 : R) −−−→ (R 𝑥+3𝑧 ⊕2𝑥+2𝑦 R), and two pair of substitutions for 𝑦
and 𝑧, at distance 2 and 1 respectively, e.g. 𝛾 1 = 𝑦 ↦→ 1, 𝑧 ↦→ 1 and 𝛾 2 = 𝑦 ↦→ 3, 𝑧 ↦→ 2, where
|𝛾 1 (𝑦) − 𝛾 2 (𝑦)| ≤ 2 and |𝛾 1 (𝑧) − 𝛾 2 (𝑧)| ≤ 1. The corresponding relational distance type after substi-
                       𝑥+2
tution is (𝑥 : R) −−−→ (R 𝑥+3 ⊕2𝑥+4 R). For notation simplicity, in the rest of the section we name
relational distance types as types when the acompanying relational distances can be inferred from
the context. Also we omit the environment notations when they are empty. On the other hand, the
logical relation for environments (GΔ JΓK) is indexed by a relational distance environment Δ, map-
ping variables to relational distances in R∞ ≥0 and a type environment Γ. We use (𝑣 1, 𝑣 2 ) ∈ V𝑑 J𝜎K
to denote that value 𝑣 1 is related to value 𝑣 2 at type 𝜎 and relational distance 𝑑, and likewise for
expressions (i.e. computations) and environments.
   To deﬁne logical relations we also make use of relational distance instantiations, which have
shape Δ·(Σ + 𝑑) and act by replacing free variables in sensitivity environment Σ with the distances
provided by distance environment Δ. Relational distance instantiations only close variables deﬁned
in Δ and are formally deﬁned as:
                                                   Δ·∅ = 0
                                              Δ·(Σ + 𝑑) = Δ·Σ + 𝑑
                                             Δ·(Σ + 𝑠𝑥) = Δ·Σ + 𝑠𝑑               if Δ(𝑥) = 𝑑
                                             Δ·(Σ + 𝑠𝑥) = Δ·Σ + 𝑠𝑥               otherwise
Furthermore, to close a type under a sensitivity environment we use the relational distance type
instantiation operator Δ(𝜎) (note that a 𝜏 is also an 𝜎 assuming that the “default” relational distance

                                      ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
30                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


𝑑 is 0) deﬁned below.
                                                  Δ(R) = R
                                                  Δ(B) = B
                                               Δ(unit) = unit
                                               Σ′ +𝑑                     Δ·Σ′ +𝑑
                                Δ((𝑥 : 𝜎1 ) −−−→ 𝜎2 ) = (𝑥 : Δ(𝜎1 )) −−−−−→ Δ(𝜎2 )
                               Δ(𝜎1 Σ1 +𝑑1 ⊕ Σ2 +𝑑2 𝜎2 ) = Δ(𝜎1 ) Δ·Σ1 +𝑑1 ⊕ Δ·Σ2 +𝑑2 Δ(𝜎2 )
                               Δ(𝜎1 Σ1 +𝑑1 &Σ2 +𝑑2 𝜎2 ) = Δ(𝜎1 ) Δ·Σ1 +𝑑1 &Δ·Σ2 +𝑑2 Δ(𝜎2 )
                               Δ(𝜎1 Σ1 +𝑑1 ⊗ Σ2 +𝑑2 𝜎2 ) = Δ(𝜎1 ) Δ·Σ1 +𝑑1 ⊗ Δ·Σ2 +𝑑2 Δ(𝜎2 )

   Now that we have all the prerequisite, we brieﬂy go through the deﬁnition of the logical relations
(in Figure 8)5 :
- Two real numbers are related at type R and distance 𝑑, if and only if the absolute diﬀerence
  between both numbers is at most 𝑑. For instance, (1, 3) ∈ V2 JRK and (3, 1) ∈ V2 JRK, as the logical
  relations are reﬂexive.
- Unit value tt is always related to itself at type unit under any distance.
- Two inl (resp. inr) values are related at 𝜎1 𝑑1 ⊕𝑑2 𝜎2 and distance 𝑑 if the underlying values
  are related at type 𝜎1 (resp. 𝜎2 ) and distance 𝑑 + 𝑑 1 (resp. 𝑑 + 𝑑 2 ). The intuition is that 𝑑 can be
  treated as the distance between two computations that reduce to the given sums, and 𝑑 1 can be
  treated as the distance between the underlying values; thus the total cost is the addition of both
  distances. For instance, for any 𝑑 and 𝜎, we have (inl 1, inl 3) ∈ V0 JR 2 ⊕𝑑 𝜎K because they are
  at immediate distance zero (both are inl) and latent distance 2; instead of delaying the distance,
  one also has (inl 1, inl 3) ∈ V2 JR 0 ⊕𝑑 𝜎K, i.e. both values are at distance 2 with zero latent
  distance between their content.
- Two additive (resp. multiplicative) products are related at type 𝜎1 𝑑1 &𝑑2 𝜎2 (resp. 𝜎1 𝑑1 ⊗𝑑2 𝜎2 ) and
  distance 𝑑 + 𝑑 1′ ⊔ 𝑑 2′ (resp. 𝑑 + 𝑑 1′ + 𝑑 2′ ), if both ﬁrst components are related at type 𝜎1 and distance
  𝑑 +𝑑 1 +𝑑 1′ , and both second components are related at type 𝜎2 and distance 𝑑 +𝑑 2 +𝑑 2′ . For instance,
  ((inl 1, 4), (inl 3, 5)) ∈ V0 J(R 2 ⊕0 𝜎) 0 &1 RK are at distance 0 and (inl 1, inl 3) ∈ V0 JR 2 ⊕0 𝜎K
  and (4, 5) ∈ V1 JRK.
- Two sensitivity closures are related if, given related inputs, they produce related computations.
  In more detail, ﬁrst the environments has to be related at some Γ and distance environment Δ.
  Note that Δ has to be the same environment that closes the latent eﬀect of the function Δ·Σ +𝑠 ′𝑥,
  and the one that closes the input type (𝜎1 = Δ(𝜏1 )). Second, inputs 𝑣 1′ and 𝑣 2′ have to be related
  at argument type 𝜎1 and any distance 𝑑 ′ . Finally, the body of the functions in environments
  extended with inputs 𝑣 1′ and 𝑣 2′ have to be related computations at type 𝑑 ′𝑥(𝜎2 ) and distance
  𝑑 + Δ·Σ + 𝑠𝑑 ′ . Note that, as the variable 𝑥 is out of scope after the application, we replace any
  instance of 𝑥 with the distance of the inputs 𝑑 ′ , using the distance type instantiation operator.
  The new distance at which both computations are now related is computed as the addition of
  the distance of the values 𝑑, and the closed latent eﬀect 𝑑 ′𝑥(Δ·Σ + 𝑠𝑥) = Δ·Σ + 𝑠𝑑 ′ . For instance,
     s                               s                                             2+1𝑥
  (h𝜆 𝑥 : R.𝑥 + 𝑦), 𝑦 ↦→ 1i, h𝜆 𝑥 : R.𝑥 + 𝑦), 𝑦 ↦→ 3i ∈ V0 J(𝑥 : R) −−−→ RK, as in this case Δ = 2𝑦,
  Σ = 1𝑦, and Δ·Σ = 2𝑦·1𝑦 = 2.
- Two sensitivity conﬁgurations are related computations at type 𝜎 and distance 𝑑, noted (𝛾 1 ⊢
  𝑒 1, 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑 J𝜎K, when the distance is inﬁnite, or if the ﬁrst conﬁguration reduces to a value,
  then the second conﬁguration also reduces to a value, and these values are related at type 𝜎 and
  distance 𝑑.

5 for simplicity we use “distance” instead of ”relational distance”



ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       31


- Finally, value environment 𝛾 1 is related to value environment 𝛾 2 at type environment Γ and
  distance environment Δ, written (𝛾 1, 𝛾 2 ) ∈ GΔ JΓK, if they both map each variable 𝑥 in the type
  environment to values related at their corresponding type (closed with Δ) and at distance Δ(𝑥).
   Sensitivity Metric Preservation. Armed with these logical relations, we can establish the no-
tion of type soundness, and prove the fundamental property—well-typed terms are related with
themselves—which corresponds to metric preservation [49]. As usual, we state this property ap-
pealing to open terms, where free variables indicate input parameters, which are then closed by
related value environments.
  Theorem 5.2 (Sensitivity Metric Preservation). If Γ ⊢ 𝑒 : 𝜏 ; Σ, then for any distance
environment Δ with 𝑑𝑜𝑚(Γ) ⊆ 𝑑𝑜𝑚(Δ) and any pair of value environments (𝛾 1, 𝛾 2 ) ∈ GΔ JΓK, it holds
that (𝛾 1 ⊢ 𝑒, 𝛾 2 ⊢ 𝑒) ∈ E Δ·Σ JΔ(𝜏)K.
In other words, if a sensitivity term is well-typed, then for any valid distance environment Δ (that
“ﬁts” Γ) and any two value environments 𝛾 1, 𝛾 2 related at Γ and Δ, conﬁgurations 𝛾 1 ⊢ 𝑒, 𝛾 2 ⊢ 𝑒
represent related computations at type Δ(𝜏) (closing all free variables) and distance Δ·Σ. Note that
since 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Γ) ⊆ 𝑑𝑜𝑚(Δ), we have Δ·Σ ∈ R∞       ≥0 .
   From the above theorem it is easy to derive a corollary that only characterizes closed terms:
   Corrolary 5.2.1 (FP for closed sensitivity terms). If ∅ ⊢ 𝑒 : 𝜏 ; ∅, then (∅ ⊢ 𝑒, ∅ ⊢ 𝑒) ∈
E0 J𝜏K.
  As a direct consequence of Theorem 5.2 we can also establish the sensitivity type soundness at
base types:
                                                                                                     𝑠𝑥
    Theorem 5.3 (Sensitivity Type Soundness at Base Types). If ∅ ⊢ 𝑒 : (𝑥 : R) −−→ R ; ∅,
|𝑟 1 − 𝑟 2 | ≤ 𝑑, ∅ ⊢ 𝑒 𝑟 1 ⇓ 𝑟 1′ , ∅ ⊢ 𝑒 𝑟 2 ⇓ 𝑟 2′ , then |𝑟 1′ − 𝑟 2′ | ≤ 𝑠𝑑.
    Let us illustrate metric preservation by revisiting some examples. Consider example 4.2:
                      𝑥 : R, 𝑦 : R ⊢ let 𝑥 1, 𝑥 2 = h2 ∗ 𝑥, 𝑦i in 𝑥 1 + 2 ∗ 𝑥 2 : R; 2𝑥 + 2𝑦
If we know that in two diﬀerent executions 𝑥 may diﬀer in at most 1, and 𝑦 in at most 3, i.e.
Δ = 1𝑥 + 3𝑦, then the result will diﬀer in at most Δ·(2𝑥 + 2𝑦) = 1·2 + 3·2 = 8. For instance, if in one
execution 𝑥 is bound to 0 and 𝑦 to 4 then the result will be 8. In a second execution, if 𝑥 is bound
to 1 and 𝑦 to 6 then the result will be 14. Comparing both results we get |8 − 14| = 6 ≤ 8. Finally,
in a third execution, if 𝑥 is bound to 1 and 𝑦 to 7 then the result will be 16. Comparing with the
ﬁrst execution we have |8 − 16| = 8 ≤ 8, and with the second |14 − 16| = 2 ≤ 8.
   Now consider example 4.3:
                        𝑥 : R ⊢ case (𝑥 ≤ 10) {𝑥 1 ⇒ true}{𝑥 2 ⇒ false} : B; ∞𝑥
In this case if 𝑥 varies in two diﬀerent executions (Δ(𝑥) > 0) then the outcome will diﬀer in at
most Δ(𝑥)·∞ = ∞. For instance, if in one execution 𝑥 is bound to 0 the result will be true, and if in
a second execution 𝑥 is bound to 1, then the result is also going to be true, and true is at distance
zero with respect to itself, and 0 ≤ ∞. If in a third execution 𝑥 is bound to 11, then the result will
be false, and false is at distance inﬁnity with respect to true. Now, if we now that 𝑥 is constant
across multiple executions (Δ(𝑥) = 0), then we know from metric preservation that the result will
diﬀer in 0·∞ = 0, i.e. the result will be constant.

6    DESIGN OF JAZZ’S PRIVACY TYPE SYSTEM
In this section, we review the limitations of prior approaches related to the tracking of privacy, and
then discuss how they are addressed by Jazz. In this section, we color expressions and metavari-
ables 𝑟𝑒𝑑 as they pertain to the privacy fragment of Jazz.

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
32                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


6.1 Privacy Closures
Consider a family of looping combinators parameterized by the number of loop iterations 𝑛, e.g.,
where loop3 𝑥 𝑓 = 𝑓 (𝑓 (𝑓 𝑥)). In Fuzz, loop𝑛 would have the type 𝜏 → (𝜏 → 𝜏) ⊸𝑛 𝜏. In this
type, regular arrows → mean no sensitivity is tracked for the argument. The linear arrow ⊸𝑛
means the result is 𝑛-sensitive (where 𝑛 is the number of loop iterations) in the closure variables of
the supplied function of type (𝜏 → 𝜏). This allows for instantiating loop with a closure capturing
a sensitive variable, like db. So loop𝑛 0 (𝜆𝑥. 𝑥 + laplace𝜖 𝑑𝑏) will give 𝑛𝜖 diﬀerential privacy for
𝑑𝑏 by scaling 𝜖—the privacy cost of closure variable 𝑑𝑏—by the loop iteration 𝑛. When supporting
advanced variants of diﬀerential privacy like (𝜖, 𝛿), a diﬀerent metric must be chosen to recover
this kind of scaling; otherwise this argument only holds for pure 𝜖-diﬀerential privacy.
    In Duet, in order to support (𝜖, 𝛿)-diﬀerential privacy (and disallow problematic scaling), privacy
closures immediately report unbounded privacy (∞) for any captured variables in privacy lambdas.
The principle of loop’s type above is justiﬁed in Duet, but not via a scaling argument, and instead
via a primitive type rule—it cannot be expressed as a type. This is problematic for two reasons:
ﬁrst, it is not possible to extend Duet’s implementation with new looping primitives by adding
terms with axiomatically justiﬁed types, leading to a bloated set of core typing rules, and second,
it is not possible to lambda abstract looping combinators, e.g., to chain or compose them in helper
functions.
    To see the root cause for the limitation in Duet, we show the type rules for looping (advanced
composition) and function introduction (from [46]):

     Duet: Loop (Advanced Composition)
                                                                        Duet: Privacy-Fun-I (1-ary)
            Γ1 ⊢ 𝑒 1 : 𝜏         ⌉Γ2 ⌈𝜖,𝛿 , 𝑥 :∞ 𝜏 ⊢ 𝑒 2 : 𝜏
                                                                                    Γ , 𝑥 :𝜖,𝛿 𝜏1 ⊢ 𝑒 : 𝜏2
                     »
                   2𝜖 2𝑛 ln 𝛿1′ ,𝛿 ′ +𝑛𝛿          𝛿′                                p
  ⌉Γ1 ⌈∞ + ⌉Γ2 ⌈                           ⊢ loop𝑛 𝑒 1 {𝑥 ⇒ 𝑒 2 } : 𝜏   ⌉Γ⌈∞ ⊢ 𝜆 (𝑥 : 𝜏2 ). 𝑒 : 𝜏1 @(𝜖, 𝛿) ⊸∗ 𝜏2

In the rule for advanced composition shown above (left), 𝑒 1 is the initial value for the looping
state of type 𝜏, and 𝑒 2 is the loop body which updates the looping state 𝜏 → 𝜏 and may mention
closure variables in Γ2 . Parameter 𝛿 ′ is a meta-parameter for the advanced composition formula—
this parameter is unique to looping in (𝜖, 𝛿)-diﬀerential privacy. The notation ⌉Γ2 ⌈𝜖, 𝛿 means there
must exist some privacy cost 𝜖 and 𝛿 which upper-bounds any individual cost for each of these
closure variables. The privacy cost of thep       whole loop is calculated based on this upper bound
for closure variables with the formula 2𝜖 2𝑛 ln(1/𝛿 ′ ), 𝛿 ′ + 𝑛𝛿. An attempt to turn loop into a
primitive (or abstract over loop, e.g., eta-expand via lambda abstraction) fails because privacy
types in Duet do not track privacy eﬀects for closure variables; instead, they are just thrown
away. In the rule for function introduction shown above (right), the function type 𝜏1 @(𝜖, 𝛿) ⊸∗ 𝜏2
is a probabilistic function from elements in 𝜏1 to elements in 𝜏2 which satisﬁes (𝜖, 𝛿)-diﬀerential
privacy in its argument. Notice the closure environment Γ above the line which is bumped to ∞ in
⌉Γ⌈∞ below the line. This has the eﬀect of tossing out privacy bounds for anything with non-zero
privacy in Γ, i.e., any closure variables that are used in the function’s deﬁnition. Privacy is only
tracked for the function parameter 𝑥 (or possibly multiple parameters; privacy functions in Duet
are n-ary).
   A deeper limitation in Duet is that the iterated 1-ary function space does not generalize to
support encoding n-ary functions (i.e., curriﬁcation is not supported). For this reason, n-ary func-
tions are primitive in Duet. Implementing n-ary from 1-ary functions is computationally pos-
sible in Duet, but results in discarding bounds on privacy eﬀects. For example, the Duet term
 p                    p
𝜆 (𝑥 : 𝜏1 ). return (𝜆 (𝑦 : 𝜏2 ). 𝑓 (𝑥,𝑦)) in a context where 𝑓 : (𝜏1 @(𝜖1 , 𝛿 1 ), 𝜏2 @(𝜖2, 𝛿 2 )) ⊸∗ 𝜏3 has

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                            33


type (𝜏1 @∞) ⊸∗ (𝜏2 @(𝜖2 , 𝛿 2 )) ⊸∗ 𝜏3 , i.e., the privacy bounds (𝜖1, 𝛿 1 ) for the ﬁrst argument 𝜏1 get
discarded due to the Duet: Privacy-Fun-I rule.

   Privacy Closures in Jazz. In Jazz, both privacy and sensitivity eﬀects are delayed and attached
to type-level connectives, including for privacy functions. Whereas in Duet privacy functions
                                                                                                                       Σ
are written (𝜏1 @𝑝 1 , . . ., 𝜏𝑛 @𝑝𝑛 ) ⊸∗ 𝜏, privacy functions in Jazz are written simply (𝑥 : 𝜏1 ) ։ 𝜏2
where Σ is a latent contextual eﬀect that can mention 𝑥. A type can now be given to loop (a named
constant, analogous to the loop primitive from Duet) in Jazz, and abstracting over loop is possible
due to the function introduction rule, also shown below.
                                                                   Jazz: Privacy-Fun-I
                                                 ′   ′′
                      ⌉Σ⌈𝜖,𝛿       ⌉Σ⌈𝜖 ,𝛿                                     Γ, 𝑥 : 𝜏1 ⊢ 𝑒 : 𝜏2 ; Σ
        𝛿′
    loop𝑛 : 𝜏 → (𝜏 −−−−−−− →→ 𝜏) −−−−−−−−−→ →𝜏
                          p
      where 𝜖 ′, 𝛿 ′′ , 2𝜖 2𝑛 ln(1/𝛿 ′), 𝛿 ′ + 𝑛𝛿                       p
                                                                                                        Σ
                                                                   Γ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑). 𝑒 : (𝑥 : 𝜏1 ·𝑑) −−−→
                                                                                                         → 𝜏2 ; ∅

N-ary functions are now recoverable from 1-ary ones using latent contextual eﬀects in closures.
The relational distance 𝑑 defaults to 1 when omitted. The encoding of lambda-abstracted gauss
then follows the usual approach of nested lambda abstractions, but with sensitivity lambdas on the
outside with a single privacy lambda on the inside. A 3-ary abstraction of the Gaussian mechanism
applied to the sum of three arguments is as follows:
    s            s            p
  (𝜆 (𝑥 : R·1). 𝜆 (𝑦 : R·1). 𝜆 (𝑧 : R·1).
                           desired privacy
                                                                                                (𝜖,𝛿)𝑥⊔(𝜖,𝛿)𝑦⊔(𝜖,𝛿)𝑧
                    gauss 3 𝜖 𝛿 (𝑥 + 𝑦 + 𝑧)) : (𝑥 : R·1) → (𝑦 : R·1) → (𝑧 : R·1) −−−−−−−−−−−−−−−→
                                                                                                →R
                sensitivity sum of (𝑥 + 𝑦 + 𝑧)
    Notice here that the latent contextual eﬀect is computed using a syntactic join operator (𝜖, 𝛿)𝑥 ⊔
(𝜖, 𝛿)𝑦⊔(𝜖, 𝛿)𝑧, which computes the pointwise maximum, instead of the sum ((𝜖, 𝛿)𝑥 +(𝜖, 𝛿)𝑦+(𝜖, 𝛿)𝑧).
One of the novelties of Jazz is that we can reason about two executions where more than one input
is at relational distance greater than 0. In particular, if 𝑥, 𝑦 and 𝑧 are at relational distance 1, i.e.
the argument of gauss 3 𝜖 𝛿 is at relational distance 3, then using addition would yield an over-
approximated latent privacy of (3𝜖, 3𝛿), while using the join, we obtain a latent privacy of (𝜖, 𝛿) as
desired.

    Abstracting Privacy Mechanisms. Even with support for privacy closures, there are still chal-
lenges in supporting lambda abstraction around privacy mechanisms in full generality. In Fuzz,
the type assigned to the family of Laplace diﬀerential privacy mechanisms parameterized by 𝜖
is laplace𝜖 : R ⊸𝜖 R for achieved privacy 𝜖. This mechanism does not need a dedicated type
rule in the core calculus—it can be axiomatized as a primitive with the right type—and lambda-
abstracting this primitive is natural via eta-expansion 𝜆(𝑥 : R). laplace𝜖 𝑥 resulting in the same
type and guarantee for privacy. However this approach does not support (𝜖, 𝛿)-diﬀerential privacy
directly. Fuzz𝜖𝛿 shows how to extend Fuzz to recover (𝜖, 𝛿)-diﬀerential privacy, by using graded
comonadic liftings, and path construction. In particular, the type assigned to the family of Gauss-
ian diﬀerential privacy mechanisms parametrized by 𝜀 and 𝛿 is gauss(𝜖,𝛿) : ⌈R⌉ ⊸ (𝜖,𝛿) R, where
⌈R⌉ is R but with the metric rounded up to the nearest integer. In Duet, in order to support
(𝜖, 𝛿)-diﬀerential privacy, the Gaussian mechanism requires its own typing rule, shown below. Fur-
thermore, a use of the mechanism looks like gauss𝑠𝜖,𝛿 𝑒 where the argument 𝑒 is a term in the
sensitivity language with sensitivity bounded by 𝑠. Using privacy closures as described above, we
             p
can write 𝜆 (𝑥 : R). gauss 1 𝜖 𝛿 𝑥, however note that we have lost the ability to be parametric in
𝑠—it must be ﬁxed to 1. This assumption that gauss will be called only with a 1-sensitive argument

                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
34                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


is enforced in the function application rule in Duet, also shown below.
             Duet: Gauss                              Duet: Privacy-Fun-E
                   ⌉Γ ⌈𝑠 ⊢ 𝑒 : R                     Γ1 ⊢ 𝑒 1 : 𝜏1 @(𝜖, 𝛿) ⊸∗ 𝜏2            ⌉Γ2 ⌈1 ⊢ 𝑒 2 : 𝜏1
            ⌉Γ⌈𝜖,𝛿 ⊢ gauss𝑠𝜖,𝛿 𝑒 : R                             ⌉Γ1 ⌈∞ + ⌉Γ2 ⌈𝜖,𝛿 ⊢ 𝑒 1 𝑒 2 : 𝜏2
In the rule for gauss (left) it allows an argument of any sensitivity 𝑠, however the privacy function
application rule (right) restricts that arguments must have sensitivity equal to 1. Restricting gauss
to only 1-distance arguments can be overly restrictive (e.g., gauss 2 𝜖 𝛿 (𝑥 + 𝑥)), and relaxing the
restriction on function application to an arbitrary 𝑠 ≠ 1 in Duet would be unsound.
   In Jazz, we extend function introduction to include an explicit bound on the sensitivity of the
parameter, and enforce this restriction in the application rule. Function introduction syntax intro-
duces the bound, and allows us to eta-expand the Gaussian mechanism with relational distance 𝑑
as a parameter, as shown below. The bound 𝑑 for the lambda argument is then enforced in function
application as the upper bound of argument relational distance, instead of being ﬁxed to 1 as in
Duet. Now the use of a variable—like 𝑥 in the body of eta-expanded gauss below—is not always
considered 1-sensitive. To communicate non-zero sensitivities to variables in the type system, an
environment of relational distances on lambda arguments must be threaded through the type sys-
tem, which we notate Δ. After extending this Δ to remember that 𝑥 has relational distance 𝑑 in
Jazz lambda abstraction, gauss 𝑠 𝜖 𝛿 𝑥 will see 𝑥 as 𝑑 distant inside the lambda body. To do this,
we allow lambda-abstracting gauss (including the distance parameter 𝑑, via singleton types), and
extend the structure of typing for sensitivity and privacy terms respectively as follows:
       s
                ˆ ). 𝜆 (𝑥 : R ·𝑑ˆ ). gauss 𝑑 𝜖 𝛿 𝑥
      𝜆 ( 𝑑 : R[𝑑]
                         p
                                                                 Γ ; Δ ⊢ 𝑒 :𝜏 ; Σ             Γ ; Δ ⊢ e:𝜏 ;Σ


6.2 Sensitivity Binding in Privacy Contexts
Jazz improves on prior systems by supporting let-binding intermediate sensitivity computations
within the privacy language, while also supporting (𝜖, 𝛿)-diﬀerential privacy. Fuzz and DFuzz en-
code let-binding through function application, which scales the sensitivity of the right-hand-side
of the let with the sensitivity of the let-variable in the body. So let 𝑦 = 2 ∗ 𝑥 in 3 ∗𝑦 is 6-sensitive
in 𝑥 because the right-hand-side is 2-sensitive, and this is scaled by 3, the sensitivity of 𝑦 in the
body. However, monadic return and bind in Fuzz can also be used to encode let-binding, e.g.,
𝑥 ← return 𝑒 1 ; 𝑒 2 instead of let 𝑥 = 𝑒 1 in 𝑒 2 . Unfortunately, this encoding of let using return
and monadic bind does not preserve typeability in Fuzz; instead it destroys the sensitivity/privacy
analysis of the right-hand-side, bumping its privacy cost unnecessarily to ∞. For this reason, let
statements are encoded exclusively through function application in Fuzz, and not through monadic
return/bind.
   In Fuzz, let-binding a sensitivity computation (the pure fragment) inside a privacy computa-
tion (the monadic fragment)—via encoding through function application—is supported seamlessly
without the addition of extra rules. This ﬂexibility can be extended to advanced privacy variants
as shown by de Amorim et al. [29]. In Duet, however, the privacy/monadic fragment of Fuzz is
pulled out into its own language with explicit typing rules; the primary reason to do this is to place
restrictions on function application in order to support advanced privacy variants, as described in
the previous subsection. This leaves the need for either an explicit typing rule for let-binding inside
the privacy language, or an escape hatch so that privacy analysis is not destroyed for let-binding
in privacy contexts a la Fuzz. Duet solves this issue by introducing a boxed type which delays the
payment of a sensitivity term at the point it is “boxed”, and pays for it later when it is “unboxed”.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       35


This avoids the issue but is unfriendly to program with: every let-binding requires an explicit box,
and every use of a let-bound variable requires an explicit unbox. So instead of writing the program
below on the left, Duet programmers are forced to write the program on the right.

       let 𝑦 = expensive 𝑥 in                           let 𝑦 = box (expensive 𝑥) in
                          p
       loop 100 initial (𝜆 (𝑖 : 𝜏). body 𝑦 𝑖)                              p
                                                        loop 100 initial (𝜆 (𝑖 : 𝜏). body ( unbox 𝑦) 𝑖)
In this program it is essential to let-bind the expensive result, since inlining it would unnecessarily
duplicate the computation, and many real programs in diﬀerential privacy require support for this
pattern [46].
   In Jazz, we recover the expressiveness that box types provide, while eliminating the need for
the programmer to explicitly introduce and eliminate them. In this way, our design can also be
seen as a powerful box-inference capability, although we do not demonstrate explicit embeddings
between a core language with box types. To recover the expressiveness of boxes without requiring
the programmer to write them down, we add new information to typing judgments that has the
eﬀect of automatically boxing let-bound variables in privacy contexts, and unboxing them at their
use. The added information extends typing judgments with a new component Φ that tracks the
sensitivities of all let-bound variables w.r.t. the sensitivities of all lambda-bound variables. All
sensitivity contexts that mention both let-bound and lambda-bound variables are then reduced
using Φ as needed to contexts that only mention lambda-bound variables. Φ can be seen as a matrix,
and the reduction of contexts to only lambda-bound variables is then just matrix multiplication—a
beautiful coincidence for a linear type system. The ﬁnal form of type judgments for the sensitivity
and privacy type systems are then:

                        Γ ; Δ;Φ⊢𝑒 :𝜏 ; Σ                               Γ ;Δ;Φ⊢𝑒 :𝜏 ; Σ

Although the prototype implementation adopts the typing rules with Φ, and because the manipu-
lation of Φ is more tedious than insightful, we omit it in the following technical presentation.

7   JAZZ’S DIFFERENTIAL PRIVACY TYPE SYSTEM, FORMALLY
In this section, we present a core subset of Jazz, dubbed 𝜆J . 𝜆J is an extension of Sax with sup-
port for reasoning about diﬀerential privacy. Similarly to Sax, we prove the type safety and type
soundness property of 𝜆J . We discuss how to bridge the gap between 𝜆J and Jazz in Section 8. Note
that our formalism is ﬁxed to (𝜖, 𝛿)-diﬀerential privacy, but our design can be instantiated to other
forms of advanced diﬀerential privacy disciplines as illustrated in Section 8.

7.1 Syntax and Type System
𝜆J is divided in two mutually embedded sublanguages: the sensitivity sublanguage —an extension
of Sax— used to reason about the sensitivity of computations, and the privacy sublanguage used
to reason about diﬀerential privacy. Thus, the type system of 𝜆J contains two mutually embedded
type systems, one for each of the sublanguages. Expressions of the sensitivity sublanguage remain
typeset in green and expressions of the privacy sublanguage are typeset in red.
   Syntax. Figure 9 presents the syntax of 𝜆J . Expressions of the language are divided into two
mutually embedded expressions: sensitivity expressions 𝑒 and privacy expressions e. Sensitivity
expressions are deﬁned the same way as in Sax, except that functions are split into sensitivity
           s                                 p
lambdas 𝜆 (𝑥 : 𝜏 ·𝑑). 𝑒 and privacy lambdas 𝜆 (𝑥 : 𝜏 ·𝑑). e. Note that the only diﬀerence between a
sensitivity lambda and a privacy lambda is that the body of a privacy lambda is a privacy expression
e. Also, both sensitivity lambdas and privacy lambdas are parametrized by a relational distance 𝑑

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
36                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                              s               p
         𝑒 ∈ sexpr F ... | 𝜆 (𝑥 : 𝜏·𝑑). 𝑒 | 𝜆 (𝑥 : 𝜏·𝑑). e                           sensitivity expressions
         e ∈ pexpr F return 𝑒 | 𝑥 : 𝜏 ← e ; e | e e                                  return, bind, applications
                   | if 𝑒 then e else e | case 𝑒 of {𝑥 ⇒ e} {𝑦 ⇒ e}                  conditionals, case
                   | let 𝑥 = 𝑒 in e                                                  let
         𝑝 ∈ 𝑝𝑟𝑖𝑣 , (R∞ , R∞ )                                                       privacies
         Σ ∈ 𝑝𝑒𝑛𝑣 , ∅ | 𝑝𝑥 | Σ + Σ | Σ ⊔ Σ | Σ ⊓ Σ                                   privacy environments
                                       Σ                Σ
         𝜏 ∈ type F ... | (𝑥 : 𝜏·𝑑) −
                                    → 𝜏 | (𝑥 : 𝜏·𝑑) −→
                                                     →𝜏                              types
         Γ ∈ tenv , var ⇀ type F {𝑥 : 𝜏, . . . , 𝑥 : 𝜏 }                             type environments



                                                   Fig. 9. 𝜆J : Syntax


which represents an upper bound on distance between inputs pertained to the binary relational
property of diﬀerential privacy: the maximum argument variation for each of two executions.
    A privacy expression e can be a point distribution return 𝑒, a sequential composition 𝑥 : 𝜏 ←
   e ; e, an application e e, a conditional if 𝑒 then e else e, a case expression case 𝑒 of {𝑥 ⇒
e} {𝑦 ⇒ e}, or a let let 𝑥 = 𝑒 in e.
    A privacy cost 𝑝 = (𝜖, 𝛿) is a pair of two (possibly-inﬁnite) real numbers, where the ﬁrst compo-
nent corresponds to the epsilon, and the second to the delta in (𝜖, 𝛿)-diﬀerential privacy. We use
notation 𝑝.𝜖 and 𝑝.𝛿 to extract 𝜖 and 𝛿 respectively. A privacy environment Σ is either an empty
environment ∅, a pair 𝑝𝑥 representing that variable 𝑥 has privacy cost 𝑝, the addition Σ + Σ of two
privacy environments, the join Σ ⊔ Σ of two privacy environments, and the meet Σ ⊓ Σ of two
privacy environments. Similarly to sensitivity environments, we also write privacy environments
as ﬁrst-order polynomials when possible. For instance 𝑝 1𝑥 + 𝑝 2𝑥 can be written as (𝑝 1 + 𝑝 2 )𝑥, but
𝑝 1𝑥 + (𝑝 2𝑥 ⊔ 𝑝 3𝑦) cannot be rewritten as a polynomial without losing precision. Function types are
                                                                 Σ                                                Σ
now divided into sensitivity function types (𝑥 : 𝜏 ·𝑑) →
                                                       − 𝜏, and privacy function types (𝑥 : 𝜏 ·𝑑) −
                                                                                                  →→ 𝜏.
   Sensitivity type system. The type system for the sensitivity sublanguage is presented in Figure 10.
The judgment Γ ; Δ ⊢ 𝑒 : 𝜏 ; Σ now includes a novel relational distance environment Δ. The rela-
tional distance environment Δ stores how much each variable in Γ can vary in every two execu-
tions of a program. Most of the rules are straightforward extensions of the type system of Sax to
include relational distance environments. We only present interesting cases.
   Some of the rules use the sensitivity environment substitution operator [Σ/𝑥]𝜏. We extend the
deﬁnition of Sax to support privacy functions as shown in Figure 11. Substitution on privacy
function types depends on the deﬁnition of sensitivity environment substitution on privacy envi-
ronments [Σ/𝑥]Σ. [Σ/𝑥]Σ is deﬁned inductively on the structure of Σ, where the only interesting
case is when Σ = 𝑝𝑥. Substitution [Σ/𝑥]𝑝𝑥 is deﬁned using the lift operator: ⌉Σ⌈𝑝 . Intuitively, if
we wiggle 6 𝑥 on 𝑝𝑥, then the privacy obtained is at most 𝑝 (no scaling, and zero if 𝑥 does not
change). After substitution, as 𝑥 depends on all variables on Σ, if we wiggle all variables in Σ at
the same time, then the privacy obtained should still be 𝑝 (scaling 𝑝 would be an over approxi-
mation). Because of this, ⌉Σ⌈𝑝 is deﬁned as the join 𝑝𝑥 1 ⊔ ... ⊔ 𝑝𝑥𝑛 , where 𝑥𝑖 ∈ 𝑑𝑜𝑚(Σ). If all 𝑥𝑖
wiggle, then the privacy obtained would be at most 𝑝. But as any Σ(𝑥𝑖 ) can be zero (it means that
variable 𝑥𝑖 is not used), we multiply each 𝑝 in 𝑝𝑥𝑖 , by ⌉Σ(𝑥𝑖 )⌈1 , to remove those variables from the
6 We show how to wiggle variables on privacy environment with the relational distance instantiation operator, later on

Section 7.3.


ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                            37




                  var                                        s-lam
                         Γ(𝑥) = 𝜏                                    Γ, 𝑥 : 𝜏1 ; Δ + 𝑑𝑥 ⊢ 𝑒 : 𝜏2 ; Σ
                                                                       s                            Σ
                  Γ ; Δ + 𝑑𝑥 ⊢ 𝑥 : 𝜏 ; 𝑥                     Γ ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑). 𝑒 : (𝑥 : 𝜏1 ·𝑑) −
                                                                                                    → 𝜏2 ; ∅

                                      p-lam
                                                  Γ, 𝑥 : 𝜏1 ; Δ + 𝑑𝑥 ⊢ e : 𝜏2 ; Σ
                                                   p                          Σ
                                     Γ ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑). e : (𝑥 : 𝜏1 ·𝑑) −→
                                                                             → 𝜏2 ; ∅

                      s-app
                                                Σ
                      Γ ; Δ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑑) −
                                                → 𝜏2 ; Σ1          Γ ; Δ ⊢ 𝑒 2 : 𝜏1 ; Σ2       Δ·Σ2 ≤ 𝑑
                                        Γ ; Δ ⊢ 𝑒 1 𝑒 2 : [Σ2 /𝑥]𝜏2 ; Σ1 + [Σ2 /𝑥]Σ

         s-case
                                          Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1
         Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2     Γ, 𝑦 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ12 ))𝑦 ⊢ 𝑒 3 : 𝜏3 ; Σ3
                     Γ ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } :
                          [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ; Σ1 ⊔ ([Σ1 + Σ11 /𝑥]Σ2 ) ⊔ ([Σ1 + Σ12 /𝑦]Σ3 )

        untup
                                              Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊗ Σ12 𝜏12 ; Σ1
            Γ, 𝑥 1 : 𝜏11 , 𝑥 2 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 1 + (Δ·(Σ1 + Σ12 ))𝑥 2 ⊢𝑒 2 : 𝜏2 ; 𝑠 1𝑥 1 + 𝑠 2 𝑥 2 + Σ2
       Γ ; Δ ⊢ let 𝑥 1 , 𝑥 2 = 𝑒 1 in 𝑒 2 : [Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ; (𝑠 1 ⊔ 𝑠 2 )Σ1 + 𝑠 1 Σ11 + 𝑠 2 Σ12 + Σ2




                         Fig. 10. 𝜆J : Type system of the sensitivity sublanguage (extract)


                                              ′
resulting privacy environment. ⌉𝑠 ⌈𝑠 along other lift operators used by Near et al. [46] are deﬁned
in Figure 11. For instance, suppose that 𝑥 depends on 2𝑦 + 0𝑧, then [(2𝑦 + 0𝑧)/𝑥]𝑝𝑥 is computed as
⌉2𝑦 + 0𝑧 ⌈𝑝 = 𝑝𝑦 ⊔ 0𝑧 = 𝑝𝑦.
   We now turn to describe the main changes of each type rule with respect to Sax.
- Rule var now requires variable 𝑥 to be present in the relational distance environment Δ. This
  way, if Γ; Δ ⊢ 𝑒 : 𝜏; Σ, we can compute how much the result of evaluating 𝑒 can change if
  we wiggle input 𝑥, by multiplying Δ(𝑥) by Σ(𝑥). For instance, consider program 𝑥 + 𝑥 and the
  following type derivations
                            var                                            plus
                                (𝑥 : R)(𝑥) = R                                      D         D
                     D=
                            𝑥 : R; 3𝑥 ⊢ 𝑥 : R ; 𝑥                          𝑥 : R; 3𝑥 ⊢ 𝑥 + 𝑥 : R ; 2𝑥

  Then we know that (1) 𝑥 can change at most by 3, and (2) the expression is 2-sensitive in 𝑥,
  therefore the result can change at most by 6.
- Rule s-lam type checks sensitivity functions. As the body of the lambda has 𝑥 as a free variable,
  the relational distance environment Δ is extended with distance 𝑑 obtained from the type anno-
                                                          s
  tation on the argument. For example, consider program 𝜆 (𝑥 : R·2). 𝑥 + 𝑥 and its type derivation:

                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
38                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                                                                                       [Σ/𝑥]𝜏
                                                        ... = ...
                                               Σ′                             [Σ/𝑥]Σ′
                                                → 𝜏2 ) = (𝑦 : [Σ/𝑥]𝜏1 ·𝑑) −−−−−−−→
                            [Σ/𝑥]((𝑦 : 𝜏1 ·𝑑) −−→                                → [Σ/𝑥]𝜏2
                                                                                                       [Σ/𝑥]Σ
                                             [Σ/𝑥]∅ = ∅
                                           [Σ/𝑥](𝑝𝑥) = ⌉Σ⌈𝑝
                                           [Σ/𝑥](𝑝𝑦) = 𝑝𝑦
                                      [Σ/𝑥](Σ1 + Σ2 ) = ([Σ/𝑥]Σ1 ) + ([Σ/𝑥]Σ2 )
                                      [Σ/𝑥](Σ1 ⊔ Σ2 ) = ([Σ/𝑥]Σ1 ) ⊔ ([Σ/𝑥]Σ2 )
                                      [Σ/𝑥](Σ1 ⊓ Σ2 ) = ([Σ/𝑥]Σ1 ) ⊓ ([Σ/𝑥]Σ2 )
                                                                                                         ⌉Σ⌈𝑝
                                                                    Ã
                                                    ⌉Σ⌈𝑝 =              𝑝𝑥
                                                                𝑥 ∈𝑑𝑜𝑚(Σ)
                                                                                                         ⌉Σ⌈𝑠
                                                        𝑠′
                                                ⌉𝑠 ⌈ = 𝑠 ′             𝑠>0
                                                     ′
                                               ⌉∅⌈𝑠 = ∅
                                                     ′      ′       ′
                                           ⌉Σ + 𝑠𝑥 ⌈𝑠 = ⌉Σ⌈𝑠 + ⌉𝑠 ⌈𝑠 𝑥
                                                     ′      ′
                                           ⌉Σ + 0𝑥 ⌈𝑠 = ⌉Σ⌈𝑠 + 0𝑥
                                                                                                         ⌉Σ⌈𝑠
                                                    ′
                                               ⌉𝑝 ⌈𝑝 = 𝑝 ′                   𝑝 ≠ (0, 0)
                                                    ′
                                             ⌉∅⌈𝑝 = ∅
                                                   ′       ′
                                            ⌉𝑝𝑥 ⌈𝑝 = ⌉𝑝 ⌈𝑝 𝑥
                                                  ∞
                                        ⌉(0, 0)𝑥 ⌈ = (0, 0)𝑥
                                      ⌉Σ1 + Σ2 ⌈∞ = ⌉Σ1 ⌈∞ + ⌉Σ2 ⌈∞
                                      ⌉Σ1 ⊔ Σ2 ⌈∞ = ⌉Σ1 ⌈∞ ⊔ ⌉Σ2 ⌈∞
                                      ⌉Σ1 ⊓ Σ2 ⌈∞ = ⌉Σ1 ⌈∞ ⊓ ⌉Σ2 ⌈∞



                              Fig. 11. 𝜆J : Auxiliary definitions of the static semantics



                                 s-lam
                                               𝑥 : R; 2𝑥 ⊢ 𝑥 + 𝑥 : R ; 2𝑥
                                           s                                    2𝑥
                                 ∅ ; ∅⊢ 𝜆 (𝑥 : R·2). 𝑥 + 𝑥 : (𝑥 : R·2) −−→ R ; ∅
  The program is a sensitivity lambda that takes as argument a real with an allowed variation of
  at most 2, and has a latent contextual eﬀect of 2𝑥.
- Rule p-lam is deﬁned analogously to s-lam, except that its body is a privacy term, therefore it
  is type checked using the privacy type system, explained later.
- Rule s-app deals with sensitivity applications. Note that from the type of the function we know
  that 𝑑 is an upper bound on the allowed argument variation, therefore we require that the dot
  product between the relational distance environment and the sensitivity eﬀect of the argument
  be less or equal than 𝑑. Intuitively, as Δ represents how much the input can change, and Σ2 repre-
  sent the sensitivity of variables used in the argument, Δ·Σ2 represents how much the argument
                                                    s          s
  can change. For example, consider program 𝜆 (𝑦 : R·1). (𝜆 (𝑥 : R·2). 𝑥 + 𝑥)(𝑦 + 𝑦) and its type
  derivation:

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                           39




 s-lam
 s-app
                  s                                       2𝑥
 𝑦 : R ; 1𝑦 ⊢ (𝜆 (𝑥 : R·2). 𝑥 + 𝑥) : (𝑥 : R·2) −−→ R                𝑦 : R ; 1𝑦 ⊢(2 ∗ 𝑦) : R; 2𝑦           (1𝑦·2𝑦) ≤ 2
                                                      s
                                𝑦 : R ; 1𝑦 ⊢ (𝜆 (𝑥 : R·2). 𝑥 + 𝑥)(2 ∗ 𝑦) : R ; 4𝑦
                                s                 s                                       4𝑦
                      ∅ ; ∅⊢ 𝜆 (𝑦 : R·1). (𝜆 (𝑥 : R·2). 𝑥 + 𝑥)(2 ∗ 𝑦) : (𝑦 : R) −−→ R ; ∅

  The outermost lambda allows a maximum variation of 1 in its argument 𝑦. The inner lambda
  allows a maximum variation of 2 on its argument, and its being applied to 2 ∗ 𝑦. As 2 ∗ 𝑦 is 2-
  sensitive on 𝑦 and 𝑦 can wiggle at most by 1, then we know that the argument is going to wiggle
  at most by 2, which matches the maximum permitted argument variation. If the argument were
  3 ∗𝑦, then the program would not type check as the argument of the application could wiggle at
  most by 1 ∗ 3 = 3.
- Rule s-case type checks subterms 𝑒 2 and 𝑒 3 by extending the relational distance environment
  with a sound bound for 𝑥 and 𝑦 respectively. For 𝑥 (resp. 𝑦) we use the dot product between the
  relational distance on all variables in scope Δ, and the cost of using 𝑒 1 : the cost Σ1 of reducing
  the expression, plus the latent cost of using its subterm Σ11 (resp. Σ12 ). For example, consider the
  type derivation of Example 4.4 given e.g. relational distance environment 𝑥 + 2𝑏:

              case
                                       Γ; 𝑥 + 2𝑏 ⊢ 𝑒 : R ∞𝑥 ⊕𝑥 R; 𝑏
              Γ, 𝑥 1 : R; 𝑥 + 2𝑏 + ∞𝑥 1 ⊢ 0 : R; ∅      Γ, 𝑥 2 : R; 𝑥 + 2𝑏 + 3𝑥 2 ⊢ 𝑥 2 : R; 𝑥 2
                            Γ; 𝑥 + 2𝑏 ⊢ case 𝑒 of {𝑥 1 ⇒ 0}{𝑥 2 ⇒ 𝑥 2 } : R; 𝑏 + 𝑥

  The relational distance for 𝑥 1 on the ﬁrst branch is computed as the dot product between the
  maximum distance of all variables in scope, 𝑥 + 2𝑏, and the cost of using 𝑒 if it were an inl
  expression, i.e. ((𝑥 + 2𝑏)·(∞𝑥 + 𝑏)) = ∞. Analogously, the bound for 𝑥 2 on the second branch is
  computed as ((𝑥 + 2𝑏)·(𝑥 + 𝑏)) = 3.
- In Rule untup, as expression 𝑒 2 has in scope new variables 𝑥 1 and 𝑥 2 , the relational distance
  environment Δ is extended accordingly. The relational distance for 𝑥 1 is computed as the dot
  product between the relational distance environment Δ and the cost Σ1 + Σ11 of accessing the
  ﬁrst component (we proceed similarly with 𝑥 2 ). For instance, consider the type derivation of
  Example 4.2 given some arbitrary relational distance environment 2𝑥 + 3𝑦
                      untup
                                        Γ; 2𝑥 + 3𝑦 ⊢ (2 ∗ 𝑥, 𝑦) : R 2𝑥 ⊗ 𝑦 R ; ∅
                      Γ, 𝑥 1 : R, 𝑥 2 : R; 2𝑥 + 3𝑦 + 4𝑥 1 + 3𝑥 2 ⊢ 𝑥 1 + 2 ∗ 𝑥 2 : R ; 𝑥 1 + 2𝑥 2
                       Γ; 2𝑥 + 3𝑦 ⊢ let 𝑥 1, 𝑥 2 = (2 ∗ 𝑥,𝑦) in 𝑥 1 + 2 ∗ 𝑥 2 : R ; 2𝑥 + 2𝑦

  The relational distance for 𝑥 1 is computed as the dot product between the relational distance of
  all variables in scope 2𝑥 + 3𝑦 and the eﬀect of using the left component of the pair 2𝑥 + 0𝑦, i.e.
  (2𝑥 + 3𝑦)·(2𝑥 + 0𝑦) = 4. Similarly, the bound of 𝑥 2 is computed as (2𝑥 + 3𝑦)·(𝑦 + 0𝑥) = 3
  Subtyping is extended accordingly and presented in Figure 12. Parameterized relational dis-
tances on function types are contravariant, and subtyping for privacy function types relies on the
deﬁnition of subtyping for privacy environment also deﬁned in Figure 12, where • is an operator

                                    ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
40                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter



                                                                                                                       𝜏 <: 𝜏
       s-lam                                                              p-lam
       𝜏1′ <: 𝜏1      𝑑 ′ <: 𝑑       Σ <: Σ′            𝜏2 <: 𝜏2′         𝜏1′ <: 𝜏1     𝑑 ′ <: 𝑑     Σ <: Σ′        𝜏2 <: 𝜏2′
                       Σ                           Σ′                                    Σ                       Σ′
                        → 𝜏2 <: (𝑥 : 𝜏1′ ·𝑑 ′) −−→ 𝜏2′
            (𝑥 : 𝜏1 ·𝑑) −                                                                  → 𝜏2 <: (𝑥 : 𝜏1′ ·𝑑 ′) −−→
                                                                              (𝑥 : 𝜏1 ·𝑑) −→                        → 𝜏2′


                                                                                                                      Σ <: Σ

                                            ∀Δ, 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Δ).Δ•Σ ≤ Δ•Σ′
                                                                    Σ <: Σ′




                                                    Fig. 12. 𝜆J : Subtyping


to close privacy environments deﬁned below:
                                        Δ•∅ = 0
                                 Δ•(Σ1 + Σ2 ) = (Δ•Σ1 ) + (Δ•Σ2 )
                                 Δ•(Σ1 ⊔ Σ2 ) = (Δ•Σ1 ) ⊔ (Δ•Σ2 )
                                 Δ•(Σ1 ⊓ Σ2 ) = (Δ•Σ1 ) ⊓ (Δ•Σ2 )
                                       Δ•𝑝𝑥 = 𝑝                               if Δ(𝑥) is deﬁned

   Privacy type system. The type system of the privacy part of the language is presented in Figure 13.
The judgment Γ ; Δ ⊢ e : 𝜏 ; Σ says that privacy term e has type 𝜏 and ambient privacy eﬀect Σ
under type environment Γ, and relational distance environment Δ.
- Rule return uses the type system of the sensitivity language to type check its subexpression 𝑒.
  Operationally, return constructs a point-distribution, and any sensitive variables in the subex-
  pression 𝑒 will have their privacy violated, i.e., privacy cost ∞. Notice that ∞ corresponds to
  the pair (𝜖, 𝛿) = (∞, ∞). The resulting ambient privacy eﬀect is computed by lifting to inﬁnity
  the ambient eﬀect of the subexpression as well as all free variable in 𝑒. The operator that lift to
  ∞ free variables is written FP∞ and deﬁned in Figure 13. As we pay inﬁnity for every free vari-
  able in 𝑒, we remove those variables from the reported type 𝜏 using the sensitivity environment
  substitution operator deﬁned in Figure 11. For instance, consider the following type derivation,
                           return
                                               s                                      2𝑥+𝑦
                                 Γ; 𝑦 + 𝑧 ⊢ 𝜆 (𝑥 : R·1). 2𝑥 + 𝑦 : (𝑥 : R·1) −−−−→ R; ∅
                                                        s                                    2𝑥
                           Γ; 𝑦 + 𝑧 ⊢ return 𝜆 (𝑥 : R·1). 2𝑥 + 𝑦 : (𝑥 : R·1) −−→ R; ∞𝑦
  The resulting type and eﬀect environment is computed by paying in advance for the free vari-
  ables in scope: the type [∅/𝑦](2𝑥 + 𝑦) = 2𝑥 is computed by erasing the free variables, and the
  eﬀect environment ∞𝑦 is computed by lifting the free variables to inﬁnity.
- Rule bind type checks both subexpressions using the type system for the privacy language as
  they are privacy expressions. To type check e2 we extend type environment with variable 𝑥,
  therefore the relational distance environment Δ is also extended. We extend Δ with 0𝑥 as the
  value bound to 𝑥 is no longer considered sensitive—it has been declassiﬁed and can be used
  without restriction. Finally, as 𝑥 is out of scope we remove it from 𝜏2 and from the resulting

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                             41




   return                                                   bind
   Γ ; Δ ⊢ 𝑒 : 𝜏 ; Σ1       𝑥Û = FV(𝑒) ∪ dom(Σ1 )           Γ ; Δ ⊢ e1 : 𝜏1 ; Σ1        Γ, 𝑥 : 𝜏1 ; Δ + 0𝑥 ⊢ e2 : 𝜏2 ; Σ2
                             𝑥 ]𝜏 ; FP∞ (Û
       Γ ; Δ ⊢ return 𝑒 : [∅/Û           𝑥)                   Γ ; Δ ⊢ 𝑥 : 𝜏1 ← e1 ; e2 : [∅/𝑥]𝜏2 ; Σ1 + [∅/𝑥]Σ2

                          if
                          Γ ; Δ ⊢ 𝑒 1 : B ; Σ1       Γ ; Δ ⊢ e2 : 𝜏 ; Σ2  Γ ; Δ ⊢ e3 : 𝜏 ; Σ3
                                                                          ∞
                                Γ ; Δ ⊢ if 𝑒 1 then e2 else e3 : 𝜏 ; ⌉Σ1 ⌈ + (Σ2 ⊔ Σ3 )

         p-case
                                           Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1
         Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ e2 : 𝜏2 ; Σ2       Γ, 𝑦 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ12 ))𝑦 ⊢ e3 : 𝜏3 ; Σ3
                     Γ ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } :
                                  [Σ11 /𝑥]𝜏2 ⊔ [Σ12 /𝑦]𝜏3 ; ⌉Σ1 ⌈∞ ⊔ ([Σ11 /𝑥]Σ2 ⊔ [Σ12 /𝑦]Σ3 )

                        p-app
                                                 Σ
                     Γ ; Δ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑑) −→
                                                → 𝜏2 ; Σ1       Γ ; Δ ⊢ 𝑒 2 : 𝜏1 ; Σ2       Δ·Σ2 ≤ 𝑑
                                                                        ∞
                                      Γ ; Δ ⊢ e1 e2 : [Σ2 /𝑥]𝜏2 ; ⌉Σ1 ⌈ + [Σ2 /𝑥]Σ


                                                  FP∞ (∅) = ∅
                                                 FP∞ (Û
                                                      𝑥 , 𝑦) = FP∞ (Û
                                                                    𝑥 ) + ∞𝑦



                                 Fig. 13. 𝜆J : Type system of the privacy sublanguage


  ambient privacy eﬀect. For instance, consider the type derivation of program 𝑦 : R ← laplace𝜖1 𝑥 ;
  𝑧 : R ← laplace𝜖2 𝑥; return 𝑦 + 𝑧, similar to the example presented in Section 6.2, given an
  arbitrary relational distance environment 𝑥.
            bind
                                           Γ ; 𝑥 ⊢ laplace𝜖1 𝑥 : R ; (𝜖1 , 0)𝑥
              bind
                                   Γ, 𝑦 : R ; 𝑥 + 0𝑦 ⊢ laplace𝜖2 𝑥 : R ; (𝜖2, 0)𝑥
                         Γ, 𝑦 : R ; 𝑥 + 0𝑦 + 0𝑧 ⊢ return 𝑦 + 𝑧 : R ; (∞, 0)𝑦 + (∞, 0)𝑧
              Γ, 𝑦 : R ; 𝑥 + 0𝑦 ⊢ 𝑧 : R ← laplace𝜖2 𝑥; return 𝑦 + 𝑧 : R ; (𝜖2, 0)𝑥 + (∞, 0)𝑦
           Γ ; 𝑥 ⊢ 𝑦 : R ← laplace𝜖1 𝑥 ; 𝑧 : R ← laplace𝜖2 𝑥; return 𝑦 + 𝑧 : R ; (𝜖1 + 𝜖2, 0)𝑥
  Each laplace call has an eﬀect environment of (𝜖1, 0)𝑥 and (𝜖2, 0)𝑥 respectively. The return
  subexpression lifts to inﬁnite the privacy of variables 𝑦 and 𝑧, but to typecheck the innermost
  bind expression the privacy on 𝑧 is dropped: (𝜖2, 0)𝑥 + (∞, 0)𝑦. Then to typecheck the outer-
  most bind expression, now the privacy on 𝑦 is dropped getting a ﬁnal eﬀect environment of
  (𝜖1 , 0)𝑥 + (𝜖2 , 0)𝑥 = (𝜖1 + 𝜖2, 0)𝑥.
- Rule p-case is similar to rule s-case. Here we lift the ambient sensitivity eﬀect of the sum ex-
  pression to inﬁnity, i.e., we pay inﬁnity for all non-zero-sensitive variables used in 𝑒 1 . For the
  additional cost of each branch, we compute the join between the cost of each branch by sub-
  stituting each binder by their appropriated cost: [Σ11/𝑥]Σ2 for the ﬁrst branch, and [Σ12/𝑦]Σ3
  for the second. Note that we do not use [Σ1 + Σ11 /𝑥]Σ2 and [Σ1 + Σ12/𝑥]Σ3 as we do in rule

                                   ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
42                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


     s-case, because we are already lifting to inﬁnity (or paying for) every cost associated with Σ1 .
     For example, consider the following type derivation

           p-case
           Γ ; 𝑥 + 2𝑦 ⊢ 𝑥 : R 𝑦 ⊕∅ R ; 𝑥        Γ, 𝑥 1 : R ; 𝑥 + 2𝑦 + 3𝑥 1 ⊢ e2 : R ; 𝑝𝑥 𝑥 + 𝑝 𝑦 𝑦 + 𝑝 2𝑥 1
                             Γ, 𝑥 2 : R ; 𝑥 + 2𝑦 + 𝑥 2 ⊢ e3 : R ; 𝑝𝑥′ 𝑥 + 𝑝 𝑦′ 𝑦 + 𝑝 3𝑥 2
               Γ ; 𝑥 + 2𝑦 ⊢ case 𝑥 of {𝑥 1 ⇒ e2 } {𝑥 2 ⇒ e3 } :
                                  R ; ⌉𝑥 ⌈∞ ⊔ (𝑝𝑥 𝑥 + 𝑝 𝑦 𝑦 + ⌉𝑦 ⌈𝑝 2 ) ⊔ (𝑝𝑥′ 𝑥 + 𝑝 𝑦′ 𝑦 + ⌉∅⌈𝑝 3 )

  Note that the variation bound of 𝑥 1 is computed as (𝑥 + 2𝑦)·(𝑥 + 𝑦) = 3, and that of 𝑥 2 as (𝑥 +
  2𝑦)·(𝑥) = 1. As ⌉𝑥 ⌈∞ = ∞𝑥, ⌉𝑦 ⌈𝑝 2 = 𝑝 2𝑦, and ⌉∅⌈𝑝 3 = ∅, then the resulting eﬀect environment is
  ∞𝑥 ⊔ (𝑝𝑥 𝑥 + (𝑝 𝑦 + 𝑝 2 )𝑦) ⊔ (𝑝𝑥′ 𝑥 + 𝑝 𝑦′ 𝑦) = ∞𝑥 ⊔ ((𝑝 𝑦 + 𝑝 2 ) ⊔ 𝑝 𝑦′ )𝑦.
- Rule p-app uses the sensitivity type system to typecheck both subterms. The ﬁrst subterm has to
  be typed as a privacy function. Just as s-app, it checks that the sensitivity cost of the argument
  is bounded by 𝑑 by computing the dot operation Δ·Σ2 between relational distance environment
  Δ and sensitivity environment Σ2 . The resulting ambient privacy eﬀect is computed as the lift
  to inﬁnite of the ambient sensitivity eﬀect of 𝑒 1 , plus the latent contextual eﬀect of the privacy
  function, where we substitute Σ2 by 𝑥. Similarly to rule s-app, rule p-app also enforces that the
  relational distance of the argument is bounded by 𝑑, i.e. Δ·Σ2 ≤ 𝑑. For instance, consider the
  following type derivation:

       p-app
                                                       𝑝 1 𝑦⊔𝑝 2𝑥
       Γ ; 𝑦 ⊢ if 𝑦 then 𝑒 2 else 𝑒 3 : (𝑥 : R·4) −−−−−−→
                                                        → R ;𝑦                 Γ ; 𝑦 ⊢ 2 ∗ 𝑦 : R ; 2𝑦    2≤4
                                                                               ∞                𝑝2
                     Γ ; 𝑦 ⊢ (if 𝑦 then 𝑒 2 else 𝑒 3 }) (2 ∗ 𝑦) : R ; ⌉𝑦 ⌈ + (𝑝 1𝑦 ⊔ ⌉2𝑦 ⌈ )

     The resulting eﬀect environment is computed as ∞𝑦 + [2𝑦/𝑥](𝑝 1𝑦 ⊔ 𝑝 2𝑥) = ∞𝑦 + 𝑝 1𝑦 ⊔ ⌉2𝑦 ⌈𝑝 2 =
     ∞𝑦 + (𝑝 1 ⊔ 𝑝 2 )𝑦, which is equivalent to ∞𝑦. If 𝑦 does not wiggle, then the ambient privacy eﬀect
     will be zero. If the relational distance environment for 𝑦 were 3, then this program would be
     ill-typed since 3𝑦·2𝑦  4.

7.2 𝜆J : Type Safety
Type safety is deﬁned in the same line of Section 5.2. To establish type safety of the privacy lan-
guage, we deﬁne a non-deterministic sampling big-step semantics of privacy expressions; see Fig-
ure 14. We naturally extend the type safety logical relations of Figure 8 to support for both sensitiv-
ity and privacy lambdas, and privacy expressions as shown in Figure 15. The fundamental property
of the type safety logical relation is deﬁned similarly to Proposition 5.2, but now accounting for
relational distance environments and expressions:

     Proposition 7.1 (Fundamental Property of the Type Safety Logical Relation).
     (a) Let Γ; Δ ⊢ 𝑒 : 𝜏; Σ, and 𝛾 ∈ GJΓK. Then 𝛾 ⊢ 𝑒 ∈ EJ𝜏/ΓK.
     (b) Let Γ; Δ ⊢ e : 𝜏; Σ, and 𝛾 ∈ GJΓK. Then 𝛾 ⊢ e ∈ EJ𝜏/ΓK.

     Finally type safety for closed terms is just a corollary of the fundamental property above:

     Corollary 7.1 (Type Safety and Normalization of 𝜆J ).
     (a) Let ⊢ 𝑒 : 𝜏; ∅, then ⊢ 𝑒 ⇓ 𝑣, and ⊢ 𝑣 : 𝜏 ′; ∅, where 𝜏 ′ <: 𝜏.
     (b) Let ⊢ e : 𝜏; ∅, then ⊢ e ⇓ 𝑣, and ⊢ 𝑣 : 𝜏 ′ ; ∅, where 𝜏 ′ <: 𝜏.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                           43



         return                          bind                                                       gauss
            𝛾 ⊢𝑒 ⇓𝑣                      𝛾 ⊢ e1 ⇓ 𝑣 1          𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣 2                        𝑟 ∈R
         𝛾 ⊢ return 𝑒 ⇓ 𝑣                          𝛾 ⊢ 𝑥 : 𝜏 1 ← e1 ; e2 ⇓ 𝑣 2                      𝛾 ⊢ gauss 𝜇 𝜎 2 ⇓ 𝑟

                    if-true                                                   if-false
                     𝛾 ⊢ 𝑒 1 ⇓ true      𝛾 ⊢ e2 ⇓ 𝑣 2                          𝛾 ⊢ 𝑒 1 ⇓ false     𝛾 ⊢ e3 ⇓ 𝑣 3
                    𝛾 ⊢ if 𝑒 1 then e2 else e3 ⇓ 𝑣 2                       𝛾 ⊢ if 𝑒 1 then e2 else e3 ⇓ 𝑣 3

          case-left                                                      case-right
           𝛾 ⊢ e ⇓ inl 𝑣          𝛾[𝑥 ↦→ 𝑣] ⊢ e2 ⇓ 𝑣 2                    𝛾 ⊢ e ⇓ inr 𝑣          𝛾[𝑥 ↦→ 𝑣] ⊢ e3 ⇓ 𝑣 3
         𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓ 𝑣 2                        𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓ 𝑣 3

                          app        p
                          𝛾 ⊢ e1 ⇓ h𝜆 𝑥 : 𝜏·𝑠. e′, 𝛾 ′ i         𝛾 ⊢ e2 ⇓ 𝑣         𝛾 ′ [𝑥 ↦→ 𝑣] ⊢ e′ ⇓ 𝑣 ′
                                                            𝛾 ⊢ e1 e2 ⇓ 𝑣 ′




                      Fig. 14. Non-deterministic sampling semantics for privacy expressions



            s                                          𝑠𝑥
          h𝜆 𝑥 : 𝜏·𝑑 ′ .𝑒, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ·𝑑 ′) −−→ 𝜏2 K           ∀𝑣 ∈ VJ𝜏1 K.𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 ∈ EJ𝜏2 /(𝑥 : 𝜏1 )K
                                           s                                        𝑠𝑥
                                        h𝜆 𝑥 : 𝜏1 ·𝑑 .𝑒, 𝛾i ∈ VJ(𝑥 : 𝜏1 ·𝑑 ′) −−→ 𝜏2 K
                                                       ′


                p                                     Σ
                                                → 𝜏2 K
           h𝜆 𝑥 : 𝜏·𝑑.e, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ·𝑑) −→                    ∀𝑣 ∈ VJ𝜏1 K.𝛾[𝑥 ↦→ 𝑣] ⊢ e ∈ EJ𝜏2 /(𝑥 : 𝜏1 )K
                                               p                                    Σ
                                                                             → 𝜏2 K
                                         h𝜆 𝑥 : 𝜏1 ·𝑑.e, 𝛾i ∈ VJ(𝑥 : 𝜏1 ·𝑑) −→

                                                   ∀𝑣, 𝛾 ⊢ e ⇓ 𝑣 =⇒ 𝑣 ∈ VJ𝜏K
                                                            𝛾 ⊢ e ∈ EJ𝜏K




                               Fig. 15. 𝜆J : Type Safety Logical Relation (selected rules)


7.3   Soundness of 𝜆J : Metric Preservation
This section establishes the soundness of 𝜆J , named metric preservation. Metric preservation for 𝜆J
extends the notion of metric preservation of Sax. In addition to reasoning about sensitivity terms,
given a privacy term with free variables, we can reason about the achieved privacy level when
closing the privacy term under diﬀerent (but related) environments.
   Contrary to Sax, we establish soundness for 𝜆J using a step-indexed logical relation [3]. Although
𝜆J is a strongly-normalizing language, step indexing is still required to prove the bind case of the
fundamental property of the logical relation.
Probabilistic Semantics. A ﬁrst step to deﬁne the soundness property of 𝜆J is to endow privacy
expressions with a probabilistic semantics. An important observation here is that even though to
match their traditional (theoretical) presentation, we have introduced the Laplacian and Gaussian

                                   ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
44                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter



                                     return
                                                    𝛾 ⊢ 𝑒 ⇓𝑘 𝑣
                                                         ß
                                                           1   when    𝑥 =𝑣
                                    𝛾 ⊢ return 𝑒 ⇓𝑘 𝜆𝑥.
                                                           0 otherwise

                             bind
                             𝛾 ⊢ e1 ⇓𝑘 𝐷 1     ∀𝑣𝑖 ∈ Sup(𝐷 1 ), 𝛾[𝑥 ↦→ 𝑣𝑖 ] ⊢ e2 ⇓𝑘𝑖 𝐷 2𝑖
                                                                    Õ
                            𝛾 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 ⇓𝑘+max𝑖 𝑘𝑖 𝜆𝑥.             𝐷 1 (𝑣𝑖 )·𝐷 2𝑖 (𝑥)
                                                                   𝑣𝑖 ∈Sup(𝐷 1 )

                     app
                                   p
                     𝛾 ⊢ 𝑒 1 ⇓𝑘1 h𝜆 𝑥 : 𝜏·𝑠. e′, 𝛾 ′ i    𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑣      𝛾 ′ [𝑥 ↦→ 𝑣] ⊢ e′ ⇓𝑘3 𝐷
                                                  𝛾 ⊢ e1 e2 ⇓𝑘1 +𝑘2 +𝑘3 𝐷

                                    case-left
                                     𝛾 ⊢ 𝑒 ⇓𝑘1 inl 𝑣         𝛾[𝑥 ↦→ 𝑣] ⊢ e2 ⇓𝑘2 𝐷
                                    𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓𝑘1 +𝑘2 𝐷




                     Fig. 16. Probabilistic semantics of privacy expressions (selected rules)




mechanisms as sampling from the (uncountable) set of real numbers, for the formal account of the
language we consider discrete versions thereof over the set of integers [22]. This discretization is
not only a natural but also a necessary requirement for any implementation of the language (on
“ﬁnite” computers), since it is well-known that the naïve use of ﬁnite-precision approximations
may result in fatal privacy breaches [43]. (However, for the sake of uniformity, in the rest of the
presentation we refer to these mechanisms—at the type level—as operating over the set of real
numbers.) Therefore, privacy expressions in 𝜆J sample values only from discrete distributions and
can be interpreted as discrete distributions over values.
   The probabilistic semantics of a privacy expression e is formally deﬁned in Figure 16. Judgment
𝛾 ⊢ e ⇓𝑘 𝐷 denotes that privacy expression e reduces to distribution 𝐷 within 𝑘 steps; the proba-
bility that the privacy conﬁguration 𝛾 ⊢ e reduces to value 𝑣 is then computed as 𝐷(𝑣). We encode
discrete distributions 𝐷 as probability mass functions (PMF), i.e. a discrete distribution over 𝐴 is
                                                              Í
modeled as an element of the set D(𝐴) = {𝑓 : 𝐴 → [0, 1] | 𝑎 ∈𝐴 𝑓 (𝑎) = 1}.
   Let us brieﬂy explain the set of rules in Figure 16. For simplicity, we omit the underlying step
indices. The probabilistic semantics of return 𝑒 assigns probability 1 to the (necessarily unique)
value to which expression 𝑒 reduces. The probabilistic semantics of a bind 𝑦 : 𝜏1 ← e1 ; e2 operates
as follows: To compute the probability that it assigns to 𝑥, it ranges over the set of values in the
support of 𝐷 1 denoted as Sup(𝐷 1 ), i.e. the set of values 𝑣 such that 𝐷 1 (𝑣) > 0, and for each 𝑣 𝑖 ∈
Sup(𝐷 1 ) it sums the product between the probability that e1 reduces to 𝑣 𝑖 with the probability that
e2 reduces to 𝑥 in an extended environment where 𝑦 is bound to 𝑣 𝑖 . The discrete Gauss distribution
                                                                         2    2
with mean 𝜇 and scale 𝜎 2 assigns probability proportional to 𝑒 −(𝑥 −𝜇) /2𝜎 to each integer 𝑥. The
probabilistic semantics of a privacy application is deﬁned as the probabilistic semantics of the body
of the resulting privacy closure, in an extended environment where the closure formal argument
is bound to the value of the real argument. Finally, the probabilistic semantics of a case term is

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                          45



                                                          △
                                (𝑟 1, 𝑟 2 ) ∈ V𝑑𝑘 JRK ⇐⇒ |𝑟 1 − 𝑟 2 | ≤ 𝑑
                                                          △
                           (𝑣 1 , 𝑣 2 ) ∈ V𝑑𝑘 JunitK ⇐⇒ 𝑣 1 = tt ∧ 𝑣 2 = tt
                                                          △
       (inl 𝑣 1 , inl 𝑣 2 ) ∈ V𝑑𝑘 J𝜎1 𝑑 1 ⊕𝑑 2 𝜎2 K ⇐⇒ (𝑣 1 , 𝑣 2 ) ∈ V𝑑+𝑑
                                                                       𝑘 J𝜎 K
                                                                           1        1
                                                          △
       (inr 𝑣 1 , inr 𝑣 2 ) ∈ V𝑑𝑘 J𝜎1 𝑑 1 ⊕𝑑 2 𝜎2 K ⇐⇒ (𝑣 1 , 𝑣 2 ) ∈ V𝑑+𝑑
                                                                       𝑘 J𝜎 K
                                                                           2
                                                                                    2
                                                          △
  ((𝑣 11 , 𝑣 12 ), (𝑣 21 , 𝑣 22 )) ∈ V𝑑𝑘 J𝜎1 𝑑 1 &𝑑 2 𝜎2 K ⇐⇒ ∃𝑑 1′ , 𝑑 2′ , 𝑑 = 𝑑 1′ ⊔ 𝑑 2′ ∧
                                                              (𝑣 11 , 𝑣 21 ) ∈ V𝑑𝑘 +𝑑 ′ J𝜎1 K ∧ (𝑣 12 , 𝑣 22 ) ∈ V𝑑𝑘 +𝑑 ′ J𝜎2 K
                                                                                   1    1                            2       2
                                                          △
 (h𝑣 11 , 𝑣 12 i, h𝑣 21 , 𝑣 22 i) ∈ V𝑑𝑘 J𝜎1 𝑑 1 ⊗𝑑 2 𝜎2 K ⇐⇒ ∃𝑑 1′ , 𝑑 2′ , 𝑑 = 𝑑 1′ + 𝑑 2′ ∧
                                                             (𝑣 11 , 𝑣 21 ) ∈ V𝑑𝑘 +𝑑 ′ J𝜎1 K ∧ (𝑣 12 , 𝑣 22 ) ∈ V𝑑𝑘 +𝑑 ′ J𝜎2 K
                                                                                   1    1                            2       2
                                           Δ·Σ            △                                                              𝑗
          (𝑣 1 , 𝑣 2 ) ∈ V𝑑𝑘 J(𝑥 : 𝜎1 ·𝑑 ′ ) −−−→ 𝜎2 K ⇐⇒ ∀𝑣 1′ , 𝑣 2′ , 𝛾 1, 𝛾 2 , 𝑗 < 𝑘, 𝑑 ′′ ≤ 𝑑 ′, (𝑣 1′ , 𝑣 2′ ) ∈ V𝑑 ′′ J𝜎1 K =⇒
                                                                                                   𝑗
                                                          (𝛾 1 ⊢ 𝑣 1 𝑣 1′ , 𝛾 2 ⊢ 𝑣 2 𝑣 2′ ) ∈ E𝑑 +(Δ+𝑑 ′′𝑥)·Σ J𝑑 ′′𝑥(𝜎2 )K
                                          Δ•Σ             △                                                              𝑗
         (𝑣 1 , 𝑣 2 ) ∈ V𝑑𝑘 J(𝑥 : 𝜎1 ·𝑑 ′) −−−→
                                              → 𝜎2 K ⇐⇒ ∀𝑣 1′ , 𝑣 2′ , 𝛾 1, 𝛾 2 , 𝑗 < 𝑘, 𝑑 ′′ < 𝑑 ′, (𝑣 1′ , 𝑣 2′ ) ∈ V𝑑 ′′ J𝜎1 K =⇒
                                                                                                 𝑗
                                                        (𝛾 1 ⊢ 𝑣 1 𝑣 2′ , 𝛾 2 ⊢ 𝑣 1 𝑣 2′ ) ∈ E ⌉𝑑 ⌈∞ +(Δ+𝑑 ′′𝑥)•Σ J𝑑 ′′𝑥(𝜎2 )K
                                                          △
                     (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑𝑘 J𝜎K ⇐⇒ ∀𝑗 < 𝑘, ∀𝑣 1, (𝑑 < ∞ ∧ 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗 𝑣 1 ) =⇒
                                                                                                     𝑘−𝑗
                                                          ∃𝑣 2 , (𝛾 2 ⊢ 𝑒 2 ⇓∗ 𝑣 2 ∧ (𝑣 1 , 𝑣 2 ) ∈ V𝑑 J𝜎K)
                                                          △
                    (𝛾 1 ⊢ e1, 𝛾 2 ⊢ e2 ) ∈ E𝑝𝑘 J𝜎K ⇐⇒ ∀𝑗 < 𝑘, ∀𝐷 1, (𝑝.𝜖 + 𝑝.𝛿 < ∞ ∧ 𝛾 1 ⊢ e1 ⇓ 𝑗 𝐷 1 ) =⇒ ∃𝐷 2,
                                                       (𝛾 2 ⊢ e2 ⇓∗ 𝐷 2 ∧ ∀𝑆 ⊆ 𝑣𝑎𝑙(∗), 𝐷 1 (𝑆) ≤ 𝑒 𝑝.𝜖 𝐷 2 (𝑆) + 𝑝.𝛿)
                                                          △
                                 (𝛾 1 , 𝛾 2 ) ∈ GΔ𝑘 JΓK ⇐⇒ 𝑑𝑜𝑚(𝛾 1 ) = 𝑑𝑜𝑚(𝛾 2 ) = 𝑑𝑜𝑚(Γ)∧
                                                                                              𝑘 JΔ(Γ(𝑥))K
                                                           ∀𝑥 ∈ dom(Γ). (𝛾 1 (𝑥), 𝛾 2 (𝑥)) ∈ VΔ(𝑥)



                                    Fig. 17. 𝜆J : logical relations for metric preservation




simply the probabilistic semantics of the corresponding branch in an extended environment with
the corresponding association for the branch binder variable.
   We consider a step-indexed semantics to establish the language metatheory. In particular, the
metric preservation theorem is proved by induction on the step index of the logical relation. How-
ever, step indices might not interact very well with the bind rule: when reducing 𝑦 : 𝜏1 ← e1 ; e2
, the reduction of e2 requires a possibly diﬀerent number of steps (𝑘𝑖 ) for each value (𝑣 𝑖 ) to which
e1 reduces. This set of steps could in principle be unbounded, making max𝑖 𝑘𝑖 undeﬁned and thus
rendering the semantics partial. However, this is not an issue for our technical development be-
cause all formal results are concerned with programs that reach the distribution of ﬁnal values
within a ﬁnite number of steps, only.
   For convenience throughout this section, we also introduce 𝐷(𝑆) to denote the probability of
                                 Í                                                               ′
observing 𝑆 in 𝐷, computed as 𝑣 ∈𝑆 𝐷(𝑣). Also we deﬁne Pr[∅ ⊢ e ⇓𝑘 𝑣] as 𝐷(𝑣) if ∅ ⊢ e ⇓𝑘 𝐷 for
        ′
some 𝑘 ≤ 𝑘 (undeﬁned otherwise).

Logical relation. The logical relations for sensitivity computations, privacy computations, values,
and environments are mutually recursive and presented in Figure 17.

                                      ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
46                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


  Note that each logical relation is also indexed by a relational distance type that now accounts
for sensitivity and privacy lambdas:
                                                          Σ+𝑑                   Σ
                                     𝜎 = ... | (𝑥 : 𝜎·𝑑) −−−→ 𝜎 | (𝑥 : 𝜎·𝑠) −
                                                                            →→𝜎
                                     Σ = ... | 𝑝
Note that similarly to sensitivity environments, privacy environments Σ are also extended to in-
clude partially instantiated data, for instance 𝑝𝑥 +𝑝 ′. Notation (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑘 J𝜎K indicates that value
𝑣 1 is related to 𝑣 2 at type 𝜎 and distance 𝑑 for 𝑘 steps.
    The sensitivity parts of the logical relations are deﬁned analogously to Figure 8 with the addition
of a step index 𝑘. We only present relevant changes:
- Two sensitivity closures are also related if, given related inputs, they produce related computa-
   tions. Speciﬁcally, ﬁrst the environments have to be related for any step 𝑗 < 𝑘. Second, inputs 𝑣 1′
   and 𝑣 2′ have to be related at distance 𝑑 ′′ not greater than 𝑑, and for 𝑗 steps. Finally, the bodies of
   the functions in extended environments have to be related computations for 𝑗 steps.
- Similarly to sensitivity closures, two privacy closures are related if they produce related compu-
   tations when applied to related inputs. The computations are related at privacy ⌉𝑑 ⌈∞ +(Δ+𝑑 ′′𝑥)•Σ.
   Note that we lift 𝑑 to inﬁnite because we cannot record relational distances as a privacy result.
   In addition to that, we also pay the latent contextual eﬀect of the function instantiated to 𝑑 ′′𝑥,
   i.e. (Δ + 𝑑 ′′𝑥)•Σ.
    Two sensitivity conﬁgurations are related computations at type 𝜎 and distance 𝑑 for 𝑘 steps,
noted (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑𝑘 J𝜎K, when for any 𝑗 < 𝑘, if the ﬁrst conﬁguration reduces in 𝑗 steps to
a value, then the second conﬁguration also reduces to a value in any number of steps, and these
values are related for the remaining 𝑘 − 𝑗 steps at type 𝜎 and distance 𝑑. We write 𝛾 ⊢ 𝑒 ⇓𝑘 𝑣 to
say that the conﬁguration 𝛾 ⊢ 𝑒 reduces to value 𝑣 in 𝑘 steps.
    We now turn to the deﬁnition of related privacy computations. Notation (𝛾 1 ⊢ e1, 𝛾 2 ⊢ e2 ) ∈
   𝑘
E𝑝 J𝜎K indicates that two privacy conﬁgurations are related computations at type 𝜎 and privacy
𝑝 = (𝜖, 𝛿) for 𝑘 steps. Two privacy conﬁgurations are related when, for any 𝑗 < 𝑘, if the ﬁrst privacy
conﬁguration reduces in 𝑗 steps to a distribution, then the second conﬁguration also reduces to a
distribution in any number of steps, and the probability of observing 𝑆 in the ﬁst distribution is
no greater than 𝑒 𝜖 times the probability of observing 𝑆 in the second distribution, plus 𝛿.
  Metric Preservation. Armed with these logical relations, we can establish the notion of type
soundness for 𝜆J , and prove the fundamental property.
     Theorem 7.2 (Metric Preservation).
     (1) Γ, Δ ⊢ 𝑒 : 𝜏 ; Σ ⇒ ∀𝑘 ≥ 0, ∀Δ ′ ⊑ Δ, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK.(𝛾 1 ⊢ 𝑒, 𝛾 2 ⊢ 𝑒) ∈ E 𝑘Δ′ ·Σ JΔ ′(𝜏)K
     (2) Γ, Δ ⊢ e : 𝜏 ; Σ ⇒ ∀𝑘 ≥ 0, ∀Δ ′ ⊑ Δ, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK.(𝛾 1 ⊢ e, 𝛾 2 ⊢ e) ∈ E Δ𝑘 ′ Σ JΔ ′(𝜏)K
                                                                                                  •



     where Δ ′ ⊑ Δ    ⇐⇒          𝑑𝑜𝑚(Δ ′) = 𝑑𝑜𝑚(Δ) ∧ ∀𝑥          ∈ 𝑑𝑜𝑚(Δ ′), Δ ′(𝑥) ≤ Δ(𝑥). The theorem says
that if a sensitivity term (resp. privacy term) is well-typed, then for any number of steps 𝑘, valid
relational distance environment Δ ′ (not greater than Δ) and value environments (𝛾 1, 𝛾 2 ), the two
conﬁgurations are related computations at distance type Δ ′(𝜏) (closing all free sensitivity or privacy
variables), and at relational distance Δ ′ ·Σ (resp. Δ ′ •Σ). Note that as 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Δ ′) = 𝑑𝑜𝑚(Δ)
and 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Δ ′) = 𝑑𝑜𝑚(Δ), then Δ ′ ·Σ ∈ R∞ and Δ ′•Σ ∈ 𝑝𝑟𝑖𝑣.
   To prove the fundamental property, we rely on the following three lemmas which connect types,
sensitivity and privacy environments from the type system, with distances and privacy costs from
the logical relations:
     Lemma 7.3. If Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ·([Σ/𝑥]Σ ′) = (Δ + 𝑑𝑥)·Σ ′

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       47


  Lemma 7.4. If Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ•([Σ/𝑥]Σ′) = (Δ + 𝑑𝑥)•Σ′

  Lemma 7.5. Let Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ([Σ/𝑥]𝜏) = 𝑑𝑥(Δ(𝜏))
  We can also derive from the fundamental property some corollaries about closed terms.
  Corollary 7.6 (FP for closed sensitivity terms). If ∅; ∅ ⊢ 𝑒 : 𝜏 ; ∅, then
∀𝑘 ≥ 0, (∅ ⊢ 𝑒, ∅ ⊢ 𝑒) ∈ E0𝑘 J𝜏K
  Corollary 7.7 (FP for closed privacy terms). If ∅; ∅ ⊢ e : 𝜏 ; ∅, then
∀𝑘 ≥ 0, (∅ ⊢ e, ∅ ⊢ e) ∈ E(𝑘0,0 ) J𝜏K

  In addition to sensitivity type soundness at base types (Prop 5.3), from the fundamental property
we can now establish privacy type soundness at base types:
                                                                                                  (𝜖,𝛿)𝑥
    Theorem 7.8 (Privacy Type Soundness at Base Types). If ∅ ⊢ 𝑒 : (𝑥 : R·1) −−−−→
                                                                                 → R ; ∅,
|𝑟 1 − 𝑟 2 | ≤ 1, ∀𝑟 , Pr[∅ ⊢ e 𝑟 1 ⇓∞ 𝑟 ] ≤ 𝑒 𝜖 Pr[∅ ⊢ e 𝑟 2 ⇓∞ 𝑟 ] + 𝛿
   Finally, we observe that our technical development relies on the speciﬁc variant of diﬀerential
privacy considered in restricted places: the bind case of the soundness theorem (Theorem C.17);
the deﬁnition of subtyping for privacy costs, specially the base case (Figure 23); operations over
privacies 𝑝, such as dot product, addition, meet, join, lifting (Figures 25 and 26); monotonicity
of meet and join of privacies w.r.t subtyping (Lemmas C.7 and C.8); monotonicity of dot product
w.r.t. privacy ordering (Lemma C.13); distributivity of dot product w.r.t. substitution (Lemma 7.4);
weakening of related private computations (Lemma C.10). The remaining deﬁnitions and lemmas
are independent and could be reused as such in order to adapt this work to deal with other variants
of diﬀerential privacy.

8 FROM 𝜆J TO JAZZ
The full prototype implementation of Jazz includes several extensions to the core language 𝜆J , and
address the non-determinism of multiplicative and additive products by using type annotations.
   Type Polymorphism. Jazz implements System F (universal quantiﬁcation over well-kinded types)
and parametric polymorphism over all compound types, including vector/matrix schemas, allow-
ing all data objects and functions in the language to be fully generic. This feature requires the use
of type-level quantiﬁers and application.
   Value Dependency. Jazz supports type-level dependency on values through singleton types—
an approach we borrow directly from DFuzz [34]. This allows diﬀerentially private algorithms
to be veriﬁed with respect to privacy parameters which are not ﬁxed, and instead are function
arguments.
   More speciﬁcally, singleton types [33] are a technique for supporting limited forms of value
dependency which builds on standard (System-F-style) polymorphic type system features and an
enriched kind system. In a type system with native support for dependent types, a dependent
function with a real-valued argument is written (𝑥 : R) → 𝜏 where the return type 𝜏 can use 𝑥 to
refer symbolically to the eventual runtime value of 𝑥. In a singleton type encoding of dependent
types, the same function is written 𝑥 : R[𝑥]   ˆ → 𝜏, where the return type 𝜏 can use 𝑥ˆ to refer
symbolically to the eventual runtime value of 𝑥. In essence, there is still a syntactic split between
term-level variables (𝑥) and type-level variables (𝑥),
                                                    ˆ and the type declaration (𝑥 : R[𝑥])
                                                                                       ˆ links them,
so 𝑥ˆ is the type-level proxy for the term-level variable 𝑥.

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
48                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


  Let-binding Sensitivity Terms in Privacy Contexts. As described in Section 6.2 we implement la-
tent sensitivity via local bindings in the privacy language. We implement this feature using an
environment Φ to delay the “payments” of a value’s sensitivity, which fulﬁlls the same role as the
boxed type introduced by Near et al. [46]. Unlike boxed types, this feature requires no additional
annotations—sensitivity is inferred automatically. The complete type systems that includes Φ are
presented in Appendix A, Figures 19 and 20.
   Context Polymorphism. When implementing ﬂexible primitives in Jazz, it becomes convenient
to abstract over latent contextual eﬀects. We label this form of abstraction as context polymor-
phism. This form of polymorphism in our language is what enables us to give a single generalized
type to the primitives gauss and seqloop (a looping combinator that uses sequential composition,
further discussed in Section 9.2). Because Jazz implements quantiﬁcation over latent contextual
eﬀects, it is possible to aﬀord privacy in type signatures to closed-over variables involved in the
diﬀerentially private computation. This feature requires the use of type-level quantiﬁers, appli-
cation, substitution and annotations for context schemas. A context schema is an angle bracket
enclosed list of variables. Angle bracket context schemas in Jazz denote the set of variables that
we care about preserving privacy for, and are used in the introduction forms for sums, pairs, and
functions, as well as in type-level application. For example, gauss <𝑥> (𝑥 + 𝑦 * 𝑦) is 1-sensitive in
𝑥, and bumps 𝑦 to inﬁnity privacy. This demonstrates the use of context polymorphism to indicate
which variables we care about preserving privacy for. The use of seqloop in Section 9 provides
another example of context polymorphism in action. Note that context-polymorphic functions in
Jazz are required to be primitives.
  Variants of Diﬀerential Privacy. In addition to (𝜖, 𝛿)-diﬀerential privacy, Jazz supports zero-concentrated
diﬀerential privacy [21] and Rényi diﬀerential privacy [44], and has built-in constructs for mixing
the variants. Each variant has diﬀerent privacy parameters and rules for composition, but all of
them follow the same basic pattern as (𝜖, 𝛿)-diﬀerential privacy. For example, we can give the
Gaussian mechanism the following types for Rényi diﬀerential privacy (RDP; privacy parameters
𝛼 and 𝜖) and zero-concentrated diﬀerential privacy (zCDP; privacy parameter 𝜌):
  RDP                                                                             ∞(𝑑+𝛼 +𝜖)+(𝛼,
                                                                                             ˆ 𝜖)𝑥
                                                                                                ˆ
gauss : ∀ (𝑑ˆ : R) (𝛼ˆ : R) (𝜖ˆ : R). (𝑑 : R[𝑑])
                                             ˆ → (𝛼 : R[𝛼])
                                                        ˆ → (𝜖 : R[𝜖])         ˆ −−
                                                                    ˆ → (𝑥 : R·𝑑)  −−−−−−−−−−−→   →R
 zCDP                                                           ∞(𝑑+𝜌)+𝜌𝑥
                                                                       ˆ
            ˆ                         ˆ
gauss : ∀ (𝑑 : R) (𝜌ˆ : R). (𝑑 : R[𝑑]) → (𝜌 : R[𝜌])         ˆ
                                                 ˆ → (𝑥 : R·𝑑) −−−−−−−−→ →R

  Since RDP and zCDP guarantees can be converted to (𝜖, 𝛿) guarantees, Jazz provides constructs
for converting between variants. For example, the following code uses the Gaussian mechanism
twice, each time satisfying (20, 0.25)-RDP. By sequential composition, the total cost is (20, 0.5)-RDP.
The program then converts this guarantee to (𝜖, 𝛿)-diﬀerential privacy, using 𝛿 = 10−5 .
         p
        𝜆 (𝑥 ·1). RENYI[𝛿 = 10−5 ]{ 𝑟 1 ← gauss 1 20 0.25 𝑥;
                                                                                               (1.08,10−5 )𝑥
                                    𝑟 2 ← gauss 2 20 0.25 (𝑥 + 𝑥);                :    (𝑥 : R·1) −−−−−−−−→
                                                                                                         →R
                                    return (𝑟 1 + 𝑟 2 ) }
Jazz automatically ﬁnds the privacy cost of this function, in (𝜖, 𝛿)-diﬀerential privacy, by perform-
ing the appropriate conversion. The ability to mix privacy variants in Jazz makes it easy to frame
the privacy guarantee of any program in terms of (𝜖, 𝛿) privacy cost, allowing privacy costs to be
directly compared. In addition, it enables embedding iterative RDP and zCDP algorithms inside of
(𝜖, 𝛿) programs, allowing these programs to take advantage of the improved composition properties
RDP and zCDP provide. This approach—leveraging recent variants for composition, but reporting
privacy costs in terms of 𝜖 and 𝛿—is extremely common in recent work on diﬀerentially private
machine learning [2]. We make extensive use of variant-mixing in our case studies, described next.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       49


9 IMPLEMENTATION & CASE STUDIES
Jazz enables programmers to implement and verify largely the same set of applications as Duet,
but Jazz empowers the programmer to construct these applications in simpler ways, e.g., via com-
position of reusable library functions. This is possible because Jazz gives types to many privacy
functions and looping combinators that required custom typing rules in Duet. Our case stud-
ies demonstrate that instead of encoding these applications as a single monolithic function, Jazz
enables their implementation through composition of multiple helper functions, and their veriﬁ-
cation without the use of custom typing rules.
   In particular, we highlight two important features of Jazz that enable refactoring programs to
reuse library functions:
    • Jazz gives types to privacy primitives and looping combinators that are not typeable in Duet,
       enabling privacy functions to be parameterized by these components (see Section 9.2).
    • Jazz’s privacy functions allow sensitivity arguments with arbitrary sensitivity bounds, en-
       abling code reuse in more places than Duet’s sensitivity-1 privacy functions (see Section 9.3).
In addition, we select realistic algorithms previously veriﬁed using other systems, to demonstrate
that Jazz maintains the capabilities of previous work.
   A summary of our case study programs appears in Table 3. We present two new representative
case study algorithms we have implemented and veriﬁed using Jazz: the MWEM algorithm [38]
for a workload of linear queries, and a recently proposed algorithm for diﬀerentially private deep
learning with adaptive clipping [53]. In both case studies, privacy mechanisms (e.g. laplace and
exponential) and looping constructs (e.g. aloop—advanced composition) can be expressed with
regular functions, provided in a library of primitives. We mark these two case studies with a ∗
in Table 3, and describe them in detail later in this section. The other case study programs are
available in our source code repository.

9.1   Implementation
We have implemented a prototype of the Jazz typechecker in Haskell, and used it to verify the
case studies from Table 3. The prototype implementation is available on GitHub7 . Table 3 lists the
time needed to typecheck each of the case studies; our typechecker takes just a few milliseconds
for each one.
   Type inference & annotations. Our prototype implements type inference for both Sax and Jazz.
Type annotations for sensitivity and privacy are required for inputs at top-level functions and
lambda-expressions, but no additional annotations are required for function outputs or elsewhere
in the program. The case studies described later in this section have been typeset for readability,
but are otherwise identical to the input for our prototype; in particular, the actual examples type-
checked by our prototype have the same annotations as the examples in this section, except for
the input sensitivity annotations on inputs to top-level functions. The types given for primitives
in this section are also drawn directly from our implementation.
   Constraint solving. As described earlier, and detailed in Section 10, prior work has made exten-
sive use of SMT solvers for the equations over real expressions which arise in type inference for
sensitivity. Because SMT solvers are incomplete for non-linear operations (like the logarithms and
square roots used in advanced composition), our implementation does not follow the same path.
   Instead, we implement a custom solver for inequalities over symbolic real expressions, based
on the solver from Duet [46]. Our custom solver is based on a simple decidable (but incomplete)
theory; it supports logarithms, square roots, and polynomial formulas over real numbers. The
7 https://github.com/uvm-plaid/contextual-duet/



                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
50                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


                                                                                              Typecheck
        Technique                                            Ref.   Privacy Concept           Time
        Machine Learning Algorithms
        Noisy Gradient Descent                               [18]   Composition               4.1 ms
        Gradient Descent w/ Output Perturbation              [56]   Parallel comp. (sens.)    4.2 ms
        Noisy Frank-Wolfe                                    [52]   Exponential mechanism     5.9 ms
        Variations on Gradient Descent
        Minibatching                                         [18]   Privacy ampliﬁcation      5.5 ms
        Parallel-composition minibatching                    —      Parallel composition      5.9 ms
        Gradient clipping                                    [2]    Sensitivity bounds        4.5 ms
        Adaptive gradient clipping∗ (§9.3)                   [53]   Advanced variants         5.6 ms
        Preprocessing & Deployment
        Hyperparameter tuning                                [23]   Exponential mechanism     6.9 ms
        Adaptive clipping                                    —      Sparse Vector Technique   7.7 ms
        Z-Score normalization                                [1]    Composition               6.9 ms
        Algorithms for Linear Queries
        Multiplicative Weights (MWEM)∗ (§9.2)                [38]   Exponential mechanism     5.2 ms

Table 3. List of case studies included with the Jazz implementation. Case studies marked with a ∗ are de-
scribed in detail in this section.




solver is transparent to the programmer, and produces readable output expressions for the privacy
costs in our case studies.

9.2    MWEM
The MWEM algorithm [38] generates diﬀerentially private synthetic data approximating the target
sensitive data by iteratively optimizing the accuracy of a set of workload queries on the synthetic
data. In each iteration, the algorithm uses the exponential mechanism to pick a query from the
workload for which the synthetic data produces an inaccurate result, uses the Laplace mechanism
to run that query on the real data, and uses the result to update the synthetic data via the multi-
plicative weights update rule. The Jazz program shown below implements the MWEM algorithm.
Its inputs are a sensitive dataset 𝑋 over a domain 𝐷, a workload 𝑄 of linear queries, the number of
iterations to be performed 𝑘, the privacy parameter 𝜖, initial synthetic data 𝑌0 (𝑛 times the uniform
distribution over 𝐷), and the dimensions of the input data set (matrix) 𝑚 rows by 𝑛 columns. The
algorithm performs 𝑘 iterations, invoking laplace and exponential in each iteration. The privacy
parameter for each invocation is 𝜖/2𝑘, yielding a total privacy cost of 𝜖. We omit the sensitivity
annotations on the function’s inputs for readability.

                            s    s     s     s     s     s          p
             MWEM , 𝜆 𝑛. 𝜆 𝑘. 𝜆 𝜖. 𝜆 𝑋 . 𝜆 𝑄. 𝜆 loop. 𝜆 𝑌0 .
                                p
              loop 𝑘 𝑌0 <𝑋 > (𝜆 𝐴𝑖−1 .
                                                             s       s
                𝑞𝑖 Index ← exponential (𝜖 / (2 ∗ 𝑘)) 𝑄 𝑋 (𝜆 𝑋 ′ . 𝜆 𝑞 ′ . |𝑞 ′ 𝐴𝑖−1 − 𝑞 ′ 𝑋 ′ |);
                let 𝑞𝑖 = matrixIndex 𝑄 (index N[0]) 𝑞𝑖 Index in
                𝑚𝑖 ← laplace 1 (𝜖 / (2 ∗ 𝑘)) (𝑞𝑖 𝑋 );
                                               s
                return mmap-row 𝑋 𝐴𝑖−1 (𝜆 𝑥 .
                    mScale 𝑥 (exp (𝑞𝑖 𝑥 ∗ (𝑚𝑖 − 𝑞𝑖 𝐴𝑖−1 / (2 ∗ 𝑛))))))

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                  51


The Jazz typechecker produces the following type for this implementation, indicating that the
algorithm satisﬁes 𝜖-diﬀerential privacy. Note the homogenous matrix type notation used here
is M[𝑚, 𝑛] 𝜏 where 𝑚 denotes the number of rows, 𝑛 the number of columns, and 𝜏 the type of
each entry. <𝑋 > is the context schema argument for type-application of loop, and indicates the
program variable we want to preserve privacy for in this expression.
                                                                         columns           iterations   relational distance

  MWEM : ∀ (𝑚ˆ : N) (𝑛ˆ : N) (𝑘ˆ : N) (𝑑ˆ : R+ ) (𝜖ˆ : R+ ). (𝑛 : N[𝑛])        ˆ → (𝑑 : R+ [𝑑])
                                                                    ˆ → (𝑘 : N[𝑘])          ˆ
       desired privacy              sensitive data                      linear queries                    initial synthetic db
                                                                 𝑥𝑠
                +
     → (𝜖 : R [𝜖])
               ˆ → (𝑋 : (M[𝑚,
                           ˆ 𝑛]    ˆ → (𝑄 : List ((𝑥𝑠 : M[1, 𝑛])
                              ˆ D)·𝑑)                        ˆ −−→ N)) → (𝑌0 : M[𝑚,
                                                                                 ˆ 𝑛]
                                                                                    ˆ D)
                                privacy eﬀect
   looping combinator                                          synthetic db
               ∞(𝑛 + 𝑘 + 𝜖 + 𝑄 + 𝑌0 ) + (𝜖,
                                          ˆ 0)𝑋
   → (𝜏loop ) −−−−−−−−−−−−−−−−−−−−−−−−−−−−−→   → M[𝑚, ˆ 𝑛] ˆ R
  where 𝜏loop = ∀ (𝑘 : N) (𝑑 : R ) (𝜖ˆ : R ) (𝛿 : R ) (𝜖ˆ : R+ ) (𝛿ˆ′ : R+ ) (Γ : cxt).
                    ˆ       ˆ   +         +   ˆ    +     ′

                                                                              (𝜖, ˆ
                                                                               ˆ 𝛿)Γ
                                   ˆ → (𝑋 : 𝜏 ·𝑑)
                            (𝑘 : N[𝑘])         ˆ → (𝑓 : (𝑥 : 𝜏 ·𝑑ˆ −−−−→
                                                                       → 𝜏))
                                     ∞(𝑘+𝑑+𝑓 )+(𝜖ˆ′,𝛿ˆ′ )Γ
                                    −−−−−−−−−−−−−−→
                                                  →𝜏
On an average of 10 runs, it takes the Jazz typechecker 5.2ms to produce this type for the MWEM
algorithm.
   Beyond Duet. This example demonstrates Jazz’s ability to deﬁne algorithms in terms of library
functions, and to parameterize algorithms by the choice of component pieces. In this case, we
deﬁne MWEM in terms of a generic looping privacy combinator loop; the caller of MWEM can specify
looping combinators based on sequential composition, advanced composition, or even a custom
combinator. Jazz similarly allows functions like MWEM to be parameterized by the choice of basic
mechanism (e.g. laplace vs. gauss) with the appropriate privacy function type. In both cases, the
relevant functions can be pulled from libraries or deﬁned by the programmer.
   This kind of modularity is impossible in Duet. Functions cannot be parameterized by basic
privacy mechanisms or looping combinators, because it is not possible to write their types in
Duet.
   Primitives used. This case study demonstrates the composition of a complex iterative algorithm
from basic privacy mechanisms encoded as Jazz primitives (e.g. laplace and exponential) and pri-
vacy combinators (e.g. seqloop, which implements looping with sequential composition for pri-
vacy). These primitives with types shown above would require explicit typing rules in the core
Duet language. In Jazz, they can be given regular types, as shown below:
                                                                                         relational distance desired privacy

   exponential : ∀ (𝑚ˆ : N) (𝑛ˆ : N) (𝑑ˆ : R+ ) (𝜖ˆ : R+ ) (Γ : cxt) (𝜏 : ⋆).                       ˆ → (𝜖 : R+ [𝜖])
                                                                                           (𝑑 : R+ [𝑑])          ˆ
                                                                                       scoring function
                         linear queries                      sensitive data
                                                                                                  ˆ
      → (𝑄 : List ((𝑥𝑠 : M[1, 𝑛])
                                  𝑥𝑠
                                                        ˆ → (𝜙 : (𝑥 : 𝜏) −𝑑(𝑥+Γ)
                              ˆ −−→ N)) → (𝑋 : (List 𝜏)·𝑑)                −−−−→ R)
                    privacy eﬀect
      ∞(𝑑 + 𝜖 + 𝑄 + 𝜙) + (𝜖,  ˆ 0)(𝑋 + Γ)
     −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−→      →𝜏
   seqloop : ∀ (𝑘ˆ : N) (𝑑ˆ : R+ ) (𝜖ˆ : R+ ) (𝛿ˆ : R+ ) (Γ : cxt). (𝑘 : N[𝑘])
                                                                           ˆ → (𝑑 : R+ [𝑑])
                                                                                        ˆ → (𝜖 : R+ [𝜖])
                                                                                                     ˆ
                                                                                ˆ
      → (𝛿 : R+ [𝛿])               ˆ → (𝑓 : (𝑥 : List R·𝑑ˆ −(−𝜖,ˆ−𝛿)Γ
                 ˆ → (𝑋 : (List R)·𝑑)                             −→→ List R))
       ∞(𝑘+𝑑+𝜖+𝛿+𝑓 )+(𝑘ˆ 𝜖,
                         ˆ 𝑘ˆ 𝛿)Γ
                              ˆ
                        → List R
      −−−−−−−−−−−−−−−−−−→

                                     ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
52                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter

                                                                                                    p
To typecheck MWEM, the privacy closure rule in Jazz creates a function type for the 𝜆 which has a
privacy eﬀect for the body of 𝑘𝜖 because of the two uses of mechanisms which give 2𝑘 𝜖
                                                                                       diﬀerential
privacy. If we pass seqloop as the looping combinator loop, then this privacy eﬀect is multiplied
                                                                                                ⌉Σ ⌈𝜖     ⌉Σ ⌈𝑘𝜖
by the loop iteration number 𝑘 as a result of the type of seqloop : N[𝑘] → 𝜏 → (𝜏 −−−→  → 𝜏) −−−−→
                                                                                                 →𝜏
and the type rule for privacy function application. Finally, the new let rule for the Jazz privacy
fragment which tracks latent contextual sensitivities is used in the let-binding for 𝑞𝑖 to precompute
an intermediate value which is used multiple times, without the need for explicit boxing.

9.3     Diﬀerentially Private Deep Learning with Adaptive Clipping
The current state-of-the-art in diﬀerentially private machine learning is noisy gradient descent [2]:
at each iteration of training, compute the gradient, clip the gradient to have bounded 𝐿2 norm, and
add noise in proportion to the clipping parameter. The clipping parameter is typically treated as a
hyperparameter, set by the analyst before training.

                                        ∞𝑠,(𝜖,𝛿)𝑥
     gauss : (𝑠 : sens) → (𝑥 : R·𝑠) −−−−−−−→   →R
                                       s    s                DPAL(𝑋, 𝑦, 𝑘, 𝛾, 𝜖, 𝛿, 𝛿 ′ ) ,
     zeros(𝑛) , mcreate𝐿∞ 1 𝑛 (𝜆 𝑖. 𝜆 𝑗 . 0.0)
                                                               let 𝐶 0 = MAXNUM in
     DPMean : ∀ (𝜖ˆ : R) (𝛿ˆ : R). (𝜖 : R[𝜖])            ˆ
                                              ˆ → (𝛿 : R[𝛿])   let 𝜃 0 = zeros (cols 𝑋 ) in
                                                                                            p
           → (𝑠 : sens) → (𝑥 : (M[𝑚,     ˆ 𝑛]
                                           ˆ D)·𝑠)             aloop 𝛿 ′ 𝑘 𝜃 0 <𝑋, 𝑦> (𝜆 (𝜃 𝑡 , 𝐶 𝑡 ).
            ∞𝑠,(𝜖,𝛿)𝑥
           −−−−−−−→ → (M[1, 𝑛]ˆ R) ,                               let 𝑔𝑠 = (gradients 𝜃 𝑡 𝑋 𝑦) in
        mgauss 𝜖 𝛿 (mean 𝑥)                                        𝑔𝑝 ← DPMean 𝜖 𝛿 (mclip 𝐶 𝑡 𝑔𝑠);
                                                                   let 𝑑 = (𝜃 𝑡 − 𝑔𝑝 ) in
     clipUpdate(𝐶 𝑡 , 𝑑, 𝛾, 𝑔𝑠, 𝜖, 𝛿) ,                            𝐶 𝑡 ′ ← clipUpdate 𝐶 𝑡 𝑑 𝛾 𝑔𝑠 𝜖 𝛿;
        𝛽 ← DPMean 𝜖 𝛿 (I k𝑑 k ≤𝐶𝑡 𝑔𝑠);                            return (𝑑, 𝐶 𝑡 ′ ))
        return 𝐶 𝑡 − (𝛽 − 𝛾)

Recent work by Thakkar et al. [53] proposed an algorithm for adaptively determining the clipping
parameter during training, by adaptively improving the clipping parameter based on a diﬀeren-
tially private estimate of the percentage of gradients clipped in each iteration.
   In each iteration, the implementation computes the gradients for a batch of examples 𝑔𝑠, clips
each gradient using the current parameter 𝐶 𝑡 , and uses the Gaussian mechanism to compute a
diﬀerentially private average gradient 𝑔𝑝 . Then, the algorithm updates the clipping parameter for
the next iteration 𝐶 𝑡 ′ using clipUpdate, which computes a noisy count 𝛽 of the number of gradients
in 𝑔𝑠 that are clipped under the clipping parameter 𝐶 𝑡 and uses the count to update the parameter.
The inputs to the algorithm are the training data 𝑋 , the training labels 𝑦, the number of iterations
𝑘, and the target percentage of gradients remaining un-clipped 𝛾. 𝜖, 𝛿, and 𝛿 ′ are the privacy cost
parameters. We omit the sensitivity annotations on top-level function inputs for readability. The
Jazz typechecker typechecks DPAL in 5.6ms (averaged over 10 runs).

   Beyond Duet. In this case study, we implement a library function for the diﬀerentially private
average (DPMean) and use it in two places. This refactoring is not possible in Duet, because Duet’s
privacy functions require all sensitive arguments to have a sensitivity of 1. In this algorithm, one
of the uses of DPMean in fact has data-dependent sensitivity (the sensitivity of mclip 𝐶 𝑡 𝑔𝑠 is 𝐶 𝑡 ).
   Practical implementations of algorithms like this one often rely on libraries of diﬀerentially
private functions like DPMean (e.g. the Opacus library for diﬀerentially private deep learning [57],
or the OpenDP library for diﬀerentially private analytics [35]). By lifting the limitations of Duet’s
privacy functions, Jazz makes it possible to implement and use such libraries.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       53


  Primitives used. This algorithm demonstrates the use of privacy combinators (e.g. aloop) that
can be speciﬁed as primitives in Jazz but require special typing rules in Duet:

                                                                    𝛿 relaxation      iterations   initial value
          aloop : ∀ 𝜖 : R+, 𝛿 : R+, 𝛿 ′ : R+, 𝑠 : R+ , Γ : cxt. (𝛿 ′ : R+ [𝛿 ′ ]) → (𝑘 : N) → (𝑖𝑛𝑖𝑡 : 𝜏)
                           loop body    total privacy cost of the loop
                             (𝜖,𝛿)Γ      (𝜖 ′, 𝑘𝛿 + 𝛿 ′ )Γ
              → (M : (𝑥p: 𝜏 −−−−→ → 𝜏)) −−−−−−−−−−−−→    →𝜏
          𝑤ℎ𝑒𝑟𝑒 𝜖 ′ , 2𝜖( 2𝑘(log(1/𝛿 ′)))
This type for aloop encodes the advanced composition theorem (introduced in Section 2). Our
advanced composition combinator runs an (𝜖, 𝛿)-diﬀerentially
                                                         Ä p private function (M)       ä representing
the body of the loop 𝑘 times, for a total privacy cost of 2𝜖( 2𝑘(log(1/𝛿 ′ ))), 𝑘𝛿 + 𝛿 ′ (a signiﬁcant
improvement over the sequential composition cost of (𝑘𝜖, 𝑘𝛿)).
    Our version of the adaptive clipping gradient descent algorithm uses advanced composition and
(𝜖, 𝛿)-diﬀerential privacy, to demonstrate the encoding of aloop as a regular function in Jazz. Our
source code repository contains an alternative implementation that uses zero-concentrated diﬀer-
ential privacy for improved composition, and converts the privacy guarantee to (𝜖, 𝛿)-diﬀerential
privacy at the end of the algorithm.

10 RELATED WORK
Verification techniques based on type systems. There are two threads of prior work in type-system-
based veriﬁcation of diﬀerential privacy for high-level programs: those based in linear types, and
those based on relational reﬁnement types. Reed and Pierce [49] proposed Fuzz, the ﬁrst type
system for diﬀerential privacy based on linear typing; its fundamental components are a linear
type system with an indexed “scaling” modality !𝑠 for tracking the sensitivity of programs and a
monadic connective to model randomized computations. An 𝑠-sensitive function is encoded
in Fuzz as a linear function with scaled domain !𝑠 𝐴 ⊸ 𝐵 and often notated 𝐴 ⊸𝑠 𝐵. An 𝜖-
diﬀerential privacy mechanism is represented as an 𝜖-sensitive function with monadic return type
as in 𝐴 ⊸𝜖 𝐵. DFuzz [34] extends Fuzz with dependent types to encode sensitivity and pri-
vacy bounds that depend on the values of function arguments. This allows e.g. reasoning about
the privacy of iterative algorithms whose privacy cost depend on the number of iterations. Fuzz
and DFuzz can be characterized by strong support for higher-order programming and potential
for automation via type inference. They support pure diﬀerential privacy but approximate and
any other recent variants of diﬀerential privacy fall out of their scope due to nonlinear scaling.
Several recently-proposed approaches allow a Fuzz-like analysis for (𝜖, 𝛿)-diﬀerentially private
programs: Azevedo de Amorim et al. [29] leverage a path construction and a Fuzz-like type sys-
tem. Fuzzi [59] integrates a Fuzz-like type system with an expressive program logic. Fuzzi directly
connects (automated) type-based proofs of composition for sensitivity and privacy properties with
(manual) apRHL proofs for basic constructs like sequential composition and the Laplace mecha-
nism. In our approach, on the other hand, properties of basic mechanisms must be axiomatized.
The Fuzzi system targets imperative programs, and does not provide support for higher-order pro-
gramming with privacy functions. Finally Duet [46] proposes a two-language design with linear
types for tracking sensitivity and privacy; crucial restrictions in the typing rules of the privacy
language allow encoding advanced diﬀerential privacy variants such as approximate, Rényi, zero-
concentrated and truncated-concentrated diﬀerential privacy. In Duet privacy functions are 𝑛-ary
and written (𝜏1 @𝑝 1 , . . . , 𝜏𝑛 @𝑝𝑛 ) ⊸∗ 𝜏 for privacy quantities 𝑝𝑖 such as (𝜖𝑖 , 𝛿𝑖 ) in the case of approx-
imate diﬀerential privacy.

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
54                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter



       System    Sens. Function                   Sens. Typing     Priv. Function                     Priv. Typing
     (D)Fuzz 𝜏1 ⊸𝑠 𝜏2                            Γ ⊢𝑒 :𝜏           𝜏1 ⊸𝜖         𝜏2                   Γ⊢𝑒 : 𝜏
               ′ . {𝑥 :: 𝜏 | 𝔇 (𝑥 , 𝑥 ) ≤ 𝑠 ′ }
                                                                   {𝑥 :: 𝜏1 | 𝔇𝜏1 (𝑥 ⊳ , 𝑥 ⊲ ) ≤ 1}
     HOARe2 Π𝑠            1   𝜏1 ⊳ ⊲
                                              ′
              → {𝑦 :: 𝜏2 | 𝔇𝜏2 (𝑦⊳ , 𝑦⊲ ) ≤ 𝑠𝑠 }
                                                 𝔊 ⊢ 𝑒 :: 𝜏        → 𝔐𝜖,𝛿 [{𝑦 :: 𝜏2 | 𝑦⊳ = 𝑦⊲ }]
                                                                                                      𝔊 ⊢ 𝑒 :: 𝔐𝜖,𝛿 [𝜏]
       Duet 𝜏 ⊸𝑠 𝜏                               Γ ⊢𝑒 :𝜏           (𝜏@𝑝, . . . , 𝜏@𝑝) ⊸∗ 𝜏            Γ ⊢𝑒 :𝜏
                          Σ                                                  Σ
         Jazz (𝑥 : 𝜏) →
                      − 𝜏                         Γ ⊢𝑒 :𝜏 ; Σ      (𝑥 : 𝜏) →
                                                                           −→ 𝜏                       Γ ⊢𝑒 :𝜏 ; Σ

Table 4. How each system —(D)Fuzz, HOARe2 , Duet and Jazz (this paper)—(1) encodes function sensitivity
in types, (2) structures typing judgments for function sensitivity, (3) encodes diﬀerential privacy in types,
and (4) structures typing judgments for diﬀerential privacy.

    Unlike previous works based on linear type systems, HOARe2 [14] uses relational reﬁnement
types to encode arbitrary relational properties of programs, including diﬀerential privacy. In HOARe2 ,
an 𝑠-sensitive function type is written Π𝑠 ′ . {𝑥 :: 𝜏1 | 𝔇𝜏1 (𝑥 ⊳, 𝑥 ⊲ ) ≤ 𝑠 ′ } → {𝑦 :: 𝜏2 | D𝜏2 (𝑦⊳, 𝑦⊲ ) ≤
𝑠𝑠 ′ } where 𝔇𝜏 is a type-indexed distance metric, and 𝑥 ⊳ and 𝑥 ⊲ are explicit symbolic representation
of the “left” and “right” execution of the program in support of encoding relational properties. To
account for probabilistic private computations, HOARe2 uses an indexed monad 𝔐𝜖,𝛿 [𝜏]: the type
of an (𝜖, 𝛿)-diﬀerentially private function is written {𝑥 :: 𝜏1 | 𝔇𝜏1 (𝑥 ⊳, 𝑥 ⊲ ) ≤ 1} → 𝔐𝜖,𝛿 [{𝑦 :: 𝜏2 |
𝑦⊳ = 𝑦⊲ }]. A limitation of this encoding is that a function of two arguments which provides diﬀer-
ent privacy bounds for each argument (as described in Section 3.3) will report a summed, global
privacy bound, because the tracking of privacy occurs in a single global index to the privacy monad
𝔐𝜖,𝛿 . Because privacy is proved as a relational property, rather than as a sensitivity/Lipschitz conti-
nuity property, HOARe2 is also capable of placing relational distance bounds on arguments to func-
tions. Regarding the implementation, both HOARe2 and Jazz use dependent types to capture sizes.
Regarding typechecking, even though some automation has been achieved [24], the automation re-
lies heavily on what is achievable with SMT solvers, and has limited application to programs which
make generous use of compositional or higher-order programming techniques, or metric-distance
relationships between values at non-base types. SMT solvers are not complete for non-linear op-
erations, which are common in complex diﬀerential privacy mechanisms. Consider,          p      for example,
the expression for privacy cost under advanced composition: 𝜖 ′ = 𝑘𝜖(𝑒 𝜖 − 1) + 𝜖 2𝑘 ln(1/𝛿 ′ ); SMT
solvers are not capable of proving universally quantiﬁed qualities between equations like these,
which limits their ability to automate reasoning about privacy cost.
    It is important to note that all of these type systems support some form of recursion. Adding
any form of recursion in the formalism of Jazz would make the technical development even more
complicated. We just focused on a small core that could illustrate the main novelties of the latent
or contextual approach.
    To conclude the overview about type-system-based veriﬁcation techniques, we refer the reader
to Table 4, comparing diﬀerent aspects of the reviewed type systems.
Techniques based on couplings and program logics. Approximate couplings [12] are a probabilis-
tic abstraction that witnesses diﬀerential privacy properties of programs and have been success-
fully exploited for veriﬁcation purposes. The relational Hoare logic apRHL [16] and its succes-
sors apRHL+ [15] and span-apRHL [50] internalize the compositional construction of such cou-
plings and capture from pure and approximate diﬀerential privacy to more recent variants such
as Rényi, zero-concentrated and truncated-concentrated diﬀerential privacy. While compared to
other methods these program logics are rather expressive going beyond the composition of (a
set of predeﬁned) basic mechanisms, derivations in the logics involve complex quantitative rea-
soning, not always amenable to automation. Even though there has been a successful report on

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       55


partial automation [11], e.g. the synthesis of (quantitative relational) loop invariants for iterative
algorithms remains challenging. To synthesise couplings, Albarghouthi and Hsu [5] use an alterna-
tive approach based on constraint solving which is highly amenable to automation; the approach
is however conﬁned to 𝜖-DP. Finally, to verify programs that achieve (𝜖, 𝛿)-DP composing basic
mechanisms, Barthe et al. [13] use a customised program product construction and traditional
(non-relational and non-probabilistic) Hoare logic augmented with mechanism-speciﬁc rules. In
recent work, Barthe et al. [9] show that checking diﬀerential privacy for imperative programs is
undecidable in general, but present a reduction to a decidable fragment of ﬁrst-order logic for
a restricted class of programs. Barthe et al. [10] also shows that checking accuracy bounds for
diﬀerentially private programs is also undecidable (in general). A common limitation of all these
approaches is that they are restricted to ﬁrst order imperative programs.
Techniques based on randomness alignment. LightDP [58] and ShadowDP [54] take a third approach
to verifying diﬀerential privacy based on randomness alignments. A randomness alignment is an
injective function relating the randomness from one execution of a diﬀerentially private mecha-
nism to a second execution of the same mechanism (i.e. M(𝑥) outputs the same result with noise 𝐻
as M(𝑥 ′) outputs with noise 𝑓 (𝐻 ), where 𝑓 is the randomness alignment). Both LightDP and Shad-
owDP are capable of verifying complex low-level mechanisms like the sparse vector technique in
just a few seconds. However, both tools target a ﬁrst-order imperative programming language, and
have limited support for higher-order programming.
Techniques based on testing. Since diﬀerential privacy mechanisms are randomized, traditional
methods of software testing do not apply. Two recent works by Bichsel et al. [19] and Ding et al.
[30] address this challenge by automatically generating neighboring inputs for the mechanism
being tested, and sampling from their outputs many times to approximate their output distribu-
tions. For privacy mechanisms with major bugs, these tools are able to show that the approximated
distributions do not satisfy the claimed diﬀerential privacy guarantee. Wilson et al. [55] have imple-
mented a testing tool based on this approach in their open-source library. DPCheck [60] combines
static analysis with instrumented concrete execution of the target program to detect bugs in even
more complex algorithms.
Type systems and contextual information. The technical device of contextual latent eﬀects used
in Sax and Jazz is related to prior approaches to expose information about captured variables in
function types. Leroy [40] and Hannan et al. [37] use function types augmented with the set of
captured variables, the former for tracking dangerous type variables for polymorphic generaliza-
tion, and the latter for lifetime analysis. Scherer and Hoﬀmann [51] introduce open closure types in
order to track additional information about closed-over variables in ﬁrst-class functions. An open
closure type augments the traditional arrow type with a lexical environment of closed over vari-
ables, further decorated by a mapping characterizing the use of each variable. For instance, they
formalize a system where the mapping marks each variable with a Boolean indicating whether the
evaluation of the body of the function depends on the variable or not. An open closure type also
includes the name of the function argument similarly decorated. For the considered system, they
prove a non-interference property, which states that closing an open term with two valuations
that coincide on used variables yield the same result, up to used variables. Function types in Sax
and Jazz can be seen as speciﬁc cases of open closure types, in which the information attached
to captured variables (and arguments) is not a Boolean value, but sensitivity and privacy informa-
tion. Consequently, the type soundness result we establish is more general than noninterference;
for instance, in Sax, for two valuations that are at a given distance apart, the distance between the
results are bounded by the sensitivities of each variables. The technical development of contextual

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
56                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


linear types shares many concerns with that of open closure types, notably regarding the proper
handling of the typing environment—in which order matters—and of scoping. However, our sound-
ness results rely on logical relations, while they adopt a more restricted technique, suﬃcient for
the purpose of the simple type system tracking Boolean information.
   As observed by Scherer and Hoﬀmann, using open closure types allows delaying the accounting
of information ﬂow into closures from abstraction time to application time. Likewise, contextual
sensitivity in Sax delays sensitivity accounting to application time. We extend this principle to pos-
itive type constructors such as products and sums, generally deferring accounting to elimination
forms; we believe this would likewise apply to the simpler information-ﬂow control setting they
study.
   Recently, Bao et al. [8] use a similar context-annotation technique to track reachability infor-
mation in types. For instance, they augment the type of reference cell with the variables in scope
that alias the cell. This information is tracked on function types as well, in order to track the reach-
ability information from closures. In all these approaches, type information depends on variable
names; this is quite diﬀerent from dependent types, however, where types depend on arbitrary
terms. The telescope nature of the typing environment is similar, but many of the deep challenges
of dependent types do not manifest in this restricted setting.
   Hoare Type Theory [45] supports specifying eﬀectful, heap-manipulating computations by in-
troducing Hoare-style pre/postconditions in types. Computation types include contexts of vari-
ables and heap locations in order to track footprints of logical assertions. In a similar vein as Leroy
[40], the context of variables is not decorated with any information, so it is unclear whether one
could handle contextual sensitivity and privacy in this approach.
   Finally, it would be interesting to study if generic approaches such as coeﬀects [48] and graded
modal types [47] can express delayed sensitivity and privacy tracking as developed here. These
generic approaches use resource algebras (such as the semiring of natural numbers) for capturing
modalities in types. To the best of our knowledge, these are not contextual: for instance, the arrow
type is annotated with a scalar, label, etc., not with a decorated environment as in open closure
types and this work. Extending these generic approaches to support contextual information on
all type constructors could bring the beneﬁts of lazy accounting to a wide range of type-based
quantitative program reasoning.

11 CONCLUSION
We have presented Jazz, a language and type system for diﬀerentially private programming with
strong support for both higher-order programming and advanced variants of diﬀerential privacy.
The key insight of our approach is latent contextual tracking of both privacy and sensitivity,
which enables sum, product and function types to describe their privacy eﬀects—even for closure
variables—making it possible to delay the payment of the eﬀects until actual elimination, some-
times yielding advantages on the precision of the analysis and the annotation burden.
   We have formalized a core subset of Jazz and proved its soundness using a step-indexed logical
relation, following a novel strategy. Case studies demonstrate the ability to encode basic privacy
mechanisms and privacy combinators as primitives in Jazz, and to compose them to develop more
complicated iterative diﬀerentially private algorithms.
   Jazz extends the expressive power of systems like Fuzz [49] to advanced variants of diﬀerential
privacy. Like Fuzz, it remains incapable of proving the correctness of basic privacy mechanisms
like the Laplace mechanism. One interesting avenue for future work lies in combining Jazz with an
expressive program logic like apRHL [16, 17] in the style of Fuzzi [59]. Such a combined system
would provide a complete programming framework supporting higher-order programming and

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                           57


end-to-end privacy proofs. Another line of future work is to incorporate some form of recursion
to Jazz such as recursive types.

REFERENCES
 [1] 2019.                 scikit-learn:    Standardization,       or    mean       removal     and      variance    scaling.
     https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
 [2] Martin Abadi, Andy Chu, Ian Goodfellow, H Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep
     learning with diﬀerential privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications
     Security. 308–318.
 [3] Amal Ahmed. 2004. Semantics of Types for Mutable State. Ph.D. Dissertation. Princeton University.
 [4] Amal Ahmed. 2006. Step-Indexed Syntactic Logical Relations for Recursive and Quantiﬁed Types. In Programming
     Languages and Systems, 15th European Symposium on Programming, ESOP 2006, Held as Part of the Joint European
     Conferences on Theory and Practice of Software, ETAPS 2006, Vienna, Austria, March 27-28, 2006, Proceedings (Lecture
     Notes in Computer Science), Vol. 3924. Springer, 69–83.
 [5] Aws Albarghouthi and Justin Hsu. 2018. Synthesizing coupling proofs of diﬀerential privacy. PACMPL 2, POPL (2018),
     58:1–58:30. https://doi.org/10.1145/3158146
 [6] Andrew W. Appel and David McAllester. 2001. An Indexed Model of Recursive Types for Foundational Proof-carrying
     Code. ACM Trans. Program. Lang. Syst. 23, 5 (Sept. 2001), 657–683.
 [7] Borja Balle and Yu-Xiang Wang. 2018. Improving the Gaussian mechanism for diﬀerential privacy: Analytical cali-
     bration and optimal denoising. In International Conference on Machine Learning. PMLR, 394–403.
 [8] Yuyan Bao, Guannan Wei, Oliver Bracevac, Yuxuan Jiang, Qiyang He, and Tiark Rompf. 2021. Reachability types:
     tracking aliasing and separation in higher-order functional programs. Proc. ACM Program. Lang. 5, OOPSLA (2021),
     1–32.
 [9] Gilles Barthe, Rohit Chadha, Vishal Jagannath, A Prasad Sistla, and Mahesh Viswanathan. 2020. Deciding diﬀerential
     privacy for programs with ﬁnite inputs and outputs. In Proceedings of the 35th Annual ACM/IEEE Symposium on Logic
     in Computer Science. 141–154.
[10] Gilles Barthe, Rohit Chadha, Paul Krogmeier, A Prasad Sistla, and Mahesh Viswanathan. 2021. Deciding accuracy of
     diﬀerential privacy schemes. Proceedings of the ACM on Programming Languages 5, POPL (2021), 1–30.
[11] Gilles Barthe, George Danezis, Benjamin Grégoire, César Kunz, and Santiago Zanella Béguelin. 2013. Ver-
     iﬁed Computational Diﬀerential Privacy with Applications to Smart Metering. In 2013 IEEE 26th Computer
     Security Foundations Symposium, New Orleans, LA, USA, June 26-28, 2013. IEEE Computer Society, 287–301.
     https://doi.org/10.1109/CSF.2013.26
[12] Gilles Barthe, Thomas Espitau, Justin Hsu, Tetsuya Sato, and Pierre-Yves Strub. 2019. Relational ★★\star-Liftings for
     Diﬀerential Privacy. Logical Methods in Computer Science 15, 4 (2019). https://lmcs.episciences.org/5989
[13] G. Barthe, M. Gaboardi, E. J. G. Arias, J. Hsu, C. Kunz, and P. Strub. 2014. Proving Diﬀerential Privacy in Hoare Logic.
     In 2014 IEEE 27th Computer Security Foundations Symposium. 411–424. https://doi.org/10.1109/CSF.2014.36
[14] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu, Aaron Roth, and Pierre-Yves Strub. 2015. Higher-
     Order Approximate Relational Reﬁnement Types for Mechanism Design and Diﬀerential Privacy. In Proceedings of
     the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’15). Association
     for Computing Machinery, New York, NY, USA, 55–68. https://doi.org/10.1145/2676726.2677000
[15] Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016.                 Proving Dif-
     ferential Privacy via Probabilistic Couplings. In Proceedings of the 31st Annual ACM/IEEE Symposium on
     Logic in Computer Science (LICS ’16). Association for Computing Machinery, New York, NY, USA, 749–758.
     https://doi.org/10.1145/2933575.2934554
[16] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. 2012. Probabilistic Relational Rea-
     soning for Diﬀerential Privacy. In Proceedings of the 39th Annual ACM SIGPLAN-SIGACT Symposium on Princi-
     ples of Programming Languages (POPL ’12). Association for Computing Machinery, New York, NY, USA, 97–110.
     https://doi.org/10.1145/2103656.2103670
[17] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella-Béguelin. 2013. Probabilistic Relational Rea-
     soning for Diﬀerential Privacy. ACM Trans. Program. Lang. Syst. 35, 3, Article Article 9 (Nov. 2013), 49 pages.
     https://doi.org/10.1145/2492061
[18] Raef Bassily, Adam Smith, and Abhradeep Thakurta. 2014. Private empirical risk minimization: Eﬃcient algorithms
     and tight error bounds. In Foundations of Computer Science (FOCS), 2014 IEEE 55th Annual Symposium on. IEEE, 464–
     473.
[19] Benjamin Bichsel, Timon Gehr, Dana Drachsler-Cohen, Petar Tsankov, and Martin Vechev. 2018. Dp-ﬁnder: Finding
     diﬀerential privacy violations by sampling and optimization. In Proceedings of the 2018 ACM SIGSAC Conference on


                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
58                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


     Computer and Communications Security. 508–524.
[20] Mark Bun, Cynthia Dwork, Guy N Rothblum, and Thomas Steinke. 2018. Composable and versatile privacy via
     truncated CDP. In Proceedings of the 50th Annual ACM SIGACT Symposium on Theory of Computing. 74–86.
[21] Mark Bun and Thomas Steinke. 2016. Concentrated diﬀerential privacy: Simpliﬁcations, extensions, and lower bounds.
     In Theory of Cryptography Conference. Springer, 635–658.
[22] Clément L. Canonne, Gautam Kamath, and Thomas Steinke. 2020. The Discrete Gaussian for Diﬀerential Privacy. In
     Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems
     2020 (NeurIPS 2020).
[23] Kamalika Chaudhuri and Staal A Vinterbo. 2013. A stability-based validation procedure for diﬀerentially private
     machine learning. In Advances in Neural Information Processing Systems. 2652–2660.
[24] Ezgi Çiçek, Weihao Qu, Gilles Barthe, Marco Gaboardi, and Deepak Garg. 2019. Bidirectional type checking for
     relational properties. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and Im-
     plementation, PLDI 2019, Phoenix, AZ, USA, June 22-26, 2019, Kathryn S. McKinley and Kathleen Fisher (Eds.). ACM,
     533–547. https://doi.org/10.1145/3314221.3314603
[25] Michael R. Clarkson and Fred B. Schneider. 2010. Hyperproperties. J. Comput. Secur. 18, 6 (Sept. 2010), 1157–1210.
[26] Arthur Azevedo de Amorim, Emilio Jesús Gallego Arias, Marco Gaboardi, and Justin Hsu. 2015. Really Natural Linear
     Indexed Type Checking. CoRR abs/1503.04522 (2015). arXiv:1503.04522 http://arxiv.org/abs/1503.04522
[27] Arthur Azevedo de Amorim, Marco Gaboardi, Emilio Jesús Gallego Arias, and Justin Hsu. 2014. Really Natural Linear
     Indexed Type Checking. In Proceedings of the 26nd 2014 International Symposium on Implementation and Application of
     Functional Languages (IFL ’14). ACM, New York, NY, USA, Article 5, 12 pages. https://doi.org/10.1145/2746325.2746335
[28] Arthur Azevedo de Amorim, Marco Gaboardi, Justin Hsu, Shin-ya Katsumata, and Ikram Cherigui. 2017. A semantic
     account of metric preservation. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming
     Languages, POPL 2017, Paris, France, January 18-20, 2017, Giuseppe Castagna and Andrew D. Gordon (Eds.). 545–556.
[29] Arthur Azevedo de Amorim, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. 2019. Probabilistic Relational
     Reasoning via Metrics. In 2019 34th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS). IEEE, 1–19.
[30] Zeyu Ding, Yuxin Wang, Guanhong Wang, Danfeng Zhang, and Daniel Kifer. 2018. Detecting violations of diﬀerential
     privacy. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security. 475–489.
[31] Cynthia Dwork, Moni Naor, Omer Reingold, Guy N. Rothblum, and Salil Vadhan. 2009. On the Complexity of Diﬀer-
     entially Private Data Release: Eﬃcient Algorithms and Hardness Results. In Proceedings of the Forty-First Annual ACM
     Symposium on Theory of Computing (STOC ’09). Association for Computing Machinery, New York, NY, USA, 381–390.
     https://doi.org/10.1145/1536414.1536467
[32] Cynthia Dwork and Aaron Roth. 2014. The algorithmic foundations of diﬀerential privacy. Foundations and Trends®
     in Theoretical Computer Science 9, 3–4 (2014), 211–407.
[33] Richard A. Eisenberg and Stephanie Weirich. 2012. Dependently Typed Programming with Singletons. In Proceedings
     of the 2012 Haskell Symposium. Association for Computing Machinery, New York, NY, USA, 117–130.
[34] Marco Gaboardi, Andreas Haeberlen, Justin Hsu, Arjun Narayan, and Benjamin C Pierce. 2013. Linear dependent
     types for diﬀerential privacy. In Proceedings of the 40th annual ACM SIGPLAN-SIGACT symposium on Principles of
     programming languages. 357–370.
[35] Marco Gaboardi, Michael Hay, and Salil Vadhan. 2020. A programming framework for opendp. Manuscript (2020).
[36] David K. Giﬀord and John M. Lucassen. 1986. Integrating functional and imperative programming. In Proceedings of
     the 1986 ACM Conference on Lisp and Functional Programming. 28–38.
[37] J. Hannan, P. Hicks, and D. Liben-Nowell. 1997. A Lifetime Analysis for Higher-Order Languages. Technical Report.
     Pennsylvania State University.
[38] Moritz Hardt, Katrina Ligett, and Frank McSherry. 2012. A simple and practical algorithm for diﬀerentially private
     data release. In Advances in Neural Information Processing Systems. 2339–2347.
[39] Susumu Hayashi. 1991. Singleton, Union and Intersection Types for Program Extraction. In Theoretical Aspects of
     Computer Software, International Conference TACS ’91, Sendai, Japan, September 24-27, 1991, Proceedings (Lecture Notes
     in Computer Science), Takayasu Ito and Albert R. Meyer (Eds.), Vol. 526. Springer, 701–730.
[40] Xavier Leroy. 1992. Polymorphic Typing of an Algorithmic Language. Technical Report Research Report 1778. INRIA.
[41] Min Lyu, Dong Su, and Ninghui Li. 2017. Understanding the Sparse Vector Technique for Diﬀerential Privacy. PVLDB
     10, 6 (2017), 637–648. https://doi.org/10.14778/3055330.3055331
[42] Frank McSherry. 2009. Privacy integrated queries: an extensible platform for privacy-preserving data anal-
     ysis. In Proceedings of the 2009 ACM SIGMOD International Conference on Management of Data. ACM, 19–30.
     https://doi.org/10.1145/1559845.1559850
[43] Ilya Mironov. 2012. On Signiﬁcance of the Least Signiﬁcant Bits for Diﬀerential Privacy. In Proceedings of the 2012
     ACM Conference on Computer and Communications Security (CCS ’12). ACM, 650–661.



ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                          59


[44] Ilya Mironov. 2017. Rényi diﬀerential privacy. In 2017 IEEE 30th Computer Security Foundations Symposium (CSF).
     IEEE, 263–275.
[45] Aleksandar Nanevski, J. Gregory Morrisett, and Lars Birkedal. 2008. Hoare type theory, polymorphism and separation.
     J. Funct. Program. 18, 5-6 (2008), 865–911.
[46] Joseph P Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel Somani, Mu Zhang,
     Nikhil Sharma, Alex Shan, et al. 2019. Duet: an expressive higher-order language and linear type system for statically
     enforcing diﬀerential privacy. Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–30.
[47] Dominic Orchard, Vilem-Benjamin Liepelt, and Harley Eades III. 2019. Quantitative program reasoning with graded
     modal types. Proc. ACM Program. Lang. 3, ICFP (2019), 110:1–110:30.
[48] Tomas Petricek, Dominic A. Orchard, and Alan Mycroft. 2014. Coeﬀects: a calculus of context-dependent computation.
     In Proceedings of the 19th ACM SIGPLAN international conference on Functional programming, Gothenburg, Sweden,
     September 1-3, 2014, Johan Jeuring and Manuel M. T. Chakravarty (Eds.). ACM, 123–135.
[49] Jason Reed and Benjamin C Pierce. 2010. Distance makes the types grow stronger: a calculus for diﬀerential privacy.
     In Proceedings of the 15th ACM SIGPLAN international conference on Functional programming. 157–168.
[50] T. Sato, G. Barthe, M. Gaboardi, J. Hsu, and S. Katsumata. 2019. Approximate Span Liftings: Compositional Semantics
     for Relaxations of Diﬀerential Privacy. In 2019 34th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS).
     1–14. https://doi.org/10.1109/LICS.2019.8785668
[51] Gabriel Scherer and Jan Hoﬀmann. 2013. Tracking Data-Flow with Open Closure Types. In Proceedings of the 19th
     International Conference on Logic for Programming, Artiﬁcial Intelligence, and Reasoning (LPAR 2013) (Lectures Notes in
     Computer Science). Springer, 710–726.
[52] Kunal Talwar, Abhradeep Guha Thakurta, and Li Zhang. 2015. Nearly optimal private lasso. In Advances in Neural
     Information Processing Systems. 3025–3033.
[53] Om Thakkar, Galen Andrew, and H Brendan McMahan. 2019. Diﬀerentially private learning with adaptive clipping.
     arXiv preprint arXiv:1905.03871 (2019).
[54] Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang. 2019. Proving diﬀerential privacy
     with shadow execution. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and
     Implementation. 655–669.
[55] Royce J Wilson, Celia Yuxing Zhang, William Lam, Damien Desfontaines, Daniel Simmons-Marengo, and Bryant Gip-
     son. 2020. Diﬀerentially Private SQL with Bounded User Contribution. Proceedings on Privacy Enhancing Technologies
     2020, 2 (2020).
[56] Xi Wu, Fengan Li, Arun Kumar, Kamalika Chaudhuri, Somesh Jha, and Jeﬀrey Naughton. 2017. Bolt-on Diﬀerential Pri-
     vacy for Scalable Stochastic Gradient Descent-based Analytics. In Proceedings of the 2017 ACM International Conference
     on Management of Data (SIGMOD ’17). ACM, New York, NY, USA, 1307–1322. https://doi.org/10.1145/3035918.3064047
[57] Ashkan Yousefpour, Igor Shilov, Alexandre Sablayrolles, Davide Testuggine, Karthik Prasad, Mani Malek, John
     Nguyen, Sayan Ghosh, Akash Bharadwaj, Jessica Zhao, et al. 2021. Opacus: User-friendly diﬀerential privacy library
     in PyTorch. arXiv preprint arXiv:2109.12298 (2021).
[58] Danfeng Zhang and Daniel Kifer. 2017. LightDP: towards automating diﬀerential privacy proofs. In Proceedings of the
     44th ACM SIGPLAN Symposium on Principles of Programming Languages. 888–901.
[59] Hengchu Zhang, Edo Roth, Andreas Haeberlen, Benjamin C Pierce, and Aaron Roth. 2019. Fuzzi: A three-level logic
     for diﬀerential privacy. Proceedings of the ACM on Programming Languages 3, ICFP (2019), 1–28.
[60] Hengchu Zhang, Edo Roth, Andreas Haeberlen, Benjamin C Pierce, and Aaron Roth. 2020. Testing diﬀerential privacy
     with dual interpreters. Proceedings of the ACM on Programming Languages 4, OOPSLA (2020), 1–26.




                                 ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
60                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




     𝑟 ∈R
     𝑏∈B
     𝑥 ∈ var
     𝑒 ∈ sexpr F 𝑟 | 𝑒 + 𝑒 | 𝑒 ∗ 𝑒 | 𝑒 ≤ 𝑒                                                  real numbers
                       s                p
               | 𝑥 | 𝜆 (𝑥 : 𝜏 ·𝑠). 𝑒 | 𝜆 (𝑥 : 𝜏 ·𝑠). e | 𝑒 𝑒                                vars, functions, applications
               | tt                                                                         unit
               | inl𝜏2 𝑒 | inr𝜏1 𝑒 | case 𝑒 of {𝑥 ⇒ 𝑒} {𝑦 ⇒ 𝑒 }                             sums
               | (𝑒, 𝑒) | fst 𝑒 | snd 𝑒                                                     add. products
               | h𝑒, 𝑒i | let 𝑥, 𝑥 = 𝑒 in 𝑒                                                 mult. products
               | 𝑒 :: 𝜏                                                                     ascription
               | 𝑏 | if 𝑒 then 𝑒 else 𝑒                                                     (derived) booleans
               | let 𝑥 = 𝑒 in 𝑒                                                             (derived) let
     e ∈ pexpr F return 𝑒 | 𝑥 : 𝜏 ← e ; e | e e                                             return, bind, applications
               | if 𝑒 then e else e | case 𝑒 of {𝑥 ⇒ e} {𝑦 ⇒ e}                             conditionals, case
               | let 𝑥 = 𝑒 in e                                                             let
     𝑠 ∈ 𝑠𝑒𝑛𝑠 , R∞                                                                          sensitivities
     Σ ∈ 𝑠𝑒𝑛𝑣 , var ⇀ 𝑠𝑒𝑛𝑠 F 𝑠𝑥 + . . . + 𝑠𝑥                                                sensitivity environments
     𝑝 ∈ 𝑝𝑟𝑖𝑣 , (R∞, R∞ )                                                                   privacy costs
     Σ ∈ 𝑝𝑒𝑛𝑣 , ∅ | 𝑝𝑥 | Σ + Σ | Σ ⊔ Σ | Σ ⊓ Σ                                              privacy environments
                                                   Σ                 Σ
     𝜏 ∈ type F R | B | unit | (𝑥 : 𝜏 ·𝑠) →
                                          − 𝜏 | (𝑥 : 𝜏 ·𝑠) −
                                                           →→𝜏
              | 𝜏 Σ ⊕ Σ 𝜏 | 𝜏 Σ &Σ 𝜏 | 𝜏 Σ ⊗ Σ 𝜏                                            types
     Γ ∈ tenv , var ⇀ type F {𝑥 : 𝜏, . . . , 𝑥 : 𝜏 }                                        type environments


                                                   Fig. 18. 𝜆J : Syntax




APPENDIX
Throughout the appendix we use symbol 𝑠 instead of 𝑑, and Σ instead of Δ as they are interchange-
able.

A 𝜆J : STATIC SEMANTICS
In this section we present some deﬁnitions of the static semantics of 𝜆J not presented in the main
document. Figure 18 presents the syntax of 𝜆J . Figures 19 and 19 present the complete sensitivity
type system of 𝜆J . Figure 21 presents the complete type system of 𝜆J . They include the usage of Φ
and the type rules for the derived expressions: boolean, conditional and let expressions. Figure 22
presents the sensitivity instantiation or dot product operator and the sensitivity type instantiation
operator. Figure 23 presents the subtyping rules for 𝜆J . Figure 24 presents the sensitivity environ-
ment substitution environment. Figure 25, presents the diﬀerent lifts operators. Finally, Figure 26
presents the join and meet operator between types.

B 𝜆J : DYNAMIC SEMANTICS
Figure 27, presents the dynamic semantics of the sensitivity language. Figure 28, presents the
dynamic semantics of the privacy language.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       61




                                                       plus
                   rlit                                Γ ; Δ ⊢ 𝑒1 : R ; Σ1        Γ ; Δ ⊢ 𝑒2 : R ; Σ2
                   Γ;Δ⊢𝑟 :R;∅                                 Γ ; Δ ⊢ 𝑒1 + 𝑒2 : R ; Σ1 + Σ2
     times                                                                                 l-scale
    Γ ; Δ ⊢ 𝑒1 : R ; Σ1         Γ ; Δ ⊢ 𝑒2 : R ; Σ2           𝑒1 ≠ 𝑟         𝑒2 ≠ 𝑟           Γ ; Δ⊢ 𝑒 : R ; Σ
                          Γ ; Δ ⊢ 𝑒 1 ∗ 𝑒 2 : ∞(Σ1 + Σ2 )                                  Γ ; Δ⊢ 𝑟 ∗ 𝑒 : R ; 𝑟 Σ

   r-scale                        leq                                                        var
     Γ ; Δ⊢ 𝑒 : R ; Σ             Γ ; Δ ⊢ 𝑒1 : R ; Σ1             Γ ; Δ ⊢ 𝑒2 : R ; Σ2                Γ(𝑥) = 𝜏
   Γ ; Δ⊢ 𝑒 ∗ 𝑟 : R ; 𝑟 Σ                  Γ ; Δ ⊢ 𝑒 1 ≤𝑒 2 : ∞(Σ1 + Σ2 )                    Γ ; Δ + 𝑠𝑥 ⊢ 𝑥 : 𝜏 ; 𝑥

     s-lam                                                        p-lam
             Γ, 𝑥 : 𝜏1 ; Δ + 𝑑𝑥 ⊢ 𝑒 : 𝜏2 ; Σ                              Γ, 𝑥 : 𝜏1 ; Δ + 𝑠𝑥 ⊢ e : 𝜏2 ; Σ
               s                            Σ                                p                           Σ
     Γ ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑). 𝑒 : (𝑥 : 𝜏1 ·𝑠) → 𝜏2 ; ∅              Γ ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑). e : (𝑥 : 𝜏1 ·𝑑) → 𝜏2 ; ∅
               s-app
                                          Σ+𝑑𝑥
               Γ ; Δ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑑 ′ ) −−−−→ 𝜏2 ; Σ1         Γ ; Δ ⊢ 𝑒 2 : 𝜏1 ; Σ2      Δ·Σ2 ≤ 𝑑 ′
                                    Γ ; Δ ⊢ 𝑒 1 𝑒 2 : [Σ2/𝑥]𝜏2 ; Σ1 + 𝑠Σ2 + Σ
                                   inl                                           inr
   unit                                    Γ ; Δ ⊢ 𝑒 : 𝜏1 ; Σ                             Γ ; Δ ⊢ 𝑒 : 𝜏2 ; Σ
                                                                  ∅
   Γ ; Δ ⊢ tt : unit ; ∅                          𝜏2
                                   Γ ; Δ ⊢ inl 𝑒 : 𝜏1 ⊕ 𝜏2 ; ∅Σ
                                                                                 Γ ; Δ ⊢ inr𝜏1 𝑒 : 𝜏1 ∅ ⊕ Σ 𝜏2 ; ∅




                              Fig. 19. 𝜆J : Complete sensitivity type system (part 1)




C 𝜆J : SOUNDNESS
In this section we present auxiliary deﬁnitions used in Section 7.3, and the proof of the funda-
mental property. Figure 29 presents the join and meet operators for sensitivity environments and
sensitivities Σ + 𝑠. Figure 30 presents the subtyping relation between sensible types.

  Lemma C.1 (Associativity of the instantiation operator). Σ·(Σ1 + Σ2 ) = Σ·Σ1 + Σ·Σ2

  Proof. By induction on Σ1 :

Case (1) Σ1 = ∅

Subproof. Trivial as Σ·(∅ + Σ2 ) = Σ·Σ2 = Σ·∅ + Σ·Σ2 .                                                                 ⊳

Case (2) Σ1 = Σ1′ + 𝑠 1𝑥

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
62                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




     s-case
           Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1     Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 2 𝑥
                                Γ, 𝑦 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ12 ))𝑥 ⊢ 𝑒 3 : 𝜏3 ; Σ3 + 𝑠 3𝑦
                   Γ ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } :
                      [Σ1 + Σ11/𝑥]𝜏2 ⊔ [Σ1 + Σ12/𝑦]𝜏3 ; (Σ1 ⊔ (𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 Σ1 + 𝑠 3 Σ12 + Σ3 ))

         pair                                                                        proj1
         Γ ; Δ ⊢ 𝑒 1 : 𝜏1 ; Σ1 + Σ1′        Γ ; Δ ⊢ 𝑒 2 : 𝜏2 ; Σ2 + Σ2′              Γ ; Δ ⊢𝑒 : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ
                 Γ ; Δ ⊢ (𝑒 1, 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ1′ ⊔ Σ2′                     Γ ; Δ ⊢ fst 𝑒 : 𝜏1 ; Σ + Σ1

         proj2                                      tup
         Γ ; Δ ⊢𝑒 : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ                Γ ; Δ ⊢ 𝑒 1 : 𝜏1 ; Σ1 + Σ1′         Γ ; Δ ⊢ 𝑒 2 : 𝜏2 ; Σ2 + Σ2′
         Γ ; Δ ⊢ snd 𝑒 : 𝜏2 ; Σ + Σ2                         Γ ; Δ ⊢ h𝑒 1 , 𝑒 2 i : 𝜏1 Σ1 ⊗ Σ2 𝜏2 ; Σ1′ + Σ2′
     untup
                                            Γ ; Δ ⊢𝑒 1 : 𝜏11 Σ11 ⊗ Σ12 𝜏12 ; Σ1
          Γ, 𝑥 1 : 𝜏11, 𝑥 2 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 1 + (Δ·(Σ1 + Σ12 ))𝑥 2 ⊢𝑒 2 : 𝜏2 ; Σ2 + 𝑠 1𝑥 1 + 𝑠 2𝑥 2
     Γ ; Δ ⊢ let 𝑥 1, 𝑥 2 = 𝑒 1 in 𝑒 2 : [Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ; (𝑠 1 ⊔ 𝑠 2 )Σ1 + 𝑠 1 Σ11 + 𝑠 2 Σ12 + Σ2
                                             ascr
                                             Γ ;Δ⊢𝑒 :𝜏 ;Σ              𝜏 <: 𝜏 ′
                                                 Γ ; Δ ⊢ (𝑒 :: 𝜏 ′) : 𝜏 ′ ; Σ

                                                     . . . derived rules
                                       if
        blit                           Γ ; Δ ⊢ 𝑒1 : B ; Σ1         Γ ; Δ ⊢ 𝑒2 : 𝜏 ; Σ2          Γ ; Δ ⊢ 𝑒3 : 𝜏 ; Σ3
        Γ;Δ⊢𝑏:B;∅                           Γ ; Δ ⊢ if 𝑒 1 then {𝑒 2 } else {𝑒 3 } : 𝜏 ; Σ1 + (Σ2 ⊔ Σ3 )
                          let
                         Γ ; Δ ⊢ 𝑒 1 : 𝜏1 ; Σ1         Γ, 𝑥 : 𝜏1 ; Δ + ∞𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠𝑥
                                 Γ ; Δ ⊢ let 𝑥 = 𝑒 1 in 𝑒 2 : [Σ1/𝑥]𝜏2 ; 𝑠Σ1 + Σ2




                                Fig. 20. 𝜆J : Complete sensitivity type system (part 2)


Subproof. Let us assume 𝑥 ∉ Σ2 , and that 𝑟 = Σ(𝑥) if Σ(𝑥) is deﬁned, otherwise 𝑟 = 𝑥:
                        Σ·((Σ1′ + 𝑠 1𝑥) + Σ2 ) = Σ·((Σ1′ + Σ2 ) + 𝑠 1 𝑥)
                                               = Σ·(Σ1′ + Σ2 ) + 𝑠 1𝑟        (by deﬁnition)
                                               = (Σ·Σ1′ + Σ·Σ2 ) + 𝑠 1𝑟 (by induction hyp.)
                                               = (Σ·Σ1′ + 𝑠 1𝑟 ) + Σ·Σ2
                                               = Σ·(Σ1′ + 𝑠 1𝑥) + Σ·Σ2       (by deﬁnition)

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                         63




                                    return
                                    Γ ; Δ ⊢ 𝑒 : 𝜏 ; Σ1       𝑥Û = FV(𝑒) ∪ dom(Σ1 )
                                                             𝑥 ]𝜏 ; FP∞ (Û
                                       Γ ; Δ ⊢ return 𝑒 : [∅/Û           𝑥)
                             bind
                             Γ ; Δ ⊢ e 1 : 𝜏 1 ; Σ1      Γ, 𝑥 : 𝜏1 ; Δ + 0𝑥 ⊢ e2 : 𝜏2 ; Σ2
                               Γ ; Δ ⊢ 𝑥 : 𝜏1 ← e1 ; e2 : [∅/𝑥]𝜏2 ; Σ1 + [∅/𝑥]Σ2
                     if
                     Γ ; Δ ⊢ 𝑒1 : B ; Σ1           Γ ; Δ ⊢ e 2 : 𝜏 ; Σ2       Γ ; Δ ⊢ e 3 : 𝜏 ; Σ3
                                                                             ∞
                            Γ ; Δ ⊢ if 𝑒 1 then e2 else e3 : 𝜏 ; ⌉Σ1 ⌈ + (Σ2 ⊔ Σ3 )
    p-case
                                      Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1
    Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ e2 : 𝜏2 ; Σ2       Γ, 𝑦 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ12 ))𝑦 ⊢ e3 : 𝜏3 ; Σ3
                Γ ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } :
                              [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 ; ⌉Σ1 ⌈∞ ⊔ ([Σ11/𝑥]Σ2 ⊔ [Σ12/𝑦]Σ3 )
                  p-app
                                               Σ
                 Γ ; Δ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑠) −
                                           →→ 𝜏2 ; Σ1          Γ ; Δ ⊢ 𝑒 2 : 𝜏1 ; Σ2        Δ·Σ2 ≤ 𝑠
                                                                        ∞
                                    Γ ; Δ ⊢ e1 e2 : [Σ2/𝑥]𝜏2 ; ⌉Σ1 ⌈ + [Σ2/𝑥]Σ


                                      FP∞ (R) = ∅
                                       ∞
                                    FP (unit) = ∅
                                           Σ
                                           − 𝜏2 ) = [∅/𝑥]⌉Σ⌈∞ + FP∞ (𝜏1 ) + FP∞ ([∅/𝑥]𝜏2)
                          FP∞ ((𝑥 : 𝜏1 ·𝑠) →
                                           Σ
                      FP∞ ((𝑥 : 𝜏1 ·𝑠) −
                                       →→ 𝜏2 ) = [∅/𝑥]⌉Σ⌈∞ + FP∞ (𝜏1 ) + FP∞ ([∅/𝑥]𝜏2)
                         FP (𝜏1 ⊕ 𝜏2 ) = ⌉Σ1 ⌈∞ + ⌉Σ2 ⌈∞ + FP∞ (𝜏1 ) + FP∞ (𝜏2 )
                             ∞      Σ1 Σ2

                         FP∞ (𝜏1 Σ1 &Σ2 𝜏2 ) = ⌉Σ1 ⌈∞ + ⌉Σ2 ⌈∞ + FP∞ (𝜏1 ) + FP∞ (𝜏2 )
                         FP∞ (𝜏1 Σ1 ⊗ Σ2 𝜏2 ) = ⌉Σ1 ⌈∞ + ⌉Σ2 ⌈∞ + FP∞ (𝜏1 ) + FP∞ (𝜏2 )


                                      Fig. 21. 𝜆J : Complete privacy type system


and the result holds. Let us assume now that Σ2 = Σ2′ + 𝑠 2 𝑥, and that 𝑟 = Σ(𝑥) if Σ(𝑥) is deﬁned,
otherwise 𝑟 = 𝑥:
             Σ·((Σ1′ + 𝑠 1𝑥) + (Σ2′ + 𝑠 2𝑥)) = Σ·((Σ1′ + Σ2′ ) + 𝑠 1𝑥 + 𝑠 2 𝑥)
                                             = Σ·(Σ1′ + Σ2′ ) + (𝑠 1 + 𝑠 2 )𝑟
                                             = Σ·(Σ1′ + Σ2′ ) + (𝑠 1 + 𝑠 2 )𝑟        (by deﬁnition)
                                             = (Σ·Σ1′ + Σ·Σ2′ ) + (𝑠 1 + 𝑠 2 )𝑟 (by induction hyp.)
                                             = (Σ·Σ1′ + Σ·Σ2′ ) + 𝑠 1𝑟 + 𝑠 2𝑟
                                             = (Σ·Σ1′ + 𝑠 1𝑟 ) + (Σ·Σ2′ + 𝑠 2𝑟 )
                                             = (Σ·(Σ1′ + 𝑠 1𝑥) + Σ·(Σ2′ + 𝑠 2𝑥)      (by deﬁnition)

                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
64                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                       Σ1 ·∅ = 0
                                Σ1 ·(Σ2 + 𝑠) = Σ1 ·Σ2 + 𝑠
                               Σ1 ·(Σ2 + 𝑠𝑥) = Σ1 ·Σ2 + 𝑠Σ1 (𝑥) if Σ(𝑥) is deﬁned
                               Σ1 ·(Σ2 + 𝑠𝑥) = Σ1 ·Σ2 + 𝑠𝑥      otherwise



                                                Σ(R) = R
                                                Σ(B) = B
                                             Σ(unit) = unit
                                             Σ′ +𝑠                       Σ·Σ′ +𝑠
                                Σ((𝑥 : 𝜎1 ) −−−→ 𝜎2 ) = (𝑥 : Σ(𝜎1 )) −−−−−→ Σ(𝜎2 )
                               Σ(𝜎1 Σ1 +𝑠1 ⊕ Σ2 +𝑠2 𝜎2 ) = Σ(𝜎1 ) Σ·Σ1 +𝑠1 ⊕ Σ·Σ2 +𝑠2 Σ(𝜎2 )
                               Σ(𝜎1 Σ1 +𝑠1 &Σ2 +𝑠2 𝜎2 ) = Σ(𝜎1 ) Σ·Σ1 +𝑠1 &Σ·Σ2 +𝑠2 Σ(𝜎2 )
                               Σ(𝜎1 Σ1 +𝑠1 ⊗ Σ2 +𝑠2 𝜎2 ) = Σ(𝜎1 ) Σ·Σ1 +𝑠1 ⊗ Σ·Σ2 +𝑠2 Σ(𝜎2 )


              Fig. 22. Sensitivity instantiation / “dot product” and sensitivity type instantiation


and the result holds.                                                                                             ⊳
Case (3) Σ1 = Σ1′ + 𝑠 1
Subproof. Similar to previous case.                                                                               ⊳
                                                                                                                  
     Lemma C.2. If 𝑥 ∉ 𝑑𝑜𝑚(Σ), then 𝑠𝑥(Σ(𝜏)) = (Σ + 𝑠𝑥)(𝜏)
     Proof. By induction on 𝜏.                                                                                    
     Lemma C.3. If Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ·([Σ/𝑥]Σ ′) = (Δ + 𝑑𝑥)·Σ ′
  Proof. We prove: if Δ·Σ2 = 𝑑 ∈ sens and 𝑥 ∉ 𝑑𝑜𝑚(Σ2) ∪ 𝑑𝑜𝑚(Δ), then Δ·[Σ2/𝑥]Σ3 = 𝑑𝑥(Δ·Σ3 ).
We proceed by induction on the structure of Σ3 .
Case (1) Σ3 = ∅
Subproof. Trivial as [Σ2/𝑥]∅ = 𝑑𝑥(∅) = ∅ and Δ·∅ = 0.                                     ⊳
Case (2) 𝑥 ∉ 𝑑𝑜𝑚(Σ3)
Subproof. Then [Σ2/𝑥]Σ3 = Σ3 , Δ·[Σ2/𝑥]Σ3 = Δ·Σ3 , and [𝑠/𝑥](Δ·Σ3 ) = Δ·Σ3 , and the result
holds.                                                                                    ⊳




ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                         65




                                                                                                                               Σ <: Σ
                                                           △
                                         Σ <: Σ ′      ⇐⇒        ∀𝑥 . Σ(𝑥) ≤ Σ ′(𝑥)
                                                                                                                               Σ <: Σ
                         ′                   ′
               𝑝.𝜖 ≤ 𝑝 .𝜖        𝑝.𝛿 ≤ 𝑝 .𝛿                                                     Σ1 <: Σ1′    Σ2 <: Σ2′
                         𝑝𝑥 <: 𝑝 ′𝑥                              ∅ <: Σ                          Σ1 + Σ2′ <: Σ1′ + Σ2′

            Σ1 <: Σ1′ ∨ Σ1 <: Σ2′                    Σ1 <: Σ1′ ∧ Σ1 <: Σ1′                           Σ1 <: Σ1′ ∨ Σ2 <: Σ1′
                Σ1 <: Σ1′ ⊔ Σ2′                           Σ1 ⊔ Σ2 <: Σ1′                                    Σ1 ⊓ Σ2 <: Σ1′

                                                     Σ1 <: Σ1′ ∧ Σ1 <: Σ2′
                                                          Σ1 <: Σ1′ ⊓ Σ2′

                                                                                                                               𝜏 <: 𝜏
                  base                                s-lam
                  𝜏 ∈ {R, unit}                      𝜏1′ <: 𝜏1       𝑑 ′ <: 𝑑                   Σ <: Σ ′           𝜏2 <: 𝜏2′
                                                                        Σ                                     Σ′
                       𝜏 <: 𝜏                                          − 𝜏2 <: (𝑥 : 𝜏1′ ·𝑑 ′) −→ 𝜏2′
                                                           (𝑥 : 𝜏1 ·𝑑) →
                                  p-lam
                                 𝜏1′ <: 𝜏1           𝑑 ′ <: 𝑑        Σ <: Σ′                    𝜏2 <: 𝜏2′
                                                      Σ                                    Σ′
                                       (𝑥 : 𝜏1 ·𝑑) −
                                                   →→ 𝜏2 <: (𝑥 : 𝜏1′ ·𝑑 ′ ) −−→
                                                                              → 𝜏2′
                                sum
                                𝜏1 <: 𝜏1′           Σ1 <: Σ1′        𝜏2 <: 𝜏2′                  Σ2 <: Σ2′
                                                                       ′ Σ′1        Σ′2
                                                 𝜏1 Σ1 ⊕ Σ2 𝜏2 <: 𝜏1            ⊕         𝜏2′
                                pair
                                𝜏1 <: 𝜏1′           Σ1 <: Σ1′        𝜏2 <: 𝜏2′                  Σ2 <: Σ2′
                                                                       ′ Σ′1        Σ′2
                                                 𝜏1 Σ1 &Σ2 𝜏2 <: 𝜏1             &         𝜏2′
                                tup
                                𝜏1 <: 𝜏1′           Σ1 <: Σ1′        𝜏2 <: 𝜏2′                  Σ2 <: Σ2′
                                                                            ′        ′
                                                 𝜏1 Σ1 ⊗ Σ2 𝜏2 <: 𝜏1′ Σ1 ⊗ Σ2 𝜏2′




                                                      Fig. 23. Subtyping




                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
66                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                         [_/𝑥]_ : sensv × type → type
                                           [Σ/𝑥]R = R
                                           [Σ/𝑥]B = B
                                        [Σ/𝑥]unit = unit
                                              Σ′                             [Σ/𝑥]Σ′
                          [Σ/𝑥]((𝑦 : 𝜏1 ·𝑑) −→ 𝜏2 ) = (𝑦 : [Σ/𝑥]𝜏1 ·𝑑) −−−−−→ [Σ/𝑥]𝜏2
                             [Σ/𝑥](𝜏1 Σ1 ⊕ Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 ⊕[Σ/𝑥]Σ2 [Σ/𝑥]𝜏2
                             [Σ/𝑥](𝜏1 Σ1 &Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 &[Σ/𝑥]Σ2 [Σ/𝑥]𝜏2
                             [Σ/𝑥](𝜏1 Σ1 ⊗ Σ2 𝜏2 ) = [Σ/𝑥]𝜏1 [Σ/𝑥]Σ1 ⊗[Σ/𝑥]Σ2 [Σ/𝑥]𝜏2

                                         [_/𝑥]_ : sensv × sensv → sensv
                                                 [Σ/𝑥]∅ = ∅
                                          [Σ/𝑥](Σ ′ + 𝑠𝑥) = [Σ/𝑥]Σ + 𝑠Σ ′
                                          [Σ/𝑥](Σ ′ + 𝑠𝑦) = [Σ/𝑥]Σ + 𝑠𝑦

                               [_/𝑥]_ : sensv × (sensv + sens) → (sensv + sens)
                                          [Σ/𝑥](Σ ′ + 𝑠) = [Σ/𝑥]Σ ′ + 𝑠
                                                [Σ/𝑥]𝑠 = 𝑠



                                   Fig. 24. Sensitivity environment substitution



                                                ′
                                          ⌉𝑠 ⌈𝑠 = 𝑠 ′                    𝑠>0
                                               ′
                                         ⌉∅⌈𝑠 = ∅
                                               ′       ′    ′
                                   ⌉Σ + 𝑠𝑥 ⌈𝑠 = ⌉Σ⌈𝑠 + ⌉𝑠 ⌈𝑠 𝑥
                                               ′       ′
                                   ⌉Σ + 0𝑥 ⌈𝑠 = ⌉Σ⌈𝑠 + 0𝑥
                                               ′
                                         ⌉𝑝 ⌈𝑝 = 𝑝 ′                  𝑝 ≠ (0, 0)
                                               ′
                                     ⌉(0, 0)⌈𝑝 = (0, 0)
                                               ′
                                        ⌉∅⌈𝑝 = ∅
                                               ′       ′
                                       ⌉𝑝𝑥 ⌈𝑝 = ⌉𝑝 ⌈𝑝 𝑥
                                  ⌉Σ1 + Σ2 ⌈∞ = ⌉Σ1 ⌈∞ + ⌉Σ2 ⌈∞
                                  ⌉Σ1 ⊔ Σ2 ⌈∞ = ⌉Σ1 ⌈∞ ⊔ ⌉Σ2 ⌈∞
                                  ⌉Σ1 ⊓ Σ2 ⌈∞ = ⌉Σ1 ⌈∞ ⊓ ⌉Σ2 ⌈∞
                                               ′      Ã
                                        ⌉Σ⌈𝑝 =           (⌉Σ(𝑥)⌈1 𝑝)𝑥
                                                      𝑥 ∈𝑑𝑜𝑚(Σ)




                                                   Fig. 25. Lift operators




ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                         67




                                           _ ⊔ _ : type × type → type
                                                R⊔R =R
                                                B⊔B =B
                                          unit ⊔ unit = unit
                              Σ                     Σ′                                      Σ⊔Σ′
                            − 𝜏1 ⊔ (𝑦 : 𝜏1′ ·𝑑 ′ ) −→ 𝜏2′ = (𝑦 : (𝜏1 ⊓ 𝜏1′ )·(𝑑 ⊓ 𝑑 ′ )) −−−−→ (𝜏2 ⊔ 𝜏2′ )
                (𝑦 : 𝜏1 ·𝑑) →
                          Σ                        Σ′                                       Σ⊔Σ′
              (𝑦 : 𝜏1 ·𝑑) −
                          →→ 𝜏1 ⊔ (𝑦 : 𝜏1′ ·𝑑 ′) −−→
                                                   → 𝜏2′ = (𝑦 : (𝜏1 ⊓ 𝜏1′ )·(𝑑 ⊓ 𝑑 ′ )) −−−−→      → (𝜏2 ⊔ 𝜏2′ )
                                            ′   ′   ′   ′             ′       ⊔Σ′       ⊔Σ′
                            Σ    Σ            Σ    Σ
                         𝜏1 ⊕ 𝜏2 ⊔ (𝜏1 1 ⊕ 2 𝜏2 ) = (𝜏1 ⊔ 𝜏1 )
                              1    2                                      Σ 1    1⊕ Σ 2    2 (𝜏 2 ⊔ 𝜏 ′ )
                                               ′     ′                          ′         ′
                                                                                                     2
                         𝜏1 1 & 2 𝜏2 ⊔ (𝜏1 1 & 2 𝜏2 ) = (𝜏1 ⊔ 𝜏1 ) 1 1 & 2 2 (𝜏2 ⊔ 𝜏2′ )
                            Σ    Σ          ′ Σ    Σ    ′             ′   Σ   ⊔Σ    Σ   ⊔Σ
                                                ′   ′                           ′         ′
                         𝜏1 Σ1 ⊗ Σ2 𝜏2 ⊔ (𝜏1′ Σ1 ⊗ Σ2 𝜏2′ ) = (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 ⊗ Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ )

                                           _ ⊓ _ : type × type → type
                                                R⊓R =R
                                                B⊓B =B
                                          unit ⊓ unit = unit
                              Σ                     Σ′                                      Σ⊓Σ′
                            − 𝜏1 ⊓ (𝑦 : 𝜏1′ ·𝑑 ′ ) −→ 𝜏2′ = (𝑦 : (𝜏1 ⊔ 𝜏1′ )·(𝑑 ⊔ 𝑑 ′ )) −−−−→ (𝜏2 ⊓ 𝜏2′ )
                (𝑦 : 𝜏1 ·𝑑) →
                          Σ                        Σ′                                       Σ⊓Σ′
              (𝑦 : 𝜏1 ·𝑑) −
                          →→ 𝜏1 ⊓ (𝑦 : 𝜏1′ ·𝑑 ′) −−→
                                                   → 𝜏2′ = (𝑦 : (𝜏1 ⊔ 𝜏1′ )·(𝑑 ⊔ 𝑑 ′ )) −−−−→  → (𝜏2 ⊓ 𝜏2′ )
                                               ′    ′                          ′        ′
                         𝜏1 1 ⊕ 2 𝜏2 ⊓ (𝜏1 1 ⊕ 2 𝜏2 ) = (𝜏1 ⊓ 𝜏1 ) 1 1 ⊕ 2 2 (𝜏2 ⊓ 𝜏2′ )
                            Σ    Σ          ′ Σ    Σ    ′             ′   Σ  ⊓Σ    Σ  ⊓Σ
                                               ′     ′                         ′        ′
                         𝜏1 Σ1 &Σ2 𝜏2 ⊓ (𝜏1′ Σ1 &Σ2 𝜏2′ ) = (𝜏1 ⊓ 𝜏1′ ) Σ1 ⊓Σ1 &Σ2 ⊓Σ2 (𝜏2 ⊓ 𝜏2′ )
                                               ′    ′                          ′        ′
                         𝜏1 Σ1 ⊗ Σ2 𝜏2 ⊓ (𝜏1′ Σ1 ⊗ Σ2 𝜏2′ ) = (𝜏1 ⊓ 𝜏1′ ) Σ1 ⊓Σ1 ⊗ Σ2 ⊓Σ2 (𝜏2 ⊓ 𝜏2′ )

                                        _ ⊔ _ : sensv × 𝑠𝑒𝑛𝑠𝑣 → 𝑠𝑒𝑛𝑠𝑣
                                       ∅⊔∅=∅
                        (Σ + 𝑠𝑥) ⊔ (Σ ′ + 𝑠 ′𝑥) = (Σ ⊔ Σ ′) + (𝑠 ⊔ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊔ Σ ′)
                               Σ ⊔ (Σ ′ + 𝑠𝑥) = (Σ ⊔ Σ ′) + 𝑠𝑥               (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                               (Σ + 𝑠𝑥) ⊔ Σ ′ = (Σ ⊔ Σ ′) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ ′))
                                        _ ⊔ _ : sensv × 𝑠𝑒𝑛𝑠𝑣 → 𝑠𝑒𝑛𝑠𝑣
                                       ∅⊓∅=∅
                        (Σ + 𝑠𝑥) ⊓ (Σ ′ + 𝑠 ′𝑥) = (Σ ⊓ Σ ′) + (𝑠 ⊓ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊓ Σ ′)
                               Σ ⊓ (Σ ′ + 𝑠𝑥) = (Σ ⊓ Σ ′)                    (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                               (Σ + 𝑠𝑥) ⊓ Σ ′ = (Σ ⊓ Σ ′)                   (𝑥 ∉ 𝑑𝑜𝑚(Σ ′))


                          Fig. 26. Join and Meet of types and sensitivity environments




                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
68                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                     plus                                               times
          rlit                     𝛾 ⊢ 𝑒 1 ⇓𝑘1 𝑟 1           𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑟 2            𝛾 ⊢ 𝑒 1 ⇓𝑘2 𝑟 1           𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑟 2
          𝛾 ⊢ 𝑟 ⇓0 𝑟                  𝛾 ⊢ 𝑒 1 + 𝑒 2 ⇓𝑘1 +𝑘2 +1 𝑟 1 + 𝑟 2                       𝛾 ⊢ 𝑒 1 ·𝑒 2 ⇓𝑘1 +𝑘2 +1 𝑟 1𝑟 2
        leq                                                  var                   lam
       𝛾 ⊢ 𝑒 1 ⇓𝑘1 𝑟 1           𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑟 2             𝛾(𝑥) = 𝑣                   𝛾′ ⊆ 𝛾            𝐹𝑉 (𝑒) = 𝑑𝑜𝑚(𝛾 ′)
                                                                                         s                          s
         𝛾 ⊢ 𝑒 1 ≤ 𝑒 2 ⇓𝑘1 +𝑘2 +1 𝑟 1 ≤ 𝑟 2                 𝛾 ⊢ 𝑥 ⇓1 𝑣            𝛾 ⊢ 𝜆 (𝑥 : 𝜏 ·𝑠). 𝑒 ⇓1 h𝜆 𝑥 : 𝜏 ·𝑠. 𝑒, 𝛾 ′ i
         app
        𝛾 ⊢ 𝑒 1 ⇓𝑘1 h𝜆𝑥 : 𝜏 ·𝑠. 𝑒 ′, 𝛾 ′i            𝛾 ⊢ 𝑒 ⇓𝑘2 𝑣           𝛾 ′[𝑥 ↦→ 𝑣] ⊢ 𝑒 ′ ⇓𝑘3 𝑣                  unit

                                         𝛾 ⊢ 𝑒 1 𝑒 ⇓𝑘1 +𝑘2 +𝑘3 +1 𝑣                                                 𝛾 ⊢ tt ⇓0 tt
                           inl                                                  inr
                                     𝛾 ⊢ 𝑒 ⇓𝑘 𝑣                                          𝛾 ⊢ 𝑒 ⇓𝑘 𝑣
                          𝛾 ⊢ inl𝜏2 𝑒 ⇓𝑘 inl𝜏2 /𝛾 𝑣                            𝛾 ⊢ inr𝜏1 𝑒 ⇓𝑘 inr𝜏1 /𝛾 𝑣
                                      case-left
                                         𝛾 ⊢ 𝑒 1 ⇓𝑘1 inl 𝑣            𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 2 ⇓𝑘2 𝑣 ′
                                     𝛾 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑥 ⇒ 𝑒 3 } ⇓𝑘1 +𝑘2 +1 𝑣 ′
          case-right                                                                    pair
               𝛾 ⊢ 𝑒 1 ⇓𝑘1 inr 𝑣            𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 3 ⇓𝑘2 𝑣 ′                    𝛾 ⊢ 𝑒 1 ⇓𝑘1 𝑣 1            𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑣 2
          𝛾 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑥 ⇒ 𝑒 3 } ⇓𝑘1 +𝑘2 +1 𝑣 ′                               𝛾 ⊢ (𝑒 1 , 𝑒 2 ) ⇓𝑘1 +𝑘2 (𝑣 1, 𝑣 2 )

              proj1                                proj2                              tup
              𝛾 ⊢ 𝑒 ⇓𝑘 (𝑣 1, 𝑣 2 )                 𝛾 ⊢ 𝑒 ⇓𝑘 (𝑣 1, 𝑣 2 )               𝛾 ⊢ 𝑒 1 ⇓𝑘1 𝑣 1           𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑣 2
           𝛾 ⊢ fst 𝑒 ⇓𝑘+1 𝑣 1                   𝛾 ⊢ snd 𝑒 ⇓𝑘+1 𝑣 2                       𝛾 ⊢ h𝑒 1 , 𝑒i ⇓𝑘1 +𝑘2 h𝑣 1 , 𝑣 2 i
               untup                                                                                      ascr
               𝛾 ⊢ 𝑒 1 ⇓𝑘1 h𝑣 1, 𝑣 2 i       𝛾[𝑥 1 ↦→ 𝑣 1, 𝑥 2 ↦→ 𝑣 2 ] ⊢ 𝑒 2 ⇓𝑘2 𝑣 ′                        𝛾 ⊢ 𝑒 ⇓𝑘 𝑣
                           𝛾 ⊢ let 𝑥 1, 𝑥 2 = 𝑒 1 in 𝑒 2 ⇓𝑘1 +𝑘2 +1 𝑣 ′                                  𝛾 ⊢ 𝑒 :: 𝜏 ⇓𝑘+1 𝑣
                                                           if-true
                         blit                                    𝛾 ⊢ 𝑒 1 ⇓𝑘1 true            𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑣
                         𝛾 ⊢ 𝑏 ⇓0 𝑏                        𝛾 ⊢ if 𝑒 1 then {𝑒 2 } else {𝑒 3 } ⇓𝑘1 +𝑘2 +1 𝑣
         if-false                                                              let
                𝛾 ⊢ 𝑒 1 ⇓𝑘1 false           𝛾 ⊢ 𝑒 3 ⇓𝑘2 𝑣                      𝛾 ⊢ 𝑒 1 ⇓𝑘1 𝑣           𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 2 ⇓𝑘2 𝑣 ′
         𝛾 ⊢ if 𝑒 1 then {𝑒 2 } else {𝑒 3 } ⇓𝑘1 +𝑘2 +1 𝑣                         𝛾 ⊢ let 𝑥 = 𝑒 1 in 𝑒 2 ⇓𝑘1 +𝑘2 +1 𝑣 ′




                                         Fig. 27. 𝜆J : Sensitivity dynamic semantics




ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                    69



                                        return
                                                     𝛾 ⊢ 𝑒 ⇓𝑘 𝑣
                                                        ß
                                                          1     when  𝑥 =𝑣
                                        return 𝑒 ⇓𝑘 𝜆𝑥.
                                                          0 otherwise

  bind                                                                         gauss
  𝛾 ⊢ e1 ⇓𝑘 𝐷 1      ∀𝑣𝑖 , 𝐷 1 (𝑣𝑖 ) > 0, 𝛾[𝑥 ↦→ 𝑣𝑖 ] ⊢ e2 ⇓𝑘𝑖 𝐷 2𝑖
                                             Õ                                                                        2
                                                                                                            𝑒 −(𝑥 −𝜇) /2𝜎
                                                                                                                            2
   𝛾 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 ⇓𝑘+max𝑖 𝑘𝑖 𝜆𝑥.              𝐷 1 (𝑣𝑖 )·𝐷 2𝑖 (𝑥)        𝛾 ⊢ gauss 𝜇 𝜎 2 ⇓1 𝜆𝑥. Í
                                                                                                                    −(𝑦−𝜇)2/2𝜎 2
                                            𝐷 1 (𝑣𝑖 )>0                                                    𝑦 ∈Z 𝑒

              if-true                                                    if-false
                𝛾 ⊢ 𝑒 1 ⇓𝑘1 true       𝛾 ⊢ e2 ⇓𝑘2 𝐷                        𝛾 ⊢ 𝑒 1 ⇓𝑘1 false    𝛾 ⊢ e3 ⇓𝑘2 𝐷
             𝛾 ⊢ if 𝑒 1 then e2 else e3 ⇓𝑘1 +𝑘2 𝐷                        𝛾 ⊢ if 𝑒 1 then e2 else e3 ⇓𝑘1 +𝑘2 𝐷

      case-left                                                      case-right
       𝛾 ⊢ 𝑒 ⇓𝑘1 inl 𝑣          𝛾[𝑥 ↦→ 𝑣] ⊢ e2 ⇓𝑘2 𝐷                  𝛾 ⊢ 𝑒 ⇓𝑘1 inr 𝑣          𝛾[𝑥 ↦→ 𝑣] ⊢ e3 ⇓𝑘2 𝐷
     𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓𝑘1 +𝑘2 𝐷                     𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓𝑘1 +𝑘2 𝐷

                      app
                                    p
                      𝛾 ⊢ 𝑒 1 ⇓𝑘1 h𝜆 𝑥 : 𝜏·𝑠. e′, 𝛾 ′ i     𝛾 ⊢ 𝑒 2 ⇓𝑘2 𝑣        𝛾 ′ [𝑥 ↦→ 𝑣] ⊢ e′ ⇓𝑘3 𝐷
                                                    𝛾 ⊢ e1 e2 ⇓𝑘1 +𝑘2 +𝑘3 𝐷




                                           Fig. 28. 𝜆J : Probabilistic semantics




                                        ∅⊔∅=∅
                         (Σ + 𝑠𝑥) ⊔ (Σ ′ + 𝑠 ′𝑥) = (Σ ⊔ Σ ′) + (𝑠 ⊔ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊔ Σ ′)
                                 Σ ⊔ (Σ ′ + 𝑠𝑥) = (Σ ⊔ Σ ′) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                                (Σ + 𝑠𝑥) ⊔ Σ ′ = (Σ ⊔ Σ ′) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ ′))
                            (Σ + 𝑠) ⊔ (Σ ′ + 𝑠 ′) = (Σ ⊔ Σ ′) + (𝑠 ⊔ 𝑠 ′)      𝑠 ′′ ∉ Σ ⊔ Σ ′
                                         _ ⊔ _ : sensv × 𝑠𝑒𝑛𝑠𝑣 → 𝑠𝑒𝑛𝑠𝑣
                                        ∅⊓∅=∅
                         (Σ + 𝑠𝑥) ⊓ (Σ ′ + 𝑠 ′𝑥) = (Σ ⊓ Σ ′) + (𝑠 ⊓ 𝑠 ′)𝑥 𝑥 ∉ 𝑑𝑜𝑚(Σ ⊓ Σ ′)
                                 Σ ⊓ (Σ ′ + 𝑠𝑥) = (Σ ⊓ Σ ′) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ))
                                (Σ + 𝑠𝑥) ⊓ Σ ′ = (Σ ⊓ Σ ′) + 𝑠𝑥              (𝑥 ∉ 𝑑𝑜𝑚(Σ ′))
                            (Σ + 𝑠) ⊓ (Σ ′ + 𝑠 ′) = (Σ ⊓ Σ ′) + (𝑠 ⊓ 𝑠 ′)      𝑠 ′′ ∉ Σ ⊓ Σ ′


                        Fig. 29. Join and Meet of sensitivity environment and sensitivities




                                   ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
70                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter




                                                                                                                        𝜎 <: 𝜎
                                         s-fun
           base
                                       𝜎1′ <: 𝜎1          𝑠 ′ <: 𝑠           Σ1 <: Σ2′          Σ2 <: Σ2′           𝜎2 <: 𝜎2′
           𝜎 ∈ {R, unit}
                                                                  Σ1 +Σ·Σ2                             Σ′1 +Σ·Σ′2
                𝜎 <: 𝜎                           (𝑥 : 𝜎1 ·𝑠) −−−−−−→ 𝜎2 <: (𝑥 : 𝜎1′ ·𝑠 ′) −−−−−−→ 𝜎2′
                         p-fun
                         𝜎1′ <: 𝜎1        𝑠 ′ <: 𝑠        Σ1 <: Σ2′              Σ2 <: Σ2′          𝜎2 <: 𝜎2′
                                             Σ1 +Σ•Σ2                                  Σ′1 +Σ•Σ′2
                                 (𝑥 : 𝜎1 ·𝑠) −−−−−−−
                                                   →→ 𝜎2 <: (𝑥 : 𝜎1′ ·𝑠 ′ ) −
                                                                            −−−−−−
                                                                                 →→ 𝜎2′
                                   sum
                                   𝜎1 <: 𝜎1′         𝑠 1 ≤ 𝑠 1′        𝜎2 <: 𝜎2′          𝑠 2 ≤ 𝑠 2′
                                                                         ′ 𝑠1′   𝑠2′
                                               𝜎1 𝑠1 ⊕𝑠2 𝜎2 <: 𝜎1 ⊕ 𝜎2′
                                   pair
                                   𝜎1 <: 𝜎1′         𝑠 1 ≤ 𝑠 1′        𝜎2 <: 𝜎2′          𝑠 2 ≤ 𝑠 2′
                                                                             ′    ′
                                               𝜎1 𝑠1 &𝑠2 𝜎2 <: 𝜎1′ 𝑠1 &𝑠2 𝜎2′
                                   tup
                                   𝜎1 <: 𝜎1′         𝑠 1 ≤ 𝑠 1′        𝜎2 <: 𝜎2′          𝑠 2 ≤ 𝑠 2′
                                                                             ′    ′
                                               𝜎1 𝑠1 ⊗𝑠2 𝜎2 <: 𝜎1′ 𝑠1 ⊗𝑠2 𝜎2′




                                          Fig. 30. Subtyping of sensible types




ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       71


Case (3) Σ3 = Σ4 + 𝑑 ′𝑥
Subproof. By induction hypothesis on Σ4 , we know that Δ·([Σ2/𝑥]Σ4) = 𝑑𝑥((Δ·Σ4 )). Therefore
                     Δ·([Σ2/𝑥]Σ3) = Δ·([Σ2/𝑥](Σ4 + 𝑑 ′𝑥))
                                  = Δ·([Σ2/𝑥]Σ4 + 𝑑 ′ Σ2 )
                                  = Δ·([Σ2/𝑥]Σ4) + Δ·𝑑 ′ Σ2
                                  = Δ·([Σ2/𝑥]Σ4) + 𝑑 ′(Δ·Σ2 )
                                  = 𝑑𝑥(Δ·Σ4 ) + 𝑑 ′ (Δ·Σ2 )       (by induction hyp.)
                                  = 𝑑𝑥(Δ·Σ4 ) + 𝑑 ′ (𝑑𝑥(𝑥))
                                  = 𝑑𝑥(Δ·Σ4 ) + 𝑑𝑥(𝑑 ′𝑥)
                                  = 𝑑𝑥((Δ·Σ4 ) + 𝑑 ′𝑥)        (by deﬁnition of subst)
                                  = 𝑑𝑥(Δ·(Σ4 + 𝑑 ′𝑥))           (because 𝑥 ∉ 𝑑𝑜𝑚(Δ))
                                  = 𝑑𝑥(Δ·Σ3 )
And the result holds.                                                                                                  ⊳
Case (4) Σ3 = Σ4 + 𝑑 ′𝑦
Subproof. By induction hypothesis on Σ4 , we know that Δ·([Σ2/𝑥]Σ4) = 𝑑𝑥(Δ·Σ4 ). Therefore
                  Δ·([Σ2/𝑥]Σ3) = Δ·([Σ2/𝑥](Σ4 + 𝑑 ′𝑦))
                               = Δ·([Σ2/𝑥]Σ4 + 𝑑 ′𝑦)
                               = Δ·([Σ2/𝑥]Σ4) + Δ·𝑑 ′𝑦
                               = 𝑑𝑥(Δ·Σ4 ) + Δ·𝑑 ′𝑦              (by induction hyp.)
                               = 𝑑𝑥(Δ·Σ4 + Δ·𝑑 ′𝑦)     (by deﬁnition as 𝑥 ∉ 𝑑𝑜𝑚(𝑠𝑦))
                               = 𝑑𝑥(Δ·(Σ4 + 𝑑 ′𝑦))
                               = 𝑑𝑥(Δ·Σ3 )
And the result holds.                                                                                                  ⊳
Case (5) Σ3 = Σ4 + 𝑑 ′
Subproof. By induction hypothesis on Σ4 , we know that Δ·([Σ2/𝑥]Σ4) = 𝑑𝑥(Δ·Σ4 ). Therefore
                         Δ·([Σ2/𝑥]Σ3) = Δ·([Σ2/𝑥](Σ4 + 𝑑 ′ ))
                                      = Δ·([Σ2/𝑥]Σ4 + 𝑑 ′ )
                                      = Δ·([Σ2/𝑥]Σ4) + 𝑠 ′
                                      = 𝑑𝑥(Δ·Σ4 ) + 𝑠 ′        (by induction hyp.)
                                      = 𝑑𝑥(Δ·Σ4 + 𝑠 ′ )       (by deﬁnition of Σ() )
                                      = 𝑑𝑥(Δ·(Σ4 + 𝑠 ′ ))
                                      = 𝑑𝑥(Δ·Σ3 )
And the result holds.                                                                                                 ⊳
                                                                                                                      
  Lemma C.4. If Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ•([Σ/𝑥]Σ′) = (Δ + 𝑑𝑥)•Σ′
  Proof. We prove: if Δ·Σ2 = 𝑑 ∈ sens and 𝑥 ∉ 𝑑𝑜𝑚(Σ2) ∪ 𝑑𝑜𝑚(Δ), then Δ•[Σ2/𝑥]Σ3 = 𝑑𝑥 •(Δ•Σ3 ).
We proceed by induction on the structure of Σ3 .
Case (1) Σ3 = ∅
Subproof. Trivial as [Σ2/𝑥]∅ = 𝑑𝑥(∅) = ∅ and Δ•∅ = 0.                                      ⊳
Case (2) Σ3 = 𝑝𝑦
Subproof. Then [Σ2/𝑥]Σ3 = Σ3 , Δ•[Σ2/𝑥]Σ3 = Δ•Σ3 , and [𝑑/𝑥](Δ•Σ3 ) = Δ•Σ3 , and the result
holds.                                                                                     ⊳
Case (3) Σ3 = 𝑝𝑥

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
72                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Subproof. Then
                                          Δ•([Σ2/𝑥]Σ3 ) = Δ•([Σ2/𝑥](𝑝𝑥))
                                                        = Δ•(⌉Σ2Ã ⌈𝑝 )
                                                        =Δ(•            𝑝𝑦)
                                                             Ã
                                                             𝑥 ∈𝑑𝑜𝑚(Σ2 )
                                                        =           𝑝
                                                             𝑥 ∈𝑑𝑜𝑚(Σ2 )
                                                           =𝑝
But (Δ + 𝑑𝑥)•Σ3 = (Δ + 𝑑𝑥)•𝑝𝑥 = 𝑝 and the result holds.                                     ⊳
Case (4) Σ3 = Σ4 + Σ5
Subproof. By induction hypothesis on Σ4 and Σ5 , we know that Δ•([Σ2/𝑥]Σ4) = 𝑑𝑥 •(Δ·Σ4 ), and
Δ•([Σ2/𝑥]Σ5) = 𝑑𝑥 •(Δ·Σ5 ). Therefore
                    Δ•([Σ2/𝑥]Σ3) = Δ•([Σ2/𝑥](Σ4 + Σ5 ))
                                 = Δ•([Σ2/𝑥]Σ4 + [Σ2/𝑥]Σ5 )
                                 = Δ•([Σ2/𝑥]Σ4 ) + Δ([Σ2/𝑥]Σ5 )
                                 = 𝑑𝑥 •(Δ•Σ4 ) + 𝑑𝑥(Δ•Σ5 )         (by induction hyp.)
                                 = 𝑑𝑥 •(Δ•Σ4 + Δ•Σ5 )           (by deﬁnition of Δ(_))
                                 = 𝑑𝑥 •(Δ(Σ4 + Σ5 ))
                                 = 𝑑𝑥 •(Δ•Σ3 )
And the result holds.                                                                       ⊳
Case (5) Σ3 = Σ4 ⊔ Σ5
Subproof. By induction hypothesis on Σ4 and Σ5 , we know that Δ•([Σ2/𝑥]Σ4) = 𝑑𝑥 •(Δ·Σ4 ), and
Δ•([Σ2/𝑥]Σ5) = 𝑑𝑥 •(Δ·Σ5 ). Therefore
                   Δ•([Σ2/𝑥]Σ3) = Δ•([Σ2/𝑥](Σ4 ⊔ Σ5 ))
                                = Δ•([Σ2/𝑥]Σ4 ⊔ [Σ2/𝑥]Σ5)
                                = Δ•([Σ2/𝑥]Σ4 ) ⊔ Δ•([Σ2/𝑥]Σ5 )
                                = 𝑑𝑥 •(Δ•Σ4 ) ⊔ 𝑑𝑥 •(Δ•Σ5 )        (by induction hyp.)
                                = 𝑑𝑥 •(Δ•Σ4 ⊔ Δ•Σ5 )            (by deﬁnition of Δ(_))
                                = 𝑑𝑥 •(Δ•(Σ4 ⊔ Σ5 ))
                                = 𝑑𝑥 •(Δ•Σ3 )
And the result holds.                                                                       ⊳
Case (6) Σ3 = Σ4 ⊓ Σ5
Subproof. By induction hypothesis on Σ4 and Σ5 , we know that Δ•([Σ2/𝑥]Σ4) = 𝑑𝑥 •(Δ·Σ4 ), and
Δ•([Σ2/𝑥]Σ5) = 𝑑𝑥 •(Δ·Σ5 ). Therefore
                   Δ•([Σ2/𝑥]Σ3) = Δ•([Σ2/𝑥](Σ4 ⊓ Σ5 ))
                                = Δ•([Σ2/𝑥]Σ4 ⊓ [Σ2/𝑥]Σ5)
                                = Δ•([Σ2/𝑥]Σ4 ) ⊓ Δ•([Σ2/𝑥]Σ5 )
                                = 𝑑𝑥 •(Δ•Σ4 ) ⊓ 𝑑𝑥 •(Δ•Σ5 )        (by induction hyp.)
                                = 𝑑𝑥 •(Δ•Σ4 ⊓ Δ•Σ5 )            (by deﬁnition of Δ(_))
                                = 𝑑𝑥 •(Δ•(Σ4 ⊓ Σ5 ))
                                = 𝑑𝑥 •(Δ•Σ3 )
And the result holds.                                                                                             ⊳
                                                                                                                  
     Lemma C.5. Let Δ·Σ = 𝑑 and 𝑥 ∉ 𝑑𝑜𝑚(Σ) ∪ 𝑑𝑜𝑚(Δ), then Δ([Σ/𝑥]𝜏) = 𝑑𝑥(Δ(𝜏))

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                             73


  Proof. We prove: let Δ·Σ ′ = 𝑑 ∈ sens and 𝑥 ∉ 𝑑𝑜𝑚(Σ ′) ∪ 𝑑𝑜𝑚(Δ), then Δ([Σ ′/𝑥]𝜏) = 𝑑𝑥(Δ(𝜏)).
We proceed by induction on 𝜏.
Case (1) 𝜏 ∈ {R, B, unit}
Subproof. Trivial as Δ(𝜏) = 𝜏 and 𝑠𝑥(𝜏) = 𝜏.                                                 ⊳
                         Σ′′
Case (2) 𝜏 = (𝑥 : 𝜏1 ) −−→ 𝜏2
Subproof.
                               Σ′′                                   [Σ′ /𝑥]Σ′′
   Δ([Σ ′/𝑥]((𝑥 : 𝜏1 ·𝑑 ′) −−→ 𝜏2 )) = Δ((𝑥 : [Σ ′/𝑥]𝜏1 ·𝑑 ′ ) −−−−−−→ [Σ ′/𝑥]𝜏2 )                       (by def subst.)
                                                                       Δ·([Σ′ /𝑥]Σ′′ )
                                          = (𝑥 : Δ([Σ ′/𝑥]𝜏1 ·𝑑 ′ )) −−−−−−−−−→ Δ([Σ ′/𝑥]𝜏2 )         (by def inst.)
                                                              ′    Δ·([Σ′ /𝑥]Σ′′ )
                                          = (𝑥 : 𝑑𝑥(Δ(𝜏1 ))·𝑑 ) −−−−−−−−−→ 𝑑𝑥(Δ(𝜏2 ))         (by induction hyp.)
                                                              ′   𝑑𝑥(Δ·Σ′′ )
                                          = (𝑥 : 𝑑𝑥(Δ(𝜏1 ))·𝑑 ) −−−−−−−→ 𝑑𝑥(Δ(𝜏2 ))               (by Lemma 7.3)
                                                                 Δ·Σ  ′′
                                          = 𝑑𝑥((𝑥 : Δ(𝜏1 )·𝑑 ′) −−−→ Δ(𝜏2 ))                        (by def subst.)
                                                                Σ′′
                                          = 𝑑𝑥(Δ((𝑥 : 𝜏1 ·𝑑 ′) −−→ 𝜏2 ))                              (by def inst.)
and the result holds.                                                                                                        ⊳
                                Σ′′
Case (3) 𝜏 = (𝑥 : 𝜏1 ·𝑑 ′ ) −−→ 𝜏2
Subproof.
                           Σ′′                                       [Σ′ /𝑥]Σ′′
  Δ([Σ ′/𝑥]((𝑥 : 𝜏1 ·𝑑 ′ ) −−→ 𝜏2 )) = Δ((𝑥 : [Σ ′/𝑥]𝜏1 ·𝑑 ′) −−−−−−−→ [Σ ′/𝑥]𝜏2 )                        (by def subst.)
                                                                       Δ•([Σ′ /𝑥]Σ′′)
                                          = (𝑥 : Δ([Σ ′/𝑥]𝜏1 )·𝑑 ′ ) −−−−−−−−−→ Δ([Σ ′/𝑥]𝜏2 )         (by def inst.)
                                                                ′   Δ•([Σ′ /𝑥]Σ′′)
                                          = (𝑥 : 𝑑𝑥(Δ(𝜏1 ))·𝑑 ) −−−−−−−−−→ 𝑑𝑥(Δ(𝜏2 ))         (by induction hyp.)
                                                                            ′′
                                                                ′ 𝑑𝑥(Δ Σ )
                                                                         •

                                          = (𝑥 : 𝑑𝑥(Δ(𝜏1 ))·𝑑 ) −−−−−−−→ 𝑑𝑥(Δ(𝜏2 ))               (by Lemma 7.4)
                                                              ′    Δ•Σ′′
                                          = 𝑑𝑥((𝑥 : Δ(𝜏1 )·𝑑 ) −−−−→ Δ(𝜏2 ))                        (by def subst.)
                                                            ′     Σ′′
                                          = 𝑑𝑥(Δ((𝑥 : 𝜏1 ·𝑑 ) −−→ 𝜏2 ))                               (by def inst.)
and the result holds.                                                                                                        ⊳
Case (4) 𝜏 = 𝜏1 Σ1 ⊕ Σ2 𝜏2
Subproof.
                                                 ′           ′
     Δ([Σ ′/𝑥](𝜏1 Σ1 ⊕ Σ2 𝜏2 )) = Δ([Σ ′/𝑥]𝜏1 [Σ /𝑥]Σ1 ⊕[Σ /𝑥]Σ2 [Σ ′/𝑥]𝜏2 )              (by def subst.)
                                                     ′             ′
                                = Δ([Σ ′/𝑥]𝜏1 ) Δ·[Σ /𝑥]Σ1 ⊕ Δ·[Σ /𝑥]Σ2 Δ([Σ ′/𝑥]𝜏2)        (by def inst.)
                                                  ′            ′
                                = 𝑑𝑥(Δ(𝜏1 )) Δ·[Σ /𝑥]Σ1 ⊕ Δ·[Σ /𝑥]Σ2 𝑑𝑥(Δ(𝜏2 ))      (by induction hyp.)
                                = 𝑑𝑥(Δ(𝜏1 )) 𝑑𝑥(Δ·Σ1 ) ⊕𝑑𝑥(Δ·Σ2 ) 𝑑𝑥(Δ(𝜏2 ))             (by Lemma 7.3)
                                = 𝑑𝑥(Δ(𝜏1 ) (Δ·Σ1 ) ⊕(Δ·Σ2 ) Δ(𝜏2 ))                      (by def subst.)
                                = 𝑑𝑥(Δ(𝜏1 Σ1 ⊕ Σ2 𝜏2 ))                                     (by def inst.)
and the result holds.                                                                                                        ⊳
Case (5) 𝜏 = 𝜏1 Σ1 &Σ2 𝜏2
Subproof. Analogous to 𝜏 = 𝜏1 Σ1 ⊕ Σ2 𝜏2 case.                                                                              ⊳
                                                                                                                            
  Lemma C.6. If 𝜏 <: 𝜏 ′ then Σ(𝜏) <: Σ(𝜏 ′)
  Proof. By induction on 𝜏:
Case (1) 𝜏 = R
Subproof. Then 𝜏 ′ = R so the result is trivial.                                                                             ⊳

                                      ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
74                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Case (2) 𝜏 = B
Subproof. Then 𝜏 ′ = B so the result is trivial.                                                                      ⊳
Case (3) 𝜏 = unit
Subproof. Then 𝜏 ′ = unit so the result is trivial.                                                                   ⊳
                              Σ′
Case (4) 𝜏 = (𝑥 : 𝜏1 ·𝑑) −→ 𝜏2
                                             Σ′′
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑑 ′ ) −−→ 𝜏2′ such that 𝑑 ′ <: 𝑑, 𝜏1′ <: 𝜏1, Σ ′ <: Σ ′′ , and 𝜏2 <: 𝜏2′ . But
                 Σ′                            Σ·Σ′
Σ((𝑥 : 𝜏1 ·𝑑) −→ 𝜏2 ) = (𝑥 : Σ(𝜏1 )·𝑑) −−−→ Σ(𝜏2 ), then by induction hypotheses Σ(𝜏1′ ) <: Σ(𝜏1 ), and
Σ(𝜏2 ) <: Σ(𝜏2′ ). Also by Lemma C.12, Σ·Σ ′ <: Σ·Σ ′′ , therefore
                Σ′                          Σ·Σ′                            Σ·Σ′′                         Σ′′
Σ((𝑥 : 𝜏1 ·𝑑) −→ 𝜏2 ) = (𝑥 : Σ(𝜏1 )·𝑑) −−−→ Σ(𝜏2 ) <: (𝑥 : Σ(𝜏1′ )·𝑑 ′ ) −−−→ Σ(𝜏2′ ) = Σ((𝑥 : 𝜏1′ ·𝑑 ′ ) −−→ 𝜏2′ ) and
the result holds.                                                                                                     ⊳
                              Σ′
Case (5) 𝜏 = (𝑥 : 𝜏1 ·𝑑) −−→
                           → 𝜏2
                                            Σ′′
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑑 ′ ) −−→
                                       → 𝜏2′ such that 𝑑 ′ <: 𝑑, 𝜏1′ <: 𝜏1 , Σ′ <: Σ′′ , and 𝜏2 <: 𝜏2′ . But
                Σ′                            Σ·Σ′
                                           → Σ(𝜏2 ), then by induction hypotheses Σ(𝜏1′ ) <: Σ(𝜏1 ), and
                → 𝜏2 ) = (𝑥 : Σ(𝜏1 )·𝑑) −−−→
Σ((𝑥 : 𝜏1 ·𝑑) −−→
Σ(𝜏2 ) <: Σ(𝜏2 ). Also by Lemma C.13, Σ·Σ′ <: Σ·Σ′′ , therefore
              ′
                Σ′                           Σ·Σ′                              Σ·Σ′′                            Σ′′
                → 𝜏2 ) = (𝑥 : Σ(𝜏1 )·𝑑) −−−→
Σ((𝑥 : 𝜏1 ·𝑑) −−→                            → Σ(𝜏2 ) <: (𝑥 : Σ(𝜏1′ )·𝑑 ′ ) −−−−→
                                                                                → Σ(𝜏2′ ) = Σ((𝑥 : 𝜏1′ ·𝑑 ′) −−→
                                                                                                               → 𝜏2′ )
and the result holds.                                                                                              ⊳
                   Σ
Case (6) 𝜏 = 𝜏1 ⊕ 𝜏2 1  Σ 2
                                ′    ′
Subproof. Then 𝜏 ′ = 𝜏1′ Σ1 ⊕ Σ2 𝜏2′ such that 𝜏1 <: 𝜏1′, Σ1 <: Σ1′ , Σ2′ <: Σ2′ , and 𝜏2 <: 𝜏2′ . But Σ(𝜏1 Σ1 ⊕ Σ2
𝜏2 ) = Σ(𝜏1 ) Σ·Σ1 ⊕ Σ ·Σ2 Σ(𝜏2 ), then by induction hypotheses Σ(𝜏1 ) <: Σ(𝜏1′ ), and Σ(𝜏2 ) <: Σ(𝜏2′ ). Also
by Lemma C.12, Σ·Σ1 <: Σ·Σ1′ and Σ·Σ2 <: Σ·Σ2′ , therefore
                                                            ′      ′                     ′  ′
Σ(𝜏1 Σ1 ⊕ Σ2 𝜏2 ) = Σ(𝜏1 ) Σ·Σ1 ⊕ Σ·Σ2 Σ(𝜏2 ) <: Σ(𝜏1′ ) Σ·Σ1 ⊕ Σ·Σ2 Σ(𝜏2′ ) = Σ(𝜏1′ Σ1 ⊕ Σ2 𝜏2′ ) and the result
holds.                                                                                                             ⊳
Case (7) 𝜏 = 𝜏1 Σ1 &Σ2 𝜏2
                                ′    ′
Subproof. Then 𝜏 ′ = 𝜏1′ Σ1 &Σ2 𝜏2′ such that 𝜏1 <: 𝜏1′, Σ1 <: Σ1′ , Σ2′ <: Σ2′ , and 𝜏2 <: 𝜏2′ . But Σ(𝜏1 Σ1 &Σ2
𝜏2 ) = Σ(𝜏1 ) Σ·Σ1 &Σ·Σ2 Σ(𝜏2 ), then by induction hypotheses Σ(𝜏1 ) <: Σ(𝜏1′ ), and Σ(𝜏2 ) <: Σ(𝜏2′ ). Also
by Lemma C.12, Σ·Σ1 <: Σ·Σ1′ and Σ·Σ2 <: Σ·Σ2′ , therefore
                                                            ′      ′                     ′  ′
Σ(𝜏1 Σ1 &Σ2 𝜏2 ) = Σ(𝜏1 ) Σ·Σ1 &Σ·Σ2 Σ(𝜏2 ) <: Σ(𝜏1′ ) Σ·Σ1 &Σ·Σ2 Σ(𝜏2′ ) = Σ(𝜏1′ Σ1 &Σ2 𝜏2′ ) and the result
holds.                                                                                                             ⊳
                                                                                                                  
     Lemma C.7. Let Σ and Σ ′ Then
     (1) Σ <: Σ ⊔ Σ ′
     (2) Σ ⊓ Σ ′ <: Σ
     Proof. By induction of Σ, and noticing that 𝑠 ≤ 𝑠 ⊔ 𝑠 ′, and 𝑠 ⊓ 𝑠 ′ ≤ 𝑠.                                        
     Lemma C.8. Let Σ and Σ′ Then
     (1) Σ <: Σ ⊔ Σ′
     (2) Σ ⊓ Σ′ <: Σ
     Proof. By deﬁnition of the <: operator for privacy environments.                                                 
     Lemma C.9. Let 𝜏 and 𝜏 ′, such that 𝜏 ⊔ 𝜏 ′ and 𝜏 ⊓ 𝜏 ′ are deﬁned. Then
     (1) 𝜏 <: 𝜏 ⊔ 𝜏 ′
     (2) 𝜏 ⊓ 𝜏 ′ <: 𝜏

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                          75


  Proof. Let us prove (1) ﬁrst by induction by induction on 𝜏:
Case (1) 𝜏 = R
Subproof. Then 𝜏 ′ = R so the result is trivial.                                                                          ⊳
Case (2) 𝜏 = B
Subproof. Then 𝜏 ′ = B so the result is trivial.                                                                          ⊳
Case (3) 𝜏 = unit
Subproof. Then 𝜏 ′ = unit so the result is trivial.                                                                       ⊳
                           Σ
Case (4) 𝜏 = (𝑥 : 𝜏1 ·𝑑) →
                         − 𝜏2
                                               Σ′                                               Σ⊔Σ′
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑑 ′ ) −→ 𝜏2′ , and 𝜏 ⊔ 𝜏 ′ = (𝑥 : (𝜏1 ⊓ 𝜏1′ )·(𝑑 ⊓ 𝑑 ′)) −−−−→ (𝜏2 ⊔ 𝜏2′ )
By induction hypothesis (𝜏1 ⊓ 𝜏1′ ) <: 𝜏1 , we know that 𝑑 ⊓ 𝑑 ′ ≤ 𝑑, by Lemma C.7, Σ <: Σ ⊔ Σ ′, and
                                                                     Σ                                     Σ⊔Σ′
by induction hypothesis 𝜏2 <: 𝜏2 ⊔ 𝜏2′ . Then (𝑥 : 𝜏1 ·𝑑) →
                                                          − 𝜏2 <: (𝑥 : (𝜏1 ⊓ 𝜏1′ )·(𝑑 ⊓ 𝑑 ′)) −−−−→ (𝜏2 ⊔ 𝜏2′ )
and the result holds.                                                                                       ⊳
                           Σ′
Case (5) 𝜏 = (𝑥 : 𝜏1 ·𝑑) −−→
                           → 𝜏2
                                               Σ′                                               Σ⊔Σ′
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑑 ′ ) −−→
                                       → 𝜏2′ , and 𝜏 ⊔ 𝜏 ′ = (𝑥 : (𝜏1 ⊓ 𝜏1′ )·(𝑑 ⊓ 𝑑 ′ )) −−−−→
                                                                                              → (𝜏2 ⊔ 𝜏2′ )
By induction hypothesis (𝜏1 ⊓ 𝜏1 ) <: 𝜏1 , we know that 𝑑 ⊓ 𝑑 ≤ 𝑑, by Lemma C.8, Σ <: Σ ⊔ Σ′ , and
                                    ′                                ′
                                                                   Σ                                      Σ⊔Σ′
by induction hypothesis 𝜏2 <: 𝜏2 ⊔𝜏2′ . Then (𝑥 : 𝜏1 ·𝑑) −
                                                         →→ 𝜏2 <: (𝑥 : (𝜏1 ⊓𝜏1′ )·(𝑑 ⊓𝑑 ′ )) −−−−→
                                                                                                 → (𝜏2 ⊔𝜏2′ )
and the result holds.                                                                                     ⊳
Case (6) 𝜏 = 𝜏1 Σ1 ⊕ Σ2 𝜏2
                                    ′     ′                                        ′        ′
Subproof. Then 𝜏 ′ = 𝜏1′ Σ1 ⊕ Σ2 𝜏2′ , and 𝜏 ⊔ 𝜏 ′ = (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 ⊕ Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ ). By induction
hypotheses 𝜏1 <: 𝜏1 ⊔ 𝜏1′ , and 𝜏2 <: 𝜏2 ⊔ 𝜏2′ , and by Lemma C.7, Σ1 <: Σ1 ⊔ Σ1′ , and Σ2 <: Σ2 ⊔ Σ2′ .
          ′    ′                         ′        ′
Then 𝜏1′ Σ1 ⊕ Σ2 𝜏2′ <: (𝜏1 ⊔ 𝜏1′ ) Σ1 ⊔Σ1 ⊕ Σ2 ⊔Σ2 (𝜏2 ⊔ 𝜏2′ ) and the result holds.                    ⊳
Case (7) 𝜏 = 𝜏1 Σ1 &Σ2 𝜏2
Subproof. Analogous to the 𝜏 = 𝜏1 Σ1 ⊕ Σ2 𝜏2 case.                                                                        ⊳
Case (8) 𝜏 = 𝜏1   Σ1 ⊕ Σ2 𝜏
                    2
Subproof. Analogous to the 𝜏 = 𝜏1 Σ1 ⊕ Σ2 𝜏2 case.                                                                        ⊳
                                                                                                                         

  Lemma C.10 (Relation subsumption/weakening). Consider 𝑑 ≤ 𝑑 ′ and 𝜎 <: 𝜎 ′ then
  (1) If (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑘 J𝜎K, then (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑘′ J𝜎 ′ K
  (2) If (𝑒 1 , 𝑒 2 ) ∈ E𝑑𝑘 J𝜎K, then (𝑒 1, 𝑒 2 ) ∈ E𝑑𝑘′ J𝜎 ′ K
  (3) If (e1, e2 ) ∈ E𝑝𝑘 J𝜎K, then (e1, e2 ) ∈ E𝑝𝑘 ′ J𝜎 ′ K

  Proof. We only present intersting cases. We ﬁrst prove (1) by induction on 𝜏:
Case (1) 𝜎 = R
Subproof. Then 𝑣 1 = 𝑟 1 , 𝑣 2 = 𝑟 2 , 𝜎 ′ = R, and (𝑟 1, 𝑟 2 ) ∈ V𝑑𝑘 JRK, i.e. |𝑟 1 − 𝑟 2 | ≤ 𝑠. But if 𝑠 ≤ 𝑠 ′, then
it is easy to see that |𝑟 1 − 𝑟 2 | ≤ 𝑠 ′ , therefore (𝑟 1, 𝑟 2 ) ∈ V𝑑𝑘′ JRK and the result holds.                   ⊳
Case (2) 𝜎 = unit
Subproof. Trivial as 𝜎 ′ = unit and (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑘 JunitK does not depend on 𝑠, i.e. ∀𝑠 ′, (𝑣 1, 𝑣 2 ) ∈
V𝑑𝑘′ JunitK.                                                                                              ⊳
                               Δ1 ·Σ2 +𝑑 1 𝑥
Case (3) 𝜎 = (𝑥 : 𝜎1 ·𝑑 2 ) −−−−−−−−→ 𝜎2

                                   ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
76                  Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter

                                                              Δ1 ·Σ′2 +𝑑 1′ 𝑥
Subproof. Then 𝜎 ′ = (𝑥 : 𝜎1′ ·𝑑 2′ ) −−−−−−−−→ 𝜎2′ where 𝜎1′ <: 𝜎1, Σ2 <: Σ2′ , 𝑑 1 ≤ 𝑑 1′ , 𝑑 2′ < 𝑑 2 and
𝜎2 <: 𝜎2′ .
                s                            s                                  s           s                                                 Δ1 ·Σ2 +𝑑 1𝑥
Also 𝑣 1 = h𝜆 𝑥 .𝑒 1 , 𝛾 1 i, 𝑣 2 = h𝜆 𝑥 .𝑒 2 , 𝛾 2 i, and (h𝜆 𝑥 .𝑒 1 , 𝛾 1 i, h𝜆 𝑥 .𝑒 2 , 𝛾 2 i) ∈ V𝑑 J(𝑥 : 𝜎1 ·𝑑 2 ) −−−−−−−−→ 𝜎2 K.

                                        s                       s                                       Δ1 ·Σ′2 +𝑑 1′ 𝑥
We have to prove that (h𝜆 𝑥 .𝑒 1 , 𝛾 1 i, h𝜆 𝑥 .𝑒 2 , 𝛾 2 i) ∈ V𝑑𝑘′ J(𝑥 : 𝜎1′ ·𝑑 2′ ) −−−−−−−−→ 𝜎2′ K, i.e. for any 𝑗 < 𝑘,
(𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗3 J𝜎1′ K, 𝑑 3 ≤ 𝑑 2′ then (𝛾 1 [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1, 𝛾 2 [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2 ) ∈ E𝑑𝑗 ′+Δ1 ·Σ′ +𝑑 ′ 𝑑3 J𝑑 3𝑥(𝜎2′ )K.
                                                                                                                          2       1
We know that 𝑑 3 ≤ 𝑑 2′ ≤ 𝑑 2 , then by induction hypothesis on (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗3 J𝜎1′ K, we know that
(𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗3 J𝜎1 K. Then we instantiate the premise with 𝑑 ′′ = 𝑑 3 and 𝑣 1 and 𝑣 2 , so we know that
                                                   𝑗
(𝛾 1 [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1, 𝛾 2 [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2 ) ∈ E𝑑+Δ 1 ·Σ2 +𝑑 1𝑑 3
                                                                     J𝑑 3 𝑥(𝜎2 )K. By Lemma C.6, 𝑑 3𝑥(𝜎2 ) <: 𝑑 3𝑥(𝜎2′ ),
by Lemma C.12, Δ1 ·Σ2 ≤ Δ1 ·Σ2 , and as 𝑑 + Δ1 ·Σ2 + 𝑑 1𝑑 3 ≤ 𝑑 ′ + Δ1 ·Σ2′ + 𝑑 1′𝑑 3 , then by induction
                                        ′

hypothesis we know that (𝛾 1 [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1, 𝛾 2 [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2 ) ∈ E𝑑𝑗 ′+Σ′ ·Σ′ +𝑑 ′ 𝑑3 J𝑑 3𝑥(𝜎2′ )K and the
                                                                                          1 2  1
result holds.                                                                                                         ⊳
                                       Δ1 •Σ2
Case (4) 𝜎 = (𝑥 : 𝜎1 ·𝑑 2 ) −−−−→
                                → 𝜎2
                                                        Δ1 •Σ′2
Subproof. Then 𝜎 ′ = (𝑥 : 𝜎1′ ·𝑑 2′ ) −−−−→
                                          → 𝜎2′ where 𝜎1′ <: 𝜎1, Σ2 <: Σ2′ , 𝑑 2′ < 𝑑 2 and 𝜎2 <: 𝜎2′ .
                p                               p                                   p           p                                               Δ1 •Σ2
Also 𝑣 1 = h𝜆 𝑥 .e1 , 𝛾 1 i, 𝑣 2 = h𝜆 𝑥 .e2, 𝛾 2 i, and (h𝜆 𝑥 .e1, 𝛾 1 i, h𝜆 𝑥 .e2, 𝛾 2 i) ∈ V𝑑 J(𝑥 : 𝜎1 ·𝑑 2 ) −−−−→
                                                                                                                    → 𝜎2 K.

                                         p                          s                                      Δ1 •Σ′2
We have to prove that (h𝜆 𝑥 .e1, 𝛾 1 i, h𝜆 𝑥 .e2, 𝛾 2 i) ∈ V𝑑𝑘′ J(𝑥 : 𝜎1′ ·𝑑 2′ ) −−−−→        → 𝜎2′ K, i.e. for any 𝑗 < 𝑘,
                𝑗                                                                           𝑗
(𝑣 1, 𝑣 2 ) ∈ V𝑑3 J𝜎1′ K, 𝑑 3 ≤ 𝑑 2′ then (𝛾 1 [𝑥 ↦→ 𝑣 1 ] ⊢ e1, 𝛾 2 [𝑥 ↦→ 𝑣 2 ] ⊢ e2 ) ∈ E ⌉𝑑 ′ ⌈∞ +Δ1 Σ′ J𝑑 3𝑥(𝜎2′ )K.      •
                                                                                                                                      2
We know that 𝑑 3 ≤ 𝑑 2′ ≤ 𝑑 2 , then by induction hypothesis on (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗3 J𝜎1′ K, we know that
(𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗3 J𝜎1 K. Then we instantiate the premise with 𝑑 ′′ = 𝑑 3 and 𝑣 1 and 𝑣 2 , so we know that
                                                  𝑗
(𝛾 1 [𝑥 ↦→ 𝑣 1 ] ⊢ e1, 𝛾 2 [𝑥 ↦→ 𝑣 2 ] ⊢ e2 ) ∈ E ⌉𝑑 ⌈∞ +Δ1 •Σ2 J𝑑 3𝑥(𝜎2 )K. By Lemma C.6, 𝑑 3𝑥(𝜎2 ) <: 𝑑 3𝑥(𝜎2′ ), by
Lemma C.13, Δ1 •Σ2 ≤ Δ1 ·Σ2′ , then ⌉𝑑 ⌈∞ +Δ1 •Σ2 ≤ ⌉𝑑 ′ ⌈∞ +Δ1 •Σ2′ . The result follows from induction
hypothesis (3).                                                                                                                                              ⊳
Case (5) 𝜎 = 𝜎1       𝑠 1 ⊕𝑠 2 𝜎
                                   2
                                         ′       ′
Subproof. Then 𝜎 ′ = 𝜎1′ 𝑠1 ⊕𝑠2 𝜎2′ where 𝜎1 <: 𝜎1′, 𝑠 1 ≤ 𝑠 1′ , 𝑠 2 ≤ 𝑠 2′ , and 𝜎2 <: 𝜎2′ .
We proceed by case analysis on (𝑣 1, 𝑣 2 ):
Case (a) (𝑣 1, 𝑣 2 ) = (inl 𝑣 1′ , inl 𝑣 2′ )
Subproof. Then we know that (inl 𝑣 1′ , inl 𝑣 2′ ) ∈ V𝑑+𝑠   𝑘 J𝜎 K, then by induction hypothesis using
                                                              1
                                                                    1
𝑠 + 𝑠 1 ≤ 𝑠 + 𝑠 1 and 𝜎1 <: 𝜎2 , then (inl 𝑣 1 , inl 𝑣 2 ) ∈ V𝑠𝑘′ +𝑠 ′ J𝜎1′ K and therefore (inl 𝑣 1′ , inl 𝑣 2′ ) ∈
           ′       ′                          ′        ′
                                                                                                    1
           ′   ′
V𝑠𝑘′ J𝜎1′ 𝑠1 ⊕𝑠2 𝜎2′ K and the result holds.                                                                                                                 ⊳
Case (b) (𝑣 1, 𝑣 2 ) = (inr 𝑣 1′ , inr 𝑣 2′ )
Subproof. Analogous to previous case.                                                                                                                        ⊳
Case (c) (𝑣 1, 𝑣 2 ) = (inl 𝑣 1′ , inr 𝑣 2′ ) and (𝑣 1, 𝑣 2 ) = (inr 𝑣 1′ , inl 𝑣 2′ )
Subproof. Then 𝑠 = ∞ and as 𝑠 ≤ 𝑠 ′ , therefore 𝑠 ′ = ∞, and the result holds immediately.                                                                   ⊳
                                                                                                                                                             ⊳
Case (6) 𝜎 = 𝜎1 𝑠1 &𝑠2 𝜎2
                                         ′          ′
Subproof. Then 𝜎 ′ = 𝜎1′ 𝑠1 &𝑠2 𝜎2′ where 𝜎1 <: 𝜎1′, 𝑠 1 ≤ 𝑠 1′ , 𝑠 2 ≤ 𝑠 2′ , and 𝜎2 <: 𝜎2′ .
                                                                                        𝑘 J𝜎 K and (𝑣 , 𝑣 ) ∈ V 𝑘 J𝜎 K.
We know that (𝑣 1, 𝑣 2 ) = (h𝑣 11 , 𝑣 12 i, h𝑣 21 , 𝑣 22 i), such that (𝑣 11, 𝑣 21 ) ∈ V𝑑+𝑠 1
                                                                                              1       12 22    𝑑+𝑠2 2
                                                                       𝑘        ′                   𝑘     ′
By induction hypotheses we know that (𝑣 11, 𝑣 21 ) ∈ V𝑠 ′ +𝑠 ′ J𝜎1 K and (𝑣 12, 𝑣 22 ) ∈ V𝑠 ′ +𝑠 ′ J𝜎2 K, and there-
                                                                                        1                                                 2
                                                          ′         ′
fore (h𝑣 11, 𝑣 12 i, h𝑣 21 , 𝑣 22 i) ∈ V𝑠𝑘′ J𝜎1′ 𝑠1 &𝑠2 𝜎2′ K and the result holds.                                                                          ⊳

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                         77

                                                                                                      𝑘−𝑗
Now let us prove (2). We know that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑣 1 ∧ 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑣 2 then (𝑣 1, 𝑣 2 ) ∈ V𝑑 J𝜎K. We have
to prove that (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑘−𝑗
                               ′  J𝜎 ′ K, which follows from (1).
Now let us prove (3). We know that ∀𝑆 ⊆ 𝑣𝑎𝑙 ∗𝑘 , if Pr[𝛾 1 ⊢ e1 ⇓𝑘 𝑆] ∧ Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆], then Pr[𝛾 1 ⊢
e1 ⇓𝑘 𝑆] ≤ 𝑒 𝑝 .𝜖 Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆] + 𝑝.𝛿 and Pr[𝛾 1 ⊢ e2 ⇓𝑘 𝑆] ≤ 𝑒 𝑝.𝜖 Pr[𝛾 2 ⊢ e1 ⇓𝑘 𝑆] + 𝑝.𝛿. We have to
                                                                                     ′
prove that, if Pr[𝛾 1 ⊢ e1 ⇓𝑘 𝑆] ∧ Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆], then Pr[𝛾 1 ⊢ e1 ⇓𝑘 𝑆] ≤ 𝑒 𝑝 .𝜖 Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆] +𝑝 ′.𝛿
                              ′
and Pr[𝛾 1 ⊢ e2 ⇓𝑘 𝑆] ≤ 𝑒 𝑝 .𝜖 Pr[𝛾 2 ⊢ e1 ⇓𝑘 𝑆] + 𝑝 ′ .𝛿 .
                                                      ′                                    ′
   But notice that as 𝑝.𝜖 ≤ 𝑝 ′ .𝜖, then 𝑒 𝑝.𝜖 ≤ 𝑒 𝑝 .𝜖 , and 𝑒 𝑝.𝜖 Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆] ≤ 𝑒 𝑝 .𝜖 Pr[𝛾 2 ⊢ e2 ⇓𝑘 𝑆].
We also know that 𝑝.𝛿 ≤ 𝑝 ′ .𝛿, and the result follows.                                                        
   Lemma C.11. Consider 𝑘 ′ ≤ 𝑘 then
                                                            ′
   (1) If (𝑣 1, 𝑣 2 ) ∈ V𝑠𝑘 J𝜎K, then (𝑣 1, 𝑣 2 ) ∈ V𝑠𝑘 J𝜎K
                                                        ′
   (2) If (𝑒 1 , 𝑒 2 ) ∈ E𝑠𝑘 J𝜎K, then (𝑒 1, 𝑒 2 ) ∈ E𝑠𝑘 J𝜎K
                                                          ′
   (3) If (e1, e2 ) ∈ E𝑝𝑘 J𝜎K, then (e1, e2 ) ∈ E𝑝𝑘 J𝜎K
   Proof. By induction on 𝑘.                                                                                            
   Lemma C.12. Let 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Δ ′), then ∀Σ ′′, Σ <: Σ ′′ , then Δ ′ ·Σ ≤ Δ ′ ·Σ ′′.
    Proof. By induction on Σ.
Case (1) Σ = ∅
Subproof. Trivial as Σ ′′ = ∅, therefore 0 ≤ 0.                                                            ⊳
Case (2) Σ = Σ1 + 𝑑𝑥
Subproof. Let Σ ′′ = Σ1′ + 𝑑 ′𝑥 such that 𝑑 ≤ 𝑑 ′ , then we have to prove that Δ ′ ·Σ1 + 𝑑Δ ′(𝑥) ≤
Δ ′ ·Σ1′ + 𝑑 ′ Δ ′ (𝑥), but we know by induction hypothesis that Δ ′ ·Σ1 ≤ Δ ′ ·Σ1′ and 𝑑Δ ′(𝑥) ≤ 𝑑 ′ Δ ′(𝑥),
so the result holds immediately.                                                                           ⊳
Case (3) Σ = Σ1 + 𝑑
Subproof. Let Σ ′′ = Σ1′ + 𝑑 ′ such that 𝑑 ≤ 𝑑 ′, then we have to prove that Δ ′ ·Σ1 + 𝑑 ≤ Δ ′ ·Σ1′ + 𝑑 ′ ,
but we know by induction hypothesis that Δ ′ ·Σ1 ≤ Δ ′ ·Σ1′ , so the result holds immediately.             ⊳
                                                                                                           
   Lemma C.13. Let 𝑑𝑜𝑚(Σ) ⊆ 𝑑𝑜𝑚(Δ), then ∀Σ′, Σ <: Σ′ , then Δ•Σ ≤ Δ•Σ′.
   Proof. By deﬁnition of Σ <: Σ′ .                                                                                     
   Lemma C.14. .
   (1) If Γ ; Δ ⊢ 𝑒 1 : 𝜏 ; Σ and Γ ; Δ ⊢ 𝑒 2 : 𝜏 ; Σ, then (𝛾 1 ⊢ 𝑒 1𝛾 2 ⊢ 𝑒 2 ) ∈ E∞JΔ ′ (𝜏)K.
   (2) If Γ ; Δ ⊢ e1 : 𝜏 ; Σ and Γ ; Δ ⊢ e2 : 𝜏 ; Σ, then (𝛾 1 ⊢ e1𝛾 2 ⊢ e2 ) ∈ E∞ JΔ ′(𝜏)K.
   Proof. By induction on 𝜏.                                                                                            
    Lemma C.15. Let 𝑗 ≤ 𝑘, 𝛾 1 ⊢ e1 ⇓ 𝑗 𝛾 1′ ⊢ e1′ , 𝛾 2 ⊢ e2 ⇓∗ 𝛾 2′ ⊢ e2′ , and (𝛾 1′ ⊢ e1′ , 𝛾 2′ ⊢ e2′ ) ∈ E𝑝𝑘−𝑗 J𝜏K,
then
(𝛾 1 ⊢ e1, 𝛾 2 ⊢ e2 ) ∈ E𝑝𝑘 J𝜏K.
                                                                ′
   Proof. We know that for 𝑗 ′ < 𝑘 − 𝑗 if 𝛾 1′ ⊢ e1′ ⇓ 𝑗 𝐷 1 , then 𝛾 2′ ⊢ e2′ ⇓∗ 𝐷 2 , and both distributions
                                                                                ′                         ′
satisfy the dp inequality. Then as 𝛾 1 ⊢ e1 ⇓ 𝑗 𝛾 1′ ⊢ e1′ and 𝛾 1′ ⊢ e1′ ⇓ 𝑗 𝐷 1 , then 𝛾 1 ⊢ e1 ⇓ 𝑗+𝑗 𝐷 1
      ′                    ∗
(𝑗 + 𝑗 < 𝑘), and 𝛾 2 ⊢ e2 ⇓ 𝐷 1 , and the result is direct.                                                  

   Lemma C.16. If Γ; Δ ⊢ 𝑒 : 𝜏 ; Σ, 𝛾 1, 𝛾 ⊢ 𝑒 ⇓∗ 𝑣 1 , 𝛾 2, 𝛾 ⊢ 𝑒 ⇓∗ 𝑣 2 , and FV(𝑒) ⊆ 𝑑𝑜𝑚(𝛾), then 𝑣 1 = 𝑣 2 .
   Proof. By induction on Γ; Δ ⊢ 𝑒 : 𝜏 ; Σ.

                                  ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
78                   Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Case (1) Γ; Δ ⊢ 𝑟 : R ; ∅
Subproof. Trivial as numbers are already values.                                                                  ⊳
Case (2) Γ; Δ ⊢ 𝑒 1 + 𝑒 2 : R ; Σ1 + Σ2
Subproof. By induction hypotheses on Γ; Δ ⊢ 𝑒 1 : R ; Σ1 , and Γ; Δ ⊢ 𝑒 2 : R ; Σ2 . 𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 ,
𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 , and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 , 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 . The result holds as 𝑟 1 + 𝑟 2 = 𝑟 1 + 𝑟 2 . ⊳
Case (3) Γ; Δ ⊢ 𝑒 1 ∗ 𝑒 2 : R ; ∞(Σ1 + Σ2 )
Subproof. By induction hypotheses on Γ; Δ ⊢ 𝑒 1 : R ; Σ1 , and Γ; Δ ⊢ 𝑒 2 : R ; Σ2 . 𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 ,
𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 , and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 , 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 . The result holds as 𝑟 1 ∗ 𝑟 2 = 𝑟 1 ∗ 𝑟 2 . ⊳
Case (4) Γ; Δ ⊢ 𝑒 1 ≤ 𝑒 2 : B ; ∞(Σ1 + Σ2 )
Subproof. By induction hypotheses on Γ; Δ ⊢ 𝑒 1 : R ; Σ1 , and Γ; Δ ⊢ 𝑒 2 : R ; Σ2 . 𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 ,
𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑟 1 , and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 , 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑟 2 . The result holds as 𝑟 1 ≤ 𝑟 2 = 𝑟 1 ≤ 𝑟 2 . ⊳
Case (5) Γ; Δ ⊢ 𝑥 : 𝜏 ; 𝑥
Subproof. Given that FV(𝑒) = {𝑥 } ⊆ 𝑑𝑜𝑚(𝛾), then 𝑥 ∈ 𝑑𝑜𝑚(𝛾). Then 𝛾 1, 𝛾 ⊢ 𝑥 ⇓∗ 𝛾(𝑥) and
𝛾 2, 𝛾 ⊢ 𝑥 ⇓∗ 𝛾(𝑥), and the result holds as 𝛾(𝑥) = 𝛾(𝑥).                                                          ⊳
                      s                                   Σ′′ +𝑠 ′𝑥
Case (6) Γ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′ : (𝑥 : 𝜏1 ·𝑑 1 ) −−−−−→ 𝜏2 ; ∅
                                                                            s                   s
Subproof. We know that FV(𝑒) ⊆ 𝑑𝑜𝑚(𝛾), then 𝛾 1, 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′ ⇓1 h𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′, 𝛾 ′i and
          s                         s
𝛾 2, 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′ ⇓1 h𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′, 𝛾 ′i, for 𝛾 ′ ⊆ 𝛾 and the result holds.            ⊳
                          s                                     𝑠 ′𝑥
Case (7) Γ; Δ ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑑 1 ). 𝑒 ′, 𝛾i : (𝑥 : 𝜏1 ·𝑑 1 ) −−→ 𝜏2 ; ∅
Subproof. Trivial as closures are already values.                                                                                   ⊳
Case (8) Γ; Δ ⊢ 𝑒 1 𝑒 2 : [Σ2/𝑥]𝜏2 ; Σ1 + 𝑠Σ2 + Σ ′′
                                                                                   Σ′′ +𝑠𝑥
Subproof. By induction hypotheses on Γ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ) −−−−→ 𝜏2 ; Σ1 and Γ ⊢ 𝑒 2 : 𝜏1 ; Σ2 .
                    s                                             s
𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 ′ i, 𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 ′ i, and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣, 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣.
The result holds as 𝛾 [𝑥 ↦→ 𝑣] ⊢ 𝑒 ⇓ 𝑣 1 and 𝛾 [𝑥 ↦→ 𝑣] ⊢ 𝑒 ′ ⇓∗ 𝑣 2 , therefore 𝑣 1 = 𝑣 2 .
                             ′                  ′    ∗          ′                                                                    ⊳
Case (9) Γ; Δ ⊢ tt : unit ; ∅
Subproof. Trivial.                                                                                                                   ⊳
                            𝜏2 ′         Σ ′′ ∅
Case (10) Γ; Δ ⊢ inl 𝑒 : 𝜏1 ⊕ 𝜏2 ; ∅
Subproof. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 ; Σ ′′ . 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣, 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣, and the result
holds as inl𝜏2 𝑣 = inl𝜏2 𝑣.                                                                                                          ⊳
                                                ′′
Case (11) Γ; Δ ⊢ inr𝜏1 𝑒 ′ : 𝜏1 ∅ ⊕ Σ 𝜏2 ; ∅
Subproof. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 ; Σ ′′ . 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣, 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣, and the result
holds as inr𝜏2 𝑣 = inr𝜏2 𝑣.                                                                                                          ⊳
Case (12) Γ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } : [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ; Σ1 ⊔ ([Σ1 +
Σ11/𝑥](Σ2 + 𝑠 2𝑥) ⊔ [Σ1 + Σ12/𝑦](Σ3 + 𝑠 3𝑦))
Subproof. By induction hypothesis on Γ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1 , we know that
𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 , 𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 . Suppose 𝑣 1 = inl 𝑣 1′ (the other case is analogous). Then by
induction hypothesis on Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 2𝑥, we know that, 𝛾 1, 𝛾[𝑥 ↦→
𝑣 1′ ] ⊢ 𝑒 2 ⇓∗ 𝑣, 𝛾 2, 𝛾[𝑥 ↦→ 𝑣 1′ ] ⊢ 𝑒 2 ⇓∗ 𝑣, and the result holds,                                                              ⊳
Case (13) Γ; Δ ⊢ (𝑒 1, 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; ∅
Subproof. By induction hypotheses on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 , 𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 ,
𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 , and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣 2 , 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣 2 . The result holds as (𝑣 1, 𝑣 2 ) = (𝑣 1, 𝑣 2 ). ⊳
                              ′         ′′
Case (14) Γ; Δ ⊢ fst 𝑒 : 𝜏1 ; Σ + Σ1

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                  79


Subproof. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ ′′ , 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ (𝑣 1, 𝑣 2 ), 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗
(𝑣 1, 𝑣 2 ). The result holds as 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣 1 and 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣 1 .                                         ⊳
                                ′
Case (15) Γ; Δ ⊢ snd 𝑒 : 𝜏1 ; Σ + Σ2       ′′

Subproof. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ ′′ , 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ (𝑣 1, 𝑣 2 ), 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗
(𝑣 1, 𝑣 2 ). The result holds as 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣 2 and 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣 2 .                                         ⊳
                                       Σ
Case (16) Γ; Δ ⊢ h𝑒 1 , 𝑒 2 i : 𝜏1 ⊗ 𝜏2 ; ∅
                                         1    Σ 2


Subproof. By induction hypotheses on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 , 𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 ,
𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ 𝑣 1 , and 𝛾 1, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣 2 , 𝛾 2, 𝛾 ⊢ 𝑒 2 ⇓∗ 𝑣 2 . The result holds as h𝑣 1 , 𝑣 2 i = h𝑣 1 , 𝑣 2 i. ⊳
Case (17) Γ; Δ ⊢ let 𝑥 1 , 𝑥 2 = 𝑒 1 in 𝑒 2 : [Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ; 𝑠 1 (Σ11 + Σ1 ) +𝑠 2 (Σ12 + Σ1 ) + Σ2
Subproof. By induction hypothesis on Γ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊗ Σ12 𝜏12 ; Σ1 , we know that
𝛾 1, 𝛾 ⊢ 𝑒 1 ⇓∗ h𝑣 1 , 𝑣 2 i, 𝛾 2, 𝛾 ⊢ 𝑒 1 ⇓∗ h𝑣 1 , 𝑣 2 i. Then by induction hypothesis on Γ, 𝑥 : 𝜏11, 𝑥 : 𝜏12 ; Δ +
(Δ·(Σ1 + Σ11 ))𝑥 1 + (Δ·(Σ1 + Σ12 ))𝑥 2 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 1𝑥 1 + 𝑠 2𝑥 2 , we know that, 𝛾 1, 𝛾[𝑥 1 ↦→ 𝑣 1 , 𝑥 2 ↦→
𝑣 2 ] ⊢ 𝑒 2 ⇓∗ 𝑣, 𝛾 2, 𝛾[𝑥 1 ↦→ 𝑣 1, 𝑥 2 ↦→ 𝑣 2 ] ⊢ 𝑒 2 ⇓∗ 𝑣, and the result holds,                                    ⊳
                          ′
Case (18) Γ; Δ ⊢ (𝑒 :: 𝜏) : 𝜏 ; Σ
Subproof. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏 ′ ; Σ, 𝛾 1, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣, 𝛾 2, 𝛾 ⊢ 𝑒 ′ ⇓∗ 𝑣. The result
holds as 𝛾 1, 𝛾 ⊢ (𝑒 ′ :: 𝜏) ⇓∗ 𝑣 and 𝛾 2, 𝛾 ⊢ (𝑒 ′ :: 𝜏) ⇓∗ 𝑣 1 .                                                     ⊳
                       p                                   Σ′′
Case (19) Γ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′ : (𝑥 : 𝜏1 ·𝑑 ′ ) −−→   → 𝜏2 ; ∅
                                                                               s                   s
Subproof. We know that FV(𝑒) ⊆ 𝑑𝑜𝑚(𝛾), therefore 𝛾 1, 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 ′ ). e′ ⇓1 h𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′, 𝛾 ′ i
              s                        s
and 𝛾 2, 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). e′ ⇓1 h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). e′, 𝛾 ′i, for 𝛾 ′ ⊆ 𝛾 and the result holds.        ⊳
                                                                                                          

   Theorem C.17 (Metric Preservation).
   (1) Γ, Δ ⊢ 𝑒 : 𝜏 ; Σ ⇒ ∀𝑘 ≥ 0, ∀Δ ′ ⊑ Δ, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK.(𝛾 1 ⊢ 𝑒, 𝛾 2 ⊢ 𝑒) ∈ E 𝑘Δ′ ·Σ JΔ ′(𝜏)K
   (2) Γ, Δ ⊢ e : 𝜏 ; Σ ⇒ ∀𝑘 ≥ 0, ∀Δ ′ ⊑ Δ, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK.(𝛾 1 ⊢ e, 𝛾 2 ⊢ e) ∈ E Δ𝑘 ′ Σ JΔ ′(𝜏)K
                                                                                                          •



   Proof. We prove the two parts using induction on 𝑘 ﬁrst.
We start by proving Part (1) by induction on 𝑘 and the typing derivation.
Case (1) Γ; Δ ⊢ 𝑟 : R ; ∅
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑟, 𝛾 2 ⊢ 𝑟 ) ∈ E Δ′ ·∅ JΔ ′ (R)K, for Δ ′ ⊑ Δ.
Notice that Δ ′ ·∅ = 0 and 𝛾 1 (𝑟 ) = 𝛾 2 (𝑟 ) = 𝑟 . Then we have to prove that (𝑟, 𝑟 ) ∈ V0𝑘 JRK, i.e. |𝑟 −𝑟 | ≤ 0
which is direct.                                                                                                           ⊳
Case (2) Γ; Δ ⊢ 𝑒 1 + 𝑒 2 : R ; Σ1 + Σ2
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑒 1 +𝑒 2 , 𝛾 2 ⊢ 𝑒 1 +𝑒 2 ) ∈ E 𝑘Δ′ ·(Σ1 +Σ2 ) JΔ ′(R)K,
for Δ ′ ⊑ Δ. By induction hypotheses
Γ; Δ ⊢ 𝑒 1 : R ; Σ1 ⇒ (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E Δ𝑘 ′ ·Σ1 JΔ ′(R)K and Γ; Δ ⊢ 𝑒 2 : R ; Σ2 ⇒ (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢
         𝑘−𝑗
𝑒 2 ) ∈ E Δ′ ·Σ12 JΔ ′ (R)K for some 𝑗 1 ≤ 𝑘. By unfolding (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (R)K, we know that
if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑟 11 then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑟 12 and (𝑟 11, 𝑟 12 ) ∈ VΔ𝑘−𝑗                                ′
                                                                     ′ ·Σ JRK, where |𝑟 11 − 𝑟 12 | ≤ Δ ·Σ 1 .
                                                                         1
                                                                         1

Also, by unfolding (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E 𝑘−𝑗      ′
                                                Δ′ ·Σ2 JΔ (R)K, if 𝛾 1 ⊢ 𝑒 2 ⇓
                                                     1                         𝑗2 𝑟                    ∗
                                                                                    21 then 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑟 22
                       𝑘−𝑗 −𝑗
and (𝑟 21, 𝑟 22 ) ∈ VΔ′ ·Σ12 2 JRK, where |𝑟 21 − 𝑟 22 | ≤ Δ ′ ·Σ2 .
Then if 𝛾 1 ⊢ 𝑒 1 + 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑟 1′ and 𝛾 2 ⊢ 𝑒 1 + 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑟 2′ , where 𝑟 1′ = 𝑟 11 + 𝑟 21 and 𝑟 2′ = 𝑟 12 + 𝑟 22 , we
                                         𝑘−𝑗 −𝑗 −1
have to prove that (𝑟 1′, 𝑟 2′ ) ∈ VΔ′ ·(Σ11 +Σ2 2 ) JRK, i.e. |(𝑟 11 + 𝑟 21 ) − (𝑟 12 + 𝑟 22 )| ≤ Δ ′ ·(Σ1 + Σ2 ).
Notice that |(𝑟 11 + 𝑟 21 ) − (𝑟 12 + 𝑟 22 )| = |(𝑟 11 − 𝑟 12 ) + (𝑟 21 − 𝑟 22 )|, and by the triangle inequality of the
absolute value, |(𝑟 11 − 𝑟 12 ) + (𝑟 21 − 𝑟 22 )| ≤ |(𝑟 11 − 𝑟 12 )| + |(𝑟 21 − 𝑟 22 )|. Also as |𝑟 11 − 𝑟 12 | ≤ Δ ′ ·Σ1 and

                                    ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
80                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


|𝑟 21 − 𝑟 22 | ≤ Δ ′ ·Σ2 , then |(𝑟 11 − 𝑟 12 )| + |(𝑟 21 − 𝑟 22 )| ≤ Δ ′ ·Σ1 + Δ ′ ·Σ2 . By Lemma C.1, Δ ′ ·Σ1 + Δ ′ ·Σ2 =
Δ ′ ·(Σ1 + Σ2 ), therefore |(𝑟 11 + 𝑟 21 ) − (𝑟 12 + 𝑟 22 )| ≤ Δ ′ ·(Σ1 + Σ2 ) and the result holds.                      ⊳
Case (3) Γ; Δ ⊢ 𝑒 1 ∗ 𝑒 2 : R ; ∞(Σ1 + Σ2 )
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑒 1 ∗𝑒 2 , 𝛾 2 ⊢ 𝑒 1 ∗𝑒 2 ) ∈ E 𝑘Δ′ ·∞(Σ1 +Σ2 ) JΔ ′(R)K,
for Δ ′ ⊑ Δ. By induction hypotheses
Γ ⊢ 𝑒 1 : R ; Σ1 ⇒ (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′(R)K and Γ ⊢ 𝑒 2 : R ; Σ2 ⇒ (𝛾 1 ⊢ 𝑒 2, 𝛾 2 ⊢
𝑒 2 ) ∈ E Δ𝑘−𝑗     ′                                                            𝑘       ′
            ′ ·Σ JΔ (R)K for 𝑗 1 ≤ 𝑘. By unfolding (𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈ E Δ′ ·Σ JΔ (R)K, we know that if
                1
                 2                                                                   1

𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑟 11 then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑟 12 and (𝑟 11, 𝑟 12 ) ∈ VΔ𝑘−𝑗                                ′
                                                                  ′ ·Σ JRK, where |𝑟 11 − 𝑟 12 | ≤ Δ ·Σ 1 .
                                                                      1

Also, by unfolding (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E 𝑘−𝑗      ′
                                                Δ′ ·Σ2 JΔ (R)K, if 𝛾 1 ⊢ 𝑒 2 ⇓
                                                     1                         𝑗2 𝑟                    ∗
                                                                                    21 then 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑟 22
                           1 −𝑗 2
and (𝑟 21, 𝑟 22 ) ∈ VΔ𝑘−𝑗
                       ′ ·Σ
                            2
                                   JRK, where |𝑟 21 − 𝑟 22 | ≤ Δ ′ ·Σ2 .
Then if 𝛾 1 ⊢ 𝑒 1 ∗ 𝑒 2 ⇓ 2 +1 𝑟 1′ and 𝛾 2 ⊢ 𝑒 1 ∗ 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑟 2′ , where 𝑟 1′ = 𝑟 11 ∗ 𝑟 21 and 𝑟 2′ = 𝑟 12 ∗ 𝑟 22 , we
                             𝑗 1 +𝑗
                                                1 −𝑗 2 −1
have to prove that (𝑟 1′, 𝑟 2′ ) ∈ VVΔ𝑘−𝑗                                                             ′
                                            ′ ·∞(Σ +Σ ) JRK, i.e. |(𝑟 11 ·𝑟 21 ) − (𝑟 12 ∗ 𝑟 22 )| ≤ Δ ·∞(Σ 1 + Σ 2 ).
                                                   1     2
                   ′                         ′
Notice that Δ ·∞(Σ1 + Σ2 ) = ∞(Δ ·(Σ1 + Σ2 )) = 𝑠. There are two cases to analyze, where if 𝑠 = ∞
then the result holds immediately. Let us suppose that 𝑠 = 0. Then by Lemma C.1, Δ ′ ·(Σ1 + Σ2 ) =
Δ ′ ·Σ1 + Δ ′ ·Σ1 , also notice that |𝑟 11 − 𝑟 12 | ≤ Δ ′ ·Σ1 and |𝑟 21 − 𝑟 22 | ≤ Δ ′ ·Σ2 , then 0 ≤ Δ ′ ·Σ1 and
0 ≤ Δ ′ ·Σ2 . Therefore if Δ ′ ·Σ1 + Δ ′ ·Σ1 = 0, then Δ ′ ·Σ1 = 0 and Δ ′ ·Σ2 = 0. This means that 𝑟 11 = 𝑟 12
and 𝑟 21 = 𝑟 22 , thus 𝑟 11 ∗ 𝑟 21 = 𝑟 12 ∗ 𝑟 22 , |(𝑟 11 ∗ 𝑟 21 ) − (𝑟 12 ∗ 𝑟 22 )| = 0, and the result holds.               ⊳
Case (4) Γ; Δ ⊢ 𝑒 1 ≤ 𝑒 2 : B ; ∞(Σ1 + Σ2 )
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑒 1 ≤ 𝑒 2 , 𝛾 2 ⊢ 𝑒 1 ≤ 𝑒 2 ) ∈ E 𝑘Δ′ ·∞(Σ1 +Σ2 ) JΔ ′ (B)K,
for Δ ′ ⊑ Δ. By induction hypotheses
Γ ⊢ 𝑒 1 : R ; Σ1 ⇒ (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (B)K and Γ ⊢ 𝑒 2 : R ; Σ2 ⇒ (𝛾 1 ⊢ 𝑒 2, 𝛾 2 ⊢ 𝑒 2 ) ∈
  𝑘−𝑗
E Δ′ ·Σ12 JΔ ′ (B)K, for some 𝑗 1 ≤ 𝑘. By unfolding (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (B)K, we know that if
𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑟 11 then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑟 12 and (𝑟 11, 𝑟 12 ) ∈ VΔ𝑘−𝑗                                ′
                                                                  ′ ·Σ JRK, where |𝑟 11 − 𝑟 12 | ≤ Δ ·Σ 1 .
                                                                      1
                                                                      1

Also, by unfolding (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ VΔ𝑘−𝑗     ′
                                                 ′ ·Σ JΔ (B)K, if 𝛾 1 ⊢ 𝑒 2 ⇓
                                                     1
                                                     2
                                                                              𝑗2 𝑟                    ∗
                                                                                   21 then 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑟 22
                           1 −𝑗 2
and (𝑟 21, 𝑟 22 ) ∈ VΔ𝑘−𝑗
                       ′ ·Σ
                            2
                                  JRK, where |𝑟 21 − 𝑟 22 | ≤ Δ ′ ·Σ2 .
Then if 𝛾 1 ⊢ 𝑒 1 ≤ 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑏 1 and 𝛾 2 ⊢ 𝑒 1 ≤ 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑏 2 , where 𝑏𝑖 ∈ {inl tt, inr tt}, we have
                                        1 −𝑗 2 −1
to prove that (𝑏 1, 𝑏 2 ) ∈ VΔ𝑘−𝑗   ′ ·∞(Σ +Σ ) JBK.
                                           1     2
Notice that Δ ·∞(Σ1 + Σ2 ) = ∞(Δ ′ ·(Σ1 + Σ2 )) = 𝑠. There are two cases to analyze, if 𝑠 = ∞ or
                   ′

𝑠 = 0. If 𝑠 = ∞ and 𝑏 1 ≠ 𝑏 2 then the result holds immediately. If 𝑠 = ∞ and 𝑏 1 = 𝑏 2 , let us
suppose 𝑏 1 = inl tt (the other case is analogous), then we have to prove that (inl tt, inl tt) ∈
   𝑘−𝑗 −𝑗 −1                                                      𝑘−𝑗 −𝑗 −1
V∞ 1 2 JunitK, but this is direct as (tt, tt) ∈ V∞ 1 2 JunitK. Let us suppose that 𝑠 = 0. Then
by Lemma C.1, Δ ′ ·(Σ1 +Σ2 ) = Δ ′ ·Σ1 +Δ ′ ·Σ1 , also notice that |𝑟 11 −𝑟 12 | ≤ Δ ′ ·Σ1 and |𝑟 21 −𝑟 22 | ≤ Δ ′ ·Σ2 ,
then 0 ≤ Δ ′ ·Σ1 and 0 ≤ Δ ′ ·Σ2 . Therefore if Δ ′ ·Σ1 + Δ ′ ·Σ1 = 0, then Δ ′ ·Σ1 = 0 and Δ ′ ·Σ2 =
0. This means that 𝑟 11 = 𝑟 12 and 𝑟 21 = 𝑟 22 , thus 𝑟 11 ≤ 𝑟 21 = 𝑟 12 ≤ 𝑟 22 . Then 𝑏 1 = 𝑏 2 , let us
suppose 𝑏 1 = inl tt (the other case is analogous), then we have to prove that (inl tt, inl tt) ∈
V0𝑘−𝑗1 −𝑗2 −1 JunitK, but this is direct as (tt, tt) ∈ V0𝑘−𝑗1 −𝑗2 −1 JunitK.                                         ⊳
Case (5) Γ; Δ ⊢ 𝑥 : 𝜏 ; 𝑥
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑥, 𝛾 2 ⊢ 𝑥) ∈ E 𝑘Δ′ ·𝑥 JΔ ′ (𝜏)K, where
𝜏 = Γ(𝑥), for Δ ′ ⊑ Δ. Notice that Δ ′ ·𝑥 = Δ ′ ·1𝑥 = Δ ′(𝑥), therefore we have to prove that (𝛾 1 ⊢ 𝑥,𝛾 2 ⊢
𝑥) ∈ VΔ𝑘−𝑗       ′                       1                       1
         ′ (𝑥) JΔ (Γ(𝑥))K. But 𝛾 1 ⊢ 𝑥 ⇓ 𝛾 1 (𝑥) and 𝛾 2 ⊢ 𝑥 ⇓ 𝛾 2 (𝑥) therefore we have to prove that
                               ′
(𝛾 1 (𝑥),𝛾 2 (𝑥)) ∈ VΔ𝑘−1                                                                       𝑘
                       ′ (𝑥) JΔ (Γ(𝑥))K. The result is direct as by deﬁnition of (𝛾 1, 𝛾 2 ) ∈ GΔ′ JΓK, we know
                                             𝑘−1   ′
by weakening that (𝛾 1 (𝑥),𝛾 2 (𝑥)) ∈ VΔ′(𝑥) JΔ (Γ(𝑥))K.                                                      ⊳

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                           81


                       s                                     Σ′′ +𝑠 ′ 𝑥
Case (6) Γ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′ : (𝑥 : 𝜏1 ·𝑠 1 ) −−−−−→ 𝜏2 ; ∅

Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK,
         s                           s                                               Δ′ ·Σ′′ +𝑠 ′𝑥
(𝛾 1 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 2 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′ ) ∈ E 𝑘Δ′ ·∅ JΔ ′ (𝜏1 ·𝑠 1 ) −−−−−−−→ Δ ′(𝜏2 )K, for Δ ′ ⊑ Δ..
                                                        Σ′′ +𝑠 ′𝑥                                 Δ′ ·Σ′′ +𝑠 ′ 𝑥
Notice that Δ ′ ·∅ = 0, that Δ ′((𝑥 : 𝜏1 ·𝑠 1 ) −−−−−→ 𝜏2 ) = (𝑥 : Δ ′(𝜏1 )·𝑠 1 ) −−−−−−−→ Δ ′ (𝜏2 ) (as 𝑥 ∉ 𝑑𝑜𝑚(Δ ′)),
and that lambdas reduce to closures, therefore we have to prove that
   s                            s                                                              Δ′ ·Σ′′ +𝑠 ′𝑥
(h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 1 i, h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 2 i) ∈ V0𝑘−1 J(𝑥 : Δ ′(𝜏1 )·𝑠 1 ) −−−−−−−→ Δ ′(𝜏2 )K.
Note that as Γ, 𝑥 : 𝜏1 ; Δ+𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ +𝑠 ′𝑥 and (𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, then 𝑑𝑜𝑚(Σ ′′) ⊆ 𝑑𝑜𝑚(Δ ′), there-
fore Δ ′ ·Σ ′′ ∈ sens (the result is a scalar). Consider 𝑠 ′′ ≤ 𝑠 1, 𝑣 1 and 𝑣 2 such that (𝑣 1, 𝑣 2 ) ∈ V𝑠𝑗′′ JΔ ′ (𝜏1 )K
                                                                                                              𝑗−1
for some 𝑗 < 𝑘. We have to prove that (𝛾 1, 𝑥 ↦→ 𝑣 1 ⊢ 𝑒 ′, 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ 𝑒 ′ ) ∈ E Δ′ ·Σ′′ +𝑠 ′𝑠 ′′ J𝑠 ′′𝑥(Δ ′(𝜏2 ))K.
Notice that by Lemma C.2 𝑠 ′′𝑥(Δ ′(𝜏2 )) = (Δ ′ + 𝑠 ′′𝑥)(𝜏2 ), therefore we have to prove that (𝛾 1, 𝑥 ↦→
                                              𝑗−1
𝑣 1 ⊢ 𝑒 ′, 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ 𝑒 ′ ) ∈ E Δ′ ·Σ′′+𝑠 ′𝑠 ′′ J(Δ ′ + 𝑠 ′′𝑥)(𝜏2 )K.
By induction hypothesis on Γ, 𝑥 : 𝜏1 ; Δ + 𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + 𝑠 ′𝑥, and choosing Σ 𝜒 = Δ ′ + 𝑠 ′′𝑥, we
                                                  𝑗−1                                           𝑗−1
know that ∀𝛾 1′ , 𝛾 2′, (𝛾 1′, 𝛾 2′ ) ∈ GΣ 𝜒 JΓ, 𝑥 : 𝜏1 K then (𝛾 1′ ⊢ 𝑒 ′, 𝛾 2′ ⊢ 𝑒 ′ ) ∈ E Σ 𝜒 ·(Σ′′ +𝑠 ′𝑥) JΣ 𝜒 (𝜏2 )K. Notice that
   𝜒       ′′     ′           ′     ′′           ′′   ′        ′   ′′  ′
Σ ·(Σ + 𝑠 𝑥) = (Δ + 𝑠 𝑥)·(Σ + 𝑠 𝑥) = Δ ·Σ + 𝑠 𝑠 . Therefore we know that ′′

(𝛾 1′ ⊢ 𝑒 ′, 𝛾 2′ ⊢ 𝑒 ′ ) ∈ E Δ𝑗−1                  ′   ′′
                                ′ ·Σ′′ +𝑠 ′𝑠 ′′ J(Δ + 𝑠 𝑥)(𝜏 2 )K.

As (𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, and by Lemma C.10 (𝛾 1, 𝛾 2 ) ∈ GΔ𝑗−1                                                    𝑗−1    ′
                                                                                 ′ JΓK, also (𝑣 1 , 𝑣 2 ) ∈ V𝑠 ′′ JΔ (𝜏 1 )K, and
   ′                ′        ′′
Δ (𝜏1 ) = (Δ + 𝑠𝑥 )(𝜏1 ) (as 𝑥 is not free in 𝜏1 ), it is easy to see that (𝛾 1, 𝑥 ↦→ 𝑣 1 , 𝛾 2, 𝑥 ↦→ 𝑣 2 ) ∈
GΔ𝑗−1                                                                             ′                             ′
     ′ +𝑠 ′′𝑥 JΓ, 𝑥 : 𝜏 1 K. Finally, the result follows by choosing 𝛾 1 = 𝛾 1 , 𝑥 ↦→ 𝑣 1 , and 𝛾 2 = 𝛾 2 , 𝑥 ↦→ 𝑣 2 .                ⊳

                       s                                     Σ′′ +𝑠 ′ 𝑥
Case (7) Γ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′ : (𝑥 : 𝜏1 ·𝑠 1 ) −−−−−→ 𝜏2 ; Σ ′

Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK,
         s                           s                                                Δ′ ·Σ′′ +𝑠 ′𝑥
(𝛾 1 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 2 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′ JΔ ′ (𝜏1 ·𝑠 1 ) −−−−−−−→ Δ ′(𝜏2 )K, for Δ ′ ⊑ Δ..
                                         Σ′′ +𝑠 ′𝑥                             Δ′ ·Σ′′ +𝑠 ′𝑥
Notice that Δ ′((𝑥 : 𝜏1 ·𝑠 1 ) −−−−−→ 𝜏2 ) = (𝑥 : Δ ′(𝜏1 )·𝑠 1 ) −−−−−−−→ Δ ′(𝜏2 ) (as 𝑥 ∉ 𝑑𝑜𝑚(Δ ′)), and that
lambdas reduce to closures, therefore we have to prove that
   s                            s                                                               Δ′ ·Σ′′ +𝑠 ′𝑥
(h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 1 i, h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾 2 i) ∈ VΔ𝑘−1                     ′
                                                                            ′ ·Σ′ J(𝑥 : Δ (𝜏 1 )·𝑠 1 ) −−−−−−−→ Δ ′(𝜏2 )K.
Note that as Γ, 𝑥 : 𝜏1 ; Δ + 𝑠 1𝑥 ⊢ 𝑒 : 𝜏2 ; Σ + Σ + 𝑠 𝑥 and (𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, then 𝑑𝑜𝑚(Σ ′′) ⊆
                                                                ′        ′′       ′     ′

𝑑𝑜𝑚(Δ ′), therefore Δ ′ ·Σ ′′ ∈ sens (the result is a scalar). Consider 𝑠 ′′ ≤ 𝑠 1 , 𝑣 1 and 𝑣 2 such that
(𝑣 1, 𝑣 2 ) ∈ V𝑠𝑗′′ JΔ ′ (𝜏1 )K for some 𝑗 < 𝑘. We have to prove that (𝛾 1, 𝑥 ↦→ 𝑣 1 ⊢ 𝑒 ′, 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ 𝑒 ′ ) ∈
E Δ𝑗−1                          ′′      ′                                                    ′′     ′            ′
     ′ ·Σ′′ +Δ′ ·Σ′ +𝑠 ′𝑠 ′′ J𝑠 𝑥(Δ (𝜏 2 ))K. Notice that by Lemma C.2 𝑠 𝑥(Δ (𝜏 2 )) = (Δ + 𝑠 𝑥)(𝜏 2 ), therefore we
                                                                                                                       ′′
                                                              ′                 ′        𝑗−1                   ′     ′′
have to prove that (𝛾 1, 𝑥 ↦→ 𝑣 1 ⊢ 𝑒 , 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ 𝑒 ) ∈ E Δ′ ·Σ′′ +Δ′ ·Σ′ +𝑠 ′𝑠 ′′ J(Δ + 𝑠 𝑥)(𝜏2 )K.
By induction hypothesis on Γ, 𝑥 : 𝜏1 ; Δ + 𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + Σ ′ + 𝑠 ′𝑥, and choosing Σ 𝜒 = Δ ′ + 𝑠 ′′𝑥, we
know that ∀𝛾 1′, 𝛾 2′, (𝛾 1′, 𝛾 2′ ) ∈ GΣ𝑗−1                                        ′     ′ ′         ′      𝑗−1               𝜒
                                                        𝜒 JΓ, 𝑥 : 𝜏 1 K then (𝛾 1 ⊢ 𝑒 , 𝛾 2 ⊢ 𝑒 ) ∈ E Σ 𝜒 ·(Σ′′ +Σ′ +𝑠 ′𝑥) JΣ (𝜏 2 )K. Notice

that Σ 𝜒 ·(Σ ′′ + Σ ′ + 𝑠 ′𝑥) = (Δ ′ + 𝑠 ′′𝑥)·(Σ ′′ + Σ ′ + 𝑠 ′𝑥) = Δ ′ ·Σ ′′ + Δ ′ ·Σ ′ + 𝑠 ′𝑠 ′′ . Therefore we know that
(𝛾 1′ ⊢ 𝑒 ′, 𝛾 2′ ⊢ 𝑒 ′ ) ∈ E Δ𝑗−1                                ′ ′′
                                     ′ ·Σ′′ +Δ′ ·Σ′ +𝑠 ′𝑠 ′′ J(Δ + 𝑠 𝑥)(𝜏 2 )K.

As (𝛾 1, 𝛾 2 ) ∈ GΔ′ JΓK, and by Lemma C.10 (𝛾 1, 𝛾 2 ) ∈ GΔ𝑗−1
                              𝑘                                                                                             𝑗−1  ′
                                                                                             ′ JΓK, also (𝑣 1 , 𝑣 2 ) ∈ V𝑠 ′′ JΔ (𝜏 1 )K, and
   ′                 ′            ′′
Δ (𝜏1 ) = (Δ + 𝑠𝑥 )(𝜏1 ) (as 𝑥 is not free in 𝜏1 ), it is easy to see that (𝛾 1, 𝑥 ↦→ 𝑣 1 , 𝛾 2, 𝑥 ↦→ 𝑣 2 ) ∈
GΔ𝑗−1                                                                                         ′
     ′ +𝑠 ′′𝑥 JΓ, 𝑥 : 𝜏 1 K. Finally, the result follows by choosing 𝛾 1 = 𝛾 1 , 𝑥 ↦→ 𝑣 1 , and 𝛾 2 = 𝛾 2 , 𝑥 ↦→ 𝑣 2 .
                                                                                                                          ′                 ⊳

                           s                                        𝑠 ′𝑥
Case (8) Γ; Δ ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i : (𝑥 : 𝜏1 ·𝑠 1 ) −−→ 𝜏2 ; ∅



                                         ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
82                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Subproof.
                                ∃Γ ′, Δ0′ , 𝑑𝑜𝑚(Σ ′′) ⊆ 𝑑𝑜𝑚(Γ ′) ⊆ 𝑑𝑜𝑚(Δ0′ )
         ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ ′(𝑥𝑖 ); ∅
                             ′
                                                                Γ ′, 𝑥 : 𝜏1 ; Δ0′ + 𝑠 1 𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + 𝑠 ′𝑥
                             s                                                                       𝑠 ′𝑥
              Γ; Δ ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i : (𝑥 : [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏1 ·𝑠 1 ) −−→ [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏2 ; ∅
By induction hypotheses on ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ′), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′ ; ∅, we know that, h𝛾(𝑥𝑖 ), 𝛾(𝑥𝑖 )i ∈
V0𝑘−1 J∅(𝜏𝑖′ )K, and by C.10 h𝛾(𝑥𝑖 ), 𝛾(𝑥𝑖 )i ∈ V0𝑘−1 J∅(Γ ′ (𝑥𝑖 ))K. Therefore h𝛾, 𝛾i ∈ V∅𝑘−1 JΓ ′K, and by
Lemma C.11, h𝛾, 𝛾i ∈ V∅𝑗 JΓ ′ K for 𝑗 < 𝑘.
Notice that Δ ′([∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏1 ) = [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏1 = ∅([∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏1 ), Δ ′([∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏2 ) =
[∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏2 = ∅([∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏2 ), as 𝜏1 and 𝜏2 have no free variables. We have to prove that
     s                                s                                                                                𝑠 ′𝑥
(h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i, h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i) ∈ V0𝑘 J(𝑥 : [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏1 ·𝑠 1 ) −−→ [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏2 K.
Notice that if we choose Δ ′ = 0𝑥 1, ..., 0𝑥𝑛 , we can use that same Δ ′ in the induction hypothesis of
Γ ′, 𝑥 : 𝜏1 ; Δ0′ + 𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + 𝑠 ′𝑥, and then we can use the same analogous arguments of the
previous case and Lemma C.10 to conclude the result.                                                                        ⊳
Case (9) Γ; Δ ⊢ 𝑒 1 𝑒 2 : [Σ2/𝑥]𝜏2 ; Σ1 + 𝑠Σ2 + Σ ′′
Subproof. Notice that Δ ′ ·(Σ1 + 𝑠Σ2 + Σ ′′) = (Δ ′ ·Σ1 + 𝑠(Δ ′ ·Σ2 ) + Δ ′ ·Σ ′′), for Δ ′ ⊑ Δ.
We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ 𝑒 1 𝑒 2, 𝛾 2 ⊢ 𝑒 1 𝑒 2 ) ∈ E Δ𝑘 ′ ·Σ1 +𝑠(Δ′ ·Σ2 )+Δ′ ·Σ′′ JΔ ′ ([Σ2/𝑥]𝜏2 )K,
i.e. if 𝛾 1 ⊢ 𝑒 1 𝑒 2 ⇓ 𝑗 𝑣 1′ then 𝛾 2 ⊢ 𝑒 1 𝑒 2 ⇓∗ 𝑣 2′ , and (𝑣 1′ , 𝑣 2′ ) ∈ VΔ𝑘−𝑗                        ′
                                                                                    ′ ·Σ +𝑠(Δ′ ·Σ )+Δ′ ·Σ′′ JΔ ([Σ 2 /𝑥]𝜏 2 )K.
                                                                                        1        2
By induction hypotheses we know that
                                 Σ′′ +𝑠𝑥                                                                                             Σ′′ +𝑠𝑥
Γ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ) −−−−→ 𝜏2 ; Σ1 ⇒ (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E Δ𝑘 ′ ·Σ1 JΔ ′ ((𝑥 : 𝜏1 ·𝑠 ′) −−−−→ 𝜏2 )K and
                                                                                                                                     Σ′′ +𝑠𝑥
Γ ⊢ 𝑒 2 : 𝜏1 ; Σ2 ⇒ (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E 𝑘−𝑗      ′                              ′          ′
                                                 Δ′ ·Σ2 JΔ (𝜏 1 )K for some 𝑗 1 ≤ 𝑘. As Δ ((𝑥 : 𝜏 1𝑠 ) −−−−→ 𝜏 2 ) = (𝑥 :
                                                      1

               Δ′ ·Σ′′ +𝑠𝑥                                                                                                    Δ′ ·Σ′′ +𝑠𝑥
Δ ′(𝜏1 )·𝑠 ′ ) −−−−−−−→ Δ ′(𝜏2 ), by unfolding (𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 J(𝑥 : Δ ′(𝜏1 ·𝑠 ′)) −−−−−−−→ Δ ′(𝜏2 )K, we
know that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 h𝜆(𝑥 : 𝜏1 ). 𝑒 1′ , 𝛾 1′ i then 𝛾 2 ⊢ 𝑒 1 ⇓∗ h𝜆(𝑥 : 𝜏1 ). 𝑒 2′ , 𝛾 2′ i and
                                                                                                     Δ′ ·Σ′′ +𝑠𝑥
(h𝜆 (𝑥 : 𝜏1 ). 𝑒 1′ , 𝛾 1′ i, h𝜆 (𝑥 : 𝜏1 ·𝑠 ′ ). 𝑒 2′ , 𝛾 2′ i) ∈ VΔ𝑘−𝑗
     s                            s                                              ′       ′   −−−−−−→ Δ ′(𝜏2 )K (1).
                                                                     ′ ·Σ J(𝑥 : Δ (𝜏 1 ·𝑠 )) −
                                                                         1

Also, by unfolding (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E Δ𝑘−𝑗  1
                                                       2
                                                         ′       ′
                                                  ′ ·Σ JΔ (𝜏 1 ·𝑠 )K, if 𝛾 1 ⊢ 𝑒 2 ⇓
                                                                                     𝑗2 𝑣 then 𝛾 ⊢ 𝑒 ⇓∗ 𝑣
                                                                                         1      2   2     2
                               1 −𝑗 2
and (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗   ′ ·Σ
                               2
                                      JΔ ′ (𝜏1 )K.
As Δ ·Σ2 ∈ sens, we instantiate (1) with 𝑠 ′′ = Δ ′ ·Σ2 (we know that 𝑠 ′′ ≤ Δ·Σ2 ≤ 𝑠 ′ ), then
         ′
                                                                     1 −𝑗 2 −1
(𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1′ , 𝛾 2′ [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2′ ) ∈ E 𝑘−𝑗    Δ′ ·Σ1 +Δ′ ·Σ′′ +𝑠(Δ′ ·Σ2 )
                                                                                            J[Δ ′ ·Σ2/𝑥]Δ ′(𝜏2 )K. But Δ ′ ·Σ1 + Δ ′ ·Σ ′′ +
𝑠(Δ ·Σ2 ) = Δ ·Σ1 + 𝑠(Δ ·Σ2 ) + Δ ·Σ , and by Lemma 7.5, [Δ ′ ·Σ2/𝑥]Δ ′(𝜏2 ) = Δ ′([Σ2/𝑥]𝜏2 ), therefore
       ′          ′                   ′            ′ ′′
                                                              1 −𝑗 2 −1
(𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1′ , 𝛾 2′ [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2′ ) ∈ E 𝑘−𝑗
                                                         Δ′ ·Σ1 +𝑠(Δ′ ·Σ2 )+Δ′ ·Σ′′
                                                                                    JΔ ′ ([Σ2/𝑥]𝜏2 )K, i.e. if 𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1′ ⇓ 𝑗3 𝑣 1′′
                                                                     1 −𝑗 2 −𝑗 3 −1
then 𝛾 2′ [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2′ ⇓∗ 𝑣 2′′ , and (𝑣 1′′, 𝑣 2′′ ) ∈ VΔ𝑘−𝑗                        ′
                                                                 ′ ·Σ +𝑠(Δ′ ·Σ )+Δ′ ·Σ′′ JΔ ([Σ 2/𝑥]𝜏 2 )K. But notice that by
                                                                     1            2
 app:
                       𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 h𝜆𝑥 . 𝑒 1′ , 𝛾 1′ i          𝛾 1 ⊢ 𝑒 2 ⇓ 𝑗2 𝑣 1            𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ 𝑒 1′ ⇓ 𝑗3 𝑣 1′
                                                            𝛾 1 ⊢ 𝑒 1 𝑒 2 ⇓ 𝑗1 +𝑗2 +𝑗3 +1 𝑣 1′
and
                        𝛾 2 ⊢ 𝑒 1 ⇓∗ h𝜆𝑥 . 𝑒 2′ , 𝛾 2′ i           𝛾 2 ⊢ 𝑒 2 ⇓∗ 𝑣 2          𝛾 1′ [𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 2′ ⇓∗ 𝑣 2′
                                                                 𝛾 2 ⊢ 𝑒 1 𝑒 2 ⇓∗ 𝑣 2′
for 𝑖 ∈ {1, 2}. Notice that 𝑗 = 𝑗 1 + 𝑗 2 + 𝑗 3 + 1, and by premise 𝛾 1′ [𝑥 ↦→ 𝑣 𝑖 ] ⊢ 𝑒𝑖′ ⇓ 𝑗 𝑣 𝑖′ , we know that
𝑣 𝑖′′ = 𝑣 𝑖′ and the result holds immediately.                                                                   ⊳
Case (10) Γ; Δ ⊢ tt : unit ; ∅

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                             83


Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ tt, 𝛾 2 ⊢ tt) ∈ E Δ𝑘 ′ ·∅ JΔ ′ (unit)K, for
Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, Σ(unit) = unit, and 𝛾 1 (tt) = 𝛾 2 (tt) = tt. Then we have to prove
that (tt, tt) ∈ V0𝑘 JunitK which is direct.                                                                    ⊳
                                            ′′
Case (11) Γ; Δ ⊢ inl𝜏2 𝑒 ′ : 𝜏1 Σ ⊕∅ 𝜏2 ; ∅
                                                                                                                                                   ′′
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ inl𝜏2 𝑒 ′, 𝛾 2 ⊢ inl𝜏2 𝑒 ′ ) ∈ E 𝑘Δ′ ·∅ JΔ ′ (𝜏1 Σ ⊕∅
                                                                           ′′                      ′ ′′
𝜏2 )K, for Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, and Δ ′ (𝜏1 Σ ⊕∅ 𝜏2 ) = Δ ′ (𝜏1 ) Δ ·Σ ⊕0 Δ ′(𝜏2 ), then we have to
prove that
                                                                     ′ ′′
(𝛾 1 ⊢ inl𝜏2 𝑒 ′, 𝛾 2 ⊢ inl𝜏2 𝑒 ′ ) ∈ E0𝑘 JΔ ′ (𝜏1 ) Δ ·Σ ⊕0 Δ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ inl𝜏2 𝑒 ′ ⇓ 𝑗 𝑣 1 then 𝛾 2 ⊢
                                                               ′   ′′
inl𝜏2 𝑒 ′ ⇓∗ 𝑣 2 , and (𝑣 1, 𝑣 2 ) ∈ V0𝑘−𝑗 JΔ ′ (𝜏1 ) Δ ·Σ ⊕0 Δ ′ (𝜏2 )K.
By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 ; Σ ′′ , we know that
(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′′ JΔ ′ (𝜏1 )K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1′ , then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2′ and (𝑣 1′ , 𝑣 2′ ) ∈ VΔ𝑘−𝑗       ′
                                                                                                                              ′ ·Σ′′ JΔ (𝜏 1 )K.
                𝜏2 ′ 𝑗                        ′   ∗    ′                                𝜏2 ′
If 𝛾𝑖 ⊢ inl 𝑒 ⇓ 𝑣 𝑖 and 𝛾𝑖 ⊢ 𝑒 ⇓ 𝑣 𝑖 , then by INL, 𝑣 𝑖 = inl 𝑣 𝑖 . Then we have to prove that
                                                      ′ ′′
(inl𝜏2 𝑣 1′ , inl𝜏2 𝑣 2′ ) ∈ V0𝑘−𝑗 JΔ ′ (𝜏1 ) Δ ·Σ ⊕0 Δ ′(𝜏2 )K, i.e. that (𝑣 1′ , 𝑣 2′ ) ∈ VΔ𝑘−𝑗                 ′                    ′ ′′
                                                                                                      ′ ·Σ′′ +0 JΔ (𝜏 1 )K, but as Δ ·Σ +
        ′    ′′
0 = Δ ·Σ , the result holds immediately.                                                                                                       ⊳
                                            ′′
Case (12) Γ; Δ ⊢ inl𝜏2 𝑒 ′ : 𝜏1 Σ ⊕∅ 𝜏2 ; Σ ′
                                                                                                                                                    ′′
Subproof. We have to prove that ∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ inl𝜏2 𝑒 ′, 𝛾 2 ⊢ inl𝜏2 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′ JΔ ′ (𝜏1 Σ ⊕∅
                                                                        ′′                  ′ ′′
𝜏2 )K, for Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, and Δ ′ (𝜏1 Σ ⊕∅ 𝜏2 ) = Δ ′ (𝜏1 ) Δ ·Σ ⊕0 Δ ′(𝜏2 ), then we have to
prove that
                                                                    ′ ′′
(𝛾 1 ⊢ inl𝜏2 𝑒 ′, 𝛾 2 ⊢ inl𝜏2 𝑒 ′ ) ∈ E Δ𝑘 ′ ·Σ′ JΔ ′(𝜏1 ) Δ ·Σ ⊕0 Δ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ inl𝜏2 𝑒 ′ ⇓ 𝑗 𝑣 1 then 𝛾 2 ⊢
inl𝜏2 𝑒 ′ ⇓∗ 𝑣 2 , and (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗          ′       Δ′ ·Σ′′ ⊕ 0 Δ ′ (𝜏 )K.
                                            ′ ·Σ′ JΔ (𝜏 1 )                   2
By induction hypothesis on Γ ⊢ 𝑒 : 𝜏1 ; Σ + Σ ′, we know that
                                                ′           ′′

(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E Δ𝑘 ′ ·(Σ′′ +Σ′ ) JΔ ′ (𝜏1 )K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1′ , then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2′ and (𝑣 1′ , 𝑣 2′ ) ∈
VΔ𝑘−𝑗                ′
    ′ ·(Σ′′ +Σ′ ) JΔ (𝜏 1 )K.

If 𝛾𝑖 ⊢ inl 𝑒 ⇓ 𝑣 𝑖 and 𝛾𝑖 ⊢ 𝑒 ′ ⇓∗ 𝑣 𝑖′ , then by INL, 𝑣 𝑖 = inl𝜏2 𝑣 𝑖′ . Then we have to prove that
                  𝜏2 ′ 𝑗

(inl𝜏2 𝑣 1′ , inl𝜏2 𝑣 2′ ) ∈ VΔ𝑘−𝑗       ′       Δ′ ·Σ′′ ⊕ 0 Δ ′ (𝜏 )K, i.e. that (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗              ′
                                 ′ ·Σ′ JΔ (𝜏 1 )                   2                 1 2          Δ′ ·Σ′′ +Δ′ ·Σ′ JΔ (𝜏 1 )K, but as
  ′      ′′        ′       ′  ′′ ′    ′
Δ ·(Σ + Σ ) = Δ ·Σ + Δ ·Σ , the result holds immediately.                                                                          ⊳
                                                 ′′
Case (13) Γ; Δ ⊢ inr𝜏1 𝑒 ′ : 𝜏1 ∅ ⊕ Σ 𝜏2 ; ∅
                                                                                                                                                 ′′
Subproof. We have to prove that ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ inr𝜏1 𝑒 ′, 𝛾 2 ⊢ inr𝜏1 𝑒 ′ ) ∈ E 𝑘Δ′ ·∅ JΔ ′(𝜏1 ∅ ⊕ Σ
                                                                                ′′                     ′ ′′
𝜏2 )K, for Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, and Δ ′ (𝜏1 ∅ ⊕ Σ 𝜏2 ) = Δ ′ (𝜏1 ) 0 ⊕ Δ ·Σ Δ ′(𝜏2 ), then we have to
prove that
                                                                         ′ ′′
(𝛾 1 ⊢ inr𝜏1 𝑒 ′, 𝛾 2 ⊢ inr𝜏1 𝑒 ′ ) ∈ E0𝑘 JΔ ′ (𝜏1 ) 0 ⊕ Δ ·Σ Δ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ inr𝜏1 𝑒 ′ ⇓ 𝑗 𝑣 1 then 𝛾 2 ⊢
                                                                    ′  ′′
inr𝜏1 𝑒 ′ ⇓∗ 𝑣 2 , and (𝑣 1, 𝑣 2 ) ∈ V0𝑘−𝑗 JΔ ′ (𝜏1 ) 0 ⊕ Δ ·Σ Δ ′ (𝜏2 )K.
By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ , we know that
(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′′ JΔ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1′ , then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2′ and (𝑣 1′ , 𝑣 2′ ) ∈ VΔ𝑘−𝑗       ′
                                                                                                                              ′ ·Σ′′ JΔ (𝜏 2 )K.

If 𝛾𝑖 ⊢ inr𝜏1 𝑒 ′ ⇓ 𝑗 𝑣 𝑖 and 𝛾𝑖 ⊢ 𝑒 ′ ⇓∗ 𝑣 𝑖′ , then by INR, 𝑣 𝑖 = inr𝜏1 𝑣 𝑖′ . Then we have to prove that
                                                           ′ ′′
(inr𝜏1 𝑣 1′ , inr𝜏1 𝑣 2′ ) ∈ V0𝑘−𝑗 JΔ ′ (𝜏1 ) 0 ⊕ Δ ·Σ Δ ′ (𝜏2 )K, i.e. that (𝑣 1′ , 𝑣 2′ ) ∈ V0+Δ       𝑘−𝑗             ′
                                                                                                            ′ ·Σ′′ JΔ (𝜏 2 )K, but as 0 +
  ′    ′′       ′  ′′
Δ ·Σ = Δ ·Σ , the result holds immediately.                                                                                                    ⊳
                                                 ′′
Case (14) Γ; Δ ⊢ inr𝜏1 𝑒 ′ : 𝜏1 ∅ ⊕ Σ 𝜏2 ; Σ ′
                                                                                                                                                   ′′
Subproof. We have to prove that ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ inr𝜏1 𝑒 ′, 𝛾 2 ⊢ inr𝜏1 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′ JΔ ′ (𝜏1 ∅ ⊕ Σ
                                                                      ′′                    ′ ′′
𝜏2 )K, for Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, and Δ ′ (𝜏1 ∅ ⊕ Σ 𝜏2 ) = Δ ′ (𝜏1 ) 0 ⊕ Δ ·Σ Δ ′(𝜏2 ), then we have to
prove that
                                                                 ′ ′′
(𝛾 1 ⊢ inr𝜏1 𝑒 ′, 𝛾 2 ⊢ inr𝜏1 𝑒 ′ ) ∈ E Δ𝑘 ′ ·Σ′ JΔ ′(𝜏1 ) 0 ⊕ Δ ·Σ Δ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ inr𝜏1 𝑒 ′ ⇓ 𝑗 𝑣 1 then 𝛾 2 ⊢
inr𝜏1 𝑒 ′ ⇓∗ 𝑣 2 , and (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗      ′      0 Δ′ ·Σ′′ Δ ′ (𝜏 )K.
                                        ′ ·Σ′ JΔ (𝜏 1 ) ⊕               2


                                       ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
84                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + Σ ′, we know that
(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E Δ𝑘 ′ ·(Σ′′ +Σ′ ) JΔ ′ (𝜏2 )K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1′ , then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2′ and (𝑣 1′ , 𝑣 2′ ) ∈
VΔ𝑘−𝑗                 ′
     ′ ·(Σ′′ +Σ′ ) JΔ (𝜏 2 )K.

If 𝛾𝑖 ⊢ inr𝜏1 𝑒 ′ ⇓ 𝑗 𝑣 𝑖 and 𝛾𝑖 ⊢ 𝑒 ′ ⇓∗ 𝑣 𝑖′ , then by INR, 𝑣 𝑖 = inr𝜏1 𝑣 𝑖′ . Then we have to prove that
(inr𝜏1 𝑣 1′ , inr𝜏1 𝑣 2′ ) ∈ VΔ𝑘−𝑗           ′       0 ⊕ Δ′ ·Σ′′ Δ ′ (𝜏 )K, i.e. that (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗               ′
                                     ′ ·Σ′ JΔ (𝜏 1 )                   2                  1 2          Δ′ ·Σ′ +Δ′ ·Σ′′ JΔ (𝜏 2 )K, but as
  ′       ′′        ′       ′  ′′    ′    ′
Δ ·(Σ + Σ ) = Δ ·Σ + Δ ·Σ , the result holds immediately.                                                                               ⊳
Case (15) Γ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } : [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ; Σ1 ⊔ ([Σ1 +
Σ11/𝑥](Σ2 + 𝑠 2𝑥) ⊔ [Σ1 + Σ12/𝑦](Σ3 + 𝑠 3𝑦))
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK,
(𝛾 1 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 }, 𝛾 2 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 }) ∈ E Δ𝑘 ′ ·Σ′′ JΔ ′ (𝜏 ′)K, for
Δ ′ ⊑ Δ, where
Σ ′′ = Σ1 ⊔ ([Σ1 + Σ11 /𝑥](Σ2 +𝑠 2 𝑥) ⊔ [Σ1 + Σ12 /𝑦](Σ3 +𝑠 3𝑦)) = Σ1 ⊔ ((𝑠 2 Σ1 +𝑠 2 Σ11 Σ2 ) ⊔ (𝑠 3 Σ1 +𝑠 3 Σ12 Σ2 )),
and 𝜏 ′ = [Σ1 + Σ11/𝑥]𝜏2 ⊔ [Σ1 + Σ12/𝑦]𝜏3 .
By induction hypothesis on Γ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1 , we know that
(𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏11 Σ11 ⊕ Σ12 𝜏12 )K, i.e. if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11 , then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑣 12 and (𝑣 11 , 𝑣 12 ) ∈
                       ′         ′
VΔ𝑘−𝑗    1    ′
     ′ ·Σ JΔ (𝜏 11 )
         1
                        Δ ·Σ11 ⊕ Δ ·Σ12 Δ ′ (𝜏 )K. Either 𝑣
                                                 12
                                                                                      ′                         ′
                                                                      11 = inl 𝑣 11 and 𝑣 12 = inl 𝑣 12 , 𝑣 11 = inr 𝑣 11 and
                                                                                                                                         ′
                   ′                   ′                            ′                         ′                        ′
𝑣 12 = inr 𝑣 12 , 𝑣 11 = inl 𝑣 11 and 𝑣 12 = inr 𝑣 12 , or 𝑣 11 = inr 𝑣 11 and 𝑣 12 = inl 𝑣 12 . We proceed by
case analysis on (𝑣 11, 𝑣 12 ):
Case (a) (𝑣 11 , 𝑣 12 ) = (inl 𝑣 11    ′ , inl 𝑣 ′ ) (the case (𝑣 , 𝑣 ) = (inr 𝑣 ′ , inr 𝑣 ′ ) is analogous)
                                                     12                     11 12                11          12
Subproof. By Lemma C.1 Δ ′ ·Σ1 + Δ ′ ·Σ11 = Δ ′ ·(Σ1 + Σ11 ), then (𝑣 11                           ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗1           JΔ ′ (𝜏11 )K.
                                                                                                         12      Δ′ ·(Σ1 +Σ11 )
Also, by induction hypothesis on Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 2 𝑥, by choosing
Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥 ⊑ Δ + (Δ·(Σ1 + Σ11 ))𝑥 and 𝑘 = 𝑘 − 𝑗 1 (and by weakening lemma C.11)
(𝛾 1 [𝑥 ↦→ 𝑣 12   ′ ], 𝛾 [𝑥 ↦→ 𝑣 ′ ]) ∈ G𝑘−𝑗1 −1                           JΓ, 𝑥 : 𝜏11 K (note that 𝑥 ∉ 𝑑𝑜𝑚(Σ1) ∪ 𝑑𝑜𝑚(Σ11),
                         2            22             Δ′ +(Δ′ ·(Σ1 +Σ11 ))𝑥
therefore (Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥)(𝜏11 ) = Δ ′(𝜏11 )) we know that
(𝛾 1 [𝑥 ↦→ 𝑣 12 ′ ] ⊢ 𝑒 , 𝛾 [𝑥 ↦→ 𝑣 ′ ] ⊢ 𝑒 ) ∈ E 𝑘−𝑗1                                        J(Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥)(𝜏2)K.
                         2 2              22       2         (Δ′+(Δ′ ·(Σ1 +Σ11 ))𝑥)·(Σ2 +𝑠2𝑥)
But (Δ + (Δ ·(Σ1 + Σ11 ))𝑥)·(Σ2 + 𝑠 2𝑥) = Δ ·Σ2 + 𝑠 2 (Δ ·(Σ1 + Σ11 )) = Δ ′ ·(𝑠 2 (Σ1 + Σ11 ) + Σ2 ), and by
           ′         ′                                           ′               ′

Lemma C.2 and because Δ ′ ·(Σ1 +Σ11 ) ∈ sens, then (Δ ′ +(Δ ′ ·(Σ1 +Σ11 ))𝑥)(𝜏2 ) = (Δ ′ ·(Σ1 +Σ11 ))𝑥(Δ ′(𝜏2 )),
and by Lemma 7.5 (Δ ′ ·(Σ1 +Σ11 ))𝑥(Δ ′(𝜏2 )) = Δ ′([Σ1 +Σ11 /𝑥]𝜏2 ). Therefore if 𝛾 1 [𝑥 ↦→ 𝑣 12                           ′ ] ⊢ 𝑒 ⇓ 𝑗2 𝑣 ,
                                                                                                                                      2       21
                       ′            ∗
then 𝛾 2 [𝑥 ↦→ 𝑣 22 ] ⊢ 𝑒 2 ⇓ 𝑣 22 , and
                      𝑘−𝑗 −𝑗
(𝑣 21, 𝑣 22 ) ∈ VΔ′ ·(𝑠12 Σ12+𝑠2 Σ11 +Σ2 ) JΔ ′ ([Σ1 + Σ11/𝑥]𝜏2 )K.
By following the case-left reduction rule:
                                                          ′                       ′
                                     𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 inl 𝑣 11          𝛾 1 [𝑥 ↦→ 𝑣 11 ] ⊢ 𝑒 2 ⇓ 𝑗2 𝑣 21
                                     𝛾 1 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑥 ⇒ 𝑒 3 } ⇓ 𝑗1 +𝑗2 +1 𝑣 21
and
                                      𝛾 2 ⊢ 𝑒 1 ⇓∗ inl 𝑣 12
                                                         ′                        ′
                                                                      𝛾 2 [𝑥 ↦→ 𝑣 12 ] ⊢ 𝑒 2 ⇓∗ 𝑣 22
                                       𝛾 2 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑥 ⇒ 𝑒 3 } ⇓∗ 𝑣 22
for 𝑖 ∈ {1, 2}. Then we just have to prove that
                       1 −𝑗 2 −1
(𝑣 21, 𝑣 22 ) ∈ VΔ𝑘−𝑗         2 1 2 11 2    3 1 3 12   3
                                                           ′
                   ′ ·(Σ ⊔(𝑠 Σ +𝑠 Σ +Σ )⊔(𝑠 Σ +𝑠 Σ +Σ )) JΔ ([Σ 1 + Σ 11 /𝑥]𝜏 2 ⊔ [Σ 1 + Σ 12 /𝑦]𝜏 3 )K. Notice that by
                        1
deﬁnition of the join operator (𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) <: (𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 Σ1 + 𝑠 3 Σ12 + Σ3 ), also
(𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 Σ1 + 𝑠 3 Σ12 + Σ3 ) <: Σ1 ⊔ (𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 Σ1 + 𝑠 3 Σ12 + Σ3 ) therefore
by Lemma C.12 Δ ′ ·(𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ≤ Δ ′ ·(Σ1 ⊔ (𝑠 2 Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 Σ1 + 𝑠 3 Σ12 + Σ3 )).
Also [Σ1 + Σ11 /𝑥]𝜏2 <: [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 therefore by Lemma C.6,
Δ ′([Σ1 + Σ11 /𝑥]𝜏2 ) <: Δ ′([Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ). Finally by Lemma C.10,

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                           85

                   𝑘−𝑗 −𝑗
(𝑣 21 , 𝑣 22 ) ∈ VΔ′ ·(Σ11 ⊔(𝑠2 2 Σ1 +𝑠2 Σ11 +Σ2 )⊔(𝑠3 Σ1 +𝑠3 Σ12 +Σ3 )) JΔ ′ ([Σ1 + Σ11/𝑥]𝜏2 ⊔ [Σ1 + Σ12/𝑦]𝜏3 )K and the result
holds by Lemma C.11.                                                                                                           ⊳
                                          ′            ′                                      ′         ′
Case (b) (𝑣 11 , 𝑣 12 ) = (inl 𝑣 11          , inr 𝑣 12   ) (the case (𝑣 11, 𝑣 12 ) = (inr 𝑣 11 , inl 𝑣 12 ) is analogous)
Subproof. Then Δ ′ ·Σ1 = ∞, and the result vacuously holds.                                                                    ⊳
                                                                                                                               ⊳
Case (16) Γ; Δ ⊢ (𝑒 1, 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; ∅
Subproof. We have to prove that
∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ (𝑒 1, 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1, 𝑒 2 )) ∈ E Δ𝑘 ′ ·∅ JΔ ′ (𝜏1 Σ1 &Σ2 𝜏2 )K, for Δ ′ ⊑ Δ. Notice that
                                                            ′        ′
Δ ′ ·∅ = 0, and Δ ′(𝜏1 Σ1 &Σ2 𝜏2 ) = Δ ′(𝜏1 ) Δ ·Σ1 &Δ ·Σ2 Δ ′(𝜏2 ), then we have to prove that
                                                      ′        Δ′ ·Σ1 Δ′ ·Σ2
                                                𝑘
(𝛾 1 ⊢ (𝑒 1 , 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1 , 𝑒 2 )) ∈ E0 JΔ (𝜏1 )                 &        Δ ′(𝜏2 )K, i.e. if 𝛾 1 ⊢ (𝑒 1 , 𝑒 2 ) ⇓ 𝑗 (𝑣 11 , 𝑣 12 ) and
                                                                               𝑘−𝑗             ′       ′
𝛾 2 ⊢ (𝑒 1, 𝑒 2 ) ⇓ 𝑗 (𝑣 21 , 𝑣 22 ), then ((𝑣 11, 𝑣 12 ), (𝑣 21, 𝑣 22 )) ∈ V0 JΔ ′ (𝜏1 ) Δ ·Σ1 &Δ ·Σ2 Δ ′(𝜏2 )K, or equivalently
                     𝑘−𝑗            ′                                   𝑘−𝑗       ′
(𝑣 11, , 𝑣 21 ) ∈ V0+Δ   ′ ·Σ JΔ (𝜏 1 )K, and (𝑣 12 , , 𝑣 22 ) ∈ V0+Δ′ ·Σ JΔ (𝜏 2 )K.
                             1                                               2
By induction hypothesis on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 , we know that (𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈
E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏1 )K and (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E Δ𝑘 ′ ·Σ2 JΔ ′(𝜏2 )K respectively. This means that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11           ′
                                                                                                                                            ,
                     ′ then (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗1 JΔ ′ (𝜏 )K, and that if 𝛾 ⊢ 𝑒 ⇓ 𝑗2 𝑣 ′ , and 𝛾 ⊢ 𝑒 ⇓ 𝑗2 𝑣 ′ then
and 𝛾 2 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 12        11 12        Δ′ ·Σ1       1                 1   2       21       2   2       22
   ′      ′        𝑘−𝑗
(𝑣 21 , 𝑣 22 ) ∈ VΔ′ ·Σ22 JΔ ′(𝜏2 )K. As reduction is deterministic, then 𝑗 = 𝑗 1 + 𝑗 2 and 𝑣 𝑖′𝑗 = 𝑣 𝑖 𝑗 , therefore as
0 + Δ ·Σ𝑖 = Δ ′ ·Σ𝑖 , the result holds immediately by Lemma C.11.
         ′

                                                                                                                       ⊳
                                         ′        ′
Case (17) Γ; Δ ⊢ (𝑒 1, 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ1′′ ⊔ Σ2′′
Subproof.
                                   Γ; Δ ⊢ 𝑒 1 : 𝜏1 ; Σ1′′ + Σ1′           Γ; Δ ⊢ 𝑒 2 : 𝜏2 ; Σ2′′ + Σ2′
                                                                      ′    ′
                                             Γ; Δ ⊢ (𝑒 1 , 𝑒 2 ) : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ1′′ ⊔ Σ2′′

We have to prove that
                                                                                                     ′   ′
∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ (𝑒 1, 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1 , 𝑒 2 )) ∈ E Δ𝑘 ′ ·(Σ′′ ⊔Σ′′ ) JΔ ′(𝜏1 Σ1 &Σ2 𝜏2 )K, for Δ ′ ⊑ Δ. Let
                                                                                   1           2
                                                                                                               ′   ′                  ′    ′
𝑑𝑖′ = Δ ′ ·Σ𝑖′ and 𝑑𝑖′′ = Δ ′ ·Σ𝑖′′ . Notice that Δ ′ ·(Σ1′′ ⊔ Σ2′′) = 𝑑 1′′ ⊔ 𝑑 2′′ , and Δ ′ (𝜏1 Σ1 &Σ2 𝜏2 ) = Δ ′(𝜏1 ) 𝑑1 &𝑑2
Δ ′(𝜏2 ), then we have to prove that
                                                                ′   ′
(𝛾 1 ⊢ (𝑒 1, 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1, 𝑒 2 )) ∈ E𝑑𝑘′′⊔𝑑 ′′ JΔ ′ (𝜏1 ) 𝑑1 &𝑑2 Δ ′(𝜏2 )K, i.e. if 𝛾 1 ⊢ (𝑒 1, 𝑒 2 ) ⇓ 𝑗 (𝑣 11, 𝑣 12 ) then 𝛾 2 ⊢
                                              1       2
                                                                                           ′               ′
(𝑒 1, 𝑒 2 ) ⇓∗ (𝑣 21, 𝑣 22 ), and ((𝑣 11, 𝑣 12 ), (𝑣 21, 𝑣 22 )) ∈ V𝑑𝑘−𝑗
                                                                      ′′
                                                                               ′      𝑑 𝑑     ′
                                                                          ′′ JΔ (𝜏 1 ) 1 & 2 Δ (𝜏 2 )K.
                                                                     1 ⊔𝑑 2
By induction hypothesis on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1′′ + Σ1′ and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2′′ + Σ2′ , we know that
(𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈ E𝑑𝑘′ +𝑑 ′′ JΔ ′(𝜏1 )K and (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑𝑘′ +𝑑 ′′ JΔ ′(𝜏2 )K respectively. This means
                               1   1                                                       2           2
                         ′ , then 𝛾 ⊢ 𝑒 ⇓∗ 𝑣 ′ and (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗1 JΔ ′ (𝜏 )K, and that if 𝛾 ⊢ 𝑒 ⇓ 𝑗2 𝑣 ′ ,
that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11        2   1     12       11 12        𝑑 ′ +𝑑 ′′    1                 1   2       21
                                                                                       1           1
                                                          𝑘−𝑗
then 𝛾 2 ⊢ 𝑒 2 ⇓∗ 𝑣 22
                    ′         ′
                       and (𝑣 21     ′
                                 , 𝑣 22 ) ∈ V𝑑 ′ +𝑑2′′ JΔ ′(𝜏2 )K. Notice that 𝑑𝑖′′ ≤ 𝑑 1′′ ⊔ 𝑑 2′′ . As reduction is
                                               2    2
deterministic, then 𝑗 = 𝑗 1 + 𝑗 2 and 𝑣 𝑖′𝑗 = 𝑣 𝑖 𝑗 , therefore as 0 + 𝑑𝑖′ + 𝑑𝑖′′ = 𝑑𝑖′ + 𝑑𝑖′′ , the result holds
immediately by Lemma C.11.
                                                                                                                    ⊳
Case (18) Γ; Δ ⊢ fst 𝑒 ′ : 𝜏1 ; Σ ′′ + Σ1
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ fst 𝑒 ′, 𝛾 2 ⊢ fst 𝑒 ′ ) ∈
E 𝑘Δ′ ·(Σ′′ +Σ1 ) JΔ ′ (𝜏1 )K, for Δ ′ ⊑ Δ. By induction hypothesis on Γ ⊢ 𝑒 ′ : 𝜏1 Σ1 &Σ2 𝜏2 ; Σ ′′ we know
that
(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ′′ JΔ ′ (𝜏1 Σ1 &Σ2 𝜏2 )K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 (𝑣 11, 𝑣 12 ) then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ (𝑣 21, 𝑣 22 ),

                                       ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
86                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter

                                        𝑘−𝑗                 ′       ′                                                            𝑘−𝑗
and ((𝑣 11, 𝑣 12 ), (𝑣 21, 𝑣 22 )) ∈ VΔ′ ·Σ′′ JΔ ′ (𝜏1 ) Δ ·Σ1 &Δ ·Σ2 Δ ′(𝜏2 )K, or equivalently (𝑣 11, , 𝑣 21 ) ∈ VΔ′ ·Σ′′ +Δ′ ·Σ1 JΔ ′ (𝜏1 )K,
and (𝑣 12, , 𝑣 22 ) ∈ VΔ𝑘−𝑗              ′
                         ′ ·Σ′′ +Δ′ ·Σ JΔ (𝜏 2 )K.
                                      2
Following the proj1 reduction rule, if:
                                                          𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 (𝑣 11, 𝑣 12 )
                                                           𝛾 1 ⊢ fst 𝑒 ′ ⇓ 𝑗 𝑣 11
and
                                                          𝛾 2 ⊢ 𝑒 ′ ⇓∗ (𝑣 21, 𝑣 22 )
                                                           𝛾 2 ⊢ fst 𝑒 ′ ⇓∗ 𝑣 21

Then we have to prove that (𝑣 11 , 𝑣 21 ) ∈ VΔ𝑘−𝑗                               ′
                                                                 ′ ·(Σ′′ +Σ ) JΔ (𝜏 1 )K, but as by Lemma C.1, Δ ·(Σ
                                                                           1
                                                                                                                           ′     ′′ + Σ ) =
                                                                                                                                       1
   ′    ′′      ′
Δ ·Σ + Δ ·Σ1 , the result holds immediately.                                                                                                ⊳
                         ′
Case (19) snd 𝑒 : 𝜏1 ; Σ + Σ2         ′′

Subproof. Analogous to previous case.                                                                                                       ⊳
Case (20) Γ; Δ ⊢ h𝑒 1 , 𝑒 2 i : 𝜏1 Σ1 ⊗ Σ2 𝜏2 ; ∅
Subproof. We have to prove that ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ h𝑒 1 , 𝑒 2 i, 𝛾 2 ⊢ h𝑒 1 , 𝑒 2 i) ∈ E Δ𝑘 ′ ·∅ JΔ ′ (𝜏1 Σ1 ⊗ Σ2
                                                                                                  ′        ′
𝜏2 )K, for Δ ′ ⊑ Δ. Notice that Δ ′ ·∅ = 0, and Δ ′ (𝜏1 Σ1 ⊗ Σ2 𝜏2 ) = Δ ′ (𝜏1 ) Δ ·Σ1 ⊗ Δ ·Σ2 Δ ′(𝜏2 ), then we have
to prove that
                                                            ′         ′
(𝛾 1 ⊢ h𝑒 1 , 𝑒 2 i, 𝛾 2 ⊢ h𝑒 1 , 𝑒 2 i) ∈ E0𝑘 JΔ ′ (𝜏1 ) Δ ·Σ1 ⊗ Δ ·Σ2 Δ ′(𝜏2 )K, i.e. if 𝛾 1 ⊢ h𝑒 1 , 𝑒 2 i ⇓ 𝑗1 h𝑣 11 , 𝑣 12 i then 𝛾 2 ⊢
                                                                                              ′     ′
h𝑒 1 , 𝑒 2 i ⇓∗ h𝑣 21 , 𝑣 22 i, and (h𝑣 11 , 𝑣 12 i, h𝑣 21 , 𝑣 22 i) ∈ V0𝑘−𝑗 JΔ ′ (𝜏1 ) Δ ·Σ1 ⊗ Δ ·Σ2 Δ ′ (𝜏2 )K, or equivalently
                     𝑘−𝑗          ′                                  𝑘−𝑗        ′
(𝑣 11, 𝑣 21 ) ∈ V0+Δ     ′ ·Σ JΔ (𝜏 1 )K, and (𝑣 12 , 𝑣 22 ) ∈ V0+Δ′ ·Σ JΔ (𝜏 2 )K.
                             1                                               2
By induction hypothesis on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1 and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2 , we know that (𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈
E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏1 )K and (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E Δ𝑘 ′ ·Σ2 JΔ ′(𝜏2 )K respectively. This means that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11           ′
                                                                                                                                             ,
                    ′ and (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗1 JΔ ′ (𝜏 )K, and that if 𝛾 ⊢ 𝑒 ⇓ 𝑗2 𝑣 ′ , then 𝛾 ⊢ 𝑒 ⇓∗ 𝑣 ′
then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑣 12       11 12        Δ′ ·Σ1       1                 1   2       21        2   2     22
       ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗2 JΔ ′ (𝜏 )K. As reduction is deterministic, then 𝑗 = 𝑗 + 𝑗 and 𝑣 ′ = 𝑣 , therefore
and (𝑣 21    22      Δ′ ·Σ2      2                                             1   2     𝑖𝑗    𝑖𝑗
as 0 + Δ ′ ·Σ𝑖 = Δ ′ ·Σ𝑖 , the result holds immediately by Lemma C.11.
                                                                                                          ⊳
                                   Σ′  Σ′     ′′     ′′
Case (21) Γ; Δ ⊢ (𝑒 1, 𝑒 2 ) : 𝜏1 1 ⊗ 2 𝜏2 ; Σ1 + Σ2
Subproof.
                                   Γ; Δ ⊢ 𝑒 1 : 𝜏1 ; Σ1′′ + Σ1′                 Γ; Δ ⊢ 𝑒 2 : 𝜏2 ; Σ2′′ + Σ2′
                                                                         Σ′1      ′
                                              Γ; Δ ⊢ (𝑒 1 , 𝑒 2 ) : 𝜏1         ⊗ Σ2 𝜏2 ; Σ1′′ + Σ2′′
We have to prove that
                                                                                                     ′    ′
∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ (𝑒 1 , 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1, 𝑒 2 )) ∈ E 𝑘Δ′ ·(Σ′′ +Σ′′ ) JΔ ′ (𝜏1 Σ1 ⊗ Σ2 𝜏2 )K, for Δ ′ ⊑ Δ. Let 𝑑𝑖′ =
                                                                                      1   2
                                                                                                              ′   ′          ′     ′
Δ ′ ·Σ𝑖′ and 𝑑𝑖′′ = Δ ′ ·Σ𝑖′′ . Notice that Δ ′ ·(Σ1′′ + Σ2′′) = 𝑑 1′′ +𝑑 2′′ , and Δ ′(𝜏1 Σ1 ⊗ Σ2 𝜏2 ) = Δ ′(𝜏1 ) 𝑑1 ⊗𝑑2 Δ ′(𝜏2 ),
then we have to prove that
                                                                ′   ′
(𝛾 1 ⊢ (𝑒 1, 𝑒 2 ), 𝛾 2 ⊢ (𝑒 1, 𝑒 2 )) ∈ E𝑑𝑘′′+𝑑 ′′ JΔ ′ (𝜏1 ) 𝑑1 ⊗𝑑2 Δ ′(𝜏2 )K, i.e. if 𝛾 1 ⊢ (𝑒 1 , 𝑒 2 ) ⇓ 𝑗 (𝑣 11 , 𝑣 12 ) then 𝛾 2 ⊢
                                               1   2
                                                                        𝑘−𝑗                       ′       ′
(𝑒 1, 𝑒 2 ) ⇓∗ (𝑣 21, 𝑣 22 ), and ((𝑣 11, 𝑣 12 ), (𝑣 21, 𝑣 22 )) ∈ V𝑑 ′′+𝑑 ′′ JΔ ′(𝜏1 ) 𝑑1 ⊗𝑑2 Δ ′ (𝜏2 )K.
                                                                      1    2
By induction hypothesis on Γ ⊢ 𝑒 1 : 𝜏1 ; Σ1′′ + Σ1′ and Γ ⊢ 𝑒 2 : 𝜏2 ; Σ2′′ + Σ2′ , we know that
(𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈ E𝑑𝑘′ +𝑑 ′′ JΔ ′(𝜏1 )K and (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E𝑑𝑘′ +𝑑 ′′ JΔ ′(𝜏2 )K respectively. This means
                               1   1                                                              2       2
                         ′ , then 𝛾 ⊢ 𝑒 ⇓∗ 𝑣 ′ and (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗1 JΔ ′ (𝜏 )K, and that if 𝛾 ⊢ 𝑒 ⇓ 𝑗2 𝑣 ′ ,
that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11        2   1     12       11 12        𝑑 ′ +𝑑 ′′    1                 1   2       21
                                                                                              1       1
                    ′ and (𝑣 ′ , 𝑣 ′ ) ∈ V 𝑘−𝑗2 JΔ ′ (𝜏 )K. Notice that 𝑑 ′′ ≤ 𝑑 ′′ + 𝑑 ′′ . As reduction is
then 𝛾 2 ⊢ 𝑒 2 ⇓∗ 𝑣 22       21 22        𝑑 ′ +𝑑 ′′    2                 𝑖      1      2
                                                            2   2


ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                     87


deterministic, then 𝑗 = 𝑗 1 + 𝑗 2 and 𝑣 𝑖′𝑗 = 𝑣 𝑖 𝑗 , therefore as 0 + 𝑑𝑖′ + 𝑑𝑖′′ = 𝑑𝑖′ + 𝑑𝑖′′ , the result holds
immediately by Lemma C.11.
                                                                                                                ⊳
Case (22) Γ; Δ ⊢ let 𝑥 1 , 𝑥 2 = 𝑒 1 in 𝑒 2 : [Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ; 𝑠 1 (Σ11 + Σ1 ) +𝑠 2 (Σ12 + Σ1 ) + Σ2
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ let 𝑥 1, 𝑥 2 = 𝑒 1 in 𝑒 2 , 𝛾 2 ⊢
let 𝑥 1, 𝑥 2 = 𝑒 1 in 𝑒 2 ) ∈ E 𝑘Δ′ ·(Σ′′ ) JΔ ′ (𝜏)K, for Δ ′ ⊑ Δ. where Σ ′′ = 𝑠 1 (Σ11 + Σ1 ) + 𝑠 2 (Σ12 + Σ1 ) + Σ2 .
Suppose
                              𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 h𝑣 11 , 𝑣 12 i       𝛾 1 [𝑥 1 ↦→ 𝑣 11 , 𝑥 2 ↦→ 𝑣 12 ] ⊢ 𝑒 2 ⇓ 𝑗2 𝑣 1′
                                              𝛾 1 ⊢ let 𝑥 1, 𝑥 2 = 𝑒 1 in 𝑒 2 ⇓ 𝑗1 +𝑗2 +1 𝑣 1′


By induction hypothesis on Γ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊗ Σ12 𝜏12 ; Σ1 we know that
(𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏11 Σ11 ⊗ Σ12 𝜏12 )K, i.e. if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 h𝑣 11 , 𝑣 12 i then 𝛾 2 ⊢ 𝑒 1 ⇓∗ h𝑣 21 , 𝑣 22 i,
                                                              ′          ′
and (h𝑣 11, 𝑣 12 i, h𝑣 21 , 𝑣 22 i) ∈ VΔ𝑘−𝑗  1  ′
                                         ′ ·Σ JΔ (𝜏 11 )
                                             1
                                                         Δ ·Σ11 ⊗ Δ ·Σ12 Δ ′ (𝜏 )K, or equivalently
                                                                               12
                    𝑘−𝑗                                                         𝑘−𝑗
(𝑣 11, 𝑣 21 ) ∈ VΔ′ ·Σ11 +Δ′ ·Σ11 JΔ ′ (𝜏11 )K, and (𝑣 12, 𝑣 22 ) ∈ VΔ′ ·Σ11 +Δ′ ·Σ12 JΔ ′(𝜏12 )K. By Lemma C.1 Δ ′ ·Σ1 +
Δ ′ ·Σ11 = Δ ′ ·(Σ1 + Σ11 ), then (𝑣 11, 𝑣 12 ) ∈ VΔ𝑘−𝑗   1  11
                                                                  ′                           ′        ′
                                                     ′ ·(Σ +Σ ) JΔ (𝜏 11 )K, and analogously Δ ·Σ 1 + Δ ·Σ 12 =

Δ ′ ·(Σ1 + Σ12 ), then (𝑣 22 , 𝑣 22 ) ∈ VΔ𝑘−𝑗                          ′
                                                       ′ ·(Σ +Σ ) JΔ (𝜏 12 )K
                                                            1   12
Also, by induction hypothesis on Γ, 𝑥 : 𝜏11, 𝑥 : 𝜏12 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 1 + (Δ·(Σ1 + Σ12 ))𝑥 2 ⊢ 𝑒 2 : 𝜏2 ;
Σ2 + 𝑠 1𝑥 1 + 𝑠 2𝑥 2 , by choosing 𝑘 = 𝑘 − 𝑗 1
                                                                                  1 −1
(𝛾 1 [𝑥 1 ↦→ 𝑣 11 , 𝑥 2 ↦→ 𝑣 12 ], 𝛾 2 [𝑥 1 ↦→ 𝑣 21 , 𝑥 2 ↦→ 𝑣 22 ]) ∈ GΔ𝑘−𝑗  ′ +(Δ′ ·(Σ +Σ ))𝑥 +(Δ′ ·(Σ +Σ ))𝑥 JΓ, 𝑥 : 𝜏 11 K (note
                                                                                        1  11  1        1  12  2
that 𝑥 1 ∉ 𝑑𝑜𝑚(Σ1) ∪ 𝑑𝑜𝑚(Σ11 ) and 𝑥 2 ∉ 𝑑𝑜𝑚(Σ1) ∪ 𝑑𝑜𝑚(Σ12), therefore (Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥 1 +
(Δ ′·(Σ1 + Σ12 ))𝑥 2 )(𝜏1𝑖 ) = Δ ′(𝜏1𝑖 )) we know that
(𝛾 1′ ⊢ 𝑒 2, 𝛾 2′ ⊢ 𝑒 2 ) ∈ E 𝑘−𝑗   1
                              Σ′′ ·(Σ2 +𝑠1 𝑥 1 +𝑠2 𝑥 2 )
                                                         JΣ ′′ (𝜏2 )K,
for 𝛾𝑖′ = 𝛾 1 [𝑥 1 ↦→ 𝑣 𝑖1, 𝑥 2 ↦→ 𝑣 𝑖2], Σ ′′ = Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥 1 + (Δ ′ ·(Σ1 + Σ12 ))𝑥 2 .
But (Δ ′ +(Δ ′ ·(Σ1 + Σ11 ))𝑥 1 +(Δ ′·(Σ1 + Σ12 ))𝑥 2 )·(Σ2 +𝑠 1𝑥 1 +𝑠 2𝑥 2 ) = Δ ′ ·Σ2 +𝑠 1 (Δ ′ ·(Σ1 + Σ11 ))+𝑠 2 (Δ ′ ·(Σ1 +
Σ12 )) = Δ ′ ·(𝑠 1 (Σ1 + Σ11 ) + 𝑠 2 (Σ1 + Σ12 ) + Σ2 ), and by Lemma C.2 and because Δ ′ ·(Σ1 + Σ1𝑖 ) ∈ sens,
then (Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥 1 + (Δ ′ ·(Σ1 + Σ12 ))𝑥 2 )(𝜏2 ) = ((Δ ′·(Σ1 + Σ11 ))𝑥 1 + (Δ ′ ·(Σ1 + Σ12 ))𝑥 2 )(Δ ′(𝜏2 )),
and by Lemma 7.5 ((Δ ′·(Σ1 + Σ11 ))𝑥 1 + (Δ ′ ·(Σ1 + Σ12 ))𝑥 2 )(Δ ′(𝜏2 )) = Δ ′ ([Σ1 + Σ11/𝑥 1 ][Σ1 + Σ12 /𝑥 2 ]𝜏2 ).
Therefore if 𝛾 1′ ⊢ 𝑒 2 ⇓ 𝑗2 𝑣 1′ , then 𝛾 2′ ⊢ 𝑒 2 ⇓∗ 𝑣 2′ , and
                       𝑘−𝑗 −𝑗
(𝑣 21, 𝑣 22 ) ∈ VΔ′ ·(𝑠11 (Σ21 +Σ11 )+𝑠2 (Σ1 +Σ12 )+Σ2 ) JΔ ′([Σ1 + Σ11 /𝑥 1 ][Σ1 + Σ12/𝑥 2 ]𝜏2 )K, and the result holds by
Lemma C.11.                                                                                                                        ⊳
Case (23) Γ; Δ ⊢ (𝑒 ′ :: 𝜏) : 𝜏 ; Σ
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, (𝛾 1 ⊢ (𝑒 ′ :: 𝜏), 𝛾 2 ⊢ (𝑒 ′ :: 𝜏)) ∈
E 𝑘Δ′ ·Σ JΔ ′ (𝜏)K, for Δ ′ ⊑ Δ. By induction hypothesis on Γ; Δ ⊢ 𝑒 ′ : 𝜏 ′ ; Σ where 𝜏 ′ <: 𝜏, we know that
(𝛾 1 ⊢ 𝑒 ′, 𝛾 2 ⊢ 𝑒 ′ ) ∈ E 𝑘Δ′ ·Σ JΔ ′ (𝜏 ′)K, i.e. if 𝛾 1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1 then 𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2 , and (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗     ′ ′
                                                                                                                       ′ ·Σ JΔ (𝜏 )K.
Following the ascr reduction rule, if:
                                       𝛾1 ⊢ 𝑒 ′ ⇓ 𝑗 𝑣 1                                  𝛾 2 ⊢ 𝑒 ′ ⇓∗ 𝑣 2
                                   𝛾 1 ⊢ 𝑒 ′ :: 𝜏 ⇓ 𝑗+1 𝑣 1                           𝛾 2 ⊢ 𝑒 ′ :: 𝜏 ⇓∗ 𝑣 2


Then we have to prove that (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗−1
                                            ′ ·Σ JΔ ′ (𝜏)K. As 𝜏 ′ <: 𝜏, by Lemma C.6 Δ ′ (𝜏 ′) <: Δ ′(𝜏), and
the result holds immediately by Lemma C.11.                                                                  ⊳
                          p                                       Σ′′
Case (24) Γ; Δ ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′ : (𝑥 : 𝜏1 ·𝑑 ′ ) −−→
                                                        → 𝜏2 ; ∅

                                        ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
88                   Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Subproof. We have to prove that ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK,
         p                             p                                                   Δ′ ·Σ′′
(𝛾 1 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 ′ ). e′, 𝛾 2 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′ ) ∈ E 𝑘Δ′ ·∅ JΔ ′ (𝑥 : 𝜏1 ·𝑑 ′ ) −−−−→
                                                                                            → Δ ′(𝜏2 )K, for Δ ′ ⊑ Δ.
Notice that Δ ′ ·∅ = 0, and that lambdas reduce to closures, therefore we have to prove that
     p                             p                                                        Δ′ ·Σ′′
(h𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′, 𝛾 1 i, h𝜆 (𝑥 : 𝜏1 ·𝑑 ′). e′, 𝛾 2 i) ∈ V0𝑘 J(𝑥 : Δ ′(𝜏1 )·𝑑 ′) −−−−→
                                                                                         → Δ ′ (𝜏2 )K.
                                                                  𝑗
Consider 𝑗 < 𝑘, 𝑣 1 and 𝑣 2 such that (𝑣 1, 𝑣 2 ) ∈ V𝑑 ′′ JΔ (𝜏1 )K, for some 𝑑 ′′ ≤ 𝑑 ′. We have to prove that
                                                                       ′
                                                 𝑗
(𝛾 1, 𝑥 ↦→ 𝑣 1 ⊢ e′, 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ e′) ∈ E(Δ                      ′′   ′                                  ′′  ′
                                                    ′+𝑑 ′′𝑥)·Σ′′ J𝑑 𝑥(Δ (𝜏 2 ))K. Notice that by Lemma C.2 𝑑 𝑥(Δ (𝜏 2 )) =
                                                                                                                   𝑗
(Δ ′ +𝑑 ′′𝑥)(𝜏2 ), therefore we have to prove that (𝛾 1, 𝑥 ↦→ 𝑣 1 ⊢ e′, 𝛾 2, 𝑥 ↦→ 𝑣 2 ⊢ e′ ) ∈ E(Δ                                   ′
                                                                                                                     ′+𝑑 ′′𝑥)·Σ′′ J(Δ +

𝑑 ′′𝑥)(𝜏2 )K.
By induction hypothesis on Γ, 𝑥 : 𝜏1 ; Δ+𝑑 ′𝑥 ⊢ e′ : 𝜏2 ; Σ′′, and choosing Σ 𝜒 = Δ ′ +𝑑 ′′𝑥 ⊑ Δ ′ +𝑑 ′𝑥, we
                                          𝑗                                                       𝑗
know that ∀𝛾 1′ , 𝛾 2′, (𝛾 1′, 𝛾 2′ ) ∈ G(Δ                                 ′    ′ ′       ′                          ′      ′′
                                            ′ +𝑑 ′′𝑥) JΓ, 𝑥 : 𝜏 1 K then (𝛾 1 ⊢ e , 𝛾 2 ⊢ e ) ∈ E (Δ′+𝑑 ′′𝑥)·Σ′′ J(Δ + 𝑑 𝑥)(𝜏 2 )K.

As (𝛾 1, 𝛾 2 ) ∈ GΔ𝑗 ′ JΓK (by Lemma C.11), (𝑣 1, 𝑣 2 ) ∈ V𝑑𝑗′′ JΔ ′(𝜏1 )K, and Δ ′(𝜏1 ) = (Δ ′ + 𝑑 ′′𝑥)(𝜏1 ) (as 𝑥 is
                                                                              𝑗
not free in 𝜏1 ), it is easy to see that (𝛾 1, 𝑥 ↦→ 𝑣 1 , 𝛾 2, 𝑥 ↦→ 𝑣 2 ) ∈ G(Δ ′ +𝑑 ′′𝑥) JΓ, 𝑥 : 𝜏 1 K. Finally, the result
                            ′                      ′
follows by choosing 𝛾 1 = 𝛾 1, 𝑥 ↦→ 𝑣 1 , and 𝛾 2 = 𝛾 2, 𝑥 ↦→ 𝑣 2 .                                                        ⊳
Let us prove now Part (2).
Case (1) Γ; Δ ⊢ e1 e2 : [Σ2/𝑥]𝜏2 ; ⌉Σ1 ⌈∞ + [Σ2/𝑥]Σ′′
Subproof. We have to prove that
∀𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, for Δ ′ ⊑ Δ, then (𝛾 1 ⊢ e1 e2, 𝛾 2 ⊢ e1 e2 ) ∈ E 𝑘Δ′ Σ JΔ ′ ([Σ2/𝑥]𝜏2 )K.
                                                                                                  •

By induction hypotheses we know that
                               Σ′′                                                                      Σ′′
Γ; Δ ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑑 ′) −−→
                             → 𝜏2 ; Σ1 ⇒ (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ ((𝑥 : 𝜏1 ·𝑑 ′ ) −−→
                                                                                                    → 𝜏2 )K and
                                                        𝑘−𝑗
Γ; Δ ⊢ 𝑒 2 : 𝜏1 ; Σ2 ⇒ (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E Δ′ ·Σ12 JΔ ′ (𝜏1 )K.
                         Σ′′                              Δ′•Σ′′
As Δ ′((𝑥 : 𝜏1 ·𝑑 ′ ) −−→
                        → 𝜏2 ) = (𝑥 : Δ ′ (𝜏1 )·𝑑 ′) −−−−→
                                                         → Δ ′(𝜏2 ), by unfolding (𝛾 1 ⊢ 𝑒 1 , 𝛾 2 ⊢ 𝑒 1 ) ∈ E Δ𝑘 ′ ·Σ1 J(𝑥 :
               Δ′ •Σ′′                                                               p                                            p
Δ ′(𝜏1 )·𝑑 ′ ) −−−−→
                   → Δ ′(𝜏2 )K, we know that if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 h𝜆 (𝑥 : 𝜏1 ). e1′ , 𝛾 1′ i then 𝛾 2 ⊢ 𝑒 1 ⇓∗ h𝜆 (𝑥 :
       ′    ′
𝜏1 ). e2, 𝛾 2 i and
                                                                                         Δ′•Σ′′
(h𝜆 (𝑥 : 𝜏1 ). e1′ , 𝛾 1′ i, h𝜆 (𝑥 : 𝜏1 ). e2′ , 𝛾 2′ i) ∈ VΔ𝑘−𝑗
     p                         p                                          ′        ′ −−−
                                                                  1
                                                              ′ ·Σ J(𝑥 : Δ (𝜏 1 )·𝑑 ) −
                                                                  1
                                                                                        → Δ ′(𝜏2 )K (for 𝑑 ′′ >= 𝑑 ′) (1).
                                                                                        →
Also, by unfolding (𝛾 1 ⊢ 𝑒 2 , 𝛾 2 ⊢ 𝑒 2 ) ∈ E 𝑘−𝑗      ′                       𝑗2                   ∗
                                                Δ′ ·Σ2 JΔ (𝜏 1 )K, if 𝛾 1 ⊢ 𝑒 2 ⇓ 𝑣 1 then 𝛾 2 ⊢ 𝑒 2 ⇓ 𝑣 2 and (𝑣 1 , 𝑣 2 ) ∈
                                                     1

           1 −𝑗 2
VΔ𝑘−𝑗  ′ ·Σ
            2
                  JΔ ′ (𝜏1 )K.
By p-app we know that Δ·Σ2 ≤ 𝑑 ′ , as Δ ′ ⊑ Δ then Δ ′ ·Σ2 ≤ 𝑑 ′. Then we instantiate (1) with
𝑑 ′′ = Δ ′ ·Σ2 , then for some 𝑗 3 < 𝑘 − 𝑗 1 − 𝑗 2
                                                       𝑗3
(𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ e1′ , 𝛾 2′ [𝑥 ↦→ 𝑣 2 ] ⊢ e2′ ) ∈ E ⌉Δ                                 ′        ′
                                                          ′ ·Σ ⌈∞ +(Δ′ +(Δ′ ·Σ )𝑥) Σ′′ J(Δ ·Σ 2𝑥)(Δ (𝜏 2 ))K (2).
                                                              1               2  •

Suppose Δ ⌉Σ1 ⌈ = 0 (otherwise the result follows immediately). Then Δ ′•Σ = Δ ′•([Σ2/𝑥]Σ′′).
                    ′•        ∞

Also as Δ ′ ⊑ Δ, and 𝑥 ∉ 𝑑𝑜𝑚(Δ), then by Lemma 7.4, Δ ′•([Σ2/𝑥]Σ′′ = ((Δ ′ ·Σ2 )𝑥)•(Δ ′•Σ′′ ) =
(Δ ′ + (Δ ′ ·Σ2 )𝑥)•Σ′′ . By Lemma 7.5, [Δ ′ ·Σ2 /𝑥]Δ ′(𝜏2 ) = Δ ′ ([Σ2/𝑥]𝜏2 ), then by (1) and weakening
(Lemma C.10) (𝛾 1′ [𝑥 ↦→ 𝑣 1 ] ⊢ e1′ , 𝛾 2′ [𝑥 ↦→ 𝑣 2 ] ⊢ e2′ ) ∈ E Δ𝑗3′ Σ JΔ ′ ([Σ2/𝑥]𝜏2 )K (3). The result follows by
                                                                             •

Lemma C.15.
                                                                                                                      ⊳
Case (2) Γ ; Δ ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } : [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 ; ⌉Σ1 ⌈∞ ⊔ [Σ11/𝑥]Σ2 ⊔
[Σ12/𝑥]Σ3
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, for Δ ′ ⊑ Δ
(𝛾 1 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 }, 𝛾 2 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 }) ∈ E 𝑘Δ′ ·Σ JΔ ′ (𝜏)K.
By induction hypothesis on Γ ; Δ ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1 , we know that
(𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏11 Σ11 ⊕ Σ12 𝜏12 )K, i.e. if 𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗1 𝑣 11 , then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑣 12 and (𝑣 11 , 𝑣 12 ) ∈

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                  89

   𝑘−𝑗               ′        ′
VΔ′ ·Σ11 JΔ ′(𝜏11 ) Δ ·Σ11 ⊕ Δ ·Σ12 Δ ′(𝜏12 )K. Notice that Δ ′ •Σ = Δ ′•⌉Σ1 ⌈∞ ⊔ Δ ′•([Σ11/𝑥]Σ2 ) ⊔ Δ ′•([Σ12/𝑥]Σ3 ).
If Δ ′•⌉Σ1 ⌈∞ = ∞ then the result is trivial and holds immediately. Let us suppose that Δ ′ •⌉Σ1 ⌈∞ = 0,
then this means that Δ ′ ·Σ1 = 0, i.e. either 𝑣 11 = inl 𝑣 11              ′ and 𝑣                ′
                                                                                     12 = inl 𝑣 12 , or 𝑣 11 = inr 𝑣 11 and
                                                                                                                             ′
                ′
𝑣 12 = inr 𝑣 12 .
                                                  ′             ′                                       ′             ′
Let us suppose that (𝑣 11 , 𝑣 12 ) = (inl 𝑣 11       , inl 𝑣 12   ) (the case (𝑣 11, 𝑣 12 ) = (inr 𝑣 11     , inr 𝑣 12  ) is analo-
                                ′         ′           ′                          ′    ′         𝑘−𝑗1            ′
gous). By Lemma C.1 Δ ·Σ1 + Δ ·Σ11 = Δ ·(Σ1 + Σ11 ), then (𝑣 11 , 𝑣 12 ) ∈ VΔ′ ·(Σ1 +Σ11 ) JΔ (𝜏11 )K.
Also, by induction hypothesis on Γ, 𝑥 : 𝜏11 ; Δ + (Δ·(Σ1 + Σ11 ))𝑥 ⊢ e2 : 𝜏2 ; Σ2 , by choosing
Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥 ⊑ Δ + (Δ·(Σ1 + Σ11 ))𝑥, (𝛾 1 [𝑥 ↦→ 𝑣 12       ′ ], 𝛾 [𝑥 ↦→ 𝑣 ′ ]) ∈ G𝑘−𝑗1                     JΓ, 𝑥 : 𝜏11 K
                                                                               2        22        Δ′ +(Δ′ ·(Σ1 +Σ11 ))𝑥
(note that 𝑥 ∉ 𝑑𝑜𝑚(Σ1) ∪ 𝑑𝑜𝑚(Σ11), therefore (Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥)(𝜏11 ) = Δ ′(𝜏11 )) we know that
              ′ ] ⊢ e , 𝛾 [𝑥 ↦→ 𝑣 ′ ] ⊢ e ) ∈ E 𝑘−𝑗1
(𝛾 1 [𝑥 ↦→ 𝑣 12                                                               J(Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥)(𝜏2 )K.
                      2 2           22       2      (Δ′+(Δ′ ·(Σ1 +Σ11 ))𝑥) Σ2
                                                                          •

But Δ ′ ·Σ1 = 0, therefore (Δ ′ + (Δ ′ ·(Σ1 + Σ11 ))𝑥)•Σ2 = (Δ ′ + (Δ ′ ·Σ11 )𝑥)•Σ2 , and Δ ′ ·(Σ1 + Σ11 ) = Δ ′ ·Σ11 ,
and by Lemma C.2 and because Δ ′ ·Σ11 ∈ sens, then (Δ ′ + (Δ ′ ·Σ11 )𝑥)(𝜏2 ) = (Δ ′ ·Σ11 )𝑥(Δ ′(𝜏2 )), and by
Lemma 7.5 (Δ ′ ·Σ11 )𝑥(Δ ′(𝜏2 )) = Δ ′([Σ11/𝑥]𝜏2 ).
Then by weakening lemma C.10 we know that
              ′ ] ⊢ e , 𝛾 [𝑥 ↦→ 𝑣 ′ ] ⊢ e ) ∈ E 𝑘−𝑗1
(𝛾 1 [𝑥 ↦→ 𝑣 12                                                           JΔ ′ ([Σ11/𝑥]𝜏2)K. Notice that by Lemma C.8,
                       2 2           22        2      (Δ′+(Δ′ ·Σ11 )𝑥) Σ2
                                                                      •

Σ2 <: Σ2 ⊔Σ3 , and then by Lemma C.13 (Δ +(Δ ·Σ11 )𝑥)•Σ2 <: (Δ ′ +(Δ ′ ·Σ11 )𝑥)•Σ2 ⊔(Δ ′ +(Δ ′·Σ12 )𝑥)•Σ3 .
                                                       ′      ′

Also by Lemma C.9 [Σ11/𝑥]𝜏2 <: [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 , therefore by Lemma C.6, Δ ′([Σ11/𝑥]𝜏2 ) <:
Δ ′([Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 ). Once again by Lemma C.10, (𝛾 1 [𝑥 ↦→ 𝑣 12                      ′ ] ⊢ e , 𝛾 [𝑥 ↦→ 𝑣 ′ ] ⊢ e ) ∈
                                                                                                   2 2                22       2
   𝑘−𝑗1    ′
E Δ′ Σ JΔ (𝜏)K (3). The result follows by Lemma C.15.
    •

                                                                                                                                   ⊳
                                 𝑥 ]𝜏 ; FP∞ (Û
Case (3) Γ ; Δ ⊢ return 𝑒 1 : [∅/Û           𝑥 ), where 𝑥Û = FV(𝑒 1 ) ∪ dom(Σ1 )
Subproof. We use notation FP∞ (𝑒 1 ) to stand for FP∞ (Û              𝑥 ). We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈
GΔ𝑘 ′ JΓK and Δ ′ ⊑ Δ, (𝛾 1 ⊢ return 𝑒 1, 𝛾 2 ⊢ return 𝑒 1 ) ∈ E 𝑘Δ′ (⌉Σ1 ⌈∞ +FP∞ (𝑒1 )) JΔ ′ ([∅/Û
                                                                              •
                                                                                                   𝑥 ]𝜏)K.
Note that Δ ′•FP∞ (Û     𝑥 ) is eitherÍ∞ or 0. If Δ ′•FP∞ (Û 𝑥 ) = ∞ then the result is direct by Lemma C.14. Let
us assume that Δ ′•FP∞ (Û        𝑥 ) = 𝑝 ∈𝑐𝑜𝑑(FP∞ (Û𝑥 )) 𝑝 = (0, 0).
By induction hypothesis on Γ; Δ ⊢ 𝑒 1 : 𝜏 ; Σ1 , we know that (𝛾 1 ⊢ 𝑒 1, 𝛾 2 ⊢ 𝑒 1 ) ∈ E Δ′ ·Σ1 JΔ ′ (𝜏)K, i.e. if
𝛾 1 ⊢ 𝑒 1 ⇓ 𝑗 𝑣 1 , then 𝛾 2 ⊢ 𝑒 1 ⇓∗ 𝑣 2 and (𝑣 1, 𝑣 2 ) ∈ VΔ𝑘−𝑗      ′
                                                               ′ ·Σ JΔ (𝜏)K. Notice that ⌉Σ 1 ⌈
                                                                   1
                                                                                                ∞ = 0 and FP∞ (𝑒 ) = 0,
                                                                                                                 1
then FV(𝑒) = ∅.ßThis means that by Lemma C.16 𝑣 1 = 𝑣ß2 .
                       1       when        𝑥 = 𝑣1                          1    when      𝑥 = 𝑣2
Let 𝐷 1 = 𝜆𝑥 .                                      and 𝐷 2 = 𝜆𝑥 .                                . We have to prove
                       0 otherwise                                         0 otherwise
that 𝐷 1 (𝑆) ≤ 𝐷 2 (𝑆). If 𝑣 1 ∉ 𝑆 then the result is trivial as 𝐷 1 (𝑆) = 0 and 0 ≤ 𝐷 2 (𝑆) . Let us suppose
that 𝑣 1 ∈ 𝑆, then as 𝑣 1 = 𝑣 2 , we also know that 𝑣 2 ∈ 𝑆, thus 𝐷 1 (𝑆) = 1, and 𝐷 2 (𝑆) = 1, so the result
holds.
                                                                                                                         ⊳
Case (4) Γ ; Δ ⊢ 𝑥 : 𝜏1 ←e1 ; e2 : [∅/𝑥]𝜏2 ; Σ1 + Σ2
Subproof. We have to prove that for any 𝑘, ∀(𝛾 1, 𝛾 2 ) ∈ GΔ𝑘 ′ JΓK, for Δ ′ ⊑ Δ it holds that
(𝛾 1 ⊢ 𝑥 : 𝜏1 ←e1 ; e2, 𝛾 2 ⊢ 𝑥 : 𝜏1 ←e1 ; e2 ) ∈ E 𝑘Δ′ ·(Σ1 +[∅/𝑥]Σ2 ) JΔ ′ ([∅/𝑥]𝜏2)K.
By induction hypothesis on Γ ; Δ ⊢ e1 : 𝜏1 ; Σ1 , we know that
                                                                                                                        ′
(𝛾 1 ⊢ e1, 𝛾 2 ⊢ e1 ) ∈ E 𝑘Δ′ ·Σ1 JΔ ′ (𝜏1 )K, i.e. let (𝜖1 , 𝛿 1 ) = Δ ′ ·Σ1 , ∀𝑆 ⊆ 𝑣𝑎𝑙(∗), for 𝑘 ′ < 𝑘, if 𝛾 1 ⊢ e1 ⇓𝑘 𝐷 1
then 𝛾 2 ⊢ e1 ⇓∗ 𝐷 2 , and 𝐷 1 (𝑆) ≤ 𝑒 𝜖1 𝐷 2 (𝑆) + 𝛿 1 (notice 𝑘 ′ > 0).
                                                                                     ′ ,𝛾′ ) ∈ G        𝑗             𝑘−𝑘 ′
Similarly, by induction hypothesis on Γ, 𝑥 : 𝜏1 ; Δ + 0𝑥 ⊢ e2 : 𝜏2 ; Σ2 , for all (𝛾 1𝑗  2𝑗        Δ′ +0𝑥 JΓ, 𝑥 :
                                                                                                 ′
𝜏1 K, for some 𝑘 ′′       ′      ′                                  ′          ′             𝑘−𝑘
                 𝑗 < 𝑘 − 𝑘 and Δ + 0𝑥 ⊑ Δ + 0𝑥, we know that (𝛾 1𝑗 ⊢ e2, 𝛾 2𝑗 ⊢ e2 ) ∈ E (Δ′+0𝑥) Σ2 J(Δ +
                                                                                                             ′
                                                                                                                        •


0𝑥)(𝜏2 )K. Let 𝑘 = max(𝑘 𝑗 ). Notice that by Lemma 7.4, (Δ + 0𝑥)·Σ2 = Δ ·([∅/𝑥]Σ2) as 𝑥 ∉ 𝑑𝑜𝑚(Δ ′),
                ′′        ′′                               ′                 ′



                                    ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
90                   Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


and that by Lemma 7.3, (Δ ′ + 0𝑥)(𝜏2 ) = Δ ′ ([∅/𝑥]𝜏2). Then let (𝜖2, 𝛿 2 ) = Δ ′ ·[∅/𝑥]Σ2, ∀𝑆 ′ ∈ 𝑣𝑎𝑙, if
  ′ ⊢ e ⇓𝑘 ′′ 𝐷 ′ then 𝛾 ′ ⊢ e ⇓∗ 𝐷 ′ , and 𝐷 ′ (𝑆) ≤ 𝑒 𝜖 2 𝐷 ′ (𝑆) + 𝛿 .
𝛾 1𝑗   2       1𝑗        2𝑗   2       2        1𝑗                2𝑗       2
                                                                                    Í
Let 𝑑𝑣𝑎𝑙 = {𝑣 | 𝐷 1 (𝑣) > 0} ∪ {𝑣 | 𝐷 2 (𝑣) > 0} ⊆ 𝑣𝑎𝑙(𝜏1 /Γ). Let 𝐷𝑖′′ = 𝜆𝑥 . 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷𝑖 (𝑣 𝑗 ) × 𝐷𝑖′𝑗 (𝑥). We
have to prove then that ∀𝑆 ′ ∈ 𝑣𝑎𝑙(∗), let (𝜖1 + 𝜖2 , 𝛿 1 + 𝛿 2 ) = Δ ′ ·Σ1 + Δ ′ ·[∅/𝑥]Σ2 = Δ ′ ·(Σ1 + [∅/𝑥]Σ2)


                                     Í         𝐷 1′′𝑆 ′ ≤ 𝑒 𝜖1 +𝜖2 (𝐷   ′′ ′
                                                                       Í2 𝑆 ) + 𝛿′′1 + 𝛿 2
                                                ′′           𝜖   +𝜖
                                      𝑣1 ∈𝑆 ′ 𝐷 1 (𝑣 1 ) ≤ 𝑒          ( 𝑣2 ∈𝑆 ′ 𝐷 2 (𝑣 2 )) + 𝛿 1 + 𝛿 2
                                                               1    2
           Í        Í                          ′             𝜖 1 +𝜖 2 (Í        Í                          ′
             𝑣1 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × 𝐷 1𝑗 (𝑣 1 ) ≤ 𝑒             𝑣2 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 2 (𝑣 𝑗 ) × 𝐷 2𝑗 (𝑣 2 )) + 𝛿 1 + 𝛿 2

                                                                                 ′
As 𝑘 − 𝑘 ′ < 𝑘, by induction hypothesis (𝑣 𝑗 , 𝑣 𝑗 ) ∈ V0𝑘−𝑘 J𝜏1 /ΓK (notice that 𝑘 ′ > 0 as values are
not privacy expressions), but 𝜏1 /Γ = Δ∅ (𝜏1 ), and by weakening lemmas C.11, and C.10 (𝛾 1, 𝛾 2 ) ∈
       ′                                 ′ , 𝛾 ′ ) = (𝛾 [𝑥 ↦→ 𝑣 ], 𝛾 [𝑥 ↦→ 𝑣 ]) and know that that, for all 𝑗 ,
G𝑘−𝑘 JΓK, then we can choose (𝛾 1𝑗
ÍΔ′         ′            𝜖2 Í       ′
                                               2𝑗           1       𝑗    2
                                                                           Í           𝑗
                                                                                        ′
         ′ 𝐷 (𝑣 1 ) ≤ 𝑒 ( 𝑣 ∈𝑆 ′ 𝐷 (𝑣 2 )) + 𝛿 2 . Also notice that                 ′ 𝐷 (𝑣 1 ) is a probability therefore
Í 𝑣 1 ∈𝑆    1𝑗
            ′                 𝜖
                               2  Í 2𝑗
                                          ′                            𝜖   Í 𝑣 1 ∈𝑆    1𝑗
                                                                                          ′
  𝑣1 ∈𝑆 ′ 𝐷 1𝑗 (𝑣 1 ) ≤ 𝑚𝑖𝑛(𝑒 ( 𝑣2 ∈𝑆 ′ 𝐷 2𝑗 (𝑣 2 )) + 𝛿 2 , 1) ≤ 𝑚𝑖𝑛(𝑒 ( 𝑣2 ∈𝑆 ′ 𝐷 2𝑗 (𝑣 2 )), 1) + 𝛿 2 . Then
                                2                                        2


                     Í        Í                           ′
                       𝑣1 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × 𝐷 1𝑗 (𝑣 1 )
                     Í                         Í            ′ (𝑣 ))
                   = 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × ( 𝑣1 ∈𝑆 ′ 𝐷 1𝑗     1
                     Í                                    Í          ′ (𝑣 )), 1) + 𝛿 )
                   ≤ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × (𝑚𝑖𝑛(𝑒 𝜖2 ( 𝑣2 ∈𝑆 ′ 𝐷 2𝑗    2           2
                      Í                               𝜖   Í          ′ (𝑣 )), 1)) + (Í
                   = ( 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × 𝑚𝑖𝑛(𝑒 ( 𝑣2 ∈𝑆 ′ 𝐷 2𝑗
                                                        2
                                                                         2             𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × 𝛿 2 )
                     Í                                    Í         ′ (𝑣 )), 1) + 𝛿
                   ≤ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) × 𝑚𝑖𝑛(𝑒 𝜖2 ( 𝑣2 ∈𝑆 ′ 𝐷 2𝑗    2           2

                                       Í                       Í
Let 𝑆 = 𝑑𝑣𝑎𝑙, then we know that 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 1 (𝑣 𝑗 ) ≤ 𝑒 𝜖1 ( 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝐷 2 (𝑣 𝑗 )) + 𝛿 1 .
Let 𝜇 𝑣 = (𝐷 1 (𝑣) − 𝑒 𝜖1 𝐷 2 (𝑣))+ (notice that 𝜇 𝑣 is not necessarily a measure) and 𝑇1 = {𝑣 ∈ 𝑑𝑣𝑎𝑙 |
𝐷 1 (𝑣) − 𝑒 𝜖1 𝐷 2 (𝑣) > 0}, then:

                                                    Í
                                                    Í𝑣 ∈𝑑 𝑣𝑎𝑙 𝜇 𝑣
                                                  = Í𝑣 ∈𝑑 𝑣𝑎𝑙 (𝐷 1 (𝑣) − 𝑒 𝜖1 𝐷 2 (𝑣))+
                                                  = 𝑣 ∈𝑇1 𝐷 1 (𝑣) − 𝑒 𝜖1 𝐷 2 (𝑣)
                                                  ≤ 𝛿 1 (By def. of (𝜖1, 𝛿 1 )-dp)

Finally,

             Í                                     Í           ′ (𝑣 )), 1) + 𝛿
                         𝐷 (𝑣 ) × 𝑚𝑖𝑛(𝑒 𝜖2 ( 𝑣1 ∈𝑆 ′ 𝐷 2𝑗
             Í𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝜖11 𝑗                           𝜖   Í 1 ′                2
           = 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 (𝑒 𝐷 2 (𝑣) + 𝜇 𝑣 ) × 𝑚𝑖𝑛(𝑒 ( 𝑣1 ∈𝑆 ′ 𝐷 2𝑗 (𝑣 1 )), 1) + 𝛿 2
                                                           2
             Í                                 Í           ′ (𝑣 ) + 𝑚𝑖𝑛(𝑒 𝜖 2 (Í               ′ (𝑣 )), 1)𝜇 ) + 𝛿
           ≤ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 (𝑒 𝜖1 𝐷 2 (𝑣) × 𝑒 𝜖2 𝑣1 ∈𝑆 ′ 𝐷 2𝑗        1                   𝑣1 ∈𝑆 ′ 𝐷 2𝑗  1        𝑣        2
             Í         Í            𝜖 1 +𝜖 2             ′            Í                     𝜖2 Í          ′
           = 𝑣1 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝑒            𝐷 2 (𝑣) × 𝐷 2𝑗 (𝑣 1 ) + ( 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝑚𝑖𝑛(𝑒 ( 𝑣1 ∈𝑆 ′ 𝐷 2𝑗       (𝑣 1 )), 1)𝜇 𝑣 + 𝛿 2
                       Í       Í                           ′ (𝑣 )) + (Í
           ≤ 𝑒 𝜖1 +𝜖2 ( 𝑣1 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 (𝐷 2 (𝑣) × 𝐷 2𝑗       1         𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 𝜇 𝑣 ) + 𝛿 2
                       Í       Í
           ≤ 𝑒 𝜖1 +𝜖2 ( 𝑣1 ∈𝑆 ′ 𝑣 𝑗 ∈𝑑 𝑣𝑎𝑙 (𝐷 2 (𝑣) × 𝐷 2𝑗 ′ (𝑣 )) + 𝛿 + 𝛿
                                                                 1      1       2


and the result holds.                                                                                                               ⊳
                                                                                                                                    

                                                                                                                               𝑠𝑥
    Theorem C.18 (Sensitivity Type Soundness at Base Types). If ∅; ∅ ⊢ 𝑒 : (𝑥 : R·∞) −−→ R ; ∅,
|𝑟 1 − 𝑟 2 | ≤ 𝑠 ′ , ∅ ⊢ 𝑒 𝑟 1 ⇓ 𝑟 1′ , ∅ ⊢ 𝑒 𝑟 2 ⇓ 𝑟 2′ , then |𝑟 1′ − 𝑟 2′ | ≤ 𝑠𝑠 ′

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                              91

                                                             𝑠𝑥
  Proof. We know that ∅ ⊢ 𝑒 : (𝑥 : R·∞) −−→ R ; ∅ therefore by the Fundamental Property
                                                                                                   𝑠𝑥
(Theorem C.17), using 𝛾 1 = ∅ and 𝛾 2 = ∅, then (∅ ⊢ 𝑒, ∅ ⊢ 𝑒) ∈ E0𝑘 J(𝑥 : R·∞) −−→ RK, i.e. if
                                                                                𝑠𝑥
∅ ⊢ 𝑒 ⇓ 𝑗1 h𝜆𝑥 . 𝑒 ′, 𝛾i then (h𝜆𝑥 . 𝑒 ′, 𝛾i, h𝜆𝑥 . 𝑒 ′, 𝛾i) ∈ V0𝑘−𝑗1 J(𝑥 : R) −−→ RK, for some 𝑘 > 𝑗 1 .
                                 ′                           ′
  We know that ∅ ⊢ 𝑒 𝑟 1 ⇓𝑘 𝑟 1 ′, and ∅ ⊢ 𝑒 𝑟 2 ⇓𝑘 𝑟 2 ′ , for some 𝑘 ′ = 𝑗 1 + 𝑗 2 , and 𝑘 > 𝑗 1 + 𝑗 2 , i.e.
                                  app
                                  ∅ ⊢ 𝑒 ⇓ 𝑗1 h𝜆𝑥 . 𝑒 ′, 𝛾i        𝛾[𝑥 ↦→ 𝑟 𝑖 ] ⊢ 𝑒 ′ ⇓ 𝑗2 𝑟 𝑖′
                                                                    ′
                                                      ∅ ⊢ 𝑒 𝑟 𝑖 ⇓𝑘 𝑟 𝑖′
for some 𝛾 and Γ such that Γ, 𝑥 : R ⊢ 𝑒 ′ : R; 𝑠𝑥, and (𝛾, 𝛾) ∈ G∅𝑘−𝑗1 −1 JΓK. As |𝑟 1 − 𝑟 2 | ≤ 𝑠 ′ ,
                              1 −1
                                                                                                                    𝑠𝑥
then (𝑟 1, 𝑟 2 ) ∈ V𝑠𝑘−𝑗   ′       JRK. We instantiate (h𝜆𝑥 . 𝑒 ′, 𝛾i, h𝜆𝑥 . 𝑒 ′, 𝛾i) ∈ V0𝑘−𝑗1 J(𝑥 : R·∞) −−→ RK with
                       1 −1                                                                          𝑘−𝑗1 −1
(𝑟 1, 𝑟 2 ) ∈ V𝑠𝑘−𝑗
                  ′         JRK to know that (𝛾[𝑥 ↦→ 𝑟 1 ] ⊢ 𝑒 ′, 𝛾[𝑥 ↦→ 𝑟 2 ] ⊢ 𝑒 ′ ) ∈ E0+0+𝑠𝑠           ′ JRK, i.e. if 𝛾[𝑥 ↦→
                                                    1 −𝑗 2 −1
𝑟 𝑖 ] ⊢ 𝑒 ′ ⇓ 𝑗2 𝑟 𝑖′ then (𝑟 1 ′, 𝑟 2 ′ ) ∈ V𝑠𝑠𝑘−𝑗
                                                 ′            JRK, meaning that |𝑟 1
                                                                                     ′ − 𝑟 ′ | ≤ 𝑠𝑠 ′ , which is exactly what
                                                                                          2
we want to prove and the result holds immediately.                                                                             
                                                                                                        (𝜖,𝛿)𝑥
    Theorem 7.8 (Privacy Type Soundness at Base Types). If ∅ ⊢ 𝑒 : (𝑥 : R·1) −−−−→
                                                                                 → R ; ∅,
|𝑟 1 − 𝑟 2 | ≤ 1, ∀𝑟 , Pr[∅ ⊢ e 𝑟 1 ⇓∞ 𝑟 ] ≤ 𝑒 𝜖 Pr[∅ ⊢ e 𝑟 2 ⇓∞ 𝑟 ] + 𝛿
  Proof. We proceed analogously to Theorem C.18. But unfolding the deﬁnition of related com-
putations, and using a 𝑘 big enough so both probabilities are deﬁned (and using the fact that two
real numbers are semantically equivalent for any index).                                        

D 𝜆J : TYPE SAFETY
In this section we present auxiliary deﬁnitions used in Section 7.2, and the proof of type safety.
   Non-deterministic sampling big-step semantics of privacy expressions are presented in Fig-
ure 31. We write 𝑒 ⇓ 𝑣, when 𝑒 ⇓𝑘 𝑣 for some 𝑘. This semantics is coherent with respect to
the distribution semantics of Figure 28, in the following sense:
  Lemma D.1 (Coherence of non-deterministic semantics wrt distribution semantics). If
∃𝑘.𝛾 ⊢ e ⇓𝑘 𝐷 ∧ 𝐷(𝑣) > 0 then 𝛾 ⊢ e ⇓ 𝑣.
  Proof. We present a proof sketch for this lemma, illustrating some relevant cases. We proceed
by case analysis and induction in 𝑘 and the structure of e.
Case (1) e = return 𝑒
Subproof. We know that
                                                      return
                                                        𝛾 ⊢ 𝑒 ⇓𝑘 𝑣 ′
                                                     return 𝑒 ⇓𝑘 𝐷
where
                                                   ß
                                                    1          when    𝑥 = 𝑣′
                                          𝐷 = 𝜆𝑥 .
                                                    0        otherwise

Let 𝑣 such that 𝐷(𝑣) > 0; this means that 𝑣 = 𝑣 ′ , and 𝛾 ⊢ 𝑒 ⇓ 𝑣, Then
                                                       return
                                                         𝛾 ⊢𝑒 ⇓𝑣
                                                      return 𝑒 ⇓ 𝑣
and the result holds.                                                                                                         ⊳
Case (2) e = 𝑥 : 𝜏1 ← e1 ; e2

                                   ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
92                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Subproof. We know that
                           bind
                                     ′
                           𝛾 ⊢ e1 ⇓𝑘 𝐷 1         ∀𝑣 𝑖 ∈ Sup(𝐷 1 ), 𝛾[𝑥 ↦→ 𝑣 𝑖 ] ⊢ e2 ⇓𝑘𝑖 𝐷 2𝑖
                                                                    ′
                                          𝛾 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 ⇓𝑘 +max𝑖 𝑘𝑖 𝐷
                    Í
where 𝐷 = 𝜆𝑥 . 𝑣𝑖 ∈Sup(𝐷 1 ) 𝐷 1 (𝑣 𝑖 )·𝐷 2𝑖 (𝑥).
Let 𝑣 such that 𝐷(𝑣) > 0, then it must be the case that for some 𝑣 𝑗 ∈ Sup(𝐷 1 ), 𝐷 1 (𝑣 𝑗 )·𝐷 2𝑗 (𝑣) > 0,
i.e. 𝐷 1 (𝑣 𝑗 ) > 0 and 𝐷 2𝑗 (𝑣) > 0. By induction hypothesis in 𝑘 ′ < 𝑘 (note that every probabilistic
expression takes at least one step of reduction), as 𝐷 1 (𝑣 𝑗 ) > 0, we know that 𝛾 ⊢ e1 ⇓ 𝑣 𝑗 . Also as
𝛾[𝑥 ↦→ 𝑣 𝑗 ] ⊢ e2 ⇓𝑘 𝑗 𝐷 2𝑗 , then by induction hypothesis in 𝑘𝑖 < 𝑘, as 𝐷 2𝑗 (𝑣) > 0, we know that
𝛾[𝑥 ↦→ 𝑣 𝑗 ] ⊢ e2 ⇓ 𝑣, thus
                                         case-left
                                         𝛾 ⊢ e1 ⇓ 𝑣 1     𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣
                                               𝛾 ⊢ 𝑥 : 𝜏 1 ← e1 ; e2 ⇓ 𝑣
and the result holds.                                                                                                   ⊳
Case (3) e = case e1 of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 }
Subproof. We know that
                                  case-left
                                  𝛾 ⊢ 𝑒 1 ⇓𝑘1 inl 𝑣 1        𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓𝑘2 𝐷
                                  𝛾 ⊢ case e of {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓𝑘1 +𝑘2 𝐷


Let 𝑣 such that 𝐷(𝑣) > 0. By induction hypothesis in e2 on 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓𝑘2 𝐷, then we know
that 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣, thus
                                     case-left
                                    𝛾 ⊢ 𝑒 1 ⇓ inl 𝑣 1        𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣
                                      𝛾 ⊢ case e1 {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓ 𝑣
and the result holds.                                                                                                   ⊳
                                                                                                                       

   Thus, type safety of the non-deterministic semantics implies type safety for the distribution
semantics.8
   The type safety logical relation is deﬁned in Figure 32. Its deﬁnition is straightforward, split
into a value relation V, a computation relation E, and an environment relation G. As usual, the
fundamental property of the type safety logical relation states that well-typed open terms are in
the relation closed by an adequate environment 𝛾:9
     Proposition D.1 (Fundamental Property of the Type Safety Logical Relation).
     (a) Let Γ; Σ0 ⊢ 𝑒 : 𝜏; Σ, and 𝛾 ∈ GJΓK. Then 𝛾 ⊢ 𝑒 ∈ EJ𝜏/ΓK.
     (b) Let Γ; Σ0 ⊢ e : 𝜏; Σ, and 𝛾 ∈ GJΓK. Then 𝛾 ⊢ e ∈ EJ𝜏/ΓK.

8 The other direction 𝛾 ⊢ e ⇓ 𝑣  =⇒ ∃𝑘.𝛾 ⊢ e ⇓𝑘 𝐷 ∧ 𝐷 (𝑣) > 0 would establish soundness of the non-deterministic seman-
tics; given that the language does not feature recursion, we believe that it holds, although this is left for future work.
9 We use the following operators to remove variables from a type:

𝜏/Γ = [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏, ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ) and 𝜏/𝛾 = [∅/𝑥 1, ..., ∅/𝑥𝑛 ]𝜏, ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(𝛾).


ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                                      93



           return                         bind                                                              gauss
            𝛾 ⊢𝑒 ⇓𝑣                       𝛾 ⊢ e1 ⇓ 𝑣 1                𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣 2                         𝑟∈R
          return 𝑒 ⇓ 𝑣                                  𝛾 ⊢ 𝑥 : 𝜏 1 ← e1 ; e2 ⇓ 𝑣 2                         𝛾 ⊢ gauss 𝜇 𝜎 2 ⇓ 𝑟

              if-true                                                              if-false
                  𝛾 ⊢ 𝑒 1 ⇓ true          𝛾 ⊢ e2 ⇓ 𝑣 2                                𝛾 ⊢ 𝑒 1 ⇓ false         𝛾 ⊢ e3 ⇓ 𝑣 3
             𝛾 ⊢ if 𝑒 1 then {e2 } else {e3 } ⇓ 𝑣 2                               𝛾 ⊢ if 𝑒 1 then {e2 } else {e3 } ⇓ 𝑣 3

            case-left                                                             case-right
            𝛾 ⊢ e ⇓ inl 𝑣            𝛾[𝑥 ↦→ 𝑣] ⊢ e2 ⇓ 𝑣 2                         𝛾 ⊢ e ⇓ inr 𝑣            𝛾[𝑥 ↦→ 𝑣] ⊢ e3 ⇓ 𝑣 3
             𝛾 ⊢ case e {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓ 𝑣 2                                 𝛾 ⊢ case e {𝑥 ⇒ e2 } {𝑥 ⇒ e3 } ⇓ 𝑣 3

                             app
                             𝛾 ⊢ e1 ⇓ h𝜆𝑥 : 𝜏·𝑠. e′, 𝛾 ′ i               𝛾 ⊢ e2 ⇓ 𝑣         𝛾 ′ [𝑥 ↦→ 𝑣] ⊢ e′ ⇓ 𝑣 ′
                                                                     𝛾 ⊢ e1 e2 ⇓ 𝑣 ′




                        Fig. 31. Non-deterministic sampling semantics for privacy expressions




        ∅; ∅ ⊢ 𝑣 : 𝜏 ′ ; ∅         𝜏 ′ <: 𝜏                 𝑑𝑜𝑚(Γ) = 𝑑𝑜𝑚(𝛾)                ∀𝑥 ∈ 𝑑𝑜𝑚(𝛾).         𝛾(𝑥) ∈ VJΓ(𝑥)/ΓK
                     𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏K                                                            𝛾 ∈ GJΓK

                                                                                       ′
        𝑟 ∈ 𝐴𝑡𝑜𝑚JRK                   tt ∈ 𝐴𝑡𝑜𝑚JunitK                          inl𝜏2 𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊕ ∅ 𝜏2 K             𝑣 ∈ VJ𝜏1 K
                                                                                                 𝜏2′            ∅ ∅
          𝑟 ∈ VJRK                      tt ∈ VJunitK                                        inl        𝑣 ∈ VJ𝜏1 ⊕ 𝜏2 K

                                                ′
                                         inr𝜏1 𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏1 ∅ ⊕ ∅ 𝜏2 K                      𝑣 ∈ VJ𝜏2 K
                                                               𝜏1′              ∅ ∅
                                                           inr       𝑣 ∈ VJ𝜏1 ⊕ 𝜏2 K

             s                                                𝑠𝑥
           h𝜆 𝑥 : 𝜏·𝑠 ′ .𝑒, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ·𝑠 ′) −−→ 𝜏2 K                   ∀𝑣 ∈ VJ𝜏1 K.𝛾[𝑥 ↦→ 𝑣] ⊢ 𝑒 ∈ EJ𝜏2 /(𝑥 : 𝜏1 )K
                                                s                                           𝑠𝑥
                                              h𝜆 𝑥 : 𝜏1 ·𝑠 ′ .𝑒, 𝛾i ∈ VJ(𝑥 : 𝜏1 ·𝑠 ′) −−→ 𝜏2 K

                 p                                           Σ
                                                 → 𝜏2 K
            h𝜆 𝑥 : 𝜏·𝑠.e, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 ·𝑠) −→                            ∀𝑣 ∈ VJ𝜏1 K.𝛾[𝑥 ↦→ 𝑣] ⊢ e ∈ EJ𝜏2 /(𝑥 : 𝜏1 )K
                                                    p                                       Σ
                                                                                   → 𝜏2 K
                                               h𝜆 𝑥 : 𝜏1 ·𝑠.e, 𝛾i ∈ VJ(𝑥 : 𝜏1 ·𝑠) −→

                          𝛾 ⊢𝑒 ⇓𝑣             𝑣 ∈ VJ𝜏K                            ∀𝑣, 𝛾 ⊢ e ⇓ 𝑣 =⇒ 𝑣 ∈ VJ𝜏K
                                 𝛾 ⊢ 𝑒 ∈ EJ𝜏K                                                𝛾 ⊢ e ∈ EJ𝜏K




                                              Fig. 32. 𝜆J : Type Safety Logical Relation



  Proof. (a) Sensitivity FP. We proceed by induction on Γ; Σ0 ⊢ 𝑒 : 𝜏; Σ.

                                      ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
94                    Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


  First, to deal with the cases of sensitivity and privacy functions, we give the typing rules for
sensitivity and privacy closures below:
       s-closure
                               ∃Γ ′, Σ0′ , 𝑑𝑜𝑚(Σ ′′) ⊆ 𝑑𝑜𝑚(Γ ′) ⊆ 𝑑𝑜𝑚(Σ0′ )
       ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ ′(𝑥𝑖 ); ∅
                            ′
                                                              Γ ′, 𝑥 : 𝜏1 ; Σ0′ + 𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + 𝑠 ′𝑥
                                                      s                                          𝑠 ′𝑥
                                        Γ; Σ0 ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i : (𝑥 : 𝜏1 /Γ ′ ·𝑠 1 ) −−→ 𝜏2 /Γ ′ ; ∅

           p-closure
                               ∃Γ ′, Σ0′ , 𝑑𝑜𝑚(Σ ′′) ⊆ 𝑑𝑜𝑚(Γ ′) ⊆ 𝑑𝑜𝑚(Σ0′ )
          ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ ′(𝑥𝑖 ); ∅
                                    ′
                                                                 Γ ′, 𝑥 : 𝜏1 ; Σ0′ + 𝑠 1𝑥 ⊢ e′ : 𝜏2 ; Σ′′
                                                  p                                          Σ′′ /Γ′
                                Γ; Σ0 ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). e′, 𝛾i : (𝑥 : 𝜏1 /Γ ′ ·𝑠 1 ) −−−−→
                                                                                            → 𝜏2 /Γ ′ ; ∅


Case (1) Γ; Σ0 ⊢ 𝑥 : Γ(𝑥); 𝑥
Subproof. By 𝛾 ∈ GJΓK, we know that 𝛾(𝑥) ∈ VJΓ(𝑥)/ΓK . By inspection of the evaluation rules,
we know that 𝛾 ⊢ 𝑥 ⇓ 𝛾(𝑥). We have to prove that 𝛾(𝑥) ∈ VJΓ(𝑥)/ΓK, which we already know and
the result holds.                                                                          ⊳
Case (2) Γ; Σ0 ⊢ 𝑟 : R; ∅
Subproof. Trivial as ∅; ∅ ⊢ 𝑟 : R; ∅.                                                      ⊳
Case (3) Γ; Σ0 ⊢ tt : unit; ∅
Subproof. Trivial as ∅; ∅ ⊢ tt : unit; ∅.                                                  ⊳
Case (4) Γ; Σ0 ⊢ 𝑒 1 𝑒 2 : 𝜏; Σ
Subproof. By s-app we know that
              s-app
                                                          Σ′ +𝑠2𝑥
              Γ ; Σ0 ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑠 1 ) −−−−−→ 𝜏2 ; Σ1                      Γ ; Σ0 ⊢ 𝑒 2 : 𝜏1 ; Σ2             Σ0 ·Σ2 ≤ 𝑠 1
                                                                                                          ′
                                                 Γ ; Σ0 ⊢ 𝑒 1 𝑒 2 : [Σ2/𝑥]𝜏2 ; Σ1 + 𝑠 2 Σ2 + Σ
where 𝜏 = [Σ2/𝑥]𝜏2 , and Σ = Σ1 + 𝑠 2 Σ2 + Σ ′. By induction hypotheses we know that 𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 ,
                                              𝑠2𝑥
𝛾 ⊢ 𝑒 2 ⇓ 𝑣 2 , 𝑣 1 ∈ VJ(𝑥 : 𝜏1 /Γ·𝑠 1 ) −−→ 𝜏2 /ΓK and 𝑣 2 ∈ VJ𝜏1 /ΓK.
                                                                                                       𝑠2𝑥
By inspection of the function predicate, we know that 𝑣 1 ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 /Γ·𝑠 1 ) −−→ 𝜏2 /ΓK and 𝑣 1 =
   s
h𝜆 (𝑥 : 𝜏1′ ·𝑠 1′ ). 𝑒 ′, 𝛾 ′i, for some 𝜏1′, 𝑠 1′ , 𝑒 ′ and 𝛾 ′. We also know then that 𝛾 ′[𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 ′ ∈ EJ𝜏2 /(Γ, 𝑥 :
𝜏1 )K, i.e. 𝛾 ′[𝑥 ↦→ 𝑣 2 ] ⊢ 𝑒 ′ ⇓ 𝑣 ′ and [Σ2/𝑥]𝜏2/Γ = [(Σ2/Γ)/𝑥](𝜏2/Γ) = [∅/𝑥](𝜏2/Γ) = 𝜏2 /(Γ, 𝑥 : 𝜏1 ), but
𝑣 ′ ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K and the result holds.                                                                            ⊳
                        s                                           Σ′
Case (5) Γ; Σ0 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′ : (𝑥 : 𝜏1 ·𝑠) −→ 𝜏2 ; ∅
Subproof. We know that
                                                s-lam
                                                          Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′
                                                              s                             Σ′
                                                Γ ; Σ0 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′ : (𝑥 : 𝜏1 ·𝑠) → 𝜏2 ; ∅
                                s                              s                                                       s
We know that 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′ ⇓ h𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′, 𝛾i. We have to prove that h𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′, 𝛾i ∈
                 Σ′                                                                              Σ′                               𝑠 ′𝑥
VJ((𝑥 : 𝜏1 ·𝑠) −→ 𝜏2 )/ΓK. Suppose Σ ′ = Σ ′′ + 𝑠 ′𝑥, then ((𝑥 : 𝜏1 ·𝑠) −→ 𝜏2 )/Γ = (𝑥 : 𝜏1 /Γ·𝑠) −−→ (𝜏2 /Γ).
                                                  s                                                     𝑠 ′𝑥
First, we have to prove that, h𝜆 (𝑥 : 𝜏1 ·𝑠). 𝑒 ′, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 /Γ·𝑠) −−→ (𝜏2 /Γ)K, i.e. that ∃Γ ′, Σ0′ , 𝑑𝑜𝑚(Σ ′′) ⊆
𝑑𝑜𝑚(Γ ′) ⊆ 𝑑𝑜𝑚(Σ0′ ), ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ′), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ ′(𝑥𝑖 ); ∅, Γ ′, and 𝑥 : 𝜏1 ; Σ0′ + 𝑠𝑥 ⊢ 𝑒 ′ : 𝜏2 ;

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                             95


Σ ′′ + 𝑠 ′𝑥. We prove this by choosing Γ ′ = Γ, Σ0′ = Σ0 , and Σ ′′ + 𝑠 ′𝑥 = Σ ′:

        ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ(𝑥𝑖 ); ∅                Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠 1𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′′ + 𝑠 ′𝑥
                                         s                                            𝑠 ′𝑥
                             Γ; Σ0 ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). 𝑒 ′, 𝛾i : (𝑥 : 𝜏1 /Γ ′ ·𝑠 1 ) −−→ 𝜏2 /Γ ′ ; ∅


Then we have prove that ∀𝑣 ′ ∈ VJ𝜏1 /ΓK, 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ 𝑒 ′ ∈ EJ𝜏2 /(Γ, 𝑥 : 𝑇1 )K. By induction
hypothesis on Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠𝑥 ⊢ 𝑒 ′ : 𝜏2 ; Σ ′, we know that for any 𝛾 ′ ∈ GJΓ, 𝑥 : 𝜏1 K,
𝛾 ′ ⊢ 𝑒 ′ ∈ EJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K. As 𝛾 ∈ GJΓK and 𝑣 ′ ∈ VJ𝜏1 /(Γ, 𝑥 : 𝜏1 )K (𝜏1 /Γ = 𝜏1 /(Γ, 𝑥 : 𝜏1 )), then
𝛾[𝑥 ↦→ 𝑣 ′ ] ∈ GJΓ, 𝑥 : 𝜏1 K, so we pick 𝛾 ′ = 𝛾[𝑥 ↦→ 𝑣 ′ ] and the result holds.                         ⊳
                     p                                     Σ′
Case (6) Γ; Σ0 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). e′ : (𝑥 : 𝜏1 ·𝑠) −−→
                                                   → 𝜏2 ; ∅
Subproof. We know that
                                     p-lam
                                                 Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠𝑥 ⊢ e′ : 𝜏2 ; Σ′
                                                    p                               Σ′
                                     Γ ; Σ0 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). e′ : (𝑥 : 𝜏1 ·𝑠) → 𝜏2 ; ∅
                         p                           p                                                       p
We know that 𝛾 ⊢ 𝜆 (𝑥 : 𝜏1 ·𝑠). e′ ⇓ h𝜆 (𝑥 : 𝜏1 ·𝑠). e′, 𝛾i. We have to prove that h𝜆 (𝑥 : 𝜏1 ·𝑠). e′, 𝛾i ∈
                Σ′                                        Σ′                             Σ′ /Γ
                 → 𝜏2 )/ΓK. Then ((𝑥 : 𝜏1 ·𝑠) −−→
VJ((𝑥 : 𝜏1 ·𝑠) −−→                              → 𝜏2 )/Γ = (𝑥 : 𝜏1 /Γ·𝑠) −−−→
                                                                            → (𝜏2 /Γ).
                                             p                                                       Σ′ /Γ
First, we have to prove that, h𝜆 (𝑥 : 𝜏1 ·𝑠). e′, 𝛾i ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1 /Γ·𝑠) −−−→        → (𝜏2 /Γ)K, i.e. that
∃Γ ′, Σ0′ , 𝑑𝑜𝑚(Σ′′) ⊆ 𝑑𝑜𝑚(Γ ′) ⊆ 𝑑𝑜𝑚(Σ0′ ), ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ ′), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ ′(𝑥𝑖 ); ∅, Γ ′, and
𝑥 : 𝜏1 ; Σ0′ + 𝑠𝑥 ⊢ e′ : 𝜏2 ; Σ′. We prove this by choosing Γ ′ = Γ, Σ0′ = Σ0 :

           ∀𝑥𝑖 ∈ 𝑑𝑜𝑚(Γ), ∅; ∅ ⊢ 𝛾(𝑥𝑖 ) : 𝜏𝑖′, 𝜏𝑖′ <: Γ(𝑥𝑖 ); ∅                   Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠 1𝑥 ⊢ e′ : 𝜏2 ; Σ′
                                        p                                            Σ′ /Γ
                             Γ; Σ0 ⊢ h𝜆 (𝑥 : 𝜏1 ·𝑠 1 ). e′, 𝛾i : (𝑥 : 𝜏1 /Γ·𝑠 1 ) −−−→
                                                                                     → 𝜏2 /Γ ; ∅


Then we have prove that ∀𝑣 ′ ∈ VJ𝜏1 /ΓK, 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ e′ ∈ EJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K. By induction
hypothesis on Γ, 𝑥 : 𝜏1 ; Σ0 + 𝑠𝑥 ⊢ e′ : 𝜏2 ; Σ ′, we know that for any 𝛾 ′ ∈ GJΓ, 𝑥 : 𝜏1 K,
𝛾 ′ ⊢ e′ ∈ EJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K. As 𝛾 ∈ GJΓK and 𝑣 ′ ∈ VJ𝜏1 /(Γ, 𝑥 : 𝜏1 )K (𝜏1 /Γ = 𝜏1 /(Γ, 𝑥 : 𝜏1 ))
𝛾[𝑥 ↦→ 𝑣 ′ ] ∈ GJΓ, 𝑥 : 𝜏1 K, so we pick 𝛾 ′ = 𝛾[𝑥 ↦→ 𝑣 ′ ] and the result holds.                 ⊳
Case (7) Γ ; Σ0 ⊢ inl𝜏2 𝑒 ′ : 𝜏1 Σ ⊕∅ 𝜏2 ; ∅
Subproof. We know that
                                             inl
                                                         Γ ; Σ0 ⊢ 𝑒 ′ : 𝜏1 ; Σ
                                             Γ ; Σ0 ⊢ inl𝜏2 𝑒 ′ : 𝜏1 Σ ⊕∅ 𝜏2 ; ∅

By induction hypothesis on Γ ; Σ0 ⊢ 𝑒 ′ : 𝜏1 ; Σ we know that 𝛾 ⊢ 𝑒 ′ ⇓ 𝑣 ′ and 𝑣 ′ ∈ VJ𝜏1 /ΓK.
As 𝛾 ⊢ inl𝜏2 𝑒 ′ ⇓ inl𝜏2 /𝛾 𝑣 ′ , we have to prove that inl𝜏2 /𝛾 𝑣 ′ ∈ VJ(𝜏1 Σ ⊕∅ 𝜏2 )/ΓK. Notice that
(𝜏1 Σ ⊕∅ 𝜏2 )/Γ = (𝜏1 /Γ ∅ ⊕∅ 𝜏2 /Γ, and that 𝜏2 /𝛾 = 𝜏2 /Γ Then we have to prove that inl𝜏2 /Γ 𝑣 ′ ∈
VJ𝜏1 /Γ ∅ ⊕∅ 𝜏2 /ΓK, which is direct as we already know that 𝑣 ′ ∈ VJ𝜏1 /ΓK.                         ⊳
Case (8) Γ ; Σ0 ⊢ inr𝜏1 𝑒 ′ : 𝜏1 Σ ⊕∅ 𝜏2 ; ∅
Subproof. Analogous to the inl𝜏2 𝑒 ′ case.                                                                                  ⊳
Case (9) Γ ; Σ0 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } : [Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12 /𝑦]𝜏3 ; ((𝑠 2 ∗ Σ1 +
𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 ∗ Σ1 + 𝑠 3 Σ12 + Σ3 ))

                                    ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
96                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


Subproof. We know that
     s-case
        Γ ; Σ0 ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1     Γ, 𝑥 : 𝜏11 ; Σ0 + (Σ0 ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 2 𝑥
                              Γ, 𝑦 : 𝜏12 ; Σ0 + (Σ0 ·(Σ1 + Σ12 ))𝑥 ⊢ 𝑒 3 : 𝜏3 ; Σ3 + 𝑠 3𝑦
                Γ ; Σ0 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } :
                    [Σ1 + Σ11/𝑥]𝜏2 ⊔ [Σ1 + Σ12/𝑦]𝜏3 ; ((𝑠 2 ∗ Σ1 + 𝑠 2 Σ11 + Σ2 ) ⊔ (𝑠 3 ∗ Σ1 + 𝑠 3 Σ12 + Σ3 ))

where 𝜏 = [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 .
By induction hypothesis on Γ ; Σ0 ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1 , we know that 𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 and
𝑣 1 ∈ VJ𝜏11 /Γ ∅ ⊕∅ 𝜏12 /ΓK (Σ1𝑖 /Γ = ∅). Then either 𝑣 1 = inl𝜏12 /Γ 𝑣 11 , or 𝑣 1 = inl𝜏11 /Γ 𝑣 12 . Let us
suppose 𝑣 1 = inl𝜏12 /Γ 𝑣 11 (the other case is similar), then inl𝜏12 /Γ 𝑣 11 ∈ VJ𝜏11 /Γ ∅ ⊕∅ 𝜏12 /ΓK, and
thus 𝑣 11 ∈ VJ𝜏11 /ΓK.
Then by induction hypothesis on Γ, 𝑥 : 𝜏11 ; Σ0 + (Σ0 ·(Σ1 + Σ11 ))𝑥 ⊢ 𝑒 2 : 𝜏2 ; Σ2 + 𝑠 2𝑥, we know that
𝛾[𝑥 ↦→ 𝑣 11 ] ⊢ 𝑒 2 ∈ EJ𝜏/ΓK, therefore 𝛾 ⊢ 𝑒 2 ⇓ 𝑣 2 and 𝑣 2 ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏11 )K.
Then by inspection of the evaluation semantics for p-case, 𝛾 ⊢ case 𝑒 1 of {𝑥 ⇒ 𝑒 2 } {𝑦 ⇒ 𝑒 3 } ⇓
𝑣 2 and we have to prove that 𝑣 2 ∈ VJ([Σ1 + Σ11 /𝑥]𝜏2 ⊔ [Σ1 + Σ12/𝑦]𝜏3 K)/Γ. But ([Σ1 + Σ11 /𝑥]𝜏2 ⊔
[Σ1 + Σ12 /𝑦]𝜏3 K)/Γ = (𝜏2 ⊔ 𝜏3 K)/(Γ, 𝑥 : 𝜏11 ). The result follows from weakening lemma D.2.              ⊳
(b) Privacy FP. We proceed by induction on Γ; Σ0 ⊢ e : 𝜏1 ; Σ.
                                𝑥 ]𝜏1 ; ⌉Σ1 ⌈∞ + FS∞ (𝜏1 )
Case (1) Γ ; Σ0 ⊢ return 𝑒 : [∅/Û
Subproof. By return we know that
                                return
                                     Γ ; Σ0 ⊢ 𝑒 1 : 𝜏1 ; Σ1       𝑥Û = FV(FS(𝜏1 ))
                                                        𝑥 ]𝜏1 ; ⌉Σ1 ⌈∞ + FS∞ (𝜏1 )
                               Γ ; Σ0 ⊢ return 𝑒 1 : [∅/Û

where 𝜏 = [∅/Û   𝑥 ]𝜏, and Σ = ⌉Σ1 ⌈∞ + FS∞ (𝜏1 ). By induction hypotheses we know that 𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 ,
and 𝑣 1 ∈ VJ𝜏1 /ΓK.
By inspection of the evaluation semantics 𝛾 ⊢ return 𝑒 1 ⇓ 𝑣 1 . Notice that 𝑥Û ⊆ Γ, then ([∅/Û
                                                                                              𝑥 ]𝜏1 )/Γ =
𝜏1 /Γ, and as 𝑣 1 ∈ VJ𝜏1 /ΓK the result holds immediately.                                              ⊳
Case (2) Γ ; Σ0 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 : [∅/𝑥]𝜏2 ; Σ1 + Σ2
Subproof. By bind we know that
                           bind
                           Γ ; Σ 0 ⊢ e 1 : 𝜏 1 ; Σ1      Γ, 𝑥 : 𝜏1 ; Σ0 + 0𝑥 ⊢ e2 : 𝜏2 ; Σ2
                              Γ ; Σ0 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 : [∅/𝑥]𝜏2 ; Σ1 + [∅/𝑥]Σ2

where 𝜏 = [∅/𝑥]𝜏2, and Σ = Σ1 +[∅/𝑥]Σ2. By induction hypothesis on Γ ; Σ0 ⊢ e1 : 𝜏1 ; Σ1 , we know
that 𝛾 ⊢ e1 ∈ EJ𝜏1 /ΓK, therefore for all 𝑣 1 such that 𝛾 ⊢ e1 ⇓ 𝑣 1 it follows that 𝑣 1 ∈ VJ𝜏1 /ΓK. Also, by
induction hypothesis on Γ, 𝑥 : 𝜏1 ; Σ0 +0𝑥 ⊢ e2 : 𝜏2 ; Σ2 , we know that 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ∈ EJ𝜏2 /(Γ, 𝑥 :
𝜏1 )K, therefore for all 𝑣 2 such that 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣 2 it follows that 𝑣 2 ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K.
Then, we have to prove that for all 𝑣 2 such that 𝛾 ⊢ 𝑥 : 𝜏1 ← e1 ; e2 ⇓ 𝑣 2 it follows that
𝑣 2 ∈ VJ([∅/𝑥]𝜏2 )/ΓK. Let us ﬁx 𝑣 2 . By inspection of the evaluation semantics for bind, we know
that there exist 𝑣 1 such that 𝛾 ⊢ e1 ⇓ 𝑣 1 and 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣 2 . But we know that for all
𝑣 1 and 𝑣 2 such that 𝛾 ⊢ e1 ⇓ 𝑣 1 and 𝛾[𝑥 ↦→ 𝑣 1 ] ⊢ e2 ⇓ 𝑣 2 , it follows that 𝑣 1 ∈ VJ𝜏1 /ΓK and
𝑣 2 ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K. Finally, notice that ([∅/𝑥]𝜏2)/Γ = 𝜏2 /(Γ, 𝑥 : 𝜏1 ) and the result holds.
                                                                                                            ⊳
Case (3) Γ ; Σ0 ⊢ gauss 𝜇 𝜎 2 : R ; ∅

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       97


Subproof. By gauss we know that
                                        gauss

                                       Γ ; Σ0 ⊢ 𝛾 ⊢ gauss 𝜇 𝜎 2 : R ; ∅
we know that 𝛾 ⊢ gauss 𝜇 𝜎 2 ⇓ 𝑟 , for some 𝑟 . But 𝑟 ∈ VJRK and the result holds.                                     ⊳
Case (4) Γ ; Σ0 ⊢ 𝑖 𝑓 𝑒 1 {e2 } {e3 } : 𝜏 ; ⌉Σ1 ⌈∞ ⊔ (Σ2 ⊔ Σ3 )
Subproof. By if we know that
                   if
                   Γ ; Σ0 ⊢ 𝑒1 : B ; Σ1           Γ ; Σ 0 ⊢ e 2 : 𝜏 ; Σ2       Γ ; Σ 0 ⊢ e 3 : 𝜏 ; Σ3
                                                                           ∞
                              Γ ; Σ0 ⊢ 𝑖 𝑓 𝑒 1 {e2 } {e3 } : 𝜏 ; ⌉Σ1 ⌈ ⊔ (Σ2 ⊔ Σ3 )
where Σ = ⌉Σ1 ⌈∞ ⊔ (Σ2 ⊔ Σ3 ). By induction hypothesis on Γ ; Σ0 ⊢ 𝑒 1 : B ; Σ1 , we know that
𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 and 𝑣 1 ∈ VJBK. Unfolding booleans as sums we know that 𝑣 1 ∈ VJunit ∅ ⊕∅ unitK.
Let us assume that 𝑣 1 = inlunit tt (the other case is analogous). Then by induction hypothesis
on Γ ; Σ0 ⊢ e2 : 𝜏 ; Σ2 , we know that 𝛾 ⊢ e2 ∈ EJ𝜏/ΓK, therefore for all 𝑣 2 such that 𝛾 ⊢ e2 ⇓ 𝑣 2 it
follows that 𝑣 2 ∈ VJ𝜏/ΓK.
Then we have to prove that for all 𝑣 2 such that 𝛾 ⊢ 𝑖 𝑓 𝑒 1 {e2 } {e3 } ⇓ 𝑣 2 it follows that 𝑣 2 ∈ VJ𝜏/ΓK.
Then by inspection of the evaluation semantics for if, we know that if 𝛾 ⊢ 𝑖 𝑓 𝑒 1 {e2 } {e3 } ⇓ 𝑣 2
then 𝛾 ⊢ e2 ⇓ 𝑣 2 . Then, the result holds immediately.                                                   ⊳
                                                                                           ∞
Case (5) Γ ; Σ0 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } : [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 ; ⌉Σ1 ⌈ ⊔ [Σ11/𝑥]Σ2 ⊔
[Σ12/𝑦]Σ3
Subproof. By p-case we know that
  p-case
                                       Γ ; Σ0 ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1
  Γ, 𝑥 : 𝜏11 ; Σ0 + (Σ0 ·(Σ1 + Σ11 ))𝑥 ⊢ e2 : 𝜏2 ; Σ2        Γ, 𝑦 : 𝜏12 ; Σ0 + (Σ0 ·(Σ1 + Σ12 ))𝑦 ⊢ e3 : 𝜏3 ; Σ3
               Γ ; Σ0 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } :
                               [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 ; ⌉Σ1 ⌈∞ ⊔ [Σ11/𝑥]Σ2 ⊔ [Σ12/𝑦]Σ3
where 𝜏 = [Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 , and Σ = ⌉Σ1 ⌈∞ ⊔ [Σ11/𝑥]Σ2 ⊔ [Σ12/𝑦]Σ3 .
By induction hypothesis on Γ ; Σ0 ⊢ 𝑒 1 : 𝜏11 Σ11 ⊕ Σ12 𝜏12 ; Σ1 , we know that 𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 and
𝑣 1 ∈ VJ𝜏11 /Γ ∅ ⊕∅ 𝜏12 /ΓK (Σ1𝑖 /Γ = ∅). Then either 𝑣 1 = inl𝜏12 /Γ 𝑣 11 , or 𝑣 1 = inl𝜏11 /Γ 𝑣 12 . Let us
suppose 𝑣 1 = inl𝜏12 /Γ 𝑣 11 (the other case is similar), then inl𝜏12 /Γ 𝑣 11 ∈ VJ𝜏11 /Γ ∅ ⊕∅ 𝜏12 /ΓK, and
thus 𝑣 11 ∈ VJ𝜏11 /ΓK.
Then by induction hypothesis on Γ, 𝑥 : 𝜏11 ; Σ0 + (Σ0 ·(Σ1 + Σ11 ))𝑥 ⊢ e2 : 𝜏2 ; Σ2 , we know that
𝛾[𝑥 ↦→ 𝑣 11 ] ⊢ e2 ∈ EJ𝜏/ΓK, therefore for all 𝑣 2 such that 𝛾 ⊢ e2 ⇓ 𝑣 2 it follows that 𝑣 2 ∈ VJ𝜏2 /(Γ, 𝑥 :
𝜏11 )K.
Then we have to prove that for all 𝑣 2 such that 𝛾 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } ⇓ 𝑣 2 it follows
that 𝑣 2 ∈ VJ([Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 K)/Γ. By inspection of the evaluation semantics for p-case, if
𝛾 ⊢ case 𝑒 1 of {𝑥 ⇒ e2 } {𝑦 ⇒ e3 } ⇓ 𝑣 2 then 𝛾 ⊢ e2 ⇓ 𝑣 2 . Then, by the induction hypothesis we
know that 𝑣 2 ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏11 )K. But ([Σ11/𝑥]𝜏2 ⊔ [Σ12/𝑦]𝜏3 K)/Γ = (𝜏2 ⊔ 𝜏3 K)/(Γ, 𝑥 : 𝜏11 ). The result
follows from weakening lemma D.2.                                                                           ⊳
                                            ∞
Case (6) Γ ; Σ0 ⊢ e1 e2 : [Σ2/𝑥]𝜏2 ; ⌉Σ1 ⌈ + [Σ2/𝑥]Σ
Subproof. By p-app we know that
              p-app
                                        Σ+𝑝𝑥
              Γ ; Σ0 ⊢ 𝑒 1 : (𝑥 : 𝜏1 ·𝑠) −−−−→
                                             → 𝜏2 ; Σ1          Γ ; Σ0 ⊢ 𝑒 2 : 𝜏1 ; Σ2        Σ0 ·Σ2 ≤ 𝑠
                                                                       ∞
                                Γ ; Σ0 ⊢ e1 e2 : [Σ2/𝑥]𝜏2 ; ⌉Σ1 ⌈ + [Σ2/𝑥]Σ

                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
98                 Matías Toro, David Darais, Chike Abuah, Joe Near, Damián Árquez, Federico Olmedo, and Éric Tanter


where 𝜏 = [Σ2/𝑥]𝜏2, and Σ = ⌉Σ1 ⌈∞ + [Σ2/𝑥]Σ. By induction hypotheses we know that for all 𝑣 1
                                                                                                  Σ/Γ
and 𝑣 2 such that 𝛾 ⊢ 𝑒 1 ⇓ 𝑣 1 , 𝛾 ⊢ 𝑒 2 ⇓ 𝑣 2 , it follows that 𝑣 1 ∈ VJ(𝑥 : 𝜏1 /Γ·𝑠 1 ) −−−→     → 𝜏2 /ΓK and
𝑣 2 ∈ VJ𝜏1 /ΓK.
We have to prove that for all 𝑣 ′ such that 𝛾 ⊢ e1 e2 ⇓ 𝑣 ′ it follows that 𝑣 ′ ∈ VJ[Σ2/𝑥]𝜏2/ΓK. By
                                                                                                                 p
inspection of the evaluation semantics for p-app, we know that if 𝛾 ⊢ e1 e2 ⇓ 𝑣 ′ then 𝑣 1 = h𝜆 (𝑥 :
  ′   ′     ′   ′                                ′    ′    ′     ′
𝜏1 ·𝑠 1 ). e , 𝛾 i and 𝛾 ⊢ 𝑒 2 ⇓ 𝑣 2 , for some 𝜏1, 𝑠 1 , e and 𝛾 . By inspection of the function predicate, we
know that 𝛾 ′[𝑥 ↦→ 𝑣 2 ] ⊢ e′ ∈ EJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K, i.e. for all 𝑣 ′ such that 𝛾 ′[𝑥 ↦→ 𝑣 2 ] ⊢ e′ ⇓ 𝑣 ′ it follows
that 𝑣 ′ ∈ VJ𝜏2 /(Γ, 𝑥 : 𝜏1 )K but [Σ2/𝑥]𝜏2/Γ = [(Σ2/Γ)/𝑥](𝜏2/Γ) = [∅/𝑥](𝜏2/Γ) = 𝜏2 /(Γ, 𝑥 : 𝜏1 ) and the
result holds.                                                                                                      ⊳
                                                                                                                   
     Lemma D.2 (Weakening).            If 𝑣 ∈ VJ𝜏K and 𝜏 <: 𝜏 ′ , 𝐹𝑉 (𝜏 ′ ) = ∅, then 𝑣 ∈ VJ𝜏 ′ K.
  Proof. Straightforward induction on 𝜏 such that VJ𝜏K.
Case (1) 𝜏 ∈ {R, unit}
Subproof. Trivial as 𝜏 <: 𝜏.                                                                                      ⊳
                                Σ1
Case (2) 𝜏 = (𝑥 : 𝜏1 ·𝑠)𝑃 −−→
                            → 𝜏2
                                         Σ′1
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑠 ′ ) −−→
                                       → 𝜏2′ , for some 𝜏1′ <: 𝜏1, 𝑠 ′ ≤ 𝑠, Σ1 <: Σ1′ , and 𝜏2 <: 𝜏2′ . We know
                          Σ1                                                                Σ′1
                         → 𝜏2 K and we have to prove that 𝑣 ∈ VJ(𝑥 : 𝜏1′ ·𝑠 ′ ) −−→
that 𝑣 ∈ VJ(𝑥 : 𝜏1 ·𝑠) −−→                                                        → 𝜏2′ K. First we have to
                                       Σ′1
prove that 𝑣 ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1′ ·𝑠 ′ ) −−→
                                      → 𝜏2′ K, which is direct.
                 p
Suppose 𝑣 = h𝜆 𝑥 : 𝜏1 ·𝑠.e, 𝛾i. Let 𝑣 ′ ∈ VJ𝜏1′ K, we have to prove that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ e ∈ EJ𝜏2′ K, i.e. that
𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ e ⇓ 𝑣 ′′ and 𝑣 ′′ ∈ VJ𝜏2′ K. By induction hypothesis we know that 𝑣 ′ ∈ VJ𝜏1 K, and by
                     Σ1
                    → 𝜏2 K we know that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ e ∈ EJ𝜏2 K. This means that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ e ⇓ 𝑣 ′′
𝑣 ∈ VJ(𝑥 : 𝜏1 ·𝑠) −−→
and 𝑣 ∈ VJ𝜏2 K. But as 𝜏2 <: 𝜏2′ by induction hypothesis 𝑣 ′′ ∈ VJ𝜏2′ K and the result holds.
     ′′                                                                                                 ⊳
                            Σ1
Case (3) 𝜏 = (𝑥 : 𝜏1 ·𝑠) −−→ 𝜏2
                                         Σ′1
Subproof. Then 𝜏 ′ = (𝑥 : 𝜏1′ ·𝑠 ′ ) −−→ 𝜏2′ , for some 𝜏1′ <: 𝜏1, 𝑠 ′ ≤ 𝑠, Σ1 <: Σ1′ , and 𝜏2 <: 𝜏2′ . We know
                           Σ1                                                               Σ′1
that 𝑣 ∈ VJ(𝑥 : 𝜏1 ·𝑠) −−→ 𝜏2 K and we have to prove that 𝑣 ∈ VJ(𝑥 : 𝜏1′ ·𝑠 ′ ) −−→ 𝜏2′ K. First we have to
                                       Σ′1
prove that 𝑣 ∈ 𝐴𝑡𝑜𝑚J(𝑥 : 𝜏1′ ·𝑠 ′ ) −−→ 𝜏2′ K, which is direct.
               p
Suppose 𝑣 = h𝜆 𝑥 : 𝜏1 ·𝑠.𝑒, 𝛾i. Let 𝑣 ′ ∈ VJ𝜏1′ K, we have to prove that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ 𝑒 ∈ EJ𝜏2′ K, i.e. that
𝛾[𝑥 ↦→ 𝑣 ] ⊢ 𝑒 ⇓ 𝑣 ′′ and 𝑣 ′′ ∈ VJ𝜏2′ K. By induction hypothesis we know that 𝑣 ′ ∈ VJ𝜏1 K, and by
        ′
                     Σ1
𝑣 ∈ VJ(𝑥 : 𝜏1 ·𝑠) −−→ 𝜏2 K we know that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ 𝑒 ∈ EJ𝜏2 K. This means that 𝛾[𝑥 ↦→ 𝑣 ′ ] ⊢ 𝑒 ⇓ 𝑣 ′′
and 𝑣 ′′ ∈ VJ𝜏2 K. But as 𝜏2 <: 𝜏2′ by induction hypothesis 𝑣 ′′ ∈ VJ𝜏2′ K and the result holds.             ⊳
                 ∅ ∅
Case (4) 𝜏 = 𝜏1 ⊕ 𝜏2
Subproof. Then 𝜏 ′ = 𝜏1′ ∅ ⊕∅ 𝜏2′ , for some 𝜏1 <: 𝜏1′ and 𝜏2 <: 𝜏2′ . We know that 𝑣 ∈ VJ𝜏1 ∅ ⊕∅ 𝜏2 K
                                                                           ′′
and we have to prove that 𝑣 ∈ VJ𝜏1′ ∅ ⊕∅ 𝜏2′ K. Suppose 𝑣 = inl𝜏2 𝑣 ′ (the other case is analogous).
We know 𝜏2′′ <: 𝜏2 , and as 𝜏2 <: 𝜏2′ , then 𝜏2′′ <: 𝜏2′ . First we have to prove that 𝑣 ∈ 𝐴𝑡𝑜𝑚J𝜏1′ ∅ ⊕∅ 𝜏2′ K,
which is direct.
We know that 𝑣 ′ ∈ VJ𝜏1 K, then by induction hypothesis we know that 𝑣 ′ ∈ VJ𝜏1′ K, therefore
    ′′
inl𝜏2 𝑣 ′ ∈ VJ𝜏1′ ∅ ⊕∅ 𝜏2′ K and the result holds.                                                           ⊳
                                                                                                            
     Type safety for open terms follows immediately.

ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
Contextual Linear Types for Diﬀerential Privacy                                                                       99


  Corollary D.3 (Type Safety and Normalization of 𝜆J ).
  (a) Let ⊢ 𝑒 : 𝜏; ∅, then ⊢ 𝑒 ⇓ 𝑣, and ⊢ 𝑣 : 𝜏 ′; ∅, where 𝜏 ′ <: 𝜏.
  (b) Let ⊢ e : 𝜏; ∅, then ⊢ e ⇓ 𝑣, and ⊢ 𝑣 : 𝜏 ′ ; ∅, where 𝜏 ′ <: 𝜏.
  Proof. Direct consequence of Prop D.1.                                                                              




                                ACM Trans. Program. Lang. Syst., Vol. 1, No. 1, Article . Publication date: January 2023.
