                                                              The FIL Hypothesis:
                                                 Inductive Biases Help with Kernel Engineering


                                               Nikolai Rozanov1,3∗          Subhabrata Dutta2         Preslav Nakov1          Iryna Gurevych2,1
                                                                       1
                                                                         NLP Department, MBZUAI, Abu Dhabi, UAE
                                                         2
                                                             Ubiquitous Knowledge Processing, TU Darmstadt, Darmstadt, Germany
                                                              3
                                                                Department of Computing, Imperial College London, London, UK
arXiv:2606.30442v1 [cs.AI] 29 Jun 2026




                                                                                          Abstract
                                                     The Bitter Lesson, which posits that general-purpose methods that scale with
                                                     computation and data ultimately outperform those with built-in human knowledge,
                                                     has become a dominant paradigm in the era of Large Language Models. We revisit
                                                     this principle by observing a new and critical scaling dimension: the duration of
                                                     the Feedback Information Loop (FIL), the time required for a system to receive a
                                                     verification signal after generating a prediction. Most historic successes in Artificial
                                                     Intelligence (AI) have benefited from near instantaneous feedback (e.g., games or
                                                     classification tasks), but we argue that future AI applications in science and the
                                                     physical world will inherently involve FILs ranging from hours to weeks. This trend
                                                     poses a fundamental scaling limit, as obtaining enough verification steps required
                                                     by purely data-driven methods becomes practically impossible. Additionally, we
                                                     propose a method that is orthogonal to purely data-driven approaches, based on
                                                     human-inspired expert knowledge. The method relies on inductive biases and
                                                     constraining the solution space. We provide an initial validation of the hypothesis
                                                     and the method, by studying the real-world GPU programming task, a domain
                                                     with non-trivial FIL, and demonstrate that incorporating inductive biases yields
                                                     superior performance over data-driven approaches. The code is released under:
                                                     https://github.com/ai-nikolai/robust_kernelbench.


                                         1     Introduction
                                         The Bitter Lesson, published nearly seven years ago, states that Artificial Intelligence (AI) systems
                                         that benefit from scaling with computation and data are those that outperform other approaches “by a
                                         big margin”, notably those that rely on human-inspired inductive biases [6]. Since the publication, this
                                         lesson has seen even more empirical evidence with Large Language Models (LLMs) not only when
                                         solving various classical Natural Language Processing (NLP) tasks [46; 45] that seemed extremely
                                         hard only a decade ago, but also when solving tasks such as problems from the Math Olympiad [25],
                                         the International Collegiate Programming Competition (ICPC) [53], as well as Agentic AI tasks such
                                         as Web Navigation, Robotics and many others [38; 50]. A key method behind these successes was
                                         the reinforcement learning-based scaling [19] of LLMs.
                                         In line with the Bitter Lesson these approaches benefit from scaling with large amounts of data and
                                         computational effort. As can be seen in Table 1, previous state-of-the-art approaches scaled and
                                         exceeded human performance with data scales ranging from around O(106 ) simulations or O(1012 )
                                         tokens of training data. Contrary to existing views, we propose a new dimension to think about such
                                         systems: the Feedback Information Loop (FIL). We define the Feedback Information Loop as the
                                         duration for an AI system to receive ‘feedback’ after it has made a prediction. This can be the reward
                                         (+1, 0 or -1) when playing chess or Go, the accuracy in classification tasks, a numerical reward on
                                         LLM generated responses and so on. The crucial observation is that most, if not all, existing problems
                                             ∗ Correspondence to: Nikolai Rozanov, nikolai.rozanov13@imperial.ac.uk



                                         Preprint.
enjoyed a very short Feedback Information Loop; given an AI response and a desired gold answer it
is very quick to compute whether the AI system is right. For example, in chess it is very quick to
compute if the position is a draw, a win, or a loss; likewise, in natural language processing, one can
quickly tell whether the answer is correct, etc.
Looking into state-of-the-art and future AI application areas, it is evident that the Feedback Informa-
tion Loop is only bound to increase. This can be easily seen in applications such as the AI Scientist
[31] (e.g., designing automatic GPU code, or machine learning experiments) or AI for the physical
world (e.g., designing a chemical synthesis, or a new aerodynamic design), which will take several
hours to several weeks to verify, as shown in Table 3. The scaling to the required2 O(106 ) data points
in such cases would yield practically impossible timelines for purely data driven approaches. This
can be clearly seen in Table 2, e.g., if a single verification takes an hour to verify, then 106 batches
would take around 114 years of verification, if it takes a day that would be nearly 3,000 years of
verification, while if the verification takes a week it would take almost 20,000 years to verify. Hence
purely data-driven approaches are becoming prohibitively expensive in the extended FIL setting.
Previous approaches did not openly identify this issue; however, they can be seen as implicit attempts
to solve the long FIL problem. Specifically, some existing work has attempted to overcome the
orthogonal but related problem of sparse feedback signal [15; 8]; however, the underlying problems
have short FIL and do not fundamentally overcome the problem. The most direct comparison is
existing work that aims to simulate the underlying process and thereby to implicitly approximate the
Feedback Information Loop, such as World Models, model-based Reinforcement Learning, reward
modeling, and other forms of modeling the environment or the feedback [20; 23]. Such approaches
are limited, however, as shown in the latest comprehensive work [16], specifically due to (1) the need
for training data, and (2) the so-called “simulation to real” gap, which represents the aleatoric and
epistemic uncertainty of the models. When looking at long FIL, we see that these two issues with
environment models would only amplify. Hence, data-driven approximation techniques also do not
represent a fundamental solution.
Our main hypothesis, the FIL hypothesis, is that “as the Feedback Information Loop increases in
duration, it will pose a fundamental limit to purely data-driven methods”, thereby extending the Bitter
Lesson.
Inspired by this observation and hypothesis, we propose a method based on inductive biases. We
define inductive biases as constraints on the solution search space. These are often inspired by a
human expert , which is orthogonal to purely data-driven approaches. In order to show an initial
validation of the FIL-Hypothesis and our proposal to use human expert-based inductive biases, we
chose a real-world problem that exhibits the slow Feedback Information Loop trend and designed
an algorithm with human-inspired solution constraints. Specifically, we chose a challenging GPU
programming task [36] in line with the AI Scientist paradigm, where AI can help the human solve
real and challenging scientific tasks. Our results demonstrate that even use cases with only several
minutes in their Feedback Information Loop duration already show signs of the improvement via
human-inspired algorithm design; we outperform the state-of-the-art baseline methods by introducing
our inductive bias across different model sizes, settings and evaluation measures.


2     The Feedback Information Loop

The core scaling dimensions in the last years of machine learning research have been (1) data and
(2) compute. In our work, we introduce a third critical one: the Feedback Information Loop.

2.1    Defining the Feedback Information Loop

We define the Feedback Information Loop as the time it takes for an AI system to receive feedback
on its prediction or a batch of predictions, as seen in Figure 1. There are three main stages in
the Feedback Information Loop: (1) the actual prediction mechanism, (2) the verification of the
prediction, (3) the (potential) use of the feedback information. Stages 1 and 3 are dependent on
the algorithmic choices. In the case of LLMs, for example, the actual prediction happens via the
    2 The number of required data points for these methods to scale is consistently very large. 106 is taken as a lower estimate

given the existing problems.


                                                               2
                  Table 1: Training data scale of the selected machine learning systems.

          System                Primary Do-             Type          of     Quantity              Feedback
                                main                    Training                                   Information
                                                        Data                                       Loop (FIL)
          AlphaGo Zero          Specialised    GO Games                      ∼4.9M                 < 1 second
          [41]                  RL Algorithm                                 O(106 )
          DeepSeek-R1           Large     Lan- Verifiable                    ∼5M O(106 )           < 1 second
          [19]                  guage Reason- Problems
                                ing Model
          Dreamer V3            General RL Game Steps                        ∼100M                 < 1 second
          [23]                  Agent                                        O(108 )
          AlphaProof            Automatic      Formal Prob-                  ∼80M                  < 1 seconds
          [25]                  Mathematical lems                            O(107 )               [40]
                                Prover


forward pass of the LLM, while the usage of feedback can happen either via updating the prompt or
via updating the parameters.




Table 2: The calculation of the total verification
time given different Feedback Information Loop
(FIL) times for 106 and 103 data points, respec-
tively. O(106 ) represents the case where tradi-
tionally that was sufficient data for super-human
performance. O(103 ) represents an “idealistic”
data-efficient scenario.

  FIL                      O(106 )            O(103 )
  1 millisecond         17 minutes           1 second
  1 second                12 days           17 minutes
  1 minute               694 days            17 hours
  1 hour                 114 years            42 days
  1 day                 2,738 years          2.7 years
  1 week               19,165 years          19 years
  1 month              83,136 years          82 years              Figure 1: Illustration of the different stages of the
                                                                   Feedback Information Loop (FIL). Step 1: The
                                                                   AI algorithm produces a solution. Step 2: The
                                                                   solution is verified. Step 3: The verification
                                                                   signal is used by the algorithm.

The total FIL duration is calculated by adding the time for each stage. Since stages 1 and 3 depend
on the algorithm; algorithmic improvements, hardware improvements and other techniques can be
used to reduce this time.3 Therefore, for the purpose of our paper, we simplify the FIL duration to the
duration of stage 2 only, which mainly depends on the underlying problem to be solved and is fully
independent of the choice of algorithm.
Existing AI problems that enjoyed widespread recognition and success, such as protein folding
prediction [27], the game of GO [41], Large Language Models for mathematical and computational
competitions [19; 25], and many more have a Feedback Information Loop (FIL) of less than a second.
Therefore, training for O(106 ) iterations takes around a day (in terms of verification costs). However,
for emerging and future AI applications, as shown in Table 3 and Appendix Table 10 training for the
   3 Naturally, for stages 1 and 3, it is sometimes not trivial to continue reducing their duration and perhaps other fundamental

limits might exists, only further amplifying the FIL.


                                                               3
same number iterations would take unrealistic time: for example one hour verification per batch leads
to 114 years of total verification time.

2.1.1    Data Needs and Scaling Laws
The scaling laws that underpin modern large language models implicitly assume the existence of vast,
static datasets [24]. The duration of the Feedback Information Loop (FIL) introduces a critical new
dimension to these scaling considerations. The well-established Chinchilla scaling laws posit that for
compute-optimal training, model size and training tokens should be scaled equally: doubling model
size requires doubling the number of tokens [24].
This problem is exacerbated for domains like code generation or physical process modeling, which
emerging evidence suggests reside in a “more data-hungry regime” than natural language [32]. In
reinforcement learning, this has often been approached with replay buffers [18], which allows the
reuse of previous data, but still requires new data to be collected. Recent work on data-efficient
reasoning has demonstrated that a model can achieve state-of-the-art performance on competition-
level mathematics with as few as 817 curated training examples [51]. Crucially, however, achieving
these results still requires 15 training epochs over this small dataset, meaning that the model sees each
example 15 times and performs over 12,000 total training steps [51]. While this represents a dramatic
improvement in sample efficiency, it does not eliminate the underlying requirement for multiple
verification signals per data point. For a real-world scientific task with a FIL of days or weeks, the
cumulative time required to complete this number of training iterations remains prohibitive. Even if
we optimistically assume that a scientific task requires only the O(104 ) verification steps necessary
for a purely data-driven approach, the cumulative waiting time renders this strategy infeasible, as at 1
hour verification time per batch, this would take a year, and for a task that takes 1 day, this would take
24 years of verification, and for a task that takes 1 week, this would take over a century of verification
time.
Thus, while data-efficient methods narrow the gap, they do not overcome the fundamental barrier
imposed by a long feedback loop. Consequently, the extended feedback delays inherent in scientific
and physical applications demand a paradigm shift away from purely data-driven approaches.

              Table 3: Selected Tasks with Prolonged Feedback Information Loop.
         Domain                                      Feedback Information Loop (FIL)
         GPU Kernel Programming [36]                      ∼2 - 30 minutes
         Machine Learning Engineering [10]                ∼2 minutes - 1 hour
         OS Kernel Engineering                            ∼ 5 minutes [7]
         Real Chemical Synthesis                          ∼< 1 hour - several weeks [43]
         Automatic Large Language Model Research          ∼< 1 day - several months [28]


3     Method Based on Inductive Biases
Our method is motivated by the slow Feedback Information Loop. Previous approaches have
attempted to overcome this challenge by modeling the environment and simulating it, or finding ways
to reuse data. Our proposed direction is orthogonal. We propose to imbue deep domain knowledge
into the system where the FIL duration is large. Specifically, our method focuses on test-time search.
We propose to break up the test-time search into subproblems based on how human experts solve the
task. Interestingly, this also leads to reduced FIL durations for each individual stage of the problem.
In line with the idea of AI searching for solutions in a (hypothesis) space [17], we define inductive
biases as a constraint of the search space for the AI system, similarly to previous work such as
[34; 6; 39]. While the exact notion of inductive biases might differ between previous work, the
commonality is the “biasing” or constraining an AI system to allow for better generalization.

3.1     Inductive Bias Search

We start with the observation that humans typically break up a complex process into smaller stages.
For example, in the case of GPU programming, when writing a specific GPU kernel, we first try


                                                    4
and make it run, then check for correctness and next, we look for ways to improve the code, and
we iterate this sequence; or, in chemical synthesis, we synthesize prerequisite chemicals first before
combining them in a final synthesis stage.
Following this principle, we propose Inductive Bias Search. Similarly to previous test-time scaling
approaches [49; 38], our method requires iterative search in the hypothesis space. Additionally, we
use verifiable rewards similarly to Reinforcement Learning with Verifiable Rewards (RLVR) [14] to
determine the different stages. The core of our method lies in the decomposition of these rewards and
stages. Existing approaches group complex rewards into a single scalar value [5], often via some
weighting. In our case, we introduce an ordered reward function that consists of limiting the solution
space at every stage. Schematically the difference compared to classical (existing) approaches and
our method can be seen in Appendix C, Figure 5 for the classical approach and Figure 6 for our
method.

3.1.1   Formalizing the Inductive Bias Search under Feedback Constraints
Let a machine learning task be defined by an input space X , a solution space Y, a reference solution
yref ∈ Y, and a final verification metric V(y, yref ) : Y × Y → R (which we denote simply as V (y)
when the reference is fixed). The goal is to find
                                         y ∗ = arg max V (y).
                                                    y∈Y


Ordered decomposition. An ordered decomposition of V is a non-increasing sequence of sub-
metrics {Vi }Ni=1 such that Vi (y) ≥ Vj (y) whenever i < j and VN = V . Intuitively, each Vi
represents an “easier” sub-objective that is less stringent than the final metric. For each stage i, we
associate a performance threshold ti and a (soft) inductive bias Bi that guides the search toward
solutions satisfying Vi ≥ ti .

Feedback budget constraint. Let τ denote the duration of a single Feedback Information Loop
(FIL) the time from generating a candidate solution to receiving its verification signal. Given a total
time budget B and the ability to run k independent verification processes in parallel, the maximum
number of verifiable evaluations is
                                                     k·B
                                               M=         .
                                                       τ
If p is the probability that a randomly sampled candidate y ∼ Y (under the model’s base distribution)
meets the final performance threshold, then under independent sampling the probability of success
after M trials is
                                        Psuccess = 1 − (1 − p)M .
For large M , even a small p yields high success probability. However, when M is severely limited
(as in long-FIL settings), the mitigation is to increase p itself i.e., to bias the sampling distribution
toward high-quality solutions without requiring many verification steps.

Inductive conditioning Inductive bias search achieves this by decomposing the final objective into
intermediate constraints. Let {Vi }Ni=1 be ordered decomposition corresponding to progressively
stricter constraints, where VN = V denotes the final objective. For simplicity, we assume each Vi
defines a binary predicate indicating whether a candidate satisfies a given stage.
Each evaluation function Vi induces a feasible subset of the hypothesis space:
                                  Yi = {y ∈ Y | Vj (y) = 1 ∀j ≤ i}

By construction,
                                  Y = Y0 ⊇ Y1 ⊇ Y2 ⊇ · · · ⊇ YN

Increasing the probability of success Inductive bias search is designed to improve the success
probability, by constraining solutions at stage i to the respective feasible hypothesis set Yi . We
consider the unconditional success probability for stage i:
                                      pi = P(Vi (y) = 1 | y ∈ Y)


                                                   5
and the conditional success probability for stage i, corresponding to our inductive bias search:
                                 p̃i = P(Vi (y) = 1 | y ∈ Yj , j < i)

Therefore, we have pi ≤ p̃i , ∀i, since Y ⊇ Yi . Therefore, we expect that successive searches yield a
higher final stage probability:


                                      p̃0 ≤ p̃1 ≤ · · · ≤ p̃N ≤ 1                                   (1)

A step by step of the method is given in Appendix C, Algorithm 1.

3.1.2    Construction of the Ordered Decomposition
The critical stage of the algorithm 1 is the human expert contribution of the ordered decomposition
     N
{Vi }i=1 , thresholds T and inductive biases B. Importantly, this stage requires the creation of
additional sub-metrics Vi , which often requires creating human-crafted verifiers for these stages. For
example in a coding task this could be measurement of specific compilation errors. Secondly, this
requires the setting of appropriate thresholds for the sub-metrics as to what counts as a successful
passing of the given metric. To simplify the threshold setting we use only binary sub-metrics in our
proposed algorithms. Finally, the creation of the (soft) inductive biases depends on the underlying
machine learning system; in our study the primary focus is on LLMs and hence the inductive biases
come in form of extended prompts and in-context learning.
The choice of the ordered decomposition depends on the task at hand and can be based on the existing
process of the human. For example in coding task the debugging pipeline of first fixing syntax errors,
then runtime errors, etc.

4     Experimental Setup
Overall, our aim with the empirical section is to demonstrate that: 1) slow FIL tasks exist in the wild;
2) demonstrate that inductive-bias based methods, like our inductive bias search can outperform the
purely data-drive approaches.
A very practical problem to this end is GPU kernel engineering. This is a very applied and important
tasks for AI scientists and engineers. On one hand because it is part of active research itself, such
as for ML systems researchers [29]; and on the other hand it is a critical component for AI research
itself, as often ML experiments would be infeasible without efficient GPU code. For example libraries
such as vLLM [29] or Unsloth [13] facilitate resource constraint training and inference.

4.1     The KernelBench Challenge as a Slow-FIL Testbed

To ground our investigation in a concrete slow-FIL problem, we adopt KernelBench, a benchmark
for evaluating LLMs’ ability to write efficient GPU kernels [36]. KernelBench level 1 comprises 100
real-world PyTorch machine learning workloads, each requiring the generation of a custom GPU
kernel that is both functionally correct and provides measurable speedup over the PyTorch baseline
[36].
The task exhibits several properties that make it an ideal representative of the emerging slow-FIL
regime. First, verification is non-trivial: each generated kernel must be compiled, executed, and
profiled to assess both correctness and runtime performance. Second, feedback is sparse and delayed:
obtaining a reward signal (speedup relative to baseline) requires minutes of compilation and execution
time per candidate. Third, the performance landscape is rugged: small semantic differences in
kernel code can produce order-of-magnitude differences in runtime, and the mapping from code to
performance is not easily approximated.
Critically, the current state-of-the-art on KernelBench is an iterative refinement paradigm that
explicitly relies on rapid feedback loops. Frontier reasoning models generate candidate kernels,
receive execution and profiling feedback, and refine their solutions over multiple rounds [4]. This
approach is a direct instantiation of the short-FIL assumption. Additionally, even with this iterative


                                                   6
feedback, the best models match PyTorch baseline performance in less than 20% of cases, and
furthermore are failing on simpler metrics like compilation and runtime as well [36]
KernelBench therefore provides a controlled setting where the Feedback Information Loop duration
is on the order of minutes already sufficient to reveal the limitations of purely data-driven, iterative
refinement approaches. KernelBench offers empirical evidence that even modest FIL durations
impose meaningful constraints on existing methods, and a testbed for evaluating inductive biases
designed to operate under such constraints.

4.2     Inductive Bias Test Time Scaling in KernelBench

In this part we describe the concrete implementation of our proposed method applied to the challenge
of GPU kernel engineering.
Following Algorithm 1, we need to identify the main metric of KernelBench as well as define an
ordered decomposition of this metric.
Given the reference pytorch solution y and the LLM proposed kernel ŷ, the objective V for Kernel-
Bench is the f astk metric [36], which measures how many solutions are correct and have a speed-up
of at least k.

                          f astk = Iŷ runs corectly {time(y)/time(ŷ) > k}                            (2)

4.2.1    Ordered Decomposition of Metrics
For KernelBench [36] , to decompose the main metric, we adopt the following metrics 1) Compilation
Success, 2) Runtime Success, 3) Correctness, 4) Fast 1 and 5) Fast 2. For more details see Appendix
D.
This structure follows the requirement presented in Section 3.1.1 that Vi (y, ŷ) ≥ Vj (y, ŷ) whenever
i < j and VN = V.
In our case each Vi is a binary variable and follows a strict order in that if a preceding metric is false
all subsequent metrics will be false and therefore 0. The thresholds required for our algorithm are
also set trivially to 1 for each metric.

4.2.2    Inductive Biases for Each Metric
Finally, we choose the inductive biases to be extensions of the prompt to the LLM that explicitly
bias the LLM to produce solutions in the given failing metric, e.g. compilation, or runtime, etc., see
Appendix E for the complete list of inductive biases.

4.3     Baselines

In terms of baselines we use the current best in class test time scaling method based on iterative
refinement [36; 5]. In our study we take a strong iterative refinement baseline, based on the current
best in class methods [36; 5], which represents the data-driven approach. We test it against our
method by keeping everything fixed and adding only the inductive bias.
Concrete, implementation details are given in Appendix B.

5     Results
We can see our results in Figure 2 and G Table 4. The x-axis represents the various metrics we used;
while the y-axis represents the aggregate score.

Uniform improvement from inductive bias For every model and important metrics like compi-
lation, runtime and correctness, the inductive bias prompt shows significant improvement over the
iterative refinement baseline. No metric degrades. This consistency across 4 architecturally diverse
models: Qwen, DeepSeek, Mistral and GPT. This strongly suggests that the advantage of inductive
bias is not an artifact of a particular model family.


                                                    7
Figure 2: Results across various models from Table 4. X-axis represents the various metrics. Y-axis
represents the normalized score from the 100 samples. IR (green) represents the iterative refinement
approach; IB (orange) represents our inductive bias based iterative refinement.



Magnitude of gains The largest absolute improvements are observed in compilation success, with
deltas ranging being up to +0.31 for Mistral’s Devstral-2512. Runtime success improves by up to
+0.17, and correctness by up to +0.12 for gpt-oss. Relative improvements are often substantial:
for example, Qwen3-14B shows a 2x relative increase in correctness, from 0.04 to 0.11. Even the
strongest iterative refinement baseline, GPT-OSS-120B with correctness 0.21 is outperformed by its
own inductive bias variant 0.33, indicating that inductive biases benefit both weak and state-of-the-art
models.

Correctness remains challenging. Despite consistent improvements, absolute correctness under
multi stage search does not exceed 0.33 for any model. This reflects the inherent difficulty of the
GPU programming task, which highly sophisticated low level parallel code. Inductive biases provide
a meaningful but not yet sufficient advantage.

5.1   Model Specific Observations
       • DeepSeek V3.1 Terminus and Mistral Devstral-2512 exhibit the largest improvements
         from the inductive biases, particularly in compilation (+0.22 and +0.29, respectively).
         These models appear to benefit most from explicit solution space constraints.
       • Qwen3-32B under iterative refinement performs poorly (compilation 0.26) but rises to a
         competitive 0.41 with inductive biases, nearly matching the iterative refinement performance
         of much larger models. This further highlights how inductive biases alleviate the ‘smaller’
         data regime.
       • GPT-oss-120b achieves on average the best scores across most metrics and especially fast 1
         and fast 2. Interestingly, inductive biases are very effective with this model for all metrics.


                                                   8
        • The performance metrics fast1 and fast2 show only a small direction of change; some
          models see small increases with inductive biases, only Qwen3-30B-A3B has any statistical
          significance. Again this indicates that this field of designing effective inductive biases for
          harder fields is still open.

Table 4: Main results table summarizing the scores. All experiments were conducted on the Ker-
nelBench GPU programming task with a fixed test set of size N = 100 problems from level 1. IR
= Iterative Refinement; IB = Inductive Bias. Reported values are mean ± standard deviation over
3 runs. Green bold values indicate statistically significant improvement of +IB over IR (Welch’s
t-test, one-tailed, p < 0.05). Bold = best overall, underline = second best (ties allowed). COMP =
Compilation Success, RUN = Runtime Success, CORR = Correctness.

      Model                Method       COMP             RUN           CORR           Fast1          Fast2
      Qwen3-14B            IR          0.22 ± 0.06   0.19 ± 0.03   0.04 ± 0.02    0.01 ± 0.01    0.01 ± 0.01
      Qwen3-14B            +IB         0.34 ± 0.04   0.29 ± 0.05   0.11 ± 0.01    0.03 ± 0.01    0.02 ± 0.01
      Qwen3-32B            IR          0.26 ± 0.05   0.23 ± 0.05   0.06 ± 0.01    0.00 ± 0.01    0.00 ± 0.01
      Qwen3-32B            +IB         0.41 ± 0.02   0.39 ± 0.02   0.11 ± 0.02    0.02 ± 0.02    0.01 ± 0.01
      Qwen3-30B-A3B        IR          0.40 ± 0.00   0.38 ± 0.00   0.02 ± 0.00    0.00 ± 0.00    0.00 ± 0.00
      Qwen3-30B-A3B        +IB         0.53 ± 0.00   0.48 ± 0.00   0.12 ± 0.00    0.03 ± 0.00    0.02 ± 0.00
      deepseek-v3.1        IR          0.28 ± 0.01   0.26 ± 0.02   0.09 ± 0.01    0.05 ± 0.01    0.02 ± 0.02
      deepseek-v3.1        +IB         0.57 ± 0.08   0.55 ± 0.07   0.20 ± 0.03    0.09 ± 0.02    0.03 ± 0.01
      devstral-2512        IR          0.38 ± 0.02   0.33 ± 0.02   0.09 ± 0.01    0.05 ± 0.02    0.02 ± 0.01
      devstral-2512        +IB         0.69 ± 0.02   0.57 ± 0.01   0.14 ± 0.01    0.05 ± 0.01    0.02 ± 0.01
      gpt-oss-120b         IR          0.53 ± 0.03   0.48 ± 0.05   0.21 ± 0.02    0.04 ± 0.01    0.02 ± 0.02
      gpt-oss-120b         +IB         0.63 ± 0.05   0.56 ± 0.07   0.33 ± 0.05    0.11 ± 0.06    0.05 ± 0.03


5.2    Control Study: Effect of Additional Coding Pre-training Data

In order to test the hypothesis that inductive biases are truly effective in the low data regime, we
construct a small controlled study where we test the ‘coding’ models in two LLM families, Qwen and
DeepSeek. This controlled experiment is in line with the hypothesis that more data reduces the effect
of inductive biases. Conversely, this also affirms that reducing data increases the role of inductive
biases. Table 5 and Table 11, clearly show that the effect of inductive biases drops as more data is
added.

Table 5: Results for the ‘Coder’ models in the Qwen and DeepSeek family, it can be seen that the
inductive bias method has only marginal improvement in the case of further pre-training. See Table 4
for details.

    Model                      Method       COMP           RUN           CORR            Fast1          Fast2
    Qwen3-30B-A3B              IR          0.40 ± 0.00   0.38 ± 0.00    0.02 ± 0.00    0.00 ± 0.00    0.00 ± 0.00
    Qwen3-30B-A3B              +IB         0.53 ± 0.00   0.48 ± 0.00    0.12 ± 0.00    0.03 ± 0.00    0.02 ± 0.00
    Qwen3-Coder-30B-A3B        IR          0.60 ± 0.00   0.59 ± 0.00    0.22 ± 0.00    0.05 ± 0.00    0.02 ± 0.00
    Qwen3-Coder-30B-A3B        +IB         0.63 ± 0.00   0.59 ± 0.00    0.23 ± 0.00    0.01 ± 0.00    0.00 ± 0.00
    DeepSeek-Coder             IR          0.58 ± 0.00   0.50 ± 0.00    0.18 ± 0.00    0.03 ± 0.00    0.00 ± 0.00
    DeepSeek-Coder             +IB         0.59 ± 0.00   0.54 ± 0.00    0.20 ± 0.00    0.05 ± 0.00    0.03 ± 0.00



6     Conclusion

We explored a new scaling dimension for AI: the duration of the Feedback Information Loop (FIL).
Nowadays the prevailing ML paradigm leverages vast amounts of near instantaneous data to drive
improvements. We argued that many emerging applications in science, engineering, and the physical
world are characterized by inherently slow FILs ranging from hours to weeks. In such regimes purely
data driven approaches that have dominated recent AI successes become impractical.


                                                     9
We use KernelBench as a slow FIL task to investigate this hypothesis. Specifically, KernelBench has
slow reward signals due to its non trivial verification. The current state-of-the-art relies on iterative
refinement and achieves only modest success, underscoring the limitations of short FIL approaches
even in minute scale tasks.
As a first step toward addressing these constraints, we proposed an inductive bias based method that
decomposes the verification process into an ordered hierarchy of binary metrics and injects stage
specific inductive biases via targeted prompting. This approach leverages structured prior knowledge
to produce better predictions.
Our results demonstrate that incorporating such inductive biases, consistently outperforms existing
iterative refinement approaches across a range of open and frontier models. These serves as an initial
validation that, as FIL duration grows, explicit inductive biases can once again become an important
component for ML algorithms and complementing or even surpassing purely data driven scaling.
Looking forward, we hope this work encourages the community to systematically study and develop
methods for the emerging problem of slow FIL AI.

Acknowledgements
This work has been supported by the German Federal Ministry of Research, Technology and Space
and the Hessian Ministry of Higher Education, Research, Science and the Arts within their joint
support of the National Research Center for Applied Cybersecurity ATHENE.

References
 [1] Jie An, De Wang, Pengsheng Guo, Jiebo Luo, and Alex Schwing. 2025. On Inductive Biases
     That Enable Generalization in Diffusion Transformers. In The Thirty-ninth Annual Confer-
     ence on Neural Information Processing Systems. https://openreview.net/forum?id=
     lE2cD7C9fk

 [2] Jose A. Arjona-Medina, Michael Gillhofer, Michael Widrich, Thomas Unterthiner, Johannes
     Brandstetter, and Sepp Hochreiter. 2019. RUDDER: return decomposition for delayed rewards.
     Curran Associates Inc., Red Hook, NY, USA.

 [3] Randall Balestriero and Yann LeCun. 2025.     LeJEPA: Provable and Scalable Self-
     Supervised Learning Without the Heuristics. ArXiv abs/2511.08544 (2025).  https:
     //api.semanticscholar.org/CorpusID:282922448

 [4] Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo, and Silas Alberti. 2025. Kevin: Multi-
     Turn RL for Generating CUDA Kernels. ArXiv abs/2507.11948 (2025). https://api.
     semanticscholar.org/CorpusID:280232580

 [5] Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo, and Silas Alberti. 2026. Kevin: Multi-Turn
     RL for Generating CUDA Kernels. In The Fourteenth International Conference on Learning
     Representations. https://openreview.net/forum?id=xu1XwVZtDi

 [6] Peter W. Battaglia, Jessica B. Hamrick, Victor Bapst, Alvaro Sanchez-Gonzalez, Vinicius
     Zambaldi, Mateusz Malinowski et al. 2018. Relational inductive biases, deep learning, and
     graph networks. arXiv:1806.01261 [cs.LG] https://arxiv.org/abs/1806.01261

 [7] Heraldo Borges, Juliana Alves Pereira, Djamel Eddine Khelladi, and Mathieu Acher. 2025.
     Linux Kernel Configurations at Scale: A Dataset for Performance and Evolution Analysis.
     arXiv:2505.07487 [cs.SE] https://arxiv.org/abs/2505.07487

 [8] Yuri Burda, Harrison Edwards, Amos Storkey, and Oleg Klimov. 2018. Exploration by Random
     Network Distillation. arXiv:1810.12894 [cs.LG] https://arxiv.org/abs/1810.12894

 [9] Yuri Burda, Harrison Edwards, Amos Storkey, and Oleg Klimov. 2019. Exploration by random
     network distillation. In International Conference on Learning Representations. https://
     openreview.net/forum?id=H1lJJnR5Ym


                                                   10
[10] Jun Shern Chan, Neil Chowdhury, Oliver Jaffe, James Aung, Dane Sherburn, Evan Mays et al.
     2025. MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering. In
     The Thirteenth International Conference on Learning Representations. https://openreview.
     net/forum?id=6s5uXNWGIh
[11] Yingshan Chang and Yonatan Bisk. 2025. Language Models Need Inductive Biases to Count
     Inductively. In The Thirteenth International Conference on Learning Representations. https:
     //openreview.net/forum?id=s3IBHTTDYl
[12] Chang Chen, Jaesik Yoon, Yi-Fu Wu, and Sungjin Ahn. 2021. TransDreamer: Reinforcement
     Learning with Transformer World Models. In Deep RL Workshop NeurIPS 2021. https:
     //openreview.net/forum?id=sVrzVAL90sA
[13] Michael Han Daniel Han and Unsloth team. 2023. Unsloth.               https://github.com/
     unslothai/unsloth
[14] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang et al.
     2025. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.
     arXiv:2501.12948 [cs.CL] https://arxiv.org/abs/2501.12948
[15] Rati Devidze, Parameswaran Kamalaruban, and Adish Singla. 2022.      Exploration-
     Guided Reward Shaping for Reinforcement Learning under Sparse Rewards. In Ad-
     vances in Neural Information Processing Systems, S. Koyejo, S. Mohamed, A. Agar-
     wal, D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran Associates, Inc.,
     5829–5842.    https://proceedings.neurips.cc/paper_files/paper/2022/file/
     266c0f191b04cbbbe529016d0edc847e-Paper-Conference.pdf
[16] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng et al. 2025.
     Understanding World or Predicting Future? A Comprehensive Survey of World Models. ACM
     Comput. Surv. 58, 3, Article 57 (Sept. 2025), 38 pages. doi:10.1145/3746449
[17] Subhabrata Dutta, Timo Kaufmann, Goran Glavaš, Ivan Habernal, Kristian Kersting, Frauke
     Kreuter et al. 2025. Problem Solving Through Human–AI Preference-based Cooperation.
     Computational Linguistics 51, 4 (12 2025), 1337–1372. arXiv:https://direct.mit.edu/coli/article-
     pdf/51/4/1337/2539252/coli.a.19.pdf doi:10.1162/COLI.a.19
[18] Ben Eysenbach, Russ R Salakhutdinov, and Sergey Levine. 2019. Search on the Replay
     Buffer: Bridging Planning and Reinforcement Learning. In Advances in Neural Information
     Processing Systems, H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox, and
     R. Garnett (Eds.), Vol. 32. Curran Associates, Inc. https://proceedings.neurips.cc/
     paper_files/paper/2019/file/5c48ff18e0a47baaf81d8b8ea51eec92-Paper.pdf
[19] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu et al. 2025.
     DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. Nature 645,
     8081 (01 Sep 2025), 633–638. doi:10.1038/s41586-025-09422-z
[20] David Ha and Jürgen Schmidhuber. 2018. Recurrent World Models Facilitate Policy Evo-
     lution. In Advances in Neural Information Processing Systems, S. Bengio, H. Wallach,
     H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett (Eds.), Vol. 31. Curran As-
     sociates, Inc. https://proceedings.neurips.cc/paper_files/paper/2018/file/
     2de5d16682c3c35007e4e92982f1a2ba-Paper.pdf
[21] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. 2020. Dream to Control:
     Learning Behaviors by Latent Imagination. https://arxiv.org/pdf/1912.01603.pdf
[22] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and
     James Davidson. 2019. Learning Latent Dynamics for Planning from Pixels. In Proceedings of
     the 36th International Conference on Machine Learning (Proceedings of Machine Learning
     Research, Vol. 97), Kamalika Chaudhuri and Ruslan Salakhutdinov (Eds.). PMLR, 2555–2565.
     https://proceedings.mlr.press/v97/hafner19a.html
[23] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. 2025. Mastering diverse
     control tasks through world models. Nature 640, 8059 (01 Apr 2025), 647–653. doi:10.1038/
     s41586-025-08744-2


                                                 11
[24] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza
     Rutherford et al. 2022. Training compute-optimal large language models. In Proceedings of the
     36th International Conference on Neural Information Processing Systems (New Orleans, LA,
     USA) (NIPS ’22). Curran Associates Inc., Red Hook, NY, USA, Article 2176, 15 pages.
[25] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser
     et al. 2025. Olympiad-level formal mathematical reasoning with reinforcement learning. Nature
     (12 Nov 2025). doi:10.1038/s41586-025-09833-y
[26] Humaid Ibrahim, Nikolai Rozanov, and Marek Rei. 2025. Fine-tuning with RAG for Improving
     LLM Learning of New Skills. arXiv:2510.01375 [cs.AI] https://arxiv.org/abs/2510.
     01375
[27] John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ron-
     neberger et al. 2021. Highly accurate protein structure prediction with AlphaFold. Nature 596,
     7873 (01 Aug 2021), 583–589. doi:10.1038/s41586-021-03819-2
[28] Apoorv Khandelwal, Tian Yun, Nihal V. Nayak, Jack Merullo, Stephen H. Bach, Chen Sun,
     and Ellie Pavlick. 2024. $100K or 100 Days: Trade-offs when Pre-Training with Academic
     Resources. CoRR abs/2410.23261 (2024). arXiv:2410.23261 doi:10.48550/ARXIV.2410.
     23261
[29] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu et al.
     2023. Efficient Memory Management for Large Language Model Serving with PagedAttention.
     In Proceedings of the 29th Symposium on Operating Systems Principles (Koblenz, Germany)
     (SOSP ’23). Association for Computing Machinery, New York, NY, USA, 611–626. doi:10.
     1145/3600006.3613165
[30] Anne Lauscher, Olga Majewska, Leonardo F. R. Ribeiro, Iryna Gurevych, Nikolai Rozanov,
     and Goran Glavaš. 2020. Common Sense or World Knowledge? Investigating Adapter-Based
     Knowledge Injection into Pretrained Transformers. In Proceedings of Deep Learning Inside Out
     (DeeLIO): The First Workshop on Knowledge Extraction and Integration for Deep Learning
     Architectures, Eneko Agirre, Marianna Apidianaki, and Ivan Vulić (Eds.). Association for
     Computational Linguistics, Online, 43–49. doi:10.18653/v1/2020.deelio-1.5
[31] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha.
     2024. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery.
     arXiv:2408.06292 [cs.AI] https://arxiv.org/abs/2408.06292
[32] Xianzhen Luo, Wenzhen Zheng, Qingfu Zhu, Rongyi Zhang, Houyi Li, Siming Huang et al.
     2025. Scaling Laws for Code: A More Data-Hungry Regime. arXiv:2510.08702 [cs.CL]
     https://arxiv.org/abs/2510.08702
[33] Vincent Micheli, Eloi Alonso, and François Fleuret. 2024. Efficient World Models with Context-
     Aware Tokenization. In Proceedings of the 41st International Conference on Machine Learning
     (Proceedings of Machine Learning Research, Vol. 235), Ruslan Salakhutdinov, Zico Kolter,
     Katherine Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp (Eds.).
     PMLR, 35623–35638. https://proceedings.mlr.press/v235/micheli24a.html
[34] Tom Michael Mitchell. 2007. The Need for Biases in Learning Generalizations.          https:
     //api.semanticscholar.org/CorpusID:3237155
[35] Ian Osband, Charles Blundell, Alexander Pritzel, and Benjamin Van Roy. 2016. Deep explo-
     ration via bootstrapped DQN. In Proceedings of the 30th International Conference on Neural
     Information Processing Systems (Barcelona, Spain) (NIPS’16). Curran Associates Inc., Red
     Hook, NY, USA, 4033–4041.
[36] Anne Ouyang, Simon Guo, Simran Arora, Alex L. Zhang, William Hu, Christopher Ré,
     and Azalia Mirhoseini. 2025. KernelBench: Can LLMs Write Efficient GPU Kernels?
     arXiv:2502.10517 [cs.LG] https://arxiv.org/abs/2502.10517
[37] Nikolai Rozanov. 2026. Multi-task LLMs for Bug Classification: Efficient Inference with
     Auxiliary Decoding Heads. arXiv:2606.09956 [cs.SE] https://arxiv.org/abs/2606.
     09956


                                                12
[38] Nikolai Rozanov and Marek Rei. 2025. StateAct: Enhancing LLM Base Agents via Self-
     prompting and State-tracking. arXiv:2410.02810 [cs.AI] https://arxiv.org/abs/2410.
     02810
[39] Dhruv Sahnan, Subhabrata Dutta, Tanmoy Chakraborty, Preslav Nakov, and Iryna Gurevych.
     2026. Co-FactChecker: A Framework for Human-AI Collaborative Claim Verification Us-
     ing Large Reasoning Models. arXiv:2604.13706 [cs.CL] https://arxiv.org/abs/2604.
     13706
[40] Marco Dos Santos, Hugues de Saxcé, Haiming Wang, Ran Wang, Mantas Baksys, Mert Unsal
     et al. 2025. Kimina Lean Server: A High-Performance Lean Server for Large-Scale Verification.
     arXiv:2504.21230 [cs.LO] https://arxiv.org/abs/2504.21230
[41] David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja Huang, Arthur
     Guez et al. 2017. Mastering the game of Go without human knowledge. Nature 550, 7676 (01
     Oct 2017), 354–359. doi:10.1038/nature24270
[42] Vighnesh Subramaniam, David Mayo, Colin Conwell, Tomaso Poggio, Boris Katz, Brian
     Cheung, and Andrei Barbu. 2025. Training the Untrainable: Introducing Inductive Bias via
     Representational Alignment. In The Thirty-ninth Annual Conference on Neural Information
     Processing Systems. https://openreview.net/forum?id=zvYxXhlQHM
[43] Amanda A. Volk, Robert W. Epps, Daniel T. Yonemoto, Benjamin S. Masters, Felix N. Castel-
     lano, Kristofer G. Reyes, and Milad Abolhasani. 2023. AlphaFlow: autonomous discov-
     ery and optimization of multi-step chemistry using a self-driven fluidic lab guided by rein-
     forcement learning. Nature Communications 14, 1 (14 Mar 2023), 1403. doi:10.1038/
     s41467-023-37139-y
[44] Laura von Rueden, Sebastian Mayer, Katharina Beckh, Bogdan Georgiev, Sven Giesselbach,
     Raoul Heese et al. 2023. Informed Machine Learning – A Taxonomy and Survey of Integrat-
     ing Prior Knowledge into Learning Systems. IEEE Transactions on Knowledge and Data
     Engineering 35, 1 (2023), 614–633. doi:10.1109/TKDE.2021.3079836
[45] Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix Hill
     et al. 2020. SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding
     Systems. arXiv:1905.00537 [cs.CL] https://arxiv.org/abs/1905.00537
[46] Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel R. Bow-
     man. 2019. GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language
     Understanding. arXiv:1804.07461 [cs.CL] https://arxiv.org/abs/1804.07461
[47] Andrew Gordon Wilson. 2025. Position: Deep Learning is Not So Mysterious or Different.
     In Proceedings of the 42nd International Conference on Machine Learning (Proceedings
     of Machine Learning Research, Vol. 267), Aarti Singh, Maryam Fazel, Daniel Hsu, Simon
     Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu (Eds.). PMLR,
     82326–82346. https://proceedings.mlr.press/v267/wilson25a.html
[48] Ziyi Wu, Nikita Dvornik, Klaus Greff, Thomas Kipf, and Animesh Garg. 2023. SlotFormer:
     Unsupervised Visual Dynamics Simulation with Object-Centric Models. In The Eleventh Inter-
     national Conference on Learning Representations. https://openreview.net/forum?id=
     TFbwV6I0VLg
[49] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik
     Narasimhan. 2023. Tree of Thoughts: Deliberate Problem Solving with Large Language
     Models. In Advances in Neural Information Processing Systems, A. Oh, T. Naumann,
     A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.), Vol. 36. Curran Associates, Inc.,
     11809–11822. https://proceedings.neurips.cc/paper_files/paper/2023/file/
     271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf
[50] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and
     Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models.
     arXiv:2210.03629 [cs.CL] https://arxiv.org/abs/2210.03629


                                               13
[51] Yixin Ye, Zhen Huang, Yang Xiao, Ethan Chern, Shijie Xia, and Pengfei Liu. 2025. LIMO: Less
     is More for Reasoning. In Second Conference on Language Modeling. https://openreview.
     net/forum?id=T2TZ0RY4Zk

[52] Tianren Zhang, Guanyu Chen, and Feng Chen. 2025. When do neural networks learn world
     models?. In Proceedings of the 42nd International Conference on Machine Learning (Proceed-
     ings of Machine Learning Research, Vol. 267), Aarti Singh, Maryam Fazel, Daniel Hsu, Simon
     Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu (Eds.). PMLR,
     74639–74670. https://proceedings.mlr.press/v267/zhang25j.html

[53] Kaijian Zou, Aaron Xiong, Yunxiang Zhang, Frederick Zhang, Yueqi Ren, Jirong Yang et al.
     2025. LiveOIBench: Can Large Language Models Outperform Human Contestants in Informat-
     ics Olympiads? arXiv preprint arXiv:2510.09595 (2025). doi:10.48550/arXiv.2510.09595


A     Background
A.1   Learning with delayed and sparse feedback

The challenge of learning from delayed feedback has been a persistent concern across multiple
subfields of machine learning, especially in reinforcement learning (RL). The problem is often
referred to as a sparse rewards setting. This both degrades sample efficiency and often prevents
meaningful asymptotic solutions [15; 9]. In the sparse or delayed reward setting, the delay can be
formalized as the number of environment steps between an action and the reward for that action, the
goal is to learn a policy that performs well despite this delay. This setting is orthogonal to the one
presented in this paper as can be seen in Figure 3, since both delay due to the environment dynamics
and due to FIL are independent.
Existing work has approached this problem of delayed environment dynamics via curiosity driven
algorithms [9], reward shaping [15; 2] and principled statistics algorithms, such as Bayes Exploration
in RL [35] While such approaches represents a meaningful advance, they represent an orthogonal
approach to the one we discuss in this study, as the existing approaches are still data driven. Our setting,
by contrast, focuses on regimes where the verification process itself determines the maximum feasible
data scale, transforming what has traditionally been an algorithmic challenge into a fundamental data
bottleneck.

A.2   Approximate feedback loop

A parallel line of research seeks to circumvent long feedback delays by learning surrogate models
that approximate it. Model based RL and the more recent work on world models learn to predict the
environment dynamic and represent the most systematic instantiation of this approach [20; 52; 3; 37].
By enabling an agent to “imagine” the outcomes of potential actions without executing them in the
real environment, world models can dramatically reduce the need for real world interaction.
The development of world models has progressed through several architectural generations. PlaNet
[22] introduced learning latent dynamics from pixels for planning. The Dreamer family of algorithms
[21; 23] extended this paradigm to scalable reinforcement learning, achieving state-of-the-art per-
formance on Atari and continuous control benchmarks by learning behaviors entirely within latent
imagination. Recent work has expanded world models to incorporate object-centric representations
[48], which improve compositional generalization and sample efficiency in visually challenging tasks.
Transformers have been integrated into world models [12; 33] to capture longer-range dependen-
cies. The application domains for world models now span robotics, autonomous driving, scientific
discovery, coding and many more.
While these approaches are successful for short FIL, the world model approach faces fundamental
limitations that are directly relevant to our thesis. Firstly, the simulation to real gap: policies
trained entirely within learned simulators often fail when deployed in the real world due to distribution
shift between the model’s training distribution and the true environment dynamics. This challenge is
extensively documented in different fields, including robotics, natural and social sciences. Recent
surveys explicitly identify “Physical and Natural Sciences” and “Social Science and Socioeconomic
Systems” as an area where world models exhibit a significant struggle [16]. Second, and more


                                                    14
Figure 3: Schematic illustration of the difference between delay in reward due to number of steps
in the environment versus delay in reward due to increased FIL, showing that these are orthogonal
properties.


fundamentally, the world model itself must be trained on real-world data. Learning an accurate
simulator of chemical synthesis, aerodynamic design, or GPU kernel performance still requires
collecting verification data from the real world. The world model approach does not eliminate the
Feedback Information Loop. If the FIL for a single verification is one week, collecting the dataset
to train a reliable world model may require thousands or millions of such verifications, which is
precisely the infeasible regime we identify.
Thus, while world models represent a powerful complementary technique, they do not resolve the
underlying problem that some environments will require real verification process that creates a
concrete feedback bottleneck.

A.3   Existing work on inductive biases and using expert knowledge and constraints

Inductive biases are often characterized as structural priors embedded within machine learning models
guide generalization [47; 42]. Notably, work on diffusion models has revealed that locally linear
UNet based denoisers possess specific inductive biases that enable generalization under constrained
conditions [1]. Additionally, studies demonstrate that language models require explicit inductive
biases to perform certain reasoning tasks like recursive counting, challenging the notion that scale
alone suffices [11].
Additionally, there have been several works studying the systematic injection of knowledge into
machine learning systems [44; 30; 38; 26], termed informed machine learning, which posits four
stages at which prior knowledge can be integrated into a machine learning pipeline: 1) the training
data, 2) the hypothesis set, 3) the learning algorithm, and 4) the final hypothesis choice. Existing
work of informed machine learning operates generally under the assumption of enhancing existing
solutions with expert knowledge.
In our work we enhance the concept of informed machine learning to the setting where the FIL
duration becomes expensive and therefore posits fundamental limits to the data collection process.

B     Implementation Details
Our evaluation code and prompts will be open-sourced upon publication. Generally, we use our own
adaptation of the original KernelBench evaluation suite and made it more robust. Our flow consists


                                                 15
                   Figure 4: Data flow during the evaluation of a single sample.


                            Table 6: The models we used in our work.
                  Model Type                        Size    Inference Provider
                  Qwen3-4B                          14B     vLLM
                  Qwen3-8B                          14B     vLLM
                  Qwen3-14B                         14B     vLLM
                  Qwen3-32B                         32B     vLLM
                  Qwen3-30B-A3B-Instruct            30B     vLLM
                  Qwen3-Coder-30B-A3B-Instruct 30B          vLLM
                  DeepSeek-V2-Coder                 16B     vLLM
                  DeepSeek-V3.1                     671B OpenRouter
                  Devstral-0512 (Devstral 2)        123B OpenRouter
                  Gpt-oss-120B                      120B OpenRouter


of three parts: 1) Inference either via API or vLLM [29]; 2) Distributed Compilation using Nvidia’s
NVCC compiler; 3) Evaluation using our own custom evaluation script; that overcomes existing
issues with KernelBench4 . Figure 4 demonstrates our data flow schematically.

B.1   Models

In our paper we aim at reproducibility, therefore we priortize results and experiments using open
models. We investigate four model families, Qwen, GPT, Mistral and DeepSeek, specifically see
Table 6.
All hyper-parameters were either default values of OpenRouter and vLLM respectively or set based
on Table 7.

                     Table 7: Hyper-parameters that we set fixed for all runs.
                    Hyper-parameter                    Value
                     Temperature                         0.6
                    Max Model Len                      32000
                     Max Tokens                         8000
                        Dtype         Automatic (i.e. default for each model)


B.2   Computational Infrastructure

All experiments were run using A40 GPUs; or A100 GPUs Overall, more than 500 GPU hours were
spent on the project. Additionally, OpenRouter credits were used.

B.3   Licenses

LLM Models all models have open-weight licenses that we used. We were allowed to use them.
The work was cited.
  4 The following issue crashes the original benchmark: https://github.com/ScalingIntelligence/KernelBench/

issues/76.


                                                   16
Dataset    KernelBench, is licensed under MIT, so free to use. The work was cited.

Software All software is opensource and open for use, only standard libraries were used or own
software. All relevant software was cited.

C     Inductive bias search
Deriving the Probabilistic Relation Let p(y) denote the base sampling distribution induced by
the underlying model. Inductive bias search modifies this distribution through conditioning on
intermediate constraints. At stage i, the effective sampling distribution is:
                                       pi (y) = p(y | y ∈ Yi−1 )

Define the stage-wise success probability:
                                       pi = Py∼pi−1 (Vi (y) = 1)
i.e., the probability that a sample drawn at stage i − 1 satisfies the constraint introduced at stage i.
The probability of sampling a solution that satisfies all stages can be decomposed as:
                                                        N
                                                        Y
                                             pfinal =         pi
                                                        i=1

The monotonicity of stage-wise success probabilities pi does not hold in general, as each pi is defined
with respect to a different conditional distribution. Instead, we consider the conditional success
probability of the final objective:
                                     p̃i = P(VN (y) = 1 | y ∈ Yi )
Under effective decomposition, we expect:
                                       p̃0 ≤ p̃1 ≤ · · · ≤ p̃N = 1
that is, successive constraints increase the likelihood that a candidate satisfies the final objective.

C.1   Inductive bias algorithm

Algorithm 1 Inductive bias search
Input: Input x ∈ X , output y ∈ Y, metric V, iteration budget M, (existing) LLM (prompt, x)
                                                   N
Output: Solution y ∗ , ordered decomposition {Vi }i=1 , thresholds T = {t1 , ..., tN }, inductive biases
    B = {inductive_bias1 , ..., inductive_biasN }
 1: Human expert proposes and creates ordered decomposition of metric V alongside appropriate
    thresholds and the inductive biases in N stages.
 2: Initialize ŷ ← LLM (prompt, x)
 3: for i = 1, 2, . . . , M do
 4:    for j = 1, 2, . . . , N do
 5:       current_score ← Vj (y, ŷ)
 6:       if current_score < tj then
 7:          ŷ ← LLM (prompt + inductive_biasj , x)
 8:          break
 9:       end if
10:    end for
11: end for
12: return ŷ



C.2   Comparison of Classical Search vs. Multi-Stage Search

D     Metrics used for KernelBench


                                                   17
                        Figure 5: Classical Solution Search




                       Figure 6: Inductive bias search (Ours)



E   Inductive Biases for KernelBench




                                        18
Table 8: Metrics for KernelBench evaluation. Some are from [36] while other metrics are newly
introduced.
    Metric                   Description                                             New
    Format Success           Checks if the LLM output is correct                      Yes
    Syntax Success            Checks whether the syntax of the code is correct              Yes
    Compilation Step 1 Suc-   Does a simple compilation of the file, but does not try to    Yes
    cess                      load the file itself.
    Compilation Step 2 Suc-   Compiles and loads the file                                   Yes
    cess
    Full Compilation Suc-     Compiles, loads the file and loads the new model.             No
    cess
    Model Available           A second attempt at compiling, loading the file and loading   Yes
                              the new model from scratch.
    Model Init Success        Attempts to initalize the model class, without any weight     Yes
                              transfer.
    Model Loading Success     Attempts to load the new model fully.                         Yes
    Full Runtime Success      Runs the model and compares against the reference model.      No
    Correctness               Checks whether the output is correct.                         No
    Fast 1                    Counts how many solutions are both correct and at least       No
                              1x faster than the reference solution (i.e. same speed)
    Fast 2                    Same as Fast 1, but at least 2x faster than the reference     No
                              solution.


F    Feedback Information Loop Tables




                                                19
Table 9: The below are the metrics we choose for the ordered decomposition; as well as the inductive
biases we chose for our method.
   Compilation “Unfortunately, your previous answer failed to compile.
   Success       Think carefully about how to solve the compilation issues.
                 Here is the error message: {error_message}” “Remember your
                 key objective now is to debug the code and arrive at a
                 correct CUDA Implementation.”
      Runtime    “Your previous answer compiled successfully but had runtime
      Success    errors. Think carefully how to solve the runtime issues.
                 Here is the error message: {error_message}” “Remember your
                 key objective now is to debug the code and arrive at a
                 correct CUDA Implementation.”
      Correctness “Your previous answered compiled and ran without problems.
      Success     However, your previous code produced the wrong answer.
                  I.e. either the shape or the numbers were wrong. Think
                  carefully how to make your code produce the correct code.
                  Here is the error message: {error_message}” “Remember your
                  key objective now is to make sure your code produces the
                  correct answer.”
      Fast 1     “Your previous answer was correct but can be made faster.
                 Think carefully how to make the solution faster. Here
                 is the speedup you achieved relative to the baseline:
                 {score}times faster. ” “Remember your key objective now
                 is to make the code run faster.”
      Fast 2     “Your previous answer was correct but can be made faster.
                 Think carefully how to make the solution faster. Here
                 is the speedup you achieved relative to the baseline:
                 {score}times faster. ” “Remember your key objective now
                 is to make the code run faster.”


G      Additional Results

In the figure plots of the transitions Figure 7 & 8; we observe the transition counts from the previous
best metric of a given sample to the new best metric. What we can see is that inductive biases have
the propensity to bias the metric towards improvement; especially in the easier part of the metrics.

H      Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many
potential societal consequences of our work, none which we feel must be specifically highlighted
here.
The only exception to this is perhaps the fact that AI progress might be significantly limited by the
implications of our hypothesis, at the same time this work would indicate a bigger role for humans in
the future of AI.

I     Additional discussion and limitations

I.1    Relation to the Feedback Information Loop hypothesis

We hypothesized that as the feedback information loop (FIL) lengthens, purely data driven iterative
refinement becomes less effective, and methods that embed inductive biases should gain an advantage.
The KernelBench task has a FIL on the order of minutes, longer than the typical classification or game
tasks, but far shorter than the hours or weeks envisioned for future scientific applications. Within this


                                                   20
               Table 10: Selected Tasks with Prolonged Feedback Information Loop.
    Domain                          Type of Evaluation               Feedback Information
                                                                     Loop (FIL)
    GPU Kernel Programming          Code Compilation and Perfor- ∼2 - 30 minutes
    [36]                            mance Evaluation
    Machine Learning Engineer-      Datascience and Machine Learn- ∼2 minutes - 1 hour
    ing [10]                        ing Challenges
    OS Kernel Engineering           Compiling new OS Kernels and ∼ 5 minutes [7]
                                    checking if a specific metric has
                                    improved (performance, mem-
                                    ory, security)
    Real Chemical Synthesis         Checking if a proposed synthesis ∼< 1 hour - several days
                                    plan yields a given substance     - several weeks [43]
    Automatic Large Language        Checking whether a given LLM ∼< 1 day - several days
    Model Research                  recipe (training data and train- - several months [28]
                                    ing pipeline) yields an improved
                                    LLM




Table 11: Additional results table summarizing the scores of all tested models. All experiments
were conducted on the KernelBench GPU programming task with a fixed test set of size N = 100
problems from level 1. IR = Iterative Refinement; IB = Inductive Bias. Reported values are mean ±
standard deviation over 3 runs. Green bold values indicate statistically significant improvement of
+IB over IR (Welch’s t-test, one-tailed, p < 0.05). Bold = best overall, underline = second best (ties
allowed). COMP = Compilation Success, RUN = Runtime Success, CORR = Correctness.

 Model                        Method      COMP           RUN          CORR           Fast1         Fast2
 Qwen3-4B                     IR         0.52 ± 0.00   0.50 ± 0.00   0.05 ± 0.00   0.02 ± 0.00   0.00 ± 0.00
 Qwen3-4B                     +IB        0.54 ± 0.01   0.52 ± 0.01   0.02 ± 0.00   0.02 ± 0.00   0.00 ± 0.00
 Qwen3-8B                     IR         0.13 ± 0.00   0.11 ± 0.00   0.03 ± 0.00   0.01 ± 0.00   0.00 ± 0.00
 Qwen3-8B                     +IB        0.11 ± 0.00   0.09 ± 0.00   0.05 ± 0.00   0.03 ± 0.00   0.02 ± 0.00
 Qwen3-14B                    IR         0.22 ± 0.06   0.19 ± 0.03   0.04 ± 0.02   0.01 ± 0.01   0.01 ± 0.01
 Qwen3-14B                    +IB        0.34 ± 0.04   0.29 ± 0.05   0.11 ± 0.01   0.03 ± 0.01   0.02 ± 0.01
 Qwen3-32B                    IR         0.26 ± 0.05   0.23 ± 0.05   0.06 ± 0.01   0.00 ± 0.01   0.00 ± 0.01
 Qwen3-32B                    +IB        0.41 ± 0.02   0.39 ± 0.02   0.11 ± 0.02   0.02 ± 0.02   0.01 ± 0.01
 Qwen3-30B-A3B                IR         0.40 ± 0.00   0.38 ± 0.00   0.02 ± 0.00   0.00 ± 0.00   0.00 ± 0.00
 Qwen3-30B-A3B                +IB        0.53 ± 0.00   0.48 ± 0.00   0.12 ± 0.00   0.03 ± 0.00   0.02 ± 0.00
 Qwen3-Coder-30B-A3B          IR         0.60 ± 0.00   0.59 ± 0.00   0.22 ± 0.00   0.05 ± 0.00   0.02 ± 0.00
 Qwen3-Coder-30B-A3B          +IB        0.63 ± 0.00   0.59 ± 0.00   0.23 ± 0.00   0.01 ± 0.00   0.00 ± 0.00
 DeepSeek-Coder               IR         0.58 ± 0.00   0.50 ± 0.00   0.18 ± 0.00   0.03 ± 0.00   0.00 ± 0.00
 DeepSeek-Coder               +IB        0.59 ± 0.00   0.54 ± 0.00   0.20 ± 0.00   0.05 ± 0.00   0.03 ± 0.00
 deepseek-v3.1                IR         0.28 ± 0.01   0.26 ± 0.02   0.09 ± 0.01   0.05 ± 0.01   0.02 ± 0.02
 deepseek-v3.1                +IB        0.57 ± 0.08   0.55 ± 0.07   0.20 ± 0.03   0.09 ± 0.02   0.03 ± 0.01
 devstral-2512                IR         0.38 ± 0.02   0.33 ± 0.02   0.09 ± 0.01   0.05 ± 0.02   0.02 ± 0.01
 devstral-2512                +IB        0.69 ± 0.02   0.57 ± 0.01   0.14 ± 0.01   0.05 ± 0.01   0.02 ± 0.01
 gpt-oss-120b                 IR         0.53 ± 0.03   0.48 ± 0.05   0.21 ± 0.02   0.04 ± 0.01   0.02 ± 0.02
 gpt-oss-120b                 +IB        0.63 ± 0.05   0.56 ± 0.07   0.33 ± 0.05   0.11 ± 0.06   0.05 ± 0.03




                                                  21
Figure 7: Transition Counts for Devstral 2, from the base Trial 1 to the one based on classical iterative
refinement Trial 2.




Figure 8: Transition Counts for Devstral 2, from the base Trial 1 to the one based on Inductive Biases
Trial 3.



setting, inductive biases consistently outperforms iterative refinement, which is consistent with the
hypothesis. We also conducted a controlled experiment where adding additional domain data reduced
the effect of the inductive bias, in line with the ‘Bitter Lesson’ and further affirming that both data
solves problems, but also that data needs might become inhibitive.

I.1.1    Statistical significance for some models has low variance
For the Qwen-A30-A3B models as well as DeepSeek-Coder, standard deviations are reported as 0.00,
likely stemming from low (or non existent) variance during inference, making significance testing
trivial, but also potentially less reliable for these specific models. Overall this does not change the
results as we have clear statistical significance for the other results.


J   LLM usage

LLM usage was done for:

        1. Looking material up (similar to a Web Search)


                                                   22
2. Simple coding tasks (e.g. processing existing .csv files for better data analysis).
3. Minimal rewritting help (e.g. of a paragraph or sentence).
4. Help with Latex Table formatting.




                                            23
NeurIPS Paper Checklist
The checklist is designed to encourage best practices for responsible machine learning research,
addressing issues of reproducibility, transparency, research ethics, and societal impact. Do not remove
the checklist: The papers not including the checklist will be desk rejected. The checklist should
follow the references and follow the (optional) supplemental material. The checklist does NOT count
towards the page limit.
Please read the checklist guidelines carefully for information on how to answer these questions. For
each question in the checklist:

       • You should answer [Yes], [No], or [N/A].
       • [N/A] means either that the question is Not Applicable for that particular paper or the
         relevant information is Not Available.
       • Please provide a short (1–2 sentence) justification right after your answer (even for [N/A]).

The checklist answers are an integral part of your paper submission. They are visible to the
reviewers, area chairs, senior area chairs, and ethics reviewers. You will also be asked to include it
(after eventual revisions) with the final version of your paper, and its final version will be published
with the paper.
The reviewers of your paper will be asked to use the checklist as one of the factors in their evaluation.
While [Yes] is generally preferable to [No], it is perfectly acceptable to answer [No] provided a
proper justification is given (e.g., error bars are not reported because it would be too computationally
expensive” or “we were unable to find the license for the dataset we used”). In general, answering
[No] or [N/A] is not grounds for rejection. While the questions are phrased in a binary way, we
acknowledge that the true answer is often more nuanced, so please just use your best judgment and
write a justification to elaborate. All supporting evidence can appear either in the main paper or the
supplemental material, provided in appendix. If you answer [Yes] to a question, in the justification
please point to the section(s) where related material for the question can be found.
IMPORTANT, please:

      1. Claims
         Question: Do the main claims made in the abstract and introduction accurately reflect the
         paper’s contributions and scope?
         Answer: [Yes]
         Justification: The paper clearly introduces the proof of concept of FIL hypothesis and tests
         it carefully, see Results section.
         Guidelines:
             • The answer [N/A] means that the abstract and introduction do not include the claims
               made in the paper.
             • The abstract and/or introduction should clearly state the claims made, including the
               contributions made in the paper and important assumptions and limitations. A [No] or
               [N/A] answer to this question will not be perceived well by the reviewers.
             • The claims made should match theoretical and experimental results, and reflect how
               much the results can be expected to generalize to other settings.
             • It is fine to include aspirational goals as motivation as long as it is clear that these goals
               are not attained by the paper.
      2. Limitations
         Question: Does the paper discuss the limitations of the work performed by the authors?
         Answer: [Yes]
         Justification: Yes, see Appendix I.
         Guidelines:
             • The answer [N/A] means that the paper has no limitation while the answer [No] means
               that the paper has limitations, but those are not discussed in the paper.


                                                    24
     • The authors are encouraged to create a separate “Limitations” section in their paper.
     • The paper should point out any strong assumptions and how robust the results are to
       violations of these assumptions (e.g., independence assumptions, noiseless settings,
       model well-specification, asymptotic approximations only holding locally). The authors
       should reflect on how these assumptions might be violated in practice and what the
       implications would be.
     • The authors should reflect on the scope of the claims made, e.g., if the approach was
       only tested on a few datasets or with a few runs. In general, empirical results often
       depend on implicit assumptions, which should be articulated.
     • The authors should reflect on the factors that influence the performance of the approach.
       For example, a facial recognition algorithm may perform poorly when image resolution
       is low or images are taken in low lighting. Or a speech-to-text system might not be
       used reliably to provide closed captions for online lectures because it fails to handle
       technical jargon.
     • The authors should discuss the computational efficiency of the proposed algorithms
       and how they scale with dataset size.
     • If applicable, the authors should discuss possible limitations of their approach to
       address problems of privacy and fairness.
     • While the authors might fear that complete honesty about limitations might be used by
       reviewers as grounds for rejection, a worse outcome might be that reviewers discover
       limitations that aren’t acknowledged in the paper. The authors should use their best
       judgment and recognize that individual actions in favor of transparency play an impor-
       tant role in developing norms that preserve the integrity of the community. Reviewers
       will be specifically instructed to not penalize honesty concerning limitations.
3. Theory assumptions and proofs
  Question: For each theoretical result, does the paper provide the full set of assumptions and
  a complete (and correct) proof?
  Answer: [N/A]
  Justification: Not applicable.
  Guidelines:
     • The answer [N/A] means that the paper does not include theoretical results.
     • All the theorems, formulas, and proofs in the paper should be numbered and cross-
       referenced.
     • All assumptions should be clearly stated or referenced in the statement of any theorems.
     • The proofs can either appear in the main paper or the supplemental material, but if
       they appear in the supplemental material, the authors are encouraged to provide a short
       proof sketch to provide intuition.
     • Inversely, any informal proof provided in the core of the paper should be complemented
       by formal proofs provided in appendix or supplemental material.
     • Theorems and Lemmas that the proof relies upon should be properly referenced.
4. Experimental result reproducibility
  Question: Does the paper fully disclose all the information needed to reproduce the main ex-
  perimental results of the paper to the extent that it affects the main claims and/or conclusions
  of the paper (regardless of whether the code and data are provided or not)?
  Answer: [Yes]
  Justification: Methods, Experiments, and Appendix B all explain the results. Additionally
  data with LLM outputs is attached (to the allowed upload limit).
  Guidelines:
     • The answer [N/A] means that the paper does not include experiments.
     • If the paper includes experiments, a [No] answer to this question will not be perceived
       well by the reviewers: Making the paper reproducible is important, regardless of
       whether the code and data are provided or not.


                                           25
      • If the contribution is a dataset and/or model, the authors should describe the steps taken
         to make their results reproducible or verifiable.
      • Depending on the contribution, reproducibility can be accomplished in various ways.
         For example, if the contribution is a novel architecture, describing the architecture fully
         might suffice, or if the contribution is a specific model and empirical evaluation, it may
         be necessary to either make it possible for others to replicate the model with the same
         dataset, or provide access to the model. In general. releasing code and data is often
         one good way to accomplish this, but reproducibility can also be provided via detailed
         instructions for how to replicate the results, access to a hosted model (e.g., in the case
         of a large language model), releasing of a model checkpoint, or other means that are
         appropriate to the research performed.
      • While NeurIPS does not require releasing code, the conference does require all submis-
         sions to provide some reasonable avenue for reproducibility, which may depend on the
         nature of the contribution. For example
        (a) If the contribution is primarily a new algorithm, the paper should make it clear how
             to reproduce that algorithm.
        (b) If the contribution is primarily a new model architecture, the paper should describe
             the architecture clearly and fully.
        (c) If the contribution is a new model (e.g., a large language model), then there should
             either be a way to access this model for reproducing the results or a way to reproduce
             the model (e.g., with an open-source dataset or instructions for how to construct
             the dataset).
        (d) We recognize that reproducibility may be tricky in some cases, in which case
             authors are welcome to describe the particular way they provide for reproducibility.
             In the case of closed-source models, it may be that access to the model is limited in
             some way (e.g., to registered users), but it should be possible for other researchers
             to have some path to reproducing or verifying the results.
5. Open access to data and code
   Question: Does the paper provide open access to the data and code, with sufficient instruc-
   tions to faithfully reproduce the main experimental results, as described in supplemental
   material?
   Answer: [Yes]
   Justification: Data and part of code is already attached. The full code will be released upon
   publication.
   Guidelines:
      • The answer [N/A] means that paper does not include experiments requiring code.
      • Please see the NeurIPS code and data submission guidelines (https://neurips.cc/
         public/guides/CodeSubmissionPolicy) for more details.
      • While we encourage the release of code and data, we understand that this might not
         be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not
         including code, unless this is central to the contribution (e.g., for a new open-source
         benchmark).
      • The instructions should contain the exact command and environment needed to run to
         reproduce the results. See the NeurIPS code and data submission guidelines (https:
         //neurips.cc/public/guides/CodeSubmissionPolicy) for more details.
      • The authors should provide instructions on data access and preparation, including how
         to access the raw data, preprocessed data, intermediate data, and generated data, etc.
      • The authors should provide scripts to reproduce all experimental results for the new
         proposed method and baselines. If only a subset of experiments are reproducible, they
         should state which ones are omitted from the script and why.
      • At submission time, to preserve anonymity, the authors should release anonymized
         versions (if applicable).
      • Providing as much information as possible in supplemental material (appended to the
         paper) is recommended, but including URLs to data and code is permitted.
6. Experimental setting/details


                                             26
   Question: Does the paper specify all the training and test details (e.g., data splits, hyperpa-
   rameters, how they were chosen, type of optimizer) necessary to understand the results?
   Answer: [Yes]
   Justification: Sections: Method, Experiments and Appendix B specify these parameters.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The experimental setting should be presented in the core of the paper to a level of detail
         that is necessary to appreciate the results and make sense of them.
      • The full details can be provided either with the code, in appendix, or as supplemental
         material.
7. Experiment statistical significance
   Question: Does the paper report error bars suitably and correctly defined or other appropriate
   information about the statistical significance of the experiments?
   Answer: [Yes]
   Justification: All results tables include statistical testing using Welch-T testing and p-value
   of 0.05; all runs reported in the paper are N=3.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The authors should answer [Yes] if the results are accompanied by error bars, confidence
         intervals, or statistical significance tests, at least for the experiments that support the
         main claims of the paper.
      • The factors of variability that the error bars are capturing should be clearly stated (for
         example, train/test split, initialization, random drawing of some parameter, or overall
         run with given experimental conditions).
      • The method for calculating the error bars should be explained (closed form formula,
         call to a library function, bootstrap, etc.)
      • The assumptions made should be given (e.g., Normally distributed errors).
      • It should be clear whether the error bar is the standard deviation or the standard error
         of the mean.
      • It is OK to report 1-sigma error bars, but one should state it. The authors should
         preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis
         of Normality of errors is not verified.
      • For asymmetric distributions, the authors should be careful not to show in tables or
         figures symmetric error bars that would yield results that are out of range (e.g., negative
         error rates).
      • If error bars are reported in tables or plots, the authors should explain in the text how
         they were calculated and reference the corresponding figures or tables in the text.
8. Experiments compute resources
   Question: For each experiment, does the paper provide sufficient information on the com-
   puter resources (type of compute workers, memory, time of execution) needed to reproduce
   the experiments?
   Answer: [Yes]
   Justification: Appendix B contains the information.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The paper should indicate the type of compute workers CPU or GPU, internal cluster,
         or cloud provider, including relevant memory and storage.
      • The paper should provide the amount of compute required for each of the individual
         experimental runs as well as estimate the total compute.
      • The paper should disclose whether the full research project required more compute
         than the experiments reported in the paper (e.g., preliminary or failed experiments that
         didn’t make it into the paper).


                                             27
 9. Code of ethics
    Question: Does the research conducted in the paper conform, in every respect, with the
    NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?
    Answer: [Yes]
    Justification: Yes, (additionally, no human study was conducted.)
    Guidelines:
       • The answer [N/A] means that the authors have not reviewed the NeurIPS Code of
          Ethics.
       • If the authors answer [No], they should explain the special circumstances that require a
          deviation from the Code of Ethics.
       • The authors should make sure to preserve anonymity (e.g., if there is a special consid-
          eration due to laws or regulations in their jurisdiction).
10. Broader impacts
    Question: Does the paper discuss both potential positive societal impacts and negative
    societal impacts of the work performed?
    Answer: [Yes]
    Justification: We don’t see major impact of this work on society as of now, see Appendix H
    for a brief comment.
    Guidelines:
       • The answer [N/A] means that there is no societal impact of the work performed.
       • If the authors answer [N/A] or [No], they should explain why their work has no societal
          impact or why the paper does not address societal impact.
       • Examples of negative societal impacts include potential malicious or unintended uses
          (e.g., disinformation, generating fake profiles, surveillance), fairness considerations
          (e.g., deployment of technologies that could make decisions that unfairly impact specific
          groups), privacy considerations, and security considerations.
       • The conference expects that many papers will be foundational research and not tied
          to particular applications, let alone deployments. However, if there is a direct path to
          any negative applications, the authors should point it out. For example, it is legitimate
          to point out that an improvement in the quality of generative models could be used to
          generate Deepfakes for disinformation. On the other hand, it is not needed to point out
          that a generic algorithm for optimizing neural networks could enable people to train
          models that generate Deepfakes faster.
       • The authors should consider possible harms that could arise when the technology is
          being used as intended and functioning correctly, harms that could arise when the
          technology is being used as intended but gives incorrect results, and harms following
          from (intentional or unintentional) misuse of the technology.
       • If there are negative societal impacts, the authors could also discuss possible mitigation
          strategies (e.g., gated release of models, providing defenses in addition to attacks,
          mechanisms for monitoring misuse, mechanisms to monitor how a system learns from
          feedback over time, improving the efficiency and accessibility of ML).
11. Safeguards
    Question: Does the paper describe safeguards that have been put in place for responsible
    release of data or models that have a high risk for misuse (e.g., pre-trained language models,
    image generators, or scraped datasets)?
    Answer: [N/A]
    Justification: Not applicable.
    Guidelines:
       • The answer [N/A] means that the paper poses no such risks.
       • Released models that have a high risk for misuse or dual-use should be released with
          necessary safeguards to allow for controlled use of the model, for example by requiring
          that users adhere to usage guidelines or restrictions to access the model or implementing
          safety filters.


                                             28
       • Datasets that have been scraped from the Internet could pose safety risks. The authors
         should describe how they avoided releasing unsafe images.
       • We recognize that providing effective safeguards is challenging, and many papers do
         not require this, but we encourage authors to take this into account and make a best
         faith effort.
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [Yes]
    Justification: See Appendix B.
    Guidelines:
       • The answer [N/A] means that the paper does not use existing assets.
       • The authors should cite the original paper that produced the code package or dataset.
       • The authors should state which version of the asset is used and, if possible, include a
         URL.
       • The name of the license (e.g., CC-BY 4.0) should be included for each asset.
       • For scraped data from a particular source (e.g., website), the copyright and terms of
         service of that source should be provided.
       • If assets are released, the license, copyright information, and terms of use in the
         package should be provided. For popular datasets, paperswithcode.com/datasets
         has curated licenses for some datasets. Their licensing guide can help determine the
         license of a dataset.
       • For existing datasets that are re-packaged, both the original license and the license of
         the derived asset (if it has changed) should be provided.
       • If this information is not available online, the authors are encouraged to reach out to
         the asset’s creators.
13. New assets
    Question: Are new assets introduced in the paper well documented and is the documentation
    provided alongside the assets?
    Answer: [Yes]
    Justification: Software only. On release it will be documented.
    Guidelines:
       • The answer [N/A] means that the paper does not release new assets.
       • Researchers should communicate the details of the dataset/code/model as part of their
         submissions via structured templates. This includes details about training, license,
         limitations, etc.
       • The paper should discuss whether and how consent was obtained from people whose
         asset is used.
       • At submission time, remember to anonymize your assets (if applicable). You can either
         create an anonymized URL or include an anonymized zip file.
14. Crowdsourcing and research with human subjects
    Question: For crowdsourcing experiments and research with human subjects, does the paper
    include the full text of instructions given to participants and screenshots, if applicable, as
    well as details about compensation (if any)?
    Answer: [N/A]
    Justification: No human studies were conducted.
    Guidelines:
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
         with human subjects.


                                             29
       • Including this information in the supplemental material is fine, but if the main contribu-
          tion of the paper involves human subjects, then as much detail as possible should be
          included in the main paper.
       • According to the NeurIPS Code of Ethics, workers involved in data collection, curation,
          or other labor should be paid at least the minimum wage in the country of the data
          collector.
15. Institutional review board (IRB) approvals or equivalent for research with human
    subjects
    Question: Does the paper describe potential risks incurred by study participants, whether
    such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
    approvals (or an equivalent approval/review based on the requirements of your country or
    institution) were obtained?
    Answer: [N/A]
    Justification: No human crowdsourcing was done.
    Guidelines:
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
          with human subjects.
       • Depending on the country in which research is conducted, IRB approval (or equivalent)
          may be required for any human subjects research. If you obtained IRB approval, you
          should clearly state this in the paper.
       • We recognize that the procedures for this may vary significantly between institutions
          and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the
          guidelines for their institution.
       • For initial submissions, do not include any information that would break anonymity (if
          applicable), such as the institution conducting the review.
16. Declaration of LLM usage
    Question: Does the paper describe the usage of LLMs if it is an important, original, or
    non-standard component of the core methods in this research? Note that if the LLM is used
    only for writing, editing, or formatting purposes and does not impact the core methodology,
    scientific rigor, or originality of the research, declaration is not required.
    Answer: [Yes]
    Justification: Both in OpenReview and in the paper, see Appendix J.
    Guidelines:
       • The answer [N/A] means that the core method development in this research does not
          involve LLMs as any important, original, or non-standard components.
       • Please refer to our LLM policy in the NeurIPS handbook for what should or should not
          be described.




                                             30
