                                        Preprint




                                        LLM Library Learning Fails: A LEGO-Prover Case Study

                                            Ian Berlot-Attwell♡♠ , Frank Rudzicz♠♣ , Xujie Si♡♠
                                            ♡ University of Toronto, ♠ Vector Institute, ♣ Dalhousie University
                                            Correspondence: ianberlot@cs.toronto.edu



                                                                                   Abstract

                                                  Recent advancements in the coding, reasoning, and tool-using abilities
arXiv:2504.03048v1 [cs.LG] 3 Apr 2025




                                                  of LLMs have spurred interest in library learning (i.e., online learning
                                                  through the creation, storage, and retrieval of reusable and composable
                                                  functions, knowledge, checklists, or lemmas). Such systems often promise
                                                  improved task performance through the automatic creation of broadly
                                                  applicable tools, as well as superior computational performance through
                                                  the caching of reasoning (i.e., the storage of generated tools). However, we
                                                  find strong reasons to be skeptical. We perform an in-depth examination of
                                                  one such system, LEGO-Prover, which purports to learn reusable lemmas
                                                  for mathematical reasoning. We find no evidence of the direct reuse of
                                                  learned lemmas, and find evidence against the soft reuse of learned lemmas
                                                  (i.e., reuse by modifying relevant examples). Crucially, we find that LEGO-
                                                  Prover does not in fact improve over the simple baseline of prompting the
                                                  model – the improvements in task accuracy vanish once computational cost
                                                  is accounted for. Our findings suggest that serious misconceptions exist
                                                  as to the effectiveness of these techniques, that a serious re-examination
                                                  of the state of LLM-based library learning is required, and that we require
                                                  much stronger standards for evaluation including behavioural analysis and
                                                  ensuring that an equal computational budget is used for baselines.1


                                        1     Introduction

                                        Humans extend their capabilities, improve their reliability, and save mental effort through
                                        creating broadly applicable, composable, and reusable tools and knowledge. Whether
                                        software libraries, standard operating procedures, or mathematical lemmas, these artifacts
                                        allow us to save effort, act predictably, act accurately, and more easily solve tasks. Library
                                        learning systems aim to artificially reproduce this ability – e.g., DreamCoder (Ellis et al.,
                                        2021) can learn to write code for complex text editing and LOGO drawing tasks by building
                                        up a library of increasingly complex composable functions.
                                        Recent advances in the coding, reasoning, and tool-use abilities of LLMs has raised the
                                        possibility of performing library learning with LLMs. Coding ability is required to create
                                        reusable and composable code, and tool-use ability is needed to leverage these self-created
                                        tools. Indeed, within the last year, several works have leveraged in-context learning to
                                        perform library learning – prompting the LLM to generate and apply broadly applicable
                                        helper tools. The primary benefit claimed is typically improved performance (Nguyen et al.,
                                        2024), though the proposed reasons for these gains vary. Compared to directly generating
                                        task-specific code, Wang et al. (2024c) and Yuan et al. (2024) hypothesize that library learning
                                        encourages simpler and more reliable functions. Similarly, Qian et al. (2023) suggest that
                                        performance improves because the task is broken down into separate abstract reasoning and
                                        instantiation tasks (i.e., creating a generic tool before calling it with the specifics of the give
                                        problem). Wang et al. (2024a) propose that their system works through the accumulation of
                                        reusable relevant reference examples. These systems may also claim reduced costs through
                                        caching these created tools (Cai et al., 2024).

                                             1We release our code on GitHub: https://github.com/ikb-a/llm lib learning fails



                                                                                        1
Preprint




In this work, we investigate the internal behaviour and black box performance of one such
system: LEGO-Prover (Wang et al., 2024a). LEGO-Prover (i.e., LP in tables) is a LLM-based
library learning system built for the autoformalization of theorems, i.e., converting natural
language proofs into formal theorems verifiable by the Isabelle theorem prover (Paulson,
1994). Specifically, Wang et al. (2024a) reported SotA performance at the time of publication,
and stated that “LEGO-Prover enables LLMs to utilize existing skills retrieved from the
library” and “[m]odular and reusable skills are constantly added to the library to enable
tackling increasingly intricate mathematical problems.” Based on these claims, we aim
to answer two important questions. First: Does LEGO-Prover exhibit library learning
behaviours? Second: Does LEGO-Prover improve performance?
Our contributions are as follows. (1) For a variety of LLMs, we demonstrate that the learned
library is not directly reused. (2) For a variety of LLMs, we provide evidence that the learned
library does not serve as a useful reference for solving related tasks. (3) We demonstrate
that LEGO-Prover does not outperform repeatedly prompting the model after accounting
for computational budget. Together, these points suggests that a serious re-examination
of LLM-based library learning is required. (4) Based on our findings, we make concrete
proposals for improving the development and evaluation of library learning systems.

2   Background
LEGO-Prover was designed to convert natural language proofs into verifiable formal proofs.
It does so through two families of concurrent processes that interact via a shared database:
the P ROVER and E VOLVER.
The P ROVER iterates over pending tasks: For each task, it first decomposes the natural
language proof into requests for potentially useful lemmas (in the form of Isabelle lemma
statements without proofs) and then rewords the natural language proof as a step-by-step
proof, still in English. This step-by-step proof is then augmented with retrieved lemmas and
converted into a formal proof which is either verified or rejected by Isabelle. Simultaneously,
the E VOLVER attempts to prove the requested potentially useful lemmas, adding these to
the shared database. The E VOLVER also attempts to “evolve” existing lemmas to make them
more useful for the solving of retrieved pending tasks or lemma requests. The P ROVER cycles
through a pool of unsolved problems; the maximum number of attempts per problem is a
hyperparameter. In both the P ROVER and E VOLVER, all steps are performed via in-context
learning with examples. Retrieval is performed via Ada embeddings.
We use Draft-Sketch-Prove (Jiang et al., 2023) as a baseline, as done by Wang et al. (2024a).
Draft-Sketch-Prove (i.e., DSP in tables) uses in-context learning to directly convert a natural
language proof into an Isabelle proof, applying post-processing with heuristics to fill or
correct gaps in the proof. In our experiments we use Wang et al. (2024a)’s post-processor and
wrapper of the Isabelle verifier, increasing the timeout to 120s as used by Draft-Sketch-Prove
– this wrapper was derived from Draft-Sketch-Prove and applies a superset of the original
Draft-Sketch-Prove heuristics for correcting generated proofs.
Note that the original implementation of Draft-Sketch-Prove generated all proof attempts
before performing verification. For fairer comparison and reduced cost we modify Draft-
Sketch-Prove to alternate between proof generation and evaluation as LEGO-Prover does,
i.e., once a problem is solved by Draft-Sketch-Prove we cease generating proofs for this task.

3   Evaluating LEGO-Prover Under Various LLMs
We begin by evaluating LEGO-Prover and Draft-Sketch-Prove on the miniF2F test set using
three different LLMs (see Table 1). Following Wang et al. (2024a) we run all models for a
fixed number of prover attempts. We improve upon the original experimental procedure
by performing three trials and reporting the standard deviation. We detail models and
hyperparameters in Appendix A.
Note that our experiments on the full miniF2F test set use gpt-4o-mini as the underlying
LLM instead of ChatGPT-3.5-Turbo as used by Wang et al. (2024a). This model was selected


                                              2
Preprint




           gpt-4o-mini* gpt-4o†           gpt-4o‡    gpt-4o§        o3-mini‡       o3-mini§
    DSP 35.9 ± 0.9%        23.1 ± 1.2% 25.0 ± 0.0%   25.0 ± 0.0% 19.4 ± 2.4% 19.4 ± 4.8%
    LP     25.8 ± 1.6%     29.3 ± 3.1% 29.2 ± 0.0%   33.3 ± 8.3% 27.8 ± 4.8% 36.1 ± 4.8%
      * 100 attempts, miniF2F test set                 † 50 attempts, 20% of miniF2F test set
      ‡ 50 attempts, 10% of miniF2F test set            § 50 attempts, 5% of miniF2F test set


Table 1: Evaluation of LEGO-Prover and Draft-Sketch-Prove for a fixed number of prover
attempts on various subsets of the miniF2F test set. Due to the cost, we reduce the number
of attempts and evaluate more costly models on a subset of the test set. Consequently,
LEGO-Prover and Draft-Sketch-Prove are comparable between rows, but not all columns
can be directly compared. Standard deviations over 3 trials are reported.



due to its superior cost effectiveness and improved reasoning, coding, and mathematics
proficiency (OpenAI, 2024). We find that our Draft-Sketch-Prove performance of 35.9 ± 0.9%
using 4o-mini is close to the 38.5% GPT-3.5-Turbo accuracy reported by Wang et al. (2024a).
This makes the discrepancy with Wang et al. (2024a)’s reported 45.5% (or 50% using human
proofs) LEGO-Prover accuracy all the more striking. We investigated whether LEGO-Prover
may be particularly sensitive to prompt, but found no such evidence (see Appendix B.1 for
details).
With the exception of gpt-4o-mini, these results appear to confirm the findings of Wang
et al. (2024a): LEGO-Prover outperforms Draft-Sketch-Prove which suggests a benefit from
library learning (at the very least under more powerful models).



4     A behavioural analysis of LEGO-Prover

Assuming there is an improvement, what aspect of LEGO-Prover is responsible? The most
obvious explanation is that LEGO-Prover develops a library of useful lemmas. These may
be broadly applicable and useful results that can be directly reused in the problem (as a
mathematician might do when directly applying a theorem). Alternatively, these may be
useful exemplars that are softly reused (i.e., fragments reproduced with minor edits). This
behaviour is akin, e.g., to forking a code repository as the starting point for a new project.
This explanation hypothesizes two key behaviours: First, that the LEGO-Prover can directly
or indirectly leverage relevant lemmas in its proof writing. i.e., the LEGO-Prover can use
relevant lemmas. Second, that the library contains general lemmas that are both relevant to
and leveraged in several tasks. I.e., the LEGO-Prover can reuse lemmas.
In the following sections, we examine both direct and indirect reuse, finding evidence for
use but against both soft and direct reuse.


4.1   Quantifying Soft Use

We quantify the soft use between a given input lemma and the P ROVER’s solution as the
minimum proportion of space-separated tokens in the lemma that must be deleted or
substituted for the lemma to appear within the solution. We obtain this score by first
computing the Levenshtein distance (Levenshtein, 1966) (i.e., the minimum number of
deletions, replacements, or insertions required to convert one string to another) assigning a
weight of 0 to insertions. We allow for an arbitrary number of insertions, as a used lemma
is likely to be only a fragment of the final proof. This modified Levenshtein distance thus
has a value between 0 (all tokens in the lemma also appear in the solution and in the same
order) and, N, the number of tokens in the lemma (no tokens in the lemma appear in the
solution). We divide this value by the length of the lemma to produce a normalized score
for soft use. See Appendix E for examples of various lemmas and their soft use scores.


                                               3
Preprint




                   Model      % of Test Set    Verbatim Use     Name Use
                   GPT-4o              20%             2/43          9/43
                   GPT-4o              10%             4/21          6/21
                   o3-mini             10%             0/20          5/20
                   4o-mini            100%           13/189        47/189

Table 2: Proportion of found solutions in which a retrieved lemma or its name appears in
the solution. We observe that LEGO-Prover’s P ROVER can reproduce the retrieved input
lemmas, however Table 3 reveals that these lemmas are not reused across tasks. We report
sums over 3 runs. Note that we run some models on random subsets of the miniF2F test set
due to cost limitations.


4.2   Does the P ROVER use the input lemmas?

A prerequisite for tool reuse is tool use: a tool cannot be used several times if one cannot
use it at all.
To test for direct use, we apply the methodology by Berlot-Attwell et al. (2024): for every
retrieved lemma provided to the P ROVER we directly check for the presence of the lemma
or the lemma’s name in the P ROVER’s output (the latter being a generous way of accounting
for changes such as whitespace or comments that do not impact semantics). We find that
LEGO-Prover is capable of direct use with gpt-4o and 4o-mini (i.e., directly copying an input
lemma into the final proof – see Table 2). While we do not find direct use with o3-mini, a
manual inspection of the instances of name use finds two solutions where the lemmas were
copied from the input with some modifications (i.e., soft use).
We also find evidence for indirect use. For any given threshold of the soft use score, we can
calculate the proportion of input lemmas with a soft-use score of at least the threshold. This
defines a survival function with the threshold as the independent variable. The greater the
extent of soft use exhibited by the system, the slower we expect this curve to decay. For
systems that perform direct use, this curve does not reach zero as the threshold approaches
one. Instead, the lower bound is the proportion of lemmas that are directly used. To analyze
soft-use behaviour, we compare the survival function of retrieved lemmas against that of
other baseline populations of lemmas. The first baseline is a pool of non-retrieved lemmas
produced by LEGO-Prover (i.e., lemmas written by the same LLM for the same tasks but not
retrieved and provided to the P ROVER). These non-retrieved lemmas represent semantically
and stylistically similar lemmas. The second baseline is a pool of unrelated human-written
lemmas extracted from the 2019 Archive of Formal Proofs (AFP)2 .
These survival curves are plotted in the top row of Figure 1. As expected, we see that the
survival curve of unrelated AFP lemmas drops fastest and rapidly reaches zero (demonstrat-
ing that our soft use metric is capturing relevant information). At high similarity thresholds,
the retrieved lemmas maintain a larger population than the non-retrieved lemmas, thus
providing evidence for soft use. Note that o3-mini is consistent with the trend, but has
noisier measurements, as it was evaluated on a smaller dataset due to cost limitations.

4.3   Does the LEGO-Prover learn a library?

The ability to use tools is a necessary but insufficient condition for library learning. Unlike
mere task decomposition, library learning must create reusable tools. We must therefore
inspect the reuse behaviour of LEGO-Prover. A lemma is said to be reused n times by the
P ROVER if it is used in n + 1 proofs (i.e., the initial use, followed by n reuses).

Direct Reuse We find no evidence for the direct reuse of lemmas (see Table 3). We find only
one instance of name reuse in 189 successful proofs generated by 4o-mini. Manual inspection
reveals that this reuse does not appear in the final verified proof as the reuse was part of an
  2 https://www.isa-afp.org/; see Appendix A for details.



                                              4
Preprint




                                                         Verbatim reused      Name reused
                              Successful   Lemmas in
    Model     % of Test Set                              1   2+               1   2+
                              Attempts      Prompts
    GPT-4o    20%               43/5537            121   0   0                0   0
    GPT-4o    10%               21/2727             64   0   0                0   0
    o3-mini   10%               20/1825             75   0   0                0   0
    4o-mini   100%            189/57419            583   0   0                1   0

Table 3: Lemma reuse in successful P ROVER attempts. For various models and random
subsets of the miniF2F test set, we report the proportion of successful P ROVER attempts, the
number of unique retrieved lemmas occurring in the P ROVER’s input prompts, the number
of lemmas reused verbatim once, or more than once, and the number of lemmas whose
name is reused once, or more than once. A lemma is reused N times if it appears in N + 1
solutions (i.e., the initial use, and then N reuses). We sum all figures over 3 runs.


erroneous proof step generated by the LLM that was replaced by the human-written proof
correction heuristics.

Soft Reuse While these results bode poorly, the original authors claim that “[m]any skills
cannot be directly reused but are very helpful as reference examples for formalizing the
main problem.” Therefore, to study LEGO-Prover’s soft reuse behaviour, we repeat our
survival curves from Section 4.2 but instead plot the proportion of lemmas used in at least
two solutions generated by the LLM (see Figure 1, bottom row). In sharp contrast to our
single-use findings there is no significant difference between the retrieved and non-retrieved
lemmas. This suggests that LEGO-Prover learns overly-specific lemmas that are not reused
in other problems.
As an alternative analysis, we also plot the survival function for the proportion of solved
tasks exhibiting soft use, or soft reuse, at a given threshold (See Figure 2). We note that the
soft reuse curves are within one standard deviation of 0% of tasks by the 70% soft-reuse
threshold, and reach zero while 30-40% of tasks continue exhibiting soft use. This suggests
that soft reuse is not occurring. Note that these curves also reveal an upper bound on the
proportion of tasks that can benefit from lemma reuse, given the created library. Unlike our
previous analyses, this bound arises from the retriever that selects lemmas from the library.
Specifically, some tasks do not retrieve any lemmas that are also retrieved by another task.
Therefore, it is impossible for these tasks to exhibit P ROVER reuse. Consequently, at a soft
use threshold of zero (i.e., all retrieved lemmas are considered to be soft used) the task
survival functions for reuse still attains a value of less than 100% – this value is an upper
bound on the proportion of tasks that can benefit from reuse in the P ROVER, assuming that
the retriever and library remain unchanged.


5    What drives LEGO-Prover’s superior miniF2F performance?

Table 1 appears to demonstrate that LEGO-Prover outperforms Draft-Sketch-Prove. Wang
et al. (2024a), naturally, claim that library learning is the mechanism for this improvement.
However, we have shown that LEGO-Prover does not reuse the learned library. As such, we
claim that the improvements instead arise from increased compute. The original data com-
pares Draft-Sketch-Prove and LEGO-Prover based on a fixed number of P ROVER attempts.
However, this does not account for the compute used by the E VOLVER, which runs in paral-
lel to the P ROVER. The E VOLVER’s compute is significant, as the default hyperparameters
create twice as many E VOLVER processes than P ROVER processes. Furthermore, the P ROVER
itself is more computationally intensive, as it performs a 2-stage process of decomposition
and formalization. Using cost as a proxy for GPU compute, we estimate that each LEGO-
Prover attempt uses approximately 6 times more GPU compute than Draft-Sketch-Prove,
increasing to 14 times with o3-mini (see Table 4). Adjusting for the GPU budget, we find
that Draft-Sketch-Prove matches or outperforms LEGO-Prover (see Table 5).


                                              5
Preprint




                                            LEGO-Prover (4o-mini)             LEGO-Prover (4o)     LEGO-Prover (o3-mini)
                                   100


    1 Solutions)
  % of Lemmas
    Soft Used                                                                                             Retrieved Lemmas
   (Matching                                                                                              Non-Retrieved Lemmas
                                       50
                                                                                                          Irrelevant AFP Lemmas

                                     0
                                       0.0           0.5          1.0    0.0           0.5   1.0   0.0      0.5       1.0
                                   100
    2 Solutions)
  % of Lemmas
  Soft Reused
   (Matching




                                       50

                                       0
                                            0.0      0.5          1.0    0.0           0.5   1.0   0.0      0.5       1.0
                                                           Similarity Threshold for Soft Use & Reuse
                                                           (0 is any degree of use and 1 is direct use)
Figure 1: These plots demonstrate that LEGO-Prover exhibits soft use, but not reuse, of
lemmas. The top row concerns use. It plots the percentage of lemmas meeting a given the
threshold for soft use in at least one solution (see Section 4.1 for the definition of this score).
The lemmas available to the P ROVER are shown in the solid blue line, these are the only
lemmas for which use is possible. As expected, in the top row this line remains the highest
for large values of the threshold, surpassing the non-retrieved lemmas (red dashed line).
However, in the bottom row we consider the proportion of lemmas meeting the soft use
threshold in two tasks (i.e., reused by LEGO-Prover). Unlike in the top row, there is no
significant difference between the lines – suggesting retrieved lemmas are only meaningful
in a single task (consequently, used, not reused). See Section 4.2 for a detailed explanation.


                                       LEGO-Prover (4o-mini)              LEGO-Prover (4o)         LEGO-Prover (o3-mini)
                                 100
Percentage of Tasks Exhibiting




                                                                                                                    Soft Use
                                 80                                                                                 of Lemma
                                                                                                                    Soft Reuse
                                                                                                                    of Lemma
       Soft Use/Reuse




                                 60

                                 40

                                 20

                                  0
                                       0.0         0.5          1.0     0.0        0.5       1.0   0.0      0.5       1.0
                                                           Similarity Threshold for Soft Use & Reuse
                                                           (0 is any degree of use and 1 is direct use)
Figure 2: We define a normalized score for the degree to which a lemma is used in a proof
(i.e., soft use). Using this score and a threshold, we can determine whether LEGO-Prover’s
solution to a task soft-uses the retrieved lemmas provided in the P ROVER’s context. In blue
we plot the percentage of solutions meeting the desired threshold for soft use. In orange,
we plot the percentage of solutions meeting the threshold in a lemma that is also used at the
same level in at least one other solution. We observe that the lines for reuse rapidly reach
zero for even moderate similarity thresholds wheras the lines for use remain relatively high.
This suggests that lemmas are used by the P ROVER in generating solutions, but that there
tends to be only one task that exploits a given lemma.


                                                                                   6
Preprint




                                              gpt-4o-mini     gpt-4o   o3-mini
                   GPU Budget Ratio           5.84            5.94     14.23

Table 4: We find that LEGO-Prover uses significantly more GPU resources that Draft-Sketch-
Prove per attempt, and calculate the ratio of the costs under a fixed number of attempts.
This ratio grows larger for o3-mini as LEGO-Prover uses significantly more output tokens
per input token. We speculate that either lemma creation or reasoning about the use of
lemmas require a higher proportion of reasoning tokens than directly solving the task.

               gpt-4o-mini* gpt-4o†             gpt-4o‡       gpt-4o§       o3-mini‡      o3-mini§
  DSP          35.9 ± 0.9%     23.1 ± 1.2%      25.0 ± 0.0%   25.0 ± 0.0% 19.4 ± 2.4% 19.4 ± 4.8%
  LP           17.5 ± 0.9%     23.8 ± 1.2%      22.2 ± 2.4%   22.2 ± 4.8% 15.3 ± 2.4% 19.4 ± 9.6%
  LP attempts 17               9                8             6             4             3
* 100 DSP attempts, miniF2F test set                     † 50 DSP attempts, 20% of miniF2F test set
 ‡ 50 DSP attempts, 10% of miniF2F test set               § 50 DSP attempts, 5% of miniF2F test set


Table 5: A modification of Table 1 that limits the number of LEGO-Prover attempts to match
Draft-Sketch-Prove’s compute budget. Note that Draft-Sketch-Prove consistently outper-
forms LEGO-Prover or is within one standard deviation of LEGO-Prover’s performance.
Average accuracy and standard deviations are again reported over 3 trials.


However, this analysis it limited – it is possible that Draft-Sketch-Prove initially matches
the performance before plateauing ahead of LEGO-Prover, or that LEGO-Prover requires
a certain number of iterations for the library to reach a critical mass. Therefore, we run
a followup experiment in which we extend our Draft-Sketch-Prove runs, increasing the
number of iterations to approximately match the GPU resources used using cost as as
proxy. Doing so, we find that Draft-Sketch-Prove remains within one standard deviation or
outperforms LEGO-Prover throughout the evaluation (see Figure 3).


6   Related Work

Within the specific area of LLM-based library learning, there has been growing evidence
that these systems do not perform direct reuse. Berlot-Attwell et al. (2024) previously
studied LEGO-Prover and TroVE (Wang et al., 2024c), finding negligible direct reuse within
these systems and instead proposing that the performance gains are due to self-correction
and indirect reuse. Similarly, Nguyen et al. (2024) reported that their library learning
DynaSaur system achieved SoTA results on the GAIA agent benchmark (Mialon et al.,
2024), but exhibited low direct reuse of the learned libraries. They did not speculate on
the implications, however, beyond that it may be addressed via curriculum learning. Our
work (1) provides further evidence against direct reuse (to the best of our knowledge we
are the first to evaluate direct reuse in a reasoning model), (2) advances our understanding
by providing new evidence against the soft reuse hypothesis, and (3) provides a simple
compute-based hypothesis as to why these systems outperform their baselines – they
increase the test-time compute per attempt in a way that is not accounted for in typical
evaluation methods.
In the related domain of Python code generation, Olausson et al. (2024) studied the relative
efficacy of self-correction as compared to increased sampling for the APPS (Hendrycks
et al., 2021) and HumanEval (Chen et al., 2021) tasks. Unlike our results, they found a
moderate effect when accounting for compute. They hypothesized that “current models are
held back by their inability to reliably produce accurate and useful feedback on why the
code is wrong.” Given the known success of tool-using LLMs (e.g., ViperGPT (Surı́s et al.,
2023) achieved SotA performance on vision-language tasks using a code generating LLM
conditioned on a human provided Python library for vision processing), we suspect that
there may be a similar bottleneck in library learning. I.e., these systems may be held back
by an inability to reliably produce general theorems and would improve in performance if
given human-created libraries.


                                                  7
Preprint




                                                LP and DSP Accuracy vs. Average Cost                   LEGO-Prover
                    100% of Test Set                                                                   DSP
                    4o-mini Backend




                                       20

                                       0
                                            0    10          20      30        40          50         60           70
                                       30
                    o3-mini Backend
                    10% of Test Set




                                       20
% of Tasks Solved




                                       10
                                       0
                                            0          50               100              150               200
                                       30
                    gpt-4o Backend
                    10% of Test Set




                                       20
                                       10
                                       0
                                            0    10          20      30        40          50         60           70
                                       30
                    gpt-4o Backend
                    20% of Test Set




                                       20
                                       10
                                       0
                                            0     20           40         60        80          100          120
                                                            Average Cost (USD)
Figure 3: Average LEGO-Prover and Draft-Sketch-Prove performance compared by average
cost in USD. The shaded region is 1 standard deviation based on 3 trials. Draft-Sketch-Prove
has strongly superior performance using 4o-mini, and comparable performance on gpt-4o
and o3-mini. The vertical line represents the number of Draft-Sketch-Prove prover attempts
equal to LEGO-Prover’s. For reasons of cost o3-mini was run on a random 10% subset of
the test set and gpt-4o was run on the same random 10% subset as well as a 20% subset.
Note that as the cost of o3-mini was over twice our predicted cost we were unable to run
Draft-Sketch-Prove for a comparable budget. See Appendix D for the details of how this
plot was generated.




                                                                    8
Preprint




In the domain of agentic AI, Kapoor et al. (2024) call for the use of cost as a metric and claim
that planning, reflection, and debugging offer no improvement over trivial baselines on
the HumanEval (Chen et al., 2021) task. Our work provides similar findings in the area
of autoformalization when using the techniques of library learning. This is interesting, as
autoformalization is closer to a translation task rather than generation (i.e., converting a
natural language proof to code) and, unlike Python programming, we have access to a
strong verifier that can confirm the correctness of our reasoning (i.e., unlike self-correction
that may introduce errors by fixing hallucinatory errors, all intermediary lemmas are
verified by Isabelle). Despite these advantages, we do not to find an improvement in
accuracy. Furthermore, given our focus on library learning specifically, we also go into the
details of whether the system internally behaves as expected, as opposed to studying the
general trends of cost and accuracy. In doing so, we find evidence that these techniques are
ineffective and fail to operate as believed, suggesting that there are fundamental flaws in
these specific approaches.


7   Conclusions

We have gained a number of insights into the LEGO-Prover system. Firstly, LEGO-Prover
does not exhibit reuse behaviour – therefore, it does not perform library learning. Sec-
ondly, LEGO-Prover does not improve performance over a simple prompting baseline once
computational cost is accounted for.
These findings, particularly with respect to accounting for computational budget, become
wide-reaching when considered in the broader literature of LLM library learning. Our
work combines with other emerging evidence to suggest serious flaws in the assessment of
LLM-based library learning. It was believed that LLM library learning works, as it improves
performance – but our findings on the importance of accounting for computational cost
cast this into question. We are unaware of any LLM-based library learning work that
controls for compute in its evaluation. It is possible that the observed benefits of library
learning are simply due to a hidden form of inference-time scaling. This calls into the
question the efficacy of all these works – and we cannot hope to make progress without
resolving this problem. This would also go towards explaining other findings: previous
work has demonstrated that the library learning system TroVE does not outperform library-
free ablations (Berlot-Attwell et al., 2024) – whereas our work can explain this finding as
Berlot-Attwell et al. (2024)’s ablation implicitly matched computational cost. Our work
can also explain apparent paradoxes – the DynaSaur library learning system reports SoTA
performance and a lack of reuse behaviour (Nguyen et al., 2024). This contradiction is
resolved if increased inference-time compute is responsible for the performance gains.
Indeed, in their evaluation, they fixed all models to 20 steps. I.e., their evaluation did
not account for the differences in computational cost per step between DynaSaur, direct
prompting of gpt-4o, Sibyl (Wang et al., 2024b), and HF Agent (Roucher & Nguyen, 2024).
These findings also call into question the argument that LLM library learners can reduce
costs (at least in their current form). The caching of generated tools is moot if said tools
are not reused, and our analysis suggests that they are not. Secondly, the savings from
caching must exceed the cost of creating and selecting these tools – we perform the first
cost-controlled comparison of an LLM library learner that we are aware of and find no
improvement over prompting with the same budget.
Looking to how we can build better systems – from the perspective of accuracy, our work
suggests that our effort may be best directed towards improving base models. From the
perspective of library learning, our work calls into question the innate ability of LLMs to
perform refactoring using in-context learning alone. Our suggestion would therefore be
towards incorporating symbolic refactoring systems that are known to work (e.g., the LILO
(Grand et al., 2024) system takes this approach). If we instead wish to use LLMs directly for
library learning then, as context learning is not enough, it may be worthwhile to explore
finetuning or RL (e.g., via GRPO (DeepSeek-AI et al., 2025) with human-written reward
functions, possibly based on compression). Critically, any such system must be evaluated
thoroughly. Therefore, any system claiming to perform library learning should be evaluated


                                               9
Preprint




with respect to both accuracy accounting for computational budget, and the system’s
behaviour. The extent of reuse must be measured, be it direct or soft reuse. In service of this
goal, we also suggest the construction of a synthetic diagnostic dataset based on a known
ground truth library.


Acknowledgments

Resources used in preparing this research were provided, in part, by the Province of
Ontario, the Government of Canada through CIFAR, and companies sponsoring the Vector
Institute www.vectorinstitute.ai/partnerships/. Generous support was also provided by
the Microsoft Accelerating Foundation Models Research (AFMR) program.
We would also like to thank Francois Roewer-Despres and Haokun Liu for their time and
conversations that helped in various ways to shape and improve this work. We would also
like to thank Steven Zhong for his technical support, without which this project would not
have been possible.


References
Ian Berlot-Attwell, Frank Rudzicz, and Xujie Si. Library learning doesn’t: The curious case
  of the single-use “library”. In The 4th Workshop on Mathematical Reasoning and AI at
  NeurIPS’24, 2024. URL https://openreview.net/forum?id=et2T8SKF1O.

Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou. Large language mod-
  els as tool makers. In The Twelfth International Conference on Learning Representations,
  2024. URL https://openreview.net/forum?id=qV83K9d5WB.

Anwoy Chatterjee, H S V N S Kowndinya Renduchintala, Sumit Bhatia, and Tanmoy
 Chakraborty. POSIX: A prompt sensitivity index for large language models. In Yaser
 Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (eds.), Findings of the Association
 for Computational Linguistics: EMNLP 2024, pp. 14550–14565, Miami, Florida, USA,
 November 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.
 findings-emnlp.852. URL https://aclanthology.org/2024.findings-emnlp.852/.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto,
 Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray,
 Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin,
 Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mo-
 hammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings,
 Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen
 Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji,
 Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua
 Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage,
 Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish,
 Ilya Sutskever, and Wojciech Zaremba. Evaluating large language models trained on code.
 CoRR, abs/2107.03374, 2021. URL https://arxiv.org/abs/2107.03374.

DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin
 Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu,
  Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan
 Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu
  Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong
  Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu,
  Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong
  Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L.
  Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin
  Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang,
  Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng Li, Miaojun
 Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu


                                              10
Preprint




  Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin,
  Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang,
  Shuiping Yu, Shunfeng Zhou, Shuting Pan, and S. S. Li. DeepSeek-R1: Incentivizing
  reasoning capability in LLMs via reinforcement learning. CoRR, abs/2501.12948, 2025.
  doi: 10.48550/ARXIV.2501.12948. URL https://doi.org/10.48550/arXiv.2501.12948.
Kevin Ellis, Catherine Wong, Maxwell I. Nye, Mathias Sablé-Meyer, Lucas Morales, Luke B.
  Hewitt, Luc Cary, Armando Solar-Lezama, and Joshua B. Tenenbaum. DreamCoder: boot-
  strapping inductive program synthesis with wake-sleep library learning. In Stephen N.
  Freund and Eran Yahav (eds.), PLDI ’21: 42nd ACM SIGPLAN International Conference
  on Programming Language Design and Implementation, Virtual Event, Canada, June
  20-25, 2021, pp. 835–850. ACM, 2021. doi: 10.1145/3453483.3454080. URL https:
 //doi.org/10.1145/3453483.3454080.
Gabriel Grand, Lionel Wong, Matthew Bowers, Theo X. Olausson, Muxin Liu, Joshua B.
 Tenenbaum, and Jacob Andreas. LILO: Learning interpretable libraries by compress-
 ing and documenting code. In The Twelfth International Conference on Learning
 Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
 URL https://openreview.net/forum?id=TqYbAWKMIe.
Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan
 Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt. Mea-
 suring coding challenge competence with APPS. In Joaquin Vanschoren and Sai-Kit Ye-
 ung (eds.), Proceedings of the Neural Information Processing Systems Track on Datasets
 and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual,
 2021. URL https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/
 c24cd76e1ce41366a4bbe8a49b02a028-Abstract-round2.html.
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda
  Li, Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove:
  Guiding formal theorem provers with informal proofs. In The Eleventh International
  Conference on Learning Representations, 2023. URL https://openreview.net/forum?
  id=SMa9EAovKMC.
Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, and Arvind Narayanan.
  AI agents that matter. CoRR, abs/2407.01502, 2024. doi: 10.48550/ARXIV.2407.01502.
  URL https://doi.org/10.48550/arXiv.2407.01502.
Vladimir Iosifovich Levenshtein. Binary codes capable of correcting deletions, insertions
  and reversals. Soviet Physics Doklady, 10(8):707–710, feb 1966. Doklady Akademii Nauk
  SSSR, V163 No4 845-848 1965.
Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom.
  GAIA: a benchmark for general AI assistants. In The Twelfth International Conference on
  Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net,
  2024. URL https://openreview.net/forum?id=fibxvahvs3.
Dang Nguyen, Viet Dac Lai, Seunghyun Yoon, Ryan A. Rossi, Handong Zhao, Ruiyi Zhang,
 Puneet Mathur, Nedim Lipka, Yu Wang, Trung Bui, Franck Dernoncourt, and Tianyi Zhou.
 DynaSaur: Large language agents beyond predefined actions. CoRR, abs/2411.01747,
 2024. doi: 10.48550/ARXIV.2411.01747. URL https://doi.org/10.48550/arXiv.2411.
 01747.
Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and Armando Solar-
  Lezama. Is self-repair a silver bullet for code generation? In International Conference on
  Learning Representations (ICLR), 2024.
OpenAI. GPT-4o mini: advancing cost-efficient intelligence. https://openai.com/index/
 gpt-4o-mini-advancing-cost-efficient-intelligence/, 2024. Accessed: 2025-03-19.
Lawrence C. Paulson. Isabelle - A Generic Theorem Prover, volume 828 of Lecture Notes in
  Computer Science. Springer, 1994. ISBN 3-540-58244-4. doi: 10.1007/BFB0030541. URL
  https://doi.org/10.1007/BFb0030541.


                                            11
Preprint




Cheng Qian, Chi Han, Yi Ren Fung, Yujia Qin, Zhiyuan Liu, and Heng Ji. CRE-
 ATOR: Tool creation for disentangling abstract and concrete reasoning of large lan-
 guage models. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), Findings of
 the Association for Computational Linguistics: EMNLP 2023, Singapore, December
 6-10, 2023, pp. 6922–6939. Association for Computational Linguistics, 2023. doi:
 10.18653/V1/2023.FINDINGS-EMNLP.462. URL https://doi.org/10.18653/v1/2023.
 findings-emnlp.462.

Aymeric Roucher and Dang Nguyen. Beating GAIA with Transformers Agents. https:
 //github.com/aymeric-roucher/GAIA, 2024. Accessed: 2025-03-19.

Dı́dac Surı́s, Sachit Menon, and Carl Vondrick. ViperGPT: Visual inference via python
  execution for reasoning. In IEEE/CVF International Conference on Computer Vision,
  ICCV 2023, Paris, France, October 1-6, 2023, pp. 11854–11864. IEEE, 2023. doi: 10.1109/
  ICCV51070.2023.01092. URL https://doi.org/10.1109/ICCV51070.2023.01092.

Jan Philip Wahle, Terry Ruas, Yang Xu, and Bela Gipp. Paraphrase types elicit prompt
  engineering capabilities. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen
  (eds.), Proceedings of the 2024 Conference on Empirical Methods in Natural Language
  Processing, pp. 11004–11033, Miami, Florida, USA, November 2024. Association for
  Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.617. URL https:
  //aclanthology.org/2024.emnlp-main.617/.

Haiming Wang, Huajian Xin, Chuanyang Zheng, Zhengying Liu, Qingxing Cao, Yinya
 Huang, Jing Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and Xiaodan Liang. LEGO-
 Prover: Neural theorem proving with growing libraries. In The Twelfth International
 Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024.
 OpenReview.net, 2024a. URL https://openreview.net/forum?id=3f5PALef5B.

Yulong Wang, Tianhao Shen, Lifeng Liu, and Jian Xie. Sibyl: Simple yet effective agent
  framework for complex real-world reasoning. CoRR, abs/2407.10718, 2024b. doi: 10.
  48550/ARXIV.2407.10718. URL https://doi.org/10.48550/arXiv.2407.10718.

Zhiruo Wang, Graham Neubig, and Daniel Fried. TroVE: Inducing verifiable and efficient
  toolboxes for solving programmatic tasks. In Forty-first International Conference on
  Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024c.
  URL https://openreview.net/forum?id=DCNCwaMJjI.

Lifan Yuan, Yangyi Chen, Xingyao Wang, Yi Fung, Hao Peng, and Heng Ji. CRAFT: Cus-
  tomizing LLMs by creating and retrieving from specialized toolsets. In The Twelfth
  International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May
  7-11, 2024. OpenReview.net, 2024. URL https://openreview.net/forum?id=G0vdDSt9XM.


A   Technical Details & Hyperparameters

In our experiments we use gpt-4o version 2024-08-06, o3-mini version 2025-01-31, 4o-mini
version 2024-07-18, and text-embedding-ada-002.
LEGO-Prover’s hyperparameters are listed in Table 6; values changed from defaults are
underlined. Note that Wang et al. (2024a) use 50 attempts for their ablation experiments.
Draft-Sketch-Prove’s hyperparameters are listed in Table 7. Note that we modified Draft-
Sketch-Prove to run 11 processes in parallel (with each launching its own Isabelle instance)
so that the average resources per Isabelle instance is equal to LEGO-Prover. The prompts
used in our experiment are documented in Appendix C. All our experiments use Isabelle
2022.
We used fixed, random, non-overlapping subsets of 5%, 10% and 20% of the miniF2F
test set for our experiments. For reasons of cost, we only study system behaviour with
human-written English proofs as inputs to the systems.


                                            12
Preprint




           LEGO-Prover Hyperparameter                             Value
        Temperature                                0.7, (N/A for o3-mini)
        # P ROVER Processes                        3
        # E VOLVER Processes                       8
        # Attempts                                 100 for full miniF2F test set, else 50
        E VOLVER maximum tokens decoded            1024, (8092 for o3-mini)
        P ROVER maximum tokens decoded             2000, (8092 for o3-mini)

Table 6: LEGO-Prover hyperparameters. Values changed from Wang et al. (2024a) are
underlined.

       Draft-Sketch-Prove Hyperparameter                           Value
       Temperature                                 0.0, (N/A for o3-mini)
       # Processes                                 11
       # Attempts                                  100 for full miniF2F test set, else 50
       Maximum tokens decoded                      2048, (8092 for o3-mini)

Table 7: Draft-Sketch-Prove hyperparameters. Values changed from Jiang et al. (2023) are
underlined.

Our pool of unrelated Isabelle lemmas used in Figures 1 and 2 are extracted from the
2019-08-19 Archive of Formal Proofs3 . Specifically, we used all matches to the following
Python3 regex:

(?:lemma|theorem)\s+[ˆ:]+?\s*:(?:[\s\S](?!lemma|theorem))+?qed

This regex matches lemmas and theorems with similar syntax to the in-context examples,
though it may prematurely truncate some lemmas and theorems.
Each experiment is performed with a resource allocation of 180 GB of RAM and 50 Intel
Broadwell CPU cores @2.095 GHz. These resources are shared among all Isabelle instances.

B   Limitations
Due to reasons of cost, we were unable to run o3-mini or gpt-4o on the full test set. o3-mini
in particular was far more costly than expected As such, we could only afford to evaluate
on a 10% subset of the test set. Having said this, we do observe the same trends across all
three of the LLMs studied, and we were able to evaluate gpt-4o-mini on the full test set.
Cost and a lack of access to the underlying model also raise barriers to the reproduction of
this work. We are releasing all of our collected data in an effort to lower barriers, as well
as releasing our code so that it may be adapted to other LLMs. This data also includes
the token usage for all of our experiments, allowing for more precise estimates of cost, as
well as the estimation of costs under other LLMs. We also used gpt-4o-mini for our largest
experiments, reducing the cost of these experiments.
In the interests of improved reproducibility we also attempted evalua-
tion      using      DeepSeek-R1-Distill-Qwen-1.5B,         DeepSeek-R1-Distill-Qwen-7B,
DeepSeek-R1-Distill-Llama-8B, and DeepSeek-R1-Distill-Llama-70B. Unfortunately,
were unable to get the Draft-Sketch-Prove baseline to work due as we found all of these
models posses a strong bias for producing Lean 4 code. On the rare occasions when the
models did produce Isabelle code, it was still produced within a lean code block – based on
this we suspect that lean theorem proving was used in the distillation data, and possibly
also as one of the RL tasks used to originally train DeepSeek R1.
   3Available for download at the time of publication from https://sourceforge.net/projects/afp/
files/afp-Isabelle2019/


                                              13
Preprint




There are also limitations to the measurement of cost. Firstly, we could only measure the
token usage of completed runs, therefore there may be slight distortions in Figure 3 as it
was necessary to plot based on the average cost per attempt. In reality, it will be the case
(at least for Draft-Sketch-Prove) that the cost per attempt reduces slightly over time, as the
pool of problems to solve shrinks and fewer problems must be tried per attempt. Secondly,
LEGO-Prover uses the text-embedding-ada-002 model for the retrieval of lemmas, lemma
requests, and pending tasks. For some LEGO-Prover logs we were unable to log Ada usage.
As such we chose to remove Ada from the cost for all of our plots – in practice the cost of
Ada was quite low and this omission reduces LEGO-Prover’s running costs, therefore we
do not consider this to be an issue.
Another limitation applies to our LEGO-Prover evaluations with gpt-4o and o3-mini, as
well as our prompt stability experiments in Appendix B.1. We performed our experiments
using the released LEGO-Prover code base, however we realized after our experiments
were completed that this code base forcibly initializes the E VOLVER with a database of
all test queries. As such, the LEGO-Prover evolver has access to information about other
tasks. The impact of this on the LEGO-Prover’s performance is unclear: on one hand our
intuition suggests that this may distract the LEGO-Prover from the tasks at hand, hindering
performance until new P ROVERrequests take priority. On the other hand, we performed
some informal experiments with LEGO-Prover ablations using gpt-4o-mini and found that
preventing the E VOLVER from retrieving these entries counter-intuitively slowed the rate at
which problems were solved. Regardless, given the vast gap in cost (which persists in our
4o-mini experiments for which the E VOLVER was initialized with exactly the set of tasks
to be solved), we do not believe that adjusting the E VOLVER’s initialization will have a
significant impact on our results.
Other limitations are due to our chosen soft use score. Firstly, our key assumption was that
soft use would take a form similar to the modification of starter code. It remains possible
that there are other forms of soft reuse (e.g., ones that involves substantial paraphrasing or
merely imitate the general structure of the lemma) that our soft use score would not detect.
Having said this, as the difference between the text and the proof increases, our intuition
dictates that the likelihood of the introduction of an error would increase (as the model
would be further distancing itself from the Isabelle-verified code), and thus the value of
such reuse would decrease. Secondly, as our metric does not penalize the insertion of new
tokens, it almost certainly scores shorter lemmas higher on average. Having said this, we
believed that this trade-off was acceptable, given the premise that the final proof would
(and, indeed, in any working library learning system should) contain more than just the
lemma – e.g., a proof may use the Pythagorean theorem, but it would do so in conjunction
with other axioms, lemmas, and reasoning steps.
One concern is that gpt-4o and o4-mini scores appear to be low on our random test subsets.
We suspect that random test sets consist of harder problems. Specifically, we can observe in
Tables 1 & 8 that while Draft-Sketch-Prove reproduces Wang et al. (2024a)’s reported overall
miniF2F test set accuracy, its performance drops by 15.9% (absolute) on our random 5%
subset of the test set.
Another possible limitation follows from our observation that o3-mini has difficulties placing
the solutions to lemma requests inside of markdown code blocks. Through manual prompt
tuning we were able to improve the reliability but it remains imperfect – it is possible
that this behaviour reduces the performance of LEGO-Prover by slowing the E VOLVER.
Closely related, as neither Draft-Sketch-Prove nor LEGO-Prover were designed for reasoning
models, their prompts are suboptimal. OpenAI recommends that prompts be short, and
not contain examples. Thus the options were to use suboptimal prompts, or to significantly
modify the prompts of both models (which, due to the low temperature used by Draft-
Sketch-Prove, could eliminate variations in Draft-Sketch-Prove prompt required to solicit
diverse LLM responses). Ultimately we erred towards the side of caution and chose to make
only the minimal changes required to correct any gross errors of behaviour in Draft-Sketch-
Prove or LEGO-Prover (e.g., formatting errors, producing proofs for example problems,
etc...). Based on our prompt stability experiments (see Appendix B.1) we believe that minor
rephrasing of our final prompts would not seriously change the results, though it remains
possible that o3-mini behaves significantly differently to gpt-4o-mini in this regard.


                                             14
Preprint




       model    val Baseline acc                        val Paraphrase acc            Max Pot. Gain         Max Pot. Loss
       dsp      50.0 ± 0.0%                             48.3 ± 3.7%                   0.0%                  0.0%
       lp       38.3 ± 4.6%                             38.3 ± 4.6%                   0.0%                  0.0%
      model    test Baseline acc                        test Paraphrase acc           Max Pot. Gain         Max Pot. Loss
      dsp      16.7 ± 0.0%                              20.0 ± 4.6%                   16.7%                 0.0%
      lp       18.3 ± 3.7%                              16.7 ± 5.9%                   0.0%                  0.0%

Table 8: Average test accuracy of the models under both our baseline prompt and para-
phrases of the prompt. We also report variability in the results, following the methodology
for prompt sensitivity from Wahle et al. (2024). All experiments were run using 50 attempts,
5 runs, and on a 5% split of the miniF2F validation and test sets respectively.

                                                         Prompt Stability, 5% of Validation Set
                                               50

                                               40
                        % of Problems Solved




                                               30

                                               20

                                               10                                LEGO-Prover
                                                                                 LP (paraphrased prompt)
                                                                                 DSP
                                               0                                 DSP (paraphrased prompt)
                                                    0     10         20          30        40         50
                                                                     Solver Attempt


Figure 4: For LEGO-Prover and Draft-Sketch-Prove we compare 5 runs with our default
prompt versus 5 runs with different paraphrased prompts. We evaluate on a subset of the
validation set. We find that the systems are fairly robust to minor changes in wording –
performance is typically within 1 standard deviation. These results are for a 5% subset of
the validation split.


Another concern is that due to the changes made to our prompts the resulting prompts may
be suboptimal. To address this possibility we study the prompt sensitivity of Draft-Sketch-
Prove and LEGO-Prover; the results are outlined in Appendix B.1.

B.1   Stability with Respect to Prompt

For both Draft-Sketch-Prove and LEGO-Prover we were required to make minor modifica-
tions to the prompt to ensure that 4o-mini generated responses with the correct formatting
(See Appendix C for the prompts and our modifications). To address the concern that our
choice of prompt may be disadvantaging LEGO-Prover, we generate five prompt para-
phrases, and following Wahle et al. (2024) study the relative stability under the paraphrased
prompts versus the original prompt. We generate the prompt paraphrases using GPT3.5, as
done by Chatterjee et al. (2024).
We find no evidence that LEGO-Prover is disadvantaged by prompt: accuracies are within
one standard deviation, and there was no maximum potential gain (i.e., no problems were
solved under one of the paraphrases, but not by the original prompt). See Table 8 for details.
Indeed, Draft-Sketch-Prove exhibited potential gain, suggesting that our Draft-Sketch-Prove
prompt may be supoptimal. We also plot the performance per attempt in Figures 4 and 5.
Note that we modify Wahle et al. (2024)’s maximum potential gain metric to reflect that we
collect data from 5 baseline trials instead of one. In our implementation, we consider it to be
a 0% improvement for a specific problem if a paraphrase achieves the same performance or
worse (i.e., no improvement is possible for problems solvable under the baseline prompt),
and 100% if it solves a task that was unsolved under the baseline prompt. Averaging over


                                                                       15
Preprint




                                                        Prompt Stability, 5% of Test Set
                                              25

                                              20




                       % of Problems Solved
                                              15

                                              10

                                              5
                                                                             LEGO-Prover
                                                                             LP (paraphrased prompt)
                                              0                              DSP
                                                                             DSP (paraphrased prompt)
                                                   0   10        20          30        40         50
                                                                 Solver Attempt


Figure 5: For LEGO-Prover and Draft-Sketch-Prove we compare 5 runs with our default
prompt versus 5 runs with different paraphrased prompts. We evaluate on a subset of
the test set. We find that these system are fairly robust to minor changes in wording –
performance is typically within 1 standard deviation. These results are for a 5% subset of
the test split.


all problems this becomes the fraction of problems that are only solved by a paraphrased
prompt. The maximum potential loss is calculated in the same way but with the rewards
reversed, thus becoming the fraction of problems that are solved by the baseline prompt,
but by none of the paraphrased prompts.

C     Changes to Prompts

C.1     Draft-Sketch-Prove

Draft-Sketch-Prove was originally designed for text completion models, specifically Codex
code-davinci-002 (Hendrycks et al., 2021). As it was not designed for conversational
models, and none of the models evaluated support a text completion mode, we developed
our own minimal system prompts to preface the few-shot examples preprended by Draft-
Sketch-Prove to the task statement.

C.1.1    gpt-4o-mini & gpt-4o System Prompt
In the prompt we emphasized the use of sledgehammer as it was a focus of the original
Draft-Sketch-Prove paper, and the model would avoid its use unless told otherwise. After
designing the prompt for gpt-4o-mini, we found that gpt-4o displayed no obviously incorrect
behaviours, so we did not modify it further. We validated our prompts on a subset of two
validation set problems (mathd algebra 109 and algebra sqineq 2at2pclta2c2p41pc).

As a mathematician familiar with Isabelle, your task is to complete the proof sketch provided
by the user, MAKING SURE TO **ALWAYS** USE ‘sledgehammer‘ TO PROVE THE
INTERMEDIATE RESULTS.




                                                                   16
Preprint




C.1.2    o3-mini System Prompt
For o3-mini we modified the prompt to explicitly prohibit o3-mini from answering the in-
context examples. We also removed the instruction to use sledgehammer as o3-mini would
ignore the examples and attempt to use “by sledgehammer” instead of “sledgehammer” – this
would cause parsing errors in the human proof-correcting heuristics. Based on our small
validation set of two problems, we found that removing the instruction to use sledgehammer
worked more reliably than adding instructions to use sledgehammer correctly.

Complete the Isabelle proof sketch provided by the user. The user will provide several
examples, but you should only complete the last example (i.e., the example that does not
have a proof).

C.2     LEGO-Prover

LEGO-Prover was designed for conversational models, and as such has default system
prompts for the P ROVER decomposer, P ROVER formalizer, and several E VOLVER variants.
As a general rule, we attempted to minimize changes to these prompts where possible,
doing so only when we found erroneous behaviour. Text in green is added to the prompt,
text in red is removed from the original prompt.

C.2.1    gpt-4o-mini prompts
For gpt-4o-mini we found it necessary to add additional formatting instructions to the
P ROVER’s decomposer prompt:

As an mathematician and expert in isabelle theorem prover, your task is to analyze the
given theorem (including problem’s informal statement, human written informal proof, and
formal statement). Provide a better structured step by step proof that closer to isabelle. and
request relevant lemmas, theorems that might help in proving this problem.
You will format your answer as follows:
- A section with the header ‘## Structured informal proof‘ containing the step-by-step proof.
- A subsequent section with the header ‘## Request skills‘ containing any requested relevant
lemmas or theorems
- Each requested skill is represented by an isabelle code block containing its formal definition

We also observed that the rate of rejection of proof attempts was high due to slight para-
phrasing of the requested theorem statement. We addressed this by modifying the P ROVER’s
formalizer prompt:

As a mathematician familiar with Isabelle, your task is to provide a formal proof in response
to a given problem statement.
Your proof should be structured and clearly written, meeting the following criteria:
- It can be verified by Isabelle.
- Each step of the proof should be explained in detail using comments enclosed in ”(*” and
”*)”.
- The explanation for each step should be clear and concise, avoiding any unnecessary or
apologetic language.
- You are **strongly encouraged** to create useful and reusable lemmas to solve the problem.
- The lemmas should be as general as possible (generalizable), and be able to cover a large
step in proofs (non-trivial).
- You **MUST** copy the input lemma EXACTLY: **without changing whitespace**, without
paraphrasing, and without adding comments.
Please ensure that your proof is well-organized and easy to follow, with each step building
upon the previous one.

The E VOLVER prompts were unchanged.


                                             17
Preprint




C.2.2   gpt-4o prompts
For gpt-4o we used the gpt-4o-mini prompts and further modified the P ROVER’s decomposer
prompt to prevent it from decomposing the provided in-context examples.

As an mathematician and expert in isabelle theorem prover, your task is to analyze the
given theorem (including problem’s informal statement, human written informal proof, and
formal statement). Provide a better structured step by step proof that is closer to isabelle.
You will be given several examples; you must only decompose the last theorem given (i.e.,
the only theorem without a provided solution).
Furthermore, you must and request relevant lemmas, theorems that might help in proving
this problem.
You will format your answer as follows:
- A section with the header ‘## Structured informal proof‘ containing the step-by-step proof.
- A subsequent section with the header ‘## Request skills‘ containing any requested relevant
lemmas or theorems
- Each requested skill is represented by an isabelle code block containing its formal definition


C.2.3   o3-mini prompts
For o3-mini we found it necessary to change all prompts to prevent the model from solving
the in-context examples. We also found o3-mini struggled with placing the solution to
proofs inside of Markdown code blocks, even after Markdown formatting was enabled by
prepending “Formatting re-enabled” to the prompts.
For P ROVER’s decomposer prompt we re-enabled Markdown formatting and added instruc-
tions to not decompose the in-context examples.

Formatting re-enabled
As an mathematician and expert in isabelle theorem prover, your task is to analyze the
given theorem (including problem’s informal statement, human written informal proof, and
formal statement). Provide a better structured step by step proof that closer to isabelle. and
request relevant lemmas, theorems that might help in proving this problem. Note that you
will be provided with several examples, but you should only complete the last example (i.e.,
the example that does not have a structured step by step proof and requests for relevant
lemmas).
You will format your answer as follows:
- A section with the header ‘## Structured informal proof‘ containing the step-by-step proof.
- A subsequent section with the header ‘## Request skills‘ containing any requested relevant
lemmas or theorems
- Each requested skill is represented by an isabelle code block containing its formal definition




                                             18
Preprint




The P ROVER’s formalizer prompt was modified to re-enable Markdown formatting and to
emphasize the desired output format.

Formatting re-enabled
As a mathematician familiar with Isabelle, your task is to provide a formal proof in response
to a given problem statement.
Your proof should be structured and clearly written, meeting the following criteria:
- It can be verified by Isabelle.
- Each step of the proof should be explained in detail using comments enclosed in ”(*” and
”*)”.
- The explanation for each step should be clear and concise, avoiding any unnecessary or
apologetic language.
- You are **strongly encouraged** to create useful and reusable lemmas to solve the problem.
- The lemmas should be as general as possible (generalizable), and be able to cover a large
step in proofs (non-trivial).
- Your solution should be written within a Markdown isabelle code block. i.e., within a triple
back ticked code block, labelled as ”isabelle”
- You **MUST** copy the input lemma EXACTLY: **without changing whitespace**, without
paraphrasing, and without adding comments. - Within the code block, you must create a
new Isabelle ‘theory‘ containing the aforementioned input lemma copied from the input, as
well as your proof and any lemmas you created for the proof. Please ensure that your proof
is well-organized and easy to follow, with each step building upon the previous one.

The evolver prompts were likewise modified. The do request prompt (immediately below)
was particularly problematic as o3-mini tended to disregard the formatting instructions:

Formatting re-enabled
As a mathematician familiar with Isabelle, your task is to provide a formal proof in response
to a given formal statement.
Your proof should be structured and clearly written, meeting the following criteria:
- It can be verified by Isabelle.
- Please ensure that your proof is well-organized and easy to follow, with each step building
upon the previous one.
- THIS IS **CRITICAL**: YOUR PROOF **MUST** BE WRITTEN WITHIN A MARKDOWN
ISABELLE CODE BLOCK!!! i.e., within a triple back ticked code block, labelled as ”isabelle”

Note that you will be provided with several examples, but you should only complete the
last example (i.e., the example that does not have a formal proof).

{examples}

####################

# Statement:
“‘isabelle
{formal statement}
“‘

# Proof




                                             19
Preprint




Formatting re-enabled
As an expert mathematician who is proficient in Isabelle theorem proving, your task is to
modify the given lemma, theorem, function or definition given in the code to aid in solving
one or more of the problems provided. Your should accomplish this by Extend Dimensions:
If the problem is defined in a specific number of dimensions, consider if it would still hold
in more or fewer dimensions.
Your answer **MUST** be written within a Markdown isabelle code block. i.e., within a
triple back ticked code block, labelled as ”isabelle”

Here is some reference problems, you should evolve the skill to help solving theses
problems:
{problems}

Note that you will be provided with several examples, but you should only complete the
last example (i.e., the example that does not have a modified version).

############ Extend Dimensions ############
{examples}


####################
## Skill to evolve
“‘isabelle
{code}
“‘

## Evolved skill


Formatting re-enabled
As an expert mathematician who is proficient in Isabelle theorem proving, your task is to
modify the given lemma, theorem, function or definition given in the code to aid in solving
one or more of the problems provided. Your should accomplish this by ‘Identifying Key
Concepts‘: Extract the essential ideas, methods, or theorems that are critical to solving the
problem.
Your answer **MUST** be written within a Markdown isabelle code block. i.e., within a
triple back ticked code block, labelled as ”isabelle”

Here is some reference problems, you should evolve the skill to help solving theses
problems:
{problems}

Note that you will be provided with several examples, but you should only complete the
last example (i.e., the example that does not have a modified version).

############ Identifying key Concepts ############
{examples}


####################
## Skill to evolve
“‘isabelle
{code}
“‘

## Evolved skill




                                            20
Preprint




Formatting re-enabled
As an expert mathematician who is proficient in Isabelle theorem proving, your task is to
modify the given lemma, theorem, function or definition given in the code to aid in solving
one or more of the problems provided. Your should accomplish this by Parameterize: If the
problem involves specific numbers, generalize it by replacing these with variables.
Your answer **MUST** be written within a Markdown isabelle code block. i.e., within a
triple back ticked code block, labelled as ”isabelle”

Here is some reference problems, you should evolve the skill to help solving theses
problems:
{problems}

Note that you will be provided with several examples, but you should only complete the
last example (i.e., the example that does not have a modified version).

############ Parameterize ############
{examples}


####################
## Skill to evolve
“‘isabelle
{code}
“‘

## Evolved skill


Formatting re-enabled
As an expert mathematician who is proficient in Isabelle theorem proving, your task is to
modify the given lemma, theorem, function or definition given in the code to aid in solving
one or more of the problems provided. Your should accomplish this by Scale Complexity:
Try both simpler and more complicated versions of the problem to see how the approach
adapts.
Your answer **MUST** be written within a Markdown isabelle code block. i.e., within a
triple back ticked code block, labelled as ”isabelle”

Here is some reference problems, you should evolve the skill to help solving theses
problems:
{problems}

Note that you will be provided with several examples, but you should only complete the
last example (i.e., the example that does not have a modified version).

############ Scale Complexity ############
{examples}


####################
## Skill to evolve
“‘isabelle
{code}
“‘

## Evolved skill




                                           21
Preprint




D    Calculation of Cost

In our experiments we recorded the total token usage per run. I.e., if an experiment run
consisted of 100 attempts, then we recorded the cost of 100 attempts. However, to create
Table 5 we required the cost for a reduced number of attempts. To estimate this, we
determined the average cost per problem attempt. I.e., we calculated the total cost over all
runs and divided this by the total number of problem attempts over all runs. For example,
the 3 runs of the gpt-4o-mini experiment on the full test set used 100 attempts per problem
each; therefore, we divided the total cost of these 3 experiment runs by 300 to determine the
average cost per attempt.
Similarly, Figure 3 required the total expenditures up to the nth success, and we again
estimated this using the average cost per attempt. Specifically, we plotted ( x, y) points
where x was the cost of i attempts on all remaining problems, and y was the number of
problems solved after i attempts.
For further details, the code used to calculate Table 5 and plot Figure 3 is publicly available
in our GitHub repository.

E   Soft Use Score Examples

In this section we report examples of various retrieved lemmas and their soft use scores. The
example chosen (data/full data/test/amc12a 2021 p9.json) was generated in the first run
of gpt-4o-mini; it was selected as it has the largest range of soft use values.
The English description for this task is:

Which of the following is equivalent to (2 + 3)(22 + 32 )(24 + 34 )(28 + 38 )(216 + 316 )(232 +
332 )(264 + 364 )?
(A) 3127 + 2127     (B) 3127 + 2127 + 2 · 363 + 3 · 263 (C) 3128 − 2128     (D) 3128 + 2128
                     128
Show that it is (C) 3 − 2 . 128




                                              22
Preprint




The model output prior to correction by heuristics is reproduced below. Some lines have
been word wrapped to fit within margins.

theory amc12a_2021_p9
  imports Complex_Main
begin

lemma prod_sum_of_powers:
  fixes n :: nat
  shows "(\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) = (3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)"
proof (induction n)
  case 0
  then show ?case
     by auto
next
  case (Suc n)
  then have IH: "(\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
                                                    (3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)"
     by simp
  have "(\<Prod> k < Suc n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
                   (\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) * (2ˆ(2ˆn) + 3ˆ(2ˆn))"
     by (simp add: prod.atLeastLessThan_Suc)
  also have "... = ((3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)) * (2ˆ(2ˆn) + 3ˆ(2ˆn))"
     using IH by simp
  also have "... = 3ˆ(2ˆn) * 3ˆ(2ˆn) - 2ˆ(2ˆn) * 2ˆ(2ˆn)"
     by (simp add: algebra_simps)
  also have "... = 3ˆ(2ˆ(Suc n)) - 2ˆ(2ˆ(Suc n))"
     by (metis power2_eq_square power_Suc power_even_eq semiring_norm(3))
  finally show ?case by simp
qed

theorem amc12a_2021_p9 :
  shows "(\<Prod> k<7. (2ˆ(2ˆk) + 3ˆ(2ˆk))) = (3::nat)ˆ128 - 2ˆ128"
proof -
  have "(\<Prod> k<7. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
                                   (\<Prod> k<7. (2ˆ(2ˆk) + 3ˆ(2ˆk)))" by simp
  then have "(\<Prod> k<7. (2ˆ(2ˆk) + 3ˆ(2ˆk))) = (3::nat)ˆ(2ˆ7) - 2ˆ(2ˆ7)"
    using prod_sum_of_powers[of 7] by simp
  then have "(\<Prod> k<7. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
                                    (3::nat)ˆ(128) - 2ˆ(128)" by simp
  thus ?thesis by simp
qed

end




                                          23
Preprint




The following retrieved lemma provided to the P ROVER when generating the solution above
attained a soft use score of 0.378. It is largely irrelevant, as it is specialized to a function that
does not appear in this problem.

definition f :: "nat \<Rightarrow> nat" where
  "f x = 4ˆx + 6ˆx + 9ˆx"

lemma f_12k_plus_9:
  fixes k :: nat
  shows "f (12 * k + 9) = 4ˆ(12 * k + 9) + 6ˆ(12 * k + 9) + 9ˆ(12 * k + 9)"
proof -
  have "f (12 * k + 9) = 4ˆ(12 * k + 9) + 6ˆ(12 * k + 9) + 9ˆ(12 * k + 9)"
    by (simp add: f_def)
  thus ?thesis by simp
qed

The following retrieved lemmas provided to the P ROVER when generating the solution
above attained soft use scores of 0.695 and 0.706 respectively. They are more relevant,
involving powers of powers, but are again overly specialized and the proof tactics used
(simp add: power add, simp add: power2 eq square, etc...) are not used in the P ROVER’s
outputted solution. Note that the LEGO-Prover’s E VOLVER often produces minor variations
of the same lemma as seen in this case.

lemma power_computation:
  fixes k :: nat
  shows "kˆ12 = (kˆ6)ˆ2"
proof -
  have "kˆ12 = kˆ(6 + 6)" by simp
  also have "... = kˆ6 * kˆ6" by (simp add: power_add)
  also have "... = (kˆ6)ˆ2" by (simp add: power2_eq_square)
  finally show ?thesis by simp
qed

lemma power_computation:
  fixes k :: nat
  shows "kˆ12 = (kˆ6)ˆ2"
proof -
  have "kˆ12 = kˆ(6 + 6)" by simp
  also have "... = (kˆ6)ˆ2" by (simp add: power_add)
  finally show ?thesis .
qed




                                                 24
Preprint




The following retrieved lemma provided to the P ROVER when generating the solution above
attained a soft use score of 0.96. Note that some lines are word wrapped to fit within the
margins. It is reproduced almost exactly in the P ROVER’s output, with minor changes to
parenthesization and the name of the lemma.

lemma sum_of_powers:
  fixes n :: nat
  shows "(\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) = (3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)"
proof (induction n)
  case 0
  then show ?case
     by auto
next
  case (Suc n)
  then have IH: "(\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
                                                (3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)"
     by simp
  have "(\<Prod> k < Suc n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) =
               (\<Prod> k < n. (2ˆ(2ˆk) + 3ˆ(2ˆk))) * (2ˆ(2ˆn) + 3ˆ(2ˆn))"
     by (simp add: prod.atLeastLessThan_Suc)
  also have "... = ((3::nat)ˆ(2ˆn) - 2ˆ(2ˆn)) * (2ˆ(2ˆn) + 3ˆ(2ˆn))"
     using IH by simp
  also have "... = (3ˆ(2ˆn) * 3ˆ(2ˆn)) - (2ˆ(2ˆn) * 2ˆ(2ˆn))"
     by (simp add: algebra_simps)
  also have "... = 3ˆ(2ˆ(Suc n)) - 2ˆ(2ˆ(Suc n))"
     by (metis power2_eq_square power_Suc power_even_eq semiring_norm(3))
  finally show ?case by simp
qed




                                           25
