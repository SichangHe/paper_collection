                                                               Are We in the AI-Generated Text World Already?
                                                              Quantifying and Monitoring AIGT on Social Media

                                                                      Zhen Sun1 * Zongmin Zhang1 * Xinyue Shen2                                 Ziyi Zhang1

                                                                         Yule Liu1           Michael Backes2       Yang Zhang2                  Xinlei He1†

                                                                 1 The Hong Kong University of Science and Technology (Guangzhou)
arXiv:2412.18148v3 [cs.AI] 1 Jun 2025




                                                                              2 CISPA Helmholtz Center for Information Security




                                                                                                                            Social Media Post
                                        Abstract                                                                              (before 2022)            AIGTBench                         Detector Benchmark

                                                                                                                         LLMs              AIGTs /HWTs                                           DetectGPT
                                                                                                                                           (Social Media)   Multi-Domains
                                        Social media platforms are experiencing a growing presence                                                                                    Metric-     GLTR
                                                                                                                                                                                      based
                                        of AI-Generated Texts (AIGTs). However, the misuse of                                                                      …                                …

                                        AIGTs could have profound implications for public opinion,                      Internet          AIGTs/HWTs
                                                                                                                                          (Open Source)     Multi-LLMs                             LM-D
                                        such as spreading misinformation and manipulating narra-                                                                                      Model-
                                                                                                                                                                                                 GPTZero
                                                                                                                                                                                      based
                                        tives. Despite its importance, it remains unclear how prevalent                                                            …
                                                                                                                                                                                                    …
                                        AIGTs are on social media. To address this gap, this paper
                                                                                                                      Social Media Data Cleaning                                                  Best Detector
                                        aims to quantify and monitor the AIGTs on online social me-                  Post Datasets                 SM-D
                                                                                                                                                             Quantifying
                                                                                                                                                                            OSM-Det
                                                                                                                                                                                                    Selection
                                                                                                                     （After 2022）
                                        dia platforms. We first collect a dataset (SM-D) with around
                                        2.4M posts from 3 major social media platforms: Medium,
                                        Quora, and Reddit. Then, we construct a diverse dataset
                                        (AIGTBench) to train and evaluate AIGT detectors. AIGT-                     Figure 1: Pipeline for quantifying AIGTs on social media: SM-
                                        Bench combines popular open-source datasets and our AIGT                    D (2.4M posts), AIGTBench (training benchmark), OSM-Det
                                                                                                                    (optimal detector).
                                        datasets generated from social media texts by 12 LLMs, serv-
                                        ing as a benchmark for evaluating mainstream detectors. With
                                        this setup, we identify the best-performing detector (OSM-
                                        Det). We then apply OSM-Det to SM-D to track AIGTs                          1    Introduction
                                        across social media platforms from January 2022 to Octo-                    The rapid development of Large Language Models (LLMs)
                                        ber 2024, using the AI Attribution Rate (AAR) as the metric.                has markedly enhanced the quality of AIGTs, enabling the
                                        Specifically, Medium and Quora exhibit marked increases in                  use of models like GPT-3.5 [42] in daily life to produce
                                        AAR, rising from 1.77% to 37.03% and 2.06% to 38.95%,                       high-quality texts, such as in academic writing [14], question-
                                        respectively. In contrast, Reddit shows slower growth, with                 answering [23], and translation [65]. These AIGTs are often
                                        AAR increasing from 1.31% to 2.45% over the same period.                    indistinguishable from Human-Written Texts (HWTs), pre-
                                        Our further analysis indicates that AIGTs on social media                   senting AIGT detection as a crucial yet challenging task for
                                        differ from human-written texts across several dimensions,                  effective classification. On social media platforms, the use
                                        including linguistic patterns, topic distributions, engagement              of LLMs to answer questions can contribute to the spread
                                        levels, and the follower distribution of authors. We envision               of misinformation [72]. Furthermore, AIGTs may be delib-
                                        our analysis and findings on AIGTs in social media can shed                 erately used for information manipulation or the dissemina-
                                        light on future research in this domain. Our code and dataset               tion of fake news, potentially resulting in serious societal
                                        are publicly available.1                                                    impacts [16]. To better understand the prevalence of AIGTs
                                                                                                                    on social media platforms, we aim to quantify and monitor
                                                                                                                    their presence, addressing the question: On social media, are
                                                                                                                    we already interacting with AI-generated texts?
                                        * Equal contribution.
                                        † Corresponding author (xinleihe@hkust-gz.edu.cn).                             Currently, numerous detectors have been developed to
                                        1 Code & Dataset: https://github.com/TrustAIRLab/AIGT_on_Social_            detect AIGTs. According to the MGTBench [17], these
                                        Media.                                                                      detectors are broadly divided into two categories: metric-


                                                                                                               1
based [12, 39] and model-based detectors [4, 21, 54], some             as HWTs receives more average “Likes” and “Comments”
of which have shown high accuracy and robustness. While                than AIGTs. This suggests that users are more inclined to
these detectors have been applied in controlled settings, recent       engage with HWTs; and (5) Authors with fewer followers
studies have explored their effectiveness in real-world sce-           are more likely to produce AIGTs. On Medium, users with
narios. Hanley and Durumeric [16] conduct AIGT detection               no more than one thousand followers tend to produce content
on news website articles, with a primary focus on content              that has the highest mean AAR at 54.02%. In contrast, as the
generated by GPT-3.5 and others from Turing benchmark,                 follower count increases, the AAR gradually shifts toward the
which includes various pre-2022 models [62]. Furthermore,              lower range (≤ 25.00%).
Liu et al. [31] detects ChatGPT-generated content on arXiv                Our contributions are summarized as follows:
papers. However, academic and news writing are formal and              • We are the first to conduct a systematic study to quantify,
tailored to specific audiences, whereas social media content             monitor, and analyze AIGTs on social media. To achieve
is more interactive, making it a better domain for observing             this, we collect a large-scale dataset SM-D, which includes
AIGTs’ impact on daily life. Moreover, previous studies do               around 2.4M posts from three platforms, spanning from
not account for recent popular LLMs, while we consider a                 January 2022 to October 2024.
broader range of models in our efforts to detect AIGTs on              • We construct AIGTBench, a dataset for benchmarking AIGT
social media.                                                            detectors. AIGTBench can be divided into two parts: one de-
   To quantify and monitor AIGTs on social media, we collect             rived from open-source datasets and the other generated by
textual data from 3 popular platforms spanning January 1,                12 LLMs based on platform-specific characteristics. Lever-
2022, to October 31, 2024, as most LLMs are released after               aging AIGTBench, we identify the most effective AIGT
2022. After data preprocessing, we obtain 1, 170, 821 posts              detector, OSM-Det.
from Medium, 245, 131 answers from Quora, and 982, 440                 • Our research reveals a remarkable increase in AAR on
comments from Reddit. We name it as SM-D, short for Social               social media after the widespread adoption of LLMs. More-
Media Dataset.                                                           over, this trend varies markedly across different platforms.
                                                                       • We conduct an in-depth analysis of the characteristics of
   To identify the most effective detector, we construct
                                                                         AIGTs and HWTs through linguistic analysis and multidi-
a dataset named AIGTBench, which consists of public
                                                                         mensional analysis of posts, revealing differences in lexical
AIGT/Supervised-Finetuning (SFT) datasets and our own
                                                                         patterns, topic distributions, engagement levels, and the
AIGT datasets generated from social media data. AIGTBench
                                                                         follower distributions of authors. These analyses provide
includes AIGTs generated by 12 different LLMs, such as GPT
                                                                         valuable insights for future research.
Series [44]) and Llama Series [10, 60, 61]), totaling around
28.77M AIGT and 13.55M HWT samples. We then bench-
mark AIGT detectors on AIGTBench and leverage the best-                2   Related Work
performing detector as our primary detector, which achieves            The growth in model parameters and training data has recently
an accuracy of 0.979 and an F1-score of 0.980. To better re-           empowered LLMs to demonstrate exceptional language pro-
flect its application in detecting AIGTs on online social media,       cessing capabilities [70]. Since then, LLMs have gradually
we rename it as OSM-Det (Online Social Media Detector).                gained popularity, like GPT-4 [43] and Llama [60], enabling
   Based on OSM-Det, we quantify and monitor the texts                 users to generate high-quality texts effortlessly. Yet, LLMs
across the 3 platforms and use the AI Attribution Rate (AAR)           exhibit multiple inherent vulnerabilities [18, 29, 57, 71] and
to represent the rate of posts classified as AI-generated (The         have raised concerns about potential misuse, such as fake
pipeline is shown in Figure 1). We observe several note-               news generation [69], academic misconduct [63], hate speech
worthy phenomena: (1) A sharp rise in AI-generated con-                generation [52], and performance degradation of training
tent begins in December 2022, with distinct AAR trends                 LLMs using AI content [6], making the detection of AIGTs
emerging across platforms. Before December 2022, the                   (also known as machine-generated texts) increasingly im-
AAR across platforms remains stable. However, starting                 portant [11]. He et al. [17] introduce MGTBench for stan-
in December, Medium and Quora show significant surges,                 dardizing the evaluation of different LLMs and experimental
while Reddit shows only a slight increase. This suggests the           setups within the AIGT detectors. They broadly categorize
widespread and diverse LLM adoption on social media; (2)               the detectors into two main types: metric-based and model-
Linguistic analysis shows similar AAR trends and exhibits              based detectors. Metric-based detectors use pre-defined met-
stylistic features in AIGTs/HWTs. Based on the word-level              rics, such as log-likelihood, to capture the characteristics
analysis, we find that the usage trend of top-frequency AI-            of texts [12, 39, 56]. In contrast, model-based detectors
preferred words aligns closely with LLM adoption trends.               rely on trained models to distinguish between AIGTs and
With sentence-level analysis, we also reveal that AIGTs tend           HWTs [4, 15, 21, 25, 31, 54]. More introduction refer to Ap-
to be more objective and standardized, whereas HWTs are                pendix B.
more flexible and informal; (3) Technology-related topics                 Besides, some researchers have applied detectors to text
drive higher AARs on Medium. Topics like “Technology”                  detection in real-world scenarios. Hanley and Durumeric [16]
and “Software Development” show the highest AARs, indi-                train a detector using data generated by the ChatGPT and
cating that users with a strong technical background are more          Turing benchmark model and conduct tests on multiple news
likely to adopt LLMs; (4) Predicted HWTs receive more                  websites. Their study reveals that, from January 1, 2022, to
engagement than AIGTs. On Medium, the content predicted                May 1, 2023, the proportion of synthetic articles increased


                                                                   2
on news sites. Liu et al. [31] also conduct detection on arXiv
and find a significant rise in the proportion of papers using
ChatGPT-generated content, reaching 26.1% by December
2023. In contrast to their detection targets, we focus on detect-
ing AIGTs on social media platforms and covering a broader
range of LLMs. Macko et al. [33] construct a multilingual
dataset based on instant messaging and social interaction plat-
forms such as Telegram and Discord, using it to compare the
performance of existing detectors. In contrast, our research
focuses on providing an in-depth temporal analysis of AIGTs
on content-driven social platforms like Medium, Quora, and                        Figure 2: Proportion of total sentences various LLMs, with
Reddit.                                                                           “Others” including Alpaca 7B and Vicuna 13B.


3   Data Collection
                                                                                  data as HWTs, given that most LLMs had not been published
In this section, we elaborate on the data collection process,                     during this period. We also design different LLMs writing
which primarily includes two datasets: the social media                           tasks to generate AIGTs that align with the characteristics of
dataset (SM-D) and the detector training dataset (AIGTBench).                     platforms (Table A1 describes the statistics details).
                                                                                     For Medium, which is primarily used for sharing articles
3.1 SM-D (Social Media Dataset)                                                   and blogs, the core tasks are centered on writing. We design
                                                                                  two LLM writing tasks: (1) polish articles to create polished
Dataset      # Posts    # Filtered Posts             Time Range                   versions; (2) based on the article’s title and summary, direct-
Medium    1, 416, 208        1, 170, 821   January 1, 2022-October 31, 2024       ing the LLM to generate complete article content, thereby
Quora        445, 864           245, 131   January 1, 2022-October 31, 2024       simulating a writing scenario. For Quora and Reddit, which
Reddit    1, 019, 261           982, 440     January 1, 2022-July 31, 2024        mainly focus on question answering and user interaction, we
                                                                                  design two tasks: (1) polish texts like Medium and (2) query
Table 1: Overview of the Medium, Quora, and Reddit datasets.                      LLM directly answer questions, simulating a user interaction
                                                                                  scenario. Detailed prompts are provided in Appendix F.
   Unlike previous research, we focus on social media plat-
                                                                                     Overall, the datasets used for training our detector and the
forms, including Medium, Quora, and Reddit, emphasizing
                                                                                  distribution of LLM series are shown in Figure 2. This dataset
content creation, sharing, and discussion. The introduction
                                                                                  includes 12 different LLMs, with a detailed introduction pro-
of platforms is in Appendix C. These platforms stand out for
                                                                                  vided in Appendix A. Within these datasets, the two most
hosting longer, more detailed posts where users emphasize
                                                                                  prevalent model series are the GPT Series, which accounts
the depth and quality of the information they share. As shown
                                                                                  for 42.99%, and the Llama series, which represents 39.05%.
in Table 1, we collect data from these social media platforms
                                                                                  GPT Series is the most widely used proprietary model and
from January 1, 2022 to October 31, 2024. We consider this
                                                                                  has played a pivotal role in the evolution of generative AI. As
part as our social media dataset for analysis.
                                                                                  of January 2023, approximately 13M users interact daily with
   For each platform, the detection targets are determined
                                                                                  GPT-3.5 [66]. The Llama series models also have significant
based on their distinct characteristics. On Medium, a blog
                                                                                  influences, as the report indicates that downloads of Llama
hosting platform, we extract both the titles and contents of
                                                                                  models on the Hugging Face platform have nearly reached
articles, treating the entire article as the detection target. On
                                                                                  around 350M [38]. Therefore, these two model series are
Quora, a question-and-answer platform, we select the corre-
                                                                                  the primary focus of our dataset. During the data genera-
sponding answers to questions as the detection target. Sim-
                                                                                  tion process, we notice that certain samples contain textual
ilarly, on Reddit, which is known for its user-driven discus-
                                                                                  noise, like irrelevant or redundant information. To maintain
sions, we also choose the response content as the detection
                                                                                  data quality, we implement some data processing strategies
target. Furthermore, we apply data filtering with the rules
                                                                                  (see Appendix E for details).
described in Appendix E.

3.2 AIGTBench (Detector Training Dataset)                                         4     Experimental Settings
To train the AIGT detectors, we consider two parts of the data.
First, we consider 6 publicly available AIGT datasets and 5
                                                                                  4.1    Datasets
common SFT datasets to form the training dataset (see Ta-                         As mentioned in Section 3, we collect the social media dataset
bles A3 and A4 for dataset statistics and Appendix D for                          (SM-D) and the detector training dataset (AIGTBench). SM-D
more details). Second, to increase the detector’s general-                        refers to the social media dataset that we conduct the quantifi-
ization capabilities on social media, we additionally collect                     cation, with more details provided in Section 3.1. AIGTBench
data from the 3 social media platforms ranging from January                       is the benchmark for AIGT detectors, which includes AIGTs
1, 2018, to December 31, 2021, as verified by an ablation                         generated by 12 different LLMs, as described in Section 3.2.
study demonstrating that these new subsets fill a gap that                        We randomly divide AIGTBench into training, validation, and
older benchmarks missed (see Appendix J). We classify this                        test sets in a 7 : 1 : 2 ratio. Specifically, the distribution of


                                                                              3
                                              Metric-based                                                                 Model-based
               Log-                Log-                                                          OpenAI      ChatGPT
                           Rank            Entropy      GLTR        LRR     DetectGPT    NPR                            ConDA    GPTZero        CheckGPT   LM-D
            Likelihood             Rank                                                          Detector    Detector
 Accuracy      0.730       0.618   0.713     0.650          0.704   0.680     0.686     0.658     0.615        0.686     0.972        0.933       0.966    0.979
 F1-score      0.754       0.730   0.741     0.697          0.733   0.660     0.659     0.639     0.484        0.602     0.973        0.930       0.966    0.980

                         Table 2: Performance of detectors on AIGTBench. The F1-score corresponds to the AI class.


token lengths in the training, validation, and test set are shown                       5     Evaluation
in Figure A1.
                                                                                        5.1     Benchmarking Detectors
                                                                                        This section compares different AIGT detectors on the test
4.2    AIGT Detectors                                                                   set of the AIGTBench. Illustrated in Table 2, the metric-based
Following the experimental setup of MGTBench [17], we                                   detectors perform poorly. The F1-scores for Log-Likelihood,
evaluate 14 detectors. For metric-based detectors, we con-                              Rank, Log-Rank, and Entropy are 0.754, 0.730, 0.741, and
sider LogLikelihood, Rank, LogRank, Entropy, GLTR, LRR,                                 0.697, respectively. These low scores indicate that metric-
DetectGPT, and NPR [12, 39, 54]. We choose the GPT-2                                    based detectors face limitations in handling complex, multi-
medium [49] as the base model, given its good detection                                 source datasets and struggle to capture subtle textual features
performance at limited computational costs.                                             effectively.
   During the detection process, we initially use the GPT-2                                Regarding model-based detectors, we observe that both
medium to extract multiple metrics, including log-likelihood                            OpenAI Detector and ChatGPT Detector perform worse than
and log-rank. Based on these extracted metrics, we train logis-                         some metric-based detectors. Specifically, OpenAI Detector
tic regression models to enhance the accuracy of predictions.                           has an F1-score of only 0.484, with relatively low accuracy.
For the model-based detectors, we consider both pre-trained                             This underperformance may be due to the detector being fine-
detectors and fine-tuned models with the AIGTBench, that is,                            tuned using GPT-2 output, which struggles to adapt to more
OpenAI Detector [54], ChatGPT Detector [15], ConDA [4],                                 complex data generated by modern LLMs, such as the Llama
GPTZero [13], CheckGPT [31], and LM-D [21]. Specifically,                               and Claude Series.
for the OpenAI Detector and ChatGPT Detector, we consider                                  Notably, LM-D and ConDA outperform the others. ConDA
their pre-trained version and select the RoBERTa-base model                             achieves an accuracy of 0.972, while the LM-D performs
as it demonstrates stable performance across multiple detec-                            even better, with an accuracy of 0.979 and an F1-score of
tion tasks and typically provides better detection results. For                         0.980, making it the most effective detector. Based on these
ConDA and LM-D, we choose the Longformer-base-4096                                      benchmark results, we consider LM-D as the most effective
model as the base model and fine-tune it with the AIGTBench.                            detection method and name LM-D fine-tuned on AIGTBench
All of them have a learning rate of 1e-5, a batch size of 16,                           as OSM-Det, which is subsequently used to quantify and
and the AdamW optimizer. For GPTZero, we directly use                                   monitor the AAR in social media dataset (SM-D). More details
its commercial API. For CheckGPT, we retrain the original                               on performance across different platforms and all text lengths
training framework [31].                                                                in SM-D are shown in Appendix G.

                                                                                                            Platform    # text (Human)        FPR
4.3    Evaluation Metrics                                                                                   Medium         116, 303           1.82%
                                                                                                             Quora         101, 145           1.36%
We use accuracy and F1-score as the evaluation metrics to                                                   Reddit          53, 321           1.70%
evaluate the performance of different detectors, which are
common standards in AIGT detection tasks. Besides, we                                          Table 3: FPR of OSM-Det on social media platforms.
introduce two metrics AI Attribution Rate (AAR) and False
Positive Rate (FPR) for quantification analysis. The AAR
indicates the proportion of texts that the model predicts as                            5.2     Generalizability of OSM-Det
AI-generated, while the FPR denotes the proportion of HWTs
                                                                                        AIGTBench is a comprehensive dataset that contains multi-
misclassified as AIGTs.
                                                                                        source, multi-domain, and multi-LLM data. The diversity of
   To assess word usage, we compute the normalized term                                 this dataset enhances the generalizability of detectors in real-
frequency (NTF) as:                                                                     world (in-the-wild) environments. OSM-Det, on the other
                                                                                        hand, is the optimal detection model trained on AIGTBench.
                                         ft,d                                              In this section, we evaluate the generalizability of OSM-
                   NTF(t, d) =                          ,                   (1)         Det from three perspectives: AIGTs produced with different
                                    N · ∑t ′ ∈d ft ′ ,d
                                                                                        generation parameters, AIGTs of social media generated by
where ft,d is the frequency of word t in document d, ∑t ′ ∈d ft ′ ,d                    unseen models, and tests in the wild.
accounts for all words in d, and N is the total occurrences of t                        Different Generation Parameters. To investigate whether
across all documents.                                                                   OSM-Det can effectively detect AIGTs generated with differ-


                                                                                  4
                                GPT4o             GPT4o-mini                    demonstrates that OSM-Det exhibits strong generalization
                1.00                                                            capability when detecting AIGTs generated by previously
     Accuracy


                0.99                                                            unseen LLMs.
                0.98                                                            Test In the Wild. To test OSM-Det in the wild, we randomly
                       0.1 0.2          0.4      0.6       0.8        1.0
                                           Temperature                          select datasets from the huggingface platform for evaluation.
                1.00                                                            These datasets are in two main categories: unseen models and
     Accuracy




                0.99                                                            unseen domains, neither of which are included in AIGTBench.
                0.98                                                               As shown in Table A7, for the unseen model scenario,
                       0.1 0.2          0.4      0.6       0.8        1.0       the test results align with previous findings, where OSM-
                                              Top-P
                                                                                Det maintains high accuracy and F1-score. Similarly, in
                1.00
     Accuracy




                                                                                the unseen domain scenario, OSM-Det also demonstrates
                0.99
                                                                                strong generalizability, achieving a minimum accuracy of
                0.98
                       1 5 10     50           100                    200       0.943. This is consistent with the findings of Liu et al. [30],
                                              Top-K                             which suggest that AIGT detectors exhibit generalizability
                                                                                across different domains.
Figure 3: Impact of different generation parameters on AIGT
detection accuracy.                                                             5.3    Evaluation on Social Media Platforms
                                                                                As shown in Table 3, OSM-Det achieves False Positive Rates
ent generation parameters, we randomly sample 5, 000 HWTs                       (FPR) of 1.82%, 1.36%, and 1.70% on Medium, Quora, and
from the AIGTBench and apply the same prompt to refine                          Reddit, respectively, while achieving a benchmark F1-score
them using different generation parameters (including temper-                   of 0.980 (see Table 2). These results highlight OSM-Det’s
ature, top-p, and top-k). The models used for this experiment                   low misclassification rate and high overall accuracy, making
are GPT4o and GPT4o-mini.                                                       it a reliable choice for quantifying and monitoring AIGTs on
   As shown in Figure 3, OSM-Det maintains an accuracy                          social media.
of over 0.99 across the entire range of temperature settings                    Evaluation on Medium. Figure 4a illustrates the trend of
(0.1 to 1.0). Top-P (0.1 to 1.0) and Top-K (1 to 200) show                      AAR on Medium from January 2022 to October 2024. From
a similar trend. This indicates that OSM-Det demonstrates                       January 2022 to November 2022, the AAR remains stable,
strong generalizability when detecting AIGTs generated with                     fluctuating around 1.82%. This suggests that, before the
different parameters.                                                           widespread adoption of GPT-3.5, creators mainly rely on
                                                                                original content with minimal dependency on LLM-generated
                            Model               Accuracy   F1-score
                                                                                content. However, starting in December 2022, coinciding
                        Deepseek-V3              0.986      0.993
                        GLM-4-Flash              0.997      0.998
                                                                                with the launch of GPT-3.5, the AAR begin to rise rapidly.
                       Gemini-1.5-Flash          0.938      0.952               Between December 2022 and July 2023, the AAR surges from
                       Gemini-2.0-Flash          0.984      0.992               10.20% to 30.24%, reflecting how the popularization of LLM
                         Yi-1.5-34B              0.999      0.999
                       InternVL2.5-8B            0.925      0.958               technology significantly lowers the barriers of content gen-
                   Dolphin3.0-Llama3.1-8B        0.996      0.998               eration, prompting Medium’s creator community to widely
                   Llama3-OpenBioLLM-8B          0.960      0.980
                      Xwin-LM-13B-V0.2           0.996      0.998
                                                                                adopt LLM-assisted content creation. From August 2023
                                                                                to July 2024, the AAR experiences slower growth, ranging
Table 4: Performance of OSM-Det on AIGTs generated from                         between 29.20% and 36.29%, with fluctuations stabilizing be-
unseen LLMs based on social media data from AIGTBench.                          tween 30.12% and 33.75%. This indicates that AIGTs have
                                                                                gradually become an integral part of the platform’s creative
                                                                                ecosystem, serving as a critical component of content produc-
AIGTs of Social Media Generated By Unseen Models.
                                                                                tion. From August 2024 to October 2024, the AAR further
To investigate the generalizability of OSM-Det on social
                                                                                increased to 37.03%, reaching a new peak. This likely re-
media AIGTs generated by unseen models, we selected 6
                                                                                flects the growing acceptance and reliance on LLM-assisted
pre-trained models, including Deepseek-V3 [26], GLM-4-
                                                                                creation among content creators to enhance writing efficiency
Flash [5], Gemini-1.5-Flash [9], Gemini-2.0-Flash [9], Yi-
                                                                                and quality.
1.5-34B [68], and InternVL2.5-8B [45]. Additionally, we
include three fine-tuned models based on the LLaMA series:                         Overall, from December 2022 to October 2024, the AAR on
Dolphin3.0-Llama3.1-8B [8], Llama3-OpenBioLLM-8B [1],                           Medium has shown a continuous upward trend, underscoring
and Xwin-LM-13B-V0.2 [67]. Since none of these models                           the significant impact of LLM technology on content creation.
were included in AIGTBench, they are considered unseen to                       Evaluation on Quora. Figure 4b displays the trend of AAR
OSM-Det. We also apply the same polishing process to the                        on Quora. We observe that from January 2022 to October
previously selected 5, 000 data samples.                                        2022, the AAR fluctuates but remains relatively low. After
   From Table 4, we observe that OSM-Det maintains strong                       the release of GPT-3.5 in November 2022, the AAR slightly
detection performance across these unseen models. The low-                      increases to 2.87%. Subsequently, starting in December 2022,
est performance was recorded for InternVL2.5-8B, yet it still                   the AAR markedly rises to 15.12% and shows a clear upward
achieve an accuracy of 0.925 and an F1-score of 0.958. This                     trend in AIGTs, reaching a peak of 38.95% in August 2023.


                                                                            5
                                                                     Evaluation on Reddit. Figure 4c shows the quantification
                                                                     analysis on Reddit from January 2022 to July 2024. From
                                                                     January to November 2022, we observe that the AAR remains
                                                                     below the FPR, fluctuating around 1.30%, indicating that
                                                                     there is almost no AI-generated content on Reddit during this
                                                                     period. Following the release of GPT-3.5, the AAR begins
                                                                     to rise slightly, reaching 2.36% in January 2023 and further
                                                                     increases to 2.93% in February 2023. From March 2023 to
                                                                     July 2024, the AAR stabilizes at a low level, within the range
                                                                     of 1.86% − 2.95%.
                                                                        Briefly, similar to Medium and Quora, AAR on Reddit
                                                                     shows an upward trend following the release of GPT-3.5, but
(a) AAR Trends on Medium from January 1, 2022, to October            it consistently maintains a lower level, indicating a lower
31, 2024.
                                                                     dependency on LLMs among Reddit users.




                                                                     (a) Word frequency trends on Medium from January 1, 2022, to
                                                                     October 31, 2024.
(b) AAR Trends on Quora from January 1, 2022, to October 31,
2024.




                                                                     (b) Word frequency trends on Quora from January 1, 2022, to
                                                                     October 31, 2024.




(c) AAR Trends on Reddit from January 1, 2022, to July 31,
2024.
                                                                     (c) Word frequency trends on Reddit from January 1, 2022, to
Figure 4: Comparison of AAR and FPR across Medium, Quora,
                                                                     July 31, 2024.
and Reddit over different time periods.
                                                                     Figure 5: Comparison of Medium and Quora word frequency
                                                                     trends: human vs. AI preferences.
From September 2023 to the first half of 2024, although the
AAR remains high, it declines from the peak in early 2023 and
gradually stabilizes between 22.03% − 30.79% throughout              5.4   Linguistic Analysis at Different Levels
2024. This indicates that the behavior of Quora users in
generating AI content is becoming more stable. From June             We explore the interpretability of the OSM-Det model in the
2024, the AAR gradually decreases and reaches a low near             case study using two methods: Integrated Gradients [58],
19.79% between September and October 2024. The increase              representing a model-dependent perspective, and Shapley
in AAR may be attributed to Quora’s launch of its LLM                Value [32], offering a model-independent perspective. Details
platform, Poe, in 2023 [2], which initially led to a rise in         of the two methods can be found in Appendix H.2.
AI-generated content. However, as many Quora users found             Word-Level Analysis. In the case study of Reddit (refer to
Poe’s capabilities insufficient to meet their daily needs, the       Figures A6 and A8), words like “and” , “think” and “I”
AAR likely declined following this initial surge, eventually         have the highest Integrated Gradients and Shapley Values,
stabilizing.                                                         which lead model to classify texts as human-written. Mean-


                                                                 6
while, model-specific analysis shows the words “think” ,                                          70%




                                                                                                                  GPT-3.5 Release Date
                                                                                                                                November 30, 2022
 “can” , and “Online” have the lowest scores, leading to                                          60%
AI-generated prediction. From these observations, we note




                                                                            AI Attribution Rate
                                                                                                  50%
that specifying clear word-level patterns between two class is                                    40%
challenging because certain words, like “think” , contribute                                      30%
significantly to both classifications. This overlap suggests that                                 20%
word importance is highly context-dependent. Similar chal-                                        10%
                                                                                                                                                                    False Positive Rate (1.82%)
lenges are also observed on Medium and Quora (Figures A9,                                         0%
A11, A12 and A14).




                                                                                                  -01

                                                                                                        20 4

                                                                                                        20 7

                                                                                                        20 0
                                                                                                        20 1
                                                                                                        20 4

                                                                                                        20 7

                                                                                                        20 0
                                                                                                        20 1
                                                                                                        20 4

                                                                                                        20 7
                                                                                                             -10
                                                                                                             -0
                                                                                                             -0

                                                                                                             -1

                                                                                                             -0
                                                                                                             -0
                                                                                                             -0

                                                                                                             -1

                                                                                                             -0
                                                                                                             -0
                                                                                                             -0
                                                                                       22
                                                                                                          22
                                                                                                          22

                                                                                                          22

                                                                                                          23
                                                                                                          23
                                                                                                          23

                                                                                                          23

                                                                                                          24
                                                                                                          24
                                                                                                          24

                                                                                                          24
                                                                             20
                                                                                                   20
   Given this difficulty, we then turn to a different approach: a                                                                                   AAR of Topics
statistical analysis of high-frequency adjectives, conjunctions,                                        Culture                          Self Improvement                           Technology
and adverbs (details provided in Appendix H.1). These high-                                             Life                             Society                                    Work
                                                                                                        Media                            Software Development                       World
frequency terms are then classified into human-preferred and
AI-preferred vocabularies. We then track the trends of these
lexical items on SM-D.                                                                              Figure 6: AAR trends across different topics.
   As shown in Figures 5a and 5b, the NTF of AI-preferred
vocabulary on the Medium and Quora is closely aligned with              We observe a rapid increase in AAR for all topics following
the development of LLMs. Following the release of LLMs                  the release of GPT-3.5 in December 2022, indicating that
such as GPT, Llama, and the Claude series, the NTF of human-            the popularity of LLMs has impacted all topics on Medium.
preferred vocabulary has gradually declined. Meanwhile,                 Besides, the AAR for “Technology” and “Software Devel-
AI-preferred vocabulary shows an increase. These results                opment” remains consistently higher than other topics from
reflect an increasing usage of LLMs for content generation              December 2022 to October 2024, ranking respectively first
by Medium and Quora platform users. In contrast, the trends             and second. One possible reason is that people in the technol-
on Reddit show some differences. From 2022 to 2024, the                 ogy field are more likely to know about LLMs and frequently
NTF of human-preferred vocabulary always remains high,                  interact with them, leading to a higher AAR.
while the AI-preferred vocabulary consistently remains low.
This indicates that Reddit users rely less on LLMs to produce
                                                                                                                    Mean Likes                                          Mean Comments
content. From above, we obverse that word frequency changes                 Follower Group
                                                                                                                  (AIGTs / HWTs)                                        (AIGTs / HWTs)
closely align with the AAR trends in Figure 4.
                                                                                                    0-1K                 49.48/79.39                                          3.18/5.68
Sentence-Level Analysis. We also conduct a sentence-level                                           1-5K                111.50/191.61                                         5.11/9.09
analysis using Shapley values, as Integrated Gradients are                                          >5K                 126.94/211.92                                         5.56/8.25
only suitable for word-level. From the case studies of
Medium, Quora, and Reddit (shown in Figures A7, A10                     Table 5: Engagement statistics on Medium for different follower
and A13), we observe that AIGTs are characterized by their              groups, comparing AIGTs and HWTs.
objective and standardized structures, typically beginning
with a noun or pronoun and following a verb-object pat-
tern,    like   “Online bullying...contributes...feelings...” .
In contrast, HWTs often contain flexible sen-
tence structures and informal expressions, as il-
lustrated by      “That being said, why not both?”        and
 “Why can’t we restore...” . In summary, the results suggest
that sentence-level patterns provide more distinctive charac-
teristics for distinguishing AIGTs and HWTs, as LLMs may
usually follow a standardized pattern to generate texts.

5.5    Multidimensional Analysis of Posts
We analyze posts on social media from multi-dimensions to                            Figure 7: AAR distribution among follower groups.
find the characteristics between posts predicted as AIGTs and
those classified as HWTs, including topic, engagement, and
                                                                        Engagement Analysis. To understand how user engagement
author analysis.
                                                                        differs between articles predicted to be AIGTs or HWTs,
Topic Analysis. Classifying topics on platforms like Quora              we analyze the number of “Likes” (known as “Claps” on
and Reddit is challenging due to their wide range. There-               Medium) and “Comments” in Medium blogs. To ensure bal-
fore, we focus our analysis on 9 major topics listed on the             anced comparisons, we randomly select 16, 600 blogs with a
Medium [36], examining them from a temporal perspective.                1:1 class ratio. Mann-Whitney U tests reveal statistically sig-
The proportion of topics is shown in Figure A2.                         nificant differences in the number of “Likes” and “Comments”
  Figure 6 shows the trends of AAR across different topics.             between the two classes (p < 0.05).


                                                                    7
   As shown in Figure A3a, the predicted-AIGTs receive                 AIGTs nor to interfere with legitimate content-creation activi-
fewer “Likes” on average than predicted-HWTs, with mean                ties. Instead, our goal is to provide valuable insights through
values of 69.15 and 127.59, respectively. And predicted-               scientific analysis to aid the research community and the
AIGTs exhibit a higher frequency of low “Likes” counts.                public to better understand the current state and trends of
Figure A3b shows that predicted-AIGTs receive fewer “Com-              generative AI usage on social media. All data used in our
ments” on average compared to predicted-HWTs, with mean                paper is publicly available, and we do not collect and monitor
values of 4.16 and 7.38, respectively. We further investigate          any private information.
the mean values of Likes and Comments for authors with dif-
ferent numbers of followers and Table 5 indicates that, across         Limitations
all follower count groups, AIGTs receive significantly fewer
Likes and Comments compared to HWTs.                                   In this paper, we conduct long-term quantification of AIGTs
   To summarize, predicted-HWTs obtain more “Likes” and                on 3 commonly used social media platforms, but there are
“Comments”, which indicates that users in Medium are gen-              still some limitations:
erally more willing to engage with human-written content.              1. Limited coverage of LLMs: AIGTBench includes only
However, the relatively small gap between the two suggests                 12 LLMs and does not cover all LLMs released across
that AI-generated content appeals to users.                                different time periods. We only included models released
                                                                           after November 2022. This decision was made because our
Author Analysis. On Medium, we randomly select 1, 000 au-                  study specifically focuses on more powerful models, such
thors from the predicted-AIGTs group who have published at                 as ChatGPT, which may lead to misclassifications for ear-
least ten articles. We collect and detect all of their published           lier models. In addition, the data set shows distributional
articles to determine if they are AI-generated, aiming to ex-              bias favoring the GPT series 42.9% and the Llama series
plore the potential relationship between an author’s follower              39.05% models. While current AIGT detectors can gener-
count and their usage of AI-generated content.                             alize to unseen LLMs to some extent [25], these coverage
   As shown in Figure 7, we divide these authors into three                limitations may introduce slight errors and pose potential
groups based on their follower count. Among the groups,                    impacts on the accuracy of some results. However, these
those with 1, 000 or fewer followers exhibit a stronger con-               biases are unlikely to significantly impact the analysis re-
centration in the high AAR range (≥ 75.00%). This group                    sults, as these models are also the most widely used in
also achieves the highest mean AAR at 54.02%. From the                     real-world applications.
overall distribution, as the follower number increases, the            2. Lack of analysis on multilingual platforms: Our re-
AAR gradually shifts toward the lower range (≤ 25.00%).                    search focuses on English-dominated social media plat-
This trend may stem from more popular authors prioritizing                 forms. Therefore, the applicability of our findings is re-
content quality, while less-followed authors rely on LLMs to               stricted to these specific platforms and language contexts.
boost efficiency.                                                          Since data collection is a long-term process, we plan to
   Furthermore, Figure A4 illustrates the publication timeline             gradually expand to multilingual environments and more
of the first articles detected as AIGTs from these authors. It             platforms in future research to improve the universality of
can be observed that there is a significant increase in such               the conclusions.
publications during the month GPT-3.5 is released, followed            3. Insufficient dimensions of analysis across platforms:
by a relatively stable trend in subsequent months.                         We conduct an in-depth analysis of the three dimensions
                                                                           of topic, engagement, and author on the Medium platform,
6   Conclusion                                                             but we are unable to conduct similar multi-dimensional
                                                                           research on Quora and Reddit. This is mainly due to the
In this paper, we collect a large-scale dataset, SM-D, encom-              differences in data collection methods and the difficulty
passing multiple platforms and diverse time periods, providing             of different platforms. If richer data from these platforms
the first comprehensive quantification and analysis of AIGTs               becomes available in the future, we will supplement and
on online social media. We construct AIGTBench, an AIGT                    enhance the analysis.
detection benchmark integrating diverse LLMs, to identify the
most effective detector, OSM-Det. We then perform temporal
                                                                       Acknowledgement
tracking analyses, highlighting distinct trends in AAR that are
shaped by platform-specific characteristics and the increasing         We would like to thank all anonymous reviewers, Area Chair,
adoption of LLMs. Finally, our analysis uncovers critical dif-         and Program Chair for their insightful comments and con-
ferences between AIGTs and HWTs across linguistic patterns,            structive suggestions. We are also grateful to Dr. Yun Shen
topical features, engagement levels, and the follower distribu-        for his valuable guidance and feedback in this work.
tion of authors. Our findings offer valuable perspectives into
the evolving dynamics of AIGTs on social media.


Ethical Statement
We emphasize that the purpose of this research is not to ex-
pose or criticize specific platforms or users for employing


                                                                   8
References                                                           [13] GPTZero. Gptzero, 2024. URL https://gptzero.me/.
                                                                          Accessed: 2024-11-04. 4, 14
 [1] Aaditya.   Llama 3 - openbiollm - 8b model,
     2024.    URL https://huggingface.co/aaditya/                    [14] Dritjon Gruda. Three ways chatgpt helps me in my aca-
     Llama3-OpenBioLLM-8B. Accessed: 2025-02-15. 5                        demic writing. Nature, 2024. doi: 10.1038/d41586-024-
 [2] Adam D’Angelo, 2023. Poe ai introduction, 2024. Avail-               01042-3. URL https://doi.org/10.1038/d41586-
     able at: https://quorablog.quora.com/Poe-1 [Ac-                      024-01042-3. Advance online publication. 1
     cessed: 2024-12-05]. 6                                          [15] Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang,
 [3] Anthropic. Anthropic official website, 2024. URL                     Jinran Nie, Yuxuan Ding, Jianwei Yue, and Yupeng Wu.
     https://www.anthropic.com/. Accessed: 2024-11-                       How close is chatgpt to human experts? comparison cor-
     04. 13                                                               pus, evaluation, and detection. CoRR, abs/2301.07597,
                                                                          2023. 2, 4, 13, 14, 19
 [4] Amrita Bhattacharjee, Tharindu Kumarage, Raha Moraf-
     fah, and Huan Liu. Conda: Contrastive domain adapta-            [16] Hans W. A. Hanley and Zakir Durumeric. Machine-
     tion for ai-generated text detection. In Annual Meeting              made media: Monitoring the mobilization of machine-
     of the Association for Computational Linguistics and                 generated articles on misinformation and mainstream
     International Joint Conference on Natural Language                   news websites. In Proceedings of the Eighteenth Inter-
     Processing (ACL/IJCNLP), pages 598–610. ACL, 2023.                   national AAAI Conference on Web and Social Media,
     2, 4, 14                                                             ICWSM 2024, Buffalo, New York, USA, June 3-6, 2024,
                                                                          pages 542–556. AAAI Press, 2024. 1, 2
 [5] BigModel.     Glm-4 api documentation, 2024.
     URL https://open.bigmodel.cn/dev/api/normal-                    [17] Xinlei He, Xinyue Shen, Zeyuan Chen, Michael Backes,
     model/glm-4. Accessed: 2025-02-15. 5                                 and Yang Zhang. Mgtbench: Benchmarking machine-
                                                                          generated text detection. In ACM Conference on Com-
 [6] Martin Briesch, Dominik Sobania, and Franz Rothlauf.                 puter and Communications Security (CCS), pages 2251–
     Large language models suffer from their own output:                  2265. ACM, 2024. 1, 2, 4, 14
     An analysis of the self-consuming training loop. CoRR,
     abs/2311.16822, 2023. 2                                         [18] Xinlei He, Guowen Xu, Xingshuo Han, Qian Wang,
                                                                          Lingchen Zhao, Chao Shen, Chenhao Lin, Zhengyu
 [7] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng,
                                                                          Zhao, Qian Li, Le Yang, Shouling Ji, Shaofeng Li,
     Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan
                                                                          Haojin Zhu, Zhibo Wang, Rui Zheng, Tianqing Zhu,
     Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al.
                                                                          Qi Li, Chaoxiang He, Qifan Wang, Hongsheng Hu,
     Vicuna: An open-source chatbot impressing gpt-4 with
                                                                          Shuo Wang, Shi-Feng Sun, Hongwei Yao, Zhan Qin,
     90%* chatgpt quality. See https://vicuna. lmsys. org
                                                                          Kai Chen, Yue Zhao, Hongwei Li, Xinyi Huang, and
     (accessed 14 April 2023), 2(3):6, 2023. 13
                                                                          Dengguo Feng. Artificial intelligence security and pri-
 [8] Cognitive Computations. Dolphin 3.0 - llama 3.1 -                    vacy: a survey. Science China Information Sciences,
     8b model, 2024. URL https://huggingface.co/                          2025. 2
     cognitivecomputations/Dolphin3.0-Llama3.1-
                                                                     [19] Heralax.    Mannerstral-dataset, 2025.   URL
     8B. Accessed: 2025-02-15. 5
                                                                          https://huggingface.co/datasets/Heralax/
 [9] DeepMind. Gemini flash, 2024. URL https://                           Mannerstral-dataset?row=2. 20
     deepmind.google/technologies/gemini/flash/.
     Accessed: 2025-02-15. 5                                         [20] Matthew Honnibal, Ines Montani, Sofie Van Landeghem,
                                                                          and Adriane Boyd. spaCy: Industrial-strength Natural
[10] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,                     Language Processing in Python. 2020. doi: 10.5281/
     Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,                      zenodo.1212303. 16
     Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,
     et al. The llama 3 herd of models. arXiv preprint               [21] Daphne Ippolito, Daniel Duckworth, Chris Callison-
     arXiv:2407.21783, 2024. 2, 13                                        Burch, and Douglas Eck. Automatic detection of gener-
                                                                          ated text is easiest when humans are fooled. In Annual
[11] Kathleen C. Fraser, Hillary Dawkins, and Svetlana Kir-               Meeting of the Association for Computational Linguis-
     itchenko. Detecting ai-generated text: Factors influenc-             tics (ACL), pages 1808–1822. ACL, 2020. 2, 4, 14
     ing detectability with current methods. J. Artif. Intell.
     Res., 82:2233–2278, 2025. 2                                     [22] Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux,
                                                                          Arthur Mensch, Blanche Savary, Chris Bamford, De-
[12] Sebastian Gehrmann, Hendrik Strobelt, and Alexan-                    vendra Singh Chaplot, Diego de las Casas, Emma Bou
     der M. Rush. GLTR: statistical detection and visual-                 Hanna, Florian Bressand, et al. Mixtral of experts. arXiv
     ization of generated text. In Annual Meeting of the                  preprint arXiv:2401.04088, 2024. 13
     Association for Computational Linguistics (ACL), pages
     111–116. Association for Computational Linguistics,             [23] Ehsan Kamalloo, Nouha Dziri, Charles L. A. Clarke,
     2019. 2, 4, 13                                                       and Davood Rafiei. Evaluating open-domain question


                                                                 9
     answering in the era of large language models. In Annual        [33] Dominik Macko, Jakub Kopal, Róbert Móro, and Ivan
     Meeting of the Association for Computational Linguis-                Srba. Multisocial: Multilingual benchmark of machine-
     tics (ACL), pages 5591–5606. ACL, 2023. 1                            generated text detection of social-media texts. CoRR,
                                                                          abs/2406.12549, 2024. 3
[24] Narine Kokhlikyan, Vivek Miglani, Miguel Martin, Ed-
     ward Wang, Bilal Alsallakh, Jonathan Reynolds, Alexan-          [34] Magpie-Align. Magpie-reasoning-v1-150k-cot-qwq,
     der Melnikov, Natalia Kliushkina, Carlos Araya, Siqi                 2025. URL https://huggingface.co/datasets/
     Yan, and Orion Reblitz-Richardson. Captum: A unified                 Magpie-Align/Magpie-Reasoning-V1-150K-CoT-
     and generic model interpretability library for pytorch.              QwQ. 20
     CoRR, abs/2009.07896, 2020. 16
                                                                     [35] Magpie-Align.       Magpie-reasoning-v2-250k-cot-
[25] Yafu Li, Qintong Li, Leyang Cui, Wei Bi, Zhilin Wang,                deepseek-r1-llama-70b, 2025.     URL https://
     Longyue Wang, Linyi Yang, Shuming Shi, and Yue                       huggingface.co/datasets/Magpie-Align/Magpie-
     Zhang. MAGE: machine-generated text detection in                     Reasoning-V2-250K-CoT-Deepseek-R1-Llama-70B.
     the wild. In Annual Meeting of the Association for                   20
     Computational Linguistics (ACL), pages 36–53. ACL,
     2024. 2, 8, 14                                                  [36] Medium. Explore topics on medium, 2024. URL https:
                                                                          //medium.com/explore-topics. Accessed: 2025-02-
[26] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang,                        15. 7
     Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi
     Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3              [37] Medium. Medium, 2024. URL https://medium.com/.
     technical report. arXiv preprint arXiv:2412.19437, 2024.             Accessed: 2024-11-04. 14
     5
                                                                     [38] Meta AI.     With 10x growth since 2023, llama
[27] Xiaoming Liu, Zhaohan Zhang, Yichen Wang, Hang Pu,                   is the leading engine of ai innovation, 2024.
     Yu Lan, and Chao Shen. Coco: Coherence-enhanced                      URL     https://ai.meta.com/blog/llama-usage-
     machine-generated text detection under low resource                  doubled-may-through-july-2024/.       Accessed:
     with contrastive learning. In Conference on Empirical                2024-11-04. 3
     Methods in Natural Language Processing (EMNLP),
                                                                     [39] Eric Mitchell, Yoonho Lee, Alexander Khazatsky,
     pages 16167–16188. ACL, 2023. 14, 19
                                                                          Christopher D Manning, and Chelsea Finn. Detect-
[28] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-                  gpt: Zero-shot machine-generated text detection using
     dar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke                   probability curvature. In International Conference on
     Zettlemoyer, and Veselin Stoyanov. Roberta: A ro-                    Machine Learning (ICML), pages 24950–24962. PMLR,
     bustly optimized BERT pretraining approach. CoRR,                    2023. 2, 4, 13
     abs/1907.11692, 2019. 13
                                                                     [40] Moonshot. Mootshot llm, 2024. URL https://kimi.
[29] Yule Liu, Zhen Sun, Xinlei He, and Xinyi Huang.                      moonshot.cn/. Accessed: 2024-11-04. 13
     Quantized delta weight is safety keeper. CoRR,
                                                                     [41] OdiaGenAI.     Roleplay-english, 2025.  URL
     abs/2411.19530, 2024. 2
                                                                          https://huggingface.co/datasets/OdiaGenAI/
[30] Yule Liu, Zhiyuan Zhong, Yifan Liao, Zhen Sun, Jingyi                roleplay_english?row=24. 20
     Zheng, Jiaheng Wei, Qingyuan Gong, Fenghua Tong,
                                                                     [42] OpenAI. Introducing chatgpt, 2022. URL https://
     Yang Chen, Yang Zhang, and Xinlei He. On the Gener-
                                                                          openai.com/index/chatgpt/. Accessed: 2024-11-04.
     alization and Adaptation Ability of Machine-Generated
                                                                          1, 13
     Text Detectors in Academic Writing. In Proceedings of
     the 31st ACM International Conference on Knowledge              [43] OpenAI. Gpt-4 technical report, 2023. 2
     Discovery and Data Mining (KDD), Volume 2. ACM,
     2025. 5, 14, 19                                                 [44] OpenAI.         Gpt-4o mini:  Advancing cost-
                                                                          efficient intelligence, 2024.   URL https:
[31] Zeyan Liu, Zijun Yao, Fengjun Li, and Bo Luo. On the                 //openai.com/index/gpt-4o-mini-advancing-
     detectability of chatgpt content: Benchmarking, method-              cost-efficient-intelligence/. Accessed: 2024-
     ology, and evaluation through the lens of academic writ-             11-04. 2, 13
     ing. In ACM SIGSAC Conference on Computer and Com-
     munications Security (CCS), pages 2236–2250. ACM,               [45] OpenGVLab. Internvl2.5-8b model, 2024. URL https:
     2024. 2, 3, 4, 14, 15, 19                                            //huggingface.co/OpenGVLab/InternVL2_5-8B.
                                                                          Accessed: 2025-02-15. 5
[32] Scott M. Lundberg and Su-In Lee. A unified approach
     to interpreting model predictions. In Advances in neural        [46] OpenGVLab. Internvl-sa-1b-caption, 2025. URL
     information processing systems, pages 4765–4774, 2017.               https://huggingface.co/datasets/OpenGVLab/
     6, 16                                                                InternVL-SA-1B-Caption?row=0. 20


                                                                10
[47] PJMixers-Dev. camel-ai_chemistry-gemini-2.0-flash-               [58] Mukund Sundararajan, Ankur Taly, and Qiqi Yan. Ax-
     thinking-exp-1219-customsharegpt, 2025.     URL                       iomatic attribution for deep networks. In International
     https://huggingface.co/datasets/PJMixers-                             Conference on Machine Learning (ICML), volume 70,
     Dev/camel-ai_chemistry-gemini-2.0-flash-                              pages 3319–3328. PMLR, 2017. 6
     thinking-exp-1219-CustomShareGPT. 20
                                                                      [59] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann
[48] Quora. Quora, 2024. URL https://www.quora.com/.                       Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and
     Accessed: 2024-11-04. 14                                              Tatsunori B Hashimoto. Alpaca: A strong, replicable
                                                                           instruction-following model. Stanford Center for Re-
[49] Alec Radford, Jeffrey Wu, Rewon Child, David Luan,                    search on Foundation Models. https://crfm. stanford.
     Dario Amodei, Ilya Sutskever, et al. Language models                  edu/2023/03/13/alpaca. html, 3(6):7, 2023. 13
     are unsupervised multitask learners. OpenAI blog, 1(8):
     9, 2019. 4                                                       [60] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
                                                                           Martinet, Marie-Anne Lachaux, Timothée Lacroix, Bap-
[50] Reddit. Reddit, 2024. URL https://www.reddit.                         tiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar,
     com/. Accessed: 2024-11-04. 14                                        et al. Llama: Open and efficient foundation language
                                                                           models. arXiv preprint arXiv:2302.13971, 2023. 2, 13
[51] Lloyd S Shapley. A value for n-person games. Contri-
     bution to the Theory of Games, 2, 1953. 16                       [61] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert,
                                                                           Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov,
[52] Xinyue Shen, Yixin Wu, Yiting Qu, Michael Backes,
                                                                           Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al.
     Savvas Zannettou, and Yang Zhang. HateBench: Bench-
                                                                           Llama 2: Open foundation and fine-tuned chat models.
     marking Hate Speech Detectors on LLM-Generated
                                                                           arXiv preprint arXiv:2307.09288, 2023. 2, 13, 17
     Content and Hate Campaigns. In USENIX Security Sym-
     posium (USENIX Security). USENIX, 2025. 2                        [62] Adaku Uchendu, Zeyu Ma, Thai Le, Rui Zhang, and
                                                                           Dongwon Lee. TURINGBENCH: A benchmark envi-
[53] Yuhui Shi, Qiang Sheng, Juan Cao, Hao Mi, Beizhe
                                                                           ronment for turing test in the age of neural text genera-
     Hu, and Danding Wang. Ten words only still help: Im-
                                                                           tion. In Findings of the Association for Computational
     proving black-box ai-generated text detection via proxy-
                                                                           Linguistics: EMNLP 2021, Virtual Event / Punta Cana,
     guided efficient re-sampling. In International Joint Con-
                                                                           Dominican Republic, 16-20 November, 2021, pages
     ferences on Artifical Intelligence (IJCAI), pages 494–
                                                                           2001–2016. Association for Computational Linguistics,
     502. ijcai.org, 2024. 14, 19
                                                                           2021. 2
[54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda
                                                                      [63] Christoforos Vasilatos, Manaar Alam, Talal Rahwan,
     Askell, Ariel Herbert-Voss, Jeff Wu, Alec Radford, and
                                                                           Yasir Zaki, and Michail Maniatakos. Howkgpt: In-
     Jasmine Wang. Release strategies and the social impacts
                                                                           vestigating the detection of chatgpt-generated univer-
     of language models. CoRR, abs/1908.09203, 2019. 2, 4,
                                                                           sity student homework through context-aware perplexity
     13
                                                                           analysis. arXiv preprint arXiv:2305.18226, 2023. 2
[55] Rafael A. Rivera Soto, Kailin Koch, Aleem Khan,
                                                                      [64] Longyue Wang, Chenyang Lyu, Tianbo Ji, Zhirui Zhang,
     Barry Y. Chen, Marcus Bishop, and Nicholas An-
                                                                           Dian Yu, Shuming Shi, and Zhaopeng Tu. Document-
     drews. Few-shot detection of machine-generated text
                                                                           level machine translation with large language models.
     using style representations. In International Conference
                                                                           In Houda Bouamor, Juan Pino, and Kalika Bali, editors,
     on Learning Representations (ICLR). OpenReview.net,
                                                                           Conference on Empirical Methods in Natural Language
     2024. 14, 19
                                                                           Processing (EMNLP), pages 16646–16661. ACL, 2023.
[56] Jinyan Su, Terry Yue Zhuo, Di Wang, and Preslav Nakov.                14
     Detectllm: Leveraging log rank information for zero-             [65] Longyue Wang, Chenyang Lyu, Tianbo Ji, Zhirui Zhang,
     shot detection of machine-generated text. In Findings of              Dian Yu, Shuming Shi, and Zhaopeng Tu. Document-
     the Association for Computational Linguistics: EMNLP                  level machine translation with large language models. In
     2023, Singapore, December 6-10, 2023, pages 12395–                    Conference on Empirical Methods in Natural Language
     12412. ACL, 2023. 2, 13                                               Processing (EMNLP), pages 16646–16661. ACL, 2023.
[57] Zhen Sun, Tianshuo Cong, Yule Liu, Chenhao                            1
     Lin, Xinlei He, Rongmao Chen, Xingshuo Han,                      [66] Yuntao Wang, Yanghe Pan, Miao Yan, Zhou Su, and
     and Xinyi Huang. PEFTGuard: Detecting Back-                           Tom H. Luan. A survey on chatgpt: Ai-generated con-
     door Attacks Against Parameter-Efficient Fine-Tuning.                 tents, challenges, and solutions. IEEE Open J. Comput.
     In 2025 IEEE Symposium on Security and Pri-                           Soc., 4:280–302, 2023. 3
     vacy (SP), pages 1620–1638. IEEE Computer So-
     ciety, 2025.   doi: 10.1109/SP61157.2025.00161.                  [67] Xwin-LM.      Xwin-lm 13b v0.2 model, 2024.
     URL https://doi.ieeecomputersociety.org/10.                           URL https://huggingface.co/Xwin-LM/Xwin-LM-
     1109/SP61157.2025.00161. 2                                            13B-V0.2. Accessed: 2025-02-15. 5


                                                                 11
[68] Alex Young, Bei Chen, Chao Li, Chengen Huang,
     Ge Zhang, Guanwei Zhang, Guoyin Wang, Heng Li,
     Jiangcheng Zhu, Jianqun Chen, et al. Yi: Open founda-
     tion models by 01. ai. arXiv preprint arXiv:2403.04652,
     2024. 5
[69] Rowan Zellers, Ari Holtzman, Hannah Rashkin, Yonatan
     Bisk, Ali Farhadi, Franziska Roesner, and Yejin Choi.
     Defending against neural fake news. Advances in neural
     information processing systems, 32, 2019. 2

[70] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xi-
     aolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang,
     Junjie Zhang, Zican Dong, et al. A survey of large lan-
     guage models. arXiv preprint arXiv:2303.18223, 2023.
     2

[71] Jingyi Zheng, Tianyi Hu, Tianshuo Cong, and Xinlei He.
     Cl-attack: Textual backdoor attacks via cross-lingual
     triggers. In Proceedings of the AAAI Conference on
     Artificial Intelligence, volume 39, pages 26427–26435,
     2025. 2

[72] Jiawei Zhou, Yixuan Zhang, Qianni Luo, Andrea G.
     Parker, and Munmun De Choudhury. Synthetic lies: Un-
     derstanding ai-generated misinformation and evaluating
     algorithmic and human solutions. In Annual ACM Con-
     ference on Human Factors in Computing Systems (CHI),
     pages 436:1–436:20. ACM, 2023. 1




                                                               12
A Introduction of LLMs in Detector Training                               text generation. This model can understand and generate
  Dataset                                                                 natural language text, manage everyday conversational ex-
                                                                          changes, and produce structured content in various forms,
In this paper, we have selected the most representative LLMs              such as articles, code, and summaries, across specialized
as our detection targets:                                                 domains.
• Llama-1 (Feb. 2023) [60], Llama-2 (Jul. 2023)[61], and                • Mixtral 8 × 7B (Dec. 2023) [22]: Developed by Mistral
  Llama-3 (Apr. 2024) [10]: The Llama series (from Llama-                 AI, this LLM employs a Sparse Mixture of Experts (SMoE)
  1 to Llama-3) launched by Meta are powerful and extremely               architecture. It has demonstrated exceptional performance
  popular open source models. This series of models enables               across multiple benchmarks, surpassing models like Llama-
  researchers to fine-tune diverse datasets, is highly scalable,          2 70B and GPT-3.5, especially excelling in tasks involving
  and is suitable for various research and development envi-              mathematics, code generation, and multilingual understand-
  ronments. The latest version, Llama-3, is equipped with a               ing.
  larger parameter size and optimized training architecture,
  making it perform better in text generation, context under-
  standing, and complex task processing.
                                                                        B    Introduction of Detectors
• ChatGPT/GPT-3.5 Turbo (Nov. 2022) [42]: GPT-3.5, an                   In this work, we adopt metric-based detectors from the MGT-
  optimized version of GPT-3 by OpenAI, was released in                 Bench framework to detect AIGTs, including:
  2022. By incorporating a Reinforcement Learning from                  • Log-Likelihood [54]: We evaluate the likelihood of text
  Human Feedback (RLHF) reward mechanism and human                        generation by computing its log-likelihood score under a
  feedback data, GPT-3.5 achieves significant improvements                specific language model. The model constructs a reference
  in accuracy and coherence in text generation. This version              distribution based on HWTs and AIGTs to calculate the log-
  includes the Text-DaVinci-003 and GPT-3.5 (or GPT-3.5                   likelihood score of the input text. A higher score suggests a
  Turbo), which focuses on fluent and natural multi-turn con-             greater likelihood of the text being LLM-generated.
  versations and serves as the core model for systems like              • Rank [12] and Log-Rank [39]: The Rank method identifies
  ChatGPT website.                                                        the source of generation by analyzing the ranking of each
• GPT4o-mini (Jul. 2024) [44]: Developed by OpenAI,                       word in the text. The model calculates the absolute ranking
  GPT4o-mini is a lightweight language model optimized                    of each word based on context and averages all word rank-
  from GPT-4o technology. This model is designed to deliver               ings to derive an overall score. Generally, a lower score
  efficient language processing capabilities that are suitable            indicates that the text is more likely to be LLM-generated.
  for applications with lower resource requirements. It sup-              Log-Rank, a variant of Rank, employs a logarithmic func-
  ports both text and visual input, with future plans to expand           tion when calculating each word’s ranking, enhancing the
  into audio and video input and output. Since its release, the           detection of AIGTs.
  GPT4o-mini has progressively replaced the GPT-3.5 Turbo               • Entropy [12]: The Entropy method calculates the average
  as the core model on the ChatGPT website.                               entropy value of each word in the text under context condi-
• Claude (Mar. 2023) [3], : Claude is an advanced AI assis-               tions. Studies show that AIGTs tend to have lower entropy
  tant developed by Anthropic. It is a closed-source model                values.
  designed to communicate efficiently and intuitively with              • GLTR [12]: GLTR is a supportive tool for detecting AIGTs
  users through NLP technology. Claude can understand and                 that use the ranking of words generated by a language model
  generate human language to assist users in completing a                 to sort the vocabulary of the text by predicted probability.
  variety of tasks, including answering questions, writing                Following Guo et al. [15], we employ the Test-2 feature
  content, and programming assistance.                                    to analyze the proportion of words in the top 10, 100, and
• Alpaca 7B (Mar. 2023) [59]: Alpaca 7B is a lightweight                  1000 ranks to assess the generative nature of the text.
  instruction-following model released by Stanford Univer-              • DetectGPT [39], NPR, and LRR [56]: The DetectGPT
  sity, based on Meta’s Llama-7B model and fine-tuned on                  method introduces minor perturbations into the original text
  the dataset of 52, 000 instruction-following examples. This             and observes changes in the model’s log probability to de-
  fine-tuning markedly enhances the model’s performance                   tect its source. AIGTs typically reside at the local optima of
  in understanding and executing task instructions. In eval-              the model’s log probability function, whereas HWTs show
  uations of single-turn instruction-following tasks, Alpaca              greater changes in log probability after perturbation. The
  demonstrates performance comparable to OpenAI’s Text-                   NPR method, similar to DetectGPT, focuses on observing
  DaVinci-003, exhibiting high-quality responses to instruc-              significant increases in log-rank following perturbations to
  tions.                                                                  differentiate between AIGTs and HWTs. By combining
• Vicuna 13B (Mar. 2023) [7]: Released by the LMSYS                       log-likelihood and log-rank information, the LRR method
  team, Vicuna 13B is based on Meta’s Llama-13B model                     captures the adaptiveness of generated texts in probability
  and trained on a large dataset of conversation data aggre-              distributions while reflecting the text’s ordinal preference
  gated from high-quality models like GPT-3.5. The goal is                relative to HWTs. This dual metric markedly enhances the
  to develop an open-source conversational model that ap-                 detection accuracy.
  proaches the quality of GPT-3.5.                                      We also consider model-based detectors, including:
• Moonshot-v1 (Oct. 2023) [40]: Developed by Moonshot                   • OpenAI Detector [54]: This detector fine-tunes a
  AI, Moonshot-v1 is an advanced large language model for                 RoBERTa [28] model using output data generated by the


                                                                   13
  GPT-2 large, which has 1.5 billion parameters, to predict               tionalities closely align with common use cases for LLMs,
  whether texts are LLM-generated.                                        such as writing and question-answering. Based on this, we
• ChatGPT Detector [15]: Trained using the HC3 dataset,                   hypothesize that there may be instances where users utilize
  this approach employs a RoBERTa model and various train-                LLMs to generate content on these platforms.
  ing methods to distinguish between human and AIGTs. We
  select one that uses only the response texts to align with
  other detectors, following instructions described by He [17].           D    Introduction of Open Source Datasets for
• ConDA [4]: This method enhances model discrimination of
                                                                               Training Detectors
  text sources in the feature space by maximizing the feature
  differences between generated samples and real samples.                 We consider 6 publicly available AIGT datasets and 5 com-
  It also introduces a contrastive learning loss to improve               mon supervised finetuning datasets as one part of AIGTBench.
  detection accuracy.                                                     • The MGT-Academic dataset [30], assembled from textual
• GPTZero [13]: A tool aimed at AIGT detection that analy-                  sources such as Wikipedia, arXiv, and Project Gutenberg,
  ses the perplexity and burstiness of texts to determine their             covers STEM, Social Sciences, and Humanities. It is gener-
  generative nature. GPTZero provides a public API interface                ated by various LLMs, including Llama3, GPT-3.5 Turbo,
  capable of returning a confidence score indicating whether                Moonshot, and Mixtral 8 × 7B, forming a comprehensive
  a text is LLM-generated.                                                  AIGT dataset.
• CheckGPT [31]: The CheckGPT uses the pre-trained                        • The Coco-GPT3.5 dataset [27], produced using OpenAI’s
  Roberta model to extract text features. Then, it uses LSTM                text-davinci-0035 model, incorporates entire newspaper
  to classify the text features and determine whether the text              articles from December 2022 to February 2023, reflecting
  is LLM-generated or human-generated.                                      the latest content of that period.
• LM-D Detector [21]: This approach adds an additional                    • The GPABench2 dataset [31], based on the GPT-3.5 Turbo
  classification layer to a pre-trained language model (like                model, focuses on 3 LLM-generated tasks: GPT-written,
  RoBERTa) and fine-tunes it to differentiate between human-                GPT-completed, and GPT-polished, all based on academic
  made and AIGTs. Inspired by the research of Li et al.[25],                abstracts. Due to the extensive amount of text generated by
  which shows that Longformer [64] has robust performance                   GPT-3.5 Turbo, we sampled around 100M tokens from this
  in detecting AIGT in out-of-domain texts, we also use the                 dataset for compilation.
  Longformer-base-4096 model to assess its performance in                 • The LWD dataset [55] involves texts generated by Llama-
  AIGT detection.                                                           2, GPT-4, and ChatGPT. Researchers designed specific
                                                                            prompts to “write an Amazon review in the style of the
C    Social Media Platforms                                                 author of the following review: <human review>”, where
To select suitable social media platforms for testing AIGT                  each prompt incorporates a real human-written Amazon
detection, we particularly consider the platform’s mainstream               review as a stylistic reference.
status, the diversity of content, and their unique characteris-           • The HC3 dataset [15], collected by researchers, comprises
tics. Ultimately, we choose Reddit, Medium, and Quora as                    nearly 40,000 questions and their answers from human
representative platforms.                                                   experts and ChatGPT, covering a broad range of fields in-
• Reddit [50] is a social discussion platform where users au-               cluding open-domain, computer science, finance, medicine,
   tonomously create and manage “subreddit” sections featur-                law, and psychology.
   ing diverse and rich content themes. All content on the site           • The AIGT dataset [53] samples human-generated content
   is categorized into different “subreddits” according to user             and content from seven popular open-source or API-driven
   interests, covering a wide range of topics from technology               LLMs, applied in real-world scenarios such as low-quality
   to social issues. We choose Reddit not only for its active               content generation, news fabrication, and student cheat-
   user base—with around 330M monthly active users—but                      ing. Due to the markedly lesser capabilities of GPT-2 XL
   also for its vast content diversity, including millions of sub-          and GPT-J compared to GPT-3.5, these models were not
   reddit topics, allowing it to cover a variety of discussion              included.
   scenarios.                                                             • Given that high-quality Supervised Finetuning (SFT)
• Medium [37] is an American online publishing platform                     datasets are frequently used for finetuning LLMs, and
   developed by Evan Williams and launched in August 2012.                  considering the lack of Claude and GPT-4 model-related
   It centers on high-quality original articles and blog content            content in the AIGT detection datasets, we also incorpo-
   and exemplifies social journalism, known for its content’s               rate four SFT datasets with instruction-following features:
   depth, length, and professionalism.                                      Claude2-Alpaca2 , Claude-3-Opus-Claude-3.5-Sonnet-
• Quora [48] is a platform to gain and share knowledge. It                  9k3 , GPTeacher/GPT-4 General-Instruct4 , and Instruc-
   enables users to ask questions and connect with people                   tion in the Wild5 .
   who provide unique insights or quality answers. Users can
                                                                          2 https://github.com/Lichang-Chen/claude2-alpaca.
   pose questions and receive answers from other users on top-            3 https://huggingface.co/datasets/QuietImpostor/Claude-3-
   ics ranging from daily life to highly specialized academic,            Opus-Claude-3.5-Sonnnet-9k.
   technical, and professional queries.                                   4 https://github.com/teknium1/GPTeacher/tree/main/Instruct.

We have selected these 3 platforms because their main func-               5 https://github.com/XueFuzhao/InstructionWild.




                                                                     14
E Data Preprocessing for the SM-D and AIGT-                                 You are a content creator on Quora/Reddit.
  Bench Datasets                                                               Your task is to generate a thoughtful and insightful
                                                                            answer to the following question. Follow these guide-
                                                                            lines:
SM-D Dataset. For the SM-D dataset, we exclude texts with                      1. Provide a clear and comprehensive explanation
fewer than 150 characters (including spaces) and texts where                that addresses the question thoroughly.
the proportion of English content is below 90%. Plus, we                       2. Use simple, relatable language to connect with a
observe that LLMs’ responses often contain redundant or                     broad audience, making the content easy to understand.
irrelevant content. For example, many LLMs’ generated                          3. Highlight key points with examples or anecdotes
texts include irrelevant phrases at the beginning, such as                  where applicable, to make the answer more engaging.
  “Of course. . . ” or “Hey there. . . ” . Additionally, we find               4. Add a conversational and friendly tone to make
that responses generated by the Llama model often repeti-                   the answer feel more approachable.
tively display strings of numbers or specific symbols, hitting                 5. Ensure the answer is well-structured, with an in-
the generation length limit instead of providing a complete an-             troduction, body, and conclusion, for better readability.
                                                                               6. Where relevant, include unique insights or per-
swer. like “. . . .throwaway11111. . . ” . We filter and remove
                                                                            spectives to make the answer stand out.
these anomalous generated contents to enhance the accuracy                     7. Respond with the generated answer only and noth-
of our dataset.                                                             ing else.
                                                                               Here is the question: “{question}”
AIGTBench Dataset. For the AIGTBench dataset, we exclude
texts with fewer than 150 characters (including spaces) and               Below are two task prompts designed for summarizing
texts where the proportion of English content is below 90%.             Medium articles and writing detailed articles based on those
                                                                        summaries for Medium articles.

                                                                            You are a helpful, respectful, and honest assistant.
                                                                              Summarize the following content succinctly:
                                                                              “{content}”
                                                                              Summary:
F Task Prompts for Generated AIGTs from
  Social Media
                                                                            You are a helpful, respectful and honest assistant. Al-
Inspired by [31], below are designed task prompts for polish-               ways answer as helpfully as possible, while being safe.
ing texts on Medium, Quora, and Reddit.                                       Write a detailed article based on the summary below,
                                                                            following these guidelines:
                                                                              1. Ensure it flows naturally and is enjoyable to read.
                                                                               2. Use simple and relatable language for a broad
   Please act as a social media platform Medium/Quo-                        audience.
   ra/Reddit content creator.                                                  3. Highlight key points in a concise, impactful way.
      Your task is to polish the following content. Follow                    4. Make it conversational and friendly.
   these guidelines:                                                           5. Add an engaging tone where appropriate.
      1. Ensure the content flows naturally and is enjoyable                   Summary:
   to read.                                                                   “{summary content}”
      2. Use simple and relatable language to connect with                    Article:
   a broad audience.
      3. Highlight key points in a concise and impactful
   way.                                                                 G     Detailed Performance of OSM-Det
      4. Make the content feel more conversational and
   friendly.                                                            Table A6 presents the performance of OSM-Det on indi-
      5. Where appropriate, add an engaging tone to draw                vidual platform-specific datasets within AIGTBench. The
   the reader in.                                                       results show that OSM-Det achieves consistently high accu-
      6. Respond with the revised content only and nothing              racy across all three platforms, with accuracy scores of 0.995,
   else:                                                                0.999, and 0.984 on Medium, Quora, and Reddit, respectively.
      Here is the original content: “{content}”                            Figure A5 illustrates the accuracy and F1-score across dif-
                                                                        ferent text lengths in AIGTBench. We observe that accuracy is
                                                                        relatively lower for shorter texts, with an accuracy of approxi-
                                                                        mately 0.940 for texts between 0 − 149 characters. However,
                                                                        for texts exceeding 150 characters, accuracy improves signifi-
   Below are designed task prompts for answering the ques-              cantly to above 0.980. Both accuracy and F1-score continue
tions on Quora and Reddit.                                              to increase as text length increases.


                                                                   15
   To ensure the reliability of our conclusions, we filter out         well with the generation patterns of LLMs. Another factor
texts shorter than 150 characters from SM-D in our paper.              is that technical terminology inherently possesses objectivity,
                                                                       with readers typically focusing more on information accu-
H Details About the Collection of High-                                racy rather than storytelling, making AIGTs easier to accept.
                                                                       Moreover, technical communities tend to view AI tools as
  Frequency Words and Model Interpretation
                                                                       “advanced productivity enhancers” rather than ethical threats,
  Analysis Methods                                                     further normalizing the use of AIGTs in technical subjects.
H.1    Collection of High-Frequency Words                                  The phenomenon of “AIGTs receiving lower engagement
                                                                       than HWTs but with limited disparity” may be related
We use the Spacy library [20] to classify the part-of-speech of
                                                                       to cognitive psychology factors. We speculate that some
words in the AIGTBench, specifically dividing them into ad-
                                                                       users possibly rely on heuristic judgments (such as language
jectives, adverbs, and connectives. We then select around the
                                                                       fluency and information density) to evaluate content, mak-
top 20 words for human-preferred and AI-preferred categories,
                                                                       ing it difficult for them to clearly distinguish between high-
respectively. For detailed results, refer to Table A5.
                                                                       quality AIGTs and HWTs. This explains why some AIGT
H.2    Model Interpretation Analyze Methods                            still achieves fundamental interaction measures. However,
                                                                       when content involves subjective perspectives, users tend to
Here are the details and how we implement the two different            activate deeper analytical processes, and AIGTs often lack
methods:                                                               personal experiential grounding. This flattening of affective
• Integrated Gradients give an importance score to each                expression triggers user vigilance, consequently diminishing
  input value by calculating the gradient of the detector. We          interaction behaviors.
  follow [24] for implementation.
                                                                           When it comes to why “low-follower authors tend to rely
• Shapley Value is originally introduced in [51] and recently
                                                                       more on AI”, one likely explanation is that some authors with
  apply to machine learning interpretation. It quantifies the
                                                                       smaller followers (0-1K) are often less experienced in writing
  impact of each feature by perturbing the input value and ob-
                                                                       quality content, leading them to prioritize using AI to sustain
  serving the contributions in the prediction. We follow [32]
                                                                       their content output. Meanwhile, high-follower authors (>5K)
  for implementation.
                                                                       often consciously limit their use of AI. By doing so, they
                                                                       can preserve their authentic human writing style, which helps
I   Deeper Analysis of the Result                                      reinforce their expert credibility and protects their relationship
Regarding the results of “Evaluation on Social Media Plat-             with their audience.
forms”, the AAR observed on Medium, Quora, and Red-                        We have the following recommendations for platform oper-
dit show divergent trends in AI adoption. Medium’s con-                ators, content creators, and readers:
sistently high AAR suggests that its longer-form, polished             • For platform operators: AI-generated content presents
content format may be particularly conducive to AI-assisted               dual challenges of content authenticity and user trust. Our
creation. The early and substantial adoption may indicate                 research shows that although platforms have established AI
that Medium’s creators see AI tools as valuable for improving             content disclosure policies, compliance rates fall far below
article efficiency. While Medium’s policy permits AI-assisted             expectations. Platforms may choose to implement defensive
content with disclosure, our analysis (based on syntactic pat-            strategies, such as AI detection and content screening, or
terns and keyword detection) finds that just 0.81% of authors             integrative strategies incorporating AI as a creative aid.
compiled. This suggests that many users may not be follow-                Looking ahead, we foresee that AI content labeling will
ing the platform’s guidelines. On the other hand, Quora’s                 become standardized, alliances will form among platforms
adoption pattern tends to fluctuate. The platform experienced             to harmonize policies, and the relationship between AI and
a temporary surge after introducing the Poe (AI tools), but               human creation will evolve from substitution to symbiosis.
this trend did not persist, possibly indicating a misalignment            This requires platforms to develop mechanisms that foster
between AI capabilities and community expectations. In con-               such an ecosystem proactively.
trast, Reddit maintains a low AAR, strongly resisting AIGT             • For content creators: We recommend establishing clear
despite the platform’s text-centric nature. This phenomenon               guidelines for AI usage: AI tools should serve as assis-
may stem from Reddit’s vertically organized subcommuni-                   tants, primarily supporting essential tasks such as grammar
ties (subreddits), where members reinforce identity through               checks and formatting adjustments. The core aspects of
shared jargon and memes, content that current LLMs strug-                 creation, central arguments, narrative logic, and emotional
gle to generate. On top of that, active community modera-                 expression, must remain human-driven. Besides, if human-
tion behaviors serve as a self-purifying mechanism, such as               original content is mistakenly flagged as AIGT, we encour-
downvoting "overly fluent" or suspicious content. Thus, the               age authors to appeal and request formal disclosure of the
platform’s strong community governance and inherent culture               decision basis. This demand for transparency safeguards
pose barriers to AI content adoption.                                     creators’ rights and drives platforms to refine their AIGT
   Regarding the underlying reasons for “significantly                    detection algorithms, leading to fairer content evaluation
higher AAR in technical fields (including Technology and                  mechanisms.
Software Development)”, One possible explanation is that               • For readers: We recommend cultivating critical thinking
technical content tends to be highly structured, which fits               when engaging with AI content. For instance, check for AI


                                                                  16
    assistance disclosures at the beginning of articles, analyze
    texts to learn general AI-generated features, and maintain
    skepticism toward factual claims. AI may provide incorrect
    answers to complex questions. Furthermore, when encoun-
    tering uncertain content, readers can use accessible tools
    (e.g., GPTZero) to aid judgment. We also urge readers
    to report unlabeled AI content to platform administrators,
    helping maintain the community’s integrity.

              Dataset      Type        Sentence Number
                        Llama Series      1, 881, 733
              Medium     GPT Series        681, 480
                           Human          2, 033, 105
                        Llama Series      1, 974, 368
               Quora     GPT Series        721, 878
                           Human           569, 749
                        Llama Series      2, 892, 584
               Reddit    GPT Series       1, 391, 054
                           Human          2, 695, 271
                          AIGTs           9, 543, 097
                Total
                          HWTs            5, 298, 125
                                                                                  (a) Token length distribution in the training set.
Table A1: Sentence number statistics of our generated datasets
(Llama Series include Llama-1, 2, 3; GPT Series include GPT-
3.5, GPT4o-mini).


J     Ablation Study on Social Media Data
To validate the necessity of the social media data collection for
AIGTBench, we conducted an ablation study comparing OSM-
Det performance with and without the social media training
subsets on AIGTBench. As shown in Table A2, OSM-Det
trained only on open-source datasets exhibits poor perfor-
mance when evaluated on social media test sets, particularly
on Quora and Reddit platforms. This performance gap demon-
strates that traditional benchmarks fail to capture the linguistic                (b) Token length distribution in the testing set.
patterns and stylistic variations inherent in social media con-
tent. The new collected datasets created address this issue,
improving model robustness.

Table A2: Performance comparison of OSM-Det trained on
AIGTBench without social media data.

              Platform      Accuracy        F1-score
              Medium           0.975          0.967
              Quora            0.684          0.678
              Reddit           0.631          0.608


                                                                                 (c) Token length distribution in the validation set.

                                                                          Figure A1: Token length distribution in the training, testing, and
                                                                          validation sets, calculated by the Llama-2 tokenizer [61].




                                                                     17
Figure A2: Stacked area chart shows the monthly proportions
of 9 topics.




   (a) Number of Likes.           (b) Number of Comments.

Figure A3: Differences between predicted AIGTs and predicted
HWTs compressed using a log10 transformation.




 Figure A4: Timeline of authors’ earliest adoption of AIGTs.




                                                               18
        Dataset                  Type             Sentence Number                                 Domain
                              Llama3                   1, 478, 485              STEM (Physics, Math, Biology, CS,
                            Mixtral 8×7B               2, 639, 498              EE, Statistics, Chemistry, Medicine),
   MGT-Academic [30]         Moonshot                   726, 357                Social Science (Education, Economy,
                              GPT-3.5                  1, 611, 244            Management), Humanities (Literature, Law,
                              Human                    6, 007, 476                    Art, History, Philosophy)
                               GPT-3.5                   79, 647
    Coco-GPT3.5 [27]                                                                               News
                               Human                     55, 565
                               GPT-3.5           12, 648, 338 (Sample)
    GPABench2 [31]                                                            Computer Science, Physics, Social Sciences
                               Human                   1, 065, 860
                               Llama2                   94, 732
                               GPT-3.5                  95, 443
       LWD [55]                                                                            Finance, Social Media
                                GPT-4                    62, 632
                               Human                    106, 952
                               Llama2                    6, 967
                             Alpaca 7B                   6, 083
                             Vicuna 13B                  7, 028
       AIGT [53]                                                                Soical media, News, Academic Writing
                              GPT-3.5                    8, 022
                               GPT-4                      7, 156
                               Human                     12, 228
                               GPT-3.5                  184, 692                   Open-domain, Finance, Medicine,
       HC3 [15]
                               Human                    347, 423                        Law, and Psychology

                                Table A3: Statistics of open-source datasets (part 1).




                            Dataset                           Type        Sentence Number              Domain
                        Claude2-Alpaca                     Claude-2             404, 051             Open-domain
                                                           Claude-3             276, 246
           Claude-3-Opus-Claude-3.5-Sonnnet-9k                                                       Open-domain
                                                            Human                37, 785
                                                            GPT-4                74, 160
              GPTeacher/GPT-4 General-Instruct                                                       Open-domain
                                                            Human                24, 465
                                                            GPT-4               354, 801
                         Alpaca_GPT4                                                                 Open-domain
                                                            Human                22, 253
                   Instruction in the Wild                  GPT-3.5             300, 424             Open-domain

                                Table A4: Statistics of open-source datasets (part 2).




   Category               Words
   Human top
                          ‘little’, ‘small’, ‘last’, ‘able’, ‘bad’, ‘next’, ‘right’, ‘most’, ‘long’, ‘old’, ‘much’, ‘sure’, ‘great’,
frequency words
                          ‘actually’, ‘again’, ‘probably’, ‘much’, ‘very’, ‘pretty’, ‘already’, ‘since’, ‘against’, ‘yet’
     AI top
                          ‘various’, ‘significant’, ‘positive’, ‘complex’, ‘original’, ‘free’, ‘specific’, ‘unique’, ‘crucial’, ‘clear’,
frequency words
                          ‘human’, ‘personal’, ‘essential’, ‘particularly’, ‘especially’, ‘truly’, ‘instead’, ‘here’, ‘rather’,
                          ‘additionally’, ‘despite’, ‘due to’, ‘following’

                       Table A5: Categorization of words into human and AI characteristics.




                                                              19
             Platform      Accuracy       F1-score
             Medium          0.995         0.995
              Quora          0.999         0.999
             Reddit          0.984         0.984

Table A6: Performance of OSM-Det on AIGTs within AIGT-
Bench across different platforms.




Figure A5: Performance of OSM-Det across varying text lengths
on AIGTBench.



                                              Performance
  Category   Dataset
                                           Accuracy   F1-score
             QwQ-32B-Preview [34]           0.999      0.999
  Unseen     Gemini-2.0-Flash [47]          0.993      0.997
  Model      Deepseek-R1-Llama-70B [35]     0.999      0.999
             Roleplay-English [41]          0.999      0.999
  Unseen
             Mannerstral-dataset [19]       0.943      0.968
  Domain
             InternVL-SA-1B-Captio [46]     0.998      0.999

Table A7: Test OSM-Det in the wild (all datasets from Hugging-
Face).




                                                                 20
                                    Prediectd Logits
                                   0.999906, 0.000094




                                 (a) Human written text (Reddit)


                                     Prediectd Logits
                                     0.000093, 0.999907




                             (b) GPT4o-mini generated text


                                   Prediectd Logits
                                   0.000096, 0.999904




                              (c) GPT3.5 generated text


                                   Prediectd Logits
                                   0.000095, 0.999905




                             (d) Llama3 generated text


Figure A6: Case study of word-level analysis through Integrated Gradients on Reddit.




                                          21
                                   Prediectd Logits
                                  0.999906, 0.000094




                                (a) Human written text (Reddit)


                                    Prediectd Logits
                                    0.000093, 0.999907




                            (b) GPT4o-mini generated text


                                  Prediectd Logits
                                  0.000096, 0.999904




                             (c) GPT3.5 generated text


                                  Prediectd Logits
                                  0.000095, 0.999905




                            (d) Llama3 generated text


Figure A7: Case study of sentence-level analysis through Shaplay Value on Reddit.




                                         22
                                 Prediectd Logits
                                0.999906, 0.000094




                             (a) Human written text (Reddit)


                                  Prediectd Logits
                                 0.000093, 0.999907




                          (b) GPT4o-mini generated text


                                Prediectd Logits
                                0.000096, 0.999904




                           (c) GPT3.5 generated text


                                Prediectd Logits
                                0.000095, 0.999905




                           (d) Llama3 generated text


Figure A8: Case study of word-level analysis through Shaplay Value on Reddit.




                                       23
Figure A9: Case study of word-level analysis through Integrated Gradients on Quora.




                                        24
                                   Prediectd Logits
                                  0.999906, 0.000094




                             (a) Human written text (Quora)
                                    Prediectd Logits
                                   0.000093, 0.999907




                            (b) GPT4o-mini generated text


                                  Prediectd Logits
                                  0.000096, 0.999904




                             (c) GPT3.5 generated text


                                   Prediectd Logits
                                  0.000095, 0.999905




                              (d) Llama3 generated text



Figure A10: Case study of sentence-level analysis through Shaplay Value on Quora.




                                         25
                                 Prediectd Logits
                                0.999906, 0.000094




                             (a) Human written text (Quora)

                                  Prediectd Logits
                                  0.000094, 0.999906




                          (b) GPT4o-mini generated text


                                Prediectd Logits
                                0.000096, 0.999904




                           (c) GPT3.5 generated text


                               Prediectd Logits
                               0.000095, 0.999905




                            (d) Llama3 generated text



Figure A11: Case study of word-level analysis through Shaplay Value on Quora.




                                        26
                                    Prediectd Logits
                                    0.999906, 0.000094




                              (a) Human written text (Medium)

                                      Prediectd Logits
                                     0.000095, 0.999905




                              (b) GPT4o-mini generated text


                                    Prediectd Logits
                                    0.000094, 0.999906




                               (c) GPT3.5 generated text

                                   Prediectd Logits
                                   0.000094, 0.999906




                               (d) Llama3 generated text


Figure A12: Case study of word-level analysis through Integrated Gradients on Medium.




                                           27
                                   Prediectd Logits
                                  0.999906, 0.000094




                            (a) Human written text (Medium)

                                    Prediectd Logits
                                   0.000095, 0.999905




                            (b) GPT4o-mini generated text

                                  Prediectd Logits
                                  0.000094, 0.999906




                              (c) GPT3.5 generated text


                                 Prediectd Logits
                                 0.000094, 0.999906




                              (d) Llama3 generated text



Figure A13: Case study of sentence-level analysis through Shaplay Value on Medium.




                                          28
                                 Prediectd Logits
                                0.999906, 0.000094




                          (a) Human written text (Medium)


                                  Prediectd Logits
                                  0.000095, 0.999905




                           (b) GPT4o-mini generated text

                                 Prediectd Logits
                                0.000094, 0.999906




                             (c) GPT3.5 generated text


                               Prediectd Logits
                               0.000094, 0.999906




                             (d) Llama3 generated text



Figure A14: Case study of word-level analysis through Shaplay Value on Medium.




                                        29
