# CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data

Guillaume Wenzek<sup>∗</sup> , Marie-Anne Lachaux<sup>∗</sup> , Alexis Conneau, Vishrav Chaudhary, Francisco Guzmán, Armand Joulin, Edouard Grave Facebook AI

{guw, malachaux, aconneau, vishrav, fguzman, ajoulin, egrave}@fb.com

### Abstract

Pre-training text representations have led to significant improvements in many areas of natural language processing. The quality of these models benefits greatly from the size of the pretraining corpora as long as its quality is preserved. In this paper, we describe an automatic pipeline to extract massive high-quality monolingual datasets from Common Crawl for a variety of languages. Our pipeline follows the data processing introduced in fastText [\(Mikolov et al., 2017;](#page-6-0) [Grave et al.,](#page-5-0) [2018\)](#page-5-0), that deduplicates documents and identifies their language. We augment this pipeline with a filtering step to select documents that are close to high quality corpora like Wikipedia. Keywords: Common Crawl, web data

### 1. Introduction

Pre-trained text representations have brought significant performance gains on many natural language processing tasks [\(Peters et al., 2018\)](#page-6-1). Since the introduction of Transformers [\(Vaswani et al., 2017\)](#page-6-2) and BERT [\(Devlin et al., 2018\)](#page-5-1), we have a seen a steady improvement in the quality of these pre-trained models, mainly driven by increasing the size of the pretraining corpora [\(Radford et al., 2019;](#page-6-3) [Yang et al.,](#page-6-4) [2019;](#page-6-4) [Lan et al., 2019\)](#page-5-2). Nonetheless, the size only does not guarantee better models and the quality of the data has to be preserved, which has lead to the use of ad-hoc datasets created by concatenating existing high-quality data sources like Wikipedia. Unfortunately, such datasets cannot be replicated as easily for low-resources languages, as many have much smaller curated datasets such as Wikipedia.

In this paper, we present a data collection pipeline that allows to gather massive monolingual corpora of high quality in a variety of languages, including many low-resource ones. The principles of our pipeline are general and we show the results of its application to data collected by the Common Crawl project.[1](#page-0-0) Common Crawl is a massive non-curated dataset of webpages in many languages, mixed together in temporal snapshots of the web. Our pipeline performs standard document deduplication and language identification similar to [Grave et al. \(2018\)](#page-5-0), but differs in two ways: first, we preserve the document-level structure to allow for the training of paragraph-level representations like BERT [\(Devlin et al., 2018\)](#page-5-1) ; second, we add an optional monolingual filtering step that selects documents that are close to high quality sources, like Wikipedia. This is achieved by training a language model on the targeted sources and use the perplexity as a scoring function for documents. Our pipeline can be applied to any number of Common Crawl snapshots and takes 8.5 hours to process per snapshot on 5000 CPU cores. For example, the dataset obtained by preprocessing the February 2019 snapshot is composed of 1.5 billions documents in 174 languages. There are

This paper is organized as follows: we first present the Common Crawl corpora, followed by our overall pipeline to filter high quality documents from it. We then describe additional tools that can be used to tailor the filtering to a targeted corpora. Finally, we give in depth statistics about the dataset obtained from pre-processing a single Common Crawl snapshot. The pipeline and the tools are publicly available[2](#page-0-1) .

# 2. Related work

Preprocessing of massive datasets for training text representations has been developed in the context of word embeddings, such as word2vec [\(Mikolov et al., 2013\)](#page-6-5), GloVe [\(Pennington et al., 2014\)](#page-6-6) or fastText [\(Mikolov](#page-6-0) [et al., 2017\)](#page-6-0). In particular, our pipeline follows the fastText pipeline of [Grave et al. \(2018\)](#page-5-0) where Common Crawl is split into monolingual datasets using a language identifier based on fastText [\(Joulin et al.,](#page-5-3) [2016a\)](#page-5-3).

Common Crawl has been used in the context of language modeling to evaluate n-gram statistics [\(Buck](#page-5-4) [et al., 2014\)](#page-5-4). More recently, [Baevski et al. \(2019\)](#page-5-5) pretrained a BERT-like model on Common Crawl as preprocessed in [Grave et al. \(2018\)](#page-5-0). In general, progress in sentence representations has been observed by increasing the size of the pre-training corpora [\(Yang et](#page-6-4) [al., 2019;](#page-6-4) [Liu et al., 2019;](#page-6-7) [Raffel et al., 2019\)](#page-6-8). In particular, and concurrently to our work, [Raffel et al. \(2019\)](#page-6-8) used a large scale dataset based on Common Crawl to train text representations. Existing work using web based datasets have been using English specific preprocessing, such as keeping URLs shared on Reddit or using hand-crafted filtering rules. As opposed to these approaches, our pipeline can easily be applied to many languages other than English. Closer to this work, [Ortiz Suárez et al. \(2019\)](#page-6-9) has improved the pipeline of [Grave et al. \(2018\)](#page-5-0), showing that large monolingual corpora can be extracted from Common

<sup>700</sup> millions filtered documents in English alone, corresponding to 532 billions tokens. That is 120 times bigger than the data used in [Devlin et al. \(2018\)](#page-5-1).

<span id="page-0-0"></span><sup>1</sup><https://commoncrawl.org/about/>

<span id="page-0-1"></span><sup>2</sup> [github.com/facebookresearch/cc\\_net](github.com/facebookresearch/cc_net)

Crawl rapidly even with limited resources. Our work follows a similar pipeline with an additional step to select high-quality documents.

## 3. Methodology

Every month, Common Crawl releases a snapshot of the web obtained by randomly exploring and sampling URLs. Each webpage is made available different formats: raw (WARC), UTF-8 text (WET), and metadata (WAT). There is little content overlap between monthly snapshots. The complete archive consists of petabytes of data collected over 8 years of web crawling. The webpages are crawled from the whole web without restriction; they come in many different languages and in the quality of the text varies greatly. The Common Crawl represents a rich resource for monolingual data that comprises a large variety of domains, yet poses challenges due to the large quantity of noisy text.

Here we describe our the methodology used to fetch, deduplicate and filter the Common Crawl data. We focus on preprocessing the text (WET) format of the common crawl snapshots. Our pre-processing pipeline consists of several steps that we describe in this section. An overview of the pipeline is illustrated in figure [1.](#page-2-0)

### 3.1. Preprocessing

Each snapshot contain between 20 and 30TB of uncompressed plain text, corresponding to approximately 3 billion web pages (for instance the Feb. 2019 snapshot contains 24TB of data). We download and process each snapshot independently. For each snapshot, we regroup WET files into shards of 5GB each. This makes up for 1600 shards for Feb. 2019 crawl. These shards are saved into a JSON file where one entry corresponds to one web page.

### 3.2. Deduplication

The first step of our pipeline consists in removing duplicated paragraphs across the different web pages in a snapshot, as they represent 70% of the text. We first normalize each paragraph by lower-casing all characters, replacing numbers by a placeholder (i.e. 0) and removing all Unicode punctuation and accent marks. Then, the deduplication is done in two independent steps. First, for every shard, we compute a hash code for each paragraph and save them into a binary file. We use the first 64-bits of SHA-1 digits of the normalized paragraphs as the key. Then, we deduplicate every shard by comparing it with either 1, a subset or all of the binary files.

The impact of this choice is discussedin [4.](#page-1-0) These steps are independent for each shard and can thus be distributed. In addition to removing web copies, this step gets rid of a lot boilerplate such as navigation menus, cookie warnings and contact information. In particular, it removes significant amount of English content from webpages in other languages. This makes the language identification, which is the next step of our pipeline, more robust.

### 3.3. Language identification

The second step of our pipeline consists in splitting data per language. Following [Grave et al. \(2018\)](#page-5-0), we use the language classifier from fastText [\(Joulin et](#page-5-6) [al., 2016b;](#page-5-6) [Grave et al., 2018\)](#page-5-0). The fastText language identifier was trained on Wikipedia, Tatoeba and SE-Times. It uses characters n-grams as features, and the hierarchical softmax. It supports 176 languages and outputs a score for each of them in the [0, 1] range. It processes 1k documents per second on a single CPU core. For every web page we compute the most probable language, and the corresponding classifier score. If this score is higher than 0.5, we classify the document in the corresponding language. Otherwise, the language is not clearly identified, and we discard the corresponding page.

### 3.4. LM filtering

At this step of the pipeline, there are still documents with low quality content. A way to filter out these samples, is to compute a score of similarity of a web page with a targeted domain such as Wikipedia. In this paper, we propose to use the perplexity of a language model trained on the targeted domain as the quality score.

More precisely, for each language, we train a sentence piece tokenizer [\(Kudo, 2018\)](#page-5-7) and a language model on data from the targeted domain. We use a 5-gram Kneser-Ney model as implemented in the KenLM library [\(Heafield, 2011\)](#page-5-8) because of its efficiency to process large quantity of data. Then, we tokenize each page in our dataset, with our sentence piece tokenizer and compute the perplexity of each paragraph using our language model. The lower the perplexity, the closer the data is to the targeted domain. At the end of this step, each language is split into three even parts head, middle and tail, corresponding to the perplexity score. In section [5.](#page-4-0) we show perplexity distributions for one snapshot of Common Crawl.

We have trained sentence piece and Kneser-Ney language models on Wikipedia for 48 languages. We make these models publicly available in the repository. We also provide code to train sentence piece and Kneser-Ney language models and compute the terciles thresholds if the user wants to use other data to filter Common Crawl.

### 3.5. Reproducing results without the pipeline

Reconstructing the dataset by running our pipeline requires a lot of resources and time. Together with the release of the pipeline, we provide a tool to efficiently reproduce the results of this work. This tool builds on a file containing URLs of webpages and reconstructs the final output of our pipeline from this file.

# 4. Ablation study

<span id="page-1-0"></span>In this section, we discuss the impact of several design choices in our pipeline on the resulting datasets.

<span id="page-2-0"></span>![](_page_2_Figure_0.jpeg)

Figure 1: We show the whole pipeline for downloading and processing one snapshot of Common Crawl. First we download all the wet files and compute the paragraph hashes that we group and save into binary files. Then we process every document of the wet files independently: we deduplicate the paragraph using the binary files, we do a language identification and compute language model perplexity score. Finally, we regroup the documents into json files by language and perplexity score. The steps of the pipeline indicated with dashed arrows are parallelisable.

<span id="page-2-2"></span>![](_page_2_Figure_2.jpeg)

Figure 2: Number of tokens per language for the Feb. 2019 snapshot after deduplication. We display the histogram with logarithmic scale.

### 4.1. Order of LID and deduplication steps

Contrarily to [\(Grave et al., 2018\)](#page-5-0), we have chosen to deduplicate the data before language identification, because a lot of English boilerplate, such as cookie warnings, is present in pages of other languages. A significant amount of this noisy data is removed by deduplication which allows for better language identification. This is particularly important for some low resource languages. In Figure [3](#page-3-0) we report the relative increase in number of documents when doing "deduplication then LID" instead of "LID then deduplication". We observe that a lot of low resource language documents were mis-classified before deduplication (generally to English), or discarded because no language could be identified.

### 4.2. Impact of the amount of deduplication

For deduplication, we can compare paragraphs hashes shard by shard, across N shards or across the whole snapshot (1600 shards). The higher N, the higher the number of documents removed and the more RAM the algorithm will use. We show in [4](#page-3-1) the amount of data remaining (percentage of number of characters) for one shard of the snapshot Feb. 2019 after deduplication across 1, 2, 5, 10, 20, 50 and 100 shards. After deduplication across 1 shard, there is 42% of characters remaining and 28% across 100 shards. Loading hashes from 50 represents 1.5B unique hashes, making up 13.5GB on disk. Using a memory efficient hashset[3](#page-2-1) we can fit those into 40GB of RAM. In [5](#page-3-2) we show how the RAM increase when we try to load more hashes in memory. We found 50 shards to be a reasonable

<span id="page-2-1"></span><sup>3</sup> <github.com/greg7mdp/parallel-hashmap>

<span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)

Figure 3: Impact of doing "Deduplication then LID" rather than "LID then Deduplication". Y-axis shows per language-ratio of number of documents between the two methods. X-axis is the number of documents found for each language using LID scores obtained after deduplication. Low resources languages benefits the more from doing "Deduplication then LID" Stats estimated on 1% of Feb. 2019 snapshot.

trade-off and are therefore running the deduplication on blocks corresponding to 3% of the corpus.

<span id="page-3-1"></span>![](_page_3_Figure_3.jpeg)

Figure 4: Amount of data remaining after deduplication with different fraction of the dataset. These statistics are computed on one shard.

<span id="page-3-2"></span>![](_page_3_Figure_5.jpeg)

Figure 5: RAM usage when loading hashes from different fraction of the dataset. Computed on one shard.

#### 4.3. Benchmarking

The pipeline is massively parallelizable but still has to run in two steps because of the deduplication which requires to compare billions of documents paragraphs. In our case we chose shards of 5GB as the smallest unit of parallelisation. One dump is divided in 1600 shards, each containing around 1.6M documents. Computing the hashes of paragraphs is done at about 600 doc/s on one CPU core, while downloading the files at the same time. This means that one shard of about 1.6M documents is done in 45 min. We compute all the hashes in 45 minutes on 1600 CPUs. In one pass, the next step removes duplicates, and performs language identification, sentence piece tokenization, language modeling and splitting based on language. Each shard creates 3 files for the top 48 languages for which we have a LM, and one file for each other language where we don't have a LM. Each of those processing require a significant amount of RAM but the memory can be shared across processes since it is read only. This step is significantly longer than the previous one. We allocate 17 processes to one shard. The master process is responsible for downloading the data and distributing the raw documents to the 16 workers as well as writings the results to disk. The worker threads process around 40doc/s, processing the whole shard in about 40 minutes. Removing the duplicated parapgraphs takes 40% of the time. This step is computationally less expensive than the following ones but is done on all the data, as opposed to the next steps which are only applied to the deduplicated data. The language identifier takes 12.5% of CPU time, sentence piece 33% and the LM 13%. Finally we regroup the files produced at the previous steps in chunks of 5Gb. This can be run in parallel for each output file, and since gzip archive can be concatenated without being decompressed first it's very fast and runs in matter of minutes. The total processing time is about 9 hours using 5000 CPU cores for one snapshot.

# <span id="page-4-0"></span>5. Metrics about the resulting dataset

In this section, we report statistics corresponding to the corpus obtained after applying our pipeline on the Feb. 2019 snapshot of Common Crawl.

### 5.1. Statistics per language

After preprocessing it, we get 3.2TB of compressed documents in 174 languages. In table [6.,](#page-7-0) we give the sizes of each monolingual corpora for the 130 languages for which we have more than 1000 documents. We also compute the number of tokens and sentences for each language, and report them in Figure [2.](#page-2-2) The tokens were obtained by using the Sentence Piece tokenizer that was used in our preprocessing pipeline. The sentences were split using Moses. The three largest languages are English (en) with 532B tokens, Russian (ru) with 101B tokens and Chinese (zh) with 92B tokens. We obtained 11 languages with more than 10B tokens, and 27 languages with more than 1B tokens. In terms of documents, the three largest languages are English (en) with 706M documents, Russian (ru) with 167M and German (de) with 105M. There are 12 languages with more than 10M documents and 29 languages containing more than 1M documents. Common Crawl is also a good source for lower resource languages. For example Afrikaans (af), Gujarati (gu), Khmer (km) and Burmese (my) contains respectively 160MB, 190MB, 154MB and 440MB of data. In comparison Wikipedia contains 103MB, 88MB, 71MB and 153MB of data for these languages. And more resources are available through the 60 dumps of Common Crawl. These numbers could probably be improved by increasing the recall of the LID model for low-resource languages.

### 5.2. Statistics from the language model

We found that perplexity was a relative good proxy for quality. Journalistic and well written content ends up in the head of our dataset. Some documents which contained a lot of keywords list passes through deduplication and LID but receive a high perplexity. Some documents despite being valid text ends up in the tail because they have a vocabulary very different from Wikipedia. This includes blog comments with spokenlike text, or very specialized forums with specific jargon. We decided to not remove content based on the LM score because we think that some of it could be useful for specific applications.

Some languages have very spiked distribution of perplexity while others are more spread out. We postulate that this is rather due to the variance in the Wikipedia sizes used for training the LM than to some language having less high-quality content. Therefore we decided to use different perplexity thresholds for each language. The thresholds have been picked to split the corpus in 3 parts of equal size. In Figure [7](#page-5-9) we show the perplexity distribution for two languages English and Gujarati using their respective LM. English LM was trained on 534M of text while Gujarati was trained on only 12M.

### 5.3. Training models on this dataset

We assess the quality of the resulting dataset by learning unsupervised word and sentence representations through fastText and BERT models. For fastText, we train 300-dimensional word embeddings on the head, middle and tail subsets of the English and Polish CommonCrawl corpora, sorted by document perplexity. We evaluate these on standard semantic and syntactic analogy datasets [\(Mikolov et al., 2013\)](#page-6-5). We observe in Table [1](#page-4-1) a steady increase in performance as we go from the tail to the head of the dataset, confirming the positive impact of our filtering method based on document perplexity.

<span id="page-4-1"></span>

|              |              | English      |              | Polish       |              |              |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
|              | Total        | Sem          | Syn          | Total        | Sem          | Syn          |
| head         | 77.9         | 81.2         | 75.3         | 65.3         | 66.5         | 64.1         |
| mid.<br>tail | 74.2<br>62.0 | 79.0<br>68.1 | 70.4<br>57.3 | 62.8<br>59.9 | 62.7<br>59.8 | 63.0<br>60.1 |

Table 1: Impact of corpus quality on the quality of fastText word embeddings. We evaluate on semantic and syntactic similarity datasets.

We also train BERT models on the English (en), Russian (ru), Chinese (zh) and Urdu (ur) languages, using either the Wikipedia corpora or our new CommonCrawl datasets. For these languages, we use respectively 16G, 5G, 1.1G and 106M of raw Wikipedia data (full datasets), and we cap the head Common-Crawl data to 21G, 21G, 17G, 2.2G for English, Russian, Chinese and Urdu. That is, we consider roughly the same amount of data for English, but increase the amount of data for Russian, Chinese and Urdu. We train a BERT-BASE architecture [\(Devlin et al., 2018\)](#page-5-1) on each of these corpora, without next sentence prediction (NSP) as in [\(Lample and Conneau, 2019\)](#page-5-10). For better comparison, we early-stop all our models after two days of training on 16 Volta32 GPUs, and use the exact same number of steps for each model. We evaluate each model on the XNLI [\(Conneau et al., 2018\)](#page-5-11) corpus by using the training data in each language. Results presented in Table [2](#page-5-12) indicate that BERT-BASE models trained on CommonCrawl outperform identical models trained on Wikipedia by 3.3% on average. With the same amount of data for English, the BERT-BASE model trained on our corpus outperforms the one trained on the Wikipedia. For low-resource languages like Urdu (ur), the Wikipedia dataset being too small, the model pretrained on Wikipedia obtains similar performance than a randomly initialized model. Using our corpus instead, we obtain a 7 points improvement in accuracy, which demonstrates how our filtered corpus can enable language model pretraining for low-resource languages.

![](_page_5_Figure_0.jpeg)

Figure 6: Number of documents per language for the Feb. 2019 snapshot after deduplication. We display the histogram with logarithmic scale. We display statistics for 25 languages only. All statisctics are available in table [6.](#page-7-0)

<span id="page-5-9"></span>![](_page_5_Figure_2.jpeg)

Figure 7: Histogram of language model perplexities for the Feb. 2019 Common Crawl snapshot. The two histograms correspond to English, which is the largest dataset, and Gujarati which is a low-resource language. Vertical lines correspond to perplexity thresholds applied to split the corpus in head/middle/tail.

<span id="page-5-12"></span>

|      | en   | ru   | zh   | ur   | ∆    |
|------|------|------|------|------|------|
| Wiki | 82.8 | 73.3 | 77.0 | 57.3 | 72.6 |
| CC   | 85.0 | 76.4 | 77.9 | 64.3 | 75.9 |

Table 2: XNLI dev accuracy for English, Russian, Chinese and Urdu (∆ for average) for BERT-BASE models trained either on Wikipedia or CommonCrawl. The additional data provided by our pipeline alleviates the lack of resources in most languages and enables representation learning for low-resource languages such as Urdu.

### 6. Conclusion

In this paper, we present a pipeline to create curated monolingual corpora in more than 100 languages. We preprocess Common Crawl by following the pipeline of [\(Grave et al., 2018\)](#page-5-0), with the differences that we preserve the structure of documents and filter the data based on their distance to Wikipedia. This improves the quality of the resulting dataset and allows for the training of multilingual text level representations like XLM [\(Lample and Conneau, 2019\)](#page-5-10).

# References

<span id="page-5-5"></span>Baevski, A., Edunov, S., Liu, Y., Zettlemoyer, L., and Auli, M. (2019). Cloze-driven pretraining of self-attention networks. arXiv preprint arXiv:1903.07785.

<span id="page-5-4"></span>Buck, C., Heafield, K., and Van Ooyen, B. (2014). Ngram counts and language models from the common crawl. In LREC, volume 2, page 4. Citeseer.

<span id="page-5-11"></span>Conneau, A., Rinott, R., Lample, G., Williams, A., Bowman, S. R., Schwenk, H., and Stoyanov, V. (2018). Xnli: Evaluating cross-lingual sentence representations. In Proc. EMNLP.

<span id="page-5-1"></span>Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. (2018). Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805.

<span id="page-5-0"></span>Grave, E., Bojanowski, P., Gupta, P., Joulin, A., and Mikolov, T. (2018). Learning word vectors for 157 languages. arXiv preprint arXiv:1802.06893.

<span id="page-5-8"></span>Heafield, K. (2011). KenLM: faster and smaller language model queries. In Proceedings of the EMNLP 2011 Sixth Workshop on Statistical Machine Translation.

<span id="page-5-3"></span>Joulin, A., Grave, E., Bojanowski, P., Douze, M., Jégou, H., and Mikolov, T. (2016a). Fasttext.zip: Compressing text classification models. arXiv preprint arXiv:1612.03651.

<span id="page-5-6"></span>Joulin, A., Grave, E., Bojanowski, P., and Mikolov, T. (2016b). Bag of tricks for efficient text classification. arXiv preprint arXiv:1607.01759.

<span id="page-5-7"></span>Kudo, T. (2018). Subword regularization: Improving neural network translation models with multiple subword candidates. arXiv preprint arXiv:1804.10959.

<span id="page-5-10"></span>Lample, G. and Conneau, A. (2019). Crosslingual language model pretraining. arXiv preprint arXiv:1901.07291.

<span id="page-5-2"></span>Lan, Z., Chen, M., Goodman, S., Gimpel, K., Sharma, P., and Soricut, R. (2019). Albert: A lite bert for

- self-supervised learning of language representations. arXiv preprint arXiv:1909.11942.
- <span id="page-6-7"></span>Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., and Stoyanov, V. (2019). Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692.
- <span id="page-6-5"></span>Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., and Dean, J. (2013). Distributed representations of words and phrases and their compositionality. In Adv. NIPS.
- <span id="page-6-0"></span>Mikolov, T., Grave, E., Bojanowski, P., Puhrsch, C., and Joulin, A. (2017). Advances in pre-training distributed word representations. arXiv preprint arXiv:1712.09405.
- <span id="page-6-9"></span>Ortiz Suárez, P. J., Sagot, B., and Romary, L. (2019). Asynchronous pipeline for processing huge corpora on medium to low resource infrastructures. CMLC.
- <span id="page-6-6"></span>Pennington, J., Socher, R., and Manning, C. (2014). Glove: Global vectors for word representation. In Proc. EMNLP.
- <span id="page-6-1"></span>Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., and Zettlemoyer, L. (2018). Deep contextualized word representations. arXiv preprint arXiv:1802.05365.
- <span id="page-6-3"></span>Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., and Sutskever, I. (2019). Language models are unsupervised multitask learners. OpenAI Blog, 1(8).
- <span id="page-6-8"></span>Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. (2019). Exploring the limits of transfer learning with a unified text-to-text transformer. arXiv preprint arXiv:1910.10683.
- <span id="page-6-2"></span>Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. (2017). Attention is all you need. In Adv. NIPS.
- <span id="page-6-4"></span>Yang, Z., Dai, Z., Yang, Y., Carbonell, J., Salakhutdinov, R., and Le, Q. V. (2019). Xlnet: Generalized autoregressive pretraining for language understanding. arXiv preprint arXiv:1906.08237.

<span id="page-7-0"></span>

| -                      |                                                   |                                                    |                                                    |                                                    |
|------------------------|---------------------------------------------------|----------------------------------------------------|----------------------------------------------------|----------------------------------------------------|
| Language               | Documents                                         | Sentences                                          | Tokens                                             | Size in bytes                                      |
| af                     | $73.232 \times 10^3$                              | $5.390 \times 10^{6}$                              | $73.041 \times 10^6$                               | $160.015 \times 10^6$                              |
| als                    | $7.615 \times 10^{3}$                             | $324.334 \times 10^3$                              | $3.526 \times 10^{6}$                              | $9.977 \times 10^{6}$                              |
| am                     | $54.182 \times 10^3$                              | $1.533 \times 10^{6}$                              | $27.561 \times 10^{6}$                             | $98.878 \times 10^{6}$                             |
| an                     | $1.264 \times 10^{3}$                             | $16.818 \times 10^3$                               | $213.407 \times 10^3$                              | $824.466 \times 10^3$                              |
| ar                     | $7.132 \times 10^{6}$                             | $248.711 \times 10^6$                              | $3.777 \times 10^9$                                | $13.602 \times 10^9$                               |
| arz                    | $44.384 \times 10^3$                              | $379.209 \times 10^3$                              | $4.222 \times 10^{6}$                              | $18.821 \times 10^{6}$                             |
| as                     | $12.758 \times 10^{3}$                            | $563.956 \times 10^3$                              | $10.463 \times 10^6$                               | $24.174 \times 10^{6}$                             |
| ast                    | $3.814 \times 10^{3}$                             | $104.890 \times 10^{3}$                            | $1.357 \times 10^{6}$                              | $3.907 \times 10^{6}$                              |
| az                     | $507.612 \times 10^3$                             | $21.341 \times 10^{6}$                             | $232.269 \times 10^6$                              | $757.804 \times 10^{6}$                            |
| azb                    | $12.733 \times 10^{3}$                            | $306.696 \times 10^{3}$                            | $4.365 \times 10^{6}$                              | $13.829 \times 10^{6}$                             |
| ba                     | $30.195 \times 10^{3}$                            | $1.047 \times 10^{6}$                              | $12.923 \times 10^6$                               | $44.612 \times 10^{6}$                             |
| be                     | $176.037 \times 10^3$                             | $9.719 \times 10^{6}$                              | $124.716 \times 10^6$                              | $476.612 \times 10^6$                              |
| bg                     | $3.002 \times 10^{6}$                             | $129.758 \times 10^6$                              | $1.835 \times 10^{9}$                              | $6.224 \times 10^{9}$                              |
| $\operatorname{bn}$    | $941.621 \times 10^{3}$                           | $38.413 \times 10^{6}$                             | $708.464 \times 10^6$                              | $1.717 \times 10^{9}$                              |
| bo                     | $30.028 \times 10^{3}$                            | $528.293 \times 10^3$                              | $47.940 \times 10^{6}$                             | $50.786 \times 10^6$                               |
| bpy                    | $2.514 \times 10^{3}$                             | $41.791 \times 10^{3}$                             | $549.568 \times 10^3$                              | $1.536 \times 10^{6}$                              |
| $\mathrm{br}$          | $21.594 \times 10^{3}$                            | $653.440 \times 10^{3}$                            | $7.413 \times 10^{6}$                              | $17.989 \times 10^{6}$                             |
| bs                     | $12.906 \times 10^{3}$                            | $72.042 \times 10^{3}$                             | $506.201 \times 10^3$                              | $3.476 \times 10^{6}$                              |
| ca                     | $2.018 \times 10^{6}$                             | $70.986 \times 10^{6}$                             | $1.230 \times 10^{9}$                              | $2.841 \times 10^{9}$                              |
| ce                     | $5.534 \times 10^{3}$                             | $222.896 \times 10^{3}$                            | $2.401 \times 10^{6}$                              | $7.812 \times 10^{6}$                              |
| $\operatorname{ceb}$   | $58.489 \times 10^{3}$                            | $2.044 \times 10^{6}$                              | $11.655 \times 10^6$                               | $26.459 \times 10^6$                               |
| $\operatorname{ckb}$   | $116.103 \times 10^3$                             | $2.696 \times 10^{6}$                              | $62.219 \times 10^6$                               | $146.949 \times 10^6$                              |
| CS                     | $11.140 \times 10^6$                              | $444.808 \times 10^6$                              | $5.691 \times 10^{9}$                              | $17.306 \times 10^9$                               |
| $\operatorname{cv}$    | $13.312 \times 10^{3}$                            | $392.207 \times 10^3$                              | $3.840 \times 10^{6}$                              | $14.483 \times 10^6$                               |
| cy                     | $127.800 \times 10^3$                             | $4.249 \times 10^{6}$                              | $56.984 \times 10^6$                               | $132.824 \times 10^6$                              |
| da                     | $4.411 \times 10^{6}$                             | $209.623 \times 10^6$                              | $2.974 \times 10^{9}$                              | $7.100 \times 10^{9}$                              |
| $\mathrm{d}\mathrm{e}$ | $105.425 \times 10^6$                             | $4.249 \times 10^{9}$                              | $58.195 \times 10^9$                               | $164.540 \times 10^9$                              |
| dv                     | $26.274 \times 10^{3}$                            | $841.155 \times 10^3$                              | $9.899 \times 10^{6}$                              | $35.401 \times 10^{6}$                             |
| el                     | $5.681 \times 10^{6}$                             | $201.470 \times 10^6$                              | $3.282 \times 10^{9}$                              | $12.174 \times 10^9$                               |
| en                     | $706.583 \times 10^6$                             | $32.110 \times 10^9$                               | $532.368 \times 10^9$                              | $1.955 \times 10^{12}$                             |
| eo                     | $126.188 \times 10^3$                             | $6.152 \times 10^{6}$                              | $70.107 \times 10^6$                               | $161.092 \times 10^6$                              |
| es                     | $82.991 \times 10^6$                              | $3.048 \times 10^{9}$                              | $54.792 \times 10^9$                               | $134.206 \times 10^9$                              |
| $\operatorname{et}$    | $1.043 \times 10^6$                               | $56.678 \times 10^{6}$                             | $537.668 \times 10^6$                              | $1.598 \times 10^{9}$                              |
| eu                     | $381.323 \times 10^3$                             | $10.355 \times 10^{6}$                             | $109.635 \times 10^6$                              | $342.909 \times 10^6$                              |
| fa                     | $7.201 \times 10^{6}$                             | $282.130 \times 10^6$                              | $5.441 \times 10^9$                                | $15.571 \times 10^9$                               |
| fi                     | $4.118 \times 10^{6}$                             | $191.905 \times 10^6$                              | $2.089 \times 10^9$                                | $6.836 \times 10^9$                                |
| fr                     | $86.176 \times 10^6$                              | $3.540 \times 10^9$                                | $58.428 \times 10^9$                               | $220.869 \times 10^9$                              |
| fy                     | $31.228 \times 10^3$                              | $1.087 \times 10^{6}$                              | $12.082 \times 10^6$                               | $31.296 \times 10^6$                               |
| $_{\mathrm{ga}}$       | $59.515 \times 10^3$                              | $2.068 \times 10^6$                                | $29.632 \times 10^{6}$                             | $73.301 \times 10^6$                               |
| $\operatorname{gd}$    | $10.114 \times 10^3$                              | $225.829 \times 10^3$                              | $4.132 \times 10^{6}$                              | $9.906 \times 10^{6}$                              |
| $\operatorname{gl}$    | $400.289 \times 10^3$                             | $12.171 \times 10^6$                               | $196.539 \times 10^6$                              | $487.379 \times 10^6$                              |
| gu                     | $98.263 \times 10^{3}$                            | $4.705 \times 10^6$                                | $71.586 \times 10^6$                               | $189.806 \times 10^6$                              |
| he                     | $2.166 \times 10^{6}$                             | $124.089 \times 10^6$                              | $1.470 \times 10^9$                                | $4.583 \times 10^9$                                |
| hi                     | $1.370 \times 10^6$                               | $52.221 \times 10^6$                               | $1.165 \times 10^9$                                | $2.762 \times 10^9$                                |
| hr                     | $821.782 \times 10^3$                             | $40.070 \times 10^6$                               | $515.230 \times 10^6$                              | $1.413 \times 10^9$                                |
| hsb                    | $8.914 \times 10^3$                               | $216.630 \times 10^3$<br>$249.899 \times 10^6$     | $2.288 \times 10^{6}$                              | $8.500 \times 10^6 $ $10.232 \times 10^9 $         |
| hu                     | $5.643 \times 10^6$ $308.674 \times 10^3$         | $10.995 \times 10^{6}$                             | $3.272 \times 10^9$ $152.337 \times 10^6$          | $10.232 \times 10^{6}$<br>$579.637 \times 10^{6}$  |
| hy<br>:-               |                                                   | $10.995 \times 10^{3}$<br>$17.315 \times 10^{3}$   | $152.337 \times 10^{3}$<br>$291.786 \times 10^{3}$ | $930.327 \times 10^{3}$                            |
| ia                     | $1.460 \times 10^{3}$ $9.728 \times 10^{6}$       | $17.315 \times 10^{6}$<br>$488.888 \times 10^{6}$  | $291.786 \times 10^{9}$ $6.124 \times 10^{9}$      | $930.327 \times 10^{9}$<br>$15.782 \times 10^{9}$  |
| id<br>ilo              | $9.728 \times 10^{3}$<br>$3.990 \times 10^{3}$    | $488.888 \times 10^{3}$<br>$131.515 \times 10^{3}$ | $6.124 \times 10^{6}$<br>$1.671 \times 10^{6}$     | $15.782 \times 10^{6}$<br>$4.421 \times 10^{6}$    |
| ilo<br>io              | $3.990 \times 10^{3}$<br>$1.051 \times 10^{3}$    | $131.515 \times 10^{3}$<br>$22.527 \times 10^{3}$  | $1.671 \times 10^{\circ}$ $174.627 \times 10^{3}$  | $4.421 \times 10^{\circ}$ $653.994 \times 10^{3}$  |
| io<br>ia               | $1.051 \times 10^{3}$<br>$346.180 \times 10^{3}$  | $22.527 \times 10^{6}$<br>$13.072 \times 10^{6}$   | $174.627 \times 10^{6}$<br>$173.198 \times 10^{6}$ | $553.994 \times 10^{6}$<br>$502.002 \times 10^{6}$ |
| is<br>:+               | $346.180 \times 10^{6}$<br>$45.080 \times 10^{6}$ | $13.072 \times 10^{9}$<br>$1.637 \times 10^{9}$    | $173.198 \times 10^{9}$<br>$29.381 \times 10^{9}$  | $502.002 \times 10^{9}$<br>$72.517 \times 10^{9}$  |
| it                     | $45.080 \times 10^{6}$<br>$53.880 \times 10^{6}$  | $1.637 \times 10^{9}$<br>$4.092 \times 10^{9}$     | $29.381 \times 10^{9}$<br>$54.883 \times 10^{9}$   | $72.517 \times 10^{9}$<br>$127.792 \times 10^{9}$  |
| ja<br>ibo              | $53.880 \times 10^{3}$<br>$1.261 \times 10^{3}$   | $4.092 \times 10^{3}$<br>$171.615 \times 10^{3}$   | $54.883 \times 10^{6}$ $1.514 \times 10^{6}$       | $127.792 \times 10^{6}$ $1.873 \times 10^{6}$      |
| jbo<br>iv              | $1.261 \times 10^{3}$<br>$2.165 \times 10^{3}$    | $358.813 \times 10^{3}$                            | $5.185 \times 10^{6}$                              | $1.873 \times 10^{6}$<br>$11.502 \times 10^{6}$    |
| jv<br>ko               | $2.165 \times 10^{3}$<br>$368.404 \times 10^{3}$  | $16.747 \times 10^6$                               | $5.185 \times 10^{6}$ $176.632 \times 10^{6}$      | $11.502 \times 10^{6}$<br>$695.075 \times 10^{6}$  |
| ka                     | 506.404 × 10°                                     | $10.747 \times 10^{\circ}$                         | $170.052 \times 10^{\circ}$                        | 090.075 × 10°                                      |

| kk                          | $208.652 \times 10^3$                             | $11.658 \times 10^{6}$                            | $134.347 \times 10^6$                            | $526.160 \times 10^6$                                 |
|-----------------------------|---------------------------------------------------|---------------------------------------------------|--------------------------------------------------|-------------------------------------------------------|
| $\mathrm{km}$               | $85.211 \times 10^{3}$                            | $2.103 \times 10^{6}$                             | $87.503 \times 10^6$                             | $153.530 \times 10^6$                                 |
| $_{\rm kn}$                 | $112.553 \times 10^3$                             | $5.733 \times 10^{6}$                             | $95.568 \times 10^{6}$                           | $217.285 \times 10^6$                                 |
| ko                          | $5.707 \times 10^{6}$                             | $361.022 \times 10^6$                             | $7.590 \times 10^{9}$                            | $11.969 \times 10^9$                                  |
| krc                         | $1.696 \times 10^{3}$                             | $92.260 \times 10^{3}$                            | $926.524 \times 10^3$                            | $3.371 \times 10^{6}$                                 |
| ku                          | $49.678 \times 10^{3}$                            | $1.843 \times 10^{6}$                             | $24.831 \times 10^{6}$                           | $61.128 \times 10^6$                                  |
| kv                          | $1.003 \times 10^{3}$                             | $56.540 \times 10^{3}$                            | $586.116 \times 10^{3}$                          | $2.008 \times 10^{6}$                                 |
| ky                          | $92.894 \times 10^{3}$                            | $2.988 \times 10^{6}$                             | $36.216 \times 10^{6}$                           | $131.434 \times 10^6$                                 |
| la                          | $75.987 \times 10^{3}$                            | $2.932 \times 10^{6}$                             | $41.604 \times 10^{6}$                           | $101.977 \times 10^6$                                 |
| lb                          | $30.740 \times 10^{3}$                            | $965.947 \times 10^{3}$                           | $11.306 \times 10^6$                             | $32.277 \times 10^{6}$                                |
| lez                         | $1.735 \times 10^{3}$                             | $95.626 \times 10^{3}$                            | $987.272 \times 10^3$                            | $3.274 \times 10^{6}$                                 |
| lmo                         | $1.219 \times 10^{3}$                             | $19.033 \times 10^{3}$                            | $243.748 \times 10^3$                            | $798.331 \times 10^{3}$                               |
| lo                          | $44.895 \times 10^{3}$                            | $903.215 \times 10^3$                             | $22.707 \times 10^6$                             | $51.361 \times 10^{6}$                                |
| lt                          | $1.485 \times 10^{6}$                             | $63.860 \times 10^{6}$                            | $780.747 \times 10^6$                            | $2.337 \times 10^{9}$                                 |
| lv                          | $846.034 \times 10^3$                             | $33.904 \times 10^{6}$                            | $440.403 \times 10^6$                            | $1.336 \times 10^{9}$                                 |
| mg                          | $14.670 \times 10^3$                              | $409.271 \times 10^3$                             | $6.172 \times 10^6$                              | $14.535 \times 10^6$                                  |
| mhr                         | $4.091 \times 10^{3}$                             | $114.556 \times 10^3$                             | $1.215 \times 10^{6}$                            | $4.699 \times 10^{6}$                                 |
| mk                          | $268.409 \times 10^3$                             | $8.653 \times 10^{6}$                             | $136.563 \times 10^6$                            | $482.894 \times 10^6$                                 |
| ml                          | $292.062 \times 10^3$                             | $13.485 \times 10^6$                              | $327.757 \times 10^6$                            | $559.466 \times 10^6$                                 |
| mn                          | $161.780 \times 10^3$                             | $6.790 \times 10^{6}$                             | $90.969 \times 10^6$                             | $339.398 \times 10^6$                                 |
| $^{\mathrm{mr}}$            | $151.850 \times 10^3$                             | $8.132 \times 10^{6}$                             | $130.610 \times 10^6$                            | $319.199 \times 10^6$                                 |
| $^{\rm ms}$                 | $373.244 \times 10^3$                             | $6.964 \times 10^{6}$                             | $85.562 \times 10^6$                             | $259.173 \times 10^6$                                 |
| $^{\rm mt}$                 | $27.734 \times 10^{3}$                            | $1.096 \times 10^{6}$                             | $17.246 \times 10^6$                             | $44.436 \times 10^{6}$                                |
| my                          | $170.775 \times 10^3$                             | $6.712 \times 10^6$                               | $79.498 \times 10^{6}$                           | $439.538 \times 10^6$                                 |
| mzn                         | $2.483 \times 10^{3}$                             | $16.401 \times 10^{3}$                            | $146.797 \times 10^3$                            | $1.085 \times 10^{6}$                                 |
| $\frac{111211}{\text{nds}}$ | $16.518 \times 10^{3}$                            | $380.501 \times 10^3$                             | $4.051 \times 10^6$                              | $11.791 \times 10^6$                                  |
| ne                          | $184.598 \times 10^{3}$                           | $6.278 \times 10^6$                               | $147.027 \times 10^6$                            | $333.808 \times 10^6$                                 |
| new                         | $3.670 \times 10^{3}$                             | $68.984 \times 10^{3}$                            | $1.632 \times 10^6$                              | $3.705 \times 10^{6}$                                 |
| nl                          | $31.635 \times 10^{6}$                            | $1.214 \times 10^9$                               | $15.946 \times 10^9$                             | $41.821 \times 10^9$                                  |
|                             | $123.371 \times 10^3$                             | $4.705 \times 10^{6}$                             | $55.776 \times 10^6$                             | $145.495 \times 10^6$                                 |
| nn                          | $3.268 \times 10^6$                               | $158.837 \times 10^6$                             | $2.145 \times 10^9$                              | $5.524 \times 10^9$                                   |
| no                          | $9.138 \times 10^{3}$                             | $300.022 \times 10^3$                             | $4.327 \times 10^{6}$                            | $10.648 \times 10^6$                                  |
| oc                          | $65.718 \times 10^{3}$                            | $961.342 \times 10^{3}$                           | $33.005 \times 10^{6}$                           | $73.860 \times 10^6$                                  |
| or                          | $3.723 \times 10^{3}$                             | $163.153 \times 10^3$                             | $1.762 \times 10^6$                              | $5.828 \times 10^6$                                   |
| os<br>pl                    | $31.242 \times 10^{6}$                            | $1.300 \times 10^9$                               | $16.661 \times 10^9$                             | $49.738 \times 10^9$                                  |
| pl                          | $4.087 \times 10^{3}$                             | $72.314 \times 10^{3}$                            | $1.124 \times 10^6$                              | $2.262 \times 10^{6}$                                 |
| pms                         | $12.195 \times 10^{3}$                            | $12.314 \times 10^{4}$<br>$221.196 \times 10^{3}$ | $2.752 \times 10^{6}$                            | $8.905 \times 10^6$                                   |
| pnb                         | $69.971 \times 10^3$                              | $1.975 \times 10^6$                               | $43.603 \times 10^6$                             | $109.935 \times 10^6$                                 |
| ps<br>nt                    | $37.305 \times 10^6$                              | $1.489 \times 10^9$                               | $23.875 \times 10^9$                             | $57.388 \times 10^9$                                  |
| pt                          | $5.187 \times 10^6$                               | $1.469 \times 10^{6}$ $222.040 \times 10^{6}$     | $3.848 \times 10^9$                              | $9.904 \times 10^9$                                   |
| ro                          | $167.323 \times 10^6$                             | $7.718 \times 10^9$                               | $3.848 \times 10^{9}$ $101.143 \times 10^{9}$    | $384.733 \times 10^9$                                 |
| ru                          | $107.323 \times 10^{3}$<br>$10.064 \times 10^{3}$ | $7.718 \times 10^{3}$<br>$794.837 \times 10^{3}$  | $101.143 \times 10^{6}$ $19.843 \times 10^{6}$   | $32.559 \times 10^6$                                  |
| sa<br>1-                    | $8.403 \times 10^3$                               | $434.283 \times 10^3$                             | $4.135 \times 10^6$                              | $14.271 \times 10^6$                                  |
| sah                         | $8.403 \times 10^{3}$<br>$31.636 \times 10^{3}$   | $434.283 \times 10^{6}$ $1.133 \times 10^{6}$     | $4.135 \times 10^{\circ}$ $22.065 \times 10^{6}$ | $14.271 \times 10^{\circ}$<br>$53.052 \times 10^{6}$  |
| $\operatorname{sd}$         | $66.385 \times 10^{3}$                            | $2.569 \times 10^{6}$                             | $8.072 \times 10^{6}$                            | $53.052 \times 10^{\circ}$<br>$27.332 \times 10^{6}$  |
| sh                          | $154.658 \times 10^{3}$                           | $2.569 \times 10^{6}$<br>$7.072 \times 10^{6}$    | $8.072 \times 10^{6}$ $124.514 \times 10^{6}$    | $27.332 \times 10^{\circ}$<br>$270.364 \times 10^{6}$ |
| si<br>-1-                   | $4.472 \times 10^6$                               | $1.072 \times 10^{6}$<br>$115.211 \times 10^{6}$  |                                                  | $4.787 \times 10^9$                                   |
| $\operatorname{sk}$         |                                                   | $50.734 \times 10^6$                              | $1.618 \times 10^9$ $749.341 \times 10^6$        |                                                       |
| sl                          | $1.828 \times 10^6$                               |                                                   |                                                  | $2.101 \times 10^9$                                   |
| $\operatorname{sq}$         | $687.411 \times 10^3$                             | $23.223 \times 10^6$                              | $392.871 \times 10^6$                            | $929.548 \times 10^{6}$                               |
| $\operatorname{sr}$         | $1.344 \times 10^{6}$                             | $56.660 \times 10^{6}$                            | $717.548 \times 10^6$                            | $2.108 \times 10^9$                                   |
| sv                          | $15.774 \times 10^6$                              | $479.216 \times 10^{6}$                           | $7.149 \times 10^9$                              | $19.160 \times 10^9$                                  |
| sw                          | $66.205 \times 10^3$                              | $1.915 \times 10^6$                               | $36.508 \times 10^6$                             | $84.468 \times 10^6$                                  |
| $_{\rm ta}$                 | $944.262 \times 10^3$                             | $48.390 \times 10^{6}$                            | $1.002 \times 10^9$                              | $1.513 \times 10^9$                                   |
| te                          | $324.091 \times 10^3$                             | $13.951 \times 10^{6}$                            | $225.516 \times 10^{6}$                          | $491.376 \times 10^{6}$                               |
| tg                          | $95.142 \times 10^3$                              | $3.524 \times 10^{6}$                             | $52.462 \times 10^{6}$                           | $167.373 \times 10^6$                                 |
| th                          | $6.639 \times 10^6$                               | $181.397 \times 10^6$                             | $2.743 \times 10^9$                              | $7.869 \times 10^9$                                   |
| tk                          | $10.841 \times 10^3$                              | $347.561 \times 10^3$                             | $4.722 \times 10^{6}$                            | $14.295 \times 10^{6}$                                |
| tl                          | $192.164 \times 10^3$                             | $12.370 \times 10^6$                              | $154.572 \times 10^6$                            | $329.472 \times 10^6$                                 |
| $\operatorname{tr}$         | $19.454 \times 10^6$                              | $478.459 \times 10^{6}$                           | $6.427 \times 10^9$                              | $20.045 \times 10^9$                                  |
| $\operatorname{tt}$         | $112.660 \times 10^3$                             | $3.721 \times 10^6$                               | $46.220 \times 10^6$                             | $158.642 \times 10^6$                                 |
|                             |                                                   |                                                   |                                                  |                                                       |

| ug  | $27.041 \times 10^{3}$ | $803.821 \times 10^{3}$ | $13.479 \times 10^{6}$  | $44.824 \times 10^{6}$  |
|-----|------------------------|-------------------------|-------------------------|-------------------------|
| uk  | $4.100 \times 10^{6}$  | $199.198 \times 10^6$   | $2.672 \times 10^{9}$   | $9.877 \times 10^{9}$   |
| ur  | $506.610 \times 10^3$  | $8.579 \times 10^{6}$   | $289.277 \times 10^6$   | $745.210 \times 10^6$   |
| uz  | $35.274 \times 10^{3}$ | $1.242 \times 10^{6}$   | $17.024 \times 10^6$    | $45.010 \times 10^{6}$  |
| vi  | $16.207 \times 10^6$   | $529.567 \times 10^6$   | $9.836 \times 10^{9}$   | $20.272 \times 10^9$    |
| vo  | $4.934 \times 10^{3}$  | $72.943 \times 10^{3}$  | $629.462 \times 10^3$   | $1.689 \times 10^{6}$   |
| wa  | $1.548 \times 10^{3}$  | $77.610 \times 10^{3}$  | $758.117 \times 10^{3}$ | $1.735 \times 10^{6}$   |
| war | $14.530 \times 10^{3}$ | $162.150 \times 10^{3}$ | $1.160 \times 10^{6}$   | $4.310 \times 10^{6}$   |
| wuu | $2.907\times10^3$      | $4.252\times10^3$       | $70.935\times10^3$      | $956.106 \times 10^{3}$ |
| xmf | $3.854 \times 10^{3}$  | $116.818 \times 10^3$   | $764.346 \times 10^3$   | $3.128 \times 10^{6}$   |
| yi  | $30.177 \times 10^{3}$ | $1.630 \times 10^{6}$   | $23.397 \times 10^{6}$  | $59.623 \times 10^{6}$  |
| zh  | $46.264 \times 10^6$   | $3.081 \times 10^{9}$   | $92.373 \times 10^9$    | $140.366 \times 10^9$   |

 ${\it Table 3: \ Number of documents, sentences and tokens after deduplication.}$