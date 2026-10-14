                                         Modular Verification of Differential Privacy in Probabilistic
                                         Higher-Order Separation Logic (Extended Version)
                                         PHILIPP G. HASELWARTER, Aarhus University, Denmark
                                         ALEJANDRO AGUIRRE, Aarhus University, Denmark
                                         SIMON ODDERSHEDE GREGERSEN, New York University, USA
                                         KWING HEI LI, Aarhus University, Denmark
                                         JOSEPH TASSAROTTI∗ , New York University, USA
arXiv:2604.12713v1 [cs.PL] 14 Apr 2026




                                         LARS BIRKEDAL, Aarhus University, Denmark
                                         Differential privacy is the standard method for privacy-preserving data analysis. The importance of having
                                         strong guarantees on the reliability of implementations of differentially private algorithms is widely recognized
                                         and has sparked fruitful research on formal methods. However, the design patterns and language features
                                         used in modern DP libraries as well as the classes of guarantees that the library designers wish to establish
                                         often fall outside of the scope of previous verification approaches.
                                            We introduce a program logic suitable for verifying differentially private implementations written in
                                         complex, general-purpose programming languages. Our logic has first-class support for reasoning about
                                         privacy budgets as a separation logic resource. The expressiveness of the logic and the target language allow
                                         our approach to handle common programming patterns used in the implementation of libraries for differential
                                         privacy, such as privacy filters and caching. While previous work has focused on developing guarantees for
                                         programs written in domain-specific languages or for privacy mechanisms in isolation, our logic can reason
                                         modularly about primitives, higher-order combinators, and interactive algorithms.
                                            We demonstrate the applicability of our approach by implementing a verified library of differential privacy
                                         mechanisms, including an online version of the Sparse Vector Technique, as well as a privacy filter inspired
                                         by the popular Python library OpenDP, which crucially relies on our ability to handle the combination of
                                         randomization, local state, and higher-order functions. We demonstrate that our specifications are general
                                         and reusable by instantiating them to verify clients of our library. All of our results have been foundationally
                                         verified in the Rocq Prover.
                                         CCS Concepts: • Theory of computation → Separation logic; Logic and verification; Probabilistic
                                         computation; Program verification; • Mathematics of computing → Probabilistic algorithms.

                                         1   Introduction
                                         Differential privacy [Dwork et al. 2006; Dwork and Roth 2014] (DP) is a collection of programming
                                         techniques to release aggregate information from a database while providing statistical guarantees
                                         about the privacy of individual user data. DP has been used widely in government and industrial
                                         applications to protect critical personal information (medical, financial, demographic, behavioral).
                                         The correctness of the implementations of DP is therefore crucial: logic- or implementation-level
                                         bugs can lead to catastrophic failure of the promised privacy guarantees.
                                            The importance of having trustworthy implementations of DP is widely recognized. On the one
                                         hand, it has led to significant research in programming language and program verification. On the
                                         ∗ Also affiliated with Amazon Web Services. This paper does not reflect the views of Amazon Web Services.


                                         Authors’ Contact Information: Philipp G. Haselwarter, Aarhus University, Denmark, pgh@cs.au.dk; Alejandro Aguirre,
                                         Aarhus University, Denmark, alejandro@cs.au.dk; Simon Oddershede Gregersen, New York University, USA, s.gregersen@
                                         nyu.edu; Kwing Hei Li, Aarhus University, Denmark, hei.li@cs.au.dk; Joseph Tassarotti, New York University, USA,
                                         jt4767@cs.nyu.edu; Lars Birkedal, Aarhus University, Denmark, birkedal@cs.au.dk.



                                         This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
233:2                                P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


other, industrial developments of DP are routinely accompanied by pen-and-paper proofs of their
claimed privacy properties. The OpenDP collaboration1 even goes as far as to collect a proof for
each element of the library, which are checked by a “privacy proof review board”.
   DP provides strong statistical guarantees that the data contributed by an individual does not
influence the result of the analysis by too much, and hence cannot be recovered by observing the
outcome. This is achieved by adding a small amount of random noise to each step of data analysis
that could leak private information. This way, even if the input data changes by a small amount
(say, the data of one user in a database), we can expect the output of the noisy program output to
be similar, and an observer will not be able to tell whether the change comes from the noise or a
change in inputs. The strength of the privacy guarantee of differentially private (dp) programs is
governed by a parameter 𝜀 ∈ R ≥0 , that controls the overall probability that any user’s privacy is
compromised; a lower 𝜀 means a more private program.

   Managing the privacy budget. A central idea of programming with DP is to think of the
parameter 𝜀 that controls the noise distribution as the “privacy budget”. To ensure that the whole
program 𝑃, written as a sequence of computations 𝑃 = 𝑐 0 ; 𝑐 1 ; . . . ; 𝑐𝑛 , is 𝜀-differentially private (𝜀-dp),
we can “allocate” some part 𝜀𝑖 of our budget to each part 𝑐𝑖 of the program and check that the
probability that 𝑐𝑖 compromises privacy is controlled according to 𝜀𝑖 . So long as the sum of the
error terms 𝜀𝑖 is below the global budget 𝜀, the program as a whole is 𝜀-dp. This principle is known
as the sequential composition theorem of DP, and it justifies our budget intuition of the privacy
parameter: 𝜀 represents a resource that can be split according to the structure of the program, and
is consumed by computing noisy results from a database.
   The most widely used deployments of DP are based on dynamic techniques for tracking the pri-
vacy budget via a trusted library such as OpenDP (written in Python, Rust) or Google’s Differential
Privacy library (C++, Go, Java). Rather than specifying exactly how much 𝜀𝑖 each part of a program
consumes, the budget consumption of the completed computations 𝑐 0 ; . . . ; 𝑐𝑖 −1 is tracked, and a
runtime check ensures that enough budget for 𝑐𝑖 remains.

1.1     The Challenges of Verifying DP Frameworks
Most practical DP frameworks use “advanced” programming language features like higher-order
functions (e.g., in the form of classes or function pointers) and dynamically allocated, local state
(e.g., via class-private attributes). This is necessary to enable the modular construction of private
programs through an API, where a library client does not have to concern themselves with the
management of the privacy budget and correct application of noise to the results. To be able to reason
compositionally, privacy proofs of a library API should likewise support modular specifications. We
consider three representative challenges that arise from reasoning about libraries for DP:
     (i) encapsulating dynamic, fine-grained budget accounting,
    (ii) interactive or “online” data analysis,
   (iii) budget minimization via caching.
As we shall see shortly, all three of these techniques rely on stateful randomized higher-order
functions to implement features that are essential to the modular construction of dp programs. To
verify modular API specifications we must thus support higher-order reasoning about local state.
  We illustrate the programming patterns via Python code snippets inspired by OpenDP, but the
challenges also arise in, e.g., the C++ implementation of Google’s Differential Privacy library.2

1 OpenDP was initiated as a collaboration between Harvard University and Microsoft.
2 See, e.g., https://github.com/google/differential-privacy/blob/0a3b05a65f7ed8de/cc/accounting/accountant.cc#L46
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:3


Although the verification approach developed in this paper is for an ML-like core language (§2.3)
rather than Python, it can faithfully represent the salient aspects of these Python programs.
1.1.1 Dynamic budget accounting. An essential functionality of these libraries is that they
offer privacy filters [Rogers et al. 2016] that encapsulate the intricate reasoning about the privacy
budget in a core, trusted API. A privacy filter tracks the privacy cost that a program has incurred
up to the current execution point 𝑐 0 ; . . . ; 𝑐𝑖 −1 , and only executes 𝑐𝑖 if enough budget remains. The
example implementation of a simplified PrivacyFilter in Figure 1 is initialized with some budget
and provides a single try_run(cost, f) method, which only runs f if there is indeed at least
enough budget left to cover its cost. So long as each mechanism f correctly reports its budget
consumption (cost), the filter will ensure that the total privacy cost will never exceed the global
budget.

                                    class PrivacyFilter:
                                      def __init__(self, budget):
                                        self.budget_left = budget

                                      def try_run(self, cost, f):
                                        if self.budget_left < cost :
                                          return None
                                        self.budget_left -= cost
                                        return f()
                  Fig. 1. PrivacyFilter ensures that no client can exceed the privacy budget.
    Centralized dynamic budget management simplifies the privacy analysis of programs and allows
for scaling to industrial applications. Importantly, dynamically computed bounds enable a tighter
analysis of the privacy cost compared to static type checks [Gaboardi et al. 2013; Lobo-Vesga
et al. 2020]. Recall that the usual sequential composition theorem of DP requires that all 𝜀𝑖 be
chosen upfront. The adaptive composition theorem [Rogers et al. 2016] for DP lifts this restriction
and allows the analyst to adaptively chose each 𝜀𝑖 depending on the results of previous (private)
computations. Despite the successes of type- and program-logic-based analyses of DP, none of the
existing systems can be used to specify and verify the correctness of implementations of privacy
filters.
1.1.2 Interactive data analysis. Interactivity is central to real-world data analysis under DP.
Given a new dataset, a data analyst does not just issue a static set of queries. Instead, they may
compute some summary statistics to explore what ranges of values or categories of responses are of
interest, and construct further queries based on those observations. This interactive or “online” style
of analysis is crucial for practical utility [Cowan et al. 2024; Dwork and Roth 2014; Kostopoulou
et al. 2023]. A standard way to represent interactive computations is as streams: given a stream of
queries, a private interactive mechanism should produce a stream of results.
   The AboveThreshold mechanism in Figure 2 constructs a stream of booleans from a stream
of queries as an iterator. The 𝑛-th boolean indicates whether 𝑞𝑛 was above the threshold 𝑇 , after
suitable Laplace noise was added. Crucially, the queries themselves are provided as an iterator
rather than as a precomputed list, and 𝑞𝑛 is only evaluated in the 𝑛-th call to __next__. The
AboveThreshold mechanism is 𝜀-dp because the stream stops producing results after the first time
True is returned; this is a standard result in DP but challenging to prove formally because it does
not follow simply from the sequential composition theorem.
   Any realistic verification framework for DP must therefore capture not only isolated, static
mechanisms but also their behavior as interactive, stateful processes that maintain internal state
and privacy budget across calls.
233:4                            P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal

class AboveThreshold:
  def __init__(self, eps, T, queries, db):                    def __next__(self):
    self.eps = eps                                              if self.halted:
    self.T = Laplace(T, eps/2)                                    raise StopIteration
    self.queries = queries                                      q = next(self.queries)
    self.db = db                                                v = Laplace(q(self.db), self.eps/4)
    self.halted = False                                         b = (self.T <= v)
                                                                self.halted = b
  def __iter__(self):                                           return b
    return self
                        Fig. 2. The classic Above Threshold interactive mechanism.

1.1.3 Budget minimization via caching. Certain results (e.g., the number of non-zero entries)
have to be calculated many times over as part of different analysis passes on a dataset. This
can be wasteful in practical applications, since each private computation consumes some of the
privacy budget, even if the same result has already been computed elsewhere in the program.
Caching provides a solution to this problem: if the noisy results of queries are cached, then a
repeated query can simply reuse the prior noisy result without incurring any privacy cost. Recent
implementations of privacy frameworks have studied increasingly sophisticated caching strategies
for DP workloads [Kostopoulou et al. 2023; Kotsogiannis et al. 2019; Mazmudar et al. 2022; Peng
et al. 2013], but even simple implementations of caching via memoization can lead to substantial
savings in privacy budget in practical workloads [Peng et al. 2013][Kostopoulou et al. 2023, Fig. 3].
   The implementation of memoization mk_query_cache in Figure 3 locally allocates a cache
associated to a mechanism add_noise and a dataset db and returns a closure f which can be used
subsequently to privately evaluate queries on db. Although it is a simple general-purpose caching
mechanism, studying it formally requires reasoning about local state and higher-order functions.
This places it outside of the scope of existing systems.

                          def mk_query_cache(add_noise, db):
                            cache = {}
                            def f(query):
                              if query in cache:
                                return cache[query]
                              v = add_noise(query(db))
                              cache[query] = v
                              return v
                            return f
                                  Fig. 3. A generic caching mechanism.

1.2     Formal Guarantees for Differential Privacy
DP lends itself well to the analysis via standard PL methods due to its compositional nature. We
distinguish two main classes of approaches. Type-based approaches [Abuah et al. 2022; Barthe
et al. 2015b; de Amorim et al. 2021; Gaboardi et al. 2013; Lobo-Vesga et al. 2020, 2024; Near et al.
2019; Reed and Pierce 2010; Toro et al. 2023; Winograd-Cort et al. 2017; Zhang and Kifer 2017]
use a static typing discipline to ensure that the programs accepted by the system are dp. These
approaches benefit from high degrees of automation. Most type-based approaches, however, do not
handle mutable state. More generally, the complex nature of the type systems required (dependent-,
linear-, contextual-, or refinement types, or combinations thereof), hinders their integration with
mainstream programming languages.
   On the other hand, relational probabilistic Hoare logics such as apRHL [Barthe et al. 2015a,
2016a,b], are more expressive but require more user effort in the form of manual or interactive
proofs. These methods works particularly well when the program logic is defined with respect
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:5


to a relatively simple denotational semantics of programs as subdistributions. This, however,
generally restricts the applicability of the method to first-order programs. HO-RPL [Aguirre et al.
2021] extends the previous approach to support higher-order functions by constructing a more
sophisticated semantic model, but general recursion or dynamic allocation and higher-order state
are still unsupported. In a similar vein, some projects verified the privacy of sampling algorithms
and simple mechanisms directly in the denotational semantics of programs [de Medeiros et al.
2025; Sato and Minamide 2025]. In summary, these approaches work well for the verification of
algorithms in isolation, but do not focus on supporting modular program verification.


1.3     Modular Verification for DP Libraries in Clutch-DP
To address the challenges arising from the verification of DP libraries, we introduce the relational ap-
proximate probabilistic higher-order separation logic Clutch-DP. Clutch-DP supports higher-order
functions such as PrivacyFilter and mk_query_cache via quantification over specifications, and
references storing closures as they occur in the implementation of iterators (e.g., AboveThreshold)
via impredicative invariants à la Iris [Jung et al. 2018]. Building on previous relational separation
logics [Gregersen et al. 2024b; Haselwarter et al. 2025], we internalize the privacy budget of DP in
Clutch-DP as a first-class separation logic resource. These privacy credits can be tracked in invari-
ants and interact with the heap and with higher-order functions that consume a privacy budget in
flexible ways. We prove that the usual rules for (sequential) relational separation logic [Frumin
et al. 2021] are sound in the probabilistic setting. To reason about privacy of primitives, we prove
novel relational sampling rules for the Laplacian; in particular, we internalize a proof technique
based on choice couplings [Albarghouthi and Hsu 2017] as a logical rule, which, in particular, is
used in the privacy proof of AboveThreshold. We apply Clutch-DP to a number of case studies
inspired by the challenge problems described above. Our specifications of, e.g., AboveThreshold
are compositional and reusable: we derive the privacy of clients and more complex mechanisms
from the specifications of the building blocks, without referring to implementation details.

   Contributions. To summarize, we make the following contributions.

      (1) A higher-order separation logic for DP which internalizes privacy credits as first-class,
          composable logical resources and which supports heap allocation and higher-order closures.
      (2) New probabilistic sampling rules, including a Laplacian rule that enables selective recovery of
          privacy credits, which can be used to verify examples whose privacy analysis goes beyond
          composition theorems.
      (3) A library of reusable, abstract specifications for common DP primitives (Laplace, AboveThresh-
          old, Sparse Vector Technique, Report-Noisy-Max, Privacy Filters, Caching via Memoization)
          that cleanly separate mechanism proof from client reasoning.
      (4) Client case studies that highlight both expressiveness and reusability of specifications and
          that demonstrate that our approach successfully addresses the challenges outlined above
          (dynamic budget accounting, interactive data analysis, and budget minimization via caching).
      (5) Mechanized proofs: a foundational formalization of the logic and all case studies in the Rocq
          Prover together with an adequacy theorem connecting our logic to standard DP.

   Outline. In §2 we briefly recall the basic notions of DP and define the RandML programming
language used in the remainder of the paper. In §3 we define the Clutch-DP logic and explain how
it relates to DP. In §4 we illustrate reasoning in Clutch-DP via a number of case studies addressing
233:6                                  P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


the challenges set out in §1.1. The soundness of Clutch-DP is addressed in §5. Finally, in §6 we
survey related work, before concluding in §7.3

2     Differential Privacy and Programming Language Preliminaries
We briefly recall the elements of probability theory §2.1 and DP §2.2 we need to refer to, and
formally define the programming language §2.3 used throughout the paper.

2.1     Probability Theory
Since we do not assume a priori that all programs we study terminate, we allow programs to “lose
mass” on diverging runs and define the operational semantics using probability sub-distributions.
   Definition 2.1. A discrete subdistribution  (henceforth simply distribution) on a countable set 𝐴
is a function 𝜇 : 𝐴 → [0, 1] such that 𝑎∈𝐴 𝜇 (𝑎) ≤ 1. The distributions on 𝐴 are denoted by D (𝐴).
                                      Í

    In §2.3, we will define the operational semantics of RandML in terms of the distribution monad.
    Lemma 2.2. The discrete distribution monad induced by D has operations
             ret : 𝐴 → D (𝐴)                                  bind : (𝐴 → D (𝐵)) → D (𝐴) → D (𝐵)
                           (
                      ′      1 if 𝑎 = 𝑎 ′                                           ∑︁
             ret(𝑎) (𝑎 ) ≜                                    bind(𝑓 , 𝜇) (𝑏) ≜           𝜇 (𝑎) · 𝑓 (𝑎) (𝑏)
                             0 otherwise                                            𝑎∈𝐴

We write (𝜇 ≫= 𝑓 ) for bind(𝑓 , 𝜇).

2.2     Differential Privacy
For background information on DP see, e.g., Dwork and Roth [2014] and Cowan et al. [2024].
   Defining privacy. The definition of DP captures the intuition that it is hard to reconstruct
information about any individual in a database from the output of a dp program.
   Definition 2.3. A function 𝑓 : DB → D (𝑋 ) is (𝜀, 𝛿)-differentially private (short: “𝑓 is (𝜀, 𝛿)-dp”)
if Pr 𝑓 (𝑥 ) [𝜙 ] ≤ 𝑒 𝜀 · Pr 𝑓 (𝑦) [𝜙 ] + 𝛿 for all adjacent 𝑥, 𝑦 : DB and all predicates 𝜙 ⊆ 𝑋 . If 𝑓 is (𝜀, 0)-dp
we simply say that 𝑓 is 𝜀-dp.
   A function is thus (𝜀, 𝛿)-dp if it amplifies the probability of any observation 𝜙 by at most 𝑒 𝜀 , or
by more than that with probability at most 𝛿. A small value for 𝜀 and 𝛿 thus means strong privacy
guarantees. The definition of DP is parametrized by a type of databases DB and an adjacency
relation. Clutch-DP can work with any database type and adjacency relation, but a common choice
is to think of a database as a list of rows where each row is a tuple of a fixed size. If the type of
databases comes with a notion of distance 𝑑 DB : DB → R ≥0 we say that two databases 𝑥, 𝑦 are
adjacent if 𝑑 DB (𝑥, 𝑦) ≤ 1. For instance, if 𝑑 DB (𝑥, 𝑦) is the number of rows where 𝑥 and 𝑦 differ, then
adjacency means they only differ in one row.
  Adding noise: the Laplace mechanism. To prove that any program is dp, we need primitives
that add random noise. The prototypical example of a noise mechanism that achieves DP is
the Laplacian distribution. However, since the Laplacian is a continuous distribution on R, an
implementation of a Laplacian sampler would have to work with exact real arithmetic, since
implementations using floats lead to well-known privacy bugs [Mironov 2012].
3 This is the extended version of [Haselwarter et al. 2026a], which differs from the published version by the inclusion of the

full Appendix.
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)                          233:7


   We therefore work with the discrete Laplacian (Fig. 4),                               0.35
                                                                                                   Discrete                  Continuous
the distribution on Z obtained by discretizing the contin-                               0.30      ε=0.7, m=0                 ε=0.7, m=0
uous Laplacian. The discrete Laplacian with scale param-                                 0.25      ε=0.7, m=1                 ε=0.7, m=1




                                                                           Probability
eter 𝜀 and mean 𝑚 has as probability mass function4 [Hsu                                 0.20                           0.167
                                                                                         0.15
2017; Inusah and Kozubowski 2006]:
                                                                                         0.10                           0.083

                1                              ∑︁                                        0.05
      L𝑚𝜀 (𝑣) ≜    · 𝑒 −𝜀 · |𝑣−𝑚 | where 𝑊 ≜        𝑒 −𝜀 |𝑧 |                            0.00                                            (1)
                𝑊                              𝑧 ∈Z                                             −4 −3 −2 −1     0   1   2      3    4       5

 Interpreting adjacency on Z as being at distance at Fig. 4. 𝑚Continuous and discrete Laplacian,
most 𝑐, we have the following result.                with L 0.7 (𝑣) for 𝑣=2 and 𝑚 ∈ {0, 1}, demon-
                                                                          1              0
                                                                           strating 0.7-DP: L 0.7 (2) ≤ 𝑒
                                                                                  0.7                                       · L 0.7 (2) .
  Theorem 2.4 ([Ghosh et al. 2012]). (𝜆 𝑚. L𝑚
                                            𝜀/𝑐 ) :
Z → D (Z) is 𝜀-dp.

  As a direct consequence, given any function 𝑓 : DB → Z such that |𝑓 (𝑥) − 𝑓 (𝑦)| ≤ 1 for adjacent
datasets 𝑥, 𝑦 : DB, the function (𝜆 𝑚. L𝑚
                                        𝜀 ) ◦ 𝑓 : DB → D (Z) is 𝜀-dp.

  Composing DP. Differentially private functions satisfy a number of composition laws that can
help structure and simplify the privacy verification of larger programs.

   Lemma 2.5. DP is stable under post-processing: if 𝑓 : 𝐴 → D (𝐵) is (𝜀, 𝛿)-dp then for any
𝑔 : 𝐵 → 𝐶, the function 𝜆 𝑥 . (𝑓 (𝑥) ≫= 𝜆 𝑦. ret 𝑔(𝑦)) : 𝐴 → D (𝐶) is (𝜀, 𝛿)-dp.

  When two dp functions are composed sequentially, their privacy parameters add up. Due to the
post-processing property this holds even if the later computations can see the results of earlier
computations. We only show the case for two functions, but the lemma directly generalizes to
arbitrary 𝑘-fold composition for 𝑘 ∈ N.

   Lemma 2.6 (Seqential Composition). Let 𝑓 : DB → D (𝐵) be (𝜀 1, 𝛿 1 )-dp and let 𝑔 be a function
𝑔 : DB × 𝐵 → D (𝐶) such that (𝜆 𝑥 . 𝑔(𝑥, 𝑏)) : DB → D (𝐶) is (𝜀 2, 𝛿 2 )-dp for all 𝑏 ∈ 𝐵. Then
𝜆 𝑥 . (𝑓 (𝑥) ≫= 𝜆 𝑏. 𝑔(𝑥, 𝑏)) is (𝜀 1 + 𝜀 2, 𝛿 1 + 𝛿 2 )-dp.

  Another useful composition law holds for functions which increase the distance between inputs
by at most a fixed amount 𝑐 in the following sense.

  Definition 2.7. We say that 𝑓 : 𝐴 → 𝐵 is 𝑐-sensitive (also: “𝑐-stable”) if for all 𝑥, 𝑦 ∈ 𝐴, the
bound 𝑑𝐵 (𝑓 (𝑥), 𝑓 (𝑦)) ≤ 𝑐 ·𝑑𝐴 (𝑥, 𝑦) holds, where the distances 𝑑𝐴 , 𝑑𝐵 are taken with respect to a metric
space structure on 𝐴 and 𝐵.

  Note that if 𝑓 : 𝐴 → 𝐵 is 𝑐-sensitive and 𝑔 : 𝐵 → 𝐶 is 𝑑-sensitive then 𝑔 ◦ 𝑓 is (𝑐·𝑑)-sensitive.
The following metric composition law then generalizes the remark following Theorem 2.4.

   Lemma 2.8. If 𝑓 : DB → Z is 𝑐-sensitive then (𝜆 𝑚. L𝑚
                                                       𝜀/𝑐 ) ◦ 𝑓 : DB → D (Z) is 𝜀-dp.

2.3    The Language: Randomized ML
The RandML language that we consider is an ML-like language with higher-order recursive func-
tions and higher-order state that we extend with an operator Laplace 𝑎 𝑏 𝑚 that samples from the

4 NB: The weight 𝑊 is a geometric series over Z (hence why L
                                                                𝜀 is also called the (two-sided) 𝜀-geometric) with the closed
              𝑒 𝜀 −1     −𝜀 ·|𝑣−𝑚| [Canonne et al. 2020]. We adopt the convention that L𝑚 = ret(𝑚) if 𝜀 ≤ 0.
form L𝑚
      𝜀 (𝑣) = 𝑒 𝜀 +1 · 𝑒                                                                   𝜀
233:8                                   P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


Laplacian with scale (𝑎/𝑏) and mean 𝑚. The syntax is defined by the grammar below.
𝑣, 𝑤 ∈Val ::= 𝑧 ∈ Z | 𝑏 ∈ B | () | ℓ ∈ Loc | rec f x = 𝑒 | (𝑣, 𝑤) | inl 𝑣 | inr 𝑣
 𝑒 ∈ Expr ::= 𝑣 | x | rec f x = 𝑒 | 𝑒 1 𝑒 2 | 𝑒 1 + 𝑒 2 | 𝑒 1 − 𝑒 2 | . . . | if 𝑒 then 𝑒 1 else 𝑒 2 | (𝑒 1, 𝑒 2 ) | fst 𝑒 | . . .
                  ref 𝑒 1 | ! 𝑒 | 𝑒 1 ← 𝑒 2 | Laplace 𝑒 1 𝑒 2 𝑒 3 | . . .
𝐾 ∈ Ectx ::= − | 𝑒 𝐾 | 𝐾 𝑣 | ref 𝐾 | ! 𝐾 | 𝑒 ← 𝐾 | 𝐾 ← 𝑣 | Laplace 𝑒 1 𝑒 2 𝐾 | Laplace 𝑒 𝐾 𝑣 | . . .
                       fin
 𝜎 ∈ State ≜ Loc −⇀Val                𝜌 ∈ Cfg ≜ Expr × State
In RandML, ref 𝑒 1 allocates a new reference containing the value returned by 𝑒 1 , ! 𝑒 dereferences
the location 𝑒 evaluates to, and 𝑒 1 ← 𝑒 2 evaluates 𝑒 2 and assigns the result to the location that 𝑒 1
evaluates to. We may refer to a recursive function value rec f x = 𝑒 by its local name f. The heap is
represented as a (partial) finite map from locations to values, and evaluation happens right to left
as indicated by the evaluation context grammar Ectx.
   The expression Laplace 𝑎 𝑏 𝑚 samples from the discrete Laplacian with scale 𝜀 = 𝑎/𝑏 and mean 𝑚.
To avoid unnecessary complications with adding real numbers to the programming language, we
require the scale 𝜀 to be a rational number. Formally, in RandML, Laplace takes three integers
as input, but to keep our notation free from clutter we will simply write Laplace 𝜀 𝑚 instead of
Laplace 𝑎 𝑏 𝑚 with 𝜀 = 𝑎/𝑏.
   Operational Semantics. Program execution is defined by iterating step : Cfg → D (Cfg),
where step(𝜌) is the distribution induced by the single step reduction of the configuration 𝜌.
The semantics is mostly standard. We first define head reduction and then lift it to reduction in
an evaluation context 𝐾. All non-probabilistic constructs reduce deterministically as usual, e.g.,
step((λ x. 𝑒) 𝑣, 𝜎) = ret(𝑒 [𝑣/x], 𝜎). We write 𝑒 ⇝ 𝑒 ′ if the evaluation is deterministic and holds
independently of the state, e.g., (λ x. 𝑒) 𝑣 ⇝ 𝑒 [𝑣/x] and fst(𝑣 1, 𝑣 2 ) ⇝ 𝑣 1 . The sampling operator
Laplace 𝑎 𝑏 𝑚 reduces according to the Laplacian with scale 𝑎/𝑏 and mean 𝑚, i.e.,
                                                        (
                                                          L𝑚𝑎/𝑏 (𝑣) for 𝑣 ∈ Z,
                        step(Laplace 𝑎 𝑏 𝑚, 𝜎) (𝑣, 𝜎) ≜                                              (2)
                                                          0          otherwise.
  With the single step reduction step : Cfg → D (Cfg) defined, we next define a step-stratified
execution probability exec𝑛 : Cfg → D (Val) by induction on 𝑛:
                        (
                          1 if 𝑒 ∈Val ∧ 𝑒 = 𝑣,
     exec0 (𝑒, 𝜎) (𝑣) ≜
                          0 otherwise.
                        (
                          1                                                                  if 𝑒 ∈Val ∧ 𝑒 = 𝑣,
   exec𝑛+1 (𝑒, 𝜎) (𝑣) ≜ Í                                        ′   ′            ′   ′
                            (𝑒 ′ ,𝜎 ′ ) ∈Expr×State step(𝑒, 𝜎) (𝑒 , 𝜎 ) · exec𝑛 (𝑒 , 𝜎 ) (𝑣) otherwise.

That is, exec𝑛 (𝑒, 𝜎) (𝑣) is the probability of stepping from the configuration (𝑒, 𝜎) to a value 𝑣 in at
most 𝑛 steps. The probability that an execution, starting from configuration 𝜌, reaches a value 𝑣 is
taken as the limit of its stratified approximations, which exists by monotonicity and boundedness:
                                          exec(𝜌) (𝑣) ≜ lim𝑛→∞ exec𝑛 (𝜌) (𝑣)
  The interpretation of programs as distributions induces a natural notion of (𝜀, 𝛿)-DP for RandML
programs. Concretely, if 𝑓 ∈ Expr is a RandML function then for adjacent databases 𝑥, 𝑦 it should
be the case that for all states 𝜎,
                               Prexec( 𝑓 inj(𝑥 ), 𝜎 ) [𝜙 ] ≤ 𝑒 𝜀 · Prexec(𝑓 inj(𝑦), 𝜎 ) [𝜙 ] + 𝛿                              (3)
where inj : DB →Val embeds the type of databases into RandML values (we usually omit inj).
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)      233:9


  Note that in particular 𝑓 = (λ x. Laplace 𝜀 x) is 𝜀-dp in the sense of (3) by the definition of the
operational semantics (2) and Theorem 2.4.

3    Program Logic
In this section, we introduce the Clutch-DP logic, the soundness theorem of Clutch-DP, which
connects it to DP, and the new logical connectives and rules pertaining to the privacy budget
reasoning. Our logic takes inspiration from Approxis [Haselwarter et al. 2025], but we remark that
the underlying model is different, and that it is designed to support our novel reasoning principles
for DP via multiplicative error credits, rules for the Laplacian, and new composition laws.
   The logical connectives. Clutch-DP is built on top of the Iris separation logic framework [Jung
et al. 2018] and inherits many of Iris’s logical connectives, a selection of which is shown below. Most
of the propositions are standard, such as separating conjunction 𝑃 ∗ 𝑄 and separating implication
𝑃 ∗ 𝑄.
       𝑃, 𝑄 ∈ iProp ::= True | False | 𝑃 ∧ 𝑄 | 𝑃 ∨ 𝑄 | 𝑃 ⇒ 𝑄 | ∀𝑥 . 𝑃 | ∃𝑥 . 𝑃 | 𝑃 ∗ 𝑄 | 𝑃                 ∗𝑄|
                                                   ×          +                   ′        ′
                            ℓ ↦→ 𝑣 | ℓ ↦→s 𝑣 | E (𝜀) | E (𝛿) | {𝑃 } 𝑒 ­ 𝑒 {𝑣 𝑣 . 𝑄 } | . . .
Since DP is a relational property, Clutch-DP is a relational program logic that proves properties about
the execution of two programs 𝑒 and 𝑒 ′ . The central logical connective capturing the relationship
between 𝑒 and 𝑒 ′ is the Hoare quadruple:
                                                  {𝑃 } 𝑒 ­ 𝑒 ′ {𝑣 𝑣 ′ . 𝑄 }                                           (4)
Intuitively, this quadruple asserts that under the precondition 𝑃, if the two programs 𝑒 and 𝑒 ′ evaluate
to results 𝑣 and 𝑣 ′ respectively, then the postcondition 𝑄 holds. Since the pre- and postcondition
range over arbitrary Clutch-DP assertions, they can refer to the state or contain nested Hoare
quadruples, which will be useful to write specifications about higher-order functions.
   Logical assertions about the heap come in two versions, one for 𝑒 and one for 𝑒 ′ . The heap
points-to assertion that denotes ownership of location ℓ for the left-hand side program 𝑒 is written
as ℓ ↦→ 𝑣, and ℓ ′ ↦→s 𝑣 ′ denotes ownership of ℓ ′ for the right-hand side program 𝑒 ′ .
   Clutch-DP defines two kinds of resources that are novel with respect to standard Iris and which
are inspired by Approxis [Haselwarter et al. 2025]. The proposition E× (𝜀) asserts ownership of 𝜀
multiplicative privacy credits and E+ (𝛿) similarly asserts ownership of 𝛿 additive privacy credits.
These credits are a logical representation of the privacy budget of DP. Just as reasoning about the
physical state of a program is logically captured by the points-to connective, so is reasoning about
the privacy budget (𝜀, 𝛿) logically expressed via privacy credits.5
    Internalizing privacy. We now have all of the ingredients to define DP in Clutch-DP.
    Definition 3.1. A RandML function f is internally (𝜀, 𝛿)-dp if the following quadruple holds:
               ∀db db′ . Adj(db, db′ ) ∗ E× (𝜀) ∗ E+ (𝛿) f db ­ f db′ {𝑣, 𝑣 ′ . 𝑣 = 𝑣 ′ }
                        
                                                                                                  (5)
   As with Definition 2.3, this notion is parametrized by an adjacency relation Adj(db, db′ ) on
inputs. For instance, we could represent the databases as lists, where each element represents one
entry, and say two databases are adjacent if they differ only in one entry (when considered as
multisets). We abbreviate the Hoare quadruple (5) as (𝜀, 𝛿)-iDP(f) when the adjacency relation is
clear from context, and simply 𝜀-iDP(f) for the case where 𝛿 = 0.
5 Contrary to heaps, the privacy budget pertains to a pair of program executions rather than to the left or right program,

and hence there is no left- and right-hand version of credits; instead, they are shared.
233:10                                  P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


   We call Definition 3.1 internal DP since it is a property of the RandML program f stated entirely in
terms of the program logic. All reasoning about concrete probabilities is abstracted away via the use
of privacy credits. In contrast, the usual external definition of DP (Def. 2.3) for arbitrary functions
and for RandML programs (Eq. (3)) is given in terms of plain mathematics, probabilities, and the
operational semantics. Working with internal DP has two advantages: (1) It uses an expressive
program logic, which allows us to reason about complex programs, whereas reasoning directly
about the operational semantics would be infeasible. (2) We can “pay” some privacy credits to get
an equality in the postcondition of Eq. (5), so that a client of f can simply assume that the results
of (f db) and (f db′ ) are identical instead of having to work with the assumption that they are
distributions at distance (𝜀, 𝛿).
   The precise meaning of Hoare quadruples and privacy credits can be understood through the
following theorem which connects Clutch-DP to DP in the sense of Equation (3).

  Theorem 3.2 (Soundness). If f is internally (𝜀, 𝛿)-dp then f is also externally (𝜀, 𝛿)-dp.

  This theorem is a consequence of the adequacy of the semantic model of Clutch-DP (see §5).

3.1      Relational Separation Logic Rules
The standard rules of relational separation logic as used in, e.g., [Frumin et al. 2021] are also available
in Clutch-DP. For instance, the Frame rule enables local reasoning by framing out 𝑅, and the Bind
rule allows us to focus on sub-programs in evaluation contexts. The usual load and store rules
for heap locations come in a left- and a right version, requiring ownership of the corresponding
points-to connective.


              {𝑃 } 𝑒 ­ 𝑒 ′ {𝑄 }                   {𝑃 } 𝑒 ­ 𝑒 ′ {𝑣 𝑣 ′ . 𝑅}     ∀𝑣 𝑣 ′ . {𝑅} 𝐾 [𝑣] ­ 𝐾 ′ [𝑣 ′ ] {𝑄 }
                         ′
                                      Frame                                                                           Bind
          {𝑃 ∗ 𝑅} 𝑒 ­ 𝑒 {𝑄 ∗ 𝑅}                                      {𝑃 } 𝐾 [𝑒] ­ 𝐾 ′ [𝑒 ′ ] {𝑄 }

{ℓ ↦→ 𝑤 } 𝑤 ­ 𝑒 ′ {𝑄 }                     {ℓ ′ ↦→s 𝑤 } 𝑒 ­ 𝑤 {𝑄 }                          {ℓ ↦→ 𝑤 } () ­ 𝑒 ′ {𝑄 }
                   ′
                             Load-l           ′                  ′
                                                                         Load-r                                          Store-l
{ℓ ↦→ 𝑤 } ! ℓ ­ 𝑒 {𝑄 }                     {ℓ ↦→s 𝑤 } 𝑒 ­ ! ℓ {𝑄 }                        {ℓ ↦→ 𝑣 } ℓ ← 𝑤 ­ 𝑒 ′ {𝑄 }

                              Fig. 5. Excerpt of the non-probabilistic rules of Clutch-DP.

  It is worth noting that the rules in Figure 5 do not mention distributions, despite the fact that the
operational semantics of RandML is probabilistic in general and references can, for instance, store
randomly sampled values. Clutch-DP thus provides a convenient basis for program verification
where reasoning about privacy is integrated as an orthogonal feature while preserving the familiar
rules of relational higher-order separation logic.

3.2      Privacy Credit Laws
The privacy credit resources logically track two non-negative real numbers 𝜀 and 𝛿 corresponding
to the privacy budget. In light of this intuition, one would expect that they support laws such as
sequential composition (Lemma 2.6). Indeed, we can derive an internal version of this law from the
primitive rules pertaining to privacy credits show in Figure 6 together with the structural rules for
RandML in Figure 5.


      E× (𝜀 1 + 𝜀 2 ) ⊣⊢ E× (𝜀 1 ) ∗ E× (𝜀 2 )           E+ (𝛿 1 + 𝛿 2 ) ⊣⊢ E+ (𝛿 1 ) ∗ E+ (𝛿 2 )            E+ (1) ⊢ False
                                                  Fig. 6. Privacy credit laws.
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)           233:11


  Just as in Lemma 2.6, both multiplicative and additive privacy credits can be split into their
summands6 (and recombined). The last rule states that from 1 additive error credit, we can derive
False and hence anything. This makes sense if we recall that 𝛿 models a bound on an inequality
between probabilities in the definition of DP (Def. 2.3), since any probability is bounded by 1, and
hence any program is trivially (𝜀, 1)-dp.
  The fact that the privacy budget is treated like any other separation logic resource and being
able to split the budget enables flexible reasoning about privacy. Privacy credits are animated by
the rules that govern their interaction with the operational semantics of RandML via sampling.

3.3    Rules for Sampling Noise
Privacy credits are consumed by the rules that reason about sampling operations. We introduce a
rule Laplace-shift to reason about a pair of Laplacians, with the same parameter 𝜀 and means
𝑚, 𝑚 ′ . By setting 𝑘 = 0 (and thus, |𝑚 − 𝑚 ′ | ≤ 𝑐), the rule lets us spend E× (𝑐 · 𝜀) to ensure that both
Laplacians return the same result. If, instead, 𝑘 > 0 and 𝑐 = 0 (and thus, |𝑚 − 𝑚 ′ | = 𝑘), the rule
lets us conclude, without consuming privacy, that we will get two samples at distance 𝑘. The rule
combines the two reasoning principles into one:

                                           |𝑘 + 𝑚 − 𝑚 ′ | ≤ 𝑐
                  ×                                                                        Laplace-shift
                  E (𝑐 · 𝜀) Laplace 𝜀 𝑚 ­ Laplace 𝜀 𝑚 ′ {𝑧 𝑧 ′ . 𝑧 ′ = 𝑧 + 𝑘 }
A consequence of Laplace-shift (when 𝑘 = 0) is that Laplace is internally private, i.e., the Clutch-
DP statement 𝜀-iDP(λ x. Laplace 𝜀 x) is derivable. This internalizes DP of the Laplacian (Thm. 2.4).
  Finally, we have the following novel rule for the Laplacian which can be used to recover some
privacy credits. The idea is to partition the results into two groups of outcomes depending on some
threshold 𝑇 . If both Laplacians sample a result above 𝑇 (in fact, above 𝑇 + 1 for the right-hand side)
the privacy credits are consumed. If, on the other hand, both results remain below their respective
thresholds, then the privacy credits can be recovered. This yields a useful reasoning principle for
the Laplacian that is applied, e.g., in the verification of the AboveThreshold mechanism (§4.1.1).

                          |𝑚 − 𝑚 ′ | ≤ 1   𝑇 ∈Z
                                                            ′            Laplace-choice
                                         ′ (𝑇 ≤ 𝑧 ∧ 𝑇 + 1 ≤ 𝑧 ) ∨
   ×                                ′
   E (2𝜀) Laplace 𝜀 𝑚 ­ Laplace 𝜀 𝑚 𝑧 𝑧 . (𝑧 < 𝑇 ∧ 𝑧 ′ < 𝑇 + 1 ∗ × (2𝜀))                   E
Intuitively this rule is sound because it partitions the outcomes into disjoint events such that the
total privacy budget for the two is bounded by the initial privacy budget. Despite its conceptual
simplicity, constructing a sound model that validates Laplace-choice required substantial new
insights in the form of a new composition theorem (see Theorem 5.2).

3.4    Internal Composition Laws
Working in a program logic makes it simple to internalize the various composition laws for DP, as
presented in §2. First, we remark that the internal version of post-processing holds. This is stated
in our logic through the following lemma:

  Lemma 3.3 (Internal post-processing). Let f be internally (𝜀, 𝛿)-dp and assume g is “safe to
execute” in the sense that ∀𝑤 . {True} g 𝑤 ­ g 𝑤 {𝑣 𝑣 ′ . 𝑣 = 𝑣 ′ } holds. Then g ◦ f is internally (𝜀, 𝛿)-dp.

6 NB: Both kinds of privacy credit are split into separating conjunctions by using addition, not multiplication, as the resource

algebra operation. The name “multiplicative privacy credit” for E× (𝜀 ) derives from the multiplicative factor 𝑒 𝜀 in Def. 2.3.
233:12                           P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


  This lemma can be proven entirely within the logic as an immediate consequence of the fact that
Clutch-DP validates the Bind rule. Similarly to the definition of internal DP, we can also recast the
notion of sensitivity (Def. 2.7) in Clutch-DP.
    Definition 3.4. A RandML function f is internally 𝑐-sensitive (𝑐-sens(f)) if the following holds:
                       ∀𝑥 𝑦 : 𝐴. {True} f 𝑥 ­ f 𝑦 {𝑣 𝑣 ′ . 𝑑𝐵 (𝑣, 𝑣 ′ ) ≤ 𝑐 · 𝑑𝐴 (𝑥, 𝑦)}
   As before, the definition is parametrized by two distances at types 𝐴 and 𝐵, which can then
be internalized as distances between values. The internal equivalent of metric composition then
follows.
    Lemma 3.5. ∀ f 𝑐 𝜀. 𝑐-sens(f) ∗ 𝜀-iDP(λ x. Laplace (𝜀/𝑐) (f x)) is derivable in Clutch-DP.

4     Reusable Specs for Privacy Mechanisms
Privacy mechanisms are the primitive building blocks of DP. Mechanisms sample the appropriate
noise for a given data processing task. We give specifications for some widely used mechanisms
and demonstrate that clients can be verified based on these abstract specs.
  Our first example will be the Above Threshold (AT) mechanism, and we will see how to (1)
prove that it satisfies an abstract specification capturing its privacy, (2) build the Sparse Vector
Technique (SVT) from it, and (3) use AT to calculate the clipping bounds required to privately
compute averages over a dataset. Both (2) and (3) use the same abstract specification of AT.
  Besides the case studies presented hereafter, we also verified the privacy of the Report Noisy Max
mechanism, which is of note because—as with AT—its privacy does not follow from composition
laws but requires careful manipulation of the privacy budget and the use of budget- and state-
dependent invariants. Details can be found in §B. We will present the most interesting ideas for
each proof. Full proofs from the rules of Clutch-DP are available in our Rocq formalization.

4.1      Sparse Vector Technique
Suppose we have an incoming sequence of (1-sensitive) queries on a database and a fixed privacy
budget. The Sparse Vector Technique (SVT) allows us to fix a threshold T and release, in a private
manner, whether the result of each query exceeds T or not. The benefit of SVT is that one only has
to spend privacy budget on the “successful” queries which do indeed exceed T and are released; the
results of the queries that do not exceed the threshold can be computed (and discarded) without
incurring a privacy cost. We can thus set in advance a maximum number 𝑁 of successful queries
to be released, and keep answering incoming queries interactively until 𝑁 is reached. The SVT is
usually implemented in terms of the Above Threshold mechanism (AT), which finds a single query
above 𝑇 . SVT then simply runs 𝑁 iterations of AT. The privacy cost of SVT is 𝑁 times the cost of
finding one query above T.
   The SVT is of interest for verification because several buggy privacy proofs have been published
(see Lyu et al. [2017] for a survey). As the survey explains, the SVT is particularly interesting in
the interactive setting; in the non-interactive setting, one can use the Exponential Mechanism
instead and get more accurate results. We explore two subtleties of SVT: how to perform the privacy
analysis of AT, and how to build an interactive algorithm out of AT. The privacy analysis of AT
(and SVT) is challenging because it requires fine-grained reasoning about the privacy budget that
cannot be justified by the sequential composition law alone.
4.1.1 Above Threshold. The Above Threshold mechanism can be used to evaluate queries on a
database until one query returns a result that exceeds a specified threshold T. The implementation
of above_threshold in Figure 7 initializes the noisy threshold T̂ and returns a function to run queries
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:13


interactively. This function receives a query, computes its result, adds additional noise to it and
checks whether the noisy result exceeds T̂.

             let above_threshold ε T = let T̂ = Laplace (ε / 2) T in
                                       let f q db = let x = q db in let y = Laplace (ε / 4) x in T̂ ≤ y
                                       in f
                                     Fig. 7. The Above Threshold mechanism.

   Example 4.1. Suppose we want to privately compute the number of even numbers in a list and
check whether it exceeds a threshold of 3. If we run AT with a high privacy budget (e.g., 𝜀 = 10)
there is very little noise added and we are very likely to disclose the true result and disclose private
information. Concretely, with probability about 92%,
 above_threshold 10 3 (List.count (λ 𝑥 . 𝑥 mod 2 = 0))          [1, 2, 3, 4, 5]      →   false
 above_threshold 10 3 (List.count (λ 𝑥 . 𝑥 mod 2 = 0))          [1, 2, 3, 4, 5, 6]   →   true
  As the value of ε decreases, we are more likely to observe true in the first query or false in the
second, i.e., privacy improves while accuracy deteriorates.
   Our specification (6) captures the idea that above_threshold is interactive: after initialization, the
function f can be used to compare a query to the (noisy) threshold T̂ until a result above T̂ is found,
but queries can be supplied and chosen one by one after observing the result of previous queries.
                      ×
                       E (ε)
                        above_threshold ε T ­ above_threshold ε T
                     
                           ∃𝐴𝑈𝑇 𝐻 . 𝐴𝑈𝑇 𝐻 ∗                                       
                                                                                                      (6)
                                          {𝐴𝑈𝑇 𝐻 ∗ Adj(db, db′ ) ∗ 1-sens(q)} 
                     
                                                                                  
                      ′
                                                                                  
                                                                                   
                       ff .                                     ′
                     
                             ∀ db db′ q. f q db ­ f ′ q db                        
                                                                                   
                                              ′         ′                         
                     
                                         {𝑏 𝑏   . 𝑏 = 𝑏   ∗ if not 𝑏 then 𝐴𝑈𝑇 𝐻 } 
                                                                                   
Let us unpack the specification piece by piece. After initializing the mechanism with a privacy
budget of ε, we obtain a pair of functions f and f ′ , where both functions represent the same
computation but with a priori different randomly sampled values of T̂, as well as an abstract
“authorization token” 𝐴𝑈𝑇 𝐻 . The Hoare quadruple for f, f ′ in the postcondition indicates that so
long as we have the 𝐴𝑈𝑇 𝐻 token, running the functions on a 1-sensitive query q and adjacent
datasets (1) produces the same result for both q db and q db′ , i.e., the computation is private, and
(2) only consumes the 𝐴𝑈𝑇 𝐻 token if q db is above T̂. If the result of the comparison is false,
𝐴𝑈𝑇 𝐻 can be recovered in the postcondition and we can continue to privately look for a query
that exceeds T̂. Note that the initial budget E× (ε) is only spent once at initialization, but we can
still privately run as many queries as it takes to get a result above the threshold.
   Proving Privacy. The proof of the specification (6) proceeds as follows:
    (1) We split E× (ε) into E× (ε/2) ∗ E× (ε/2) and use the first half to pay for the Laplace-shift
        rule with parameters 𝑚 = 𝑚 ′ = T, 𝑐 = 1, 𝑘 = 1. We thus obtain related results T̂, T̂′ for the
        left- and right-hand program such that T̂′ = T̂ + 1. Forcing the two noisy thresholds to be at
        distance 1 rather than equal is a standard “trick” in the analysis of Above Threshold.
    (2) We pick 𝐴𝑈𝑇 𝐻 ≜ E× (ε/2) and use the remaining budget to provide the initial 𝐴𝑈𝑇 𝐻 token.
    (3) We now have to show the specification for
                     f q db ≜ let x = q db in let y = Laplace (ε / 4) x in T̂ ≤ y
                     f ′ q db′ ≜ let x′ = q db′ in let y′ = Laplace (ε / 4) x′ in T̂′ ≤ y′
233:14                           P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


    (4) By sensitivity of q and adjacency of the databases, x and x′ are at distance at most 1.
    (5) By the definition of 𝐴𝑈𝑇 𝐻 , the precondition of the refinement confers us a privacy budget
        of E× (𝜀/2). We use this budget to apply the Laplace-choice rule and partition the outcomes
        (y, y′ ) of the remaining Laplace sampling into two mutually exclusive cases:
          • T̂ ≤ y and T̂′ ≤ y′ . In this case, both of the comparisons return true.
          • y < T̂ and y′ < T̂′ . In this case, both comparisons return false, the rule does not
             consume the privacy budget and we can return 𝐴𝑈𝑇 𝐻 .
        Either way, f and f ′ return the same result 𝑏, and if 𝑏 = false then 𝐴𝑈𝑇 𝐻 is returned too. □
To see that the specification (6) is indeed useful, we will now use it to verify the privacy of the
interactive sparse vector technique.
4.1.2 An interactive Sparse Vector Technique. We prove privacy of the interactive SVT directly
from the abstract specification of the AT mechanism (6). SVT orchestrates repeated invocations of
above_threshold in order to identify the first N of the queries that exceed the threshold T. Unlike
a purely batch-style algorithm, the SVT exposes a streaming interface that allows queries to be
submitted interactively, i.e., depending on the results of earlier queries. This makes the verification
of privacy significantly more challenging, as the set of queries cannot be fixed in advance but
may depend on previously released (noisy) information. In Clutch-DP however, the proof that
sparse_vector is dp is a relatively straightforward consequence of the privacy of above_threshold.
   The implementation in §4.1.2 works as follows. It maintains two pieces of mutable state: a reference
AT to the current Above Threshold instance and a counter that tracks how many additional true
results (i.e., queries that exceed the threshold) may still be released. Each invocation of the returned
function f runs the current above_threshold instance on a new query q and database db, producing
a boolean result b. If b is true and the counter has not yet reached zero, the mechanism consumes ε
privacy credits and reinitializes AT with a fresh Above Threshold instance. Otherwise, the counter
and function reference remain unchanged. The caller may then use the result b to decide which
query to issue next.

 let sparse_vector ε T N =                                       let SVT_stream ε T N QS db =
      let AT = ref (above_threshold ε T) in                          let f = sparse_vector ε T N in
      let counter = ref (N − 1) in                                   let rec iter i bs =
      let f q db = let b = (! AT) q db in                               if i = N then List.reverse bs
                   if ! counter > 0 && b then                            else let q = QS bs in
                      ( counter ← (! counter − 1) ;                           let b = f q db in
                         AT ← above_threshold ε T ) ;                         iter (if b then (i + 1) else i) (b :: bs)
                   b                                                 in iter 0 []
      in f
                        Fig. 8. The Sparse Vector Technique and a streaming client.

 The specification (7) formalizes the intuition that the interactive SVT behaves like a private state
machine that can be queried multiple times while consuming a fixed privacy budget.
               E (N · ε)
               ×

                 sparse_vector ε T N ­ sparse_vector ε T N
              
                    ∃ 𝑖𝑆𝑉𝑇 . 𝑖𝑆𝑉𝑇 (N) ∗                                                
                                                                                                 (7)
                                     {𝑖𝑆𝑉𝑇 (𝑛 + 1) ∗ Adj(db, db′ ) ∗ 1-sens(q)} 
              
                                                                                       
               ′
                                                                                       
                                                                                        
                ff .                                        ′
              
                       ∀ db db′ q 𝑛. f q db ­ f ′ q db                                 
                                                                                        
                                          ′         ′                                  
              
                                    {𝑏  𝑏   . 𝑏 = 𝑏   ∗ 𝑖𝑆𝑉𝑇 (if 𝑏 then 𝑛 else 𝑛 + 1)} 
                                                                                        
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:15


Initially, the mechanism owns a total privacy resource of E× (N · ε), corresponding to N possible
above-T releases. The abstract token 𝑖𝑆𝑉𝑇 (𝐾) in the postcondition tracks the remaining number 𝐾
of true results we can release. The returned function f satisfies the nested quadruple: if we own at
least 𝑖𝑆𝑉𝑇 (1), we can run a 1-sensitive query on adjacent databases and ensure we get the same
result; if the result is true (i.e., the query exceeds the threshold), we decrease 𝑖𝑆𝑉𝑇 by 1, otherwise
we get back our initial token. This specification thus captures both the privacy accounting and the
interactive behavior of SVT: the mechanism remains private for any adaptively chosen sequence of
1-sensitive queries until the allotted number N of positive releases has been exhausted.
   Notably, the proof of this specification treats AT abstractly and relies only on its specification (6),
not its implementation, which gives us a more modular analysis. The proof relies on keeping a
simple invariant over the counter, the AT reference and the remaining privacy budget.
   To summarize, this implementation and our verification of it has several noteworthy features:
      • the SVT is a client of AT via an abstract specification,
      • its interactive interface is specified through nested Hoare quadruples, and
      • it requires storing a private higher-order function in a reference.
   Next, we demonstrate that our specifications are expressive enough for reuse by different clients.
4.1.3 SVT Client: Streams of Queries. The standard textbook account of SVT [Dwork and
Roth 2014] presents it as an algorithm that takes in a stream of queries QS and produces a list of
booleans 𝑏𝑠 where 𝑏𝑖 indicates whether the 𝑖-th query was above the noisy threshold. The stream
is represented as a (possibly stateful) function that produces a new query on each invocation, and
interactivity is modeled by the fact that each time a new query is requested, QS gets access to the
booleans 𝑏𝑠 resulting from the preceding queries.
   We can directly prove that the implementation SVT_stream (§4.1.2) is private by applying the
generic specification for SVT. A user of SVT_stream only has to satisfy the textbook assumption
that all of the queries are indeed 1-sensitive. The privacy reasoning is encapsulated in (7).
4.1.4 Above Threshold Client: auto_avg. As a last application of the Above Threshold mecha-
nism, we analyze the auto_avg client that privately computes the average of a dataset. This example
is taken from the online textbook [Near and Abuah 2021, Chapter 10].
   The fact that both sparse_vector and auto_avg can both be verified against the same abstract
interface for above_threshold is good evidence that our specifications are indeed reusable and can
be used to verify libraries without having to worry about implementation details.

 let auto_avg bnds ε db =                                         let mk_query b db =
    let bound = get_clip_bound bnds ε db in                          (clip_sum b db) − (clip_sum (b + 1) db)
    let sum = clip_sum bound db in                                let clip_sum bound db =
    let sumnoisy = Laplace (ε / bound) sum in                        List.sum (List.clip bound db)
    let countnoisy = Laplace ε (List.length db) in
    sumnoisy / countnoisy                                         let AT_list ε T db qs =
                                                                     let AT = above_threshold ε T in
 let get_clip_bound bnds ε db =                                      List.find (λ (bound, q). AT q db) qs
    let qs = List.map (λ b. (b, mk_query b)) bnds in
    let (bound, _) = AT_list ε 0 db qs in
    bound
                            Fig. 9. Privately computing the average of a list of data.
  To privately compute the average of a dataset it is not enough to first compute the average and
then add ε Laplacian noise for a fixed ε, as this may leak information about the size of the dataset.
The noise has to be calibrated to the largest element—but that value in itself is private information!
233:16                                P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


  The solution adopted in the implementation of auto_avg in Figure 9 is to “clip” the elements of
the database to lie in a bounded range [0, 𝐵]. If two adjacent databases are clipped to the same
bound, their sum can differ by at most 𝐵. In other words, we can prove that clip_sum 𝐵 is internally
𝐵-sensitive. We can apply internal metric composition (Lem. 3.5) to show that computing sumnoisy
by adding to the clipped sum Laplacian noise with scale (ε/𝐵) is ε-private. Therefore, auto_avg
achieves (3·ε)-DP, where the budget is divided equally between the call to get_clip_bound and the
two calls to Laplace:

        E (3 · ε) ∗ Adj(db, db′ ) auto_avg bnds ε db ­ auto_avg bnds ε db′ {𝑥 𝑥 ′ . 𝑥 = 𝑥 ′ }
        ×

   The utility of auto_avg stems from carefully choosing 𝐵. Given a list of candidate bounds bnds
we can do this privately via the AT mechanism. The function get_clip_bound to finds the first value
b in bnds such that the sum of elements in db stops increasing if the clipping bound is relaxed from
b to b + 1. Testing this for all values in bnds via mk_query is 1-sensitive. Therefore we can directly
apply the specification (6) for above_threshold to derive that get_clip_bound is ε-dp.

4.2      Privacy Filters
A common implementation technique for DP in general-purpose programming languages is to
explicitly track the remaining privacy budget as a program variable. At the beginning of a data
analysis, this variable is initialized to the global privacy budget 𝜀, and it must remain non-negative
throughout the program execution. So long as care is taken to decrement the budget every time
(noisy) data is released, the whole data analysis is 𝜀-private. To ensure that these rules are respected,
the management of the privacy budget is commonly encapsulated in a privacy filter, a higher-order
function that runs a computation only if there is sufficient budget for it. This programming pattern
provides a separation of concerns: if the privacy analysis of the individual computations is correct,
and the filter is correctly implemented, then the entire computation is private. This allows us to
verify the different components (privacy filter and mechanisms) modularly.

let privacy_filter εbudget =                 let adaptive_count εcoarse εprecise T εbudget predicates db =
    let εrem = ref εbudget in                    let try_run = privacy_filter εbudget in
    let try_run εcost f =                        List.map (λ pred. let nexact = List.count pred db in
         if ! εrem < εcost then                                      let g _ = Laplace εprecise nexact in
            None                                                     let f _ = let ncoarse = Laplace εcoarse nexact in
         else                                                                  let nprecise = if T < ncoarse
            εrem ← ! εrem − εcost ;                                               then try_run εprecise g
            Some (f ())                                                           else None in
    in try_run                                                                 (ncoarse, nprecise )
                                                    in try_run εcoarse f)
                                                    predicates
                       Fig. 10. Implementations of a Privacy Filter and Adaptive Count.

   The implementation privacy_filter in Figure 10 works as follows. Upon initialization it allocates
a reference that tracks the remaining privacy budget and returns a closure try_run that can be used
to run private computations in an interactive manner. If a client tries to run a computation with
cost exceeding the remaining budget, try_run does not run the computation, otherwise it decreases
the budget by the cost, runs the computation, and returns the result.
   For the sake of simplicity we present a privacy filter that only tracks the 𝜀-budget, but the method
directly generalizes to (𝜀, 𝛿)-privacy filters.
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:17


4.2.1 Proving Privacy of Privacy Filters. The high-level intuition for the privacy filter is that it
should never exceed the budget that was initially set up so long as any client that calls try_run εcost f
ensures that f is indeed εcost -dp. This intuition is captured by the following specification.
                           E εbudget
                          ×          

     ∀ εbudget .            privacy_filter εbudget ­ privacy_filter εbudget                           (8)
                         {try_run try_run′ . ∃ 𝑖𝑃𝐹 . 𝑖𝑃𝐹 ∗ try_run-spec}
where try_run-spec is defined as
                          (                                                                             )
                           𝑖𝑃𝐹 ∗ 𝐼𝑛𝑣 f
                             ∗ E× (εcost ) ∗ 𝑖𝑃𝐹 ∗ 𝐼𝑛𝑣 f f () ­ f ′ () {𝑣 𝑣 ′ . 𝑣 = 𝑣 ′ ∗ 𝑖𝑃𝐹 ∗ 𝐼𝑛𝑣 f }
                                

    ∀ εcost f f ′ 𝐼𝑛𝑣 f .   try_run εcost f ­ try_run′ εcost f ′                                                    (9)
                          {𝑏 𝑏 ′ . 𝑏 = 𝑏 ′ ∗ 𝑖𝑃𝐹 ∗ 𝐼𝑛𝑣 f }
The existentially quantified 𝑖𝑃𝐹 token in the postcondition of (8) represents a client’s ability to exe-
cute computations privately via try_run. The specification (9) defines the behavior of try_run εcost f.
Assuming that for a privacy cost of εcost the functions f and f ′ produce equal results and maintain an
invariant 𝐼𝑛𝑣 f , calling them through try_run (and try_run′ respectively) satisfies the same invariant
regardless of whether there actually is enough budget left to execute f. Since f may itself contain
calls to try_run, the specification for (f, f ′ ) has access to the 𝑖𝑃𝐹 token. We give a simple application
of this expressivity in the form of nested calls to the privacy filter in §4.2.2.
   The proof of the specification in Clutch-DP is straightforward. We define the token 𝑖𝑃𝐹 as
                                    ∃𝜀. E× (𝜀) ∗ εrem ↦→ 𝜀 ∗ ε′rem ↦→s 𝜀 .
The link between the logical resource representing ownership of the error budget and the program
state tracking the remaining budget allows us to conclude that the call to Some (f ()) in the definition
of try_run is only executed when sufficient privacy budget remains to satisfy the precondition of
(f, f ′ ) in (9), and hence the invariant 𝐼𝑛𝑣 f is satisfied. In case try_run decides that the budget is
insufficient for f, the invariant is trivially preserved.
   The power of this specification for privacy_filter lies in the fact that a client does not have to
perform any privacy accounting or reasoning whatsoever for try_run εcost f! We can conveniently
combine library functions to build a private f and run it without having to worry whether we still
have enough budget: the filter ensures that the initial budget is never exceeded.
4.2.2 Client: Adaptive Counting. Another advantage of implementing DP through privacy
filters is that it allows the data analyst to decide dynamically where the privacy budget should be
spent, i.e., the way the budget is spent can adapt to the results of prior analyses. This is especially
useful in exploratory data analysis when it is unclear, a priori, what values the dataset ranges over.
    The example adaptive_count in Figure 10 employs a form of adaptivity to privately count the
number of elements of db that satisfy each of the tests in the list of predicates. First, a cheaper but
less precise count is performed, consuming εcoarse privacy credits. Only if this yields a promising
result that exceeds a threshold T, a more precise analysis is performed for an additional larger
budget of εprecise . The result of adaptive_count is thus a numeric estimate for each predicate, with
a more precise value for a few “important” candidates.
    A conservative privacy analysis would have to assume a worst-case cost of length(predicates) ·
(εcoarse + εprecise ) even if many of the coarse counts may in practice not exceed the threshold. By
employing a privacy filter, we can instead fix a budget εbudget that we want to allocate to this
analysis task and try to run the analysis so long as the filter has enough budget left. If only a few of
233:18                           P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


the data entries exceed T, this allows to count many more predicates than the conservative analysis
without a privacy filter.
  In Clutch-DP, we can prove that adaptive_count is εbudget -dp from the specification (8) because f
and g meet the precondition of try_run, as they consume a budget of εcoarse and εprecise respectively.

4.3      Caching Techniques for DP
Interactive analysis with data-dependent queries is common in real-world workloads for DP. This
poses a challenge for DP frameworks because it makes it impossible to statically avoid repeated
evaluation of certain queries, say, by refactoring code that requires the same result, and hence
repeated queries inflate the privacy cost unnecessarily. This problem can be solved with a query
cache that memoizes the results of a query on first execution and reuses this result upon repetition.
One would hope that reusing a noisy result in a repeated query should be “for free” and consume no
privacy budget. However, the privacy analysis of such a memoization method is subtle, because the
privacy cost of a query depends on the history of queries, which is highly non-local information.

 let mk_query_cache add_noise db =                     let map_cache add_noise qs db =
     let cache = Map.init () in                            let run_cache =
     let run_cache q =                                        mk_query_cache add_noise db in
         match Map.get cache q with                        List.map run_cache qs
         | Some x ⇒ x
         | None ⇒ let x = add_noise q db in
                      Map.set cache q x ;
                      x
     in run_cache
                             Fig. 11. Implementations of a cache and a client.
   In this section, we reason about the privacy of the caching method introduced in Figure 3, which
we implement in RandML through the algorithm shown in Figure 11. Our formalization crucially
relies on our logic being able to support higher-order functions, local state, and a resource-based
representation of the privacy budget.
4.3.1 Cache spec: repeated queries are free. Upon initialization, mk_query_cache allocates a
mutable map cache and returns a closure run_cache that stores and looks up noisy query results
in cache. This is reflected in (10) as the existentially quantified iC(𝑀𝑐𝑎𝑐ℎ𝑒 ) resource. Initially, the
map 𝑀𝑐𝑎𝑐ℎ𝑒 is empty, but it can be updated via run_cache as we will see next.
                 {Adj(db, db′ )}
                   mk_query_cache add_noise db ­ mk_query_cache add_noise db′                                       (10)
                 {run_cache run_cache′ . ∃iC. iC(Map.empty) ∗ spec-cached ∗ spec-fresh}
where spec-fresh is defined as
                 q ∉ dom(𝑀𝑐𝑎𝑐ℎ𝑒 ) ∗ E× (𝜀) ∗ E+ (𝛿) ∗ (𝜀, 𝛿)-iDP(add_noise q) ∗ iC(𝑀𝑐𝑎𝑐ℎ𝑒 )
               

 ∀ 𝑀𝑐𝑎𝑐ℎ𝑒 q .     run_cache q ­ run_cache′ q                                                                        (11)
               {𝑣 𝑣 ′ . 𝑣 = 𝑣 ′ ∗ iC(𝑀𝑐𝑎𝑐ℎ𝑒 [q ↦→ 𝑣])}
and spec-cached is defined as
                 {q ∈ dom(𝑀𝑐𝑎𝑐ℎ𝑒 ) ∗ iC(𝑀𝑐𝑎𝑐ℎ𝑒 )}
 ∀ 𝑀𝑐𝑎𝑐ℎ𝑒 q .       run_cache q ­ run_cache′ q                                                                      (12)
                 {𝑣 𝑣 ′ . 𝑣 = 𝑣 ′ ∗ iC(𝑀𝑐𝑎𝑐ℎ𝑒 ) ∗ 𝑀𝑐𝑎𝑐ℎ𝑒 [q] = 𝑣 }
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:19


The specification (11) describes the behavior of (run_cache q) on a query that has not been memo-
ized yet. It requires that add_noise should indeed run q under (𝜀, 𝛿)-iDP and assumes ownership of
enough privacy credits to pay for this execution. Furthermore, it requires ownership of iC(𝑀𝑐𝑎𝑐ℎ𝑒 )
for the current internal state of the cache. In the postcondition, we recover iC where 𝑀𝑐𝑎𝑐ℎ𝑒 is
updated with the result of the noisy query.
   The intuition that repeated queries should be free is formalized in (12): if q is in the cache then
no privacy credits are consumed for executing it under run_cache.
4.3.2 A cache client. A simple application is map_cache (Figure 11), which employs the cache to
run add_noise on a list of queries qs. We can prove that the privacy cost of map_cache is (𝑘𝜀, 𝑘𝛿)
where (𝜀, 𝛿) is the privacy cost of the add_noise mechanism and 𝑘 = |{q ∈ qs}| is the number of
unique queries in qs. The proof of (13) follows directly from the abstract specification (10).
           (∀q ∈ qs. (𝜀, 𝛿)-iDP(add_noise q)) ∗ (𝑘𝜀, 𝑘𝛿)-iDP(map_cache add_noise qs)                              (13)
Without caching, the privacy cost would have to be multiplied by List.length(qs) instead of 𝑘.

5   Soundness: A Model of Clutch-DP
In this section we give an overview of the model behind Clutch-DP and its adequacy theorem. A
detailed account can be found in §A.
   Our program logic is based around the notion of (𝜀, 𝛿)-approximate coupling [Barthe et al. 2016a;
Sato 2016]:
   Definition 5.1. Let 𝐴, 𝐵 be countable types, and Φ ⊆ 𝐴 × 𝐵 a relation. Given two real-valued
parameters 0 ≤ 𝜀, 𝛿, we say that there is an (𝜀, 𝛿)-approximate Φ−coupling between distributions
𝜇1 : D (𝐴), 𝜇2 : D (𝐵) if, for any real-valued random variables 𝑓 : 𝐴 → [0, 1], 𝑔 : 𝐵 → [0, 1] such that
∀(𝑎, 𝑏) ∈ Φ, 𝑓 (𝑎) ≤ 𝑔(𝑏), the following holds : E𝜇1 [ 𝑓 ] ≤ exp(𝜀) · E𝜇2 [𝑔 ] + 𝛿. We denote the existence
of such a coupling by 𝜇 1 Φ (𝜀,𝛿 ) 𝜇2 .
   The model is similar in spirit to that of Approxis [Haselwarter et al. 2025], which can be seen as
based on a notion of (0, 𝛿)-approximate coupling. Crucially, we prove a novel choice composition
theorem, that is key to some of our proof rules, in particular Laplace-choice. This is heavily
inspired by choice couplings [Albarghouthi and Hsu 2017], but it really shines in our setting, since
we have a resourceful treatment of the privacy budget.
  Theorem 5.2. Let 𝜇1 : D (𝐴), 𝜇 2 : D (𝐵), 𝑓 : 𝐴 → D (𝐴′ ), 𝑔 : 𝐵 → D (𝐵 ′ ). Assume we have a
predicate Ξ ⊆ 𝐴, and Φ1, Φ2 ⊆ 𝐴 × 𝐵, Ψ ⊆ 𝐴′ × 𝐵 ′ , with Φ1, Φ2 disjoint in the sense that, ∀𝑎, 𝑎 ′, 𝑏.𝑎 ∈
Ξ ∧ 𝑎 ′ ∉ Ξ ⇒ ((𝑎, 𝑏) ∉ Φ1 ∨ (𝑎 ′, 𝑏) ∉ Φ2 ). Assume further that:
     (i) 𝜇1 Φ1 (𝜀1,𝛿1 ) 𝜇2
    (ii) 𝜇 1 Φ2 (𝜀2,𝛿2 ) 𝜇2
                                                                    ′ ′
   (iii) For all 𝑎, 𝑏 such that 𝑎 ∈ Ξ and (𝑎, 𝑏) ∈ Φ1 , 𝑓 𝑎 Ψ (𝜀1,𝛿1 ) 𝑔 𝑏.
                                                                   ′ ,𝛿 ′ )
   (iv) For all 𝑎, 𝑏 such that 𝑎 ∉ Ξ and (𝑎, 𝑏) ∈ Φ2 , 𝑓 𝑎 Ψ 2 2 𝑔 𝑏.
                                                                (𝜀

  Then, (𝜇 1 ≫= 𝑓 ) Ψ (𝜀,𝛿 ) (𝜇2 ≫= 𝑔), where 𝜀 ≜ max(𝜀 1 + 𝜀 1′ , 𝜀 2 + 𝜀 2′ ) and 𝛿 ≜ 𝛿 1 + 𝛿 2 + max(𝛿 1′ , 𝛿 2′ )
  This statement might appear cryptic at first. The idea is that, when proving a coupling for the
composed computations 𝜇1 ≫= 𝑓 , 𝜇2 ≫= 𝑔, one can choose between two different couplings for 𝜇1, 𝜇2 ,
each with a different cost 𝜀 1 or 𝜀 2 , and then also spend a different privacy cost 𝜀 1′ or 𝜀 2′ for the
continuations depending on whether the value sampled from 𝜇 falls inside or outside Ξ (note
however, that the additive cost 𝛿 1 + 𝛿 2 for the first step must be paid in any case).
  For instance, the proof of Laplace-choice for parameters 𝜀,𝑇 , 𝑚, 𝑚 ′ essentially uses Theorem 5.2
with Ξ(𝑧) ≜ (𝑇 ≤ 𝑧), 𝜀 1 ≜ 2𝜀, 𝜀 1′ ≜ 0, 𝜀 2 ≜ 0, and 𝜀 2′ ≜ 2𝜀. The coupling (i) comes from Laplace-
shift with 𝑘 = 1, which (together with 𝑧 ∈ Ξ) ensures the condition Φ1 ≜ (𝑇 ≤ 𝑧 ∧ 𝑇 + 1 ≤ 𝑧 ′ )
      233:20                            P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


                                                                                                      al
                                                                                                  loc HO            ns
                                                                                         l ,        , ■       c tio
                                                                                      b a          r
                                                                                                         fu n
                                                                                  glo         rde                                                  p.
                                                         gy                     # rst-o rder
                                                                                G                                           on                   om e
                                                     olo                                         o                    n iti                    c          ive
                                                                                                                                         ed ond ptiv ract
                                                    d                            △ fi          -
                                                tho                          t e        h er                   d  efi               i fi         a    e
                                                                                      g                                           r        y
                                             Me                          Sta      Hi                      DP                    Ve Be         Ad Int
Fuzz [Reed and Pierce 2010]                 lin. types                   #                                𝜀                    # # #               #
Fuzz𝜖𝛿 [de Amorim et al. 2021]              lin. typ., path adj.         #                             (𝜀, 𝛿 )                 # # #               #
DFuzz [Gaboardi et al. 2013]                lin. dep. types              #                                𝜀                    # # #               #
AFuzz [Winograd-Cort et al. 2017]           dyn. typ. + priv. filter     #                             (𝜀, 𝛿 )                 # #                 #
Fuzzi [Zhang et al. 2019]                   Fuzz-like + apRHL            #        #                    (𝜀, 𝛿 )                 #             #     #
Duet [Near et al. 2019]                     sens. + priv. types          #               (𝜀, 𝛿 ), RDP, (z/t)CDP # # #                              #
Jazz [Toro et al. 2023]                     ctxt’l sens. + priv. typ.    #                   (𝜀, 𝛿 ), RDP, zCDP                # # #               #
DPella [Lobo-Vesga et al. 2020]             eDSL dep. types              #                                𝜀                    # # #               #
Solo [Abuah et al. 2022]                    eDSL dep. types              #                         (𝜀, 𝛿 ), RDP                # # #               #
Spar [Lobo-Vesga et al. 2024]               eDSL dep. types              #                                𝜀                    # # #               #
HOARe2 [Barthe et al. 2015b]                rel. refinement types        #                             (𝜀, 𝛿 )                 # # #               #
LightDP [Zhang and Kifer 2017]              types + annot.              G
                                                                        # △ #                             𝜀                    #             #     #
SampCert [de Medeiros et al. 2025]          semantic                     #                        (𝜀, 𝛿 ), zCDP                              #     #
DP/Isabelle [Sato and Minamide 2025]        semantic                     #        #                    (𝜀, 𝛿 )                               #     #
apRHL+ [Barthe et al. 2015a, 2016a, 2012]   rel. prob. Hoare logic      G
                                                                        # △ #                          (𝜀, 𝛿 )                 #             #     G
                                                                                                                                                   #
HO-RPL [Aguirre et al. 2021]                rel. prob. Hoare logic      G
                                                                        # △                            (𝜀, 𝛿 )                 # # #               G
                                                                                                                                                   #
Clutch-DP                                   rel. prob. sep. logic         ■                            (𝜀, 𝛿 )
      Fig. 12. Comparison of DP systems. “Beyond comp.” = support for mechanisms whose DP goes beyond
      composition laws (e.g., SVT, RNM).


      in the postcondition of Laplace-choice for a privacy cost of 𝜀 1 = 2𝜀 since |𝑘 + 𝑚 − 𝑚 ′ | ≤ 2. The
      coupling (ii) comes from Laplace-shift with 𝑘 ≜ 𝑚 ′ − 𝑚, which (together with 𝑧 ∉ Ξ) ensures the
      condition Φ2 ≜ (𝑧 < 𝑇 ∧ 𝑧 ′ < 𝑇 + 1) in the postcondition of Laplace-choice for a privacy cost of
      𝜀 2 = 0. Since the coupling for (ii) does not consume any privacy credits, we recover 𝜀 2′ = 2𝜀 in the
      second branch of the postcondition of Laplace-choice.
          In the model of Clutch-DP, this composition is possible at every execution step, and realized
      through the way separation logic resources tracking the budgets are threaded through the execution.
          There is a tight connection between couplings and DP: a function 𝑓 : DB → D (𝑋 ) is (𝜀, 𝛿)-dp
      iff for any adjacent inputs 𝑏, 𝑏 ′ : DB, we have 𝑓 𝑏 (=) (𝜀,𝛿 ) 𝑓 𝑏 ′ . With this connection in mind, we
      can now state the adequacy theorem of Clutch-DP.

         Theorem 5.3. Let 𝑓 , 𝑓 ′ be two RandML functions and Φ, Ψ : Val ×Val → Prop. If

                                     Φ(𝑤, 𝑤 ′ ) ∗ E+ (𝛿) ∗ E× (𝜀) 𝑓 𝑤 ­ 𝑓 ′ 𝑤 ′ {Ψ}
                                   


      holds in Clutch-DP then, for any initial states 𝜎, 𝜎 ′ , we have exec(𝑓 𝑤, 𝜎) Ψ (𝜀,𝛿 ) exec(𝑓 ′ 𝑤 ′, 𝜎 ′ ).

         By instantiating Φ with adjacency and Ψ with equality, we recover Theorem 3.2 as a corollary.
         Internally, the Hoare quadruples are defined in terms of a primitive, unary notion of weakest
      precondition (WP), where the right-hand side program is represented as a separation logic re-
      source [Frumin et al. 2021; Gregersen et al. 2024b; Haselwarter et al. 2025]. Validity of the WP is
      defined by guarded induction on the program execution, establishing an approximate coupling
      at each step, and finally composing all the couplings into a coupling for the full execution. Each
      program logic rule is then proven sound w.r.t. the definition of the WP. In particular, all standard
      separation logic rules for the deterministic fragment of RandML can be re-established. We refer the
      reader to the supplementary material for more details.
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:21


6   Related Work
   Types for DP. A wide range of type systems ensuring DP have been developed. Fuzz [Reed
and Pierce 2010] and its variants track function sensitivity via linear types and rely on metric
composition to statically ensure pure DP for a probabilistic λ-calculus. DFuzz [Gaboardi et al. 2013]
integrated linear and dependent types to improve sensitivity analysis. Fuzz𝜖𝛿 [de Amorim et al. 2021]
extends Fuzz with support for (𝜀, 𝛿)-DP. The two-level type system of Adaptive Fuzz [Winograd-
Cort et al. 2017] enhances static typing by integrating a trusted privacy filter into the language
runtime. The system allows programming with adaptive composition by dynamically type-checking
programs during execution and composing them according to the privacy filter. In Clutch-DP,
privacy filters are just regular programs that can be verified in their own right.
   Duet [Near et al. 2019] is a linear type system supporting various notions of DP by a separation of
the language into a sensitivity and a privacy layer which interact through bespoke composition laws
that restrict rescaling, which limits the kinds of higher-order functions that can be type-checked.
Jazz [Toro et al. 2023] lifts some of these restrictions by introducing latent contextual effect types.
HOARe2 [Barthe et al. 2015b] encodes sensitivity and privacy information in relational refinement
types for a pure calculus.
   The DPella system [Lobo-Vesga et al. 2020], Solo [Abuah et al. 2022], and Spar [Lobo-Vesga et al.
2024] leverage extensions to Haskell’s type system to encode sensitivity (or distance) information
via dependent types instead of linear types.
   None of these systems support mutable state, or the verification of programs whose privacy
requires advanced budget management instead of following directly from composition laws.
   LightDP [Zhang and Kifer 2017] employs a dependent relational type system to bound distances
in program variables. With SMT-backed type inference, LightDP can verify DP for some mechanisms
beyond composition laws (e.g., non-interactive SVT), but the method does not extend to advanced
language features or flexible privacy budget analysis as used, e.g., in Report Noisy Max.
   Logics for DP. The apRHL(+) program logics [Barthe et al. 2015a, 2016a, 2012] can prove (𝜀, 𝛿)-
DP for programs written in a first-order while-language. Reasoning about basic mechanisms is well
supported in apRHL, and it has been applied to advanced mechanisms such as SVT. Verification
of interactive DP is supported through a specialized rule for adversaries that can interact with
mechanisms through fixed patterns. In apRHL, adversaries are programs subject to a number of
side-conditions; in contrast, our model of interactive computations via higher-order functions does
not come with syntactic restrictions and can be composed modularly. For instance, we can recover
the apRHL model of SVT used by Barthe et al. [2016a, Fig. 1] through our streaming SVT (§4.1.3)
by instantiating the stream of queries QS with the adversary A of loc. cit. The privacy budget in
apRHL is handled via a grading on judgments which offers less flexibility compared to Clutch-DP’s
privacy credits. On the other hand, working with a concrete denotational model allowed the authors
of [Barthe et al. 2016a] to extend apRHL with support for “advanced composition” in the sense of
[Dwork and Roth 2014, §3.5.2] and derive the corresponding bounds for SVT, which is not possible
in Clutch-DP.
   A variant of the EasyCrypt prover supports apRHL but the implementation of the apRHL rules
are part of the trusted code base, whereas the rules of Clutch-DP are proven sound in a proof
assistant. During the development of our case studies we found a bug in the Laplace sampling
rule of EasyCrypt7 which has accidentally been exploited in a user-contributed privacy proof of
Report Noisy Max. Our foundational approach would have prevented us from introducing such an
erroneous rule. Proof search for coupling-based proofs of DP for first-order programs was studied

7We have disclosed the bug to the EasyCrypt team.
233:22                         P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


in [Albarghouthi and Hsu 2017]. Their definition of choice couplings inspired our Laplace-choice
rule.
   Fuzzi [Zhang et al. 2019] integrates an apRHL-style logic with a Fuzz-inspired sensitivity- and
privacy-logic; working at the intersection of the languages of the two systems, it does not support
mutable state or higher-order functions.
   The HO-RPL logic extends the ideas from apRHL to support higher-order functions and continu-
ous distributions by giving a denotational semantics of programs in Quasi-Borel Spaces, but it is
not known how to extend this approach to other language features that our challenge problems
require such as dynamic allocation or higher-order store.
   The Isabelle/HOL formalization of DP [Sato and Minamide 2025] develops the mathematical
theory of DP in the continuous setting. Working directly in a measure-theoretic semantics, they
prove privacy of Report Noisy Max, stating however that “the formal proof is quite long”. It is
unclear how to scale their approach to a language like RandML.
   The SampCert project [de Medeiros et al. 2025] formalized DP in the Lean prover by interpreting
a shallow embedding of a while-like language in the same kind of denotational semantics that
apRHL is based on. Rather than assuming that the language has a primitive that samples from
the Laplacian, SampCert proves that an efficient implementation of a sampler realizes the Laplace
distribution. Their approach is particularly well-suited to carrying out the low-level probabilistic
reasoning and focuses less on building modular systems. SampCert formalizes non-interactive
variants of AT and SVT.
   Separation logic. Several probabilistic separation logics exist, but only Clutch-DP supports
reasoning about DP. The Approxis [Haselwarter et al. 2025] relational separation logic supports
reasoning about approximate program equivalence. Their notion of 𝛼-approximate equivalence
amounts to (0, 𝛼)-dp in our setting, i.e., our additive privacy credits correspond to their “error
credits”. Approxis can prove cryptographic security or correctness of samplers but cannot express
DP. Approxis includes specific provisions for reasoning about samplers such as the spec-coupl-
err-1 clause and “expectation-preserving composition” that are not present in our model. Approxis
also develops a logical relation model for contextual equivalence. We believe that Clutch-DP can be
extended to support these features, and effectively subsume Approxis for additive error credits.
Whether a expectation-preserving composition law can be formulated for the full generality of
Clutch-DP remains a question for future work. Bluebell [Bao et al. 2025] encodes coupling-based
relational reasoning via a conditioning modality, but only supports exact program equivalences for
terminating first-order programs.
   (Non-) Termination. When verifying DP, we have to decide whether non-termination is
considered an observable behavior that can leak information about the presence of an individual
in a database. This is a well-known consideration in the context of DP (e.g., [Reed and Pierce
2010, §3.5], [Barthe et al. 2012, p.11]), and the most common solution to this problem is to rule out
non-terminating programs a priori, e.g., by restricting the programming language syntactically,
by including side-conditions in the program logic, or simply by not supporting reasoning about
not-obviously-terminating programs. Clutch-DP is a partial correctness logic: it neither assumes
nor guarantees termination, and instead follows a more flexible approach by allowing verification
of DP for an arbitrary RandML program f. If we separately also prove that f is terminating on
all inputs, we recover termination-sensitive DP. Standard techniques for ensuring termination
of probabilistic programs apply [Chatterjee et al. 2020; Majumdar and Sathiyanarayana 2025],
and termination for RandML-like languages can be handled via separation logics for reasoning
about termination probabilities [Aguirre et al. 2024; Gregersen et al. 2024a] or expected runtime
[Haselwarter et al. 2024; Lohse and Garg 2024].
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:23


7   Conclusion and Future Work
We have developed Clutch-DP, a probabilistic higher-order separation logic for DP. To demonstrate
how Clutch-DP enables modular verification of DP libraries, we addressed three representative
challenges and verified a wide range of case studies involving interactive mechanisms, privacy
filters, and memoization. Clutch-DP is proven sound as a library for Iris in the Rocq Prover.
    In future work, we would like to extend Clutch-DP to model concurrency to reason about local DP
in a distributed setting. Clutch-DP supports reasoning about generic mechanisms and about Laplace
distributions, but it should be possible to extend the operational semantics with, say, Gaussian
distributions. This should not invalidate any rules of the logic since Hoare quadruples are defined
for a general probabilistic operational semantics and our key lemmas such as choice-composition
are valid for arbitrary distributions. To prove approximate DP of programs based on the Gaussian,
new rules would be required. A challenging problem would be to extend Clutch-DP with support
for further reasoning principles such as advanced composition in the sense of DP or privacy
amplification by subsampling [Abadi et al. 2016; Balle et al. 2018]. We would also like to integrate
verified sampling mechanisms as developed by, e.g., de Medeiros et al. [2025], to provide end-to-end
DP guarantees by adapting the techniques of Aguirre et al. [2024] to verify rejection samplers to
the relational setting. Finally, it would be interesting to integrate other divergences [Sato et al.
2019] with relational separation logics to model, e.g., Rényi-DP.

Data Availability Statement
The Rocq formalization accompanying this work is available on Zenodo [Haselwarter et al. 2026b]
and on GitHub at github.com/logsem/clutch/tree/pldi26-clutch-dp.

Acknowledgments
This work was supported in part by the National Science Foundation, grant no. 2338317, the
Carlsberg Foundation, grant no. CF23-0791, Villum Investigator grants, no. VIL25804 and no.
VIL73403, Center for Basic Research in Program Verification (CPV), from the VILLUM Foundation,
and the European Union (ERC, CHORDS, 101096090). Views and opinions expressed are however
those of the author(s) only and do not necessarily reflect those of the European Union or the
European Research Council. Neither the European Union nor the granting authority can be held
responsible for them.
233:24                              P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


A     Semantic Model
In this section we dive into the model behind Clutch-DP and show how our adequacy theorem is
proven. We begin by recalling some notions of probability theory.

A.1      Probability Theory and Probabilistic Couplings
GivenÍ a countable set 𝐴, a probability (sub-)distribution 𝜇 over 𝐴 is a function 𝜇 : 𝐴 → [0, 1] such
that 𝑎 𝜇 (𝑎) ≤ 1. We use the notation D (𝐴) to denote the set of distributions over 𝐴. Distributions
have a well-known monadic structure, see, e.g., [Haselwarter et al. 2025]. We use ret 𝑎 and 𝜇 ≫= 𝑓 to
denote the return and bind operations. Given a random variable 𝑓 : 𝐴 → [0, 1], its expected value
                      Í
is given by E𝜇 [ 𝑓 ] ≜ 𝑎 𝜇 (𝑎) 𝑓 (𝑎).
   We recall the notion of (𝜀, 𝛿)-approximate coupling, due to [Barthe et al. 2016a; Sato 2016]:
   Definition A.1. Let 𝐴, 𝐵 be countable types, and Φ ⊆ 𝐴 × 𝐵 a relation. Given two real-valued
parameters 0 ≤ 𝜀, 𝛿, we say that there is an (𝜀, 𝛿)-approximate Φ−coupling between distributions
𝜇1 : D (𝐴), 𝜇2 : D (𝐵) if, for any real-valued random variables 𝑓 : 𝐴 → [0, 1], 𝑔 : 𝐵 → [0, 1] such that
∀(𝑎, 𝑏) ∈ Φ, 𝑓 𝑎 ≤ 𝑔𝑏, the following holds : E𝜇1 [ 𝑓 ] ≤ exp(𝜀) · E𝜇2 [𝑔 ] + 𝛿. We denote the existence of
such a coupling by 𝜇1 Φ (𝜀,𝛿 ) 𝜇2 .
  The reason we are interested in approximate couplings is that there is a tight connection between
them and DP. Indeed, when instantiating Φ to be the equality relation we have the following result:
  Theorem A.2. Let 𝑓 : DB → D (𝑋 ) be a function over databases. Then, 𝑓 is (𝜀, 𝛿)-dp iff for any
inputs 𝑏, 𝑏 ′ : DB such that 𝑑 DB (𝑏, 𝑏) ≤′ 1, we have 𝑓 𝑏 (=) (𝜀,𝛿 ) 𝑓 𝑏 ′ .
   Approximate couplings are the key component of our relational program logic. One can think of
𝜇1, 𝜇2 as two randomized computations, Φ as a relational postcondition we wish to establish and
(𝜀, 𝛿) as a privacy budget that we can spend in order to prove the postcondition. We will see later
in the section how to interpret 𝜀 and 𝛿 as separation logic resources, but for now notice that they
have an affine flavor to them, since they satisfy the following monotonicity lemma:
  Lemma A.3. Let 𝜇1 : D (𝐴), 𝜇 2 : D (𝐵), Φ ⊆ 𝐴 × 𝐵. Assume that 𝜇1 Φ (𝜀,𝛿 ) 𝜇2 . Then, for all 𝜀 ′, 𝛿 ′, Φ′
                                                            ′ ′
such that 𝜀 ≤ 𝜀 ′ , 𝛿 ≤ 𝛿 ′ , Φ ⊆ Φ′ , we also have 𝜇1 Φ′ (𝜀 ,𝛿 ) 𝜇2 .
  In order to build a logic around couplings, we need them to be able to compose them along the
operations of the underlying distribution monad. The following results are well-known:
    Theorem A.4. The distribution monad operations lift to couplings, in the sense that:
      • Let 𝑎 : 𝐴, 𝑏 : 𝐵 and Φ ⊆ 𝐴 × 𝐵 such that (𝑎, 𝑏) ∈ Φ. Then ret 𝑎 Φ (𝜀,𝛿 ) ret 𝑏.
      • Let 𝜇1 : D (𝐴), 𝜇2 : D (𝐵), 𝑓 : 𝐴 → D (𝐴′ ), 𝑔 : 𝐵 → D (𝐵 ′ ) and Φ ⊆ 𝐴 × 𝐵, Ψ ⊆ 𝐴′ × 𝐵 ′ such
                                                              ′ ′                              ′    ′
        that 𝜇 1 Φ (𝜀,𝛿 ) 𝜇2 and, for all (𝑎, 𝑏) ∈ Φ, 𝑓 𝑎 Ψ (𝜀 ,𝛿 ) 𝑔𝑏. Then, (𝜇1 ≫= 𝑓 ) Ψ (𝜀+𝜀 ,𝛿+𝛿 ) (𝜇 2 ≫= 𝑔).
   In order to support a more flexible form of composition, such as in our Above Threshold example
(§4.1.1), we introduce a more general version of the composition lemma above, where the choice of
coupling in the continuation can depend on the result of the first step. This is heavily inspired by
choice couplings [Barthe et al. 2016a], but it really shines in our setting, since we have a resourceful
treatment of the privacy budget.
  Theorem A.5. Let 𝜇1 : D (𝐴), 𝜇 2 : D (𝐵), 𝑓 : 𝐴 → D (𝐴′ ), 𝑔 : 𝐵 → D (𝐵 ′ ). Assume we have a
predicate Ξ ⊆ 𝐴, and Φ1, Φ2 ⊆ 𝐴 × 𝐵, Ψ ⊆ 𝐴′ × 𝐵 ′ , with Φ1, Φ2 disjoint in the sense that, ∀𝑎, 𝑎 ′, 𝑏.𝑎 ∈
Ξ ∧ 𝑎 ′ ∉ Ξ → ((𝑎, 𝑏) ∉ Φ1 ∨ (𝑎 ′, 𝑏) ∉ Φ2 ). Assume further that:
     • 𝜇1 Φ1 (𝜀1,𝛿1 ) 𝜇2
     • 𝜇1 Φ2 (𝜀2,𝛿2 ) 𝜇2
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)                233:25

                                                                            ′   ′
      • For all 𝑎, 𝑏 such that 𝑎 ∈ Ξ and (𝑎, 𝑏) ∈ Φ1 , 𝑓 𝑎 Ψ (𝜀1,𝛿1 ) 𝑔𝑏.
                                                               ′ ′
      • For all 𝑎, 𝑏 such that 𝑎 ∉ Ξ and (𝑎, 𝑏) ∈ Φ2 , 𝑓 𝑎 Ψ (𝜀2,𝛿2 ) 𝑔𝑏.
   Then, (𝜇 1 ≫= 𝑓 ) Ψ (𝜀,𝛿 ) (𝜇2 ≫= 𝑔), where 𝜀 ≜ max(𝜀 1 + 𝜀 1′ , 𝜀 2 + 𝜀 2′ ) and 𝛿 ≜ 𝛿 1 + 𝛿 2 + max(𝛿 1′ , 𝛿 2′ )

    The idea behind the statement above is that it allows us to use two different couplings for the
first step: one over Φ1 and another over Φ2 . Then get a sample 𝑎 from 𝜇1 , and we choose which of
the couplings to use depending on whether 𝑎 lands in Ξ, and we continue the rest of the execution.
In particular, this allows us to optimize the use of the 𝜀 component of the privacy budget, since we
can set the amount to use in each of the variants and only spend what we need. In the case of the 𝛿
component, we can also set the optimal amount for the continuation, but not for the first step, both
𝛿 1 and 𝛿 2 need to be spent no matter the result.

A.2    Hoare Quadruples and the Weakest Precondition
Hoare Quadruples are not a primitive notion in Clutch-DP. Instead, they are defined in terms of a
weakest precondition predicate (WP). This is a unary predicate about the left-hand side program.
The right-hand program 𝑒𝑅 is tracked by a resource spec(𝑒𝑅 ).

  {𝑃 } 𝑒 ­ 𝑒 ′ {𝑣 𝑣 ′ . 𝑄 }      ≜     (𝑃       ∗ ∃𝐾 . spec(𝐾 [𝑒 ′ ]) ∗ wp 𝑒 {𝑣 .∃𝑣 ′ . spec(𝐾 [𝑣 ′ ]) ∗ 𝑄 (𝑣, 𝑣 ′ )})

to state that 𝑒 refines 𝑒 ′ and that if 𝑒 terminates with 𝑣 then 𝑒 ′ terminates with 𝑣 ′ and the postcon-
dition 𝑃 is satisfied.
   The WP, whose definition is shown below, couples the execution of the implementation program
together with the execution of the specification program and ensures that the postcondition holds
at the end. The construction is similar to the one presented in Approxis [Haselwarter et al. 2025],
but adapted to our more general notion of coupling. Crucially, we also employ an updated program
coupling modality to support choice coupling composition at the level of program steps. Notice
that this definition tracks the two components of the error, both 𝜀 and 𝛿. As usual, the weakest
precondition is a predicate defined as a guarded fixpoint, whose existence is ensured by the presence
of the later modality (⊲) in front of the recursive occurrence of the weakest precondition:

  wp E 𝑒 1 {Φ} ≜ ∀𝜎1, 𝜌 1′ , 𝜀 1, 𝛿 1 . 𝑆 (𝜎1, 𝜌 1′ , 𝜀 1, 𝛿 1 ) ∗
                                                       ′        ′
                         E |⇛∅ scpl 𝜎1 ­ (𝜀 1 ,𝛿 1 ) 𝜌 1 {𝜎2, 𝜌 2, 𝜀 2, 𝛿 2 .
                             𝑒 1 ∈Val ∗ ∅ |⇛E 𝑆 (𝜎2, 𝜌 2′ , 𝜀 2, 𝛿 2 ) ∗ Φ(𝑒 1 ) ∨
                                                                                     

                             𝑒 1 ∉Val ∗ pcpl (𝑒 1, 𝜎2 ) ­ (𝜀2,𝛿2 ) 𝜌 2′ {𝑒 2, 𝜎3, 𝜌 3′ , 𝜀 3, 𝛿 3 .
                                ⊲ scpl 𝜎3 ­ (𝜀3,𝛿3 ) 𝜌 3′ {𝜎4, 𝜌 4′ , 𝜀 4, 𝛿 4 . ∅ |⇛E 𝑆 (𝜎4, 𝜌 4′ , 𝜀 4, 𝛿 4 ) ∗ wp E 𝑒 2 {Φ}}} }
                                                                                                                                


   The weakest precondition requires us to own the state interpretation 𝑆 (𝜎1, 𝜌 1′ , 𝜀 1, 𝛿 1 ), which is
a predicate that maps the different resources in Clutch-DP (the physical state of the implemen-
tation program, the configuration of the specification program, and the privacy budget) to their
corresponding resource algebras. We then have to prove two different cases, depending on whether
the current program 𝑒 is or is not a value. In the former case, we can just give back the state
interpretation and prove Φ. Otherwise, we have to prove a property about the distribution that
results after taking one program step. This is phrased in terms of the composition of two modalities,
the specification coupling modality and the program coupling modality.
   The specification coupling modality, initially introduced in Approxis, accounts for logical updates
to the current state of the execution. In particular, it allows for the specification program to take
233:26                                     P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


physical steps. It is defined as and inductive predicate given by the following rules:
                                                        spec-coupl-ret
                                                              Φ(𝜎, 𝜌 ′, 𝜀, 𝛿)
                                                        scpl 𝜎 ­ (𝜀,𝛿 ) 𝜌 ′ {Φ}
          spec-coupl-bind
                 𝜇1 𝑅 (𝜀1,𝛿1 ) (𝜇 1′ ≫= 𝜆 𝜎2′ . step𝑛 (𝑒 1′ , 𝜎2′ ))     𝜀1 + 𝜀2 ≤ 𝜀        𝛿1 + 𝛿2 ≤ 𝛿
          erasable(𝜇 1, 𝜎1 )        erasable(𝜇1′ , 𝜎1′ )          ∀(𝜎2, 𝜌 2′ ) ∈ 𝑅. |⇛∅ scpl 𝜎2 ­ (𝜀2,𝛿2 ) 𝜌 2′ {Φ}
                                                    scpl 𝜎1 ­ (𝜀,𝛿 ) (𝑒 1′ , 𝜎1′ ) {Φ}
   For the purpose of this work, the notion of erasability can mostly be ignored, this is used to
support presampling tapes [Gregersen et al. 2024b]. By the spec-coupl-ret rule, if the current
implementation and specification programs, and error budget satisfy Φ, we can immediately
conclude scpl 𝜎 ­ (𝜀,𝛿 ) 𝜌 ′ {Φ}. The spec-coupl-bind considers the recursive case. We can split
our current credit budget 𝜀, 𝛿 into 𝜀 1 + 𝜀 2, 𝛿 1 + 𝛿 2 and use 𝜀 1, 𝛿 1 to take a number 𝑛 of steps on
the specification program under an approximate coupling that satisfies an intermediate relation
𝑅. Then from (𝜎2, 𝜌 2′ ) ∈ 𝑅, we continue to recursively stablish scpl 𝜎2 ­ (𝜀2,𝛿2 ) 𝜌 2′ {Φ}, with our
remaining credit budget 𝜀 2, 𝛿 2 .
   The program coupling modality couples exactly one physical step of the left-hand side program
with an arbitrary number of physical steps 𝑛 of right-hand side program. In addition, the right-
hand side program is also allowed to execute an erasable update before its physical steps. Choice
couplings are baked into the definition of the program coupling modality, thus the intermediate pair
of states that the program reach can satisfy one of either 𝑅1 or 𝑅2 before executing the continuation.
The amount of error credits that is available for the continuation may also depend on this choice.

prog-coupl-bind
step(𝑒 1, 𝜎1 ) 𝑅1 (𝜀1,𝛿1 ) (𝜇 1′ ≫= 𝜆 𝜎2′ . step𝑛 (𝑒 1′ , 𝜎2′ ))     step(𝑒 1, 𝜎1 ) 𝑅2 (𝜀2,𝛿2 ) (𝜇 1′ ≫= 𝜆 𝜎2′ . step𝑛 (𝑒 1′ , 𝜎2′ ))
                                             ′    ′
 red(𝑒 1, 𝜎1 )       𝜀1 + 𝜀2 ≤ 𝜀            𝜀1 + 𝜀2 ≤ 𝜀          𝛿 1 + 𝛿 2 + max(𝛿 1′ + 𝛿 2′ ) ≤ 𝛿         erasable(𝜇1′ , 𝜎1′ )

           ∀((𝑒 2, 𝜎2 ), (𝑒 2′ , 𝜎2′ )). ((𝑃 (𝑒 2, 𝜎2 ) ∧ 𝑅1 ((𝑒 2, 𝜎2 ), (𝑒 2′ , 𝜎2′ )))|⇛∅ Φ(𝑒 2, 𝜎2, 𝑒 2′ , 𝜎2′ , 𝜀 1′ , 𝛿 1′ ))∗
                        ((¬𝑃 (𝑒 2, 𝜎2 ) ∧ 𝑅2 ((𝑒 2, 𝜎2 ), (𝑒 2′ , 𝜎2′ )))|⇛∅ Φ(𝑒 2, 𝜎2, 𝑒 2′ , 𝜎2′ , 𝜀 2′ , 𝛿 2′ ))
                                                pcpl (𝑒 1, 𝜎1 ) ­ (𝜀,𝛿 ) (𝑒 1′ , 𝜎1′ ) {Φ}

A.3      An Adequacy Theorem
With these definitions in hand, we can state the adequacy theorem of Clutch-DP, now in full
generality:
   Theorem A.6. Let 𝑒, 𝑒 ′ be two RandML functions and Ψ : Val ×Val → Prop a proposition over (final)
values. If spec(𝑒 ′ ) ∗ E× (𝜀) ∗ E+ (𝛿) ∗ wp 𝑒 {𝑣, 𝑣 ′ .spec(𝑣 ′ ) ∗ Ψ} holds in Clutch-DP, then, for any
initial states 𝜎, 𝜎 ′ , we have exec(𝑒, 𝜎) Ψ (𝜀,𝛿 ) exec(𝑒 ′, 𝜎 ′ ).
  The proof is done by induction on the execution of the left-hand side program, by proving the
lemma below, and finally taking a limit:
  Lemma A.7. Let 𝑒, 𝑒 ′ be two RandML functions and Ψ : Val ×Val → Prop a proposition over (final)
values. If spec(𝑒 ′ ) ∗ E× (𝜀) ∗ E+ (𝛿) ∗ wp 𝑒 {𝑣, 𝑣 ′ .spec(𝑒 ′ ) ∗ Ψ} holds in Clutch-DP, then, for any
𝑛 ∈ N and any initial states 𝜎, 𝜎 ′ , we have exec𝑛 (𝑒, 𝜎) Ψ (𝜀,𝛿 ) exec(𝑒 ′, 𝜎 ′ ).
   The key part of the proof happens when the program on the left is not a value, and has to take a
step. This requires two applications of spec-coupl-bind and one application of prog-coupl-bind to
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)   233:27


establish the specification coupling in the non-value case of the WP. In particular, prog-coupl-bind
allows us to advance the program on the left exactly one step, which lets us use our inductive
hypothesis about exec𝑛 (𝑒, −) to reason about exec𝑛+1 (𝑒, 𝜎).

B    Case Study: Report Noisy Max
The Report Noisy Max mechanism (RNM) is a DP mechanism that receives a list of 𝑁 1-sensitive
queries, runs them privately by adding noise sampled from Laplace (ε/2), and returns the index
of the query with the highest value. While a naïve analysis of the algorithm using composition
theorems would show that the algorithm is (𝑁 · ε/2)-dp, the only information that is released is the
index of the highest query and all other (noisy) results are discarded. This suggests that a better
analysis should be possible. In fact, one can prove that RNM is ε-dp, in other words, its privacy cost
is constant and is completely independent of the number of queries.
   We now show how this is proven in Clutch-DP. In this example, we make use of presampling
tapes, a reasoning principle for talking about future probabilistic outcomes [Gregersen et al. 2024b;
Haselwarter et al. 2025]. Our implementation of RNM (see Figure 13) therefore utilizes code to
manipulate tapes, and one can show that this implementation is contextually equivalent to one
with all the tape annotations removed [Gregersen et al. 2024b].

                   let RNM q N db =
                       let xs = List.init N (𝜆 i. q i db) in
                       let xs_tapes = List.map (𝜆 x. (x, tape L (ε/2) x)) xs in
                       let noisy_xs = List.map (𝜆 (x, 𝜄). Laplace (ε/2) x 𝜄) xs_tapes in
                       List.max_index noisy_xs
                                    Fig. 13. The Report Noisy Max mechanism
   The implementation of RNM takes three arguments: the query function q, the number of queries
N, and the database db. The first line of RNM computes the (exact) results of running the query
function for all indices 0 ≤ i < N on the database and stores the result in the list xs. The second
line pairs each result x with a freshly allocated presampling tape label for a Laplacian with spread
ε/2 and mean x. This ghost code will later allow us to reason about the Laplacian samples. On line
three, we compute the noisy results noisy_xs by adding Laplace noise, and finally on line four we
return the index of the largest noisy value.
   We prove that RNM is internally differentially private for any 1-sensitive family of queries q.
Concretely, this amounts to
                                                        Adj(db, db′ ) ∗ E× (ε)
                                                      
                            ′
               ∀ q N db db . (∀𝑖. 1-sens(q 𝑖)) ∗         RNM q N db ­ RNM q N db′                (14)
                                                      {𝑣 𝑣 ′ . 𝑣 = 𝑣 ′ }
By soundness of Clutch-DP (Theorem 3.2), RNM q N is ε-dp for suitable queries q and for all N.
   The key idea in this proof is to utilize tapes to perform a relatively complicated presampling
operation on all of the N allocated Laplace tapes at the logic level in one logical step. This ensures
that the index of the highest presampled result is the same for db and for db′ . Then, when the
Laplace instructions on line three are executed, we deterministically read out the presampled values
from the tapes, and establish the postcondition directly.
   Let us step through the proof line-by-line. After querying the database at the beginning, we
obtain two lists of results represented by lists 𝑙 1 and 𝑙 1′ for the program and specification side,
respectively. Since the queries are 1-sensitive, it follows that 𝑙 1 and 𝑙 1′ are pairwise-adjacent. Next,
we allocate tapes for these results, obtaining a list of tape labels 𝜄𝑠 and 𝜄𝑠 ′ where all of them point
233:28                                                P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


to empty tapes:

                                       ∗
                                    (𝑥,𝜄 ) ∈𝑙 1 ;𝜄𝑠
                                                      𝜄 ↩→ (L𝑥ε/2, [])                          ∗
                                                                                                          ∗
                                                                                                    (𝑥 ′ ,𝜄 ′ ) ∈𝑙 1′ ;𝜄𝑠 ′
                                                                                                                                          ′
                                                                                                                              𝜄 ′ ↩→s (L𝑥ε/2, [])

   We then perform a logic-level resource update, where we perform a presampling operation on
the tapes in one go (similar to rel-couple-tapes from the Clutch paper [Gregersen et al. 2024b],
albeit being more complicated), which consumes E× (ε) from the precondition. After this operation,
the program and specification tapes contain 𝑙 2 and 𝑙 2′ , respectively, where the index of the maximum
element in 𝑙 2 and 𝑙 2′ is the same. Instead of consuming E× (𝑁 · ε) to apply Laplace-shift 𝑁 times
for each of the 𝑁 samplings, roughly speaking, this operation enables us to consume exactly E× (ε)
to pay for the component of the Laplace coupling which returns the largest result among the list
of samplings. This operation is sound in Clutch-DP by leveraging a pointwise-equality argument,
also used in Hsu [2017], and we obtain the following:

      ∗
(𝑥,𝑦,𝜄 ) ∈𝑙 1 ;𝑙 2 ;𝜄𝑠
                         𝜄 ↩→ (L𝑥ε/2, [𝑦])            ∗
                                                                     ∗
                                                          (𝑥 ′ ,𝑦 ′ ,𝜄 ′ ) ∈𝑙 1′ ;𝑙 2′ ;𝜄𝑠 ′
                                                                                                                     ′
                                                                                               𝜄 ′ ↩→s (L𝑥ε/2, [𝑦 ′ ]) ∗ max_index 𝑙 2 = max_index 𝑙 2′

  Calling Laplace on these pre-populated tapes then deterministically returns the value stored in
the tape. As a result, noisy_xs and noisy_xs′ contains 𝑙 2 and 𝑙 2′ , respectively, and the index of the
maximum element of both lists is the same, establishing the postcondition of the specification.
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)          233:29


References
Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep
    Learning with Differential Privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications
    Security (Vienna, Austria) (CCS ’16). Association for Computing Machinery, New York, NY, USA, 308–318. https:
    //doi.org/10.1145/2976749.2978318
Chiké Abuah, David Darais, and Joseph P. Near. 2022. Solo: A Lightweight Static Analysis for Differential Privacy. Proc.
    ACM Program. Lang. 6, OOPSLA2, Article 150 (Oct. 2022). https://doi.org/10.1145/3563313
Alejandro Aguirre, Gilles Barthe, Marco Gaboardi, Deepak Garg, Shin-ya Katsumata, and Tetsuya Sato. 2021. Higher-order
    probabilistic adversarial computations: categorical semantics and program logics. Proc. ACM Program. Lang. 5, ICFP,
    Article 93 (Aug 2021), 30 pages. https://doi.org/10.1145/3473598
Alejandro Aguirre, Philipp G. Haselwarter, Markus de Medeiros, Kwing Hei Li, Simon Oddershede Gregersen, Joseph Tas-
    sarotti, and Lars Birkedal. 2024. Error Credits: Resourceful Reasoning about Error Bounds for Higher-Order Probabilistic
    Programs. Proc. ACM Program. Lang. 8, ICFP, Article 246 (Aug 2024), 33 pages. https://doi.org/10.1145/3674635
Aws Albarghouthi and Justin Hsu. 2017. Synthesizing Coupling Proofs of Differential Privacy. Proceedings of the ACM on
    Programming Languages 2, POPL (Dec. 2017), 58:1–58:30. https://doi.org/10.1145/3158146
Borja Balle, Gilles Barthe, and Marco Gaboardi. 2018. Privacy amplification by subsampling: tight analyses via couplings
    and divergences. In Proceedings of the 32nd International Conference on Neural Information Processing Systems (Montréal,
    Canada) (NIPS’18). Curran Associates Inc., Red Hook, NY, USA, 6280–6290.
Jialu Bao, Emanuele D’Osualdo, and Azadeh Farzan. 2025. Bluebell: An Alliance of Relational Lifting and Independence for
    Probabilistic Reasoning. Proc. ACM Program. Lang. 9, POPL, Article 58 (Jan. 2025), 31 pages. https://doi.org/10.1145/
    3704894
Gilles Barthe, Thomas Espitau, Benjamin Grégoire, Justin Hsu, Léo Stefanesco, and Pierre-Yves Strub. 2015a. Relational
    Reasoning via Probabilistic Coupling. In Logic for Programming, Artificial Intelligence, and Reasoning - 20th International
    Conference, LPAR-20 2015, Suva, Fiji, November 24-28, 2015, Proceedings. https://doi.org/10.1007/978-3-662-48899-7_27
Gilles Barthe, Noémie Fong, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016a. Advanced
    Probabilistic Couplings for Differential Privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and
    Communications Security, Vienna, Austria, October 24-28, 2016 (CCS ’16). 55–67. https://doi.org/10.1145/2976749.2978391
Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu, Aaron Roth, and Pierre-Yves Strub. 2015b. Higher-
    Order Approximate Relational Refinement Types for Mechanism Design and Differential Privacy. In Proceedings of the
    42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’15). Association for
    Computing Machinery, New York, NY, USA, 55–68. https://doi.org/10.1145/2676726.2677000
Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016b. Proving Differential Privacy
    via Probabilistic Couplings. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science (New
    York, NY, USA) (LICS ’16). Association for Computing Machinery, New York, NY, USA, 749–758. https://doi.org/10.1145/
    2933575.2934554
Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. 2012. Probabilistic relational reasoning for
    differential privacy. SIGPLAN Not. 47, 1 (Jan 2012), 97–110. https://doi.org/10.1145/2103621.2103670
Clément L. Canonne, Gautam Kamath, and Thomas Steinke. 2020. The Discrete Gaussian for Differential Privacy. In
    Proceedings of the 34th International Conference on Neural Information Processing Systems (NIPS ’20). Curran Associates
    Inc., Red Hook, NY, USA, 15676–15688.
Krishnendu Chatterjee, Hongfei Fu, and Petr Novotný. 2020. Termination Analysis of Probabilistic Programs with Martingales.
    In Foundations of Probabilistic Programming, Gilles Barthe, Joost-Pieter Katoen, and Alexandra Silva (Eds.). Cambridge
    University Press, 221–258. https://doi.org/10.1017/9781108770750.008
Ethan Cowan, Michael Shoemate, and Mayana Pereira. 2024. Hands-on Differential Privacy: Introduction to the Theory and
    Practice Using OpenDP (first edition ed.). O’Reilly Media, Inc, Sebastopol, CA.
Arthur Azevedo de Amorim, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. 2021. Probabilistic Relational Reasoning
    via Metrics. In Proceedings of the 34th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS ’19). IEEE Press,
    Vancouver, Canada, 1–19.
Markus de Medeiros, Muhammad Naveed, Tancrède Lepoint, Temesghen Kahsai, Tristan Ravitch, Stefan Zetzsche, Anjali
    Joshi, Joseph Tassarotti, Aws Albarghouthi, and Jean-Baptiste Tristan. 2025. Verified Foundations for Differential Privacy.
    Artifact for Verified Foundations for Differential Privacy 9, PLDI (June 2025), 191:1094–191:1118. https://doi.org/10.1145/
    3729294
Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006. Calibrating Noise to Sensitivity in Private
    Data Analysis. In Theory of Cryptography, Shai Halevi and Tal Rabin (Eds.). Springer, Berlin, Heidelberg, 265–284.
    https://doi.org/10.1007/11681878_14
Cynthia Dwork and Aaron Roth. 2014. The Algorithmic Foundations of Differential Privacy. Foundations and Trends® in
    Theoretical Computer Science 9, 3–4 (Aug. 2014), 211–407. https://doi.org/10.1561/0400000042
233:30                               P. G. Haselwarter, A. Aguirre, S. O. Gregersen, K. H. Li, J. Tassarotti, and L. Birkedal


Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2021. ReLoC Reloaded: A Mechanized Relational Logic for Fine-Grained
   Concurrency and Logical Atomicity. Log. Methods Comput. Sci. 17, 3 (2021). https://doi.org/10.46298/lmcs-17(3:9)2021
Marco Gaboardi, Andreas Haeberlen, Justin Hsu, Arjun Narayan, and Benjamin C. Pierce. 2013. Linear Dependent
   Types for Differential Privacy. In Proceedings of the 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles
   of Programming Languages (POPL ’13). Association for Computing Machinery, New York, NY, USA, 357–370. https:
   //doi.org/10.1145/2429069.2429113
Arpita Ghosh, Tim Roughgarden, and Mukund Sundararajan. 2012. Universally Utility-maximizing Privacy Mechanisms.
   SIAM J. Comput. 41, 6 (Jan. 2012), 1673–1693. https://doi.org/10.1137/09076828X
Simon Oddershede Gregersen, Alejandro Aguirre, Philipp G. Haselwarter, Joseph Tassarotti, and Lars Birkedal. 2024a. Almost-
   Sure Termination by Guarded Refinement. CoRR abs/2404.08494 (2024). https://doi.org/10.48550/ARXIV.2404.08494
   arXiv:2404.08494
Simon Oddershede Gregersen, Alejandro Aguirre, Philipp G. Haselwarter, Joseph Tassarotti, and Lars Birkedal. 2024b.
   Asynchronous Probabilistic Couplings in Higher-Order Separation Logic. Proc. ACM Program. Lang. 8, POPL (2024),
   753–784. https://doi.org/10.1145/3632868
Philipp G. Haselwarter, Alejandro Aguirre, Simon Oddershede Gregersen, Kwing Hei Li, Joseph Tassarotti, and Lars Birkedal.
   2026a. Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic. Proc. ACM Program.
   Lang. 10, PLDI, Article 233 (June 2026). https://doi.org/10.1145/3808311
Philipp G. Haselwarter, Alejandro Aguirre, Simon Oddershede Gregersen, Kwing Hei Li, Joseph Tassarotti, and Lars
   Birkedal. 2026b. Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic - Artifact.
   https://doi.org/10.5281/zenodo.19089094
Philipp G. Haselwarter, Kwing Hei Li, Alejandro Aguirre, Simon Oddershede Gregersen, Joseph Tassarotti, and Lars Birkedal.
   2025. Approximate Relational Reasoning for Higher-Order Probabilistic Programs. Proc. ACM Program. Lang. 9, POPL,
   Article 41 (Jan. 2025), 31 pages. https://doi.org/10.1145/3704877
Philipp G. Haselwarter, Kwing Hei Li, Markus de Medeiros, Simon Oddershede Gregersen, Alejandro Aguirre, Joseph
   Tassarotti, and Lars Birkedal. 2024. Tachis: Higher-Order Separation Logic with Credits for Expected Costs. Proc. ACM
   Program. Lang. 8, OOPSLA2, Article 313 (Oct. 2024), 30 pages. https://doi.org/10.1145/3689753
Justin Hsu. 2017. Probabilistic Couplings for Probabilistic Reasoning. Ph. D. Dissertation. University of Pennsylvania.
   arXiv:1710.09951
Seidu Inusah and Tomasz J. Kozubowski. 2006. A Discrete Analogue of the Laplace Distribution. Journal of Statistical
   Planning and Inference 136, 3 (March 2006), 1090–1102. https://doi.org/10.1016/j.jspi.2004.08.014
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   https://doi.org/10.1017/S0956796818000151
Kelly Kostopoulou, Pierre Tholoniat, Asaf Cidon, Roxana Geambasu, and Mathias Lécuyer. 2023. Turbo: Effective Caching
   in Differentially-Private Databases. In Proceedings of the 29th Symposium on Operating Systems Principles (SOSP ’23).
   Association for Computing Machinery, New York, NY, USA, 579–594. https://doi.org/10.1145/3600006.3613174
Ios Kotsogiannis, Yuchao Tao, Xi He, Maryam Fanaeepour, Ashwin Machanavajjhala, Michael Hay, and Gerome Miklau.
   2019. PrivateSQL: A Differentially Private SQL Query Engine. Proc. VLDB Endow. 12, 11 (July 2019), 1371–1384.
   https://doi.org/10.14778/3342263.3342274
Elisabet Lobo-Vesga, Alejandro Russo, and Marco Gaboardi. 2020. A Programming Framework for Differential Privacy with
   Accuracy Concentration Bounds. In 2020 IEEE Symposium on Security and Privacy (SP). 411–428. https://doi.org/10.1109/
   SP40000.2020.00086
Elisabet Lobo-Vesga, Alejandro Russo, Marco Gaboardi, and Carlos Tomé Cortiñas. 2024. Sensitivity by Parametricity. Paper
   Artifact: Sensitivity by Parametricity 8, OOPSLA2 (Oct. 2024), 286:415–286:441. https://doi.org/10.1145/3689726
Janine Lohse and Deepak Garg. 2024. An Iris for Expected Cost Analysis. arXiv:2406.00884 [cs.PL]
Min Lyu, Dong Su, and Ninghui Li. 2017. Understanding the Sparse Vector Technique for Differential Privacy. Proc. VLDB
   Endow. 10, 6 (Feb. 2017), 637–648. https://doi.org/10.14778/3055330.3055331
Rupak Majumdar and V.R. Sathiyanarayana. 2025. Sound and Complete Proof Rules for Probabilistic Termination. Proc.
   ACM Program. Lang. 9, POPL, Article 63 (Jan. 2025), 32 pages. https://doi.org/10.1145/3704899
Miti Mazmudar, Thomas Humphries, Jiaxiang Liu, Matthew Rafuse, and Xi He. 2022. Cache Me If You Can: Accuracy-
   Aware Inference Engine for Differentially Private Data Exploration. Proc. VLDB Endow. 16, 4 (Dec. 2022), 574–586.
   https://doi.org/10.14778/3574245.3574246
Ilya Mironov. 2012. On Significance of the Least Significant Bits for Differential Privacy. In Proceedings of the 2012 ACM
   Conference on Computer and Communications Security (CCS ’12). Association for Computing Machinery, New York, NY,
   USA, 650–661. https://doi.org/10.1145/2382196.2382264
Joseph P. Near and Chiké Abuah. 2021. Programming Differential Privacy. Vol. 1. https://programming-dp.com/
Modular Verification of Differential Privacy in Probabilistic Higher-Order Separation Logic (Extended Version)        233:31


Joseph P. Near, David Darais, Chike Abuah, Tim Stevens, Pranav Gaddamadugu, Lun Wang, Neel Somani, Mu Zhang, Nikhil
   Sharma, Alex Shan, and Dawn Song. 2019. Duet: An Expressive Higher-Order Language and Linear Type System for
   Statically Enforcing Differential Privacy. Proc. ACM Program. Lang. 3, OOPSLA (Oct. 2019). https://doi.org/10.1145/
   3360598
Shangfu Peng, Yin Yang, Zhenjie Zhang, Marianne Winslett, and Yong Yu. 2013. Query Optimization for Differentially
   Private Data Management Systems. In 2013 IEEE 29th International Conference on Data Engineering (ICDE). 1093–1104.
   https://doi.org/10.1109/ICDE.2013.6544900
Jason Reed and Benjamin C. Pierce. 2010. Distance Makes the Types Grow Stronger: A Calculus for Differential Privacy. In
   Proceedings of the 15th ACM SIGPLAN International Conference on Functional Programming (ICFP ’10). Association for
   Computing Machinery, New York, NY, USA, 157–168. https://doi.org/10.1145/1863543.1863568
Ryan M Rogers, Aaron Roth, Jonathan Ullman, and Salil Vadhan. 2016. Privacy Odometers and Filters: Pay-as-you-Go
   Composition. In Advances in Neural Information Processing Systems, Vol. 29. Curran Associates, Inc.
Tetsuya Sato. 2016. Approximate Relational Hoare Logic for Continuous Random Samplings. In The Thirty-second Conference
   on the Mathematical Foundations of Programming Semantics, MFPS 2016. https://doi.org/10.1016/J.ENTCS.2016.09.043
Tetsuya Sato, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. 2019. Approximate Span Liftings:
   Compositional Semantics for Relaxations of Differential Privacy. In 2019 34th Annual ACM/IEEE Symposium on Logic in
   Computer Science (LICS). 1–14. https://doi.org/10.1109/LICS.2019.8785668
Tetsuya Sato and Yasuhiko Minamide. 2025. Formalization of Differential Privacy in Isabelle/HOL. In Proceedings of the 14th
   ACM SIGPLAN International Conference on Certified Programs and Proofs (CPP ’25). Association for Computing Machinery,
   New York, NY, USA, 67–82. https://doi.org/10.1145/3703595.3705875
Matías Toro, David Darais, Chike Abuah, Joseph P. Near, Damián Árquez, Federico Olmedo, and Éric Tanter. 2023. Contextual
   Linear Types for Differential Privacy. ACM Trans. Program. Lang. Syst. 45, 2 (May 2023), 8:1–8:69. https://doi.org/10.
   1145/3589207
Daniel Winograd-Cort, Andreas Haeberlen, Aaron Roth, and Benjamin C. Pierce. 2017. A Framework for Adaptive Differential
   Privacy. Proc. ACM Program. Lang. 1, ICFP (Aug. 2017), 10:1–10:29. https://doi.org/10.1145/3110254
Danfeng Zhang and Daniel Kifer. 2017. LightDP: Towards Automating Differential Privacy Proofs. In Proceedings of the 44th
   ACM SIGPLAN Symposium on Principles of Programming Languages (POPL ’17). Association for Computing Machinery,
   New York, NY, USA, 888–901. https://doi.org/10.1145/3009837.3009884
Hengchu Zhang, Edo Roth, Andreas Haeberlen, Benjamin C. Pierce, and Aaron Roth. 2019. Fuzzi: A Three-Level Logic for
   Differential Privacy. Prototype Implementation of Fuzzi: A Three-Level Logic for Differential Privacy 3, ICFP (July 2019),
   93:1–93:28. https://doi.org/10.1145/3341697
