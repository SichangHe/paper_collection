                                                Linear Reasoning vs. Proof by Cases: Obstacles for Large Language
                                                                 Models in FOL Problem Solving



                                               Yuliang Ji           Fuchen Shen                  Jian Wu                  Qiujie Xie                Yue Zhang
                                          Nanjing University of    Westlake University       Westlake University       Zhejiang University       Westlake University
                                         Science and Technology                                                        Westlake University
arXiv:2602.20973v1 [cs.CL] 24 Feb 2026




                                                                  Abstract                                mathematical problems (Ahn et al., 2024; Kojima et al.,
                                                                                                          2022), where mathematical logic establishes an essential
                                                 To comprehensively evaluate the mathemati-               role in structuring mathematical proofs and reasoning
                                                 cal reasoning capabilities of Large Language             (Hilbert and Ackermann, 1928). The core of mathemati-
                                                 Models (LLMs), researchers have introduced               cal logic involves propositional logic and first-order logic
                                                 abundant mathematical reasoning datasets.                (FOL), where FOL problems need to derive conclusions
                                                 However, most existing datasets primarily                from given premises, demanding logical reasoning skills
                                                 focus on linear reasoning, neglecting other              and the capability to process complex logical relation-
                                                 parts such as proof by contradiction and proof           ships described in natural language (Cobbe et al., 2021;
                                                 by cases, which are crucial for investigating            Parmar et al., 2024).
                                                 LLMs’ reasoning abilities. To address this               To comprehensively evaluate the mathematical reason-
                                                 limitation, we first introduce a novel first-            ing capabilities of LLMs, scientists have introduced
                                                 order logic (FOL) dataset named PC-FOL,                  many datasets (Kaliszyk et al., 2017; Karl et al., 2021;
                                                 annotated by professional mathematicians, fo-            Mitra et al., 2024; Iman et al., 2024; Welleck et al.,
                                                 cusing on case-based reasoning problems. All             2021; Yang et al., 2023a). For example, researchers
                                                 instances in this dataset are equipped with              have evaluated the capabilities of their models on the
                                                 a manually written natural language proof                GSM8K (Karl et al., 2021) dataset, which contains both
                                                 , clearly distinguishing it from conventional            computational and word problems, requiring models
                                                 linear reasoning datasets. Our experimental              to possess logical reasoning and calculation abilities to
                                                 results over leading LLMs demonstrate a sub-             get correct answers. However, limited FOL reasoning
                                                 stantial performance gap between lin-                    datasets (Amini et al., 2019) have been proposed to
                                                 ear reasoning and case-based reasoning                   evaluate the FOL reasoning abilities of LLMs, and each
                                                 problems. To further investigate this phe-               of them has its own shortcomings. As shown in Table
                                                 nomenon, we provide a theoretical analysis               1, RuleTaker (Clark et al., 2020), LogicNLI (Tian et al.,
                                                 grounded in graphical model, which provides              2021), ProntoQA (Saparov and He, 2023) are datasets
                                                 an explanation for the observed disparity be-            that include FOL examples, but they do not provide
                                                 tween the two types of reasoning problems.               natural language proofs. FOLIO (Han et al., 2024a)
                                                 We hope this work can reveal the core chal-              and P-FOLIO (Han et al., 2024b) are among the earli-
                                                 lenges in the field of automated natural lan-            est datasets to propose standard FOL problems based
                                                 guage mathematical proof generation, paving              on real-world stories, written in natural language by
                                                 the way for future research.                             human annotators. However, FOLIO does not provide
                                                                                                          corresponding answers, and P-FOLIO includes only
                                                                                                          step-by-step reasoning chains without natural language
                                            1    Introduction                                             explanations.
                                                                                                          More importantly, although existing FOL datasets have
                                            By utilizing massive training datasets and computa-
                                                                                                          made progress in terms of coverage and linguistic diver-
                                            tional resources, LLMs have shown potential in solving
                                                                                                          sity, they generally lack systematic annotation
                                            Proceedings of the 29th International Conference on Arti-     of proof strategies, particularly whether a prob-
                                            ficial Intelligence and Statistics (AISTATS) 2026, Tangier,   lem requires the use of proof by cases, a widely
                                            Morocco. PMLR: Volume 300. Copyright 2026 by the au-          employed reasoning technique in discrete mathematics
                                            thor(s).                                                      (Hales, 2005; Ji et al., 2019). From the perspective of
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving

Table 1: Comparison of BS-FOL with other datasets                      lems. For example, GPT-4o performs well on our
related to mathematical logic reasoning. “Standard                     linear reasoning instances with 85% accuracy, but only
FOL” represents whether the data instances are writ-                   gets a 51% accuracy on our proof-by-cases instances.
ten in formal FOL. “NL Instance” represents whether                    Furthermore, we provide theoretical analysis (Section
the dataset is written in natural language. “Reason-                   6) by using the graphical model to explain why such
ing Chains” shows whether the dataset explains the                     a significant performance gap exists between the two
answer in the form of reasoning chains. “NL proofs”                    types of reasoning problems.
represents whether the dataset gives natural language
proofs. “Linear/Case Label” represents whether the                     Our contributions are the following parts: (1)
data instance is supported with a label of FOL type.                   We manually curate a FOL dataset named PC-
                                                                       FOL, which contains expert-annotated instances under
                          Standard   NL         NL       Linear/Case   two types of FOL questions for the first time. (2) We
  Dataset Name     Size
                          FOL        Instance   proofs   Label         benchmark the performance of the FOL reason-
  GSM8K(2021)      8.5k      ✕          ✓         ✓         N/A        ing task for several LLMs by prompting them with
  MathQA(2019)     37k                                      N/A
                             ✕          ✓         ✓
                                                                       zero-shot or few-shot examples, and find a substan-
 RuleTaker(2020)   500k      ✓          ✓         ✕          ✕
 LogicNLI(2021)    20k       ✓          ✓         ✕          ✕         tial performance gap between the two types of FOL
 ProntoQA(2023)    46k       ✓          ✓         ✕          ✕         problems. (3) We provide a plausible theory to
  FOLIO(2024a)     1204      ✓          ✓         ✕          ✕
 P-FOLIO(2024b)    1437      ✓          ✓         ✕          ✕
                                                                       explain the reason why there exists such a substantial
  Our PC-FOL       2044      ✓          ✓         ✓          ✓
                                                                       performance gap.

reasoning methodology, natural language FOL prob-                      2     Related Work
lems can be broadly categorized into two types (Table
2): linear-reasoning and proof-by-cases. Problems                      2.1   Dataset for FOL reasoning
in the linear-reasoning category exhibit a single, sequen-
tial reasoning path, where conclusions can be derived                  Compared with abundant mathematical reasoning
through straightforward step-by-step inference. In con-                datasets, the number of datasets specifically designed
trast, proof-by-cases problems require partitioning the                for FOL reasoning is limited. RuleTaker (Clark et al.,
reasoning process into multiple scenarios, analyzing                   2020) systematically evaluates a model’s multi-step rea-
each case independently, and subsequently integrating                  soning capabilities using data automatically generated
the outcomes to determine the final truth value. Thus,                 from facts and rules. LogicNLI (Tian et al., 2021) is a
it is necessary to evaluate LLMs’ FOL reasoning abili-                 benchmark following basic principles of FOL to diag-
ties across these two types of problems, since the proof               nose LLMs’ FOL reasoning ability. ProntoQA (Saparov
processes they involve are fundamentally different.                    and He, 2023) creates the dataset through a four-stage
                                                                       process: ontology generation, proof construction, nat-
To address these challenges, we propose a Proof-by-
                                                                       ural language conversion, and answer annotation. It
Cases FOL benchmark (PC-FOL), which is a robust
                                                                       is specifically designed to assess model performance
FOL reasoning dataset annotated by professional math-
                                                                       in complex logical reasoning and planning tasks. FO-
ematicians and focuses on FOL problems that need to
                                                                       LIO (Han et al., 2024a) is the first reasoning dataset
be solved by proof-by-cases technique. All instances in
                                                                       to combine natural language with FOL annotations.
this dataset are equipped with a manually written nat-
                                                                       Based on FOLIO, P-FOLIO (Han et al., 2024b) gives
ural language proof by our annotators. Note that we do
                                                                       the answers as step-by-step reasoning chains in the
not list proof-by-contradiction as an independent type,
                                                                       form of designed inference rules.
because all such proofs can be expressed in a standard
process in the form of proof by cases. The details are
shown in Appendix I. To further assess the reasoning                   2.2   LLM Natural Language Reasoning over
abilities of LLMs, inspired by CofQA (Wu et al., 2024),                      Mathematical Problems
we apply lexical substitution by replacing certain
                                                                       Recent research has introduced various methods to
nouns with random combinations of English alphabets
                                                                       enhance the natural language reasoning capabilities
in our instances. Therefore, LLMs cannot rely on their
                                                                       of LLMs in solving mathematical problems, while our
memories and must answer the problem based on the
                                                                       work focuses on the obstacles that LLMs encounter in
given premises.
                                                                       logical reasoning tasks. Here, we highlight several signif-
Based on PC-FOL, we evaluate and report the reason-                    icant works that employ diverse approaches, including:
ing ability of several leading LLMs (Section 5). Ex-                   (1) Chain-of-Thought (CoT) Reasoning, which
perimental results show that there is a huge gap                       significantly improves the ability of LLMs on complex
between the performance of LLMs on linear-                             problems. This strategy is employed by leading models
reasoning problems and proof-by-cases prob-                            such as OpenAI-O1 (OpenAI, 2024) and DeepSeek-R1
                             Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang

Table 2: Examples of linear-reasoning problem and proof-by-cases problem. The left side presents an example
of linear-reasoning FOL question with a step-by-step proof sketch. The right side presents an example of
proof-by-cases FOL question with a proof sketch.

 FOL
                    Linear-Reasoning                                              Proof-by-Cases
 Type
           NL Premises                        NL Premises
           1.No songs are visuals.            1.Any person that is tall does not major in physics.
           2.All folk songs are songs.        2.All people who are not tall study quantum computing.
           3.All videos are visuals.          3.All students major in math or physics.
 Example   4.All movies are videos.           4.If a person majors in math, then the person studies algebraic geometry.
           5.All sci-fi movies are movies.    5.If a person majors in math, then the person does not study quantum computing.
           6.Inception is a sci-fi movie.     6.Billy is a student who studies algebraic geometry.
           NL Conclusions                     NL Conclusions
           Inception is a folk song.          Billy either majors in physics or studies quantum computing.




 Proof
 Process




(DeepSeek-AI et al., 2025a). (2) Symbolic Reason-                3     Preliminaries
ing. MathCoder (Wang et al., 2024) improves the
performance by enabling LLMs to use code for mod-
eling and deriving math equations. AlphaGeometry                 3.1     FOL Natural-Language Problem
(Trinh et al., 2024) employs LLMs to translate natural
language math problems into formal proof languages,              Propositional logic and FOL are two topics in the math-
demonstrating impressive generalization capabilities.            ematical logic field, focusing on the study of formalized
Other models such as MathBERT (Peng et al., 2021)                structures of reasoning. Propositional logic establishes
and MathGLM (Yang et al., 2023b) optimize symbolic               reasoning relationships between atomic propositions
understanding by embedding mathematical formulas                 using logical connectives such as implication (→), con-
during pretraining, achieving outstanding results on             junction (∧), disjunction (∨), and negation (¬). FOL
algebraic and arithmetic tasks. (3) Prompt Engi-                 extends this framework by introducing quantifiers (∀,
neering The Thought Propagation method (Yu et al.,               ∃) and predicates, enabling the formal representation
2024) explores designing a special prompt template,              of individual objects and their attributes.
dynamically selecting the optimal path to enhance                Most widely used mathematical datasets, particularly
the flexibility and effectiveness of solving mathemati-          FOL datasets, focus on step-by-step proofs. However,
cal problems. Active Prompting method (Diao et al.,              a substantial class of mathematical problems involves
2024) focuses on selecting high-information examples             statements containing logical disjunctions (“or,” ∨) or
to optimize model responses.                                     exclusive disjunctions (“either/or,” XOR). Such prob-
                                                                 lems cannot be solved through straightforward sequen-
                                                                 tial reasoning, since it is necessary to consider the dis-
                                                                 tinct cases introduced by the disjunctive or exclusive
                                                                 disjunctive terms and determine whether the conclusion
                                                                 holds under each scenario.
  Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving

Table 3: Basic statistics of PC-FOL. #Linear-                  Table 4: Statistical comparison of PC-FOL with
Reasoning represents the number of linear-reasoning            other datasets related to mathematical logic or FOL.
type instances, #Proof-by-Cases represents the number          #Stories represents the number of distinct premise
of the proof-by-cases type instances.                          sets aligned to the instances. #Vocab represents the
                                                               number of distinct words in the dataset.
                      #Linear      #Proof-by
   Dataset Name                                  #Total
                      Reasoning    -Cases                          Dataset Name   #Stories   #Premises   #Instances   #Vocab
    PC-FOL               511           511         1022         RuleTaker(2020)    456         11M         500k         65
 PC-FOL-Replace          511           511         1022         LogicNLI(2021)     2000        480k         20k        1091
                                                                 FOLIO(2024a)      413         6398        1204        4119
   PC-FOL Total          1022         1022         2044         P-FOLIO(2024b)     487         7620        1437        4658
                                                                   PC-FOL           291        5836        1022        3373
Hence, in this work, we categorize natural language             PC-FOL-Replace      291        5870        1022       11293
FOL problems into two types: linear-reasoning and                  PC-FOL Total     582        11706       2044       14666
proof-by-cases. The left side of Table 2 presents
an example of a linear-reasoning FOL question. The             step-by-step proofs (corresponding to the left side of Ta-
step-by-step answer for this question is given as follows:     ble 2) is represented as a binary variable that takes the
Based on the given premises, premise 6 establishes             value true or false. For instance, let A denote “Incep-
that “Inception” is a sci-fi movie. Subsequently, from         tion is a sci-fi movie,” B denote “Inception is a movie,”
premise 5, we know it is a movie; from premise 4, it is        and F denote “Inception is a folk song.” Arrows in the
a video; and from premise 3, it is a visual. According         graph indicate the direction of logical inference. Such
to premise 1, “Inception” is not a song, and premise 2         representation is similar to the probabilistic graphical
states it is not a folk song. As a result, the conclusion      model. The probabilistic graphical model uses a graph
“Inception is a folk song” is false. The right side of Table   to express the conditional dependencies among random
2 provides an example of a proof-by-cases FOL question.        variables. Mathematically, in a graphical model, if
To determine the truth value of the conclusion, one            the events are X1 , . . . , Xn , then
                                                                                                   Qn their joint probabil-
must discuss the two possible cases given by premise           ity satisfies P [X1 , . . . , Xn ] = i=1 P [Xi |pa(Xi )] where
3 separately. The reasoning proceeds as follows: In            pa(Xi ) is the set of parents of node Xi .
the left case, Billy majors in math, then Billy neither
majors in physics (premises 5, 1, and 2) nor studies           4     The PC-FOL Dataset
quantum computing (premise 5); In the right case,
Billy majors in physics, then Billy must study quantum         In this section, we detail the properties of our PC-
computing (premises 1, 2); Thus, in both cases, the            FOL dataset, and present key statistics of our dataset
conclusion is false; As a result, we can conclude that         in comparison to existing FOL datasets. The data
the truth value of the conclusion is false.                    collection process is outlined in Appendix B.1.
Based on the above explanation, we can see that the            Dataset Structure Our PC-FOL dataset contains
two proof types are completely different. Therefore, it is     2044 instances categorized into two types: Linear-
essential to additionally evaluate the LLMs’ reasoning         Reasoning type questions and Proof-by-Cases type
abilities on proof-by-cases FOL problems and discover          questions. For each instance, natural language answers
the performance gap of LLMs between the two types              are carefully provided by by professional annotators.
of FOL questions.                                              Furthermore, we apply the lexical substitution tech-
                                                               niques by replacing the nouns with various nonsensical
3.2   Graphical Model                                          combinations of alphabetic characters on the PC-FOL
                                                               dataset to construct the PC-FOL-Replace dataset.
                                                               Number of Instances The basic statistics of PC-
                                                               FOL are shown in Table 3. Since our dataset focuses
                                                               on the proof-by-case type FOL reasoning problems,
                                                               we balance the number of instances of the two types.
Figure 1: Abstracted reasoning chain for the left side         Therefore, for each sub-dataset, our annotators col-
example of Table 2.                                            lected 511 instances, resulting in 1022 linear-reasoning
                                                               instances and 1022 proof-by-case instances.
When solving FOL problems in mathematical logic as-            Stories and Premises Table 4 shows that our dataset
signments, it is possible to abstract the logical reasoning    contains 2044 instances and 11706 premises. Using the
process into a graphical representation, as shown in Fig-      same definition in FOLIO, we call the premise sets in
ure 1. In this graph, each property of “Inception” in the      an instance a story. By this definition, our PC-FOL
                           Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang

Table 5: Logical reasoning accuracy results (in %) of zero-shot and few-shot prompting on PC-FOL dataset. “Acc.
Gap” represents the performance gap between the Linear-Reasoning questions and Proof-by-Cases questions.

                       PC-FOL             PC-FOL           PC-FOL      PC-FOL-Replace     PC-FOL-Replace   PC-FOL-Replace
         Model
                       Linear-Reasoning   Proof-by-Cases   Acc. Gap    Linear-Reasoning   Proof-by-Cases   Acc. Gap
     GPT-4o 0-shot          85.13             51.08         34.05↓          84.34             51.66            32.68↓
     GPT-4o 3-shot          83.17             55.58         27.59↓          82.39             52.64            29.75↓
     GPT-4.1 0-shot         89.24             69.86         19.38↓          88.45             63.80            24.65↓
     GPT-4.1 3-shot         86.30             71.23         15.07↓          84.34             68.69            15.65↓
      o4-mini 0-shot        90.80             79.84         10.96↓          88.26             77.89            10.37↓
      o4-mini 3-shot        90.02             80.43          9.59↓          88.45             79.45            9.00↓
 Llama 3-70B 0-shot         80.63             46.77         33.86↓          79.84             50.88            28.96↓
 Llama 3-70B 3-shot         83.56             54.21         29.35↓          80.63             53.62            27.01↓
 Deepseek-V3 0-shot         89.63             76.71         12.92↓          86.69             73.39            13.30↓
 Deepseek-V3 3-shot         90.02             77.10         12.92↓          85.71             72.02            13.69↓
    Qwen3-14B 0-shot        87.28             63.60         23.68↓          84.54             59.10            25.44↓
    Qwen3-14B 3-shot        89.04             66.34         22.70↓          86.89             64.97            21.92↓



dataset contains 291 distinct stories.                          use Accuracy as the metric to evaluate the generated
                                                                truth values. Also, following the P-FOLIO (Han et al.,
Vocabulary Our PC-FOL dataset contains a vocabu-
                                                                2024b) paper, we try two metrics to evaluate the gen-
lary of 3373 unique words. By replacing noun words
                                                                erated proofs: ROUGE (Lin, 2004) and pass@k (Chen
with combinations of random English alphabets and
                                                                et al., 2021). The Accuracy metric reports the per-
making minor modifications to the instances in PC-
                                                                centage of correct truth value (True/False/Unknown)
FOL, we construct the PC-FOL-Replace dataset, sig-
                                                                generated by the tested LLMs. The ROUGE met-
nificantly increasing the vocabulary size to 11293.
                                                                rics including ROUGE-1, ROUGE-2, and ROUGE-L
                                                                (Lin, 2004), are used to compare the model-generated
5      Experiments                                              proofs with human-written proofs. The pass@k met-
                                                                ric is defined as the same in P-FOLIO (Han et al.,
We conduct several experiments based on the proposed            2024b): After sampling k proofs from the tested LLM,
PC-FOL dataset, aiming to answer the following re-              the pass@k represents the percentage of instances in
search questions: 1) Is there a performance gap for             which at least one generated proof follows the same
LLMs between the two types of FOL problems? 2) Are              reasoning process as the annotated proof. The verifica-
the proofs generated by LLMs correct?                           tion process is automatically checked by GPT-4o, and
                                                                the prompt templates are provided in Appendix D.

5.1      Experiment Setting                                     Models We employ both proprietary LLMs and open-
                                                                source LLMs in experiments. The proprietary LLMs in-
Experimental Tasks Based on PC-FOL dataset, we                  clude GPT-4o (OpenAI et al., 2024), GPT-4.1 (OpenAI,
conduct two types of experiments: Natural Language              2025a), o4-mini (OpenAI, 2025b). The open-source
FOL Reasoning and Proof Evaluation. The Natural                 LLMs tested in our experiments are Llama-3.3-70B
Language FOL Reasoning task aims to evaluate the rea-           (Grattafiori et al., 2024), deepseek (DeepSeek-AI et al.,
soning capabilities of selected LLMs, where the LLMs            2025b) and Qwen3 (Yang et al., 2025). More details
are given the premises and are asked to give the truth          are deferred to Appendix E.
value of the conclusion from the following three choices:
“True”, “False”, and “Unknown”. The prompt templates             5.2    Natural language FOL reasoning
used in this task are provided in Appendix D. The
Proof Evaluation task is designed to evaluate the cor-          We present the results of evaluating the natural lan-
rectness of the proofs generated by LLMs. For each              guage FOL reasoning capabilities of various LLMs
instance, the premises are provided, and the LLMs are           based on PC-FOL dataset in Tables 5. More experi-
tasked with generating natural language proofs along            mental results can be found in Appendix F.
with the corresponding truth value of the conclusion.
                                                                 Based on the results, we can observe that there are
We also conduct additional fine-tuning experiments on
                                                                 significant performance gaps between the linear-
the PC-FOL dataset, and the corresponding details are
                                                                 reasoning FOL problems and the proof-by-cases
presented in Appendix G.
                                                                 FOL problems across all experiments. For the
Metrics To evaluate the performance of the LLMs, we              GPT-4o model, while it achieves 85.13% accuracy
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving

          Table 6: Result of ROUGE metrics for few-shot prompting with GPT-4o on PC-FOL dataset.

                             Linear   Linear   Linear   Linear     Case       Case      Case      Case
                   #Shot
                             R-1      R-2      R-L      Acc        R-1        R-2       R-L       Acc
                    0-shot   43.56    29.24    31.67    85.13      59.05   36.73        34.37     51.66
                    5-shot   54.88    37.60    42.42    85.77      62.00   39.99        37.97     53.95
                   10-shot   55.98    38.50    43.23    86.36      62.16   40.36        38.57     55.73
                   20-shot   55.77    38.58    43.02    87.15      62.86   40.96        39.27     55.53
                   40-shot   55.96    38.74    43.11    87.94      63.38   41.20        39.76     57.91

on the 0-shot task for the PC-FOL linear-reasoning          and about 5% for case-based reasoning problems when
dataset, its accuracy on the proof-by-cases dataset is      the number of shots increases from 0 to 40. Besides,
34.05% lower. A similar trend is observed in the 3-shot     label accuracy shows a relative improvement of 5% in
task, where the accuracy for the linear-reasoning prob-     the 40-shot setting compared to the 0-shot baseline.
lems is 83.17%, compared to 55.58% for the proof-by-
cases problems. The DeepSeek-v3 model performs best         5.4     Manually Checking Proofs
overall but still exhibits a 12.92% gap, with 89.63% ac-
curacy on linear-reasoning problems and 76.71% on           In Section 5.2, we observe that LLMs exhibit low
proof-by-cases problems. On the PC-FOL-Replace              accuracy when solving proof-by-cases type FOL
dataset, we also observe a 1-5% accuracy gap com-           problems. Consequently, employing another LLM
pared to the PC-FOL dataset for each tested LLM.            to evaluate the correctness of the answers (e.g., the
                                                            Pass@k metric in Section 5.3), would likely introduce
5.3     Proof Evaluation                                    significant errors. To mitigate this issue, we further
                                                            conduct a manual experiment to evaluate the answers
Pass@k Evaluation                                           generated by the GPT-4o model. Specifically, in this
                                                            experiment, we utilize GPT-4o (web interactive version)
Table 7: Pass@k results for GPT-4o model on the             to generate a proof with a corresponding label for each
PC-FOL dataset.                                             problem in our PC-FOL dataset. These proofs are
                                                            then examined by a professional mathematician, who
      Model    k
                   PC-FOL             PC-FOL                categorized each instance into one of three categories:
                   Linear-Reasoning   Proof-by-Cases        Wrong Label with Wrong Proof, Correct Label with
               1        82.58             46.38             Wrong Proof, and Correct Label with Correct Proof.
               2        96.67             71.82             The distribution of results across these categories is
      GPT-4o   3        99.41             85.13             reported in Table 8.
               4        100.0             92.95
               5        100.0             95.50
                                                           Table 8: Proportions of the three answer categories
                                                           (round to two decimal places) of GPT-4o (web interac-
Table 7 presents the Pass@k results for GPT-4o on the      tive) on our PC-FOL dataset.
PC-FOL dataset. The Pass@k metric represents the
percentage of instances where at least one of k sampled                              PC-FOL               PC-FOL
                                                                   Category
proofs is deemed to match the expert-written proof by                                Linear-Reasoning     Proof-by-Cases
the evaluation LLM model.                                        Wrong Label
                                                                                         15.07%              45.79%
The results indicate that as k increases, the Pass@k             Wrong Proof
metric improves significantly. For example, on                   Correct Label
                                                                                          4.31%              28.18%
the linear-reasoning type problems, the Pass@k score             Wrong Proof
reaches 100% when k = 4, indicating that the evalua-             Correct Label
                                                                                         80.63%              26.03%
tion model believes there is at least one correct proof          Correct Proof
for every instance. For proof-by-case type problems,
                                                            We can now answer the research question “(2): Are
when k = 1, only 46.38% of instances are considered to
                                                            the proofs generated by LLMs correct?” based on
get a correct answer from GPT-4o, and this percentage
                                                            the results in Table 8, which indicates that for linear-
rises to 95.50% when k = 5, showcasing a substantial
                                                            reasoning problems, when the model assigns a cor-
metric increase.
                                                            rect label, the corresponding proof is also likely
Few-shot prompting Table 6 indicates that increas-          to be correct. However, for proof-by-cases problems,
ing the number of proof examples leads to improved          not only is the label accuracy only 54.21%, but fewer
performance. Specifically, the ROUGE scores improve         than half of these samples with the correct label actu-
by approximately 10% for linear reasoning problems          ally get a correct proof. Through our manual checking
                        Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


of the proofs, we identify four main reasons for the       to mathematical logic problems.
proof errors: misapplication of premises, misinterpre-
tation of disjunctive statements, mistakes in inductive    6.1    Reasoning Ability of LLMs for
and deductive reasoning, and semantic misunderstand-              Linear-Reasoning problem
ings. In particular, for proof-by-cases problems, the
predominant cause of incorrect proof is the misappli-      On the one hand, directly using the graphical model
cation of disjunctive statements, where the tested         (described in Section 3) can hardly define the linear
LLM often misunderstands exclusive disjunctions, or        reasoning ability of LLM. On the other hand, tradi-
fails to provide proofs that address separate scenarios.   tional analysis of neural-based NLP models typically
                                                           defines
                                                           Qn      the probability distribution as P [X1 , . . . , Xn ] =
5.5   Main Findings                                           i=1 [Xi |Context, X1 , . . . , Xi−1 ], where Xi repre-
                                                                 P
                                                           sents the i-th token of the output sequence, which offers
Below we summarize our main findings, which are the        limited explanatory power regarding the mathematical
answers of the research question (1).                      principles or underlying mechanisms of black-box neu-
                                                           ral models. To address this limitation, we propose a
For all tested LLMs, there is a huge perfor-               variant graphical model constructed upon the following
mance gap between Linear-Reasoning type in-                assumptions and definitions:
stances and Proof-by-Cases type instances. The
average accuracy performance gap between the two
                                                             1. Define each Xi as a proposition described in the
types of questions for different LLMs, as shown in
                                                                given premises.
Tables 5, is calculated as follows: GPT-4o (31.02%),
GPT-4.1 (18.69%), o3-mini (9.98%), Llama-3 (29.80%),         2. The             conditional              probability
Deepseek-V3 (13.21%), Qwen3-14B (23.44%). Through               P [Xi |Context, X1 , . . . , Xi−1 ] can be viewed
manual evaluation and considering the distribution of           as selecting the next proposition based on an
the number of premises (shown in Appendix A), we                augmented context.
found no evidence to suggest that this performance
gap is related to the number of premises. Instead,           3. Fixed the LLM as a function F .            Define
the performance gap is attributed to the fundamental            pF (Augmented Context) as the correctness per-
problem-solving methods required for linear-reasoning           centage of selecting the correct proposition from
problems and proof-by-cases problems.                           context. The values for different augmented con-
Lexical substitution has only a marginal effect                 texts are assumed to be the same, defined as pF .
on model performance. The average performance
difference between the PC-FOL and PC-FOL-Replace           Therefore, the generated proof with the process
for different LLMs is calculated as follows: GPT-4o        Qn= {X1 , . . . , Xn } has the form of P [X1 , . . . , Xn ] =
                                                           X
(0.98%), GPT-4.1 (2.84%), o3-mini (1.76%), Llama-3           i=1 P [Xi |Augment Context], and the probability of
(0.05%), Deepseek-V3 (3.91%), Qwen3-14B (2.69%).           generating the correct reasoning chain is pkF , if there
The only notable exception appears in Table 5, where       are k steps in the corrected proof.
Llama-3 shows an abnormal accuracy gap on the 0-shot       Based on the previous assumptions, we can prove the
proof-by-cases task. In general, the performance degra-    following theorem:
dation caused by lexical substitution can be attributed
to the inability of LLMs to correctly recognize the sub-   Theorem 6.1. Under previous assumptions, for a
stituted nouns. This difficulty arises because nouns in    LLM F , a linear-reasoning dataset D with the distri-
the PC-FOL-Replace dataset are randomly generated          bution PD of reasoning steps, the probability that the
                                                                                             ∞
alphabetic strings, which are unlikely to have appeared                                        pkF · PD (|X| = k),
                                                                                             P
                                                           LLM F can give a correct proof is
in the training corpora of any LLM.                                   |X|
                                                                                                 k=1
                                                           or EX∼PD [pF ].

6     Theoretical Analysis                                 The justification for the assumptions, together with
                                                           the complete proof of Theorem 6.1, are provided in
To explain the substantial performance gap exhibited       Appendix H. As a result, by using the distribution of the
between linear-reasoning problems and proof-by-cases       proof steps in the linear-reasoning part (Appendix J),
problems, we employ the probabilistic graphical            we can then calculate the probability pF , the accuracy
model to discuss theoretical approaches for analyzing      for getting the next step for different LLM F . For
the performance of LLMs on mathematical logic tasks,       example, since Table 8 shows that the correct proof
propose specific theoretical assumptions, and introduce    rate for GPT-4o over our dataset is 80.63%, by using
a variant of the probabilistic graphical model tailored    Theorem 6.1, we can calculate that pGP T −4o = 92.62%.
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving


                                                             Assuming that, for the i-th possible case, the rea-
                                                             soning chain for the given question is represented as
                                                                E
                                                             {Xi,1 , · · · , Xi,nE
                                                                                     i
                                                                                       }, and for the j-th impossible case, the
                                                             reasoning chain for the given question is represented
                                                             as {Xj,1NE                 NE
                                                                           , · · · , Xj,n  j
                                                                                             }. Under these definitions, the
                                                             proof should be the set {{Xj,1          NE             NE
                                                                                                         , · · · , Xj,n j
                                                                                                                          }∀case j ∈
                                                                         E                E
                                                             N E, {Xk,1 , · · · , Xk,ni }f or selected case k ∈ E},
                                                             where the k means that the k-th case of the set E
                                                             satisfies the given requisite of the question.
                                                             Therefore, based on the previous assumptions, we can
                                                             prove the following theorem:
                                                             Theorem 6.2. Under previous assumptions, for a
                                                             LLM F , a dataset D with the distribution PD of
                                                             the set of reasoning chains. Define pF,cases (X) as
                                                             the probability that the LLM can correctly identify all
                                                             the cases in X required for discussion, then the prob-
                                                             ability that the PLLM F can give P        a correct proof is
                                                                                     NE
                                                                                 i |Xi  |+|X N E |+           |XkE |
                                                                                                   selected k
                                                             P
                                                                pF,cases (X)·pF                                      ·PD (X =
                                                             {all{X N E }, selected{X E }})
Figure 2: Upper: The abstracted reasoning chain for
right side example of Table 2. Lower: The abstracted         If people define a correct proof as the set of all the
reasoning chain for a typical example that existing a        reasoning steps in different cases, even for the cases
contradiction in a subcase. The dotted line represents       that do not satisfy the requisite of the question, then
a possible case inferred from a certain premise and          the Theorem 6.2 will be simplified as
the previous steps, and the red double-headed arrow          Theorem 6.3. Under previous assumptions, for a
denotes the existence of a contradiction.                    LLM F , a dataset D with the distribution PD of the set
                                                             of reasoning chains. Then the probability that the LLM
                                                                                           ∞
6.2   Reasoning Ability of LLMs for                          F can give a correct proof is
                                                                                           P
                                                                                             pkF · PD (|X| +|X N E | =
      Proof-by-Cases problem                                                                         k=1
                                                                                 |X|+|X N E |
                                                             k), or EX∼PD [pF                   ].
We have shown the abstract reasoning chain for a
linear-reasoning example in Figure 1. However, for           From Theorems 6.2 and 6.3, we can identify two pri-
proof-by-cases questions, the abstract reasoning chain       mary factors leading to LLMs’ errors in proof-
is completely different. The upper part of Figure 2          by-cases problems: incorrect selection of cases (re-
shows an abstracted reasoning chain for the right side       flected by a low value of pF,cases ) and an excessive
example of Table 2, and the lower part shows an ab-          number of steps required to show the logical chains
stracted reasoning chain for an example that exists a        for each valid case (reflected by a large exponent k in
contradiction in one case. The original description of       pkF ). These theoretical findings align with the issues
the lower part example is deferred to Appendix H.2.          observed in our experimental results, demonstrating
In mathematical logic problem-solving, a standard            the reasonableness of our theoretical framework for the
proof for a proof-by-cases problem must comprise two         proof-by-cases problems.
parts: 1) Complete logical chains for all cases where
a contradiction arises, demonstrating that these cases       7     Limitation and Conclusion
are invalidated by the contradiction; and 2) for all
cases that satisfy the given requisite (e.g., “If A holds,   In this paper, we introduced the PC-FOL dataset, a
then xxxxxx.”), a corresponding logical deduction that       novel dataset for evaluating the FOL reasoning ca-
verifies the validity of the conclusion.                     pabilities of LLMs, which contains expert-annotated
                                                             instances under two types of FOL questions: linear-
Thus, the proof of proof-by-cases type problems should
                                                             reasoning and proof-by-cases. Although the scale of
be defined as a set of reasoning chain sets. Mathemat-
                                                             this dataset is limited compared to the extensive cor-
ically, suppose the set E contains the cases that are
                                                             pora typically used for LLM pretraining, the dataset
possible to exist based on the given premises, and the
                                                             can still be used for LLM evaluation.
set N E contains the cases that can not exist (there is
a contradiction in them) based on the given premises.        Extensive experiments involving widely-used LLMs
                        Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


revealed that while LLMs perform relatively well on        References
traditional linear reasoning FOL tasks, they struggle
significantly with problems requiring proof-by-cases       Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui
technique.                                                 Zhang, and Wenpeng Yin. Large language models for
                                                           mathematical reasoning: Progresses and challenges.
Finally, to explain this phenomenon, we proposed spe-      In Proceedings of the 18th Conference of the European
cific theoretical assumptions and designed a variant       Chapter of the Association for Computational Lin-
probabilistic graphical model specifically for FOL prob-   guistics: Student Research Workshop, pages 225–237,
lems. Note that, in our assumptions, the probability       2024.
of a correct single-step inference is set as constant,
which simplifies the inference process of complex LLM      Aida Amini, Saadia Gabriel, Shanchuan Lin, Rik
models.                                                    Koncel-Kedziorski, Yejin Choi, and Hannaneh Ha-
                                                           jishirzi. MathQA: Towards interpretable math word
This work highlighted the limitations of current LLMs      problem solving with operation-based formalisms. In
and underscores the need for robust methods that           Proceedings of the 2019 Conference of the North Amer-
can handle a broader spectrum of real-world problem-       ican Chapter of the Association for Computational
solving, particularly case-based reasoning.                Linguistics, pages 2357–2367, 2019.
                                                           Mark Chen, Jerry Tworek, Heewoo Jun, and et al.
                                                           Evaluating large language models trained on code.
                                                           arXiv, arXiv:2107.03374, 2021.
                                                           Hyung Won Chung, Le Hou, Shayne Longpre, and
                                                           et al. Scaling instruction-finetuned language models.
                                                           arXiv, arXiv:2210.11416, 2022.
                                                           Peter Clark, Oyvind Tafjord, and Kyle Richardson.
                                                           Transformers as soft reasoners over language. In Pro-
                                                           ceedings of the Twenty-Ninth International Joint Con-
                                                           ference on Artificial Intelligence, IJCAI-20, pages
                                                           3882–3890, 2020.
                                                           Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                           and et al. Training verifiers to solve math word prob-
                                                           lems. arXiv, arXiv:2110.14168, 2021.
                                                           DeepSeek-AI, Daya Guo, Dejian Yang, and et al.
                                                           Deepseek-r1: Incentivizing reasoning capability in llms
                                                           via reinforcement learning. arXiv, arXiv:2501.12948,
                                                           2025a.
                                                           DeepSeek-AI, Aixin Liu, Bei Feng, and et al. Deepseek-
                                                           v3 technical report. arXiv, arXiv:2412.19437, 2025b.
                                                           Shizhe Diao, Pengcheng Wang, Yong Lin, Rui Pan,
                                                           Xiang Liu, and Tong Zhang. Active prompting with
                                                           chain-of-thought for large language models. In Pro-
                                                           ceedings of the 62nd Annual Meeting of the Association
                                                           for Computational Linguistics, pages 1330–1350, 2024.
                                                           Aaron Grattafiori, Abhimanyu Dubey, Abhinav
                                                           Jauhri, and et al. The llama 3 herd of models. arXiv,
                                                           arXiv:2407.21783, 2024.
                                                           Thomas C. Hales. A proof of the kepler conjecture.
                                                           Annals of Mathematics, 162:1065–1185, 2005.
                                                           Simeng Han, Hailey Schoelkopf, Yilun Zhao, and
                                                           et al. Folio: Natural language reasoning with first-
                                                           order logic. In Proceedings of the 2024 Conference on
Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving


Empirical Methods in Natural Language Processing         OpenAI. Openai o1 system card, 2024. URL https:
(EMNLP), pages 22017–22031, 2024a.                       //openai.com/index/openai-o1-system-card/.

Simeng Han, Aaron Yu, Rui Shen, and et al. P-            OpenAI. Introducing gpt-4.1 in the api, 2025a. URL
folio: Evaluating and improving logical reasoning with   https://openai.com/index/gpt-4-1/.
abundant human-written reasoning chains. In Find-
ings of the Association for Computational Linguistics:   OpenAI.    Introducing openai o3 and o4-mini,
EMNLP, pages 16553–16565, 2024b.                         2025b.       URL https://openai.com/index/
                                                         introducing-o3-and-o4-mini/.
David Hilbert and Wilhelm Ackermann. Grundzüge
der theoretischen Logik (Principles of Mathematical      OpenAI, Aaron Hurst, Adam Lerer, and et al. Gpt-4o
Logic). 1928.                                            system card. arXiv, arXiv:2410.21276, 2024.

Mirzadeh Iman, Alizadeh Keivan, Shahrokhi Hooman,        Mihir Parmar, Nisarg Patel, Neeraj Varshney, Mut-
Tuzel Oncel, Bengio Samy, and Farajtabar Mehrdad.        sumi Nakamura, Man Luo, Santosh Mashetty,
Gsm-symbolic: Understanding the limitations of           Arindam Mitra, and Chitta Baral. LogicBench: To-
mathematical reasoning in large language models.         wards systematic evaluation of logical reasoning ability
arXiv, arXiv:2410.05229, 2024.                           of large language models. In Proceedings of the 62nd
                                                         Annual Meeting of the Association for Computational
Yuliang Ji, Jie Ma, Juan Yan, and Xingxing Yu. On        Linguistics, pages 13679–13707, 2024.
problems about judicious bipartitions of graphs. Jour-
nal of Combinatorial Theory, Series B, 139:230–250,      Shuai Peng, Ke Yuan, Liangcai Gao, and Zhi Tang.
2019.                                                    Mathbert: A pre-trained model for mathematical for-
                                                         mula understanding. arXiv, arXiv:2105.00377, 2021.
Cezary Kaliszyk, François Chollet, and Christian
Szegedy. Holstep: A machine learning dataset             Abulhair Saparov and He He. Language models are
for higher-order logic theorem proving. In Inter-        greedy reasoners: A systematic formal analysis of
national Conference on Learning Representations          chain-of-thought. In International Conference on
(ICLR), 2017.                                            Learning Representations (ICLR), 2023.

Cobbe Karl, Kosaraju Vineet, Bavarian Mohammad,          Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao,
Chen Mark, Jun Heewoo, Kaiser Lukasz, Plappert           Hao He, and Yaohui Jin. Diagnosing the first-order
Matthias, Tworek Jerry, Hilton Jacob, Nakano Rei-        logical reasoning ability through LogicNLI. In Proceed-
ichiro, Hesse Christopher, and Schulman John. Train-     ings of the 2021 Conference on Empirical Methods in
ing verifiers to solve math word problems. arXiv,        Natural Language Processing (EMNLP), pages 3738–
arXiv:2110.14168, 2021.                                  3747, 2021.

Takeshi Kojima, Shixiang Shane Gu, Machel Reid,          Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and
Yutaka Matsuo, and Yusuke Iwasawa. Large language        Thang Luong. Solving olympiad geometry without
models are zero-shot reasoners. In Proceedings of        human demonstrations. Nature, 625:476–482, 2024.
International Conference on Neural Information Pro-
                                                         Ke Wang, Houxing Ren, Aojun Zhou, Zimu Lu, Sichun
cessing Systems (NeurIPS), pages 22199–22213, 2022.
                                                         Luo, Weikang Shi, Renrui Zhang, Linqi Song, Mingjie
Chin-Yew Lin. ROUGE: A package for automatic eval-       Zhan, and Hongsheng Li. Mathcoder: Seamless code
uation of summaries. In Text Summarization Branches      integration in LLMs for enhanced mathematical rea-
Out, pages 74–81. Association for Computational Lin-     soning. In International Conference on Learning Rep-
guistics, 2004.                                          resentations (ICLR), 2024.

Ilya Loshchilov and Frank Hutter. Sgdr: Stochas-         Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh
tic gradient descent with warm restarts. arXiv,          Hajishirzi, Yejin Choi, and Kyunghyun Cho. Natu-
arXiv:1608.03983, 2016.                                  ralproofs: Mathematical theorem proving in natural
                                                         language. In Proceedings of International Conference
Ilya Loshchilov and Frank Hutter. Decoupled weight       on Neural Information Processing Systems (NeurIPS),
decay regularization. arXiv, arXiv:1711.05101, 2017.     2021.

Arindam Mitra, Hamed Khanpour, Corby Rosset,             Jian Wu, Linyi Yang, Zhen Wang, Manabu Okumura,
and Ahmed Awadallah. Orca-math: Unlocking the            and Yue Zhang. Cofca: A step-wise counterfactual
potential of slms in grade school math. arXiv,           multi-hop qa benchmark. In International Conference
arXiv:2402.14830, 2024.                                  on Learning Representations (ICLR), 2024.
                       Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


An Yang, Baosong Yang, Binyuan Hui, and et al.              (b) All the training details (e.g., data splits, hy-
Qwen2 technical report. arXiv, arXiv:2407.10671,                perparameters, how they were chosen). [Yes]
2024a.                                                      (c) A clear definition of the specific measure or
An Yang, Baosong Yang, Beichen Zhang, and et al.                statistics and error bars (e.g., with respect to
Qwen2.5 technical report. arXiv, arXiv:2412.15115,              the random seed after running experiments
2024b.                                                          multiple times). [Yes]
                                                            (d) A description of the computing infrastructure
An Yang, Anfeng Li, Baosong Yang, and et al. Qwen3              used. (e.g., type of GPUs, internal cluster, or
technical report. arXiv, arXiv:2505.09388, 2025.                cloud provider). [Yes]
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-           4. If you are using existing assets (e.g., code, data,
mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan            models) or curating/releasing new assets, check if
Prenger, and Anima Anandkumar. LeanDojo: Theo-              you include:
rem proving with retrieval-augmented language mod-
els. In Proceedings of International Conference on          (a) Citations of the creator If your work uses
Neural Information Processing Systems (NeurIPS),                existing assets. [Yes]
2023a.                                                      (b) The license information of the assets, if appli-
                                                                cable. [Yes]
Zhen Yang, Ming Ding, Qingsong Lv, Zhihuan Jiang,
                                                            (c) New assets either in the supplemental material
Zehai He, Yuyi Guo, Jinfeng Bai, and Jie Tang. Gpt
                                                                or as a URL, if applicable. [Yes]
can solve mathematical problems without a calculator.
arXiv, arXiv:2309.03241, 2023b.                             (d) Information about consent from data provider-
                                                                s/curators. [Not Applicable]
Junchi Yu, Ran He, and Zhitao Ying. Thought propa-          (e) Discussion of sensible content if applicable,
gation: An analogical approach to complex reasoning             e.g., personally identifiable information or of-
with large language models. In International Confer-            fensive content. [Not Applicable]
ence on Learning Representations (ICLR), 2024.
                                                         5. If you used crowdsourcing or conducted research
Checklist                                                   with human subjects, check if you include:
                                                            (a) The full text of instructions given to partici-
 1. For all models and algorithms presented, check if
                                                                pants and screenshots. [Not Applicable]
    you include:
                                                            (b) Descriptions of potential participant risks,
    (a) A clear description of the mathematical set-            with links to Institutional Review Board (IRB)
        ting, assumptions, algorithm, and/or model.             approvals if applicable. [Not Applicable]
        [Yes]                                               (c) The estimated hourly wage paid to partici-
    (b) An analysis of the properties and complexity            pants and the total amount spent on partici-
        (time, space, sample size) of any algorithm.            pant compensation. [Not Applicable]
        [Not Applicable]
    (c) (Optional) Anonymized source code, with
        specification of all dependencies, including
        external libraries. [Yes]
 2. For any theoretical claim, check if you include:
    (a) Statements of the full set of assumptions of
        all theoretical results. [Yes] See Section 6.
    (b) Complete proofs of all theoretical results.
        [Yes] See Appendix H.
    (c) Clear explanations of any assumptions. [Yes]
        See Appendix H.
 3. For all figures and tables that present empirical
    results, check if you include:
    (a) The code, data, and instructions needed to re-
        produce the main experimental results (either
        in the supplemental material or as a URL).
        [Yes] See Appendix B.3.
                           Paper Submission to AISTATS 2026:
                                Supplementary Materials



A     Distribution of number of Premises

The distribution of the number of premises in each instance of the PC-FOL dataset is shown in Figure 3. The
other part, PC-FOL-Replace, has almost the same distribution as the PC-FOL dataset. Therefore, we do not list
the same image multiple times.




Figure 3: The distribution of the number of premises in each instance of the PC-FOL dataset. Blue color
represents the distribution of the proof-by-case type problems, and the yellow color represents the distribution of
the linear reasoning type problems.


B     Dataset Description

B.1   Data collection process

Most instances in our PC-FOL dataset come from the instances in the FOLIO (Han et al., 2024a) dataset with
little modifications, or from the exercises or homework in some mathematical logic courses.
Through carefully and manually checking each instance in FOLIO, we utilize the data that is logically sound
and has the correct label. We re-write some instances which have logical issues, and re-label those data with the
wrong label. We also utilize the exercises or homework in mathematical logic courses. By modifying the exercises
in some lecture notes, or re-writing the homework from FOL formulas to natural language, many instances in the
                         Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


proof-by-case category have been collected in our dataset.
To make the logical reasoning complicated enough, the number of premises in each instance is at least 4. Unlike
the linear-reasoning problems shown in previous work, the reasoning depth of proof-by-cases problems can not
be defined well and the reason is given in Appendix C. Therefore, we show the distribution of the number of
premises in each instance instead. The figure of the distribution is shown in Appendix A.
For each instance, we provide a natural language answer, and the answers are all written by our professional
annotators.
The quality control process is shown in Appendix B.2.

B.2     Quality control of PC-FOL dataset

Dataset Annotation (1) To ensure that our dataset is annotated with high precision and professionalism, our
annotators are all professional mathematicians with a math PhD degree and have taken at least one graduate-level
course related to mathematical logic or discrete math. (2) Our annotators wrote the premises and the conclusions
by using the same format as the FOLIO dataset. (3) Our annotators are native English speakers, or have the
ability to write professional academic English.
Natural Language Quality Since our annotators are professional mathematicians, we can make sure that the
sentences in our dataset, especially the natural language answers of the instances, have the same writing style as
the answers of exercises from graduate-level mathematics textbooks. Besides, all the sentences are checked with
two grammar checking tools: a traditional software called Grammarly, and a LLM-based software called Writefull.
Cross checking Each instance and its answer are double-checked by two annotators.

B.3     Anonymous Link

We provide an anonymous link for downloading our PC-FOL dataset: https://www.kaggle.com/datasets/
c425f3c00b279f2b843a71456b9ecc9ddba8c0d12b9f83deb6bd6b0435db85c6.

C      Explanation about the reasoning depth

In this section, we give an example to show why we believe that the reasoning depth of proof-by-cases FOL
question can not be defined well.
Suppose that we have such premises

    • If C holds, then either A or B holds.
    • If C holds and B holds, then A holds.
    • If C holds and B does not hold, then A does not hold.

And a statement “C holds”.
To evaluate whether the statement is true or false, the standard way is to consider two cases:
Case 1: C holds.
Case 2: C does not hold.
In case 1, since C holds, consider two subcases:
Case 1.1 A holds. Then by premise 1, B does not hold. By premise 3, A does not hold, which makes a contradiction.
Case 1.2 A does not hold. Then by premise 1, B holds. By premise 2, A holds, which makes a contradiction too.
Since both subcases are impossible, case 1 is impossible.
When attempting to construct a reasoning chain for Case 1, one may observe the following process:
(A holds)
→ premise 1, (B does not hold)
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving


→ premise 3, (A does not hold)
→ premise 1, (B holds)
→ premise 2, (A holds)
→ ... (cycle continues)
As a result, we obtain a cyclic graph, rather than a typical linear chain of standard reasoning questions. Because
the length of the longest path in a cyclic graph is not well-defined (especially in graph theory), it is unusual to
define the reasoning depth for such FOL questions. Previous work ignored this situation and they may give the
depth as the depth in one case.

D     Prompt used in Experiments

The prompts used in our experiments are shown below. The templates are designed from the ideas of several
published FOL reasoning papers.

D.1   Prompts used for generating proofs and labels

Reasoning with proof version:
Using deductive reasoning, find out the truth values of the conclusions based on the premises. The truth
value can be True, False or Uncertain. First show the reasoning process, and then output the truth value in
the format of "Truth value: ".
Premises: nl_premises
Conclusion: conclusion
Multi-shot version:
Here are some examples of deductive reasoning problems and their correct truth values:
few_shot_examples
Now, using deductive reasoning, find out the truth values of the conclusions based on the premises. The
truth value can be True, False or Uncertain. First show the reasoning process, and then output the truth
value in the format of "Truth value: ".
Premises: nl_premises
Conclusion: conclusion
Chinese version:
使用演绎推理，找出结论的真值。真值可以是“真”、“假”或“不确定”。首先展示推理过程，然后以“真值:
”的格式输出真值。
前提: nl_premises
结论: conclusion
Label-only version:
Find out the truth values of the conclusions based on the premises. The truth value can be True, False or
Uncertain. Output the truth value in the format of "Truth value: " directly without any reasoning process.
Premises: nl_premises
Conclusion: conclusion

D.2   Prompts used for proof evaluation

Given a deductive reasoning question, demonstrate whether the two reasoning chains are semantically
similar and follow the same reasoning path to derive the final answer. After your explanations, output your
decision in the format of "Decision: ". Your decision should be either Yes or No.
Premises: nl_premises
Conclusion: conclusion
Reasoning chain A: reasoning_chain_a
Reasoning chain B: reasoning_chain_b
                        Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


E     Details of Experiments

In this section, we show the details of our experiments in Section 5.

E.1    LLM Model version and cost

We utilized API services provided by commercial companies to access these LLMs via the cloud services. The
versions used are as follows.

    • GPT-4o: GPT-4o-2024-11-20

    • GPT-4.1: GPT-4.1-2025-04-14

    • Llama-3-70B: Llama-3.3-70B-Instruct

    • Deepseek-V3: Deepseek-V3-2025-03-24

We use the default parameter to request all of the responses of these models. The total amount of the expenditure
is approximately $600.

E.2    Natural language FOL reasoning

For the PC-FOL dataset, we evaluate zero-shot (0-shot) and three-shot (3-shot) tasks on all tested LLMs. The
few-shot examples are randomly selected from the dataset and include corresponding manually written proofs,
each with a different story ID.
For the PC-FOL-Replace dataset, we similarly evaluate 0-shot and 3-shot tasks on all tested LLMs. The few-shot
examples are randomly drawn from the PC-FOL dataset, accompanied by corresponding manually written proofs,
and assigned a different story ID.

E.3    Proof Evaluation

Pass@k Evaluation
In this experiment, we sample k different proofs by GPT-4o model.
Few-shot prompting
In this experiment, the few-shot prompting results are generated by GPT-4o. The evaluation LLM model in the
ROUGE metric processing is set as GPT-4o.


F     Experimental results for more models

F.1    Different Hyperparameters for Qwen3 Model

In this section, we present the accuracy results for Qwen3 (Yang et al., 2025) models with different hyperparameters
and Deepseek-R1 models. Table 9 shows the accuracy results of zero-shot and few-shot prompting on PC-FOL
dataset.

F.2    Different random seeds or temperatures

In this section, we present additional experiments evaluating the GPT-4o model on our dataset. Table 10 and
Table 11 show the results of the experiments across different random seeds and temperatures. These experiments
demonstrate that varying random seeds or temperatures slightly affects the observed performance gap between
linear-reasoning and proof-by-cases instances.
Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving

Table 9: Logical reasoning accuracy results of zero-shot and few-shot prompting on English PC-FOL dataset.

                                  PC-FOL               PC-FOL            PC-FOL-Replace           PC-FOL-Replace
                Model
                                  Linear reasoning     proof-by-case     Linear reasoning         proof-by-case
            GPT-4o 0-shot                 85.13            51.08                84.34                 51.66
            GPT-4o 3-shot                 83.17            55.58                82.39                 52.64
            GPT-4.1 0-shot                89.24            69.86                88.45                 63.80
            GPT-4.1 3-shot                86.30            71.23                84.34                 68.69
            o4-mini 0-shot                90.80            79.84                88.26                 77.89
            o4-mini 3-shot                90.02            80.43                88.45                 79.45
         Llama 3-70B 0-shot               80.63            46.77                79.84                 50.88
         Llama 3-70B 3-shot               83.56            54.21                80.63                 53.62
         Deepseek-V3 0-shot               89.63            76.71                86.69                 73.39
         Deepseek-V3 3-shot               90.02            77.10                85.71                 72.02
         DeepSeek-R1 0-shot               91.39            82.16                86.30                 80.04
         DeepSeek-R1 3-shot               89.82            82.00                87.08                 80.04
          Qwen3-4B 0-shot                 85.32            61.45                83.76                 55.77
          Qwen3-4B 3-shot                 82.97            64.97                81.60                 60.67
          Qwen3-8B 0-shot                 84.93            61.64                84.93                 59.69
          Qwen3-8B 3-shot                 86.11            63.60                86.69                 60.86
          Qwen3-14B 0-shot                87.28            63.60                84.54                 59.10
          Qwen3-14B 3-shot                89.04            66.34                86.89                 64.97
        Qwen3-4B-think 0-shot             87.67            74.56                85.52                 72.21
        Qwen3-4B-think 3-shot             88.85            75.15                86.89                 72.21
        Qwen3-8B-think 0-shot             89.43            77.30                84.93                 73.97
        Qwen3-8B-think 3-shot             90.22            80.63                88.45                 75.54
        Qwen3-14B-think 0-shot            91.39            80.82                87.87                 77.10
        Qwen3-14B-think 3-shot            91.59            79.06                85.91                 76.52




  Table 10: Evaluating the GPT-4o model on PC-FOL dataset. Random seeds of the model are fixed as 1.

                                            PC-FOL                 PC-FOL
                                                                                        PC-FOL
                                            Linear-Reasoning       Proof-by-Cases
                                                                                        Acc. Gap
                                            Accuracy               Accuracy
                         Temperature 0            82.39                54.99             27.40↓
                        Temperature 0.5           83.17                55.58             27.59↓
                         Temperature 1            82.39                52.45             29.94↓
                             Average              82.65                54.34             28.31↓
                         Standard
                                                  0.4503               1.6632              -
                         Deviation




  Table 11: Evaluating the GPT-4o model on PC-FOL dataset. Temperatures of the model are fixed as 1.

                                            PC-FOL                 PC-FOL
                                                                                        PC-FOL
                                            Linear-Reasoning       Proof-by-Cases
                                                                                        Acc. Gap
                                            Accuracy               Accuracy
                        Random seed 1             82.39                52.45             29.94↓
                        Random seed 11            84.15                52.25             31.90↓
                        Random seed 22            82.19                48.73             33.46↓
                             Average              82.91                51.14             31.77↓
                         Standard
                                                  1.0785               2.0924              -
                         Deviation
                         Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


G     Fine-tuning Results

G.1   Settings

To evaluate the impact of proof-by-case data on improving reasoning capabilities, we train our models on two
distinct dataset variants: one includes expert proofs in the completion block, while the other contains only
ground-truth labels as target answers. The datasets are split by 70%/15%/15% as mentioned in Section 5.
We fine-tune an encoder-decoder model, Flan-T5-large(Chung et al., 2022), alongside 2 LLMs, including Llama-
3.1-8B-Instruct(Grattafiori et al., 2024) and Qwen3-0.6B(Yang et al., 2024a,b). For the Flan-T5-large model, we
conduct training on a single NVIDIA A100 GPU with a batch size of 8 and a learning rate of 1e-4.
For the remaining LLMs, we adopt a learning rate of 5e-5. Specifically, we train Llama3-8B and Qwen3-0.6B on 8
and 4 NVIDIA A800 GPUs, respectively, maintaining a consistent batch size of 16 across all experiments.
All the fine-tuning experiments utilize the AdamW optimizer (Loshchilov and Hutter, 2017) with a cosine annealing
learning rate scheduler (Loshchilov and Hutter, 2016) and a warm-up ratio of 10% during training. Models are
trained for 3 epochs.

G.2   Results and Analysis

Table 12 shows the fine-tuning results by using our PC-FOL dataset.
Flan-T5 exhibits consistent performance gains, while the accuracy improvement across LLMs ranges from 4% to
9%. However, we also observe a decline in label accuracy, where proof-by-case performance on Qwen3-0.6B even
decreased by 6.58%, in the with proof setting after fine-tuning, and the validation loss suggests overfitting.
To further investigate this unexpected phenomenon, we conduct an experiment where we train Qwen3-0.6B on
the linear reasoning portion of the data and evaluate it on the proof-by-case portion—and vice versa. The results
are shown in Table 13.
Our findings reveal that training on linear proof tokens negatively impacts performance in proof-by-case problems
, whereas models trained on proof-by-case data show significant improvement in simpler linear reasoning tasks.
This provides a plausible explanation for the lower proof-by-case accuracy in fine-tuned models: when trained
on mixed data, models tend to prioritize easily learnable patterns for simpler problems, which may hinder their
ability to reason deeply in more complex scenarios.
Conversely, when proof procedures are omitted, models appear to "learn" label prediction superficially without
truly "understanding" the underlying reasoning.

Table 12: Fine-tuning results (Label Accuracy in %) of LLMs trained on the full set of PC-FOL dataset and
tested on the test set of Case/Linear.

                                                 PC-FOL w/ proof                 PC-FOL w/o proof
              Model            w/ SFT
                                          Linear reasoning proof-by-case   Linear reasoning proof-by-case
                                 Yes          47.37↑           35.53↑          57.89↑           47.37↑
           Flan-T5-large
                                 No           46.05             30.26           43.42            36.84
                                 Yes          73.68↑           48.68↓          59.21↑           46.05↑
       Llama-3.1-8B-Instruct
                                 No           64.47             50.00           57.89            40.79
                                 Yes          61.84↑           32.89↓          40.79-           36.84↑
            Qwen3-0.6B
                                 No           57.89             39.47          40.79             32.89



H     Proofs of the Theorems

H.1   Proof of Theorem 6.1 for Linear-Reasoning problem

Recall the assumptions and definitions:
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving

Table 13: Fine-tuning results of Qwen3 trained on the Linear/Case of PC-FOL dadaset and tested on the test set
of Case/Linear.

                                               PC-FOL w/ proof                    PC-FOL w/o proof
              Model        SFT Data
                                        Linear reasoning proof-by-case      Linear reasoning proof-by-case
                             Linear             -               36.84              -               47.37
            Qwen3-0.6B        Case            72.37               -              51.32               -
                              Null            57.89             39.47            40.79             32.89


 1. Define each Xi as a proposition described in the given premises.
 2. The conditional probability P [Xi |Context, X1 , . . . , Xi−1 ] can be viewed as selecting the next proposition
    based on the augmented context.
 3. Fixed the LLM as a function F . Define pF (Augmented Context) as the correctness percentage of selecting
    the correct proposition from context. The values for different augmented contexts are assumed to be the
    same, defined as pF .

First, we give the explanations of the assumptions, and the reasons why these assumptions can hold.

H.1.1    Define each Xi as a proposition described in the given premises.

Traditional analysis  Qn for the neural-based NLP models directly considered the probability distribution as
P [X1 , . . . , Xn ] = i=1 P [Xi |Context, X1 , . . . , Xi−1 ]. Although it is reasonable for analyzing LLMs, this method
can not reveal the structure of one proposition (for example, “Grass is green”, “One is not a computer”) in a
generated sentence.
Therefore, to emphasize the logical relationships between the propositions themselves rather than the specific
meaning of each word, we define Xi as a proposition in the given premises. Under this definition, various
equivalent natural language expressions can be represented by the same Xi , such as "Xi is true" and "the truth
value of Xi is 1."

H.1.2    The conditional probability P [Xi |Context, X1 , . . . , Xi−1 ] can be viewed as selecting the next
         proposition based on the augmented context.

That is, we assumed that, for any prompt, with any variant of the sentence structure, which includes the needed
context (the full given premises, the previous reasoning steps, the previous state, asking for the next reasoning
step, etc.), the distribution of selecting the next proposition for the LLM is the same.
For example, suppose we have the premise ‘A is true, then B is true’, and we have the fact (or in previous steps)
that ‘A is true’, and we want to ask the LLM for the next step or if B is true. The input can be “Suppose we
have a premise ‘A is true, then B is true’, and we know that ‘A is true’, what can we find based on these facts?”,
or “We have already known that ‘A is true, then B is true’, and the previous theorem shows ‘A is true’, will ‘B’
be a correct proposition?”.
Under this assumption, the augmented context contains all the needed information for the next-step reasoning.

H.1.3    Fixed the LLM as a function F . Define pF (Augmented Context) as the correctness
         percentage of selecting the correct proposition from context. The values for different
         augmented contexts are assumed to be the same, defined as pF .

This assumption is based on a basic concept of a well-trained LLM: when giving full premises and the previous
state, asking for the next reasoning step (must be linear connectivity), the accuracy of selecting the next step
should be almost the same. Since all the training data are selected randomly and batch-wise, a well-trained LLM
has such property theoretically.

H.1.4    Proof

Based on the previous assumptions, we can prove the theorem 6.1:
                         Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


Under previous assumptions, for a LLM F , a linear-reasoning dataset D with the distribution PD of reasoning
                                                                  ∞
                                                                                                 |X|
steps, the probability that the LLM F can give a correct proof is   pkF · PD (X = k), or EX∼PD [pF ]
                                                                  P
                                                                             k=1

                                                                                     Qn
Proof. From definition 1, the probabilistic graphical model P [X1 , . . . , Xn ] = i=1 P [Xi |pa(Xi )] can be re-written
as
                                                      n
                                                      Y
                               P [X1 , . . . , Xn ] =   P [Xi |Context, X1 , · · · , Xi−1 )]                          (1)
                                                      i=1

for proposition Xi , and a linear-reasoning type step-by-step proof X1 → X2 → · · · → Xn .
                                                                         Qn
Then, by definition 2, the formula has the form of P [X1 , . . . , Xn ] = i=1 P [Xi |Augmented Context], where
“Augmented Context" represents a input with full premises and previous state.
Consequently, by premise 3, since we assume that all the state transition has the same accuracy, we can get the
probability formula of generating correct proof sequence X1 , . . . , Xn as
                                                           n
                                                           Y
                                  P [X1 , . . . , Xn ] =         P [Xi |Augmented Context]
                                                           i=1
                                                           Yn
                                                     =           pF (Augmented Context)
                                                           i=1                                                       (2)
                                                           Yn
                                                     =           pF
                                                       i=1
                                                     = pnF

As a result, when given a linear-reasoning dataset D with the distribution PD of reasoning steps, the probability
that the LLM F can give a correct proof is
                                 1 X
 Pdata∼D (correct proof ) =          P (correct proof f or datai )
                                |D|
                                       |D|
                               1 X
                            =      P (Xi,1 , . . . , Xi,ni )
                              |D|
                                       |D|
                               1 X ni
                            =     pF ( ni represents the number of reasoning steps)
                              |D|
                                       |D|
                                  ∞
                               1 X k
                            =       pF · Nk (Nk represents the number of instances need k steps to prove)
                              |D|
                                      k=1
                                ∞
                                X             Nk
                            =         pkF ·
                                              |D|
                                k=1
                                X∞
                            =         pkF · PD (X = k)
                                k=1
                                              |X|
                            = EX∼PD [pF ]
                                                                                                                     (3)



By using the theorem 6.1, and using the distribution of the proof steps in our dataset (shown in Appendix J),
we can calculate the probability pF , the accuracy for getting the next step for different LLM F . Table 1 shows
that the correct proof rate for GPT-4o over our dataset is 80.63%, by using Theorem 6.1, we can calculate
that pGP T −4o = 92.62%. Thus, the probability of GPT-4o generating a correct proof for a linear-reasoning
mathematical logic problem with k steps is estimated by 0.9262k .
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving


We compare the ground truth of the correctness ratio and the estimated correctness ratio 0.9262k in Figure 4.
In this Figure, we can find that, for the same number of proof steps,the estimated correctness ratio is almost
the same as the ground truth value. Therefore, we can conclude that our theory is suitable for analyzing the
reasoning ability for LLM over linear-reasoning mathematical logic problems.




Figure 4: Comparison between the ground truth of the correct proof ratio and the estimated correctness ration
over the PC-FOL Linear-Reasoning dataset.


H.2   Proof of Theorems for Proof-by-Cases problem

We give two examples to show the structure of the standard proof-by-cases problem.




Figure 5: Left: The abstracted reasoning chain for right side example of Table 2. Right: The abstracted
reasoning chain for a typical example that existing a contradiction in a subcase.

The first is the example shown in the right side of Table 2. The premises of the example are:

  • Any person that is tall does not major in physics.
  • All people who are not tall study quantum computing.
                                Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


  • All students major in math or physics.

  • If a person majors in math, then the person studies algebraic geometry.

  • If a person majors in math, then the person does not study quantum computing.

  • Billy is a student who studies algebraic geometry.

When drawing the reasoning chain of this example, we define S as the proposition "Billy is a student, and is a
person", A as "Billy majors in math", B as "Billy studies quantum computing", C as "Billy is tall", D as "Billy
majors in physics", and E as "Billy studies algebraic geometry." Thus, the reasoning chain can be drawn as the
left part in Figure 5.
Another example we call it "subcase-contradiction", since there exists a contradiction when trying to get the
truth value of some propositions in a subcase. The premises of the example are:

  • A neuroimaging technique is either an invasive neuroimaging technique or a noninvasive neuroimaging
    technique.

  • All noninvasive neuroimaging techniques provide a spatial resolution of brains.

  • If a technique provides a spatial resolution of brains, then it is a measurement of brain activity.

  • All measurements of brain activity are used by neuroscience researchers.

  • FMRI is either a measurement of brain activity or a noninvasive neuroimaging technique.

  • FMRI is a neuroimaging technique.

When drawing the reasoning chain of this example, we define S as the proposition "FMRI is a neuroimaging
technique", A as "FMRI is an invasive neuroimaging technique", B as "FMRI is a measurement of brain activity",
C as "FMRI provides a spatial resolution of brains", and D as "FMRI is used by neuroscience researchers". Thus,
the reasoning chain can be drawn as the right part in Figure 5.
Recall the assumption that, for the i-th possible case, the reasoning chain for the given question is repre-
sented as {Xi,1 E              E
                    , · · · , Xi,n i
                                     }, and for the i-th possible case, the reasoning chain for the given question is repre-
sented as {Xj,1 , · · · , Xj,nj }. Under these definitions, the proof should be the set {{Xi,1
                NE               NE                                                                NE            NE
                                                                                                      , · · · , Xi,ni
                                                                                                                      }∀case i ∈
N E, {Xk,1 , · · · , Xk,ni }f or selected case k ∈ E}, where the k are means that the k-th case of the set E satisfies
        E                E

the given requisite of the question. Now we try to prove the Theorem 6.2 and 6.3.

H.2.1       Proof of Theorem 6.2

Recall the theorem: Under previous assumptions, for a LLM F , a dataset D with the distribution PD of
the set of reasoning chains. Define pF,cases as the probability that the LLM can correctly identify    all the
cases required for discussion, then the probability that the LLM F can give a correct proof is
                                                                                               P
                                                                                                 pF,cases (X) ·
         NE
            |+|X N E |+           |XkE |
 P                         P
     i |Xi
pF                     selected k
                                           · PD (X = {all{X N E }, selected{X E }})

Proof. From the proof of Theorem 6.1, we have proven that for a linear-reasoning sequence Xi,1 , . . . , Xi,ni ,
the probability of generating such a sequence correctly is pnFi . Thus, to generate a proof with propositions
    NE
{{Xi,1            NE
       , · · · , Xi,n i
                                          E
                        }∀case i ∈ N E, {Xk,1            E
                                              , · · · , Xk,n i
                                                               }f or selected case k ∈ E}, the number of reasoning steps
should be                                 X                               X
                                               |XiN E | + |X N E | +            |XkE |.
                                                    i                    selected k


Note that in order to show the cases in set N E are impossible to exist, the proof should add an extra reasoning
step to find the contradiction in such cases. That is the reason why we add |X N E | in the number of reasoning
steps.
 Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving


Hence, we have



                                1 X
Pdata∼D (correct proof ) =          P (correct proof f or datai )
                               |D|
                                   |D|
                              1 X
                           =      pF,cases (X)·
                             |D|
                                   |D|
                                          NE             NE                      E              E
                                    P ({{Xi,1 , · · · , Xi,n i
                                                               }∀case i ∈ N E, {Xk,1 , · · · , Xk,n i
                                                                                                      }f or selected case k ∈ E})
                                                                NE
                                                                     |+|X N E |+             |XkE |
                                                         P                         P
                              1 X                   i |Xi
                                                                               selected k
                           =      pF,cases (X) · pF
                             |D|
                                   |D|
                                                           NE
                                                              |+|X N E |+           |XkE |
                                                    P                        P
                               X                       i |Xi
                           =       pF,cases (X) · pF                     selected k
                                                                                             · PD (X = {all{X N E }, selected{X E }})
                                                                                                                                  (4)




H.2.2    Proof of Theorem 6.3

Recall the theorem: If people define a correct proof as the set of all the reasoning steps in different cases, even
for the cases that do not satisfy the requisite of the question, then under previous assumptions, for a LLM F , a
dataset D with the distribution PD of the set of reasoning chains. Then the probability that the LLM F can give
                   ∞
                                                                |X|+|X N E |
a correct proof is    pkF · PD (|X| + |X N E | = k), or EX∼PD [pF
                   P
                                                                             ].
                   k=1




Proof. From the proof of Theorem 6.1, we have proven that for a linear-reasoning sequence Xi,1 , . . . , Xi,ni , the
probability of generating such a sequence correctly is pnFi . To generate a proof with full propositions and logical
reasoning steps {{Xi,1
                    NE             NE
                        , · · · , Xi,n i
                                                           E
                                         }∀case i ∈ N E, {Xk,1            E
                                                               , · · · , Xk,n i
                                                                                }∀case k ∈ E}, the number of reasoning steps
should be


                                    X                             X
                                          |XiN E | + |X N E | +        |XkE | = |X N E | + |X|.
                                      i                            k




Note that in order to show the cases in set N E are impossible to exist, the proof should add an extra reasoning
step to find the contradiction in such cases. That is the reason why we add |X N E | in the number of reasoning
steps.
                          Yuliang Ji, Fuchen Shen, Jian Wu, Qiujie Xie, Yue Zhang


Hence, we have
                               1 X
Pdata∼D (correct proof ) =         P (correct proof f or datai )
                              |D|
                                    |D|
                             1 X       NE             NE                      E              E
                          =      P ({{Xi,1 , · · · , Xi,n   }∀case i ∈ N E, {Xk,1 , · · · , Xk,n   }∀case k ∈ E})
                            |D|                           i                                      i
                                    |D|
                             1 X |X N E |+|X|
                          =     pF
                            |D|
                                    |D|
                                     ∞
                               1 X k
                          =       pF · N|X N E |+|X|=k
                              |D|
                                    k=1
                            (N|X N E |+|X| represents the number of instances need |X N E | + |X| = k steps to prove)
                            ∞
                            X        N|X N E |+|X| = k
                          =   pkF ·
                                            |D|
                              k=1
                              X∞
                          =         pkF · PD (|X N E | + |X| = k)
                              k=1
                                          |X|+|X N E |
                          = EX∼PD [pF                    ]
                                                                                                                    (5)




I     Discussion about Proof-by-Contradiction technique

Mathematically, Proof-by-Contradiction technique can be considered a sub-category of Proof-by-Cases, since all
such proofs can be reformulated as a standard Proof-by-Cases proof by the following process.
The “Proof by Contradiction” proof involves:

    1. Assume the opposite of what people want to prove.
    2. Reason logically from this assumption.
    3. Find a contradiction in the reasoning steps.
    4. Conclude that the assumption must be false.

Then, reformulated as

    1. Consider two cases: what people want to prove is False and what people want to prove is True.
    2. In case 1, reason logically from the assumption that “what people want to prove is False”.
    3. Find a contradiction in the reasoning steps of case 1, and then conclude that case 1 can not occur.
    4. Show that case 2, “what people want to prove is true,” is compatible with the given premises, and conclude
       that only case 2 exists, which means that what people want to prove is True.

Consequently, “Proof by Contradiction” can be viewed as a sub-category of “Proof by Cases.” Therefore, all
instances in our dataset utilizing this technique are classified under the “Proof by Cases” category.

J      Distribution of the number of proof steps

The distribution of the number of proof steps in each linear-reasoning instance of the PC-FOL dataset is shown
in Figure 3.
Linear Reasoning vs. Proof by Cases: Obstacles for Large Language Models in FOL Problem Solving




 Figure 6: The distribution of the number of proof steps over the PC-FOL dataset (linear-reasoning part).
