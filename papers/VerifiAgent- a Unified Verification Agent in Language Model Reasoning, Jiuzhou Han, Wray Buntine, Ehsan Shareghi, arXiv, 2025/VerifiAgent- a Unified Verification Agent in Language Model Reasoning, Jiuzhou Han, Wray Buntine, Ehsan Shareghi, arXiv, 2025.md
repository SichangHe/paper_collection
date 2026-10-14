                                             VerifiAgent: a Unified Verification Agent in Language Model Reasoning

                                                                      Jiuzhou Han♮ Wray Buntine♭ Ehsan Shareghi♮
                                                                      ♮
                                                                      Department of Data Science & AI, Monash University
                                                                 ♭
                                                                   College of Engineering and Computer Science, VinUniversity
                                                                      jiuzhou.han@monash.edu wray.b@vinuni.edu.vn
                                                                                  ehsan.shareghi@monash.edu



                                                                    Abstract                                2024). To address this critical issue, several verifi-
                                                 Large language models demonstrate remark-                  cation methods have been proposed, ranging from
arXiv:2504.00406v2 [cs.CL] 21 Aug 2025




                                                 able reasoning capabilities but often produce              task-specific verifiers to generalised verification
                                                 unreliable or incorrect responses. Existing veri-          methods leveraging prompting techniques.
                                                 fication methods are typically model-specific or              Training a task-specific verifier to verify the out-
                                                 domain-restricted, requiring significant compu-            put of LLM requires specific training data. For
                                                 tational resources and lacking scalability across          instance, Ni et al. (2023) train a verification model
                                                 diverse reasoning tasks. To address these limi-
                                                                                                            that judges language-to-code outputs based on
                                                 tations, we propose VerifiAgent, a unified veri-
                                                 fication agent that integrates two levels of verifi-       both program text and execution results. Liang
                                                 cation: meta-verification, which assesses com-             et al. (2024) design verifiers trained on outputs
                                                 pleteness and consistency in model responses,              from multiple reasoning paradigms, using correct-
                                                 and tool-based adaptive verification, where Ver-           ness signals for improvement. Han et al. (2024b)
                                                 ifiAgent autonomously selects appropriate ver-             train a lightweight verifier for improving semantic
                                                 ification tools based on the reasoning type,               graph generation in text-to-graph tasks. Similarly,
                                                 including mathematical, logical, or common-
                                                                                                            Thatikonda et al. (2024) train a verifier that corrects
                                                 sense reasoning. This adaptive approach en-
                                                 sures both efficiency and robustness across dif-
                                                                                                            potential syntactic and semantic first-order logic
                                                 ferent verification scenarios. Experimental re-            translation errors. Nevertheless, these existing so-
                                                 sults show that VerifiAgent outperforms base-              lutions typically face limitations such as domain
                                                 line verification methods (e.g., deductive ver-            restriction, computational inefficiency, and lack of
                                                 ifier, backward verifier) among all reasoning              scalability when handling varied reasoning tasks.
                                                 tasks. Additionally, it can further enhance rea-           Table 1 demonstrates a feature comparison of vari-
                                                 soning accuracy by leveraging feedback from                ous verification methods.
                                                 verification results. VerifiAgent can also be
                                                                                                               In this paper, we propose VerifiAgent, a uni-
                                                 effectively applied to inference scaling, achiev-
                                                 ing better results with fewer generated samples            fied verification agent designed specifically to over-
                                                 and costs compared to existing process reward              come these limitations by offering a generalisable
                                                 models in the mathematical reasoning domain.1              and efficient verification framework. Unlike prior
                                                                                                            methods, VerifiAgent adopts a two-layer verifi-
                                         1       Introduction
                                                                                                            cation mechanism, comprising meta-verification
                                         Large language models (LLMs) have demonstrated                     and tool-based adaptive verification. The meta-
                                         significant capabilities in natural language rea-                  verification layer ensures completeness and logi-
                                         soning tasks, exhibiting potential to solve com-                   cal consistency of responses, while the tool-based
                                         plex problems across diverse domains (Yang et al.,                 adaptive verification autonomously selects appro-
                                         2024a; DeepSeek-AI et al., 2025; Dubey et al.,                     priate external tools (e.g., Python interpreters, sym-
                                         2024; OpenAI, 2023). However, despite their ad-                    bolic solvers, search engines) to deal with different
                                         vanced reasoning abilities, these models often pro-                reasoning types, including mathematical, logical,
                                         duce responses that are unreliable or incorrect,                   commonsense, and hybrid reasoning tasks.
                                         which poses substantial challenges for practical                      Our approach not only achieves superior ver-
                                         applications that require high precision and trust-                ification accuracy compared to existing baseline
                                         worthiness (Augenstein et al., 2024; Huang et al.,                 methods, such as deductive verifier (Ling et al.,
                                             Code is available at https://github.com/Jiuzhouh/
                                             1                                                              2023), backward verifier (Weng et al., 2023), but
                                         VerifiAgent.                                                       also enhances reasoning accuracy by integrating

                                                                                                        1
Method                                   Training-free   Generalised   Tool-based   Fine-grained Feedback
DIVERSE (Li et al., 2023)                     ×              ×             ×                 ×
                                                                                                                act with tools (e.g., calculators, search engines) to
                                              ×              ×             ×
PiVe (Han et al., 2024b)
Math/Code-Rev (Liang et al., 2024)            ×              ×             ✓
                                                                                             ✓
                                                                                             ×                  critique and revise their own outputs, leading to
LEVER (Ni et al., 2023)                       ×              ×             ✓                 ×
CoVe (Dhuliawala et al., 2024)                ✓              ×             ×                 ✓                  improved factuality and reasoning. Different from
CSV(Zhou et al., 2024)                        ✓              ×             ✓                 ✓
Deductive Verifier (Ling et al., 2023)
Backward Verifier (Weng et al., 2023)
                                              ✓
                                              ✓
                                                             ✓
                                                             ✓
                                                                           ×
                                                                           ×
                                                                                             ×
                                                                                             ×
                                                                                                                these works, our VerifiAgent provides a generalised
VerifiAgent (ours)                            ✓              ✓             ✓                 ✓                  verification agentic framework adaptable to diverse
                                                                                                                reasoning tasks with fine-grained feedback.
 Table 1: Comparison of various verification methods.
                                                                                                                   A broader concept of verification by LLMs is re-
                                                                                                                ferred to LLM-as-a-Judge, where LLMs are used as
detailed feedback derived from the verification pro-                                                            general evaluators for tasks like response scoring,
cess. Furthermore, VerifiAgent can be effectively                                                               pairwise comparison, and content moderation. As
applied to inference scaling, requiring significantly                                                           surveyed by Gu et al. (2024); Li et al. (2024), LLM-
fewer computational resources compared to stan-                                                                 as-a-Judge systems perform holistic evaluations, as
dard Process Reward Models (PRMs), thereby pro-                                                                 a scalable and consistent alternative to human eval-
viding a practical approach to improve LLM per-                                                                 uation, applicable in model benchmarking, safety
formance during inference. Through extensive ex-                                                                assessment, and alignment data labelling. VerifiA-
periments across three types of reasoning tasks,                                                                gent can be viewed as a specialised type of LLM-as-
we summarise two key empirical findings: 1) An                                                                  a-Judge system, specifically designed to evaluate
LLM reasoner can improve via inference scaling                                                                  the correctness of certain reasoning tasks through
methods like Majority Vote, PRMs, or VerifiAgent,                                                               tool-based verification mechanisms.
but VerifiAgent achieves higher accuracy at lower
cost. 2) VerifiAgent’s capabilities scale alongside
improvements in its backbone LLM, enabling con-
                                                                                                                2.2   Scaling Test-Time Compute
sistent performance gains on the same reasoner.

2        Related Work                                                                                           Scaling test-time compute refers to allocating more
                                                                                                                computational budget during inference via sam-
2.1         LLMs as Verifiers                                                                                   pling, deeper reasoning, or adaptive search to
Leveraging the prompting and in-contenxt learning                                                               boost model accuracy. Brown et al. (2024) present
ability of LLMs to verify the outputs of LLMs pro-                                                              a comprehensive study of inference-time scaling
vides a generalised approach of verification. Wu                                                                through repeated sampling, demonstrating that cov-
et al. (2024); Weng et al. (2023) show that LLMs                                                                erage—the probability of generating at least one
can refine reasoning chains via backward verifica-                                                              correct answer—scales log-linearly with the num-
tion or masked condition checking, while Ling et al.                                                            ber of samples. Stroebl et al. (2024) theoreti-
(2023) decompose solutions into verifiable steps                                                                cally analyse the limits of resampling, showing
using a Natural Program format. Dhuliawala et al.                                                               that imperfect verifiers lead to diminishing returns,
(2024) propose Chain-of-Verification, which de-                                                                 especially when false positives dominate. Simi-
composes the verification into a sequence of ques-                                                              larly, Setlur et al. (2025a) argue that verifier-based
tions, improving factual consistency through multi-                                                             strategies scale more robustly than verifier-free
step prompting. Hong et al. (2024) evaluate LLMs’                                                               ones, particularly when base models exhibit anti-
ability to detect logical errors, finding that while                                                            concentrated output distributions.
models can catch some flaws, their verification is                                                                 The growing use of Process Reward Models
often shallow. Stechly et al. (2024) further investi-                                                           (PRMs) suggests that fine-grained supervision over
gate the reliability of self-critique, demonstrating                                                            intermediate reasoning steps can improve model re-
that performance often degrades when doing self-                                                                liability (Lightman et al., 2024; Wang et al., 2024;
verification without external grounding.                                                                        Zhang et al., 2025). PRMs offer another strategy
   To enhance the verification quality of LLMs,                                                                 for scaling test-time compute by enhancing Best-
some methods integrate external tools. Zhou                                                                     of-N sampling (Snell et al., 2024). As a verifier,
et al. (2024) introduce code-based self-verification,                                                           VerifiAgent does not require any training process,
which prompts GPT-4 Code Interpreter to evaluate                                                                eliminating the need for collecting task-specific
and fix its answers by executing code and inter-                                                                training data. By leveraging frozen LLMs, it can
preting the output. Similarly, Gou et al. (2024)                                                                be integrated into test-time compute scaling strate-
propose CRITIC, a framework where LLMs inter-                                                                   gies, enhancing the accuracy of LLM outputs.

                                                                                                            2
3     VerfiAgent                                              comparing them with the original solution. Unlike
                                                              the meta verification stage, which evaluates general
VerifiAgent is a plug-and-play verification frame-            reasoning quality, this phase evaluates factual and
work that empowers frozen LLMs to utilise exter-              computational accuracy.
nal mechanisms to verify the correctness of solu-                VerifiAgent dynamically selects the most suit-
tions of diverse reasoning tasks. As illustrated in           able verification tool based on the nature of the task
Figure 1, VerifiAgent adopts a two-layer verifica-            and instructions. For instance, in mathematical rea-
tion mechanism, which contains two levels of veri-            soning, it may utilise a Python interpreter to verify
fication. The first level is to do a Meta Verification,       calculations, while for knowledge-based common-
and the second level is to do a Tool-based Adap-              sense reasoning, it may query a search engine to
tive Verification. The solution will be evaluated             gather relevant information. For hybrid reasoning
sequentially through the two layers. The second-              tasks, it can combine multiple tools to ensure com-
level verification can further validate the results           prehensive verification. Additionally, VerifiAgent
from meta-verification, enhancing the accuracy of             autonomously determines the required number of
the verification results. With this two-layer veri-           external tool calls, continuing until it gathers suffi-
fication mechanism, the VerifiAgent can provide               cient information to validate the answer.
fine-grained feedback of the verification process.               When VerifiAgent selects a tool for verification,
                                                              the environment returns the corresponding execu-
3.1    Meta Verification
                                                              tion result. Based on this observation, the agent
The Meta Verification aims to verify two aspects              iteratively determines its next action until the veri-
of the solution: completeness and consistency.                fication process is complete. The VerifiAgent not
The completeness refers to a solution that is self-           only ensures the accuracy of solutions but also pro-
contained, fully addresses every part of the ques-            vides a transparent and interpretable verification
tion, and contains a clear result or conclusion. The          process for natural language reasoning tasks. See
consistency refers to reasoning that follows a log-           Appendix E for examples.
ical structure with no jumps, gaps, or inconsis-
tencies. This initial layer acts as a foundational            3.3   Fine-grained Feedback
check, preventing incomplete or inconsistent solu-            Based on the two levels of verification, Veri-
tions from progressing further. Through meta verifi-          fiAgent provides a final evaluation result (i.e.,
cation, VerifiAgent ensures that only solutions with          Correct/Incorrect) to indicate the correctness
structural integrity and coherent reasoning proceed           of the solution. In addition to the verification result,
to the next tool-based adaptive verification.                 VerifiAgent also generate a Vscore as a confidence
   Since the solutions of different types of reason-          score of the verification. Vscore is calculated by
ing tasks may have different structures, to make              applying the softmax function to the log probabil-
VerifiAgent adaptable to diverse solutions, we lever-         ity of the token (Correct/Incorrect) and the log
age a unified way to rewrite the solutions in the             probabilities of the top 5 alternative tokens. Specif-
meta verification phase. Specifically, the agent will         ically:
first list all the known conditions and the final ob-
                                                                                        exp (p (t))
jective provided in the problem, then divide the                          Vscore = P5
solution into individual and explicit logical steps.                                   k=1 exp (p (tk ))
This will be beneficial for the meta verification and         where Vscore represents the confidence score for
the following tool-based adaptive verification. See           the verification result token t. the term p (t) de-
Appendix E for examples.                                      notes the log probability of the token t generated
                                                              by the LLM. p (tk ) is for k = 1 to 5 represents the
3.2    Tool-based Adaptive Verification                       log probabilities of the top five predicted tokens at
After the meta verification stage, the solution en-           the verification result token position. This equation
ters the Tool-based Adaptive Verification phase.              ensures that the confidence score reflects the rela-
This level leverages external tools, such as Python           tive likelihood of the chosen token compared to the
program interpreter, search engine and symbolic               top alternatives, effectively normalising the scores
solver, to cross-check the correctness of the solu-           within the range of 0 to 1.
tion. The agent will first solve the question using              Furthermore, when a solution is deemed incor-
appropriate tools, and then verify the results by             rect, VerifiAgent provides fine-grained feedback

                                                          3
                                                                                  VerifiAgent

    Reasoning Task & Solution            To verify the correctness of the given answer, let’s perform a Meta Verification first.
                                         1. List all the known conditions and final objective provided in the problem …
      Mathematical Reasoning             2. Divide the answer into individual and explicit logical steps …
                                         Completeness: Check if it contains a clear result or conclusion to the question…
      Commonsense Reasoning     Input
                                         Consistency: Check whether each step logically follows from the previous one …

         Logical Reasoning               The answer is complete and logically consistent. Next, let’s perform a Tool Verification.
                                         For this reasoning task, I will use … to verify …
         Hybrid Reasoning


            Feedback                                         Python Interpreter    Search Engine        Theorem Prover

         Evaluation Result
                                         The tool execution result indicates that … Based on the two verification results …
           Error Reason         Output
                                         Summarisation:
                                         Evaluation Result: [Correct/Incorrect]
         Revision Method
                                         Error Reason: There is an error in Step … , and this error is because …
                                         Revision Method: To avoid making the error again, …
         Verification Score
                                         Verification Score: …


Figure 1: An overview of VerifiAgent. Given a reasoning task and a candidate solution, VerifiAgent leverages two
levels of verification: (1) meta verification – verifying the completeness and consistency of the solution and (2)
tool-based adaptive verification – autonomously selecting appropriate tools to do the correctness verification. The
VerifiAgent can provide fine-grained feedback about the verification process based on the instruction in the prompt.

about the verification process based on the instruc-              • Deductive Verifier. Deductive Verifier (Ling
tion in the prompt. This feedback includes the iden-                  et al., 2023) enables the LLM to carry out ex-
tified error reason, derived from the two levels of                   plicit and rigorous deductive reasoning to evalu-
verification, and a potential revision method that in-                ate the correctness of a solution. It decomposes
corporates observations from tool execution results                   the verification process into a sequence of step-
(See Appendix E for examples). Such feedback                          by-step subprocesses using Natural Program,
can be leveraged to refine and enhance the solution,                  a natural language-based deductive reasoning
improving the accuracy of reasoning tasks.                            format, to facilitate the breakdown of logical
                                                                      steps in a step-by-step manner.
4     Experiment                                                  • Backward Verifier. Backward Verifier (Weng
                                                                      et al., 2023) appends the predicted answer to the
4.1     Baseline and Experimental Setup                               question while masking the original condition,
Datasets. We evaluate VerifiAgent on three natural                    then prompts the LLM to predict the masked
language reasoning tasks, including mathematical                      condition. Verification is conducted by com-
reasoning, logical reasoning, commonsense reason-                     paring the predicted condition with the original
ing, and hybrid reasoning. Specifically, for math-                    one. If the two conditions align, the solution
ematical reasoning we use GSM8K (Cobbe et al.,                        is deemed correct; otherwise, inconsistencies
2021) and MATH (Hendrycks et al., 2021), for log-                     indicate errors in the provided solution.
ical reasoning we use FOLIO (Han et al., 2024c)                   Models. We explored various combinations of
and ProverQA (Qi et al., 2025), for commonsense                   backbone LLMs for both the Reasoner and Ver-
reasoning we use HotpotQA (Yang et al., 2018)                     ifiAgent. For the Reasoner, we utilise GPT-4o, o3-
and StrategyQA (Geva et al., 2021), for hybrid rea-               mini, and Llama-3.3-70B-Instruct-Turbo, while for
soning we use ReWild (Yang et al., 2024c). The                    the VerifiAgent, we employ GPT-4o and o1-mini.
statistics of the datasets are shown in Appendix A.               In our experiments, unless explicitly stated other-
Baselines. Since VerifiAgent is a training-free and               wise, both the Reasoner and VerifiAgent default to
generalised approach, we compare it against base-                 GPT-4o as their backbone LLMs.
line methods that are similarly prompting-based
and generalised. Specifically:                                    4.2      Main Result
• Vanilla Verifier. Vanilla Verifier employs a                    Table 2 shows the performance of VerifiAgent
    structured prompt to instruct the LLM to verify               compared to baseline methods (Vanilla, Deductive,
    a solution given a problem, without relying on                and Backward Verifiers) across different reason-
    specialised mechanisms (Kamoi et al., 2024).                  ing tasks. Overall, VerifiAgent consistently out-

                                                              4
                                                           Baselines
                                                                                                      VerifiAgent
 Type              Dataset
                                Vanilla Verifier    Deductive Verifier        Backward Verifier
                               Acc    Pre    Rec    Acc       Pre      Rec    Acc    Pre    Rec    Acc    Pre    Rec
                   GSM8K      0.93   0.96    0.96   0.95     0.96      0.99   0.95   0.96   0.98   0.96   0.96   1.00
 Mathematical
                   MATH       0.75   0.73    0.86   0.80     0.76      0.86   0.82   0.80   0.88   0.85   0.86   0.92
                   FOLIO      0.75   0.78    0.96   0.73     0.73      0.95   0.74   0.76   0.96   0.76   0.78   0.97
 Logical
                  ProverQA    0.75   0.77    0.97   0.74     0.75      0.98   0.75   0.78   0.96   0.77   0.82   0.95
                 StrategyQA   0.78   0.79    0.92   0.75     0.82      0.92   0.79   0.80   0.94   0.84   0.85   0.95
 Commonsense
                 HotpotQA     0.56   0.53    0.91   0.56     0.53      0.96   0.57   0.54   0.90   0.61   0.56   0.92
 Hybrid            ReWild     0.76   0.88    0.82   0.61     0.91      0.60   0.74   0.87   0.84   0.78   0.88   0.89

Table 2: Main results of VerifiAgent on different reasoning tasks. The evaluation metrics are accuracy (Acc),
precision (Pre), and recall (Rec). Bold shows the best result for each row.


performs baselines, excelling in accuracy while              fiAgent, the process terminates; otherwise, we con-
maintaining competitive precision and recall across          tinue sampling additional candidate outputs until
mathematical, logical, commonsense, and hybrid               one passes verification or the maximum number of
reasoning tasks. Specifically, for mathematical rea-         samples is reached. For cases reaching the max-
soning tasks, VerifiAgent attains the highest accu-          imum number of samples, we select the final an-
racy (0.96 and 0.85) and recall scores (1.00 and             swer using a majority vote approach. We compare
0.92) on GSM8K and MATH datasets, respectively.              our VerifiAgent-based inference scaling method
In logical reasoning, VerifiAgent demonstrates im-           with the standard Majority Vote approach that does
provements, particularly on FOLIO (accuracy 0.76,            not employ a verifier. Majority Vote aggregates
recall 0.97) and ProverQA (precision 0.82). For              multiple sampled responses directly from reason-
commonsense reasoning tasks, VerifiAgent signifi-            ers without any verification. Table 3 demonstrates
cantly outperforms baselines on StrategyQA with              the performance across three reasoning datasets
accuracy and precision of 0.84 and 0.85, respec-             (MATH, ProverQA, and StrategyQA) using vari-
tively, while remaining competitive on HotpotQA.             ous combinations of reasoners (GPT-4o, o3-mini,
Finally, on the hybrid reasoning dataset ReWild,             and Llama-3.3-70B-Instruct-Turbo) and VerifiA-
VerifiAgent achieves the best accuracy (0.78) and            gent variants (GPT-4o and o1-mini).
recall (0.89), highlighting its verification capabili-          Across all datasets and reasoners, inference scal-
ties in handling complex reasoning tasks. To inves-          ing with VerifiAgent consistently outperforms Ma-
tigate the impact of different backbone LLMs on              jority Voting, achieving higher accuracy with fewer
VerifiAgent’s performance, we further evaluate Ver-          samples and less cost (See Appendix D). Notably,
ifiAgent using o1-mini as an alternative backbone            o3-mini reasoner achieves the highest performance
model. The results indicate that the verification            on MATH and ProverQA but the lowest on Strate-
capability of VerifiAgent scales effectively with            gyQA among all reasoners, suggesting that o3-mini
the underlying backbone model’s capacity. Due                is more proficient in mathematical and logical rea-
to the page limit, we put the detailed results in            soning than in knowledge-intensive commonsense
Appendix C.                                                  reasoning tasks. We identify two key findings: (1)
                                                             When the reasoner and VerifiAgent are the same
4.3   Inference Scaling with VerifiAgent                     model (e.g., GPT-4o) or have comparable capac-
Inference scaling aims at enhancing reasoning per-           ities (e.g., Llama-3.3-70B-Instruct-Turbo paired
formance by utilising increased computational re-            with GPT-4o), integrating VerifiAgent significantly
sources during the inference stage. However, this            enhances performance, with further improvement
approach inherently requires effective verification          achievable by employing a stronger VerifiAgent
to ensure the accuracy and reliability of generated          (e.g., o1-mini). (2) When the reasoner (o3-mini)
answers (Setlur et al., 2025b). Due to the verifi-           surpasses the VerifiAgent (GPT-4o) in capability,
cation ability of VerifiAgent, it naturally comple-          the performance gain is limited. However, pair-
ments inference scaling approaches by serving as             ing a strong reasoner with a stronger VerifiAgent
an effective verifier during the inference process.          (o1-mini) substantially enhances performance.
Specifically, we first sample an output from the                PRMs provide another approach to inference
LLM. If this output passes verification by the Veri-         scaling. We investigated two open-source PRMs

                                                         5
            Method                                          MATH         ProverQA         StrategyQA
            GPT-4o Reasoner                                 69.4(1)        75.3(1)          84.2(1)
            - IS w/ Majority Vote @10                      73.5(10)       77.0(10)         85.6(10)
            - IS w/ VerifiAgent (GPT-4o)                   74.0(1.5)      77.3(1.6)        86.0(1.3)
            - IS w/ VerifiAgent (o1-mini)                  78.0(1.8)      77.7(1.3)        87.3(1.2)
            o3-mini Reasoner                                87.9(1)        78.3(1)          76.4(1)
            - IS w/ Majority Vote @8                       91.1(10)       80.0(10)         78.2(10)
            - IS w/ VerifiAgent (GPT-4o)                   88.3(1.3)      79.1(1.1)        78.6(1.3)
            - IS w/ VerifiAgent (o1-mini)                  91.4(1.1)      80.7(1.1)        79.0(1.6)
            Llama-3.3-70B-Instruct-Turbo Reasoner           62.3(1)        70.6(1)          83.8(1)
            - IS w/ with Majority Vote @10                 68.3(10)       71.7(10)         84.7(10)
            - IS w/ VerifiAgent (GPT-4o)                   69.7(2.0)      72.0(1.3)        85.1(1.3)
            - IS w/ VerifiAgent (o1-mini)                  71.1(2.2)      74.0(1.3)        85.1(1.4)

Table 3: Results of different Reasoners with Inference Scaling (IS) methods on three datasets. The number in the
bracket denotes the average number of samples for each question.

                                                                                   MATH    ProverQA    StrategyQA
specifically designed for the MATH dataset:
                                                            Init. Reasoning Acc.   69.4       75.3        84.3
Qwen2.5-Math-PRM-7B and Qwen2.5-Math-7B-
PRM800K, which fine-tune Qwen2.5-Math-7B-                   Feedback Type             Precaution-Based Feedback
Instruct using synthetic data from Qwen mod-                Verification Result    69.7       76.0        84.3
els (Zhang et al., 2025) and PRM800K (Light-                + Error Reason         74.9       77.0        85.6
                                                            + Mitigation Method    73.4       77.6        86.0
man et al., 2024), respectively. These PRMs as-
                                                            Feedback Type           Post-Editing-Based Feedback
sign scores to each reasoning step, and we use the
last step score as the final response score. Follow-        Verification Result    71.7       77.3        84.7
                                                            + Error Reason         72.3       74.7        84.3
ing previous studies (Zhang et al., 2025; Light-            + Mitigation Method    72.6       74.3        83.8
man et al., 2024; Yang et al., 2024b; Wang et al.,
2024), we evaluate the PRMs using the Best-of-              Table 4: Results of feedback utilisation on GPT-4o.
N sampling strategy, selecting the highest-scored
response from N candidates according to a PRM.
The evaluation results for the GPT-4o and Qwen2.5-         Qwen2.5-Math-7B-Instruct gains greater improve-
Math-7B-Instruct reasoners are shown in Figure 2.          ments from Qwen2.5-Math-PRM-7B. We hypoth-
As the number of samples increases, both Majority          esise that the linguistic discrepancies may affect
Vote and Best-of-N sampling strategies consistently        the performance of PRMs. Specifically, Qwen2.5-
improve in accuracy. When sampling 10 responses,           Math-7B-PRM800K utilises synthetic data from
the Best-of-N method’s accuracy approaches that            GPT-style LLMs for training, while Qwen2.5-
of VerifiAgent, which notably achieves comparable          Math-PRM-7B employs data generated by Qwen-
performance with significantly fewer average sam-          style LLMs for training.
ples (1.5 and 1.6 on GPT-4o reasoner and Qwen2.5-
Math-7B-Instruct reasoner, respectively).                  4.4   Exploration on Feedback Utilisation
   Interestingly, the two PRMs exhibit distinct be-        VerifiAgent provides fine-grained feedback during
haviours depending on the reasoner. For the GPT-           verification, which includes an explicit error rea-
4o reasoner, Qwen2.5-Math-7B-PRM800K sig-                  son and a suggested revision method for enhanc-
nificantly outperforms Qwen2.5-Math-PRM-7B,                ing solutions. To evaluate the effectiveness of this
which even underperforms relative to the Majority          feedback, we conducted experiments using two dis-
Vote baseline. However, for the Qwen2.5-Math-              tinct methods: precaution-based and post-editing-
7B-Instruct reasoner, Qwen2.5-Math-PRM-7B out-             based feedback. In the precaution-based method,
performs Qwen2.5-Math-7B-PRM800K at 10 sam-                the LLM leverages feedback from previous verifica-
ples. These results indicate that GPT-4o benefits          tion attempts to proactively generate a new solution.
more from Qwen2.5-Math-7B-PRM800K, whereas                 Conversely, the post-editing-based method allows

                                                       6
                    Accuracy on MATH 350 Test Cases using GPT-4o Reasoner               Method                         MATH      ProverQA    StrategyQA
               74
                                                                                        GPT-4o (Tool-use)              56.9        47.8            83.5
               73                                                                       GPT-4o (Tool-use) + Feedback   61.5        50.3            85.7
                                                                                        GPT-4o (CoT)                   69.4        75.3            84.3
               72                                                                       GPT-4o (CoT) + Feedback        73.4        77.6            86.0
Accuracy (%)




               71
                                                                                        Table 5: Resutls of GPT-4o reasoner using CoT and
               70
                                                                                        Tool with feedback on three different reasoning tasks.
                                             Majority Vote @N
               69                            Best-of-N (Qwen2.5-Math-PRM-7B)
                                             Best-of-N (Qwen2.5-Math-7B-PRM800K)
               68                            GPT-4o+VerifiAgent                                  Dataset (Method)         Acc      Pre      Rec
                                             GPT-4o
                        2           4             6             8            10                  MATH (CoT)               0.85     0.86     0.92
                                      Number of Samples
                                                                                                 MATH (Tool-use)          0.82     0.83     0.90
                                (a) GPT-4o Reasoner
                                                                                                 ProverQA (CoT)           0.77     0.82     0.95
    Accuracy on MATH 350 Test Cases using Qwen2.5-Math-7B-Instruct Reasoner
                                                                                                 ProverQA (Tool-use)      0.75     0.79     0.93
               74
                                                                                                 StrtegyQA (CoT)          0.84     0.85     0.95
               73                                                                                StrtegyQA (Tool-use)     0.80     0.84     0.92
               72
Accuracy (%)




                                                                                        Table 6: Results of VerifiAgent evaluating CoT and
               71                                                                       Tool-use outputs on different reasoning tasks.
               70                            Majority Vote @N
                                             Best-of-N (Qwen2.5-Math-PRM-7B)
               69                            Best-of-N (Qwen2.5-Math-7B-PRM800K)
                                             Qwen2.5-Math-7B-Instruct+VerifiAgent       4.5    VerifiAgent on Tool-based Reasoner
               68                            Qwen2.5-Math-7B-Instruct
                        2           4             6             8              10       To evaluate the effectiveness of VerifiAgent on tool-
                                      Number of Samples
                                                                                        based reasoning tasks, we conducted experiments
                       (b) Qwen2.5-Math-7B-Instruct Reasoner
                                                                                        using a tool-using reasoner with access to the same
Figure 2: Results of GPT-4o Reasoner and Qwen2.5-                                       tools as VerifiAgent. Specifically, we evaluated
Math-7B-Instruct Reasoner with different inference scal-                                GPT-4o on MATH, ProverQA, and StrategyQA,
ing methods on MATH. VerifiAgent uses GPT-4o as the                                     where the model was instructed to use the Python
backbone LLM.                                                                           interpreter, Z3 Theorem Prover, and Search Engine,
                                                                                        respectively. We then applied VerifiAgent to these
                                                                                        outputs, leveraging its feedback to further improve
the LLM to directly refine its previous incorrect                                       performance. The results are shown in Table 5.
solution based on feedback provided.                                                       Interestingly, the tool-use baseline does not
                                                                                        outperform CoT, especially in math and logic
   We explored three feedback settings for each
                                                                                        reasoning. This trend is also observed in prior
method: (1) verification result only (i.e., simply
                                                                                        works (Yao et al., 2023; Han et al., 2024a), where
indicating “Incorrect”), (2) verification result with
                                                                                        tool-augmented methods such as ReAct can under-
error reason, and (3) verification result with both er-
                                                                                        perform compared to CoT. We hypothesise this is
ror reason and revision method. Experiments were
                                                                                        due to several factors: (1) For simpler problems,
conducted on instances initially identified as “Incor-
                                                                                        LLMs may already solve them accurately via CoT,
rect” by VerifiAgent, and the results are presented
                                                                                        and mandatory tool use may introduce unnecessary
in Table 4.
                                                                                        complexity and more opportunities for errors. (2)
   Overall, precaution-based feedback consistently                                      For more difficult tasks, the LLM may still struggle
outperforms post-editing-based feedback, indicat-                                       to solve them effectively, even with tools. (3) The
ing the inherent difficulty for LLMs to effectively                                     external knowledge from inaccurate tool-use can
correct previously incorrect responses. Addition-                                       sometimes mislead the LLM’s correct prior knowl-
ally, within precaution-based feedback, providing                                       edge. Despite these challenges, integrating Veri-
richer information typically yields greater improve-                                    fiAgent feedback consistently improves tool-use
ments. For post-editing-based feedback, however,                                        accuracy across all datasets, though results still lag
mathematical reasoning tasks benefit from more                                          behind CoT+Feedback in math and logic. For com-
detailed feedback, whereas logical and common-                                          monsense tasks (StrategyQA), tool-use approaches
sense reasoning tasks achieve better performance                                        CoT+Feedback performance.
with simpler, less detailed feedback.                                                      We also measured VerifiAgent’s verification per-

                                                                                    7
                1.00                                                                                    1.4%
                                                       Correct Solution
                0.95                                   Incorrect Solution
                                                                                                       MATH           StrategyQA
                0.90
                0.85                                                                                  98.6%            100.0%
       Vscore                                                                                                                          Python Interpreter
                0.80                                                                                                                   Search Engine
                                                                                                                                       Symbolic Solver
                                                                                                                            11.2%
                0.75                                                                                                            4.3%
                0.70                                                                                  ProverQA          ReWild
                0.65
                                                                                                      100.0%        84.5%
                          MATH              ProverQA       StrategyQA

Figure 3: The floating bar chart comparing Vscore distri-                                  Figure 4: The pie charts showing the relative usage
butions (mean ± std) for correct and incorrect solutions                                   frequency of three different tools by the VerifiAgent
across three datasets. The horizontal grey line indicates                                  across four types of reasoning tasks.
the mean.

                              MATH              ProverQA           StragegyQA
Method
                       Acc     Pre   Rec     Acc    Pre    Rec    Acc    Pre    Rec        across three datasets. As illustrated, the mean
Vanilla Verifier       0.75   0.73   0.86    0.75   0.77   0.97   0.78   0.79   0.92       Vscore for correct solutions is slightly higher than
Deductive Verifier     0.80   0.76   0.86    0.74   0.75   0.98   0.75   0.82   0.92
Backward Verifier      0.82   0.80   0.88    0.75   0.78   0.96   0.79   0.80   0.94
                                                                                           for incorrect ones on all the reasoning tasks. Since
VerifiAgent            0.85   0.86   0.92    0.77   0.82   0.95   0.84   0.85   0.95       Vscore represents the confidence of the verification
- w/o meta v.          0.79   0.78   0.96    0.74   0.81   0.90   0.83   0.83   0.94       result, this indicates that the VerifiAgent is more
- w/o tool v.          0.75   0.75   0.98    0.74   0.75   0.98   0.78   0.80   0.96
                                                                                           confident when identifying correct solutions com-
      Table 7: Ablation study results of VerifiAgent.                                      pared to incorrect ones. Additionally, the consis-
                                                                                           tently lower variance in Vscore among correct solu-
formance on both CoT and tool-use outputs, shown                                           tions further supports the reliability of the agent in
in Table 6. While performance is slightly lower                                            verifying correct responses.
for tool-use outputs, which is expected, since Ver-
ifiAgent is not designed specifically for program                                          Tool Usage Analysis. VerifiAgent autonomously
or tool-use evaluation. This points an important                                           determines the reasoning type of a task and selects
direction for future work, enhancing VerifiAgent’s                                         the appropriate tool for verification. Figure 4 illus-
robustness in verifying tool-based reasoning.                                              trates tool usage across four reasoning task types.
                                                                                           For the MATH dataset (mathematical), the Python
4.6      Ablation Study                                                                    Interpreter is predominantly used (98.6%), with
Meta verification and tool verification are two es-                                        minimal reliance on the Symbolic Solver (1.4%),
sential components of VerifiAgent. To evaluate the                                         reflecting the computational nature of the task.
individual contributions of these components, we                                           StrategyQA (commonsense) exclusively relies on
conducted an ablation study, with results presented                                        the Search Engine (100%), highlighting its depen-
in Table 7. Results demonstrate that removing ei-                                          dence on external knowledge for the verification.
ther meta verification or tool verification consis-                                        ProverQA (logical) solely utilises the Symbolic
tently reduces VerifiAgent’s performance across all                                        Solver (100%), aligning with its need for logical
datasets. Specifically, omitting meta verification                                         and symbolic reasoning. ReWild (hybrid) shows a
leads to noticeable declines in overall accuracy,                                          more balanced tool distribution, primarily using the
while removing tool verification results in even                                           Python Interpreter (84.5%), supplemented by the
more substantial performance reductions, bringing                                          Symbolic Solver (11.2%) and the Search Engine
the performance close to baseline levels. Addition-                                        (4.3%). The results demonstrate that the VerifiA-
ally, tool verification tends to enhance accuracy                                          gent effectively selects appropriate external tools
and precision, whereas meta verification primar-                                           based on the nature of the reasoning task.
ily improves recall. These findings underscore the                                         Error Analysis. To further investigate the capa-
complementary roles of meta and tool verification,                                         bility of VerifiAgent, we conducted an error anal-
with each contributing uniquely to the effectiveness                                       ysis on different types of questions. The MATH
of VerifiAgent.                                                                            dataset contains seven types of math problems: Al-
                                                                                           gebra (Alg), Counting&Probability (Count&Prob),
5     Analysis
                                                                                           Geometry (Geo), Intermediate Algebra (Int Alg),
Verification Score Visualisation. Figure 3 visu-                                           Number Theory (Num Thr), Prealgebra (PreAlg)
alises the Vscore for correct and incorrect solutions                                      and Precalculus (PreCal). The ProverQA classifies

                                                                                       8
              PreCal                      Geo                   Count&Prob     PreAlg        Int Alg     Alg     Num Thr
             (26.9%)                    (23.9%)                   (11.9%)     (11.9%)       (10.4%)    (9.0%)     (6.0%)
                                Hard                                              Medium                     Easy
                              (58.6%)                                             (27.1%)                  (14.3%)
               Level 2                            Level 5                      Level 3                 Level 4
               (30.1%)                            (28.5%)                      (21.7%)                 (19.7%)
0                        20                40                           60                    80                      100
                                                     Percentage (%)

Figure 5: The proportion of different question types among VerifiAgent’s incorrectly verified examples by GPT-4o
Reasoner. From top to bottom, the bars represent MATH, ProverQA, and StrategyQA datasets, respectively. For
MATH and ProverQA, the number of questions in each type is the same. For the imbalanced StrategyQA, the
proportion is normalised by the total number of questions per difficulty level.


the question into three types based on the difficulty           ifiAgent employs a two-layer verification frame-
level: Hard, Medium and Easy. Although Strate-                  work combining meta-verification, which assesses
gyQA does not explicitly label questions by diffi-              completeness and consistency, and adaptive tool-
culty, each question includes a decomposition into              based verification tailored to each reasoning type.
sub-questions that reflect its reasoning pathway.               Experimental results demonstrate that VerifiAgent
We used the number of decomposed sub-questions                  consistently outperforms baseline methods in ver-
(ranging from 1 to 5) as an indicator of question               ification accuracy. Additionally, VerifiAgent can
difficulty, classifying them into five levels (Level 1          be integrated with inference scaling approaches,
through Level 5).                                               achieving improved performance with fewer sam-
   Figure 5 illustrates the distribution of question            ples than PRMs. Overall, VerifiAgent provides an
types among cases where VerifiAgent provided in-                efficient and scalable solution, enhancing the relia-
correct verifications. In the MATH dataset, Pre-                bility and trustworthiness of large language model
calculus and Geometry questions accounted for                   reasoning.
the highest proportion of errors, suggesting these                 VerifiAgent heavily relies on the instruction-
question types pose greater verification challenges             following capabilities of the backbone LLM, mean-
for VerifiAgent. Errors in Counting & Probabil-                 ing that only models proficient at accurately in-
ity, Prealgebra, Intermediate Algebra, and Algebra              terpreting and executing instructions can serve
occurred at similar rates, while VerifiAgent per-               effectively as the backbone. This reliance indi-
formed best on Number Theory problems. This                     cates the importance of selecting suitable backbone
trend is in line with the capability of the backbone            LLMs to ensure optimal performance. VerifiA-
LLMs. See Appendix B for the error distributions                gent currently supports only three verification tools
on each type of question.                                       (Python interpreter, search engine, and symbolic
   For ProverQA, VerifiAgent’s verification accu-               solver). Expanding its capabilities by integrating
racy correlated clearly with question difficulty,               additional verification tools could further enhance
making the highest number of errors on Hard ques-               VerifiAgent’s adaptability and effectiveness across
tions and the fewest on Easy questions. Conversely,             a broader range of reasoning scenarios.
no clear error pattern emerged for StrategyQA.
Since verification relies mainly on search engines              Limitations
to retrieve factual knowledge, VerifiAgent appears
                                                                Our study has two primary limitations. First, due
capable of accessing sufficient information irre-
                                                                to the significant computational costs associated
spective of question difficulty, indicating that the
                                                                with accessing and running LLMs, we were un-
complexity of questions in StrategyQA has mini-
                                                                able to evaluate a comprehensive range of models,
mal impact on verification performance.
                                                                necessitating a selection of representative models.
6   Conclusion                                                  Second, the current implementation of VerifiAgent
                                                                only supports three tools. While these demonstrate
In this paper, we introduced VerifiAgent, a uni-                its core capabilities, we plan to expand the toolset
fied verification agent that verifies and improves              in future work to enhance its versatility and appli-
outputs from LLMs across mathematical, logical,                 cability across more verification scenarios.
commonsense, and hybrid reasoning tasks. Ver-

                                                            9
References                                                       Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan,
                                                                    Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen,
Isabelle Augenstein, Timothy Baldwin, Meeyoung Cha,                 Shengjie Ma, Honghao Liu, Yuanzhuo Wang, and
   Tanmoy Chakraborty, Giovanni Luca Ciampaglia,                    Jian Guo. 2024. A survey on llm-as-a-judge. CoRR,
   David P. A. Corney, Renee DiResta, Emilio Ferrara,               abs/2411.15594.
   Scott Hale, Alon Y. Halevy, Eduard H. Hovy, Heng
   Ji, Filippo Menczer, Rubén Míguez, Preslav Nakov,             Jiuzhou Han, Wray L. Buntine, and Ehsan Shareghi.
   Dietram Scheufele, Shivam Sharma, and Giovanni                   2024a. Towards uncertainty-aware language agent.
   Zagni. 2024. Factuality challenges in the era of large           In Findings of the Association for Computational
   language models and opportunities for fact-checking.             Linguistics, ACL 2024, Bangkok, Thailand and vir-
   Nat. Mac. Intell., 6(8):852–863.                                 tual meeting, August 11-16, 2024, pages 6662–6685.
                                                                    Association for Computational Linguistics.
Bradley C. A. Brown, Jordan Juravsky, Ryan Ehrlich,
  Ronald Clark, Quoc V. Le, Christopher Ré, and                  Jiuzhou Han, Nigel Collier, Wray L. Buntine, and Ehsan
  Azalia Mirhoseini. 2024. Large language monkeys:                  Shareghi. 2024b. Pive: Prompting with iterative veri-
  Scaling inference compute with repeated sampling.                 fication improving graph-based generative capability
  CoRR, abs/2407.21787.                                             of llms. In Findings of the Association for Compu-
                                                                    tational Linguistics, ACL 2024, Bangkok, Thailand
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,                     and virtual meeting, August 11-16, 2024, pages 6702–
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias                    6718. Association for Computational Linguistics.
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
  Nakano, Christopher Hesse, and John Schulman.                  Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-
  2021. Training verifiers to solve math word prob-                ing Qi, Martin Riddell, Wenfei Zhou, James Coady,
  lems. CoRR, abs/2110.14168.                                      David Peng, Yujie Qiao, Luke Benson, Lucy Sun,
                                                                   Alexander Wardle-Solano, Hannah Szabó, Ekaterina
DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang,                  Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,
  Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,                 Brian Wong, Malcolm Sailor, and 16 others. 2024c.
  Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang,                 FOLIO: natural language reasoning with first-order
  Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhi-                    logic. In Proceedings of the 2024 Conference on
  hong Shao, Zhuoshu Li, Ziyi Gao, and 81 others.                  Empirical Methods in Natural Language Processing,
  2025. Deepseek-r1: Incentivizing reasoning capa-                 EMNLP 2024, Miami, FL, USA, November 12-16,
  bility in llms via reinforcement learning. CoRR,                 2024, pages 22017–22031. Association for Computa-
  abs/2501.12948.                                                  tional Linguistics.
Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu,                   Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Ja-             Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
  son Weston. 2024. Chain-of-verification reduces hal-             cob Steinhardt. 2021. Measuring mathematical prob-
  lucination in large language models. In Findings of              lem solving with the MATH dataset. In Proceedings
  the Association for Computational Linguistics, ACL               of the Neural Information Processing Systems Track
  2024, Bangkok, Thailand and virtual meeting, Au-                 on Datasets and Benchmarks 1, NeurIPS Datasets
  gust 11-16, 2024, pages 3563–3578. Association for               and Benchmarks 2021, December 2021, virtual.
  Computational Linguistics.
                                                                 Ruixin Hong, Hongming Zhang, Xinyu Pang, Dong Yu,
Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,                   and Changshui Zhang. 2024. A closer look at the
  Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,                  self-verification abilities of large language models
  Akhil Mathur, Alan Schelten, Amy Yang, Angela                    in logical reasoning. In Proceedings of the 2024
  Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang,                Conference of the North American Chapter of the
  Archi Mitra, Archie Sravankumar, Artem Korenev,                  Association for Computational Linguistics: Human
  Arthur Hinsvark, Arun Rao, Aston Zhang, and 82                   Language Technologies (Volume 1: Long Papers),
  others. 2024. The llama 3 herd of models. CoRR,                  NAACL 2024, Mexico City, Mexico, June 16-21, 2024,
  abs/2407.21783.                                                  pages 900–925. Association for Computational Lin-
                                                                   guistics.
Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot,
 Dan Roth, and Jonathan Berant. 2021. Did aristotle              Xiaowei Huang, Wenjie Ruan, Wei Huang, Gaojie
 use a laptop? A question answering benchmark with                 Jin, Yi Dong, Changshun Wu, Saddek Bensalem,
 implicit reasoning strategies. Trans. Assoc. Comput.              Ronghui Mu, Yi Qi, Xingyu Zhao, Kaiwen Cai, Yang-
 Linguistics, 9:346–361.                                           hao Zhang, Sihao Wu, Peipei Xu, Dengyu Wu, André
                                                                   Freitas, and Mustafa A. Mustafa. 2024. A survey of
Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,                 safety and trustworthiness of large language models
  Yujiu Yang, Nan Duan, and Weizhu Chen. 2024.                     through the lens of verification and validation. Artif.
  CRITIC: large language models can self-correct with              Intell. Rev., 57(7):175.
  tool-interactive critiquing. In The Twelfth Inter-
  national Conference on Learning Representations,               Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han,
  ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-                and Rui Zhang. 2024. When can llms Actually cor-
  Review.net.                                                      rect their own mistakes? A critical survey of self-


                                                            10
  correction of llms. Trans. Assoc. Comput. Linguis-             Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Ku-
  tics, 12:1417–1440.                                              mar. 2024. Scaling LLM test-time compute optimally
                                                                   can be more effective than scaling model parameters.
Dawei Li, Bohan Jiang, Liangjie Huang, Alimohammad                 CoRR, abs/2408.03314.
  Beigi, Chengshuai Zhao, Zhen Tan, Amrita Bhat-
  tacharjee, Yuxuan Jiang, Canyu Chen, Tianhao Wu,               Kaya Stechly, Karthik Valmeekam, and Subbarao Kamb-
  Kai Shu, Lu Cheng, and Huan Liu. 2024. From gen-                 hampati. 2024. On the self-verification limitations
  eration to judgment: Opportunities and challenges of             of large language models on reasoning and planning
  llm-as-a-judge. CoRR, abs/2411.16594.                            tasks. CoRR, abs/2402.08115.

Yifei Li, Zeqi Lin, Shizhuo Zhang, Qiang Fu, Bei Chen,           Benedikt Stroebl, Sayash Kapoor, and Arvind
  Jian-Guang Lou, and Weizhu Chen. 2023. Making                    Narayanan. 2024. Inference scaling flaws: The limits
   language models better reasoners with step-aware                of LLM resampling with imperfect verifiers. CoRR,
  verifier. In Proceedings of the 61st Annual Meeting              abs/2411.17501.
   of the Association for Computational Linguistics (Vol-
   ume 1: Long Papers), ACL 2023, Toronto, Canada,               Ramya Keerthy Thatikonda, Jiuzhou Han, Wray L. Bun-
  July 9-14, 2023, pages 5315–5333. Association for                tine, and Ehsan Shareghi. 2024. Strategies for im-
   Computational Linguistics.                                      proving nl-to-fol translation with llms: Data genera-
                                                                   tion, incremental fine-tuning, and verification. CoRR,
Zhenwen Liang, Ye Liu, Tong Niu, Xiangliang Zhang,                 abs/2409.16461.
  Yingbo Zhou, and Semih Yavuz. 2024. Improv-
  ing LLM reasoning through scaling inference com-               Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
  putation with collaborative verification. CoRR,                  Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
  abs/2410.05318.                                                  2024. Math-shepherd: Verify and reinforce llms step-
                                                                   by-step without human annotations. In Proceedings
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-               of the 62nd Annual Meeting of the Association for
  son Edwards, Bowen Baker, Teddy Lee, Jan Leike,                  Computational Linguistics (Volume 1: Long Papers),
  John Schulman, Ilya Sutskever, and Karl Cobbe.                   ACL 2024, Bangkok, Thailand, August 11-16, 2024,
  2024. Let’s verify step by step. In The Twelfth In-              pages 9426–9439. Association for Computational
  ternational Conference on Learning Representations,              Linguistics.
  ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-
  Review.net.                                                    Yixuan Weng, Minjun Zhu, Fei Xia, Bin Li, Shizhu He,
                                                                   Shengping Liu, Bin Sun, Kang Liu, and Jun Zhao.
Zhan Ling, Yunhao Fang, Xuanlin Li, Zhiao Huang,                   2023. Large language models are better reasoners
  Mingu Lee, Roland Memisevic, and Hao Su. 2023.                   with self-verification. In Findings of the Associa-
  Deductive verification of chain-of-thought reason-               tion for Computational Linguistics: EMNLP 2023,
  ing. In Advances in Neural Information Processing                Singapore, December 6-10, 2023, pages 2550–2575.
  Systems 36: Annual Conference on Neural Informa-                 Association for Computational Linguistics.
  tion Processing Systems 2023, NeurIPS 2023, New
  Orleans, LA, USA, December 10 - 16, 2023.                      Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan
                                                                   Tan, Chao Shen, and Meng Jiang. 2024. Large lan-
Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoy-               guage models can self-correct with minimal effort.
  anov, Wen-Tau Yih, Sida I. Wang, and Xi Victoria                 CoRR, abs/2405.14092.
  Lin. 2023. LEVER: learning to verify language-to-
  code generation with execution. In International               An Yang, Baosong Yang, Beichen Zhang, Binyuan
  Conference on Machine Learning, ICML 2023, 23-                   Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayi-
  29 July 2023, Honolulu, Hawaii, USA, volume 202                  heng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian
  of Proceedings of Machine Learning Research, pages               Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Ji-
  26106–26128. PMLR.                                               axi Yang, Jingren Zhou, Junyang Lin, Kai Dang, and
                                                                   22 others. 2024a. Qwen2.5 technical report. CoRR,
OpenAI. 2023. GPT-4 technical report.            CoRR,             abs/2412.15115.
  abs/2303.08774.
                                                                 An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
Chengwen Qi, Ren Ma, Bowen Li, He Du, Binyuan Hui,                 Bowen Yu, Chengpeng Li, Dayiheng Liu, Jian-
  Jinwang Wu, Yuanjun Laili, and Conghui He. 2025.                 hong Tu, Jingren Zhou, Junyang Lin, Keming Lu,
  Large language models meet symbolic provers for                  Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang
  logical reasoning evaluation.                                    Ren, and Zhenru Zhang. 2024b. Qwen2.5-math tech-
                                                                   nical report: Toward mathematical expert model via
Amrith Setlur, Nived Rajaraman, Sergey Levine, and                 self-improvement. CoRR, abs/2409.12122.
 Aviral Kumar. 2025a. Scaling test-time compute
 without verification or RL is suboptimal. CoRR,                 Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi,
 abs/2502.12118.                                                   and Faramarz Fekri. 2024c. Can llms reason in the
                                                                   wild with programs? In Findings of the Association
Amrith Rajagopal Setlur, Nived Rajaraman, Sergey                   for Computational Linguistics: EMNLP 2024, Miami,
 Levine, and Aviral Kumar. 2025b. Scaling test-time                Florida, USA, November 12-16, 2024, pages 9806–
 compute without verification or rl is suboptimal.                 9829. Association for Computational Linguistics.


                                                            11
Dataset    GSM8K        MATH    FOLIO    ProverQA        StrategyQA       HotpotQA      ReWild        Method                          MATH    ProverQA   StrategyQA
Size        300         350      204           300           229            200          491
                                                                                                      GPT-4o Reasoner                 0.018    0.003       0.008
                                                                                                      - IS w/ Majority Vote @10       0.175    0.025       0.089
             Table 8: The statistics of the datasets.                                                 - IS w/ VerifiAgent (GPT-4o)    0.047    0.024       0.022
                                                                                                      - IS w/ VerifiAgent (o1-mini)   0.051    0.028       0.019
                                MATH                    ProverQA             StragegyQA
Method                                                                                                o3-mini Reasoner                0.007    0.002       0.005
                         Acc     Pre    Rec      Acc      Pre      Rec     Acc    Pre     Rec
                                                                                                      - IS w/ Majority Vote @8        0.067    0.018       0.042
VerifiAgent (GPT-4o)     0.85   0.86    0.92     0.77     0.82     0.95    0.84   0.85    0.95
VerifiAgent (o1-mini)    0.86   0.86    0.98     0.78     0.84     0.96    0.84   0.87    0.96
                                                                                                      - IS w/ VerifiAgent (GPT-4o)    0.022    0.016       0.018
                                                                                                      - IS w/ VerifiAgent (o1-mini)   0.024    0.015       0.022
Table 9: Results of VerifiAgent using different backbone
LLMs on three tasks.                                                                                  Table 10: The average cost (in $) per instance for dif-
                                                                                                      ferent methods across three datasets, including both
                                                                                                      the reasoner cost and the cost of the inference scaling
Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Ben-                                                     method.
  gio, William W. Cohen, Ruslan Salakhutdinov, and
  Christopher D. Manning. 2018. Hotpotqa: A dataset
  for diverse, explainable multi-hop question answer-                                                 backbone LLMs, these results indicate that the ver-
  ing. In Proceedings of the 2018 Conference on Em-                                                   ification capability of VerifiAgent scales effectively
  pirical Methods in Natural Language Processing,
  Brussels, Belgium, October 31 - November 4, 2018,
                                                                                                      with the underlying backbone model’s capacity.
  pages 2369–2380. Association for Computational
  Linguistics.                                                                                        D     Inference Cost Comparison
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak                                                      Table 10 demonstrates the average inference cost
  Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023.
                                                                                                      per instance for different methods across three
  React: Synergizing reasoning and acting in language
  models. In The Eleventh International Conference                                                    datasets. Compared to Majority Vote, Inference
  on Learning Representations, ICLR 2023, Kigali,                                                     Scaling with VerifiAgent methods yields substan-
  Rwanda, May 1-5, 2023. OpenReview.net.                                                              tially lower inference costs on MATH and Strat-
Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen                                                      egyQA, whereas on ProverQA, both approaches
  Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jin-                                                      demonstrate similar cost levels. These results in-
  gren Zhou, and Junyang Lin. 2025. The lessons of                                                    dicate that VerifiAgent not only enhances perfor-
  developing process reward models in mathematical                                                    mance, but also offers greater cost-efficiency.
  reasoning. CoRR, abs/2501.07301.
                                                                                                         Figure 7 shows the average cost versus accu-
Aojun Zhou, Ke Wang, Zimu Lu, Weikang Shi, Sichun                                                     racy on the three datasets. We can find that using
  Luo, Zipeng Qin, Shaoqing Lu, Anya Jia, Linqi Song,                                                 a strong reasoner (o3-mini for math, logic reason-
  Mingjie Zhan, and Hongsheng Li. 2024. Solving
  challenging math word problems using GPT-4 code                                                     ing) without any inference scaling techniques could
  interpreter with code-based self-verification. In The                                               achieve better performance than using a weak rea-
  Twelfth International Conference on Learning Rep-                                                   soner with inference scaling techniques. In ad-
  resentations, ICLR 2024, Vienna, Austria, May 7-11,                                                 dition, A strong reasoner can still leverage infer-
  2024. OpenReview.net.
                                                                                                      ence scaling techniques to further enhance its per-
Appendix                                                                                              formance on the task. VerifiAgent is more effec-
                                                                                                      tive than Majority Vote, with higher accuracy with
A         Data Statistics                                                                             lower cost.
Table 8 illustrates the statistics of the datasets.
                                                                                                      E     Example of VerifiAgent Trajectory
B         Error Statistics
                                                                                                          An Example VerifiAgent Trajectory on
Figure 6 shows the error statistics of the three                                                          MATH Dataset
datasets on the GPT-4o reasoner.
                                                                                                          Question:
C         Different backbone LLMs for                                                                     What is the smallest positive integer n such
          VerifiAgent                                                                                     that, out of the n unit fractions k1 where
                                                                                                          1 ≤ k ≤ n, exactly half of the fractions
Table 9 compares the performance of VerifiAgent                                                           give a terminating decimal?
(o1-mini) with VerifiAgent (GPT-4o) across three
reasoning tasks. Given that VerifiAgent does not                                                          GPT-4o Solution:
require additional training data and utilises frozen

                                                                                                 12
                 MATH                PreCal                                   Geo                    Int Alg                      Count/Prob        PreAlg Num Thr Alg
                                    (25.2%)                                 (22.5%)                 (19.8%)                        (14.4%)          (8.1%) (5.4%) (4.5%)

          ProverQA                                         Hard                                                         Medium                                Easy
                                                         (56.8%)                                                        (29.7%)                             (13.5%)

    StrategyQA                          Level 3                                        Level 2                              Level 5                        Level 4
                                        (32.0%)                                        (27.2%)                              (26.8%)                        (13.9%)
                        0                         20                              40                        60                                 80                     100
                                                                                           Percentage (%)

 Figure 6: The proportion of different question types among the incorrectly answered examples by GPT-4o Reasoner.
 From top to bottom, the bars represent MATH, ProverQA, and StrategyQA datasets, respectively. For MATH and
 ProverQA, the number of questions in each type is the same. For the imbalanced StrategyQA, the proportion is
 normalised by the total number of questions per difficulty level.

                                   MATH                                                 StrategyQA                                                  ProverQA
               90
               85
Accuracy (%)




                                                             Accuracy (%)




                                                                                                                   Accuracy (%)
               80
               75
               70
                0.00        0.05       0.10       0.15                           0.02 0.04 0.06 0.08                                 0.005 0.010 0.015 0.020 0.025
                             Cost per Example ($)                                   Cost per Example ($)                                   Cost per Example ($)
                                                   GPT-4o Reasoner                                 o3-mini Reasoner
                                                   GPT-4o + Majority Vote                          o3-mini + Majority Vote
                                                   GPT-4o + VerifiAgent (GPT-4o)                   o3-mini + VerifiAgent (GPT-4o)
                                                   GPT-4o + VerifiAgent (o1-mini)                  o3-mini + VerifiAgent (o1-mini)

                                  Figure 7: Visualisation of average cost versus accuracy on the three datasets.



               To determine the smallest positive integer                                         - For k = 16, it is 24 .
               n such that exactly half of the fractions k1                                       - For k = 20, it is 22 × 51 .
               for 1 ≤ k ≤ n are terminating decimals,                                            - For k = 25, it is 52 .
               we need to understand the conditions under                                         - For k = 32, it is 25 .
               which a unit fraction k1 has a terminating                                         - For k = 40, it is 23 × 51 .
               decimal representation.                                                            - For k = 50, it is 21 × 52 .
               A fraction k1 has a terminating decimal if                                         - For k = 64, it is 26 .
               and only if the denominator k in its simplest                                      - For k = 80, it is 24 × 51 .
               form (after removing common factors with                                           - For k = 100, it is 22 × 52 .
               the numerator) has only the prime factors
               2 and/or 5. Thus, k must be of the form                                             2. **Count such numbers up to n:**
               2a × 5b for non-negative integers a and b.                                          We need to find n such that there are n2 such
               Now, let’s find the smallest n such that half                                       numbers. Notice the sequence of numbers
               of the numbers 1, 2, . . . , n are of this form.                                    where k can be expressed as 2a × 5b .
               1.     **Analyze numbers of the form
               2 × 5b :**
                 a
                                                                                                   Checking for small values of n:
               - For k = 1, it is 20 × 50 .                                                       - When n = 1, there is 1 number that gives
               - For k = 2, it is 21 .                                                             a terminating decimal.
               - For k = 4, it is 22 .                                                            - When n = 2, there are 2 numbers (1, 2).
               - For k = 5, it is 51 .                                                            - When n = 4, there are 3 numbers (1, 2, 4).
               - For k = 8, it is 23 .                                                            - When n = 5, there are 4 numbers (1, 2, 4,
               - For k = 10, it is 21 × 51 .                                                       5).



                                                                                           13
- When n = 8, there are 5 numbers (1, 2, 4,
5, 8).                                             decimal: k must be of the form
- When n = 10, there are 6 numbers (1, 2,          2a × 5b .
4, 5, 8, 10).                                      - Step 2: List numbers of the form
- When n = 12, it still remains 6.                 2a × 5b up to a certain n.
- When n = 16, there are 7 numbers (1, 2,          - Step 3: Count such numbers for
4, 5, 8, 10, 16).                                  increasing values of n and check
- When n = 20, there are 8 numbers (1, 2,          when they equal n2 .
4, 5, 8, 10, 16, 20).                              - Step 4: Verify that for n = 10,
                                                   there are 6 numbers (1, 2, 4, 5, 8,
We need to verify when these numbers               10) that are of the form 2a × 5b ,
equal n2 . For this to hold:                       which is half of 10.
                                                   - Step 5: Conclude that the smallest
- Let’s check n = 10, where the numbers            n is 10.
1, 2, 4, 5, 8, 10 are exactly half of the
numbers from 1 to 10.                              3. Analyze the divided answer to
                                                   determine if it contains a clear result
Thus, the smallest n such that exactly half        or conclusion to the question.
of the fractions k1 for 1 ≤ k ≤ n have             - The last step provides a clear
terminating decimals is 10 .                       conclusion: the smallest n is 10.

VerfiAgent Output:                                 4. Check whether each step logically
                                                   follows from the previous one, ex-
                                                   plaining any logical errors if they ex-
   To verify the correctness of the
                                                   ist.
   given answer, let’s perform a meta
                                                   - Each step logically follows from
   verification first.
                                                   the previous one. The reasoning is
                                                   consistent and correctly applies the
   1. List all the known conditions
                                                   condition for terminating decimals.
   and final objective provided in the
   problem.
   - Conditions:                                   Now, let’s perform tool verification
   1) A fraction k1 has a terminating              using Python Interpreter to ensure
   decimal if and only if k in its                 the calculations are correct.
   simplest form has only the prime
   factors 2 and/or 5.                             Thought: I will use Python Inter-
   2) We need to find the smallest posi-           preter to find the correct smallest n
   tive integer n such that exactly half           where the count of numbers of the
   of the fractions k1 for 1 ≤ k ≤ n are           form 2a × 5b is exactly half of n.
   terminating decimals.
   - Objective: Find the smallest n                Action: Use Python Interpreter
   such that half of the fractions k1 for
   1 ≤ k ≤ n are terminating decimals.             def solver():
                                                       def is_terminating(k):
   2. Divide the answer into individual                    while k % 2 == 0:
   and explicit logical steps.                                 k //= 2
   - Step 1: Identify the condition for a                  while k % 5 == 0:
   fraction k1 to have a terminating                           k //= 5
                                                           return k == 1




                                              14
                                             An Example VerifiAgent Trajectory on
     n = 1                                   StrategyQA Dataset
     while True:
                                             Question:
        terminating_count = sum(
                                             Will more people go in and out of Taco Bell
                1
                                             than a Roy Rogers each year? Answer the
           for k in range(1, n + 1)
                                             question with True or False.
           if is_terminating(k)
            )
                                             GPT-4o Solution:
        if terminating_count == n//2:
                                             To determine whether more people go in
            return n
                                             and out of Taco Bell than a Roy Rogers
        n += 1
                                             each year, we need to consider several
                                             factors, including the number of locations,
ans = solver()
                                             brand popularity, and customer traffic.
The program will find the smallest
n where the count of terminating             1. **Number of Locations**:
decimals is exactly half of n. Let’s         - Taco Bell is a major fast-food chain with a
see the result.                               large number of locations worldwide. As
                                              of recent data, Taco Bell has over 7,000
Observation: [12]                             locations primarily in the United States.
                                             - Roy Rogers, on the other hand, is a smaller
Thought: The tool verification result         chain with significantly fewer locations.
indicates that the smallest positive         As of recent data, Roy Rogers has around
integer n such that exactly half of           50 locations, mostly concentrated in the
the fractions k1 for 1 ≤ k ≤ n are            Mid-Atlantic region of the United States.
terminating decimals is actually 12,
not 10 as initially stated in the an-         2. **Brand Popularity and Customer
swer. Based on the tool verification,        Traffic**:
the original answer is incorrect. The        - Taco Bell is a well-known brand with a
correct smallest n is 12.                     strong presence in the fast-food industry. It
                                              is part of Yum! Brands, which also owns
Action: Evaluate[Incorrect]                   KFC and Pizza Hut. Taco Bell is known for
Summarisation:                                its Mexican-inspired menu and has a large
Evaluation Result: Incorrect                  customer base.
Error Reason: Step 4 contains                - Roy Rogers is a smaller chain with a more
the error. The original answer                limited customer base. It is known for its
incorrectly treated 6 as half of 10,          burgers, roast beef sandwiches, and fried
which led to prematurely stopping             chicken, but it does not have the same level
at n = 10.                                    of brand recognition or customer traffic as
Revision Method: Systematically              Taco Bell.
check the count of numbers of
the form 2a × 5b for each n until            3. **Conclusion**:
the count equals n2 , which shows            - Given the significantly larger number of
n = 12 is the correct solution               Taco Bell locations and its widespread
instead of n = 10.                           popularity, it is reasonable to conclude that
                                             more people visit Taco Bell locations than
Observation: [Done]                          Roy Rogers locations each year.

Vscore : 0.8241994820658969                  Based on this reasoning, the answer is:
                                             Answer: True.




                                        15
VerifiAgent Output:
                                                  exist.
   To verify the correctness of the              - Step 1 logically follows from the
   answer, let’s perform a meta verifi-           conditions about the number of loca-
   cation first.                                  tions.
                                                 - Step 2 logically follows from the
  1. List all the known conditions                conditions about brand popularity
  and final objective provided in the             and customer traffic.
  problem.                                       - Step 3 logically follows from Steps
  - Conditions:                                  1 and 2, concluding that more people
  1) Taco Bell has over 7,000 locations          visit Taco Bell.
  primarily in the United States.                - Step 4 provides a clear answer
  2) Roy Rogers has around 50                     based on the conclusion in Step 3.
  locations, mostly concentrated
  in the Mid-Atlantic region of the              The meta verification indicates that
  United States.                                 the answer is complete and logically
  3) Taco Bell is a well-known                   consistent. However, to ensure the
  brand with a strong presence in the            accuracy of the factual information
  fast-food industry.                            regarding the number of locations
  4) Roy Rogers is a smaller chain               and brand popularity, I will use
  with a more limited customer base.             the Online Search Engine to verify
  - Objective: Determine if more                 these details.
  people go in and out of Taco Bell
  than a Roy Rogers each year.                   Thought: I will verify the number
                                                 of locations and brand popularity of
   2. Divide the answer into individual          Taco Bell and Roy Rogers to ensure
   and explicit logical steps.                   the factual accuracy of the answer.
  - Step 1: Compare the number of
   locations of Taco Bell and Roy                Action: Use Search Engine[Number
   Rogers.                                       of Taco Bell locations 2023]
  - Step 2: Compare the brand popu-
   larity and customer traffic of Taco           Observation: [As of 2023, Taco
   Bell and Roy Rogers.                          Bell operates approximately 8,200
  - Step 3: Conclude that more people            locations globally. In the United
  visit Taco Bell locations than Roy             States alone, there are more than
   Rogers locations each year. - Step 4:         7,980 Taco Bell restaurants. The
  Answer: True.                                  company has plans for significant
                                                 expansion, aiming to increase its
  3. Analyze the divided answer to               total number of locations to 10,000
  determine if it contains a clear result        in the coming years, with a focus on
  or conclusion to the question.                 growing its international presence
  - The last independent step contains           from 1,150 to 3,000 restaurants
  the answer “True”, which is a clear            outside the U.S. over the next five
  result to the question.                        years [2][4][5].]

   4. Check whether each step logically          Thought: The information obtained
   follows from the previous one, ex-            from the search engine confirms that
   plaining any logical errors if they           Taco Bell has a significantly larger




                                            16
                                              An Example VerifiAgent Trajectory on
number of locations than initially            ProverQA Dataset
stated in the answer, with over 7,980
                                              Context:
locations in the United States alone.
                                              Raul either ignored warning signs or lis-
This further supports the conclusion
                                              tened to his body. Raul did not ignore warn-
that more people visit Taco Bell than
                                              ing signs.
Roy Rogers each year. Now, I will
                                              Question:
verify the number of Roy Rogers
                                              Based on the above information, is the fol-
locations to ensure the accuracy of
                                              lowing statement true, false, or uncertain?
the comparison.
                                              Raul got proper medical attention when
                                              needed.
Action: Use Search Engine[Number
                                              Options: [‘A) True’, ‘B) False’, ‘C)
of Roy Rogers locations 2023]
                                              Uncertain’]
Observation: [As of 2023, there are
                                              GPT-4o Solution:
over 50 Roy Rogers restaurant loca-
                                              Based on the context provided, Raul either
tions. This reflects a resurgence in
                                              ignored warning signs or listened to his
interest and investment in the brand
                                              body. Since it is stated that Raul did not
following a decline in the number
                                              ignore warning signs, it implies that he
of locations in previous years due to
                                              listened to his body. Listening to one’s
conversions and closures [2].]
                                              body typically suggests being attentive to
                                              health needs, which often leads to seeking
Thought: The information obtained
                                              proper medical attention when necessary.
from the search engine confirms that
Roy Rogers has over 50 locations,
                                              Therefore, the statement “Raul got proper
which aligns with the data provided
                                              medical attention when needed” is likely
in the answer. This supports the con-
                                              true.
clusion that Taco Bell, with its sig-
                                              Answer: A) True
nificantly larger number of locations,
likely has more customer traffic than
                                              VerifiAgent Output:
Roy Rogers. Since both the num-
ber of locations and brand popular-
                                                 Meta Verification:
ity have been verified and support
the conclusion, I will proceed to the
                                                 1. List all the known conditions
final evaluation.
                                                 and final objective provided in the
                                                 problem.
Action: Evaluate[Correct]                        - Conditions: [Raul either ignored
Summarisation:                                   warning signs or listened to his
Evaluation Result: Correct                       body, Raul did not ignore warning
Error Reason: None                               signs]
Revision Method: None                            - Objective: [Determine if the
                                                 statement “Raul got proper medical
Observation: [Done]                              attention when needed” is true, false,
                                                 or uncertain]
Vscore : 0.941521122813535




                                         17
 2. Divide the answer into individual           the correctness of the assumption
 and explicit logical steps.                    made in Step 4, I will use the Z3
- Step 1: Raul either ignored warning           Theorem Prover to verify the logical
 signs or listened to his body.                 reasoning.
- Step 2: Raul did not ignore warning
 signs.                                         Thought: I will use the Z3 The-
- Step 3: Therefore, Raul listened to           orem Prover to verify the logical
 his body.                                      reasoning that listening to one’s
- Step 4: Listening to one’s body               body implies getting proper medical
 typically suggests being attentive             attention when needed.
 to health needs, which often leads
 to seeking proper medical attention            Action: Use Theorem Prover
when necessary.                                 import z3
- Step 5: Therefore, the statement              from z3 import *
 "Raul got proper medical attention
when needed" is likely true.                    def check_model(solver):
- Final Answer: A) True                             res = solver.check()
 3. Analyze the divided answer to                   if res == sat:
 determine if it contains a clear result                return 'sat'
 or conclusion to the question.                     elif res == unsat:
- The last independent step contains                    return 'unsat'
 the answer “A) True”, which is a                   else:
 clear result to the question.                          return 'unsolvable'

4. Check whether each step logically            def check_constraint(solver, c):
follows from the previous one, ex-                  pos_res = solver.check(c)
plaining any logical errors if they ex-            neg_res = solver.check(Not(c))
ist.
- Step 1 to Step 2: The transition                  if (pos_res == sat) and
is logical as it uses the given condi-              (neg_res == unsat):
tion that Raul did not ignore warning                    return 'Agree'
signs.                                             elif (pos_res == unsat) and
- Step 2 to Step 3: The transition is               (neg_res == sat):
logical as it concludes that Raul lis-                   return 'Contradict'
tened to his body based on the given               elif (pos_res == unknown) or
conditions.                                         (neg_res == unknown):
- Step 3 to Step 4: The transition                       return 'unsolvable'
is logical as it makes a reasonable                 else:
assumption that listening to one’s                       return 'Uncertain'
body suggests attentiveness to health
needs.                                          def main():
- Step 4 to Step 5: The transition is               s = z3.Solver()
logical as it concludes that being at-              # Define the variables
tentive to health needs often leads to             ignored_warning_signs = Bool
seeking proper medical attention.                   ('ignored_warning_signs')
                                                    listened_to_body = Bool
The answer is complete and logically                ('listened_to_body')
consistent. However, to ensure                      got_med_attention = Bool
                                                    ('got_med_attention')



                                           18
    # Define the conditions                        Vscore : 0.6459490712193161
   s.add(Or(ignored_warning_signs,
    listened_to_body))
   s.add(Not(ignored_warning_signs)) F          VerifiAgent Prompt
    # Define the implication                   VerifiAgent System Prompt
    implication = Implies
(listened_to_body, got_med_attention)          You are an expert in evaluating the correct-
                                               ness of answers to reasoning problems,
   # Check if the implication is               including mathematical reasoning, com-
   consistent with conditions                  monsense reasoning and logical reasoning.
   return check_constraint(s,                  Your unique strength lies in your ability to
     implication)                              utilise specialised tools to verify answers
                                               effectively. You will be provided with a
ans = main()                                   reasoning question and a potential answer.
                                               Your task is to verify the correctness of
Observation: [Uncertain]
                                               the answer using the following tools. You
                                               should select appropriate tools for different
Thought: The tool verification result
                                               reasoning problems as needed.
is “Uncertain”, which means that the
logical implication that listening to
                                               Before you perform tool verification, you
one’s body leads to getting proper
                                               should first do a meta verification without
medical attention is not definitively
                                               tool that verifies (1) the completeness of
supported by the given conditions.
                                               the answer (2) the logical consistency of
This suggests that the assumption
                                               the answer. Your final decision should be
made in Step 4 of the solution may
                                               based on the meta verification and tool
not be entirely reliable. Therefore, I
                                               verification results.
will reflect on both the meta verifi-
cation and tool verification results to
                                               Definition:
make a final decision.
                                               - Completeness refers to an answer that is
                                               self-contained, fully addresses every part of
Action: Evaluate[Incorrect]                    the question, and contains a clear result or
Summarisation:                                 conclusion.
Evaluation Result: Incorrect                   - Logical consistency refers to reasoning
Error Reason: Step 4 contains the              that follows a logical structure with no
error. The assumption that listening           jumps, gaps, or inconsistencies.
to one’s body typically leads to
seeking proper medical attention               Meta Verification Steps:
is not definitively supported by the           1. List all the known conditions and the
given conditions, as indicated by the          final objective provided in the problem.
tool verification result.                      • Put the known conditions in the format of
Revision Method: To avoid making               ‘Conditions: [condition1, condition2, ...]’
the error again, the reasoning should          • Put the final objective in the format of
not assume that listening to one’s             ‘Objective: [Objective]’
body directly implies getting proper           2. Divide the answer into individual and
medical attention without additional           explicit logical steps.
supporting information.                        • Put the individual steps in the format of
                                               ‘Step 1: [step 1] Step 2: [step 2]...’
Observation: [Done]                            • Put the final answer in the last independent
                                               step.


                                          19
3. Analyse the divided answer to determine            ans = solver()
if it contains a clear result or conclusion to
the question.                                         **Online Search Engine**
• You should check whether the last                   Online Search Engine is best suited for
independent step contains an answer.                  verifying answers to factual or knowledge-
• If the answer is not complete, there is no          based reasoning problems. By querying the
need to check the logical consistency.                search engine, you can retrieve authoritative
4. Check whether each step logically                  results that serve as ground-truth references
follows from the previous one, explaining             to verify the given answer.
any logical errors if they exist.
• You should analyse the reasoning flow               Instructions for using Online Search
one by one, from Step 1 to Step 2, from               Engine:
Step 2 to Step 3, ...                                 1. Understand the problem and identify
• Based on the reasoning flow, check                  any areas where additional information is
whether every step move is reasonable and             needed to verify the answer.
logically correct.                                    2. Generate specific questions that will help
                                                      you gather the necessary information.
Below are the introduction and guidelines             3. Your questions should be clear, concise,
for three tools you can use:                          and directly related to verifying the original
                                                      answer.
**Python Interpreter**                                4. You can use a search engine multiple
Python Interpreter is ideal for verifying             times, but you should only generate one
answers to mathematical reasoning prob-               question per time.
lems involving calculations or numerical
analysis. By executing Python programs,               Question Template:
you can obtain precise results and compare            Question
them against the provided answer.
                                                      **Z3 Theorem Prover**
Instructions for using Python Interpreter:            Z3 Theorem Prover excels at solving
                                                      logical reasoning problems that require
1. Understand the problem and think about             deductive, inductive, or abductive reason-
how you would solve the problem using                 ing. It allows you to represent problems
Python programs.                                      in first-order logic (FOL), comprising
2. Write a Python program to solve the                constants, predicates, logic variables,
problem using appropriate variables and               quantifiers, functions, operators, grounded
functions.                                            facts, and logic formulas. Using the Z3
3. Ensure the code is clean and executable,           library, you can perform formal reasoning
but do not include any extra output.                  to determine the validity of the answer.
4. The program must start with ‘def
solver():’ and end with ‘ans = solver()’.             Instructions for using Z3 Theorem Prover:
                                                      1. Understand the Logical Reasoning types:
Python Program Template:                              - Deductive reasoning: Given Facts and
def solver():                                         Logic Formulas, deduce new Facts from
  # Let's write a Python program to                   the system by applying the Formulas to the
  solve the problem using appropriate                 Facts.
  # variables and functions, and then                 - Inductive reasoning: Given Facts and
   return the answer.                                 potentially some Formulas, induce new
   # Firstly, we need to define the                   Formulas that entail the given Facts and are
   following variable:                                consistent with the preexisting Formulas.
                                                      - Abductive reasoning: Given Facts, Logic



                                                 20
Formulas, and a consequence Fact, infer                  if (pos_res == sat) and
the missing Facts or Formulas, such that                 (neg_res == unsat):
the consequence Fact can be entailed by the                  return 'Agree'
system.                                                  elif (pos_res == unsat) and
2. Note that the type of reasoning and the               (neg_res == sat):
system built for the problem determine:                      return 'Contradict'
- How the output is interpreted.                         elif (pos_res == unknown) or
- Whether the output serves as the final                 (neg_res == unknown):
answer or intermediate checks for the                        return 'unsolvable'
problem-specific answer.                                 else:
- For example:                                               return 'Uncertain'
for a deductive reasoning task with a
given hypothesis, one builds the system to          def main():
determine if the hypothesis Agree/Contra-               s = z3.Solver()
dict/Uncertain to the system;                           # Your code here
for a deductive reasoning task where one
wants to deduce all possible Facts, then one        ans = main()
should infer all Facts that Agree with the
system;                                              Important:
for inductive reasoning, one infers the             1. For each time of tool call, you will
Formulas that Agree with the system;                 receive a response based on your request
for abductive reasoning, one infers the              and you should use tool response to
Facts or Formulas that Agree with the                evaluate the potential answer.
consequence and the system.                         - The program will return the program
3. Write a Python program with Z3 lib                execution result.
to solve the problem using appropriate              - The search engine will return the obtained
variables and functions.                             result from the Internet.
4. Ensure the code is clean and executable,          2. This is an iterative process, you can
but do not include any extra output.                 repeat the process of using tools until
5. You should use the following code                you have sufficient information to make a
template to solve the problem and end with           confident verification of the answer.
‘ans = main()’.                                      3. Once you think you have enough
                                                     information to verify the answer, provide a
Z3 Program Template:                                 Final Evaluation of the original answer.
import z3                                           - Based on the meta verification and tool
from z3 import *                                    verification, make your final decision.
                                                    - State whether the answer is Correct or
def check_model(solver):                             Incorrect based on your analysis.
    res = solver.check()                            - Provide a clear and concise explanation
    if res == sat:                                   for your assessment, referencing the
        return 'sat'                                 information gathered.
    elif res == unsat:                              4. The tool verification is to help you
        return 'unsat'                               further verify your meta verification result,
    else:                                            so you cannot skip tool verification process.
        return 'unsolvable'                         - If tool verification result disagrees with
                                                     meta verification result, you should reflect
def check_constraint(solver, c):                     on both verification processes and decide
    pos_res = solver.check(c)                       which one you will trust.
    neg_res = solver.check(Not(c))
                                                    You should strictly follow the following re-



                                               21
sponse format and only generate responses
in this way:

If you want to use Python Interpreter:
Thought: [The reason why you choose to
take this action.]
Action: Use Python Interpreter[your
Python Program]

If you want to use Online Search Engine:
Thought: [The reason why you choose to
take this action.]
Action: Use Search Engine[your Question]

If you want to use Z3 Theorem Prover:
Thought: [The reason why you choose to
take this action.]
Action: Use Theorem Prover[your Z3
Program]

 If you want to generate Final Evaluation
 result:
Thought: [The reason why you choose to
 take this action.]
Action: Evaluate[Correct/Incorrect]
 Summarisation:
 Evaluation Result: [Correct/Incorrect]
 Error Reason: [Only generate the error
 reason when the evaluation is ‘Incorrect’,
 otherwise generate ‘None’. The reason
 should first indicate which step in the
 solution contains the error and then explain
why the error occurred.]
 Revision Method: [Only generate the
 revision method when the evaluation is
‘Incorrect’, otherwise generate ‘None’. The
 revision method should be summarised
 from the tool verification result to avoid
 making the error again.]




                                                22
