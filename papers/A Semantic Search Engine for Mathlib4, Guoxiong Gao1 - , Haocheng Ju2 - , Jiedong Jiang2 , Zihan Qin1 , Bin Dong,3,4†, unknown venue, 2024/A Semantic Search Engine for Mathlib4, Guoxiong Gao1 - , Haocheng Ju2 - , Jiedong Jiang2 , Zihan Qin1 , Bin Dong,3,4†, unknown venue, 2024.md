                                                                           A Semantic Search Engine for Mathlib4
                                                         Guoxiong Gao1 * , Haocheng Ju2 * , Jiedong Jiang2 , Zihan Qin1 , Bin Dong,3,4†
                                                               1
                                                           School of Mathematical Sciences, Peking University, Beijing, China
                                            2
                                                Beijing International Center for Mathematical Research, Peking University, Beijing, China
                                                                 3
                                                                   Beijing International Center for Mathematical Research
                                                     and the New Cornerstone Science Laboratory, Peking University, Beijing, China
                                                       4
                                                         Center for Machine Learning Research, Peking University, Beijing, China
                                                                      samggx@stu.pku.edu.cn hcju@pku.edu.cn
                                                       {emailboxofjjd,15261375660}@163.com dongbin@math.pku.edu.cn
                                                                Abstract                         the limitations of officially provided search tools,
                                                                                                              which struggle to find relevant theorems with infor-
                                                    The interactive theorem prover Lean enables
                                                    the verification of formal mathematical proofs
                                                                                                              mal queries.
                                                    and is backed by an expanding community.                     There are primarily two methods to search for
arXiv:2403.13310v2 [cs.IR] 4 Feb 2025




                                                    Central to this ecosystem is its mathematical             theorems in mathlib4: using the mathlib4 docu-
                                                    library, mathlib4, which lays the groundwork              mentation3 and searching the GitHub repository
                                                    for the formalization of an expanding range               of mathlib44 . The mathlib4 documentation allows
                                                    of mathematical theories. However, searching              users to search for theorems by their formal names.
                                                    for theorems in mathlib4 can be challenging.
                                                                                                              However, this feature can be challenging for be-
                                                    To successfully search in mathlib4, users often
                                                    need to be familiar with its naming conventions
                                                                                                              ginners to utilize effectively, as they may not be
                                                    or documentation strings. Therefore, creating             familiar with the naming conventions. For exam-
                                                    a semantic search engine that can be used eas-            ple, Cauchy’s Mean Value Theorem is named as
                                                    ily by individuals with varying familiarity with          exists_ratio_deriv_eq_ratio_slope in math-
                                                    mathlib4 is very important. In this paper, we             lib4, meaning a direct search for "Cauchy’s Mean
                                                    present a semantic search engine1 for mathlib4            Value Theorem" yields no results. An alterna-
                                                    that accepts informal queries and finds the rele-         tive method involves searching within the GitHub
                                                    vant theorems. We also establish a benchmark
                                                                                                              repository of mathlib4, which allows for keyword-
                                                    for assessing the performance of various search
                                                    engines for mathlib4.2                                    based searches across the source files, including for-
                                                                                                              mal statements, proofs, and documentation strings.
                                        1           Introduction                                              This method can locate Cauchy’s Mean Value
                                                                                                              Theorem as it is mentioned in the documentation
                                        Lean (de Moura et al., 2015; de Moura and Ull-
                                                                                                              string of exists_ratio_deriv_eq_ratio_slope.
                                        rich, 2021) is an interactive theorem prover built
                                                                                                              However, this approach faces two issues: many the-
                                        on dependent type theory, designed to verify math-
                                                                                                              orems in mathlib4 lack documentation strings, and
                                        ematical proofs written in a formal language and
                                                                                                              semantically similar user queries that don’t exactly
                                        thereby enhancing their rigor. It has a vibrant and
                                                                                                              match the theorems or documentation strings may
                                        supportive community, with its popularity growing
                                                                                                              lead to unsuccessful searches.
                                        among mathematicians. A prime example of the
                                                                                                                 Consequently, neither method adequately sup-
                                        Lean community’s collaborative spirit is mathlib4,
                                                                                                              ports finding theorems based on informal queries,
                                        the mathematical library for Lean 4. This library,
                                                                                                              leading to beginners spending significant time on
                                        regularly updated by contributors from around the
                                                                                                              this task. Discussions on Zulip5 have highlighted
                                        globe, acts as a basis for the formalization of new
                                                                                                              the need for creating a semantic search engine for
                                        mathematical theories. This eliminates the need to
                                                                                                              mathlib4. Therefore, developing such a search en-
                                        repeatedly formalize established results, as users
                                                                                                              gine for mathlib4 is highly desirable to improve the
                                        can simply check if mathlib4 contains the necessary
                                                                                                              efficiency of theorem retrieval.
                                        theorems referenced in informal proofs. However,
                                        locating these theorems is often challenging due to                      In this paper, we introduce a semantic search
                                                * These authors contributed equally.                             3
                                                                                                                   https://leanprover-community.github.io/mathlib4_docs/
                                                †                                                                4
                                              Corresponding author                                                 https://github.com/leanprover-community/mathlib4
                                            1                                                                    5
                                              The search engine is available at https://leansearch.net.            https://leanprover.zulipchat.com/#narrow/stream/219941-
                                            2
                                              The data and the source code are available at                   Machine-Learning-for-Theorem-
                                        https://github.com/reaslab/LeanSearch.                                Proving/topic/Semantic.20Search.20for.20Mathematics


                                                                                                          1
engine for mathlib4 that allows users to input an in-       tors. Training paradigms have also evolved, with
formal query and retrieve a list of relevant theorems       the Inverse Close Task (ICT) (Lee et al., 2019)
from mathlib4. To construct this search engine, we          initially proposed for dense retriever pre-training.
translate the formal statements of mathlib4 theo-           Subsequently, other pre-training tasks have been de-
rems into informal ones and integrate these pairs           veloped, including Body First Selection and Wiki
into a database. Each database entry consists of a          Link Prediction, both introduced in (Chang et al.,
formal theorem statement and its informal version.          2020). Recent studies (Neelakantan et al., 2022;
Upon receiving a user query, we augment the query           Wang et al., 2022; Su et al., 2023; Xiao et al.,
for improved context understanding and perform              2023) have explored large-scale unsupervised pre-
semantic search across the database to find rele-           training using contrastive loss, followed by fine-
vant results. Additionally, we have established a           tuning on smaller, labeled datasets. Pre-training
benchmark to compare the effectiveness of various           with extensive text pairs allows the language model
search engines for mathlib4.                                to grasp textual semantics and the fine-tuning stage
   The remaining part of the paper is organized             further enhances its performance across various
as follows. In Section 2, we review the related             retrieval tasks. However, the authors of (Wang
works on text retrieval and mathematical informa-           et al., 2024) argue that a two-stage training ap-
tion retrieval. Section 3 describes our approach to         proach might not be necessary, demonstrating that
developing a semantic search engine for mathlib4.           directly fine-tuning a decoder-only model on both
Section 4 presents the mathlib4 semantic search             synthetic and labeled data can yield competitive
benchmark. Numerical results are discussed in Sec-          results.
tion 5. We conclude this paper in Section 6.
                                                               Mathematical Information Retrieval. Math-
2   Related Work                                            ematical Information Retrieval (MIR) differs from
                                                            text retrieval in that it involves queries and docu-
   Text Retrieval. Text retrieval is the task of            ments that contain mathematical formulas. These
finding relevant information within a corpus based          formulas are highly structured, which distinguishes
on user queries. Early methods, such as BM25                them from plain text. To effectively capture the se-
(Robertson et al., 1995; Robertson and Zaragoza,            mantics of math formulas, several representations
2009), used sparse vector representations for               are employed. The Symbol Layout Tree (SLT)
queries and documents, assessing relevance by               (Zanibbi and Blostein, 2012) preserves the original
comparing these vectors with certain weighting              layout of formulas, while the Operator Tree (OPT)
techniques (Salton and Buckley, 1988). While ef-            (Gao et al., 2016) represents mathematical symbols
fective in measuring lexical similarity, these ap-          as nodes, with edges denoting the relationships be-
proaches fall short in capturing the semantic simi-         tween operators and operands. Classical MIR meth-
larity between queries and documents.                       ods (Fraser et al., 2018; Gao et al., 2016; Kristianto
   To address this limitation, deep learning tech-          et al., 2016; Zanibbi et al., 2016; Kane et al., 2022;
niques (Huang et al., 2013; Xiong et al., 2017;             Ng et al., 2021, 2020) rely on structure search,
McDonald et al., 2018; Liu et al., 2018) have               identifying matching substructures across various
been introduced. Utilizing deep neural networks,            features. Among these, the Approach0 structural
these techniques encode queries and documents               search method (Zhong and Zanibbi, 2019; Zhong
into dense vectors, thereby assessing relevance             et al., 2020) has shown to be particularly effec-
based on semantic similarity. Further developments          tive. It indexes formulas through leaf-root paths
have been made in neural architectures and training         in the OPT and utilizes subexpression matching
paradigms. There are two main architectures: the            to assess formula similarity. With advancements
cross-encoder (Qiao et al., 2019; Nogueira et al.,          in deep learning, dense retrievers have been inte-
2020) and the bi-encoder (Karpukhin et al., 2020;           grated into MIR, often combined with structural
Qu et al., 2021; Ni et al., 2022b,a). Cross-encoders        searches (Kane et al., 2022; Zhong et al., 2022a,b,
take the concatenation of query and document as             2023). A notable example is the Approach0 hybrid
input and produce the final relevance of this query-        search (Zhong et al., 2022a), which combines Ap-
document pair, while bi-encoders map the query              proach0 structure search with a bi-encoder dense
and document into vectors separately, determining           retriever, ColBERT (Khattab and Zaharia, 2020).
relevance through similarity between the two vec-           This combination not only facilitates effective for-

                                                        2
mula matching but also enhances understanding of                     theorem
                                                                     orderOf_dvd_nat_card
                                                                                                                                   Order-Divides-
                                                                                                                                   Cardinality Theorem: The
                                                                     {G : Type u_6} [Group G]                                      order of an element in a
context.                                                             {x : G} : orderOf x ∣
                                                                     Nat.card G
                                                                                                   Mathlib4
                                                                                                    Formal          informalizer
                                                                                                                                   group divides the
                                                                                                                                   cardinality of the group.
                                                                                                                                                                Informalized
                                                                                                                                                                  Mathlib4
                                                                                                  Statements                                                     Statements
   The preceding literature focuses on extracting                     …                                                             …

mathematical content from a corpus composed of
natural language texts and formulas formatted in
markup languages. This contrasts with our objec-
tive of conducting searches within mathlib4, a for-                   Query
                                                                                                   Query
                                                                      Order of an element                                                   Search Engine
mal mathematical library. The work most closely                       divides the order
                                                                      of the group
                                                                                                Augmentation


related to ours is Moogle6 , a semantic search en-
gine for mathlib4. However, its technical details
have not been released. We will compare the perfor-
                                                                      Search Results
mance of Moogle and our search engine in Section                      1. Order-Divides-Cardinality Theorem: The order of an element in a group divides the cardinality of the
                                                                         group.

5.                                                                    2. Order-Divides-Cardinality Theorem: The order of an element in a finite group divides the cardinality
                                                                         of the group.
                                                                      3. Order of Element Divides Cardinality Theorem: For any element x in an additive group G, the order of x
                                                                         divides the cardinality of G.
                                                                      …

3       Methodology
                                                                    Figure 1: Overview of our method for creating a se-
In this section, we will describe the implementation                mantic search engine for mathlib4. We employ an in-
of our semantic search engine for mathlib47 . This                  formalizer to convert formal statements from mathlib4
engine is designed to accept a user query in natural                into their informal counterparts. These informal-formal
language and return a list of relevant theorems in                  pairs are then stored in a vector database. When users in-
mathlib4. Our approach involves converting formal                   put a query, the system augments the query and searches
theorems from mathlib4 into their informal coun-                    across the database, yielding a list of relevant theorems.
terparts, as illustrated in Figure 1. These informal-
formal theorem pairs are then vectorized and stored
                                                                    ate informal theorem names and statements. These
in a vector database, a step that can be executed
                                                                    are subsequently formatted as "theorem name: in-
offline. When a user query is submitted, we aug-
                                                                    formal statement" and incorporated into an infor-
ment the query to better grasp its context, vectorize
                                                                    mal corpus. Figure 3 shows the prompt used for in-
the enriched query, and locate the corresponding
                                                                    formalizing the theorem Exists.choose_spec, in-
theorems in the embedding space. In the following
                                                                    cluding the formal statement, documentation string,
subsections, we will elaborate on the informaliza-
                                                                    and the definition of Exists.choose as annota-
tion of mathlib4, the design of the search engine,
                                                                    tions to aid the LLM’s understanding.
and the method of query augmentation.
                                                                       Notably, the authors of (Jiang et al., 2023) also
3.1      Informalizing Mathlib4                                     employed an LLM for informalizing mathlib4 state-
Our strategy for informalizing mathlib4 involves                    ments, relying solely on the formal statements. We
employing a large language model (LLM). Central                     argue that providing the LLM with additional con-
to this strategy is providing the LLM with sufficient               text, such as related definitions and documentation
context to accurately grasp the formal theorem’s                    strings, enhances its ability to accurately interpret
exact meaning. To this end, we not only extract                     and convert formal theorems into their informal
the theorem’s name, statement, and documentation                    counterparts. An example comparing the informal-
string8 from the mathlib4 documentation but also                    ized mathlib4 statement generated by (Jiang et al.,
include related definitions found in the theorem                    2023) to the one produced by our method is pro-
statements through hyperlinks. For example, as                      vided in Appendix A.
illustrated in Figure 2, we extract the definition of
                                                                    3.2        Semantic Search Engine for Mathlib4
Exists.choose because it is referenced and linked
in the theorem Exists.choose_spec. The gath-                        After obtaining the informal corpus, we employ
ered information is then fed into an LLM9 to gener-                 dense embedding models, which excel at captur-
    6                                                               ing semantic information, to encode the informal-
      https://www.moogle.ai/
    7
      We        use        mathlib4        with      commit         formal theorem pairs. Recent advancements in text
db04a978b67b2200691f0bd968f334c83261b66a.                           embedding models have introduced the practice
    8
      For many theorems in mathlib4 that lack a documentation       of integrating specific task instructions into either
string, we will extract only the theorem name and statement.
    9
      We use gpt-3.5-turbo-16k for generating informal              queries or documents, enhancing the model’s adapt-
names and statements, setting the temperature to 0.                 ability to diverse tasks and boosting performance in

                                                                3
                              theorem name & statement
                                                                                                         Input:
                              theorem Exists.choose_spec {α : Sort u_1}
                              {p : α → Prop} (P : ∃ a, p a) : p                                          System message: As a mathematician and expert in Lean and Mathlib, your task is to translate the formal theorem
                              (Exists.choose P)                                                          provided below into an informal statement that is more accessible to mathematicians. Please utilize the provided
                                                                                                         doc string and annotations to better understand the formal theorem. Additionally, please express the
                                                                                                         mathematical formulas in LaTeX when necessary.
                                                                                                         Formal theorem:
 Annotations                                                                                             theorem Exists.choose_spec {α : Sort u_1} {p : α → Prop} (P : ∃ a, p a) : p
                                                         Doc String                                      (Exists.choose P)
 noncomputable def Exists.choose {α :                                                                    Doc string:
 Sort u_1} {p : α → Prop} (P : ∃ a, p a) :               Show that an element extracted from P :         Show that an element extracted from P : ∃ a, p a using P.choose satisfies p.
 α                                                       ∃ a, p a using P.choose satisfies p.            Annotations:
 Extract an element from a existential
                                                                                                         noncomputable def Exists.choose {α : Sort u_1} {p : α → Prop} (P : ∃ a, p a) : α
 statement, using Classical.choose.
                                                                                                         Extract an element from a existential statement, using Classical.choose.



                                                                                                         Output:
                                             GPT-3.5                                                     Theorem name: Existential Element Chosen by Choose Function
                    Theorem name: Existential Element Chosen by Choose Function                          Informal statement: For any property p on a set α, if there exists an element a such that p(a) is true, then the
                    Informal statement: For any property p on a set α, if there                          element chosen from the existential statement using the choose function also satisfies p.
                    exists an element a such that p(a) is true, then the element
                    chosen from the existential statement using the choose
                    function also satisfies p.




                      Existential Element Chosen by Choose Function: For any
                      property p on a set α, if there exists an element a such
                                                                                                       Figure 3: Prompt for informalizing mathlib4 statements
                                                                                      Informal
                      that p(a) is true, then the element chosen from the
                      existential statement using the choose function also             Corpus          with documentation strings.
                      satisfies p.




Figure 2: Our approach to informalizing mathlib4 the-                                                  an efficient approximate nearest neighbor search
orems. We extract the theorem name, statement, and                                                     method, ensuring rapid retrieval from the corpus.
documentation string from the mathlib4 documentation.
Moreover, we collect related definitions via the hyper-                                                3.3       Query Augmentation
links in the theorem statements. The gathered informa-                                                 To enhance query clarity and achieve a more accu-
tion is then inputted into GPT-3.5 to generate informal                                                rate embedding, our system incorporates a query
names and statements. These are then organized in the
                                                                                                       augmentation step. This process involves prompt-
format "theorem name: informal statement" and added
to an informal corpus.                                                                                 ing an LLM10 to transform a brief, vague query
                                                                                                       into a detailed statement that includes both infor-
                                                                                                       mal and formal statements, ensuring mathematical
zero-shot settings (Su et al., 2023; Li and Li, 2023;                                                  equivalence with the original query. We guide the
Wang et al., 2024). Consequently, for the purpose                                                      LLM with specific principles for query augmenta-
of theorem retrieval within mathlib4, we enrich our                                                    tion, emphasizing the importance of precision, the
corpus documents with specific instructions. We                                                        use of LaTeX for mathematical expressions, and
adopt the following instruction template:                                                              the clarification of ambiguous inputs. Additionally,
                                                                                                       we provide examples of query augmentations to
Instruct: Retrieve math theorems stated
                                                                                                       improve the LLM’s comprehension of the task. A
 in bilingual Lean 4 + natural language
                                                                                                       detailed prompt for query augmentation is provided
 that are mathematically equivalent to
                                                                                                       in Appendix B. Although Lean 4 code generation
     the given one \n Doc:{document}
                                                                                                       by LLMs may occasionally introduce inaccuracies
Here, {document} denotes                                                                               due to the limited presence of mathlib4 in their
                                                                                                       training data, this approach effectively enriches the
        "{formal statement} \n {informal
                                                                                                       query with additional contextual information.
          name}:{informal statement}".
                                                                                                          Following augmentation, the enriched query
   These task-specific instructions significantly in-                                                  is structured as "{formal statement} \n
fluence the performance of embedding models. We                                                        {informal name}:{informal statement}",
will investigate the effect of varying task instruc-                                                   matching the structure of our database. In a similar
tions on the overall retrieval performance in Ap-                                                      manner to adding task instructions in document
pendix D.                                                                                              processing, we enrich the query with specific in-
   Embedding the entire corpus, although a time-                                                       structions, utilizing a template as follows:
consuming process, is performed offline and does                                                        Instruct: Retrieve math theorems stated
not require repetition for each use of the engine. We                                                   in bilingual Lean 4 + natural language
utilize Chroma DB to store the embeddings. Upon                                                          that are mathematically equivalent to
receiving a query, our system vectorizes it and re-                                                    the given one \n Query:{formal statement}
trieves theorems based on their cosine distance to                                                     \n {informal name}:{informal statement}"
the query in the embedding space. Chroma DB
                                                                                                       This formatted query is then vectorized and utilized
employs the Hierarchical Navigable Small World
(HNSW) algorithm (Malkov and Yashunin, 2020),                                                            10
                                                                                                              We use gpt-4-0125-preview for query augmentation.


                                                                                                   4
                                                               Category      Count   Example 1                               Example 2
by the search engine to retrieve theorems based on                                   If there exist injective maps of sets
                                                                Natural              from A to B and from B to A, then       If p implies q, then not
the cosine distance in the embedding space.                    Description
                                                                              18
                                                                                     there exists a bijective map between    q implies not p.
                                                                                     A and B.
                                                                                     If there exist f : A → B injective,
                                                                 LaTeX                                                       (p → q) → (¬q →
                                                                                     g : B → A injective, then there
4     Mathlib4 Semantic Search Benchmark                        Formula
                                                                              15
                                                                                     exists h : A → B bijective.
                                                                                                                             ¬p)
                                                                Theorem
                                                                               7     Schroeder Bernstein Theorem             Modus Tollens
                                                                 Name
To rigorously assess and compare the efficacy of                 Lean 4
                                                                                     {f : A → B} {g : B → A} (hf :
                                                                                                                   (p → q) → (¬q →
                                                                              10     Injective f) (hg : Injective
various retrieval methods, we have established the                Term                                             ¬p)
                                                                                     g) : ∃ h, Bijective h
Mathlib4 Semantic Search Benchmark. This bench-
mark encompasses a curated set of queries, rele-              Table 1: Statistics and examples of query groups in our
                                                              benchmark.
vance labels of each mathlib4 theorem for these
queries, and a collection of performance metrics.
In this section, we provide a detailed explanation            4.2     Relevance Judgments
of the benchmark. Section 4.1 describes the com-
                                                              During the process of collecting relevance labels
position of the query set. In Section 4.2, we explain
                                                              for query-document pairs, we adopt an approach
the relevance criteria for our benchmark and the la-
                                                              similar to ARQMath(Mansouri et al., 2022). Ini-
beling procedure. Section 4.3 lists the performance
                                                              tially, we establish a carefully crafted relevance
metrics used in our benchmark.
                                                              assessment criteria, elaborated in Table 2. While
                                                              performing the labeling, assessors are instructed to
4.1    Composition of the Query Set                           evaluate whether a given search result facilitates
The query set of our benchmark has 50 distinct                their mathematical formalization workflow. Instead
queries, spanning various mathematical disciplines            of merely considering similarity in topic, presented
including calculus, abstract algebra, linear algebra,         form, formula structure, or mathematical induc-
number theory, algebraic number theory, set theory,           tion relationship, the relevance we focus on here is
and mathematical logic. This selection aims to                deeply aligned with the needs of Lean 4 experts.
cover a broad spectrum of topics and complexities.               Rating      Label   Score    Definition
We argue that this is a typical size for the query sets        Exact Match     2       1
                                                                                              Exact match to the query or being a stronger
                                                                                              statement
in mathematical information retrieval datasets, as              Relevant       1      0.3
                                                                                              Useful in locating where the corresponding
                                                                                              statement should be
demonstrated by the ARQMath1, ARQMath2, and                     Irrelevant     0       0
                                                                                              Not expected to be useful in mathematics
                                                                                              formalization workflow
ARQMath3 databases from the MIR field, which
contain 77, 71, and 78 queries, respectively, for             Table 2: The relevance assessment criteria for our bench-
their answer retrieval tasks (Mansouri et al., 2022).         mark.
   To optimize labeling efforts, we organize queries
with identical search intents into 18 distinct, non-             For each set of queries grouped by identical
overlapping groups, each containing at least two              search intentions, assessors are presented with the
distinct queries. This approach assumes that all              top 50 theorems retrieved by an intermediate ver-
queries within a group have the same relevance                sion of our search engine. In addition to evaluating
score for any document, significantly reducing the            the provided theorems, assessors are tasked with
need for repetitive labeling, as each document is             identifying and adding any relevant theorems that
evaluated only once per query group. Furthermore,             may have been omitted from the initial list by in-
to provide a more detailed assessment and mitigate            specting the files where "Exact Match" items in the
the impact of duplicate document labels, we con-              list are located, with particular attention to those
sider four prevalent forms of mathematical queries:           with "Exact Match" rating.
natural language descriptions, LaTeX formulas,                   Given the structured organization of mathlib4,
theorem names, and Lean 4 term descriptions. In               where related theorems are often located within
each query group, we strive to include as many                the same file, it is reasonable to assume that any
different description forms as possible. Table 1              items not in the list are irrelevant to this query
provides statistics and examples of the query set.            group. Additionally, all queries are guaranteed to
However, not all query groups contain all four rep-           have at least one exact match in mathlib4. These
resentation forms, as some theorems may not have              assumptions support the performance metrics we
an official name or their representation in a LaTeX           use in the benchmark, as described in the following
formula might be redundant.                                   subsection.

                                                          5
4.3   Performance Measures                                 5     Experiments
To compare different retrieval paradigms’ perfor-          In this section, we evaluate the performance of
mance on our labeled dataset, three commonly               various theorem retrieval methods using our bench-
used metrics are adopted in our benchmark. Preci-          mark. The experimental setup is detailed in Section
sion@k calculates the average relevant document            5.1. We compare the performances of different re-
proportion in top-k retrieved results among the            trieval methods in Section 5.2. Additionally, the
query set Q:                                               ablation study on document preparations and query
                               |Q|
                                                           augmentations is presented in Section 5.3.
                                      k
                      1 XX
      Precision@k =        I(i, dji ),           (1)       5.1    Experiment Setup
                    k|Q|
                               i=1 j=1
                                                           We have considered four embedding models in
where di represents the list of retrieved theorems         our experiments: text-embedding-ada-002 and
for the i-th query, and I(i, dji ) = 1 if and only         text-embedding-3-large from OpenAI, UAE-Large-
if the j-th retrieved result of i-th query is "Exact       V1(Li and Li, 2023), and E5mistral-7b (Wang et al.,
Match", otherwise I(i, dji ) = 0. Assuming that            2024). For the baseline methods, we compare
all unlabeled theorems are irrelevant, we can also         BM25 (Robertson and Zaragoza, 2009), Moogle,
calculate Recall@k:                                        and the four embedding models applied to the orig-
                                                           inal Lean 4 formal corpus and unaugmented query.
                         |Q|          k
                  1 X 1 X                                  The same four embedding models equipped with
      Recall@k =          I(i, dji ),            (2)
                 |Q|  σi                                   formal + informal query augmentation and formal
                         i=1         j=1
                                                           + informal document corpus are also tested on our
   where σi is the number of "Exact Match" theo-           benchmark to demonstrate the efficacy of our ap-
rems for i-th query.                                       proach. The implementation details are provided
   The third metric, nDCG (normalized Discounted           in Appendix C.
Cumulative Gain), incorporates the position of the
                                                           5.2    Main Results
retrieved result. A decaying weight is allocated to
each position:                                             Table 3 and 4 present the results of BM25,
                                                           Moogle, and four embedding models. The model
                       k
                       X        s(i, dji )                 E5mistral-7b , when integrated with our retrieval
          DCGi @k =                        ,     (3)       pipeline, achieves the best performance across
                              log2 (j + 1)
                        j=1                                three overall metrics and significantly outperforms
                                                           all other methods, including its own performance
   where s(i, dji ) represents the score of the j-th       on a formal corpus with unaugmented queries. We
retrieved theorem for the i-th query, as defined in        observe that all retrieval methods benefit from us-
Table 2. Our scoring system is not proportional            ing an augmented corpus and queries, as augmen-
to the label number, emphasizing the importance            tation expands concrete mathematics and Lean 4
of exact matching in the mathlib4 retrieval task.          terms, and these embedding models typically per-
We further define IDCGi @k as the highest possi-           form better on symmetrical retrieval tasks (Wang
ble DCGi @k by properly arranging the retrieved            et al., 2024).
theorems, and finally:                                        Examining the results averaged by category, we
                              |Q|
                                                           find that E5mistral-7b attains the best results in nearly
                   1 X DCGi @k                             all categories, with the exception of nDCG@20
         nDCG@k =                                (4)
                  |Q|  IDCGi @k                            for Lean 4 Terms. This exception is likely due to
                              i=1
                                                           the augmented informal information negatively im-
   To sum up, nDCG@k measures both the retrieval           pacting retrieval performance, as it is not essential
and ranking ability of the given engine in a uni-          in formal-formal retrieval (formal queries, formal
fied and detailed way. Meanwhile, P@10 (Preci-             results) which focuses on lexical matches. Notably,
sion@10) and R@10 (Recall@10) focus solely on              our method significantly improves performance in
the retrieval effectiveness. In our benchmark, all         the Theorem Name category. The enhancement is
three metrics will be reported for both the entire         due to the expansion of the statement for a given
query set and each query category.                         theorem name by our query augmentation, which

                                                       6
                                                                                                            1.0
is essential for successful retrieval in this category.                                                                                          MIS_formal
                                                                                                                                                 MIS_informal
                                                                                                            0.8                                  MIS_F+IF
Furthermore, the combined corpus of formal and




                                                                                                  NDCG@20
                                                                                                            0.6
informal statements facilitates the retrieval process.                                                      0.4

                                                                                                            0.2
 Model              Corpus         Query aug.          nDCG@20         P@10         R@10
                                                                                                            0.0
                                     Baselines




                                                                                                                              ap
                                                                                                                   tiv t




                                                                                                                     lu d




                                                                                                                  ify ee


                                                                                                                syl local
                                                                                                       Sc s_ex ant


                                                                                                                              us




                                                                                                                 d sum


                                                                                                                ite m
                                                                                                     int gro main

                                                                                                                   bs r




                                                                                                                  ly_ 3
                                                                                                                du ion

                                                                                                                               s
                                                                                                                 ass on




                                                                                                                 ati st




                                                                                                                   rin tia


                                                                                                                tra third
                                                                                                               ec se




                                                                                                              _su rde


                                                                                                                            en
                                                                                                             en _gc




                                                                                                               po pi_
                                                                                                              riv xi




                                                                                                            fin e_sy
                                                                                                                          ha




                                                                                                            ram gr




                                                                                                                        _sw
                                                                                                            r_Z nsi




                                                                                                                           er
                                                                                                           bij ZFC_




                                                                                                           mo titut
                                                                                                           loi in




                                                                                                          de e_e




                                                                                                                        oll
                                                                                                          ral _o
                                                                                                                         _




                                                                                                                         e
                                                                                                         eig ivide




                                                                                                                      _in
                                                                                                                       g_

                                                                                                                         _
                                                                                                                      en




                                                                                                                    _do
                                                                                                         Ga term




                                                                                                                      ve
                                                                                                         hu te




                                                                                                                    ow
                                                                                                                       d
                                                                                                                    s_t




                                                                                                                     ce
                                                                                                        eg up
 Moogle†                                                0.365†         0.092†       0.513†




                                                                                                                 va
                         \                \




                                                                                                             _de
                                                                                                          2d
 BM25                    F                \             0.024          0.004        0.030
 OpenAI v2               F                \             0.312          0.078        0.405
 OpenAI v3               F                \             0.493          0.128        0.622
 UAE-Large-V1            F                \             0.233          0.066        0.307         Figure 4: nDCG@20 performance of E5mistral-7b across
 E5mistral-7b            F                \             0.593          0.132        0.687         formal, informal and formal + informal corpus on our
                                   Our Methods                                                    benchmark, averaged by query groups. These evalua-
 OpenAI v2              F+IF          F+IF               0.553           0.144      0.707         tions are conducted using non-augmented queries.
 OpenAI v3              F+IF          F+IF               0.691           0.178      0.837
 UAE-Large-V1           F+IF          F+IF               0.368           0.084      0.440
 E5mistral-7b           F+IF          F+IF               0.733           0.196      0.913
                                                                                                  the ablation study on task instructions in provided
Table 3: Results on our benchmark, averaged across                                                in Appendix D.
all queries in our dataset. Here "aug.", F, IF, P@10
and R@10 represent augmentation, formal, informal,                                                5.3.1           Ablation of Document Preparations
Precision@10, and Recall@10, respectively. The terms
                                                                                                  Table 5 presents the effects of changing corpus
OpenAI v2 and v3 refer to the text-embedding mod-
els ada-002 and 3-large, respectively. Moogle† , unlike
                                                                                                  type with and without query augmentation. We
other retrieval systems, not only fetches theorems but                                            use the original Lean 4 statement and its informal-
also definitions, structures, instances, etc., making it                                          ized version to create the formal and informal cor-
incomparable under our performance metrics directly.                                              pus. Without query augmentation, results indicate
For the purpose of this analysis, all non-theorem items                                           that both OpenAI v3 large and E5mistral-7b underper-
retrieved are considered irrelevant, given the explicit                                           form with incomplete corpus components, yielding
theorem-searching intent of our queries. This approach,                                           lower overall scores on all metrics. Specifically, the
however, might advantage our theorem retrieval systems
                                                                                                  formal + informal corpus enhances performance
over Moogle, as non-theorem items occupy potential
slots in the retrieval list. The notation † is used to denote                                     on Lean 4 Terms by incorporating formal data and
this adjustment.                                                                                  improves score on the Natural Description category
                                                                                                  by providing hybrid information. For the Theorem
                                                                                                  Name category, E5mistral-7b significantly benefits
                             nDCG@20                                   P@10
 Model
                 ND          LF      TN        LT        ND       LF        TN        LT
                                                                                                  from the formal + informal corpus by utilizing the
                                      Baselines                                                   unfolded mathematical descriptions provided by
 Moogle†        0.369†    0.324†    0.333†    0.441†    0.083†   0.107†    0.071†    0.100†
 BM25           0.000     0.000     0.000     0.119     0.000    0.000     0.000     0.020
                                                                                                  the informalized statement, whereas OpenAI v3
 OpenAI v2
 OpenAI v3
                0.276
                0.479
                          0.379
                          0.553
                                    0.000
                                    0.235
                                              0.498
                                              0.610
                                                        0.061
                                                        0.122
                                                                 0.107
                                                                 0.160
                                                                           0.000
                                                                           0.057
                                                                                     0.120
                                                                                     0.140
                                                                                                  large shows diminished results, likely due to the
 UAE-Large-V1
 E5mistral-7b
                0.301
                0.576
                          0.216
                          0.633
                                    0.004
                                    0.294
                                              0.298
                                              0.774
                                                        0.078
                                                        0.139
                                                                 0.067
                                                                 0.140
                                                                           0.000
                                                                           0.043
                                                                                     0.090
                                                                                     0.170
                                                                                                  lack of training on mixed-domain texts and absence
                                    Our Methods                                                   of adaptive instructions. We note that the formal
 OpenAI v2
 OpenAI v3
                0.536
                0.681
                          0.533
                          0.657
                                    0.571
                                    0.772
                                              0.600
                                              0.703
                                                        0.111
                                                        0.167
                                                                 0.160
                                                                 0.180
                                                                           0.186
                                                                           0.200
                                                                                     0.150
                                                                                     0.180
                                                                                                  corpus outperforms the formal+informal corpus in
 UAE-Large-V1   0.415     0.337     0.371     0.329     0.100    0.080     0.071     0.070        the Lean 4 Terms category for E5mistral-7b , as ex-
 E5mistral-7b   0.748     0.712     0.855     0.654     0.194    0.200     0.214     0.180
                                                                                                  plained in Section 5.2: retrieval on Lean 4 Terms
Table 4: Results on our benchmark averaged by category.                                           relies heavily on lexical rather than semantic infor-
Here ND, LF, TN and LT stands for Natural Descrip-                                                mation, and the presence of informal information
tion, LaTeX Formula, Theorem Name and Lean 4 Term                                                 negatively impacts retrieval performance. Similar
respectively. Corpus type and query augmentation type                                             results are observed with augmented queries.
remain the same as Table 3 and are omitted here due to
space limitations. † indicates a different performance
                                                                                                     A more detailed examination of the results for
calculation rule, detailed in captions of Table 3.                                                each query group without query augmentation is
                                                                                                  shown in Figure 4. In most instances, the "for-
                                                                                                  mal + informal" configuration avoids the abrupt
5.3      Ablation Studies                                                                         performance decline observed in solely formal or
In this subsection, we perform ablation studies                                                   informal settings. The informalized statement pro-
on document preparation and query augmentation.                                                   vided in the corpus mitigates the lexical mismatch
The results of these studies are presented in Sec-                                                between the query and the formal statement, which
tions 5.3.1 and 5.3.2, respectively. Additionally,                                                justifies our choice of a combined corpus.

                                                                                              7
                                         nDCG@20                   P@10    R@10
 Model & Corpus                                                                        tation. This makes it a cost-effective option for
                           ND       LF      TN      LT      All     All     All
                           without query augmentation
                                                                                       deploying our semantic search engine, as it elimi-
 OpenAI v3 large                                                                       nates the need to prompt an LLM with every query.
 formal corpus             0.479   0.553   0.235   0.610   0.493   0.128   0.622
 informal corpus           0.591   0.527   0.365   0.451   0.512   0.134   0.628
 formal+informal corpus    0.607   0.549   0.267   0.622   0.545   0.140   0.677       6   Conclusion
 E5mistral-7b
                                                   0.774
 formal corpus
 informal corpus
                           0.576
                           0.696
                                   0.633
                                   0.636
                                           0.294
                                           0.616   0.604
                                                           0.593
                                                           0.648
                                                                   0.132
                                                                   0.174
                                                                           0.687
                                                                           0.773
                                                                                       In this paper, we introduce a semantic search en-
 formal+informal corpus    0.749   0.687   0.698   0.612   0.701   0.184   0.845       gine designed to enable users to locate theorems in
                            with query augmentation                                    mathlib4 using informal queries. Specifically, we
 OpenAI v3 large
 formal corpus             0.637   0.617   0.565   0.647   0.623   0.160   0.747       translate the formal statements of mathlib4 theo-
 informal corpus           0.603   0.650   0.810   0.575   0.640   0.166   0.783
 formal+informal corpus    0.681   0.657   0.772   0.703   0.691   0.178   0.837
                                                                                       rems into informal versions and develop our search
 E5mistral-7b                                                                          engine to work with a corpus of informal-formal
 formal corpus             0.688   0.685   0.631   0.694   0.680   0.178   0.847
 informal corpus           0.711   0.646   0.824   0.670   0.699   0.184   0.877
                                                                                       theorem pairs. Additionally, we construct a dataset
 formal+informal corpus    0.748   0.712   0.855   0.654   0.733   0.196   0.913       to facilitate evaluation. Our comprehensive experi-
                                                                                       ments on this dataset reveal that the best theorem
Table 5: Results of ablation studies on document prepa-
ration and query augmentation. "All" indicates the per-                                retrieval performance is attained by augmenting the
formance averaged across the entire query set. In the                                  user’s query appropriately and embedding the con-
query augmentation section, all queries are augmented                                  tent of the corpus simultaneously. Consequently,
to match the corpus type. Here, E5mistral-7b uses different                            our system employs a strategy that first augments
task instructions for the document and query in the non-                               the query, followed by a semantic search, thereby
augmented query setting and the same task instructions                                 precisely aligning with the users’ search intentions.
for both in the query augmentation setting. Detailed
                                                                                          Our future research will focus on three primary
task instructions can be found in Table 6.
                                                                                       directions. First, in terms of informalizing math-
  Query aug. &
                                                                                       lib4, we aim to design guidelines for translation
                    Side     Task Instructions
   Doc Type
                             Given a math search query, retrieve theorems
                                                                                       and provide examples of converting mathlib4 state-
                   Query
                             mathematically equivalent to the query                    ments to informal language for LLMs, enhancing
 None & Informal             Represent the given math theorem statement
                    Doc      for retrieving related statement by natural               the informal corpus’s quality. Second, regarding
                             language query
                             Given a math search query, retrieve theorems              the mathlib4 semantic search benchmark, we plan
                   Query     stated in bilingual Lean 4 + natural language
                             that mathematically match the query                       to continually enlarge the query set, aiming for a
                             Represent the given formal math statement
  None & F+IF
                             written in Lean 4 concatenated with its
                                                                                       more comprehensive benchmark. Lastly, for the se-
                    Doc
                             natural language explanation for retrieving               mantic search engine itself, we intend to fine-tune
                             related statement by natural language query
                   Query
                             Retrieve math theorems stated in Lean 4 that              a text embedding model on the task of theorem
 Formal & Formal             are mathematically equivalent to the given
                   & Doc
                             one                                                       retrieval, aiming to improve the search engine’s
                   Query     Retrieve math theorems that are
     IF & IF
                   & Doc     mathematically equivalent to the given one                performance.

Table 6: Task Instructions for E5mistral-7b in ablation                                7   Limitations
studies, supplementing Table 7. The abbreviation "aug."
denotes augmentation, while "F" and "IF" represent                                     When translating mathlib4 theorems into their in-
formal and informal, respectively.                                                     formal versions, we extract the related definitions
                                                                                       through the hyperlinks in the theorem statements.
                                                                                       This approach to extracting dependencies can some-
5.3.2      Ablation of Query Augmentations                                             times be inaccurate and may omit certain depen-
The effect of query augmentation is evident when                                       dencies. A more precise method is to extract the de-
comparing the results in the upper and lower sec-                                      pendencies of a theorem by interacting with Lean’s
tions of Table 5. As shown, augmented queries                                          language server.
enhance the performance across all compared meth-                                         Another limitation of our work is the use of
ods. Specifically, query augmentation significantly                                    E5mistral-7b , a 7B embedding model, in our search
improves the ability of all methods to identify                                        engine. This model may pose challenges when de-
Theorem Names by expanding terms and provid-                                           ploying the search engine on resource-constrained
ing richer context. Notably, the performance of                                        devices like laptops. In future work, we aim to im-
E5mistral-7b on the formal + informal corpus with-                                     prove the performance of smaller embedding mod-
out query augmentation is comparable to its per-                                       els for theorem retrieval tasks to enable broader
formance on the same corpus with query augmen-                                         accessibility.

                                                                                   8
Acknowledgment                                                 to - 8th, 2022, volume 3180 of CEUR Workshop
                                                               Proceedings, pages 40–62. CEUR-WS.org.
This work is supported in part by the New Corner-
                                                             Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick
stone Investigator Program.
                                                               Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and
                                                               Wen-tau Yih. 2020. Dense Passage Retrieval for
                                                               Open-Domain Question Answering. In Proceedings
References                                                     of the 2020 Conference on Empirical Methods in
                                                               Natural Language Processing (EMNLP), pages 6769–
Wei-Cheng Chang, Felix X. Yu, Yin-Wen Chang, Yim-
                                                               6781, Online. Association for Computational Lin-
  ing Yang, and Sanjiv Kumar. 2020. Pre-training
                                                               guistics.
 Tasks for Embedding-based Large-scale Retrieval.
  In 8th International Conference on Learning Repre-         Omar Khattab and Matei Zaharia. 2020. ColBERT:
  sentations, ICLR 2020, Addis Ababa, Ethiopia, April         Efficient and Effective Passage Search via Contextu-
 26-30, 2020. OpenReview.net.                                 alized Late Interaction over BERT. In Proceedings
                                                              of the 43rd International ACM SIGIR Conference on
Leonardo de Moura and Sebastian Ullrich. 2021. The            Research and Development in Information Retrieval,
  Lean 4 Theorem Prover and Programming Language.             SIGIR ’20, page 39–48, New York, NY, USA. Asso-
  In Automated Deduction - CADE 28 - 28th Interna-            ciation for Computing Machinery.
  tional Conference on Automated Deduction, Virtual
  Event, July 12-15, 2021, Proceedings, volume 12699         Giovanni Yoko Kristianto, Goran Topic, and Akiko
  of Lecture Notes in Computer Science, pages 625–             Aizawa. 2016. MCAT Math Retrieval System for
  635. Springer.                                               NTCIR-12 MathIR Task. In Proceedings of the 12th
                                                               NTCIR Conference on Evaluation of Information
Leonardo Mendonça de Moura, Soonho Kong, Jeremy                Access Technologies, National Center of Sciences,
  Avigad, Floris van Doorn, and Jakob von Raumer.              Tokyo, Japan, June 7-10, 2016. National Institute of
  2015. The Lean Theorem Prover (System Descrip-               Informatics (NII).
  tion). In Automated Deduction - CADE-25 - 25th
  International Conference on Automated Deduction,           Kenton Lee, Ming-Wei Chang, and Kristina Toutanova.
  Berlin, Germany, August 1-7, 2015, Proceedings, vol-         2019. Latent Retrieval for Weakly Supervised Open
  ume 9195 of Lecture Notes in Computer Science,               Domain Question Answering. In Proceedings of the
  pages 378–388. Springer.                                     57th Annual Meeting of the Association for Computa-
                                                               tional Linguistics, pages 6086–6096, Florence, Italy.
Dallas Fraser, Andrew Kane, and Frank Wm. Tompa.               Association for Computational Linguistics.
  2018. Choosing Math Features for BM25 Ranking
  with Tangent-L. In Proceedings of the ACM Sympo-           Xianming Li and Jing Li. 2023. AnglE-optimized Text
  sium on Document Engineering 2018, DocEng ’18,               Embeddings. CoRR, abs/2309.12871.
  New York, NY, USA. Association for Computing               Zhenghao Liu, Chenyan Xiong, Maosong Sun, and
  Machinery.                                                   Zhiyuan Liu. 2018. Entity-Duet Neural Ranking:
                                                               Understanding the Role of Knowledge Graph Seman-
Liangcai Gao, Ke Yuan, Yuehan Wang, Zhuoren Jiang,
                                                               tics in Neural Information Retrieval. In Proceedings
  and Zhi Tang. 2016. The Math Retrieval System of
                                                               of the 56th Annual Meeting of the Association for
  ICST for NTCIR-12 MathIR Task. In Proceedings
                                                               Computational Linguistics (Volume 1: Long Papers),
  of the 12th NTCIR Conference on Evaluation of In-
                                                               pages 2395–2405, Melbourne, Australia. Association
  formation Access Technologies, National Center of
                                                               for Computational Linguistics.
  Sciences, Tokyo, Japan, June 7-10, 2016. National
  Institute of Informatics (NII).                            Yury A. Malkov and Dmitry A. Yashunin. 2020. Ef-
                                                               ficient and Robust Approximate Nearest Neighbor
Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng,              Search Using Hierarchical Navigable Small World
  Alex Acero, and Larry Heck. 2013. Learning deep              Graphs. IEEE Trans. Pattern Anal. Mach. Intell.,
  structured semantic models for web search using              42(4):824–836.
  clickthrough data. In Proceedings of the 22nd ACM
  International Conference on Information & Knowl-           Behrooz Mansouri, Vít Novotný, Anurag Agarwal, Dou-
  edge Management, CIKM ’13, page 2333–2338, New               glas W. Oard, and Richard Zanibbi. 2022. Overview
  York, NY, USA. Association for Computing Machin-             of ARQMath-3 (2022): Third CLEF Lab on Answer
  ery.                                                         Retrieval for Questions on Math (Working Notes Ver-
                                                               sion). In Conference and Labs of the Evaluation
Albert Q. Jiang, Wenda Li, and Mateja Jamnik.                  Forum.
  2023. Multilingual Mathematical Autoformalization.
  CoRR, abs/2311.03755.                                      Ryan McDonald, George Brokos, and Ion Androut-
                                                               sopoulos. 2018. Deep Relevance Ranking Using
Andrew Kane, Yin Ki Ng, and Frank Wm. Tompa. 2022.             Enhanced Document-Query Interactions. In Proceed-
  Dowsing for Answers to Math Questions: Doing                 ings of the 2018 Conference on Empirical Methods
  Better with Less. In Proceedings of the Working              in Natural Language Processing, pages 1849–1860,
  Notes of CLEF 2022 - Conference and Labs of the              Brussels, Belgium. Association for Computational
  Evaluation Forum, Bologna, Italy, September 5th -            Linguistics.


                                                         9
Arvind Neelakantan, Tao Xu, Raul Puri, Alec Rad-                 Stephen Robertson, S. Walker, S. Jones, M. M. Hancock-
  ford, Jesse Michael Han, Jerry Tworek, Qiming                     Beaulieu, and M. Gatford. 1995. Okapi at TREC-3.
  Yuan, Nikolas Tezak, Jong Wook Kim, Chris Hallacy,                In Overview of the Third Text REtrieval Conference
  Johannes Heidecke, Pranav Shyam, Boris Power,                    (TREC-3), pages 109–126. Gaithersburg, MD: NIST.
  Tyna Eloundou Nekoul, Girish Sastry, Gretchen
  Krueger, David Schnurr, Felipe Petroski Such, Kenny            Stephen Robertson and Hugo Zaragoza. 2009. The
  Hsu, Madeleine Thompson, Tabarak Khan, Toki                       Probabilistic Relevance Framework: BM25 and Be-
  Sherbakov, Joanne Jang, Peter Welinder, and Lilian               yond. Found. Trends Inf. Retr., 3(4):333–389.
  Weng. 2022. Text and Code Embeddings by Con-
  trastive Pre-Training. CoRR, abs/2201.10005.                   Gerard Salton and Christopher Buckley. 1988. Term-
                                                                   weighting approaches in automatic text retrieval. In-
Yin Ki Ng, Dallas J. Fraser, Besat Kassaie, George                 formation Processing & Management, 24(5):513–
  Labahn, Mirette S. Marzouk, Frank Wm. Tompa, and                 523.
  Kevin Wang. 2020. Dowsing for Math Answers with
  Tangent-L. In Working Notes of CLEF 2020 - Con-                Hongjin Su, Weijia Shi, Jungo Kasai, Yizhong Wang,
  ference and Labs of the Evaluation Forum, Thessa-                Yushi Hu, Mari Ostendorf, Wen-tau Yih, Noah A.
  loniki, Greece, September 22-25, 2020, volume 2696               Smith, Luke Zettlemoyer, and Tao Yu. 2023. One
  of CEUR Workshop Proceedings. CEUR-WS.org.                       Embedder, Any Task: Instruction-Finetuned Text Em-
Yin Ki Ng, Dallas J. Fraser, Besat Kassaie, and                    beddings. In Findings of the Association for Compu-
  Frank Wm. Tompa. 2021. Dowsing for Answers                       tational Linguistics: ACL 2023, pages 1102–1121,
  to Math Questions: Ongoing Viability of Traditional              Toronto, Canada. Association for Computational Lin-
  MathIR. In Proceedings of the Working Notes of                   guistics.
  CLEF 2021 - Conference and Labs of the Evalua-
  tion Forum, Bucharest, Romania, September 21st -               Laurens van der Maaten and Geoffrey Hinton. 2008.
  to - 24th, 2021, volume 2936 of CEUR Workshop                    Visualizing Data using t-SNE. Journal of Machine
  Proceedings, pages 63–81. CEUR-WS.org.                           Learning Research, 9(86):2579–2605.

Jianmo Ni, Gustavo Hernandez Abrego, Noah Con-                   Liang Wang, Nan Yang, Xiaolong Huang, Binx-
   stant, Ji Ma, Keith Hall, Daniel Cer, and Yinfei Yang.          ing Jiao, Linjun Yang, Daxin Jiang, Rangan Ma-
   2022a. Sentence-T5: Scalable Sentence Encoders                  jumder, and Furu Wei. 2022. Text Embeddings by
   from Pre-trained Text-to-Text Models. In Findings of            Weakly-Supervised Contrastive Pre-training. CoRR,
   the Association for Computational Linguistics: ACL              abs/2212.03533.
   2022, pages 1864–1874, Dublin, Ireland. Association
   for Computational Linguistics.                                Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang,
                                                                   Rangan Majumder, and Furu Wei. 2024. Improv-
Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Her-              ing Text Embeddings with Large Language Models.
   nandez Abrego, Ji Ma, Vincent Zhao, Yi Luan, Keith              CoRR, abs/2401.00368.
   Hall, Ming-Wei Chang, and Yinfei Yang. 2022b.
   Large Dual Encoders Are Generalizable Retrievers.             Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas
   In Proceedings of the 2022 Conference on Empiri-                Muennighof. 2023. C-Pack: Packaged Resources
   cal Methods in Natural Language Processing, pages               To Advance General Chinese Embedding. CoRR,
   9844–9855, Abu Dhabi, United Arab Emirates. As-                 abs/2309.07597.
   sociation for Computational Linguistics.
                                                                 Chenyan Xiong, Zhuyun Dai, Jamie Callan, Zhiyuan
Rodrigo Nogueira, Zhiying Jiang, Ronak Pradeep, and
                                                                   Liu, and Russell Power. 2017. End-to-End Neural
  Jimmy Lin. 2020. Document Ranking with a Pre-
                                                                   Ad-hoc Ranking with Kernel Pooling. In Proceed-
  trained Sequence-to-Sequence Model. In Findings
                                                                   ings of the 40th International ACM SIGIR Confer-
  of the Association for Computational Linguistics:
                                                                   ence on Research and Development in Information
  EMNLP 2020, pages 708–718, Online. Association
                                                                   Retrieval, SIGIR ’17, page 55–64, New York, NY,
  for Computational Linguistics.
                                                                   USA. Association for Computing Machinery.
Yifan Qiao, Chenyan Xiong, Zhenghao Liu, and
  Zhiyuan Liu. 2019. Understanding the Behaviors                 Richard Zanibbi and Dorothea Blostein. 2012. Recog-
  of BERT in Ranking. CoRR, abs/1904.07531.                        nition and retrieval of mathematical expressions. Int.
                                                                   J. Document Anal. Recognit., 15(4):331–357.
Yingqi Qu, Yuchen Ding, Jing Liu, Kai Liu, Ruiyang
  Ren, Wayne Xin Zhao, Daxiang Dong, Hua Wu, and                 Richard Zanibbi, Kenny Davila, Andrew Kane, and
  Haifeng Wang. 2021. RocketQA: An Optimized                       Frank Wm. Tompa. 2016. Multi-Stage Math For-
  Training Approach to Dense Passage Retrieval for                 mula Search: Using Appearance-Based Similarity
  Open-Domain Question Answering. In Proceedings                   Metrics at Scale. In Proceedings of the 39th Inter-
  of the 2021 Conference of the North American Chap-               national ACM SIGIR Conference on Research and
  ter of the Association for Computational Linguistics:            Development in Information Retrieval, SIGIR ’16,
  Human Language Technologies, pages 5835–5847,                    page 145–154, New York, NY, USA. Association for
  Online. Association for Computational Linguistics.               Computing Machinery.


                                                            10
Wei Zhong, Sheng-Chieh Lin, Jheng-Hong Yang, and                      Informal Statement (ours): Dependent if-
 Jimmy Lin. 2023. One Blade for One Purpose: Ad-                   then-else equivalence: For any proposition P that
 vancing Math Information Retrieval using Hybrid
                                                                   is decidable, and any elements c, A, and B, the
 Search. In Proceedings of the 46th International
 ACM SIGIR Conference on Research and Devel-                       expression ‘if P then A else B’ is equal to c if and
 opment in Information Retrieval, SIGIR ’23, page                  only if either there exists a proof h such that A h is
 141–151, New York, NY, USA. Association for Com-                  equal to c, or there exists a proof h such that B h is
 puting Machinery.                                                 equal to c.
Wei Zhong, Shaurya Rohatgi, Jian Wu, C. Lee Giles,                    In this example, the informalized statement pro-
 and Richard Zanibbi. 2020. Accelerating Substruc-                 vided by (Jiang et al., 2023) retains the "dite" no-
 ture Similarity Search for Formula Retrieval. In                  tation, which may be difficult for readers unfamil-
 Advances in Information Retrieval: 42nd European
 Conference on IR Research, ECIR 2020, Lisbon, Por-
                                                                   iar with mathlib4 naming conventions. In con-
 tugal, April 14–17, 2020, Proceedings, Part I, page               trast, our informalized statement translates "dite"
 714–727, Berlin, Heidelberg. Springer-Verlag.                     into "dependent if-then-else," making the statement
                                                                   more accessible. This translation was achieved
Wei Zhong, Yuqing Xie, and Jimmy Lin. 2022a. Apply-
  ing Structural and Dense Semantic Matching for the               by extracting the definition of "dite" and its docu-
 ARQMath Lab 2022, CLEF. In Proceedings of the                     mentation string "Dependent if-then-else..." in the
 Working Notes of CLEF 2022 - Conference and Labs                  prompt, demonstrating how additional context en-
  of the Evaluation Forum, Bologna, Italy, September               hances the interpretation and conversion of formal
  5th - to - 8th, 2022, volume 3180 of CEUR Workshop
  Proceedings, pages 147–170. CEUR-WS.org.
                                                                   theorems into informal language.

Wei Zhong, Jheng-Hong Yang, Yuqing Xie, and Jimmy                  B   Prompt for Query Augmentation
  Lin. 2022b. Evaluating Token-Level and Passage-
  Level Dense Retrieval Models for Math Information                In this section, we present the prompt template for
  Retrieval. In Findings of the Association for Com-               query augmentation, as illustrated in Figure 5. We
  putational Linguistics: EMNLP 2022, Abu Dhabi,                   outline specific principles for query augmentation,
 United Arab Emirates, December 7-11, 2022, pages
 1092–1102. Association for Computational Linguis-                 highlighting the importance of providing precise
  tics.                                                            information, using LaTeX for mathematical expres-
                                                                   sions, and clarifying ambiguous inputs. Addition-
Wei Zhong and Richard Zanibbi. 2019. Structural Simi-
                                                                   ally, we offer examples of query augmentations to
  larity Search for Formulas Using Leaf-Root Paths in
  Operator Subtrees. In Advances in Information Re-                enhance understanding of the task.
  trieval - 41st European Conference on IR Research,
 ECIR 2019, Cologne, Germany, April 14-18, 2019,                   C    Implementation Details
 Proceedings, Part I, volume 11437 of Lecture Notes
  in Computer Science, pages 116–129. Springer.                    In this section, we provide the implementation de-
                                                                   tails of our experiments.
A         Example of Informalized Mathlib4                            We use default task instructions in UAE-Large-
          Statements                                               V1. For E5mistral-7b , we employ different task in-
In this section, we provide an example comparing                   structions for the document and query in the non-
the informalized mathlib4 statement generated by                   augmented query setting and the same task instruc-
(Jiang et al., 2023), which used GPT-4 without any                 tions for both in the query augmentation setting,
additional context, to the statement produced by                   as shown in Table 7. Notably, the original im-
our approach that incorporates additional context.                 plementation of E5mistral-7b omits document-side
                                                                   task instructions to reduce computational costs dur-
  Formal Statement: theorem dite_eq_iff {α :                       ing document indexing in multiple retrieval tasks.
Sort u_2} {P : Prop} [Decidable P] {c : α} {A : P                  Given the complexity of the theorem retrieval task,
→ α} {B : ¬P → α} : dite P A B = c ↔ (∃ h, A h                     we have modified this approach to use two-sided
= c) ∨ ∃ h, B h = c                                                prompts.
                                                                      During evaluation, inputs to the embedding
   Informal Statement (Jiang et al., 2023)11 :
                                                                   model exceeding 4096 characters were truncated
dite P A B equals c if and only if there exists a
                                                                   due to GPU memory limitations. For all tested
proof h such that A h equals c, or there exists a
                                                                   models, the corpus embedding process was com-
proof h such that B h equals c.
                                                                   pleted within three hours on a single Nvidia V100
    11
         https://github.com/albertqjiang/MMA/tree/main/data        GPU with 16GB of GPU memory.

                                                              11
    Input:                                                                                                                     retrieval instruction ("Given a math search query,
    System message: Suppose you are an expert in mathematics and Lean4. Your task is to rewrite a short, vague
    input description of a mathematical theorem into a detailed, explicit statement of the theorem, first written in
                                                                                                                               retrieve theorems mathematically equivalent to the
    natural mathematical language, then in the formal language of Lean4.
                                                                                                                               query"), and a Lean 4 retrieval instruction ("Given a
    Output Format

    Your output must contain exactly two parts. The first part is a natural mathematical language statement, starting
                                                                                                                               math search query, retrieve Lean 4 written theorems
    with a theorem name, followed by the detailed statement of the theorem. The second part is a Lean4 code block,
    write the formal theorem statement directly without import before or proof following. NO other paragraph is
    allowed to appear in the output.
                                                                                                                               that mathematically match the query").
    Principles of Output                                                                                                          As illustrated in Figure 6, clusters of theorem
    1. You should provide as much information and be as precise as possible.
    2. The natural language part should be accessible to mathematicians. Additionally, please express the
    mathematical formulas in LaTeX when necessary.
                                                                                                                               names appear in the results produced by all four
    3. Even in the case that the input is very vague, you should guess a most similar mathematical theorem and write
    it out explicitly.
    4. The formal statement can assume certain definitions in hypothesis is already formalized, in the case you are not
                                                                                                                               embedding models. However, these clusters van-
    sure whether or not.
                                                                                                                               ish when we provide E5mistral-7b with mathematics-
    Example1

    Input description
                                                                                                                               aware task instructions. Given that we assume
    The image of a compact set under a continuous function is compact.                                                         all queries within the same query group (denoted
    Output                                                                                                                     by identical colors in Figure 6) have the same
    Theorem (Image of a Compact Set Under a Continuous Function):
    Let \(f: X \rightarrow Y\) be a continuous function between two topological spaces \(X\) and \(Y\). If \(K\) is a          search intent, they should be proximal on the graph,
    compact subset of \(X\), then the image \(f(K)\) is a compact subset of \(Y\).

    theorem image_compact_of_compact {X Y : Type*} [TopologicalSpace X] [TopologicalSpace Y]
                                                                                                                               as t-SNE maintains the relative distance relation-
    (f : X → Y) (K : Set X) (hf : Continuous f) (hK : IsCompact K) : IsCompact (f '' K) :=

    <...other examples...>
                                                                                                                               ships between vectors. Thus, the more effective
    Now, the statement for you to rewrite is:                                                                                  the embedding engine, the more closely the dots
    Input description                                                                                                          of the same color group together. A comparison
    degree of product of two polynomials equals to sum of degree
                                                                                                                               of subfigures 6c and 6d with 6a and 6b reveals
    Output:                                                                                                                    that text-embedding-3-large and E5mistral-7b demon-
    Theorem (Degree of the Product of Two Polynomials):
    Let \(P(x)\) and \(Q(x)\) be two non-zero polynomials over a field \(F\). The degree of the product \(P(x)Q(x)\) is
                                                                                                                               strate superior performance in discerning mathe-
    equal to the sum of the degrees of \(P(x)\) and \(Q(x)\). Formally, if \(\deg(P) = m\) and \(\deg(Q) = n\), then
    \(\deg(PQ) = m + n\).                                                                                                      matical search intentions, aligning with our main
    theorem degree_product_eq_sum_degree {F : Type*} [Field F] {P Q : Polynomial F}
    (hP : P ≠ 0) (hQ : Q ≠ 0) : Polynomial.degree (P * Q) = Polynomial.degree P + Polynomial.degree Q :=                       results (Table 3).
                                                                                                                                  The presence of theorem name clusters in these
                                                                                                                               subfigures, however, contradicts this principle, sug-
           Figure 5: Prompt for query augmentations.
                                                                                                                               gesting that the embedding models perceive these
 Query aug. &
                              Side         Input with Task Instructions
                                                                                                                               theorem names as more similar to each other rather
  Doc Type
                                           "Instruct: Given a math search query, retrieve                                      than correctly associating them with their respec-
                                           theorems stated in Lean 4 that mathematically
                             Query
                                           match the query \n Query:{F+IF augmented
                                                                                                                               tive query groups. While this might be accept-
                                           query}"                                                                             able for other retrieval tasks, it is inappropriate for
 None & Formal                             "Instruct: Represent the given formal math
                              Doc
                                           statement written in Lean 4 for retrieving                                          our mathematical information retrieval context. In
                                           related statement by natural language query \n
                                           Doc:{Formal statement}"                                                             contrast, the absence of theorem clusters in sub-
                                           "Instruct: Retrieve math theorems stated in
                                           bilingual Lean 4 + natural language that are                                        figures 6e and 6f suggests that these embedding
                             Query
                                           mathematically equivalent to the given one \n
                                           Query:{query}"
                                                                                                                               methods successfully group theorem names with
  F+IF & F+IF                              "Instruct: Retrieve math theorems stated in
                                           bilingual Lean 4 + natural language that are
                                                                                                                               their corresponding statements, despite their no-
                              Doc
                                           mathematically equivalent to the given one \n                                       table differences in appearance and structure. This
                                           Doc:{F + IF statement}"
                                                                                                                               indicates their proficiency in comprehending math-
Table 7: Task instructions used in E5mistral-7b . Here                                                                         ematical theorems and recognizing search intents.
"aug." stands for augmentation, and F and IF stands for                                                                        In summary, appropriate task instructions enhance
formal and informal respectively. The "None & Formal"                                                                          the embedding models’ sensitivity to the search in-
setting is used as baseline, and "F+IF & F+IF" is used                                                                         tents of mathematical concepts, thereby improving
in our method.
                                                                                                                               retrieval effectiveness on mathlib4.

D        Ablation Study on Task Instructions                                                                                   E   Models for Query Augmentation

In this section, we investigate the impact of task                                                                             In this section, we compare the performance of two
instructions on the theorem retrieval performance.                                                                             LLMs, DeepSeek-V2-Chat and GPT-4, for query
We present a visualization of the embeddings of all                                                                            augmentation. Table 8 presents the performance
50 queries, generated by four embedding engines                                                                                of both models using the informal+formal corpus
in our benchmark, using t-SNE(van der Maaten and                                                                               setting, with results averaged over 10 runs.
Hinton, 2008). We use the default task instruction                                                                                As shown, DeepSeek-V2-Chat not only outper-
for UAE-Large-V1. For E5mistral-7b , we test three                                                                             forms GPT-4 in terms of effectiveness but also of-
instructions: an empty instruction, a mathematics                                                                              fers a significantly lower cost. The results suggest

                                                                                                                          12
(a) text-embedding-ada-002                          (b) UAE-Large-V1 with de-
(without task instruction)                          fault instruction




(c) text-embedding-3-large                          (d) E5mistral-7b with empty in-
(without task instruction)                          struction




(e) E5mistral-7b with Math re-                      (f) E5mistral-7b with Lean 4 re-
trieving instruction                                trieving instruction

Figure 6: t-SNE visualization of the embeddings of all
queries in our benchmark. Each dot denotes a distinct
query, with queries within the same query group sharing
identical colors. The shape of the markers differentiates
the four distinct query categories. Theorem name clus-
ters are emphasized with circles.

 API                  nDCG@20   P@10    R@10    Cost per 1M input tokens   Cost per 1M output tokens
 gpt-4-0125-preview    0.721    0.195   0.911           $10.00                      $30.00
 deepseek-chat         0.749    0.202   0.933            $0.14                       $0.14



Table 8: Performance of DeepSeek-V2-Chat and GPT-4
for query augmentation.


that DeepSeek-V2-Chat is a more efficient and cost-
effective choice for query augmentation tasks.




                                                                                                       13
