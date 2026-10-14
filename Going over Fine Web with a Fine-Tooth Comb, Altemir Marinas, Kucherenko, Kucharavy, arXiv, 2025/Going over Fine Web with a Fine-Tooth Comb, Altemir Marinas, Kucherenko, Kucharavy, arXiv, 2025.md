                                                         Going over Fine Web with a Fine-Tooth Comb:
                                             Technical Report of Indexing Fine Web for Problematic Content Search
                                                                         and Retrieval
                                                         Inés Altemir Marinas ∗1 , Anastasiia Kucherenko2 , Andrei Kucharavy3
                                                                   1
                                                                     École Polytechnique Fédérale de Lausanne, Switzerland
                                                  2
                                                    Institute of Entrepreneurship and Management, HES-SO Valais-Wallis, Switzerland
                                                                3
                                                                  Institute of Informatics, HES-SO Valais-Wallis, Switzerland

                                                                Abstract                          et al. (2025), which propagate into LLM output. Re-
                                                                                                  search has consistently demonstrated that such con-
                                              Large language models (LLMs) rely heavily on        tent persists even after conventional filtering pro-
arXiv:2508.21788v1 [cs.CL] 29 Aug 2025




                                              web-scale datasets like Common Crawl, which
                                                                                                  cedures (such as perplexity-based filtering), with
                                              provides over 80% of training data for some
                                              modern models. However, the indiscriminate          studies finding that 2-6% of web pages in Com-
                                              nature of web crawling raises challenges in data    mon Crawl contain hate speech and approximately
                                              quality, safety, and ethics. Despite the critical   2% contain sexually explicit content (Luccioni and
                                              importance of training data quality, prior re-      Viviano (2021)).
                                              search on harmful content has been limited to          The implications of this contamination vary
                                              small samples due to computational constraints.
                                                                                                  significantly across different model deployment
                                              This project presents a comprehensive frame-
                                              work for indexing and analyzing entire LLM          paradigms. While API-only models can implement
                                              training datasets using an ElasticSearch-based      generation-time filtering to mitigate harmful out-
                                              pipeline. We apply it to SwissAI’s FineWeb-2        puts, this approach becomes ineffective for open-
                                              corpus (1.5TB, four languages), achieving fast      weights models where the full model parameters
                                              query performance—most searches in millisec-        are publicly available. For open-source models,
                                              onds, all under 2 seconds. Our work demon-          comprehensive training data mapping and analysis
                                              strates the feasibility of comprehensive, real-
                                                                                                  represents the primary defense against propagating
                                              time dataset analysis, offering practical tools
                                              for safer, more accountable AI systems.
                                                                                                  problematic content, making preemptive dataset
                                                                                                  governance essential rather than optional. This
                                         1    Introduction                                        fundamental difference underscores the critical im-
                                                                                                  portance of thorough training data analysis for the
                                         The capabilities of large language models Brown          growing ecosystem of open-weights language mod-
                                         et al. (2020)), Touvron et al. (2023), Grattafiori       els.
                                         et al. (2024), Abdin et al. (2024), Bubeck et al.           The personally identifiable information present
                                         (2023) are primarily derived from pretraining            in these large-scale datasets poses a severe privacy
                                         on extense web-scale datasets such as Common             risk, as demonstrated by Carlini et al. (2021), who
                                         Crawl and derivates C4 Raffel et al. (2020) and          showed that adversaries can perform training data
                                         FineWeb Penedo et al. (2024). These web-scraped          extraction attacks to recover individual training
                                         datasets have become the de facto standard for           examples—including personally identifiable infor-
                                         internet-scale pretraining datasets, as some models      mation like names, phone numbers, and email ad-
                                         such as GPT-3 Brown et al. (2020) had more than          dresses—by simply querying large language mod-
                                         80% of its tokens coming from Common Crawl.              els like GPT-2. These privacy concerns are further
                                                                                                  compounded by copyright and content authenticity
                                            However, the scale that enables these remark-         challenges that have emerged from the indiscrimi-
                                         able capabilities also introduces significant chal-      nate use of web-scraped data. The legal and ethi-
                                         lenges. Web-mined corpora inevitably contain sub-        cal implications of using massive internet-scraped
                                         stantial amounts of undesirable content, including       datasets without clear rights or consent have materi-
                                         hate speech, sexually explicit material, misinforma-     alized in high-profile cases, with major content cre-
                                         tion, copyrighted data, and personally identifiable      ators like the New York Times now actively block-
                                         informationLuccioni and Viviano (2021), Mendu            ing OpenAI’s web crawler and Common Crawl
                                              ∗
                                              The main contributing author                        from accessing their pages using robots.txt to pre-
vent unauthorized use of their content in AI training     gual training corpora. The urgency of such
(Baack, 2024). Simultaneously, the infiltration of        comprehensive-scale analysis is underscored by the
misinformation into training datasets represents an-      multilingual nature of modern LLM training, where
other critical vulnerability. Malicious actors can        harmful content patterns may vary significantly
deliberately inject false or misleading information       across languages and cultural contexts—variations
into web content that subsequently gets incorpo-          that sampling-based approaches cannot reliably
rated into model training data, potentially compro-       capture. While considerable research has focused
mising the reliability of AI systems at scale. An         on post-training alignment techniques, significantly
example of this is the Moscow-based disinforma-           less attention has been devoted to the foundational
tion network “Pravda”, who with 3,600,000 articles        role of training data quality in ensuring model
in 2024 have flooded search results and web web           safety, making scalable indexing infrastructure es-
crawlers with pro-Kremlin discourse1 .                    sential for responsible AI development.
   These interconnected challenges—privacy viola-            Our work specifically addresses this gap by
tions, copyright infringement, and data contamina-        applying our framework to SwissAI’s multilingual
tion—underscore the urgent need for transparent,          FineWeb-2 corpus, demonstrating comprehensive
searchable, and auditable data pipelines.                 exploration capabilities that sampling-based
   A critical limitation of existing research on train-   approaches cannot reliably access at scale. The
ing data quality is the reliance on small-scale sam-      contributions of this work are threefold: (1) the
pling due to computational constraints. Luccioni          development of a scalable indexing infrastructure
and Viviano (2021) analyzed only 1% of Common             that overcomes computational barriers limiting pre-
Crawl files (approximately 81 GB) due to "hard-           vious research to small samples, (2) demonstration
ware constraints", while Mendu et al. (2025) ex-          of the system’s efficiency through targeted searches
amined 1 million random web pages for their com-          across multiple query types that reveal problematic
prehensive harm taxonomy development. While               content across languages in the complete training
these samples may be statistically representative,        corpus, and (3) the provision of production-ready
the limitation to subsets potentially obscures impor-     tools for ongoing dataset governance at the scale
tant patterns in harmful content distribution, rare       required for modern LLM development.
but significant toxic clusters, and domain-specific
bias patterns that emerge only at scale.                     This framework positions Switzerland and its
   To address these critical challenges, this project     SwissAI model as leaders in responsible AI devel-
develops a comprehensive ElasticSearch-based              opment, demonstrating how comprehensive train-
framework for indexing and searching complete             ing data governance can ensure AI systems are built
LLM training datasets rather than representative          on well-understood, ethically-sourced, and legally-
samples. The indexing pipeline ingests large train-       compliant datasets—goals that align closely with
ing datasets and builds searchable indexes that sup-      Switzerland’s longstanding values. By developing
port multiple query paradigms: exact phrase match-        the tools and methodologies to thoroughly under-
ing for precise content identification, approximate       stand and audit training data, we can ensure that
matching through configurable fuzzy search for            the next generation of AI systems serves society
handling variations and typos, and semantic similar-      while respecting privacy, copyright, and safety prin-
ity search for discovering conceptually related con-      ciples. Crucially, our open indexing infrastructure
tent. These capabilities are unified through additive     enables independent third parties to audit both the
query logic, enabling complex boolean combina-            training data and resulting models, fostering the
tions that can simultaneously search for exact terms,     kind of transparent, verifiable AI development that
semantic concepts, and fuzzy variants—creating            can build public trust and establish international
an extremely powerful tool for ensuring LLM user          standards for responsible AI governance.
safety and comprehensive dataset governance.
   Unlike previous research constrained by compu-         2   ElasticSearch
tational limitations, our framework enables sys-
tematic content analysis across entire multilin-          Elasticsearch (ES) is a distributed, RESTful search
   1
                                                          and analytics engine built on Apache Lucene.
    https://www.newsguardtech.com/special-repor
ts/moscow-based-global-news-network-infected-wes            For the distributed character of ES, we can run an
tern-artificial-intelligence-russian-propaganda/          ES instance in discovery.type=single-node or
discovery.type=multi.node, where multi-node                    processing across multiple workers. A merg-
configuration allows ES to discover other nodes                ing operation is later executed to create a uni-
when forming a cluster and allows other nodes to               fied unique index.
join the cluster later. (explain what a cluster is).
                                                            • Advanced query execution engine: Supports
In multi-node mode, the data is automatically split
                                                              six distinct query types ranging from simple
across multiple nodes (servers) in a cluster. Each
                                                              term matching to complex boolean combina-
index is divided into "shards" - independent pieces
                                                              tions and fuzzy matching.
that can be placed on different machines. For now,
we have explored the single-node configuration           2.2   Indexing operation
only, as the multi-node approach is pending on           The Elasticsearch indexing component processes
how feasible the true clustering across SLURM-           large-scale parquet datasets containing web-
managed nodes can be (4.2).                              scraped text data and transforms them into search-
                                                         able indexes. The pipeline is designed to handle
2.1   General overview of pipeline                       massive datasets while maintaining memory effi-
   • Text processing stage: Implements a multi-          ciency and enabling distributed processing.
     analyzer approach that processes the ’text’            The indexing operation begins by streaming par-
     field through different levels of linguistic pro-   quet files to prevent memory accumulation, extract-
     cessing - from heavily normalized text (lower-      ing text content along with metadata (including
     case, ASCII folding, stemming, stopword re-         URLs for provenance tracking). Each document
     moval) to minimally processed exact matches.        undergoes multi-level text processing through con-
     URL metadata is extracted and indexed for           figurable analyzers that create different searchable
     document provenance tracking. The imple-            representations - from heavily normalized text op-
     mentation is able to handle both English and        timized for semantic search to exact matches pre-
     multilingual datasets                               serving original structure.
                                                            The system employs a distributed architecture
   • Multi-field indexing strategy: Creates three        with configurable sharding and supports parallel
     searchable versions of each text document:          processing through file-range indexing, allowing
     (1) a main analyzed field optimized for full-       multiple workers to process different portions of
     text search, (2) a keyword field for exact          the dataset simultaneously. Performance optimiza-
     string matching, and (3) an exact field that        tions include bulk indexing with configurable batch
     preserves original structure while handling         sizes, and dynamic refresh interval adjustments
     HTML normalization. This enables different          to maximize throughput during large-scale opera-
     search strategies from fuzzy matching to pre-       tions.This optimization is essential due to the time
     cise phrase detection.                              and memory constraints imposed on Clariden jobs.
                                                            Advanced Elasticsearch cluster management ca-
   • Inverted index construction: Elasticsearch          pabilities enable merging of distributed indexes
     builds optimized inverted indexes mapping           through a multi-cluster approach, where individual
     each unique term to all documents contain-          data directories run separate Elasticsearch instances
     ing it, including positional information. This      that are then combined using remote _reindex op-
     enables both term-based queries (finding doc-       erations. This ensures data integrity while scaling
     uments with any search terms) and phrase-           to handle datasets that exceed single-node capacity
     based queries (finding exact word sequences),       limitations.
     with configurable relevance scoring using TF-
     IDF and BM25 algorithms.                            2.2.1 Parameters tuning
                                                         The indexing operation is based around the
   • Distributed storage and processing: The             elasticsearch.helpers.parallel_bulk func-
     system uses a N-shard configuration with no         tion, which enables concurrent bulk indexing of
     replicas for optimal indexing performance.          documents to Elasticsearch by distributing bulk re-
     Compression and refresh interval optimiza-          quests across multiple threads
     tions further enhance throughput during bulk           Performance optimization in runtime and mem-
     operations. Larger datasets and data directo-       ory usage requires careful tuning of multiple inter-
     ries are splitted, enabling parallel indexing       dependent parameters.
   The thread count is the size of the threadpool to   Fineweb CC-MAIN-2024-51 dataset (original size:
use for the bulk requests, and it should not exceed    363GB, available on Hugging Face). We report the
available CPU cores. Each thread count maintains       running time, peak memory usage, and index size
its own request queue, multiplying the memory          obtained when varying CPU thread count, chunk
usage. In most of our experimental runs, we run        size, and queue size. These results help illustrate
with --cpus-per-task=8. Hihger values improve          the trade-offs between speed, memory consump-
the parallel processing capacity.                      tion, and index size under different parallelization
   The chunk size is the number of documents           settings. We show that increasing the thread count
bundled in one bulk request to ES. A too small         and queue size generally reduces running time, but
value may imply more HTTP overhead and reduce          at the cost of significantly higher peak memory us-
throughput. A too large value will increase memory     age. Conversely, configurations with fewer threads
pressure, causing potential timeouts.                  and smaller queues yield lower memory consump-
   The max chunk bytes is the maximum size of          tion, though with longer processing times.
individual bulk requests. Larger chunks will reduce
HTTP overhead, but also require more RAM per           2.2.3   Indexing SwissAI Filtered Fineweb 2
thread.                                                        dataset
   The queue size is size of the task queue between    As the objective of this project is to develop a tool
the main thread (producing chunks to send) and         capable of analyzing and searching large-scale
the processing threads. (values tested have been       training datasets, and to apply such a tool in the
between 2 - 8)                                         context of the ongoing development of the SwissAI
                                                       large language model (LLM), we present an initial
   The parameter tuning analysis focuses on the        indexing analysis intended as a sample case study
FineWeb CC-MAIN-2024-51 2 dataset indexing             demonstrating the tool’s potential use.
operation. Computing the average size of the doc-
uments, let’s call it avg_doc_size, along with            This analysis serves as a first step towards illus-
thread_count, chunk_size and queue_size, we            trating how the tool can support the inspection and
can estimate this memory usage. For starters,          evaluation of training data in practice.
we have a first constraint on chunk_size, as           The SwissAI project has produced a filtered ver-
this is dependent on the max_chunk_size and            sion of the Fineweb 2 dataset as part of the pre-
the avg_doc_size. Therefore, the division of           training data recipe. We index pertinent sub-
these two values gives us an upper bound for           datasets of the SwissAI FineWeb 2 dataset, specif-
chunk_size.                                            ically focusing on the Italian (ita_Latn), Ger-
                                                       man (deu_Latn), Swiss German (gsw_Latn), and
                        max_chunk_size
       chunk_size ≤                              (1)   French (fra_Latn) subsets, as these correspond to
                         avg_doc_size                  the official languages of Switzerland. The sizes of
In our case, with avg_doc_size=4KB, and                these indexed datasets are: 329 GB for ita_Latn,
setting max_chunk_size to 50MB, we get                 634 GB for deu_Latn, 113 MB for gsw_Latn, and
chunk_size=12500.                                      515 GB for fra_Latn.
   The values of thread_count and queue_size              The parallel processing architecture successfully
can be guided by our desired memory usage.             indexed 1.5TB+ of multilingual web content us-
                                                       ing file range partitioning, simultaneous batch pro-
2.2.2 Tests                                            cessing, and remote reindex merging. The Ger-
We seek to gain insight into the scaling behav-        man dataset (634GB) demonstrated optimal per-
ior of the indexing process. Using the FineWeb         formance with 16-shard configuration, achieving
CC-MAIN-2024-51 dataset, we indexed portions           79.25 GB/hour throughput and nearly 8-hour total
of increasing size—2GB, 178GB, and the full            processing time. In contrast, the French dataset
363GB—and observed running times of 391s,              (515GB) suffered from suboptimal 7-shard design,
18,000s, and 31,094s respectively.                     resulting in 2.3× slower processing (34.3 GB/hour)
   Table 1 summarizes the performance metrics          and violating Elasticsearch’s 50GB/shard recom-
of different indexing configurations applied to the    mendation. Peak memory usage remained below
   2
     https://huggingface.co/datasets/HuggingFaceF      5.17GB across all operations, with batch sizes of
W/fineweb/viewer/CC-MAIN-2024-51                       100-125 parquet files proving optimal. All details
        CPUs       Chunk size   Thread count       Queue size    Running time    Peak memory      Index size
                                                                           (s)          (GB)          (GB)
             8          12500               2              2           34.634            1.55        612.01
             8          12500               4              2           33.704            2.81        595.60
             8          12500               4              4           31.427            2.59        621.69
             8          12500               4              8           34.433            3.32        615.14
             8          12500               8              8           31.094            3.76        604.31
            16          12500              16              4           33.227            7.79        607.59

  Table 1: Performance metrics of runtime and peak memory usage for various index parameters configurations


can be found in Table 2. The indexing parame-              Regarding production deployment enhance-
ters used for all these indexing operation was the      ments, enabling the memory mapping functionality
optimal configuration found in 2.2.1.                   (as discussed in 4.1.2) would provide for enhanced
   The indexing pipeline utilized optimized param-      performance. Additionally, managing parallel job
eters derived from systematic tuning, including:        submissions in SLURM through automated array
custom text analyzers, compressed storage with          job would prove useful.
best_compression codec and disabled refresh                An ablation regarding the memory usage scenar-
intervals during bulk indexing.                         ios for different total memory allocation strategies
   This architecture successfully indexed over
                                                        2.3     Search operation
1.5TB of multilingual web content while main-
taining sub-6GB memory footprints per process,          The Elasticsearch search component provides
demonstrating the viability of Elasticsearch for        a comprehensive query execution framework
large-scale document retrieval systems in resource-     designed to perform diverse search operations
constrained environments.                               on large-scale indexed web content. The system
                                                        enables systematic exploration of massive text
2.2.4   Upper limit of indexable information            corpora through multiple search strategies, each
With the current achieved optimization, the practi-     optimized for different information retrieval
cal upper limit for single batch-processings appears    scenarios.
to be approximately around 500GB. (respecting
Clariden’s job time limit).                                In the current set-up, the search system takes
   Regarding ElasticSearch’s shard constraints, it      predefined collections of search terms provided by
imposes fundamental limitations on index scala-         a user (such as misinformation keyword lists or
bility, with a maximum number of documents per          domain-specific vocabularies in our test case) and
shard ( 2.1 billion) and a recommended shard size:      executes queries for each term against the com-
50GB maximum, 200M documents optimal                    plete indexed dataset. This systematic approach
                                                        processes entire keyword files containing hundreds
2.2.5   Improvements
                                                        or thousands of terms, ensuring exhaustive cover-
   • Dynamic sharding configuration to achieve          age across millions of documents. The pipeline
     optimal data distribution per shard based on       handles high-volume query execution through op-
     dataset characteristics                            timized connection management and configurable
                                                        timeouts designed for large-scale index operations.
   • Adaptive chunk sizing in parallel batch pro-
                                                        Beyond returning simple hit counts, the pipeline ex-
     cessing operations to optimize the balance
                                                        tracts highlighted text snippets from matching doc-
     between maximum chunk size and average
                                                        uments, capturing the actual context where search
     document size
                                                        terms appear. This enables us to examine not only
   • Chunk size parameter tuning to determine op-       whether specific content exists within the corpus,
     timal values for maximum chunk bytes based         but also how terms are used, what surrounding con-
     on dataset characteristics in single-process       text they appear in, and how meaning varies across
     jobs                                               different documents and sources.
                                                        The system tracks query execution times, hit dis-
   • Resource monitoring for memory usage and           tributions, and relevance scoring. This monitoring
     bandwidth utilization to optimally adjust          reveals which query types work best for specific
     queue size and thread count parameters             content domains and helps identify optimal search
                 Table 2: Elasticsearch Indexing Performance for FineWeb Dataset Languages

 Dataset    Original Size   Parquet Files   Batch    Peak Memory    Execution Time    Index Size   Merge Time
                   (GB)          (Total)     Size           (GB)          (seconds)        (GB)     (minutes)
                                              125            2.38             5587         95.1
                                              125            2.74             5332        101.2
                                              125            2.84             5402         82.1
                                              125            3.56             5142         85.0
 deu_Latn            634             994                                                                379.8
                                              125            3.11             2819         61.0
                                              125            1.42             1410         18.6
                                              124            2.22             1572         23.4
                                              124            1.52             1298         17.0
                                              100            4.43            14859          70.0
                                              100            5.17            20371          69.2
                                              100            4.42            15014          69.0
                                               98            4.41            11774          59.8
 fra_Latn            515             785                                                                571.4
                                               98            4.00             5775          36.2
                                               98            2.61             2480          21.0
                                               98            2.06             2152          17.8
                                               93            1.55             1040          9.1*
 ita_Latn            329             486    Single           3.94            17148        213.0             –
 gsw_Latn          0.113               1    Single           1.92            25.48          0.35            –



approaches for different research objectives. The         This preprocessing significantly affects how
relevance scoring uses BM25 (Best Matching 25)            queries match against indexed content.There is
as its default algorithm, which is an improved ver-       also a exact_match_analyzer available, which
sion of TF-IDF that addresses the saturation prob-        does not perform ascii folding, stop word removal
lem where term frequency has diminishing returns          or stemming in order to identify pure verbatim.
and incorporates document length normalization.
BM25 calculates relevance scores by combining
                                                            The match query match_query implements OR
term frequency (how often query terms appear in a
                                                         logic between terms, applying full-text analysis to
document), inverse document frequency (how rare
                                                         both query and indexed content. For single-word
terms are across the corpus), and document length
                                                         queries like “climate,” the term is analyzed and
normalization.
                                                         stemmed to “climat,” which matches documents
2.3.1 Type of queries possible                           containing variations like “climate,” “climates,” or
The index uses a web_content_analyzer that ap-           “climatic.” BM25 scoring is used for relevance
plies:                                                   ranking. For multi-word queries such as “climate
                                                         change,” each word is analyzed separately, result-
   • HTML stripping: Removes HTML tags from              ing in a query for “climat” OR “chang.” Documents
     content                                             need to contain only one of the terms to match, and
                                                         word order is irrelevant; “change climate” yields
   • Standard tokenization: Splits text into tokens      the same results. Documents containing both terms
   • Lowercase normalization: Converts all text to       receive higher relevance scores.
     lowercase                                              The match phrase query match_phrase_query
                                                          requires exact phrase matching, with configurable
   • ASCII folding: Converts accented characters          proximity tolerance. For single-word queries, it
     (é e)                                                behaves like the match query. For multi-word
   • English stop word removal: Removes com-              queries like “climate change,” the terms must ap-
     mon words (the, and, of, etc.)                       pear in the exact order after analysis. For exam-
                                                          ple, “climat” must immediately precede “chang”
   • English stemming: Reduces words to root              when the slop is 0, preserving phrase integrity. The
     forms (running run, climates climat)                 MATCH_PHRASE_SLOP parameter controls tolerance
for word proximity; slop 0 enforces exact match-        Query     Avg (ms)   Med (ms)     Std (ms)   Hit Rate (%)
ing, slop 1 allows one intervening word, and slop       Length
2 allows two. This means slop 1 can match “cli-
mate and change,” while slop 2 can match “climate       1 word     36.07       27.87       41.09         98.7
action and change.”                                     10         15.01        7.30       14.73         100.0
   The term query exact term_query_exact by-            words
passes text analysis entirely, searching for exact
                                                        100        55.51       40.86       35.64         100.0
tokens using the text.exact field. For single-word      words
queries, no stemming or analysis is applied, so
searching for “climate” only finds the exact token      300        100.51      105.50      20.52         99.5
                                                        words
“climate,” excluding variations like “climates” or
“climatic.” This is useful for exact word forms,       Table 3: Query performance statistics across different
proper nouns, or technical terms. Term queries         segment lengths for the GSW index. Results show aver-
do not support multi-word inputs and will return       age (Avg), median (Med), and standard deviation (Std)
empty results for such cases, as they operate on       of query execution times, plus hit rates indicating suc-
single tokens only.                                    cessful query matches.
   The fuzzy query fuzzy_query handles typo-
graphical errors and variations through edit dis-
                                                          To this end, we sampled random contiguous
tance calculations. For single-word queries, it uses
                                                       segments of varying lengths (1, 10, 100, and 300
Levenshtein distance to find similar terms within a
                                                       words) from the source datasets used to build the
tolerance, typically allowing one or two character
                                                       indexes. These segments were then issued as match
edits. For example, searching for “climat” could
                                                       phrase queries against the corresponding indexes.
match “climate” or “climax” if within tolerance.
                                                          Table 3 summarizes the query performance re-
Text analysis still applies. For multi-word queries,
                                                       sults. For the GSW index, the hit rate remains
the system falls back to a multi-match query with
                                                       consistently high across all segment lengths, rang-
fuzziness enabled per term, using AND or OR op-
                                                       ing from 98.7% for 1-word queries to 100% for 10-
erators. This approach is more computationally ex-
                                                       and 100-word queries, and 99.5% for 300-word
pensive and can match inputs like “changge” with
                                                       queries. Query execution times exhibit the ex-
“change” or “cliamte” with “climate.”
                                                       pected trend of increasing with segment length:
   The boolean must query bool_must_query cre-
                                                       median query times range from approximately 7
ates structured boolean queries with configurable
                                                       ms for 10-word queries to 105 ms for 300-word
logic and scoring control. For single-word queries,
                                                       queries. The standard deviation of execution time
it creates a single must clause, similar to a match
                                                       also generally increases with query length, though
query with the AND operator but allowing com-
                                                       the 300-word queries display a relatively stable la-
plex scoring. For multi-word queries, it creates
                                                       tency (standard deviation of 20.52 ms), suggesting
separate match clauses where all terms must be
                                                       that longer phrases may incur a more predictable
satisfied, up to a configurable maximum (default
                                                       computational cost within this small index.
is three terms). The BOOL_MUST_OPERATOR param-
                                                          Overall, these preliminary results indicate that
eter controls term relationships, where “and” re-
                                                       match phrase queries can be executed with low la-
quires all terms and “or” allows partial matches
                                                       tency on smaller indexes even for longer segments,
with minimum_should_match . This provides fine-
                                                       supporting the feasibility of this method as part
tuned control over precision and recall.
                                                       of a toolset for detecting potential memorization.
2.3.2   Verbatim query length search time              Further experimentation on larger indexes and ad-
The purpose of this experiment is to evaluate the      ditional languages will be required to fully charac-
performance of match phrase queries when applied       terize performance and accuracy under conditions
to an index with varying query segment length.         representative of production-scale language model
Specifically, this experiment seeks to explore the     training datasets.
feasibility of using verbatim phrase matching as
                                                       3   Search results on SwissAI training data
a method for detecting potential memorization
and regurgitation of training data passages by the     We present an initial analysis intended as a sample
model.                                                 case study demonstrating the tool’s potential use.
This analysis serves as a first step towards illus-    GPT generated list of misinformation keywords
trating how the tool can support the inspection and    (see Table 6)
evaluation of training data in practice.                  Further more extensive will results will be avail-
                                                       able on the HEVS Github elasticsearch_alps
3.1     SwissAI FineWeb-2 Dataset                      repository.
On the German, French, Swiss German and Italian
datsets from FineWeb-2, indexed in 2.2.3, we           4       Deployment on ALPS Clariden -
conduct searches using the Weaponized Words                    Technicalities
dictionary 3 , which provides language-specific        This project has been deployed on Clariden, a
lexicons of curse words, slurs, and other forms of     vcluster within the Alps system of the CSCS, the
toxic or discriminatory language. The motivation       Swiss National Supercomputing Centre 5 . The de-
behind this analysis is to explore the presence and    ployment process has revealed several technical
distribution of potentially harmful or offensive       challenges stemming from the platform’s specific
terms within the SwissAI filtered training data, and   container management approach and security con-
to validate our experimental pipeline. An example      straints.
of the result of queries of the german lexicon of
WeaponizedWords on the DEU index is Table 5.           4.1      Container environment
                                                       Clariden provides its own container environment
  Here is the query configuration used for all 4 in-   through the Container Engine (CE), which is specif-
dexes to perform the queries on WeaponizedWords:       ically designed for HPC workloads and does not
                                                       support Docker directly. Docker is incompatible
{                                                      with Clariden due to two primary constraints: secu-
        " execute_match_query ": true ,
        " execute_match_phrase_query ": true ,         rity concerns arising from Docker’s default shared
        " execute_term_query_exact ": true ,           read/write permissions for all users (rather than
        " execute_wildcard_query ": false ,            inheriting permissions from the user who initi-
        " execute_fuzzy_query ": true ,
        " execute_bool_must_query ": true ,            ated the container), and architectural incompat-
        " match_query_operator ": [                    ibility, as most Docker containers are built for
             " or "
        ],
                                                       x86/x86_64/amd64 architectures rather than the
        " match_phrase_slop ": [                       arm64 architecture used by Clariden.
             0
        ],                                             4.1.1 Docker incomptability
        " bool_must_operator ": " or " ,
        " bool_must_max_words ": 3,                    Since Clariden does not support the direct use of
        " bool_must_minimum_should_match ": "          Docker, we cannot directly pull and use the offi-
             50% "                                     cial Elasticsearch image from Docker Hub6 . This
}
                                                       also precludes the use of Docker Compose, which
                                                       would have provided significant benefits for or-
3.2     SwissAI FineWeb-edu-score 2 dataset            chestration by allowing us to compose existing ele-
We index all of the SwissAI Fineweb-edu-score 2        ments with ease—for example, combining an ex-
dataset. The dataset has undergone some filtering      isting Elasticsearch container with storage blocks
process, and is composed of 95 MAIN-CC dumps.          and Python code in separate containers. Docker
As illustrated with the previous SwissAI FineWeb-      Compose facilitates problem isolation to individual
2 dataset, we perform parallel processing of the       containers and simplifies component updates and
95 dumps simultaenously, which render 95 source        upgrades by allowing modular changes to specific
indexes. For these indexes, at the time of writing     parts of the deployment. This limitation means
of the raport, subsequent merge stages to obtain a     we cannot directly use the official Docker Hub im-
unique final index are still ongoing. We randomly      age for Elasticsearch7 , which introduces additional
sample 3 source indexes among these 95 to perform      complexity in building, customizing, and deploying
search queries upon WeaponizedWords (visible in        the container. The process requires creating custom
Table 7), a list of Obscene Words 4 , and a Chat-      OCI-compliant container images using Podman
    3                                                      5
    https://weaponizedword.org/                              https://www.cscs.ch/computers/alps
    4                                                      6
    https://github.com/LDNOOBW/List-of-Dirty-Nau             https://hub.docker.com/_/elasticsearch
                                                           7
ghty-Obscene-and-Otherwise-Bad-Words                         https://hub.docker.com/_/elasticsearch
 Index (Size)        Query Type               Avg Time (ms)       Med Time (ms)       Avg Hits     Total Queries
                     match_query                      10.75                7.61         210.02               53
                     match_phrase_query               10.71                7.84          21.34               53
 GSW (389MB)         term_query_exact                  5.74                4.75          14.68               53
                     fuzzy_query                      38.45               35.00         520.35               52
                     bool_query                        9.46                7.46         210.02               53
                     match_query                     185.49              136.95        7754.94               53
                     match_phrase_query               86.62               51.56        7590.21               53
 DEU (400GB)         term_query_exact                177.06              198.71        5290.13               53
                     fuzzy_query                    3462.92             3586.34        8636.56               52
                     bool_query                       76.97               51.94        7754.94               53
                     match_query                     191.45              120.03        9162.91               75
                     match_phrase_query              193.11               56.44        7607.07               75
 FRA (313GB)         term_query_exact                106.85              135.62        4479.76               75
                     fuzzy_query                    2055.44             2333.66        9382.21               57
                     bool_query                       71.87               53.14        9162.91               75
                     match_query                     156.42              100.78        7359.83               24
                     match_phrase_query               70.93               31.80        5887.25               24
 ITA (196GB)         term_query_exact                108.91              112.44        5276.42               24
                     fuzzy_query                    1175.49             1187.93        8754.60               20
                     bool_query                       41.80               32.01        7359.83               24

Table 4: Query performance comparison across language indexes (and their index size). Metrics include average
and median query times (ms), average hits per query, and total queries executed. Queries done in the respective
language WeaponizedWords dataset.


and Containerfile, ensuring that components inte-        configuration through command-line parameters
grate correctly with Clariden’s resource manage-         or configuration files. This limitation necessitates
ment and security policies. Furthermore, efficient       passing critical Elasticsearch settings as command-
resource utilization is critical—workloads must be       line arguments during container startup, although
registered within SLURM job windows, and since           this can be partially mitigated by using SLURM
Alps is an extremely efficient computing platform        files tht register such arguments
designed for high-performance computing, compo-             A major system-level constraint is the memory
nents must be compiled against optimized libraries       mapping limitation. Elasticsearch relies on mem-
before being run at scale to maintain the platform’s     ory mapping (mmap) for efficient index access, re-
performance standards.                                   quiring the kernel parameter vm.max_map_count
                                                         to be set to at least 262,144. However, Clariden’s
4.1.2 Custom container image construction
                                                         default value is 65,530, and unprivileged containers
Following the CSCS Documentation, 8 , we must            cannot modify kernel parameters. Without proper
build custom OCI-compliant container images us-          configuration, Elasticsearch fails during startup
ing Podman and Containerfile. This one will in-          with:
clude a certain version of Elasticsearch, the cor-
                                                               bootstrap check failure [1] of [1]:
responding Elasticsearch API, and the necessary                    max virtual memory areas vm .
extra tools like curl, pyarrow, python3 and so on.                 max_map_count [65530] is too low
   Following, the Environment Definition File                      , increase to at least [262144]
(EDF), a text file in the TOML format, represents        We resolve this by disabling memory mapping en-
the creation of a computing environment based on         tirely using:
such container image. Environment variables de-
                                                               node . store . allow_mmap = false
fined in TOML files are not properly interpreted
by Elasticsearch during startup, requiring runtime       This solution enables Elasticsearch to run but
   8
     https://confluence.cscs.ch/spaces/KB/pages/8        introduces performance implications such as
68834153/Building+container+images+on+Alps               reduced I/O performance, as without memory
 Query Type           Score        Snippet (with URL)
 match_query          21.066      Halt Die Fresse "Halt die Fresse!" Dann halt die Fresse. Was machen die da. Halt Die Fresse
                                  nicht buchen. - Halt die fresse! Namensräume Artikel Diskussion. (https://neocarla.com/a
                                  ktuelle-nachrichten-welt/halt-die-fresse.php)
                      20.764      Daraus folgt: Halt die Fresse! Antwort: Halt die Fresse! Halt die Fresse! - Stimmt tatsächlich,
                                  echt schönes Wetter heute! Schönen Tag noch! Antwort: Halt die Fresse! Halt die Fresse! Halt
                                  die Fresse! - Ja, ich weiß. Sie hat mir heute davon erzählt, aber sie war davon nicht so begeistert.
                                  (http://kamelopedia.net/wiki/Halt_die_Fresse)
                      20.744      Das war wie ein Schlag in die Fresse. Nur halt ins Herz. wie ein schlag in die fresse, nur ins herz
                                  -.- Hauptschule: "Halt die Fresse!" Realschule: "Halt die Fresse!" Gymnasium Wäre dein Herz
                                  geborchen, wärst du Tot. Also halt die Fresse! Junge: Ach H Starrt sie auf dein Mund dann küss
                                  sie.. HALT DIE FRESSE ICH HÖR AUF Irgendwann schlag ich Dir in die Fresse. Versprochen!
                                  ;D (https://www.spruchmonster.de/das-war-wie-ein-schlag-die-fresse-nur-hal
                                  t-ins-herz)
                      20.568      Bewertung, Halt die Die Geschichte Rapper Toony, dessen Beitrag für Halt die Fresse man
                                  auch diese Informationen hilfreich. Halt die Fresse man. Halt Die Fresse Man Translations &
                                  Examples VideoOidorno - Halt die Fresse ich will saufen (Official Video) Halt Die Fresse Man
                                  Inhaltsverzeichnis VideoHDF Halt Die Fresse Man "Halt die Fresse!" (https://ebony-anal.
                                  com/syrien-nachrichten/halt-die-fresse-man.php)
                      20.368      HDF, Halt die FresseHalt deine Fresse. Mir kamen Tränen in die Augen und er meinte nur Halt
                                  die Fresse und 3. Juni 2015. Einen Beutel mit dem Aufdruck Halt die Fresse verschicken Sie mit
                                  Sticker und Konfetti. (http://arrestmorning.live/halt-die-fresse-ich-liebe-dich/)
 match_phrase_query   20.990       Übersetzung im Kontext von "halt die Fresse" in Deutsch-Englisch von Reverso Context: Halt
                                   die Fresse, Jackie Boy. Halt Die Fresse "Halt die Fresse!" Als Halt Die Fresse - Navigation-
                                   smenüAmazon Web Services Cloud Computing Dienste von Amazon. Halt Die Fresse nicht
                                   buchen. - Halt die fresse! (https://neocarla.com/aktuelle-nachrichten-welt/halt-d
                                   ie-fresse.php)
                      20.741       Daraus folgt: Halt die Fresse! Antwort: Halt die Fresse! Halt die Fresse! - Stimmt tatsächlich,
                                   echt schönes Wetter heute! Schönen Tag noch! Antwort: Halt die Fresse! Halt die Fresse! Halt
                                   die Fresse! - Ja, ich weiß. Sie hat mir heute davon erzählt, aber sie war davon nicht so begeistert.
                                   (http://kamelopedia.net/wiki/Halt_die_Fresse)
                      20.344       Übersetzung im Kontext von "halt die Fresse" in Deutsch-Englisch von Reverso Context: Halt
                                   die Fresse, Jackie Boy. Halt Die Fresse Man Translations & Examples VideoOidorno - Halt die
                                   Fresse ich will saufen (Official Video) Halt Die Fresse Man Inhaltsverzeichnis VideoHDF Halt
                                   Die Fresse Man "Halt die Fresse!" (https://ebony-anal.com/syrien-nachrichten/hal
                                   t-die-fresse-man.php)
                      20.280       Komm halt die Fresse FRÜHER warst du ein guter Freund. sein; aber nein es heißt ja Hauptschule:
                                   "Halt die Fresse!" Realschule: "Halt die Fresse!" (https://www.spruchmonster.de/und-d
                                   u-sollst-ein-guter-freund-sein-und-immer-fuer-mich-da-gewessen-seinkomm-h
                                   alt-die-fresse)
                      20.016       Tasse Ich bin der Boss - Halt die Fresse! Product.Nr. cup_kn_ibdb product description Tasse
                                   Knorkator "Ich bin der Boss - Halt die Fresse!" die Fresse! (https://www.fantotal.de/en/k
                                   norkator-shop/jewelry/tasse-knorkator-ich-bin-der-boss-halt-die-fresse.ht
                                   ml)

Table 5: Example of output of DEU index with ’halt die fresse’ query from WeaponizedWords. Top 5 hits per query
type (cleaned snippets, URL at end of snippet).


mapping, disk I/O operations become less efficient,          search bundles its own optimized OpenJDK distri-
potentially increasing query response times and              bution and the bundled JVM is specifically tuned
indexing throughput limitations. There is also an            for Elasticsearch’s performance characteristics, and
increased memory usage, as alternative memory                the host Java installations may be incompatible
management strategies consume more RAM and                   with containerized Elasticsearch requirements.
scalability considerations, as these performance                The conflict manifests as:
impacts may become more pronounced as data                          warning : ignoring JAVA_HOME =/ usr /
volume and concurrent operations increase.                              lib64 / jvm / java -11 - openjdk -11;
                                                                        using bundled JDK
                                                                    could not find java in JAVA_HOME at
   Containers launched on Clariden inherit envi-                        / usr / lib64 / jvm / java -11 - openjdk
ronment variables from the host system, including                       -11/ bin / java
JAVA_HOME, which may be set by system config-
                                                             We resolve this by explicitly managing the Java
urations as pointing to cluster-managed Java in-
                                                             environment within the container:
stallations. This creates conflicts because Elastic-
 Query Type           Score       Snippet (with URL)
 match_query          25.438      No, there’s clear evidence that the MMR (measles, mumps, rubella) vaccine does not cause autism.
                                  | vaccines (but not MMR), caused autism. | More recently, some parents have been concerned
                                  that too many vaccines given too soon might cause autism. (https://www.babycenter.com/4
                                  04_does-the-mmr-vaccine-put-my-child-at-greater-risk-for-autism_11518.bc)
                      25.437      Many proponents of the idea that vaccines cause autism have a habit of shifting between
                                  variants of the autism / vaccine theory without a lot of thought | It seems that they don’t care
                                  about exactly how vaccines cause autism, as long as they do. | that is caused by vaccines.
                                  (http://www.aconversationonautism.com/Vaccines-and-Autism/Vaccines-Autism-G
                                  enerally/Logical-Problems-with-the-Arguments/Theory-Shifting)
                      25.306      cause autism. | Brian Hooker PhD, linking vaccines as a plausible cause of autism. | in the cause
                                  of autism Dr. (http://vaccinationdecisions.net/vaccines-and-autism/)
                      25.301      The belief that vaccines cause autism is not just wrong, but damaging. | Also, the component in
                                  vaccines that is "causing autism," hasn’t been in vaccines since the 90s. | Furthermore, if you
                                  believe that vaccines cause autism, the only way a vaccine could cause autism is if the disease
                                  that the child is being vaccinated (http://www.debate.org/opinions/are-vaccines-cau
                                  sing-autism)
 match_phrase_query   23.401      Japanese Data Show Vaccines Cause Autism June 3, 2009 Just months following the US Court
                                  of Federal Claims rejection of the claim that the MMR vaccine causes autism, here you will see
                                  data from formal peer refereed medical papers showing that vaccines caused autism in Japanese
                                  children and will be doing (http://recoveringnicholas.com/2010/02/13/japanese-dat
                                  a-show-vaccines-cause-autism/)
                      23.196      Does Thimerosal used in vaccines cause Autism? 2. Does the MMR vaccine cause autism? 3. |
                                  Does the combination of Thimerosal-containing vaccines and the MMR vaccine cause autism?
                                  (http://spiriteddoula.blogspot.com/2009/02/vaccine-court-to-release-autis
                                  m-ruling.html)
                      22.865      May 13, 2008 WASHINGTON (AP) — Parents claiming that childhood vaccines cause autism
                                  should not be rewarded by the courts when the scientific community | Court of Claims alleging
                                  that vaccines caused autism and other neurological problems in their children. | Lawyers for
                                  the families are presenting three different theories of how vaccines caused autism. (http:
                                  //www.infowars.com/families-make-case-for-vaccine-link-to-autism/)
                      22.754      Do Vaccines Cause Autism? Our crack team of scienticians have investigated. Read on for the
                                  full report. Q: Do vaccines cause autism? A: No. (http://blog.westandfirm.org/2008/06
                                  /change-of-pace.html)
                      22.719      The special "vaccine court" ruled yesterday, in three separate cases, each of which was testing
                                  a different strategy for claiming that vaccines cause autism | , that there was no evidence that
                                  vaccines caused autism in any of the cases. | The judges rule against the notion that MMR
                                  vaccine causes autism, and against the notion that thimerosal used as a preservative in vaccines
                                  causes autism (http://genome.fieldofscience.com/2009/02/special-court-rules-t
                                  hat-vaccines-are.html)

Table 6: Example of output of FineWeb-edu-score-2 index with "vaccines cause autism" query from misinformation
dataset. Top 5 hits per query type (cleaned snippets, URL at end of snippet).


      unset JAVA_HOME
      export ES_JAVA_HOME ="/ usr / share /
          elasticsearch / jdk "
                                                               Firstly, Elasticsearch requires specific network
                                                            configuration to operate properly. In a basic
This ensures Elasticsearch uses its bundled, tested         setup, Elasticsearch uses two types of network
JDK while avoiding conflicts with host system Java          communication: the HTTP interface (default port
configurations.                                             9200) for client requests like searches and data
4.2   Networking settings                                   ingestion, and the transport interface (default port
                                                            9300-9400) for internal node-to-node commu-
When implementing Elasticsearch within container-           nication. Each node has two different network
ized environments on the CSCS Alps Clariden clus-           interfaces - clients send requests to Elasticsearch’s
ter, to execute indexing and search operations , we         REST APIs using its HTTP interface, while
may encounter network binding configuration is-             the transport interface is used for inter-node
sues, such as the                                           communication in multi-node clusters and for
Connection error : HEAD http :// localhost                  internal component coordination and specialized
    :9200/ [ status :400]
                                                            client connections even in single-node setups. By
which bring forward the necessity to configure              default, Elasticsearch binds only to ‘localhost‘
specific host and port variables.                           (127.0.0.1), which means it cannot be accessed
Query        Score     Snippet (with URL)
Type
match        28.392   What is a transtrender? Binary trans people expose "transtrenders" on Youtube. Transtrending is gatekeeping (https:
                      //www.beyounetwork.org/articles/transtrending-what-it-means-and-how-it-harms)
             27.149   Transtrenders never experience dysphoria or oppression, often identify as "otherkin." They are gender-conforming cisgender
                      people pretending to be transgender (https://www.urbandictionary.com/author.php?author=transapple)
             26.210   Body dysphoria separates true transsexuals from "transtrenders." In the truscum worldview, true transsexuals deserve priority
                      over transtrenders (https://transblog.grieve-smith.com/2015/01/)
             25.143   Transtrend aims to contribute to well-functioning markets. Transtrend promotes balance between supply and demand (https:
                      //www.transtrend.com/en/approach/responsible-investing/)
             25.085   A "transtrender" refers to a person who identifies as transgender because they think it’s cool to do so. There’s a lot of problematic
                      implications that go with the term "transtrender." "Transtrender" is a word no person in this community should ever use or
                      condone. (https://letsqueerthingsup.com/2015/03/28/why-the-trans-community-needs-to-ban-the-word-tra
                      nstrender-for-good/?like_comment=2496&_wpnonce=108d059f06)
match_phrase 28.392   What is a transtrender? Among (binary) trans people on Youtube, you can find reaction videos exposing "transtrenders" or
                      video opinions on "transtrending". What binary trans people need to understand about transtrending Binary trans people need to
                      understand that transtrending is gatekeeping (https://www.beyounetwork.org/articles/transtrending-what-it-means
                      -and-how-it-harms)
             27.149   Transtrenders never experience disphoria transphobia or opression, and often identify as "otherkin." Transtrenders are basically
                      gender-onforming cisgender people pretending to be transgender and using different pronouns because they think it makes them
                      (https://www.urbandictionary.com/author.php?author=transapple)
             26.210   the word is adopted as a badge of pride by many people who espouse it), the feeling of body dysphoria separates the true
                      transsexuals from the wannabe "transtrenders" truscum worldview, resources available for trans people are scarce, and the true
                      transsexuals with their medical condition deserve priority over the transtrenders (https://transblog.grieve-smith.com/2
                      015/01/)
             25.143   Transtrend aims to contribute to well-functioning, well-organized and reliable markets. Transtrend – and its clients – must
                      therefore be prepared to take risks. Transtrend aims to promote a healthy balance between supply and demand. (https:
                      //www.transtrend.com/en/approach/responsible-investing/)
             25.085   A "transtrender" refers to a person who identifies as transgender because they think it’s cool to do so. There’s a lot of problematic
                      implications that go with the term "transtrender." "Transtrender" is a word no person in this community should ever use or
                      condone. (https://letsqueerthingsup.com/2015/03/28/why-the-trans-community-needs-to-ban-the-word-tra
                      nstrender-for-good/?like_comment=2496&_wpnonce=108d059f06)
fuzzy        22.905   Trans people who long for the days where transition and dysphoria were treated seriously have coined these new invaders
                      as "transtrenders," with the implication These new additions seem to only cause confusion amongst the general public who
                      historically have viewed transgenderism as indicative of a gender transition (https://thepostmillennial.com/transtrend
                      er-craze-trans-people)
             21.260   Transtrend aims to contribute to well-functioning, well-organized and reliable markets. Transtrend – and its clients – must
                      therefore be prepared to take risks. Transtrend aims to promote a healthy balance between supply and demand. (https:
                      //www.transtrend.com/en/approach/responsible-investing/)
             20.861   transgender issues extensively, also looks at mental health issues in the bisexual and transger communities, and contains
                      information on bisexuality and transgernderism and particularly the common ground between the bisexual and transgender
                      communities (http://www.pinktherapy.com/en-gb/knowledge/bisexual.aspx)
             20.717   transgender issues extensively, also looks at mental health issues in the bisexual and transger communities, and contains
                      information on bisexuality and transgernderism and particularly the common ground between the bisexual and transgender
                      communities (http://www.pinktherapy.com/en-gb/knowledge/bisexual.aspx)
             20.139   That being said, pretending to be a female is unlikely a sexual strategy due to a very low prevalence rate of transgenderism of
                      0,001% Many transgenders appear to use the protected class status of transgenderism as a means of status ascension (transtrender)
                      (https://incels.wiki/w/Sneaker_male)
bool_must    56.784   What is a transtrender? Among (binary) trans people on Youtube, you can find reaction videos exposing "transtrenders" or
                      video opinions on "transtrending". What binary trans people need to understand about transtrending Binary trans people need to
                      understand that transtrending is gatekeeping (https://www.beyounetwork.org/articles/transtrending-what-it-means
                      -and-how-it-harms)
             54.298   Transtrenders never experience disphoria transphobia or opression, and often identify as "otherkin." Transtrenders are basically
                      gender-onforming cisgender people pretending to be transgender and using different pronouns because they think it makes them
                      (https://www.urbandictionary.com/author.php?author=transapple)
             52.420   the word is adopted as a badge of pride by many people who espouse it), the feeling of body dysphoria separates the true
                      transsexuals from the wannabe "transtrenders" truscum worldview, resources available for trans people are scarce, and the true
                      transsexuals with their medical condition deserve priority over the transtrenders (https://transblog.grieve-smith.com/2
                      015/01/)
             50.286   Transtrend aims to contribute to well-functioning, well-organized and reliable markets. Transtrend – and its clients – must
                      therefore be prepared to take risks. Transtrend aims to promote a healthy balance between supply and demand. (https:
                      //www.transtrend.com/en/approach/responsible-investing/)
             50.170   A "transtrender" refers to a person who identifies as transgender because they think it’s cool to do so. There’s a lot of problematic
                      implications that go with the term "transtrender." "Transtrender" is a word no person in this community should ever use or
                      condone. (https://letsqueerthingsup.com/2015/03/28/why-the-trans-community-needs-to-ban-the-word-tra
                      nstrender-for-good/?like_comment=2496&_wpnonce=108d059f06)

            Table 7: Example of output of FineWeb-edu-score-2 index with ’transtrenders’ query from WeaponizedWords. Top
            5 hits per query type (cleaned snippets, URL at end of snippet)


            remotely - this is a security feature.                           patibility with Elasticsearch’s default networking
                                                                             behavior, manifested as
                                                                              Connection error : HEAD http :// localhost
              This HPC architecture creates a critical incom-                     :9200/ [ status :400]
The error occurs perhaps because Alps                  scripts should be consolidated into a centralized en-
compute nodes route HTTP traffic through               vironment variable management system that can dy-
proxy.cscs.ch:8080. The proxy may intercept            namically tune heap sizes, thread pools, and buffer
localhost requests and add headers incompatible        settings based on SLURM resource allocations
with Elasticsearch’s REST API, despite localhost       (SLURM_MEM_PER_NODE, SLURM_CPUS_PER_TASK).
being in the noproxy list. This issue can happen for   This would transform the current single-node bot-
a variety of different reasons (container networking   tleneck into a scalable, SLURM-native distributed
complications, application level proxy settings,       Elasticsearch cluster capable of parallel indexing
namespace ambiguity), but further investigation        across multiple compute nodes.
is required to clarify exactly the cause of this
misbehavior, which is why this point is being          5   Comparison to other methods
clarified with CSCS engineers as of the moment of
                                                       Bloom filters may offer a significantly improve-
the report writing.
                                                       ment in indexing speed compared to ES, as among
   The solution requires explicit network configu-     other factors they do not build any complex struc-
ration that bypasses the proxy and forces localhost-   tures, just bit arrays. However, they present severe
only binding: first, configure proxy bypass with:      limitations in their search capabilities: they can
      export no_proxy ="${ no_proxy                    only perform membership testing, quickly resolv-
          } ,127.0.0.1 , localhost "
      export http_proxy ="" `
                                                       ing if a term definitely doesn’t exist in a dataset
      and use ` curl -- noproxy " 127.0.0.1 " `        (no false negatives) or might exist (possible false
            for all local API calls                    positives). They are therefore extremely memory-
                                                       efficient for large text corpora but are only use-
   second, explicitly bind all Elasticsearch network
                                                       ful when one needs a fast "does this term appear
interfaces to localhost using:
                                                       anywhere?" check. They have no storage of the
      -E   network . host =127.0.0.1                   document IDs, the term positions, frequencies, or
      -E   http . host =127.0.0.1
      -E   transport . host =127.0.0.1                 actual content. Consequently, they cannot resolve
      -E   network . bind_host =127.0.0.1              questions such as: which documents contain the
      -E   network . publish_host =127.0.0.1
                                                       term?, where in documents do these terms appear?,
  and third, disable cluster discovery with:           how many times do these terms occur (ranking and
                                                       frequency information), are there any term rela-
       -E discovery . type = single - node
                                                       tionships or proximity? (phrase matching) and so
To comply with SLURM’s job isolation model.            on.
This configuration is architecturally mandated by         Infinigram is a Burrow-Wheeler Transform-
the intersection of Alps’ proxy-mediated network-      based method, based on the order permutation to
ing and SLURM’s resource management, making            create an implicit pointer-based index. It gener-
it the only viable approach for successful Elastic-    ally enablew fast substring and n-gram matching
search deployment in this specialized HPC environ-     across massive text corpora using pure lexical pat-
ment.                                                  tern matching, without any semantic understanding
                                                       or meaning-based search capabilities. It operates
4.3   Future directions in technical deployment        solely on exact character sequences and n-gram
The current Elasticsearch implementation is lim-       patterns without supporting boolean operators like
ited to single-node clusters (discovery.type=single-   AND, OR, or NOT. In comparison, ElasticSearch
node) which prevents horizontal scaling across         has the capability to implement semantic-search
SLURM’s multi-node allocations and signifi-            and complex boolean queries that allow for a wider
cantly constrains indexing performance. To op-         variety of search operations.
timize for SLURM workloads, the cluster setup
should leverage SLURM environment variables            References
like SLURM_NODELIST and SLURM_JOB_NODELIST
to automatically configure proper cluster discovery    Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed
                                                        Awadallah, Ammar Ahmad Awan, Nguyen Bach,
with seed hosts, enabling true distributed index-       Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat
ing. Additionally, the numerous scattered Elas-         Behl, Alon Benhaim, Misha Bilenko, Johan Bjorck,
ticsearch configuration parameters throughout the       Sébastien Bubeck, Martin Cai, Qin Cai, Vishrav
  Chaudhary, Dong Chen, Dongdong Chen, Weizhu              Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
  Chen, Yen-Chun Chen, Yi-Ling Chen, Hao Cheng,              Abhinav Pandey, Abhishek Kadian, Ahmad Al-
  Parul Chopra, Xiyang Dai, Matthew Dixon, Ro-               Dahle, Aiesha Letman, Akhil Mathur, Alan Schel-
  nen Eldan, Victor Fragoso, Jianfeng Gao, Mei Gao,          ten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh
  Min Gao, Amit Garg, Allie Del Giorno, Abhishek             Goyal, Anthony Hartshorn, Aobo Yang, Archi Mi-
  Goswami, Suriya Gunasekar, Emman Haider, Jun-              tra, Archie Sravankumar, Artem Korenev, Arthur
  heng Hao, Russell J. Hewett, Wenxiang Hu, Jamie            Hinsvark, Arun Rao, Aston Zhang, Aurelien Ro-
  Huynh, Dan Iter, Sam Ade Jacobs, Mojan Javaheripi,         driguez, Austen Gregerson, Ava Spataru, Baptiste
  Xin Jin, Nikos Karampatziakis, Piero Kauffmann,            Roziere, Bethany Biron, Binh Tang, Bobbie Chern,
  Mahoud Khademi, Dongwoo Kim, Young Jin Kim,                Charlotte Caucheteux, Chaya Nayak, Chloe Bi,
  Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi          Chris Marra, Chris McConnell, Christian Keller,
  Li, Yunsheng Li, Chen Liang, Lars Liden, Xihui             Christophe Touret, Chunyang Wu, Corinne Wong,
  Lin, Zeqi Lin, Ce Liu, Liyuan Liu, Mengchen Liu,           Cristian Canton Ferrer, Cyrus Nikolaidis, Damien Al-
  Weishung Liu, Xiaodong Liu, Chong Luo, Piyush              lonsius, Daniel Song, Danielle Pintz, Danny Livshits,
  Madan, Ali Mahmoudzadeh, David Majercak, Matt              Danny Wyatt, David Esiobu, Dhruv Choudhary,
  Mazzola, Caio César Teodoro Mendes, Arindam Mi-            Dhruv Mahajan, Diego Garcia-Olano, Diego Perino,
  tra, Hardik Modi, Anh Nguyen, Brandon Norick,              Dieuwke Hupkes, Egor Lakomkin, Ehab AlBadawy,
  Barun Patra, Daniel Perez-Becker, Thomas Portet,           Elina Lobanova, Emily Dinan, Eric Michael Smith,
  Reid Pryzant, Heyang Qin, Marko Radmilac, Liliang          Filip Radenovic, Francisco Guzmán, Frank Zhang,
  Ren, Gustavo de Rosa, Corby Rosset, Sambudha Roy,          Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis An-
  Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil          derson, Govind Thattai, Graeme Nail, Gregoire Mi-
  Salim, Michael Santacroce, Shital Shah, Ning Shang,        alon, Guan Pang, Guillem Cucurell, Hailey Nguyen,
  Hiteshi Sharma, Yelong Shen, Swadheen Shukla, Xia          Hannah Korevaar, Hu Xu, Hugo Touvron, Iliyan
  Song, Masahiro Tanaka, Andrea Tupini, Praneetha            Zarov, Imanol Arrieta Ibarra, Isabel Kloumann, Is-
  Vaddamanu, Chunyu Wang, Guanhua Wang, Lijuan               han Misra, Ivan Evtimov, Jack Zhang, Jade Copet,
  Wang, Shuohang Wang, Xin Wang, Yu Wang, Rachel             Jaewon Lee, Jan Geffert, Jana Vranes, Jason Park,
  Ward, Wen Wen, Philipp Witte, Haiping Wu, Xiaoxia          Jay Mahadeokar, Jeet Shah, Jelmer van der Linde,
  Wu, Michael Wyatt, Bin Xiao, Can Xu, Jiahang Xu,           Jennifer Billock, Jenny Hong, Jenya Lee, Jeremy Fu,
  Weijian Xu, Jilong Xue, Sonali Yadav, Fan Yang,            Jianfeng Chi, Jianyu Huang, Jiawen Liu, Jie Wang,
  Jianwei Yang, Yifan Yang, Ziyi Yang, Donghan Yu,           Jiecao Yu, Joanna Bitton, Joe Spisak, Jongsoo Park,
  Lu Yuan, Chenruidong Zhang, Cyril Zhang, Jianwen           Joseph Rocca, Joshua Johnstun, Joshua Saxe, Jun-
  Zhang, Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan           teng Jia, Kalyan Vasuden Alwala, Karthik Prasad,
  Zhang, and Xiren Zhou. 2024. Phi-3 technical report:       Kartikeya Upasani, Kate Plawiak, Ke Li, Kenneth
  A highly capable language model locally on your            Heafield, Kevin Stone, Khalid El-Arini, Krithika Iyer,
  phone.                                                     Kshitiz Malik, Kuenley Chiu, Kunal Bhalla, Kushal
                                                             Lakhotia, Lauren Rantala-Yeary, Laurens van der
Stefan Baack. 2024. A critical analysis of the largest       Maaten, Lawrence Chen, Liang Tan, Liz Jenkins,
   source for generative ai training data: Common crawl.     Louis Martin, Lovish Madaan, Lubo Malo, Lukas
   pages 2199–2208.                                          Blecher, Lukas Landzaat, Luke de Oliveira, Madeline
                                                             Muzzi, Mahesh Pasupuleti, Mannat Singh, Manohar
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie             Paluri, Marcin Kardas, Maria Tsimpoukelli, Mathew
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind           Oldham, Mathieu Rita, Maya Pavlova, Melanie Kam-
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda           badur, Mike Lewis, Min Si, Mitesh Kumar Singh,
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,              Mona Hassan, Naman Goyal, Narjes Torabi, Niko-
  Gretchen Krueger, Tom Henighan, Rewon Child,               lay Bashlykov, Nikolay Bogoychev, Niladri Chatterji,
  Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,              Ning Zhang, Olivier Duchenne, Onur Çelebi, Patrick
  Clemens Winter, Christopher Hesse, Mark Chen, Eric         Alrassy, Pengchuan Zhang, Pengwei Li, Petar Va-
  Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,        sic, Peter Weng, Prajjwal Bhargava, Pratik Dubal,
  Jack Clark, Christopher Berner, Sam McCandlish,            Praveen Krishnan, Punit Singh Koura, Puxin Xu,
  Alec Radford, Ilya Sutskever, and Dario Amodei.            Qing He, Qingxiao Dong, Ragavan Srinivasan, Raj
  2020. Language models are few-shot learners.               Ganapathy, Ramon Calderer, Ricardo Silveira Cabral,
                                                             Robert Stojnic, Roberta Raileanu, Rohan Maheswari,
Sébastien Bubeck, Varun Chandrasekaran, Ronen El-            Rohit Girdhar, Rohit Patel, Romain Sauvestre, Ron-
  dan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Pe-         nie Polidoro, Roshan Sumbaly, Ross Taylor, Ruan
  ter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg,          Silva, Rui Hou, Rui Wang, Saghar Hosseini, Sa-
  Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro,           hana Chennabasappa, Sanjay Singh, Sean Bell, Seo-
  and Yi Zhang. 2023. Sparks of artificial general in-       hyun Sonia Kim, Sergey Edunov, Shaoliang Nie, Sha-
  telligence: Early experiments with gpt-4.                  ran Narang, Sharath Raparthy, Sheng Shen, Shengye
                                                             Wan, Shruti Bhosale, Shun Zhang, Simon Van-
Nicholas Carlini, Florian Tramer, Eric Wallace,              denhende, Soumya Batra, Spencer Whitman, Sten
  Matthew Jagielski, Ariel Herbert-Voss, Katherine           Sootla, Stephane Collot, Suchin Gururangan, Syd-
  Lee, Adam Roberts, Tom Brown, Dawn Song, Ul-               ney Borodinsky, Tamar Herman, Tara Fowler, Tarek
  far Erlingsson, Alina Oprea, and Colin Raffel. 2021.       Sheasha, Thomas Georgiou, Thomas Scialom, Tobias
  Extracting training data from large language models.
Speckbacher, Todor Mihaylov, Tong Xiao, Ujjwal            Martynas Mankus, Matan Hasson, Matthew Lennie,
Karn, Vedanuj Goswami, Vibhor Gupta, Vignesh              Matthias Reso, Maxim Groshev, Maxim Naumov,
Ramanathan, Viktor Kerkez, Vincent Gonguet, Vir-          Maya Lathi, Meghan Keneally, Miao Liu, Michael L.
ginie Do, Vish Vogeti, Vítor Albiero, Vladan Petro-       Seltzer, Michal Valko, Michelle Restrepo, Mihir Pa-
vic, Weiwei Chu, Wenhan Xiong, Wenyin Fu, Whit-           tel, Mik Vyatskov, Mikayel Samvelyan, Mike Clark,
ney Meers, Xavier Martinet, Xiaodong Wang, Xi-            Mike Macey, Mike Wang, Miquel Jubert Hermoso,
aofang Wang, Xiaoqing Ellen Tan, Xide Xia, Xin-           Mo Metanat, Mohammad Rastegari, Munish Bansal,
feng Xie, Xuchao Jia, Xuewei Wang, Yaelle Gold-           Nandhini Santhanam, Natascha Parks, Natasha
schlag, Yashesh Gaur, Yasmine Babaei, Yi Wen,             White, Navyata Bawa, Nayan Singhal, Nick Egebo,
Yiwen Song, Yuchen Zhang, Yue Li, Yuning Mao,             Nicolas Usunier, Nikhil Mehta, Nikolay Pavlovich
Zacharie Delpierre Coudert, Zheng Yan, Zhengxing          Laptev, Ning Dong, Norman Cheng, Oleg Chernoguz,
Chen, Zoe Papakipos, Aaditya Singh, Aayushi Sri-          Olivia Hart, Omkar Salpekar, Ozlem Kalinli, Parkin
vastava, Abha Jain, Adam Kelsey, Adam Shajnfeld,          Kent, Parth Parekh, Paul Saab, Pavan Balaji, Pe-
Adithya Gangidi, Adolfo Victoria, Ahuva Goldstand,        dro Rittner, Philip Bontrager, Pierre Roux, Piotr
Ajay Menon, Ajay Sharma, Alex Boesenberg, Alexei          Dollar, Polina Zvyagina, Prashant Ratanchandani,
Baevski, Allie Feinstein, Amanda Kallet, Amit San-        Pritish Yuvraj, Qian Liang, Rachad Alao, Rachel
gani, Amos Teo, Anam Yunus, Andrei Lupu, An-              Rodriguez, Rafi Ayub, Raghotham Murthy, Raghu
dres Alvarado, Andrew Caples, Andrew Gu, Andrew           Nayani, Rahul Mitra, Rangaprabhu Parthasarathy,
Ho, Andrew Poulton, Andrew Ryan, Ankit Ramchan-           Raymond Li, Rebekkah Hogan, Robin Battey, Rocky
dani, Annie Dong, Annie Franco, Anuj Goyal, Apara-        Wang, Russ Howes, Ruty Rinott, Sachin Mehta,
jita Saraf, Arkabandhu Chowdhury, Ashley Gabriel,         Sachin Siby, Sai Jayesh Bondu, Samyak Datta, Sara
Ashwin Bharambe, Assaf Eisenman, Azadeh Yaz-              Chugh, Sara Hunt, Sargun Dhillon, Sasha Sidorov,
dan, Beau James, Ben Maurer, Benjamin Leonhardi,          Satadru Pan, Saurabh Mahajan, Saurabh Verma,
Bernie Huang, Beth Loyd, Beto De Paola, Bhargavi          Seiji Yamamoto, Sharadh Ramaswamy, Shaun Lind-
Paranjape, Bing Liu, Bo Wu, Boyu Ni, Braden Han-          say, Shaun Lindsay, Sheng Feng, Shenghao Lin,
cock, Bram Wasti, Brandon Spence, Brani Stojkovic,        Shengxin Cindy Zha, Shishir Patil, Shiva Shankar,
Brian Gamido, Britt Montalvo, Carl Parker, Carly          Shuqiang Zhang, Shuqiang Zhang, Sinong Wang,
Burton, Catalina Mejia, Ce Liu, Changhan Wang,            Sneha Agarwal, Soji Sajuyigbe, Soumith Chintala,
Changkyu Kim, Chao Zhou, Chester Hu, Ching-               Stephanie Max, Stephen Chen, Steve Kehoe, Steve
Hsiang Chu, Chris Cai, Chris Tindal, Christoph Fe-        Satterfield, Sudarshan Govindaprasad, Sumit Gupta,
ichtenhofer, Cynthia Gao, Damon Civin, Dana Beaty,        Summer Deng, Sungmin Cho, Sunny Virk, Suraj
Daniel Kreymer, Daniel Li, David Adkins, David            Subramanian, Sy Choudhury, Sydney Goldman, Tal
Xu, Davide Testuggine, Delia David, Devi Parikh,          Remez, Tamar Glaser, Tamara Best, Thilo Koehler,
Diana Liskovich, Didem Foss, Dingkang Wang, Duc           Thomas Robinson, Tianhe Li, Tianjun Zhang, Tim
Le, Dustin Holland, Edward Dowling, Eissa Jamil,          Matthews, Timothy Chou, Tzook Shaked, Varun
Elaine Montgomery, Eleonora Presani, Emily Hahn,          Vontimitta, Victoria Ajayi, Victoria Montanez, Vijai
Emily Wood, Eric-Tuan Le, Erik Brinkman, Este-            Mohan, Vinay Satish Kumar, Vishal Mangla, Vlad
ban Arcaute, Evan Dunbar, Evan Smothers, Fei Sun,         Ionescu, Vlad Poenaru, Vlad Tiberiu Mihailescu,
Felix Kreuk, Feng Tian, Filippos Kokkinos, Firat          Vladimir Ivanov, Wei Li, Wenchen Wang, Wen-
Ozgenel, Francesco Caggioni, Frank Kanayet, Frank         wen Jiang, Wes Bouaziz, Will Constable, Xiaocheng
Seide, Gabriela Medina Florez, Gabriella Schwarz,         Tang, Xiaojian Wu, Xiaolan Wang, Xilun Wu, Xinbo
Gada Badeer, Georgia Swee, Gil Halpern, Grant             Gao, Yaniv Kleinman, Yanjun Chen, Ye Hu, Ye Jia,
Herman, Grigory Sizov, Guangyi, Zhang, Guna               Ye Qi, Yenda Li, Yilin Zhang, Ying Zhang, Yossi Adi,
Lakshminarayanan, Hakan Inan, Hamid Shojanaz-             Youngjin Nam, Yu, Wang, Yu Zhao, Yuchen Hao,
eri, Han Zou, Hannah Wang, Hanwen Zha, Haroun             Yundi Qian, Yunlu Li, Yuzi He, Zach Rait, Zachary
Habeeb, Harrison Rudolph, Helen Suk, Henry As-            DeVito, Zef Rosnbrick, Zhaoduo Wen, Zhenyu Yang,
pegren, Hunter Goldman, Hongyuan Zhan, Ibrahim            Zhiwei Zhao, and Zhiyu Ma. 2024. The llama 3 herd
Damlaj, Igor Molybog, Igor Tufanov, Ilias Leontiadis,     of models.
Irina-Elena Veliche, Itai Gat, Jake Weissman, James
Geboski, James Kohli, Janice Lam, Japhet Asher,         Alexandra Luccioni and Joseph Viviano. 2021. What’s
Jean-Baptiste Gaya, Jeff Marcus, Jeff Tang, Jen-          in the box? an analysis of undesirable content in the
nifer Chan, Jenny Zhen, Jeremy Reizenstein, Jeremy        Common Crawl corpus. In Proceedings of the 59th
Teboul, Jessica Zhong, Jian Jin, Jingyi Yang, Joe         Annual Meeting of the Association for Computational
Cummings, Jon Carvill, Jon Shepard, Jonathan Mc-          Linguistics and the 11th International Joint Confer-
Phie, Jonathan Torres, Josh Ginsburg, Junjie Wang,        ence on Natural Language Processing (Volume 2:
Kai Wu, Kam Hou U, Karan Saxena, Kartikay Khan-           Short Papers), pages 182–189, Online. Association
delwal, Katayoun Zand, Kathy Matosich, Kaushik            for Computational Linguistics.
Veeraraghavan, Kelly Michelena, Keqian Li, Ki-
ran Jagadeesh, Kun Huang, Kunal Chawla, Kyle            Sai Krishna Mendu, Harish Yenala, Aditi Gulati, Shanu
Huang, Lailin Chen, Lakshya Garg, Lavender A,             Kumar, and Parag Agrawal. 2025. Towards safer
Leandro Silva, Lee Bell, Lei Zhang, Liangpeng             pretraining: Analyzing and filtering harmful content
Guo, Licheng Yu, Liron Moshkovich, Luca Wehrst-           in webscale datasets for responsible llms.
edt, Madian Khabsa, Manav Avalani, Manish Bhatt,
                                                        Guilherme Penedo, Hynek Kydlíček, Loubna Ben al-
  lal, Anton Lozhkov, Margaret Mitchell, Colin Raffel,
  Leandro Von Werra, and Thomas Wolf. 2024. The
  fineweb datasets: Decanting the web for the finest
  text data at scale.
Colin Raffel, Noam Shazeer, Adam Roberts, Kather-
  ine Lee, Sharan Narang, Michael Matena, Yanqi
  Zhou, Wei Li, and Peter J. Liu. 2020. Exploring the
  limits of transfer learning with a unified text-to-text
  transformer. Journal of Machine Learning Research,
  21(140):1–67.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,
  Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
  Azhar, Aurelien Rodriguez, Armand Joulin, Edouard
  Grave, and Guillaume Lample. 2023. Llama: Open
  and efficient foundation language models.
