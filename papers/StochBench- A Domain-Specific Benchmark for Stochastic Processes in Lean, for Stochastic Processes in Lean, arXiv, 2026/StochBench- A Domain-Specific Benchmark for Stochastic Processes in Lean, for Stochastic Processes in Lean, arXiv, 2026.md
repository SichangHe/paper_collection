                                               S TOCH B ENCH: A Domain-Specific Benchmark
                                                      for Stochastic Processes in Lean


                                                    Idan Davidovich  Debargha Ganguly Vikash Singh Vipin Chaudhary
                                                                       Case Western Reserve University
                                                               {idan, debargha, vikash, vipin}@case.edu
                                                       https://huggingface.co/datasets/IdanDavidovich/StochBench
arXiv:2609.09264v1 [cs.CL] 8 Sep 2026




                                                                                        Abstract
                                                    Leading benchmarks for formal theorem proving with large language models are
                                                    small collections drawn from competition math, such as the IMO and Putnam,
                                                    that poorly represent field-specific applications. We introduce S TOCH B ENCH,
                                                    a Lean 4 benchmark of 450 graduate stochastic-processes problems at varying
                                                    abstraction levels, each paired with its natural-language source. Addressing a field
                                                    underrepresented in Mathlib, it covers finite and countable Markov chains, renewal
                                                    processes, random walks, martingales, stopping times, queues, Brownian motion,
                                                    stochastic calculus, weak convergence, and Poisson and continuous-time Markov
                                                    processes. Our Opus 4.8-based agent achieves a 34.9% proof rate (157/450) under
                                                    a 15-minute per-problem limit. S TOCH B ENCH better represents domain-specific
                                                    applied mathematics while remaining challenging for advanced provers.


                                        1    Introduction
                                        Lean enables machine-checkable mathematics, with substantial formalizations including sphere
                                        packing in dimension eight, Brownian motion, and Fermat’s Last Theorem for regular primes
                                        [Hariharan et al., 2026, Degenne et al., 2025, Best et al., 2025]. Extending this progress to everyday
                                        mathematical assistance requires evaluating how consistently automated provers handle a discipline’s
                                        recurring arguments. Competition benchmarks and broad textbook collections offer valuable tests, but
                                        aggregate scores can obscure domain-specific strengths and failures [Zheng et al., 2021, Azerbayev
                                        et al., 2023, Tsoukalas et al., 2024].
                                        We introduce S TOCH B ENCH, a Lean 4 benchmark for graduate stochastic processes, a field central to
                                        statistics and machine learning. Concentrating on related problems in Markov chains, martingales,
                                        and continuous-time processes, we prioritize within-domain depth over cross-domain breadth. Some
                                        problems, however, require infrastructure unavailable in the Mathlib environment [The mathlib
                                        Community, 2026]. Direct targets use Mathlib or shared definitions, while abstracted targets take
                                        the required properties as hypotheses. Lean verifies that each proved conclusion follows from its
                                        stated hypotheses. We have taken utmost care to make sure the (all human written) definitions and
                                        hypotheses faithfully represent the source problem, but can benefit from further peer review.
                                        Our contributions are:
                                               1. A domain-focused benchmark. We release 450 Lean 4 theorem targets paired with informal
                                                  statements, alongside shared definitions and baseline proof attempts.
                                               2. A scope-aware baseline evaluation. We annotate formalization scope and evaluate a
                                                  compiler-guided proof agent under a 15-minute per-problem cap, reporting results by topic
                                                  and representation.

                                        Preprint.
    1   Sources
         textbook           p                    τ                                                                             λ                     Xₙ ⇒ X
                        0       1   2                               X₂                                                     0       1   2
                                                               X₁        X₃
         course notes       q
                                        n
                                                                                                                               μ
                                                                                                                                           t



                        DTMC                Martingales       Renewal               Random walk   Brownian   Poisson       CTMC                    Weak conv.
         original
                            96                 94                   41                   62          45           40           55                       17

                                               Mathematician Driven

    2   Curation                                 3   Formalization                                                     4       Benchmark                 n = 450

                                                                         Claude
                                                                         Opus 4.8                                      25.3%
                                                                                                                                       114 direct

                                                                         theorem optional_stopping                                     Mathlib objects
                            off-topic            Stochastic               (hX : Martingale X ℱ μ)
                                                 Stationary

        GIVEN
                                                 TVDist
                                                 Miixing …
                                                                          (hτ : IsStoppingTime ℱ τ)                    74.7%           336 abstracted
                                                                          (hN : ∀ ω, τ ω ≤ N) :
                                                                                                                                               h

                                                Shared                    μ[ stoppedValue X τ] = μ[ X 0 ] := by
        SHOW                                    Definitions              sorry
                                                                                                                                       Explicit hypotheses




Figure 1: Construction of S TOCH B ENCH: mathematician-led curation and LLM-assisted formaliza-
tion with shared definitions produce 450 Lean 4 targets across eight topics, comprising 114 direct
and 336 abstracted statements.


2       Related Work
Benchmarks for formal mathematical reasoning. Lean-based evaluation has developed along
complementary axes of competition difficulty, curricular coverage, and research context. MINI F2F
[Zheng et al., 2021] established a benchmark centered on Olympiad-style mathematics, P ROOF N ET
[Azerbayev et al., 2023] paired informal statements and proofs with formal undergraduate theorem
statements, and P UTNAM B ENCH [Tsoukalas et al., 2024] extended competition-based evaluation
to challenging undergraduate problems. F ORMAL MATH [Yu et al., 2025] expanded the scale and
disciplinary coverage of Lean 4 benchmarks, while F ORMAL P ROOF B ENCH [Ravi et al., 2026]
targeted advanced undergraduate and graduate problems from textbooks and qualifying examinations.
Moving toward mathematical practice, RLME VAL [Poiroux et al., 2025] evaluates theorems from
research-level Lean formalization projects, and F ORMAL ML [Yang et al., 2025] studies subgoal
completion in machine-learning theory, including optimization and probability inequalities.
Proof automation, representation, and semantic faithfulness. Lean 4 [Moura and Ullrich, 2021]
and Mathlib [The mathlib Community, 2020] provide an extensible proof environment and reusable
mathematical abstractions for automated reasoning. L EAN D OJO [Yang et al., 2023] combines
programmatic proof interaction with retrieval-augmented premise selection, while L EAN C OPILOT
[Song et al., 2024] integrates tactic suggestion and proof search into interactive formalization.
L EAN -STA R [Lin et al., 2024] interleaves informal reasoning with tactic generation; D EEP S EEK -
P ROVER -V1.5 [Xin et al., 2024] combines proof-assistant feedback with reinforcement learning and
tree search; and D EEP S EEK -P ROVER -V2 [Ren et al., 2025] develops reinforcement learning around
subgoal decomposition. These advances address proof construction, but successful checking alone
does not establish correspondence with an intended informal claim. F ORMAL A LIGN [Lu et al., 2024]
explicitly evaluates informal–formal semantic alignment, while M ATH ATLAS [Patel et al., 2026]
examines graduate-level autoformalization with definitions and dependency structure. TAO B ENCH
[Taylor et al., 2026] isolates a related representation issue through paired, mathematically equivalent
statements expressed using bespoke and Mathlib definitions.
Formal probability and stochastic-process infrastructure. Substantial Lean developments already
support the mathematics underlying S TOCH B ENCH. Ying and Degenne [2022] formalize Doob’s mar-
tingale convergence theorems together with conditional expectation, stopping times, and martingale
theory; Marion [2025] constructs trajectory-space probability measures through the Ionescu–Tulcea
theorem, and Degenne [2025] develops Markov kernels and disintegration. Degenne et al. [2025]
formalize Brownian motion and its extension and path-continuity machinery, while Coelho [2026a]
develops the L2 Itô integral and Itô’s formula for C 3 functions with bounded derivatives. Comple-
mentary work connects textbook probability to Mathlib interfaces [Deng and Shum, 2026], verifies
                                                                                     2
reinforcement-learning convergence [Zhang, 2025], and constructs a mathematical-finance library
with explicit faithfulness auditing [Coelho, 2026b].

3   The S TOCH B ENCH Benchmark
Sources and selection. S TOCH B ENCH contains 450 Lean 4 theorem targets in graduate stochastic
processes. We combine problems written for the benchmark with exercises, lemmas, theorems, and
corollaries selected from Probability, Mathematical Statistics, and Stochastic Processes [Siegrist,
2022] and the MIT course notes and assignments for Introduction to Stochastic Processes [Wu, 2015],
Advanced Stochastic Processes [Gamarnik, 2013], and Discrete Stochastic Processes [Gallager,
2011]. We selected problems for their relevance to stochastic processes and wrote them as claims
with hypotheses. Statements that are closer to general probability theory, such as “show that the total
variation distance satisfies triangle inequality : ||µ − ν||T V ≤ ||µ − η||T V + ||η − ν||T V ”, were not
included. The corpus covers eight topics, summarized in Table 1(a).

Statement construction. All benchmark-specific definitions, hypotheses and questions are human-
written. An Opus 4.8-based formalizer assisted with expressing the problems as Lean theorem
statements. We revised candidate statements using Lean feedback until they elaborated in Lean 4.30.0
with a fixed Mathlib version. Elaboration checks that a statement is well-typed. We consider the task
to prove the theorem with established correspondence with the source problem. On the off chance
that a formalization error has crept in, we also accept a kernel-checked proof of the theorem being
incorrect.

Shared mathematical definitions. We build shared abstractions and definitions for recurring
concepts. Finite-state chains use a common matrix representation for stochasticity, stationarity, irre-
ducibility, aperiodicity, eventual positivity of transition powers, detailed balance, time reversal, and
total-variation distance. IsHittingSolution and returnTime express first-step equations, while
nstep defines transition powers through infinite sums for countable-state formulations. Other defini-
tions connect the targets to Mathlib: natStop converts natural-valued stopping times to WithTop,
runningMax expresses finite running maxima, and IsConstDrift states conditional increment
identities. Reusing these definitions gives related targets a common mathematical representation.

Marginals and joint process laws. We distinguish the distribution of a process at one time from its
joint behavior over time. HasMatrixMarginals relates the distribution of Xn to the corresponding
row of P n . HasChainLaw instead specifies finite-dimensional probabilities through
                                                                  n−1
                                                                  Y
                       Pµ (X0 = x0 , . . . , Xn = xn ) = ν(x0 )         P (xi , xi+1 ).
                                                                  i=0
The coupling-bound target combines matrix marginals with an explicit condition that the processes
agree after the meeting time. The strong-stationary-time target uses the joint law and stopping-time
conditions to relate the state at the stopping time to the state at a later deterministic time. These
representations specify which information about the process is available to the prover.
Formalization scope. Some problems require infrastructure unavailable in the Mathlib environ-
ment. Direct targets use Mathlib objects or shared definitions, while abstracted targets take the
required properties as hypotheses. The JSON records these labels as literal and abstract, respec-
tively. The supplied properties may define an object or provide intermediate results from the source
problem. These are different choices: specifying Brownian-motion properties does not assume a
quadratic-variation conclusion, whereas assuming memorylessness removes the need to derive it from
continuous-time chain dynamics. Likewise, a hitting-time target stated through first-step equations
need not establish that their solution equals a pathwise expected hitting time.
Path properties and convergence. The targets state the required form of convergence explicitly.
Brownian-motion properties are expressed through Gaussian increment laws, independence, and
almost-sure path continuity; several targets package these properties in a local IsBM definition. The
quadratic-variation target asks for convergence of the mean-square error as the partition mesh tends
to zero. The Donsker target asks for convergence of expectations for every bounded continuous
functional on C([0, T ], R), rather than only convergence at individual times. A separate target asks
for existence and uniqueness of Wiener measure on continuous path space.


                                                   3
                                              (a) Corpus composition                (b) Baseline
                                                                               Clean proofs
Topic                                       Direct Abstracted Items    Direct Abstracted Total Rate (%)
Poisson processes                               5           35    40       0            7       7   17.5
Markov chains (finite & countable)             23           73    96      15           22      37   38.5
Renewal processes                               0           41    41       0            2       2    4.9
Continuous-time Markov & queues                 1           54    55       1           22      23   41.8
Random walks & large deviations                 9           53    62       6           10      16   25.8
Martingales & stopping                         67           27    94      51            7      58   61.7
Brownian motion & stochastic calculus           0           45    45       0            8       8   17.8
Weak convergence & functional limits            9            8    17       6            0       6   35.3
All                                           114          336   450      79           78     157   34.9
(c) Clean-proof rates by target class (%)                               69.3          23.2


Table 1: Corpus composition and baseline results for S TOCH B ENCH (recorded proving time at most
15 minutes). Only proofs with recorded proving times of at most 900 seconds are counted. Topic rates
use all items in the topic; class rates use all items in the class. The class comparison is descriptive,
not a controlled causal effect.



Human review and release. We reviewed the definitions and hypotheses against the source problems,
but they would benefit from further peer review. Lean verifies that each completed proof establishes
its conclusion under the stated hypotheses; source review assesses whether the definitions and
hypotheses represent the intended problem. Each JSON record contains an identifier, a problem
name, an informal statement, a Lean target, and a representation label. We also release the shared
definitions and baseline proof attempts. The release is a collection of theorem targets, not a claim
that all targets have complete proofs. Baseline proof checking and results are described in Section 4.

4     Evaluation
We evaluated a multi-turn tool-using Opus 4.8-based agent using lean4skills and the Lean LSP
MCP server [Freer, 2025, Dressler, 2025]. Each target received one run capped at 15 minutes, allowing
Lean-error inspection, library and shared-definition search, loogle and leansearch queries, and
proof revisions. The same model family assisted with statement construction. This is a single-agent,
single-budget baseline, not a model comparison or repeated-run evaluation.
The agent produced 157 clean proofs out of 450. A proof is clean if Lean accepts it without sorry,
sorryAx, or additional admitted facts, checked by Lean comparator. Tables 1(b) and 1(c) report topic
and class breakdowns. These are descriptive comparisons: they do not separate abstraction effects
from differences in problems or library support.
Qualitative inspection found proof-search failures on plausible targets, missing lemmas or difficult
library interfaces, and a smaller group of formalization defects, including missing measurability,
integrability, or non-emptiness assumptions.

5     Limitations and Conclusion
We note that S TOCH B ENCH’s question curation, faithfulness review, and its topic and direct/abstracted
classifications are currently decided by human curators, introducing some bias; as the corresponding
terminologies were not rigorously defined within the scope of this work. Despite these limitations,
S TOCH B ENCH provides a focused testbed for evaluating proof agents on graduate stochastic processes.
Its newly constructed informal–formal pairs can support autoformalization training, while successfully
checked baseline proofs provide supervision for proof generation. Together with the shared definitions,
these resources support both the development of stronger domain-specific provers and the continued
formalization of stochastic processes in Lean.


                                                       4
References
Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and
  Jeremy Avigad. ProofNet: Autoformalizing and formally proving undergraduate-level mathematics.
  arXiv.org, 2023. doi: 10.48550/arXiv.2302.12433.
Alex Best, Christopher Birkbeck, Riccardo Brasca, Eric Rodriguez Boidi, Ruben van De Velde, and
  Andrew Yang. A complete formalization of fermat’s last theorem for regular primes in lean, 2025.
  URL https://arxiv.org/abs/2410.01466.
Raphael Coelho. A Machine-Checked Itô Calculus for Brownian Motion, 2026a. URL https:
  //arxiv.org/abs/2606.15089.
Raphael Coelho. A Formally Verified Library of Mathematical Finance in Lean 4, 2026b. URL
  https://arxiv.org/abs/2606.01356.
Rémy Degenne. Markov Kernels in Mathlib’s Probability Library, 2025. URL https://arxiv.or
  g/abs/2510.04070.
Rémy Degenne, David Ledvinka, Etienne Marion, and Peter Pfaffelhuber. Formalization of brownian
  motion in lean, 2025. URL https://arxiv.org/abs/2511.20118.
Shuo Deng and Kenneth W. Shum. From Lecture Notes to Lean: Formalizing a Textbook on
  Probability Theory, 2026. URL https://arxiv.org/abs/2607.27298.
Oliver Dressler. Lean LSP MCP: Tools for agentic interaction with the Lean theorem prover, 3 2025.
  URL https://github.com/oOo0oOo/lean-lsp-mcp.
Cameron Freer. Lean 4 Skills: Theorem proving skill and workflow pack for AI coding agents,
  October 2025. URL https://github.com/cameronfreer/lean4-skills.
Robert Gallager. 6.262 Discrete Stochastic Processes. Spring 2011. Massachusetts Institute of Tech-
  nology: MIT OpenCourseWare, https://ocw.mit.edu/, 2011. License: Creative Commons
  BY-NC-SA.
David Gamarnik. 15.070J Advanced Stochastic Processes. Fall 2013. Massachusetts Institute
  of Technology: MIT OpenCourseWare, https://ocw.mit.edu/, 2013. License: Creative
  Commons BY-NC-SA.
Sidharth Hariharan, Christopher Birkbeck, Seewoo Lee, Ho Kiu Gareth Ma, Bhavik Mehta, Auguste
  Poiroux, and Maryna Viazovska. A milestone in formalization: The sphere packing problem in
  dimension 8, 2026. URL https://arxiv.org/abs/2604.23468.
Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean Welleck. Lean-STaR: Learning to Interleave
  Thinking and Proving, 2024. URL https://arxiv.org/abs/2407.10040.
Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, and Zhijiang Guo. FormalAlign:
   Automated Alignment Evaluation for Autoformalization, 2024. URL https://arxiv.org/abs/
   2410.10135.
Etienne Marion. A Formalization of the Ionescu-Tulcea Theorem in Mathlib, 2025. URL https:
  //arxiv.org/abs/2506.18616.
L. D. Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language. In CADE,
   pages 625–635. Springer International Publishing, 2021. doi: 10.1007/978-3-030-79876-5_37.
Nilay Patel, Noah Arias, Davit Babayan, Victoria Cochran, Timothy Libman, Hafsah Mahmood,
  Liam McCarty, Soli Munoz, Laurel Willey, and Jeffrey Flanigan. MathAtlas: A Benchmark for
  Autoformalization in the Wild, 2026. URL https://arxiv.org/abs/2605.14061.
Auguste Poiroux, Antoine Bosselut, and Viktor Kunčak. RLMEval: Evaluating Research-Level
  Neural Theorem Proving, 2025. URL https://arxiv.org/abs/2510.25427.
Nikil Ravi, Kexing Ying, Vasilii Nesterov, Rayan Krishnan, Elif Uskuplu, Bingyu Xia, Janitha
  Aswedige, and Langston Nashold. FormalProofBench: Can models write graduate level math
  proofs that are formally verified? arXiv.org, 2026. doi: 10.48550/arXiv.2603.26996.


                                                5
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu,
  Wenjun Gao, Daya Guo, and Chong Ruan. DeepSeek-Prover-V2: Advancing Formal Mathematical
   Reasoning via Reinforcement Learning for Subgoal Decomposition, 2025. URL https://arxiv.
   org/abs/2504.21801.
Kyle Siegrist. Probability, Mathematical Statistics, and Stochastic Processes. LibreTexts, 2022.
  URL https://stats.libretexts.org/Bookshelves/Probability_Theory/Probabil
  ity_Mathematical_Statistics_and_Stochastic_Processes_(Siegrist). Originally
  sourced from http://www.randomservices.org/random. License: CC BY 2.0.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Towards Large Language Models as Copilots
  for Theorem Proving in Lean, 2024. URL https://arxiv.org/abs/2404.12534.
Alexander K Taylor, Junyi Zhang, Ethan Ji, Vigyan Sahai, Haikang Deng, Yuanzhou Chen, Yifan
  Yuan, Di Wu, Jia-Chen Gu, Kai-Wei Chang, Nanyun Peng, Amit Sahai, and Wei Wang. TaoBench:
  Do Automated Theorem Prover LLMs Generalize Beyond MathLib?, 2026. URL https://arxi
  v.org/abs/2603.12744.
The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, pages 367–381. ACM, 2020. doi:
  10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
The mathlib Community. Missing undergraduate mathematics in mathlib. https://leanprover
 -community.github.io/undergrad_todo.html, 2026.
George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Ami-
  tayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating neural theorem-provers on the
  putnam mathematical competition. Advances in Neural Information Processing Systems 37, pages
 11545–11569, 2024. doi: 10.52202/079017-0368.
Hao Wu. 18.445 Introduction to Stochastic Processes. Spring 2015. Massachusetts Institute of Tech-
  nology: MIT OpenCourseWare, https://ocw.mit.edu/, 2015. License: Creative Commons
  BY-NC-SA.
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo,
  and Chong Ruan. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement
  Learning and Monte-Carlo Tree Search, 2024. URL https://arxiv.org/abs/2408.08152.
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem Proving with Retrieval-Augmented
  Language Models, 2023. URL https://arxiv.org/abs/2306.15626.
Xiao-Wen Yang, Zihao Zhang, Jianuo Cao, Zhi Zhou, Zenan Li, Lan-Zhe Guo, Yuan Yao, Taolue
  Chen, Yu-Feng Li, and Xiaoxing Ma. FormalML: A Benchmark for Evaluating Formal Subgoal
  Completion in Machine Learning Theory, 2025. URL https://arxiv.org/abs/2510.02335.
Kexing Ying and Rémy Degenne. A Formalization of Doob’s Martingale Convergence Theorems in
  mathlib, 2022. URL https://arxiv.org/abs/2212.05578.
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
  Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. Formal-
  MATH: Benchmarking Formal Mathematical Reasoning of Large Language Models, 2025. URL
  https://arxiv.org/abs/2505.02735.
Shangtong Zhang. Towards Formalizing Reinforcement Learning Theory: A Robbins-Siegmund
  Approach, 2025. URL https://arxiv.org/abs/2511.03618.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. miniF2F: A cross-system benchmark for
  formal olympiad-level mathematics. In International Conference on Learning Representations,
  2021.



                                                6
A     Supplementary material
A.1   An abstracted proof example - SOTA Prover

We illustrate Q361 through its natural-language statement, Lean abstraction, and an agent-generated
proof obtained in a separate run lasting more than 30 minutes, outside the 15-minute baseline protocol.

Natural-language statement. Suppose that a Markov chain on a finite, nonempty state space Ω is
irreducible and has stationary probability measure π. Define the hitting time of x ∈ Ω by
                                       τx = min{n ≥ 0 : Xn = x}.
For a fixed state a ∈ Ω, let
                               X
                        t⊙ =         Ea [τx ] π(x),       thit = max Ex [τy ] ≥ t⊙ .
                                                                x,y∈Ω
                               x∈Ω

Show that                                                          X
                        thit ≤ 2 max Eπ [τw ],        Eπ [τw ] =         π(x)Ex [τw ].
                                 w∈Ω
                                                                   x∈Ω


Formalization. The Lean statement represents expected hitting times by a real-valued function
g(x, y) satisfying the first-step equations
                                      
                                        0,                       x = y,
                            g(x, y) =       P
                                        1 + z∈Ω P (x, z)g(z, y), x ̸= y.
These equations are supplied by IsHittingSolution; the proof works with this characteriza-
tion rather than constructing hitting-time random variables. The assumptions IsStochastic,
IsIrreducible, and IsStationary specify the transition matrix and stationary distribution. The
auxiliary quantity t⊙ and the given lower bound on thit are not needed for the formalized conclusion.

Proof structure and difficulty. Although Q361 asks for a single inequality, the generated proof
develops nine auxiliary theorems across several levels of abstraction. It establishes nonnegativity
of matrix powers and hitting-time solutions, extends closure under positive one-step transitions
to positive matrix powers, and proves a maximum-principle  P propagation lemma. A return-time
identity yields harmonicity of Kemeny’s function K(x) = y π(y)g(x, y), whose constancy follows
from irreducibility and the maximum principle. The same propagation lemmas are reused for
θ(x) = g(x, b) − g(x, c) to establish the hitting-time triangle inequality. Stationary averaging then
combines these results into a pointwise bound, which is lifted to the required supremum inequality.

Implications for proof search. The abstraction supplies the first-step equations, not Kemeny
constancy or the triangle inequality. The proof therefore builds supporting mathematics rather than
merely simplifying the supplied hypotheses. Its structure illustrates a challenge for hierarchical
proof search: identifying useful intermediate statements, proving them at sufficient generality for
reuse, and coordinating their dependencies. Here, elementary matrix and finite-sum reasoning
supports harmonic-function arguments, which in turn support the global hitting-time bound. The
agent-produced result is thus a coherent collection of auxiliary theorems together with their final
composition. This example shows how an abstracted benchmark target can test mathematical proof
construction beyond local tactic selection.
import Mathlib
import Leanproj.Basic
open MeasureTheory ProbabilityTheory Filter Auto
open scoped ENNReal NNReal Topology Matrix RealInnerProductSpace
attribute [local instance] Classical.propDecidable
set_option maxHeartbeats 2000000
set_option maxRecDepth 4096

namespace Q361Helpers

open Finset



                                                      7
/-- Entries of powers of a nonnegative matrix are nonnegative. -/
theorem pow_nonneg_entry {Ω : Type*} [Fintype Ω] [DecidableEq Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) : ∀ n x y, 0 ≤ (P ^ n) x y := by
  intro n
  induction n with
  | zero => intro x y; simp [pow_zero, Matrix.one_apply]; split <;> norm_num
  | succ k ih =>
    intro x y
    rw [pow_succ, Matrix.mul_apply]
    apply Finset.sum_nonneg; intro z _
    exact mul_nonneg (ih x z) (hP1 z y)

/-- Hitting times are nonnegative. -/
theorem g_nonneg {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq
                                                               P      Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,       y, P P
                                                                       x y = 1)
    (g : Ω → Ω → R) (hg : ∀ x y, g x y = if x = y then 0 else 1 +        z, P x z * g z y)
    (y : Ω) : ∀ x, 0 ≤ g x y := by
    obtain ⟨x0, -, hx0⟩ := Finset.exists_min_image Finset.univ (fun x => g x y)
    ⟨Classical.arbitrary Ω, Finset.mem_univ _⟩
  have hmin : ∀ x, g x0 y ≤ g x y := fun x => hx0 x (Finset.mem_univ x)
  have hx0y : g x0 y = 0 := by
    by_cases h : x0 = y
    · rw [hg x0 y, if_pos h]
    · exfalso
      have hval := hg x0 y
      rw [if_neg h] at hval P                           P
      have hlb :P(1 : R) +     z, P x0 z *Pg z y ≥ 1 +     z, P x0 z * g x0 y := by
        have : (    z, P x0 z * g z y) ≥     z, P x0 z * g x0 y := by
          apply Finset.sum_le_sum; intro z _
          exact mul_le_mul_of_nonneg_left (hmin z) (hP1 x0 z)
        linarith    P
      have hsum : (    z, P x0 z * g x0 y) = g x0 y := by
        rw [← Finset.sum_mul, hP2 x0, one_mul]
      rw [hsum] at hlb
      linarith [hval, hlb]
  intro x
  calc 0 = g x0 y := hx0y.symm
    _ ≤ g x y := hmin x

/-- Forward-closure reachability: a set closed under positive one-step transitions is
closed under positive ‘n‘-step transitions. -/
theorem reach_closed {Ω : Type*} [Fintype Ω] [DecidableEq Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y)
    (A : Ω → Prop) (hclosed : ∀ x, A x → ∀ z, 0 < P x z → A z)
    (x0 : Ω) (hx0 : A x0) : ∀ n z, 0 < (P ^ n) x0 z → A z := by
  have hpow := pow_nonneg_entry P hP1
  intro n
  induction n with
  | zero =>
    intro z hz
    rw [pow_zero, Matrix.one_apply] at hz
    by_cases h : x0 = z
    · rwa [← h]
    · simp [h] at hz
  | succ k ih =>
    intro z hz
    rw [pow_succ, Matrix.mul_apply] at hz
    have hex : ∃ w ∈ Finset.univ, (0:R) < (P ^ k) x0 w * P w z := by
      apply Finset.exists_lt_of_sum_lt; simpa using hz
    obtain ⟨w, -, hw⟩ := hex
    have h1 : 0 < (P ^ k) x0 w :=
      lt_of_le_of_ne (hpow k x0 w) (fun h => by rw [← h, zero_mul] at hw; exact lt_irrefl _
     hw)
    have h2 : 0 < P w z :=
      lt_of_le_of_ne (hP1 w z) (fun h => by rw [← h, mul_zero] at hw; exact lt_irrefl _ hw)
    exact hclosed w (ih w h1) z h2

/-- Maximum-principle propagation step: at a maximizing point where ‘f‘ is harmonic, all



                                              8
positively-reachable neighbours also attain the maximum. -/
theorem prop_step {Ω : Type*} [Fintype Ω]                     P
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,       y, P x y = 1)
    (f : Ω → R) (mP: R) (hmax : ∀ z, f z ≤ m) (x : Ω) (hfx : f x = m)
    (hharm : f xP =    z, P x z * f z) (z : Ω) (hz : 0 < P x z) : f z = m := by
  have hsum0P : (   w, P x w * (m - f w))P= 0 := by         P
    have : (    w, P x w * (m - f w)) = (   w, P x w) * m -    w, P x w * f w := by
      rw [Finset.sum_mul, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl; intro w _; ring
    rw [this, hP2 x, one_mul, ← hharm, hfx]; ring
  have hnonneg : ∀ w ∈ Finset.univ, 0 ≤ P x w * (m - f w) := by
    intro w _; exact mul_nonneg (hP1 x w) (by linarith [hmax w])
  have hzero := (Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp hsum0 z (Finset.mem_univ z)
  have : m - f z = 0 := by
    rcases mul_eq_zero.mp hzero with h | h
    · linarith [hz]
    · exact h
  linarith
                                            P
/-- Return-time identity: ‘π w · (1 +         _z P(w,z) g(z,w)) = 1‘. -/
theorem returnTime_identity {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq Ω]
    (P : Matrix Ω Ω R) (g : Ω → Ω → R)                   P
    (hg : ∀ x y, g x y = if    Px = y then 0 else 1 +       z, P x z * g z y)
    (π : Ω → R) P     (hpi2 :     x, π x = 1)
    (hpi3 : ∀ y,P       x, π x * P x y = π y) (w : Ω) :
    π w * (1 + P z, P w z *P      g z w) = 1 := by        P
  have hswap : P (     x, π x *P z, P x z * g z w) =P x,P        π x * g x w := by
    have e1 : (       x, π x *      z, P x z * g z w) =     x,     z, π x * (P x z * g z w) := by
      apply Finset.sum_congr rfl; intro x _; rw [Finset.mul_sum]
    rw [e1, Finset.sum_comm]
    apply Finset.sum_congr
             P                  rfl; intro z _     P
    have : (     x, π x * (P x z * g z w)) = (        x, π x * P x z) * g z w := by
      rw [Finset.sum_mul]; apply Finset.sum_congr rfl; intro x _; ring
    rw [this,P hpi3 z]
  have s1 : (P x, if x = w then 0 else π x) =P        1 - π w := by
    have : (     x, if x = w then 0 else π x) =         x, (π x - if x = w then π x else 0) := by
      apply Finset.sum_congr rfl; intro x _; by_cases hx : x = w <;> simp [hx]
    rw [this,P Finset.sum_sub_distrib, hpi2, Finset.sum_ite_eq’
                                                     P                 Finset.univ w π]; simp
  have s2P: (      x, if x = w then 0 elseP π x *       z, P x z * g z w)
      = (    x, π xP* g x w) - π w *          z, P w z * gPz w := by
    have step1
            P    :  (    x, if
                            P   x =  w then 0 else π x * Pz, P x z * g z w)
        = (     x, π x *
                P              z, P x z * g z w) - πPw *       z, P w z * g z w := by
      have :P (     x, if x = P w then 0 else π x *      z, P x z * g z w)
          =      x, ((π x *       z, P x zP* g z w)
                - (if x = w then π w *         z, P w z * g z w else 0)) := by
        apply Finset.sum_congr rfl; intro x _; by_cases hx : x = w <;> simp [hx]
      rw [this, Finset.sum_sub_distrib, Finset.sum_ite_eq’ Finset.univ w]; simp
    rw [step1,P  hswap]
  have key : (      x, π Px * g x w)                     P
      = (1 - π P w) + ((      x, π x * g x w) - π w * (      z, P w z * g z w)) := by
    have e1
          P: (        x, π x * g x w)                  P
        =     x, π x * (if x = w then 0 else 1 +          z, P x z * g z w) := by
      apply Finset.sum_congr
                 P                rfl; intro x _; rw [hg x P w]
    have e2P : (      x, π x * (if x = w then 0 else 1 +        z, P x z * g z w))
        = ( P   x, if x = w then 0 else π x)         P
          + (      x, if x = w then 0 else π x *        z, P x z * g z w) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl; intro x _
      by_cases hx : x = w <;> simp [hx] <;> ring
    conv_lhs => rw [e1, e2, s1, s2]
  nlinarith [key]
                           P                                    P
/-- Kemeny function ‘K x =   _c π_c g(x,c)‘ is harmonic: ‘K x =   _z P(x,z) K(z)‘. -/
theorem K_harmonic {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq
                                                              P       Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,      y, P P
                                                                      x y = 1)
    (g : Ω → Ω → R) (hg : ∀ x y, g x y = if x P  = y then 0 else 1 +    z, P x z * g z y)
    (π : Ω → R) (hpi1 : ∀ P x, 0 ≤ π x) (hpi2 :     x, π x = 1)
    (hRT : ∀ w, π w * (1 +    z, P w z * g z w) = 1) (x : Ω) :



                                                 9
     P                        P                  P
   (    c, π c * g x c) P   =      z, P x z * (     c, π c * g z c) := by
 have hpx : π x * (1 +          z, P x z * g z x) = 1 := hRT x
 have hpxpos : 0 < π x := by
   rcases (hpi1 x).lt_or_eq with h | h
   · exact h
   · exfalso; rw [← P   h, zero_mul] at hpx; norm_num at hpx
 have hret :P   π x * (     z, P x z *P  g z x) = 1 - π x := by nlinarith [hpx] P
 have e1 : (      c, π c * g x c) =        c, (if c = x then 0 else π c * (1 +           z, P x z * g z c
    )) := by
   apply Finset.sum_congr rfl; intro c _
   rw [hg x c]; by_cases h : x = c
   · simp [h]
   · rw [if_neg
              P h, if_neg (Ne.symm h)]                        P
 have e2P : (     c, (if c = x then 0 else π c * (1 +             z, P x z * g z c)))
      = ( P  c, if c = x then 0 else π c)           P
        + (     c, if c = x then 0 else π c *           z, P x z * g z c) := by
   rw [← Finset.sum_add_distrib]; apply Finset.sum_congr rfl; intro c _
   by_cases h P: c = x <;> simp [h] <;> ring
 have sa : P(     c, if c = x then 0 else π c) =P       1 - π x := by
   have : (      c, if c = x then 0 else π c) =            c, (π c - if c = x then π c else 0) := by
      apply Finset.sum_congr rfl; intro c _; by_cases h : c = x <;> simp [h]
   rw [this,P  Finset.sum_sub_distrib, hpi2, Finset.sum_ite_eq’
                                                      P                    Finset.univ x π]; simp
 have sbP : (     c, if c =Px then 0 else π c *            z, P Px z * g z c)
      = (    z, P P x z * (     c, π c * g z c)) - π x P    * (     z, P x z * g z x) := by
   have dropP  :  (    c, if
                          P   c  =  x then 0  else  π c  *    Pz,   P x z * g z c)
        = (     c, π c *
                P             z, P x z * g z c) - πPx *            z, P x z * g z x := by
      have :P (     c, if c = P x then 0 else π c *         z, P x z * g z c)
          =      c, ((π c *        z, P x zP* g z c)
                - (if c = x then π x *         z, P x z * g z x else 0)) := by
        apply Finset.sum_congr rfl; intro c _; by_cases h : c = x <;> simp [h]
      rw [this, Finset.sum_sub_distrib, Finset.sum_ite_eq’ Finset.univ x]; simp
   rw [drop]
   congr 1       P              P                           P       P
   have l1 : (       c, π c *       z, P x z * g z c) =         c,     z, π c * (P x z * g z c) := by
      apply Finset.sum_congr
                 P                rfl;
                                    P   intro  c _;  rw  [Finset.mul_sum]
                                                              P       P
   have l2 : (       z, P x z * (      c, π c * g z c)) =          z,    c, P x z * (π c * g z c) := by
      apply Finset.sum_congr rfl; intro z _; rw [Finset.mul_sum]
   rw [l1, l2, Finset.sum_comm]
   apply Finset.sum_congr rfl; intro z _; apply Finset.sum_congr rfl; intro c _; ring
 rw [e1, e2, sa, sb, hret]
 ring

/-- The Kemeny function is constant on an irreducible chain. -/
theorem K_const {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq
                                                               P   Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,      y, P x y = 1)
    (hirr : ∀ x y, ∃ n : N, 0 < (P ^ n)
                                      P x y)
    (K : Ω → R) (hharm : ∀ x, K x =      z, P x z * K z) (a b : Ω) : K a = K b := by
  obtain ⟨x0, -, hx0⟩ := Finset.exists_max_image Finset.univ K
    ⟨Classical.arbitrary Ω, Finset.mem_univ _⟩
  set m := K x0 with hm
  have hmax : ∀ z, K z ≤ m := fun z => hx0 z (Finset.mem_univ z)
  have hAclosed : ∀ x, K x = m → ∀ z, 0 < P x z → K z = m := by
    intro x hx z hz
    exact prop_step P hP1 hP2 K m hmax x hx (hharm x) z hz
  have hall : ∀ y, K y = m := by
    intro y
    obtain ⟨n, hn⟩ := hirr x0 y
    exact reach_closed P hP1 (fun w => K w = m) hAclosed x0 rfl n y hn
  rw [hall a, hall b]

/-- Hitting-time triangle inequality: ‘g a b ≤ g a c + g c b‘. -/
theorem tri_ineq {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq
                                                             P      Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,      y, P x y = 1)
    (hirr : ∀ x y, ∃ n : N, 0 < (P ^ n) x y)                         P
    (g : Ω → Ω → R) (hg : ∀ x y, g x y = if x = y then 0 else 1 +       z, P x z * g z y)
    (gnn : ∀ x y, 0 ≤ g x y) (a b c : Ω) : g a b ≤ g a c + g c b := by
  by_cases hbc : b = c
  · subst hbc



                                                  10
    have h0 : g b b = 0 := by rw [hg b b, if_pos rfl]
    have := gnn a b; nlinarith [h0]
  set θ : Ω → R := fun x => g x b - g x c with P hθ
  have hharm : ∀ x, x ̸= b → x ̸= c → θ x =       z, P x z * θ z := by
    intro x hxb hxc        P
    have gb : g x b = 1 + P z, P x z * g z b := by rw [hg x b, if_neg hxb]
    have gc : g x c = 1 +      z, P x z * g z c := by rw [hg x c, if_neg hxc]
    simp onlyP[hθ]; rw [gb, gc]                 P                      P
    have : (    z, P x z * (g z b - g z c)) = (    z, P x z * g z b) -    z, P x z * g z c :=
     by
      rw [← Finset.sum_sub_distrib]; apply Finset.sum_congr rfl; intro z _; ring
    rw [this]; ring
  obtain ⟨x0, -, hx0⟩ := Finset.exists_max_image Finset.univ θ
    ⟨Classical.arbitrary Ω, Finset.mem_univ _⟩
  set m := θ x0 with hm
  have hmax : ∀ z, θ z ≤ m := fun z => hx0 z (Finset.mem_univ z)
  have hθc : θ c = g c b := by simp only [hθ]; rw [hg c c, if_pos rfl]; ring
  have hθb : θ b = - g b c := by simp only [hθ]; rw [hg b b, if_pos rfl]; ring
  have hmeq : m = θ c := by
    by_cases hcA : θ c = m
    · exact hcA.symm
    · by_cases hbA : θ b = m
      · exfalso
        have h1 : m ≤ 0 := by rw [← hbA, hθb]; linarith [gnn b c]
        have h2 : 0 ≤ θ c := by rw [hθc]; exact gnn c b
        have h3 : θ c ≤ m := hmax c
        apply hcA; linarith
      · exfalso
        have hAclosed : ∀ x, θ x = m → ∀ z, 0 < P x z → θ z = m := by
           intro x hx z hz
           have hxb : x ̸= b := fun h => hbA (h ▶ hx)
           have hxc : x ̸= c := fun h => hcA (h ▶ hx)
           exact prop_step P hP1 hP2 θ m hmax x hx (hharm x hxb hxc) z hz
        obtain ⟨n, hn⟩ := hirr x0 c
        exact hcA (reach_closed P hP1 (fun w => θ w = m) hAclosed x0 rfl n c hn)
  have hθa : θ a ≤ θ c := by rw [← hmeq]; exact hmax a
  rw [hθc] at hθa
  simp only [hθ] at hθa
  linarith

/-- The core inequality: every hitting time is at most ‘2 * M‘. -/
theorem core_bound {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq
                                                                P        Ω]
    (P : Matrix Ω Ω R) (hP1 : ∀ x y, 0 ≤ P x y) (hP2 : ∀ x,        y, P x y = 1)
    (hirr : ∀ x y, ∃ n : N, 0 < (P ^ n) x y)                            P
    (g : Ω → Ω → R) (hg : ∀ x y, g x y = if x P    = y then 0 else 1 +     z, P x z * g z y)
    (π : Ω → R) P (hpi1 : ∀ x, 0 ≤ π x) (hpi2 :       x, π x = 1)
    (hpi3 : ∀ y,     x, π x * PP x y = π y)
    (M : R) (hM : ∀ y : Ω, (      x, π x * g x y) ≤ M) (a b : Ω) :
    g a b ≤ 2 * M := by
  have gnn : ∀ x y, 0 ≤ g x yP:= fun x y => g_nonneg P hP1 hP2 g hg y x
  have hRT : ∀ w, π w * (1 +      z, P w z * g z w) = 1 :=
    fun w => returnTime_identity P g hg π hpi2 hpi3 w
  have tri : ∀ x y z, g x y ≤ g x z + g z y :=
    fun x y z => tri_ineqPP hP1 hP2 hirr g hg gnnP x y z
  have Kconst : ∀ x y, (     c, π c * g x c) = (    c, π c * g y c) := by
    intro x y                                P
    exact K_const P hP1 hP2 hirr (fun x =>      c, π c * g x c)
      (fun x => K_harmonic P hP1 hP2 g hg π hpi1 hpi2 hRT x) x y
  -- Step 1: g a b ≤ K a P+ Z b                 P
  have hgab : g a b ≤ P(    c, π c * g a c) + (    c, π c * g c b) := by
    have h1 : g a b =     c, π c * g a b := by rw [← Finset.sum_mul, hpi2, one_mul]
    rw [h1, ← Finset.sum_add_distrib]
    apply Finset.sum_le_sum; intro c _
    have htri := tri a b c
    have : π c * g a b ≤ π c * (g a c + g c b) := mul_le_mul_of_nonneg_left htri (hpi1 c)
    nlinarith [this]
  -- Step 2: ZPb ≤ M
  have hZb : (   c, π c * g c b) ≤ M := hM b



                                              11
  -- Step 3: KP a ≤ M
  have hKa : (     c,Pπ c * g a c) ≤ M := P  by            P
    have hka_eqP :  (   c, π  c
                              P *  g a c) =     x, π xP* (    c, π cP* g x c) := by
      have : (     x, π x * (     c, π c * g x c)) =     x, π x * (    c, π c * g a c) := by
        apply Finset.sum_congr rfl; intro x _; rw [Kconst x a]
      rw [this, ← Finset.sum_mul, hpi2, one_mul]
    rw [hka_eq] P                 P                      P             P
    have swap : (P x, π x * (P c, π c * g x c)) = P c, π        Pc * (    x, π x * g x c) := by
      have l1 : (     x, π x * (     c, π c * g x c)) =      x,    c, π x * (π c * g x c) := by
        apply Finset.sum_congr
                   P              Prfl; intro x _; rw [Finset.mul_sum]
                                                         P      P
      have l2 : (     c, π c * (     x, π x * g x c)) =      c,    x, π c * (π x * g x c) := by
        apply Finset.sum_congr rfl; intro c _; rw [Finset.mul_sum]
      rw [l1, l2, Finset.sum_comm]
      apply Finset.sum_congr rfl; intro c _; apply Finset.sum_congr rfl; intro x _; ring
    rw [swap]
           P             P                         P
    calc (    c, π c * (     x, π x * g x c)) ≤       c, π c * M := by
               apply Finset.sum_le_sum; intro c _
               exact mul_le_mul_of_nonneg_left (hM c) (hpi1 c)
      _ = M := by rw [← Finset.sum_mul, hpi2, one_mul]
  linarith

end Q361Helpers

open Auto in
theorem q361_hitting_bound {Ω : Type*} [Fintype Ω] [Nonempty Ω] [DecidableEq Ω]
    (P : Matrix Ω Ω R) (hP : IsStochastic P) (hirr : IsIrreducible P)
    (g : Ω → Ω → R) (hg : IsHittingSolution P g)
     F : Ω → R) (hπ : IsStationary PFπ) :P
    (π
    ( p : Ω × Ω, g p.1 p.2) ≤ 2 *       w,    x, π x * g x w := by
  obtain ⟨hP1, hP2⟩ := hP
  obtain ⟨hpi1, hpi2, hpi3⟩ := hπ
  have hreach : ∀ x y, ∃ n : N, 0 < (P ^ n) x y := by
    intro x y
    obtain ⟨n, _, hn⟩ := hirr x y
    exact ⟨n,
           F hn⟩ P
  set M :=    w,    x, π x * g x w with hMdefP
  have hbddM : BddAbove (Set.range
                          P        (fun w =>    x, π x * g x w)) := Finite.bddAbove_range _
  have hZle : ∀ y : Ω, (    x, π x * g x y) ≤ M := fun y => le_ciSup hbddM y
  apply ciSup_le
  intro p
  exact Q361Helpers.core_bound P hP1 hP2 hreach g hg π hpi1 hpi2 hpi3 M hZle p.1 p.2


A.2   A direct proof example - Opus Prover

We illustrate Q222 through its natural-language statement, Lean abstraction, and an agent-generated
proof obtained in a separate run lasting less than 15 minutes.

Natural-language statement. Suppose that P is irreducible. Show that there exists a probability
measure π such that π = πP and π(x) > 0 for all x ∈ Ω.

Formalization. The Lean statement represents the chain by a real transition matrix P on a finite,
nonempty state space Ω. The assumptions IsStochastic and IsIrreducible specify nonnegative
entries, unit row sums, and reachability through positive entries of matrix powers. A stationary
probability measure is represented by a function π : Ω → R satisfying
                                   X                   X
                   π(x) ≥ 0,           π(x) = 1,         π(x)P (x, y) = π(y).
                                  x∈Ω                 x∈Ω

import Mathlib
import Leanproj.Basic
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal NNReal Topology Matrix
open Auto
variable {Ω : Type*} {m0 : MeasurableSpace Ω}



                                                12
Figure 2: Main logical dependencies in the generated proof of Q361. Shared maximum-principle
lemmas establish Kemeny constancy and the hitting-time triangle inequality, which are combined by
stationary averaging to prove the bound. Nodes give Lean theorem names and their mathematical
roles; dashed arrows indicate results supplied as hypotheses to later lemmas.

                                                                                  P
/-- The pushforward of a distribution ‘v‘ by the transition matrix ‘P‘: ‘(vP) y =   x, v x P
      x y‘. -/
private defPstepMap {Ω : Type*} [Fintype Ω] (P : Matrix Ω Ω R) (v : Ω → R) : Ω → R :=
  fun y =>     x, v x * P x y

/-- Cesàro averages of the iterates of ‘stepMap P‘ started at ‘v0‘. -/
private noncomputable def cesaro {Ω : Type*} [Fintype Ω] (P : Matrix Ω Ω R) (v0 : Ω → R)
    (N : N) : Ω → R :=         P
  fun y => (1 / (N + 1 : R)) *    n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) y

/-- ‘stepMap P‘ maps the standard simplex into itself. -/
private lemma stepMap_mem {Ω : Type*} [Fintype
                                           P     Ω] {P : Matrix Ω Ω R}
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x,      y, P x y = 1)
    {v : Ω → R} (hv : v ∈ stdSimplex R Ω) : stepMap P v ∈ stdSimplex R Ω := by
  refine ⟨fun Py => ?_, ?_⟩
  · show 0 ≤     x, v x * P x y
    exactPFinset.sum_nonneg
                P            (fun x _ => mul_nonneg (hv.1 x) (hP0 x y))
  · show    y,     x, v x * P x y = 1
    rw [Finset.sum_comm]
          P     P                   P           P
    calc    x,     y, v x * P x y =    x, v x *     y, P x y := by
          Papply Finset.sum_congr rfl; intro x _; rw [Finset.mul_sum]
      _ = P x, v x * 1 := by apply Finset.sum_congr rfl; intro x _; rw [hP1 x]
      _ =     x, v x := by apply Finset.sum_congr rfl; intro x _; rw [mul_one]
      _ = 1 := hv.2




                                               13
/-- Entries of powers of a nonnegative matrix are nonnegative. -/
private lemma pow_nonneg_entries {Ω : Type*} [Fintype Ω] [DecidableEq Ω] {P : Matrix Ω Ω R}

   (hP0 : ∀ x y, 0 ≤ P x y) : ∀ n x y, 0 ≤ (P ^ n) x y := by
 intro n
 induction n with
 | zero => intro x y; rw [pow_zero]; by_cases h : x = y <;> simp [Matrix.one_apply, h]
 | succ n ih =>
   intro x y
   rw [pow_succ, Matrix.mul_apply]
   exact Finset.sum_nonneg (fun z _ => mul_nonneg (ih x z) (hP0 z y))

/-- A stationary distribution is stationary for every power of ‘P‘. -/
                                : Type*} [Fintype Ω] [DecidableEq Ω] {P : Matrix Ω Ω R}
private lemma stationary_pow {Ω P
    {π : Ω P→ R} (hstat : ∀ y,     x, π x * P x y = π y) :
    ∀ n y,    x, π x * (P ^ n) x y = π y := by
  intro n
  induction n with
  | zero =>
    intro y
    rw [pow_zero]
    simp [Matrix.one_apply, Finset.sum_ite_eq’]
  | succ n ih =>
    introPy
    calc Px, πPx * (P ^ (n + 1)) x y
        =    x,    z, π x * ((P ^ n) x z * P z y) := by
          apply Finset.sum_congr rfl; intro x _
          rw
          P [pow_succ,
                 P      Matrix.mul_apply, Finset.mul_sum]
      _ = P z, Px, π x * ((P ^ n) x z * P z y) := Finset.sum_comm
      _ =    z, (   x, π x * (P ^ n) x z) * P z y := by
          apply Finset.sum_congr rfl; intro z _
          rw
          P [Finset.sum_mul]; apply Finset.sum_congr rfl; intro x _; ring
      _ =    z, π z * P z y := by
          apply Finset.sum_congr rfl; intro z _; rw [ih z]
      _ = π y := hstat y

theorem q222_stationary_existence_positive {Ω : Type*} [Fintype Ω] [DecidableEq Ω] [Nonempty
      Ω]
    (P : Matrix Ω Ω R) (hP : IsStochastic P) (hirr : IsIrreducible P) :
    ∃ π : Ω → R, IsStationary P π ∧ ∀ x, 0 < π x := by
  obtain ⟨hP0, hP1⟩ := hP
  -- Choose a starting point in the simplex.
  obtain ⟨v0, hv0⟩ : (stdSimplex R Ω).Nonempty := Set.nonempty_coe_sort.mp inferInstance
  -- The iterates of ‘stepMap P‘ stay in the simplex.
  have hiter : ∀ n, (stepMap P)^[n] v0 ∈ stdSimplex R Ω := by
    intro n
    induction n with
    | zero => simpa only [Function.iterate_zero_apply] using hv0
    | succ n ih => rw [Function.iterate_succ_apply’]; exact stepMap_mem hP0 hP1 ih
  -- The Cesàro averages stay in the simplex.
  have hbmem : ∀ N, cesaro P v0 N ∈ stdSimplex R Ω := by
    intro N
    refine ⟨fun y => ?_, ?_⟩        P
    · show 0 ≤ (1 / (N + 1 : R)) *     n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) y
      exactPmul_nonneg (by positivity)
                                     P(Finset.sum_nonneg (fun n _ => (hiter n).1 y))
    · show    y, (1 / (N + 1 : R)) *     n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) y = 1
      rw [← Finset.mul_sum, Finset.sum_comm]
      rw [Finset.sum_congr rfl (fun n (_ : n ∈ Finset.range (N + 1)) => (hiter n).2)]
      rw [Finset.sum_const, Finset.card_range]
      simp only [nsmul_eq_mul, mul_one, Nat.cast_add, Nat.cast_one]
      exact one_div_mul_cancel (by positivity)
  -- Key algebraic identity: ‘stepMap‘ moves the Cesàro average by a telescoping tail.
  have hdiff : ∀ N y, stepMap P (cesaro P v0 N) y - cesaro P v0 N y
      = (1 / (N + 1 : R)) * (((stepMap P)^[N + 1] v0) y - v0 y) := by
    intro N y
    have hTb : stepMap P (cesaro
                               P P v0 N) y
        = (1P/ (N + 1 : R)) *     n ∈ Finset.range (N + 1), ((stepMap P)^[n + 1] v0) y := by
      show    x, cesaro P v0 N x * P x y = _



                                             14
    have e1 : ∀ x, cesaro P v0 PN x * P x y
         = (1 / (N + 1 : R)) *    n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) x * P x y
   := by
      intro x                    P
      show ((1 / (N + 1 : R)) *      n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) x) * P x
    y = _
      rw [mul_assoc, Finset.sum_mul]
    rw [Finset.sum_congr rfl (fun x (_ : x ∈ Finset.univ) => e1 x), ← Finset.mul_sum]
    congr 1
    rw [Finset.sum_comm]
    applyP Finset.sum_congr rfl; intro n _
    show     x, ((stepMap P)^[n] v0) x * P x y = ((stepMap P)^[n + 1] v0) y
    rw [Function.iterate_succ_apply’]; rfl
  have hbNy : cesaro P v0 N yP
      = (1 / (N + 1 : R)) *     n ∈ Finset.range (N + 1), ((stepMap P)^[n] v0) y := rfl
  rw [hTb, hbNy, ← mul_sub]
  congr 1
  rw [← Finset.sum_sub_distrib, Finset.sum_range_sub (fun n => ((stepMap P)^[n] v0) y)]
  simp [Function.iterate_zero_apply]
-- Hence ‘stepMap‘ of the average minus the average tends to ‘0‘.
have htend0 : ∀ y, Filter.Tendsto (fun N => stepMap P (cesaro P v0 N) y - cesaro P v0 N y)
    Filter.atTop (nhds 0) := by
  intro y
  refine squeeze_zero_norm (fun N => ?_) tendsto_one_div_add_atTop_nhds_zero_nat
  rw [hdiff N y, norm_mul]
  have ha := mem_Icc_of_mem_stdSimplex (hiter (N + 1)) y
  have hb := mem_Icc_of_mem_stdSimplex hv0 y
  rw [Set.mem_Icc] at ha hb
  have hcnn : (0 : R) ≤ 1 / ((N : R) + 1) := by positivity
  rw [Real.norm_of_nonneg hcnn]
  have hbound : ∥((stepMap P)^[N + 1] v0) y - v0 y∥ ≤ 1 := by
    rw [Real.norm_eq_abs, abs_le]
    refine ⟨?_, ?_⟩ <;> linarith [ha.1, ha.2, hb.1, hb.2]
  calc 1 / ((N : R) + 1) * ∥((stepMap P)^[N + 1] v0) y - v0 y∥
      ≤ 1 / ((N : R) + 1) * 1 := mul_le_mul_of_nonneg_left hbound hcnn
    _ = 1 / ((N : R) + 1) := mul_one _
-- Extract a convergent subsequence of the averages; its limit is stationary.
obtain ⟨π, hπsimplex, φ, hφmono, hφtend⟩ := (isCompact_stdSimplex R Ω).tendsto_subseq
   hbmem
have hπcoord : ∀ x, Filter.Tendsto (fun N => cesaro P v0 (φ N) x) Filter.atTop (nhds (π x)
   ) :=
  fun x => tendsto_pi_nhds.mp
                 P             hφtend x
have key : ∀ y,     x, π x * P x y = π y := by
  intro y                              P
  have hL1 : PFilter.Tendsto (fun N =>     x, cesaro P v0 (φ N) x * P x y) Filter.atTop
      (nhds (    x, π x * P x y)) :=
    tendsto_finset_sum _ (fun x _ => (hπcoord x).mul_const (P x y))
  have hL2 : Filter.Tendsto (fun N => cesaro P v0 (φ N) y) Filter.atTop (nhds (π y)) := hπ
   coord y
  have hLdiff : Filter.Tendsto
                  P
      (fun N => (    x, cesaro
                            P P v0 (φ N) x * P x y) - cesaro P v0 (φ N) y)
      Filter.atTop (nhds ((    x, π x * P x y) - π y)) := hL1.sub hL2
  have hL0 : Filter.Tendsto
                  P
      (fun N => (    x, cesaro P v0 (φ N) x * P x y) - cesaro P v0 (φ N) y)
      Filter.atTop (nhds 0) := (htend0 y).comp hφmono.tendsto_atTop
  have huniq := tendsto_nhds_unique hLdiff hL0
  linarith [huniq]
refine ⟨π, ⟨hπsimplex.1, hπsimplex.2, key⟩, ?_⟩
-- Strict positivity via irreducibility.
intro x0
obtain ⟨a, ha⟩ : ∃ a, 0 < π a := by
  by_contra h
  push_neg atPh
  have h0 :     x, π x = 0 :=
    Finset.sum_eq_zero (fun a _ => le_antisymm (h a) (hπsimplex.1 a))
  rw [hπsimplex.2] at h0
  exact one_ne_zero h0
obtain ⟨n, _, hn2⟩ := hirr a x0



                                            15
  have hpow := stationary_pow key n x0
  rw [← hpow]
  refine Finset.sum_pos’
    (fun x _ => mul_nonneg (hπsimplex.1 x) (pow_nonneg_entries hP0 n x x0)) ?_
  exact ⟨a, Finset.mem_univ a, mul_pos ha hn2⟩




Figure 3: Main logical dependencies in the generated proof of Q222. A telescoping identity and
compactness establish a stationary subsequential limit of the Cesàro averages. Irreducibility and
stationarity under matrix powers then yield strict positivity. Nodes include helper lemmas and local
proof facts; edge labels identify supplied hypotheses or supporting arguments.


A.3   An abstracted proof example - Opus Prover

We illustrate Q128 through its natural-language statement, Lean abstraction, and an agent-generated
proof obtained in a separate run lasting less than 15 minutes.

Natural-language statement. Let Bµ (t) = µt + σB(t) be a Brownian motion with drift. Show
that Bµ (t) − µt is a martingale, and that (Bµ (t) − µt)2 − σ 2 t is a martingale.

Formalization. The Lean statement uses a real-valued process B on a probability space with
measure µ and filtration F. Adaptedness and integrability of Bt and Bt2 are explicit assumptions.
For 0 ≤ s ≤ t, HasLaw specifies Bt − Bs ∼ N (0, t − s), and Indep specifies independence
of this increment from Fs . Lean uses c for the drift and µ for the probability measure. Writing



                                                16
Xt = ct + σBt , the conclusion consists of the almost-sure conditional-expectation identities
                                  Eµ [Xt − ct | Fs ] = Xs − cs,
                         Eµ [(Xt − ct)2 − σ 2 t | Fs ] = (Xs − cs)2 − σ 2 s.
The increment properties are supplied as hypotheses; the proof derives the two identities from these
properties.
import Mathlib
import Leanproj.Basic
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal NNReal Topology Matrix
open Auto
variable {Ω : Type*} {m0 : MeasurableSpace Ω}

theorem q128_drifted_brownian_martingale (µ : Measure Ω) [IsProbabilityMeasure µ]
    ( F : Filtration R m0) (B : R → Ω → R) (c σ : R)
    (hadap : Adapted F B)
    (hint : ∀ t, Integrable (B t) µ)
    (hint2 : ∀ t, Integrable (fun ω => (B t ω) ^ 2) µ)
    (hB0 : ∀m ω ∂µ, B 0 ω = 0)
    (hincr : ∀ s t : R, 0 ≤ s → s ≤ t →
      HasLaw (fun ω => B t ω - B s ω) (gaussianReal 0 (t - s).toNNReal) µ)
    (hpast : ∀ s t : R, 0 ≤ s → s ≤ t →
      Indep (MeasurableSpace.comap (fun ω => B t ω - B s ω) inferInstance) ( F s) µ) :
    (∀ s t : R, 0 ≤ s → s ≤ t →
        µ[(fun ω => (c * t + σ * B t ω) - c * t) | ( F s)]
          =m [µ] (fun ω => (c * s + σ * B s ω) - c * s)) ∧
    (∀ s t : R, 0 ≤ s → s ≤ t →
        µ[(fun ω => ((c * t + σ * B t ω) - c * t) ^ 2 - σ ^ 2 * t) | ( F s)]
          =m [µ] (fun ω => ((c *R s + σ * B s ω) - c * s) ^ 2 - σ ^ 2 * s)) := by
  have hsq_int : ∀ v : NNReal,    x, x ^ 2 ∂(gaussianReal (0:R) v) = (v : R) := by
    intro v
    have hv := variance_of_integral_eq_zero (µ := gaussianReal (0:R) v) (X := fun x => x)
      measurable_id.aemeasurable (by simpa using integral_id_gaussianReal (µ := (0:R)) (v :=
      v))
    rw [variance_fun_id_gaussianReal] at hv
    simpa using hv.symm
  have main : ∀ s t : R, 0 ≤ s → s ≤ t →
      (µ[B t | F s] =m [µ] B s) ∧
      (µ[fun ω => (B t ω) ^ 2 | F s] =m [µ] fun ω => (B s ω) ^ 2 + (t - s)) := by
    intro s t hs hst
    have hst0 : (0:R) ≤ t - s := by linarith
    have hBt : Measurable (B t) := (hadap t).mono ( F .le t) le_rfl
    have hBs : Measurable (B s) := (hadap s).mono ( F .le s) le_rfl
    have hg_meas : Measurable (fun ω => B t ω - B s ω) := hBt.sub hBs
    have hg_int : Integrable (fun ω => B t ω - B s ω) µ := (hint t).sub (hint s)
    have hindep := hpast s t hs hst
    have hle1 : MeasurableSpace.comap (fun ω => B t ω - B s ω) inferInstance ≤ m0 :=
      hg_meas.comap_le
    have hle2 : F s ≤ m0 := F .le s
    have hsm : StronglyMeasurable[MeasurableSpace.comap (fun ω => B t ω - B s ω)
     inferInstance]
        (fun ω => B t ω - B s ω) := (measurable_iff_comap_le.2 le_rfl).stronglyMeasurable
    have hEg : µ[fun ω => B t ω - B s ω] = 0 := by
      rw [(hincr s t hs hst).integral_eq, integral_id_gaussianReal]
    have hcz : µ[fun ω => B t ω - B s ω | F s] =m [µ] fun _ => (0 : R) := by
      have h := condExp_indep_eq hle1 hle2 hsm hindep
      rw [hEg] at h; exact h
    have hmart : µ[B t | F s] =m [µ] B s := by
      have hcond_Bs : µ[B s | F s] = B s :=
        condExp_of_stronglyMeasurable hle2 (hadap s).stronglyMeasurable (hint s)
      have key : (B t) = (B s) + (fun ω => B t ω - B s ω) := by
        funext ω; show B t ω = B s ω + (B t ω - B s ω); ring
      have hadd : µ[B t | F s] =m [µ]
          (µ[B s | F s] + µ[fun ω => B t ω - B s ω | F s]) := by
        calc µ[B t | F s] = µ[(B s) + (fun ω => B t ω - B s ω) | F s] :=
              congrArg (fun h => µ[h | F s]) key


                                                 17
         _ =m [µ] _ := condExp_add (hint s) hg_int _
    filter_upwards [hadd, hcz] with ω h1 h3
    rw [h1]; simp [Pi.add_apply, hcond_Bs, h3]
  refine ⟨hmart, ?_⟩
  have hmemBt : MemLp (B t) 2 µ :=
    (memLp_two_iff_integrable_sq hBt.aestronglyMeasurable).2 (hint2 t)
  have hmemBs : MemLp (B s) 2 µ :=
    (memLp_two_iff_integrable_sq hBs.aestronglyMeasurable).2 (hint2 s)
  have hmemInc : MemLp (fun ω => B t ω - B s ω) 2 µ := hmemBt.sub hmemBs
  have hd_int : Integrable (fun ω => (B t ω - B s ω) ^ 2) µ := hmemInc.integrable_sq
  have hmem2Bs : MemLp (fun ω => 2 * B s ω) 2 µ := hmemBs.const_mul 2
  have hb_int : Integrable ((fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω)) µ :=
    hmem2Bs.integrable_mul hmemInc
  have ha_int : Integrable (fun ω => (B s ω) ^ 2) µ := hint2 s
  have ea : µ[fun ω => (B s ω) ^ 2 | F s] = fun ω => (B s ω) ^ 2 :=
    condExp_of_stronglyMeasurable hle2 ((hadap s).pow_const 2).stronglyMeasurable ha_int
  have eb : µ[(fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω) | F s] =m [µ] fun _ => (0:R
   ) := by
    have hpull := condExp_mul_of_stronglyMeasurable_left
       (((hadap s).const_mul 2).stronglyMeasurable) hb_int hg_int
    filter_upwards [hpull, hcz] with ω h1 h3
    rw [h1]; simp [Pi.mul_apply, h3]
  have hsm_d : StronglyMeasurable[MeasurableSpace.comap (fun ω => B t ω - B s ω)
   inferInstance]
       (fun ω => (B t ω - B s ω) ^ 2) :=
    ((measurable_iff_comap_le.2 le_rfl).pow_const 2).stronglyMeasurable
  have hEd : µ[fun ω => (B t ω - B s ω) ^ 2] = t - s := by
    have hc := (hincr s t hs hst).integral_comp (f := fun x : R => x ^ 2) (by fun_prop)
    simp only [Function.comp_def] at hc
    rw [hc, hsq_int, Real.coe_toNNReal _ hst0]
  have ed : µ[fun ω => (B t ω - B s ω) ^ 2 | F s] =m [µ] fun _ => (t - s) := by
    have h := condExp_indep_eq hle1 hle2 hsm_d hindep
    rw [hEd] at h; exact h
  have key2 : (fun ω => (B t ω) ^ 2) =
       (fun ω => (B s ω) ^ 2) + (fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω)
         + (fun ω => (B t ω - B s ω) ^ 2) := by
    funext ω; simp only [Pi.add_apply, Pi.mul_apply]; ring
  have hcongr : µ[fun ω => (B t ω) ^ 2 | F s] =
       µ[(fun ω => (B s ω) ^ 2) + (fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω)
         + (fun ω => (B t ω - B s ω) ^ 2) | F s] :=
    congrArg (fun h => µ[h | F s]) key2
  have e2 : µ[(fun ω => (B s ω) ^ 2) + (fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω) |
   F s]
       =m [µ] (µ[fun ω => (B s ω) ^ 2 | F s]
         + µ[(fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω) | F s]) :=
    condExp_add ha_int hb_int _
  have e1 : µ[(fun ω => (B s ω) ^ 2) + (fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω)
         + (fun ω => (B t ω - B s ω) ^ 2) | F s]
       =m [µ] (µ[(fun ω => (B s ω) ^ 2) + (fun ω => 2 * B s ω) * (fun ω => B t ω - B s ω)
   | F s]
         + µ[fun ω => (B t ω - B s ω) ^ 2 | F s]) :=
    condExp_add (ha_int.add hb_int) hd_int _
  rw [hcongr]
  filter_upwards [e1, e2, eb, ed] with ω h1 h2 hb hd
  rw [h1]
  simp only [Pi.add_apply] at h2 ⊢
  rw [h2, ea]
  simp only [Pi.add_apply] at hb hd ⊢
  rw [hb, hd]
  ring
constructor
· intro s t hs hst
  have h368 := (main s t hs hst).1
  have harg : (fun ω => (c * t + σ * B t ω) - c * t) = σ • B t := by
    funext ω; simp only [Pi.smul_apply, smul_eq_mul]; ring
  rw [harg]
  have hsmul := condExp_smul (µ := µ) σ (B t) ( F s : MeasurableSpace Ω)
  filter_upwards [hsmul, h368] with ω h1 h2



                                          18
    simp only [Pi.smul_apply, smul_eq_mul] at h1
    rw [h1, h2]; ring
  · intro s t hs hst
    have hquad := (main s t hs hst).2
    have harg : (fun ω => ((c * t + σ * B t ω) - c * t) ^ 2 - σ ^ 2 * t) =
         (σ ^ 2 • (fun ω => (B t ω) ^ 2)) - (fun _ => σ ^ 2 * t) := by
      funext ω; simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; ring
    rw [harg]
    have hconst : µ[(fun _ => σ ^ 2 * t) | F s] = fun _ => σ ^ 2 * t :=
      condExp_const ( F .le s) _
    have hsmul := condExp_smul (µ := µ) (σ ^ 2) (fun ω => (B t ω) ^ 2) ( F s :
     MeasurableSpace Ω)
    have hBt2 : MemLp (B t) 2 µ :=
      (memLp_two_iff_integrable_sq
         (((hadap t).mono ( F .le t) le_rfl).aestronglyMeasurable)).2 (hint2 t)
    have hsub : µ[(σ ^ 2 • (fun ω => (B t ω) ^ 2)) - (fun _ => σ ^ 2 * t) | F s]
         =m [µ] (µ[σ ^ 2 • (fun ω => (B t ω) ^ 2) | F s] - µ[(fun _ => σ ^ 2 * t) | F s]) :=
      condExp_sub (Integrable.smul (σ ^ 2) hBt2.integrable_sq) (integrable_const _) _
    filter_upwards [hsub, hsmul, hquad] with ω hs1 hs2 hq
    rw [hs1]
    simp only [Pi.sub_apply, hconst]
    rw [hs2]
    simp only [Pi.smul_apply, smul_eq_mul]
    rw [hq]
    ring




Figure 4: Main logical dependencies in the generated proof of Q128. Both conclusions use the zero
conditional increment mean. The squared-process argument additionally requires the conditional
second moment and integrability of the cross term. Deterministic scaling and subtraction complete the
proof. Nodes name local proof facts and the final theorem; edge labels identify additional hypotheses
or algebraic steps.




                                                 19
