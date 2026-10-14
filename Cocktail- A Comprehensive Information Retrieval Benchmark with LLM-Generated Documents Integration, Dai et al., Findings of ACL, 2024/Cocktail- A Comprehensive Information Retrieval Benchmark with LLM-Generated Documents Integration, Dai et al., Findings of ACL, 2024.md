             Cocktail: A Comprehensive Information Retrieval Benchmark
                  with LLM-Generated Documents Integration
     Sunhao Dai1 , Weihao Liu1 , Yuqi Zhou1 , Liang Pang2 , Rongju Ruan3 , Gang Wang3 ,
                         Zhenhua Dong3 , Jun Xu1∗, Ji-Rong Wen1
            1
              Gaoling School of Artificial Intelligence, Renmin University of China
         2
           CAS Key Laboratory of AI Safety, Institute of Computing Technology, CAS
                                  3
                                    Huawei Noah’s Ark Lab
                {sunhaodai, junxu}@ruc.edu.cn, pangliang@ict.ac.cn
                  Abstract                         queries (Li, 2022; Zhao et al., 2023a). Traditionally,
    The proliferation of Large Language Models                IR benchmarks, notably MS MARCO (Nguyen
    (LLMs) has led to an influx of AI-generated               et al., 2016), TREC (Craswell et al., 2020) and
    content (AIGC) on the internet, transforming              BEIR (Thakur et al., 2021), have exclusively uti-
    the corpus of Information Retrieval (IR) sys-             lized human-written content. However, the recent
    tems from solely human-written to a coexis-               surge in Artificial Intelligence Generated Content
    tence with LLM-generated content. The impact              (AIGC) facilitated by advanced Large Language
    of this surge in AIGC on IR systems remains
                                                              Models (LLMs) has revolutionized the IR land-
    an open question, with the primary challenge
    being the lack of a dedicated benchmark for re-           scape (Dai et al., 2024a). This evolution has broad-
    searchers. In this paper, we introduce Cocktail,          ened the scope of IR systems, which now encom-
    a comprehensive benchmark tailored for eval-              pass a hybrid corpus composed of both human-
    uating IR models in this mixed-sourced data               written and LLM-generated content (Ai et al., 2023;
    landscape of the LLM era. Cocktail consists of            Zhu et al., 2023; Dai et al., 2024a), presenting new
    16 diverse datasets with mixed human-written              challenges and opportunities of IR in the LLM era.
    and LLM-generated corpora across various text
    retrieval tasks and domains. Additionally, to                For instance, recent studies (Dai et al., 2024b;
    avoid the potential bias from previously in-              Xu et al., 2024) have shed light on a critical issue
    cluded dataset information in LLMs, we also               within neural retrieval models in the LLM era: a
    introduce an up-to-date dataset, named NQ-                pronounced “source bias”. This bias, characterized
    UTD, with queries derived from recent events.             by the preferential ranking of LLM-generated con-
    Through conducting over 1,000 experiments to              tent over semantically equivalent human-written
    assess state-of-the-art retrieval models against          content, poses a significant threat to the IR ecosys-
    the benchmarked datasets in Cocktail, we un-
    cover a clear trade-off between ranking per-
                                                              tem. Hence, the need to comprehensively un-
    formance and source bias in neural retrieval              derstand such impact of LLM-generated content
    models, highlighting the necessity for a bal-             across different IR models and diverse IR domains
    anced approach in designing future IR sys-                and tasks has become more pressing, especially
    tems. We hope Cocktail can serve as a foun-               with the escalating prevalence of LLM-generated
    dational resource for IR research in the LLM              content (Hanley and Durumeric, 2023; Bengio
    era, with all data and code publicly available at         et al., 2023). However, existing IR benchmarks
    https://github.com/KID-22/Cocktail.
                                                              either fail to reflect the real-world IR scenarios of
1   Introduction                                              the LLM era, as they solely contain human-written
                                                              texts in their corpus, or provide limited datasets for
Information retrieval (IR) systems, as the keystone
                                                              exploring source bias. These shortcomings high-
in overcoming information overload, have seen
                                                              light the need for a comprehensive benchmark that
widespread application across various domains,
                                                              accurately mirrors the current IR landscape, char-
including search engines (Li et al., 2014), ques-
                                                              acterized by the integration of both human-written
tion answering (Karpukhin et al., 2020), dialog
                                                              and LLM-generated texts within the corpus, to fa-
systems (Chen et al., 2017), etc. A typical IR
                                                              cilitate new research questions in this LLM era.
system aims at finding relevant documents or pas-
sages from a specific corpus in response to user’s               To fill this gap, we present a comprehensive
    ∗
                                                              benchmark tailored for IR in the LLM era, namely
     Corresponding author. Work partially done at Engineer-
ing Research Center of Next-Generation Intelligent Search     Cocktail, where the corpus contains both human-
and Recommendation, Ministry of Education.                    written and LLM-generated texts. Cocktail en-
                                                          7052
                  Findings of the Association for Computational Linguistics: ACL 2024, pages 7052–7074
                          August 11-16, 2024 ©2024 Association for Computational Linguistics
compasses 16 retrieval datasets spanning differ-                                   -20.0
ent domains and tasks, enabling both in-domain                                     -22.5




                                                        Source Bias (Relative Δ)
                                                                                           BERT-mini
and out-of-domain evaluation settings. To con-                                     -25.0               BERT-small
                                                                                                                  coCondenser
                                                                                                         RoBERTa
struct these datasets, we first select 15 widely                                   -27.5
                                                                                                         BERT-base
                                                                                                                         Contriever
                                                                                                                                      monoT5
used public human-written corpora from MS                                          -30.0
                                                                                                                ANCE TAS-B
MARCO (Nguyen et al., 2016), TREC (Craswell                                        -32.5
                                                                                                  Neural Retriever      RetroMAE       CE
et al., 2020), and BEIR (Thakur et al., 2021). Then,                               -35.0
                                                                                                  Neural Re-ranker
                                                                                   -37.5                                          DRAGON
based on these human-written corpora, we use                                                      Trade-off Trend Line
                                                                                   -40.0
Llama2 (Touvron et al., 2023) to rewrite each text                                     42.5 45.0 47.5 50.0 52.5 55.0 57.5 60.0 62.5
to preserve semantic equivalence while introducing                                             Ranking Performance (NDCG@1)
LLM-generated corpora. Finally, we mix the origi-
nal human-written corpora and the LLM-generated         Figure 1: Ranking performance versus source bias com-
                                                        parison on averaged results of 16 datasets benchmarked
corpora to get the final Cocktail corpora and as-
                                                        in Cocktail. A more negative Relative ∆ signifies in-
sign the same relevancy label for the corresponding     creased source bias towards LLM-generated content.
query-document pairs. Furthermore, to address the       The Pearson correlation coefficient between these two
potential biases introduced by the inherent knowl-      axes is −0.772 (p-value < 0.05), indicating a strong neg-
edge of LLMs during the rewriting process, we col-      ative correlation. For brevity, we omit the ‘%’ symbol
lect an additional new dataset, NQ-UTD. This new        of the scores in all the tables and figures.
dataset comprises 80 queries and 800 documents
from recent events. It serves as a critical compo-      bias. The evaluation tool, along with the codes,
nent of Cocktail, offering an essential perspective     is open-sourced, facilitating ease of adaptation for
for assessing the performance of IR systems in the      evaluating new models and datasets.
context of both pre- and post-LLM era datasets.            (3) Extensive empirical studies reveal a clear
   With the benchmarked diverse datasets in Cock-       trade-off between ranking performance and source
tail, we then conduct comprehensive evaluations         bias in neural retrieval models. This finding un-
of over ten state-of-the-art (SOTA) retrieval mod-      derscores the importance of achieving a suitable
els through more than 1,000 experiments. Our            balance between performance improvement and
analysis firstly reinforces previous findings by Dai    bias mitigation in future IR model designs.
et al. (2024b), highlighting a pervasive bias to-
wards LLM-generated content across nearly all 16        2                          Related Work
datasets in Cocktail among all neural retrieval mod-
els. Furthermore, the results illustrated in Figure 1   IR meets Large Language Models. Information
reveal a distinct trade-off between ranking perfor-     retrieval (IR), the keystone of information access,
mance and source bias within these SOTA neural          has now significantly been reshaped by the emer-
models. This observation suggests that while striv-     gence of large language models (LLMs) (Zhao
ing for high performance, these models may rely         et al., 2023b; Ai et al., 2023; Dai et al., 2024a). This
on inherent shortcuts, failing to grasp true seman-     intersection has manifested in two pivotal ways.
tic relevance and resulting in severe source bias.      On the one hand, much effort has been made to
Hence, future work requires better considering a        utilize the advanced capabilities of LLMs to refine
balance between performance and bias mitigation         the whole retrieval pipeline (Zhu et al., 2023), in-
in the design of next-generation IR models.             cluding the integration of LLMs across various
                                                        IR components, such as query rewriters (Srini-
  In summary, our contributions are as follows:
                                                        vasan et al., 2022), retrievers (Wang et al., 2023),
   (1) To the best of our knowledge, Cocktail is the    re-rankers (Sun et al., 2023b), and readers (Shi
first comprehensive benchmark with 16 datasets          et al., 2023). On the other hand, the capacity
from a variety of domains and tasks tailed for IR       of LLMs for generating human-like text at scale
research in the LLM era, where the corpus of each       has shifted the landscape of searchable corpora,
dataset contains both human-written texts and cor-      which now includes both human-written and LLM-
responding LLM-generated counterparts.                  generated texts. This evolution has introduced new
  (2) We conduct extensive evaluations of state-of-     challenges, most notably the emergence of source
the-art retrieval models using the Cocktail bench-      bias (Dai et al., 2024b; Xu et al., 2024; Dai et al.,
mark, assessing both retrieval accuracy and source      2024a), where neural retrievers exhibit a preference
                                                    7053
                                                                   Train      Dev                     Test                       Avg. Word Length
     Dataset
                  Domain               Task           Relevancy   # Pairs   # Query   # Query    # Corpus     Avg. D/Q   Query    Human Doc    LLM Doc
                                           Collected Before the Emergence of LLM (∼ - 2021/04)
  MS MARCO          Misc.       Passage-Retrieval      Binary     532,663        -      6,979       542,203        1.1     6.0          58.1         55.1
      DL19          Misc.       Passage-Retrieval      Binary        -           -         43       542,203       95.4     5.4          58.1         55.1
      DL20          Misc.       Passage-Retrieval      Binary        -           -         54       542,203       66.8     6.0          58.1         55.1
  TREC-COVID     Bio-Medical     Bio-Medical IR        3-level       -           -         50       128,585      430.1    10.6         197.6        165.9
    NFCorpus     Bio-Medical     Bio-Medical IR        3-level    110,575     324         323         3,633       38.2     3.3         221.0        206.7
      NQ          Wikipedia    Question Answering      Binary        -           -      3,446       104,194        1.2     9.2          86.9         81.0
    HotpotQA      Wikipedia    Question Answering      Binary     169,963    5447       7,405       111,107        2.0    17.7          67.9         66.6
   FiQA-2018       Finance     Question Answering      Binary     14,045      499         648        57,450        2.6    10.8         133.2        107.8
   Touché-2020      Misc.      Argument Retrieval      3-level       -           -         49       101,922       18.4     6.6         165.4        134.4
  CQADupStack     StackEx.     Dup. Ques.-Retrieval    Binary        -           -      1,563        39,962        2.4     8.5          77.2         72.0
    DBPedia       Wikipedia      Entity-Retrieval      3-level       -          67        400       145,037       37.3     5.4          53.1         54.0
    SCIDOCS       Scientific    Citation-Prediction    Binary        -           -      1,000        25,259        4.7     9.4         169.7        161.8
     FEVER        Wikipedia       Fact Checking        Binary     140,079    6666       6,666       114,529        1.2     8.1         113.4         91.1
 Climate-FEVER    Wikipedia       Fact Checking        Binary        -           -      1,535       101,339        3.0    20.2          99.4         81.3
     SciFact      Scientific      Fact Checking        Binary       919          -        300         5,183        1.1    12.4         201.8        192.7
                                         Collected After the Emergence of LLM (2023/11 - 2024/01)
    NQ-UTD          Misc.      Question Answering      3-level       -           -         80          800         3.7    12.1         101.1         94.7


Table 1: Statistics of all 16 datasets in Cocktail benchmark. Avg. D/Q denotes the average number of relevant
documents per query.


for LLM-generated content, potentially compro-                               the integration of LLMs into IR.
mising the fairness and accuracy of search results.
Moreover, the inclusion of LLM-generated content                             3       Benchmarking Retrieval Datasets
also raises concerns about privacy (Yao et al., 2023)
                                                                             Cocktail establishes a comprehensive benchmark
and the dissemination of misinformation (Pan et al.,
                                                                             tailored for the evaluation of IR models in the
2023). In this paper, we focus on the second line
                                                                             LLM era, characterized by corpora containing both
and aim to establish a comprehensive benchmark
                                                                             human-written and LLM-generated content. This
for evaluating IR models in the LLM era, which
                                                                             benchmark aims to access the performance and
can help understand the impact of LLM-generated
                                                                             biases of existing retrieval models while encourag-
content on IR systems.
                                                                             ing the creation of future IR systems that excel in
Related Benchmarks. Historically, before the pro-                            robustness and generalization across diverse scenar-
liferation of LLM-generated content on the inter-                            ios in the LLM era. To achieve this, we collect and
net, several benchmarks were established for the                             construct 16 IR datasets, incorporating 15 datasets
evaluation of IR models, primarily utilizing cor-                            from the pre-LLM era and one newly developed
pora composed of human-written documents or                                  dataset to ensure a wide representation of domains
passages. Notably, MS MARCOO (Nguyen et al.,                                 and tasks. The statistics for the 16 datasets bench-
2016) and TREC (Craswell et al., 2020) are widely                            marked in Cocktail are summarized in Table 1. We
used for supervised evaluation in IR research. Sim-                          also list the dataset website links and the corre-
ilarly, BEIR (Thakur et al., 2021) presents a diverse                        sponding licenses in Appendix Table 5.
benchmark incorporating 18 datasets from various
IR domains and tasks, tailored to zero-shot evalu-                           3.1      Dataset Construction
ation. Despite their contributions to advancing IR                           A key concern in constructing datasets with LLMs
systems, these benchmarks fall short of reflecting                           is the potential for LLMs to have prior knowl-
the real-world scenarios of the current LLM era due                          edge about queries, which could lead to an unfair
to the absence of LLM-generated content in their                             evaluation. To address this, following previous
corpora (Dai et al., 2024b; Xu et al., 2024; Dai et al.,                     works (Dai et al., 2024b), we choose rewriting doc-
2024a). This gap underscores the necessity for new                           uments without incorporating query-related infor-
benchmarks that include both human-written and                               mation rather than a full generation from LLMs
LLM-generated texts, offering a more comprehen-                              with given queries, ensuring that any detected
sive and realistic evaluation environment to navi-                           source bias is a genuine reflection of model prefer-
gate the challenges and opportunities presented by                           ences. Moreover, by avoiding full document gen-
                                                                         7054
                                                                                     Query            Query
          Queries                                                                     Doc               Doc
      Annotated Labels
                         Corpus          Human Doc              LLM Doc               Label            Label
 (1) Seed Human Data Collection           (2) LLM Content Generation            (3) Relevancy Label Assignment

                Figure 2: An overview of the dataset construction pipeline involved in Cocktail.


eration based on queries, this approach also sim-         follows: Rewritten Text: <your rewritten text>.”
plifies controlling the text length across different      This post-instruction strengthens the instruction-
sources, ensuring consistency and further reduc-          following capabilities of LLMs, proving particu-
ing potential biases in the evaluation. Specifically,     larly effective for processing and generating re-
we construct each dataset in Cocktail following a         sponses to long input texts (Liu et al., 2023).
three-step process: 1) collecting seed datasets with      Relevancy Label Assignment. Upon the creation
human-written corpus and alongside relevancy la-          of the LLM-generated corpus for each dataset, we
bels for given queries; 2) leveraging LLMs to gener-      assign the relevancy labels from the original <query,
ate corresponding LLM-generated corpus with the           human-written doc> pairs to the new <query, LLM-
human-written corpus as inputs; and 3) assigning          generated doc> pairs. This process is underpinned
relevancy labels to the LLM-generated content and         by the premise that both sources of the content pre-
given queries, ensuring seamless integration into         serve nearly identical semantic information, which
the benchmark. An overview of our construction            will be further verified in the following section.
pipeline is shown in Figure 2.                               All the datasets in Cocktail are organized in a
Seed Human Datasets. To cover as diverse IR do-           standard format (corpus, queries, qrels) akin to the
mains and tasks as possible, we select the widely-        BEIR benchmark (Thakur et al., 2021), facilitating
used 15 datasets from MS MARCO (Nguyen                    ease of use and comparison. Examples for each
et al., 2016), TREC (Craswell et al., 2020), and          dataset are showcased in Appendix Table 12. More
BEIR (Thakur et al., 2021) benchmark as our               details about the data processing and quality control
human-written corpus. These datasets span six do-         are provided in Appendix A.2.
mains and eight distinct tasks, facilitating compre-
hensive evaluations under both in-domain and out-         3.2    Dataset Statistics and Analysis
of-domain settings. Moreover, as suggested in Sun         As shown in Table 1, there are minimal differences
et al. (2023b), we also construct a new test dataset      in average word length between human-written and
NQ-UTD to ensure that relevance annotations have          LLM-generated documents, with the latter being
not been learned by LLMs. NQ-UTD comprises 80             marginally shorter. The detailed text length distri-
queries distributed across eight domains, sourcing        bution, depicted in Appendix Figure 5, further con-
from recent events (from Nov. 2023 to Jan. 2024).         firms the negligible variance in text length. Addi-
We verify that neither GPT-4 nor Gemini, two of           tionally, term-based Jaccard similarity and overlap
the most advanced LLMs to date, can not answer            distributions between LLM-generated and human-
the questions within NQ-UTD, validating no prior          written documents, visualized in Appendix Fig-
knowledge of these questions in LLM. For details          ure 6, show a noticeable distinction in terms despite
about the collection and annotation processes of          similar semantic content.
NQ-UTD, along with detailed descriptions of all              Following practices in Dai et al. (2024b), our
16 datasets, please refer to Appendix A.1.                dataset construction process involved feeding only
LLM-Generated Corpus. To ensure a fair                    the original human-written text to the LLM for
evaluation of the impact of incorporating LLM-            rewriting, without inputting any query-specific in-
generation content, we utilize the widely used            formation to avoid introducing additional query-
llama-2-7b-chat to rewrite each human-written             related bias. Furthermore, we employed the Ope-
text without changing its semantic information,           nAI embedding model1 to obtain semantic em-
with the following instructions: “Original Text:          beddings for both text sources, comparing them
{{human-written text}} Please rewrite the above              1
                                                               text-embedding-ada-002: https://platform.openai.
given text. Your answer must be formatted as              com/docs/guides/embeddings

                                                     7055
through cosine similarity. For calibrating the re-      K = 1 since the top-1 item in the retrieved list is
sults, we also compare the semantic similarity          most likely to be viewed and clicked by users. To
between randomly selected <human-written doc,           provide a more comprehensive evaluation, we also
LLM-generated doc> pairs and matching pairs             report results on K = 3 and K = 5 in Appendix C.
<human-written doc, LLM-generated doc>. These             Moreover, in the multi-sourced corpus shaped
comparisons, presented in Appendix Figure 7 and         by LLMs, the evaluation of IR systems necessitates
Table 9, demonstrate a high similarity between the      not only mere accuracy metrics but also a criti-
LLM-generated document and the corresponding            cal assessment of source bias (Dai et al., 2024b).
original human-written counterpart, indicating suc-     This bias, as evidenced by ranking LLM-generated
cessful semantic retention of the original human-       content higher than human-written content, poses
written text in the LLM-generated texts. Addition-      a significant challenge in today’s IR ecosystem.
ally, evaluations of several retrieval models on sole   To quantify and normalize source bias in differ-
human-written or LLM-generated corpora showed           ent datasets, we follow previous works (Dai et al.,
consistent performance, as seen in Appendix Ta-         2024b; Xu et al., 2024) and adopt the Relative ∆.
ble 8. Moreover, we also conduct human evalu-           This metric captures the relative percentage differ-
ations for quality verification for each dataset in     ence in NDCG scores between human-written and
Appendix Table 10. These observations reinforce         LLM-generated content, which is defined as:
confidence in the quality of our newly constructed                           NDCGHuman −NDCGLLM
                                                              Relative ∆ = (NDCG                    × 100%,
                                                                                 Human +NDCGLLM )/2
datasets, suggesting that the LLM-generated con-
tent maintains semantics comparable to human-           where the NDCGHuman and NDCGLLM denote the
written texts for IR tasks. The detailed dataset        NDCG scores attributed to human-written and
analysis is provided in Appendix A.3.                   LLM-generated content, respectively. Note that
                                                        Relative ∆ > 0 indicates that IR models rank
4   Benchmarking Evaluation Protocol                    human-written content higher than LLM-generated
                                                        content, and conversely, Relative ∆ < 0 indi-
Evaluation Framework. To standardize the as-            cates the opposite tendency. The absolute value
sessment of IR models within the LLM era, we also       of Relative ∆ reflects the extent of source bias.
develop a Python framework that combines user-
friendliness with comprehensive evaluation capabil-     5       Benchmarking Retrieval Models
ities. Built on the foundation of the BEIR (Thakur      In this section, we delve into the evaluation and
et al., 2021), our framework inherits its best fea-     analysis of various retrieval models utilizing the
tures, including the ability to easily replicate ex-    constructed Cocktail benchmarked datasets.
periments from open-sourced repositories and in-
corporate new models and datasets. A key in-            5.1      Retrieval Models
novation of our framework is its ability to con-        Following the BEIR benchmark (Thakur et al.,
duct evaluations using either individual or mixed       2021), we focus on evaluating the advanced state-
corpora, accommodating the mixture of human-            of-the-art transformer-based neural retrieval mod-
written and LLM-generated content characteris-          els. Besides the widely used lexical retriever
tic of the LLM era. These features make our             BM25 (Robertson et al., 2009), our experiments
framework an invaluable tool for advancing IR re-       include two main types of neural retrieval models:
search and application in both academia and indus-
                                                        Neural Retriever. We utilize and fine-tune the fol-
try. A detailed description and all the scripts of
                                                        lowing two most commonly used pre-trained lan-
our evaluation framework are provided in the link
                                                        guage models on the MS MARCO dataset (Nguyen
https://github.com/KID-22/Cocktail.
                                                        et al., 2016) using the official training script2
Evaluation Metrics. Aligned with the BEIR               from BEIR: 1) BERT (Devlin et al., 2019); 2)
benchmark (Thakur et al., 2021), we select Nor-         RoBERTa (Liu et al., 2019). Additionally, we
malized Discounted Cumulative Gain (NDCG@K)             evaluate the performance of state-of-the-art mod-
as our primary metric to assess retrieval accuracy,     els also trained on MS MARCO, employing offi-
given its robustness in capturing the effectiveness     cially released checkpoints: 3) ANCE (Xiong et al.,
of IR systems across tasks with binary and graded           2
                                                            https://github.com/beir-cellar/beir/blob/
relevance judgments. Following previous stud-           main/examples/retrieval/training/train_msmarco_
ies (Dai et al., 2024b; Xu et al., 2024), we choose     v3.py

                                                    7056
                 Lexical                                        Neural Retrievers                                          Neural Re-rankers
   Model (→)
                 BM25      BERT   RoBERTa     ANCE         TAS-B       Contriever   coCondenser   RetroMAE        DRAGON    CE      monoT5
      PLM           -      BERT   RoBERTa    RoBERTa     DistilBERT      BERT           BERT        BERT           BERT    MiniLM      T5        Average
     # Paras        -      110M    125M        125M         66M          110M           110M        110M           110M     66M      220M      All    Neural
                                            Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
   MS MARCO       38.8     51.6    51.9         52.8        54.4         55.6           55.3         55.7          59.1     57.8      55.3     53.5    54.9
      DL19        57.8     78.3    76.4         72.5        71.7         72.1           76.4         77.5          78.3     81.0      74.0     74.2    75.8
      DL20        55.3     79.9    76.9         73.2        72.5         73.8           79.3         76.5          82.4     73.5      71.0     74.0    75.9
                                          Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID      67.0     67.0    62.0         68.0        65.0         64.0           70.0         72.0          75.0     77.0      82.0     69.9    70.2
    NFCorpus      45.4     39.2    36.4         35.3        41.5         42.6           43.5         41.6          42.7     50.2      44.1     42.0    41.7
      NQ          45.7     62.5    60.0         60.0        65.0         69.6           65.6         67.5          70.4     69.1      71.3     64.2    66.1
    HotpotQA      84.3     75.3    62.9         72.1        84.6         88.1           82.1         88.5          89.1     93.9      89.8     82.8    82.6
   FiQA-2018      24.4     24.7    24.9         28.9        28.1         34.0           27.2         31.8          36.3     35.5      40.9     30.6    31.2
   Touché-2020    57.1     39.8    42.9         44.9        44.9         40.8           36.7         44.9          52.0     56.1      55.1     46.8    45.8
  CQADupStack     28.6     26.6    26.9         31.3        23.4         34.2           33.2         31.3          36.0     34.7      36.8     31.2    31.4
    DBPedia       36.6     55.3    50.6         48.0        56.3         62.1           56.9         56.8          59.6     58.6      49.3     53.6    55.3
    SCIDOCS       16.2     12.3    11.2         14.5        16.0         16.6           14.5         16.2          17.9     19.0      19.5     15.8    15.8
     FEVER        65.6     80.6    75.9         80.4        83.1         86.4           75.8         87.6          88.0     90.2      76.3     80.9    82.4
 Climate-FEVER    25.2     26.4    27.4         28.3        32.7         31.4           28.1         32.3          34.0     35.2      33.8     30.4    31.0
     SciFact      55.7     38.0    40.3         40.7        53.7         55.0           50.0         52.3          55.3     56.3      65.3     51.2    50.7
                                          Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD        76.9     74.4    66.9         78.8        81.9         75.6           73.1         78.8          76.9     89.4      90.0     78.4    78.6
                                                                      Averaged Result
   Supervised     50.6     69.9    68.4         66.2        66.2         67.2           70.3         69.9          73.3     70.8      66.8     67.2    68.9
    Zero-shot     48.4     47.9    45.3         48.6        52.0         53.9           50.5         54.0          56.4     58.9      58.0     52.1    52.5
       All        48.8     52.0    49.6         51.9        54.7         56.4           54.2         57.0          59.6     61.1      59.7     55.0    55.6


Table 2: Overall ranking performance (NDCG@1) across all benchmarked datasets in Cocktail. The second-to-last
column is the average result across all models, while the last column is the average for all neural retrieval models.
The best performed result for each dataset is marked in bold, and the second best is underlined.


2020); 4) TAS-B (Hofstätter et al., 2021); 5) Con-                              Neural models consistently exhibit source bias
triever (Izacard et al., 2022); 6) coCondenser (Gao                             towards LLM-generated content. This bias is
and Callan, 2022); 7) RetroMAE (Xiao et al., 2022)                              evident across neural retrieval models, spanning
; 8) DRAGON (Lin et al., 2023).                                                 both in-domain and, more significantly, out-of-
Neural Re-ranker. For re-ranking, we employ two                                 distribution datasets. This trend persists in data
state-of-the-art models with their publicly available                           from both pre-LLM and LLM eras. Remarkably,
official pre-trained checkpoints: 1) CE (Wang et al.,                           the average Relative ∆ across all neural models
2020); 2) monoT5 (Raffel et al., 2020).                                         on the datasets surpasses −25%. These findings
   In our experiments, unless specified otherwise,                              further support the findings of Dai et al. (2024b)
neural re-rankers re-rank the top-100 documents                                 and verify the widespread source bias in neural re-
retrieved by BM25. Detailed information on the                                  trieval models, regardless of the domain or task,
benchmarked models, including the publicly avail-                               highlighting an urgent need to address this bias.
able official pre-trained checkpoints and implemen-                             Stronger neural retrieval models exhibit more
tation details, can be found in Appendix B.                                     severe source bias. The results illustrated in Fig-
5.2 Benchmarked Results                                                         ure 1 underscore a significant trade-off faced by
                                                                                neural retrieval models: advancements in ranking
We conduct extensive evaluations with more than                                 performance often come with an increase in source
1,000 experiments on the Cocktail benchmarked                                   bias. This trend suggests that these SOTA neural
datasets. The results of retrieval accuracy and                                 models may not fully understand semantic rele-
source bias across all benchmarked retrieval mod-                               vance. Instead, these models tend to leverage in-
els and datasets are reported in Table 2 and Table 33 ,                         herent shortcuts to enhance performance, inadver-
respectively. Figure 1 shows average results of neu-                            tently leading to increased bias. This phenomenon
ral retrieval models across all datasets. From the                              suggests that attempts to boost model performance
results, we have the following key observations:                                could unintentionally magnify source bias issues,
    3
      Note that SciFact was regenerated with our prompt, lead-                  underlining the challenge of advancing model ca-
ing to slight result discrepancies from Dai et al. (2024b)                      pabilities without leading to severe source bias.
                                                                         7057
                       Lexical                                                             Neural Retrievers                                      Neural Re-rankers
   Model (→)
                       BM25       BERT      RoBERTa         ANCE                   TAS-B         Contriever    coCondenser   RetroMAE   DRAGON     CE      monoT5
      PLM                 -       BERT      RoBERTa       RoBERTa            DistilBERT            BERT           BERT        BERT       BERT     MiniLM      T5         Average
     # Paras              -       110M       125M            125M                  66M             110M           110M        110M       110M      66M      220M      All     Neural
                                                         Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
  MS MARCO              72.2      -13.2      -18.9               1.1               -29.0           -10.8           5.1         -20.5     -18.2     -26.3     -7.8     -6.0    -13.8
     DL19              108.7      -51.3      11.0                -0.8              -55.0           -21.4          -39.6        -53.9     -111.1    -18.3     -53.7    -25.9   -39.4
     DL20              101.6      -76.5      -63.5               -2.5              -11.0           -10.8          -38.1        -43.7     -59.2     -25.3     -11.3    -21.8   -34.2
                                                       Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID            32.8      -62.7      -64.5           -58.8                 -95.4           -87.5          -68.6        -66.7     -45.3     -64.9     -63.5    -58.6   -67.8
   NFCorpus             -29.5     -30.6      -50.5           -23.2                 -44.8           -99.5          -49.2        -17.3     -37.9     -66.1     -38.9    -44.3   -45.8
      NQ                -17.9     -26.6      -16.7           -12.7                 -41.8           -37.9          -25.0        -25.2     -47.2     -61.6     -33.6    -31.5   -32.8
   HotpotQA             51.0      -1.1        -3.5           -13.6                  0.2             -5.7          -5.4         5.2        -8.5     36.6      14.8     6.4      1.9
   FiQA-2018            -8.2      -38.1       8.8            -33.3                  -6.4           -38.3          -29.4        -52.8     -12.7     -42.3     -35.7    -26.2   -28.0
  Touché-2020           -21.4     -25.6      -76.0           -36.1                 -36.1           -29.8          10.9         -9.4      -66.4    -127.3     -66.4    -44.0   -46.2
  CQADupStack           22.4      -45.1      -39.4           -19.8                 -10.3           -22.2          -6.6         -67.1     -24.4     -30.5     -8.7     -22.9   -27.4
    DBPedia             18.6      -5.4       -19.3           -25.8                  2.5             4.5           -11.6        -24.6     -21.5     -13.3      5.5     -8.2    -10.9
   SCIDOCS               2.5      21.1       -21.4               -9.7              -20.0            0.0           -26.2        -22.2     -16.8     -27.4     -35.9    -14.2   -15.8
    FEVER               -26.2     2.5         -2.4           -87.1                 -16.8           -20.4          -22.2        -1.4      -26.8     -4.4      11.5     -17.6   -16.7
 Climate-FEVER           6.3      -15.2      -16.1          -109.9                 -22.6           -12.7          -17.8        -15.5     -10.6     5.1       -89.0    -27.1   -30.4
     SciFact             1.1      -52.6      -14.9           -29.6                 -53.3            1.5           -21.6        -29.4     -38.7     -8.2      -38.2    -25.8   -28.5
                                                        Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD              37.2      -35.5      -27.8           -22.3                 -47.1           -31.4          -56.3        -73.1     -30.9     -51.9     -16.9    -32.4   -39.3
                                                                                                Averaged Result
   Supervised           94.2      -47.0      -23.8               -0.7              -31.7           -14.3          -24.2        -39.4     -62.8     -23.3     -24.3    -17.9   -29.2
    Zero-shot            5.3      -24.2      -26.4           -37.1                 -30.1           -29.2          -25.3        -30.7     -29.8     -35.1     -30.4    -26.6   -29.8
       All              22.0      -28.5      -25.9           -30.3                 -30.4           -26.4          -25.1        -32.3     -36.0     -32.9     -29.2    -25.0   -29.7


Table 3: Overall source bias evaluation w.r.t. Relative ∆ (NDCG@1) across all benchmarked datasets in Cocktail.
The numbers (i.e., Relative ∆ > 0) suggest that retrieval models generally prefer human-written content while
the numbers (i.e., Relative ∆ ≤ 0) indicate retrieval models prefer LLM-generated content.


   Metric       BM25      + CE    + monoT5      DRAGON                  + CE         + monoT5              and tends to intensify during the second-stage re-
 NDCG@1         48.8      61.1       59.7           59.6 ↑10.8         61.0 ↓0.1      59.7 ↓0.0
 Relative ∆     22.0      -32.9      -29.2       -36.0 ↓58.0        -36.5 ↓3.6        -33.7 ↓4.5
                                                                                                           ranking. Moreover, as detailed in Table 4, enhanc-
                                                                                                           ing the efficiency of the first-stage retrieval by re-
Table 4: Re-ranking results with the top-100 retrieved                                                     placing BM25 with DRAGON does not necessarily
hits from a first-stage BM25 or DRAGON model.                                                              improve performance in the subsequent re-ranking
                                                                                                           phase. However, the source bias inherent in the
                                                                                                           first-stage retriever significantly impacts and may
Neural re-rankers generalize better but are still                                                          even magnify in subsequent re-ranking. This obser-
biased towards LLM-generated content. Neu-                                                                 vation underscores the critical need for developing
ral re-rankers, while achieving superior ranking                                                           holistic approaches to mitigate bias throughout the
performance on most datasets and showing en-                                                               retrieval pipeline, thereby ensuring fairness and
hanced generalization capabilities compared to                                                             accuracy in the whole IR system.
neural retrievers, are not exempt from pervasive
source bias. Specifically, re-ranking models like                                                          5.3      Further Analysis
CE and monoT5 exhibit a significant bias towards
LLM-generated content, sometimes even more pro-                                                            Impact of Different Pooling Strategies. Pooling
nounced than that observed in neural retrievers.                                                           strategies in PLMs are critical for aggregating infor-
This is particularly evident in datasets such as                                                           mation from the token embeddings for downstream
NQ and Touché-2020, further emphasizing the                                                                semantic matching. We explore the ranking per-
widespread nature of source bias in PLM-based                                                              formance and source bias on BERT and RoBERTa
neural retrieval models.                                                                                   w.r.t. different pooling strategies, including CLS
                                                                                                           token, max token, last token (Muennighoff, 2022),
Bias in the first retrieval stage tends to prop-                                                           mean (Reimers and Gurevych, 2019), and weighted
agate and even amplify during the re-ranking                                                               mean pooling (Muennighoff, 2022). The averaged
stage. This trend is particularly notable in datasets                                                      results of all benchmarked datasets in Cocktail are
like NFCorpus and Touché-2020, where the source                                                            shown in Figure 3. As we can see, the ranking
bias observed in the first retrieval stage persists                                                        performance and degree of source bias vary signifi-
                                                                                                    7058
           0.54                                                       0.50
                                                                                                                                                    Ranking           Source Bias
                                            -27.5
           0.52                                                       0.49
                                                                                                                                           52




                                                                                                                              NDCG@1 (%)
                                                                                                            -15
                                                                                                                                                                                    -23
  NDCG@1




                                                             NDCG@1
                                                Relative Δ




                                                                                                              Relative Δ
                                            -30.0




                                                                                                                                                                                      Relative Δ
                                                                      0.48
           0.50
                                            -32.5                     0.47                                  -20                            49                                       -26
           0.48
                         Ranking            -35.0
           0.46          Source Bias
                                                                      0.46
                                                                                                            -25
                                                                                                                                           46                                       -29
                                            -37.5                     0.45
                  mean cls   last max w-mean                                 mean cls   last   max w-mean
                                                                                                                                           43                                       -32
                                                                                                                                             mini      small      base        large
                      (a) BERT                                                (b) RoBERTa
                                                                                                                                            (11M)     (29M)     (110M)       (340M)
                                                                                                                                                         Model Size
Figure 3: Results of different pooling strategies. “w-
mean” denotes weighted mean pooling. A more nega-                                                                             Figure 4: Comparison of different model sizes. A more
tive Relative ∆ signifies increased source bias towards                                                                       negative Relative ∆ signifies increased source bias to-
LLM-generated content.                                                                                                        wards LLM-generated content.


cantly with the specific pooling strategy.                                                                                    performance and source bias, utilizing BERT mod-
   Weighted mean pooling demonstrates the most                                                                                els of varying sizes: mini, small, base, and large.
effectiveness for ranking, which can be attributed                                                                            As illustrated in Figure 4, an increase in model size
to the nuanced semantic understanding by posi-                                                                                leads to a notable enhancement in ranking perfor-
tionally weighting tokens, thus enhancing docu-                                                                               mance. However, this improvement is paralleled
ment relevance matching. Yet, this strategy also in-                                                                          by a rise in source bias (i.e., more negative).
curs the most severe source bias, possibly because                                                                               The trend indicates that larger models, with
LLM-generated texts have distinctive structural or                                                                            their enhanced semantic understanding and pro-
stylistic features that become more pronounced and                                                                            cessing capabilities, are more effective in judg-
amplified under weighted aggregation.                                                                                         ing document relevance, boosting their ranking
   Conversely, max pooling, which selects the max-                                                                            performance. However, the increased capabili-
imum value across each dimension from the to-                                                                                 ties may also make them more sensitive to the
ken embeddings, appears to be the least effective.                                                                            nuanced distinctions between human-written and
This could be due to its focus on the most domi-                                                                              LLM-generated texts, amplifying the source bias.
nant features within the text, potentially overlook-                                                                          Consequently, while the advanced performance of
ing the broader contextual nuances captured by                                                                                larger models is promising, it is coupled with a
other strategies. The dominance of specific features                                                                          more severe bias risk, posing a significant challenge
might not always align with the relevance signals                                                                             that merits more exploration in future research.
needed for accurate document ranking, explaining
the lower performance and less bias.                                                                                          6            Conclusion and Future Work
   Other strategies, such as mean, CLS token, and
                                                                                                                              This study proposes Cocktail, the first comprehen-
last token pooling, strike a balance by capturing
                                                                                                                              sive benchmark consisting of 16 diverse datasets
overall text representations while still highlighting
                                                                                                                              with mixed human-written and LLM-generated cor-
key tokens. However, the results show that while
                                                                                                                              pora. Alongside this, we present an evaluation tool
they are capable of supporting effective document
                                                                                                                              equipped with standardized data formats and eas-
ranking, they still suffer from severe source bias
                                                                                                                              ily adaptable evaluation codes for a wide array of
with Relative ∆ far below −10%.
                                                                                                                              retrieval models. This tool is designed to systemati-
   Overall, the variance in ranking performance and                                                                           cally evaluate ranking performance and source bias
source bias across pooling strategies underscores                                                                             in IR systems, both in supervised and zero-shot
the critical role of model architecture in retrieval                                                                          settings, paving the way for the development of
model design. This analysis suggests that while                                                                               more robust next-generation IR models.
weighted mean pooling offers enhanced ranking                                                                                    Utilizing Cocktail, we conduct an extensive eval-
capabilities, it comes with a trade-off of increased                                                                          uation of over ten state-of-the-art neural retrieval
source bias. Future work can explore hybrid or in-                                                                            models through more than 1,000 experiments. Our
novative pooling methods to balance performance                                                                               findings reveal a clear trade-off between ranking
with bias mitigation.                                                                                                         performance and source bias in neural retrieval
Impact of PLM Model Size. Our investigation                                                                                   models, underscoring the difficulty of enhancing
extends to the influence of model size on ranking                                                                             model performance without increasing bias to-
                                                                                                                           7059
wards LLM-generated content. This challenge em-           upon which next-generation IR models can be built.
phasizes the need for a suitable balance between
performance enhancement and bias mitigation in            Ethics Statement
the design of future IR models.
   The newly collected and annotated NQ-UTD               We commit to maintaining the highest ethical stan-
dataset comprises queries derived from recent             dards in our research, strictly adhering to ethical
events, featuring all content not yet incorporated        guidelines, applicable licenses, and laws. The 15
into the pre-training knowledge of most LLMs.             datasets utilized in this study are sourced from pub-
This characteristic renders it a valuable resource        lic repositories and have been employed within
for fairly evaluating the effectiveness of LLMs in        the bounds of their respective licenses and legal
processing new, unseen data, especially for LLM-          constraints. For the collected NQ-UTD dataset,
based retrieval or question-answering systems.            we followed stringent ethical protocols, ensuring
                                                          the corpus collected from online news sources was
Limitations                                               carefully screened and double-checked to remove
                                                          any personally identifiable or sensitive information.
We believe our proposed Cocktail benchmark is
                                                          Participants involved in data annotation were thor-
a foundational step toward advancing IR research
                                                          oughly informed about the process and provided
in the LLM era. Nonetheless, our work still has
                                                          informed consent before their participation.
several limitations for future research efforts. First,
while our benchmarked 16 datasets encompass a                We recognize the potential risks posed by large
broad range of IR domains and tasks, the IR field         language models (LLMs), such as generating harm-
is continually evolving, with new areas of interest       ful, biased, or incorrect content (Pan et al., 2023;
emerging regularly. Future updates to the Cocktail        Chen and Shu, 2023). The Llama2 model, used in
benchmark could benefit from including datasets           this study for corpus generation, is not immune to
from other IR domains, such as legal information          these issues and may inadvertently produce mis-
retrieval (Sansone and Sperlí, 2022). This expan-         leading content. We have taken measures to min-
sion would not only diversify but also enhance the        imize these risks, ensuring our benchmark aligns
benchmark’s utility across more specialized areas.        with ethical standards. Despite the acknowledged
Second, the scale of our NQ-UTD dataset is cur-           risks associated with LLMs, we assert that the
rently limited to 800 query-passage pairs, primarily      scientific benefits and insights derived from our
due to the high costs of human annotation. This           benchmark far outweigh potential concerns. Our
encompasses financial costs, the time required to         resources are intended solely for scientific research,
develop annotation guidelines, train annotators, and      designed to foster advancements in information
perform manual audits and validations. Future ini-        retrieval within this LLM era.
tiatives could focus on expanding the NQ-UTD
dataset, possibly by employing LLMs to support            Acknowledgements
and streamline the annotation process (Zhang et al.,
2023). Such an approach could facilitate broader          This work was funded by the National Key R&D
coverage and richer labeled query-passage pairs.          Program of China (2023YFA1008704), the Na-
Third, the construction of LLM-generated corpus           tional Natural Science Foundation of China (No.
in our benchmarked 16 datasets was significantly          62377044, No.62276248), Beijing Key Labora-
influenced by the inference costs of LLM, leading         tory of Big Data Management and Analysis Meth-
us to rely exclusively on Llama2 (Touvron et al.,         ods, Major Innovation & Planning Interdisciplinary
2023) for generating LLM-based content. How-              Platform for the “Double-First Class” Initiative,
ever, the real-world IR landscape is shaped by a          PCC@RUC, funds for building world-class univer-
variety of LLMs. Future research might include            sities (disciplines) of Renmin University of China,
content generated by an array of LLMs, such as            and the Youth Innovation Promotion Association
OpenAI ChatGPT and Google Gemini, to mirror               CAS under Grants No.2023111. This work was
the diversity of LLM-generated content more ac-           supported by the Fundamental Research Funds for
curately. Despite these limitations, we envision          the Central Universities, and the Research Funds of
the Cocktail benchmark as a valuable resource for         Renmin University of China (RUC24QSDL013).
IR research in the LLM era, offering a foundation
                                                      7060
References                                                   Sunhao Dai, Yuqi Zhou, Liang Pang, Weihao Liu, Xi-
                                                               aolin Hu, Yong Liu, Xiao Zhang, Gang Wang, and
Qingyao Ai, Ting Bai, Zhao Cao, Yi Chang, Jiawei               Jun Xu. 2024b. Neural retrievers are biased towards
  Chen, Zhumin Chen, Zhiyong Cheng, Shoubin Dong,              llm-generated content. Proceedings of the 30th ACM
  Zhicheng Dou, Fuli Feng, et al. 2023. Information            SIGKDD Conference on Knowledge Discovery and
  retrieval meets large language models: A strategic           Data Mining.
  report from chinese ir community. AI Open, 4:80–90.
                                                             Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Yoshua Bengio, Geoffrey Hinton, Andrew Yao, Dawn                Kristina Toutanova. 2019. BERT: Pre-training of
  Song, Pieter Abbeel, Yuval Noah Harari, Ya-Qin                deep bidirectional transformers for language under-
  Zhang, Lan Xue, Shai Shalev-Shwartz, Gillian Had-             standing. In Proceedings of the 2019 Conference
  field, et al. 2023. Managing ai risks in an era of rapid      of the North American Chapter of the Association
  progress. arXiv preprint arXiv:2310.17688.                    for Computational Linguistics: Human Language
                                                               Technologies, pages 4171–4186.
Alexander Bondarenko, Maik Fröbe, Meriem Be-
  loucif, Lukas Gienapp, Yamen Ajjour, Alexander             Thomas Diggelmann, Jordan Boyd-Graber, Jannis Bu-
  Panchenko, Chris Biemann, Benno Stein, Henning               lian, Massimiliano Ciaramita, and Markus Leip-
  Wachsmuth, Martin Potthast, et al. 2020. Overview            pold. 2020. Climate-fever: A dataset for verifica-
  of touché 2020: argument retrieval. In Experimental          tion of real-world climate claims. arXiv preprint
  IR Meets Multilinguality, Multimodality, and Interac-        arXiv:2012.00614.
  tion: 11th International Conference of the CLEF As-
  sociation, CLEF 2020, Thessaloniki, Greece, Septem-        Luyu Gao and Jamie Callan. 2022. Unsupervised cor-
  ber 22–25, 2020, Proceedings 11, pages 384–395.              pus aware language model pre-training for dense pas-
  Springer.                                                    sage retrieval. In Proceedings of the 60th Annual
                                                               Meeting of the Association for Computational Lin-
Vera Boteva, Demian Gholipour, Artem Sokolov, and              guistics (Volume 1: Long Papers), pages 2843–2853.
  Stefan Riezler. 2016. A full-text learning to rank
  dataset for medical information retrieval. In Ad-          Hans WA Hanley and Zakir Durumeric. 2023.
  vances in Information Retrieval: 38th European Con-          Machine-made media: Monitoring the mobiliza-
  ference on IR Research, ECIR 2016, Padua, Italy,             tion of machine-generated articles on misinforma-
  March 20–23, 2016. Proceedings 38, pages 716–722.            tion and mainstream news websites. arXiv preprint
  Springer.                                                    arXiv:2305.09820.
Canyu Chen and Kai Shu. 2023. Can llm-generated              Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisz-
  misinformation be detected?    arXiv preprint                tian Balog, Svein Erik Bratsberg, Alexander Kotov,
  arXiv:2309.13788.                                            and Jamie Callan. 2017. Dbpedia-entity v2: a test
                                                               collection for entity search. In Proceedings of the
Hongshen Chen, Xiaorui Liu, Dawei Yin, and Jiliang             40th International ACM SIGIR Conference on Re-
  Tang. 2017. A survey on dialogue systems: Re-                search and Development in Information Retrieval,
  cent advances and new frontiers. Acm Sigkdd Ex-              pages 1265–1268.
  plorations Newsletter, 19(2):25–35.
                                                             Sebastian Hofstätter, Sheng-Chieh Lin, Jheng-Hong
Arman Cohan, Sergey Feldman, Iz Beltagy, Doug                  Yang, Jimmy Lin, and Allan Hanbury. 2021. Ef-
  Downey, and Daniel Weld. 2020. SPECTER:                      ficiently teaching an effective dense retriever with
  Document-level representation learning using                 balanced topic aware sampling. In Proceedings of
  citation-informed transformers. In Proceedings               the 44th International ACM SIGIR Conference on
  of the 58th Annual Meeting of the Association                Research and Development in Information Retrieval,
  for Computational Linguistics, pages 2270–2282,              pages 113–122.
  Online. Association for Computational Linguistics.
                                                             Doris Hoogeveen, Karin M Verspoor, and Timothy Bald-
Nick Craswell, Bhaskar Mitra, Emine Yilmaz, and                win. 2015. Cqadupstack: A benchmark data set for
  Daniel Campos. 2021. Overview of the trec 2020               community question-answering research. In Proceed-
  deep learning track.                                         ings of the 20th Australasian document computing
                                                               symposium, pages 1–8.
Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel
  Campos, and Ellen M Voorhees. 2020. Overview               Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebas-
  of the trec 2019 deep learning track. arXiv preprint         tian Riedel, Piotr Bojanowski, Armand Joulin, and
  arXiv:2003.07820.                                            Edouard Grave. 2022. Unsupervised dense informa-
                                                               tion retrieval with contrastive learning. Transactions
Sunhao Dai, Chen Xu, Shicheng Xu, Liang Pang, Zhen-            on Machine Learning Research.
  hua Dong, and Jun Xu. 2024a. Unifying bias and
  unfairness in information retrieval: A survey of chal-     Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick
  lenges and opportunities with large language models.         Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and
  Proceedings of the 30th ACM SIGKDD Conference                Wen-tau Yih. 2020. Dense passage retrieval for open-
  on Knowledge Discovery and Data Mining.                      domain question answering. In Proceedings of the

                                                         7061
  2020 Conference on Empirical Methods in Natural             of transfer learning with a unified text-to-text trans-
  Language Processing (EMNLP), pages 6769–6781.               former. The Journal of Machine Learning Research,
                                                              21(1):5485–5551.
Tom Kwiatkowski, Jennimaria Palomaki, Olivia Red-
  field, Michael Collins, Ankur Parikh, Chris Alberti,     Nils Reimers and Iryna Gurevych. 2019. Sentence-
  Danielle Epstein, Illia Polosukhin, Jacob Devlin, Ken-     BERT: Sentence embeddings using Siamese BERT-
  ton Lee, et al. 2019. Natural questions: a benchmark       networks. In Proceedings of the 2019 Conference on
  for question answering research. Transactions of the       Empirical Methods in Natural Language Processing
  Association for Computational Linguistics, 7:453–          and the 9th International Joint Conference on Natu-
  466.                                                       ral Language Processing (EMNLP-IJCNLP), pages
                                                             3982–3992.
Zhenzhong Lan, Mingda Chen, Sebastian Goodman,
  Kevin Gimpel, Piyush Sharma, and Radu Soricut.           Stephen Robertson, Hugo Zaragoza, et al. 2009. The
  2019. Albert: A lite bert for self-supervised learn-        probabilistic relevance framework: Bm25 and be-
  ing of language representations. arXiv preprint            yond. Foundations and Trends® in Information Re-
  arXiv:1909.11942.                                           trieval, 3(4):333–389.

Hang Li. 2022. Learning to rank for information re-        Carlo Sansone and Giancarlo Sperlí. 2022. Legal infor-
  trieval and natural language processing. Springer          mation retrieval systems: State-of-the-art and open
  Nature.                                                    issues. Information Systems, 106:101967.

Hang Li, Jun Xu, et al. 2014. Semantic matching in         Weijia Shi, Sewon Min, Michihiro Yasunaga, Min-
  search. Foundations and Trends® in Information            joon Seo, Rich James, Mike Lewis, Luke Zettle-
  Retrieval, 7(5):343–469.                                  moyer, and Wen-tau Yih. 2023. Replug: Retrieval-
                                                            augmented black-box language models. arXiv
Sheng-Chieh Lin, Akari Asai, Minghan Li, Barlas Oguz,       preprint arXiv:2301.12652.
  Jimmy Lin, Yashar Mehdad, Wen-tau Yih, and Xilun
  Chen. 2023. How to train your dragon: Diverse            Krishna Srinivasan, Karthik Raman, Anupam Samanta,
  augmentation towards generalizable dense retrieval.        Lingrui Liao, Luca Bertelli, and Michael Bendersky.
  arXiv preprint arXiv:2302.07452.                           2022. Quill: Query intent with large language mod-
                                                             els using retrieval augmentation and multi-stage dis-
Yijin Liu, Xianfeng Zeng, Fandong Meng, and Jie Zhou.        tillation. In Proceedings of the 2022 Conference on
   2023. Instruction position matters in sequence gen-       Empirical Methods in Natural Language Processing:
   eration with large language models. arXiv preprint        Industry Track, pages 492–501.
   arXiv:2308.12097.
                                                           Weiwei Sun, Lingyong Yan, Zheng Chen, Shuaiqiang
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-         Wang, Haichao Zhu, Pengjie Ren, Zhumin Chen,
  dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,             Dawei Yin, Maarten de Rijke, and Zhaochun Ren.
  Luke Zettlemoyer, and Veselin Stoyanov. 2019.             2023a. Learning to tokenize for generative retrieval.
  Roberta: A robustly optimized bert pretraining ap-        In Thirty-seventh Conference on Neural Information
  proach. arXiv preprint arXiv:1907.11692.                  Processing Systems.

Macedo Maia, Siegfried Handschuh, André Freitas,           Weiwei Sun, Lingyong Yan, Xinyu Ma, Shuaiqiang
 Brian Davis, Ross McDermott, Manel Zarrouk, and            Wang, Pengjie Ren, Zhumin Chen, Dawei Yin, and
 Alexandra Balahur. 2018. Www’18 open challenge:            Zhaochun Ren. 2023b. Is ChatGPT good at search?
 financial opinion mining and question answering. In        investigating large language models as re-ranking
 Companion proceedings of the the web conference            agents. In Proceedings of the 2023 Conference on
 2018, pages 1941–1942.                                     Empirical Methods in Natural Language Processing,
                                                            pages 14918–14937.
Niklas Muennighoff. 2022. Sgpt: Gpt sentence
  embeddings for semantic search. arXiv preprint           Nandan Thakur, Nils Reimers, Andreas Rücklé, Ab-
  arXiv:2202.08904.                                          hishek Srivastava, and Iryna Gurevych. 2021. BEIR:
                                                             A heterogeneous benchmark for zero-shot evaluation
Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao,           of information retrieval models. In Thirty-fifth Con-
   Saurabh Tiwary, Rangan Majumder, and Li Deng.             ference on Neural Information Processing Systems
   2016. Ms marco: A human generated machine read-           Datasets and Benchmarks Track.
   ing comprehension dataset. choice, 2640:660.
                                                           James Thorne,       Andreas Vlachos,         Christos
Yikang Pan, Liangming Pan, Wenhu Chen, Preslav               Christodoulopoulos, and Arpit Mittal. 2018.
  Nakov, Min-Yen Kan, and William Yang Wang. 2023.           FEVER: a large-scale dataset for fact extraction
  On the risk of misinformation pollution with large         and VERification. In Proceedings of the 2018
  language models. arXiv preprint arXiv:2305.13661.          Conference of the North American Chapter of
                                                             the Association for Computational Linguistics:
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine          Human Language Technologies, Volume 1 (Long
  Lee, Sharan Narang, Michael Matena, Yanqi Zhou,            Papers), pages 809–819, New Orleans, Louisiana.
  Wei Li, and Peter J Liu. 2020. Exploring the limits        Association for Computational Linguistics.

                                                       7062
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-        Ruoyu Zhang, Yanzeng Li, Yongliang Ma, Ming Zhou,
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay            and Lei Zou. 2023. LLMaAA: Making large lan-
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti        guage models as active annotators. In Findings of the
  Bhosale, et al. 2023. Llama 2: Open founda-               Association for Computational Linguistics: EMNLP
  tion and fine-tuned chat models. arXiv preprint           2023, pages 13088–13103.
  arXiv:2307.09288.
                                                          Wayne Xin Zhao, Jing Liu, Ruiyang Ren, and Ji-Rong
Ellen Voorhees, Tasmeer Alam, Steven Bedrick, Dina         Wen. 2023a. Dense text retrieval based on pretrained
   Demner-Fushman, William R Hersh, Kyle Lo, Kirk          language models: A survey. ACM Trans. Inf. Syst.
   Roberts, Ian Soboroff, and Lucy Lu Wang. 2021.
   Trec-covid: constructing a pandemic information re-    Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang,
   trieval test collection. In ACM SIGIR Forum, vol-       Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen
   ume 54, pages 1–12. ACM New York, NY, USA.              Zhang, Junjie Zhang, Zican Dong, et al. 2023b. A
                                                           survey of large language models. arXiv preprint
David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu              arXiv:2303.18223.
  Wang, Madeleine van Zuylen, Arman Cohan, and
  Hannaneh Hajishirzi. 2020. Fact or fiction: Verifying   Yujia Zhou, Jing Yao, Zhicheng Dou, Ledell Wu, and Ji-
  scientific claims. In Proceedings of the 2020 Con-        Rong Wen. 2022. Dynamicretriever: A pre-training
  ference on Empirical Methods in Natural Language          model-based ir system with neither sparse nor dense
  Processing (EMNLP), pages 7534–7550, Online. As-          index. arXiv preprint arXiv:2203.00537.
  sociation for Computational Linguistics.
                                                          Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan
Liang Wang, Nan Yang, and Furu Wei. 2023.                   Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou,
  Query2doc: Query expansion with large language            and Ji-Rong Wen. 2023. Large language models
  models. arXiv preprint arXiv:2303.07678.                  for information retrieval: A survey. arXiv preprint
                                                            arXiv:2308.07107.
Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan
 Yang, and Ming Zhou. 2020. Minilm: Deep self-
 attention distillation for task-agnostic compression
 of pre-trained transformers. Advances in Neural In-
 formation Processing Systems, 33:5776–5788.

Shitao Xiao, Zheng Liu, Yingxia Shao, and Zhao Cao.
  2022. Retromae: Pre-training retrieval-oriented lan-
  guage models via masked auto-encoder. In Proceed-
  ings of the 2022 Conference on Empirical Methods
  in Natural Language Processing, pages 538–548.

Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang,
  Jialin Liu, Paul Bennett, Junaid Ahmed, and Arnold
  Overwijk. 2020. Approximate nearest neighbor neg-
  ative contrastive learning for dense text retrieval.
  arXiv preprint arXiv:2007.00808.

Shicheng Xu, Danyang Hou, Liang Pang, Jingcheng
  Deng, Jun Xu, Huawei Shen, and Xueqi Cheng. 2024.
  Invisible relevance bias: Text-image retrieval models
  prefer ai-generated images. Proceedings of the 47th
  international ACM SIGIR conference on research
  and development in information retrieval.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
  William Cohen, Ruslan Salakhutdinov, and Christo-
  pher D. Manning. 2018. HotpotQA: A dataset for
  diverse, explainable multi-hop question answering.
  In Proceedings of the 2018 Conference on Empiri-
  cal Methods in Natural Language Processing, pages
  2369–2380, Brussels, Belgium. Association for Com-
  putational Linguistics.

Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai,
  Eric Sun, and Yue Zhang. 2023. A survey on
  large language model (llm) security and privacy:
  The good, the bad, and the ugly. arXiv preprint
  arXiv:2312.02003.

                                                      7063
A    Dataset Details                                      A.1.2   MS MARCO
                                                          MS MARCO (Nguyen et al., 2016), developed
In this section, we provide details about the datasets    by Microsoft Research, is a cornerstone dataset
in Cocktail. Table 5 lists the dataset website links      in the fields of natural language processing (NLP)
and the corresponding licenses.                           and information retrieval (IR). This dataset com-
                                                          prises over a million user-generated questions de-
                                                          rived from Bing search logs, tailored to advance
A.1 Detailed Description of Datasets                      three primary NLP tasks: document ranking, pas-
                                                          sage retrieval, and question answering. Within
A.1.1   NQ-UTD
                                                          our Cocktail benchmark, we specifically utilize
The Natural Question-Up To Date (NQ-UTD)                  the passage retrieval subset, which contains 532K
dataset comprises 80 questions focusing on re-            labeled query-passage pairs. A majority of the
cent hotspot events from November 2023 to Jan-            open-sourced pre-trained transformer checkpoints
uary 2024. These questions span eight domains:            have been trained using this dataset. Following
Sports, News, Science, Technology, Autos, Music,          previous studies (Thakur et al., 2021; Lin et al.,
Movies, and Games, with approximately 10 queries          2023), we employ the MS MARCO Dev set as the
per domain related to the latest events, question-        supervised evaluation test set.
ing about their times, locations, or other specifics.     A.1.3   TREC
To gather relevant passages for each query, we
searched these questions on platforms like Google,        DL19. The DL19 (TREC Deep Learning Track
X (formerly Twitter), Reddit, Wikipedia, Quora,           2019) dataset (Craswell et al., 2020), is a key re-
and Facebook. Following the practice in Sun et al.        source for exploring ad hoc ranking across exten-
(2023b), we also conducted searches using key-            sive datasets from various domains. Our study
words to retrieve passages that are partially rel-        focuses on the passage retrieval task utilizing the
evant but do not directly answer the questions.           DL19 dataset, which comprises 43 queries and uses
We also queried these questions with the latest           the MS MARCO passage corpus. This allows for
state-of-the-art LLMs, gpt-4-1106-preview and             its application in supervised evaluation settings.
gemini-pro, which have their knowledge bases              DL20. The DL20 dataset (Craswell et al., 2021)
updated only until April 2023. The results show           comes from the second year of the TREC Deep
their 0% accuracy in answering questions from our         Learning Track, and also focuses on ad hoc rank-
test set, confirming that these LLMs had no pre-          ing through human-annotated training sets across
knowledge about these questions. The collected            diverse domains. We also focus on the passage
800 documents were then manually annotated for            ranking task featured in the DL20 dataset, which
relevance by the authors and their highly educated        includes 54 queries and also leverages the MS
colleagues. Each document received a relevance            MARCO passage corpus. This also allows for its
score: 0 for not relevant, 1 for partially relevant       application in supervised evaluation settings.
(mentioning some aspects of the query but not fully
answering it), and 2 for relevant (providing a com-       A.1.4   BEIR
plete answer to the query). To ensure consistent          If not specified, we utilize the preprocessed ver-
and high-quality annotations, each document was           sion of the following open-sourced datasets as
reviewed by five individuals, with a majority vote        included in the BEIR benchmark (Thakur et al.,
determining the final label.                              2021) to serve as the human-written seed datasets
   The statistics and examples of the NQ-UTD              in our Cocktail benchmark, ensuring consistency
dataset are presented in Table 6 and Table 7, respec-     and comparability in our evaluations.
tively. Note that this dataset also offers a fair eval-   TREC-COVID. The TREC-COVID dataset is
uation of the current capabilities of the advanced        developed by the Text REtrieval Conference
LLM-based IR models. As NQ-UTD contains con-              (TREC) (Voorhees et al., 2021), specifically de-
tent not previously included in LLM training data,        signed to address the challenges of biomedical in-
it can serve as a valuable resource for evaluating        formation retrieval in the context of the COVID-19
LLMs’ ability to process and answer queries on            pandemic. This dataset represents a concerted ef-
recent events.                                            fort to harness the rapidly expanding collection of
                                                      7064
 Dataset                                  Official Website Link                                        License
 MS MARCO            https://microsoft.github.io/msmarco/                              MIT License
 DL19                https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019       CC BY 4.0 license
 DL20                https://microsoft.github.io/msmarco/TREC-Deep-Learning-2020       CC BY 4.0 license
 TREC-COVID          https://ir.nist.gov/covidSubmit/index.html                        Dataset License Agreement
 NFCorpus            https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
 NQ                  https://ai.google.com/research/NaturalQuestions                   CC BY-SA 3.0 license
 HotpotQA            https://hotpotqa.github.io                                        CC BY-SA 4.0 license
 FiQA-2018           https://sites.google.com/view/fiqa/
 Touché-2020         https://webis.de/events/touche-20/shared-task-1.html              CC BY 4.0 license
 CQADupStack         http://nlp.cis.unimelb.edu.au/resources/cqadupstack/              License 2.0 license
 DBPedia             https://github.com/iai-group/DBpedia-Entity/                      CC BY-SA 3.0 license
 SCIDOCS             https://allenai.org/data/scidocs                                  GNU General Public License v3.0 license
 FEVER               http://fever.ai                                                   CC BY-SA 3.0 license
 Climate-FEVER       http://climatefever.ai
 SciFact             https://github.com/allenai/scifact                                CC BY-NC 2.0 license
 NQ-UTD              https://github.com/KID-22/Cocktail                                MIT License

Table 5: Website links and licenses for the benchmarked datasets in Cocktail. (Note: Licenses for NFCorpus,
FiQA-2018, and Climate-FEVER are not provided by the authors).

                                                # Relevancy Scores                      # Source
        Domain        # Queries   # Passages
                                                 0      1        2    Google   X     Reddit Wikipedia Quora     Facebook
         Sports          12          120        66      17      37      60     22     10       19       9          0
          News           13          130        78      14      38      68     23     11       13      15          0
        Scientific       10          100        68      12      20      59     10      8        6       9          8
       Technology        12          120        92       1      27     64       6      4       12      13         21
         Autos           8           80         50      15      15     51       6      1        7      11          4
         Music           10          100        60      18      22      67      6      8        5      14          0
         Movies          7           70         41      8       21     53       2      3        9       3          0
         Games           8           80         48       9      23     56       3      9        8       4          0
           All           80          800       503      94     203     478     78     54       79      78         33

Table 6: Statistics of our proposed NQ-UTD dataset. The column ‘# Relevancy Scores’ represents the count of
documents categorized by their respective relevance levels.


scholarly articles related to COVID-19, providing                    crafted to evaluate the effectiveness of models in
a focused resource for biomedical IR.                                deciphering complex, multi-hop questions and de-
                                                                     livering precise answers.
NFCorpus. The NFCorpus dataset (Boteva et al.,
2016) serves as a detailed resource tailored for rank-               FiQA-2018. FiQA-2018 (Financial Opinion Min-
ing tasks within the biomedical field. A distinctive                 ing and Question Answering-2018) (Maia et al.,
aspect of NFCorpus is its meticulously curated rele-                 2018) presents a specialized question-answering
vance links, connecting queries directly to pertinent                challenge within the financial domain. The dataset
research articles.                                                   benefits from a comprehensive corpus gathered
                                                                     from esteemed financial news platforms, analyst
NQ. The NQ (Natural Questions) dataset aims to
                                                                     reports, and influential financial blogs.
propel advancements in natural language under-
standing, particularly focusing on the question-                     Touché-2020. Touché-2020 dataset (Bondarenko
answering task (Kwiatkowski et al., 2019). This                      et al., 2020) was created with the specific aim of
dataset is compiled from real questions submitted                    advancing the field of argument retrieval. Its pur-
by users on Google search, each annotated with                       pose is to identify argumentative content relevant
answers extracted from Wikipedia articles.                           to contentious queries. It contains argumentative
                                                                     passages from a broad spectrum of domains, which
HotpotQA. HotpotQA (Yang et al., 2018) is a
                                                                     are carefully selected and annotated.
large-scale dataset that includes diverse questions
posed by human participants. These questions ne-                     CQADupStack. CQADupStack (Hoogeveen et al.,
cessitate a multi-step reasoning process, often re-                  2015) is a popular dataset for duplicate question
quiring the extraction of answers from extensive                     retrieval, which aims to identify duplicate ques-
Wikipedia texts and the identification of supporting                 tions in community question answering (cQA) fo-
evidence within them. HotpotQA is specifically                       rums. This dataset includes carefully annotated
                                                              7065
 Domain       Question                                                                  Reference Answer
 Sports       Who is the MVP of the first NBA In-Season Tournament?                     LeBron James
 Sports       Who wins 2023 FIFA Club World Cup?                                        Manchester City F.C.
 News         Where was the 44th Gulf Cooperation Council (GCC) Summit held?            Doha, Qatar
 News         Which country will take over as the rotating chair of the APEC in 2024?   Peru
 Scientific   Which paper won NeurIPS2023 Test of Time Award?                           Distributed Representations of Words
                                                                                        and Phrases and their Compositionality
 Scientific   Which university designed AI Coscientist?                                 Carnegie Mellon University
 Technology   Which company released the machine learning framework MLX?                Apple
 Technology   What is the maximum number of cores in Intel fifth-generation Xeon CPU?   64
 Autos        When did Xiaomi announce SU7?                                             Dec 2023
 Autos        The country with the largest automobile export volume in 2023?            China
 Music        Which singer was named the 2023 Person of the Year by Time magazine?      Taylor Swift
 Music        When did Les McCann pass away?                                            December 29, 2023
 Moves        Which movie was the highest-grossing film worldwide in 2023?              Barbie
 Moves        Which actress won the Best Actress award at the European Film Awards?     Sandra Wheeler
 Games        Which team is the champion of the League of Legends S13 Finals?           SKT T1
 Games        Which one is the best-selling games in the US 2023?                       Hogwarts Legacy

 Table 7: Examples of queries and reference answers from different domains of our proposed NQ-UTD dataset.


and categorized questions and answers across vari-                mation to adjudicate each claim.
ous domains. To maintain focus without losing the                 SciFact. SciFact (Wadden et al., 2020) is designed
essence of generalizability, our study incorporates               for the verification of scientific claims sourced from
a subset from the English domains as our selected                 peer-reviewed literature, with each claim meticu-
CQADupStack dataset.                                              lously matched with corroborative or refuting evi-
DBPedia. The DBPedia dataset (Hasibi et al.,                      dence from related studies. The dataset comprises
2017) includes structured information about en-                   expert-crafted scientific claims alongside abstracts
tities, concepts, categories, and their relationships,            containing evidence, each annotated with labels
gathered from Wikipedia entries. This dataset fo-                 indicating support or contradiction, and rationales
cuses on the entity retrieval task, where queries                 explaining the basis of the evidence.
aim to retrieve relevant entities from the English
DBpedia corpus dated October 2015.                                A.2     Dataset Processing and Quality Control

SCIDOCS. The SCIDOCS dataset (Cohan et al.,                       Given the substantial computational cost associated
2020) is a vast collection of scholarly articles from             with rewriting documents for the 16 datasets using
the Semantic Scholar database, enhanced with                      Large Language Models (LLMs), we adopted sam-
detailed metadata extraction and annotations. It                  pling methods in line with practices from Zhou
serves as a robust dataset for the citation prediction            et al. (2022); Sun et al. (2023a). Specifically, for
task, where the objective is to identify papers cited             datasets with an original corpus size smaller than
by a given query paper title.                                     200,000 documents, we retained the entire corpus
                                                                  without filtering. For datasets exceeding 100,000
FEVER. The FEVER (Fact Extraction and VERifi-                     documents, we retain all candidate documents that
cation) dataset (Thorne et al., 2018) comes from the              appear in the labeled data (including train, valid,
fact-checking domain, offering a curated collection               and test set). If the number of documents post-
of human-labeled claims sourced from Wikipedia.                   filtering fell below 100,000, we supplemented the
Each claim is meticulously classified as Supported,               corpus with a random selection of up to 100,000
Refuted, or NotEnoughInfo, setting the stage for a                additional documents from the remaining corpus
nuanced fact-checking task.                                       to ensure a challenging dataset size.
Climate-FEVER. Climate-FEVER (Diggelmann                              Documents with text lengths between 10 and
et al., 2020) is a specialized dataset focused on                 2,000 words are retained for each corpus. This cri-
the area of climate science, comprising real-world                terion was set because texts shorter than 10 words
claims accompanied by evidence sentences from                     often consisted of empty texts or symbols, com-
Wikipedia. Similar to the FEVER dataset, the pri-                 promising data quality—this was particularly evi-
mary task involves evaluating whether the provided                dent in the TREC-COVID dataset, which contained
evidence supports, refutes, or lacks sufficient infor-            over 40,000 documents with empty text. Con-
                                                             7066
versely, texts over 2,000 words were filtered out        the original human-written content. We also com-
to satisfy the context length limitation of 4,096        pare the semantics between randomly selected <hu-
tokens for rewriting with Llama2, impacting only         man doc, LLM doc> pairs and matching pairs <hu-
0.05% of the data. These filters did not significantly   man doc, LLM doc>, as shown in Table 9. The
alter the overall data distribution, with a total of     average similarity score for matching pairs was
less than 1% data removed, and our evaluation re-        0.9816, significantly higher than the 0.7135 aver-
sults align closely with those reported in the BEIR      age for random pairs. This significant statistical
benchmark (Thakur et al., 2021) for the original         difference supports the close semantic alignment
datasets, as shown in Table 2. For most datasets,        between LLM-generated and human-authored doc-
we generated LLM Corpus once. However, for MS            uments, further validating the quality of our con-
MARCO, HotpotQA, DBPedia, and NQ-UTD, to                 structed dataset. Further, evaluations of various
construct a more challenging benchmark for evalu-        retrieval models on sole human-written or LLM-
ating source bias in IR models, we generated mul-        generated corpora, as detailed in Table 8, demon-
tiple versions and used BERT to filter and merge         strate consistent performance across all datasets
the corpus, aiming to increase the task difficulty.      between two types of corpus. These observations
   When LLM is used for rewriting, LLM will in-          across all datasets reinforce confidence in the qual-
evitably refuse to rewrite due to safety constraints,    ity of our newly constructed datasets, suggesting
especially for datasets like Touché-2020, which fo-      that the LLM-generated content maintains seman-
cus on retrieving contentious viewpoints. For such       tics comparable to human-written texts for IR tasks.
LLM-generated data, we keep the same content             Quality Verification with Human Evaluation. To
as the human-written counterparts. This approach         further validate the assigned relevancy label, we
allows for the easy removal of refused rewrites if       also conduct a human evaluation study. Due to cost
necessary, ensuring both the integrity and the qual-     constraints of human evaluation, we sample 20
ity of the dataset processing and control measures       <query, human doc, LLM doc> triples from each of
implemented. The statistics of the 16 benchmarked        the 16 datasets included in Cocktail. These triples
datasets in Cocktails are summarized in Table 1.         were annotated by graduate students and our col-
A.3 Dataset Statistics and Analysis                      leagues, who were asked to assess which document
                                                         is more semantically relevant to the given query,
Term-based Statistics. Figure 5 illustrates the          with options being “human doc”, “LLM doc”, or
distribution of text lengths, revealing minimal vari-    “equal”. At least three different annotators evalu-
ation between the lengths of texts. We then calcu-       ated each triple, with the majority vote deciding the
lated the Jaccard similarity and overlap between         final label. We summarized the results in Table 10,
each LLM-generated document dG and the corre-            with numbers in parentheses indicating the percent-
sponding human-written document dH , using the           age of agreement among all three evaluators for
following two formulas:                                  each option. The results show a comparable level
                                     T                   of semantic relevance between human-written and
                                 |dG dH |                LLM-generated texts for the given queries, ensur-
          Jaccard similarity = G S H ,
                                 |d     d |              ing the fairness of our analysis of source bias.
                                   G
                                     T H
                                 |d     d |
                    Overlap =         H
                                            .            A.4    Dataset Examples
                                    |d |
                                                         For a better understanding of the datasets used in
The results presented in Figure 6 highlight signif-      our Cocktail benchmark, we offer examples for
icant differences in terms despite their ostensibly      each dataset in Table 12, showcasing a given query
similar semantic information.                            along with the corresponding relevant human-
Semantic Analysis. Cosine similarity between             written document and LLM-generated document.
LLM-generated and human-written documents, cal-
culated using the OpenAI embedding model4 , is           B     Model Details
displayed in Figure 7. The results, predominantly        B.1    Detailed Description of Models
above 0.9, signify a high level of semantic preser-
                                                         We select the widely used approach BM25 (Robert-
vation in the LLM-generated texts compared to
                                                         son et al., 2009) as the representation of lexical
   4
       text-embedding-ada-002                            retrieval models in our benchmark.
                                                     7067
                         Lexical                                      Neural Retrievers                                 Neural Re-rankers
   Model (→)
                         BM25      BERT    RoBERTa   ANCE     TAS-B     Contriever coCondenser   RetroMAE   DRAGON      CE      monoT5
                 Human    38.6      49.9     49.8     51.4     54.2        55.3         54.1        55.2      60.2      58.3     56.8
  MS MARCO
                  LLM     34.3      49.5     50.1     50.1     51.8        53.5         52.4        53.0      56.2      55.2     53.7
                 Human    56.2      77.1     79.5     72.1     76.4        74.4         77.9        76.4      76.7      80.2     78.7
     DL19
                  LLM     51.2      79.8     73.6     68.2     73.3        70.9         79.5        76.0      79.1      81.0     80.6
                 Human    54.6      74.7     75.3     73.5     75.9        73.2         78.7        73.5      81.8      79.6     76.9
     DL20
                  LLM     45.7      79.3     73.8     76.2     71.9        75.6         77.5        79.3      78.7      75.3     76.5
                 Human    62.0      63.0     61.0     74.0     75.0        64.0         73.0        79.0      75.0      68.0     83.0
  TREC-COVID
                  LLM     63.0      63.0     60.0     67.0     63.0        60.0         70.0        73.0      65.0      75.0     86.0
                 Human    43.8      38.4     32.5     33.4     40.9        42.9         43.0        40.3      42.6      49.2     48.9
   NFCorpus
                  LLM     45.8      37.5     36.1     34.1     41.0        42.3         43.5        41.8      43.2      49.7     48.4
                 Human    44.8      61.4     59.5     58.9     64.3        69.3         64.5        66.5      69.9      68.5     69.3
      NQ
                  LLM     43.5      60.5     57.8     58.1     64.0        68.1         63.8        66.3      68.9      68.0     68.0
                 Human    83.9      74.1     61.5     70.4     84.2        88.0         80.8        88.2      89.0      94.2     91.1
   HotpotQA
                  LLM     80.7      73.7     62.3     70.8     83.4        87.3         81.1        87.2      88.2      92.6     89.6
                 Human    23.3      23.3     24.5     27.8     28.7        31.3         27.3        30.1      35.5      33.0     40.0
   FiQA-2018
                  LLM     22.1      23.3     21.5     26.2     25.3        31.2         24.7        29.2      33.3      33.2     37.0
                 Human    52.0      46.9     40.8     49.0     55.1        48.0         38.8        44.9      43.9      51.0     53.1
  Touché-2020
                  LLM     57.1      46.9     49.0     41.8     38.8        37.8         27.6        44.9      55.1      58.2     51.0
                 Human    28.1      24.3     24.3     29.9     23.1        33.6         32.9        30.5      36.0      33.9     35.7
  CQADupStack
                  LLM     22.8      24.1     23.5     26.7     21.0        29.8         28.9        28.0      32.1      29.7     31.3
                 Human    34.1      54.3     49.0     46.8     56.6        61.8         57.4        57.8      60.5      60.8     37.0
    DBPedia
                  LLM     33.9      55.3     49.4     48.5     55.8        62.1         57.8        56.5      59.6      59.0     33.0
                 Human    16.0      13.5     11.3     14.4     15.8        16.7         14.2        16.1      17.2      18.8     19.6
   SCIDOCS
                  LLM     15.9      11.8     11.8     13.6     15.1        16.0         14.4        15.9      17.2      18.4     19.5
                 Human    65.2      79.0     74.4     79.5     82.3        85.4         72.2        87.2      86.8      89.8     25.5
    FEVER
                  LLM     63.0      79.1     73.3     80.0     82.3        85.6         74.5        86.5      87.1      89.2     24.2
                 Human    25.9      26.8     27.2     29.5     32.1        32.8         28.1        33.6      34.3      36.0     35.9
 Climate-FEVER
                  LLM     24.3      25.9     26.2     28.0     32.6        31.3         27.6        31.0      33.2      34.4     33.9
                 Human    53.0      35.3     38.3     38.7     52.7        54.3         46.3        53.0      53.7      54.3     64.0
    SciFact
                  LLM     56.3      35.3     39.7     39.3     50.7        53.0         46.7        51.7      52.7      53.0     63.7
                 Human    71.9      75.6     63.1     76.3     81.3        77.5         73.1        80.0      76.9      88.1     89.4
    NQ-UTD
                  LLM     73.1      75.0     68.8     77.5     81.3        76.3         71.3        76.9      78.8      89.4     88.1


Table 8: Performance comparison (NDCG@1) of retrieval models on Cocktail benchmark using the sole human-
written or LLM-generated corpus.


        Dataset       Matching Pairs         Random Pairs                    Dataset       Human Doc       LLM Doc            Equal
     MS MARCO        0.9802 (±0.0138)      0.6725 (±0.0369)               MS MARCO        0.0% (0.0%)    10.0% (0.0%)      90% (77.8%)
         DL19        0.9798 (±0.0145)      0.6733 (±0.0373)                   DL19        0.0% (0.0%)     5.0% (0.0%)     95.0% (94.7%)
         DL20        0.9817 (±0.0133)      0.6728 (±0.0362)                   DL20        5.0% (0.0%)     0.0% (0.0%)     95.0% (78.9%)
    TREC-COVID       0.9875 (±0.0088)      0.7502 (±0.0436)              TREC-COVID       5.0% (0.0%)     5.0% (0.0%)      90% (61.1%)
                                                                            NFCorpus       0.0% (0.0%)    0.0% (0.0%)    100.0% (75.0%)
       NFCorpus      0.9856 (±0.0096)      0.7490 (±0.0373)
                                                                               NQ         0.0% (0.0%)    0.0% (0.0%)    100.0% (100.0%)
          NQ         0.9847 (±0.0150)      0.6996 (±0.0348)
                                                                            HotpotQA      0.0% (0.0%)    0.0% (0.0%)     100.0% (80.0%)
       HotpotQA      0.9905 (±0.0123)      0.7073 (±0.0366)                FiQA-2018       5.0% (0.0%)    0.0% (0.0%)     95.0% (68.4%)
      FiQA-2018      0.9657 (±0.0243)      0.7216 (±0.0372)               Touché-2020     0.0% (0.0%)    0.0% (0.0%)    100.0% (70.0%)
     Touché-2020     0.9693 (±0.0262)      0.7274 (±0.0359)              CQADupStack       5.0% (0.0%)    5.0% (0.0%)      90% (83.3%)
    CQADupStack      0.9583 (±0.0336)      0.7360 (±0.0311)                  DBPedia       0.0% (0.0%)    0.0% (0.0%)    100.0% (85.0%)
        DBPedia      0.9900 (±0.0121)      0.7023 (±0.0373)                 SCIDOCS       0.0% (0.0%)     0.0% (0.0%)   100.0% (100.0%)
       SCIDOCS       0.9863 (±0.0112)      0.7444 (±0.0352)                  FEVER        5.0% (0.0%)     0.0% (0.0%)     95.0% (84.2%)
        FEVER        0.9866 (±0.0110)      0.6983 (±0.0363)              Climate-FEVER     0.0% (0.0%)    0.0% (0.0%)    100.0% (90.0%)
    Climate-FEVER    0.9873 (±0.0107)      0.6992 (±0.0366)                  SciFact      10.0% (0.0%)    5.0% (0.0%)     85.0% (64.7%)
        SciFact      0.9881 (±0.0084)      0.7484 (±0.0445)                 NQ-UTD        0.0% (0.0%)    0.0% (0.0%)     100.0% (90.0%)
       NQ-UTD        0.9833 (±0.0122)      0.7138 (±0.0443)                   Avg.            2.2%           1.9%             95.9%
         Avg.        0.9816 (±0.0150)      0.7135 (±0.0376)
                                                                       Table 10: Human evaluation of semantic relevance be-
Table 9: Comparison of cosine similarity scores between                tween human-written and LLM-generated documents
matching and random pairs for each dataset.                            across all datasets in the Cocktail benchmark.


   For neural retrieval models that leverage pre-                       tuned on the MSMARCO dataset using the official
trained language models to acquire semantic re-                         BEIR benchmark training script.
lationships between queries and documents, we                              RoBERTa (Liu et al., 2019) builds on BERT’s
select the following representative and state-of-the-                   success with more data and refined training tech-
art models:                                                             niques to enhance performance. RoBERTa was
   BERT (Devlin et al., 2019), a foundational pre-                      fine-tuned in the same manner to BERT, using the
trained language model, is commonly used as an                          MSMARCO dataset.
encoder in dense retrieval systems. It was fine-                           ANCE (Xiong et al., 2020) improves dense re-
                                                                7068
   Probability                               Human                                              Human                                                 Human
                                                                                                                                                                                 0.06                  Human




                                                        Probability




                                                                                                             Probability




                                                                                                                                                                   Probability
                 0.2                                                  0.2                                                  0.2
                                             LLM                                                LLM                                                   LLM                        0.04                  LLM
                 0.1                                                  0.1                                                  0.1                                                   0.02
                 0.0                                                  0.0                                                  0.0                                                   0.00
                        0           500         1000                         0            500        1000                          0            500        1000                         0        500       1000
                                 Text Length                                          Text Length                                           Text Length                                      Text Length

                       (a) MS MARCO                                                  (b) DL19                                              (c) DL20                                (d) TREC-COVID

                                                                      0.10
                                                                                                Human                                                                            0.10                  Human
                                                        Probability




                                                                                                                                                                   Probability
                                                                                                                                                      Human




                                                                                                             Probability
                                             Human
   Probability




                 0.075                                                                          LLM                        0.10                                                                        LLM
                                             LLM                                                                                                      LLM
                 0.050                                                0.05                                                                                                       0.05
                                                                                                                           0.05
                 0.025
                 0.000                                                0.00                                                 0.00                                                  0.00
                             0       500        1000                             0        500        1000                          0            500        1000                          0       500       1000
                                  Text Length                                          Text Length                                           Text Length                                     Text Length

                         (e) NFCorpus                                                 (f) NQ                                       (g) HotpotQA                                         (h) FiQA-2018


                 0.075                                                                          Human                                                 Human                                            Human
                                                        Probability




                                                                                                             Probability




                                                                                                                                                                   Probability
                                             Human                    0.10                                                 0.15                                                  0.06
   Probability




                                             LLM                                                LLM                                                   LLM                                              LLM
                 0.050                                                                                                     0.10                                                  0.04
                                                                      0.05
                 0.025                                                                                                     0.05                                                  0.02
                 0.000                                                0.00                                                 0.00                                                  0.00
                             0       500        1000                         0            500        1000                          0            500        1000                         0        500       1000
                                  Text Length                                          Text Length                                           Text Length                                     Text Length

                        (i) Touché-2020                                  (j) CQADupStack                                               (k) DBPedia                                      (l) SCIDOCS

                                                                                                                                                                                 0.15
                                            Human                                               Human
  Probability




                                                       Probability




                                                                                                                                                                  Probability
                                                                                                                           0.075                      Human                                            Human
                                                                                                            Probability




                 0.10                                                 0.10
                                            LLM                                                 LLM                                                   LLM                        0.10                  LLM
                                                                                                                           0.050
                 0.05                                                 0.05                                                                                                       0.05
                                                                                                                           0.025
                 0.00                                                 0.00                                                 0.000                                                 0.00
                         0           500        1000                         0            500        1000                              0        500        1000                         0       500        1000
                                 Text Length                                          Text Length                                            Text Length                                     Text Length

                         (m) FEVER                                     (n) Climate-FEVER                                               (o) SciFact                                      (p) NQ-UTD

                                           Figure 5: Distribution of text length of corpus for each dataset in Cocktail.


trieval by selecting challenging negatives across                                                                    Auto-Encoder approach for pretraining, enhancing
the corpus and updating the Approximate Nearest                                                                      sentence reconstruction from masked inputs to re-
Neighbor (ANN) index asynchronously with each                                                                        fine language modeling.
training iteration.                                                                                                     DRAGON (Lin et al., 2023) applies progressive
   TAS-B (Hofstätter et al., 2021), a bi-encoder                                                                     supervision and query augmentation for effective
model, leverages balanced margin sampling for ef-                                                                    dense retrieval, suitable for both supervised and
ficient query selection and dual supervision from a                                                                  zero-shot settings.
cross-encoder and a ColBERT model for enhanced                                                                          Additionally, the following two widely used neu-
learning.                                                                                                            ral re-ranking models are also adopted in our eval-
   Contriever (Izacard et al., 2022) employs con-                                                                    uation framework:
trastive learning with positive samples generated                                                                       CE (Wang et al., 2020) is a cross-encoder model
through cropping and token sampling, using MoCo                                                                      pre-trained on MS MARCO dataset (Nguyen et al.,
to incorporate negatives from a queue of previous                                                                    2016) through knowledge distillation from three
batches for self-supervised training.                                                                                teacher models: BERT-base (Devlin et al., 2019),
   coCondenser (Gao and Callan, 2022) under-                                                                         BERT-large (Devlin et al., 2019), and ALBERT-
takes a two-stage process beginning with pretrain-                                                                   large (Lan et al., 2019).
ing and unsupervised contrastive loss for embed-                                                                        monoT5 (Raffel et al., 2020) is a sequence-
ding generation, followed by supervised training                                                                     to-sequence re-ranker based on T5 (Raffel et al.,
with the pre-trained encoder.                                                                                        2020), which is also pre-trained on the MS
   RetroMAE (Xiao et al., 2022) utilizes a Masked                                                                    MARCO dataset.
                                                                                                        7069
  Probability           Jaccard            Overlap                          Jaccard            Overlap                          Jaccard            Overlap                           Jaccard           Overlap




                                                      Probability




                                                                                                          Probability




                                                                                                                                                              Probability
                0.04                                                0.04                                                0.04                                                0.050
                0.02                                                0.02                                                0.02                                                0.025
                0.00                                                0.00                                                0.00                                                0.000
                       0.0          0.5         1.0                        0.0          0.5        1.0                         0.0          0.5        1.0                          0.0         0.5         1.0
                                   Score                                               Score                                               Score                                               Score

                      (a) MS MARCO                                           (b) DL19                                             (c) DL20                                    (d) TREC-COVID

                         Jaccard           Overlap                           Jaccard           Overlap                          Jaccard            Overlap                          Jaccard            Overlap




                                                                                                          Probability




                                                                                                                                                              Probability
  Probability




                                                      Probability
                0.050                                               0.050                                               0.05
                                                                                                                                                                            0.05
                0.025                                               0.025
                0.000                                               0.000                                               0.00                                                0.00
                        0.0          0.5        1.0                         0.0         0.5         1.0                        0.0          0.5        1.0                         0.0          0.5        1.0
                                   Score                                               Score                                               Score                                               Score

                        (e) NFCorpus                                              (f) NQ                                       (g) HotpotQA                                        (h) FiQA-2018

                        Jaccard            Overlap                          Jaccard            Overlap                          Jaccard            Overlap                          Jaccard            Overlap
  Probability




                                                      Probability




                                                                                                          Probability




                                                                                                                                                              Probability
                0.2                                                 0.04                                                0.05                                                0.05
                0.1                                                 0.02
                0.0                                                 0.00                                                0.00                                                0.00
                      0.0           0.5        1.0                         0.0          0.5        1.0                         0.0          0.5        1.0                         0.0          0.5        1.0
                                   Score                                               Score                                               Score                                               Score

                      (i) Touché-2020                                 (j) CQADupStack                                           (k) DBPedia                                         (l) SCIDOCS

                        Jaccard            Overlap                          Jaccard            Overlap                           Jaccard           Overlap                           Jaccard           Overlap
  Probability




                                                      Probability




                                                                                                          Probability




                                                                                                                                                              Probability
                                                                                                                        0.050                                               0.050
                0.05                                                0.05
                                                                                                                        0.025                                               0.025
                0.00                                                0.00                                                0.000                                               0.000
                       0.0          0.5         1.0                        0.0          0.5        1.0                          0.0         0.5         1.0                         0.0         0.5         1.0
                                   Score                                               Score                                               Score                                               Score

                        (m) FEVER                                    (n) Climate-FEVER                                          (o) SciFact                                         (p) NQ-UTD

Figure 6: Distribution of term-based Jaccard similarity and overlap between LLM-generated and human-written
corpora for each dataset in Cocktail.


B.2              Checkpoints and Implementation Details                                                              For the other benchmarked neural retrieval mod-
For the fine-tuning of BERT and RoBERTa mod-                                                                      els, we use the publicly available official pre-
els, we utilized the official training script5 in BEIR                                                            trained checkpoints, which are listed in Table 11.
on the MSMARCO training dataset. Unless oth-                                                                      For all the neural models, only the first 512 word
erwise noted, mean pooling was employed as the                                                                    tokens of all documents are inputted.
pooling strategy, alongside cosine similarity as the
                                                                                                                  C             More Experimental Results
scoring function. Training parameters for each
model included a duration of 10 epochs, utilizing                                                                 In addition to the findings presented through
a batch size of 75, a learning rate set at 2e-5, and                                                              NDCG@1 in Table 2 and Table 3, we further ex-
the AdamW optimizer for efficient optimization.                                                                   tend our analysis to include the results for ranking
Our software framework utilizes PyTorch version                                                                   performance and source bias for NDCG@3 and
2.0.0 and the HuggingFace Transformers library                                                                    NDCG@5. These results are detailed in Table 13
version 4.31.0. All experiments were performed                                                                    and Table 14 for NDCG@3, and Table 15 and Ta-
using approximately 100 hours on four NVIDIA                                                                      ble 16 for NDCG@5, respectively. Consistent with
RTX A6000 (48G) GPUs.                                                                                             our earlier observations in Section 5.2, results on
    5
    https://github.com/beir-cellar/beir/blob/
                                                                                                                  these metrics also reveal a similar trend, underscor-
main/examples/retrieval/training/train_msmarco_                                                                   ing the robustness of our findings.
v3.py

                                                                                                     7070
                0.06                                                0.06




                                                                                                                                                                Probability
  Probability




                                                      Probability




                                                                                                           Probability
                                                                                                                         0.06                                                 0.10
                0.04                                                0.04                                                 0.04
                0.02                                                                                                                                                          0.05
                                                                    0.02                                                 0.02
                0.00                                                0.00                                                 0.00                                                 0.00
                        0.925 0.950 0.975 1.000                              0.925 0.950 0.975 1.000                        0.925 0.950 0.975 1.000                                   0.925 0.950 0.975 1.000
                          Cosine Similarity                                      Cosine Similarity                                 Cosine Similarity                                   Cosine Similarity

                      (a) MS MARCO                                               (b) DL19                                          (c) DL20                                     (d) TREC-COVID

                                                                                                                         0.2
                                                                                                                                                                              0.10
                                                      Probability
                                                                    0.2




                                                                                                           Probability




                                                                                                                                                                Probability
                0.075
  Probability




                0.050                                                                                                    0.1
                                                                    0.1                                                                                                       0.05
                0.025
                0.000                                               0.0                                                  0.0                                                  0.00
                        0.94   0.96    0.98    1.00                        0.8          0.9          1.0                        0.90           0.95      1.00                            0.8      0.9        1.0
                          Cosine Similarity                                  Cosine Similarity                                    Cosine Similarity                                     Cosine Similarity

                        (e) NFCorpus                                              (f) NQ                                         (g) HotpotQA                                        (h) FiQA-2018


                0.2                                                                                                                                                           0.15
  Probability




                                                      Probability




                                                                    0.06                                   Probability




                                                                                                                                                                Probability
                                                                                                                         0.2
                                                                    0.04                                                                                                      0.10
                0.1                                                                                                      0.1
                                                                    0.02                                                                                                      0.05
                0.0                                                 0.00                                                 0.0                                                  0.00
                           0.90       0.95    1.00                         0.8          0.9          1.0                           0.90         0.95     1.00                          0.90     0.95        1.00
                         Cosine Similarity                                       Cosine Similarity                                 Cosine Similarity                                    Cosine Similarity

                      (i) Touché-2020                                 (j) CQADupStack                                            (k) DBPedia                                          (l) SCIDOCS

                0.15
                                                                                                                         0.075
  Probability




                                                      Probability




                                                                                                           Probability




                                                                                                                                                                Probability
                                                                    0.10                                                                                                      0.075
                0.10                                                                                                     0.050
                                                                                                                                                                              0.050
                0.05                                                0.05                                                 0.025                                                0.025
                0.00                                                0.00                                                 0.000                                                0.000
                        0.925 0.950 0.975 1.000                            0.925 0.950 0.975 1.000                                      0.96      0.98   1.00                          0.925 0.950 0.975 1.000
                          Cosine Similarity                                      Cosine Similarity                                     Cosine Similarity                                Cosine Similarity

                        (m) FEVER                                    (n) Climate-FEVER                                            (o) SciFact                                         (p) NQ-UTD

Figure 7: Distribution of cosine similarity of semantic embedding between LLM-generated and human-written
corpora for each dataset in Cocktail.




          Model Name                                                       Publicly Available Link
          BERT (mini)                         https://huggingface.co/prajjwal1/bert-mini
          BERT (small)                        https://huggingface.co/prajjwal1/bert-small
          BERT (base)                         https://huggingface.co/bert-base-uncased
          BERT (large)                        https://huggingface.co/bert-large-uncased
          RoBERTa                             https://huggingface.co/FacebookAI/roberta-base
          ANCE                                https://huggingface.co/sentence-transformers/msmarco-roberta-base-ance-firstp
          TAS-B                               https://huggingface.co/sentence-transformers/msmarco-distilbert-base-tas-b
          Contriever                          https://huggingface.co/nthakur/contriever-base-msmarco
          coCondenser                         https://huggingface.co/sentence-transformers/msmarco-bert-co-condensor
          RetroMAE                            https://huggingface.co/nthakur/RetroMAE_BEIR
          DRAGON (Query)                      https://huggingface.co/nthakur/dragon-roberta-query-encoder
          DRAGON (Doc)                        https://huggingface.co/nthakur/dragon-roberta-context-encoder
          CE                                  https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2
          monoT5                              https://huggingface.co/castorini/monot5-base-msmarco-10k

                 Table 11: Publicly available model checkpoints links used for evaluation in the Cocktail benchmark.


                                                                                                      7071
   Dataset                Query                         Relevant Human-Written Document                                   Relevant LLM-Generated Document
  MS MARCO       do physicians pay for       Active-duty physicians and their dependents will receive          Active-duty physicians and their dependents are eligible for
                 insurance from their        free or discounted health care coverage and dental cover-         free or discounted healthcare coverage and dental coverage.
                 salaries?                   age. Physicians in the Reserve and Guard can also par-            In addition, physicians in the Reserve and Guard can enroll
                                             ticipate in TRICARE Reserve Select, which is part of the          in TRICARE Reserve Select, which is part of the Military’s
                                             Military’s health care plan. Finally, physicians can receive      healthcare plan. Furthermore, physicians can receive up to
                                             up to $400,000 in term life insurance coverage for only $29       $400,000 in term life insurance coverage for just $29 per
                                             a month.                                                          month.
     DL19        axon terminals or synap-    April 29, 2013. the terminal part of an axon from which           April 29, 2013. The terminal end of an axon, where a neural
                 tic knob definition         a neural signal is rendered, via dispersion of a neurotrans-      signal is transmitted to a nearby neuron through the diffu-
                                             mitter, across a synapse to a nearby neuron. TERMINAL             sion of a neurotransmitter across a synapse. TERMINAL
                                             BUTTON: The terminal button is commonly referred to as            BUTTON: Also known as the synaptic button, end button,
                                             the synaptic button, end button, button terminal, terminal        button terminal, terminal bulb, or synaptic knob.
                                             bulb, and synaptic knob..
     DL20        average salary for dental   In Nebraska, as the number of dental hygienists is grow-          In Nebraska, as the number of dental hygienists is increasing,
                 hygienist in nebraska       ing, the salaries earned by dental hygienists are increasing.     so are their salaries. According to data from 2006, dental
                                             Dental hygienists earned a yearly mean salary of $58,410 in       hygienists earned a yearly mean salary of $58,410. By 2010,
                                             2006. They earned a yearly mean salary of $64,440 in 2010.        this figure had risen to $64,440.
 TREC-COVID      will SARS-CoV2 in-          Summary COVID-19 had a mild clinical course in patients           COVID-19 had a mild clinical course in patients with Agam-
                 fected people develop       with Agammaglobulinemia lacking B lymphocytes, whereas            maglobulinemia, a condition characterized by a lack of B
                 immunity? Is cross pro-     it developed aggressively in Common Variable Immune De-           lymphocytes, while it developed aggressively in Common
                 tection possible?           ficiency. Our data offer mechanisms for possible therapeutic      Variable Immune Deficiency. Our data provide insights into
                                             targets.                                                          potential therapeutic targets.
   NFCorpus      What is Actually in         To study the origin and spread of Yersinia enterocolitica         To investigate the origins and spread of Yersinia enterocol-
                 Chicken Nuggets?            among pigs, fecal and blood samples were repeatedly taken         itica among pigs, fecal and blood samples were repeatedly
                                             on a fattening farm. A few piglets were found to be already       collected from a fattening farm. Initially, a few piglets on
                                             infected on breeding farms. After the piglets were mixed,         breeding farms were found to be infected. Once these piglets
                                             the infection spread through the whole unit. Eventually, all      were mixed, the infection rapidly spread throughout the en-
                                             the pigs excreted the pathogen.                                   tire unit, eventually infecting all the pigs.
      NQ         how many episodes are       The fourth season of Chicago Fire, an American drama              The fourth season of Chicago Fire, a US drama television
                 in chicago fire season 4    television series with executive producer Dick Wolf, and          series created by executive producer Dick Wolf and produc-
                                             producers Derek Haas, Michael Brandt, and Matt Olmstead,          ers Derek Haas, Michael Brandt, and Matt Olmstead, was
                                             was ordered on February 5, 2015, by NBC,[1] and premiered         greenlit by NBC on February 5, 2015, and premiered on
                                             on October 13, 2015 and concluded on May 17, 2016.[2]             October 13, 2015, concluding on May 17, 2016. The season
                                             The season contained 23 episodes.[3]                              consisted of 23 episodes.
   HotpotQA      What government posi-       Kiss and Tell is a 1945 American comedy film starring then        Kiss and Tell is a 1945 American comedy film starring then
                 tion was held by the        17-year-old Shirley Temple as Corliss Archer. In the film,        17-year-old Shirley Temple as Corliss Archer. In the film,
                 woman who portrayed         two teenage girls cause their respective parents much con-        two teenage girls, Corliss and her friend, cause their re-
                 Corliss Archer in the       cern when they start to become interested in boys. The            spective parents much distress when they start to develop
                 film Kiss and Tell?         parents’ bickering about which girl is the worse influence        romantic interests in boys. The parents’ arguing over which
                                             causes more problems than it solves.                              girl is the worse influence creates more problems than it
                                                                                                               solves.
   FiQA-2018     What are the ins/outs       Keep this rather corny acronym in mind. Business expenses         Keep this straightforward acronym in mind. Business ex-
                 of writing equipment        must be CORN: As other posters have already pointed out,          penses must be CLEAR: As other posters have already noted,
                 purchases off as busi-      certain expenses that are capital items (computers, furniture,    certain expenses that are capital items (computers, furniture,
                 ness expenses in a home     etc.) must be depreciated over several years, but you have a      etc.) must be depreciated over several years, but you have a
                 based business?             certain amount of capital items that you can write off in the     certain amount of capital items that you can write off in the
                                             current tax year.                                                 current tax year.
  Touché-2020    Should teachers      get    Why should teachers be laid off because of seniority? Many        Teachers should not be laid off solely based on seniority. It
                 tenure?                     electives teachers got laid off. Even a Music Teacher got laid    is unfair that many elective teachers were let go, including
                                             off even though she won a award for the best teacher in the       a talented Music Teacher who recently won an award for
                                             valley! Ironic isn’t it?                                          being the best teacher in the valley. It is ironic that she was
                                                                                                               laid off despite her achievement.
 CQADupStack     Is "a wide range of fea-    I hope you can enlighten me. I get varying answers in Google      I hope you can enlighten me. I’ve been getting conflicting
                 tures" singular or plu-     and I need to find out which is the correct grammatical           answers in Google, and I need to determine the correct gram-
                 ral?                        structure for these sentences. > The rest of the staff is/are     matical structure for these sentences. The rest of the staff are
                                             on leave at the moment. > > The rest of my family is/are          on leave at the moment. The rest of my family are arriving
                                             arriving late.                                                    late.
   DBPedia       social network group se-    Cluster analysis or clustering is the task of grouping a set of   Clustering is the process of grouping a set of objects together
                 lection                     objects in such a way that objects in the same group (called a    based on their similarities, where objects within the same
                                             cluster) are more similar (in some sense or another) to each      group (cluster) are more alike than those in other groups.
                                             other than to those in other groups (clusters).
   SCIDOCS       DeltaCFS: Boosting          The state machine approach is a general method for imple-         The state machine approach is a versatile method for build-
                 Delta Sync for Cloud        menting fault-tolerant services in distributed systems. This      ing fault-tolerant services in distributed systems. This paper
                 Storage Services by         paper reviews the approach and describes protocols for two        examines the approach and outlines protocols for two dis-
                 Learning from NFS           different failure models—Byzantine and fail stop. Systems         tinct failure models—Byzantine and fail-stop. Additionally,
                                             reconfiguration techniques for removing faulty components         the paper discusses techniques for reconfiguring systems to
                                             and integrating repaired components are also discussed.           remove faulty components and integrate repaired ones.
    FEVER        Konidela Production         Konidela Production Company is an Indian film production          Konidela Production Company is a renowned Indian film
                 Company was estab-          company established by actor Ram Charan , son of Chiran-          production house founded by the talented actor Ram Charan,
                 lished.                     jeevi .                                                           the son of the legendary actor Chiranjeevi.
 Climate-FEVER   Each of the six ma-         The Geologic temperature record are changes in Earth ’s           The geologic temperature record reflects changes in Earth’s
                 jor past ice ages began     environment as determined from geologic evidence on multi-        environment as revealed through geologic evidence spanning
                 when the atmospheric        million to billion ( 109 ) year time scales . The study of        millions to billions of years (109 years). The study of past
                 carbon dioxide content      past temperatures provides an important paleoenvironmental        temperatures offers valuable paleoenvironmental insights
                 was far higher than at      insight because it is a crucial component of the climate and      since it is a fundamental component of Earth’s climate and
                 present.                    oceanography of the time .                                        oceanography during those time periods.
    SciFact      Cataract and trachoma       Background Blindness and low vision are thought to be             Background blindness and low vision are believed to be
                 are the primary cause       common in southern Sudan. However, the magnitude and              prevalent in southern Sudan, but the scope and geographical
                 of blindness in Southern    geographical distribution are largely unknown. We aimed to        distribution of these issues remain largely unexplored. Our
                 Sudan.                      estimate the prevalence of blindness and low vision, identify     study aimed to determine the prevalence of blindness and
                                             the main causes of blindness and low vision, and estimate         low vision, identify the primary causes of blindness and
                                             targets for blindness prevention programs in Mankien payam        low vision, and estimate targets for blindness prevention
                                             (district), southern Sudan.                                       programs in Mankien payam (district), southern Sudan.
   NQ-UTD        Who won women’s dou-        The women’s doubles final of the BWF World Tour Finals            The women’s doubles final of the BWF World Tour Finals
                 bles champion in the        2023 concluded at the Hangzhou Olympic Sports Center on           2023 came to a close at the Hangzhou Olympic Sports Center
                 2023 Badminton World        Sunday. China’s top doubles pair, Chen Qingchen and Jia           on Sunday. China’s premier doubles pair, Chen Qingchen
                 Tour Finals?                Yifan, defeated South Korea’s Baek Ha Na and Lee So Hee           and Jia Yifan, outplayed South Korea’s Baek Ha Na and Lee
                                             2-0 to successfully defend their title and win $210,000 in        So Hee, winning the match 2-0 and successfully defending
                                             prize money.                                                      their title to collect a prize money of $210,000.


Table 12: Examples of queries, relevant human-written documents, and relevant LLM-generated documents for
each dataset in our Cocktail Benchmark.

                                                                                7072
                 Lexical                                              Neural Retrievers                                       Neural Re-rankers
   Model (→)
                 BM25      BERT    RoBERTa       ANCE         TAS-B         Contriever    coCondenser   RetroMAE    DRAGON      CE      monoT5
      PLM           -      BERT    RoBERTa     RoBERTa     DistilBERT         BERT           BERT         BERT        BERT    MiniLM       T5        Average
     # Paras        -      110M     125M         125M          66M            110M           110M         110M        110M     66M       220M      All    Neural
                                              Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
  MS MARCO        39.7     53.5      53.7         54.6         57.1            58.3           57.4        58.1        61.9      59.0      58.4    55.6     57.2
     DL19         51.7     75.7      75.5         69.4         75.0            72.6           75.5        75.5        76.6      78.8      75.5    72.9     75.0
     DL20         50.7     75.5      75.5         72.2         72.9            71.2           76.5        77.4        78.0      76.9      73.0    72.7     74.9
                                            Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID      62.4     66.4      60.0         71.0         64.0            63.2           70.9        74.3        68.3      71.9      79.9    68.4     69.0
   NFCorpus       44.2     36.3      32.3         33.0         39.1            42.1           41.1        39.3        41.1      48.2      43.1    40.0     39.6
      NQ          46.2     62.5      60.0         60.3         66.3            70.6           66.0        67.9        71.2      68.6      72.7    64.7     66.6
   HotpotQA       72.3     62.3      51.7         59.2         72.3            76.3           69.4        76.5        77.0      83.5      80.1    71.0     70.8
   FiQA-2018      22.2     21.9      22.2         26.2         26.1            29.9           25.3        28.6        33.5      31.6      37.3    27.7     28.3
  Touché-2020     51.4     47.0      42.1         46.8         44.7            46.3           34.3        47.1        53.4      52.8      51.7    47.1     46.6
  CQADupStack     26.4     24.8      25.0         29.5         23.3            32.6           31.7        29.5        34.8      32.6      35.2    29.6     29.9
    DBPedia       34.2     52.6      47.3         45.8         54.5            59.3           54.8        55.1        57.7      57.4      49.6    51.7     53.4
   SCIDOCS        15.4     11.7      10.5         12.7         15.0            15.5           13.9        14.8        16.1      17.4      18.4    14.7     14.6
    FEVER         67.5     80.5      75.8         80.7         83.8            86.5           75.5        87.7        87.9      89.1      77.0    81.1     82.4
 Climate-FEVER    23.4     25.1      25.2         25.9         30.3            29.6           25.4        29.9        31.0      32.7      31.8    28.2     28.7
     SciFact      58.3     37.9      40.9         40.8         54.0            56.4           49.9        54.5        56.7      57.1      65.2    52.0     51.3
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD        70.5     72.4      66.7         74.3         78.7            75.4           69.3        75.5        76.6      86.6      87.1    75.7     76.3
                                                                           Averaged Result
   Supervised     47.4     68.2      68.2         65.4         68.3            67.4           69.8        70.3        72.2      71.6      69.0    67.1     69.0
    Zero-shot     45.7     46.3      43.1         46.6         50.2            52.6           48.3        52.4        54.3      56.1      56.1    50.1     50.6
       All        46.0     50.4      47.8         50.2         53.6            55.4           52.3        55.7        57.6      59.0      58.5    53.3     54.0


Table 13: Overall ranking performance (NDCG@3) across all benchmarked datasets in Cocktail. The second-to-last
column is the average result across all models, while the last column is the average for all neural retrieval models.
The best performed result for each dataset is marked in bold, and the second best is underlined.



                 Lexical                                              Neural Retrievers                                       Neural Re-rankers
   Model (→)
                 BM25      BERT    RoBERTa       ANCE        TAS-B          Contriever    coCondenser   RetroMAE   DRAGON      CE      monoT5
      PLM           -      BERT    RoBERTa     RoBERTa     DistilBERT         BERT           BERT        BERT         BERT    MiniLM      T5         Average
     # Paras        -      110M     125M         125M         66M             110M           110M        110M         110M     66M      220M      All     Neural
                                              Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
  MS MARCO        35.9     -4.2      -8.3         0.5          -8.5            -1.7           1.9         -5.3        -3.2     -4.0       0.9     0.4      -3.2
     DL19         81.6     -50.6    -17.2        -21.0        -49.3           -21.9          -21.1        -47.6       -45.4    -19.5     -25.4    -21.6   -31.9
     DL20         91.3     -59.3    -37.8         -7.7        -18.7           -10.6          -17.0        -31.1       -36.2    -21.3     -13.9    -14.8   -25.4
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID      25.6     -51.0    -40.4        -33.8        -73.1           -62.0          -68.0        -25.9       -17.9    -66.5     -46.0    -41.7   -48.5
   NFCorpus       -16.2    -16.8    -29.7        -19.1        -22.7           -43.2          -24.9        -18.9       -22.9    -38.4     -18.5    -24.7   -25.5
      NQ          -3.9     -8.0      -3.8         -4.3        -12.4           -10.2          -8.5         -7.9        -14.7    -16.6     -8.7     -9.0     -9.5
   HotpotQA       21.0     -0.5      -1.8         -5.7         0.2             -1.6          -2.9         1.4         -1.8     14.1       4.9     2.5      0.6
   FiQA-2018      -3.6     -14.0     -5.8        -20.3        -10.7           -28.9          -19.0        -20.0       -15.1    -25.4     -17.2    -16.4   -17.6
  Touché-2020     -32.1    -41.4    -40.2        -12.3         -9.7           -46.7           6.4         -18.2       -53.0    -69.9     -53.8    -33.7   -33.9
  CQADupStack     17.8     -20.4    -15.7         -0.9         -1.7            -4.1           1.3         -20.7       -4.7     -7.5       3.5     -4.8     -7.1
    DBPedia       21.3     -9.9     -14.1        -17.7         -5.1            -5.3          -10.8        -13.1       -10.9    -2.6      10.9     -5.2     -7.9
   SCIDOCS         1.3     -1.7     -21.0         -1.6         -1.3            -6.5          -5.7         -10.8       -18.6    -12.7     -23.0    -9.2    -10.3
    FEVER         -5.2     0.2       -0.2        -25.8         -4.5            -6.3          -8.0         0.6         -7.0     -0.7       6.2     -4.6     -4.5
 Climate-FEVER    10.3     -7.4      -8.1        -38.4        -10.2            -6.9          -9.3         -4.6        -5.0     3.2       -37.9    -10.4   -12.5
     SciFact       0.6     -12.5     -2.5         -5.9        -16.4            2.2           -10.3        -6.2        -7.5     1.3       -8.4     -6.0     -6.6
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD         9.0     -13.3    -14.2        -13.9         -9.7           -17.5          -10.7        -18.7       -20.6    -21.8     -9.0     -12.8   -14.9
                                                                           Averaged Result
   Supervised     69.6     -38.0    -21.1         -9.4        -25.5           -11.4          -12.1        -28.0       -28.3    -14.9     -12.8    -12.0   -20.2
    Zero-shot      3.5     -15.1    -15.2        -15.4        -13.6           -18.2          -13.1        -12.5       -15.4    -18.7     -15.2    -13.5   -15.2
       All        15.9     -19.4    -16.3        -14.2        -15.9           -16.9          -12.9        -15.4       -17.8    -18.0     -14.7    -13.2   -16.2


Table 14: Overall source bias evaluation w.r.t. Relative ∆ (NDCG@3) across all benchmarked datasets in Cocktail.
The numbers (i.e., Relative ∆ > 0) suggest that retrieval models generally prefer human-written content while
the numbers (i.e., Relative ∆ ≤ 0) indicate retrieval models prefer LLM-generated content.


                                                                               7073
                 Lexical                                              Neural Retrievers                                       Neural Re-rankers
   Model (→)
                 BM25      BERT    RoBERTa       ANCE         TAS-B         Contriever    coCondenser   RetroMAE    DRAGON      CE      monoT5
      PLM           -      BERT    RoBERTa     RoBERTa     DistilBERT         BERT           BERT         BERT        BERT    MiniLM       T5        Average
     # Paras        -      110M     125M         125M          66M            110M           110M         110M        110M     66M       220M      All    Neural
                                              Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
  MS MARCO        43.5     58.0      58.1         59.0         61.7            63.0           62.0        62.6        66.6      62.7      63.1    60.0     61.7
     DL19         49.9     75.3      73.4         69.5         74.3            71.8           75.0        73.9        76.7      76.7      73.4    71.8     74.0
     DL20         48.3     74.9      73.9         71.6         73.7            70.7           75.0        76.0        77.9      74.6      70.7    71.6     73.9
                                            Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID      61.3     63.2      57.7         68.1         64.4            62.0           70.7        74.4        68.4      70.9      80.0    67.4     68.0
   NFCorpus       41.5     34.3      30.0         30.1         37.5            39.7           38.2        37.3        39.7      45.4      41.3    37.7     37.3
      NQ          49.3     64.8      62.3         62.8         68.9            73.5           68.7        70.4        73.7      70.2      75.3    67.3     69.1
   HotpotQA       67.8     56.6      46.8         53.7         67.4            71.4           64.0        71.6        72.0      79.0      76.2    66.0     65.9
   FiQA-2018      21.6     21.1      22.1         25.5         25.7            29.2           24.4        27.8        32.3      30.5      36.5    27.0     27.5
  Touché-2020     50.4     45.6      40.9         48.7         42.9            43.7           32.6        44.4        50.1      50.2      50.6    45.5     45.0
  CQADupStack     27.3     25.4      25.7         30.1         24.5            33.5           32.6        30.2        35.7      33.1      36.1    30.4     30.7
    DBPedia       33.3     49.2      44.4         43.5         51.8            55.5           52.6        52.6        54.0      55.1      48.1    49.1     50.7
   SCIDOCS        14.1     10.7      9.5          11.4         13.3            14.2           12.4        13.6        14.8      15.8      16.7    13.3     13.2
    FEVER         71.4     82.5      78.1         82.4         85.8            88.1           78.5        89.2        89.5      89.9      79.5    83.2     84.3
 Climate-FEVER    22.1     23.8      23.9         24.0         28.6            28.0           23.7        27.9        29.0      31.3      31.0    26.7     27.1
     SciFact      62.0     41.0      43.0         42.9         56.4            59.6           53.0        57.1        59.9      61.2      68.0    54.9     54.2
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD        68.7     71.3      63.9         72.4         76.5            74.2           69.4        74.3        74.6      83.9      84.9    74.0     74.5
                                                                           Averaged Result
   Supervised     47.2     69.4      68.5         66.7         69.9            68.5           70.7        70.8        73.7      71.3      69.1    67.8     69.8
    Zero-shot     45.4     45.3      42.2         45.8         49.5            51.7           47.8        51.6        53.4      55.1      55.7    49.4     49.8
       All        45.8     49.9      47.1         49.7         53.3            54.9           52.1        55.2        57.2      58.2      58.2    52.9     53.6


Table 15: Overall ranking performance (NDCG@5) across all benchmarked datasets in Cocktail. The second-to-last
column is the average result across all models, while the last column is the average for all neural retrieval models.
The best performance result for each dataset is marked in bold, and the second best is underlined.



                 Lexical                                              Neural Retrievers                                       Neural Re-rankers
   Model (→)
                 BM25      BERT    RoBERTa       ANCE        TAS-B          Contriever    coCondenser   RetroMAE   DRAGON      CE      monoT5
      PLM           -      BERT    RoBERTa     RoBERTa     DistilBERT         BERT           BERT        BERT         BERT    MiniLM      T5         Average
     # Paras        -      110M     125M         125M         66M             110M           110M        110M         110M     66M      220M      All     Neural
                                              Supervised Evaluation (In-Domain Datasets Collected in Pre-LLM Era)
  MS MARCO        30.5     -4.0      -6.6         1.0          -7.8            -1.0           2.2         -4.7        -2.6     -2.5       2.0     0.6      -2.4
     DL19         59.5     -37.9    -27.7        -17.0        -39.3           -20.7          -16.5        -38.6       -48.1    -21.7     -23.0    -21.0   -29.0
     DL20         74.1     -31.8    -34.1         -5.6        -13.7           -10.6          -14.0        -16.8       -27.8    -28.9     -14.3    -11.2   -19.8
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in Pre-LLM Era)
  TREC-COVID      16.6     -42.4    -37.1        -33.4        -62.7           -58.7          -56.9        -28.5       -23.4    -66.3     -32.7    -38.7   -44.2
   NFCorpus       -15.8    -15.1    -19.4        -10.4        -13.6           -34.9          -13.8        -17.6       -16.4    -26.1     -12.3    -17.8   -18.0
      NQ          -2.3     -6.7      -3.2         -2.2         -9.7            -8.8          -7.0         -5.8        -11.3    -14.8     -7.5     -7.2     -7.7
   HotpotQA       16.5     -0.4      -1.4         -4.5         0.8             -0.7          -1.4         1.8         -1.1     10.2       4.6     2.2      0.8
   FiQA-2018      -5.2     -14.1     -5.1        -12.2         -9.2           -18.8          -14.5        -18.2       -12.2    -17.8     -14.1    -12.9   -13.6
  Touché-2020     -32.2    -35.3    -42.9        -19.8        -32.0           -34.1          -8.5         -19.1       -45.2    -55.1     -55.0    -34.5   -34.7
  CQADupStack     15.5     -15.8    -11.0         -0.4         0.5             -3.8           3.6         -17.9       -2.5     -4.7       3.3     -3.0     -4.9
    DBPedia       18.3     -11.8    -13.1        -17.7         -4.4            -2.2          -11.1        -9.0        -9.4     -3.9      13.9     -4.6     -6.9
   SCIDOCS         1.4     -1.8     -16.3         -3.4         -4.4            -8.2          -7.9         -10.1       -13.2    -12.3     -17.8    -8.5     -9.5
    FEVER         -4.2     0.3       0.2         -22.3         -3.9            -5.0          -6.1         0.4         -6.1     -0.8       4.9     -3.9     -3.8
 Climate-FEVER     7.2     -4.8      -5.3        -37.2        -10.1            -4.6          -7.2         -4.6        -3.5     2.3       -28.3    -8.7    -10.3
     SciFact       0.4     -10.9     -3.2         -4.0        -11.6            1.2           -8.7         -5.2        -7.0     -0.6      -6.4     -5.1     -5.6
                                             Zero-shot Evaluation (Out-of-Domain Datasets Collected in the LLM Era)
    NQ-UTD         4.4     -12.2     -5.0         -7.7         -8.1            -9.0          -5.7         -16.4       -13.0    -16.3     -4.1     -8.5     -9.7
                                                                           Averaged Result
   Supervised     54.7     -24.6    -22.8         -7.2        -20.3           -10.8          -9.4         -20.0       -26.2    -17.7     -11.8    -10.5   -17.1
    Zero-shot      1.6     -13.2    -12.5        -13.5        -13.0           -14.4          -11.2        -11.6       -12.6    -15.9     -11.7    -11.6   -12.9
       All        11.5     -15.3    -14.4        -12.3        -14.3           -13.7          -10.8        -13.1       -15.2    -16.2     -11.7    -11.4   -13.7


Table 16: Overall source bias evaluation w.r.t. Relative ∆ (NDCG@5) across all benchmarked datasets in Cocktail.
The numbers (i.e., Relative ∆ > 0) suggest that retrieval models generally prefer human-written content while
the numbers (i.e., Relative ∆ ≤ 0) indicate retrieval models prefer LLM-generated content.


                                                                               7074
