# Don't Stop Pretraining: Adapt Language Models to Domains and Tasks

Suchin Gururangan† Ana Marasovic´ †♦ Swabha Swayamdipta† Kyle Lo† Iz Beltagy† Doug Downey† Noah A. Smith†♦

†Allen Institute for Artificial Intelligence, Seattle, WA, USA ♦Paul G. Allen School of Computer Science & Engineering, University of Washington, Seattle, WA, USA {suching,anam,swabhas,kylel,beltagy,dougd,noah}@allenai.org

### Abstract

Language models pretrained on text from a wide variety of sources form the foundation of today's NLP. In light of the success of these broad-coverage models, we investigate whether it is still helpful to tailor a pretrained model to the domain of a target task. We present a study across four domains (biomedical and computer science publications, news, and reviews) and eight classification tasks, showing that a second phase of pretraining indomain (*domain-adaptive pretraining*) leads to performance gains, under both high- and low-resource settings. Moreover, adapting to the task's unlabeled data (*task-adaptive pretraining*) improves performance even after domain-adaptive pretraining. Finally, we show that adapting to a task corpus augmented using simple data selection strategies is an effective alternative, especially when resources for domain-adaptive pretraining might be unavailable. Overall, we consistently find that multiphase adaptive pretraining offers large gains in task performance.

### 1 Introduction

Today's pretrained language models are trained on massive, heterogeneous corpora [\(Raffel et al.,](#page-10-0) [2019;](#page-10-0) [Yang et al.,](#page-11-0) [2019\)](#page-11-0). For instance, ROBERTA [\(Liu](#page-10-1) [et al.,](#page-10-1) [2019\)](#page-10-1) was trained on over 160GB of uncompressed text, with sources ranging from Englishlanguage encyclopedic and news articles, to literary works and web content. Representations learned by such models achieve strong performance across many tasks with datasets of varying sizes drawn from a variety of sources (e.g., [Wang et al.,](#page-10-2) [2018,](#page-10-2) [2019\)](#page-10-3). This leads us to ask whether a task's textual *domain*—a term typically used to denote a distribution over language characterizing a given topic or genre (such as "science" or "mystery novels")—is still relevant. Do the latest large pretrained models work universally or is it still helpful to build

<span id="page-0-0"></span>![](_page_0_Picture_7.jpeg)

Figure 1: An illustration of data distributions. Task data is comprised of an observable task distribution, usually non-randomly sampled from a wider distribution (light grey ellipsis) within an even larger target domain, which is not necessarily one of the domains included in the original LM pretraining domain – though overlap is possible. We explore the benefits of continued pretraining on data from the task distribution and the domain distribution.

separate pretrained models for specific domains?

While some studies have shown the benefit of continued pretraining on domain-specific unlabeled data (e.g., [Lee et al.,](#page-10-4) [2019\)](#page-10-4), these studies only consider a single domain at a time and use a language model that is pretrained on a smaller and less diverse corpus than the most recent language models. Moreover, it is not known how the benefit of continued pretraining may vary with factors like the amount of available labeled task data, or the proximity of the target domain to the original pretraining corpus (see Figure [1\)](#page-0-0).

We address this question for one such highperforming model, ROBERTA [\(Liu et al.,](#page-10-1) [2019\)](#page-10-1) (§[2\)](#page-1-0). We consider four domains (biomedical and computer science publications, news, and reviews; §[3\)](#page-1-1) and eight classification tasks (two in each domain). For targets that are not already in-domain for ROBERTA, our experiments show that continued pretraining on the domain (which we refer to as *domain-adaptive pretraining* or DAPT) consistently improves performance on tasks from the target domain, in both high- and low-resource settings.

Above, we consider domains defined around genres and forums, but it is also possible to induce a domain from a given corpus used for a task, such as the one used in supervised training of a model. This raises the question of whether pretraining on a corpus more directly tied to the *task* can further improve performance. We study how domainadaptive pretraining compares to *task-adaptive pretraining*, or TAPT, on a smaller but directly taskrelevant corpus: the unlabeled task dataset (§[4\)](#page-4-0), drawn from the *task distribution*. Task-adaptive pretraining has been shown effective [\(Howard and](#page-9-0) [Ruder,](#page-9-0) [2018\)](#page-9-0), but is not typically used with the most recent models. We find that TAPT provides a large performance boost for ROBERTA, with or without domain-adaptive pretraining.

Finally, we show that the benefits from taskadaptive pretraining increase when we have additional unlabeled data from the task distribution that has been *manually curated* by task designers or annotators. Inspired by this success, we propose ways to automatically select additional task-relevant unlabeled text, and show how this improves performance in certain low-resource cases (§[5\)](#page-5-0). On all tasks, our results using adaptive pretraining techniques are competitive with the state of the art.

In summary, our contributions include:

- a thorough analysis of domain- and taskadaptive pretraining across four domains and eight tasks, spanning low- and high-resource settings;
- an investigation into the transferability of adapted LMs across domains and tasks; and
- a study highlighting the importance of pretraining on human-curated datasets, and a simple data selection strategy to automatically approach this performance.

Our code as well as pretrained models for multiple domains and tasks are publicly available.[1](#page-1-2)

### <span id="page-1-0"></span>2 Background: Pretraining

Learning for most NLP research systems since 2018 consists of training in two stages. First, a neural language model (LM), often with millions of parameters, is trained on large unlabeled corpora. The word (or wordpiece; [Wu et al.](#page-11-1) [2016\)](#page-11-1) representations learned in the *pretrained* model are then reused in supervised training for a downstream task, with optional updates (*fine-tuning*) of the representations and network from the first stage.

One such pretrained LM is ROBERTA [\(Liu](#page-10-1) [et al.,](#page-10-1) [2019\)](#page-10-1), which uses the same transformerbased architecture [\(Vaswani et al.,](#page-10-5) [2017\)](#page-10-5) as its predecessor, BERT [\(Devlin et al.,](#page-9-1) [2019\)](#page-9-1). It is trained with a masked language modeling objective (i.e., cross-entropy loss on predicting randomly masked tokens). The unlabeled pretraining corpus for ROBERTA contains over 160 GB of uncompressed raw text from different English-language corpora (see Appendix §[A.1\)](#page-12-0). ROBERTA attains better performance on an assortment of tasks than its predecessors, making it our baseline of choice.

Although ROBERTA's pretraining corpus is derived from multiple sources, it has not yet been established if these sources are diverse enough to generalize to most of the variation in the English language. In other words, we would like to understand what is out of ROBERTA's domain. Towards this end, we explore further adaptation by continued pretraining of this large LM into two categories of unlabeled data: (i) large corpora of domain-specific text (§[3\)](#page-1-1), and (ii) available unlabeled data associated with a given task (§[4\)](#page-4-0).

### <span id="page-1-1"></span>3 Domain-Adaptive Pretraining

Our approach to domain-adaptive pretraining (DAPT) is straightforward—we continue pretraining ROBERTA on a large corpus of unlabeled domain-specific text. The four domains we focus on are biomedical (BIOMED) papers, computer science (CS) papers, newstext from REALNEWS, and AMAZON reviews. We choose these domains because they have been popular in previous work, and datasets for text classification are available in each. Table [1](#page-2-0) lists the specifics of the unlabeled datasets in all four domains, as well as ROBERTA's training corpus.[1](#page-1-3)

#### <span id="page-1-4"></span>3.1 Analyzing Domain Similarity

Before performing DAPT, we attempt to quantify the similarity of the target domain to ROBERTA's pretraining domain. We consider domain vocabularies containing the top 10K most frequent unigrams (excluding stopwords) in comparably sized

<span id="page-1-2"></span><sup>1</sup>[https://github.com/allenai/](https://github.com/allenai/dont-stop-pretraining) [dont-stop-pretraining](https://github.com/allenai/dont-stop-pretraining)

<span id="page-1-3"></span><sup>1</sup> For BIOMED and CS, we used an internal version of S2ORC that contains papers that cannot be released due to copyright restrictions.

<span id="page-2-0"></span>

| Domain             | Pretraining Corpus                                   | # Tokens | Size  | LROB.     | LDAPT |
|--------------------|------------------------------------------------------|----------|-------|-----------|-------|
| BIOMED             | 2.68M full-text papers from S2ORC (Lo et al., 2020)  | 7.55B    | 47GB  | 1.32      | 0.99  |
| CS                 | 2.22M full-text papers from S2ORC (Lo et al., 2020)  | 8.10B    | 48GB  | 1.63      | 1.34  |
| NEWS               | 11.90M articles from REALNEWS (Zellers et al., 2019) | 6.66B    | 39GB  | 1.08      | 1.16  |
| REVIEWS            | 24.75M AMAZON reviews (He and McAuley, 2016)         | 2.11B    | 11GB  | 2.10      | 1.93  |
| ROBERTA (baseline) | see Appendix §A.1                                    | N/A      | 160GB | ‡<br>1.19 | -     |

Table 1: List of the domain-specific unlabeled datasets. In columns 5 and 6, we report ROBERTA's masked LM loss on 50K randomly sampled held-out documents from each domain before (L<sup>R</sup>OB.) and after (LDAPT) DAPT (lower implies a better fit on the sample). ‡ indicates that the masked LM loss is estimated on data sampled from sources *similar* to ROBERTA's pretraining corpus.

<span id="page-2-1"></span>![](_page_2_Figure_2.jpeg)

Figure 2: Vocabulary overlap (%) between domains. PT denotes a sample from sources similar to ROBERTA's pretraining corpus. Vocabularies for each domain are created by considering the top 10K most frequent words (excluding stopwords) in documents sampled from each domain.

random samples of held-out documents in each domain's corpus. We use 50K held-out documents for each domain other than REVIEWS, and 150K held-out documents in REVIEWS, since they are much shorter. We also sample 50K documents from sources similar to ROBERTA's pretraining corpus (i.e., BOOKCORPUS, STORIES, WIKIPEDIA, and REALNEWS) to construct the pretraining domain vocabulary, since the original pretraining corpus is not released. Figure [2](#page-2-1) shows the vocabulary overlap across these samples. We observe that ROBERTA's pretraining domain has strong vocabulary overlap with NEWS and REVIEWS, while CS and BIOMED are far more dissimilar to the other domains. This simple analysis suggests the degree of benefit to be expected by adaptation of ROBERTA to different domains—the more dissimilar the domain, the higher the potential for DAPT.

#### <span id="page-2-2"></span>3.2 Experiments

Our LM adaptation follows the settings prescribed for training ROBERTA. We train ROBERTA on each domain for 12.5K steps, which amounts to single pass on each domain dataset, on a v3-8 TPU; see other details in Appendix [B.](#page-12-1) This second phase of pretraining results in four domain-adapted LMs, one for each domain. We present the masked LM loss of ROBERTA on each domain before and after DAPT in Table [1.](#page-2-0) We observe that masked LM loss decreases in all domains except NEWS after DAPT, where we observe a marginal increase. We discuss cross-domain masked LM loss in Appendix §[E.](#page-14-0)

Under each domain, we consider two text classification tasks, as shown in Table [2.](#page-3-0) Our tasks represent both high- and low-resource (≤ 5K labeled training examples, and no additional unlabeled data) settings. For HYPERPARTISAN, we use the data splits from [Beltagy et al.](#page-9-3) [\(2020\)](#page-9-3). For RCT, we represent all sentences in one long sequence for simultaneous prediction.

Baseline As our baseline, we use an off-the-shelf ROBERTA-base model and perform supervised fine-tuning of its parameters for each classification task. On average, ROBERTA is not drastically behind the state of the art (details in Appendix §[A.2\)](#page-12-2), and serves as a good baseline since it provides a single LM to adapt to different domains.

Classification Architecture Following standard practice [\(Devlin et al.,](#page-9-1) [2019\)](#page-9-1) we pass the final layer [CLS] token representation to a task-specific feedforward layer for prediction (see Table [14](#page-15-0) in Appendix for more hyperparameter details).

Results Test results are shown under the DAPT column of Table [3](#page-3-1) (see Appendix §[C](#page-13-0) for validation results). We observe that DAPT improves over ROBERTA in all domains. For BIOMED, CS, and REVIEWS, we see consistent improve-

<span id="page-3-0"></span>

| Domain  | Task                      | Label Type                             | Train (Lab.)    | Train (Unl.) | Dev.         | Test           | Classes |
|---------|---------------------------|----------------------------------------|-----------------|--------------|--------------|----------------|---------|
| BIOMED  | CHEMPROT                  | relation classification                | 4169            | -            | 2427         | 3469           | 13      |
|         | †RCT                      | abstract sent. roles                   | 18040           | -            | 30212        | 30135          | 5       |
| CS      | ACL-ARC                   | citation intent                        | 1688            | -            | 114          | 139            | 6       |
|         | SCIERC                    | relation classification                | 3219            | -            | 455          | 974            | 7       |
| NEWS    | HYPERPARTISAN             | partisanship                           | 515             | 5000         | 65           | 65             | 2       |
|         | †AGNEWS                   | topic                                  | 115000          | -            | 5000         | 7600           | 4       |
| REVIEWS | †HELPFULNESS<br>†<br>IMDB | review helpfulness<br>review sentiment | 115251<br>20000 | -<br>50000   | 5000<br>5000 | 25000<br>25000 | 2<br>2  |

Table 2: Specifications of the various target task datasets. † indicates high-resource settings. Sources: CHEMPROT [\(Kringelum et al.,](#page-9-4) [2016\)](#page-9-4), RCT [\(Dernoncourt and Lee,](#page-9-5) [2017\)](#page-9-5), ACL-ARC [\(Jurgens et al.,](#page-9-6) [2018\)](#page-9-6), SCIERC [\(Luan](#page-10-7) [et al.,](#page-10-7) [2018\)](#page-10-7), HYPERPARTISAN [\(Kiesel et al.,](#page-9-7) [2019\)](#page-9-7), AGNEWS [\(Zhang et al.,](#page-11-3) [2015\)](#page-11-3), HELPFULNESS [\(McAuley](#page-10-8) [et al.,](#page-10-8) [2015\)](#page-10-8), IMDB [\(Maas et al.,](#page-10-9) [2011\)](#page-10-9).

<span id="page-3-1"></span>

| Dom. | Task                     | ROBA.              | DAPT               | ¬DAPT              |
|------|--------------------------|--------------------|--------------------|--------------------|
| BM   | CHEMPROT 81.91.0<br>†RCT | 87.20.1            | 84.20.2<br>87.60.1 | 79.41.3<br>86.90.1 |
| CS   | ACL-ARC<br>SCIERC        | 63.05.8<br>77.31.9 | 75.42.5<br>80.81.5 | 66.44.1<br>79.20.9 |
| NEWS | HYP.<br>†AGNEWS          | 86.60.9<br>93.90.2 | 88.25.9<br>93.90.2 | 76.44.9<br>93.50.2 |
| REV. | †HELPFUL.<br>†<br>IMDB   | 65.13.4<br>95.00.2 | 66.51.4<br>95.40.2 | 65.12.8<br>94.10.4 |

Table 3: Comparison of ROBERTA (ROBA.) and DAPT to adaptation to an *irrelevant* domain (¬ DAPT). Reported results are test macro-F1, except for CHEMPROT and RCT, for which we report micro-F1, following [Beltagy et al.](#page-9-8) [\(2019\)](#page-9-8). We report averages across five random seeds, with standard deviations as subscripts. † indicates high-resource settings. Best task performance is boldfaced. See §[3.3](#page-3-2) for our choice of irrelevant domains.

ments over ROBERTA, demonstrating the benefit of DAPT when the target domain is more distant from ROBERTA's source domain. The pattern is consistent across high- and low- resource settings. Although DAPT does not increase performance on AGNEWS, the benefit we observe in HYPERPAR-TISAN suggests that DAPT may be useful even for tasks that align more closely with ROBERTA's source domain.

#### <span id="page-3-2"></span>3.3 Domain Relevance for DAPT

Additionally, we compare DAPT against a setting where for each task, we adapt the LM to a domain outside the domain of interest. This controls for the case in which the improvements over ROBERTA might be attributed simply to exposure to more data,

regardless of the domain. In this setting, for NEWS, we use a CS LM; for REVIEWS, a BIOMED LM; for CS, a NEWS LM; for BIOMED, a REVIEWS LM. We use the vocabulary overlap statistics in Figure [2](#page-2-1) to guide these choices.

Our results are shown in Table [3,](#page-3-1) where the last column (¬DAPT) corresponds to this setting. For each task, DAPT significantly outperforms adapting to an irrelevant domain, suggesting the importance of pretraining on domain-relevant data. Furthermore, we generally observe that ¬DAPT results in worse performance than even ROBERTA on end-tasks. Taken together, these results indicate that in most settings, exposure to more data without considering domain relevance is detrimental to end-task performance. However, there are two tasks (SCIERC and ACL-ARC) in which ¬DAPT marginally *improves* performance over ROBERTA. This may suggest that in some cases, continued pretraining on any additional data is useful, as noted in [Baevski et al.](#page-8-0) [\(2019\)](#page-8-0).

#### 3.4 Domain Overlap

Our analysis of DAPT is based on prior intuitions about how task data is assigned to specific domains. For instance, to perform DAPT for HELPFULNESS, we only adapt to AMAZON reviews, but not to any REALNEWS articles. However, the gradations in Figure [2](#page-2-1) suggest that the boundaries between domains are in some sense fuzzy; for example, 40% of unigrams are shared between REVIEWS and NEWS. As further indication of this overlap, we also qualitatively identify documents that overlap cross-domain: in Table [4,](#page-4-1) we showcase reviews and REALNEWS articles that are similar to these reviews (other examples can be found in Appendix §[D\)](#page-14-1). In fact, we find that adapting ROBERTA to

<span id="page-4-1"></span>

| IMDB review                                                                                                                                                                                                                                                                                                                                                                                                                              | REALNEWS article                                                                                                                                                                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "The Shop Around the Corner" is one of the great films from director                                                                                                                                                                                                                                                                                                                                                                     | [] Three great festive films The Shop Around                                                                                                                                                                                                            |
| Ernst Lubitsch. In addition to the talents of James Stewart and Margaret Sullavan, it's filled with a terrific cast of top character actors such as Frank Morgan and Felix Bressart. [] The makers of "You've Got Mail" claim their film to be a remake, but that's just nothing but a lot of inflated self praise. Anyway, if you have an affection for romantic comedies of the 1940's, you'll find "The Shop Around the Corner" to be | the Corner (1940) Delightful Comedy by Ernst<br>Lubitsch stars James Stewart and Margaret Sulla-<br>van falling in love at Christmas. Remade as<br>You've Got Mail. []                                                                                  |
| nothing short of wonderful. Just as good with repeat viewings.                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                                                                                         |
| HELPFULNESS review                                                                                                                                                                                                                                                                                                                                                                                                                       | REALNEWS article                                                                                                                                                                                                                                        |
| Simply the Best! I've owned countless Droids and iPhones, but this one destroys them all. Samsung really nailed it with this one, extremely fast, very pocketable, gorgeous display, exceptional battery life, good audio quality, perfect GPS & WiFi performance, transparent status bar, battery percentage, ability to turn off soft key lights, superb camera for a smartphone and more! []                                          | We're living in a world with a new Samsung. [] more on battery life later [] Exposure is usually spot on and focusing is very fast. [] The design, display, camera and performance are all best in class, and the phone feels smaller than it looks. [] |

Table 4: Examples that illustrate how some domains might have overlaps with others, leading to unexpected positive transfer. We highlight expressions in the reviews that are also found in the REALNEWS articles.

NEWS not as harmful to its performance on RE-VIEWS tasks (DAPT on NEWS achieves  $65.5_{2.3}$  on Helpfulness and  $95.0_{0.1}$  on IMDB).

Although this analysis is by no means comprehensive, it indicates that the factors that give rise to observable domain differences are likely not mutually exclusive. It is possible that pretraining beyond conventional domain boundaries could result in more effective DAPT; we leave this investigation to future work. In general, the provenance of data, including the processes by which corpora are curated, must be kept in mind when designing pretraining procedures and creating new benchmarks that test out-of-domain generalization abilities.

#### <span id="page-4-0"></span>4 Task-Adaptive Pretraining

Datasets curated to capture specific tasks of interest tend to cover only a subset of the text available within the broader domain. For example, the CHEMPROT dataset for extracting relations between chemicals and proteins focuses on abstracts of recently-published, high-impact articles from hand-selected PubMed categories (Krallinger et al., 2017, 2015). We hypothesize that such cases where the task data is a narrowly-defined subset of the broader domain, pretraining on the task dataset itself or data relevant to the task may be helpful.

Task-adaptive pretraining (TAPT) refers to pretraining on the unlabeled training set for a given task; prior work has shown its effectiveness (e.g. Howard and Ruder, 2018). Compared to domainadaptive pretraining (DAPT; §3), the task-adaptive approach strikes a different trade-off: it uses a far smaller pretraining corpus, but one that is much more task-relevant (under the assumption that the training set represents aspects of the task well). This makes TAPT much less expensive to run than DAPT, and as we show in our experiments, the performance of TAPT is often competitive with that of DAPT.

#### 4.1 Experiments

Similar to DAPT, task-adaptive pretraining consists of a second phase of pretraining ROBERTA, but only on the available task-specific training data. In contrast to DAPT, which we train for 12.5K steps, we perform TAPT for 100 epochs. We artificially augment each dataset by randomly masking different words (using the masking probability of 0.15) across epochs. As in our DAPT experiments, we pass the final layer [CLS] token representation to a task-specific feedforward layer for classification (see Table 14 in Appendix for more hyperparameter details).

Our results are shown in the TAPT column of Table 5. TAPT consistently improves the ROBERTA baseline for all tasks across domains. Even on the news domain, which was part of ROBERTA pretraining corpus, TAPT improves over ROBERTA, showcasing the advantage of task adaptation. Particularly remarkable are the relative differences between TAPT and DAPT. DAPT is more resource intensive (see Table 9 in §5.3), but TAPT manages to match its performance in some of the tasks, such as SCIERC. In RCT, HYPERPARTISAN, AGNEWS, HELPFULNESS, and IMDB, the results even exceed those of DAPT, highlighting the efficacy of this cheaper adaptation technique.

<span id="page-5-1"></span>

|         |               |         |         |         | Additional Pretraining Phases |
|---------|---------------|---------|---------|---------|-------------------------------|
| Domain  | Task          | ROBERTA | DAPT    | TAPT    | DAPT + TAPT                   |
|         | CHEMPROT      | 81.91.0 | 84.20.2 | 82.60.4 | 84.40.4                       |
| BIOMED  | †RCT          | 87.20.1 | 87.60.1 | 87.70.1 | 87.80.1                       |
|         | ACL-ARC       | 63.05.8 | 75.42.5 | 67.41.8 | 75.63.8                       |
| CS      | SCIERC        | 77.31.9 | 80.81.5 | 79.31.5 | 81.31.8                       |
|         | HYPERPARTISAN | 86.60.9 | 88.25.9 | 90.45.2 | 90.06.6                       |
| NEWS    | †AGNEWS       | 93.90.2 | 93.90.2 | 94.50.1 | 94.60.1                       |
|         | †HELPFULNESS  | 65.13.4 | 66.51.4 | 68.51.9 | 68.71.8                       |
| REVIEWS | †<br>IMDB     | 95.00.2 | 95.40.1 | 95.50.1 | 95.60.1                       |

Table 5: Results on different phases of adaptive pretraining compared to the baseline ROBERTA (col. 1). Our approaches are DAPT (col. 2, §[3\)](#page-1-1), TAPT (col. 3, §[4\)](#page-4-0), and a combination of both (col. 4). Reported results follow the same format as Table [3.](#page-3-1) State-of-the-art results we can compare to: CHEMPROT (84.6), RCT (92.9), ACL-ARC (71.0), SCIERC (81.8), HYPERPARTISAN (94.8), AGNEWS (95.5), IMDB (96.2); references in §[A.2.](#page-12-2)

<span id="page-5-3"></span>

| BIOMED                | RCT                          | CHEMPROT                     |
|-----------------------|------------------------------|------------------------------|
| TAPT<br>Transfer-TAPT | 87.70.1<br>(↓0.6)<br>87.10.4 | 82.60.5<br>80.40.6<br>(↓2.2) |
|                       |                              |                              |
| NEWS                  | HYPERPARTISAN                | AGNEWS                       |

| CS                    | ACL-ARC                      | SCIERC                       |
|-----------------------|------------------------------|------------------------------|
| TAPT<br>Transfer-TAPT | 67.41.8<br>(↓3.3)<br>64.12.7 | 79.31.5<br>79.12.5<br>(↓0.2) |
|                       |                              |                              |
| REVIEWS               | HELPFULNESS                  | IMDB                         |

Table 6: Though TAPT is effective (Table [5\)](#page-5-1), it is harmful when applied *across* tasks. These findings illustrate differences in task distributions within a domain.

Combined DAPT and TAPT We investigate the effect of using both adaptation techniques together. We begin with ROBERTA and apply DAPT then TAPT under this setting. The three phases of pretraining add up to make this the most computationally expensive of all our settings (see Table [9\)](#page-7-0). As expected, combined domain- and task-adaptive pretraining achieves the best performance on all tasks (Table [5\)](#page-5-1).[2](#page-5-2)

Overall, our results show that DAPT followed by TAPT achieves the best of both worlds of domain and task awareness, yielding the best performance. While we speculate that TAPT followed by DAPT would be susceptible to catastrophic forgetting of the task-relevant corpus [\(Yogatama et al.,](#page-11-4) [2019\)](#page-11-4), alternate methods of combining the procedures may result in better downstream performance. Future work may explore pretraining with a more sophisticated curriculum of domain and task distributions.

Cross-Task Transfer We complete the comparison between DAPT and TAPT by exploring whether adapting to one task transfers to other tasks in the same domain. For instance, we further pretrain the LM using the RCT unlabeled data, fine-tune it with the CHEMPROT labeled data, and observe the effect. We refer to this setting as Transfer-TAPT. Our results for tasks in all four domains are shown in Table [6.](#page-5-3) We see that TAPT optimizes for single task performance, to the detriment of cross-task transfer. These results demonstrate that data distributions of tasks within a given domain might differ. Further, this could also explain why adapting only to a broad domain is not sufficient, and why TAPT after DAPT is effective.

## <span id="page-5-0"></span>5 Augmenting Training Data for Task-Adaptive Pretraining

In §[4,](#page-4-0) we continued pretraining the LM for task adaptation using only the training data for a supervised task. Inspired by the success of TAPT, we next investigate another setting where a larger pool of unlabeled data from the task distribution exists,

<span id="page-5-2"></span><sup>2</sup>Results on HYPERPARTISAN match those of TAPT, within a standard deviation arising from the five seeds.

<span id="page-6-2"></span>

| Pretraining         | BIOMED  | NEWS    | REVIEWS |
|---------------------|---------|---------|---------|
|                     | RCT-500 | HYP.    | IMDB †  |
| TAPT                | 79.81.4 | 90.45.2 | 95.50.1 |
| DAPT + TAPT         | 83.00.3 | 90.06.6 | 95.60.1 |
| Curated-TAPT        | 83.40.3 | 89.99.5 | 95.70.1 |
| DAPT + Curated-TAPT | 83.80.5 | 92.13.6 | 95.80.1 |

Table 7: Mean test set macro-F<sup>1</sup> (for HYP. and IMDB) and micro-F<sup>1</sup> (for RCT-500), with Curated-TAPT across five random seeds, with standard deviations as subscripts. † indicates high-resource settings.

typically curated by humans.

We explore two scenarios. First, for three tasks (RCT, HYPERPARTISAN, and IMDB) we use this larger pool of unlabeled data from an available human-curated corpus (§[5.1\)](#page-6-0). Next, we explore *retrieving* related unlabeled data for TAPT, from a large unlabeled in-domain corpus, for tasks where extra human-curated data is unavailable (§[5.2\)](#page-6-1).

#### <span id="page-6-0"></span>5.1 Human Curated-TAPT

Dataset creation often involves collection of a large unlabeled corpus from known sources. This corpus is then downsampled to collect annotations, based on the annotation budget. The larger unlabeled corpus is thus expected to have a similar distribution to the task's training data. Moreover, it is usually available. We explore the role of such corpora in task-adaptive pretraining.

Data We simulate a low-resource setting RCT-500, by downsampling the training data of the RCT dataset to 500 examples (out of 180K available), and treat the rest of the training data as unlabeled. The HYPERPARTISAN shared task [\(Kiesel et al.,](#page-9-7) [2019\)](#page-9-7) has two tracks: low- and high-resource. We use 5K documents from the high-resource setting as Curated-TAPT unlabeled data and the original lowresource training documents for task fine-tuning. For IMDB, we use the extra unlabeled data manually curated by task annotators, drawn from the same distribution as the labeled data [\(Maas et al.,](#page-10-9) [2011\)](#page-10-9).

Results We compare Curated-TAPT to TAPT and DAPT + TAPT in Table [7.](#page-6-2) Curated-TAPT further improves our prior results from §[4](#page-4-0) across all three datasets. Applying Curated-TAPT after adapting to the domain results in the largest boost in performance on all tasks; in HYPERPARTISAN, DAPT + Curated-TAPT is within standard deviation of Curated-TAPT. Moreover, curated-TAPT achieves

<span id="page-6-3"></span>![](_page_6_Figure_8.jpeg)

Figure 3: An illustration of automated data selection (§[5.2\)](#page-6-1). We map unlabeled CHEMPROT and 1M BIOMED sentences to a shared vector space using the VAMPIRE model trained on these sentences. Then, for each CHEMPROT sentence, we identify k nearest neighbors, from the BIOMED domain.

<span id="page-6-4"></span>

|             | BIOMED   |         | CS      |
|-------------|----------|---------|---------|
| Pretraining | CHEMPROT | RCT-500 | ACL-ARC |
| ROBERTA     | 81.91.0  | 79.30.6 | 63.05.8 |
| TAPT        | 82.60.4  | 79.81.4 | 67.41.8 |
| RAND-TAPT   | 81.90.6  | 80.60.4 | 69.73.4 |
| 50NN-TAPT   | 83.30.7  | 80.80.6 | 70.72.8 |
| 150NN-TAPT  | 83.20.6  | 81.20.8 | 73.32.7 |
| 500NN-TAPT  | 83.30.7  | 81.70.4 | 75.51.9 |
| DAPT        | 84.20.2  | 82.50.5 | 75.42.5 |

Table 8: Mean test set micro-F<sup>1</sup> (for CHEMPROT and RCT) and macro-F<sup>1</sup> (for ACL-ARC), across five random seeds, with standard deviations as subscripts, comparing RAND-TAPT (with 50 candidates) and kNN-TAPT selection. Neighbors of the task data are selected from the domain data.

95% of the performance of DAPT + TAPT with the fully labeled RCT corpus (Table [5\)](#page-5-1) with only 0.3% of the labeled data. These results suggest that curating large amounts of data from the task distribution is extremely beneficial to end-task performance. We recommend that task designers release a large pool of unlabeled task data for their tasks to aid model adaptation through pretraining.

### <span id="page-6-1"></span>5.2 Automated Data Selection for TAPT

Consider a low-resource scenario without access to large amounts of unlabeled data to adequately benefit from TAPT, as well as absence of computational resources necessary for DAPT (see Table [9](#page-7-0) for details of computational requirements for different pretraining phases). We propose simple unsupervised methods to retrieve unlabeled text that aligns with the task distribution, from a large in-domain corpus. Our approach finds task-relevant data from the domain by embedding text from both the task and domain in a shared space, then selects candidates from the domain based on queries using the task data. Importantly, the embedding method must be lightweight enough to embed possibly millions of sentences in a reasonable time.

Given these constraints, we employ VAMPIRE [\(Gururangan et al.,](#page-9-11) [2019;](#page-9-11) Figure [3\)](#page-6-3), a lightweight bag-of-words language model. We pretrain VAM-PIRE on a large deduplicated[3](#page-7-2) sample of the domain (1M sentences) to obtain embeddings of the text from both the task and domain sample. We then select k candidates of each task sentence from the domain sample, in embeddings space. Candidates are selected (i) via nearest neighbors selection (kNN-TAPT) [4](#page-7-3) , or (ii) randomly (RAND-TAPT). We continue pretraining ROBERTA on this augmented corpus with both the task data (as in TAPT) as well as the selected candidate pool.

Results Results in Table [8](#page-6-4) show that kNN-TAPT outperforms TAPT for all cases. RAND-TAPT is generally worse than kNN-TAPT, but within a standard deviation arising from 5 seeds for RCT and ACL-ARC. As we increase k, kNN-TAPT performance steadily increases, and approaches that of DAPT. Appendix [F](#page-14-2) shows examples of nearest neighbors of task data. Future work might consider a closer study of kNN-TAPT, more sophisticated data selection methods, and the tradeoff between the diversity and task relevance of selected examples.

#### <span id="page-7-1"></span>5.3 Computational Requirements

The computational requirements for all our adaptation techniques on RCT-500 in the BIOMED domain in Table [9.](#page-7-0) TAPT is nearly 60 times faster to train than DAPT on a single v3-8 TPU and storage requirements for DAPT on this task are 5.8M times that of TAPT. Our best setting of DAPT + TAPT amounts to three phases of pretraining, and at first glance appears to be very expensive. However, once the LM has been adapted to a broad domain, it can be reused for multiple tasks within that domain, with only a single additional TAPT phase per task. While Curated-TAPT tends to achieve the best cost-

<span id="page-7-0"></span>

| Pretraining                                                           | Steps                                         | Docs.                                    | Storage                                    | F1                                                             |
|-----------------------------------------------------------------------|-----------------------------------------------|------------------------------------------|--------------------------------------------|----------------------------------------------------------------|
| ROBERTA                                                               | -                                             | -                                        | -                                          | 79.30.6                                                        |
| TAPT<br>50NN-TAPT<br>150NN-TAPT<br>500NN-TAPT<br>Curated-TAPT<br>DAPT | 0.2K<br>1.1K<br>3.2K<br>9.0K<br>8.8K<br>12.5K | 500<br>24K<br>66K<br>185K<br>180K<br>25M | 80KB<br>3MB<br>8MB<br>24MB<br>27MB<br>47GB | 79.81.4<br>80.80.6<br>81.20.8<br>81.70.4<br>83.40.3<br>82.50.5 |
| DAPT + TAPT                                                           | 12.6K                                         | 25M                                      | 47GB                                       | 83.00.3                                                        |

Table 9: Computational requirements for adapting to the RCT-500 task, comparing DAPT (§[3\)](#page-1-1) and the various TAPT modifications described in §[4](#page-4-0) and §[5.](#page-5-0)

benefit ratio in this comparison, one must also take into account the cost of curating large in-domain data. Automatic methods such as kNN-TAPT are much cheaper than DAPT.

### <span id="page-7-5"></span>6 Related Work

Transfer learning for domain adaptation Prior work has shown the benefit of continued pretraining in domain [\(Alsentzer et al.,](#page-8-1) [2019;](#page-8-1) [Chakrabarty et al.,](#page-9-13) [2019;](#page-9-13) [Lee et al.,](#page-10-4) [2019\)](#page-10-4).[5](#page-7-4) We have contributed further investigation of the effects of a shift between a large, diverse pretraining corpus and target domain on task performance. Other studies (e.g., [Huang et al.,](#page-9-14) [2019\)](#page-9-14) have trained language models (LMs) in their domain of interest, from scratch. In contrast, our work explores multiple domains, and is arguably more cost effective, since we continue pretraining an already powerful LM.

Task-adaptive pretraining Continued pretraining of a LM on the unlabeled data of a given task (TAPT) has been show to be beneficial for endtask performance (e.g. in [Howard and Ruder,](#page-9-0) [2018;](#page-9-0) [Phang et al.,](#page-10-10) [2018;](#page-10-10) [Sun et al.,](#page-10-11) [2019\)](#page-10-11). In the presence of *domain shift* between train and test data distributions of the same task, domain-adaptive pretraining (DAPT) is sometimes used to describe what we term TAPT [\(Logeswaran et al.,](#page-10-12) [2019;](#page-10-12) [Han and](#page-9-15) [Eisenstein,](#page-9-15) [2019\)](#page-9-15). Related approaches include language modeling as an auxiliary objective to task classifier fine-tuning [\(Chronopoulou et al.,](#page-9-16) [2019;](#page-9-16) [Radford et al.,](#page-10-13) [2018\)](#page-10-13) or consider simple syntactic structure of the input while adapting to task-specific

<span id="page-7-2"></span><sup>3</sup>We deduplicated this set to limit computation, since different sentences can share neighbors.

<span id="page-7-3"></span><sup>4</sup>We use a flat search index with cosine similarity between embeddings with the FAISS [\(Johnson et al.,](#page-9-12) [2019\)](#page-9-12) library.

<span id="page-7-4"></span><sup>5</sup> In contrast, [Peters et al.](#page-10-14) [\(2019\)](#page-10-14) find that the Jensen-Shannon divergence on term distributions between BERT's pretraining corpora and each MULTINLI domain [\(Williams](#page-11-5) [et al.,](#page-11-5) [2018\)](#page-11-5) does not predict its performance, though this might be an isolated finding specific to the MultiNLI dataset.

<span id="page-8-3"></span>

|              | Training Data         |                     |                   |  |
|--------------|-----------------------|---------------------|-------------------|--|
|              | Domain<br>(Unlabeled) | Task<br>(Unlabeled) | Task<br>(Labeled) |  |
| Roberta      |                       |                     | <b>√</b>          |  |
| DAPT         | $\checkmark$          |                     | $\checkmark$      |  |
| TAPT         |                       | $\checkmark$        | $\checkmark$      |  |
| DAPT + TAPT  | $\checkmark$          | $\checkmark$        | $\checkmark$      |  |
| knn-tapt     | (Subset)              | $\checkmark$        | $\checkmark$      |  |
| Curated-TAPT |                       | (Extra)             | $\checkmark$      |  |

Table 10: Summary of strategies for multi-phase pretraining explored in this paper.

data (Swayamdipta et al., 2019). We compare DAPT and TAPT as well as their interplay with respect to dataset size for continued pretraining (hence, expense of more rounds of pretraining), relevance to a data sample of a given task, and transferability to other tasks and datasets. See Table 11 in Appendix §A for a summary of multi-phase pretraining strategies from related work.

**Data selection for transfer learning** Selecting data for transfer learning has been explored in NLP (Moore and Lewis, 2010; Ruder and Plank, 2017; Zhang et al., 2019, among others). Dai et al. (2019) focus on identifying the most suitable corpus to pretrain a LM from scratch, for a single task: NER, whereas we select relevant examples for various tasks in §5.2. Concurrent to our work, Aharoni and Goldberg (2020) propose data selection methods for NMT based on cosine similarity in embedding space, using DISTILBERT (Sanh et al., 2019) for efficiency. In contrast, we use VAMPIRE, and focus on augmenting TAPT data for text classification tasks. Khandelwal et al. (2020) introduced kNN-LMs that allows easy domain adaptation of pretrained LMs by simply adding a datastore per domain and no further training; an alternative to integrate domain information in an LM. Our study of human-curated data §5.1 is related to *focused* crawling (Chakrabarti et al., 1999) for collection of suitable data, especially with LM reliance (Remus and Biemann, 2016).

What is a domain? Despite the popularity of domain adaptation techniques, most research and practice seems to use an intuitive understanding of domains. A small body of work has attempted to address this question (Lee, 2001; Eisenstein et al., 2014; van der Wees et al., 2015; Plank, 2016; Ruder et al., 2016, among others). For instance, Aharoni and Goldberg (2020) define domains by implicit

clusters of sentence representations in pretrained LMs. Our results show that DAPT and TAPT complement each other, which suggests a spectra of domains defined around tasks at various levels of granularity (e.g., Amazon reviews for a specific product, all Amazon reviews, all reviews on the web, the web).

### 7 Conclusion

We investigate several variations for adapting pretrained LMs to domains and tasks within those domains, summarized in Table 10. Our experiments reveal that even a model of hundreds of millions of parameters struggles to encode the complexity of a single textual domain, let alone all of language. We show that pretraining the model towards a specific task or small corpus can provide significant benefits. Our findings suggest it may be valuable to complement work on ever-larger LMs with parallel efforts to identify and use domain- and taskrelevant corpora to specialize models. While our results demonstrate how these approaches can improve Roberta, a powerful LM, the approaches we studied are general enough to be applied to any pretrained LM. Our work points to numerous future directions, such as better data selection for TAPT, efficient adaptation large pretrained language models to distant domains, and building reusable language models after adaptation.

#### **Acknowledgments**

The authors thank Dallas Card, Mark Neumann, Nelson Liu, Eric Wallace, members of the AllenNLP team, and anonymous reviewers for helpful feedback, and Arman Cohan for providing data. This research was supported in part by the Office of Naval Research under the MURI grant N00014-18-1-2670.

#### References

<span id="page-8-2"></span>Roee Aharoni and Yoav Goldberg. 2020. Unsupervised domain clusters in pretrained language models. In *ACL*. To appear.

<span id="page-8-1"></span>Emily Alsentzer, John Murphy, William Boag, Wei-Hung Weng, Di Jindi, Tristan Naumann, and Matthew McDermott. 2019. Publicly available clinical BERT embeddings. In *Proceedings of the 2nd Clinical Natural Language Processing Workshop*.

<span id="page-8-0"></span>Alexei Baevski, Sergey Edunov, Yinhan Liu, Luke Zettlemoyer, and Michael Auli. 2019. Cloze-driven pretraining of self-attention networks. In *EMNLP*.

- <span id="page-9-8"></span>Iz Beltagy, Kyle Lo, and Arman Cohan. 2019. [SciB-](https://www.aclweb.org/anthology/D19-1371)[ERT: A pretrained language model for scientific text.](https://www.aclweb.org/anthology/D19-1371) In *EMNLP*.
- <span id="page-9-3"></span>Iz Beltagy, Matthew E. Peters, and Arman Cohan. 2020. [Longformer: The long-document transformer.](https://arxiv.org/abs/2004.05150) arXiv:2004.05150.
- <span id="page-9-19"></span>Soumen Chakrabarti, Martin van den Berg, and Byron Dom. 1999. [Focused Crawling: A New Approach to](https://api.semanticscholar.org/CorpusID:206134284) [Topic-Specific Web Resource Discovery.](https://api.semanticscholar.org/CorpusID:206134284) *Comput. Networks*, 31:1623–1640.
- <span id="page-9-13"></span>Tuhin Chakrabarty, Christopher Hidey, and Kathy McKeown. 2019. [IMHO fine-tuning improves claim](https://www.aclweb.org/anthology/N19-1054/) [detection.](https://www.aclweb.org/anthology/N19-1054/) In *NAACL*.
- <span id="page-9-25"></span>Ciprian Chelba, Tomas Mikolov, Michael Schuster, Qi Ge, Thorsten Brants, Phillipp Koehn, and Tony Robinson. 2014. [One billion word benchmark for](https://arxiv.org/abs/1312.3005) [measuring progress in statistical language modeling.](https://arxiv.org/abs/1312.3005) In *INTERSPEECH*.
- <span id="page-9-16"></span>Alexandra Chronopoulou, Christos Baziotis, and Alexandros Potamianos. 2019. [An embarrassingly](https://www.aclweb.org/anthology/N19-1213/) [simple approach for transfer learning from pre](https://www.aclweb.org/anthology/N19-1213/)[trained language models.](https://www.aclweb.org/anthology/N19-1213/) In *NAACL*.
- <span id="page-9-22"></span>Arman Cohan, Iz Beltagy, Daniel King, Bhavana Dalvi, and Dan Weld. 2019. [Pretrained language models](https://www.aclweb.org/anthology/D19-1383) [for sequential sentence classification.](https://www.aclweb.org/anthology/D19-1383) In *EMNLP*.
- <span id="page-9-17"></span>Xiang Dai, Sarvnaz Karimi, Ben Hachey, and Cecile Paris. 2019. [Using similarity measures to select pre](https://www.aclweb.org/anthology/N19-1213)[training data for NER.](https://www.aclweb.org/anthology/N19-1213) In *NAACL*.
- <span id="page-9-5"></span>Franck Dernoncourt and Ji Young Lee. 2017. [Pubmed](https://www.aclweb.org/anthology/I17-2052/) [200k RCT: a dataset for sequential sentence classifi](https://www.aclweb.org/anthology/I17-2052/)[cation in medical abstracts.](https://www.aclweb.org/anthology/I17-2052/) In *IJCNLP*.
- <span id="page-9-1"></span>Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. [BERT: Pre-training of](https://www.aclweb.org/anthology/N19-1423) [deep bidirectional transformers for language under](https://www.aclweb.org/anthology/N19-1423)[standing.](https://www.aclweb.org/anthology/N19-1423) In *NAACL*.
- <span id="page-9-27"></span>Jesse Dodge, Suchin Gururangan, Dallas Card, Roy Schwartz, and Noah A Smith. 2019. [Show your](https://arxiv.org/abs/1909.03004) [work: Improved reporting of experimental results.](https://arxiv.org/abs/1909.03004) In *EMNLP*.
- <span id="page-9-20"></span>Jacob Eisenstein, Brendan O'connor, Noah A. Smith, and Eric P. Xing. 2014. [Diffusion of lexical change](https://arxiv.org/abs/1210.5268) [in social media.](https://arxiv.org/abs/1210.5268) *PloS ONE*.
- <span id="page-9-26"></span>Matt Gardner, Joel Grus, Mark Neumann, Oyvind Tafjord, Pradeep Dasigi, Nelson F. Liu, Matthew Peters, Michael Schmitz, and Luke Zettlemoyer. 2018. [AllenNLP: A deep semantic natural language pro](https://www.aclweb.org/anthology/W18-2501)[cessing platform.](https://www.aclweb.org/anthology/W18-2501) In *NLP-OSS*.
- <span id="page-9-21"></span>Aaron Gokaslan and Vanya Cohen. 2019. [OpenWeb-](http://Skylion007.github.io/OpenWebTextCorpus)[Text Corpus.](http://Skylion007.github.io/OpenWebTextCorpus)
- <span id="page-9-11"></span>Suchin Gururangan, Tam Dang, Dallas Card, and Noah A. Smith. 2019. [Variational pretraining for](https://www.aclweb.org/anthology/P19-1590) [semi-supervised text classification.](https://www.aclweb.org/anthology/P19-1590) In *ACL*.

- <span id="page-9-15"></span>Xiaochuang Han and Jacob Eisenstein. 2019. [Unsuper](https://www.aclweb.org/anthology/D19-1433)[vised domain adaptation of contextualized embed](https://www.aclweb.org/anthology/D19-1433)[dings for sequence labeling.](https://www.aclweb.org/anthology/D19-1433) In *EMNLP*.
- <span id="page-9-2"></span>Ruining He and Julian McAuley. 2016. [Ups and downs:](https://arxiv.org/abs/1602.01585) [Modeling the visual evolution of fashion trends with](https://arxiv.org/abs/1602.01585) [one-class collaborative filtering.](https://arxiv.org/abs/1602.01585) In *WWW*.
- <span id="page-9-23"></span>Matthew Honnibal and Ines Montani. 2017. [spaCy 2:](https://spacy.io/) [Natural language understanding with Bloom embed](https://spacy.io/)[dings, convolutional neural networks and incremen](https://spacy.io/)[tal parsing.](https://spacy.io/)
- <span id="page-9-0"></span>Jeremy Howard and Sebastian Ruder. 2018. [Universal](https://www.aclweb.org/anthology/P18-1031) [language model fine-tuning for text classification.](https://www.aclweb.org/anthology/P18-1031) In *ACL*.
- <span id="page-9-14"></span>Kexin Huang, Jaan Altosaar, and Rajesh Ranganath. 2019. [ClinicalBERT: Modeling clinical notes and](https://arxiv.org/abs/1904.05342) [predicting hospital readmission.](https://arxiv.org/abs/1904.05342) arXiv:1904.05342.
- <span id="page-9-12"></span>Jeff Johnson, Matthijs Douze, and Herve J ´ egou. 2019. ´ [Billion-scale similarity search with gpus.](https://arxiv.org/abs/1702.08734) *IEEE Transactions on Big Data*.
- <span id="page-9-6"></span>David Jurgens, Srijan Kumar, Raine Hoover, Daniel A. McFarland, and Dan Jurafsky. 2018. [Measuring the](https://www.aclweb.org/anthology/Q18-1028/) [evolution of a scientific field through citation frames.](https://www.aclweb.org/anthology/Q18-1028/) *TACL*.
- <span id="page-9-18"></span>Urvashi Khandelwal, Omer Levy, Dan Jurafsky, Luke Zettlemoyer, and Mike Lewis. 2020. [Generalization](https://arxiv.org/abs/1911.00172) [through memorization: Nearest neighbor language](https://arxiv.org/abs/1911.00172) [models.](https://arxiv.org/abs/1911.00172) In *ICLR*. To appear.
- <span id="page-9-7"></span>Johannes Kiesel, Maria Mestre, Rishabh Shukla, Emmanuel Vincent, Payam Adineh, David Corney, Benno Stein, and Martin Potthast. 2019. [SemEval-](https://www.aclweb.org/anthology/S19-2145/)[2019 Task 4: Hyperpartisan news detection.](https://www.aclweb.org/anthology/S19-2145/) In *SemEval*.
- <span id="page-9-24"></span>Diederik P Kingma and Jimmy Ba. 2015. [Adam: A](https://arxiv.org/abs/1412.6980) [method for stochastic optimization.](https://arxiv.org/abs/1412.6980) In *ICLR*.
- <span id="page-9-9"></span>Martin Krallinger, Obdulia Rabal, Saber Ahmad Akhondi, Mart´ın Perez P ´ erez, J ´ es´ us L ´ opez Santa- ´ mar´ıa, Gael Perez Rodr ´ ´ıguez, Georgios Tsatsaronis, Ander Intxaurrondo, Jose Antonio Baso L ´ opez, ´ Umesh Nandal, E. M. van Buel, A. Poorna Chandrasekhar, Marleen Rodenburg, Astrid Lægreid, Marius A. Doornenbal, Julen Oyarzabal, An ´ alia ´ Lourenc¸o, and Alfonso Valencia. 2017. [Overview of](https://pdfs.semanticscholar.org/eed7/81f498b563df5a9e8a241c67d63dd1d92ad5.pdf) [the biocreative vi chemical-protein interaction track.](https://pdfs.semanticscholar.org/eed7/81f498b563df5a9e8a241c67d63dd1d92ad5.pdf) In *Proceedings of the BioCreative VI Workshop*.
- <span id="page-9-10"></span>Martin Krallinger, Obdulia Rabal, Florian Leitner, Miguel Vazquez, David Salgado, Zhiyong Lu, Robert Leaman, Yanan Lu, Donghong Ji, Daniel M Lowe, et al. 2015. [The chemdner corpus of chemi](https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-7-S1-S2)[cals and drugs and its annotation principles.](https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-7-S1-S2) *Journal of cheminformatics*, 7(1):S2.
- <span id="page-9-4"></span>Jens Kringelum, Sonny Kim Kjærulff, Søren Brunak, Ole Lund, Tudor I. Oprea, and Olivier Taboureau. 2016. [ChemProt-3.0: a global chemical biology dis](https://www.ncbi.nlm.nih.gov/pubmed/26876982)[eases mapping.](https://www.ncbi.nlm.nih.gov/pubmed/26876982) In *Database*.

- <span id="page-10-20"></span>David YW Lee. 2001. [Genres, registers, text types, do](https://brill.com/view/book/edcoll/9789004334236/B9789004334236-s021.xml)[mains and styles: Clarifying the concepts and nav](https://brill.com/view/book/edcoll/9789004334236/B9789004334236-s021.xml)[igating a path through the BNC jungle.](https://brill.com/view/book/edcoll/9789004334236/B9789004334236-s021.xml) *Language Learning & Technology*.
- <span id="page-10-4"></span>Jinhyuk Lee, Wonjin Yoon, Sungdong Kim, Donghyeon Kim, Sunkyu Kim, Chan Ho So, and Jaewoo Kang. 2019. [BioBERT: A pre-trained](https://arxiv.org/abs/1901.08746) [biomedical language representation model for](https://arxiv.org/abs/1901.08746) [biomedical text mining.](https://arxiv.org/abs/1901.08746) *Bioinformatics*.
- <span id="page-10-1"></span>Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. [RoBERTa: A robustly optimized BERT pretraining](https://arxiv.org/abs/1907.11692) [approach.](https://arxiv.org/abs/1907.11692) arXiv:1907.11692.
- <span id="page-10-6"></span>Kyle Lo, Lucy Lu Wang, Mark Neumann, Rodney Kinney, and Daniel S. Weld. 2020. [S2ORC: The Se](https://arxiv.org/abs/1911.02782)[mantic Scholar Open Research Corpus.](https://arxiv.org/abs/1911.02782) In *ACL*. To appear.
- <span id="page-10-12"></span>Lajanugen Logeswaran, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, Jacob Devlin, and Honglak Lee. 2019. [Zero-shot entity linking by reading entity de](https://www.aclweb.org/anthology/P19-1335)[scriptions.](https://www.aclweb.org/anthology/P19-1335) In *ACL*.
- <span id="page-10-7"></span>Yi Luan, Luheng He, Mari Ostendorf, and Hannaneh Hajishirzi. 2018. [Multi-task identification of enti](https://www.aclweb.org/anthology/D18-1360/)[ties, relations, and coreference for scientific knowl](https://www.aclweb.org/anthology/D18-1360/)[edge graph construction.](https://www.aclweb.org/anthology/D18-1360/) In *EMNLP*.
- <span id="page-10-9"></span>Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. 2011. [Learning word vectors for sentiment analysis.](https://www.aclweb.org/anthology/P11-1015/) In *ACL*.
- <span id="page-10-8"></span>Julian McAuley, Christopher Targett, Qinfeng Shi, and Anton Van Den Hengel. 2015. [Image-based recom](https://arxiv.org/abs/1506.04757)[mendations on styles and substitutes.](https://arxiv.org/abs/1506.04757) In *ACM SI-GIR*.
- <span id="page-10-28"></span>Arindam Mitra, Pratyay Banerjee, Kuntal Kumar Pal, Swaroop Ranjan Mishra, and Chitta Baral. 2020. [Exploring ways to incorporate additional knowledge](https://arxiv.org/abs/1909.08855) [to improve natural language commonsense question](https://arxiv.org/abs/1909.08855) [answering.](https://arxiv.org/abs/1909.08855) arXiv:1909.08855v3.
- <span id="page-10-16"></span>Robert C. Moore and William Lewis. 2010. [Intelligent](https://www.aclweb.org/anthology/P10-2041/) [selection of language model training data.](https://www.aclweb.org/anthology/P10-2041/) In *ACL*.
- <span id="page-10-24"></span>Sebastian Nagel. 2016. [CC-NEWS.](http://commoncrawl.org/2016/10/news-dataset-available/)
- <span id="page-10-27"></span>Mark Neumann, Daniel King, Iz Beltagy, and Waleed Ammar. 2019. [Scispacy: Fast and robust models for](http://dx.doi.org/10.18653/v1/W19-5034) [biomedical natural language processing.](http://dx.doi.org/10.18653/v1/W19-5034) *Proceedings of the 18th BioNLP Workshop and Shared Task*.
- <span id="page-10-14"></span>Matthew E. Peters, Sebastian Ruder, and Noah A. Smith. 2019. [To tune or not to tune? Adapt](https://www.aclweb.org/anthology/W19-4302/)[ing pretrained representations to diverse tasks.](https://www.aclweb.org/anthology/W19-4302/) In *RepL4NLP*.
- <span id="page-10-10"></span>Jason Phang, Thibault Fevry, and Samuel R. Bow- ´ man. 2018. [Sentence encoders on STILTs: Supple](https://arxiv.org/abs/1811.01088)[mentary training on intermediate labeled-data tasks.](https://arxiv.org/abs/1811.01088) arXiv:1811.01088.

- <span id="page-10-22"></span>Barbara Plank. 2016. [What to do about non-standard](https://arxiv.org/abs/1608.07836) [\(or non-canonical\) language in NLP.](https://arxiv.org/abs/1608.07836) In *KONVENS*.
- <span id="page-10-13"></span>Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. 2018. [Improving language under](https://www.semanticscholar.org/paper/Improving-Language-Understanding-by-Generative-Radford/cd18800a0fe0b668a1cc19f2ec95b5003d0a5035)[standing by generative pre-training.](https://www.semanticscholar.org/paper/Improving-Language-Understanding-by-Generative-Radford/cd18800a0fe0b668a1cc19f2ec95b5003d0a5035)
- <span id="page-10-0"></span>Colin Raffel, Noam Shazeer, Adam Kaleo Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. 2019. [Ex](https://arxiv.org/abs/1910.10683)[ploring the limits of transfer learning with a unified](https://arxiv.org/abs/1910.10683) [text-to-text transformer.](https://arxiv.org/abs/1910.10683) arXiv:1910.10683.
- <span id="page-10-19"></span>Steffen Remus and Chris Biemann. 2016. [Domain-](https://www.aclweb.org/anthology/L16-1572)[Specific Corpus Expansion with Focused Webcrawl](https://www.aclweb.org/anthology/L16-1572)[ing.](https://www.aclweb.org/anthology/L16-1572) In *LREC*.
- <span id="page-10-23"></span>Sebastian Ruder, Parsa Ghaffari, and John G. Breslin. 2016. [Towards a continuous modeling of natural lan](https://www.aclweb.org/anthology/W16-6012/)[guage domains.](https://www.aclweb.org/anthology/W16-6012/) In *Workshop on Uphill Battles in Language Processing: Scaling Early Achievements to Robust Methods*.
- <span id="page-10-17"></span>Sebastian Ruder and Barbara Plank. 2017. [Learning to](https://www.aclweb.org/anthology/D17-1038/) [select data for transfer learning with Bayesian opti](https://www.aclweb.org/anthology/D17-1038/)[mization.](https://www.aclweb.org/anthology/D17-1038/) In *EMNLP*.
- <span id="page-10-18"></span>Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. 2019. [DistilBERT, a distilled version](https://arxiv.org/abs/1910.01108) [of BERT: smaller, faster, cheaper and lighter.](https://arxiv.org/abs/1910.01108) In *EMC2 @ NeurIPS*.
- <span id="page-10-11"></span>Chi Sun, Xipeng Qiu, Yige Xu, and Xuanjing Huang. 2019. [How to fine-tune BERT for text classification?](https://arxiv.org/abs/1905.05583) In *CCL*.
- <span id="page-10-15"></span>Swabha Swayamdipta, Matthew Peters, Brendan Roof, Chris Dyer, and Noah A Smith. 2019. [Shallow syn](https://arxiv.org/abs/1908.11047)[tax in deep water.](https://arxiv.org/abs/1908.11047) arXiv:1908.11047.
- <span id="page-10-26"></span>Tan Thongtan and Tanasanee Phienthrakul. 2019. [Sen](https://www.aclweb.org/anthology/P19-2057)[timent classification using document embeddings](https://www.aclweb.org/anthology/P19-2057) [trained with cosine similarity.](https://www.aclweb.org/anthology/P19-2057) In *ACL SRW*.
- <span id="page-10-25"></span>Trieu H. Trinh and Quoc V. Le. 2018. [A simple method](https://arxiv.org/abs/1806.02847) [for commonsense reasoning.](https://arxiv.org/abs/1806.02847) arXiv:1806.02847.
- <span id="page-10-5"></span>Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. [Attention is all](https://arxiv.org/abs/1706.03762) [you need.](https://arxiv.org/abs/1706.03762) In *NeurIPS*.
- <span id="page-10-3"></span>Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel R. Bowman. 2019. [SuperGLUE:](https://arxiv.org/abs/1905.00537) [A stickier benchmark for general-purpose language](https://arxiv.org/abs/1905.00537) [understanding systems.](https://arxiv.org/abs/1905.00537) In *NeurIPS*.
- <span id="page-10-2"></span>Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel Bowman. 2018. [GLUE: A multi-task benchmark and analysis plat](https://www.aclweb.org/anthology/W18-5446)[form for natural language understanding.](https://www.aclweb.org/anthology/W18-5446) In *BlackboxNLP @ EMNLP*.
- <span id="page-10-21"></span>Marlies van der Wees, Arianna Bisazza, Wouter Weerkamp, and Christof Monz. 2015. [What's in a](https://www.aclweb.org/anthology/P15-2092/) [domain? Analyzing genre and topic differences in](https://www.aclweb.org/anthology/P15-2092/) [statistical machine translation.](https://www.aclweb.org/anthology/P15-2092/) In *ACL*.

- <span id="page-11-5"></span>Adina Williams, Nikita Nangia, and Samuel Bowman. 2018. [A broad-coverage challenge corpus for sen](https://www.aclweb.org/anthology/N18-1101/)[tence understanding through inference.](https://www.aclweb.org/anthology/N18-1101/) In *NAACL*.
- <span id="page-11-10"></span>Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Remi Louf, Morgan Funtow- ´ icz, and Jamie Brew. 2019. [HuggingFace's Trans](https://github.com/huggingface/transformers)[formers: State-of-the-art natural language process](https://github.com/huggingface/transformers)[ing.](https://github.com/huggingface/transformers) arXiv:1910.03771.
- <span id="page-11-1"></span>Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. 2016. [Google's neural machine](https://arxiv.org/abs/1609.08144) [translation system: Bridging the gap between human](https://arxiv.org/abs/1609.08144) [and machine translation.](https://arxiv.org/abs/1609.08144)
- <span id="page-11-8"></span>Hu Xu, Bing Liu, Lei Shu, and Philip Yu. 2019a. [BERT](https://www.aclweb.org/anthology/N19-1242) [post-training for review reading comprehension and](https://www.aclweb.org/anthology/N19-1242) [aspect-based sentiment analysis.](https://www.aclweb.org/anthology/N19-1242) In *NAACL*.
- <span id="page-11-9"></span>Hu Xu, Bing Liu, Lei Shu, and Philip S. Yu. 2019b. [Review conversational reading comprehen](https://arxiv.org/abs/1902.00821)[sion.](https://arxiv.org/abs/1902.00821) arXiv:1902.00821v2.
- <span id="page-11-0"></span>Zhilin Yang, Zihang Dai, Yiming Yang, Jaime G. Carbonell, Ruslan Salakhutdinov, and Quoc V. Le. 2019. [XLNet: Generalized autoregressive pretraining for](https://arxiv.org/abs/1906.08237) [language understanding.](https://arxiv.org/abs/1906.08237) In *NeurIPS*.
- <span id="page-11-4"></span>Dani Yogatama, Cyprien de Masson d'Autume, Jerome Connor, Tomas Kocisk ´ y, Mike Chrzanowski, Ling- ´ peng Kong, Angeliki Lazaridou, Wang Ling, Lei Yu, Chris Dyer, and Phil Blunsom. 2019. [Learning and](https://arxiv.org/abs/1901.11373) [evaluating general linguistic intelligence.](https://arxiv.org/abs/1901.11373)
- <span id="page-11-2"></span>Rowan Zellers, Ari Holtzman, Hannah Rashkin, Yonatan Bisk, Ali Farhadi, Franziska Roesner, and Yejin Choi. 2019. [Defending against neural fake](https://arxiv.org/abs/1905.12616) [news.](https://arxiv.org/abs/1905.12616) In *NeurIPS*.
- <span id="page-11-3"></span>Xiang Zhang, Junbo Jake Zhao, and Yann LeCun. 2015. [Character-level convolutional networks for text clas](https://arxiv.org/abs/1509.01626)[sification.](https://arxiv.org/abs/1509.01626) In *NeurIPS*.
- <span id="page-11-6"></span>Xuan Zhang, Pamela Shapiro, Gaurav Kumar, Paul Mc-Namee, Marine Carpuat, and Kevin Duh. 2019. [Cur](https://arxiv.org/abs/1905.05816)[riculum learning for domain adaptation in neural ma](https://arxiv.org/abs/1905.05816)[chine translation.](https://arxiv.org/abs/1905.05816) In *NAACL*.
- <span id="page-11-7"></span>Yukun Zhu, Ryan Kiros, Richard S. Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, and Sanja Fidler. 2015. [Aligning books and movies:](https://arxiv.org/abs/1506.06724) [Towards story-like visual explanations by watching](https://arxiv.org/abs/1506.06724) [movies and reading books.](https://arxiv.org/abs/1506.06724) In *ICCV*.

### Appendix Overview

In this supplementary material, we provide: (i) additional information for producing the results in the paper, and (ii) results that we could not fit into the main body of the paper.

Appendix [A.](#page-12-3) A tabular overview of related work described in Section §[6,](#page-7-5) a description of the corpus used to train ROBERTA in [Liu et al.](#page-10-1) [\(2019\)](#page-10-1), and references to the state of the art on our tasks.

Appendix [B.](#page-12-1) Details about the data preprocessing, training, and implementation of domain- and taskadaptive pretraining.

Appendix [C.](#page-13-0) Development set results.

Appendix [D.](#page-14-1) Examples of domain overlap.

Appendix [E.](#page-14-0) The cross-domain masked LM loss and reproducibility challenges.

Appendix [F.](#page-14-2) Illustration of our data selection method and examples of nearest neighbours.

### <span id="page-12-3"></span>A Related Work

Table [11](#page-13-1) shows which of the strategies for continued pretraining have already been explored in the prior work from the Related Work (§[6\)](#page-7-5). As evident from the table, our work compares various strategies as well as their interplay using a pretrained language model trained on a much more heterogeneous pretraining corpus.

#### <span id="page-12-0"></span>A.1 ROBERTA's Pretraining Corpus

ROBERTA was trained on data from BOOKCOR-PUS [\(Zhu et al.,](#page-11-7) [2015\)](#page-11-7),[6](#page-12-4) WIKIPEDIA, [7](#page-12-5) a portion of the CCNEWS dataset [\(Nagel,](#page-10-24) [2016\)](#page-10-24),[8](#page-12-6) OPENWEB-TEXT corpus of Web content extracted from URLs shared on Reddit [\(Gokaslan and Cohen,](#page-9-21) [2019\)](#page-9-21),[9](#page-12-7) and a subset of CommonCrawl that it is said to resemble the "story-like" style of WINOGRAD schemas (STORIES; [Trinh and Le,](#page-10-25) [2018\)](#page-10-25).[10](#page-12-8)

### <span id="page-12-2"></span>A.2 State of the Art

In this section, we specify the models achieving state of the art on our tasks. See the caption of Table [5](#page-5-1) for the reported performance of these models. For ACL-ARC, that is SCIBERT [\(Beltagy](#page-9-8) [et al.,](#page-9-8) [2019\)](#page-9-8), a BERT-base model for trained from scratch on scientific text. For CHEMPROT and SCI-ERC, that is S2ORC-BERT [\(Lo et al.,](#page-10-6) [2020\)](#page-10-6), a similar model to SCIBERT. For AGNEWS and IMDB, XLNet-large, a much larger model. For RCT, [Cohan et al.](#page-9-22) [\(2019\)](#page-9-22). For HYPERPARTISAN, LONGFORMER, a modified Transformer language model for long documents [\(Beltagy et al.,](#page-9-3) [2020\)](#page-9-3). [Thongtan and Phienthrakul](#page-10-26) [\(2019\)](#page-10-26) report a higher number (97.42) on IMDB, but they train their word vectors on the test set. Our baseline establishes the first benchmark for the HELPFULNESS dataset.

### <span id="page-12-1"></span>B Experimental Setup

Preprocessing for DAPT The unlabeled corpus in each domain was pre-processed prior to language model training. Abstracts and body paragraphs from biomedical and computer science articles were used after sentence splitting using scispaCy [\(Neumann et al.,](#page-10-27) [2019\)](#page-10-27). We used summaries and full text of each news article, and the entire body of review from Amazon reviews. For both news and reviews, we perform sentence splitting using spaCy [\(Honnibal and Montani,](#page-9-23) [2017\)](#page-9-23).

Training details for DAPT We train ROBERTA on each domain for 12.5K steps. We focused on matching all the domain dataset sizes (see Table [1\)](#page-2-0) such that each domain is exposed to the same amount of data as for 12.5K steps it is trained for. AMAZON reviews contain more documents, but each is shorter. We used an effective batch size of 2048 through gradient accumulation, as recommended in [Liu et al.](#page-10-1) [\(2019\)](#page-10-1). See Table [13](#page-15-1) for more hyperparameter details.

Training details for TAPT We use the same pretraining hyperparameters as DAPT, but we artificially augmented each dataset for TAPT by randomly masking different tokens across epochs, using the masking probability of 0.15. Each dataset was trained for 100 epochs. For tasks with less than 5K examples, we used a batch size of 256 through gradient accumulation. See Table [13](#page-15-1) for more hyperparameter details.

Optimization We used the Adam optimizer [\(Kingma and Ba,](#page-9-24) [2015\)](#page-9-24), a linear learning rate scheduler with 6% warm-up, a maximum learning rate of 0.0005. When we used a batch size of 256, we

<span id="page-12-5"></span><span id="page-12-4"></span><sup>6</sup><https://github.com/soskek/bookcorpus> <sup>7</sup>[https://github.com/google-research/](https://github.com/google-research/bert) [bert](https://github.com/google-research/bert)

<span id="page-12-6"></span><sup>8</sup>[https://github.com/fhamborg/](https://github.com/fhamborg/news-please) [news-please](https://github.com/fhamborg/news-please)

<span id="page-12-7"></span><sup>9</sup>[https://github.com/jcpeterson/](https://github.com/jcpeterson/openwebtext) [openwebtext](https://github.com/jcpeterson/openwebtext)

<span id="page-12-8"></span><sup>10</sup>[https://github.com/tensorflow/models/](https://github.com/tensorflow/models/tree/master/research/lm_commonsense) [tree/master/research/lm\\_commonsense](https://github.com/tensorflow/models/tree/master/research/lm_commonsense)

<span id="page-13-1"></span>

|                             | DAPT Domains<br>(if applicable)                           | Tasks                                               | Model                            | DAPT | TAPT    | DAPT<br>+ TAPT | knn-     | Curated<br>TAPT |
|-----------------------------|-----------------------------------------------------------|-----------------------------------------------------|----------------------------------|------|---------|----------------|----------|-----------------|
| This Paper                  | biomedical & computer<br>science papers, news,<br>reviews | 8 classification tasks                              | ROBERTA                          | ✓    | ✓       | <b>√</b>       | <b>√</b> | <b>√</b>        |
| Aharoni and Goldberg (2020) | -                                                         | NMT                                                 | DISTILBERT +<br>Transformer NMT  | -    | -       | -              | similar  | -               |
| Alsentzer et al. (2019)     | clinical text                                             | NER, NLI,<br>de-identification                      | (BIO)BERT                        | ✓    | -       | -              | -        | -               |
| Chakrabarty et al. (2019)   | opinionated claims from<br>Reddit                         | claim detection                                     | ULMFiT                           | ✓    | ✓       | -              | -        | -               |
| Chronopoulou et al. (2019)  | -                                                         | 5 classification tasks                              | ULMF <sub>1</sub> T <sup>†</sup> | -    | similar | -              | -        | -               |
| Han and Eisenstein (2019)   | -                                                         | NER in historical texts                             | ELMo, BERT                       | -    | ✓       | -              | -        | -               |
| Howard and Ruder (2018)     | -                                                         | 6 classification tasks                              | ULMFiT                           | -    | ✓       | -              | -        | -               |
| Khandelwal et al. (2020)    | -                                                         | language modeling                                   | Transformer LM                   | -    | -       | -              | similar  | -               |
| Lee et al. (2019)           | biomedical papers                                         | NER, QA, relation extraction                        | BERT                             | ✓    | -       | -              | -        | -               |
| Logeswaran et al. (2019)    | -                                                         | zero-shot entity<br>linking in Wikia                | BERT                             | -    | ✓       | -              | -        | -               |
| Mitra et al. (2020)         | -                                                         | commonsense QA                                      | BERT                             | -    | ✓       | -              | -        | -               |
| Phang et al. (2018)         | -                                                         | GLUE tasks                                          | ELMo, BERT,<br>GPT               | -    | ✓       | -              | -        | -               |
| Radford et al. (2018)       | -                                                         | NLI, QA,<br>similarity,<br>classification           | GPT                              | -    | similar | -              | -        | -               |
| Sun et al. (2019)           | sentiment, question, topic                                | 7 classification tasks                              | BERT                             | ✓    | ✓       | -              | -        | -               |
| Swayamdipta et al. (2019)   | -                                                         | NER, parsing, classification                        | ELMo                             | -    | similar | -              | -        | -               |
| Xu et al. (2019a)           | reviews                                                   | RC, aspect extract.,<br>sentiment<br>classification | BERT                             | ✓    | ✓       | <b>√</b>       | -        | -               |
| Xu et al. (2019b)           | restaurant reviews,<br>laptop reviews                     | conversational RC                                   | BERT                             | ✓    | ✓       | -              | -        | -               |

Table 11: Overview of prior work across strategies for continued pre-training summarized in Table 10. ULMFIT is pretrained on English Wikipedia; ULMFIT $^{\dagger}$  on English tweets; ELMO on the 1BWORDBENCHMARK (newswire; Chelba et al., 2014); GPT on BOOKCORPUS; BERT on English Wikipedia and BOOKCORPUS. In comparison to these pretraining corpora, Roberta's pretraining corpus is substantially more diverse (see Appendix  $\S$ A.1).

used a maximum learning rate of 0.0001, as recommended in Liu et al. (2019). We observe a high variance in performance between random seeds when fine-tuning ROBERTA to HYPERPARTISAN, because the dataset is extremely small. To produce final results on this task, we discard and resample degenerate seeds. We display the full hyperparameter settings in Table 13.

**Implementation** Our LM implementation uses the HuggingFace transformers library (Wolf et al., 2019)<sup>11</sup> and PyTorch XLA for TPU compatibility.<sup>12</sup> Each adaptive pretraining exper-

iment was performed on a single v3-8 TPU from Google Cloud.  $^{13}$  For the text classification tasks, we used AllenNLP (Gardner et al., 2018). Following standard practice (Devlin et al., 2019) we pass the final layer [CLS] token representation to a task-specific feedforward layer for prediction.

#### <span id="page-13-0"></span>C Development Set Results

Adhering to the standards suggested by Dodge et al. (2019) for replication, we report our development set results in Tables 15, 17, and 18.

<span id="page-13-2"></span>IIhttps://github.com/huggingface/
transformers

<span id="page-13-3"></span><sup>12</sup>https://github.com/pytorch/xla

<span id="page-13-4"></span><sup>13</sup>http://github.com/allenai/tpu-pretrain

### <span id="page-14-1"></span>D Analysis of Domain Overlap

In Table [20](#page-17-0) we display additional examples that highlight the overlap between IMDB reviews and REALNEWS articles, relevant for analysis in §[3.1.](#page-1-4)

### <span id="page-14-0"></span>E Analysis of Cross-Domain Masked LM Loss

In Section §[3.2,](#page-2-2) we provide ROBERTA's masked LM loss before and after DAPT. We display crossdomain masked-LM loss in Table [12,](#page-15-2) where we evaluate masked LM loss on text samples in other domains after performing DAPT.

We observe that the cross-domain masked-LM loss mostly follows our intuition and insights from the paper, i.e. ROBERTA's pretraining corpus and NEWS are closer, and BIOMED to CS (relative to other domains). However, our analysis in §[3.1](#page-1-4) illustrates that REVIEWS and NEWS also have some similarities. This is supported with the loss of ROBERTA that is adapted to NEWS, calculated on a sample of REVIEWS. However, ROBERTA that is adapted to REVIEWS results in the highest loss for a NEWS sample. This is the case for all domains. One of the properties that distinguishes REVIEWS from all other domains is that its documents are significantly shorter. In general, we find that cross-DAPT masked-LM loss can in some cases be a noisy predictor of domain similarity.

### <span id="page-14-2"></span>F k-Nearest Neighbors Data Selection

In Table [21,](#page-18-0) we display nearest neighbor documents in the BIOMED domain identified by our selection method, on the RCT dataset.

<span id="page-15-2"></span>

|                       |                                            |                                      | Data Sample Unseen During DAPT       |                                      |                                      |                                      |
|-----------------------|--------------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|
|                       |                                            | PT                                   | BIOMED                               | CS                                   | NEWS                                 | REVIEWS                              |
| <br><br>DAPT<br> | ROBERTA<br>BIOMED<br>CS<br>NEWS<br>REVIEWS | 1.19<br>1.63<br>1.82<br>1.33<br>2.07 | 1.32<br>0.99<br>1.43<br>1.50<br>2.23 | 1.63<br>1.63<br>1.34<br>1.82<br>2.44 | 1.08<br>1.69<br>1.92<br>1.16<br>2.27 | 2.10<br>2.59<br>2.78<br>2.16<br>1.93 |

Table 12: ROBERTA's (row 1) and domain-adapted ROBERTA's (rows 2–5) masked LM loss on randomly sampled held-out documents from each domain (lower implies a better fit). PT denotes a sample from sources similar to ROBERTA's pretraining corpus. The lowest masked LM for each domain sample is boldfaced.

<span id="page-15-1"></span>

| Computing Infrastructure | Google Cloud v3-8 TPU                   |
|--------------------------|-----------------------------------------|
| Model implementations    | https://github.com/allenai/tpu_pretrain |

| Hyperparameter          | Assignment                              |
|-------------------------|-----------------------------------------|
| number of steps         | 100 epochs (TAPT) or 12.5K steps (DAPT) |
| batch size              | 256 or 2058                             |
| maximum learning rate   | 0.0001 or 0.0005                        |
| learning rate optimizer | Adam                                    |
| Adam epsilon            | 1e-6                                    |
| Adam beta weights       | 0.9, 0.98                               |
| learning rate scheduler | None or warmup linear                   |
| Weight decay            | 0.01                                    |
| Warmup proportion       | 0.06                                    |
| learning rate decay     | linear                                  |

Table 13: Hyperparameters for domain- and task- adaptive pretraining.

<span id="page-15-0"></span>

| Computing Infrastructure | Quadro RTX 8000 GPU                              |
|--------------------------|--------------------------------------------------|
| Model implementation     | https://github.com/allenai/dont-stop-pretraining |

| Hyperparameter           | Assignment |
|--------------------------|------------|
| number of epochs         | 3 or 10    |
| patience                 | 3          |
| batch size               | 16         |
| learning rate            | 2e-5       |
| dropout                  | 0.1        |
| feedforward layer        | 1          |
| feedforward nonlinearity | tanh       |
| classification layer     | 1          |
|                          |            |

Table 14: Hyperparameters for ROBERTA text classifier.

<span id="page-16-0"></span>

|         |                           |                    | Additional Pretraining Phases |                    |                    |
|---------|---------------------------|--------------------|-------------------------------|--------------------|--------------------|
| Domain  | Task                      | ROBERTA            | DAPT                          | TAPT               | DAPT + TAPT        |
| BIOMED  | CHEMPROT                  | 83.21.4            | 84.10.5                       | 83.00.6            | 84.10.5            |
|         | †RCT                      | 88.10.05           | 88.50.1                       | 88.30.1            | 88.50.1            |
| CS      | ACL-ARC                   | 71.32.8            | 73.21.5                       | 73.23.6            | 78.62.9            |
|         | SCIERC                    | 83.81.1            | 88.41.7                       | 85.90.8            | 88.01.3            |
| NEWS    | HYPERPARTISAN             | 84.01.5            | 79.13.5                       | 82.73.3            | 80.82.3            |
|         | †AGNEWS                   | 94.30.1            | 94.30.1                       | 94.70.1            | 94.90.1            |
| REVIEWS | †HELPFULNESS<br>†<br>IMDB | 65.53.4<br>94.80.1 | 66.51.4<br>95.30.1            | 69.22.4<br>95.40.1 | 69.42.1<br>95.70.2 |

Table 15: Results on different phases of adaptive pretraining compared to the baseline ROBERTA (col. 1). Our approaches are DAPT (col. 2, §[3\)](#page-1-1), TAPT (col. 3, §[4\)](#page-4-0), and a combination of both (col. 4). Reported results are development macro-F1, except for CHEMPROT and RCT, for which we report micro-F1, following [Beltagy et al.](#page-9-8) [\(2019\)](#page-9-8). We report averages across five random seeds, with standard deviations as subscripts. † indicates high-resource settings. Best task performance is boldfaced. State-of-the-art results we can compare to: CHEMPROT (84.6), RCT (92.9), ACL-ARC (71.0), SCIERC (81.8), HYPERPARTISAN (94.8), AGNEWS (95.5), IMDB (96.2); references in §[A.2.](#page-12-2)

| Dom. | Task                   | ROB.               | DAPT               | ¬DAPT              |
|------|------------------------|--------------------|--------------------|--------------------|
| BM   | CHEMPROT               | 83.21.4            | 84.10.5            | 80.90.5            |
|      | †RCT                   | 88.10.0            | 88.50.1            | 87.90.1            |
| CS   | ACL-ARC                | 71.32.8            | 73.21.5            | 68.15.4            |
|      | SCIERC                 | 83.81.1            | 88.41.7            | 83.90.9            |
| NEWS | HYP.                   | 84.01.5            | 79.13.5            | 71.64.6            |
|      | †AGNEWS                | 94.30.1            | 94.30.1            | 94.00.1            |
| REV. | †HELPFUL.<br>†<br>IMDB | 65.53.4<br>94.80.1 | 66.51.4<br>95.30.1 | 65.53.0<br>93.80.2 |

Table 16: Development comparison of ROBERTA (ROBA.) and DAPT to adaptation to an *irrelevant* domain (¬ DAPT). See §[3.3](#page-3-2) for our choice of irrelevant domains. Reported results follow the same format as Table [5.](#page-5-1)

<span id="page-16-1"></span>

| BIOMED        | RCT             | CHEMPROT        | CS             | ACL-ARC         | SCIERC          |
|---------------|-----------------|-----------------|----------------|-----------------|-----------------|
| TAPT          | 88.30.1         | 83.00.6         | TAPT           | 73.23.6         | 85.90.8         |
| Transfer-TAPT | 88.00.1 (↓ 0.3) | 81.10.5 (↓ 1.9) | Transfer-TAPT  | 74.04.5 (↑ 1.2) | 85.51.1 (↓ 0.4) |
| NEWS          | HYPERPARTISAN   | AGNEWS          | AMAZON reviews | HELPFULNESS     | IMDB            |
| TAPT          | 82.73.3         | 94.70.1         | TAPT           | 69.22.4         | 95.40.1         |
| Transfer-TAPT | 77.63.6 (↓ 5.1) | 94.40.1 (↓ 0.4) | Transfer-TAPT  | 65.42.7 (↓ 3.8) | 94.90.1 (↓ 0.5) |

Table 17: Development results for TAPT transferability.

<span id="page-16-2"></span>

| Pretraining         | BIOMED<br>RCT-500 | NEWS<br>HYPERPARTISAN | REVIEWS<br>†<br>IMDB |
|---------------------|-------------------|-----------------------|----------------------|
| TAPT                | 80.51.3           | 82.73.3               | 95.40.1              |
| DAPT + TAPT         | 83.90.3           | 80.82.3               | 95.70.2              |
| Curated-TAPT        | 84.40.3           | 84.91.9               | 95.80.1              |
| DAPT + Curated-TAPT | 84.50.3           | 83.13.7               | 96.00.1              |

Table 18: Mean development set macro-F<sup>1</sup> (for HYPERPARTISAN and IMDB) and micro-F<sup>1</sup> (for RCT-500), with Curated-TAPT across five random seeds, with standard deviations as subscripts. † indicates high-resource settings.

| Pretraining | BioN                | <b>I</b> ED                | CS                  |
|-------------|---------------------|----------------------------|---------------------|
|             | СнемРкот            | RCT-500                    | ACL-ARC             |
| Roberta     | 83.2 <sub>1.4</sub> | 80.3 <sub>0.5</sub>        | 71.3 <sub>2.8</sub> |
| TAPT        | $83.0_{0.6}$        | $80.5_{1.3}$               | $73.2_{3.6}$        |
| RAND-TAPT   | 83.3 <sub>0.5</sub> | 81.6 <sub>0.6</sub>        | 78.7 <sub>4.0</sub> |
| 50nn-tapt   | $83.3_{0.8}$        | $81.7_{0.5}$               | $70.1_{3.5}$        |
| 150nn-tapt  | $83.3_{0.9}$        | $81.9_{0.8}$               | $78.5_{2.2}$        |
| 500nn-tapt  | $84.5_{0.4}$        | $82.6_{0.4}$               | $77.4_{2.3}$        |
| DAPT        | 84.1 <sub>0.5</sub> | <b>83.5</b> <sub>0.8</sub> | 73.2 <sub>1.5</sub> |

Table 19: Mean development set macro- $F_1$  (for HYP. and IMDB) and micro- $F_1$  (for RCT), across five random seeds, with standard deviations as subscripts, comparing RAND-TAPT (with 50 candidates) and kNN-TAPT selection. Neighbors of the task data are selected from the domain data.

#### <span id="page-17-0"></span>IMDB review REALNEWS article

Spooks is enjoyable trash, featuring some well directed sequences, ridiculous plots and dialogue, and some third rate acting. Many have described this is a UK version of "24", and one can see the similarities. The American version shares the weak silly plots, but the execution is so much slicker, sexier and I suspect, expensive. Some people describe weak comedy as "gentle comedy". This is gentle spy story hour, the exact opposite of anything created by John Le Carre. Give me Smiley any day.

The Sopranos is perhaps the most mind-opening series you could possibly ever want to watch. It's smart, it's quirky, it's funny - and it carries the mafia genre so well that most people can't resist watching. The best aspect of this show is the overwhelming realism of the characters, set in the subterranean world of the New York crime families. For most of the time, you really don't know whether the wise guys will stab someone in the back, or buy them lunch. Further adding to the realistic approach of the characters in this show is the depth of their personalities - These are dangerous men, most of them murderers, but by God if you don't love them too. I've laughed at their wisecracks, been torn when they've made err in judgement, and felt scared at the sheer ruthlessness of a serious criminal. [...]

The Wicker Man, starring Nicolas Cage, is by no means a good movie, but I can't really say it's one I regret watching. I could go on and on about the negative aspects of the movie, like the terrible acting and the lengthy scenes where Cage is looking for the girl, has a hallucination, followed by another hallucination, followed by a dream sequence- with a hallucination, etc., but it's just not worth dwelling on when it comes to a movie like this. Instead, here's five reasons why you SHOULD watch The Wicker Man, even though it's bad: 5. It's hard to deny that it has some genuinely creepy ideas to it, the only problem is in its cheesy, unintentionally funny execution. If nothing else, this is a movie that may inspire you to see the original 1973 film, or even read the short story on which it is based. 4. For a cheesy horror/thriller, it is really aesthetically pleasing. [...] NOTE: The Unrated version of the movie is the best to watch, and it's better to watch the Theatrical version just for its little added on epilogue, which features a cameo from James Franco.

Dr. Seuss would sure be mad right now if he was alive. Cat in the Hat proves to show how movie productions can take a classic story and turn it into a mindless pile of goop. We have Mike Myers as the infamous Cat in the Hat, big mistake! Myers proves he can't act in this film. He acts like a prissy show girl with a thousand tricks up his sleeve. The kids in this movie are all right, somewhere in between the lines of dull and annoying. The story is just like the original with a couple of tweaks and like most movies based on other stories, never tweak with the original story! Bringing in the evil neighbor Quin was a bad idea. He is a stupid villain that would never get anywhere in life. [...]

[...] Remember poor Helen Flynn from **Spooks**? In 2002, the headlong BBC spy caper was in such a hurry to establish the high-wire stakes of its morally compromised world that Lisa Faulkner's keen-as-mustard MI5 rookie turned out to be a lot more expendable than her prominent billing suggested. [...] Functioning as both a shocking twist and rather callous statement that No-One Is Safe, it gave the slick drama an instant patina of edginess while generating a record-breaking number of complaints.

The drumbeat regarding the "Breaking Bad" finale has led to the inevitable speculation on whether the final chapter in this serialized gem will live up to the hype or disappoint (thank you, "Dexter," for setting that bar pretty low), with debate, second-guessing and graduate-thesis-length analysis sure to follow. The Most Memorable TV Series Finales of All-Time [...] No ending in recent years has been more divisive than "The Sopranos" – for some, a brilliant flash (literally, in a way) of genius; for others (including yours truly), a too-cute copout, cryptically leaving its characters in perpetual limbo. The precedent to that would be "St. Elsewhere," which irked many with its provocative, surreal notion that the whole series was, in fact, conjured in the mind of an autistic child.

[...] What did you ultimately feel about "The Wicker Man" movie when all was said and done? [...] I'm a fan of the original and I'm glad that I made the movie because they don't make movies like that anymore and probably the result of what "Wicker Man" did is the reason why they don't make movies like that anymore. Again, it's kind of that '70's sensibility, but I'm trying to do things that are outside the box. Sometimes that means it'll work and other times it won't. Again though I'm going to try and learn from anything that I do. I think that it was a great cast, and Neil La Bute is one of the easiest directors that I've ever worked with. He really loves actors and he really gives you a relaxed feeling on the set, that you can achieve whatever it is that you're trying to put together, but at the end of the day the frustration that I had with 'The Wicker Man,' which I think has been remedied on the DVD because I believe the DVD has the directors original cut, is that they cut the horror out of the horror film to try and get a PG-13 rating. I mean, I don't know how to stop something like that. So I'm not happy with the way that the picture ended, but I'm happy with the spirit with which it was made. [...]

The Cat in the Hat, [...] Based on the book by Dr. Seuss [...] From the moment his tall, red-and-white-striped hat appears at their door, Sally and her brother know that the Cat in the Hat is the most mischievous cat they will ever meet. Suddenly the rainy afternoon is transformed by the Cat and his antics. Will their house ever be the same? Can the kids clean up before mom comes home? With some tricks (and a fish) and Thing Two and Thing One, with the Cat in The Hat, the fun's never done!Dr. Seuss is known worldwide as the imaginative master of children's literature. His books include a wonderful blend of invented and actual words, and his rhymes have helped many children and adults learn and better their understanding of the English language. [...]

Table 20: Additional examples that highlight the overlap between IMDB reviews and REALNEWS articles.

<span id="page-18-0"></span>

| Source     | During median follow-up of 905 days ( $IQR 773-1050$ ) , 49 people died and 987 unplanned admissions were recorded ( totalling 5530 days in hospital ) .                                   |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Neighbor 0 | Of this group, 26% died after discharge from hospital, and the median time to death was 11 days (interquartile range, 4.0-15.0 days) after discharge.                                      |
| Neighbor 1 | The median hospital stay was 17 days (range 8-26 days), and all the patients were discharged within 1 month.                                                                               |
| Neighbor 2 | The median hospital stay was 17 days (range 8-26 days).                                                                                                                                    |
| Neighbor 3 | The median time between discharge and death was 25 days (mean, 59.1 days) and no patient was alive after 193 days.                                                                         |
| Neighbor 4 | The length of hospital stay after colostomy formation ranged from 3 days to 14 days with a median duration of 6 days (+IQR of 4 to 8 days).                                                |
| Source     | Randomized, controlled, parallel clinical trial.                                                                                                                                           |
| Neighbor 0 | Design: Unblinded, randomised clinical controlled trial.                                                                                                                                   |
| Neighbor 1 | These studies and others led to the phase III randomized trial RTOG 0617/NCCTG 0628/ CALGB 30609.                                                                                          |
| Neighbor 2 | -Definitive randomized controlled clinical trial (RCT):                                                                                                                                    |
| Neighbor 3 | RCT $\frac{1}{4}$ randomized controlled trial.                                                                                                                                             |
| Neighbor 4 | randomized controlled trial [Fig. 3(A)].                                                                                                                                                   |
| Source     | Forty primary molar teeth in 40 healthy children aged 5-9 years were treated by direct pulp capping.                                                                                       |
| Neighbor 0 | In our study, we specifically determined the usefulness of the Er:YAG laser in caries removal and cavity preparation of primary and young permanent teeth in children ages 4 to 1 8 years. |
| Neighbor 1 | Males watched more TV than females, although it was only in primary school-aged children and on weekdays.                                                                                  |
| Neighbor 2 | Assent was obtained from children and adolescents aged 7-17 years.                                                                                                                         |
| Neighbor 3 | Cardiopulmonary resuscitation was not applied to children aged ;5 years (Table 2).                                                                                                         |
| Neighbor 4 | It measures HRQoL in children and adolescents aged 2 to 25 years.                                                                                                                          |

Table 21: 5 nearest neighbors of sentences from the RCT dataset (Source) in the BIOMED domain (Neighbors 0–4).