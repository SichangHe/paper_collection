                                         P SYCHOMETRIC -BASED E VALUATION FOR T HEOREM P ROVING
                                                    WITH L ARGE L ANGUAGE M ODELS



                                             Jianyu Zhang1 , Yongwang Zhao2,* , Long Zhang3 , Jilin Hu2 , Xiaokun Luan4 , Zhiwei Xu2 , Feng Yang3
                                                 1
                                                   University of Electronic Science and Technology of China, 202222060304@std.uestc.edu.cn
                                                                                        2
                                                                                          Zhejiang University
                                                                                   3
                                                                                     Academy of Military Sciences
arXiv:2502.00855v1 [cs.AI] 2 Feb 2025




                                                                                          4
                                                                                            Peking University
                                                                        *Corresponding author: zhaoyw@zju.edu.cn




                                                                                            A BSTRACT
                                                 Large language models (LLMs) for formal theorem proving have become a prominent research
                                                 focus. At present, the proving ability of these LLMs is mainly evaluated through proof pass rates
                                                 on datasets such as miniF2F. However, this evaluation method overlooks the varying importance
                                                 of theorems. As a result, it fails to highlight the real performance disparities between LLMs and
                                                 leads to high evaluation costs. This study proposes a psychometric-based evaluation method for
                                                 theorem proving with LLMs, comprising two main components: Dataset Annotation and Adaptive
                                                 Evaluation. First, we propose a metric calculation method to annotate the dataset with difficulty and
                                                 discrimination metrics. Specifically, we annotate each theorem in the miniF2F dataset and grade
                                                 them into varying difficulty levels according to the performance of LLMs, resulting in an enhanced
                                                 dataset: miniF2F-Graded. Experimental results show that the difficulty grading in miniF2F-Graded
                                                 better reflects the theorem difficulty perceived by LLMs. Secondly, we design an adaptive evaluation
                                                 method to dynamically select the most suitable theorems for testing based on the annotated metrics
                                                 and the real-time performance of LLMs. We apply this method to evaluate 10 LLMs. The results
                                                 show that our method finely highlights the performance disparities between LLMs. It also reduces
                                                 evaluation costs by using only 23% of the theorems in the dataset.

                                        Keywords Theorem Proving with LLMs, Adaptive Evaluation, Dataset Annotation, Psychometrics

                                        1   Introduction
                                        The rapid development of large language models (LLMs) has led to the creation of specialized models across various
                                        fields [1, 2]. One area that has garnered significant attention is theorem proving in formal methods. The application
                                        of theorem proving is widespread, especially in mathematical research and in verifying the correctness and security
                                        of safety-critical systems. However, theorem proving remains a complex and labor-intensive task, often requiring
                                        substantial effort from experts to complete [3, 4]. The advent of LLMs has made automated theorem proving feasible.
                                        Pre-trained LLMs can now assist developers in rapidly completing complex proof tasks, such as DeepSeek-Prover [5]
                                        and LEGO-Prover [6].
                                        In automated theorem proving, evaluating the theorem-proving ability of LLMs is a crucial task, as accurate evaluation
                                        standards are essential to guide the continuous improvement of LLM training methods [7, 3]. Currently, the mainstream
                                        evaluation method is testing the proportion of theorems successfully proven by the model within N attempts (P ass@N ).
                                        While this evaluation method is intuitive, it faces several challenges:

                                              • The evaluation results fail to highlight the disparities in theorem-proving abilities between LLMs, as the pass
                                                rate overlooks the varying importance of theorems and assigns equal weight to both difficult and simple ones.
                                                For instance, DeepSeek-prover-RL introduced several meaningful improvements over DeepSeek-Prover-SFT
                                                but only achieved a slight increase in P ass@128 [5], suggesting that the evaluation results lack a fine-grained
                                                distinction.
Running Title for Header


         • Evaluation incurs high computational costs, as it does not filter the test theorems and requires testing all the
           theorems in the dataset. For example, testing the P ass@128 score of a 7B-metric model on 488 theorems in
           our experiment took 39.3 hours on a single A100 GPU. For larger models or datasets, the computational cost
           would increase even further.




Figure 1: The method consists of two parts. In Part 1: Dataset Annotation, difficulty and discrimination metrics are
assigned to each theorem in the miniF2F dataset based on the performance of LLMs, as determined by the Metric
Calculation process, resulting in an annotated dataset, miniF2F-Graded. In Part 2: Adaptive Evaluation, the most
suitable theorems are dynamically selected for testing based on their annotated metrics in miniF2F-Graded and the
initial or current ability scores of LLMs, following the Theorem Selection Algorithm. Throughout the iterative testing
process, ability scores are continuously updated under the Adaptive Test Algorithm until they converge, with the final
stabilized scores serving as the evaluation results.

To address these issues, this study draws on concepts from psychometrics: adaptive evaluation based on the model’s
real-time performance, rather than relying on a fixed test set. We propose a psychometric-based evaluation method
for theorem proving with LLMs. This method annotates each theorem with difficulty (the ability level required for
an LLM to prove it) and discrimination (how well the theorem distinguishes LLMs of varying abilities). Based on
these annotations, the method dynamically selects the most suitable theorems to efficiently evaluate the LLM’s proving
ability. The overview of this method is shown in 1, consisting of two parts: Dataset Annotation (3.1) and Adaptive
Evaluation (3.2).
In summary, the core contributions of this study are as follows:
         • This study proposes a psychometric-based evaluation method for theorem proving with LLMs, which evaluates
           the LLM’s proving ability through dataset annotation and adaptive evaluation, enabling a more fine-grained
           and efficient assessment. To the best of our knowledge, this is the first study to combine psychometrics with
           the evaluation of LLMs’ theorem-proving ability. Specifically, this study designs a metric calculation method,
           a theorem selection algorithm, and an adaptive test algorithm, all tailored to the characteristics of LLMs in the
           context of theorem proving.
         • Building on the widely used formal theorem dataset miniF2F, we propose an enhanced version with metric
           annotations and difficulty grading: miniF2F-Graded1 . Experimental results indicate that, compared to the
           previous manual grading method, miniF2F-Graded more accurately reflects the difficulty of the theorems as
   1
       The miniF2F-Graded dataset is available at https://zenodo.org/records/14776138.


                                                              2
Running Title for Header


         perceived by LLMs. Additionally, this paper analyzes the distribution of metrics across the different categories
         of theorems in miniF2F, providing valuable guidance for future researchers in theorem proving, training, and
         evaluation.

       • We apply our adaptive evaluation method and the miniF2F-Graded dataset to evaluate the performance of 10
         open-source LLMs with theorem-proving abilities. The results demonstrate that our method finely distinguishes
         performance disparities between LLMs. Moreover, it uses only 23% of the theorems in the dataset, thereby
         reducing the evaluation cost.

The structure of this paper is as follows: 2 reviews related work. 3 introduces our method, including dataset annotation
and adaptive evaluation. 4 presents experiments verifying the effectiveness of our method. 5 offers a detailed analysis
of the experimental results. Finally, 6 concludes the paper with a summary and directions for future work.


2   Related Work

This study proposes a psychometric-based evaluation method for theorem proving with LLMs. Our research builds on
existing literature in Theorem Proving with LLMs, LLM evaluation methods, and psychometrics.
Theorem Proving with LLMs. In recent years, a growing number of studies have explored training LLMs for theorem
proving [3]. These works have developed models capable of generating proofs in formal languages such as Lean [8],
Isabelle [9], and Coq [10]. Based on proof generation strategies, existing methods can be broadly categorized into tree
search methods and whole-proof generation methods. Tree search methods formulate the proof process as a search
problem, incrementally exploring potential proof paths within a search tree. Notable approaches include LeanDojo
[11], Thor [12], LEGO [6], DSP [13], among others. In contrast, whole-proof generation methods treat the proof as
a complete sequence, generating the entire proof path in a single step. Representative works in this category include
Baldur [14], DeepSeek [5], TheoremLlama [15], and MetaMath-Llemma [16]. Among them, DeepSeek-Prover-V1.5
leverages an enhanced formal theorem proving dataset for supervised fine-tuning, achieving a 60.2% pass rate on the
miniF2F test set using a single-pass full-proof generation approach [5].
In this study, we focus on evaluating whole-proof generation models, as their evaluation should adhere to consistent
criteria. In contrast, tree search methods, due to their distinct search strategies, face challenges in establishing uniform
evaluation standards.
LLM Evaluation Methods. Evaluating the capabilities of large language models remains a critical challenge. In
the field of Theorem Proving with LLMs, proof pass rate is widely regarded as the primary evaluation criterion [7].
However, an increasing number of studies advocate for more comprehensive evaluation methods. For instance, [17, 18]
propose Chain-of-Thought (CoT) evaluation strategies, which assess LLM performance at each critical reasoning
step rather than relying solely on the final answer. [19, 20, 21] highlight the importance of analyzing errors in the
reasoning process to gain deeper insights into the common mistakes made by LLMs. [7, 22] explore evaluation methods
based on perturbation analysis, examining how LLMs respond to variations in input. Lastly, [23] suggest categorizing
and annotating evaluation data based on the number of reasoning steps and question types, enabling a more detailed
assessment of LLM performance across different data types.
[24] explores the use of human psychometrics in LLM evaluation and proposes that adaptive evaluation, which adjusts
to a model’s performance rather than relying on fixed test sets, will become the new standard in AI model assessment.
This concept serves as an important reference for our study. Specific applications of adaptive evaluation in LLM
assessment can be found in works such as [25, 26], which achieve efficient evaluation with fewer examples. This study
aims to investigate how adaptive evaluation methods can be applied to evaluating the theorem-proving abilities of
LLMs.
Psychometrics. Psychometrics is a field dedicated to the effective measurement of psychological traits. In exam
assessments, it provides the scientific foundation and methodological tools for designing, analyzing, and interpreting
exam results, ensuring that assessments accurately and reliably measure the true abilities of students or test subjects
[27, 28, 29]. Item Response Theory (IRT), introduced by [30], models both the characteristics of individual test items
(e.g., difficulty, discrimination) and the ability scores of test subjects, offering a more precise measurement framework.
IRT remains one of the most influential theoretical models in psychometrics [31]. Building on IRT’s approach to
modeling item difficulty and discrimination, this study develops a metric calculation method and an adaptive test
algorithm specifically designed to address the limited number of test subjects (LLMs) in theorem proving, achieving
promising results.


                                                             3
Running Title for Header


3     Method

3.1     Dataset Annotation

3.1.1    miniF2F dataset

This study uses the MiniF2F dataset [32] as the basis for annotation. The MiniF2F dataset is one of the most widely
used datasets in the field, with many LLMs evaluating their performance based on the pass rate achieved on MiniF2F
[6, 33]. A more detailed introduction of the MiniF2F dataset can be found in the A.1.
Theorems in the MiniF2F dataset are formalized using a range of languages, including Metamath, Lean, Isabelle, and
HOL Light. The difficulty of proving the same theorem can vary depending on the formal language used. For instance,
a typical proof in Lean is significantly shorter than its counterpart in Metamath, as Lean offers many powerful tactics
that aid in formalization [32]. As a result, many studies opt to use Lean data for training and evaluation. To ensure
the comparability of evaluation results, this study focuses on evaluating theorems in MiniF2F that are formalized in
Lean. The dataset in [34] updates the theorems from miniF2F to a newer version of Lean and includes natural language
descriptions. Therefore, we use this version of miniF2F for annotation and evaluation.
In the MiniF2F paper [32], it is noted that 260 theorems in the dataset are derived from the MATH dataset [35], with
the theorems in MATH being classified into five difficulty levels. However, this grading was done manually by humans.
We believe that the perceptions of difficulty between humans and LLMs may differ, as confirmed by the results in 3.
Therefore, in this study, we re-annotate each theorem’s difficulty and discrimination, categorizing them into difficulty
levels.

3.1.2    Metric Calculation

This study argues that there is a similarity between LLM test sets and human exam questions: not all questions hold
equal importance [24]. For instance, an LLM should receive higher scores for solving high-difficulty theorems than
for solving low-difficulty ones. Furthermore, for an LLM that has already proven several relatively difficult theorems,
testing a high-difficulty theorem is more valuable than testing a simpler one.
To fully exploit the differences between the theorems, this study uses the miniF2F dataset as an example and calculates
the difficulty and discrimination of each theorem based on the performance of multiple LLMs (four Annotation LLMs
were selected, as described in 4.1).
In Item Response Theory from psychometrics [31, 36], metrics like difficulty and discrimination are typically estimated
through statistical models. A detailed explanation of the statistical modeling methods can be found in the B.1. By
applying the statistical modeling methods from IRT and the theorem-proving results from LLMs, we estimated the
difficulty and discrimination metrics for the theorems. However, the results were suboptimal, with the estimated metric
distributions being too concentrated. The suboptimal results stem from the limited number of test subjects, as we used
only four LLMs, far fewer than the number of examinees in human exams used in IRT models. However, it is currently
impossible to find the same number of open-source LLMs as human test-takers.
To address the issue of insufficient test subjects, this study developed a metric calculation method that does not rely
on metric estimation, instead using a more direct formula to compute the difficulty and discrimination metrics for the
theorems.
Notations and Definitions To accurately calculate the difficulty and discrimination metrics, we need to know the
prior ability values of the models. We use the pass rate across the entire dataset (P ass@128) to represent the prior
ability values of the models. The models used for annotation are denoted as M1 , M2 , M3 , M4 , with their relative prior
ability values ranked as: θ(M1 ) < θ(M2 ) < θ(M3 ) < θ(M4 ). We also compute the attempt success rate for each
theorem across the four models. The attempt success rate is defined as the number of successful proof attempts divided
by the total number of attempts, with each model making 128 attempts. The attempt success rates for the 4 models
on theorem x are represented as PM1 (x), PM2 (x), PM3 (x), and PM4 (x), and P (x) is their average, representing the
overall attempt success rate for theorem x. Finally, we use Dif f iculty(x) and Discrimination(x) to denote the
difficulty and discrimination metrics for theorem x.
Difficulty Calculation. To calculate the difficulty more precisely, we designed a new formula that incorporates a
correction term into P (x), as shown in 1. We subtract from P (x) the value of each model that has successfully proven
the theorem, divided by its prior ability score, and multiply the correction term by a weight ϵ (0.005). This approach
aims to highlight the difficulty differences between the theorems. The more models that successfully prove the theorem,
and the lower the ability of those models, the more it suggests that the theorem’s difficulty should be lowered. We also


                                                           4
Running Title for Header


experimented without the correction term, and the results are provided in the B.2. The findings indicate that including
the correction term makes it easier to distinguish between the difficulty levels of the theorems.

                                                              4
                                                              X                      1
                                      P ′ (x) = P (x) − ϵ ·         1PMi (x)>0 ·          .                              (1)
                                                              i=1
                                                                                   θ(Mi )

We then use 2 to calculate the difficulty for each theorem. Instead of directly using the attempt success rate, we
employ a reciprocal relationship derived from logistic regression. This approach more effectively captures the nonlinear
relationship between the success rate and difficulty. The rationale behind this is that P ′ (x) exhibits smaller changes near
0 and 1, even though the actual difficulty may differ significantly. For example, the difference between P ′ (x) = 0.01
and P ′ (x) = 0.1 may be more substantial than the difference between P ′ (x) = 0.6 and P ′ (x) = 0.7. By amplifying
the differences near 0 and 1, 2 highlights variations in the marginal intervals. This mapping enables a clearer distinction
between high- and low-difficulty theorems by better separating items with low and high success rates.

                                                                        P ′ (x)
                                             Dif f iculty(x) = −                  .                                      (2)
                                                                      1 − P ′ (x)

Discrimination Calculation. We use 3 to calculate the discrimination for each theorem. P represents the set of all
possible pairs of model combinations, which consists of 6 pairs.

                                                           1 X Pi (x) − Pj (x)
                                 Discrimination(x) =
                                                           6    θ(i) − θ(j)                                              (3)
                                                              (i,j)∈P

                                 where P = {(i, j) | i, j ∈ {M1 , M2 , M3 , M4 }, i < j}.

Using 3, we calculate the ratio of the difference in attempt success rates to the difference in ability levels between two
models for a given theorem. If the ability difference between the two models is small but the pass rate difference is
large, it indicates that the theorem has high discrimination, effectively distinguishing between models of different ability
levels. A negative discrimination value may suggest data contamination or that a low-ability model is particularly adept
at proving the theorem, warranting further investigation. To reduce potential bias introduced by any single model, we
sum the discrimination ratios for all model pairs and take the average, yielding a more stable discrimination metric.
To facilitate subsequent information content calculations, we linearly normalize the difficulty and discrimination metrics
to the intervals [0, 1] and [−1, 1], respectively.

3.2     Adaptive Evaluation

3.2.1    Theorem Selection Algorithm
After completing the dataset annotation, a theorem selection algorithm is developed to identify the most informative
theorems for testing, based on their difficulty, discrimination, and the model’s current ability score during adaptive
evaluation. In Item Response Theory, the information of a question reflects how effectively it measures ability at a
specific ability score [36]. The greater the information, the better the question can differentiate between candidates with
varying ability scores at that level, leading to more accurate measurements.
Information is typically calculated using the Fisher information function [37]. In this study, we apply a slightly modified
version of the Fisher information function, as shown in 4. Here, P (x, θ) represents the probability of theorem x being
correctly proven by a model with ability score θ, calculated using the 5 from Item Response Theory [31]. a(x) denotes
the discrimination, while a(x)f represents a modification introduced in this study to adjust and amplify the influence of
the discrimination metric on the information, prioritizing the selection of theorems with higher discrimination. Here, f
is a hyperparameter.

                                        I(x, θ) = a(x)f · P (x, θ) · (1 − P (x, θ)).                                     (4)

The selection algorithm is outlined in C. We rank the candidate theorems in D based on their information scores,
excluding T last, which have already been selected in the previous 10 rounds of testing to prevent overfitting the ability
score by repeatedly choosing the same theorems. Finally, the top 5 theorems, T selected, are selected for this round
based on the information ranking.


                                                              5
Running Title for Header


Algorithm 1 Adaptive Test
  Input: Model M , Annotated Dataset D with metrics Discrimination : ai and Dif f iculty : bi
  Output: Ability Score θ
  θ, θprev ← 0.5, S ← 0
  while S <10 do
     Tselected ← Theorem Selection(θ, D)
     for each theorem ti ∈ Tselected do
        ri ← Proof Test(ti , M) /*Test and return the success rate of M proving ti 128 times.*/
        If 0 < ri < 0.1 Then ri ← log(ri + 1)
     end for
     for i = 1 to |Tselected | do
        P (ti , θ) ← 1+e−a1i (θ−bi )
        θ ← θ + η · ai · (ri − P (ti , θ))
     end for
     θ ← min(max(θ, θmin ), θmax )
     Convergence Check:
     If |θ − θprev | < 0.01 Then S ← S + 1
     Else S ← 0
     θprev ← θ
  end while
  Return θ


3.2.2    Adaptive Test Algorithm
In the adaptive evaluation, our goal is to obtain an ability score that accurately reflects the model’s theorem-proving
ability. To achieve this, we perform multiple rounds of testing and ability score updates, gradually converging to the
true ability score. As shown in 1, we first assign an initial ability score of 0.5. This initial score allows the model to
begin testing with theorems of moderate difficulty. Next, based on the theorem selection algorithm, we select theorems
for testing. The ability score, denoted as θ, is updated according to the model’s performance on these theorems, and
new theorems are selected for further testing using the updated ability score. This process continues until the model’s
ability score changes by less than 0.01 over 10 consecutive rounds. At this point, we consider the model’s ability score
to have converged to its true value.
In 1, we designed the ability score update rule. When the success rate on a theorem ri is greater than 0 but less than
0.1, we consider that the model’s ability to prove this theorem may be influenced by random factors. For instance,
when the model’s success rate is 0.023, meaning it succeeded in only 3 out of 128 attempts, such a small number
of successful attempts suggests a smaller score for this proof. Therefore, we apply a special transformation to these
models: ri ← log(1 + ri ). The step size for updating the ability score is controlled by the hyperparameter η.
For the two hyperparameters appearing in the algorithm of this chapter: the discrimination influence factor f in 4
and the step size adjustment factor η in 1, we selected an optimal set of parameters through tuning experiments:
[f, η] = [0.49, 0.004].


4     Experiment

4.1     Experiment Setup

In this section, we introduce two distinct sets of LLMs: Annotation LLMs, used for dataset annotation, and Evaluation
LLMs, responsible for adaptive evaluation, as described in 3. Additionally, we present the proof settings.
Annotation LLMs. When selecting the Annotation LLMs, we aimed to choose a model that could achieve the current
state-of-the-art (SOTA) level for generating complete Lean proofs. To ensure more reasonable difficulty annotations
for the theorems, we selected DeepSeek-Prover-V1.5-RL [5] as one of the Annotation LLMs. This model achieved a
P ass@128 of 58.61% on miniF2F2 (including the validation and test sets; this result and the following pass rates were
obtained through our own testing), which, to the best of our knowledge, represents the highest pass rate currently.
To achieve appropriate discrimination metrics, a sufficient gap in the proof capabilities of the Annotation LLMs is
necessary. Therefore, we selected the following LLMs: codegeex4 [38], llemma [39], TheoremLlama[40], DeepSeek-
Prover-V1.5-RL[5]. The introduction to Annotation LLMs can be found in D.1.


                                                            6
Running Title for Header


Evaluation LLMs. To validate whether our method can be applied to a broader range of models, we need to select a
set of Evaluation LLMs distinct from the Annotation LLMs. Given the limited number of open-source models with
theorem-proving capabilities, the selection process proved challenging. Nevertheless, we made efforts to identify
models with theorem-proving ability as follows: Code-Llama [41], Qwen2.5-Coder-7B [42, 43], MetaMath-Llemma-7B
[16, 39], DeepSeek-Prover-V1 [33], DeepSeek-Prover-V1.5-Base. DeepSeek-Prover-V1.5-SFT [5]. The introduction to
Evaluation LLMs can be found in D.2.
Proof Settings. When using the models mentioned above for proof generation, specific prompts must be provided. The
DeepSeek-Prover series models and TheoremLlama were designed with prompts tailored for Lean proofs [5, 40], and
we continued using these prompts in our testing. For other models, the prompts utilized are listed in D.3.
We set the maximum number of proof attempts to 128, with a maximum proof length of 2048 tokens. The generated
proofs are verified for correctness by interacting with Lean 4.13 [8].

4.2   Main Results

Dataset Annotation Results. Using the annotation models described in 4.1 and the methods outlined in 3.1, we
completed the annotation and grading of the dataset, resulting in the miniF2F-Graded dataset. The detailed results of
the annotation and grading can be found in E. We classified 488 theorems by type and created a scatter plot based on
difficulty and discrimination, as shown in 2. It can be observed that, except for some theorems in mathd_numbertheory,
which exhibit high discrimination at lower difficulty levels due to one model’s exceptional performance in this category,
other theorems show an increase in discrimination as difficulty rises. The theorems within the difficulty range of 0.4–0.6
generally demonstrate higher discrimination, but as the difficulty continues to increase, the discrimination begins to
decrease. This difficulty-discrimination distribution trend largely aligns with our understanding of test problems. For
some unusual observations in the figure, we provide a detailed analysis in E.2.




Figure 2: The scatter plot of the dataset annotation results illustrates the relationship between theorem difficulty (x-axis)
and discrimination (y-axis).

Model Evaluation Results. Based on the annotated dataset (miniF2F-Graded) and the adaptive evaluation method
described in 3.2, we evaluated six Evaluation LLMs and four Annotation LLMs. The evaluation results are presented in
1. We also present in F.1 the process of model evaluation, including the selection of theorems, the changes in ability
scores, and the evaluation results. It can be observed that the evaluation method proposed in this study significantly


                                                             7
Running Title for Header


reduces the evaluation cost for both the Annotation LLMs and Evaluation LLMs, with an average reduction of 76.13%.
While the Ability Score and P ass@128 are measured in different units and have numerical differences, their rankings
are largely the same. Further analysis of the authenticity of the evaluation results is discussed in 5.2.

Table 1: Model evaluation results. The table summarizes our evaluation outcomes: Ability Score. P ass@128 is
included solely for comparison. The Evaluation Cost represents the number of theorems used in the evaluation, and
Cost Changes indicates the reduction ratio of our method’s Evaluation Cost relative to the full dataset.


                                                   A NNOTATION LLM S
      M ODEL                               A BILITY S CORE        P ass@128    E VALUATION C OST        C OST C HANGES
      CODEGEEX 4                                0.1038             0.0799               195                 -60.04%
      LLEMMA                                    0.2946             0.2029               110                 -77.46%
      T HEOREM L LAMA                           0.4283              0.416                55                 -88.73%
      D EEP S EEK -P ROVER -V1.5-RL             0.6234             0.5861                65                 -86.68%
                                                   E VALUATION LLM S
      M ODEL                               A BILITY S CORE        P ass@128    E VALUATION C OST        C OST C HANGES
      C ODE -L LAMA                             0.1384              0.123               180                 -63.11%
      Q WEN 2.5-C ODER                          0.2344             0.1783               135                 -72.34%
      M ETA M ATH -L LEMMA                      0.2353             0.1967               135                 -72.34%
      D EEP S EEK -P ROVER -V1.5-BASE           0.1427             0.1803               180                 -63.11%
      D EEP S EEK -P ROVER -V1                  0.5323             0.5205                55                 -88.73%
      D EEP S EEK -P ROVER -V1.5-SFT            0.5995              0.582                55                 -88.73%


5     Analysis on Results
5.1    Analysis on Data Annotation Results

Effectiveness of Difficulty Grading. We divided the miniF2F-graded theorems into Level 1-4 based on the sorting
of the difficulty metric. Among them, Level 4 theorems are the most difficult, with a pass rate of 0 in all Annotation
LLMs, corresponding to a difficulty metric of 1, and there are 127 theorems in this category. The remaining three levels
are divided based on the principle of equal quantity, and the difficulty coefficient range and quantity for each level are
shown in 2.
                                                Table 2: Difficulty Grading.




        D IFFICULTY G RADING                               D IFFICULTY RANGE                             C OUNT
        L EVEL 1                                            0 ≤ x ≤ 0.5539                                   120
        L EVEL 2                                         0.5539 < x ≤ 0.7661                                 120
        L EVEL 3                                         0.7661 < x ≤ 0.9864                                 121
        L EVEL 4                                                x=1                                          127
To validate the effectiveness of the difficulty grading in miniF2F-graded, we tested the pass rates of various models on
the theorems from the four difficulty levels and compared the results with the original grading method in the miniF2F
dataset [32], as shown in 3. It can be seen that in miniF2F-Graded, whether for all theorems or for MATH-category
theorems, there is a clear distinction in the pass rates of LLMs across difficulty levels Level 1-4. For each LLM, the
pass rate gradually decreases from Level 1 to Level 4, without exception. In contrast, in the original miniF2F, although
the difficulty is divided into five levels, there is little distinction in the pass rates across different levels, and even the
average pass rate for Level 2 theorems is higher than that for Level 1 theorems. The above results also confirm our


                                                              8
Running Title for Header


hypothesis: LLMs perceive theorem difficulty differently from humans. miniF2F-Graded annotates difficulty based on
the model’s actual performance, which better reflects the difficulty of theorems as perceived by LLMs.

Table 3: Model performance (P ass@128) under different difficulty levels by MiniF2F-Graded and MiniF2F. In the
original miniF2F dataset, only 260 MATH-category theorems were manually graded into 5 difficulty levels, while the
remaining theorems lack grading information. For comparison, we present separate results for all theorems and for only
the MATH-category theorems in the table.



                                                    MINI F2F-G RADED

      M ODEL                            T HEOREM S ET     L EVEL 1     L EVEL 2     L EVEL 3    L EVEL 4
      C ODE -L LAMA -7 B                    M ATH           0.48        0.0649       0.0217         0
                                            A LL            0.45        0.0417       0.0083         0
      Q WEN 2.5-C ODER -7 B                 M ATH           0.65        0.1558       0.0652         0
                                            A LL           0.5917       0.1083       0.0248         0
      M ETA M ATH -L LEMMA -7 B             M ATH           0.68        0.2078       0.0652         0
                                            A LL           0.6333       0.1417       0.0248         0
      D EEP S EEK -P ROVER -V1.5-BASE       M ATH           0.61        0.2078       0.0217         0
                                            A LL           0.5833       0.1333       0.0165         0
      D EEP S EEK -P ROVER -V1              M ATH             1         0.9351       0.3696         0
                                            A LL              1          0.925       0.1901         0
      D EEP S EEK -P ROVER -V1.5-SFT        M ATH             1            1         0.6087      0.027
                                            A LL              1            1         0.3471      0.0157
      AVERAGE                               M ATH          0.7367       0.4286       0.1920      0.0045
                                            A LL           0.7097       0.3917       0.1019      0.0026
                                                        MINI F2F

      M ODEL                            T HEOREM S ET     L EVEL 1     L EVEL 2     L EVEL 3    L EVEL 4     L EVEL 5
      C ODE -L LAMA -7 B                    M ATH          0.0952         0.2         0.26       0.2388       0.1806
      Q WEN 2.5-C ODER -7 B                 M ATH          0.3333        0.44         0.28       0.2687       0.2639
      M ETA M ATH -L LEMMA -7 B             M ATH           0.381        0.42          0.3       0.3731        0.25
      D EEP S EEK -P ROVER -V1.5-BASE       M ATH          0.4286        0.32         0.32       0.2687       0.2639
      D EEP S EEK -P ROVER -V1              M ATH          0.7143         0.7         0.76       0.7015        0.75
      D EEP S EEK -P ROVER -V1.5-SFT        M ATH          0.8095        0.76         0.84       0.7463       0.8194
      AVERAGE                               M ATH          0.4603       0.4733        0.46       0.43285      0.4213

Metric Distribution of Theorems in Each Category. The theorems in miniF2F have multiple classification methods,
and the detailed classification schemes can be found in the A.2 that introduces miniF2F. We have summarized the
average difficulty and discrimination metrics for each category of theorems based on these classification methods,
as shown in 4. Additionally, we have plotted the distribution of difficulty metrics for theorems in each category and
provided a detailed discussion of these distributions. This part can be found in E.3.
Based on the data in 4 and the analysis in Appendix, we can conclude that the metric distribution of theorems in each
category aligns with our expectations. For instance, when categorized by source, it is clear that the difficulty values of
theorems from math competitions such as IMO, AIME, and AMC are significantly higher than those from the CUSTOM
(mathematics courses) category. Several examples analyzed in the E.3 further support the reasonableness of our metric
calculation.

5.2     Analysis on Model Evaluation Results

Authenticity of Evaluation Results. In 1, we present the evaluation results obtained using our method. This section
examines whether these results accurately reflect the true proof abilities of the LLMs. The results from our evaluation
method are represented by ability scores, which belong to a different dimension than pass rates and cannot be directly
compared. However, we can still compare the differences in proof abilities between models as reflected by these
two metrics.We compared the pass rate rankings of the LLMs with different numbers of attempts to the rankings
obtained from our ability scores, and the resulting confusion matrix is shown in 3. From the results in the figure, it is
clear that the ability score rankings align well with those of P ass@16, P ass@32, and P ass@64. The only exception
is in the comparison with P ass@128, where one pair of models—Qwen2.5-Coder-7B and DeepSeek-Prover-V1.5-


                                                            9
Running Title for Header


Table 4: The average values of difficulty and discrimination metrics for theorems in each classification under different
categorization methods.



    Categorization                   Classification             Difficulty       Discrimination            Count
    Overall                                   /                  0.7494                0.4493                488
    Sort by Usage                         Test                   0.8118                0.3243                244
                                       Validation                0.687                 0.5743                244
    Sort by Provenance                   IMO                      0.978                0.0335                 40
                                        AIME                     0.9177                0.1486                 30
                                        AMC                      0.8571                0.2774                 90
                                        MATH                     0.6458                0.6185                260
                                       CUSTOM                     0.794                0.4072                 68
    Sort by Problem                   Algebra                    0.7012                0.5787                136
                                   Number Theory                 0.6318                0.5838                176
                                     Induction                   0.7854                0.4523                16
                                       Others                    0.8987                0.1923                160

Base—are ranked differently. We provide a detailed analysis of this group of models with differing rankings in F.2.
The F.2 also discusses why our results better highlight the ability differences across multiple sets of models, such as
DeepSeek-Prover-V1.5-RL and DeepSeek-Prover-V1.5-SFT.
In conclusion, the ability scores obtained through this evaluation method accurately reflect the proof abilities of LLMs.
Compared to pass rates, ability scores better reveal the performance disparities among LLMs.

6   Conclusion and Future Work

This study proposes a psychometric-based evaluation method for theorem proving with LLMs, which includes dataset
annotation and adaptive evaluation. It effectively leverages the varying importance of theorems, enabling accurate
evaluation of proof abilities with a minimal number of high-information theorems. By annotating the miniF2F dataset,
this research introduces a new dataset with metric annotations and difficulty grading: miniF2F-Graded. The difficulty
grading in miniF2F-Graded is more closely aligned with LLMs’ difficulty perception compared to manual grading. In
the evaluation of multiple open-source LLMs, the adaptive evaluation method reduced the evaluation cost by 76.13%
and yielded results that more clearly highlight the performance disparities between LLMs.
Currently, this method has been implemented using the miniF2F dataset as a case study. However, we believe
the approach is applicable to more extensive and diverse datasets and is expected to offer even greater efficiency
improvements when applied to larger-scale data collections. In the future, we plan to expand the method to additional
datasets and models, continuously updating the annotations and grading in miniF2F-Graded using progressively
enhanced SOTA models, thereby providing a reliable and efficient evaluation benchmark for LLMs in theorem proving.

Impact Statement

This paper presents a psychometric-based evaluation method for large language models in theorem proving. By
introducing the miniF2F-Graded dataset, which includes difficulty and discrimination metrics. The adaptive evaluation
method efficiently highlights performance disparities between LLMs using fewer theorems.
The societal impact of this research lies in its potential to optimize LLM evaluation in automated theorem proving,
making the process more efficient and reliable. Ethical considerations focus on ensuring the fairness and transparency of


                                                           10
Running Title for Header




                                   Figure 3: Confusion matrix of model rankings.


the grading system. Future work will extend this method to larger datasets and models, providing a scalable benchmark
for LLM evaluation in theorem proving.


References

 [1] Humza Naveed, Asad Ullah Khan, Shi Qiu, Muhammad Saqib, Saeed Anwar, Muhammad Usman, Naveed
     Akhtar, Nick Barnes, and Ajmal Mian. A comprehensive overview of large language models. arXiv preprint
     arXiv:2307.06435, 2023.
 [2] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang,
     Junjie Zhang, Zican Dong, et al. A survey of large language models. arXiv preprint arXiv:2303.18223, 2023.
 [3] Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri, and Dawn Song. Formal
     mathematical reasoning: A new frontier in ai. arXiv preprint arXiv:2412.16075, 2024.
 [4] Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui Zhang, and Wenpeng Yin. Large language models for
     mathematical reasoning: Progresses and challenges. arXiv preprint arXiv:2402.00157, 2024.
 [5] Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
     Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong Ruan.


                                                         11
Running Title for Header


     Deepseek-prover-v1.5: Harnessing proof assistant feedback for reinforcement learning and monte-carlo tree
     search. 2024.
 [6] Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya Huang, Jing
     Xiong, Han Shi, Enze Xie, et al. Lego-prover: Neural theorem proving with growing libraries. arXiv preprint
     arXiv:2310.00656, 2023.
 [7] Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and Pengfei Liu. Evaluating mathematical reasoning beyond
     accuracy. arXiv preprint arXiv:2404.05692, 2024.
 [8] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In Automated
     Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual Event, July 12–15, 2021,
     Proceedings 28, pages 625–635. Springer, 2021.
 [9] Lawrence C Paulson. Isabelle: A generic theorem prover. Springer, 1994.
[10] Gérard Huet, Gilles Kahn, and Christine Paulin-Mohring. The coq proof assistant a tutorial. Rapport Technique,
     178, 1997.
[11] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger,
     and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented language models. Advances
     in Neural Information Processing Systems, 36, 2024.
[12] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś,
     Yuhuai Wu, and Mateja Jamnik. Thor: Wielding hammers to integrate language models and automated theorem
     provers. Advances in Neural Information Processing Systems, 35:8360–8373, 2022.
[13] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix, Yuhuai
     Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem provers with informal proofs.
     arXiv preprint arXiv:2210.12283, 2022.
[14] Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation and repair with
     large language models. In Proceedings of the 31st ACM Joint European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering, pages 1229–1241, 2023.
[15] Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. Theoremllama:
     Transforming general-purpose llms into lean4 experts. arXiv preprint arXiv:2407.03203, 2024.
[16] Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu, Zhengying Liu, Yu Zhang, James T Kwok, Zhenguo Li, Adrian
     Weller, and Weiyang Liu. Metamath: Bootstrap your own mathematical questions for large language models.
     arXiv preprint arXiv:2309.12284, 2023.
[17] Renrui Zhang, Dongzhi Jiang, Yichi Zhang, Haokun Lin, Ziyu Guo, Pengshuo Qiu, Aojun Zhou, Pan Lu, Kai-Wei
     Chang, Yu Qiao, et al. Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems? In
     European Conference on Computer Vision, pages 169–186. Springer, 2025.
[18] Shibo Hao, Yi Gu, Haotian Luo, Tianyang Liu, Xiyan Shao, Xinyuan Wang, Shuhua Xie, Haodi Ma, Adithya
     Samavedhi, Qiyue Gao, et al. Llm reasoners: New evaluation, library, and analysis of step-by-step reasoning with
     large language models. arXiv preprint arXiv:2404.05221, 2024.
[19] Minghao Shao, Boyuan Chen, Sofija Jancheska, Brendan Dolan-Gavitt, Siddharth Garg, Ramesh Karri, and
     Muhammad Shafique. An empirical evaluation of llms for solving offensive security challenges. arXiv preprint
     arXiv:2402.11814, 2024.
[20] Zhijing Jin, Yuen Chen, Felix Leeb, Luigi Gresele, Ojasv Kamal, LYU Zhiheng, Kevin Blin, Fernando Gonzalez
     Adauto, Max Kleiman-Weiner, Mrinmaya Sachan, et al. Cladder: Assessing causal reasoning in language models.
     In Thirty-seventh conference on neural information processing systems, 2023.
[21] Marcelo Orenes-Vera, Margaret Martonosi, and David Wentzlaff. Using llms to facilitate formal verification of rtl.
     arXiv e-prints, pages arXiv–2309, 2023.
[22] Pengfei Hong, Deepanway Ghosal, Navonil Majumder, Somak Aditya, Rada Mihalcea, and Soujanya Poria.
     Stuck in the quicksand of numeracy, far from agi summit: Evaluating llms’ mathematical competency through
     ontology-guided perturbations. arXiv preprint arXiv:2401.09395, 2024.
[23] Pragya Srivastava, Manuj Malik, Vivek Gupta, Tanuja Ganu, and Dan Roth. Evaluating llms’ mathematical
     reasoning in financial document question answering. In Findings of the Association for Computational Linguistics
     ACL 2024, pages 3853–3878, 2024.
[24] Yan Zhuang, Qi Liu, Yuting Ning, Weizhe Huang, Rui Lv, Zhenya Huang, Guanhao Zhao, Zheng Zhang, Qingyang
     Mao, Shijin Wang, et al. Efficiently measuring the cognitive ability of llms: An adaptive testing perspective. arXiv
     preprint arXiv:2306.10512, 2023.


                                                          12
Running Title for Header


[25] Felipe Maia Polo, Lucas Weber, Leshem Choshen, Yuekai Sun, Gongjun Xu, and Mikhail Yurochkin. tinybench-
     marks: evaluating llms with fewer examples. arXiv preprint arXiv:2402.14992, 2024.
[26] Xiaohan Yuan, Jinfeng Li, Dongxia Wang, Yuefeng Chen, Xiaofeng Mao, Longtao Huang, Hui Xue, Wenhai
     Wang, Kui Ren, and Jingyi Wang. S-eval: Automatic and adaptive test generation for benchmarking safety
     evaluation of large language models. arXiv preprint arXiv:2405.14191, 2024.
[27] R Michael Furr. Psychometrics: an introduction. SAGE publications, 2021.
[28] Jonathan Templin, Robert A Henson, et al. Diagnostic measurement: Theory, methods, and applications. Guilford
     press, 2010.
[29] Robert J Mislevy, Russell G Almond, and Janice F Lukas. A brief introduction to evidence-centered design. ETS
     Research Report Series, 2003(1):i–29, 2003.
[30] Frank B Baker. The basics of item response theory. ERIC, 2001.
[31] Peter Fayers. Item response theory for psychologists, 2004.
[32] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for formal olympiad-
     level mathematics. arXiv preprint arXiv:2109.00110, 2021.
[33] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and Xiaodan
     Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic data. arXiv preprint
     arXiv:2405.14333, 2024.
[34] K. Yang. minif2f-lean4, 2023.
[35] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
     Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv preprint arXiv:2103.03874,
     2021.
[36] Li Cai, Kilchan Choi, Mark Hansen, and Lauren Harrell. Item response theory. Annual Review of Statistics and
     Its Application, 3(1):297–321, 2016.
[37] Alexander Ly, Maarten Marsman, Josine Verhagen, Raoul PPP Grasman, and Eric-Jan Wagenmakers. A tutorial
     on fisher information. Journal of Mathematical Psychology, 80:40–55, 2017.
[38] Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan Wang, Yufei Xue, Zihan Wang, Lei Shen, Andi Wang, Yang
     Li, Teng Su, Zhilin Yang, and Jie Tang. Codegeex: A pre-trained model for code generation with multilingual
     benchmarking on humaneval-x. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery
     and Data Mining, pages 5673–5684, 2023.
[39] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Albert Q. Jiang, Jia
     Deng, Stella Biderman, and Sean Welleck. Llemma: An open language model for mathematics, 2023.
[40] Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. Theoremllama:
     Transforming general-purpose llms into lean4 experts, 2024.
[41] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu
     Liu, Romain Sauvestre, Tal Remez, et al. Code llama: Open foundation models for code. arXiv preprint
     arXiv:2308.12950, 2023.
[42] An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li,
     Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong
     Tu, Jianwei Zhang, Jianxin Ma, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming
     Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize
     Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong
     Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Yang Fan, Yang Yao, Yichang
     Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zhihao Fan. Qwen2 technical report.
     arXiv preprint arXiv:2407.10671, 2024.
[43] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu,
     Kai Dang, et al. Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186, 2024.
[44] Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han, and Yuhuai Wu. Lisa: Language models of isabelle proofs.
     In 6th Conference on Artificial Intelligence and Theorem Proving, pages 378–392, 2021.
[45] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev, and Jeremy
     Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics. arXiv preprint
     arXiv:2302.12433, 2023.
[46] Qihao Zhu Runxin Xu Junxiao Song Mingchuan Zhang Y.K. Li Y. Wu Daya Guo Zhihong Shao, Peiyi Wang.
     Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024.


                                                       13
Running Title for Header


A     MiniF2F Dataset and Theorem Categories.

A.1   Introduction to MiniF2F

The miniF2F dataset [32] comprises formalized mathematical problem statements at the Olympiad level. It includes
488 formalized problems spanning high school and college-level mathematics, as well as questions from prestigious
competitions such as the International Mathematical Olympiad (IMO), American Mathematical Competitions (AMC),
and American Invitational Mathematics Examination (AIME). Although smaller in size compared to datasets like LISA
[44] and ProofNet [45], miniF2F is widely recognized for its high-quality data and extensive adoption, making it an
ideal benchmark dataset for this study.



A.2   Theorem Categories

The theorems in miniF2F are classified using multiple criteria. By purpose, they are divided into a test set and a
validation set. By source, they are categorized into IMO (International Mathematical Olympiad), AIME (American
Invitational Mathematics Examination), AMC (American Mathematics Competitions), MATH [35], and CUSTOM
(datasets from high school and undergraduate mathematics courses). By problem type, they are classified into number
theory, algebra, and induction.



B     Different Methods of Metric Calculation.

B.1   Metric Calculation by Statistical Modeling.

In Item Response Theory (IRT), models are categorized based on the number of metrics they incorporate, such as
one-metric, two-metric, or three-metric models. The two-metric model considers difficulty, which represents the
ability score required to correctly answer a question, and discrimination, which measures how effectively a question
differentiates between varying ability levels [36]. The mathematical formulation for the two-metric model is as follows:



                                                                  ea(x)(θ−b(x))
                                          P (X = 1 | θ, x) =                      .                                        (5)
                                                                1 + ea(x)(θ−b(x))



In 5, θ represents the ability level of the test subject, a(x) and b(x) represent the discrimination and difficulty of item x,
respectively, and P (X = 1 | θ, x) represents the probability of correctly answering item x with an ability level of θ.
After determining the statistical model, methods such as Maximum Likelihood Estimation (MLE), Bayesian Estimation,
and the EM algorithm are commonly used to estimate the difficulty and discrimination metrics. The more data from
test-takers, the more accurate the estimates become.



B.2   Difficulty Calculation without the Correction Term.

In the calculation of the difficulty metric, if we do not add a correction term to P (x), the result of the metric calculation
is shown in 4. By comparing 4 and 2, we can observe that adding the correction term to the difficulty metric calculation
results in a more dispersed distribution of difficulty values. Specifically, for the theorems with difficulty values between
0.4 and 0.6, the points in 4 are almost clustered together, making it difficult to distinguish them. However, in 2, where
the correction term is included, these theorems are spread across multiple difficulty levels, which is more conducive to
theorem grading and selection.


                                                             14
Running Title for Header




Figure 4: The scatter plot of the dataset annotation results when the correction term is not used in the difficulty metric
calculation.




C      Theorem Selection Algorithm.




Algorithm 2 Theorem Selection
  Input: Current ability value θ, Annotated Dataset D with metrics Discrimination : ai and Dif f iculty : bi
  Output: Selected theorems Tselected
  if First execution then
     Initialize Tlast = ∅
  end if
  for each theorem ti ∈ D do
     P (ti , θ) ← 1+e−a1i (θ−bi )
       I(ti , θ) ← afi · P (ti , θ) · (1 − P (ti , θ))
    end for
    Df iltered ← D \ Tlast
    Initialize Tselected = ∅
    for k = 1 to 5 do
       t∗ ← arg maxti ∈Df iltered I(ti , θ)
       Tselected ← Tselected ∪ {t∗ }
       Df iltered ← Df iltered \ {t∗ }
    end for
    Tlast ← (Tlast ∪ Tselected )[−50 :]
    Return Tselected


                                                           15
Running Title for Header


D     Experiment LLMs and Prompts.

D.1   Annotation LLMs.

1)codegeex4-9B (Pass@128=7.99%) is the open-source version of the latest CodeGeeX4 model series. It is a multilin-
gual code generation model trained on GLM-4-9B, which significantly enhances its code generation capabilities[38].
2)llemma-7B (Pass@128=20.29%) is a mathematical language model. The Llemma model is particularly outstanding
in terms of chain-of-thought mathematical reasoning and formal theorem proving[39].
3)TheoremLlama (Pass@128=41.60%) is a fine-tuned model for writing Lean4 proofs. Using the Open Bootstrapped
Theorem dataset for fine-tuning, TheoremLlama can achieve quite good performance when writing Lean4 proofs based
on natural language theorem statements[40].
4)DeepSeek-Prover-V1.5-RL (Pass@128=58.61%) is an open-source language model for theorem proving in Lean 4.
The model was pre-trained on DeepSeekMath-Base, focusing on formal mathematical language, and uses reinforcement
learning (RL) to improve performance based on the validation feedback of the Lean4 prover, resulting in a significant
increase in proving ability[5].


D.2   Evaluation LLMs.

1)Code-Llama-7B (Pass@128=12.30%) is a large code language model series based on Llama 2, which has achieved
state-of-the-art performance among open models in multiple code benchmarks[41].
2)Qwen2.5-Coder-7B (Pass@128=17.83%) is the latest series of the Code-Specific Qwen large language model. This
model has expanded the training token scale to 5.5 trillion on the basis of Qwen2.5, not only enhancing its coding
capabilities but also maintaining its advantages in mathematics and general abilities[42, 43].
3)MetaMath-Llemma-7B (Pass@128=19.67%), based on the Llemma-7B model, has been fully fine-tuned on the
MetaMathQA dataset. The MetaMath-7B model has achieved 66.4% on GSM8K and 19.4% on MATH, surpassing the
most advanced models of the same size[16, 39].
4-6) Three different versions of the DeepSeek-Prover series: DeepSeek-Prover-V1 (Pass@128=52.05%), V1.5-Base
(Pass@128=18.03%), and V1.5-SFT (Pass@128=58.20%). V1 fine-tuned the DeepSeekMath-7B model using large-
scale synthetic data to enhance its proving capability[33]; V1.5-Base was pre-trained on DeepSeekMath-Base[46], with
a special focus on formal languages such as Lean, Isabelle, and Metamath. V1.5-SFT was supervised fine-tuned using
an enhanced formal theorem proving dataset derived from DeepSeek-Prover-V1, which included detailed explanatory
annotations.[5].
The DeepSeek-Prover series models are used multiple times in both the annotation and evaluation models for the
following reasons: By comparing the evaluation results between different versions of the DeepSeek-Prover series
models, we can verify the effectiveness of the evaluation methods used in this study. For example, DeepSeek-Prover-
V1.5-RL, compared to DeepSeek-Prover-V1.5-SFT, has enhanced its capabilities through a combination of online
reinforcement learning (RL) and validation feedback. However, the difference between the two in terms of Pass@128 is
only 0.41% [5]. We aim to assess a more accurate gap between the two using the methods of this study.
Additionally, among the aforementioned models, some are not specifically trained for Lean formal proof but are targeted
at tasks such as code generation and mathematics. However, judging by the pass rates, these models possess a certain
level of formal proof capability, and their training data should include corpora written in Lean. Therefore, we believe
they can be used for annotation and evaluation.


D.3   Proof Prompt.

We used the following prompt to instruct the LLMs to perform theorem proofs, this is an example of a prompt for
proving a Lean theorem. The prompt includes the natural language description of the theorem (Informal Prefix) from
[34].

       • Prompt: This is a theorem written in Lean 4. Please complete the corresponding proof code to formalize the
         argument: -Informal Prefix: Expand the following expression: 7(3y + 2) Show that it is 21y + 14. -Header:
         import Mathlib import Aesop set_option maxHeartbeats 0 open BigOperators Real Nat Topology Rat -Formal
         Statement: (y : C) : 7 · (3 · y + 2) = 21 · y + 14 : = by


                                                          16
Running Title for Header


E     Data Annotation Results and Analysis.

E.1       Annotation Results: miniF2F-Graded.

The first 60 theorems in our annotated results are shown in 5, The complete results can be found at https://zenodo.
org/records/14776138.

                      Table 5: The annotation results of the first 60 theorems in miniF2F-Graded.



 T HEOREM NAME                                                     D IFFICULTY   D ISCRIMINATION    D IFFICULTY G RADE
 AMC 12 A _2019_ P 21                                                1.0000           0.0000             L EVEL 4
 AMC 12 A _2015_ P 10                                                1.0000           0.0000             L EVEL 4
 AMC 12 A _2008_ P 8                                                 0.7377           0.6056             L EVEL 2
 MATHD _ ALGEBRA _182                                                0.4083           0.9594             L EVEL 1
 AIME _1984_ P 5                                                     0.9793           0.0025             L EVEL 3
 MATHD _ NUMBERTHEORY _780                                           0.9819           0.0012             L EVEL 3
 MATHD _ ALGEBRA _116                                                0.5083           0.9305             L EVEL 1
 MATHD _ NUMBERTHEORY _13                                            1.0000           0.0000             L EVEL 4
 MATHD _ NUMBERTHEORY _169                                           0.5012           0.8897             L EVEL 1
 AMC 12 A _2009_ P 9                                                 0.5561           0.9339             L EVEL 2
 AMC 12 A _2019_ P 9                                                 1.0000           0.0000             L EVEL 4
 MATHD _ ALGEBRA _13                                                 0.5405           0.9218             L EVEL 1
 INDUCTION _ SUM 2 KP 1 NPQSQM 1                                     0.6128           0.8390             L EVEL 2
 AIME _1991_ P 6                                                     0.9767           0.0037             L EVEL 3
 MATHD _ NUMBERTHEORY _149                                           0.4107           0.8946             L EVEL 1
 IMO _1984_ P 2                                                      1.0000           0.0000             L EVEL 4
 AMC 12 A _2008_ P 4                                                 0.9682           0.0085             L EVEL 3
 IMO _2006_ P 3                                                      1.0000           0.0000             L EVEL 4
 MATHD _ ALGEBRA _462                                                0.4182           0.9193             L EVEL 1
 IMO _1964_ P 1_2                                                    0.9524           0.1021             L EVEL 3
 MATHD _ NUMBERTHEORY _221                                           1.0000           0.0000             L EVEL 4
 MATHD _ NUMBERTHEORY _64                                            0.5606           0.9266             L EVEL 2
 IMO _1987_ P 4                                                      0.9819           0.0012             L EVEL 3
 MATHD _ NUMBERTHEORY _33                                            0.5450           0.9205             L EVEL 1
 AMC 12_2001_ P 9                                                    0.5651           0.9193             L EVEL 2
 IMO _1965_ P 1                                                      1.0000           0.0000             L EVEL 4
 MATHD _ NUMBERTHEORY _48                                            0.5360           0.9351             L EVEL 1
 NUMBERTHEORY _ SQMOD 4 IN 01 D                                      0.5561           0.9339             L EVEL 2
 MATHD _ NUMBERTHEORY _466                                           0.4430           0.9225             L EVEL 1
 MATHD _ ALGEBRA _48                                                 0.5174           0.8870             L EVEL 1
 AMC 12_2000_ P 15                                                   1.0000           0.0000             L EVEL 4
 MATHD _ NUMBERTHEORY _132                                           0.1974           0.9030             L EVEL 1
 AMC 12 A _2009_ P 5                                                 0.5561           0.9339             L EVEL 2
 MATHD _ NUMBERTHEORY _188                                           0.2371           0.9427             L EVEL 1
 MATHD _ ALGEBRA _224                                                1.0000           0.0000             L EVEL 4
 INDUCTION _ DIVISIBILITY _3 DIVNTO 3 M 2 N                          0.5561           0.9339             L EVEL 2
 INDUCTION _ SUM _1 OKTKP 1                                          0.5606           0.9266             L EVEL 2
 MATHD _ NUMBERTHEORY _32                                            0.5539           0.9059             L EVEL 1
 MATHD _ ALGEBRA _422                                                0.5827           0.8901             L EVEL 2
 MATHD _ ALGEBRA _73                                                 0.5268           0.9316             L EVEL 1
 MATHD _ NUMBERTHEORY _109                                           0.4634           0.9279             L EVEL 1
 ALGEBRA _ XMYSQPYMZSQPZMXSQEQXYZ _ XPYPZP 6 DVDX 3 Y 3 Z 3          0.5561           0.9339             L EVEL 2
 AMC 12 B _2002_ P 11                                                1.0000           0.0000             L EVEL 4
 IMO _1962_ P 4                                                      1.0000           0.0000             L EVEL 4
 MATHD _ NUMBERTHEORY _236                                           0.2146           0.9611             L EVEL 1
 MATHD _ NUMBERTHEORY _24                                            0.4903           0.8495             L EVEL 1
 ALGEBRA _ AMGM _ PROD 1 TONEQ 1_ SUM 1 TONGEQN                      0.9819           0.0012             L EVEL 3
 MATHD _ ALGEBRA _101                                                0.5606           0.9266             L EVEL 2
 MATHD _ NUMBERTHEORY _257                                           0.5651           0.9193             L EVEL 2
 ......                                                               ......           ......               ......


                                                          17
Running Title for Header


E.2   Analysis on Unusual Observations in the Scatter Plot.

The difficulty-discrimination distribution in 2 generally aligns with our intuitive understanding of test items. However,
unlike typical test distributions, no tester (LLM) has been able to correctly answer all difficult questions (theorems),
leading to a blank upper-right region in the scatter plot. Additionally, the lower-right corner contains numerous points
(where difficulty is close to 1 and discrimination is close to 0), representing theorems that no model has successfully
proven. Furthermore, the absence of theorems with a discrimination value below 0 suggests that the proof performance
of the selected labeling models exhibits a gradient distribution, which aligns with the prior ability distribution.

E.3   Analysis on Distribution of Difficulty Metrics.




                      Figure 5: Difficulty Distribution Chart for Theorems in Various Categories..


From the distribution in 5 and 4, we can draw several key conclusions:
1) For all the theorems, excluding those with a difficulty value of 1, the difficulty of the remaining theorems roughly
follows a normal distribution centered around 0.6.
2) When the theorems are divided into the test set and the validation set, it is evident that the overall difficulty of the test
set is higher than that of the validation set, which aligns with our expectations. This is because, in the miniF2F design,
the test set is reserved for evaluation, while the validation set may have been used during model training [32]. However,
the average discrimination of the validation set is still higher than that of the test set, which is due to the fact that the
test set contains many high-difficulty theorems that reduce the discrimination.
3) When the theorems are categorized by source, it is clear that the average difficulty of the IMO, AIME, and AMC
competitions is significantly higher than that of MATH and CUSTOM. This is because competition problems tend to be
more complex, but their higher complexity also leads to a lower discrimination. The MATH dataset, with its moderate
difficulty, has the highest discrimination, making it suitable for testing. In contrast, problems in the CUSTOM category,


                                                              18
Running Title for Header


sourced from high school and undergraduate courses, have the lowest difficulty, which lowers the discrimination since
even lower-capacity models can solve these problems.
4) When classified by problem type, we can observe that induction problems are the most difficult for the models,
while number theory problems are the easiest. Theorems in the "OTHERS" category, most of which originate from
competitions, may involve algebra, number theory, and other types of problems, thus making their difficulty the highest.


F     Adaptive Evaluation Results and Analysis.

F.1   Evaluation Process.

We present the evaluation process of one LLM in 6.

                                Table 6: Test process for model DeepSeek-Prover-V1.

           N UMBER         T HEOREM NAME         D IFFICULTY    D ISCRIMINATION   S UCCESS R ATE     A BILITY S CORE
           1           MATHD _ ALGEBRA _182        0.4083           0.9594         0.5859375       0.50025 (+0.00025)
           2         MATHD _ NUMBERTHEORY _551     0.3564           0.9578           0.65625       0.50074 (+0.00049)
           3         MATHD _ NUMBERTHEORY _517     0.2552           0.9762         0.8671875       0.50197 (+0.00123)
           4         MATHD _ NUMBERTHEORY _198     0.2959           0.9668         0.7265625       0.50268 (+0.00071)
           5         MATHD _ NUMBERTHEORY _101     0.3128           0.9631         0.8046875       0.50372 (+0.00104)
           6         MATHD _ NUMBERTHEORY _202     0.1751           0.9971          0.890625       0.50496 (+0.00124)
           7           MATHD _ ALGEBRA _109        0.4763           0.9419          0.78125        0.50605 (+0.00109)
           8           MATHD _ ALGEBRA _536        0.513            0.9414         0.3046875       0.50528 (-0.00077)
           9             AMC 12 A _2016_ P 3        0.513           0.9414          0.484375       0.50522 (-0.00006)
           10        MATHD _ NUMBERTHEORY _37      0.2611           0.9669         0.6328125       0.50552 (+0.00030)
           11           MATHD _ ALGEBRA _77        0.5223           0.9389         0.0234375       0.50363 (-0.00189)
           12           MATHD _ ALGEBRA _55        0.5268           0.9376         0.9296875       0.50537 (+0.00174)
           13          MATHD _ ALGEBRA _126        0.5314           0.9364           0.8125        0.50664 (+0.00127)
           14          MATHD _ ALGEBRA _410        0.5314           0.9364         0.7578125       0.50770 (+0.00106)
           15        MATHD _ NUMBERTHEORY _412     0.5314           0.9364          0.796875       0.50891 (+0.00121)
           16          MATHD _ ALGEBRA _182        0.4083           0.9594         0.5859375       0.50915 (+0.00024)
           17        MATHD _ NUMBERTHEORY _551     0.3564           0.9578           0.65625       0.50963 (+0.00048)
           18        MATHD _ NUMBERTHEORY _517     0.2552           0.9762         0.8671875       0.51085 (+0.00122)
           19        MATHD _ NUMBERTHEORY _198     0.2959           0.9668         0.7265625       0.51155 (+0.00070)
           20        MATHD _ NUMBERTHEORY _101     0.3128           0.9631         0.8046875       0.51258 (+0.00103)
           21          MATHD _ ALGEBRA _536         0.513           0.9414         0.3046875       0.51180 (-0.00078)
           22            AMC 12 A _2016_ P 3        0.513           0.9414          0.484375       0.51174 (-0.00006)
           23        MATHD _ NUMBERTHEORY _202     0.1751           0.9971          0.890625       0.51297 (+0.00123)
           24          MATHD _ ALGEBRA _109        0.4763           0.9419          0.78125        0.51406 (+0.00109)
           25        MATHD _ NUMBERTHEORY _37      0.2611           0.9669         0.6328125       0.51435 (+0.00029)
           26           MATHD _ ALGEBRA _77        0.5223           0.9389         0.0234375       0.51245 (-0.00190)
           27           MATHD _ ALGEBRA _55        0.5268           0.9376         0.9296875       0.51418 (+0.00173)
           28          MATHD _ ALGEBRA _126        0.5314           0.9364           0.8125        0.51545 (+0.00127)
           29          MATHD _ ALGEBRA _410        0.5314           0.9364         0.7578125       0.51649 (+0.00104)
           30        MATHD _ NUMBERTHEORY _412     0.5314           0.9364          0.796875       0.51769 (+0.00120)
           31          MATHD _ ALGEBRA _182        0.4083           0.9594         0.5859375       0.51793 (+0.00024)
           32        MATHD _ NUMBERTHEORY _551     0.3564           0.9578           0.65625       0.51840 (+0.00047)
           33        MATHD _ NUMBERTHEORY _198     0.2959           0.9668         0.7265625       0.51910 (+0.00070)
           34        MATHD _ NUMBERTHEORY _101     0.3128           0.9631         0.8046875       0.52012 (+0.00102)
           35        MATHD _ NUMBERTHEORY _517     0.2552           0.9762         0.8671875       0.52133 (+0.00121)
           36          MATHD _ ALGEBRA _536         0.513           0.9414         0.3046875       0.52054 (-0.00079)
           37            AMC 12 A _2016_ P 3        0.513           0.9414          0.484375       0.52047 (-0.00007)
           38          MATHD _ ALGEBRA _109        0.4763           0.9419          0.78125        0.52155 (+0.00108)
           39        MATHD _ NUMBERTHEORY _202     0.1751           0.9971          0.890625       0.52277 (+0.00122)
           40        MATHD _ NUMBERTHEORY _37      0.2611           0.9669         0.6328125       0.52305 (+0.00028)
           41           MATHD _ ALGEBRA _77        0.5223           0.9389         0.0234375       0.52114 (-0.00191)
           42           MATHD _ ALGEBRA _55        0.5268           0.9376         0.9296875       0.52287 (+0.00173)
           43          MATHD _ ALGEBRA _126        0.5314           0.9364           0.8125        0.52413 (+0.00126)
           44          MATHD _ ALGEBRA _410        0.5314           0.9364         0.7578125       0.52516 (+0.00103)
           45        MATHD _ NUMBERTHEORY _412     0.5314           0.9364          0.796875       0.52636 (+0.00120)
           46          MATHD _ ALGEBRA _182        0.4083           0.9594         0.5859375       0.52659 (+0.00023)
           47        MATHD _ NUMBERTHEORY _551     0.3564           0.9578           0.65625       0.52705 (+0.00046)
           48        MATHD _ NUMBERTHEORY _198     0.2959           0.9668         0.7265625       0.52773 (+0.00068)
           49        MATHD _ NUMBERTHEORY _101     0.3128           0.9631         0.8046875       0.52875 (+0.00102)
           50        MATHD _ NUMBERTHEORY _517     0.2552           0.9762         0.8671875       0.52995 (+0.00120)
           51          MATHD _ ALGEBRA _536         0.513           0.9414         0.3046875       0.52915 (-0.00080)
           52            AMC 12 A _2016_ P 3        0.513           0.9414          0.484375       0.52908 (-0.00007)
           53          MATHD _ ALGEBRA _109        0.4763           0.9419          0.78125        0.53015 (+0.00107)
           54        MATHD _ NUMBERTHEORY _202     0.1751           0.9971          0.890625       0.53136 (+0.00121)
           55        MATHD _ NUMBERTHEORY _48       0.536           0.9351         0.7421875       0.53234 (+0.00098)



                                                               19
Running Title for Header


F.2   Analysis on Ability Ranking

We will analyze this pair of reversed models: In the ability score results, Qwen2.5-Coder-7B has a higher ability
score (0.2344) than DeepSeek-Prover-V1.5-Base (0.1427), but in the P ass@128 results, the ranking is reversed. This
occurs because Qwen2.5-Coder-7B performs better on higher-difficulty problems than DeepSeek-Prover-V1.5-Base.
From 3, we observe that Qwen2.5-Coder-7B achieves a pass rate of 6.52% on Level 3 theorems, much higher than
the 2.17% achieved by DeepSeek-Prover-V1.5-Base. Our adaptive evaluation method assigns higher weights to high-
difficulty theorems, which results in Qwen2.5-Coder-7B having a higher overall ability score. Furthermore, although
DeepSeek-Prover-V1.5-Base (0.1803) slightly exceeds Qwen2.5-Coder-7B (0.1783) in P ass@128, when we compare
the attempt success rate shown in 7, Qwen2.5-Coder-7B (0.0068) is higher than DeepSeek-Prover-V1.5-Base (0.0055).
This suggests that the higher ability score assigned to Qwen2.5-Coder-7B by our evaluation method is reasonable.
Analysis of other models: Taking the codegeex4-9b model as an example, the model’s P ass@128 reaches 0.0799, but
the attempt success rate is only 0.0012, which is much lower than Llemma-7b’s 0.0119. This indicates that, out of
128 proof attempts, the model has only a small number of successful attempts. The P ass@128 metric clearly ignores
this aspect, focusing only on whether there was a success in any of the 128 attempts. The actual proof capability
gap between codegeex4-9b and Llemma-7b should be greater than what is indicated by P ass@128. Our method’s
evaluation result, 0.1038, accounts for the number of successful attempts and provides a more authentic reflection of the
actual proof capability gap, which is more accurately shown by Llemma-7b (0.2946).
Additionally, comparing DeepSeek-Prover-V1.5-RL and SFT, the RL model is enhanced with online reinforcement
learning and other techniques based on the SFT model. However, the improvement in the P ass@128 metric is only
0.41%. Is the actual difference between the two models really that small? We can see from the attempt success rate
that this is not the case. The attempt success of RL (47.72%) is higher than that of SFT (44.86%), and our evaluation
method has more accurately reflected the difference between them, with ability scores of 0.623 and 0.5995, respectively.

                                      Table 7: Comparison of Evaluation Results.


      Model                                   Ability Score          Pass@128           Attempt Succse Rate
      Codegeex4-9b                                 0.1038              0.0799                     0.0012
      Llemma7b                                     0.2946              0.2029                     0.0119
      TheoremLlama                                 0.4283              0.416                       0.026
      DeepSeek-Prover-V1.5-RL                      0.6234              0.5861                     0.4772
      Code-Llama-7b                                0.1384              0.123                      0.0022
      Qwen2.5-Coder-7b                             0.2344              0.1783                     0.0068
      MetaMath-Llemma-7b                           0.2353              0.1967                     0.0094
      DeepSeek-Prover-V1.5-Base                    0.1427              0.1803                     0.0055
      DeepSeek-Prover-V1                           0.5323              0.5205                     0.3282
      DeepSeek-Prover-V1.5-SFT                     0.5995              0.5820                     0.4486




                                                           20
