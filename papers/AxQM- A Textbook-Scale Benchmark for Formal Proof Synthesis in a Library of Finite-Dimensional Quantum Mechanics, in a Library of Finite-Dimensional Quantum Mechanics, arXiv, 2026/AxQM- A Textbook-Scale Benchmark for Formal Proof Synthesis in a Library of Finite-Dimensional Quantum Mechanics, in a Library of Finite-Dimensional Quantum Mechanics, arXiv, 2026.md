                                            AxQM: A Textbook-Scale Benchmark for Formal Proof Synthesis
                                               in a Library of Finite-Dimensional Quantum Mechanics
                                            Weichen Winston Yin1 , Jacob M. Taylor1 , Dirk R. Englund1,3,∗ , Frank H.L. Koppens2,4,∗
                                               1
                                                 Axiomatic AI. 2 Institut de Ciències Fotòniques (ICFO). 3 Massachusetts Institute of Technology
                                                (MIT). 4 Institució Catalana de Recerca i Estudis Avançats (ICREA). ∗ Corresponding author(s):
                                                                          dirk@axiomatic-ai.com, frank.koppens@icfo.eu
arXiv:2609.05157v1 [quant-ph] 4 Sep 2026




                                                                                        September 7, 2026


                                                                                              Abstract
                                                       Formalizing mathematics in a proof assistant, where a machine checks every definition, state-
                                                   ment and proof, has set a new standard of rigor. Large language models are now capable of
                                                   formalizing autonomously, even at the scale of whole textbooks. We bring this standard of rigor
                                                   to physics, where theoretical arguments carry idealizations that are rarely stated fully, and any
                                                   logical gaps could have a cascading effect on interdependent results. Recognizing the need to
                                                   evaluate autoformalization systems for physics, we release AxQM, 1,019 kernel-checkable proof-
                                                   synthesis tasks over 479 items drawn from the textbook Quantum Computation and Quantum
                                                   Information by Nielsen and Chuang. The tasks are stated in a custom Lean library of finite-
                                                   dimensional quantum mechanics. By task count, it is the largest proof-synthesis benchmark in
                                                   physics by a factor of four. AxQM is derived from a near-complete formalization of the formal
                                                   portions of the textbook, so every task is guaranteed a solution, which we keep private. Grading
                                                   of the benchmark is done deterministically by the Lean kernel, which checks that the proof
                                                   compiles, that no sorry appears in it or in any declaration it depends on, and that it introduces
                                                   no new axioms.


                                           1    Introduction
                                           Formalization in a proof assistant is increasingly used by the mathematics community to achieve
                                           machine-checked rigor that eliminates the possibility of an incomplete proof. Lean 4 [1] is one such
                                           assistant: a programming language in which definitions, theorem statements and proofs are all
                                           written in code, and whose compiler accepts a proof only when a small trusted kernel has checked
                                           every step of it. Faced with the proof of a theorem formalized in Lean, a reviewer can now simply
                                           check that the statement carries the correct mathematical meaning, and fully trust that the proof
                                           of that statement has been checked down to the axioms by the kernel. The whole burden of review
                                           becomes a single question rather than pages upon pages of argument: does this formal statement
                                           say what it claims to say? With autoformalization, the translation of mathematical text into Lean
                                           code can now be performed by AI at scale, and what is produced this way has grown from single
                                           theorems to entire textbooks [2–4]. LLM formal provers for Lean now span reinforcement-learning
                                           systems [5–10], retrieval-augmented assistants [11, 12], and agentic scaffolds around general-purpose
                                           models, including one tool-assisted iterative prover [13] and a minimal open-source baseline [14].
                                               Outside of mathematics, physics stands to gain a great deal from this technological advancement.
                                           Formal reasoning in the physical sciences, machine-checked and traceable to physical foundations, is
                                           now within reach. In some ways, physics needs this more than mathematics does. Seldom is physical

                                                                                                  1
reasoning expressed at the level of mathematical rigor [15]. Everything from quantum field theory
to adiabatic elimination is full of assumptions and occasional hand-waving, yet remains sufficient
for predicting the outcomes of experiment. Where the reasoning is formalizable, formalization
has yielded fruitful results: formalizing the stability conditions of the two-Higgs-doublet potential
recently exposed an error in a widely cited paper [16], and a machine-verified proof has settled an
open conjecture in quantum optimization [17]. By moving to AI-assisted autonomous formalization,
physicists are confronted up front with new challenges, but can also benefit from advances in
verifiable computer-aided reasoning.
    Crucially, formalization must build upon a well-scaffolded set of mathematical axioms and
definitions that self-consistently enable lemmas and theorems that build upon that foundation. To
date, progress in this scaffolding is largely available only in a few branches of mathematics through
the community effort known as Mathlib [18]. Physics has begun to acquire the same scaffolding.
    PhysLean, formerly HepLean, collects formalized results across classical mechanics, relativity,
condensed matter, quantum field theory and string theory [15, 19], with supporting developments
in index notation and Wick’s theorem [20, 21] and an axiomatization of quantum field theory
[22]. Formalization is being attempted across physics more broadly, from chemical physics [23]
and the mean-field derivation of the Vlasov equation [24] to control theory [25], numerical analysis
[26], power-flow analysis [27] and particle-physics model building [28], with related work in other
proof assistants [29]. In quantum information, Lean-QIT builds an operational layer for quantum
Shannon theory, while Lean-Quantum builds it in a basis-independent way; Lean-QuantumInfo
covers finite-dimensional quantum information in over a thousand theorems [30–33].
    Individual formalized results in quantum information include Shor’s algorithm [34, 35], the
generalized quantum Stein’s lemma [33], CHSH rigidity [36], error correction [37], and the funda-
mental theorem of matrix-product states of tensor network theory [38], several of them assisted by
AI. Agentic autoformalization systems have also been built for the domain, targeting certified quan-
tum neural network design and quantum computation broadly [39, 40]. Quantum computation and
protocols have also been formalized in other proof assistants: in Coq [41–44] and in Isabelle/HOL
[45–47].
    Here we go beyond individual formalized results and apply autonomous formalization to a
physics textbook in full, releasing AxQM, a Lean 4 benchmark for the formalization of quantum
information and computing theory, built from the exercises in the textbook Quantum Computa-
tion and Quantum Information by Nielsen and Chuang [48]. Following the scope of the textbook
itself, this benchmark is purposely limited to finite-dimensional Hilbert spaces. Every construction
therefore stays inside Mathlib’s finite-dimensional linear algebra library, where the spectral theo-
rem, the trace, and tensor products are available without functional-analytic hypotheses. Infinite-
dimensional systems and unbounded operators are outside this scope.


2    The Benchmark
AxQM consists of 1,019 proof-synthesis tasks over 479 items, covering a large majority of the
textbook’s exercises and theorems (Fig. 1). Each task is a single formal statement in Lean whose
proof is to be filled in, and each item (e.g. Theorem 11.8, Exercise 12.15) can include one or
more tasks that are intended to capture the item’s full meaning. Topics include the density-
operator formalism and the Schmidt decomposition, universal gate sets and circuit decompositions,
the quantum Fourier transform with order-finding and Grover search, quantum channels and the
distance measures on them, stabilizer codes and fault tolerance, and von Neumann entropy and its
inequalities.


                                                 2
                           200   items                                             196
                           175   tasks
                           150




                   count
                           125

                           100

                            75

                            50
                                                     24
                            25

                             0
                                 2       4   5      6      7      8         9     10     11   12
                                                 chapter of Nielsen & Chuang


Figure 1: Coverage: items and tasks by chapter of Nielsen and Chuang. Items refer to explicitly
numbered items in the book: theorems, problems, exercises, and examples. Tasks are individual
Lean theorem statements that capture all or part of an item. Each item may have multiple tasks.
Chapters 1 (overview) and 3 (classical computation) contribute no items to the benchmark. Chap-
ters 7 (physical realization) and 10 (error correction) are the densest in tasks per item.

                                     Proof length estimate        Tasks         Share
                                     very small                       158       15.5%
                                     small                            324       31.8%
                                     moderate                         280       27.5%
                                     large                            190       18.6%
                                     very large                        67        6.6%
                                     Total                        1,019         100%

Table 1: Proof length estimates for the 1,019 benchmark tasks. The band is assigned from the
number of declarations a task’s reference proof needs beyond the released benchmark library. It
estimates the length of a reference proof, not how hard a task is for a human or a model to solve.


    The tasks span a wide range of difficulty. At one end are one-line identities about a Pauli matrix;
at the other are items, often given as exercises to students, whose formalization involves proofs not
only outside the text but also outside Mathlib. For example, Exercise 9.9 asks for a fixed point
of every quantum channel and points the reader to Schauder’s theorem. Neither Schauder’s nor
Brouwer’s theorem is in Mathlib, so the reference proof instead uses the linearity of the channel and
a mean-ergodic averaging argument on the compact convex set of density operators. The task with
the largest reference proof (by declaration count) introduced more than 450 declarations beyond
the benchmark library. We assign each task a proof length estimate from this count, the number
of declarations its reference proof needs beyond the benchmark library, on a five-point scale from
“very small” to “very large” (Table 1).1
    Existing benchmarks for formal proof synthesis (generating the proof code for a formal state-
ment) are drawn primarily from competition mathematics, ranging in size from 488 to 5,560 state-
   1
     This scale measures something different from the difficulty scale of Zhang et al. [49]. Of the five items Lean-QIT-
Bench shares with AxQM, four of them carry that benchmark’s maximum difficulty of 10. On our scale, the same four
fall into “moderate” for Exercise 9.9, “large” for Theorem 9.2 and Theorem 12.9, and “very large” for Theorem 12.1.
Zhang et al. [49] caution that their 1–10 assignments are not objective measurements of proof complexity. Neither
does our scale measure difficulty for a human or LLM to solve the problem.


                                                           3
ments [50–52]. With textbooks as the source material, ProofNet samples 371 statements across
many undergraduate books [53], and TaoBench contains 150 from one analysis textbook by Terence
Tao [54]. Formal Conjectures collects formalized but unproved statements and grows continuously
[55]. SorryDB likewise maintains a live database of unproved sorry goals harvested from 78 public
Lean projects [56], and VeriSoftBench builds repository-scale software-verification tasks [57]. For-
mal benchmarks in physics are still in a nascent stage, at 76 to 250 tasks [13, 49, 58, 59]. Formal
proof translation has also been benchmarked across proof assistants [60]; the physics benchmarks
that ask only for informal reasoning are larger but do not use the kernel checker [61–63]. Our
benchmark, AxQM, differs from these in two ways. It is a census of a single book rather than a
sparse sample drawn across many sources, and its tasks are presented as part of a Lean library
instead of standing alone. Solving the tasks thus requires working within and building on a custom
library of quantum physics outside of an LLM’s training corpus.
    AxQM includes the formal statements of items in the book expressed in a shared foundational
library of quantum physics, on top of a forked version of Mathlib (justified in §3). The fork was
needed because Mathlib’s implementation of multilinear maps is not general enough to express the
inner product on systems composed of several registers. A separate “solution library”, which we
keep private, holds the formal proofs of all benchmark tasks. We take these steps to ensure that
every benchmark task is solvable, each task has a difficulty estimate, and the formal solutions are
not leaked for LLM training [64, 65].
    Grading follows the usual standard of Lean benchmarks: the library compiles, the submitted
proof does not have sorry in its dependencies, and no new axioms are added. As an indication of
scale, the benchmark library adds 3,519 Lean declarations on top of the Mathlib fork, while the
complete library with solutions adds 10,560. The released benchmark keeps only the minimal set
of declarations needed for the tasks to compile, without any of the infrastructure needed to prove
them.
    To further establish confidence in the quantum physics library underlying AxQM, we develop
metrics to clarify how much of the library is reused by multiple items. For example, one could ask
what percentage of the Lean declarations in the dependency closure of a formalized textbook item
are also used by at least one other item. For the median item in the solution library, this number is
84% (Fig. 2). Foundational concepts are also highly reused throughout the library: each of the Pauli
matrices is used by well over a hundred items, as many as 159. While this in no way guarantees
the semantic correctness of the library, the high interdependency between declarations and the
successful formalization of a large number of textbook items across a range of topics constrain the
kinds of errors that can still persist.
    This is also how conventional science is built. A physicist does not re-derive the spectral
theorem or the no-cloning theorem before using them. A result is established once and then relied
on, and its reliability grows with every independent use of it in downstream results, a process
that leaves its trace in the citation record. Our library demonstrates that process explicitly in the
formal relationships between Lean declarations. The declarations with the most dependencies were
introduced early and gathered dependents monotonically without being restated. Critically, our
approach is well designed for textbooks, where this ordering of dependencies is a typical pedagogical
choice.
    This interdependency is also seen between individual items. In the solution library, 387 of the
1,019 tasks were proved by invoking at least one other task. This suggests that the benchmark
can be run under two regimes: the independent regime requires each task to be completed on
its own, and the dependency-order regime requires the prerequisite tasks to be completed first.
We record the empirical proof dependencies between tasks in the published ledger; the aggregate
dependencies between chapters of the book are given in Fig. 3.

                                                 4
               200
                                   median 84%                              pauliX                                   159
               175
                                                                           pauliZ                                 148
               150                                                         pauliY                              133
               125                                                          qubit                             127
       items

                                                                         pauliDot                        95
               100
                                                                       qubitBasis                        95
                75                                                   pauliDot_eq                        92
                50                                    qubitBasis_inner_qubitBasis                  78
                                                               pauliDot_mul_self                   76
                25
                                                                  qubitBasis_vec                  71
                 0
                     0   20   40     60    80   100                                 0        50         100     150
          dependencies shared with another item (%)                                 items depending on the declaration


Figure 2: Shared use of the quantum physics library underlying the benchmark, measured on the
full solution library. Left: for each item, the share of its dependency closure (declaration count)
that at least one other item also depends on; the median item shares 84% of its dependencies with
another item. Right: the ten most depended-upon declarations, by the number of distinct items
whose statements reach them. A definitional error in any of these would have had to survive every
one of those items’ proofs.


    At 1,019 tasks, AxQM is the largest benchmark for formal proof synthesis in physics to date.
Purpose-built proof-synthesis benchmarks in physics have not exceeded 200 tasks [13, 49, 58], while
the largest comparable evaluation set is the 250-instance held-out split of PhysLeanData, a training
corpus harvested from PhysLean [59]. This puts AxQM at 4.1 times the size of PhysLeanData.
Even if one counts individual textbook items, each formalized as one or more tasks, there are still
479. We expect that AxQM, as a formalization of a significant portion of a physics textbook, sets
a baseline for the formalization of a field of physics.
    It is worth contrasting our proof-synthesis benchmark with benchmarks of a different class: a
model is asked to produce a faithful formal statement rather than a proof of one. FormalPhysics has
200 problems, graded by compilation and an LLM judge [66], while QuantumLean-Bench, which
has 931 problems, is only graded by a manual faithfulness rubric that awards credit even when the
Lean code does not compile [67].
    While we are confident in the quality of the benchmark items, we welcome the community’s
thorough review of their physical correctness and faithfulness to the book. This is the failure mode
that matters for a formal benchmark, and recent audits of widely used Lean suites show it is not
rare: a statement can be vacuous, or quietly weaker than the claim in print, and still compile
and still be provable [68]. The Lean kernel is silent on such issues by construction. We give the
structural argument that constrains such errors above (Fig. 2), and record what it does not cover in
§4. Any corrections and improvements will be part of periodic updates to the benchmark following
the initial release. Feedback may be sent by contacting the authors directly or by opening issues
on the benchmark’s GitHub repository.


3    Forking Mathlib
Many proof-synthesis benchmarks take a pinned version of Mathlib as a package dependency
[49, 51, 52, 54, 69]. This allows tasks to be stated and attempted with the full mathemati-
cal machinery provided by Mathlib. As a community-curated library with a stringent review


                                                           5
                                                           2   35

                                                           4   11   46   1              1         5




                          chapter of the dependent task
                                                           5   3    1    10                       2    3

                                                           6   1    4         5

                                                           7   5    15            53

                                                           8   4    1                  14

                                                           9   5    2                   2   19

                                                          10   26   20                  7        61

                                                          11   13                            1         73

                                                          12   26   24   2             10    1    2    111   48

                                                               2    4    5    6    7    8    9   10    11    12
                                                                         chapter of the prerequisite


Figure 3: Direct dependencies between tasks, aggregated by chapter, measured on the full solution
library. For example, there are 15 instances of tasks in chapter 7 directly depending on tasks in
chapter 4. The matrix is close to lower-triangular, which reflects the pedagogical structure of the
book, where later chapters build upon earlier chapters.


process, Mathlib is usually taken as a trusted layer in formalization projects. We should there-
fore justify our choice to base our quantum physics library on an edited version that forked off
leanprover-community/mathlib4 at commit e560e3ad, on Lean toolchain v4.30.0-rc1, and ex-
plain the content of the edits.
    All 24 file changes we made to Mathlib are part of a single refactor. In the official Mathlib,
MultilinearMap is linear over a single ring in each of its arguments. Our fork generalizes it to a
multi-semi-linear map, so that scaling one argument by c scales the value by σ(c), where σ is a
ring homomorphism. The original Mathlib statement is recovered by setting σ to be the identity
homomorphism.
    The generalization is forced by the foundations of finite-dimensional quantum mechanics them-
selves. It is needed to define an inner product on the n-ary tensor product of quantum state spaces,
an inner product that is conjugate-linear in each argument of the left factor (σ being complex conju-
gation). A number of benchmark items concern multi-party registers, which are such tensor powers,
and this refactor enables us to apply Mathlib’s trusted InnerProductSpace machinery to them,
without developing a new API for multi-conjugate-linear maps separate from MultilinearMap.
    This refactor closely follows a precedent Mathlib has already set. LinearMap was generalized
to a semilinear map along an arbitrary ring homomorphism [70], and the inner product on a binary
tensor product was then stated in terms of it. Our change is the n-ary analog of that construction.
As of the writing of this text, the same refactor is an open pull request under review on Mathlib
(#42534). If it is accepted, our benchmark can then be rebased to a newer pinned version of
Mathlib in a future update, removing the need for the fork.




                                                                                  6
4        Failure modes in formalizing physics
In this section, we describe a few failure modes in the formalization of physics and clarify what
kinds of errors can evade a proof assistant’s kernel. Some of these are shared by the formalization
of mathematics [71–73]. The most elementary one is that the formal statement does not mean
what it purports to mean. The statement “one plus one is equal to two” can be formalized as One
+ One = Two, with both One and Two incorrectly defined as the natural number 0. The statement
is nevertheless provable in Lean, but it means something entirely different.
    There is a more subtle manifestation of this error in the formalization of natural language text
that may be more pronounced in physics. We first illustrate it with an elementary example. Suppose
the natural language source text reads, “show that a particle undergoing constant acceleration
starting from rest travels a distance that is quadratic in time.” The following Lean code purports
to formalize and prove this statement:
 def distanceTraveled (a t: R): R:= a * t ^ 2 / 2

 theorem distanceTraveled_eq (a t: R) :
     distanceTraveled a t = a * t ^ 2 / 2 := rfl

    This compiles, contains no sorry, and adds no new axiom. From the standpoint of the Lean
kernel, this is a “correct” formalization. However, its physical content is vacuous: it merely defines
the “distance traveled” to be 12 at2 , and proves that it is equal to 21 at2 by definition. Nevertheless,
in isolation, each declaration can be seen as semantically correct.
    In contrast, a faithful formalization of the natural language statement would have to introduce
the trajectory as a formal object constrained by the physical hypotheses: a function x : R → R
whose second derivative is the constant a, with x(0) = 0 and x′ (0) = 0, and then show that
x(t) = 12 at2 . The difference between this and the vacuous version is the entire content of the
exercise, the integration of the equation of motion, but the gap is invisible to the Lean kernel.
    Physics is more exposed to this than mathematics for a structural reason. Objects in a mathe-
matical text are already mathematical objects, usually with a clear definitional chain back to a set
of canonical and rigorous definitions. Physics texts, however, speak of both the physical objects
and the mathematical objects that model them, often in an interchangeable way. This modeling
step is not something a proof assistant can check, even in principle, and is also one that sometimes
confuses the typical student learning physics.
    While the above error states the conclusion as a definition, a related error moves the conclusion,
or a critical logical step, into the hypotheses of a theorem, which weakens the statement and avoids
proving that step. These kinds of errors can be found in existing proof-synthesis benchmarks for
quantum information theory, Lean-QIT-Bench and Lean-QuantumAlg-Bench, which publish 76
tasks [49].2 We list two of these errors.
    In their task HamiltonianSimulation/FirstOrderLieTrotterGlobalErrorScaling, the in-
formal statement asks for a proof that a function f (m) asymptotically scales as O(1/m). However,
the formal statement in the benchmark is (schematically) “· · · ∀m · · · ∃K · · · f (m) ≤ K/m”. The
ordering of the logical quantifiers means that K is allowed to depend on m, making the statement
trivially true by setting K = mf (m). This is certainly not the intention of the informal statement,
but this error is not caught by the Lean kernel checker.
    Another task, Fourier/QPESuperpositionExactEigenvectors, asks for a proof that phase
estimation, run on the superposition α|u1 ⟩ + β|u2 ⟩ of two eigenvectors, produces α|N ϕ1 ⟩|u1 ⟩ +
    2
        QudeLeap/Lean-QuantumAlg-Bench at b540e86 and QuAIR/Lean-QIT-Bench at 231830d, both 2026-08-15.



                                                        7
β|N ϕ2 ⟩|u2 ⟩. However, the phase estimation circuit is never constructed or referred to in the for-
mal statement. Instead, the circuit’s action on an arbitrary eigenvector is taken as a hypothesis,
bypassing the algorithm entirely. The task is therefore solved trivially by linearity. This semantic
deficiency again evades the Lean kernel.
    We have taken care to minimize these types of defects in AxQM, but a thorough evaluation can
only be done by relying on a larger effort beyond the authors. We invite the community of physicists
and Lean experts to inspect and review the content of AxQM, with any resulting improvements
included in future updates to the benchmark.


5    Discussion
While physics heavily invokes and relies on mathematical reasoning, it is reasonable to ask to
what extent physical reasoning as a whole could be formalized. Douglas [74] points out that in
mathematical physics, a rigorous statement and proof already exist, and thus their formalization
may proceed exactly as in mathematics proper. Much of theoretical physics, however, is not of
this kind, with results often justified by arguments that a community trusts without a rigorous
statement or proof (such as perturbative quantum field theory via path integrals). Douglas’s
response is to extract the rigorous parts of the physical reasoning as explicit mathematical premises
and consequences, so that physics enters only through typed hypotheses and a dictionary between
physical quantities and mathematical objects.
    An example of this split is conventional (BCS) superconductivity. The theory assumes an
effective attraction between electrons and restricts the many-body problem to mean-field states.
From the resulting BCS functional onward, all further steps can be derived with mathematical
rigor: the gap equation, the energy gap and the transition temperature [75, 76]. The first two steps
are physical assumptions: the attraction is an effective interaction obtained from a well-established
but not mathematically rigorous calculation, and the mean-field restriction is an approximation
which is only partially justified [77]. In Douglas’ terms, those two steps are the typed hypotheses,
and the identification of the measured gap with the order parameter of the functional is a dictionary
entry.
    AxQM applies the same split to a physics textbook. The postulates of quantum mechanics enter
the library as its primitives, and each formal statement is a dictionary entry that ties a claim in the
textbook to a mathematical object. The kernel checks every proof from there on. The dictionary is
also where an error can enter. Tooby-Smith [15] states that an interactive theorem prover verifies
logical consistency but cannot prevent a physically meaningless starting point, so whether each
formal statement is faithful to the textbook rests on an expert’s review, and the kernel does not
check it (§4).
    The first decision is therefore which parts of the textbook can be dictionary entries at all. Those
are entries that are expressed, or expressible, as rigorous mathematical statements. Out of the 687
items extracted from the textbook, 505 are formalized; the other items (essay prompts, graph
plotting, intuitive arguments, numerical computation, research problems, and infinite-dimensional
quantum mechanics statements) are excluded. Out of the formalized items, 479 have tasks in this
benchmark. The remaining 26 items were excluded for one of five reasons: the item is an existing
theorem in upstream Mathlib, its proof is needed for the statement of another task to compile, it
is a definition with no proof to synthesize, it duplicates another item, or we removed it manually
for quality. AxQM and its solution library are therefore not a complete formalization of every
physically meaningful statement in the textbook. Such a formalization is out of reach in principle,
since the items excluded first are not mathematical statements, and we narrowed it further in


                                                  8
practice by the five conditions above. AxQM is nonetheless the first textbook-scale formalization
of physics (§2 compares its size with other proof-synthesis benchmarks in physics).
    We intend for AxQM to serve as a baseline for the evaluation of proof synthesis in physics. We
chose Nielsen and Chuang [48] as the source text because of the textbook’s foundational status in
the field of quantum information and quantum computing. As a pedagogical book, it naturally
includes many problems which could be considered “easy” for a state-of-the-art LLM. We also
include these problems in the benchmark, so that the benchmark score is an accurate measure of
the model’s ability to complete a course based on this textbook.


6    Data and code availability
AxQM is published as a GitHub repository at https://github.com/Axiomatic-AI/AxQM under
the Apache 2.0 license. The repository contains the task statements, the finite-dimensional quantum
mechanics library, the Mathlib fork (branched from leanprover-community/mathlib4 at commit
e560e3ad, Lean toolchain v4.30.0-rc1), the per-task proof length estimates, the task-dependency
ledger, and the grading and submission scripts. The solution library, containing reference proofs of
all 1,019 tasks, is withheld to keep the solutions out of model training corpora. An overview of the
benchmark structure and instructions for running and grading it are included in the repository.
    Comments and error reports may be submitted as issues on the GitHub repository. Inquiries
and benchmark submissions may be sent to the authors by email.


Acknowledgments
We thank Luigi Massacci, Michail Karatarakis and Victor Galitski for their critical inspection of
the code and for checking the faithfulness of formal statements to the textbook.


Author contributions
W.W.Y. produced the foundational library of quantum physics on which the benchmark is built,
contributed to the development and testing of the agentic autoformalization pipeline which aided
in the construction of the benchmark, performed the quality check and preparations for the bench-
mark’s release, and produced the figures. J.M.T. reviewed the benchmark code and checked formal
statements against the textbook for faithfulness. D.R.E. proposed and carried out initial work on
agentic formalization grounded in the axioms of quantum mechanics, and its specialization to quan-
tum information and to Nielsen and Chuang in particular, including the restriction of the library
to finite-dimensional Hilbert spaces. F.H.L.K. built the first agentic harness for autonomous for-
malization of the Nielsen and Chuang textbook, produced the prototype of the foundational library
of quantum physics grounded in the axioms of quantum mechanics, and, with W.W.Y., developed
the harness that built the library at scale. All authors discussed the results and contributed to the
manuscript.


Competing interests
W.W.Y., D.R.E. and J.M.T. are affiliated with Axiomatic AI, and F.H.L.K. is a co-founder of
Axiomatic AI.



                                                 9
References
 [1] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In Automated Deduction (CADE-28), volume 12699 of Lecture Notes in Computer
     Science, pages 625–635, 2021. doi: 10.1007/978-3-030-79876-5_37.

 [2] Fabian Gloeckle, Ahmad Rammal, Charles Arnal, Remi Munos, Vivien Cabannes, Gabriel
     Synnaeve, and Amaury Hayat. Automatic textbook formalization, 2026. arXiv:2604.03071.

 [3] Zichen Wang, Wanli Ma, Zhenyu Ming, Gong Zhang, Kun Yuan, and Zaiwen Wen. M2F:
     Automated formalization of mathematical literature at scale, 2026. arXiv:2602.17016.

 [4] Ahmad Rammal, Niket Patel, Fabian Gloeckle, Amaury Hayat, Julia Kempe, Remi
     Munos, Charles Arnal, and Vivien Cabannes. Formalizing mathematics at scale, 2026.
     arXiv:2605.29955.

 [5] Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
     Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F.
     Wu, Fuli Luo, and Chong Ruan. DeepSeek-prover-v1.5: Harnessing proof assistant feedback for
     reinforcement learning and monte-carlo tree search. In International Conference on Learning
     Representations (ICLR 2025), 2025. arXiv:2408.08152.

 [6] Haiming Wang et al. Kimina-Prover Preview: Towards large formal reasoning models with
     reinforcement learning, 2025. arXiv:2504.11354.

 [7] Luoxin Chen et al. Seed-Prover: Deep and broad reasoning for automated theorem proving,
     2025. arXiv:2507.23726.

 [8] Tudor Achim et al. Aristotle: IMO-level automated theorem proving, 2025. arXiv:2510.01346.

 [9] Yong Lin et al. Goedel-Prover-V2: Scaling formal theorem proving with scaffolded data syn-
     thesis and self-correction, 2025. arXiv:2508.03613.

[10] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser,
     Aja Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, Ottavia Bertolli, Tom
     Zahavy, Amol Mandhane, Jessica Yung, Iuliya Beloshapka, Borja Ibarz, Vivek Veeriah, Lei
     Yu, Oliver Nash, Paul Lezeau, Salvatore Mercuri, Calle Sönne, Bhavik Mehta, Alex Davies,
     Daniel Zheng, Fabian Pedregosa, Yin Li, Ingrid von Glehn, Mark Rowland, Samuel Albanie,
     Ameya Velingker, Simon Schmitt, Edward Lockhart, Edward Hughes, Henryk Michalewski,
     Nicolas Sonnerat, Demis Hassabis, Pushmeet Kohli, and David Silver. Olympiad-level formal
     mathematical reasoning with reinforcement learning. Nature, 651:607–613, 2025. doi: 10.1038/
     s41586-025-09833-y.

[11] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-
     augmented language models. In Advances in Neural Information Processing Systems 36
     (NeurIPS 2023), Datasets and Benchmarks Track, 2023. doi: 10.52202/075280-0944.

[12] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models
     as copilots for theorem proving in Lean, 2024. arXiv:2404.12534.




                                               10
[13] Benjamin Breen, Marco Del Tredici, Jacob McCarran, Javier Aspuru Mijares, Weichen Win-
     ston Yin, Kfir Sulimany, Jacob M. Taylor, Frank H. L. Koppens, and Dirk Englund.
     Ax-prover: A deep reasoning agentic framework for theorem proving in mathematics and
     quantum physics. Machine Learning: Science and Technology, 7(4):045073, 2026. doi:
     10.1088/2632-2153/ae9452.

[14] Borja Requena, Austin Letson, Krystian Nowakowski, Izan Beltran-Ferreiro, and Leopoldo
     Sarra. A minimal agent for automated theorem proving. In International Conference on
     Machine Learning (ICML 2026), 2026. arXiv:2602.24273.

[15] Joseph Tooby-Smith. A perspective on interactive theorem provers in physics. Advanced
     Science, page e17294, 2025. doi: 10.1002/advs.202517294.

[16] Joseph Tooby-Smith. Formalizing the stability of the two Higgs doublet model potential into
     Lean: identifying an error in the literature, 2026. arXiv:2603.08139.

[17] Uri Kol, Maor Ben-Shahar, Kfir Sulimany, and Dirk Englund. A machine-verified proof of a
     quantum-optimization conjecture, 2026. arXiv:2606.29687.

[18] The mathlib Community. The Lean mathematical library. In Certified Programs and Proofs
     (CPP 2020), pages 367–381, 2020. doi: 10.1145/3372885.3373824.

[19] Joseph Tooby-Smith. HepLean: Digitalising high energy physics. Computer Physics Commu-
     nications, 308:109457, 2025. doi: 10.1016/j.cpc.2024.109457.

[20] Joseph Tooby-Smith.       Formalization of physics index notation in Lean 4, 2024.
     arXiv:2411.07667.

[21] Joseph Tooby-Smith. Digitalizing Wick’s theorem, 2025. arXiv:2505.07939.

[22] Michael R. Douglas, Sarah Hoback, Anna Mei, and Ron Nissim. Formalization of QFT, 2026.
     arXiv:2603.15770.

[23] Maxwell P. Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong Dang, Catherine M.
     Wraback, and Tyler R. Josephson. Formalizing chemical physics using the Lean theorem
     prover. Digital Discovery, 3(2):264–280, 2024. doi: 10.1039/D3DD00077J.

[24] Joseph K. Miller. A formalization of the mean-field derivation of the Vlasov equation, 2026.
     arXiv:2607.08986.

[25] Moritz Doll and Iman Shames. Foundations of machine-checked control theory in Lean, 2026.
     arXiv:2607.19727.

[26] Mohit Tekriwal, Karthik Duraisamy, and Jean-Baptiste Jeannin. A formal proof of the Lax
     equivalence theorem for finite difference schemes. In NASA Formal Methods (NFM 2021),
     volume 12673 of Lecture Notes in Computer Science, pages 322–339. Springer, 2021. doi:
     10.1007/978-3-030-76384-8_20.

[27] Cameron Khanpour and Samuel Talkington. Proving the limits of quantum power flow, 2026.
     arXiv:2607.19263.

[28] Sven Krippendorf and Joseph Tooby-Smith. Physics as code: From scans to theorems with
     ITP APIs in SU(5) model building, 2026. arXiv:2603.28406.

                                               11
[29] Jonathan Julián Huerta y Munive, Simon Foster, Mario Gleirscher, Georg Struth, Chris-
     tian Pardillo Laursen, and Thomas Hickman. IsaVODEs: Interactive verification of cyber-
     physical systems at scale. Journal of Automated Reasoning, 68(4):21, 2024. doi: 10.1007/
     s10817-024-09709-2.

[30] Chengkai Zhu, Ziao Tang, Guocheng Zhen, Yimeng Cao, Yusheng Zhao, Ranyiliu Chen, Xu-
     anqiang Zhao, Lei Zhang, and Xin Wang. Lean-QIT: Towards a formal infrastructure for
     quantum information theory, 2026. arXiv:2607.09632.

[31] Kazumi Kasaura, Kei Tsukamoto, Kento Mori, Risa Mizuno, Takahiro Namatame, Yuta Ori-
     ike, Masaya Taniguchi, Sho Sonoda, and Hayata Yamasaki. Lean-Quantum: Toward AI-
     assisted formalization of quantum information, 2026. arXiv:2607.05492.

[32] Alex Meiburg.    Lean-quantuminfo.     https://github.com/Timeroot/Lean-QuantumInfo,
     2025.

[33] Alex Meiburg, Leonardo A. Lessa, and Rodolfo R. Soldati. A formalization of the generalized
     quantum Stein’s lemma in Lean, 2025. arXiv:2510.08672.

[34] Yuxiang Peng, Kesha Hietala, Runzhou Tao, Liyi Li, Robert Rand, Michael Hicks, and
     Xiaodi Wu. A formally certified end-to-end implementation of Shor’s factorization algo-
     rithm. Proceedings of the National Academy of Sciences, 120(21):e2218775120, 2023. doi:
     10.1073/pnas.2218775120.

[35] Lei Zhang, Yusheng Zhao, Hongshun Yao, and Xin Wang. Building Shor’s algorithm in Lean:
     An agentic formalization of quantum attacks on RSA-2048 and P-256, 2026. arXiv:2607.14082.

[36] Tianrun Zhao and Nengkun Yu. Formalizing CHSH rigidity in Lean 4, 2026. arXiv:2604.03884.

[37] Mattias Ehatamm, Yi Lee, Xiaodi Wu, and Runzhou Tao. End-to-end formalization of quan-
     tum error correction, 2026. arXiv:2605.16523.

[38] Sirui Lu, Erickson Tjoa, and J. Ignacio Cirac. Multi-agent autoformalization of tensor network
     theory, 2026. arXiv:2607.07857.

[39] Mingrui Jing, Lei Zhang, Yusheng Zhao, Hongshun Yao, and Xin Wang. An agentic formal-
     ization for certified quantum neural network design, 2026. arXiv:2607.12981.

[40] Yuanjie Ren, Jinzheng Li, and Yidi Qi. MerLean: An agentic framework for autoformalization
     in quantum computation, 2026. arXiv:2602.16554.

[41] Jaap Boender, Florian Kammüller, and Rajagopal Nagarajan. Formalization of quantum pro-
     tocols using Coq. Electronic Proceedings in Theoretical Computer Science (EPTCS), 195:
     71–83, 2015. doi: 10.4204/EPTCS.195.6. Proceedings of the 12th International Workshop on
     Quantum Physics and Logic (QPL 2015).

[42] Jennifer Paykin, Robert Rand, and Steve Zdancewic. QWIRE: a core language for quantum
     circuits. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming
     Languages, 2017. doi: 10.1145/3009837.3009894.

[43] Kesha Hietala, Robert Rand, Shih-Han Hung, Xiaodi Wu, and Michael Hicks. A verified
     optimizer for quantum circuits. Proceedings of the ACM on Programming Languages, 5(POPL):
     1–29, 2021. doi: 10.1145/3434318.

                                                12
[44] Li Zhou, Gilles Barthe, Pierre-Yves Strub, Junyi Liu, and Mingsheng Ying. CoqQ: Founda-
     tional verification of quantum programs. Proceedings of the ACM on Programming Languages,
     7(POPL):833–865, 2023. doi: 10.1145/3571222.

[45] Anthony Bordg, Hanna Lachnitt, and Yijun He. Certified quantum computation in Is-
     abelle/HOL.    Journal of Automated Reasoning, 65(5):691–709, 2021. doi: 10.1007/
     s10817-020-09584-7.

[46] Anthony Bordg, Hanna Lachnitt, and Yijun He. Isabelle marries Dirac: a library for quantum
     computation and quantum information. Archive of Formal Proofs, 2020. URL https://
     isa-afp.org/entries/Isabelle_Marries_Dirac.html.

[47] Mnacho Echenim and Mehdi Mhalla. A formalization of the CHSH inequality and Tsirelson’s
     upper-bound in Isabelle/HOL. Journal of Automated Reasoning, 68(1):2, 2023. doi: 10.1007/
     s10817-023-09689-9.

[48] Michael A. Nielsen and Isaac L. Chuang. Quantum Computation and Quantum Information.
     Cambridge University Press, 10th anniversary edition, 2010. doi: 10.1017/CBO9780511976667.

[49] Lei Zhang, Yusheng Zhao, Yimeng Cao, Ranyiliu Chen, Mingrui Jing, Jizhe Lai, Ziao Tang,
     Jingu Xie, Hongshun Yao, Xuanqiang Zhao, Guocheng Zhen, Chengkai Zhu, and Xin Wang.
     Benchmarking agents for proving theorems in quantum algorithms and quantum information,
     2026. arXiv:2607.21533.

[50] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. miniF2F: A cross-system benchmark for
     formal Olympiad-level mathematics. In International Conference on Learning Representations
     (ICLR 2022), 2022. arXiv:2109.00110.

[51] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating neural theorem-provers
     on the Putnam mathematical competition. In Advances in Neural Information Processing Sys-
     tems 37 (NeurIPS 2024), Datasets and Benchmarks Track, 2024. doi: 10.52202/079017-0368.

[52] Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan
     Zhang, Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang
     Liu. FormalMATH: Benchmarking formal mathematical reasoning of large language models,
     2025. arXiv:2505.02735.

[53] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir
     Radev, and Jeremy Avigad. ProofNet: Autoformalizing and formally proving undergraduate-
     level mathematics, 2023. arXiv:2302.12433.

[54] Alexander K. Taylor, Junyi Zhang, Ethan Ji, Vigyan Sahai, Haikang Deng, Yuanzhou Chen,
     Yifan Yuan, Di Wu, Jia-Chen Gu, Kai-Wei Chang, Nanyun Peng, Amit Sahai, and Wei
     Wang. TaoBench: Do automated theorem prover LLMs generalize beyond MathLib?, 2026.
     arXiv:2603.12744.

[55] Moritz Firsching, Paul Lezeau, Salvatore Mercuri, Miklós Z. Horváth, Yaël Dillies, Calle Sönne,
     Eric Wieser, Fred Zhang, Thomas Hubert, Blaise Agüera y Arcas, and Pushmeet Kohli. Formal
     conjectures: An open and evolving benchmark for verified discovery in mathematics, 2026.
     arXiv:2605.13171.


                                                13
[56] Austin Letson, Leopoldo Sarra, Auguste Poiroux, Oliver Dressler, Paul Lezeau, Dhyan Aranha,
     Frederick Pu, Aaron Hill, Miguel Corredera Hidalgo, Julian Berman, George Tsoukalas, and
     Lenny Taelman. SorryDB: Can AI provers complete real-world Lean theorems? In Interna-
     tional Conference on Machine Learning (ICML 2026), 2026. arXiv:2603.02668.

[57] Yutong Xin, Qiaochu Chen, Greg Durrett, and Işil Dillig. VeriSoftBench: Repository-scale
     formal verification benchmarks for Lean, 2026. arXiv:2602.18307.

[58] Yuxin Li, Minghao Liu, Ruida Wang, WenZhao Ji, Zhitao He, Rui Pan, Junming Huang, Tong
     Zhang, and Yi R. Fung. Lean4Physics: Comprehensive reasoning framework for college-level
     physics in Lean4, 2025. arXiv:2510.26094.

[59] Hanning Zhang, Ruida Wang, Rui Pan, Wenyuan Wang, Bingxu Meng, and Tong Zhang.
     PhysProver: Advancing automatic theorem proving for physics, 2026. arXiv:2601.15737.

[60] Jiayi Wu, Robert Joseph George, and Anima Anandkumar. ITPEval: Benchmarking formal
     translation across interactive theorem provers, 2026. arXiv:2607.19407.

[61] Daniel J. H. Chung et al. Theoretical physics benchmark (TPBench): a dataset and study of
     AI reasoning capabilities in theoretical physics. Machine Learning: Science and Technology, 6
     (3):030505, 2025. doi: 10.1088/2632-2153/adfcb0.

[62] Shi Qiu et al. PHYBench: Holistic evaluation of physical perception and reasoning in large
     language models, 2025. arXiv:2504.16074.

[63] Xin Xu et al. UGPhysics: A comprehensive benchmark for undergraduate physics reasoning
     with large language models, 2025. arXiv:2502.00334.

[64] Alon Jacovi, Avi Caciularu, Omer Goldman, and Yoav Goldberg. Stop uploading test data in
     plain text: Practical strategies for mitigating data contamination by evaluation benchmarks.
     In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing,
     pages 5075–5084, 2023. doi: 10.18653/v1/2023.emnlp-main.308.

[65] Simone Balloccu, Patrícia Schmidtová, Mateusz Lango, and Ondřej Dušek. Leak, cheat, repeat:
     Data contamination and evaluation malpractices in closed-source LLMs. In Proceedings of the
     18th Conference of the European Chapter of the Association for Computational Linguistics,
     pages 67–93, 2024. doi: 10.18653/v1/2024.eacl-long.5.

[66] Jordan Meadows, Lan Zhang, and Andre Freitas. FormalScience: Scalable human-in-the-loop
     autoformalisation of science with agentic code generation in Lean. In Proceedings of the 64th
     Annual Meeting of the Association for Computational Linguistics (ACL 2026), Volume 1: Long
     Papers, 2026. URL https://aclanthology.org/2026.acl-long.1057/.

[67] Isha Goswami, Anushka Paulchoudhury, Robert Joseph George, and Anima Anandkumar.
     QuantumLean-Bench: A unified benchmark for informal and formal quantum reasoning. In
     ICML Workshop on AI for Physics (AI4Physics), 2026. OpenReview:K9bHv3Y3Uf.

[68] Pawan Sasanka Ammanamanchi, Siddharth Bhat, and Stella Biderman. Faults in our formal
     benchmarking: Dataset defects and evaluation failures in Lean theorem proving. In Interna-
     tional Conference on Machine Learning (ICML 2026), 2026. arXiv:2606.29493.




                                               14
[69] Jiewen Hu, Thomas Zhu, and Sean Welleck. miniCTX: Neural theorem proving with (long-
     )contexts. In International Conference on Learning Representations (ICLR 2025), 2025.
     arXiv:2408.03350.

[70] Frédéric Dupuis, Robert Y. Lewis, and Heather Macbeth. Formalized functional analysis with
     semilinear maps. In 13th International Conference on Interactive Theorem Proving (ITP 2022),
     volume 237 of LIPIcs, pages 10:1–10:19. Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
     2022. doi: 10.4230/LIPIcs.ITP.2022.10.

[71] Theodore Meek, Siyuan Ge, Di Qiu Xiang, Simon Chess, and Vasily Ilin. Formalizing
     numerical analysis: An agent pipeline and quality audit beyond kernel acceptance, 2026.
     arXiv:2606.14000.

[72] Noor Islam S. Mohammad and Tamim Sheikh. The faithfulness gap: Certifying semantic equiv-
     alence between natural-language and formal mathematical statements, 2026. arXiv:2606.16541.

[73] Tanya Klowden and Terence Tao. Mathematical methods and human thought in the age of
     AI, 2026. arXiv:2603.26524.

[74] Michael R. Douglas. Axioms for physical reasoning: Codifying the Seiberg–Witten solution in
     Lean, 2026. arXiv:2607.06379; working paper.

[75] Christian Hainzl, Eman Hamza, Robert Seiringer, and Jan Philip Solovej. The BCS functional
     for general pair interactions. Communications in Mathematical Physics, 281:349–367, 2008.
     doi: 10.1007/s00220-008-0489-2.

[76] Rupert L. Frank, Christian Hainzl, Robert Seiringer, and Jan Philip Solovej. Microscopic
     derivation of Ginzburg–Landau theory. Journal of the American Mathematical Society, 25:
     667–713, 2012. doi: 10.1090/s0894-0347-2012-00735-8.

[77] Gerhard Bräunlich, Christian Hainzl, and Robert Seiringer. Translation-invariant quasi-free
     states for fermionic systems and the BCS approximation. Reviews in Mathematical Physics,
     26(7):1450012, 2014. doi: 10.1142/S0129055X14500123.




                                               15
