                                                       Self-Edit: Fault-Aware Code Editor for Code Generation

                                                               Kechi Zhang, Zhuo Li, Jia Li ♂, Ge Li∗, Zhi Jin∗
                                                  Key Lab of High Confidence Software Technology (PKU), Ministry of Education
                                                              School of Computer Science, Peking University, China
                                                         {zhangkechi,lizhmq}@pku.edu.cn, lijia@stu.pku.edu.cn,
                                                                         {lige,zhijin}@pku.edu.cn


                                                                Abstract                                                   write              execute on
                                                                                                                                                                        refine and debug            submit
                                                                                                                      an initial code      example test cases
                                                                                                 Human Programmers
                                              Large language models (LLMs) have demon-
                                                                                                                    generate an initial   execute on example               refine with
                                              strated an impressive ability to generate codes                        code from LLM            test cases              a neural-based editor
                                                                                                                                                                                                    submit

                                              on competitive programming tasks. However,             Our approach
arXiv:2305.04087v5 [cs.SE] 11 Sep 2023




                                              with limited sample numbers, LLMs still suffer                                                    (a)
                                              from poor accuracy. Inspired by the process of     Problem Description:               APPS-test-673
                                                                                                 Find the smallest integer x greater than n,
                                                                                                                                                      GPT3 Output:
                                                                                                                                                      n, k = map(int, input().split())
                                              human programming, we propose a generate-          so it is divisible by the number k.
                                                                                                 The input only line contains two integers
                                                                                                                                                      if n % k == 0:
                                                                                                                                                            print n + k
                                                                                                 n and k (1 ≤ n, k ≤ 10^9).                           else:
                                              and-edit approach named Self-Edit that utilizes    -----Examples-----                                         print n + k - (n % k)
                                                                                                 Input
                                              execution results of the generated code from       5 3        example test case                         Error Message:
                                                                                                 Output                                               SyntaxError: Missing parentheses in call to 'print'.
                                              LLMs to improve the code quality on the com-       6
                                                                                                                                                      Did you mean print(n + k)?

                                              petitive programming task. We execute the gen-                                                   (b)
                                              erated code on the example test case provided     Figure 1: (a) Our approach is inspired by the problem-
                                              in the question and wrap execution results into   solving process of human programmers. (b) Output
                                              a supplementary comment. Utilizing this com-      from GPT3 model on APPS-test dataset and its corre-
                                              ment as guidance, our fault-aware code editor     sponding error message, which is obtained by running
                                              is employed to correct errors in the generated    on the example test case.
                                              code. We perform extensive evaluations across
                                              two competitive programming datasets with
                                              nine different LLMs. Compared to directly gen-       To improve the performance of LLMs on the
                                              erating from LLMs, our approach can improve       competitive programming task, we take inspiration
                                              the average of pass@1 by 89% on APPS-dev,
                                                                                                from the process of human programming. When
                                              31% on APPS-test, and 48% on HumanEval
                                              over nine popular code generation LLMs with
                                                                                                solving competitive programming problems, pro-
                                              parameter sizes ranging from 110M to 175B.        grammers usually write an initial program, execute
                                              Compared to other post-processing methods,        some example test cases, and refine the code based
                                              our method demonstrates superior accuracy and     on the test results. In this process, a programmer
                                              efficiency.                                       can take key information (e.g, program outputs or
                                         1    Introduction                                      compile/runtime error message) from the test re-
                                                                                                sults, which helps them debug the program. We
                                         Large language models (LLMs) have recently been        instantiate this idea by adopting a similar pipeline
                                         applied to the competitive programming task. This      with a neural-based editor (in Figure 1(a)). Analyz-
                                         task requires understanding a complex natural lan-     ing the code generated by a pre-trained LLM, we
                                         guage description of a problem with example test       have found that some of the generated codes can
                                         cases and correctly implementing solutions that        be improved with minor modifications. Figure 1(b)
                                         can span hundreds of lines. Solutions are evalu-       shows an example of generated code by GPT3 on
                                         ated by executing them on hidden test cases. How-      the APPS-test dataset. GPT3 generates code that
                                         ever, existing LLMs often have low accuracy and        is inconsistent with the problem description. We
                                         pass rates in this task. For example, on a popular     notice that the error message directly points out the
                                         competitive programming benchmark APPS-test            bug in the code, with which we can quickly fix the
                                         (Hendrycks et al., 2021), the nearly most powerful     error. It motivates us to investigate approaches to
                                         model GPT3 (Brown et al., 2020) achieves only 7%       edit and improve the quality of the code generated
                                         accuracy when allowed to submit only one program       by LLMs with the help of execution results.
                                         per task (referred to as pass@1).                         In this work, we propose a novel generate-and-
                                             * Corresponding authors                            edit approach to augment LLMs on the competitive
programming task, named Self-Edit. To mimic                   named Self-Edit for large language models
the above human programmers’ behavior, our ap-                (LLMs) to generate high-quality code for com-
proach incorporates the ability of LLMs in three              petitive programming tasks.
steps: ❶ Generation with LLMs. We use large lan-
guage models as black-box generators and generate           • We develop a fault-aware neural code editor
the program based on the problem description. ❷               that takes the generated code and error mes-
Execution. Given a generated code from LLMs, we               sages as input and uses them to refine the code,
execute it on the example test case to get the execu-         improving its quality and accuracy.
tion results. We further wrap the execution results
with templates as supplementary comments to in-             • We conduct experiments on two popular
clude additional helpful information for editing. ❸           datasets and nine LLMs to demonstrate the
Edit. We develop a fault-aware neural code editor             effectiveness and universality of our approach.
that takes the generated code and supplementary
comment as input and refines the code. Our code         2     Related Work
editor aims to improve the quality and accuracy of      2.1    Code Generation
code generation using LLMs.
   We conduct extensive experiments on two public       Code generation is a process in which source code
competitive programming benchmarks, including           is automatically generated based on functional re-
APPS (Hendrycks et al., 2021) and HumanEval             quirements such as natural language descriptions
(Chen et al., 2021). We apply our approach to 9         (Iyer et al., 2018; Yin and Neubig, 2018; Li et al.,
popular LLMs with parameter sizes ranging from          2023a,b,c) or pseudo code algorithms (Kulal et al.,
110M to 175B to show the universality. Compared         2019; Oda et al., 2015) or a old version of code (Li
to directly generating from LLMs, we have several       et al., 2022a) or a response from programming tools
findings: ❶ Our approach significantly improves         (Zhang et al., 2023). One particularly challenging
the performance of LLMs. In particular, our ap-         type of code generation task is competitive pro-
proach improves the average of pass@1 by 89%            gramming (Li et al., 2022c), in which models must
on APPS-dev and 31% on APPS-test. Even for the          solve problems at the level of programming com-
chosen largest language model GPT3-175B, our            petitions. This task often involves natural language
relatively small editor model can improve pass@1        descriptions and example input-output pairs. The
from 26.6% to 32.4% on the APPS-dev benchmark.          performance of a code generation model on compet-
❷ Our approach is generalizable on a different style    itive programming tasks can serve as a measure of
of dataset HumanEval, improving the average of          its ability to create complete solutions to problems.
pass@1 by 48%, showing the transfer ability on          In recent years, large pre-trained language models
the out-of-distribution benchmark.                      such as AlphaCode (Li et al., 2022c) and the GPT3
   Recently some approaches are also proposed to        (Brown et al., 2020) series have demonstrated im-
post-process programs generated by LLMs (Shi            pressive capabilities in code generation and compet-
et al., 2022; Inala et al., 2022; Chen et al., 2022;    itive programming. Other open-source code gener-
Zhang et al., 2022). These approaches do large-         ation models include GPT-Neo (Black et al., 2021),
scale sampling from LLMs, rerank these sampled          GPT-J (Wang and Komatsuzaki, 2021), CodePar-
programs, and output the final program. In compari-     rot (Wolf et al., 2020), PolyCoder (Xu et al., 2022),
son, our self-edit framework has two advantages: ❶      CodeGen (Nijkamp et al., 2022) and InCoder (Fried
Our approach maintains a constant sample budget         et al., 2022). We utilize the text-davinci-002 API
and significantly reduces the computational over-       from OpenAI and various competitive code genera-
head for LLMs. ❷ Our editor directly modifies the       tion models in this work.
programs and outperforms these reranking-based
                                                        2.2    Post-processing of LLMs for code
methods, especially with a limited sample budget
                                                               generation
such as pass@1. To our knowledge, we are the first
to adopt an editing-based post-processing method        To find the correct code solutions based on LLMs,
for competitive programming tasks.                      researchers adopt various post-processing methods
   The contributions are listed as follows:             to filter/rerank the original outputs from LLMs.
                                                        In the domain of solving math problems, Cobbe
   • We propose a generate-and-edit approach            et al. (2021) and Shen et al. (2021) chose the one
 Problem Description                                                           SyntaxError
 …find the smallest integer x                                              Wrong answers                                          Wrong answers
 greater than n, so it is                                                       NameError                                       Pass the test case
 divisible by the number k…                                                       EOFError                                             NameError
 -----Examples-----                                                                                                                   SyntaxError
 Input
                                                                         Pass the test case                                             IndexError
 5 3        example test case                                                   ValueError                                              ValueError
 Output                                                                         IndexError                                               TypeError
 6                                                                               TypeError                                    Time limit exceeded
                                                                          IndentationError                                                EOFError
 ...                                                                        RecursionError                                         RecursionError
                                                                                          0.0   0.1   0.2   0.3   0.4   0.5                     0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40
                  1. LLM for generating
                     programs               3. Fault-aware Code Editor
                                                                          (a) PyCodeGPT-110M-finetuned                                         (b) GPT3
 LLM Output                                         Editor Output
       …                                                  …
 print n + k                                        print (n + k)
       …                                                  …              Figure 3: Distribution of the top 10 classes of supple-
                  2. Executor for running                                mentary comments in the APPS-train dataset when us-
                     example test case                                   ing the PyCodeGPT-110M-finetuned and GPT3 models,
 Supplementary Comment
 Line 3, print n + k
                                                                         expressed as a percentage of the total number of gener-
 SyntaxError: Missing parentheses                                        ated programs for each class.
 in call to ‘print’. Did you mean
 print(n + k)? Fix the bug.



       Figure 2: Pipeline of our self-edit approach.                     train a fault-aware code editor model to refine the
                                                                         code based on the problem description, generated
                                                                         code, and supplementary   comment. testcase和hidden test case的表示
                                                                                              是否要增加example
with the highest rank by a trained ranker. Simi-
lar ranking methods are also used in the field of                        3.1       LLMs as Black-box Generator
cross-domain adaptation (Li et al., 2022b). In the                       We use large language models as black-box gen-
domain of code generation, post-processing tech-                         erators with fixed parameters in our design. This
niques are also often used (Lahiri et al., 2022; Le                      design choice is motivated by the fact that train-
et al., 2022). AlphaCode (Li et al., 2022c) and                          ing LLMs is costly, and access to LLMs is often
Shi et al. (2022) adopted the clustering and filter-                     restricted. (E.g., OpenAI only offers paid API to
ing methods based on the execution output of the                         infer GPT3.) Using LLM as a black-box genera-
generated programs. Inala et al. (2022) trained                          tor makes our approach flexible for using different
a fault-aware neural ranker to rerank the outputs                        LLMs. We investigate nine LLMs for code gen-
with a large sample budget. Chen et al. (2022) use                       eration with sizes ranging from 110M to 175B. A
the large models to generate test cases for them-                        detailed comparison is described in Table 2.
selves and automatically rank the solutions based
on the test-driven dual execution agreement. Zhang                       3.2       Executor and Supplementary Comments
et al. (2022) reranked the LLM outputs with the                          After we generate the code using LLMs, we use an
generation probability of back translation.                              executor to run the example test case. We classify
   However, these existing methods require large-                        the execution results into three types: ❶ Passed:
scale sampling. They need to generate a large num-                       The program passes the test case. ❷ Wrong An-
ber of programs for post-processing. For example,                        swer: The program runs normally but gives incor-
AlphaCode (Li et al., 2022c) needs 1 million sam-                        rect outputs. ❸ Error: The program terminates
ples per problem, costing 105 TPU-seconds. In                            abnormally due to syntax error, runtime exceptions,
the real world, computing resources are precious                         or exceeding time limit.
and limited, and existing methods are ineffective                           We analyze the distribution of test results on
in practical applications. Our self-edit approach                        APPS-train dataset for code generated by a rela-
addresses this issue by maintaining a constant sam-                      tively small model PyCodeGPT-110M and a large
ple budget and improving computational efficiency,                       model GPT3-175B as shown in Figure 3. We ob-
described in Section 4.3.                                                serve that programs produced by different mod-
                                                                         els yield different test result distributions. Code
3      Methodology                                                       generated by smaller models (PyCodeGPT) tends
                                                                         to encounter SyntaxError issues more frequently,
We provide an overview of the self-edit pipeline in                      while large models (GPT3) show fewer Syntax-
Figure 2. Given the problem description, We first                        Errors, fewer RuntimeErrors, but more normally
generate the initial code with LLM. Then we exe-                         executed cases.
cute the example test case to obtain test results and                       In order to construct meaningful supplementary
construct the supplementary comment. Finally, we                         comments for the code editor model to understand
 Comment 1:                                                    case letters represent the token of the correspond-
 Pass the example test case.
                                                               ing content in the input pair (N, S, C). We train
 Comment 2:
 Template: Wrong Answer with input: <input>. Expected
                                                               a decoder-only model to complete the code edit
 output is <output_1>, but generated output is <output_2>.
 Rewrite the code.
                                                               task. Concretely, we implement the code editor by
 Example: Wrong Answer with input: 2 5 3. Expected output
 is 1, but generated output is 0. Rewrite the code.
                                                               fine-tuning PyCodeGPT-110M on this task.
                                                                  At inference time, we first generate multiple pro-
 Comment 3:
 Template: Line <lineno>, <line_content>, <error_msg>.         grams from LLMs using natural language descrip-
 Fix the bug.
 Example: Line 2,                                              tion as input. For each generated program, we feed
 return len([i for i in str(i**2) for i in range(n+1) if
 i == str(d)])                                                 the example test case provided in the description
 NameError: name 'i' is not defined. Fix the bug.
                                                               into the executor to obtain a fault-aware comment.
                                                               We then use the editor to generate a new program,
Figure 4: Example Supplementary Comments in differ-
ent situations.                                                which is the final version for further evaluation.
                                                               This inference approach maintains a small sample
                                                               budget compared with existing large-scale sam-
various execution results, we design the comment               pling and filter/reranking methods.
templates (Fig. 4) for the three types of test re-
sults. The comment template can wrap potential                 3.3.2   Dataset Construction for Code Editor
error messages with additional helpful information             To train a fault-aware code editor, we need datasets
for editing. ❶ For the code passing the example                that contain the generated program and the cor-
test case, we use Comment 1: “Pass the example                 responding supplementary comments. To collect
test case.”. ❷ For the code producing incorrect                such datasets, we use different LLMs (Sec. 4.1) to
outputs, we use Comment 2 to include the relevant              generate candidate programs for problems in the
input, expected output, and the actual output. We              APPS-train dataset. For each problem, we sam-
also append the instruction “Rewrite the code” to              ple 10 programs from the LLM and then execute
guide the editor model to reimplement the algo-                the example test case to get the test results and
rithm to produce correct outputs. ❸ For the code               construct supplementary comments. At this point,
that terminates with errors, we use Comment 3 to               we get the datasets of triplets (N, S, C) for dif-
include the error line number, line context, and full          ferent LLMs. To further obtain the ground truth
error message. These supplementary comments                    program Ĉ, we collect the standard ground truth
provide additional context and clarity for the gen-            programs in the original APPS training dataset and
erated code and are used to guide editing the code.            the generated programs that pass all hidden test
                                                               cases. For each LLM, we create an individual ed-
3.3     Fault-aware Code Editor                                itor dataset with nearly 4.5k generated programs
Once we have constructed the supplementary com-                with comments. For each generated program, we
ments, we train a fault-aware editor that takes the            set at most 15 ground truth programs. As we de-
natural language description, generated code, and              scribed in Figure 3, the generated programs from
supplementary comments as input and produces                   different LLMs have different distributions of the
higher-quality refined code.                                   corresponding comments. To optimize the perfor-
                                                               mance of the fault-aware code editor for each LLM,
3.3.1    Code Editor Models                                    it is necessary to use training datasets specific to
The fault-aware code edit task is formally de-                 the corresponding LLM.
fined as a sequence-to-sequence task: given a
natural language description N , a program gen-                3.3.3   Training Objective of Code Editor
erated by LLM S, and accompanied supplemen-                    Editing for a high-quality program based on the
tary comments C (Sec. 3.2), the model is re-                   input pair (N, S, C) is a one-of-many task because
quired to generate higher-quality code Ĉ that imple-          multiple correct target programs satisfy the require-
ments the natural language description and passes              ments. Standard maximum likelihood objectives
test cases. In our experiments, the input pair                 aim to minimize loss by considering all of the solu-
(N, S, C) is segmented into three parts and concate-           tions in the training set (like recall), while we focus
nated using special separator tokens, represented as           on a model’s ability to edit a single correct solu-
[SOS], n1 , n2 , . . . , n|N | , [CODE], s1 , . . . , s|S| ,   tion based on the existing generated code within
, [CM N T ], c1 , . . . , c|C| , [EOS], where the lower-       a limited budget of attempts (like precision). To
address this discrepancy, we follow previous work                                                    Problems
                                                                                                                Hidden
                                                                                                                 Tests
and adopt a variation of GOLD (Pang and He, 2021;
                                                               Training
                                                                                 APPS-train           4207       5.56
Li et al., 2022c), which incorporates an off-policy             dataset

importance weight into the standard maximum like-                                 APPS-dev             598       4.03
                                                                                      Introductory    1000
lihood objective gradient:                                       Testing
                                                               benchmark
                                                                           APPS-test    Interview     3000      21.19
                                                                                      Competition     1000
                      X                                                          HumanEval             164       8.08
         ∇L(θ) = −           Pθ (t)∇logPθ (t)    (1)
                      t∈Ĉ                              Table 1: Statistics of training dataset and testing bench-
                                                        marks: the total number of problems in datasets (Prob-
where θ represents the model parameters and             lems), the average number of hidden test cases per prob-
logPθ (t) is the standard log-likelihood objective      lem (Hidden Tests).
for next token prediction. The additional weight
Pθ (t) allows the model to focus on the tokens that
already have a high likelihood, so the model can        APPS training dataset for validation1 . The detailed
concentrate on these easier-to-learn ground truth       statistic of the datasets is shown in Table 1. The
solutions and increase the chance of getting at least   hidden test cases are those test cases for evaluation.
one correct output. Such a loss setting allows edi-     They are not included in the problem description,
tors to learn to copy part of the content from exist-   so they are distinguished from the example test
ing generated programs to obtain better outputs.        case used to obtain supplementary comments.
                                                        Base LLMs. In this paper, we investigate the
4     Experiment                                        effectiveness of several widely used language mod-
                                                        els for code generation, including text-davinci-002
We present extensive experiments that span two          (175B) (Brown et al., 2020), CodeGen (2B, 350M)
representative datasets and nine different LLMs         (Nijkamp et al., 2022), InCoder (1B) (Fried et al.,
for code generation, whose parameter counts range       2022), GPT-Neo (1.3B, 125M) (Black et al., 2021),
across four orders of magnitude. The details of the     GPT-J (6B) (Wang and Komatsuzaki, 2021) and
adopted LLMs are described in Section 3.1. We           PycodeGPT (110M) (Zan et al., 2022). These mod-
aim to investigate four research questions: (1) how     els are evaluated under zero-shot or finetune ex-
much can fault-aware code editors improve various       perimental conditions, with additional descriptions
code generation models on competitive program-          provided as a part of Table 2. 2
ming (Sec. 4.2), (2) the advantages of editor-based     Editor Model. We implement the code editor
methods over existing ranking methods (Sec. 4.3),       by fine-tuning PyCodeGPT-110M. We choose this
(3) to what extent does the supplementary com-          model because of its relatively small parameter size
ments help to refine the program (Sec. 4.4), (4)        and high performance. We also tried the CodeGen-
how does the number of editing rounds affect the        350M model in early experiments but found that
final result (Sec. 4.5).                                the training speed and final performance were not
4.1    Experiment Setup                                 as good as the model we chose.
                                                           Considering that LLMs shows strong in-context
Dataset. We consider evaluating our approach on         learning abilities that do not need training process,
two existing code generation datasets: (1) APPS         we also explore to design a variant of our self-edit
(Hendrycks et al., 2021): a collection of 5000 train-   method with in-context learning. We use the text-
ing and 5000 test tasks collected from coding com-      davinci-002 as both base model and editor model.
petitions and interview problems. The test set has      The in-context learning self-edit performances are
three different difficulty levels: Introductory, In-    discussed in Section 5.2.
terview, and Competition. (2) HumanEval (Chen           Metrics. We use the metric pass rate pass@k
et al., 2021): a set of 164 test programming prob-      for performance evaluation and take advantage of
lems with a function signature, docstring, body,        hidden test cases to determine the functional cor-
and several unit tests. Our experiments only use        rectness of code solutions. For each problem, we
the APPS-train dataset to finetune the code gener-      submit k code solutions for evaluation. If any of the
ation models and the code editor models since it
                                                           1
is the largest training dataset. Following previous          https://github.com/microsoft/CodeRanker
                                                           2
                                                             We do not use the CodeX model as it was in closed beta
studies (Inala et al., 2022), we adopted the same di-   and was not available during our experiments. We choose
vision and used a set of 598 tasks excluded from the    text-davinci-002 with equal parameter size as an alternative.
k code solutions passes all ground truth test cases,    than APPS-dev, which we can see by the smaller
the problem is considered solved. Then pass@k is        pass@k numbers. Our editors maintain significant
the percentage of solved problems. In our experi-       improvement for models of different sizes. The ab-
ments, we set k = {1, 5, 10}.                           solute improvement of pass@1 covers from 0.12%
   To show the number of programs corrected by          to 0.7%, showing that the editor can solve 6 to 35
our editor, we design a new metric sol@k, which         more problems on this challenging benchmark. As
means the total number of correct programs given        for sol@10, our editors can additionally correct
k samples per problem. For example, for the 5000        hundreds of generated codes from LLMs.
problems in APPS-test, we will generate 5000 ∗ k          In some cases, we observe that the edit-pass@1
code solutions, from which we will count the num-       outperforms the pass@5. It demonstrates that edit-
ber of correct solutions as sol@k. In our experi-       ing the candidate code is very sample efficient.
ments, we set k = 10. We show the performance           With the editor model, the number of required pro-
of the base model and the performance after editing     grams sampled from the LLM can be reduced.
(denoted as edit-pass@k and edit-sol@k).                   Another interesting observation is that a smaller
Training/Inference Settings. For each finetuned         LLM equipped with our editor can achieve compa-
LLM, we limit the maximum epochs to 10 with a           rable performance as the super large models. For
learning rate of 1e-5, and choose the best check-       example, the GPT-Neo-125M, GPT-Neo-1.3B, and
point based on the validation loss on APPS-dev.         GPT-J are pretrained and finetuned with the same
We adopt the same training strategy to train fault-     dataset. Using the editor can fill in the gaps in the
aware code editors on each corresponding editor         parameter sizes of this series of models. The 125M
dataset. We set the maximum input length to 1024        pretrained model with a 110M editor can signif-
and output length to 512 for our editors. To extract    icantly outperform a 1.3B pretrained model and
the supplementary comment, we choose only one           even outperform the 6B pretrained model in some
example test case contained in the problem descrip-     cases. This finding can also be observed in other
tion even if it contains multiple. At inference time,   experiments, showing that our editor can offer a
we use temperature sampling with T = 0.8 both           boost approximately equivalent to a tens of times
for LLM and editor outputs. We limit the sample         pretrained model size increase.
budget of LLMs to 10. For each LLM output code,
                                                        On Different Difficulty-Level Problems. Consid-
we only generate one code as the final version with
                                                        ering that the APPS-test dataset has three difficulty
our editor. Thus the usage of the editor maintains a
                                                        levels, we further analyze the improvement on prob-
constant sample budget. All experiments are con-
                                                        lems of different difficulty in Table 5. We choose
ducted with 4 Tesla V100-32GB GPUs.
                                                        GPT-J-6B-finetuned as the base model because it
                                                        has shown promising results on this challenging
4.2   Comparison with Base LLMs                         benchmark and has certain representativeness. The
APPS-dev & APPS-test. We first compare with di-         editor can improve the base model on problems of
rectly generating from LLMs to analyze how fault-       all difficulty levels but has a relatively high pass
aware code editors can improve nine popular code        rate improvement on simple "Introductory" prob-
generation models. Table 2 shows the primary re-        lems. We find that the output of LLMs is poor on
sults on the APPS-dev dataset for nine different        very difficult problems, making it too difficult for
code generation models. The fault-aware editor          the editor to correct these solutions. Even so, our
improves all code generation models despite their       method slightly improves the "Competition" prob-
different sizes and training settings. The average      lems when enlarging the sample budget from 1 to
pass@1 value across nine models increases from          10.
6.17% to 11.67%, representing an impressive 89%         HumanEval. We also measure the transfer ability
improvement. For those LLMs with a particularly         of our editor on HumanEval, a dataset of different
large number of parameters, our editor can also         styles, in Table 4. The HumanEval dataset requires
achieve a significant improvement. For GPT3 with        the model to give the function body based on the
175B parameters, the improvement of our editor          function signature, comments, and example test
also achieves 5.9%, 5.0%, 8.4% on pass@{1,5,10}.        cases. Following the executability filter in previous
   Results on the APPS-test dataset are shown in        work (Zhang et al., 2022), in this dataset, we only
Table 3. The test problems are more challenging         edit the outputs that can not pass the example test
                                                     edit                          edit                          edit                         edit
   Code Gen. Model          Para.     pass@1                        pass@5                        pass@10                       sol@10
                                                     pass@1                        pass@5                        pass@10                      sol@10
        finetuned
       PyCodeGPT            110M           4.8            11.4            7.9           15.1            8.9           17.1          286          659
      GPT-Neo 125M          125M           1.5             8.5            6.7           10.2           10.2           17.2          102          501
      CodeGen-350M          350M           1.7             5.7            2.5            9.2            3.2           13.5          103          339
      GPT-Neo 1.3B          1.3B           4.0            10.5           10.9           18.6           17.2           25.4          200          663
       InCoder-1B           1.3B           9.4            12.4           12.5           16.2           13.5           18.1          568          730
          GPT-J              6B            6.0            12.0           17.9           27.8           24.6           37.8          365          750
          zero-shot
        InCoder-1B          1.3B            0.2            4.7            0.8            7.7            1.2           9.9            13          270
        CodeGen-2B          2.7B            1.3            7.4            5.9           14.0            9.7           19.7           92          438
      text-davinci-002      175B           26.6           32.4           43.8           48.8           49.7           58.0          1626         1948

Table 2: Results on the APPS-dev dataset on how our fault-aware editors can improve the pass rates for different
sample budgets with various code generation models. "finetuned" indicates we finetune those models on APPS-train
dataset. "zero-shot" indicates we use those models in the zero-shot setting. We will use the best checkpoints of
LLMs and editor models based on this validation set in other experiments.

                                                  edit                          edit                          edit                        edit
         Code Gen. Model        pass@1                           pass@5                        pass@10                       sol@10
                                                  pass@1                        pass@5                        pass@10                     sol@10
            finetuned
           PyCodeGPT                0.20           0.64           0.38           0.98           0.44           1.24           126          308
          GPT-Neo 125M              0.08           0.22           0.40           0.70           0.70           1.12            45          135
          CodeGen 350M              0.20           0.32           0.30           0.56           0.32           0.84            92          149
          GPT-Neo 1.3B              0.14           0.68           0.74           1.38           1.40           2.10           106          340
           InCoder 1B               0.66           0.86           1.18           1.62           1.44           2.10           344          421
              GPT-J                 0.70           1.40           2.46           3.34           3.52           4.76           404          738
              zero-shot
            InCoder 1B              0.00           0.24           0.02          0.50            0.02           0.76            1            121
            CodeGen 2B              0.12           0.28           0.34          0.66            0.66           1.08           41            131
          text-davinci-002          7.48           7.94          15.94          16.66             -              -           1876 †        1983 †
          †
              As we access GPT3 through a paid API, we limit the sample budget of GPT3 as 5 for this large benchmark and
              evaluate sol@5.

                                              Table 3: Results on the APPS-test dataset.


case. We also modify the input format to be similar                              error type and use this classification prediction to
to the format in the APPS dataset. We select sev-                                rerank the generated codes from LLMs. The su-
eral representative LLMs for evaluation within our                               pervised training task makes this method more effi-
computational capabilities. We can again see that                                cient than previous filtering and reranking methods.
the editor improves the performance of all code                                  However, our experiments (Table 6) prove that our
generation models on all metrics. We notice that                                 editor outperforms this state-of-the-art method in
under larger sample budget conditions, even if the                               terms of accuracy and efficiency.
pass@10 does not increase for CodeGen-2B, our                                       We choose the GPT-Neo-1.3B-finetuned as the
editor can still correct more generated solutions.                               base model and finetune on the APPS-train dataset,
Thus the sol@10 increases significantly. These re-                               keeping the same experimental settings as CodeR-
sults demonstrate the ability and generality of our                              anker for a fair comparison. Our method ("+ ed-
editor to correct out-of-distribution output codes.                              itor") significantly outperforms CodeRanker ("+
                                                                                 ranker"). In particular, on APPS-test, our method
4.3     Comparison with Post-processing Baseline                                 can improve pass@1 from 0.14% to 0.68%, while
This experiment compares our self-edit approach                                  their method can only improve from 0.14% to 0.3%.
with existing post-processing methods for code gen-                              It means our method can solve 19 more problems
eration. We choose to compare with CodeRanker                                    on this challenging dataset. We also provide the
(Inala et al., 2022), a state-of-the-art reranking                               performance of other reproduced base models in
method on the APPS dataset. CodeRanker fine-                                     Table 9, where our method generally outperforms.
tuned CodeBERT (125M) to classify the potential                                     More importantly, existing post-processing
                                            edit               edit                             edit                       edit
         Code Gen. Model         pass@1               pass@5                   pass@10                       sol@10
                                            pass@1             pass@5                           pass@10                    sol@10
        finetuned on APPS
            PyCodeGPT             6.10        8.54      7.32    10.98            7.93             13.41        100           159
          GPT-Neo 125M            0.61        3.05      3.05    7.32             6.10             9.76         21            76
          CodeGen-350M            6.10        7.93      7.32    9.15             7.32             10.37        100           140
           GPT-Neo 1.3B           2.44        5.49      8.54    10.98            11.59            14.63        66            132
            Incoder-1B            6.71       10.37     8.54     13.41            9.76             14.63        112           169
               GPT-J              7.32        9.76     17.07    19.51            25.00            25.61        133           183
             zero-shot
            Incoder-1B            1.22        3.66      2.44    7.93             5.49             10.98        13            87
           CodeGen-2B            14.02       17.07     29.27    29.88            34.15            34.15        226           255

                                          Table 4: Results on the HumanEval dataset.


 Difficulty level   pass@1         pass@5        pass@10                                              APPS-dev        APPS-test
                    2.10           7.40          10.10                      Setting       Samples    @1       @5      @1        @5
  Introductory
                    4.90 133%      10.40 40.5%   14.20 40.6%
                                                                        base model                   4.0     10.9     0.14     0.74
                    0.43           1.53          2.37
      Interview                                                          + ranker     †
                                                                                           100       8.0     15.1     0.3      1.1
                    0.67 53.5%     1.97 28.1%    3.03 28.3%
                                                                         + editor         {1,5}      10.5    18.6     0.68     1.38
                    0.10           0.30          0.40                   †
  Competition                                                               The results are copied from the original paper.
                    0.10           0.40 33.3%    0.50 25.0%

      Average
                    0.70           2.46          3.52            Table 6: Pass Rate Results compared with CodeRanker
                    1.40 100%      3.34 35.8%    4.76 35.2%      on the APPS dataset. "+ ranker" numbers are cited
                                                                 from Inala et al. (2022). We use the GPT-Neo-1.3B-
Table 5: Results on the APPS-test dataset with 3 diffi-          finetuned as the base model. Our method outperforms
culty levels. We use the GPTJ-6B-finetuned as the base           CodeRanker with an extremely small sample budget.
model. We show the base model results (the first row)
and edited results (shaded row below). The numbers in
                                                                                                  APPS-dev                 APPS-test
red indicate the improvements of our editor.
                                                                  Setting                  @1       @5       @10     @1      @5      @10

                                                                  base model               4.8      7.9      8.9     0.2     0.4     0.4
methods rely on sampling many outputs from                        after edit               11.4     15.1     17.1    0.6     1.0     1.2
LLMs. For instance, the CodeRanker requires 100                     - comments             9.4      11.5     13.5    0.3     0.3     0.4
outputs for each problem and then selects k sam-                    + edit round           11.7     15.2     17.1    0.4     0.7     0.9
ples with their ranker model to evaluate pass@k
metric. In contrast, our method only requires                    Table 7: Pass Rate Results of ablation studies. We use
                                                                 the PyCodeGPT-110M-finetuned as the base model. The
k = {1, 5} outputs per problem and then utilizes
                                                                 column "after edit" means the performance of our edi-
these outputs to generate a final solution through               tor in original settings. We experiment with additional
editing. Our approach is more efficient and effec-               editing rounds or without supplemental comment.
tive, especially when obtaining outputs from large
language models is costly. As a result, our method
has greater practical significance and is more suit-             prove the APPS-dev dataset compared to the base
able for use with limited sample budgets.                        model. However, on the more difficult APPS-test
                                                                 dataset, the editor model without comments shows
4.4     Ablation on Supplementary Comments                       no performance improvement. The results indicate
To investigate the influence of supplementary com-               that losing the guidance of the supplementary com-
ments, we remove the supplementary comments                      ment will hurt the performance of the editor model.
from the editor input and only use problem descrip-              Our experiments show that using error messages
tion and generated code to train a new editor. Other             as supplementary comments for the code editor is
settings are kept the same. Results on APPS vali-                crucial for achieving remarkable performances.
dation and test datasets are shown in Table 7.
   We find that the pass rate of the modified editor             4.5     Ablation on the Number of Edit Rounds
decreases significantly on both datasets compared                In our self-edit approach, we make edits to the
with the original editor. The modified editor can im-            output of LLMs to produce the final program. It
leads to a question: what if we make additional               Benchmark             pass@1   pass@5    sol@5
edits to the program after the first edit? We add                          before    7.48     15.94     1876
                                                              APPS-test
an additional editing step to answer this question                          after    8.94     17.12     2214
using our original editor. Concretely, the edited                          before   34.76     60.98      288
                                                              HumanEval
program is executed on an example test case to ob-                          after   39.63     64.63      331
tain comments and then refined by the editor model
                                                          Table 8: Results of the in-context learning self-edit on
again. The results of this approach are presented
                                                          APPS-test and HumanEval benchmarks. We use the
in Table 7, with the column labeled "+ edit round"        text-davinci-002 as the base model and editor model.
indicating the two-round editing approach.                We use the in-context learning ability of GPT3 to self-
   The results show the two-round editing leads to a      edit the model output. The constructed supplementary
slight increase in pass@1 on APPS-dev. However,           comments are used as input prompts for the editor. We
the additional edit round hurts the performance on        show the base model results (the first row) and edited
APPS-test. We guess the reason is the gap between         results (shaded row below).
training and test time in the second editing round.
The editor is trained to edit LLM outputs but used        without additional training, offering a promising
to edit its own output in the second edit round. In       solution for optimizing the potential of LLMs.
this setting, an additional editing round is not very        Our experiments on APPS-test and HumanEval
helpful in generating better programs.                    are presented in Table 8. Results demonstrate that
                                                          our self-edit framework can be extended using in-
5       Discussion                                        context learning, achieving significantly better per-
5.1       Time Cost compared with Post-processing         formance than smaller editors across various bench-
          Baseline                                        marks. However, it is important to note that this
                                                          in-context learning self-edit method still incurs a
For the specific issue of time cost, we use Google        relatively large number of LLM calls. Therefore,
Colab 3 with a Tesla T4 GPU to build a demo               optimizing resource requirements while exploiting
and conduct evaluations over APPS-test dataset.           the potential of LLMs remains critical. To this
We use text-davinci-002 as the base model and the         end, we will explore strategies to efficiently utilize
average time cost is nearly 8.4s to obtain 1 sample       the in-context learning capabilities of LLMs in our
for each question. The executor costs <0.01s, and         self-edit framework in future work.
our editor costs 3.7s to get the final output, which is
acceptable in our actual experience using the demo.       6   Conclusion
By contrast, the state-of-the-art reranking method
                                                          We propose a generate-and-edit approach named
CodeRanker requires >110s to obtain candidate
                                                          Self-Edit that utilizes execution results of the gener-
lists and 0.53s for the following ranker. As a result,
                                                          ated code from LLMs to improve the code quality
our framework achieves better performance with
                                                          on the competitive programming task. The central
less total time cost and fewer LLM calls.
                                                          component of our approach is the fault-aware code
5.2       Performances of In-Context Learning             editor, which can edit and optimize the generated
          Self-Edit                                       code. In-depth evaluations demonstrate our ap-
                                                          proach significantly improves the quality of LLMs’
Given that LLMs have demonstrated strong in-              output code.
context learning abilities without requiring any spe-
cific training, we leverage the capabilities of the       7   Acknowledgement
text-davinci-002 model as both the base and editor
models to develop a variant of our self-edit method       This research is supported by the National Nat-
that utilizes in-context learning. Specifically, we       ural Science Foundation of China under Grant
utilize in-context learning abilities of the model to     Nos. 62072007, 62192731, 62192733, 62192730,
self-edit its output using the supplementary com-         61832009. The AI training platform supporting this
ments we construct (detailed in Section 3.2) as in-       work were provided by High-Flyer AI. (Hangzhou
put prompts for zero-shot inference. This approach        High-Flyer AI Fundamental Research Co., Ltd.)
allows the large model to edit its output program         We also would like to thank all the anonymous re-
                                                          viewers for constructive comments and suggestions
    3
        https://colab.research.google.com                 to this paper.
Limitations                                                Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
                                                           Clemens Winter, Christopher Hesse, Mark Chen, Eric
Our work has several limitations, which we aim to          Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
address in our future work:                                Jack Clark, Christopher Berner, Sam McCandlish,
                                                           Alec Radford, Ilya Sutskever, and Dario Amodei.
   Firstly, we implement our editor with relatively
                                                           2020. Language models are few-shot learners. In Ad-
small pretrained models within our computational           vances in Neural Information Processing Systems 33:
capabilities. Our in-depth evaluations have prelimi-       Annual Conference on Neural Information Process-
narily demostrated the effectiveness of the generate-      ing Systems 2020, NeurIPS 2020, December 6-12,
and-edit approach. We hope to further understand           2020, virtual.
the performance when using different pretrained          Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan,
models and architectures for the editor.                   Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2022.
   Secondly, the editor datasets we constructed are        Codet: Code generation with generated tests. CoRR,
relatively small due to our computational capabil-         abs/2207.10397.
ities. In our experiment, we only sample 10 pro-
                                                         Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
grams from the LLM for each problem for dataset           Henrique Ponde de Oliveira Pinto, Jared Kaplan,
construction. Compared with existing post-editing         Harrison Edwards, Yuri Burda, Nicholas Joseph,
methods, the dataset we use is quite small. It would      Greg Brockman, Alex Ray, Raul Puri, Gretchen
be meaningful to do a detailed analysis of the im-        Krueger, Michael Petrov, Heidy Khlaaf, Girish Sas-
                                                          try, Pamela Mishkin, Brooke Chan, Scott Gray,
pact of editor dataset size, or to experiment with        Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz
other dataset construction methods. We leave this         Kaiser, Mohammad Bavarian, Clemens Winter,
as future work.                                           Philippe Tillet, Felipe Petroski Such, Dave Cum-
   Thirdly, We do not have strict comparison about        mings, Matthias Plappert, Fotios Chantzis, Eliza-
                                                          beth Barnes, Ariel Herbert-Voss, William Hebgen
computing resources with other post-editing meth-
                                                          Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie
ods. In Section 4.3 we compare with a state-of-the-       Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
art re-reaking baseline. We both use an additional        William Saunders, Christopher Hesse, Andrew N.
model with a similar amount of parameters, but            Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan
our approach outperforms using very few samples           Morikawa, Alec Radford, Matthew Knight, Miles
                                                          Brundage, Mira Murati, Katie Mayer, Peter Welinder,
from LLMs. As accessing LLMs is costing, our              Bob McGrew, Dario Amodei, Sam McCandlish, Ilya
approach demonstrates both superior accuracy and          Sutskever, and Wojciech Zaremba. 2021. Evaluat-
efficiency.                                               ing large language models trained on code. CoRR,
   Finally, in our ablation study on the number of        abs/2107.03374.
edit rounds, we faced with a gap between train-          Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
ing and test time in the second editing round. Our         Jacob Hilton, Reiichiro Nakano, Christopher Hesse,
existing implementation is not designed for this           and John Schulman. 2021. Training verifiers to solve
multiple-round editor. We hope to further try new          math word problems. CoRR, abs/2110.14168.
specially designed model to implement the editor
                                                         Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang,
model. As large language models continue to ad-            Eric Wallace, Freda Shi, Ruiqi Zhong, Wen-tau Yih,
vance, the need for effective strategies to interact       Luke Zettlemoyer, and Mike Lewis. 2022. Incoder:
with LLMs will be an important area of future re-          A generative model for code infilling and synthesis.
search.                                                    CoRR, abs/2204.05999.

                                                         Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-
                                                           tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
References                                                 Samir Puranik, Horace He, Dawn Song, and Jacob
Sid Black, Leo Gao, Phil Wang, Connor Leahy, and           Steinhardt. 2021. Measuring coding challenge com-
  Stella Biderman. 2021. Gpt-neo: Large scale autore-      petence with APPS. In Proceedings of the Neural
  gressive language modeling with mesh-tensorflow.         Information Processing Systems Track on Datasets
  If you use this software, please cite it using these     and Benchmarks 1, NeurIPS Datasets and Bench-
  metadata, 58.                                            marks 2021, December 2021, virtual.

Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie         Jeevana Priya Inala, Chenglong Wang, Mei Yang, An-
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind          dres Codas, Mark Encarnación, Shuvendu K Lahiri,
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda          Madanlal Musuvathi, and Jianfeng Gao. 2022. Fault-
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,             aware neural code rankers. In Advances in Neural
  Gretchen Krueger, Tom Henighan, Rewon Child,              Information Processing Systems.
Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, and       Yusuke Oda, Hiroyuki Fudaba, Graham Neubig,
   Luke Zettlemoyer. 2018. Mapping language to              Hideaki Hata, Sakriani Sakti, Tomoki Toda, and
   code in programmatic context. arXiv preprint             Satoshi Nakamura. 2015. Learning to generate
   arXiv:1808.09588.                                        pseudo-code from source code using statistical ma-
                                                            chine translation. In 2015 30th IEEE/ACM Interna-
Sumith Kulal, Panupong Pasupat, Kartik Chandra, Mina        tional Conference on Automated Software Engineer-
  Lee, Oded Padon, Alex Aiken, and Percy S Liang.           ing (ASE), pages 574–584. IEEE.
  2019. Spoc: Search-based pseudocode to code. Ad-
  vances in Neural Information Processing Systems,        Richard Yuanzhe Pang and He He. 2021. Text genera-
  32.                                                       tion by learning from demonstrations. In 9th Inter-
                                                            national Conference on Learning Representations,
Shuvendu K. Lahiri, Aaditya Naik, Georgios Sakkas,          ICLR 2021, Virtual Event, Austria, May 3-7, 2021.
  Piali Choudhury, Curtis von Veh, Madanlal Musu-           OpenReview.net.
  vathi, Jeevana Priya Inala, Chenglong Wang, and
  Jianfeng Gao. 2022. Interactive code generation         Jianhao Shen, Yichun Yin, Lin Li, Lifeng Shang, Xin
  via test-driven user-intent formalization. CoRR,           Jiang, Ming Zhang, and Qun Liu. 2021. Generate &
  abs/2208.05950.                                            rank: A multi-task framework for math word prob-
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio           lems. In Findings of the Association for Compu-
  Savarese, and Steven Chu-Hong Hoi. 2022. Coderl:           tational Linguistics: EMNLP 2021, Virtual Event /
  Mastering code generation through pretrained models        Punta Cana, Dominican Republic, 16-20 November,
  and deep reinforcement learning. In NeurIPS.               2021, pages 2269–2279. Association for Computa-
                                                             tional Linguistics.
Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2023a. En-
   abling programming thinking in large language          Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke
   models toward code generation. arXiv preprint            Zettlemoyer, and Sida I. Wang. 2022. Natural lan-
   arXiv:2305.06599.                                        guage to code translation with execution. CoRR,
                                                            abs/2204.11454.
Jia Li, Ge Li, Zhuo Li, Zhi Jin, Xing Hu, Kechi Zhang,
   and Zhiyi Fu. 2022a. Codeeditor: Learning to edit      Ben Wang and Aran Komatsuzaki. 2021. GPT-J-
   source code with pre-trained models. arXiv preprint      6B: A 6 Billion Parameter Autoregressive Lan-
   arXiv:2210.17040.                                        guage Model. https://github.com/kingoflolz/
                                                            mesh-transformer-jax.
Jia Li, Yongmin Li, Ge Li, Zhi Jin, Yiyang Hao, and
   Xing Hu. 2023b. Skcoder: A sketch-based ap-            Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
   proach for automatic code generation. arXiv preprint     Chaumond, Clement Delangue, Anthony Moi, Pier-
   arXiv:2302.06144.                                        ric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz,
                                                            Joe Davison, Sam Shleifer, Patrick von Platen, Clara
Jia Li, Chongyang Tao, Huang Hu, Can Xu, Yining             Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le
   Chen, and Daxin Jiang. 2022b. Unsupervised cross-        Scao, Sylvain Gugger, Mariama Drame, Quentin
   domain adaptation for response selection using self-     Lhoest, and Alexander M. Rush. 2020. Transform-
   supervised and adversarial training. In WSDM ’22:        ers: State-of-the-art natural language processing. In
   The Fifteenth ACM International Conference on Web        Proceedings of the 2020 Conference on Empirical
   Search and Data Mining, Virtual Event / Tempe, AZ,       Methods in Natural Language Processing: System
   USA, February 21 - 25, 2022, pages 562–570. ACM.         Demonstrations, pages 38–45, Online. Association
Jia Li, Yunfei Zhao, Yongmin Li, Ge Li, and Zhi Jin.        for Computational Linguistics.
   2023c. Towards enhancing in-context learning for
   code generation. arXiv preprint arXiv:2303.17780.      Frank F. Xu, Uri Alon, Graham Neubig, and Vincent Jo-
                                                             sua Hellendoorn. 2022. A systematic evaluation of
Yujia Li, David H. Choi, Junyoung Chung, Nate Kush-          large language models of code. In MAPS@PLDI
  man, Julian Schrittwieser, Rémi Leblond, Tom Ec-          2022: 6th ACM SIGPLAN International Symposium
  cles, James Keeling, Felix Gimeno, Agustin Dal             on Machine Programming, San Diego, CA, USA, 13
  Lago, Thomas Hubert, Peter Choy, Cyprien de Mas-          June 2022, pages 1–10. ACM.
  son d’Autume, Igor Babuschkin, Xinyun Chen, Po-
  Sen Huang, Johannes Welbl, Sven Gowal, Alexey           Pengcheng Yin and Graham Neubig. 2018. Tranx: A
  Cherepanov, James Molloy, Daniel J. Mankowitz,            transition-based neural abstract syntax parser for se-
  Esme Sutherland Robson, Pushmeet Kohli, Nando             mantic parsing and code generation. arXiv preprint
  de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.         arXiv:1810.02720.
  2022c. Competition-level code generation with al-
  phacode. CoRR, abs/2203.07814.                          Daoguang Zan, Bei Chen, Dejian Yang, Zeqi Lin,
                                                            Minsu Kim, Bei Guan, Yongji Wang, Weizhu Chen,
Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan       and Jian-Guang Lou. 2022. CERT: Continual pre-
  Wang, Yingbo Zhou, Silvio Savarese, and Caiming           training on sketches for library-oriented code genera-
  Xiong. 2022. A conversational paradigm for program        tion. In The 2022 International Joint Conference on
   synthesis. CoRR, abs/2203.13474.                         Artificial Intelligence.
Kechi Zhang, Ge Li, Jia Li, Zhuo Li, and Zhi Jin. 2023.
  Toolcoder: Teach code generation models to use api
  search tools. ArXiv, abs/2305.04032.
Tianyi Zhang, Tao Yu, Tatsunori B. Hashimoto, Mike
  Lewis, Wen-tau Yih, Daniel Fried, and Sida I. Wang.
  2022. Coder reviewer reranking for code generation.
  CoRR, abs/2211.16490.
A   Compared with CodeRanker
We compare with CodeRanker (Inala et al., 2022)
using GPT-Neo-125M-finetuned, GPT-Neo-1.3B-
finetuned and GPT-J-6B-finetuned as the base
model. For fair comparison, we choose the same
base model, training dataset and test benchmark as
the CodeRanker. We choose the above three base
models and finetune on the APPS-train dataset to
reproduce their results. The purpose of this step
is to make our base model results similar to their
reported base model results, so as to fairly compare
the post-processing performance. In the experi-
ments, the base model performance in our results is
similar to the base model reported by CodeRanker.
Full details of results are shown in Table 9. With a
very small number of samples output by LLMs, our
method significantly exceeds this state-of-the-art
baseline.

B   Qualitative analysis of Code Editor
In Figure 5 and 6 we show various programs gen-
erated by the GPT3, its corresponding problem
description (contains example test case) and the
supplementary comment. Our fault-aware code
editor concatenates these as input, and generate
the edited code as the final output. We find that
the edited code is simialr to the GPT3 output. In
particular, the first few lines of the edited output
are exactly the same as the output of GPT3, and
the subsequent code is also partially based on the
content in GPT3 output. Through statistical anal-
ysis, we find that the common prefix between the
two sequences accounted for 19.10% of the edited
output on the APPS-dev and APPS-test datasets.
While this does not account for similarities in the
intermediate content, it is sufficient evidence to
demonstrate the impact of the LLM output on the
edited code. As for the HumanEval benchmark, we
also show case studies in Figure 7.
                    GPT-Neo-125M-finetuned
                                                                         APPS-dev        APPS-test
                                                  Setting    Samples     @1     @5      @1      @5
                                                         †
                        Reported in          base model                  1.4    5.2     0.04   0.17
                     (Inala et al., 2022)       + ranker       100       6.5    11.4    0.1    0.5
                                              base model                 1.5     6.7    0.08   0.40
                           Our results
                                                 + editor     {1,5}      8.5    10.2    0.22   0.70

                    GPT-Neo-1.3B-finetuned
                                                                         APPS-dev        APPS-test
                                                  Setting    Samples     @1     @5      @1      @5
                                                         †
                        Reported in          base model                  2.6    9.1     0.14   0.53
                     (Inala et al., 2022)       + ranker       100       8.0    15.1    0.3     1.1
                                              base model                 4.0    10.9    0.14   0.74
                           Our results
                                                 + editor     {1,5}     10.5    18.6    0.68   1.38

                    GPT-J-6B-finetuned
                                                                         APPS-dev        APPS-test
                                                  Setting    Samples     @1     @5      @1      @5
                                                         †
                        Reported in          base model                 5.1     15.6    0.5     1.6
                     (Inala et al., 2022)       + ranker       100      11.0    21.7    0.8     2.6
                                              base model                 6.0    17.9    0.7    2.46
                           Our results
                                                 + editor     {1,5}     12.0    27.8    1.4    3.34
                     †
                         As CodeRanker does not release the weights of base models, we cite their
                         results from Inala et al. (2022) and reproduce finetuned base models shown in
                         the "Our results - base model" row below.

Table 9: Full details of Pass Rate Results compared with the CodeRanker on the APPS dataset. We use GPT-Neo-
125M-finetuned, GPT-Neo-1.3B-finetune and GPT-J-6B-finetuned as the base model.
                                                                                           Problem Description:                                          Question id: APPS-dev-4615

                                                                                           Our AAA company is in need of some software to help with logistics: you will be
Problem Description:                                        Question id: APPS-dev-305
                                                                                           given the width and height of a map, a list of x coordinates and a list of y
                                                                                           coordinates of the supply points, starting to count from the top left corner of the
Return the number of distinct non-empty substrings of text that can be written as          map as 0.
the concatenation of some string with itself (i.e. it can be written as a + a where a is   Your goal is to return a two dimensional array/list with every item having the value
some string).                                                                              of the distance of the square itself from the closest supply point expressed as a
                                                                                           simple integer.
Example 1:                                                                                 Quick examples:
Input: text = "abcabcabc"                                                                  ```python
Output: 3                                                                                  logistic_map(3,3,[0],[0])
Explanation: The 3 substrings are "abcabc", "bcabca" and "cabcab".                         #returns
                                                                                           #[[0,1,2],
Example 2:                                                                                 # [1,2,3],
Input: text = "leetcodeleetcode"                                                           # [2,3,4]]
Output: 2                                                                                  logistic_map(5,2,[0,4],[0,0])
Explanation: The 2 substrings are "ee" and "leetcodeleetcode".                             #returns
                                                                                           #[[0,1,2,1,0],
Constraints:                                                                               # [1,2,3,2,1]]
1 <= text.length <= 2000                                                                   ```
text has only lowercase English letters.                                                   Remember that our company is operating with trucks, not drones, so you can
                                                                                           simply use Manhattan distance. If supply points are present, they are going to be
GPT3:                                                                                      within the boundaries of the map; if no supply point is present on the map, just
class Solution:                                                                            return `None`/`nil`/`null` in every cell.
     def distinctEchoSubstrings(self, text: str) -> int:                                   ```python
          n = len(text)                                                                    logistic_map(2,2,[],[])
          res = set()                                                                      #returns
          for i in range(n):                                                               #[[None,None],
                for j in range(i+1, n+1):                                                  # [None,None]]
                     if text[i] == text[j]:                                                ```
                          k = 1                                                            **Note:** this one is taken (and a bit complicated) from a problem a real world
                          while i+k < j and j+k < n and                                    AAA company [whose name I won't tell here] used in their interview. It was done
text[i+k] == text[j+k]:
                                                                                           by a friend of mine. It is nothing that difficult and I assume it is their own version of
                                k += 1                                                     the FizzBuzz problem, but consider candidates were given about 30 mins to solve it.
                          if k == j-i:
                                res.add(text[i:j])
          return len(res)                                                                  GPT3:
                                                                                           def logistic_map(width, height, x, y):
Supplementary Comment:                                                                         return [[min(abs(x - i) + abs(y - j) for x, y in zip(x, y))
Line 7, if text[i] == text[j]:                                                             for i in range(width)] for j in range(height)]
IndexError: string index out of range. Fix the bug.
                                                                                           Supplementary Comment:
After Edit:                                                                                Line 2, return [[min(abs(x - i) + abs(y - j) for x, y in zip(x, y)) for i in range(width)] for
class Solution:                                                                            j in range(height)]
     def distinctEchoSubstrings(self, text: str) -> int:                                   ValueError: min() arg is an empty sequence. Fix the bug.
          n = len(text)
          res = set()                                                                      After Edit:
          for i in range(n):                                                               def logistic_map(width, height, supply_x, supply_y):
                                                                                               if not supply_x or not supply_y:
                for j in range(i+1, n):                                                            return [[None] * width for _ in range(height)]
                     if text[i:j] == text[j:j+j-i]:                                            return [[min(abs(x - sx) + abs(y - sy) for sx, sy in
                          res.add(text[i:j])                                               zip(supply_x, supply_y)) for x in range(width)] for y in
          return len(res)                                                                  range(height)]


                                           (a)                                                                                         (b)

                                       Figure 5: Case Study on APPS-dev dataset using GPT3 model.
                                                                                        Problem Description:                                     Question id: APPS-test-4854

                                                                                        Mirko is a great code breaker. He intercepted an enemy message. The message
                                                                                        consists of $N$ numbers, smaller than or equal to $C$. Mirko belives freqency
                                                                                        analysis consists of sorting this sequence so that more frequent numbers appear
                                                                                        before less frequent ones.

                                                                                        Formally, the sequence must be sorted so that given any two numbers $X$ and $Y$,
                                                                                        $X$ appears before $Y$ if the number of times $X$ appears in the original
                                                                                        sequence is larger than the number of time $Y$ does. If the number of
                                                                                        appearances is equal, the number whose value appears sooner in the input should
                                                                                        appear sooner in the sorted sequence.

                                                                                        Help Mirko by creating a “frequency sorter”.
Problem Description:                                      Question id: APPS-test-2629
                                                                                        -----Input-----
Given a positive integer n, generate a square matrix filled with elements from 1 to     First line of input contains two integers, $N$ ($1 \le N \le 1000$), the length of the
n2 in spiral order.                                                                     message, and $C$ ($1 \le C \le 1000000000$), the number from the task
                                                                                        description above.
Example:
                                                                                        The next line contains $N$ positive integers smaller than or equal to $C$, the
Input: 3                                                                                message itself.
Output:
[                                                                                       -----Output-----
 [ 1, 2, 3 ],                                                                           The first and only line of output should contain $N$ numbers, the sorted sequence.
 [ 8, 9, 4 ],
 [ 7, 6, 5 ]                                                                            -----Examples-----
]                                                                                       Sample Input 1:
                                                                                        52
GPT3:                                                                                   21212
class Solution:                                                                         Sample Output 1:
    def generateMatrix(self, n):
        if n == 0:                                                                      22211
            return []
        if n == 1:                                                                      Sample Input 2:
            return [[1]]                                                                93
                                                                                        133322211
                res = [[0 for i in range(n)] for j in range(n)]
                                                                                        Sample Output 2:
                i = 0
                j = 0                                                                   111333222
                count = 1
                while i < n and j < n:                                                  GPT3:
                    for k in range(j, n):                                               n, c = map(int, input().split())
                        res[i][k] = count                                               arr = list(map(int, input().split()))
                        count += 1                                                      d = {}
                    i += 1                                                              for i in arr:
                    for k in range(i, n):                                                   if i not in d:
                        res[k][n - 1] = count                                                   d[i] = 1
                        count += 1                                                          else:
                    n -= 1                                                                      d[i] += 1
                return res                                                              for key, value in sorted(d.items(), key=lambda item: (item[1], -
                                                                                        key)):
Supplementary Comment:                                                                      print((key) * value, end=" ")
Wrong Answer with input 3. Expected output is [[1, 2, 3], [8, 9, 4], [7, 6, 5]], but
generated output is [[1, 2, 3], [6, 7, 4], [0, 0, 5]]. Rewrite the code.                Supplementary Comment:
                                                                                        Line 9, for key, value in sorted(d.items(), key=lambda item: (item[1], -key)):
After Edit:                                                                             NameError: name 'key' is not defined. Fix the bug.
class Solution:
    def generateMatrix(self, n):                                                        After Edit:
        if n == 0:                                                                      n, c = map(int, input().split())
            return []                                                                   a = list(map(int, input().split()))
        res = [[0 for i in range(n)] for j in range(n)]                                 cnt = Counter(a)
        i, j, di, dj = 0, 0, 0, 1                                                       for i in range(n):
        for k in range(1, n * n + 1):                                                       for j in range(i+1, n):
            res[i][j] = k                                                                       if cnt[a[i]] < cnt[a[j]]:
            if res[(i + di) % n][(j + dj) % n]:                                                     a[i], a[j] = a[j], a[i]
                di, dj = dj, -di                                                                elif cnt[a[i]] == cnt[a[j]]:
            i += di                                                                                 if a.index(a[i]) > a.index(a[j]):
            j += dj                                                                                      a[i], a[j] = a[j], a[i]
        return res                                                                      print(*a)


                                         (a)                                                                                    (b)

                                       Figure 6: Case Study on APPS-test dataset using GPT3 model.
                                                                                              Problem Description:                                    Question id: HumanEval-157

                                                                                              def right_angle_triangle(a, b, c):
                                                                                                '''
                                                                                                Given the lengths of the three sides of a triangle. Return True if the three
                                                                                                sides form a right-angled triangle, False otherwise.
                                                                                                A right-angled triangle is a triangle in which one angle is right angle or
                                                                                                90 degree.
                                                                                                Example:
Problem Description:                                             Question id: HumanEval-116     right_angle_triangle(3, 4, 5) == True
                                                                                                right_angle_triangle(1, 2, 3) == False
def sort_array(arr):                                                                            '''
  """
  In this Kata, you have to sort an array of non-negative integers according to               CodeGen-2B:
  number of ones in their binary representation in ascending order.                           def right_angle_triangle(a, b, c):
  For similar number of ones, sort based on decimal value.                                        if (a**2 + b**2) == c**2 or (b**2 + c**2) == a**2 or
                                                                                              (a**2 + c**2) == b**2:
  It must be implemented like this:                                                                   print("Right angled triangle")
  >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]                                              else:
  >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]                                        print("Not Right angled triangle")
  >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
                                                                                              Supplementary Comment:
  """
                                                                                              Wrong Answer with input 3, 4, 5. Expected output is True, but generated output is
CodeGen-2B:                                                                                   None. Rewrite the code.
def sort_array(arr):                                                                          After Edit:
    return sorted(arr, key = lambda x: count_ones(x))                                         def right_angle_triangle(a, b, c):
                                                                                                  if a == 0 or b == 0 or c == 0:
Supplementary Comment:                                                                                return False
Line 1, return sorted(arr, key = lambda x: count_ones(x))                                         else:
NameError: name ‘count_ones’ is not defined. Fix the bug.                                             if (a**2 + b**2) == c**2 or (b**2 + c**2) == a**2
After Edit:                                                                                   or (a**2 + c**2) == b**2:
def sort_array(arr):                                                                                      return True
    return sorted(arr, key=lambda x: (bin(x).count('1'),                                              else:
x))                                                                                                       return False


                                            (a)                                                                                       (b)

                                  Figure 7: Case Study on HumanEval dataset using CodeGen-2B model.
