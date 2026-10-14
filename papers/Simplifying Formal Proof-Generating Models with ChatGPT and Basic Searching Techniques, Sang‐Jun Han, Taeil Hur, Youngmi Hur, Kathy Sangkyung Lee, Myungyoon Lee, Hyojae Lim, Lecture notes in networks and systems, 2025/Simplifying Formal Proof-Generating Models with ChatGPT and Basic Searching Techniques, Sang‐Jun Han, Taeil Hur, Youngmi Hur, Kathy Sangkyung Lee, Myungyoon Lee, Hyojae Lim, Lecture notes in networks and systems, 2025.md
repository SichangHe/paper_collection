                                           Simplifying Formal Proof-Generating Models
                                          with ChatGPT and Basic Searching Techniques

                                              Sangjun Han1 , Taeil Hur2 , Youngmi Hur1,3 , Kathy Sangkyung Lee1 ,
                                                              Myungyoon Lee1 , and Hyojae Lim4
                                                               1
                                                                Yonsei University, Seoul, South Korea
arXiv:2502.03321v3 [cs.LO] 19 Feb 2025




                                                         {qkqhwl4,yhur,kathy,yooni7272}@yonsei.ac.kr
                                                                 2
                                                                    JENTI Inc., Seoul, South Korea
                                                                        taeil.hur@jenti.ai
                                                    3
                                                      Korea Institute for Advanced Study, Seoul, South Korea
                                         4
                                           Johann Radon Institute for Computational and Applied Mathematics, Linz, Austria
                                                                      hyojae.lim@oeaw.ac.at



                                               Abstract. The challenge of formal proof generation has a rich history,
                                               but with modern techniques, we may finally be at the stage of making
                                               actual progress in real-life mathematical problems. This paper explores
                                               the integration of ChatGPT and basic searching techniques to simplify
                                               generating formal proofs, with a particular focus on the miniF2F dataset.
                                               We demonstrate how combining a large language model like ChatGPT
                                               with a formal language such as Lean, which has the added advantage
                                               of being verifiable, enhances the efficiency and accessibility of formal
                                               proof generation. Despite its simplicity, our best-performing Lean-based
                                               model surpasses all known benchmarks with a 31.15% pass rate. We ex-
                                               tend our experiments to include other datasets and employ alternative
                                               language models, showcasing our models’ comparable performance in di-
                                               verse settings and allowing for a more nuanced analysis of our results.
                                               Our findings offer insights into AI-assisted formal proof generation, sug-
                                               gesting a promising direction for future research in formal mathematical
                                               proof.

                                               Keywords: Mathematical reasoning, Formal proof generation, Proof
                                               search, Large language model


                                         1   Introduction

                                         Writing mathematical proofs in formal language has been a research topic for
                                         many years. Notably, we recall McCarthy’s symbolic computation on machines
                                         [18], Hoare’s axiomatic approach to computer programming [13], and DeMillo,
                                         Lipton, and Perlis’s skepticism towards formal proofs of theorems [8]. Due to the
                                         surprising performance of AI algorithms witnessed over the last decade, such as
                                         transformers in natural language processing, we believe it is an opportune time
                                         to revisit the formal proof challenge with the modern techniques available. As
                                         evidenced by our literature review below, we are not alone in this pursuit.
2       S. Han et al.

    Our primary interest lies in writing ordinary, workaday mathematical proofs
in formal language and, conversely, in using these formal proofs to enhance our
everyday mathematical reasoning. With this ultimate goal in mind, we have
made progress, albeit slowly, in understanding this issue over the past few years.
In this paper, we aim to share some of the insights and experiences we have
gained, hoping to contribute to the broader research community’s understanding
of future directions to explore in tackling this complex problem.
    We utilize ChatGPT (GPT-4 and GPT-4 Turbo) together with Lean for
a set of experiments, primarily focusing on the miniF2F dataset [33], a stan-
dard dataset in formal proof research. Our models achieve surprisingly compe-
tent performance for their simplicity, notably our best-performing model, which
surpasses most known benchmarks with a 31.15% pass rate. We evaluate our
approach on other datasets to ensure similar effectiveness across various mathe-
matical domains and previously unpublished problems. We also study our search
algorithms under another language model, Llemma, displaying the versatility of
our approach.
    The outline of the rest of this paper is as follows. The rest of Section 1 broadly
discusses the previous work related to our research. In Section 2, we cover some
preliminary background material that would be helpful in understanding our
work, which includes Lean, miniF2F, and proof search algorithms. We explain the
characteristics of our models in Section 3, and Section 4 details our experiments.
We analyze the results of our models with specific examples in Section 5, and
present our conclusion and overview in Section 6.


1.1   Related Work

Mathematical theorem proving in machine learning has garnered significant at-
tention, particularly for developing artificial intelligence capable of logical rea-
soning. As a result, various studies have been conducted, with those most closely
related to our work outlined below.


Formal and informal languages Languages used for the integration of ma-
chine learning with mathematical reasoning can be broadly categorized as either
formal or informal. Informal language has a format that is familiar to the human
eye and is thus easily understood and used. The authors in [7] propose a machine
learning-based framework and leverage informal language to offer mathematical
insight, and the models in [10, 28] are fine-tuned to prove mathematical theorems
in informal language. However, informal language proofs have the disadvantage
of being difficult to verify. To address this issue, many studies have utilized ver-
ifiable programming languages, spanning across formal languages such as Lean
[2, 11, 20, 32], Metamath [21], HOL4 [29], Isabelle [14, 15, 27], Coq [31], Python
[5], or a mix of these environments [16, 23]. These formal languages can represent
mathematical ideas precisely, making them easier to utilize in a computing sys-
tem. However, formal languages differ vastly from the mathematical arguments
written by humans, making it difficult to interpret without ample understanding
             Simplifying Proof Generation with ChatGPT and Basic Search          3

of the formal setting used. Given that we consider the verifiability of proofs to
be essential, we choose to work with formal language to construct the models in
our study, despite its lower accessibility.



Large language models with theorem proving Large language models
(LLMs) have become increasingly useful in natural language processing [1, 4,
5, 6, 24], inspiring many studies on these models. The researchers from [9] use
Codex to find solutions for informal language problems by converting the prob-
lems into programming tasks, while the authors of [23] improve their model’s
performance by composing effective prompts for ChatGPT. Many also create
new models based on LLMs, such as Llemma [3], which achieves high perfor-
mance in mathematical proof generation by fine-tuning LLaMA [24] on newly
proposed data. Others, as those in [15, 27], link together LLMs and theorem
proving by writing formal proofs informed by the informal proofs generated for
a mathematical problem. In this paper, we aim to construct a simple and easily
reproducible model that can be tried by anyone. To this end, we utilize Chat-
GPT and enhance its performance by modifying existing proof search algorithms
specifically tailored for this LLM.



Development of proof search algorithms There have been various efforts
towards developing formal language models. Among these, there are many mod-
els that have modified the proof search algorithm in innovative ways, often dis-
playing strong performances. A pioneer in this endeavor is GPT-f [21], which
introduced the proof search process and evaluation criteria for the field. Some
models rely on extra training, such as expert iteration in [20] to tackle problems
of increasing difficulty and control the lengths of formal proofs, or reinforcement
learning in [29]. Other models focus on premise selection to call relevant theorems
or other mathematical statements. For example, Thor [14] utilizes Hammer to
aid the proof search process by choosing appropriate premises in interactive the-
orem provers, and LeanDojo [32] and DS-Prover [26] integrate models dedicated
to this task.
    Some of the leading models have displayed impressive prowess in proof gen-
eration, such as the HyperTree proof search [16], a new method related to the
Monte Carlo tree search which uses online training to achieve the highest per-
formance in the field. Also, AlphaGeometry [25] has recently demonstrated ex-
ceptional performance in the field of geometry proof search by combining a
symbolic deduction engine, a type of computer program, with language models
fine-tuned on more than 100 million geometry problems. We aim to preserve
the overall structure of the existing proof search process, but make adaptations
to the proof search algorithm to explore a wider range of proofs. Additionally,
we make our adjustments to enhance performance based on ChatGPT’s specific
parameters, bypassing the challenges that existing algorithms face when used
with ChatGPT.
4      S. Han et al.

2     Background
2.1   Lean
Lean is an interactive theorem prover based on dependent type theory, and allows
us to use mathematical objects such as definitions, theorems, and lemmas [19].
Lean utilizes tactic expressions, as do some other formal languages, which can
be helpful in writing proofs. For example, have is a tactic that can create a
new subgoal to act as a stepping stone in a theorem’s proof, enabling users
to construct a forward proof. Lean is popular in the mathematical community,
serving as a base for active projects such as the Aesop and the Liquid Tensor
experiments [17, 22]. Furthermore, there is a massive library called mathlib in
Lean, which covers various mathematical topics. Considering the above aspects,
we selected Lean as a proof assistant for our experiments. Our main experiment
utilizes the GPT-4 Turbo model of ChatGPT. This model generates proofs using
Lean 3 syntax by default, and considering its pre-training period, it is unfamiliar
with Lean 4. Therefore, we conducted all our experiments using Lean 3, with the
exception of our further analysis involving Llemma, for which we used Lean 4,
following the methodology outlined in the existing Llemma paper.

2.2   MiniF2F
The dataset miniF2F [33] is a cross-system benchmark for formal mathemat-
ical proof, formalized in the formal languages Lean, Metamath, and Isabelle.
MiniF2F consists of problems selected from the MATH dataset [12]; Olympiad-
level problems, chosen from past AIME, AMC, and IMO questions; and CUS-
TOM problems, derived from topics in algebra, number theory and induction.
The MATH dataset is divided into 5 levels of difficulty: problems in levels 1 to 3
require only simple calculations and straightforward approaches, while questions
in levels 4 to 5 have more complex solutions. The Olympiad and CUSTOM prob-
lems in miniF2F range from high school-level to undergraduate-level mathemat-
ics. In general, solving the problems in these two categories necessitates more
logical reasoning or stepwise proofs, sometimes by introducing premises to aid
the proof.

2.3   Proof Search Algorithm
In [11, 23, 32], the general proof search process of the proof-generating model
via Lean is as follows:
(1) The model takes a tactic state which includes the hypotheses and goals in
    the current stage.
(2) The model generates n many tactics to advance to the next goal or to gen-
    erate new hypotheses.
(3) Each generated tactic is sent to Lean to obtain new goals or hypotheses,
    updating the tactic state. (We henceforth refer to this step as interaction
    with Lean.)
               Simplifying Proof Generation with ChatGPT and Basic Search           5

(4) Repeat steps (1)-(3) for each new tactic state.
(5) The process is terminated when (a) goals no longer appear, indicating a valid
    proof has been generated, (b) all tactics fail to update the tactic state, (c)
    the model gives up on proving, generating sorry, or (d) the time limit is
    reached.

    Our proof search algorithm also follows the above process; the details are
given in the following section.


3     Characteristics of Our Model

Often, a pre-trained model is fine-tuned on newly constructed data to create a
model tailored for a specific task. However, the process of constructing a proper
dataset itself is demanding. Even if the data is well-structured, fine-tuned mod-
els frequently exhibit suboptimal performance on out-of-distribution data (e.g.,
[11, 32]). Thus, we choose to employ ChatGPT without any additional fine-
tuning, which relieves the burden of further training. Additionally, our exper-
iments primarily utilize ChatGPT with prompt messages containing just two
simple guidelines, while COPRA [23] generates the desired output through rel-
atively complex prompt messages.
     The development of the existing models can be broadly divided into three
approaches: (i) creating new training data or improving existing data [11, 26, 32],
(ii) conducting additional training after fine-tuning [16, 20, 29], or (iii) introduc-
ing appropriate proof search algorithms [9, 14, 15, 23]. We choose to focus on the
last method to improve performance, and as such, modify the existing algorithms
to suit our purposes. We design two types of proof search algorithms following a
similar process as in Section 2.3 - one with the properties of a breadth-first search,
which we call the b-search, and the other with the properties of a depth-first
search, which we call the d-search. While the b-search requires more requests to
ChatGPT and more memory, it generally achieves greater performance. In con-
trast, the d-search usually has lower performance but requires fewer resources.
We anticipate that the combination of these two types of searches with Chat-
GPT will lead to the exploration of a wider range of tactics. The details of our
modified proof search algorithms are explained below.
     The b-search follows closely with the search process outlined in Section 2.3,
with the number of generated tactics set to 64 through the ChatGPT hyperpa-
rameter “n” in API reference5 . This method resembles the beam search-based
proof search in ReProver [32] and Llemma [3]. However, instead of looking at
n many tactics through beam search as ReProver and Llemma do, the b-search
generates tactics that have a very high probability of correctly continuing the
proof but are likely to be redundant. This slows down the model, so we per-
form an additional step after step (2) in Section 2.3 to eliminate the doubles
by deduplicating the generated tactics for each tactic state. We also regulate
5
    https://platform.openai.com/docs/api-reference/chat/create#chat-create-n
6       S. Han et al.

the diversity of the generated tactics in the b-search by temperature, another
ChatGPT hyperparameter.
    In the d-search, a single tactic (n=1) with the highest probability of success is
generated at each step of the proof (i.e., a greedy search base). After interaction
with Lean, if the tactic fails, the search returns to the initial state and reattempts
a proof of the theorem. Generating all the proof steps correctly from the initial
state while generating only one tactic at a time is challenging, so we alter the
number of attempts (later parameterized with k) to generate the proof. Although
the d-search is taxing, as it involves restarting from the initial state rather than
from the state that failed, we find that it can explore possible tactics more
extensively through its consideration of tactics from previous steps. Furthermore,
since this method revisits a single problem multiple times, it is suitable to apply
the feedback algorithm with the so-called “Bad(O)”, as proposed in COPRA [23].
    Bad(O) refers to the set of tactics that are unproductive or erroneous within a
specific proof state. This set ensures that, when COPRA encounters the current
proof state again, it avoids generating these unsuccessful tactics. This concept
helps to avoid repeating the same mistakes by recording these failed tactics, thus
leading to progress in the proof generation process. In contrast to COPRA, our
d-search restarts the entire proof from the initial stage, even in cases where it fails
at a later stage. Therefore, we modify the original Bad(O) feedback algorithm to
complement our proof search by storing the tactic states along with their failed
tactics in Bad(O), instead of just the failed tactics. Then, when the proof is
restarted, the tactic state is checked against those in Bad(O) to avoid repeating
past failures if a match is found. We walk through the steps for d-search with
Bad(O) in a specific example in Section 5.


4     Experiments

In this section, we present the various experiments we conducted by employing
ChatGPT, which is easily accessible to the general public, to achieve performance
comparable to current models. By applying our search algorithms, we attain
slightly higher performance than that of the COPRA models. Additionally, we
include the results of the ReProver and COPRA models for a comprehensive
comparison with our output.


4.1   Experimental Setup

We classify our models based on the methods used in their proof search processes,
as follows:

 1. bChatLean, based on b-search, and
 2. dChatLean, based on d-search.

We incorporate a feedback algorithm using Bad(O), as discussed in Section 3,
into the dChatLean model to get a new model, which we refer to as dChatLean+.
               Simplifying Proof Generation with ChatGPT and Basic Search        7

Additionally, we experiment with a combination of the bChatLean, dChatLean,
and dChatLean+ models.
    These models use ChatGPT with either GPT-4-0613 (GPT-4) or GPT-4-
1106-preview (GPT-4 Turbo) as a baseline. Our implementation involves 5-shot
tests, using 5 examples extracted from the miniF2F validation data. To guide
ChatGPT toward proper tactic creation, we present the following prompt mes-
sage:

   Make a proof statement in Lean3 to prove theorem using the following
guidelines:

      - Generate only the single line of proof that immediately follows.
      - Do not use ‘sorry’.

    Our models are significantly influenced by the diversity of output from Chat-
GPT, which is affected by the temperature setting. In our experiments, we ex-
plore two temperature values: 0.7 and 1.4. As for other hyperparameters, in
bChatLean, we fix the number of tactic samplings n in a single step to 64, and
in dChatLean, we investigate the effect of varying the number of attempts k to
solve one theorem, comparing results at values of 1, 10, and 50.
    To interact with Lean, we utilize LeanDojo [32], which allows parallel im-
plementation, easily checks time limits, and is well-organized. The time limit
to prove one theorem is set to 600 seconds, consistent with other papers. All
experiments in this section are conducted in parallel on the CPU. The source
code for our algorithms and experiments discussed in this paper is available on
GitHub6 .


4.2     Main Result

Our results are presented in Table 1. The results of our models shown in this table
are all obtained using GPT-4 Turbo with a temperature setting of T = 1.4. We
display the pass@k rate of each model as presented in each paper for the miniF2F
Lean test dataset. The pass@k rate, the most widely used metric for evaluating
proof-generating models, represents the proportion of completed proofs over the
entire dataset, where k denotes the number of attempts to generate a proof made
on each problem. We employ specific terminology in our table for simplification.

    - # of Att. (k): The number of attempts k to prove a problem, the same k as
      in a pass@k rate.
    - # of Tactics (n): The number of tactic samples n a model generates upon
      receiving one tactic state. It is similar in notion to the number of beams in
      a typical beam search.

6
    https://github.com/chatlean
8          S. Han et al.

                      Table 1. Pass@k rates on the miniF2F test dataset

                                                      # of       # of          Sample
              Model                   Baseline                                              Pass@k
                                                     Att. (k) Tactics (n)      budget

            PACT [11]             similar to GPT-3      1          8          1 × 8 × 512   24.6%
     Lean Expert iteration [20]   similar to GPT-3      1          8          1 × 8 × 512   29.6%
           ReProver [32]               ByT5             1         64          1 × 64 × −    26.5%
          DS-Prover [26]               ByT5             1         −               −         29.8%
          HyperTree [16]                               64         48          64 × 5000     41.0%
          Llemma-7b [3]           Code Llama 7b         1         32         1 × 32 × 100   26.23%
             COPRA
                                 GPT-4 T(urbo)          1          1            1 × 60      26.64%
    (GPT-4 Turbo+retrieval) [23]
        COPRA+One-Shot
        +Informal-One-Shot
                                     GPT-4 T            1          1           1 × 100      29.92%
      (GPT-4 Turbo+retrieval
       +informal proof) [23]

            bChatLean                GPT-4 T            1         64          1 × 64 × −    29.10%
            dChatLean                GPT-4 T           50          1          50 × 1 × −    23.77%
           dChatLean+                GPT-4 T           50          1          50 × 1 × −    25.00%
                                                                             (1 × 64 ×−)
     bChatLean & dChatLean+          GPT-4 T         1 & 50    64 & 1                     31.15%
                                                                            + (50 × 1 ×−)




    - Sample budget: A measure of computational complexity, generally in the
      form of k × n × e, where e denotes the number of calls to the baseline model.
      Alternative forms and a more detailed explanation are provided below.

     Current proof models use a variety of proof generation algorithms, making
it challenging to conduct a fair comparison of their computational complexities.
We thus compute the “sample budget” based on [30]. The general form for the
sample budget is k ×n×e, but in the case of HyperTree and COPRA, the sample
budget is represented as k × e. Also, in our table, “–” represents a dynamic value
that varies depending on the situation and has no fixed upper limit.
     Although our models use a dynamic value for the parameter e, as a reference,
if we retrospectively examine the experimental results and calculate the average
number of calls, this value can be compared to the e value of other models. To
give a few of the values, the average number of calls was 1.664 for bChatLean
and 1.057 for dChatLean+.
     Our dChatLean models show lower performance than the bChatLean model.
In particular, as can be seen from Table 1, the best performance for dChatLean
is lower than the 29.10% pass rate achieved by bChatLean, reaching a peak pass
rate of 25.00% through its natural synergy with Bad(O) in dChatLean+. The
lower performance from dChatLean can be attributed to the relative difficulty of
the dChatLean proof search problem, as it requires restarting from the beginning
if an intermediate step fails.
               Simplifying Proof Generation with ChatGPT and Basic Search        9

    Since the two proof searches described above use separate strategies to find
proofs, we expect that combining the two models will open up room for a wider
range of tactics to explore. Thus, we couple bChatLean with dChatLean+, both
under GPT-4 Turbo (k = 1, n = 64 for bChatLean and k = 50, n = 1 for
dChatLean+), yielding an impressive performance of 31.15%. This pass rate
surpasses all values in Table 1 except for in the case of the HyperTree model,
which uses a much larger sample budget. Out of the 244 theorems attempted, 56
were successfully solved by both of our models, 15 were only solved in bChatLean,
and 5 were only solved in dChatLean+. Furthermore, out of the proven theorems,
21 theorems have not been proved in the recent miniF2F GitHub repository7 .
    Despite the high performance ultimately obtained, there are still some lim-
itations in our models. To name one in particular, while a simplified prompt is
handy for our experiment, it occasionally fails to deliver our intention to the
model. For example, we introduce a guideline of “Generate only the single
line of proof that immediately follows” to facilitate step-by-step theo-
rem proving. Contrary to our purposes, the proof for the solved problems of-
ten manifested as a single line of output, achieved by combining various tactics
through the generous use of semicolons. Consequently, we think that our models
can report a higher pass rate if slightly more detailed instructions are given.
Many other areas can be improved, but we leave these to future works.

4.3    Ablation Studies
On the number of attempts in dChatLean Generating proofs by using
dChatLean is significantly more challenging than with other models that utilize
breadth-first search or depth-first search algorithms. One of the reasons for this
is that dChatLean restarts the proof generation from the initial state if it fails.
Additionally, any minor typos in dChatLean’s tactic generation can critically
impact the model’s pass rate. We observe that, as the number of attempts k
made on a problem increases, dChatLean’s proof generation stabilizes, directly
enhancing the overall performance of the model (see Table 2). In GPT-4 Turbo
with temperature T = 0.7, an increase of k from 10 to 50 yields a performance
increase of 6.97%. The same trend holds for GPT-4 Turbo under T = 1.4, as
the addition of attempts from 10 to 50 shows a performance rise of 8.61%.
This notable increase can be attributed to the model attempting many proof
directions by generating more diverse tactics multiple times, confirming that
increasing the number of attempts on a proof produces a higher pass rate.

On tactic diversity Since dChatLean only produces one tactic at a time, it
is important to explore multiple possibilities by generating a variety of tactics
in subsequent attempts. Additionally, since bChatLean uses ChatGPT’s n hy-
perparameter, it is necessary for the model to produce more diverse outputs
to avoid repeated attempts. In this context, temperature is a crucial parameter
that influences the model’s pass rate.
7
    GitHub repository for MiniF2F dataset
10     S. Han et al.

               Table 2. Ablation study for the number of attempts

                   Model       Baseline Temp. (T ) # of Att. (k) Pass Rate

                                                        10        13.93%
                               GPT-4 T      0.7
                                                        50        20.90%
                 dChatLean
                                                        10        15.16%
                               GPT-4 T      1.4
                                                        50        23.77%



    As shown in Table 3, in our dChatLean model, GPT-4 with k = 10 and
GPT-4 Turbo with k = 10 both reflect a performance gain of about 1.23% when
T is raised from 0.7 to 1.4. GPT-4 Turbo with k = 50 when T = 1.4 yielded
a performance increase of about 2.87% from its performance when T = 0.7.
Hence, we see that the influence of temperature changes on the pass rate is more
substantial when the number of attempts is higher, highlighting the benefits of
a wider range of attempts on performance. This tendency of achieving better
performance with higher temperature is mirrored in our bChatLean model, as
GPT-4 Turbo with T fixed at 1.4 reflects a pass rate 1.23% higher than when T
is 0.7.

                   Table 3. Ablation study for the temperature

                   Model       Baseline # of Att. (k) Temp. (T ) Pass Rate

                                                         0.7      27.87%
                 bChatLean GPT-4 T            1
                                                         1.4      29.10%
                                                         0.7      14.75%
                               GPT-4         10
                                                         1.4      15.98%
                                                         0.7      13.93%
                 dChatLean GPT-4 T           10
                                                         1.4      15.16%
                                                         0.7      20.90%
                               GPT-4 T       50
                                                         1.4      23.77%




             Table 4. Ablation for the feedback algorithm by Bad(O)

                       Model    Baseline Temp. (T ) # of Att. (k) Pass Rate

                  dChatLean                                       15.16%
                            GPT-4 T          1.4         10
                 dChatLean+                                       18.85%
                  dChatLean                                       23.77%
                            GPT-4 T          1.4         50
                 dChatLean+                                       25.00%




On the feedback algorithm in dChatLean Due to dChatLean’s character-
istic of returning to the initial state to reattempt the proof, it is natural that
              Simplifying Proof Generation with ChatGPT and Basic Search        11

some tactic states reappear during the proof search. Thus, the feedback algo-
rithm by Bad(O) plays a vital role in increasing the pass rate of the model by
avoiding previously failed tactics and instead coaxing the model to consider new
tactics. Table 4 shows the comparison between pass rates for dChatLean, which
does not use a feedback algorithm, and dChatLean+, which utilizes the feedback
algorithm with Bad(O). When the number of attempts k is 10, the inclusion of
the feedback algorithm helps dChatLean+ achieve a pass rate 3.69% higher than
that of dChatLean. Setting k to 50, dChatLean+ records a performance 1.23%
above dChatLean’s. In Section 5, we provide a specific example to illustrate the
process of generating a proof using Bad(O) in dChatLean+ (c.f. Figure 2 and
Figure 3).


4.4   Evaluation Across Datasets and LLMs

We evaluate our models on the ProofNet dataset and the 2023 AMC 12 prob-
lems to verify our models’ abilities to generate proofs for problems outside of the
scope covered by miniF2F. We also assess our algorithms using another language
model, Llemma, in place of ChatGPT. Despite the simplicity of our models, the
results demonstrate performance comparable to established benchmarks, effec-
tively addressing mathematical problems across diverse contexts and settings.


On ProofNet We used our bChatLean and dChatLean+ coupled model on
ProofNet8 , a benchmark for undergraduate-level mathematics, covering Anal-
ysis, Abstract Algebra, Linear Algebra, and Topology, as well as a topic la-
beled “Examinations” that consists of some Putnam Competition problems. The
ProofNet set is composed of 350 problems drawn from mathematics textbooks
and formalized in Lean 3. When running our model on this benchmark, we
achieve an overall performance of 13.14%, as seen in Table 5, and generate 35
new Lean proofs. The performance in Table 5 outlines the pass rate across differ-
ent mathematical topics. In particular, our model performs best with Analysis
problems, with a pass rate of 15.91%, and conversely, finds Linear Algebra and
Topology problems more challenging, with pass rates of 10.00% and 10.71%,
respectively. This domain-based comparison informs us of the specific strengths
and weaknesses within our models, providing direction for future enhancements.


On AMC 12 To conduct our evaluation, we selected problems from the 2023
AMC 12A9 and 12B10 exams, both of which make up the high school mathemat-
ics problem-solving competition that acts as a first step towards Olympiad-level
tests. These problems were published after the training for the ChatGPT version
that we use for this paper, and thus were outside of the possible scope of prob-
lems that could have slipped into the training set for the model. We formalized
8
   GitHub repository for ProofNet dataset
9
   2023 AMC 12A Problems and Solutions
10
   2023 AMC 12B Problems and Solutions
12        S. Han et al.

                          Table 5. Pass rates on ProofNet by topic

                               Topic         Theorems   Proved   Pass rate

                              Analysis          88        14     15.91%
                          Abstract Algebra     162        21     12.96%
                           Linear Algebra       28         3     10.71%
                              Topology          60         6     10.00%
                           Examinations         12         2     16.67%
                               Total           350        46     13.14%




26 problems from this competition into Lean 3 using ChatGPT, and manually
verified that the formalized problems were free of errors and retained their orig-
inal meanings11 . After running the bChatLean & dChatLean+ coupled model
on this dataset, we obtained 6 successful proofs, giving us a pass rate of 23.07%.
Although we do not have access to the data that ChatGPT was trained on, we
test our models on some newly published problems and note that we achieve a
comparable pass rate as on the miniF2F dataset. This demonstrates our models’
applicability to new problems, highlighting the potential that these models can
later have in real-world applications.


Using Llemma Though our models are based on search algorithms that specif-
ically cater to ChatGPT and its properties, we verify our proof searching al-
gorithms’ capabilities with the mathematics-specialized large language model
Llemma [3]. In parallel with the ChatGPT-based models, we call the Llemma-
based models bLlemLean, dLlemLean, and dLlemLean+. These models are based
on the b-search, d-search, and the d-search with Bad(O), respectively. They con-
tinue to use Lean as their formal language, but since the established performance
of Llemma is dependent on Lean 4, we adopt Lean 4 in this experiment rather
than Lean 3. The miniF2F pass rates for these models and their combinations
are outlined in Table 6.
    Unlike with our ChatGPT models, our dLlemLean+ model performs worse
than our dLlemLean model, indicating that the d-search method suffers with the
introduction of Bad(O). We can attribute this to the fact that Bad(O) generally
makes longer prompts, which Llemma struggles with due to the far fewer pa-
rameters used in comparison to ChatGPT. However, Bad(O) has its advantages
when d-search is used together with b-search, as the bLlemLean and dLlemLean
combined model performs a little worse than the bLlemLean and dLlemLean+
combined model does. This suggests that Bad(O) still aids d-search in finding
proofs that the b-search fails to find alone.
    We achieved the highest performance of 28.28% using the combination of
bLlemLean and dLlemLean+, surpassing the benchmark of 26.23% previously
reported for Llemma. Although our proof search algorithms were specially cus-
tomized to enhance the ChatGPT output for our purposes, that the Llemma-
11
     https://github.com/chatlean/AMC12 2023 Lean
             Simplifying Proof Generation with ChatGPT and Basic Search        13

based models perform comparatively well conveys that our algorithms are robust
to language model substitutions.


                   Table 6. MiniF2F test pass rate on Llemma

                                 Model           Pass Rate

                              Llemma [3]          26.23%
                              bLlemLean       26.64%
                              dLlemLean       22.54%
                             dLlemLean+       21.31%
                        bLlemLean & dLlemLean 27.46%
                       bLlemLean & dLlemLean+ 28.28%




5   Additional Analysis with Examples
In this section, we analyze our results based on specific criteria with examples.

Considering the number of attempts in dChatLean+
In our experiments with dChatLean+, where k was set to be strictly greater
than 1, we found that for the problems solved in only one attempt, the proofs
involved either performing a simple calculation or simply solving a system of
equations, as illustrated in the left example of Figure 1. In contrast, problems
solved with more than one attempt included proofs demonstrating that given
properties hold, as shown in the right example of Figure 1. These findings suggest
that increasing the number of attempts in dChatLean+ may enable the model to
identify approaches that require additional premises beyond basic calculations.




     Fig. 1. Examples considering numbers of attempts taken by dChatLean+


   Moreover, we observe that, for the problems with successful proofs, the av-
erage number of attempts taken with dChatLean is 10.3, while just 9.3 with
14      S. Han et al.

dChatLean+. (These values are based on our observations but are not explic-
itly presented in the paper.) This indicates that the feedback algorithm using
Bad(O) guides the model to produce fewer failures when searching for a solu-
tion. Table 7 shows the number of attempts taken by both models to solve a few
problems for which they produce similar proofs.

        Table 7. Number of attempts taken by dChatLean and dChatLean+

                        Name of problem              dChatLean dChatLean+

                       mathd algebra 478                 5            2
              algebra sqineq unitcircatbpabsamblt1      12            2
                       mathd algebra 113                47           17




Considering the feedback algorithm




Fig. 2. The process of generating a proof for “mathd algebra 171” using the Bad(O)-
based feedback algorithm. The highlighted lines indicate the trials selected to be further
illustrated in Figure 3. The final proof is given in green, while other selected trials are
in blue.


    The proof generation process using the Bad(O)-based feedback algorithm in
dChatLean+ can be seen in Figure 2, where the model completed the proof
for the miniF2F problem “mathd algebra 171” in 21 attempts. The completed
proof, 21 try, begins with rw h0 , and one can note many previous failed attempts
that also started with rw h0 . These attempts were stored in Bad(O) to avoid
repeating the same failure when faced with the same tactic state. We depict a
few selected trials in Figure 3 and walk through the proof search process below.
○
1 On the sixth trial, the model reached rw h0 and simp [h0 ]. To continue
     the proof, it then generated the tactic rw [← h0 1], but resulted in failure.
              Simplifying Proof Generation with ChatGPT and Basic Search             15




Fig. 3. Selected proof trials highlighted in blue, also displayed in Figure 2. The final
proof is highlighted in green.


  This tactic rw [← h0 1] was thus stored in Bad(O) for the model to refer
  to in any subsequent attempts to solve the same tactic state–or goal–that
  rw [← h0 1] was brought in to address.
○
2 The same tactic state appeared in trials 9 and 11, and the model avoided the
  tactics in Bad(O) to try new tactics, generating rw [← h0 1, mul one] for
  trial 9 and rw [← h0 1, mul one, add comm] for trial 11. However, these
  also resulted in failures, and these new tactics were added to Bad(O).
○
3 After this series of failures, the model decided to step out and seek a solu-
  tion for the tactic state using norm num, as seen in trial 13 with rw [← h0
  (5/5)], norm num. This also resulted in failure, adding this last tactic to
  Bad(O) as well.
○
4 The model decided to then step out of the tactic state involving simp [h0 ]
  and instead work in the tactic state resulting from rw h0 . Trials 17 and 20
  generated tactics using norm num, but resulted in failures, which were stored
  in Bad(O) under this new tactic state.
○
5 Finally, under guidance from Bad(O), the model produced a successful proof
  in trial 21. After seeing that all goals have been cleared, the proof search
  algorithm terminates and returns the successful proof.

    As demonstrated in this example, the feedback algorithm in dChatLean+
allows the model to adapt failed tactics or change the direction of the proof by
referring to previous attempts.


Considering challenging problems

Our bChatLean model solves a problem named “induction 1pxpownlt1pnx” from
the miniF2F dataset with the proof presented in Figure 4. This problem cor-
responds to Bernoulli’s inequality, which we believe is intended to be proved
16      S. Han et al.




        Fig. 4. The proof generated by bChatLean for Bernoulli’s inequality



using mathematical induction. However, the model uses the pre-defined theorem
one add mul le pow, which corresponds to Bernoulli’s inequality in the math-
lib library. While the problem was technically solved, the resulting proof may
be considered unsatisfactory. The outcome suggests that the model may have
leveraged prior exposure to the library during training, leading it to apply the
theorem directly. Conversely, we found that the ReProver model, which is prob-
ably less influenced by such prior exposure due to its smaller size, cannot prove
this problem. This raises several points for consideration: there is still a lack of
algorithms for small-scale models that address problems of this level, and even
if a problem can be solved when scaled up in size, it is important to consider
whether the solution aligns with the intended solution. Additionally, mitigating
the influence of pre-existing knowledge in large-scale models will be crucial.




6    Conclusion


In this paper, we proposed two simple proof search methods: the b-search and
the d-search. These gave rise to our bChatLean and dChatLean models, which
employ a pre-trained large language model in ChatGPT and achieve comparable
performance to that of state-of-the-art models even in the absence of fine-tuning,
as demonstrated on the miniF2F dataset. In addition, we improved the perfor-
mance of these two models by coupling bChatLean with dChatLean+, which
introduces a feedback algorithm into dChatLean. To test the capabilities of our
approach, we applied our models and proof search algorithms on other datasets,
namely ProofNet and the 2023 AMC 12, and to the other large language model,
Llemma. We analyzed our models through ablation studies on factors such as
the number of attempts, the temperature, and our feedback algorithm. More-
over, we selected examples to illustrate and scrutinize the models’ results and
presented further consideration for future research in the field of formal mathe-
matical proof.
              Simplifying Proof Generation with ChatGPT and Basic Search              17

7    Acknowledgments

T. Hur–This work was partly supported by the Institute of Information & com-
munications Technology Planning & Evaluation (IITP) grant funded by the
Korea government (MSIT) (No. RS-2023-00221236, Development of document
understanding and information extraction model using multi-modal artificial in-
telligence technology).
    Y. Hur–This work was partly supported by the National Research Foun-
dation of Korea (NRF) (Grant Number 2021R1A2C1007598), by the National
Supercomputing Center with supercomputing resources including technical sup-
port (Grant Number: KSC-2023-CRE-0087), and by the Visiting Professorship
at Korea Institute for Advanced Study.
    H. Lim–This work was partly supported by the Hausdorff Research Institute
for Mathematics (HIM) funded by the Deutsche Forschungsgemeinschaft (DFG,
German Research Foundation) under Germany’s Excellence Strategy – EXC-
2047/1 – 390685813.


References

 1. Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F.L., Almeida,
    D., Altenschmidt, J., Altman, S., Anadkat, S., et al.: GPT-4 technical report
    (2023). Eprint: arXiv:2303.08774
 2. Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E.W., Radev, D., Avigad, J.:
    ProofNet: Autoformalizing and formally proving undergraduate-level mathematics
    (2023). Eprint: arXiv:2302.12433
 3. Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M.D., McAleer, S.M., Jiang,
    A.Q., Deng, J., Biderman, S., Welleck, S.: Llemma: An open language model for
    mathematics (2023). Eprint: arXiv:2310.10631
 4. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Nee-
    lakantan, A., Shyam, P., Sastry, G., Askell, A., et al.: Language models are few-shot
    learners. In: Conference on Neural Information Processing Systems, vol. 33, pp.
    1877–1901 (2020). URL https://proceedings.neurips.cc/paper files/paper/2020/
    file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf
 5. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.d.O., Kaplan, J., Edwards,
    H., Burda, Y., Joseph, N., Brockman, G., et al.: Evaluating large language models
    trained on code (2021). Eprint: arXiv:2107.03374
 6. Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A.,
    Barham, P., Chung, H.W., Sutton, C., Gehrmann, S., et al.: PaLM: Scaling lan-
    guage modeling with pathways. Journal of Machine Learning Research 24(240),
    1–113 (2023). URL http://jmlr.org/papers/v24/22-1144.pdf
 7. Davies, A., Veličković, P., Buesing, L., Blackwell, S., Zheng, D., Tomašev, N.,
    Tanburn, R., Battaglia, P., Blundell, C., Juhász, A., Lackenby, M., Williamson,
    G., Hassabis, D., Kohli, P.: Advancing mathematics by guiding human intuition
    with AI. Nature 600, 70–74 (2021). DOI 10.1038/s41586-021-04086-x. URL
    https://doi.org/10.1038/s41586-021-04086-x
 8. DeMillo, R., Lipton, R., Perlis, A.: Social processes and proofs of theorems and
    programs. Communications of the ACM 22(5), 271–280 (1979)
18      S. Han et al.

 9. Drori, I., Tran, S., Wang, R., Cheng, N., Liu, K., Tang, L., Ke, E., Singh, N.,
    Patti, T.L., Lynch, J., et al.: A neural network solves and generates mathematics
    problems by program synthesis: Calculus, differential equations, linear algebra, and
    more. CoRR, abs/2112.15594 (2021)
10. Gou, Z., Shao, Z., Gong, Y., Yang, Y., Huang, M., Duan, N., Chen, W., et al.:
    ToRA: A tool-integrated reasoning agent for mathematical problem solving (2023).
    Eprint: arXiv:2309.17452
11. Han, J.M., Rute, J., Wu, Y., Ayers, E.W., Polu, S.: Proof artifact co-training for
    theorem proving with language models. In: International Conference on Learning
    Representations (2022)
12. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E.,
    Song, D., Steinhardt, J.: Measuring mathematical problem solving with the
    MATH dataset. In: Conference on Neural Information Processing Systems
    (2021). URL https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/
    file/be83ab3ecd0db773eb2dc1b0a17836a1-Paper-round2.pdf
13. Hoare, C.A.R.: An axiomatic basis for computer programming. Communications
    of the ACM 12(10), 576–580 (1969). DOI 10.1145/363235.363259. URL https:
    //doi.org/10.1145/363235.363259
14. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Mil oś, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers. In: Conference on Neural Information Processing Sys-
    tems, vol. 35, pp. 8360–8373 (2022). URL https://proceedings.neurips.cc/paper
    files/paper/2022/file/377c25312668e48f2e531e2f2c422483-Paper-Conference.pdf
15. Jiang, A.Q., Welleck, S., Zhou, J.P., Lacroix, T., Liu, J., Li, W., Jamnik, M.,
    Lample, G., Wu, Y.: Draft, sketch, and prove: Guiding formal theorem provers
    with informal proofs. In: International Conference on Learning Representations
    (2023)
16. Lample, G., Lacroix, T., Lachaux, M.A., Rodriguez, A., Hayat, A., Lavril, T.,
    Ebner, G., Martinet, X.: Hypertree proof search for neural theorem proving.
    In: Conference on Neural Information Processing Systems, vol. 35, pp. 26,337–
    26,349 (2022). URL https://proceedings.neurips.cc/paper files/paper/2022/file/
    a8901c5e85fb8e1823bbf0f755053672-Paper-Conference.pdf
17. Limperg, J., From, A.H.: Aesop: White-box best-first proof search for Lean. In:
    International Conference on Certified Programs and Proofs, p. 253–266 (2023).
    DOI 10.1145/3573105.3575671. URL https://doi.org/10.1145/3573105.3575671
18. McCarthy, J.: Recursive functions of symbolic expressions and their computation
    by machine, part I. Communications of the ACM 3(4), 184–195 (1960)
19. de Moura, L., Avigad, J., Kong, S., Roux, C.: Elaboration in dependent type theory
    (2015). Eprint: arXiv:1505.04324
20. Polu, S., Han, J.M., Zheng, K., Baksys, M., Babuschkin, I., Sutskever, I.: For-
    mal mathematics statement curriculum learning. In: International Conference on
    Learning Representations (2023)
21. Polu, S., Sutskever, I.: Generative language modeling for automated theorem prov-
    ing (2020). Eprint: arXiv:2009.03393
22. Scholze, P.: Liquid tensor experiment. https://xenaproject.wordpress.com/2020/
    12/05/liquid-tensor-experiment/ (2020). Last accessed: January 23, 2024
23. Thakur, A., Wen, Y., Chaudhuri, S.: A language-agent approach to formal theorem-
    proving (2023). Eprint: arXiv:2310.04353v3
24. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.A., Lacroix, T.,
    Rozière, B., Goyal, N., Hambro, E., Azhar, F., et al.: LLaMA: Open and efficient
    foundation language models (2023). Eprint: arXiv:2302.13971
              Simplifying Proof Generation with ChatGPT and Basic Search            19

25. Trinh, T.H., Wu, Y., Le, Q.V., He, H., Luong, T.: Solving olympiad geometry with-
    out human demonstrations. Nature 625, 476–482 (2024). DOI 10.1038/s41586-
    023-06747-5. URL https://doi.org/10.1038/s41586-023-06747-5
26. Vishwakarma, R., Mishra, S.: DS-Prover: A dynamic sampling based approach for
    neural theorem proving (2024). URL https://openreview.net/pdf?id=lxlMFlzZO9
27. Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang, Y., Xiong, J., Shi, H., Xie,
    E., Yin, J., Li, Z., Liang, X.: LEGO-Prover: Neural theorem proving with growing
    libraries (2023). Eprint: arXiv:2310.00656
28. Welleck, S., Liu, J., Han, J.M., Choi, Y.: Towards grounded natural language proof
    generation. In: Conference on Neural Information Processing Systems (2021)
29. Wu, M., Norrish, M., Walder, C., Dezfouli, A.: TacticZero: Learning to
    prove theorems from scratch with deep reinforcement learning.             In: Con-
    ference on Neural Information Processing Systems, vol. 34, pp. 9330–
    9342 (2021). URL https://proceedings.neurips.cc/paper files/paper/2021/file/
    4dea382d82666332fb564f2e711cbc71-Paper.pdf
30. Xin, H., Ren, Z.Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu, B., Zhang, L.,
    Lu, X., Du, Q., Gao, W., Zhu, Q., Yang, D., Gou, Z., Wu, Z.F., Luo, F., Ruan,
    C.: DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement
    Learning and Monte-Carlo Tree Search (2024). Eprint: arXiv:2408.08152
31. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assis-
    tants. In: International Conference on Machine Learning, vol. 97, pp. 6984–6994
    (2019). URL http://proceedings.mlr.press/v97/yang19a/yang19a.pdf
32. Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger,
    R., Anandkumar, A.: LeanDojo: Theorem proving with retrieval-augmented lan-
    guage models. In: Conference on Neural Information Processing Systems (2023)
33. Zheng, K., Han, J.M., Polu, S.: MiniF2F: a cross-system benchmark for formal
    olympiad-level mathematics. In: International Conference on Learning Represen-
    tations (2022)
