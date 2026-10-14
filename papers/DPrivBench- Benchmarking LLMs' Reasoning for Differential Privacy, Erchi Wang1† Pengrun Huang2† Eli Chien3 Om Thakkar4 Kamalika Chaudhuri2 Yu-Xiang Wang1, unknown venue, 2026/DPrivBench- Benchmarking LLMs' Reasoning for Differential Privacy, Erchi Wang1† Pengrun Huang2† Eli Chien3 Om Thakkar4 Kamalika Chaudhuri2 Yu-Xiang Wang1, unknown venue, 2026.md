                                              DP RIV B ENCH : B ENCHMARKING LLM S ’ R EASONING FOR
                                                               D IFFERENTIAL P RIVACY

                                             Erchi Wang1† Pengrun Huang2† Eli Chien3 Om Thakkar4 Kamalika Chaudhuri2 Yu-Xiang Wang1
                                                                                   Ruihan Wu4†,∗
                                                                           1
                                                                            Halıcıoğlu Data Science Institute, UC San Diego
                                                                  2
                                                                    Department of Computer Science and Engineering, UC San Diego
arXiv:2604.15851v3 [cs.LG] 18 May 2026




                                                                  3
                                                                    Department of Electrical Engineering, National Taiwan University
                                                                                               4
                                                                                                 OpenAI
                                                                    †
                                                                      Denotes core contribution, ∗ Work performed at UC San Diego
                                                                     Correspondence to: erw011@ucsd.edu, ruihan@openai.com




                                                                                              A BSTRACT
                                                  Differential privacy (DP) has a wide range of applications for protecting data privacy, but designing
                                                  and verifying DP algorithms requires expert-level reasoning, creating a high barrier for non-expert
                                                  practitioners. Prior works either rely on specialized verification languages that demand substantial
                                                  domain expertise or remain semi-automated and require human-in-the-loop guidance. In this work,
                                                  we investigate whether large language models (LLMs) can automate DP reasoning. We introduce
                                                  DPrivBench, a benchmark in which each instance asks whether a function or algorithm satisfies a
                                                  stated DP guarantee under specified assumptions. The benchmark is carefully designed to cover a
                                                  broad range of DP topics, span diverse difficulty levels, and resist shortcut reasoning through trivial
                                                  pattern matching. Experiments show that while the strongest models handle textbook mechanisms
                                                  well, all models struggle with advanced algorithms, revealing substantial gaps in current DP reasoning
                                                  capabilities. Through further analytic study and failure-mode analysis, we identify several promising
                                                  directions for improving automated DP reasoning. Our benchmark provides a solid foundation for
                                                  developing and evaluating such methods, and complements existing benchmarks for mathematical
                                                  reasoning.

                                         Resources: § Code        |      Dataset

                                         1   Introduction
                                         Differential privacy (DP) [28] has emerged as the gold standard for data privacy, offering rigorous mathematical
                                         guarantees that protect individual information while still enabling meaningful analyses. Its impact spans a wide range
                                         of applications from national statistics released by government agencies [2, 33] to the handling of user data by major
                                         technology companies [35, 31, 63, 5].

                                         Despite its broad applicability, developing and deploying DP mechanisms for specific use cases often requires substantial
                                         expertise. Designing an algorithm with a target privacy budget involves careful reasoning with specialized knowledge
                                         in DP, an error-prone task even for DP researchers [see, e.g., 47]. This high barrier prevents non-experts from utilizing
                                         DP in their application.

                                         Towards the long-term goal of developing and deploying DP algorithms automatically, the literature has primarily
                                         advanced along two directions. Programmatic DP verification [60, 8, 9, 3, 64] formally verify DP guarantees by
                                         checking symbolic proofs or synthesizing mechanisms from formal algorithm specifications. While these systems
                                         provide strong soundness guarantees, they typically require substantial domain expertise to encode algorithms in
                                         specialized verification languages, which limits their accessibility to non-expert users. Another complementary line
                                         of work can be viewed as semi-automated DP, pioneered by DPCheatSheet [18], in which LLMs are used to help
                                         non-experts design and implement DP algorithms interactively.
                       DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy




Figure 1: Overview of DPrivBench. The left panel shows a representative reasoning instance, while the right panel
summarizes the benchmark construction: Category 1 mechanism-level instances from a function bank and Category 2
algorithm-level instances from the DP literature. Overall, DPrivBench contains 588 Category 1 and 125 Category 2
instances, totaling 713 instances.


With the rapid progress of large language models (LLMs), especially their strong performance on general mathematical
reasoning tasks [39, 56, 34], it is natural to ask whether they can assist with reasoning about differential privacy
(DP), for example, by identifying flaws in DP proofs or verifying the privacy guarantees of stated DP algorithms.
Unlike approaches based on formal verification languages or intensive human-in-the-loop guidance, this direction
treats the LLM as the primary reasoning agent: given an algorithm description in natural language or LATEX, as is often
the case in practice, the LLM is asked to reason about whether the algorithm satisfies a claimed DP guarantee. A
sufficiently capable agent could support both beginners in developing basic DP algorithms and experts by serving as a
complementary “second check” on the correctness of system design.
This paper focuses on this emerging direction as the first work:
                              Can LLM reason about the DP guarantees of algorithms?
To study this question, we introduce DPrivBench, a benchmark of curated instances that describe an algorithm and
its assumptions, and ask LLMs to verify the stated DP guarantee. The benchmark is designed according to three
guiding principles for comprehensiveness and reliability: broad topic coverage, diverse difficulty levels, and resistance
to shortcut reasoning through trivial pattern matching.The benchmark consists of two complementary categories.
DPrivBench contains two complementary categories: Category 1 covers textbook sensitivity-based mechanisms, while
Category 2 targets advanced DP algorithms requiring substantially more sophisticated reasoning.
By evaluating a diverse set of state-of-the-art language models on DPrivBench, we obtain several key observations. For
foundational sensitivity-based DP mechanisms, the strong closed-source models (eg. GPT-5-High and Gemini-3-Pro)
equipped with an enhanced reasoning mode achieve high accuracy, while all other models exhibit non-negligible
error rates. For advanced differential privacy algorithms with nontrivial analysis, no evaluated model demonstrates
consistently strong performance, even among stronger models such as GPT-5.5-High and Gemini-3.1-Pro. These
results suggest that while current models are sufficient for textbook-level DP reasoning and may serve as useful aids for
beginners, a gap remains for reliably analyzing modern DP algorithms.
We conduct further study supported by our collected metadata, aiming to guide the future study for better LLM
reasoning. First, we evaluate whether providing explicit references that mimic information retrieval from external
sources improves accuracy. In this case, performance increases noticeably, pointing to a promising direction for future
tools that integrate LLM reasoning with curated DP knowledge bases. Second, we further utilize LLM-as-Judge to
perform fine-grind analysis of response, and find that the prediction produced by strong reasoning models is trustworthy
in general. Last, We conduct targeted case studies to characterize common model failure modes, highlighting key
aspects to address when improving reasoning trajectories.
Our benchmark serves as a cornerstone for advancing the automation of DP reasoning with LLMs, paving
the way for broader deployment of DP by reducing expertise requirements and enhancing efficiency for experts. By
guiding the development of stronger reasoning agents, our benchmark can further promote the wider adoption of
privacy-preserving techniques in real-world applications. Beyond its practical value for privacy research, it also serves
as a new and challenging testbed for mathematical reasoning. Since DP is typically taught as a graduate-level topic
in applied mathematics and theoretical computer science, our benchmark complements existing math reasoning datasets
(e.g., GSM8K [19], GPQA [62], MATH-Perturb [38]).



                                                           2
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


2     Problem Set-Up
Differential Privacy. DP is a formal framework for quantifying privacy guarantees in randomized algorithms. It ensures
that the algorithm’s output distribution changes only minimally when a single individual’s data is modified, providing
robustness against arbitrary auxiliary information. We next present the standard definition of (ε, δ)-differential privacy.
Definition 2.1 ((ε, δ)-Differential Privacy [28]). A randomized mechanism M : D → R with domain D and range R
satisfies (ε, δ)-differential privacy if for any neigbouring datasets pair D, D′ ∈ D, and for any measurable subset of
outputs S ⊆ R, it holds that P[M(D) ∈ S] ≤ eε · P[M(D′ ) ∈ S] + δ

2.1   LLM reasoning for differential privacy
A long-term goal of LLM-based reasoning for DP is to build agents that can assist throughout the full DP workflow.
Ideally, given a non-private function or algorithm and a target privacy budget, such an agent would be able to design a
differentially private variant or even produce a faithful implementation, with a sound argument for its privacy guarantee.
Success on this broader goal would make DP more accessible to non-expert users and provide useful design baselines
for DP researchers.
Achieving this end-to-end goal, however, requires a more basic capability: the ability to verify whether a proposed
algorithm actually satisfies a claimed privacy guarantee. We therefore focus first on the verification task rather than on
open-ended algorithm design, for two reasons. First, verification could be a necessary building block for trustworthy
DP generation: a reliable DP verifier can therefore be used to evaluate candidate designs, guide iterative refinement,
or serve as a reward signal for training LLMs that generate increasingly valid DP algorithms. Second, verification is
practically useful in its own right. It can help audit proposed mechanisms and identify mistakes in privacy arguments.
Motivated by these considerations, in this paper we focus on the following question as the first step towards LLM-based
reasoning for DP: Can LLMs reason about the DP guarantees of algorithms? Specifically, given a concrete
description of a function or algorithm together with a claimed privacy guarantee, an LLM is tasked with determining
whether the guarantee holds.
To support this study, we construct a benchmark with the following design principles:
• Broad topic coverage. The benchmark spans core topics in DP, making the evaluation broadly representative and
  relevant to the DP community. A complete list of covered topics is provided in Table 6.
• Diverse difficulty. It ranges from textbook mechanisms to advanced mathematical reasoning about research-level DP
  algorithms, enabling fine-grained assessment across difficulty levels.
• Resistance to shortcut reasoning. Instances are designed to require genuine reasoning, preventing correct answers
  from being obtained via recall of public training data.
Within these principles, benchmark performance provides a reliable signal of DP reasoning ability and a solid foundation
for developing improved DP reasoning methods. In particular, verification is not merely a simplified proxy for algorithm
generation; it is a necessary building block for any future system that aims to design, implement, and justify differentially
private algorithms end to end.

2.2   Related Work
We now discuss how the emerging direction of LLM-based reasoning for differential privacy connects to other lines
of work in differential privacy. Overall, we view this emerging direction as complementary to existing directions: in
some cases, they address different stages or challenges, while in others, they pursue similar goals from different angles.
In both settings, combining these approaches can lead to stronger, more accessible, and reliable privacy-preserving
systems.
DP Auditing. DP auditing is an important line of work for detecting implementation-level violations of differential
privacy. Most existing approaches adopt a black-box framework [12, 22]: by carefully designing neighboring input
datasets and empirically evaluating the outputs of a target implementation, auditors estimate a lower bound on the
privacy loss. If this empirical lower bound exceeds the claimed theoretical guarantee, it indicates a likely privacy
violation due to implementation bugs. Recently, several works [67, 48, 70] have focused on improving the efficiency of
such audits, reducing the number of required executions to mitigate the substantial computational overhead, especially
in settings involving large-scale deep learning models. For a comprehensive survey, we refer readers to [4].
In contrast to implementation auditing, our work targets the correctness of algorithms themselves, as specified in natural
language and mathematical notation. These two directions address complementary but equally essential stages of the
DP pipeline. Implementation auditing serves as a final safeguard prior to deployment, whereas algorithm-level checking


                                                             3
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


operates earlier in the design process, verifying whether a proposed algorithmic description satisfies differential privacy
in the first place.
Programmatic DP verification. A line of work [60, 8, 9, 3, 72, 64, 55] investigates DP verification through program-
language and formal-methods approaches, which encode algorithms in specialized languages and establish privacy
guarantees using symbolic proofs such as type systems, relational Hoare logic, or coupling arguments.
Our work pursues the same goal of determining whether an algorithm satisfies a DP guarantee, but through LLM-based
reasoning. While prior systems offer strong formal soundness, they require substantial expertise and are often limited in
expressiveness. In contrast, LLMs can reason directly over natural-language and mathematical algorithm descriptions,
lowering the barrier to use and enabling analysis of more expressive settings.
Verified DP implementations. Besides DP auditing and programmatic verification, there are also software libraries
for verified DP implementations and privacy accounting, such as TensorFlow Privacy [68], Opacus [71], AutoDP [6],
and OpenDP [66]. These tools provide human-verified building blocks for implementing DP mechanisms and support
privacy accounting to improve implementation correctness. However, when new building blocks are introduced and
when the algorithm design goes beyond what is representable using existing building blocks, we currently still rely on
a slow and error-prone human-verification process. We believe LLMs, when used carefully, can help reduce human
efforts and enhance correctness. Moreover, going beyond this work, LLMs can function as tool-using agents that make
packages like OpenDP [66] more accessible – a natural and important future direction.
Under the broader objective of automating differential privacy, LLM-based reasoning is better suited to supporting
algorithm design and first-pass expert-like checking, while verified DP libraries remain essential for deployment and
serve as an additional verification safeguard.
LLM benchmarks on mathematical reasoning. Mathematical reasoning with large language models has been
extensively studied in recent years, leading to the development of a wide range of evaluation benchmarks. Representative
pre-college–level benchmarks include MATH [37], GSM8K [19], and AIME [49], which primarily assess problem-
solving skills in algebra, geometry, and arithmetic. Recent closed-source models with enhanced reasoning capabilities
achieve near-perfect performance on these benchmarks, while open-source models continue to exhibit a noticeable
performance gap. More challenging benchmarks target college-level and graduate-level mathematics, including
MathBench [44], Ghost [32], GPQA [62], HARDMath [30], and MATH-Perturb [38]. These datasets require deeper
conceptual understanding and multi-step reasoning. Even the strongest existing models still show substantial room for
improvement.
Our proposed benchmark, DPrivBench, also contributes to this line of work by focusing on differential privacy
reasoning, a core topic in graduate-level applied mathematics and theoretical computer science.

3   Dataset Construction
In this section, we describe the construction of DPrivBench. Each question consists of a concrete algorithm description
together with a claimed privacy guarantee, and asks whether the algorithm satisfies that guarantee. To ensure
broad coverage of privacy notions, the claimed guarantees are stated under different DP frameworks across questions,
including approximate DP [28], Rényi DP [53], zero-Concentrated DP[13], and Gaussian DP[25], with privacy
parameters specified either as fixed constants or as functions of algorithmic parameters.
Guided by the principles of broad topic coverage and diverse difficulty levels, we organize the benchmark into two
complementary categories. Category 1 focuses on foundational DP mechanisms and requires textbook-level reasoning
about function sensitivity and noise calibration, which are fundamental components of nearly all DP algorithms. In
contrast, Category 2 targets advanced DP algorithms drawn from a broad range of research topics. These questions
require nontrivial, algorithm-specific reasoning beyond standard textbook lookup, and therefore pose a substantially
greater challenge than Category 1. We further collect auxiliary metadata in Category 2, including reference links
and expert-written comments, for better understanding the LLM reasoning.
3.1 Category 1: Mechanism-Level Instances with a Function Bank
Category 1 evaluates models’ ability to reason about foundational, textbook-level DP mechanisms. We use a query-
release type formulation: each mechanism is specified by a template and instantiated with a concrete query function
sampled from a curated function bank.
Mechanism. We consider six mechanism settings: the Laplace mechanism [28] under pureDP, the Gaussian mechanism
under zCDP or Gaussian DP, Report-Noisy-Max with Gumbel noise (known as Exponential mechanism [52]), Report-
Noisy-Max with Laplace noise [29], Report-Noisy-Max with Exponential noise (i.e. Permute-and-Flip mechanism
[50, 21]). Each setting is instantiated as a mechanism template that adds calibrated noise to a query function, possibly


                                                            4
                            DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


      Topic                               Yes No Total          Suppose that for all z ∈ Z, ℓ(·, z) is twice-differentiable, and the
      Privacy Accounting                   5    7    12         rank of its Hessian ∇2 ℓ(w, z) at any w ∈ W is at most 1. Also
      Amplification by Subsampling         2    3     5         assume that the smoothness parameter satisfies β ≤ εnλ.
      Private Selection                    2    3     5         Is the following algorithm (ε, δ)-differentially private?
      DP Gradient Descent                  1   12    13
      DP Linear Regression                 1    5     6         Algorithm 1: AObjP : Objective Perturbation
      DP Hyperparameter Tuning             1    5     6
      Private Agg. of Teacher Ensembles    1    2     3         Input: Private dataset S = (z1 , . . . , zn ) ∈ Z n , L-Lipschitz,
      Propose-Test-Release                 2    2     4                β-smooth, convex loss function ℓ, convex set W ⊆ Rd ,
      Parallel Composition                 6    8    14                privacy parameters ε ≤ 1, δ ≤ 1/n2 , regularization
      Sparse Vector Technique              3    5     8
                                                                       parameter λ.
      Sequential/Adaptive Composition      3    4     7
      Smooth Sensitivity                   2    1     3                                              10L2 log(1/δ)
      DP Adam                              1    2     3         1: Sample G ∼ N (0, σ 2 Id ), where σ 2 =          ;
      DP SGD                               3    6     9
                                                                                                           ε2
                                                                                                 ⟨G,w⟩        2
      Mean Estimation                      5   10    15         2: return ŵ = arg min L̂(w; S) + n + λ∥w∥ , where
                                                                                  w∈W
      Objective Perturbation               1    3     4                      1 Pn
      Output Perturbation                  1    2     3          L̂(w; S) ≜         ℓ(w, zi );
      Quantile Estimation                  2    3     5                      n i=1
      Total                               42   83   125

    Table 1: Topic distribution in Category 2.                     Figure 2: Example question from Category 2 (Qid 87).


followed by mechanism-specific transformations. As a concrete example, the Laplace mechanism is stated as below.
Formal definitions of all six mechanisms are provided in the Appendix A.1.
Theorem 3.1 (Laplace Mechanism [28]). Given query function f : D → R, the laplace mechanism A(D) =
                                                                                                     1
f (D) + Lap(∆f /ε) satisfies ε-DP, where Lap(b) denotes the Laplace distribution with density p(x) = 2b exp(−|x|/b).
In our construction, the query function is drawn from a curated function bank.
Function Bank. To systematically evaluate models’ ability to reason about sensitivity calculation and noise calibration,
we construct a curated function bank consisting of 49 functions, initially generated by GPT-5 and subsequently filtered
by the authors, to ensure a wide range of sensitivity-reasoning difficulty. Without loss of generality, each function maps
an n-dimensional data vector x ∈ [0, 1]n to a real-value scalar and we manually compute its tight global sensitivity ∆f ,
which serves as the ground truth involving in constructing positive or negative question instances:
                                            ∆f =       max
                                                        ′    n
                                                               |f (x) − f (x′ )|
                                                          x∼x ∈[0,1]
                                                                                                      Pn
The bank admits a broad difficulty range: from functions with immediate sensitivity, such as f (x) =P i=1 xi with
                                                                                                       n
∆f = 1, to functions requiring reasoning about global extrema and coordinate coupling, such as f (x) = i=1 |xi − x̄|,
                                 2(n−1)
whose tight sensitivity is ∆f = n .
Category 1 construction. Given a DP mechanism and a function–sensitivity pair (g, ∆g ) from the function bank, we
generate a positive instance by correctly calibrating the noise to ∆g , as shown in the example below. Negative instances
are constructed by under-calibrating the noise multiplier. For example, replacing Lap(∆g /ε) with Lap(∆g /(2ε))
yields a negative instance: the mechanism satisfies only 2ε-DP, rather than the claimed ε-DP guarantee.
    Category 1: Question Template for Laplace Mechanism

    Suppose X = (x1 , . . . , xn ) ∈ [0, 1]n . Define f (X) = g(X) and define f˜(X) = f (X) + Lap(∆g · 1ε ). The neighboring
    datasets X and X ′ differ in at most one element. Does f˜ satisfy ε-differential privacy?

To test genuine reasoning beyond theorem memorization, we instantiate questions with explicit mechanisms and
concrete functions, rather than mechanism names alone. In addition, positive and negative instances are paired to differ
only in a single noise-scaling term. These two approach make surface-level pattern matching insufficient for achieving
high accuracy.
3.2 Category 2: Algorithm-Level Instances from Research Literatures
Beyond fundamental DP mechanisms, we further evaluate models on more advanced DP algorithms. Instances in
this category are derived from algorithms in the research literature (Table 6), together with a systematic perturbation
approach to generate negative questions.
DP algorithm selection from the literature. We organize algorithm selection around four major areas in differential
privacy: DP accounting, DP statistics, DP machine learning, and data-adaptive mechanisms. Within these areas, we


                                                                   5
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


identify 16 commonly studied topics and select representative algorithms for each. Table 1 summarizes the topics and
the corresponding number of instances.
Structured instance construction. For each selected algorithm, we construct both positive and negative instances.
Algorithms taken from the peer-reviewed literature generally yield positive (yes) instances. To test whether models
understand the underlying DP reasoning rather than merely memorize canonical results, we systematically perturb these
algorithms to create negative (no) instances. Notice that each positive example is decomposed into three components:
(i) the algorithm description, (ii) the underlying assumptions or conditions, and (iii) the claimed DP guarantee. We
provide a colored text box for illustration (Fig. 2). We then generate negative instances by perturbing exactly one
of these components at a time: (1) algorithm perturbations, such as altering the necessary algorithmic steps; (2)
assumption perturbations, such as removing essential conditions (e.g., convexity of the loss function); and (3) guarantee
perturbations, such as claiming a strictly stronger privacy guarantee than what the algorithm can support. Concrete
examples of these perturbations are illustrated in Appendix E. We also include a more fine-grained taxonomy of error
patterns in the Appendix B.
Resistance to shortcut reasoning. Negative instances are constructed through targeted perturbations, so models cannot
succeed by simply memorizing published results. Such memorization would tend to incorrectly accept perturbed
algorithms that superficially resemble valid ones. For positive instances, we conduct a rephrasing-based perturbation test.
The stable accuracy suggests that model performance is not driven by memorization. We defer details to Appendix G.
Evaluation scope. This category is substantially more challenging: correctness cannot be checked by directly applying
textbook DP mechanisms, but requires algorithm-specific reasoning about advanced analyses and nontrivial design
choices. Since each question is associated with a topic in Table 1, this category also supports fine-grained evaluation
across DP research topics.
Auxiliary metadata. Beyond questions and binary labels, we provide auxiliary metadata to support validation and
future research on automated DP reasoning. Each instance includes a reference link pointing to the source paper
underlying the instance and expert-written comments that serve as proof sketches. In our experiments, this
metadata allows us to evaluate whether knowledge augmentation improves LLM performance, and to analyze model
behavior beyond binary accuracy by checking whether the reasoning trace correctly supports the final decision. 1

4       Experimental Setup and Results Overview
Rubric-guided binary evaluation. To enable reliable and automated metric computation, we adopt a standardized
prompt template that instructs the LLM to produce a binary “yes” or “no” decision in a fixed, machine-parsable format.
If a model fails to follow this instruction and does not output an explicit binary verdict, we apply a secondary judging
step using GPT-4o to map the response to a “yes” or “no” label. Each question is evaluated using the binary correctness
metric. For the main results, we run five trials with different random seeds and report accuracy aggregated across seeds.
Benchmarking LLMs. We evaluate 11 LLMs on both Category 1 and Category 2. The models cover the closed-
source models (GPT-5 with minimal reasoning effort, GPT-5 with highest reasoning effort, Gemini-3, Gemini-2.5-
flash, Claude-Sonnet, Claude-Opus), the open-source models (Qwen3-30-Think, Qwen3-30-Instruct, DeepSeek-R1,
DeepSeek-V3.1-chat, Goedel-Prover-V2). In addition, for Category 2, the advanced algorithm track, we further evaluate
three up-to-date frontier models: Gemini-3.1-Pro, GPT-5.4-High, and GPT-5.5-High. We report model details, including
version and release date, in Table 8. Throughout all experiments, we disabled the tool use for a fair comparison.
In Section 5, we will present the results for the 11 LLMs on our benchmark DPrivBench. In Section 6, we will
conduct further analysis supported by our metadata and the case study for failure modes to better understand the model
performance and gain more intuition of how to improve the performance in future work.

5       Main Results
For Category 1, we highlight two findings. First, the strongest closed-source models, GPT-5-High and Gemini-3-Pro,
achieve near-perfect performance, while other models leave clear room for improvement. Second, most models,
including open-source ones, perform nearly perfectly on questions involving the standard Laplace mechanism, but
accuracy drops substantially on the other five mechanisms. For Category 2, we again observe that GPT-5-High and
Gemini-3-Pro perform best, but both still have substantial room for improvement in this more challenging setting. We
further analyze their per-topic accuracy, ranking topics by performance to identify which DP research areas are easiest
and hardest for LLMs to reason about.
    1
   For the better readability of metadata, please refer to: https://github.com/erchiw/DPriv-Bench/blob/main/cate_2_
metadata.pdf


                                                            6
                            DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy



Table 2: Model accuracy (↑) on the Category 1 (mean ± 1.96×standard error). Model-Avg reports the averaged
accuracy across the six tasks for each model. Task-Avg reports the accuracy after averaging across the eleven models
for each task.
                           Task-Avg       Lap.        Gauss. (GDP)        Gauss. (zCDP)     ExpMech        Lap. RNM          P-n-F

      GPT-5-High            0.995     1.000 ± 0.000   0.976 ± 0.014       1.000 ± 0.000   1.000 ± 0.000   0.998 ± 0.004   0.996 ± 0.005
      Gemini-3-Pro          0.923     1.000 ± 0.000   0.996 ± 0.005       1.000 ± 0.000   0.959 ± 0.022   0.645 ± 0.019   0.939 ± 0.006
      Gemini-2.5-Flash      0.778     1.000 ± 0.000   0.743 ± 0.052       0.996 ± 0.005   0.749 ± 0.045   0.514 ± 0.026   0.665 ± 0.015
      Claude-Sonnet-4.5     0.738     0.949 ± 0.017   0.814 ± 0.015       0.931 ± 0.022   0.588 ± 0.023   0.549 ± 0.038   0.600 ± 0.038
      GPT-5-Minimal         0.736     0.963 ± 0.022   0.733 ± 0.046       0.835 ± 0.032   0.782 ± 0.016   0.573 ± 0.019   0.533 ± 0.037
      Claude-Opus-4.5       0.728     0.955 ± 0.023   0.753 ± 0.038       0.908 ± 0.017   0.502 ± 0.031   0.590 ± 0.026   0.657 ± 0.035
      DeepSeek-V3.1-chat    0.841     0.992 ± 0.007   0.951 ± 0.016       0.994 ± 0.005   0.818 ± 0.026   0.643 ± 0.033   0.651 ± 0.038
      DeepSeek-R1           0.741     0.933 ± 0.030   0.929 ± 0.020       0.943 ± 0.020   0.763 ± 0.043   0.359 ± 0.040   0.522 ± 0.029
      Qwen3-30-Instruct     0.671     0.992 ± 0.007   0.567 ± 0.038       0.918 ± 0.006   0.520 ± 0.033   0.508 ± 0.032   0.520 ± 0.054
      Goedel-Prover-V2      0.628     0.873 ± 0.033   0.596 ± 0.041       0.822 ± 0.027   0.500 ± 0.035   0.469 ± 0.022   0.506 ± 0.030
      Qwen3-30-Think        0.565     0.973 ± 0.015   0.545 ± 0.010       0.569 ± 0.013   0.418 ± 0.023   0.416 ± 0.037   0.465 ± 0.042

      Model-Avg               -          0.966           0.782                0.901          0.691           0.570           0.641




5.1       Model Performance on Category 1 Benchmark
Overall performance. Table 2 summarizes overall performance on Category 1. Among all evaluated models, GPT-5-
High is the only one to achieve near-perfect accuracy (0.995). The strongest open-source model, DeepSeek-V3.1-chat,
reaches 0.841, leaving a substantial gap relative to the best closed-source models. Overall, these results show that
sensitivity calculation and noise calibration remain challenging for open-source models we tested.

Fine-grained results across mechanisms. We further report mechanism-level accuracy in Table 2. Nearly all
models except Goedel-Prover-V2 achieve high performance (≥ 0.94) on the Laplace mechanism, but accuracy drops
substantially on the other five mechanisms. Since all questions use the same function bank, the main difference is not
sensitivity computation, but how the noise multiplier is calibrated to satisfy mechanism-specific privacy guarantees. This
suggests that many models can compute sensitivity correctly yet struggle to apply it in less familiar DP mechanisms,
likely because the Laplace mechanism is more prevalent in training data.

A particularly interesting case is Report-Noisy-Max with Laplace noise. GPT-5-High is the only model with perfect
accuracy, while all others, including Gemini-3-Pro, perform near or below the 0.5 random-guess baseline. Inspection
shows that many models incorrectly reuse the standard Laplace noise scale, adding Lap(∆f /ε) instead of the required
Lap(2∆f /ε) to each candidate value. They therefore tend to answer “yes” for all instances, yielding roughly 0.5
accuracy. This confusion between closely related mechanisms highlights a limitation in mechanism-specific DP
reasoning.

5.2       Model Performance on Category 2 Benchmark
Overall performance. In Table 3, we report F1, precision, and recall for Category 2. GPT-5.5-High and Gemini-3.1-Pro
achieve the best overall performance, with F1 scores of 0.829 and 0.810, respectively; Gemini-3.1-Pro has higher
precision, while GPT-5.5-High has higher recall. Among open-source models, the DeepSeek series performs best,
reaching an F1 score of 0.614, outperforming GPT-5-Minimal (0.548) and Gemini-2.5-Flash (0.602). Nevertheless,
most other models perform close to or below a naive always-yes baseline (F1 ≈ 0.503)2 , indicating that advanced
algorithm-level DP reasoning remains challenging for current LLMs.

Fine-grained results across topics. We further analyze per-topic accuracy for the four best-performing models,
GPT-5.5-High, GPT-5.4-High, Gemini-3.1-Pro, and Gemini-3-Pro. By ranking topics according to their mean accuracy
across the two models, we identify which topics are easiest and most challenging for LLMs to reason about.
As shown in Table 4, Quantile, DP-Adam, Accounting, and Private Selection are the easiest topics, with all models
achieving accuracy at least 0.95. In contrast, Smooth Sensitivity, PATE, Output Perturbation, emerge as the most
challenging topics, with average accuracies below 0.6.

      2                                                                                             42
   This baseline predicts “yes” for all Category 2 instances, yielding Recall = 1.00, Precision = 42+83 ≈ 0.336, and
F1 ≈ 0.503.


                                                                      7
                               DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy



                         Table 3: Model performance on the Category 2 (↑) (mean ± 1.96×standard error).
                                        Model                  F1 Score            Precision          Recall
                                        GPT-5.5-High         0.829 ± 0.021       0.807 ± 0.026     0.852 ± 0.017
                                        Gemini-3.1-Pro       0.810 ± 0.016       0.831 ± 0.025     0.790 ± 0.027
                                        GPT-5.4-High         0.793 ± 0.009       0.731 ± 0.013     0.867 ± 0.019
                                        Gemini-3-Pro         0.748 ± 0.019       0.699 ± 0.018     0.805 ± 0.034
                                        GPT-5-High           0.742 ± 0.032       0.716 ± 0.044     0.771 ± 0.024
                                        Gemini-2.5-Flash     0.602 ± 0.028       0.637 ± 0.038     0.571 ± 0.026
                                        GPT-5-Minimal        0.548 ± 0.036       0.497 ± 0.031     0.614 ± 0.052
                                        Claude-Sonnet-4.5    0.518 ± 0.046       0.499 ± 0.040     0.538 ± 0.054
                                        Claude-Opus-4.5      0.487 ± 0.026       0.516 ± 0.028     0.462 ± 0.028
                                        DeepSeek-R1          0.614 ± 0.050       0.657 ± 0.045     0.576 ± 0.054
                                        DeepSeek-V3.1-chat   0.603 ± 0.032       0.576 ± 0.029     0.633 ± 0.041
                                        Qwen3-30-Instruct    0.460 ± 0.019       0.526 ± 0.024     0.410 ± 0.027
                                        Qwen3-30-Think       0.407 ± 0.046       0.509 ± 0.070     0.343 ± 0.052
                                        Goedel-Prover-V2     0.362 ± 0.045       0.509 ± 0.063     0.281 ± 0.037



Table 4: Category 2 topic-wise Accuracy (↑). We report the top four and bottom three topics. (Please refer to Table 10
for complete results.)
          Topic                                                 Gemini-3-Pro       Gemini-3.1      GPT-5.4-High       GPT-5.5-High      Avg
          DP Adam                                                         1.00              1.00              1.00               1.00   1.00
          Quantile Estimation                                             1.00              1.00              1.00               1.00   1.00
          Privacy Accounting                                              0.92              1.00              1.00               0.98   0.97
          Private Selection                                               0.80              1.00              1.00               1.00   0.95
          ...
          Output Perturbation                                             0.33              0.87              0.40               0.67   0.57
          Private Aggregation of Teacher Ensembles (PATE)                 0.67              0.60              0.40               0.60   0.52
          Smooth Sensitivity                                              0.33              0.33              0.33               0.33   0.33




6     More Analytic Results and Case Study
6.1   Context-Augmented DP Reasoning
We study whether external context improves DP reasoning through theorem augmentation, retrieval augmented
generation, and in-context learning. For the 18 lowest-accuracy questions in Category 2, we augment prompts with
information from correct prior implementations, key theorems, and relevant definitions, either by directly injecting the
information or by retrieving it from a reference-paper database via RAG. We augment prompts in two ways: by directly
providing the relevant key theorem, or more implicitly by retrieving supporting evidence through RAG from a database
of source papers identified by the metadata reference link. As shown in Figure 3, direct theorem augmentation
yields the largest gains, while RAG also improves performance but more modestly, reflecting its noisier yet more
realistic retrieval setting.

                                0.625
                         0.6
                                                                                                                     with theorem
                                                                                                                     RAG
                                          0.521                                                                      zero-shot
                         0.5
                                                                 0.467                                0.463
                                                                          0.435
                         0.4
                                                  0.403
                                                                                                                0.353
              F1 Score




                                                                                    0.315
                         0.3
                                                                                                                         0.258
                         0.2


                         0.1


                         0.0
                                    GPT-5-High                    Gemini-2.5-Flash                         GPT-5-Low
Figure 3: Performance on the 18 hardest Category 2 questions with theorem augmentation, RAG, and zero-shot
prompting. Scores are averaged over five trials.


                                                                          8
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


We further evaluate one-shot in-context learning on the challenging Category 1 LaplaceRNM task, where instances
share similar proof structures. Using a single Laplace Report Noisy Max question–answer exemplar adapted from
Theorem A.8 (Appendix C.3.2), we observe improved performance, as shown in Table 5.

                    Table 5: One-shot in-context learning accuracy (mean ± 1.96× standard error).
                                 Model                  Zero-Shot        One-shot
                                  GPT-5-Minimal         0.573 ± 0.019      0.737 ± 0.065
                                  Gemini-2.5-Flash      0.514 ± 0.026      0.661 ± 0.073


6.2 Reasoning Plausibility and Soundness Beyond Binary Evaluation
To assess whether LLMs reason correctly about differential privacy, rather than merely guessing the final “yes”/“no”
label via superficial patterns or flawed reasoning, we conduct a reasoning-level evaluation on Category 2 using a strong
LLM judge, GPT-5.4-High. We focus on the best-performing closed-source models: GPT and Gemini families.
Given the question, model response, and metadata expert-written comment as an optional reference hint, the
judge assigns one of the fine-grained labels in Table 9, with increasing level of correctness: fatal_error,
unclear_or_insufficient, correct_direction_fixable, minor_gap, correct. We define reasoning plausi-
bility as labels at least correct_direction_fixable, and reasoning soundness as labels at least minor_gap. Among
responses with final predictions matches ground-truth label, we report the fraction with plausible or sound reasoning in
Table 4.
We find that predictions from strong reasoning models are        Figure 4: Reasoning quality on Category 2 (mean ± std). (Note
largely trustworthy at the level of high-level DP principles.    that Plausibility and Soundness are computed only among re-
For GPT-5.5-High and Gemini-3.1-Pro, both plausibility           sponses with correct final answers. See Appendix C.4.3 for
and soundness scores are close to 1. For both GPT-5-High         detailed metric definitions.)
and Gemini-3-Pro, plausibility is close to one. However,          Model              Accuracy(↑)     Plausibility(↑)   Soundness(↑)
their lower soundness scores show that many proofs re-
                                                                  GPT-5.5-High       0.882 ± 0.017   0.998 ± 0.004     0.978 ± 0.008
main incomplete or mathematically unsound. This gap is            GPT-5.4-High       0.848 ± 0.008   0.996 ± 0.005     0.949 ± 0.018
larger for weaker models; for example, Gemini-2.5-Flash           Gemini-3.1-Pro     0.875 ± 0.012   0.973 ± 0.006     0.848 ± 0.018
achieves relatively high final-answer accuracy but much           GPT-5-High         0.819 ± 0.029   0.950 ± 0.019     0.773 ± 0.013
lower plausibility and soundness. Overall, final-answer cor-      Gemini-3-Pro       0.818 ± 0.014   0.943 ± 0.017     0.732 ± 0.020
rectness is informative for strong reasoning models, but can      GPT-5-Minimal      0.661 ± 0.030   0.874 ± 0.007     0.623 ± 0.022
                                                                  Gemini-2.5-Flash   0.746 ± 0.024   0.702 ± 0.037     0.429 ± 0.014
overestimate proof-level reasoning quality, especially for
weaker models. For examples of judge results, please refer
to Appendix F.

6.3 Case Study for Failure Modes
We analyze two common failure modes exhibited by the top performing models. By identifying these error patterns,
we aim to provide insights that can inform future method development – for example, by using these failure modes as
highlighted aspects when assessing the correctness of a reasoning trajectory.
Failure to identify subtle but semantically significant changes. We find that LLMs can confuse questions with
similar structures, leading to systematic errors. In Q106 from our dataset, we modify the standard assumption required
for parallel composition: instead of requiring pairwise disjointness, i.e., Xi ∩ Xj = ∅ for all i ̸= j, we require only
sequential disjointness, i.e., Xi ∩ Xi+1 = ∅. We then ask whether the resulting algorithm satisfies parallel composition.
Among the models evaluated, only Gemini-3.1-Pro succeeds in one out of five trials; all other models, including
GPT-5.4-High, GPT-5.5-High, Gemini-3-Pro, and GPT-5-High, achieve zero accuracy on this question.
We further include Q76. In this case, the issue is that the summation in the numerator ranges from 1 to n − 1 rather
than from 1 to n, which doubles the sensitivity. As a result, the added Laplace noise is insufficient. Only Gemini-3-Pro
and GPT-5-High succeed in one out of five trials, while all other models, including GPT-5.4-High, GPT-5.5-High, and
Gemini-3.1-Pro, achieve zero accuracy.
Hallucination of assumptions learned from training data. LLMs may also hallucinate assumptions based on
their pretraining data. For example, in one output perturbation question (Figure 6), the original result appears as
Proposition 2.1 in [46], where the sensitivity of the objective is defined with respect to the minimizer. In our question,
however, we omit this assumption and state only that an L2 sensitivity is considered in general, which should typically
be interpreted as the sensitivity of the function f . This interpretation is insufficient to guarantee the correctness of the


                                                             9
                         DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


 Category 2 Question 106 (Label: No)
 Consider the following procedure:     M := {Mi (Xi )}n i=1 , where Xi ∩ Xi+1 = ∅ for all i ∈ {1, . . . , n − 1}, and their union
 covers the entire dataset, i.e., n
                                 S
                                   i=1 X i = X. Furthermore, the partition is data-independent.
 Suppose each mechanism Mi satisfies (εi , δi )-differential privacy.             Does the combined mechanism M satisfy
 (maxi∈[n] εi , maxi∈[n] δi )-differential privacy?


 Category 2 Question 76 (Label: No)
 Does the following algorithm satisfy ε-differential privacy under the add/remove neighboring relation?
 Algorithm 2: Mean estimation
 Input: scalar dataset D := {x1 , . . . , xn }, privacy budget ε, clipping threshold C.
 Sample ξ1 ∼ Lap(2C/ε).
 Sample ξ2 ∼ Lap(2/ε).
 Let                                                Pn−1
                                                       i=1 min{max{−C, xi }, C} + ξ1
                                              θ̂ ←                                      .
                                                                    n + ξ2
 return θ̂.

                    Figure 5: Examples where LLMs confuse superficially similar privacy reasoning patterns.


 Category 2 Question 91 (Label: No)
 Let ε > 0, δ ∈ [0, 21 ). Let F : Rd × X n → R be a function with L2 sensitivity ∆F and unique minimizer w∗ (X) =
 arg minw∈Rd F (w, X) for all X ∈ X n . The (conceptual) output perturbation algorithms A(X) = wA (X) := w∗ (X) + z with
 noise given by density
                                                      
                                                  ε∥t∥2
                                          exp   −         ,                     if δ = 0,
                                        
                                        
                                               ∆F
                                        
                                        
                                        
                                                                         
                               pz (t) ∝
                                                          ε2 ∥t∥22                        1
                                                                                            
                                          exp−                        2  , if δ ∈ 0, 2 .
                                        
                                                                        
                                        
                                                            p
                                                    2             2
                                                  ∆F cδ + cδ + ε
                                        
                                        

 where                                                  s                     
                                                                       2
                                                cδ :=       log √                .
                                                                 16δ 2 + 1 − 1
 Is A(X) (ε, δ)-differentially private?

                            Figure 6: Example Question where LLM hallucinates assumptions


output perturbation algorithm. Nevertheless, the LLMs often verify the statement as correct, implicitly assuming that
the sensitivity is taken with respect to the minimizer, as evidenced by their outputs. Over five trials on this question,
Gemini-3-Pro consistently predicts the incorrect affirmative answer, achieving 0% accuracy, which reflects a systematic
substitution of objective sensitivity for minimizer sensitivity. GPT-5.4-High performs only slightly better, with 20%
accuracy, while GPT-5.5-High reaches 40%. Gemini-3.1 and GPT-5-High achieve the best observed performance, but
still only reach 60% accuracy.

7   Conclusion and Future Work
Conclusion. We introduce DPrivBench, the first benchmark for evaluating LLM reasoning about differential privacy
across both foundational and advanced DP algorithms. Our results show that leading models handle textbook DP
mechanisms well but struggle with algorithm-specific analyses requiring careful accounting and assumption validation,
revealing a clear gap to expert-level DP reasoning.

Future work. Our work motivates improving LLM-based DP reasoning using DPrivBench as a guide. Promising next
steps include automated DP algorithm generation, which synthesizes private algorithms from non-private specifications,
and implementation-level automation, which detects and prevents privacy violations in code.


                                                                 10
                      DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


8   Acknowledgment
This work was supported in part by the ONR under grants N000142412304 and N00014-25-1-2116, by the NSF under
grants CNS 2048091, CIF-2402817 and CNS-2241100, and by the ARO-MURI under grant W911NF2110317. We
acknowledge an OpenAI security research grant for providing the necessary credits and API access to their models.




                                                       11
                      DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


References
 [1] Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang.
     Deep learning with differential privacy. 2016.
 [2] John M Abowd. The us census bureau adopts differential privacy. In Proceedings of the 24th ACM SIGKDD
     international conference on knowledge discovery & data mining, pages 2867–2867, 2018.
 [3] Aws Albarghouthi and Justin Hsu. Synthesizing coupling proofs of differential privacy. Proceedings of the ACM
     on Programming Languages, 2(POPL):1–30, 2017.
 [4] Meenatchi Sundaram Muthu Selva Annamalai, Borja Balle, Jamie Hayes, Georgios Kaissis, and Emil-
     iano De Cristofaro. The hitchhiker’s guide to efficient, end-to-end, and tight dp auditing. arXiv preprint
     arXiv:2506.16666, 2025.
 [5] Apple Blog. Understanding aggregate trends for apple intelligence using differential privacy, 2025.
 [6] Autodp Contributors. autodp: Automating differential privacy computation. https://github.com/yuxiangw/
     autodp, 2023. GitHub repository, version 0.2.3.1, accessed 2026-04-16.
 [7] Borja Balle, Gilles Barthe, and Marco Gaboardi. Privacy amplification by subsampling: Tight analyses via
     couplings and divergences. arXiv preprint arXiv:1807.01647, 2018.
 [8] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu, César Kunz, and Pierre-Yves Strub.
     Proving differential privacy in hoare logic. In 2014 IEEE 27th Computer Security Foundations Symposium, pages
     411–424. IEEE, 2014.
 [9] Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. Proving differential privacy
     via probabilistic couplings. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer
     Science, pages 749–758, 2016.
[10] Raef Bassily, Vitaly Feldman, Kunal Talwar, and Abhradeep Thakurta. Private stochastic convex optimization
     with optimal rates. arXiv preprint arXiv:1908.09970, 2019.
[11] Raef Bassily, Adam Smith, and Abhradeep Thakurta. Differentially private empirical risk minimization: Efficient
     algorithms and tight error bounds. arXiv preprint arXiv:1405.7085, 2014.
[12] Benjamin Bichsel, Samuel Steffen, Ilija Bogunovic, and Martin Vechev. Dp-sniper: Black-box discovery of
     differential privacy violations using classifiers. In 2021 IEEE Symposium on Security and Privacy (SP), pages
     391–409. IEEE, 2021.
[13] Mark Bun and Thomas Steinke. Concentrated differential privacy: Simplifications, extensions, and lower bounds.
     In Theory of cryptography conference, pages 635–658. Springer, 2016.
[14] Mark Bun and Thomas Steinke. Average-case averages: Private algorithms for smooth sensitivity and mean
     estimation. arXiv preprint arXiv:1906.02830, 2019.
[15] Clément L. Canonne, Gautam Kamath, and Thomas Steinke. The discrete gaussian for differential privacy. arXiv
     preprint arXiv:2004.00010, 2020.
[16] Mark Cesar and Ryan Rogers. Bounding, concentrating, and truncating: Unifying privacy loss composition for
     data analytics. arXiv preprint arXiv:2004.07223, 2020.
[17] Kamalika Chaudhuri, Claire Monteleoni, and Anand D Sarwate. Differentially private empirical risk minimization.
     Journal of Machine Learning Research, 12(3), 2011.
[18] Shao-Yu Chu, Yuhe Tian, Yu-Xiang Wang, and Haojian Jin. Dpcheatsheet: Using worked and erroneous llm-usage
     examples to scaffold differential privacy implementation. arXiv preprint arXiv:2509.12590, 2025.
[19] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert,
     Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve
     math word problems. arXiv preprint arXiv:2110.14168, 2021.
[20] Soham De, Leonard Berrada, Jamie Hayes, Samuel L. Smith, and Borja Balle. Unlocking high-accuracy
     differentially private image classification through scale. arXiv preprint arXiv:2204.13650, 2022.
[21] Zeyu Ding, Daniel Kifer, Thomas Steinke, Yuxin Wang, Yingtai Xiao, Danfeng Zhang, et al. The permute-and-flip
     mechanism is identical to report-noisy-max with exponential noise. arXiv preprint arXiv:2105.07260, 2021.
[22] Zeyu Ding, Yuxin Wang, Guanhong Wang, Danfeng Zhang, and Daniel Kifer. Detecting violations of differential
     privacy. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, pages
     475–489, 2018.


                                                         12
                       DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


[23] Jinshuo Dong, David Durfee, and Ryan Rogers. Optimal differential privacy composition for exponential
     mechanisms and the cost of adaptivity. arXiv preprint arXiv:1909.13830, 2019.
[24] Jinshuo Dong, David Durfee, and Ryan Rogers. Optimal differential privacy composition for exponential
     mechanisms. 2020.
[25] Jinshuo Dong, Aaron Roth, and Weijie J Su. Gaussian differential privacy. Journal of the Royal Statistical Society
     Series B: Statistical Methodology, 84(1):3–37, 2022.
[26] David Durfee and Ryan Rogers. Practical differentially private top-k selection with pay-what-you-get composition.
     2019.
[27] Cynthia Dwork and Jing Lei. Differential privacy and robust statistics. 2009.
[28] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. Calibrating noise to sensitivity in private data
     analysis. In Theory of cryptography conference, pages 265–284. Springer, 2006.
[29] Cynthia Dwork, Aaron Roth, et al. The algorithmic foundations of differential privacy. Foundations and trends®
     in theoretical computer science, 9(3–4):211–407, 2014.
[30] Jingxuan Fan, Sarah Martinson, Erik Y Wang, Kaylie Hausknecht, Jonah Brenner, Danxian Liu, Nianli Peng,
     Corey Wang, and Michael P Brenner. Hardmath: A benchmark dataset for challenging problems in applied
     mathematics. arXiv preprint arXiv:2410.09988, 2024.
[31] Natalia Figas. How meta uses privacy-enhancing technologies in advertising and analytics, 2025.
[32] Simon Frieder, Luca Pinchetti, Alexis Chevalier, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas Lukasiewicz,
     Philipp Christian Petersen, and Julius Berner. Mathematical capabilities of chatGPT. In Thirty-seventh Conference
     on Neural Information Processing Systems Datasets and Benchmarks Track, 2023.
[33] Simson Garfinkel. How we’re helping developers with differential privacy, Jan 2020.
[34] Google DeepMind. Gemini 3 pro model card, 2025.
[35] Google Developers Blog. How we’re helping developers with differential privacy, Jan 2021.
[36] Charlie Harrison and Pasin Manurangsi. Exact zcdp characterizations for fundamental differentially private
     mechanisms. arXiv preprint arXiv:2510.25746, 2025.
[37] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
     Steinhardt. Measuring mathematical problem solving with the math dataset. In J. Vanschoren and S. Yeung,
     editors, Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks, volume 1,
     2021.
[38] Kaixuan Huang, Jiacheng Guo, Zihao Li, Xiang Ji, Jiawei Ge, Wenzhe Li, Yingqing Guo, Tianle Cai, Hui Yuan,
     Runzhe Wang, Yue Wu, Ming Yin, Shange Tang, Yangsibo Huang, Chi Jin, Xinyun Chen, Chiyuan Zhang, and
     Mengdi Wang. MATH-perturb: Benchmarking LLMs’ math reasoning abilities against hard perturbations. In
     Forty-second International Conference on Machine Learning, 2025.
[39] Yichen Huang and Lin F Yang. Winning gold at imo 2025 with a model-agnostic verification-and-refinement
     pipeline. arXiv preprint arXiv:2507.15855, 2025.
[40] Haim Kaplan, Shachar Schnapp, and Uri Stemmer. Differentially private approximate quantiles. 2022.
[41] Daniel Kifer, Adam Smith, and Abhradeep Thakurta. Private convex empirical risk minimization and high-
     dimensional regression. 2012.
[42] Alex Kulesza, Ananda Theertha Suresh, and Yuyan Wang. Mean estimation in the add-remove model of differential
     privacy. arXiv preprint arXiv:2312.06658, 2023.
[43] Xuechen Li, Florian Tramèr, Percy Liang, and Tatsunori Hashimoto. Large language models can be strong
     differentially private learners. arXiv preprint arXiv:2110.05679, 2021.
[44] Hongwei Liu, Zilong Zheng, Yuxuan Qiao, Haodong Duan, Zhiwei Fei, Fengzhe Zhou, Wenwei Zhang, Songyang
     Zhang, Dahua Lin, and Kai Chen. Mathbench: Evaluating the theory and application proficiency of llms with a
     hierarchical mathematics benchmark. arXiv preprint arXiv:2405.12209, 2024.
[45] Yi Liu, Ke Sun, Bei Jiang, and Linglong Kong. Identification, amplification and measurement: A bridge to
     gaussian differential privacy. Advances in Neural Information Processing Systems, 35:11410–11422, 2022.
[46] Andrew Lowy and Meisam Razaviyayn. Output perturbation for differentially private convex optimization: Faster
     and more general. arXiv preprint arXiv:2102.04704, 2021.
[47] Min Lyu, Dong Su, and Ninghui Li. Understanding the sparse vector technique for differential privacy. Proceedings
     of the VLDB Endowment, 10(6):637–648, 2017.


                                                         13
                       DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


[48] Saeed Mahloujifar, Luca Melis, and Kamalika Chaudhuri. Auditing f -differential privacy in one run. arXiv
     preprint arXiv:2410.22235, 2024.
[49] Mathematical Association of America. American invitational mathematics examination. https://maa.org/
     maa-invitational-competitions/, 2025. Accessed: 2026-01-23.
[50] Ryan McKenna and Daniel R Sheldon. Permute-and-flip: A new mechanism for differentially private selection.
     Advances in Neural Information Processing Systems, 33:193–203, 2020.
[51] Frank McSherry. Privacy integrated queries: an extensible platform for privacy-preserving data analysis. Commu-
     nications of the ACM, 2010.
[52] Frank McSherry and Kunal Talwar. Mechanism design via differential privacy. In 48th Annual IEEE Symposium
     on Foundations of Computer Science (FOCS’07), pages 94–103. IEEE, 2007.
[53] Ilya Mironov. Rényi differential privacy. In 2017 IEEE 30th computer security foundations symposium (CSF),
     pages 263–275. IEEE, 2017.
[54] Ilya Mironov. Renyi differential privacy. arXiv preprint arXiv:1702.07476, 2017.
[55] Joseph P Near and Chiké Abuah. Programming differential privacy. URL: https://uvm, 2021.
[56] OpenAI. Introducing GPT-5, 2025.
[57] Nicolas Papernot, Shuang Song, Ilya Mironov, Ananth Raghunathan, Kunal Talwar, and Úlfar Erlingsson. Scalable
     private learning with pate. arXiv preprint arXiv:1802.08908, 2018.
[58] Nicolas Papernot and Thomas Steinke. Hyperparameter tuning with renyi differential privacy. arXiv preprint
     arXiv:2110.03620, 2021.
[59] Rachel Redberg, Yuqing Zhu, and Yu-Xiang Wang. Generalized ptr: User-friendly recipes for data-adaptive
     algorithms with differential privacy. arXiv preprint arXiv:2301.00301, 2022.
[60] Jason Reed and Benjamin C Pierce. Distance makes the types grow stronger: a calculus for differential privacy. In
     Proceedings of the 15th ACM SIGPLAN international conference on Functional programming, pages 157–168,
     2010.
[61] Aki Rehn, Linzh Zhao, Mikko A Heikkilä, and Antti Honkela. On optimal hyperparameters for differentially
     private deep transfer learning. arXiv preprint arXiv:2510.20616, 2025.
[62] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian
     Michael, and Samuel R. Bowman. GPQA: A graduate-level google-proof q&a benchmark. In First Conference on
     Language Modeling, 2024.
[63] Ryan Rogers. Deploying differential privacy in industry: Progress and learnings, 2021.
[64] Tetsuya Sato, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Shin-ya Katsumata. Approximate span liftings:
     Compositional semantics for relaxations of differential privacy. In 2019 34th Annual ACM/IEEE Symposium on
     Logic in Computer Science (LICS), pages 1–14. IEEE, 2019.
[65] Or Sheffet. Differentially private ordinary least squares. 2017.
[66] Michael Shoemate, Andrew Vyrros, Chuck McCallum, Raman Prasad, Philip Durbin, Sílvia Casacuberta Puig,
     Ethan Cowan, Vicki Xu, Zachary Ratliff, Nicolás Berrios, Alex Whitworth, Michael Eliot, Christian Lebeda, Oren
     Renard, and Claire McKay Bowen. OpenDP Library.
[67] Thomas Steinke, Milad Nasr, and Matthew Jagielski. Privacy auditing with one (1) training run. Advances in
     Neural Information Processing Systems, 36:49268–49280, 2023.
[68] Tensorflow Privacy Contributors. TensorFlow Privacy: Library for training machine learning models with
     privacy for training data. https://github.com/tensorflow/privacy, 2019. GitHub repository, accessed
     2026-04-16.
[69] Salil Vadhan. The complexity of differential privacy. In Tutorials on the Foundations of Cryptography: Dedicated
     to Oded Goldreich, pages 347–450. Springer, 2017.
[70] Zihang Xiang, Tianhao Wang, and Di Wang. Privacy audit as bits transmission:(im) possibilities for audit by one
     run. In USENIX Security, 2025.
[71] Ashkan Yousefpour, Igor Shilov, Alexandre Sablayrolles, Davide Testuggine, Karthik Prasad, Mani Malek, John
     Nguyen, Sayan Ghosh, Akash Bharadwaj, Jessica Zhao, et al. Opacus: User-friendly differential privacy library in
     pytorch. arXiv preprint arXiv:2109.12298, 2021.
[72] Danfeng Zhang and Daniel Kifer. Lightdp: Towards automating differential privacy proofs. In Proceedings of the
     44th ACM SIGPLAN Symposium on Principles of Programming Languages, pages 888–901, 2017.


                                                         14
                       DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


Contents
1   Introduction                                                                                                      1

2   Problem Set-Up                                                                                                    3
    2.1 LLM reasoning for differential privacy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    3
    2.2 Related Work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    3

3   Dataset Construction                                                                                              4
    3.1 Category 1: Mechanism-Level Instances with a Function Bank . . . . . . . . . . . . . . . . . . . . .          4
    3.2 Category 2: Algorithm-Level Instances from Research Literatures . . . . . . . . . . . . . . . . . . .         5

4   Experimental Setup and Results Overview                                                                           6

5   Main Results                                                                                                      6
    5.1 Model Performance on Category 1 Benchmark . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           7
    5.2 Model Performance on Category 2 Benchmark . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           7

6   More Analytic Results and Case Study                                                                              8
    6.1 Context-Augmented DP Reasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        8
    6.2 Reasoning Plausibility and Soundness Beyond Binary Evaluation . . . . . . . . . . . . . . . . . . . .         9
    6.3 Case Study for Failure Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      9

7   Conclusion and Future Work                                                                                       10

8 Acknowledgment                                                                                                     11

A Privacy Guarantee and References                                                                                   16
  A.1 Privacy guarantee for Category 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     16
  A.2 References for Category 2 questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      17

B Taxonomy of Error Patterns for Negative Questions in Category 2                                                    17

C Experiment Details                                                                                                 17
  C.1 Model Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    17
  C.2 Experiment details for evaluation of Category 1 and Category 2 . . . . . . . . . . . . . . . . . . . . .       18
  C.3 Experiment details for Augmented QA prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         18
      C.3.1 QA prompt augmented with relevant theorems . . . . . . . . . . . . . . . . . . . . . . . . .             18
      C.3.2 QA prompt with one-shot proof template . . . . . . . . . . . . . . . . . . . . . . . . . . . .           18
  C.4 Experiment details for analyzing LLMs’ responses . . . . . . . . . . . . . . . . . . . . . . . . . . .         19
      C.4.1 Prompt for judging LLMs’ response . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          19
      C.4.2 Description of Fine-Grained Reasoning Assessment Labels . . . . . . . . . . . . . . . . . . .            20
      C.4.3 Calculation for plausibility and soundness scores . . . . . . . . . . . . . . . . . . . . . . . .        20

D Accuracy per topic for Category 2                                                                                  20

E Benchmark Examples                                                                                                 20

F Examples of Fine-Grained Error Analysis with GPT-5.4-High as Judge                                                 22

G Paraphrasing experiment of Category 2                                                                              28
  G.1 Paraphrasing Set-up . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    28
  G.2 Example of Paraphrased Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       28




                                                          15
                                DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


A    Privacy Guarantee and References
A.1 Privacy guarantee for Category 1
In this section, we state formal proof for all six mechanisms use in Category 1. Through the question statement in
Category 1, we use replace-one neighbouring relationship.
Theorem A.1 (Laplace Mechanism [28]). Let f : X n → Rd be a function with ℓ1 -sensitivity ∆1 (f ) := max′ ∥f (X) −
                                                                                                          X∼X
f (X ′ )∥1 . The Laplace mechanism defined as follow satisfies ε-DP:
                                                                                     
                                                                       i.i.d. ∆1 (f )
                                         M(X) = f (X) + Z,          Zi ∼ Lap            .
                                                                                ε
Theorem A.2 (zCDP guarantee of Gaussian Mechanism [13]). Let f : X n → Rd be a function with ℓ2 -sensitivity
∆2 (f ) := max′ ∥f (X) − f (X ′ )∥2 . The Gaussian mechanism defined as follow satisfies ρ-zero Concentrated Differen-
             X∼X
tial Privacy (zCDP):
                                                                           ∆2 (f )2
                                                                                      
                                                                      i.i.d.
                                        M(X) = f (X) + Z,        Zi ∼ N 0,                  .
                                                                             2ρ
Theorem A.3 (GDP guarantee of Gaussian Mechanism [25]). Let f : X n → Rd be a function with ℓ2 -sensitivity
∆2 (f ) := max′ ∥f (X) − f (X ′ )∥2 . The Gaussian mechanism defined as follow satisfies µ-Gaussian Differential
              X∼X
Privacy (GDP):
                                                                           ∆2 (f )2
                                                                                      
                                                                      i.i.d.
                                        M(X) = f (X) + Z,        Zi ∼ N 0,                  .
                                                                            µ2

Another type of question in Category 1 is report noisy max[29] for private selection, we provide a general template
in Algorithm 2. In particular, when instantiated with exponential noise, the algorithm is called the permute and flip
[50, 21]. When instantiated with Gumbel noise, the algorithm is the famous exponential algorithm [52].

Algorithm 2: R EPORT N OISY M AX
Input :Dataset X; score functions {uj (·)}m     i=1 with sensitivity ∆ (w.r.t. same neighboring relation); noise
         distribution P
Output :Index î ∈ {1, . . . , m} of the selected item.
for i = 1 to m do
    si ← ui (X)
    Sample ηi ∼ P
    s̃i ← si + ηi
î ← arg      max         s̃i
            i∈{1,...,m}
return î

Before stating the privacy guarantee of private selection mechanisms used in Category 1, we introduce definition of
noises:
Definition A.4 (Exponential Distribution). A random variable X is said to follow an exponential distribution with
parameter λ > 0, denoted by X ∼ Exp(λ), if it has probability density function
                                                       1 −x/λ
                                                          e    , x ≥ 0,
                                            fX (x) = λ
                                                        0,        x < 0.

Definition A.5 (Gumbel Distribution). A random variable X is said to follow Gumbel(α) distribution if it has
probability density function
                                              1     x        x 
                                  fX (x) = exp − − exp −             ,     x ∈ R.
                                             α        α         α
Theorem A.6 (Privacy guarantee of report noisy max with Laplace noise [29]). Suppose noise distribution P follows
Laplace 2∆ ε , then Algorithm 2 satisfies ε-DP
Theorem A.7 (Privacy      guarantee of report noisy max with Exponential noise [21]). Suppose noise distribution P
follows Exp 2∆
                 
               ε   , then Algorithm 2 satisfies ε-DP.
Theorem A.8(Privacy guarantee of report noisy max with Gumbel noise [21]). Suppose noise distribution P follows
Gumbel 2∆   ε , then Algorithm 2 satisfies ε-DP.



                                                               16
                          DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


A.2   References for Category 2 questions
In addition to DP textbook references [29, 69], we include in Table 6 the research papers used to construct and justify
the Category 2 questions.


                        Table 6: Reference for Category 2 questions (grouped by subject and topic).
 Subject                           Topic                                     Reference
                                   Accounting                                [54, 25, 16, 21, 45, 36, 24, 26]
                                   Amplification by Subsampling              [7]
 Accounting and Composition        Parallel Composition                      [51]
                                   SVT                                       [47]
                                   Sequential or Adaptive Composition        [13, 54, 15, 16]
                                   DP-GD                                     [11, 25]
                                   DP-OLS                                    [65]
                                   Hyperparameter-tuning                     [58]
                                   PATE                                      [57]
 DP-ML
                                   dp-adam                                   [43]
                                   dp-sgd                                    [1, 20, 61]
                                   objective perturbation                    [10, 41, 17]
                                   output perturbation                       [46]
                                   DP selection                              [23, 24]
 DP-statistics                     mean estimation                           [42]
                                   quantile                                  [40]
                                   PTR                                       [59, 27]
 Data-Adaptive
                                   Smooth_sensitivity                        [14]



B     Taxonomy of Error Patterns for Negative Questions in Category 2
Table 7 summarizes the error taxonomy for questions with negative labels in Category 2.


                                             Table 7: Error taxonomy in Category 2
 Error pattern                             Core characterization

 Overclaiming guarantee                    Starts from a valid result but claims a strictly stronger privacy guarantee than what the
                                           theorem or mechanism actually supports.
 Broken implementation step                The overall algorithm looks standard, but a key implementation detail is altered in a way
                                           that breaks privacy.
 Noise miscalibration                      Noise is added, but not at the level required by the true sensitivity or correct accounting.
 Assumption mismatch                       The claim changes the assumptions, adjacency relation, norm bound, or sampling model
                                           while keeping the statement superficially similar.
 non-privatized data-dependent com-        A control-flow, hyperparameter, initialization, or stopping rule depends on private data
 ponent                                    without being privatized.
 Public/private boundary mistake           Quantities such as dataset size n or N are treated as public when they are private under
                                           the stated neighboring relation.
 Conceptual impossibility                  The claim is false at the conceptual level, such as invalid conversions between DP notions
                                           or privacy guarantees that are impossible in general.
 Natural mistake                           The error originates in the literature



C     Experiment Details
C.1   Model Details
We provide version information of models in the following table:


                                                                  17
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy



                                          Table 8: Version information of Models
               Model                    Provider                       Version/Link/Release-date

               Claude-Sonnet-4.5       Anthropic                          September 29, 2025
               Claude-Opus-4.5         Anthropic                          November 24, 2025
               Gemini-2.5-Flash     Google DeepMind                          June 17, 2025
               Gemini-3-Pro         Google DeepMind                       November 18, 2025
               Gemini-3.1-Pro       Google DeepMind                        Feburary 19, 2026
               GPT-5-High               OpenAI                              August 7, 2025
               GPT-5-Minimal            OpenAI                              August 7, 2025
               GPT-5.4-High             OpenAI                              March 5, 2026
               GPT-5.5-High             OpenAI                              April 24, 2026

               DeepSeek-R1           Open-sourced          https://huggingface.co/deepseek-ai/DeepSeek-R1
               DeepSeek-V3.1-chat    Open-sourced         https://huggingface.co/deepseek-ai/DeepSeek-V3.1
               Qwen3-30-Instruct     Open-sourced     https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507
               Qwen3-30-Think        Open-sourced     https://huggingface.co/Qwen/Qwen3-30B-A3B-Thinking-2507
               Goedel-Prover-V2      Open-sourced      https://huggingface.co/Goedel-LM/Goedel-Prover-V2-32B



C.2 Experiment details for evaluation of Category 1 and Category 2
For each question, we repeat the experiment with five random seeds. The prompt we use is as follows:
   QA prompt for testing Category 1 and Category 2

   {Question} Please provide some explanations or deriviations first and then provide your final answer ‘yes‘ or
   ‘no‘ inside a Latex boxed format ‘\\boxed{}‘

C.3 Experiment details for Augmented QA prompt
C.3.1 QA prompt augmented with relevant theorems
   QA prompt augmented with relevant theorems

   {Question description}
   You may use the following theorems or definitions if applicable.
   [THEOREM] {Theorem} [/THEOREM]
   Please provide explanations or derivations first. If you use any theorem or definition, cite it by its ID in the
   reasoning. The very last line of your response must be exactly ‘\\boxed{yes}‘ or ‘\\boxed{no}‘. Do not
   include citations or any other text on the last line.

C.3.2   QA prompt with one-shot proof template
   QA template for one-shot reasoning on LaplaceRNM task

   Below is an example of the question.

   Example Question:
   For each item j ∈ F , define a score sj (D) with sensitivity 1. Consider the mechanism that samples independent
   noise Zj Laplace(2/ϵ) for each j and outputs argmaxj (sj (D) + Zj ).

   Claim: This mechanism satisfies ϵ-differential privacy.

   Now answer the following question.

   {Question description}

   Please provide some explanations or deriviations first and then provide your final answer ‘yes‘ or ‘no‘ inside a
   Latex boxed format ‘\\boxed{}‘.




                                                              18
                          DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


C.4     Experiment details for analyzing LLMs’ responses


For the judge LLM, we use GPT-5.4 with high reasoning effort.




C.4.1     Prompt for judging LLMs’ response


      Prompt for judging LLM response

      You are an expert evaluator of differential privacy reasoning.

      Evaluate whether the model response gives a mathematically reasonable argument for the stated problem.
      Do not require a fully formal proof. Minor omissions are acceptable if the main idea is correct and the
      conclusion is supported.

      Use the ground-truth label only to check whether the response’s final conclusion matches the benchmark.
      Hints are optional reference information. The response does not need to use the hints or follow the same
      solution path. A response can be correct if it gives a different mathematically valid argument.

      Classify the response into one category:

   - "correct": sound and sufficient reasoning.
   - "minor_gap": mostly correct with small omissions or imprecision.
   - "correct_direction_fixable": right high-level idea, but missing or mistaken key details that are locally fixable.
   - "fatal_error": core mathematical error that invalidates the reasoning.
   - "unclear_or_insufficient": too vague or lacks substantive reasoning.

   Set reasoning_correct as: - "yes" for correct or minor_gap
   - "partial" for correct_direction_fixable
   - "no" for fatal_error or unclear_or_insufficient

   Return exactly one JSON object:
   {
   "reasoning_correct": "yes" or "partial" or "no",
   "error_category": "correct" or "minor_gap" or "correct_direction_fixable" or "fatal_error" or "un-
   clear_or_insufficient",
   "error_summary": "Briefly summarize the main issue, or state why the reasoning is acceptable.",
   "detailed_explanation": "2-5 sentences explaining the assessment. Do not penalize the response for not using
   the hints if its alternative reasoning is valid."
   }

   Problem:
   {problem}

   Ground-truth answer:
   {label}

   Hints, if available:
   {hints}

   Model response:
   {response}



                                                            19
                         DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy


C.4.2    Description of Fine-Grained Reasoning Assessment Labels

                 Error Category                          Description
                 correct                         sound and sufficient reasoning
                 minor_gap                       mostly correct with small omissions or imprecision
                 correct_direction_fixable       right high-level idea, but missing or mistaken key
                                                 details that are fixable
                 fatal_error                     core mathematical error that invalidates the reason-
                                                 ing
                 unclear_or_insufficient         too vague or lacks substantive reasoning
                              Table 9: Description of reasoning assessment labels




C.4.3    Calculation for plausibility and soundness scores
Define shorthand for labels: C : correct, M : minor_gap, F : correct_direction_fixable. The Soundness and
Plausibility are calculated as follow:

                          #{answer correct ∧ C} + #{answer correct ∧ M }
             Soundness =
                                        #{answer correct}
                                                                                                                             (1)
                          #{answer correct ∧ C} + #{answer correct ∧ M } + #{answer correct ∧ F }
           Plausibility =
                                                    #{answer correct}


D   Accuracy per topic for Category 2

Table 10: The performance of GPT-5-High and Gemini-3-Pro on Category 2 by topics. We sort the topics by the mean
accuracy of two models.
 Topic                                             Gemini-3-Pro    Gemini-3.1-Pro   GPT-5.4-High   GPT-5.5-High   Avg Accuracy
 DP Adam                                                   1.00              1.00           1.00           1.00           1.00
 Quantile Estimation                                       1.00              1.00           1.00           1.00           1.00
 Privacy Accounting                                        0.92              1.00           1.00           0.98           0.97
 Private Selection                                         0.80              1.00           1.00           1.00           0.95
 Privacy Amplification via Subsampling                     1.00              1.00           0.96           1.00           0.94
 Sparse Vector Technique                                   0.92              0.95           1.00           1.00           0.94
 DP Gradient Descent                                       0.92              0.92           0.92           0.88           0.92
 Sequential/Adaptive Composition                           0.91              0.97           0.94           0.97           0.90
 Mean Estimation                                           0.87              0.85           0.87           0.87           0.86
 DP Linear Regression                                      0.80              0.93           0.80           0.83           0.85
 Objective Perturbation                                    0.80              0.80           0.70           0.90           0.80
 Parallel Composition                                      0.71              0.84           0.77           0.86           0.80
 DP Stochastic Gradient Descent                            0.78              0.78           0.82           0.76           0.79
 DP Hyperparameter Optimization                            0.60              0.70           0.67           1.00           0.75
 Propose–Test–Release (PTR)                                0.70              0.75           0.85           0.75           0.74
 Output Perturbation                                       0.33              0.87           0.40           0.67           0.57
 Private Aggregation of Teacher Ensembles (PATE)           0.67              0.60           0.40           0.60           0.52
 Smooth Sensitivity                                        0.33              0.33           0.33           0.33           0.33




E   Benchmark Examples
Example of the positive question in category 2: Suppose that for all z ∈ Z, ℓ(·, z) is twice-differentiable, and
the rank of its Hessian ∇2 ℓ(w, z) at any w ∈ W is at most 1. Also assume that the smoothness parameter satisfies
β ≤ εnλ. Is the following algorithm(ε, δ)-differentially private?


                                                                  20
                        DPrivBench: Benchmarking LLMs’ Reasoning for Differential Privacy



Algorithm 3: AObjP : Objective Perturbation
Input: Private dataset S = (z1 , . . . , zn ) ∈ Z n , L-Lipschitz, β-smooth, convex loss function ℓ, convex set
       W ⊆ Rd , privacy parameters ε ≤ 1, δ ≤ 1/n2 , regularization parameter λ.
                                      10L2 log(1/δ)
1: Sample G ∼ N (0, σ 2 Id ), where σ 2 =           ;
                                            ε2
                                     ⟨G, w⟩                             1 Pn
2: return ŵ = arg minw∈W L̂(w; S) +         + λ∥w∥2 , where L̂(w; S) ≜       ℓ(w, zi );
                                        n                               n i=1

Example of the negative question (assumption perturbation) in category 2: Suppose that for all z ∈ Z, ℓ(·, z) is
twice-differentiable, and the rank of its Hessian ∇2 ℓ(w, z) at any w ∈ W is at most 1. Also assume that the smoothness
parameter satisfies β ≤ εnλ. Is the following algorithm(ε, δ)-differentially private?

Algorithm 4: AObjP : Objective Perturbation
Input: Private dataset S = (z1 , . . . , zn ) ∈ Z n , L-Lipschitz, β-smooth,   loss function ℓ, privacy parameters
                                                                             convex
                       2
       ε ≤ 1, δ ≤ 1/n , regularization parameter λ.
                                      10L2 log(1/δ)
1: Sample G ∼ N (0, σ 2 Id ), where σ 2 =           ;
                                            ε2
                                     ⟨G, w⟩                             1 Pn
2: return ŵ = arg minw∈W L̂(w; S) +         + λ∥w∥2 , where L̂(w; S) ≜       ℓ(w, zi );
                                        n                               n i=1

Example of the negative question (algorithm perturbation) in category 2: Suppose that for all z ∈ Z, ℓ(·, z) is
twice-differentiable, and the rank of its Hessian ∇2 ℓ(w, z) at any w ∈ W is at most 1. Also assume that the smoothness
parameter satisfies β ≤ εnλ. Is the following algorithm(ε, δ)-differentially private?

Algorithm 5: AObjP : Objective Perturbation
Input: Private dataset S = (z1 , . . . , zn ) ∈ Z n , L-Lipschitz, β-smooth, convex loss function ℓ, convex set
       W ⊆ Rd , privacy parameters ε ≤ 1, δ ≤ 1/n2 , regularization parameter λ.
                                      10L2 log(1/δ)
1: Sample G ∼ N (0, σ 2 Id ), where σ 2 =           ;
                                            ε2
                                     ⟨G, w⟩ λ                            1 Pn
2: return ŵ = arg minw∈W L̂(w; S) +         + 2 ∥w∥2 , where L̂(w; S) ≜       ℓ(w, zi );
                                        n                                n i=1

Example of the negative question (conclusion perturbation) in category 2: Suppose that for all z ∈ Z, ℓ(·, z) is
twice-differentiable, and the rank of its Hessian ∇2 ℓ(w, z) at any w ∈ W is at most 1. Also assume that the smoothness
parameter satisfies β ≤ εnλ. Is the following algorithm(ε/2, δ)-differentially private?

Algorithm 6: AObjP : Objective Perturbation
Input: Private dataset S = (z1 , . . . , zn ) ∈ Z n , L-Lipschitz, β-smooth, convex loss function ℓ, convex set
       W ⊆ Rd , privacy parameters ε ≤ 1, δ ≤ 1/n2 , regularization parameter λ.
                                      10L2 log(1/δ)
1: Sample G ∼ N (0, σ 2 Id ), where σ 2 =           ;
                                            ε2
                                     ⟨G, w⟩                             1 Pn
2: return ŵ = arg minw∈W L̂(w; S) +         + λ∥w∥2 , where L̂(w; S) ≜       ℓ(w, zi );
                                        n                               n i=1




                                                            21
F     Examples of Fine-Grained Error Analysis with GPT-5.4-High as Judge
We include examples of judge results for responses generated by GPT-5-High. GT denotes the ground truth label, Pred
denotes the label predicted by the response LLM.


    Q 18      GT: Yes (1)             Pred: Yes (1)      Correct ✓ correct


    DP-statistics ▷ DP selection: expoMech
    The pseudocode below implements the exponential mechanism. Does this implementation ensure ε-differential
    privacy under the add/remove neighboring relationship?


Algorithm 7: Exponential Mechanism
                                                                                                   Pn
Input : Dataset D = {zi }ni=1 ; candidate set Y ; utility (score) function q(D, y) =                  i=1 1{zi = y}; privacy
        parameter ε
Output : Selected item ŷ ∈ Y sampled by the exponential mechanism
for y ∈ Y do
    py ← P ′ exp(ε q(D,y))
                exp(ε q(D,y ′ ))
              y ∈Y

Sample ŷ ∼ Multinomial(1; {py }y∈Y )
return ŷ

Comments from metadata

                                                                              
                                                                          εq
    For a monotone query q, the exponential mechanism with py ∝ exp       ∆q
                                                                                   satisfies ε-DP [24].


Model Response (gpt-5-high)
 Short answer with context

 - The exponential mechanism with generic utility u ensures epsilon-DP when it samples with probability proportional to exp((
      epsilon u(D,y))/(2Deltau)), where Deltau is the global sensitivity. The factor 1/2 is needed in general because both
      the numerator term and the normalizing constant can each contribute a factor exp(epsilon/2) in the privacy ratio.

 - In your pseudocode, the utility is the count q(D,y) = sumi 1{zi = y}. Under add/remove adjacency, this utility is monotone
       with respect to adding a record: if D’ = D union {y*}, then q(D’,y) = q(D,y) + 1{y = y*} (no utility decreases). This
       monotonicity allows a tighter analysis that eliminates the extra factor 1/2.

 Derivation for the add/remove case

 Let D’ = D union {y*}. Define ZD = sumy exp(epsilon q(D,y)) and ZD’ = sumy exp(epsilon q(D’,y)).

 - Because q(D’,y) = q(D,y) + 1{y=y*}, we have
   ZD’ = ZD + (e^epsilon - 1) exp(epsilon q(D,y*)) = ZD * [1 + (e^epsilon - 1) wD(y*)],
   where wD(y*) = exp(epsilon q(D,y*))/ZD in [0,1]. Hence 1 <= ZD’/ZD <= e^epsilon.

 - For y = y*, the ratio of output probabilities is
   pD(y*)/pD’(y*) = e^{-epsilon} * (ZD’/ZD) in [e^{-epsilon}, 1] subseteq [e^{-epsilon}, e^{epsilon}].

 - For y != y*, the ratio is
   pD(y)/pD’(y) = ZD’/ZD in [1, e^{epsilon}] subseteq [e^{-epsilon}, e^{epsilon}].

 Thus for every y, e^{-epsilon} <= pD(y)/pD’(y) <= e^{epsilon}. Summing over any subset S subseteq Y preserves the bound, so
      the mechanism satisfies epsilon-differential privacy under add/remove adjacency.

 Remarks
 - For substitution (replace-one) adjacency or for non-monotone utilities, the same code would only be 2epsilon-DP; to get
      epsilon-DP in that generality you need the standard scaling exp((epsilon q(D,y))/(2Deltaq)).
 - The argument assumes the candidate set Y is fixed (data-independent).

 Final answer:
 \boxed{yes}


Judge Assessment (gpt-5.4)
  Reasoning correct                                                                               Category: Correct
  Summary: The response gives a valid monotonicity-based privacy argument showing that the unscaled exponential
  mechanism is epsilon-DP for this count utility under add/remove adjacency.
  Detail: The key observation is correct: when one record is added, only the score of the matching item increases
  by 1, so the utility is monotone and the partition function changes by at most a factor of e^epsilon. Using this, the
  response correctly bounds the pointwise output-probability ratios for both the affected y* and all other outputs by
  e^epsilon (and below by e^{-epsilon}), which is sufficient for epsilon-DP. The note that the usual 1/2 factor is
  needed only in the general non-monotone or replace-one setting is also mathematically appropriate.




  Q 35        GT: No (0)             Pred: No (0)             Correct ✓ correct


  DP-ML ▷ DP-GD
  The following is an implementation of differentially private gradient descent (DP-GD). Does this implementation
  satisfy µ-Gaussian differential privacy under the add/remove neighboring relationship (assume number of samples
  n is public information)?


Algorithm 8: DP-GD with Gaussian Noise
                                                                                                           −1
Input : Dataset D = {zi }ni=1 ; loss ℓ(θ; z); initial parameter θ0 ∈ Rd ; iterations T ; step sizes {ηt }Tt=0 ;
        clipping norm C > 0; target gaussian DP µ; Stopping threshold τ
Output :Final parameter θT
for t = 0, . . . , T − 1 do
    for i = 1, . . . , n do
        gi ← ∇θ ℓ(θt ; zi )
        ĝi ← gi · min 1, ∥gCi ∥2
                                  
              P               √    
                    n
    g̃t ← n1        i=1 ĝi +
                              C 2T
                               µ ξt ,       ξt ∼ N (0, Id )
   θt+1 ← θt − ηt g̃t
   // running above-threshold
                           √
     Pn
   if i=1 ℓ(θt+1 ; zi ) + C µ2T ξt ≥ τ then
      break
return θt+1

Comments from metadata

  The noise added to the threshold is not properly calibrated to its sensitivity.

Model Response (gpt-5-high)
 Short answer: No, because the early-stopping "above-threshold" check is not privatized correctly.

 Explanation/derivation:

 - GDP basics. A Gaussian mechanism that outputs f(D) + N(0, sigma^2 I) with L2-sensitivity Delta under add/remove adjacency
      is exactly mu-GDP with mu = Delta/sigma. For a sequence of (possibly adaptive) Gaussian mechanisms with mu1, ..., muT,
       composition in GDP gives mutotal = sqrt(sumt mut^2).

 - Gradient step (ignoring the stopping rule). The per-iteration query is the averaged, per-example-clipped gradient:
   f_t(D) = (1/n) sumi hat g_i, with ||hat g_i||2 <= C.
   Under add/remove adjacency, the L2-sensitivity is Deltagrad = C/n. The code adds Gaussian noise with std to the average
      equal to sigmagrad = (Csqrt(2T))/(mu n). Hence the per-iteration GDP parameter is mut = Deltagrad/sigmagrad = mu/sqrt
      (2T). Composing T iterations gives mugrad,total = sqrt(T*(mu^2/(2T))) = mu/sqrt2 <= mu. So the gradient part alone
      would be at least as private as mu-GDP (indeed, slightly stronger).

 - Early-stopping "above-threshold" step breaks privacy:



                                                                 23
  1) The statistic being tested is S_t(D) = sumi l(theta_{t+1}; z_i). Under add/remove adjacency, the sensitivity of S_t is
     DeltaS = supz |l(theta; z)|, which is unbounded unless the loss is explicitly bounded or clipped. The code does not
     bound or clip the loss.
  2) The noise scale used for the threshold test is tied to the gradient clipping constant C, which has no relation to
     DeltaS. Calibrating to C does not protect the sum of losses.
  3) The same noise sample xi_t is (apparently) reused for both the vector-valued gradient noise and the scalar threshold
     test, which is both dimensionally inconsistent and, even if made consistent, undermines clean composition accounting;
     at minimum one needs fresh, independently drawn noise for the test, calibrated to the sensitivity of S_t and budgeted
     in composition.

Because the stopping condition depends directly on the (non-privatized) sum of losses, the stopping time can leak
     information about the presence/absence of a point. Since the final output depends on whether the loop stops, this
     additional data access is not protected by "post-processing" closure (post-processing only applies to functions of DP
     outputs, not fresh queries to the data). Therefore, as written, the overall algorithm does not satisfy mu-GDP.

If the above-threshold step were removed, or replaced by a properly privatized AboveThreshold mechanism with bounded loss
     sensitivity and independently calibrated noise accounted for in composition (ensuring mugrad,total^2 + muthresh,total
     ^2 <= mu^2), then one could achieve mu-GDP. But in its current form, it does not.

\boxed{No}


Judge Assessment (gpt-5.4)


  Reasoning correct                                                                              Category: Correct
  Summary: The response correctly identifies that the gradient updates alone can be made mu-GDP under
  composition, but the early-stopping loss-threshold query is not properly privatized because its noise is not
  calibrated to that query’s sensitivity.
  Detail: The response gives a mathematically reasonable privacy analysis of the clipped-gradient Gaussian
  mechanism: under add/remove adjacency the averaged clipped gradient has sensitivity C/n, and the stated noise
  scale yields a per-step GDP parameter that composes to at most mu for the gradient part. It then correctly notes
  that the stopping rule performs an additional data-dependent query, namely the sum of losses, and this is not
  protected by post-processing since it accesses the dataset anew. The key flaw is that the threshold-test noise is
  tied to the gradient clipping constant C rather than the sensitivity of the loss sum (which may even be unbounded
  without a bounded/clipped loss assumption), so the overall algorithm as written does not satisfy mu-GDP.




 Q 92        GT: No (0)             Pred: Yes (1)          Fatal Error × wrong


  DP-ML ▷ output perturbation
  Let ε > 0, δ ∈ [0, 12 ). Let F : Rd × X n → R be a function with L2 sensitivity ∆F and unique minimizer
  w∗ (X) = arg minw∈Rd F (w, X) for all X ∈ X n . The (conceptual) output perturbation algorithms A(X) =
  wA (X) := w∗ (X) + z with noise given by density
                                                      
                                                 ε∥t∥2
                                        
                                        exp −
                                                         ,                  if δ = 0,
                                        
                                                 ∆F
                               pz (t) ∝                                !
                                                         ε∥t∥2
                                                                          , if δ ∈ (0, 21 )
                                        
                                        exp −
                                        
                                                           p
                                                 ∆F (cδ + c2δ + ε)
              s                        
                                2
  where cδ := log √                       . Is A(X) (ε, δ)-differentially private?
                          16δ 2 + 1 − 1

Comments from metadata


  (1) Not necessarily: adding Laplace/Gaussian noise to w∗ (X) is (ε, δ)-DP only if the noise is calibrated to the L2 -sensitivity
  of w∗ (X), which does not follow from assuming F has sensitivity ∆F without additional stability/regularity conditions; (2)
  the density for δ ∈ (0, 1/2) is not correct.



                                                                24
Model Response (gpt-5-high)
Explanation/derivation:
- Let the "query" be q(X) := w*(X). Interpret DeltaF as the L2 global sensitivity of this query: for all neighboring
     datasets X, X’, we have ||q(X) - q(X’)||2 <= DeltaF.
- Consider additive noise Z with density galpha(z) propto exp(-alpha ||z||2), and output A(X) = q(X) + Z. For any y in Rd,
  log(p(y|X)/p(y|X’)) = -alpha(||y - q(X)||2 - ||y - q(X’)||2) <= alpha ||q(X) - q(X’)||2 <= alpha DeltaF,
  where we used the triangle inequality and the fact the normalizing constant cancels. Hence A is (alpha DeltaF, 0)-DP.
- delta = 0 case: choosing alpha = epsilon/DeltaF gives (epsilon, 0)-DP (the K-norm/L2-Laplace mechanism).
- delta in (0, 1/2) case: the proposed density uses alpha = epsilon/[DeltaF(cdelta + sqrt(cdelta^2 + epsilon))], so the
     mechanism is (epsilon’, 0)-DP with epsilon’ = alpha DeltaF = epsilon/(cdelta + sqrt(cdelta^2 + epsilon)) <= epsilon.
     Pure DP with parameter epsilon’ <= epsilon trivially implies (epsilon, delta)-DP.

Remark: If DeltaF is meant as the L2 sensitivity of q(X) = w*(X), the above holds. If instead DeltaF referred only to
     sensitivity of the scalar-valued objective F(*, X) while the argmin’s sensitivity is unbounded, no finite-noise DP
     guarantee follows. Under the usual interpretation (DeltaF is the sensitivity of w*), the mechanism is indeed (epsilon,
      delta)-DP; in fact it is strictly stronger (pure DP) in both cases.

Final answer:
\boxed{\,\text{Yes}\,}


Judge Assessment (gpt-5.4)

  Reasoning incorrect                                                                       Category: Fatal Error
  Summary: The response incorrectly treats Delta_F as the L2 sensitivity of the argmin query w*(X), but the
  problem only assumes sensitivity of the objective F, which does not imply bounded sensitivity of w*(X).
  Detail: The main proof would be valid for additive L2-Laplace noise if Delta_F were a bound on ||w*(X)-
  w*(X’)||_2 for neighboring datasets. However, that is not what the problem states: sensitivity of F(w,X) does
  not by itself control the sensitivity of its minimizer, so the DP argument does not apply. The response even
  acknowledges this caveat but then answers "Yes" anyway, which is incompatible with the stated assumptions. It
  also does not address that the proposed delta>0 calibration is not the standard correct one.




 Q 95       GT: No (0)            Pred: No (0)          Minor Gap ✓ correct


  Accounting and Composition ▷ Parallel Composition
  We aim to release a histogram whose bins are n data-independent but potentially non-disjoint intervals. If we add
  independent noise drawn from Lap(2/ε) to each bin, does the resulting mechanism satisfy ε-differential privacy
  under the replace-one neighboring relationship?

Comments from metadata

  Since the histogram bins may be non-disjoint, replacing a single data point can affect the counts of more than two bins.
  Consequently, adding Laplace noise with scale 2/ε may not be sufficient to guarantee ε-differential privacy.

Model Response (gpt-5-high)
Let I1,...,In be fixed (data-independent) intervals, possibly overlapping. Let h(D) in R^n be the histogram vector with
     coordinates hi(D) = #{x in D : x in Ii}. For replace-one neighbors D and D’ that differ by changing one record from x
     to y, the change in the histogram is
h(D) - h(D’) = (1{xinIi} - 1{yinIi})i=1..n,
so
||h(D) - h(D’)||1 = sumi |1{xinIi} - 1{yinIi}| = |Sx Delta Sy|,
where Sx = {i : x in Ii} and Delta denotes symmetric difference.

Let c = maxz |Sz| be the maximum number of bins any single point belongs to (the overlap multiplicity). Then
||h(D) - h(D’)||1 <= |Sx| + |Sy| <= 2c,
and this bound can be tight. For disjoint bins, c = 1 and the L1 sensitivity under replace-one is Delta1 = 2. For
     overlapping bins with c > 1, the global sensitivity Delta1 can exceed 2 (e.g., if some x lies in r > 1 bins and y in
     none, then ||h(D) - h(D’)||1 = r).

The Laplace mechanism that adds i.i.d. Lap(b) noise per coordinate achieves epsilon’ = Delta1/b differential privacy. With b
      = 2/epsilon, the achieved privacy is epsilon’ = (epsilon Delta1)/2. If Delta1 > 2 (which occurs whenever c > 1 in the
      worst case), then epsilon’ > epsilon, so the mechanism is not epsilon-differentially private.



                                                            25
A simple counterexample: take three identical intervals I1 = I2 = I3 = [-1,1]. Replacing a single record at x = 0 with y =
     10 changes three coordinates by 1, so Delta1 = 3. Adding Lap(2/epsilon) yields epsilon’ = 3epsilon/2 > epsilon,
     violating epsilon-DP.

Therefore, adding Lap(2/epsilon) noise per bin guarantees epsilon-DP only if the bins are disjoint (c = 1). In general with
     overlapping bins, it does not.

\boxed{\text{no}}



Judge Assessment (gpt-5.4)


  Reasoning correct                                                                              Category: Minor Gap
  Summary: The response correctly argues via L1 sensitivity and gives a valid counterexample showing
  Lap(2/epsilon) can fail for overlapping bins, though it slightly overstates that disjointness is necessary in all cases.
  Detail: The main reasoning is sound: for replace-one neighbors, the histogram change is the symmetric difference
  of bin-membership vectors, so overlapping intervals can make the L1 sensitivity exceed 2. Since the Laplace
  mechanism with coordinatewise Lap(2/epsilon) only guarantees epsilon-DP when the global L1 sensitivity is at
  most 2, the explicit example with three identical intervals gives sensitivity 3 and therefore violates epsilon-DP.
  The only imprecision is the statement that the mechanism guarantees epsilon-DP only if bins are disjoint; over-
  lapping bins can still have sensitivity at most 2 in some special cases. But for the problem’s yes/no claim, the
  counterexample is enough, so the conclusion is correct.




 Q 96        GT: No (0)            Pred: No (0)         Correct ✓ correct


  Accounting and Composition ▷ Parallel Composition
  We aim to release a histogram whose bins are n disjoint, data-independent intervals. If we add independent
  noise drawn from Lap(1/ε) to each bin, does the resulting mechanism satisfy ε-differential privacy under the
  replace-one neighboring relationship?


Comments from metadata


  The sensitivity for releasing the histogram under the replace-one neighboring relation is 2. Therefore, adding independent
  Laplace noise with scale ε to each histogram bin only guarantees 2ε-differential privacy.


Model Response (gpt-5-high)
Let h(D) in R^n be the histogram counts for n fixed, disjoint bins. Under the replace-one neighboring relationship, a single
      record can move from one bin to another, so exactly one bin decreases by 1 and another increases by 1. Hence the L1-
     sensitivity of the vector-valued query is
Delta1(h) = max_{D~D’} ||h(D) - h(D’)||_1 = 2.

The vector Laplace mechanism that adds independent Lap(b) to each coordinate satisfies epsilon-DP when b = Delta1/epsilon.
     With b = 1/epsilon, the joint density of the mechanism is
p(y | D) propto exp(-epsilon ||y - h(D)||_1),
and for neighboring D, D’:
p(y | D) / p(y | D’) <= exp(epsilon ||h(D) - h(D’)||_1) <= exp(2epsilon).

Thus the mechanism is 2epsilon-DP (not epsilon-DP) under replace-one adjacency. To achieve epsilon-DP under replace-one, one
      would need Lap(2/epsilon) noise per bin.

\boxed{\text{no}}



Judge Assessment (gpt-5.4)


                                                             26
  Reasoning correct                                                                         Category: Correct
  Summary: The response correctly identifies that under replace-one adjacency the histogram has L1 sensitivity 2,
  so Laplace noise with scale 1/epsilon per bin yields 2epsilon-DP, not epsilon-DP.
  Detail: The argument correctly notes that replacing one record can decrement one bin and increment an-
  other, changing the histogram by an L1 distance of 2. It then applies the standard Laplace mechanism
  analysis for vector-valued queries with independent Laplace noise, showing the privacy loss is bounded by
  exp(epsilon*2)=exp(2epsilon) when the scale is 1/epsilon. The conclusion that the mechanism is not epsilon-DP
  under replace-one adjacency, and would need scale 2/epsilon to achieve epsilon-DP, is mathematically sound.




 Q 106           GT: No (0)                   Pred: Yes (1)   Fatal Error × wrong


  Accounting and Composition ▷ Parallel Composition
  Consider the following procedure: M := {MSi (Xi )}ni=1 , where Xi ∩ Xi+1 = ∅ for all i ∈ {1, . . . , n − 1},
                                                     n
  and their union covers the entire dataset, i.e., i=1 Xi = X. Furthermore, the partition is data-independent.
  Suppose each mechanism Mi satisfies (εi , δi )-differential privacy. Does the combined mechanism M satisfy
  (maxi∈[n] εi , maxi∈[n] δi )-differential privacy?


Comments from metadata


  Consider
          the following counter example:
                                         let Xi = X when i is odd and Xi = ∅ when i is even, then M satisfies M satisfies
        P                P
                 εi ,            δi -DP
    i∈[n] and i is odd   i∈[n] and i is odd



Model Response (gpt-5-high)
Yes. This is the parallel composition property of differential privacy.

Explanation/derivation:
- Because the partition {X_i} is disjoint and data-independent, for any neighboring datasets X and X’ that differ in exactly
      one individual’s record, there exists a unique block j such that X_j != X’_j and X_i = X’_i for all i != j.
- For i != j the inputs to M_i are identical on X and X’, hence the distributions of M_i(X_i) are identical across the two
     datasets and contribute no privacy loss.
- The joint release M(X) = (M_1(X_1), ..., M_n(X_n)) can be viewed as post-processing of M_j(X_j) together with side
     information and randomness that do not depend on the changed record (namely, the other blocks X_{-j}, which are the
     same across X and X’, and any randomness). Differential privacy is preserved under post-processing and under adding
     randomness independent of the changed record.
- Therefore, for any event S, P[M(X) in S] <= e^{epsilon_j} P[M(X’) in S] + delta_j. Maximizing over the possible affected
     block j gives (max_i epsilon_i, max_i delta_i).

Final answer:
\boxed{yes}


Judge Assessment (gpt-5.4)


  Reasoning incorrect                                                                           Category: Fatal Error
  Summary: The response incorrectly applies parallel composition by assuming the \(X_i\) form a fully disjoint
  partition, which is stronger than the stated condition.
  Detail: The key step in the response–that a neighboring change affects a unique block \(j\)–does not follow from
  the problem statement, which only requires \(X_i \cap X_{i+1} = \emptyset\), not pairwise disjointness for all \(i
  \neq j\). A single individual’s record may therefore appear in multiple non-adjacent subsets, so several mechanisms
  can incur privacy loss and the losses can compose additively rather than via a max. Thus the claimed \((\max_i
  \varepsilon_i, \max_i \delta_i)\)-DP guarantee is not justified for the stated setup, and the final conclusion "yes" is
  incorrect.


                                                                 27
G      Paraphrasing experiment of Category 2

In this section we evaluate: Do LLMs rely on memorization for achieving high accuracy of positive instances? Standard
DP textbooks and research papers may have appeared in model pretraining data, and many positive instances in our
benchmark are faithful re-statements of results with the same notations established in the literature. This raises the
concern that LLMs might rely on superficial pattern matching – simply answering “yes” when a question resembles
previously seen material. To probe this possibility, we conduct an ablation study in which all positive instances in
Category 2 are paraphrased and re-evaluated using the two best-performing models, GPT-5-High and Gemini-3-Pro. As
shown in Table 11, accuracy changes only marginally, suggesting that performance is not driven solely by memorization
but also the understanding.



Table 11: Average accuracy on paraphrased positive questions, results are reported in format Mean Accuracy± standard
deviation
                                    Model          After Paraphrase   Before Paraphrase
                                    Gemini-3-pro   0.810 ± 0.024       0.805 ± 0.039
                                    GPT-5-High     0.771 ± 0.055       0.771 ± 0.027




G.1     Paraphrasing Set-up

For each positive question in Category 2, we use GPT-5 to generate a paraphrased version. We then let a human expert
verify that the paraphrase preserves the original question’s meaning and fixes any LaTeX compilation errors when
necessary. The system prompt used for paraphrasing is provided below.


      System prompt for paraphrasing question

    You are given a technical description of a differential privacy mechanism.

    Task:
    - paraphrasing, change notation and algorithm style, but don’t change name of algorithm
    - Change the structure of the algorithm (change the order of the steps, represent the operations in a different
    way)

    Constraints:
    - Preserve exact mathematical meaning.
    - Change all variable names, symbols, and function identifiers.
    - Rewrite the algorithm using a different presentation style.
    - Do NOT change the algorithm name.
    - ALL mathematical symbols, formulas, and equations MUST be written in valid LaTeX.
    - Do NOT introduce non-LaTeX math notation.
    - Do NOT add explanations, commentary, or assumptions.
    - Output ONLY the paraphrased LaTeX content.



G.2     Example of Paraphrased Questions

We identified some interesting patterns in the paraphrased questions. In some cases, the paraphrased versions exhibit
only symbolic differences or superficial changes in structure, as shown in Figure 7, panels (a) and (a). However, the
structure of the paraphrased algorithm can also change in a more substantive way. As shown in Figure 7 (c) and (d), the
high-level description of the exponential mechanism (Lines 2-3 of Figure 7c) has been paraphrased to inverse CDF
sampling (Lines 3-4 of Figure 7d).


                                                           28
(a) Question 72: Original                                        (b) Question 72: Paraphrased




(c) Question 18: Original
                                                                 (d) Question 18: Paraphrased
                        Figure 7: Examples of paraphrased questions.




                                            29
