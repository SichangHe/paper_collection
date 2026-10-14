                                                  Spiral of Silence: How is Large Language Model Killing Information
                                                    Retrieval?—A Case Study on Open Domain Question Answering
                                                         Xiaoyang Chen1,2 , Ben He1,2 B , Hongyu Lin2 B , Xianpei Han2 ,
                                                            Tianshu Wang2,3 , Boxi Cao2,1 , Le Sun2 B , Yingfei Sun1 B
                                                                    1
                                                                      University of Chinese Academy of Sciences
                                         2
                                           Chinese Information Processing Laboratory, Institute of Software, Chinese Academy of Sciences
                                               3
                                                 Hangzhou Institute for Advanced Study, University of Chinese Academy of Sciences
                                               chenxiaoyang19@mails.ucas.ac.cn, {benhe, yfsun}@ucas.ac.cn
                                              {hongyu, xianpei, tianshu2020, boxi2020, sunle}@iscas.ac.cn

                                                                    Abstract
                                                  The practice of Retrieval-Augmented Genera-
                                                  tion (RAG), which integrates Large Language
arXiv:2404.10496v4 [cs.IR] 23 Jun 2024




                                                  Models (LLMs) with retrieval systems, has be-
                                                  come increasingly prevalent. However, the
                                                  repercussions of LLM-derived content infil-
                                                  trating the web and influencing the retrieval-
                                                  generation feedback loop are largely uncharted
                                                  territories. In this study, we construct and it-
                                                  eratively run a simulation pipeline to deeply
                                                  investigate the short-term and long-term effects     Figure 1: The evolution of RAG systems after introduc-
                                                  of LLM text on RAG systems. Taking the               ing LLM-generated texts, where the “Spiral of Silence”
                                                  trending Open Domain Question Answering              effect gradually emerges.
                                                  (ODQA) task as a point of entry, our findings
                                                  reveal a potential digital “Spiral of Silence” ef-
                                                  fect, with LLM-generated text consistently out-      becoming commonplace, impacting how content is
                                                  performing human-authored content in search          produced and shared (Goldstein et al., 2023; Pan
                                                  rankings, thereby diminishing the presence and       et al., 2023; Dai et al., 2023b). These developments
                                                  impact of human contributions online. This           pose novel challenges and opportunities for infor-
                                                  trend risks creating an imbalanced information       mation retrieval (IR) and generation, especially for
                                                  ecosystem, where the unchecked proliferation         Retrieval-Augmented Generation (RAG) systems,
                                                  of erroneous LLM-generated content may re-
                                                                                                       which combine both capabilities (Guu et al., 2020;
                                                  sult in the marginalization of accurate informa-
                                                  tion. We urge the academic community to take         Lewis et al., 2020; Borgeaud et al., 2022; Izacard
                                                  heed of this potential issue, ensuring a diverse     et al., 2023). As text produced by large language
                                                  and authentic digital information landscape.1        models continues to flood the internet and is in-
                                                                                                       dexed by search systems, the enduring effects of
                                          1       Introduction                                         such text on the retrieval-generation process grow
                                          The integration of Large Language Models                     more ambiguous, and the future landscape of the
                                          (LLMs) (OpenAI, 2022, 2023; Touvron et al., 2023;            information environment is yet to be determined.
                                          Google, 2023) is reshaping the online information               In our research, we focus on the effects of LLM-
                                          landscape, making text generation easier, increas-           generated text on RAG systems. As shown in Fig-
                                          ing content production, enhancing personalized               ure 1, we construct a pipeline that simulates the
                                          knowledge assistance, and enabling advanced fake             continuous influx of LLM-generated text into
                                          news creation. Schick (2020) suggest that by 2026,           web datasets and assess its impact on the perfor-
                                          synthetic content could dominate up to 90% of the            mance of RAG through iterative runs. To evaluate
                                          web. CounterCloud2 shows that a single developer             the RAG performance in the simulation process,
                                          can create an AI fake news factory cheaply and con-          we adopt the Open Domain Question Answering
                                          vincingly. AI-driven content generation is rapidly           (ODQA) task as our evaluative benchmark due to
                                              1                                                        its recent surge in research popularity as an effec-
                                              We release the resources at https://github.com/
                                          VerdureChen/SOS-Retrieval-Loop                               tive test of both retrieval accuracy and generation
                                            2
                                              https://countercloud.io/?page_id=307                     quality (Pan et al., 2023; Chen et al., 2023). We
employ widely used retrieval and re-ranking meth-        other tasks (Cai et al., 2019; Zhou et al., 2023),
ods to supply the context necessary for LLMs to          current research explores LLMs’ output accuracy
generate answer documents. Upon evaluating these         against specific contexts (Adlakha et al., 2023), ro-
documents, we integrate them into the text corpus        bustness to extraneous information (Chen et al.,
for subsequent retrieval-generation cycles. This         2023), and the effects of output integration strate-
process is repeated multiple times to monitor and        gies (Liu et al., 2023b). Our study aims to provide a
assess the emerging patterns. Experimental results       novel perspective to observe and predict the poten-
show that LLM-generated text has an immediate            tial trajectory and impact of its future development.
effect on RAG systems, generally improving re-
                                                            Effects of AIGC. Advances in Artificial Intel-
trieval outcomes while producing varied effects on
                                                         ligence Generated Content (AIGC) have signifi-
QA performance. However, over the long term, a
                                                         cantly impacted society and technology. LLMs
marked decrease in retrieval effectiveness emerges,
                                                         facilitate creating content to combat misinforma-
while the QA performance remains unaffected.
                                                         tion (Xu et al., 2023; Chen and Shu, 2023) but
   Further examination reveals a bias in search sys-     can also produce damaging content (Huang et al.,
tems towards LLM-generated texts, which consis-          2023b). The potential biases and discrimination in
tently rank higher than human-written content. As        AIGC have garnered widespread attention (Liang
LLM-generated texts increasingly dominate the            et al., 2021; Zhuo et al., 2023). Shumailov et al.
search results, the visibility and influence of human-   (2023) and Alemohammad et al. (2023) show that
authored web content diminish, fostering a digital       LLMs trained on self-generated data degrade with-
“Spiral of Silence” effect. This effect aptly explains   out fresh real-world input. Pan et al. (2023) inves-
what we observe in our simulations and reveals           tigated the impact of erroneous information gen-
the potential negative impact of LLM-generated           erated by LLMs on ODQA systems. Dai et al.
texts on the information ecosystem: while LLM-           (2023a) indicated that AI-modified texts might rank
generated texts sometimes provide a more effective       higher in search results, potentially affecting the
IR experience in the short term, in the long term        fairness of those outcomes. Our research aims to
they may lead to the invisibility of human-authored      further explore the short-term and long-term effects
content, the homogenization of search results, and       on RAG systems when AIGC text is continuously
the inaccessibility of certain accurate information,     integrated into the search system’s datasets.
thereby adversely affecting public knowledge ac-
quisition and decision-making.                              Spiral of Silence. The “Spiral of Silence” the-
   The contributions of this paper are threefold:        ory (Noelle-Neumann, 1974), is a seminal theory
1) We propose an iterative pipeline to investigate       within the field of communications that describes
the short-term and long-term impacts of LLM-             how people may suppress their views to avoid iso-
generated text on RAG systems. 2) We study the           lation, thus often reinforcing dominant public opin-
potential emergence of a “Spiral of Silence” phe-        ions (Scheufle and Moy, 2000; Liu et al., 2019;
nomenon within RAG systems. 3) We analyze                Lin et al., 2022). We shift focus to a novel “pas-
the implications of this phenomenon, offering a          sive human silence” influenced by LLMs, where
new perspective on the dynamic interplay between         rapid AI content production and biased search al-
LLM-generated content and RAG systems.                   gorithms potentially marginalize human contribu-
                                                         tions in public discourse. This theory stands apart
2   Related Works                                        from concepts such as “echo chambers", “filter
                                                         bubbles", and “degenerate feedback loops” preva-
Retrieval Augmented Generation. RAG systems              lent in recommendation systems (Alatawi et al.,
have been extensively analyzed, demonstrating re-        2021; Chitra and Musco, 2020; Jiang et al., 2019).
trieval’s role in enhancing language model effi-         While these terms describe the narrowing of in-
cacy (Guu et al., 2020; Lewis et al., 2020; Borgeaud     formational scope as users engage with algorith-
et al., 2022; Izacard et al., 2023; Ram et al., 2023).   mic systems, the “Spiral of Silence” theory pro-
These systems also curtail LLMs’ hallucinations          poses a scenario where human users are compelled
during text generation (Ji et al., 2023; Huang et al.,   into silence in public discourse due to the influ-
2023a) and reduce knowledge obsolescence (He             ence of LLMs and IR systems. This phenomenon
et al., 2023). Applied in ODQA (Izacard and Grave,       goes beyond mere selective exposure or algorith-
2021; Trivedi et al., 2023; Liu et al., 2023a) and       mic recommendations. Our study explores how
LLM-generated text might induce a “Spiral of Si-         optimize the process. In the generation stage, we
lence” in RAG systems over time. For further dis-        use the LLMs which are widely used to generate
cussion regarding the rationale for applying this        responses. To accurately simulate the evolution
theory to our study, please see Appendix A.1.            process of the RAG system, we specifically use an
                                                         iteratively updated indexing structure that sup-
3     Pipeline Construction                              ports incorporating the newly generated LLM text
                                                         into the index in each iteration, keeping the dataset
In this section, a simulation framework is designed
                                                         updated for subsequent retrieval and evaluation.
to explore the potential impacts that texts generated
                                                            Specifically, the iterative simulation process
by LLMs may have on RAG systems. This frame-
                                                         unfolds as follows: 1) Baseline Establishment:
work models a simplified process that tracks how
                                                         Utilizing an initial dataset comprised of human-
RAG systems gradually adjust their responses as
                                                         authored text unaffected by LLM (D0 ), ascertain
they accumulate LLM-generated text over time.
                                                         the performance of a benchmark RAG pipeline.
3.1    Preliminaries                                     2) Zero-shot Text Introduction: The baseline
                                                                                                       (zero-shot)
                                                         dataset D0 is enriched with text set TLLM
An RAG system f can be formalized as f : (Q ×
                                                         generated by LLMs in zero-shot manner, yielding
D × K) → S, where Q is the set of queries, D                              (zero-shot)
represents a large collection of documents, K is the     D1 = D0 ∪ TLLM               . This simulates the evo-
knowledge within the LLM, and S is the set of text       lution of users’ application of LLMs from initial
outputs generated by the system. For a particular        zero-shot deployments to sophisticated RAG con-
query q ∈ Q, the goal of the RAG system is to            figurations. 3) Retrieval and Re-ranking: For
find a mapping f (q, D, K) = s that produces a           each query q, a subset of documents Di′ is retrieved
response text s ∈ S satisfying the query q. This         from the dataset Di through a retrieval and optional
process involves two stages:                             re-ranking step R(q, Di ) → Di′ . The retrieval func-
                                                         tion R remains constant throughout the experimen-
   Retrieval Stage, executed by the retrieval func-
                                                         tal process to control variables. 4) Generation
tion R, is formally defined as R : (Q × D) → D′ ,
                                                         Phase: Answers S are generated using the LLMs
where D′ ⊆ D represents the subset of documents
                                                         (G(p, D′ , q, K) → s) with a uniform prompt p in
judged by R to be most relevant to the query q.
                                                         the experiment. 5) Post-processing Phase: Post-
   Generation Stage, executed by the generation
                                                         process S to obtain S ′ , removing text fragments
function G : (P × Q × D′ × K) → S. Its task is
                                                         that may expose the identity of the LLMs. 6) Index
to utilize the prompt p ∈ P , the query q ∈ Q, the
                                                         Update: Integrate S ′ into Di to update the dataset
related document subset D′ , and the knowledge of
                                                         to Di+1 . 7) Iterative Operation: Repeat steps 3
LLMs K to construct the answer s.
                                                         to 6 for each new dataset Di+1 , until the required
   Within the entire RAG system f , the functions R
                                                         number of iterations t is reached.
and G act in series to form a process expressed as
                                                            The pseudo-code for this process is presented
f (q, D, K) = G(p, q, R(q, D), K). In this man-
                                                         in Appendix A.2. Through the simulation process,
ner, the RAG system integrates the precision of IR
                                                         we observe how LLM-generated text influences the
with the richness of LLMs to provide information-
                                                         RAG systems and how this impact evolves with
rich content when answering questions.
                                                         data accumulation. While the main simulation as-
3.2    Simulation Process                                sumes that the LLMs remain static due to their
                                                         relatively infrequent update cycles, we also con-
 Our simulation process starts with a pure human-
                                                         duct experiments on the effects of LLM evolution
authored text dataset and gradually introduces the
                                                         over time in Appendix A.6. For prompt and post-
LLM-generated text, observing how this change
                                                         processing details, see Appendix A.9 and A.3.
over time affects the RAG system. Adhering to
the specifications outlined in Section 3.1, the RAG      4   Experiment
architecture is instantiated and expanded with ad-
ditional details. In the retrieval stage, we apply       Datasets and Metrics. We conduct experiments
sparse and dense retrieval strategies to obtain a can-   on commonly used ODQA datasets, including
didate document set that is relevant to the query.       NQ (Kwiatkowski et al., 2019), WebQ (Berant
Additionally, we also have the option to perform         et al., 2013), TriviaQA (Joshi et al., 2017), and
a re-ranking of the candidate documents to further       PopQA (Mallen et al., 2022). We preprocess the
datasets following Yu et al. (2023) and Zhang et al.    effects observed in the first iteration, while the
(2023). Given the constraints on experimental re-       long-term effect is analyzed from the second to
sources, we randomly select 200 samples from each       the tenth iteration. We investigate the occurrence
test set. When evaluating the retrieval phase, we       of the “Spiral of Silence” effect and how RAG sys-
utilize Acc@5 and Acc@20 following Karpukhin            tems respond. Under the task settings of ODQA,
et al. (2020). These metrics assess the proportion of   we analyze the potential influence of the “Spiral of
questions where the correct answers appear in the       Silence” on RAG systems’ response patterns.
top 5 or top 20 retrieval results, respectively. For
the answer quality of the LLM output for each iter-     5.1   Short-Term Effects on RAG Performance
ation, we follow Chen et al. (2023) by applying the     When comparing RAG system results using differ-
Exact Match (EM) metric, which checks if the cor-       ent retrieval methods on the original dataset versus
rect answer is fully contained within the generated     the augmented one in the first iteration, we observe
text. Furthermore, in Section 5, we adopt a holistic    that: 1) Immediate Impact of LLM-Generated
perspective to examine the RAG pipeline, with a         Text on the RAG System: The introduction of a
focus on the interaction between the retrieval and      minimal amount of LLM-generated text produces
generation phases and how the ranking of human-         immediate effects on both retrieval and QA perfor-
generated texts changes over time.                      mance of the RAG system, as shown in Table 1 and
   Retrieval and Re-ranking Methods. In our             Figure 2. Specifically, both retrieval and generation
experiments, we employ a variety of retrieval           performance exhibit noticeable fluctuations. These
methods, including the sparse model BM25, the           changes highlight the sensitivity of the system to
contrastive learning-based dense retriever Con-         even small modifications made by LLM-generated
triever (Izacard et al., 2022), the advanced BGE-       text. 2) LLM-Generated Text Generally Im-
Base (Xiao et al., 2023) retriever, and the LLM-        proves Retrieval Accuracy: Table 1 reveals that
Embedder (Zhang et al., 2023) designed for LLMs.        adding LLM-generated responses to a dataset typ-
For the results retrieved using BM25 and BGE-           ically enhances the accuracy of retrieval systems,
Base, we separately apply the T5-based (Raf-            as measured by Acc@5 and Acc@20 metrics. For
fel et al., 2020) re-ranking model MonoT5-              example, using the BM25 on TriviaQA resulted in
3B (Nogueira et al., 2020), the UPR-3B (Sachan          accuracy improvements of 31.2% and 19.1% re-
et al., 2022) which uses the unsupervised capabil-      spectively. However, a slight decline in Acc@5
ities of T0-3B (Sanh et al., 2022), and the BGE-        is also observed in certain cases. This suggests a
Reranker (Xiao et al., 2023), which is based on the     primarily positive, yet complex, impact of LLM-
XLM-RoBERTa-Large (Conneau et al., 2020).               generated text on retrieval accuracy. 3) The Impact
   Generative Models. Considering the complex-          on QA Performance is Mixed: Due to space con-
ity and variability of real-world environments, the     straints, we only present the results of four retrieval
text that is continuously integrated into the system    methods. As shown in Figure 2, while the RAG
may be generated by a variety of LLMs. Our iter-        system’s QA performance typically surpasses the
ative experiments incorporate text produced by a        zero-shot LLM outputs, the addition of LLM text
suite of prevalent LLMs. These include GPT-3.5-         can either enhance or impair QA performance de-
Turbo (OpenAI, 2022), LLaMA2-13B-Chat (Tou-             pending on the dataset and retrieval strategy. It
vron et al., 2023), Qwen-14B-Chat (Bai et al.,          appears to enhance performance for TriviaQA, but
2023), Baichuan2-13B-Chat (Yang et al., 2023),          for NQ and PopQA, the effect is detrimental with
and ChatGLM3-6B (Du et al., 2022). This enables         non-BM25 retrieval methods, suggesting that with-
the RAG systems to blend varied linguistic styles       out significant retrieval enhancement, LLM text
and knowledge, leading to results that more closely     inclusion might be counterproductive.
replicate real-world scenarios. For more implemen-
                                                        5.2   Long-term Effects on RAG Performance
tation details, please refer to Appendix A.4.
                                                        In this section, we investigate whether the short-
5   Results                                             term effects are predictive of the long-term behav-
                                                        ior of the system. We present the results on NQ and
In this section, we examine both initial and ex-        PopQA in Figure 3. For results on other datasets,
tended iterations within the simulation framework.      please refer to Figure 8 in Appendix A.5, where we
We define the short-term effect as the immediate        observe consistent patterns across these datasets.
                                 NQ                    WebQ                 TriviaQA               PopQA
   Model
                           Acc@5     Acc@20      Acc@5      Acc@20     Acc@5       Acc@20    Acc@5      Acc@20
                        Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ Ori. +LLMZ
   BM25                 49.0   57.5   67.0   73.5   41.0   51.0∗   63.0     71.0    62.5   82.0∗   73.0   87.0∗   35.5   41.5   51.5   59.5
   Contreiver           68.0   68.5   84.0   85.0   66.0   69.5    74.0     80.0    68.0   83.5∗   80.5   87.5    62.0   65.0   77.5   79.5
   LLM-Embedder         75.5   75.5   86.5   88.0   62.5   72.5∗   76.0     79.5    67.5   81.0∗   77.5   87.5∗   70.0   67.5   79.5   82.0
   BGEbase              77.0   73.0   86.0   86.0   65.5   71.5    77.0     80.0    69.5   81.5∗   80.0   87.5∗   72.0   70.0   83.0   84.5
   BM25+UPR             63.0   66.5   73.5   78.0   57.0   68.0∗   68.5     75.0    71.5   83.0∗   78.0   89.0∗   57.5   61.5   60.0   67.0
   BM25+MonoT5          66.5   69.0   74.5   80.5   62.0   67.5    69.5     76.0    72.0   83.5∗   78.0   88.0∗   53.5   58.5   59.5   66.5
   BM25+BGEreranker     68.0   69.5   76.5   81.0   64.5   68.5    71.0     76.0    72.5   84.0∗   78.0   88.5∗   54.0   61.0   60.0   67.5
   BGEbase +UPR         75.5   71.5   87.5   88.0   64.0   69.0    77.0     79.5    76.0   84.0∗   84.5   89.5    76.0   71.0   84.5   84.5
   BGEbase +MonoT5      75.0   70.5   86.5   86.5   68.5   72.0    78.0     81.5    77.0   83.5    83.5   89.5    72.0   72.5   85.5   86.0
   BGEbase +BGEreranker 69.0   68.0   84.0   84.5   67.5   70.5    78.0     81.5    72.5   83.5∗   82.0   88.0    73.0   70.0   84.0   85.0

Table 1: Short-term retrieval performance. A blue background indicates a decrease in retrieval results after the
incorporation of LLM-generated text, while a purple background signifies an increase. The deeper the color, the
larger the discrepancy from the original results. Statistical significance at 0.05 relative to origin is marked with ∗ .




            (a) NQ                           (b) WebQ                              (c) TriviaQA                          (d) PopQA
Figure 2: Short-Term QA performance. For each retrieval method, we present both the average performance and
the range of variation exhibited by five LLMs. A red dashed line symbolizes the average EM score for zero-shot
question generation by LLMs. “Ori.” and “+LLMZ ” represent the average EM values when models use the original
dataset or a dataset enhanced with LLM-generated texts as context, respectively. Retrieval methods are abbreviated:
“Contri” for Contriever, “LLM-E” for LLM-Embedder, and “BGE-B” for BGEbase .

We find that: 1) Decreased Retrieval Effective-                           5.3      Spiral of Silence
ness Over Time: Figures 3a and 3b show a general
decline in Acc@5 across successive iterations for                         In the context of LLM-augmented RAG systems,
most methods, with an average drop of 21.4% for                           we have observed a rapid shift in response to the
NQ and 19.4% for PopQA from the first iteration                           integration of LLM-generated text, a decline in re-
to the last, except for a temporary improvement                           trieval performance over time, and stability in QA
in BM25 during the second iteration on PopQA.                             performance despite retrieval decline. To explain
This trend signals that the retrieval quality boost                       these phenomena, we draw on the theory of the
provided by LLM-generated text may be transient,                          “Spiral of Silence” as posited by Noelle-Neumann
with a propensity for degradation over time. 2)                           (1974), extending its principles to the behavior of
Stability in QA Performance Despite Retrieval                             RAG systems enhanced by LLMs. To explore the
Decline: Contrary to expectations, the QA per-                            presence of a “Spiral of Silence” phenomenon, we
formance does not mirror the retrieval accuracy’s                         propose three Hypotheses for investigation. (H1):
decrease. As shown in Figure 3c and 3d, the EM                            Dominance of LLM-Generated Texts: Retrieval
exhibit slight variations but generally maintain their                    models are more likely to prioritize LLM-generated
level throughout the iterations. While a diminished                       text in search results, which could result in LLM-
retrieval accuracy intuitively seems to undermine                         generated text taking a dominant position in the
the system’s capacity to output correct answers, this                     retrieval hierarchy. (H2): Marginalization of
does not unequivocally translate into a decline in                        Human-Generated Content: If human-authored
QA efficacy. In subsequent sections, we will delve                        text consistently loses ranking prominence through
deeper into the reasons behind these observations                         successive iterations, it may be excluded from the
and examine the complex dynamic relationship that                         top results until it becomes invisible, thus creating
may exist between retrieval and QA performance.                           silence. (H3): Homogenization of Opinions: The
                                                                          preferential ranking of LLM-generated text could
                                                          Method                 NQ     WebQ    TriviaQA   PopQA
                                                          BM25                   34.1    19.6      57.6     23.9
                                                          Contriever             72.8    75.2      80.1     67.0
                                                          LLM-Embedder           68.2    64.6      75.3     70.0
                                                          BGEbase                80.7    84.1      85.6     81.5
                                                          BM25+UPR               62.3    49.8      75.7     47.1
                                                          BM25+MonoT5            66.2    55.8      83.0     47.1
                                                          BM25+BGEreranker       64.4    55.2      81.6     46.6
                                                          BGEbase +UPR           74.4    69.3      79.1     71.2
       (a) NQ                    (b) PopQA                BGEbase +MonoT5        81.4    84.0      88.4     74.3
                                                          BGEbase +BGEreranker   67.2    74.2      83.2     72.8

                                                         Table 2: Percentage of LLM-generated documents occu-
                                                         pying the top 5 retrieval results, after augmenting each
                                                         query with five LLM-generated documents. The blue
                                                         background indicates a majority presence of human-
                                                         generated documents, while the purple background
                                                         denotes a predominance of LLM-generated documents.
       (c) NQ                   (d) PopQA
Figure 3: Long-Term RAG performance. The upper
section illustrates the retrieval outcomes for various
methods, while the lower section depicts the average
EM across LLMs. Iteration 1 represents the results
following the incorporation of zero-shot LLM-generated
text. Abbreviated re-ranking methods in the legend
are: +U for UPR, +M for MonoT5, and +BR for BGE-
                                                                 (a) NQ                    (b) PopQA
Reranker.
                                                         Figure 4: Average percentage of texts from various
                                                         sources within the top 50 search results over multiple
culminate in a uniformity of displayed perspectives      iterations across different search methods. For results
by the RAG system, potentially sidelining the ac-        on WebQ and TriviaQA, please refer to Figure 9 in
curacy or variety of the information.                    Appendix A.5.
   To verify (H1), we analyze Iteration 1 where
LLM-generated texts are first introduced to the re-         To validate (H2), we incorporate a temporal di-
trieval system. We calculate the proportion of these     mension, observing the percentage change of texts
texts appearing in the top 5 search results:             generated by various LLMs and humans within the
                                                         top 50 search results across different datasets over
                       LLM
                P
                  q∈Q cq                                 time. As shown in Figure 4, after ten iterations, the
    P= P          LLM + cHuman )
                                 × 100%           (1)
            q∈Q (cq      q                               percentage of human-generated texts significantly
                                                         decreased, falling below 10% for all datasets. This
where cLLM
         q     is the count of LLM-generated texts       pattern suggests a sustained diminishing impact
and cqHuman   is the count of human-generated texts      of human-contributed texts and hints at the pos-
in the top 5 search results for query q. Table 2         sibility of their eventual exclusion from search
reveals that, even with a modest inclusion of LLM-       results if the trend continues.
generated texts, most retrieval models often rank           To explore (H3), we examine the risk of poten-
them at the top. This behavior supports the find-        tial viewpoint homogenization in the RAG system
ings of Dai et al. (2023a), where LLM-rewritten          from both the diversity and accuracy dimensions
texts are preferred by retrieval models over the orig-   during the simulation. Diversity is quantified us-
inals. Our study extends this by directly generating     ing Self-BLEU (Zhu et al., 2018), which works
query-specific texts with LLMs. The preference           by comparing a generated text with other gener-
might stem from inherent biases within the sys-          ated texts to measure similarity. High similarity
tem or the actual relevance of the LLM-produced          results in a high Self-BLEU score, indicating lower
content. This suggests retrieval systems tend to         diversity and suggesting a convergence of view-
favor LLM-generated texts, making them more              points. As shown in Figure 5, upon introducing
prominent in search results, which can rapidly           zero-shot LLM-generated texts (Iteration 1), the
influence an RAG system’s behavior.                      Self-BLEU scores across different datasets expe-
                                                            of correct answers remains constant through the
                                                            iterations, aligning to Section 5.2. However, as it-
                                                            erations advance, correct answers diminish within
                                                            top documents for LLM-incorrect queries, reduc-
                                                            ing their contribution to the Acc@5 and thus de-
                                                            creasing retrieval performance. In contrast, for
       (a) NQ                     (b) PopQA                 LLM-correct queries, more retrieved documents
Figure 5: 3-gram Self-BLEU score for the top 5 search       containing the correct answer do not affect Acc@5
results over iterations, from the original dataset (Ori.)   or EM. Thus, the pattern discussed in Section 5.2
to subsequent iterations including LLM-generated texts.     can be explained by the “Spiral of Silence” the-
For results on WebQ and TriviaQA, please refer to Fig-      ory, which accounts for the observed dip in IR
ure 10 in Appendix A.5.
                                                            results and the sustained QA performance.

rience varying degrees of change. However, over             5.4   Effects of “Spiral of Silence” on ODQA
more iterations, the Self-BLEU scores for the top
5 results consistently rise and plateau across all          We will delve into a more nuanced discussion of
datasets, indicating a significant reduction in tex-        the impact of the “Spiral of Silence” within the
tual diversity with each iterative cycle. Subse-            context of ODQA. It is important to note that the
quently, we assessed whether the accuracy of the            influence of the phenomenon is not confined to this
top documents returned by the IR system tends               scenario; it may also be pertinent across all settings
toward uniformity over time. Figure 6 charts the            that involve knowledge retrieval, generation, and
number of documents with the correct answer in              the influx of text from LLMs. Specifically, our
the top 5 results ("Context Right Num") against the         analysis is structured around two dimensions: the
number of queries LLM answers correctly or incor-           query level and the document level.
rectly, across the Iteration1, 2, 5, 10. For simplicity,       At the query level, Figure 7a signifies the av-
we showcase only the NQ dataset’s averaged out-             erage count of queries shifting between consecu-
comes, but we find the same trends across other             tive iterations from incorrect to correct and vice
datasets. It indicates that in the initial iterations,      versa, respectively. Notably, during the 1->2 it-
fewer correct answer documents (e.g., “Context              eration, there is an initial surge in both metrics,
Right Num” of 0, 1, or 2) typically correlate with          which subsequently experience a sharp decline
a greater number of LLM-answered queries being              as the iterations continue. This suggests that the
incorrect (EM=0). Despite this, a significant frac-         LLM-generated text’s initial introduction catalyzes
tion of the top documents still include the correct         a more dynamic state, likely due to the correction
answer. When the LLM correctly answers a query              of existing errors or the introduction of new inaccu-
(EM=1), the correct answer documents within the             racies. Over time, however, the “Spiral of Silence”
top results can range anywhere from 1 to 5. As              effect seems to guide the system towards a state of
the iterations continue, the frequency of having 1          equilibrium where the transition rate stabilizes to
to 4 correct answer documents in the top 5 results          less than 1% per 200 queries. This means most
for each query diminishes, and by the Iteration10,          queries maintain their status as either correct or
contexts for LLM-correct queries almost always              incorrect, indicating that individual query QA
contain the correct answer, whereas contexts for            results become fixed.
LLM-incorrect answers almost always do not. This               At the document level, we compute the average
pattern demonstrates a trend towards polariza-              rank shifts of the first documents containing the cor-
tion and uniformity in the accuracy of provided             rect answer within retrieval results, under different
contexts as the RAG system iterates.                        LLM answer states. In Figure 7b, we observe that:
   At this point, we have confirmed through our             1) Different Trends of Correct Answer Rankings
experiments the presence of the “Spiral of Silence”         Based on Source: In instances where EM=0, cor-
phenomenon, as outlined in three tested hypotheses.         rect documents from all sources (“First Right From
Moreover, the dashed lines in Figure 6 represent            ALL Sources”) and from humans (“First Right
the total number of correct and incorrect LLM an-           From Human") both tend to be ranked lower over
swered queries, along with the Acc@5 retrieval              time. When EM=1, the rankings for correct docu-
metric over various iterations. The LLM’s rate              ments from all sources improve slightly, while rank-
Figure 6: Correlation between the number of top 5 search results containing the correct answer (“Context Right
Num”) and the accuracy of responses given by LLMs on the NQ dataset. The responses are categorized based on
Exact Match (EM) score: EM=1 for correct and EM=0 for incorrect. The overall number of queries that the LLMs
answered correctly (EM=1 Total) and incorrectly (EM=0 Total), along with the average retrieval accuracy (Acc@5)
are shown by dashed lines. The results are averaged across different LLMs, retrieval, and ranking methods.




(a) Average Query State Transition Number          (b) Ranking of the first retrieved document containing the correct answer
from incorrect to correct (“Average 0->1”) and     in each iteration, with LLM responses being incorrect (EM=0) or correct
correct to incorrect (“Average 1->0”) between      (EM=1). “First Right From All Sources” refers to the average rank for the
consecutive iterations, aggregated across all IR   first text containing the correct answer, where the source could be either
methods and datasets.                              LLM or human; “First Right From Human” is for human-only sources, both
                                                   considered across datasets and LLMs.
               Figure 7: Effects of “Spiral of Silence” on query and document level of RAG systems.


ings for correct answers from humans continue to                6    Analysis
decline. This suggests that the LLM’s correct texts
gain prominence in retrieval rankings over time,                To further comprehend the “Spiral of Silence” ef-
overshadowing correct texts from human-generated                fect, we illustrate its interaction with misinforma-
texts. 2) Gradual Dysfunction of the IR System                  tion introduced by adversaries using LLMs. More-
in Incorrect LLM Responses: When the LLM                        over, we test two information filtering mechanisms
provides incorrect answers (EM=0), there’s a risk               to alleviate the progression of the effect. For more
that documents that once rose to the top with ac-               information on the experimental setup and results,
curate information might increasingly be obscured               refer to Appendix A.7 and Appendix A.8.
by the growing mass of LLM-generated content.
This can lead to a scenario where the IR system,                7    Conclusion
originally intended to help users find precise infor-
                                                                In this study, we initiate our research from empiri-
mation, becomes less reliable. If it prioritizes and
                                                                cal observations, aiming to investigate the implica-
disseminates the LLM’s inaccuracies, a feedback
                                                                tions of progressively integrating LLM-generated
loop could ensue, solidifying these errors. This
                                                                text into RAG systems. To this end, We employ
concerning trend highlights the critical need for
                                                                the ODQA task as a case study to examine both
ongoing adjustments and improvements to the IR
                                                                the immediate and extended impacts of LLM text
systems to uphold their purpose.
                                                                on these systems. Our simulation has revealed the
                                                                emergence of a “Spiral of Silence” effect, suggest-
ing that without appropriate intervention, human-         Acknowledgements
generated content may progressively diminish its
                                                          This work is supported by the National
influence within RAG systems. Further investiga-
                                                          Natural Science Foundation of China
tion into this phenomenon reveals that unchecked
                                                          (62122077/62272439/62106251),             Beijing
accumulation of erroneous LLM-generated infor-
                                                          Municipal Science and Technology Project (No.
mation could lead to the overlooking of correct
                                                          Z231100010323002), and the Fundamental
information by IR systems, resulting in harm. We
                                                          Research Funds for the Central Universities.
urge the academic community to be vigilant and
take measures to prevent the potential misuse of
LLM-generated data.                                       References
                                                          Vaibhav Adlakha, Parishad BehnamGhader, Xing Han
                                                            Lu, Nicholas Meade, and Siva Reddy. 2023. Eval-
Limitations                                                 uating correctness and faithfulness of instruction-
                                                            following models for question answering. CoRR,
This study aims to present a new perspective on the         abs/2307.16877.
impact of LLM-generated texts entering the inter-         Faisal Alatawi, Lu Cheng, Anique Tahir, Mansooreh
net on RAG systems. However, the complexity of              Karami, Bohan Jiang, Tyler Black, and Huan Liu.
reality means that it is impossible to account for all      2021. A survey on echo chambers on social me-
variables. The methods of LLM text generation and           dia: Description, detection and mitigation. CoRR,
                                                            abs/2112.05084.
the mechanisms by which this content enters the
retrieval set are constantly changing, which could        Sina Alemohammad, Josue Casco-Rodriguez, Lorenzo
affect the performance of RAG systems. While                 Luzi, Ahmed Imtiaz Humayun, Hossein Babaei,
                                                             Daniel LeJeune, Ali Siahkoohi, and Richard G. Bara-
ODQA serves as an insightful approach to eval-               niuk. 2023. Self-consuming generative models go
uate the progression of RAG systems, it is nec-              MAD. CoRR, abs/2307.01850.
essary to recognize that ODQA assessments are
                                                          Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang,
not exhaustive in capturing the full spectrum of
                                                             Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei
information retrieval scenarios. Nonetheless, the            Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin,
simulation framework proposed in this research is            Runji Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu,
readily adaptable to other tasks that employ RAG             Keming Lu, Jianxin Ma, Rui Men, Xingzhang Ren,
systems. Our discussion introduces the “Spiral of            Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong
                                                             Tu, Peng Wang, Shijie Wang, Wei Wang, Shengguang
Silence” as a potential outcome of the proliferation         Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian
of LLM-generated texts. Although such a devel-               Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi
opment is not predetermined, given the myriad of             Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang,
factors at play in the real world, this work aims to         Yichang Zhang, Zhenru Zhang, Chang Zhou, Jin-
                                                             gren Zhou, Xiaohuan Zhou, and Tianhang Zhu. 2023.
foster a deeper investigation into the phenomenon            Qwen technical report. CoRR, abs/2309.16609.
and its prospective implications for information
diversity in AI-mediated environments.                    Jonathan Berant, Andrew Chou, Roy Frostig, and Percy
                                                            Liang. 2013. Semantic parsing on freebase from
                                                            question-answer pairs. In Proceedings of the 2013
                                                            Conference on Empirical Methods in Natural Lan-
Ethical Considerations                                      guage Processing, EMNLP 2013, 18-21 October
                                                            2013, Grand Hyatt Seattle, Seattle, Washington, USA,
This paper only explores the potential impact of the        A meeting of SIGDAT, a Special Interest Group of the
                                                            ACL, pages 1533–1544. ACL.
LLM-generated text, without involving the release
of the generated text and the intervention of social      Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann,
progress, so the possibility of ethical risks is small.     Trevor Cai, Eliza Rutherford, Katie Millican, George
                                                            van den Driessche, Jean-Baptiste Lespiau, Bogdan
We used publicly available LLMs and datasets to             Damoc, Aidan Clark, Diego de Las Casas, Aurelia
conduct experiments that did not involve any ethi-          Guy, Jacob Menick, Roman Ring, Tom Hennigan,
cal issues. In the appendix, we analyze the poten-          Saffron Huang, Loren Maggiore, Chris Jones, Albin
tial interplay between harmful information and the          Cassirer, Andy Brock, Michela Paganini, Geoffrey
                                                            Irving, Oriol Vinyals, Simon Osindero, Karen Si-
phenomena outlined in our paper, with a principal           monyan, Jack W. Rae, Erich Elsen, and Laurent Sifre.
objective to draw attention to this issue to advocate       2022. Improving language models by retrieving from
for its resolution.                                         trillions of tokens. In International Conference on
  Machine Learning, ICML 2022, 17-23 July 2022, Bal-          influence operations: Emerging threats and potential
  timore, Maryland, USA, volume 162 of Proceedings            mitigations. CoRR, abs/2301.04246.
  of Machine Learning Research, pages 2206–2240.
  PMLR.                                                     Google. 2023.    Introducing gemini: our largest
                                                              and most capable ai model.            https:
Deng Cai, Yan Wang, Wei Bi, Zhaopeng Tu, Xiaojiang            //blog.google/technology/ai/
  Liu, Wai Lam, and Shuming Shi. 2019. Skeleton-              google-gemini-ai/?utm_source=gdm&
  to-response: Dialogue generation guided by retrieval        utm_medium=referral#sundar-note.
  memory. In Proceedings of the 2019 Conference of            Accessed: 2023-12-06.
  the North American Chapter of the Association for
  Computational Linguistics: Human Language Tech-           Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasu-
  nologies, NAACL-HLT 2019, Minneapolis, MN, USA,             pat, and Ming-Wei Chang. 2020. REALM: retrieval-
  June 2-7, 2019, Volume 1 (Long and Short Papers),           augmented language model pre-training. CoRR,
  pages 1219–1228. Association for Computational              abs/2002.08909.
  Linguistics.
                                                            Hangfeng He, Hongming Zhang, and Dan Roth. 2023.
Canyu Chen and Kai Shu. 2023. Combating misinfor-             Rethinking with retrieval: Faithful large language
  mation in the age of llms: Opportunities and chal-          model inference. CoRR, abs/2301.00303.
  lenges. CoRR, abs/2311.05656.
                                                            Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong,
Jiawei Chen, Hongyu Lin, Xianpei Han, and                     Zhangyin Feng, Haotian Wang, Qianglong Chen,
   Le Sun. 2023. Benchmarking large language                  Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting
   models in retrieval-augmented generation. CoRR,            Liu. 2023a. A survey on hallucination in large lan-
   abs/2309.01431.                                            guage models: Principles, taxonomy, challenges, and
                                                              open questions. CoRR, abs/2311.05232.
Uthsav Chitra and Christopher Musco. 2020. Analyz-
  ing the impact of filter bubbles on social network        Yangsibo Huang, Samyak Gupta, Mengzhou Xia, Kai
  polarization. In WSDM ’20: The Thirteenth ACM In-           Li, and Danqi Chen. 2023b. Catastrophic jailbreak
  ternational Conference on Web Search and Data Min-          of open-source llms via exploiting generation. CoRR,
  ing, Houston, TX, USA, February 3-7, 2020, pages            abs/2310.06987.
  115–123. ACM.

Alexis Conneau, Kartikay Khandelwal, Naman Goyal,           Gautier Izacard, Mathilde Caron, Lucas Hosseini, Se-
  Vishrav Chaudhary, Guillaume Wenzek, Francisco              bastian Riedel, Piotr Bojanowski, Armand Joulin,
  Guzmán, Edouard Grave, Myle Ott, Luke Zettle-               and Edouard Grave. 2022. Unsupervised dense in-
  moyer, and Veselin Stoyanov. 2020. Unsupervised             formation retrieval with contrastive learning. Trans.
  cross-lingual representation learning at scale. In Pro-     Mach. Learn. Res., 2022.
  ceedings of the 58th Annual Meeting of the Associa-
                                                            Gautier Izacard and Edouard Grave. 2021. Leveraging
  tion for Computational Linguistics, ACL 2020, On-
                                                              passage retrieval with generative models for open do-
  line, July 5-10, 2020, pages 8440–8451. Association
                                                              main question answering. In Proceedings of the 16th
  for Computational Linguistics.
                                                              Conference of the European Chapter of the Associ-
Sunhao Dai, Yuqi Zhou, Liang Pang, Weihao Liu,                ation for Computational Linguistics: Main Volume,
  Xiaolin Hu, Yong Liu, Xiao Zhang, and Jun Xu.               EACL 2021, Online, April 19 - 23, 2021, pages 874–
  2023a. Llms may dominate information access: Neu-           880. Association for Computational Linguistics.
  ral retrievers are biased towards llm-generated texts.
  CoRR, abs/2310.20501.                                     Gautier Izacard, Patrick S. H. Lewis, Maria Lomeli,
                                                              Lucas Hosseini, Fabio Petroni, Timo Schick, Jane
Yi Dai, Hao Lang, Yinhe Zheng, Bowen Yu, Fei Huang,           Dwivedi-Yu, Armand Joulin, Sebastian Riedel, and
   and Yongbin Li. 2023b. Domain incremental lifelong         Edouard Grave. 2023. Atlas: Few-shot learning
   learning in an open world. In Findings of the Asso-        with retrieval augmented language models. J. Mach.
   ciation for Computational Linguistics: ACL 2023,           Learn. Res., 24:251:1–251:43.
  Toronto, Canada, July 9-14, 2023, pages 5844–5865.
   Association for Computational Linguistics.               Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu,
                                                              Dan Su, Yan Xu, Etsuko Ishii, Yejin Bang, Andrea
Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding,                Madotto, and Pascale Fung. 2023. Survey of halluci-
  Jiezhong Qiu, Zhilin Yang, and Jie Tang. 2022. Glm:         nation in natural language generation. ACM Comput.
  General language model pretraining with autoregres-         Surv., 55(12):248:1–248:38.
  sive blank infilling. In Proceedings of the 60th An-
  nual Meeting of the Association for Computational         Ray Jiang, Silvia Chiappa, Tor Lattimore, András
  Linguistics (Volume 1: Long Papers), pages 320–335.         György, and Pushmeet Kohli. 2019. Degenerate feed-
                                                              back loops in recommender systems. In Proceedings
Josh A. Goldstein, Girish Sastry, Micah Musser, Re-           of the 2019 AAAI/ACM Conference on AI, Ethics,
  nee DiResta, Matthew Gentzel, and Katerina Sedova.          and Society, AIES 2019, Honolulu, HI, USA, January
  2023. Generative language models and automated              27-28, 2019, pages 383–390. ACM.
Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019.          ACM International Conference on Web Search and
   Billion-scale similarity search with GPUs. IEEE            Data Mining, WSDM 2019, Melbourne, VIC, Aus-
   Transactions on Big Data, 7(3):535–547.                    tralia, February 11-15, 2019, pages 222–230. ACM.
Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke         Ye Liu, Semih Yavuz, Rui Meng, Meghana Moor-
 Zettlemoyer. 2017. Triviaqa: A large scale distantly         thy, Shafiq Joty, Caiming Xiong, and Yingbo
 supervised challenge dataset for reading comprehen-          Zhou. 2023b. Exploring the integration strategies
 sion. In Proceedings of the 55th Annual Meeting of           of retriever and large language models. CoRR,
 the Association for Computational Linguistics, ACL           abs/2308.12574.
 2017, Vancouver, Canada, July 30 - August 4, Volume
 1: Long Papers, pages 1601–1611. Association for           Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das,
 Computational Linguistics.                                   Hannaneh Hajishirzi, and Daniel Khashabi. 2022.
Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick           When not to trust language models: Investigating
  S. H. Lewis, Ledell Wu, Sergey Edunov, Danqi Chen,          effectiveness and limitations of parametric and non-
  and Wen-tau Yih. 2020. Dense passage retrieval for          parametric memories. CoRR, abs/2212.10511.
  open-domain question answering. In Proceedings of
  the 2020 Conference on Empirical Methods in Nat-          Elisabeth Noelle-Neumann. 1974. The spiral of silence
  ural Language Processing, EMNLP 2020, Online,                a theory of public opinion. Journal of communica-
  November 16-20, 2020, pages 6769–6781. Associa-              tion, 24(2):43–51.
  tion for Computational Linguistics.
                                                            Rodrigo Frassetto Nogueira, Zhiying Jiang, Ronak
Tom Kwiatkowski, Jennimaria Palomaki, Olivia Red-             Pradeep, and Jimmy Lin. 2020. Document ranking
  field, Michael Collins, Ankur P. Parikh, Chris Alberti,     with a pretrained sequence-to-sequence model. In
  Danielle Epstein, Illia Polosukhin, Jacob Devlin, Ken-      Findings of the Association for Computational Lin-
  ton Lee, Kristina Toutanova, Llion Jones, Matthew           guistics: EMNLP 2020, Online Event, 16-20 Novem-
  Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob                ber 2020, volume EMNLP 2020 of Findings of ACL,
  Uszkoreit, Quoc Le, and Slav Petrov. 2019. Natu-            pages 708–718. Association for Computational Lin-
  ral questions: a benchmark for question answering           guistics.
  research. Trans. Assoc. Comput. Linguistics, 7:452–
  466.                                                      OpenAI. 2022. ChatGPT. https://openai.com/
                                                              blog/chatgpt. Accessed: January 10, 2024.
Patrick S. H. Lewis, Ethan Perez, Aleksandra Pik-
  tus, Fabio Petroni, Vladimir Karpukhin, Naman
  Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih,         OpenAI. 2023. GPT-4 technical report.            CoRR,
  Tim Rocktäschel, Sebastian Riedel, and Douwe                abs/2303.08774.
  Kiela. 2020. Retrieval-augmented generation for
  knowledge-intensive NLP tasks. In Advances in Neu-        Yikang Pan, Liangming Pan, Wenhu Chen, Preslav
  ral Information Processing Systems 33: Annual Con-          Nakov, Min-Yen Kan, and William Wang. 2023. On
  ference on Neural Information Processing Systems            the risk of misinformation pollution with large lan-
  2020, NeurIPS 2020, December 6-12, 2020, virtual.           guage models. In Findings of the Association for
                                                              Computational Linguistics: EMNLP 2023, Singapore,
Paul Pu Liang, Chiyu Wu, Louis-Philippe Morency, and          December 6-10, 2023, pages 1389–1403. Association
  Ruslan Salakhutdinov. 2021. Towards understanding           for Computational Linguistics.
  and mitigating social biases in language models. In
  Proceedings of the 38th International Conference          Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
  on Machine Learning, ICML 2021, 18-24 July 2021,            Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
  Virtual Event, volume 139 of Proceedings of Machine         Wei Li, and Peter J. Liu. 2020. Exploring the limits
  Learning Research, pages 6565–6576. PMLR.                   of transfer learning with a unified text-to-text trans-
                                                              former. J. Mach. Learn. Res., 21:140:1–140:67.
Chen Lin, Dugang Liu, Hanghang Tong, and Yanghua
  Xiao. 2022. Spiral of silence and its application in      Ori Ram, Yoav Levine, Itay Dalmedigos, Dor Muhlgay,
  recommender systems. IEEE Trans. Knowl. Data                Amnon Shashua, Kevin Leyton-Brown, and Yoav
  Eng., 34(6):2934–2947.                                      Shoham. 2023. In-context retrieval-augmented lan-
Chang Liu, Xiaoguang Li, Lifeng Shang, Xin Jiang,             guage models. CoRR, abs/2302.00083.
  Qun Liu, Edmund Y. Lam, and Ngai Wong. 2023a.
  Gradually excavating external knowledge for implicit      Devendra Singh Sachan, Mike Lewis, Mandar Joshi,
  complex question answering. In Findings of the As-          Armen Aghajanyan, Wen-tau Yih, Joelle Pineau, and
  sociation for Computational Linguistics: EMNLP              Luke Zettlemoyer. 2022. Improving passage retrieval
  2023, Singapore, December 6-10, 2023, pages 14405–          with zero-shot question generation. In Proceedings
  14417. Association for Computational Linguistics.           of the 2022 Conference on Empirical Methods in
                                                              Natural Language Processing, EMNLP 2022, Abu
Dugang Liu, Chen Lin, Zhilin Zhang, Yanghua Xiao,             Dhabi, United Arab Emirates, December 7-11, 2022,
  and Hanghang Tong. 2019. Spiral of silence in rec-          pages 3781–3797. Association for Computational
  ommender systems. In Proceedings of the Twelfth             Linguistics.
Victor Sanh, Albert Webson, Colin Raffel, Stephen H.        Hang Xu, Haoze Sun, Hongda Zhang, Hui Liu,
  Bach, Lintang Sutawika, Zaid Alyafeai, Antoine            Jiaming Ji, Jian Xie, Juntao Dai, Kun Fang, Lei
  Chaffin, Arnaud Stiegler, Arun Raja, Manan Dey,           Su, Liang Song, Lifeng Liu, Liyun Ru, Luyao Ma,
  M Saiful Bari, Canwen Xu, Urmish Thakker,                 Mang Wang, Mickel Liu, MingAn Lin, Nuolan Nie,
  Shanya Sharma Sharma, Eliza Szczechla, Taewoon            Peidong Guo, Ruiyang Sun, Tao Zhang, Tianpeng
  Kim, Gunjan Chhablani, Nihal V. Nayak, Debajyoti          Li, Tianyu Li, Wei Cheng, Weipeng Chen, Xian-
  Datta, Jonathan Chang, Mike Tian-Jian Jiang, Han          grong Zeng, Xiaochuan Wang, Xiaoxi Chen, Xin
  Wang, Matteo Manica, Sheng Shen, Zheng Xin Yong,          Men, Xin Yu, Xuehai Pan, Yanjun Shen, Yiding
  Harshit Pandey, Rachel Bawden, Thomas Wang, Tr-           Wang, Yiyu Li, Youxin Jiang, Yuchen Gao, Yu-
  ishala Neeraj, Jos Rozen, Abheesht Sharma, An-            peng Zhang, Zenan Zhou, and Zhiying Wu. 2023.
  drea Santilli, Thibault Févry, Jason Alan Fries, Ryan     Baichuan 2: Open large-scale language models.
  Teehan, Teven Le Scao, Stella Biderman, Leo Gao,          CoRR, abs/2309.10305.
  Thomas Wolf, and Alexander M. Rush. 2022. Multi-
  task prompted training enables zero-shot task gener-    Wenhao Yu, Dan Iter, Shuohang Wang, Yichong Xu,
  alization. In The Tenth International Conference on      Mingxuan Ju, Soumya Sanyal, Chenguang Zhu,
  Learning Representations, ICLR 2022, Virtual Event,      Michael Zeng, and Meng Jiang. 2023. Generate
  April 25-29, 2022. OpenReview.net.                       rather than retrieve: Large language models are
                                                           strong context generators. In The Eleventh Inter-
Dietram A Scheufle and Patricia Moy. 2000. Twenty-         national Conference on Learning Representations,
  five years of the spiral of silence: A conceptual re-    ICLR 2023, Kigali, Rwanda, May 1-5, 2023. Open-
  view and empirical outlook. International journal of     Review.net.
  public opinion research, 12(1):3–28.
                                                          Peitian Zhang, Shitao Xiao, Zheng Liu, Zhicheng Dou,
Nina Schick. 2020. Deep Fakes and the Infocalypse:          and Jian-Yun Nie. 2023. Retrieve anything to aug-
  What You Urgently Need To Know. Monoray.                  ment large language models. CoRR, abs/2310.07554.

Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Yarin       Shuyan Zhou, Uri Alon, Frank F. Xu, Zhengbao Jiang,
   Gal, Nicolas Papernot, and Ross J. Anderson. 2023.       and Graham Neubig. 2023. Docprompting: Gener-
   The curse of recursion: Training on generated data       ating code by retrieving the docs. In The Eleventh
   makes models forget. CoRR, abs/2305.17493.               International Conference on Learning Representa-
                                                            tions, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier       OpenReview.net.
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,
  Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal      Yaoming Zhu, Sidi Lu, Lei Zheng, Jiaxian Guo, Weinan
  Azhar, Aurélien Rodriguez, Armand Joulin, Edouard         Zhang, Jun Wang, and Yong Yu. 2018. Texygen: A
  Grave, and Guillaume Lample. 2023. Llama: Open            benchmarking platform for text generation models.
  and efficient foundation language models. CoRR,           In The 41st International ACM SIGIR Conference on
  abs/2302.13971.                                           Research & Development in Information Retrieval,
                                                            SIGIR 2018, Ann Arbor, MI, USA, July 08-12, 2018,
Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot,       pages 1097–1100. ACM.
  and Ashish Sabharwal. 2023. Interleaving retrieval
  with chain-of-thought reasoning for knowledge-          Terry Yue Zhuo, Yujin Huang, Chunyang Chen, and
  intensive multi-step questions. In Proceedings of         Zhenchang Xing. 2023. Exploring AI ethics of chat-
  the 61st Annual Meeting of the Association for Com-       gpt: A diagnostic analysis. CoRR, abs/2301.12867.
  putational Linguistics (Volume 1: Long Papers),
  ACL 2023, Toronto, Canada, July 9-14, 2023, pages
  10014–10037. Association for Computational Lin-
  guistics.

Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas
  Muennighof. 2023. C-pack: Packaged resources
  to advance general chinese embedding. CoRR,
  abs/2309.07597.

Danni Xu, Shaojing Fan, and Mohan S. Kankanhalli.
  2023. Combating misinformation in the era of gen-
  erative AI models. In Proceedings of the 31st ACM
  International Conference on Multimedia, MM 2023,
  Ottawa, ON, Canada, 29 October 2023- 3 November
  2023, pages 9291–9298. ACM.

Aiyuan Yang, Bin Xiao, Bingning Wang, Borong Zhang,
  Ce Bian, Chao Yin, Chenxu Lv, Da Pan, Dian Wang,
  Dong Yan, Fan Yang, Fei Deng, Feng Wang, Feng
  Liu, Guangwei Ai, Guosheng Dong, Haizhou Zhao,
Algorithm 1 Simulation Process                          A.3    Post-Process Details
  function RUN RAG(D, Q)                                During the experimental process, we observe that
     Res ← empty list                                   the response texts from LLMs occasionally con-
     for q ∈ Q do                                       tain specific phrases at the beginning that indicate
         D′ ← R ETRIEVE(q, D)                           their identity. These phrases are difficult to remove
         p ← G EN P ROMPT(q)                            through prompts and are irrelevant to the topic at
         S ← G ENA NSWER(p, D′ , q)                     hand. Examples include sentences such as:
         S ′ ← P OST P ROC(S)
         Add (q, D′ , S ′ ) to Res                         • “I’d be happy to assist you
     end for                                                 with your question.”
     return Res
  end function                                             • “According to my knowledge...”

                                                           • “As an AI language model...”
    D0 ← L OAD DATA
    initRes ← RUN RAG(D0 , Q)                              We collect over 40 such sentences using a man-
    baseP erf ← E VAL RAG(initRes)                      ual annotation approach and filter each LLM-
    T ← G EN Z ERO S HOT                                generated text through string matching. If a match-
    D1 ← D0 combined with T                             ing string is found, the corresponding sentence or
    t ← number of iterations                            fragment is removed.
    for i ← 1 to t do
        iterRes ← RUN RAG(Di , Q)                       A.4    Implementation Details.
        perfi ← E VAL RAG(iterRes)                      To construct and execute the simulated iterative
        Di+1 ← U PDATE DATA(Di , iterRes)               framework, we adopt a diverse array of tools and
    end for                                             technologies to facilitate real-time interaction be-
                                                        tween various retrieval methods, indexing architec-
A     Appendix                                          tures, and LLMs. We implement the APIs of vari-
                                                        ous LLMs relying on api-for-open-llm3 . With inte-
A.1    Discussion of Application on “Spiral of          gration of LangChain4 with Faiss (Johnson et al.,
       Silence”                                         2019) and Elasticsearch5 , we execute batched in-
In aligning the “Spiral of Silence” theory with the     cremental updates of LLM-generated documents
focus of this study, emphasis on the aspect of the      in each iteration, thus simulating the process of
“individual’s will to express” inherent in the origi-   document index updating by search engines in real-
nal theory is purposefully diminished. The factors      world scenarios. To maintain the diversity of the
influencing the “Spiral of Silence” phenomenon,         generated texts, we set the temperature at 0.7 for
as mentioned in Scheufle and Moy (2000), with           all LLMs. In each iteration of the experiment, ex-
media and temporality being the principal elements      cept for the zero-shot setting, we keep the size of
within RAG systems, directly affect the relative        the context document set Di′ fixed at 5. We rerank
standing of LLM and human texts as the system           the first 100 documents recalled by the retrieval
evolves. While the individual’s desire to express       method when the step is applied. We apply the
may be indirectly affected by media and temporal-       LLMs to generate response text, post-process via
ity, these are not the primary drivers of the “Spiral   rules, and then merge their outputs into the index
of Silence” within RAG systems. In RAG systems,         for each query in every iteration. Therefore, for
we hypothesize that texts generated by LLMs will        each iteration, we will add 4k new samples to the
increasingly be favored in the hierarchy of informa-    index. The total number of iterations t is set at 10,
tion retrieval, whereas texts authored by humans        which results in a total of 40k invocations of the
might be systematically marginalized, resulting in      LLMs for each experimental run.
a structural form of “passive silencing".                  3
                                                            https://github.com/xusenlinzy/
                                                        api-for-open-llm
A.2    Pseudo-Code of Simulation Process                  4
                                                            https://github.com/langchain-ai/
                                                        langchain
The pseudo-code of the simulation process in sec-         5
                                                            https://github.com/elastic/
tion 3.2 is shown in Algotirhm 1.                       elasticsearch
                                                                   (a) WebQ                      (b) TriviaQA
       (a) WebQ                   (b) TriviaQA               Figure 10: 3-gram Self-BLEU score for the top 5 search
                                                             results over iterations for WebQ and TriviaQA, from the
                                                             original dataset (Ori.) to subsequent iterations including
                                                             LLM-generated texts.

                                                                 Dataset            NQ                  WebQ
                                                                 Iteration    Acc@20      EM       Acc@20       EM
                                                                 1              68.5      29.5       66.0       35.5
       (c) WebQ                   (d) TriviaQA
                                                                 2              67.5      28.5       65.0       38.7
Figure 8: Long-Term RAG performance for WebQ and                 3              64.0      29.3       63.5       38.0
TriviaQA. The upper section illustrates the retrieval out-       4              63.0      32.5       62.5       43.5
comes for various methods, while the lower section
                                                                 5              60.5      32.3       62.5       41.8
depicts the average EM across LLMs. Iteration 1 repre-
                                                                 6              58.0      32.0       61.5       43.3
sents the results following the incorporation of zero-shot
                                                                 7              55.5      30.7       61.5       43.2
LLM-generated text. Abbreviated re-ranking methods
in the legend are: +U for UPR, +M for MonoT5, and                8              52.0      33.7       60.5       44.0
+BR for BGE-Reranker.                                            9              51.5      32.8       61.0       44.3
                                                                 10             47.5      33.7       58.5       44.2

                                                             Table 3: BM25 retrieval performance (Acc@20) and
                                                             QA performance (EM) across iterations for NQ and
                                                             WebQ under the evolving LLM setting.


                                                             For the text generation models, we use progres-
       (a) WebQ                   (b) TriviaQA               sively larger versions of the Qwen1.5 model (Bai
                                                             et al., 2023) across different iterations: 0.5b, 1.8b,
Figure 9: Average Percentage of texts from various
sources within the top 50 search results over multiple       and 4b versions for the first three iterations. For
iterations across different search and methods for WebQ      iterations four to seven, we employ Qwen1.5-7b-
and TriviaQA.                                                Chat (Bai et al., 2023), LLaMA2-7b-Chat (Touvron
                                                             et al., 2023), and Baichuan2-7b-Chat (Yang et al.,
                                                             2023). Finally, for the eighth to tenth iterations, we
A.5    Results on WebQ and TriviaQA
                                                             utilize GPT-3.5-Turbo (OpenAI, 2022), LLaMA2-
 Figure 8 shows long-term RAG performance on                 13b-Chat (Touvron et al., 2023), and Qwen1.5-14b-
WebQ and TriviaQA.                                           Chat (Bai et al., 2023). This setup simulates the
   The percentage from various sources and the               impact of increasing model capabilities on the RAG
Self-BLEU of the retrieval results on WebQ and               system over time.
TriviaQA are shown in Figure 9 and Figure 10.                   Analysis of Experimental Results: From the
                                                             experimental results, we can observe that: 1) Re-
A.6    Simulation with Model Evolution
                                                             trieval Performance Continues to Decline: Ac-
In this section, we explore the impact of the con-           cording to the Acc@20 results reported in Table 3,
tinuous influx of text generated by evolving LLMs            even with the gradual improvement of LLM perfor-
on RAG systems over time. To this end, we ex-                mance in the simulation, the retrieval performance
periment by using a series of LLMs, ranging from             exhibits a general downward trend over time. Com-
weak to strong, to observe the phenomenon.                   pared to the results in Table 1, the improvements in
   Experimental Setup: We conduct experiments                retrieval performance are also limited for weaker
based on BM25 on the NQ and WebQ datasets.                   LLMs in the initial stage (73.5 → 68.5, 71.0 →
Figure 11: Correlation between the number of top 5 BM25 search results containing the correct answer ("Context
Right Num") and the accuracy of responses given by evolving LLMs on the NQ dataset. The responses are
categorized based on n Exact Match (EM) score: EM=1 for correct and EM=0 for incorrect. The overall number
of queries that the LLMs answered correctly (EM=1 Total) and incorrectly (EM=0 Total), along with the average
retrieval accuracy (Acc@5) are shown by dashed lines. The results are averaged across different LLMs.


              Iteration    NQ     WebQ                            Model Name                NQ     WebQ
              1           77.7     87.0                           Qwen1.5-0.5b-Chat        12.5      6.9
              2           45.9     64.3                           Qwen1.5-1.8b-Chat         7.4      4.4
              3           27.2     48.6                           Qwen1.5-4b-Chat           8.5      6.3
              4           18.0     40.2                           Qwen-7b-Chat              1.1      1.7
              5           14.6     36.2                           LLaMA2-7b-Chat           20.9     18.5
              6           12.3     32.6                           Baichuan2-7b-Chat        10.3      7.6
              7           10.1     28.9                           LLaMA2-13B-Chat          19.1     19.9
              8            8.6     25.6                           Qwen1.5-14b-chat          0.9      1.8
              9            6.7     21.9                           GPT-3.5-Turbo            13.5     13.7
              10           5.8     19.2                           Human                     5.8     19.2

Table 4: Percentage of human text in the top 5 BM25        Table 5: Percentage of generated text by different LLMs
retrieval results across iterations for NQ and WebQ un-    in the top 5 BM25 retrieval results at the end of the
der the evolving LLM setting.                              simulation (Iteration 10) for NQ and WebQ under the
                                                           evolving LLM setting.

66.0). 2) QA Results Show Improvement: Based
on the EM results reported in Table 3, we can see          Table 6 presents the diversity of retrieval results,
that with the expansion of the LLM scale, the QA           while Figure 11 illustrates the relationship between
results have improved, especially from the third           retrieval accuracy and the generated answers. As
to the fourth iteration, where the model expanded          the model evolves, the experimental results remain
from less than 4B to 7B, resulting in more than a          consistent with the conclusion in Section 5.3: the
10% improvement in QA results on both datasets.            diversity of retrieval results continues to decline,
Considering that QA results remain stable in Fig-          and polarization occurs. In summary, the experi-
ure 3 when LLMs are unchanged, the current im-             mental results indicate that the evolution of LLMs
provement likely stems from the enhanced capa-             will not prevent the occurrence of the “Spiral of
bilities of the LLM itself. 3) The Existence of            Silence” phenomenon.
the “Spiral of Silence” Phenomenon: In Table 4,
                                                           A.7   Effects of Misinformation
we present the proportion of human text in the top
5 retrieval results during the iterations. It can be       In previous sections, we explored the impact of
observed that LLM-generated text still dominates           non-maliciously LLM-generated texts on the evo-
the retrieval results, and the influence of human          lution of the RAG system over time. In this section,
text continues to decline. In Table 5, we report the       we will discuss the persistence of the “Spiral of
proportion of different LLM-generated texts in the         Silence” when attackers deliberately inject specific
top 5 retrieval results after the tenth iteration. Over-   misinformation into the RAG system, how misin-
all, texts generated by larger-scale LLMs occupy a         formation could affect the system over time, and
slightly higher proportion, but this is not absolute.      the feasibility of targeted misinformation injection.
             Iteration    NQ     WebQ                    tribute positively to this metric if it encompasses
                                                         a and is validated by GPT-3.5-Turbo as being sup-
             1           27.5     25.4                   portive of a. The EMllm for the correct answers
             2           49.8     39.5                   and specific incorrect answers, as generated by the
             3           65.6     53.3                   CTRLGEN method containing misinformation, are
             4           74.4     60.9                   presented in Table 7.
             5           70.8     59.2
             6           72.3     60.9                      Moreover, we substantiate the rationality of em-
             7           74.8     63.6                   ploying EM as a QA evaluation metric in the experi-
             8           75.5     64.5                   ments of Section 4 by calculating the Pearson corre-
             9           75.3     64.7                   lation coefficient between EMllm and EM based on
             10          78.2     68.4                   the experimental results in this section. We observe
                                                         that the EMllm values for the texts generated by
Table 6: 3-gram Self-BLEU score for the top 5 BM25       the other four LLMs, as verified by GPT-3.5-Turbo,
search results over iterations for NQ and WebQ under     have an average correlation exceeding 0.5 across
the evolving LLM setting.
                                                         four datasets when compared to the EM values ob-
                                                         tained through direct string matching, as shown in
   Experimental Setup: Our experiment follows            Table 8. This demonstrates a significant correlation
the CTRLGEN method detailed in Pan et al.                between the two metrics. For incorrect answers, the
(2023), which aligns well with the zero-shot set-        correlation is relatively lower, indicating the neces-
ting used in our trials and simulates the intent of      sity of using GPT-3.5-Turbo to further filter texts
malicious actors to create and propagate false infor-    in the exploration of misinformation. Considering
mation. Specifically, for each query, we generate        the higher efficiency of direct EM calculation over
five incorrect answers using GPT-3.5-Turbo and           EMllm , we use EM to evaluate the QA quality of
then randomly select one to guide five different         the RAG system for experiments in other sections.
LLMs to each create a document supporting that
incorrect response. These documents replace the             Analysis of Experimental Results: From the
zero-shot data in the index from the experiments in      experimental results, we can observe that: 1) The
Section 3 and are used for simulated iterative exper-    “Spiral of Silence” Still Exists: We first investigate
iments. Details of the prompts used are provided in      the presence of the “Spiral of Silence” phenomenon
Appendix A.9. For the sake of conciseness, we re-        when misinformation targeting the objective is in-
port only the experimental results for four retrieval    jected into the corpus. As shown in Table 9, al-
methods.                                                 though the majority of the injected information is
   Experimental Evaluation: When generating              misleading, the content generated by the LLMs
texts containing misinformation using LLMs, we           is still quickly ranked at the top by the retrieval
face two primary challenges. First, the model may        systems, taking a dominant position. When com-
ignore the instructions, thus inadvertently gener-       paring four different retrieval methods, the BM25
ating texts that only contain the correct answer.        algorithm shows greater robustness than the others,
Second, even if the LLM-generated text includes          being least affected by the LLM-generated content.
the provided incorrect answer, the content may not       However, it is noteworthy that approximately 20%
genuinely support that answer. To address these          of the content generated by the LLM could still be
issues, we utilize GPT-3.5-Turbo to evaluate the         quickly placed in the forefront of the search results
alignment of text t with the given answer a, which       by the BM25 algorithm. Figure 12 illustrates that
could be either correct or incorrect. This evaluation    over time, human-written texts are gradually ex-
complements the calculation of the EM metric for         cluded from the searchable range, and as depicted
texts generated by LLMs. We define the EMllm             in Figure 13, the phenomenon of homogenization
metric as follows:                                       of opinions in search results persists. This fur-
                 (                                       ther indicates that regardless of the accuracy of
                   1, if t contains and supports a       the LLM-generated information, the “Spiral of Si-
EMllm (t, a) =
                   0, otherwise                          lence” phenomenon remains present. 2) The RAG
                                                   (2)   System has a Limited Degree of Self-Correction
Here, a represents an answer that the text t is being    Capability: LLM-generated texts containing mis-
evaluated against. The text t is deemed to con-          information lead to a significant decline in retrieval
  Model                              NQ                 WebQ                  TriviaQA              PopQA
                           Correct    Incorrect   Correct Incorrect       Correct Incorrect    Correct Incorrect
  GPT-3.5-Turbo             0.015         0.7     0.075        0.57       0.105      0.57       0.045       0.71
  Baichuan2-13B-Chat         0.11       0.595      0.21        0.44        0.16     0.455         0.1       0.65
  Qwen-14B-Cha              0.065       0.61       0.11       0.565       0.165     0.535       0.05        0.7
  ChatGLM3-6B               0.085       0.605     0.195       0.435       0.245     0.415       0.105       0.61
  LLaMA2-13B-Chat            0.04        0.43     0.085       0.385       0.125     0.405        0.03       0.55
  Avg                       0.063       0.588     0.135       0.479        0.16     0.476       0.066      0.644

             Table 7: EMllm of different models for Correct answers and specific Incorrect answers.




          (a) NQ                    (b) WebQ               (c) TriviaQA                       (d) PopQA
Figure 12: Average percentage of texts from various sources within the top 50 search results over multiple iterations
when adding Misinformation across different search methods.




Figure 13: Correlation between the number of top 5 search results containing the correct answer (“Context Right
Num”) and the accuracy of responses given by LLMs on the NQ dataset when adding Misinformation. The
responses are categorized based on EMllm score: EM_L=1 for correct and EM_L=0 for incorrect. The overall
number of queries that the LLMs answered correctly (EM_L=1 Total) and incorrectly (EM_L=0 Total), along with
the average retrieval accuracy (Acc@5) are shown by dashed lines. The results are averaged across different LLMs,
retrieval and ranking methods.
   Answer Type     NQ      WebQ     TriviaQA   PopQA     still severely compromise the system’s accuracy
   Correct        0.740    0.568      0.836     0.529
   Incorrect      -0.574   -0.389    -0.385    -0.121
                                                         and enable the manipulation of the RAG system
                                                         to consistently output specific misinformation in
Table 8: Evaluation of the Average Pearson Correlation   response to certain questions. Therefore, without
Coefficient between EM and EMllm for Correct and         timely intervention, the “Spiral of Silence” phe-
Incorrect Answers.
                                                         nomenon could marginalize accurate information,
                                                         leading to severe misinformation consequences.
  Method           NQ      WebQ     TriviaQA   PopQA
  BM25              26.7     17.7      24.7      47.4    A.8   Attempts to Alleviate the “Spiral of
  Contriever        60.7     62.5      64.7      67.2          Silence"
  LLM-Embedder      65.8     70.4      73.3      74.2
  BGEbase           50.7     48.6      63.2      60.6    The “Spiral of Silence” effect could lead to the
                                                         marginalization of human-generated text expres-
Table 9: Percentage of LLM-generated documents with
Misinformation occupying the top 5 retrieval results,    sion and further enhance the homogeneity of re-
after augmenting each query with five documents gen-     trieval outcomes. If left unaddressed, this phe-
erated by LLMs. Data entries framed by a blue back-      nomenon could precipitate a series of adverse reper-
ground indicate a majority presence of human-generated   cussions. To mitigate or eliminate the influence of
documents, while entries with a purple background de-    the “Spiral of Silence” effect, this section initiates
note a predominance of LLM-generated documents.          a discussion on two fronts. First, from the perspec-
                                                         tive of the authenticity of sources, we employ the
                                                         widely used AIGC detection technologies to filter
and QA performance based on the RAG system
                                                         out and exclude all non-human-produced texts at
compared to results in Section 5.2. With the con-
                                                         the top of the search results. Second, addressing the
tinuation of the iteration process, the number of
                                                         validity of content, we strive to maintain diversity
correct answers increased and the number of incor-
                                                         among the top search results to overcome potential
rect answers decreased, albeit by a small margin.
                                                         issues caused by excessive homogenization.
This suggests that the RAG system has a certain de-
                                                            Experimental Setup: To balance the efficiency
gree of self-correction capability, which may stem
                                                         and effectiveness of the retrieval system, for each
from the model’s knowledge or the human-written
                                                         set of search results returned by the system, we
texts containing correct information retrieved in the
                                                         post-process to acquire the top 5 qualifying doc-
initial stages. 3) The Introduction of a Small
                                                         uments that are visible to the LLMs. In the
Amount of the LLM-generated Texts with Spe-
                                                         source filtering experiment, we employ the Hello-
cific Misleading Information during the Itera-
                                                         SimpleAI/chatgpt-qa-detector-roberta6 model to
tive Process could Inject such Information into
                                                         authenticate the origins of the texts within the
the RAG Output: In Figure 14, we quantify the
                                                         search results, aiming to retain the first 5 docu-
EMllm metric of the original and specific mislead-
                                                         ments identified as human-generated and supply
ing answers generated by the RAG system based
                                                         them as input to the LLM’s context. For the con-
on four retrieval methods at various iteration stages.
                                                         tent filtering part of the experiment, we apply a
The results show that after the purposeful addi-
                                                         selection process based on computing the 3-gram
tion of misleading information (before the first it-
                                                         Self-BLEU scores. The specific procedure is as
eration), the proportion of RAG system-generated
                                                         follows: For the top 5 documents returned for each
answers containing specific misleading informa-
                                                         search query, we initially calculate their Self-BLEU
tion significantly increases, especially on NQ and
                                                         scores; if the score exceeds a predetermined thresh-
PopQA, where the proportion of incorrect answers
                                                         old (set at 0.4 for this experiment), we then com-
exceeds that of correct ones, and the influence of
                                                         pute the Self-BLEU scores for all possible combi-
misleading answers persisted over time. However,
                                                         nations of 4 documents and select the minimum
the BM25 algorithm exhibits relatively higher ro-
                                                         value among them. This minimum value indicates
bustness, and the EMllm of incorrect answers out-
                                                         the maximum individual document contribution
put by the RAG system based on it remains lower
                                                         to the Self-BLEU score not included in the calcu-
than the other three retrieval methods. The exper-
                                                         lation. Subsequently, we exclude the document
imental results of this section reveal that despite
the presence of self-correcting mechanisms, the            6
                                                             https://github.com/Hello-SimpleAI/
injection of specific misleading information can         chatgpt-comparison-detection
Figure 14: The average EMllm scores of the correct and incorrect answers of the RAG system in the simulation
across datasets and LLMs.




        (a) NQ                     (b) WebQ                 (c) TriviaQA                      (d) PopQA
                 Figure 15: Average long-term retrieval performance of different filtering strategies.




        (a) NQ                     (b) WebQ                  (c) TriviaQA                      (d) PopQA
                   Figure 16: Average long-term QA performance of different filtering strategies.
contributing the most to the Self-BLEU score and         portion of human-generated content continues to
incorporate the next ranked document into the com-       exhibit a declining trend. Figure 18 and Figure 19
bination, repeating this filtering process until the     demonstrate that compared to the absence of filter-
combination’s Self-BLEU score meets the preset           ing strategies, both filtering methods slow down
threshold criteria.                                      the polarization speed of top document accuracy
                                                         in retrieval performance. Overall, we discovered
    Analysis of Experimental Results: From the           that filtering based on the source of documents and
experimental results, we can observe that: 1) Both       their diversity can, to some extent, slow down the
Approaches Yield more Stable Retrieval Out-              emergence of the “Spiral of Silence” phenomenon.
comes; however, the Source Filtering Method              Source-based filtering has a more pronounced ef-
Incurs a Performance Cost: Figure 15 and Fig-            fect in terms of preserving the proportion of human-
ure 16 illustrate the variations in the average          generated texts and mitigating viewpoint polariza-
retrieval outcomes and QA performance across             tion; however, this benefit comes at the expense of
datasets, before and after the application of two        the performance of the RAG system. Text filtering
distinct filtering strategies, compared to an unfil-     based on diversity shows superior performance in
tered condition. Observations indicate that by im-       maintaining RAG system functionality, but it has
plementing source-based and diversity-based fil-         a weaker impact on preserving the ratio of human
tering methods, the fluctuation range of the top 5       texts and alleviating viewpoint polarization. De-
retrieval results is reduced compared to the non-        spite these findings, neither method can completely
intervention scenario, suggesting that the filter-       eradicate the “Spiral of Silence” effect, indicating
ing mechanisms can bring a more stable retrieval         the imperative to explore additional solutions. For
performance for RAG systems. Across the four             example, there is a need to investigate retrieval
datasets, the retrieval performance following SELF-      models that can effectively balance between LLM-
BLEU value filtering generally surpasses the un-         generated documents and human-generated docu-
filtered condition; conversely, the source-based fil-    ments to address this issue.
tering strategy results in an overall performance
degradation. This could be attributed to the discrim-    A.9   Prompts
inating model erroneously excluding valid human-         The prompts used in the experiment are shown in
generated texts while aiming to eliminate those          Table 10.
generated by LLMs. Moreover, in QA tasks, di-
versity filtering either enhances or maintains QA
performance, whereas source-based document fil-
tering leads to a decline in QA performance across
all datasets. For instance, on the TriviaQA dataset,
the average EM score drops by over 14%. 2) Both
Methods can only Alleviate the “Spiral of Si-
lence” Phenomenon to Varying Degrees but Can-
not Eliminate it: Figure 17 displays the proportion
of documents from different sources within the top
5 retrieval results in each iteration under three fil-
tering setups on the NQ dataset. It is observable
that without any filtering strategy, human-generated
texts rapidly vanish from the top 5 documents in the
initial iterations. The SELF-BLEU value filtering
method retains human-generated texts to a small
extent; source filtering, on the other hand, maxi-
mally filters out LLM-generated texts, especially
those produced by GPT-3.5-Turbo, Qwen, and
ChatGLM3, with over 30% of human-generated
texts remaining in the top 5 by the end of the tenth
iteration. However, despite both filtering strategies
slowing the disappearance of human texts, the pro-
           (a) None                     (b) Content Filtering                      (c) Source Filtering
Figure 17: Average percentage of texts from various sources within the top 5 search results over multiple iterations
on NQ when using different filtering strategies across different search methods.




Figure 18: Correlation between the number of top 5 search results containing the correct answer ("Context Right
Num") and the accuracy of responses given by LLMs on the NQ dataset when using Content Filtering. The
responses are categorized based on Exact Match (EM) score: EM=1 for correct and EM=0 for incorrect. The overall
number of queries that the LLMs answered correctly (EM=1 Total) and incorrectly (EM=0 Total), along with the
average retrieval accuracy (Acc@5) are shown by dashed lines. The results are averaged across different LLMs,
retrieval, and ranking methods.




Figure 19: Correlation between the number of top 5 search results containing the correct answer (“Context Right
Num”) and the accuracy of responses given by LLMs on the NQ dataset when using Source Filtering. The
responses are categorized based on Exact Match (EM) score: EM=1 for correct and EM=0 for incorrect. The overall
number of queries that the LLMs answered correctly (EM=1 Total) and incorrectly (EM=0 Total), along with the
average retrieval accuracy (Acc@5) are shown by dashed lines. The results are averaged across different LLMs,
retrieval and ranking methods.
Task                       Prompts
Zero-Shot Generation       Provide a background document in 100 words
                           according to your knowledge from Wikipedia to
                           answer the given question.

                           Question:{question_str}

                           Background Document:
Generation with Contexts   Context information is below.
                           --------------
                           [Context 1]:{context_str1}
                           ...
                           [Context 5]:{context_str5}
                           --------------
                           Using both the context information and also
                           using your own knowledge, answer the following
                           question with a background document in 100
                           words.

                           Question:{question_str}

                           Background Document:
Mis_Answer Generation      Generate a false answer to the given question.
                           It should be short (less than ten words in
                           general) and look plausible, compared to the
                           reference answer.

                           Question:{question_str}

                           Reference Answers:{ref_answer_str},

                           False answer:
Mis_Passage Generation     Suppose you are generating realistic-looking
                           claims for a quiz contest. You need to generate
                           a background document less than 100 words in
                           support of the answer to the given question.
                           Don’t contain any word in the original answers
                           in {ref_answer_str}. The background document
                           must contain the following given answers with
                           their original form.

                           Question:{question_str}

                           Answers:{false_answer_str},

                           Background document:
Answer Check               Does the following response support the answer
                           to the question?
                           Question: {question_str}
                           Response: {response_str}
                           Answer: {ref_answer_str} / {false_answer_str}
                           Just answer ’yes’ or ’no’.

                             Table 10: Prompts for different tasks.
