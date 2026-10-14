                                            Can Large Language Models Model Programs
                                                            Formally?

                                        Zhiyong Chen1[0009−0005−2555−5728] , Jialun Cao2,3[0000−0003−4892−6294] , Jiarong
                                         Wu2,3[0000−0001−6126−303X] , Chang Xu1[0000−0002−6299−4704] , and Shing-Chi
                                                               Cheung2,3[0000−0002−3508−7172]
                                                      1
                                                       State Key Laboratory for Novel Software Technology,
                                                               Nanjing University, Nanjing, China
arXiv:2604.01851v1 [cs.SE] 2 Apr 2026




                                                     zhiyongchen@smail.nju.edu.cn, changxu@nju.edu.cn
                                         2
                                           Department of Computer Science and Engineering, The Hong Kong University of
                                                           Science and Technology, Hong Kong, China
                                            3
                                              Guangzhou HKUST Fok Ying Tung Research Institute, Guangzhou, China
                                                   jialuncao@ust.hk, jwubf@cse.ust.hk, sccheung@ust.hk


                                              Abstract. In the digital age, ensuring the correctness, safety, and re-
                                              liability of software through formal verification is paramount, particu-
                                              larly as software increasingly underpins critical infrastructure. Formal
                                              verification, split into theorem proving and model checking, provides a
                                              feasible and reliable path. Unlike theorem proving, which yields notable
                                              advances, model checking has been less focused due to the difficulty of au-
                                              tomatic program modeling. To fill this gap, we introduce Model-Bench,
                                              a benchmark and an accompanying pipeline for evaluating and improv-
                                              ing LLMs’ program modeling capability by modeling Python programs
                                              into verification-ready model checking specifications checkable by its ac-
                                              companying model checker. Model-Bench comprises 400 Python pro-
                                              grams derived from three well-known benchmarks (HumanEval, MBPP,
                                              and LiveCodeBench). Our extensive experiments reveal significant limi-
                                              tations in LLMs’ program modeling and further provide inspiring direc-
                                              tions.

                                              Keywords: Model Checking · Large Language Model · Formal Verifi-
                                              cation.


                                        1   Introduction
                                        While software testing can reveal the presence of bug, but it cannot prove their
                                        absence. Formal verification, when grounded in precise specifications, can provide
                                        machine-checkable guarantees. Technically, formal methods split into two main
                                        approaches: theorem proving, which establishes properties via logical derivations
                                        in proof assistants or automated provers, and model checking [9], which decides
                                        property satisfaction by exhaustively exploring a system’s state space against
                                        temporal specifications.
                                            Recent progress has concentrated on LLM-assisted theorem proving (e.g.,
                                        autoformalization [36,19], proof generation [39], and premise selection and re-
                                        trieval), yielding notable advances. By contrast, model checking has been less
2      Chen et al.

focused, largely due to the automodeling bottleneck: it is difficult to derive ac-
curate and tractable behavioral models from programs automatically. Though
there are a few attempts to model formal properties from requirements [5], mod-
eling formal models for programs has rarely been explored.
    However, automatically constructing such models from code is technically
challenging and underexplored. Dynamic languages like Python exhibit rich
runtime behavior (e.g., mutable aliasing, higher-order functions, third-party li-
braries, async/await) that must be abstracted to a finite but faithful state space.
Useful models are expected to keep a soundness and precision trade-off: too
concrete and model checkers do not scale; too abstract and properties become
vacuous or unsound.
    This gap motivates our work, Model-Bench, a benchmark and an accom-
panying pipeline for evaluating and improving LLMs’ program modeling ca-
pability by modeling Python programs into verification-ready TLA+ (Tempo-
ral Logic of Actions, a formal language for model checking) [21] specifications
checkable by its accompanying model checker TLC [41]. Model-Bench com-
prises 400 Python programs derived from three well-known benchmarks (i.e.
HumanEval [8], MBPP [3], and LiveCodeBench [18]) by normalization, simplifi-
cation, and rewrite. The benchmark covers progressively difficult settings, from
easy to medium, and then to hard. These programs are covered by a total of
1,639 test cases, ensuring a rigorous evaluation.
    Our extensive experiments reveal significant limitations in LLMs’ program
modeling: only 66.25% runnable and 49.55% state similarity under in-context
learning at best. We also propose a code transformation approach to facilitate
LLMs modeling and yield promising complementary improvements. Finally, we
showed that the modeling difficulty is not reliably correlated with algorithmic
difficulty but with nested loops and data-structure complexity. Our contribution
includes:

– Significance. We proposed Model-Bench, a benchmark and an accompa-
  nying pipeline for evaluating and improving LLMs’ program modeling capa-
  bility by modeling Python programs into verification-ready TLA+
– Novelty. Besides introducing Model-Bench, we also demonstrate a way to
  improve the LLMs’ program modeling capability via code transformation.
– Evaluation. We conduct extensive experiments that yield several instructive
  findings. Our analysis of bad cases also provides directions for future improve-
  ment.


2   Related Work

Automated Formal Verification While there exist various approaches and
techniques for automated formal verification that generates program specifica-
tions from natural language [10,42,15], our Model-Bench primarily focuses on
specification generation based on the programming language. In recent years,
                   Can Large Language Models Model Programs Formally?          3

there has also been a growing interest in applying LLMs to assist program ver-
ification [23,24,32,17,20]. These works focus on using LLMs for theorem prov-
ing or domain-specific modeling. For example, Zhou [43] introduces a two-stage
proof generation method that combines LLMs with Retrieval-Augmented Gen-
eration. Additionally, frameworks such as CryptoFormalEval [11], AVRE [38],
and Mao et al. [29] have designed specialized automated modeling and verifica-
tion architectures for specific domains, such as cryptographic protocols and 5G
communication protocols. Our Model-Bench represents the first LLM-based,
general-purpose research effort focused on generating model specifications di-
rectly from source code.
    Formal Verification Benchmarks The formal specification benchmarks
offer a standard, well-defined set of problems, providing a shared challenge that
helps build a community of practice among researchers. For formal theorem
proving, a recent survey [22] summarized the existing datasets. NL-PS [14]
first builds a natural language premise selection dataset source from ProofWiki.
Similarly, NaturalProofs [33] further incorporates data from Stacks and text-
books, resulting in a dataset with roughly 25k examples. Adapted from it,
NaturalProofs-Gen [34] contains around 14.5k theorems for informal proof gener-
ation. Moreover, FM-bench [6] constructed 18k high-quality instruction-response
pairs across five mainstream formal specification languages (Coq, Lean4, Dafny,
ACSL, and TLA+). For model checking, there are few benchmarks and
datasets. FM-bench [6] includes benchmarks in TLA+ that evaluates the LLMs’
ability to turn informal language to formal specification. So Model-Bench
takes the first step in auto modeling from programs with LLMs.


3     Benchmark Construction

3.1   Data Processing

The workflow of data processing for Model-Bench is illustrated in Figure 1.
    Data Sources Model-Bench originates from three Python benchmarks for
LLM evaluation: HumanEval, MBPP and LiveCodeBench. We select them be-
cause they are the most widely known and commonly used function-level bench-
marks. All of them provide problem-wise testcases, allowing Model-Bench to
validate the correctness of the generated TLA+ models.
    Fetching and Normalization The workflow begins with the data collec-
tion, where we download all three raw datasets from Hugging Face(HumanEval,
MBPP, LiveCodeBench) [1]. The code solutions in Python and the correspond-
ing test cases are extracted from the raw datasets. In order to standardize our
benchmark and ensure consistent evaluation, each problem is de-duplicated, nor-
malized and combined into an isolated Python file with a function and test
assertions.
    Simplification and rewrite Our focus is on how LLMs abstract and model
the core program logic rather than translating every line of code with com-
plex high-level syntax. However, Python is a programming language equipped
4              Chen et al.

                                                   Fetching and Normalization

    Prompt




    Solution




     Tests




                                                   Simplification and Rewrite
          (1) Filter libraries                                                        (3) Filter types     (4) Execute
                                          (2) Rewrite language features
                                                                                                         Prompt derivation



                                                       gpt-4o

                                 Any instance of failed rewriting will be discarded




                                      Fig. 1. Overview of Data Processing



with rich built-in libraries and modern language features that cannot be easily
expressed in modeling languages like TLA+. Therefore, we take the following
aspects to pick and rewrite those bench cases that satisfied our goals. (1) Li-
braries. For built-in libraries, we eliminate all Python code that imports li-
braries other than typing and math. Having LLMs continuously generate code
for all complex dependencies and their nested dependencies would deviate from
our research focus. We retain typing because its usage does not affect the code
logic in any way and these dependencies can be completely ignored during model-
ing. We also keep math since it contains convenient mathematical functions that
are typically simple and commonly used. (2) Language features. For language
features, we identify those that require treatment: multiple function declarations,
recursion, list comprehension, slice operations, classes, lambda expressions, and
generators. Instead of directly discarding these programs, we perform prepro-
cessing and instructing LLMs to equivalently rewrite all programs with these
features using the prompt shown in Figure 11. Only after multiple rewriting at-
tempts were problems that still fail to run or meet the requirements discarded.
(3) Types. Finally, we exclude Python problems involving variables with com-
plex types beyond None, Number, String, and their derived List, Tuple, Dict
and Iter, as these types are difficult to represent in TLA+. Our statistics show
that this filtering only eliminates a negligible portion of Python problems. (4)
Execution. Subsequently, the Python problem files undergo execution to verify
their functionality and accuracy, with all problematic files that fail this verifica-
tion process being eliminated. The code must also be acceptable and processable
by our code transformer.
                                   Can Large Language Models Model Programs Formally?                                                                   5

         Input Python Code                                   Control-flow Graph                             Transformed Code
   def sum_even(arr):                                                                              def sum_even(arr):
                                                                                                       n: any
       n = len(arr)                                                                                    i: any
       i = 0                                                         Entry                             s: any
       s = 0                                                                                           ret: any
                                                                                                       pc = 0
       while i < n:                                                                                    while True:
           if arr[i] % 2 == 0:                                                                             if pc == 0 and True:
                s += arr[i]                                                                                     pc = 2
           i += 1                                                 n = len(arr)                                  n = len(arr)
                                                                                                                i = 0
       return s                                                   i=0                                           s = 0
                                                                  s=0                                           arr, ret = arr, ret
        TLA+ Model (Partial)                                                                               if pc == 2 and True:
                                                                                                                pc = 3
   SumEven ==                                                                                                   arr, i, n, ret, s = arr, i, n, ret, s
      \/ /\ pc = 0                                                                                         if pc == 3 and i < n:
         /\ pc' = 2                                                                                             pc = 5
         /\ n' = Len(arr)                                                                                       arr, i, n, ret, s = arr, i, n, ret, s
         /\ i' = 0                                                 While test                              if pc == 3 and not i < n:
                                                                                                                pc = 4
         /\ s' = 0
                                                                                                                ret = s
      \/ /\ pc = 2
                                                                                                               return
         /\ pc' = 3                                          Not(i < n) i < n                              if pc == 4 and True:
      \/ /\ pc = 3 /\ i < n                                                                                     pc = 1
         /\ pc' = 5                                                                                             arr, i, n, ret, s = arr, i, n, ret, s
      \/ /\ pc' = 3 /\ i >= n                                                                              if pc == 5 and not arr[i] % 2 == 0:
         /\ ret' = s                        return s                                                            pc = 6
         /\ pc' = 4                                                                                             i += 1
      \/ /\ pc = 4                                                                                              arr, n, ret, s = arr, n, ret, s
         /\ pc' = 1 \* Return                                                    arr[i] % 2 == 0           if pc == 5 and arr[i] % 2 == 0:
      \/ /\ pc = 5 /\ arr[i] % 2 = 0                                                                            pc = 7
                                                                                                                s += arr[i]
         /\ pc' = 6
                                                                                                                arr, i, n, ret = arr, i, n, ret
         /\ i' = i + 1
      \/ /\ pc = 5 /\ arr[i] % 2 # 0
                                           Exit        Not(arr[i] % 2 == 0)      s += arr[i]               if pc == 7 and True:
                                                                                                                pc = 6
         /\ pc' = 7                                                                                             i += 1
         /\ s' = s + arr[i]                                                                                     arr, n, ret, s = arr, n, ret, s
      \/ /\ pc = 7                                                                                         if pc == 6 and True:
         /\ pc' = 6                                                                                             pc = 3
         /\ i' = i + 1                                                             i += 1                       arr, i, n, ret, s = arr, i, n, ret, s
      \/ /\ pc = 6
         /\ pc' = 3




                                       Fig. 2. Overview of Code Transformation


    Prompt derivation For each filtered Python code, we derive three vari-
ants of the prompts from the same template shown in Figure 14: original code
supplemented with two examples, original code without examples, and trans-
formed code (Section 3.2) with two examples. The prompt template contains
fixed domain knowledge of TLA+ and instructions of common mistakes [28].
The examples are TLA+ models manually crafted from Python programs, de-
signed to provide maximum reference value for LLMs.

3.2     Code Transformation
One significant distinction between Python (or other modern high-level program-
ming languages) and TLA+ lies in their fundamental execution models. TLA+
models are essentially state machines that explicitly describe all possible pro-
gram behaviors as a set of flat, discrete events (actions), representing program
execution as a sequence of state transitions triggered by these actions. Previous
research has indicated that LLMs excel more at imitation and pattern recog-
nition rather than complex reasoning. To investigate the effectiveness of this
approach, we lower Python programs into a representation more closely aligned
with TLA+ models.
    The overview of our code transformation is shown in Figure 2. It starts with
converting Python programs into control-flow graphs(CFG), where node repre-
sent basic blocks, and edges denote either conditional or unconditional jumps
between blocks. Each basic block contains a sequence of consecutively executed
instructions, which naturally corresponds to actions in TLA+ specifications.
This structural similarity enables us to bridge the gap between the two repre-
sentations while preserving the behavior of the original program.
6      Chen et al.

                     Table 1. Data Statistics of Model-Bench


    Source    Origin Libraries Language Features Types         Execution
HumanEval        164         156              139         122          105
MBPP             427         356              334         309          262
LiveCodeBench     92          73               55          48           33
Total            683 595(-12.9%)     528 (-11.2%) 479 (-9.2%) 400 (-16.5%)




    The transformation process involves several key steps: (1) CFG construction.
We construct a CFG from the Python program’s abstract syntax tree. Control
flow statements (if/else, while/for, break/continue) are identified to par-
tition the code into basic blocks, while recording transition conditions between
blocks. Then we assign unique numerical identifiers to each node in the CFG. (2)
Code generation. We generate the transformed code following a state machine
pattern. All variables are declared at the beginning, followed by introducing a
pc variable to track the current state in the runtime. The main structure is a
while loop, containing if statements for each node, controlled by pc and transi-
tion conditions. (3) Finally, we also lower Python strings to number arrays based
on characters’ ASCII values because the strings in TLA+ are immutable. The
whole transformation process is deterministic and does not alter the semantics
of the program.


3.3   Data Statistics

The data statistics of Model-Bench are shown in Table 1. In particular, it
presents a detailed breakdown of the number of reserved problems in each stage
of data processing above. The "Origin" column represents the original bench-
mark size for each dataset. Each subsequent column corresponds to the number
of problems remaining after applying the filtering steps described in Section 3.1,
with each step based on the results of the previous one. Our filtering process re-
sulted in the elimination of approximately 41.4% of the initial dataset, compris-
ing 26.2% from HumanEval, 65.5% from MBPP, and 8.3% from LiveCodeBench.
The sequential filtering stages exhibited rates of 12.9%, 11.2%, 9.2%, and 16.5%
respectively, representing reasonable attrition levels for maintaining data qual-
ity.


4     Experiment Design

We instruct LLMs to model the program across three prompt settings, conduct-
ing three sampling trials for each. In these trials, LLMs self-correct via error
feedback and iterative multi-turn chats. We also perform post-processing on the
models generated by LLMs (Section A.1). The processed models are evaluated
using TLC [41] and two metrics (Section 4.1).
                    Can Large Language Models Model Programs Formally?           7

4.1   Evaluation Design
Evaluation Preparation. We employ GPT-4o to generate a TLA+ model
for each Python program. After that, Three practitioners with over three years
of experience in programing spend two months comparing the semantics of the
generated TLA+ models and the original Python code from both the source code
and state diagram perspectives. Through manual verification and refinement, we
ensure the correctness and quality of the oracle models. These models serve as the
ground truth for evaluating the similarity (defined below) of models generated
by LLMs.

Evaluation Metrics Runnable@k: derived from Pass@k [8], a popular metric
in LLM evaluation:
                                       "         !     !#
                                              n−c    n
                      Runnable@k = E 1 −           /                            (1)
                                               k     k

 Here, we define it as the proportion of models that TLC checks without failures
at least once within k generated models. For each problem, n solutions are sam-
pled from an LLM, and c of n solutions are correct. Considering the time and
cost, we set n to 3 and k to 1, 2, 3 for each model sampling.
    Previous research has demonstrated that LLMs may not strictly adhere to
prompts [27]. To verify whether the LLM-generated models align with the orig-
inal programs, rather than being complete rewrites, we introduce a formal sim-
ilarity metric. Before introducing the metric itself, we first clarify the concepts
of states and state traces.

Definition 1. Given a model M , the state at time t, denoted as State(M, t), is
defined as the set of variable-value pairs at that step:

                  State(M, t) = {(v, val(v, t)) | v ∈ V ars(M )}

where V ars(M ) is the set of variables in M , and val(v, t) denotes the value of
variable v at time t.

  The execution trace of a model consists of all states observed during its run.
We formalize this as follows.

Definition 2. For a model M , the set of all observed
                                               S      states during execution,
denoted States(M ), is given by: States(M ) = t State(M, t), where t ranges
over all time steps in the execution trace.

    Let Mo denote the oracle (original) model, and Mg denote the LLM-generated
model. We measure their similarity as the proportion of states in Mo that are
also present in Mg :

Definition 3 (Similarity). Given two models Mo and Mg , their similarity is
                                   |{s|s∈States(Mo )∩States(Mg )}|
defined as: Similarity(Mo , Mg ) =          |States(Mo )|
8       Chen et al.

   Two states State1 and State2 are considered sufficiently similar, if and
only if the proportion of variable values in Stateg that also exist in Stateo is
greater than or equal to a threshold θ ∈ [0, 1]. Formally,

Definition 4. Given two states Stateo and Stateg , we define the matching set:

                  M atchingSet = { (vg , valg (vg , tg )) ∈ Stateg |
                                      ∃(vo , valo (vo , to )) ∈ Stateo ,
                                      valg (vg , tg ) = valo (vo , to ) }

The two states are considered sufficiently similar if |M atchingSet|
                                                         |Stateg |   ≥ θ, where
θ ∈ [0, 1] is a predefined threshold.

    We set the threshold θ to 1.0 to ensure that all variable-value pairs in the
state of the generate model must be present in the state of the oracle model, i.e.,
no discrepancies or noise. Note that higher Runnable@k doesn’t mean higher
similarity. This metric represents a compromise, given the challenge of fully
assessing whether the execution process and semantics of the program and the
model are entirely aligned.
    Suppose that one state in the oracle model is given by Stateo1 = {a = 1, b =
2}, and one state in the generated model is given by Stateg1 = {b = 2, pc =
3, a = 1}. According to the definition above, the similarity between these two
states is 1.0. This example also illustrates an important property of the metric: it
eliminates the bias introduced by additional auxiliary variables in the generated
model, as well as by the reordering of variables.


5   Evaluation

We use nucleus sampling [16] in line with recent works [7,12,4,40]. All solu-
tion samples are randomly generated with a temperature of 0.7 [35], which is
the default temperature of ChatGPT. Due to computational constraints, only
the Gemma and Llama models are run on our local server equipped with two
NVIDIA RTX 6000 Ada GPUs (each with 48GB of graphic memory). The re-
maining models are executed through the SiliconFlow API [2].
    The research questions (RQs) were designed as follows:

– RQ1. Overall Performance. We first show the overall performance of the
  studied LLMs on Model-Bench. We use three sets of prompts to generate
  modelings for all Python code. The comprehensive results are displayed with
  multiple metrics.
– RQ2. Effectiveness of Code Transformation. The transformed code (Sec-
  tion 3.2) more closely resembles the form of a TLA+ model. We thus explore
  how this approach affects different LLMs.
– RQ3. Impact of Source Code Syntactic Complexity. Research indi-
  cated that the accuracy of code generated by LLMs is negatively correlated
                           Can Large Language Models Model Programs Formally?                               9

                          Table 2. Overall Results on Model-Bench


          Model               Runnable@1 (%) Runnable@2 (%) Runnable@3 (%) Avg Similarity (%) Avg Fixes
                                               Original Code / Few-shot
DeepSeek-V3                  51.75               61.33            66.25           49.55           0.78
DeepSeek-V2.5                44.33               53.50            57.75           46.17           0.78
Qwen3-32B                    39.50               53.08            60.75           52.03           1.07
Qwen3-14B                    29.75               41.50            49.25           43.60           1.23
DeepSeek-R1-Distill-Qwen-32B 21.00               30.42            36.50           30.15           1.38
Qwen3-8B                     16.00               24.75            31.00           22.84           1.90
Gemma-3-12b-it               7.92                12.17            15.00           21.14           1.40
Llama-3.1-8B-Instruct        4.33                7.33             10.00           5.39            2.87
                    Average          26.82               35.51            40.81           33.86      1.43
                                              Original Code / Zero-shot
DeepSeek-V3                  37.92               52.92            61.00           4.38            2.29
DeepSeek-V2.5                12.75               21.17            27.25           3.08            2.68
Qwen3-32B                    18.08               29.75            37.75           11.90           2.49
Qwen3-14B                    1.17                1.33             1.50            0.00            4.71
DeepSeek-R1-Distill-Qwen-32B 1.08                1.17             1.25            0.00            5.00
Qwen3-8B                     1.00                1.00             1.00            0.00            5.00
Gemma-3-12b-it               1.00                1.00             1.00            0.00            5.00
Llama-3.1-8B-Instruct        1.00                1.00             1.00            0.00            5.00
                    Average          9.25                13.67            16.47           2.42       4.02
                                             Transformed Code / Few-shot
DeepSeek-V3                  43.50               51.75            56.00           68.54           0.71
DeepSeek-V2.5                39.92               48.17            52.25           61.55           0.84
Qwen3-32B                    33.42               45.42            53.25           62.64           0.68
Qwen3-14B                    26.08               37.08            44.25           57.67           1.48
DeepSeek-R1-Distill-Qwen-32B 24.00               35.08            41.25           52.95           1.69
Qwen3-8B                     16.83               25.42            31.50           50.19           1.75
Gemma-3-12b-it               7.42                10.67            12.50           39.31           2.00
Llama-3.1-8B-Instruct        5.50                8.83             11.75           40.71           2.47
                    Average          24.58               32.80            37.84           54.20      1.45




  with code complexity [30]. So we aim to explore the relationship between the
  performance of LLMs in automated modeling and the complexity of the code
  involved.
– RQ4. Bad Case Analysis. We analyze bad cases with syntactic or semantic
  errors due to various issues and identify the limitations of LLMs in TLA+
  automated modelings.


5.1    RQ1: Overall Performance

The overall performance of the studied LLMs on Model-Bench is shown in
Table 2, which lists various metrics for TLA+ models generated by each studied
model under three prompt settings (Section 3.1). Metrics include Runnable@k,
average state similarity between the TLA+ models and oracle models, as well
as the average number of fixes under Runnable@1 (Section 4.1). To better vi-
sualize the results, we use darker background colors to indicate larger values.
Only models that pass TLC verification have the opportunity to calculate state
similarity with oracle models.
10     Chen et al.

    Generally, across all prompt settings, DeepSeek-V3 demonstrates the best
performance, followed by DeepSeek-V2.5 and Qwen3-32B, achieving Runnable@1
of 51.75%, 44.33%, and 39.50%, respectively. These three models also have the
top-3 highest average similarities and lowest average fix counts, indicating they
can generate models that pass verification within fewer iterations.

 Finding 1: The Top-3 performing LLMs are DeepSeek-V3, DeepSeek-V2.5,
 and Qwen3-32B among the studied LLMs, achieving Runnable@1 rates of
 51.75%, 44.33%, and 39.50%, respectively. Their performance rankings remain
 consistent across all three prompt settings.

    Comparing few-shot and zero-shot results, all models demonstrate signif-
icantly better performance with few-shot prompt than with zero-shot, aver-
agely improving 17.57% (26.82% - 9.25%) in Runnable@1 and 31.44%(33.86% -
2.42%) in similarity. Particularly, DeepSeek-V2.5 showed a 31.58% improvement
(44.33% - 12.75%) in Runnable@1. With few-shot prompt, the three lowest-
ranking models achieve a breakthrough from near 0 Runnable@1, with Llama-
3.1-8B-Instruct improving to 4.33%, Gemma-3-12b-it reaching 7.92%, and Qwen3-
8B achieving 16.00%. For higher-ranked models, few-shot prompt also reduces
the average number of fix attempts and increases the average state similarity.
For example, DeepSeek-V2.5’s average fix attempts decrease by 1.90 (from 2.68
to 0.78), while its average state similarity improves by 46.47% (from 3.08% to
49.55%).

 Finding 2: The enhancement of few-shot learning for automatic modeling
 tasks is substantial. Notably, with zero-shot, models such as Gemma-3-12b-
 it, Llama-3.1-8B-Instruct, DeepSeek-R1-Distill-Qwen-32B, Qwen3-14B, and
 Qwen3-8B all demonstrate a nearly 0 Runnable@1 rate.

   In addition, by comparing the Runnable@1 rates of all models, we observe
that the automatic modeling task from Python to TLA+ exhibits high dis-
criminability. This finding suggests that when applying this technique in actual
industrial production, employing more powerful models often yields significant
improvements.

5.2   RQ2: Effectiveness of Code Transformation
In RQ2, we primarily compare the results of original Python code and trans-
formed Python code in a few-shot setting. By comparing the data in Table 2,
we observe that for all models, code transformation leads to a decrease in
Runnable@k, but significantly improves similarity. For instance, in the case of
the DeepSeek-V3 model, similarity increases by 18.99% (68.54% - 49.55%), while
Runnable@3 decreases by only 10.25% (66.25% - 56.00%). This indicates that
code transformation indeed provides LLMs with references that are easier to
follow and translate. We hypothesize that the decline in Runnable@k can be at-
tributed to two main factors: (1) It reduces instances where LLMs bypass TLC
                   Can Large Language Models Model Programs Formally?          11

by completely restructuring the program. (2) Code transformation increases code
length, making the “lost in the middle” [27] phenomenon more likely to occur.




             Fig. 3. Venn Diagram of Ensemble based on Runnable@3


   Figure 3 illustrates the complementary effects of the two prompt settings
based on Runnable@3. More results are demonstrated in Figure 8. Assembling
the results from both prompt settings proves to be effective, e.g., for Qwen3-32B,
prompting with transformed code yields an additional 13.75% runnable TLA+
models from Python programs, compared that with the original code alone.

 Finding 3: Code transformation significantly improves similarity while only
 leads to a small decrease in Runnable@k. It can still serve as a complemen-
 tary technique for all models when combined with original code prompting,
 increasing the total number of runnable models.


5.3   RQ3: Impact of Source Code Syntactic Complexity




          Fig. 4. Relationship between Runnable@1 and Code Complexity


   This section aims to explore the relationship between the performance of
LLMs in automated modeling and the complexity of the code involved. We cal-
culate cyclomatic complexity with the Radon library which is also used by pre-
vious work [30], max loop depth, and the number of variables for each original
Python code in advance. We group all problems according to these metrics sep-
arately and calculate the proportion of samples in each group that successfully
passed the TLC check based on the Runnable@1 results across all models. Fig-
12     Chen et al.

ure 4 illustrates the relationship between these complexity metrics and modeling
success rates.
   We also collect difficulty ratings for Python programs from LiveCodeBench,
where these ratings correspond to the difficulty of the problems rather than the
complexity of the code. Figure 4 shows the Runnable@k of all models across the
three original problem difficulty distributions.

 Finding 4: Python programs with higher syntactic complexity, i.e., those
 exhibiting higher cyclomatic complexity, larger loop depth, and a greater
 number of variables, demonstrate lower Runnable@k as well as similarity
 when automatically translated into TLA+ models using LLMs.



5.4   RQ4: Bad Case Analysis

This section discusses cases that cannot pass TLC verification, including sce-
narios where the generated TLA+ model contains compilation errors, runtime
errors, or fails to satisfy assertion properties. Since TLC categorizes errors in a
coarse-grained manner via exit codes, we can only roughly determine the cause
through manual judgment. These kind of failures also demonstrates that the
difference between Python and TLA+ makes automated modeling and code
translation hard. More bad cases are demonstrated in Section A.3


Compilation Error Compilation errors indicate that, as a result of insufficient
training data or inadequate contextual information, LLMs fail to produce TLA+
code that is syntactically or semantically correct.
    Compilation Error 1: Unknown Operator. Figure 5 shows an error
caused by the absence of sort function, which is a built-in function existing in
Python. Although we can make LLMs aware of this issue through multiple rounds
of chat, such iterative interactions may also continuously introduce new unknown
operators. The differences in built-in libraries between the two languages further
increase the difficulty of automatic modeling.


Runtime Error Runtime errors are another type of result stemming from
LLMs’ lack of attention to differences between languages. Unlike compilation
errors, correcting such errors requires LLMs to have a deeper understanding of
language specifications.
    Runtime Error 1: One-based Array Index. Figure 6 shows the error of
array index out of bounds. In the Python code, initializing i as 1 leads to the
first iteration accessing dp[0]. However, in TLA+, array indices start from 1,
which means that dp[0] is an invalid access. One-based arrays are uncommon
in most programming languages. Although we explicitly mentioned this in the
prompt, LLMs still get lost in the middle of long contexts.
                                    Can Large Language Models Model Programs Formally?                                                                  13

def sort_third(l):                                                          --------------------------- MODULE SortThird ----------------------------
    """This function takes a list l and returns a list l' such that         EXTENDS Naturals, Integers, Reals, Sequences, FiniteSets, TLC
    l' is identical to l in the indices that are not divisible by three,    VARIABLES l, result, third_indices, i, third_index, ret, initl, pc
    while its values at the indices that are divisible by three are equal   vars == <<l, result, third_indices, i, third_index, ret, initl, pc>>
    to the values of the corresponding indices of l, but sorted.
    >>> sort_third([1, 2, 3])                                               Init == \* ...
    [1, 2, 3]
\                                                                           SortThird ==
    result = []                                                               \* ...
    third_indices = []                                                        \/ /\ pc = 4
                                                                                  /\ pc' = 9
    for i in range(len(l)):                                                       /\ third_indices' = Sort(third_indices)
        if i % 3 == 0:                                                            /\ i' = 0
            third_indices.append(l[i])                                            /\ third_index' = 0
            result.append(None) # Placeholder for sorting later                   /\ result' = result
        else:                                                                     /\ initl' = initl
            result.append(l[i])                                                   /\ ret' = ret
                                                                                  /\ l' = l
    third_indices.sort()
                                                                            Next == SortThird
    third_index = 0
    for i in range(len(result)):                                            Spec ==
        if result[i] is None:                                                 /\ Init
            result[i] = third_indices[third_index]                            /\ [][Next]_vars
            third_index += 1
                                                                            Assertion == \* ...
    return result                                                           =============================================================================




                                Fig. 5. Compilation Error 1. Unknown Operator

def lengthOfLongestSubsequence(nums, sum):                                  ---------------- MODULE LengthOfLongestSubsequence ------------------
    n = len(nums)                                                           \* ...
    dp = []
    for i in range(n + 1):                                                  Init == \* ...
        dp.append([-1] * (sum + 1))
                                                                            Next ==
    for i in range(n + 1):                                                    \/ /\ pc = 6
        dp[i][0] = 0                                                             /\ i >= n + 1
                                                                                 /\ pc' = 7
    for i in range(1, n + 1):                                                    /\ i' = 1
        for j in range(1, sum + 1):                                           \* ...
            dp[i][j] = dp[i - 1][j]                                           \/ /\ pc = 12
            if j >= nums[i - 1] and dp[i - 1][j - nums[i - 1]] != -1:            /\ j < sum + 1
                dp[i][j] = max(1 + dp[i - 1][j - nums[i - 1]], dp[i][j])         /\ pc' = 14
                                                                                 /\ j' = j + 1
    return dp[n][sum]                                                            /\ dp' = [dp EXCEPT ![i] = [dp[i] EXCEPT ![j+1] = dp[i-1][j+1]]]
                                                                                 /\ UNCHANGED <<n, initsum, i, sum, nums, initnums, ret>>
assert lengthOfLongestSubsequence([1, 1, 5, 4, 5], 3) == -1                 =============================================================================




                                Fig. 6. Runtime Error 1. One-based Array Index


Assertion Error Assertion errors occur not because LLMs omit the logic in
the Python code. This stands in contrast to the two types of errors discussed
earlier, as the essence of these errors is rooted in this excessive fidelity to the
source code.
    Assertion Error 1: Omission of Function-call. Figure 7 demonstrates
the reason behind the assertion error. The LLMs fail to include the .lower()
function-call in Python, which leads to the test cases not passing.
    Assertion Error 2: Constant Loop Count. Figure ?? illustrates a case
where LLMs directly use the constant MaxLen, which originally intends to con-
strain the initial variable search space, as the maximum loop count for traversing
an array under arbitrary inputs. The correct way is to use Len(arr).


6       Conclusion

In this paper, we introduce Model-Bench, a benchmark and an accompany-
ing pipeline for evaluating and improving LLMs’ program modeling capability
by modeling Python programs into verification-ready model checking specifica-
tions checkable by its accompanying model checker. Model-Bench comprises
400 Python programs derived from three well-known benchmarks (HumanEval,
14            Chen et al.

def check_if_last_char_is_a_letter(txt):                                   ----------------------- MODULE CheckIfLastCharIsALetter ---------------------
    '''                                                                    \* ...
    Create a function that returns True if the last character
    of a given string is an alphabetical character and is not              Init == \* ...
    a part of a word, and False otherwise.
    Note: "word" is a group of characters separated by space.              CheckIfLastCharIsALetter ==
                                                                             LET IsLetter(c) == /\ Len(c) = 1 /\ 97 <= c[1] /\ c[1] <= 122
     Examples:                                                               IN
     check_if_last_char_is_a_letter("apple pie") ➞ False                     /\ \/ /\ pc = 0
     check_if_last_char_is_a_letter("apple pi e") ➞ True                           /\ check' = check[Len(check)]
     check_if_last_char_is_a_letter("apple pi e ") ➞ False                         /\ ret' = IsLetter(check')
     check_if_last_char_is_a_letter("") ➞ False                                    /\ pc' = 1
     '''                                                                           /\ UNCHANGED <<inittxt, txt>>

    check = txt.split(' ')[-1]
    return True if len(check) == 1 and (97 <= ord(check.lower()) <= 122)   \* ...
else False                                                                 =============================================================================




                              Fig. 7. Assertion Error 1. Omission of Function-call


MBPP, and LiveCodeBench). Our benchmark collection methodology and eval-
uation metrics demonstrate scalability, allowing for future extension to other
programming languages. Our extensive experiments reveal significant limitations
in LLMs’ program modeling and further provide inspiring directions. We hope
Model-Bench could drive progress in automated formal verification, especially
for model checking, and encourage the development of more sophisticated rea-
soning capabilities in future LLMs.


References
 1. Hugging face (2016), https://huggingface.co/
 2. Siliconflow (2023), https://siliconflow.cn
 3. Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E.,
    Cai, C., Terry, M., Le, Q., et al.: Program synthesis with large language models.
    arXiv preprint arXiv:2108.07732 (2021)
 4. Cao, J., Chen, Z., Wu, J., Cheung, S.C., Xu, C.: Javabench: A benchmark of object-
    oriented code generation for evaluating large language models. In: Proceedings of
    the 39th IEEE/ACM International Conference on Automated Software Engineer-
    ing. pp. 870–882 (2024)
 5. Cao, J., Lu, Y., Li, M., Ma, H., Li, H., He, M., Wen, C., Sun, L., Zhang, H.,
    Qin, S., Cheung, S.C., Tian, C.: From informal to formal – incorporating and
    evaluating llms on natural language requirements to verifiable formal proofs (2025),
    https://arxiv.org/abs/2501.16207
 6. Cao, J., Lu, Y., Li, M., Ma, H., Li, H., He, M., Wen, C., Sun, L., Zhang, H., Qin,
    S., et al.: From informal to formal–incorporating and evaluating llms on natural
    language requirements to verifiable formal proofs. arXiv preprint arXiv:2501.16207
    (2025)
 7. Cao, J., Zhang, W., Cheung, S.C.: Concerned with data contamination? assessing
    countermeasures in code language model. arXiv preprint arXiv:2403.16898 (2024)
 8. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.D.O., Kaplan, J., Edwards,
    H., Burda, Y., Joseph, N., Brockman, G., et al.: Evaluating large language models
    trained on code. arXiv preprint arXiv:2107.03374 (2021)
 9. Clarke, E.M.: Model checking. In: International conference on foundations of soft-
    ware technology and theoretical computer science. pp. 54–56. Springer (1997)
10. Cosler, M., Hahn, C., Mendoza, D., Schmitt, F., Trippel, C.: nl2spec: Interactively
    translating unstructured natural language to temporal logics with large language
                     Can Large Language Models Model Programs Formally?               15

    models. In: International Conference on Computer Aided Verification. pp. 383–396.
    Springer (2023)
11. Curaba, C., D’Ambrosi, D., Minisini, A., Antolín, N.P.C.: Cryptoformaleval: Inte-
    grating llms and formal verification for automated cryptographic protocol vulner-
    ability detection. arXiv preprint arXiv:2411.13627 (2024)
12. Du, X., Liu, M., Wang, K., Wang, H., Liu, J., Chen, Y., Feng, J., Sha, C., Peng, X.,
    Lou, Y.: Classeval: A manually-crafted benchmark for evaluating llms on class-level
    code generation. arXiv preprint arXiv:2308.01861 (2023)
13. Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur,
    A., Schelten, A., Yang, A., Fan, A., et al.: The llama 3 herd of models. arXiv
    e-prints pp. arXiv–2407 (2024)
14. Ferreira, D., Freitas, A.: Natural language premise selection: Finding supporting
    statements for mathematical text. arXiv preprint arXiv:2004.14959 (2020)
15. Giannakopoulou, D., Pressburger, T., Mavridou, A., Schumann, J.: Generation of
    formal requirements from structured natural language. In: International working
    conference on requirements engineering: Foundation for software quality. pp. 19–35.
    Springer (2020)
16. Holtzman, A., Buys, J., Du, L., Forbes, M., Choi, Y.: The curious case of neural
    text degeneration. arXiv preprint arXiv:1904.09751 (2019)
17. Huang, Y., Lin, X., Liu, Z., Cao, Q., Xin, H., Wang, H., Li, Z., Song, L., Liang, X.:
    Mustard: Mastering uniform synthesis of theorem and proof data. arXiv preprint
    arXiv:2402.08957 (2024)
18. Jain, N., Han, K., Gu, A., Li, W.D., Yan, F., Zhang, T., Wang, S., Solar-Lezama,
    A., Sen, K., Stoica, I.: Livecodebench: Holistic and contamination free evaluation
    of large language models for code. arXiv preprint arXiv:2403.07974 (2024)
19. Jiang, A.Q., Li, W., Jamnik, M.: Multi-language diversity benefits autoformaliza-
    tion. Advances in Neural Information Processing Systems 37, 83600–83626 (2024)
20. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Miłoś, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers. Advances in Neural Information Processing Systems
    35, 8360–8373 (2022)
21. Lamport, L.: Specifying systems (2002)
22. Li, Z., Sun, J., Murphy, L., Su, Q., Li, Z., Zhang, X., Yang, K., Si, X.: A survey
    on deep learning for theorem proving. arXiv preprint arXiv:2404.09939 (2024)
23. Lin, X., Cao, Q., Huang, Y., Wang, H., Lu, J., Liu, Z., Song, L., Liang, X.: Fvel:
    Interactive formal verification environment with large language models via theo-
    rem proving. Advances in Neural Information Processing Systems 37, 54932–54946
    (2024)
24. Ling, Z., Fang, Y., Li, X., Huang, Z., Lee, M., Memisevic, R., Su, H.: Deductive ver-
    ification of chain-of-thought reasoning. Advances in Neural Information Processing
    Systems 36, 36407–36433 (2023)
25. Liu, A., Feng, B., Wang, B., Wang, B., Liu, B., Zhao, C., Dengr, C., Ruan, C.,
    Dai, D., Guo, D., et al.: Deepseek-v2: A strong, economical, and efficient mixture-
    of-experts language model. arXiv preprint arXiv:2405.04434 (2024)
26. Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao, C., Deng, C., Zhang,
    C., Ruan, C., et al.: Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437
    (2024)
27. Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang,
    P.: Lost in the middle: How language models use long contexts. arXiv preprint
    arXiv:2307.03172 (2023)
16      Chen et al.

28. Lu, M., Delaware, B., Zhang, T.: Proof automation with large language models.
    In: Proceedings of the 39th IEEE/ACM International Conference on Automated
    Software Engineering. pp. 1509–1520 (2024)
29. Mao, Z., Wang, J., Sun, J., Qin, S., Xiong, J.: Llm-aided automatic modelling for
    security protocol verification. In: 2025 IEEE/ACM 47th International Conference
    on Software Engineering (ICSE). pp. 734–734. IEEE Computer Society (2025)
30. Sepidband, M., Taherkhani, H., Wang, S., Hemmati, H.: Enhancing llm-based code
    generation with complexity metrics: A feedback-driven approach. arXiv preprint
    arXiv:2505.23953 (2025)
31. Team, G., Kamath, A., Ferret, J., Pathak, S., Vieillard, N., Merhej, R., Perrin, S.,
    Matejovicova, T., Ramé, A., Rivière, M., et al.: Gemma 3 technical report. arXiv
    preprint arXiv:2503.19786 (2025)
32. Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q., Huang, Y., Xiong, J., Shi,
    H., Xie, E., et al.: Lego-prover: Neural theorem proving with growing libraries.
    arXiv preprint arXiv:2310.00656 (2023)
33. Welleck, S., Liu, J., Bras, R.L., Hajishirzi, H., Choi, Y., Cho, K.: Natu-
    ralproofs: Mathematical theorem proving in natural language. arXiv preprint
    arXiv:2104.01112 (2021)
34. Welleck, S., Liu, J., Lu, X., Hajishirzi, H., Choi, Y.: Naturalprover: Grounded
    mathematical proof generation with language models. Advances in Neural Infor-
    mation Processing Systems 35, 4913–4927 (2022)
35. Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S.C., Tian, C.:
    Enchanting program specification synthesis by large language models using static
    analysis and program verification. In: International Conference on Computer Aided
    Verification. pp. 302–328. Springer (2024)
36. Wu, Y., Jiang, A.Q., Li, W., Rabe, M., Staats, C., Jamnik, M., Szegedy, C.: Auto-
    formalization with large language models. Advances in neural information process-
    ing systems 35, 32353–32368 (2022)
37. Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang,
    C., Lv, C., et al.: Qwen3 technical report. arXiv preprint arXiv:2505.09388 (2025)
38. Yang, J., Wang, Y.: Toward auto-modeling of formal verification for nextg proto-
    cols: A multimodal cross-and self-attention large language model approach. IEEE
    Access 12, 27858–27869 (2024)
39. Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger,
    R.J., Anandkumar, A.: Leandojo: Theorem proving with retrieval-augmented lan-
    guage models. Advances in Neural Information Processing Systems 36, 21573–
    21612 (2023)
40. Yu, H., Shen, B., Ran, D., Zhang, J., Zhang, Q., Ma, Y., Liang, G., Li, Y., Wang, Q.,
    Xie, T.: Codereval: A benchmark of pragmatic code generation with generative pre-
    trained models. In: Proceedings of the 46th IEEE/ACM International Conference
    on Software Engineering. pp. 1–12 (2024)
41. Yu, Y., Manolios, P., Lamport, L.: Model checking tla+ specifications. In: Ad-
    vanced research working conference on correct hardware design and verification
    methods. pp. 54–66. Springer (1999)
42. Zhai, J., Shi, Y., Pan, M., Zhou, G., Liu, Y., Fang, C., Ma, S., Tan, L., Zhang,
    X.: C2s: translating natural language comments to formal program specifications.
    In: Proceedings of the 28th ACM joint meeting on European software engineering
    conference and symposium on the foundations of software engineering. pp. 25–37
    (2020)
43. Zhou, Y.: Retrieval-augmented tlaps proof generation with large language models.
    arXiv preprint arXiv:2501.03073 (2025)
                   Can Large Language Models Model Programs Formally?          17

                    Table 3. Studied Large Language Models


        Model Family            Model             Size     Time
        DeepSeek     DeepSeek-V3[26]              685B Dec, 2024
        DeepSeek     DeepSeek-V2.5[25]            236B May, 2024
        Qwen         Qwen3-8B[37]                 8.19B May, 2025
        Qwen         Qwen3-14B[37]                14.8B May, 2025
        Qwen         Qwen3-32B[37]                32.8B May, 2025
        Qwen         DeepSeek-R1-Distill-Qwen-32B 32.8B July, 2024
        Gemma        Gemma-3-12B-it[31]           12.2B March, 2025
        Llama        Llama-3.1-8B-Instruct[13]    8.03B July, 2024




A     Appendix

A.1   Post Processing

Given the limited availability of training data for TLA+ compared to main-
stream programming languages, we observe that LLMs tend to make trivial
but patterned errors (see below). To ensure more meaningful observations, we
conduct post-processing for every generated output. In particular, the post-
processing consists of three steps: (1) Import all built-in modules. We auto-
matically incorporate all built-in TLA+ modules through the EXTENDS keyword,
ensuring access to fundamental operators and definitions required for formal
specification. (2) Define null model values. To achieve better correspondence
with Python, we introduce None and Null as model values in the specifications.
(3) Complete unchanged variables. We implement comprehensive handling of the
UNCHANGED variables to ensure that each action’s resulting state is complete.
    These post-processing steps effectively eliminate common errors that would
otherwise impede the validity of our experimental results. This approach allows
us to focus on evaluating the substantive aspects of the LLMs’ ability to generate
formal specifications.


A.2   Studied Large Language Models

The studied LLMs are listed in Table 3. We focus on recent LLMs released after
2024. We primarily choose the DeepSeek and Qwen model families, which are
the strongest open-source models according to public leaderboards. We specif-
ically include Qwen3-8B, Qwen3-14B, and Qwen3-32B to evaluate how model
performance scales with different parameter count within the same family. We
incorporate Gemma and Llama to ensure model diversity. Note that we delib-
erately exclude GPT-series models from OpenAI to ensure fairness, as our later
comparison between LLM-generated TLA+ models and oracle models relies on
human-corrected outputs based on GPT’s generations.
18     Chen et al.




                   Fig. 8. Venn Diagram of Ensemble based on Runnable@3


A.3   Evaluation Supplement

RQ2: Effectiveness of Code Transformation


RQ4: Bad Case Analysis Compilation Error 2: Unexpected Token.
Figure 9 shows an error caused by invalid string concatenation operator. Python
uses + to concatenate two string while TLA+ should use \o. LLMs lack this
knowledge, so it generate unexpected tokens as a result.

        def finalString(s: str) -> str:              --------------------------- MODULE FinalString ----------------------------
            while "i" in s:                          EXTENDS Naturals, Integers, Reals, Sequences, FiniteSets, TLC
                index = s.index("i")                 VARIABLES s, init_s, ret, pc, first, index, j, second
                                                     vars == <<s, init_s, ret, pc, first, index, j, second>>
                first = ""
                for j in range(index - 1, -1, -1):   Init == \* ...
                    first += s[j]
                                                     FinalString ==
                second = ""                              \* ...
                for j in range(index + 1, len(s)):       \/ /\ pc = 9
                    second += s[j]                          /\ j >= LenS
                                                            /\ pc' = 10
                s = first + second                          /\ s' = first @ second
            return s                                        /\ UNCHANGED <<first, index, j, init_s, second>>
                                                     \* ...
        assert finalString('poiinter') == 'ponter'   =============================================================================




                              Fig. 9. Compilation Error 2. Unexpected Token


    Runtime Error 2: Indexing String. Figure 10 illustrates the error that oc-
curs when attempting to index the string ALPHABET in TLA+. While in Python,
programmers can access individual characters in a string using array-like index-
ing, this operation is invalid in TLA+, causing runtime errors.
                                    Can Large Language Models Model Programs Formally?                                                              19

def encrypt(s):                                                           --------------------------- MODULE Encrypt ----------------------------
    """Create a function encrypt that takes a string as an argument and   EXTENDS Naturals, Integers, Sequences, TLC
    returns a string encrypted with the alphabet being rotated.           CONSTANTS MaxLen
    The alphabet should be rotated in a manner such that the letters      VARIABLES s, i, out, pc, ret
    shift down by two multiplied to two places.                           vars == <<s, i, out, pc, ret>>
    For example:
    encrypt('hi') returns 'lm'                                            ALPHABET == "abcdefghijklmnopqrstuvwxyz"
    encrypt('asdfghjkl') returns 'ewhjklnop'                              Init ==
    encrypt('gf') returns 'kj'                                              /\ s = << "h", "i" >>
    encrypt('et') returns 'ix'                                              /\ i = 1
    """                                                                     /\ out = <<>>
    d = 'abcdefghijklmnopqrstuvwxyz'                                        /\ pc = 0
    out = ''                                                                /\ ret = <<>>
    for c in s:
        if c in d:                                                        IndexInAlphabet(c) == CHOOSE pos \in 1..LenAlphabet : ALPHABET[pos] = c
             out += d[(d.index(c)+2*2) % 26]
        else:                                                             \* …
             out += c
    return out                                                            =============================================================================




                                      Fig. 10. Runtime Error 2. Indexing String


A.4         Prompt Design



      Prompt for rewriting code of problems

      # System Prompt
      You are a Python expert. Please refactor the user’s Python code into equivalent
      code following these rules:
      1. Avoid using list comprehensions like [x*2 for x in range(5)]. Use traditional
      for loops instead.
      2. Avoid using slicing operations like array[1:4]. Use loops to access elements
      individually.
      3. Avoid using classes with self references like “class Calculator: def add(self, x,
      y)”. Use standalone functions.
      4. Avoid using lambda functions like “lambda x: x + 1”. Use regular named
      functions.
      5. Avoid using generator expressions like “(x for x in range(5))”. Use regular
      loops and lists.
      6. Write single, non-recursive functions instead of recursive ones like “def fac-
      torial(n): return n * factorial(n-1)”.
      Please output the refactored code directly without any additional explanations.
      # User Prompt
      - Original Python code goes here -


                               Fig. 11. Prompt for Rewriting Code of Problems
20       Chen et al.




     Prompt for fix

     The TLA+ specification has the following error:
     - error message -
     Please fix the specification while keeping the same logic.


                               Fig. 12. Prompt for Fixing




     Config template for running TLC

     CONSTANTS
     - constants -
     NONE = NONE
     NULL = NULL

     SPECIFICATION
     Spec

     INVARIANT
     Assertion

     CHECK_DEADLOCK FALSE


                       Fig. 13. Config Template for Running TLC
                 Can Large Language Models Model Programs Formally?              21

Prompt for generating TLA+ models

# Role description
As an expert in TLA+, you are good at understanding and writing TLA+.
TLA+ is a formal specification language used for modeling and verifying
concurrent and distributed systems.

# Domain knowledge
1. The logical operators supported by TLA+ include:
/ (and), \/ (or), ∼ (not), => (Implication), <=> (Bidirectional
implication), TRUE, FALSE, \A (Universal Quantification), \E
(Existential Quantification)

2. The set operators supported by TLA+ include:
= (Equality), # (not equal), \union (Union), \intersect
(Intersection), \in (Membership), \notin (Not in), \subseteq
(Subset Equal), \ (Difference).

3. The temporal operators supported by TLA+ include:
[] x > 0
The above code is an example of [] (Always). It means that at all times, the
value of variable x is greater than 0.

<> x = 0
The above code is an example of <> (Eventually). It means that at some point
in time, the value of variable x becomes 0.

4. Built-in keywords and operators in TLA+ include:
MODULE, EXTENDS, CONSTANTS, INSTANCE, VARIABLE, ASSUME, PROVE,
INIT, NEXT, ACTION, SPECIFICATION, IF, ELSE, WITH, CASE, THEN,
LET, IN, CHOOSE, ENABLED, UNCHANGED, DOMAIN.

Based on the information and python code with assertions, give a complete
TLA+ model code in only one single code block without explanations.
The model should initialize a set of all possible states constrained by max or
min CONSTANTs instead of fixed inputs.
1. Use LET keyword if there’s any temporary variable.
2. Each step should define all variables, even though keep them unchange.
3. Since the start index in TLA+ is 1 instead of 0, you may change the corre-
sponding initialization, checks, and assignment.
4. Don’t declare parameters with same names as variables or constants.
5. Define arrays like arr \in [1..MaxLen -> 0..MaxValue].
If there are assertions in the code, you should also generate a corresponding
Assertion == action.

For example:
- example1 -
- example2 -

Module Name: - module_name -
- code -


               Fig. 14. Prompt for Generating TLA+ Models
