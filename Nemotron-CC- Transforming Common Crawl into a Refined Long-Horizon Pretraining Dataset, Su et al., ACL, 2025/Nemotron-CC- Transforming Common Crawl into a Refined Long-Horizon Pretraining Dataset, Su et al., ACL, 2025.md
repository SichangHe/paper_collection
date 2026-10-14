   Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon
                           Pretraining Dataset

                  Dan Su* , Kezhi Kong* , Ying Lin* , Joseph Jennings, Brandon Norick,
                Markus Kliegl† , Mostofa Patwary, Mohammad Shoeybi, Bryan Catanzaro

                                                                NVIDIA
                                    *
                                        Equal contribution. † Correspondence to mkliegl@nvidia.com.



                             Abstract                                                             60
                                                                                                            59.0
                                                                                                                             53.4     53.0
           Recent English Common Crawl datasets like
           FineWeb-Edu and DCLM achieved significant                                                                                                  42.9   42.4
           benchmark gains via aggressive model-based




                                                                                                                                       4x more data
                                                                                                  40




                                                                                                             +5.6 MMLU
           filtering, but at the cost of removing 90% of
           data. This limits their suitability for long token



                                                                               MMLU Accuracy
           horizon training, such as 15T tokens for Llama
           3.1. In this paper, we show how to achieve                                             20
           better trade-offs between accuracy and data
           quantity by a combination of classifier ensem-
           bling, synthetic data rephrasing, and reduced
           reliance on heuristic filters. When training                                            0
           8B parameter models for 1T tokens, using

                                                                                                                         LM




                                                                                                                                                    u

                                                                                                                                                  -2
                                                                                                            Q




                                                                                                                                                   C

                                                                                                                                                 Ed
                                                                                                                                                 C
                                                                                                        -H




                                                                                                                                               du
                                                                                                                         C

                                                                                                                                              n-


                                                                                                                                              b-
           a high-quality subset of our data improves
                                                                                                        C


                                                                                                                         D




                                                                                                                                             -E
                                                                                                                                ro
                                                                                                    C




                                                                                                                                            e

                                                                                                                                          eb
                                                                                                                                         eW
                                                                                                                              ot
                                                                                                   n-




                                                                                                                                         W
                                                                                                                             em
                                                                                                   ro




           MMLU by 5.6 over DCLM, demonstrating

                                                                                                                                        n

                                                                                                                                      ne
                                                                                                 ot




                                                                                                                                     Fi
                                                                                                                         N
                                                                                               em




                                                                                                                                    Fi
           the efficacy of our methods for boosting
                                                                                          N




           accuracies over a relatively short token horizon.
           Furthermore, our full 6.3T token dataset                    Figure 1: MMLU scores for 8B parameter models
           matches DCLM on MMLU, but contains                          trained for 1T tokens. Compared to DCLM, our meth-
           four times more unique real tokens than                     ods enable us to either create a 4× larger dataset of
           DCLM. This unlocks state-of-the-art training                similar quality or increase the MMLU using a high qual-
           over a long token horizon: an 8B parameter                  ity subset of the tokens. Having a larger dataset, in the
           model trained for 15T tokens, of which 7.2T                 sense of unique real tokens, is crucial when training
           came from our dataset, is better than the                   over long horizons such as 15T tokens.
           Llama 3.1 8B model: +5 on MMLU, +3.1 on
           ARC-Challenge, and +0.5 on average across
           ten diverse tasks. The dataset is available at
                                                                       trained over 2.6T tokens), primarily thanks to the
           https://data.commoncrawl.org/contrib/
           Nemotron/Nemotron-CC/index.html.
                                                                       use of model-based filters to extract high-quality
                                                                       educational and instructional content. However,
   1       Introduction                                                this comes at the cost of data quantity: they remove
                                                                       around 90% of the data. Such aggressive pruning
   Internet crawl is the largest source of unique to-                  may not be the most effective strategy when train-
   kens for training LLMs and can be seen as serving                   ing larger models over longer token horizons (e.g.,
   two main purposes: high-quality content and diver-                  Llama 3.1 includes 8B–405B parameter models,
   sity. Recent English datasets derived from Com-                     trained for 15T tokens (Dubey et al., 2024) and
   mon Crawl1 such as FineWeb-Edu (Penedo et al.,                      Gemma 2 27B was trained for 13T tokens (Team
   2024) and DCLM (Li et al., 2024) have empha-                        et al., 2024)). Both DCLM and FineWeb-Edu
   sized high-quality content that boosts benchmark                    contain around 80% near-duplicates (1T and 0.2T
   accuracies over data quantity. They have demon-                     unique tokens, respectively) (Ben Allal, 2024; Li
   strated significant strides in achieving benchmark                  et al., 2024) and to train on these datasets for many
   results competitive with some of the best closed                    trillions of tokens implies seeing essentially the
   models at a small scale (e.g., DCLM’s 7B model                      same samples many times during training. This
       1
           https://commoncrawl.org/                                    could lead to inferior models, as Muennighoff et al.
                                                                  2459
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 2459–2475
                            July 27 - August 1, 2025 ©2025 Association for Computational Linguistics
(2024) find there are diminishing returns after four              diverse set of high quality tokens.
epochs compared to training on more unique to-                (b) Rephrasing can effectively reduce noise
kens.                                                             and errors in low-quality data and pro-
   In this paper, we show how to achieve a better                 duce diverse variants with fresh unique
trade-off between benchmark accuracy and data                     tokens from high-quality data, leading to
quantity with a combination of classifier ensem-                  better results in downstream tasks.
bling, synthetic data generation, and reduced re-
                                                              (c) Disabling traditional non-learned heuris-
liance on heuristic filters. Our main contributions
                                                                  tic filters for high-quality data can further
are:
                                                                  boost high quality token yield without
  1. We propose a method for transforming En-                     hurting accuracy.
     glish Common Crawl into a 6.3T token long-
     horizon pretraining dataset, consisting of 4.4T      Finally, we remark that our overall guiding prin-
     globally deduplicated original tokens and 1.9T    ciple is to shift from a static, non-learned, heuristic
     synthetically generated tokens. We release the    pipeline towards a more learned flywheel whose
     dataset2 under the Common Crawl Terms of          performance will naturally get better over time. As
     Use and a reference implementation as part        our data improves, so will the LLMs we train, and
     of the Apache 2.0 open-source NeMo Curator        these improved LLMs will in turn improve our data
     library.3 The quality classifier models have      as we use them to generate better synthetic data
     been released as well.4                           and quality classifications.

  2. We prove the effectiveness of this method
                                                       2     Methods
     by comparing to the state-of-the-art open En-
     glish Common Crawl datasets DCLM and              In this section we explain our efforts to build the
     FineWeb-Edu (Figure 1).                           best English Common Crawl pretraining dataset
       (a) A 1.1T-token high-quality subset of our     for LLMs. Our efforts can be split into three folds.
           data achieves a 5.6 MMLU improvement        First, we talk about our efforts in boosting token
           over DCLM, showing the superiority of       yield by utilizing text extractor and heuristic filters
           our method over a relatively short token    more properly in Section 2.1. Second, we introduce
           horizon.                                    the model-based quality labeling pipeline methods
       (b) Our full dataset performs on par with       in Section 2.2. Third, we introduce our synthetic
           DCLM while having 4× as many unique         data generation method to further improve the data
           real tokens.                                quality in Section 2.3. For a schematic overview
                                                       of our final pipeline, please see Figure 3 in Ap-
       (c) This larger size enables state-of-the-art
                                                       pendix A.
           results over long token horizons: An
           8B parameter model trained for 15T to-
                                                       2.1    HTML-to-text Extractor & Filter
           kens using a weighted version of our
           dataset achieves higher overall accuracy    Extracted texts from HTMLs are the foundation
           than Llama 3.1 8B, and in particular        and major source of LLM pretraining dataset, so it
           MMLU 70.3 vs. Llama’s 65.3. Note            is of great significance to analyze and understand
           that Llama 3.1 8B was also trained on       the extraction tools for optimal data quality and
           15T tokens (Dubey et al., 2024).            token yield. Moreover, heuristic filters are often
                                                       utilized to remove low-quality tokens with human-
  3. We conduct ablation studies and find:             designed heuristics (Li et al., 2024; Parmar et al.,
       (a) Ensembling different model-based clas-      2024; Penedo et al., 2024; Dubey et al., 2024),
           sifiers can help select a larger and more   which may also put good tokens at the risk of being
   2                                                   removed. We carefully examine both aspects with
     https://data.commoncrawl.org/contrib/Nemotron/
Nemotron-CC/index.html                                 the assist of the FineWeb-Edu classifier (Penedo
   3
     https://github.com/NVIDIA/NeMo-Curator            et al., 2024), a model-based quality classifier that
   4
     https://huggingface.co/nvidia/nemocurator-        had shown effectiveness in identifying high-quality
fineweb-nemotron-4-edu-classifier      and   https:
//huggingface.co/nvidia/nemocurator-fineweb-           tokens that are significant in boosting the strength
mixtral-edu-classifier                                 of LLMs.
                                                   2460
                       #Tokens   #HQ tokens     #HQ +%       (2021) and a perplexity filter based on a KenLM
Trafilatura-filtered     994          80           -         model (Heafield, 2011) trained on Wikipedia and
Justext-filtered        1,380        104         28.6%       books data (Wenzek et al., 2020). To quantitatively
Justext                 1,804        127         57.4%
                                                             better understand the effectiveness of the filtering
                                                             pipeline, we calculate the token yield and report the
Table 1: Extraction and filteration token count statistics
(billion). Tokens counted after deduplication.               numbers in Table 1. We find the filtering pipeline
                                                             removes a non-trivial portion of high-quality to-
                                                             kens (-18.1%) classified by FineWeb-Edu classifier
HTML-to-text Extraction We test two HTML-                    from the dataset.
to-text extractors, Justext (Pomikálek, 2011) and               Given the impact that the heuristic filters have on
Trafilatura (Barbaresi, 2021). Qualitatively, we             the high-quality token yield, we propose to NOT
view both extractors at the same level of quality.           apply such filters to the high-quality tokens dis-
Quantitatively, we calculate token yields of both            tinguished by model-based quality classifers (de-
extractors on 13 selected snapshots of Common                scribed in the next section), but only use those on
Crawl (see Appendix F). The statistics are reported          the low-quality splits. In the experiment section we
in Table 1. We see that Justext can yield more to-           empirically verify the impact of both the extractor
kens, notably more high-quality tokens (+28.6%)              and filter on pretraining data quality through down-
by the standard of Fineweb-Edu classifier (score 3,          stream benchmarks. We refer readers to Section 3.3
4, and 5). We highlight that boosting unique token           for detailed results.
amount is of great importance when building long-
horizon pretraining dataset, e.g., 15T tokens for            2.2   Model-based Quality Labeling
Llama3.1. Even though there is a slight decline in           Recent work (Li et al., 2024; Penedo et al., 2024)
the percentage of HQ tokens for Justext vs. Justext-         use model-based classifiers to extract high-quality
filtered (7.0% vs. 7.5%), what we aim to maximize            pretraining documents from English Common
here is the absolute number of HQ tokens (127B               Crawl. However, both of the two quality classi-
vs. 104B). We will later sort the data into quality          fiers have a limited recall (around 10%) of high-
buckets, which enables exact control of the propor-          quality tokens (see Table 9), and this will become
tion of HQ vs. non-HQ data seen during training              a bottleneck to train an LLM over a long horizon.
instead of reliance on the natural distribution for          Also, the quality labels assigned by the quality
a particular extraction tool. After extraction, we           classifier are not necessarily aligned with LLM’s
apply filtering to keep only English text, as deter-         downstream task performance. Therefore, we pro-
mined by pycld25 and the FastText lid176 language            pose our ensemble-based quality labeling pipeline
classifier6 with threshold 0.3 (Joulin et al., 2016,         method. Specifically, we first build three quality
2017). We then apply global fuzzy deduplication as           classifiers, each of which has different high-quality
well as exact substring deduplication over eighths           preferences. Then, we ensemble the three clas-
of snapshots (Lee et al., 2022), using the NeMo              sifiers to score all the documents, and split the
Curator library7 and the deduplicate-text-datasets           crawl corpus into different quality buckets based
library,8 respectively.                                      on the quality score. Finally, we regroup the fine-
Filtering Conventionally, heuristic filters are              grained document buckets into 5 different quality
leveraged to remove low-quality tokens from the              levels based on their corresponding performance
pretraining dataset as a post-processing step (Li            on downstream task.
et al., 2024; Parmar et al., 2024; Penedo et al.,            Quality Classifier Training Preparing pretrain-
2024; Dubey et al., 2024). We revisit the filter-            ing documents with quality annotations is the first
ing pipeline as in (Parmar et al., 2024). Such               key step in building a quality classifier (Dubey
pipeline sequentially consists of a set of heuris-           et al., 2024; Abdin et al., 2024; Yang et al., 2024).
tic filters proposed by Raffel et al. (2020); Rae et al.     Similar to the work (Penedo et al., 2024)9 , we
   5
     https://pypi.org/project/pycld2/                        constructed two versions of quality annotation
   6
     https://fasttext.cc/docs/en/language-                   data. We prompt Mistral 8x22B-instruct10 and
identification.html
   7                                                            9
     https://github.com/NVIDIA/NeMo-Curator                       We use the same 460K document samples as in the
   8                                                         FineWeb-Edu-Annotation dataset.
     https://github.com/google-research/
                                                               10
deduplicate-text-datasets                                         https://mistral.ai/news/mixtral-8x22b/

                                                         2461
Nemotron-340B-instruct (Adler et al., 2024), to              Quality Label   Buckets   # Tokens (B)   Token (%)
score web documents from FineWeb based on                    High               19             553        12.63
their educational value on a scale from 0 to 5.              Medium-High        18             504        11.52
                                                             Medium           12-17          2,023        46.24
We then fine-tune a linear regression model on               Medium-Low        7-11            894        20.43
top of the Snowflake-arctic-embed-m embedding                Low                0-6            402         9.18
model (Merrick et al., 2024) using the two different
version of training sets. The two models have been            Table 2: Common Crawl quality labels statistics.
trained for 20 epochs with a learning rate of 3e-
4, with the embedding and encoder layers frozen,
                                                          2.3    Synthetic Data Generation
and we selected the checkpoint with the highest F1
score on the held-out validation set.                     Upon reviewing samples across the quality tiers,
   We also employ the DCLM classifier which is a          we observe that documents with lower scores tend
fastText-based classifier released by Li et al. (2024).   to contain more noise and errors, while those scor-
The DCLM classifier is trained on a combination           ing higher generally exhibit good writing and for-
of instruction-formatted data (Teknium, 2023) and         matting. Therefore, we employ different strategies
high-scoring posts data from ELI5 subreddit (Fan          when generating data from low- and high-quality
et al., 2019), and has shown stronger performance         documents.
in identifying high-quality pretraining tokens, com-         For low-quality data, our goal is to improve the
pared to the FineWeb-Edu classifier (Penedo et al.,       quality by reducing noise and errors while preserv-
2024). The DCLM classifier will offer a new per-          ing useful information, thereby decreasing train-
spective in labeling high-quality pretraining doc-        ing compute expenses. As shown by Maini et al.
uments, and will help increase the recall of high-        (2024), rephrasing web data using a medium-sized
quality tokens.                                           language model yields an enhanced parallel cor-
                                                          pus of synthetic data, thereby reducing model per-
Quality Scoring and Bucketing First, we use
                                                          plexity and boosting its accuracy on downstream
each of the three classifiers to predict the qual-
                                                          tasks. Unlike existing methods that create new
ity scores for all the documents. Then based on
                                                          content such as textbooks and short stories (Wang
the ranked quality score from each classifier, we
                                                          et al., 2023; Eldan and Li, 2023; Gunasekar et al.,
rounded the model’s output score to integers from
                                                          2023), our rephrasing-based approach does not uti-
0 to 19. So that each score bucket will have around
                                                          lize the language model as a knowledge bank but
5% of the documents, and bucket 19 will have the
                                                          focuses on transforming provided texts into another
top 5% highest quality documents. We then assign
                                                          style, allowing it to operate with a lighter-weight
the final quality score for each document by en-
                                                          model. We adopt the Wikipedia style prompt
sembling the three classifiers’ integer score by a
                                                          from (Maini et al., 2024) to rewrite low-quality
maximum operation. The number of documents
                                                          documents (Prompt 5 in Appendix H), which ef-
distribution in each buckets will be skewed by the
                                                          fectively reduces errors and redundancies and im-
ensemble operation.
                                                          proves formatting.
Quality Labeling In order to assign a quality la-            For high-quality data, we aim to obtain more
bel that is more aligned with their real performance      unique tokens and condense essential knowledge.
on downstream tasks, we further group the fine-           According to (Muennighoff et al., 2024), adding
grained quality score predicted by three classifiers      repeated tokens yields a diminishing return, espe-
into 5 downstream quality categories. We used an-         cially after 4 epochs. For high-quality documents,
nealing to assess each data bucket’s downstream           we generate synthetic data using four additional
task’s quality. Specifically, we measure the quality      prompts: (1) Diverse Question-Answer (QA) pairs:
of each bucket by continuous pretraining with 50B         ask questions in various forms (e.g., yes/no ques-
tokens on a 70% trained 8B models. We assign              tion, open-ended question, multi-choice question)
66% of weight to the default data mix and 34%             about factual information in the text and provide
to the dataset that we are evaluating. By compar-         the correct answers; (2) Distill: rewrite the text into
ing the average performance of each bucket over 9         a concise and clear passage; (3) Extract knowledge:
tasks, we group the 20 buckets into 5 big categories,     rewrite knowledge from the text and disregard un-
with the final distribution shown in Table 2. For         informative content; (4) Knowledge list: extract
more details, please see Appendix C.                      key information from the text as an organized list.
                                                      2462
We require the model to provide clear and concise             eration due to time and resource constraints. We
responses while preserving factual information and            employ TensorRT-LLM13 and NeMo-Skills14 to
concrete details such as numbers. The full prompts            enable large-scale data synthesis.
are shown in Appendix H.
   As we increase the length of provided text, the               Source     #Raw    Prompt                  #Synthetic
model shows a tendency to produce over-simplified                Low        403.0   Wikipedia                 336.3
outputs with reduced detail. Therefore, we chunk                                    Wikipedia                 372.9
each document into segments, each of which con-                                     Diverse QA Pairs          499.5
tains one or more complete lines and is shorter than             High       451.3   Distill                   157.6
                                                                                    Extract Knowledge         303.6
a specific token limit.11 Over-length lines exceed-                                 Knowledge List            203.2
ing the token limit are discarded.
                                                              Table 3: Synthetic data token count statistics (billion).
 Question: Which year did the United Nations
 implement the 2030 agenda for SDGs?
 Answer: January 1, 2016
 Question: What are the three key dimensions of
                                                              2.4       Putting It All Together
 sustainable development covered by the SDGs?
 Answer: (a) economic growth, (b) social
 inclusion, and (c) environmental protection                     Dataset                  Total    Unique    Synthetic

 Question: Which of the following can flossing                   FineWebEdu-2                5.4    1.1          -
 prevent? A) Cavities B) Gum disease C) Both A and               FineWebEdu                  1.3    0.2          -
 B D) Neither A nor B                                            DCLM                        3.8    1.0          -
 Answer: C) Both A and B                                         Nemotron-CC                 6.3    4.4         1.9
                                                                 Nemotron-CC-HQ              1.1    0.6         0.5
 Question: Is flossing important even if you
 brush your teeth twice a day?
 Answer: Yes, flossing is important as it reaches             Table 4: Dataset sizes in trillions of tokens. "Unique"
 areas that brushing alone cannot.                            shows the estimated number of tokens after global fuzzy
                                                              deduplication of the real tokens.
Figure 2: Examples of generated question-answer pairs.
                                                                 Combining the techniques above to the 99
   Our post-processing steps include removing in-
                                                              snapshots CC-MAIN-2013-20 through CC-MAIN-
complete results, eliminating specific Markdown
                                                              2024-30 of Common Crawl, we create a 6.3T token
formatting (e.g., double asterisks), stripping away
                                                              dataset (Nemotron-CC), consisting of 4.4T globally
prefixes of certain patterns (e.g., “Here is a para-
                                                              deduplicated tokens and 1.9T synthetically derived
phrased version:” and “Paraphrased Text:”), re-
                                                              tokens. This dataset has roughly 4× more unique
moving quotation marks enclosing the entire re-
                                                              tokens than FineWebEdu-2 and DCLM, since both
sponse, and filtering out under-length outputs (i.e.,
                                                              of those datasets only underwent a sharded form
shorter than 50 tokens). For Wikipedia results, we
                                                              of approximate deduplication and contain roughly
concatenate passages generated from segments be-
                                                              80% fuzzy duplicates (Ben Allal, 2024; Li et al.,
longing to the same original document. For Diverse
                                                              2024). To enable a fairer comparison over relatively
QA Pairs results, we shuffle the generated question
                                                              short token horizons, we thus also consider a 1.1T
and answer pairs, retain up to a number based on
                                                              token high quality subset of our data (Nemotron-
the length of the segment, and append the pairs to
                                                              CC-HQ), consisting of just the highest-scoring real
the end of the segment.
                                                              and diverse QA pairs synthetic data. The size break-
   Using the instruct version of Mistral NeMo
                                                              down of the datasets is shown in Table 4.
12B12 with FP8 inference, a top-p value of 0.9, and
a sampling temperature of 0.5, we synthesize over
                                                              3        Experiments
1.8T tokens as Table 3 shows, including 336.3B
tokens from low-quality documents and 1.5T to-                3.1       Experiment Setup
kens from high-quality documents. We do not use
                                                              Training Setup We use the open source
medium-quality documents for synthetic data gen-
                                                              Megatron-LM library15 (Shoeybi et al., 2019) to
  11
     The token limit is set to 512 for Wikipedia, 2,000 for   train standard 8B parameter transformer LLMs.
Distill, 1,400 for Extract Knowledge and 1,000 for Diverse
                                                                  13
QA Pairs and Knowledge List, including tokens from the               https://github.com/NVIDIA/TensorRT-LLM
                                                                  14
prompt and chat format.                                              https://github.com/NVIDIA/NeMo-Skills
  12                                                              15
     https://mistral.ai/news/mistral-nemo                            https://github.com/NVIDIA/Megatron-LM

                                                          2463
 Dataset                 ARC-E         ARC-C         H       W       RACE     PIQA     SIQA    CSQA    OBQA   MMLU     Avg
 FineWebEdu-2            71.9          44.7          75.4    67.0    36.8     79.5     45.2    25.5    43.8   42.4     53.2
 FineWebEdu              73.6          48.0          70.7    64.6    38.0     76.4     43.5    30.0    44.4   42.9     53.2
 DCLM                    74.7          47.0          76.3    69.1    36.5     79.7     45.6    44.1    44.0   53.4     57.0
 Nemotron-CC             75.3          50.7          75.9    67.8    37.9     80.5     45.1    47.7    44.2   53.0     57.8
 Nemotron-CC-HQ          78.8          52.9          76.6    69.4    36.4     80.1     46.6    55.8    45.4   59.0     60.1

Table 5: Results for 8B parameter models trained on 1T tokens (73% English Common Crawl from the tested
dataset, 27% the same, fixed non-Crawl datasets). The models were evaluated on ARC-Easy, ARC-Challenge,
Hellaswag, Winogrande, RACE, PIQA, Social IQA, Commonsense QA, Openbook QA, and MMLU.

 Model            ARC-E         ARC-C         H          W       RACE       PIQA     SIQA     CSQA    OBQA    MMLU     Avg
 Llama 3.1        82.4          55.0          79.3       74.7    39.1       81.2     48.3     70.6    46.0    65.3     64.2
 Ours             82.7          58.1          80.8       73.8    37.8       81.1     47.4     69.9    45.4    70.3     64.7

Table 6: Comparison of our 8B parameter model vs Llama 3.1 8B. Both were trained for 15T tokens. The numbers
for Llama 3.1 are from our own lm-evaluation-harness setup described in Section 3.1 and may not match Meta’s
publicly reported numbers, as Meta made various customizations to the benchmarks.


The hyperparameter details are shown in Ap-                             shows accuracy gains over DCLM and FineWeb-
pendix D.                                                               Edu on all tasks except RACE. In particular, there
                                                                        is a 5.6 MMLU and 3.1 average gain over DCLM.
Data Blend Unless otherwise noted, we train                             This shows the effectiveness of our classifier en-
for 1T tokens on a blend of 73% English Com-                            sembling and synthetic data even in the non-data-
mon Crawl data and 27% a fixed mix of special-                          constrained setting. Our complete 6.3T token
ized code, papers, books, patents, and Wikipedia                        dataset (Nemotron-CC) gives MMLU and average
datasets (Adler et al., 2024). When comparing                           accuracies roughly on par with DCLM. But since
datasets, we vary only the 73% English Common                           this dataset contains 4× more unique real tokens,
Crawl portion. See Table 12 in Appendix D.                              we expect it to be superior in data-constrained set-
                                                                        tings like 15T token training runs.
Evaluation Setup We use the open source LM
Evaluation Harness library16 (Gao et al., 2023)                         Long Token Horizon (15T) Our dataset con-
to evaluate on the following ten common sense                           tributed 7.2T of the tokens used to train an 8B
and reasoning tasks (reported metric in parenthe-                       model for 15T tokens. As shown in Table 6, our
ses): ARC-Easy and ARC-Challenge (normalized                            model achieves a higher average accuracy than
accuracy) (Clark et al., 2018), Hellaswag (nor-                         Llama 3.1 8B, which was also trained for 15T
malized accuracy) (Zellers et al., 2019), Wino-                         tokens, including an MMLU score of 70.3 vs.
grande (accuracy) (Sakaguchi et al., 2021), RACE                        Llama’s 65.3. This shows that our dataset is in-
(accuracy) (Lai et al., 2017), PIQA (normalized                         deed suitable for state-of-the-art training over long
accuracy) (Bisk et al., 2020), Social IQA (accu-                        token horizons. For more details on this experi-
racy) (Sap et al., 2019), Commonsense QA (accu-                         ment, please see Appendix E.
racy) (Talmor et al., 2019), Openbook QA (normal-
ized accuracy) (Mihaylov et al., 2018), and MMLU                        3.3    Ablation Study
(accuracy) (Hendrycks et al., 2021).                                    To further investigate the contribution and effect
                                                                        of each module in our method, we conducted thor-
3.2 Main Results                                                        ough ablation studies.
Short Token Horizon (1T) To validate the qual-
                                                                        Extractor & Filter Comparison As we have dis-
ity of our datasets, we first train standard 8B pa-
                                                                        cussed in Section 2.1, by deploying Justext instead
rameter transformer LLMs over a relatively short
                                                                        of Trafilatura and removing filter from the post-
1T token horizon. The results are shown in Ta-
                                                                        processing step, we can attain significantly 57.4%
ble 5. Our high quality dataset (Nemotron-CC-HQ)
                                                                        more high-quality tokens. We also conduct abla-
  16
    https://github.com/EleutherAI/lm-evaluation-                        tion studies to better understand the impact of the
harness                                                                 extractor selection and the removal of filter through
                                                                    2464
downstream benchmarks. We carry out four 8B-1T            documents from Common Crawl.17
experiments. We report the benchmark scores in               We further compare each of the classifiers with
Table 7. Beyond the token-yield benefit by lever-         the ensembled method18 by their downstream
aging Justext instead of Trafilatura and not using        tasks’ performances. We pretrain 8B parameters
heuristic filters, we see that combining these two        LLMs with 1T tokens, using the high-quality docu-
does not impact the downstream task accuracies            ments labeled by different classifiers on randomly
with only marginal differences (comparing Trafi-          selected 13 Common Crawl snapshots (see Ap-
latura filtered vs. Justext unfiltered). Moreover,        pendix F). Table 9 shows the detailed comparison
when we ONLY remove filter from high-quality              on different evaluation tasks. We can see that the
tokens, the results get further improved (comparing       ensembled method greatly boost the high-quality
Justext unfiltered vs. Justext HQ unfiltered). In         tokens percentage from 9% to 25%, while still
particular, MMLU gets boosted by +2%. Note that,          achieving the highest general language understand-
the motivation behind removing filter is to boost         ing performance on average on all the tasks. The
token yield, especially on high-quality tokens due        ensembled method also outperforms the FineWeb-
to the notable scarcity of such. Given the experi-        Edu classifier and the DCLM classifier, in terms
mental results and considering the overall growth         of the high-quality token percentage, and is on-par
in token yield, we opt to only remove filter from         or slightly better on the 9 evaluation tasks. This
high-quality tokens.                                      is very important since more unique high-quality
                                                          tokens is the key in pretraining larger LLMs on
 Exp name                MMLU      Avg (non-MMLU)         longer tokens horizons.
 Trafilatura filtered      55.4           60.6
 Justext filtered          54.1           60.9               What                      #Docs           Total unique(%)
 Justext unfiltered        55.5           60.3               Total unique in union     11,359,655          100.0%
 Justext HQ-unfiltered     57.5           60.6               In intersection           1,152,821           10.1%
                                                             In FineWeb-Edu only        4,022,294           35.4%
Table 7: Ablation studies on extractor and filter. HQ        In DCLM only               6,184,540           54.4%
means high-quality data judged by FineWeb-Edu clas-
sifier (score 3,4,5). HQ-unfiltered means filtering is       Table 8: High-quality documents overlap analysis.
applied only to LQ data. See Appendix G for more
details.
                                                          Evaluating Synthetic Data As Table 10 shows,
                                                          this ablation study aim to answer two questions: (1)
Classifiers Comparison Assembling different               Does rephrasing low-quality improve accuracies on
classifiers to label the document quality is one of       downstream tasks? (2) Can synthetic data help off-
the key steps in constructing our datasets, so we         set the decreasing value of duplicated data reported
did thorough analysis and comparison of the com-          in (Muennighoff et al., 2024)? To answer these
ponent.                                                   questions, we train four 8B models with the same
                                                          hyperparameters on different blends of 1T tokens:
   We did a detailed comparison of two types of
                                                          (1) LQ-Base: original Common Crawl data in-
classifiers that we employ in our method: the
                                                          cluding low-quality documents; (2) LQ-Synthetic:
FineWeb-Edu classifier which score document
                                                          an augmented version of LQ-Base where the low-
quality based on their educational-level, and the
                                                          quality documents are rephrased; (3) HQ-Base: a
DCLM-based classifier which value the informa-
                                                          blend containing eightfold high-quality documents
tiveness of the document. We compare the high-
                                                          and less low- and medium-quality documents; (4)
quality documents predicted by the two classifiers
                                                          HQ-Synthetic: a variant of HQ-Base where 4 repe-
on a randomly selected Common Crawl Snapshot
                                                          titions of the high-quality documents are swapped
(CC-MAIN-2021-21). Table 8 shows the document
                                                          out for synthetic datasets.
statistics comparison. We can see that only 10% of
                                                              By comparing the results between LQ-Base and
the documents are predicted as high quality by both
                                                          LQ-Synthetic, we can see that rephrasing low-
classifiers, while 35.4% documents are predicted
as high quality by FineWeb-Edu classifier only, and          17
                                                                Detailed URL domain comparison can be found in Ap-
54.4% of documents are predicted as high-quality          pendix B
                                                             18
                                                                Note that we did not employ FineWeb-Edu classifier in
by DCLM classifier. Therefore, ensembling differ-         our ensemble for license issue, since it is trained with annota-
ent classifiers can increase the recall of high-quality   tions from Llama3.

                                                      2465
Classifier                 HQ(%) ARC-E ARC-C             H       W   RACE PIQA SIQA CSQA OBQA MMLU Avg
FineWeb-Edu                 8%       77.7       50.1    74.9 67.3     39.5   78.8   45.8     53.6      43.0     55.4   59.0
DCLM                       11%       76.0       49.2    76.5 70.2     38.2   80.8   33.9     55.2      45.8     56.0   58.4
Ours-mistral                9%       75.8       49.2    75.9 66.9     37.5   80.1   46.2     46.9      44.8     53.2   58.1
Ours-nemotron-340B         14%       76.3       50.3    75.6 67.5     37.8   80.2   34.3     54.0      46.2     54.9   58.0
Ours-ensembled             25%       78.0       49.7    75.3 67.1     37.2   79.6   45.7     56.8      44.8     56.4   59.4

Table 9: Different classifiers comparison. Our ensemble method includes the three classifiers: Ours-mistral, Ours-
nemotron-340B and DCLM.

    Blend          ARC-E     ARC-C          H     W      RACE        PIQA    SIQA   CSQA       OBQA           MMLU     Avg
    LQ-Base         67.7      41.8      75.2     67.1     37.4       78.8    45.3     36.9          41.0      48.2     52.5
    LQ-Synthetic    71.3      45.2      75.0     66.9     37.4       79.4    46.2     41.6          42.8      47.1     54.0
    HQ-Base         74.2      47.7      74.8     66.9     37.3       78.2    46.0     47.3          43.6      53.4     55.8
    HQ-Synthetic    76.7      49.2      74.5     67.3     38.2       78.8    45.2     47.9          45.8      53.6     56.7

                                 Table 10: Impact of incorporating synthetic data.


quality data leads to 1.50 absolute gains on average             Web, TxT360 largely focus on extraction and non-
score. We also observe noticeable boosts from                    learned heuristics (Penedo et al., 2023; Soldaini
1.80% to 4.75% on ARC-Easy, ARC-Challenge,                       et al., 2024; Rae et al., 2021; Raffel et al., 2020;
OpenbookQA, CommonsenseQA; however, we                           Tang et al., 2024). Just as for FineWeb-Edu and
also encounter slight accuracy drops on some tasks,              DCLM, the core pipeline we started from incorpo-
which may indicate potential misinformation intro-               rates many of these ideas, but our paper describes
duced by data synthesis. Current practices typically             how to modify and go beyond these non-learned
utilize data curation approaches to detect and elim-             techniques to achieve state-of-the-art accuracy and
inate noisy examples. Due to time and resource                   diversity. Concurrent work Zyda-2 shows how to
constraints, we leave the detailed exploration of                filter, cross-deduplicate, and combine the FineWeb-
this issue for future efforts.                                   Edu, DCLM, Zyda-1, and Dolma-CC datasets
   The comparison between HQ-Base and HQ-                        into a higher-accuracy and larger whole (Tokpanov
Synthetic shows that swapping 4 out of 8 epochs of               et al., 2024). In contrast, we focus on techniques
high-quality data with a mix of synthetic datasets               for the creation of a new English Common Crawl
improves accuracy on most benchmarks. This im-                   dataset rather than combinations or modifications
provement could potentially result from two fac-                 of existing datasets. Finally, many works have fo-
tors: the incorporation of fresh unique tokens and               cused on creating multilingual datasets (Xue et al.,
styles that enable the model to learn specific abili-            2021; Brack et al., 2024; Abadji et al., 2022; Wen-
ties (e.g., question answering) or absorb knowledge              zek et al., 2020; Kudugunta et al., 2023). We leave
more efficiently.                                                extension of our ideas beyond English to the future.
                                                                     Synthetic datasets have been widely used in
4     Related Work
                                                                 language model pre-training and post-training.
The Phi series of models pioneered training on                   In (Cheng et al., 2024), instruction-response pairs
small amounts of very high quality data, includ-                 are synthesized for pre-training. In (Eldan and
ing curated Web and synthetic data (Gunasekar                    Li, 2023), the authors show that smaller or sim-
et al., 2023; Li et al., 2023; Abdin et al., 2024).              pler models trained on a synthetic dataset of short
However, their focus is on shorter token hori-                   stories are capable of generating fluent and con-
zons and they share limited details. FineWeb-                    sistent stories. Similarly, smaller models trained
Edu and DCLM are the main points of compar-                      using high-quality synthetic textbook and exercise
ison for our paper (Li et al., 2024; Penedo et al.,              datasets can achieve impressive high accuracy on
2024). We build upon their core idea of model-                   coding benchmarks (Gunasekar et al., 2023; Li
based filtering, but show how to improve the fil-                et al., 2023). These approaches typically require
tering and data quantity through a combination of                a powerful language model, such as GPT-3.5 and
other techniques. Other English Common Crawl                     GPT-4 in (Eldan and Li, 2023), to synthesize new
datasets such as C4, DOLMA, Gopher, Refined-                     contents. Instead, (Maini et al., 2024) shows that
                                                          2466
compact models such as Qwen-1.8B and Mistral-            (FineWeb-Edu, DCLM) were released without de-
7B are adequate to rephrase web data. This ap-           contamination, and the model we compare against
proach generates diverse, high-quality synthetic         (Meta Llama 3.1) was also trained on contaminated
data that effectively lowers model perplexity and        data. DCLM reports some contamination analy-
boosts performance across benchmarks. We adopt           sis, but the findings suggest contamination is not
this main idea, but explore more prompts and show        a key factor: e.g., MMLU actually increases af-
how to specialize them for low and high quality          ter decontamination, and DCLM does better than
data.                                                    FineWeb on MMLU, even though FineWeb has
                                                         more MMLU contamination (see Section 4.6 and
5   Conclusion                                           Appendix N in Li et al. (2024)). Still, it would be
                                                         interesting to better understand the impact of con-
For producing long-horizon pretraining tokens for
                                                         tamination for different model sizes and different
LLMs from English Common Crawl data, we
                                                         token horizons, and we hope the community can
showed how to improve upon the state of the art
                                                         explore such questions on this public dataset.
and achieve better trade-offs between benchmark
accuracy and data quantity, as measured by number        Acknowledgments
of unique real tokens. Specifically, we showed the
efficacy of ensembling model-based quality filters,      We thank the Common Crawl Foundation for host-
rephrasing low and high quality documents, and re-       ing the dataset. We thank Pedro Ortiz Suarez
ducing the reliance on non-learned heuristics. The       for valuable feedback that improved the paper
dataset is public and split by quality level and type    and Greg Lindahl for help with improving the
(actual data vs. different types of synthetic data),     data formatting and layout. Furthermore, we
enabling the community to do further experiments         thank Ayush Dattagupta, Randy Gelhausen, Smita
on quality vs. diversity and how to build effective      Ithape, Vibhu Jawa, Nirmal Kumar Juluru, Vineeth
short and long horizon curricula.                        Kalluru, Mehran Maghoumi, Arham Mehta, Ran-
                                                         jit Rajan, Janaki Vamaraju, Ryan Wolf, and Sarah
6   Limitations                                          Yurick for help with NeMo Curator and for open
                                                         sourcing Nemotron-CC recipes and classifiers as
Some of the key limitations of our work are as
                                                         part of NeMo Curator.
follows. For the model-based filter ensembling
and quality bucketing, we only had time and re-
sources to try a single strategy. Though it is ef-       References
fective, it is possible this could be improved upon
in future work, especially to improve the sensitiv-      Julien Abadji, Pedro Ortiz Suarez, Laurent Romary, and
                                                            Benoît Sagot. 2022. Towards a cleaner document-
ity at the higher-quality end of the spectrum. For          oriented multilingual crawled corpus. In Proceedings
the rephrased data, we did not verify the factual           of the Thirteenth Language Resources and Evalua-
accuracy or fidelity to the original contents. More         tion Conference, pages 4344–4355, Marseille, France.
work is required to understand the risks of halluci-        European Language Resources Association.
nations or loss of content diversity in this setting     Marah Abdin, Sam Ade Jacobs, Ammar Ahmad Awan,
and how to mitigate them. We also only looked at          Jyoti Aneja, Ahmed Awadallah, Hany Awadalla,
rephrasing low and high quality data. It could be         Nguyen Bach, Amit Bahree, Arash Bakhtiari, Harki-
interesting to explore how to best rephrase medium        rat Behl, et al. 2024. Phi-3 technical report: A highly
                                                          capable language model locally on your phone. arXiv
quality data as well. We did not do ablations on          preprint arXiv:2404.14219.
all parts of the pipeline. There is probably room
for improvement with, for example, the language          Bo Adler, Niket Agarwal, Ashwath Aithal, Dong H Anh,
identification. Overall, we tried our methods only         Pallab Bhattacharya, Annika Brundyn, Jared Casper,
                                                           Bryan Catanzaro, Sharon Clay, Jonathan Cohen, et al.
on English text. More work is needed to adapt our          2024. Nemotron-4 340b technical report. arXiv
methods to other languages.                                preprint arXiv:2406.11704.
   Finally, we did not decontaminate the dataset, as
there is not yet a strong consensus on how to best do    Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury
                                                            Zemlyanskiy, Federico Lebron, and Sumit Sanghai.
this and the impact is uncertain and debated, espe-         2023. Gqa: Training generalized multi-query trans-
cially for large models trained over large token hori-      former models from multi-head checkpoints. In Pro-
zons. We note that the datasets we compare against          ceedings of the 2023 Conference on Empirical Meth-
                                                     2467
  ods in Natural Language Processing, pages 4895–             Bryan Catanzaro. 2024. Maximize your data’s po-
  4901.                                                       tential: Enhancing llm accuracy with two-phase pre-
                                                              training. Preprint, arXiv:2412.15285.
Adrien Barbaresi. 2021. Trafilatura: A Web Scrap-
  ing Library and Command-Line Tool for Text Dis-          Leo Gao, Jonathan Tow, Baber Abbasi, Stella Biderman,
  covery and Extraction. In Proceedings of the Joint         Sid Black, Anthony DiPofi, Charles Foster, Laurence
  Conference of the 59th Annual Meeting of the Asso-         Golding, Jeffrey Hsu, Alain Le Noac’h, Haonan Li,
  ciation for Computational Linguistics and the 11th         Kyle McDonell, Niklas Muennighoff, Chris Ociepa,
  International Joint Conference on Natural Language         Jason Phang, Laria Reynolds, Hailey Schoelkopf,
  Processing: System Demonstrations, pages 122–131.          Aviya Skowron, Lintang Sutawika, Eric Tang, An-
  Association for Computational Linguistics.                 ish Thite, Ben Wang, Kevin Wang, and Andy Zou.
                                                             2023. A framework for few-shot language model
Loubna Ben Allal. 2024. Most of the data is du-              evaluation.
  plicated? https://huggingface.co/datasets/
  HuggingFaceFW/fineweb-edu/discussions/7.                 Suriya Gunasekar, Yi Zhang, Jyoti Aneja, Caio
  Accessed: October 24, 2024.                                César Teodoro Mendes, Allie Del Giorno, Sivakanth
                                                             Gopi, Mojan Javaheripi, Piero Kauffmann, Gustavo
Yonatan Bisk, Rowan Zellers, Jianfeng Gao, Yejin Choi,       de Rosa, Olli Saarikivi, et al. 2023. Textbooks are all
  et al. 2020. Piqa: Reasoning about physical com-           you need. arXiv preprint arXiv:2306.11644.
  monsense in natural language. In Proceedings of the
  AAAI conference on artificial intelligence, volume 34,   Kenneth Heafield. 2011. Kenlm: Faster and smaller
  pages 7432–7439.                                           language model queries. In Proceedings of the sixth
                                                             workshop on statistical machine translation, pages
Manuel Brack, Malte Ostendorff, Pedro Ortiz Suarez,
                                                             187–197.
 José Javier Saiz, Iñaki Lacunza Castilla, Jorge
 Palomar-Giner,      Alexander Shvets,      Patrick        Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
 Schramowski, Georg Rehm, Marta Villegas,                    Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
 and Kristian Kersting. 2024. Community OSCAR:               2021. Measuring massive multitask language under-
 A community effort for multilingual web data. In            standing. In International Conference on Learning
 Proceedings of the Fourth Workshop on Multilingual          Representations.
 Representation Learning (MRL 2024), pages
 232–235, Miami, Florida, USA. Association for             Armand Joulin, Edouard Grave, Piotr Bojanowski,
 Computational Linguistics.                                  Matthijs Douze, Hérve Jégou, and Tomas Mikolov.
                                                             2016. Fasttext.zip: Compressing text classification
Daixuan Cheng, Yuxian Gu, Shaohan Huang, Junyu Bi,           models. arXiv preprint arXiv:1612.03651.
  Minlie Huang, and Furu Wei. 2024. Instruction pre-
  training: Language models are supervised multitask       Armand Joulin, Edouard Grave, Piotr Bojanowski, and
  learners. In Proceedings of the 2024 Conference on         Tomas Mikolov. 2017. Bag of tricks for efficient
  Empirical Methods in Natural Language Processing,          text classification. In Proceedings of the 15th Con-
  pages 2529–2550, Miami, Florida, USA. Association          ference of the European Chapter of the Association
  for Computational Linguistics.                             for Computational Linguistics: Volume 2, Short Pa-
                                                             pers, pages 427–431, Valencia, Spain. Association
Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot,
                                                             for Computational Linguistics.
  Ashish Sabharwal, Carissa Schoenick, and Oyvind
  Tafjord. 2018. Think you have solved question an-        Sneha Kudugunta, Isaac Caswell, Biao Zhang, Xavier
  swering? try arc, the ai2 reasoning challenge. arXiv       Garcia, Derrick Xin, Aditya Kusupati, Romi Stella,
  preprint arXiv:1803.05457.                                 Ankur Bapna, and Orhan Firat. 2023. Madlad-400:
Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,             A multilingual and document-level large audited
  Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,            dataset. Advances in Neural Information Process-
  Akhil Mathur, Alan Schelten, Amy Yang, Angela              ing Systems, 36:67284–67296.
  Fan, et al. 2024. The llama 3 herd of models. arXiv
                                                           Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang,
  preprint arXiv:2407.21783.
                                                             and Eduard Hovy. 2017. Race: Large-scale read-
Ronen Eldan and Yuanzhi Li. 2023. Tinystories: How           ing comprehension dataset from examinations. In
  small can language models be and still speak coherent      Proceedings of the 2017 Conference on Empirical
  english? arXiv preprint arXiv:2305.07759.                  Methods in Natural Language Processing, pages 785–
                                                             794.
Angela Fan, Yacine Jernite, Ethan Perez, David Grang-
  ier, Jason Weston, and Michael Auli. 2019. Eli5:         Katherine Lee, Daphne Ippolito, Andrew Nystrom,
  Long form question answering. In Proceedings of            Chiyuan Zhang, Douglas Eck, Chris Callison-Burch,
  the 57th Annual Meeting of the Association for Com-        and Nicholas Carlini. 2022. Deduplicating training
  putational Linguistics, pages 3558–3567.                   data makes language models better. In Proceedings
                                                             of the 60th Annual Meeting of the Association for
Steven Feng, Shrimai Prabhumoye, Kezhi Kong, Dan             Computational Linguistics (Volume 1: Long Papers),
   Su, Mostofa Patwary, Mohammad Shoeybi, and                pages 8424–8445.
                                                       2468
Jeffrey Li, Alex Fang, Georgios Smyrnis, Maor Ivgi,          Jack W Rae, Sebastian Borgeaud, Trevor Cai, Katie
   Matt Jordan, Samir Gadre, Hritik Bansal, Etash Guha,         Millican, Jordan Hoffmann, Francis Song, John
   Sedrick Keh, Kushal Arora, et al. 2024. Datacomp-           Aslanides, Sarah Henderson, Roman Ring, Susan-
   LM: In search of the next generation of training sets        nah Young, et al. 2021. Scaling language models:
   for language models. In The Thirty-eight Conference          Methods, analysis & insights from training gopher.
   on Neural Information Processing Systems Datasets            arXiv preprint arXiv:2112.11446.
   and Benchmarks Track.
                                                             Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
Yuanzhi Li, Sébastien Bubeck, Ronen Eldan, Allie               Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
  Del Giorno, Suriya Gunasekar, and Yin Tat Lee. 2023.         Wei Li, and Peter J Liu. 2020. Exploring the lim-
  Textbooks are all you need ii: phi-1.5 technical report.     its of transfer learning with a unified text-to-text
  arXiv preprint arXiv:2309.05463.                             transformer. Journal of machine learning research,
                                                               21(140):1–67.
Pratyush Maini, Skyler Seto, He Bai, David Grangier,
  Yizhe Zhang, and Navdeep Jaitly. 2024. Rephras-            Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavat-
  ing the web: A recipe for compute and data-efficient         ula, and Yejin Choi. 2021. Winogrande: An adver-
  language modeling. In ICLR 2024 Workshop on Navi-            sarial winograd schema challenge at scale. Commu-
  gating and Addressing Data Problems for Foundation           nications of the ACM, 64(9):99–106.
  Models.
                                                             Maarten Sap, Hannah Rashkin, Derek Chen, Ronan
Luke Merrick, Danmei Xu, Gaurav Nuti, and Daniel              Le Bras, and Yejin Choi. 2019. Social iqa: Com-
  Campos. 2024. Arctic-embed: Scalable, efficient,            monsense reasoning about social interactions. In
  and accurate text embedding models. arXiv preprint          Proceedings of the 2019 Conference on Empirical
  arXiv:2405.05374.                                           Methods in Natural Language Processing and the 9th
                                                              International Joint Conference on Natural Language
Todor Mihaylov, Peter Clark, Tushar Khot, and Ashish          Processing (EMNLP-IJCNLP), pages 4463–4473.
  Sabharwal. 2018. Can a suit of armor conduct elec-
  tricity? a new dataset for open book question an-          Noam Shazeer. 2020. Glu variants improve transformer.
  swering. In Proceedings of the 2018 Conference on            arXiv preprint arXiv:2002.05202.
  Empirical Methods in Natural Language Processing,
  pages 2381–2391.                                           Mohammad Shoeybi, Mostofa Patwary, Raul Puri,
                                                              Patrick LeGresley, Jared Casper, and Bryan Catan-
Niklas Muennighoff, Alexander Rush, Boaz Barak,               zaro. 2019. Megatron-lm: Training multi-billion
  Teven Le Scao, Nouamane Tazi, Aleksandra Piktus,            parameter language models using model parallelism.
  Sampo Pyysalo, Thomas Wolf, and Colin A Raffel.             arXiv preprint arXiv:1909.08053.
  2024. Scaling data-constrained language models.
  Advances in Neural Information Processing Systems,         Luca Soldaini, Rodney Kinney, Akshita Bhagia, Dustin
  36.                                                          Schwenk, David Atkinson, Russell Authur, Ben Bo-
                                                               gin, Khyathi Chandu, Jennifer Dumas, Yanai Elazar,
Jupinder Parmar, Shrimai Prabhumoye, Joseph Jennings,          et al. 2024. Dolma: an open corpus of three trillion
  Bo Liu, Aastha Jhunjhunwala, Zhilin Wang, Mostofa            tokens for language model pretraining research. In
  Patwary, Mohammad Shoeybi, and Bryan Catanzaro.              Proceedings of the 62nd Annual Meeting of the As-
  2024. Data, data everywhere: A guide for pretraining         sociation for Computational Linguistics (Volume 1:
  dataset construction. In Proceedings of the 2024 Con-        Long Papers), pages 15725–15788.
  ference on Empirical Methods in Natural Language
  Processing, pages 10671–10695.                             Alon Talmor, Jonathan Herzig, Nicholas Lourie, and
                                                               Jonathan Berant. 2019. Commonsenseqa: A question
Guilherme Penedo, Hynek Kydlíček, Loubna Ben al-              answering challenge targeting commonsense knowl-
  lal, Anton Lozhkov, Margaret Mitchell, Colin Raffel,         edge. In Proceedings of the 2019 Conference of
  Leandro Von Werra, and Thomas Wolf. 2024. The                the North American Chapter of the Association for
  fineweb datasets: Decanting the web for the finest           Computational Linguistics: Human Language Tech-
  text data at scale. In The Thirty-eight Conference on        nologies, Volume 1 (Long and Short Papers), pages
  Neural Information Processing Systems Datasets and           4149–4158.
  Benchmarks Track.
                                                             Liping Tang, Nikhil Ranjan, Omkar Pangarkar, Xuezhi
Guilherme Penedo, Quentin Malartic, Daniel Hesslow,            Liang, Zhen Wang, Li An, Bhaskar Rao, Ling-
  Ruxandra Cojocaru, Hamza Alobeidli, Alessandro               hao Jin, Huijuan Wang, Zhoujun Cheng, Suqi Sun,
  Cappelli, Baptiste Pannier, Ebtesam Almazrouei, and          Cun Mu, Victor Miller, Xuezhe Ma, Yue Peng,
  Julien Launay. 2023. The refinedweb dataset for fal-         Zhengzhong Liu, and Eric P. Xing. 2024. Txt360:
  con llm: Outperforming curated corpora with web              A top-quality llm pre-training dataset requires the
  data only. Advances in Neural Information Process-           perfect blend. https://huggingface.co/spaces/
  ing Systems, 36:79155–79172.                                 LLM360/TxT360. Accessed: October 24, 2024.
Jan Pomikálek. 2011. Removing boilerplate and du-            Gemma Team, Morgane Riviere, Shreya Pathak,
  plicate content from web corpora. Disertacnı práce,          Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupati-
  Masarykova univerzita, Fakulta informatiky.                  raju, Léonard Hussenot, Thomas Mesnard, Bobak
                                                         2469
  Shahriari, Alexandre Ramé, et al. 2024. Gemma 2:         A         Pipeline Overview
  Improving open language models at a practical size.
  arXiv preprint arXiv:2408.00118.                         An overview of the pipeline is shown in Figure 3.
Teknium. 2023.      Openhermes 2.5: An open                B        Comparison of FineWeb-Edu and
  dataset of synthetic data for generalist llm as-
  sistants.   https://huggingface.co/datasets/                      DCLM Classifier
  teknium/OpenHermes-2.5. Accessed: October 24,
                                                           Different classifiers have different standards for
  2024.
                                                           high-quality documents. Thus, ensemble multi-
Yury Tokpanov, Paolo Glorioso, Quentin Anthony, and        ple classifiers will help increase the recall of high-
  Beren Millidge. 2024. Zyda-2: a 5 trillion token         quality documents. We did a detailed compari-
  high-quality dataset. Preprint, arXiv:2411.06068.
                                                           son of two of the classifiers that we employ in our
Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa         method: the FineWeb-Edu classifier which score
  Liu, Noah A Smith, Daniel Khashabi, and Hannaneh         document quality based on their educational-level,
  Hajishirzi. 2023. Self-instruct: Aligning language
  models with self-generated instructions. In Proceed-
                                                           and the DCLM based classifier which value the
  ings of the 61st Annual Meeting of the Association for   informativeness of the document.
  Computational Linguistics (Volume 1: Long Papers),          We compare the high-quality documents pre-
  pages 13484–13508.                                       dicted by the two classifiers on one Common Crawl
Guillaume Wenzek, Marie-Anne Lachaux, Alexis Con-          snapshot (dated 2021-21). Table 8 show the doc-
  neau, Vishrav Chaudhary, Francisco Guzmán, Ar-           ument statistics comparison. We further show the
  mand Joulin, and Edouard Grave. 2020. CCNet:             detailed URL domains comparison between the
  Extracting high quality monolingual datasets from        two classifiers’ predictions in Table 11. We can
  web crawl data. In Proceedings of the Twelfth Lan-
  guage Resources and Evaluation Conference, pages         see that each classifier has their own high-quality
  4003–4012, Marseille, France. European Language          domain preferences. Among the top 1k domains,
  Resources Association.                                   only 368 domains are in the intersection. Therefore,
                                                           ensemble of different classifiers can help increase
Linting Xue, Noah Constant, Adam Roberts, Mihir Kale,
  Rami Al-Rfou, Aditya Siddhant, Aditya Barua, and         retrieving more high-quality documents from Com-
  Colin Raffel. 2021. mT5: A massively multilingual        mon Crawl.
  pre-trained text-to-text transformer. In Proceedings
  of the 2021 Conference of the North American Chap-       C         Bucket Comparison
  ter of the Association for Computational Linguistics:
  Human Language Technologies, pages 483–498, On-          To better understand the quality of data in each of
  line. Association for Computational Linguistics.         our 20 data buckets, we carry out ablation studies to
An Yang, Baosong Yang, Binyuan Hui, Bo Zheng,              test their benchmark accuracies. For each study, we
  Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan            take a 900B-token checkpoint and continue the pre-
  Li, Dayiheng Liu, Fei Huang, et al. 2024. Qwen2          training for 50B more tokens. For 34% of the 50B
  technical report. arXiv preprint arXiv:2407.10671.       tokens we used the bucket data being tested, while
Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali             we fixed the other 66% as the same data distribution
  Farhadi, and Yejin Choi. 2019. Hellaswag: Can a          of the 900B pretraining process to make sure the
  machine really finish your sentence? In Proceedings      distribution did not shift too much. See Figure 4
  of the 57th Annual Meeting of the Association for
  Computational Linguistics, pages 4791–4800.              for the results. The average accuracy is calculated
                                                           across 13 downstream tasks. Note that Bucket 19
                                                           greatly outperforms all other buckets and the differ-
                                                           ences within bucket 12-18 are marginal. We used
                                                           the results here as a reference when designing the
                                                           quality labels in Table 2.

                                                           D         Training Details: Ablations
                                                           As mentioned in Section 3.1, we use the open
                                                           source Megatron-LM library19 (Shoeybi et al.,
                                                           2019) to train 8B parameter transformer LLMs
                                                           for 1T tokens. The key hyperparameters are
                                                               19
                                                                    https://github.com/NVIDIA/Megatron-LM

                                                       2470
                            Common Crawl data



                              Text extraction



                                 Language
                               identification

                                        English

                              Deduplication




                                Ensemble-
                               of-classifier-
                              based filtering




                                 Bucketing



Low quality data            Medium quality data     High quality data



Heuristic filtering          Heuristic filtering
                                                      SDG (Diverse
                                                     QA, Distillation,
                                                       Knowledge
SDG (Wikipedia-                                         extraction,
style rephrasing)                                   Knowledge listing,
                                                     Wikipedia-style
                               Final dataset           rephrasing)




                      Figure 3: Pipeline overview




                                  2471
                                         Top domains and domain overlap analysis =>368 domains are in top 1k domains of both
     FineWeb-Edu                                   DCLM                                                    Top 1k Domains
                                    Count                        Count
     Top Domains                                Top Domains               Intersection (368)     In FineWeb-Edu only               In DCLM only
 wordpress.com                      39228 wordpress.com          85378 123helpme.com              111papers.com                     4archive.org
 thefreedictionary.com              20420 stackexchange.com      64831 24houranswers.com          3dprint.com                       4channel.org
 stackexchange.com                  17853 livejournal.com        36521 abc.net.au                 aafp.org                          4hw.com.cn
 britannica.com                     14761 medium.com             27347 abovetopsecret.com         aappublications.org               5winebar.com
 ipl.org                            13132 fandom.com             13986 academickids.com           abs.gov.au                        aawsat.com
 medium.com                         11539 ipl.org                12282 adafruit.com               accessgenealogy.com               abc11.com
 nih.gov                            10624 answers.com            10790 adobe.com                  achrnews.com                      abc30.com
 igi-global.com                      9136 nih.gov                 9091     alchetron.com          acm.org                           abc7chicago.com
 slideplayer.com                     8460 typepad.com             8078     aljazeera.com          adidasshoesoutletwholesale.com    able2know.org
 answers.com                         8103 commonsensemedia.org 7772        allegancountyedc.com adslspeedtest.net                   aceshowbiz.com
 wikipedia.org                       6867 wsj.com                 7652     allinterview.com       aero-net.org                      activerain.com
 dictionary.com                      6763 imdb.com                7263     amazon.com             agwired.com                       addicted2success.com
 en-academic.com                     5292 theatlantic.com         7008     americanbar.org        ahdictionary.com                  additudemag.com
 sciencemag.org                      5254 yahoo.com               5921     angelfire.com          ajol.info                         agingcare.com
 brainscape.com                      5129 fanfiction.net          5499     answers.com            akjournals.com                    agnostic.com
 encyclopedia.com                    4698 huffpost.com            5471     antiessays.com         aleteia.org                       airmilescalculator.com
 nasa.gov                            4615 adobe.com               5182     apple.com              alison.com                        airportia.com
 slideserve.com                      4538 scribd.com              4948     archive.org            all-creatures.org                 alarabiya.net
 scribd.com                          4430 thefreedictionary.com   4847     arduino.cc             allaboutheaven.org                alex-in-wonderland.com
 kiddle.co                           4323 mathworks.com           4655     arstechnica.com        allthatsinteresting.com           alexa-gueguen.com


                   Table 11: High Quality Documents Domains Comparison. 368 Top Domains are in the intersection.


                                                                                     as follows: We use 32 transformer layers with
                                                                                     hidden dimension 4096, 32 attention heads, and
                   48.8
                                                                                     SwiGLU activations (Shazeer, 2020). For the atten-
                                                                                     tion, we use grouped query attention with 8 query
                   48.6                                                              groups (Ainslie et al., 2023). We use the Adam
                                                                                     optimizer with β1 = 0.9, β2 = 0.95, ϵ = 1e−8,
                   48.4
                                                                                     weight decay 0.1, and the cosine learning rate
     Average Acc




                   48.2                                                              schedule with peak learning rate at 3e-4 and min-
                                                                                     imum learning rate at 3e-6. A single training run
                   48.0
                                                                                     takes about 40 hours using 1024 NVIDIA H100
                   47.8
                                                                                     GPUs.
                                                                                        The data blend breakdown for these experiments
                          12   13     14     15       16    17   18    19
                                             Bucket index                            is shown in Table 12. Experiments in this paper
                                                                                     varied only the 73% English Common Crawl por-
                    Figure 4: Ablation study on the buckets.
                                                                                     tion.

                                                                                      E Long-Horizon Curriculum Details
                                                                                      For the 15T token training run, a two-phase curricu-
                                                                                      lum was employed that is described in more detail
                                                                                      in Feng et al. (2024). The first phase of 9T tokens
 Category                                                             Blend %         used 59% English Common Crawl data (5.31T) and
 English Common Crawl                                                       73
                                                                                      the second phase of 6T tokens used 31% (1.86T),
 Books and patents                                                           9        for a combined total of 47.8% (7.17T). In the first
 Papers                                                                      9        phase, we used medium, medium-high, and high
 Code                                                                        5
 Conversational                                                              3        quality data (real and synthetic), and in the sec-
 Wikipedia                                                                   1        ond phase we used only high quality data (real and
                                                                                      synthetic).
Table 12: Data blend for the experiments with 8B pa-
rameter transformer LLMs trained for 1T tokens. Ex-                                   F     Common Crawl Snapshots
periments in this paper varied only the 73% English
Common Crawl portion.                                                                 For the main datasets, we used the 99 snapshots
                                                                                      CC-MAIN-2013-20 through CC-MAIN-2024-30.
                                                                                         The thirteen Common Crawl snapshots we use
                                                                                      in some of the analysis and 1T token experiments
                                                                                 2472
are CC-MAIN-2023-23, CC-MAIN-2023-14, CC-
MAIN-2023-06, CC-MAIN-2022-49, CC-MAIN-
2022-27, CC-MAIN-2022-05, CC-MAIN-2021-
43, CC-MAIN-2021-21, CC-MAIN-2021-04, CC-
MAIN-2020-45, CC-MAIN-2020-29, CC-MAIN-
2020-05, CC-MAIN-2019-35.

G    Extractor & Filter Ablation
The Avg tasks include ARC-Easy, ARC-Challenge,
Hellaswag, Winogrande, RACE, PIQA, Common-
sense QA, Openbook QA.
  Note that we only use FineWeb-Edu classifier
for the quality labels of this ablation study and
analysis. We do not use it in the final preparation
of our dataset. See Section 2.2 for the details of
our classifiers being used eventually to prepare the
data.

H    Prompt Templates
Prompts 1-5 show the prompt templates we use for
synthetic data generation.




                                                   2473
Task: Read the text, ask questions and answer them.

Follow these instructions:
1. Ask diverse questions that require different cognitive skills or cover different aspects of the
text.
2. Ask questions in various forms such as:
  - Yes/No questions that require determining whether a statement is true or false.
  - Open-ended questions that begin with words like what, how, when, where, why and who.
  - Multi-choice questions that offers two or more options to choose from. Include the options in the
   question.
  - Comparison questions that compare two quantities or objects and determine the relationship
  between them.
  - Reading comprehension questions that test the ability to understand and analyze the text.
  - Problem-solving questions that test the ability to solve mathematical, physical, or logical
  problems.
3. Focus on asking questions about factual information, important knowledge, or concrete details in
the text.
4. Write questions and answers using clear and concise language.
5. Use plain text. Do not use Markdown.
6. Each question and answer pair should be on a separate line. Tag the question with "Question:" and
the answer with "Answer:".

Text:
[DOCUMENT SEGMENT]

Task:
After reading the above text, ask up to 8 questions and provide the correct answers following the
instructions. Give your response in this format:

Here are the questions and answers based on the provided text:
- Question: [first question] Answer: [first answer]
- Question: [second question] Answer: [second answer]
....

                              Prompt 1: Prompt template: Diverse QA pairs




Your task is to read and paraphrase the provided text following these instructions:
- Aim to create a condensed but accurate and informative version of the original text, not a
simplistic summary.
- Capture and preserve the crucial information, key concepts, important values, and factual details
in the original text, while making it more readable and accessible.
- Retain technical terms, specialized vocabulary, and complex concepts.
- Retain examples, explanations of reasoning processes, and supporting evidence to maintain the text'
s depth and context.
- Only include information that is present in the original text. Do not adding new or unsubstantiated
 claims.
- Write in plain text.

Here is the text:
[DOCUMENT SEGMENT]

Task:
After thoroughly reading the above text, paraphrase it in high-quality and clear English following
the instructions.

                                  Prompt 2: Prompt template: Distill.




                                                 2474
Review the text and extract the key information. Follow these instructions:
- Carefully read the above text and provide a concise and organized list of factual information,
concrete details, key concepts, and important numbers and statistics extracted from the text.
- Ensure each point is clear, specific, and supported by the original text.
- Ensure the extract text is information-dense and easier to learn from.
- Do not add titles or headings.

Text:
[DOCUMENT SEGMENT]

Task:
Extract the factual information, concrete details, and key concepts from the above text following the
 instructions.

                               Prompt 3: Prompt template: Knowledge list.




Your task is to rewrite knowledge from the provided text following these instructions:
- Rewrite the text as a passage or passages using easy-to-understand and high-quality English like
sentences in textbooks and Wikipedia.
- Focus on content in disciplines such as humanities, social sciences, natural sciences, technology,
engineering, math, law and legal, business, management, art, education, agricultural sciences,
politics, and history.
- Disregard content that does not contain useful facts or knowledge.
- Retain examples, explanations of reasoning processes, and supporting evidence to maintain the text'
s depth and context.
- Do not add or alter details. Only restate what is already in the text.
- Write in plain text.
- Do not add titles, subtitles, note, or comment.

Text:
[DOCUMENT SEGMENT]

Task:
Rewrite facts and knowledge from the above text as a passage or passages following the instructions.

                             Prompt 4: Prompt template: Extract knowledge.




For the following paragraph give me a diverse paraphrase of the same in high quality English language
 as in sentences on Wikipedia. Begin your answer on a separate line with "Here is a paraphrased
version:".

Text: [DOCUMENT SEGMENT]

                Prompt 5: Prompt template: Wikipedia-style rephrasing (Maini et al., 2024).




                                                   2475
