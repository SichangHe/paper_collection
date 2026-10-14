                                        A Primal-Dual Perspective on Program Verification
                                        Algorithms (Extended Version)
                                        TAKESHI TSUKADA, Chiba University, Japan
                                        HIROSHI UNNO, Tohoku University, Japan
arXiv:2501.01512v1 [cs.PL] 2 Jan 2025




                                        ODED PADON, Weizmann Institute of Science, Israel
                                        SHARON SHOHAM, Tel Aviv University, Israel
                                        Many algorithms in verification and automated reasoning leverage some form of duality between proofs and
                                        refutations or counterexamples. In most cases, duality is only used as an intuition that helps in understanding
                                        the algorithms and is not formalized. In other cases, duality is used explicitly, but in a specially tailored way
                                        that does not generalize to other problems.
                                           In this paper we propose a unified primal-dual framework for designing verification algorithms that leverage
                                        duality. To that end, we generalize the concept of a Lagrangian that is commonly used in linear programming
                                        and optimization to capture the domains considered in verification problems, which are usually discrete, e.g.,
                                        powersets of states, predicates, ranking functions, etc. A Lagrangian then induces a primal problem and a dual
                                        problem. We devise an abstract primal-dual procedure that simultaneously searches for a primal solution and
                                        a dual solution, where the two searches guide each other. We provide sufficient conditions that ensure that
                                        the procedure makes progress under certain monotonicity assumptions on the Lagrangian.
                                           We show that many existing algorithms in program analysis, verification, and automated reasoning can
                                        be derived from our algorithmic framework with a suitable choice of Lagrangian. The Lagrangian-based
                                        formulation sheds new light on various characteristics of these algorithms, such as the ingredients they use
                                        to ensure monotonicity and guarantee progress. We further use our framework to develop a new validity
                                        checking algorithm for fixpoint logic over quantified linear arithmetic. Our prototype achieves promising
                                        results and in some cases solves instances that are not solved by state-of-the-art techniques.

                                        CCS Concepts: • Theory of computation → Logic and verification; Program verification.

                                        Additional Key Words and Phrases: primal-dual method, Lagrangian, verification

                                        1   Introduction
                                        Duality and the primal-dual approach are a corner stone in algorithm design and optimization [Bert-
                                        simas and Tsitsiklis 1997; Boyd and Vandenberghe 2014]. In program analysis, verification, and
                                        automated reasoning, many algorithms also have a primal-dual flavor. The common duality in
                                        these contexts is between a proof and a refutation or counterexample. That is, the algorithm simul-
                                        taneously searches for a proof and a refutation, and both searches guide each other in a meaningful
                                        way. For example, in counterexample guided abstraction refinement (CEGAR) [Ball et al. 2001a;
                                        Clarke et al. 2000], the search alternates between searching for a counterexample to the current
                                        abstraction and refining the abstraction to eliminate a spurious counterexample. The intuition
                                        is that refining the abstraction according to a spurious counterexample makes progress towards
                                        a proof (if one exists), and finding counterexamples for more refined abstractions might make
                                        progress towards a non-spurious counterexample (if one exists).
                                           A similar interaction between the search for proofs and the search for counterexamples exists in
                                        many program analysis, verification, and automated reasoning algorithms, including may-must
                                        analysis [Godefroid et al. 2010], ICE learning [Garg et al. 2014], lazy SMT solving [Nieuwenhuis
                                        et al. 2006], quantifier instantiation [Ge and de Moura 2009], program synthesis [Jha et al. 2010],

                                        Authors’ Contact Information: Takeshi Tsukada, Chiba University, Chiba, Japan, t.tsukada@acm.org; Hiroshi Unno, Tohoku
                                        University, Sendai, Japan, hiroshi.unno@acm.org; Oded Padon, Weizmann Institute of Science, Rehovot, Israel, oded.padon@
                                        weizmann.ac.il; Sharon Shoham, Tel Aviv University, Tel Aviv, Israel, sharon.shoham@gmail.com.
2                                                   Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


game solving [Farzan and Kincaid 2018] and more. In most of these cases, the primal-dual nature
of the search algorithm is not made explicit and formal.
   Recently, some algorithms were proposed that are explicitly manifested as primal-dual algorithms.
In [Padon et al. 2022], a primal-dual algorithm for safety verification is proposed, based on a duality
between executions in a transition system and a form of incremental induction proofs. In [Unno
et al. 2023], a primal-dual algorithm for validity of formulas in first-order fixpoint logic with
background theories is proposed, based on a duality between the validity of a formula and that of
its negation, which corresponds to a duality between least and greatest fixpoints. However, while
these algorithms are both explicitly primal-dual, the duality and the primal-dual algorithm are
bespoke in each case.
   In this paper, we propose a unifying perspective that shows that many algorithms in program
analysis, verification, and automated reasoning that leverage duality, be it informally and intuitively
or explicitly and formally, can be derived from a common principle. Moreover, this principle is
connected to the classical notion of duality based on a Lagrangian used in linear programming [Bert-
simas and Tsitsiklis 1997; Boyd and Vandenberghe 2014]. We leverage the Lagrangian perspective
to study different characteristics of existing algorithms, and to develop a new algorithm for solving
formulas in fixpoint logic over quantified linear arithmetic.
   In linear programming, a Lagrangian 𝐿(𝑥, 𝜆) is typically defined as a function from R𝑛 × R𝑚
to R. The Lagrangian induces two related optimization problems: the primal problem is find-
ing inf 𝑥 sup𝜆 𝐿(𝑥, 𝜆), and the dual problem is finding sup𝜆 inf 𝑥 𝐿(𝑥, 𝜆). It is easy to see that
sup𝜆 inf 𝑥 𝐿(𝑥, 𝜆) ≤ inf 𝑥 sup𝜆 𝐿(𝑥, 𝜆), which is known as weak duality (strong duality is when
an equality holds). That is, the solution to the dual problem provides a lower bound on the solution
of the primal problem. Moreover, for any 𝜆, the value of inf 𝑥 𝐿(𝑥, 𝜆) provides such a lower bound.
Similarly (dually), the value of sup𝜆 𝐿(𝑥, 𝜆) for any 𝑥 provides an upper bound on the dual problem.
These properties are used in algorithm design to simultaneously search for solutions to the primal
and dual problems, where both searches guide each other.
   We propose to define a Lagrangian 𝐿(𝑥, 𝑦) from 𝑋 × 𝑌 for arbitrary sets 𝑋 and 𝑌 to a totally-
ordered complete lattice, such that the induced primal and dual problems correspond, intuitively,
to checking validity of a candidate proof and checking validity of a candidate refutation. Unlike in
the linear programming case, the sets 𝑋 and 𝑌 that arise in verification contexts are not real vector
spaces but discrete sets or lattices (e.g, powerset lattices of sets of states or abstract domains).
   For example, we can define a Lagrangian that captures the classic CEGAR algorithm as follows.
The set 𝑋 represents possible (abstract) counterexample traces, i.e, 𝑋 is the set of sequences of
states. The set 𝑌 represents possible abstractions, i.e., 𝑌 is the set of finite sets of predicates. We
define the Lagrangian 𝐿((𝑠 0𝑠 1 · · · 𝑠𝑛 ), {𝑝 0, 𝑝 1, . . . , 𝑝𝑚 }) to be −1 if the sequence (𝑠 0𝑠 1 · · · 𝑠𝑛 ) is a
counterexample for the abstract transition system defined by the abstraction to {𝑝 0, 𝑝 1, . . . , 𝑝𝑚 },
and 1 otherwise. That is, the Lagrangian is −1 if for every 0 < 𝑖 < 𝑛 there is a transition from a
state 𝑠 to a state 𝑡 such that on all the predicates in {𝑝 0, 𝑝 1, . . . , 𝑝𝑚 }, 𝑠 agrees with 𝑠𝑖 and 𝑡 agrees
with 𝑠𝑖+1 . With this definition of a Lagrangian, safety is captured by sup𝑦 inf 𝑥 𝐿(𝑥, 𝜆) = 1, which
holds if there exists a set of predicates 𝑦 such that for every sequence of states 𝑥, 𝐿(𝑥, 𝑦) = 1, i.e., 𝑥
is not an abstract counterexample in the abstract transition system induced by 𝑦.
   We further propose an algorithmic framework that given a Lagrangian, tries to solve the primal
and dual problems simultaneously with primal-dual guidance between both sides of the duality.
The basic algorithm attempts to find 𝛼 ∈ 𝑋 such that sup𝑦 𝐿(𝛼, 𝑦) is small enough, providing an
upper bound on the primal solution, or 𝛽 ∈ 𝑌 such that inf 𝑥 𝐿(𝑥, 𝛽) is large enough, providing a
lower bound on the dual problem. For example, in the case of CEGAR, if inf 𝑥 𝐿(𝑥, 𝛽) is 1 for some
set of predicates 𝛽, so is the solution of the dual problem, and the system is safe. Starting from some
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                         3


candidates 𝛼 and 𝛽, as long as the aforementioned conditions do not hold, the algorithm iteratively
updates 𝛼 to some 𝛼 ′ that witnesses that inf 𝑥 𝐿(𝑥, 𝛽) is not large enough (i.e., 𝐿(𝛼 ′, 𝛽) is not large
enough); or updates 𝛽 to 𝛽 ′ that witnesses that sup𝑦 𝐿(𝛼, 𝑦) is not small enough (i.e., 𝐿(𝛼, 𝛽 ′ ) is not
small enough). That is, the update of the primal candidate 𝛼 is guided by the dual problem and vice
versa. For CEGAR, given a set of predicates 𝛽, computing a witness for inf 𝑥 𝐿(𝑥, 𝛽) ≱ 1, i.e., finding
𝛼 ′ such that 𝐿(𝛼 ′, 𝛽) = −1, corresponds to finding an abstract counterexample for the abstraction 𝛽
defines; and for a given sequence 𝛼, finding 𝛽 ′ such that 𝐿(𝛼, 𝛽 ′ ) = 1 corresponds to finding an
abstraction that rules out 𝛼 as an abstract counterexample, i.e., an abstraction refinement step.
    Often, 𝑋 or 𝑌 (or both) are join semilattices, in which case it is possible to increase 𝛼 or 𝛽 (or
both) in each iteration by joining their new value with the previous one. For example, in the case
of the Lagrangian that captures CEGAR, the set 𝑌 of possible abstractions (sets of predicates) is
a join semilattice, and increasing 𝛽 ∈ 𝑌 corresponds to “accumulating” predicates, as opposed to
starting from scratch with a new set of predicates in each iteration. We prove that if the Lagrangian
is (anti-)monotone in 𝑋 or 𝑌 the “accumulation” of values ensures that the primal-dual algorithm
makes progress in the sense of never generating the same 𝛼 or 𝛽 more than once. This is the case
for CEGAR, where the Lagrangian is monotone on 𝑌 .
    We show that many existing algorithms for a variety of problems can be described as instances
of our framework with a suitable Lagrangian. For safety verification, we provide Lagrangians that
capture CEGAR [Ball et al. 2001a; Clarke et al. 2000] (as described above), ICE learning [Garg et al.
2014], and primal-dual Houdini [Padon et al. 2022]. We show that our Lagrangian-based algorithmic
framework can also capture algorithms for termination verification [Podelski and Rybalchenko
2004], and for solving quantified linear real arithmetic (LRA) formulas [Farzan and Kincaid 2016].
    The Lagrangians succinctly capture the corresponding algorithms, and make the primal-dual
interaction explicit. Furthermore, they allow us to compare the different algorithms. For example,
our Lagrangian-based framework makes it clear that CEGAR makes progress by accumulating on
the proof side, ICE makes progress by accumulating on the counterexample side, and primal-dual
Houdini accumulates on both sides.
    In some cases, the Lagrangians shed new light on some of the ingredients of existing techniques.
For example, for termination verification, the Lagrangian perspective exposes that the disjunction
found in disjunctively well-founded transition invariants [Podelski and Rybalchenko 2004] provides
a mechanism to accumulate and make monotonic progress on the proofs side for termination proofs.
For solving quantified LRA formulas, we see that the strategy skeletons of [Farzan and Kincaid
2016] play a similar role in enabling monotonic progress.
    Another interesting aspect exposed by our unifying framework is the symmetry or asymmetry
between the primal and dual problems induced by the Lagrangian. For example, in primal-dual
Houdini and in quantified LRA solving, the primal and dual problems are symmetric in the sense
that they have an identical high-level structure. In contrast, in CEGAR and ICE the two sides of the
duality have different structures.
    The Lagrangians also provide a new perspective on the cases where the algorithms captured by
them fail, due to a connection between strong duality and the ability of the generic primal-dual
algorithm to terminate. Namely, in cases where the primal and dual solutions do not coincide
(i.e., strong duality does not hold), the primal-dual algorithm diverges. In the kinds of problems
we consider, strong duality often holds for an “idealized” version of the problem, where sets of
states can be infinite, or where any set of states can be captured by a predicate, but is lost when
restrictions are imposed on the values in 𝑋 and 𝑌 . For example, in the case of CEGAR, this may be
the case if the target system is safe, but the set of predicates considered is not sufficient to prove its
4                                             Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


safety. Thus, from the Lagrangian perspective, the loss of precision or expressiveness that prevents
termination is captured by the loss of strong duality.
   Equipped with Lagrangian based framework and the insights it provides, we go on to develop a
new primal-dual algorithm for solving formulas in fixpoint logic over quantified linear arithmetic.
Our new algorithm combines ideas from the aforementioned algorithms for termination verification
and quantified LRA solving. We derive it cleanly by defining a Lagrangian that combines elements
from the Lagrangians of these prior algorithms. A prototype implementation of this new algorithm
achieves promising results and solves some instances that state-of-the-art algorithms do not.
   In summary, this paper makes the following contributions:
      (1) We define the notions of a Lagrangian and the primal and dual optimization problems it
          induces in a way that generalizes the classic Lagrangian from linear programming and is
          general enough for the setting of verification algorithms.
      (2) We present a primal-dual search procedure that is parameterized by a Lagrangian and
          attempts to conclude either an upper bound on the value of the primal problem or a lower
          bound on the value of the dual problem. We provide a sufficient condition that ensures that
          the procedure makes progress.
      (3) We demonstrate that with suitable Lagrangians, several existing algorithms for a variety
          of program analysis and automated reasoning problems can be seen as instances of our
          framework, and some of their characteristics can be explained in terms of the Lagrangians.
      (4) We use our framework to derive a new primal-dual algorithm for solving formulas in
          fixpoint logic over quantified linear arithmetic. We present an initial empirical evaluation
          that shows the promise of the new algorithm.
   The rest of the paper is organized as follows. Section 2 recalls the classical notion of a Lagrangian
from linear programming, and introduces our generalization that is applicable to program verifi-
cation as well as an abstract primal-dual search algorithm that is parameterized by a Lagrangian.
Section 3 considers the safety verification problem and derives CEGAR and ICE learning as instances
of our framework. Section 4 derives primal-dual Houdini [Padon et al. 2022] as an instance of our
framework with a suitable Lagrangian. Section 5 formalizes algorithms for termination verification
based on disjunctive well-founded ranking functions [Podelski and Rybalchenko 2004] as instances
of the primal-dual procedure with a suitable Lagrangian, and Section 6 introduces a Lagrangian that
captures the algorithm of [Farzan and Kincaid 2016] for solving quantified linear real arithmetic
(LRA) formulas. Section 7 presents our new algorithm for fixpoint logic over quantified linear
arithmetic. We conclude the paper with a discussion of related work in Section 8.

2     Lagrange Duality for Linear Programming and Verification
Duality is a fundamental and useful concept in linear programming problems, and this section aims
to generalize this concept to verification problems. However, there are various differences between
linear programming problems and verification problems. For example, in a linear programming
problem, both the values to be controlled and to be optimized are continuous, whereas in a
verification problem, both are often discrete. This section introduces the Lagrange duality in a
general form applicable to both linear programming and verification problems. We also provide a
basic procedure to solve the optimization problem with a progress property.

2.1     Duality in Linear Programming
We briefly review the duality in linear programming. Let R be the set of reals and R ≥0 be the subset
of non-negative reals. For vectors 𝑥, 𝑦 ∈ R𝑛 , we write ⟨𝑥, 𝑦⟩ for the inner product and 𝑥 ≤ 𝑦 to
mean 𝑥𝑖 ≤ 𝑦𝑖 for every 𝑖. For a matrix 𝐴 ∈ R𝑛×𝑚 , its transpose is written as 𝐴𝑇 .
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                     5


   Consider the following linear program, which we shall call the primal problem:1
                                         minimize     ⟨𝑐, 𝑥⟩,       𝑥 ∈ R𝑛≥0,
                                         subject to 𝐴𝑥 = 𝑏,
where 𝑐 ∈ R𝑛 , 𝑏 ∈ R𝑚 and 𝐴 ∈ R𝑛×𝑚 are constants. We say 𝑥 ∈ R𝑛≥0 is feasible if 𝐴𝑥 = 𝑏. A feasible
𝑥 gives an upper bound ⟨𝑐, 𝑥⟩ of the optimal value, but a way to obtain a lower bound is not obvious.
   The dual problem is a useful tool to overcome the situation. It is defined as:
                                         maximize      ⟨𝜆, 𝑏⟩,      𝜆 ∈ R𝑚 ,
                                         subject to 𝐴𝑇 𝜆 ≤ 𝑐.
An important point is that the optimal value of this dual problem coincides with the optimal value
of the primal problem described above. So 𝜆 satisfying 𝐴𝑇 𝜆 ≤ 𝑐 provides a lower bound ⟨𝜆, 𝑏⟩ of
the optimal value of both the primal and dual problems. It is often the case that solving the primal
problem takes a long time but the dual problem can be solved quickly (and vice versa). Linear
programming algorithms often leverage this duality by exchanging information between the primal
and the dual problems.
   The primal and dual problems are connected by the Lagrangian, a function on 𝑥 and 𝜆 given by
                        𝐿(𝑥, 𝜆)     :=     ⟨𝑐, 𝑥⟩ − ⟨𝜆, 𝐴𝑥 − 𝑏⟩,        𝑥 ∈ R𝑛≥0, 𝜆 ∈ R𝑚 .
This is obtained by changing the hard constraint 𝐴𝑥 = 𝑏 to a soft constraint. The constraint is
violated if 𝐴𝑥 − 𝑏 is non-zero for some element, say (𝐴𝑥 − 𝑏)𝑖 ≠ 0, and then the objective function
is increased by −𝜆𝑖 (𝐴𝑥 − 𝑏)𝑖 . Since this penalty can be made arbitrarily large by choosing 𝜆𝑖 to
have the same sign as (𝐴𝑥 − 𝑏)𝑖 and a large absolute value, the worst choice of the weights 𝜆 for
the penalty makes the objective function ∞ if the constraint 𝐴𝑥 = 𝑏 is violated. So
                                                  (
                                                    ⟨𝑐, 𝑥⟩ if 𝐴𝑥 = 𝑏
                                sup 𝐿(𝑥, 𝜆) =
                                 𝜆                  ∞      if 𝐴𝑥 ≠ 𝑏.
Hence, the optimal value to the original problem is equivalent to inf 𝑥 sup𝜆 𝐿(𝑥, 𝜆), and the optimal
solution 𝑥 ∗ achieves sup𝜆 𝐿(𝑥 ∗, 𝜆) = inf 𝑥 sup𝜆 𝐿(𝑥, 𝜆).
  The Lagrangian also characterizes the dual problem. We have
                                      𝐿(𝑥, 𝜆) = ⟨𝑐, 𝑥⟩ − ⟨𝜆, 𝐴𝑥 − 𝑏⟩
                                                = ⟨𝑐, 𝑥⟩ − ⟨𝜆, 𝐴𝑥⟩ + ⟨𝜆, 𝑏⟩
                                                = ⟨𝑐, 𝑥⟩ − ⟨𝐴𝑇 𝜆, 𝑥⟩ + ⟨𝜆, 𝑏⟩
                                                = ⟨𝑐 − 𝐴𝑇 𝜆, 𝑥⟩ + ⟨𝜆, 𝑏⟩.
For a fixed 𝜆, if 𝑐 − 𝐴𝑇 𝜆 has a negative element, say (𝑐 − 𝐴𝑇 𝜆)𝑖 < 0, by choosing large 𝑥𝑖 > 0, the
value of 𝐿(𝑥, 𝜆) can be made arbitrary small. So
                                                 (
                                                    ⟨𝜆, 𝑏⟩ if 𝐴𝑇 𝜆 ≤ 𝑐
                                inf 𝐿(𝑥, 𝜆) =
                                 𝑥                 −∞      if 𝐴𝑇 𝜆 ̸ ≤ 𝑐.
Hence sup𝜆 inf 𝑥 𝐿(𝑥, 𝜆) is the optimum value for the dual problem.
  The coincidence of the primal and dual is expressed as
                        inf 𝑥 sup𝜆 𝐿(𝑥, 𝜆)      =    𝐿(𝑥 ∗, 𝜆 ∗ )   =    sup𝜆 inf 𝑥 𝐿(𝑥, 𝜆),
1We implicitly assume that {𝑥 ∈ R𝑛 | 𝐴𝑥 = 𝑏 } is non-empty and the optimal value is finite.
                                 ≥0
6                                              Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


where 𝑥 ∗ and 𝜆 ∗ are the optimal solutions to the primal and dual problems, respectively. Furthermore,
optimal solutions 𝑥 ∗ and 𝜆 ∗ are characterized by sup𝜆 𝐿(𝑥 ∗, 𝜆) = 𝐿(𝑥 ∗, 𝜆 ∗ ) = inf 𝑥 𝐿(𝑥, 𝜆 ∗ ). This
non-trivial but useful property is called the strong duality.

2.2    Generalized Lagrange Duality
In typical situations in linear programming and convex optimization, a Lagrangian takes vectors
and returns a real. Vectors and reals have useful operations and properties, and the development
of Lagrange duality exploits these operations and properties. On the contrary, the verification
community mainly deals with logical expressions, state transition systems, etc., which significantly
differ from reals and vectors. This subsection develops the Lagrange duality that works for such
situations with less structure.
   The following definition is probably the minimum requirement, assuming only that the upper
and lower bounds in the codomain of a Langrangian make sense.
    Definition 2.1 (Lagrangian). A Lagrangian is a function
                                            𝐿 : 𝑋 × 𝑌 −→ 𝑃
from sets 𝑋 and 𝑌 to a totally-ordered complete lattice 𝑃 = (𝑃, ≤).                                      □
  Similar to the case of linear programming, a Lagrangian 𝐿 : 𝑋 × 𝑌 −→ 𝑃 induces primal and dual
objective functions as well as the associated optimization problems.
   Definition 2.2. Let 𝐿 : 𝑋 × 𝑌 −→ 𝑃 be a Lagrangian. The primal objective function is 𝛼 ↦→
sup𝑦 ∈𝑌 𝐿(𝛼, 𝑦) and the primal optimization problem is to minimize the primal objective function,
i.e. to compute inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦). Similarly, the dual objective function is 𝛽 ↦→ inf 𝑥 ∈𝑋 𝐿(𝑥, 𝛽) and
the dual optimization problem is to compute sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦).                                       □
    Example 2.3. Let 𝐿1 : Z × Z −→ {−1, 1} (with −1 ≤ 1) be the Lagrangian defined by
                                                 (
                                                   −1 if 𝑥 ≥ 𝑦
                                    𝐿1 (𝑥, 𝑦) :=
                                                   1  if 𝑥 < 𝑦.
The primal objective function 𝛼 ↦→ sup𝑦 ∈Z 𝐿1 (𝛼, 𝑦) is the constant function to 1, so the optimal
outcome for the primal optimization problem is 1. The dual objective function 𝛽 ↦→ inf 𝑥 ∈Z 𝐿1 (𝑥, 𝛽)
is the constant function to −1, so the optimal outcome for the dual optimization problem is −1. Let
𝐿2 : Z × (Z → Z) −→ {−1, 1} be another Lagrangian defined by
                                                 (
                                                   −1 if 𝑥 ≥ 𝑦 (𝑥)
                                    𝐿2 (𝑥, 𝑦) :=
                                                   1  if 𝑥 < 𝑦 (𝑥).
The primal objective function 𝛼 ↦→ sup𝑦 ∈ (Z→Z) 𝐿2 (𝛼, 𝑦) is the constant function to 1, so the optimal
outcome for the primal optimization problem is 1. The dual objective function 𝛽 ↦→ inf 𝑥 ∈Z 𝐿2 (𝑥, 𝛽)
is 1 if ∀𝑥 ∈ Z.𝑥 < 𝛽 (𝑥) and −1 otherwise. For example, its value on 𝛽 ∗ (𝑥) = 𝑥 + 1 is 1. So the
optimal outcome for the dual optimization problem is 1.                                              □
  As example 2.3 shows, the optimal values for the primal and dual problems do not necessarily
coincide. However, even this very general setting enjoys a weak form of duality.
    Lemma 2.4. Every Lagrangian 𝐿 : 𝑋 × 𝑌 −→ 𝑃 enjoys the weak duality:
                               sup inf 𝐿(𝑥, 𝑦)     ≤     inf sup 𝐿(𝑥, 𝑦).
                               𝑦 ∈𝑌 𝑥 ∈𝑋                𝑥 ∈𝑋 𝑦 ∈𝑌
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                          7


   Proof. Since 𝐿(𝑥, 𝑦) ≤ sup𝑥 𝐿(𝑥, 𝑦) for every 𝑥 and 𝑦, we have inf 𝑦 𝐿(𝑥, 𝑦) ≤ inf 𝑦 sup𝑥 𝐿(𝑥, 𝑦)
for every 𝑥. So sup𝑥 inf 𝑦 𝐿(𝑥, 𝑦) ≤ inf 𝑦 sup𝑥 𝐿(𝑥, 𝑦).                                           □
  Example 2.5. Recall the Lagrangian 𝐿1 in example 2.3. We have
                                sup inf 𝐿1 (𝑥, 𝑦) = −1 < 1 = inf sup 𝐿(𝑥, 𝑦),
                                𝑦 ∈Z 𝑥 ∈Z                        𝑥 ∈Z 𝑦 ∈Z

so the inequality in Lemma 2.4 can be strict. In general, for 𝐿 : 𝑋 × 𝑌 −→ {−1, 1}, we have
inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦) = 1 if and only if ∀𝑥 .∃𝑦.𝐿(𝑥, 𝑦) = 1 holds, and similarly (sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) =
1) ⇔ (∃𝑦.∀𝑥 .𝐿(𝑥, 𝑦) = 1). So the weak duality is a mild generalization of the well-known fact
(∃𝑥 .∀𝑦.𝜑 (𝑥, 𝑦)) ⇒ (∀𝑦.∃𝑥 .𝜑 (𝑥, 𝑦)).                                                            □
   We say a Lagrangian 𝐿 : 𝑋 ×𝑌 −→ 𝑃 enjoys strong duality if sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) = inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦).
The Lagrangian 𝐿2 in example 2.3 enjoys strong duality. The strong duality is a desirable and useful
property, but we do not assume it.
   In the examples in this paper, a typical situation is as follows. A Lagrangian 𝐿 : 𝑋 × 𝑌 −→ 𝑃
has an “idealization” 𝐿 ′ : 𝑋 ′ × 𝑌 ′ −→ 𝑃 satisfying 𝑋 ⊆ 𝑋 ′ and 𝑌 ⊆ 𝑌 ′ , and the idealization 𝐿 ′
enjoys the strong duality and its optimal value coincides with the answer to a problem of interest
(e.g. whether a given system is safe). However, 𝑋 ′ and 𝑌 ′ are often not computationally tractable sets
such as the set P (States) of all subsets of an infinite set States. The Lagrangian 𝐿 is a computably
tractable approximation of 𝐿 ′ , typically obtained by replacing an intractable set (e.g. P (States)) with
a tractable one (e.g. the set Pfin (States) of finite subsets or an appropriate set of logical formulas
describing properties on States). This approximation, however, may lose desirable properties such
as strong duality, so we do not assume the strong duality of 𝐿.

2.3   A Primal-Dual Procedure
In the typical setting in this paper, we want to know whether the optimal value of the primal (or
dual) optimization problem of a given Lagrangian 𝐿 is bounded by a specific value, which we write as
0. For example, for the Lagrangian 𝐿CEGAR : 𝑋 × 𝑌 −→ {−1, 1} in Section 3.2, inf 𝑥 𝐿CEGAR (𝑥, 𝛽) = 1
if and only if 𝛽 witnesses the safety of the target system, so we are interested in whether the
optimal value sup𝑦 inf 𝑥 𝐿CEGAR (𝑥, 𝑦) of the dual optimization problem exceeds 0 or not, regarding
the codomain of 𝐿CEGAR as {−1 < 0 < 1}. This subsection develops a general procedure to solve
this problem.
   Suppose that we would like to know whether sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) ≥ 0 for a given Lagrangian
𝐿 : 𝑋 × 𝑌 −→ {−1, 1}. To affirmatively answer this question, it suffices to find a witness 𝛽 ∈ 𝑌
such that inf 𝑥 𝐿(𝑥, 𝛽) ≥ 0. Similarly, a negative answer is confirmed by finding 𝛼 ∈ 𝑋 such that
sup𝑦 𝐿(𝛼, 𝑦) ≤ 0. To find a witness 𝛼 or 𝛽, we start by choosing an arbitrary value 𝛽 0 ∈ 𝑌 as a
candidate for a witness 𝛽. If inf 𝑥 𝐿(𝑥, 𝛽 0 ) ≥ 0, we are done; otherwise, there exists 𝛼 1 ∈ 𝑋 such
that 𝐿(𝛼 1, 𝛽 0 ) < 0. Now 𝛼 1 can be a candidate for a negative witness 𝛼, so we check whether
sup𝑦 𝐿(𝛼 1, 𝑦) ≤ 0. We are done if it is the case, and otherwise, 𝐿(𝛼 1, 𝛽 1 ) > 0 for some 𝛽 1 ∈ 𝑌 , which
is the next candidate for a positive witness. In this way, we can iteratively update the candidates of
𝛼 and 𝛽 against each other until we finally find a positive or negative witness.
   While the above process might converge, it might also get stuck in a cycle. For example, if 𝛽 1
above is not a valid positive witness we will discover 𝛼 2 such that 𝐿(𝛼 2, 𝛽 1 ) < 0 as a counter-witness
to 𝛽 1 and our next candidate negative witness. But it may be the case that 𝐿(𝛼 2, 𝛽 0 ) ≥ 0, in which
case we may start repeating ourselves. That is, our sequence of candidate positive and negative
witnesses will be 𝛽 0, 𝛼 1, 𝛽 1, 𝛼 2, 𝛽 0, . . ., iterating back and forth between two pairs of candidate
positive and negative witnesses. One way to ensure progress, at least in the sense of not revisiting
the same candidates, is to assume additional structure on 𝑋 or 𝑌 (or possibly both). Suppose that 𝑋
8                                              Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


or 𝑌 is a join semilattice (𝑋, ⊑𝑋 , ⊔𝑋 ) or (𝑌 , ⊑𝑌 , ⊔𝑌 ) and that the Lagrangian 𝐿 is anti-monotone
on 𝑋 or monotone on 𝑌 . Then, when updating the candidate positive or negative witness, rather
than forgetting the previous candidate we can take the join of the previous candidate and the new
counter-witness. The option of this monotonic update appears in Algorithm 1, lines 6 and 10. As
we prove below, a monotonic update on either side is sufficient to prevent the search from getting
stuck and ensures it keeps exploring new possible solutions (on both sides).
                                             Algorithm 1 formalizes this idea. Algorithm 1 can be
                                          divided into two parts, namely lines 3–5 and lines 7–9. The
Algorithm 1 Primal-Dual Procedure former checks whether the current 𝛽 is a positive witness
                                          and, if it is not the case, produces a counter 𝛿. The latter is
function PrimalDual(𝐿)                    the dual of the former, checking whether 𝛼 is a negative wit-
  1: let 𝛼 ∈ 𝑋 , 𝛽 ∈ 𝑌
                                          ness and producing a counter 𝛾. We call the former the dual
  2: while true do
                                          witness check and the latter the primal witness check (recall
  3:     if inf 𝑥 𝐿(𝑥, 𝛽) ≥ 0 then        that the primal optimization problem is minimization, and
  4:          return (D, 𝛽)               the dual is maximization). Algorithm 1 does not tell us how
  5:     let 𝛿 ∈ {𝑥 ∈ 𝑋 | 𝐿(𝑥, 𝛽) < 0} to implement the subprocedures to solve these subproblems
  6:     𝛼 ← 𝛿 or 𝛼 ← 𝛼 ⊔𝑋 𝛿              and leaves the choice in lines 5 and 9 nondeterministic.
  7:     if sup𝑦 𝐿(𝛼, 𝑦) ≤ 0 then
  8:          return (P, 𝛼)                  Remark 2.6. There are similar variants of Algorithm 1.
                                          E.g., rather than checking the dual witness first, it is possible
  9:     let 𝛾 ∈ {𝑦 ∈ 𝑌 | 𝐿(𝛼, 𝑦) > 0}
                                          to start with the primal witness check. Also, instead of
 10:     𝛽 ← 𝛾 or 𝛽 ← 𝛽 ⊔𝑌 𝛾
                                          computing 𝛾 ∈ {𝑦 ∈ 𝑌 | 𝐿(𝛼, 𝑦) ̸ ≤ 0} and updating 𝛽 ←
                                          𝛽 ⊔ 𝛾, we can directly update 𝛽 to an element from {𝑦 ∈
                                          𝑌 | 𝐿(𝛼, 𝑦) ̸ ≤ 0, 𝑦 ≥ 𝛽}. We will refer to Algorithm 1 and
these variants collectively as the basic primal-dual procedure.                                          □
  Remark 2.7. Developing a practical procedure based on Algorithm 1 often requires optimizations.
Heuristics for choosing a “good” 𝛿 or 𝛾 on lines 5 or 9 can have a significant impact on performance.
One could also consider managing additional information beyond 𝛼 and 𝛽 to solve the primal and
dual witness check problems faster. Algorithm 1 just describes a skeleton of practical procedures. □
Partial Correctness and Progress. The partial correctness (i.e., correctness assuming termination)
and progress properties of Algorithm 1 are formalized in the following theorems.
    Theorem 2.8. PrimalDual in Algorithm 1 is correct in the following sense:
      • If (P, 𝛼) = PrimalDual(𝐿), then 0 is an upper bound of the optimal value of the primal
        optimization problem and 𝛼 is a witness: inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦) ≤ sup𝑦 𝐿(𝛼, 𝑦) ≤ 0.
      • If (D, 𝛽) = PrimalDual(𝐿), then 0 is a lower bound of the optimal value of the dual optimization
        problem and 𝛽 is a witness: sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) ≥ inf 𝑥 𝐿(𝑥, 𝛽) ≥ 0.
  Proof. If the procedure returns (P, 𝛼), then the value 𝛼 has passed the condition in line 7, hence
sup𝑦 𝐿(𝛼, 𝑦) ≤ 0. The case of (D, 𝛽) is similar.                                                   □
   Theorem 2.9. Let 𝐿 : 𝑋 × 𝑌 −→ 𝑃 be a Lagrangian. Assume that 𝑋 or 𝑌 is a join semilattice, and
𝐿 is anti-monotone on 𝑋 or monotone on 𝑌 . Then, PrimalDual in Algorithm 1 enjoys progress, i.e. it
does not assign the same value to 𝛼 or 𝛽 twice, provided that we always choose 𝛼 ← 𝛼 ⊔𝑋 𝛿 in line 6
(or that we always choose 𝛽 ← 𝛽 ⊔𝑌 𝛾 in line 10).
  Proof. We focus on the case where 𝑌 is a join semilattice and 𝛽 is updated monotonically (the
other case is similar). We write 𝛼𝑛 , 𝛽𝑛 and 𝛾𝑛 for the values at the 𝑛-th iteration of the loop. Assume
for contradiction that 𝛼𝑖 = 𝛼 𝑗 for some 𝑖 < 𝑗. Then 𝐿(𝛼𝑖 , 𝛾𝑖 ) ̸ ≤ 0. Since 𝛾𝑖 ≤ 𝛽𝑖 ≤ 𝛽 𝑗 −1 , we have
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                9


𝐿(𝛼𝑖 , 𝛽 𝑗 −1 ) ̸ ≤ 0 by the monotonicity of 𝐿 on 𝑌 . We have 𝐿(𝛼 𝑗 , 𝛽 𝑗 −1 ) ̸ ≥ 0 by the definition of 𝛼 𝑗 , a
contradiction. We show that 𝛽𝑖 ≠ 𝛽 𝑗 for every 𝑖 ≠ 𝑗. Since 𝛽𝑖 ≤ 𝛽𝑖+1 ≤ · · · ≤ 𝛽 𝑗 for 𝑖 ≤ 𝑗, it suffices
to show that 𝛽𝑖 < 𝛽𝑖+1 , or equivalently that 𝛽𝑖 ≠ 𝛽𝑖+1 . Assume for contradiction that 𝛽𝑖 = 𝛽𝑖+1 . By
the definition of 𝛽𝑖+1 , we have 𝐿(𝛼𝑖+1, 𝛽𝑖+1 ) ̸ ≤ 0. So 𝐿(𝛼𝑖+1, 𝛽𝑖 ) ̸ ≤ 0 since 𝛽𝑖 = 𝛽𝑖+1 . By the definition
of 𝛼𝑖+1 , we have 𝐿(𝛼𝑖+1, 𝛽𝑖 ) ̸ ≥ 0, a contradiction.                                                         □

Termination. Unlike partial correctness and progress, termination of Algorithm 1 is generally not
guaranteed (except for trivial cases where 𝑋 or 𝑌 are finite). This is because Algorithm 1 is a
general procedure applicable to a variety of verification problems, many of which are undecidable.
Our Lagrangian framework, however, provides a necessary condition for termination, relating
termination and strong duality.
   Theorem 2.10. Assume 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} does not enjoy the strong duality property, i.e.,
inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦) = 1 while sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) = −1. Then Algorithm 1 cannot terminate. A similar
claim holds if 0 is in the duality gap in the sense that
                                    sup inf 𝐿(𝑥, 𝑦) < 0 < inf sup 𝐿(𝑥, 𝑦).
                                      𝑦   𝑥                   𝑥    𝑦

   Proof. Since sup𝑦 𝐿(𝛼, 𝑦) > 0 and inf 𝑥 𝐿(𝑥, 𝛽) < 0 for every 𝛼 ∈ 𝑋 and 𝛽 ∈ 𝑌 , the conditions
in lines 3 and 7 are never met.                                                                 □

  A typical example of the above situation is CEGAR satisfying the following conditions: the target
system is safe, and the set of available predicates is strong enough to refute individual suspicious
error traces but not enough to prove the safety of the entire system.
   Example 2.11. Algorithm 1 may diverge, even for a Lagrangian with strong duality. Let Z∞ :=
Z∪{∞} and 𝐿3 : Z×Z∞ −→ {−1, 1} be the Lagrangian defined by 𝐿3 (𝑥, 𝑦) = 1 ⇔ (𝑥 < 𝑦). Note that
inf 𝑥 𝐿3 (𝑥, ∞) = 1 but inf 𝑥 𝐿3 (𝑥, 𝛽) = −1 for every 𝛽 ≠ ∞. So the loop continues until 𝛽 becomes ∞.
However, one can always choose a finite 𝛾 in line 9, resulting in divergence of the procedure. □
   Let us now turn our attention to the opposite, i.e. ideas to ensure termination in some situations.
Assume a Lagrangian 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} with a positive witness 𝛽 satisfying inf 𝑥 𝐿(𝑥, 𝛽) = 1.
Stratification [Jhala and McMillan 2006; Unno et al. 2021] is a technique to ensure the procedure
                                                                                              Ò
eventually finds a positive witness (possibly different from 𝛽). The idea is to decompose 𝑌 = 𝑛∈N 𝑌𝑛
into an infinite union of finite sets, and to force the procedure to find 𝛾 ∈ 𝑌𝑙 with minimum 𝑙 (in
line 9).
   By combining monotonicity as formulated in Theorem 2.9 with stratification we can ensure
termination, assuming a suitable positive or negative witness exists. The conditions for termination
vary between the case where monotonicity and stratification are applied at the same side (i.e., both
to 𝑋 or to 𝑌 ) or at different sides (i.e., 𝑋 is a semilattice with monotonicity and 𝑌 is stratified, or
vice versa). Below we analyze the case where 𝑋 is a semilattice and 𝑌 is stratified and then the case
where 𝑌 is a semilattice and also stratified. The other two cases are dual.
   Theorem 2.12. Let 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} be aÒLagrangian where 𝑋 is a join semilattice with 𝐿
anti-monotone on 𝑋 , and 𝑌 is stratified, i.e., 𝑌 = 𝑛∈N 𝑌𝑛 such that 𝑌𝑛 is finite for each 𝑛. Assume
that 𝐿 has a positive witness 𝛽 ∗ , i.e. inf 𝑥 𝐿(𝑥, 𝛽 ∗ ) = 1. Then Algorithm 1 terminates provided that 𝛾 in
line 9 is chosen from the smallest possible layer, i.e. 𝛾 ∈ 𝑌𝑙 with 𝑙 = min{𝑘 ∈ N | ∃𝛾 ∈ 𝑌𝑘 .𝐿(𝛼, 𝛾) > 0}.
   Proof. Assume 𝛽 ∗ ∈ 𝑌𝑛 . Then 𝑌≤𝑛 := 𝑛𝑖=0 𝑌𝑖 is a finite set. Algorithm 1 terminates before |𝑌≤𝑛 |
                                                Ð
iterations because of progress (Theorem 2.9) and because 𝛽 ∈ 𝑌≤𝑛 is an invariant of the procedure,
since 𝛽 ∗ is always a possible choice in line 9 and we choose 𝛾 from the smallest possible layer. □
10                                                 Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


  Theorem 2.12 guarantees termination (when a positive witness exists) but imposes an additional
condition on the choice of 𝛾, making the implementation of line 9 more difficult. It is therefore
important to design a stratification for which the modified line 9 can be implemented efficiently.
  Stratification and monotonicity can also be on the same side (i.e., 𝑋 or 𝑌 ). In a stratification of a
semilattice the layers need not be finite, only of finite height, and they must be closed under join.
   Theorem 2.13. Let 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} be a Lagrangian and assume that 𝑌 is a join semilattice
and 𝐿 is monotone on 𝑌 . Assume a join semilattice homomorphism 𝑟 : 𝑌 −→ N, i.e. 𝑟 (𝑦 ⊔ 𝑦 ′ ) =
max(𝑟 (𝑦), 𝑟 (𝑦 ′ )) and consider the induced stratification 𝑌𝑛 := {𝑦 ∈ 𝑌 | 𝑟 (𝑦) = 𝑛}. Suppose that each
𝑌𝑛 is of finite height, i.e., it has no infinite increasing chain 𝑦0 ⊏ 𝑦1 ⊏ · · · ∈ 𝑌𝑛 . We assume that the
procedure always chooses 𝛽 ← 𝛽 ⊔𝑌 𝛾 in line 10 and that 𝛾 in line 9 is chosen from the smallest possible
layer. Then the procedure terminates provided that there exists a positive witness 𝛽 ∗ .
     Proof. Similar to that of Theorem 2.12, combining progress and the invariant 𝑟 (𝛽) ≤ 𝑟 (𝛽 ∗ ).            □
   Remark 2.14. Although we were only interested in the sign of the optimal outcome of a La-
grangian, seeking the optimal outcome can also be useful for verification in some contexts. In
this setting, it is natural to choose 𝛾 in line 9 in Algorithm 1 from those achieveing the best out-
come against 𝛼 (i.e. 𝐿(𝛼, 𝛾) = max{𝐿(𝛼, 𝑦) | 𝑦 ∈ 𝑌 }). A Lagrangian 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} with a
                     Ò
stratification 𝑌 = 𝑛∈N 𝑌𝑛 induces the stratified Lagrangian b   𝐿 : 𝑋 × 𝑌 −→ R defined by
                                            (
                                              −1 if 𝐿(𝑥, 𝑦) = −1
                            𝐿(𝑥, 𝑦) :=
                            b
                                              1/𝑛 if 𝐿(𝑥, 𝑦) = 1 and 𝑦 ∈ 𝑌𝑛 .

The procedure seeking the optimal outcome of b
                                             𝐿 is the stratified version of Algorithm 1 mentioned
in Theorems 2.12 and 2.13.                                                                      □
Summary: Requirements for Applying our Framework. We conclude this section by summarizing the
process to apply Algorithm 1.
    • Develop a Lagrangian 𝐿 : 𝑋 × 𝑌 −→ 𝑃 with the following conditions:
          – Soundness: At least one of inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦) ≤ 0 and sup𝑦 inf 𝑥 𝐿(𝑥, 𝑦) ≥ 0 is related
            to the problem we would like to solve.
          – Monotonicity: At least one of 𝑋 or 𝑌 is a join-lattice, and 𝐿 is (anti-)monotone on
            that component.
    • Develop solvers for both the primal and dual witness check problems. Possibly design
       heuristics for the nondeterministic choices in lines 5 and 9 that lead to good generalization
       in practice.
  Remark 2.15. Hereafter, we assume that the codomain 𝑃 of a Lagrangian is a finite subset of Z
with the order inherited from Z. All the examples in this paper satisfy this assumption.      □

3     Lagrangians for Safety Verification: CEGAR and ICE
This section provides the first examples of Lagrangians in verification. We provide two Lagrangians
for the safety verification problem, which induce CEGAR and ICE.

3.1     Problem setting
This section focuses on the safety verification problem of a given transition system, which is a
problem asking if one can reach a bad state in a given transition system. We give a formal definition.
   Definition 3.1. A transition system S is a tuple (|S|, 𝐼 S, ⇝S, 𝐵 S ) where |S| is the set of states, 𝐼 S ⊆ |S|
is the initial states, (⇝S ) ⊆ |S| × |S| is the transition relation, and 𝐵 S ⊆ |S| is the set of bad states.
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                  11


A state 𝑠 ∈ |S| is reachable if there exists a transition sequence 𝐼 S ∋ 𝑠 0 ⇝S 𝑠 1 ⇝S . . . ⇝S 𝑠𝑛 = 𝑠
for some 𝑛 ≥ 0. The transition system S is safe if no bad state 𝑠 ∈ 𝐵 S is reachable. Otherwise S is
unsafe.                                                                                             □
  Example 3.2. Let S0 be the transition system given by |S0 | = Z, 𝐼 S0 = {0}, (𝑥 ⇝S0 𝑦) ⇔ 𝑥 + 1 = 𝑦
and 𝐵 S0 = {−3}. The set of reachable states is {𝑛 ∈ Z | 𝑛 ≥ 0}, so S0 is safe.                    □
     The unsafety of a transition system can be witnessed by a transition sequence 𝐼 S ∋ 𝑠 0 ⇝S 𝑠 1 ⇝S
. . . ⇝S 𝑠𝑛 ∈ 𝐵 S from an initial state 𝑠 0 to a bad state 𝑠𝑛 . A safety proof cannot always be possible in
such an obvious way. A common approach is to consider an appropriate set of predicates P and try
to find a safe inductive invariant.
   Definition 3.3. A predicate set over a transition system S is a set P together with a satisfaction
relation (|=) ⊆ |S| × P. When (𝑠, 𝑝) ∈ (|=), we write 𝑠 |= 𝑝 and say that 𝑠 satisfies 𝑝. A subset
𝑋 ⊆ |S| is an inductive invariant if it satisfies the following conditions: (1) 𝐼 S ⊆ 𝑋 (initiation); and
(2) (𝑠 ∈ 𝑋 ) ∧ (𝑠 ⇝S 𝑠 ′ ) =⇒ (𝑠 ′ ∈ 𝑋 ) (consecution). If an invariant further satisfies (3) 𝐵 S ∩ 𝑋 = ∅
(safety), we call it a safe inductive invariant. A predicate 𝑝 ∈ P is a (safe) inductive invariant if so is
{𝑠 ∈ |S| | 𝑠 |= 𝑝}.                                                                                      □
  Example 3.4. Recall the transition system S0 in example 3.2. An inductive invariant is 𝑝 (𝑥) :⇔
(𝑥 ≥ 0). There may be more than one inductive invariant for a system. For example, 𝑝 ′ (𝑥) :⇔ (𝑥 >
−2) is another inductive invariant for S0 .                                                      □

3.2   Lagrangian for CEGAR
Counter-Example Guided Abstraction Refinement (known as CEGAR) is a famous technique for the
safety verification problem [Ball et al. 2001a; Clarke et al. 2000]. The CEGAR procedure manages a
finite subset 𝐴 ⊆ P of the predicate set, and it iterates the following two phases.
    (a) Abstract the target transition system S by using the predicate set 𝐴 and check its safety. If
        the abstract system is safe, then S is safe; otherwise, the abstract transition system has a
        transition sequence to a bad state.
    (b) Check the feasibility of the abstract transition sequence to a bad state. If it is feasible, then S
        is unsafe; otherwise, add predicates to 𝐴 that suffice to show the infeasibility of the abstract
        transition sequence.
   The abstract transition system for a predicate set 𝐴 ⊆ P is given as follows. The states 𝑠, 𝑠 ′ ∈ |S|
                                            𝐴
are indistinguishable by 𝐴, written 𝑠 ≈ 𝑠 ′ , if (𝑠 |= 𝑝) ⇔ (𝑠 ′ |= 𝑝) for every 𝑝 ∈ 𝐴. A state of the
                                                                                      𝐴          𝐴
abstract transition system is an equivalence class [𝑠] 𝐴 := { 𝑠 ′ ∈ |S| | 𝑠 ≈ 𝑠 ′ } of ≈. The abstract
transition system has a transition from [𝑠 1 ] 𝐴 to [𝑠 2 ] 𝐴 if there exists a transition from a state in
[𝑠 1 ] 𝐴 to a state in [𝑠 2 ] 𝐴 (i.e. [𝑠 1 ] 𝐴 ∋ 𝑠 1′ ⇝S 𝑠 2′ ∈ [𝑠 2 ] 𝐴 for some 𝑠 1′ and 𝑠 2′ ). An abstract state
[𝑠] 𝐴 is an initial state (resp. a bad state) if it contains an initial state (resp. a bad state). We write
S𝐴 = (|S|𝐴 , 𝐼 S𝐴 , ⇝𝐴S , 𝐵𝐴
                           S
                             ) for the abstract transition system.
    CEGAR can be seen as an instance of the Lagrangian-based primal-dual method. Let
                                      𝑋 := |S| ∗     and 𝑌 := Pfin (P)
where |S| ∗ is the set of all finite sequences over |S| and Pfin (P) is the set of all finite subsets of P.
We regard 𝑌 = Pfin (P) as a poset ordered by set-inclusion ⊆. The Lagrangian is given by
                                     (
                                       −1     if 𝐼 S𝐴 ∋ [𝑠 0 ] 𝐴 ⇝𝐴S [𝑠 1 ] 𝐴 ⇝𝐴S · · · ⇝𝐴S [𝑠𝑛 ] 𝐴 ∈ 𝐵𝐴
   𝐿CEGAR ((𝑠 0𝑠 1 . . . 𝑠𝑛 ), 𝐴) :=                                                                   S
                                       1      otherwise.
                   ′
An “idealization” 𝐿CEGAR of 𝐿CEGAR is obtained by setting P to be P (|S|).
12                                               Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


Algorithm 2 CEGAR in the standard description (left) and as a primal-dual method (right)
   1: let 𝐴 ← ∅                                     1: let 𝐴 ← ∅
   2: while true do                                 2: while true do
   3:     if S𝐴 is safe then                        3:     if inf 𝜏 𝐿CEGAR (𝜏, 𝐴) ≥ 0 then
   4:          return (safe, 𝐴)                     4:          return (safe, 𝐴)
   5:     let 𝜏 be an abstract error trace in S𝐴    5:     let 𝜏 ∈ {𝜏 ∈ |S| ∗ | 𝐿CEGAR (𝜏, 𝐴) ̸ ≥ 0}
   6:     if feasibility of 𝜏 is not refutable then 6:     if sup𝛼 𝐿CEGAR (® 𝑠 , 𝛼) ≤ 0 then
   7:          return (unknown, 𝜏)                  7:          return (unknown, 𝜏)
   8:     let 𝛼 be an infeasibility witness for 𝜏   8:     let 𝛼 ∈ {𝛼 ∈ 𝑌 | 𝐿CEGAR (𝜏, 𝛼) ̸ ≤ 0}
   9:     𝐴 ←𝐴∪𝛼                                    9:     𝐴 ←𝐴∪𝛼

                       ′
     Proposition 3.5. 𝐿CEGAR enjoys strong duality, and its optimal value is 1 if and only if S is safe.
   Proof. If S is unsafe, a concrete error trace 𝐼 S ∋ 𝑠 0 ⇝S . . . ⇝S 𝑠𝑛 ∈ 𝐵 S is an optimal choice of
𝑋 . Otherwise, the set 𝑅 of reachable states is a safe inductive invariant and {𝑅} is optimal for 𝑌 . □
     Corollary 3.6. If sup𝑦 inf 𝑥 𝐿CEGAR (𝑥, 𝑦) = 1, then S is safe.                                         □
  If inf 𝑥 sup𝑦 𝐿CEGAR (𝑥, 𝑦) = −1, then we know that 𝑌 is insufficient to prove the safety of S but
not to say that S is unsafe. However, given 𝛼 such that sup𝑦 𝐿CEGAR (𝛼, 𝑦) = −1, we can examine it
and may conclude that S is unsafe.
  Corollary 3.6 ensures the soundness criterion. The monotonicity criterion is trivially met on 𝑌 .
We examine the primal and dual witness check problems.
      • The dual witness check asks to find 𝜏 such that 𝐿CEGAR (𝜏, 𝐴) < 0. This is equivalent to the
         safety verification of the abstract transition system S𝐴 , and 𝜏 is an error trace.
      • The primal witness check asks to find 𝐴 such that 𝐿CEGAR (𝜏, 𝐴) > 0. This is the so-called
         abstraction refinement and has well-known procedures.
So Algorithm 1 with 𝐿CEGAR is applicable to solve the safety verification problem. Algorithm 2
describes the resulting procedure, which is the standard CEGAR procedure.
   Remark 3.7. The stratified version of CEGAR [Jhala and McMillan 2006] can be understood    Ò    in
the Lagrangian framework as follows. In this setting, the set of predicates is stratified: P = 𝑛∈N P𝑛 .
This induces a stratification on 𝑌 = Pfin (P) as
                                               Ðfollows: 𝐴 ∈ Pfin (P) belongs to the 𝑛-th level where
𝑛 is the minimum number such that 𝐴 ⊆ 𝑛𝑖=0 P𝑖 . By Theorem 2.12, the CEGAR procedure is
guaranteed to terminate for instances with positive witnesses, as long as newly added predicates
are always chosen from the smallest possible level.                                                 □

3.3     Lagrangian for ICE
The ICE learning [Garg et al. 2014] is another approach to the safety verification problem. It is
described as an interaction between a teacher and a learner. The teacher tells a finite information
on the system, and the leaner generates a candidate of satefy proof that works for the provided
information. Then the teacher checks if the candidate is a proof against the whole system, and if
not, tells an additional information on the system that explains why the candidate generated by
the leaner is insufficient. Example 3.8 explains the interaction by an example.
    Example 3.8. We prove the safety of S0 in example 3.2 by ICE. Information passed from the
teacher to the learner is a triple (𝐼 ′, ⇝′, 𝐵 ′ ) of finite subsets of 𝐼 S0 , ⇝S0 and 𝐵 S0 , respectively. Let
𝑆 0′ = (𝐼 0′, ⇝0′ , 𝐵 0′ ) = (∅, ∅, ∅) be the initial choice. The learner proposes an inductive invariant
for the subsystem 𝑆 0′ : the subsystem 𝑆 0′ does not have a bad state, so 𝑝 0 (𝑥) :⇔ ⊤ is an inductive
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                          13


Algorithm 3 ICE in the standard description (left) and as a primal-dual method (right)
   1: let 𝑆 ′ ← (∅, ∅, ∅)                        1: let 𝑆 ′ ← (∅, ∅, ∅)
   2: while true do                              2: while true do
   3:      if Safety of 𝑆 ′ is unprovable then   3:      if sup𝑝 𝐿ICE (𝑆 ′, 𝑝) = −1 then
                                    ′
   4:           return (unknown, 𝑆 )             4:           return (unknown, 𝑆 ′ )
                                         ′
   5:      let 𝑝 be a safety proof for 𝑆         5:      let 𝑝 ∈ {𝑝 ∈ 𝑌 | 𝐿ICE (𝑆 ′, 𝑝) = 1}
   6:      if 𝑝 is a safety proof for S then     6:      if inf 𝑆 ′′ 𝐿ICE (𝑆 ′′, 𝑝) = 1 then
   7:           return (safe, 𝑝)                 7:           return (safe, 𝑝)
                 ′′
   8:      let 𝑆 be counterexamples for 𝑝        8:      let 𝑆 ′′ ∈ {𝑆 ′′ ∈ 𝑋 | 𝐿ICE (𝑆 ′′, 𝑝) = −1}
             ′      ′    ′′
   9:     𝑆 ←𝑆 ∪𝑆                                9:     𝑆 ′ ← 𝑆 ′ ∪ 𝑆 ′′


invariant for the subsystem 𝑆 0′ . Then the teacher checks if 𝑝 0 is an inductive invariant for S0 , but it
is obviously not. The teacher adds a bad state −3 to the subsystem, resulting in 𝑆 1′ = (∅, ∅, {−3}).
The leaner proposes an inductive invariant for the subsystem 𝑆 1′ : the subsystem does not have
an initial state, so 𝑝 1 (𝑥) :⇔ ⊥ is an inductive invariant for the subsystem 𝑆 1′ . The teacher then
checks if 𝑝 1 is an inductive invariant for S0 , but it is not. The teacher adds an initial state 0 to
the subsystem: 𝑆 2′ = ({0}, ∅, {−3}). The learner proposes an inductive invariant for the subsystem
𝑆 2′ : one can choose 𝑝 2 (𝑥) :⇔ (𝑥 mod 2 = 0), which separates the initial state 0 from the bad
state −3. The teacher then checks if 𝑝 2 is an inductive invariant for S0 , but it is not because 𝑝 2 is
not closed under the transition relation. The teacher adds some examples of transitions, yielding
𝑆 3′ = ({0}, {(0, 1), (2, 3), (8, 9), (−4, −3)}, {−3}). Now, the learner has a much narrower range of
candidates: an inductive invariant 𝑝 3 for 𝑆 3′ must be true on 0, 1 and must be false on −4, −3. A
candidate is 𝑝 3 (𝑥) :⇔ (𝑥 > −2). The teacher can ensure that 𝑝 3 is an inductive invariant for S0 . □
  Then ICE-learning can be seen as an instance of the Lagrangian-based primal-dual method. Let
                         𝑋 := Pfin (𝐼 S ) × Pfin (⇝S ) × Pfin (𝐵 S )     and 𝑌 := P.
Intuitively, 𝑋 tells us partial information on the transition system. The Lagrangian is given by
                            (
                    ′         1      𝑝 is an inductive invariant for the subsystem 𝑆 ′ of S
             𝐿ICE (𝑆 , 𝑝) =
                              −1 otherwise.
So 𝐿ICE (𝑆 ′, 𝜑) is 1 if and only if 𝜑 witnesses the safety of the subtransition system 𝑆 ′ . The “idealiza-
       ′
tion” 𝐿ICE  of 𝐿ICE is obtained by setting 𝑌 := P (|S|).
                    ′ enjoys the strong duality, and its optimal value is 1 iff S is safe.
  Proposition 3.9. 𝐿ICE
  Proof. If S is safe, an optimal choice of 𝑌 is the set of reachable states. If S is unsafe, an optimal
choice of 𝑋 is an error trace.                                                                        □

  Corollary 3.10. If sup𝑦 inf 𝑥 𝐿ICE (𝑥, 𝑦) = 1, then S is safe.                                         □
  The Lagrangian 𝐿ICE satisfies both soundness and monotonicity criteria. Unlike in the CEGAR
case, the 𝑋 component has a join semilattice structure and 𝐿ICE is anti-monotone on 𝑋 . We examine
the primal and dual witness checks.
      • The dual witness check asks to find 𝑆 ′ such that 𝐿ICE (𝑆 ′, 𝑝) = −1. This is the teacher.
      • The primal witness check asks to find 𝑝 such that 𝐿ICE (𝑆 ′, 𝑝) = 1. This is the learner.
So the variant of Algorithm 1 that monotonically updates 𝛼 is applicable to this setting. Algorithm 3
describes the resulting procedure (which, unlike Algorithm 1, starts from the dual side).
14                                               Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


4     Lagrangian for Primal-Dual Houdini
This section analyzes primal-dual Houdini [Padon et al. 2022], a procedure that motivated this
paper, in terms of the Lagrange duality. The Lagrangian for primal-dual Houdini yields monotone
progress on both sides of the duality; it is symmetric in the sense that the primal and dual problems
have the same high-level structure and can be swapped, changing the sign of the Lagrangian; and
interestingly showing that the Lagrangian is well-defined requires a non-trivial lemma.

4.1 Warmup: CEGAR for Cartesian Abstraction
As a stepping stone towards developing a Lagrangian for primal-dual Houdini, we first consider a
version of CEGAR that operates not on predicate abstraction as in Section 3.2, but on Cartesian
abstraction [Ball et al. 2001b]. Given a set of predicates 𝑃, the Cartesian or conjunctive abstraction
it induces considers inductive invariants that can be expressed as a conjunction of predicates
from 𝑃. This abstraction is coarser than the Boolean or predicate abstraction, which considers
invariants that can be expressed as an arbitrary Boolean formula over predicates from 𝑃 (i.e., using
conjunction, disjunction, and negation). While in the case of predicate abstraction the abstract
counterexample takes the form of an abstract trace (i.e., a sequence of transitions), in the case of
Cartesian abstraction the abstract counterexample can be thought of as a directed acyclic graph
(DAG) of transitions. We abstract over the details of the DAG structure, and focus just on the set of
states that participate in the abstract counterexample.
    As in Section 3, let us fix a transition system S (Definition 3.1) and a predicate set P (Definition 3.3),
i.e. a set with a satisfaction relation (|=) ⊆ |S| × P. To define a Lagrangian for CEGAR for Cartesian
abstraction, we let

                                    𝑋 = Pfin (|S|) and 𝑌 = Pfin (P).
   We now define the value of 𝐿CEGAR∧ (𝑥, 𝑦) according to whether there is a conjunctive inductive
invariant over predicates from 𝑦 that proves that S|𝑥 is safe, where S|𝑥 is the transition system S
restricted to states from 𝑥, i.e., |S|𝑥 | = 𝑥, 𝐼 S|𝑥 = 𝐼 S ∩ 𝑥, ⇝S|𝑥 =⇝S ∩ (𝑥 × 𝑥), and 𝐵 S|𝑥 = 𝐵 S ∩ 𝑥. We
define the Lagrangian 𝐿CEGAR∧ : 𝑋 × 𝑌 −→ {−1, +1}.
                                   (
                                     −1 if no 𝜗 ⊆ 𝑦 is a safe inductive invariant of S|𝑥
                𝐿CEGAR∧ (𝑥, 𝑦) =                                                                         (1)
                                     +1 otherwise
   Given a finite set of predicates 𝑦 ∈ 𝑌 , checking whether inf 𝑥 𝐿CEGAR∧ (𝑥, 𝑦) ≥ 0 (i.e., the dual
witness check) amounts to checking whether S can be proven safe using the Cartesian abstraction
defined by 𝑦. The well-known Houdini algorithm [Flanagan et al. 2001; Flanagan and Leino 2001] is a
procedure for answering this question, and it operates by a straightforward fixpoint computation to
compute the strongest inductive invariant of S that can be expressed as a conjunction of predicates
from 𝑦. The algorithm also computes a set of (at most |𝑦|) transitions that show why no larger
subset of 𝑦 is an inductive invariant for S; or, in our terms, it produces a set of states 𝑥 such that no
larger subset of 𝑦 is an inductive invariant for S|𝑥 .
   Given a finite set of states 𝑥, the primal witness check, i.e., checking if sup𝑦 𝐿CEGAR∧ (𝑥, 𝑦) ≤ 0,
corresponds to finding the right predicates that can be used to prove safety of S|𝑥 using Cartesian
abstraction. That is, it corresponds to abstraction refinement, similarly to the primal witness check
problem in Section 3.2.

4.2    Induction Duality
Let S be a transition system and P be a predicate set. For a subset 𝜗 ⊆ P of predicates, 𝑠 |= 𝜗 means
∀𝑝 ∈ 𝜗 . 𝑠 |= 𝑝. Similarly, for a subset 𝜛 ⊆ |S| of states, 𝜛 |= 𝑝 means ∀𝑠 ∈ 𝜛. 𝑠 |= 𝑝. Finally, 𝜛 |= 𝜗
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                                   15


means 𝑠 |= 𝑝 for every 𝑠 ∈ 𝜛 and 𝑝 ∈ 𝜗. Below we sometimes abuse the notation and use 𝑝 either
for a single predicate or for a finite set of predicates. We extend the definition of an inductive
invariant (Definition 3.3) to finite sets of predicates by interpreting the sets conjunctively. That is,
                                                                                                         Ó
a finite set of predicates 𝜗 ⊆ P is an inductive invariant of if its conjunction, denoted 𝜗, is an
inductive invariant.
   Primal-dual Houdini operates by analyzing S together with another transition system I =
(|I|, 𝐼 I, ⇝I, 𝐵 I ) which is defined over finite sets of predicates, i.e., |I| = Pfin (P). I is assumed to be
an induction dual of S, meaning that the following conditions are satisfied:2
 (ID1) 𝑠 0 |= 𝑝 for every 𝑠 0 ∈ 𝐼 S and 𝑝 ∈ |I|, that is, the initial states satisfy all predicates;
 (ID2) 𝑠 |= 𝑝 0 for every 𝑠 ∈ |S| and 𝑝 0 ∈ 𝐼 I , that is, the initial predicates are satisfied by all states;
 (ID3) 𝑠 ̸ |= 𝑝 for every 𝑠 ∈ 𝐵 S and 𝑝 ∈ 𝐵 I , that is, every bad state is excluded by every “bad”
           predicate set; and
 (ID4) if (𝑠 ⇝S 𝑠 ′ ) ∧ (𝑝 ⇝I 𝑝 ′ ) ∧ (𝑠 |= 𝑝) ∧ (𝑠 |= 𝑝 ′ ) ∧ (𝑠 ′ |= 𝑝), then (𝑠 ′ |= 𝑝 ′ ), that is, transitions
           in ⇝S and in ⇝I restrict each other in a particular way.
   The intuition behind this definition is that traces in I represents incremental induction proofs
over S. Specifically, (ID4) means that if we assume 𝑝 is an invariant (of S) and 𝑝 ⇝I 𝑝 ′ , then 𝑝 ′ is
also an invariant. As the following lemma shows, a path in I implies an inductive invariant of S.
   Lemma 4.1 ([Padon et  Ðal. 2022]). Assume induction-dual transition systems S and I. If 𝐼 I ∋ 𝑝 0 ⇝I
𝑝 1 ⇝I . . . ⇝I 𝑝𝑛 , then 𝑛𝑖=0 𝑝𝑖 is an inductive invariant for S.
    Proof. Initiation follows from (ID1). For consecution, suppose 𝐼 I ∋ 𝑝 0 ⇝I 𝑝 1 ⇝I . . . ⇝I 𝑝𝑛 and
assume 𝑠 |= 𝑝 0 ∪ 𝑝 1 ∪ · · · ∪ 𝑝𝑛 and 𝑠 ⇝S 𝑠 ′ . We prove 𝑠 ′ |= 𝑝𝑖 for every 0 ≤ 𝑖 ≤ 𝑛 by induction on 𝑖.
For 𝑖 = 0, the claim follows from (ID2). For 𝑖 > 0, since 𝑠 |= 𝑝𝑖 −1 ∪ 𝑝𝑖 and 𝑠 ′ |= 𝑝𝑖 −1 , we conclude
𝑠 ′ |= 𝑝𝑖 from (ID4)—the duality condition on transitions.                                              □
   Corollary 4.2. For S and I that are induction dual, if some 𝑝 ∈ 𝐵 I is reachable in I then S is safe.
   Proof. Follows from Lemma 4.1 and (ID3).                                                                                       □
  Dually, a path 𝐼 S ∋ 𝑠 0 ⇝S 𝑠 1 ⇝S . . . ⇝S 𝑠𝑛 in S induces an inductive invariant for I, and
reachability to a bad state in S implies safety of the dual transition system I.

4.3    Lagrangian for Primal-Dual Houdini
We can understand primal-dual Houdini as a simultaneous CEGAR for Cartesian abstraction for
both S and I, where the dual witness check in CEGAR for S also solves the primal witness check
for I, and the dual witness check for I solves the primal witness check for S. The fact that this can
be done requires a non-trivial lemma about the connection between S and I (and their restrictions).
   Formally, let
                                 𝑋 = Pfin (|S|) and 𝑌 = Pfin (P).
The Lagrangian 𝐿pdH : 𝑋 × 𝑌 −→ {−1, 0, 1} is defined by
                                   
                                   
                                    −1 if no 𝜗 ⊆ 𝑦 is a safe inductive invariant of S|𝑥
                                   
                                   
                     𝐿pdH (𝑥, 𝑦) := 1   if no 𝜛 ⊆ 𝑥 is a safe inductive invariant of I| 𝑦                                        (2)
                                   
                                   
                                   0   otherwise
                                   
2 This presentation of induction duality is a slight adaptation of [Padon et al. 2022]. For example, the original paper assumes

that the only element in 𝐼 I is the empty set (representing ⊤), which (ID2) generalizes; it also assumes that 𝐵 S is represented
by a single predicate 𝑝 0 ∈ P, i.e. 𝐵 S = {𝑠 ∈ |S| | 𝑠 ̸ |= 𝑝 0 }, and that 𝐵 I = {𝑦 ∈ Pfin (P) | 𝑝 0 ∈ 𝑦 }, which (ID3) generalizes.
The original paper also assumes that transitions in I only grow the set of predicates, which we do not assume here.
16                                              Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


where S|𝑥 is the subsystem of S consisting of states in 𝑥 and I| 𝑦 is the subsystem of S consisting
of sets of predicates from 𝑦 (i.e., more formally this can be written as I| P (𝑦) ). We need a slightly
advanced result of the dual transition system to understand this definition, as well as to confirm its
well-definedness. The following theorem is new to this paper, an abstraction of the progress proof
in Padon et al. [2022].
     Theorem 4.3. Assume dual transition systems S and I. Then at least one of the following holds:
       • some 𝜗 ⊆ P is a safe inductive invariant for S, or
       • some 𝜛 ⊆ |S| is a safe inductive invariant for I.
     Proof. See Appendix A.                                                                               □
   Theorem 4.3 shows that the conditions for 𝐿pdH (𝑥, 𝑦) = 1 and for 𝐿pdH (𝑥, 𝑦) = −1 do not hold
simultaneously. So 𝐿pdH given by eq. (2) is well-defined. Both 𝑋 and 𝑌 are join semilattices, and 𝐿 is
anti-monotone in 𝑋 and monotone in 𝑌 . So the general method applies to this Lagrangian, yielding
a procedure in Algorithm 4 that enjoys the progress property. The resulting procedure is the core
of primal-dual Houdini in [Padon et al. 2022].
     Proposition 4.4. sup𝑦 inf 𝑥 𝐿pdH (𝑥, 𝑦) ≥ 0 implies the satefy of S.
    Proof. If S is unsafe, there exists an error trace 𝐼 S ∋ 𝑠 0 ⇝S . . . ⇝S 𝑠𝑛 ∈ 𝐵 S . Letting 𝑥 =
{𝑠 0, . . . , 𝑠𝑛 }, there is no safe inductive invariant of S↾𝑥 , so sup𝑦 𝐿(𝑥, 𝑦) = −1.           □
  Even if sup𝑦 inf 𝑥 𝐿pdH (𝑥, 𝑦) = −1, we cannot conclude that S is unsafe: it just shows that P is
not sufficient to prove the safety of S. Similar to the case of CEGAR and ICE, analysis of 𝑆𝐺 ∈ 𝑋
satisfying sup𝑦 𝐿pdH (𝑆𝐺 , 𝑦) ≤ 0 may provide an unsafety proof.
  The Lagrangian 𝐿pdH is symmetric in the sense that swapping S and I does not essentially change
                                        S,I
the Lagrangian. That means, writing 𝐿pdH    for the Lagrangian for the dual transition systems (S, I),
           S,I            I,S
we have 𝐿pdH   (𝑥, 𝑦) = −𝐿pdH (𝑦, 𝑥). By this symmetry, the primal and dual witness check problems
are essentially the same. Primal-dual Houdini [Padon et al. 2022] solves these subproblems by using
the famous Houdini procedure [Flanagan et al. 2001; Flanagan and Leino 2001].
  Theorem 4.3 also suggests a connection to CEGAR. By Theorem 4.3, if 𝐿pdH (𝑥, 𝑦) = 1 (i.e. no
𝜛 ⊆ 𝑥 is a safe inductive invariant of I| 𝑦 ), then some 𝜗 ⊆ 𝑦 is a safe inductive invariant of S. So
𝐿pdH (𝑥, 𝑦) ≥ 0 if and only if some 𝜗 ⊆ 𝑦 is a safe inductive invariant of S. Therefore finding 𝑃
such that 𝐿pdH (𝑆𝐺 , 𝑃) ≥ 0 is essentially the abstraction refinement problem, which asks to find a
predicate set that proves the safety of an approximation of the transition system S. In primal-dual
Houdini (Algorithm 4), line 10 computes 𝑃 that satisfies 𝐿pdH (𝑥, 𝑦) ≥ 1 instead of 𝐿pdH (𝑥, 𝑦) ≥ 0,
and this is a requirement stronger than the standard abstraction refinement. This strategy for
updating the predicate set is the characteristic feature of primal-dual Houdini.

4.4     A More Abstract View
Our exposition above was rather close to that of [Padon et al. 2022]. Specifically, we used sets of
predicates for I. The use of sets of predicates is consistent with the perspective of incremental in-
duction and constructing invariants in a conjunctive domain. However, the Lagrangian formulation
suggests that a more abstract structure is enough to define primal-dual Houdini, as follows.
  In the more abstract form, we assume transition systems S and I, but do not assume anything on
the state space |I|, i.e., we do not assume it consists of predicates or sets of predicates. The only
assumption is that there is a binary relation between |S| and |I|, and that the two transition systems
are induction duals, that is, conditions (ID1)–(ID4) hold. This is very similar to the induction-dual
graphs of [Padon et al. 2022, Section 3.1].
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                           17


Algorithm 4 Primal-Dual Houdini
function Primal-Dual Houdini
  1: let 𝑆𝐺 ← ∅
  2: let 𝑃𝐺 ← {𝑝} for some 𝑝 ∈ 𝐵 I
  3: while true do
  4:      if inf 𝑆 𝐿pdH (𝑆, 𝑃𝐺 ) ≥ 0 then
  5:           return (safe, 𝑃𝐺 )
  6:      let 𝑆 ∈ {𝑆 ∈ 𝑋 | 𝐿pdH (𝑆, 𝑃𝐺 ) = −1}
  7:     𝑆𝐺 ← 𝑆𝐺 ∪ 𝑆
  8:      if sup𝑃 𝐿pdH (𝑆𝐺 , 𝑃) ≤ 0 then
  9:           return (unknown, 𝑆𝐺 )
 10:      let 𝑃 ∈ {𝑃 ∈ 𝑌 | 𝐿pdH (𝑆𝐺 , 𝑃) = 1}
 11:      𝑃𝐺 ← 𝑃𝐺 ∪ 𝑃


   Next, we assume arbitrary join semilattices 𝑋 and 𝑌 . That is, 𝑋 is not assumed to be finite sets of
states, and 𝑌 is not assumed to be finite sets of predicates. Instead, we assume a restriction mapping,
which maps every element of 𝑋 to a transition system S|𝑥 that is a subsystem of S in the following
sense: |S|𝑥 | ⊆ |S|, 𝐼 S|𝑥 = 𝐼 S ∩ |S|𝑥 |, ⇝S|𝑥 =⇝S ∩(|S|𝑥 | × |S|𝑥 |), and 𝐵 S|𝑥 = 𝐵 S ∩ |S|𝑥 |. We further
require that the restriction mapping is monotone, i.e., if 𝑥 ⊑𝑋 𝑥 ′ then |S|𝑥 | ⊆ |S|𝑥 ′ |, and that the
restriction is unbounded in the following sense: sup𝑥 |S|𝑥 | = |S|. We assume a similar restriction
mapping for 𝑌 and I.
   With this structure over the arbitrary sets 𝑋 and 𝑌 , we can define the Lagrangian by the following
generalization of eq. (2):

                              
                              
                               −1 if no 𝜗 ⊆ |I| 𝑦 | is a safe inductive invariant of S|𝑥
                              
                              
                 𝐿pdH (𝑥, 𝑦) = 1   if no 𝜛 ⊆ |S|𝑥 | is a safe inductive invariant of I| 𝑦                 (3)
                              
                              
                              0   otherwise
                              
   It is not too hard to see that Theorem 4.3 generalizes to the setting eq. (3) and that this Lagrangian
is well-defined. Note that the Lagrangian of Section 4.3 is obtained from the more abstract one by
letting |I| = Pfin (P), 𝑋 = Pfin (|S|), 𝑌 = Pfin (P), and defining |S|𝑥 | = 𝑥, and |I| 𝑦 | = P (𝑦) (note the
difference in the definition of the restriction mapping between 𝑋 and 𝑌 ).

5     Lagrangians for Termination Verification
So far, we have focused on the safety verification problem. This section discusses how our Lagrangian-
based approach applies to termination verification, presenting ICE-based and CEGAR-based proce-
dures. Intuitively, the Lagrangians can be obtained by replacing predicates in the safety verification
with ranking functions. This idea works well for ICE, but for CEGAR, a problem arises with the
monotonicity requirement. From our perspective, the concept of disjunctive well-foundedness [Podel-
ski and Rybalchenko 2004] is an idea to address the monotonicity requirement.

5.1    Termination and Ranking Function
Let S = (|S|, 𝐼 S, ⇝S ) be a transition system. In this section, we omit the bad states 𝐵 S as this
component is irrelevant to the verification problem in this section. An infinite trace is an infinite
sequence 𝑠 0𝑠 1𝑠 2 · · · ∈ |S|𝜔 of states such that 𝑠 0 ∈ 𝐼 S and 𝑠𝑖 ⇝S 𝑠𝑖+1 for every 𝑖. A transition system
is terminating if it has no infinite trace.
18                                                        Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


   The termination of a transition system S can be witnessed by a ranking function. In this paper,
it is a function 𝑟 : |S| −→ 𝜅 from states to an ordinal number 𝜅 such that 𝐼 S ∋ 𝑠 0 ⇝∗S 𝑠 ⇝S 𝑠 ′
implies 𝑟 (𝑠) > 𝑟 (𝑠 ′ ) (readers who are not familiar with ordinal numbers may set 𝜅 = N). So 𝑟 must
decrease for every reachable transition (but a transition 𝑠 ⇝S 𝑠 ′ from an unreachable state 𝑠 does
not require anything on 𝑟 ). The existence of a ranking function is a sound and complete criterion
for termination.

5.2 ICE for Termination
It is straightforward to modify the Lagrangian for the safety verification in Section 3.3 to handle the
termination verification. Let ℜ ⊆ (|S| → N) be a set of candidates for ranking functions, and let
                                    𝑋 := Pfin (𝐼 S ) × Pfin (⇝S )         and 𝑌 := ℜ.
The 𝑋 -component is the same as the 𝑋 -component for ICE (but the bad-state information is omitted).
The 𝑌 -component is the set of candidate proofs, which in the case of termination verification is
the set of candidate ranking functions. (Recall that in the case of safety verification 𝑌 is the set
of predicates, thus in termination verification ranking functions assume the role of predicates in
safety verification.) The Lagrangian 𝐿T-ICE : 𝑋 × 𝑌 −→ {−1, 1} is defined by
                                (
                       ′          1  𝑟 is a ranking function for the subsystem 𝑆 ′ of S
              𝐿T-ICE (𝑆 , 𝑟 ) =
                                  −1 otherwise.
The 𝑋 -component has an obvious join semilattice structure, and 𝐿T-ICE is anti-monotone on 𝑋 . So
the basic primal-dual procedure is applicable, provided that the primal and dual witness check
problems are tractable.
  We now discuss soundness. An “idealized” version 𝐿T′ -ICE : 𝑋 × 𝑌 ′ −→ {−1, 1} of 𝐿T-ICE is given
by setting 𝑋 ′ := P (𝐼 S ) × P (⇝S ) and 𝑌 ′ := (|S| → 𝜅) for a sufficiently large ordinal number 𝜅.3
We define 𝐿T′ -ICE (𝑆 ′, 𝑟 ) = 1 if and only if 𝑟 is a ranking function for the subsystem 𝑆 ′ of S.
     Proposition 5.1. 𝐿T′ -ICE enjoys strong duality, and inf 𝑥 sup𝑦 𝐿T′ -ICE (𝑥, 𝑦) = 1 iff S terminates.
     Proof. If S terminates, a ranking function 𝑟 for S is given by
                     𝑟 (𝑠)     =     (The number of steps remaining before termination)
                               =     sup {𝑟 (𝑠 ′ ) + 1 | 𝑠 ⇝S 𝑠 ′ }.
This is a definition by induction on ⇝S . Then 𝐿T′ -ICE (𝑆 ′, 𝑟 ) = 1 since 𝑆 ′ is a subsystem of S. If S is
not terminating, 𝐿T′ -ICE (S, 𝑟 ) = −1 for every 𝑟 ∈ 𝑌 ′ .                                                □
     Lemma 5.2. inf 𝑆 ′ 𝐿T-ICE (𝑆 ′, 𝑟 ) = 1 implies the termination of S.                                                      □
    Proof. If 𝑟 is not a ranking function of S, there exists a transition 𝐼 S ∋ 𝑠 0 ⇝S . . . ⇝S 𝑠𝑛 ⇝S 𝑠𝑛+1
such that 𝑟 (𝑠𝑛 ) ≯ 𝑟 (𝑠𝑛+1 ). Then the subsystem 𝑆 ′ = ({𝑠 0 }, {(𝑠𝑖 , 𝑠𝑖+1 ) | 0 ≤ 𝑖 ≤ 𝑛}) satisfies
𝐿T′ -ICE (𝑆 ′, 𝑟 ) = −1.                                                                                □
     We discuss the tractability of the primal and dual witness check.
     The dual witness check is tractable because whether inf 𝑆 ′ 𝐿T-ICE (𝑆 ′, 𝑟 ) = −1 is reducible to a safety
verification problem. Let S (𝑟 ) be the transition system (with bad states) given by |S (𝑟 ) | := |S| × |S|,
𝐼 S (𝑟 ) := {(𝑠, 𝑠 ′ ) | 𝑠 ∈ 𝐼 S, 𝑠 ⇝S 𝑠 ′ }, (⇝S (𝑟 ) ) := {((𝑠, 𝑠 ′ ), (𝑠 ′, 𝑠 ′′ )) | 𝑠 ′ ⇝S 𝑠 ′′ } and 𝐵 S (𝑟 ) := {(𝑠, 𝑠 ′ ) |
𝑟 (𝑠) ≤ 𝑟 (𝑠 ′ )}. A state of S (𝑟 ) is a pair (𝑠, 𝑠 ′ ) of a previous state 𝑠 and a current state 𝑠 ′ , and a pair is
bad if and only if it violates the ranking condition with respect to 𝑟 . If the system S (𝑟 ) is safe, 𝑟 is a
ranking function for S. The safety verification of S (𝑟 ) can be solved by procedures such as those
3 One can choose 𝜅 as the minimum ordinal that has the same cardinality as P ( |S| ).
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                                  19


discussed in Sections 3 and 4. If S (𝑟 ) is unsafe, an error trace (𝑠 0, 𝑠 1 ) (𝑠 1, 𝑠 2 ) . . . (𝑠𝑛 , 𝑠𝑛+1 ) ∈ |S (𝑟 ) | ∗
induces 𝑆 ′ = ({𝑠 0 }, {(𝑠 0, 𝑠 1 ) (𝑠 1, 𝑠 2 ) . . . (𝑠𝑛 , 𝑠𝑛+1 )}).
   On the contrary, it is hard to check the primal witness, which asks to find a ranking function 𝑟
that works well on the subsystem 𝑆 ′ . Since 𝑆 ′ is a terminating finite transition system, a ranking
function can in theory be given by mapping each point to the number of remaining steps, but
this would not be expected to behave well for points outside of 𝑆 ′ . To find generalized ranking
functions, methods have been proposed that use template-based synthesis [Unno et al. 2021] as
well as machine learning techniques, such as decision tree learning [Kura et al. 2021] and support
vector machines [Li et al. 2020].

5.3    CEGAR for Termination
The Lagrangian for CEGAR has a semilattice structure on 𝑌 and 𝐿CEGAR is monotone on 𝑌 . In the
context of termination verification, 𝑌 consists of (sets of) candidate ranking functions, but it is not
straightforward to introduce the join semilattice structure to the 𝑌 -component.
   A disjunctively well-founded relation [Podelski and Rybalchenko 2004] is a concept to address
this issue: a relation ≻ is disjunctively well-founded if it is a finite union of well-founded relations.
For a finite set 𝑅 ∈ Pfin (ℜ) of candidate ranking functions, the relation ≻𝑅 defined by (𝑠 ≻𝑅 𝑠 ′ ) :⇔
∃𝑟 ∈ 𝑅.𝑟 (𝑠) > 𝑟 (𝑠 ′ ) is a disjunctively well-founded relation. The set Pfin (ℜ) has an obvious lattice
structure, and 𝑅 ⊆ 𝑅 ′ ∈ Pfin (ℜ) implies (≻𝑅 ) ⊆ (≻𝑅 ′ ).
   Let 𝑋 := {𝑠 0𝑠 1 . . . 𝑠𝑛 ∈ |S| | 𝐼 S ∋ 𝑠 0 ⇝S . . . ⇝S 𝑠𝑛 }, 𝑌 := Pfin (ℜ), and
                                                      (
                                                        1    ∀𝑖.∀𝑗 .(𝑖 < 𝑗) ⇒ (𝑠𝑖 ≻𝑅 𝑠 𝑗 )
                        𝐿T-CEGAR (𝑠 0 . . . 𝑠𝑛 , 𝑅) =
                                                        −1 otherwise.
Note that ≻𝑅 must satisfy 𝑠𝑖 ≻𝑅 𝑠 𝑗 for every 𝑖 < 𝑗, including the case that 𝑖 + 1 ≠ 𝑗, i.e. 𝑠 𝑗 is not the
immediate successor of 𝑠𝑖 , unlike the condition for ranking functions. Then 𝑌 is a join semilattice
and 𝐿T-CEGAR is monotone on 𝑌 . When sup𝑅 inf 𝜏 𝐿T-CEGAR (𝜏, 𝑅) = 1, then S is terminating by the
following theorem.
   Theorem 5.3 (Podelski and Rybalchenko [2004, Theorem 1]). A transition system S is termi-
nating if there exists a disjunctively well-founded relation ≻ such that 𝐼 S ∋ 𝑠 0 ⇝∗S 𝑠 ⇝+S 𝑠 ′ implies
𝑠 ≻ 𝑠 ′.                                                                                              □
    Corollary 5.4. If sup𝑦 inf 𝑥 𝐿T-CEGAR (𝑥, 𝑦) = 1, then S is terminating.                                                     □
   The dual witness check, which asks to find 𝜏 such that 𝐿T-ICE (𝜏, 𝑅) = −1, is reducible to a
safety verification problem. The idea is similar to the above case, but the first component 𝑠 of a
pair (𝑠, 𝑠 ′ ) is now a past state that is not necessarily the previous state. Formally, let S (𝑅) be the
transition system (with bad states) given by |S (𝑅) | := |S| × |S|, 𝐼 S (𝑅) := {(𝑠, 𝑠 ′ ) | 𝑠 ∈ 𝐼 S, 𝑠 ⇝S 𝑠 ′ },
(⇝S (𝑅) ) := {((𝑠 1, 𝑠 1′ ), (𝑠 2, 𝑠 2′ )) | 𝑠 1′ ⇝S 𝑠 2′ and 𝑠 2 = 𝑠 1 ∨𝑠 2 = 𝑠 1′ } and 𝐵 S (𝑅) := {(𝑠, 𝑠 ′ ) | 𝑠 ⊁𝑅 𝑠 ′ }. For an
error trace (𝑠 0, 𝑠 0′ ) (𝑠 1, 𝑠 1′ ) . . . (𝑠𝑛 , 𝑠𝑛′ ) ∈ |S (𝑅) | ∗ for S (𝑅) , we have 𝐼 S ∋ 𝑠 0 ⇝S 𝑠 0′ ⇝S 𝑠 1′ ⇝S . . . ⇝S 𝑠𝑛′ ,
𝑠𝑛 ⊁𝑅 𝑠𝑛′ and 𝑠𝑛 ∈ {𝑠 0, 𝑠 0′ , 𝑠 1′ , . . . , 𝑠𝑛−1′ }.

   The primal witness check is more tractable than 𝐿T-ICE since it suffices to find a ranking function
that works for a single trace.
   The basic primal-dual procedure applied to 𝐿T-CEGAR is (the core of) the procedure known as
Terminator [Cook et al. 2005, 2006].

6     Lagrangian for Quantified Linear Arithmetic Solver
This section deals with a problem that is closely related to verification, but different in nature from
the safety/termination verification problems we have dealt with so far. The problem is validity
20                                                      Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


checking of first-order predicate logic formulas, and this section analyses the procedure given
by Farzan and Kincaid [2016] from the viewpoint of Lagrange duality. Basically, the Lagrangian
corresponds to Skolemization, but as discussed in Farzan and Kincaid [2016], Skolemization alone is
not sufficient. Interestingly, our framework of Lagrangian duality and basic primal-dual procedure
clarifies the issue: as we shall see, it is the monotonicity criterion.

6.1     First-Order Formula and Skolemization
This section focuses on first-order formulas. We consider the theory of linear rational arithmetic,
LRA, which is the theory that Farzan and Kincaid [2016] mainly dealt with. A term is given by
𝑡 ::= 𝑥 | 𝑐 | 𝑡 1 + 𝑡 2 | 𝑐 · 𝑡 (where 𝑐 ∈ Q) and atomic predicates are 𝑡 1 < 𝑡 2 and 𝑡 1 ≤ 𝑡 2 . We assume
that formulas are in prenex normal form, i.e., 𝜑 = Q1𝑥 1 . . . . Q𝑘 𝑥𝑘 .𝜗 where Q𝑖 ∈ {∀, ∃} and 𝜗 is
quantifier-free. Since LRA enjoys effective quantifier elimination (i.e., given a quantified formula
𝜑 (𝑥, 𝑦),
      ® one can effectively construct a quantifier-free formula 𝜓 (𝑦)  ® such that 𝜓 (𝑦)  ® ↔ ∃𝑥 .𝜑 (𝑥, 𝑦)),
                                                                                                         ®
the validity checking problem for first-order logic formulas over LRA is decidable.
   Skolemization is a satisfiability-preserving translation of first-order logic formulas, introducing
new functional symbols. Consider a quantified formula:
                                       ∀𝑎 ∈ Q.∃𝑏 ∈ Q.∀𝑐 ∈ Q.𝜑 (𝑎, 𝑏, 𝑐).                                         (4)
If this formula is true, there exists a function 𝑓𝑏 : Q → Q that maps a value assigned to 𝑎 to an
appropriate value for 𝑏, i.e., for every 𝑣 ∈ Q,
                                                 ∀𝑐 ∈ Q.𝜑 (𝑣, 𝑓𝑏 (𝑣), 𝑐),
and 𝑓𝑏 is called a Skolem function for 𝑏. By using the Skolem function, the validity of eq. (4) is
reduced to the problem to find an appropriate function 𝑓𝑏 such that
                                          ∀𝑎 ∈ Q.∀𝑐 ∈ Q.𝜑 (𝑎, 𝑓𝑏 (𝑎), 𝑐)
is valid, and this validity problem can be solved by SMT solvers (provided that 𝑓𝑏 is describable
as a term in LRA). Conversely, if the formula in eq. (4) is false, its negation ∃𝑎 ∈ Q.∀𝑏 ∈ Q.∃𝑐 ∈
Q.¬𝜑 (𝑎, 𝑏, 𝑐) is true, so there exist Skolem functions 𝑓𝑎 : Z and 𝑓𝑐 : Z → Z such that
                                             ∀𝑏 ∈ Z.¬𝜑 (𝑓𝑎 , 𝑏, 𝑓𝑐 (𝑏)).
     The above observation yields the following Lagrangian: letting
                           𝑋 = (Skolem functions for 𝑎 and 𝑐) = (Z × (Z → Z))
                            𝑌 = (Skolem function for 𝑏) = (Z → Z),
the Lagrangian 𝐿 : 𝑋 × 𝑌 −→ {−1, 1} is given by
                        𝐿((𝑓𝑎 , 𝑓𝑐 ), 𝑓𝑏 ) = 1     :⇔       𝜑 (𝑓𝑎 , 𝑓𝑏 (𝑓𝑎 ), 𝑓𝑐 (𝑓𝑏 (𝑓𝑎 ))) is true.
  The optimal value of the dual optimization problem is 1 if and only if there exists an appropriate
Skolem function for 𝑏. To see this, note that
         inf 𝐿((𝑓𝑎 , 𝑓𝑐 ), 𝛽) = −1    ⇔      ∃𝑓𝑎 ∈ Q.∃𝑓𝑐 ∈ (Q → Q).𝜑 (𝑓𝑎 , 𝛽 (𝑓𝑎 ), 𝑓𝑐 (𝛽 (𝑓𝑎 ))) is false
        𝑓𝑎 ,𝑓𝑐
                                      ⇔      ∃𝑎 ∈ Q.∃𝑐 ∈ Q.𝜑 (𝑎, 𝛽 (𝑎), 𝑐) is false,
so, by negating the both sides,
                         inf 𝐿((𝑓𝑎 , 𝑓𝑐 ), 𝛽) = 1       ⇔      ∀𝑎 ∈ Q.∀𝑐 ∈ Q.𝜑 (𝑎, 𝛽 (𝑎), 𝑐).
                        𝑓𝑎 ,𝑓𝑐
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                               21


Hence, 𝛽 ∈ 𝑌 witnessing sup𝑦 ∈𝑌 inf 𝑥 ∈𝑋 𝐿(𝑥, 𝑦) = 1 is a Skolem function for 𝑏 that witnesses the
truth of the formula in eq. (4). Dually, a witness 𝛼 ∈ 𝑋 of inf 𝑥 ∈𝑋 sup𝑦 ∈𝑌 𝐿(𝑥, 𝑦) = −1 is a pair of
Skolem functions for 𝑎 and 𝑐 that witnesses the falsity of the formula.
   In the above setting, both 𝑋 and 𝑌 are the sets of all possible Skolem functions in the semantic
domains, so there is an appropriate choice for exactly one of 𝑋 and 𝑌 . Therefore, we have the
strong duality:
                         sup inf 𝐿((𝑓𝑎 , 𝑓𝑐 ), 𝑓𝑏 ) = inf sup 𝐿((𝑓𝑎 , 𝑓𝑐 ), 𝑓𝑏 ),
                             𝑓𝑏 𝑓𝑎 ,𝑓𝑐                        𝑓𝑎 ,𝑓𝑐 𝑓𝑏

and the optimal value coincides with the truth of the formula.
   This argument can be applied to arbitrary formulas. Given a first-order predicate logic formula
𝜓 with quantifiers, there exists a Lagrangian 𝐿𝜓 : 𝑋𝜓 × 𝑌𝜓 −→ {−1, 1}, where 𝑋𝜓 (resp. 𝑌𝜓 ) is the
set of Skolem functions for universally (resp. existentially) quantified variables in 𝜓 , such that 𝐿𝜓
satisfies the strong duality and the optimal value of 𝐿𝜓 is the truth of 𝜓 .

6.2   Quantified LRA Solver by Farzan and Kincaid
Very roughly, the procedure by Farzan and Kincaid [2016] is an instance of the basic primal-dual
procedure for Lagrangians in Section 6.1. However, we cannot directly apply the basic primal-dual
procedure since the Lagrangian does not satisfy the monotonicicy criterion, i.e. the sets 𝑋 and 𝑌 of
Skolem functions are not poset (and the Lagrangian is not monotone). Another, relatively minor
issue is that the sets 𝑋 and 𝑌 are too large, containing elements that have no finite representations.
   Farzan and Kincaid [2016] introduced the notion of strategy skeletons to address the above issues.
Intuitively, a strategy skeleton is a variant of Skolem functions, albeit with the additional capacity to
select multiple values, claiming that at least one of the selected values is appropriate. The inclusion
of the set of selected values is an order for strategy skeletons, and the Lagrangian is monotone (or
antimonotone) with respect to this order.
  Definition 6.1 (Strategy Skeleton). The set of SAT strategy skeletons is defined by the grammar
                                                       Ã
                                  𝜋 ::= • | ∀𝑦.𝜋 | 𝑖=1,...,𝑛 𝑡𝑖 .𝜋𝑖
where 𝑡𝑖 is a term of LRA and 𝑡𝑖 ≠ 𝑡 𝑗 if 𝑖 ≠ 𝑗. For a formula 𝜓 in prenex normal form we write
𝑥® ⊢ 𝜓 ◁ 𝜋 to denote that 𝜋 is a SAT strategy skeleton for 𝜓 and satisfies fv(𝜋) ⊆ {𝑥®}. Formally, it is
the relation defined by the following rules:
              QF (𝜗)            ® 𝑦 ⊢𝜓 ◁𝜋
                                𝑥,                    𝑥® ⊢ 𝜓 ◁ 𝜋𝑖 for every 𝑖     ∀𝑖.fv(𝑡𝑖 ) ⊆ {𝑥®}
                                                                                Ã
            𝑥® ⊢ 𝜗 ◁ •     𝑥® ⊢ (∀𝑦.𝜓 ) ◁ (∀𝑦.𝜋)                𝑥® ⊢ (∃𝑦.𝜓 ) ◁ ( 𝑖 𝑡𝑖 .𝜋𝑖 )
The strategy skeleton • is for quantifier-free formulas, to which we have nothing to choose. The
strategy skeleton ∀𝑦.𝜋 is for universally-quantified formulas ∀𝑦.𝜓 : a SAT strategy skeleton does
nothing on      Ã∀𝑦, and 𝜋 describes a way to choose values for ∃-quantified variables in 𝜓 . The strategy
skeleton 𝑖=1,...,𝑛 𝑡𝑖 .𝜋𝑖 is for ∃𝑦.𝜓 , meaning that an appropriate choice for 𝑦 should be found in
{𝑡 1, . . . , 𝑡𝑛 }. An UNSAT strategy skeleton can be defined similarly:
                                                          d
                                      𝜚 ::= • | ∃𝑦.𝜚 | 𝑖=1,...,𝑛 𝑡𝑖 .𝜚 𝑖
              QF (𝜗)            ® 𝑦 ⊢ 𝜚 ▷𝜓
                               𝑥,                     𝑥® ⊢ 𝜚 𝑖 ▷ 𝜓 for every 𝑖          ∀𝑖.fv(𝑡𝑖 ) ⊆ {𝑥®}
                                                                        d                                 .
            𝑥® ⊢ • ▷ 𝜗    𝑥® ⊢ (∃𝑦.𝜚 ) ▷ (∃𝑦.𝜓 )                  𝑥® ⊢ ( 𝑖 𝑡𝑖 .𝜚 𝑖 ) ▷ (∀𝑦.𝜓 )
For a sentence 𝜑 in prenex normal form, let SkeletonSAT (𝜑) and SkeletonUNSAT (𝜑) be the set of SAT
and UNSAT strategy sketelons for 𝜑 with no free variable, i.e. SkeletonSAT (𝜑) := {𝜋 | ⊢ 𝜑 ◁ 𝜋 } and
SkeletonUNSAT (𝜑) := {𝜚 | ⊢ 𝜚 ▷ 𝜑 }.                                                               □
22                                                            Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


     Example 6.2 ([Farzan and Kincaid 2016]). Let
 𝜑      :=    ∃𝑤 .∀𝑥 .∃𝑦.∀𝑧.𝜗 (𝑤, 𝑥, 𝑦, 𝑧),                 𝜗 (𝑤, 𝑥, 𝑦, 𝑧) ≡ ((𝑦 < 1 ∨ 2𝑤 < 𝑦) ∧ (𝑧 < 𝑦 ∨ 𝑥 < 𝑧)).
A SAT strategy skeleton is
                                                                                            
                                   𝜋           :=      0 . ∀𝑥 . (𝑥 . ∀𝑧 . •) ⊔ (2𝑥 . ∀𝑧 . •) .
This skeleton selects 0 for 𝑤 and 𝑥 or 2𝑥 for 𝑦 depending on the branch of ⊔.                                           □
     The set SkeletonSAT (𝜑) is a preordered set by the order defined by the following rules:
                                                   𝜋 ≤ 𝜋′               ∀𝑖.∃𝑗 .𝑡𝑖 = 𝑡 𝑗′ ∧ 𝜋𝑖 ≤ 𝜋 𝑗′
                                                                                         Ã ′ ′
                                                ∀𝑦.𝜋 ≤ ∀𝑦.𝜋 ′
                                                                          Ã
                              •≤•                                           𝑖 𝑡𝑖 .𝜋𝑖 ≤     𝑗 𝑡 𝑗 .𝜋 𝑗

The join operation ∪ is defined by • ∪ • := •, (∀𝑦.𝜋) ∪ (∀𝑦.𝜋 ′ ) := ∃𝑦.(𝜋 ∪ 𝜋 ′ ) and
                                     (           Ã
                   Ã                   (𝑡 .𝜋) ⊔ ( 𝑖 ∈𝐼 𝑡𝑖 .𝜋𝑖 )                     if 𝑡 ≠ 𝑡𝑖 for every 𝑖
         (𝑡 .𝜋) ∪ ( 𝑖 ∈𝐼 𝑡𝑖 .𝜋𝑖 ) :=                       Ã
                                       (𝑡 .(𝜋 ∪ 𝜋 𝑗 )) ⊔ ( 𝑖 ∈ (𝐼 \{ 𝑗 } ) 𝑡𝑖 .𝜋𝑖 ) if 𝑡 = 𝑡 𝑗 .
Dually SkeletonUNSAT (𝜑) has a similar structure, obtained by replacing ⊔ with ⊓ (e.g. 𝜚 ≤ (𝜚 ⊓ 𝜚 ′ )).
We write the join in SkeletonUNSAT (𝜑) as ∪, since it computes the union of candidates.
   A pair (𝜚, 𝜋) ∈ SkeletonUNSAT (𝜑) × SkeletonSAT (𝜑) of SAT and UNSAT skeletons for the same
formula 𝜑 induces a quantifier-free formula ⟨𝜚 | 𝜑 | 𝜋⟩ defined by induction on 𝜑 as follows:

                        d   ⟨• |       𝜗        | •⟩               :=         𝜗Ó
                    ⟨   𝑖 𝑡𝑖 .𝜚 𝑖 | ∀𝑥 .𝜑 | ∀𝑥
                                            Ã .𝜋⟩                  :=          Ô𝑖 ⟨𝜚 𝑖 | 𝜑 [𝑡𝑖 /𝑥] | 𝜋 [𝑡𝑖 /𝑥]⟩
                        ⟨∃𝑥 .𝜚 | ∃𝑥 .𝜑 | 𝑖 𝑡𝑖 .𝜋𝑖 ⟩                :=           𝑖 ⟨𝜚 [𝑡𝑖 /𝑥] | 𝜑 [𝑡𝑖 /𝑥] | 𝜋𝑖 ⟩.

Let 𝐿FK : SkeletonUNSAT (𝜑) × SkeletonSAT (𝜑) −→ {−1, 1} be the Lagrangian defined by
                                       𝐿FK (𝜚, 𝜋) = 1           :⇔        ⟨𝜚 | 𝜑 | 𝜋⟩ is true.
                                           𝜑
This Lagrangian is written as 𝐿FK if the formula 𝜑 should be clarified. The procedure by Farzan and
Kincaid [2016] is an instance of the basic primal-dual procedure for 𝐿FK .
  Example 6.3 ([Farzan and Kincaid 2016]). Recall the formulas 𝜑 and 𝜗 and the SAT strategy
skeleton 𝜋 in example 6.2. An example of an UNSAT strategy skeleton is
                                                 
      𝜚 := ∃𝑤 . (−1) . ∃𝑦 . (𝑢 1 . •) ⊓ (𝑢 2 . •) , 𝑢 1 (𝑤, 𝑦) = 𝑦, 𝑢 2 (𝑤, 𝑦) = (𝑤 + 𝑦)/2
Then, the calculation of ⟨𝜚 | 𝜑 | 𝜋⟩ proceeds as
       D                                                                                                  E
         ∃𝑦.((𝑢 1 (0, 𝑦) . •) ⊓ (𝑢 2 (0, 𝑦) . •)) ∃𝑦.∀𝑧.𝜗 (0, −1, 𝑦, 𝑧) ((−1) . ∀𝑧 . •) ⊔ ((−2) . ∀𝑧 . •)
       D                                                                   E
    = ((𝑢 1 (0, −1) . •) ⊓ (𝑢 2 (0, −1) . •)) ∀𝑧.𝜗 (0, −1, −1, 𝑧) ∀𝑧 . •
             D                                                                    E
          ∨ ((𝑢 1 (0, −2) . •) ⊓ (𝑢 2 (0, −2) . •)) ∀𝑧.𝜗 (0, −1, −2, 𝑧) ∀𝑧 . •
                                                              
    = 𝜗 0, −1, −1, 𝑢 1 (0, −1) ∧ 𝜗 0, −1, −1, 𝑢 2 (0, −1)
                                                                    
          ∨ 𝜗 0, −1, −2, 𝑢 1 (0, −2) ∧ 𝜗 0, −1, −2, 𝑢 2 (0, −2)
                                                              
so we have 𝐿FK (𝜚, 𝜋) = ⟨𝜚 | 𝜑 | 𝜋⟩ = ⊥ ∧ ⊤ ∨ ⊥ ∧ ⊥ = −1.                                                               □
  Lemma 6.4. 𝐿FK : SkeletonUNSAT (𝜑) × SkeletonSAT (𝜑) −→ {−1, 1} is anti-monotone on the first
argument and monotone on the second argument.
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                       23


   Proof. Intuitively, if 𝜋 ≤ 𝜋 ′ , then 𝜋 ′ has more components than 𝜋 connected by ⊔. Then
⟨𝜚 |𝜑 |𝜋 ′ ⟩ has more components than ⟨𝜚 |𝜑 |𝜋⟩ connected by ∨. So, the validity of the latter implies
the validity of the former. The anti-monotonicity on SkeletonUNSAT (𝜑) is similar.                  □

   Prior to the discussion of correctness, we discuss the decidability of the primal/dual witness
check problems, following Farzan and Kincaid [2016]. We discuss the dual witness check here;
the primal is essentially equivalent. Assume a SAT strategy skeleton 𝜋 ∈ SkeletonSAT (𝜑). Then
       𝜑
inf 𝜚 𝐿FK (𝜚, 𝜋) = 1 is reducible to the validity of the formula 𝜑 |𝜋⟩ given as follows:
                                                                   Ã             Ô
         𝜗 |•⟩ := 𝜗      (∀𝑥 .𝜑)|∀𝑥 .𝜋⟩ := ∀𝑥 .(𝜑 |𝜋⟩)     (∃𝑥 .𝜑)| 𝑖 𝑡𝑖 .𝜋𝑖 ⟩ := 𝑖 (𝜑 [𝑡𝑖 /𝑥])|𝜋𝑖 ⟩.
Since 𝜑 |𝜋⟩ is a formula with no ∃, its validity can be checked by an SMT solver.
   Example 6.5. Recall the formulas 𝜑 and 𝜗 and a SAT strategy skeleton 𝜋 in example 6.2. Then
                                                                                      
                   𝜑 |𝜋⟩ = ∀𝑥 . (∀𝑧 1 .𝜗 (0, 𝑥, 𝑥, 𝑧 1 )) ∨ (∀𝑧 2 .𝜗 (0, 𝑥, 2𝑥, 𝑧 2 )) ,
which is invalid. For example, consider the assignment 𝑥 = −1, 𝑧 1 = −1 and 𝑧 2 = −2. This assignment
gives a UNSAT strategy skeleton 𝜚 := ∀𝑤 .(−1).∀𝑦. (−1). • ⊔ (−2). • such that 𝐿FK (𝜚, 𝜋) = −1. For
another SAT strategy skeleton 𝜋 ′ := (−2).∀𝑥 .(𝑥 + 1).∀𝑧.•, we have 𝜑 |𝜋 ′ ⟩ = ∀𝑥 .∀𝑧.𝜗 (−2, 𝑥, 𝑥 + 1, 𝑧),
which is valid.                                                                                         □
                          𝜑
   Lemma 6.6. inf 𝜚 𝐿FK (𝜚, 𝜋) = 1 if and only if 𝜑 |𝜋⟩ is valid.
   Proof. See Appendix B.                                                                                              □
                                                                                       𝜑
  Theorem 6.7. For every closed formula 𝜑 over LRA, the Lagrangian 𝐿FK enjoys the strong duality,
and its optimal value coincides with the validity of 𝜑.
   Proof. The result follows from Farzan and Kincaid [2016]. To show the strong duality, it suffices
to prove that, for a valid formula 𝜑, there exists a SAT strategy skeleton 𝜋 ∈ SkeletonSAT (𝜑)
                        𝜑
such that inf 𝜚 𝐿FK (𝜚, 𝜋) = 1. The basic observation in Farzan and Kincaid [2016] is that the
quantifier elimination 𝜗 (𝑦) ↔ ∃𝑥 .𝜓 (𝑥, 𝑦) can be achieved by substitution, i.e. there exists a finite
set {𝑡 1, . . . , 𝑡𝑛 } of terms such that (∃𝑥 .𝜓 (𝑥, 𝑦)) ↔ (𝜓 (𝑡 1, 𝑦) ∨ · · · ∨ 𝜓 (𝑡𝑛 , 𝑦)).4 Iterative application
of this result yields a SAT strategy skeleton 𝜋 such that 𝜑 ↔ (𝜑 |𝜋⟩).
   Since 𝜓 (𝑡) → (∃𝑥 .𝜓 (𝑥)) is valid for every 𝜓 and 𝑡, the formula 𝜑 |𝜋⟩, obtained by instantiating
                                                               𝜑
∃-variables, is stronger than 𝜑. By Lemma 6.6, inf 𝜚 𝐿FK (𝜚, 𝜋) = 1 implies the validity of 𝜑 |𝜋⟩ and
hence the validity of 𝜑.                                                                                           □

   The algorithm given by Farzan and Kincaid [2016] is an instance of the basic primal-dual
procedure for the Lagrangian 𝐿FK . Given a SAT strategy skeleton 𝜋, the check of inf 𝜚 𝐿FK (𝜚, 𝜋) = 1
is reducible to the validity of 𝜑 |𝜋⟩, which can de solved by an SMT solver. If inf 𝜚 𝐿FK (𝜚, 𝜋) = −1,
or equivalently, 𝜑 |𝜋⟩ is invalid, the SMT solver generates a counter-model for 𝜑 |𝜋⟩, from which a
UNSAT strategy skeleton 𝜚 can be constructed as illustrated in example 6.5. But their procedure has
an important twist here: the assignment to each variable in the counter-model, which is a concrete
rational number, is converted to a term. The terms are chosen from those playing an important
role in quantifier elimination or model-based projection (cf. [Farzan and Kincaid 2016, Section 4.1]).
As the set of such terms is finite, Farzan and Kincaid [2016] in effect considered finite subsets
of SkeletonSAT (𝜑) and SkeletonUNSAT (𝜑), and this finiteness guarantees that Farzan and Kincaid’s
procedure is terminating.
4 Farzan and Kincaid [2016] was inspired by model-based projection [Komuravelli et al. 2014], which is closely related to

quantifier elimination (see [Farzan and Kincaid 2016, Section 4.1]).
24                                                        Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


7     Lagrangian for Fixed-Point Logic over Quantified Linear Arithmetic
This section demonstrates the usefulness of our Lagrangian-based approach by developing a solver
of the validity problem for a fixed-point logic over quantified linear arithmetic. The validity problem
is closely related to game solving against liveness winning criteria as in Heim and Dimitrova [2024].
   Our observation is that the difficulty of this problem can actually be decomposed into the
difficulties of termination analysis and of quantifiers, each of which has been addressed in Sections 5
and 6. So a Lagrangian for the validity problem of fixed-point logic with quantifiers is obtained as a
simple combination of ideas in these sections.
   We have developed a prototype implementation of the basic primal-dual procedure for the
proposed Lagrangian and provide an evaluation.

7.1    Fixed-Point Logic
We define the syntax and semantics of the fixed-point logic studied in this section. Although the
discussion in this section is applicable to first-order structures in general to some extent, we will
focus on the fixed-point logic over linear integer arithmetic, LIA. An atomic predicate 𝑝 is either =
or ≤, and a term is given by 𝑡 ::= 𝑛 | 𝑥 | 𝑡 + 𝑡 ′ | 𝑛 × 𝑡 | 𝑡 mod 𝑛 (where 𝑛 is an integer and 𝑥 is a
variable).
   A (fixed-point-free) formula is defined by the following grammar:
                        𝜑,𝜓      ::=     𝑝 (𝑡®) | ¬𝑝 (𝑡®) | 𝑃 (𝑡®) | 𝜑 ∧ 𝜓 | 𝜑 ∨ 𝜓 | ∀𝑥 .𝜑 | ∃𝑥 .𝜑,
where 𝑡 is a term in LIA, 𝑝 is an atomic predicate in LIA (i.e. = or ≤), and 𝑃 is a user-defined predicate.
For notational simplicity, we will also use logical formulas that do not follow the above syntax in
the strict sense but can be transformed into the above form (e.g. (𝑥 < 42 ∧ 𝑖 ≠ 0) ⇒ 𝑃 (𝑥 + 𝑖), which
is equivalent to (42 ≤ 𝑥 ∨ 𝑖 = 0 ∨ 𝑃 (𝑥 + 1))). Predicates 𝑃 are defined by mutual recursion:
                                            𝜉1                𝜉2                      𝜉𝑛
                                   𝑃1 (𝑥®1 ) = 𝜑 1 ; 𝑃2 (𝑥®2 ) = 𝜑 2 ; . . . ; 𝑃𝑛 (𝑥®𝑛 ) = 𝜑𝑛
where 𝑥®𝑖 is a sequence of variables, 𝜉𝑖 ∈ {𝜈, 𝜇}, and 𝜑𝑖 is a fixed-point-free formula with free variables
in {𝑥®𝑖 , 𝑃1, . . . , 𝑃𝑛 }. If 𝜉𝑖 = 𝜈 (resp. 𝜇), then 𝑃𝑖 is the greatest solution (resp. least solution) of the
equation 𝑃𝑖 (𝑥®𝑖 ) = 𝜑𝑖 (for details, see the formal semantics defined below). The order of definitions
                          𝜉𝑖                     𝜉𝑖+1                                             𝜉𝑖+1                𝜉𝑖
matters: · · · ; 𝑃𝑖 (𝑥®𝑖 ) = 𝜑𝑖 ; 𝑃𝑖+1 (𝑥®𝑖+1 ) = 𝜑𝑖+1 ; · · · differs from · · · ; 𝑃𝑖+1 (𝑥®𝑖+1 ) = 𝜑𝑖+1 ; 𝑃𝑖 (𝑥®𝑖 ) = 𝜑𝑖 ; · · ·
when 𝜉𝑖 ≠ 𝜉𝑖+1 . For readers familiar with parity conditions, the left has higher priority. A formula
is a pair (𝜑, R) of a fixed-point free formula 𝜑 with a mutually-recursive definition R of predicates
in 𝜑.
   Example 7.1 (Heim and Dimitrova [2024, Example 1.1]). This example is a formalization of the
following control problem. Consider a system with a single integer variable 𝑥 : Z. For each step,
the environment chooses 𝑖 ∈ Z. If 𝑥 < 42 or 𝑖 = 0, the system successfully terminates. If 𝑥 ≥ 42 and
𝑖 ≠ 0, the system proceeds to the next step, updating 𝑥. In this case, the controller can choose the
next value of 𝑥 from (𝑥 + 𝑖) and (𝑥 − 𝑖). The problem is to synthesize a controller that will always
make the system terminate (or, if such a controller does not exist, to answer that it does not exist).
   The existence of a controller is equivalent to the validity of ∀𝑥 .𝑃 (𝑥) where
               𝜇
                                                                                           
      𝑃 (𝑥) = ∀𝑖. (𝑥 < 42 ∨ 𝑖 = 0 ⇒ ⊤) ∧ (𝑥 ≥ 42 ∧ 𝑖 ≠ 0) ⇒ (𝑃 (𝑥 + 𝑖) ∨ 𝑃 (𝑥 − 𝑖))
The user-defined predicate 𝑃 (𝑛) means that the system with an appropriate controller terminates
from the state 𝑥 = 𝑛. The right-hand-side of the definition describes the one-step transition of
the system; the universal quantification ∀𝑖 expresses that 𝑖 is chosen by the environment. The
predicate 𝑃 is defined as the least fixed-point; this reflects the requirement that the system should
not perform infinite step transitions. The formula ∀𝑥 .𝑃 (𝑥) is valid, as we shall see.            □
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                       25


   We formally define the semantics of a mutually-recursive definition of predicates. First, we deal
                                  𝜉
with a single equation 𝑃 (𝑥)
                           ® = 𝜑. We write 𝜑 (𝑃) (𝑥)     ® to make explicit that 𝜑 depends on 𝑃 and 𝑥.® Let
D := (Zℓ → {0, 1}) be the semantic domain for the predicate 𝑃, where ℓ is the length of 𝑥.         ® This is
a complete lattice by the point-wise order (i.e., for 𝑓 , 𝑔 ∈ D, 𝑓 ≤ 𝑔 if and only if 𝑓 (𝑛)     ® ≤ 𝑔(𝑛)
                                                                                                      ® for
every 𝑛® ∈ Zℓ ). Since ¬𝑃 does not appear in 𝜑, the function 𝜑 : D −→ D mapping 𝑑 ∈ D to 𝜑 (𝑑)
(which is a predicate Zℓ ∋ 𝑛® ↦→ 𝜑 (𝑑) (𝑛)  ® ∈ {0, 1}) is a monotone function. Then, Knaster-Tarski
theorem shows that the set {𝑑 ∈ D | 𝑑 = 𝜑 (𝑑)} has both the least and greatest elements. When
𝜉 = 𝜇 (resp. 𝜉 = 𝜈), then 𝑃 is defined as the least solution (resp. greatest solution).
   The semantics of a mutually-recursive definition
                                            𝜉1                 𝜉2                        𝜉𝑛   
                       R =        𝑃1 (𝑥®1 ) = 𝜑 1 ; 𝑃 2 (𝑥®2 ) = 𝜑 2 ; . . . ; 𝑃𝑛 (𝑥®𝑛 ) = 𝜑𝑛
is given as follows. Let D𝑖 := (Zℓ𝑖 → {0, 1}) be the semantic domain for the predicate 𝑃𝑖 , where
ℓ𝑖 is the length of 𝑥®𝑖 . We solve the equations in the right-to-left direction. A subtlety here is that
𝜑𝑛 may contain 𝑃1, . . . , 𝑃𝑛−1 ; we write 𝜑𝑛 (𝑃1, . . . , 𝑃𝑛−1, 𝑃𝑛 ) (𝑥®𝑛 ) to clarify the dependency. For each
                                                                 𝜉𝑛
(𝑑 1, . . . , 𝑑𝑛−1 ) ∈ D1 ×· · ·×D𝑛−1 , the equation 𝑃𝑛 (𝑥®𝑛 ) = 𝜑𝑛 (𝑑 1, . . . , 𝑑𝑛−1, 𝑃𝑛 ) (𝑥®𝑛 ) determines a value
𝜆𝑛 (𝑑 1, . . . , 𝑑𝑛−1 ) ∈ D𝑛 depending on 𝑑 1, . . . , 𝑑𝑛−1 . The solutions 𝜆𝑛 (𝑑 1, . . . , 𝑑𝑛−1 ) parameterized by
(𝑑 1, . . . , 𝑑𝑛−1 ) ∈ D1 × · · · × D𝑛−1 determine a function 𝜆𝑛 : D1 × · · · × D𝑛−1 → D𝑛 . Substituting 𝑃𝑛
with 𝜆𝑛 (𝑃 1, . . . , 𝑃𝑛−1 ) yields a system of equations without 𝑃𝑛 , and then we solve the equation for
𝑃𝑛−1 . Iteratively applying this process yields 𝑃𝑘 = 𝜆𝑘 (𝑃1, . . . , 𝑃𝑘 −1 ) for each 𝑘 = 1, . . . , 𝑛 depending
on 𝑃 1, . . . , 𝑃𝑘 −1 . Let 𝛿 1 = 𝜆1 (), 𝛿 2 = 𝜆2 (𝛿 1 ), and 𝛿𝑘 = 𝜆𝑘 (𝛿 1, . . . , 𝛿𝑘 −1 ) for general 𝑘. The assignment
on 𝑃1, . . . , 𝑃𝑛 determined by R is (𝛿 1, . . . , 𝛿𝑛 ) ∈ D1 × · · · × D𝑛 . The formula (𝜑, R) is valid if
𝜑 = 𝜑 (𝛿 1, . . . , 𝛿𝑛 ) is valid.

7.2    Lagrangian and Primal-Dual Procedure
As we have mentioned at the end of the previous subsection, the validity problem becomes easier if
one can remove the least fixed-point 𝜇 and existential quantifier ∃. We have already discussed a
way to remove an existential quantifier ∃ in Section 6, in which we used a SAT strategy skeleton to
guide a process of removal. The removal of the least fixed-point has been addressed in Section 5,
albeit in a slightly different form: a ranking function or disjunctively-well-founded relation is used
to reduce the termination problem (a typical 𝜇-property) to a safety problem (a typical 𝜈-property).
   The Lagrangian of this section simply combines these data, so the 𝑌 -component is a pair of a
SAT strategy skeleton and a disjunctively-well-founded relation. The 𝑋 -component is similar: it
describes choices of ∀-variables and ranking information for 𝜈-recursions.
   We formally describe the details. Assume a pair (𝜑, R), where
                                            𝜉1                𝜉2                        𝜉𝑛  
                        R =       𝑃1 (𝑥®1 ) = 𝜑 1 ; 𝑃2 (𝑥®2 ) = 𝜑 2 ; . . . ; 𝑃𝑛 (𝑥®𝑛 ) = 𝜑𝑛 .
Let ℓ𝑖 be the length of 𝑥®𝑖 . For simplicity, we assume that 𝜑, 𝜑 1, . . . , 𝜑𝑛 are in prenex normal form.
Let ℜ𝑖 be the set of candidate ranking functions available for 𝑃𝑖 . Let 𝐿 := {𝑖 | 𝜉𝑖 = 𝜇} and
𝐺 := {𝑖 | 𝜉𝑖 = 𝜈 } be the sets of indices of 𝜇- and 𝜈-predicates, repectively.
  The Lagrangian is a function 𝐿Fix : 𝑋 × 𝑌 −→ {−1, 1}, where
                         Î                                     Î
                 𝑋 := 𝑖 ∈𝐺 Pfin (ℜ𝑖 ) × SkeletonUNSAT (𝜑) × 𝑛𝑖=1 SkeletonUNSAT (𝜑𝑖 )
                         Î                                   Î
                 𝑌 := 𝑖 ∈𝐿 Pfin (ℜ𝑖 ) × SkeletonSAT (𝜑) × 𝑛𝑖=1 SkeletonSAT (𝜑𝑖 ).
Recall that in Section 6, which dealt with logical expressions with quantifiers, the two arguments of
the Lagrangian produce a logical formula whose validity is trivially computable (i.e. a logical formula
without quantifiers). A similar situation can be observed for fixed-point logic: two arguments of
the Lagrangian induce a logic formula whose validity is computable. The problematic constructs
26                                                              Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


in fixed-point logic formulas are quantifiers and recursions; the quantifiers are eliminated by the
strategy skeletons, and we avoid the divergence in the evaluation of the recursion by immediately
stopping the evaluation when a ranking information violation is detected. Then, we define the
value of the Lagrangian as the outcome of the evaluation.
   Given 𝑥 = ((𝑅𝑖 )𝑖 ∈𝐺 , 𝜚, (𝜚 𝑖 )𝑖=1,...,𝑛 ) ∈ 𝑋 and 𝑦 = ((𝑅𝑖 )𝑖 ∈𝐿 , 𝜋, (𝜋𝑖 )𝑖=1,...,𝑛 ), we formally define the
value 𝐿Fix (𝑥, 𝑦) of the Lagrangian as follows. We first apply the strategy skeletons (𝜚, (𝜚 𝑖 )𝑖 ) and
(𝜋, (𝜋𝑖 )𝑖 ) and construct a quantifier-free approximation (𝜑 ′, R ′ ) of the input (𝜑, R). This is simply
obtained by applying the translation ⟨𝜚 | 𝜑 | 𝜋⟩ defined in Section 6. That is, 𝜑 ′ := ⟨𝜚 | 𝜑 | 𝜋⟩ and
           𝜉𝑖
𝑃𝑖′ (𝑥®𝑖 ) = ⟨𝜚 𝑖 | 𝜑𝑖 | 𝜋𝑖 ⟩. Note that (𝜑 ′, R ′ ) is neither over- nor under-approximation.
    The formula (𝜑 ′, R ′ ) has no quantifier nor free variable, which we regard as a “program” with
recursively defined functions 𝑃1′ , . . . , 𝑃𝑛′ with two kinds of non-deterministic branches, demonic ∧
and angelic ∨. We run the program, recording all visited states and monitoring them for violations
of the disjunctively-well-founded relations 𝑅𝑖 . So, a configuration is a pair (𝜓, 𝑉® ) of a formula 𝜓
and a list of sets 𝑉® = (𝑉1, . . . , 𝑉𝑛 ) in which 𝑉𝑖 consists of actual arguments 𝑛®𝑖 such that 𝑃𝑖 (𝑛®𝑖 ) has
been visited. The reduction relation is defined by
 (𝜓 1 □ 𝜓 2, (𝑉1, . . . , 𝑉𝑛 )) −→ (𝜓𝑖 , (𝑉1, . . . , 𝑉𝑛 ))                                                □ ∈ {∧, ∨}, 𝑖 ∈ {1, 2}
     (𝑃𝑖′ (𝑛®𝑖 ), (𝑉1, . . . , 𝑉𝑛 )) −→ (𝜑𝑖′ [𝑛®𝑖 /𝑉®𝑖 ], (𝑉1, . . . , 𝑉𝑖 ∪ {(𝑛®𝑖 )}, . . . , 𝑉𝑛 ))            ∀𝑚
                                                                                                                ® ∈ 𝑉𝑖 . 𝑚
                                                                                                                         ® ≻𝑅𝑖 𝑛®𝑖
     (𝑃𝑖′ (𝑛®𝑖 ), (𝑉1, . . . , 𝑉𝑛 )) −→ false                                                         𝜉𝑖 = 𝜇 ∧ ∃𝑚
                                                                                                                ® ∈ 𝑉𝑖 . 𝑚
                                                                                                                         ® ⊁𝑅𝑖 𝑛®𝑖
     (𝑃𝑖′ (𝑛®𝑖 ), (𝑉1, . . . , 𝑉𝑛 )) −→ true                                                          𝜉𝑖 = 𝜈 ∧ ∃𝑚
                                                                                                                ® ∈ 𝑉𝑖 . 𝑚
                                                                                                                         ® ⊁𝑅𝑖 𝑛®𝑖
(where 𝜑 ′ is the formula defined above, stemming from the definition of 𝑃𝑖′ ) and this reduction
process always terminates because ≻𝑅𝑖 is disjunctively well-founded. A normal form is true, false
or (atomic, 𝑉® ) for some closed atomic formula atomic, so a normal form is associated to a truth
value. Then we can reverse the reduction backwards and assign a truth value to each configuration.
A configuration (𝜓, 𝑉® ) with 𝜓 = 𝜓 1 ∧ 𝜓 2 or 𝜓 1 ∨ 𝜓 2 has successors, and its truth value is the
conjuction or the disjunction of those of the successors depending on 𝜓 . We define 𝐿Fix (𝑥, 𝑦) = 1 if
and only if the value assigned to (𝜑 ′, (∅, . . . , ∅)) is true. Note that 𝐿Fix (𝑥, 𝑦) is computable (provided
that every ranking function in ℜ𝑖 is computable).
  We say that a subset ℜ ⊆ (𝑍 → N) of ranking functions on a set 𝑍 is fine if, for every 𝑥, 𝑦 ∈ 𝑍 ,
there exists 𝑟 ∈ ℜ such that 𝑟 (𝑥) > 𝑟 (𝑧).
  Theorem 7.2. Assume that ℜ𝑖 is fine for every 𝑖. Then sup𝑦 inf 𝑥 𝐿Fix (𝑥, 𝑦) = 1 implies the truth of
the input formula.
    Proof Sketch. We prove the contraposition. Assume that the input formula is false, and assume
𝑦 ∈ 𝑌 . It suffices to find 𝑥 ∈ 𝑋 such that sup𝑦 inf 𝑥 𝐿Fix (𝑥, 𝑦) = −1. By the game semantics of the
fixed-point logic, the opponent has a winning strategy 𝜎 for the game induced by the input formula.
For every proponent strategy 𝜎 ′ , the play determined by 𝜎 and 𝜎 ′ reaches a false atomic formula or
diverges with an infinitely deep recursive calls to a 𝜇-predicate. The evaluation of such a recursive
call eventually violates the disjunctively-well-founded relation given by 𝑥. So the fact that 𝜎 ′ loses
against 𝜎 is witnessed by a finite set of finite reduction sequences. This is particularly true when
𝜎 ′ chooses each assignment of ∃ following the SAT strategy skeletons in 𝑥. When the proponent
follows the SAT strategy skeleton, the proponent always has finitely many options at each moment.
So the fact that the proponent cannot win the game following the SAT strategy skeletons in 𝑥
can be witnessed by a finitely branching tree with no infinite path, so it is a finite tree by König’s
lemma. Thanks to the finiteness, together with the fineness assumption on ℜ, we can give 𝑦 that
beats 𝑥.                                                                                             □
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                        27


   Both of the 𝑋 - and 𝑌 -components are join semilattices, and the Lagrangian 𝐿fix is anti-monotone
on 𝑋 and monotone on 𝑌 . So the monotonicity requirement is satisfied. Our implementation uses a
variant of the basic primal-dual procedure that is monotone on both 𝛼 ∈ 𝑋 and 𝛽 ∈ 𝑌 .
   Let us examine the primal and dual witness check problems. An interesting observation for the
termination analysis with disjunctively-well-founded relations is that the dual witness check is
reducible to a safety problem, using a transition system with an additional component that records
one of the already visited states. One may expect that the same idea should apply to the problem of
this section as well, but here is a subtlety. The soundness of the reduction relies on the setting of
Section 5, in which all non-deterministic branches in the transition system are demonic branching
∧ (i.e. whatever the choice, the system should terminate). In the presence of angelic branches ∨,
the reduction is unsound in general, because the proponent can make a choice that depends on
the value of the additional component, which is a kind of cheating as the additional component
is not a part of the real state of the transition system. One way to restore soundness is to ensure
that choices are independent of additional components by making the dependencies explicit using
(fresh) functional symbols. This is the approach of our implementation.
                                                                    𝜇
   Example 7.3. Conisder the predicate 𝑃 defined by 𝑃 (𝑥) = ∃𝑧.𝑃 (𝑧). Then 𝑃 (𝑥) is false for every 𝑥.
                                                                  𝜈
Applying the translation in Section 5.3, we obtain 𝑃 ′ (𝑥, 𝑦) = ∃𝑧.(𝑦 ≻𝑅 𝑧) ∧ 𝑃 ′ (𝑧, 𝑦) ∧ 𝑃 ′ (𝑧, 𝑧), but
this formula becomes true when we appropriately choose a disjunctively-well-founded relation 𝑅.
Note that 𝑃 ′ is the greatest fixed-point, corresponding to the fact that Section 5.3 translates the
termination problem to a safety problem. Let 𝑟 (𝑥) := max(𝑥, 0) and 𝑟 ′ (𝑥) := max(3 − 𝑥, 0). Our
strategy is to choose 𝑧 from 0, 1 so that 𝑧 ≠ 𝑦. Then 𝑦 ≻𝑅 𝑧 holds for every 𝑦, and thus 𝑃 ′ (𝑥, 𝑦) is
true for every 𝑥 and 𝑦. Note that the choice of 𝑧 depends on the additional component 𝑦.
                                                                                                         𝜈
   Our implementation reduces the problem to find an appropriate function 𝑓 such that 𝑃 ′′ (𝑥, 𝑦) =
(𝑦 ≻𝑅 𝑓 (𝑥)) ∧ 𝑃 ′ (𝑓 (𝑥), 𝑦) ∧ 𝑃 ′ (𝑓 (𝑥), 𝑓 (𝑥)). The definition of 𝑃 ′′ is obtained by replacing 𝑧 with
𝑓 (𝑥), expressing that the choice of 𝑧 should only depend on 𝑥. This approach is sound, and there is
no pair (𝑓 , 𝑅) that makes 𝑃 ′′ (𝑥, 𝑦) true.                                                             □

7.3   Propotype Implementation and Evaluation
We implemented the new method proposed in this section as MuStrat, a prototype validity checker
for a fixpoint-logic over quantified linear integer and real arithmetic. Additionally, for evaluation,
we conducted comparative experiments with MuVal [Unno et al. 2023], the existing state-of-the-art
fixpoint logic validity checker. We ran the tools on (1) the 335 (non-)termination benchmarks from
termCOMP (C Integer category), (2) the 202 fixpoint logic benchmarks provided by the authors of
MuVal [Unno et al. 2023], and (3) the 47 game-solving benchmarks from [Heim and Dimitrova
2024], with a timeout of 300 seconds in the StarExec environment. The results are summarized
in scatter plots, respectively in Figures 1, 2, and 3. In (1) and (2), although the total number of
solved problems is slightly lower than MuVal, MuStrat successfully solved 6 and 7 problems
respectively that MuVal timed out on. Additionally, in problems where strategy synthesis is crucial,
such as non-termination verification and branching-time properties verification, MuStrat was able
to find witnesses faster than MuVal in more cases. (Note that in Figure 1, the red dots represent
non-terminating instances.) MuStrat also has an engineering advantage as it uses the highly
efficient Spacer as the backend CHC solver, allowing it to quickly solve examples that require the
synthesis of complex inductive invariants. On the other hand, MuVal, through CEGIS iterations,
can simultaneously synthesize the necessary ranking functions and inductive invariants, which may
be inter-dependent, allowing it to solve problem instances requiring complex ranking functions
that MuStrat times out on. On the other hand, the dedicated game solver rpgsolve, proposed in
the paper that provided the benchmark set (3) [Heim and Dimitrova 2024], successfully solved all
28                                                 Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham



        100                              100                                   100
     MuVal




                                      MuVal




                                                                            MuVal
             10                               10                                    10




              1                                1                                     1




                  1      10     100                1      10     100                     1      10     100
                      MuStrat                          MuStrat                               MuStrat



     Fig. 1. MuStrat vs. MuVal on     Fig. 2. MuStrat vs. MuVal on         Fig. 3. MuStrat vs. MuVal on
     the (non-)term. benchmark set    the fixed-point logic benchmark      the game solving benchmark set
     from termCOMP (C Integer).       set from [Unno et al. 2023].         from [Heim and Dimitrova 2024].


but two problems. To achieve performance close to rpgsolve, implementation tuning unrelated to
the core algorithm (e.g., efficiently handling the DAG-shaped resolution proofs returned by Spacer
without expanding them into trees) is necessary. This is future work for tool development and is
out of scope for the present paper. Additionally, it should be noted that rpgsolve targets a limited
subset of fixpoint logic, making it inapplicable to the benchmark sets (1) and (2).

8     Related Work and Concluding Remarks
The development of unifying frameworks for algorithms in program analysis and verification is
a common theme. Abstract Interpretation [Cousot and Cousot 1977, 1979] is perhaps the most
prominent example of a mathematical framework that describes a variety of program analysis
algorithms. While in some instances the primal or dual problems in our framework can be seen
as solved by computing an abstract fixpoint in a suitable domain (e.g., in CEGAR and in primal-
dual Houdini), it seems to us that the entirety of Algorithm 1 is not an instance of abstract
fixpoint computation. We consider it an interesting avenue for future work to better understand
the connection between our Lagrangian-based algorithmic framework and abstract interpretation.
In particular, primal-dual search may be related to widening and narrowing.
   In optimization and constraint solving, the so called inference dual and the relaxation dual (which
is a special case of the inference dual) have been observed to underlie many algorithms [Hooker
2000, 2006]. In these terms, the duality of our generalized Lagrangian can be seen as both an
inference dual and a relaxation dual, in the sense that, e.g., some 𝑥 ∈ 𝑋 such that sup𝑦 𝐿(𝑥, 𝑦) = 𝑣
can be seen as a proof that inf 𝑥 sup𝑦 𝐿(𝑥, 𝑦) ≤ 𝑣. In some cases Algorithm 1 can yield what [Hooker
2006] calls a nogood-based search method, but Algorithm 1 seems to be more general. Exploring
the connection between our framework and more algorithms and mathematical frameworks for
constraint satisfaction and optimization is an interesting avenue for future work.
   Applications of linear/semidefinite programming and their (relaxation) duals to verification can
be found in the literature. Cousot [2005] proposed an approach to reduce a verification problem
into linear or semidefinite programming using Lagrangian relaxation as a key component. Gonnord
et al. [2015] synthesizes ranking functions by formulating the problem as a linear programming
problem. Their use of extremal counterexamples to guarantee finiteness and therefore termination
bears some resemblance to the choice of terms (mentioned at the end of Section 6) that guarantee
termination in the Quantified LRA solver discussed in Section 6.
   The duality in verification and constraint solving often appears as the duality between the
proponent and opponent of a game. For example, the quantified SMT solver by Farzan and Kincaid
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                         29


[2016] studied in Section 6 is presented in terms of games. Many quantified SMT solvers Bjørner
and Janota [2015]; Bonacina et al. [2023]; Murphy and Kincaid [2024] are inspired by the game
semantics of logical formulas and the duality inherent in it. For example, Murphy and Kincaid
[2024] improved the approach by Farzan and Kincaid [2016]: whereas the original method adds a
strategy skeleton that could beat the current opponent strategy, the new method seeks a strategy
skeleton that not only beats the current opponent strategy but also is winning on a subgame. It is
an interesting challenge to see if these advanced ideas can be understood and developed within a
Lagrangian-based framework.
   An important family of procedures that this paper does not deal with is IC3/PDR [Bradley 2011;
Een et al. 2011] and its relatives such as GPDR [Hoder and Bjørner 2012] and Spacer [Komuravelli
et al. 2015, 2014; Tsukada and Unno 2024; Vediramana Krishnan et al. 2023]. We developed some
candidate Lagrangians aiming to capture the behavior of PDR, some of which seem to capture
PDR to a certain extent. Detailed analysis of PDR based on Lagrangians is an important topic for
future work. According to Tsukada and Unno [2022], a game solving procedure by Farzan and
Kincaid [2018] can be related to PDR, so the analysis of PDR would be beneficial to understand
their procedure as well.
   The primal-dual algorithms of [Padon et al. 2022; Unno et al. 2023] have inspired the development
of our Lagrangian-based framework. Section 4 presented a suitable Lagrangian that shows that the
high-level structure of primal-dual Houdini [Padon et al. 2022] is an instance of our framework.
We believe the algorithm of [Unno et al. 2023] can similarly be captured by our framework, and we
are still developing a suitable Lagrangian. One challenge there is that the primal and dual sides
exchange information only under certain validity conditions. Therefore, either developing a suitable
Lagrangian or possibly extending our framework is a planned future work.

Acknowledgments
We thank the anonymous reviewers for comments which improved the paper. The research leading
to these results has received funding from the European Research Council under the European
Union’s Horizon 2020 research and innovation programme (grant agreement No [759102-SVIS]).
This research was partially supported by the Israel Science Foundation (ISF) grant No. 2117/23 and
JSPS KAKENHI Grant Numbers JP20H04162, JP20H05703, JP19H04084, JP24H00699, JP23K24826,
and JP23K24820. This research was partially supported by a research grant from the Center for
New Scientists at the Weizmann Institute of Science and by a grant from the Azrieli Foundation.

References
Thomas Ball, Rupak Majumdar, Todd D. Millstein, and Sriram K. Rajamani. 2001a. Automatic Predicate Abstraction of C
  Programs. In Proceedings of the 2001 ACM SIGPLAN Conference on Programming Language Design and Implementation
  (PLDI), Snowbird, Utah, USA, June 20-22, 2001, Michael Burke and Mary Lou Soffa (Eds.). ACM, 203–213. https://doi.org/
  10.1145/378795.378846
Thomas Ball, Andreas Podelski, and Sriram K. Rajamani. 2001b. Boolean and Cartesian Abstraction for Model Checking C
  Programs. In Tools and Algorithms for the Construction and Analysis of Systems, 7th International Conference, TACAS 2001
  Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2001 Genova, Italy, April 2-6,
  2001, Proceedings (Lecture Notes in Computer Science, Vol. 2031), Tiziana Margaria and Wang Yi (Eds.). Springer, 268–283.
  https://doi.org/10.1007/3-540-45319-9_19
Dimitris Bertsimas and John N. Tsitsiklis. 1997. Introduction to linear optimization. Athena scientific optimization and
  computation series, Vol. 6. Athena Scientific.
Nikolaj Bjørner and Mikoláš Janota. 2015. Playing with Quantified Satisfaction. In 20th International Conferences on
  Logic for Programming, Artificial Intelligence and Reasoning (LPAR 2015) (EPiC Series in Computing). EasyChair. https:
  //doi.org/10.29007/vv21
Maria Paola Bonacina, Stéphane Graham-Lengrand, and Christophe Vauthier. 2023. QSMA: A New Algorithm for Quantified
  Satisfiability Modulo Theory and Assignment. In Automated Deduction - CADE 29 - 29th International Conference on
30                                                       Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


   Automated Deduction, Rome, Italy, July 1-4, 2023, Proceedings (Lecture Notes in Computer Science, Vol. 14132), Brigitte
   Pientka and Cesare Tinelli (Eds.). Springer, 78–95. https://doi.org/10.1007/978-3-031-38499-8_5
Stephen P. Boyd and Lieven Vandenberghe. 2014. Convex Optimization. Cambridge University Press. https://doi.org/10.
   1017/CBO9780511804441
Aaron R. Bradley. 2011. SAT-Based Model Checking without Unrolling. In Lecture Notes in Computer Science. Springer
   Berlin Heidelberg, 70–87. https://doi.org/10.1007/978-3-642-18275-4_7
Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2000. Counterexample-Guided Abstraction
   Refinement. In Computer Aided Verification, 12th International Conference, CAV 2000, Chicago, IL, USA, July 15-19, 2000,
   Proceedings (Lecture Notes in Computer Science, Vol. 1855), E. Allen Emerson and A. Prasad Sistla (Eds.). Springer, 154–169.
   https://doi.org/10.1007/10722167_15
Byron Cook, Andreas Podelski, and Andrey Rybalchenko. 2005. Abstraction Refinement for Termination. In Static Analysis
   Symposium (SAS 2005) (LNCS, Vol. 3672). Springer Berlin Heidelberg, 87–101. https://doi.org/10.1007/11547662_8
Byron Cook, Andreas Podelski, and Andrey Rybalchenko. 2006. Termination proofs for systems code. In Proceedings of
   the 27th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI ’06). ACM, 415–426.
   https://doi.org/10.1145/1133981.1134029
Patrick Cousot. 2005. Proving Program Invariance and Termination by Parametric Abstraction, Lagrangian Relaxation and
   Semidefinite Programming. In Verification, Model Checking, and Abstract Interpretation (LNCS, Vol. 3385). Springer Berlin
   Heidelberg, 1–24. https://doi.org/10.1007/978-3-540-30579-8_1
Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs
   by Construction or Approximation of Fixpoints. In Proceedings of the 4th ACM SIGACT-SIGPLAN Symposium on Principles
   of Programming Languages (Los Angeles, California) (POPL ’77). ACM, New York, NY, USA, 238–252. https://doi.org/10.
   1145/512950.512973
Patrick Cousot and Radhia Cousot. 1979. Systematic Design of Program Analysis Frameworks. In Proceedings of the 6th
   ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (San Antonio, Texas) (POPL ’79). ACM, New
   York, NY, USA, 269–282. https://doi.org/10.1145/567752.567778
Niklas Een, Alan Mishchenko, and Robert Brayton. 2011. Efficient implementation of property directed reachability. In 2011
   Formal Methods in Computer-Aided Design (FMCAD). 125–134.
Azadeh Farzan and Zachary Kincaid. 2016. Linear Arithmetic Satisfiability via Strategy Improvement. In Proceedings of
   the Twenty-Fifth International Joint Conference on Artificial Intelligence, IJCAI 2016, New York, NY, USA, 9-15 July 2016,
   Subbarao Kambhampati (Ed.). IJCAI/AAAI Press, 735–743. http://www.ijcai.org/Abstract/16/110
Azadeh Farzan and Zachary Kincaid. 2018. Strategy synthesis for linear arithmetic games. Proc. ACM Program. Lang. 2,
   POPL (2018), 61:1–61:30. https://doi.org/10.1145/3158149
Cormac Flanagan, Rajeev Joshi, and K. Rustan M. Leino. 2001. Annotation inference for modular checkers. Inf. Process. Lett.
   77, 2-4 (2001), 97–108. https://doi.org/10.1016/S0020-0190(00)00196-4
Cormac Flanagan and K. Rustan M. Leino. 2001. Houdini, an Annotation Assistant for ESC/Java. In FME 2001: Formal
   Methods for Increasing Software Productivity, International Symposium of Formal Methods Europe, Berlin, Germany, March
   12-16, 2001, Proceedings (Lecture Notes in Computer Science, Vol. 2021), José Nuno Oliveira and Pamela Zave (Eds.). Springer,
   500–517. https://doi.org/10.1007/3-540-45251-6_29
Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. 2014. ICE: A Robust Framework for Learning Invariants.
   In Computer Aided Verification - 26th International Conference, CAV 2014, Held as Part of the Vienna Summer of Logic,
   VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8559), Armin Biere and
   Roderick Bloem (Eds.). Springer, 69–87. https://doi.org/10.1007/978-3-319-08867-9_5
Yeting Ge and Leonardo Mendonça de Moura. 2009. Complete Instantiation for Quantified Formulas in Satisfiabiliby Modulo
   Theories. In Computer Aided Verification, 21st International Conference, CAV 2009, Grenoble, France, June 26 - July 2, 2009.
   Proceedings (Lecture Notes in Computer Science, Vol. 5643), Ahmed Bouajjani and Oded Maler (Eds.). Springer, 306–320.
   https://doi.org/10.1007/978-3-642-02658-4_25
Patrice Godefroid, Aditya V. Nori, Sriram K. Rajamani, and Sai Deep Tetali. 2010. Compositional may-must program analysis:
   unleashing the power of alternation. In Proceedings of the 37th annual ACM SIGPLAN-SIGACT symposium on Principles of
   programming languages (POPL ’10). ACM. https://doi.org/10.1145/1706299.1706307
Laure Gonnord, David Monniaux, and Gabriel Radanne. 2015. Synthesis of ranking functions using extremal counterexamples.
   In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI ’15).
   ACM, 608–618. https://doi.org/10.1145/2737924.2737976
Philippe Heim and Rayna Dimitrova. 2024. Solving Infinite-State Games via Acceleration. Proceedings of the ACM on
   Programming Languages 8, POPL (Jan. 2024), 1696–1726. https://doi.org/10.1145/3632899
Kryštof Hoder and Nikolaj Bjørner. 2012. Generalized Property Directed Reachability. In Theory and Applications of
   Satisfiability Testing – SAT 2012. Springer Berlin Heidelberg, 157–171. https://doi.org/10.1007/978-3-642-31612-8_13
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                             31


J. N. Hooker. 2000. Logic-Based Methods for Optimization: Combining Optimization and Constraint Satisfaction. Wiley, New
    York. https://doi.org/10.1002/9781118033036
J. N. Hooker. 2006. Duality in Optimization and Constraint Satisfaction. In The 3rd International Conference on the Integration
    of Constraint Programming, Artificial Intelligence, and Operations Research (CPAIOR 2006) (LNCS, Vol. 3990). Springer
    Berlin Heidelberg, 3–15. https://doi.org/10.1007/11757375_3
Susmit Jha, Sumit Gulwani, Sanjit A. Seshia, and Ashish Tiwari. 2010. Oracle-guided component-based program synthesis.
    In Proceedings of the 32nd ACM/IEEE International Conference on Software Engineering - Volume 1, ICSE 2010, Cape Town,
    South Africa, 1-8 May 2010, Jeff Kramer, Judith Bishop, Premkumar T. Devanbu, and Sebastián Uchitel (Eds.). ACM,
    215–224. https://doi.org/10.1145/1806799.1806833
Ranjit Jhala and Kenneth L. McMillan. 2006. A Practical and Complete Approach to Predicate Refinement. In TACAS ’06
    (Lecture Notes in Computer Science, Vol. 3920). Springer, 459–473.
Anvesh Komuravelli, Nikolaj Bjørner, Arie Gurfinkel, and Kenneth L. Mcmillan. 2015. Compositional verification of
    procedural programs using horn clauses over integers and arrays. In 2015 Formal Methods in Computer-Aided Design
    (FMCAD). IEEE. https://doi.org/10.1109/fmcad.2015.7542257
Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2014. SMT-Based Model Checking for Recursive Programs. In
    Computer Aided Verification (CAV). Springer International Publishing, 17–34. https://doi.org/10.1007/978-3-319-08867-9_2
Satoshi Kura, Hiroshi Unno, and Ichiro Hasuo. 2021. Decision Tree Learning in CEGIS-Based Termination Analysis. In CAV
    ’21 (Lecture Notes in Computer Science). Springer, 75–98.
Xie Li, Yi Li, Yong Li, Xuechao Sun, Andrea Turrini, and Lijun Zhang. 2020. SVMRanker: A General Termination Analysis
    Framework of Loop Programs via SVM. ACM, 1635–1639.
Charlie Murphy and Zachary Kincaid. 2024. Quantified Linear Arithmetic Satisfiability via Fine-Grained Strategy Improve-
    ment. In CAV 2024. Springer, Cham, 89–109.
Robert Nieuwenhuis, Albert Oliveras, and Cesare Tinelli. 2006. Solving SAT and SAT Modulo Theories: From an abstract
    Davis–Putnam–Logemann–Loveland procedure to DPLL(T ). J. ACM 53, 6 (2006), 937–977. https://doi.org/10.1145/
    1217856.1217859
Oded Padon, James R. Wilcox, Jason R. Koenig, Kenneth L. McMillan, and Alex Aiken. 2022. Induction duality: primal-
    dual search for invariants. Proceedings of the ACM on Programming Languages 6, POPL (Jan. 2022), 1–29. https:
    //doi.org/10.1145/3498712
A. Podelski and A. Rybalchenko. 2004. Transition invariants. In Proceedings of the 19th Annual IEEE Symposium on Logic in
    Computer Science (LICS 2004). IEEE. https://doi.org/10.1109/lics.2004.1319598
Takeshi Tsukada and Hiroshi Unno. 2022. Software model-checking as cyclic-proof search. Proceedings of the ACM on
    Programming Languages 6, POPL (jan 2022), 1–29. https://doi.org/10.1145/3498725
Takeshi Tsukada and Hiroshi Unno. 2024. Inductive Approach to Spacer. Proc. ACM Program. Lang. 8, PLDI, Article 227
    (June 2024), 24 pages. https://doi.org/10.1145/3656457
Hiroshi Unno, Tachio Terauchi, Yu Gu, and Eric Koskinen. 2023. Modular Primal-Dual Fixpoint Logic Solving for Temporal
    Verification. Proc. ACM Program. Lang. 7, POPL (2023), 2111–2140. https://doi.org/10.1145/3571265
Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. 2021. Constraint-Based Relational Verification. In CAV ’21 (Lecture Notes
    in Computer Science). Springer, 742–766.
Hari Govind Vediramana Krishnan, YuTing Chen, Sharon Shoham, and Arie Gurfinkel. 2023. Global guidance for local
    generalization in model checking. Formal Methods in System Design (March 2023). https://doi.org/10.1007/s10703-023-
    00412-3
32                                                   Takeshi Tsukada, Hiroshi Unno, Oded Padon, and Sharon Shoham


A    Proof of Theorem 4.3
In this proof, we will refer to “S with bad states 𝐵” the transition system obtained by replacing the
bad states of S with 𝐵. The key to the proof is the following claim:
Claim. For each 𝑝 ∈ 𝐵 I , at least one of the following holds:
   (1) some 𝜗 ⊆ P is an inductive invariant for S with bad states {𝑠 | 𝑠 ̸ |= 𝑝}, or
   (2) some 𝜛 ⊆ |S| is an inductive invariant for I with bad states {𝑝}.
    Proof. Let 𝜗 ⊆ P be the maximum inductive invariant of P. Note that this is the “strongest”
                                                         Ó
invariant since 𝜗 is regarded as the conjunction 𝑝 ∈𝜗 𝑝. The maximum        Ð           inductive invariant exists
since, for a family 𝜗𝑖 ⊆ P of inductive invariants, their union 𝑖 𝜗𝑖 is also an inductive invariant.
    Let 𝜛 ⊆ |S| be the subset of states satisfying all 𝑝 ∈ 𝜗, i.e. 𝜛 := {𝑠 ∈ |S| | ∀𝑝 ∈ 𝜗 . 𝑠 |= 𝑝}. Since 𝜗
is an invariant, 𝜛 is closed under transition. Then 𝜛 |= 𝑝 ⇐⇒ 𝑝 ∈ 𝜗. The right-to-left direction
comes from the definition of 𝜛. To see the other direction, assume 𝜛 |= 𝑝. Then 𝜗 ∪ {𝑝} is an
invariant: if 𝑠 |= 𝜗 ∪ {𝑝} and 𝑠 ⇝S 𝑠 ′ , then 𝑠 ′ |= 𝜗 by the invariance of 𝜗, so 𝑠 ′ ∈ 𝜛 that implies
𝑠 ′ |= 𝑝. By the maximality of 𝜗, we have 𝜗 = 𝜗 ∪ {𝑝}, that means, 𝑝 ∈ 𝜗.
    The maximum inductive invariant 𝜗 is closed under the transition. Assume 𝑝 ⇝I 𝑝 ′ and 𝑝 ∈ 𝜗.
It suffices to show that 𝜗 ∪ {𝑝 ′ } is an inductive invariant (because 𝜗 is the maximum invariant).
Assume 𝑠 ⇝S 𝑠 ′ and 𝑠 |= 𝜗 ∪ {𝑝 ′ }. Then 𝑠 ′ |= 𝜗 since 𝜗 is an inductive invariant. We have 𝑠 ⇝S 𝑠 ′ ,
𝑝 ⇝I 𝑝 ′ , 𝑠 |= 𝑝, 𝑠 ′ |= 𝑝 and 𝑠 |= 𝑝 ′ . By the duality, 𝑠 ′ |= 𝑝 ′ . So 𝑠 ′ |= 𝜗 ∪ {𝑝 ′ } as expected.
    This means that 𝜛 is a dual-inductive invariant. Assume a transition 𝑝 ⇝I 𝑝 ′ and 𝜛 |= 𝑝. Then
𝑝 ∈ 𝜗. Since 𝜗 is closed under ⇝, we have 𝑝 ′ ∈ 𝜗. So 𝜛 |= 𝑝 ′ .
    Now we have a pair (𝜗, 𝜛) of an inductive invariant 𝜗 and a dual-inductive invariant 𝜛 related by
𝜛 |= 𝑝 ⇔ 𝑝 ∈ 𝜗. If 𝑞 ∈ 𝜗, the first condition is met. If 𝑞 ∉ 𝜗, then ¬(𝜛 |= 𝑞), i.e. there exists 𝑠 ∈ 𝜛
such that 𝑥 ̸ |= 𝑝. So the dual-inductive invariant 𝜛 witnesses the safety of I with respect to {𝑞}. □
   We prove the theorem using the claim.
   Assume that the latter case holds for every 𝑝 ∈ 𝐵 I . Let 𝜛 𝑝 ⊆ |S| be a safe inductive invariant
                                                                                                   Ð for
I with bad states {𝑝}. Since the set of inductive invariants is closed under the union, 𝜛 := 𝑝 𝜛 𝑝
is an inductive invariant for I. For every 𝑝 ∈ 𝐵 I , we have 𝑝 ̸ |= 𝜛 𝑝 and hence 𝑝 ̸ |= 𝜛. So 𝜛 is a safe
inductive invariant for I.
   Assume that the former holds for some 𝑝 ∈ 𝐵 I . That means, the safety of S with respect to
{𝑠 | 𝑠 ̸ |= 𝑝} is witnessed by some 𝜗 ⊆ P. Then 𝑠 |= 𝜗 ⇒ ¬(𝑠 ̸ |= 𝑝) ⇔ 𝑠 |= 𝑝 ⇒ 𝑠 ∉ 𝐵 S . So 𝜗
witnesses the safety of S with respect to 𝐵 S .

B    Proof of Lemma 6.6
                                                                                                      𝜑
To prove the right-to-left direction, we prove the following claim by induction on 𝜋: if 𝐿FK (𝜚, 𝜋) = −1,
d𝑛 𝜑 |𝜋⟩ is invalid. The claim
then                                Ó𝑛 is trivial     for 𝜋 = •. Assume 𝜋 = ∀𝑥 .𝜋 ′ . Then 𝜑 = ∀𝑥 .𝜑 ′ and 𝜚 =
                                                ′           ′                                        ′         ′
  𝑖=1 𝑡𝑖 .𝜚 𝑖 . Then ⟨𝜚 |𝜑 |𝜋⟩ =     𝑖=1 ⟨𝜚 𝑖 |𝜑 [𝑡𝑖 /𝑥] |𝜋 [𝑡𝑖 /𝑥]⟩, which is invalid. So ⟨𝜚 𝑖 |𝜑 [𝑡𝑖 /𝑥] |𝜋 [𝑡𝑖 /𝑥]⟩
                                                                    ′             ′
is invalid for some 𝑖. By the induction hypothesis, 𝜑 [𝑡𝑖 /𝑥] |𝜋 [𝑡𝑖 /𝑥]⟩ is invalid. It is not difficult
to see that (𝜑 ′ [𝑡𝑖 /𝑥] |𝜋 ′ [𝑡𝑖 /𝑥]⟩) = (𝜑 ′ |𝜋 ′ ⟩) [𝑡𝑖 /𝑥], so ∀𝑥 .(𝜑 ′ |𝜋 ′ ⟩) is invalid. Assume 𝜋 = 𝑡 .𝜋 ′ . Then
𝜑 = ∃𝑥 .𝜑 ′ and 𝜚 = ∃𝑥 .𝜚 ′ . Since ⟨𝜚 |𝜑 |𝜋⟩ = ⟨𝜚 ′ [𝑡/𝑥] |𝜑 ′ [𝑡/𝑥] |𝜋 ′ ⟩, by the induction hypothesis,
(𝜑 ′ [𝑡/𝑥] |𝜋 ′ ⟩) = (𝜑 |𝜋 ′ ⟩) is invalid. Assume 𝜋 = 𝜋 1 ⊔ 𝜋2 . Then ⟨𝜚 |𝜑 |𝜋⟩ = ⟨𝜚 |𝜑 |𝜋1 ⟩ ∨ ⟨𝜚 |𝜑 |𝜋2 ⟩ and
this formula is invalid. So both ⟨𝜚 |𝜑 |𝜋1 ⟩ and ⟨𝜚 |𝜑 |𝜋2 ⟩ are invalid, and by the induction hypothesis,
both 𝜑 |𝜋1 ⟩ and 𝜑 |𝜋2 ⟩ are invalid. So (𝜑 |𝜋⟩) = (𝜑 |𝜋1 ⟩) ∨ (𝜑 |𝜋2 ⟩) is invalid.
   To prove the left-to-right direction, assume that 𝜑 |𝜋⟩ is invalid. We construct an UNSAT strategy
skeleton 𝜚 such that 𝐿FK (𝜚, 𝜋) = −1 by induction on 𝜋. If 𝜋 = •, let 𝜑 = •. Assume 𝜋 = ∀𝑥 .𝜋 ′ . Then
                            𝜑

𝜑 = ∀𝑥 .𝜑 ′ and (𝜑 |𝜋⟩) = ∀𝑥 .(𝜑 ′ |𝜋 ′ ⟩). Since this formula is invalid, there exists a rational number
𝑟 ∈ Q such that (𝜑 ′ |𝜋 ′ ⟩) [𝑟 /𝑥] = (𝜑 ′ [𝑟 /𝑥] |𝜋 ′ [𝑟 /𝑥]⟩) is invalid. By the induction hypothesis, there
A Primal-Dual Perspective on Program Verification Algorithms (Extended Version)                                   33

                       (𝜑 ′ [𝑟 /𝑥 ] )
exists 𝜚 ′ such that 𝐿FK            (𝜚 ′, 𝜋 ′ ) = −1. Then 𝜚 := 𝑟 .𝜚 ′ satisfies the requirement. Assume 𝜋 = 𝑡 .𝜋 ′ .
Then 𝜑 = ∃𝑥 .𝜑 and (𝜑 |𝜋⟩) = (𝜑 ′ [𝑡/𝑥] |𝜋 ′ ⟩), which is invalid. By the induction hypothesis, there
                  ′
                         (𝜑 ′ [𝑡 /𝑥 ] ) ′ ′
exists 𝜚 ′ such that 𝐿FK               (𝜚 , 𝜋 ) = −1. Then 𝜚 := ∃𝑥 .𝜚 ′ satisfies the requirement. Assume
𝜋 = 𝜋1 ⊔ 𝜋 2 . Then (𝜑 |𝜋⟩) = (𝜑 |𝜋1 ⟩) ∨ (𝜑 |𝜋2 ⟩), which is invalid. By the induction hypothesis, we
have 𝜚 1′ and 𝜚 2′ such that both ⟨𝜚 1′ |𝜑 |𝜋 1 ⟩ and ⟨𝜚 2′ |𝜑 |𝜋2 ⟩ are invalid. Then 𝜚 := 𝜚 1 ∩ 𝜚 2 satisfies the
requirement.
