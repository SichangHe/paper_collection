Journal of Intelligent Information Systems (2026) 64:2545–2568
https://doi.org/10.1007/s10844-026-01071-6

RESEARCH



GradeSQL: Outcome reward models for intelligent Text-to-
SQL generation from LLMs

Mattia Tritto1 · Giuseppe Farano1 · Dario Di Palma1 · Gaetano Rossiello2 ·
Dharmashankar Subramanian2 · Fedelucio Narducci1 · Tommaso Di Noia1

Received: 9 February 2026 / Revised: 21 June 2026 / Accepted: 22 June 2026 /
Published online: 7 July 2026
© The Author(s) 2026


Abstract
As Large Language Models (LLMs) become foundational to next-generation Intelligent
Information Systems, the bridge between natural language interfaces and structured data-
base systems remains a critical bottleneck. While Text-to-SQL generation enables coop-
erative support for complex query formulation, ensuring the reliability of these generated
queries at inference time is a central challenge. Conventional methods rely on coarse
execution-based signals, which may limit their ability to capture the nuanced semantic
alignment required for high-stakes database environments. In this work, we propose the
use of Outcome Reward Models (ORMs) as a fine-grained, probabilistic feedback mecha-
nism for test-time verification in Text-to-SQL tasks. We introduce GradeSQL, a frame-
work for training task-specific ORMs that assign scalar utility scores to candidate SQL
queries based on their semantic correctness and alignment with database schema. Our
approach is evaluated on the BIRD and Spider benchmarks across multiple open-source
LLM families. Experimental results demonstrate that ORM-based verification consistently
outperforms traditional execution-based heuristics.

Keywords Large language models (LLMs) · Text-to-SQL · Outcome reward models
(ORMs) · Natural language interfaces to databases (NLIDB) · Test-time verification ·
Knowledge-directed inference



1 Introduction

Text-to-SQL, the task of translating Natural Language (NL) questions into executable SQL
queries, facilitates the use of data management systems and represents a step toward democ-
ratizing database access (Kim et al., 2020), enabling both expert and non-expert users to
interact with complex database systems through NL (Androutsopoulos et al., 1995; Liu et
al., 2025).



Mattia Tritto, Giuseppe Farano and Dario Di Palma are authors contributed equally to this work.

Extended author information available on the last page of the article
2546                                    Journal of Intelligent Information Systems (2026) 64:2545–2568


    Early approaches were predominantly rule-based, relying on manually crafted rules and
heuristics to map NL questions to SQL queries (Li and Jagadish, 2014). While often capable
of generating syntactically correct queries, these systems struggled with challenges such as
nested clauses, co-references, and complex aggregations (Hong et al., 2025).
    The field progressed with the adoption of neural network-based techniques (Xiao et
al., 2016; Bogin et al., 2019), which improved intent recognition and semantic parsing.
This was followed by the introduction of Pre-trained Language Models (PLMs) such as
BERT (Devlin et al., 2019), and T5 (Raffel et al., 2020), which achieved competitive results
across various benchmarks (Li et al., 2023, 2023a). Nevertheless, PLM-based systems still
face difficulties with schema generalization and complex queries (Liu et al., 2025).
    Recently, the advent of Large Language Models (LLMs) has introduced a new paradigm
in Text-to-SQL. LLMs demonstrate strong emergent capabilities that surpass PLMs across
diverse NLP tasks (Kumar, 2024), and they currently dominate research in this area, as
demonstrated by the works introduced by Pourreza and Rafiei (2023); Gao et al. (2023);
Zhang et al. (2024). Nevertheless, LLMs still face challenges in generating correct SQL for
complex queries involving multi-table joins, nested subqueries, and sophisticated aggre-
gations (Ma et al., 2024; Kanburoğlu Ab and Tek F, 2024). To address these limitations,
researchers are exploring techniques such as prompt engineering (Gao et al., 2023), multi-
agent frameworks (Wang et al., 2025; Askari et al., 2025), and fine-tuning (Qin et al., 2025).
While these approaches have driven notable advances, achieving further improvements
remains challenging due to the inherent complexity of the task, and even minor gains repre-
sent substantial progress (Gao et al., 2023).
    Inspired by recent advances in mathematical reasoning with LLMs, such as in Zhang et
al. (2025), the research community is increasingly investigating test-time inference strate-
gies, which allocate additional computational resources at inference to enhance output qual-
ity (Brown et al., 2024; Li et al., 2025; He et al., 2025). These strategies typically generate
multiple candidate outputs and apply heuristics to select the best one, leveraging the ability
of LLMs to produce correct answers when afforded more inference time rather than larger
model size or additional training (Xie et al., 2025). Common approaches include Best-of-N
(BoN), such as Cobbe et al. (2021), which samples N outputs and selects the highest-scoring
candidate, and Majority Voting (Maj) (Sheng and Shuai, 2025), which chooses the most
frequently generated output based on execution equivalence. Specifically, the study intro-
duced by Sheng and Shuai (2025) investigates the application of test-time compute scaling
to the Text-to-SQL task via Majority Voting. Through an empirical evaluation of various
generation budgets, they determined that N = 32 represents the optimal trade-off between
task performance and computational efficiency. However, these methods typically provide
discrete, coarse-grained signals. For instance, Majority Voting relies on the frequency of
execution results, while execution-based BoN treats all executable queries that return non-
empty sets with equal weight. In this work, we look toward ORMs to provide a continu-
ous, probabilistic assessment of semantic quality, allowing for a more nuanced ranking of
candidate outputs. In particular, the Reinforcement Learning (RL) community has proposed
Outcome Reward Models (ORMs), which assign fine-grained semantic correctness scores
to candidate outputs (Sheng and Shuai, 2025). When used as reward functions in RL loops,
ORMs improve the alignment between model predictions and user intent (Havrilla et al.,
2024), highlighting their potential as principled verifiers of model output. This naturally
raises the question: can ORMs also enhance test-time inference strategies? In particular,


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                         2547


integrating ORMs into BoN offers a way to move beyond frequency- or execution-based
heuristics, enabling candidate selection grounded in semantic correctness. Although BoN
and Maj have already been applied to Text-to-SQL by Li et al. (2025), the use of ORMs in
test-time inference remains largely unexplored, hindered by the scarcity of reward-labeled
data and the absence of clear methodological guidelines. Moreover, no systematic evalua-
tion has yet compared ORM-guided selection with traditional test-time compute strategies,
leaving open the potential of ORMs as a more robust heuristic for BoN.
    To address these limitations, we first introduce a scalable data synthesis framework
tailored for Outcome Reward Models in the Text-to-SQL setting, which automates data
generation to mitigate data scarcity and enables the development of task-specific ORMs.
Building on this foundation, we present a comprehensive evaluation of ORM-guided Best-
of-N, benchmarking it against execution-based BoN and Majority Voting.
    To evaluate the effectiveness of our approach, we conduct a comprehensive study using
open-source LLMs in an end-to-end Text-to-SQL setup. Our results demonstrate that ORMs
consistently outperform both execution-based Best-of-N and Majority Voting, achieving
execution accuracy gains of up to +4.33% on BIRD and +2.10% on Spider over ex-BoN,
and +2.91% (BIRD) and +0.93% (Spider) over Maj.
    In summary, our work makes the following contributions:

● Scalable Data Synthesis and ORM Training: We introduce a framework to synthesize
  high-quality annotated datasets for ORM fine-tuning, overcoming data scarcity in Text-
  to-SQL reward modeling.
● Extensive Empirical Evaluation and Analysis: We conduct a large-scale study across
  LLM families and parameter sizes, analyze test-time efficiency under candidate scaling,
  and provide controlled ablations on prompt design, model scale, and training losses.
● Open-Source Resources: We release our codebase, synthesized datasets, and fine-tuned
  ORMs on GitHub and Hugging Face to promote reproducibility and future research.


2 Related work

In this section, we trace the evolution of Text-to-SQL solutions, review test-time inference
strategies, and conclude with an overview of existing data-augmentation frameworks for
Text-to-SQL.

2.1 Text-to-SQL meets LLMs

Text-to-SQL refers to the task of translating Natural Language (NL) questions into execut-
able SQL queries, serving as a bridge between human intent and structured data access. Its
development spans more than five decades, evolving from early handcrafted systems to
today’s approaches powered by Large Language Models (LLMs) (Hong et al., 2025).
   The earliest systems were entirely rule-based, relying on domain-specific grammars and
manually engineered parsing rules. A seminal example is LUNAR (Woods W, 1972), which
answered questions about lunar rock samples using an Augmented Transition Network
parser combined with procedural semantics.




                                                                                 13
2548                                    Journal of Intelligent Information Systems (2026) 64:2545–2568


    The mid-2010s marked a paradigm shift with the advent of deep learning. Neural seman-
tic parsers were capable of jointly modeling questions and database schemas, but progress
was constrained by the lack of large-scale labeled datasets (Kim et al., 2020). A break-
through came with the release of Spider (2018) (Yu et al., 2019), which provided bench-
marks for cross-domain generalization. Building on these datasets, Pre-trained Language
Models (PLMs) such as BERT (Devlin et al., 2019) and T5 (Raffel et al., 2020) catalyzed
the development of schema-aware neural parsers. RAT-SQL (Wang et al., 2020), for exam-
ple, integrated relation-aware transformers with pre-trained embeddings to significantly
improve schema linking, i.e., mapping question terms to database elements.
    The advent of LLMs such as GPT (Openai et al., 2024), Llama (Grattafiori et al., 2024),
and PaLM (Anil et al., 2023) has further transformed the landscape. Few-shot prompting
strategies, such as DIN-SQL (Pourreza and Rafiei, 2023), decompose the task into subtasks
to improve accuracy, though performance still degrades on highly complex queries. Building
on these advances, recent research increasingly frames Text-to-SQL as a reasoning problem.
Rather than treating query generation as a single-shot task, approaches leverage LLMs for
multi-step decomposition, error correction, and domain adaptation. Pipelines often decom-
pose the task into components such as schema linking, query generation, refinement, and
selection, orchestrated through prompt engineering or fine-tuning (Hong and Yuan, 2024;
He et al., 2025). Some frameworks adopt multi-agent designs (Askari et al., 2025), while
others focus on scaling SQL-specific training data (Li et al., 2025). Current trends empha-
size expanding reasoning capacity (Gao et al., 2023; Rossiello et al., 2025), and integrating
domain knowledge (Li et al., 2023b; Xu et al., 2026).
    Despite this rapid progress, the intrinsic complexity of Text-to-SQL continues to limit
accuracy, especially on queries requiring multi-table joins, nested subqueries, and sophis-
ticated aggregations. These challenges have sparked growing interest in test-time inference
strategies, which allocate additional computational resources at inference time to enhance
output quality (Li et al., 2025; He et al., 2025).

2.2 Test-time inference strategies

Test-Time Inference (TTI), also known as inference-time scaling or test-time computation,
refers to strategies that improve LLM outputs by allocating additional computation dur-
ing inference without modifying model parameters (Snell et al., 2024). Nowadays, LLMs
generate text by sequentially predicting tokens, with decoding strategies that determine
which token to produce at each step. Early approaches relied on deterministic methods such
as greedy decoding (Chickering, 2002) or beam search (Tillmann and Ney, 2003), which
maximized sequence likelihood but often produced repetitive outputs with limited diver-
sity (Wiher et al., 2022). To address this, later research introduced stochastic decoding algo-
rithms, including temperature scaling, top-k sampling (Fan et al., 2018), and nucleus (top-p)
sampling (Holtzman et al., 2020), which add controlled randomness by sampling from trun-
cated distributions. Although effective in improving local variability, these methods operate
only at the token level and thus cannot substantially improve the correctness of full outputs,
leaving the system vulnerable to the danger of LLM hallucinations (Li et al., 2026).
    Building on this idea, commonly adopted methods such as Best-of-N (BoN) and
Majority Voting (Maj) have emerged (Snell et al., 2024). BoN selects the candidate with
the highest score according to a heuristic function, such as model likelihood (Holtzman et


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                          2549


al., 2020) or execution accuracy (Chen et al., 2022), while Maj chooses the most frequent
final answer among diverse samples (Wang et al., 2023). These approaches are attractive
because they require no retraining, but they also inherit critical limitations: BoN tends
to over-prefer generic high-probability outputs (Li et al., 2023), while Maj can fail when
correct solutions are underrepresented (Wang et al., 2023; Huang et al., 2025). This
motivated the development of verification-guided selection methods, which go beyond
traditional heuristics by introducing an explicit verifier to score or filter candidates (Yi
and Chen, 2025).
    A major advancement in this direction came with reward models. Process Reward
Models (PRMs) (Khalifa et al., 2025) evaluate intermediate reasoning steps but require
costly step-level supervision. In contrast, Outcome Reward Models (ORMs) score only
final outputs, avoiding intermediate annotation. The use of Outcome Reward Models
(ORMs) for verification was pioneered by Cobbe et al. (2021) in the context of multi-
step mathematical reasoning. Commonly with our work, they propose a generator-verifier
framework that uses Best-of-N sampling to rank model outputs based on a predicted
probability of correctness. However, GradeSQL differs significantly in its application
to the Text-to-SQL domain. While the math verifier in the work (Cobbe et al., 2021)
checks for numeric equality, GradeSQL must assess the semantic alignment between a
natural language prompt, a structured database schema, and the resulting SQL execution.
In Text-to-SQL, ORMs are particularly appealing because they can semantically evaluate
SQL queries independently of the generator. This enables the selection of high-quality
but underrepresented candidates (Borchmann and Wydmuch, 2025; He et al., 2025), a
capability missing in Maj, while also identifying semantically equivalent but syntactically
different queries. These properties make ORMs a natural fit for re-ranking diverse
candidate sets and for modular system designs where generation and verification can be
optimized independently.
    Despite these advances, to the best of our knowledge, no prior work has directly adapted
and scaled the ORM-based verifier training framework specifically for the Text-to-SQL task
domain, where datasets must support fine-grained outcome scoring across diverse candidate
outputs rather than solely boosting general SQL generation performance. This gap under-
scores the need for new methodologies that explicitly target ORM development.


3 Methodology

3.1 Problem formulation

Given a natural language question qi ∈ Q, where Q denotes the set of all questions, the
Text-to-SQL task aims to map qi and its corresponding database schema Σi (a collection of
tables with their columns) into a valid SQL query ygoldi ∈ Ygold (Baek et al., 2025; Dai et
al., 2025).
    While the traditional formulation focuses on generating a single query, in the context
of test-time inference the process is extended to consider multiple candidates. Specifically,
given qi , an LLM generates a pool of N candidate queries

                                 Ycandidate = {c1 , c2 , . . . , cN },



                                                                                  13
2550                                      Journal of Intelligent Information Systems (2026) 64:2545–2568


from which either a heuristic or a verifier must identify the candidate cj ∈ Ycandidate that
best corresponds to the ground-truth gold query. In this work, we define the verifier as an
Outcome Reward Model (ORM).
   Formally, the ORM is a scoring function ϕ(qi , cj ) that maps a natural language question
qi and a candidate SQL query cj ∈ Ycandidate to a probabilistic score:

                                     ϕ(qi , cj ) ∈ [0, 1],

where higher scores indicate a greater likelihood that the query is correct. The ORM thus
induces a ranked list of candidate SQL queries, with the best candidate c∗ selected as the
one achieving the highest score:

                          c∗ = *arg maxcj ∈Ycandidate ϕ(qi , cj ).

Training an ORM as a scoring function for candidate ranking introduces two central chal-
lenges: (i) constructing datasets that explicitly identify which candidate cj is correct, and (ii)
assigning relative scores to multiple candidates in a way that faithfully reflects user intent.
    To overcome these challenges, we leverage the LLM’s internal ability to self-assess (Liu
et al., 2024; Huang et al., 2024; Li and Ea, 2024) query correctness. Specifically, we prompt
the model to classify each candidate as “Yes” (correct) or “No” (incorrect), and then extract
the associated logits. These logits are used during training to supervise the ORM, enabling
it to learn a probabilistic scoring function that generalizes to ranking candidates at inference
time.
    In the following, we present the GradeSQL framework, which implements this idea by
constructing and training ORMs specifically designed for test-time inference in the Text-to-
SQL setting.

3.2 GradeSQL framework

Given a Text-to-SQL dataset D = {(qi , ygoldi )}ni=1 , where qi is a natural language question
and ygoldi its corresponding gold SQL query, our framework (Fig. 1) comprises three stages:
(i) Candidates generation, (ii) Data labeling, and (iii) Supervised Fine-Tuning (SFT). The
overall objective is to train an Outcome Reward Model (ORM) tailored to the target dataset.

Stage 1: Candidate generation For each question qi , we employ an LLM, referred to as the
generator G , to produce a set of N candidate SQL queries.

   Formally, let qi denote a natural language question and Σi the corresponding database
schema. The generator G(qi , Σi ) produces N candidate SQL queries:

             Ycandidate = {SQL1 , SQL2 , . . . , SQLN } = {c1 , c2 , . . . , cN }.



Stage 2: Data labeling Once candidates are generated, the next step is to determine which
of them correctly capture the intent of qi . Let R(cj ) denote the execution result of a query
cj , i.e., the set of tuples returned when cj is executed on the target database. A candidate


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                        2551




Fig. 1 Overview of the GradeSQL framework for training an ORM. The framework consists of three
stages: (i) Candidate Generation, an LLM generates N SQL queries via a Chain-of-Thought (CoT)
prompt, then removes the CoT trace; (ii) Data Labeling, each candidate is annotated as correct or incor-
rect; and (iii) Supervised Fine-Tuning (SFT), the base LLM is fine-tuned with LoRA on the labeled data
to obtain the final ORM



cj ∈ Ycandidate is labeled as correct if its result set matches that of the gold query ygoldi ,
i.e., R(cj ) = R(ygoldi ).

  Candidates are labeled as incorrect if they fail to capture the intended semantics. This
may occur in two cases:

1. Semantic mismatch: The query executes successfully but returns a different result set
   from the gold query, i.e., R(cj ) ̸= R(ygoldi ).
2. Execution error: The query contains syntactic or runtime errors that cause the database
   management system (DBMS) to fail during execution.

Since execution errors are trivial to detect, the framework primarily focuses on distinguish-
ing semantically correct queries from incorrect but executable ones. This process is formal-
ized by the labeling function ℓ(ci ):
                         {
                             correct (Yes)       if R(cj ) = R(ygoldi ),
              ℓ(cj ) =       incorrect (No)      if R(cj ) ̸= R(ygoldi ),
                             discarded           if cj raises an execution error.


Stage 3: Supervised fine-tuning The labeled candidates form a training set
Dlabel = {(ci , li )}ni=1 , where ci is a candidate SQL query and li ∈ {Yes, No} indicates cor-
rectness. At this stage, the verification task is cast as an autoregressive binary classification
problem.




                                                                                              13
2552                                    Journal of Intelligent Information Systems (2026) 64:2545–2568


   Formally, let x = Prompt(Σ, q, c) denote the input sequence constructed from the data-
base schema Σ, the natural language question q, and the candidate SQL query c. The label
l ∈ {Yes, No} specifies whether c semantically satisfies q under Σ. The model is trained to
autoregressively generate the next token: “Yes” if correct and “No” otherwise.
   We fine-tune the causal LM head as a verifier using Low-Rank Adaptation (LoRA)
under the causal language modeling objective (Radford and Wu, 2019). Given the input
x = Prompt(Σ, q, c), we append the label l ∈ {Yes, No} to obtain the target sequence
s = [ x; l ]. During training, the model conditions on s and is optimized to minimize the
negative log-likelihood:

                                        |s|
                                        ∑
                           L(θ) = −           log Pθ (st | s<t ) .
                                        t=1



This objective guides the model, when presented with a structured input x = Prompt(Σ, q, c)
, to autoregressively generate the correct label token l ∈ {Yes, No}.

3.3 ORM inference and probabilistic scoring mechanism

At inference time, the verifier assigns a probabilistic score to each candidate SQL query,
reflecting its likelihood of being semantically correct. This is achieved by prompting the
fine-tuned LLM in an autoregressive setting to generate a single verification token, either
“Yes” or “No”. Rather than treating this prediction as a discrete token-level decision, we
instead use the model’s logit corresponding to the “Yes” token, normalized into [0, 1], as
a continuous confidence score. In this way, the ORM functions not merely as a classifier
but as a ranking mechanism over candidate queries. A visual representation of the inference
process is provided in Fig. 2.

3.3.1 Autoregressive verification

Formally, for a given prompt x = Prompt(Σ, q, c), constructed from the schema Σ, natural
language question q, and candidate query c, the model defines a conditional distribution:

                             P (y | x; θ),    y ∈ {Yes, No},

where θ are the model parameters. The verifier’s score for candidate c is then:

                              Score(c) = P (yyes | x; θ).

This formulation avoids hard decision boundaries, instead producing a real-valued confi-
dence score that can be directly used to rank candidates.

3.3.2 Motivation for probabilistic scoring

Framing ORM inference in terms of probabilities provides two key advantages for Text-to-
SQL verification:


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                       2553




                                                             Candidate Queries           Scores
                                                           SELECT ID FROM pilots          0.9

                                                            SELECT * FROM pilots          0.4



                                                             SELECT name FROM
                                                                                          0.1
                                                                    pilots




                         Final N SQL
                         candidates


Fig. 2 Overview of the GradeSQL ORM at inference. The pipeline consists of two stages: (i) Candidate
Generation, where an LLM produces a pool of N SQL candidates; and (ii) Query Selection, where the
ORM scores each candidate and ranks them, selecting the query with the highest probability as the final
output


1. Fine-grained calibration: Scores capture nuanced differences in semantic plausibility,
   even among syntactically valid queries.
2. Differentiable ranking: The continuous nature of the scores enables consistent ordering
   of candidates, avoiding the brittleness of binary thresholding.

By interpreting the verifier as a probabilistic scoring function rather than a binary classi-
fier, the ORM offers a mechanism for ranking candidate SQL queries by their semantic
correctness.


4 Experimental setup


Datasets To evaluate our approach, we use two widely adopted Text-to-SQL benchmarks:
Spider (Yu et al., 2019) and BIRD (Li et al., 2023b). Both are cross-domain benchmarks
with disjoint databases across train/dev/test splits to assess generalization. On Spider, we
construct the labeled dataset from the training questions, train the ORM, and evaluate it on
the dev and test sets. On BIRD, we adopt the same setup, using the training questions to
build the dataset and train the ORM, but, due to the hidden test set, evaluate only on the
dev set.


                                                                                                13
2554                                         Journal of Intelligent Information Systems (2026) 64:2545–2568


Metrics To ensure fair comparison across methods, we adopt the official evaluation metrics
defined for BIRD (Li et al., 2023b), which are also applicable to Spider. Let Qtest denote the
set of evaluation questions. For each question qi ∈ Qtest , let c∗i be the predicted SQL query
and ygoldi the corresponding gold query.

  Execution Accuracy (EX) measures the proportion of questions for which the predicted
and gold queries return identical result sets:

                                1         ∑
                     EX =                           1(R(c∗i ) = R(ygoldi )) ,
                             |Qtest |
                                        qi ∈Qtest


where 1(·) is the indicator function, returning 1 if the condition holds and 0 otherwise.
   Pass@N (Ma et al., 2024) evaluates the proportion of questions for which at least one of
the N predicted candidates returns the correct result set:
                                                    (N                          )
                               1          ∑          ∨
                Pass@N =                            1         R(cj ) = R(ygoldi ) ,
                            |Qtest |
                                        qi ∈Qtest       j=1


       ∨
where denotes the logical OR across N candidates. Specifically, the prediction is consid-
ered correct if any of the N candidates for question qi yield the same result set as the ground
truth ygoldi .

Baselines We benchmark the ORM-based test-time inference (TTI) against two TTI strate-
gies widely used in Text-to-SQL and code generation tasks: Majority Voting and execution-
based Best-of-N. Both methods select a single SQL query from the generated pool without
relying on gold references, but differ in how they aggregate candidates.

Majority voting Majority Voting selects the most plausible SQL query based on execution
equivalence (Sheng and Shuai, 2025). Each candidate query is executed on the target data-
base, and queries producing identical result sets are grouped into k clusters. The class with
the largest cardinality is selected, and the final query is sampled uniformly from it. For-
mally, let Ycandidate = {c1 , c2 , . . . , cN } be the set of candidates. We define

                         ci ∼ cj if andonlyif R(ci ) = R(cj ),

which partitions Ycandidate into k clusters C1 , . . . , Ck . Majority Voting then selects the
cluster with the largest cardinality and samples one candidate from it. This method is
robust to surface-level variations and has been widely adopted in the literature, including
BIRD (Li et al., 2023b).

Execution-based Best-of-N Best-of-N selects the most promising candidate based on an
execution-level heuristic (Chen et al., 2022). Given Ycandidate = {c1 , . . . , cN }, the heuris-
tic h : Ycandidate → [0 , 1 ] considers two signals: (i) executability (whether the query runs
without errors), and (ii) non-emptiness (whether it returns at least one row). The scoring
function is:




13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                2555

Table 1 Reproducibility results of OmniSQL-7B. Maj = Majority Voting (T = 0.8, N = 8); Gre = Greedy
decoding (N = 1)
               BIRD dev                        Spider dev                     Spider test
               Maj                Gre          Maj            Gre             Maj            Gre
Our            66.95              64.41        83.95          82.11           85.61          84.49
Origin         66.10              63.90        81.60          81.20           88.90          87.90

                           {
                               0     if ci isnotexecutable,
                h(ci ) =       0.5   if ci executesbutreturns0rows,
                               1     if ci executesandreturnsatleastonerow.

The final query c ∗ is selected uniformly from the subset of candidates that achieve the
highest score.
   While this efficiently filters invalid queries, it provides only coarse discrimination: mul-
tiple queries may achieve the same maximal score while differing in semantic correctness.
This limitation motivates our ORM-based extension of Best-of-N.

ORMs and evaluation setup To evaluate ORM-based Best-of-N, we adopt OmniSQL-7B (Li
et al., 2025) as the generator, which, at the time of writing, is the most capable open-source
7B model trained specifically for the Text-to-SQL task. For each input question, OmniSQL
produces N candidate queries, which are then re-ranked by three strategies: Majority Voting,
execution-based Best-of-N, and ORM-based Best-of-N.

   Before integration, we validated OmniSQL through a reproducibility study on Spider
and BIRD. As shown in Table 1, our reproduced results closely match those of the original
work, with deviations of at most 1% on BIRD dev and within +3% on Spider dev. This
confirms the robustness of OmniSQL and justifies its use as our base generator, particularly
in combination with ORM re-ranking.

Reproducibility details All experiments were conducted on compute nodes with Intel Xeon
8358 CPUs (32 cores, 2.6 GHz), 512 GB RAM, and 4 NVIDIA A100 SXM4 GPUs (64 GB).
SQL candidates were generated via vLLM using the OmniSQL setup (Li et al., 2025), with
ORM inference through Hugging Face transformers. Runs used a fixed seed of 42.
Code1, datasets2, and models3 are publicly available.


5 Results and discussion

We evaluated our framework on seven models: Qwen2.5-1.5B-Instruct, Qwen2.5-7B-Instruct,
Granite-3.3-2B-Instruct, Granite-3.3-8B-Instruct, Llama-3.2-1B-Instruct, Llama-3.1-8B-
Instruct, and OmniSQL-7B. Benchmarks were conducted on the BIRD dev (1,534 samples),
Spider dev (1,034 samples), and Spider test (2,147 samples) splits. For both the BIRD and Spi-
der datasets, we began with the original training sets of 9,428 queries (BIRD) and 9,000 queries


1
    GradeSQL Framework
2
    GradeSQL Training Datasets
3
    Pretrained GradeSQL ORMs


                                                                                       13
2556                                         Journal of Intelligent Information Systems (2026) 64:2545–2568


(Spider). After light pre-processing to remove duplicates and reduce redundancy, we obtained
9,411 queries for BIRD and 8,960 for Spider. For each question, OmniSQL-7B was used to gen-
erate N = 32 candidate SQL queries. We selected N = 32 following Li (2025), as it represents
a well-balanced trade-off between performance and computational cost (Lewkowycz, 2022;
Wang et al., 2023). A comprehensive analysis of these trade-offs is provided by Chung and
Hsiao (2025), who demonstrated that in mathematical reasoning tasks, performance gains are
primarily concentrated between N = 2 and N = 32. Beyond this range, the authors observed
diminishing returns, with performance improvements reaching a distinct plateau. The frame-
work automatically discards syntactically invalid queries and labels each remaining candidate
as correct (s+ ) or incorrect (s− ) depending on whether its result set matches the gold SQL. This
procedure yielded final labeled datasets of 82,640 samples for BIRD and 50,073 for Spider.
   Analyzing these datasets reveals a marked class imbalance. In Spider, 69.4% of the can-
didates are labeled correct, while only 30.6% are incorrect. BIRD shows a milder skew,
with 58.63% correct and 41.37% incorrect. To investigate the impact of imbalance on ORM
training, we constructed balanced versions of both datasets by downsampling. Specifically,
for each question, we retained min(s+ , s− ) candidates, ensuring a 50/50 split between posi-
tive and negative labels. The resulting statistics are summarized in Table 2.
   With these datasets prepared, we proceed to train ORMs on the seven selected models to
address three main research questions:
RQ1        Are ORMs consistently trainable across heterogeneous model families?
RQ2        How does dataset balancing influence ORM performance?
RQ3        How effective is the best ORM compared to Majority Voting and execution-based
BoN?

RQ1 – Cross-family trainability of ORMs Table 3 reports ORM performance on BIRD and
Spider using the unbalanced training set, across Granite, Llama, Qwen, and OmniSQL
backbones. The trained ORMs exhibit tightly clustered scores: Bird dev ranges from

Table 2 Dataset statistics for                                       BIRD (train)          Spider (train)
BIRD and Spider (training splits)
                                    Questions
                                       # (pre)                       9,428                 9,000
                                       # (post)                      9,411                 8,960
                                       Removed ∆ (%)                 17 (0.18%)            40 (0.44%)
                                    Labeled sets
                                       Imbalanced size               82,640                50,073
                                       Class split (% inc/cor)       41.37 / 58.63         30.60 / 69.40
                                       Balanced size (50/50)         30,686                17,834



Table 3 ORM performance             ORM Model                    BIRD dev     Spider dev      Spider test
on BIRD and Spider with the
                                    Granite-3.3-2B-Instruct      66.88        82.79           85.14
unbalanced dataset, reporting
Execution Accuracy (%) on dev       Granite-3.3-8B-Instruct      68.25        84.42           86.91
and test sets                       Llama-3.2-1B-Instruct        67.67        84.04           86.31
                                    Llama-3.1-8B-Instruct        68.32        82.30           85.89
                                    Qwen2.5-1.5B-Instruct        68.12        84.33           86.17
                                    Qwen2.5-7B-Instruct          68.58        84.33           86.91
                                    OmniSQL-7B                   68.64        84.42           86.63


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                        2557


66.88 to 68.64, Spider dev from 82.30 to 84.42, and Spider test from 85.14 to 86.91.
These close score range shows ORMs train reliably across LLM families.

   A closer look reveals three key patterns. The first is that the scale effect is modest: larger
variants such as Granite-3.3-8B or Qwen2.5-7B yield only small improvements (typically
below two points) over their smaller counterparts, suggesting that ORM effectiveness is not
strongly tied to parameter count. The second is family-agnostic generalization: each family
contributes at least one competitive ORM, for instance, Granite-3.3-8B and Qwen2.5-7B
rank at the top of the Spider test, while Llama and OmniSQL models perform comparably
on both development and test splits. This indicates that architectural heterogeneity does
not hinder successful ORM training. The third is the stability of rankings across splits and
datasets: although Spider generally achieves higher EX Accuracy than BIRD, the relative
orderings remain consistent, supporting the robustness of ORMs across evaluation settings.
   Overall, these findings demonstrate that ORMs are consistently trainable across hetero-
geneous LLM families and scales, achieving comparable accuracies with minimal variance.
This establishes their generality and motivates the use of any backbone family in the subse-
quent experiments, RQ2, which investigates the effect of dataset balancing, and RQ3, which
benchmarks ORM performance against test-time baselines.

RQ2 – The role of dataset balancing Table 4 compares ORM performance on BIRD dev,
Spider dev, and Spider test when trained on the Unbalanced versus Balanced datasets. Each
cell reports accuracy before and after balancing, with the difference ∆ highlighted in green
(↑) for improvements and red (↓) for drops.

   The results reveal a nuanced picture: balancing leads to both gains and losses depend-
ing on the backbone and dataset. On BIRD dev, several backbones exhibit small decreases,
e.g. Qwen2.5-1.5B at −0.84 and Qwen2.5-7B at −0.39, while Granite-3.3-8B (+0.13) and

Table 4 Execution accuracy (%) of ORM models on BIRD dev, Spider dev, and Spider test. Each cell shows
results on Unbalanced (Unbal.) and Balanced (Bal.) sets with ∆ (green ↑ = gain, red ↓ = drop). Ordered by
BIRD Unbalanced; best in bold, runner-up underlined




                                                                                              13
2558                                          Journal of Intelligent Information Systems (2026) 64:2545–2568


OmniSQL-7B (+0.26) show slight improvements. On Spider dev, the effect is more mixed:
Llama-3.1-8B improves substantially (+1.81), whereas others decline moderately, such as
Qwen2.5-1.5B (−0.77), or remain unchanged, as with Granite-3.3-2B (0.00). By contrast,
Spider test shows more consistent gains, with the largest improvements for Llama-3.1-8B
(+1.07), OmniSQL-7B (+0.84), and Llama-3.2-1B (+0.23).
    Overall, on Spider balancing appears to enhance generalization. While accuracy on the
development set fluctuates, on the test set balancing lead an overall improvements for the
majority of the models. The effect is particularly notable for Llama-3.1-8B and OmniSQL-
7B, where gains exceed +1.0 and +0.8 points. At the same time, the overall relatively
small magnitude of changes (generally within ±1.2) suggests that ORMs remain stable even
under skewed distributions of labels.
    Furthermore, as shown in Table 2, the number of training samples differs substantially:
the imbalanced sets contain over 80k (BIRD train) and 50k (Spider train) examples, while
the balanced counterparts reduce to just 30k and 18k, respectively. This reduction makes
training considerably faster, lowering both computational cost and time-to-train. Despite the
smaller datasets, ORM performance remains largely comparable across settings, with over-
all differences being minimal. More interestingly, in certain cases balancing even improves
results, for instance, the best-performing models on BIRD dev, such as OmniSQL-7B,
achieve higher execution accuracy when trained on the smaller, balanced set.
    In summary, dataset balancing not only reduces data requirements and training time, but
also yields competitive, and sometimes superior, performance. Based on these trends, we
adopt the Balanced configuration as the default setup for the comparison against baselines
in RQ3.

RQ3 – ORM effectiveness vs. baseline methods Table 5 compares the ORM-based Best-of-N
strategy with execution-based BoN (ex-BoN) and Majority Voting (Maj), using OmniSQL-
7B as the candidate generator. The ORM is trained on OmniSQL-7B with the balanced
dataset. We report execution accuracy on BIRD dev, Spider dev, and Spider test, along with
the absolute gains over the single-sample baseline (N = 1), corresponding to the first gener-
ated query. Following Dror (2018), we apply the McNemar statistical test together with the
Bonferroni correction to assess significance across methods. Results indicate that the ORM-
based strategy consistently achieves the highest execution accuracy across all datasets and
evaluation splits. Although the improvement on Spider dev does not retain significance after
Bonferroni correction, which may be attributed to the smaller sample size, all other results
remain statistically significant

Table 5 Execution accuracy (%) of OmniSQL-7B on BIRD dev, Spider dev, and Spider test. ∆ indicates the
gain over the baseline ( N = 1 ). Best and runner-up results are in bold and underlined, respectively. Values
marked with † are not McNemar significant (p < 0.05), and those with * lose significance after Bonferroni
correction
Method                            BIRD dev                   Spider dev                Spider test
                                  EX           ∆             EX            ∆           EX            ∆
Baseline (N = 1)                  63.89        –             82.40         –           84.02         –
Majority Voting (N = 32)          66.95        +3.06         83.75∗        +1.35       85.47         +1.45
Best-of-N (N = 32)
   Execution-based                66.04        +2.15         82.79†∗       +0.39       85.14         +1.12
   ORM-based                      68.90        +5.01         84.53∗        +2.13       87.47         +3.45



13
Journal of Intelligent Information Systems (2026) 64:2545–2568                          2559


   Specifically, on BIRD dev, ORMs reach 68.90% execution accuracy, surpassing both Maj
(66.95%) and ex-BoN (66.04%), and achieving a gain of +5.01 points over the baseline. On
Spider dev, ORMs again outperform all baselines with 84.53% accuracy, a +2.13 improve-
ment compared to 83.75% for Maj and 82.79% for ex-BoN. The same trend holds on Spider
test, where ORM-based selection achieves 87.47%, outperforming both Maj (85.47%) and
ex-BoN (85.14%), with an absolute gain of +3.45 points over the baseline.
   These results highlight a clear pattern: while heuristic strategies such as Majority Vot-
ing and execution-based Best-of-N offer gains over the single-sample baseline, ORM-
based selection delivers consistent and stronger improvements. Notably, the largest gain
is observed on BIRD dev (+5.01), indicating that ORMs provide the greatest advantage in
scenarios with more challenging or diverse query distributions.
   Overall, these findings demonstrate that ORMs not only generalize across model fami-
lies (RQ1) and benefit from dataset balancing (RQ2), but also achieve improvements over
widely used test-time strategies. This represents the central contribution of our work: show-
ing that ORM-based selection outperforms Majority Voting and execution-based Best-of-N,
providing a stronger heuristic for Best-of-N test-time inference.


6 Ablation studies

In this section, we further investigate ORM training by addressing additional research ques-
tions to better understand its effectiveness compared to alternative methods. Specifically,
we aim to answer:
RQ4        What is the role of N in ORM performance?
RQ5        Are ORMs effective when using larger base models as generators?
RQ6        How does the training prompt influence ORM results?

RQ4 – Effect of N on ORM performance How the number of candidates N influence the
performance of ORM-based selection? Table 6 present the effect of varying N on execu-
tion accuracy across BIRD dev, Spider dev, and Spider test. We compare four strategies:
execution-based Best-of-N, Majority Voting, ORM-based Best-of-N, and Pass@N, the latter
serving as an upper bound on achievable performance by reporting the proportion of queries
for which at least one correct candidate is generated. The results show that ORM-based
selection consistently achieves higher accuracy than heuristic methods across all values of
N, while also approaching the upper bound defined by Pass@N more closely as N increases.

   On BIRD dev, ORM accuracy increases from 63.89% at N = 1 to 68.71% at N = 25,
after which it stabilizes with only minor fluctuations, reaching 68.90% at N = 32. In con-
trast, execution-based Best-of-N plateaus earlier around 66.0%, while Majority Voting con-
verges near 67.0%. A similar pattern emerges on Spider dev, where ORM steadily improves
to 84.62–84.72% in the range N = 17–30, compared to 82.88% for execution-based Best-
of-N and 84.14% for Majority Voting. On Spider test, ORM achieves 87.47% at N = 32
, maintaining a consistent margin of +2 to +3 points over both baselines. Overall, these
results show that ORMs not only scale more effectively with increasing candidate pools
but also sustain their advantage as N grows, underscoring their effectiveness as a selection
mechanism.


                                                                                  13
2560                                        Journal of Intelligent Information Systems (2026) 64:2545–2568

Table 6 Execution accuracy (%) and Pass@N of test-time strategies across varying N values. Columns are
color-coded from light yellow (lowest) to dark orange (highest) performance




   Figure 3 further decomposes performance by query difficulty (Simple, Moderate, Chal-
lenging) on the BIRD dev set. For simple queries, all methods improve with increasing N,
but ORM consistently maintains a margin of 1–2 points over Majority Voting and 2–3 points
over execution-based Best-of-N. The advantage becomes more pronounced for moderate
queries, where ORM shows a smooth upward trajectory and stabilizes near 63%, while
both baselines plateau earlier at lower levels. The most striking gains are observed on chal-
lenging queries: here, ORM substantially outperforms both strategies, with improvements
exceeding 3–4 points at higher N, whereas execution-based Best-of-N remains flat and
Majority Voting oscillates with unstable progress. These results highlight that ORM selec-
tion is particularly effective in harder scenarios, where discriminating between semantically
correct and incorrect candidates becomes critical.
   Overall, these findings show that ORM-based selection benefits consistently from larger
candidate pools, outperforming the other heuristic strategies across datasets, evaluation
splits, and difficulty levels. While Majority Voting and execution-based Best-of-N provide
incremental improvements at low values of N, they quickly saturate, whereas ORM con-
tinues to scale and more closely approaches the oracle bound defined by Pass@N. This
reinforces the conclusion that ORMs provide a principled and effective mechanism for lever-
aging increased generation budgets, ensuring more reliable gains from test-time compute.

RQ5 – ORM effectiveness with larger generator models How does ORM performance vary
when the underlying generator model is scaled to larger parameter sizes?


13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                    2561




      (a) Simple EX at scaling N                                 (b) Moderate EX at scaling N




   (c) Challenging EX at scaling N                                (d) Total EX at scaling N

Fig. 3 Execution accuracy (%) on BIRD dev across different N values, comparing execution-based Best-
of-N (ex-BoN), Majority Voting (Maj), and ORM-based Best-of-N (ORM-BoN). Results are shown by
query difficulty (Simple, Moderate, Challenging) and overall (Total)


   Table 7 reports execution accuracy and Pass@32 across OmniSQL models of differ-
ent sizes (7B, 14B, 32B) on BIRD dev, Spider dev, and Spider test. The ORM is fixed to
OmniSQL-7B, while the generator varies in scale. Results show that ORM-based selection
remains consistently competitive across all generator sizes, outperforming Majority Voting
(Maj) and Execution-based Best-of-N (ex-BoN) methods, while approaching the oracle-like
upper bound defined by Pass@32.
   On BIRD dev, ORM achieves the highest accuracy with all generator sizes, reaching
68.90% with 7B, 69.04% with 14B, and 69.30% with 32B, demonstrating that ORM
continues to provide robust gains even as the generator becomes larger. Interestingly,
while Majority Voting and Best-of-N improve moderately with 14B, they fall behind
at 32B, where ORM remains stable and sustains its advantage. On Spider dev, ORM
also achieves the strongest results, with 84.33% (7B), 84.62% (14B), and 84.43%




                                                                                           13
2562                                        Journal of Intelligent Information Systems (2026) 64:2545–2568

Table 7 Execution accuracy (%) and Pass@32 on the BIRD dev, Spider dev, and Spider test. Candidate que-
ries are generated by OmniSQL models with 7B, 14B, and 32B parameters, while the ORM is implemented
using OmniSQL-7B. Best scores per column are shown in bold
             Model               Baseline     Ex-BoN       Majority       ORM-BoN           Pass@32
BIRD         OmniSQL-7B          63.89        66.04        66.95          68.90             80.57
dev          OmniSQL-14B         64.28        66.75        67.01          69.04             80.90
             OmniSQL-32B         64.02        66.10        63.95          69.30             82.20
Spider       OmniSQL-7B          82.40        82.79        83.75          84.33             91.68
dev          OmniSQL-14B         82.01        82.20        83.56          84.62             92.75
             OmniSQL-32B         83.17        83.37        83.08          84.43             92.84
Spider       OmniSQL-7B          84.02        85.14        85.47          87.33             93.29
test         OmniSQL-14B         84.91        85.28        84.86          87.42             93.53
             OmniSQL-32B         84.30        84.72        86.07          87.19             94.08


(32B), consistently outperforming heuristic baselines by 0.5–2 points. A similar trend is
observed on Spider test, where ORM yields 87.33% (7B), 87.42% (14B), and 87.19%
(32B), surpassing both Maj and ex-BoN in nearly all settings.
   These results suggest that ORM effectiveness is not diminished by scaling the generator.
While larger models naturally improve baseline performance, the relative improvements
provided by ORM remain intact. Moreover, ORM demonstrates greater stability across
datasets and evaluation splits, whereas other heuristics exhibit fluctuations depending on
model size.
   In summary, ORM-based selection delivers consistent accuracy improvements even as
the underlying generator grows to 14B and 32B parameters. By sustaining its advantage
across scales and datasets, ORM establishes itself as a robust and scalable strategy for test-
time SQL generation, ensuring reliable gains whether deployed with medium or large gen-
erator backbones.

RQ6 – Impact of training prompt on ORM results How does the design of verification
prompts affect ORM performance?

   Table 8 presents an ablation study on prompt design for ORM verification using Qwen2.5-
7B-Instruct as the verifier and OmniSQL-7B as the generator, evaluated on the BIRD dev
set. Four prompt variants are compared: (i) Instruction, which provides the SQL query with
explicit verification instructions; (ii) Data-Only which provides only the result set produced
by executing the query; (iii) SQL-only which includes only the query; and (iv) Data+SQL,
which provides both the query and its result set. Results show that the choice of prompt can
influence ORM effectiveness, particularly for moderate and challenging queries, while dif-
ferences are less pronounced for simple ones.


Table 8 Ablation study on verification prompt design for ORM on BIRD dev. Execution accuracy (%) by
query difficulty. Generator: OmniSQL-7B; ORM: Qwen2.5-7B-Instruct. Best scores in bold
Prompt Variant                Simple             Moderate           Challenging              Total
Instruction                   72.65              59.70              51.32                    66.72
Data-Only                     72.76              59.48              51.72                    66.75
SQL-Only                      72.86              63.36              53.79                    68.19
Data + SQL                    73.08              62.50              50.34                    67.73



13
Journal of Intelligent Information Systems (2026) 64:2545–2568                           2563


   For simple queries, all prompts yield nearly identical results, with accuracies clustering
around 72% - 73%, suggesting that prompt design plays a minimal role when the task is
straightforward and candidates are easy to discriminate. Differences emerge more clearly for
moderate queries, where the SQL-only prompt achieves the strongest accuracy (63.36%),
outperforming the next-best SQL+Data prompt by nearly one point, while the instruction-
style and data-only variants lag behind at 59% - 60%. This trend becomes even more evi-
dent in challenging queries, where the SQL-only prompt again delivers the best results
(53.79%), surpassing all other formulations by more than two points. These gains translate
into the highest overall average accuracy for the SQL-only prompt (68.19%), followed by
the SQL+Data variant (67.73%), while the instruction and data-only variants converge at
roughly 66.7%.
   These findings suggest that the most effective verification signal for ORM training comes
from exposing the verifier directly to SQL structures, without additional natural language
instructions or contextual data. While including schema or data information can slightly
improve performance in moderate cases, excessive context appears to reduce the verifier’s
discriminative ability.


7 Conclusions

In this work, we presented GradeSQL, a unified framework for synthesizing training data
and developing Outcome Reward Models (ORMs) to enhance the reliability of the Text-to-
SQL task. By shifting the focus from frequency-based heuristics to dense semantic rank-
ing, GradeSQL facilitates a more robust integration of AI within the lifecycle of structured
information systems. Our study demonstrates that ORMs function as an effective knowl-
edge-directed inference mechanism, providing a superior alternative to classical test-time
strategies such as execution-based Best-of-N (ex-BoN) and Majority Voting (Maj).
    Experimental results across heterogeneous model families confirm that task-specific
ORMs can be trained on relatively small-scale, balanced datasets to achieve competitive
performance on the BIRD and Spider benchmarks. We observed that the effectiveness of
GradeSQL scales with the strength of the generator model and remains robust across vary-
ing candidate budgets. Importantly, our analysis suggests that lightweight verifiers are suf-
ficient for achieving significant accuracy gains, making them highly suitable for practical
deployment in real-time Intelligent Information Systems where minimizing computational
latency is paramount.
    Ultimately, GradeSQL offers a scalable architectural approach for building reliable natu-
ral language interfaces to databases. By moving beyond simple execution success toward
deep semantic verification, this framework enhances the cooperative support provided to
users during complex query refinement. To support the research community and foster
further innovation in the integration of AI and database technologies, we have made the
GradeSQL framework4, training datasets5, and pretrained ORMs6 available as open-source
resources.


4
    https://github.com/sisinflab/GradeSQL
5
    https://hug​gingface.co​/collection​s/sisinf​lab-ai/68ac62e1356b5399ef81236c
6
    https:​​​//huggingfa​ce​.co/collect​ions/sis​i​nf​lab-ai/68ac58755ffe5fe880e0acb5


                                                                                        13
2564                                                          Journal of Intelligent Information Systems (2026) 64:2545–2568


8 Limitations

While our study establishes the effectiveness of Outcome Reward Models (ORMs) for rank-
ing SQL queries, several limitations remain. First, our evaluation focuses on two bench-
marks, BIRD and Spider, which may not capture the full diversity of real-world databases
and query distributions. Future work should validate ORM generalization across domains,
schema sizes, and multilingual settings. Second, although the computational cost of train-
ing ORMs is moderate compared to larger generators, it still raises scalability concerns
in resource-constrained environments. Third, future research should investigate the impact
of advanced prompting strategies and diverse instruction-based evaluation frameworks.
Finally, our work centers on test-time selection and does not yet address integration with
reinforcement learning loops or interactive query refinement, which remain promising but
unexplored directions.

Author contributions M.T. and G.F. implemented the framework and authored the original draft. D.D. pro-
vided critical revisions and significant improvements to the manuscript. G.R., F.N., T.D. and D.S. offered
strategic guidance throughout the research process. All authors have reviewed the final version.

Funding Open access funding provided by Politecnico di Bari within the CRUI-CARE Agreement. No fund-
ing was received for conducting this study.

Data availability Our approach is evaluated on the BIRD and Spider benchmarks, both linked within the
manuscript. We also release on Hugging face all pre-processed data that have fed our models.

Declarations

Competing interests The authors declare no competing interests.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License,
which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as
you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons
licence, and indicate if changes were made. The images or other third party material in this article are
included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material.
If material is not included in the article’s Creative Commons licence and your intended use is not permitted
by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the
copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.




References
Androutsopoulos, I., Ritchie, G. D., & Thanisch, P. (1995). Natural language interfaces to databases–an
     introduction. In Natural language engineering, vol 1. Cambridge University Press, (pp. 29–81). ​h​t​t​p​s​:​/​
     /​d​o​i​.​o​r​g​/​1​0​.​1​0​1​7​/​S​1​3​5​1​3​2​4​9​0​0​0​0​0​0​5​X​​​​
Anil, R., Dai, A. M., Firat, O., et al. (2023). PaLM 2 technical report. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​3​0​5​.​
     1​0​4​0​3​​​​
Askari, A., Poelitz, C., & Tang, X. (2025). MAGIC: Generating self-correction guideline for in-context text-
     to-SQL. Proceedings of the AAAI Conference on Artificial Intelligence, 39(22), 23433–23441. ​h​t​t​p​s​:​/​/​d​
     o​i​.​o​r​g​/​1​0​.​1​6​0​9​/​a​a​a​i​.​v​3​9​i​2​2​.​3​4​5​1​1​​​​
Baek, J., Samulowitz, H., & Hassanzadeh, O. (2025). Knowledge base construction for knowledge-aug-
     mented text-to-SQL. https://doi​.org/10.186​53/v1/2025.​findings​-acl.1363




13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                                                      2565

Bogin, B., Berant, J., & Gardner, M. (2019). Representing schema structure with graph neural networks for
      text-to-SQL parsing. In A. Korhonen, D. Traum, & L. Màrquez (Eds.), Proceedings of the 57th Annual
      Meeting of the Association for Computational Linguistics (pp. 4560–4565). Association for Computa-
      tional Linguistics. https://doi.org/10.18653/v1/P19-1448
Borchmann, U., & Wydmuch, M. (2025). Query and conquer: Execution-guided SQL generation. ​h​t​t​p​s​:​/​/​d​o​
      i​.​o​r​g​/​1​0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​5​0​3​.​2​4​3​6​4​​​​
Brown, B., Juravsky, J., Ehrlich, R., et al. (2024). Large language monkeys: Scaling inference compute with
      repeated sampling. https://doi.org/10.48550/arXiv.2407.21787
Chen, B., Zhang, F., Nguyen, A., et al. (2022). CodeT: Code generation with generated tests. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
      1​0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​2​0​7​.​1​0​3​9​7​​​​
Chickering, D. M. (2002). Optimal structure identification with greedy search. In Association for Computata-
      tion Machinery. https://doi.org/10.1162/153244303321897717
Chung, H. L., & Hsiao. (2025). Revisiting test-time scaling: A survey and a diversity-aware method for effi-
      cient reasoning. arXiv:2506.04611
Cobbe, K., Kosaraju, V., Bavarian, M., et al. (2021). Training verifiers to solve math word problems. ​h​t​t​p​s​:​/​/​
      d​o​i​.​o​r​g​/​1​0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​1​1​0​.​1​4​1​6​8​​​​
Dai, Y., Yang, H., & Hao, M. (2025). PARSQL: Enhancing text-to-SQL through SQL parsing and reasoning.
      In Findings of the Association for Computational Linguistics: ACL 2025. ACL (pp. 661–681). ​h​t​t​p​s​​:​/​/​d​
      o​i​​.​o​r​g​/​​1​0​.​1​​8​6​5​3​/​v​1​/​2​0​2​5​.​f​i​n​d​i​n​g​s​-​a​c​l​.​3​7​​​​
Devlin, J., Chang, M. W., Lee, K., et al. (2019). BERT: Pre-training of deep bidirectional transformers for
      language understanding. In Proceedings of the 2019 Conference of the North American Chapter of the
      Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short
      Papers). Association for Computational Linguistics, pp 4171–4186. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​8​6​5​3​/​v​1​/​N​1​9​-​1​
      4​2​3​​​​
Dror. (2018). The hitchhiker’s guide to testing statistical significance in natural language processing. In 56th
      Annual Meeting of the Association for Computational Linguistics (pp. 1383–1392). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​
      1​8​6​5​3​/​v​1​/​P​1​8​-​1​1​2​8​​​​
Fan, A., Lewis, M., & Dauphin, Y. (2018). Hierarchical neural story generation. Association for Computa-
      tional Linguistics. https://doi.org/10.18653/v1/P18-1082
Gao, D., Wang, H., Li. Y., et al. (2023). Text-to-SQL empowered by large language models: A benchmark
      evaluation. https://doi.org/10.48550/arXiv.2308.15363
Grattafiori, A., Dubey, A., Jauhri, A., et al. (2024). The llama 3 herd of models. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​4​8​5​5​0​/​a​r​
      X​i​v​.​2​4​0​7​.​2​1​7​8​3​​​​
Havrilla, A., Du, Y., Raparthy, S. C., et al. (2024). Teaching large language models to reason with reinforce-
      ment learning. https://doi.org/10.48550/arXiv.2403.04642
He, M., Shen, Y., & Zhang, W. (2025). STaR-SQL: Self-taught reasoner for text-to-SQL. Association for
      Computational Linguistics. https://doi​.org/10.186​53/v1/2025.​acl-long​.1187, arXiv:2502.13550.
Holtzman, A., Buys, J., Du, L., et al. (2020). The curious case of neural text degeneration. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​
      .​4​8​5​5​0​/​a​r​X​i​v​.​1​9​0​4​.​0​9​7​5​1​​​​
Hong, Z., & Yuan, Z. (2024). Knowledge-to-SQL: Enhancing SQL generation with data expert LLM. ​h​t​t​p​s​:​/​
      /​d​o​i​.​o​r​g​/​1​0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​4​0​2​.​1​1​5​1​7​​​​
Hong, Z., Yuan, Z., Zhang, Q., et al. (2025). Next-generation database interfaces: A survey of LLM-based
      text-to-SQL. IEEE Transactions on Knowledge and Data Engineering, 37(12), 7328–7345. ​h​t​t​p​s​:​/​/​d​o​i​.​
      o​r​g​/​1​0​.​1​1​0​9​/​T​K​D​E​.​2​0​2​5​.​3​6​0​9​4​8​6​​​​
Huang, S., Ma, Z., & Du, J. (2025). Mirror-consistency: Harnessing inconsistency in majority voting. Asso-
      ciation for Computational Linguistics. https://doi​.org/10.186​53/v1/2024.​findings​-emnlp.135
Huang, H., Qu, Y., & Liu, J. (2024). Self-evaluation of large language model based on glass-box features.
      Association for Computational Linguistics. https://doi​.org/10.186​53/v1/2024.​findings​-emnlp.333
Kanburoğlu, A. B., & Tek, F. (2024). Text-to-SQL: A methodical review of challenges and models. Turkish
      Journal of Electrical Engineering and Computer Sciences, 32(3), 403–419. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​5​5​7​3​0​/​1​
      3​0​0​-​0​6​3​2​.​4​0​7​7​​​​
Khalifa, M., Agarwal, R., Logeswaran, L., et al. (2025). Process reward models that think. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
      0​.​4​8​5​5​0​/​a​r​X​i​v​.​2​5​0​4​.​1​6​8​2​8​​​​
Kim, H., So, B. H., Han, W. S., et al. (2020). Natural language to SQL: where are we today? Proc VLDB
      Endow, 13(10), 1737–1750. https://doi.org/10.14778/3401960.3401970
Kumar, P. (2024). Large language models (LLMs): survey, technical frameworks, and future challenges.
      Artificial Intelligence Review, 57(10), 260. https://doi.org/10.1007/s10462-024-10888-y
Lewkowycz, A. (2022). Solving quantitative reasoning problems with language models.
Li, Y. (2025). Learning to reason from feedback at test-time. In Proceedings of the 63rd Annual Meeting of
      the Association for Computational Linguistics (Volume 1). Association for Computational Linguistics,
      (pp. 5241–5253). https://doi​.org/10.186​53/v1/2025.​acl-long​.262


                                                                                                                          13
2566                                                                                    Journal of Intelligent Information Systems (2026) 64:2545–2568

Li, M., & Wang, E. A. (2024). Think twice before trusting: Self-detection for large language models through
      comprehensive answer reflection. In Findings of the Association for Computational Linguistics:
      EMNLP 2024. Association for Computational Linguistics. https://doi.org/10.48550/arXiv.2403.09972
Li, X. L., Holtzman, A., Fried, D., et al. (2023d). Contrastive decoding: Open-ended text generation as opti-
      mization. In A. Rogers, J. Boyd-Graber, N. Okazaki (eds.), Proceedings of the 61st Annual Meeting of
      the Association for Computational Linguistics (Volume 1: Long Papers). Association for Computational
      Linguistics, (pp. 12286–12312). https://doi​.org/10.186​53/v1/2023.​acl-long​.687
Li, J., Hui, B., Cheng, R., et al. (2023). Graphix-t5: Mixing pre-trained transformers with graph-aware lay-
      ers for text-to-SQL parsing. Proceedings of the AAAI Conference on Artificial Intelligence, 37(11),
      13076–13084. https://doi.org/10.1609/aaai.v37i11.26536
Li, J., Hui, B., Qu, G., et al. (2023c). Can LLM already serve as a database interface? A big bench for large-
      scale database grounded text-to-SQLs. In Advances in Neural Information Processing Systems, (pp.
      42330–42357). ​h​t​t​p​s​​:​/​/​p​r​o​​c​e​e​d​i​​n​g​s​.​​n​e​u​r​i​​p​s​.​c​c​/​​p​a​p​e​r​​s​p​s​f​​i​l​e​s​/​p​a​p​e​r​/​2​0​2​3​/​f​i​l​e​/​8​3​f​c​8​f​a​b​1​7​1​0​3​6​3​0​5​0​b​b​d​1​
      d​4​b​8​c​c​0​0​2​1​-​P​a​p​e​r​-​D​a​t​a​s​e​t​s​s​p​s​a​n​d​s​p​s​B​e​n​c​h​m​a​r​k​s​.​p​d​f​​​​
Li, F., & Jagadish, H. V. (2014). Constructing an interactive natural language interface for relational data-
      bases. Proc VLDB Endow, 8(1), 73–84. https://doi.org/10.14778/2735461.2735468
Li, Y., Jin, C., Peng, X., et al. (2026). Mitigating LLM hallucinations in Text-to-SQL parsing with a self-
      refinement feedback loop and memory augmentation. Journal of Intelligent Information Systems.
      https://doi.org/10.1007/s10844-026-01050-x
Liu, W., et al. (2024). Mind’s mirror: Distilling self-evaluation capability and comprehensive thinking from
      large language models. In Proceedings of the 2024 Conference of the North American Chapter of the
      Association for Computational Linguistics: Human Language Technologies (Volume 1). ACL, (pp.
      6748–6763). https://doi​.org/10.186​53/v1/2024.​naacl-lo​ng.376
Liu, X., Shen, S., Li, B., et al. (2025). A survey of text-to-SQL in the era of LLMs: Where are we, and where
      are we going? IEEE Transactions on Knowledge and Data Engineering, 37(10), 5735–5754. ​h​t​t​p​s​:​/​/​d​o​
      i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​K​D​E​.​2​0​2​5​.​3​5​9​2​0​3​2​​​​
Li, H., Wu, S., Zhang, X., et al. (2025). OmniSQL: Synthesizing high-quality text-to-SQL data at scale.
      VLDB Endowment, 10(14778/3749646), 3749723.
Li, H., Zhang, J., Li, C., et al. (2023). Resdsql: Decoupling schema linking and skeleton parsing for text-to-
      sql. Proceedings of the AAAI Conference on Artificial Intelligence, 37(11), 13067–13075. ​h​t​t​p​s​:​/​/​d​o​i​.​o​
      r​g​/​1​0​.​1​6​0​9​/​a​a​a​i​.​v​3​7​i​1​1​.​2​6​5​3​5​​​​
Ma, L., Pu, K., & Zhu, Y. (2024). Evaluating LLMs for text-to-SQL generation with complex SQL workload.
      https://doi.org/10.48550/arXiv.2407.19517
OpenAI, Achiam, J., Adler, S., et al. (2024). GPT-4 technical report. https://doi.org/10.48550/arXiv.2303.08774
Pourreza, M., & Rafiei, D. (2023). DIN-SQL: Decomposed in-context learning of text-to-SQL with self-cor-
      rection. In Advances in Neural Information Processing Systems, (pp. 36339–36348). ​h​t​t​p​s​​:​/​/​p​r​o​​c​e​e​d​i​​n​g​
      s​.​​n​e​u​r​i​​p​s​.​c​c​/​​p​a​p​e​r​​s​p​s​f​​i​l​e​s​/​p​a​p​e​r​/​2​0​2​3​/​f​i​l​e​/​7​2​2​2​3​c​c​6​6​f​6​3​c​a​1​a​a​5​9​e​d​a​e​c​1​b​3​6​7​0​e​6​-​P​a​p​e​r​-​C​o​n​f​e​r​e​n​c​e​.​p​d​f​​​​
Qin, Y., Chen, C., Fu, Z., et al. (2025). ROUTE: Robust multitask tuning and collaboration for text-to-SQL.
      In International Conference on Learning Representations. arXiv:2412.10138, ​h​t​t​p​s​​:​/​/​p​r​o​​c​e​e​d​i​​n​g​s​.​​i​c​l​r​.​​c​
      c​/​p​a​p​​e​r​s​p​s​​f​i​l​e​​s​/​p​a​p​e​r​/​2​0​2​5​/​f​i​l​e​/​2​1​2​b​1​4​3​b​5​a​5​d​6​b​8​8​f​e​b​0​f​b​1​4​4​1​b​9​7​5​6​e​-​P​a​p​e​r​-​C​o​n​f​e​r​e​n​c​e​.​p​d​f​​​​
Radford, A., & Wu, J. (2019). Language models are unsupervised multitask learners. ​h​t​t​p​s​​:​/​/​c​d​n​​.​o​p​e​n​​a​i​.​c​​o​m​/​
      b​e​​t​t​e​r​-​l​​a​n​g​u​a​​g​e​-​m​​o​d​e​l​s​/​l​a​n​g​u​a​g​e​s​p​s​m​o​d​e​l​s​s​p​s​a​r​e​s​p​s​u​n​s​u​p​e​r​v​i​s​e​d​s​p​s​m​u​l​t​i​t​a​s​k​s​p​s​l​e​a​r​n​e​r​s​.​p​d​f​​​​
Raffel, C., Shazeer, N., Roberts, A., et al. (2020). Exploring the limits of transfer learning with a unified
      text-to-text transformer. Journal of Machine Learning Research, 21(140), 1–67. ​h​t​t​p​:​/​/​j​m​l​r​.​o​r​g​/​p​a​p​e​r​
      s​/​v​2​1​/​2​0​-​0​7​4​.​h​t​m​l​​​​
Rossiello, G., Pham, N., Glass, M., et al. (2025). Rationalization models for text-to-SQL. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​
      .​4​8​5​5​0​/​a​r​X​i​v​.​2​5​0​2​.​0​6​7​5​9​​​​
Sheng, L., & Shuai, X. S. (2025). CSC-SQL: Corrective self-consistency in text-to-SQL via reinforcement
      learning. In Proceedings of the 14th International Joint Conference on Natural Language Processing
      and the 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics.
      The Asian Federation of Natural Language Processing and The Association for Computational Linguis-
      tics, (pp. 1473–1496). http://jmlr.org/papers/v21/20-074.html
Snell, C. V., Lee, J., Xu, K., et al. (2024). Scaling LLM test-time compute optimally can be more effective
      than scaling parameters for reasoning. ​h​t​t​p​s​​:​/​/​p​r​o​​c​e​e​d​i​​n​g​s​.​​i​c​l​r​.​​c​c​/​p​a​p​​e​r​s​p​s​​f​i​l​e​​s​/​p​a​p​e​r​/​2​0​2​5​/​f​i​l​e​/​1​b​6​2​3​6​
      6​3​f​d​9​b​8​7​4​3​6​6​f​3​c​e​0​1​9​f​d​f​d​d​4​4​-​P​a​p​e​r​-​C​o​n​f​e​r​e​n​c​e​.​p​d​f​​​​
Tillmann, C., & Ney, H. (2003). Word reordering and a dynamic programming beam search algorithm for
      statistical machine translation. Computational Linguistics, 29(1), 97–133. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​6​2​/​0​8​9​
      1​2​0​1​0​3​3​2​1​3​3​7​4​5​8​​​​




13
Journal of Intelligent Information Systems (2026) 64:2545–2568                                                                        2567

Wang, B., Ren, C., & Yang, J. (2025). MAC-SQL: A multi-agent collaborative framework for text-to-SQL.
      In Proceedings of the 31st International Conference on Computational Linguistics (pp. 540–557). Asso-
      ciation for Computational Linguistics.
Wang, B., Shin, R., & Liu, X. (2020). RAT-SQL: Relation-aware schema encoding and linking for text-to-
      SQL parsers. In D. Jurafsky, J. Chai, & N. Schluter (Eds.), Proceedings of the 58th Annual Meeting of
      the Association for Computational Linguistics (pp. 7567–7578). Association for Computational Lin-
      guistics. https://doi​.org/10.186​53/v1/2020.​acl-main​.677
Wang, X., Wei, J., Schuurmans, D., et al. (2023). Self-consistency improves chain of thought reasoning in
      language models. https://doi.org/10.48550/arXiv.2203.11171
Wiher, G., Meister, C., & Cotterell, R. (2022). On decoding strategies for neural text generators. Transac-
      tions of the Association for Computational Linguistics, 10, 997–1012. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​6​2​/​t​a​c​l​s​p​s​a​
      s​p​s​0​0​5​0​2​​​​
Woods, W. (1972). The lunar sciences natural language information system: Final report. ​h​t​t​p​s​​:​/​/​c​i​r​​.​n​i​i​.​​a​c​.​j​​p​
      /​c​r​i​d​/​1​5​7​4​2​3​1​8​7​4​5​4​4​1​3​3​3​7​6​​​​
Xiao, C., Dymetman, M., & Gardent, C. (2016). Sequence-based structured prediction for semantic parsing.
      In Annual meeting of the Association for Computational Linguistics (ACL) (pp. 1341–1350). ​h​t​t​p​s​:​/​/​d​o​
      i​.​o​r​g​/​1​0​.​1​8​6​5​3​/​v​1​/​P​1​6​-​1​1​2​7​​​​
Xie, B., Xu, B., Yuan, Y., et al. (2025). From outcomes to processes: Guiding PRM learning from ORM for
      inference-time alignment. In Proceedings of the 63rd Annual Meeting of the Association for Computa-
      tional Linguistics (Volume 1: Long Papers). Association for Computational Linguistics. ​h​t​t​p​s​​:​/​/​d​o​i​​.​o​r​g​
      /​​1​0​.​1​​8​6​5​3​/​v​1​/​2​0​2​5​.​a​c​l​-​l​o​n​g​.​9​4​6​​​​
Xu, X., Jiang, X., Wang, A., et al. (2026). PPR-SQL: a robust text-to-SQL system via probabilistic graph
      pruning and multi-view reasoning. Journal of Intelligent Information Systems. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​
      /​s​1​0​8​4​4​-​0​2​6​-​0​1​0​4​9​-​4​​​​
Yi, J., & Chen, G. (2025). SKT-SQL: multi-decoupling and skeleton prompt framework for text-to-SQL on
      small-scale LMs. Journal of Intelligent Information Systems, 1779–1805. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​1​0​8​
      4​4​-​0​2​5​-​0​0​9​6​3​-​3​​​​
Yu, T., Zhang, R., & Yang, K. (2019). Spider: A large-scale human-labeled dataset for complex and cross-
      domain semantic parsing and text-to-SQL task. In Proceedings of the 2018 Conference on Empirical
      Methods in Natural Language Processing. Association for Computational Linguistics. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
      1​0​.​1​8​6​5​3​/​v​1​/​D​1​8​-​1​4​2​5​​​​
Zhang, Z., Zheng, C., & Wu, Y. (2025). The lessons of developing process reward models in mathematical
      reasoning. In Findings of the Association for Computational Linguistics: ACL 2025. Association for
      Computational Linguistics. https://doi​.org/10.186​53/v1/2025.​findings​-acl.547
Zhang, C., Mao, Y., Fan, Y., et al. (2024). FinSQL: Model-agnostic LLMs-based text-to-SQL framework for
      financial analysis. In Companion of the 2024 International Conference on Management of Data. Associ-
      ation for Computing Machinery, SIGMOD ’24, (pp. 93–105). https://doi.org/10.1145/3626246.3653375

Publisher's note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations.




                                                                                                                            13
2568                                              Journal of Intelligent Information Systems (2026) 64:2545–2568


Authors and Affiliations

Mattia Tritto1 · Giuseppe Farano1 · Dario Di Palma1 · Gaetano Rossiello2 ·
Dharmashankar Subramanian2 · Fedelucio Narducci1 · Tommaso Di Noia1

    Mattia Tritto
    mattiatritto01@gmail.com
    Giuseppe Farano
    farano.giuseppe02@gmail.com
    Dario Di Palma
    dario.dipalma@poliba.it
    Fedelucio Narducci
    fedelucio.narducci@poliba.it
    Gaetano Rossiello
    gaetano.rossiello@ibm.com
    Dharmashankar Subramanian
    dharmash@us.ibm.com
    Tommaso Di Noia
    tommaso.dinoia@poliba.it
1
    Polytechnic University of Bari, Bari, Italy
2
    IBM T.J. Watson Research Center, Yorktown Heights, NY 10598, USA




13
