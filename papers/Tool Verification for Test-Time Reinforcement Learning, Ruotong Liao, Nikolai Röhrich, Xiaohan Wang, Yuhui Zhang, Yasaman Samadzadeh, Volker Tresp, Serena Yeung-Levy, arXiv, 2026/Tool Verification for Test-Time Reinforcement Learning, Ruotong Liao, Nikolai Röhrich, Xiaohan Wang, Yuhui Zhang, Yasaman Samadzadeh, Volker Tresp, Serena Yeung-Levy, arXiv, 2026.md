                                                                          Tool Verification for Test-Time
                                                                             Reinforcement Learning

                                                      Ruotong Liao1,3,∗ Nikolai Röhrich1,∗ Xiaohan Wang2,† Yuhui Zhang2
                                                         Yasaman Samadzadeh1 Volker Tresp1,3 Serena Yeung-Levy2,†
                                                            1                                                                                     2                                            3
                                                                Ludwig-Maximilians University of Munich                                                Stanford University                         MCML
arXiv:2603.02203v2 [cs.AI] 26 Aug 2026




                                                                                                                            Abstract

                                                     Test-time reinforcement learning (TTRL) has emerged as a promising paradigm for
                                                     Recursive Self-Improving AI (RSI) by adapting Large Reasoning Models (LRMs)
                                                     on unlabeled test inputs, using self-consensus rewards derived from majority vot-
                                                     ing over sampled rollouts. However, majority voting can mistake popularity for
                                                     correctness: a spurious yet high-frequency unverified consensus may become a
                                                     biased reward signal, causing test-time RL to reinforce frequent but wrong an-
                                                     swers and collapse into an incorrect mode. We address this false-popular failure
                                                     mode with T3 RL (Tool-Verification for Test-Time Reinforcement Learning), a
                                                     verification-aware test-time RL framework. T3 RL grounds pseudo-label construc-
                                                     tion in external tool evidence. Concretely, a verifier utilizes external tool evidence
                                                     (e.g., from code execution) to upweight verified rollouts during a verification-aware
                                                     voting, producing more reliable pseudo-labels for training. Across various math
                                                     difficulties (MATH-500, AMC, and AIME 2024) and diverse backbone families,
                                                     T3 RL significantly improves over TTRL, with better performance on harder prob-
                                                     lems. T3 RL is positioned as a verified online data synthesizer, highlighting the role
                                                     of tool verification in reliable online adaptation. T3 RL is extensible to verifiable
                                                     domains and provides training and inference efficiency.


                                                       T3RL: Tool Verification for Test Time Reinforcement Learning
                                                                                                                                                                          0                   20                 40
                                                            Query                           {"! }                                   {"! }
                                                                             LLM                                                                      "$!
                                                                                             ""                                         ""                                                         31,6
                                                                                                                                                               AIME




                                                                                                                                                                                       17,1
                                                       Test Data                            "#                  Verifier                "#                                      10,7
                                                      (Unlabeled)
                                                                                            "$                                 "$
                                                                                                        (e.g. Code Interpreter
                                                                                             …            Integrated LLM )     …                                              4,1
                                                                                                                                                               AMC




                                                                                                                                                                               7,3                 Qwen-
                                                                                                                                                                                       17,8        Math-2.5-
                                                                                                    Reinforcement Learning
                                                                                                                                                                                                   1.5B
                                                                                                                                                               MATH-500




                                                                                    Test Time Verification (e.g. Majority Voting)                                             2,2                  Qwen2.5-
                                                                                                                                                                              2,8                  1.5B
                                                             True Label                                         C                            Estimated Label                  5,5

                                                             Sampled Predictions       A A          B   B   B       B   C   C   C   D                                                              Llama-3.2-
                                                     TTRL                                                                                    B   Skewed ❌                     6,3                  1B-Instruct
                                                                                                                                                               Avg




                                                             Estimated Rewards          0   0       1   1   1       1   0   0   0   0                                         4,7
                                                                                                                                                                                 9,3
                                                             Verified Predictions      A A          B   B   B       B   C   C   C   D
                                                     T3RL                                                                                    C   Reliable ✅
                                                             Estimated Rewards          0   0       0   0   0       0   1   1   1   0                                     Relative Accuracy Gain (%)


                                         Figure 1: The concept of T3 RL. Top: T3 RL introduces test-time verification into self-evolvement
                                         via tool-executed evidence (e.g., code interpreter) to stabilize training with verified rollouts. Bottom:
                                         Majority-vote pseudo-labels can be spurious. T3 RL introduces verification to suppress false-popular
                                         pseudo-labels. Right: T3 RL achieves consistent gains with evidence-grounded test-time training.

                                            ∗ Equal contribution.
                                            † Correspondence: liao@dbs.ifi.lmu.de; xhanwang@stanford.edu.

                                             Code: https://github.com/mayhugotong/T3RL


                                         Preprint.
1   Introduction
Modern language models often know more than they reliably say [Orgad et al., 2025, Wang et al.,
2023]. Pre-training and post-training endow models with broad factual and reasoning capabilities,
yet a single inference-time generation may fail to express them. This gap has motivated test-time
scaling [Snell et al., 2024b, Muennighoff et al., 2025]: improving model performance by allocating
additional computation at inference through sampling, search, verification, or aggregation [Snell
et al., 2024a, Wu et al., 2025, Chang et al., 2025, Venktesh et al., 2025]. A key observation behind
these methods is that, even when one rollout is unreliable, the distribution over many rollouts may
contain a useful signal [Kang et al., 2026, Mekala et al., 2024, Lifshitz et al., 2025a].
Test-Time Reinforcement Learning (TTRL) turns this signal into online learning [Zuo et al., 2025]
for Recursive Self-Improving AI (RSI). Given an unlabeled test input, a model samples multiple
reasoning traces, uses majority voting to infer a pseudo-label, and reinforces rollouts that agree with
this majority answer. When the correct answer is the dominant mode of the model distribution, this
provides a simple label-free reward signal that sharpens the model at test time.
However, the majority answer is not always correct. If the model has a systematic bias, many rollouts
may converge to the same wrong solution. In this case, voting selects popularity rather than truth:
incorrect rollouts receive positive reward, correct minority rollouts are suppressed, and test-time RL
amplifies the error. We call this failure mode false-popular mode collapse. As shown in Figure 1, a
frequent wrong answer can dominate the vote over a less frequent correct one, causing self-training
to reinforce a false mode. Worse, once mode collapse occurs, it becomes even harder to self-correct.
This failure arises because self-consistency forms a closed loop: the model generates candidates,
votes on them, and learns from its own vote. To break this loop, test-time learning needs evidence
beyond the model’s internal distribution. Many reasoning tasks provide exactly such evidence. Math
solutions can be checked by computation, code can be executed against tests, and structured reasoning
can be validated by external tools. These tasks are hard to solve but easy to verify.
We therefore ask: Can label-free test-time reinforcement learning be made robust to false-
popular mode collapse? To answer this question, we propose T3 RL, Tool Verification for Test-
Time Reinforcement Learning. Rather than relying on majority vote alone, T3 RL uses tools to
verify candidate rollouts and constructs pseudo-labels through verification-weighted voting. In short,
the model should not only ask which answer is most frequent, but which answers can be verified.
Concretely, T3 RL adds three components to TTRL. (1) A Verifier extracts the final answer from
each rollout and translates checkable reasoning steps into executable code. (2) A Verification Tool,
such as a Python interpreter, executes the code and returns evidence about the rollout’s validity. (3)
A Verification Weight then gives verified rollouts greater vote mass when constructing the pseudo-
label. The reward remains label-free, but is grounded in external tool feedback rather than raw
self-consensus.
We evaluate T3 RL on MATH500, AMC, and AIME2024. T3 RL consistently improves over majority-
vote TTRL, with larger gains on harder benchmarks and a maximum relative improvement of 31.6%
on AIME2024 (§5.2). We point out that T3 RL is implicitly a verified synthetic data generator on
the fly (§6.1). Extensive ablations validate the importance of the Verifier, the Verification Tool, and
the Verification Weight (§5.3). We also demonstrate that T3 RL is more robust (Figure 8b), test-time
compute-efficient (Table 4), and can be improved by stronger verifiers (Figure 6).
More broadly, T3 RL offers a plug-and-play framework for reliable test-time learning on verifiable
tasks. While we instantiate it primarily with code-based verification for mathematical reasoning, our
non-math Knights-and-Knaves experiment demonstrates that the same principle extends to ssymbolic
verification with logical puzzles using SMT-LIB2 and Z3 (§6.2). We envision further extensions to
code execution, theorem checkers, simulators, retrieval systems, and other task-specific verification
tools.

2   Related Works
Verification for Test Time Scaling Verification in test time scaling uses external verifiers to
evaluate the quality of additional computation and select the best output from multiple candidates
during inference. Verification mechanisms include reward models [Uesato et al., 2022, Lightman


                                                  2
    T3RL: Tool Verification for Test Time Reinforcement Learning                            Tool
                                                                                                                            Pseudo
                                                                                                                             Label
                                                            Verifier                                                 w%
      Query       LLM        {"! }       Think step                                                                              %
                                                                                                                                 y*
                                         by step …                                                        {"! }
                                                       Tool Integrated LLM                                        Verification
                              ""
                                                                                       Code Interpreter    ""      Weight
  Test Data                   "#         Adding 2 and 3             a = 2
 (Unlabeled)                             equals 5 …                 b = 3                                 "#
                              "$         Then multiply by           c = a + b
                                         4 equals 20 …              print(c*4 == 20)                      "$
                              …
                                                                                                           …
                                         Adding 2 and 3             a = 2
                                         equals 6 …                 b = 3
                                         Then multiply by           c = a + b
                                         4 equals 24
                                                                    print(c*4 == 24)




                                                            Reinforcement Learning


Figure 2: T3 RL: Tool Verification for Test-Time Reinforcement Learning. Verifier: an LLM
verifier parses each sampled rollout yi into a candidate answer ai and, with tool feedback, produces
a binary validity flag vi ∈ {0, 1}. Tool verification: the verifier compiles the rollout’s claimed
computations into lightweight Python and queries a code interpreter to obtain executable evidence.
Verification-weighted majority voting: unverified rollouts receive unit vote mass, and verified rollouts
receive ω vote mass. A verification-aware pseudo-label ỹ ∗ is formed by weighted voting.


et al., 2023, Cobbe et al., 2021], generative verifiers [Zhang et al., 2024], symbolic checks [Ling
et al., 2023], or multi-agent systems [Jin et al., 2025, Lifshitz et al., 2025b]. Recently, tool-integrated
reasoning (TIR) [Gou et al., 2024] has brought a new perspective to tool-integrated verification
[Mekala et al., 2024, Kang et al., 2026], formalizing tool use as an additional robust evidence.
However, none of the prior works explore verification in test-time training; we are the first to turn
sampled rollouts into online, evidence-labeled training instances through verification and shape the
training process as a verified data synthesizer on-the-fly.

Test-Time Training Test Time Training (TTT) adapts model parameters during inference to
handle distribution shifts on new tasks [Sun et al., 2020, 2024b,a, Behrouz et al., 2024, Liu et al.,
2021], in domains like video generation and understanding [Wang et al., 2025a, Dalal et al., 2025],
large language models [Hardt and Sun, 2023], or scientific discovery [Yuksekgonul et al., 2026].
Recently, TTT advanced to test-time reinforcement learning (TTRL) [Zuo et al., 2025] that combines
unsupervised reinforcement learning [Prasad et al., 2024, Zhang et al., 2025] and reinforcement
learning with verifiable rewards (RLVR) [Zeng et al., 2025, Wang et al., 2025b], which has been
widely discussed in the era of self-evolving artificial intelligence. However, in the face of the challenge
that spurious reward estimation presents to test-time training, none of the existing work has discussed
verification. To the best of our knowledge, we are the first to propose test-time verification for
test-time training, especially tool-assisted verification for evidence-grounded test-time reinforcement
learning. This provides a broader vision of agentic systems that increasingly rely on tool interaction,
yet require reliable reward signals to for stable online learning.


3      The Failure Mode: How Unverified Consensus Induces Reward Bias

3.1     Test Time Reinforcement Learning

Unlike traditional RL, where models learn from known reward signals, TTRL operates on unlabeled
test data without access to explicit supervision. TTRL is defined as follows:
Given a state represented by the prompt x, the model acts by producing an output y sampled
from a policy πθ (y | x), parameterized by θ. To construct a reward signal without ground-truth
labels, TTRL generates multiple candidate outputs {y1 , y2 , . . . , yN } through repeated sampling. A
consensus output y ∗ is derived by majority voting, serving as a proxy for the optimal estimation. The
environment then provides a reward r(y, y ∗ ) based on the alignment between the sampled estimation
y and the consensus estimation y ∗ . The RL objective is thus to maximize the expected reward:

                                         max Ey∼πθ (·|x) [r(y, y ∗ )],                                                                (1)
                                              θ



                                                                  3
True Label                                   C                       Estimated Label
1st Round                      False-Popular Predictions
Sampled Predictions    A A       B   B   B       B   C   C   C   D
                                                                       B is good!
Estimated Rewards      0   0     1   1   1       1   0   0   0   0
…




Nth Round                      Cycle of Reinforced Bias
Sampled Predictions    A   B     B   B   B       B   B   B   C   D     B is really
Estimated Rewards      0   1     1   1   1       1   1   1   0   0       good!



                    (a) Failure case of TTRL.                                                 (b) Success case of T3 RL.

Figure 3: Unverified consensus versus tool-verified consensus. (a) Spurious reward in the reinforced
cycle of TTRL: the false-popular answer is rewarded and its vote share grows over rounds. (b) Tool
verification can adjust the false-popular answer.


and parameters θ are updated through gradient ascent:
                                                             θ ← θ + η∇θ Ey∼πθ (·|x) [r(y, y ∗ )],                         (2)
where η denotes the learning rate.

3.2     Spurious Majority as a Biased Pseudo-Label

Self-consensus can estimate wrong labels. Let the gener-

                                                                                                False-majority share
                                                                  80%                  73.33%
ator induce a distribution over final answers, and consider two
                                          ⋆
competing modes: the correct answer y and an incorrect but        60%          46.07%
high-frequency answer ỹ, e.g. B and C in Figure 3a respectively. 40% 25.85%
If the win probability of B over C is non-zero, the majority vote 20%
can select ỹ as the pseudo-label. We measure the fraction of         MATH-500  AMC   AIME 2024
questions for which the unverified majority answer is wrong
(Figure 4) and the fraction for which verification-weighted Figure 4: False-majority share
voting changes that answer (Figure 3b). The false-majority across benchmarks.
share rises sharply with difficulty.

Self-reinforcing feedback loop and incorrect mode collapse. Once the pseudo-label is set to the
false-popular ỹ, the majority-based reward assigns positive reinforcement to rollouts that agree with
the false signal ỹ and zero out rewards for truthful rollouts. The RL update increases the likelihood
of sampling ỹ in subsequent rollouts, which further increases its vote share, making the pseudo-label
even more confidently wrong. This self-reinforcing dynamic can drive TTRL toward incorrect mode
collapse. Furthermore, once mode collapse occurs, the model becomes even harder to self-correct in
an echo chamber.

4     Method: Tool Verification for Test Time Reinforcement Learning
To prevent this failure mode, we present T3 RL, an RL framework which integrates tool verification
into the aggregation mechanism of test-time RL, thus achieving grounded and more robust reward
estimation. Specifically, T3 RL has three core components: (1) An external Verifier, an LLM that is
tasked with verifying a given reasoning trace by compiling the trace into executable Python code,
and judging its validity based on the execution output (§4.1); (2) The Verification Tool, a code
interpreter that executes the generated Python program and returns signals to the verifier (§4.2); (3)
The Verification Weight, which is used to replace the majority vote with a verification-aware weighted
vote that boosts the voting power of verified rollouts. (§4.3).

4.1     Verifier

A verifier V is designed to evaluate each rollout before aggregation derives the estimated consensus
label y ∗ :


                                                                                       4
Verifier. Given an input prompt x, we sample N rollouts {yi }N
                                                             i=1 ∼ πθ (· | x) and extract the
rollout’s own final answer from each rollout,
                                       âi = Extract(yi ),           âi ∈ A                          (3)
V then evaluates each rollout and returns only a validity flag
                                               (vi ) = V(x, yi , ti ),                                (4)
where vi ∈ {0, 1} indicates whether the rollout passes executable checks. ti represents the tool output
from the verification tool T used by the verifier.
In T3 RL, V is implemented as an LLM-based verifier that performs the following tasks: 1) generating
the tool-calling query, by transforming the rollout rationale into a lightweight python program; 2) the
execution of the verification tool (§4.2), and 3) returning the verification validity results. Note that
the verifier provides a reliability signal for âi .

4.2   Verification Tool

A verification tool T provides external, deterministic, and executable evidence to assist the verifier V
by offloading specific verification tasks from V to an external tool.

Tool execution as external evidence. For math problems, many rollouts hinge on intermediate
correctness (e.g., arithmetic computations, calculation hallucinations, etc). In T3 RL, tool verification
is initiated as a code interpreter T , that is an executable checker that evaluates a verifier-generated
Python program and returns the output of the executed code
                                             ti = T (Code(x, yi )).                                   (5)

The verifier then contrasts the tool result with the rollout’s extracted answer âi and produces a
tool-verified validity indicator
                                        vi = 1[ti = âi ] .                                    (6)

4.3   Verification Weight

Heuristic Weighting. In standard TTRL, the consensus label is derived via simple majority voting,
where every reasoning path contributes equally regardless of its logical soundness. However, in our
framework, rollouts that pass the tool verification, i.e. for which vi = 1, are heuristically assumed to
be more reliable than those that do not. Since the ground truth is inaccessible at test time, we cannot
calculate the exact probability of correctness for verified rollouts. Instead, we introduce a Verification
Weight hyperparameter, ω, to quantify the voting power of tool-verified traces.

Verification-Aware Consensus. We modify the aggregation mechanism to use a verification-
weighted majority vote. To maintain the diversity of rollouts, we ensure that each rollout maintains
its contribution by setting the default weight to 1. For a set of rollouts, we assign a weight wi to each
derived answer âi based on the verification indicator vi :
                                           wi = (1 − vi ) · 1 + vi · ω,                               (7)
where ω ≥ 1 is a fixed scalar hyperparameter. This ensures that unverified rollouts retain a unit vote,
while each verified rollout contributes an upweight of ω votes. The verification-aware consensus
label ỹ ∗ is then obtained by maximizing the total weighted vote mass:
                                                         N
                                                         X
                                       ∗
                                  ỹ       = arg max           wi · 1[âi = a].                       (8)
                                                   a∈A
                                                         i=1

This mechanism allows T3 RL to shift the consensus derivation from the distribution of the most
frequent answer in the whole observed candidate set A towards the verified consensus (see Figure 3b),
provided that the verified group possesses sufficient cumulative weight.

Reward Calculation. Consistent with standard TTRL, the final reward signal remains binary but
is now anchored to the robust, verification-aware consensus ỹ ∗ . The reward for the i-th rollout is
computed as:
                                         riv = 1[âi = ỹ ∗ ].                                    (9)


                                                         5
Table 1: Main performance of T3 RL. (a) Improvement across benchmark and backbone models.
(b) Difficulty breakdown performance on MATH-500 (L5 is the hardest). The relative improvement
of T3 RL over TTRL increases with difficulty level (Figure 5).
                         (a) Main results                                                              (b) MATH-500 difficulty breakdown.
 Model / Method          AIME 2024       AMC        MATH-500        Avg                                             L1        L2        L3        L4        L5
                                 Math Model                                         Qwen-2.5-Math-1.5B             25.9       33.0     36.3      32.5      22.3
 Qwen-2.5-Math-1.5B       7.7 ± 2.0    28.6 ± 4.5   32.7 ± 2.7   23.0 ± 1.9         w/ TTRL                        95.0       88.0     85.0      69.7      47.0
  w/ TTRL                15.8 ± 2.1    48.9 ± 1.6   73.0 ± 3.8   45.9 ± 1.5         w/ T3 RL                       95.2       88.2     87.3      72.0      49.0
  w/ T3 RL               20.8 ± 1.6    50.9 ± 2.7   74.6 ± 3.2   48.8 ± 1.5
                                                                                    Rel. (% over Baseline)        ↑267.6%   ↑167.3%   ↑140.5%   ↑121.5%   ↑119.7%
                                Vanilla Model
                                                                                    Rel. (% over TTRL)             ↑0.2%     ↑0.2%     ↑2.7%     ↑3.3%     ↑4.3%
 Qwen-2.5-1.5B            0.2 ± 1.2     0.6 ± 2.2    7.7 ± 2.0    2.8 ± 1.1
  w/ TTRL                 3.5 ± 1.2    28.6 ± 4.5   63.2 ± 3.5   31.8 ± 1.9
  w/ T3 RL                4.1 ± 1.2    30.7 ± 3.7   65.0 ± 2.1   33.3 ± 1.5        Figure 5: Relative gains across MATH-500 levels.
 Qwen-3-4B                0.0 ± 0.0    12.5 ± 4.4   50.4 ± 3.5   21.0 ± 1.9                                                                                16
  w/ TTRL                36.4 ± 1.9    71.7 ± 3.0   88.4 ± 1.4   65.5 ± 1.3                     300




                                                                                                                                                                  Additional Gain (%)
                                                                                                                                                  T3 RL




                                                                              Improvement (%)
  w/ T3 RL               40.0 ± 1.6    74.2 ± 2.8   89.5 ± 1.4   67.9 ± 1.2                                                              TTRL
                                                                                                250                                                        12
                                Instruct Model                                                                                                    +9.0%
                                                                                                                             +6.3%     +7.1%               8
 Llama-3.2-1B-Instruct    0.8 ± 0.0     4.2 ± 2.6    4.4 ± 1.5    3.1 ± 1.0                     200
   w/ TTRL                7.5 ± 2.5    16.9 ± 1.6   40.0 ± 1.6   21.5 ± 1.1
   w/ T3 RL               8.3 ± 2.4    19.9 ± 0.9   42.2 ± 2.6   23.5 ± 1.2                     150                                                        4
 Llama-3.2-3B-Instruct    6.0 ± 1.4    19.4 ± 1.8   43.9 ± 2.1   23.1 ± 1.0
                                                                                                        +0.8%     +0.6%
   w/ TTRL               13.3 ± 3.8    31.3 ± 4.0   61.6 ± 5.1   35.4 ± 2.5                                                                                0
   w/ T3 RL              17.1 ± 1.2    34.2 ± 2.7   63.3 ± 3.3   38.2 ± 1.5
                                                                                                       MATH-L1   MATH-L2    MATH-L3   MATH-L4    MATH-L5




Training objective. We keep the TTRL update of Eq. (2) unchanged in form, replacing the majority-
vote pseudo-label y ∗ with the verification-aware consensus ỹ ∗ of Eq. (8) and its induced reward,
Eq. (9):
              max Ey∼πθ (·|x) [rv (y, ỹ ∗ )] , θ ← θ + η∇θ Ey∼πθ (·|x) [rv (y, ỹ ∗ )] ,      (10)
                            θ
             ∗
where ỹ is held fixed within each update, and we optimize this objective with GRPO in practice.


5     Experiments

5.1      Experimental Setup

Benchmarks We evaluate T3 RL on 3 mathematical reasoning benchmarks: AIME 2024 [Li et al.,
2024], AMC [Li et al., 2024], and MATH-500 [Hendrycks et al., 2021].

Models. We evaluate T3 RL under the test-time reinforcement learning setting across diverse
backbone configurations spanning model families, alignment regimes, and scales (1B–4B), which
appeals to the call to validate methods on diverse models [Shao et al., 2025]. Our experiments cover
both base and instruction-tuned models, as well as math-specialized backbones. Concretely, we study
LRMs from the Qwen and LLaMA families: (1) Vanilla: Qwen2.5-1.5B [Qwen and el al, 2024]
and Qwen-3-4B [Yang et al., 2025]; (2) Math: Qwen2.5-Math-1.5B [Qwen and el al, 2024]; (3)
Instruct: Llama-3.2-1B-Instruct and Llama-3.2-3B-Instruct [Grattafiori and el al, 2024].

Evaluation Setup We apply T3 RL to each benchmark utilizing a maximum token limit of 2,560.
For our main experiments, we follow the DeepSeek-R1 [Guo et al., 2025] protocol: we evaluate
each experiment 4 times (temperature 0.6, top-p 0.95) and report pass@1 as the average correctness,
formalized as: For AIME 2024, whose test set is small, we average 16 independent evaluations; for
AMC and MATH-500 we average 4. The reported ± values are standard deviations aross runs.
                                                                                                       k
                                                                                                    1X
                                                                   pass@1 =                               pi ,
                                                                                                    k i=1

where pi indicates if response i is correct.

Baselines We compare our method against base models, as well as against TTRL [Zuo et al., 2025],
where we report the original results where possible. For experiments where TTRL results are not
available, we reproduce training runs using the implementation details in Zuo et al. [2025].


                                                                                                6
Implementation Details We implement T3 RL using GRPO [Shao et al., 2024] on each benchmark,
training the policy model via AdamW with a cosine schedule (peak learning rate: 5 × 10−7 ). To
balance performance with computational efficiency, we follow TTRL [Zuo et al., 2025] in employing
a vote-then-sample strategy: 64 responses are initially generated for label estimation (temperature
0.6) and downsampled to 32 for training. The maximum token length is 2,560. Regarding the verifier
model, we find that we can restrict the generation length to 1,024 tokens, since code snippets are
relatively short. We also use a temperature of 0.6 for the verifier across all benchmarks. Training
runs are conducted on 8 NVIDIA A100 GPUs, with varying episode counts based on dataset size: 10
(MATH-500), 30 (AMC), and 80 (AIME 2024). The pseudo code is listed in Appendix A and the
system prompt is in Appendix B.

5.2          Main Results

Table 1 shows that T3 RL repeatedly outperforms TTRL across all evaluated models and benchmarks,
supporting our central hypothesis that verification-shaped majority voting mitigates unverified-
consensus bias during test-time RL. Across the 15 paired T3 RL–TTRL model–benchmark compar-
isons, T3 RL wins all 15.

Consistent gains across benchmarks and model types. T3 RL improves over TTRL on all three
evaluated benchmarks, spanning an easy-to-hard spectrum from MATH-500 (easiest), to AMC
(medium), to AIME 2024 (hardest). T3 RL consistently improves over TTRL across five backbones
spanning three regimes (math, vanilla, instruction-tuned) and two scales (1B–4B): the largest gains
are on AIME 2024 for Qwen-Math-1.5B (+31.6%) and Qwen2.5-1.5B (+17.1%), and on AMC
for Llama-3.2-1B-Instruct (+17.8%). The benefit is tied with three standing out trends:

Math-specialised backbones, harder benchmarks, and larger models benefit most.

              • (i) Math-specialised models benefit more. Qwen-Math-1.5B achieves a larger average gain
                over TTRL than the vanilla Qwen2.5-1.5B (+6.3% vs. +4.7%): math backbones generate
                longer calculation chains whose small arithmetic slips are precisely the kind of error that
                executable checks can catch.
              • (ii) Harder benchmarks benefit more. Within each backbone, gains peak on AIME 2024 (e.g.,
                +31.6% for Qwen-Math-1.5B) and on the hardest MATH-500 level L5: longer computation
                chains accumulate errors that deterministic tool execution can still verify, preserving signal
                where self-consensus degrades.
              • (iii) Gains scale to larger backbones. On Llama-3.2-3B-Instruct AIME rises from 13.3
                to 17.1 (+28.6%); on the much stronger Qwen-3-4B where TTRL already achieves 36.4,
                it reaches 40.0 (+9.9%). The gain is largely preserved under self-verification (+9.3% /
                +27.1%, Table 2), so the contribution scales with backbone capability rather than coming
                from external-coder distillation.

5.3          Ablation Studies

This section presents an analysis of the three key factors that support T3 RL: (1) test-time verification,
(2) tool-assisted verification, and (3) verification-weighted majority voting. Unless otherwise speci-
fied, we run ablations on Qwen-Math-1.5B with rollout size N =64 and report Pass@1 performance.

                      AIME                                       MATH                                  AIME                                            MATH
        21                                         74.5                                     23                                            76.0
                                    20.0                                                                                 21.7             75.5
        20                                         74.0                                     22                                                                           74.9
        19                  18.3                                         73.6               21                    20.8                    75.0                    74.6
                                                   73.5                                             20.0                                  74.5
Score




                                           Score




                                                                                    Score




                                                                                                                                  Score




        18                                                        73.1                      20
                                                          73.0                                                                            74.0      73.6
        17                                         73.0                                     19 18.3                                       73.5 73.1        73.2
        16    15.8                                                                          18
                                                   72.5                                                    16.9                           73.0
        15                                                                                  17                                            72.5
        14                                         72.0                                     16                                            72.0
                                                                                                    Code (0.5B)                 Code (1.5B)           Code (7B)
                     TTRL          No Code (1.5B)         No Code (7B)                              No Code (1.5B)              No Code (7B)

                        (a) Ablating verification.                                            (b) Ablating tool execution and verifier size.
Figure 6: Ablation on verifier and verification tool. Left: Adding an LLM verifier improves TTRL
even without tool execution. Right: Code execution significantly strengthens verification.

                                                                                7
The Contribution of Test-Time Verification. We isolate the effect of test-time verification by com-
paring (i) vanilla TTRL against (ii) T3 RL without tool access, i.e., using LLM alone for verification.
In Figure 6a, improvements are seen on both AIME and MATH with 1.5B or 7B verifier on 1.5B
policy model. These results showcase that introducing verification on rollouts yields better online
updates with improved reward estimation, even before introducing tool-assisted verification.
The Contribution of Tool-Assisted Verification. We next control for the tool execution effect by
comparing verification T3 RL with and without tool execution. The results in Figure 6b show that the
verification tool contributes a clear additional lift beyond verifier-only checking, improving AIME
from 18.3 to 20.8 for the 1.5B verifier and from 20.0 to 21.7 for the 7B, confirming that executable
evidence reduces verifier uncertainty and yields a more reliable verification signal.
Self-Verifier vs. External Verifier. We further ablate the distillation                   Table 2: Self vs. Ext. verifier.
effect by comparing T3 RL with the policy model as self-verifier on                               Math Llama Qwen3
AIME. Note that, the external verifier Qwen-2.5-Coder-1.5B is an                                  1.5B 3B     4B
even weaker model (1.7 on AIME). Table 2 shows that self-verification                     TTRL 15.8        13.3     36.4
beats TTRL on all three backbones. So the gain stems from verification                    Self 16.7        16.9     39.8
                                                                                          Ext. 20.8        17.1     40.0
itself instead of distilling math knowledge from other model. Verification
leads to flip rates on 5.40% of AIME 2024, 10.75% of AMC, and 12.87%
of MATH-500.


The Contribution of Verification-Weighted Vot-
ing. We ablate the verification weight ω in T3 RL Table 3: Verifier quality on policy rollouts.
by sweeping its value, which controls the voting
power of rollouts that pass the tool-verifier check. A Policy          Verifier      Acc. Prec. Rec. ∆ AIME

weight of ω=1 degenerates to majority-vote TTRL, Math-1.5B             Coder-1.5B 73.2
                                                       Llama-3.2-3B Coder-1.5B 73.3
                                                                                             25.0
                                                                                             39.4
                                                                                                     51.5
                                                                                                     59.1
                                                                                                             +5.0
                                                                                                             +3.8
and ω→∞ approximates binary hard filtering of Qwen-3-4B                Coder-1.5B 75.0       38.2    40.7    +3.6
unverified rollouts. As shown in Figure 7, finite             Qwen-2.5-1.5B     Llama-3.2-1B       Qwen-2.5-Math-1.5B
weights ω > 1 improve AIME accuracy across
                                                         30                          +31.6%
all three backbones. The largest gain occurs for
                                                         10
                                                               Accuracy Gain (%)




Qwen-2.5-Math-1.5B at ω=5 (AIME +31.6%,
MATH-500 +2.2%), with similar performance at               3
ω=10; hard filtering is less reliable. This behavior       1
arises because the verifier is itself noisy due to the                            +2.2%
stochastic nature of LLMs in rollout-to-code transla-      0
tion, although tool execution provides a deterministic
check: Table 3 shows that the verifier accuracy with                AIME
Coder-1.5B reaches only 73.2%, so hard filtering                    MATH
                                                          -3
can propagate false positives and discard true posi-          1            2         5            10
tives, while ω=1 ignores the verifier entirely. There-                  Verified Voting Weight
fore, tool-assisted verification should act as a soft   Figure 7: The effect of the vote weight ω.
preference signal.
Sensitivity of the verification weight: Every ω>1 improves over TTRL generally, and moderate
values plateau (ω=2 is within 0.4 points of ω=5); only hard filtering degrades.



6     Discussions and Analysis

6.1    Q1: Why Does T3 RL Work?


    T3 RL functions as a verified self-distillation loop that generates synthetic training data online.
Tool-use of reasoning models is learned from execution feedback and improved through interaction
with the environment [Silver and Sutton, 2025]. In the test-time training loop, there’s an open design
choice: tools as policy actions or tools as verification evidence. The impressive contribution of tool
verification in T3 RL raises the question of whether tool access alone suffices, or whether the position
in the loop also matters.


                                                         8
                                                                                                                    16%         TTRL
                             T3RL                         T3RL                                                                  TTRL Std. Dev.
                                                                                                                                T3RL




                                                                                                    AIME Accuracy
                                                                                                                    14%
                                                                                                                                T3RL Std. Dev.
                                                                                                                    12%
                                                                                                                    10%
                                                                                                                    8%

                                                                                                                            0 20 40 60 80 100 120 140
                                                                                                                                         Steps
(a) Tool in policy vs. in verification.                 (b) Training robustness.                      (c) Training dynamics comparison.
Figure 8: Ablations on tool position and training robustness. Left: allowing the policy to call tools
during rollouts (TTRL-AGENT) can hurt performance, while T3 RL improves by restricting tool
use to the verifier for reward shaping. Right: verifier-shaped rewards reduce run-to-run variability,
indicating more stable optimization under unlabeled test-time RL.
Setting. To further examine why T3 RL works, we compare (i) TTRL; (ii) TTRL-AGENT, which
extends TTRL and grants the trained policy access to tool calling directly with majority voting over
execution results, and (iii) T3 RL, which trains a non-agentic policy with a tool-assisted verifier.
Observation & analysis. Figure 8a shows TTRL-AGENT degrades, while T3 RL yields growing
positive gains with benchmark difficulty. We attribute TTRL-AGENT’s failure to error-signal mixture:
tool calls inside rollouts conflate reasoning errors with tool-usage errors (e.g., malformed code
generation or brittle execution artifacts), and self-consensus rewards amplify this noise. In contrast,
T3 RL decouples reasoning from tool execution: the verifier provides evidence after generation and
converts it into a verification-informed reward, turning rollouts into verified labeled training data on
the fly: an implicit verified online data synthesiser that stabilizes test-time learning.
T3 RL is more robust under tool-assisted verification voting. Tool verification further stabilizes
training, as shown in Figure 8c. Across multiple runs, TTRL exhibits noticeable run-to-run variability,
consistent with the sensitivity of self-induced rewards to sampling noise and pseudo-label estimation.
In contrast, T3 RL anchors reward construction with tool verification, yielding substantially lower
dispersion in peak performance in Figure 8b: both the standard deviation and variance of the best
accuracy after 100 steps. Overall, T3 RL produces more consistent learning dynamics and more
reliable accuracy on AIME.

Table 4: Training computation. AIME runs;                            Table 5: Inference computation. Per-query
arrows are relative to TTRL@64. T3 RL                                costs; arrows are relative to T3 RL.
achieves higher accuracy with less than half of                          Method                          Inf. Tokens ↓          AIME        AMC        MATH

the training cost, time and computations.                                Base
                                                                         TTRL
                                                                                                                    1,630
                                                                                                                    1,630
                                                                                                                              7.7 (↓63%) 28.6 (↓44%) 32.7 (↓56%)
                                                                                                                              15.8 (↓24%) 48.9 (↓4%) 73.0 (↓2%)
                                                                         T3 RL (ours)                               1,630         20.8       50.9        74.6
Method (rollout)    AIME ↑      Tokens ↓   Time (s) ↓    TFLOPs ↓
                                                                         Test-time majority (N =16)      61K (↑37×)   19.2 (↓8%) 49.4 (↓3%)          65.0 (↓13%)
TTRL@64                15.8       365K         324        7.9K           Tool-verified majority (N =16) 96K (↑59×) 20.8 (→0%) 51.5 (↑1%)             65.5 (↓12%)
                                                                         T1 (N =16, V =4)               200K (↑123×) 20.0 (↓4%) 52.1 (↑2%)           66.3 (↓11%)
T3 RL@16           20.0 (↑27%) 147K (↓60%) 126 (↓61%) 3.0K (↓63%)
                                                                         T1 + PRM (N =16, V =4)         200K (↑123×) 20.4 (↓2%) 52.7 (↑4%)            67.9 (↓9%)
T3 RL@32           20.8 (↑32%) 293K (↓20%) 218 (↓33%) 5.9K (↓25%)        Buffer-of-Thoughts              2,120 (↑30%) 9.6 (↓54%) 34.9 (↓31%)         38.6 (↓48%)
T3 RL@64           20.8 (↑32%) 586K (↑61%) 406 (↑26%) 11.8K (↑50%)       BoN-RR (N =64)                 243K (↑148×) 21.0 (↑1%) 51.8 (↑2%)           51.7 (↓31%)


Allocating test-time computation wisely: verification beats brute-force scaling. How should the
test-time budget be split between (i) sampling more rollouts for self-consensus and (ii) verifying
rollouts to make each sample more informative? We find two things. First, T3 RL is cheaper during
training (60% less) to achieve better accuracy than TTRL. Holding all else fixed and accounting
for both policy and verifier costs, T3 RL@r=16 already surpasses TTRL@64 using 59.8% fewer
tokens, 61.3% less wall-clock time, and 62.5% fewer TFLOPs (Table 4); sandbox execution adds only
∼49 ms per snippet (< 1% of training). Second, T3 RL is cheaper during inference (123–200× less)
than verifier-based TTS to achieve matched accuracy. Comparing with non-parametric alternatives
(Table 5): Buffer-of-Thoughts [Yang et al., 2024], a memory-based system that reuses successful
rollouts, cannot match even TTRL, while the verifier-guided test-time scaling approach, best-of-N
reranking (BoN-RR), approaches T3 RL’s accuracy only by inflating per-query inference tokens by
148× and paying O(2N ) at every test instance. Other verifier-aware TTS baselines are no cheaper:
T1 [Kang et al., 2026] reaches 66.3 and T1+PRM [Wang et al., 2024] reaches 67.9 on MATH-500,
both at 200K tokens per query. T3 RL instead amortises the verifier’s signal into the policy weights
once at training and infers at O(1), converting test-time compute into efficient parameter updates and
avoiding re-paying the inference cost on every query.


                                                                     9
6.2    Q2: Can T3 RL generalize?

Generalization beyond math: logical reasoning To test whether T3 RL depends on mathematical
reasoning or Python execution, we evaluate it on held-out two-character Knights-and-Knaves puzzles,
where knights always tell the truth and knaves always lie. The verifier represents knights as true
and knaves as false, translates policy solutions to the problem into Satisfiability Modulo Theories
(SMT) [Barrett and Tinelli, 2018] constraints using SMT-LIB2, and checks them with Z3 solver
execution [Xie et al., 2024, de Moura and Bjørner, 2008].

Table 6: Non-math generalization on Knights-and-Knaves puzzles with an SMT-LIB2/Z3 example.
      Method        Base model       Accuracy     ∆ vs. base              Query                  Verifier           Z3 result
                                                                                                                      ✓ sat
                                                                      A says: “B is a                               A=false
      Base      Qwen-2.5-VL-1.5B    52.13 ± 1.3     –                      knave.”
                                                                                           SMT-LIB2 constraints
      TTRL      Qwen-2.5-VL-1.5B    48.58 ± 1.3   −3.55                                   (assert (= A (not B)))     (knave)
                                                                      B says: “A and I   (assert (= B (xor A B)))    B=true
      T3 RL     Qwen-2.5-VL-1.5B    78.50 ± 1.1   +26.38               are different.”
                                                                                                                    (knight)

T3 RL improves accuracy with a gain of 26.38 points over the base model (Table 6) while TTRL
decreases. This result supports the narrower claim that T3 RL can generalize when an external tool
provides a reliable correctness check, for example, on logical reasoning intensive tasks such as SMT
solving, theorem proving, and program verification.
Generalization across-dataset. Each row adapts the policy at test time on one source benchmark
and evaluates it on all three targets, so off-diagonal entries measure transfer to unseen benchmarks.
T3 RL improves all nine train–test pairs (mean +3.0 points; Table 7). Mean run-to-run SD decreases
by 8.4% (2.38 → 2.18).

      Table 7: Cross-dataset adaptation (A/C/M: AIME/AMC/MATH-500). Inset: accuracy gain.
               Adaptation setting          AIME 2024           AMC       MATH-500             Accuracy gain (pp)
                                                                                                  A     C      M
               TTRL adapted on AIME        15.8 ± 2.1    42.9 ± 2.4     65.5 ± 2.4
                                                                                             A +5.0 +2.5 +2.5
               T3 RL adapted on AIME       20.8 ± 1.6    45.4 ± 2.5     68.0 ± 2.0
               TTRL adapted on AMC         11.5 ± 1.6    48.9 ± 1.6     66.6 ± 1.4           C +3.6 +2.0 +3.8
               T3 RL adapted on AMC        15.1 ± 2.0    50.9 ± 2.7     70.4 ± 1.7          M +3.9 +2.5 +1.6
               TTRL adapted on MATH-500    10.8 ± 3.4    43.2 ± 2.7     73.0 ± 3.8
               T3 RL adapted on MATH-500   14.7 ± 1.9    45.7 ± 2.0     74.6 ± 3.2                 T3 RL better


6.3    Q3: What boosts T3 RL, and when might it fail?

Boosting performance: stronger verifiers and larger rollout budgets help. Scaling the verifier
from 0.5B to 7B on Qwen-Math-2.5 consistently improves T3 RL across benchmarks (AIME 20.8 →
21.7, AMC 50.9 → 51.5, MATH-500 74.4 → 74.9; Table 3): stronger verifiers produce more reliable
rollout-to-code translation and verification-aware reward signals. Increasing the rollout budget
N ∈ {16, 32, 64} also improves T3 RL monotonically (Table 4), as a larger candidate set raises
solution diversity and concentrates vote mass on a more reliable pseudo-label. Figure 3b shows the
resulting effect: T3 RL flips the majority label via tool verification when an incorrect calculation
dominates.
Limitations: noisy verifiers and easy tasks limit gains. T3 RL requires V to provide a meaningful
correctness signal. When V is underpowered (e.g., Qwen-0.5B with bare-minimum coding ability),
noisy tool calls cause verification-aware voting to misweight rollouts and add a second stochastic
layer on top of self-consensus, so the pseudo-label ye∗ becomes less stable than vanilla majority
voting. Experimental results and failure-case studies are provided in Appendix C. On easy tasks
where rollouts are already accurate and consistent, verification aligns with the consensus without
changing the pseudo-label distribution, so gains over TTRL are small.

7     Conclusion
We propose T3 RL, introducing test-time verification to the test-time reinforcement learning frame-
work that learns from unlabeled test data by suppressing spurious rewards with tool verification.
Experiments across heterogeneous backbones and math benchmarks show consistent gains of tool
verification. Overall, T3 RL positions test-time RL as verified online data synthesis: sampled rollouts
become reliable training instances once verified with executable evidence, enabling more stable
verifiable test-time training. Future work will broaden to domain-specific tool verification.


                                                               10
Impact Statement
This paper aims to advance the field of machine learning. Our work introduces test-time verification as
a mechanism for stabilizing self-evolution in large reasoning models by reducing error reinforcement
and mitigating self-consistencydriven failure modes. If deployed responsibly, such verification can
improve reliability and robustness in high-stakes applications by encouraging models to seek and
check external evidence rather than relying solely on internal consistency. Potential risks include
over-reliance on imperfect verifiers and the possibility that verification pipelines inherit biases or
vulnerabilities from their underlying tools and data sources. To mitigate these risks, future work
should investigate improvements to verifiers and robustness to adversarial or noisy feedback. More
broadly, the proposed framework is modular and can incorporate improved test-time verification
methods as they become available.

References
Clark Barrett and Cesare Tinelli. Satisfiability modulo theories. In Handbook of Model Checking,
  pages 305–343. Springer International Publishing, Cham, 2018.
Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. Titans: Learning to memorize at test time, 2024.
  URL https://arxiv.org/abs/2501.00663.
Kaiyan Chang, Yonghao Shi, Chenglong Wang, Hang Zhou, Chi Hu, Xiaoqian Liu, Yingfeng Luo,
 Yuan Ge, Tong Xiao, and Jingbo Zhu. Step-level verifier-guided hybrid test-time scaling for large
  language models, 2025. URL https://arxiv.org/abs/2507.15512.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve
  math word problems. arXiv preprint arXiv:2110.14168, 2021.
Karan Dalal, Daniel Koceja, Jiarui Xu, Yue Zhao, Shihao Han, Ka Chun Cheung, Jan Kautz, Yejin
  Choi, Yu Sun, and Xiaolong Wang. One-minute video generation with test-time training. In
  Proceedings of the Computer Vision and Pattern Recognition Conference, pages 17702–17711,
  2025.
Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In Tools and Algorithms for the
  Construction and Analysis of Systems, pages 337–340, 2008.
Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Minlie Huang, Nan Duan, and
  Weizhu Chen. Tora: A tool-integrated reasoning agent for mathematical problem solving, 2024.
  URL https://arxiv.org/abs/2309.17452.
Aaron Grattafiori and el al. The llama 3 herd of models, 2024. URL https://arxiv.org/abs/
  2407.21783.
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
  Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
  via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
Moritz Hardt and Yu Sun. Test-time training on nearest neighbors for large language models. arXiv
 preprint arXiv:2305.18466, 2023.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv
  preprint arXiv:2103.03874, 2021.
Can Jin, Hongwu Peng, Qixin Zhang, Yujin Tang, Dimitris N Metaxas, and Tong Che. Two heads
  are better than one: Test-time scaling of multi-agent collaborative reasoning. arXiv preprint
  arXiv:2504.09772, 2025.
Minki Kang, Jongwon Jeong, and Jaewoong Cho. T1: Tool-integrated verification for test-time
 compute scaling in small language models. In C. Vondrick, B. Hariharan, C. Raffel, L. Pinto,
 D. Yang, and A. Faust, editors, International Conference on Learning Representations, vol-
 ume 2026, pages 73413–73444, 2026. URL https://proceedings.iclr.cc/paper_files/
 paper/2026/file/776a5f2c7d6dd4b0d83145fc044e2726-Paper-Conference.pdf.


                                                  11
Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif
   Rasul, Longhui Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in
   ai4maths with 860k pairs of competition math problems and solutions. Hugging Face repository,
   13(9):9, 2024.
Shalev Lifshitz, Sheila A. McIlraith, and Yilun Du. Multi-agent verification: Scaling test-time
  compute with multiple verifiers, 2025a. URL https://arxiv.org/abs/2502.20379.
Shalev Lifshitz, Sheila A McIlraith, and Yilun Du. Multi-agent verification: Scaling test-time
  compute with multiple verifiers (abridged). In Workshop on Reasoning and Planning for Large
  Language Models, 2025b.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan
  Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth
 International Conference on Learning Representations, 2023.
Zhan Ling, Yunhao Fang, Xuanlin Li, Zhiao Huang, Mingu Lee, Roland Memisevic, and Hao Su.
  Deductive verification of chain-of-thought reasoning. Advances in Neural Information Processing
  Systems, 36:36407–36433, 2023.
Yuejiang Liu, Parth Kothari, Bastien Van Delft, Baptiste Bellot-Gurlet, Taylor Mordan, and Alexandre
  Alahi. Ttt++: When does self-supervised test-time training fail or thrive? Advances in Neural
  Information Processing Systems, 34:21808–21820, 2021.
Dheeraj Mekala, Jason E Weston, Jack Lanchantin, Roberta Raileanu, Maria Lomeli, Jingbo Shang,
  and Jane Dwivedi-Yu. Toolverifier: Generalization to new tools via self-verification. In Findings
  of the Association for Computational Linguistics: EMNLP 2024, pages 5026–5041, 2024.
Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke
  Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori B Hashimoto. s1: Simple test-time
  scaling. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language
  Processing, pages 20286–20332, 2025.
Hadas Orgad, Michael Toker, Zorik Gekhman, Roi Reichart, Idan Szpektor, Hadas Kotek, and Yonatan
  Belinkov. Llms know more than they show: On the intrinsic representation of llm hallucinations,
  2025. URL https://arxiv.org/abs/2410.02707.
Archiki Prasad, Weizhe Yuan, Richard Yuanzhe Pang, Jing Xu, Maryam Fazel-Zarandi, Mohit Bansal,
  Sainbayar Sukhbaatar, Jason Weston, and Jane Yu. Self-consistency preference optimization. arXiv
  preprint arXiv:2411.04109, 2024.
Qwen and el al. Qwen2.5: A party of foundation models, September 2024. URL https://qwenlm.
 github.io/blog/qwen2.5/.
Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du,
  Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei
  Koh, and Luke Zettlemoyer. Spurious rewards: Rethinking training signals in rlvr, 2025. URL
  https://arxiv.org/abs/2506.10947.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathemat-
  ical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.
David Silver and Richard S Sutton. Welcome to the era of experience. Google AI, 1, 2025.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally
  can be more effective than scaling model parameters. arXiv preprint arXiv:2408.03314, 2024a.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally
  can be more effective than scaling model parameters, 2024b. URL https://arxiv.org/abs/
  2408.03314.
Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei Efros, and Moritz Hardt. Test-time training
  with self-supervision for generalization under distribution shifts. In International conference on
  machine learning, pages 9229–9248. PMLR, 2020.


                                                12
Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei
  Chen, Xiaolong Wang, Oluwasanmi Koyejo, Tatsunori Hashimoto, and Carlos Guestrin. Learning
  to (learn at test time): Rnns with expressive hidden states. ArXiv, abs/2407.04620, 2024a. URL
  https://api.semanticscholar.org/CorpusID:271039606.
Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei
  Chen, Xiaolong Wang, Sanmi Koyejo, et al. Learning to (learn at test time): Rnns with expressive
  hidden states. arXiv preprint arXiv:2407.04620, 2024b.
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia
  Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process-and
  outcome-based feedback. arXiv preprint arXiv:2211.14275, 2022.
V Venktesh, Mandeep Rathee, and Avishek Anand. Trust but verify! a survey on verification design
  for test-time scaling. arXiv preprint arXiv:2508.16665, 2025.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang
  Sui. Math-shepherd: Verify and reinforce LLMs step-by-step without human annotations. In
  Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting
  of the Association for Computational Linguistics (Volume 1: Long Papers), pages 9426–9439,
  Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/
  2024.acl-long.510. URL https://aclanthology.org/2024.acl-long.510/.
Renhao Wang, Yu Sun, Arnuv Tandon, Yossi Gandelsman, Xinlei Chen, Alexei A Efros, and Xiaolong
  Wang. Test-time training on video streams. Journal of Machine Learning Research, 26(9):1–29,
  2025a.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdh-
  ery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models,
  2023. URL https://arxiv.org/abs/2203.11171.
Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu, Baolin Peng, Hao Cheng, Xuehai
  He, Kuan Wang, Jianfeng Gao, et al. Reinforcement learning for reasoning in large language
  models with one training example. arXiv preprint arXiv:2504.20571, 2025b.
Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling laws:
  An empirical analysis of compute-optimal inference for llm problem-solving. In The Thirteenth
  International Conference on Learning Representations, 2025.
Jian Xie et al. On memorization of large language models in logical reasoning. In Advances in Neural
   Information Processing Systems, 2024.
An Yang et al. Qwen3 technical report, 2025.
Ling Yang, Zhaochen Yu, Tianjun Zhang, Shiyi Cao, Minkai Xu, Wentao Zhang, Joseph E Gonzalez,
  and Bin Cui. Buffer of thoughts: Thought-augmented reasoning with large language models.
  Advances in Neural Information Processing Systems, 37:113519–113544, 2024.
Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan
 Kautz, Yejin Choi, James Zou, Carlos Guestrin, and Yu Sun. Learning to discover at test time,
 2026. URL https://arxiv.org/abs/2601.16175.
Weihao Zeng, Yuzhen Huang, Qian Liu, Wei Liu, Keqing He, Zejun Ma, and Junxian He. Simplerl-
 zoo: Investigating and taming zero reinforcement learning for open base models in the wild. arXiv
 preprint arXiv:2503.18892, 2025.
Kongcheng Zhang, Qi Yao, Shunyu Liu, Yingjie Wang, Baisheng Lai, Jieping Ye, Mingli Song,
  and Dacheng Tao. Consistent paths lead to truth: Self-rewarding reinforcement learning for llm
  reasoning, 2025. URL https://arxiv.org/abs/2506.08745.
Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal.
  Generative verifiers: Reward modeling as next-token prediction. arXiv preprint arXiv:2408.15240,
  2024.


                                                13
     Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu Cui, Xuekai Zhu, Haozhan Li, Yuchen
       Zhang, Xinwei Long, Ermo Hua, et al. Ttrl: Test-time reinforcement learning. arXiv preprint
       arXiv:2504.16084, 2025.


     A    Implementation details: Pseudo-Code

                                        Listing 1: Pseudo-code for T3 RL
 1   from collections import defaultdict
 2
 3   def t3rl_reward_fn (x , policy , verifier , sandbox , N , omega ) :
 4       Y = policy . sample_rollouts (x , n = N )
 5       vote , A = defaultdict ( float ) , []
 6
 7         for y in Y :
 8             a_hat = extract_answer ( y )
 9             # (1) verifier generates code
10             code = verifier . generate (x , y )
11             # (2) sandbox executes the code and returns evidence
12             t = sandbox . execute ( code )
13             # (3) verifier returns only a validity flag
14             v = verifier . judge (x , y , a_hat , t )     # v in {0 ,1}
15             vote [ a_hat ] += (1.0 if v == 0 else omega )
16             A . append ( a_hat )
17
18         y_star = max ( vote , key = vote . get ) # weighted majority pseudo -
               label
19         rewards = [1.0 if a_hat == y_star else 0.0 for a_hat in A ]
20         return y_star , rewards



     B    Verifier System Prompt
     The system prompt used to guide the external LLM verifier is shown in Figure 9. We carefully
     designed the instructions to ensure reliable, independent, and easily parsable tool-assisted verification.
     The key design choices in our prompt include:

            • Role Assignment: Instructing the model to act as an “expert mathematician and Python
              programmer” sets a strong prior for generating rigorous, high-quality script formulations.
            • Independent Recomputation: By explicitly stating “DO NOT assume the reasoning trace
              is correct” and “Prefer recomputing the answer directly,” we mitigate confirmation bias.
              This prevents the verifier from blindly translating a flawed reasoning trace into code, forcing
              it to independently verify the underlying logic based on the original problem statement.
            • Trace as a Hint: Allowing the verifier to use the candidate trace as a “hint” helps it navigate
              complex problems. It can leverage the policy model’s mathematical intuition without being
              strictly bound to its (potentially flawed) arithmetic execution.




                                                        14
                     You are an expert mathematician and Python programmer.

                     You will be given:
                     - a math problem statement
                     - a candidate reasoning trace that claims to solve it

                     Your task is to VERIFY the candidate answer against the problem by
                     writing Python code.

                     Rules:
                     - DO NOT assume the reasoning trace is correct.
                     - Prefer recomputing the answer directly from the PROBLEM STATEMENT.
                     - You may use the reasoning trace as a hint for what method to try.

                     Code Requirements:
                     - Use a SINGLE Python block formatted exactly as: ```python CODE ```
                     - Allowed modules: math, sympy, numpy, fractions
                     - Your code MUST print ONLY your final, computed result, e.g.
                     print(result). Do not print hardcoded values.



                                Figure 9: System Prompt for the Verifier.


C    Failure Case: Small Verifiers
As quantitative results in Table 8 demonstrate, deploying an undersized verifier like
Qwen-Coder-0.5B actively degrades performance compared to the standard TTRL baseline. This
performance drop stems from the small model’s limited capacity to strictly adhere to the verification
instructions, which injects noise rather than reliable evidence into the reward signal. Qualitative
analysis of the generated verification scripts reveals two primary failure modes:

       • Blind Copying and Hardcoded Outputs: Despite explicit instructions in the system prompt
         to "DO NOT assume the reasoning trace is correct" and to strictly outputting hardcoded
         values, the 0.5B verifier frequently exhibits severe instruction-following failures. Instead
         of formulating an independent computational check, the model often defers entirely to the
         provided candidate trace. It typically hallucinates pseudo-reasoning within Python comments
         and bypasses actual computation, yielding a script that merely executes a hardcoded print
         statement of the trace’s final answer (see Figure 10a). This confirmation bias neutralizes the
         benefits of executable verification, creating a false-positive signal that simply reinforces the
         unverified consensus.
       • Formatting and Compilation Errors: A secondary, yet pervasive, issue is the small
         model’s inability to consistently follow structural guidelines. The 0.5B verifier struggles
         to maintain valid Python syntax and adhere to the strict code-block formatting constraints
         required for automated extraction. This manifests as an increased frequency of compilation
         and execution errors, driven by missing import statements, malformed block delimiters, syn-
         tactical hallucinations, or endless comments (see Figure 10b). Consequently, the verification
         tool returns execution failures rather than reliable validity checks, further destabilizing the
         reward estimation process.

Combined, these limitations demonstrate that T3 RL requires a minimum threshold of verifier capacity
to function effectively; below this threshold, the verifier acts as an additional source of stochastic
noise rather than a reliable grounding mechanism.

                Model / Method                       AIME 2024        AMC     MATH-500      Avg
                Qwen-2.5-0.5B Vanilla (Baseline)          0.0           4.8      7.9       4.2
                 w/ TTRL                                  0.4         12.0      34.6      15.7
                 w/ T3 RL (0.5B verifier)                 0.0         10.8      32.0      14.3
                 ∆ (T3 RL − TTRL)                        -0.4          -1.2     -2.6      -1.4
                 Rel. (% over TTRL)                    ↓100.0%       ↓10.0%    ↓7.5%     ↓8.9%

      Table 8: Performance comparison illustrating failure cases with a weak (0.5B) verifier.



                                                          15
      # Given the problem statement and reasoning trace,           # Given values
      we   need   to    determine   how   many   initial           a_3D = 6
      configurations will lead to a transformed grid               angle_A = 120
      consisting of a single filled square in the center           side_lengths = [a_minus_3d, a_minus_3d, a_3D]
      after a single transformation.
                                                                   # Calculate the area using the Law of Cosines
      # The transformation rule states that a single               # a^2 + b^2 = c^2
      fill in the center of the grid means all the                 # c = a + b
      square in this center remains filled, and none of            # a^2 + b^2 = 36
      the surrounding empty squares become filled.                 # a^2 + b^2 = 36
      # The only square that remains filled in this                # a^2 + b^2 = 6^2
      center could be the center, but since it must form           # a^2 + b^2 = 36
      the border of another empty square, the center               # a^2 + b^2 = 6^2
      must be surrounded by exactly three filled                   # a^2 + b^2 = 36
      neighbors.                                                   # a^2 + b^2 = 6^2
                                                                   # a^2 + b^2 = 36
      # The number of initial configurations that will             # a^2 + b^2 = 6^2
      lead to a transformed grid consisting of a single            # a^2 + b^2 = 36
      filled square in the center after a single                   # a^2 + b^2 = 6^2
      transformation is 1.                                         # a^2 + b^2 = 6^2

      print(1)                                                     ...



   (a) Blind copying and hardcoded outputs. The                 (b) Formatting and compilation errors. The model
   model hallucinates reasoning in code comments                fails to generate executable Python syntax and pro-
   and simply prints the unverified final answer given          duces endless comments, resulting in compilation
   in the reasoning trace.                                      errors.

Figure 10: Qualitative examples of the two primary failure modes encountered when deploying an
undersized verifier.




                                                           16
