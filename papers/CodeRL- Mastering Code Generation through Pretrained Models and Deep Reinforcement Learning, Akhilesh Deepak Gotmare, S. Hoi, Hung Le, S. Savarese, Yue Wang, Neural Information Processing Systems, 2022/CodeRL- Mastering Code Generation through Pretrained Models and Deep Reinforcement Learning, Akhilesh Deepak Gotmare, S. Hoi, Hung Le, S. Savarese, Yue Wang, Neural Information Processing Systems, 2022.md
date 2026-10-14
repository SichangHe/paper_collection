                                           CodeRL: Mastering Code Generation through
                                        Pretrained Models and Deep Reinforcement Learning


                                               Hung Le∗, Yue Wang∗, Akhilesh Deepak Gotmare, Silvio Savarese, Steven C.H. Hoi †
                                                                             Salesforce Research
                                                              https://github.com/salesforce/CodeRL
arXiv:2207.01780v3 [cs.LG] 3 Nov 2022




                                                                                      Abstract
                                                 Program synthesis or code generation aims to generate a program that satisfies a
                                                 problem specification. Recent approaches using large-scale pretrained language
                                                 models (LMs) have shown promising results, yet they have some critical limitations.
                                                 In particular, they often follow a standard supervised fine-tuning procedure to train a
                                                 code generation model only from the pairs of natural-language problem descriptions
                                                 and ground-truth programs. Such paradigm largely ignores some important but
                                                 potentially useful signals in the problem specification such as unit tests, which
                                                 thus often results in poor performance when solving complex unseen coding tasks.
                                                 To address the limitations, we propose “CodeRL”, a new framework for program
                                                 synthesis tasks through pretrained LMs and deep reinforcement learning (RL).
                                                 Specifically, during training, we treat the code-generating LM as an actor network,
                                                 and introduce a critic network that is trained to predict the functional correctness
                                                 of generated programs and provide dense feedback signals to the actor. During
                                                 inference, we introduce a new generation procedure with a critical sampling strategy
                                                 that allows a model to automatically regenerate programs based on feedback from
                                                 example unit tests and critic scores. For the model backbones, we extended the
                                                 encoder-decoder architecture of CodeT5 with enhanced learning objectives, larger
                                                 model sizes, and better pretraining data. Our method not only achieves new SOTA
                                                 results on the challenging APPS benchmark, but also shows strong zero-shot
                                                 transfer capability with new SOTA results on the simpler MBPP benchmark.


                                                     Problem Specification                                              Problem Specification
                                                                                                A string is a palindrome if it reads the same from the left to the right
                                                                                                and from the right to the left….If there is such a substring in $s$ that
                                                              Policy                            is not a palindrome, print the maximum length of such a substring….
                                                      Pretrained LM (actor)                     Example Input and Output:            Input: ‘hannah’      Output: 5

                                                       Values                          Action                             Solution Program

                                                         Value Function
                                                             Critic
                                         State        Reward
                                                          Environment
                                                           Compiler
                                                                                                                               Unit Tests
                                                                                                      Input: wuffuw                              Output: 5
                                                           Unit Tests          I/O                    Input: iiiiiii                             Output: 0…


                                        Figure 1: An example program synthesis task (Right): Each task is defined by a problem specifi-
                                        cation in natural language, often containing example input and output pairs. The expected output is a
                                        program to be checked for functional correctness against some unit tests. A high-level overview of
                                        our CodeRL framework for program synthesis (Left): we treat a pretrained code language model
                                        (LM) as a stochastic policy, code generations as actions, and rewards can be estimated based on the
                                        unit test results of output programs from the compiler (environment).
                                                                                                   Returns

                                                                                     Actor-Critic RL Finetuning with
                                           ∗
                                             Equal contribution.
                                           †
                                             Corresponding authors: {hungle, shoi}@salesforce.com
Contents

1   Introduction                                                                                      3

2   Related Work                                                                                      4
    2.1   Program Synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       4
    2.2   Reinforcement Learning for Sequence Generation . . . . . . . . . . . . . . . . . .          4
    2.3   Program Completion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        5

3   CodeRL                                                                                           5
    3.1   Program Synthesis Task . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      5
    3.2   Pretraining Language Models on Code . . . . . . . . . . . . . . . . . . . . . . . .         6
    3.3   Program Synthesis as an RL Problem . . . . . . . . . . . . . . . . . . . . . . . .          6
          3.3.1    Defining Return by Unit Test Signals . . . . . . . . . . . . . . . . . . . .       7
          3.3.2    Return with a Baseline . . . . . . . . . . . . . . . . . . . . . . . . . . . .     7
          3.3.3    Intermediate Return by Critic as Error Predictor . . . . . . . . . . . . . . .     8
          3.3.4    Generating Programs with Example Unit Tests and Critic . . . . . . . . . .         8
    3.4   Implementation Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     10

4   Experiments                                                                                      10
    4.1   Experimental Setups . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      10
    4.2   Program Synthesis Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . .         11
    4.3   Experimental Results on APPS . . . . . . . . . . . . . . . . . . . . . . . . . . . .       11
    4.4   Ablation Studies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   12
    4.5   Experimental Results on MBPP . . . . . . . . . . . . . . . . . . . . . . . . . . .         16
    4.6   Qualitative Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   17

5   Limitations and Broader Impacts                                                                  19

6   Conclusion                                                                                       19

A Critic Sampling Procedure                                                                          24

B Additional Experimental Results                                                                    24
    B.1 CodeXGLUE Benchmark Results . . . . . . . . . . . . . . . . . . . . . . . . . .              24
    B.2 MBPP Benchmark Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           26

C Additional Qualitative Analysis                                                                    27
    C.1 Failure Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     27
    C.2 Example Generated Programs . . . . . . . . . . . . . . . . . . . . . . . . . . . .           27




                                                   2
1   Introduction


Program synthesis or code generation is the task of designing and building an executable computer
program that satisfies a problem specification (see Figure 1, right, for an example). Program synthesis
research has gained much attention due to its significant impacts on the software industry, including
better productivity and accessibility of programming jobs and education. Developing an AI model
that can automatically generate programs based on human requirements can dramatically transform
programming tools and the way we work with them.
Recent attempts employ deep learning methods, specifically Transformer-based pretrained language
models (LMs) [Vaswani et al., 2017, Brown et al., 2020], which were originally intended for natural
language learning tasks, to generate unique computer programs. These approaches [Hendrycks et al.,
2021, Chen et al., 2021a, Austin et al., 2021] consider program synthesis as a sequence-to-sequence
task, which receives input sequence as problem specification in natural language and generates a
sequence of codes as the output program. While these models achieve promising results, especially
in basic programming tasks [Chen et al., 2021a, Austin et al., 2021], we observe that they still fail to
generate codes to solve complex problems such as those at programming competitions [Hendrycks
et al., 2021, Li et al., 2022].
There are two main limitations. First, current models are trained using a conventional next-token
prediction (NTP) objective which maximizes the next ground-truth token likelihood. As noted in NLP
domains [Bengio et al., 2015, Ranzato et al., 2016], training models only with next-token prediction
objective in a "teacher-forcing" manner often leads to accumulating errors during test time when
tokens are generated by conditioning on previously sampled tokens, not the ground-truth tokens. This
issue becomes more serious in the domain of program synthesis, where token-matching scores such
as BLEU [Papineni et al., 2002, Ren et al., 2020] are more appropriate in partial program synthesis
tasks (i.e. code completion) [Husain et al., 2019] but have failed to measure the functional correctness
of complete programs [Hendrycks et al., 2021, Chen et al., 2021a]. Training only with NTP objective
is hence, not ideal to tackle full program generation to solve programming problems.
Secondly, current models fail to utilize the potential meaningful signals from unit tests, which directly
determine the model performance by the functional correctness of programs. Current approaches
neglect this important signal during model optimization as well as generation procedure. During
optimization, unit tests could be factored into learning objectives to match the final goal of generating
semantically correct programs. During inference, since unit tests are often parts of problem description
(i.e. example unit tests), they are potentially powerful to further improve output programs. Related
approaches such as [Li et al., 2022] use example unit tests to filter and rank final output programs.
While this method naturally selects better program candidates, it does not allow models to improve
the programs based on the initial (example) unit test results.
To address the above issues, we introduce “CodeRL”, a new framework to improve pretrained LMs
for program synthesis tasks through deep reinforcement learning (see Figure 1, left, and Section
3 for more details). Specifically, we propose a training strategy that optimizes pretrained LMs for
program synthesis tasks in an actor-critic RL approach [Konda and Tsitsiklis, 1999, Sutton et al.,
1999]. We treat the pretrained LM as an actor network and synthetically sample sequences from this
actor, including both correct and incorrect programs. These program samples are passed to a critic
model which is trained as an error predictor to assess the functional correctness of these samples. We
use the token-level hidden states extracted from the learned critic model to estimate the values/scores
of output tokens of these synthetic samples. The actor network is then finetuned on these synthetic
samples weighted by their critic scores.
During inference, as part of the CodeRL framework, we introduce a new generation procedure
that systematically exploits example unit test signals to allow models to further improve programs.
Firstly, for samples that pass the example unit tests, we employ the critic model to filter and select
sub-sequences. These sub-sequences are utilized as “seeds” that condition the model to resample
new tokens and obtain new output programs. Secondly, among failed programs, the critic selects top
programs based on their likelihood of passing unit tests. These program candidates are concatenated
with the error information received from a compiler and passed to a program repair module. This
generation procedure enables a dual strategy to automatically refine and repair output programs based
on their functional correctness during test time.


                                                   3
Together with CodeRL, we extend CodeT5 as a foundation model with improved pretraining strate-
gies, including better pretraining objectives, larger model sizes, and massive pretraining data. Our
comprehensive experiments (Section 4) show that our models can achieve SOTA performance on the
challenging APPS benchmark [Hendrycks et al., 2021]. Specifically, our models reach more than
2% pass@1, 6% pass@5, and 20% pass@1000. Since our RL method is model-agnostic, we also
apply it to various large-scale models and achieve consistent performance gains. We further test its
zero-shot transfer ability on a simpler MBPP benchmark [Austin et al., 2021], where it sets a new
SOTA result of 63.0% pass@80 over a finetuned GPT-137B’s 61.4%. We perform qualitative analysis
to understand the problems that the model succeeds or fails to solve. Finally, we release the improved
CodeT5-large (770M) model which outperforms many pretrained LMs of much larger sizes.

2         Related Work
2.1        Program Synthesis

Program synthesis tasks can date back as early as the early adoption of machine learning research
[Waldinger and Lee, 1969, Manna and Waldinger, 1971]. Earlier tasks include problem specifications
in the form of input-output (IO) examples [Summers, 1977, Gulwani et al., 2012] and synthesis
methods are limited to probabilistic approaches [Liang et al., 2010] or simple programming concepts
[Joulin and Mikolov, 2015, Kurach et al., 2015]. As deep learning methods became popular, later
approaches adopt neural models to induce output programs, assuming an inductive bias given a
sufficient number of program samples [Parisotto et al., 2016, Balog et al., 2016, Devlin et al., 2017].
More recently, we witnessed the emergence of program synthesis tasks in which output programs
are extended to general-purpose programming languages [Yin and Neubig, 2017, Xu et al., 2018,
Chen et al., 2021a] and program specifications are fully described in natural English text [Hendrycks
et al., 2021, Austin et al., 2021, Poesia et al., 2022]. These extensions have encouraged a rising
number of applications of pretrained language models (LMs) to program synthesis to exploit the
contextual representations learned from massive data of codes and natural languages [Feng et al.,
2020, Clement et al., 2020, Wang et al., 2021, Wang and Komatsuzaki, 2021, Chen et al., 2022].
Nijkamp et al. [2022] proposed a conversational program synthesis approach with large pretrained
language models. Despite impressive results in basic programming problems and initial commercial
deployment3 , existing models still perform poorly against complex problems such as those from
programming competitions on Codeforces [Hendrycks et al., 2021, Li et al., 2022].

Program Synthesis in Visual Context. Another related line of research is program synthesis in
computer vision domains such as images and videos. Early papers such as [Kulkarni et al., 2015,
Yang et al., 2015] introduce inverse graphics networks to infer visual properties such as pose, shape,
and lighting, of visual objects. Wu et al. [2017], Liu et al. [2019], Ellis et al. [2018] study the problem
of image rendering, which transforms an image to structured and compact representations, i.e. scene
programs. Tian et al. [2019] extends the prior work to render 3D shapes from images through
shape programs, containing features to capture geometric and structural priors. Ganin et al. [2018]
introduces an RL-based approach to render realistic images through high-level graphics programs.
Sun et al. [2018]introduces program synthesis from demonstration synthetic videos to summarize the
behaviors of the objects in the videos.
While this line of research has remarkable impacts on applications such as image/video editing,
captioning, and extrapolating, these approaches are limited to programs of domain-specific languages
defined for visual objects. For instance, in [Sun et al., 2018], programming language contains
basic functions for object perception, action, and control flows. In our work, we focus on program
synthesis from natural language problem specifications and the output programs are in general-
purpose languages such as Python. This type of programming task can range from basic programming
problems to competition-level programming tasks that require a high level of problem-solving skills.

2.2        Reinforcement Learning for Sequence Generation

Related to the program synthesis tasks are research domains of sequence generation, in which RL
approaches have demonstrated remarkable achievements. In these domains, RL approaches are used
      3
          https://copilot.github.com/


                                                    4
to exploit signals from non-differentiable metrics of the task at hand. Earlier work such as [Ranzato
et al., 2016] adopts this strategy with REINFORCE algorithm [Williams, 1992] to directly optimize
models for sequence-based test metrics such as BLEU [Papineni et al., 2002] and ROUGE [Lin,
2004] scores for translation models. In the same domain, Bahdanau et al. [2016] introduced an
actor-critic framework [Sutton, 1984, Konda and Tsitsiklis, 1999]. In visual captioning domains,
Rennie et al. [2017], Wang et al. [2018] proposed to use RL to optimize image captioning models
using variants of CIDEr scores [Vedantam et al., 2015]. Alternatively, Ren et al. [2017] derived a
new goal-oriented return estimate using visual-semantic embedding. Johnson et al. [2017], Trivedi
et al. [2021] introduce program generation as an auxiliary task to learn interpretable policies in
question-answering and synthetic navigation tasks.
Different from prior domains, in program synthesis, Austin et al. [2021], Chen et al. [2021a], Li et al.
[2022] demonstrated very low correlation between token-based similarity metrics and functional
correctness of programs. Hence, it is not trivial to define an appropriate optimization goal in this
domain. We propose to exploit unit test signals, which directly exhibit functional correctness of
programs, during both - model optimization and test-time generation stages. More related to our work
are RL-based program synthesis [Guu et al., 2017, Bunel et al., 2018, Liang et al., 2018, Zhong et al.,
2018] and execution-guided synthesis approaches [Ellis et al., 2019, Chen et al., 2021b]. However,
these are limited to programming languages defined within a specific application domain only.

2.3        Program Completion

Related to our work is the research of automatic program completion or code completion. Code
completion aims to generate programs conditioned on partial codes (e.g. function signatures, code
with blank gaps) and the output programs are often short snippets as potential code suggestions.
Early work such as [Robbes and Lanza, 2008, Bruch et al., 2009] shows that sufficient program
samples and prior program history can facilitate better code completion systems in terms of the
relevance of code suggestions. Raychev et al. [2014], White et al. [2015] introduce deep learning-
based approaches by considering the tasks as an NLP problem of predicting probabilities of tokens
or sentences using neural language models. Svyatkovskiy et al. [2021], Guo et al. [2021] improve
code completion systems with a reranking strategy to select better program candidates and with
structured predictions to generate more syntactically correct programs. Recent work such as [Clement
et al., 2020, Svyatkovskiy et al., 2020] adopt pretrained language models to exploit the learned
representations from large source code data and [Aye et al., 2021] tackles real-world code completion.
Compared to code completion, program synthesis requires systems to generate complete programs
from scratch and these programs are typically evaluated by their functional correctness through some
unit tests [Hendrycks et al., 2021, Li et al., 2022]. In this work, while we focus on program synthesis
from natural problem descriptions, we adopt a similar strategy to code completion in our generation
procedure to improve output programs.

3         CodeRL
3.1        Program Synthesis Task

Following a sequence-to-sequence approach, the program synthesis task contains a problem descrip-
tion as an input sequence D and an output sequence of program Ŵ = (ŵ1 , ..., ŵT ), ŵt ∈ V 4 that
can solve the problem. The output at each decoding step t is a distribution over the vocabulary V,
computed by the softmax function ŵt ∼ softmax(Linear(st )) where st is the contextual hidden
state at decoding step t. Conventionally, during train time, model parameters, θ, are learned by
maximizing the likelihood of the ground-truth reference programs. Denoting W = (w1 , ...wT ) as
the ground-truth program, the objective is to minimize the cross-entropy loss:
                               X                      X
                   Lce (θ) = −    log pθ (W |D) = −        log[pθ (wt |w1:t−1 , D)]              (1)
                                          t                          t

where the conditional probability pθ is parameterized following the above softmax function. During
test time, models generate sequences of programs by autoregressively sampling token ŵt from the
      4
          For simplicity, we use T as the notation of sequence length for all sequences which can actually be variable.


                                                             5
           Public
                                      Solution                               Unit         Solution
          Code on        Problem                           Problem
                                      Program                               Tests         Program
           Github
                pretraining
                                                                          Sampled
                                   Finetuned                Actor         program          Critic
      Pretrained LM                   LM                   Network                        Network



Figure 2: Overview of our actor-critic framework to optimize pretrained LMs for program
synthesis: We treat the LM as an actor network and sample synthetic samples from this actor.
Another neural network is trained as a critic model to evaluate these synthetic samples based on their
probabilities of passing unit tests. The returns are estimated based on critic scores and finally factored
into the learning objective Lrl to finetune the actor LM network using synthetic samples.


distribution pθ (.|ŵ1:t−1 , D). Models are evaluated against unit tests corresponding to the problem.
Each test includes a pair of input and ground-truth output. In real-world program synthesis tasks
[Hendrycks et al., 2021], example unit tests are often given as parts ofReturns
                                                                          the problem specification.
                                                        Actor-Critic RL Finetuning with
3.2        Pretraining Language Models on Code

We adopt Transformer models as the backbone of our program synthesis systems. Specifically, this
paper extends the CodeT5 model [Wang et al., 2021] as a foundation model for CodeRL.

CodeT5. CodeT5 [Wang et al., 2021] is a multi-lingual code-aware language model pretrained on
large-scale source code corpora curated from Github. With a unified encoder-decoder architecture,
CodeT5 achieves state-of-the-art performance in a wide range of code intelligence tasks in the
CodeXGLUE benchmark [Lu et al., 2021] including both code understanding and generation tasks.

Improving Pretraining Data. We enlarge the Python pretraining dataset using the recently released
large-scale Github Code dataset5 . We have compiled public, non-personal information from GitHub
consisting of permissively licensed Python code (e.g. “mit”, “apache-2”, “bsd-3-clause”, “bsd-2- 126
clause”, “cc0-1.0”, “unlicense”, “isc”). The resulting Python dataset (GCPY) has 10.5B tokens and is
10x larger than the CodeSearchNet (CSN) corpus [Husain et al., 2019] used in the original CodeT5
[Wang et al., 2021].

Improving Pretraining Objective. While pretraining tasks in CodeT5 like masked span prediction
(MSP) benefit code understanding tasks, they have a large discrepancy with program synthesis
objectives. To mitigate this gap, we introduce a pretraining task of next-token prediction (NTP) into
CodeT5. Specifically, we uniformly sample a pivot location for each code sample, then pass the
content preceding the pivot to the encoder and remaining to the decoder. To control the length of
input and output sequences, we restrict the pivot within 10% to 90% of the original sequence.

3.3        Program Synthesis as an RL Problem

We propose to formulate the Program Synthesis as an RL problem (see Figure 1, left) and apply an
actor-critic RL approach to improve the performance of a pretrained LM by exploiting the unit test
signals in both model optimization (see Figure 2) and generation procedure (see Figure 4).
More formally, we can view the learned parameters of an LM model, θ as a stochastic policy, which
decides an action as the prediction of each token. Following each action, an LM model updates its
hidden state representations which are used by the policy to determine the next action in the next
decoding step. At the end of the generation episode (i.e. an <endoftext> token is observed), the LM
      5
          https://huggingface.co/datasets/lvwerra/github-code


                                                    6
                            Linear & Softmax                  Max Pooling            Return Estimation



           Sequence-to-Sequence Model


        Problem                                                               Sample Test Results
                                                           Unit
                                                          Tests
                                                                             Baseline Test Results

               Sampled/Baseline/Ground-truth Programs

Figure 3: Overview of our critic model: The critic model is learned as an error
predictor. The model receives problem specifications and programs as input sequences.
For each program, the model is trained to predict one of four possible test outcomes:
{CompileError, RuntimeError, FailedTest, PassedTest}. The learned hidden state representa-
tions from the critic are then used to estimate returns of synthetic samples to finetune the actor
network. To improve and stabilize the training process, baseline programs are considered and relative
returns are factored into the loss function to optimize the actor network.


model receives a return r measured by the functional correctness of the generated program. The goal
of RL finetuning is to minimize the expected return:
                                        Lrl (θ) = −EW s ∼pθ [r(W s )]                                    (2)
           s
where W        = (w1s , ..., wTs ) is a synthetic sample in which each token wts is sampled by the LM model
at decoding time step t. Following the REINFORCE algorithm [Williams, 1992, Sutton and Barto,
2018] and policy gradient theorem [Sutton et al., 1999] we can define an estimate of the gradient
∇θ L(θ) of the non-differentiable return r as:
                       ∇θ Lrl (θ) ≈ −EW s ∼pθ [r(W s )∇θ log pθ (W s |D)]
                                                       X
                                  ≈ −EW s ∼pθ [r(W s )    ∇θ log pθ (wts |w1:t−1
                                                                           s
                                                                                 , D)]                   (3)
                                                          t

3.3.1    Defining Return by Unit Test Signals
For each sample sequence W s , the return r can be defined heuristically by checking its functional
correctness. We pass generated programs together with the corresponding unit tests to a compiler.
From the outputs of the tests, we can determine the return r:
                     -1.0      , if W s cannot be compiled (i.e. compile error)                   (4)
                   
                   
                                      s
                   
                    -0.6      , if W cannot be executed with unit tests (i.e. runtime error)     (5)
        r(W s ) =                     s
                   
                    -0.3      , if W   failed any unit test                                      (6)
                                     s
                     +1.0      , if W passed all unit tests                                       (7)
However, in related domains such as text-to-SQL research [Zhong et al., 2018, Xu et al., 2018], we
note that this approach to estimate returns can lead to unstable model training with high variance of
the gradient estimate following Eq. (3) with mini-batches in training.

3.3.2    Return with a Baseline
In order to alleviate this variance, we adopt a “baseline” [Sutton and Barto, 2018]. Specifically,
we use a greedy decoding strategy as a baseline and any generated samples that outperform this
baseline are given positive return estimation, and negative return estimation otherwise. This relative
normalization technique allows models to explore imperfect programs, as long as their returns are
better than the baseline’s. Given a training sample, we denote the return of the baseline r(W b ) and
the expected gradient is computed as:
                                                          X
              ∇θ Lrl (θ) ≈ −EW s ∼pθ [(r(W s ) − r(W b ))     ∇θ log pθ (wts |w1:t−1
                                                                               s
                                                                                     , D)]         (8)
                                                                  t



                                                      7
Note that at each decoding step t, our greedy decoding baseline is independent from the action wts
and hence, the expected gradient term ∇θ Lrl (θ) from Eq. (3) remains the same in Eq. (8).

3.3.3   Intermediate Return by Critic as Error Predictor
We observe that the above gradient estimate is only based on a final return at the end of the decoding
process. However, programs often follow fixed syntactical rules in which a single token such as an
additional white-space can render a program erroneous. Therefore, Eq. (8) becomes too restrictive.
A straightforward solution is to use token-based similarity scores [Papineni et al., 2002, Ren et al.,
                                      s
2020]) between each subsequence W1:t     and the ground truth. However, code matching is not an ideal
return measure due to its poor correlation with program correctness [Hendrycks et al., 2021, Chen
et al., 2021a, Austin et al., 2021] which can only be measured against fully complete programs.
Alternatively, we introduce a critic model. Figure 3 shows an overview of our critic model. The critic
model is parameterized as a neural network with parameters φ that receives inputs as the problem
description D and a sampled program W s = {w1s , . . . , wTs }. The critic is trained to infer the unit
test outcome; one of {CompileError, RuntimeError, FailedTest, PassedTest} as described in the
return definitions in Eq. (4) to (7). The training objective of the critic φ can be expressed as:
                                   Lcritic (φ) = − log pφ (u|W s , D)                                 (9)
where u denotes the ground-truth unit test outcome given by the compiler after passing W s to the
unit tests corresponding to the problem. We use Transformer models of smaller sizes than the actor
model as the base architecture for the critic model. The contextual hidden states of the program
tokens (h1 , . . . , hT ) obtained from the critic model decoder are max-pooled along the sequence
length dimension hpool = Pooling(h1 , . . . , hT ). The critic’s prediction on the unit test outcome is
computed as û = softmax(Linear(hpool )).
Given a learned critic, we use the probability distribution v̂t = softmax(Linear(ht )) to estimate the
token-level value q̂ of wts in relation to the ground-truth unit test output (note that we use the token
level contextual representation ht here, before the pooling operation). Specifically, q̂φ (wts ) = v̂t [u]
where v̂[.] denotes the probability of a specific unit test outcome from the four possible ones. We use
this estimate to train the actor LM model with intermediate returns:
                                                         X
          ∇θ Lrl (θ) ≈ −EW s ∼pθ [(r(W s ) − r(W b ))         q̂φ (wts )∇θ log pθ (wts |w1:t−1
                                                                                         s
                                                                                               , D)] (10)
                                                          t


Note that since our critic model is applied in a supervised learning environment with available ground
truth, we also use the training samples of perfect output programs W and assign them with the default
test outcome u = PassedTest to train the critic.

3.3.4   Generating Programs with Example Unit Tests and Critic
We leverage the unit tests provided in the input problem description to improve the generation
procedure during inference too (see Figure 4 for an overview and Appendix A for step-by-step
explanation). For each problem, we generate N programs, each of which is passed to example unit
tests that are often embedded as parts of problem specifications. Among the N programs, we denote
those that pass example tests as a set P and the remaining failed programs as a set F.

Program Refining. Note that although programs in P successfully pass example tests, it is not
guaranteed that these programs will succeed against the final hidden tests. Hidden tests are often
more comprehensive and may contain corner cases that challenge these programs. Therefore, we can
apply another round of generation to further refine the programs.
Specifically, we use sub-sequences from these program samples from P as prompts (or “seed”
sequences) to the actor LM. We employ a separate critic model (φtest ) to guide our choice of sub-
sequences from these filtered samples. This critic model is trained with a similar objective as
Eq. (9), but in a binary classification setup with {FailedTest, PassedTest} labels. Let W pass =
{w1 , . . . , wT } denote a generated sample that passes the example unit tests. We use the critic model
to assign a value to each token:
                             q̂φtest (wt ) = pφtest (û = PassedTest|w1:t , D)                       (11)


                                                    8
                                                    1
                                                …
                                             SeedM


Seed Sampling



                                          Extract example                                         Hidden unit
                Problem                                                Example unit tests
                                         input/output pairs                                          tests
                                                                                    2

          LMs finetuned for         1
                                                                        Filter by example
              program
                                                                         unit test results
           synthesis/repair

                      4a                Generated Programs                                      Final Programs


                                             Sample              3a                                Program
         Seed1 Seed
         Seed            Seed1
                 Seed1 Seed
                 Seed    Seed           sub-sequences by                Pass                       Refining
        Seed
        Seed 11 Seed 11 Seed 11                                                     Fail
                                          critic scoring

                                                                                    3b     If NUM(pass)=0


           ErrorProgram
                  Program+++        ErrorProgram
                                           Program+++                        Sample top
           Error
          Error
         Buggy   Program            Error
                                   Error
                                  Buggy   Program                                                 Program
            ErrorType/Msg
           Error  Type/Msg
                 Type/Msg            ErrorType/Msg
                                    Error  Type/Msg
                                          Type/Msg             Fail
                                                              Fail          sequences by
   4b     Error
          Error Type/Msg           Error
                                   Error Type/Msg                                                 Repairing
                                                                             critic scoring

  Figure 4: Overview of our Critic Sampling approach for program synthesis during inference:
  (1) For each test problem, we first use finetuned LM to generate a set of solution programs. (2) From
  the problem description, we extract example unit tests and test against generated solutions. (3a)
  If there are any passed solutions, we pass them to the critic model to sample sub-sequences. (4a)
  The sub-sequences from (3a) are used as seed sequences to condition the LM to regenerate solution
  programs, repeating the steps from (1) onward. (3b) If there are no passed solutions from (2), we pass
  current solutions to the critic model to select the best candidates. (4b) These candidates from (3b)
  are passed to a program repair model, together with their error types and compiler error messages.
  We repeat the same steps as (2) onward. Dotted lines indicate optional processes that apply during
  program refining or repairing.


  corresponding to the critic’s predicted probability of the sub-sequence till t passing the unit tests.
  We split the sequence at position tmax corresponding to the highest critic assigned value and use
  the left split as the seed for the next stage. If this seed sequence till tmax contains a token with
  pφtest (FailedTest) > pφtest (PassedTest), we further chop it at this token by removing tokens on the
  right. This is done to pick prompts that are likely to generate successful programs in the next round.
  We use these seeds to initialize and condition the (actor) LM to resample new tokens till we encounter
  the <endoftext > token. In this round, each seed sequence can be stacked N/|P| times for upsampling.
  This results in the same number of output programs N as in the first round of generation. Finally, we
  evaluate these N refined programs against the hidden unit tests.

  Program Repairing. Generating programs to solve a problem, especially a competition-level
  programming problem, involves a huge search space of possible programs. Very often, we observe
  complete failure where all programs fail against example tests, i.e. |F| = N . Therefore, for these
  cases, we employ an additional generation step to first repair programs before refining them.
  Specifically, We use the same critic model that is also employed in program refining, to sample top
  candidates from the set F. Let W fail denote a generated sample that fails the example unit tests. We
  use the critic model to assign a value to this sample:
                               q̂φtest (W fail ) = pφtest (û = PassedTest|W fail , D)                      (12)
  corresponding to the critic’s predicted probability of the the program passing the unit tests. We select
  top M programs with the highest probabilities and pass them to a program repair model ω.
  This program repair model is designed as a sequence-to-sequence generation model. The input
  sequence is the concatenation of the problem description D and buggy program W fail . We also
  include additional signals received from the unit test results, include the type of test outcomes (as
  defined in the return definitions in Eq. (4) to (7), and error subtypes (e.g. syntax errors, out-of-index


                                                         9
errors). The error types are extracted from error traces returned by the compiler. To train the program
repair model, we exploit the synthetic samples that is originally used in our RL training, as the buggy
programs W fail = W s . The ground-truth program W can be used as the expected correct program.
The training objective of the program repair model is to minimize the cross-entropy loss:
                     X                                   X
   Lrepair
     ce    (ω) = −      log pω (W |D, W fail , u, c) = −      log[pω (wt |w1:t−1 , D, W fail , u, c)] (13)
                     t                                     t

where u is one of {CompileError, RuntimeError, FailedTest, PassedTest} and c is the error sub-
type. During test time, each selected failed sequence can be stacked N/M times for upsampling.
This results in the same number of output programs N as in the first round of generation. Finally, we
pass these N repaired programs and apply the code refining procedure as before.

Critic Sampling. We call the dual strategy of program repairing and refining as “Critic Sampling”
(CS). This dual strategy allows models to generate and improve programs during inference, both from
success cases (program refining), and from failure cases (program repairing). In practice, we use
mini-batch generating to improve efficiency during inference and employ nucleus sampling with a
batch size of N = 200. Note that during program refining, while we do incur additional computation
costs to re-sample using the seed sequences, we are only required to generate partial programs in the
re-generation stage, making this stage less expensive than conventional generation.

3.4   Implementation Details

Due to the potential large number of trajectories (i.e. V T ) to generate a sequence and the unstable
feedback loop between actor and critic [Lillicrap et al., 2015, Wang et al., 2018], we applied imitation
learning to first warm-start a pretrained LM model with Lce only for up to 10 epochs. We then
sampled program sequences from this actor network to train the critic while keeping the parameters
of the actor network frozen. For experiments with CodeT5 actor models, we use the CodeT5-small
architecture for the critic model, and GPT2-small critic architecture when the actor models are GPT
variants. Following [Bahdanau et al., 2016], since our RL method is applied in a supervised learning
task, in addition to synthetic programs, we also use the ground-truth programs of training samples to
train the critic. These samples are considered perfect programs and always have a label of PassedTest.
After training the critic, we then apply both Lce and Lrl with equal weights to finetune the actor
network. To optimize the LM actor network, in practice, following previous work [Bahdanau et al.,
2016, Rennie et al., 2017, Wang et al., 2018], in each training optimization step, we can simply
approximate the expected gradient with a single sample Ws ∼ pθ :
                                                   X
                 ∇θ Lrl (θ) ≈ −(r(W s ) − r(W b ))     q̂φ (wts )∇θ log pθ (wts |w1:t−1
                                                                                  s
                                                                                        , D)        (14)
                                                     t


4     Experiments
4.1   Experimental Setups

Pretraining. We pretrain a CodeT5-large model (770M) from scratch following T5-large’s archi-
tecture [Raffel et al., 2020]. We follow the pretraining setups in CodeT5 [Wang et al., 2021] with the
modifications as proposed in Section 3.2. Specifically, we adopt the code-specific tokenizer from
Wang et al. [2021]. We employ 6 programming languages (PLs) in CodeSearchNet [Husain et al.,
2019] (CSN) instead of 8 PLs in CodeT5 as C/C# datasets are not publicly available. We apply
only the pretraining task of masked span prediction (MSP) from [Wang et al., 2021] and hence, do
not have to parse programs into abstract syntax trees (ASTs) to obtain the identifier information.
The last preprocessing step was required in other original pretraining tasks like masked identifier
prediction [Wang et al., 2021]. To further speed up training, we concatenate data samples to batch size
512 for pretraining with MSP and the resulting number of tokens is 1.1B. To validate the benefit of
using this new pretrained CodeT5 as our foundation model, we evaluate this model on CodeXGLUE
[Lu et al., 2021] and achieve new SOTA results (see Appendix B.1).
We perform our experiments on a kubernetes with 16 A100-40G GPUs on Google Cloud Platform
and the total pretraining duration is around 21 days. In the first pretraining stage with MSP, we
employ a corruption rate of 15%, a peak learning rate (LR) of 2e-4, and a batch size of 2048. We


                                                   10
pretrain on CSN for 150 epochs (10 days) and then on GCPY for 10 epochs (5 days). For the second
stage pretraining with NTP, we adopt a peak LR of 1e-4 and a batch size of 256, and pretrain for
10 epochs (6 days). We set the maximum length to 768 and 600 for source and target sequences
respectively for this objective. For all experiments, we employ an AdamW optimizer [Loshchilov and
Hutter, 2019] with a 0.05 weight decay and a linear decay LR scheduler with a warmup step of 1000.

Evaluation. We follow [Hendrycks et al., 2021, Chen et al., 2021a] and evaluate the models using
the pass@k metric, which is the percentage of problems solved by using k generated programs per
problem. We also follow [Li et al., 2022] and use n@k metric which only considers a subset of n
candidates from k generated programs per problem. The subset of n candidates are typically selected
by a filtering method by passing generated programs through example tests given as part of the
problem description [Chen et al., 2021a, Li et al., 2022]. Note that in our critic sampling procedure,
we can perform multiple rounds to refine/repair the programs based on their initial test results. In
practice, we limit to maximum one round of repairing and/or refining only.

4.2   Program Synthesis Benchmarks

APPS Benchmark. We choose the challenging APPS program synthesis benchmark [Hendrycks
et al., 2021], as it has large coding problems of varying difficulties collected from multiple coding
websites. APPS consists of 10,000 coding problems with a 50-50 train-test split. Each problem
is accompanied by 23.2 correct Python programs and 21.2 unit tests on average. The average
length per problem is 293.2 words and the average length per program is 18.0 lines. The dataset is
categorized into three levels of difficulty: Introductory (3639, train/test=2639/1000), Interview (5000,
train/test=2000/3000), and Competition (1361, train/test=361/1000). Each sample includes 20 unit
tests on average to validate the functional correctness of programs. We follow the same preprocessing
step as [Hendrycks et al., 2021] to formulate the input sequences from problem descriptions.
On APPS, we finetune our pretrained CodeT5 following our CodeRL framework (Section 4.3). To
warm-start CodeT5 models with Lce , we adopt a batch size of 64 and warmup LR from 0 to 2e-5 for
the first 500 steps and polynomially (power=0.5) decay to 1e-5 until the end of 10 epochs, which
takes around 30 hours on one A100 GPU. We set the maximum source and target sequence length to
600 and 512 respectively.

MBPP Benchmark. We additionally include another smaller and simpler Python program synthesis
dataset called MBPP [Austin et al., 2021] (Mostly Basic Programming Problems) for evaluation. The
dataset contains 974 instances with 374/90/500 instances for training/validation/testing respectively
and 10 reserved for few-shot learning. The problems are typically short, usually one sentence of
natural language descriptions each. Each problem is accompanied by 1 correct solution (6.8 lines
of code on average) and 3 unit tests in the form of assert statements for validating the functional
correctness. Unlike APPS, unit tests in MBPP are not hidden and are explicitly incorporated into the
source sequences for program synthesis models. This might encourage models to be overfitting to
these assert statements via hard-coding an if-expression very occasionally. However, for a fair
comparison with the baselines, we construct the source sequences in the same way as prior work.
Specifically, we adopt the same prompt format as [Austin et al., 2021] to prepare the input sequence
as: problem descriptions + “Your code should satisfy these tests:” + 3 assert statements.
On MBPP, we experiment with in both zero-shot (Section 4.5) and full finetuning (Appendix B.2)
setup. To finetune CodeT5, due to the small training set of MBPP, we finetune the models for 60
epochs with a constant LR of 2e-5 and a batch size of 32, which takes less than 30 mins on one A100.
We set the maximum source and target length to 382 and 306 respectively.

4.3   Experimental Results on APPS

Baselines. As reported by Hendrycks et al. [2021], we compared our models with several baselines,
including GPT2 [Radford et al., 2019], GPT-Neo [Black et al., 2021], and GPT3 [Brown et al., 2020].
We also compare the results with Codex [Chen et al., 2021a] and AlphaCode [Li et al., 2022]. Note
that by default, results of pretrained LMs (except for Codex and GPT3) are from models finetuned on
APPS using the standard loss Lce only. In our ablations, since CodeRL is model-agnostic, we can
also integrate it with GPT variants such as GPT-J [Wang and Komatsuzaki, 2021] and GPT-Neo.


                                                  11
Table 1: Results on the APPS benchmark: Overall, CodeRL can bring the performance gains of
CodeT5 models and achieves new SOTA on both pass@k and n@k metrics. “Intro”: introductory,
“Inter”: interview, “Comp”: competition-level tasks.
                                (a) Performance by pass@k with k = {1, 5, 1000}
                                      pass@1                       pass@5                       pass@1000
      Model       Size
                           Intro   Inter Comp     All    Intro   Inter Comp    All    Intro   Inter Comp        All
 Codex             12B     4.14    0.14    0.02   0.92    9.65   0.51   0.09   2.25   25.02    3.70    3.23     7.87
 AlphaCode         1B        -       -       -      -       -      -      -      -    17.67    5.24    7.06     8.09
 GPT3             175B     0.20    0.03    0.00   0.06      -      -      -      -      -        -       -        -
 GPT2             0.1B     1.00    0.33    0.00   0.40    2.70   0.73   0.00   1.02     -        -       -        -
 GPT2             1.5B     1.30    0.70    0.00   0.68    3.60   1.03   0.00   1.34   25.00    9.27    8.80    12.32
 GPT-Neo          2.7B     3.90    0.57    0.00   1.12    5.50   0.80   0.00   1.58   27.90    9.83   11.40    13.76
 GPT-J             6B      5.60    1.00    0.50   1.82    9.20   1.73   1.00   3.08   35.20   13.15 13.51      17.63
 CodeRL+CodeT5    770M     7.08    1.86    0.75   2.69   16.37   4.95   2.84   6.81   40.00   15.67 17.90      20.98

                         (b) Performance by n@k with k up to 50000 and n = {1, 5}
                                                         1@k                                  5@k
       Model             Size        k
                                            Intro    Inter Comp        All     Intro     Inter Comp            All
  Codex                12B          1000    22.78    2.64   3.04       6.75    24.52     3.23   3.08           7.46
  AlphaCode             1B          1000      -        -      -          -     14.36     5.63   4.58           7.17
  AlphaCode             1B         10000      -        -      -          -     18.18     8.21   6.65           9.89
  AlphaCode             1B         50000      -        -      -          -     20.36     9.66   7.75          11.42
  CodeRL+CodeT5       770M          1000    17.17    6.78   4.88       8.48    25.61     9.53   8.91          12.62


Overall Results. Firstly, Table 1a shows that the CodeRL with the CodeT5 model can achieve
significant performance gains, outperforming many pretrained LMs of much larger sizes. Specifically,
our approach achieved new SOTA results of 2.69% pass@1, 6.81% pass@5, and 20.98% pass@1000.
Table 1b shows that when evaluating on a subset of filtered code samples, our CodeRL+CodeT5 can
achieve SOTA results of 8.48% 1@k and 12.62% 5@k.
Secondly, similar to prior work Hendrycks et al. [2021], Austin et al. [2021], Chen et al. [2021a], we
also observe the benefits of upsampling generation when increasing the number of generation samples
k from 1 to 1000. Note that while CodeRL incurs additional computation cost during inference with
CS, our approach only requires much lower k to achieve comparable performance with other models.
Specifically, with k = 1000 only, our model performance is as good as AlphaCode with much a larger
generation budget of k = 50000. Finally, from Table 1b, we found that for challenging programming
tasks in interview and competition levels, finetuning can significantly improve model performance.
Specifically, we note that Codex, which was not finetuned on APPS and tested in a few-shot setting,
can achieve good n@1000 results, but the model fails dramatically at synthesis tasks in interview and
competition levels. This observation indicates a significant gap between the pretraining stage and
downstream synthesis tasks.

4.4   Ablation Studies

In this section, for a fair comparison between variants of return estimates and learning objectives, we
report the results of pass@k where k = {1, 5} with beam search decoding. For ablation analysis of
CodeRL during inference with larger k, we report the results with and without the CS procedure.

Impacts of Return Estimates. Table 2 show the results of CodeT5-770M trained by different
approaches to estimate returns of code samples. Overall, we report that the CodeRL objective with
relative token-level return estimates by our critic model (Model D) can achieve the best performance
on pass@1 and pass@5. Secondly, we note that using absolute returns without a baseline (Model B)
could lead to the most performance drop, as this approach heavily penalizes all incorrect samples
(even though they might still be better than a naive baseline). Hence, considering relative return
estimates that can effectively exploit imperfect codes can lead to better synthesis systems.
Thirdly, without a critic model, simply assigning identical rewards to all tokens in a code sample
(Model A) is disadvantageous as these return estimates are too restrictive to be used as feedback
signals for RL training. For instance, a program is considered incorrect only because of an additional
blank space character, which can result in a Indentation Error in a Python program. Simply assigning


                                                         12
Table 2: Ablation results with variants of return estimates: CodeT5 model that is trained with
return estimates using a baseline (Wb ) and a trained critic model q̂θ can achieve the best performance.
“dist.” indicates a rule-based approach that estimates returns following a linear decay by token
positions from t = 1 to t = T .
                                         pass@1                             pass@5
           # Wb        q̂φ
                             Intro Inter Comp All Intro Inter Comp All
           A    X       -     4.60 1.10        0.20     1.62 7.10 1.57           0.40     2.44
           B    -      X      4.00 0.87        0.20     1.36 5.60 1.30           0.20     1.94
           C    X     dist. 4.90 1.03          0.20     1.64 7.80 1.60           0.30     2.58
           D    X      X      6.20 1.50        0.30     2.20 9.39 1.90           0.42     3.10


Table 3: Ablation results with different learning objectives: We experiment with both CodeT5
and GPT-Neo with different combinations of cross-entropy loss Lce and reinforcement learning loss
Lrl . Note that these losses are applied on models that are already warm-started with conventional
cross-entropy losses for up to 10 epochs.
                                        pass@1                         pass@5
             Lce       Lrl
                              Intro Inter Comp All Intro Inter Comp All
                                             GPT-Neo
              -         -     3.90 0.57      0.00    1.12 5.50 0.80         0.00     1.58
              X         -     2.70 0.90      0.10    1.10 5.00 1.43         0.30     1.92
          X(+W s )      -     2.90 0.80      0.30    1.12 5.20 1.57         0.40     2.06
              -         X     3.30 0.80      0.20    1.18 5.30 1.57         0.20     2.04
              X         X     4.70 0.73      0.30    1.44 6.58 1.54         0.18     2.28
                                           CodeT5-770M
              -         -     6.60 1.03      0.30    2.00 8.80 1.67         0.70     2.90
              X         -     4.60 0.93      0.10    1.50 7.00 1.37         0.20     2.26
          X(+W s )      -     5.10 1.10      0.40    1.76 8.30 1.43         0.70     2.66
              -         X     5.00 0.90      0.50    1.64 7.60 1.53         0.60     2.56
              X         X     6.20 1.50      0.30    2.20 9.39 1.90         0.42     3.10


an identical reward to all tokens in this program will heavily penalize correct parts of the program
sequence. Finally, we experimented with a distance-based critic which assumes that token values
q̂(wts ) decay linearly from t = 1 to t = T (Model C). The lower performance suggests the benefit of
training a critic network to compute the returns rather than relying on rule-based approaches.

Impacts of Learning Objectives. Table 3 shows the results with different combinations of Lce
and Lrl . Since CodeRL is model-agnostic, we apply the ablation experiments to both CodeT5 and
GPT-Neo [Black et al., 2021]. Note that in these experiments, Lce and Lrl are applied on models
that are already warm-started/finetuned with Lce for up to 10 epochs. Firstly, when we experiment
with using only Lrl , we note the problem of vanishing gradients during finetuning, which was
similarly observed by Ranzato et al. [2016], Bahdanau et al. [2016]. Therefore, the final models
actually deteriorate and lead to performance drops. Secondly, we note that by using only Lce for
further finetuning, despite improvement in losses during training time, the model performance indeed
degrades during test time. We expect these models are overfitting to the training data, as similarly
observed in our analysis of pretrained models in Figure 6.
Interestingly, we found that a naive approach of Lce with synthetic samples W s , all of which are
treated as correct codes with r(W s ) = 1, still leads to some performance improvement with GPT-Neo
on pass@5. However, in all other cases, this training strategy does not work as well as considering a
critic model to estimate returns of Ws by their test results. Finally, we found that using both Lce and
Lrl results in a more consistent performance improvement overall on pass@1 and pass@5 for the
GPT-Neo and CodeT5 models.

Impact of Critic Sampling. Table 4 shows the ablation results of critical sampling (CS) during
inference, applied on CodeT5 models. We experiment with different combinations of program
refining and repairing steps. Overall, we found positive impacts of CS, combining both program
refining and repairing, across all metrics, with particularly more significant gains on pass@1000. We


                                                  13
Table 4: Ablation results of Critic Sampling (CS): We experiment with CodeT5 with different
combinations of program refining and repairing steps. Overall, compared to results without CS,
combining both approaches lead to the best program improvement. M : the number of top candidates
selected from program samples that fail example unit tests.
   Critic Sampling              pass@200                      pass@1000                      1@1000
 Refine     Repair    Intro   Inter Comp      All    Intro   Inter Comp     All    Intro   Inter Comp    All
   -          -       26.79    8.73   7.60   12.12   35.30   13.33 13.60   17.78   16.27   6.00   4.27   7.71
  X           -       29.10   9.67    9.50   13.52   38.10   14.33 15.70   19.36   16.52   6.16   4.15   7.83
  X        X(M = 1)   29.80   10.43 10.80    14.38   40.00   15.67 17.90   20.98   17.17   6.78   4.88   8.48
  X        X(M = 2)   30.20   10.20 11.50    14.46   39.90   15.57 18.00   20.92   16.96   6.82   4.90   8.47
  X        X(M = 4)   29.50   10.60 10.80    14.42   39.40   15.37 17.60   20.62   16.99   6.63   4.78   8.33




Figure 5: Results on APPS competition-level test samples: We investigate the most challenging
programming problem tasks, i.e. competition level, in the APPS benchmark. Integrating CodeRL
with both CodeT5 and GPT-J, we observe good performance improvement across pass@k and n@k
metrics, with increasing performance gains as k increases.


note that just program refining alone can help to bring performance gains, but its impact is reduced
on the 1@1000 metric. Note that n@k measures the solving rate among the subset P filtered from k
samples. As program refining will technically increase the size of this subset, the n@k metric will
consider an exponentially larger number of options of n samples than before. This will normalize
n@k by a larger pool of n candidate set, resulting in less impact of program refining on model
performance. We recommend additional post-processing steps such as candidate ranking [Cobbe
et al., 2021] to improve the performance of program refining, particularly on n@k metrics.
Secondly, when integrated program refining with program repairing (for problems where P = ∅),
we found further performance gains in all metrics. Interestingly, when experimenting with different
top-M selection schemes, we found the best overall performance with M = 1 and performance starts
to drop from M = 2 to M = 4 (except for pass@200 results). This observation indicates the benefit
of using the critic model to focus on the best candidates for program repairing rather than choosing
multiple program candidates. Moreover, with larger M , each program candidate will have a smaller
number of batch size (i.e. N/M ). This results in a lower chance for the program repair model to
properly repair and generate correct programs.

Results on Competition-level Tasks. We choose to investigate a subset of the APPS test split,
which contains the test samples of the highest difficulty level (i.e. competition programming tasks).
Figure 5 shows the results of pass@k and n@k with k ranging from 1 to 200 and n = {1, 5}, for
CodeRL+CodeT5 and CodeT5 only. Since CodeRL is model-agnostic, we also integrate it with
GPT-J [Wang and Komatsuzaki, 2021] and report the results. To focus on the impact of our RL
optimization, during test time, we compare models using only nucleus sampling and without the CS
procedure. Figure 5 shows that the performance gains are quite consistent on both GPT-J and CodeT5.
In particular, as k increases, the performance gain of CodeRL is more significant on both GPT-J
and CodeT5 models. We attribute these gains to the CodeRL learning objective Lrl that encourages
models to explore code solutions drawn from the model’s sampling distribution. During test time


                                                      14
Table 5: Ablation results of CodeT5 pretrained model variants: We report the results of models
pretrained on different configurations by model size, pretraining data, and pretraining task. CSN:
CodeSearchNet, GCPY: Github Code Python, MSP: Masked Span Predition, NTP: Next Token
Prediction. For a fair comparison, all models are finetuned only with Lce on APPS.
                                            pass@1                           pass@5
      Size     Data       Task
                                  Intro Inter Comp All Intro Inter Comp All
      60M      CSN        MSP     1.40 0.67         0.00   0.68 2.60 0.87         0.10    1.06
     220M      CSN        MSP     2.50 0.73         0.00   0.94 3.30 1.10         0.10    1.34
     770M      CSN        MSP     3.60 0.90         0.20   1.30 4.30 1.37         0.20    1.72
     770M +GCPY MSP               4.30 1.10         0.20   1.56 5.60 1.47         0.30    2.06
     770M +GCPY +NTP 6.60 1.03                      0.30   2.00 8.80 1.67         0.70    2.90




Figure 6: Ablation results by finetuning epochs: We report the finetuning progress of CodeT5-
770M models that are pretrained on different configurations by pretraining data and pretraining tasks.
CSN: CodeSearchNet, GCPY: Github Code Python, MSP: Masked Span Prediction, NTP: Next
Token Prediction. All models are finetuned only with Lce on APPS.


with an increasing k sampling budget, models are allowed to generate diverse code solutions and the
impact of Lrl becomes more significant.

Impacts of Pretraining Approaches for CodeT5. As commonly observed in prior work [Austin
et al., 2021, Chen et al., 2021a, Li et al., 2022], the performance of synthesis systems is correlated
with the quality of foundation models. In Table 5, we report the results of CodeT5 with different
configurations of model sizes, pretraining data, and pretraining objectives. For a fair comparison, all
models are only finetuned/ warm-started with Lce on APPS up to 12 epochs. As similarly observed
in prior work [Chen et al., 2021a, Austin et al., 2021], we found that scaling up the number of
model parameters (from 60M to 770M) can significantly improve model performance of downstream
synthesis tasks. When we improve the pretraining data by adding the GCPY dataset (10x larger than
the CSN dataset), we also observe good performance improvement, i.e. from 1.3 to 1.56 pass@1, and
1.72 to 2.06 pass@5. Finally, by combining the pretraining objective from Masked Span Prediction
(MSP) and Next Token Prediction (NTP), the model is able to adapt better to the downstream synthesis
task. Notably, adding NTP pretraining task can improve the performance from 2.06 to 2.9 pass@5.

Results by Finetuning Epochs with NTP Objective. Figure 6 shows the performance of CodeT5
model variants by finetuning epochs and by difficulty levels of programming tasks. Note that in
these experiments, we only need to compare among CodeT5 model variants by pretraining strategies,
and hence, only engage Lce in the finetuning stage on APPS. Consistent with our prior analysis,
enhancing both pretraining data (with larger data of GCPY) and pretraining objectives (with NTP
objective) improves model performance across training epochs in general. Moreover, as noted by our
analysis of learning objectives, only using Lce often leads to overfitting performance, typically after
epoch 10 in our case. Hence, to further finetune large-scale LMs, we recommend adopting our RL
objective Lrl to utilize synthetic training samples and avoid overfitting models.


                                                  15
Table 6: Results on the MBPP benchmark: we test the zero-shot transfer ability of CodeRL.
CodeRL+CodeT5 (ZS) which was trained on APPS with Lrl and evaluated on MBPP (Mostly Basic
Programming Problems) Benchmark [Austin et al., 2021] in a zero-shot setting, achieves new SOTA.
                         Model                     Size     pass@80
                         GPT                      224M          7.2
                         GPT                      422M         12.6
                         GPT                        1B         22.4
                         GPT                        4B         33.0
                         GPT                        8B         40.6
                         GPT                       68B         53.6
                         GPT                      137B         61.4
                         CodeRL+CodeT5 (ZS) 770M               63.0




Figure 7: Analysis of duplicated lines between MBPP and APPS: The overlap of data between
APPS and MBPP appears to be minimal, with only 12.6% MBPP programs with > 50% lines
duplicated in APPS training data.


4.5   Experimental Results on MBPP

Zero-shot evaluation on MBPP Benchmark. In addition to the APPS benchmark, we test the
zero-shot transfer ability of CodeRL on another smaller and simpler program synthesis benchmark
MBPP [Austin et al., 2021]. Table 6 reports the results of our CodeRL+CodeT5 on MBPP benchmark
compared with finetuned GPT models of up to 137B size. Our CodeRL+CodeT5 (ZS) was trained on
APPS and then evaluated on MBPP in a zero-shot setting. We observe that CodeRL with CodeT5 of a
much smaller model size yields surprisingly good zero-shot performance, setting a new SOTA result
of 63.0% pass@80 over GPT-137B’s 61.4% pass@80. This validates the strong zero-shot transfer
ability of CodeRL for unseen tasks.

Overlap between MBPP and APPS. A common concern about transfer learning is that the source
(APPS) and target (MBPP) tasks might have overlap in their training data, which could result in the
source model tending to memorize these substantially similar data when applied to the target task. To
address this concern, we analyze how many lines of code appear in both the training set of APPS and
programs of MBPP following Austin et al. [2021]. For this analysis, we discard code comments and
normalize the whitespaces for each line, and then exclude lines that appear more than twice anywhere
in MBPP, as these are likely to be common Python keywords such as return and break.
Figure 7 illustrates the number of absolute duplicated lines (Left) and relative fraction of duplicated
lines (Right) in the MBPP programs. As can be seen, the overlap between APPS and MBPP seems to
be minimal. Only 12.6% MBPP programs have more than half of their lines matched somewhere in
the APPS training data. Besides, more than half (514 out of 974) of programs have a zero overlap and
90.9% have only no more than 3 lines overlapped with the APPS training set. If we further require


                                                  16
                                     (a) Results on example unit tests




                                      (b) Results on hidden unit tests
Figure 8: Qualitative results by test outcomes: Using CodeT5 models with and without CodeRL,
we generate 200 programs per test sample on APPS and report the % programs per sample by their
unit test outcomes, including CompileError, RuntimeError, FailedTest, and PassedTest. Test outcomes
are defined accordingly to our definition in Eq. (4) to (7).


the lines to be consecutive, there are no more than 2 consecutive duplicated lines. More experimental
analysis is included in Appendix B.2.

4.6   Qualitative Analysis

Analysis by Unit Test Outcomes. Figure 8 demonstrates the average percentages of generated pro-
grams per problem, grouped by their test outcomes. Specifically, we use CodeT5 or CodeRL+CodeT5
to generate programs and randomly select 200 generated programs per test sample in the APPS
test split. We pass programs to either example unit tests or hidden unit tests and group the output
programs by their test outcomes. The outcomes are categorized according to our definition in Eq. (4)
to (7), including CompileError, RuntimeError, FailedTest, and PassedTest.
First, on both example unit tests and hidden unit tests, we observe that integrating CodeRL can
increase the likelihood that a program can pass the tests, and reduces the probability that it fails one or
more unit tests. The probability to pass unit tests are improved more significantly in introductory-level
programming problems.
Secondly, we note that the percentages of having compiling errors decrease in CodeRL-generated
programs, with more effects on interview and competition-level problems. As compiling errors are
less likely to occur with CodeRL programs, these programs are still suffered from runtime errors.
This leads to a higher probability that a CodeRL program contains runtime errors. More analysis of
compiling and runtime failures is described in Appendix C.1.
We note that there are quite significant performance gaps by test outcomes between example unit
tests (Figure 8a) and hidden unit tests (Figure 8b). This observation suggests that example tests are
not as comprehensive as hidden tests and hence, limit the positive impacts of our CodeRL generation
procedure due to false positives. We recommend additional methods to improve example unit tests,
such as through data augmentation by mutating input/output pairs [Austin et al., 2021].

Example Generated Program. Figure 9 shows an example of a programming problem from the
APPS benchmark and corresponding programs generated by CodeT5 variants. Specifically, based
on the same foundation pretrained CodeT5 (pretrained with GCPY data and NTP objective), we
compare the CodeT5 model that is finetuned by Lce only and another model that follows our CodeRL
framework. In CodeRL+CodeT5, we further show programs before and after applying the CS
procedure. We found that applying CodeRL can generate more appropriate programs and using the
CS procedure further improves their functional correctness. For instance, in Figure 9, CodeT5 model


                                                    17
                         Input Problem                                    Example Unit Tests            Hidden Unit Tests
  QUESTION:                                                                                          Input: 10 399603090
  Holidays have finished. Thanks to the help of the hacker                                           Output: 3628800
  Leha, Noora managed to enter the university of her dreams              Input:    4 3
  which is located in a town Pavlopolis. It's well known that            Output:   6                 Input:    5 5
                                                                                                     Output:   120
  universities provide students with dormitory for the period of
                                                                                                     ...
  university studies. Consequently Noora had to leave
  Vičkopolis and move to Pavlopolis. Thus Leha was left                                  Ground-truth Program
  completely alone in a quiet town Vičkopolis. He almost
  even fell into a depression from boredom!

  Leha came up with a task for himself to relax a little. He
  chooses two integers A and B and then calculates the
  greatest common divisor of integers "A factorial" and "B
  factorial". Formally the hacker wants to find out GCD(A!,
  B!). It's well known that the factorial of an integer x is a
  product of all positive integers less than or equal to x. Thus                         CodeT5 Output Program
  x! = 1·2·3·...·(x - 1)·x. For example 4! = 1·2·3·4 = 24. Recall
  that GCD(x, y) is the largest positive integer q that divides
  (without a remainder) both x and y.

  Leha has learned how to solve this task very effective. You                                                               FAILE
  are able to cope with it not worse, aren't you?                                         Example tests: Failed             TEST
                                                                                           Hidden tests: Failed

  -----Input-----                                                          CodeRL+CodeT5 Output Program (before CS)

  The first and single line contains two integers A and B (1 ≤
  A, B ≤ 10^9, min(A, B) ≤ 12).


  -----Output-----

  Print a single integer denoting the greatest common divisor                                                               RUNTIM
  of integers A! and B!.                                                                                                     ERRO
                                                                                                                            (timeo


  -----Example-----
  Input                                                                               Example tests: Passed
  43                                                                           Hidden tests: RuntimeError (TimeOut)

  Output                                                                    CodeRL+CodeT5 Output Program (after CS)
  6



  -----Note-----                                                                                                            PASSE
                                                                                                                             TEST
  Consider the sample.

  4! = 1·2·3·4 = 24. 3! = 1·2·3 = 6. The greatest common
  divisor of integers 24 and 6 is exactly 6.
  Use Standard Input format
                                                                                         Example tests: Passed
  ANSWER:                                                                                 Hidden tests: Passed

Figure 9: An example interview-level APPS programming task and programs generated
by CodeT5 variants: The program generated by CodeT5 model fails all unit tests while
CodeRL+CodeT5 (without CS generation) can generate a functionally correct program. How-
ever, this program leads to runtime errors in extreme test cases. After applying the CS generation
procedure, the program is improved and able to pass all hidden unit tests.


misunderstands the problem and focuses on finding the greatest common divisor between a and b
only. Instead, the CodeRL model avoids this mistake and tackles the problem of finding the greatest
common divisor between the factorials of a and b.
We also found that CodeRL can improve the complexity of the generated programs, an important
quality in complex programming problems. For instance, in the interview-level program in Figure
9, we note that without applying CS, the generated program is functionally correct but fails during
execution due to a timeout error. This program simply computes separate factorials of both a and
b, which will slow down the execution in scenarios with extremely large a or b. Applying the CS


                                                                    18
procedure can condition models on parts of the prior program and (re)generates new tokens to produce
a more efficient program. In the example in Figure 9, the factorials are computed on min(a,b) to
improve the efficiency of the programs. Hence, the resulting final program is able to pass all hidden
unit tests (including tests with extremely large values) without timeout errors.
For additional example generated programs, please refer to Appendix C.2.


5   Limitations and Broader Impacts

Program synthesis can lead to substantial positive social impacts, e.g., transforming future software
developing tools, increasing the productivity of developers, and improving the accessibility and
quality of programming courses. We propose CodeRL as a general framework to improve the
performance of code generated from language models. We refer readers to the limitations and broader
impacts discussed at length by Chen et al. [2021a] as these would apply to the different actor models
one can use with CodeRL. The risks and limitations are critical to be considered before deploying
such models at scale.
One major limitation highlighted in many contemporary systems is that language models trained on
code can generate code that is biased, and can even generate toxic natural language as code comments.
Similar to previous work in language generation [Ouyang et al., 2022], besides improving functional
correctness, RL could be used to align the models as per human preferences. Guided or weighted
decoding schemes [Krause et al., 2021] or safety-specific control tokens [Xu et al., 2020] could also
be explored to guide the generation of code towards desirable attributes like being secure, reliable,
fast, efficient, fair, and representative.
Another data bias we need to consider is related to the system security of pretraining data. For
example, pretraining data from public Github code repositories may contain vulnerabilities and the
resulting synthesis models may generate programs with weak security measures [Hammond Pearce
et al., 2021]. Thus, similar to other code generation systems based on large LMs, CodeRL’s output
does warrant verification by qualified human developers.
Another limitation of our approach is the computational cost of training the critic model to estimate
returns in addition to the original LM (actor network). However, in practice, we found that training a
good critic model does not require large-scale models to attain a decent performance. For instance,
a finetuned critic model initialized from a pretrained GPT-2 (small) can achieve over 75% error
prediction accuracy on synthetic samples. Thus fine-tuning costs for the critic model are minor
compared to the pretraining of the original LM. With CodeRL, we obtain performance superior
to much larger pre-trained language models. Combining CodeRL with smaller models (e.g. a
CodeT5-770M) will have significantly lesser inference costs for generating programs.
Finally, previous works on code generation have highlighted how systems trained with the next token
prediction objective exhibit alignment failure - model outputs not being aligned with the user’s intent
despite the model being capable of doing so. This holds true for CodeRL too, as we do witness
generated code that sometimes does not satisfy user requirements in terms of the unit tests. However,
unlike previous works, CodeRL’s output can be tailored heavily by a user through the problem
description as well as the unit tests that the solution is expected to pass. By leveraging unit tests
during training, and during inference, CodeRL, when applied with a base code generation system,
improves its alignment with the user intent. CodeRL’s ability to improve alignment can be crucial in
addressing misalignment issues which are predicted by Chen et al. [2021a] to get worse as we scale
up data, parameters, and training time.


6   Conclusion

We present CodeRL, a novel framework for program synthesis, using deep reinforcement learning
to improve pretrained LMs, by exploiting unit test signals in both training and inference stages.
Specifically, we introduce an actor-critic training approach to optimize pretrained LMs with dense
feedback signals on synthetic code samples. During inference, we propose a new generation procedure
with critical sampling, which enables the model to automatically regenerate programs based on
feedback from unit tests and critic scores. We integrate CodeRL with the improved CodeT5-large
model (770M) and achieve new SOTA results on both the APPS and MBPP benchmarks, surpassing


                                                  19
the prior SOTA by massive pretrained LMs of much larger model sizes. Our comprehensive analysis
shows that CodeRL achieved consistent improvement upon the conventional pretrained LMs for code
generation tasks. CodeRL is a general framework that integrates pretrained LMs and RL holistically
for program synthesis, and can be extended and improved in various ways. For example, it can
be easily integrated with other better pretrained LMs and can be improved with more fine-grained
feedback from the environment, such as feedback received from a static code analyzer.

Acknowledgements
We would like to thank our Salesforce Research team for fruitful discussions and feedback.

References
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry,
   Q. Le, et al. Program synthesis with large language models. arXiv preprint arXiv:2108.07732,
   2021.
G. A. Aye, S. Kim, and H. Li. Learning autocompletion from real-world datasets. In 2021 IEEE/ACM
  43rd International Conference on Software Engineering: Software Engineering in Practice (ICSE-
  SEIP), pages 131–139. IEEE, 2021.
D. Bahdanau, P. Brakel, K. Xu, A. Goyal, R. Lowe, J. Pineau, A. Courville, and Y. Bengio. An
  actor-critic algorithm for sequence prediction. arXiv preprint arXiv:1607.07086, 2016.
M. Balog, A. L. Gaunt, M. Brockschmidt, S. Nowozin, and D. Tarlow. Deepcoder: Learning to write
  programs. arXiv preprint arXiv:1611.01989, 2016.
S. Bengio, O. Vinyals, N. Jaitly, and N. Shazeer. Scheduled sampling for sequence prediction with
   recurrent neural networks. Advances in neural information processing systems, 28, 2015.
S. Black, G. Leo, P. Wang, C. Leahy, and S. Biderman. Gpt-neo: Large scale autoregressive language
   modeling with mesh-tensorflow. URL https://doi. org/10.5281/zenodo, 5297715, 2021.
T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam,
   G. Sastry, A. Askell, et al. Language models are few-shot learners. Advances in neural information
   processing systems, 33:1877–1901, 2020.
M. Bruch, M. Monperrus, and M. Mezini. Learning from examples to improve code completion
 systems. In Proceedings of the 7th joint meeting of the European software engineering conference
 and the ACM SIGSOFT symposium on the foundations of software engineering, pages 213–222,
 2009.
R. Bunel, M. Hausknecht, J. Devlin, R. Singh, and P. Kohli. Leveraging grammar and reinforcement
  learning for neural program synthesis. In International Conference on Learning Representations,
  2018. URL https://openreview.net/forum?id=H1Xw62kRZ.
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda,
 N. Joseph, G. Brockman, et al. Evaluating large language models trained on code. arXiv preprint
 arXiv:2107.03374, 2021a.
Q. Chen, J. Lacomis, E. J. Schwartz, G. Neubig, B. Vasilescu, and C. Le Goues. VarCLR: Variable
  semantic representation pre-training via contrastive learning. In International Conference on
  Software Engineering, ICSE ’22, 2022.
X. Chen, D. Song, and Y. Tian. Latent execution for neural program synthesis beyond domain-specific
  languages. Advances in Neural Information Processing Systems, 34, 2021b.
C. Clement, D. Drain, J. Timcheck, A. Svyatkovskiy, and N. Sundaresan. PyMT5: multi-mode
  translation of natural language and python code with transformers. In Proceedings of the 2020
  Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 9052–9065,
  Online, Nov. 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.emnlp-main.
  728. URL https://aclanthology.org/2020.emnlp-main.728.


                                                 20
K. Cobbe, V. Kosaraju, M. Bavarian, J. Hilton, R. Nakano, C. Hesse, and J. Schulman. Training
  verifiers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021.
J. Devlin, J. Uesato, S. Bhupatiraju, R. Singh, A.-r. Mohamed, and P. Kohli. Robustfill: Neural
   program learning under noisy i/o. In International conference on machine learning, pages 990–998.
   PMLR, 2017.
K. Ellis, D. Ritchie, A. Solar-Lezama, and J. Tenenbaum. Learning to infer graphics programs from
  hand-drawn images. Advances in neural information processing systems, 31, 2018.
K. Ellis, M. Nye, Y. Pu, F. Sosa, J. Tenenbaum, and A. Solar-Lezama. Write, execute, assess: Program
  synthesis with a repl. Advances in Neural Information Processing Systems, 32, 2019.
Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong, L. Shou, B. Qin, T. Liu, D. Jiang, and
  M. Zhou. CodeBERT: A pre-trained model for programming and natural languages. In Findings
  of the Association for Computational Linguistics: EMNLP 2020, pages 1536–1547, Online, Nov.
  2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.findings-emnlp.139.
  URL https://aclanthology.org/2020.findings-emnlp.139.
Y. Ganin, T. Kulkarni, I. Babuschkin, S. A. Eslami, and O. Vinyals. Synthesizing programs for
  images using reinforced adversarial learning. In International Conference on Machine Learning,
  pages 1666–1675. PMLR, 2018.
S. Gulwani, W. R. Harris, and R. Singh. Spreadsheet data manipulation using examples. Communica-
   tions of the ACM, 55(8):97–105, 2012.
D. Guo, A. Svyatkovskiy, J. Yin, N. Duan, M. Brockschmidt, and M. Allamanis. Learning to complete
  code with sketches. In International Conference on Learning Representations, 2021.
K. Guu, P. Pasupat, E. Liu, and P. Liang. From language to programs: Bridging reinforcement
  learning and maximum marginal likelihood. In Proceedings of the 55th Annual Meeting of the
  Association for Computational Linguistics (Volume 1: Long Papers), pages 1051–1062, Vancouver,
  Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1097. URL
  https://aclanthology.org/P17-1097.
B. A. Hammond Pearce, B. Tan, B. Dolan-Gavitt, and R. Karri. An empirical cybersecurity evaluation
  of github copilot’s code contributions. arXiv preprint arXiv:2108.09293, 2021.
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He,
  D. Song, and J. Steinhardt. Measuring coding challenge competence with apps. NeurIPS, 2021.
H. Husain, H. Wu, T. Gazit, M. Allamanis, and M. Brockschmidt. Codesearchnet challenge:
  Evaluating the state of semantic code search. CoRR, abs/1909.09436, 2019.
J. Johnson, B. Hariharan, L. Van Der Maaten, J. Hoffman, L. Fei-Fei, C. Lawrence Zitnick, and
   R. Girshick. Inferring and executing programs for visual reasoning. In Proceedings of the IEEE
   International Conference on Computer Vision, pages 2989–2998, 2017.
A. Joulin and T. Mikolov. Inferring algorithmic patterns with stack-augmented recurrent nets.
  Advances in neural information processing systems, 28, 2015.
V. Konda and J. Tsitsiklis. Actor-critic algorithms. Advances in neural information processing
  systems, 12, 1999.
B. Krause, A. D. Gotmare, B. McCann, N. S. Keskar, S. Joty, R. Socher, and N. F. Rajani. GeDi:
  Generative discriminator guided sequence generation. In Findings of the Association for Computa-
  tional Linguistics: EMNLP 2021, pages 4929–4952, Punta Cana, Dominican Republic, Nov. 2021.
  Association for Computational Linguistics. doi: 10.18653/v1/2021.findings-emnlp.424. URL
  https://aclanthology.org/2021.findings-emnlp.424.
T. D. Kulkarni, W. F. Whitney, P. Kohli, and J. Tenenbaum. Deep convolutional inverse graphics
   network. Advances in neural information processing systems, 28, 2015.
K. Kurach, M. Andrychowicz, and I. Sutskever. Neural random-access machines. arXiv preprint
  arXiv:1511.06392, 2015.


                                                21
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gi-
  meno, A. D. Lago, et al. Competition-level code generation with alphacode. arXiv preprint
  arXiv:2203.07814, 2022.

C. Liang, M. Norouzi, J. Berant, Q. V. Le, and N. Lao. Memory augmented policy optimization for
  program synthesis and semantic parsing. Advances in Neural Information Processing Systems, 31,
  2018.

P. Liang, M. I. Jordan, and D. Klein. Learning programs: A hierarchical bayesian approach. In
   Proceedings of the 27th International Conference on Machine Learning (ICML-10), pages 639–646,
   2010.

T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra. Continuous
   control with deep reinforcement learning. arXiv preprint arXiv:1509.02971, 2015.

C.-Y. Lin. Rouge: A package for automatic evaluation of summaries. Text Summarization Branches
  Out, 2004.

Y. Liu, J. Wu, Z. Wu, D. Ritchie, W. T. Freeman, and J. B. Tenenbaum. Learning to describe
  scenes with programs. In International Conference on Learning Representations, 2019. URL
  https://openreview.net/forum?id=SyNPk2R9K7.

I. Loshchilov and F. Hutter. Decoupled weight decay regularization. In ICLR (Poster). OpenRe-
   view.net, 2019.

S. Lu, D. Guo, S. Ren, J. Huang, A. Svyatkovskiy, A. Blanco, C. B. Clement, D. Drain, D. Jiang,
   D. Tang, G. Li, L. Zhou, L. Shou, L. Zhou, M. Tufano, M. Gong, M. Zhou, N. Duan, N. Sundaresan,
   S. K. Deng, S. Fu, and S. Liu. Codexglue: A machine learning benchmark dataset for code
   understanding and generation. In NeurIPS Datasets and Benchmarks, 2021.

Z. Manna and R. J. Waldinger. Toward automatic program synthesis. Communications of the ACM,
  14(3):151–165, 1971.

E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou, S. Savarese, and C. Xiong. A conversa-
   tional paradigm for program synthesis. arXiv preprint arXiv:2203.13474, 2022.

L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal,
  K. Slama, A. Ray, et al. Training language models to follow instructions with human feedback.
  arXiv preprint arXiv:2203.02155, 2022.

K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu. Bleu: a method for automatic evaluation of machine
  translation. In Proceedings of the 40th annual meeting on association for computational linguistics,
  pages 311–318. Association for Computational Linguistics, 2002.

E. Parisotto, A.-r. Mohamed, R. Singh, L. Li, D. Zhou, and P. Kohli. Neuro-symbolic program
  synthesis. arXiv preprint arXiv:1611.01855, 2016.

G. Poesia, A. Polozov, V. Le, A. Tiwari, G. Soares, C. Meek, and S. Gulwani. Synchromesh: Reliable
  code generation from pre-trained language models. In International Conference on Learning
  Representations, 2022. URL https://openreview.net/forum?id=KmtVD97J43e.

A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever, et al. Language models are
  unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.

C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu.
  Exploring the limits of transfer learning with a unified text-to-text transformer. J. Mach. Learn.
  Res., 21:140:1–140:67, 2020.

M. Ranzato, S. Chopra, M. Auli, and W. Zaremba. Sequence level training with recurrent neural
 networks. In Y. Bengio and Y. LeCun, editors, 4th International Conference on Learning Repre-
 sentations, ICLR 2016, San Juan, Puerto Rico, May 2-4, 2016, Conference Track Proceedings,
 2016. URL http://arxiv.org/abs/1511.06732.


                                                    22
V. Raychev, M. Vechev, and E. Yahav. Code completion with statistical language models. In
  Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and
  Implementation, pages 419–428, 2014.
S. Ren, D. Guo, S. Lu, L. Zhou, S. Liu, D. Tang, N. Sundaresan, M. Zhou, A. Blanco, and S. Ma.
   Codebleu: a method for automatic evaluation of code synthesis. arXiv preprint arXiv:2009.10297,
   2020.
Z. Ren, X. Wang, N. Zhang, X. Lv, and L.-J. Li. Deep reinforcement learning-based image captioning
   with embedding reward. In Proceedings of the IEEE conference on computer vision and pattern
   recognition, pages 290–298, 2017.
S. J. Rennie, E. Marcheret, Y. Mroueh, J. Ross, and V. Goel. Self-critical sequence training for image
   captioning. In Proceedings of the IEEE conference on computer vision and pattern recognition,
   pages 7008–7024, 2017.
R. Robbes and M. Lanza. How program history can improve code completion. In 2008 23rd
  IEEE/ACM International Conference on Automated Software Engineering, pages 317–326. IEEE,
  2008.
P. D. Summers. A methodology for lisp program construction from examples. Journal of the ACM
   (JACM), 24(1):161–175, 1977.
S.-H. Sun, H. Noh, S. Somasundaram, and J. Lim. Neural program synthesis from diverse demonstra-
   tion videos. In J. Dy and A. Krause, editors, Proceedings of the 35th International Conference
   on Machine Learning, volume 80 of Proceedings of Machine Learning Research, pages 4790–
   4799. PMLR, 10–15 Jul 2018. URL https://proceedings.mlr.press/v80/sun18a.
   html.
R. S. Sutton. Temporal credit assignment in reinforcement learning. PhD thesis, University of
  Massachusetts Amherst, 1984.
R. S. Sutton and A. G. Barto. Reinforcement learning: An introduction. MIT press, 2018.
R. S. Sutton, D. McAllester, S. Singh, and Y. Mansour. Policy gradient methods for reinforcement
  learning with function approximation. Advances in neural information processing systems, 12,
  1999.
A. Svyatkovskiy, S. K. Deng, S. Fu, and N. Sundaresan. Intellicode compose: Code generation using
  transformer. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering
  Conference and Symposium on the Foundations of Software Engineering, pages 1433–1443, 2020.
A. Svyatkovskiy, S. Lee, A. Hadjitofi, M. Riechert, J. V. Franco, and M. Allamanis. Fast and
  memory-efficient neural code completion. In 2021 IEEE/ACM 18th International Conference on
  Mining Software Repositories (MSR), pages 329–340. IEEE, 2021.
Y. Tian, A. Luo, X. Sun, K. Ellis, W. T. Freeman, J. B. Tenenbaum, and J. Wu. Learning to infer and
   execute 3d shape programs. In International Conference on Learning Representations, 2019. URL
   https://openreview.net/forum?id=rylNH20qFQ.
D. Trivedi, J. Zhang, S.-H. Sun, and J. J. Lim. Learning to synthesize programs as interpretable and
  generalizable policies. Advances in Neural Information Processing Systems, 34:25146–25163,
  2021.
A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin.
  Attention is all you need. Advances in neural information processing systems, 30, 2017.
R. Vedantam, C. Lawrence Zitnick, and D. Parikh. Cider: Consensus-based image description
  evaluation. In Proceedings of the IEEE conference on computer vision and pattern recognition,
  pages 4566–4575, 2015.
R. J. Waldinger and R. C. Lee. Prow: A step toward automatic program writing. In Proceedings of
  the 1st international joint conference on Artificial intelligence, pages 241–252, 1969.


                                                 23
B. Wang and A. Komatsuzaki. GPT-J-6B: A 6 Billion Parameter Autoregressive Language Model.
  https://github.com/kingoflolz/mesh-transformer-jax, May 2021.

X. Wang, W. Chen, J. Wu, Y.-F. Wang, and W. Y. Wang. Video captioning via hierarchical rein-
  forcement learning. In Proceedings of the IEEE Conference on Computer Vision and Pattern
  Recognition, pages 4213–4222, 2018.

Y. Wang, W. Wang, S. R. Joty, and S. C. H. Hoi. Codet5: Identifier-aware unified pre-trained
  encoder-decoder models for code understanding and generation. In EMNLP (1), pages 8696–8708.
  Association for Computational Linguistics, 2021.

M. White, C. Vendome, M. Linares-Vásquez, and D. Poshyvanyk. Toward deep learning software
 repositories. In 2015 IEEE/ACM 12th Working Conference on Mining Software Repositories, pages
 334–345. IEEE, 2015.

R. J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement
  learning. Machine learning, 8(3):229–256, 1992.

J. Wu, J. B. Tenenbaum, and P. Kohli. Neural scene de-rendering. In Proceedings of the IEEE
   Conference on Computer Vision and Pattern Recognition (CVPR), July 2017.

J. Xu, D. Ju, M. Li, Y.-L. Boureau, J. Weston, and E. Dinan. Recipes for safety in open-domain
   chatbots. arXiv preprint arXiv:2010.07079, 2020.

X. Xu, C. Liu, and D. Song. SQLNet: Generating structured queries from natural language without re-
  inforcement learning, 2018. URL https://openreview.net/forum?id=SkYibHlRb.

J. Yang, S. E. Reed, M.-H. Yang, and H. Lee. Weakly-supervised disentangling with recurrent
   transformations for 3d view synthesis. Advances in neural information processing systems, 28,
   2015.

P. Yin and G. Neubig. A syntactic neural model for general-purpose code generation. In Proceedings
   of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
   Papers), pages 440–450, Vancouver, Canada, July 2017. Association for Computational Linguistics.
   doi: 10.18653/v1/P17-1041. URL https://aclanthology.org/P17-1041.

V. Zhong, C. Xiong, and R. Socher. Seq2SQL: Generating structured queries from natural lan-
  guage using reinforcement learning, 2018. URL https://openreview.net/forum?id=
  Syx6bz-Ab.


A     Critic Sampling Procedure
Refer to Algorithm 1 for a step-by-step explanation of our critic sampling procedure.

B     Additional Experimental Results
B.1   CodeXGLUE Benchmark Results

To validate the effectiveness of our simplified pretraining strategies of CodeT5-large, we extensively
evaluate it on a variety of generation tasks in CodeXGLUE [Lu et al., 2021], including code-to-text
generation (i.e. summarization, see Table 7), text-to-code generation (see Table 8), and code-to-code
generation (i.e., code translation and code refinement, see Table 9). Different from APPS [Hendrycks
et al., 2021] and MBPP [Austin et al., 2021], we follow the default similarity-based evaluation
metrics in the CodeXGLUE benchmark, including BLEU [Papineni et al., 2002] and CodeBLEU
[Ren et al., 2020], and exact match (EM) scores. Table 7, 8, and 9 show that our simplified pretrained
CodeT5-large sets new SOTA results on a large majority of the tasks, and hence, can be served as a
better foundation model for other code-related generation tasks. Note that in these experiments, we
employ the conventional finetuning objective with Lce and there might be potential to improve the
performance further with our CodeRL framework.


                                                 24
  Algorithm 1: Critic sampling procedure to generate programs
  Input: Problem D, Language model θ, Critic model φ, Language model for program repair ω
  Output: A set of N generated solution programs
1 begin
     /* extract example unit tests from problem */
2    example unit tests I ←− ExtractExampleInputOutput(D)
3    a set of programs for repair R ← ∅
4    while True do
5        a set of output programs S ←− ∅
6        if |R| = 0 then
             /* generate program solutions by LM */
7            for N times do
8                Ŵi ←− Sampling pθ (Wi |D) ←− Sampling pθ (wti |w1:t−1
                                                                  i
                                                                        , D)
9                S ←− S ∪ {Ŵi }
10       else
             /* repair current programs by LM */
11           upsampling param K = N/|R|
12           for each filtered program Ŵifail ∈ R do
13               Obtain corresponding test outcome ui and error message ci
14               for K times do
15                   Ŵj ←− Sampling pω (Wj |D, Ŵifail , ui , ci ) ←−
                                         j
                      Sampling pω (wtj |w1:t−1 , D, Ŵifail , ui , ci )
16                   S ←− S ∪ {Ŵj }

        /* filter programs based on their test results */
17      sets of filtered programs P ← ∅, F ← ∅
18      for each generated program Ŵi ∈ S do
19           Testoutcomes ui ←− RunTests(Ŵi , I)
20           if ui = “PassedTest” then P ←− P ∪ {Ŵi }
21           else F ←− F ∪ {Ŵi }
22      if |P| > 0 then break
23      else
            /* Sort failed programs and select top candidates */
24           Sort F by critic scores pφ (ui = PassedTest|Ŵi , D) ∀ Ŵi ∈ F
25           a set of programs R ←− top-M from F
     /* Use passed programs to select sub-sequences */
                            0
26   upsampling param N = N/|P|
                                0
27   a set of output solutions S ←− ∅
28   for each filtered program Ŵi ∈ P do
29       subsequence Ŵisub ←− Sampling pφ (ui = PassedTest|Ŵi , D)
30             ←− Sampling pφ (ui = PassedTest|ŵ1:t−1 , D)
         /* subsequence as seeds to regenerate programs */
31       length of subsequence m ←− |Ŵisub |
                0
32       for N times do
33           Ŵj ←− Sampling pθ (Wj |Ŵisub , D) ←− Sampling pθ (wtj |wm:t−1
                                                                       j
                                                                             , Ŵisub , D)
               0       0
34           S ←− S ∪ {Ŵj }
     /* return the regenerated programs for evaluation */
              0
35   return S




                                                25
         Table 7: Code-to-Text generation results (smoothed BLEU-4) on CodeXGLUE
        Model           Ruby JavaScript        Go     Python Java      PHP Overall
        RoBERTa         11.17     11.90       17.72 18.14 16.47 24.02        16.57
        CodeBERT        12.16     14.90       18.07 19.06 17.65 25.16        17.83
        DOBF              -          -          -      18.24 19.05      -      -
        PLBART          14.11     15.56       18.91 19.30 18.45 23.58        18.32
        CoTexT          14.02     14.96       18.86 19.73 19.06 24.58        18.55
        CodeT5-small 14.87        15.32       19.25 20.04 19.92 25.46        19.14
        CodeT5-base     15.24     16.16       19.56 20.01 20.31 26.03        19.55
        CodeT5-large 15.58        16.17       19.69 20.57 20.74 26.49        19.87


                     Table 8: Text-to-Code generation results on CodeXGLUE
                       Model                 EM     BLEU-4 CodeBLEU
                       GPT-2                17.35     25.37        29.69
                       CodeGPT-2            18.25     28.69        32.71
                       CodeGPT-adapted 20.10          32.79        35.98
                       PLBART               18.75     36.69        38.52
                       CoTexT               20.10     37.40        40.14
                       UniXcoder            22.60     38.23          -
                       CodeT5-small         21.55     38.13        41.39
                       CodeT5-base          22.30     40.73        43.20
                       CodeT5-large         22.65     42.66        45.08

                     Table 9: Code-to-Code generation results on CodeXGLUE
                          Java to C#          C# to Java         Refine Small       Refine Medium
  Model
                       BLEU-4      EM      BLEU-4      EM      BLEU-4     EM        BLEU-4    EM
  Naive copy            18.54      0.00     18.69      0.00     78.06     0.00       90.91    0.00
  Roborta (code)        77.46     56.10     71.99     57.90     77.30    15.90       90.07    4.10
  CodeBERT              79.92     59.00     72.14     58.00     77.42    16.40       91.07    5.20
  GraphCodeBERT         80.58     59.40     72.64     58.80     80.02    17.30       91.31    9.10
  PLBART                83.02     64.60     78.35     65.00     77.02    19.21       88.50    8.98
  CoTexT                   -         -        -          -      77.79    21.03       88.40   13.11
  NSEdit                   -         -        -          -      71.06    24.04       85.72   13.87
  CodeT5-small          82.98     64.10     79.10     65.60     76.23    19.06       89.20   10.92
  CodeT5-base           84.03     65.90     79.87     66.90     77.43    21.61       87.64   13.96
  CodeT5-large          83.56     66.00     79.77     67.00     77.38    21.70       89.22   14.76



B.2   MBPP Benchmark Results

Following Austin et al. [2021], we adopt temperature sampling to generate multiple candidate
solutions. We empirically find that CodeT5 benefits from a higher temperature of 1.2 (less greedy
decoding or more diverse) than their GPT’s temperature of 0.5 on this benchmark.
Table 10 reports the pass@80 and pass@1000 results for both finetuned and zero-shot settings. For
baselines, we compared with GPT models with sizes ranging from 224M to 137B [Austin et al.,
2021], which are pretrained on 2.93B web documents (13.8M containing source code) using standard
language modeling objective. Results of GPT models are obtained from the original authors. From
the comparison among various CodeT5 variants, we again confirm that larger model sizes and
pretraining data, and better pretraining objective of NTP all lead to a performance boost. Particularly,
our CodeT5-770M yields a pass@80 of 46.8%, surpassing GPT-8B’s 40.6% with a much smaller
model size. In addition, we find CodeT5 models finetuned on APPS can achieve a surprisingly good
zero-shot performance on MBPP with a pass@80 of 60.2% and further improved to 63.0% with
the help of CodeRL, which even outperforms the largest GPT-137B’s performance of 61.4%. This
indicates APPS is a comprehensive program synthesis benchmark and CodeT5+CodeRL models
trained on it are able to generalize to other simpler coding tasks. If we further increase the budget of


                                                  26
Table 10: Ablation results of CodeRL with different CodeT5 model variants with different sizes,
pretraining data and objectives on MBPP. CodeT5† is finetuned on APPS and evaluated on MBPP in
a zero-shot setting.
                 Model       Size     Data     Objective pass@80 pass@1000
                                      GPT finetuned results
                  GPT       224M Web Doc          LM           7.2          -
                  GPT       422M Web Doc          LM          12.6          -
                  GPT         1B    Web Doc       LM          22.4          -
                  GPT         4B    Web Doc       LM          33.0          -
                  GPT         8B    Web Doc       LM          40.6          -
                  GPT        68B    Web Doc       LM          53.6          -
                  GPT       137B Web Doc          LM          61.4          -
                                     CodeT5 finetuned results
                CodeT5       60M      CSN        MSP          19.2        36.2
                CodeT5      220M      CSN        MSP          24.0        42.8
                CodeT5      770M      CSN        MSP          32.4        47.8
                CodeT5      770M +GCPY           MSP          34.6        51.6
                CodeT5      770M +GCPY          +NTP          46.8        66.2
                                     CodeRL zero-shot results
               CodeT5† 770M +GCPY                +NTP         60.2        78.4
               +CodeRL 770M +GCPY               +NTP          63.0        81.8


attempts up to 1000, all models witness a consistent and significant boost in solving rate, especially
our CodeT5+CodeRL yielding a new SOTA result of 81.8% pass@1000.

C     Additional Qualitative Analysis
C.1   Failure Analysis

Using a CodeT5+CodeRL model, we generate 200 programs per sample in the APPS test splits. We
pass each program to the corresponding hidden unit tests. We filter for samples with either runtime
or compiling errors and extract the error types from the compiler. From Figure 10-left, (and error
definitions in Table 11), we observe that current models are able to probably indent lines of code, with
only 4% problems related to wrong tab tokens and 5% with wrong indentation levels. The majority
of mistakes are syntactical problems, assuming more than 90% of compiling errors.
From Figure 10-right, among runtime errors, the most popular types of errors are due to wrong data
index processing, inappropriate values, or mismatched data types. We found that many of these
problems occur during preprocessing of test inputs, suggesting potential ways to improve current
models in understanding and constructing proper input variables.

C.2   Example Generated Programs

We present additional example generated programs in Figure 11 to 15. Specifically, we demonstrate
cases where CodeRL+CodeT5 can successfully generate correct programs without the CS generation
procedure (Figure 11), with CS via program refining (Figure 12 and 13) and with CS via program
repairing then refining (Figure 14). In Figure 15, we demonstrate a failure case in which the final
program still fails hidden tests. This failure example shows an opposite model behavior to the example
in Figure 9, in which the CS generation procedure can successfully improve the efficiency of the
output program to pass difficult test cases. As can be seen, compared to the ground-truth program,
the output programs in Figure 15 requires a lot more drastic modifications and it would be harder for
the current CodeRL model to refine/regenerate the code.




                                                  27
Figure 10: Compiling Errors (Left): While current models are likely to generate programs with
correct indentations, there are still more than 90% of compiling errors due to syntactical mistakes.
Runtime Errors (Right): Major runtime errors include indexerror, valueerror, and typerror. Many
of these errors occur due to mistakes in processing test inputs, e.g. wrong data types or mismatched
numbers of elements. Refer to Table 11 for definitions of error types.




Table 11: Definitions of error types: Error definitions are extracted from official Python online
documentation at https://docs.python.org/3/tutorial/errors.html.
   Error Type                                               Description
   Compiling Errors
   taberror               Raised when indentation contains an inconsistent use of tabs and spaces. This
                          is a subclass of IndentationError.
   indentationerror       Base class for syntax errors related to incorrect indentation. This is a subclass
                          of SyntaxError.
   syntaxerror            Raised when the parser encounters a syntax error. This may occur in an import
                          statement, in a call to the built-in functions compile(), exec(), or eval().
   Runtime Errors
   attributeerror         Raised when an attribute reference or assignment fails.
   keyerror               Raised when a mapping (dictionary) key is not found in the set of existing
                          keys.
   zerodivisionerror      Raised when the second argument of a division or modulo operation is zero.
   unboundlocalerror      Raised when a reference is made to a local variable in a function or method,
                          but no value has been bound to that variable.
   timeoutexception       Raised when a system function timed out at the system level.
   nameerror              Raised when a local or global name is not found.
   eoferror               Raised when the input() function hits an end-of-file condition (EOF) without
                          reading any data.
   typeerror              Raised when an operation or function is applied to an object of inappropriate
                          type.
   valueerror             Raised when an operation or function receives an argument that has the right
                          type but an inappropriate value.
   indexerror             Raised when a sequence subscript is out of range.




                                                   28
                              Input Problem                                             Example Unit Tests                Hidden Unit Tests
                                                                                 Input:                         Input:
                                                                                 6 2                            6 29
 QUESTION:                                                                       1 0 1 1 1 1                    1 1 1 1 1 1
 After seeing the "ALL YOUR BASE ARE BELONG TO US" meme for                      2 10                           10 21
 the first time, numbers X and Y realised that they have different bases,        4 7                            1 1 1 1 1 1 1 1 1 1
 which complicated their relations.                                              Output: =
                                                                                                                Output:   <
 You're given a number X represented in base b_{x} and a number Y                ...                            ...
 represented in base b_{y}. Compare those two numbers.
                                                                                       Ground-truth Program          CodeT5 Output Program
 -----Input-----

 The first line of the input contains two space-separated integers n and
 b_{x} (1 ≤ n ≤ 10, 2 ≤ b_{x} ≤ 40), where n is the number of digits in the
 b_{x}-based representation of X.

 The second line contains n space-separated integers x_1, x_2, ...,
 x_{n} (0 ≤ x_{i} < b_{x}) — the digits of X. They are given in the order
 from the most significant digit to the least significant one.

 The following two lines describe Y in the same way: the third line
 contains two space-separated integers m and b_{y} (1 ≤ m ≤ 10, 2 ≤
 b_{y} ≤ 40, b_{x} ≠ b_{y}), where m is the number of digits in the
 b_{y}-based representation of Y, and the fourth line contains m                       Example tests: Passed          Example tests: Failed
 space-separated integers y_1, y_2, ..., y_{m} (0 ≤ y_{i} < b_{y}) — the                Hidden tests: Passed           Hidden tests: Failed
 digits of Y.
                                                                                 CodeRL+CodeT5 Output Program   CodeRL+CodeT5 Output Program
 There will be no leading zeroes. Both X and Y will be positive. All digits              (before CS)                     (after CS)
 of both numbers are given in the standard decimal numeral system.


 -----Output-----

 Output a single character (quotes for clarity): '<' if X < Y '>' if X > Y '='
 if X = Y


 -----Examples-----
 <Examples are not shown here just for illustration purpose>

 Use Standard Input format
 ANSWER:
                                                                                       Example tests: Passed         Example tests: Passed
                                                                                        Hidden tests: Passed          Hidden tests: Passed


Figure 11: An example synthesis task from the APPS benchmark and corresponding programs
generated by CodeT5 variants: CodeRL+CodeT5 model can generate programs that pass both
example tests and hidden tests, with or without the CS generation procedure.
                                                                                                                                               FAILED
                                                                                                                                               TESTS




                                                                                   29
                           Input Problem                              Example Unit Tests         Hidden Unit Tests
                                                                                              Input:    5 12 13
                                                                                              Output:   30
                                                                     Input:    3 4 5
                                                                     Output:   6              Input:    24 7 25
                                                                                              Output:   84
  QUESTION:                                                                                   ...
  There is a right triangle ABC with ∠ABC=90°.
  Given the lengths of the three sides, |AB|,|BC| and |CA|,
                                                                                   Ground-truth Program
  find the area of the right triangle ABC.
  It is guaranteed that the area of the triangle ABC is an
  integer.
                                                                                                                       FAILED
                                                                                                                       TESTS
  -----Constraints-----
   - 1 \leq |AB|,|BC|,|CA| \leq 100
   - All values in input are integers.
                                                                                  CodeT5 Output Program
   - The area of the triangle ABC is an integer.

  -----Input-----                                                                                                    FAILED
  Input is given from Standard Input in the following format:                                                        TESTS
  |AB| |BC| |CA|
                                                                                   Example tests: Failed
  -----Output-----                                                                  Hidden tests: Failed
  Print the area of the triangle ABC.
                                                                       CodeRL+CodeT5 Output Program (before CS)
  -----Sample Input-----                                                                                             PASSED
  345                                                                                                                 TESTS

  -----Sample Output-----
  6                                                                                Example tests: Passed
                                                                                    Hidden tests: Failed

  This triangle has an area of 6.                                       CodeRL+CodeT5 Output Program (after CS)
  Use Standard Input format

  ANSWER:


                                                                                   Example tests: Passed
                                                                                    Hidden tests: Passed

Figure 12: An example synthesis task from the APPS benchmark and corresponding programs
generated by CodeT5 variants: Without the CS generation procedure, CodeRL+CodeT5 model can
generate programs that pass all example tests but fail hidden tests. With the CS generation procedure,
the model can condition on prior programs and generate a better program that passes all hidden tests.




                                                                30
                       Input Problem                                    Example Unit Tests                 Hidden Unit Tests
                                                                  Input:    125                  Input:    74
 QUESTION:                                                        Output:   3                    Output:   8
 Allen has a LOT of money. He has $n$ dollars in the bank.
 For security reasons, he wants to withdraw it in cash (we        Input:    43                   Input:    82655
 will not disclose the reasons here). The denominations for       Output:   5                    Output:   830
 dollar bills are $1$, $5$, $10$, $20$, $100$. What is the        ...                            ...
 minimum number of bills Allen could receive after
 withdrawing his entire balance?                                       Ground-truth Program          CodeT5 Output Program

 -----Input-----

 The first and only line of input contains a single integer $n$
 ($1 \le n \le 10^9$).
                                                                                                                                            FAILED
                                                                                                                                            TESTS
 -----Output-----

 Output the minimum number of bills that Allen could
 receive.


 -----Examples-----
 Input
 125
                                                                       Example tests: Passed           Example tests: Failed
                                                                        Hidden tests: Passed            Hidden tests: Failed
 Output
 3                                                                CodeRL+CodeT5 Output Program   CodeRL+CodeT5 Output Program
                                                                          (before CS)                     (after CS)
 Input
 43

 Output
 5                                                                                                                                       FAILED
                                                                                                                                         TESTS
 Input
 1000000000

 Output
 10000000



 -----Note-----

 In the first sample case, Allen can withdraw this with a
 $100$ dollar bill, a $20$ dollar bill, and a $5$ dollar bill.
 There is no way for Allen to receive $125$ dollars in one or
 two bills.

 In the second sample case, Allen can withdraw two $20$
 dollar bills and three $1$ dollar bills.
                                                                                                                                PASSED
 In the third sample case, Allen can withdraw $100000000$                                                                        TESTS
 (ten million!) $100$ dollar bills.
 Use Standard Input format
                                                                       Example tests: Passed          Example tests: Passed
 ANSWER:                                                                Hidden tests: Failed           Hidden tests: Passed


Figure 13: An example synthesis task from the APPS benchmark and corresponding programs
generated by CodeT5 variants: Without the CS generation procedure, CodeRL+CodeT5 model
can generate programs that pass all example tests but fail hidden tests, especially those of corner
cases. With the CS generation procedure, the model can condition on prior programs and refine the
code. Specifically, we observe the model can simply reorder the elif blocks between line 11 and
15 to fix the error. The resulting program is functionally correct and passes all hidden tests.




                                                                        31
                         Input Problem                                      Example Unit Tests                    Hidden Unit Tests
                                                                      Input:    bearbtear
                                                                      Output:   6                    Input:    pbearbearhbearzqbearjkterasjhy
                                                                                                     Output:   291
 QUESTION:                                                            Input:    bearaabearc
 The bear has a string s = s_1s_2... s_{|}s| (record |s| is the       Output:   20                   ...
 string's length), consisting of lowercase English letters. The       ...
 bear wants to count the number of such pairs of indices i, j
 (1 ≤ i ≤ j ≤ |s|), that string x(i, j) = s_{i}s_{i} + 1... s_{j}
                                                                           Ground-truth Program                CodeT5 Output Program
 contains at least one string "bear" as a substring.

 String x(i, j) contains string "bear", if there is such index k (i
 ≤ k ≤ j - 3), that s_{k} = b, s_{k} + 1 = e, s_{k} + 2 = a, s_{k}
 + 3 = r.

 Help the bear cope with the given problem.                                                                                                                 FAILED
                                                                                                                                                            TESTS

 -----Input-----

 The first line contains a non-empty string s (1 ≤ |s| ≤ 5000).
 It is guaranteed that the string only consists of lowercase
 English letters.


 -----Output-----
                                                                           Example tests: Passed                Example tests: Failed
                                                                            Hidden tests: Passed                 Hidden tests: Failed
 Print a single number — the answer to the problem.
                                                                      CodeRL+CodeT5 Output Program    CodeRL+CodeT5 Output Program (after
 -----Examples-----                                                           (before CS)                           CS)
 <Examples are not shown here just for illustration purpose>

 -----Note-----
                                                                                                                                                         FAILED
 In the first sample, the following pairs (i, j) match: (1, 4), (1,                                                                                      TESTS
 5), (1, 6), (1, 7), (1, 8), (1, 9).

 In the second sample, the following pairs (i, j) match: (1, 4),
 (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (2,
 10), (2, 11), (3, 10), (3, 11), (4, 10), (4, 11), (5, 10), (5,
 11), (6, 10), (6, 11), (7, 10), (7, 11).
 Use Standard Input format
 ANSWER:
                                                                            Example tests: Failed              Example tests: Passed
                                                                             Hidden tests: Failed               Hidden tests: Passed


Figure 14: An example synthesis task from the APPS benchmark and corresponding programs
generated by CodeT5 variants: Without the CS generation procedure, CodeRL+CodeT5 model
generates programs that fail example tests. This scenario will trigger the CS generation procedure                                              PASSED
to firstly repair then refine the programs. The resulting program can pass all hidden tests and fully                                            TESTS

satisfy the problem specification.




                                                                                 32
                        Input Problem                                           Example Unit Tests                         Hidden Unit Tests
                                                                   Input:    5 2 3 12 15                      Input:    500 8 4 4 5
                                                                                                                                                         FAILED
                                                                   Output:   39                               Output:   625
                                                                                                                                                         TESTS
 QUESTION:
 Little Joty has got a task to do. She has a line of n tiles       Input:    20 2 3 3 5                       Input:    100000 3 9 1 2
 indexed from 1 to n. She has to paint them in a strange           Output:   51                               Output:   44444
 pattern.                                                          ...                                        ...

 An unpainted tile should be painted Red if it's index is                      Ground-truth Program                     CodeT5 Output Program
 divisible by a and an unpainted tile should be painted Blue
 if it's index is divisible by b. So the tile with the number
 divisible by a and b can be either painted Red or Blue.

 After her painting is done, she will get p chocolates for each
 tile that is painted Red and q chocolates for each tile that is
 painted Blue.

 Note that she can paint tiles in any order she wants.

 Given the required information, find the maximum number
 of chocolates Joty can get.


 -----Input-----                                                               Example tests: Passed                     Example tests: Failed
                                                                                Hidden tests: Passed                      Hidden tests: Failed
 The only line contains five integers n, a, b, p and q (1 ≤ n,
 a, b, p, q ≤ 10^9).

                                                                   CodeRL+CodeT5 Output Program (before CS)   CodeRL+CodeT5 Output Program (after CS)
 -----Output-----

 Print the only integer s — the maximum number of
 chocolates Joty can get.
                                                                                                                                                        FAILED
 Note that the answer can be too large, so you should use                                                                                               TESTS
 64-bit integer type to store it. In C++ you can use the long
 long integer type and in Java you can use long integer type.


 -----Examples-----
 <Examples are not shown here just for illustration purpose>

 Use Standard Input format
 ANSWER:
                                                                              Example tests: Passed                    Example tests: Passed
                                                                       Hidden tests: RuntimeError (TimeOut)     Hidden tests: RuntimeError (TimeOut)


Figure 15: An example synthesis task from the APPS benchmark and corresponding programs                                                                 PASSED
                                                                                                                                                         TESTS
generated by CodeT5 variants: We demonstrate a failure case in which CodeRL+CodeT5 model
generates incorrect programs, even with the application of the CS generation procedure. Compared
to CodeT5 model, applying CodeRL can improve the correctness of the programs but still fail during
execution due to timeout errors. The final program (after being refined by CS) still suffers from the
same error and fails to pass hidden tests.




                                                                                    33
