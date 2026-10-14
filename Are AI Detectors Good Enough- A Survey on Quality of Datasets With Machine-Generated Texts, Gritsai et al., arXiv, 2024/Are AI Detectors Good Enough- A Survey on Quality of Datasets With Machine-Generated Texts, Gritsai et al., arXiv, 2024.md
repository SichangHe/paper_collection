                                                 Are AI Detectors Good Enough? A Survey on Quality of Datasets with
                                                                     Machine-Generated Texts
                                                     German Gritsai* 1 , Anastasia Voznyuk* 2 , Andrey Grabovoy1 , Yury Chekhovich 1
                                                                                            1
                                                                                             Advacheck OÜ, Tallinn, Estonia
                                                                           2
                                                                               Moscow Institute of Physics and Technology, Moscow, Russia
                                                                                  gritsai@advacheck.com, vozniuk.ae@phystech.edu
arXiv:2410.14677v3 [cs.CL] 7 Mar 2025




                                                                    Abstract                                  eral tens of percent (Liang et al. 2024; Gritsay et al. 2023a).
                                                                                                              More than 60,000 scientific papers in the last year alone
                                          The rapid development of autoregressive Large Language
                                          Models (LLMs) has significantly improved the quality of
                                                                                                              contained evidence of the use of machine generation (Gray
                                          generated texts, necessitating reliable machine-generated text      2024). All of that proves that it is crucial to develop systems
                                          detectors. A huge number of detectors and collections with          able to counter the misuse of artificial data and signal to the
                                          AI fragments have emerged, and several detection methods            reader that the content they read is generated.
                                          even showed recognition quality up to 99.9% according to               Another concern is the Web, overflowing with machine-
                                          the target metrics in such collections. However, the quality of     generated content, often of poor quality. Such texts con-
                                          such detectors tends to drop dramatically in the wild, posing       tribute bias to publicly available texts on the Internet,
                                          a question: Are detectors actually highly trustworthy or do         through false facts, hallucinations and spelling errors. Given
                                          their high benchmark scores come from the poor quality of           the current agenda of using texts from the Internet to train
                                          evaluation datasets? In this paper, we emphasise the need for
                                                                                                              new language models, all this bias will be inadvertently
                                          robust and qualitative methods for evaluating generated data
                                          to be secure against bias and low generalising ability of fu-       added to the model. Moreover, (Villalobos et al. 2022) re-
                                          ture model. We present a systematic review of datasets from         vealed that the human-written data will run out by 2028.
                                          competitions dedicated to AI-generated content detection and        That means that the training sets for language models in the
                                          propose methods for evaluating the quality of datasets con-         future will include a large amount of generated content. Such
                                          taining AI-generated fragments. In addition, we discuss the         self-consuming will result in the substantial degradation of
                                          possibility of using high-quality generated data to achieve         the model’s abilities (Alemohammad et al. 2023). Further-
                                          two goals: improving the training of detection models and           more, the trend is evolving in such a way that human-written
                                          improving the training datasets themselves. Our contribution        texts on almost any topic will be much harder to retrieve.
                                          aims to facilitate a better understanding of the dynamics be-       While for texts dated even 5 years ago we are confident as
                                          tween human and machine text, which will ultimately sup-
                                                                                                              the usage of generation was extremely rare, we cannot state
                                          port the integrity of information in an increasingly automated
                                          world.                                                              the same for more recent texts.
                                                                                                                 Therefore, detectors capable of distinguishing human-
                                                                                                              written texts from AI-generated texts and whose detection
                                                             1    Introduction                                quality can be guaranteed, are necessary for many fields. We
                                        The quality of large language models (LLMs) has grown                 believe that one of the key factors for building reliable detec-
                                        tremendously in the last five years, making their output al-          tors is the high-quality artificial text collections that can be
                                        most indistinguishable from human-written texts (Chang                used for training and evaluation. In this paper, we would like
                                        et al. 2024). This expanded the application fields of these           to estimate the quality of the available generated texts from
                                        models, as many routine tasks can be entrusted to them                competitions and research papers. Sometimes we see that
                                        nowadays. However, they can be used for creating texts                some methods from participants of the competitions reach
                                        that are intended to be written and fact-checked by hu-               almost perfect (up to 99.9%) metric score, meanwhile in the
                                        mans. An example of such misuse is the generation of fake             wild we observe a noticeable decline in performance. Such
                                        news (Zellers et al. 2019; Zhou et al. 2023), which can               results look confusing, because the models become more
                                        mislead readers of such generated content. Teachers raise             and more advanced, seemingly making the detecting task
                                        another concern, as many students complete assignments                more challenging, meanwhile participants of competitions
                                        with LLMs (Koike, Kaneko, and Okazaki 2024; Ma et al.                 still reach almost perfect scores, bringing up the question
                                        2023), undervaluing the purpose of the educational process.           about quality of generated data in the provided datasets. Are
                                        Machine-generated fragments also appear in academic arti-             the devised methods really good or is the data easy enough
                                        cles more often with the growth of chatbots and reach sev-            for detectors to solve the seemingly hard detection task?
                                            * These authors contributed equally.
                                                                                                                 Our contributions are as following
                                        Copyright © 2025, Association for the Advancement of Artificial       1. We systemize information about existing datasets from
                                        Intelligence (www.aaai.org). All rights reserved.                        the research papers and competitions, dedicated to the
   detection of AI-generated content task.                         computational, and human resources. The human evaluators
2. We suggest methods that may be helpful for evaluating           should check that the dataset does not contain corrupted gen-
   the quality of the generated data and the datasets aimed to     erations, that the texts are coherent and grammatically cor-
   use for binary classification between human and machine         rect. We will describe the datasets we used in our analysis
   texts.                                                          and experiments in Section 3.

                    2   Related Work                               2.4   Shared Tasks on AI-Generated content
                                                                         Detection
2.1   The Task of AI-generated text detection
                                                                   Shared tasks advance research on detecting AI-generated
The task of AI-generated text detection task is generally
                                                                   content forward by offering new variations on tasks and
stated as a text classification task, which means that the input
                                                                   providing data for evaluation, encouraging participants to
is a text sequence and the output is a discrete, usually binary,
                                                                   come up with novel ideas for detectors robust to the change
class prediction. When the task is binary, the common labels
                                                                   of language, domain, or generating model. Participants ex-
are “AI” or “human”, whereas multiclass classification fo-
                                                                   plore approaches ranging from transfer learning on com-
cusses on distinguishing several language models. The last
                                                                   plex text features to utilising and fine-tuning LLMs for these
task is usually called authorship attribution. Finally, more
                                                                   tasks (2022; 2022; 2023b; 2024; 2024; 2024; 2024; 2024).
complex task suggests to determine the borders betweens
                                                                   These efforts have highlighted challenges such as handling
fragments from different authors, for example between hu-
                                                                   multilingual data and adapting to rapidly evolving genera-
man author and some LLM author.
                                                                   tive models. Some participants also provide some analysis
   The first approaches to tackle the classification prob-
                                                                   of the given data or even discuss some flaws with the gener-
lem were to utilise some linguistic, stylometric, and statis-
                                                                   ated texts (Voznyuk and Konovalov 2024).
tical features for classifiers (Jawahar, Abdul-Mageed, and
Lakshmanan 2020; Fröhling and Zubiaga 2021). However,
while these methods performed well for the texts from                                     3   Datasets
the first language models, nowadays models are advanced            3.1   Datasets From Shared Tasks
enough to output texts that are almost indistinguishable from      The most common tasks in shared tasks are binary classi-
human-written ones, therefore these methods are currently          fication and authorship attribution, with binary classifica-
not reliable enough. The next category are zero-shot meth-         tion being the prevalent task, therefore, in this work, we fo-
ods that employ metrics, such as perplexity or its modi-           cused only on it. All chosen shared tasks contain texts in En-
fications (Hans et al. 2024), which can be helpful as an           glish, unless stated otherwise. Here we give a brief overview
inference method when training is not available. Another           of each task, as well as some quantitative statistics of the
approach that do not require training is perturbing texts,         texts in Table 1, whereas a more detailed description, such
which can also provide valuable information. For example,          as models used for generation or domains of the presented
one can compare log-probabilities between between origi-           texts, can be found in Appendix A.
nal and perturbed texts, as described in DetectGPT (Mitchell
et al. 2023) method. Finally, methods based on fine-tuning          • DAGPap 2022 (Kashnitsky et al. 2022) introduced a
encoder-based models, such as DeBERTa (He et al. 2021),               dataset of human- and machine-written scientific ex-
are currently considered the state-of-the-art approach for the        cerpts collected by Elsevier.
detection task (Uchendu et al. 2021; Macko et al. 2023).            • RuATD 2022 (Shamardina et al. 2022) focused on
                                                                      human- and machine-written documents in Russian, cov-
2.2   Evaluating Generated Text                                       ering a wide range of themes.
As for evaluating the quality of the generated data itself, it      • AuTexTification 2023 (Sarvazyan et al. 2023) provided
has become more common to evaluate it with the help of                texts in English and Spanish, covering five distinct do-
LLMs (Xu et al. 2023). This approach does not require any             mains.
human reference, unlike ROUGE (Lin 2004). However, the
output of model-evaluator needs to be unified, is not always        • IberAuTexTiification 2024 (Sarvazyan et al. 2024) ex-
interpretable, and model-evaluator scores can be skewed.              panded on the previous competition with a multilingual
Alternative approach is suggested by (Zhu and Bhat 2020),             (six Iberian languages), multi-domain, and multi-model
where the text is evaluated based on several linguistic crite-        focus.
ria, such as grammar or coherence.                                  • Voight-Kampff Generative AI Authorship Verifica-
                                                                      tion 2024 (Ayele et al. 2024), hereafter referred to
2.3   Datasets with Artificial Content                                as PAN 2024, tasked participants with identifying the
There are a number of surveys of machine-generated con-               human-authored text from two samples – one human-
tent detection with an overview of the datasets (Jawahar,             written and one machine-generated.
Abdul-Mageed, and Lakshmanan 2020; Wu et al. 2023),                 • SemEval 2024 Task 8 (Wang et al. 2024c) addressed do-
however, few works focus on the quality of data in the                main, generator, and language shifts in generated texts.
available datasets, despite it being an important aspect of           Training data included multiple languages such as Chi-
the task. Building AI-generated content detectors requires            nese, Urdu, and Russian, but the test set was limited to
high-quality labelled data that involve substantial financial,        English, Italian, German, and Arabic.
Dataset                        Language             Num. of        Num. of Texts,         Average Length,             Median Length,
                                                   Texts, 103       G / H, 103                 G/H                        G/H

GPT2                                en                  1250          1000 / 250             2941 / 2616                3245 / 2459
TweepFake                           en                  20.7          10.4 / 10.4             104 / 118                   89 / 94
HC3                              en, zh                 85.4          26.9 / 58.5             1011 / 681                1012 / 422
GhostBuster                         en                   21             18 / 3               3345 / 3391               3440 / 2911.5
MGTBench                            en                  23.7           20.7 / 3              1596 / 3391               1226 / 2911.5
MAGE                                en                  436         152.3 / 284.2            1139 / 1282                 706 / 666
M4                           en, zh, ru, bg,            89.5          44.7 / 44.7            1588 / 3162                1454 / 1697
                                  ur, id
OutFox                              en                  57.6          43.2 / 14.4            2686 / 2238                2311 / 1992

DAGPap22                            en                   5.3           3.6 / 1.6              799 / 1180               680 / 1126.5
RuATD                               ru                  129           64.5 / 64.5             237 / 221                   99 / 95
AuTex                             en, es                65.9          33.1 / 32.8             315 / 297                  386 / 351
IberAuTex                    es, en, ca, gl,             98           52.5 / 45.4            1037 / 1058                981 / 1018
                                 eu, pt
PAN24                               en                  15.2          14.1 / 1.1             2641 / 3007                2731 / 2868
SemEval24 Mono                      en                  34.2           18 / 16.2             2465 / 2358               2570 / 2083.5
SemEval24 Multi               en, ar, de, it            42.3          22.1 / 20.2            2218 / 2257                2270 / 2032
MGT-1 Mono                          en                  610.7       381.8 / 228.9            1448 / 1541                1208/ 1080
MGT-1 Multi                 en, zh, it, ar, de,         674         416.1 / 257.9            1423 / 1445                1195 / 1032
                              ru, bg, ur, id

                        Table 1: Statistics of the texts in the datasets from the shared tasks and research papers.


 • MGT Detection Task 1 (COLING 2025) (Wang et al.                          prompts.
   2025) was built on SemEval 2024 Task 8 by incorpo-                     • HC3 (Human Chatbot Conversations Corpus) (Su et al.
   rating data generated by novel LLMs and expanding the                    2024) features conversations between humans and chat-
   multilingual coverage of the train and test sets.                        bots, primarily used for research on chatbot responses
                                                                            and human-AI interaction analysis. This dataset is avail-
3.2      Datasets from Research Papers                                      able for both English and Chinese, but we have focused
The number of collections with generated content has started                only on the former.
to grow with an increasing number of available generators.                • GhostBuster (Verma et al. 2024) aimed at detecting
Quite often, researchers, together with a new approach for                  AI-generated content by comparing it to human-written
AI content detection, publish a parallel dataset on which                   text, often used in the context of identifying machine-
they have validated their method. In this paper, our aim                    generated misinformation or spam.
was to pick collections with human- and machine-generated
excerpts that are the most common and cited in other re-                  • MGTBench (Machine Generated Text Benchmark) (He
searchers’ publications. Similarly to previous subsection,                  et al. 2023) is a benchmark dataset designed to evalu-
here we give a brief overview of each chosen datasets, de-                  ate the quality of machine-generated text across various
scribe some statistics about the texts in Table 1, and add a                tasks, including fluency, coherence, and creativity.
more detailed description in Appendix A.                                  • MAGE (Model Augmented Generative Evaluation) (Li
 • GPT2 Output Dataset1 consists of text outputs gener-                     et al. 2024) evaluates the performance of generative mod-
   ated by GPT-2 models of different sizes across various                   els by comparing outputs with human annotations, aiding
                                                                            in the development of more accurate generative AI mod-
   1
       https://github.com/openai/gpt-2-output-dataset                       els.
               Figure 1: Comparison of embedding shifts after two types of modifications for the HC3 dataset.




Figure 2: Topological Time Series for different datasets. The results for the remaining datasets selected in this paper can be
found in Figure 4.


 • M4 (Multilingual, Multimodal, Multitask, Massive               understanding of each dataset. For the perturbation-based
   Dataset) (Wang et al. 2024b) is a large-scale dataset de-      methods we used DetectGPT framework with GPT-2 (Rad-
   signed for training models that can handle multiple lan-       ford et al. 2019) as the base model and T5-Large (Raffel
   guages, tasks, and modalities, making it useful for devel-     et al. 2019) as perturbations generator. However, due to in-
   oping versatile AI systems. Although it is multilingual,       tensive computational costs of DetectGPT, we utilised Fast-
   we sampled only English texts.                                 DetectGPT (Bao et al. 2024) that substitutes DetectGPT’s
 • TweepFake (Fagni et al. 2021) contains real tweets writ-       perturbation step with a more efficient sampling step. For the
   ten by humans and synthetic tweets, generated by various       zero-shot methods we used Binoculars (Hans et al. 2024)
   AI models, from bots, imitating human users.                   with improved perplexity score. These two baselines need
                                                                  no fine-tuning, which is an important aspect for detection
 • Outfox (Koike, Kaneko, and Okazaki 2024) contains
                                                                  task, as it is infeasible to train the detector for every do-
   triplets of essay problem statements, human-written es-
                                                                  main and generator. Lastly, as encoder-based method we
   says, and LLM-generated essays. The students who
                                                                  used mDeBERTa (He et al. 2021), which is the current state-
   wrote the essays range from 6th to 12th grade in the USA.
                                                                  of-the-art model for multilingual machine-generated text de-
                                                                  tection (Macko et al. 2023). By taking these three detectors,
                     4    Approach                                we covered all main categories of detectors.
We decided to evaluate all datasets with common setups to
see how good standard approaches perform on them. We did          4.2   Topological Statistics
not have the goal to obtain the highest score, but rather to      It was shown in (Tulchinskii et al. 2023) that if we take the
compare the performance of the same method on different           inner dimensionality of the manifold on the set of embed-
datasets.                                                         dings, we could separate human-written texts from machine-
                                                                  generated ones. The authors used persistence homology
4.1   Baselines                                                   dimension (PHD) and showed that statistically human-
In Section 2.1 we described three main categories of meth-        generated texts have higher PHD than machine-generated
ods for tackling the detection task. We chose a method from       texts, therefore introducing a novel detector. We calculated
each category, that served as a baseline to obtain first-hand     PHD on each set of texts. Additionally, in (Kushnareva et al.
2024) it was suggested to calculate PHD within sliding win-          Dataset         DeBERTa          Binoculars DetectGPT
dow. These intrinsic dimensions of the text within sliding
window can be used as a feature for detectors. The authors           GPT-2                0.972        0.495           0.412
show that the metric is robust to the change of domain and           HC3                  0.998        0.931           0.972
generators. To be able to compare datasets between each              GhostBuster          0.910        0.683           0.711
other, we came up with a symmetrical score, utilising KL-
                                                                     MGTBench             0.961        0.364           0.447
divergence. Let hd , md be distributions of intrinsic dimen-
sions for two types of texts from the same dataset, of human         MAGE                 0.835        0.632           0.654
and machine origin, then our KLTTS is following:                     M4                   0.987        0.871           0.881
                                                                     OutFox               0.901        0.692           0.707
      KLTTS (hd , md ) = |DKL (hd ||md ) − DKL (md ||hd )|
                                                                     TweepFake            0.941        0.845           0.864
  The lower this score, the closer hd and md are, which
means almost indistinguishable texts and vice versa.                 SemEval24
                                                                                          0.991        0.913           0.924
                                                                     Mono
4.3    Perturbations and Shuffling                                   SemEval24
                                                                                          0.994          –                 –
                                                                     Multi
Based on the results of the text modification studies (Sada-
sivan et al. 2024; Mitchell et al. 2023), which show how             RuATD                0.765          –               –
small perturbations affect machine reading comprehension             DAGPap22             0.968        0.333           0.562
systems, we decided to consider this way of possibly as-             PAN24                0.826        0.411           0.890
sessing the quality of a dataset. The key idea here is that          AuTex23en            0.941        0.783           0.911
AI models are sensitive to such adversarial changes, unlike          AuTex23es            0.933          –               –
humans. We considered two modification ideas: Adversarial
Token Perturbation and Sentence Shuffling.                           IberAuTex            0.964          –               –
   Adversarial Token Perturbation. In this approach we               MGT-1
                                                                                          0.904        0.665           0.683
divide the text into tokens and randomly replace the token           Mono
with a synonym from the WordNet collection (Miller 1994)             MGT-1
                                                                                          0.934          –                 –
with a probability of 70%. We apply such a technique to each         Multi
represented class. Using an encoder model, we obtain em-
beddings for each of the texts in the current dataset. Finally,   Table 2: Classification results with different detectors esti-
we measure the average embedding shifts for the classes of        mated using F1 -score. Binoculars and DetectGPT work only
human and generated texts. We obtain the embedding shifts         with English texts, thus we could not apply them to datasets
using the cosine distance between the embeddings of the           with non-English texts.
original texts and the modified ones. As a result, after modi-
fications we obtain ∆shift — the log difference of the average
embedding shifts.
                                                                                                  X              H(i)
                            Pn                                              KLshuffle (H, M ) =       H(i) log         ,
                          1
                                  cosd (hohi , hphi )                                                            M (i)
           ∆shift = log 1 Pmi=1
                          n
                                         o       p    ,                                           i
                        m    j=1 cosd (hmj , hmj )                                      cosd (hohi , hphi ) + ϵ
   where n and m are number of samples in the human and                        H(i) = P                        .
                                                                                                  o       p
generated parts of the dataset respectively, hohi – embedding                          j cosd (hhj , hhj ) + ϵ
of the i-th fragment of human part of data, hphi – the same       M (i) has the same structure as H(i), except that instead of
embedding after perturbation. Similarly, homi and homi are        human class texts the generated class texts are used, ϵ is a
embeddings for machine-generated texts. Finally, cosd is a        small constant added to avoid division by zero.
function that measures the cosine distance between two vec-
tors.
   Sentence Shuffling. In this approach, we randomly swap                             5     Experiments
sentences, thereby affecting the cohesion of the text. We try     From each dataset, we sampled 1000 documents from the
to find out the effect of artificial origin on the difference     test set, balanced between two classes. Regarding baselines,
between the distributions after permutations. By dividing a       we fine-tuned mdeberta-v3-base for each dataset and
fragment into sentences and randomly reversing the order          evaluated the model. Additional information about hyperpa-
of 70% of the selected sentences, we apply this technique to      rameters during training can be found in the Appendix C.
each represented class. Then, using the text encoding model,      To evaluate the quality of Binoculars and Fast-DetectGPT,
we obtain embeddings for each of the texts from the current       we utilised falcon-rw-1b (Almazrouei et al. 2023) and
dataset. Finally, we measure embedding shifts for the class       gpt-neo-2.7B (Black et al. 2021) respectively. It is
of human and generated texts, and after that we convert the       worth noting that with the last two methods we were only
shifts into probability-like distributions. This allows us to     able to measure quality for samples in English.
obtain at the end KLshuffle (H, M ) — the KL-divergence be-          Our objective was to show that datasets of lower qual-
tween the shifts of human and generated texts.                    ity have shifts that will be easily recognised by the models
                      Dataset               KLTTS ↓      PHDhuman        PHDmachine      ∆shift ↓   KLshuffle ↓
                      GPT-2                  0.014      9.23 ± 1.98     10.27 ± 1.84      0.084        1.255
                      HC3                    0.053      8.76 ± 1.83     7.38 ± 1.05       0.264        1.167
                      GhostBuster            0.053      9.84 ± 1.18     9.76 ± 1.15       0.024        0.359
                      MGTBench               0.043      8.77 ± 1.31     9.97 ± 1.02       0.031        0.421
                      MAGE                   0.011      9.8 ± 2.14      9.38 ± 3.04       0.094        0.310
                      M4                     0.036      7.26 ± 1.99      8.59 ± 1.4       0.107        0.483
                      OutFox                 0.025      8.96 ± 1.21     11.48 ± 1.13      0.095        0.237
                      TweepFake                -        9.02 ± 3.19     8.12 ± 4.02       0.116        1.001
                      SemEval24 Mono         0.012      9.11 ± 1.19      9.41 ± 1.2       0.191        2.576
                      SemEval24 Multi        0.001      9.65 ± 1.81     9.42 ± 1.44       0.059        2.046
                      RuATD                  0.007      7.33 ± 1.4      7.46 ± 1.41       0.315       14.028
                      DAGPap22               0.083      8.35 ± 1.33     7.48 ± 2.01       0.039        0.472
                      PAN24                  0.053      9.4 ± 1.05      8.52 ± 1.59       0.050        0.331
                      AuTex23 Eng            0.021      8.07 ± 2.26      8.1 ± 2.68       0.110        4.331
                      AuTex23 Esp            0.001      9.16 ± 3.49     9.25 ± 3.26       0.105        1.306
                      IberAuTex              0.012      9.33 ± 2.45     8.47 ± 2.73       0.223        5.516
                      MGT-1 Mono             0.019      9.19 ± 1.75     8.96 ± 2.24       0.031        0.587
                      MGT-1 Multi            0.006      8.76 ± 1.85      8.6 ± 2.29       0.027        0.522

Table 3: Calculated statistics on texts from chosen datasets. Some values for KLTTS are underlined, because texts are too short,
see Section 7 and TTS for almost all texts in TweepFake is equal to 0.


”from the first step”, hence we have not performed any hy-            and human texts to adversarial attacks. Qualitatively gener-
perparameter tuning, only one iteration of fine-tuning and            ated data with no bias should take values close to human.
testing of the underlying models. In the experiment with                 Finally, in Table 2 we show the results of applying mod-
topological features we used roberta-base, just as the                ern detectors to the chosen test datasets. For instance, on the
authors of the original paper. In the experiment with per-            datasets with low values in Table 3, a quality close to 1 can
turbations and shuffling, the multilingual-e5-large                   be achieved, indicating the clear presence of detector bias
encoder was used to build embeddings of texts, which shows            towards them, or a structural feature that is too obvious for
high metrics on encoding high-resource languages (Wang                the detection model. It is not possible to judge the quality of
et al. 2024a).                                                        the data only by achieving F1 values close to 1, but by com-
                                                                      bining the values of the two tables, we can estimate which
                        6   Results                                   set has better quality data and which has lower quality data.
The results of the comparison of the designed features in
the selected datasets are presented in Table 3. Regarding                                   7     Discussion
the PHD and TTS score, in previous works it was shown
that texts from language models have smaller PHD values               Regarding KLTTS , on Fig. 2 we show 4 datasets with the
than human-written ones; however, this result was obtained            high value of it. While GhostBuster and PAN24 received
for GPT-2, GPT-3.5 and OPT models, and this trend could               such a high score due to the discrepancy on texts with higher
change for more recent language models that generate more             dimensions, MGTBench and DAGPap22 did it due to the
human-resembling texts. If texts of different origin have             difference in distributions themselves. Note also that KLTTS
high KLTTS , it means that it is easier for a detector to sep-        may not perform well with very short texts, since the internal
arate such texts. KLTTS is also constrained for shorter texts,        method of computing PHD requires sufficiently long texts
see Section 7. As for PHD, we hypothesise that generated              for stable computation. Therefore, we discard KLTTS on Ru-
texts of good quality should have PHD similar to human-               ATD and AuTex23-es and Tweepfake, as they do not fit the
written ones. Additionally, we compare the distributions of           criteria; see Table 1. In addition, it has already been shown
PHD for all datasets on Figure 3. Again, the distributions for        that the texts must be of sufficient length (Gritsay, Grabovoy,
texts of both origin should be similar, which mainly holds for        and Chekhovich 2022) to build reliable detectors.
texts from SemEval, PAN24 and MGT-1.                                     Analysing the values from Table 3, we can trace the pres-
   In the next columns, we list the statistics observed on            ence of sufficiently high quality data in the selected datasets.
modified texts, and for both of these the lower the better, as        The developed attributes in aggregate are able to reflect the
this reflects the similar degree of resilience of the generated       quality of the generated dataset from different perspectives
Figure 3: PHD values on all datasets, except TweepFake and AuTex23 Spanish, texts from which were too short for proper
calculation of PHD.


and angles. We propose to utilise these attributes in combi-        improve model answers and make it more human-like. Sec-
nation with other statistical tools to evaluate data quality, for   ondly, good detectors can help to clean training sets, as large
example, Zipf’s law (Powers 1998).                                  proportion of low-quality generated texts in those sets can
                                                                    result in emerging biases towards incorrect structure and
   Presented statistics can be utilised to estimate the quality
                                                                    rubbish fragments in the output of the model in the future.
of collections and to improve them. In addition, datasets that
collect machine-generated content may also provide utility            The question of whether poor performance by detectors
for the two more general purposes. First, high-quality gener-       implies poor dataset quality yields an ambiguous answer.
ated data can be utilised to evaluate the quality of the causal     For instance, in (Hans et al. 2024), the Binoculars method
model during training, as one of the training objectives to         achieves an F1 -score close to 1.0, while our experiments pro-
duced a wide range of scores: from 0.33 on DAGPap22 to           B.; and Penedo, G. 2023. The Falcon Series of Open Lan-
0.93 on HC3. For HC3, all three detectors performed sim-         guage Models. arXiv:2311.16867.
ilarly, suggesting that the HC3 texts are relatively easy to     Ayele, A. A.; Babakov, N.; Bevendorff, J.; Casals, X. B.;
detect. However, this consistency does not extend to DAG-        Chulvi, B.; Dementieva, D.; Elnagar, A.; Freitag, D.; Fröbe,
Pap22. For instance, the DeBERTa-based detector achieved         M.; Korenčić, D.; Mayerl, M.; Moskovskiy, D.; Mukher-
an F1 -score of 0.96, while DetectGPT scored only 0.562.         jee, A.; Panchenko, A.; Potthast, M.; Rangel, F.; Rizwan,
This pattern, where the DeBERTa-based detector achieves          N.; Rosso, P.; Schneider, F.; Smirnova, A.; Stamatatos, E.;
notably higher scores than the other two methods, was ob-        Stakovskii, E.; Stein, B.; Taulé, M.; Ustalov, D.; Wang,
served across a significant portion of the analysed datasets.    X.; Wiegmann, M.; Yimam, S. M.; and Zangerle, E. 2024.
We attribute this strong performance to the fine-tuning of the   Overview of PAN 2024: Multi-Author Writing Style Anal-
DeBERTa-based detector.                                          ysis, Multilingual Text Detoxification, Oppositional Think-
   Conversely, the low scores for Binoculars merit further       ing Analysis, and Generative AI Authorship Verification. In
scrutiny. Even when focusing on domains specifically tested      Goeuriot, L.; Mulhem, P.; Quénot, G.; Schwab, D.; Nunzio,
by its authors, such as PAN24 (News) and Outfox (Student         G. M. D.; Soulier, L.; Galuscakova, P.; Herrera, A. G. S.;
Essays), the scores fall well below the near-perfect results     Faggioli, G.; and Ferro, N., eds., Experimental IR Meets
reported in (Hans et al. 2024). This discrepancy suggests that   Multilinguality, Multimodality, and Interaction. 15th Inter-
the Binoculars detector may not be representative. Similarly,    national Conference of the CLEF Association (CLEF 2024),
in our experiments, DetectGPT’s scores are comparable to         Lecture Notes in Computer Science. Berlin Heidelberg New
Binoculars’ scores, potentially indicating similar underlying    York: Springer.
issues with the robustness of these detectors.                   Bao, G.; Zhao, Y.; Teng, Z.; Yang, L.; and Zhang, Y.
                                                                 2024. Fast-DetectGPT: Efficient Zero-Shot Detection of
                     8    Conclusion                             Machine-Generated Text via Conditional Probability Curva-
In the current research, we discussed the problem of quality     ture. arXiv:2310.05130.
of datasets with AI-generated texts used for testing corre-      Black, S.; Gao, L.; Wang, P.; Leahy, C.; and Biderman,
sponding detectors. This problem is relevant, as the quality     S. 2021. GPT-Neo: Large Scale Autoregressive Language
of test data directly influences the quality of widely used      Modeling with Mesh-Tensorflow. If you use this software,
detectors. We conducted a review of datasets from compe-         please cite it using these metadata.
titions and scientific publications on datasets aimed at the
detection of AI-generated content and proposed methods           Boeva, G.; Gritsai, G.; and Grabovoy, A. V. 2024. Team ap-
to evaluate the quality of datasets containing AI excerpts       team at PAN: LLM Adapters for Various Datasets. In Work-
based on different structural features. We evaluated topolog-    ing Notes of the Conference and Labs of the Evaluation Fo-
ical features, robustness to adversarial attacks, and perfor-    rum (CLEF 2024), Grenoble, France, 9-12 September, 2024,
mance of the widely used detectors on these datasets. We         volume 3740 of CEUR Workshop Proceedings, 2527–2535.
concluded that all analysed datasets fail in one or another of   Chang, Y.; Wang, X.; Wang, J.; Wu, Y.; Yang, L.; Zhu, K.;
our methods and do not allow to reliably estimate AI detec-      Chen, H.; Yi, X.; Wang, C.; Wang, Y.; Ye, W.; Zhang, Y.;
tors. We encourage researchers to propose their own ways         Chang, Y.; Yu, P. S.; Yang, Q.; and Xie, X. 2024. A Sur-
for quality assessment, which will allow to create a compre-     vey on Evaluation of Large Language Models. ACM Trans.
hensive system of evaluation of the detection datasets. Our      Intell. Syst. Technol., 15(3).
work aims to contribute to a better understanding of the dif-    Fagni, T.; Falchi, F.; Gambini, M.; Martella, A.; and Tesconi,
ference between human and machine text, which will ulti-         M. 2021. TweepFake: About detecting deepfake tweets.
mately contribute to preserving the integrity of information     PLOS ONE, 16(5): e0251415.
in the world.                                                    Fröhling, L.; and Zubiaga, A. 2021. Feature-based detection
                                                                 of automated language models: tackling GPT-2, GPT-3 and
                    9     Limitations                            Grover. PeerJ Computer Science, 7.
In our work we focused on the task of binary classification,     Gray, A. 2024. ChatGPT” contamination”: estimating the
thus suggested methods are not optimal for the task of de-       prevalence of LLMs in the scholarly literature. arXiv
tection of the hybrid AI-human content. Also, some meth-         preprint arXiv:2403.16887.
ods do not work properly on short texts, however, this is a      Gritsai, G.; Khabutdinov, I.; and Grabovoy, A. 2024. Multi-
known issue for short texts.                                     head Span-based Detector for AI-generated Fragments in
                                                                 Scientific Papers. In Ghosal, T.; Singh, A.; Waard, A.; Mayr,
                         References                              P.; Naik, A.; Weller, O.; Lee, Y.; Shen, S.; and Qin, Y., eds.,
Alemohammad, S.; Casco-Rodriguez, J.; Luzi, L.; Hu-              Proceedings of the Fourth Workshop on Scholarly Document
mayun, A. I.; Babaei, H.; LeJeune, D.; Siahkoohi, A.; and        Processing (SDP 2024), 220–225. Bangkok, Thailand: As-
Baraniuk, R. G. 2023. Self-Consuming Generative Models           sociation for Computational Linguistics.
Go MAD. arXiv:2307.01850.                                        Gritsay, G.; Grabovoy, A.; and Chekhovich, Y. 2022. Au-
Almazrouei, E.; Alobeidli, H.; Alshamsi, A.; Cappelli, A.;       tomatic Detection of Machine Generated Texts: Need More
Cojocaru, R.; Debbah, M.; Étienne Goffinet; Hesslow, D.;        Tokens. In 2022 Ivannikov Memorial Workshop (IVMEM),
Launay, J.; Malartic, Q.; Mazzotta, D.; Noune, B.; Pannier,      20–26.
Gritsay, G.; Grabovoy, A.; Kildyakov, A.; and Chekhovich,        Ma, Y.; Liu, J.; Yi, F.; Cheng, Q.; Huang, Y.; Lu, W.; and
Y. 2023a. Artificially generated text fragments search in aca-   Liu, X. 2023. AI vs. Human – Differentiation Analysis of
demic documents. In Doklady Mathematics, volume 108,             Scientific Content Generation. arXiv:2301.10416.
S434–S442. Springer.                                             Macko, D.; Moro, R.; Uchendu, A.; Lucas, J.; Yamashita,
Gritsay, G.; Grabovoy, A.; Kildyakov, A.; and Chekhovich,        M.; Pikuliak, M.; Srba, I.; Le, T.; Lee, D.; Simko, J.; and
Y. 2023b. Automated Text Identification: Multilingual            Bielikova, M. 2023. MULTITuDE: Large-Scale Multilin-
Transformer-based Models Approach. In IberLEF@SEPLN.             gual Machine-Generated Text Detection Benchmark. In
Hans, A.; Schwarzschild, A.; Cherepanova, V.; Kazemi, H.;        Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of
Saha, A.; Goldblum, M.; Geiping, J.; and Goldstein, T. 2024.     the 2023 Conference on Empirical Methods in Natural Lan-
Spotting LLMs With Binoculars: Zero-Shot Detection of            guage Processing, 9960–9987. Singapore: Association for
Machine-Generated Text. arXiv:2401.12070.                        Computational Linguistics.
He, P.; Liu, X.; Gao, J.; and Chen, W. 2021. DeBERTa:            Miller, G. A. 1994. WordNet: A Lexical Database for En-
Decoding-enhanced BERT with Disentangled Attention.              glish. In Human Language Technology: Proceedings of
arXiv:2006.03654.                                                a Workshop held at Plainsboro, New Jersey, March 8-11,
                                                                 1994.
He, X.; Shen, X.; Chen, Z.; Backes, M.; and Zhang, Y. 2023.
MGTBench: Benchmarking Machine-Generated Text De-                Miralles, P.; Martı́n, A.; and Camacho, D. 2024. Team aida
tection. CoRR abs/2303.14822.                                    at PAN: Ensembling Normalized Log Probabilities. In Fag-
                                                                 gioli, G.; Ferro, N.; Galuscáková, P.; and de Herrera, A.
Jawahar, G.; Abdul-Mageed, M.; and Lakshmanan, L., V.S.          G. S., eds., Working Notes of the Conference and Labs of
2020. Automatic Detection of Machine Generated Text: A           the Evaluation Forum (CLEF 2024), Grenoble, France, 9-
Critical Survey. In Scott, D.; Bel, N.; and Zong, C., eds.,      12 September, 2024, volume 3740 of CEUR Workshop Pro-
Proceedings of the 28th International Conference on Com-         ceedings, 2807–2813. CEUR-WS.org.
putational Linguistics, 2296–2309. Barcelona, Spain (On-
line): International Committee on Computational Linguis-         Mitchell, E.; Lee, Y.; Khazatsky, A.; Manning, C. D.; and
tics.                                                            Finn, C. 2023. DetectGPT: zero-shot machine-generated
                                                                 text detection using probability curvature. In Proceedings
Kashnitsky, Y.; Herrmannova, D.; de Waard, A.; Tsatsaro-         of the 40th International Conference on Machine Learning,
nis, G.; Fennell, C. C.; and Labbe, C. 2022. Overview of the     ICML’23.
DAGPap22 Shared Task on Detecting Automatically Gener-
ated Scientific Papers. In Cohan, A.; Feigenblat, G.; Freitag,   Powers, D. M. W. 1998. Applications and explanations of
D.; Ghosal, T.; Herrmannova, D.; Knoth, P.; Lo, K.; Mayr,        Zipf’s law. In Proceedings of the Joint Conferences on New
P.; Shmueli-Scheuer, M.; de Waard, A.; and Wang, L. L.,          Methods in Language Processing and Computational Nat-
eds., Proceedings of the Third Workshop on Scholarly Doc-        ural Language Learning, NeMLaP3/CoNLL ’98, 151–160.
ument Processing, 210–213. Gyeongju, Republic of Korea:          USA: Association for Computational Linguistics. ISBN
Association for Computational Linguistics.                       0725806346.
Koike, R.; Kaneko, M.; and Okazaki, N. 2024. OUT-                Radford, A.; Wu, J.; Child, R.; Luan, D.; Amodei, D.; and
FOX: LLM-Generated Essay Detection Through In-Context            Sutskever, I. 2019. Language Models are Unsupervised
Learning with Adversarially Generated Examples. In Pro-          Multitask Learners.
ceedings of the 38th AAAI Conference on Artificial Intelli-      Raffel, C.; Shazeer, N. M.; Roberts, A.; Lee, K.; Narang, S.;
gence. Vancouver, Canada.                                        Matena, M.; Zhou, Y.; Li, W.; and Liu, P. J. 2019. Exploring
Kushnareva, L.; Gaintseva, T.; Abulkhanov, D.; Kuznetsov,        the Limits of Transfer Learning with a Unified Text-to-Text
K.; Magai, G.; Tulchinskii, E.; Barannikov, S.; Nikolenko,       Transformer. J. Mach. Learn. Res., 21: 140:1–140:67.
S.; and Piontkovskaya, I. 2024. Boundary detection in mixed      Rosati, D. 2022. SynSciPass: detecting appropriate uses of
AI-human texts. In First Conference on Language Model-           scientific text generation. In Cohan, A.; Feigenblat, G.; Fre-
ing.                                                             itag, D.; Ghosal, T.; Herrmannova, D.; Knoth, P.; Lo, K.;
Li, Y.; Li, Q.; Cui, L.; Bi, W.; Wang, Z.; Wang, L.; Yang,       Mayr, P.; Shmueli-Scheuer, M.; de Waard, A.; and Wang,
L.; Shi, S.; and Zhang, Y. 2024. MAGE: Machine-generated         L. L., eds., Proceedings of the Third Workshop on Scholarly
Text Detection in the Wild. arXiv:2305.13242.                    Document Processing, 214–222. Gyeongju, Republic of Ko-
                                                                 rea: Association for Computational Linguistics.
Liang, W.; Zhang, Y.; Wu, Z.; Lepp, H.; Ji, W.; Zhao, X.;
Cao, H.; Liu, S.; He, S.; Huang, Z.; Yang, D.; Potts, C.; Man-   Sadasivan, V. S.; Kumar, A.; Balasubramanian, S.; Wang,
ning, C. D.; and Zou, J. Y. 2024. Mapping the Increasing         W.; and Feizi, S. 2024. Can AI-Generated Text be Reliably
Use of LLMs in Scientific Papers. In First Conference on         Detected?
Language Modeling.                                               Sarvazyan, A. M.; Ángel González, J.; Franco-Salvador,
Lin, C.-Y. 2004. ROUGE: A Package for Automatic Evalu-           M.; Rangel, F.; Chulvi, B.; and Rosso, P. 2023. Overview
ation of Summaries. In Text Summarization Branches Out,          of AuTexTification at IberLEF 2023: Detection and Attri-
74–81. Barcelona, Spain: Association for Computational           bution of Machine-Generated Text in Multiple Domains.
Linguistics.                                                     arXiv:2309.11285.
Sarvazyan, A. M.; Ángel González, J.; Rangel, F.; Rosso,      tics (Volume 1: Long Papers), 3964–3992. Bangkok, Thai-
P.; and Franco-Salvador, M. 2024. Overview of IberAuTex-        land: Association for Computational Linguistics.
Tification at IberLEF 2024: Detection and Attribution of        Wang, Y.; Mansurov, J.; Ivanov, P.; Su, J.; Shelmanov, A.;
Machine-Generated Text on Languages of the Iberian Penin-       Tsvigun, A.; Whitehouse, C.; Afzal, O. M.; Mahmoud, T.;
sula. Procesamiento del Lenguaje Natural, 73(0): 421–434.       Puccetti, G.; Arnold, T.; Aji, A. F.; Habash, N.; Gurevych,
Shamardina, T.; Mikhailov, V.; Cherniavskii, D.; Fenogen-       I.; and Nakov, P. 2024c. SemEval-2024 Task 8: Multigen-
ova, A.; Saidov, M.; Valeeva, A.; Shavrina, T.; Smurov, I.;     erator, Multidomain, and Multilingual Black-Box Machine-
Tutubalina, E.; and Artemova, E. 2022. Findings of the The      Generated Text Detection. In Proceedings of the 18th Inter-
RuATD Shared Task 2022 on Artificial Text Detection in          national Workshop on Semantic Evaluation, SemEval 2024.
Russian. CoRR, abs/2206.01583.                                  Mexico, Mexico.
Su, Z.; Wu, X.; Zhou, W.; Ma, G.; and Hu, S. 2024. HC3          Wang, Y.; Shelmanov, A.; Mansurov, J.; Tsvigun, A.;
Plus: A Semantic-Invariant Human ChatGPT Comparison             Mikhailov, V.; Xing, R.; Xie, Z.; Geng, J.; Puccetti, G.;
Corpus. arXiv:2309.02731.                                       Artemova, E.; Su, J.; Ta, M. N.; Abassy, M.; Elozeiri, K.;
Tulchinskii, E.; Kuznetsov, K.; Kushnareva, L.; Cherni-         Ahmed, S. E. D.; Goloburda, M.; Mahmoud, T.; Tomar,
avskii, D.; Nikolenko, S.; Burnaev, E.; Barannikov, S.; and     R. V.; Aziz, A.; Laiyk, N.; Afzal, O. M.; Koike, R.; Kaneko,
Piontkovskaya, I. 2023. Intrinsic dimension estimation for      M.; Aji, A. F.; Habash, N.; Gurevych, I.; and Nakov, P. 2025.
robust detection of AI-generated texts. In Proceedings of the   GenAI Content Detection Task 1: English and Multilingual
37th International Conference on Neural Information Pro-        Machine-generated Text Detection: AI vs. Human. In Pro-
cessing Systems, NIPS ’23. Red Hook, NY, USA: Curran            ceedings of the 31st International Conference on Computa-
Associates Inc.                                                 tional Linguistics (COLING). Abu Dhabi, UAE: Association
Uchendu, A.; Ma, Z.; Le, T.; Zhang, R.; and Lee, D. 2021.       for Computational Linguistics.
TURINGBENCH: A Benchmark Environment for Turing                 Wu, J.; Yang, S.; Zhan, R.; Yuan, Y.; Wong, D. F.; and
Test in the Age of Neural Text Generation. In Moens, M.-        Chao, L. S. 2023. A Survey on LLM-gernerated Text De-
F.; Huang, X.; Specia, L.; and Yih, S. W.-t., eds., Findings    tection: Necessity, Methods, and Future Directions. CoRR,
of the Association for Computational Linguistics: EMNLP         abs/2310.14724.
2021, 2001–2016. Punta Cana, Dominican Republic: Asso-
ciation for Computational Linguistics.                          Xu, W.; Wang, D.; Pan, L.; Song, Z.; Freitag, M.; Wang,
                                                                W. Y.; and Li, L. 2023. INSTRUCTSCORE: Explain-
Valdez-Valenzuela, A.; Zavala-Reyes, R. L.; Murillo, V.         able Text Generation Evaluation with Finegrained Feedback.
G. M.; and Gómez-Adorno, H. 2024. The iimasNLP team            arXiv:2305.14282.
at IberAuTexTification 2024: Integrating Graph Neural Net-
works, Multilingual LLMs, and Stylometry for Automatic          Zellers, R.; Holtzman, A.; Rashkin, H.; Bisk, Y.; Farhadi, A.;
Text Identification. In IberLEF@SEPLN.                          Roesner, F.; and Choi, Y. 2019. Defending Against Neural
                                                                Fake News. In Advances in Neural Information Processing
Verma, V.; Fleisig, E.; Tomlin, N.; and Klein, D. 2024.
                                                                Systems 32.
Ghostbuster: Detecting Text Ghostwritten by Large Lan-
guage Models. arXiv:2305.15047.                                 Zhao, Y.; Gao, J.; Wang, J.; Luo, G.; and Tang, L. 2024. Uti-
Villalobos, P.; Sevilla, J.; Heim, L.; Besiroglu, T.; Hobb-     lizing an Ensemble Model with Anomalous Label Smooth-
hahn, M.; and Ho, A. 2022. Will we run out of data? an          ing to Detect Generated Scientific Papers. Proceedings of
analysis of the limits of scaling datasets in machine learn-    the Fourth Workshop on Scholarly Document Processing
ing. arXiv preprint arXiv:2211.04325.                           (SDP 2024).
Voznyuk, A.; and Konovalov, V. 2024. DeepPavlov at              Zhou, J.; Zhang, Y.; Luo, Q.; Parker, A. G.; and De Choud-
SemEval-2024 Task 8: Leveraging Transfer Learning for           hury, M. 2023. Synthetic Lies: Understanding AI-Generated
Detecting Boundaries of Machine-Generated Texts. In Ojha,       Misinformation and Evaluating Algorithmic and Human So-
A. K.; Doğruöz, A. S.; Tayyar Madabushi, H.; Da San Mar-      lutions. In Proceedings of the 2023 CHI Conference on Hu-
tino, G.; Rosenthal, S.; and Rosá, A., eds., Proceedings of    man Factors in Computing Systems, CHI ’23. New York,
the 18th International Workshop on Semantic Evaluation          NY, USA: Association for Computing Machinery. ISBN
(SemEval-2024), 1821–1829. Mexico City, Mexico: Asso-           9781450394215.
ciation for Computational Linguistics.                          Zhu, W.; and Bhat, S. 2020. GRUEN for Evaluating Lin-
Wang, L.; Yang, N.; Huang, X.; Yang, L.; Majumder, R.;          guistic Quality of Generated Text. In Cohn, T.; He, Y.; and
and Wei, F. 2024a. Multilingual E5 Text Embeddings: A           Liu, Y., eds., Findings of the Association for Computational
Technical Report. arXiv:2402.05672.                             Linguistics: EMNLP 2020, 94–108. Online: Association for
Wang, Y.; Mansurov, J.; Ivanov, P.; Su, J.; Shelmanov, A.;      Computational Linguistics.
Tsvigun, A.; Mohammed Afzal, O.; Mahmoud, T.; Puccetti,
G.; Arnold, T.; Aji, A.; Habash, N.; Gurevych, I.; and Nakov,
P. 2024b. M4GT-Bench: Evaluation Benchmark for Black-
                                                                                 A    Data Description
Box Machine-Generated Text Detection. In Ku, L.-W.; Mar-        More detailed description with information on sources, top-
tins, A.; and Srikumar, V., eds., Proceedings of the 62nd An-   ics and years of the datasets selected in this paper from com-
nual Meeting of the Association for Computational Linguis-      petitions and research papers in Table 4
     B    Evaluation results of competitions
Table 5 shows the winning scores in the competitions re-
viewed in this paper. In the AuTex and IberAuTex compe-
titions it was forbidden to use additional data to fine-tune
the detection algorithms. In the other collections it was al-
lowed, we can notice a high quality near perfect in them.
We should note the low value of the metrics on the RuATD
dataset, which can be explained by the limited number of
high-quality language models available in Russian during
the competition.

     Competition            Metric          Best result
     RuATD                Accuracy             0.820
     AuTex23-en           Macro-F1             0.809
     AuTex23-es           Macro-F1             0.708
     IberAuTex            Macro-F1             0.805
     SemEval24
                           Accuracy            0.975
     Mono
     SemEval24
                           Accuracy            0.959
     Multi
     PAN24            Avg. of 5 metrics*       0.924
     DAGPap22          Avg. F1-score           0.994
     MGT-1 Mono          Macro-F1              0.8307
     MGT-1 Multi         Macro-F1              0.7916

Table 5: Best results from each analysed competition.
PAN24 used mean of 5 metrics, such as accuracy, F1 and
other to evaluate efficiency of the system.


                C    Hyperparameters

               Hyperparameters        Values
               Epochs                   5*
               Learning rate (LR)      5e-5
               Warm-up steps            50
               Weight decay            0.01

Table 6: Hyperparameters for fine-tuning mDeBERTa-base.
We trained for 5 epochs with possibility of early exit.

The training was carried out on NVIDIA GeForce RTX
3090. See hyperparameters in Table 6.
      Dataset        Year       Themes                                        Sources
                                                  Research papers datasets
      GPT2           2019       WebText                                       GPT-2
      TweepFake      2019       Tweets                                        Markov Chains, RNN, LSTM, GPT-2
      HC3            2023       ELI5, WikiQA, Wikipedia, Medicine, Fi-        ChatGPT
                                nance
      GhostBuster    2023       Student Essays, News Articles, Creative       ChatGPT, Claude
                                Writing
      MGTBench       2024       Student Essays, News Articles, Creative       ChatGPT. ChatGLM, Dolly, GPT4All, Sta-
                                Writing                                       bleLM, Claude
      MAGE           2024       Opinions, Reviews, News, QA, Story Gen-       text-davinci-002, GPT-3.5, ChatGPT,
                                eration, Commonsense Reasoning, Knowl-        LLaMA, GLM-130B, FLAN-T5, OPT,
                                edge Illustration, Scientific Writing         BLOOM, GPT-J-6B, GPT-NeoX-20B
      M4             2024       Wikipedia, Reddit ELI5, WikiHow, Peer-        GPT-3.5, ChatGPT, Cohere, Dolly-v2,
                                Read, arXiv abstract                          BLOOM
      OutFox         2024       Student Essays                                ChatGPT, GPT-3.5, FLAN-T5
                                                    Shared tasks datasets
      RuATD          2022       News, Social media, Wikipedia, Strategic      M-BART, M2M-100, OPUS-MT, mT5,
                                Documents, Diaries                            ruGPT2, ruGPT3, ruT5-Base
      DAGPap         2022       Scopus papers                                 Longformer Encoder-Decoder, GPT-3,
                                                                              Spinbot, GPT-Neo
      AuTex          2023       Legal documents, Social media, How-to         BLOOM, GPT-3, GPT-3.5
                                articles
      IberAuTex      2024       News, Reviews, Emails, Essays, Dia-           GPT-2, LLaMA, Mistral, Cohere, Claude,
                                logues, Wikipedia, Wikihow, Tweets            MPT, Falcon
      PAN            2024       News                                          Alpaca, BLOOM, Gemini, ChatGPT, gpt-
                                                                              4-turbo, LLaMA-2, Mistral, Qwen1.5,
                                                                              GPT-2
      SemEval        2024       Wikipedia, WikiHow, Reddit, arXiv, Peer-      GPT-3.5, GPT-4, Cohere, Dolly-v2,
      Mono                      Read, Student Essays                          BLOOMz
      SemEval        2024       Wikipedia, WikiHow, Reddit, arXiv, Peer-      ChatGPT, GPT-3.5, GPT-4, LLaMA2, Co-
      Multi                     Read, Student Essays, News                    here, Dolly-v2, BLOOM, Jais
      MGT-1          2025       CNN, DialogSum, Wikipedia, WikiHow,           text-davinci-002, GPT-3.5, ChatGPT, OPT,
      Mono                      Eli5, Finance, XSum, PubMed, SQuAD,           LLaMA3, BLOOM, FLAN-T5, Cohere,
                                IMDb, Reddit, arXiv, PeerRead                 Dolly, Gemma, Mixtral
      MGT-1          2025       CNN, DialogSum, Baike, WikiQA, Wik-           text-davinci-002, GPT-3.5, ChatGPT,
      Multi                     iHow, Eli5, Finance, Psychology, XSum,        gpt4o, GLM, GPT-J, GPT-Neo, OPT,
                                PubMed, SQuAD, IMDb, Reddit, arXiv,           LLaMA2, LLaMA3, BLOOM, FLAN-T5,
                                PeerRead                                      Cohere, Dolly, Gemma, Mixtral, Jais

Table 4: More detailed descriptive statistics about domains and generators of the chosen datasets from competitions and research
papers. ChatGPT is gpt-3.5-turbo, GPT-3.5 is text-davinci-003.
Figure 4: Topological Time Series on all datasets.
